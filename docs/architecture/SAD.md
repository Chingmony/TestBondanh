# TestBondanh — System Architecture Document (SAD)

| Field | Value |
|---|---|
| Document | System Architecture Document |
| Project | TestBondanh — Network Security Monitoring Tool |
| Purpose | Define how the code is organised: components, responsibilities, allowed dependencies, data storage, runtime flows, and how each part is tested |
| Status | **Approved** — by project owner, 2026-10-27 |
| Version | 1.0 |
| Based on | [FRD v1.0](../requirements/FRD.md), [TRD v1.0](TRD.md) (Approved) |
| Owner / Approver | Project owner (Chingmony) |
| Author | Claude Code (drafted under owner direction) |
| Last updated | 2026-10-27 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-27 | Claude Code | Initial draft from approved outline |
| 1.0 | 2026-10-27 | Project owner | Approved as drafted; DEC-029 – DEC-034 accepted |

## 1. Purpose

The FRD defines behaviour and the TRD defines technology. This SAD defines **where each piece of behaviour lives** and **which parts may depend on which**. It is the main reference for:

- deciding which file a new function belongs in;
- the review subagent, which checks code against the dependency rules in Section 5;
- the test strategy, which tests each layer differently (Section 10).

Architecture decisions made here are recorded as **DEC-029 – DEC-034** in the decision log, accepted on approval of this document (2026-10-27).

## 2. Architecture Goals

| Goal | Driven by | How the architecture serves it |
|---|---|---|
| **Correct classification is easy to test** | BR-004, BR-005, NFR-009 | All classification rules live in a pure domain layer, testable with in-memory objects |
| **Untrusted input contained at one point** | BR-006, NFR-003 | Only one module touches XML; everything after it handles validated domain objects |
| **No data leaves the machine** | BR-010, NFR-004 | Only adapters perform I/O; none performs network I/O; tests block networking |
| **Deterministic output** | NFR-008 | Ordering, masking, and rendering are pure functions of their inputs and seed |
| **Small, session-sized changes** | C-05 | Small modules with one responsibility each; a typical task touches 1–3 files |
| **AI changes are reviewable** | C-01 | Dependency rules are mechanical and checked by a test, not by judgement alone |

## 3. Architectural Style

A **layered architecture with a pure core** (also called "functional core, imperative shell"). The *core* makes every decision without performing I/O. The *shell* around it reads files, talks to the database, and prints output.

```
┌──────────────────────────────────────────────────────────────┐
│ cli            parse arguments · print · exit codes          │  shell
├──────────────────────────────────────────────────────────────┤
│ services       orchestrate one use case each                 │  shell
├───────────────────────────────┬──────────────────────────────┤
│ domain   (PURE)               │ reporting   (PURE)           │  core
│ model · states · coverage ·   │ markdown · json · wording    │
│ classify · ranking · advice · │                              │
│ masking · errors              │                              │
├───────────────────────────────┴──────────────────────────────┤
│ adapters       nmap_xml · sqlite_repo · files                │  shell
└──────────────────────────────────────────────────────────────┘
```

"Pure" means: the function's result depends only on its arguments, and it performs no file, database, network, clock, or random-source access. Time and randomness are passed in as arguments (e.g., the mask seed, the generation timestamp).

## 4. Component View

### 4.1 `cli` — command-line shell

| Module | Responsibility | FRs |
|---|---|---|
| `cli/main.py` | `main(argv) -> int`: build `argparse` parser, dispatch sub-commands, catch exceptions, return exit code | FR-001 – FR-006 |
| `cli/commands.py` | One handler per sub-command; calls a service; formats its result for stdout | FR-032, FR-040, FR-042, FR-086 |
| `cli/messages.py` | Error catalogue: error ID → message template, next step, exit code | FRD §15, FR-003 – FR-005 |

### 4.2 `services` — use cases

