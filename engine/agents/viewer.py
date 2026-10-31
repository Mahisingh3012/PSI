"""Viewer. Renders one run into a single self-contained HTML page for reviewers (runs/<project>/viewer.html).

Overview dashboard (headline KPIs, agent chain with live status, approval gate, project register, how the run
answers the judging criteria), then one tab per output. Every citation is a chip: [Dnn:Lx] shows the file and the
exact source lines, [C:id] shows the calculation and its working. Reads everything from disk, so it is rebuilt
after every step (build, approve, release, withdraw).
"""
import base64
import html
import json
import re
from pathlib import Path

import markdown

from . import gate
from .register import STATUS_TEXT
from .verify import CITE

SECTIONS = [
    ("spine", "Story spine", "agent_outputs/01_story_spine.md"),
    ("results", "Results sheet", "agent_outputs/02_results_sheet.md"),
    ("ledger", "Calculations", "calc_ledger.md"),
    ("exposure", "Exposure", "agent_outputs/03_exposure_report.md"),
    ("case", "Case study", "agent_outputs/04_case_study.md"),
    ("media", "Media pack", None),
    ("approval", "Approval request", "agent_outputs/06_approval_request.md"),
    ("verifier", "Verifier", "verifier_report.md"),
    ("log", "Run log", "run_log.txt"),
]

CHAIN = [  # (log tag, name, kind, job)
    ("[1 librarian]", "Librarian", "code", "Indexes every file and line so anything can be cited"),
    ("[2 rules]", "Rules reader", "LLM", "Reads the contract first: what may be said, who approves, banned terms"),
    ("[3 results-spec]", "Results spec", "LLM", "Picks the signed KPI definitions, baselines and windows"),
    ("[4 calculator]", "Calculator", "code", "Computes every number from raw data, with working"),
    ("[5 exposure]", "Exposure", "code+LLM", "Finds identifiers, incl. GPS hidden in images and combination risks"),
    ("[6 writer", "Writers", "LLM", "Story spine, results, exposure report, 3-reader case study, approval request"),
    ("[6 media]", "Media", "code", "Charts, diagram, illustration, ROI calculator; metadata stripped"),
    ("[7 verifier]", "Verifier", "code", "Refuses untraceable lines, wrong numbers, identifiers, unmarked estimates"),
    ("[8 gate]", "Gate", "code", "Hashes the pack and stops until the right people approve"),
]

RUBRIC = [
    ("Agentic workflow", "spine", "8 agents with single jobs; LLM judges, code counts and checks; verifier refuses, fixer loop, human gate.",
     ["Run log", "Verifier", "Calculations"]),
    ("Business understanding", "results", "Promised vs signed vs delivered; signed KPIs recomputed exactly; missed targets shown; credit shared; refused numbers listed.",
     ["Story spine", "Results sheet"]),
    ("Buyer psychology", "case", "Same facts told for gatekeeper, user, buyer and champion; approval request makes yes easy and safe.",
     ["Case study", "Approval request", "Media pack"]),
    ("Process design", "approval", "Two approval stops, right signatories, notice period, no / withdrawal handling, hash-bound records, project register.",
     ["Approval request", "Run log"]),
]

