"""Media agent. Makes industry-fit assets from the data (never from client photos) and strips all file metadata.

Manufacturing showcase (chosen from the vendor/industry profile): before/after chart split by camera cohort,
a gate "flow" chart with the other causes marked, a generic redrawn architecture, a labelled ILLUSTRATION of an
alert (not a photo), and an ROI calculator the reader fills with their own plant numbers.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

INK, MUTED, A, B, OK, BAD = "#1f2937", "#6b7280", "#2563eb", "#d97706", "#059669", "#dc2626"
NO_META = {"Software": None}
FOOT = "Anonymised. Indian cement manufacturer. Source: vendor camera analytics export; ratio of sums per week."


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=9)


def ppe_chart(library, out):
    m = pd.read_csv(Path(library) / "07_data/viewos_weekly_zone_metrics.csv")
    g = m.groupby(["week_start", "camera_cohort"])[["persons_observed", "ppe_compliant"]].sum()
    g = (g.ppe_compliant / g.persons_observed * 100).unstack()
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    x = range(len(g))
    ax.plot(x, g["pilot"], color=A, lw=2.5, marker="o", ms=4, label="First 40 cameras (pilot areas)")
    ax.plot(x, g["scale"], color=B, lw=2.5, marker="o", ms=4, label="Cameras added from week 9 (new areas)")
    ax.axhline(90, color=MUTED, ls="--", lw=1)
    ax.text(len(g) - 0.5, 90.4, "pilot target 90%", color=MUTED, fontsize=8, ha="right")
    ax.axvspan(-0.5, 7.5, color="#eef2ff", zorder=0)
    ax.text(3.5, 61.5, "8-week pilot", color=A, fontsize=9, ha="center")
    ax.annotate("69% -> 91%\npilot KPI windows", xy=(5.5, 91), xytext=(2.2, 84), fontsize=9, color=INK,
                arrowprops={"arrowstyle": "->", "color": MUTED})
    ax.annotate("new areas start low,\nthen follow the same curve", xy=(8, 72), xytext=(9.5, 66), fontsize=9, color=INK,
                arrowprops={"arrowstyle": "->", "color": MUTED})
    ax.set_xticks(list(x), [f"W{i + 1}" for i in x])
    ax.set_ylim(60, 100)
    ax.set_ylabel("% persons observed with helmet AND vest", color=MUTED, fontsize=9)
    ax.set_title("Real PPE compliance measured all day by existing cameras", loc="left", color=INK, fontsize=13, weight="bold")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    _style(ax)
    fig.text(0.01, 0.01, FOOT, fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(out / "chart_ppe_compliance_by_cohort.png", metadata=NO_META)
    plt.close(fig)


def gate_chart(library, out):
    g = pd.read_csv(Path(library) / "07_data/gate_truck_turnaround_daily.csv", parse_dates=["date"])
    g = g[g.date >= "2026-08-03"].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150)
    ax.plot(g.index, g.avg_turnaround_min, color=A, lw=1.8)
    ax.plot(g.index, g.avg_turnaround_min.rolling(7, min_periods=1).mean(), color=INK, lw=2.5, label="7-day average")
    for day, text, ha, dx in [(15, "Client adds a\n2nd weighbridge", "right", -0.5),
                              (22, "Logistics starts dispatch\nslots from the live queue view", "left", 0.5)]:
        ax.axvline(day, color=B, ls="--", lw=1.2)
        ax.text(day + dx, 112, text, fontsize=8.5, color=B, va="top", ha=ha)
    ax.set_ylim(50, 115)
    ax.set_xticks([0, 15, 22, len(g) - 1], ["Day 1", "Day 16", "Day 23", f"Day {len(g)}"])
    ax.set_ylabel("Average truck turnaround, minutes", color=MUTED, fontsize=9)
    ax.set_title("Truck turnaround: about 88 -> 68 minutes, with credit shared", loc="left", color=INK, fontsize=13, weight="bold")
    ax.text(len(g) - 1, 54, "~6 min with the weighbridge, ~15 min after dispatch slots", fontsize=8.5, color=INK, ha="right")
    ax.legend(frameon=False, fontsize=9, loc="upper right", bbox_to_anchor=(1, 0.85))
    _style(ax)
    fig.text(0.01, 0.01, "Anonymised. Same number-plate cameras throughout (no manual register mixed in). Day 1 = gate analytics go-live.",
             fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(out / "chart_gate_turnaround_attribution.png", metadata=NO_META)
    plt.close(fig)


def architecture(out):
    fig, ax = plt.subplots(figsize=(11, 5), dpi=150)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 50)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((1, 1), 72, 44, fill=False, ec=OK, lw=2, ls="--"))
    ax.text(3, 42.5, "PLANT OT NETWORK  -  no internet egress, footage never leaves", color=OK, fontsize=9, weight="bold")
    boxes = {
        "cams": (4, 26, "Existing CCTV\n(mixed brands, no new\ncameras for PPE)"),
        "edge": (28, 26, "Edge GPU servers\nperson / helmet / vest /\nzone detection"),
        "console": (52, 26, "Console + snapshots\n(stay on site)"),
        "gate": (28, 6, "Number-plate cameras\n+ weighbridge feed\n-> live queue view"),
        "jump": (52, 6, "Client jump host\nsession-recorded,\napproved per session"),
        "phone": (82, 26, "Area in-charge phone\nTEXT-ONLY alert\n(no image)"),
        "vendor": (82, 6, "Vendor support\nsigned update packages\ninstalled by client IT"),
    }
    for x, y, t in boxes.values():
        ax.add_patch(plt.Rectangle((x, y), 19, 12, fc="#eff6ff", ec=A, lw=1.3))
        ax.text(x + 9.5, y + 6, t, ha="center", va="center", fontsize=8, color=INK)
    for (x1, y1), (x2, y2) in [((23, 32), (28, 32)), ((47, 32), (52, 32)), ((71, 32), (82, 32)), ((82, 12), (71, 12)), ((37.5, 18), (37.5, 26))]:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1.3})
    ax.text(1, -1, "Generic redrawn diagram (not the as-built drawing). No addresses, brands, site names or device counts.",
            fontsize=7, color=MUTED)
    fig.savefig(out / "diagram_onprem_architecture.png", metadata=NO_META, bbox_inches="tight")
    plt.close(fig)


def alert_illustration(out):
    w, h = 1200, 675
    im = Image.new("RGB", (w, h), "#4b5563")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 430, w, h], fill="#6b6459")
    for i, (x, helmet, vest) in enumerate([(180, True, True), (420, False, True), (660, True, False)]):
        d.rectangle([x, 300, x + 70, 430], fill="#f97316" if vest else "#334155")
        d.ellipse([x + 12, 250, x + 58, 296], fill="#9ca3af")
        if helmet:
            d.pieslice([x + 6, 236, x + 64, 290], 180, 360, fill="#f8fafc")
        ok = helmet and vest
        d.rectangle([x - 12, 226, x + 82, 442], outline=OK if ok else BAD, width=4)
        d.text((x - 10, 450), "OK" if ok else ("NO HELMET" if not helmet else "NO VEST"), fill=OK if ok else BAD)
    d.rectangle([0, 0, w, 40], fill="#111827")
    d.text((16, 13), "ILLUSTRATION - not a real camera image. Drawn figures, no site, no people, no logos.", fill="#fbbf24")
    d.rectangle([800, 470, 1180, 640], fill="#f9fafb")
    d.text((815, 485), "Phone alert (text only):", fill=INK)
    d.text((815, 515), "ALERT  No helmet | Area 2 | 10:42", fill=BAD)
    d.text((815, 545), "Snapshot opens on the plant console only.", fill=INK)
    d.text((815, 575), "In-charge acknowledges -> closes with evidence.", fill=INK)
    im.save(out / "illustration_alert_flow.png", optimize=True)  # PIL writes no EXIF unless given


ROI_HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gate ROI Calculator</title><style>
:root{--bg:#fff;--ink:#1f2937;--muted:#6b7280;--acc:#2563eb;--card:#f3f4f6}
@media (prefers-color-scheme:dark){:root{--bg:#111827;--ink:#f3f4f6;--muted:#9ca3af;--acc:#60a5fa;--card:#1f2937}}
body{background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,sans-serif;max-width:640px;margin:0 auto;padding:16px}
label{display:block;margin:12px 0 4px;color:var(--muted);font-size:14px}input{width:100%;padding:8px;font-size:16px;box-sizing:border-box}
.out{background:var(--card);padding:16px;border-radius:8px;margin-top:16px}.big{font-size:28px;color:var(--acc);font-weight:700}
small{color:var(--muted)}</style></head><body>
<h1>What is a faster gate worth at your plant?</h1>
<p>Fill in <b>your own</b> numbers. Nothing is sent anywhere; no client data is in this page. The starting values are examples only.</p>
<label>Transporter detention you pay per month (Rs lakh)</label><input id="det" type="number" value="10">
<label>Reduction you expect (%) - our reference plant saw detention fall by about two thirds in one month (ASSUMED: that month is the client finance team's estimate), with its own weighbridge and dispatch-slot changes doing part of the work</label><input id="red" type="number" value="30">
<label>Share you credit to the analytics (%)</label><input id="share" type="number" value="50">
<label>One-time project cost (Rs lakh)</label><input id="cost" type="number" value="80">
<label>Yearly support cost (Rs lakh)</label><input id="amc" type="number" value="12">
<div class="out"><div>Credited saving per year</div><div class="big" id="sav">-</div><div>Simple payback</div><div class="big" id="pb">-</div>
<small>ASSUMED inputs are yours. Safety outcomes are deliberately not monetised here.</small></div>
<script>
const v=id=>parseFloat(document.getElementById(id).value)||0;
function calc(){const s=v('det')*12*v('red')/100*v('share')/100, net=s-v('amc');
document.getElementById('sav').textContent='Rs '+s.toFixed(1)+' lakh';
document.getElementById('pb').textContent=net>0?(v('cost')/net*12).toFixed(0)+' months':'not paid back on gate alone';}
document.querySelectorAll('input').forEach(i=>i.addEventListener('input',calc));calc();
</script></body></html>"""


def build(library, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    ppe_chart(library, out)
    gate_chart(library, out)
    architecture(out)
    alert_illustration(out)
    (out / "roi_calculator.html").write_text(ROI_HTML, encoding="utf-8")
    return sorted(p.name for p in out.iterdir())
