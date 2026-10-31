"""Engine checks. Run: python -m pytest -q tests   (or: python tests/test_engine.py)"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from agents import calc, exposure, gate, ingest, verify  # noqa: E402

LIB = next(p for p in [ROOT / "library" / "Project_Drishti_Library", ROOT.parent / "Project_Drishti_Library" / "Project_Drishti_Library"] if p.is_dir())
SPEC = json.loads((ROOT / "runs/drishti/agent_outputs/03_metric_spec.json").read_text(encoding="utf-8"))
TERMS = json.loads((ROOT / "runs/drishti/agent_outputs/02_rules_and_terms.json").read_text(encoding="utf-8"))["terms"]
INDEX = ingest.build_index(LIB)
LEDGER = calc.run_spec(LIB, SPEC)
BANNED = exposure.banned_terms(TERMS)


def test_01_calculator_reproduces_signed_certificate():
    """Every pilot KPI recomputed from raw data equals the signed acceptance certificate."""
    want = {"k1_base": "68.9%", "k1_final": "91.1%", "k2_base": "5.58", "k2_final": "3.00", "k2_change": "-46%",
            "k3_final_alertw": "4.9 min", "k3_last_week": "3.5 min", "k4_final": "9.7%", "walk_q4": "73.8%"}
    for k, v in want.items():
        assert LEDGER[k]["display"] == v, (k, LEDGER[k]["display"], v)


def test_02_refuses_the_sales_teams_headline():
    """REFUSE: '74% to 97%' cites real files but the numbers are not what those lines say."""
    claim = "PPE compliance rose from 74% to 97%. [C:k1_base] [C:k1_final]"
    problems = verify.verify(claim, INDEX, LEDGER)
    assert any(p[1] == "NUMBER_NOT_IN_SOURCE" and p[2] == "74" for p in problems)
    assert any(p[1] == "NUMBER_NOT_IN_SOURCE" and p[2] == "97" for p in problems)


def test_03_refuses_uncited_sentence_and_bad_citation():
    problems = verify.verify("Zero LTIs since go-live thanks to AI.\nSaved 2.3 crore. [D99:L1]", INDEX, LEDGER)
    kinds = {p[1] for p in problems}
    assert "UNTRACEABLE" in kinds and "BAD_CITE" in kinds


def test_04_refuses_identifier_in_outward_text():
    line = "The Bhadrapur plant raised compliance to 91%. [C:k1_final]"
    assert any(p[1] == "EXPOSURE" for p in verify.verify(line, INDEX, LEDGER, BANNED, outward=True))
    assert not verify.verify(line, INDEX, LEDGER, BANNED, outward=False)  # fine in internal docs


def test_05_assumed_number_must_cite_assumed_calc():
    bad = "ASSUMED payback 26 months. [D21:L31]"
    good = "ASSUMED payback 26 months. [C:payback_half_noamc]"
    assert any(p[1] == "ASSUMED_WITHOUT_CALC" for p in verify.verify(bad, INDEX, LEDGER))
    assert not verify.verify(good, INDEX, LEDGER)


def test_06_exposure_finds_gps_in_snapshot_and_secrets_in_repo():
    hits = exposure.scan_images(INDEX) + exposure.scan_text(INDEX, TERMS)
    kinds = {(h["doc"], h["kind"]) for h in hits}
    snap = next(k for k, v in INDEX.items() if v["path"].endswith(".jpg"))
    assert (snap, "image_gps") in kinds
    assert any(h["kind"] == "url_or_repo" and h["match"].startswith("rtsp://") for h in hits)


def _pack(tmp):
    pack = tmp / "pack"
    pack.mkdir()
    (pack / "case_study.md").write_text("text", encoding="utf-8")
    return pack


def _approval(tmp, pack, approvals, sent="2026-11-02", first_use="2026-11-20"):
    f = tmp / "client.json"
    f.write_text(json.dumps({"pack_sha256": gate.pack_hash(pack), "approvals": approvals,
                             "sent_for_review_on": sent, "first_use_date": first_use}), encoding="utf-8")
    return f


ROLES = ["client_corporate_communications", "client_legal"]


def test_07_stops_for_a_person():
    """STOP: no approval record -> nothing leaves."""
    tmp = Path(tempfile.mkdtemp())
    ok, why = gate.check(_pack(tmp), tmp / "client.json", ROLES)
    assert not ok and "STOP" in why[0]


def test_08_plant_head_on_whatsapp_is_not_enough():
    tmp = Path(tempfile.mkdtemp())
    pack = _pack(tmp)
    f = _approval(tmp, pack, [{"role": "unit_head", "decision": "approve", "channel": "whatsapp"}])
    ok, why = gate.check(pack, f, ROLES)
    assert not ok and any("client_legal" in w for w in why)


def test_09_edit_after_approval_and_short_notice_and_withdrawal_all_stop():
    tmp = Path(tempfile.mkdtemp())
    pack = _pack(tmp)
    good = [{"role": r, "decision": "approve_anonymised"} for r in ROLES]
    f = _approval(tmp, pack, good)
    assert gate.check(pack, f, ROLES)[0]
    (pack / "case_study.md").write_text("text edited after approval", encoding="utf-8")
    assert not gate.check(pack, f, ROLES)[0]
    f = _approval(tmp, pack, good, sent="2026-11-02", first_use="2026-11-06")
    assert not gate.check(pack, f, ROLES)[0]
    f = _approval(tmp, pack, [dict(a, withdrawn_on="2027-01-10") for a in good])
    assert not gate.check(pack, f, ROLES)[0]


def test_10_runs_on_a_different_project_library_unchanged():
    """A made-up SaaS project: different files, different KPI; same code, only a new spec."""
    tmp = Path(tempfile.mkdtemp())
    (tmp / "data").mkdir()
    (tmp / "data/releases.csv").write_text("week,deploys,failed\n1,10,3\n2,12,3\n3,20,2\n4,22,1\n", encoding="utf-8")
    (tmp / "sow.md").write_text("Target: change failure rate below 10% by week 4.\n", encoding="utf-8")
    idx = ingest.build_index(tmp)
    spec = {"calcs": [
        {"id": "cfr_base", "label": "CFR wk1-2", "op": "ratio_of_sums", "file": "data/releases.csv",
         "where": {"week": {"between": [1, 2]}}, "num": "failed", "den": "deploys", "scale": 100, "unit": "%"},
        {"id": "cfr_end", "label": "CFR wk3-4", "op": "ratio_of_sums", "file": "data/releases.csv",
         "where": {"week": {"between": [3, 4]}}, "num": "failed", "den": "deploys", "scale": 100, "unit": "%"}]}
    led = calc.run_spec(tmp, spec)
    assert led["cfr_base"]["display"] == "27.3%" and led["cfr_end"]["display"] == "7.1%"
    assert not verify.verify("Change failure rate fell from 27.3% to 7.1%, under the 10% target. [C:cfr_base] [C:cfr_end] [D02:L1]",
                             idx, led)
    shutil.rmtree(tmp)


def test_11_catches_drifted_citation_and_unmarked_estimate():
    """REFUSE: a citation pointing at an unrelated line, and an estimate presented as fact."""
    drifted = "The client's Legal team stopped face recognition. [D15:L13]"  # D15:L13 is about dusty cameras
    assert any(p[1] == "WEAK_CITE" for p in verify.verify(drifted, INDEX, LEDGER))
    unmarked = "Detention fell to 3.9 lakh a month. [C:det_sep]"
    assert any(p[1] == "ASSUMED_NOT_MARKED" for p in verify.verify(unmarked, INDEX, LEDGER))
    assert not verify.verify("ASSUMED: detention fell to 3.9 lakh a month. [C:det_sep]", INDEX, LEDGER)
    clean = verify.strip_citations(
        "| Question | Answer | Source |\n| --- | --- | --- |\n| Internet? | None from the edge | [D02:L42] |\n"
    )
    assert "[D02" not in clean and "[C:" not in clean and "[NO-CLAIM]" not in clean
    assert "Source" not in clean
    assert "None from the edge" in clean


def test_12_register_records_a_no_and_keeps_history():
    """STOP: a client 'reject' is releasable by no one, and the register keeps the full history."""
    from agents import register
    tmp = Path(tempfile.mkdtemp())
    register.update(tmp, "p1", "awaiting_internal", "build passed", pack_sha256="abc")
    register.update(tmp, "p1", "declined", "client: client_legal said no (wait for audit)")
    rec = register.get(tmp, "p1")
    assert rec["status"] == "declined" and len(rec["history"]) == 2 and (tmp / "register.md").exists()
    pack = _pack(tmp)
    f = _approval(tmp, pack, [{"role": r, "decision": "reject" if r == "client_legal" else "approve_anonymised"} for r in ROLES])
    assert not gate.check(pack, f, ROLES)[0]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}: {fn.__doc__.strip().splitlines()[0] if fn.__doc__ else ''}")
        except AssertionError as e:
            print(f"FAIL {fn.__name__}: {e}")
