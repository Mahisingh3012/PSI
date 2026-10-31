# Data used by this project

## 1. The input: Project Drishti library (included in this private repository)

- **What:** `Project_Drishti_Library.zip`, the hackathon's fictional project library: 42 files, January to September 2026.
- **Where it comes from:** the PanScience Innovation Hackathon organisers (31 Oct 2026). Brief: `PSI hackathon case study assignment.pdf`.
- **Confidential:** the hackathon rules say to treat the library as confidential. It is included here so the project opens complete; keep this repository private and rotate credentials after use. The brief is in `library/PSI hackathon case study assignment.pdf`.
- **Where it is:** already in this repository, at:
  ```
  library/Project_Drishti_Library/00_README.md
  ```
  The engine also finds it at `../Project_Drishti_Library/Project_Drishti_Library` (the author's layout), or you can pass `--library <folder>`.

### Every file, its evidence ID, and what the engine used it for

IDs are assigned by the Librarian agent in sorted path order. Citations in the outputs look like `[D06:L45]` (file D06, line 45).

| ID | File | Used for | By |
| --- | --- | --- | --- |
| D01 | 00_README.md | Library orientation (units, folder map) | Librarian |
| D02 | 01_contract/MSA_confidentiality_and_publicity_extract.md | **Read first.** Publicity rules 15.1–15.4, confidentiality 14.1–14.4, data handling | Rules, Exposure, Approval, Writer (25 citations) |
| D03 | 02_scoping/2026-02-06_discovery_call_transcript.txt | The "before" in the client's words; IT/OT constraints; the asks that became scope changes | Timeline, Writer |
| D04 | 02_scoping/2026-02-14_RFQ_…md | What was requested (mandatory vs optional) | Timeline |
| D05 | 02_scoping/2026-02-24_PredCo_proposal_v1.md | What was promised (original targets, phases, harness not offered) | Timeline (sold vs delivered) |
| D06 | 02_scoping/2026-03-05_BRD_v2_signed.md | **Signed KPI definitions, baselines, windows, targets**; acceptance rule | Results spec, Results sheet |
| D07 | 03_commercial/change_requests_CR01-CR03.md | Scope changes: kiln added, face recognition removed, gate analytics + K5 added | Timeline, Results spec |
| D08 | 03_commercial/purchase_orders.md | Phases, scope, amendment; deal size as a band only | Timeline, Exposure |
| D09 | 04_delivery/incident_report_INC-0611.md | Outage and how it was handled | Timeline, Writer (gatekeeper) |
| D10 | 04_delivery/pilot_acceptance_certificate_2026-07-06.md | **Signed pilot results** (used to check the calculator) | Results sheet, tests |
| D11 | 04_delivery/project_tracker.csv | Dates, delays, client-side remediation actions | Timeline |
| D12 | 05_meetings/2026-04-17_poc_review_transcript.txt | Turning point: false alarms, new Head EHS's conditions, floor feedback | Timeline, Writer (user) |
| D13 | 05_meetings/2026-06-26_steering_committee_transcript.txt | Credit sharing, Finance rejecting benchmark ROI, plant-wide decision | Timeline, Results sheet |
| D14 | 05_meetings/2026-09-18_QBR_transcript.txt | Post-scale results, gate attribution, case-study conditions | Results sheet, Writer, Exposure |
| D15 | 06_email/A_…inbound_and_first_reply.md | First contact; contact data (exposure) | Timeline, Exposure |
| D16 | 06_email/B_…security_review.md | Gatekeeper proof: blockers and how they were resolved | Writer (gatekeeper) |
| D17 | 06_email/C_…EHS_handover.md | Champion left; successor's requests | Timeline |
| D18 | 06_email/D_…face_recognition_privacy.md | Privacy decision and module removal | Timeline, Writer (gatekeeper) |
| D19 | 06_email/E_…pilot_results_numbers.md | The rejected "74% to 96.6%" summary: a refuse example | Results sheet |
| D20 | 06_email/F_…payment_GRN.md | Late payments (process lesson) | Timeline |
| D21 | 06_email/G_…finance_value_estimate.md | **Only money figures the client measured**; what not to monetise | Results spec, Results sheet, Writer (buyer) |
| D22 | 06_email/H_…case_study_permission.md | Who must approve, options to offer, timing advice from the champion | Rules, Approval |
| D23 | 07_data/baseline_manual_safety_walks_2025Q4.csv | Walk score 73.8% (reference only) | Calculator |
| D24 | 07_data/data_dictionary.md | Column meanings, counting rules, data quality of the gate register | Results spec |
| D25 | 07_data/ehs_register_monthly_2025_2026.csv | LTIs; near-miss definition change | Calculator, Results sheet |
| D26 | 07_data/gate_truck_turnaround_daily.csv | K5 turnaround, event markers | Calculator, Media |
| D27 | 07_data/invoices_and_payments.csv | Scale and timing only (identifiers flagged) | Exposure |
| D28 | 07_data/supervisor_survey_sep2026.csv | Survey scores; duplicate comments detected | Calculator, Writer (user) |
| D29 | 07_data/viewos_weekly_zone_metrics.csv | **K1–K4 and all post-scale results** | Calculator, Media |
| D30 | 08_github/CHANGELOG.md | What was built and when | Timeline, Writer |
| D31 | 08_github/configs/site_bhadrapur.yaml | Exposure: IPs, RTSP URLs, capacity in config | Exposure |
| D32 | 08_github/docs/model_eval_report.md | Read; not used for results (per-frame precision does not convert into compliance accuracy) | – |
| D33 | 08_github/git_log.txt | Dates of remediation work | Timeline |
| D34 | 08_github/README.md | Counting rules; exposure (repo name, IPs) | Results sheet, Exposure |
| D35 | 09_feedback/linkedin_post_…md | Public link between client and vendor (combination risk) | Exposure, Timeline |
| D36 | 09_feedback/whatsapp_Drishti-Packing_group_export.txt | Floor-level human moments, rule-change transparency | Writer (user), Results sheet |
| D37 | 10_media/architecture_as_built_revC.png | Exposure only (client name, IPs); redrawn | Exposure |
| D38 | 10_media/cam_PK2-07_alert_snapshot_2026-06-29.jpg | Exposure only (signage, **GPS in EXIF**); never used | Exposure |
| D39 | 10_media/dashboard_export_ppe_weekly_2026-09-25.png | Exposure only (client name, console URL, user email); redrawn | Exposure |
| D40 | 11_public/ardent_public_profile.md | What is already public (capacity, units, press release) | Exposure |
| D41 | 12_vendor/sales_deck_draft_notes_2026-09-23.md | Claims to refuse | Results sheet, Exposure |
| D42 | 12_vendor/vendor_profile_team_achievements.md | Vendor credentials; the withdrawn award nomination | Writer (gatekeeper), Exposure |

## 2. What is in the repo

| Path | What it is | Regenerated by `build`? |
| --- | --- | --- |
| `runs/drishti/agent_outputs/02_rules_and_terms.json` | Rules agent output: 12 rules, approvers, 38 banned/replacement terms | No: LLM output (replayed without an API key) |
| `runs/drishti/agent_outputs/03_metric_spec.json` | Results agent output: 44 calc definitions + headline KPI list | No: LLM output |
| `runs/drishti/agent_outputs/01…06_*.md` | Writer outputs (story spine, results sheet, exposure report, case study, approval request) | No: LLM output |
| `engine/`, `tests/`, `demo/`, `scripts/` | The engine, its prompts, tests, demo helpers | – |

These agent outputs quote the confidential library (client and people names). Treat the repo as confidential too.

## 3. What `build` regenerates (committed so the project opens complete; rebuilt on every run)

`evidence_index.*` (contains the full library text), `calc_ledger.*`, `exposure_scan.md`, `exposure_hits.json`,
`media/`, `verifier_report.md`, `run_log.txt`, `pack/`, `pack_sha256.txt`, `viewer.html`. Approval records
(`approvals/`) and the project register (`runs/register.*`) are local state created by `approve` / `release` / `withdraw`.
