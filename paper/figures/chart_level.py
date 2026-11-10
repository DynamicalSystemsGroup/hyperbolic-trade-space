"""The paper's chart figure (WP19, slot S-d3): the level against the chart's leading direction.

The chart rewrites each design as a position along the surface ``Z`` and a level ``log V`` (the
energy differential). Against any position coordinate the surface of the fit is the flat line
``log V = 0``, which is what the chart does and what no log-metric plane shows. The first drawing
put the first Helmert coordinate ``Z0`` on the horizontal axis and readers took nothing from it
(WP11 CR-30), so the axis is now the direction along which the near-frontier designs spread the
most: the first principal direction of the near-frontier chart, the one Appendix D.16 reads
(``case.pca_directions``: the tension report's analysis of the K = 1 fit's band, signed with its
largest loading positive). The chart coordinates ``Z`` do not depend on the fit, so the same
direction serves the K = 3 chart drawn here. Designs are one neutral colour (the supervisor's
ruling against the cluster idiom, ``work-packages/WP19-decisions.md``). Case data of record.

Run ``uv run python paper/figures/chart_level.py`` to write ``fig-chart-level.png`` beside it.
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

try:
    from figures.planes import DESIGN, INK, _case
except ImportError:  # run as a script from paper/figures
    from planes import DESIGN, INK, _case

HERE = pathlib.Path(__file__).resolve().parent
LEADING = 3  # metrics named on the axis, as Appendix D.16 lists them


def leading_direction(study, fit, leading=LEADING):
    """The first principal direction of the near-frontier chart and the words for its ends.

    Returns
    -------
    direction : ndarray of shape (d - 1,)
        A unit vector in chart coordinates ``Z``, signed so that its largest loading on the
        log-metrics is positive (Appendix D.16's convention).
    better, worse : list of str
        The names of the ``leading`` metrics that load most on it, split by the sign of their
        loading: a step along the direction improves ``better`` and worsens ``worse`` (every
        metric is conditioned so that larger is better).
    share : float
        The share of the near-frontier spread along the direction.
    """
    case = _case()
    rep = case._reports(study, fit)[0]
    load = np.asarray(rep.tension_loadings[0], float)
    sign = 1.0 if load[np.argmax(np.abs(load))] > 0 else -1.0
    load, direction = sign * load, sign * np.asarray(rep.tension_directions[0], float)
    top = np.argsort(-np.abs(load))[:leading]
    better = [study.names[j] for j in top if load[j] > 0]
    worse = [study.names[j] for j in top if load[j] < 0]
    return direction, better, worse, float(rep.explained_spread[0])


def _join(names):
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def chart_level_figure(study=None, fit=None, band=None, fit1=None):
    """The level against the chart's leading direction; the surface is the line log V = 0."""
    case = _case()
    if study is None:
        study = case.load_study("primary")
        fits = case.k_fits(study)
        fit, band, fit1 = fits[3], fits[1].band, fits[1]
    band = fit.band if band is None else band
    fit1 = fit if fit1 is None else fit1
    chart = fit.estimator.transform(study.M)
    direction, better, worse, share = leading_direction(study, fit1)
    position, logv = chart[:, :-1] @ direction, chart[:, -1]
    fig, ax = plt.subplots(figsize=(case.FIGURE_WIDTH_IN, 3.8))
    ax.axhspan(-band, 0.0, color="0.75", alpha=0.6, linewidth=0, zorder=1)
    ax.axhline(0.0, color=INK, lw=1.6, zorder=3)
    ax.scatter(position, logv, s=12, color=DESIGN, linewidth=0, zorder=2)
    ends = []
    if better:
        ends.append(f"better {_join(better)}")
    if worse:
        ends.append(f"worse {_join(worse)}")
    ax.set_xlabel(case._wrap("position along the surface: the chart's direction of most spread "
                             f"among the near-frontier designs ({share:.0%} of it); "
                             f"to the right, {'; '.join(ends)}", 96))  # fmt: skip
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
