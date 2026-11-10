"""Figures 2 and 3 redrawn (WP19, slots S-d1 and S-d2): log-metric slices with no facet colouring.

The supervisor's ruling (``work-packages/WP19-decisions.md``): colouring designs by the facet that
scores them highest is the scikit-learn cluster idiom and makes readers take a facet for a cluster.
Here the designs are one neutral colour; the model is drawn as the model: in each slice the surface
is the black line, one straight segment per facet with the facet named on its segment when there is
more than one, and the near-frontier band below it. The slice is the case module's
(``k_terms._slice``): a facet's line in the plane of two metrics, with the other metrics held at the
median of that facet's near-frontier designs. The data are the case's committed tables; WP23
regenerates them, and these figures with them.

Run ``uv run python paper/figures/planes.py`` to write ``fig-planes-k3.png`` (the K = 3 fit, three
slices) and ``fig-planes-k1.png`` (the K = 1 fit, one slice) beside this file.
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = pathlib.Path(__file__).resolve().parent
DESIGN = "0.62"
INK = "#1c1c1c"


def _case():
    root = HERE.parent.parent
    for p in (root / "src", root / "examples" / "adcs"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import case

    return case


def _envelope(ws, bs, g, shift=0.0):
    """The lowest facet line over ``g`` (the surface in the slice) and the facet attaining it."""
    ws, bs = np.asarray(ws, float), np.asarray(bs, float)
    lines = (bs[:, None] - shift - np.outer(ws[:, 0], g)) / ws[:, 1][:, None]
    return lines.min(axis=0), lines.argmin(axis=0)


def planes_figure(study=None, fit=None, band=None, n_terms=3):
    """Log-metric slices of a fit: designs in one colour, the surface by facet segment, the band.

    With no ``study`` the primary regime's fit with ``n_terms`` terms is drawn (``case.k_fits``),
    with the K = 1 fit's band, as the paper's cells do. At K = 1 the surface is one line and is
    not labelled by facet: one facet, one line.
    """
    case = _case()
    if study is None:
        study = case.load_study("primary")
        fits = case.k_fits(study)
        fit, band = fits[n_terms], fits[1].band
    band = fit.band if band is None else band
    _, k_terms, plotting = case._lib()
    est, M = fit.estimator, study.M
    U = np.log(M)
    labels = plotting.facet_labels(est, M)
    pairs = k_terms.slice_pairs(est)
    fig, axes = plt.subplots(len(pairs), 1, figsize=(case.FIGURE_WIDTH_IN, 4.6 * len(pairs)),
                             squeeze=False)  # fmt: skip
    for ax, (j, k) in zip(axes[:, 0], pairs, strict=True):
        keep, ws, bs = k_terms._slice(est, U, labels, band, j, k)
        ax.scatter(U[:, j], U[:, k], s=12, color=DESIGN, zorder=2, linewidth=0)
        lo_x, hi_x = U[:, j].min(), U[:, j].max()
        pad = 0.1 * (hi_x - lo_x)
        g = np.linspace(lo_x - pad, hi_x + pad, 400)
        top, who = _envelope(ws, bs, g)
        low, _ = _envelope(ws, bs, g, shift=band)
        ax.fill_between(g, low, top, color="0.75", alpha=0.6, linewidth=0, zorder=1)
        ax.plot(g, top, color=INK, lw=1.6, zorder=3)
        lo_y, hi_y = U[:, k].min(), U[:, k].max()
        ylim = (lo_y - 0.1 * (hi_y - lo_y), hi_y + 0.1 * (hi_y - lo_y))
        ax.set_xlim(lo_x - pad, hi_x + pad)
        ax.set_ylim(*ylim)
        # Name each facet on its segment of the surface (where the segment is in view); at K = 1
        # the surface is one line and a name on it would say nothing the legend does not.
        visible = (top > ylim[0]) & (top < ylim[1])
        for f in np.unique(who[visible]) if est.exponents_.shape[0] > 1 else ():
            idx = np.flatnonzero((who == f) & visible)
            m = idx[len(idx) // 2]
            ax.annotate(f"facet {keep[f] + 1}", (g[m], top[m]), xytext=(6, 8),
                        textcoords="offset points", fontsize=9, color=INK, zorder=4,
                        bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none",
                              "alpha": 0.8})  # fmt: skip
        ax.set_xlabel(case._wrap("log of the " + case.cond_label(study, study.attrs[j]), 80))
        ax.set_ylabel(case._wrap("log of the " + case.cond_label(study, study.attrs[k]), 44))
        ax.set_title(f"{study.names[j]} and {study.names[k]}")
    surface = "the surface in this slice"
    if est.exponents_.shape[0] > 1:
        surface += ", one segment per facet"
    handles = [
        Line2D([], [], marker="o", ls="", color=DESIGN, label="designs"),
        Line2D([], [], color=INK, label=surface),
        Patch(color="0.75", alpha=0.6, label="near-frontier band"),
    ]
    axes[0, 0].legend(handles=handles, frameon=False, loc="lower left", fontsize=9)
    fig.tight_layout()
    return fig


def main() -> None:
    """Write ``fig-planes-k3.png`` and ``fig-planes-k1.png`` beside this file."""
    for n_terms in (3, 1):
        fig = planes_figure(n_terms=n_terms)
        target = HERE / f"fig-planes-k{n_terms}.png"
        fig.savefig(target, dpi=100, metadata={"Software": None})
        plt.close(fig)
        print("wrote", target)


if __name__ == "__main__":
    main()