CSS = """
:root{--bg:#f6f7fb;--panel:#fff;--ink:#0f172a;--muted:#64748b;--line:#e5e7eb;--acc:#2563eb;--acc-soft:#eff4ff;--ok:#047857;--ok-soft:#ecfdf5;
--bad:#b91c1c;--bad-soft:#fef2f2;--warn:#b45309;--warn-soft:#fffbeb;--shadow:0 1px 2px rgba(15,23,42,.06),0 4px 16px rgba(15,23,42,.05)}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0b1020;--panel:#121a2b;--ink:#e5e9f2;--muted:#94a3b8;--line:#22304a;--acc:#7aa2ff;--acc-soft:#17223a;
--ok:#34d399;--ok-soft:#0d2b22;--bad:#f87171;--bad-soft:#2d1416;--warn:#fbbf24;--warn-soft:#2b220e;--shadow:none}}
:root[data-theme=dark]{--bg:#0b1020;--panel:#121a2b;--ink:#e5e9f2;--muted:#94a3b8;--line:#22304a;--acc:#7aa2ff;--acc-soft:#17223a;
--ok:#34d399;--ok-soft:#0d2b22;--bad:#f87171;--bad-soft:#2d1416;--warn:#fbbf24;--warn-soft:#2b220e;--shadow:none}
*{box-sizing:border-box}html,body{margin:0}body{background:var(--bg);color:var(--ink);font:15px/1.55 Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--panel);border-bottom:1px solid var(--line);box-shadow:var(--shadow)}
.bar{max-width:1240px;margin:0 auto;padding:12px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.brand{font-weight:700;font-size:16px;margin-right:auto}.brand small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.pill{font-size:12px;padding:3px 10px;border-radius:99px;border:1px solid var(--line);white-space:nowrap}
.pill.ok{color:var(--ok);background:var(--ok-soft);border-color:transparent}.pill.bad{color:var(--bad);background:var(--bad-soft);border-color:transparent}
.pill.warn{color:var(--warn);background:var(--warn-soft);border-color:transparent}
nav{max-width:1240px;margin:0 auto;padding:0 16px 10px;display:flex;gap:4px;overflow-x:auto}
nav button{font:inherit;font-size:13px;padding:6px 12px;border-radius:8px;border:0;background:transparent;color:var(--muted);cursor:pointer;white-space:nowrap}
nav button:hover{background:var(--acc-soft);color:var(--ink)}nav button.on{background:var(--acc);color:#fff}
#theme{font:inherit;font-size:12px;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:8px;padding:4px 8px;cursor:pointer}
main{max-width:1240px;margin:0 auto;padding:20px 16px 48px}section{display:none}section.on{display:block}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px;box-shadow:var(--shadow);overflow-x:auto}
.doc{max-width:1100px}h2.t{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:28px 0 10px}
.hero{display:grid;gap:6px;margin-bottom:8px}.hero h1{font-size:26px;line-height:1.25;margin:0}.hero p{margin:0;color:var(--muted);max-width:820px}
.grid{display:grid;gap:12px}.k{grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}.c3{grid-template-columns:repeat(auto-fill,minmax(270px,1fr))}
.kpi .lbl{font-size:13px;color:var(--muted)}.kpi .val{font-size:clamp(20px,2.1vw,27px);font-weight:700;margin:4px 0;font-variant-numeric:tabular-nums;white-space:nowrap}
nav{scrollbar-width:none}nav::-webkit-scrollbar{display:none}
.kpi .val .arrow{color:var(--muted);font-weight:400;font-size:20px;margin:0 6px}.kpi .meta{display:flex;gap:6px;align-items:center;flex-wrap:wrap;font-size:12px;color:var(--muted)}
.chain{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;counter-reset:a}
.agent{position:relative;padding:12px 14px;border-radius:12px;border:1px solid var(--line);background:var(--panel)}
.agent b{display:block;font-size:14px}.agent .job{font-size:12px;color:var(--muted);margin:4px 0 8px}.agent .msg{font-size:11px;color:var(--muted);font-family:ui-monospace,Consolas,monospace;word-break:break-word}
.tag{font-size:10px;font-weight:600;letter-spacing:.04em;padding:1px 6px;border-radius:4px;margin-left:6px;vertical-align:middle}
.tag.code{background:var(--acc-soft);color:var(--acc)}.tag.LLM,.tag.code\\+LLM{background:var(--warn-soft);color:var(--warn)}
.rub h3{margin:0 0 4px;font-size:15px}.rub p{margin:0 0 8px;font-size:13px;color:var(--muted)}.linkbtn{font:inherit;font-size:12px;border:1px solid var(--line);background:var(--bg);color:var(--acc);border-radius:6px;padding:2px 8px;cursor:pointer;margin:0 4px 4px 0}
table{border-collapse:collapse;font-size:13px;margin:8px 0;width:100%}th,td{border-bottom:1px solid var(--line);padding:8px 10px;vertical-align:top;text-align:left}
th{color:var(--muted);font-weight:600;font-size:12px;background:var(--bg)}tr:hover td{background:var(--acc-soft)}
.doc h1{font-size:22px}.doc h2{font-size:18px;margin-top:28px}.doc h3{font-size:15px}
.cite{display:inline-block;font-size:11px;line-height:1.6;padding:0 6px;margin:1px;border-radius:5px;background:var(--acc-soft);color:var(--acc);cursor:help;white-space:nowrap;position:relative;font-family:ui-monospace,Consolas,monospace}
.cite.calc{background:var(--ok-soft);color:var(--ok)}
.cite .tip{display:none;position:absolute;left:0;top:1.8em;z-index:9;width:min(520px,80vw);white-space:pre-wrap;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:10px 12px;font:12px/1.5 system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.cite:hover .tip,.cite:focus .tip{display:block}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px}.gallery figure{margin:0;border:1px solid var(--line);border-radius:12px;padding:10px;background:#fff}
.gallery img{width:100%;height:auto;display:block}.gallery figcaption{font-size:12px;color:#334155;margin-top:6px}pre{white-space:pre-wrap;font-size:12px}
.hint{font-size:12px;color:var(--muted)}.legend{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 10px}
.gate{display:flex;gap:8px;align-items:stretch;flex-wrap:wrap}.step{flex:1;min-width:180px;border:1px solid var(--line);border-radius:12px;padding:10px 12px;background:var(--panel)}
.step b{display:block;font-size:13px}.step span{font-size:12px;color:var(--muted)}
@media (max-width:640px){.hero h1{font-size:21px}.kpi .val{font-size:24px}}
"""


