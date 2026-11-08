"""(a) Monotonicity of each objective along the B and D alternations (round 1's loop, no guard),
planted data, seeds 0..19, tau in {inf, 50}, solver init 12345 and 20 % flipped init.
(b) Planted partition vs found (B, init 12345) vs the five restarts (the built solver's seeds),
per objective, all seeds; seeds 1, 3, 8, 16 in detail.

uv run python <folder>/bench_ab.py   -> prints; writes mono.csv, planted_vs_found.csv, restarts_all.csv
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.utils import check_random_state

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from methods import evaluate, flipped_init, refit_B, refit_D, solver_init  # noqa: E402
from objectives import (  # noqa: E402
    MINIMIZE,
    OBJECTIVES,
    alternate_traced,
    better,
    evaluate_all,
    planted_state,
)

from hyperbolic_trade_space.datasets import make_frontier_data  # noqa: E402

BAD = [1, 3, 8, 16]
TAUS = [np.inf, 50.0]
NAMES = list(OBJECTIVES)
pd.set_option("display.width", 250)

mono_rows, pf_rows, rs_rows = [], [], []
for s in range(20):
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    n_front = np.bincount(info["facet"][info["frontier_mask"]], minlength=3)
    restart_seeds = check_random_state(0).randint(0, 2**31 - 1, size=5)
    for tau in TAUS:
        # (a) monotonicity, two inits, two steps
        for init_name, lab0 in [
            ("solver", solver_init(U, 3, seed=12345)),
            ("flipped", flipped_init(info["facet"], 3, 0.2, seed=s)),
        ]:
            for step_name, step in [("B", refit_B), ("D", refit_D)]:
                W, beta, lab, conv, n_iter, trace = alternate_traced(U, lab0, 3, tau, step)
                # full iterations: compare 'refit' of it to the previous accepted state
                prev = trace[0]
                for rec in trace[1:]:
                    for name in NAMES:
                        a, b = prev[name], rec[name]
                        if np.isnan(a) or np.isnan(b):
                            worse = np.nan
                        else:
                            worse = float(
                                better(name, a, b)
                            )  # previous strictly better -> got worse
                        mono_rows.append(
                            dict(seed=s, tau=tau, init=init_name, step=step_name, half=rec["half"],
                                 it=rec["it"], objective=name, worse=worse)
                        )  # fmt: skip
                    if rec["half"] == "refit":
                        prev = rec
                    else:
                        prev_assign = rec
                        prev = rec
                if init_name == "solver" and step_name == "B":
                    found = (W, beta, lab)
        # (b) planted vs found vs restarts
        Wt, bt, labt = planted_state(U, info["exponents"], tau)
        vp = evaluate_all(U, Wt, bt, labt, tau)
        vf = evaluate_all(U, *found, tau)
        errf, rightf, _ = evaluate(U, *found, tau, info)
        rec = dict(
            seed=s, tau=tau, min_front=int(n_front.min()), err_found=errf, right_found=rightf
        )
        for name in NAMES:
            rec[f"{name}_planted"] = vp[name]
            rec[f"{name}_found"] = vf[name]
            rec[f"{name}_planted_better"] = better(name, vp[name], vf[name])
        # five restarts of B and D
        for step_name, step in [("B", refit_B), ("D", refit_D)]:
            for j, sd in enumerate(restart_seeds):
                lab0 = solver_init(U, 3, seed=sd)
                W, beta, lab, conv, n_iter, trace = alternate_traced(U, lab0, 3, tau, step)
                err, right, _ = evaluate(U, W, beta, lab, tau, info)
                v = evaluate_all(U, W, beta, lab, tau)
                rs_rows.append(dict(seed=s, tau=tau, step=step_name, restart=j, err=err, right=right,
                                    conv=conv, n_iter=n_iter, **v))  # fmt: skip
            rs = pd.DataFrame(
                [
                    r
                    for r in rs_rows
                    if r["seed"] == s and r["tau"] == tau and r["step"] == step_name
                ]
            )
            for name in NAMES:
                vals = rs[name].to_numpy()
                if np.all(np.isnan(vals)):
                    rec[f"{name}_best5_{step_name}"] = np.nan
                    rec[f"{name}_planted_beats5_{step_name}"] = np.nan
                    continue
                best = np.nanmin(vals) if MINIMIZE[name] else np.nanmax(vals)
                rec[f"{name}_best5_{step_name}"] = best
                rec[f"{name}_planted_beats5_{step_name}"] = better(name, vp[name], best)
        pf_rows.append(rec)
    print(f"seed {s} done; frontier rows per facet {n_front.tolist()}", flush=True)

mono = pd.DataFrame(mono_rows)
mono.to_csv(HERE / "mono.csv", index=False)
pf = pd.DataFrame(pf_rows)
pf.to_csv(HERE / "planted_vs_found.csv", index=False)
rs = pd.DataFrame(rs_rows)
rs.to_csv(HERE / "restarts_all.csv", index=False)

print(
    "\n=== (a) fraction of half-steps in which the objective got WORSE (nan: undefined at that tau) ==="
)
for tau in TAUS:
    d = mono[mono.tau == tau]
    t = d.pivot_table(index="objective", columns=["step", "half"], values="worse", aggfunc="mean")
    t["n_full_iters_B"] = d[(d.step == "B") & (d.half == "refit") & (d.objective == "O0")].shape[0]
    t["n_full_iters_D"] = d[(d.step == "D") & (d.half == "refit") & (d.objective == "O0")].shape[0]
    print(
        f"\n--- tau = {tau} (assign: reassignment half-step; refit: refit half-step; both inits pooled) ---"
    )
    print(t.reindex(NAMES).round(3).to_string())
    # full-iteration monotonicity: previous refit -> this refit
    full = []
    for name in NAMES:
        for step in ["B", "D"]:
            dd = d[(d.objective == name) & (d.step == step)]
            # recompute per run: worse over a full iteration
            full.append(dict(objective=name, step=step, refit_half_worse=dd[dd.half == "refit"].worse.mean(),
                             assign_half_worse=dd[dd.half == "assign"].worse.mean()))  # fmt: skip
    print(
        pd.DataFrame(full)
        .pivot(index="objective", columns="step")
        .reindex(NAMES)
        .round(3)
        .to_string()
    )

print("\n=== (b) planted vs found (B, init 12345): seeds 1, 3, 8, 16 ===")
for tau in TAUS:
    d = pf[pf.tau == tau].set_index("seed")
    print(
        f"\n--- tau = {tau} --- (planted | found | best of 5 B restarts | best of 5 D restarts; * = planted better)"
    )
    for name in NAMES:
        cols = []
        for s in BAD:
            r = d.loc[s]
            pb = "*" if r[f"{name}_planted_better"] else " "
            p5b = "*" if r[f"{name}_planted_beats5_B"] is True else " "
            p5d = "*" if r[f"{name}_planted_beats5_D"] is True else " "
            cols.append(
                f"s{s}: {r[f'{name}_planted']:.4f} |{pb}{r[f'{name}_found']:.4f} |{p5b}{r[f'{name}_best5_B']:.4f} |{p5d}{r[f'{name}_best5_D']:.4f}"
            )
        print(f"{name:3s} " + "   ".join(cols))
    print(
        "found B err/right:",
        {s: (round(d.loc[s].err_found, 3), round(d.loc[s].right_found, 2)) for s in BAD},
    )
    print("\nseeds where PLANTED is strictly better than FOUND (B, init 12345), per objective:")
    for name in NAMES:
        seeds = sorted(d.index[d[f"{name}_planted_better"] == True].tolist())  # noqa: E712
        print(f"  {name}: {len(seeds)}/20 {seeds}")
    print("seeds where PLANTED is strictly better than the BEST OF 5 B restarts:")
    for name in NAMES:
        seeds = sorted(d.index[d[f"{name}_planted_beats5_B"] == True].tolist())  # noqa: E712
        print(f"  {name}: {len(seeds)}/20 {seeds}")

print(
    "\n=== restarts: on the bad seeds, how many of the 5 B / D restarts pass (err<0.05, right>=0.9)? ==="
)
rs["pass"] = (rs.err < 0.05) & (rs.right >= 0.9)
for tau in TAUS:
    d = rs[rs.tau == tau]
    print(
        f"tau = {tau}: "
        + "; ".join(
            f"s{s} B {int(d[(d.seed == s) & (d.step == 'B')]['pass'].sum())}/5, D {int(d[(d.seed == s) & (d.step == 'D')]['pass'].sum())}/5"
            for s in BAD
        )
    )
    print(
        "  all seeds, number of seeds with >=1 passing restart: B",
        int(d[d.step == "B"].groupby("seed")["pass"].any().sum()),
        "D",
        int(d[d.step == "D"].groupby("seed")["pass"].any().sum()),
    )
