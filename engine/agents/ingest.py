"""Agent 1 - Librarian. Deterministic: indexes every file in a project library so each line can be cited.

Works on any library folder: text files are split into numbered lines, CSVs keep header + rows,
images are recorded with size and metadata (EXIF / GPS / embedded text) for the exposure agent.
"""
import json
from pathlib import Path

from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

TEXT_EXT = {".md", ".txt", ".csv", ".yaml", ".yml", ".json"}
IMAGE_EXT = {".png", ".jpg", ".jpeg"}


def image_meta(path):
    im = Image.open(path)
    exif = im.getexif()
    meta = {TAGS.get(k, str(k)): str(v) for k, v in exif.items() if k != 0x8825}
    gps = {GPSTAGS.get(k, str(k)): str(v) for k, v in exif.get_ifd(0x8825).items()}
    info = {k: str(v)[:120] for k, v in im.info.items() if k not in ("icc_profile", "exif")}
    return {"size": list(im.size), "exif": meta, "gps": gps, "info": info}


def build_index(library: Path):
    files = sorted(p for p in library.rglob("*") if p.is_file())
    index = {}
    for i, p in enumerate(files, 1):
        doc_id = f"D{i:02d}"
        rel = p.relative_to(library).as_posix()
        entry = {"id": doc_id, "path": rel, "kind": "other"}
        if p.suffix.lower() in TEXT_EXT:
            entry["kind"] = "text"
            entry["lines"] = p.read_text(encoding="utf-8").splitlines()
        elif p.suffix.lower() in IMAGE_EXT:
            entry["kind"] = "image"
            entry["meta"] = image_meta(p)
        index[doc_id] = entry
    return index


def write_index(index, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    (out / "evidence_index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    rows = ["# Evidence index", "", "Cite as `[Dnn:Lx]` (line x of file Dnn) or `[Dnn:Lx-y]`; calculations as `[C:calc_id]`.", "",
            "| ID | File | Kind | Lines |", "| --- | --- | --- | --- |"]
    for d in index.values():
        rows.append(f"| {d['id']} | {d['path']} | {d['kind']} | {len(d.get('lines', []))} |")
    (out / "evidence_index.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def cite_text(index, doc_id, a, b=None):
    lines = index[doc_id]["lines"]
    b = b or a
    return "\n".join(lines[a - 1:b])