| Module | Responsibility | FRs |
|---|---|---|
| `services/import_scan.py` | Check file → parse → build domain `Scan` → reject duplicates → save in one transaction | FR-020 – FR-033 |
| `services/history.py` | List scans; delete a scan | FR-040 – FR-042 |
| `services/compare.py` | Select scans → load → get first-seen data → classify → rank → (mask) → render → leak check → write | FR-050 – FR-094 |
| `services/settings.py` | Resolve the data folder; ensure it exists; Git warning | FR-010 – FR-012 |

Services depend on adapters only through small interfaces (Python `Protocol` classes) declared in `services/ports.py`, so tests can substitute in-memory fakes.

### 4.3 `domain` — pure business rules

| Module | Responsibility | FRs |
|---|---|---|
| `domain/model.py` | Immutable dataclasses: `Scan`, `Host`, `Port`, `Service`, `ExtraPorts`, `Coverage`, `Finding`, `Comparison` | FRD §6 |
| `domain/errors.py` | `TestBondanhError` base class and one subclass per error ID | FRD §15, TR-074 |
| `domain/coverage.py` | Expand `scaninfo` port lists; derive address coverage from `args` (heuristic) | FR-029, FR-030 |
| `domain/completeness.py` | Decide complete/incomplete and reasons | FR-028 |
| `domain/states.py` | Effective port state and state groups | FR-055 |
| `domain/classify.py` | Rules FR-056 – FR-069; produces unordered findings | FR-052 – FR-069 |
| `domain/ranking.py` | Importance levels and High-importance ports; deterministic ordering | FR-070, FR-071, FR-085 |
| `domain/advice.py` | Advice catalogue | FR-072 |
| `domain/masking.py` | Placeholder assignment from seed; masked copy of a `Comparison`; set of original identifiers; leak check on text | FR-090 – FR-094 |

### 4.4 `reporting` — pure renderers

| Module | Responsibility | FRs |
|---|---|---|
| `reporting/wording.py` | Fixed sentences: reason codes, limitations, masking statement | FR-082 AC2, FR-087, FR-093 |
| `reporting/markdown.py` | `render_markdown(comparison, generated_at) -> str` | FR-082 |
| `reporting/json_report.py` | `render_json(comparison, generated_at) -> str` | FR-083 |

### 4.5 `adapters` — I/O at the edges

| Module | Responsibility | FRs / TRs |
|---|---|---|
| `adapters/nmap_xml.py` | **The only module that parses XML.** Bytes → raw parsed values using `defusedxml`; maps parser exceptions to `E-IMP-004/005/006/007/009` | FR-022 – FR-027, FR-033, TR-021 – TR-023 |
| `adapters/sqlite_repo.py` | `SqliteScanRepository`: schema, migrations, transactions, queries | TR-030 – TR-036 |
| `adapters/files.py` | Size check; read bytes and hash; atomic exclusive-create report writes; `.git` detection; data folder path | FR-020, FR-021, FR-080, FR-081, FR-012, TR-020, TR-042 – TR-044 |

## 5. Dependency Rules

| Layer | May import | Must not import |
|---|---|---|
| `domain` | Python standard library **pure** modules only (`dataclasses`, `enum`, `ipaddress`, `random`, `re`, `typing`, `collections`, `itertools`, `datetime` for types only) | `os`, `pathlib`, `sqlite3`, `socket`, `xml`, `defusedxml`, `secrets`, `subprocess`, any other `testbondanh` layer |
| `reporting` | `domain`, `json`, pure standard-library modules | `services`, `adapters`, `cli`, any I/O module |
| `adapters` | `domain`, standard library, `defusedxml` (only `nmap_xml.py`) | `services`, `cli`, `reporting` |
| `services` | `domain`, `reporting`, `adapters`, `secrets`, `datetime` | `cli` |
| `cli` | `services`, `domain.errors`, standard library | `adapters` directly, `reporting` directly |

**Enforcement (DEC-030):** `tests/architecture/test_dependencies.py` parses every source file with the standard `ast` module and fails if any import breaks the table above. It runs with the normal test suite, so a hook running the suite also enforces the architecture.

## 6. Data View

