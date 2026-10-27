# TestBondanh — Functional Requirements Document (FRD)

| Field | Value |
|---|---|
| Document | Functional Requirements Document |
| Project | TestBondanh — Network Security Monitoring Tool |
| Purpose | Specify exactly how the system behaves — commands, inputs, outputs, rules, and errors — precisely enough to implement and test without further product decisions |
| Status | **Approved** — by project owner, 2026-10-27 |
| Version | 1.0 |
| Based on | [BRD v1.0](BRD.md), [PRD v1.0](PRD.md) (both Approved) |
| Owner / Approver | Project owner (Chingmony) |
| Author | Claude Code (drafted under owner direction) |
| Last updated | 2026-10-27 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-27 | Claude Code | Initial draft from approved outline and owner answers (FRD batch 1) |
| 1.0 | 2026-10-27 | Project owner | Approved as drafted; FQ-01 – FQ-05 resolved as proposed (DEC-023) |

---

## 1. Purpose and Relationship to the PRD

The PRD defines *what* the user gets. This FRD defines *how the system behaves* in every case the MVP handles. Each FR traces to one or more PRs/NFRs (Section 16). Technology choices — language libraries, storage layout, module structure — are **not** decided here; they belong in the TRD and SAD.

**Source verification:** Nmap XML element and attribute names in Section 8 were checked against the official Nmap XML DTD (<https://nmap.org/book/nmap-dtd.html>) and port-state definitions against the Nmap reference guide (<https://nmap.org/book/man-port-scanning-basics.html>) on 2026-10-27.

This FRD resolves BRD **OQ-06** (supported Nmap versions → FR-025) and PRD **PQ-02** (High-importance ports → FR-071).

## 2. Conventions

- **"shall"** = mandatory. **"should"** = recommended, not required for acceptance.
- Each FR has: ID, statement, priority (from the PR it implements), trace, and acceptance criteria (AC).
- ACs use **Given / When / Then**. Each AC is intended to become at least one automated test unless marked *(manual)*.
- Error references (`E-…`) point to the catalogue in Section 15.
- Example addresses use only documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`).
- Labels **Confirmed / Assumed / Proposed / Open** as in the BRD.

## 3. Terms Introduced in This Document

| Term | Meaning |
|---|---|
| **Scan ID** | Positive integer assigned at import: 1, 2, 3, … Never reused after deletion |
| **Baseline / newer** | In a comparison, the scan with the earlier start time / the later start time |
| **Coverage** | What a scan looked at: which addresses (address coverage) and which ports per protocol (port coverage) |
| **Port key** | The pair (protocol, port number), e.g. (tcp, 445). TCP 53 and UDP 53 are different ports |
| **State group** | Grouping of Nmap port states used by the rules in Section 10 (FR-055) |
| **Finding** | One item in a report: either a confirmed change or an uncertain observation |
| **Reason code** | A fixed machine-readable string explaining why a finding is uncertain |
| **Mask seed** | A number that determines placeholder assignment in a masked report |

## 4. System Context

```
          Nmap XML file (user-produced, untrusted)
                        │
                        ▼
  User ──► testbondanh CLI ──► Data folder (database + reports/)
                        │           default: %LOCALAPPDATA%\TestBondanh
                        ▼
          stdout: results    stderr: warnings and errors
```

- **Actor:** one local user (BRD A-1).
- **Inputs:** Nmap XML files; command-line arguments; one environment variable (`TESTBONDANH_DATA_DIR`).
- **Outputs:** stored scan history; Markdown and JSON report files; terminal text; exit code.
- **FR-095 — No network activity** · Must · NFR-004, BR-010
  The system shall not open any network connection during any command.
  - AC1: Given network access is blocked in the test environment such that any connection attempt raises an error, When every command is run against fixtures, Then all commands complete normally.

## 5. CLI Specification

### FR-001 — Command structure · Must · PR-017, BR-012

The system shall provide one command, `testbondanh`, with these sub-commands:

| Sub-command | Arguments and options | Purpose |
|---|---|---|
| `import` | `FILE` | Import one Nmap XML file (Section 7) |
| `list` | — | List scan history (FR-040) |
| `compare` | `[BASELINE_ID NEWER_ID]` `[--mask]` `[--mask-seed N]` `[--output DIR]` | Compare two scans and write reports (Sections 10–13) |
| `delete` | `SCAN_ID` `[--yes]` | Delete a scan (FR-041) |

- AC1: Given no sub-command, When `testbondanh` runs, Then usage help is printed to stderr and exit code is `2`.
- AC2: Given an unknown sub-command or invalid option, When run, Then a usage error is printed and exit code is `2`.

### FR-002 — Global options · Must · PR-017, PR-018

| Option | Effect |
|---|---|
| `--data-dir PATH` | Use `PATH` as the data folder (FR-010) |
| `--debug` | Show full internal error details, including tracebacks (FR-005) |
| `--help` | Show help for the command or sub-command; exit `0` |
| `--version` | Print the tool version; exit `0` |

- AC1: Given `--help` on any sub-command, Then the output states the sub-command's purpose and each of its options, and exit code is `0`.

### FR-003 — Exit codes · Must · PR-017, NFR-006

| Code | Meaning |
|---|---|
| `0` | Success (including comparisons that find High changes) |
| `1` | Input or data problem: invalid file, unknown scan ID, not enough scans, write failure |
| `2` | Command-line usage error |
| `3` | Unexpected internal error |

- AC1: Each error in Section 15 returns the code listed there.
- AC2: Given a comparison producing High findings, Then exit code is `0`.

### FR-004 — Output streams · Must · NFR-006

- Normal results (import confirmation, history list, comparison summary) shall go to **stdout**.
- Warnings and errors shall go to **stderr**, prefixed `Warning:` or `Error [E-…]:`.
- Output shall not rely on colour (NFR-012).

### FR-005 — No tracebacks by default · Must · NFR-006

- AC1: Given an unexpected internal error, When run without `--debug`, Then stderr shows `Error [E-INT-001]` with a one-line description and the hint "re-run with --debug for details", no traceback, and exit code `3`.
- AC2: Given the same error with `--debug`, Then the traceback is also printed to stderr.

### FR-006 — Authorised-use notice · Must · PR-020, BR-011

- AC1: Given `testbondanh --help`, Then the output includes: "Use only with scan results from networks you own or are authorised to assess."

## 6. Logical Data Model

Logical entities only; storage design belongs to the TRD. Raw XML files are **not** stored.

| Entity | Fields |
|---|---|
| **Scan** | scan_id; imported_at; source_file_name (name only, no folder path); content_sha256; nmap_version; nmap_args; start_time; end_time; completeness (`complete` \| `incomplete`); incompleteness_reasons (list); port_coverage (protocol → set of ports); address_coverage (set of addresses/ranges, plus `coverage_known` flag) |
| **Host** | scan_id; address (normalised); address_type (`ipv4` \| `ipv6`); mac_address (optional); mac_vendor (optional); hostnames (list); status (`up` \| `down` \| `unknown` \| `skipped`); timed_out (bool) |
| **Port** | scan_id; host address; protocol (`tcp` \| `udp` \| `sctp` \| `ip`); port_number; state (Nmap state string) |
| **Service** | port reference; name; product (optional); version (optional); extrainfo (optional); tunnel (optional); method (`probed` \| `table`); confidence (0–10) |
| **ExtraPorts** | scan_id; host address; state; count — used to infer the state of unlisted scanned ports (FR-055) |

**Address normalisation:** IPv4 in dotted-decimal; IPv6 in lowercase compressed form (e.g., `2001:db8::1`). Hosts are identified by normalised address (FR-052).

## 7. Import and Validation

Import shall perform the checks below **in order**, stopping at the first failure.

### FR-020 — File access · Must · PR-002
- AC1: Given a path that does not exist, Then `E-IMP-001`.
- AC2: Given a path that exists but cannot be read, Then `E-IMP-002`.

### FR-021 — Size limit · Must · NFR-002
The file size shall be checked **before** parsing.
- AC1: Given a file larger than 52,428,800 bytes (50 MB), Then `E-IMP-003` and the file is not parsed.

### FR-022 — Safe parsing · Must · NFR-003, BR-006
The parser shall:
1. never retrieve external resources (no external DTDs, no external entities);
2. reject any document whose DOCTYPE declares entities (`<!ENTITY`);
3. never expand entity references beyond the five predefined XML entities.

A plain `<!DOCTYPE nmaprun>` and the `<?xml-stylesheet …?>` instruction that Nmap writes shall be accepted.
- AC1: Given an XXE fixture (an entity referencing a local file), Then `E-IMP-005` and no file content appears in any output.
- AC2: Given an entity-expansion ("billion laughs") fixture, Then `E-IMP-005` within 2 seconds and without significant memory growth.
- AC3: Given a genuine-format Nmap XML fixture with `<!DOCTYPE nmaprun>` and a stylesheet instruction, Then import succeeds.

### FR-023 — Well-formed XML · Must · PR-002
- AC1: Given a file that is not well-formed XML, Then `E-IMP-004`.
- AC2: Given a file truncated mid-document (e.g., an interrupted scan whose output was cut off), Then `E-IMP-004`, with the message noting the scan may have been interrupted, and nothing is imported. *(Truncated files are rejected, not partially imported — see FQ-02.)*

### FR-024 — Nmap identification · Must · PR-002
- AC1: Given a well-formed XML file whose root element is not `nmaprun`, or whose `scanner` attribute is not `nmap`, Then `E-IMP-006`.

### FR-025 — Supported Nmap versions · Must · PR-002 (resolves BRD OQ-06)
The `nmaprun@version` attribute shall be read. Major version **7 or later** is supported.
- AC1: Given version `7.94`, Then import proceeds.
- AC2: Given version `6.47` or an unparseable version, Then `E-IMP-007`.
- AC3: `xmloutputversion` is recorded but not checked.

### FR-026 — Duplicate detection · Should · PR-003
The SHA-256 hash of the file's bytes shall be compared with stored scans.
- AC1: Given a file byte-identical to an imported scan, Then `E-IMP-008`, naming the existing scan ID.

### FR-027 — Required data · Must · PR-001
- AC1: Given an `nmaprun` without a numeric `start` attribute, or without `runstats/finished`, Then `E-IMP-009` naming the missing item.
- AC2: Given a `host` element without an `address` of type `ipv4` or `ipv6`, Then that host is skipped and a warning is printed; import continues.

### FR-028 — Completeness assessment · Must · PR-004, BR-005
A scan shall be marked **incomplete** if any of the following holds; each true condition is recorded as a reason:

| Condition | Reason code |
|---|---|
| `runstats/finished@exit` = `error` | `scan_reported_error` |
| `runstats/finished@errormsg` present and non-empty | `scan_reported_error` |
| Any `host@timedout` = `true` | `host_timed_out` |

Otherwise the scan is **complete**. A missing `exit` attribute (it is optional in the DTD) does not by itself make a scan incomplete.

Hosts with `timedout="true"` are additionally marked individually (FR-067).
- AC1: Given a fixture with `exit="error"`, Then completeness is `incomplete` with reason `scan_reported_error`.
- AC2: Given a fixture where one host has `timedout="true"`, Then completeness is `incomplete` with reason `host_timed_out` and that host is flagged.

### FR-029 — Port coverage · Must · PR-004
Port coverage shall be taken from each `scaninfo` element: `protocol` → the port list in `services` (e.g., `"1-1000,8080"`), expanded to a set of port numbers.
- AC1: Given `<scaninfo protocol="tcp" services="22,80,100-102"/>`, Then TCP coverage is {22, 80, 100, 101, 102}.
- AC2: Given no `scaninfo` for UDP, Then no UDP ports are covered.

### FR-030 — Address coverage · Must · PR-004
Address coverage shall be the union of:
1. every address appearing in a `host` element of any status except `skipped`; and
2. targets parsed from `nmaprun@args`: tokens that match an IPv4 address, IPv4 CIDR block, IPv4 octet range (e.g., `192.0.2.1-50`), IPv6 address, or IPv6 CIDR block.

`coverage_known` shall be **false** (address coverage limited to item 1 only) if `args` contains any of: `-iL`, `-iR`, `--exclude`, `--excludefile`, `-S`, `-D`, `--proxies`, or any non-option token that is a hostname rather than an address. *(Heuristic — see FQ-03.)*
- AC1: Given args `nmap -sV -oX out.xml 192.0.2.0/24`, Then coverage includes all 256 addresses of `192.0.2.0/24` and `coverage_known` is true.
- AC2: Given args containing `--exclude 192.0.2.5`, Then `coverage_known` is false.
- AC3: Given args containing `-p 22,80`, Then `22,80` is not mistaken for a target.

### FR-031 — Atomic import · Must · NFR-005
- AC1: Given a failure at any point during import (including a simulated storage failure after some data is written), Then history is identical to its state before the import.

### FR-032 — Import confirmation · Must · PR-001, PR-004
On success, stdout shall show: scan ID; start time; hosts observed `up`; completeness and, if incomplete, each reason in plain language.
- AC1: Given a valid complete fixture, Then output contains the new scan ID, start time, up-host count, and "complete".

### FR-033 — Unknown content ignored · Must · PR-002
Elements and attributes not used by this FRD (e.g., `os`, `trace`, `script`, `hostscript`, `times`) shall be ignored, not rejected.
- AC1: Given a fixture containing OS detection and script output, Then import succeeds and those elements are not stored.

## 8. Nmap XML Mapping

| Nmap XML (DTD) | Used for | FR |
|---|---|---|
| `nmaprun@scanner`, `@version` | Identification, version check | FR-024, FR-025 |
| `nmaprun@args` | Address coverage; recorded | FR-030 |
| `nmaprun@start` | Scan start time; baseline ordering | FR-027, FR-051 |
| `scaninfo@protocol`, `@services` | Port coverage | FR-029 |
| `host@timedout` | Completeness, per-host incompleteness | FR-028, FR-067 |
| `host/status@state` (`up`\|`down`\|`unknown`\|`skipped`) | Host observed responding (only `up` counts) | FR-056 – FR-058 |
| `host/address@addr`, `@addrtype` (`ipv4`\|`ipv6`\|`mac`), `@vendor` | Host identity; MAC note | FR-052, FR-053 |
| `host/hostnames/hostname@name` | Display; masking | FR-082, FR-090 |
| `host/ports/port@protocol`, `@portid` | Port key | FR-054 |
| `port/state@state` | Port state | FR-055 |
| `ports/extraports@state`, `@count` | State of unlisted scanned ports | FR-055 |
| `port/service@name`, `@product`, `@version`, `@extrainfo`, `@tunnel`, `@method` (`table`\|`probed`), `@conf` | Service comparison | FR-062 – FR-064 |
| `runstats/finished@exit` (`success`\|`error`), `@errormsg`, `@time` | Completeness; end time | FR-027, FR-028 |
| All other elements | Ignored | FR-033 |

## 9. History

### FR-040 — List scans · Must · PR-005
`list` shall print one row per scan, newest start time first, with: scan ID, start time, imported time, target summary (first target token from args, plus "+N more" if several), up-host count, completeness.
- AC1: Given three imported scans, Then three rows appear ordered by start time descending.
- AC2: Given no scans, Then the message "No scans imported yet" and exit `0`.

### FR-041 — Delete a scan · Must · PR-006
- AC1: Given an existing scan ID and confirmation, Then the scan and all its hosts, ports, and services are removed and the output states that report files already written are not deleted.
- AC2: Given an unknown scan ID, Then `E-HIS-001`.
- AC3: Given a scan is deleted, Then later `list`, `compare`, and first-seen results (FR-068) ignore it.

### FR-042 — Delete confirmation · Must · PR-006
- AC1: Given `delete 3` without `--yes`, Then the tool shows the scan summary and asks `Delete scan 3? [y/N]`; any answer other than `y`/`yes` (case-insensitive) cancels with exit `0`.
- AC2: Given `delete 3 --yes`, Then no prompt is shown.
- AC3: Given input is not interactive and `--yes` is absent, Then the deletion is cancelled with a message explaining `--yes`.

## 10. Comparison

### FR-050 — Scan selection · Must · PR-007
- AC1: Given no IDs, Then the two scans with the latest start times are compared.
- AC2: Given two IDs, Then those scans are compared.
- AC3: Given fewer than two scans in history, Then `E-CMP-001`.
- AC4: Given the same ID twice, Then `E-CMP-002`.
- AC5: Given exactly one ID, Then usage error (exit `2`).
- AC6: Given an unknown ID, Then `E-HIS-001`.

### FR-051 — Baseline ordering · Must · PR-007
The scan with the earlier start time shall be the baseline, regardless of argument order (ties: lower scan ID is baseline). The report header states which is which.
- AC1: Given `compare 5 2` where scan 2 started earlier, Then scan 2 is the baseline.

### FR-052 — Host identity · Must · PR-008 (DEC-018)
Hosts in two scans are the same host if and only if their normalised addresses are equal.
- AC1: Given `2001:DB8::1` in one scan and `2001:db8::1` in the other, Then they are the same host.

### FR-053 — Same-MAC note · Must · PR-008 (DEC-018)
If a finding concerns address A, and both scans record a MAC address, and A's MAC in one scan equals the MAC of a different address B in the other scan, the finding shall carry the note `possibly_same_device` referencing B. Classification is not changed.
- AC1: Given MAC `00:00:5E:00:53:01` at `192.0.2.10` in the baseline and at `192.0.2.20` in the newer scan, Then the new-host finding for `.20` and the host-not-observed finding for `.10` each reference the other address.

### FR-054 — Port identity · Must · PR-008
Ports are the same if their port keys (protocol, port number) are equal on the same host.

### FR-055 — State groups · Must · PR-008, PR-009
For a host and port key, the effective state in a scan is determined as follows:

1. If the port is listed in `port` elements → its `state@state`.
2. Else, if the port is in the scan's port coverage for that protocol and the host has **exactly one** `extraports` element → that element's state.
3. Else, if the port is in port coverage → `undetermined`.
4. Else → `not_scanned`.

States are grouped:

| Group | Nmap states | Meaning |
|---|---|---|
| `OPEN` | `open` | Positively observed open |
| `CLOSED` | `closed` | Positively observed closed (active response) |
| `NOT_OPEN` | `closed`, `closed\|filtered` | Certainly not open |
| `UNDETERMINED` | `filtered`, `unfiltered`, `open\|filtered`, `undetermined`, any unrecognised state | Could have been open |
| `NOT_SCANNED` | `not_scanned` | Not looked at |

(`CLOSED` is a subset of `NOT_OPEN`.)

### Classification rules

These FRs implement PRD §6.2 rules C-1 – C-10 and DEC-017. "Responding" means `status@state="up"`. A host is **evaluable** in a scan if the scan is complete and the host is not timed out.

| FR | PRD rule | Condition | Finding | Status | Reason code |
|---|---|---|---|---|---|
| **FR-056** | C-1 | Host responding in newer; baseline `coverage_known` and address in baseline coverage; not responding in baseline; baseline complete | `new_host` | confirmed | — |
| **FR-057** | C-2 | Host responding in newer; baseline coverage unknown or address not in it, or baseline incomplete | `host_first_observed` | uncertain | `not_covered_before` / `baseline_incomplete` |
| **FR-058** | C-3 | Host responding in baseline; not responding (or absent) in newer — in all cases, including a complete newer scan that covered it (DEC-017) | `host_not_observed` | uncertain | `no_response` / `not_covered` / `newer_scan_incomplete` |
| **FR-059** | C-4 | Host responding in both; port `OPEN` in newer; baseline group `NOT_OPEN`; host evaluable in baseline | `port_opened` | confirmed | — |
| **FR-060** | C-5 / C-4 strict | Port `OPEN` in newer; baseline `NOT_SCANNED`, `UNDETERMINED`, or host not evaluable in baseline | `port_first_observed_open` | uncertain | `not_scanned_before` / `previous_state_undetermined` / `baseline_incomplete` |
| **FR-061** | C-6 | Port `OPEN` in baseline; `CLOSED` in newer; host evaluable in newer | `port_closed` | confirmed | — |
| **FR-062** | C-7 | Port `OPEN` in baseline; newer `UNDETERMINED`, `closed\|filtered`, `NOT_SCANNED`, or host not evaluable in newer | `port_state_unknown` | uncertain | `port_filtered_or_ambiguous` / `not_scanned` / `newer_scan_incomplete` |
| **FR-063** | C-8 | Port `OPEN` in both; both services `method="probed"`; (name, product, tunnel) differ | `service_changed` | confirmed | — |
| **FR-064** | C-9 | Port `OPEN` in both; both `probed`; same (name, product, tunnel); version differs (including present vs. absent) | `version_changed` | confirmed | — |
| **FR-065** | C-10 | Port `OPEN` in both; service name, product, tunnel, or version differs; at least one side `method="table"` or service missing | `service_identification_unreliable` | uncertain | `service_guessed` |

Additional rules:

- **FR-066 — New host's ports.** For a `new_host` or `host_first_observed` finding, the host's `OPEN` ports shall be listed inside that finding, not as separate port findings. · Must · PR-008
- **FR-067 — Timed-out hosts.** A host with `timedout="true"` is not evaluable; absence-based conclusions about it are uncertain with reason `host_timed_out`. Positive observations in that host (e.g., an `OPEN` port) may still appear in FR-059 if the *baseline* side is evaluable. · Must · PR-004, BR-005
- **FR-068 — First seen.** For `new_host`, `host_first_observed`, `port_opened`, and `port_first_observed_open`, the finding shall include the ID and start time of the earliest scan in history (up to and including the newer scan) in which that host was responding / that port was `OPEN` on that host. · Must · PR-011
- **FR-069 — Uncertain findings always reported.** Every uncertain finding produced by the rules shall appear in the report. · Must · PR-009

Acceptance criteria for Section 10 (each becomes a fixture pair):

- AC-C1: Baseline complete, `coverage_known`, covers `192.0.2.0/24`, no host `.30`; newer has `.30` up → one confirmed `new_host`.
- AC-C2: Same, but baseline args use `-iL targets.txt` → `host_first_observed`, uncertain, reason `not_covered_before`.
- AC-C3: `.10` up in baseline; complete newer scan covering it has no `.10` → uncertain `host_not_observed`, reason `no_response`; zero confirmed findings.
- AC-C4: Newer scan `exit="error"` lists 1 of 3 baseline hosts → 2 uncertain `host_not_observed`, reason `newer_scan_incomplete`; zero confirmed removals.
- AC-C5: TCP 3389 `closed` in baseline, `open` in newer → confirmed `port_opened`, importance High.
- AC-C6: TCP 3389 `filtered` in baseline, `open` in newer → uncertain `port_first_observed_open`, reason `previous_state_undetermined`.
- AC-C7: TCP 445 `open` in baseline, `filtered` in newer → uncertain `port_state_unknown`; no confirmed finding.
- AC-C8: TCP 445 `open` → `closed` → confirmed `port_closed`, Low.
- AC-C9: TCP 80 both open, both probed, product changes → confirmed `service_changed`, Medium.
- AC-C10: TCP 22 both open, both probed, same product, version `8.9` → `9.6` → confirmed `version_changed`, Low.
- AC-C11: TCP 8080 both open, newer service `method="table"` with different name → uncertain `service_identification_unreliable`.
- AC-C12: Two identical scans (different files) → zero findings.

## 11. Ranking and Advice

### FR-070 — Importance levels · Must · PR-010
| Finding | Importance |
|---|---|
| `new_host` | High |
| `port_opened` on a High-importance port (FR-071) | High |
| `port_opened` on any other port | Medium |
| `service_changed` | Medium |
| `version_changed` | Low |
| `port_closed` | Low |
| Any uncertain finding | none (not ranked) |

### FR-071 — High-importance ports · Must · PR-010 (resolves PRD PQ-02)
TCP 22 (SSH), 23 (Telnet), 445 (SMB), 3389 (RDP), 5900 (VNC). Fixed in the MVP; not user-configurable. *(See FQ-05.)*

### FR-072 — Advice catalogue · Must · PR-012
Each High and Medium finding shall carry exactly the advice text below:

| Finding | Advice |
|---|---|
| `new_host` | Identify this device. If you do not recognise it, check your router's list of connected devices and remove it if unknown. |
| `port_opened` TCP 22 | Confirm SSH should be reachable on this device; if not, disable the SSH server or block TCP 22. |
| `port_opened` TCP 23 | Telnet sends passwords unencrypted; disable it and use SSH instead. |
| `port_opened` TCP 445 | Confirm file sharing (SMB) is intended on this device; if not, disable it or block TCP 445. |
| `port_opened` TCP 3389 | Confirm Remote Desktop should be reachable; if not, disable it or block TCP 3389. |
| `port_opened` TCP 5900 | Confirm remote screen sharing (VNC) is intended; if not, disable it or block TCP 5900. |
| `port_opened` (other) | Identify which program opened this port and confirm it should be reachable from the network. |
| `service_changed` | Confirm the software now answering on this port is expected, for example after an update or reconfiguration. |

- AC1: Every High and Medium finding in every fixture report has non-empty advice from this table; Low and uncertain findings have none.

## 12. Reports

### FR-080 — File naming and no overwrite · Must · PR-013, PR-014
Reports shall be named `compare-<BASELINE_ID>-<NEWER_ID>-<YYYYMMDD-HHMMSS>[-masked].md` and `.json` (local time of generation).
- AC1: If a file with the target name exists, a suffix `-2`, `-3`, … is added; existing files are never overwritten.

### FR-081 — Output folder · Must · PR-018
Default: `<data folder>\reports`, created if missing. `--output DIR` overrides it.
- AC1: Given an output folder that cannot be created or written, Then `E-RPT-001` and no partial report files remain.

### FR-082 — Markdown structure · Must · PR-013
Sections in this order (PRD §7.1):

```markdown
# TestBondanh Comparison Report            (+ "— MASKED" when masked)
## Scans Compared        baseline/newer: ID, start time, completeness (+ reasons)
## Summary               counts: High, Medium, Low, Uncertain
## Confirmed Changes
### High / ### Medium / ### Low     one entry per finding:
                         host, port/protocol, before → after, first seen, advice
## Uncertain Observations   one entry per finding: host, port, observation, reason (plain language)
## Coverage Notes        differences in port/address coverage between the scans
## Limitations           fixed text (FR-087)
```
Empty sections show "None." rather than being omitted.
- AC1: Every fixture report contains all section headings in order.
- AC2: Each reason code is rendered as a fixed plain-language sentence (e.g., `no_response` → "The host did not respond. It may be off, asleep, or blocking scans.").

### FR-083 — JSON structure · Must · PR-014
```json
{
  "schema_version": "1.0",
  "generated_at": "<ISO 8601 with offset>",
  "masked": false,
  "baseline": { "scan_id": 1, "start_time": "…", "completeness": "complete", "incompleteness_reasons": [] },
  "newer":    { "scan_id": 2, "start_time": "…", "completeness": "incomplete", "incompleteness_reasons": ["scan_reported_error"] },
  "summary":  { "high": 1, "medium": 0, "low": 0, "uncertain": 2 },
  "findings": [
    {
      "kind": "port_opened",
      "status": "confirmed",
      "importance": "high",
      "host": "192.0.2.10",
      "protocol": "tcp",
      "port": 3389,
      "before": { "state": "closed", "service": null },
      "after":  { "state": "open", "service": { "name": "ms-wbt-server", "product": null, "version": null } },
      "reason_code": null,
      "first_seen": { "scan_id": 2, "start_time": "…" },
      "advice": "Confirm Remote Desktop should be reachable; …",
      "notes": []
    }
  ],
  "coverage_notes": [],
  "limitations": ["…"]
}
```
- AC1: JSON output parses as valid JSON and contains every key above.
- AC2: `importance` is `null` for uncertain findings; `reason_code` is `null` for confirmed findings.

### FR-084 — Same findings in both formats · Must · PR-014
- AC1: For every fixture comparison, the set of (kind, status, host, protocol, port) in Markdown equals that in JSON.

### FR-085 — Deterministic ordering · Must · NFR-008
Findings shall be ordered: confirmed before uncertain; importance High → Medium → Low; then address (IPv4 numerically, then IPv6 numerically); then protocol; then port number.
- AC1: Given the same inputs and mask seed, two runs produce byte-identical reports except for `generated_at` and the generated-time line.

### FR-086 — Terminal summary · Should · PR-016
After `compare`, stdout shows the four counts and both report paths.

### FR-087 — Limitations text · Must · PR-013
The Limitations section shall always include:
1. A `filtered` port may be open behind a firewall.
2. Hosts are identified by IP address; a device that changes address may appear as one new host plus one host not observed.
3. Service changes are confirmed only when Nmap probed the service.
4. Results describe only what the two scans observed.

When masked, it shall also include the masking statement (FR-093).

### FR-088 — Excluded content · Must · PR-015, PRD §11
Reports shall not include Nmap script output, OS detection, or traceroute data. `extrainfo` may appear in unmasked reports only.

## 13. Masking

### FR-090 — Masked fields · Must · PR-015, BR-009
With `--mask`, the following shall not appear in either report: IP addresses, hostnames, MAC addresses, MAC vendors, `nmap_args`, source file names, address coverage ranges, and service `extrainfo`.

### FR-091 — Placeholders · Must · PR-015 (DEC-010)
- Each distinct host address in the report gets `HOST-NN`; each distinct MAC gets `MAC-NN` (two digits minimum, more if needed).
- Hostnames are replaced by the host's placeholder; vendors are omitted.
- Address coverage is shown as counts only (e.g., "256 addresses").
- AC1: Within one run, the same address has the same placeholder in Markdown and JSON.

### FR-092 — Mask seed · Must · NFR-008 (resolves PRD §7.3 design tension)
Placeholder numbers are assigned by a random permutation driven by a seed. By default the seed comes from a cryptographically secure random source; `--mask-seed N` fixes it (documented as intended for testing).
- AC1: Same inputs and same `--mask-seed` → identical masked reports (except generation time).
- AC2: Two runs without `--mask-seed` on a fixture with ≥ 5 hosts → placeholder assignments differ (allowing for a negligible chance of collision; test retries once).

### FR-093 — Masked report labelling · Must · PR-015
- AC1: Masked Markdown title ends with "— MASKED"; JSON has `"masked": true`.
- AC2: Limitations states: "Masking is best-effort. IP addresses, hostnames, MAC addresses, vendors, scan arguments, and file names were removed. Port numbers, service names, products, and versions were kept and may still identify devices."

### FR-094 — Leak check (fail closed) · Must · PR-015, BR-009
Before writing masked reports, the system shall search the full report text for every original address (IPv4, and IPv6 in compressed and expanded forms), hostname, and MAC address from both scans. If any is found, no report is written and `E-RPT-002` is raised.
- AC1: Given a fixture where a service `product` field contains a host's IP address, Then the masked report either replaces it or the comparison fails with `E-RPT-002`; in no case is the address written to disk.

## 14. Data Location and Safety

### FR-010 — Data folder resolution · Must · PR-018
Order of precedence: `--data-dir` → environment variable `TESTBONDANH_DATA_DIR` → `%LOCALAPPDATA%\TestBondanh`.
- AC1: Given both `--data-dir` and the environment variable, Then `--data-dir` wins.
- AC2: Given neither and `LOCALAPPDATA` is unset, Then `E-DAT-002`.
- AC3: Paths containing spaces and non-ASCII characters work (NFR-007).

### FR-011 — First use · Must · PR-018
- AC1: Given the data folder does not exist, When any command needing it runs, Then it is created and stdout states its location once.
- AC2: Given it cannot be created or written, Then `E-DAT-001`.

### FR-012 — Git repository warning · Should · PR-019
Before writing the database or reports, the system shall check whether the destination folder or any parent folder contains a `.git` entry (folder or file). If so, it shall print to stderr: `Warning: <path> is inside a Git repository. Real scan data could be committed by mistake.` and continue.
- AC1: Given `--data-dir` inside a folder with `.git`, Then the warning appears.

## 15. Error Catalogue

All errors print `Error [<ID>]: <message>` to stderr, followed by `Next step: <action>`.

| ID | Condition | Message (summary) | Next step | Exit |
|---|---|---|---|---|
| E-IMP-001 | File not found | File not found: `<path>` | Check the path | 1 |
| E-IMP-002 | File not readable | Cannot read file | Check permissions | 1 |
| E-IMP-003 | File > 50 MB | File exceeds 50 MB limit | Split the scan into smaller target ranges | 1 |
| E-IMP-004 | Not well-formed / truncated | File is not valid XML (it may be incomplete — was the scan interrupted?) | Re-run the scan to completion | 1 |
| E-IMP-005 | Unsafe XML construct | File contains XML entity declarations, which are not allowed for security reasons | Use an unmodified Nmap XML file | 1 |
| E-IMP-006 | Not Nmap XML | File is not Nmap XML output | Produce the file with Nmap's `-oX` option | 1 |
| E-IMP-007 | Unsupported Nmap version | Nmap version `<v>` is not supported (7.0 or later required) | Upgrade Nmap | 1 |
| E-IMP-008 | Duplicate | This file was already imported as scan `<id>` | None needed | 1 |
| E-IMP-009 | Required data missing | Required data missing: `<item>` | Use a complete Nmap XML file | 1 |
| E-HIS-001 | Unknown scan ID | No scan with ID `<id>` | Run `testbondanh list` | 1 |
| E-CMP-001 | Fewer than two scans | At least two scans are needed to compare | Import another scan | 1 |
| E-CMP-002 | Same scan twice | Cannot compare a scan with itself | Choose two different scans | 1 |
| E-DAT-001 | Data folder not writable | Cannot create or write data folder `<path>` | Choose another location with `--data-dir` | 1 |
| E-DAT-002 | LOCALAPPDATA unset | Cannot determine default data folder | Use `--data-dir` | 1 |
| E-RPT-001 | Output folder not writable | Cannot write reports to `<path>` | Choose another folder with `--output` | 1 |
| E-RPT-002 | Masking leak detected | Masked report would contain an original identifier; no report written | Report this as a bug; use an unmasked report locally only | 1 |
| E-INT-001 | Unexpected internal error | An unexpected error occurred | Re-run with `--debug` | 3 |

- AC1: For each error, a test triggers it and asserts the ID, the "Next step" line, the exit code, and the absence of a traceback.

## 16. Traceability: PR / NFR → FR

| PR / NFR | FRs |
|---|---|
| PR-001 Import | FR-027, FR-031, FR-032 |
| PR-002 Reject unsafe input | FR-020 – FR-025, FR-027, FR-033 |
| PR-003 Duplicates | FR-026 |
| PR-004 Completeness | FR-028 – FR-030, FR-032, FR-067 |
| PR-005 List | FR-040 |
| PR-006 Delete | FR-041, FR-042 |
| PR-007 Choose scans | FR-050, FR-051 |
| PR-008 Detect changes | FR-052 – FR-066 |
| PR-009 Confirmed vs uncertain | FR-055 – FR-065, FR-067, FR-069 |
| PR-010 Ranking | FR-070, FR-071 |
| PR-011 First seen | FR-068 |
| PR-012 Advice | FR-072 |
| PR-013 Markdown | FR-080 – FR-082, FR-085, FR-087, FR-088 |
| PR-014 JSON | FR-080, FR-083 – FR-085 |
| PR-015 Masking | FR-088, FR-090 – FR-094 |
| PR-016 Terminal summary | FR-086 |
| PR-017 Help and errors | FR-001 – FR-005, Section 15 |
| PR-018 Data location | FR-010, FR-011, FR-081 |
| PR-019 Git warning | FR-012 |
| PR-020 Docs / authorised use | FR-006 (README content verified manually) |
| NFR-001 Performance | Verified by timed test; no dedicated FR |
| NFR-002 Size limit | FR-021 |
| NFR-003 Untrusted input | FR-022 |
| NFR-004 No network | FR-095 |
| NFR-005 Atomic import | FR-031 |
| NFR-006 Usability | FR-003 – FR-005, Section 15 |
| NFR-007 Platform | FR-010 AC3 |
| NFR-008 Determinism | FR-085, FR-092 |
| NFR-009 Verifiability | All ACs; test strategy |
| NFR-010 Repo hygiene | Harness design (not runtime behaviour) |
| NFR-011 Dependencies | TRD (not runtime behaviour) |
| NFR-012 Readability | FR-004 |

All PRs and NFRs are covered.

## 17. Open Questions

Resolved 2026-10-27: owner approved the proposed answers for FQ-01 to FQ-05 (DEC-023).

| ID | Question | Resolution |
|---|---|---|
| FQ-01 | A port that was `filtered` and is now `open`: confirmed or uncertain? | **Uncertain** (`previous_state_undetermined`), because Nmap defines `filtered` as "cannot determine whether the port is open". Consistent with DEC-003, but a firewall change exposing a service will appear as uncertain, not High (FR-060) |
| FQ-02 | Truncated XML from an interrupted scan: reject, or partially import? | **Reject** (FR-023). Partial recovery parsing is complex and error-prone; rejecting cannot cause a false change |
| FQ-03 | Address coverage from `args` is a heuristic (FR-030). Acceptable? | **Yes** for MVP; when unsure, coverage is "unknown" and new hosts become uncertain, never falsely confirmed |
| FQ-04 | Reject Nmap versions before 7? | **Yes** (FR-025) |
| FQ-05 | High-importance ports: keep the five, or add e.g. 21 (FTP), 139 (NetBIOS), 5985/5986 (WinRM)? | **Keep five** for MVP; revisit later |
| OQ-01, OQ-02, OQ-07 | Python version, branch name, database protection | TRD / before first commit |

## 18. Approval Checklist

Completed: owner approved the FRD as drafted on 2026-10-27.

- [x] CLI commands, options, and exit codes (Section 5)
- [x] Logical data model (Section 6)
- [x] Import validation order and rules (Section 7), including FQ-02 and FQ-04
- [x] Address coverage heuristic (FR-030, FQ-03)
- [x] State groups and classification rules FR-055 – FR-069, including FQ-01
- [x] Ranking, High-importance ports, and advice text (Section 11), including FQ-05
- [x] Report structure and JSON fields (Section 12)
- [x] Masking rules and leak check (Section 13)
- [x] Data location and Git warning (Section 14)
- [x] Error catalogue (Section 15)
- [x] Every PR/NFR covered (Section 16)
- [x] **FRD approved — status may change to "Approved" (version 1.0)**