def _tip_doc(index, doc, a, b):
    d = index.get(doc)
    if not d or "lines" not in d:
        return f"{doc}: not a text file"
    b = b or a
    body = "\n".join(f"L{i}: {d['lines'][i - 1]}" for i in range(int(a), int(b) + 1) if i <= len(d["lines"]))
    return f"{d['path']}\n\n{body}"


def _tip_calc(ledger, cid):
    c = ledger.get(cid)
    if not c:
        return f"{cid}: unknown calculation"
    flag = "ASSUMED\n" if c["assumed"] else ""
    return f"{flag}{c['label']}\n= {c['display']}\n\nWorking: {c['working']}\nSource: {c['source']} {json.dumps(c['filters']) if c['filters'] else ''}\n{c['note']}"


def _render(text, index, ledger):
    chips = []

    def chip(m):
        doc, a, b, calc = m.groups()
        if calc:
            label, tip, cls = f"C:{calc}", _tip_calc(ledger, calc), "cite calc"
        else:
            label, tip, cls = f"{doc}:L{a}{'-' + b if b else ''}", _tip_doc(index, doc, a, b), "cite"
        chips.append(f'<span class="{cls}" tabindex="0">{html.escape(label)}<span class="tip" aria-hidden="true">{html.escape(tip)}</span></span>')
        return f"@@CHIP{len(chips) - 1}@@"

    text = CITE.sub(chip, text).replace("[NO-CLAIM]", "")
    out = markdown.markdown(text, extensions=["tables"])
    return re.sub(r"@@CHIP(\d+)@@", lambda m: chips[int(m.group(1))], out)


def _kpis(run, ledger):
    spec_f = run / "agent_outputs" / "03_metric_spec.json"
    heads = json.loads(spec_f.read_text(encoding="utf-8")).get("headline", []) if spec_f.exists() else []
    cards = []
    cls = {"met": "ok", "held": "ok", "missed": "warn"}
    for h in heads:
        if h.get("to") not in ledger:
            continue
        val = ledger[h["to"]]["display"]
        if h.get("from") in ledger:
            val = f"{ledger[h['from']]['display']}<span class='arrow'>&rarr;</span>{val}"
        delta = f" ({ledger[h['delta']]['display']})" if h.get("delta") in ledger else ""
        tgt = f"<span>target {html.escape(h['target'])}</span>" if h.get("target") else ""
        cards.append(f"<div class='card kpi'><div class='lbl'>{html.escape(h['label'])}{delta}</div><div class='val'>{val}</div>"
                     f"<div class='meta'><span class='pill {cls.get(h.get('status'), '')}'>{html.escape(h.get('status', ''))}</span>{tgt}"
                     f"<span>{html.escape(h.get('note', ''))}</span></div></div>")
    return "".join(cards)