Derived from the FRD logical model (§6). Created and migrated by `sqlite_repo.py` (TR-036).

```sql
CREATE TABLE scans (
  scan_id                 INTEGER PRIMARY KEY AUTOINCREMENT,  -- TR-033: never reused
  imported_at             TEXT NOT NULL,                      -- UTC ISO 8601
  source_file_name        TEXT NOT NULL,                      -- name only, no folder
  content_sha256          TEXT NOT NULL UNIQUE,               -- FR-026
  nmap_version            TEXT NOT NULL,
  nmap_args               TEXT NOT NULL,
  start_time              TEXT NOT NULL,
  end_time                TEXT NOT NULL,
  completeness            TEXT NOT NULL CHECK (completeness IN ('complete','incomplete')),
  incompleteness_reasons  TEXT NOT NULL,                      -- JSON array of reason codes
  address_coverage_known  INTEGER NOT NULL CHECK (address_coverage_known IN (0,1)),
  address_coverage        TEXT NOT NULL                       -- JSON array of CIDR networks
);

CREATE TABLE port_coverage (
  scan_id     INTEGER NOT NULL REFERENCES scans(scan_id) ON DELETE CASCADE,
  protocol    TEXT NOT NULL,
  port_ranges TEXT NOT NULL,                                  -- e.g. "1-1000,8080"
  PRIMARY KEY (scan_id, protocol)
);

CREATE TABLE hosts (
  host_id      INTEGER PRIMARY KEY,
  scan_id      INTEGER NOT NULL REFERENCES scans(scan_id) ON DELETE CASCADE,
  address      TEXT NOT NULL,                                 -- normalised
  address_type TEXT NOT NULL CHECK (address_type IN ('ipv4','ipv6')),
  mac_address  TEXT,
  mac_vendor   TEXT,
  status       TEXT NOT NULL,
  timed_out    INTEGER NOT NULL CHECK (timed_out IN (0,1)),
  UNIQUE (scan_id, address)
);

CREATE TABLE hostnames (
  host_id INTEGER NOT NULL REFERENCES hosts(host_id) ON DELETE CASCADE,
  name    TEXT NOT NULL
);

CREATE TABLE extraports (
  host_id INTEGER NOT NULL REFERENCES hosts(host_id) ON DELETE CASCADE,
  state   TEXT NOT NULL,
  count   INTEGER NOT NULL
);

CREATE TABLE ports (
  port_id     INTEGER PRIMARY KEY,
  host_id     INTEGER NOT NULL REFERENCES hosts(host_id) ON DELETE CASCADE,
  protocol    TEXT NOT NULL,
  port_number INTEGER NOT NULL,
  state       TEXT NOT NULL,
  UNIQUE (host_id, protocol, port_number)
);

CREATE TABLE services (
  port_id    INTEGER PRIMARY KEY REFERENCES ports(port_id) ON DELETE CASCADE,
  name       TEXT NOT NULL,
  product    TEXT,
  version    TEXT,
  extrainfo  TEXT,
  tunnel     TEXT,
  method     TEXT NOT NULL CHECK (method IN ('probed','table')),
  confidence INTEGER NOT NULL CHECK (confidence BETWEEN 0 AND 10)
);

CREATE INDEX idx_hosts_address ON hosts(address);             -- first-seen lookup (FR-068)
```

**Design notes:**
- Coverage is stored compactly — CIDR networks and port-range strings — and expanded in memory only when needed (DEC-032).
- Comparison and first-seen data are computed on demand; no comparison results are stored (PRD A-10).

## 7. Runtime Views

### 7.1 Import (`testbondanh import scan.xml`)

```
cli.main ─► services.import_scan.run(path)
              ├─ files.check_size(path)                  E-IMP-001/002/003
              ├─ data, sha = files.read_bytes_and_hash(path)
              ├─ repo.find_by_hash(sha)                   E-IMP-008
              ├─ raw = nmap_xml.parse(data)               E-IMP-004/005/006/007/009
              ├─ scan = domain: build Scan from raw
              │        completeness.assess(...)           FR-028
              │        coverage.ports(...), coverage.addresses(...)
              └─ repo.save(scan)  ── one transaction ──   FR-031
cli prints confirmation (FR-032) ─► exit 0
```

