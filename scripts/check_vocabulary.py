"""Check the prose a reader sees against ``glossary.yaml``.

The rule: docs/superpowers/notes/vocabulary-review.md.

    uv run python scripts/check_vocabulary.py                 # non-zero exit on a new violation
    uv run python scripts/check_vocabulary.py --no-baseline   # every violation, known ones included
    uv run python scripts/check_vocabulary.py --density       # also the density table
    uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml
    uv run python scripts/check_vocabulary.py --emit-baseline # TOML of the current violations
    uv run python scripts/check_vocabulary.py --root DIR      # check another tree (tests use this)

Fails on four kinds of violation:

``avoid``
    a variant the glossary lists under an entry's ``avoid``.
``stem``
    a phrase built on a stem of ``stems`` (a modifier word directly before the stem) that is
    neither an entry term, an alias, nor an ``assumed`` term. A bare stem word is not a phrase.
``first-use``
    in ``paper/paper.ipynb`` (body, abstract excluded), the first use of an entry's term has no
    definition or cross-reference in its paragraph: no bold or italic marking, no gloss in
    parentheses or after a comma, no "is/means/called", no cross-reference role, no link to the
    glossary or notation.
``dead-entry``
    a glossary entry no prose uses (the Appendix A notation table, compiled from the glossary,
    does not count as a use).

Reports without failing: once-used terms (entries and assumed terms used exactly once), and with
``--density`` the terms of art per hundred words by section and the densest paragraphs.

Reads: the Markdown cells and Markdown outputs (generated tables and sentences) of
``paper/paper.ipynb`` and ``paper/supporting_material.ipynb``, ``docs/*.md``,
``docs/user-guide/*.md``, ``site/index.html``, ``README.md``,
``examples/adcs/case-model.md``, the docstrings under ``src/``, and the
``short``/``formal``/``not`` fields of ``glossary.yaml``. Skips code, math, citation keys,
link targets and work-packages records.

A sentence that reports a source in the source's own words is exempted for that phrase by a marker
in the same paragraph: ``<!-- vocab-exempt: phrase one; phrase two -->`` (Markdown) or the same in
an HTML comment. Never a blanket exclusion of a file.

A baseline file (TOML, ``[[violation]]`` with ``kind``, ``file``, ``phrase``, ``owner``,
``reason``) lists known violations: with a baseline the exit status reflects only violations not in
it. On the repository itself (no ``--root``) the baseline defaults to
``scripts/vocabulary_baseline.toml``; ``--no-baseline`` reads none. Baseline entries no longer
violated are reported as stale, not failed.
"""

from __future__ import annotations

import argparse
import ast
import html
import json
import re
import sys
import tomllib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASELINE = ROOT / "scripts" / "vocabulary_baseline.toml"

STOP = set(
    """a an the this that these those each every any no some all both either neither one two three
    four five six first second third last next other another same such own more most less few many
    much of in on at to for from by with without within into onto over under between among through
    per via as than then and or but nor if so not is are was were be been being has have had do does
    did can could will would shall should may might must which what who whom whose where when why
    how
    here there it its they their them we our us you your he she his her i my me also only just very
    too still even yet whether while whose about above below after before during up down out off
    again once further whole given fixed single new old good bad big small large high low
    full""".split()  # noqa: SIM905
)

# --------------------------------------------------------------------------- normalisation


def norm_token(tok: str) -> str:
    tok = tok.lower()
    if tok.endswith("'s"):
        tok = tok[:-2]
    if len(tok) > 3 and tok.endswith("s") and not tok.endswith(("ss", "us", "is")):
        tok = tok[:-1]
    return tok


def segments(text: str) -> list[list[str]]:
    """Normalised tokens, broken into runs at punctuation (a phrase never spans one)."""
    out = []
    for seg in re.split(r"[^\w\s'\-]", text.replace("_", " ")):
        toks = [
            norm_token(t) for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9']*", seg.replace("-", " "))
        ]
        if toks:
            out.append(toks)
    return out


def phrase_key(phrase: str) -> tuple[str, ...]:
    segs = segments(phrase)
    return tuple(t for s in segs for t in s)


# --------------------------------------------------------------------------- cleaning


