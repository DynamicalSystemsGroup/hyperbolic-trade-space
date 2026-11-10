"""Table (ii): certificates on the cubesat primary and stock tables at K = 3 (the k3 record's
re-selected taus; the estimator's exact solve_terms call), plus the K = 1 tau as a diagnostic.
Run from the repo root:  uv run python <folder>/run_cubesat.py"""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path.cwd() / "examples" / "adcs"))
from certificates import termination_report  # noqa: E402
from k_terms import DATA, REGIMES, load_metrics, select_tau  # noqa: E402

from hyperbolic_trade_space.solvers import solve_terms  # noqa: E402

# the taus of the spike's own run, recorded in docs/superpowers/notes/k3-cubesat.md (deleted; last
# version at 4409920); recomputed below if --select is given
RECORDED = {"primary": {1: 38.10, 3: 195.18}, "stock": {1: 41.72, 3: 162.78}}
rows = []
for regime in REGIMES:
    feasible, M = load_metrics(DATA / REGIMES[regime])
    U = np.log(M)
    taus = dict(RECORDED[regime])
    if "--select" in sys.argv:
        t0 = time.time()
        taus[3] = select_tau(M, 3)
        print(f"{regime}: select_tau(K=3) = {taus[3]:.2f} ({time.time() - t0:.0f}s)")
    for label, tau in (("K=3 tau", taus[3]), ("K=1 tau (diagnostic)", taus[1]), ("tau=inf", np.inf)):
        for seed in range(5):
            res = solve_terms(U, 3, tau, random_state=seed)
            term, gaps, fvals, shares, F_fixed, ms = termination_report(U, res, tau)
            # duplicate rows and exact score ties
            S = U @ res.W.T - res.beta
            srt = np.sort(S, 1)
            n_tie = int((srt[:, -1] - srt[:, -2] < 1e-12).sum())
            rows.append({"regime": regime, "which": label, "tau": round(float(tau), 2), "seed": seed,
                         "N": U.shape[0], **term.as_dict(), "objective": res.objective,
                         "gaps": np.round(gaps, 10).tolist(), "facet_rows": np.bincount(res.labels, minlength=3).tolist(),
                         "exact_ties": n_tie, "F_fixed_minus_obj": F_fixed - res.objective})  # fmt: skip
            print(f"{regime:8s} {label:22s} tau={tau:>8.2f} seed={seed} {term.reason:20s} it={term.n_iter:2d} "
                  f"obj={res.objective:.6f} maxG={term.max_gap:.1e} bound={term.bound:.1e} gamma={term.gamma:.2e} "
                  f"radius={term.radius:.2e} chg={term.assignment_changes} empty={term.n_empty} ties={n_tie} "
                  f"dobj={term.objective_change:.1e} {term.status}", flush=True)
    n_dup = len(feasible) - len(pd.DataFrame(U).drop_duplicates())
    print(f"{regime}: N={len(feasible)}, duplicate log-metric rows: {n_dup}, max ||(u,-1)|| = {np.sqrt((U**2).sum(1) + 1).max():.3f}")
df = pd.DataFrame(rows)
df.to_csv(HERE / "cubesat.csv", index=False)
print("\n== status by regime and setting")
print(df.groupby(["regime", "which", "status"]).size().to_string())
print("\n== max_gap, gamma, radius, bound by regime and setting")
print(df.groupby(["regime", "which"])[["max_gap", "bound", "gamma", "radius", "n_iter", "objective"]].agg(["min", "max"]).to_string())
