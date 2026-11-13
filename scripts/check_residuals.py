"""Report the mechanical patterns of machine-written prose, per surface. A report, never an edit.

The reader's brief: docs/superpowers/notes/residual-review.md. The surfaces:
scripts/prose_surfaces.py. A count sends a reader to a sentence; the reader decides. Nothing here
changes a file.

Per surface (visible prose, math and code removed, tables left out of the sentence counts):

``metanarration``     openers that announce or summarize ("This section", "Note that")
``hedges``            "may", "might", "perhaps", "somewhat", "generally" and the like
``intensifiers``      "very", "crucial", "robust", "seamless", "importantly" and the like
``parens``            parentheticals; ``long_parens`` those of eight words or more;
                      ``path_parens`` those holding a repository path;
                      ``dense_paras`` paragraphs with three or more; ``max_parens`` the most in one
``restatements``      a sentence that repeats most of the content words of the one before
``long_sentences``    sentences over 35 words; ``mean_sentence``, ``max_sentence`` in words
``compound``          sentences joining ideas with two or more semicolons or colons
``deep_clauses``      sentences with four or more subordinating words

Per document (a file): every acronym (two to six capitals) and every glossary term, with the place
of its first use and whether a definition (an expansion in parentheses, "is", "means", "called", a
glossary or notation link) is in that paragraph. The project's own terms are checked against
``glossary.yaml`` by ``scripts/check_vocabulary.py``; this report only locates first uses.

    uv run python scripts/check_residuals.py                    # the report as a table
    uv run python scripts/check_residuals.py --json             # the same as JSON
    uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json
    uv run python scripts/check_residuals.py --compare ... --strict   # exit 1 if a count rose
    uv run python scripts/check_residuals.py --write-baseline scripts/residuals_baseline.json
    uv run python scripts/check_residuals.py --root DIR         # another tree (tests use this)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_vocabulary as cv
import prose_surfaces as ps

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASELINE = ROOT / "scripts" / "residuals_baseline.json"
SCHEMA = 1

LONG_SENTENCE = 35  # words
LONG_PAREN = 8  # words inside one parenthetical
DENSE_PARAS = 3  # parentheticals in one paragraph
DEEP_CLAUSE = 4  # subordinating words in one sentence
COMPOUND = 2  # semicolons plus colons in one sentence
OVERLAP = 0.6  # shared content words, over the smaller sentence, that count as a restatement
MIN_CONTENT = 4  # content words a sentence needs to be compared

# Counts a pass should not raise (compared against the baseline).
COUNT_KEYS = (
    "metanarration",
    "hedges",
    "intensifiers",
    "parens",
    "long_parens",
    "path_parens",
    "dense_paras",
    "restatements",
    "long_sentences",
    "compound",
    "deep_clauses",
)

_META = {
    "this-section": (
        r"\b(this|the next|the following|the present) "
        r"(section|subsection|appendix|paragraph|chapter)\b"
    ),
    "in-this": r"\bin this (section|paper|appendix|page|note|paragraph)\b",
    "we-now": r"\bwe (now|then|next) \w+",
    "we-turn": r"\b(we|let us) (turn|proceed|move on|return) to\b",
    "as-said": (
        r"\bas (noted|discussed|mentioned|described|shown|seen|stated|explained) "
        r"(above|below|earlier|before|previously)\b"
    ),
    "as-we-see": r"\bas we (will|shall) see\b",
    "remainder": r"\b(the remainder|the rest) of (this|the)\b",
    "worth-noting": (
        r"\bit is (worth|important to) "
        r"(noting|mentioning|emphasi[sz]ing|note|recogni[sz]e|remember)\b"
    ),
    "should-be-noted": r"\bit should be (noted|emphasi[sz]ed|stressed)\b",
    "note-that": r"(^|[.;:]\s+)note that\b",
    "recall-that": r"(^|[.;:]\s+)recall that\b",
    "summary": (
        r"\b(in summary|in short|in brief|in conclusion|to summari[sz]e|to sum up|taken together)\b"
    ),
    "restating": r"\b(put differently|in other words|that is to say|to be clear|to put it)\b",
    "here-we": r"(^|[.;:]\s+)(here|below),? (we|is|are)\b",
    "this-gives": (
        r"\bthis (section|paragraph|appendix|page) "
        r"(describes|explains|shows|gives|summari[sz]es|introduces|presents|collects)\b"
    ),
}
_HEDGE = re.compile(
    r"\b(may|might|could|perhaps|possibly|presumably|arguably|somewhat|fairly|quite|relatively|"
    r"generally|typically|usually|often|sometimes|likely|unlikely|tends? to|appears? to|seems? to|"
    r"roughly|in principle|to some extent|more or less|largely|mostly|probably|rather(?! than))\b",
    re.I,
)
_INTENSIFIER = re.compile(
    r"\b(very|highly|extremely|truly|genuinely|really|crucial(ly)?|vital(ly)?|essential(ly)?|"
    r"fundamental(ly)?|remarkabl[ey]|notabl[ey]|importantly|powerful(ly)?|seamless(ly)?|robust(ly)?|"
    r"comprehensive(ly)?|elegant(ly)?|rigorous(ly)?|carefully|simply|merely|entirely|completely|"
    r"clearly|obviously|of course|indeed|in fact|actually|effectively|ultimately|naturally|"
    r"inherently|leverag(e|es|ed|ing)|delve[sd]?|cutting-edge|state-of-the-art|novel)\b",
    re.I,
)
_SUBORD = re.compile(
    r"\b(which|whereas|although|though|because|since|while|unless|if|when|whose|where|whether|"
    r"until|once|so that|that)\b",
    re.I,
)
_ABBREV = re.compile(r"\b(e\.g|i\.e|etc|et al|cf|vs|Fig|Figs|Eq|Eqs|Sec|No|approx|resp|viz)\.")
_PAREN = re.compile(r"\(([^()]*)\)")
_REPO_DIRS = "docs|paper|src|scripts|tests|examples|derivation|site|work-packages"
_EXT = "md|py|toml|yaml|yml|json|ipynb|html|bib|sysml|txt|npz|cff"
_PATH = re.compile(
    rf"(?<![\w/.-])(?:(?:{_REPO_DIRS})/[\w.-]+(?:/[\w.-]+)*|[\w-]+(?:/[\w.-]+)*\.(?:{_EXT}))(?![\w-])"
)
_ACRONYM = re.compile(r"(?<![\w.#/-])([A-Z]{2,6})(?:s)?(?![\w-])")
_NOT_ACRONYMS = {
    "I", "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "OK", "AND", "OR", "NOT",
    "IF", "SO", "NO", "IS", "TODO", "NB", "PM", "AM", "BC", "AD", "USD",
}  # fmt: skip
_STOP = cv.STOP | {"that", "this", "with", "from", "have", "which", "their", "there", "these"}


# ------------------------------------------------------------------ sentences


def sentences(text: str) -> list[str]:
    t = _ABBREV.sub(lambda m: m.group(0).replace(".", "\ue000"), text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(\[*_`])", t)
    return [p.replace("\ue000", ".").strip() for p in parts if p.strip()]


def content_words(sentence: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]{3,}", sentence.lower()) if w not in _STOP}


def _analysable(b: ps.Block) -> bool:
    return not b.table and b.heading == 0


# ------------------------------------------------------------------ per surface


def path_parens(raw: str) -> int:
    """Parentheticals holding a repository path, a code span included (it reads the same
    rendered); fenced code, link targets, math and comments do not count."""
    t = re.sub(r"^[ \t]*(```+|~~~+).*?^[ \t]*\1[ \t]*$", " ", raw, flags=re.S | re.M)
    t = re.sub(r"<!--.*?-->|\$\$.*?\$\$", " ", t, flags=re.S)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)  # a link keeps its words, not its target
    t = re.sub(r"(?<![\\\w])\$[^$\n]+?\$", " ", t)
    t = t.replace("`", "")
    return sum(
        1
        for m in _PAREN.finditer(t)
        if _PATH.search(m.group(1)) and not (m.start() and t[m.start() - 1].isalnum())
    )  # a call such as f(a/b.py) is code, not a parenthetical


def surface_counts(s: ps.Surface) -> dict:
    c = {k: 0 for k in COUNT_KEYS}
    patterns: dict[str, int] = {}
    n_sent = 0
    lens: list[int] = []
    max_parens = 0
    paras = 0
    for b in s.blocks:
        if not _analysable(b):
            continue
        paras += 1
        text = b.text
        low = text.lower()
        for name, pat in _META.items():
            n = len(re.findall(pat, low if name != "x" else text, re.I))
            if n:
                c["metanarration"] += n
                patterns[name] = patterns.get(name, 0) + n
        c["hedges"] += len(_HEDGE.findall(text))
        c["intensifiers"] += len(_INTENSIFIER.findall(text))
        pars = _PAREN.findall(text)
        c["parens"] += len(pars)
        c["long_parens"] += sum(1 for p in pars if len(p.split()) >= LONG_PAREN)
        c["path_parens"] += path_parens(b.raw)
        c["dense_paras"] += 1 if len(pars) >= DENSE_PARAS else 0
        max_parens = max(max_parens, len(pars))
        prev: set[str] = set()
        for sent in sentences(text):
            n_sent += 1
            n_words = len(sent.split())
            lens.append(n_words)
            c["long_sentences"] += n_words > LONG_SENTENCE
            c["compound"] += (sent.count(";") + sent.count(":")) >= COMPOUND
            c["deep_clauses"] += len(_SUBORD.findall(sent)) >= DEEP_CLAUSE
            cw = content_words(sent)
            enough = len(cw) >= MIN_CONTENT and len(prev) >= MIN_CONTENT
            if enough and len(cw & prev) / min(len(cw), len(prev)) >= OVERLAP:
                c["restatements"] += 1
            prev = cw
    out = {
        "words": s.words,
        "prose_words": s.prose_words,
        "paragraphs": paras,
        "sentences": n_sent,
        **c,
        "max_parens": max_parens,
        "mean_sentence": round(sum(lens) / len(lens), 1) if lens else 0.0,
        "max_sentence": max(lens, default=0),
    }
    if patterns:
        out["metanarration_by_pattern"] = dict(sorted(patterns.items()))
    return out


# ------------------------------------------------------------------ per document


def _expansion_cues(tok: str) -> list[re.Pattern]:
    t = re.escape(tok)
    return [
        re.compile(r"\w[\w\s,-]{3,80}\(\s*" + t + r"s?\s*\)"),  # words (ACR)
        re.compile(r"\b" + t + r"s?\s*\([^)]{5,80}\)"),  # ACR (expansion)
        re.compile(r"\b" + t + r"s?\s+(stands for|is short for|means|denotes|is the|is a|is an)\b"),
        re.compile(r"\b(known as|called|abbreviated|short for)\s+" + t + r"\b"),
    ]


def _glossary_phrases(root: Path) -> dict[str, list[str]]:
    path = root / "glossary.yaml"
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = {}
    for e in data.get("entries", []):
        out[e["id"]] = [e["term"], *(e.get("aliases") or [])]
    return out


def _term_regex(phrases: list[str]) -> re.Pattern:
    alts = sorted((re.escape(p).replace(r"\ ", r"[\s\-]+") for p in phrases), key=len, reverse=True)
    return re.compile(r"(?<![\w-])(" + "|".join(alts) + r")(?:s|es)?(?![\w-])", re.I)


_LINK_CUE = re.compile(r"glossary|notation|\{term\}|\{ref\}`?(?:sub-)?a-|appendix[-\s]a\b", re.I)


def document_report(blocks: list[tuple[str, ps.Block]], glossary: dict[str, list[str]]) -> dict:
    """First uses of acronyms and glossary terms in one document's blocks, in reading order."""
    acr: dict[str, dict] = {}
    for sid, b in blocks:
        if b.table:
            continue
        for m in _ACRONYM.finditer(b.text):
            tok = m.group(1)
            if tok in _NOT_ACRONYMS:
                continue
            a = acr.setdefault(
                tok,
                {
                    "first_surface": sid,
                    "first_location": b.loc,
                    "count": 0,
                    "_cues": _expansion_cues(tok),
                    "defined_at_first_use": None,
                    "expanded_anywhere": False,
                },
            )
            a["count"] += 1
            defined = any(p.search(b.text) for p in a["_cues"]) or bool(_LINK_CUE.search(b.raw))
            if a["defined_at_first_use"] is None:
                a["defined_at_first_use"] = defined
            if any(p.search(b.text) for p in a["_cues"]):
                a["expanded_anywhere"] = True
    acronyms = []
    for tok in sorted(acr):
        a = acr[tok]
        a.pop("_cues")
        acronyms.append({"acronym": tok, **a})
    terms = []
    for gid, phrases in glossary.items():
        rx = _term_regex(phrases)
        first = None
        count = 0
        for _sid, b in blocks:
            if b.table:
                continue
            hits = len(rx.findall(b.text))
            if hits:
                count += hits
                if first is None:
                    first = (sid, b)
        if first:
            sid, b = first
            defined = cv.has_definition_cue(b.raw, phrases) or bool(_LINK_CUE.search(b.raw))
            terms.append(
                {
                    "term": gid,
                    "first_surface": sid,
                    "first_location": b.loc,
                    "count": count,
                    "defined_at_first_use": bool(defined),
                }
            )
    terms.sort(key=lambda t: t["term"])
    return {
        "acronyms": acronyms,
        "acronyms_undefined_at_first_use": sum(
            1 for a in acronyms if not a["defined_at_first_use"]
        ),
        "acronyms_never_expanded": sum(1 for a in acronyms if not a["expanded_anywhere"]),
        "terms": terms,
        "terms_undefined_at_first_use": sum(1 for t in terms if not t["defined_at_first_use"]),
    }


