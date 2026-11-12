"""The paper's static figures (WP19): the model's views are byte-identical copies."""

import subprocess
import sys
from pathlib import Path

import pytest

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


def test_plain_build_leaves_the_paper_figures_alone(monkeypatch, tmp_path):
    """A plain run writes only its own output directory; ``--paper`` is what rewrites the paper."""
    calls = []
    monkeypatch.setattr(build_figures, "build", lambda out: calls.append("docs") or [])
    monkeypatch.setattr(build_figures, "build_paper", lambda: calls.append("paper") or ["x"])
    assert build_figures.main(["--out", str(tmp_path)]) == 0
    assert calls == ["docs"]
    assert build_figures.main(["--out", str(tmp_path), "--paper"]) == 0
    assert calls == ["docs", "docs", "paper"]


@pytest.mark.slow
def test_figure_build_twice_changes_no_tracked_file(tmp_path):
    """Two plain runs of the real build: ``git status`` on the tracked files stays clean."""
    root = Path(build_figures.ROOT)

    def dirty():
        out = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout

    before = dirty()
    for i in range(2):
        assert build_figures.main(["--out", str(tmp_path / f"run{i}")]) == 0
        assert dirty() == before
