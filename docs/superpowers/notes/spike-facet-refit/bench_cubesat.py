"""Cubesat primary table, K = 3, seeds 0..4 (the solver's initialization per seed), per method.

uv run python <scratch>/bench_cubesat.py  -> prints and writes cubesat.csv
"""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path.cwd() / "examples" / "adcs"))
from k_terms import DATA, NAMES, REGIMES, load_metrics  # noqa: E402
from methods import (  # noqa: E402
    RefitF,
    alternate,
    make_refit_C_hard,
    make_refit_C_soft,
    make_refit_E,
    match,
    refit_A,
    refit_B,
    refit_D,
    solver_init,
    support_beta,
)

from hyperbolic_trade_space import select_temperature  # noqa: E402

feasible, M = load_metrics(DATA / REGIMES["primary"])
U = np.log(M)
tau = select_temperature(M, target_frac_above=0.10, bounds=(3, 1e3))
band = 1.0 / tau
print(f"N={len(M)}, d={M.shape[1]}, tau={tau:.3f}, band={band:.4f}")

METHODS = {
    "A": refit_A,
    "B": refit_B,
    "C_hard": make_refit_C_hard(0.2),
    "C_soft": make_refit_C_soft(1.0, 1e-3),
    "D": refit_D,
    "E": make_refit_E(1.0),
    "F": "F",
}
THR = 0.05


def contend(w):
    return "+".join(NAMES[j] for j in np.argsort(-w) if w[j] > THR)


rows, fits = [], {}
for name, refit in METHODS.items():
    for s in range(5):
        r = RefitF(4000, seed=0) if refit == "F" else refit
        lab0 = solver_init(U, 3, seed=s)
        t0 = time.perf_counter()
        W, beta, lab, conv, n_iter = alternate(U, lab0, 3, tau, r, max_iter=50)
        dt = time.perf_counter() - t0
        bs = support_beta(U, W, tau)
        lab_s = np.argmax(U @ W.T - bs, axis=1)
        slack = float(np.mean(bs[lab_s] - np.sum(W[lab_s] * U, axis=1)))
        own_slack = float(np.mean(beta[lab] - np.sum(W[lab] * U, axis=1)))
        logv = np.max(U @ W.T - bs, axis=1)
        near = np.abs(logv) < band
        shares = np.bincount(lab_s[near], minlength=3) / max(near.sum(), 1)
        sizes = np.bincount(lab_s, minlength=3)
        fits[(name, s)] = W
        rows.append(
            dict(
                method=name,
                seed=s,
                slack=slack,
                own_slack=own_slack,
                conv=conv,
                n_iter=n_iter,
                time=dt,
                n_near=int(near.sum()),
                shares=sorted(np.round(shares, 3).tolist(), reverse=True),
                sizes=sorted(sizes.tolist(), reverse=True),
                sets=" | ".join(sorted(contend(w) for w in W)),
                n_lemma=sorted((W > THR).sum(1).tolist(), reverse=True),
            )
        )
    # stability vs seed 0 after facet matching
    W0 = fits[(name, 0)]
    for s in range(5):
        perm = match(fits[(name, s)], W0)
        rows[-5 + s]["dev_vs_seed0"] = float(np.abs(fits[(name, s)] - W0[perm]).max())
    print(f"{name} done", flush=True)

df = pd.DataFrame(rows)
df.to_csv(HERE / "cubesat.csv", index=False)
pd.set_option("display.width", 300)
pd.set_option("display.max_colwidth", 200)
print(
    df[
        [
            "method",
            "seed",
            "slack",
            "own_slack",
            "conv",
            "n_iter",
            "time",
            "shares",
            "sizes",
            "n_lemma",
            "dev_vs_seed0",
        ]
    ]
    .round(4)
    .to_string(index=False)
)
print("\ncontending sets (exponent > 0.05), per method and seed:")
for name in METHODS:
    d = df[df.method == name]
    print(f"\n[{name}] distinct signatures: {d.sets.nunique()} of 5")
    for _, r in d.iterrows():
        print(f"  seed {r.seed}: {r.sets}")
summ = df.groupby("method").agg(
    slack_mean=("slack", "mean"),
    slack_sd=("slack", "std"),
    dev_max=("dev_vs_seed0", "max"),
    conv=("conv", "sum"),
    iters=("n_iter", "mean"),
    time=("time", "mean"),
    signatures=("sets", "nunique"),
)
print("\nsummary:\n" + summ.round(4).to_string())
