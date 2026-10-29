"""TR-SEC-04 / BR-014: Git must never track scan data, databases, reports, or secrets."""

import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]

REQUIRED_PATTERNS = [
    ".venv/",
    "*.db",
    "*.sqlite*",
    "reports/",
    "*.xml",
    "!tests/fixtures/**/*.xml",
    ".coverage",
    "htmlcov/",
    "__pycache__/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".pytest_cache/",
    ".env",
    ".env.*",
    ".claude/settings.local.json",
    "CLAUDE.local.md",
    ".claude/state/",
]


@pytest.mark.req("TR-SEC-04")
def test_gitignore_contains_required_patterns() -> None:
    lines = {
        line.strip() for line in (REPO / ".gitignore").read_text(encoding="utf-8").splitlines()
    }
    missing = [pattern for pattern in REQUIRED_PATTERNS if pattern not in lines]
    assert missing == []


@pytest.mark.req("TR-SEC-04", "BR-014")
@pytest.mark.parametrize(
    ("path", "ignored"),
    [
        ("scan.xml", True),
        ("data/history.db", True),
        ("history.sqlite3", True),
        ("reports/compare-1-2.md", True),
        (".env", True),
        ("tests/fixtures/import/valid/minimal_complete.xml", False),
        ("src/testbondanh/__init__.py", False),
    ],
)
def test_git_ignores_sensitive_paths(path: str, ignored: bool) -> None:
    git = shutil.which("git")
    assert git is not None, "git must be installed to run this test"
    # --no-index: judge the path by .gitignore rules alone, whether or not it exists or is tracked
    result = subprocess.run(  # noqa: S603 — fixed argument list, no shell, no untrusted input
        [git, "check-ignore", "--quiet", "--no-index", path],
        cwd=REPO,
        check=False,
    )
    assert (result.returncode == 0) == ignored
