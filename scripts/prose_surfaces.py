"""List every prose surface a reader sees, with word counts, so each is assigned and none missed.

The residual pass (docs/superpowers/notes/residual-review.md) reads each surface listed here once.
The surfaces:

``paper``
    ``paper/paper.ipynb``: the abstract, then the body by heading (Markdown cells and the
    Markdown outputs of code cells, the generated sentences and tables).
``appendix``
    ``paper/supporting_material.ipynb``: each appendix by heading (Appendix A is generated from
    ``glossary.yaml`` and is read through the glossary surface, not twice).
``docs``
    ``docs/*.md`` and ``docs/user-guide/*.md``, one surface per page.
``example``
    ``examples/adcs/case-model.md``.
``readme``
    ``README.md``, read as GitHub renders it.
``site``
    ``site/index.html`` (the root page) and ``site/history.html`` (the history page).
``glossary``
    the long forms of ``glossary.yaml`` (``short``, ``formal``, ``not`` of every entry).

A surface over the size limit is split at the next heading level so that one reader slot holds a
readable amount; the slots pack consecutive surfaces of the same view up to the slot size.
Docstrings, code, math, citation keys and link targets are not prose surfaces here (the vocabulary
check reads docstrings).

    uv run python scripts/prose_surfaces.py             # the table
    uv run python scripts/prose_surfaces.py --json      # the same as JSON
    uv run python scripts/prose_surfaces.py --root DIR  # another tree (tests use this)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_vocabulary as cv

ROOT = Path(__file__).resolve().parent.parent
SURFACE_LIMIT = 2500  # words; a larger surface is split at the next heading level
SLOT_SIZE = 3500  # words of one reader slot
MIN_WORDS = 150  # a smaller piece of a split surface is folded into its neighbour

VIEWS = {
    "paper": "the paper as rendered (built site, paper pages)",
    "appendix": "the paper's appendices as rendered (built site, supporting material)",
    "docs": "the docs site as rendered",
    "example": "the docs site as rendered (case model page) or the file on GitHub",
    "readme": "README.md as GitHub renders it",
    "site": "the root and history pages as rendered",
    "glossary": "the docs site's Glossary page and Appendix A as rendered",
}
_HEAD_HTML = re.compile(r"<h([1-6])\b", re.I)
_BLOCK_TAGS = re.compile(
    r"(</?(?:p|div|li|h[1-6]|section|header|footer|main|ul|ol|br|tr|nav|figure|figcaption)\b[^>]*>)",
    re.I,
)
_HEAD_MD = re.compile(r"^\s*(#{1,6})\s+(.*\S)\s*$")


@dataclass
class Block:
    """One paragraph (or heading, or table) of visible prose, with where it sits."""

    loc: str
    raw: str
    text: str
    heading: int = 0  # heading level if this block is a heading, else 0
    table: bool = False
    path: tuple = ()  # the headings above it, outermost first, as (level, title)


@dataclass
class Surface:
    id: str
    kind: str
    file: str
    section: str
    blocks: list = field(default_factory=list)
    generated: bool = False
    slot: str = ""

    @property
    def words(self) -> int:
        return sum(len(b.text.split()) for b in self.blocks)

    @property
    def prose_words(self) -> int:
        return sum(len(b.text.split()) for b in self.blocks if not b.table)

    @property
    def view(self) -> str:
        return VIEWS[self.kind]

    @property
    def first_loc(self) -> str:
        return self.blocks[0].loc if self.blocks else ""


# ------------------------------------------------------------------ reading blocks


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:48] or "section"


def _heading_title(text: str) -> str:
    t = re.sub(r"\{#[^}]*\}", "", text)
    t = re.sub(r"\s+", " ", cv.clean_markdown(t)).strip()
    return t


def _md_blocks(
    text: str, loc_for, path: list, line0: int = 1, keep_comments: bool = False
) -> list[Block]:
    """Split Markdown into blocks at blank lines, tracking the heading path."""
    out = []
    fence = ""  # the open code fence, which a blank line inside it does not close
    for m in re.finditer(r"\S.*?(?=\n[ \t]*\n|\Z)", text, re.S):
        block = m.group(0)
        line = line0 + text.count("\n", 0, m.start())
        kept = []
        for ln in block.split("\n"):
            fm = re.match(r"\s*(```+|~~~+)", ln)
            if fm:
                fence = "" if fence and fm.group(1)[0] == fence[0] else (fence or fm.group(1))
            elif not fence:
                kept.append(ln)
        block = "\n".join(kept)
        if not block.strip():
            continue
        lines = block.split("\n")
        # a block may carry a label line ("(name)=") before its heading
        hm = next((_HEAD_MD.match(ln) for ln in lines[:2] if _HEAD_MD.match(ln)), None)
        level = 0
        if hm and not block.lstrip().startswith("```"):
            level = len(hm.group(1))
            title = _heading_title(hm.group(2))
            while path and path[-1][0] >= level:
                path.pop()
            path.append((level, title))
        table = all(ln.lstrip().startswith("|") for ln in lines if ln.strip())
        if table:
            cleaned = re.sub(r"[|]", " ", cv.clean_markdown(block))
        else:
            cleaned = cv.clean_markdown(block)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if cleaned:
            out.append(
                Block(
                    loc_for(line),
                    block,
                    cleaned,
                    level,
                    table,
                    tuple(path),
                )
            )
    return out


def _notebook_blocks(root: Path, rel: str) -> list[Block]:
    path = root / rel
    if not path.is_file():
        return []
    nb = json.loads(path.read_text(encoding="utf-8"))
    blocks: list[Block] = []
    hpath: list = []
    for i, cell in enumerate(nb.get("cells", [])):
        chunks = []
        if cell["cell_type"] == "markdown":
            chunks.append(("", "".join(cell["source"])))
        elif cell["cell_type"] == "code":
            for out in cell.get("outputs", []):
                md = out.get("data", {}).get("text/markdown")
                if md:
                    chunks.append((" output", "".join(md) if isinstance(md, list) else md))
        for kind, chunk in chunks:
            meta, body = cv.front_matter(chunk)
            for key in ("title", "abstract"):
                if isinstance(meta.get(key), str):
                    text = re.sub(r"\s+", " ", cv.clean_markdown(meta[key])).strip()
                    if text:
                        blocks.append(
                            Block(f"cell {i} {key}", meta[key], text, 0, False, ((1, key),))
                        )
            blocks += _md_blocks(body, lambda ln, i=i, k=kind: f"cell {i}{k}", hpath)
    return blocks


def _markdown_blocks(root: Path, rel: str) -> list[Block]:
    path = root / rel
    if not path.is_file():
        return []
    src = path.read_text(encoding="utf-8")
    _, body = cv.front_matter(src)
    line0 = 1 + src.count("\n", 0, len(src) - len(body))
    return _md_blocks(body, lambda ln: f"line {ln}", [], line0)


def _html_blocks(root: Path, rel: str) -> list[Block]:
    path = root / rel
    if not path.is_file():
        return []
    src = path.read_text(encoding="utf-8")
    src = re.sub(
        r"<(style|script|head)\b.*?</\1>",
        lambda m: "\n" * m.group(0).count("\n"),
        src,
        flags=re.S | re.I,
    )
    src = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
    parts = _BLOCK_TAGS.split(src)  # text, tag, text, tag, ...
    blocks, hpath, pos, prev_tag = [], [], 0, ""
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            prev_tag = part
            pos += len(part)
            continue
        text = re.sub(r"\s+", " ", cv.clean_markdown(part)).strip()
        line = 1 + src.count("\n", 0, pos + (len(part) - len(part.lstrip())))
        pos += len(part)
        if not text:
            continue
        level = 0
        hm = _HEAD_HTML.match(prev_tag)
        if hm:
            level = int(hm.group(1))
            while hpath and hpath[-1][0] >= level:
                hpath.pop()
            hpath.append((level, text))
        blocks.append(Block(f"line {line}", part, text, level, False, tuple(hpath)))
    return blocks


def _glossary_blocks(root: Path) -> list[Block]:
    path = root / "glossary.yaml"
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    blocks = []
    for e in data.get("entries", []):
        for fld in ("short", "formal", "not"):
            val = e.get(fld)
            if isinstance(val, str) and val.strip():
                text = re.sub(r"\s+", " ", cv.clean_markdown(val)).strip()
                if text:
                    blocks.append(Block(f"entry {e['id']}.{fld}", val, text, 0, False, ()))
    return blocks


# ------------------------------------------------------------------ grouping into surfaces


def _wc(bs: list[Block]) -> int:
    return sum(len(b.text.split()) for b in bs)


def _split(blocks: list[Block], depth: int, limit: int):
    """Group blocks by the heading path truncated to ``depth``; recurse into the oversized."""
    groups: list[tuple[tuple, list[Block]]] = []
    for b in blocks:
        key = tuple(b.path[:depth]) if depth else ()
        if groups and groups[-1][0] == key:
            groups[-1][1].append(b)
        else:
            groups.append((key, [b]))
    out = []
    for key, bs in groups:
        if _wc(bs) > limit and any(len(b.path) > depth for b in bs) and depth < 4:
            out += _split(bs, depth + 1, limit)
        else:
            out.append((key, bs))
    return out


def _is_generated(key: tuple, kind: str) -> bool:
    return kind == "appendix" and bool(key) and bool(re.match(r"Appendix A\b", key[0][1]))


def _merge_small(pieces: list, kind: str) -> list:
    """Fold a piece under MIN_WORDS into the next piece (else the previous) of the same status."""
    pieces = [[k, b, False] for k, b in pieces]
    i = 0
    while i < len(pieces) and len(pieces) > 1:
        key, bs, _ = pieces[i]
        if _wc(bs) >= MIN_WORDS:
            i += 1
            continue
        gen = _is_generated(key, kind)
        nxt = i + 1 < len(pieces) and _is_generated(pieces[i + 1][0], kind) == gen
        prv = i > 0 and _is_generated(pieces[i - 1][0], kind) == gen
        if nxt:
            pieces[i + 1] = [key, bs + pieces[i + 1][1], True]
            del pieces[i]
        elif prv:
            pieces[i - 1] = [pieces[i - 1][0], pieces[i - 1][1] + bs, True]
            del pieces[i]
        else:
            i += 1
    return pieces


_CODE = re.compile(r"^(Appendix [A-G]|[A-G]\.\d+|L\d+)\b")


def _title_of(key: tuple, fallback: str) -> str:
    return key[-1][1] if key else fallback


def _id_of(prefix: str, key: tuple, fallback: str) -> str:
    if not key:
        return prefix
    title = key[-1][1]
    m = _CODE.match(title)
    return f"{prefix}/{_slug(m.group(1)) if m else _slug(title)}"


def _surfaces_from(
    blocks: list[Block], kind: str, file: str, prefix: str, depth: int, front: str
) -> list[Surface]:
    pieces = _merge_small(_split(blocks, depth, SURFACE_LIMIT), kind)
    out = []
    for key, bs, merged in pieces:
        out.append(
            Surface(
                _id_of(prefix, key, front) if len(pieces) > 1 or key else prefix,
                kind,
                file,
                _title_of(key, front) + (" (with the short parts that follow)" if merged else ""),
                bs,
                _is_generated(key, kind),
            )
        )
    seen: dict[str, int] = {}
    for s in out:  # unique ids, in order
        n = seen.get(s.id, 0)
        seen[s.id] = n + 1
        if n:
            s.id = f"{s.id}-{n + 1}"
    return out


def collect(root: Path = ROOT) -> list[Surface]:
    """Every prose surface of the tree at ``root``, in reading order, with slots assigned."""
    surfaces: list[Surface] = []
    paper = _notebook_blocks(root, "paper/paper.ipynb")
    abstract = [b for b in paper if b.path and b.path[0][1] in ("title", "abstract")]
    body = [b for b in paper if b not in abstract]
    if abstract:
        surfaces.append(
            Surface("paper/abstract", "paper", "paper/paper.ipynb", "title and abstract", abstract)
        )
    surfaces += _surfaces_from(body, "paper", "paper/paper.ipynb", "paper", 1, "front matter")
    surfaces += _surfaces_from(
        _notebook_blocks(root, "paper/supporting_material.ipynb"),
        "appendix",
        "paper/supporting_material.ipynb",
        "appendix",
        1,
        "front matter",
    )
    pages = sorted(root.glob("docs/*.md")) + sorted(root.glob("docs/user-guide/*.md"))
    for p in pages:
        rel = p.relative_to(root).as_posix()
        bs = _markdown_blocks(root, rel)
        surfaces += _surfaces_from(bs, "docs", rel, rel, 0, Path(rel).stem)
    for rel, kind in (("examples/adcs/case-model.md", "example"), ("README.md", "readme")):
        bs = _markdown_blocks(root, rel)
        surfaces += _surfaces_from(bs, kind, rel, rel, 0, Path(rel).stem)
    for rel in ("site/index.html", "site/history.html"):
        bs = _html_blocks(root, rel)
        surfaces += _surfaces_from(bs, "site", rel, rel, 0, Path(rel).stem)
    gb = _glossary_blocks(root)
    if gb:
        surfaces.append(
            Surface("glossary/long-forms", "glossary", "glossary.yaml", "long forms", gb)
        )
    surfaces = [s for s in surfaces if s.blocks]
    _assign_slots(surfaces)
    return surfaces


def _assign_slots(surfaces: list[Surface]) -> None:
    """Pack consecutive surfaces of one kind into slots of up to SLOT_SIZE words."""
    counters: dict[str, int] = {}
    current: dict[str, tuple[str, int]] = {}
    for s in surfaces:
        if s.generated:
            s.slot = "(glossary)"
            continue
        slot, used = current.get(s.kind, ("", 0))
        if not slot or used + s.words > SLOT_SIZE:
            counters[s.kind] = counters.get(s.kind, 0) + 1
            slot, used = f"{s.kind}-{counters[s.kind]:02d}", 0
        current[s.kind] = (slot, used + s.words)
        s.slot = slot


# ------------------------------------------------------------------ report


def summary(surfaces: list[Surface]) -> dict:
    kinds: dict[str, dict] = {}
    for s in surfaces:
        k = kinds.setdefault(s.kind, {"surfaces": 0, "words": 0, "generated_words": 0})
        k["surfaces"] += 1
        if s.generated:
            k["generated_words"] += s.words
        else:
            k["words"] += s.words
    slots = sorted({s.slot for s in surfaces if not s.generated})
    return {
        "kinds": kinds,
        "surfaces": len(surfaces),
        "words": sum(k["words"] for k in kinds.values()),
        "slots": len(slots),
    }


def as_json(surfaces: list[Surface]) -> dict:
    return {
        "summary": summary(surfaces),
        "surfaces": [
            {
                "id": s.id,
                "kind": s.kind,
                "file": s.file,
                "section": s.section,
                "first_location": s.first_loc,
                "words": s.words,
                "prose_words": s.prose_words,
                "generated": s.generated,
                "view": s.view,
                "slot": s.slot,
            }
            for s in surfaces
        ],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(ROOT), help="tree to list (default: the repository)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of the table")
    args = ap.parse_args(argv)
    surfaces = collect(Path(args.root))
    if args.json:
        print(json.dumps(as_json(surfaces), indent=1))
        return 0
    print(f"{'id':58} {'kind':9} {'words':>6}  {'slot':12} first location")
    for s in surfaces:
        print(f"{s.id[:58]:58} {s.kind:9} {s.words:6d}  {s.slot[:12]:12} {s.file} {s.first_loc}")
    sm = summary(surfaces)
    print()
    for kind, v in sm["kinds"].items():
        extra = (
            f" (+{v['generated_words']} generated, read elsewhere)" if v["generated_words"] else ""
        )
        print(f"{kind:9} {v['surfaces']:3d} surfaces {v['words']:7d} words{extra}")
    total = f"{sm['surfaces']:3d} surfaces {sm['words']:7d} words in {sm['slots']} reader slots"
    print(f"{'total':9} {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
