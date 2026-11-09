"""The preserved sources of the pages that left the docsite (WP8a, Amendment 2).

``docs/superpowers/notes/paper-sources/`` holds verbatim snapshots of the six moved pages. The
assertions below used to guard the pages on the docsite; they keep guarding the same text here
(the policy paragraph exactly once, the three levels, the lemma and ledger citations, the
statuses and tolerances). WP10 repoints them to the paper's sources when the paper exists.
"""

import re
from pathlib import Path

import pytest

from derivation.axioms import AXIOMS

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SRC = DOCS / "superpowers" / "notes" / "paper-sources"

BIB_KEYS = set(re.findall(r"^@\w+\{([^,\s]+),", (DOCS / "references.bib").read_text(), re.M))
CITE_RE = re.compile(r"\[(@[^\]]+)\]")
LEMMA_RE = re.compile(r"\bL(\d+)\b")
LEDGER_RE = re.compile(r"\b([AIRF]\d+)\b")
HEADING_RE = re.compile(r"^(#+)\s+(.*?)\s*$", re.M)

SNAPSHOTS = [
    "method.md",
    "literature.md",
    "limitations.md",
    "preconditioning.md",
    "api.md",
    "why-and-how.md",
]


def _text(name):
    return (SRC / name).read_text()


def _keys(text):
    keys = []
    for group in CITE_RE.findall(text):
        keys += [k.strip().lstrip("@") for k in group.split(";")]
    return keys


def test_the_six_snapshots_and_the_move_table_exist():
    for name in [*SNAPSHOTS, "README.md"]:
        assert (SRC / name).is_file(), name


@pytest.mark.parametrize("page", ["preconditioning.md", "api.md"])
def test_preserved_citation_keys_resolve(page):
    keys = _keys(_text(page))
    assert BIB_KEYS
    assert [k for k in keys if k not in BIB_KEYS] == []


@pytest.mark.parametrize("page", ["preconditioning.md", "api.md"])
def test_preserved_lemma_tags_in_range(page):
    tags = [int(n) for n in LEMMA_RE.findall(_text(page))]
    assert tags, "page cites no lemma"
    assert all(1 <= n <= 14 for n in tags)


@pytest.mark.parametrize("page", ["preconditioning.md", "api.md"])
def test_preserved_ledger_ids_exist(page):
    ids = LEDGER_RE.findall(_text(page))
    assert ids, "page cites no ledger id"
    assert [i for i in ids if i not in AXIOMS] == []


def test_preserved_api_cites_something():
    assert _keys(_text("api.md"))


def test_map_and_territory_paragraph_exactly_once():
    method = _text("method.md")
    assert len(re.findall(r"^\*\*Map and territory\.\*\*", method, re.M)) == 1
    assert method.count("All models are wrong") == 1
    assert "abstraction-gaps.md" in method
    for page in ("why-and-how.md", "limitations.md", "api.md"):
        text = _text(page)
        assert "all models are wrong" not in text.lower(), f"{page} restates the policy"
        assert len(re.findall(r"Map and territory", text)) <= 1, page


def test_method_headings_for_three_levels_and_declaration():
    heads = [h for _, h in HEADING_RE.findall(_text("method.md"))]
    for needed in (
        "Three levels of guarantee",
        "Level 1: descent",
        "Level 2: numerical stationarity",
        "Level 3: conditional local optimality",
        "The stopping declaration",
    ):
        assert needed in heads, needed
    order = [heads.index(h) for h in heads if h.startswith(("Level 1", "Level 2", "Level 3"))]
    assert order == sorted(order)
    assert heads.index("The stopping declaration") > heads.index(
        "Level 3: conditional local optimality"
    )


def test_new_lemmas_cited_and_exist():
    method = _text("method.md")
    cited = {int(n) for n in LEMMA_RE.findall(method)}
    for n in (12, 13, 14):
        assert n in cited, f"L{n} not cited in method.md"
        assert list((ROOT / "derivation").glob(f"lemma_{n:02d}_*.py")), f"no module for L{n}"
    for name in ("Lemma 1", "Lemma 2", "Proposition 3", "Corollary 4"):
        assert name in method, name


def test_statuses_and_tolerances_documented():
    method, api = _text("method.md"), _text("api.md")
    statuses = (
        "certified",
        "stationary_without_margin",
        "uncertified",
        "guard_stop",
        "iteration_cap",
        "not_applicable",
    )
    for st in statuses:
        assert f"`{st}`" in method, st
        assert st in api, st
    for const in ("EPS_KKT", "EPS_FEAS", "GUARD_TOL", "POLISH_STEPS"):
        assert const in method and const in api, const
    for field in ("termination_", "conditioning_"):
        assert field in api, field
