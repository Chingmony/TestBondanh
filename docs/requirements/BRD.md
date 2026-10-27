# TestBondanh — Business Requirements Document (BRD)

| Field | Value |
|---|---|
| Document | Business Requirements Document |
| Project | TestBondanh — Network Security Monitoring Tool |
| Purpose | Define why TestBondanh exists, who it serves, what business outcomes it must achieve, and how success is judged |
| Status | **Approved** — by project owner, 2026-10-27 |
| Version | 1.0 |
| Owner / Approver | Project owner (Chingmony) |
| Author | Claude Code (drafted under owner direction) |
| Last updated | 2026-10-27 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-27 | Claude Code | Initial draft from the approved outline and owner answers (planning batches 1–2) |
| 1.0 | 2026-10-27 | Project owner | Approved as drafted, without changes |

## How to Read This Document

Every statement in this document carries one of these labels:

| Label | Meaning |
|---|---|
| **Confirmed** | Explicitly stated or approved by the owner |
| **Assumed** | Believed true but not yet explicitly confirmed; must be validated |
| **Proposed** | A recommendation awaiting owner decision |
| **Open** | An unresolved question (see Section 16) |

**ID conventions:** `BR-` business requirement · `C-` constraint · `A-` assumption · `SM-` success metric · `R-` risk · `D-` dependency · `OQ-` open question. Decisions referenced as `DEC-` live in [`docs/planning/DECISION-LOG.md`](../planning/DECISION-LOG.md).

**Priority (MoSCoW):** **Must** (MVP fails without it) · **Should** (important, MVP still usable without it) · **Could** (desirable if time allows) · **Won't** (explicitly excluded for this release).

> The BRD states *what the business needs and why*. It deliberately avoids technical design. Product features belong in the PRD, detailed behaviour in the FRD, and technology choices in the TRD/SAD.

---

## 1. Executive Summary

Home-lab and small-office owners often scan their own networks with Nmap but have no simple way to answer the question that matters: **"What changed since last time, and should I worry?"** Comparing raw scan files by hand is slow and error-prone. Worse, a scan that failed or timed out can make it *look* like a device or service disappeared when it did not.

TestBondanh is a local, command-line tool that imports Nmap XML scan results, keeps a history of scans, identifies meaningful changes, and produces plain-language Markdown and JSON reports. Its defining principle is **trustworthiness over sensitivity**: it must not raise false alarms, and it must clearly label anything it cannot confirm.

The project has a second purpose. The owner, an instructor, is using it to evaluate whether a **documentation-first, approval-gated, AI-assisted development workflow** (Claude Code with a verified harness) produces software that is correct, secure, and traceable. The project is therefore considered successful only when both a working, tested MVP **and** a verified AI development harness exist (DEC-008).

Because the repository is public, security is a cross-cutting concern in every decision (Section 9).

## 2. Problem Statement

1. **Change is hard to see.** Two Nmap XML files may each contain hundreds of lines. Spotting a new host, a newly opened port, or a changed service version by eye is unreliable.
2. **Absence is not evidence.** A host missing from a scan may be offline, filtered by a firewall, or simply not reached because the scan was interrupted. Treating "not seen" as "gone" produces false conclusions — either false alarms or false reassurance.
3. **No history.** Without stored history, the user cannot answer "When did this port first appear?"
4. **Raw output is not actionable.** A non-specialist needs to know *what* changed, *how much it matters*, and *what to check next*.
5. **Scan data is sensitive.** Scan results are effectively a map of a network's attack surface. Any tool handling them must avoid leaking that data.

## 3. Business Objectives

| ID | Objective | Status |
|---|---|---|
| OBJ-1 | Let a non-specialist owner see meaningful changes in their own network between scans | Confirmed |
| OBJ-2 | Produce results the user can trust — no false claims of change; uncertainty made explicit | Confirmed |
| OBJ-3 | Handle scan data and untrusted input securely, suitable for a public open-source repository | Confirmed |
| OBJ-4 | Demonstrate, for the owner's evaluation, that an approval-gated AI-assisted workflow can deliver a correct, tested, traceable tool | Confirmed |

> **Note:** OBJ-4 describes *how* the project is built and how it is judged. Per DEC-002 it does not generate business requirements of its own; it is expressed as constraint C-01 and success metric SM-07.

## 4. Stakeholders and Target Users

