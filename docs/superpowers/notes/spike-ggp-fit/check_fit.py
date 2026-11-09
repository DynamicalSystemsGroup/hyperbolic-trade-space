"""Spike: the model, the fit and the analysis of the several-term case, kept apart (throwaway).

Questions (the supervisor, 2026-11-09): does a design need a unique facet in the FIT, or only in
the ANALYSIS? Is the several-term fit a generalized geometric program (GGP)?

    cd <a clean checkout> && uv run python docs/superpowers/notes/spike-ggp-fit/check_fit.py

Notation. u_i: log metrics of design i. Facet k: exponents w_k on the simplex and the offset
beta_k = J_tau(U w_k), the log-mean-exp over ALL designs (as in solvers._refit). Score
x_ik = w_k . u_i - beta_k (minus the slack of design i under facet k). Model:
Phi_kappa(u_i) = (1/kappa) log sum_k exp(kappa x_ik), the maximum over k at kappa = inf.
Objective of the fit: the mean slack F_kappa(W) = -mean_i Phi_kappa(u_i).
"""

import itertools

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.special import logsumexp, softmax

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
from hyperbolic_trade_space import solvers as S

TAU = 50.0
rng = np.random.default_rng(0)


def betas(U, W):
    return np.array([S.log_mean_exp(U @ w, TAU) for w in W])


def scores(U, W):
    return U @ W.T - betas(U, W)


def F(U, W, kappa=np.inf):
    X = scores(U, W)
    return float(-(X.max(1) if np.isinf(kappa) else logsumexp(kappa * X, axis=1) / kappa).mean())


def match(W, T):
    c = np.abs(W[:, None, :] - T[None, :, :]).sum(-1)
    r, col = linear_sum_assignment(c)
    return float(np.abs(W[r] - T[col]).max()), col


def G(U, W, A):
    """The fixed-weight objective: sum_k (n_k/N) [J_tau(U w_k) - ubar_k . w_k], weights A (N x K)."""
    n = A.sum(0)
    ub = (A.T @ U) / n[:, None]
    return float(sum(n[k] / len(U) * (S.log_mean_exp(U @ W[k], TAU) - ub[k] @ W[k]) for k in range(W.shape[0])))


def refit(U, A, W0):
    W = W0.copy()
    for k in range(W.shape[0]):
        nk = A[:, k].sum()
        if nk > 1e-9:
            W[k] = S.solve_slsqp(U - (A[:, k] @ U) / nk, TAU, w0=W0[k], tol=1e-13, max_iter=2000).w
    return W


def soft_fit(U, K, kappa, seed, iters=300):
    """Majorize-minimize on F_kappa: weights = softmax_k(kappa x_ik), then one convex refit per term."""
    N, d = U.shape
    c = U[np.random.default_rng(seed).choice(N, K, replace=False)]
    Zc = U - U.mean(1, keepdims=True)
    lab = np.argmin(((Zc[:, None] - (c - c.mean(1, keepdims=True))[None]) ** 2).sum(-1), axis=1)
    W = refit(U, np.eye(K)[lab], np.full((K, d), 1.0 / d))
    hist = [F(U, W, kappa)]
    for _ in range(iters):
        A = np.eye(K)[scores(U, W).argmax(1)] if np.isinf(kappa) else softmax(kappa * scores(U, W), axis=1)
        W = refit(U, A, W)
        hist.append(F(U, W, kappa))
        if abs(hist[-2] - hist[-1]) < 1e-12:
            break
    return W, np.array(hist)


