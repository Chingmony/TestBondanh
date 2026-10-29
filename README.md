# TestBondanh

> **Status: under development.** The requirements and design documents are complete and approved. Application code has not been written yet. Nothing in this repository is ready to use.

TestBondanh is a local command-line tool for Windows 11. It imports [Nmap](https://nmap.org/) XML scan results, keeps a private history of scans, and reports what changed between two scans. It's designed for home-lab and small-office owners who want to know what changed on their network and whether it matters.

Its guiding rule: **something seen can confirm a change; something *not* seen never can.** A host that stops answering, or a scan that didn't finish, is reported as an *uncertain observation*, never as a confirmed change.

## Authorised use only

**Use TestBondanh only with scan results from networks you own or are authorised to assess.**

TestBondanh does not scan networks itself. You produce the Nmap XML file; TestBondanh only reads it.

## Planned capabilities (MVP)

- Import Nmap XML files safely, treating every file as untrusted input
- Keep a local scan history, and delete scans you no longer want to keep
- Compare any two scans: new hosts, opened and closed ports, changed services
- Separate **confirmed changes** from **uncertain observations**; rank confirmed changes High / Medium / Low
- Markdown reports (for people) and JSON reports (for other tools)
- Optional masking of IP addresses, hostnames, and MAC addresses for safer sharing

## Privacy

- Scan data stays on your computer. TestBondanh never sends data anywhere.
- Data is stored by default in `%LOCALAPPDATA%\TestBondanh`, outside any project folder.
- The database is protected only by your Windows account permissions. It isn't encrypted.

## Project documentation

This project is built with a documentation-first, approval-gated, AI-assisted workflow using Claude Code. Every requirement is traceable to its design, code, and tests.

| Document | Purpose |
|---|---|
| [Business Requirements](docs/requirements/BRD.md) | Why the tool exists and how success is judged |
| [Product Requirements](docs/requirements/PRD.md) | What the user gets |
| [Functional Requirements](docs/requirements/FRD.md) | Exact system behaviour |
| [Technical Requirements](docs/architecture/TRD.md) | Technologies, versions, and technical rules |
| [System Architecture](docs/architecture/SAD.md) | Components and how they fit together |
| [Test Strategy](docs/quality/TEST-STRATEGY.md) | How correctness is demonstrated |
| [Traceability Matrix](docs/traceability/REQUIREMENTS-TRACEABILITY.md) | Requirement → design → test mapping |
| [AI Harness Design](docs/harness/AI-HARNESS-DESIGN.md) | How AI-assisted development is configured and verified |
| [Development Plan](docs/planning/DEVELOPMENT-PLAN.md) | Milestones and tasks |
| [Decision Log](docs/planning/DECISION-LOG.md) | Decisions and their reasons |
| [Risk Register](docs/planning/RISKS.md) | Risks and mitigations |

## License

[MIT](LICENSE)
