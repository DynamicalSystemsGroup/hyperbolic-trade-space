"""(c) Can the alternation be made to find the planted partition under each objective?

Rules (the smallest change that makes the alternation minimize the objective):
  sel:Oj    five restarts (the built solver's seeds), select by Oj instead of mean slack
  best:Oj   one init, B path, keep the best iterate along the path by Oj
  guard:Oj  one init, B path, stop when Oj gets worse (the built guard with Oj instead of O0)
  G         per-facet step minimizing O4's term (min_w J(Uw) - LME_own(Uw)), B warm start
Tables as round 1's 3b (single init: solver 12345 and 20 % flipped) and 3c (five restarts).

uv run python <folder>/bench_c.py  -> prints; writes recovery_single.csv, recovery_restarts.csv
"""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.utils import check_random_state

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from methods import evaluate, flipped_init, refit_B, refit_D, solver_init  # noqa: E402
from objectives import alternate_traced, better, make_refit_G  # noqa: E402

from hyperbolic_trade_space.datasets import make_frontier_data  # noqa: E402

BAD = {1, 3, 8, 16}
TAUS = [np.inf, 50.0]
SEL = ["O0", "O1", "T", "T0", "O2", "O3", "O4", "O5"]
G = make_refit_G(10.0)
pd.set_option("display.width", 250)

single, multi = [], []
for s in range(20):
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    restart_seeds = check_random_state(0).randint(0, 2**31 - 1, size=5)
    for tau in TAUS:
        for init_name, lab0 in [
            ("solver", solver_init(U, 3, seed=12345)),
            ("flipped", flipped_init(info["facet"], 3, 0.2, seed=s)),
        ]:
            variants = [("B", refit_B, {}), ("D", refit_D, {}), ("G", G, {})]
            for name in ["O1", "T", "O2", "O3", "O4", "O5"]:
                variants.append((f"B best:{name}", refit_B, dict(keep_best=name)))
                variants.append((f"B guard:{name}", refit_B, dict(guard=name)))
            variants.append(("B guard:O0", refit_B, dict(guard="O0")))
            for vname, step, kw in variants:
                t0 = time.perf_counter()
                W, beta, lab, conv, n_iter, _ = alternate_traced(U, lab0, 3, tau, step, **kw)
                dt = time.perf_counter() - t0
                err, right, slack = evaluate(U, W, beta, lab, tau, info)
                single.append(dict(seed=s, tau=tau, init=init_name, variant=vname, err=err, right=right,
                                   slack=slack, conv=conv, n_iter=n_iter, time=dt))  # fmt: skip
        # restarts: B, D, G; select by each objective
        for step_name, step in [("B", refit_B), ("D", refit_D), ("G", G)]:
            runs = []
            for sd in restart_seeds:
                lab0 = solver_init(U, 3, seed=sd)
                W, beta, lab, conv, n_iter, trace = alternate_traced(U, lab0, 3, tau, step)
                err, right, slack = evaluate(U, W, beta, lab, tau, info)
                runs.append((err, right, trace[-1] if len(trace) else None, conv))
            for sel in SEL:
                best = None
                for err, right, vals, conv in runs:
                    v = vals[sel]
                    if best is None or better(sel, v, best[2]):
                        best = (err, right, v, conv)
                multi.append(dict(seed=s, tau=tau, step=step_name, select=sel, err=best[0], right=best[1],
                                  value=best[2], conv=best[3]))  # fmt: skip
    print(f"seed {s} done", flush=True)

sg = pd.DataFrame(single)
sg.to_csv(HERE / "recovery_single.csv", index=False)
sg["pass"] = (sg.err < 0.05) & (sg.right >= 0.9)
for init_name in ["solver", "flipped"]:
    for tau in TAUS:
        d = sg[(sg.init == init_name) & (sg.tau == tau)]
        g = d.groupby("variant", sort=False)
        summ = pd.DataFrame({
            "pass/20": g["pass"].sum().astype(int),
            "pass_bad4": d[d.seed.isin(BAD)].groupby("variant", sort=False)["pass"].sum().astype(int),
            "bad_pass_seeds": d[d.seed.isin(BAD)].groupby("variant", sort=False).apply(lambda x: sorted(x.seed[x["pass"]].tolist())),
            "median_err": g.err.median().round(4),
            "mean_right": g.right.mean().round(3),
            "mean_slack": g.slack.mean().round(4),
            "converged": g.conv.sum().astype(int),
            "mean_iter": g.n_iter.mean().round(1),
            "s/run": g.time.mean().round(3),
        })  # fmt: skip
        print(f"\n=== single init: {init_name}, tau = {tau} ===")
        print(summ.to_string())
        print("bad seeds err (rows) by variant:")
        print(
            d[d.seed.isin(BAD)]
            .pivot(index="variant", columns="seed", values="err")
            .reindex(summ.index)
            .round(3)
            .to_string()
        )

mg = pd.DataFrame(multi)
mg.to_csv(HERE / "recovery_restarts.csv", index=False)
mg["pass"] = (mg.err < 0.05) & (mg.right >= 0.9)
for tau in TAUS:
    d = mg[mg.tau == tau]
    print(f"\n=== five restarts, tau = {tau}: pass/20 by (step, selection objective) ===")
    t = d.pivot_table(index="select", columns="step", values="pass", aggfunc="sum").reindex(SEL)
    print(t.astype(int).to_string())
    print("fail seeds:")
    for step in ["B", "D", "G"]:
        for sel in SEL:
            dd = d[(d.step == step) & (d.select == sel)]
            print(f"  {step} sel:{sel}: {sorted(dd.seed[~dd['pass']].tolist())}")