def _chain(run):
    log = (run / "run_log.txt").read_text(encoding="utf-8") if (run / "run_log.txt").exists() else ""
    out = []
    for tag, name, kind, job in CHAIN:
        lines = [ln.split("] ", 1)[-1] for ln in log.splitlines() if tag in ln]
        mode = "RECORDED" if any("RECORDED" in ln for ln in lines) else ("LIVE" if any("LIVE" in ln for ln in lines) else ("ran" if lines else "not run"))
        status = {"RECORDED": "warn", "LIVE": "ok", "ran": "ok"}.get(mode, "bad")
        msg = lines[-1][:140] if lines else "-"
        if tag == "[7 verifier]" and lines and "REFUSED" in log:
            status, mode = "bad", "refused"
        out.append(f"<div class='agent'><b>{name}<span class='tag {kind}'>{kind}</span></b><div class='job'>{job}</div>"
                   f"<span class='pill {status}'>{mode}</span><div class='msg'>{html.escape(msg)}</div></div>")
    return "".join(out)


def _gate(run, required_roles):
    steps = [("Verifier", "pack assembled" if (run / "pack").exists() else "refused: no pack", (run / "pack").exists())]
    for stage, roles in required_roles.items():
        ok, why = gate.check(run / "pack", run / "approvals" / f"{stage}.json", roles) if (run / "pack").exists() else (False, ["no pack"])
        who = ", ".join(r.replace("_", " ") for r in roles)
        detail = (f"approved by {who}" if ok else f"waiting for a person: {who}" if "no approval record" in why[0]
                  else re.sub(r"STOP: |\(.*?\)", "", why[0]).strip())
        steps.append((f"{stage.title()} approval", detail, ok))
    return "".join(f"<div class='step'><b>{'&#10003;' if ok else '&#9632;'} {html.escape(t)}</b><span class='pill {'ok' if ok else 'bad'}'>"
                   f"{'pass' if ok else 'stopped'}</span><br><span>{html.escape(d[:110])}</span></div>" for t, d, ok in steps)


def _register(run):
    f = run.parent / "register.json"
    if not f.exists():
        return "<p class='hint'>No register yet.</p>"
    reg = json.loads(f.read_text(encoding="utf-8"))
    rows = "".join(f"<tr><td>{html.escape(k)}</td><td>{html.escape(STATUS_TEXT.get(v['status'], v['status']))}</td><td>{v.get('verifier_problems', '-')}</td>"
                   f"<td>{html.escape(v['history'][-1]['event'])}</td><td>{html.escape(v['updated'])}</td></tr>" for k, v in sorted(reg.items()))
    return f"<table><tr><th>Project</th><th>Status</th><th>Verifier problems</th><th>Last event</th><th>Updated</th></tr>{rows}</table>"


