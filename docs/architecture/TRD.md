# TestBondanh — Technical Requirements Document (TRD)

| Field | Value |
|---|---|
| Document | Technical Requirements Document |
| Project | TestBondanh — Network Security Monitoring Tool |
| Purpose | Define the technologies, versions, technical rules, and toolchain used to implement the approved FRD and NFRs |
| Status | **Approved** — by project owner, 2026-10-27 |
| Version | 1.0 |
| Based on | [BRD v1.0](../requirements/BRD.md), [PRD v1.0](../requirements/PRD.md), [FRD v1.0](../requirements/FRD.md) (all Approved) |
| Owner / Approver | Project owner (Chingmony) |
| Author | Claude Code (drafted under owner direction) |
| Last updated | 2026-10-27 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-27 | Claude Code | Initial draft from approved outline and owner answers (TRD/SAD batch 1) |
| 1.0 | 2026-10-27 | Project owner | Approved as drafted |

## 1. Purpose and Sources

This TRD states *how* the requirements will be met technically: platform, dependencies, parsing, storage, toolchain, code rules, and security controls. Code organisation and component boundaries are defined separately in the SAD.

IDs use `TR-` (technical requirement) and `TR-SEC-` (technical security requirement). Labels **Confirmed / Assumed / Proposed / Open** follow the BRD.

**Verification of facts in this document (2026-10-27):**
- Package versions and licences were read from the PyPI JSON API.
- Local interpreter, SQLite, and expat versions were read from `py -3.13` on the development machine.
- Machine specification was read from Windows system information.

This TRD resolves BRD **OQ-01** (Python version), **OQ-02** (branch name), **OQ-07** (database protection), and PRD **PQ-03** (reference machine).

## 2. Runtime Platform

