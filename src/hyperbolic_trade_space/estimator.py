"""The ``HyperbolicTradeSpace`` estimator: a monomial (K = 1) frontier in a log-ratio chart.

The model is ``V(m) = prod_j m_j^{w_j} e^{-beta}`` with ``w`` on the simplex;
the fit minimizes the log-mean-exp objective ``J_tau``; the chart ``(Z, log V)`` is a linear
bijection of log space. Mathematics: see the documentation site.
"""

from __future__ import annotations

import numbers
import warnings

import numpy as np
from scipy.special import logsumexp
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import ConvergenceWarning
from sklearn.utils import check_random_state
from sklearn.utils.validation import check_array, check_is_fitted, check_non_negative, validate_data

from . import coordinates as _coords
from . import solvers as _solvers
from .solvers import EPS_FEAS, EPS_KKT, GUARD_TOL, POLISH_STEPS

__all__ = [
    "EPS_FEAS",
    "EPS_KKT",
    "EPS_ZERO_EXPONENT",
    "GUARD_TOL",
    "PARTICIPATION_THRESHOLD",
    "POLISH_STEPS",
    "HyperbolicTradeSpace",
]

_ABOVE_TOL = 1e-9  # V > 1 + tol counts as "above the frontier" at tau = inf
EPS_ZERO_EXPONENT = 1e-12  # an exponent at or below this is numerically zero: 0 * log 0 := 0
PARTICIPATION_THRESHOLD = 1e-3  # exponents above this participate (tension_report's threshold)
_WARN_STATUSES = ("guard_stop", "uncertified")  # "iteration_cap" warns on its own rule, see fit


