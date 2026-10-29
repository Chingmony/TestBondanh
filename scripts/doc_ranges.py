"""Find network identifiers outside documentation-reserved ranges (TR-SEC-03, TS-10).

Shared by tests/security/test_fixture_addresses.py and the repository audit (T-014).
When in doubt the checker reports: a false alarm costs a look, a miss can publish
real network data.
"""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from pathlib import Path

DOCUMENTATION_NETWORKS = tuple(
    ipaddress.ip_network(net)
    for net in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24", "2001:db8::/32")
)
DOCUMENTATION_MAC_PREFIX = "00:00:5E:00:53:"  # RFC 7042

_IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?(?!\d)")
_IPV6 = re.compile(r"(?<![\w:])(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}(?:/\d{1,3})?(?![\w:])")
_MAC = re.compile(r"(?<![\w:-])(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}(?![\w:-])")


@dataclass(frozen=True)
class Finding:
    value: str
    reason: str


def _is_documentation_network(text: str) -> bool | None:
    """True/False for a valid address or CIDR block; None if the text is not one."""
    try:
        network = ipaddress.ip_network(text, strict=False)
    except ValueError:
        return None
    return any(
        network.version == doc.version and network.subnet_of(doc)  # type: ignore[arg-type]
        for doc in DOCUMENTATION_NETWORKS
    )


def find_non_documentation_identifiers(text: str) -> list[Finding]:
    """Return every IP or MAC address in ``text`` outside the documentation ranges."""
    found: list[tuple[int, Finding]] = []
    for pattern, reason in ((_IPV4, "non_documentation_ipv4"), (_IPV6, "non_documentation_ipv6")):
        for match in pattern.finditer(text):
            if _is_documentation_network(match.group()) is False:
                found.append((match.start(), Finding(match.group(), reason)))
    for match in _MAC.finditer(text):
        normalised = match.group().replace("-", ":").upper()
        if not normalised.startswith(DOCUMENTATION_MAC_PREFIX):
            found.append((match.start(), Finding(match.group(), "non_documentation_mac")))
    return [finding for _, finding in sorted(found, key=lambda item: item[0])]


def scan_file(path: Path) -> list[Finding]:
    """Check one file. A file that is not UTF-8 text is reported, never skipped."""
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return [Finding(path.name, "not_utf8")]
    return find_non_documentation_identifiers(text)
