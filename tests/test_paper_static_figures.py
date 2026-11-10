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
    assert {"nlemma", "planes", "chart_level"} <= set(build_figures.PAPER_FIGURES)
    assert (ROOT / "paper" / "figures" / "fig-nlemma.png").stat().st_size > 10_000
