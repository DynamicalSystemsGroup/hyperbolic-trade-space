"""The models of the WP43 spike (protocol.md): the package's fits and the log-quadratic term.

Every model has ``log_v(U)`` for ``U = log m`` of shape (n, d); ``log V > 0`` is beyond the surface.
"""

from __future__ import annotations

import sys
import time
import warnings
from pathlib import Path

import numpy as np
from scipy.special import logsumexp

ROOT = Path(__file__).resolve().parents[3]
for p in (ROOT / "src", ROOT / "examples" / "adcs"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from hyperbolic_trade_space import HyperbolicTradeSpace, select_temperature  # noqa: E402
from hyperbolic_trade_space.coordinates import helmert_basis  # noqa: E402

TARGET = 0.10
BOUNDS = (3.0, 1e3)
TOL = 0.01
MAX_HALVINGS = 12
EPS = 1e-9


def lme(f, tau):
    """Log-mean-exp soft maximum of ``f`` at ``tau`` (the maximum at ``inf``)."""
    f = np.asarray(f, float)
    if np.isinf(tau):
        return float(f.max())
    return float(logsumexp(tau * f) / tau - np.log(len(f)) / tau)


class QuadModel:
    """``log V = w.u + (1/2) u'Qu - beta``, ``Q = B'SB``, ``S`` PSD; ``quad=False`` gives ``Q = 0``.

    Fitted by minimising ``LME_tau(f(u_i)) - mean_i f(u_i)`` (the exact maximum at ``tau = inf``)
    over ``w`` on the simplex and ``S`` positive semidefinite: a convex program in ``(w, S)``.
    """

    def __init__(self, quad=True, solver="CLARABEL", monotone=False):
        self.quad = quad
        self.monotone = monotone
        self.solver = solver

    def _f(self, U):
        z = U @ self.B.T
        f = U @ self.w
        if self.quad:
            f = f + 0.5 * np.einsum("ij,jk,ik->i", z, self.S, z)
        return f

    def fit(self, U, tau):
        import cvxpy as cp

        n, d = U.shape
        self.B = helmert_basis(d)
        z = U @ self.B.T
        w = cp.Variable(d, nonneg=True)
        f = U @ w
        S = None
        if self.quad:
            S = cp.Variable((d - 1, d - 1), PSD=True)
            f = f + 0.5 * cp.sum(cp.multiply(z @ S, z), axis=1)
        top = cp.max(f) if np.isinf(tau) else cp.log_sum_exp(tau * f) / tau - np.log(n) / tau
        cons = [cp.sum(w) == 1]
        if (
            self.monotone and S is not None
        ):  # every partial derivative w + Qu >= 0 at the training rows
            cons.append(w[None, :] + (z @ S) @ self.B >= 0)
        prob = cp.Problem(cp.Minimize(top - cp.sum(f) / n), cons)
        self.status = None
        for solver in (self.solver, "SCS"):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    prob.solve(solver=solver)
            except cp.error.SolverError:
                continue
            self.status, self.solver_used = prob.status, solver
            if prob.status in ("optimal", "optimal_inaccurate") and w.value is not None:
                break
        if w.value is None:
            raise RuntimeError(f"cvxpy returned no solution (status {self.status})")
        self.w = np.maximum(w.value, 0.0)
        self.w /= self.w.sum()
        self.S = np.zeros((d - 1, d - 1)) if S is None else 0.5 * (S.value + S.value.T)
        self.tau = float(tau)
        self.beta = lme(self._f(U), tau)
        self.ok = self.status in ("optimal", "optimal_inaccurate")
        return self

    def log_v(self, U):
        return self._f(U) - self.beta

    def grad_negative_fraction(self, U):
        """Fraction of rows where some metric's partial derivative of ``f`` is negative."""
        z = U @ self.B.T
        g = self.w[None, :] + (z @ self.S) @ self.B
        return float((g < -1e-9).any(axis=1).mean())


class PackageModel:
    """The package's estimator at a given ``K`` (sharp, or soft with ``kappa = tau``)."""

    def __init__(self, n_terms, soft=False):
        self.n_terms, self.soft = n_terms, soft

    def fit(self, M, tau):
        kw = dict(temperature=tau, n_terms=self.n_terms, random_state=0)
        if self.soft:
            kw.update(term_temperature=tau, term_aggregation="mean")
        self.est = HyperbolicTradeSpace(**kw).fit(M)
        self.tau = float(tau)
        self.ok = True
        self.status = getattr(self.est.termination_, "status", "")
        return self

    def log_v(self, U):
        return self.est.score_samples(np.exp(U))


def band_of(tau):
    return 1.0 / tau if np.isfinite(tau) else 0.1


def frac_above(model, U):
    return float((model.log_v(U) > EPS).mean())


def select_quad(U, quad, monotone=False):
    """Bisection of ``log tau`` to a training fraction above of ``TARGET`` (the protocol's)."""
    lo, hi = np.log(BOUNDS[0]), np.log(BOUNDS[1])
    best = None
    for _ in range(MAX_HALVINGS):
        mid = 0.5 * (lo + hi)
        m = QuadModel(quad, monotone=monotone).fit(U, float(np.exp(mid)))
        fa = frac_above(m, U)
        if best is None or abs(fa - TARGET) < abs(best[0] - TARGET):
            best = (fa, float(np.exp(mid)), m)
        if abs(fa - TARGET) <= TOL:
            break
        if fa > TARGET:
            lo = mid  # too many above: harder maximum
        else:
            hi = mid
    return best[1], best[2]


def fit_model(name, M, tau_hint=None, sharp=False, k2_tau=None):
    """Select tau (or take ``inf``) and fit; returns ``(model, tau, flag, t_select, t_fit)``.

    ``name`` in K1, K1c, K2, K3, K2s, LQ. ``tau_hint`` is the full-table tau of the model, used when
    the package cannot bracket the target; ``k2_tau`` is K2's tau of the same fold (for K2s).
    """
    U = np.log(M)
    flag, t_sel = "", 0.0
    if name == "LQm":
        t0 = time.perf_counter()
        tau, m = select_quad(U, True, monotone=True)
        t_sel = time.perf_counter() - t0
        t0 = time.perf_counter()
        m = QuadModel(True, monotone=True).fit(U, tau)
        return m, tau, flag, t_sel, time.perf_counter() - t0
    if name in ("K1c", "LQ"):
        if sharp:
            t0 = time.perf_counter()
            m = QuadModel(name == "LQ").fit(U, np.inf)
            return m, np.inf, flag, 0.0, time.perf_counter() - t0
        t0 = time.perf_counter()
        tau, m = select_quad(U, name == "LQ")
        t_sel = time.perf_counter() - t0
        t0 = time.perf_counter()
        m = QuadModel(name == "LQ").fit(U, tau)
        return m, tau, flag, t_sel, time.perf_counter() - t0
    K = {"K1": 1, "K2": 2, "K3": 3, "K2s": 2}[name]
    if sharp:
        tau = np.inf
    elif name == "K2s":
        tau = k2_tau
    else:
        t0 = time.perf_counter()
        try:
            tau = float(select_temperature(M, TARGET, bounds=BOUNDS, n_terms=K, random_state=0))
        except ValueError:
            tau, flag = tau_hint, "tau_from_full_table"
        t_sel = time.perf_counter() - t0
    t0 = time.perf_counter()
    m = PackageModel(K, soft=name == "K2s").fit(M, tau)
    return m, float(tau), flag, t_sel, time.perf_counter() - t0
