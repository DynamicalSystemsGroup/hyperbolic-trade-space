"""Build the root index page's own figure: the planted triangle of three metrics.

    uv run python scripts/build_site_figures.py [--out DIR] [--lines]

The triangle is the positions of three metrics, shaded by the trade-off that binds there. The
table is the package's planted three-term table, the fit is the package's own estimator, and the
regions are exact: the term k that binds at a position is the argmax over k of
``w_k . p - beta_k``.
Every word on the figure is read from the fitted exponents (nothing is hand-placed): the colour
of a region follows from which term trades all three metrics, its label names the metrics whose
exponents are large, and the label sits where the region holds few designs.

The triangle is drawn by the package's own ``plot_ternary`` (plain Matplotlib, the barycentric
projection written out there: ``x = right + top / 2``, ``y = sqrt(3) / 2 * top``), the function the
documentation's examples call; this script supplies the planted table, the fit and the figure.
:func:`build_story` writes the table with the lines of equal V and the numbered markers,
``ternary-planted-light.png`` and ``ternary-planted-dark.png``, on transparent backgrounds and with
the colours of the root page's two schemes: the one figure of the root page (the plain image,
``why-regions-light.png`` and ``why-regions-dark.png`` from :func:`build`, left the page when the
planted figure took its place). :func:`build_preview` writes the site's preview image, the one
link handlers show: the planted triangle in the light scheme with the site's name, at the size
``site/metadata.toml`` names.

``--lines`` (off by default, and off everywhere on the site) overlays lines of equal V at a fixed
total: the shares are ``c_j = (m_j / typical_j)^(1/s) / L`` with ``s = 1`` and ``L`` their sum, the
function drawn is ``f(c) = max_k (a_k + s * sum_j w_kj log c_j)`` with
``a_k = w_k . colmean - beta_k``, and each term's exponent vector ``w_k`` is a star in the term's
colour, exactly where that term's V peaks at a fixed total.
"""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import numpy as np

from tradespace import plotting as _tern
from tradespace.plotting import plot_ternary

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "build" / "site-figures"
FILES = {"light": "why-regions-light.png", "dark": "why-regions-dark.png"}
STORY_FILES = {"light": "ternary-planted-light.png", "dark": "ternary-planted-dark.png"}

N_ROWS, N_METRICS, N_TERMS, DATA_SEED = 900, 3, 3, 11
# the planted table's construction beyond the package's defaults: most designs on or just below
# the surface (70% on it, the rest 0.25 below on average), the surface rows scattered by 0.07, so
# the data reach the surface at every position and about a tenth lie beyond it
PLANT = {"frontier_fraction": 0.7, "interior_scale": 0.25, "noise": 0.07}
# the temperature is the figure's to tune (the supervisor, 2026-11-14); 50 with the table below
TEMPERATURE, FIT_SEED = 50.0, 0
FIGSIZE, DPI = (7.4, 7.0), 170  # the axes span 1.08 by 1.07 plane units, so the triangle fills it
BLUE, AMBER, GREEN = "#0072B2", "#E69F00", "#009E73"
NAMES = ["metric 1", "metric 2", "metric 3"]

# the one implementation is the package's; these names keep the generator's own vocabulary
BIG, SQ3 = _tern._TERN_BIG, _tern._SQ3
project, region_of = _tern._ternary_project, _tern._ternary_region_of
colours, shares, regions = _tern._ternary_colours, _tern._ternary_shares, _tern._ternary_regions


def says(w):
    """The trade-off a term with exponent vector ``w`` names, in words, read from its exponents."""
    return _tern._ternary_says(np.asarray(w, float), NAMES)


def fit_why(exponents=None, **plant):
    """The planted table and its three-term fit: the data, exponents, offsets, cells, log V.

    ``exponents`` (default: the package's seeded draw) sets the planted exponent vectors; ``plant``
    passes ``frontier_fraction``, ``interior_scale``, ``noise`` and the like to the generator.
    """
    from tradespace import HyperbolicTradeSpace, make_frontier_data

    X, _ = make_frontier_data(
        N_ROWS,
        N_METRICS,
        n_terms=N_TERMS,
        random_state=DATA_SEED,
        exponents=exponents,
        **{**PLANT, **plant},
    )
    ts = HyperbolicTradeSpace(n_terms=N_TERMS, temperature=TEMPERATURE, random_state=FIT_SEED)
    ts.fit(X)
    return {
        **_tern._ternary_geometry(ts, X),
        "X": X,
        "estimator": ts,
        "cell": np.asarray(ts.cell_),
        "logv": np.asarray(ts.score_samples(X), float),
    }


