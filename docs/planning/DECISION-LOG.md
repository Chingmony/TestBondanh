# TestBondanh — Decision Log

| Field | Value |
|---|---|
| Document | Decision Log |
| Purpose | Record significant project decisions, the options considered, and the reasoning, so later documents, code, and AI agents can follow them consistently |
| Status | **Draft** — living document |
| Version | 0.17 |
| Owner | Project owner (Chingmony) |
| Last updated | 2026-10-27 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-27 | Claude Code | Initial log; DEC-001 – DEC-009 recorded from owner answers during BRD planning |
| 0.2 | 2026-10-27 | Claude Code | Noted owner approval of BRD v1.0 (the source for DEC-002 – DEC-008) |
| 0.3 | 2026-10-27 | Claude Code | Added DEC-010 – DEC-016 from PRD planning answers |
| 0.4 | 2026-10-27 | Claude Code | Added DEC-017; noted PRD v1.0 approval |
| 0.5 | 2026-10-27 | Claude Code | Added DEC-018 – DEC-022 from FRD planning answers |
| 0.6 | 2026-10-27 | Claude Code | Added DEC-023; noted FRD v1.0 approval |
| 0.7 | 2026-10-27 | Claude Code | Added DEC-024 – DEC-028 from TRD/SAD planning answers |
| 0.8 | 2026-10-27 | Claude Code | Noted TRD v1.0 approval |
| 0.9 | 2026-10-27 | Claude Code | Added DEC-029 – DEC-034 (Proposed) from SAD draft |
| 0.10 | 2026-10-27 | Claude Code | DEC-029 – DEC-034 accepted with SAD v1.0 approval |
| 0.11 | 2026-10-27 | Claude Code | Added DEC-035 – DEC-039 from test strategy planning answers |
| 0.12 | 2026-10-28 | Claude Code | Noted Test Strategy and RTM v1.0 approval |
| 0.13 | 2026-10-28 | Claude Code | Added DEC-040 – DEC-045 from harness planning answers |
| 0.14 | 2026-10-28 | Claude Code | Noted AI Harness Design v1.0 approval; HQ-01 resolved (`inherit`) |
| 0.15 | 2026-10-28 | Claude Code | Added DEC-046 – DEC-048 from planning answers |
| 0.16 | 2026-10-28 | Claude Code | Added DEC-049: documentation pushed before the harness, on owner instruction |
| 0.17 | 2026-10-29 | Claude Code | Added DEC-050; noted Development Plan and Risk Register v1.0 approval |

## How to Use This Log

- One entry per decision. Never delete an entry; if a decision changes, add a new entry and mark the old one **Superseded by DEC-xxx**.
- **Status values:** *Proposed* (awaiting owner) · *Accepted* (owner explicitly decided) · *Superseded* · *Rejected*.
- Documents and code reference decisions by ID (e.g., "per DEC-003").

## Decision Index

