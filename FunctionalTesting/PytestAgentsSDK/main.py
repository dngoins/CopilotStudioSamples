import argparse
import os
import sys
from datetime import datetime
from pathlib import Path


def run_tests(test_path: str | None = None, report_path: str | None = None, verbose: bool = False,
			  maxfail: int | None = None, self_contained_html: bool = True) -> int:
	"""Run the multi_turn_eval_openai tests programmatically with pytest.

	Args:
		test_path: Path to the test module/file to run. Defaults to tests/multi_turn_eval_openai.py
		report_path: Path to write the HTML report. If None, a timestamped file is created under reports/.
		verbose: If True, run pytest with verbose output.
		maxfail: If provided, stop after this many failures.
		self_contained_html: If True, embed assets in the HTML report.

	Returns:
		The pytest exit code (0 means success)
	"""
	try:
		import pytest  # noqa: WPS433 (runtime import by design)
	except ImportError as e:
		print("pytest is required to run tests. Install dev dependencies (including pytest and pytest-html).")
		raise

	# Ensure we run relative to this file's directory so relative paths in tests work
	base_dir = Path(__file__).parent.resolve()
	os.chdir(base_dir)

	# Defaults
	test_path_str: str = test_path or str(Path("tests") / "multi_turn_eval_openai.py")

	reports_dir = Path("reports")
	reports_dir.mkdir(parents=True, exist_ok=True)

	if report_path is None:
		stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		report_path_path: Path = reports_dir / f"multi_turn_eval_openai_{stamp}.html"
	else:
		rp = Path(report_path)
		if not rp.is_absolute():
			rp = (reports_dir / rp).resolve()
		rp.parent.mkdir(parents=True, exist_ok=True)
		report_path_path = rp

	pytest_args: list[str] = [test_path_str, f"--html={str(report_path_path)}"]
	if self_contained_html:
		pytest_args.append("--self-contained-html")
	if verbose:
		pytest_args.append("-v")
	if isinstance(maxfail, int) and maxfail > 0:
		pytest_args.extend(["--maxfail", str(maxfail)])

	print(f"Running tests: {test_path_str}")
	print(f"Report: {str(report_path_path)}")

	# Execute pytest
	return pytest.main(pytest_args)


def parse_args(argv: list[str]) -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Run multi_turn_eval_openai tests and produce an HTML report.")
	parser.add_argument("--test", dest="test_path", default=None,
						help="Path to test file or test node (default: tests/multi_turn_eval_openai.py)")
	parser.add_argument("--report", dest="report_path", default=None,
						help="HTML report path under reports/ (default: timestamped file)")
	parser.add_argument("--no-self-contained-html", dest="self_contained_html", action="store_false",
						help="Disable embedding assets in the HTML report")
	parser.add_argument("-v", "--verbose", action="store_true", help="Verbose pytest output")
	parser.add_argument("--maxfail", type=int, default=None, help="Stop after the first N failures")
	return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
	args = parse_args(argv or sys.argv[1:])
	return run_tests(
		test_path=args.test_path,
		report_path=args.report_path,
		verbose=args.verbose,
		maxfail=args.maxfail,
		self_contained_html=args.self_contained_html,
	)


if __name__ == "__main__":
	sys.exit(main())

