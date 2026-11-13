"""Numeric checks of the mathematics in task item 1 (run from repo root).

1. step B's refit == argmin f_k(w) = J_tau(Uw) - ubar_k.w on the simplex, beta_k = J_tau(Uw_k)
2. mean slack == sum_k (|C_k|/N) f_k(w_k)
3. G_k == 0 at an exact optimum (interior and boundary), G >= f - f* on random points, and
   G_k == 0 iff E-2's KKT (g_j >= lambda, w_j (g_j - lambda) = 0, lambda = w^T g)
4. tau = inf: G with LP duals == LP duality gap; uniform-on-ties p gives a valid but looser bound
5. min_exponent floor version of the gap
"""

import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from certificates import facet_gap, facet_objective, lp_gap_uniform_ties, simplex_gap  # noqa: E402

from hyperbolic_trade_space.datasets import make_frontier_data  # noqa: E402
from hyperbolic_trade_space.solvers import (  # noqa: E402
    _refit,
    log_mean_exp,
    objective_and_grad,
    solve_lp,
    solve_slsqp,
    solve_terms,
    support_weights,
)

rng = np.random.default_rng(0)
X, info = make_frontier_data(400, 4, n_terms=3, random_state=0)
U = np.log(X)
N, d = U.shape
kw = {"min_exponent": 0.0, "penalty": None, "alpha": 0.0, "tol": 1e-10, "max_iter": 500}

print("== 1. step B is argmin f_k; beta_k = J_tau(U w_k)")
for tau in (np.inf, 50.0):
    labels = info["facet"] if "facet" in info else np.argmax(U @ info["exponents"].T, 1)
    labels = np.asarray(labels)
    W, beta, obj = _refit(U, labels, np.full((3, d), 0.25), np.zeros(3), tau, kw)
    for k in range(3):
        ubar = U[labels == k].mean(0)
        f_B = facet_objective(U, W[k], ubar, tau)
        # independent minimization of f_k on a fine random sample of the simplex + SLSQP from 10 starts
        best = f_B
        for _ in range(10):
            w0 = rng.dirichlet(np.ones(d))
            r = solve_slsqp(U - ubar, tau, w0=w0, tol=1e-12)
            best = min(best, facet_objective(U, r.w, ubar, tau))
        G, g, p = facet_gap(U, W[k], ubar, tau)
        print(f"  tau={tau:>5} k={k} f_B={f_B:.10f} best_restart={best:.10f} "
              f"f_B-best={f_B - best:+.2e}  G_k={G:.2e}  |beta-J|={abs(beta[k] - log_mean_exp(U @ W[k], tau)):.1e}")

print("\n== 2. mean slack == sum_k (|C_k|/N) f_k(w_k)")
for tau in (np.inf, 50.0):
    r = solve_terms(U, 3, tau, random_state=0)
    F = sum((r.labels == k).mean() * facet_objective(U, r.W[k], U[r.labels == k].mean(0), tau)
            for k in range(3) if (r.labels == k).any())
    print(f"  tau={tau:>5} objective={r.objective:.12f} sum_k share*f_k={F:.12f} diff={r.objective - F:+.1e}  msg={r.message!r}")

print("\n== 3. gap properties at finite tau (facet 0 of seed 0, tau = 50)")
tau = 50.0
ubar = U[np.asarray(info['facet']) == 0].mean(0) if 'facet' in info else U[:100].mean(0)
Uc = U - ubar
r = solve_slsqp(Uc, tau, tol=1e-14, max_iter=2000)
w_star = r.w
f_star = facet_objective(U, w_star, ubar, tau)
G_star, g_star, _ = facet_gap(U, w_star, ubar, tau)
lam = g_star @ w_star
print(f"  w*={w_star.round(6)}  G(w*)={G_star:.2e}  f*={f_star:.10f}")
print(f"  E-2 KKT at w*: g - lambda = {(g_star - lam).round(8)}  (>= 0 up to tol; = 0 where w_j > 0)")
viol = 0
for _ in range(2000):
    w = rng.dirichlet(np.ones(d) * rng.uniform(0.2, 3))
    G, g, _ = facet_gap(U, w, ubar, tau)
    f = facet_objective(U, w, ubar, tau)
    if not (f - f_star >= -1e-12 and f - f_star <= G + 1e-12):
        viol += 1
print(f"  random simplex points: violations of 0 <= f - f* <= G : {viol} / 2000")
# a boundary optimum: force one metric useless by making its column huge negative (never contends)
U2 = U.copy(); U2[:, 3] -= 5.0
ubar2 = U2[:100].mean(0)
r2 = solve_slsqp(U2 - ubar2, tau, tol=1e-14, max_iter=2000)
G2, g2, _ = facet_gap(U2, r2.w, ubar2, tau)
lam2 = g2 @ r2.w
print(f"  boundary case: w*={r2.w.round(6)}  G={G2:.2e}  g - lambda={(g2 - lam2).round(6)}  (inactive j has g_j > lambda)")

print("\n== 4. tau = inf: G with LP duals vs LP duality gap vs uniform-on-ties p")
for k in range(3):
    lab = np.asarray(info['facet']) if 'facet' in info else np.argmax(U @ info["exponents"].T, 1)
    ubar = U[lab == k].mean(0)
    Uc = U - ubar
    lp = solve_lp(Uc)
    w = lp.w
    primal = np.max(Uc @ w)
    dual = np.min(Uc.T @ lp.p)
    G_lp, g, p = facet_gap(U, w, ubar, np.inf, p=lp.p)
    G_uni = lp_gap_uniform_ties(U, w, ubar)
    # perturb w slightly off the optimum: gaps become positive; compare with f - f*
    w_pert = np.clip(w + 1e-3 * rng.standard_normal(d), 0, None); w_pert /= w_pert.sum()
    f_pert = facet_objective(U, w_pert, ubar, np.inf)
    G_pert_lp, _, _ = facet_gap(U, w_pert, ubar, np.inf)  # re-solves LP at w_pert's centre (same ubar) -> duals of the optimum, not of w_pert
    G_pert_uni = lp_gap_uniform_ties(U, w_pert, ubar)
    print(f"  k={k} primal-dual gap={primal - dual:.2e}  G(LP duals)={G_lp:.2e}  G(uniform ties)={G_uni:.2e}  "
          f"| perturbed: f-f*={f_pert - primal:.2e}  G_uni={G_pert_uni:.2e}  (valid bound: {G_pert_uni >= f_pert - primal - 1e-12})")

print("\n== 5. min_exponent floor: gap vanishes at the floored optimum")
m = 0.05
lab = np.asarray(info['facet']) if 'facet' in info else np.argmax(U @ info["exponents"].T, 1)
ubar = U[lab == 0].mean(0)
r = solve_slsqp(U - ubar, 50.0, min_exponent=m, tol=1e-14, max_iter=2000)
G_m, g, _ = facet_gap(U, r.w, ubar, 50.0, min_exponent=m)
G_0 = simplex_gap(g, r.w, 0.0)
print(f"  w*={r.w.round(6)} (floor {m})  G(floor)={G_m:.2e}  G(no floor, wrong feasible set)={G_0:.2e}")
