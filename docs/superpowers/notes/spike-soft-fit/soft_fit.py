"""Spike: fitting the several-term model with a weight on every term for every design (throwaway).

The package's loop (solvers._solve_terms_once) with one change: where it gives each design the
label of its dominant facet, this gives it the weights softmax_k(kappa * score_ik). kappa = inf is
the package's loop. Everything else is the package's own code: the start, the refit of a facet as
a supporting hyperplane over all rows centred at the facet's (weighted) mean, the polish, the cap.

    cd <a clean checkout> && uv run python docs/superpowers/notes/spike-soft-fit/soft_fit.py planted
    cd <a clean checkout> && uv run python docs/superpowers/notes/spike-soft-fit/soft_fit.py case
"""

import sys
import time
import warnings

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.special import logsumexp, softmax
from sklearn.utils import check_random_state

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
from hyperbolic_trade_space import solvers as S
from hyperbolic_trade_space.coordinates import helmert_basis

warnings.filterwarnings("ignore")
KW = dict(min_exponent=0.0, tol=1e-10, max_iter=500, penalty=None, alpha=0.0)


def scores(U, W, tau):
    return U @ W.T - np.array([S.log_mean_exp(U @ w, tau) for w in W])


def slack(U, W, tau, kappa=np.inf):
    X = scores(U, W, tau)
    return float(-(X.max(1) if np.isinf(kappa) else logsumexp(kappa * X, axis=1) / kappa).mean())


def refit(U, A, W, tau):
    W = W.copy()
    for k in range(W.shape[0]):
        nk = A[:, k].sum()
        if nk < 1e-9:
            continue
        Uc = U - (A[:, k] @ U) / nk
        w = S.solve_slsqp(Uc, tau, **KW).w
        if np.isfinite(tau):
            w = S._newton_polish(Uc, w, tau, 0.0)
        W[k] = w
    return W


def weights(U, W, tau, kappa):
    X = scores(U, W, tau)
    return np.eye(W.shape[0])[X.argmax(1)] if np.isinf(kappa) else softmax(kappa * X, axis=1)


def fit_once(U, K, tau, kappa, seed, max_iter=50, then_hard=False):
    N, d = U.shape
    Z = U @ helmert_basis(d).T
    centers = Z[check_random_state(seed).choice(N, K, replace=False)]
    lab = np.argmin(((Z[:, None] - centers) ** 2).sum(-1), axis=1)
    W = refit(U, np.eye(K)[lab], np.full((K, d), 1.0 / d), tau)
    hist, n = [slack(U, W, tau, kappa)], 0
    while n < max_iter:
        n += 1
        A = weights(U, W, tau, kappa)
        W2 = refit(U, A, W, tau)
        f2 = slack(U, W2, tau, kappa)
        if f2 > hist[-1] + 1e-9:          # the package's guard
            break
        W = W2
        hist.append(f2)
        if hist[-2] - hist[-1] < 1e-10:
            break
    mono = bool((np.diff(hist) <= 1e-9).all())
    if then_hard:                          # finish with the package's own hard steps from this start
        for _ in range(max_iter):
            A = weights(U, W, tau, np.inf)
            W2 = refit(U, A, W, tau)
            if slack(U, W2, tau) > slack(U, W, tau) - 1e-12:
                break
            W, n = W2, n + 1
    return W, n, mono


def fit(U, K, tau, kappa, n_restarts=5, then_hard=False):
    runs = [fit_once(U, K, tau, kappa, s, then_hard=then_hard) for s in range(n_restarts)]
    key = (lambda r: slack(U, r[0], tau)) if then_hard else (lambda r: slack(U, r[0], tau, kappa))
    return min(runs, key=key), runs


def match(W, T):
    c = np.abs(W[:, None, :] - T[None, :, :]).sum(-1)
    r, col = linear_sum_assignment(c)
    return float(np.abs(W[r] - T[col]).max()), dict(zip(r, col))


