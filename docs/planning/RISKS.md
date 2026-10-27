# TestBondanh — Risk Register

| Field | Value |
|---|---|
| Document | Risk Register |
| Project | TestBondanh — Network Security Monitoring Tool |
| Purpose | Track project risks, their mitigations, and their current status in one place |
| Status | **Draft** — living document, awaiting owner review |
| Version | 0.2 |
| Owner | Project owner (Chingmony) |
| Last updated | 2026-10-28 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-28 | Claude Code | Initial register: BRD R-01 – R-10 carried over; R-11 – R-20 added from later documents |
| 0.2 | 2026-10-28 | Claude Code | R-19 closed: commit email already noreply |

## How to Use

- **Likelihood / Impact:** Low · Medium · High.
- **Status:** Open (mitigation planned) · Mitigating (mitigation in progress) · Closed (no longer applies, with date and reason) · Occurred (became an issue; see notes).
- Review the register at each milestone review (T-024, T-039, …) and whenever a new risk is noticed. Never delete rows; close them.

## Register

### Business risks (from BRD §13)

| ID | Risk | L | I | Mitigation | Where | Status |
|---|---|---|---|---|---|---|
| R-01 | AI-generated comparison logic is plausible but wrong, causing false alarms | M | H | Tests-first with owner approval (DEC-035); classification tested at domain and e2e levels (TS-01); seeded-defect reviewer check (V-10) | M3, M5 | Open |
| R-02 | Real scan data or a database pushed to the public repo | M | H | Data folder outside repo (DEC-016); `.gitignore` `*.xml`/`*.db` (TR-SEC-04); fixture address test (TR-SEC-03); repo audit + git hook (DEC-045); Claude denied reading the data folder | M0, M1 | Open |
| R-03 | Input parsing vulnerability (XXE, memory exhaustion) | M | H | defusedxml (DEC-025); size check before parse (TR-020); hostile fixtures (T-020) | M2 | Open |
| R-04 | Scope creep from AI or enthusiasm | H | M | Every task lists requirement IDs; `trace.py` rejects unknown IDs; out-of-scope tables | All | Open |
| R-05 | Nmap XML varies across versions or scan options | M | M | Reference fixture modelled on the official DTD; unknown elements ignored (FR-033); version check (FR-025) | M2 | Open |
| R-06 | Context lost between one-hour sessions | H | M | HK-05 session context; "Current task" line; decision log; session routine (Plan §8) | M1 | Open |
| R-07 | Tool misused against networks the user does not own | L | H | No scanning (BR-011); authorised-use notice (FR-006, PR-020) | M4, M7 | Open |
| R-08 | Masking leaks identifiers | M | M | Leak check fails closed (FR-094); property test over all fixtures; MC-03 | M6 | Open |
| R-09 | Two Python versions installed (3.11.0 / 3.13.5) cause inconsistent results | M | M | Python 3.13 venv; explicit interpreter everywhere (DEC-024) | M0 | Mitigating (decided; applied in T-002) |
| R-10 | Plugins inject instructions that conflict with project rules (observed 2026-10-27) | M | M | Instruction hierarchy; plugins disabled for this project (DEC-040) | M1 | Occurred — mitigation in T-011 |

### Technical and process risks (added after the BRD)

| ID | Risk | L | I | Mitigation | Where | Status |
|---|---|---|---|---|---|---|
| R-11 | `defusedxml` 0.7.1 (released March 2021) behaves incorrectly on Python 3.13 or becomes unmaintained | L | H | Proven by test first (T-020, TR-022). Fallback: standard-library expat with entity-declaration handler that raises, which requires a new DEC and owner approval | M2 | Open |
| R-12 | Claude Code behaves differently from documentation on Windows (three ⚑ verify items) | M | M | Verified in T-011/T-012 before relying on them; fallback designs chosen then | M1 | Open |
| R-13 | Claude Code updates change hook or settings behaviour | M | M | Re-run V-01 – V-11 after updates; hook unit tests | Ongoing | Open |
| R-14 | Harness protections silently off when `.venv` is missing or broken | L | H | Stop-and-report rule (Harness §13); HK-05 warns when `.venv` is missing | M1 | Open |
| R-15 | Owner approval becomes a bottleneck or approvals become superficial ("approval fatigue") | M | M | Small tasks; short Given/When/Then tests; checklists; reviewer verdict summarises | All | Open |
| R-16 | Estimate overrun (40–55 sessions) | M | L | Milestone reviews; "Should" items deferrable with approval; no deadline (C-05) | All | Open |
| R-17 | Hand-written fixtures miss real-world Nmap output patterns | M | M | Reference fixture from the DTD. Optional later: owner validates the tool locally against their own authorised scan, **never committed** | M2, M7 | Open |
| R-18 | Address-coverage heuristic misreads `args` (FQ-03) | M | L | Errs toward "coverage unknown", which yields uncertain findings, not false confirmations; dedicated tests | M3 | Open |
| R-19 | Personal email address published in public commit metadata | M | M | Commit identity checked before the first push: already GitHub's noreply address | M1 | Closed (2026-10-28) — git `user.email` is the noreply address |
| R-20 | Long AI sessions lose detail when conversation context is summarised | M | M | Approved documents and the decision log are the source of truth, not conversation memory; tasks sized to one session | All | Open |

## Closed Risks

| ID | Closed | Reason |
|---|---|---|
| R-19 | 2026-10-28 | Git `user.email` is GitHub's noreply address |

## Approval Checklist

To be completed by the owner. **No item is checked until the owner explicitly approves it.**

- [ ] Risks R-01 – R-20 are relevant and correctly rated
- [ ] Mitigations are acceptable
- [ ] **Risk Register approved — status may change to "Approved" (version 1.0)**
