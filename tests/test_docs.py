"""Docs checks over the docsite (user pages): citations, tag ranges, API coverage, statuses and
tolerances in the termination page, the policy paragraph not restated, the register's phrases and
runnable code blocks (offline). The preserved sources of the moved pages are checked in
``tests/test_paper_sources.py``."""

import re
from pathlib import Path

import pytest

import hyperbolic_trade_space
from derivation.axioms import AXIOMS

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SOURCES = DOCS / "superpowers" / "notes" / "paper-sources"
GLOSSARY_YAML = ROOT / "glossary.yaml"


def docsite_pages():
    """Hand-written docsite pages, recursive: not the generated glossary, not the notes."""
    return sorted(
        p
        for p in DOCS.rglob("*.md")
        if p.relative_to(DOCS).parts[0] not in ("generated", "superpowers")
    )


PAGES = [p.relative_to(DOCS).as_posix() for p in docsite_pages()]

BIB_KEYS = set(
    re.findall(r"^@\w+\{([^,\s]+),", (DOCS / "references.bib").read_text(encoding="utf-8"), re.M)
)
CITE_RE = re.compile(r"\[(@[^\]]+)\]")
LEMMA_RE = re.compile(r"\bL(\d+)\b")
LEDGER_RE = re.compile(r"\b([AIRF]\d+)\b")


def _text(page):
    return (DOCS / page).read_text(encoding="utf-8")


def _guide_text():
    """api.md and the user-guide pages together."""
    return "\n".join(_text(p) for p in PAGES if p == "api.md" or p.startswith("user-guide/"))


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
def test_lemma_tags_and_ledger_ids_in_range(page):
    """A docsite page that names a lemma or a ledger id names one that exists."""
    text = _text(page)
    assert all(1 <= int(n) <= 14 for n in LEMMA_RE.findall(text))
    assert [i for i in LEDGER_RE.findall(text) if i not in AXIOMS] == []


def test_every_exported_name_appears_in_api():
    text = _guide_text()
    missing = [n for n in hyperbolic_trade_space.__all__ if n not in text]
    assert missing == []


def test_submodule_functions_appear_in_api():
    text = _guide_text()
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
    assert [n for n in names if n not in text] == []


# ---- the policy paragraph is not restated on the docsite; statuses and tolerances are documented
def test_policy_paragraph_not_restated_on_the_docsite():
    for page in PAGES:
        text = _text(page)
        assert "all models are wrong" not in text.lower(), f"{page} restates the policy"
        assert len(re.findall(r"Map and territory", text)) <= 1, page


def test_statuses_and_tolerances_documented():
    termination = _text("user-guide/termination.md")
    guide = _guide_text()
    statuses = (
        "certified",
        "stationary_without_margin",
        "uncertified",
        "guard_stop",
        "iteration_cap",
        "not_applicable",
    )
    for st in statuses:
        assert f"`{st}`" in termination, st
        assert st in guide, st
    for const in ("EPS_KKT", "EPS_FEAS", "GUARD_TOL", "POLISH_STEPS"):
        assert const in termination, const
    for field in ("termination_", "conditioning_"):
        assert field in termination and field in guide, field


# ------------------------------------------------------------------ the register's phrases
NOTATION = ROOT / "docs/superpowers/notes/notation.md"


def _register_list(label):
    """Phrases from the bullet list under a heading or bold lead containing ``label``, or None."""
    lines = NOTATION.read_text(encoding="utf-8").splitlines()
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
    pages = pages or PAGES
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
    preserved = "\n".join(
        f.read_text(encoding="utf-8") for f in sorted(SOURCES.glob("*.md"))
    ).lower()
    source = GLOSSARY_YAML.read_text(encoding="utf-8").lower()
    assert [p for p in phrases if p.lower() in text] == []
    assert [p for p in phrases if p.lower() in preserved] == [], "paper-sources"
    assert [p for p in phrases if p.lower() in source] == [], "glossary.yaml"


# ------------------------------------------------------------------ runnable code blocks (R-18)
RUNNABLE_RE = re.compile(r"^```python \{\.runnable\}\n(.*?)^```", re.M | re.S)


def _runnable_blocks(page):
    return RUNNABLE_RE.findall(_text(page))


RUNNABLE_PAGES = [p for p in PAGES if _runnable_blocks(p)]


def test_runnable_blocks_exist_where_the_guide_promises_them():
    assert "getting-started.md" in RUNNABLE_PAGES
    assert sum(len(_runnable_blocks(p)) for p in RUNNABLE_PAGES) >= 5


@pytest.mark.slow
@pytest.mark.parametrize("page", RUNNABLE_PAGES)
def test_runnable_blocks_execute(page, monkeypatch):
    """Each page's blocks run in order, in one namespace, offline, on seeded synthetic data."""
    import matplotlib

    matplotlib.use("Agg")
    namespace = {"__name__": "__docs_block__"}
    for i, block in enumerate(_runnable_blocks(page), 1):
        exec(compile(block, f"{page}[block {i}]", "exec"), namespace)
    import matplotlib.pyplot as plt

    plt.close("all")


@pytest.mark.slow
def test_choosing_k_pages_cubesat_numbers_are_the_blocks_output(monkeypatch):
    """The page's cubesat sentences quote what its blocks print on the regenerated record
    (thirteen metrics, 3,000 designs per regime): each pinned fragment is in the prose and in the
    output, to the digits the page gives (no more than the reading of a break needs)."""
    import contextlib
    import io

    import matplotlib

    matplotlib.use("Agg")
    page = "user-guide/choosing-k.md"
    out = io.StringIO()
    namespace = {"__name__": "__docs_block__"}
    with contextlib.redirect_stdout(out):
        for i, block in enumerate(_runnable_blocks(page), 1):
            exec(compile(block, f"{page}[block {i}]", "exec"), namespace)
    printed = out.getvalue()
    prose = " ".join(_text(page).split())
    pinned = [
        # (the fragment of the prose, the fragments of the output it quotes)
        ("The primary regime drops by 0.078, then 0.023, 0.012 and 0.005",
         ["drops [0.078 0.023 0.012 0.005]"]),
        ("a break at K = 2, where the thinnest term holds 0.28 (0.21 at K = 3)",
         ["K=2 slack=0.043 thinnest=0.28", "K=3 slack=0.020 thinnest=0.21"]),
        ("The stock regime drops by 0.055, 0.031, 0.012 and 0.010, bending with no break",
         ["drops [0.055 0.031 0.012 0.01 ]"]),
        ("0.35 at K = 2 and 0.13 at K = 3",
         ["K=2 slack=0.060 thinnest=0.35", "K=3 slack=0.030 thinnest=0.13"]),
        ("0.18 to 0.20 at K = 2, 0.15 to 0.29 at K = 3 and 0.14 to 0.95 at K = 4",
         ["2 [0.2  0.2  0.18]", "3 [0.15 0.29 0.16]", "4 [0.14 0.95 0.79]"]),
    ]  # fmt: skip
    for sentence, fragments in pinned:
        assert sentence in prose, sentence
        for fragment in fragments:
            assert fragment in printed, (sentence, fragment)
