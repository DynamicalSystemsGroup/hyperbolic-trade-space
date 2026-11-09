"""Figure 1: the three-pane schematic of a trade space (synthetic; matplotlib only).

Regenerated from the design spike ``docs/superpowers/notes/spike-figure1/make_schematics.py`` (S4)
as specified by the supervisor: the first pane is kinked (hyperbolic sheets with sharp corners),
the second is piecewise linear (the same facets in log space with their normals and one design's
energy differential), the third is the chart with the frontier as one horizontal line and the facets
as coloured regions.

The world is one synthetic ``d = 2`` trade space with an envelope of ``K = 3`` terms in log space,
``Phi(u) = max_k (w_k . u - beta_k)``; the frontier is ``Phi = 0`` and the level sets of ``V`` are
translates of it along the all-ones direction. Everything is deterministic (a fixed seed), and the
data of the figure are returned by :func:`figure1_data` so a test can hash them.

Run ``uv run python paper/figures/figure1.py`` to write ``figure1.png`` and ``figure1.svg`` beside
this file.
"""

from __future__ import annotations

import hashlib
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

from hyperbolic_trade_space.plotting import CATEGORY_COLORS, FRONTIER_COLOR

HERE = pathlib.Path(__file__).resolve().parent
SEED = 20261108
W = np.array([[0.2, 0.8], [0.5, 0.5], [0.8, 0.2]])  # exponent vectors w_k on the simplex
BETA = np.array([0.96, 0.30, 0.60])  # reaches beta_k
FACET_COLORS = CATEGORY_COLORS[:3]
HIGHLIGHT = FRONTIER_COLOR
LEVEL_COLOR = "0.45"
LEVELS = (0.5, 0.75, 1.25)
BEYOND = np.array([[-1.35, 0.06], [0.15, 0.08], [1.0, 0.07]])  # (u1, offset above V = 1)
EXTEND = 0.7
FONT = 10.5
MIN_FONT_PT = FONT - 1.5
"""The smallest type in the figure (legend and annotations)."""


def phi(u):
    """Hard-max envelope potential (log V) of rows of ``u`` in log space."""
    return np.max(np.atleast_2d(u) @ W.T - BETA, axis=-1)


def facet_of(u):
    """The facet that attains the maximum for each row of ``u``."""
    return np.argmax(np.atleast_2d(u) @ W.T - BETA, axis=-1)


def facet_line(k, u1):
    """log metric 2 on facet ``k``'s hyperplane at log metric 1 = ``u1``."""
    return (BETA[k] - W[k, 0] * u1) / W[k, 1]


def envelope(u1):
    """The frontier ``Phi = 0`` as a curve ``u2(u1)``: the minimum of the facet lines."""
    return np.min([facet_line(k, u1) for k in range(3)], axis=0)


def envelope_at(u1, level):
    """The level set ``Phi = level``: the frontier shifted along the all-ones direction."""
    return envelope(u1 - level) + level


def active_ranges():
    """The ``u1`` interval on which each facet is on the frontier."""
    c12 = (BETA[0] / W[0, 1] - BETA[1] / W[1, 1]) / (W[0, 0] / W[0, 1] - W[1, 0] / W[1, 1])
    c23 = (BETA[1] / W[1, 1] - BETA[2] / W[2, 1]) / (W[1, 0] / W[1, 1] - W[2, 0] / W[2, 1])
    return [(-np.inf, c12), (c12, c23), (c23, np.inf)]


def _visible(box):
    u1_lo, u1_hi, u2_lo, u2_hi = box
    out = []
    for k, (a, b) in enumerate(active_ranges()):
        left = (BETA[k] - W[k, 1] * u2_hi) / W[k, 0]
        right = (BETA[k] - W[k, 1] * u2_lo) / W[k, 0]
        out.append((max(a, u1_lo, left), min(b, u1_hi, right)))
    return out