@dataclass
class Para:
    file: str
    section: str
    raw: str
    text: str
    exempt: set = field(default_factory=set)
    abstract: bool = False
    generated_notation: bool = False


_MARK = re.compile(r"<!--\s*vocab-exempt:\s*(.*?)\s*-->", re.S)
_ROLE_RAW = re.compile(r"\{(numref|ref|prf:ref|eq|doc|cite|cite[pt]?|term|math)\}`")


def clean_markdown(src: str) -> str:
    s = re.sub(r"^(```+|~~~+).*?^\1[ \t]*$", " ", src, flags=re.S | re.M)  # fenced code
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"\$\$.*?\$\$", " ", s, flags=re.S)
    s = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)", " ", s, flags=re.S)
    s = re.sub(r"(?<![\\\w])\$[^$\n]+?\$", " ", s)
    s = re.sub(r"`[^`\n]*`", " ", s)  # inline code and roles
    s = re.sub(r"^\s*:{3,}\s*\{[^}]*\}\s*(.*)$", r"\1", s, flags=re.M)  # directive fence -> caption
    s = re.sub(r"^\s*:{3,}\s*$", " ", s, flags=re.M)
    s = re.sub(r"^\s*:\w[\w-]*:.*$", " ", s, flags=re.M)  # directive options
    s = re.sub(r"^\s*\([\w:.\-]+\)=\s*$", " ", s, flags=re.M)  # label targets
    s = re.sub(r"^\s*:::\s+\S+.*$", " ", s, flags=re.M)  # mkdocstrings
    s = re.sub(r"^\s*!!!\s+\w+(\s+\"[^\"]*\")?", " ", s, flags=re.M)  # admonitions
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[[^\]]*@[^\]]*\]", " ", s)  # citations
    s = re.sub(r"<https?://[^>]*>|https?://\S+", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"^[\s|:\-]+$", " ", s, flags=re.M)  # table rules
    s = re.sub(r"^\s*#+\s*", "", s, flags=re.M)
    return html.unescape(s)


def split_paras(file: str, text: str, section0: str = "") -> list[Para]:
    """Split Markdown into paragraphs, tracking the heading each sits under."""
    paras, section = [], section0
    for block in re.split(r"\n\s*\n", text):
        m = re.match(r"\s*(#{1,6})\s+(.*)", block)
        if m:
            section = m.group(2).strip()
        exempt = set()
        for mm in _MARK.finditer(block):
            exempt |= {phrase_key(p) for p in mm.group(1).split(";") if p.strip()}
        cleaned = clean_markdown(block)
        if cleaned.strip():
            paras.append(Para(file, section, block, cleaned, exempt))
    return paras


def front_matter(text: str):
    m = re.match(r"\s*---\n(.*?)\n---\s*\n?(.*)", text, re.S)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), m.group(2)


def read_notebook(root: Path, rel: str) -> list[Para]:
    path = root / rel
    if not path.is_file():
        return []
    nb = json.loads(path.read_text(encoding="utf-8"))
    paras, section = [], ""
    for cell in nb.get("cells", []):
        chunks = []
        if cell["cell_type"] == "markdown":
            chunks.append("".join(cell["source"]))
        elif cell["cell_type"] == "code":
            for out in cell.get("outputs", []):
                md = out.get("data", {}).get("text/markdown")
                if md:
                    chunks.append("".join(md) if isinstance(md, list) else md)
        for chunk in chunks:
            meta, body = front_matter(chunk)
            for key in ("title", "abstract"):
                if isinstance(meta.get(key), str):
                    ps = split_paras(rel, meta[key], key)
                    for p in ps:
                        p.abstract = True
                    paras += ps
            ps = split_paras(rel, body, section)
            if ps:
                section = ps[-1].section
            paras += ps
    for p in paras:
        if re.match(r"Appendix A\b", p.section):
            p.generated_notation = True
    return paras


def read_markdown(root: Path, rel: str) -> list[Para]:
    path = root / rel
    _, body = front_matter(path.read_text(encoding="utf-8"))
    return split_paras(rel, body)


