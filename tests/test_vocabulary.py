"""The vocabulary tool (scripts/check_vocabulary.py): each kind of violation is planted and caught,
a clean fixture passes, and the tool runs over the real repository against a committed baseline."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_vocabulary as cv  # noqa: E402

GLOSSARY = """
entries:
  - id: 'tile'
    term: 'tile'
    short: 'One monomial piece of the fitted surface.'
    register: 'tile'
    formal: 'one term'
    not: 'a cluster'
    aliases:
      - 'tiles'
  - id: 'elasticity'
    term: 'elasticity'
    short: 'The percentage given up per percentage gained.'
    register: 'elasticity'
    formal: 'a ratio of exponents'
    not: 'a price'
    avoid:
      - phrase: 'exchange rate'
        reason: 'reads as money'
  - id: 'fit-temperature'
    term: 'fit temperature'
    short: 'How hard the maximum is.'
    register: 'fit temperature'
    formal: 'tau'
    not: 'a physical temperature'
assumed:
  - term: 'convex program'
    reason: 'Boyd and Vandenberghe'
stems:
  - 'tile'
  - 'temperature'
  - 'program'
"""

CLEAN_PAPER = [
    "---\ntitle: T\nabstract: |\n  A fit uses elasticity.\n---\n\n## Method\n\n"
    "A **tile** is one piece. The elasticity is read along each tile, at the fit "
    "temperature as a convex program, with the fit temperature fixed.",
]


def make_tree(tmp_path, paper=None, docs=None, glossary=GLOSSARY, html=None):
    (tmp_path / "glossary.yaml").write_text(glossary, encoding="utf-8")
    (tmp_path / "paper").mkdir()
    cells = [{"cell_type": "markdown", "source": [t]} for t in (paper or CLEAN_PAPER)]
    cells.append(
        {"cell_type": "code", "source": ["exchange rate = 1  # code is skipped"], "outputs": []}
    )
    nb = {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    (tmp_path / "paper" / "paper.ipynb").write_text(json.dumps(nb), encoding="utf-8")
    (tmp_path / "docs").mkdir()
    for name, text in (docs or {"index.md": "# Home\n\nThe tile and the elasticity.\n"}).items():
        (tmp_path / "docs" / name).write_text(text, encoding="utf-8")
    if html is not None:
        (tmp_path / "site").mkdir()
        (tmp_path / "site" / "index.html").write_text(html, encoding="utf-8")
    return tmp_path


def run(root, *extra):
    return cv.main(["--root", str(root), *extra])


def kinds(root):
    return {(v.kind, v.phrase) for v in cv.analyse(root)["violations"]}


def test_clean_fixture_passes(tmp_path, capsys):
    root = make_tree(tmp_path)
    assert run(root) == 0, capsys.readouterr().out
    assert kinds(root) == set()


def test_avoid_variant_fails(tmp_path):
    root = make_tree(tmp_path, docs={"a.md": "# A\n\nAt what exchange rate do we trade a tile?\n"})
    assert ("avoid", "exchange rate") in kinds(root)
    assert run(root) == 1


def test_avoid_variant_in_html_and_notebook_markdown_output(tmp_path):
    root = make_tree(tmp_path, html="<html><body><p>The exchange rate here.</p></body></html>")
    assert ("avoid", "exchange rate") in kinds(root)


def test_code_math_and_citations_are_skipped(tmp_path):
    text = (
        "# A\n\n```python\nexchange rate = 1\n```\n\nSee `exchange rate`, $exchange rate$, "
        "[@exchange2020] and the tile.\n"
    )
    root = make_tree(tmp_path, docs={"a.md": text})
    assert kinds(root) == set()


def test_exempt_marker_exempts_the_phrase_in_its_paragraph_only(tmp_path):
    text = (
        "# A\n\nThe source says <!-- vocab-exempt: exchange rate --> exchange rate for a tile.\n\n"
        "Here it is the exchange rate again.\n"
    )
    root = make_tree(tmp_path, docs={"a.md": text})
    assert [v for v in cv.analyse(root)["violations"] if v.kind == "avoid"]  # second paragraph
    only_first = "# A\n\nThe source says <!-- vocab-exempt: exchange rate --> exchange rate.\n"
    root2 = (
        make_tree(tmp_path / "b", docs={"a.md": only_first})
        if (tmp_path / "b").mkdir() is None
        else None
    )
    assert kinds(root2) == set()


def test_unresolved_stem_phrase_fails(tmp_path):
    root = make_tree(
        tmp_path, docs={"a.md": "# A\n\nThe sided program and the working temperature.\n"}
    )
    found = kinds(root)
    assert ("stem", "working temperature") in found
    assert ("stem", "sided program") in found
    assert run(root) == 1


def test_resolved_stem_phrases_pass(tmp_path):
    text = (
        "# A\n\nThe fit temperature, a convex program, each tile and the tiles; "
        "one tile; the temperature.\n"
    )
    root = make_tree(tmp_path, docs={"a.md": text})
    assert kinds(root) == set()


def test_undefined_first_use_fails_and_definition_cues_pass(tmp_path):
    bare = ["## M\n\nThe elasticity along a tile is read off.\n\nThe fit temperature is fixed.\n"]
    root = make_tree(tmp_path, paper=bare)
    assert ("first-use", "elasticity") in kinds(root)
    assert ("first-use", "tile") in kinds(root)
    assert run(root) == 1
    glossed = [
        "## M\n\nThe *elasticity* (the percentage given up per percentage gained) along a "
        "tile, see {numref}`Section %s <sect-x>`; the fit temperature, a knob, is fixed.\n"
    ]
    root2 = make_tree(tmp_path / "g", paper=glossed) if (tmp_path / "g").mkdir() is None else None
    assert not [v for v in cv.analyse(root2)["violations"] if v.kind == "first-use"]


def test_first_use_rule_ignores_the_abstract(tmp_path):
    paper = [
        "---\ntitle: T\nabstract: |\n  The elasticity of a tile.\n---\n\n## M\n\n"
        "A **tile**, an **elasticity**, a **fit temperature**.\n"
    ]
    root = make_tree(tmp_path, paper=paper)
    assert not [v for v in cv.analyse(root)["violations"] if v.kind == "first-use"]


def test_dead_entry_fails(tmp_path):
    root = make_tree(
        tmp_path, docs={"a.md": "# A\n\nThe tile only.\n"}, paper=["## M\n\nA **tile**.\n"]
    )
    found = kinds(root)
    assert ("dead-entry", "elasticity") in found
    assert ("dead-entry", "fit-temperature") in found
    assert ("dead-entry", "tile") not in found
    assert run(root) == 1


def test_appendix_a_notation_table_does_not_count_as_a_use(tmp_path):
    root = make_tree(
        tmp_path, docs={"a.md": "# A\n\nThe tile only.\n"}, paper=["## M\n\nA **tile**.\n"]
    )
    sm = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": ["## Appendix A. Notation and terms\n\nelasticity; fit temperature\n"],
            }
        ]
    }
    (root / "paper" / "supporting_material.ipynb").write_text(json.dumps(sm), encoding="utf-8")
    assert ("dead-entry", "elasticity") in kinds(root)


def test_baseline_hides_known_violations_only(tmp_path, capsys):
    root = make_tree(tmp_path, docs={"a.md": "# A\n\nThe exchange rate and a tile.\n"})
    base = tmp_path / "base.toml"
    base.write_text(cv.emit_baseline(cv.analyse(root)["violations"]), encoding="utf-8")
    assert run(root, "--baseline", str(base)) == 0
    (root / "docs" / "b.md").write_text("# B\n\nThe working temperature.\n", encoding="utf-8")
    assert run(root, "--baseline", str(base)) == 1
    assert "working temperature" in capsys.readouterr().out


def test_baseline_rows_need_an_owner_and_a_reason(tmp_path):
    base = tmp_path / "base.toml"
    base.write_text('[[violation]]\nkind = "avoid"\nfile = "x"\nphrase = "y"\n', encoding="utf-8")
    with pytest.raises(SystemExit):
        cv.load_baseline(base)


def test_report_has_density_and_once_used(tmp_path, capsys):
    root = make_tree(tmp_path)
    assert run(root, "--density") == 0
    out = capsys.readouterr().out
    assert "once-used terms" in out and "terms of art per 100 words" in out


BASELINE = ROOT / "scripts" / "vocabulary_baseline.toml"


def test_real_repo_has_no_new_vocabulary_violation(capsys):
    """Against the committed baseline: passes now, fails on a new violation."""
    code = cv.main(["--root", str(ROOT), "--baseline", str(BASELINE)])
    out = capsys.readouterr().out
    assert code == 0, out
    base = cv.load_baseline(BASELINE)
    assert all(r["owner"] and r["reason"] for r in base.values())


def test_the_documented_bare_command_exits_zero_on_the_repository(capsys):
    """`CLAUDE.md` gives the bare command: it reads the committed baseline by default."""
    assert cv.main([]) == 0, capsys.readouterr().out
    assert cv.main(["--no-baseline"]) == 1