def draw(fit, scheme="light", lines=False):
    """The figure: ``plot_ternary`` on the planted table, on a transparent full-figure axes."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=FIGSIZE)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    plot_ternary(fit["estimator"], fit["X"], names=NAMES, lines=lines, ax=ax, scheme=scheme)
    for t in ax.texts:  # the tests and the page address the region labels by this id
        gid = t.get_gid() or ""
        if gid.startswith("ternary-label-"):
            t.set_gid(gid.replace("ternary-label-", "why-label-"))
    return fig


def build(out=DEFAULT_OUT, lines=False, fit=None, files=None):
    """Write both schemes' images into ``out``; returns the paths by scheme."""
    import matplotlib.pyplot as plt

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    fit = fit or fit_why()
    paths = {}
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11}):
        for scheme, name in (files or FILES).items():
            fig = draw(fit, scheme, lines=lines)
            paths[scheme] = out / name
            fig.savefig(paths[scheme], dpi=DPI, transparent=True)
            plt.close(fig)
    return paths


def build_story(out=DEFAULT_OUT, fit=None):
    """The planted table with lines of equal V and numbered markers: both schemes, into ``out``."""
    return build(out, lines=True, fit=fit, files=STORY_FILES)


# ---------------------------------------------------------------------------------------------
# The slices figure: the three metric pairs by three views, the third metric held at its median.
# ---------------------------------------------------------------------------------------------
SLICE_SPAN = (1, 99)  # the percentiles of each metric that the axes span
SLICE_PAIRS = ((0, 1), (1, 2), (0, 2))  # metric pairs (rows); the metric left out is held
SLICE_DPI = 150


def held_at(fit, third, value, quantile=0.5):
    """The log metrics held for a slice: the third at ``value``, the others at ``quantile``."""
    hold = np.quantile(fit["U"], quantile, axis=0)
    hold[third] = value
    return hold


def held_label(quantile):
    """How a row names the held value: ``its median`` or ``its 20th percentile``."""
    if abs(quantile - 0.5) < 1e-9:
        return "its median"
    n = round(100 * quantile)
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"its {n}{suffix} percentile"


def slice_pieces(fit, i, j, hold, box, n=4000):
    """The fitted surface ``log V = 0`` in the plane of metrics ``i`` and ``j``, by term.

    The other log metrics are held at ``hold``. Each term's piece is the line
    ``w_i u_i + w_j u_j = beta - w_rest . hold`` where that term attains the maximum, an exact
    envelope (no grid). Returns ``[(k, xy)]`` with ``xy`` of shape ``(m, 2)`` in log metrics
    ``(i, j)``, runs separated by a row of ``nan``.
    """
    W, beta = fit["W"], fit["beta"]
    rest = [r for r in range(W.shape[1]) if r not in (i, j)]
    const = beta - W[:, rest] @ hold[rest]
    (lo_x, hi_x), (lo_y, hi_y), out = box[0], box[1], []
    lo, hi = np.array([lo_x, lo_y]), np.array([hi_x, hi_y])
    for k in range(len(W)):
        a = W[k, [i, j]]
        if np.linalg.norm(a) < 1e-9:
            continue
        p0, t = const[k] * a / (a @ a), np.array([-a[1], a[0]]) / np.linalg.norm(a)
        reach = 2 * float((hi - lo).max())
        s = np.linspace(-reach, reach, n)
        xy = p0 + s[:, None] * t
        inside = ((xy >= lo) & (xy <= hi)).all(axis=1)
        phi = xy @ W[:, [i, j]].T - const
        on = inside & (phi[:, k] >= phi.max(axis=1) - 1e-9)
        if not on.any():
            continue
        runs = np.split(np.flatnonzero(on), np.flatnonzero(np.diff(np.flatnonzero(on)) > 1) + 1)
        xy_k = np.vstack([np.vstack([xy[r], [np.nan, np.nan]]) for r in runs])
        out.append((k, xy_k))
    return out


