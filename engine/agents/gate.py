"""Agent 8 - Approval gate. Nothing leaves the building without two recorded human approvals on the exact files.

Stage 1 (internal): the vendor's delivery owner checks the pack before it goes to the client for review.
Stage 2 (client): the client's authorised approvers (from the contract rules) choose an option per asset.
The gate hashes every file in the pack; any edit after approval invalidates it and the release stops again.
"""
import hashlib
import json
from datetime import date
from pathlib import Path


def pack_hash(pack_dir: Path):
    h = hashlib.sha256()
    for p in sorted(pack_dir.rglob("*")):
        if p.is_file():
            h.update(p.relative_to(pack_dir).as_posix().encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def check(pack_dir: Path, approval_file: Path, required_roles):
    """Return (ok, reasons). Called before any outward step (sending to client, publishing)."""
    reasons = []
    if not approval_file.exists():
        return False, [f"STOP: no approval record at {approval_file}. A person must approve before anything leaves."]
    rec = json.loads(approval_file.read_text(encoding="utf-8"))
    if rec.get("pack_sha256") != pack_hash(pack_dir):
        reasons.append("STOP: pack changed after approval (hash mismatch). Re-approval needed.")
    got = {a["role"]: a for a in rec.get("approvals", [])}
    for role in required_roles:
        a = got.get(role)
        if not a:
            reasons.append(f"STOP: missing approval from role '{role}'.")
        elif a.get("decision") not in ("approve_named", "approve_anonymised", "approve_internal_only", "approve"):
            reasons.append(f"STOP: {role} decision is '{a.get('decision')}' - not releasable.")
        elif a.get("withdrawn_on"):
            reasons.append(f"STOP: {role} withdrew approval on {a['withdrawn_on']} (MSA 15.4: stop new use within 30 days).")
    if rec.get("first_use_date") and rec.get("sent_for_review_on"):
        d0, d1 = date.fromisoformat(rec["sent_for_review_on"]), date.fromisoformat(rec["first_use_date"])
        bdays = sum(1 for i in range(1, (d1 - d0).days + 1) if date.fromordinal(d0.toordinal() + i).weekday() < 5)
        if bdays < 10:
            reasons.append(f"STOP: only {bdays} business days between review and first use; contract requires 10.")
    return not reasons, reasons
