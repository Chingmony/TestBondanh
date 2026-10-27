# TestBondanh — Testing and Verification Strategy

| Field | Value |
|---|---|
| Document | Testing and Verification Strategy |
| Project | TestBondanh — Network Security Monitoring Tool |
| Purpose | Define how correctness, security, and quality are demonstrated: test levels, workflow and approvals, fixtures, thresholds, gates, and defect rules |
| Status | **Approved** — by project owner, 2026-10-28 |
| Version | 1.0 |
| Based on | BRD, PRD, FRD, TRD, SAD (all v1.0 Approved) |
| Owner / Approver | Project owner (Chingmony) |
| Author | Claude Code (drafted under owner direction) |
| Last updated | 2026-10-27 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-27 | Claude Code | Initial draft from approved outline and owner answers (test strategy batch 1) |
| 1.0 | 2026-10-28 | Project owner | Approved as drafted |

## 1. Purpose and Principles

This strategy defines what evidence is needed before any requirement is considered met. It implements BR-013, NFR-009, and success metrics SM-01 – SM-06.

Rule IDs in this document use the prefix `TS-`.

| # | Principle |
|---|---|
| P1 | **Every acceptance criterion maps to an automated test or a documented manual check.** Nothing is "done" on inspection alone |
| P2 | **Tests are the specification in executable form.** Once the owner approves them, they are not changed to fit the code |
| P3 | **The author of the code is not the sole judge of its tests.** AI-written tests require owner approval before implementation begins (DEC-035) |
| P4 | **Prefer deterministic checks to judgement.** Anything a script can check (architecture, fixture addresses, coverage, traceability) is checked by a script |
| P5 | **No real network data, ever.** All fixtures are synthetic and use documentation-reserved addresses only |
| P6 | **A passing suite is necessary, not sufficient.** Coverage shows code ran; only assertions derived from acceptance criteria show it is correct |

## 2. Test Levels

Aligned with SAD §10.

| Level | Location | Target | Inputs | Speed |
|---|---|---|---|---|
| **Unit — domain** | `tests/unit/domain/` | Classification, states, coverage, completeness, ranking, advice, masking | In-memory objects from builder helpers | Very fast |
| **Unit — reporting** | `tests/unit/reporting/` | Markdown and JSON rendering, wording | Hand-built `Comparison` objects; golden files | Very fast |
| **Unit — services** | `tests/unit/services/` | Use-case orchestration and error paths | In-memory fake repository | Fast |
| **Integration — adapters** | `tests/integration/adapters/` | XML parsing, SQLite repository, file operations | Fixture files; `tmp_path` database and folders | Fast |
| **End-to-end** | `tests/e2e/` | CLI behaviour: commands, output, exit codes, error format | `main(argv)` with fixtures and a `tmp_path` data folder; one installed-command smoke test (DEC-034) | Moderate |
| **Architecture** | `tests/architecture/` | SAD §5 dependency rules (DEC-030) | Source files | Fast |
| **Security** | `tests/security/` | Hostile input, fixture address check, network block, masking leak | Hostile fixtures; generated oversized file | Fast |
| **Performance** | `tests/performance/` | NFR-001 timings | Generated 256-host fixture (TR-091) | Slow (`performance` marker) |

**Rule TS-01:** classification rules (FR-055 – FR-069) are tested **twice**: exhaustively at domain level with builders, and once per case end-to-end with XML fixture pairs. The domain tests prove the logic; the end-to-end tests prove the parser and storage feed the logic correctly.

## 3. Test-Writing Workflow and Approvals (DEC-035)

Each implementation task follows these steps:

```
1. Select task  ── from Development Plan; lists FR/TR IDs in scope
2. Write tests  ── Claude writes tests from the FR acceptance criteria, tagged with requirement IDs
3. ★ Owner approves tests ── reads tests; checks each AC is covered and assertions are right
4. Confirm red  ── run tests; they must FAIL for the expected reason (proves they test something)
5. Implement    ── Claude writes code until tests pass, WITHOUT modifying approved tests
6. Verify       ── scripts/verify.py passes (§11)
7. Review       ── read-only review subagent checks code against FRD/TRD/SAD
8. ★ Owner accepts ── reviews diff, verification output, and review findings
```

