# TestBondanh — Requirements Traceability Matrix

| Field | Value |
|---|---|
| Document | Requirements Traceability Matrix (RTM) |
| Project | TestBondanh — Network Security Monitoring Tool |
| Purpose | Show, for every requirement, where it is designed, implemented, and tested, and whether it currently passes |
| Status | **Approved** — by project owner, 2026-10-28 |
| Version | 1.0 |
| Based on | BRD, PRD, FRD, TRD, SAD (v1.0 Approved); Test Strategy (v1.0 Approved) |
| Owner / Approver | Project owner (Chingmony) |
| Author | Claude Code (drafted under owner direction) |
| Last updated | 2026-10-27 |

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-27 | Claude Code | Initial matrix; all tests Planned (no code exists) |
| 1.0 | 2026-10-28 | Project owner | Approved as drafted |

## 1. How to Read and Maintain This Matrix

- **Section 2 (downward chain)** is maintained **by hand**. It changes only when an approved document changes.
- **Section 3 (test mapping)** and **Section 4 (gaps)** will be **generated** by `scripts/trace.py` from `@pytest.mark.req(...)` markers and test results, once code exists (DEC-039). Until then they list *planned* tests.
- **Status values:** **Planned** (test named, not written) · **Approved** (written, owner-approved, failing) · **Passing** · **Failing** · **Manual — pending / done (date)**.

**Current implementation status: no code or tests exist. Every test below is Planned.**

## 2. Downward Chain: BR → PR / NFR → FR → TR → Component

| BR | PR / NFR | FR | TR | SAD component |
|---|---|---|---|---|
| BR-001 Import Nmap XML | PR-001, NFR-001 | FR-027, FR-031, FR-032 | TR-020 – TR-024 | `services/import_scan`, `adapters/nmap_xml` |
| BR-002 Scan history | PR-001, PR-003, PR-005, PR-006, PR-007, PR-011 | FR-026, FR-040 – FR-042, FR-050, FR-051, FR-068 | TR-030 – TR-033 | `services/history`, `services/compare`, `adapters/sqlite_repo` |
| BR-003 Detect changes | PR-007, PR-008, NFR-001 | FR-050 – FR-066 | TR-025 | `domain/states`, `domain/classify` |
| BR-004 No unsupported claims | PR-003, PR-004, PR-009 | FR-055 – FR-065, FR-069 | — | `domain/states`, `domain/classify` |
| BR-005 Incomplete ≠ gone | PR-004, PR-009 | FR-028, FR-058, FR-062, FR-067 | — | `domain/completeness`, `domain/classify` |
| BR-006 Untrusted input | PR-002, NFR-002, NFR-003, NFR-005 | FR-020 – FR-025, FR-031, FR-033 | TR-020 – TR-023, TR-032 | `adapters/files`, `adapters/nmap_xml`, `adapters/sqlite_repo` |
| BR-007 Understandable reports | PR-010, PR-012, PR-013, NFR-012 | FR-070 – FR-072, FR-082, FR-087 | — | `domain/ranking`, `domain/advice`, `reporting/*` |
| BR-008 Markdown + JSON | PR-013, PR-014 | FR-080 – FR-085 | TR-041, TR-042 | `reporting/*`, `adapters/files` |
| BR-009 Masking | PR-015 | FR-088, FR-090 – FR-094 | TR-050 | `domain/masking`, `services/compare` |
| BR-010 Data stays local | PR-006, PR-012, PR-018, NFR-004 | FR-010, FR-011, FR-095 | TR-035, TR-037, TR-SEC-02 | all (no network I/O); `services/settings` |
| BR-011 No scanning | PR-020 | FR-006 | — | `cli` |
| BR-012 Clear CLI | PR-016, PR-017, PR-020, NFR-006 | FR-001 – FR-005, FR-086, FRD §15 | TR-071, TR-072, TR-074 | `cli/*` |
| BR-013 Demonstrable correctness | NFR-008, NFR-009 | FR-085, FR-092 | TR-041, TR-050, TR-065 – TR-067 | tests, `scripts/verify.py`, `scripts/trace.py` |
| BR-014 Repository hygiene | PR-006, PR-018, PR-019, NFR-010 | FR-012 | TR-SEC-03 – TR-SEC-05 | `adapters/files`; harness |

