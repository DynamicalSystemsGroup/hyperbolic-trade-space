"""WP56 figure loop, the decision-maker's ternary: the fits' numbers and the current round's render.

Run ``uv run python work-packages/WP56-rounds/figures/ternary_rounds.py``. Prints the identity
fleet cost = unit cost x fleet size on the data of record, the range of the coverage probability,
and each fit's exponents (K = 1, 2) on the primary regime's feasible designs; writes
``ternary-values.txt`` and the current round's PNGs beside this file (light theme, 100 dpi, the
call ``case.fleet_ternary_figure``). Earlier rounds' PNGs are kept as they were rendered.
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

CURRENT = "r4"
KS = (1, 2)  # the fits whose numbers are printed
RENDER = (
    1,
)  # r1 rendered K = 1 and K = 2; r2 and r3 K = 1 (r3: corners by what a design there has)


def main():
    import matplotlib.pyplot as plt

    st = case.fleet_ternary_study()
    df = st.feasible
    ratio = df["fleet_cost_usd"] / (df["unit_cost_usd"] * df["fleet_size"])
    lines = [
        f"feasible designs (primary regime): {len(df)}",
        f"fleet cost / (unit cost x fleet size): min {ratio.min():.12f}, max {ratio.max():.12f}",
        f"coverage probability: min {df[case.COVERAGE].min():.4f}, "
        f"max {df[case.COVERAGE].max():.4f}",
        f"fleet size: {int(df['fleet_size'].min())} to {int(df['fleet_size'].max())}",
    ]
    fits = {K: case.fit_study(st, K) for K in KS}
    for K, fit in fits.items():
        W = np.atleast_2d(fit.estimator.exponents_)
        lines.append(f"K = {K}, tau {fit.tau:.3f}:")
        for k, w in enumerate(W):
            share = f", share {fit.estimator.term_share_[k]:.2f}" if K > 1 else ""
            lines.append(
                f"  term {k + 1}: "
                + ", ".join(f"{n} {v:.3f}" for n, v in zip(st.names, w, strict=True))
                + share
            )
    text = "\n".join(lines)
    print(text)
    (HERE / "ternary-values.txt").write_text(text + "\n", encoding="utf-8")
    for K in RENDER:
        fit = fits[K]
        fig = case.fleet_ternary_figure(st, fit, K)
        fig.savefig(
            HERE / f"ternary-{CURRENT}-k{K}.png", dpi=100, bbox_inches="tight", facecolor="white"
        )
        plt.close(fig)


if __name__ == "__main__":
    main()
