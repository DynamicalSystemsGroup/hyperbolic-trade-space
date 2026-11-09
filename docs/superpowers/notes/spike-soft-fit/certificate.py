"""Spike: a certificate of local optimality for the soft fit (throwaway).

The soft objective F_kappa(W) = -mean_i (1/kappa) log sum_k exp(kappa x_ik), x_ik = w_k.u_i - J_tau(U w_k),
is smooth for finite tau and kappa, so the second-order sufficient condition applies on the product
of simplices. With alpha_ik = softmax_k(kappa x_ik), p_k the support weights of facet k,
utilde_k = sum_i p_ki u_i, C_k = Cov_{p_k}(u), v_ik = u_i - utilde_k, n_k = sum_i alpha_ik:

  gradient   g_k  = (n_k/N) (utilde_k - ubar_k^alpha)                     (the weighted refit gradient)
  Hessian    H    = D - kappa M
             D    = blockdiag((n_k/N) tau C_k)                >= 0        (each term's convex refit)
             d'Md = mean_i Var_{k ~ alpha_i}(v_ik . d_k)      >= 0        (the ambiguity of the designs)

Certificate: weighted gaps within tolerance (first order) and H positive definite on the tangent
space of the active face (second order) => W is a strict local minimizer of F_kappa.

    cd <a clean checkout> && uv run python docs/superpowers/notes/spike-soft-fit/certificate.py
"""

import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.linalg import block_diag, eigh, null_space
from scipy.special import softmax

sys.path.insert(0, str(Path(__file__).parent))
import soft_fit as SF  # noqa: E402
from hyperbolic_trade_space import make_frontier_data  # noqa: E402
from hyperbolic_trade_space import solvers as S  # noqa: E402

warnings.filterwarnings("ignore")
rng = np.random.default_rng(0)


def parts(U, W, tau, kappa):
    N, d = U.shape
    K = W.shape[0]
    P = np.array([S.support_weights(U @ w, tau) for w in W])          # K x N
    ut = P @ U                                                          # K x d
    X = U @ W.T - np.array([S.log_mean_exp(U @ w, tau) for w in W])
    A = softmax(kappa * X, axis=1)
    n = A.sum(0)
    g = (n[:, None] / N) * (ut - (A.T @ U) / n[:, None])
    Dk = [(n[k] / N) * tau * ((U.T * P[k]) @ U - np.outer(ut[k], ut[k])) for k in range(K)]
    V = U[:, None, :] - ut[None, :, :]                                  # N x K x d
    M = np.zeros((K * d, K * d))
    for k in range(K):
        for l in range(K):
            wgt = A[:, k] * ((k == l) - A[:, l])
            M[k * d:(k + 1) * d, l * d:(l + 1) * d] = (V[:, k, :].T * wgt) @ V[:, l, :] / N
    return g, block_diag(*Dk), M, A, X


def grad_only(U, W, tau, kappa):
    return parts(U, W, tau, kappa)[0]


def tangent_basis(W, g, tol=1e-6, eps=1e-7):
    """Orthonormal basis of the tangent space of the face: per term, free coordinates summing to zero.
    A coordinate at its bound whose multiplier is not strictly positive is kept free (conservative)."""
    K, d = W.shape
    blocks = []
    for k in range(K):
        mu = float(W[k] @ g[k])
        free = (W[k] > tol) | (g[k] - mu <= eps)
        E = np.eye(d)[:, free]
        B = E @ null_space(np.ones((1, int(free.sum()))))               # d x (free - 1)
        blocks.append(B)
    return block_diag(*blocks)


def certificate(U, W, tau, kappa):
    g, D, M, A, X = parts(U, W, tau, kappa)
    gap = max(float(W[k] @ g[k] - g[k].min()) for k in range(W.shape[0]))  # first-order gap on each simplex
    B = tangent_basis(W, g)
    if B.shape[1] == 0:
        return gap, np.inf, np.inf, 0.0, B
    H = B.T @ (D - kappa * M) @ B
    return gap, float(eigh(H, eigvals_only=True)[0]), float(eigh(B.T @ D @ B, eigvals_only=True)[0]), float(eigh(kappa * B.T @ M @ B, eigvals_only=True)[-1]), B