class HyperbolicTradeSpace(TransformerMixin, BaseEstimator):
    """Posynomial invariant form: learn the shape of a design trade space (K monomial facets).

    Fits ``V(m) = prod_j m_j^{w_j} / e^{beta}`` to strictly positive, larger-is-better metrics so
    that ``V <= 1`` is the attainable region and ``V = 1`` the frontier, by minimizing the
    entropic soft maximum of ``w . log m`` over the simplex. The transform is the invertible chart
    ``[Z | log V]`` (log-ratio coordinates along the frontier, and the depth below it).

    Parameters
    ----------
    temperature : float, default=10.0
        Softness ``tau`` of the soft maximum, ``tau > 0`` or ``np.inf`` (an exact LP). Units are
        1 / (log-spread of the metrics), so condition the metrics first; useful range 3 to 100.
    min_exponent : float, default=0.0
        Lower bound on each exponent, in ``[0, 1/d)``.
    coordinates : {"ilr", "alr"}, default="ilr"
        Chart basis: Helmert (orthonormal rows) or additive log-ratio
        (invertible, not orthonormal; last metric is the reference).
    n_terms : int, default=1
        Number of monomial facets ``K`` (``K > 1`` is the posynomial frontier, fitted by
        ``solve_terms``; ``K = 1`` is the monomial fit).
    term_temperature : float, default=np.inf
        Softness ``kappa`` of ``Phi_K(u) = (1/kappa) log sum_k exp(kappa (w_k . u - beta_k))``,
        ``kappa > 0`` or ``np.inf`` (the exact maximum). Used for ``n_terms > 1`` only. The
        offsets ``beta_k`` are the supports, so ``max_k x_k <= Phi_K <= max_k x_k + log K / kappa``;
        the gap is disclosed, not renormalized. A finite ``kappa`` also selects the *soft fit*
        (with ``facet_step="support"``): every design carries the weights
        ``softmax_k(kappa x_k)`` on every term, the refit of term ``k`` is the supporting
        hyperplane centred at the weighted mean of the designs, and the fit minimizes the mean slack
        of the model it reports, ``-mean_i Phi_K(u_i)``. At the default ``np.inf`` every design has
        the label of its dominant term, as before. Read ``kappa`` on the scale of ``temperature``:
        a ``kappa`` far below it merges facets. ``facet_step="tangent"`` ignores ``kappa`` in the
        fit.
    term_aggregation : {"sum", "mean"}, default="sum"
        How the K terms are aggregated when ``term_temperature`` is finite. ``"sum"`` (the default)
        is the unnormalized log-sum-exp above, with ``max <= Phi_K <= max + log K / kappa``; a
        duplicated term lowers the slack by ``log 2 / kappa`` without new geometry. ``"mean"`` is
        the normalized log-mean-exp, ``Phi_K - log K / kappa``, with
        ``max - log K / kappa <= Phi_K <= max``, the same convention as ``temperature``.
        The two differ by the constant ``log K / kappa``: the soft weights, the Hessian, the
        certificate and the fitted terms are the same, ``score_samples`` and the slack shift by
        exactly that constant. No effect at ``term_temperature = inf`` or ``n_terms = 1``.
        Validated in ``fit``.
    tol : float, default=1e-10
        Solver tolerance (SLSQP ``ftol``); also the threshold of the iteration-cap warning
        (see ``max_iter``).
    max_iter : int, default=500
        Maximum SLSQP iterations of each term's fit. The ``n_terms > 1`` alternation has its
        own cap (50 partition-and-refit rounds, ``solve_terms``'s ``max_iter``). Reaching it
        means the assignment step was still moving rows, possibly cycling among rows that tie
        between terms while every term is already stationary on its rows. The fit is kept, with
        status ``"iteration_cap"`` and its gap in ``termination_``; ``fit`` warns only when
        that gap or the last change of the objective exceeds ``tol``.
    penalty : {None, "reweighted_l1"}, default=None
        Sparsity option for the exponents (see ``solve_slsqp``); acts at finite ``temperature``.
    alpha : float, default=0.0
        Penalty weight, ``alpha >= 0``; 0 leaves the fit unchanged.
    random_state : int, RandomState instance or None, default=None
        Seed for the facet initializations (``n_terms > 1`` only).
    n_restarts : int, default=5
        Number of seeded initializations of the ``n_terms > 1`` alternation; the lowest mean
        slack is kept. More restarts help against local optima (see the limitations page).
    facet_step : {"support", "tangent"}, default="support"
        Per-facet step of the ``n_terms > 1`` alternation (see
        ``solve_terms``): ``"support"`` is the supporting
        hyperplane tightest on the facet's rows, which keeps the mean slack monotone;
        ``"tangent"`` fits the near-frontier rows' tangent plane, which is not monotone. No effect
        for ``n_terms = 1``.

    Attributes
    ----------
    exponents_ : ndarray of shape (n_terms, n_features_in_)
        Fitted exponents ``w_k`` on the simplex.
    log_offset_ : ndarray of shape (n_terms,)
        The offsets ``beta_k = J_tau(w_k)`` (for ``n_terms > 1`` over all rows: each facet is a
        supporting hyperplane).
    support_weights_ : ndarray of shape (n_samples,)
        Softmax weights ``p`` at the solution (LP duals at ``tau = inf``); zero for rows with a
        zero metric. For ``n_terms > 1`` each facet's weights on its own rows, scaled by its row
        share (sum 1).
    n_eff_ : float
        Effective number of supporting rows, ``1 / sum p_i^2``.
    frac_above_ : float
        Fraction of (non-degenerate) training rows with ``V > 1``.
    objective_ : float
        What the solver minimized: ``J_tau(w)`` at the solution (equals ``beta``, a soft maximum)
        for ``n_terms = 1``; for ``n_terms > 1`` the mean slack
        ``(1/N) sum_i (beta_k(i) - w_k(i) . u_i)`` of the partition fit, or, for the soft fit
        (finite ``term_temperature``), the mean slack ``-mean_i Phi_K(u_i)`` of the soft model.
        The two are different quantities: to compare fits across ``n_terms`` use ``mean_slack_``.
    mean_slack_ : float
        The mean slack ``mean_i (beta_k(i) - w_k(i) . u_i)`` over the rows with no zero metric,
        with ``k(i)`` the row's facet (``facet_``); defined for every ``n_terms``. At
        ``n_terms = 1`` it is ``beta - mean_i (w . u_i)``. At a fixed ``temperature`` it is
        comparable across ``n_terms`` (and across restarts); ``objective_`` is not. With a finite
        ``term_temperature`` and ``n_terms > 1`` it is the slack of the reported model,
        ``-mean_i Phi_K(u_i)``.
    n_iter_ : int
        Solver iterations (at least 1; 1 on the LP-only path).
    basis_ : ndarray of shape (n_features_in_ - 1, n_features_in_)
        Chart matrix ``B`` (``Z = log(X) @ B.T``). For ``n_terms > 1`` the shape is
        ``(n_terms, n_features_in_ - 1, n_features_in_)``: the chart does not depend on ``w``, so
        the same ``B`` is stacked ``K`` times and ``Z`` is the same for every facet.
    facet_ : ndarray of int, shape (n_samples,)
        ``argmax_k (w_k . u - beta_k)`` of each training row (``-1`` for a zero metric); all
        zeros at ``n_terms = 1``. The dominant term: an analysis of the fitted model, also for the
        soft fit, which uses weights on every term.
    coefficients_ : ndarray of shape (n_terms,)
        Posynomial coefficients ``exp(-kappa beta_k)`` of
        ``exp(kappa Phi_K) = sum_k c_k prod_j m_j^(kappa w_kj)``; at ``kappa = inf`` the
        convention ``kappa = 1`` gives ``exp(-beta_k)``.
    facet_share_ : ndarray of shape (n_terms,)
        Share of the near-frontier training rows (``|log V| < band``,
        ``band = 1 / temperature``, or 0.1 at ``tau = inf``) assigned to each facet; zeros if
        there are none; ``[1.0]`` at ``n_terms = 1``.
    training_log_v_ : ndarray of shape (n_samples,)
        ``log V`` of the training rows (``-inf`` for rows with a zero metric on a participating
        exponent; a zero metric on an exponent at or below ``EPS_ZERO_EXPONENT`` contributes
        nothing, see Notes).
    termination_ : Termination
        Stopping record of the chosen run: ``status`` (``"certified"``,
        ``"stationary_without_margin"``, ``"stationary"``, ``"uncertified"``, ``"guard_stop"``,
        ``"iteration_cap"`` or ``"not_applicable"``), the first-order gaps, the assignment margin
        and radius, the Corollary bound and the tolerances (``EPS_KKT``, ``EPS_FEAS``,
        ``GUARD_TOL``). Level 3 (conditional local optimality) is for ``n_terms > 1`` with
        ``facet_step="support"`` and no penalty; ``n_terms = 1`` and the degenerate shortcuts
        record ``"not_applicable"`` with the gap of the fitted objective, read only. For the soft
        fit (finite ``term_temperature``, finite ``temperature``) ``"certified"`` means the
        facet gaps are within ``EPS_KKT`` and the Hessian of the soft objective is positive
        definite on the tangent space of the active face (a strict local minimizer of the soft
        objective); ``"stationary"`` means the gaps hold and the curvature is not positive;
        ``min_curvature`` is the smallest curvature (``nan`` otherwise); the margin, radius and
        bound are ``nan``. A soft fit at ``temperature = inf`` is ``"not_applicable"``.
    conditioning_ : ndarray of shape (n_terms,)
        Smallest eigenvalue of the Hessian of ``J_tau`` at each facet's fit,
        ``tau (U^T diag(p) U - (U^T p)(U^T p)^T)`` with ``p`` the softmax weights over the valid
        rows, restricted to the simplex tangent space and to the participating exponents
        (``w_j > PARTICIPATION_THRESHOLD``). Small values flag a nearly flat direction (weak
        identifiability of the exponents). ``nan`` at ``temperature = inf`` (the objective is not
        twice differentiable) and for a facet with fewer than two participating exponents. A
        read-only diagnostic.
    n_features_in_ : int
        Number of metrics seen in ``fit``.
    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of the metrics seen in ``fit``; defined only for string column names.

    See Also
    --------
    hyperbolic_trade_space.make_frontier_data : Synthetic data with a planted frontier.

    Notes
    -----
    Zero metrics are tolerated: ``log 0 = -inf``, the row has support weight 0 and is excluded
    from the objective; its ``Z`` is ``nan`` and it has no inverse. Scoring follows the
    continuous extension of a monomial: ``log V = sum_{j: w_j > EPS_ZERO_EXPONENT} w_j log m_j -
    beta`` with ``0 log 0 := 0``, so a zero metric on a numerically zero exponent leaves
    ``log V`` finite and a zero metric on a participating exponent gives ``V = 0``,
    ``log V = -inf`` (for ``n_terms > 1`` each facet's score follows the same rule). Negative
    values raise ``ValueError``. Grounding: homogeneity and the invariant form, the offset, gradient
    and support weights, convexity, log-mean-exp, the noise offset, elasticities and improvement
    factors, and the chart, each derived in the documentation.

    For ``n_terms > 1`` the score is ``log V = Phi_K(u)`` and the chart ``[Z | log V]`` is
    inverted in closed form (``Phi_K(u + s 1) = Phi_K(u) + s``), exactly for every
    ``term_temperature``. ``K > 1`` is a local optimum of a partition-and-refit scheme; restarts
    are drawn from ``random_state``. Degenerate input (one metric, one valid row, fewer valid
    rows than ``n_terms``) repeats the ``K = 1`` fit. A single valid row is a declared
    convention: the fitted object does not exist for it (the objective has no minimizer worth
    the name), uniform exponents are returned, and ``fit`` emits a ``UserWarning`` saying so.

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
    >>> X, info = make_frontier_data(300, 3, random_state=0)
    >>> hts = HyperbolicTradeSpace(temperature=np.inf).fit(X)
    >>> np.allclose(hts.exponents_[0], info["exponents"], atol=1e-3)
    True
    >>> hts.transform(X).shape
    (300, 3)
    >>> hts.get_feature_names_out().tolist()
    ['ilr0', 'ilr1', 'log_v']
    >>> bool(np.allclose(hts.inverse_transform(hts.transform(X)), X))
    True

    Three facets:

    >>> X, info = make_frontier_data(400, 4, n_terms=3, random_state=0)
    >>> est = HyperbolicTradeSpace(
    ...     n_terms=3, temperature=np.inf, random_state=0).fit(X)
    >>> est.exponents_.shape, est.basis_.shape
    ((3, 4), (3, 3, 4))
    >>> bool(np.isclose(est.facet_share_.sum(), 1.0))
    True
    >>> bool(np.allclose(
    ...     np.sort(est.exponents_, axis=0),
    ...     np.sort(info["exponents"], axis=0), atol=0.05))
    True
    """

    def __init__(
        self,
        temperature=10.0,
        min_exponent=0.0,
        coordinates="ilr",
        n_terms=1,
        term_temperature=np.inf,
        term_aggregation="sum",
        tol=1e-10,
        max_iter=500,
        penalty=None,
        alpha=0.0,
        random_state=None,
        facet_step="support",
        n_restarts=5,
    ):
        self.temperature = temperature
        self.min_exponent = min_exponent
        self.coordinates = coordinates
        self.n_terms = n_terms
        self.term_temperature = term_temperature
        self.term_aggregation = term_aggregation
        self.tol = tol
        self.max_iter = max_iter
        self.penalty = penalty
        self.alpha = alpha
        self.random_state = random_state
        self.facet_step = facet_step
        self.n_restarts = n_restarts

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.input_tags.positive_only = True
        tags.input_tags.sparse = False
        return tags

    # ------------------------------------------------------------------ validation helpers
    def _check_params(self, d):
        t = self.temperature
        if not (isinstance(t, numbers.Real) and not isinstance(t, bool) and t > 0):
            raise ValueError(f"temperature must be a float > 0 or np.inf, got {t!r}")
        m = self.min_exponent
        if not (isinstance(m, numbers.Real) and 0.0 <= m < 1.0 / d):
            raise ValueError(f"min_exponent must be in [0, 1/d) = [0, {1.0 / d:.4g}), got {m!r}")
        if self.coordinates not in ("ilr", "alr"):
            raise ValueError(f"coordinates must be 'ilr' or 'alr', got {self.coordinates!r}")
        if not (isinstance(self.n_terms, numbers.Integral) and self.n_terms >= 1):
            raise ValueError(f"n_terms must be an integer >= 1, got {self.n_terms!r}")
        if not (isinstance(self.tol, numbers.Real) and self.tol > 0):
            raise ValueError(f"tol must be > 0, got {self.tol!r}")
        if not (isinstance(self.max_iter, numbers.Integral) and self.max_iter >= 1):
            raise ValueError(f"max_iter must be an integer >= 1, got {self.max_iter!r}")
        k = self.term_temperature
        if not (isinstance(k, numbers.Real) and not isinstance(k, bool) and k > 0):
            raise ValueError(f"term_temperature must be a float > 0 or np.inf, got {k!r}")
        if self.term_aggregation not in ("sum", "mean"):
            raise ValueError(
                f"term_aggregation must be 'sum' or 'mean', got {self.term_aggregation!r}"
            )
        if self.penalty not in (None, "reweighted_l1"):
            raise ValueError(f"penalty must be None or 'reweighted_l1', got {self.penalty!r}")
        a = self.alpha
        if not (isinstance(a, numbers.Real) and not isinstance(a, bool) and a >= 0):
            raise ValueError(f"alpha must be a real number >= 0, got {a!r}")
        check_random_state(self.random_state)
        if not (isinstance(self.n_restarts, numbers.Integral) and self.n_restarts >= 1):
            raise ValueError(f"n_restarts must be an integer >= 1, got {self.n_restarts!r}")
        if self.facet_step not in ("support", "tangent"):
            raise ValueError(f"facet_step must be 'support' or 'tangent', got {self.facet_step!r}")

    def _log_metrics(self, X, reset):
        X = validate_data(self, X, reset=reset, dtype=np.float64)
        check_non_negative(X, "HyperbolicTradeSpace (input X)")
        with np.errstate(divide="ignore"):
            return np.log(X)

    # ------------------------------------------------------------------ fit
    def fit(self, X, y=None):
        """Fit the frontier ``w``, ``beta`` and the chart.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Strictly positive (zeros tolerated) larger-is-better metrics.
        y : None
            Ignored.

        Returns
        -------
        self : HyperbolicTradeSpace
            The fitted estimator.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(100, 2, random_state=1)
        >>> HyperbolicTradeSpace().fit(X).exponents_.shape
        (1, 2)
        """
        U = self._log_metrics(X, reset=True)
        n, d = U.shape
        self._check_params(d)
        tau = float(self.temperature)
        valid = np.isfinite(U).all(axis=1)
        if not valid.any():
            raise ValueError(f"every row contains a zero metric (n_samples = {n}); nothing to fit")
        Uv = U[valid]
        nv = Uv.shape[0]

        K = int(self.n_terms)
        if K > 1 and d > 1 and nv > 1:
            tr = _solvers.solve_terms(
                Uv, K, tau, self.min_exponent, self.penalty, self.alpha,
                random_state=self.random_state, tol=self.tol, slsqp_max_iter=self.max_iter,
                facet_step=self.facet_step, n_restarts=self.n_restarts,
                term_temperature=self.term_temperature,
                aggregation=self.term_aggregation,
            )  # fmt: skip
            res, W, betas, n_iter, beta = tr, tr.W, tr.beta, tr.n_iter, tr.objective
            term = tr.termination
        else:
            if d == 1:
                w = np.ones(1)
                beta = _solvers.log_mean_exp(Uv[:, 0], tau)
                p = _solvers.support_weights(Uv[:, 0], tau)
                n_iter, reason = 1, "d = 1: the exponent is 1"
            elif nv == 1:
                warnings.warn(
                    "a single valid row: the fitted object does not exist for this input; "
                    "uniform exponents are returned as a convention",
                    UserWarning,
                    stacklevel=2,
                )
                w = np.full(d, 1.0 / d)
                beta = float(Uv[0] @ w)
                p = np.ones(1)
                n_iter, reason = 1, "single valid row: uniform exponents (convention)"
            else:
                res = _solvers.solve_lp(Uv, self.min_exponent)
                if np.isfinite(tau):
                    res = _solvers.solve_slsqp(
                        Uv, tau, self.min_exponent, w0=res.w, tol=self.tol,
                        max_iter=self.max_iter, penalty=self.penalty, alpha=self.alpha,
                    )  # fmt: skip
                w, beta, p, n_iter, reason = res.w, res.beta, res.p, res.n_iter, res.message
            if d == 1 or nv == 1:
                res = None
            W, betas = np.tile(w, (K, 1)), np.full(K, beta)
            term = _solvers.single_facet_termination(
                Uv, w, beta, p, tau, self.min_exponent, n_iter, reason, K
            )
        if res is not None and term.status == "iteration_cap":
            # the alternation stopped at its cap: silent when every term is stationary on its
            # rows and the objective had stopped moving, both to within tol (the assignment step
            # cycles among rows that tie between terms); the status and the gap are recorded
            if not (term.max_gap <= self.tol and term.objective_change <= self.tol):
                warnings.warn(
                    "iteration cap reached before the fit was stationary to tol "
                    f"{self.tol:g} (max term gap {term.max_gap:.2e}, last objective change "
                    f"{term.objective_change:.2e}); termination status 'iteration_cap'",
                    ConvergenceWarning,
                    stacklevel=2,
                )
        elif res is not None and (not res.success or term.status in _WARN_STATUSES):
            warnings.warn(
                f"solver did not converge: {term.reason}; termination status {term.status!r}, "
                f"max term gap {term.max_gap:.2e}",
                ConvergenceWarning,
                stacklevel=2,
            )

        B = _coords.helmert_basis(d) if self.coordinates == "ilr" else _coords.alr_basis(d)
        self.exponents_, self.log_offset_ = W, betas
        self.basis_ = B if K == 1 else np.repeat(B[None], K, axis=0)
        _, log_v = self._chart(U)
        lab = self._assign(U)
        kappa = self.term_temperature
        if K > 1:
            near = valid & (np.abs(log_v) < (1.0 / tau if np.isfinite(tau) else 0.1))
            p = np.zeros(nv)
            for k in range(K):
                m = lab[valid] == k
                if m.any():
                    p[m] = _solvers.support_weights(Uv[m] @ W[k], tau) * m.sum() / nv
            share = np.bincount(lab[near], minlength=K) / max(near.sum(), 1)
        else:
            share = np.ones(1)  # the single facet owns every near-frontier row
        self.facet_ = lab
        with np.errstate(over="ignore"):
            self.coefficients_ = np.exp(-(1.0 if np.isinf(kappa) else kappa) * betas)
        self.facet_share_ = share
        # mean slack over the valid rows: beta_k(i) - w_k(i) . u_i, k(i) the row's facet (the
        # label model);
        # -mean_i Phi_kappa(u_i) for a finite term temperature (the model the estimator reports)
        lv = lab[valid]
        self.mean_slack_ = float(np.mean(betas[lv] - np.einsum("ij,ij->i", W[lv], Uv)))
        if K > 1 and np.isfinite(kappa):  # the slack of the reported (soft) model
            self.mean_slack_ = _solvers.soft_objective(Uv, W, betas, kappa, self.term_aggregation)
        support = np.zeros(n)
        support[valid] = p
        above = log_v[valid] > (_ABOVE_TOL if np.isinf(tau) else 0.0)

        self.support_weights_ = support
        self.n_eff_ = float(1.0 / np.sum(p**2))
        self.frac_above_ = float(np.mean(above))
        self.objective_ = float(beta)
        self.n_iter_ = max(int(n_iter), 1)
        self.training_log_v_ = log_v
        self.termination_ = term
        self.conditioning_ = self._conditioning(Uv, tau)
        return self

    def _conditioning(self, Uv, tau):
        """Smallest eigenvalue of each facet's restricted Hessian of ``J_tau`` (read only)."""
        W = self.exponents_
        out = np.full(W.shape[0], np.nan)
        if np.isinf(tau):
            return out
        for k, w in enumerate(W):
            part = w > PARTICIPATION_THRESHOLD
            n_part = int(part.sum())
            if n_part < 2:
                continue
            Ua = Uv[:, part]
            p = _solvers.support_weights(Uv @ w, tau)
            pa = Ua.T @ p
            H = tau * (Ua.T @ (p[:, None] * Ua) - np.outer(pa, pa))
            T = _coords.helmert_basis(n_part)  # orthonormal basis of the simplex tangent space
            out[k] = np.linalg.eigvalsh(T @ H @ T.T)[0]
        return out

    def _phi(self, S):
        kappa = self.term_temperature
        if np.isinf(kappa):
            return S.max(axis=1)
        shift = _solvers.aggregation_shift(S.shape[1], kappa, self.term_aggregation)
        return logsumexp(kappa * S, axis=1) / kappa - shift

    def _zero_limit_scores(self, U):
        """Per-facet scores of rows with a zero metric: ``0 log 0 := 0`` below EPS_ZERO_EXPONENT."""
        W, b = self.exponents_, self.log_offset_
        part = W > EPS_ZERO_EXPONENT  # (K, d)
        zero = -np.inf == U  # (n, d)
        S = np.where(zero, 0.0, U) @ np.where(part, W, 0.0).T - b
        S[(zero.astype(float) @ part.T.astype(float)) > 0] = -np.inf
        return S

    def _chart(self, U):
        W, b, B = self.exponents_, self.log_offset_, self.basis_
        if W.shape[0] == 1:
            Z, log_v = _coords.to_frontier_coordinates(U, W[0], b[0], B)
        else:
            bad = (-np.inf == U).any(axis=1)
            Uf = np.where(bad[:, None], 0.0, U)
            Z, log_v = Uf @ B[0].T, self._phi(Uf @ W.T - b)
        bad = (-np.inf == U).any(axis=1)
        if bad.any():  # rows with a zero metric: the formal limit, Z undefined
            S = self._zero_limit_scores(U[bad])
            log_v[bad] = S[:, 0] if S.shape[1] == 1 else self._phi(S)
            Z[bad] = np.nan
        return Z, log_v

    def _inverse(self, Z, log_v):
        W, b, B = self.exponents_, self.log_offset_, self.basis_
        if W.shape[0] == 1:
            return _coords.from_frontier_coordinates(Z, log_v, W[0], b[0], B)
        log_v = np.atleast_1d(np.asarray(log_v, dtype=float))
        Z = np.asarray(Z, dtype=float).reshape(log_v.size, B.shape[1])
        bad = ~np.isfinite(log_v) | ~np.isfinite(Z).all(axis=1)
        d = W.shape[1]
        base = (
            np.where(bad[:, None], 0.0, Z) @ np.linalg.pinv(B[0]).T
            if d > 1
            else np.zeros((Z.shape[0], 1))
        )
        U = base + (np.where(bad, 0.0, log_v) - self._phi(base @ W.T - b))[:, None]
        U[bad] = np.nan
        return U

    def _assign(self, U):
        bad = (-np.inf == U).any(axis=1)
        lab = np.argmax(
            np.where(bad[:, None], 0.0, U) @ self.exponents_.T - self.log_offset_, axis=1
        )
        return np.where(bad, -1, lab)

    # ------------------------------------------------------------------ chart
    def _coordinates(self, X):
        check_is_fitted(self)
        return self._chart(self._log_metrics(X, reset=False))

    def transform(self, X):
        """Map metrics to the chart ``[Z | log V]``.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Metrics, nonnegative.

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            ``Z`` (``n_features - 1`` log-ratio coordinates) then ``log V``. Rows with a zero
            metric give ``nan`` in ``Z`` and ``-inf`` in ``log V``.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(50, 3, random_state=0)
        >>> HyperbolicTradeSpace().fit(X).transform(X[:2]).shape
        (2, 3)
        """
        Z, log_v = self._coordinates(X)
        return np.column_stack([Z, log_v])

    def inverse_transform(self, Xt):
        """Map chart coordinates ``[Z | log V]`` back to metrics.

        Parameters
        ----------
        Xt : array-like of shape (n_samples, n_features)
            Chart coordinates as returned by ``transform``.

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            Metrics ``exp(u)`` (the inverse chart). Rows with non-finite coordinates (a zero
            metric in the original) are not invertible and give ``nan``.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(50, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> bool(np.allclose(hts.inverse_transform(hts.transform(X)), X))
        True
        """
        check_is_fitted(self)
        Xt = check_array(Xt, dtype=np.float64, ensure_all_finite=False)
        if Xt.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X has {Xt.shape[1]} features, but {self.__class__.__name__} is expecting "
                f"{self.n_features_in_} features as input"
            )
        return np.exp(self._inverse(Xt[:, :-1], Xt[:, -1]))

    def get_feature_names_out(self, input_features=None):
        """Names of the transform columns: ``ilr0..`` (or ``alr0..``) then ``log_v``.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Checked against ``feature_names_in_`` and ``n_features_in_`` when given.

        Returns
        -------
        ndarray of str, shape (n_features_in_,)
            Output feature names.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(30, 2, random_state=0)
        >>> hts = HyperbolicTradeSpace(coordinates="alr").fit(X)
        >>> hts.get_feature_names_out().tolist()
        ['alr0', 'log_v']
        """
        check_is_fitted(self)
        if input_features is not None:
            names = np.asarray(input_features, dtype=object)
            if names.shape != (self.n_features_in_,):
                raise ValueError(
                    f"input_features should have length equal to number of features "
                    f"({self.n_features_in_}), got {names.size}"
                )
            fitted = getattr(self, "feature_names_in_", None)
            if fitted is not None and not np.array_equal(names, fitted):
                raise ValueError("input_features is not equal to feature_names_in_")
        prefix = "ilr" if self.coordinates == "ilr" else "alr"
        out = [f"{prefix}{k}" for k in range(self.n_features_in_ - 1)] + ["log_v"]
        return np.asarray(out, dtype=object)

    # ------------------------------------------------------------------ scores and domain methods
    def score_samples(self, X):
        """Log invariant value ``log V(m) = w . log m - beta`` of each row.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns
        -------
        ndarray of shape (n_samples,)
            ``log V``; ``-inf`` for a zero metric. Positive means beyond the fitted frontier.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> HyperbolicTradeSpace().fit(X).score_samples(X).shape
        (60,)
        """
        return self._coordinates(X)[1]

    def invariant_value(self, X):
        """Invariant value ``V = exp(log V)``; ``V = 1`` on the frontier, ``V < 1`` inside.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns
        -------
        ndarray of shape (n_samples,)
            ``V``; 0 for a zero metric.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> bool((HyperbolicTradeSpace(temperature=float("inf")).fit(X)
        ...       .invariant_value(X) <= 1 + 1e-9).all())
        True
        """
        return np.exp(self.score_samples(X))

    def project(self, X):
        """Project onto the frontier along the diagonal: ``m / V`` (invariant form).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            ``m / V``, which has ``V = 1`` (homogeneity); ``nan`` rows where ``V = 0``.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> bool(np.allclose(hts.invariant_value(hts.project(X)), 1.0))
        True
        """
        V = self.invariant_value(X)
        X = check_array(X, dtype=np.float64)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = X / V[:, None]
        out[V == 0] = np.nan
        return out

    def assign_facets(self, X):
        """Facet of each row: ``argmax_k (w_k . log m - beta_k)``.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Metrics, nonnegative.

        Returns
        -------
        ndarray of int, shape (n_samples,)
            Index in ``[0, n_terms)`` of the facet that attains the maximum; ``-1`` for rows with
            a zero metric. All zeros when ``n_terms = 1``.

        Examples
        --------
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(150, 4, n_terms=3, random_state=0)
        >>> est = HyperbolicTradeSpace(n_terms=3, random_state=0).fit(X)
        >>> bool((est.assign_facets(X) == est.facet_).all())
        True
        """
        check_is_fitted(self)
        return self._assign(self._log_metrics(X, reset=False))

    def improvement_factors(self, X):
        """Per-metric improvement factor ``V^(-1/w_j)`` that lands on the frontier.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)

        Returns
        -------
        ndarray of shape (n_samples, n_features)
            Entry ``(i, j)``: the factor by which metric ``j`` alone must be multiplied to reach
            ``V = 1``. ``inf`` where ``w_j`` is below ``1e-12`` (numerically zero) or ``V = 0``.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> x = X[:1].copy()
        >>> f = hts.improvement_factors(x)[0, 1]
        >>> x[0, 1] *= f
        >>> round(float(hts.invariant_value(x)[0]), 6)
        1.0
        """
        check_is_fitted(self)
        U = self._log_metrics(X, reset=False)
        log_v = self._chart(U)[1]
        w = self.exponents_[np.maximum(self._assign(U), 0)]  # exponents of the assigned facet
        out = np.full(w.shape, np.inf)
        pos = w > 1e-12  # exponents below 1e-12 are numerically zero (solver noise)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            out[pos] = np.exp(-log_v[:, None] / w)[pos]
        out[~np.isfinite(log_v), :] = np.inf
        return out

    def novelty_score(self, X, calibrated=False):
        """Novelty of each row relative to the fitted frontier.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
        calibrated : bool, default=False
            If False return ``V - 1`` (the uniform factor by which a frontier design must improve
            to reach the point, the invariant form). If True return an array whose first column is
            the fraction of training ``log V`` (finite ones) that are ``<=`` the query's, and whose
            second is ``tau * log V`` (``log V`` itself when ``tau`` is infinite).

        Returns
        -------
        ndarray of shape (n_samples,) or (n_samples, 2)

        Notes
        -----
        Training rows exceed ``V = 1`` by construction at finite ``tau`` (``frac_above_``), so
        the calibrated form is the fair comparison. Far from the balanced region ``V - 1`` is
        conservative.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(80, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> hts.novelty_score(X[:3]).shape, hts.novelty_score(
        ...     X[:3], calibrated=True).shape
        ((3,), (3, 2))
        """
        log_v = self.score_samples(X)
        if not calibrated:
            return np.exp(log_v) - 1.0
        train = np.sort(self.training_log_v_[np.isfinite(self.training_log_v_)])
        rank = np.searchsorted(train, log_v, side="right") / train.size
        tau = self.temperature
        scaled = log_v if np.isinf(tau) else tau * log_v
        return np.column_stack([rank, scaled])

    def level_set(self, Z, value=1.0):
        """Metric points on the level set ``{V = value}`` above chart coordinates ``Z``.

        Parameters
        ----------
        Z : array-like of shape (n_points, n_features - 1)
            Log-ratio coordinates (the leading columns of ``transform``).
        value : float, default=1.0
            Target invariant value ``V > 0``; 1 is the frontier.

        Returns
        -------
        ndarray of shape (n_points, n_features)
            Metrics ``m`` with ``V(m) = value`` whose chart coordinates are ``Z``.

        Examples
        --------
        >>> import numpy as np
        >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
        >>> X, _ = make_frontier_data(60, 3, random_state=0)
        >>> hts = HyperbolicTradeSpace().fit(X)
        >>> M = hts.level_set(np.zeros((1, 2)), value=0.5)
        >>> round(float(hts.invariant_value(M)[0]), 6)
        0.5
        """
        check_is_fitted(self)
        if not value > 0:
            raise ValueError("value must be > 0")
        d = self.n_features_in_
        Z = check_array(Z, dtype=np.float64, ensure_min_features=0, ensure_min_samples=1)
        if Z.shape[1] != d - 1:
            raise ValueError(f"Z must have {d - 1} columns, got {Z.shape[1]}")
        log_v = np.full(Z.shape[0], np.log(value))
        return np.exp(self._inverse(Z, log_v))