### 7.2 Compare (`testbondanh compare [A B] [--mask]`)

```
cli.main ─► services.compare.run(ids, mask, seed, output_dir)
              ├─ select and order baseline/newer          FR-050, FR-051
              ├─ baseline, newer = repo.load(a), repo.load(b)
              ├─ first_seen = repo.first_seen(addresses, ports, up_to=newer)
              ├─ findings = classify.compare(baseline, newer, first_seen)   PURE
              ├─ comparison = ranking.rank_and_order(findings)              PURE
              ├─ if mask: seed = seed or secrets.randbits(64)
              │           comparison, originals = masking.apply(comparison, seed)  PURE
              ├─ md   = markdown.render(comparison, generated_at)           PURE
              ├─ json = json_report.render(comparison, generated_at)        PURE
              ├─ if mask: masking.check_no_leak([md, json], originals)      E-RPT-002
              └─ files.write_reports(md, json, output_dir)                  E-RPT-001
cli prints summary (FR-086) ─► exit 0
```

The leak check runs **after** rendering and **before** any file is written, so a masking defect can never reach disk (FR-094).

### 7.3 Delete (`testbondanh delete 3`)

```
cli: show summary, confirm (FR-042) ─► services.history.delete(3)
       ─► repo.delete(3)   (cascade, secure_delete; TR-031, TR-035)
```

## 8. Error Handling

1. Domain, adapters, and services raise subclasses of `TestBondanhError` that carry the **error ID** and the values for the message (e.g., the path).
2. Third-party and standard-library exceptions are converted at the adapter boundary. For example, `defusedxml.EntitiesForbidden` becomes `UnsafeXmlError` (`E-IMP-005`).
3. `cli.main` catches `TestBondanhError` and looks the ID up in `cli/messages.py` to print `Error [ID]: …` and `Next step: …`, then returns the exit code.
4. Any other exception reaching `cli.main` becomes `E-INT-001` (exit 3); the traceback is printed only with `--debug` (FR-005, TR-072).

## 9. Source Tree

```
TestBondanh/
├─ pyproject.toml                  # metadata, pinned deps, ruff/mypy/pytest config (TR-060)
├─ requirements-dev.lock.txt       # full pip freeze (TR-012)
├─ README.md · LICENSE (MIT) · .gitignore
├─ CLAUDE.md                       # added in harness stage
├─ scripts/
│  └─ verify.py                    # runs ruff, format check, mypy, pytest+coverage (TR-067, DEC-031)
├─ src/testbondanh/
│  ├─ __init__.py · __main__.py
│  ├─ cli/        main.py · commands.py · messages.py
│  ├─ services/   ports.py · import_scan.py · history.py · compare.py · settings.py
│  ├─ domain/     model.py · errors.py · coverage.py · completeness.py · states.py
│  │              classify.py · ranking.py · advice.py · masking.py
│  ├─ reporting/  wording.py · markdown.py · json_report.py
│  └─ adapters/   nmap_xml.py · sqlite_repo.py · files.py
├─ tests/
│  ├─ conftest.py                  # network block (TR-SEC-02), shared builders
│  ├─ unit/domain/ · unit/reporting/
│  ├─ integration/adapters/
│  ├─ e2e/                         # CLI via main(argv) + one installed-command smoke test
│  ├─ architecture/                # dependency rules (DEC-030)
│  ├─ security/                    # fixture address check (TR-SEC-03), hostile inputs
│  ├─ performance/                 # 256-host generated fixture (TR-091)
│  └─ fixtures/
│     ├─ import/valid/ · import/hostile/ · import/malformed/
│     ├─ compare/<case-name>/baseline.xml, newer.xml
│     └─ expected/                 # golden reports (NFR-008)
└─ docs/  requirements/ · architecture/ · quality/ · harness/ · planning/ · traceability/
```

