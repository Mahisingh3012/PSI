"""Agent 7 - Verifier. Refuses any sentence or number it cannot trace.

Rules, applied to every draft the Writer agent produces:
  1. Every claim line (sentence, bullet, table row) must carry at least one citation: [Dnn:Lx], [Dnn:Lx-y] or [C:calc_id].
  2. Cited files, lines and calc ids must exist.
  3. Every number in the line must appear in a cited source line or in a cited calculation (value, display or working),
     allowing for rounding. Numbers marked ASSUMED must cite a calc flagged assumed.
  4. For anything marked outward-facing, no banned identifying term may appear (from the exposure agent).
  5. Each cited source line must be relevant: it must share at least one content word or number with the claim
     (catches citations that drifted to the wrong line), and must not be blank.
  6. A line that cites an estimate (a calc flagged assumed) must say ASSUMED, and ASSUMED must cite such a calc.
Lines starting with '#', '>' quoting rules, or '<!-- -->' are structure, not claims. A line ending in [NO-CLAIM] is
an explicit opinion/call-to-action with no factual content and is still checked for numbers and banned terms.
"""
import re

CITE = re.compile(r"\[(D\d{2}):L(\d+)(?:-(\d+))?\]|\[C:([\w]+)\]")
NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")
IGNORE_NUM = {"1", "2", "3"}  # list ordinals / "one of two" style words written as digits


MONTHS = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*"
DATES = re.compile(rf"\b\d{{1,2}}(?:[-–]\d{{1,2}})? {MONTHS}(?: \d{{4}})?|\b{MONTHS} \d{{4}}|\b20\d\d-\d\d(?:-\d\d)?\b|\b\d{{1,2}}:\d\d\b|\bv\d+\.\d+\b|\b[A-Z]+-?\d+\b|\b(?:MSA|[Cc]lause)\s+\d+(?:\.\d+)?(?:\([a-e]\))?(?:,\s*\d+\.\d+(?:\([a-e]\))?)*")


def _numbers(text):
    text = re.sub(r"^\|\s*\d+\s*\|", "|", text)  # table row index
    # Dates, times, release tags and IDs (K1, CR-03) are checked by the citation itself, not as quantities.
    text = DATES.sub(" ", CITE.sub(" ", text))
    out = []
    for m in NUM.finditer(text):
        raw = m.group(0).replace(",", "").rstrip(".")
        if raw and raw not in IGNORE_NUM:
            out.append(raw)
    return out


STOP = set("""that this with from have were they their there which what when where would could should about after
before into than then them these those over under also only been being does done just more most much such very will
your ours other some each every same both many here like said says made make used uses using within without while
shown shows case study source sources client vendor because""".split())


def _words(text):
    """Content words (first 5 letters, so 'measured'/'measures' match) and numbers, for the citation-relevance check."""
    toks = re.findall(r"[a-z][a-z\-]{3,}|\d+(?:\.\d+)?", text.lower())
    return {t if t[0].isdigit() else t.rstrip("s")[:5] for t in toks if t not in STOP}


def _supported(num, haystack_nums):
    try:
        x = float(num)
    except ValueError:
        return False
    for h in haystack_nums:
        try:
            y = float(h)
        except ValueError:
            continue
        if x == y:
            return True
        # rounding: 91.08 -> 91.1 / 91 ; 2,40,000 written as 2.4 lakh handled by the calc ledger
        dec = len(num.split(".")[1]) if "." in num else 0
        if abs(round(y, dec) - x) < 1e-9:
            return True
    return False


