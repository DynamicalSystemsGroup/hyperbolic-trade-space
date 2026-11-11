"""Spike A, check 3: relative noise injected into the cubesat attributes of record, then conditioned and refitted.

The cubesat data of record are deterministic simulator output (no noise in the data). To see what a noise
level does, multiply each raw attribute by exp(delta * eps), eps ~ N(0,1) (a relative measurement error of
size delta, the same for every attribute), condition again (the analyst's step: log, orient, standardise), and
refit at the clean fit's temperature. Reports, over reps: the largest exponent change, the contending-set
overlap (exponents > 1e-3), the offset shift against the L6 value with the conditioned per-metric noise
(sigma_j = delta / s_j, s_j the log standard deviation of the conditioned column's raw log) and the
isotropic reading (A5, one sigma = the mean sigma_j).
Run: uv run python work-packages/WP-trackA-noise-spike/check3_cubesat_noise_injection.py
"""

import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "examples" / "adcs"))
import case  # noqa: E402

from hyperbolic_trade_space import HyperbolicTradeSpace  # noqa: E402

REPS = 8


def log_std(study):
    """s_j: the log standard deviation of each raw attribute on the feasible designs (the scaler's unit)."""
    return np.array([np.log(study.feasible[a].to_numpy(float)).std() for a in study.attrs])


if __name__ == "__main__":
    for regime in ("primary", "stock"):
        study = case.load_study(regime)
        fit = case.fit_study(study)
        tau = fit.tau
        w0 = np.ravel(fit.estimator.exponents_)
        off0 = float(fit.estimator.log_offset_[0])
        s = log_std(study)
        print(f"\n== {regime}: N={study.M.shape[0]} tau={tau:.2f}")
        print("attributes:", list(study.attrs))
        print("log spread s_j of the raw attribute:", np.round(s, 3))
        print("clean exponents:", np.round(w0, 3), " participants:", [a for a, x in zip(study.attrs, w0) if x > 1e-3])
        for delta in (0.005, 0.02, 0.05, 0.10):
            sig = delta / s
            l6_diag = tau * float((w0**2) @ (sig**2)) / 2
            l6_iso = tau * float(sig.mean() ** 2 * (w0 @ w0)) / 2
            dw, ov, dsh = [], [], []
            for r in range(REPS):
                rng = np.random.default_rng(100 + r)
                noisy = study.feasible.copy()
                for a in study.attrs:
                    noisy[a] = noisy[a].to_numpy(float) * np.exp(delta * rng.standard_normal(len(noisy)))
                _, Mn = case._condition(noisy, study.attrs, study.spec)
                e = HyperbolicTradeSpace(temperature=tau).fit(Mn)
                wn = np.ravel(e.exponents_)
                dw.append(np.abs(wn - w0).max())
                a0, a1 = set(np.flatnonzero(w0 > 1e-3)), set(np.flatnonzero(wn > 1e-3))
                ov.append(len(a0 & a1) / len(a0 | a1))
                dsh.append(float(e.log_offset_[0]) - off0)
            print(f"delta={delta:5.3f}  sigma_j range {sig.min():.3f}..{sig.max():.3f}  max|dw| {np.mean(dw):.3f}  "
                  f"contending-set Jaccard {np.mean(ov):.2f}  offset shift {np.mean(dsh):.3f}  "
                  f"L6 (diag Sigma) {l6_diag:.3f}  L6 (isotropic, mean sigma) {l6_iso:.3f}")