★ = human approval checkpoint.

| Rule | Statement |
|---|---|
| TS-02 | Tests approved in step 3 shall not be modified in step 5. Enforcement (read-only protection or change detection) is defined in the AI Harness Design |
| TS-03 | If Claude believes an approved test is wrong, it stops, explains why with reference to the requirement, and waits for the owner's decision. The test is changed only after approval |
| TS-04 | Step 4 is mandatory: a new test that passes before implementation exists proves nothing and must be investigated |
| TS-05 | Infrastructure-only tasks (e.g., project scaffolding) follow the same steps with checks appropriate to them (e.g., "verify.py runs and reports zero tests") |

## 4. Fixture Strategy (DEC-036)

### 4.1 Types

| Type | How produced | Committed? | Used by |
|---|---|---|---|
| **Minimal hand-written XML** | Written by hand, only the elements relevant to the case | Yes | Import and comparison cases |
| **Reference fixture** | One realistic file shaped like full Nmap 7.x output (DOCTYPE, stylesheet instruction, scaninfo, verbose, OS and script elements, runstats); all values synthetic | Yes | Parser realism; FR-033 (ignored elements) |
| **Generated** | Built by a test helper at test time | **No** | 256-host performance fixture; > 50 MB oversized file |
| **Builders** | Python helper functions producing domain objects | N/A (code) | Domain and reporting unit tests |

### 4.2 Rules

| Rule | Statement |
|---|---|
| TS-10 | Fixture addresses: IPv4 only within `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`; IPv6 within `2001:db8::/32`; MAC within `00:00:5E:00:53:00`–`FF`. Enforced by TR-SEC-03 |
| TS-11 | Hostnames in fixtures use the reserved `.example` or `.test` domains |
| TS-12 | Every fixture starts with an XML comment stating its purpose and the requirement IDs it supports |
| TS-13 | Fixtures are never derived from real scans, even after editing addresses |
| TS-14 | Comparison cases live in `tests/fixtures/compare/<case-name>/` as `baseline.xml` and `newer.xml` |

### 4.3 Fixture catalogue

**Import — valid** (`tests/fixtures/import/valid/`)

| File | Purpose | Requirements |
|---|---|---|
| `minimal_complete.xml` | Smallest valid complete scan: 2 hosts, few ports | FR-027, FR-028, FR-032 |
| `reference_full.xml` | Realistic full-format output | FR-022 AC3, FR-033 |
| `ipv6.xml` | IPv6 hosts, mixed case addresses | FR-052, DEC-022 |
| `exit_error.xml` | `finished@exit="error"` with `errormsg` | FR-028 AC1 |
| `no_exit_attribute.xml` | `finished` without `exit` | FR-028 |
| `host_timed_out.xml` | One host `timedout="true"` | FR-028 AC2, FR-067 |
| `host_without_ip.xml` | A host with only a MAC address | FR-027 AC2 |
| `coverage_cidr.xml` | args with CIDR target and `-p` list | FR-029, FR-030 AC1, AC3 |
| `coverage_exclude.xml` | args with `--exclude` | FR-030 AC2 |
| `extraports_single.xml` / `extraports_multiple.xml` | Unlisted-port state inference | FR-055 |

**Import — malformed** (`tests/fixtures/import/malformed/`)

| File | Purpose | Requirements |
|---|---|---|
| `not_xml.xml` | Plain text | FR-023 AC1 |
| `truncated.xml` | Cut off mid-document | FR-023 AC2 |
| `not_nmap_root.xml` | Root element is not `nmaprun` | FR-024 |
| `wrong_scanner.xml` | `scanner` attribute is not `nmap` | FR-024 |
| `nmap_v6.xml` / `bad_version.xml` | Unsupported or unparseable version | FR-025 |
| `missing_start.xml` / `missing_runstats.xml` | Required data absent | FR-027 AC1 |

**Import — hostile** (`tests/fixtures/import/hostile/`)