def figure1_data():
    """The synthetic designs and the highlighted design of the figure.

    Returns
    -------
    dict
        ``u`` (rows in log space, 250 below the envelope and 3 just beyond it), ``logV``, ``facet``,
        ``Z`` (position along the frontier, ``(u1 - u2) / sqrt(2)``), ``design`` (the index of the
        highlighted design), ``corners`` (the ``Z`` values where the frontier changes facet), the
        facet exponents ``W`` and reaches ``BETA``.
    """
    rng = np.random.default_rng(SEED)
    pts = []
    while len(pts) < 250:
        u = rng.uniform([-1.9, -1.9], [1.6, 1.6], size=(4000, 2))
        p = phi(u)
        keep = (p <= 0.0) & (p >= -1.6) & (rng.uniform(size=len(u)) < np.exp(1.1 * p))
        pts.extend(u[keep])
    u = np.array(pts[:250])
    beyond = np.column_stack([BEYOND[:, 0], envelope(BEYOND[:, 0]) + BEYOND[:, 1]])
    u = np.vstack([u, beyond])
    logv, f = phi(u), facet_of(u)
    z = (u[:, 0] - u[:, 1]) / np.sqrt(2)
    pick = np.where((f == 1) & (logv < -0.55) & (logv > -0.8) & (np.abs(z) < 0.35))[0][0]
    c1, c2 = (r[1] for r in active_ranges()[:2])
    corners = sorted([(c1 - facet_line(0, c1)) / np.sqrt(2), (c2 - facet_line(2, c2)) / np.sqrt(2)])
    return {"u": u, "logV": logv, "facet": f, "Z": z, "design": int(pick),
            "corners": np.array(corners), "W": W, "BETA": BETA}  # fmt: skip


def data_hash(data=None) -> str:
    """SHA-256 of the figure's data arrays (the deterministic fingerprint a test pins)."""
    data = figure1_data() if data is None else data
    h = hashlib.sha256()
    for key in sorted(data):
        h.update(key.encode())
        h.update(np.ascontiguousarray(np.asarray(data[key], dtype=float)).tobytes())
    return h.hexdigest()


def _scatter(ax, xy, f, alpha=0.7, s=9):
    for k in range(3):
        ax.scatter(*xy[f == k].T, s=s, color=FACET_COLORS[k], alpha=alpha, lw=0, zorder=3)


def _star(ax, xy):
    ax.scatter(*xy, s=70, color=HIGHLIGHT, edgecolor="white", lw=1.3, zorder=9)


