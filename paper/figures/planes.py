"""The paper's log-metric planes (WP19, slots S-d1 and S-d2): slices with no cell colouring.

The supervisor's ruling (``work-packages/WP19-decisions.md``): colouring designs by the term that
scores them highest is the scikit-learn cluster idiom and makes readers take a term for a cluster.
Here the model is drawn as the model: in each slice the term's line is black, with the term named in
the panel's title, and the near-frontier band lies below it. The slice is the case module's
(``k_terms._slice``): a term's line in the plane of two metrics, with the other metrics held at the
median of that term's near-frontier designs. The near-frontier band (1/tau in log V, under two
pixels here) is not drawn: three rounds of cold readers called it invisible or decoration. A design
whose other metrics sit at that median lies
on the line exactly when it is on the surface; one whose other metrics differ falls on either side
of the line however close to the surface it is. So the designs are two greys (WP11 CR-33): dark,
those whose other metrics are near the median (their weighted log offset from it within
:data:`NEAR_TOL` in log V, so the line is the surface for them to within that tolerance); light,
the rest. The data are the case's committed tables of record.

Run ``uv run python paper/figures/planes.py`` to write ``fig-planes-k1.png`` (the K = 1 fit, one
slice) beside this file. The same function draws a fit with several terms (``n_terms``), one slice
per term; the paper does not show it: at the case's K the slice of the heavier term is a lattice of
swapped parts and the other is the K = 1 plane again (``WP30-rounds/paperwp30/figure-loop.md``).
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

HERE = pathlib.Path(__file__).resolve().parent
DESIGN = "0.62"  # the one grey of a figure that does not split the designs (``chart_level``)
NEAR = "0.35"  # designs whose other metrics are near the median the line is drawn at
OTHER = "0.8"  # the rest
NEAR_TOL = 0.1  # in log V: the most the other metrics may move a near design off the line's slice
INK = "#1c1c1c"
_WORDS = {
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
}


def _case():
    root = HERE.parent.parent
    for p in (root / "src", root / "examples" / "adcs"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import case

    return case


def _envelope(ws, bs, g, shift=0.0):
    """The lowest term line over ``g`` (the surface in the slice) and the term attaining it."""
    ws, bs = np.asarray(ws, float), np.asarray(bs, float)
    lines = (bs[:, None] - shift - np.outer(ws[:, 0], g)) / ws[:, 1][:, None]
    return lines.min(axis=0), lines.argmin(axis=0)


def _near_median(est, U, keep, ws, bs, j, k, tol=NEAR_TOL):
    """Designs whose other metrics are within ``tol`` (in log V) of a drawn term's slice median.

    ``_slice`` folds the median into each line's offset ``b = (log_offset - w_rest . median) / s``
    with ``s`` the term's weight on the two plotted metrics, so the weighted offset of a design's
    other metrics from the median is ``w_rest . u_rest - (log_offset - b s)``.
    """
    W = est.exponents_
    rest = [i for i in range(U.shape[1]) if i not in (j, k)]
    near = np.zeros(len(U), bool)
    for f, b in zip(keep, bs, strict=True):
        s = W[f, j] + W[f, k]
        off = U[:, rest] @ W[f, rest] - (est.log_offset_[f] - b * s)
        near |= np.abs(off) <= tol
    return near


def planes_figure(study=None, fit=None, band=None, n_terms=None):
    """Log-metric slices of a fit: designs in two greys, each term's line in its slice, the band.

    With no ``study`` the primary regime's fit with ``n_terms`` terms is drawn (``case.k_fits``),
    with the K = 1 fit's band, as the paper's cells do. Each panel is the plane of one term's two
    heaviest metrics (``k_terms.slice_pairs``) and names that term in its title; a term is drawn
    only where it weighs both metrics, so a panel holds one line unless two terms share the pair.
    """
    case = _case()
    if study is None:
        study = case.load_study("primary")
        fits = case.k_fits(study)
        fit, band = fits[n_terms or case.CASE_K], fits[1].band
    band = fit.band if band is None else band
    _, k_terms, plotting = case._lib()
    est, M = fit.estimator, study.M
    U = np.log(M)
    labels = plotting.cell_labels(est, M)
    pairs = k_terms.slice_pairs(est)
    fig, axes = plt.subplots(len(pairs), 1, figsize=(case.FIGURE_WIDTH_IN, 4.6 * len(pairs)),
                             squeeze=False)  # fmt: skip
    several, ink = est.exponents_.shape[0] > 1, []
    for ax, (j, k) in zip(axes[:, 0], pairs, strict=True):
        keep, ws, bs = k_terms._slice(est, U, labels, band, j, k)
        near = _near_median(est, U, keep, ws, bs, j, k)
        ax.scatter(U[~near, j], U[~near, k], s=12, color=OTHER, zorder=2, linewidth=0)
        ax.scatter(U[near, j], U[near, k], s=12, color=NEAR, zorder=2.5, linewidth=0)
        lo_x, hi_x = U[:, j].min(), U[:, j].max()
        pad = 0.1 * (hi_x - lo_x)
        g = np.linspace(lo_x - pad, hi_x + pad, 400)
        top, who = _envelope(ws, bs, g)
        ax.plot(g, top, color=INK, lw=1.6, zorder=3)
        ink.append(np.vstack([U[:, [j, k]], np.c_[g, top]]))  # the designs and the line
        lo_y, hi_y = U[:, k].min(), U[:, k].max()
        ylim = (lo_y - 0.1 * (hi_y - lo_y), hi_y + 0.1 * (hi_y - lo_y))
        ax.set_xlim(lo_x - pad, hi_x + pad)
        ax.set_ylim(*ylim)
        # A panel with one term names it in the title; with two or more, each is named on its
        # segment of the surface (where the segment is in view).
        visible = (top > ylim[0]) & (top < ylim[1])
        for f in np.unique(who[visible]) if len(keep) > 1 else ():
            idx = np.flatnonzero((who == f) & visible)
            m = idx[len(idx) // 2]
            ax.annotate(f"term {keep[f] + 1}", (g[m], top[m]), xytext=(6, 8),
                        textcoords="offset points", fontsize=9, color=INK, zorder=4,
                        bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none",
                              "alpha": 0.8})  # fmt: skip
        ax.set_xlabel(case._wrap("log of the " + case.cond_label(study, study.attrs[j]), 80))
        ax.set_ylabel(case._wrap("log of the " + case.cond_label(study, study.attrs[k]), 44))
        title = f"{study.names[j]} and {study.names[k]}"
        if several and len(keep) == 1:
            title = f"term {keep[0] + 1}: " + title
        ax.set_title(title)
    others = _WORDS.get(U.shape[1] - 2, U.shape[1] - 2)
    if not several:
        line = "the surface in this slice"
    elif all(len(k_terms._slice(est, U, labels, band, j, k)[0]) == 1 for j, k in pairs):
        line = "the term's line in this slice"
    else:
        line = "the surface in this slice, one segment per term"
    handles = [
        Line2D(
            [],
            [],
            marker="o",
            ls="",
            color=NEAR,
            label=f"designs whose other {others} metrics are near the median "
            f"(within {NEAR_TOL:g} in log V)",
        ),
        Line2D([], [], marker="o", ls="", color=OTHER, label="the other designs"),
        Line2D([], [], color=INK, label=line),
    ]
    fig.tight_layout()
    _place_legend(fig, axes[:, 0], ink, handles)
    return fig


def adjusted_plane(study, fit):
    """The K = 1 plane of the two heaviest metrics with every design moved onto the line's slice.

    The line is the surface in the plane of metrics ``j`` and ``k`` (``k_terms.slice_pairs``) with
    the other metrics held at the median of the near-frontier designs. A design whose other
    metrics differ lies off that slice. Moving it vertically by what its other metrics add,
    ``(w_rest . u_rest - w_rest . median) / w_k``, puts every design in the slice with its distance
    above the line equal to ``log V / w_k``: the line is then the surface for every design, and the
    designs fall below it by their level.

    Returns
    -------
    dict
        ``x`` and ``y`` the plane's coordinates and the adjusted height of each design, ``line``
        a function of ``x`` giving the surface, ``names`` the two metrics, ``w_k`` the exponent of
        the vertical metric and ``log_v`` each design's level.
    """
    case = _case()
    _, k_terms, _ = case._lib()
    est, M = fit.estimator, study.M
    U = np.log(M)
    j, k = k_terms.slice_pairs(est)[0]
    w, beta = np.asarray(est.exponents_[0], float), float(est.log_offset_[0])
    rest = [i for i in range(U.shape[1]) if i not in (j, k)]
    near = np.abs(est.training_log_v_) < fit.band
    base = float(np.median(U[near][:, rest] @ w[rest]))
    y = U[:, k] + (U[:, rest] @ w[rest] - base) / w[k]
    return {
        "x": U[:, j],
        "y": y,
        "w_k": float(w[k]),
        "log_v": U @ w - beta,
        "line": lambda g: (beta - base - w[j] * np.asarray(g, float)) / w[k],
        "names": (j, k),
    }


def adjusted_plane_figure(study=None, fit=None):
    """Figure 5: every design against the K = 1 surface in the plane of its two heaviest metrics.

    One grey for the designs, one black line for the surface. The vertical coordinate is the
    unit-cost (second metric) coordinate adjusted for the other metrics (:func:`adjusted_plane`),
    so the line is the surface for every design, a design above it lies beyond the surface, and
    the distance below it is the design's level over the vertical metric's exponent.
    """
    case = _case()
    if study is None:
        study = case.load_study("primary")
        fit = case.k_fits(study, (1,))[1]
    d = adjusted_plane(study, fit)
    j, k = d["names"]
    fig, ax = plt.subplots(figsize=(case.FIGURE_WIDTH_IN, 4.4))
    ax.scatter(d["x"], d["y"], s=12, color=DESIGN, linewidth=0, zorder=2)
    lo, hi = d["x"].min(), d["x"].max()
    g = np.linspace(lo - 0.1 * (hi - lo), hi + 0.1 * (hi - lo), 100)
    ax.plot(g, d["line"](g), color=INK, lw=1.6, zorder=3)
    ax.set_xlim(g[0], g[-1])
    ax.set_xlabel(case._wrap("log of the " + case.cond_label(study, study.attrs[j]), 80))
    ax.set_ylabel(case._wrap(
        "log of the " + case.cond_label(study, study.attrs[k]) + ", adjusted for the other "
        f"{_WORDS.get(len(study.attrs) - 2, len(study.attrs) - 2)} metrics", 44))  # fmt: skip
    ax.set_title(f"{study.names[j]} and {study.names[k]}")
    handles = [
        Line2D([], [], marker="o", ls="", color=DESIGN, label="a design"),
        Line2D([], [], color=INK, label="the surface"),
    ]
    ax.legend(handles=handles, frameon=False, loc="lower left", fontsize=9)
    fig.tight_layout()
    return fig


def _place_legend(fig, axes, ink, handles, corners=("lower left", "lower right", "upper right")):
    """Put the legend in the panel corner whose box covers the least ink (designs and line)."""
    best, fewest = None, None
    for ax, points in zip(axes, ink, strict=True):
        for loc in corners:
            legend = ax.legend(handles=handles, frameon=False, loc=loc, fontsize=9)
            fig.canvas.draw()
            box, xy = legend.get_window_extent(), ax.transData.transform(points)
            inside = (xy >= (box.x0, box.y0)).all(axis=1) & (xy <= (box.x1, box.y1)).all(axis=1)
            covered = int(inside.sum())
            legend.remove()
            if fewest is None or covered < fewest:
                best, fewest = (ax, loc), covered
    ax, loc = best
    ax.legend(handles=handles, frameon=False, loc=loc, fontsize=9)


def main() -> None:
    """Write ``fig-planes-k1.png`` beside this file."""
    fig = adjusted_plane_figure()
    target = HERE / "fig-planes-k1.png"
    fig.savefig(target, dpi=100, metadata={"Software": None})
    plt.close(fig)
    print("wrote", target)


if __name__ == "__main__":
    main()