# ---------------------------------------------------------------------------------------------
# The slices figure (WP51 rework, candidate A): the third metric held at its median only. One
# surface per pane as one connected curve in the three term colours (the paper's Figure 1 drawn
# three ways), the chart as Figure 1 draws it (the surface laid flat, the designs below it), the
# designs within a band of the median as dots; nothing else.
# ---------------------------------------------------------------------------------------------
SLICE_FILES = {"light": "site-slices-light.png", "dark": "site-slices-dark.png"}
SLICE_BAND = 0.15  # half-width, in log metric, of the designs drawn with the held median


def _hard_logv(fit, u):
    """The surface's value ``max_k (w_k . u - beta_k)`` at log positions ``u`` (rows)."""
    return (np.atleast_2d(u) @ fit["W"].T - fit["beta"]).max(axis=1)


def term_styles(fit):
    """The one table of how a term is drawn: ``[(number, colour, marker shape, marker size)]`` by
    term index. The slices' lines, markers and legend read from it; the triangle's markers are
    drawn by ``plot_ternary`` from the same two sources (``_ternary_colours`` of the fit's
    exponents, ``_TERN_MARKERS`` by index, the number the index plus one), and a test compares
    the two figures' artists."""
    col = colours(fit["W"])
    marks = _tern._TERN_MARKERS
    return [(k + 1, col[k], *marks[k % len(marks)]) for k in range(len(fit["W"]))]


def marker_points(fit):
    """The triangle's markers as points of the surface, in log metrics, one row per term.

    A marker sits at a term's exponent vector read as shares ``c = w_k``; the ray ``m = t c``
    (each metric in units of its typical size) meets the surface once, at ``t = 1 / V(c)``,
    because V is homogeneous of degree one: ``u = log c + colmean - max_k' (w_k' . (log c +
    colmean) - beta_k')``.
    """
    base = np.log(np.clip(fit["W"], 1e-300, None)) + fit["colmean"]
    return base - _hard_logv(fit, base)[:, None]


