"""Oracle: each refit step applied once to the TRUE planted labels (no alternation).

Isolates the quality of the per-facet step from the assignment dynamics. Per facet: exponent
error of that facet vs its number of frontier rows. uv run python <scratch>/bench_oracle.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from methods import (  # noqa: E402
    RefitF,
    make_refit_C_hard,
    make_refit_C_soft,
    make_refit_E,
    refit_A,
    refit_B,
    refit_D,
)

from hyperbolic_trade_space.datasets import make_frontier_data  # noqa: E402

METHODS = {
    "A": refit_A, "B": refit_B, "C_hard": make_refit_C_hard(0.2),
    "C_soft": make_refit_C_soft(1.0, 1e-3), "D": refit_D, "E": make_refit_E(1.0), "F": "F",
}  # fmt: skip

rows = []
for s in range(20):
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    lab = info["facet"]
    n_front = np.bincount(lab[info["frontier_mask"]], minlength=3)
    n_rows = np.bincount(lab, minlength=3)
    for tau in [np.inf, 50.0]:
        for name, refit in METHODS.items():
            if name.startswith("C") and np.isinf(tau):
                continue
            r = RefitF(4000, seed=0) if refit == "F" else refit
            W0, b0 = np.full((3, 4), 0.25), np.zeros(3)
            W, b = r(U, lab, 3, tau, W0, b0, 0)
            if name in ("D", "E", "C_soft"):  # these need planes: one more step on fixed labels
                W, b = r(U, lab, 3, tau, W, b, 1)
            err_k = np.abs(W - info["exponents"]).max(1)  # same facet order, no matching needed
            for k in range(3):
                rows.append(
                    dict(
                        seed=s,
                        tau=tau,
                        method=name,
                        facet=k,
                        n_front=int(n_front[k]),
                        n_rows=int(n_rows[k]),
                        err=float(err_k[k]),
                    )
                )
df = pd.DataFrame(rows)
df.to_csv(HERE / "oracle.csv", index=False)
df["bin"] = pd.cut(df.n_front, [0, 4, 11, 30, 1000], labels=["<=4", "5-11", "12-30", ">30"])
pd.set_option("display.width", 250)
for tau in [np.inf, 50.0]:
    d = df[df.tau == tau]
    print(
        f"\n=== oracle (true labels), tau = {tau}: "
        "median / max facet exponent error by frontier rows"
    )
    t = d.pivot_table(
        index="method", columns="bin", values="err", aggfunc=["median", "max"], observed=False
    ).round(3)
    print(t.to_string())
    print("counts per bin:", d[d.method == "B"].bin.value_counts().sort_index().to_dict())
    print(
        "facets recovered to 0.05, all facets:",
        d.groupby("method").err.apply(lambda e: int((e < 0.05).sum())).to_dict(),
        "of 60",
    )