| Stakeholder | Role | Interest |
|---|---|---|
| **Project owner** (instructor) | Owner, approver, evaluator | Approves every document and change; judges whether the workflow produces trustworthy results |
| **Target user** — home-lab / small-office owner | Primary user persona | Wants to know what changed on their own network and whether to act, without deep security expertise |
| **Public repository visitors** | Readers, potential reusers | May read or reuse the code; must never be exposed to real scan data or secrets |
| **Claude Code** (AI development agent) | Development actor, not a stakeholder | Produces drafts and code under documented requirements and human approval |

### Primary persona (Assumed — refine in PRD)

*"Sokha" runs a home lab or a 5–20 device office network. Comfortable running a command in a terminal and running Nmap with a copied command line. Not a security professional. Scans occasionally (e.g., weekly or after changes). Wants a short report that says: "Here are the changes that matter, here is what to check."*

## 5. Current Situation and Pain Points

| # | Today (without TestBondanh) | Pain |
|---|---|---|
| P-1 | User saves Nmap output and compares files manually, or does not compare at all | Changes are missed; process is tedious, so it is skipped |
| P-2 | Generic text-diff tools compare XML line by line | Noise from timestamps and ordering hides real changes |
| P-3 | An interrupted scan looks like hosts went offline | False alarms or false reassurance |
| P-4 | No record of past scans | Cannot tell when an exposure began |
| P-5 | Sharing raw output to ask for help exposes the network layout | Privacy and security risk |

## 6. Proposed Solution (high level)

A local, single-user command-line tool that:

1. Imports Nmap XML files the user has produced, rejecting malformed or unsafe input safely.
2. Stores each imported scan in a local scan history.
3. Compares scans and classifies findings as **confirmed changes** or **uncertain observations**.
4. Generates human-readable (Markdown) and machine-readable (JSON) reports, prioritised and in plain language, with an option to mask identifying details.

The tool **does not perform network scanning** (C-07). It is developed through an approval-gated, AI-assisted workflow (C-01).

## 7. Business Requirements

Each requirement states a business need. Detailed behaviour is deferred to the PRD/FRD, which must trace back to these IDs.

| ID | Requirement | Priority | Rationale | Acceptance indicator | Source |
|---|---|---|---|---|---|
| **BR-001** | The tool shall accept scan results the user has produced with Nmap, in Nmap XML format. | Must | Nmap is the de-facto free scanner; XML is its structured output | A representative synthetic Nmap XML file is imported successfully | Owner context |
| **BR-002** | The tool shall keep a history of imported scans so that any two scans can be compared and the user can see when an observation first appeared. | Must | Addresses P-4 | After importing several scans, the user can list them and select any two for comparison | Owner context |
| **BR-003** | The tool shall identify meaningful changes between scans, at minimum: new hosts, newly opened ports, newly closed ports, and changed services. | Must | Core value (OBJ-1, P-1, P-2) | Synthetic scan pairs with known differences produce exactly those differences | Owner context |
| **BR-004** | The tool shall not report a host, port, or service as removed or changed unless the scan evidence supports that conclusion. Where evidence is insufficient, the finding shall be reported as **uncertain**, separately from confirmed changes. | Must | False positives are considered worse than false negatives (DEC-003) | Fixtures containing ambiguous evidence produce zero confirmed "removed/changed" findings and the corresponding uncertain findings | Owner answer Q5 |
| **BR-005** | The tool shall not treat a failed, interrupted, or incomplete scan as evidence that a host or service has disappeared. | Must | Addresses P-3; specific case of BR-004 | An incomplete-scan fixture produces no "removed" findings | Owner context |
| **BR-006** | The tool shall treat every input file as untrusted: malformed, incomplete, or malicious files shall be rejected or flagged with a clear message, without crashing, without corrupting stored history, and without exposing the host system. | Must | Security-first public project (OBJ-3) | A suite of malformed and hostile fixtures is handled safely; history is unchanged after each rejection | Owner answer Q5 |
| **BR-007** | Reports shall be understandable by the target persona: changes prioritised by likely importance, written in plain language, with a suggested next step for important changes. | Must | Addresses P-1, P-4; target user is a non-specialist (Q1) | Owner review of sample reports confirms they are readable without Nmap expertise | Owner answer Q1 |
| **BR-008** | The tool shall produce reports in two formats: Markdown for people and JSON for other tools. | Must | Human and automation use | Both formats are produced for the same comparison and contain the same findings | Owner context |
| **BR-009** | The tool shall offer an option to mask identifying details (such as IP addresses and hostnames) in reports so reports can be shared more safely. | Must | Addresses P-5; included in MVP (DEC-007) | A masked report contains no original IPs/hostnames while changes remain understandable | Owner answer Q3 |
| **BR-010** | Scan data shall remain on the user's machine. The tool shall not send scan data, reports, or usage data to any external service. | Must | Scan data is sensitive (A-3, OBJ-3) | No network calls are made by the tool during import, compare, or report | Owner answer Q5 |
| **BR-011** | The tool shall not initiate network scans in this release. | Must | Ethical/legal boundary; avoids misuse (DEC-006) | No scanning capability exists in the MVP | Owner answer, batch 2 Q2 |
| **BR-012** | The tool shall provide a command-line interface that lets the user perform the common tasks (import, list history, compare, report) with clear help and error messages. | Must | Persona is terminal-capable but not expert | Each common task is achievable from documented commands | Owner context |
| **BR-013** | Correctness shall be demonstrable: each Must requirement shall be verified by automated tests using synthetic data, and traceable from requirement to test. | Must | OBJ-2, OBJ-4; trust requires evidence | Traceability matrix shows every Must BR linked to ≥1 passing test | Owner answer batch 2 Q4 |
| **BR-014** | The public repository shall never contain real scan data, generated databases or reports, credentials, or other secrets. | Must | Public repo (Q5); a leaked scan is a network map | Repository audit before each push finds none of these items | Owner answer Q5 |