def draw_slices(fit, scheme="light", pairs=SLICE_PAIRS, markers=True, quantile=0.5):
    """Rows the metric pairs; columns the metric space, the log space and the chart (the surface
    laid flat along the pair's axis ``(e_i - e_j) / sqrt(2)``, the designs below it). The metric
    left out of a pair is held at the ``quantile`` of its values over the planted table (the median
    by default; the supervisor's ruling of 2026-11-15 that the held value is an option, not a
    constant). ``markers`` adds the three
    terms' characteristic points on the surface (the triangle's markers) on the chart column,
    where the surface is laid flat and they lie exactly on its line; the other two columns are a
    section at one value of the third metric, which three such points cannot share."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgb
    from matplotlib.lines import Line2D

    sch = _tern._TERN_SCHEMES[scheme]
    ink = sch["ink"]
    styles = term_styles(fit)
    tcol = {k: st[1] for k, st in enumerate(styles)}
    U, lv, d = fit["U"], fit["logv"], fit["U"].shape[1]
    span = np.percentile(U, SLICE_SPAN, axis=0)
    fig, axes = plt.subplots(len(pairs), 3, figsize=(11.6, 3.5 * len(pairs) + 0.9), squeeze=False)
    fig.patch.set_alpha(0.0)
    heads = ("Metric space: the fitted reference surface", "Log space: the surface as an envelope",
             "Chart: the surface laid flat")  # fmt: skip
    for r, (i, j) in enumerate(pairs):
        (third,) = [m for m in range(d) if m not in (i, j)]
        q = float(np.quantile(U[:, third], quantile))
        hold = held_at(fit, third, q, quantile)
        near = np.abs(U[:, third] - q) <= SLICE_BAND
        zs = (U[:, i] - U[:, j]) / np.sqrt(2)
        for c, ax in enumerate(axes[r]):
            ax.set_facecolor("none")
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            for sp in ax.spines.values():
                sp.set_color(ink)
            ax.tick_params(colors=ink, labelsize=9)
            ax.xaxis.label.set_color(ink)
            ax.yaxis.label.set_color(ink)
            if r == 0:
                ax.set_title(heads[c], color=ink, fontsize=10.5, loc="left", pad=30)
            xs, ys = (U[near, i], U[near, j]) if c < 2 else (zs[near], lv[near])
            if c == 0:
                xs, ys = np.exp(xs), np.exp(ys)
            # darker the nearer a design is to the slice, faint at the edge of the band
            dist = np.abs(U[near, third] - q) / SLICE_BAND
            rgba = np.zeros((len(xs), 4))
            rgba[:, :3] = to_rgb(sch["dots"])
            rgba[:, 3] = 0.95 - 0.8 * dist
            far_first = np.argsort(-dist)
            ax.scatter(xs[far_first], ys[far_first], s=9, c=rgba[far_first], linewidth=0, zorder=2)
        for k, xy in slice_pieces(fit, i, j, hold, (span[:, i], span[:, j])):
            for c in (0, 1):
                x, y = xy[:, 0], xy[:, 1]
                axes[r, c].plot(np.exp(x) if c == 0 else x, np.exp(y) if c == 0 else y,
                                color=tcol[k], lw=2.8, zorder=4,
                                solid_capstyle="round")  # fmt: skip
            zk = (xy[:, 0] - xy[:, 1]) / np.sqrt(2)
            axes[r, 2].plot([np.nanmin(zk), np.nanmax(zk)], [0, 0], color=tcol[k], lw=4,
                            zorder=4, solid_capstyle="butt")  # fmt: skip
        if (
            markers
        ):  # the terms' characteristic points on the surface (the triangle's three markers)
            for k, u in enumerate(marker_points(fit)):
                _, colour, shape, size = styles[k]
                axes[r, 2].scatter([(u[i] - u[j]) / np.sqrt(2)], [0], marker=shape,
                                   s=size * 0.45, color=colour, edgecolors=ink,
                                   linewidths=1.2, zorder=9)  # fmt: skip
        for c in (0, 1):
            ax = axes[r, c]
            ax.set_xlabel(f"{'log ' if c else ''}{NAMES[i]}", fontsize=10)
            ax.set_ylabel(f"{'log ' if c else ''}{NAMES[j]}", fontsize=10)
        axes[r, 0].set_xlim(0, np.exp(span[1, i]))
        axes[r, 0].set_ylim(0, np.exp(span[1, j]))
        axes[r, 1].set_xlim(span[0, i] - 0.2, span[1, i] + 0.2)
        axes[r, 1].set_ylim(span[0, j] - 0.2, span[1, j] + 0.2)
        ax = axes[r, 2]
        zspan = (span[0, i] - span[1, j], span[1, i] - span[0, j])
        ax.set_xlim(zspan[0] / np.sqrt(2), zspan[1] / np.sqrt(2))
        ax.set_xlabel(f"position along the {NAMES[i]} against {NAMES[j]} axis", fontsize=10)
        ax.set_ylabel("log V", fontsize=10)
        ax.set_ylim(max(np.percentile(lv, 2), -3.5), 0.6)
    lines = [Line2D([], [], color=colour, lw=3.5, label=f"term {number}")
             for number, colour, _, _ in styles]  # fmt: skip
    legend = lines
    if markers:  # one column per term: the line over its characteristic point
        points = [Line2D([], [], marker=shape, ls="", markerfacecolor=colour,
                         markeredgecolor=ink, markersize=8, label="characteristic point")
                  for _, colour, shape, _ in styles]  # fmt: skip
        legend = [h for pair in zip(lines, points, strict=True) for h in pair]
    fig.legend(handles=legend, loc="lower center", ncol=len(lines), frameon=False,
               labelcolor=ink, fontsize=9.5, columnspacing=3.0,
               bbox_to_anchor=(0.5, 0.0))  # fmt: skip
    fig.tight_layout(rect=(0, 0.07 if markers else 0.04, 1, 1), h_pad=3.2)
    for r, (i, j) in enumerate(pairs):
        (third,) = [m for m in range(d) if m not in (i, j)]
        y = axes[r, 0].get_position().y1 + 0.008
        label = held_label(quantile)
        fig.text(0.01, y, f"{NAMES[i]} against {NAMES[j]}, with {NAMES[third]} at {label}",
                 color=ink, fontsize=11, fontweight="bold", va="bottom")  # fmt: skip
    return fig


def build_slices(out=DEFAULT_OUT, fit=None, quantile=0.5):
    """The slices figure from the planted fit (``fit_why()`` unless given), both schemes; the
    metric left out of each pair held at ``quantile`` (the median by default)."""
    import matplotlib.pyplot as plt

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    fit = fit or fit_why()
    paths = {}
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 10}):
        for scheme, name in SLICE_FILES.items():
            fig = draw_slices(fit, scheme, quantile=quantile)
            paths[scheme] = out / name
            fig.savefig(paths[scheme], dpi=SLICE_DPI, transparent=True)
            plt.close(fig)
    return paths


# ---------------------------------------------------------------------------------------------
# The preview image: what a link handler shows beside a link to the site. The planted triangle in
# the light scheme on the right, the site's name, tagline and address on the left; the size link
# handlers take (site/metadata.toml names it: 1200 by 630 px), an opaque background.
# ---------------------------------------------------------------------------------------------
PREVIEW_DPI = 100
PREVIEW_BACKGROUND = "#faf9f6"  # the root page's light background
PREVIEW_INK, PREVIEW_MUTED = "#1c1c1c", "#5a5a5a"  # the root page's light text colours


def draw_preview(fit, values):
    """The preview figure, ``values["image_width"]`` by ``values["image_height"]`` px at
    ``PREVIEW_DPI``."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    width, height = values["image_width"], values["image_height"]
    fig = plt.figure(figsize=(width / PREVIEW_DPI, height / PREVIEW_DPI), dpi=PREVIEW_DPI)
    fig.patch.set_facecolor(PREVIEW_BACKGROUND)
    fig.patch.set_alpha(1.0)
    side = 0.92 * height / width  # the triangle's axes, square in pixels, nearly the full height
    ax = fig.add_axes([0.985 - side, 0.04, side, 0.92])
    plot_ternary(fit["estimator"], fit["X"], names=NAMES, ax=ax, scheme="light")
    left = 0.05
    fig.text(left, 0.66, values["name"], fontsize=56, fontweight="bold", color=PREVIEW_INK,
             va="baseline")  # fmt: skip
    fig.text(left, 0.54, values["tagline"], fontsize=24, color=PREVIEW_INK, va="baseline")
    lead = textwrap.fill(values["description"].split(":", 1)[0], 30)  # the description's lead
    fig.text(left, 0.40, lead, fontsize=17, color=PREVIEW_MUTED, va="top", linespacing=1.5)
    address = values["url"].removeprefix("https://").rstrip("/")
    fig.text(left, 0.09, address, fontsize=15, color=PREVIEW_MUTED, va="baseline")
    return fig