| ID | Decision | Status | Date |
|---|---|---|---|
| DEC-001 | Documentation-first, approval-gated workflow | Accepted | 2026-10-27 |
| DEC-002 | AI harness is a constraint (how it is built), not a business requirement | Accepted | 2026-10-27 |
| DEC-003 | False positives are worse than false negatives | Accepted | 2026-10-27 |
| DEC-004 | Security is a cross-cutting concern because the repository is public | Accepted | 2026-10-27 |
| DEC-005 | MIT license | Accepted | 2026-10-27 |
| DEC-006 | Live scanning out of MVP; possible future phase | Accepted | 2026-10-27 |
| DEC-007 | Report masking included in MVP | Accepted | 2026-10-27 |
| DEC-008 | Success requires both a tested MVP and a verified AI harness | Accepted | 2026-10-27 |
| DEC-009 | Start the decision log alongside the BRD | Accepted | 2026-10-27 |
| DEC-010 | Masking: per-report consistent placeholders; IP/hostname/MAC hidden | Accepted | 2026-10-27 |
| DEC-011 | Three-level importance ranking; uncertain findings never ranked | Accepted | 2026-10-27 |
| DEC-012 | Keep scans until the user deletes them; delete command in MVP | Accepted | 2026-10-27 |
| DEC-013 | Default comparison is latest vs. previous; any two selectable; no profiles in MVP | Accepted | 2026-10-27 |
| DEC-014 | Performance target: 256 hosts, under 10 s; 50 MB input limit | Accepted | 2026-10-27 |
| DEC-015 | Fixed one-line advice for High/Medium findings; no online lookups | Accepted | 2026-10-27 |
| DEC-016 | Default data location outside the repo: %LOCALAPPDATA%\TestBondanh | Accepted | 2026-10-27 |
| DEC-017 | A host that stops answering is an uncertain observation, never a confirmed change | Accepted | 2026-10-27 |
| DEC-018 | Host identity is the IP address; same-MAC note when a device moves | Accepted | 2026-10-27 |
| DEC-019 | CLI: one `testbondanh` command with sub-commands; integer scan IDs | Accepted | 2026-10-27 |
| DEC-020 | Exit codes 0/1/2/3; no "fail on High" option in MVP | Accepted | 2026-10-27 |
| DEC-021 | Timestamped report names; never overwrite | Accepted | 2026-10-27 |
| DEC-022 | IPv6 supported alongside IPv4; Nmap 7.x and later | Accepted | 2026-10-27 |
| DEC-023 | FRD open questions FQ-01 – FQ-05 resolved as proposed | Accepted | 2026-10-27 |
| DEC-024 | Python 3.13 in a project virtual environment; always call its interpreter explicitly | Accepted | 2026-10-27 |
| DEC-025 | `defusedxml` is the only runtime dependency | Accepted | 2026-10-27 |
| DEC-026 | Development tools: pytest, pytest-cov, ruff, mypy, pip-audit via venv + pip | Accepted | 2026-10-27 |
| DEC-027 | Database protected by Windows per-user permissions; no encryption in MVP | Accepted | 2026-10-27 |
| DEC-028 | Default branch `main` | Accepted | 2026-10-27 |
| DEC-029 | Layered architecture with a pure core | Accepted | 2026-10-27 |
| DEC-030 | Dependency rules enforced by an `ast`-based architecture test | Accepted | 2026-10-27 |
| DEC-031 | Verification entry point is `scripts/verify.py` | Accepted | 2026-10-27 |
| DEC-032 | Coverage stored compactly (CIDR networks, port ranges) | Accepted | 2026-10-27 |
| DEC-033 | Comparison on fully loaded scans in memory | Accepted | 2026-10-27 |
| DEC-034 | CLI end-to-end tests call `main(argv)` in-process, plus one installed-command smoke test | Accepted | 2026-10-27 |
| DEC-035 | Tests first, approved by the owner, then implementation without changing them | Accepted | 2026-10-27 |
| DEC-036 | Fixtures: minimal hand-written XML, one realistic reference, generated only for size/performance | Accepted | 2026-10-27 |
| DEC-037 | Golden files reviewed by the owner and never regenerated automatically | Accepted | 2026-10-27 |
| DEC-038 | Coverage: 95 % branch for domain/reporting, 85 % overall | Accepted | 2026-10-27 |
| DEC-039 | Traceability test mapping generated from `req` markers | Accepted | 2026-10-27 |
| DEC-040 | Disable Figma and Vercel plugins for this project | Accepted | 2026-10-28 |
| DEC-041 | Hooks are Python scripts in exec form using the venv interpreter | Accepted | 2026-10-28 |
| DEC-042 | Two-layer test lock: PreToolUse hook prevents, verify.py detects | Accepted | 2026-10-28 |
| DEC-043 | First skill is `/write-tests` | Accepted | 2026-10-28 |
| DEC-044 | Read-only `code-reviewer` subagent (Read, Grep, Glob) | Accepted | 2026-10-28 |
| DEC-045 | `repo_audit.py` run by git pre-commit hook and by a Claude PreToolUse hook | Accepted | 2026-10-28 |
| DEC-046 | Riskiest work first (safe parsing, then domain core) | Accepted | 2026-10-28 |
| DEC-047 | Local commits from M0; first public push only after the harness is verified | Amended by DEC-049 | 2026-10-28 |
| DEC-048 | Detail M0–M2 now; refine later milestones at their start | Accepted | 2026-10-28 |
| DEC-049 | Push documentation, LICENSE, and .gitignore before the harness exists | Accepted | 2026-10-28 |
| DEC-050 | Harness build order: permissions and hooks before the skill and subagent | Accepted | 2026-10-29 |

