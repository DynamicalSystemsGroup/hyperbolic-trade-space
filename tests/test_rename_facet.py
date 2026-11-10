"""scripts/rename_facet.py on a small fixture: the name table applied, the polyhedral sentence and
the records untouched, the register's rows moving with their surface, idempotent, and a dry run
that writes nothing."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import rename_facet as rf  # noqa: E402

SRC = '''"""Fit K monomial facets; ``color="facet"`` colours by the facet whose term scores it.

The one-facet fit is a geometric program; the several-facet fit is not. Per-facet gaps.
"""
import numpy as np


def facet_gap(U, w):
    """First-order gap of the facet refit on the facet's rows."""
    return float(np.max(U @ w))


def assign_facets(X):
    return np.array([f"facet {k + 1}" for k in range(2)])


class Est:
    facet_step = "support"

    def fit(self):
        self.facet_ = np.zeros(3)
        self.facet_share_ = np.ones(1)
        return single_facet_termination(self.facet_)


def single_facet_termination(lab):
    return lab
'''

LEMMA = '''"""L11: every exponent positive. The facet that blocks u' is one active at u, not at u'.

The facet refit is convex; see lemma_12_facet_gap.
"""
from derivation.lemma_12_facet_gap import L12_RESULT  # noqa: F401

TITLE = "facet first-order gap of a facet"
'''

RECORD = "# Records keep their wording: facet, facet_share_, the several-facet fit.\n"

PAPER_CELLS = [
    "**Words.** A term, a monomial and a facet are one object. The facet share is the fraction "
    "of near-frontier designs that facet $k$ dominates.",
    "**Conditions.** R1: the balanced point lies in the relative interior of a facet of the "
    "supporting envelope with positive normal. R2: every facet is nonempty.",
    "See `derivation/lemma_12_facet_gap.py` and `facet_share_`.",
]

REGISTER = """# register
[[claim]]
id = "C1"
fragment = "The facet share is the fraction of near-frontier designs that facet $k$ dominates"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_duplicate_facets", "glossary:facet"]
note = "facet shares sum to one"

[[claim]]
id = "C2"
fragment = "one facet per segment"
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["lemma:L10"]
"""

DOC = (
    "# Fitting\n\nWith K > 1 the frontier is bent: one facet per segment. "
    "`assign_facets(X)` reads which facet scores each design.\n\n"
    "![alt text of eight words or more for the figure]"
    "(../generated/figures/three-facets-light.png#only-light)\n"
)


def make_tree(tmp_path: Path) -> Path:
    root = tmp_path
    (root / "src/hyperbolic_trade_space").mkdir(parents=True)
    (root / "src/hyperbolic_trade_space/solvers.py").write_text(SRC, encoding="utf-8")
    (root / "derivation").mkdir()
    (root / "derivation/lemma_11_pareto.py").write_text(LEMMA, encoding="utf-8")
    (root / "derivation/lemma_12_facet_gap.py").write_text("L12_RESULT = 1\n", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests/test_solvers.py").write_text(
        "def test_duplicate_facets():\n    assert 'facet 1'\n", encoding="utf-8"
    )
    (root / "tests/test_vocabulary.py").write_text("GLOSSARY = 'facet'\n", encoding="utf-8")
    (root / "work-packages").mkdir()
    (root / "work-packages/WP1-review.md").write_text(RECORD, encoding="utf-8")
    (root / "work-packages/interface-contract.toml").write_text(
        'fitted_attributes = ["facet_", "facet_share_"]\n', encoding="utf-8"
    )
    (root / "docs/superpowers/notes").mkdir(parents=True)
    (root / "docs/superpowers/notes/spike.md").write_text(RECORD, encoding="utf-8")
    (root / "docs/user-guide").mkdir()
    (root / "docs/user-guide/fitting.md").write_text(DOC, encoding="utf-8")
    (root / "paper").mkdir()
    nb = {
        "cells": [
            {"cell_type": "markdown", "id": "c1", "source": [PAPER_CELLS[0]]},
            {"cell_type": "markdown", "id": "c2", "source": [PAPER_CELLS[1]]},
            {"cell_type": "markdown", "id": "c3", "source": [PAPER_CELLS[2]]},
            {
                "cell_type": "code",
                "id": "tab-D-exponents_and_facets",
                "source": ["exponents_and_facets()"],
                "outputs": [{"data": {"text/markdown": ["| facet | rows |"]}}],
            },
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (root / "paper/paper.ipynb").write_text(
        json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (root / "claims_register.toml").write_text(REGISTER, encoding="utf-8")
    return root


def snapshot(root: Path) -> dict:
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def run(root: Path, *args) -> int:
    return rf.main(["--root", str(root), *args])


def nb_sources(root: Path) -> list[str]:
    nb = json.loads((root / "paper/paper.ipynb").read_text(encoding="utf-8"))
    return ["".join(c["source"]) for c in nb["cells"]]


def test_dry_run_writes_nothing(tmp_path, capsys):
    root = make_tree(tmp_path)
    before = snapshot(root)
    assert run(root, "--surface", "all", "--dry-run") == 0
    assert snapshot(root) == before
    out = capsys.readouterr().out
    assert "== surface code (dry run)" in out and "names=" in out and "left=" in out


def test_code_surface_applies_the_name_table_and_leaves_prose_of_later_surfaces(tmp_path):
    root = make_tree(tmp_path)
    assert run(root, "--surface", "code") == 0
    src = (root / "src/hyperbolic_trade_space/solvers.py").read_text(encoding="utf-8")
    for old, new in [
        ("facet_gap", "term_gap"),
        ("assign_facets", "assign_cells"),
        ("facet_step", "refit_step"),
        ("facet_share_", "term_share_"),
        ("single_facet_termination", "single_term_termination"),
        ('color="facet"', 'color="cell"'),
    ]:
        assert old not in src and new in src, old
    assert "self.cell_ = np.zeros(3)" in src  # facet_ -> cell_ at an identifier boundary
    assert "one-term fit" in src and "several-term fit" in src and "Per-term gaps" in src
    assert "the term that scores it" in src  # the cell wording of the assignment sense
    assert "facet" not in src.lower()
    manifest = (root / "work-packages/interface-contract.toml").read_text(encoding="utf-8")
    assert manifest == 'fitted_attributes = ["cell_", "term_share_"]\n'
    test = (root / "tests/test_solvers.py").read_text(encoding="utf-8")
    assert "def test_duplicate_terms" in test and "'term 1'" in test
    # the notebook: code names and cell ids move, the prose and the outputs do not
    nb = json.loads((root / "paper/paper.ipynb").read_text(encoding="utf-8"))
    assert nb["cells"][3]["id"] == "tab-D-exponents_and_terms"
    assert "".join(nb["cells"][3]["source"]) == "exponents_and_terms()"
    assert nb["cells"][3]["outputs"][0]["data"]["text/markdown"] == ["| facet | rows |"]
    assert "A term, a monomial and a facet are one object" in nb_sources(root)[0]
    assert "`term_share_`" in nb_sources(root)[2]
    assert "lemma_12_facet_gap" in nb_sources(root)[2]  # the derivation's rename waits
    # the register: backing references follow the code, fragments wait for their surface
    reg = (root / "claims_register.toml").read_text(encoding="utf-8")
    assert "test:tests/test_solvers.py::test_duplicate_terms" in reg
    assert "glossary:facet" in reg and 'fragment = "The facet share' in reg
    # a lemma script is not the code surface
    assert "facet" in (root / "derivation/lemma_11_pareto.py").read_text(encoding="utf-8")


def test_derivation_surface_moves_the_module_and_keeps_the_polyhedral_sentence(tmp_path):
    root = make_tree(tmp_path)
    assert run(root, "--surface", "derivation") == 0
    assert not (root / "derivation/lemma_12_facet_gap.py").exists()
    assert (root / "derivation/lemma_12_term_gap.py").exists()
    lemma = (root / "derivation/lemma_11_pareto.py").read_text(encoding="utf-8")
    assert "The facet that blocks u' is one active at u" in lemma  # A1, verbatim
    assert "from derivation.lemma_12_term_gap import" in lemma
    assert 'TITLE = "term first-order gap of a term"' in lemma
    assert lemma.lower().count("facet") == 1
    # the paper's reference to the moved module follows; its prose does not
    cells = nb_sources(root)
    assert "lemma_12_term_gap.py" in cells[2] and "`facet_share_`" in cells[2]


def test_paper_surface_moves_prose_marks_the_kept_paragraph_and_moves_the_register_row(tmp_path):
    root = make_tree(tmp_path)
    assert run(root, "--surface", "paper") == 0
    cells = nb_sources(root)
    moved = "The term share is the fraction of near-frontier designs that term $k$ dominates"
    assert moved in cells[0]
    assert cells[1].startswith(rf.MARKER + "\n**Conditions.**")
    assert "relative interior of a facet of the supporting envelope" in cells[1]
    assert "R2: every term is nonempty" in cells[1]
    reg = (root / "claims_register.toml").read_text(encoding="utf-8")
    assert f'fragment = "{moved}"' in reg
    assert 'note = "term shares sum to one"' in reg
    assert 'fragment = "one facet per segment"' in reg  # the docs row waits for the docs surface
    assert "glossary:facet" in reg


def test_docs_surface_moves_the_page_its_register_row_and_the_figure_name(tmp_path):
    root = make_tree(tmp_path)
    assert run(root, "--surface", "docs") == 0
    doc = (root / "docs/user-guide/fitting.md").read_text(encoding="utf-8")
    assert "one term per segment" in doc and "`assign_cells(X)` reads which term" in doc
    assert "three-terms-light.png" in doc and "facet" not in doc.lower()
    reg = (root / "claims_register.toml").read_text(encoding="utf-8")
    assert 'fragment = "one term per segment"' in reg and "glossary:term" in reg


def test_records_and_the_hand_edited_files_are_never_touched(tmp_path):
    root = make_tree(tmp_path)
    before = snapshot(root)
    assert run(root, "--surface", "all") == 0
    after = snapshot(root)
    for rel in (
        "work-packages/WP1-review.md",
        "docs/superpowers/notes/spike.md",
        "tests/test_vocabulary.py",
    ):
        assert after[rel] == before[rel], rel


def test_all_surfaces_are_idempotent(tmp_path, capsys):
    root = make_tree(tmp_path)
    assert run(root, "--surface", "all") == 0
    once = snapshot(root)
    capsys.readouterr()
    assert run(root, "--surface", "all") == 0
    assert snapshot(root) == once
    out = capsys.readouterr().out
    assert "files changed 0" in out and "files changed 1" not in out
    # what the script leaves is the polyhedral sentence (and the notebook output, regenerated)
    cells = nb_sources(root)
    kept = sum(c.lower().count("facet") for c in cells)
    assert kept == 2  # the R1 sentence and its exempt marker


def test_the_name_table_carries_the_scopes_defaults():
    table = dict(rf.NAMES)
    assert table["facet_share_"] == "term_share_" and table["facet_gap"] == "term_gap"
    assert table["facet_step"] == "refit_step" and table["facet_"] == "cell_"
    assert table["assign_facets"] == "assign_cells" and table["facet_labels"] == "cell_labels"
    assert table["facet_record"] == "term_record" and table["facet_table"] == "term_table"
    assert dict(rf.REF_TOKENS["code"])["paper_facets"] == "paper_terms"
    assert dict(rf.REF_TOKENS["derivation"])["lemma_12_facet_gap"] == "lemma_12_term_gap"
    assert rf.ORDER == ("code", "derivation", "paper", "docs")


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("the facet's rows and the one-facet fit", "the term's cell and the one-term fit"),
        ("Facets meet at ridges; a facet-normal step", "Terms meet at ridges; a term-normal step"),
        ("the multi-facet fit, per-facet", "the several-term fit, per-term"),
        ('set_title("Chart:\\nfacets laid flat")', 'set_title("Chart:\\nterms laid flat")'),
        ("spike-facet-refit/bench.py", "spike-facet-refit/bench.py"),
    ],
)
def test_prose_rules(text, expected):
    out, _ = rf.Renamer("code", "x.py").prose(text)
    assert out == expected