def polish(U, W, tau, kappa, steps=30):
    """Newton steps on the active face (the joint analogue of the package's facet polish): the reduced
    Hessian is the one the certificate tests, so the first-order gap is driven to rounding."""
    W = W.copy()
    for _ in range(steps):
        g, D, M, _, _ = parts(U, W, tau, kappa)
        B = tangent_basis(W, g)
        if B.shape[1] == 0:
            break
        Hr, gr = B.T @ (D - kappa * M) @ B, B.T @ g.ravel()
        if np.abs(gr).max() < 1e-13 or eigh(Hr, eigvals_only=True)[0] <= 0:
            break
        step, t, f0 = (B @ np.linalg.solve(Hr, gr)).reshape(W.shape), 1.0, SF.slack(U, W, tau, kappa)
        while t > 1e-6 and ((W - t * step < 0).any() or SF.slack(U, W - t * step, tau, kappa) > f0 + 1e-15):
            t /= 2
        if t <= 1e-6:
            break
        W = W - t * step
    return W


def radius(U, lam, tau, kappa):
    """A valid, crude radius: the Hessian moves by at most L3 per unit step, L3 from the data's diameter."""
    R = float(np.max(np.linalg.norm(U[:, None] - U[None], axis=-1))) if len(U) <= 1500 else float(np.linalg.norm(U.max(0) - U.min(0)))
    c = 1.0 / (6.0 * np.sqrt(3.0))
    return lam / (R**3 * (c * tau**2 + 0.375 * kappa * tau + 8 * c * kappa**2)), R


def perturb_test(U, W, tau, kappa, B, n=400, step=1e-3):
    """Does F rise in every sampled feasible direction? (a sanity check of what the certificate asserts)"""
    f0, worst = SF.slack(U, W, tau, kappa), np.inf
    for _ in range(n):
        dvec = (B @ rng.normal(size=B.shape[1])).reshape(W.shape)
        dvec /= np.linalg.norm(dvec)
        W2 = W + step * dvec
        if (W2 < 0).any():
            continue
        worst = min(worst, SF.slack(U, W2, tau, kappa) - f0)
    return worst


print("=== 1. the Hessian formula against finite differences of the gradient (table A, at the soft fit) ===")
X, info = make_frontier_data(900, 3, n_terms=3, random_state=11)
U, tau = np.log(X), 50.0
(W, _, _), _ = SF.fit(U, 3, tau, tau)
g, D, M, A, _ = parts(U, W, tau, tau)
H = D - tau * M
err = 0.0
for _ in range(20):
    dv = rng.normal(size=W.shape); dv -= dv.mean(1, keepdims=True); dv /= np.linalg.norm(dv)
    h = 1e-6
    fd = (grad_only(U, W + h * dv, tau, tau) - grad_only(U, W - h * dv, tau, tau)).ravel() / (2 * h)
    err = max(err, float(np.abs(fd - H @ dv.ravel()).max() / np.abs(H @ dv.ravel()).max()))
print("largest relative error over 20 tangent directions:", f"{err:.1e}", "| D and M positive semidefinite: min eigenvalues",
      f"{eigh(D, eigvals_only=True)[0]:.1e}", f"{eigh(M, eigvals_only=True)[0]:.1e}")