# ------------------------------------------------------------------ the report


def report(root: Path = ROOT) -> dict:
    surfaces = ps.collect(root)
    glossary = _glossary_phrases(root)
    rep_surfaces = {s.id: {"file": s.file, "kind": s.kind, **surface_counts(s)} for s in surfaces}
    by_file: dict[str, list[tuple[str, ps.Block]]] = {}
    for s in surfaces:
        by_file.setdefault(s.file, []).extend((s.id, b) for b in s.blocks)
    documents = {f: document_report(bs, glossary) for f, bs in sorted(by_file.items())}
    totals = {
        k: sum(v[k] for v in rep_surfaces.values())
        for k in ("words", "prose_words", "sentences", *COUNT_KEYS)
    }
    totals["acronyms_undefined_at_first_use"] = sum(
        d["acronyms_undefined_at_first_use"] for d in documents.values()
    )
    totals["acronyms_never_expanded"] = sum(
        d["acronyms_never_expanded"] for d in documents.values()
    )
    totals["terms_undefined_at_first_use"] = sum(
        d["terms_undefined_at_first_use"] for d in documents.values()
    )
    return {
        "schema": SCHEMA,
        "thresholds": {
            "long_sentence_words": LONG_SENTENCE,
            "long_paren_words": LONG_PAREN,
            "dense_paragraph_parens": DENSE_PARAS,
            "deep_clause_subordinators": DEEP_CLAUSE,
            "compound_semicolons_colons": COMPOUND,
            "restatement_overlap": OVERLAP,
        },
        "totals": totals,
        "surfaces": rep_surfaces,
        "documents": documents,
    }