| ID | Requirement | Status |
|---|---|---|
| **TR-001** | The tool shall run on **Python 3.13** (`requires-python = ">=3.13,<3.14"`). Development uses the installed CPython 3.13.5 (64-bit) or a later 3.13 patch release | Confirmed (DEC-024) |
| **TR-002** | Target operating system is Windows 11 (64-bit). Other platforms are not tested (BRD §10) | Confirmed (C-02) |
| **TR-003** | Development uses a virtual environment at `.venv\` created with `py -3.13 -m venv .venv`. Every script, hook, and tool invocation shall call `.venv\Scripts\python.exe` explicitly, **never** a bare `python`, because `python` on this machine resolves to 3.11.0 | Confirmed (DEC-024) |

> **Note:** Upgrading to the newest 3.13 patch release is recommended for security fixes but is not required to start.

## 3. Dependencies

### 3.1 Runtime

| ID | Requirement |
|---|---|
| **TR-010** | The only third-party runtime dependency shall be **`defusedxml==0.7.1`** (licence: Python Software Foundation License; MIT-compatible) (DEC-025) |
| **TR-011** | All other runtime functionality uses the Python standard library: `argparse`, `sqlite3`, `json`, `ipaddress`, `hashlib`, `secrets`, `random`, `pathlib`, `datetime`, `os`, `sys` |

> **Risk noted:** `defusedxml` 0.7.1 was released in March 2021; later versions (0.8.0rc1/rc2) are pre-releases only. It is a thin, well-known wrapper around the standard library's expat parser, so infrequent releases are not alarming, but compatibility with Python 3.13 must be **proven by test** in the first implementation task (TR-022), not assumed.

### 3.2 Development only (never shipped)

| Package | Version | Licence | Purpose |
|---|---|---|---|
| `pytest` | 9.1.1 | MIT | Test runner |
| `pytest-cov` | 7.1.0 | MIT | Coverage measurement |
| `ruff` | 0.17.3 | MIT | Linting and formatting |
| `mypy` | 2.4.0 | MIT | Static type checking |
| `pip-audit` | 2.10.1 | Apache-2.0 | Known-vulnerability scan of dependencies |
| `setuptools` | 84.2.1 | MIT | Build backend for installing the package and its `testbondanh` command |

| ID | Requirement |
|---|---|
| **TR-012** | Dependencies are installed with standard `venv` + `pip` (DEC-026). Direct dependencies are pinned to exact versions in `pyproject.toml`. The complete installed set, including transitive dependencies, is recorded with exact versions in `requirements-dev.lock.txt` (produced by `pip freeze`) |
| **TR-013** | Adding, removing, or upgrading any dependency requires: a decision-log entry, a licence check (allowed: MIT, BSD, Apache-2.0, PSF, ISC), a clean `pip-audit` run, and owner approval |

## 4. Input Processing

| ID | Requirement | Implements |
|---|---|---|
| **TR-020** | File size shall be read with `os.stat()` and checked against 52,428,800 bytes **before** the file is opened for parsing | FR-021 |
| **TR-021** | XML shall be parsed only with `defusedxml.ElementTree`, with `forbid_dtd=False` (Nmap writes `<!DOCTYPE nmaprun>`), `forbid_entities=True`, `forbid_external=True`. defusedxml security exceptions map to `E-IMP-005`; XML syntax errors map to `E-IMP-004` | FR-022, FR-023 |
| **TR-022** | The first implementation task shall include tests proving, on Python 3.13, that (a) the XXE fixture is rejected, (b) the entity-expansion fixture is rejected within 2 s, and (c) a normal Nmap file with DOCTYPE and stylesheet instruction is accepted | FR-022 |
| **TR-023** | No module may parse untrusted XML with `xml.etree`, `xml.dom`, `xml.sax`, or `lxml` directly. Enforced by ruff's security rules (`S` rule set, which flags unsafe XML parsing) | NFR-003 |
| **TR-024** | Files are read as bytes; the SHA-256 for duplicate detection is computed on those bytes with `hashlib` | FR-026 |
| **TR-025** | Address parsing and normalisation use the standard `ipaddress` module (IPv4, IPv6, CIDR) | FR-030, FR-052 |

## 5. Storage

| ID | Requirement | Implements |
|---|---|---|
| **TR-030** | Storage is a single SQLite database file, `testbondanh.db`, in the data folder, accessed through the standard `sqlite3` module (local SQLite 3.49.1) | BR-002 |
| **TR-031** | Every connection shall enable `PRAGMA foreign_keys = ON` so that deleting a scan cascades to its hosts, ports, and services | FR-041 |
| **TR-032** | Each import runs in a single transaction (`BEGIN IMMEDIATE` … `COMMIT`); any exception triggers `ROLLBACK` | FR-031, NFR-005 |
| **TR-033** | Scan IDs use `INTEGER PRIMARY KEY AUTOINCREMENT`, which guarantees IDs are never reused after deletion | FRD §3 |
| **TR-034** | All SQL shall use parameter placeholders (`?`); building SQL with string formatting is forbidden (enforced by ruff rule `S608`) | Security |
| **TR-035** | Every connection shall enable `PRAGMA secure_delete = ON` so deleted scan data is overwritten in the database file rather than left in free space | PR-006, BR-010 |
| **TR-036** | Schema version is stored in `PRAGMA user_version`. Migrations are forward-only, applied automatically at startup, each in a transaction | Maintainability |
| **TR-037** | **Data at rest** is protected by Windows per-user permissions on `%LOCALAPPDATA%`; no encryption in the MVP. README states that anyone with access to the Windows account can read the database | Confirmed (DEC-027; resolves OQ-07) |

## 6. File Handling

| ID | Requirement | Implements |
|---|---|---|
| **TR-040** | All paths are handled with `pathlib.Path`; no string concatenation of paths | NFR-007 |
| **TR-041** | All text files are read and written with explicit `encoding="utf-8"`. Reports use `\n` line endings for deterministic output | NFR-008 |
| **TR-042** | Report files are created with exclusive-create mode (`"x"`), so an existing file is never overwritten; on name collision the next suffix is tried. Content is written to a temporary file in the same folder and then renamed into place, so no partial report remains after failure | FR-080, FR-081 |
| **TR-043** | The default data folder is `Path(os.environ["LOCALAPPDATA"]) / "TestBondanh"` | FR-010 |
| **TR-044** | Git detection (FR-012) checks for a `.git` file or folder in the destination and each parent, using filesystem checks only; Git itself is not invoked | FR-012 |

## 7. Randomness and Time

| ID | Requirement | Implements |
|---|---|---|
| **TR-050** | The default mask seed is `secrets.randbits(64)`. Placeholder permutation uses `random.Random(seed).shuffle()`. *Rationale:* the seed is unpredictable; the permutation only needs to be reproducible for a given seed | FR-092 |
| **TR-051** | Times are stored in UTC as ISO 8601 strings. Displayed times are converted to local time with offset | FR-083 |
| **TR-052** | Nmap `start` and `finished@time` (Unix seconds) are converted to UTC on import | FR-027 |

## 8. Development Toolchain and Project Layout

| ID | Requirement |
|---|---|
| **TR-060** | Project metadata, dependencies, and tool settings live in one `pyproject.toml` |
| **TR-061** | Source uses the "src layout": `src/testbondanh/`. Tests live in `tests/`; fixtures in `tests/fixtures/` |
| **TR-062** | The `testbondanh` command is installed by `[project.scripts] testbondanh = "testbondanh.cli:main"` via `pip install -e .` into `.venv` |
| **TR-063** | **ruff** lint rules: `E`, `F`, `W`, `I`, `B`, `UP`, `S`, `SIM`, `C90` (max complexity 10); line length 100; `ruff format` for formatting. `S101` (assert) is allowed in `tests/` only |
| **TR-064** | **mypy** runs in `--strict` mode on `src/` |
| **TR-065** | **pytest** settings: `testpaths = ["tests"]`; markers `slow` and `performance`; warnings treated as errors |
| **TR-066** | **Coverage** (Proposed — final values set in Test Strategy): branch coverage ≥ 95 % for the domain layer, ≥ 85 % overall |
| **TR-067** | One command runs the full verification suite: ruff check, ruff format check, mypy, pytest with coverage. Its exact form (a script under `scripts/`) is defined in the SAD and reused by the harness |

## 9. Code Quality Rules

| ID | Requirement |
|---|---|
| **TR-070** | All functions and methods have type annotations (enforced by mypy strict) |
| **TR-071** | Only the CLI layer writes to stdout/stderr; other layers return values or raise exceptions |
| **TR-072** | Catching all exceptions (`except Exception`) is allowed only at the CLI boundary, where it maps to `E-INT-001` (FR-005) |
| **TR-073** | The tool does not write log files in the MVP. `--debug` output goes to stderr only |
| **TR-074** | Every error in the FRD catalogue is raised as a dedicated exception class that carries its error ID; the CLI maps it to the message and exit code |
| **TR-075** | Code, comments, and docstrings reference requirement IDs where they implement a specific rule (e.g., `# FR-060`) |

