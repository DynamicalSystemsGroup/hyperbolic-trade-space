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
planted figure took its place).

``--lines`` (off by default, and off everywhere on the site) overlays lines of equal V at a fixed
total: the shares are ``c_j = (m_j / typical_j)^(1/s) / L`` with ``s = 1`` and ``L`` their sum, the
function drawn is ``f(c) = max_k (a_k + s * sum_j w_kj log c_j)`` with
``a_k = w_k . colmean - beta_k``, and each term's exponent vector ``w_k`` is a star in the term's
colour, exactly where that term's V peaks at a fixed total.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from hyperbolic_trade_space import plotting as _tern
from hyperbolic_trade_space.plotting import plot_ternary

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "build" / "site-figures"
FILES = {"light": "why-regions-light.png", "dark": "why-regions-dark.png"}
STORY_FILES = {"light": "ternary-planted-light.png", "dark": "ternary-planted-dark.png"}

N_ROWS, N_METRICS, N_TERMS, DATA_SEED = 900, 3, 3, 11
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


def fit_why():
    """The planted table and its three-term fit: the data, exponents, offsets, cells, log V."""
    from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

    X, _ = make_frontier_data(N_ROWS, N_METRICS, n_terms=N_TERMS, random_state=DATA_SEED)
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


def build_all(out=DEFAULT_OUT):
    """The root page's images: the story figure (the Why image no longer sits on the page)."""
    return {"story": build_story(out)}


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
    print("exponents", np.round(fit["W"], 2).tolist())
    print("labels", [says(w).replace("\n", " ") for w in fit["W"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
