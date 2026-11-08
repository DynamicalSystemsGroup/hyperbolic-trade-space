"""Table (i): certificates on the built solver's outputs, planted K = 3, d = 4, N = 400, seeds 0..19,
tau in {inf, 50}.  Run from the repo root:  uv run python <folder>/run_planted.py
Writes planted.csv and planted_restarts.csv next to this file."""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.utils import check_random_state

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from certificates import termination_report  # noqa: E402

from hyperbolic_trade_space.datasets import make_frontier_data  # noqa: E402
from hyperbolic_trade_space.solvers import _solve_terms_once, solve_terms  # noqa: E402


def exponent_error(W, W_true):
    C = np.abs(W[:, None] - W_true[None]).max(-1)
    r, c = linear_sum_assignment(C)
    return float(C[r, c].max())


rows, rrows = [], []
kw = {"min_exponent": 0.0, "penalty": None, "alpha": 0.0, "tol": 1e-10, "max_iter": 500}
t0 = time.time()
for tau in (np.inf, 50.0):
    for s in range(20):
        X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
        U = np.log(X)
        # exactly the estimator's call (defaults: n_restarts=5, max_iter=50, random_state=0)
        res = solve_terms(U, 3, tau, random_state=0)
        term, gaps, fvals, shares, F_fixed, ms = termination_report(U, res, tau)
        err = exponent_error(res.W, info["exponents"])
        rows.append({"tau": tau, "seed": s, "err": err, **term.as_dict(),
                     "gaps": np.round(gaps, 12).tolist(), "shares": np.round(shares, 4).tolist(),
                     "F_fixed_minus_objective": F_fixed - res.objective,
                     "mean_slack_minus_objective": ms - res.objective})  # fmt: skip
        # the five restarts individually (same seeds as solve_terms draws)
        seeds = check_random_state(0).randint(0, 2**31 - 1, size=5)
        for j, sd in enumerate(seeds):
            r1 = _solve_terms_once(U, 3, tau, sd, 50, kw)
            t1, g1, *_ = termination_report(U, r1, tau)
            rrows.append({"tau": tau, "seed": s, "restart": j, "objective": r1.objective,
                          "n_iter": r1.n_iter, "reason": r1.message, "max_gap": t1.max_gap,
                          "gamma": t1.gamma, "changes": t1.assignment_changes,
                          "n_empty": t1.n_empty, "status": t1.status,
                          "chosen": bool(np.isclose(r1.objective, res.objective))})  # fmt: skip
        print(f"tau={tau:>5} seed={s:2d} {term.reason:22s} it={term.n_iter:2d} maxG={term.max_gap:.1e} "
              f"bound={term.bound:.1e} gamma={term.gamma:.2e} radius={term.radius:.2e} "
              f"chg={term.assignment_changes} empty={term.n_empty} feas={term.feas_sum:.0e} "
              f"dobj={term.objective_change:.1e} err={err:.3f} {term.status}", flush=True)
print(f"elapsed {time.time() - t0:.0f}s")
df = pd.DataFrame(rows)
df.to_csv(HERE / "planted.csv", index=False)
dr = pd.DataFrame(rrows)
dr.to_csv(HERE / "planted_restarts.csv", index=False)

print("\n== chosen runs: termination reason by tau")
print(df.groupby(["tau", "reason"]).size())
print("\n== chosen runs: status by tau")
print(df.groupby(["tau", "status"]).size())
for eps in (1e-6, 1e-8, 1e-10):
    ok = df[(df.max_gap <= eps) & (df.assignment_changes == 0) & (df.gamma > 0) & (df.reason == "assignment fixed")]
    print(f"certified at eps_KKT={eps:g}: " + ", ".join(f"tau={t}: {len(ok[ok.tau == t])}/20" for t in (np.inf, 50.0)))
print("\n== max_gap quantiles by tau (chosen runs)")
print(df.groupby("tau").max_gap.describe(percentiles=[.5, .9]).to_string())
print("\n== gamma and radius by tau (chosen runs)")
print(df.groupby("tau")[["gamma", "radius"]].describe(percentiles=[.1, .5, .9]).T.to_string())
print(f"\ngamma <= 0: {(df.gamma <= 0).sum()} of {len(df)};  gamma < 1e-6: {(df.gamma < 1e-6).sum()}")
print(f"empty facets in chosen runs: {(df.n_empty > 0).sum()}")
print(f"|F_fixed - objective| max = {df.F_fixed_minus_objective.abs().max():.1e};  |mean slack - objective| max = {df.mean_slack_minus_objective.abs().max():.1e}")
print("\n== all 200 restarts: reason and status")
print(dr.groupby(["tau", "reason"]).size())
print(dr.groupby(["tau", "status"]).size())
print(dr.groupby("tau").max_gap.describe(percentiles=[.5, .9, .99]).to_string())
print(f"\nrestarts with gamma <= 0: {(dr.gamma <= 0).sum()}; with empty facets: {(dr.n_empty > 0).sum()}")
print("\n== recovery vs certification (chosen runs)")
print(pd.crosstab([df.tau, df.status], df.err < 0.05))
