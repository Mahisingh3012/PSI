"""Converts the Markdown docs to styled PDFs with a headless Edge or Chrome.  python scripts/make_pdfs.py"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ["DOCUMENTATION.md", "DEMO_SCRIPT.md", "PROCESS.md"]
BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            shutil.which("msedge") or "", shutil.which("google-chrome") or "", shutil.which("chromium") or ""]
CSS = """
@page{size:A4;margin:16mm 14mm}body{font:10.5pt/1.5 "Segoe UI",system-ui,sans-serif;color:#0f172a}
h1{font-size:20pt;border-bottom:2px solid #2563eb;padding-bottom:4px}h2{font-size:14pt;margin-top:18pt;color:#1e3a8a;page-break-after:avoid}
h3{font-size:11.5pt;page-break-after:avoid}table{border-collapse:collapse;width:100%;font-size:8.8pt;margin:6pt 0;page-break-inside:auto}
tr{page-break-inside:avoid}th,td{border:1px solid #cbd5e1;padding:4px 6px;vertical-align:top;text-align:left}th{background:#eff4ff}
code{font-family:Consolas,monospace;font-size:8.8pt;background:#f1f5f9;padding:0 3px;border-radius:3px}
pre{background:#f1f5f9;padding:8px;border-radius:6px;white-space:pre-wrap;font-size:8.5pt;page-break-inside:avoid}pre code{background:none}
blockquote{border-left:3px solid #2563eb;margin:6pt 0;padding:2pt 10pt;color:#334155;background:#f8fafc}hr{border:0;border-top:1px solid #e2e8f0}
"""


ONE_PAGE = {"PROCESS.md": "@page{size:A4 landscape;margin:10mm 12mm}body{font-size:8.6pt;line-height:1.35}table{font-size:8pt}h1{font-size:14pt}"}


def _normalise(md):
    """Python-Markdown needs a blank line before a list and 4-space indents for nested items."""
    out, prev = [], ""
    for line in md.splitlines():
        stripped = line.lstrip()
        is_item = bool(re.match(r"(?:[-*]|\d+\.)\s", stripped))
        if is_item and line.startswith("  ") and not line.startswith("    "):
            line = "    " + stripped
        prev_item = bool(re.match(r"\s*(?:[-*]|\d+\.)\s", prev))
        if is_item and prev.strip() and not prev_item and not prev.lstrip().startswith(("|", "```")):
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def main():
    browser = next((b for b in BROWSERS if b and Path(b).exists()), None)
    if not browser:
        raise SystemExit("Edge or Chrome not found; open the .md files in any Markdown viewer and print to PDF instead.")
    args = sys.argv[1:]  # optional: files to convert, and --out <dir> (default docs_pdf/)
    out_dir = Path(args[args.index("--out") + 1]) if "--out" in args else ROOT / "docs_pdf"
    files = [a for i, a in enumerate(args) if a != "--out" and (i == 0 or args[i - 1] != "--out")] or DOCS
    for name in files:
        src = Path(name) if Path(name).is_absolute() else ROOT / name
        body = markdown.markdown(_normalise(src.read_text(encoding="utf-8")), extensions=["tables", "fenced_code"])
        page = (f"<!doctype html><html><head><meta charset='utf-8'><title>{src.stem}</title>"
                f"<style>{CSS}{ONE_PAGE.get(name, '')}</style></head><body>{body}</body></html>")
        with tempfile.TemporaryDirectory() as tmp:
            html_file = Path(tmp) / f"{src.stem}.html"
            html_file.write_text(page, encoding="utf-8")
            out = out_dir / f"{src.stem}.pdf"
            out.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            f"--user-data-dir={Path(tmp) / 'profile'}", f"--print-to-pdf={out}", html_file.as_uri()],
                           check=True, capture_output=True, timeout=120)
            print(f"{out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
