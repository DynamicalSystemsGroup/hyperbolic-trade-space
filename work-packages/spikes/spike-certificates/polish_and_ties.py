"""(a) finite-tau polish: can G_k be driven below 1e-8 cheaply after the built SLSQP?
(b) tau = inf ties: which rows tie on seeds 1, 3, 16 and what fires the guard in the 9 restarts.
Run from the repo root:  uv run python <folder>/polish_and_ties.py"""

import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from sklearn.utils import check_random_state

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from certificates import assignment_margin, facet_gap, facet_objective  # noqa: E402

from hyperbolic_trade_space.datasets import make_frontier_data  # noqa: E402
from hyperbolic_trade_space.solvers import (  # noqa: E402
    _refit,
    _simplex_min,
    _solve_terms_once,
    objective_and_grad,
    solve_slsqp,
    solve_terms,
    support_weights,
)


def newton_polish(U, w, ubar, tau, n_steps=5, active_tol=1e-10):
    """Reduced Newton steps on the active set with the simplex equality (throwaway)."""
    w = w.copy()
    for _ in range(n_steps):
        s = U @ w
        p = support_weights(s, tau)
        g = U.T @ p - ubar
        act = w > active_tol
        Ua = U[:, act]
        H = tau * (Ua.T @ (p[:, None] * Ua) - np.outer(Ua.T @ p, Ua.T @ p))
        na = act.sum()
        KKT = np.block([[H, np.ones((na, 1))], [np.ones((1, na)), np.zeros((1, 1))]])
        rhs = np.concatenate([-g[act], [0.0]])
        try:
            sol = np.linalg.lstsq(KKT, rhs, rcond=None)[0]
        except np.linalg.LinAlgError:
            break
        step = np.zeros_like(w)
        step[act] = sol[:na]
        # backtrack to stay feasible and decrease f
        t = 1.0
        f0 = facet_objective(U, w, ubar, tau)
        while t > 1e-6:
            w1 = w + t * step
            if (w1 >= 0).all() and facet_objective(U, w1, ubar, tau) <= f0 + 1e-15:
                break
            t *= 0.5
        else:
            break
        w = w1 / w1.sum()
    return w


print("== (a) polish at tau = 50, facets of the chosen fit, seeds 0..19")
tau = 50.0
tot = {"built": [], "ftol1e-14": [], "ftol1e-16+2000": [], "newton": []}
times = {k: 0.0 for k in tot}
fdrop = []
for s in range(20):
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    res = solve_terms(U, 3, tau, random_state=0)
    for k in range(3):
        rows = res.labels == k
        ubar = U[rows].mean(0)
        w = res.W[k]
        G0, _, _ = facet_gap(U, w, ubar, tau)
        tot["built"].append(G0)
        t0 = time.time()
        r = _simplex_min(objective_and_grad, w, (U - ubar, tau), 0.0, 1e-14, 500)
        w1 = np.clip(r.x, 0, None); w1 /= w1.sum()
        times["ftol1e-14"] += time.time() - t0
        tot["ftol1e-14"].append(facet_gap(U, w1, ubar, tau)[0])
        t0 = time.time()
        r = _simplex_min(objective_and_grad, w, (U - ubar, tau), 0.0, 1e-16, 2000)
        w2 = np.clip(r.x, 0, None); w2 /= w2.sum()
        times["ftol1e-16+2000"] += time.time() - t0
        tot["ftol1e-16+2000"].append(facet_gap(U, w2, ubar, tau)[0])
        t0 = time.time()
        w3 = newton_polish(U, w, ubar, tau)
        times["newton"] += time.time() - t0
        G3 = facet_gap(U, w3, ubar, tau)[0]
        tot["newton"].append(G3)
        fdrop.append(facet_objective(U, w, ubar, tau) - facet_objective(U, w3, ubar, tau))
for k, v in tot.items():
    v = np.array(v)
    print(f"  {k:16s} G_k: median={np.median(v):.1e} max={v.max():.1e}  <=1e-6: {(v <= 1e-6).sum()}/60  "
          f"<=1e-8: {(v <= 1e-8).sum()}/60  <=1e-10: {(v <= 1e-10).sum()}/60  time {times[k]:.2f}s / 60 facets")
fd = np.array(fdrop)
print(f"  f_k decrease achieved by the Newton polish: median={np.median(fd):.1e} max={fd.max():.1e} "
      f"(the built SLSQP point was within this of the exact optimum)")

print("\n== (b) tau = inf ties on seeds 1, 3, 16 (chosen fit)")
for s in (1, 3, 16, 0):
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    res = solve_terms(U, 3, np.inf, random_state=0)
    gamma, radius, lab, i = assignment_margin(U, res.W, res.beta)
    S = U @ res.W.T - res.beta
    order = np.argsort(-S[i])
    slack = res.beta - U @ res.W.T  # (N, K)
    n_touch = (np.abs(slack) < 1e-9).sum(0)
    shared = ((np.abs(slack) < 1e-9).sum(1) >= 2).sum()
    on_front = bool(info["frontier_mask"][i]) if "frontier_mask" in info else "?"
    print(f"  seed {s:2d}: gamma={gamma:.1e}; tied row i={i} frontier_row={on_front} planted facet={info['facet'][i]}; "
          f"tying facets {order[:2].tolist()} scores {S[i][order[:2]].round(12).tolist()}; "
          f"rows touching each facet plane {n_touch.tolist()}; rows touching >= 2 planes: {shared}")

print("\n== (b') guard stops at tau = inf: what happened in the 9 restarts")
kw = {"min_exponent": 0.0, "penalty": None, "alpha": 0.0, "tol": 1e-10, "max_iter": 500}
seeds5 = check_random_state(0).randint(0, 2**31 - 1, size=5)
n = 0
for s in range(20):
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    for j, sd in enumerate(seeds5):
        r = _solve_terms_once(U, 3, np.inf, sd, 50, kw)
        if r.message != "no further decrease":
            continue
        n += 1
        # replay the rejected step
        new = np.argmax(U @ r.W.T - r.beta, axis=1)
        W2, b2, obj2 = _refit(U, new, r.W, r.beta, np.inf, kw)
        gamma, _, _, _ = assignment_margin(U, r.W, r.beta)
        changed = (new != r.labels).sum()
        print(f"  seed {s:2d} restart {j}: obj={r.objective:.9f} rejected obj2={obj2:.9f} increase={obj2 - r.objective:+.2e} "
              f"rows reassigned={changed} gamma(returned)={gamma:.1e} it={r.n_iter}")
print(f"  {n} guard stops found")
