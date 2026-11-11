"""The S-5 alternative ternary: a 3-lemma in the cubesat data of record.

Run from the repository root::

    uv run python \
        docs/superpowers/notes/figure-candidates/ternary_cubesat_trilemma.py

Settling time, pointing error and total mass on the primary regime's
706 feasible designs (``examples/adcs/data/v2``), conditioned on these
three attributes alone with the case module's conditioning (per column,
so the table equals the three columns of the eight-metric table) and
fitted with ``case.fit_study`` (the temperature for a tenth of designs
above V = 1, the case's seed). The one-term contending set, the support
of the exact-maximum exponents (``tension_report``), is all three
metrics. The figure is ``plot_ternary(..., lines=True)``, as the docs'
Figure 6 draws its synthetic table, saved beside this script in the
docs' light and dark schemes; ``ternary_marker_values`` is printed.
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
from hyperbolic_trade_space import tension_report  # noqa: E402
from hyperbolic_trade_space.plotting import (  # noqa: E402
    plot_ternary,
    ternary_marker_values,
)

ATTRS = ("settling_time_s", "pointing_error_deg", "total_mass_kg")
HERE = Path(__file__).resolve().parent


def trilemma():
    """The three-metric study, its one-term fit and its report."""
    full = case.load_study("primary")
    cond, M = case._condition(full.feasible, ATTRS, full.spec)
    study = case.Study(
        full.spec, "primary", full.raw, full.feasible, ATTRS, M, cond
    )
    fit = case.fit_study(study, K=1)
    return study, fit, tension_report(fit.estimator, M)


def main():
    study, fit, rep = trilemma()
    names = list(study.names)
    est = fit.estimator
    print("designs", len(study.M), "tau", round(fit.tau, 3))
    print("contending set", [names[j] for j in rep.contending_set])
    print("exact-maximum", rep.contending_exponents.round(3).tolist())
    print("working", est.exponents_.round(3).tolist())
    print("near-frontier", rep.n_near_frontier)
    values = ternary_marker_values(est, study.M, names=names)
    print(values.round(2).to_string(index=False))
    for scheme in ("light", "dark"):
        with build_figures._apply(scheme):
            plot_ternary(est, study.M, names=names, lines=True)
            plt.gcf().savefig(
                HERE / f"ternary-cubesat-trilemma-{scheme}.png",
                bbox_inches="tight",
                transparent=True,
                metadata={"Software": None},
            )
            plt.close("all")


if __name__ == "__main__":
    main()
