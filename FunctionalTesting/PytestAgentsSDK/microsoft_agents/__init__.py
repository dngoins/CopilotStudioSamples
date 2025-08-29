"""
Namespace package shim for microsoft_agents.

This enables merging with installed distributions such as:
	- microsoft-agents-activity  (provides microsoft_agents.activity)
	- microsoft-agents-copilotstudio-client (provides microsoft_agents.copilotstudio)

Do not place concrete modules here unless you also want them discovered
alongside the installed namespace segments.
"""
from pkgutil import extend_path

# Merge this local directory with any other "microsoft_agents" segments found
# on sys.path (PEP 420 alternative for environments that require explicit shim)
__path__ = extend_path(__path__, __name__)  # type: ignore[name-defined]

