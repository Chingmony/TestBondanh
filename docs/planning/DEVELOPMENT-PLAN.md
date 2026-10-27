# TestBondanh — Development Plan

| Field | Value |
|---|---|
| Document | Development Plan |
| Project | TestBondanh — Network Security Monitoring Tool |
| Purpose | Order the approved work into milestones and one-hour tasks, each traceable to requirements and governed by the approval workflow |
| Status | **Draft** — awaiting owner review |
| Version | 0.1 |
| Based on | All approved documents (BRD … AI Harness Design, v1.0) |
| Owner / Approver | Project owner (Chingmony) |
| Author | Claude Code (drafted under owner direction) |
| Last updated | 2026-10-28 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-28 | Claude Code | Initial plan; M0–M2 detailed, M3–M7 outlined (DEC-048) |

---

> **Current task:** none — awaiting plan approval. First task on approval: **T-001**.
>
> *(This line is read by the session-context hook HK-05. It is updated at the start and end of each task.)*

## 1. Planning Principles

| # | Principle | Source |
|---|---|---|
| 1 | Each task fits about one hour and ends in a verified, reviewable state | C-05 |
| 2 | Riskiest work first: prove the risky dependency, then build the most important logic while it is pure and cheap to test | DEC-046 |
| 3 | Every task lists its requirement IDs; no work without one | BR-013, DEC-039 |
| 4 | Feature tasks follow the 8-step workflow with two owner checkpoints | Test Strategy §3, DEC-035 |
| 5 | Commits only on owner instruction; first push only after the harness is verified | DEC-001, DEC-047 |
| 6 | Only M0–M2 are detailed; later milestones are refined at their start, with owner approval | DEC-048 |

**Estimate:** roughly 40–55 one-hour sessions (about 2–3 months at one hour per day). This is a planning estimate, not a commitment.

## 2. Task Conventions

- **Task ID:** `T-NNN`, grouped by milestone (T-00x = M0, T-01x = M1, …).
- **Status:** Not started · In progress · Awaiting approval · Done (date) · Deferred.
- **Feature task Definition of Done:** Test Strategy §11.2 (six conditions).
- **Infrastructure/harness task Definition of Done:** the task's stated verification passes, evidence is recorded, and the owner accepts (TS-05).
- **★** marks an owner approval checkpoint inside a task.

## 3. Milestone Overview

| Milestone | Goal | Exit criteria | Sessions (est.) | Status |
|---|---|---|---|---|
| **M0 Bootstrap** | A clean, runnable, verifiable project skeleton | `verify.py` and `trace.py` run green on an empty test suite; first local commit on `main` | 2–3 | Not started |
| **M1 Harness** | Verified AI harness (H-1 – H-7) | V-01 – V-11 pass with recorded evidence (except V-09/V-10 parts that need M2 code, noted); first public push | 8–12 | Not started |
| **M2 Safe parsing** | Untrusted XML handled safely; first full 8-step loop (H-8) | FR-020 – FR-025, FR-027, FR-033, TR-022 Passing | 4–6 | Not started |
| **M3 Domain core** | All classification, ranking, and advice rules, pure | FR-028 – FR-030, FR-052 – FR-072, FR-085 Passing at domain level | 8–10 | Not started |
| **M4 Storage and import** | Scans stored safely; import/list/delete via CLI | FR-001 – FR-006, FR-010 – FR-012, FR-026, FR-031, FR-032, FR-040 – FR-042, TR-030 – TR-036 Passing | 5–7 | Not started |
| **M5 Compare and reports** | End-to-end comparison and reports | FR-050, FR-051, FR-068, FR-080 – FR-088, e2e c01 – c14 Passing; golden files approved; MC-01 done | 6–8 | Not started |
| **M6 Masking** | Safe masked reports | FR-090 – FR-094, c15 Passing; MC-03 done | 3–4 | Not started |
| **M7 Hardening and release** | Release-ready MVP | NFR-001, NFR-007, smoke test Passing; README; MC-02; no traceability gaps; SM-01 – SM-08 met | 3–5 | Not started |

## 4. M0 — Bootstrap (detailed)

### T-001 — Repository foundation
- **Requirements:** TR-100, TR-102, TR-SEC-04, DEC-005, DEC-028
- **Steps:**
  1. ★ Owner go-ahead, then rename branch `master` → `main`.
  2. Create `.gitignore` per TR-SEC-04 (plus `.claude/settings.local.json`, `CLAUDE.local.md`, `.claude/state/`).
  3. Create `LICENSE` (MIT; copyright holder confirmed by owner).
  4. Create `README.md` stub: one-paragraph description, authorised-use notice, "under development".