def read_html(root: Path, rel: str) -> list[Para]:
    path = root / rel
    src = path.read_text(encoding="utf-8")
    src = re.sub(r"<(style|script|head)\b.*?</\1>", " ", src, flags=re.S | re.I)
    marks = _MARK.findall(src)
    src = re.sub(
        r"</?(p|div|li|h[1-6]|section|header|footer|main|ul|ol|br|tr|nav)\b[^>]*>", "\n\n", src
    )
    paras = []
    section = ""
    for block in re.split(r"\n\s*\n", src):
        text = clean_markdown(re.sub(r"<!--.*?-->", " ", block, flags=re.S))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            exempt = set()
            for mm in _MARK.finditer(block):
                exempt |= {phrase_key(p) for p in mm.group(1).split(";") if p.strip()}
            paras.append(Para(rel, section, block, text, exempt))
    del marks
    return paras


def read_docstrings(root: Path) -> list[Para]:
    paras = []
    for path in sorted((root / "src").rglob("*.py")) if (root / "src").is_dir() else []:
        rel = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                doc = ast.get_docstring(node)
                if doc:
                    doc = re.sub(r"^\s*>>>.*$|^\s*\.\.\. .*$", " ", doc, flags=re.M)
                    name = getattr(node, "name", "module")
                    paras += split_paras(rel, doc, name)
    return paras


def read_corpus(root: Path) -> list[Para]:
    paras = read_notebook(root, "paper/paper.ipynb") + read_notebook(
        root, "paper/supporting_material.ipynb"
    )
    for pattern in ("docs/*.md", "docs/user-guide/*.md"):
        for path in sorted(root.glob(pattern)):
            paras += read_markdown(root, path.relative_to(root).as_posix())
    if (root / "site/index.html").is_file():
        paras += read_html(root, "site/index.html")
    if (root / "README.md").is_file():
        paras += read_markdown(root, "README.md")
    if (root / "examples/adcs/case-model.md").is_file():
        paras += read_markdown(root, "examples/adcs/case-model.md")
    paras += read_docstrings(root)
    return paras


# --------------------------------------------------------------------------- glossary


@dataclass
class Glossary:
    entries: list
    assumed: list
    stems: set
    phrases: dict  # key tuple -> ("entry"|"assumed", id)
    avoid: dict  # key tuple -> (entry id, phrase, reason)
    max_len: int


