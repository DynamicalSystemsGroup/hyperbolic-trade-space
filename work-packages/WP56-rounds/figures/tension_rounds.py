"""WP56 figure loop, Figure 7: the tension matrix's values and the rounds' renders.

Run ``uv run python work-packages/WP56-rounds/figures/tension_rounds.py``. Prints, for each term of
the case's K = 2 fit (primary regime), the matrix in both row orders and the range of each half,
and writes ``tension-values.txt`` and the current round's PNG beside this file (light theme,
100 dpi, the paper's call ``case.tension_matrix_figure``). Earlier rounds' PNGs are kept as they
were rendered: r0 the paper's figure before WP56; r1 the two halves in exponent order; r2 the upper
half in tension order, the colour bar's full range; r3 the bar cut to the drawn side; r4 the grey
diagonal kept.
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "examples" / "adcs")]

import case  # noqa: E402

import hyperbolic_trade_space as hts  # noqa: E402

CURRENT = ("r4-upper-tension-diagonal", "upper", "tension")  # round, triangle, order


def values(study, fit):
    T = hts.tension_matrix(fit.estimator, study.M)
    W = np.atleast_2d(fit.estimator.exponents_)
    names = list(study.names)
    out = []
    for k, w in enumerate(W):
        by_w = [j for j in np.argsort(-w, kind="stable") if w[j] > 1e-3]
        for order in case.TENSION_ORDERS:
            keep = case.tension_order(T[k], by_w, order)
            up = [abs(T[k, i, j]) for a, i in enumerate(keep) for j in keep[a + 1 :]]
            lo = [abs(T[k, i, j]) for a, i in enumerate(keep) for j in keep[:a]]
            out.append(f"term {k + 1}, order {order}: " + ", ".join(names[j] for j in keep))
            out.append(
                f"  upper half |T|: min {min(up):.3f}, max {max(up):.3f}, "
                f"{sum(v < 1 for v in up)} of {len(up)} below one"
            )
            out.append(
                f"  lower half |T|: min {min(lo):.3f}, max {max(lo):.3f}, "
                f"{sum(v > 1 for v in lo)} of {len(lo)} above one"
            )
            for i in keep:
                cells = " ".join("      -" if i == j else f"{abs(T[k, i, j]):7.3f}" for j in keep)
                out.append(f"  {names[i]:>20} w={w[i]:.3f} {cells}")
    return "\n".join(out)


def main():
    import matplotlib.pyplot as plt

    study = case.load_study("primary")
    fit = case.fit_study(study, K=case.CASE_K)
    text = values(study, fit)
    print(text)
    (HERE / "tension-values.txt").write_text(text + "\n", encoding="utf-8")
    name, triangle, order = CURRENT
    fig = case.tension_matrix_figure(study, fit, triangle=triangle, order=order)
    fig.savefig(HERE / f"tension-{name}.png", dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
