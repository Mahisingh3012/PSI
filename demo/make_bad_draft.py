"""Demo helper: copy the good run's agent outputs to a new project 'drishti_bad' and slip in the claims the
vendor's sales team actually wanted to publish. Then build drishti_bad: the verifier must refuse it.

  python demo/make_bad_draft.py
  python engine/run.py build --library ../Project_Drishti_Library/Project_Drishti_Library --project drishti_bad
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src, dst = ROOT / "runs/drishti/agent_outputs", ROOT / "runs/drishti_bad/agent_outputs"
if dst.parent.exists():
    shutil.rmtree(dst.parent)
shutil.copytree(src, dst)

BAD = """
## Sales team additions (from the draft deck)

A leading cement major raised PPE compliance from 74% to 97% with AI. [C:k1_base] [C:k1_final]
Zero lost-time injuries since go-live and Rs 2.3 crore saved every year.
The Bhadrapur plant now runs 146 cameras with alerts in under 2 minutes. [D14:L8]
"""
cs = dst / "04_case_study.md"
cs.write_text(cs.read_text(encoding="utf-8") + BAD, encoding="utf-8")
print(f"Wrote {cs.relative_to(ROOT)} with 3 bad lines appended:")
print(BAD)
