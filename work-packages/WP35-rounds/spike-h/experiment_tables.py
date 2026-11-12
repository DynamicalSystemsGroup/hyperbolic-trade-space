"""Step 1 (repository environment): the experiment's tables and this work's fits.

    uv run python work-packages/WP35-rounds/spike-h/experiment_tables.py \
        <tables.npz> <earlier tables.npz>

Arms A, B, C are generated here from fixed seeds (see hypothesis.md); arm D is read from the earlier
spike's tables (log-metrics and planted exponents) and refit. For every table the file holds the
log-metrics ("logM"), the target vectors ("w", one row per planted term), this work's fitted
exponent rows ("fit") and the empirical spread along the first target and along the largest
orthogonal direction ("sd").
"""

import sys
import warnings

import numpy as np
from scipy.optimize import linear_sum_assignment

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

D, N = 4, 300
SEEDS = range(100, 106)
RHO_A = [4.0, 2.0, 1.0, 0.5, 0.25]
T_B = [0.0, 0.3, 0.6, 0.9]
RHO_C = [2.0, 0.5]
SD_G, SD_OTHER, FRONTIER_FRACTION = 1.0, 0.3, 0.3
SD_LOGV_PER_M = (
    0.954  # sd of log V per unit m: mixture of 30 percent at 0 and 70 percent at -Exp(m)
)


def draw_w(rng):
    while True:
        w = rng.dirichlet(np.ones(D))
        if w.min() >= 0.05:
            return w


def basis_orthogonal(w, rng):
    """Orthonormal rows spanning the space orthogonal to w; the first is the nuisance g."""
    A = np.column_stack([w / np.linalg.norm(w), rng.standard_normal((D, D - 1))])
    Q, _ = np.linalg.qr(A)
    return Q[:, 1:].T


def table_A(seed, rho, edge=True):
    """Edge in the plane w.u = 0 (edge=True) or a symmetric cloud with no edge (edge=False)."""
    rng = np.random.default_rng(seed)
    w = draw_w(rng)
    G = basis_orthogonal(w, rng)
    uhat = w / np.linalg.norm(w)
    if edge:
        m = rho * np.linalg.norm(w) / SD_LOGV_PER_M
        on_edge = rng.random(N) < FRONTIER_FRACTION
        logv = np.where(on_edge, 0.0, -rng.exponential(m, N))
        a = logv / np.linalg.norm(w)
    else:
        a = rho * rng.standard_normal(N)
    xi = rng.standard_normal((N, D - 1)) * np.array([SD_G, SD_OTHER, SD_OTHER])
    return a[:, None] * uhat + xi @ G, w


def spread(U, w):
    uhat = w / np.linalg.norm(w)
    along = float((U @ uhat).std())
    P = np.eye(D) - np.outer(uhat, uhat)
    ev = np.linalg.eigvalsh(np.cov((U @ P).T))
    return [along, float(np.sqrt(ev[-1]))]


def fit_exponents(U, K=1):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        est = HyperbolicTradeSpace(n_terms=K, temperature=50.0, random_state=0).fit(np.exp(U))
    return np.atleast_2d(est.exponents_)


def main(out, earlier):
    tab = {}

    def add(name, U, W, K=1):
        W = np.atleast_2d(W)
        tab[f"{name}/logM"], tab[f"{name}/w"] = U, W
        tab[f"{name}/fit"] = fit_exponents(U, K)
        tab[f"{name}/sd"] = np.array(spread(U, W[0]))
        print(name, U.shape, np.round(tab[f"{name}/sd"], 3), flush=True)

    for rho in RHO_A:
        for s in SEEDS:
            U, w = table_A(s, rho)
            add(f"A/rho{rho}/s{s}", U, w)
    for t in T_B:
        wt = (1 - t) * np.full(D, 1 / D) + t * np.array([1.0, 0, 0, 0])
        for s in SEEDS:
            X, _info = make_frontier_data(N, D, exponents=wt, random_state=s)
            add(f"B/t{t}/s{s}", np.log(X), wt)
    for rho in RHO_C:
        for s in SEEDS:
            U, w = table_A(s, rho, edge=False)
            add(f"C/rho{rho}/s{s}", U, w)
    E = np.load(earlier, allow_pickle=True)
    for name, K in [
        ("planted_K1_s0", 1),
        ("planted_K2_s7", 2),
        ("planted_K3_s0", 3),
        ("planted_K3_s4", 3),
    ]:
        U, W = E[f"{name}/logM"], np.atleast_2d(E[f"{name}/planted"])
        fit = fit_exponents(U, K)
        # match each planted term to a distinct fitted term by largest cosine (favours this work)
        c = (W / np.linalg.norm(W, axis=1, keepdims=True)) @ (
            fit / np.linalg.norm(fit, axis=1, keepdims=True)
        ).T
        r, cidx = linear_sum_assignment(-c)
        tab[f"D/{name}/logM"], tab[f"D/{name}/w"] = U, W
        tab[f"D/{name}/fit"] = fit[cidx[np.argsort(r)]]
        tab[f"D/{name}/sd"] = np.array(spread(U, W[0]))
        print("D", name, np.round(tab[f"D/{name}/sd"], 3), flush=True)
    np.savez(out, **tab)


if __name__ == "__main__":
    main(*sys.argv[1:3])
