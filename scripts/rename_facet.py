"""The WP24 rename, one surface at a time: the word "facet" goes (WP24-scope-of-work.md).

    uv run python scripts/rename_facet.py --surface code --dry-run   # counts per file, no write
    uv run python scripts/rename_facet.py --surface code             # apply; regenerate and test
    uv run python scripts/rename_facet.py --surface all --dry-run --verbose   # also the lines left

Surfaces, in the order of the pushes (the scope's default A3):

``code``
    push 1: ``src``, the tests, the case code and its generated report, the paper and figure
    generators, the scripts, the manifests (``interface-contract.toml``,
    ``environment_values.toml``); the notebooks' code cells and cell ids and the register's
    backing references follow the names.
``derivation``
    push 2: the lemma scripts (``lemma_12_facet_gap.py`` moved to ``lemma_12_term_gap.py``), the
    findings; the references to the moved module in the tests and the paper source.
``paper``
    push 3: the notebooks' sources (Markdown and code; outputs are regenerated in the container of
    record), the register's fragments of paper rows, the paper pins, the length ledger, prior art.
``docs``
    push 4: the docs pages, the site page, the README, the vocabulary baseline, the register's
    fragments of docs rows; the site figure name moves with its pin.

Per file the script: protects the tau = infinity polyhedral sentences (the scope's default A1: the
word stays where a polyhedron is meant) and the names of files that a later surface moves; applies
the file-specific literals (the cell wording of the assignment sense), the name table (the scope's
A2 and the private names), the generic identifier rule (``facet`` inside an identifier becomes
``term``) and the prose vocabulary (word-boundary swaps: facet to term, the hyphenated compounds);
restores the protected text; and in Markdown adds the vocabulary tool's exempt marker to a
paragraph that keeps the word. A second run changes nothing (idempotent).

Never touched: ``work-packages/*.md`` (records; the contract's pinned sections are a hand edit),
``docs/superpowers/notes/`` (A5), ``paper/container/RECORD.md`` (A4), ``examples/adcs/model_v2/``
(the scope's never list), ``tests/test_vocabulary.py`` (A9, by hand), ``glossary.yaml`` (lands with
the last surface, as a patch), and the generated files (``proof_map_record.json``, the figures, the
notebook outputs), which are regenerated. What the script cannot decide (a sentence that carries the
geometry or the assignment) it leaves and counts as ``left``; ``--verbose`` prints those lines.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------- the tables

# A1: the polyhedral sense keeps the textbook word, verbatim (the review lists the sentences).
KEEP = (
    "relative interior of a facet",  # R1 (paper, axioms, build_generated, the case notebook)
    "The facet that blocks",  # L11
    "an edge or a facet with a zero normal",  # R1's failure mode (axioms)
)

MARKER = "<!-- vocab-exempt: facet -->"

# Record folders and names that keep their spelling wherever a file cites them (A5), and the
# vocabulary tool's exempt marker itself.
PROTECT = ("spike-facet-", "dup_facets", MARKER)

# A2 and the private names, applied at identifier boundaries, longest first.
NAMES = (
    ("facet_numbered_tables", "term_numbered_tables"),
    ("single_facet_termination", "single_term_termination"),
    ("exponents_and_facets", "exponents_and_terms"),
    ("_permute_live_facets", "_permute_live_terms"),
    ("EXACT_FACET_OPTIMUM", "EXACT_TERM_OPTIMUM"),
    ("_FACET_NUMBERED", "_TERM_NUMBERED"),
    ("facet_objective", "term_objective"),
    ("_facet_optimum", "_term_optimum"),
    ("_facet_option", "_cell_option"),
    ("facet_share_", "term_share_"),
    ("assign_facets", "assign_cells"),
    ("FACET_COLORS", "TERM_COLORS"),
    ("facet_labels", "cell_labels"),
    ("facet_record", "term_record"),
    ("facet_table", "term_table"),
    ("facet_step", "refit_step"),
    ("facet_line", "term_line"),
    ("facet_cols", "term_cols"),
    ("facet_gap", "term_gap"),
    ("by_facet", "by_cell"),
    ("facet_of", "term_of"),
    ("_facets", "_terms"),
    ("facet_", "cell_"),
)

# Strings that name a file a surface moves (or a build output it renames); applied in that
# surface's push to its own files and to the files that only reference the name.
RENAMES = {
    "code": (("paper/paper_facets.py", "paper/paper_terms.py"),),
    "derivation": (("derivation/lemma_12_facet_gap.py", "derivation/lemma_12_term_gap.py"),),
    "paper": (),
    "docs": (),
}
REF_TOKENS = {
    "code": (("paper_facets", "paper_terms"),),
    "derivation": (("lemma_12_facet_gap", "lemma_12_term_gap"),),
    "paper": (),
    # the site figure is a build output (docs/generated/ is not committed): the path and its pin;
    # the register's glossary references follow the glossary, which lands with the docs (A3)
    "docs": (("three-facets", "three-terms"), ("glossary:facet", "glossary:term")),
}

# The assignment sense in literal strings: the cell wording (A2: colours and labels by cell).
# Option values and code literals move with the names; the wording moves with the prose.
LITERALS_NAMES = (
    ('color="facet"', 'color="cell"'),
    ("color='facet'", "color='cell'"),
)
LITERALS_PROSE = (
    ("colour: facet", "colour: cell"),
    ("colour by facet", "colour by cell"),
    ("color by facet", "color by cell"),
    ("coloured by facet", "coloured by cell"),
    ("colouring designs by facet", "colouring designs by cell"),
    ("colouring by facet", "colouring by cell"),
    ("facet colouring", "cell colouring"),
    ("shaded by facet", "shaded by cell"),
    ("the facet's own rows", "the term's own cell"),
    ("the facet's rows", "the term's cell"),
    ("the facet whose term scores", "the term that scores"),
    ("facet whose term scores", "term that scores"),
)
LITERALS_BY_FILE = {
    "src/hyperbolic_trade_space/plotting.py": (
        (
            '[f"facet {k + 1}" for k in estimator.assign_facets(X)]',
            '[f"cell {k + 1}" for k in estimator.assign_cells(X)]',
        ),
        ('"""Facet of each row of ``X`` as', '"""Cell of each row of ``X`` as'),
        ('"facet 1" .. "facet K"', '"cell 1" .. "cell K"'),
        ("becomes the facet labels", "becomes the cell labels"),
        ("legend ``facet 1 .. facet K``", "legend ``cell 1 .. cell K``"),
        ('color != "facet"', 'color != "cell"'),
        ('color == "facet"', 'color == "cell"'),
        ('{None, "facet"}', '{None, "cell"}'),
        ('or "facet", default=None', 'or "cell", default=None'),
        ("the string 'facet'", "the string 'cell'"),
        ("or 'facet' (the assigned facet)", "or 'cell' (the assigned cell)"),
        ('``"facet"``', '``"cell"``'),
        ("facet = np.asarray(estimator.assign_facets", "cell = np.asarray(estimator.assign_cells"),
        ("(facet == k)", "(cell == k)"),
    ),
    "src/hyperbolic_trade_space/estimator.py": (
        ('"""Facet of each row: ``argmax_k', '"""Cell of each row: ``argmax_k'),
    ),
    "examples/adcs/k_terms.py": (('labels == f"facet {f + 1}"', 'labels == f"cell {f + 1}"'),),
    "tests/test_plotting.py": (
        ('{f"facet {k + 1}" for k in range(3)}', '{f"cell {k + 1}" for k in range(3)}'),
        ('== ["facet 1"]', '== ["cell 1"]'),
        ('"facet 1" in _texts(ax)', '"cell 1" in _texts(ax)'),
        ('match="facet"', 'match="cell"'),
    ),
}

# The prose vocabulary, word-boundary aware, compounds before the bare word.
PROSE = (
    (r"\b[Ss]everal-facet\b", lambda m: m.group(0)[0] + "everal-term"),
    (r"\b[Mm]ulti-facet\b", lambda m: ("S" if m.group(0)[0] == "M" else "s") + "everal-term"),
    (r"\b[Ss]ingle-facet\b", lambda m: ("O" if m.group(0)[0] == "S" else "o") + "ne-term"),
    (r"\b([A-Za-z]+)-facets?\b", r"\1-term"),
    (r"\bfacet-(?=[A-Za-z])", "term-"),
    (r"\bFacet-(?=[A-Za-z])", "Term-"),
    (r"\bfacets\b", "terms"),
    (r"(?<=\\n)facets\b", "terms"),  # after an escaped newline in a code string
    (r"\bFacets\b", "Terms"),
    (r"\bFACETS\b", "TERMS"),
    (r"\bfacet\b", "term"),
    (r"(?<=\\n)facet\b", "term"),
    (r"\bFacet\b", "Term"),
    (r"\bFACET\b", "TERM"),
)

# Sentences the swap keeps true but the vocabulary wants in the cell wording, or that carry the
# geometry: flagged for the hand pass (counted as ``review``; printed with --verbose).
REVIEW = re.compile(
    r"facet'?s? (own )?rows|rows (assigned|belonging) to|assigned to (each|that|the|one) facet|"
    r"facets? (that |which )?(it |k )?dominates|maximizing facet|facet that dominates|which facet|"
    r"facet for the geometry|facets meet|piece of the surface|segment per facet|"
    r"facet'?s near-frontier|designs (of|in) (a|the|that|each) facet|"
    r"a monomial and a facet|one flat facet|single-facet frontier",
    re.I,
)

WORD = re.compile(r"facet", re.I)
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

# --------------------------------------------------------------------------- the surfaces


@dataclass(frozen=True)
class Surface:
    own: tuple  # globs: names, literals and prose
    names_only: tuple = ()  # globs: names and this surface's reference tokens, no prose
    refs: tuple = ()  # globs: this surface's reference tokens only


SURFACES: dict[str, Surface] = {
    "code": Surface(
        own=(
            "src/hyperbolic_trade_space/*.py",
            "tests/test_*.py",
            "examples/adcs/*.py",
            "examples/adcs/experiments/sensitivity.py",
            "examples/adcs/experiments/reports/sensitivity.json",
            "paper/*.py",
            "paper/figures/*.py",
            "scripts/build_*.py",
            "paper/environment_values.toml",
            "work-packages/interface-contract.toml",
        ),
        names_only=(
            "paper/paper.ipynb",
            "paper/supporting_material.ipynb",
            "examples/adcs/adcs_trade_study.ipynb",
            "claims_register.toml",
        ),
    ),
    "derivation": Surface(
        own=(
            "derivation/*.py",
            "derivation/PROOF_MAP_FINDINGS.md",
            "tests/test_derivation.py",
            "tests/test_proof_map.py",
        ),
        refs=("paper/paper.ipynb",),
    ),
    "paper": Surface(
        own=(
            "paper/paper.ipynb",
            "paper/supporting_material.ipynb",
            "examples/adcs/adcs_trade_study.ipynb",
            "paper/length_ledger.toml",
            "paper/prior_art.yaml",
            "tests/test_paper.py",
            "tests/test_narrative.py",
            "claims_register.toml",
        ),
    ),
    "docs": Surface(
        own=(
            "docs/*.md",
            "docs/user-guide/*.md",
            "site/index.html",
            "README.md",
            "scripts/vocabulary_baseline.toml",
            "tests/test_site.py",
            "tests/test_docs.py",
            "tests/test_build_generated.py",
            "claims_register.toml",
        ),
    ),
}
ORDER = ("code", "derivation", "paper", "docs")

# Tests whose prose pins belong to a later surface: names only in the code push.
LATER_TESTS = {
    "tests/test_paper.py",
    "tests/test_narrative.py",
    "tests/test_derivation.py",
    "tests/test_proof_map.py",
    "tests/test_site.py",
    "tests/test_docs.py",
    "tests/test_build_generated.py",
}
# Never edited by the script (the reason is printed in the dry run).
SKIP = {
    "tests/test_vocabulary.py": "A9: the fixture's made-up term is replaced by hand",
    "tests/test_rename_facet.py": "this script's own fixture uses the word on purpose",
    "tests/test_diagnostic_pair.py": "asserts the absence of the word; its meaning must not flip",
    "paper/container/RECORD.md": "A4: past entries are records",
}
GENERATED = {
    "derivation/proof_map_record.json": "regenerated: python -m derivation.proofmap --update",
    "paper/figures/figure1.svg": "regenerated: uv run python scripts/build_figures.py",
}
BLOCKED = {
    "examples/adcs/model_v2/diagnostic_pair.py": (
        "the scope's never list, but it calls case.facet_table, est.facet_ and est.facet_share_ "
        "and strips the column name 'facet': a question for the PM"
    ),
    "CHANGELOG.md": "not in the scope's blast radius: a question for the PM",
    "paper/BROWSER_NOTES.md": "not in the scope's blast radius (a record of browser passes?)",
}

# --------------------------------------------------------------------------- the passes


@dataclass
class Report:
    rel: str
    mode: str
    names: int = 0
    prose: int = 0
    kept: int = 0
    review: int = 0
    left: int = 0
    outputs: int = 0
    changed: bool = False
    moved: str = ""
    lines: list = field(default_factory=list)  # (kind, text) for --verbose

    def row(self) -> str:
        extra = f" outputs={self.outputs}" if self.outputs else ""
        extra += f" moved -> {self.moved}" if self.moved else ""
        return (
            f"  {self.rel:58s} {self.mode:10s} names={self.names:<4d} prose={self.prose:<4d} "
            f"kept={self.kept:<2d} review={self.review:<3d} left={self.left:<4d}{extra}"
        )


def _ident_sub(old: str, new: str, text: str) -> tuple[str, int]:
    pat = re.compile(f"(?<![A-Za-z0-9_]){re.escape(old)}(?![A-Za-z0-9_])")
    return pat.subn(new, text)


def _generic_identifier(token: str) -> str:
    if "_" not in token or not WORD.search(token):
        return token
    for a, b in (
        ("facets", "terms"),
        ("facet", "term"),
        ("Facets", "Terms"),
        ("Facet", "Term"),
        ("FACETS", "TERMS"),
        ("FACET", "TERM"),
    ):
        token = token.replace(a, b)
    return token


class Renamer:
    """The passes over one text, with the protection of what must not move."""

    def __init__(self, surface: str, rel: str):
        self.surface, self.rel = surface, rel
        later = [t for s in ORDER if s != surface for t, _ in REF_TOKENS[s]]
        self.protect = [*KEEP, *PROTECT, *later]

    def _shield(self, text: str) -> tuple[str, list[str]]:
        saved: list[str] = []
        for phrase in self.protect:
            while phrase in text:
                saved.append(phrase)
                text = text.replace(phrase, f"\x00{len(saved) - 1}\x00", 1)
        return text, saved

    @staticmethod
    def _restore(text: str, saved: list[str]) -> str:
        return re.sub(r"\x00(\d+)\x00", lambda m: saved[int(m.group(1))], text)

    def names(self, text: str) -> tuple[str, int]:
        text, saved = self._shield(text)
        n = 0
        for old, new in REF_TOKENS[self.surface]:
            text, k = _ident_sub(old, new, text)
            n += k
        for old, new in (*LITERALS_NAMES, *LITERALS_BY_FILE.get(self.rel, ())):
            n += text.count(old)
            text = text.replace(old, new)
        for old, new in NAMES:
            text, k = _ident_sub(old, new, text)
            n += k

        def gen(m):
            nonlocal n
            out = _generic_identifier(m.group(0))
            n += out != m.group(0)
            return out

        text = IDENT.sub(gen, text)
        return self._restore(text, saved), n

    def refs(self, text: str) -> tuple[str, int]:
        n = 0
        for old, new in REF_TOKENS[self.surface]:
            text, k = _ident_sub(old, new, text)
            n += k
        return text, n

    def prose(self, text: str) -> tuple[str, int]:
        text, saved = self._shield(text)
        n = 0
        for old, new in LITERALS_PROSE:
            n += text.count(old)
            text = text.replace(old, new)
        for pat, rep in PROSE:
            text, k = re.subn(pat, rep, text)
            n += k
        return self._restore(text, saved), n

    def kept(self, text: str) -> int:
        return sum(text.count(p) for p in KEEP)


def mark_kept_paragraphs(text: str) -> tuple[str, int]:
    """Prepend the exempt marker to every Markdown paragraph that keeps a polyhedral sentence."""
    blocks = re.split(r"(\n\s*\n)", text)
    n = 0
    for i in range(0, len(blocks), 2):
        b = blocks[i]
        if any(p in b for p in KEEP) and MARKER not in b:
            lead = re.match(r"\s*", b).group(0)
            blocks[i] = lead + MARKER + "\n" + b[len(lead) :]
            n += 1
    return "".join(blocks), n


def apply_text(r: Renamer, text: str, mode: str, rep: Report, markdown: bool) -> str:
    rep.review += len(REVIEW.findall(text))
    for m in REVIEW.finditer(text):
        s = text.rfind("\n", 0, m.start()) + 1
        rep.lines.append(("review", text[s : text.find("\n", m.end())].strip()[:160]))
    if mode == "refs":
        text, k = r.refs(text)
        rep.names += k
        return text
    text, k = r.names(text)
    rep.names += k
    if mode == "own":
        text, k = r.prose(text)
        rep.prose += k
        if markdown:
            text, _ = mark_kept_paragraphs(text)
    rep.kept += r.kept(text)
    return text


def process_file(surface: str, rel: str, mode: str, root: Path, write: bool) -> Report:
    path = root / rel
    rep = Report(rel, mode)
    r = Renamer(surface, rel)
    raw = path.read_text(encoding="utf-8")
    if rel.endswith(".ipynb"):
        nb = json.loads(raw)
        for cell in nb.get("cells", []):
            src = "".join(cell.get("source", []))
            md = cell.get("cell_type") == "markdown"
            new = apply_text(r, src, mode, rep, markdown=md)
            if new != src:
                cell["source"] = new.splitlines(keepends=True)
            if "id" in cell and mode != "refs":
                cell["id"], k = r.names(cell["id"])
                rep.names += k
            for out in cell.get("outputs", []):
                rep.outputs += len(WORD.findall(json.dumps(out)))
        text = json.dumps(nb, indent=1, ensure_ascii=False) + "\n"
        body = "".join("".join(c.get("source", [])) for c in nb.get("cells", []))
    elif rel == "claims_register.toml":
        text = apply_register(surface, raw, rep)
        body = text
    else:
        text = apply_text(r, raw, mode, rep, markdown=rel.endswith(".md"))
        body = text
    stripped = body
    for phrase in (*KEEP, *PROTECT):
        stripped = stripped.replace(phrase, "")
    rep.left = len(WORD.findall(stripped))
    for line in stripped.splitlines():
        if WORD.search(line):
            rep.lines.append(("left", line.strip()[:160]))
    rep.changed = text != raw
    if write and rep.changed:
        path.write_text(text, encoding="utf-8")
    return rep


def _owner(rel: str) -> str | None:
    """The surface whose push moves the prose of ``rel`` (for the register's fragments)."""
    from fnmatch import fnmatch

    for s in ORDER:
        if any(fnmatch(rel, g) for g in SURFACES[s].own) and rel != "claims_register.toml":
            return s
    return None


def apply_register(surface: str, raw: str, rep: Report) -> str:
    """Backing references follow the code push; a row's fragment, anchor and note follow the push
    of the file the row cites."""
    blocks = raw.split("[[claim]]")
    out = [blocks[0]]
    for b in blocks[1:]:
        m = re.search(r'^file = "([^"]*)"', b, re.M)
        rel = m.group(1) if m else ""
        r = Renamer(surface, rel)
        lines = []
        in_backing = False
        for line in b.splitlines(keepends=True):
            key = line.split(" = ", 1)[0] if " = " in line else ""
            if key == "backing" or in_backing:  # test and function names move with the code,
                in_backing = "]" not in line  # a moved file's name with its surface
                line, k = r.names(line) if surface == "code" else r.refs(line)
                rep.names += k
            elif key in ("fragment", "anchor", "note") and _owner(rel) == surface:
                line = apply_text(r, line, "own", rep, markdown=False)
            elif key in ("fragment", "anchor", "note") and surface == "code":
                line, k = r.names(line)  # a code name quoted in a sentence follows the code
                rep.names += k
            lines.append(line)
        out.append("".join(lines))
    return "[[claim]]".join(out)


# --------------------------------------------------------------------------- the surfaces' files


def expand(root: Path, globs: tuple) -> list[str]:
    seen: list[str] = []
    for g in globs:
        for p in sorted(root.glob(g)):
            rel = p.relative_to(root).as_posix()
            if p.is_file() and rel not in seen:
                seen.append(rel)
    return seen


def surface_files(surface: str, root: Path) -> list[tuple[str, str]]:
    s = SURFACES[surface]
    files: list[tuple[str, str]] = []
    for rel in expand(root, s.own):
        if rel in SKIP or rel in BLOCKED or rel in GENERATED:
            continue
        mode = "names" if surface == "code" and rel in LATER_TESTS else "own"
        files.append((rel, mode))
    have = {rel for rel, _ in files}
    for rel in expand(root, s.names_only):
        if rel not in have and rel not in SKIP:
            files.append((rel, "names"))
            have.add(rel)
    for rel in expand(root, s.refs):
        if rel not in have:
            files.append((rel, "refs"))
    return files


def move_files(surface: str, root: Path, write: bool) -> list[str]:
    done = []
    for old, new in RENAMES[surface]:
        if (root / old).exists() and not (root / new).exists():
            done.append(f"{old} -> {new}")
            if write:
                rc = subprocess.run(["git", "mv", old, new], cwd=root, capture_output=True)
                if rc.returncode != 0:
                    (root / old).rename(root / new)
    return done


def run_surface(surface: str, root: Path, write: bool, verbose: bool) -> list[Report]:
    print(f"\n== surface {surface} ({'apply' if write else 'dry run'})")
    for mv in move_files(surface, root, write):
        print(f"  move   {mv}")
    reports = []
    for rel, mode in surface_files(surface, root):
        rep = process_file(surface, rel, mode, root, write)
        reports.append(rep)
        if rep.names or rep.prose or rep.kept or rep.left or rep.review or rep.outputs:
            print(rep.row())
    if surface == "code":
        for rel, why in (*SKIP.items(), *BLOCKED.items(), *GENERATED.items()):
            if (root / rel).exists():
                n = len(WORD.findall((root / rel).read_text(encoding="utf-8", errors="replace")))
                print(f"  {rel:58s} {'untouched':10s} facet={n:<4d} {why}")
    tot = {
        k: sum(getattr(r, k) for r in reports)
        for k in ("names", "prose", "kept", "review", "left", "outputs")
    }
    print(
        f"  total: files changed {sum(r.changed for r in reports)}, "
        + ", ".join(f"{k} {v}" for k, v in tot.items())
    )
    if verbose:
        for rep in reports:
            for kind, line in rep.lines:
                print(f"  {kind:7s} {rep.rel}: {line}")
    return reports


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--surface", required=True, choices=[*ORDER, "all"])
    ap.add_argument("--dry-run", action="store_true", help="print the counts; write nothing")
    ap.add_argument("--verbose", action="store_true", help="print the lines left and to review")
    ap.add_argument("--root", default=str(ROOT), help="tree to rename (tests use this)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    for s in ORDER if args.surface == "all" else [args.surface]:
        run_surface(s, root, write=not args.dry_run, verbose=args.verbose)
    return 0


if __name__ == "__main__":
    sys.exit(main())
