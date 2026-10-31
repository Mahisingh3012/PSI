# Process: from project closure to published proof (one page)

| # | Step | Trigger | Owner | What the engine does / records |
| --- | --- | --- | --- | --- |
| 1 | Trigger | Acceptance or go-live sign-off is signed, or a QBR reports results | Delivery Manager | Freezes a read-only copy of the project folder; `run.py build --project <name>` |
| 2 | Engine run | Automatic | Agents 1–7 | Six outputs + `verifier_report.md` + `run_log.txt`; register status `awaiting_internal` or `refused` |
| 3 | Verifier refuses | Any untraceable line, wrong number, identifier, unmarked estimate, image metadata | Fixer agent (live mode, up to 2 rounds) → Delivery Manager | No pack exists while anything is refused; an older pack is deleted so it can never be released |
| 4 | **STOP 1: internal approval** | Pack assembled | Delivery owner who did **not** write it (plus Legal/DPO if sensitive) | `run.py approve --stage internal …`, bound to the pack's SHA-256 hash |
| 5 | Send to client | `release --stage internal` passes | Account Director | Sends to the approvers the **contract** names (here Corporate Comms, cc Legal), by email, never WhatsApp; review clock starts (10 business days here) |
| 6 | **STOP 2: client decision** | Reply received | Client's authorised signatories, per asset: named / anonymised / internal only / no | `run.py approve --stage client …` per role; `release --stage client` checks roles, hash, notice period, withdrawals |
| 7 | Publish | Gate passes | Marketing | Publishes exactly the approved hash; register status `approved` |

**On a "no"** (`--decision reject`): nothing is published; register status becomes `declined` with the reason;
every asset stays internal-only. We make one smaller ask (anonymised without numbers, or internal sales use only)
and otherwise wait for the next milestone (here: the final audit result) with a fresh build. We never chase.

**On a partial yes**: each approver's option is recorded; only what every required approver allowed is released.

**On a later change of mind** (contract clause 15.4): `run.py withdraw …`; the gate blocks new use at once; register status
`withdrawn`; Marketing removes live copies within 30 days; sales decks are rebuilt without it.

**On any edit after approval**: the pack hash changes, so earlier approvals are void (kept in history) and both stops repeat.

**Records**: `runs/register.json|md` holds one row per project with status and an append-only event history.
Each run folder keeps its evidence index, calculation ledger, verifier report, run log, approvals (who, role,
decision, channel, time, hash) and the exact pack. Keep for 5 years, matching the contract's confidentiality term.

**50 projects a year, different data**: the code doesn't change per project. The Rules agent reads each project's
own contract, and the Results agent writes each project's own metric spec over whatever CSVs exist. The register shows
every project's status in one table. People spend time only at the two stops, ASSUMED to be about 30 minutes for the
internal check because every line already shows its source. Projects whose contract forbids publicity run as
`internal only`, so sales still get a fact-checked internal reference.
