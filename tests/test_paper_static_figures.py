"""The paper's static figures (WP19): the model's views are byte-identical copies."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_figures  # noqa: E402


def test_model_views_in_the_paper_equal_the_models_views():
    for name, source in build_figures.MODEL_VIEWS.items():
        copy = ROOT / "paper" / "figures" / name
        assert copy.read_bytes() == (ROOT / source).read_bytes(), name


def test_the_nlemma_figure_is_committed_beside_its_generator():
    assert {"nlemma", "planes", "chart_level", "ternary_pair"} <= set(build_figures.PAPER_FIGURES)
    assert (ROOT / "paper" / "figures" / "fig-nlemma.png").stat().st_size > 10_000


def test_the_two_panel_ternary_is_committed_beside_its_generator():
    """Figure 9: the module draws ``case.ternary_pair_figure``; its PNG is committed."""
    assert (ROOT / "paper" / "figures" / "ternary_pair.py").is_file()
    assert (ROOT / "paper" / "figures" / "fig-ternary-pair.png").stat().st_size > 10_000
