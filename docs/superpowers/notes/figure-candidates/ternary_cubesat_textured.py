"""The S-5 textured candidates: the triples of the search, drawn.

Run from the repository root (after ``triple_search.py`` has chosen)::

    uv run python \
        docs/superpowers/notes/figure-candidates/ternary_cubesat_textured.py

Each candidate is a regime, three attributes and a K. The three columns
are conditioned alone with the case module's conditioning, the
temperature is selected by ``case.fit_study`` and the figure is
``plot_ternary(..., lines=True)``, as the docs' Figure 6 draws its
table, in the docs' light and dark schemes. Designs are one neutral
colour (no colouring by cell). The terms' rows, near-frontier counts and
exact-maximum exponents are printed.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "examples" / "adcs"), str(ROOT / "scripts")]

import build_figures  # noqa: E402
import case  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from hyperbolic_trade_space import plotting  # noqa: E402
from hyperbolic_trade_space.plotting import plot_ternary  # noqa: E402

# a region of a real fit can be small: let the labels fall to the case's
# smallest legible size (``case.FIGURE_MIN_FONT_PT``) before giving up
plotting._TERN_LABEL_SIZES += (13.0, 12.0, 11.0, 10.0, 9.5)
# redraw iteration (WP19): the regions are model regions, not clusters
# of designs, so the fill is a light tint and each border a drawn line;
# the dark render is saved on its own dark ground so the corner names
# are read as on a dark page
plotting._TERN_SCHEMES = {
    "light": {
        **plotting._TERN_SCHEMES["light"],
        "mix": ("#ffffff", 0.90),
    },
    "dark": {
        **plotting._TERN_SCHEMES["dark"],
        "mix": ("#191817", 0.80),
    },
}
GROUND = {"light": "#ffffff", "dark": "#191817"}

HERE = Path(__file__).resolve().parent
CANDIDATES = {
    "A": (
        "primary",
        ("pointing error", "total mass", "control effort"),
        2,
    ),
    "B": (
        "primary",
        ("settling time", "control effort", "depth of discharge"),
        2,
    ),
    "C": (
        "primary",
        ("pointing error", "energy balance", "depth of discharge"),
        3,
    ),
}


def triple_study(regime, names):
    full = case.load_study(regime)
    attrs = tuple(full.attrs[full.names.index(n)] for n in names)
    cond, M = case._condition(full.feasible, attrs, full.spec)
    return case.Study(
        full.spec, regime, full.raw, full.feasible, attrs, M, cond
    )


# the dashed border in a colour of its own: the thin lines are ink
BORDER = {"light": "#c2410c", "dark": "#ffb347"}
MARKER_NAMES = {"*": "star", "D": "diamond"}


def draw_borders_and_key(ax, est, M, scheme):
    """A line where the leading term changes, the callouts moved to open
    space, and the key."""
    import numpy as np
    from matplotlib.lines import Line2D

    sch = plotting._TERN_SCHEMES[scheme]
    fit = plotting._ternary_geometry(est, M)
    x, y, top, left, right, inside = plotting._ternary_grid(900)
    reg = np.full(top.shape, np.nan)
    reg[inside] = plotting._ternary_region_of(
        fit, 1.0, top[inside], left[inside], right[inside]
    )[0]
    edge = BORDER[scheme]
    for k in range(1, len(fit["W"])):
        ax.contour(
            x,
            y,
            reg,
            levels=[k - 0.5],
            colors=[edge],
            linewidths=2.6,
            linestyles=[(0, (6, 3))],
            zorder=4.5,
        )
    ink = sch["ink"]
    W = est.exponents_
    col = plotting._ternary_colours(W)

    # callouts: out of the triangle, beside the apex, joined to the
    # marker of the term they name by a thin line in its colour
    side = {"left": 0.0, "right": 0.0}
    for k in range(len(W)):
        gid = f"ternary-label-{k}"
        t = ax.findobj(lambda a, g=gid: a.get_gid() == g)
        if not t:
            continue
        t = t[0]
        sx, sy = plotting._ternary_project(*W[k])
        words = " ".join(t.get_text().split())
        for cut in (" against ",):
            words = words.replace(cut, "\nagainst ")
        if "\n" not in words and len(words) > 24:
            words = words.replace(" alone", "\nalone")
        t.set_text(words)
        which = "left" if sx < 0.5 else "right"
        cx = {"left": 0.06, "right": 0.94}[which]
        cy = 0.80 - side[which]
        side[which] += 0.2
        t.set_position((cx, cy))
        t.set_fontsize(14)
        t.set_ha("center")
        t.set_va("center")
        ax.annotate(
            "",
            xy=(sx, sy),
            xytext=(cx, cy),
            textcoords="data",
            arrowprops={
                "arrowstyle": "-",
                "color": col[k],
                "lw": 1.6,
                "shrinkA": 24,
                "shrinkB": 9,
            },
            zorder=3.5,
        )

    keys = [
        Line2D(
            [],
            [],
            marker="o",
            ls="",
            ms=8,
            mfc=sch["dots"],
            mec=sch["plate"],
        ),
        Line2D([], [], color=ink, lw=1.0),
        Line2D([], [], color=edge, lw=2.6, ls=(0, (6, 3))),
    ]
    text = [
        "a design, placed by its shares of the three metrics\n"
        "(each scaled by its typical size); larger: near the frontier",
        "thin lines: equal invariant value V at a fixed total\n"
        "(0.3 to 0.97 of the peak)",
        "dashed line: where the leading term changes",
    ]
    for k in range(len(W)):
        m = plotting._TERN_MARKERS[k % len(plotting._TERN_MARKERS)][0]
        keys.append(
            Line2D(
                [],
                [],
                marker=m,
                ls="",
                ms=11,
                mfc=col[k],
                mec=ink,
                mew=1.2,
            )
        )
        text.append(
            f"{MARKER_NAMES.get(m, m)}: term {k + 1}'s exponent vector"
            " (where its V peaks)"
        )
    leg = ax.legend(
        keys,
        text,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.0),
        ncol=1,
        fontsize=11,
        frameon=False,
        labelcolor=ink,
        handlelength=2.2,
        borderaxespad=2.6,
        labelspacing=0.7,
    )
    leg.set_zorder(10)


def main():
    for key, (regime, names, K) in CANDIDATES.items():
        if key == "C":  # dropped: each region is one metric alone
            continue
        st = triple_study(regime, names)
        fit = case.fit_study(st, K=K)
        est = fit.estimator
        reps = case.term_reports(est, st.M, fit.band)
        lab = est.assign_cells(st.M)
        print(key, regime, names, "K", K, "tau", round(fit.tau, 2))
        for k, r in enumerate(reps):
            print(
                "  term",
                k + 1,
                "rows",
                int((lab == k).sum()),
                "near",
                r.n_near_frontier,
                "exact",
                [round(float(x), 2) for x in r.contending_exponents],
                "set",
                [
                    names[j]
                    for j, x in zip(
                        r.contending_set,
                        r.contending_exponents,
                        strict=True,
                    )
                    if x >= case.CO_CONTENDER
                ],
                "working",
                est.exponents_[k].round(2).tolist(),
            )
        for scheme in ("light", "dark"):
            with build_figures._apply(scheme):
                ax = plot_ternary(
                    est, st.M, names=list(names), lines=True
                )
                draw_borders_and_key(ax, est, st.M, scheme)
                plt.gcf().savefig(
                    HERE
                    / f"ternary-cubesat-textured-{key}-{scheme}.png",
                    bbox_inches="tight",
                    facecolor=GROUND[scheme],
                    metadata={"Software": None},
                )
                plt.close("all")


if __name__ == "__main__":
    main()
