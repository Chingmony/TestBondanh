"""Shared pytest configuration.

Network block (FR-095, TR-SEC-02): every test runs with outgoing socket connections
disabled. The error is a RuntimeError, not an OSError, so production code that
handles network errors cannot accidentally swallow it.
"""

import socket
from typing import NoReturn

import pytest


class NetworkAccessBlocked(RuntimeError):
    """Raised when code under test attempts a network connection."""


def _blocked(sock: socket.socket, *args: object, **kwargs: object) -> NoReturn:
    # Close first: socket.create_connection only cleans up after OSError, so without
    # this the half-made socket leaks and raises a ResourceWarning.
    sock.close()
    raise NetworkAccessBlocked("Network access blocked during tests (FR-095, TR-SEC-02)")


@pytest.fixture(autouse=True)
def _block_network(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket.socket, "connect", _blocked)
    monkeypatch.setattr(socket.socket, "connect_ex", _blocked)
