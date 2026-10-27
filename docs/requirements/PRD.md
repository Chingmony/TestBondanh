# TestBondanh — Product Requirements Document (PRD)

| Field | Value |
|---|---|
| Document | Product Requirements Document |
| Project | TestBondanh — Network Security Monitoring Tool |
| Purpose | Define what the product does from the user's point of view: features, user journeys, change classification, report content, and quality targets |
| Status | **Approved** — by project owner, 2026-10-27 |
| Version | 1.0 |
| Based on | [BRD v1.0 (Approved)](BRD.md) |
| Owner / Approver | Project owner (Chingmony) |
| Author | Claude Code (drafted under owner direction) |
| Last updated | 2026-10-27 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-27 | Claude Code | Initial draft from approved outline and owner answers (PRD batches 1–2) |
| 1.0 | 2026-10-27 | Project owner | Approved; PQ-01 resolved as "uncertain" (DEC-017) |

## How to Read This Document

Labels (**Confirmed / Assumed / Proposed / Open**), priorities (**MoSCoW**), and ID conventions follow the [BRD](BRD.md#how-to-read-this-document). New ID prefixes:

- `PR-` product requirement (a user-visible feature or behaviour)
- `NFR-` non-functional requirement (a quality the product must have: speed, security, usability, etc.)
- `PQ-` PRD open question

Every PR and NFR lists the BR(s) it serves. Section 16 shows the reverse mapping. **Anything not traceable to a BR does not belong in the product.**

> **Level of detail:** this PRD describes commands by purpose ("import a scan"), not syntax. Exact command names, options, data fields, and Nmap XML element handling are specified in the FRD.

---

## 1. Purpose and Relationship to the BRD

The BRD (v1.0, approved 2026-10-27) defines *why* TestBondanh exists and how success is judged. This PRD turns those business requirements into a concrete product definition. It resolves BRD open questions **OQ-03** (masking), **OQ-04** (prioritisation), and **OQ-05** (retention). OQ-01, OQ-02, OQ-06, and OQ-07 remain for the TRD.

## 2. Product Overview

TestBondanh is a local command-line tool for Windows 11. The user runs Nmap against their own network, saves the result as XML, and imports it. TestBondanh keeps a private history of scans, compares any two of them, and produces a short, prioritised report that answers: **"What changed that I should look at, and what am I unsure about?"**

Its defining product principle, from BRD BR-004 and DEC-003:

> **Something seen can confirm a change. Something *not* seen never can.**

Positive evidence (a port observed open, a host observed responding) may support a confirmed change. Absence of evidence (a host missing, a port not scanned, a scan interrupted) produces an *uncertain observation*, never a confirmed change.

## 3. Persona and Usage Scenarios

### Persona — "Sokha" (Assumed, from BRD §4)

| Attribute | Description |
|---|---|
| Environment | Home lab or small office, roughly 5–50 devices |
| Skills | Can open a terminal and run a copied Nmap command; not a security specialist |
| Frequency | Scans weekly, or after adding or changing equipment |
| Goal | "Tell me what changed and whether I should care, in two minutes." |
| Concern | Does not want to leak details of their network |

### Usage scenarios

| ID | Scenario |
|---|---|
| US-1 | Sokha imports this week's scan and wants to know what changed since last week. |
| US-2 | Last night's scan was interrupted by a laptop sleep. Sokha must not be told that half the network vanished. |
| US-3 | Sokha wants advice on a forum and needs to share a report without revealing internal addresses. |
| US-4 | Sokha wants to know when port 3389 first appeared on a machine. |
| US-5 | Sokha accidentally imports the wrong file (not Nmap XML, or corrupted). |
| US-6 | Sokha wants to remove old scans containing sensitive data. |

## 4. User Journeys

### J-1 First run
1. Sokha runs the tool's help and reads how to import a scan and the authorised-use notice.
2. On first import, the tool creates its data folder in the per-user location (PR-018) and reports where it is.
3. With only one scan, a compare request explains that at least two scans are needed.

### J-2 Routine comparison (US-1, US-4)
1. Import the new scan → tool confirms import and states whether the scan looks **complete** or **incomplete** (PR-004).
2. Compare → by default, latest vs. previous (PR-008).
3. Terminal shows a short summary: counts of High/Medium/Low confirmed changes and uncertain observations (PR-016).
4. Markdown and JSON reports are written; the terminal shows their paths (PR-013, PR-014).
5. Sokha reads High findings first, each with a one-line next step and the scan in which it was first seen.

### J-3 Interrupted scan (US-2)
1. Import → tool reports the scan as **incomplete** and explains why.
2. Compare → hosts and ports not observed are listed under **Uncertain observations** with the reason "not covered by an incomplete scan". Nothing is reported as closed or gone.

### J-4 Share a masked report (US-3)
1. Compare with the masking option → identifiers replaced by placeholders (`HOST-01`, `MAC-01`).
2. Report header states clearly that it is masked and lists masking limitations.

### J-5 Bad input (US-5)
1. Import a corrupted, oversized, non-Nmap, or hostile XML file.
2. Tool rejects it with a plain message stating what is wrong and what to do; no traceback; history unchanged (PR-002).

### J-6 Delete a scan (US-6)
1. List scans → choose one → delete.
2. Tool asks for confirmation (unless explicitly told not to), then removes the scan and its data.

## 5. Product Features

Each feature: user story, priority, acceptance criteria (AC), and BR trace. ACs are product-level; the FRD will make them exact.

### Import and validation

**PR-001 — Import a scan** · Must · BR-001, BR-002
*As Sokha, I want to import an Nmap XML file so that it is added to my scan history.*
- AC1: A valid Nmap XML file is stored in history and receives an identifier the user can refer to later.
- AC2: The tool confirms the import and shows: scan identifier, scan start time, number of hosts observed, and completeness status.

**PR-002 — Reject unsafe or invalid input** · Must · BR-006
*As Sokha, I want bad files rejected clearly so that my history is never corrupted.*
- AC1: Files that are not well-formed XML, not Nmap output, larger than 50 MB (NFR-002), or contain unsafe XML constructs (e.g., external entity or entity-expansion attacks) are rejected.
- AC2: Each rejection gives a plain-language reason and a suggested action; no Python traceback is shown by default.
- AC3: After any rejection, history is unchanged.

**PR-003 — Detect duplicate imports** · Should · BR-002, BR-004
*As Sokha, I want to be told if I import the same file twice so that I don't compare a scan with itself.*
- AC1: Importing a file whose content is identical to an already imported scan is refused with a message naming the existing scan.

**PR-004 — Assess scan completeness** · Must · BR-004, BR-005
*As Sokha, I want to know whether a scan finished properly so that I know how much to trust it.*
- AC1: On import, each scan is classified as **complete** or **incomplete**, with the reason when incomplete (e.g., scan did not finish, scan reported an error).
- AC2: The scan's coverage (which targets and ports were scanned) is recorded so comparisons can tell "not seen" from "not looked at".

### History

**PR-005 — List scan history** · Must · BR-002
- AC1: Lists all scans with identifier, import time, scan start time, target summary, host count, and completeness.
- AC2: Ordered from newest to oldest.

**PR-006 — Delete a scan** · Must · BR-002, BR-010, BR-014
*As Sokha, I want to delete scans so that I control how long sensitive data is kept.*
- AC1: A chosen scan and all its stored data are removed.
- AC2: Deletion requires confirmation unless the user explicitly opts out for that command.
- AC3: Later comparisons and first-seen information reflect the remaining history only.

### Comparison

**PR-007 — Choose scans to compare** · Must · BR-002, BR-003
- AC1: With no scans specified, the latest scan is compared with the one immediately before it.
- AC2: The user can specify any two scans by identifier.
- AC3: Comparing fewer than two scans produces an explanatory message, not an error trace.

**PR-008 — Detect changes** · Must · BR-003
- AC1: Detects at least: new host, newly opened port, newly closed port, changed service (product), and changed service version.
- AC2: Every finding is classified as **confirmed** or **uncertain** using the rules in Section 6.

**PR-009 — Separate confirmed changes from uncertain observations** · Must · BR-004, BR-005
- AC1: Uncertain observations never appear among confirmed changes.
- AC2: Each uncertain observation states its reason (e.g., "port not scanned in newer scan", "newer scan incomplete", "port filtered").
- AC3: Uncertain observations are always shown, never silently dropped.

**PR-010 — Rank confirmed changes by importance** · Must · BR-007
- AC1: Each confirmed change is ranked High, Medium, or Low using the documented rules in Section 6.3.
- AC2: Uncertain observations are not ranked.

**PR-011 — First-seen information** · Must · BR-002
*As Sokha, I want to know when something first appeared so that I can tell how long it has been exposed.*
- AC1: For each newly opened port and new host, the report states the earliest scan in history where it was observed.

**PR-012 — Fixed next-step advice** · Must · BR-007
- AC1: Every High and Medium finding includes a one-line suggested next step.
- AC2: Advice text is written in advance for each rule; no online lookups (BR-010).

### Reports

**PR-013 — Markdown report** · Must · BR-007, BR-008
- AC1: Contains the sections listed in Section 7.1, in that order.
- AC2: Readable as plain text, not only when rendered.

**PR-014 — JSON report** · Must · BR-008
- AC1: Contains the same findings as the Markdown report from the same comparison.
- AC2: Includes a schema version field so consumers can detect format changes.

**PR-015 — Masked reports** · Must · BR-009
- AC1–AC6: see Section 7.3.

**PR-016 — Terminal summary** · Should · BR-012
- AC1: After a comparison, the terminal shows counts per importance level, the number of uncertain observations, and the report file paths.

### CLI, data, and documentation

**PR-017 — Help and error messages** · Must · BR-012
- AC1: Each command has help text describing its purpose and options.
- AC2: Every user-facing error states what went wrong and what to do next.

**PR-018 — Local data location** · Must · BR-010, BR-014
- AC1: By default, the database and reports are stored in a per-user folder outside any project repository: `%LOCALAPPDATA%\TestBondanh`.
- AC2: The user can choose a different location.
- AC3: The tool states where data is stored on first use and in help output.

**PR-019 — Warn when writing inside a Git repository** · Should · BR-014
- AC1: If the database or report destination is inside a Git working folder, the tool warns that real scan data could be committed.

**PR-020 — Usage documentation and authorised-use notice** · Must · BR-011, BR-012
- AC1: The README and help output explain the common tasks and state that the tool is intended only for scan results of networks the user owns or is authorised to assess.
- AC2: Documentation explains how to produce a suitable Nmap XML file, without encouraging scanning of others' networks.

## 6. Change Classification and Priority Model

Resolves BRD **OQ-04**. This section defines *product rules*; the FRD maps them to exact Nmap XML fields.

### 6.1 Evidence principle

| Evidence | May produce |
|---|---|
| **Positive** — something was observed (host responded; port open; port actively closed; service identified by probing) | Confirmed change |
| **Absent or weak** — not scanned, scan incomplete, no response, port *filtered*, service guessed only from the port number | Uncertain observation |

### 6.2 Classification rules (baseline = older scan, newer = later scan)

| # | Situation | Result |
|---|---|---|
| C-1 | Host responds in newer scan; baseline covered that address and the host was not observed responding | **Confirmed:** new host |
| C-2 | Host responds in newer scan; baseline did not cover that address | **Uncertain:** first observed (not covered before) |
| C-3 | Host responded in baseline; not observed in newer scan | **Uncertain:** host not observed (reason: not covered / scan incomplete / no response) — including when a complete scan covered it (DEC-017) |
| C-4 | Port open in newer scan; baseline scanned that port on that host and it was not open | **Confirmed:** port opened |
| C-5 | Port open in newer scan; baseline did not scan that port on that host | **Uncertain:** first observed open |
| C-6 | Port open in baseline; newer scan reports it *closed* (an active response) | **Confirmed:** port closed |
| C-7 | Port open in baseline; newer scan reports it *filtered* or ambiguous, or did not scan it, or is incomplete | **Uncertain:** port state unknown |
| C-8 | Same port open in both; service product differs and both were identified by probing | **Confirmed:** service changed |
| C-9 | Same port open in both; same product, version differs, both identified by probing | **Confirmed:** version changed |
| C-10 | Service or version differs but at least one side was only guessed from the port number | **Uncertain:** service identification not reliable |

Rule for incomplete scans (BR-005): an incomplete newer scan may still **confirm additions** it positively observed (C-1, C-4), but anything it did *not* observe is uncertain.

### 6.3 Importance ranking (confirmed changes only)

| Level | Applies to |
|---|---|
| **High** | New host (C-1); port opened (C-4) on a remote-access or file-sharing port — initial list: 22 SSH, 23 Telnet, 445 SMB, 3389 RDP, 5900 VNC (final list fixed in FRD) |
| **Medium** | Port opened (C-4) on any other port; service changed (C-8) |
| **Low** | Version changed (C-9); port closed (C-6) |

Uncertain observations are listed separately and never ranked (DEC-011).

## 7. Report Content

### 7.1 Markdown report — sections in order

1. **Header** — the two scans compared (identifiers, start times), completeness of each, report generation time, and a clear **MASKED** banner when masking is applied.
2. **Summary** — counts of High / Medium / Low confirmed changes and of uncertain observations.
3. **Confirmed changes** — grouped High → Medium → Low; each with host, port/service, what changed, first seen (PR-011), and next step (PR-012, for High and Medium).
4. **Uncertain observations** — each with its reason.
5. **Coverage notes** — differences in what the two scans covered.
6. **Limitations** — fixed text: what the tool cannot know (e.g., a filtered port may be open), and masking limitations when masked.

### 7.2 JSON report

Same findings and metadata as the Markdown report, with a `schema_version` field. Exact schema defined in the FRD.

### 7.3 Masking (resolves BRD OQ-03; DEC-010)

| # | Rule |
|---|---|
| AC1 | IP addresses, hostnames, and MAC addresses are replaced with placeholders: `HOST-01`, `HOST-02`, … and `MAC-01`, … |
| AC2 | Within one comparison run, the same original value always gets the same placeholder, across both Markdown and JSON outputs |
| AC3 | Placeholders are not consistent *between* separate runs, so two shared reports cannot be linked by placeholder |
| AC4 | Port numbers, service names, and versions are kept |
| AC5 | Raw Nmap script output and free-text service details are excluded from masked reports, because they can contain identifiers |
| AC6 | The masked report states that masking is best-effort and lists what was and was not masked |

> **Design tension (noted for TRD/test strategy):** AC3 requires placeholder assignment to vary between runs, while NFR-008 requires reproducible output for testing. Resolution proposed: placeholder assignment uses a random seed per run that tests can fix. Determinism is then defined as "same inputs **and** same seed → same report".

## 8. Scan History Management

Resolves BRD **OQ-05** (DEC-012).

- Scans are kept until the user deletes them (PR-006). No automatic expiry in the MVP.
- Comparisons are computed on demand; reports are output files, not stored history. **(Assumed)**
- Deleting a scan permanently removes its stored data. Report files already written elsewhere are the user's responsibility; the tool says so when deleting.

## 9. Non-Functional Requirements

| ID | Requirement | Priority | Verification | Traces to |
|---|---|---|---|---|
| **NFR-001** | **Performance:** for a scan of up to 256 hosts, import, comparison, and report generation each complete in under 10 seconds on the reference machine (the owner's development laptop; specified in TRD) | Must | Timed test with a generated 256-host fixture | BR-001, BR-003, BR-008 |
| **NFR-002** | **Input size limit:** files larger than 50 MB are rejected before parsing | Must | Test with an oversized fixture | BR-006 |
| **NFR-003** | **Untrusted input:** XML parsing must not resolve external entities, fetch external resources, or expand entities without limit | Must | Hostile fixture suite (XXE, entity expansion) | BR-006 |
| **NFR-004** | **No network activity:** the tool makes no network connections during any operation | Must | Test that fails if a network connection is attempted | BR-010 |
| **NFR-005** | **Atomic import:** an import either fully succeeds or leaves history unchanged | Must | Test interrupting/failing import midway | BR-006 |
| **NFR-006** | **Usability:** no Python tracebacks shown to users by default; every error message states cause and next action | Must | Tests asserting error output format; owner review | BR-012 |
| **NFR-007** | **Platform:** works on Windows 11, including paths containing spaces and non-ASCII characters | Must | Tests using such paths | C-02 |
| **NFR-008** | **Determinism:** same input scans and same masking seed produce identical report content (excluding generation timestamp) | Must | Golden-file (saved expected output) tests | BR-013 |
| **NFR-009** | **Verifiability:** every Must PR and NFR is covered by at least one automated test using synthetic fixtures, or by a documented manual check where automation is not meaningful (e.g., readability) | Must | Traceability matrix | BR-013 |
| **NFR-010** | **Repository hygiene:** the repository contains only synthetic fixtures using documentation-reserved addresses; no databases, reports, real scans, or secrets | Must | Automated pre-push check (defined in harness design) | BR-014 |
| **NFR-011** | **Dependencies:** minimal, free, open-source, MIT-compatible, pinned to exact versions, each justified in the decision log | Must | Dependency review | C-04, DEC-005 |
| **NFR-012** | **Readability:** report meaning never depends on colour or rendering; terminal output is readable without colour | Should | Owner review | BR-007 |

## 10. Release Scope

### MVP (this release)
PR-001 – PR-020 and NFR-001 – NFR-012. "Should" items (PR-003, PR-016, PR-019, NFR-012) may move to the next release if time requires, with owner approval.

### Candidate later releases (not committed)
- Named network profiles (e.g., "home", "office")
- User-configurable list of High-importance ports
- HTML report
- Authorised live scanning — requires a new BRD revision (DEC-006)

## 11. Out of Scope

All items in [BRD §10](BRD.md#10-out-of-scope) apply. Additionally, for the MVP:

| Item | Reason |
|---|---|
| Automatic deletion / retention policies | Manual delete is sufficient (DEC-012) |
| Comparing more than two scans in one report | Two-scan comparison plus first-seen covers the need |
| Including raw Nmap script output in reports | Leak risk and noise |
| Editing or merging scans | Not needed for the core value |

## 12. Constraints, Assumptions, and Dependencies

All BRD constraints (C-01 – C-08), assumptions, and dependencies apply. New items:

| ID | Type | Statement | Status |
|---|---|---|---|
| A-9 | Assumption | Networks are roughly 5–50 devices; 256 hosts is the tested upper bound | Assumed (refines BRD A-8) |
| A-10 | Assumption | Comparisons are computed on demand and not stored in history | Assumed |
| A-11 | Assumption | Users scan with options that include service/version detection when they want service changes reported; without it, service differences are uncertain (C-10) | Assumed |

## 13. Product Success Metrics

| BRD metric | Product evidence |
|---|---|
| SM-01 end-to-end flow | J-2 automated end-to-end test passes |
| SM-02 traceability | Section 16 complete; FRD and tests extend it |
| SM-03 no false confirmed changes | All C-2, C-3, C-5, C-7, C-10 fixtures produce zero confirmed changes |
| SM-04 hostile input | PR-002 and NFR-002/003/005 tests pass |
| SM-05 repo audit | NFR-010 check passes |
| SM-06 masking | PR-015 tests find zero original identifiers |
| SM-07 harness | Defined in AI Harness Design |
| SM-08 approvals | This PRD reaches Approved status by owner decision |

## 14. Open Questions

| ID | Question | Proposed answer | Resolve in |
|---|---|---|---|
| PQ-01 | Should a host that responded before and **did not respond** in a complete newer scan that covered it be a confirmed change ("host not responding") or uncertain? | **Resolved: Uncertain** (owner, 2026-10-27; DEC-017) | — |
| PQ-02 | Exact list of High-importance ports | Start with 22, 23, 445, 3389, 5900; finalise in FRD | FRD |
| PQ-03 | Reference machine specification for NFR-001 | Owner's development laptop; record specs in TRD | TRD |
| OQ-01, OQ-02, OQ-06, OQ-07 | Carried over from BRD (Python version, branch name, Nmap versions, database protection) | — | TRD / before first commit |

## 15. Approval Checklist

Completed: owner approved the PRD on 2026-10-27, choosing "uncertain" for PQ-01.

- [x] Persona and usage scenarios are realistic
- [x] User journeys J-1 – J-6 cover the expected use
- [x] PR-001 – PR-020 are correct, necessary, and correctly prioritised
- [x] Classification rules C-1 – C-10 reflect the "avoid false alarms" principle
- [x] PQ-01 decided (host non-response: uncertain or confirmed)
- [x] Importance ranking (§6.3) is acceptable
- [x] Report content and masking rules (§7) are acceptable, including the seed-based determinism resolution
- [x] NFR-001 – NFR-012 are acceptable and testable
- [x] Every BR is covered in Section 16
- [x] **PRD approved — status may change to "Approved" (version 1.0)**

## 16. Traceability: BR → PR / NFR

| BR | Covered by |
|---|---|
| BR-001 Import Nmap XML | PR-001, NFR-001 |
| BR-002 Scan history | PR-001, PR-003, PR-005, PR-006, PR-007, PR-011 |
| BR-003 Detect meaningful changes | PR-007, PR-008, NFR-001 |
| BR-004 No unsupported change claims | PR-003, PR-004, PR-009, §6 |
| BR-005 Incomplete scans ≠ disappearance | PR-004, PR-009, §6.2 |
| BR-006 Untrusted input handled safely | PR-002, NFR-002, NFR-003, NFR-005 |
| BR-007 Understandable, prioritised reports | PR-010, PR-012, PR-013, NFR-012 |
| BR-008 Markdown and JSON | PR-013, PR-014, NFR-001 |
| BR-009 Masking | PR-015, §7.3 |
| BR-010 Data stays local | PR-006, PR-012, PR-018, NFR-004 |
| BR-011 No scanning | PR-020 |
| BR-012 Clear CLI | PR-016, PR-017, PR-020, NFR-006 |
| BR-013 Demonstrable correctness | NFR-008, NFR-009 |
| BR-014 Repository hygiene | PR-006, PR-018, PR-019, NFR-010 |

All 14 BRs are covered.
