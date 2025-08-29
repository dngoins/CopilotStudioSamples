import asyncio
from os import environ, path

from dotenv import load_dotenv
load_dotenv()

from msal import ConfidentialClientApplication

from .config import McsConnectionSettings
from .msal_cache_plugin import get_msal_token_cache
from microsoft_agents.copilotstudio.client import (
    CopilotClient,
)

class CopilotStudioClient:
    def __init__(self):
        self.connection_settings = McsConnectionSettings()
        self.token = self._acquire_token()
        self.client = CopilotClient(self.connection_settings, self.token)
        # Expose conversation_id for convenience in tests
        self.conversation_id: str = ""

    def _acquire_token(self) -> str:
        cache_path = environ.get("TOKEN_CACHE_PATH") or path.join(path.dirname(__file__), "../../bin/token_cache.bin")
        cache = get_msal_token_cache(cache_path)

        app = ConfidentialClientApplication(
            client_id=self.connection_settings.app_client_id,
            authority=f"https://login.microsoftonline.com/{self.connection_settings.tenant_id}",
            client_credential=self.connection_settings.client_credential,
            token_cache=cache,
        )

        token_scopes = ["https://api.powerplatform.com/.default"]
        # Client credentials flow (confidential client). MSAL will use the cache under the hood.
        result = app.acquire_token_for_client(scopes=token_scopes)

        if isinstance(result, dict) and result.get("access_token"):
            return result["access_token"]
        error_desc = None
        if isinstance(result, dict):
            error_desc = result.get("error_description") or result.get("error")
        raise Exception(f"Token acquisition failed: {error_desc or 'unknown error'}")
