# Case Study Engine

Turns one project's document library into a case study the buyer believes and the client's finance and legal teams
would sign: story spine, results sheet, exposure report, three-reader case study, media pack and approval request.
Every line is traced, every number is computed by code with its working, and nothing leaves without the right human approvals.

**New here?** Read `CLAUDE.md` (quick context), then `DOCUMENTATION.md` (full design). `DATA.md` lists every data file used.

## Quick start
```bash
pip install -r requirements.txt
```
Unzip the project library (confidential, from the hackathon organisers) to `library/Project_Drishti_Library/`, then:
```bash
python engine/run.py build --project drishti
```
```bash
python -m pytest -q tests
```
Open `runs/drishti/viewer.html`.

## Hand-in checklist (maps to the brief)

| Brief item | Where |
| --- | --- |
| 1. Six outputs | `runs/drishti/pack/` after a build (story spine, results sheet + calc ledger, exposure report, case study traced + clean, `05_media/`, approval request) |
| 1b. Manual edits log | `MANUAL_EDITS_LOG.md` |
| 2. Engine + every prompt | `engine/run.py`, `engine/agents/`, `engine/prompts/`; run log `runs/drishti/run_log.txt` |
| 3. Tests (12; refuse + stop included) | `tests/test_engine.py` |
| 4. Process, one page | `PROCESS.md` |
| 5. Prompt log | `PROMPT_LOG.md` |
| 6. Pitch, 3 slides | `PITCH.pptx` (`python scripts/make_pitch.py`) |
| Review screen | `runs/drishti/viewer.html` |
| Demo script | `DEMO_SCRIPT.md` |
| Docs as PDF | `docs_pdf/` (`python scripts/make_pdfs.py`) |

## Commands
| Command | What it does |
| --- | --- |
| `python engine/run.py build --project <p> [--library <dir>]` | Runs the agent chain; stops at the human gate |
| `python engine/run.py approve --project <p> --stage internal\|client --role <r> --name <n> --decision <d>` | A person records a decision on the exact pack |
| `python engine/run.py release --project <p> --stage internal\|client` | Releases only if every rule is met |
| `python engine/run.py withdraw --project <p> --stage client --role <r> --date <d>` | Client withdraws approval |
| `python demo/reset_demo.py` / `python demo/make_bad_draft.py` | Demo reset / refusal demo |