## 8. Project Scope (MVP)

In scope for the first release:

- Importing Nmap XML files (BR-001, BR-006)
- Local scan history (BR-002)
- Scan comparison with confirmed vs. uncertain findings (BR-003 – BR-005)
- Markdown and JSON reports, prioritised and plain-language, with masking (BR-007 – BR-009)
- CLI for common tasks (BR-012)
- Automated tests with synthetic fixtures, and traceability (BR-013)
- Security and repository hygiene controls (BR-006, BR-010, BR-014)
- The AI development harness needed to build the above (C-01, SM-07)

## 9. Security and Ethical Considerations

Security is a cross-cutting requirement, not a feature (DEC-004). Every later document must state how it addresses the items below.

| # | Concern | Business rule | Related |
|---|---|---|---|
| S-1 | **Real scan data leaking via the public repo** | Only synthetic data is committed. Fixtures use only IETF-reserved documentation ranges: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` (IPv4) and `2001:db8::/32` (IPv6) | BR-014, C-08 |
| S-2 | **Generated files committed by accident** | Databases, reports, and user-imported scans are never tracked in version control | BR-014 |
| S-3 | **Hostile input files** — e.g., *XXE* (XML External Entity: a crafted file that tricks a parser into reading local files or contacting the network) and *billion laughs* (a small file that expands into gigabytes in memory) | All input is untrusted and parsed defensively; specific controls defined in TRD | BR-006 |
| S-4 | **Data leaving the machine** | No telemetry, no external services, no network calls | BR-010 |
| S-5 | **Sharing reports** | Masking option available | BR-009 |
| S-6 | **Secrets** | No credentials or tokens in the repo; checked before push | BR-014 |
| S-7 | **Supply chain** — every third-party library adds attack surface | Minimal, free, well-maintained dependencies, pinned to exact versions; each justified in the decision log | C-04 |
| S-8 | **Misuse against others' networks** | No scanning capability; documentation states the tool is for networks the user owns or is authorised to assess | BR-011 |
| S-9 | **AI-generated code introducing vulnerabilities** | AI output is never assumed correct; security review and tests are part of the harness and human approval is required | C-01 |

## 10. Out of Scope

| Item | Status | Note |
|---|---|---|
| Performing live network scans | **Won't (MVP)** — possible future phase | Would require a new BRD revision limited to explicitly authorised targets (DEC-006) |
| Graphical or web user interface | Won't | CLI only |
| Multiple users, accounts, authentication | Won't | Single local user (A-1) |
| Scanners other than Nmap; Nmap non-XML outputs | Won't | XML only (A-2) |
| Vulnerability assessment / CVE lookup | Won't | Would require external data sources (conflicts with BR-010) |
| Scheduled scanning, continuous monitoring, alerts (email/chat) | Won't | Tool runs on demand |
| Cloud hosting or remote deployment | Won't | Local only |
| Automatic remediation (changing firewall rules, etc.) | Won't | Report only |
| Official support for Linux/macOS | Won't | Developed and verified on Windows 11; may work elsewhere but untested |

## 11. Constraints and Assumptions

### Constraints

| ID | Constraint | Status |
|---|---|---|
| C-01 | All development is performed with Claude Code inside a documented AI harness, under human approval gates. AI output is never assumed correct. The harness design is defined in `docs/harness/AI-HARNESS-DESIGN.md` | Confirmed (DEC-002) |
| C-02 | Developed and run on Windows 11 without a virtual machine | Confirmed |
| C-03 | Initial technology assumptions: Python, SQLite, pytest, Git — to be confirmed in the TRD | Proposed |
| C-04 | Free and open-source tools and dependencies only; no paid services | Confirmed |
| C-05 | Owner capacity is about 1 hour per day; work must be split into tasks completable and verifiable within roughly one session, with no fixed deadline | Confirmed |
| C-06 | Repository is public on GitHub and licensed under MIT | Confirmed (DEC-005) |
| C-07 | No live network scanning during development or testing | Confirmed |
| C-08 | All test data is synthetic, using documentation-reserved address ranges (S-1) | Confirmed |

### Assumptions

| ID | Assumption | Status |
|---|---|---|
| A-1 | One user, running locally; no authentication or multi-user features | Assumed |
| A-2 | Input is Nmap XML only | Assumed |
| A-3 | Real scan data is sensitive and must stay local | **Confirmed** (now constraint-backed by BR-010, BR-014) |
| A-4 | No paid services are needed to meet the requirements | Assumed |
| A-5 | Success means a working, tested MVP plus a verified harness that the owner can evaluate; no external deadline | **Confirmed** (DEC-008) |
| A-6 | The tool never initiates scans in the MVP | **Confirmed** (BR-011) |
| A-7 | Users run Nmap themselves and save results with Nmap's XML output option | Assumed |
| A-8 | Typical networks are small (tens, not thousands, of hosts) | Assumed — affects performance targets in the PRD/TRD |

## 12. Success Metrics and Acceptance Indicators

The project succeeds when **all** of the following are met (DEC-008).

| ID | Metric | Target | Traces to |
|---|---|---|---|
| SM-01 | End-to-end flow works on synthetic data: import two scans → compare → Markdown and JSON reports | Demonstrated by automated test and owner walkthrough | BR-001 – BR-003, BR-008, BR-012 |
| SM-02 | Every **Must** BR is linked through PRD/FRD to at least one passing automated test | 100% of Must BRs | BR-013 |
| SM-03 | No false confirmed changes on the ambiguous/incomplete-scan fixture set | 0 false confirmed "removed/changed" findings | BR-004, BR-005 |
| SM-04 | Hostile and malformed fixtures are handled safely | 100% rejected or flagged; no crash; history unchanged | BR-006 |
| SM-05 | Repository audit before each push | 0 real scan files, databases, reports, or secrets tracked | BR-014 |
| SM-06 | Masked reports contain no original identifiers | 0 original IPs/hostnames in masked output for the fixture set | BR-009 |
| SM-07 | AI harness components exist and each has recorded verification evidence: `CLAUDE.md`, at least one skill, a read-only code-review subagent, at least one verification hook, and a test-and-review loop | All five verified | C-01 |
| SM-08 | Owner can review and approve each document and change at a defined checkpoint | Every document reaches "Approved" status by explicit owner decision | C-01 |

## 13. Risks and Mitigations

Business-level risks. Detailed technical risks will be tracked in `docs/planning/RISKS.md`.

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | AI-generated comparison logic is plausible but wrong, causing false alarms | Medium | High | BR-004/005 tests with adversarial fixtures; independent review subagent; owner approval |
| R-02 | Real scan data or a database is pushed to the public repo | Medium | High | BR-014; ignore rules; pre-push audit check enforced by the harness |
| R-03 | Input parsing vulnerability (XXE, memory exhaustion) | Medium | High | BR-006; defensive parser chosen in TRD; hostile fixture suite |
| R-04 | Scope creep from AI or from enthusiasm (e.g., adding live scanning or CVE lookups) | High | Medium | Out-of-scope table; traceability: no code without a requirement ID |
| R-05 | Nmap XML varies across versions or scan options | Medium | Medium | Fixture set covering variations; unknown elements handled per BR-006 |
| R-06 | Context is lost between 1-hour sessions, causing inconsistent work | High | Medium | Small tasks (C-05); persistent project context in `CLAUDE.md`; decision log |
| R-07 | Tool is misused against networks the user does not own | Low | High | No scanning (BR-011); authorised-use statement in README |
| R-08 | Masking is incomplete and leaks identifiers through hostnames, banners, or service details | Medium | Medium | SM-06 tests include identifiers in unusual fields; scope of masking defined in PRD (OQ-03) |
| R-09 | Development environment inconsistency (two Python versions are installed: 3.11.0 and 3.13.5) | Medium | Medium | Pin one version in TRD (OQ-01) |
| R-10 | Third-party Claude Code plugins inject instructions that conflict with project rules (observed during repository inspection) | Medium | Medium | Instruction precedence and plugin settings defined in the AI Harness Design |

## 14. Dependencies

| ID | Dependency | Note |
|---|---|---|
| D-01 | Nmap XML output format | Publicly documented; the tool depends on its structure, not on Nmap being installed |
| D-02 | Python runtime and standard tooling | Version decided in TRD (OQ-01) |
| D-03 | Git and GitHub | Public repository `Chingmony/TestBondanh` |
| D-04 | Claude Code | Development environment and harness (C-01) |
| D-05 | Owner availability for reviews and approvals | Approval gates are sequential (C-05) |

## 15. Glossary

See Appendix A.

## 16. Open Questions

| ID | Question | Resolve in | Owner |
|---|---|---|---|
| OQ-01 | Which Python version will be the project standard (3.11.0 vs 3.13.5 are both installed)? | TRD | Owner |
| OQ-02 | Default branch name: `master` (current local) or `main`? Decide before first commit | Before first commit | Owner |
| OQ-03 | What exactly does masking cover (IPs, hostnames, MAC addresses, service banners)? Should masked values be consistent pseudonyms (e.g., `HOST-01`) so changes remain readable? | PRD | Owner |
| OQ-04 | How are changes prioritised (e.g., a new remote-access port vs. a version change)? | PRD | Owner |
| OQ-05 | How long is scan history retained, and should the user be able to delete scans? | PRD | Owner |
| OQ-06 | Which range of Nmap versions must be supported? | TRD | Owner |
| OQ-07 | Should the stored database be protected beyond normal Windows account permissions (e.g., encryption at rest)? | TRD | Owner |

## 17. Approval Checklist

Completed: owner approved the BRD as drafted on 2026-10-27.

- [x] Problem statement reflects the real need
- [x] Business objectives OBJ-1 – OBJ-4 are correct and complete
- [x] Target persona is right (or will be refined in PRD)
- [x] BR-001 – BR-014 are correct, necessary, and appropriately prioritised
- [x] Each BR has a credible acceptance indicator
- [x] Out-of-scope list is acceptable
- [x] Constraints and assumptions are correctly labelled
- [x] Security and ethical considerations are sufficient for a public repository
- [x] Success metrics SM-01 – SM-08 define "done" for this project
- [x] Open questions are acceptable to defer to the stated documents
- [x] **BRD approved — status may change to "Approved" (version 1.0)**

---

## Appendix A — Glossary

| Term | Meaning |
|---|---|
| **Nmap** | A free, widely used network scanner that discovers hosts and open ports |
| **Nmap XML** | Nmap's structured output format (produced with the `-oX` option), which the tool imports |
| **Host** | A device with a network address observed in a scan |
| **Port state** | Nmap's classification of a port, e.g., *open*, *closed*, *filtered* (no answer — possibly blocked by a firewall) |
| **Service** | The software Nmap believes is listening on a port, optionally with product and version |
| **Scan history** | The stored collection of imported scans over time |
| **Baseline scan** | The earlier scan in a comparison, used as the reference point |
| **Confirmed change** | A difference between two scans that both scans have enough evidence to support |
| **Uncertain observation** | A possible difference that the evidence cannot confirm, e.g., a host absent from an incomplete scan |
| **Incomplete scan** | A scan that was interrupted, timed out, or did not cover the same targets/ports as the baseline |
| **False positive** | Reporting a change that did not happen (treated as the more serious error in this project) |
| **False negative** | Failing to report a change that did happen |
| **Masking** | Replacing identifying details in a report with placeholders so it can be shared more safely |
| **Synthetic fixture** | A hand-made test input file with known contents, containing no real network data |
| **Documentation address ranges** | IP ranges reserved by the IETF for examples (RFC 5737, RFC 3849); they never belong to real networks |
| **XXE** | XML External Entity attack — a crafted XML file that makes a parser read local files or make network requests |
| **Billion laughs** | An XML attack where nested entity definitions expand a tiny file into enormous memory use |
| **AI harness** | The configuration around an AI coding agent — instructions, skills, subagents, hooks, permissions — that keeps its work consistent, verified, and safe |
| **MVP** | Minimum Viable Product — the smallest release that delivers the core value |
| **MoSCoW** | Prioritisation scheme: Must, Should, Could, Won't |