## 10. Security Requirements

| ID | Requirement | Implements |
|---|---|---|
| **TR-SEC-01** | `pip-audit` reports no known vulnerabilities in installed dependencies before any push | S-7, NFR-011 |
| **TR-SEC-02** | A test (autouse fixture) makes any outgoing network connection attempt during tests fail, so FR-095 is checked on every run. Implemented by patching `socket.socket.connect`; no extra dependency | FR-095, NFR-004 |
| **TR-SEC-03** | An automated test scans every file under `tests/fixtures/` and fails if it finds an IP address outside the documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`) or a MAC address outside the documentation range `00:00:5E:00:53:00`–`FF` | S-1, BR-014, NFR-010 |
| **TR-SEC-04** | `.gitignore` shall include at least: `.venv/`, `*.db`, `*.sqlite*`, `reports/`, `*.xml` with the exception `!tests/fixtures/**/*.xml`, `.coverage`, `htmlcov/`, `__pycache__/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `.env` | BR-014 |
| **TR-SEC-05** | A secrets and sensitive-file check runs before every push. Tool choice and enforcement mechanism are defined in the AI Harness Design | BR-014 |
| **TR-SEC-06** | The tool never prints scan content in error messages beyond the file path and the specific missing or invalid item | Privacy |

## 11. Performance

