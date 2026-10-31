"""Thin wrapper for the judgement agents (rules, timeline, results spec, exposure, writer, approval).

With ANTHROPIC_API_KEY set, each agent's prompt (engine/prompts/NN_*.md) is sent to Claude together with the
evidence index and the outputs of earlier agents, and the reply is saved to runs/<project>/agent_outputs/.
Without a key, the engine replays the saved outputs of a previous run (marked RECORDED in the run log), so the
deterministic agents, checks and the approval gate can still run end to end.
"""
import json
import os
import urllib.request
from pathlib import Path

MODEL = os.environ.get("CASE_ENGINE_MODEL", "claude-opus-5-5")


def call_claude(system, user, max_tokens=8000):
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({"model": MODEL, "max_tokens": max_tokens, "system": system,
                         "messages": [{"role": "user", "content": user}]}).encode(),
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return "".join(b.get("text", "") for b in json.loads(r.read())["content"])


def live():
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def run_agent(name, prompt_file: Path, context: str, out_file: Path, log):
    if os.environ.get("ANTHROPIC_API_KEY"):
        shared = (prompt_file.parent / "00_shared_rules.md").read_text(encoding="utf-8")
        text = call_claude(shared + "\n\n" + prompt_file.read_text(encoding="utf-8"), context)
        out_file.write_text(text, encoding="utf-8")
        log(f"[{name}] LIVE call to {MODEL} -> {out_file.name}")
    elif out_file.exists():
        log(f"[{name}] RECORDED output replayed: {out_file.name} (set ANTHROPIC_API_KEY for a live run)")
    else:
        raise SystemExit(f"[{name}] no API key and no recorded output at {out_file}")
    return out_file.read_text(encoding="utf-8")