def build_preview(out=DEFAULT_OUT, fit=None, values=None):
    """Write the preview image into ``out`` under the name ``site/metadata.toml`` gives; returns
    its path."""
    import matplotlib.pyplot as plt
    import site_metadata

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    fit = fit or fit_why()
    values = values or site_metadata.load()
    path = out / values["image"]
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11}):
        fig = draw_preview(fit, values)
        fig.savefig(path, dpi=PREVIEW_DPI, facecolor=fig.get_facecolor())
        plt.close(fig)
    from PIL import Image  # Matplotlib's own image library: an opaque RGB file, no alpha channel

    with Image.open(path) as image:
        image.convert("RGB").save(path, optimize=True)
    return path


def build_all(out=DEFAULT_OUT):
    """The root page's images, the story figure and the slices figure, and the site's preview
    image, from one fit."""
    fit = fit_why()
    return {
        "story": build_story(out, fit=fit),
        "slices": build_slices(out, fit=fit),
        "preview": build_preview(out, fit=fit),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    parser.add_argument(
        "--lines",
        action="store_true",
        help="overlay lines of equal V at a fixed total, with each term's exponent vector as a "
        "star (off by default)",
    )
    args = parser.parse_args(argv)
    fit = fit_why()
    for scheme, path in build(args.out, lines=args.lines, fit=fit).items():
        print(f"{scheme}: {path}")
    for scheme, path in build_story(args.out, fit=fit).items():
        print(f"story {scheme}: {path}")
    for scheme, path in build_slices(args.out, fit=fit).items():
        print(f"slices {scheme}: {path}")
    print(f"preview: {build_preview(args.out, fit=fit)}")
    print("exponents", np.round(fit["W"], 2).tolist())
    print("labels", [says(w).replace("\n", " ") for w in fit["W"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
