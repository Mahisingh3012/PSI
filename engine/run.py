"""Case Study Engine - orchestrator.

  python engine/run.py build   --library <folder> --project <name>     # agents 1-7, stops at the human gate
  python engine/run.py approve  --project <name> --stage internal|client --role R --name N --decision D  # a person decides
  python engine/run.py release  --project <name> --stage internal|client # agent 8: refuses without approvals
  python engine/run.py withdraw --project <name> --stage client --role R --date YYYY-MM-DD           # MSA 15.4

Chain (each agent has one job; judgement agents have a prompt in engine/prompts, the rest are code):
  1 Librarian (code)      index every file/line so anything can be cited
  2 Rules (LLM)           read contract/NDA first -> publicity rules + banned/identifying terms
  3 Results spec (LLM)    decide KPI definitions, baselines, windows -> metric_spec.json
  4 Calculator (code)     compute every number from raw data, with working -> calc_ledger
  5 Exposure (code + LLM) scan for identifiers incl. image metadata, judge combinations -> exposure report
  6 Timeline + Writer (LLM) story spine, results sheet, 3-reader case study, approval request (all cited)
  7 Verifier (code)       refuse any line/number it cannot trace; refuse identifiers in outward text
  8 Gate (code)           hash the pack; nothing is sent or published without recorded human approvals
  + Fixer (LLM, live mode) gets refused lines back from the verifier, up to 2 rounds
  + Register (code)       runs/register.json|md: status and history of every project (records, many projects)
"""
import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image  # noqa: E402

from agents import calc, exposure, gate, ingest, llm, media, register, verify, viewer  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
PROMPTS = Path(__file__).parent / "prompts"
MAX_FIX_ROUNDS = 2
# Where the library is looked for when --library is not given (first match wins).
LIBRARY_CANDIDATES = [ROOT / "library" / "Project_Drishti_Library", ROOT.parent / "Project_Drishti_Library" / "Project_Drishti_Library"]

# Writer outputs that are checked line by line; the ones marked outward must also be free of identifiers.
DRAFTS = {
    "01_story_spine.md": False,
    "02_results_sheet.md": False,
    "03_exposure_report.md": False,
    "04_case_study.md": True,
    "06_approval_request.md": False,
}