- **Verification:** `git branch` shows `main`; owner reviews the three files.
- **Done when:** owner accepts. No commit yet.
- **Status:** In progress — steps 1–3 done early with the first push (DEC-049, 2026-10-28); step 4 (README) remains

### T-002 — Python project and environment
- **Requirements:** TR-001 – TR-003, TR-010 – TR-012, TR-060 – TR-066, DEC-024 – DEC-026
- **Steps:**
  1. `pyproject.toml`: metadata, `requires-python`, pinned runtime and dev dependencies, `[project.scripts]`, ruff/mypy/pytest/coverage settings, `req` marker registration.
  2. `py -3.13 -m venv .venv`; ★ owner approves the install command; `pip install -e ".[dev]"`.
  3. Write `requirements-dev.lock.txt` from `pip freeze`.
  4. Package skeleton: `src/testbondanh/__init__.py` with `__version__`; empty layer packages per SAD §9.
  5. ★ Owner runs or approves `pip-audit` (needs network).
- **Verification:** `.venv\Scripts\python.exe -c "import testbondanh"` succeeds; `pip-audit` clean; ruff and mypy run without errors.
- **Status:** Not started

### T-003 — Verification entry point and baseline safety tests
- **Requirements:** TR-067, TR-SEC-02, TR-SEC-03, TR-SEC-04, DEC-031, DEC-038
- **Steps:**
  1. Tests first (TS-05): `test_network_block_is_active`, `test_gitignore_contains_required_patterns`, `test_fixtures_contain_only_documentation_addresses` (passes trivially on an empty fixture folder; also tested with a temporary bad fixture). ★ Owner approves tests.
  2. `tests/conftest.py` with the autouse network block.
  3. `scripts/verify.py`: steps 1–4 of Test Strategy §11.1, `--quick` flag, placeholder for step 0 (locks) and step 5 (trace).
- **Verification:** `verify.py` passes; deliberately breaking each check (owner present) makes it fail.
- **Status:** Not started

### T-004 — Traceability script and first commit
- **Requirements:** DEC-039, TS-31, TS-32, Test Strategy §11.1 step 5
- **Steps:**
  1. Tests first for `scripts/trace.py`: untagged test → fail; unknown ID → fail; valid IDs → pass. ★ Owner approves tests.
  2. Implement `trace.py --check` (reads requirement IDs from `docs/**`, markers from tests) and `trace.py --report` (prints the Section 3 mapping).
  3. Wire into `verify.py` step 5.
  4. ★ Owner instructs the first commit (local only). Commit includes all `docs/`.
- **Verification:** `verify.py` full run passes; `git log` shows one commit on `main`.
- **Status:** Not started

## 5. M1 — Harness (detailed)

Each task implements one harness step (AI Harness Design §16) and records evidence in `docs/harness/HARNESS-VERIFICATION.md`.

