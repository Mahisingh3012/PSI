# Manual edits log

How the judgement-agent outputs in `runs/drishti/agent_outputs/` were produced: no LLM API key was available on
this machine, so the Rules, Results-spec, Exposure, Timeline, Writer and Approval agents were run by Claude (Opus 5.5)
in Claude Code, following the prompts in `engine/prompts/`. The engine replays those saved outputs (the run log marks
them RECORDED) and runs every deterministic agent live. With `GEMINI_API_KEY` set (in `.env`), the same prompts are sent live to Google Gemini 3.

| # | File | Edit | Why | By |
| --- | --- | --- | --- | --- |
| 1 | 03_metric_spec.json | K3 note changed after the calculator showed the alert-weighted proxy reproduces 4.9 min exactly | Note was wrong ("cannot reproduce") | Claude, after first calc run |
| 2 | 03_metric_spec.json | Added `payback_half_noamc` | To match the client Finance's own "a little over two years" | Claude |
| 3 | 01_story_spine.md | "4 LTIs ... 90 target" changed to the words used in the transcript, plus a calc cite | Verifier refused: numbers not on the cited line | Verifier -> Claude |
| 4 | 02_results_sheet.md | Added BRD and certificate line cites for the 90% target and the 41-hour outage; "15 hours" written as in the source | Verifier refused | Verifier -> Claude |
| 5 | 03_exposure_report.md | Added cites for 146 cameras and the audit month; "40 km" written as in the source | Verifier refused | Verifier -> Claude |
| 6 | 04_case_study.md | Added BRD cite for the 50% target | Verifier refused | Verifier -> Claude |
| 7 | 06_approval_request.md | Form rows marked [NO-CLAIM]; added sales-deck cite for the rejected 2.3 crore | Verifier refused | Verifier -> Claude |
| 8 | engine/agents/verify.py | Table header rows and contract clause numbers ("MSA 15.2") no longer treated as claims | False positives on the first run (63 refused, 0 after fixes) | Claude |
| 9 | engine/agents/media.py | Moved overlapping chart labels; removed a wrong arrow in the diagram | Visual check of the rendered PNGs | Claude |
| 10 | engine/agents/verify.py | New rules: citation relevance (WEAK_CITE / blank line) and estimates must say ASSUMED | Rubric review: judges check every claim against the library; rule 5 of the brief | Claude |
| 11 | 01_story_spine.md | Corrected three citations (PO amendment, proposal harness line, BRD definitions); "Sponsor" changed to "business owner and first champion"; full go-live corrected to "3 days after plan" (was "one week late") | New verifier rules + fact check against BRD stakeholders and tracker T21/T27 | Verifier -> Claude |
| 12 | 02_results_sheet.md | Two citations moved to the right lines (certificate header, gate-register data quality) | WEAK_CITE | Verifier -> Claude |
| 13 | 03_exposure_report.md | Six citations moved to the right lines (state in signature, invoices header, camera config); row wording made specific | WEAK_CITE | Verifier -> Claude |
| 14 | 04_case_study.md | September detention marked ASSUMED (Finance estimate); "within two months" changed to "by September" | ASSUMED_NOT_MARKED; fact check | Verifier -> Claude |
| 15 | 06_approval_request.md | Firm reply date (Mon 16 Nov 2026 = 10 business days from Mon 2 Nov); estimates marked ASSUMED; offered charts for the client's own council deck | Brief asks for a reply date; make yes good for them | Claude |
| 16 | 03_metric_spec.json | Added a `headline` list (6 KPIs) for the viewer dashboard | UI | Claude |
| 17 | media.py ROI calculator | Labelled example inputs; the one-month reference figure marked ASSUMED | Rule 5 | Claude |
| 18 | engine/run.py | A refused rebuild now deletes any older pack | Bug: an old approved pack could otherwise stay releasable | Claude |

No number in any output was typed by hand: all come from `calc_ledger.md` or a cited source line.
