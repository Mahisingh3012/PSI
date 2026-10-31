"""Reset the demo to its starting state: no approvals recorded, no 'bad draft' project, empty register.

  python demo/reset_demo.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in [ROOT / "runs/drishti/approvals", ROOT / "runs/drishti_bad", ROOT / "runs/register.json", ROOT / "runs/register.md"]:
    if p.is_dir():
        shutil.rmtree(p)
        print(f"removed {p.relative_to(ROOT)}")
    elif p.exists():
        p.unlink()
        print(f"removed {p.relative_to(ROOT)}")
print("Demo reset. Next: python engine/run.py build --project drishti")