def recovered(U, W, tau, info):
    err, m = match(W, np.asarray(info["exponents"]))
    lab = np.array([m[k] for k in scores(U, W, tau).argmax(1)])
    fm = np.asarray(info["frontier_mask"], bool)
    agree = float((lab[fm] == np.asarray(info["facet"])[fm]).mean())
    return err < 0.05 and agree >= 0.9, err, agree


def planted():
    default_tau = float(HyperbolicTradeSpace().temperature)
    taus = (default_tau, 50.0, np.inf) if len(sys.argv) < 3 else (float(sys.argv[2]),)
    for tau in taus:
        print(f"\n=== planted: make_frontier_data(400, 4, n_terms=3, random_state=0..19), tau = {tau} ===")
        print("variant | recovered of 20 (5 starts) | single starts recovered of 100 | mean exponent error | mean steps | all runs monotone | seconds per fit")
        tables = [make_frontier_data(400, 4, n_terms=3, random_state=s) for s in range(20)]
        ref = 0
        for X, info in tables:
            est = HyperbolicTradeSpace(n_terms=3, temperature=tau, random_state=0).fit(X)
            ref += recovered(np.log(X), est.exponents_, tau, info)[0]
        print(f"the package's estimator (reference) | {ref}")
        for label, kappa, th in [("one label (kappa = inf)", np.inf, False), ("soft, kappa = 10", 10.0, False), ("soft, kappa = 20", 20.0, False),
                                 ("soft, kappa = 50", 50.0, False), ("soft, kappa = 200", 200.0, False), ("soft kappa = 20, then one label", 20.0, True),
                                 ("soft, kappa = tau", tau, False)]:
            ok = single = 0; errs = []; steps = []; mono = True; t0 = time.perf_counter()
            for X, info in tables:
                U = np.log(X)
                (W, n, m), runs = fit(U, 3, tau, kappa, then_hard=th)
                r = recovered(U, W, tau, info)
                ok += r[0]; errs.append(r[1])
                for Wr, nr, mr in runs:
                    single += recovered(U, Wr, tau, info)[0]; steps.append(nr); mono &= mr
            print(f"{label} | {ok} | {single} | {np.mean(errs):.4f} | {np.mean(steps):.1f} | {mono} | {(time.perf_counter() - t0) / 20:.2f}")


def case():
    sys.path.insert(0, "examples/adcs")
    import case as C  # noqa: E402

    for regime in C.CUBESAT.regimes:
        st = C.load_study(regime)
        for K in (2, 3):
            ft = C.fit_study(st, K=K)
            U, tau, hard = np.log(st.M), ft.tau, ft.estimator
            Wh = hard.exponents_
            print(f"\n=== cubesat, regime {regime}, K = {K}, tau = {tau:.2f}, {U.shape[0]} designs x {U.shape[1]} metrics ===")
            print("package: mean slack", round(slack(U, Wh, tau), 5), "| leading metric per facet", [st.names[j] for j in Wh.argmax(1)])
            for kappa, th in [(np.inf, False), (20.0, False), (50.0, False), (tau / 2, False), (tau, False), (20.0, True)]:
                (W, n, mono), _ = fit(U, K, tau, kappa, then_hard=th)
                err, m = match(W, Wh)
                sets_same = all(set(np.flatnonzero(W[a] > 0.05)) == set(np.flatnonzero(Wh[b] > 0.05)) for a, b in m.items())
                lead_same = all(W[a].argmax() == Wh[b].argmax() for a, b in m.items())
                lab = np.array([m[k] for k in scores(U, W, tau).argmax(1)])
                agree = float((lab == scores(U, Wh, tau).argmax(1)).mean())
                tag = f"kappa = {kappa:.1f}" + (" (tau)" if kappa == tau else " (tau / 2)" if kappa == tau / 2 else "") + (", then one label" if th else "")
                print(f"  {tag:<34} | F_inf {slack(U, W, tau):.5f} | max exponent diff from package {err:.4f} | contending sets (w > 0.05) same: {sets_same}"
                      f" | leading metrics same: {lead_same} | dominant facet agrees on {agree:.3f} of designs | steps {n} | monotone {mono}")


if __name__ == "__main__":
    {"planted": planted, "case": case}[sys.argv[1]]()