def verify(text, index, ledger, banned=(), outward=False):
    problems = []
    all_lines = text.splitlines()
    for n, line in enumerate(all_lines, 1):
        s = line.strip()
        if not s or s.startswith(("#", "<!--", "---", "|---", "| ---")) or set(s) <= set("|-: "):
            continue
        nxt = all_lines[n].strip() if n < len(all_lines) else ""
        if s.startswith("|") and nxt.startswith("|") and set(nxt) <= set("|-: "):
            continue  # table header row
        cites = CITE.findall(s)
        no_claim = s.endswith("[NO-CLAIM]")
        if not cites and not no_claim:
            problems.append((n, "UNTRACEABLE", "no citation", s[:120]))
            continue
        hay = []
        for doc, a, b, calc in cites:
            if calc:
                if calc not in ledger:
                    problems.append((n, "BAD_CITE", f"unknown calc {calc}", s[:120]))
                    continue
                c = ledger[calc]
                hay += NUM.findall(c["display"].replace(",", "")) + [str(c["value"])] + NUM.findall(c["working"].replace(",", ""))
                hay += NUM.findall(c["label"])
            else:
                if doc not in index or index[doc]["kind"] != "text":
                    problems.append((n, "BAD_CITE", f"unknown or non-text doc {doc}", s[:120]))
                    continue
                lines = index[doc]["lines"]
                a, b = int(a), int(b or a)
                if b > len(lines) or a < 1:
                    problems.append((n, "BAD_CITE", f"{doc} has {len(lines)} lines, cited {a}-{b}", s[:120]))
                    continue
                for src in lines[a - 1:b]:
                    hay += [x.replace(",", "") for x in NUM.findall(src)]
        for num in _numbers(s):
            if not _supported(num, hay):
                problems.append((n, "NUMBER_NOT_IN_SOURCE", num, s[:120]))
        claim_words = _words(CITE.sub(" ", s))
        for doc, a, b, calc in cites:
            if calc or doc not in index or index[doc]["kind"] != "text":
                continue
            src = " ".join(index[doc]["lines"][int(a) - 1:int(b or a)])
            if not src.strip():
                problems.append((n, "BAD_CITE", f"{doc}:L{a} is a blank line", s[:120]))
            elif not claim_words & _words(src):
                problems.append((n, "WEAK_CITE", f"{doc}:L{a}{'-' + b if b else ''} shares no words with the claim", s[:120]))
        if "ASSUMED" in s and not any(calc and ledger.get(calc, {}).get("assumed") for *_, calc in cites):
            problems.append((n, "ASSUMED_WITHOUT_CALC", "ASSUMED must cite an assumed calc", s[:120]))
        if "ASSUMED" not in s and any(calc and ledger.get(calc, {}).get("assumed") for *_, calc in cites):
            problems.append((n, "ASSUMED_NOT_MARKED", "cites an estimate, so the line must say ASSUMED", s[:120]))
        if outward:
            for t in banned:
                if re.search(rf"\b{re.escape(t)}\b", CITE.sub("", s), re.I):
                    problems.append((n, "EXPOSURE", t, s[:120]))
    return problems


def strip_citations(text):
    """Clean copy for the client/public: remove citation tags (the traced copy is kept as the record)."""
    text = CITE.sub("", text).replace("[NO-CLAIM]", "")
    text = re.sub(r"[ \t]+([.,;:])", r"\1", re.sub(r"[ \t]{2,}", " ", text))
    text = re.sub(r"[ \t]+(\n|$)", r"\1", text)
    return _drop_empty_table_columns(text)


def _drop_empty_table_columns(text):
    """After citations are stripped, drop table columns that are now empty (usually Source)."""
    lines = text.splitlines(keepends=True)
    out, i = [], 0
    while i < len(lines):
        if not lines[i].lstrip().startswith("|"):
            out.append(lines[i])
            i += 1
            continue
        block, i = _table_block(lines, i)
        out.extend(_trim_empty_cols(block))
    return "".join(out)


def _table_block(lines, i):
    start = i
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        i += 1
    return lines[start:i], i


def _trim_empty_cols(block):
    parsed = []
    for line in block:
        nl = "\n" if line.endswith("\n") else ""
        raw = line[:-1] if nl else line
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        parsed.append((cells, nl))
    if not parsed:
        return block
    ncols = max(len(p[0]) for p in parsed)
    for cells, _ in parsed:
        cells.extend([""] * (ncols - len(cells)))

    def is_sep(cells):
        return bool(cells) and all(re.fullmatch(r":?-{1,}:?", c.replace(" ", "") or "-") for c in cells)

    body = [cells for cells, _ in parsed if cells and not is_sep(cells)]
    if len(body) < 2:
        return block
    header, rows = body[0], body[1:]
    drop = {c for c in range(ncols) if all(not row[c] for row in rows)}
    if not drop:
        return block
    rebuilt = []
    for cells, nl in parsed:
        kept = [cells[c] for c in range(len(cells)) if c not in drop]
        rebuilt.append("| " + " | ".join(kept) + " |" + nl if kept else nl)
    return rebuilt
