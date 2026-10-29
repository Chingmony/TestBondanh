"""Single verification entry point (TR-067, DEC-031, Test Strategy §11.1).

Usage (from the repository root):
    .venv\\Scripts\\python.exe scripts\\verify.py           full run
    .venv\\Scripts\\python.exe scripts\\verify.py --quick   skip slow and performance tests

Runs every step even after a failure, then prints a summary. Exit code 0 only if
no step failed.
"""

from __future__ import annotations

import argparse
import io
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VENV_PYTHON = REPO / ".venv" / "Scripts" / "python.exe"
CORE_COVERAGE_INCLUDE = "src/testbondanh/domain/*,src/testbondanh/reporting/*"
CORE_COVERAGE_MINIMUM = "95"  # DEC-038; overall 85 % is fail_under in pyproject.toml

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIPPED"


def _run(args: list[str]) -> tuple[int, str]:
    # Fixed argument lists built in this file; executed with our own interpreter, no shell.
    result = subprocess.run(  # noqa: S603
        [sys.executable, *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = result.stdout + result.stderr
    print(output, end="" if output.endswith("\n") or not output else "\n")
    return result.returncode, output


def _step(title: str, args: list[str]) -> str:
    print(f"\n== {title} ==", flush=True)
    code, _ = _run(args)
    return PASS if code == 0 else FAIL


def _core_coverage() -> str:
    print("\n== Coverage: domain and reporting >= 95 % (DEC-038) ==", flush=True)
    code, output = _run(
        [
            "-m",
            "coverage",
            "report",
            f"--include={CORE_COVERAGE_INCLUDE}",
            f"--fail-under={CORE_COVERAGE_MINIMUM}",
        ]
    )
    if code != 0 and "No data to report" in output:
        print("No domain or reporting code yet; threshold not applicable.")
        return PASS
    return PASS if code == 0 else FAIL


def _not_yet(title: str, task: str) -> str:
    print(f"\n== {title} ==\nNot implemented yet ({task}).", flush=True)
    return SKIP


def main(argv: list[str] | None = None) -> int:
    # Windows consoles and redirects default to cp1252; tool output can contain any character.
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Run all TestBondanh verification steps.")
    parser.add_argument("--quick", action="store_true", help="skip slow and performance tests")
    options = parser.parse_args(argv)

    if Path(sys.executable).resolve() != VENV_PYTHON.resolve():
        print(f"FAIL: run with {VENV_PYTHON}, not {sys.executable} (TR-003)")
        return 1

    pytest_args = ["-m", "pytest", "--cov", "--cov-report=term-missing"]
    if options.quick:
        pytest_args += ["-m", "not slow and not performance"]

    results = {
        "0 Locked tests unchanged": _not_yet("0 Locked tests unchanged", "T-012"),
        "1 ruff check": _step("1 ruff check", ["-m", "ruff", "check", "."]),
        "2 ruff format": _step("2 ruff format", ["-m", "ruff", "format", "--check", "."]),
        "3 mypy --strict": _step("3 mypy --strict", ["-m", "mypy"]),
        "4 pytest + coverage >= 85 %": _step("4 pytest + coverage >= 85 %", pytest_args),
        "4b core coverage >= 95 %": _core_coverage(),
        "5 traceability": _step("5 traceability", ["scripts/trace.py", "--check"]),
    }

    print("\n== Summary ==")
    for name, status in results.items():
        print(f"{status:8} {name}")
    failed = [name for name, status in results.items() if status == FAIL]
    print("\nRESULT:", "FAIL" if failed else "PASS", "(quick)" if options.quick else "(full)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