def build(args):
    run = ROOT / "runs" / args.project
    ao = run / "agent_outputs"
    ao.mkdir(parents=True, exist_ok=True)
    log_lines = []

    def log(msg):
        line = f"{datetime.now():%H:%M:%S} {msg}"
        print(line)
        log_lines.append(line)

    library = Path(args.library) if args.library else next((p for p in LIBRARY_CANDIDATES if p.is_dir()), None)
    if not library or not library.is_dir():
        print("No library found. Pass --library <folder> or unzip it to library/Project_Drishti_Library (see DATA.md).")
        return 4
    index = ingest.build_index(library)
    ingest.write_index(index, run)
    log(f"[1 librarian] indexed {len(index)} files")
    ctx = (run / "evidence_index.md").read_text(encoding="utf-8") + "\n\n" + json.dumps(
        {k: {"path": v["path"], "lines": v.get("lines"), "meta": v.get("meta")} for k, v in index.items()}, ensure_ascii=False)

    llm.run_agent("2 rules", PROMPTS / "02_rules.md", ctx, ao / "02_rules_and_terms.json", log)
    llm.run_agent("3 results-spec", PROMPTS / "03_results_spec.md", ctx, ao / "03_metric_spec.json", log)
    spec = json.loads((ao / "03_metric_spec.json").read_text(encoding="utf-8"))
    ledger = calc.run_spec(library, spec)
    calc.write_ledger(ledger, run)
    log(f"[4 calculator] {len(ledger)} numbers computed with working -> calc_ledger.md")

    hits = exposure.run(index, ao / "02_rules_and_terms.json", run)
    log(f"[5 exposure] machine pass: {len(hits)} hits -> exposure_scan.md")
    ctx2 = ctx + "\n\nCALC LEDGER\n" + (run / "calc_ledger.md").read_text(encoding="utf-8") + "\n\nEXPOSURE SCAN\n" + (
        run / "exposure_scan.md").read_text(encoding="utf-8")
    for name, prompt in [("01_story_spine.md", "06_timeline.md"), ("02_results_sheet.md", "06_results_sheet.md"),
                         ("03_exposure_report.md", "05_exposure.md"), ("04_case_study.md", "06_writer.md"),
                         ("06_approval_request.md", "06_approval.md")]:
        llm.run_agent(f"6 writer:{name}", PROMPTS / prompt, ctx2, ao / name, log)

    assets = media.build(library, run / "media")
    log(f"[6 media] {len(assets)} assets made from data, metadata stripped: {', '.join(assets)}")

    terms = json.loads((ao / "02_rules_and_terms.json").read_text(encoding="utf-8"))["terms"]
    banned = exposure.banned_terms(terms)
    failed, by_draft = verify_all(run, ao, index, ledger, banned)
    log(f"[7 verifier] {failed} untraceable/unsafe items -> verifier_report.md")
    # Writer <-> verifier loop: in live mode the fixer agent gets the refused lines back, at most MAX_FIX_ROUNDS times.
    for rnd in range(1, MAX_FIX_ROUNDS + 1):
        if not failed or not llm.live():
            break
        for name, problems in by_draft.items():
            if problems:
                listing = "\n".join(f"line {n}: {kind} {what}" for n, kind, what, _ in problems)
                llm.run_agent(f"7 fixer:{name} round {rnd}", PROMPTS / "07_fix.md",
                              ctx2 + f"\n\nDRAFT {name}\n" + (ao / name).read_text(encoding="utf-8") + "\n\nVERIFIER PROBLEMS\n" + listing,
                              ao / name, log)
        failed, by_draft = verify_all(run, ao, index, ledger, banned)
        log(f"[7 verifier] after fix round {rnd}: {failed} problems")

    pack = run / "pack"
    if pack.exists():
        shutil.rmtree(pack)  # an older pack must never stay releasable after a refused rebuild
    if failed:
        log("[7 verifier] REFUSED: pack not assembled. Writer must fix or drop the listed lines.")
        (run / "run_log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        register.update(RUNS, args.project, "refused", f"build refused: {failed} problems",
                        library=str(library), verifier_problems=failed, pack_sha256=None)
        log(f"[viewer] open {viewer.build(run, ROLES).relative_to(ROOT)}")
        return 2

    pack.mkdir()
    for name in DRAFTS:
        shutil.copy(ao / name, pack / name)
    (pack / "04_case_study_CLEAN_for_client_review.md").write_text(
        verify.strip_citations((ao / "04_case_study.md").read_text(encoding="utf-8")), encoding="utf-8")
    shutil.copy(run / "calc_ledger.md", pack / "02b_calc_ledger.md")
    if (run / "media").exists():
        shutil.copytree(run / "media", pack / "05_media")
    (run / "pack_sha256.txt").write_text(gate.pack_hash(pack) + "\n")
    log(f"[8 gate] pack assembled, sha256 {gate.pack_hash(pack)[:16]}...; STOPPED for human approval "
        f"(python engine/run.py approve --project {args.project} --stage internal ...)")
    (run / "run_log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    register.update(RUNS, args.project, "awaiting_internal", "build passed verifier; pack assembled",
                    library=str(library), verifier_problems=0, pack_sha256=gate.pack_hash(pack))
    log(f"[viewer] open {viewer.build(run, ROLES).relative_to(ROOT)}")
    return 0


def verify_all(run, ao, index, ledger, banned):
    report, failed, by_draft = ["# Verifier report", ""], 0, {}
    for name, outward in DRAFTS.items():
        problems = verify.verify((ao / name).read_text(encoding="utf-8"), index, ledger, banned, outward)
        by_draft[name] = problems
        failed += len(problems)
        report.append(f"## {name} ({'outward: identifiers checked' if outward else 'internal'}) - {len(problems)} problems")
        report += [f"- line {n}: **{kind}** `{what}` in: {txt}" for n, kind, what, txt in problems]
    for img in (run / "media").glob("*.png"):  # media must carry no metadata
        im = Image.open(img)
        if im.getexif() or {k for k in im.info if k not in ("dpi",)}:
            failed += 1
            report.append(f"- media {img.name}: **EXPOSURE** metadata present {list(im.info)}")
    (run / "verifier_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return failed, by_draft


ROLES = {"internal": ["vendor_delivery_owner"],
         "client": ["client_corporate_communications", "client_legal"]}
DECISIONS = ["approve", "approve_named", "approve_anonymised", "approve_internal_only", "reject"]


def approve(args):
    """A person records a decision on the exact pack they reviewed (the pack hash is stored with it)."""
    run = ROOT / "runs" / args.project
    if not (run / "pack").exists():
        print("STOP: no assembled pack to approve. Run build first; the verifier must pass.")
        return 3
    f = run / "approvals" / f"{args.stage}.json"
    f.parent.mkdir(exist_ok=True)
    rec = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"approvals": []}
    h = gate.pack_hash(run / "pack")
    if rec.get("pack_sha256") not in (None, h):
        print("Pack changed since earlier approvals: earlier approvals are void and kept in history.")
        rec.setdefault("history", []).extend(rec["approvals"])
        rec["approvals"] = []
    rec["pack_sha256"] = h
    rec["approvals"] = [a for a in rec["approvals"] if a["role"] != args.role] + [{
        "role": args.role, "name": args.name, "decision": args.decision, "channel": args.channel,
        "recorded_at": datetime.now().isoformat(timespec="seconds"), "note": args.note or ""}]
    if args.sent_on:
        rec["sent_for_review_on"] = args.sent_on
    if args.first_use:
        rec["first_use_date"] = args.first_use
    f.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    print(f"Recorded: {args.role} = {args.decision} on pack {h[:16]}... -> {f.relative_to(ROOT)}")
    if args.decision == "reject":
        print(ON_NO)
        register.update(RUNS, args.project, "declined", f"{args.stage}: {args.role} said no ({args.note or 'no reason given'})")
    else:
        status = "internal_approved" if args.stage == "internal" else "with_client"
        register.update(RUNS, args.project, status, f"{args.stage}: {args.role} = {args.decision} via {args.channel}")
    return 0