## 3. Test Mapping (planned)

### 3.1 Import and validation

| Req | Planned test(s) | Level | Status |
|---|---|---|---|
| FR-020 | `test_missing_file_raises_e_imp_001`, `test_unreadable_file_raises_e_imp_002` | integration | Planned |
| FR-021 | `test_oversized_file_rejected_before_parsing` | security | Planned |
| FR-022 | `test_xxe_local_file_rejected`, `test_external_dtd_rejected`, `test_billion_laughs_rejected_quickly`, `test_reference_fixture_with_doctype_accepted` | security / integration | Planned |
| FR-023 | `test_non_xml_rejected`, `test_truncated_file_rejected_with_interrupt_hint` | integration | Planned |
| FR-024 | `test_non_nmaprun_root_rejected`, `test_wrong_scanner_rejected` | integration | Planned |
| FR-025 | `test_nmap_7_accepted`, `test_nmap_6_rejected`, `test_unparseable_version_rejected` | integration | Planned |
| FR-026 | `test_duplicate_file_rejected_with_existing_id` | e2e | Planned |
| FR-027 | `test_missing_start_rejected`, `test_missing_runstats_rejected`, `test_host_without_ip_skipped_with_warning` | integration | Planned |
| FR-028 | `test_exit_error_marks_incomplete`, `test_timed_out_host_marks_incomplete`, `test_missing_exit_attribute_is_complete` | unit (domain) | Planned |
| FR-029 | `test_scaninfo_services_expanded` | unit (domain) | Planned |
| FR-030 | `test_cidr_target_coverage_known`, `test_exclude_makes_coverage_unknown`, `test_port_list_not_mistaken_for_target` | unit (domain) | Planned |
| FR-031 | `test_failed_import_leaves_history_unchanged` | integration | Planned |
| FR-032 | `test_import_prints_id_start_hosts_completeness` | e2e | Planned |
| FR-033 | `test_os_and_script_elements_ignored` | integration | Planned |

### 3.2 History

| Req | Planned test(s) | Level | Status |
|---|---|---|---|
| FR-040 | `test_list_orders_newest_first`, `test_list_empty_history_message` | e2e | Planned |
| FR-041 | `test_delete_removes_all_scan_data`, `test_delete_unknown_id_e_his_001`, `test_deleted_scan_ignored_by_first_seen` | integration / e2e | Planned |
| FR-042 | `test_delete_prompts_and_cancels_on_no`, `test_delete_yes_skips_prompt`, `test_delete_non_interactive_without_yes_cancels` | e2e | Planned |

### 3.3 Comparison

