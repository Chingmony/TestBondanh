"""TR-SEC-03 / TS-10: fixtures may contain only documentation-reserved identifiers.

The checker lives in scripts/doc_ranges.py so the repository audit (T-014) can reuse it.

Negative examples are assembled at runtime so this file never contains a literal
non-documentation address that the repository audit would itself report.
"""

from pathlib import Path

import pytest
from scripts.doc_ranges import find_non_documentation_identifiers, scan_file

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _join(sep: str, *parts: str) -> str:
    return sep.join(parts)


@pytest.mark.req("TR-SEC-03", "TS-10")
@pytest.mark.parametrize(
    "value",
    [
        "192.0.2.10",
        "198.51.100.1",
        "203.0.113.254",
        "192.0.2.0/24",
        "2001:db8::1",
        "2001:DB8:0:0:0:0:0:1",
        "00:00:5E:00:53:01",
        "00:00:5e:00:53:ff",
    ],
)
def test_documentation_identifiers_allowed(value: str) -> None:
    assert find_non_documentation_identifiers(f"host {value} seen") == []


@pytest.mark.req("TR-SEC-03", "TS-10")
@pytest.mark.parametrize(
    ("value", "reason"),
    [
        (_join(".", "10", "0", "0", "1"), "non_documentation_ipv4"),
        (_join(".", "8", "8", "8", "8"), "non_documentation_ipv4"),
        (_join(".", "192", "168", "1", "1"), "non_documentation_ipv4"),
        (_join("::", "fe80", "1"), "non_documentation_ipv6"),
        (_join("::", "2001:4860", "8888"), "non_documentation_ipv6"),
        (_join(":", "AA", "BB", "CC", "DD", "EE", "FF"), "non_documentation_mac"),
        (_join(":", "00", "00", "5E", "00", "54", "01"), "non_documentation_mac"),
    ],
)
def test_other_identifiers_reported(value: str, reason: str) -> None:
    findings = find_non_documentation_identifiers(f"host {value} seen")
    assert [(f.value, f.reason) for f in findings] == [(value, reason)]


@pytest.mark.req("TR-SEC-03")
@pytest.mark.parametrize(
    "text",
    [
        "nmap version 7.94",
        'xmloutputversion="1.05"',
        "scan started 12:30:45",
        "ports 1-1000,8080",
    ],
)
def test_non_address_text_not_reported(text: str) -> None:
    assert find_non_documentation_identifiers(text) == []


@pytest.mark.req("TR-SEC-03")
def test_non_utf8_file_is_reported_not_crashed(tmp_path: Path) -> None:
    binary = tmp_path / "binary.xml"
    binary.write_bytes(b"\xf3\x00\xff not text")
    findings = scan_file(binary)
    assert [f.reason for f in findings] == ["not_utf8"]


@pytest.mark.req("TR-SEC-03", "NFR-010")
def test_fixtures_contain_only_documentation_addresses() -> None:
    files = [p for p in FIXTURES.rglob("*") if p.is_file()]
    problems = [
        (str(p.relative_to(FIXTURES)), f.value, f.reason) for p in files for f in scan_file(p)
    ]
    assert problems == []