def load_glossary(root: Path) -> Glossary:
    data = yaml.safe_load((root / "glossary.yaml").read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    assumed = data.get("assumed", []) or []
    stems = {norm_token(s) for s in data.get("stems", []) or []}
    phrases, avoid = {}, {}
    for e in entries:
        for p in [e["term"], *(e.get("aliases") or [])]:
            phrases[phrase_key(p)] = ("entry", e["id"])
        for a in e.get("avoid") or []:
            avoid[phrase_key(a["phrase"])] = (e["id"], a["phrase"], a.get("reason", ""))
    for a in assumed:
        phrases.setdefault(phrase_key(a["term"]), ("assumed", a["term"]))
    longest = max([len(k) for k in [*phrases, *avoid]] or [1])
    return Glossary(entries, assumed, stems, phrases, avoid, longest)


def match_spans(tokens: list[str], table: dict, max_len: int):
    """Longest, non-overlapping matches of ``table`` keys in ``tokens``: (start, end, value)."""
    i, out = 0, []
    while i < len(tokens):
        for n in range(min(max_len, len(tokens) - i), 0, -1):
            v = table.get(tuple(tokens[i : i + n]))
            if v is not None:
                out.append((i, i + n, v))
                i += n
                break
        else:
            i += 1
    return out


# --------------------------------------------------------------------------- the checks


@dataclass(frozen=True)
class Violation:
    kind: str
    file: str
    phrase: str
    where: str = ""
    context: str = ""

    @property
    def key(self):
        return (self.kind, self.file, self.phrase)


_DEF_CUES = re.compile(
    r"\*\*[^*]+\*\*|(?<!\*)\*[^*\s][^*]*\*(?!\*)|\bglossary\b|\bnotation\b|"
    r"\{(numref|ref|prf:ref|eq|doc)\}",
    re.I,
)


def has_definition_cue(raw: str, term_phrases: list[str]) -> bool:
    if _DEF_CUES.search(raw):
        return True
    for t in term_phrases:
        pat = re.escape(t).replace(r"\ ", r"[\s\-]+")
        if re.search(
            pat
            + r"s?\W{0,2}(\(|,\s+(the|a|an|which|where)\b|"
            + r"\s+((is|are)\s+(the|a|an|one|called|defined)|means|denotes|names)\b)",
            raw,
            re.I,
        ):
            return True
        if re.search(
            r"\b(called|call|named|name|say|termed)\s+(the\s+|a\s+)?[\"'*_]*" + pat, raw, re.I
        ):
            return True
    return False


def analyse(root: Path):
    g = load_glossary(root)
    paras = read_corpus(root)
    # glossary's own text (what the Glossary page shows): avoid check only
    gloss_paras = []
    for e in g.entries:
        for f in ("short", "formal", "not"):
            if e.get(f):
                gloss_paras.append(Para("glossary.yaml", e["id"], e[f], e[f]))
    violations: dict = {}
    usage = Counter()  # entry/assumed id -> uses outside the generated notation table
    first_seen: dict = {}
    density: dict = defaultdict(lambda: [0, 0])  # (file, section) -> [terms, words]
    dense_paras = []

    def add(v: Violation):
        violations.setdefault(v.key, v)

    all_terms = {k: v for k, v in g.phrases.items()}
    entry_terms: dict = defaultdict(list)
    for e in g.entries:
        entry_terms[e["id"]] = [e["term"], *(e.get("aliases") or [])]

    for p in [*paras, *gloss_paras]:
        glossary_text = p.file == "glossary.yaml"
        for seg in segments(p.text):
            for s, e_, (_eid, phrase, _reason) in (
                (a, b, v)
                for a, b, v in match_spans(seg, {k: v for k, v in g.avoid.items()}, g.max_len)
            ):
                key = tuple(seg[s:e_])
                if key in p.exempt:
                    continue
                add(
                    Violation(
                        "avoid", p.file, phrase, p.section, " ".join(seg[max(0, s - 4) : e_ + 4])
                    )
                )
        if glossary_text:
            continue
        nwords = len(re.findall(r"\w+", p.text))
        nterms = 0
        for seg in segments(p.text):
            spans = match_spans(seg, all_terms, g.max_len)
            covered, resolved = set(), set()
            for s, e_, (kind, ident) in spans:
                covered.update(range(s, e_))
                resolved.update(range(s, e_))  # a stem inside an entry or assumed term resolves
                nterms += 1
                if not p.generated_notation:
                    usage[ident] += 1
                if (
                    kind == "entry"
                    and p.file == "paper/paper.ipynb"
                    and not p.abstract
                    and not p.raw.lstrip().startswith("|")  # a generated table row is not prose
                ):
                    first_seen.setdefault(ident, p)
            for i, tok in enumerate(seg):
                if tok in g.stems and i not in resolved and i > 0:
                    prev = seg[i - 1]
                    if prev in STOP or len(prev) < 2 or prev.isdigit() or (i - 1) in covered:
                        continue
                    phrase = f"{prev} {tok}"
                    if (prev, tok) in p.exempt:
                        continue
                    add(
                        Violation(
                            "stem", p.file, phrase, p.section, " ".join(seg[max(0, i - 3) : i + 3])
                        )
                    )
        d = density[(p.file, p.section)]
        d[0] += nterms
        d[1] += nwords
        if nwords >= 15:
            dense_paras.append((nterms / nwords * 100, nterms, nwords, p))

    # undefined first use (paper body)
    for e in g.entries:
        p = first_seen.get(e["id"])
        if p is None:
            continue
        if not has_definition_cue(p.raw, entry_terms[e["id"]]):
            add(Violation("first-use", p.file, e["term"], p.section, p.text.strip()[:120]))

    # dead entries
    for e in g.entries:
        if usage[e["id"]] == 0:
            add(Violation("dead-entry", "glossary.yaml", e["id"], "", e["term"]))

    once = sorted(
        [e["term"] for e in g.entries if usage[e["id"]] == 1]
        + [a["term"] for a in g.assumed if usage[a["term"]] == 1]
    )
    return {
        "violations": sorted(violations.values(), key=lambda v: (v.kind, v.file, v.phrase)),
        "once": once,
        "density": density,
        "dense_paras": sorted(dense_paras, key=lambda t: -t[0]),
        "unused_assumed": sorted(a["term"] for a in g.assumed if usage[a["term"]] == 0),
    }


# --------------------------------------------------------------------------- baseline


def load_baseline(path: Path) -> dict:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    out = {}
    for row in data.get("violation", []):
        for f in ("kind", "file", "phrase", "owner", "reason"):
            if not row.get(f):
                raise SystemExit(f"baseline row lacks {f!r}: {row}")
        out[(row["kind"], row["file"], row["phrase"])] = row
    return out


OWNERS = (
    ("paper/", "WP10 paper stream"),
    ("docs/", "WP8a docsite stream"),
    ("site/", "WP8a root page"),
    ("README.md", "WP8a docsite stream"),
    ("src/", "package docstrings"),
    ("glossary.yaml", "PM (glossary)"),
)


def emit_baseline(violations) -> str:
    lines = [
        "# Known vocabulary violations (check_vocabulary.py). A row is a debt, with an owner;",
        "# the test fails on a violation not listed here. Remove a row when it is fixed.",
        "",
    ]
    for v in violations:
        owner = next((o for pre, o in OWNERS if v.file.startswith(pre)), "PM")
        reason = f"found at the first run of the tool; triage per vocabulary-review.md ({v.kind})"
        lines += [
            "[[violation]]",
            f"kind = {json.dumps(v.kind)}",
            f"file = {json.dumps(v.file)}",
            f"phrase = {json.dumps(v.phrase)}",
            f"owner = {json.dumps(owner)}",
            f"reason = {json.dumps(reason)}",
            "",
        ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- CLI


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(ROOT), help="tree to check (default: the repository)")
    ap.add_argument("--density", action="store_true", help="also print the density table")
    ap.add_argument("--baseline", help="TOML of known violations; exit status ignores them")
    ap.add_argument(
        "--no-baseline",
        action="store_true",
        help="read no baseline (the default only on the repository)",
    )
    ap.add_argument(
        "--emit-baseline", action="store_true", help="print the baseline TOML and exit 0"
    )
    args = ap.parse_args(argv)
    root = Path(args.root)
    res = analyse(root)
    vs = res["violations"]
    if args.emit_baseline:
        print(emit_baseline(vs))
        return 0
    baseline = args.baseline
    if baseline is None and not args.no_baseline and root.resolve() == ROOT:
        baseline = str(DEFAULT_BASELINE)
    base = load_baseline(Path(baseline)) if baseline else {}
    new = [v for v in vs if v.key not in base]
    known = [v for v in vs if v.key in base]
    stale = [k for k in base if k not in {v.key for v in vs}]
    for v in new:
        print(f"FAIL {v.kind}: {v.file} [{v.where}] {v.phrase!r}  ...{v.context}")
    if known:
        counts = Counter(v.kind for v in known)
        print(f"known (baseline): {dict(counts)}")
    if stale:
        print(f"stale baseline rows (fixed; remove): {len(stale)}")
        for k in stale:
            print(f"  {k}")
    print(f"once-used terms ({len(res['once'])}): {', '.join(res['once'])}")
    if res["unused_assumed"]:
        print(
            f"unused assumed terms ({len(res['unused_assumed'])}): "
            + ", ".join(res["unused_assumed"])
        )
    if args.density:
        print("\nterms of art per 100 words, by section")
        rows = [(t / w * 100 if w else 0, t, w, k) for k, (t, w) in res["density"].items()]
        for dens, t, w, (f, s) in sorted(rows, reverse=True)[:40]:
            print(f"{dens:6.1f}  {t:4d}/{w:<5d} {f} :: {s}")
        print("\ndensest paragraphs")
        for dens, _t, _w, p in res["dense_paras"][:15]:
            print(f"{dens:6.1f}  {p.file} [{p.section}] {' '.join(p.text.split())[:140]}")
    print(f"{len(new)} new violation(s), {len(known)} known")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
