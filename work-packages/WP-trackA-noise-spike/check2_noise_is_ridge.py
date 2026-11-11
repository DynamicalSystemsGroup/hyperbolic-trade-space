"""Spike A, check 2: is independent log-noise on the metrics, at the level of the fit, a ridge on w?

Claim A2 (population level, L6 applied row by row): when the weights p of the soft maximum spread over many
rows, E_noise[J_tau^noisy(w)] ~= J_tau(w) + tau sigma^2 ||w||^2 / 2. So the noisy fit minimises the clean J
plus a ridge, and to first order the exponent bias is  delta = - sigma^2 (P C P)^+ P w,  C = Cov_p(u)
(p = softmax(tau U w) at the clean fit; the tau cancels because the Hessian is tau C).
Compares, on planted frontier data (d = 4, w* = (.4,.3,.2,.1)), the exponents of
  clean fit | noisy fit (the package) | ridge-objective minimiser (clean U) | first-order prediction.
Run: uv run python work-packages/WP-trackA-noise-spike/check2_noise_is_ridge.py
"""

import numpy as np
from scipy.optimize import minimize

from hyperbolic_trade_space import HyperbolicTradeSpace
from hyperbolic_trade_space.datasets import make_frontier_data
from hyperbolic_trade_space.solvers import objective_and_grad

W = np.array([0.4, 0.3, 0.2, 0.1])


def minimise(U, tau, ridge_coeff=0.0, w0=None):
    d = U.shape[1]

    def f(w):
        j, g = objective_and_grad(w, U, tau)
        return j + ridge_coeff * w @ w / 2, g + ridge_coeff * w

    r = minimize(f, np.full(d, 1 / d) if w0 is None else w0, jac=True, method="SLSQP",
                 bounds=[(0, 1)] * d, constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
                 options={"ftol": 1e-14, "maxiter": 500})
    return r.x


def first_order(U, w, tau):
    z = tau * (U @ w)
    p = np.exp(z - z.max())
    p /= p.sum()
    mu = U.T @ p
    C = (U - mu).T @ ((U - mu) * p[:, None])
    d = len(w)
    P = np.eye(d) - np.ones((d, d)) / d
    return -(np.linalg.pinv(P @ C @ P)) @ P @ w, 1.0 / (p**2).sum()  # (per unit sigma^2, n_eff)


if __name__ == "__main__":
    N = 20000
    print("N =", N, " planted w =", W)
    for sigma in (0.05, 0.10, 0.20):
        for tau in (5.0, 20.0, 50.0):
            X, info = make_frontier_data(N, 4, exponents=W, frontier_fraction=0.3, random_state=0)
            rng = np.random.default_rng(1)
            Xn = X * np.exp(sigma * rng.standard_normal(X.shape))
            U = np.log(X)
            w_clean = HyperbolicTradeSpace(temperature=tau).fit(X).exponents_
            w_noisy = HyperbolicTradeSpace(temperature=tau).fit(Xn).exponents_
            w_ridge = minimise(U, tau, tau * sigma**2)
            w_mine = minimise(U, tau)
            d1, neff = first_order(U, w_mine, tau)
            d1 = sigma**2 * d1
            e = lambda a, b: np.abs(a - b).max()
            print(f"sigma={sigma:.2f} tau={tau:4.0f} n_eff={neff:7.0f} | noisy-clean {e(w_noisy, w_clean):.4f} "
                  f"| ridge-clean {e(w_ridge, w_clean):.4f} | noisy-ridge {e(w_noisy, w_ridge):.4f} "
                  f"| 1st-order-vs-ridge {e(w_clean + d1, w_ridge):.4f} | pkg-vs-mine(clean) {e(w_mine, w_clean):.4f}")