| Task | Harness step | Content | Verification | Status |
|---|---|---|---|---|
| **T-010** | H-1 | `CLAUDE.md` (< 200 lines) and `.claude/rules/` (domain, adapters, tests, fixtures); create `HARNESS-VERIFICATION.md` | V-01, V-02 | Not started |
| **T-011** | H-2 | `.claude/settings.json`: plugins disabled, permissions per Harness §5; resolve the three ⚑ verify items | V-03, V-04; `claude doctor` clean | Not started |
| **T-012** | H-5a | `scripts/lock_tests.py` (interactive), HK-01 `protect_tests.py` with hook unit tests, `verify.py` step 0 | V-05 | Not started |
| **T-013** | H-5b | HK-02 `lint_file.py` and HK-03 `stop_verify.py` (loop guard), with hook unit tests | V-06, V-07 | Not started |
| **T-014** | H-6 | `scripts/repo_audit.py` with tests; `.githooks/pre-commit`; `core.hooksPath`; HK-04 `guard_git.py` | V-08 | Not started |
| **T-015** | H-7 | HK-05 `session_context.py` reading the "Current task" line | V-11 | Not started |
| **T-016** | H-3 | `/write-tests` skill; demonstrate on **FR-021** (the tests become T-021's tests if approved) | V-09 | Not started |
| **T-017** | H-4 | `code-reviewer` subagent; seeded-defect test on a scratch branch (★ owner approves creating and later deleting the scratch branch) | V-10 | Not started |
| **T-018** | — | First public push: ★ owner checks the commit author email (R-19), runs `pip-audit`, confirms `repo_audit.py` passes; ★ owner instructs push | Remote shows `main`; audit evidence recorded | Not started |

**Order note:** hooks (T-012 – T-015) come before the skill and subagent (T-016 – T-017) in this plan, so that the skill's first real use already runs under test-lock and verification hooks. This differs from Harness Design §16's H-3/H-4-before-H-5 listing; the dependencies there allow either order. *(Flagged for owner review.)*

## 6. M2 — Safe Parsing (detailed)

All tasks follow the full 8-step workflow. **T-020 is harness step H-8:** the first complete loop, with evidence recorded.

| Task | Requirements | Content | Status |
|---|---|---|---|
| **T-020** | TR-022, FR-022, NFR-003 | Fixtures `xxe_local_file.xml`, `xxe_external_dtd.xml`, `billion_laughs.xml`, `reference_full.xml`; `adapters/nmap_xml.parse` minimal; `domain/errors.py` with `UnsafeXmlError`. **Proves defusedxml on Python 3.13 (R-11).** If it fails: stop, report, revisit DEC-025 | Not started |
| **T-021** | FR-020, FR-021, NFR-002, TR-020 | `adapters/files`: existence, readability, size check before parse; errors E-IMP-001 – 003 (tests from T-016) | Not started |
| **T-022** | FR-023, FR-024, FR-025 | Well-formedness and truncation, Nmap identification, version check; malformed fixtures | Not started |
| **T-023** | FR-027, FR-033, TR-024, TR-052 | Required data, host without IP, ignored elements; parse into raw values; SHA-256 helper | Not started |
| **T-024** | — | Milestone review: ★ owner reviews M2 results; Claude proposes the detailed M3 task list (refinement of Section 7) | Not started |

## 7. M3 – M7 (outline; refined at each milestone start)

| Milestone | Planned tasks (titles) |
|---|---|
| **M3 Domain core** | T-030 domain model and builders · T-031 port and address coverage (FR-029, FR-030) · T-032 completeness (FR-028) · T-033 effective state and groups (FR-054, FR-055) · T-034 host rules (FR-052, FR-053, FR-056 – FR-058) · T-035 port rules (FR-059 – FR-062) · T-036 service rules (FR-063 – FR-065) · T-037 FR-066, FR-067, FR-069, AC-C12 · T-038 ranking, advice, ordering (FR-070 – FR-072, FR-085) · T-039 milestone review |
| **M4 Storage and import** | T-040 schema and migrations (TR-030 – TR-036) · T-041 save/load, atomic import, ID non-reuse, secure delete · T-042 import service (FR-026, FR-028 – FR-032) · T-043 CLI skeleton and error catalogue (FR-001 – FR-006, FRD §15) · T-044 list and delete (FR-040 – FR-042) · T-045 data folder and Git warning (FR-010 – FR-012) · T-046 milestone review |
| **M5 Compare and reports** | T-050 scan selection and first-seen (FR-050, FR-051, FR-068) · T-051 e2e comparison fixtures c01 – c14 · T-052 Markdown renderer (FR-082, FR-087, FR-088) · T-053 JSON renderer (FR-083, FR-084) · T-054 report files and terminal summary (FR-080, FR-081, FR-086) · T-055 golden files ★ owner review and MC-01 · T-056 milestone review |
| **M6 Masking** | T-060 placeholders and seed (FR-090 – FR-092) · T-061 labelling and leak check (FR-093, FR-094, c15) · T-062 ★ MC-03 and milestone review |
| **M7 Hardening and release** | T-070 performance (NFR-001) · T-071 Windows paths and installed-command smoke test (NFR-007, DEC-034) · T-072 README and ★ MC-02 · T-073 release check: full verify, `pip-audit`, no traceability gaps, SM-01 – SM-08 status, ★ owner instructs release push |

## 8. Session Routine (about one hour)

1. **Start (5 min):** HK-05 shows branch, current task, lock count. Claude restates the task, its requirement IDs, and the next step.
2. **Work (40 min):** one workflow step or a small group of steps, stopping at any ★ checkpoint.
3. **Close (10 min):** `verify.py --quick`; update task status and the "Current task" line; note anything for the decision log or risk register; ★ owner decides on commit.

A task may span sessions; it must always stop at a checkpoint or in a state where `verify.py --quick` passes (or failures are recorded as expected red tests).

## 9. Change Control

- Adding, removing, or reordering tasks: owner approval; recorded in the revision history.
- Moving a "Should" requirement to a later release: owner approval and a decision-log entry (PRD §10).
- Discovering missing or wrong requirements: stop, raise with the owner, update the source document first (it is Approved, so it gets a new version), then the plan.

## 10. Approval Checklist

To be completed by the owner. **No item is checked until the owner explicitly approves it.**

- [ ] Milestones, exit criteria, and estimates (§3)
- [ ] M0 tasks T-001 – T-004 (§4)
- [ ] M1 tasks T-010 – T-018, including the order note (§5)
- [ ] M2 tasks T-020 – T-024 (§6)
- [ ] M3 – M7 outline (§7)
- [ ] Session routine and change control (§8 – §9)
- [ ] **Development Plan approved — status may change to "Approved" (version 1.0)**
