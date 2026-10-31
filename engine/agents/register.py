"""Project register. One record per project across all runs: status, approvals, decisions, withdrawals and an
append-only event history. This is the record-keeping layer of the process (runs/register.json + register.md),
and the place to see 50 projects a year at a glance.
"""
import json
from datetime import datetime
from pathlib import Path

STATUS_TEXT = {
    "refused": "Verifier refused the draft (writer must fix)",
    "awaiting_internal": "Pack ready; waiting for internal approval",
    "internal_approved": "Internal approval recorded",
    "with_client": "Sent to client; waiting for authorised approvers",
    "declined": "Client said no: internal use only, no new ask until the next milestone",
    "approved": "Approved for use (see options per approver)",
    "withdrawn": "Approval withdrawn: stop new use within 30 days",
}


def _load(runs: Path):
    f = runs / "register.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def update(runs: Path, project, status, event, **fields):
    reg = _load(runs)
    rec = reg.setdefault(project, {"history": []})
    rec.update(fields)
    rec["status"] = status
    rec["updated"] = datetime.now().isoformat(timespec="seconds")
    rec["history"].append({"at": rec["updated"], "event": event, "status": status})
    (runs / "register.json").write_text(json.dumps(reg, indent=1), encoding="utf-8")
    rows = ["# Project register", "", "| Project | Status | Pack | Verifier problems | Last event | Updated |",
            "| --- | --- | --- | --- | --- | --- |"]
    for name, r in sorted(reg.items()):
        rows.append(f"| {name} | {STATUS_TEXT.get(r['status'], r['status'])} | {str(r.get('pack_sha256', '-'))[:12]} | "
                    f"{r.get('verifier_problems', '-')} | {r['history'][-1]['event']} | {r['updated']} |")
    (runs / "register.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return rec


def get(runs: Path, project=None):
    reg = _load(runs)
    return reg.get(project) if project else reg
