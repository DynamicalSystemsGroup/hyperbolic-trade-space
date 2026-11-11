"""The n-lemma on the simplex: a candidate figure for Section 4 (WP19, slot S-a5).

For three metrics the simplex of exponent vectors is a triangle. A term's exponent vector is a
point of it, and the smallest face holding that point is the term's contending set: a corner is
one binding metric, an edge a dilemma of the two metrics at its ends, the interior a trilemma
(assumption A2 and Definition 5 of the paper). The figure fits a synthetic table of three
metrics with three planted terms, two on edges and one inside, and draws each fitted exponent
vector. The n-lemma printed for each term is the tension report's (the
support of the exact-maximum fit on the term's cell), not read off the marker.

Run ``uv run python paper/figures/nlemma.py`` to write ``fig-nlemma.png`` beside this file.
"""

from __future__ import annotations

import pathlib
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from hyperbolic_trade_space.plotting import CATEGORY_COLORS

HERE = pathlib.Path(__file__).resolve().parent
PLANTED = [[0.0, 0.35, 0.65], [0.5, 0.25, 0.25], [0.7, 0.3, 0.0]]
TABLE = {"n_samples": 900, "n_features": 3, "n_terms": 3, "random_state": 0}
FIT = {"n_terms": 3, "temperature": 50.0, "random_state": 0}
BAND = 0.1  # near-frontier rows of each term for the tension report
NAMES = ("metric 1", "metric 2", "metric 3")
SQ3 = np.sqrt(3.0) / 2.0
INK = "#1c1c1c"
FACE = "#f1efe9"


def xy(w):
    """Barycentric projection: metric 1 at the top, metric 2 bottom left, metric 3 bottom right."""
    w = np.asarray(w, float)
    return np.array([w[..., 2] + w[..., 0] / 2.0, SQ3 * w[..., 0]]).T


def nlemma_data():
    """The fitted and planted exponent vectors and each term's contending set.

    Returns
    -------
    dict
        ``fitted`` (K, 3) and ``planted`` (K, 3) exponent vectors, matched term by term;
        ``support`` a list of index arrays (the exact-maximum support); ``lemma`` the names.
    """
    from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data, tension_report

    X, _ = make_frontier_data(exponents=PLANTED, **TABLE)
    est = HyperbolicTradeSpace(**FIT).fit(X)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        reports = tension_report(est, X, band=BAND)
    W = np.asarray(est.exponents_, float)
    P = np.asarray(PLANTED, float)
    match = [int(np.argmin(np.abs(P - w).sum(axis=1))) for w in W]
    order = np.argsort(match)
    return {
        "fitted": W[order],
        "planted": P[np.asarray(match)[order]],
        "support": [np.asarray(reports[k].contending_set) for k in order],
        "lemma": [reports[k].lemma_name for k in order],
    }


def _members(support):
    return " and ".join(NAMES[j].split()[1] for j in support)


def nlemma_figure(data=None, figsize=(6.4, 3.9)):
    """Draw the triangle of exponent vectors with its faces named and the terms placed."""
    d = nlemma_data() if data is None else data
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0.0, 0.0, 0.6, 1.0])
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.set(xlim=(-0.3, 1.3), ylim=(-0.15, SQ3 + 0.15))

    corners = xy(np.eye(3))
    ax.fill(corners[:, 0], corners[:, 1], color=FACE, zorder=0)
    ax.plot(*np.vstack([corners, corners[:1]]).T, color="0.55", lw=2.2, zorder=1)
    ax.scatter(*corners.T, s=26, color=INK, zorder=3)
    # Corner names; the top one says what a term at a corner would be.
    places = [(0, 0.04, "bottom", f"{NAMES[0]}\n(corner: it binds alone)"),
              (0, -0.035, "top", NAMES[1]), (0, -0.035, "top", NAMES[2])]  # fmt: skip
    for (x, y), (dx, dy, va, text) in zip(corners, places, strict=True):
        ax.text(x + dx, y + dy, text, ha="center", va=va, fontsize=8.5, color=INK,
                linespacing=1.15)  # fmt: skip
    # Edge names: the dilemma of the two metrics at its ends, written outside the edge.
    edges = [((0, 1), (-0.13, 0.03), 60), ((0, 2), (0.13, 0.03), -60), ((1, 2), (0, -0.08), 0)]
    for (i, j), (dx, dy), rot in edges:
        mid = (corners[i] + corners[j]) / 2
        ax.text(mid[0] + dx, mid[1] + dy, f"edge: dilemma of {i + 1} and {j + 1}",
                rotation=rot, ha="center", va="center", fontsize=8.5, color="0.35")  # fmt: skip
    ax.text(0.5, 0.2, "interior:\ntrilemma", ha="center", va="center", fontsize=8.5,
            color="0.35", linespacing=1.15)  # fmt: skip

    for k, w in enumerate(d["fitted"]):
        col = CATEGORY_COLORS[k]
        ax.scatter(*xy(w), s=95, color=col, edgecolor="white", lw=0.8, zorder=5)
        x, y = xy(w)
        ax.text(x, y, str(k + 1), ha="center", va="center", fontsize=7, color="white",
                weight="bold", zorder=6)  # fmt: skip

    # The key: one line per term, its exponents, and its n-lemma.
    tx = fig.add_axes([0.62, 0.0, 0.38, 1.0])
    tx.set_axis_off()
    y = 0.84
    tx.text(0.0, y + 0.08, "Each term's exponent vector", fontsize=9.5, weight="bold", color=INK)
    for k, w in enumerate(d["fitted"]):
        col = CATEGORY_COLORS[k]
        tx.scatter([0.03], [y - 0.035], s=95, color=col, transform=tx.transAxes, clip_on=False)
        tx.text(0.03, y - 0.035, str(k + 1), ha="center", va="center", fontsize=7, color="white",
                weight="bold")  # fmt: skip
        what = f"{d['lemma'][k]} of {_members(d['support'][k])}"
        if len(d["support"][k]) == 3:
            what = f"{d['lemma'][k]} of all three"
        tx.text(0.1, y, f"term {k + 1}: {what}", fontsize=9, color=INK, va="center")
        tx.text(0.1, y - 0.07, "w = (" + ", ".join(f"{v:.2f}" for v in w) + ")", fontsize=8.5,
                color="0.3", va="center")  # fmt: skip
        y -= 0.17
    tx.set(xlim=(0, 1), ylim=(0, 1))
    return fig


def main() -> None:
    """Write ``fig-nlemma.png`` beside this file."""
    fig = nlemma_figure()
    fig.savefig(HERE / "fig-nlemma.png", dpi=150, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    print("wrote", HERE / "fig-nlemma.png")


if __name__ == "__main__":
    main()