`scripts/verify.py` is a Python script, run as `.venv\Scripts\python.exe scripts\verify.py`, rather than a PowerShell script. This avoids Windows PowerShell execution-policy restrictions and keeps the harness hook command identical everywhere (DEC-031).

## 10. Testing by Layer

| Layer | Test type | Inputs | Notes |
|---|---|---|---|
| `domain` | Unit | In-memory objects made by builder helpers | Fast; covers every classification rule AC-C1 – AC-C12 without XML |
| `reporting` | Unit + golden files | Hand-built `Comparison` objects | Golden files catch unintended output changes |
| `adapters/nmap_xml` | Integration | Fixture XML files (valid, hostile, malformed) | Includes TR-022 compatibility proof |
| `adapters/sqlite_repo` | Integration | Temporary database in pytest's `tmp_path` | Atomicity, cascade, ID non-reuse |
| `adapters/files` | Integration | `tmp_path` | No-overwrite, atomic write, Git detection |
| `services` | Unit with fakes | In-memory fake repository | Orchestration and error paths |
| `cli` | End-to-end | `main(argv)` with fixture files and `tmp_path` data folder | Exit codes, stdout/stderr, error format |
| Whole package | Architecture | Source files | Dependency rules (§5) |

Detailed thresholds and the fixture catalogue are defined in the Test Strategy.

## 11. Architecture Decisions

Recorded in the decision log (Accepted 2026-10-27):

| ID | Decision |
|---|---|
| DEC-029 | Layered architecture with a pure core (domain and reporting perform no I/O) |
| DEC-030 | Dependency rules enforced by an `ast`-based architecture test |
| DEC-031 | Verification entry point is `scripts/verify.py`, not a PowerShell script |
| DEC-032 | Coverage stored compactly (CIDR networks, port-range strings) |
| DEC-033 | Comparison works on fully loaded scans in memory (sized for ≤ 256 hosts) |
| DEC-034 | CLI end-to-end tests call `main(argv)` in-process, plus one smoke test of the installed command |

## 12. Traceability: Component → FR

| Component | FRs |
|---|---|
| `cli` | FR-001 – FR-006, FR-032, FR-040 (output), FR-042, FR-086, §15 |
| `services/import_scan` | FR-020 – FR-033 (orchestration) |
| `services/history` | FR-040, FR-041 |
| `services/compare` | FR-050, FR-051, FR-068 (lookup), FR-092 (seed) |
| `services/settings` | FR-010 – FR-012 |
| `domain/coverage`, `completeness` | FR-028 – FR-030 |
| `domain/states`, `classify` | FR-052 – FR-069 |
| `domain/ranking`, `advice` | FR-070 – FR-072, FR-085 |
| `domain/masking` | FR-090 – FR-094 |
| `reporting/*` | FR-082 – FR-084, FR-087, FR-088, FR-093 |
| `adapters/nmap_xml` | FR-022 – FR-027, FR-033 |
| `adapters/sqlite_repo` | FR-031, FR-041, TR-030 – TR-036 |
| `adapters/files` | FR-012, FR-020, FR-021, FR-080, FR-081 |
| All (no network I/O anywhere) | FR-095 |

## 13. Open Questions

| ID | Question | Proposed answer |
|---|---|---|
| SQ-01 | Should `reporting` be a separate layer or part of `domain`? | Separate: rendering text is a different responsibility from deciding findings, and golden-file tests target it alone |

## 14. Approval Checklist

Completed: owner approved the SAD as drafted on 2026-10-27.

- [x] Architectural style: layered with a pure core (§3)
- [x] Components and responsibilities (§4)
- [x] Dependency rules and their automated enforcement (§5)
- [x] Database tables (§6)
- [x] Runtime flows, including leak check before write (§7)
- [x] Error handling approach (§8)
- [x] Source tree and `scripts/verify.py` (§9)
- [x] Testing by layer (§10)
- [x] Architecture decisions DEC-029 – DEC-034 (§11)
- [x] **SAD approved — status may change to "Approved" (version 1.0)**
