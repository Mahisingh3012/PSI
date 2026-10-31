"""Thin wrapper for the judgement agents (rules, results spec, exposure, writers, approval, fixer).

Provider: Google Gemini (Gemini 3). Put the key in the environment or in a `.env` file at the project root:
    GEMINI_API_KEY=...            (GOOGLE_API_KEY also works)
    GEMINI_MODEL=gemini-3-pro-preview   (optional; falls back to the models in FALLBACK_MODELS if unavailable)

With a key, each agent's prompt (engine/prompts/NN_*.md, with 00_shared_rules.md prepended) is sent with the
evidence index and the earlier agents' outputs, and the reply is saved to runs/<project>/agent_outputs/ (log: LIVE).
Without a key, the saved outputs of a previous run are replayed (log: RECORDED), so the deterministic agents,
checks and the approval gate still run end to end.
"""
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FALLBACK_MODELS = ["gemini-3-pro-preview", "gemini-3-flash-preview"]
API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def _load_dotenv():
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*)\s*$", line)
            if m and not line.lstrip().startswith("#"):
                os.environ.setdefault(m.group(1), m.group(2).strip().strip('"').strip("'"))


_load_dotenv()


def _key():
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


def live():
    return bool(_key())


def _models():
    first = os.environ.get("GEMINI_MODEL")
    return [first] + [m for m in FALLBACK_MODELS if m != first] if first else FALLBACK_MODELS


def call_gemini(system, user, max_tokens=16000):
    body = json.dumps({
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.2},
    }).encode()
    last_error = None
    for model in _models():
        req = urllib.request.Request(API.format(model=model), data=body,
                                     headers={"x-goog-api-key": _key(), "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read())
            parts = data["candidates"][0]["content"]["parts"]
            return model, "".join(p.get("text", "") for p in parts if not p.get("thought"))
        except urllib.error.HTTPError as e:
            last_error = f"{model}: HTTP {e.code} {e.read()[:300]!r}"
            if e.code != 404:  # 404 = model name not available: try the next one
                break
    raise SystemExit(f"Gemini call failed ({last_error})")


def _strip_fences(text):
    m = re.match(r"^\s*```[a-zA-Z]*\n(.*)\n```\s*$", text, re.S)
    return m.group(1) if m else text


def run_agent(name, prompt_file: Path, context: str, out_file: Path, log):
    if live():
        shared = (prompt_file.parent / "00_shared_rules.md").read_text(encoding="utf-8")
        model, text = call_gemini(shared + "\n\n" + prompt_file.read_text(encoding="utf-8"), context)
        out_file.write_text(_strip_fences(text), encoding="utf-8")
        log(f"[{name}] LIVE call to {model} -> {out_file.name}")
    elif out_file.exists():
        log(f"[{name}] RECORDED output replayed: {out_file.name} (set GEMINI_API_KEY in .env for a live run)")
    else:
        raise SystemExit(f"[{name}] no GEMINI_API_KEY and no recorded output at {out_file}")
    return out_file.read_text(encoding="utf-8")