def file_totals(rep: dict) -> dict:
    out: dict[str, dict] = {}
    for v in rep["surfaces"].values():
        t = out.setdefault(v["file"], {k: 0 for k in COUNT_KEYS})
        for k in COUNT_KEYS:
            t[k] += v[k]
    for f, d in rep["documents"].items():
        t = out.setdefault(f, {k: 0 for k in COUNT_KEYS})
        t["acronyms_undefined_at_first_use"] = d["acronyms_undefined_at_first_use"]
        t["terms_undefined_at_first_use"] = d["terms_undefined_at_first_use"]
    return out


RISE_KEYS = (*COUNT_KEYS, "acronyms_undefined_at_first_use", "terms_undefined_at_first_use")


def compare(current: dict, base: dict) -> list[str]:
    """Rises against the baseline, by file (stable under renamed headings) and by surface."""
    rises = []
    cf, bf = file_totals(current), file_totals(base)
    for f, t in cf.items():
        b = bf.get(f)
        if b is None:
            rises.append(f"{f}: new file (not in the baseline)")
            continue
        for k in RISE_KEYS:
            if t.get(k, 0) > b.get(k, 0):
                rises.append(f"{f}: {k} {b.get(k, 0)} -> {t.get(k, 0)}")
    for sid, v in current["surfaces"].items():
        b = base["surfaces"].get(sid)
        if b is None:
            continue
        for k in COUNT_KEYS:
            if v[k] > b[k]:
                rises.append(f"{sid}: {k} {b[k]} -> {v[k]}")
    return rises