| Req | Planned test(s) | Level | Status |
|---|---|---|---|
| FR-050 | `test_default_compares_latest_two`, `test_compare_explicit_ids`, `test_fewer_than_two_scans_e_cmp_001`, `test_same_id_twice_e_cmp_002`, `test_single_id_usage_error` | e2e | Planned |
| FR-051 | `test_baseline_is_earlier_regardless_of_order` | unit (services) | Planned |
| FR-052 | `test_ipv6_case_insensitive_identity` | unit (domain) | Planned |
| FR-053 | `test_same_mac_note_on_moved_device` (+ e2e `c13`) | unit / e2e | Planned |
| FR-054 – FR-055 | `test_effective_state_listed_port`, `test_effective_state_single_extraports`, `test_effective_state_multiple_extraports_undetermined`, `test_effective_state_not_scanned`, `test_state_groups` | unit (domain) | Planned |
| FR-056 | `test_new_host_confirmed_when_covered` (+ e2e `c01`) | unit / e2e | Planned |
| FR-057 | `test_new_host_uncertain_when_not_covered`, `test_new_host_uncertain_when_baseline_incomplete` (+ e2e `c02`) | unit / e2e | Planned |
| FR-058 | `test_missing_host_uncertain_even_if_complete_scan`, `test_missing_host_uncertain_when_newer_incomplete` (+ e2e `c03`, `c04`) | unit / e2e | Planned |
| FR-059 | `test_closed_to_open_confirmed` (+ e2e `c05`) | unit / e2e | Planned |
| FR-060 | `test_filtered_to_open_is_uncertain`, `test_not_scanned_to_open_is_uncertain` (+ e2e `c06`) | unit / e2e | Planned |
| FR-061 | `test_open_to_closed_confirmed` (+ e2e `c08`) | unit / e2e | Planned |
| FR-062 | `test_open_to_filtered_is_uncertain`, `test_open_to_closed_filtered_is_uncertain` (+ e2e `c07`) | unit / e2e | Planned |
| FR-063 | `test_probed_product_change_confirmed` (+ e2e `c09`) | unit / e2e | Planned |
| FR-064 | `test_probed_version_change_confirmed` (+ e2e `c10`) | unit / e2e | Planned |
| FR-065 | `test_table_method_change_uncertain` (+ e2e `c11`) | unit / e2e | Planned |
| FR-066 | `test_new_host_ports_listed_inside_finding` | unit (domain) | Planned |
| FR-067 | `test_timed_out_host_absences_uncertain` (+ e2e `c14`) | unit / e2e | Planned |
| FR-068 | `test_first_seen_is_earliest_scan` (`history_first_seen`) | integration / e2e | Planned |
| FR-069 | `test_all_uncertain_findings_reported` | unit (domain) | Planned |
| AC-C12 | `test_identical_scans_no_findings` (+ e2e `c12`) | unit / e2e | Planned |

### 3.4 Ranking, advice, reports, masking

| Req | Planned test(s) | Level | Status |
|---|---|---|---|
| FR-070 – FR-071 | `test_importance_levels`, `test_high_ports_tcp_only` | unit (domain) | Planned |
| FR-072 | `test_high_and_medium_have_advice_low_and_uncertain_do_not` | unit (domain) | Planned |
| FR-080 | `test_report_names_follow_pattern`, `test_existing_report_never_overwritten` | integration | Planned |
| FR-081 | `test_unwritable_output_e_rpt_001_no_partial_files` | integration | Planned |
| FR-082 | `test_markdown_sections_in_order`, `test_reason_codes_rendered_as_sentences`, golden `c01`/`c04`/`c09` | unit (reporting) | Planned |
| FR-083 | `test_json_has_all_keys`, `test_json_importance_and_reason_nullability` | unit (reporting) | Planned |
| FR-084 | `test_markdown_and_json_same_findings` | e2e | Planned |
| FR-085 | `test_findings_ordering`, `test_same_input_same_seed_identical_reports` | unit / e2e | Planned |
| FR-086 | `test_compare_prints_counts_and_paths` | e2e | Planned |
| FR-087 – FR-088 | `test_limitations_always_present`, `test_script_output_never_in_reports` | unit (reporting) | Planned |
| FR-090 – FR-091 | `test_masked_report_has_no_original_identifiers`, `test_placeholders_consistent_across_formats` | unit / security | Planned |
| FR-092 | `test_fixed_seed_reproducible`, `test_default_seed_varies` | unit / e2e | Planned |
| FR-093 | `test_masked_title_and_json_flag`, `test_masking_statement_present` | unit (reporting) | Planned |
| FR-094 | `test_leak_detected_nothing_written` (`c15`) | security | Planned |

### 3.5 CLI, data location, errors

| Req | Planned test(s) | Level | Status |
|---|---|---|---|
| FR-001 – FR-002 | `test_no_subcommand_usage_exit_2`, `test_unknown_option_exit_2`, `test_help_describes_options`, `test_version_flag` | e2e | Planned |
| FR-003 – FR-004 | `test_errors_use_catalogue_exit_codes`, `test_errors_go_to_stderr_with_prefix` | e2e | Planned |
| FR-005 | `test_internal_error_no_traceback_without_debug`, `test_debug_shows_traceback` | e2e | Planned |
| FR-006 | `test_help_contains_authorised_use_notice` | e2e | Planned |
| FR-010 | `test_data_dir_option_overrides_env`, `test_missing_localappdata_e_dat_002`, `test_paths_with_spaces_and_non_ascii` | integration | Planned |
| FR-011 | `test_data_dir_created_and_announced`, `test_unwritable_data_dir_e_dat_001` | integration | Planned |
| FR-012 | `test_warning_when_inside_git_repository` | integration | Planned |
| FR-095 | network-block autouse fixture active for every test (TR-SEC-02); `test_network_block_is_active` | security | Planned |
| FRD §15 | `test_every_error_id_has_message_next_step_exit_code` (parametrised over the catalogue) | e2e | Planned |
| — smoke | `test_installed_command_runs` (DEC-034) | e2e | Planned |