ON_NO = """Decision 'reject' recorded. What happens on a no (PROCESS.md):
  - nothing is published; every asset stays internal use only; the reason is kept in the register
  - offer a smaller ask once (anonymised without numbers, or internal sales use only); never chase
  - ask again only at the next milestone (e.g. after the final audit), with a fresh build and fresh approvals"""


def withdraw(args):
    """Client withdraws approval later (MSA 15.4). The gate blocks new use from now on."""
    f = ROOT / "runs" / args.project / "approvals" / f"{args.stage}.json"
    rec = json.loads(f.read_text(encoding="utf-8"))
    for a in rec["approvals"]:
        if a["role"] == args.role:
            a["withdrawn_on"] = args.date
    f.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    print(f"Withdrawal recorded for {args.role} on {args.date}. Stop new use within 30 days.")
    register.update(RUNS, args.project, "withdrawn", f"{args.stage}: {args.role} withdrew on {args.date}")
    return 0


def release(args):
    run = ROOT / "runs" / args.project
    if args.stage == "client":  # the client never sees a pack the vendor has not checked internally
        ok, reasons = gate.check(run / "pack", run / "approvals" / "internal.json", ROLES["internal"])
        if not ok:
            for r in reasons:
                print("internal stage: " + r)
            return 3
    ok, reasons = gate.check(run / "pack", run / "approvals" / f"{args.stage}.json", ROLES[args.stage])
    for r in reasons:
        print(r)
    if any("'reject'" in r for r in reasons):
        print(ON_NO)
    if ok:
        print(f"RELEASE OK for stage '{args.stage}'. Record kept in runs/{args.project}/approvals/.")
        register.update(RUNS, args.project, "with_client" if args.stage == "internal" else "approved",
                        f"release {args.stage}: OK")
    else:
        register.update(RUNS, args.project, register.get(RUNS, args.project)["status"] if register.get(RUNS, args.project)
                        else "awaiting_internal", f"release {args.stage}: STOPPED ({len(reasons)} reasons)")
    return 0 if ok else 3


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--library", help="library folder (default: library/Project_Drishti_Library, then ../Project_Drishti_Library/...)")
    b.add_argument("--project", required=True)
    r = sub.add_parser("release")
    r.add_argument("--project", required=True)
    r.add_argument("--stage", choices=["internal", "client"], required=True)
    ap = sub.add_parser("approve")
    ap.add_argument("--project", required=True)
    ap.add_argument("--stage", choices=["internal", "client"], required=True)
    ap.add_argument("--role", required=True, help="e.g. vendor_delivery_owner, client_legal, client_corporate_communications")
    ap.add_argument("--name", required=True)
    ap.add_argument("--decision", choices=DECISIONS, required=True)
    ap.add_argument("--channel", default="email")
    ap.add_argument("--note")
    ap.add_argument("--sent-on", help="date the complete pack reached the client (YYYY-MM-DD)")
    ap.add_argument("--first-use", help="planned first publication date (YYYY-MM-DD)")
    w = sub.add_parser("withdraw")
    w.add_argument("--project", required=True)
    w.add_argument("--stage", choices=["internal", "client"], required=True)
    w.add_argument("--role", required=True)
    w.add_argument("--date", required=True)
    a = p.parse_args()
    code = {"build": build, "release": release, "approve": approve, "withdraw": withdraw}[a.cmd](a)
    if a.cmd != "build" and (ROOT / "runs" / a.project / "evidence_index.json").exists():
        viewer.build(ROOT / "runs" / a.project, ROLES)  # keep the gate status on the viewer current
    sys.exit(code)
