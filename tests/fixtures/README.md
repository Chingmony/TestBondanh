# Test fixtures

All fixtures are synthetic. They are never derived from real scans, even after editing (TS-13).

- IPv4 addresses only from `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` (TS-10)
- IPv6 addresses only from `2001:db8::/32` (TS-10)
- MAC addresses only from `00:00:5E:00:53:00` – `00:00:5E:00:53:FF` (TS-10)
- Hostnames only under `.example` or `.test` (TS-11)
- Each fixture starts with a comment stating its purpose and requirement IDs (TS-12)
- Comparison cases live in `compare/<case-name>/baseline.xml` and `newer.xml` (TS-14)

`tests/security/test_fixture_addresses.py` enforces the address rules on every file in this folder (TR-SEC-03).
