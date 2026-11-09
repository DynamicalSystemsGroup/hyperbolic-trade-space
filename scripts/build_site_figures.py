"""Build the root index page's own figure: the Why image (the triangle of three metrics).

    uv run python scripts/build_site_figures.py [--out DIR] [--lines]

The triangle is the positions of three metrics, shaded by the trade-off that binds there. The
table is the package's planted three-facet table, the fit is the package's own estimator, and the
regions are exact: the facet k that binds at a position is the argmax over k of
``w_k . p - beta_k``.
Every word on the figure is read from the fitted exponents (nothing is hand-placed): the colour
of a region follows from which facet trades all three metrics, its label names the metrics whose
exponents are large, and the label sits where the region holds few designs.

The triangle is drawn with plain Matplotlib (the barycentric projection is written out below:
``x = right + top / 2``, ``y = sqrt(3) / 2 * top``), so there is no extra dependency. Two files are
written, ``why-regions-light.png`` and ``why-regions-dark.png``, on transparent backgrounds and
with the colours of the root page's two schemes.

``--lines`` (off by default, and off everywhere on the site) overlays lines of equal V at a fixed
total: the shares are ``c_j = (m_j / typical_j)^(1/s) / L`` with ``s = 1`` and ``L`` their sum, the
function drawn is ``f(c) = max_k (a_k + s * sum_j w_kj log c_j)`` with
``a_k = w_k . colmean - beta_k``, and each facet's exponent vector ``w_k`` is a star in the facet's
colour, exactly where that facet's V peaks at a fixed total.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "build" / "site-figures"
FILES = {"light": "why-regions-light.png", "dark": "why-regions-dark.png"}

N_ROWS, N_METRICS, N_TERMS, DATA_SEED = 900, 3, 3, 11
TEMPERATURE, FIT_SEED = 50.0, 0
FIGSIZE, DPI = (7.4, 7.0), 170  # the axes span 1.08 by 1.07 plane units, so the triangle fills it
BLUE, AMBER, GREEN = "#0072B2", "#E69F00", "#009E73"
BIG = 0.12  # an exponent above this makes its metric part of the trade-off the facet names
NAMES = ["metric 1", "metric 2", "metric 3"]
SQ3 = np.sqrt(3.0) / 2.0

SCHEMES = {
    "light": {
        "ink": "#1a1a1a",
        "plate": "#ffffff",
        "dots": "#7d7d7d",
        "mix": ("#ffffff", 0.80),
    },
    "dark": {
        "ink": "#e8e6e1",
        "plate": "#221f1e",
        "dots": "#a5a19a",
        "mix": ("#191817", 0.62),
    },
}


def project(top, left, right):
    """Barycentric (top, left, right) to plane coordinates; the corner of ``top`` is up."""
    top, right = np.asarray(top, float), np.asarray(right, float)
    return right + top / 2.0, SQ3 * top


def _hex(h):
    return np.array([int(h[i : i + 2], 16) for i in (1, 3, 5)]) / 255.0


def _close(x):
    x = np.asarray(x, float)
    return x / x.sum(axis=-1, keepdims=True)


def says(w):
    """The trade-off a facet with exponent vector ``w`` names, in words, read from its exponents."""
    big = [j for j in np.argsort(-w) if w[j] > BIG]
    if len(big) >= len(w):
        return "all three trade"
    return f"{NAMES[big[0]]} trades\nagainst {NAMES[big[1]]}"


def fit_why():
    """The planted table and its three-facet fit: the data, exponents, offsets, facets, log V."""
    from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

    X, _ = make_frontier_data(N_ROWS, N_METRICS, n_terms=N_TERMS, random_state=DATA_SEED)
    ts = HyperbolicTradeSpace(n_terms=N_TERMS, temperature=TEMPERATURE, random_state=FIT_SEED)
    ts.fit(X)
    U = np.log(X)
    P = U - U.mean(axis=1, keepdims=True)  # position: the level direction removed
    return {
        "X": X,
        "U": U,
        "colmean": P.mean(axis=0),  # log of each metric's typical size, up to a common factor
        "spread": float(2.0 * (P - P.mean(axis=0)).std()),
        "W": np.asarray(ts.exponents_, float),
        "beta": np.asarray(ts.log_offset_, float).ravel(),
        "facet": np.asarray(ts.facet_),
        "logv": np.asarray(ts.score_samples(X), float),
    }


def colours(W):
    """Facet colours: the facet trading all three metrics is amber, the others blue and green."""
    tri = int(np.argmax(W.min(axis=1)))
    others = [k for k in range(len(W)) if k != tri]
    return {tri: AMBER, others[0]: BLUE, others[1]: GREEN}


def shares(fit, s):
    """Each design as shares c_j = (m_j / typical_j)^(1/s) / L, L their sum (s = 1: plain sum)."""
    return _close(np.exp((fit["U"] - fit["colmean"]) / s))


def region_of(fit, s, top, left, right):
    """The binding facet at barycentric positions: argmax_k a_k + s * sum_j w_kj log c_j."""
    W = fit["W"]
    a = W @ fit["colmean"] - fit["beta"]
    c = np.stack([top, left, right], axis=-1)
    with np.errstate(divide="ignore"):
        g = a + s * (np.log(np.clip(c, 1e-300, None)) @ W.T)
    return g.argmax(axis=-1), g


def _grid(n):
    """Plane grid of the triangle: x, y, barycentric (top, left, right), and the inside mask."""
    x, y = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, SQ3, int(n * SQ3)))
    top = y / SQ3
    right = x - top / 2.0
    left = 1.0 - top - right
    inside = (top > 1e-3) & (left > 1e-3) & (right > 1e-3)
    return x, y, top, left, right, inside


def regions(fit, s, n=500):
    """The regions on a grid of the triangle: (barycentric points, region index per point)."""
    _, _, top, left, right, inside = _grid(n)
    t, lf, r = top[inside], left[inside], right[inside]
    return np.column_stack([t, lf, r]), region_of(fit, s, t, lf, r)[0]


LABEL_SIZES = (15.0, 14.5, 14.0)  # points; the largest that fits is used
LABEL_MARGIN = 0.004  # clear space, in plane units, between a label's box and any border


def _wraps(text):
    """The label's own wrap, then the same words on one to four lines ("metric 3" is a unit)."""
    units = re.findall(r"metric \d|\S+", text.replace("\n", " "))
    out = [text]
    for lines in (2, 3, 4, 1):
        per = -(-len(units) // lines)
        alt = "\n".join(" ".join(units[i : i + per]) for i in range(0, len(units), per))
        if alt not in out:
            out.append(alt)
    return out


def _box(ax, text, size, ink, plate, edge):
    """A label drawn at the origin; returns the text artist and its box half-extents (plane units),
    read from the renderer (the bounding box includes the round box around the words)."""
    t = ax.text(
        0,
        0,
        text,
        ha="center",
        va="center",
        fontsize=size,
        fontweight="bold",
        color=ink,
        bbox={"boxstyle": "round,pad=0.3", "fc": plate, "ec": edge, "lw": 2.0},
        zorder=6,
    )
    ax.figure.canvas.draw()
    bb = t.get_bbox_patch().get_window_extent(ax.figure.canvas.get_renderer())
    (x0, y0), (x1, y1) = ax.transData.inverted().transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
    return t, (x1 - x0) / 2.0, (y1 - y0) / 2.0


def place_labels(fit, comp, s, ax, ink, plate, col):
    """Draw each facet's label inside its own region and return ``{facet: text artist}``.

    The rule reads the fit. On a fine grid of the triangle the region of facet k is where
    ``k = argmax_k w_k . p - beta_k``. A label's box (its extent as the renderer measures it, in
    plane units, plus a margin) is placed only where it lies wholly in its region, so it crosses
    neither a border with another region nor an edge of the triangle: the feasible centres are the
    region's grid points eroded by the box. Of those the chosen one maximises the distance to the
    region's border less the local density of designs (a Gaussian-smoothed count, bandwidth 0.04;
    the distance counts a quarter as much).
    The largest of ``LABEL_SIZES`` that has a feasible centre is used, with the wrap (the same words
    on one to four lines) whose best centre scores highest. Nothing in the rule depends on the
    colour scheme, so the light and dark images get the same placement.
    """
    from scipy import ndimage

    n = 500
    x, y, top, left, right, inside = _grid(n)
    reg = np.full(top.shape, -1, int)
    reg[inside] = region_of(fit, s, top[inside], left[inside], right[inside])[0]
    dx = x[0, 1] - x[0, 0]
    dy = y[1, 0] - y[0, 0]
    px, py = project(comp[:, 0], comp[:, 1], comp[:, 2])
    hist, _, _ = np.histogram2d(
        py,
        px,
        bins=[y.shape[0], x.shape[1]],
        range=[[-dy / 2, SQ3 + dy / 2], [-dx / 2, 1 + dx / 2]],
    )
    density = ndimage.gaussian_filter(hist, sigma=0.04 / dx)
    density /= density.max()
    out = {}
    for k in range(len(fit["W"])):
        mask = reg == k
        if not mask.any():
            continue
        dist = ndimage.distance_transform_edt(mask) * dx
        text = says(fit["W"][k])
        for size in LABEL_SIZES:
            best = None
            for variant in _wraps(text):
                t, hw, hh = _box(ax, variant, size, ink, plate, col[k])
                nx = int(np.ceil((hw + LABEL_MARGIN) / dx))
                ny = int(np.ceil((hh + LABEL_MARGIN) / dy))
                ok = ndimage.binary_erosion(mask, structure=np.ones((2 * ny + 1, 2 * nx + 1), bool))
                score = np.where(ok, 0.25 * dist / dist.max() - density, -np.inf)
                i, j = np.unravel_index(np.argmax(score), score.shape)
                if ok.any() and (best is None or score[i, j] > best[0]):
                    if best is not None:
                        best[1].remove()
                    best = (score[i, j], t, (x[i, j], y[i, j]))
                else:
                    t.remove()
            if best is not None:  # the best wrap at the largest size that fits
                best[1].set_position(best[2])
                best[1].set_gid(f"why-label-{k}")
                out[k] = best[1]
                break
        else:
            raise RuntimeError(f"no room for the label of facet {k} inside its region")
    return out


def draw(fit, scheme="light", lines=False):
    """The figure: regions, designs, labels (and, when asked, the lines of equal V)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sc = SCHEMES[scheme]
    ink = sc["ink"]
    W, col = fit["W"], colours(fit["W"])
    s = 1.0 if lines else fit["spread"]
    comp = shares(fit, s)
    near = np.abs(fit["logv"]) < 0.2

    fig = plt.figure(figsize=FIGSIZE)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.set_xlim(-0.04, 1.04)
    ax.set_ylim(-0.13, SQ3 + 0.075)
    ax.patch.set_alpha(0.0)

    # the exact regions, as an image clipped by the triangle
    n = 900
    x, y, top, left, right, inside = _grid(n)
    reg = np.zeros(top.shape, int)
    reg[inside] = region_of(fit, s, top[inside], left[inside], right[inside])[0]
    mix, f = sc["mix"]
    mixc = _hex(mix)
    rgba = np.zeros((*top.shape, 4))
    for k in range(len(W)):
        rgba[reg == k, :3] = f * mixc + (1 - f) * _hex(col[k])
    rgba[..., 3] = inside.astype(float)
    ax.imshow(
        rgba,
        extent=(0, 1, 0, SQ3),
        origin="lower",
        interpolation="nearest",
        zorder=0,
        aspect="equal",
    )
    ax.set_xlim(-0.04, 1.04)
    ax.set_ylim(-0.13, SQ3 + 0.075)

    px, py = project(comp[:, 0], comp[:, 1], comp[:, 2])
    ax.scatter(px[~near], py[~near], s=7, color=sc["dots"], alpha=0.55, linewidths=0, zorder=2)
    for k in range(len(W)):
        mk = near & (fit["facet"] == k)
        ax.scatter(
            px[mk], py[mk], s=30, color=col[k], linewidths=0.6, edgecolors=sc["plate"], zorder=3
        )

    if lines:
        top_peak = _peak_level(fit, s)
        ratios = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.97])
        fval = np.full(top.shape, np.nan)
        fval[inside] = region_of(fit, s, top[inside], left[inside], right[inside])[1].max(axis=-1)
        ax.contour(
            x,
            y,
            fval - top_peak,
            levels=np.log(ratios),
            colors=[ink],
            linewidths=1.0,
            linestyles="solid",
            zorder=4,
        )
        for k in range(len(W)):
            sx, sy = project(W[k, 0], W[k, 1], W[k, 2])
            ax.scatter(
                [sx],
                [sy],
                marker="*",
                s=420,
                color=col[k],
                edgecolors=ink,
                linewidths=1.4,
                zorder=8,
                clip_on=False,
            )

    ax.plot([0, 0.5, 1, 0], [0, SQ3, 0, 0], color=ink, lw=1.4, solid_joinstyle="miter", zorder=5)

    place_labels(fit, comp, s, ax, ink, sc["plate"], col)
    corner = {"fontsize": 15, "fontweight": "bold", "color": ink, "zorder": 6}
    ax.text(0.5, SQ3 + 0.035, "favours metric 1", ha="center", va="bottom", **corner)
    ax.text(-0.03, -0.03, "favours\nmetric 2", ha="left", va="top", **corner)
    ax.text(1.03, -0.03, "favours\nmetric 3", ha="right", va="top", **corner)
    return fig


def _peak_level(fit, s):
    """The highest of the facets' own peaks (log V less the level), at their exponent vectors."""
    W = fit["W"]
    a = W @ fit["colmean"] - fit["beta"]
    logw = np.log(np.clip(W, 1e-300, None))
    peak = a + s * (logw * W).sum(axis=1)
    own = [int(np.argmax(a + s * (logw[k] @ W.T))) for k in range(len(W))]
    own_peaks = [peak[k] for k in range(len(W)) if own[k] == k]
    return float(max(own_peaks)) if own_peaks else float((a[None] + s * logw @ W.T).max())


def build(out=DEFAULT_OUT, lines=False, fit=None):
    """Write both schemes' images into ``out``; returns the paths by scheme."""
    import matplotlib.pyplot as plt

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    fit = fit or fit_why()
    paths = {}
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11}):
        for scheme, name in FILES.items():
            fig = draw(fit, scheme, lines=lines)
            paths[scheme] = out / name
            fig.savefig(paths[scheme], dpi=DPI, transparent=True)
            plt.close(fig)
    return paths


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    parser.add_argument(
        "--lines",
        action="store_true",
        help="overlay lines of equal V at a fixed total, with each facet's exponent vector as a "
        "star (off by default)",
    )
    args = parser.parse_args(argv)
    fit = fit_why()
    for scheme, path in build(args.out, lines=args.lines, fit=fit).items():
        print(f"{scheme}: {path}")
    print("exponents", np.round(fit["W"], 2).tolist())
    print("labels", [says(w).replace("\n", " ") for w in fit["W"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