| ID | Requirement | Implements |
|---|---|---|
| **TR-090** | **Reference machine** (resolves PQ-03): Intel Core i7-13620H, 31.8 GB RAM, internal fixed disk, Windows 11 Home, Python 3.13.5 | NFR-001 |
| **TR-091** | The 256-host fixture is **generated by a test helper** at test time from synthetic rules (documentation ranges only), not stored as a large file | NFR-001 |
| **TR-092** | Performance tests carry the `performance` marker and assert each of import, compare, and report completes in < 10 s. They run in the full suite but may be skipped in quick runs | NFR-001 |

## 12. Version Control

| ID | Requirement |
|---|---|
| **TR-100** | Default branch is **`main`** (resolves OQ-02; DEC-028). The local branch is renamed from `master` before the first commit, with the owner's go-ahead at that time |
| **TR-101** | Commit messages: a short imperative summary line; body references requirement IDs (e.g., `Refs: FR-059, FR-060`) |
| **TR-102** | A `LICENSE` file with the MIT licence text is added in the first commit (DEC-005) |
| **TR-103** | Commits and pushes are made only on explicit owner instruction (DEC-001) |

## 13. Traceability: Requirements → TR

| Source | TRs |
|---|---|
| FR-021 / NFR-002 size limit | TR-020 |
| FR-022 / FR-023 / NFR-003 safe parsing | TR-021, TR-022, TR-023 |
| FR-026 duplicates | TR-024 |
| FR-030, FR-052 addresses | TR-025 |
| FR-031 / NFR-005 atomic import | TR-032 |
| FR-041 / PR-006 delete | TR-031, TR-035 |
| FR-080 – FR-081 report files | TR-042 |
| FR-010 data folder | TR-043 |
| FR-012 Git warning | TR-044 |
| FR-092 mask seed | TR-050 |
| FR-095 / NFR-004 no network | TR-SEC-02 |
| NFR-001 performance | TR-090 – TR-092 |
| NFR-006 usability | TR-071, TR-072, TR-074 |
| NFR-007 Windows paths | TR-040, TR-043 |
| NFR-008 determinism | TR-041, TR-050 |
| NFR-009 verifiability | TR-065 – TR-067 |
| NFR-010 / BR-014 repo hygiene | TR-SEC-03, TR-SEC-04, TR-SEC-05 |
| NFR-011 dependencies | TR-010 – TR-013, TR-SEC-01 |
| C-02 Windows | TR-002, TR-003 |
| OQ-01 / OQ-02 / OQ-07 / PQ-03 | TR-001, TR-100, TR-037, TR-090 |

## 14. Open Questions

| ID | Question | Proposed answer |
|---|---|---|
| TQ-01 | Final coverage thresholds | Set in Test Strategy; TR-066 values are the starting proposal |
| TQ-02 | Secrets-scanning tool for TR-SEC-05 | Decide in AI Harness Design |

## 15. Approval Checklist

Completed: owner approved the TRD as drafted on 2026-10-27.

- [x] Python 3.13 and explicit virtual-environment interpreter rule (TR-001 – TR-003)
- [x] Runtime dependency `defusedxml==0.7.1` and its noted risk (TR-010 – TR-011)
- [x] Development tools and pinning approach (§3.2, TR-012 – TR-013)
- [x] Parsing, storage, and file-handling rules (§4 – §6)
- [x] Code quality rules (§9)
- [x] Security requirements TR-SEC-01 – TR-SEC-06
- [x] Reference machine and performance approach (§11)
- [x] Version-control rules (§12)
- [x] **TRD approved — status may change to "Approved" (version 1.0)**
