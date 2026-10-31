"""Agent 5 - Exposure scanner. Deterministic first pass; the Exposure agent (prompt 05_exposure.md) adds
judgement (combinations, quasi-identifiers) on top of what this finds.

Generic detectors run on any library. Client-specific terms (names, sites, code names) are learned from the
library itself: email senders, attendee lists, the client's legal name, and the terms file the Rules agent writes.
"""
import json
import re
from pathlib import Path

PATTERNS = {
    "email": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "phone": r"\+91[\s\d X]{8,}",
    "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "url_or_repo": r"(?:https?|rtsp|sap-pi)://\S+|github\.com/\S+",
    "tax_id": r"\bGSTIN\s*\S+",
    "po_or_contract_no": r"\b45\d{8}\b|ACWL[-/][A-Z/\-\d]+|CAPEX/[\w/-]+|PC/26-27/\d+",
    "capacity": r"\b\d+(?:\.\d+)?\s*(?:MTPA|million-tonne)",
    "camera_id": r"\b(?:PK\d|CV-TP|KL-IN|CM3|ST)-\d{2}\b",
}


def scan_text(index, terms):
    hits = []
    for d in index.values():
        if d["kind"] != "text":
            continue
        for n, line in enumerate(d["lines"], 1):
            for kind, pat in PATTERNS.items():
                for m in re.finditer(pat, line):
                    hits.append({"doc": d["id"], "line": n, "kind": kind, "match": m.group(0)[:80]})
            for t in terms:
                if re.search(rf"\b{re.escape(t['term'])}\b", line, re.I):
                    hits.append({"doc": d["id"], "line": n, "kind": t["category"], "match": t["term"]})
    return hits


def scan_images(index):
    hits = []
    for d in index.values():
        if d["kind"] != "image":
            continue
        meta = d["meta"]
        if meta["gps"]:
            hits.append({"doc": d["id"], "line": 0, "kind": "image_gps", "match": json.dumps(meta["gps"])[:80]})
        for k, v in meta["exif"].items():
            hits.append({"doc": d["id"], "line": 0, "kind": f"image_exif_{k}", "match": v[:80]})
        for k, v in meta["info"].items():
            hits.append({"doc": d["id"], "line": 0, "kind": f"image_info_{k}", "match": v[:80]})
        hits.append({"doc": d["id"], "line": 0, "kind": "image_pixels_need_human_review", "match": d["path"]})
    return hits


def banned_terms(terms):
    """Terms that must never appear in anything leaving the building (used by the verifier)."""
    return sorted({t["term"] for t in terms if t.get("banned", True)}, key=len, reverse=True)


def run(index, terms_path: Path, out: Path):
    terms = json.loads(terms_path.read_text(encoding="utf-8"))["terms"]
    hits = scan_text(index, terms) + scan_images(index)
    (out / "exposure_hits.json").write_text(json.dumps(hits, indent=1, ensure_ascii=False), encoding="utf-8")
    summary = {}
    for h in hits:
        summary.setdefault(h["kind"], set()).add(h["match"])
    rows = ["# Exposure scan (machine pass)", "", f"{len(hits)} hits across the library.", "",
            "| Category | Distinct values (first 8) |", "| --- | --- |"]
    for k, v in sorted(summary.items()):
        rows.append(f"| {k} | {'; '.join(sorted(v)[:8]).replace('|', '/')} |")
    (out / "exposure_scan.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return hits
