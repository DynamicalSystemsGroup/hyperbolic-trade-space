"""(1) Five restarts per method (the built solver's seeds), selected by the common mean slack.
(2) Is the planted solution the mean-slack optimum? slack(planted) vs slack(found).
uv run python <scratch>/bench_restarts.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.utils import check_random_state

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from methods import (  # noqa: E402
    RefitF,
    alternate,
    evaluate,
    make_refit_E,
    refit_B,
    refit_D,
    solver_init,
    support_beta,
)

from hyperbolic_trade_space.datasets import make_frontier_data  # noqa: E402

BAD = {1, 3, 8, 16}
METHODS = {"B": refit_B, "D": refit_D, "E": make_refit_E(1.0), "F": "F"}
rows, cmp_rows = [], []
for s in range(20):
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    seeds = check_random_state(0).randint(0, 2**31 - 1, size=5)  # as solve_terms(random_state=0)
    for tau in [np.inf, 50.0]:
        Wt = info["exponents"]
        bt = support_beta(U, Wt, tau)
        labt = np.argmax(U @ Wt.T - bt, axis=1)
        slack_planted = float(np.mean(bt[labt] - np.sum(Wt[labt] * U, axis=1)))
        for name, refit in METHODS.items():
            best = None
            for sd in seeds:
                r = RefitF(4000, seed=0) if refit == "F" else refit
                lab0 = solver_init(U, 3, seed=sd)
                W, beta, lab, conv, n_iter = alternate(U, lab0, 3, tau, r, max_iter=50)
                err, right, slack = evaluate(U, W, beta, lab, tau, info)
                if best is None or slack < best[2]:
                    best = (err, right, slack, conv)
            err, right, slack, conv = best
            rows.append(
                dict(
                    seed=s,
                    tau=tau,
                    method=name,
                    err=err,
                    right=right,
                    slack=slack,
                    conv=conv,
                    slack_planted=slack_planted,
                    found_below_planted=slack < slack_planted - 1e-9,
                )
            )
    print(f"seed {s} done", flush=True)

df = pd.DataFrame(rows)
df.to_csv(HERE / "restarts.csv", index=False)
df["pass"] = (df.err < 0.05) & (df.right >= 0.9)
pd.set_option("display.width", 250)
for tau in [np.inf, 50.0]:
    d = df[df.tau == tau]
    g = d.groupby("method")
    print(f"\n=== 5 restarts, best common slack, tau = {tau} ===")
    print(
        pd.DataFrame(
            {
                "pass/20": g["pass"].sum().astype(int),
                "pass_bad4": d[d.seed.isin(BAD)].groupby("method")["pass"].sum().astype(int),
                "median_err": g.err.median().round(4),
                "max_err": g.err.max().round(3),
                "mean_right": g.right.mean().round(3),
                "found<planted (seeds)": g.apply(
                    lambda x: sorted(x.seed[x.found_below_planted].tolist())
                ),
                "fail seeds": g.apply(lambda x: sorted(x.seed[~x["pass"]].tolist())),
            }
        ).to_string()
    )
    print(
        "bad seeds err:\n"
        + d[d.seed.isin(BAD)]
        .pivot(index="seed", columns="method", values="err")
        .round(3)
        .to_string()
    )
    print("slack planted vs found (B), bad seeds:")
    print(
        d[(d.method == "B") & d.seed.isin(BAD)][["seed", "slack_planted", "slack"]]
        .round(4)
        .to_string(index=False)
    )