def build(run: Path, required_roles):
    index = json.loads((run / "evidence_index.json").read_text(encoding="utf-8"))
    ledger = json.loads((run / "calc_ledger.json").read_text(encoding="utf-8")) if (run / "calc_ledger.json").exists() else {}
    vr = (run / "verifier_report.md").read_text(encoding="utf-8") if (run / "verifier_report.md").exists() else ""
    problems = len(re.findall(r"^- ", vr, re.M))
    pills = [f'<span class="pill">{len(index)} files</span>', f'<span class="pill">{len(ledger)} numbers</span>',
             f'<span class="pill {"ok" if problems == 0 else "bad"}">verifier: {"0 problems" if problems == 0 else f"refused {problems}"}</span>']
    for stage, roles in required_roles.items():
        ok = (run / "pack").exists() and gate.check(run / "pack", run / "approvals" / f"{stage}.json", roles)[0]
        pills.append(f'<span class="pill {"ok" if ok else "bad"}">{stage}: {"approved" if ok else "stopped"}</span>')

    rubric = "".join(
        f"<div class='card rub'><h3>{t}</h3><p>{d}</p>" + "".join(
            f"<button class='linkbtn' data-go='{next(s for s, n, _ in SECTIONS if n == lbl)}'>{lbl}</button>" for lbl in links) + "</div>"
        for t, _, d, links in RUBRIC)
    overview = f"""<div class='hero'><h1>From an 8-month project folder to a case study the client can sign</h1>
<p>Every sentence below is traced to a file and line or to a calculation. Numbers are computed by code, not by the language model.
Nothing leaves until the client's authorised approvers say yes.</p></div>
<h2 class='t'>Headline results (signed definitions)</h2><div class='grid k'>{_kpis(run, ledger) or "<p class='hint'>No headline list in the metric spec.</p>"}</div>
<h2 class='t'>The agent chain</h2><div class='chain'>{_chain(run)}</div>
<h2 class='t'>Approval gate</h2><div class='gate'>{_gate(run, required_roles)}</div>
<h2 class='t'>How this run answers the judging criteria</h2><div class='grid c3'>{rubric}</div>
<h2 class='t'>Project register (all projects)</h2><div class='card'>{_register(run)}</div>"""

    nav = ['<button data-s="overview" class="on">Overview</button>']
    secs = [f'<section id="overview" class="on">{overview}</section>']
    for sid, title, rel in SECTIONS:
        nav.append(f'<button data-s="{sid}">{title}</button>')
        if sid == "media":
            figs = []
            for p in sorted((run / "media").glob("*")) if (run / "media").exists() else []:
                # embedded so the viewer is one self-contained file
                if p.suffix == ".png":
                    data = base64.b64encode(p.read_bytes()).decode()
                    figs.append(f'<figure><img src="data:image/png;base64,{data}" alt="{p.stem}"><figcaption>{p.name}</figcaption></figure>')
                elif p.suffix == ".html":
                    figs.append(f'<figure><iframe title="{p.stem}" srcdoc="{html.escape(p.read_text(encoding="utf-8"))}" '
                                f'style="width:100%;height:640px;border:0"></iframe><figcaption>{p.name} (interactive)</figcaption></figure>')
            body = ('<p class="hint">Made from data only, never from client photos. File metadata stripped and checked by the verifier.</p>'
                    '<div class="gallery">' + "".join(figs) + "</div>")
        else:
            f = run / rel
            if not f.exists():
                body = "<p>Not produced in this run.</p>"
            elif rel.endswith(".txt"):
                body = f"<pre>{html.escape(f.read_text(encoding='utf-8'))}</pre>"
            else:
                body = ("<div class='legend hint'><span class='cite'>D06:L45</span> source line "
                        "<span class='cite calc'>C:k1_final</span> calculation &mdash; hover or tab to see it</div>"
                        + _render(f.read_text(encoding="utf-8"), index, ledger))
        secs.append(f'<section id="{sid}"><div class="card doc">{body}</div></section>')

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Case Study Pack</title><style>{CSS}</style></head><body>
<header><div class="bar"><div class="brand">Case Study Engine<small>run: {html.escape(run.name)}</small></div>{''.join(pills)}
<button id="theme" title="Toggle light/dark">Theme</button></div><nav>{''.join(nav)}</nav></header>
<main>{''.join(secs)}</main>
<script>
const show=s=>{{document.querySelectorAll('nav button,section').forEach(e=>e.classList.remove('on'));
 document.querySelector('nav button[data-s="'+s+'"]').classList.add('on');document.getElementById(s).classList.add('on');
 scrollTo(0,0);try{{localStorage.setItem('tab',s)}}catch(e){{}}}};
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>show(b.dataset.s));
document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>show(b.dataset.go));
const flip=e=>{{const c=e.currentTarget,t=c.querySelector('.tip'),r=c.getBoundingClientRect();
 const right=r.left>innerWidth/2;t.style.left=right?'auto':'0';t.style.right=right?'0':'auto';}};
document.querySelectorAll('.cite').forEach(c=>{{c.addEventListener('mouseenter',flip);c.addEventListener('focus',flip)}});
const root=document.documentElement;
document.getElementById('theme').onclick=()=>{{const d=matchMedia('(prefers-color-scheme: dark)').matches;
 const cur=root.dataset.theme||(d?'dark':'light');root.dataset.theme=cur==='dark'?'light':'dark';try{{localStorage.setItem('theme',root.dataset.theme)}}catch(e){{}}}};
try{{const th=localStorage.getItem('theme');if(th)root.dataset.theme=th;const t=localStorage.getItem('tab');if(t&&document.getElementById(t))show(t)}}catch(e){{}}
</script></body></html>"""
    (run / "viewer.html").write_text(page, encoding="utf-8")
    return run / "viewer.html"
