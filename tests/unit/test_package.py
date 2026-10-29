"""TR-001 / TR-003: tests run on Python 3.13 inside the project virtual environment."""

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


@pytest.mark.req("TR-001", "TR-003")
def test_package_imports_on_python_313() -> None:
    import testbondanh

    assert sys.version_info[:2] == (3, 13)
    assert Path(sys.prefix).resolve() == (REPO / ".venv").resolve()
    assert isinstance(testbondanh.__version__, str)
