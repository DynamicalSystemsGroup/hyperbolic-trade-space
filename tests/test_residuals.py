"""The residual-pass tooling (scripts/prose_surfaces.py, scripts/check_residuals.py).

Each pattern is planted and counted, the report keeps its form, the checker edits nothing, and the
committed baseline has the report's shape. Thresholds are not tested, and the numbers of the
repository's own prose are not pinned here (the baseline records them; a pass compares against it).
"""

import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_residuals as cr  # noqa: E402
import prose_surfaces as ps  # noqa: E402

BASELINE = ROOT / "scripts" / "residuals_baseline.json"

GLOSSARY = """entries:
  - id: configuration
    term: 'configuration'
    short: 'The design variables the engineer chooses.'
    formal: 'the design variables of one evaluated design'
    not: 'an input of the fit'
"""

PLANTED = """# A page

This section describes the method. It is very robust and perhaps somewhat general. Note that the
fit (which was run twice on the same table, with the same seed, by the same person) converged.

The fit converged on the table of designs. The table of designs converged on the fit of designs.

The configuration is chosen by the engineer. The PCA step runs; the KKT check follows; the result
stands because the fit is convex, which holds when the temperature is positive, since the maximum
is smooth, although the data are noisy and the table, which is long, is split. The GP (geometric
program) is solved.
"""

SECOND = "# Other\n\nA configuration (the design variables) is an input. The API is documented.\n"


@pytest.fixture
def tree(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "glossary.yaml").write_text(GLOSSARY, encoding="utf-8")
    (tmp_path / "README.md").write_text(PLANTED, encoding="utf-8")
    (tmp_path / "docs" / "other.md").write_text(SECOND, encoding="utf-8")
    return tmp_path


def _digest(root: Path) -> dict:
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_inventory_lists_each_surface_once_with_words(tree):
    surfaces = ps.collect(tree)
    ids = [s.id for s in surfaces]
    assert len(ids) == len(set(ids))
    kinds = {s.kind for s in surfaces}
    assert {"readme", "docs", "glossary"} <= kinds
    assert all(s.words > 0 and s.slot for s in surfaces)
    assert sum(s.words for s in surfaces if s.kind == "docs") == len(
        ps._markdown_blocks(tree, "docs/other.md")[1].text.split()
    ) + len(ps._markdown_blocks(tree, "docs/other.md")[0].text.split())


def test_inventory_splits_an_oversized_page_and_keeps_its_words(tmp_path):
    body = "# Page\n\n" + "\n\n".join(
        f"## Part {i}\n\n" + ("word " * 400).strip() + "." for i in range(1, 9)
    )
    (tmp_path / "README.md").write_text(body, encoding="utf-8")
    surfaces = ps.collect(tmp_path)
    assert len(surfaces) > 1
    assert sum(s.words for s in surfaces) == len(
        [w for b in ps._markdown_blocks(tmp_path, "README.md") for w in b.text.split()]
    )


def test_each_pattern_is_counted(tree):
    rep = cr.report(tree)
    s = rep["surfaces"]["README.md"]
    assert s["metanarration"] >= 2  # "This section describes", "Note that"
    assert s["hedges"] >= 2  # "perhaps", "somewhat"
    assert s["intensifiers"] >= 2  # "very", "robust"
    assert s["long_parens"] == 1  # the parenthetical of 16 words
    assert s["restatements"] >= 1  # the second sentence repeats the first
    assert s["deep_clauses"] >= 1  # "which holds ... since ... although ... which"
    assert s["compound"] >= 1  # two semicolons
    assert s["long_sentences"] >= 1


def test_acronyms_and_terms_report_first_use_and_definition(tree):
    docs = cr.report(tree)["documents"]
    acr = {a["acronym"]: a for a in docs["README.md"]["acronyms"]}
    assert acr["GP"]["defined_at_first_use"] is True  # expanded in parentheses
    assert acr["PCA"]["defined_at_first_use"] is False
    assert acr["KKT"]["expanded_anywhere"] is False
    assert docs["README.md"]["acronyms_undefined_at_first_use"] == 2
    other = {a["acronym"]: a for a in docs["docs/other.md"]["acronyms"]}
    assert other["API"]["defined_at_first_use"] is False
    terms = {t["term"]: t for t in docs["docs/other.md"]["terms"]}
    assert terms["configuration"]["defined_at_first_use"] is True  # "configuration (the ...)"
    first = {t["term"]: t for t in docs["README.md"]["terms"]}["configuration"]
    assert first["first_location"].startswith("line ")


def test_the_report_is_stable_in_form_and_in_content(tree):
    first, second = cr.report(tree), cr.report(tree)
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert set(first) == {"schema", "thresholds", "totals", "surfaces", "documents"}
    assert first["schema"] == cr.SCHEMA
    for v in first["surfaces"].values():
        assert set(cr.COUNT_KEYS) <= set(v)
        assert {"words", "prose_words", "sentences", "mean_sentence", "max_sentence"} <= set(v)
    for d in first["documents"].values():
        assert set(d) == {
            "acronyms",
            "acronyms_undefined_at_first_use",
            "acronyms_never_expanded",
            "terms",
            "terms_undefined_at_first_use",
        }


def test_the_checker_edits_nothing(tree, capsys):
    before = _digest(tree)
    assert cr.main(["--root", str(tree)]) == 0
    assert cr.main(["--root", str(tree), "--json"]) == 0
    assert ps.main(["--root", str(tree)]) == 0
    capsys.readouterr()
    assert _digest(tree) == before


def test_compare_lists_a_rise_and_strict_fails(tree, tmp_path_factory, capsys):
    base = tmp_path_factory.mktemp("base") / "base.json"
    assert cr.main(["--root", str(tree), "--write-baseline", str(base)]) == 0
    assert cr.main(["--root", str(tree), "--compare", str(base), "--strict"]) == 0
    (tree / "README.md").write_text(PLANTED + "\nIn summary, it is very very robust.\n", "utf-8")
    assert cr.main(["--root", str(tree), "--compare", str(base)]) == 0
    assert cr.main(["--root", str(tree), "--compare", str(base), "--strict"]) == 1
    out = capsys.readouterr().out
    assert "README.md: intensifiers" in out


def test_the_committed_baseline_has_the_reports_shape():
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    assert base["head"]
    assert set(base) == {"head", "schema", "thresholds", "totals", "surfaces", "documents"}
    assert base["schema"] == cr.SCHEMA
    assert set(cr.COUNT_KEYS) <= set(next(iter(base["surfaces"].values())))


def test_every_prose_file_of_the_repository_is_inventoried():
    files = {s.file for s in ps.collect(ROOT)}
    expected = {
        "paper/paper.ipynb",
        "paper/supporting_material.ipynb",
        "README.md",
        "glossary.yaml",
    }
    expected |= {p.relative_to(ROOT).as_posix() for p in ROOT.glob("docs/*.md")}
    expected |= {p.relative_to(ROOT).as_posix() for p in ROOT.glob("docs/user-guide/*.md")}
    expected |= {"site/index.html", "site/history.html"}
    assert expected <= files
