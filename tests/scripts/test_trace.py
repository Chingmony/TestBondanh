"""TS-31 / TS-32 (DEC-039): every test is tagged with real requirement IDs.

scripts/trace.py reads test files statically (no import) and the approved
documents, and reports untagged tests and unknown or malformed IDs.
"""

from pathlib import Path

import pytest
from scripts.trace import Problem, check, main, report

REPO = Path(__file__).resolve().parents[2]


def _project(tmp_path: Path, docs: str, tests: str) -> tuple[Path, Path]:
    docs_dir = tmp_path / "docs" / "requirements"
    docs_dir.mkdir(parents=True)
    (docs_dir / "FRD.md").write_text(docs, encoding="utf-8")
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_sample.py").write_text(tests, encoding="utf-8")
    return tmp_path / "docs", tests_dir


@pytest.mark.req("TS-31", "TS-32")
def test_tagged_test_with_known_id_has_no_problems(tmp_path: Path) -> None:
    docs, tests = _project(
        tmp_path,
        "### FR-021 — Size limit\n",
        'import pytest\n\n@pytest.mark.req("FR-021")\ndef test_x():\n    pass\n',
    )
    assert check(docs, tests) == []


@pytest.mark.req("TS-32")
def test_untagged_test_is_reported(tmp_path: Path) -> None:
    docs, tests = _project(tmp_path, "FR-021\n", "def test_y():\n    pass\n")
    assert check(docs, tests) == [Problem("untagged_test", "test_sample.py::test_y", "")]


@pytest.mark.req("TS-32")
def test_empty_req_marker_is_reported(tmp_path: Path) -> None:
    docs, tests = _project(
        tmp_path,
        "FR-021\n",
        "import pytest\n\n@pytest.mark.req()\ndef test_y():\n    pass\n",
    )
    assert check(docs, tests) == [Problem("untagged_test", "test_sample.py::test_y", "")]


@pytest.mark.req("TS-32")
def test_unknown_id_is_reported(tmp_path: Path) -> None:
    docs, tests = _project(
        tmp_path,
        "FR-021\n",
        'import pytest\n\n@pytest.mark.req("FR-999")\ndef test_z():\n    pass\n',
    )
    assert check(docs, tests) == [Problem("unknown_id", "test_sample.py::test_z", "FR-999")]


@pytest.mark.req("TS-32")
@pytest.mark.parametrize("bad_id", ["FR21", "fr-021", "DEC-001", "FR-021 "])
def test_malformed_or_non_requirement_id_is_reported(tmp_path: Path, bad_id: str) -> None:
    docs, tests = _project(
        tmp_path,
        "FR-021 DEC-001\n",
        f'import pytest\n\n@pytest.mark.req("{bad_id}")\ndef test_z():\n    pass\n',
    )
    assert check(docs, tests) == [Problem("invalid_id", "test_sample.py::test_z", bad_id)]


@pytest.mark.req("TS-31", "TS-32")
def test_methods_in_test_classes_are_checked(tmp_path: Path) -> None:
    docs, tests = _project(
        tmp_path,
        "FR-021\n",
        "class TestThing:\n    def test_m(self):\n        pass\n",
    )
    assert check(docs, tests) == [Problem("untagged_test", "test_sample.py::TestThing::test_m", "")]


@pytest.mark.req("TS-32")
def test_helper_functions_are_not_tests(tmp_path: Path) -> None:
    docs, tests = _project(tmp_path, "FR-021\n", "def _helper():\n    pass\n")
    assert check(docs, tests) == []


@pytest.mark.req("TS-31")
def test_ids_are_found_in_any_document(tmp_path: Path) -> None:
    docs, tests = _project(
        tmp_path,
        "nothing here\n",
        'import pytest\n\n@pytest.mark.req("TR-SEC-03")\ndef test_x():\n    pass\n',
    )
    (docs / "architecture").mkdir()
    (docs / "architecture" / "TRD.md").write_text("| **TR-SEC-03** | ... |\n", encoding="utf-8")
    assert check(docs, tests) == []


@pytest.mark.req("TS-31")
def test_report_maps_requirement_ids_to_tests(tmp_path: Path) -> None:
    docs, tests = _project(
        tmp_path,
        "FR-021 FR-022\n",
        "import pytest\n\n"
        '@pytest.mark.req("FR-021", "FR-022")\ndef test_a():\n    pass\n\n'
        '@pytest.mark.req("FR-021")\ndef test_b():\n    pass\n',
    )
    assert report(docs, tests) == {
        "FR-021": ["test_sample.py::test_a", "test_sample.py::test_b"],
        "FR-022": ["test_sample.py::test_a"],
    }


@pytest.mark.req("TS-32")
def test_check_command_exit_codes(tmp_path: Path) -> None:
    good_docs, good_tests = _project(
        tmp_path / "good",
        "FR-021\n",
        'import pytest\n\n@pytest.mark.req("FR-021")\ndef test_x():\n    pass\n',
    )
    bad_docs, bad_tests = _project(tmp_path / "bad", "FR-021\n", "def test_y():\n    pass\n")
    assert main(["--check", "--docs", str(good_docs), "--tests", str(good_tests)]) == 0
    assert main(["--check", "--docs", str(bad_docs), "--tests", str(bad_tests)]) == 1


@pytest.mark.req("TS-31", "TS-32")
def test_repository_is_fully_traceable() -> None:
    assert check(REPO / "docs", REPO / "tests") == []