### 3.6 Non-functional and technical requirements

| Req | Planned test / check | Level | Status |
|---|---|---|---|
| NFR-001 / TR-090 – TR-092 | `test_import_compare_report_256_hosts_under_10s` | performance | Planned |
| NFR-007 | covered by FR-010 path test | integration | Planned |
| NFR-008 | covered by FR-085, FR-092 tests and golden files | unit / e2e | Planned |
| NFR-010 / TR-SEC-03 | `test_fixtures_contain_only_documentation_addresses` | security | Planned |
| TR-SEC-04 | `test_gitignore_contains_required_patterns` | security | Planned |
| TR-022 | `test_defusedxml_compatibility_on_python_313` (the three FR-022 cases) | security | Planned |
| TR-031 / TR-035 | `test_foreign_keys_enabled`, `test_deleted_scan_bytes_overwritten` | integration | Planned |
| TR-033 | `test_scan_ids_never_reused` | integration | Planned |
| SAD §5 / DEC-030 | `test_layer_dependency_rules` | architecture | Planned |
| NFR-011 / TR-SEC-01 | `pip-audit` before push | tool | Planned |
| TR-063 / TR-064 | ruff and mypy steps of `verify.py` | tool | Planned |
| TR-SEC-05 | secrets check — defined in AI Harness Design | harness | Planned |

### 3.7 Manual checks

| ID | Requirement | Status |
|---|---|---|
| MC-01 | BR-007, NFR-012 | Manual — pending |
| MC-02 | PR-020, TR-037 | Manual — pending |
| MC-03 | BR-009 | Manual — pending |

## 4. Gaps Report

| Type | Items |
|---|---|
| Requirements without a planned test or check | **None** (every FR, NFR, and testable TR in Sections 2–3 has at least one) |
| Planned tests without a requirement | **None** |
| Requirements verified only by tooling or review | NFR-011 (dependency policy), TR-013 (dependency approval process), TR-101 – TR-103 (version-control rules) — enforced by harness and owner review |

## 5. Success Metric Status

| Metric | Evidence required | Status |
|---|---|---|
| SM-01 End-to-end flow | e2e `c01` import → compare → both reports | Not started |
| SM-02 Every Must BR traced to a passing test | Section 2 complete; Section 3 all Passing | Not started (chain complete; tests planned) |
| SM-03 No false confirmed changes | `c02`, `c03`, `c04`, `c06`, `c07`, `c11`, `c14` Passing | Not started |
| SM-04 Hostile input handled | Section 3.1 security tests Passing | Not started |
| SM-05 Repository audit clean | TR-SEC-03 – TR-SEC-05 Passing before each push | Not started |
| SM-06 Masking leaks nothing | FR-090 – FR-094 tests Passing; MC-03 done | Not started |
| SM-07 Harness verified | Defined in AI Harness Design | Not started |
| SM-08 Documents approved | All planned documents approved: BRD, PRD, FRD, TRD, SAD (2026-10-27); Test Strategy, RTM, AI Harness Design (2026-10-28); Development Plan, Risk Register (2026-10-29). Decision Log is a living document | Met for documentation; continues per change |

## 6. Approval Checklist

Completed: owner approved this document as drafted on 2026-10-28.

- [x] Downward chain (Section 2) matches the approved documents
- [x] Planned tests cover every requirement (Section 3)
- [x] Gaps report is acceptable (Section 4)
- [x] Generated-maintenance approach (Section 1, DEC-039)
- [x] **RTM approved — status may change to "Approved" (version 1.0)**
