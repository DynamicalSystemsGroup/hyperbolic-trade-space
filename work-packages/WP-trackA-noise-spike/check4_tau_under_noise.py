"""Spike A, check 4: exponent error of the fit against the planted exponents, as the temperature varies, under noise.

Planted d = 4, w* = (.4,.3,.2,.1), 30% of rows on the surface, i.i.d. log-noise sigma on every metric added
to the rows (frontier and interior). Median over seeds of max_j |w_j - w*_j|, for tau and N.
Candidate claim (A4): under noise the error is U-shaped in tau (small tau: soft maximum tends to the mean,
bias; large tau: tends to the maximum of noisy scores, variance), with the minimum moving up with N.
Run: uv run python work-packages/WP-trackA-noise-spike/check4_tau_under_noise.py
"""

import numpy as np

from hyperbolic_trade_space import HyperbolicTradeSpace
from hyperbolic_trade_space.datasets import make_frontier_data

W = np.array([0.4, 0.3, 0.2, 0.1])
TAUS = (1.0, 3.0, 10.0, 30.0, 100.0, 300.0, np.inf)

if __name__ == "__main__":
    print("median over 15 seeds of max exponent error; columns tau =", TAUS)
    for sigma in (0.05, 0.15):
        for N in (200, 2000, 20000):
            errs = {t: [] for t in TAUS}
            for seed in range(15):
                X, _ = make_frontier_data(N, 4, exponents=W, frontier_fraction=0.3, random_state=seed)
                rng = np.random.default_rng(1000 + seed)
                Xn = X * np.exp(sigma * rng.standard_normal(X.shape))
                for t in TAUS:
                    w = np.ravel(HyperbolicTradeSpace(temperature=t).fit(Xn).exponents_)
                    errs[t].append(np.abs(w - W).max())
            print(f"sigma={sigma:.2f} N={N:6d} | " + "  ".join(f"{np.median(errs[t]):.3f}" for t in TAUS))