def figure1(figsize=(8.2, 3.6)):
    """Draw Figure 1.

    Parameters
    ----------
    figsize : tuple of float, optional
        Width and height in inches.

    Returns
    -------
    matplotlib.figure.Figure
        Three panes: the fitted reference surface in metric space (kinked sheets), the facets
        with their normals and one design's energy differential in log space, and the chart
        (Z, log V) with the frontier as one horizontal line and the facets as coloured regions.
    """
    d = figure1_data()
    u, f, z, logv, i = d["u"], d["facet"], d["Z"], d["logV"], d["design"]
    us, zs, ls = u[i], z[i], logv[i]
    top = us - ls  # where uniform scaling carries the design onto the frontier
    with plt.rc_context({"font.size": FONT, "axes.titlesize": FONT + 1,
                         "axes.labelsize": FONT, "xtick.labelsize": FONT - 1,
                         "ytick.labelsize": FONT - 1, "axes.spines.top": False,
                         "axes.spines.right": False}):  # fmt: skip
        fig = plt.figure(figsize=figsize)
        fw, fh = figsize
        y0, h = 0.62 / fh, 2.2 / fh  # the three panes share the baseline and the height
        axm = fig.add_axes([0.55 / fw, y0, 2.0 / fw, h])
        axl = fig.add_axes([3.05 / fw, y0, 1.94 / fw, h])
        axc = fig.add_axes([5.65 / fw, y0, 2.4 / fw, h])
        box_l = (-2.3, 1.75, -2.1, 2.5)

        # pane 1: metric space, the fitted reference surface, hyperbolic sheets with sharp corners
        _scatter(axm, np.exp(u), f)
        g = np.exp(np.linspace(np.log(0.12), np.log(5.2), 600))
        for lev in LEVELS:
            axm.plot(
                g,
                np.exp(envelope_at(np.log(g), np.log(lev))),
                color=LEVEL_COLOR,
                lw=0.9,
                ls=":",
                zorder=2,
            )
        for k, (a, b) in enumerate(
            _visible((np.log(0.12), np.log(5.2), np.log(0.02), np.log(5.2)))
        ):
            seg = np.exp(np.linspace(a, b, 160))
            axm.plot(
                seg,
                np.exp(facet_line(k, np.log(seg))),
                color=FACET_COLORS[k],
                lw=2.0,
                zorder=4,
                solid_capstyle="round",
            )
        _star(axm, np.exp(us))
        axm.set_xlim(0, 5.2)
        axm.set_ylim(0, 5.2)
        axm.set_xlabel("metric 1")
        axm.set_ylabel("metric 2")
        axm.set_title("Metric space:\nfitted reference surface", loc="left")
        axm.text(2.9, 1.0, "V = 1", fontsize=FONT, fontweight="bold")
        axm.text(2.3, 2.0, "V > 1: beyond", fontsize=FONT - 1, color=LEVEL_COLOR)

        # pane 2: log space, the facets with normals and one design's energy differential
        _scatter(axl, u, f, alpha=0.55)
        gg = np.linspace(box_l[0], box_l[1], 400)
        axl.plot(gg, envelope_at(gg, ls), color=LEVEL_COLOR, lw=0.9, ls=":", zorder=2)
        for k, (a, b) in enumerate(_visible(box_l)):
            seg = np.linspace(a, b, 60)
            axl.plot(
                seg,
                facet_line(k, seg),
                color=FACET_COLORS[k],
                lw=2.0,
                zorder=4,
                solid_capstyle="round",
            )
            um = np.array([(a + b) / 2, facet_line(k, (a + b) / 2)])
            n = W[k] / np.linalg.norm(W[k]) * 0.62
            axl.add_patch(
                FancyArrowPatch(
                    um,
                    um + n,
                    arrowstyle="-|>",
                    mutation_scale=9,
                    color=FACET_COLORS[k],
                    lw=1.3,
                    zorder=6,
                )
            )
            axl.text(
                *(um + n * 1.38),
                rf"$w_{k + 1}$",
                color=FACET_COLORS[k],
                ha="center",
                va="center",
                fontsize=FONT + 0.5,
                fontweight="bold",
                zorder=7,
            )
        axl.add_patch(
            FancyArrowPatch(
                us, top, arrowstyle="-|>", mutation_scale=11, color=HIGHLIGHT, lw=2.0, zorder=8
            )
        )
        _star(axl, us)
        axl.text(
            us[0] - 0.14,
            us[1] + 0.1,
            "energy\ndifferential\nlog V",
            fontsize=FONT - 1.5,
            fontweight="bold",
            va="center",
            ha="right",
            zorder=10,
            bbox={"fc": "white", "ec": "none", "alpha": 0.85, "pad": 1.0},
        )
        axl.set_xlim(box_l[0], box_l[1])
        axl.set_ylim(box_l[2], box_l[3])
        axl.set_aspect("equal")
        axl.set_xlabel("log metric 1")
        axl.set_ylabel("log metric 2")
        axl.set_title("Log space:\nsupporting envelope", loc="left")

        # pane 3: the chart (Z, log V): the frontier is one horizontal line, facets are regions
        zlim = (z.min() - 0.25, z.max() + 0.25)
        edges = [zlim[0], *d["corners"], zlim[1]]
        for k in range(3):
            axc.axvspan(edges[k], edges[k + 1], color=FACET_COLORS[k], alpha=0.14, lw=0, zorder=1)
            axc.text(
                (edges[k] + edges[k + 1]) / 2,
                0.3,
                f"facet {k + 1}",
                ha="center",
                color=FACET_COLORS[k],
                fontsize=FONT - 1,
                fontweight="bold",
            )
        axc.axhline(0.0, color=FRONTIER_COLOR, lw=2.2, zorder=4)
        for k in range(3):
            axc.scatter(
                z[f == k], logv[f == k], s=9, color=FACET_COLORS[k], alpha=0.65, lw=0, zorder=3
            )
        axc.add_patch(
            FancyArrowPatch(
                (zs, ls),
                (zs, 0.0),
                arrowstyle="-|>",
                mutation_scale=11,
                color=HIGHLIGHT,
                lw=2.0,
                zorder=8,
            )
        )
        _star(axc, (zs, ls))
        axc.text(zs + 0.08, ls / 2, "log V", fontsize=FONT, fontweight="bold", va="center")
        axc.text(
            zlim[1] - 0.05,
            0.06,
            "frontier, log V = 0",
            ha="right",
            va="bottom",
            fontsize=FONT - 0.5,
            fontweight="bold",
        )
        axc.set_xlim(*zlim)
        axc.set_ylim(-1.75, 0.5)
        axc.set_xlabel("Z (position along the frontier)")
        axc.set_ylabel("log V")
        axc.set_title("Chart (Z, log V):\nfacets as regions", loc="left")
        axl.legend(handles=[Line2D([], [], color=FACET_COLORS[k], lw=2.0, label=f"facet {k + 1}")
                            for k in range(3)], loc="upper right", frameon=False,
                   fontsize=FONT - 1.5, handlelength=1.2, borderaxespad=0.0,
                   labelspacing=0.15)  # fmt: skip
    return fig


def main():
    """Write ``figure1.png`` and ``figure1.svg`` beside this file."""
    fig = figure1()
    fig.savefig(HERE / "figure1.png", dpi=200, metadata={"Software": None})
    fig.savefig(HERE / "figure1.svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    print("wrote", HERE / "figure1.png", HERE / "figure1.svg")


if __name__ == "__main__":
    main()
