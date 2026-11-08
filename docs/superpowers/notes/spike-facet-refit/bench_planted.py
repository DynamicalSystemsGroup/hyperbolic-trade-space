"""Planted benchmark: N=400, d=4, K=3, seeds 0..19, tau in {inf, 50}, common initial labels.

uv run python <scratch>/bench_planted.py [solver|flipped]  -> writes planted_<init>.csv and prints.
"""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from methods import (
    RefitF,
    alternate,
    code_lines,
    evaluate,
    flipped_init,
    make_refit_C_hard,
    make_refit_C_soft,
    make_refit_E,
    refit_A,
    refit_B,
    refit_D,
    solver_init,
)

from hyperbolic_trade_space.datasets import make_frontier_data

HERE = Path(__file__).parent
INIT = sys.argv[1] if len(sys.argv) > 1 else "solver"
SEEDS = range(20)
TAUS = [np.inf, 50.0]
BAD = {1, 3, 8, 16}

METHODS = {
    "A": refit_A,
    "B": refit_B,
    "C_hard": make_refit_C_hard(0.2),
    "C_soft": make_refit_C_soft(1.0, 1e-3),
    "D": refit_D,
    "E": make_refit_E(1.0),
    "F": "F",  # fresh RefitF per data set (candidate cache)
}

rows = []
for s in SEEDS:
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    fr = info["frontier_mask"]
    n_front = np.bincount(info["facet"][fr], minlength=3)
    for tau in TAUS:
        if INIT == "solver":
            lab0 = solver_init(U, 3, seed=12345)
        else:
            lab0 = flipped_init(info["facet"], 3, 0.2, seed=s)
        for name, refit in METHODS.items():
            if refit == "F":
                refit = RefitF(4000, seed=0)
            if name.startswith("C") and np.isinf(tau):
                rows.append(
                    dict(
                        seed=s,
                        tau=tau,
                        method=name,
                        err=np.nan,
                        right=np.nan,
                        slack=np.nan,
                        conv=None,
                        n_iter=0,
                        time=np.nan,
                        min_front=int(n_front.min()),
                        note="undefined at tau=inf",
                    )
                )
                continue
            t0 = time.perf_counter()
            try:
                W, beta, lab, conv, n_iter = alternate(U, lab0, 3, tau, refit, max_iter=50)
                err, right, slack = evaluate(U, W, beta, lab, tau, info)
                note = ""
            except Exception as e:
                err = right = slack = np.nan
                conv, n_iter, note = None, 0, f"error: {e}"[:60]
            dt = time.perf_counter() - t0
            rows.append(
                dict(
                    seed=s,
                    tau=tau,
                    method=name,
                    err=err,
                    right=right,
                    slack=slack,
                    conv=conv,
                    n_iter=n_iter,
                    time=dt,
                    min_front=int(n_front.min()),
                    note=note,
                )
            )
    print(f"seed {s} done; frontier rows per facet {n_front.tolist()}", flush=True)

df = pd.DataFrame(rows)
df.to_csv(HERE / f"planted_{INIT}.csv", index=False)
df["pass"] = (df.err < 0.05) & (df.right >= 0.9)

pd.set_option("display.width", 250)
print(f"\n=== init: {INIT} ===")
for tau in TAUS:
    d = df[df.tau == tau]
    g = d.groupby("method")
    summ = pd.DataFrame(
        {
            "pass/20": g["pass"].sum().astype(int),
            "pass_bad4": d[d.seed.isin(BAD)].groupby("method")["pass"].sum().astype(int),
            "pass_good16": d[~d.seed.isin(BAD)].groupby("method")["pass"].sum().astype(int),
            "median_err": g.err.median().round(4),
            "max_err": g.err.max().round(3),
            "mean_right": g.right.mean().round(3),
            "mean_slack": g.slack.mean().round(4),
            "converged": g.conv.apply(lambda x: int(np.sum([bool(v) for v in x if v is not None]))),
            "mean_iter": g.n_iter.mean().round(1),
            "mean_time_s": g.time.mean().round(3),
        }
    )
    print(f"\n--- tau = {tau} ---")
    print(summ.to_string())
    print("\nfailing seeds (1, 3, 8, 16) detail: err / right")
    bad = d[d.seed.isin(BAD)].pivot(index="seed", columns="method", values="err").round(3)
    print(bad.to_string())
    badr = d[d.seed.isin(BAD)].pivot(index="seed", columns="method", values="right").round(2)
    print(badr.to_string())

print("\ncode lines per refit step (non-blank, non-docstring):")
for name, refit in METHODS.items():
    fn = RefitF if refit == "F" else refit
    print(f"  {name}: {code_lines(fn)}")
