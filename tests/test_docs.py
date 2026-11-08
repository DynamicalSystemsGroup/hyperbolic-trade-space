"""WP3 docs checks: citations, lemma tags, ledger ids and API coverage (offline)."""

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
    assert all(1 <= n <= 11 for n in tags)


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
