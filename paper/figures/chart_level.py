"""Figure 4 redrawn (WP19, slot S-d3): the chart as position against level, with no facet colouring.

The chart rewrites each design as a position along the surface ``Z`` and a level ``log V`` (the
energy differential). In the plane of the first position coordinate and the level the surface of
the K = 3 fit is the flat line ``log V = 0`` whatever the position, which is what the chart does and
what no log-metric plane shows. Designs are one neutral colour (the supervisor's ruling against the
cluster idiom, ``work-packages/WP19-decisions.md``). Case data as committed; WP23 regenerates them.

Run ``uv run python paper/figures/chart_level.py`` to write ``fig-chart-level.png`` beside it.
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

try:
    from figures.planes import DESIGN, INK, _case
except ImportError:  # run as a script from paper/figures
    from planes import DESIGN, INK, _case

HERE = pathlib.Path(__file__).resolve().parent
_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def chart_level_figure(study=None, fit=None, band=None):
    """First position coordinate against the level, the surface as the line log V = 0."""
    case = _case()
    if study is None:
        study = case.load_study("primary")
        fits = case.k_fits(study)
        fit, band = fits[3], fits[1].band
    band = fit.band if band is None else band
    chart = fit.estimator.transform(study.M)
    z0, logv = chart[:, 0], chart[:, -1]
    fig, ax = plt.subplots(figsize=(case.FIGURE_WIDTH_IN, 3.8))
    ax.axhspan(-band, 0.0, color="0.75", alpha=0.6, linewidth=0, zorder=1)
    ax.axhline(0.0, color=INK, lw=1.6, zorder=3)
    ax.scatter(z0, logv, s=12, color=DESIGN, linewidth=0, zorder=2)
    n = chart.shape[1] - 1  # position coordinates: one fewer than the metrics
    ax.set_xlabel(f"Z0: position along the surface (first of {_WORDS.get(n, n)} coordinates, "
                  "no meaning alone)")  # fmt: skip
    ax.set_ylabel("log V: level\n(0 on the surface, negative inside)")
    handles = [
        Line2D([], [], marker="o", ls="", color=DESIGN, label="designs"),
        Line2D([], [], color=INK, label="the surface, log V = 0"),
        Patch(color="0.75", alpha=0.6, label="near-frontier band"),
    ]
    ax.legend(handles=handles, frameon=False, loc="lower left", fontsize=9)
    fig.tight_layout()
    return fig


def main() -> None:
    """Write ``fig-chart-level.png`` beside this file."""
    fig = chart_level_figure()
    fig.savefig(HERE / "fig-chart-level.png", dpi=100, metadata={"Software": None})
    plt.close(fig)
    print("wrote", HERE / "fig-chart-level.png")


if __name__ == "__main__":
    main()
