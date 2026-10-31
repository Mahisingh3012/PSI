"""Agent 4 - Calculator. Executes a metric spec (written by the Results agent) against raw data files.

The LLM decides *what* to measure (definition, baseline, window, filters); this code does the arithmetic
and records the working for every number, so no figure in the case study is computed by a language model.
Ops are generic so the same code runs on any project's CSV exports.
"""
import json
from pathlib import Path

import pandas as pd


def _frame(library, step):
    df = pd.read_csv(Path(library) / step["file"])
    for col, cond in step.get("where", {}).items():
        if isinstance(cond, dict):
            if "between" in cond:
                lo, hi = cond["between"]
                df = df[(df[col] >= lo) & (df[col] <= hi)]
            if "in" in cond:
                df = df[df[col].isin(cond["in"])]
            if "notna" in cond:
                df = df[df[col].notna()]
        else:
            df = df[df[col] == cond]
    return df


def run_spec(library, spec):
    ledger = {}
    for step in spec["calcs"]:
        op, cid = step["op"], step["id"]
        work, value = "", None
        if op == "ratio_of_sums":
            df = _frame(library, step)
            n, d = df[step["num"]].sum(), df[step["den"]].sum()
            value = n / d * step.get("scale", 1)
            work = f"sum({step['num']})={n} / sum({step['den']})={d} x {step.get('scale', 1)} over {len(df)} rows"
        elif op == "mean":
            df = _frame(library, step)
            value = df[step["col"]].mean()
            work = f"mean({step['col']}) over {df[step['col']].notna().sum()} non-empty rows = {value:.4f}"
        elif op == "median":
            df = _frame(library, step)
            value = df[step["col"]].median()
            work = f"median({step['col']}) over {len(df)} rows (zone-week medians) = {value:.4f}"
        elif op == "weighted_mean":
            df = _frame(library, step)
            value = (df[step["col"]] * df[step["weight"]]).sum() / df[step["weight"]].sum()
            work = f"sum({step['col']} x {step['weight']}) / sum({step['weight']}) over {len(df)} rows"
        elif op == "count":
            df = _frame(library, step)
            value = len(df)
            work = f"rows matching filter = {value}"
        elif op == "sum":
            df = _frame(library, step)
            value = df[step["col"]].sum()
            work = f"sum({step['col']}) over {len(df)} rows"
        elif op == "pct_change":
            a, b = ledger[step["from"]]["value"], ledger[step["to"]]["value"]
            value = (b - a) / a * 100
            work = f"({b:.4f} - {a:.4f}) / {a:.4f} x 100 using [C:{step['from']}] and [C:{step['to']}]"
        elif op == "diff":
            a, b = ledger[step["from"]]["value"], ledger[step["to"]]["value"]
            value = b - a
            work = f"{b:.4f} - {a:.4f} using [C:{step['from']}] and [C:{step['to']}]"
        elif op == "formula":
            env = {k: ledger[k]["value"] for k in step["inputs"] if k in ledger}
            env.update(step.get("constants", {}))
            value = eval(step["expr"], {"__builtins__": {}}, env)  # expr is from the reviewed spec, not from data
            work = f"{step['expr']} with " + ", ".join(f"{k}={v:.4g}" for k, v in env.items())
        else:
            raise ValueError(f"unknown op {op}")
        rnd = step.get("round", 1)
        ledger[cid] = {
            "label": step["label"], "value": float(value), "display": f"{value:.{rnd}f}{step.get('unit', '')}",
            "working": work, "source": step.get("file") or "ledger", "filters": step.get("where", {}),
            "assumed": step.get("assumed", False), "note": step.get("note", ""),
        }
    return ledger


def write_ledger(ledger, out: Path):
    (out / "calc_ledger.json").write_text(json.dumps(ledger, indent=1, ensure_ascii=False), encoding="utf-8")
    rows = ["# Calculation ledger (machine-generated, every number with its working)", "",
            "| ID | Metric | Value | Working | Source / filter | Note |", "| --- | --- | --- | --- | --- | --- |"]
    for k, v in ledger.items():
        flt = json.dumps(v["filters"]) if v["filters"] else ""
        note = ("ASSUMED. " if v["assumed"] else "") + v["note"]
        rows.append(f"| {k} | {v['label']} | **{v['display']}** | {v['working']} | {v['source']} {flt} | {note} |")
    (out / "calc_ledger.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