for name, (N, d, K, seed) in {"table A (900 x 3, the figures)": (900, 3, 3, 11), "table B (400 x 4, the package's test table)": (400, 4, 3, 0)}.items():
    X, info = make_frontier_data(N, d, n_terms=K, random_state=seed)
    U = np.log(X)
    T = np.asarray(info["exponents"])
    ts = HyperbolicTradeSpace(n_terms=K, temperature=TAU, random_state=0).fit(X)
    W, lab = ts.exponents_, ts.facet_
    print(f"\n=== {name} ===")
    print("fitted exponents vs planted: max error", round(match(W, T)[0], 4), "| mean slack F =", round(F(U, W), 5))

    # ---- 1. every design constrains every facet
    Xs = scores(U, W)
    b_all, b_own = betas(U, W), np.array([S.log_mean_exp(U[lab == k] @ W[k], TAU) for k in range(K)])
    P = np.array([S.support_weights(U @ W[k], TAU) for k in range(K)])
    foreign = [float(P[k][lab != k].sum()) for k in range(K)]
    print("1. offsets use all designs: |beta_code - J_tau(all rows)| =", f"{np.abs(ts.log_offset_.ravel() - b_all).max():.1e}",
          "| J_tau(own rows) differs by", np.round(b_all - b_own, 4).tolist())
    print("   share of each facet's support weight carried by designs whose dominant facet is another:", np.round(foreign, 3).tolist())
    print("   every design has a slack under every facet: largest score over all (i, k) =", round(float(Xs.max()), 4),
          "| designs within 0.05 of two or more facets:", int(((-Xs) < 0.05).sum(1).__ge__(2).sum()), "of", N)

    # ---- 2. is the fit, as posed, convex in the log variables (W, with beta tied or free)?
    worst = 0.0
    for a, b in itertools.combinations(range(K), 2):
        Wp = W.copy(); Wp[[a, b]] = W[[b, a]]                 # the same model, two terms renamed
        mid = (W + Wp) / 2                                     # the midpoint in the log variables
        worst = max(worst, F(U, mid) - F(U, W))
        for kap in (5.0, 20.0, 100.0):
            worst = max(worst, F(U, mid, kap) - (F(U, W, kap) + F(U, Wp, kap)) / 2)
    Wbar = np.tile(W.mean(0), (K, 1))
    one = S.solve_slsqp(U - U.mean(0), TAU, tol=1e-13).w
    print("2. midpoint of the fit and its renamed copy: F rises by up to", round(worst, 5), "(a convex objective cannot rise)")
    print("   F at: the fit", round(F(U, W), 5), "| all terms equal to their mean", round(F(U, Wbar), 5),
          "| the best single term", round(F(U, np.tile(one, (K, 1))), 5))

    # ---- 3. with the weights fixed, the refit of all terms is one convex program, a GGP in x = exp(w)
    A = softmax(20.0 * Xs, axis=1)
    viol = 0
    for _ in range(2000):
        Wa, Wb = rng.dirichlet(np.ones(d), K), rng.dirichlet(np.ones(d), K)
        viol += G(U, (Wa + Wb) / 2, A) > (G(U, Wa, A) + G(U, Wb, A)) / 2 + 1e-12
    n = A.sum(0); ub = (A.T @ U) / n[:, None]
    x = np.exp(W)                                              # GP variables
    gp = np.prod([(np.mean(np.prod(x[k] ** (TAU * U), axis=1)) ** (1 / TAU) * np.prod(x[k] ** (-ub[k]))) ** (n[k] / N) for k in range(K)])
    maj = 0.0
    for _ in range(500):                                       # the bound F_kappa <= G_A - entropy term, tight at the anchor
        Wr = rng.dirichlet(np.ones(d), K)
        Hm = float(-(A * np.log(np.clip(A, 1e-300, None))).sum(1).mean()) / 20.0
        maj = max(maj, F(U, Wr, 20.0) - (G(U, Wr, A) - Hm))
    Hm = float(-(A * np.log(np.clip(A, 1e-300, None))).sum(1).mean()) / 20.0
    print("3. fixed weights: midpoint-convexity violations in 2000 random pairs:", int(viol),
          "| exp(objective) vs product of powers of posynomials in x: relative gap", f"{abs(gp - np.exp(G(U, W, A))) / gp:.1e}")
    print("   the fixed-weight program bounds the fit from above: largest F - bound over 500 random W =", f"{maj:.1e}",
          "| at the anchor F - bound =", f"{F(U, W, 20.0) - (G(U, W, A) - Hm):.1e}")

    # ---- 4. a fit in which no design has a unique facet (weights = softmax), against the hard one
    print("4. fit by soft weights (best of 8 starts), kappa | max error vs planted | F_inf | monotone | designs with largest weight < 0.9 | steps")
    for kap in (5.0, 20.0, 50.0, 200.0, np.inf):
        best = None
        for s in range(8):
            Wk, h = soft_fit(U, K, kap, s)
            mono = bool((np.diff(h) <= 1e-9).all())
            if best is None or h[-1] < best[1][-1]:
                best = (Wk, h, mono)
        Wk, h, mono = best
        A2 = np.eye(K)[scores(U, Wk).argmax(1)] if np.isinf(kap) else softmax(kap * scores(U, Wk), axis=1)
        print(f"   {kap:>6} | {match(Wk, T)[0]:.4f} | {F(U, Wk):.5f} | {mono} | {int((A2.max(1) < 0.9).sum())} of {N} | {len(h) - 1}")

    # ---- 5. aside: one term, the level beta against the mean slack beta - w . ubar
    wJ = S.solve_slsqp(U, TAU, tol=1e-13).w
    print("5. one term: argmin of the level J_tau and argmin of the mean slack differ by", round(float(np.abs(wJ - one).max()), 4),
          "| spread of the mean log metrics:", round(float(np.ptp(U.mean(0))), 3))