---

### DEC-001 — Documentation-first, approval-gated workflow

- **Status:** Accepted (owner's mission brief, 2026-10-27)
- **Context:** The project tests whether AI-assisted development can be kept reliable and traceable.
- **Decision:** Documents are produced in sequence (BRD → PRD → FRD → TRD/SAD → test strategy/traceability → harness design → plan). Each requires explicit owner approval before the next begins. No commits, pushes, or deletions without owner instruction.
- **Alternatives:** Code-first with documentation afterwards — rejected: AI agents would have no authoritative reference to check work against.
- **Consequences:** Slower start; every later artifact can be traced to an approved source.

### DEC-002 — AI harness is a constraint, not a business requirement

- **Status:** Accepted (owner answer, planning batch 1 Q4)
- **Context:** The project has two purposes: the security tool and the AI workflow evaluation.
- **Decision:** The harness is recorded as constraint C-01 ("how it is built"). It has no `BR-` IDs. Its detailed design lives in `docs/harness/AI-HARNESS-DESIGN.md`.
- **Alternatives:** Harness as first-class business objective with its own BRs — not chosen.
- **Consequences:** The BRD stays focused on the product. Harness verification is still a success criterion via SM-07 (see DEC-008).

### DEC-003 — False positives are worse than false negatives

- **Status:** Accepted (owner answer, planning batch 1 Q5)
- **Context:** Change detection must choose how to act when evidence is ambiguous.
- **Decision:** The tool must not claim a change it cannot support. Ambiguous findings are reported as *uncertain*, separately from confirmed changes.
- **Alternatives:** Report every possible change (higher sensitivity, more noise) — rejected.
- **Consequences:** Drives BR-004 and BR-005. Some real changes may initially appear only as "uncertain"; uncertain findings must still be visible so they are not silently lost.

### DEC-004 — Security as a cross-cutting concern (public repository)

- **Status:** Accepted (owner answer, planning batch 1 Q5)
- **Context:** The repository is public, and scan data describes a network's attack surface.
- **Decision:** Every document must address security. Baseline rules: synthetic data only with documentation-reserved IP ranges; no real scans, databases, reports, or secrets in Git; all input treated as untrusted; no external data transmission; minimal pinned dependencies.
- **Consequences:** Drives BR-006, BR-009, BR-010, BR-014 and BRD Section 9. Harness must enforce repository hygiene automatically, not rely on memory.

### DEC-005 — MIT license

- **Status:** Accepted (owner answer, planning batch 2 Q1)
- **Context:** A public repository without a license is "all rights reserved".
- **Decision:** License the project under MIT.
- **Consequences:** A `LICENSE` file will be added when the repository is first populated (not yet created). Dependencies must have MIT-compatible licenses.

### DEC-006 — Live scanning: out of MVP, possible future phase

- **Status:** Accepted (owner answer, planning batch 2 Q2)
- **Decision:** The MVP never initiates scans (BR-011). Live scanning may be considered later, only through a new BRD revision restricted to explicitly authorised targets.
- **Consequences:** No Nmap installation is needed for development or testing.

### DEC-007 — Report masking included in MVP

- **Status:** Accepted (owner clarification, 2026-10-27)
- **Decision:** An option to mask identifying details in reports is a Must requirement (BR-009).
- **Alternatives:** Defer to a later release — not chosen.
- **Consequences:** Adds an estimated 2–3 sessions of work. Exact masking coverage is open (BRD OQ-03).

### DEC-008 — Success requires a tested MVP and a verified harness

- **Status:** Accepted (owner clarification, 2026-10-27)
- **Decision:** The project succeeds only when the MVP meets its tested requirements **and** the harness components (`CLAUDE.md`, a skill, a read-only review subagent, a verification hook, a test-and-review loop) each have recorded verification evidence.
- **Consequences:** BRD SM-07. Harness stages need their own verification steps in the development plan.

### DEC-009 — Start the decision log alongside the BRD

- **Status:** Accepted (owner clarification, 2026-10-27)
- **Context:** Original document order placed this log near the end.
- **Decision:** Start the log now so decisions are recorded with their reasoning when they are made.
- **Consequences:** One extra file to maintain from the beginning.

### DEC-010 — Masking approach

- **Status:** Accepted (owner, PRD batch 1 Q1)
- **Decision:** Mask IP addresses, hostnames, and MAC addresses with placeholders (`HOST-01`, `MAC-01`) that stay the same throughout one report but differ between reports. Keep ports, services, and versions. Exclude raw script output. Mark masked reports and state that masking is best-effort.
- **Alternatives:** Full redaction — rejected, because the reader couldn't tell which host changed.
- **Consequences:** Conflicts with deterministic output. The PRD proposes a per-run seed that tests can fix (PRD §7.3).

### DEC-011 — Importance ranking

- **Status:** Accepted (owner, PRD batch 1 Q2)
- **Decision:** High / Medium / Low by documented rules (PRD §6.3). Uncertain observations are listed separately and never ranked.
- **Alternatives:** Unranked list — rejected because it's too much effort for a non-specialist.

### DEC-012 — Retention and deletion

- **Status:** Accepted (owner, PRD batch 1 Q3)
- **Decision:** Keep scans until the user deletes them; delete-a-scan command is in the MVP (PR-006).
- **Consequences:** Being able to remove data is a privacy control. Deletion needs confirmation.

### DEC-013 — Comparison selection

- **Status:** Accepted (owner, PRD batch 1 Q4)
- **Decision:** Default latest vs. previous; any two scans selectable; differing coverage is reported as uncertain; no named network profiles in MVP.

### DEC-014 — Performance target and input size limit

- **Status:** Accepted (owner, PRD batch 2)
- **Decision:** Up to 256 hosts; import, compare, and report each under 10 seconds on the reference machine; files over 50 MB rejected (NFR-001, NFR-002).
- **Consequences:** The size limit doubles as a defence against oversized hostile files.

### DEC-015 — Report guidance

- **Status:** Accepted (owner, PRD batch 2)
- **Decision:** One-line advice written in advance for each High and Medium rule. No online lookups (keeps BR-010).

### DEC-016 — Default data location

- **Status:** Accepted (owner, PRD batch 2)
- **Decision:** Database and reports default to `%LOCALAPPDATA%\TestBondanh`, which the user can change; warn if the destination is inside a Git repository (PR-019).
- **Alternatives:** Project-local `./data` excluded from Git — rejected because one wrong `.gitignore` change could expose real data.

### DEC-017 — A host that stops answering is uncertain

- **Status:** Accepted (owner, PRD review, 2026-10-27)
- **Context:** PRD PQ-01. A host answered in the baseline but not in a newer scan that was complete and covered it.
- **Decision:** Report it as an **uncertain observation** ("host not observed"), never as a confirmed change.
- **Alternatives:** Confirmed "host not responding" change — rejected. A host may be off, asleep, or behind a firewall that now blocks probes; claiming a change would break DEC-003.
- **Consequences:** No rule in PRD §6.2 can confirm a host disappearing. Tests must assert this for both complete and incomplete newer scans.

### DEC-018 — Host identity by IP address

- **Status:** Accepted (owner, FRD batch 1 Q2)
- **Decision:** Two observations are the same host only when their IP addresses match. When both scans record MAC addresses and the same MAC appears at a different IP, the finding gets a "possibly the same device" note. Classification doesn't change.
- **Alternatives:** Identify hosts by MAC — rejected for MVP. It would add an "address changed" category, which needs a PRD revision.
- **Consequences:** A device that changes address (DHCP) appears as one new host plus one host not observed. This is documented in every report's Limitations section (FRD FR-087).

### DEC-019 — CLI structure and scan IDs

- **Status:** Accepted (owner, FRD batch 1 Q1)
- **Decision:** `testbondanh import | list | compare | delete`. Scan IDs are integers that are never reused. A global `--data-dir` option or the `TESTBONDANH_DATA_DIR` environment variable overrides the data folder.
- **Alternatives:** Short hash IDs — rejected because they're harder to type.

### DEC-020 — Exit codes

- **Status:** Accepted (owner, FRD batch 1 Q3)
- **Decision:** 0 success, 1 input/data problem, 2 usage error, 3 internal error. Comparisons with High findings return 0. No "fail on High" option, because no PR requires it.

### DEC-021 — Report file naming

- **Status:** Accepted (owner, FRD batch 1 Q4)
- **Decision:** `compare-<baseline>-<newer>-<YYYYMMDD-HHMMSS>[-masked].md/.json` in `<data>
eports`, with `--output` to override. Existing files are never overwritten.

### DEC-022 — IPv6 and Nmap version support

- **Status:** Accepted (owner, FRD batch 1 Q5 and recommendation on BRD OQ-06)
- **Decision:** IPv6 is handled the same as IPv4, with fixtures in `2001:db8::/32`. Nmap 7.x and later is supported; older versions are rejected. Unrecognised XML elements are ignored.

### DEC-023 — FRD open questions resolved as proposed

- **Status:** Accepted (owner approved FRD v1.0 as drafted, 2026-10-27)
- **Decision:**
  - FQ-01: `filtered` → `open` is **uncertain** (`previous_state_undetermined`), not a confirmed opening.
  - FQ-02: truncated XML is rejected, not partially imported.
  - FQ-03: address coverage uses the heuristic based on the `args` attribute; when unsure, coverage is unknown.
  - FQ-04: Nmap versions before 7 are rejected.
  - FQ-05: High-importance ports are TCP 22, 23, 445, 3389, 5900.
- **Consequences:** FQ-01 is a strict reading of PRD C-4. A firewall change that exposes a service appears as uncertain, not High. Revisit if real usage shows this hides important exposures.

### DEC-024 — Python 3.13 and explicit interpreter

- **Status:** Accepted (owner, TRD/SAD batch 1 Q1)
- **Context:** `python` on the PATH runs 3.11.0; the `py` launcher has 3.13.5.
- **Decision:** Target Python 3.13. Create `.venv` with `py -3.13`. Every script and hook calls `.venv\Scripts\python.exe`, never a bare `python`.
- **Alternatives:** 3.11 — rejected because it gets security fixes for about two years less.
- **Consequences:** Removes a class of "works in one place, fails in another" problems, especially for hooks.

### DEC-025 — `defusedxml` as the only runtime dependency

- **Status:** Accepted (owner, TRD/SAD batch 1 Q2)
- **Decision:** Parse Nmap XML with `defusedxml==0.7.1` (PSF licence).
- **Alternatives:** Standard library parser with hand-written protections — rejected; the security-critical code would be our own and unreviewed.
- **Consequences:** The latest stable release is from March 2021. Compatibility with Python 3.13 must be proven by test (TRD TR-022).

### DEC-026 — Development toolchain

- **Status:** Accepted (owner, TRD/SAD batch 1 Q3)
- **Decision:** pytest 9.1.1, pytest-cov 7.1.0, ruff 0.17.3, mypy 2.4.0, pip-audit 2.10.1, setuptools 84.2.1, installed with `venv` + `pip`. Exact pins, plus a full `pip freeze` lock file.
- **Alternatives:** `uv` — not chosen, to keep the toolchain transparent while learning.

### DEC-027 — Database protection at rest

- **Status:** Accepted (owner, TRD/SAD batch 1 Q4; resolves BRD OQ-07)
- **Decision:** Rely on Windows per-user permissions on `%LOCALAPPDATA%`. No encryption. Enable SQLite `secure_delete` so deleted scans are overwritten.
- **Consequences:** Anyone with access to the Windows account can read the database. Documented in the README.

### DEC-028 — Default branch `main`

- **Status:** Accepted (owner, TRD/SAD batch 1 Q5; resolves BRD OQ-02)
- **Decision:** Use `main`. Rename the local `master` branch before the first commit, with the owner's go-ahead at that time.

### DEC-029 — Layered architecture with a pure core

- **Status:** Accepted (owner approved SAD v1.0, 2026-10-27)
- **Decision:** `cli` → `services` → `domain` and `reporting` (pure: no I/O, no clock, no random source) and `adapters` (all I/O).
- **Alternatives:** Flat modules — rejected because classification logic would mix with I/O and become harder to test and review.
- **Consequences:** The most important rules are tested with plain in-memory objects. Time and seeds are passed in as arguments.

### DEC-030 — Architecture test

- **Status:** Accepted (owner approved SAD v1.0, 2026-10-27)
- **Decision:** A test parses source imports with `ast` and fails on any import that breaks SAD §5.
- **Alternatives:** Third-party import-linting tool — rejected to avoid a dependency; review-only enforcement — rejected because it isn't deterministic.

### DEC-031 — `scripts/verify.py` as the single verification entry point

- **Status:** Accepted (owner approved SAD v1.0, 2026-10-27)
- **Decision:** One Python script runs ruff check, ruff format check, mypy, and pytest with coverage. Run it as `.venv\Scripts\python.exe scriptserify.py`.
- **Alternatives:** PowerShell script — rejected; execution-policy settings can block `.ps1` files.

### DEC-032 — Compact coverage storage

- **Status:** Accepted (owner approved SAD v1.0, 2026-10-27)
- **Decision:** Store address coverage as CIDR networks and port coverage as range strings; expand in memory when needed.

### DEC-033 — In-memory comparison

- **Status:** Accepted (owner approved SAD v1.0, 2026-10-27)
- **Decision:** Load both scans fully and compare in memory. This is sized for NFR-001 (≤ 256 hosts); revisit if larger networks come into scope.

### DEC-034 — CLI testing approach

- **Status:** Accepted (owner approved SAD v1.0, 2026-10-27)
- **Decision:** End-to-end tests call `main(argv)` in-process (fast, easy to inspect), plus one smoke test that runs the installed `testbondanh` command as a subprocess.

### DEC-035 — Tests first, owner-approved

- **Status:** Accepted (owner, test strategy batch 1 Q2)
- **Context:** When the same AI writes both code and tests, one misunderstanding can appear in both, and the tests then "confirm" the bug.
- **Decision:** For each task, Claude writes tests from the FR acceptance criteria. The owner approves them, they're confirmed to fail, and only then is code written. Approved tests aren't modified during implementation; enforcement is defined in the AI Harness Design.
- **Alternatives:** Code and tests together, reviewed afterwards — rejected because the tests can't serve as an independent check.
- **Consequences:** One extra short review per task.

### DEC-036 — Fixture strategy

- **Status:** Accepted (owner, test strategy batch 1 Q4)
- **Decision:** Minimal hand-written XML per case; one realistic synthetic reference fixture; generated fixtures only for the 256-host performance test and the oversized-file test.

### DEC-037 — Golden-file policy

- **Status:** Accepted (owner, test strategy batch 1 Q3)
- **Decision:** Golden reports are reviewed by the owner before commit and never regenerated automatically. There is no "update all" command.
- **Consequences:** Unintended output changes are always visible as test failures.

### DEC-038 — Coverage thresholds

- **Status:** Accepted (owner, test strategy batch 1 Q1)
- **Decision:** Branch coverage of at least 95 % for `domain` and `reporting`, and at least 85 % overall; the build fails below either.

### DEC-039 — Generated traceability

- **Status:** Accepted (owner, test strategy batch 1 Q5)
- **Decision:** Tests carry `@pytest.mark.req(...)`. `scripts/trace.py` generates the test-mapping and gaps sections of the RTM and fails verification for untagged tests or unknown requirement IDs. The BR → FR → component chain stays hand-written.

### DEC-040 — Disable unrelated plugins for this project

- **Status:** Accepted (owner, harness batch 1 Q1)
- **Context:** At session start on 2026-10-27, the Vercel plugin injected instructions that conflicted with the approval-gated workflow.
- **Decision:** Set `enabledPlugins` to `false` for the Figma and Vercel plugins in the project's `.claude/settings.json`. They stay enabled in other projects. The override must be confirmed in Stage 5.

### DEC-041 — Hook implementation

- **Status:** Accepted (owner, harness batch 1 Q3, with the design principles)
- **Decision:** Hooks are Python scripts in `.claude/hooks/`, run in exec form with `.venv\Scripts\python.exe`. Protective hooks fail closed; advisory hooks fail open. Hook scripts have unit tests and don't import the application package.
- **Alternatives:** Bash or PowerShell scripts — rejected because of shell differences on Windows and PowerShell execution policy.

### DEC-042 — Test lock

- **Status:** Accepted (owner, harness batch 1 Q2)
- **Decision:** The owner runs `scripts/lock_tests.py` (interactive confirmation) to record approved test hashes in `.claude/tests.lock`. A PreToolUse hook blocks edits to locked files; `verify.py` detects hash mismatches.
- **Consequences:** This is a guardrail against accidental changes, not a security boundary. Owner diff review remains the final check.

### DEC-043 — First skill `/write-tests`

- **Status:** Accepted (owner, harness batch 1 Q6)
- **Decision:** `/write-tests <REQ-IDs>` writes tagged tests, confirms they fail, and stops for approval. It can only be invoked explicitly.
- **Alternatives:** `/task` covering the whole workflow — deferred until `/write-tests` is proven.

### DEC-044 — Read-only review subagent

- **Status:** Accepted (owner, approved outline and batch 1)
- **Decision:** `.claude/agents/code-reviewer.md` with `tools: Read, Grep, Glob`. It receives the task ID, requirement IDs, and changed files, not the main session's reasoning. It ends every review with a verdict line. It must pass a seeded-defect test (V-10) before being trusted.

### DEC-045 — Repository audit

- **Status:** Accepted (owner, harness batch 1 Q4)
- **Decision:** `scripts/repo_audit.py` checks for forbidden files, non-documentation addresses, secret patterns, and lock integrity. It runs as a git pre-commit hook (covering everyone's commits) and as a Claude PreToolUse hook on `git commit` and `git push`. No `detect-secrets` dependency for now.

### DEC-046 — Riskiest work first

- **Status:** Accepted (owner, plan batch 1 Q1)
- **Decision:** After bootstrap and harness, build safe parsing (proving defusedxml), then the pure domain core, then storage, reports, and masking.
- **Alternatives:** Thin end-to-end slice first — rejected; the riskiest parts would come later.

### DEC-047 — Timing of the first public push

- **Status:** Accepted (owner, plan batch 1 Q2)
- **Decision:** Commit locally from M0. The first push happens after M1, once the repository audit and git pre-commit hook are verified. Every push needs explicit owner instruction.

### DEC-048 — Plan granularity

- **Status:** Accepted (owner, plan batch 1 Q3)
- **Decision:** M0–M2 tasks are fully detailed. M3–M7 are outlined and refined at each milestone review, with owner approval.

### DEC-049 — Push documentation before the harness exists

- **Status:** Accepted (owner instruction, 2026-10-28). Amends DEC-047.
- **Context:** The owner asked to push to `https://github.com/Chingmony/TestBondanh.git` before the harness (M1) was built.
- **Decision:** Make the first commit and push now, containing only the 11 documents, an MIT `LICENSE` ("Copyright (c) 2026 Chingmony"), and the TR-SEC-04 `.gitignore`. Rename the branch to `main` first (DEC-028).
- **Safeguards applied by hand in place of the not-yet-built `repo_audit.py`:**
  - The documents were scanned for non-documentation IPs, MAC addresses, emails, Windows user paths, and secret patterns. There were zero findings.
  - The scanner was first shown to catch planted examples of each type.
  - The commit identity uses GitHub's noreply email (R-19 resolved).
- **Consequences:** Later pushes still require owner instruction. Code pushes still wait for the verified harness (DEC-047 otherwise unchanged). T-001 is partly done: the branch rename, `LICENSE`, and `.gitignore` remain; the README is still to do.

### DEC-050 — Harness build order

- **Status:** Accepted (owner approved the Development Plan as written, 2026-10-29)
- **Decision:** Build the harness as CLAUDE.md → permissions → hooks (test lock, lint, stop-verify, repo audit, session context) → `/write-tests` skill → `code-reviewer` subagent.
- **Alternatives:** The mission's order (CLAUDE.md → skill → subagent → hooks) — not chosen. The skill's first real use would then run without test-lock and verification hooks.
- **Consequences:** The skill and subagent are demonstrated a few sessions later, but under the full set of protections. Reversible on owner request before T-012 starts.

---

## Pending Decisions

Not yet decided — listed so they are not lost.

| Topic | Options | Decide by |
|---|---|---|
| Review subagent model (HQ-01) | `inherit` accepted for now; revisit | After harness verification V-10 |
