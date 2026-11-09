"""Docs checks: citations, lemma tags, ledger ids, API coverage, the policy paragraph, the three
levels and the register's phrases (offline)."""

import re
from pathlib import Path

import pytest

import hyperbolic_trade_space
from derivation.axioms import AXIOMS

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PAGES = ["preconditioning.md", "api.md"]

BIB_KEYS = set(re.findall(r"^@\w+\{([^,\s]+),", (DOCS / "references.bib").read_text(), re.M))
CITE_RE = re.compile(r"\[(@[^\]]+)\]")
LEMMA_RE = re.compile(r"\bL(\d+)\b")
LEDGER_RE = re.compile(r"\b([AIRF]\d+)\b")


def _text(page):
    return (DOCS / page).read_text()


def _keys(text):
    keys = []
    for group in CITE_RE.findall(text):
        keys += [k.strip().lstrip("@") for k in group.split(";")]
    return keys


@pytest.mark.parametrize("page", PAGES)
def test_citation_keys_resolve(page):
    keys = _keys(_text(page))
    assert BIB_KEYS
    assert [k for k in keys if k not in BIB_KEYS] == []


@pytest.mark.parametrize("page", PAGES)
def test_lemma_tags_in_range(page):
    tags = [int(n) for n in LEMMA_RE.findall(_text(page))]
    assert tags, "page cites no lemma"
    assert all(1 <= n <= 14 for n in tags)


@pytest.mark.parametrize("page", PAGES)
def test_ledger_ids_exist(page):
    ids = LEDGER_RE.findall(_text(page))
    assert ids, "page cites no ledger id"
    assert [i for i in ids if i not in AXIOMS] == []


def test_pages_cite_something():
    assert _keys(_text("api.md"))  # api.md cites bibliography keys


def test_every_exported_name_appears_in_api():
    api = _text("api.md")
    missing = [n for n in hyperbolic_trade_space.__all__ if n not in api]
    assert missing == []


def test_submodule_functions_appear_in_api():
    api = _text("api.md")
    names = [
        "knn_gap_scores",
        "find_holes",
        "frontier_targets",
        "orient_by_pca",
        "TensionReport",
        "plot_tensions",
        "plot_log_plane",
        "plot_frontier_surface_3d",
        "plot_frontier_coordinates",
        "plot_v_by_variable",
    ]
    assert [n for n in names if n not in api] == []


# ---- the method page: policy paragraph, three levels, stopping declaration, statuses
HEADING_RE = re.compile(r"^(#+)\s+(.*?)\s*$", re.M)


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


# ------------------------------------------------------------------ the register's phrases
NOTATION = ROOT / "docs/superpowers/notes/notation.md"


def _register_list(label):
    """Phrases from the bullet list under a heading or bold lead containing ``label``, or None."""
    lines = NOTATION.read_text().splitlines()
    start = next(
        (
            i
            for i, ln in enumerate(lines)
            if label in ln and (ln.startswith("#") or ln.startswith("**"))
        ),
        None,
    )
    if start is None:
        return None
    phrases = []
    for ln in lines[start + 1 :]:
        if ln.startswith("#") or ln.startswith("**"):
            break
        if ln.lstrip().startswith(("- ", "* ")):
            quoted = re.findall(r"`([^`]+)`|\"([^\"]+)\"", ln)
            found = [a or b for a, b in quoted]
            phrases += (
                found if found else [re.split(r"\s+[-\u2014:]\s+", ln.lstrip()[2:])[0].strip()]
            )
    return phrases


def _prose(pages=None):
    pages = pages or sorted(f.name for f in DOCS.glob("*.md"))
    return "\n".join(re.sub(r"<!--.*?-->", "", _text(p)) for p in pages)


def test_register_phrases_present():
    phrases = _register_list("Register phrases")
    if phrases is None:
        pytest.skip("notation.md has no 'Register phrases' subsection yet")
    assert phrases, "the 'Register phrases' subsection lists nothing"
    text = _prose().lower()
    assert [p for p in phrases if p.lower() not in text] == []


def test_forbidden_phrases_absent():
    phrases = _register_list("Forbidden phrases")
    if phrases is None:
        pytest.skip("notation.md has no 'Forbidden phrases' subsection yet")
    assert phrases, "the 'Forbidden phrases' subsection lists nothing"
    text = _prose().lower()
    assert [p for p in phrases if p.lower() in text] == []