| File | Purpose | Requirements |
|---|---|---|
| `xxe_local_file.xml` | External entity referencing a local file | FR-022 AC1 |
| `xxe_external_dtd.xml` | External DTD reference | FR-022 |
| `billion_laughs.xml` | Nested entity expansion | FR-022 AC2 |
| *(generated)* oversized | 52,428,801 bytes | FR-021 |

**Comparison cases** (`tests/fixtures/compare/`)

| Case folder | FRD AC | Expected |
|---|---|---|
| `c01_new_host_confirmed` | AC-C1 | 1 confirmed `new_host`, High |
| `c02_host_first_observed` | AC-C2 | uncertain `host_first_observed` |
| `c03_host_no_response` | AC-C3 | uncertain `host_not_observed`, 0 confirmed |
| `c04_newer_incomplete` | AC-C4 | 2 uncertain, 0 confirmed |
| `c05_port_opened_high` | AC-C5 | confirmed `port_opened`, High |
| `c06_filtered_to_open` | AC-C6 | uncertain `port_first_observed_open` |
| `c07_open_to_filtered` | AC-C7 | uncertain `port_state_unknown` |
| `c08_port_closed` | AC-C8 | confirmed `port_closed`, Low |
| `c09_service_changed` | AC-C9 | confirmed `service_changed`, Medium |
| `c10_version_changed` | AC-C10 | confirmed `version_changed`, Low |
| `c11_service_guessed` | AC-C11 | uncertain `service_identification_unreliable` |
| `c12_identical` | AC-C12 | 0 findings |
| `c13_mac_moved` | FR-053 | notes reference the other address |
| `c14_timed_out_host` | FR-067 | absence-based findings uncertain |
| `c15_masking_leak` | FR-094 | product field contains an IP; never written to disk |
| `history_first_seen/` (3 scans) | FR-068 | first-seen points to the earliest scan |

## 5. Golden Files (DEC-037)

Golden files are saved expected reports in `tests/fixtures/expected/`, compared byte-for-byte (after removing the generation-time line/field) against fresh output.

| Rule | Statement |
|---|---|
| TS-20 | Initial set: Markdown and JSON for `c01`, `c04`, `c09`; masked Markdown and JSON for `c01` with `--mask-seed 42` |
| TS-21 | Golden files are produced once by the implementation, **reviewed by the owner**, then committed |
| TS-22 | Golden files are **never regenerated automatically**. Any change requires owner approval, and the commit message states which requirement caused it |
| TS-23 | No "update all golden files" command or flag is provided. Updating is a deliberate, single-file action |

## 6. Security Testing

| Check | Mechanism | Requirements |
|---|---|---|
| Hostile XML rejected | Hostile fixture tests | FR-022, TR-022 |
| Size limit before parsing | Generated oversized file; test asserts parser never invoked | FR-021, TR-020 |
| No network connections | Autouse fixture in `tests/conftest.py` patches `socket.socket.connect` to raise | FR-095, TR-SEC-02 |
| Fixture addresses are reserved | `tests/security/test_fixture_addresses.py` | TR-SEC-03, TS-10 |
| Masking never leaks | `c15_masking_leak` plus a property check: for every comparison fixture, a masked report contains none of the original identifiers | FR-090 – FR-094, SM-06 |
| Atomic import | Simulated failure mid-import; history unchanged | FR-031 |
| Secure delete | After delete, the database file bytes no longer contain a unique marker string from the deleted scan | TR-035 |
| Unsafe code patterns | ruff `S` rules (unsafe XML, SQL string building) | TR-023, TR-034 |
| Dependency vulnerabilities | `pip-audit` | TR-SEC-01 |

## 7. Performance Testing

- `tests/performance/test_nfr001.py` generates a 256-host scan pair (each host with ~10 open ports among 1,000 scanned), then times import, compare, and report separately.
- Each must complete in **< 10 s** on the reference machine (TR-090).
- Marked `performance`; included in the full verification run, excluded from `--quick` runs.

## 8. Manual Checks

Some acceptance criteria are judgements and cannot be automated meaningfully.

