"""FR-095 / TR-SEC-02: no test may open a network connection.

The autouse fixture in tests/conftest.py must make every connection attempt fail
with an error that is not an OSError, so code that handles network errors cannot
swallow it. The target is a documentation-reserved address (TS-10).
"""

import socket

import pytest

TARGET = ("192.0.2.1", 9)  # TEST-NET-1, discard port: never a real host


@pytest.mark.req("FR-095", "TR-SEC-02")
def test_network_block_is_active() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        with pytest.raises(RuntimeError, match="Network access blocked"):
            sock.connect(TARGET)


@pytest.mark.req("FR-095", "TR-SEC-02")
def test_network_block_covers_connect_ex() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        with pytest.raises(RuntimeError, match="Network access blocked"):
            sock.connect_ex(TARGET)


@pytest.mark.req("FR-095", "TR-SEC-02")
def test_network_block_covers_create_connection() -> None:
    with pytest.raises(RuntimeError, match="Network access blocked"):
        socket.create_connection(TARGET, timeout=1)
