"""(d) Cubesat primary table, K = 3, seeds 0..4, under each objective's alternation.

Per seed s (the solver's init, seed s, shared): B (O0 reference), B best:Oj, B guard:Oj, D, G.
Also: which of the 5 B fits each objective would select (restart selection).
uv run python <folder>/bench_cubesat2.py  -> prints; writes cubesat2.csv
"""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
REPO = Path("/Users/z/Documents/GitHub/posynomial-invariant-form")
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "examples" / "adcs"))
from k_terms import DATA, NAMES, REGIMES, load_metrics  # noqa: E402
from methods import match, refit_B, refit_D, solver_init, support_beta  # noqa: E402
from objectives import MINIMIZE, OBJECTIVES, alternate_traced, make_refit_G  # noqa: E402

from hyperbolic_trade_space import select_temperature  # noqa: E402

feasible, M = load_metrics(DATA / REGIMES["primary"])
U = np.log(M)
tau = select_temperature(M, target_frac_above=0.10, bounds=(3, 1e3))
band = 1.0 / tau
print(f"N={len(M)}, d={M.shape[1]}, tau={tau:.3f}, band={band:.4f}")
THR = 0.05
G = make_refit_G(10.0)


def contend(w):
    return "+".join(NAMES[j] for j in np.argsort(-w) if w[j] > THR)


VARIANTS = [("B", refit_B, {}), ("D", refit_D, {}), ("G", G, {})]
for name in ["O1", "T", "O2", "O3", "O4", "O5"]:
    VARIANTS.append((f"B best:{name}", refit_B, dict(keep_best=name)))
    VARIANTS.append((f"B guard:{name}", refit_B, dict(guard=name)))

rows, fits, last = [], {}, {}
for vname, step, kw in VARIANTS:
    for s in range(5):
        lab0 = solver_init(U, 3, seed=s)
        t0 = time.perf_counter()
        W, beta, lab, conv, n_iter, trace = alternate_traced(U, lab0, 3, tau, step, **kw)
        dt = time.perf_counter() - t0
        bs = support_beta(U, W, tau)
        lab_s = np.argmax(U @ W.T - bs, axis=1)
        vals = {k: f(U, W, bs, lab_s, tau) for k, f in OBJECTIVES.items()}
        logv = np.max(U @ W.T - bs, axis=1)
        near = np.abs(logv) < band
        shares = np.bincount(lab_s[near], minlength=3) / max(near.sum(), 1)
        fits[(vname, s)] = W
        rows.append(dict(variant=vname, seed=s, conv=conv, n_iter=n_iter, time=dt, n_near=int(near.sum()),
                         shares=sorted(np.round(shares, 3).tolist(), reverse=True),
                         sets=" | ".join(sorted(contend(w) for w in W)),
                         n_lemma=sorted((W > THR).sum(1).tolist(), reverse=True), **vals))  # fmt: skip
    W0 = fits[(vname, 0)]
    WB0 = fits[("B", 0)]
    for s in range(5):
        perm = match(fits[(vname, s)], W0)
        rows[-5 + s]["dev_vs_seed0"] = float(np.abs(fits[(vname, s)] - W0[perm]).max())
        perm = match(fits[(vname, s)], WB0)
        rows[-5 + s]["dev_vs_B0"] = float(np.abs(fits[(vname, s)] - WB0[perm]).max())
    print(f"{vname} done", flush=True)

df = pd.DataFrame(rows)
df.to_csv(HERE / "cubesat2.csv", index=False)
pd.set_option("display.width", 300)
pd.set_option("display.max_colwidth", 200)
cols = [
    "variant",
    "seed",
    "conv",
    "n_iter",
    "time",
    "O0",
    "O1",
    "T",
    "T0",
    "O2",
    "O3",
    "O4",
    "shares",
    "n_lemma",
    "dev_vs_seed0",
    "dev_vs_B0",
]
print(df[cols].round(4).to_string(index=False))
print("\ncontending sets (exponent > 0.05), per variant and seed:")
for vname, _, _ in VARIANTS:
    d = df[df.variant == vname]
    print(f"\n[{vname}] distinct signatures: {d.sets.nunique()} of 5")
    for _, r in d.iterrows():
        print(f"  seed {r.seed}: {r.sets}")
summ = df.groupby("variant", sort=False).agg(
    O0_mean=("O0", "mean"), O0_sd=("O0", "std"), T_mean=("T", "mean"), O3_mean=("O3", "mean"),
    dev_max=("dev_vs_seed0", "max"), dev_vs_B0_max=("dev_vs_B0", "max"), conv=("conv", "sum"),
    iters=("n_iter", "mean"), time=("time", "mean"), signatures=("sets", "nunique"),
)  # fmt: skip
print("\nsummary:\n" + summ.round(4).to_string())

print(
    "\nrestart selection among the 5 B fits (seeds 0..4 as restarts): which seed each objective picks"
)
dB = df[df.variant == "B"].set_index("seed")
for name in ["O0", "O1", "T", "T0", "O2", "O3", "O4", "O5"]:
    v = dB[name]
    pick = int(v.idxmin() if MINIMIZE[name] else v.idxmax())
    print(f"  {name}: seed {pick} (value {v[pick]:.4f}; values {v.round(4).tolist()})")
