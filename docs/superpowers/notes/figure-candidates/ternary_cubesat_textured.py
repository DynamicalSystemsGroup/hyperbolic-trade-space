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


def main():
    for key, (regime, names, K) in CANDIDATES.items():
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
                plot_ternary(est, st.M, names=list(names), lines=True)
                plt.gcf().savefig(
                    HERE
                    / f"ternary-cubesat-textured-{key}-{scheme}.png",
                    bbox_inches="tight",
                    transparent=True,
                    metadata={"Software": None},
                )
                plt.close("all")


if __name__ == "__main__":
    main()