| ID | Check | Requirement | When | Evidence |
|---|---|---|---|---|
| MC-01 | Owner reads the golden Markdown reports and confirms a non-specialist could understand them and act on High findings | BR-007, NFR-012 | When golden files are first approved | Entry in the traceability matrix with date |
| MC-02 | Owner reviews the README: common tasks, data location, authorised-use notice, database-protection limitation | PR-020, TR-037 | Before first public push of the README | Same |
| MC-03 | Owner reviews the masked golden report for anything that still identifies the network | BR-009 | With MC-01 | Same |

## 9. Coverage (DEC-038)

| Scope | Minimum branch coverage | Failure below threshold |
|---|---|---|
| `domain` and `reporting` | **95 %** | Yes |
| Whole package | **85 %** | Yes |

Coverage shows which code ran during tests, not whether results were checked (P6). A requirement is met only when its acceptance-criteria tests pass.

## 10. Test Naming and Requirement Tagging

| Rule | Statement |
|---|---|
| TS-30 | Test function names describe behaviour: `test_<situation>_<expected_result>`, e.g. `test_filtered_to_open_is_uncertain` |
| TS-31 | Every test carries `@pytest.mark.req("ID", ...)` with one or more requirement IDs (FR, NFR, TR, or TR-SEC). The marker is registered in `pyproject.toml` |
| TS-32 | A test without a `req` marker fails the traceability check (§11). Shared helpers are not tests and need no marker |
| TS-33 | Parametrised tests use readable IDs (e.g., the fixture case name) |

## 11. Verification Gates

### 11.1 `scripts/verify.py` (DEC-031)

| Step | Command (run via `.venv\Scripts\python.exe`) | Fails when |
|---|---|---|
| 1 | `ruff check .` | Any lint or security-rule violation |
| 2 | `ruff format --check .` | Any unformatted file |
| 3 | `mypy --strict src` | Any type error |
| 4 | `pytest` with coverage | Any test failure; coverage below §9 thresholds |
| 5 | `scripts/trace.py --check` | Any test without a `req` marker; any requirement ID in a marker that does not exist in the documents |

`verify.py --quick` runs steps 1–5 but excludes `performance` and `slow` tests. `pip-audit` runs separately before any push (TR-SEC-01) because it needs network access, which the test suite forbids.

### 11.2 Definition of Done for a task

A task is done only when **all** of the following are true:

1. Tests for every AC in scope exist, are tagged, and were approved by the owner before implementation.
2. Those tests failed before implementation for the expected reason (TS-04).
3. `verify.py` (full, not quick) passes.
4. The traceability matrix shows the task's requirements as Passing.
5. The review subagent reports no unresolved blocking findings.
6. The owner has accepted the change.

## 12. Defect Handling

| Rule | Statement |
|---|---|
| TS-40 | A failing approved test means the code is wrong until the owner decides otherwise (TS-03) |
| TS-41 | Tests may not be skipped, marked expected-to-fail, or deleted without owner approval; any such marker must state the reason and an issue or decision reference |
| TS-42 | Coverage thresholds, lint rules, and type-check strictness may not be lowered or bypassed (including `# noqa`, `# type: ignore`, `# pragma: no cover`) without owner approval and a stated reason on the same line |
| TS-43 | A flaky test (passes and fails without code changes) is treated as a defect and fixed, not retried until green. Exception: FR-092 AC2's documented single retry |
| TS-44 | When a bug is found that tests did not catch, a test reproducing it is written and approved **before** the fix |

## 13. Open Questions

None at this time.

## 14. Approval Checklist

Completed: owner approved this document as drafted on 2026-10-28.

- [x] Principles and test levels (§1 – §2)
- [x] Tests-first workflow with owner approval of tests (§3)
- [x] Fixture strategy and catalogue (§4)
- [x] Golden-file rules (§5)
- [x] Security and performance testing (§6 – §7)
- [x] Manual checks MC-01 – MC-03 (§8)
- [x] Coverage thresholds (§9)
- [x] Naming, tagging, and verification gates (§10 – §11)
- [x] Definition of Done (§11.2)
- [x] Defect handling rules (§12)
- [x] **Test Strategy approved — status may change to "Approved" (version 1.0)**