print("\n=== 2. the certificate at fitted points, and at a point that is stationary but not a minimum ===")
print("where | kappa | first-order gap | min curvature of H | of D alone | largest ambiguity term | certified | F rises in all sampled directions (smallest rise) | crude radius")
for name, (N, d, seed) in {"table A": (900, 3, 11), "table B": (400, 4, 0)}.items():
    X, info = make_frontier_data(N, d, n_terms=3, random_state=seed)
    U = np.log(X)
    for kappa in (tau, 4 * tau):
        (W, _, _), _ = SF.fit(U, 3, tau, kappa)
        W = polish(U, W, tau, kappa)
        gap, lam, lamD, amb, B = certificate(U, W, tau, kappa)
        r, R = radius(U, lam, tau, kappa)
        print(f"{name}, soft fit | {kappa:.0f} | {gap:.1e} | {lam:.4f} | {lamD:.4f} | {amb:.4f} | {gap < 1e-8 and lam > 0} | {perturb_test(U, W, tau, kappa, B):.2e} | {r:.1e}")
    one = S._newton_polish(U - U.mean(0), S.solve_slsqp(U - U.mean(0), tau, tol=1e-13).w, tau, 0.0)
    Wc = np.tile(one, (3, 1))
    for kappa in (2.0, tau):
        gap, lam, lamD, amb, B = certificate(U, Wc, tau, kappa)
        print(f"{name}, all terms equal (the one-term answer) | {kappa:.0f} | {gap:.1e} | {lam:.4f} | {lamD:.4f} | {amb:.4f} | {gap < 1e-8 and lam > 0} | {perturb_test(U, Wc, tau, kappa, B):.2e} | -")
    # the sharpness at which the all-equal point stops being a minimum: smallest kappa with min eig (D - kappa M) = 0
    g, D, M, A, _ = parts(U, Wc, tau, 1.0)
    B = tangent_basis(Wc, g)
    Dr, Mr = B.T @ D @ B, B.T @ M @ B
    kc = 1.0 / eigh(Mr, Dr, eigvals_only=True)[-1]
    print(f"{name}: the all-equal point is a minimum below kappa = {kc:.2f} and a saddle above it (tau = {tau:.0f})")

print("\n=== 3. the benchmark: twenty planted tables, tau = 50, soft fit at kappa = tau ===")
cert = rec = both = 0
lams = []
for s in range(20):
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    (W, _, _), _ = SF.fit(U, 3, tau, tau)
    W = polish(U, W, tau, tau)
    gap, lam, lamD, amb, B = certificate(U, W, tau, tau)
    ok = gap < 1e-8 and lam > 0
    r = SF.recovered(U, W, tau, info)[0]
    cert += ok; rec += r; both += ok and r; lams.append(lam)
print(f"certified {cert} of 20 | recovered {rec} of 20 | both {both} | min curvature: smallest {min(lams):.4f}, median {np.median(lams):.4f}")

print("\n=== 4. the hard certificate as the limit: at the package's one-label fit, the soft Hessian as kappa grows (table A) ===")
X, info = make_frontier_data(900, 3, n_terms=3, random_state=11)
U = np.log(X)
(Wh, _, _), _ = SF.fit(U, 3, tau, np.inf)
Xs = np.sort(SF.scores(U, Wh, tau), axis=1)
print("assignment margin of the one-label fit (smallest gap between a design's two best facets):", f"{float((Xs[:, -1] - Xs[:, -2]).min()):.2e}")
for kappa in (tau, 4 * tau, 16 * tau, 64 * tau, 256 * tau):
    gap, lam, lamD, amb, B = certificate(U, Wh, tau, kappa)
    print(f"kappa = {kappa:>7.0f} | gap {gap:.1e} | min curvature of H {lam:.4f} | of D alone {lamD:.4f} | largest ambiguity term {amb:.4f}")

if len(sys.argv) > 1:
    print("\n=== 5. the cubesat fits at kappa = tau ===")
    sys.path.insert(0, "examples/adcs")
    import case as C  # noqa: E402
    for regime in C.CUBESAT.regimes:
        st = C.load_study(regime)
        for K in (2, 3):
            ft = C.fit_study(st, K=K)
            U, tau_c = np.log(st.M), ft.tau
            (W0, _, _), _ = SF.fit(U, K, tau_c, tau_c)
            W = polish(U, W0, tau_c, tau_c)
            moved = float(np.abs(W - W0).max())
            gap, lam, lamD, amb, B = certificate(U, W, tau_c, tau_c)
            free = [int((W[k] > 1e-6).sum()) for k in range(K)]
            print(f"{regime}, K = {K}, tau = {tau_c:.1f} | gap {gap:.1e} | min curvature {lam:.5f} | of D alone {lamD:.5f} | ambiguity {amb:.5f} | free exponents per facet {free}"
                  f" | certified {gap < 1e-8 and lam > 0} | smallest rise in sampled directions {perturb_test(U, W, tau_c, tau_c, B, step=1e-4):.2e} | polish moved exponents by {moved:.1e}")
