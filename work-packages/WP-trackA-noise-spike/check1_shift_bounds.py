"""Spike A, check 1: how far does the soft maximum's noise shift follow L6, and what bounds it?

Scores s_i (clean), noise z_i ~ N(0, v^2) i.i.d. with v = sigma * ||w|| (the weighted noise of L6).
Shift = E[LME_tau(s + z)] - LME_tau(s), by Monte Carlo over noise draws, rows fixed.
Candidate claim (A1): 0-side bounds  mean(s) - LME(s) <= shift <= min( tau v^2 / 2 , E max z ),
with E max z <= v sqrt(2 log N).  Reports how often each branch is the active one.
Run: uv run python work-packages/WP-trackA-noise-spike/check1_shift_bounds.py
"""

import numpy as np
from scipy.special import logsumexp


def lme(x, tau):
    return (logsumexp(tau * x, axis=-1) - np.log(x.shape[-1])) / tau


def run(case, N, v, tau, reps, rng):
    s = np.zeros(N) if case == "on-surface" else -rng.exponential(1.0, N)
    z = v * rng.standard_normal((reps, N))
    shift = lme(s + z, tau).mean() - lme(s, tau)
    emax = z.max(axis=1).mean()
    return shift, tau * v**2 / 2, emax, v * np.sqrt(2 * np.log(N)), np.mean(s) - lme(s, tau)


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    print(f"{'case':11s} {'N':>6s} {'v':>5s} {'tau':>6s} {'shift':>8s} {'L6':>8s} {'Emax z':>8s} "
          f"{'vsqrt2lnN':>9s} {'lower':>8s}  ok  active")
    bad = 0
    for case in ("on-surface", "interior"):
        for N in (100, 1000, 10000):
            for v in (0.05, 0.2):
                for tau in (1, 5, 20, 50, 200):
                    reps = 400 if N <= 1000 else 100
                    sh, l6, em, emb, lo = run(case, N, v, tau, reps, rng)
                    ok = (sh <= l6 + 3e-3) and (sh <= em + 3e-3) and (sh >= lo - 3e-3) and em <= emb
                    bad += not ok
                    act = "L6" if l6 <= em else "max"
                    print(f"{case:11s} {N:6d} {v:5.2f} {tau:6d} {sh:8.4f} {l6:8.4f} {em:8.4f} "
                          f"{emb:9.4f} {lo:8.4f}  {'y' if ok else 'N'}   {act}")
    print("violations:", bad)