def _head(root: Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def print_table(rep: dict) -> None:
    keys = ("words", "metanarration", "hedges", "intensifiers", "parens", "long_parens")
    keys += ("restatements", "long_sentences", "compound", "deep_clauses")
    short = (
        "words",
        "meta",
        "hedge",
        "intens",
        "paren",
        "lparen",
        "restat",
        "longs",
        "compd",
        "deepc",
    )
    print(f"{'surface':50} " + " ".join(f"{h:>6}" for h in short))
    for sid, v in rep["surfaces"].items():
        print(f"{sid[:50]:50} " + " ".join(f"{v[k]:6d}" for k in keys))
    t = rep["totals"]
    print(f"{'TOTAL':50} " + " ".join(f"{t[k]:6d}" for k in keys))
    print("\nper document: acronyms and glossary terms met before a definition")
    print(f"{'document':50} {'acr':>4} {'undef':>6} {'noexp':>6} {'terms':>6} {'undef':>6}")
    for f, d in rep["documents"].items():
        cells = (
            len(d["acronyms"]),
            d["acronyms_undefined_at_first_use"],
            d["acronyms_never_expanded"],
            len(d["terms"]),
            d["terms_undefined_at_first_use"],
        )
        print(f"{f[:50]:50} " + " ".join(f"{c:6d}" for c in cells))
    print(
        f"\nacronyms undefined at first use: {t['acronyms_undefined_at_first_use']}; "
        f"never expanded: {t['acronyms_never_expanded']}; glossary terms without a "
        f"definition at first use: {t['terms_undefined_at_first_use']}"
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(ROOT), help="tree to report on (default: the repository)")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--compare", help="baseline JSON; print the counts that rose")
    ap.add_argument("--strict", action="store_true", help="with --compare, exit 1 if a count rose")
    ap.add_argument("--write-baseline", help="write the report, with the head, to this JSON file")
    args = ap.parse_args(argv)
    root = Path(args.root)
    rep = report(root)
    if args.write_baseline:
        head = _head(root)
        note = f"taken at the dev head {head}; taken again when the pass starts"
        out = {"head": head, "note": note, **rep}
        Path(args.write_baseline).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
        print(f"baseline written: {args.write_baseline} (head {out['head']})")
        return 0
    if args.json:
        print(json.dumps(rep, indent=1))
    else:
        print_table(rep)
    if args.compare:
        base = json.loads(Path(args.compare).read_text(encoding="utf-8"))
        rises = compare(rep, base)
        print(f"\nagainst the baseline (head {base.get('head', '?')}): {len(rises)} count(s) rose")
        for r in rises:
            print("  " + r)
        if rises and args.strict:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
