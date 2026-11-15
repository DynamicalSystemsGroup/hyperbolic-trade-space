"""Trade-offs of a fitted trade space: the report, the tension matrix and a design's tensions.

The model is built to find trade-offs, not variance. PCA picks the directions of largest spread
(where the data are free); the fit picks the positive combination ``w`` of log-metrics with the
smallest upper extent, the binding constraint among larger-is-better metrics. ``trade_off_report``
reads that structure at three levels, all for the K = 1 fit (one trade-off; several regional
trade-offs are the K > 1 extension, below, and a deflation search for successive trade-offs is a
research question). At K > 1 the same three levels are read once per term, on the rows assigned to
that term (``assign_cells``), and a list of K
reports is returned:

1. **Participation and elasticities.** Metrics with ``w_j > threshold`` participate, the rest are
   free at the balanced point; the elasticity of metric ``k`` against metric ``j`` along the
   frontier is ``-w_k / w_j``.
2. **The contending set (n-lemma).** At ``tau = inf`` the fit is a linear program whose solution is
   sparse, with exact zero exponents; the support is the set of metrics that contend, of any size
   ``n`` and without a prior choice of which or how many. At a working finite ``tau`` the weights
   are smoothed, so small weights mean weak participation rather than membership. This reading needs
   ``min_exponent = 0``, since a positive floor masks the sparsity.
3. **Association and spread directions among near-frontier designs** (``|log V| < band``): the
   pairwise association of log-metrics (negative = traded, positive = aligned), and the PCA of the
   near-frontier chart coordinates ``Z`` whose principal directions are the directions of the
   spread, with loadings on the metrics through the chart basis.

The *tension* is another object, a derivative along the fitted reference surface:
``T[i, j] = d m_j / d m_i = -(w_i / w_j)(m_j / m_i)`` on a term, with the other metrics held.
``tension_matrix`` gives each term's matrix at the term's balanced point (from the fit) and
``design_tensions`` the same formula at each design's own metric ratios (from the data); the
elasticity is its log-log form, constant on a term. The report's association, a correlation of the
data, is a different object from the tension.

Limits, stated here because the report cannot state them for you: a *trade-off* is a binding
constraint, a *correlation* is only a co-movement; near the frontier ``w . u`` is almost
constant, so the **closure effect** forces some negative association among participating metrics
even where no designer ever traded them; the result depends on the ``band``; and K = 1 finds
one term (at K > 1 each term's contending set is the ``tau = inf`` LP support on that term's rows
centred on their mean, as in the term refit, since the raw rows of one term do not enclose the
origin and the uncentred LP returns vertex artefacts).
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np
from scipy.stats import rankdata
from sklearn.utils.validation import check_array, check_is_fitted

from . import solvers as _solvers
from .gaps import orient_by_pca

__all__ = [
    "DesignTensions",
    "TradeOffReport",
    "design_tensions",
    "tension_matrix",
    "trade_off_report",
]

_CLOSURE_NOTE = (
    "Closure effect: near the frontier w . u is nearly constant, so a binding constraint induces "
    "negative association among participating metrics even where no designer traded them. Read "
    "negative association as a trade-off only together with the exponents and the principal "
    "spread directions; positive association among participating metrics is the stronger "
    "evidence of alignment."
)
_NAMES = {1: "monolemma", 2: "dilemma", 3: "trilemma"}


@dataclass(frozen=True, eq=False)
class TradeOffReport:
    """What ``trade_off_report`` returns: the contending set, elasticities and spread directions.

    Attributes
    ----------
    participating : ndarray of bool, shape (d,)
        ``exponents > threshold`` at the fit temperature.
    exponents : ndarray of shape (d,)
        Working-temperature exponents ``w`` (the estimator's ``exponents_[0]``).
    elasticities : ndarray of shape (d, d)
        Entry ``[j, k] = -w_k / w_j`` ; ``nan`` in rows where ``w_j <= threshold``.
        The diagonal is ``-1`` by the formula and carries no information.
    association : ndarray of shape (d, d)
        Correlation matrix of the log-metrics of the near-frontier rows.
    association_kind : str
        ``"pearson"`` or ``"spearman"``.
    closure_note : str
        Statement of the closure effect on ``association``.
    spread_directions : ndarray of shape (d-1, d-1)
        Unit principal directions in chart coordinates ``Z`` of the near-frontier rows (rows).
    spread_loadings : ndarray of shape (d-1, d)
        The same directions as loadings on the (log-)metrics, ``directions @ basis_``.
    explained_spread : ndarray of shape (d-1,)
        Share of near-frontier ``Z`` variance along each direction.
    contending_set : ndarray of int
        Indices of the support of the ``tau = inf`` LP exponents (greater than 1e-9), computed with
        ``min_exponent = 0``.
    contending_exponents : ndarray
        The LP exponents on the contending set.
    n_lemma : int
        Size of the contending set.
    lemma_name : str
        ``"monolemma"``, ``"dilemma"``, ``"trilemma"``, then ``"4-lemma"``, ...
    band : float
        The half-width of ``|log V|`` that defined the near-frontier rows.
    n_near_frontier : int
        Number of near-frontier rows used.
    """

    participating: np.ndarray
    exponents: np.ndarray
    elasticities: np.ndarray
    association: np.ndarray
    association_kind: str
    closure_note: str
    spread_directions: np.ndarray
    spread_loadings: np.ndarray
    explained_spread: np.ndarray
    contending_set: np.ndarray
    contending_exponents: np.ndarray
    n_lemma: int
    lemma_name: str
    band: float
    n_near_frontier: int


def _lemma_name(n):
    return _NAMES.get(n, f"{n}-lemma")


def trade_off_report(
    estimator, X, band=None, min_near_frontier=10, threshold=1e-3, association="pearson"
):
    """Report the trade-offs of a fitted trade space (a list of K reports when ``n_terms = K > 1``).

    Parameters
    ----------
    estimator : HyperbolicTradeSpace
        Fitted estimator.
    X : array-like of shape (n_samples, n_features)
        Metrics (nonnegative); rows with a zero metric are ignored. The ``tau = inf`` LP is solved
        on the log of these rows, independent of the fit temperature and ``min_exponent``.
    band : float, optional
        Near-frontier rows are those with ``|log V| < band``. Default ``1 / tau`` for finite
        ``tau`` and 0.1 at ``tau = inf``.
    min_near_frontier : int, default=10
        Fewer near-frontier rows raises ``ValueError``.
    threshold : float, default=1e-3
        Exponents above this participate at the fit temperature.
    association : {"pearson", "spearman"}, default="pearson"
        Association measure for the log-metrics of near-frontier rows.

    Returns
    -------
    TradeOffReport or list of TradeOffReport
        One report at ``n_terms = 1``; at ``n_terms = K > 1`` a list of K, one per term, each on
        the rows assigned to that term with the term's exponents, near-frontier rows
        (``|Phi_K| < band``), spread directions and loadings (through ``basis_[k]``).

    Raises
    ------
    ValueError
        If ``association`` is unknown or fewer than ``min_near_frontier`` rows are near the
        frontier; the message gives the ``band`` (and the fit temperature that matches it, since the
        default band is ``1 / tau``) that would hold ``min_near_frontier`` rows; at K > 1 it names
        the term.

    Warns
    -----
    UserWarning
        If ``estimator.min_exponent > 0``: the working weights are floored, and the contending
        set (always computed with ``min_exponent = 0``) can differ from the working support.

    Notes
    -----
    For ``d = 1`` the report is trivial (``w = [1]``, a monolemma, no directions). The report is
    deterministic. Part 3 equals ``orient_by_pca(Z, |log V| < band)`` on the same rows
    (``hyperbolic_trade_space.gaps.orient_by_pca``). The closure effect is stated in
    ``closure_note`` and in the module docstring.

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space import (
    ...     HyperbolicTradeSpace, make_frontier_data, trade_off_report)
    >>> X, _ = make_frontier_data(400, 3, random_state=0)
    >>> est = HyperbolicTradeSpace(temperature=np.inf).fit(X)
    >>> rep = trade_off_report(est, X)
    >>> rep.lemma_name, rep.contending_set.tolist(), rep.spread_directions.shape
    ('trilemma', [0, 1, 2], (2, 2))

    At ``n_terms = 3`` there is one report per term:

    >>> W = [[.5, .5, 0, 0], [0, .5, .5, 0], [0, 0, .5, .5]]
    >>> X, _ = make_frontier_data(900, 4, exponents=W, n_terms=3, random_state=0)
    >>> est = HyperbolicTradeSpace(
    ...     n_terms=3, temperature=20.0, random_state=0).fit(X)
    >>> sorted(r.contending_set.tolist() for r in trade_off_report(est, X))
    [[0, 1], [1, 2], [2, 3]]
    """
    check_is_fitted(estimator)
    if association not in ("pearson", "spearman"):
        raise ValueError(f"association must be 'pearson' or 'spearman', got {association!r}")
    if estimator.min_exponent > 0:
        warnings.warn(
            f"estimator.min_exponent = {estimator.min_exponent} > 0 floors the working exponents; "
            "the n-lemma reading needs min_exponent = 0 (the contending set here is recomputed "
            "with min_exponent = 0 at tau = inf).",
            UserWarning,
            stacklevel=2,
        )
    X = check_array(X, dtype=np.float64, ensure_min_features=1)
    if X.shape[1] != estimator.n_features_in_:
        raise ValueError(
            f"X has {X.shape[1]} features, but the estimator expects {estimator.n_features_in_}"
        )
    if (X < 0).any():
        raise ValueError("Negative values in data")
    tau = float(estimator.temperature)
    if band is None:
        band = 0.1 if np.isinf(tau) else 1.0 / tau
    band = float(band)
    args = (float(band), min_near_frontier, threshold, association)

    Z, log_v = estimator._coordinates(X)
    finite = np.isfinite(log_v) & np.isfinite(Z).all(axis=1)
    U = np.log(X[finite])
    Zf, lvf = Z[finite], log_v[finite]
    K = estimator.exponents_.shape[0]
    if K == 1:
        return _report(U, Zf, lvf, estimator.exponents_[0], U, estimator.basis_, *args, "")
    lab = estimator.assign_cells(X)[finite]
    reports = []
    for k in range(K):
        r = lab == k
        Uk, wk, Bk = U[r], estimator.exponents_[k], estimator.basis_[k]
        reports.append(_report(Uk, Zf[r], lvf[r], wk, Uk - Uk.mean(0), Bk, *args, f"term {k}: "))
    return reports


def _report(U, Zf, lvf, w, U_lp, basis, band, min_near_frontier, threshold, association, who):
    """One report from finite log rows ``U``, their chart ``Zf, lvf`` and the term ``w``."""
    w, d = np.array(w, dtype=float), U.shape[1]
    # contending set: tau = inf LP with exact zeros
    if d == 1:
        support = np.array([0])
        lp_w = np.ones(1)
    else:
        res = _solvers.solve_lp(U_lp, 0.0)
        if not res.success:
            warnings.warn(
                f"{who}tau = inf LP did not converge: {res.message}", UserWarning, stacklevel=3
            )
        support = np.flatnonzero(res.w > 1e-9)
        lp_w = res.w
    n_lemma = int(support.size)

    participating = w > threshold
    with np.errstate(divide="ignore", invalid="ignore"):
        rates = np.where(participating[:, None], -w[None, :] / w[:, None], np.nan)

    near = np.abs(lvf) < band
    n_near = int(near.sum())
    if d > 1 and n_near < min_near_frontier:
        have = np.sort(np.abs(lvf))
        if have.size >= min_near_frontier:
            # the smallest band that holds min_near_frontier rows of this term (strict inequality)
            need = float(np.nextafter(float(f"{have[min_near_frontier - 1]:.2g}"), np.inf))
            if need <= have[min_near_frontier - 1]:
                need = float(f"{have[min_near_frontier - 1] * 1.1:.2g}")
            hint = (
                f"use a larger band, band={need:g} (the smallest round band with "
                f"{min_near_frontier} rows on this term), or fit at temperature={1.0 / need:.3g} "
                f"(the band is 1/temperature), or "
                f"lower min_near_frontier"
            )
        else:
            hint = (
                f"this term owns only {have.size} usable rows; lower min_near_frontier to "
                f"{max(have.size, 2)}, use a larger band, or fit with fewer terms"
            )
        raise ValueError(
            f"{who}only {n_near} near-frontier rows (|log V| < {band:g}) but min_near_frontier = "
            f"{min_near_frontier}; {hint}"
        )

    if d == 1:
        assoc = np.ones((1, 1))
        dirs, load, evr = np.empty((0, 0)), np.empty((0, 1)), np.empty(0)
    else:
        Un = U[near]
        if association == "spearman":
            Un = np.column_stack([rankdata(c) for c in Un.T])
        with np.errstate(invalid="ignore", divide="ignore"):
            assoc = np.corrcoef(Un, rowvar=False)
        _, dirs, evr = orient_by_pca(Zf, near)
        load = dirs @ basis

    return TradeOffReport(
        participating=participating,
        exponents=w,
        elasticities=rates,
        association=np.atleast_2d(assoc),
        association_kind=association,
        closure_note=_CLOSURE_NOTE,
        spread_directions=dirs,
        spread_loadings=load,
        explained_spread=evr,
        contending_set=support,
        contending_exponents=lp_w[support],
        n_lemma=n_lemma,
        lemma_name=_lemma_name(n_lemma),
        band=band,
        n_near_frontier=n_near,
    )


# --------------------------------------------------------------------------- the tension matrix


def _balanced_point(U_term, w, tau):
    """The term's balanced point in log-metrics: the softmax-weighted mean log-metric of its rows.

    The weights are ``p_i`` proportional to ``exp(tau w . u_i)``; at ``tau = inf`` they are the rows
    that attain the maximum of ``w . u_i``, equally weighted.
    """
    s = U_term @ w
    p = (s >= s.max() - 1e-12).astype(float) if np.isinf(tau) else np.exp(tau * (s - s.max()))
    return (p / p.sum()) @ U_term


def _tension_cells(w, u, threshold):
    """``T[i, j] = -(w_i / w_j) exp(u_j - u_i)`` with the cases of the definition.

    ``u`` has shape ``(..., d)``; the result ``(..., d, d)``. The diagonal is ``nan`` (a metric
    against itself is not a tension); ``nan`` also in every column ``j`` whose exponent is at or
    below ``threshold`` (blank: the metric ``j`` is not determined by ``i`` on the term); ``0.0``
    where only ``i`` carries none (zero).
    """
    w = np.asarray(w, dtype=float)
    part = w > threshold
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.exp(u[..., None, :] - u[..., :, None])  # exp(u_j - u_i)
        T = -(w[:, None] / w[None, :]) * ratio
    T = np.where(part[:, None], T, 0.0)  # i carries no exponent: zero
    T = np.where(part[None, :], T, np.nan)  # j carries none: blank
    d = w.size
    T[..., np.arange(d), np.arange(d)] = np.nan
    return T


def tension_matrix(estimator, X, threshold=1e-3):
    """The tension matrix of every term, at the term's balanced point (from the fit).

    The tension of metric ``j`` against metric ``i`` on a term is the derivative of ``m_j`` with
    respect to ``m_i`` along the term, the other metrics held, in the conditioned metrics::

        T[i, j] = d m_j / d m_i = -(w_i / w_j) (m_j / m_i)

    (Definition of tension; derived in ``derivation/lemma_21_tension.py``). The elasticity
    ``-w_i / w_j`` is its log-log form and is constant on a term; the tension carries the factor
    ``m_j / m_i`` and so changes along the term. The term's matrix evaluates it at the term's
    balanced point, the softmax-weighted mean log-metric of the rows assigned to the term at the
    fit temperature. A design's tensions, from the data, are another object
    (:func:`design_tensions`).

    Parameters
    ----------
    estimator : HyperbolicTradeSpace
        Fitted estimator.
    X : array-like of shape (n_samples, n_features)
        Metrics (nonnegative) whose rows locate each term's balanced point; rows with a zero
        metric are ignored. At ``n_terms > 1`` each row counts for the term it is assigned to
        (``assign_cells``).
    threshold : float, default=1e-3
        Exponents above this carry the metric (the package's participation threshold).

    Returns
    -------
    ndarray of shape (n_terms, n_features, n_features)
        Entry ``[k, i, j]`` is the tension of ``j`` against ``i`` on term ``k``: negative where
        both metrics carry an exponent on the term; ``0.0`` where ``i`` carries none and ``j``
        does (raising ``i`` moves nothing along the term); ``nan`` where ``j`` carries none (the
        derivative is undefined, so the cell is blank and not zero) and on the diagonal. Where both
        entries of a pair are nonzero, ``T[k, i, j] * T[k, j, i] = 1``. A term that owns no row has
        an all-``nan`` matrix.

    Notes
    -----
    At ``n_terms > 1`` the surface is the maximum of the terms, so each term has its own matrix;
    near a seam the two terms' values differ and neither is the surface's. The tension is a partial
    derivative along the fitted reference surface with the other metrics held, not the effect of
    changing a design variable.

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space import (
    ...     HyperbolicTradeSpace, make_frontier_data, tension_matrix)
    >>> X, _ = make_frontier_data(300, 3, random_state=0)
    >>> est = HyperbolicTradeSpace(temperature=20.0).fit(X)
    >>> T = tension_matrix(est, X)
    >>> T.shape
    (1, 3, 3)
    >>> bool((T[0][~np.eye(3, dtype=bool)] < 0).all())
    True
    """
    check_is_fitted(estimator)
    X = check_array(X, dtype=np.float64, ensure_min_features=1)
    if X.shape[1] != estimator.n_features_in_:
        raise ValueError(
            f"X has {X.shape[1]} features, but the estimator expects {estimator.n_features_in_}"
        )
    if (X < 0).any():
        raise ValueError("Negative values in data")
    W = np.atleast_2d(estimator.exponents_)
    K, d = W.shape
    tau = float(estimator.temperature)
    keep = (X > 0).all(axis=1)
    U = np.log(X[keep])
    cells = estimator.assign_cells(X)[keep]
    out = np.full((K, d, d), np.nan)
    for k in range(K):
        rows = cells == k
        if not rows.any():
            continue
        out[k] = _tension_cells(W[k], _balanced_point(U[rows], W[k], tau), threshold)
    return out


@dataclass(frozen=True, eq=False)
class DesignTensions:
    """What ``design_tensions`` returns: the tensions at each design's own metric ratios.

    Attributes
    ----------
    term : ndarray of int, shape (n,)
        The term each design belongs to (``assign_cells``); ``-1`` for a row with a zero metric.
    tensions : ndarray of shape (n, d, d)
        The tension matrix of the design's own term at the design's metrics, in the metrics'
        units (cells as in :func:`tension_matrix`); all ``nan`` for a row with a zero metric.
    by_term : ndarray of shape (n, n_terms, d, d)
        The same formula for every term at the design's metrics: the other terms' values, reported
        beside the design's own and never merged with it.
    margin : ndarray of shape (n,)
        The design's score on its own term less its score on the next best term, a measure of its
        nearness to a seam (``inf`` at one term).
    attribute_tensions : ndarray of shape (n, d, d) or None
        ``ds_j / ds_i`` in the attributes' own units, the same cells, on the design's own term,
        when ``preconditioner`` and ``attributes`` were given; else ``None``.
    attribute_by_term : ndarray of shape (n, n_terms, d, d) or None
        The attributes' units for every term, as ``by_term`` is for the metrics.
    """

    term: np.ndarray
    tensions: np.ndarray
    by_term: np.ndarray
    margin: np.ndarray
    attribute_tensions: np.ndarray | None
    attribute_by_term: np.ndarray | None = None


def design_tensions(estimator, X, preconditioner=None, attributes=None, threshold=1e-3):
    """The tensions at each design's own metric ratios, on the term it belongs to (from the data).

    The formula of :func:`tension_matrix` evaluated at the design's own metrics ``m`` instead of a
    term's balanced point. The level of the design does not matter: a level set is the surface
    scaled (Theorem 1), which leaves the ratios ``m_j / m_i`` alone. With the fitted
    ``preconditioner`` and the designs' raw ``attributes`` the tensions are also given in the
    attributes' own units, through the conditioning ``log m_j = alpha_j log(a_j + s_j) + b_j``::

        d s_j / d s_i = -(w_i alpha_i) / (w_j alpha_j) (a_j + s_j) / (a_i + s_i)

    Its sign is minus the sign of ``alpha_i alpha_j``: negative for two attributes of one
    orientation, positive for mixed orientation.

    Parameters
    ----------
    estimator : HyperbolicTradeSpace
        Fitted estimator.
    X : array-like of shape (n_samples, n_features)
        The designs' metrics (nonnegative).
    preconditioner : LogAffinePreconditioner, optional
        The fitted conditioning that produced ``X`` from ``attributes``.
    attributes : array-like of shape (n_samples, n_features), optional
        The designs' raw attributes, the input of ``preconditioner``.
    threshold : float, default=1e-3
        Exponents above this carry the metric.

    Returns
    -------
    DesignTensions

    Raises
    ------
    ValueError
        If only one of ``preconditioner`` and ``attributes`` is given, or the shapes disagree.

    Notes
    -----
    A tension is a rate along the fitted reference surface with the other metrics held. For metrics
    that move together in the data (a fleet's cost is the unit cost times its size) it is not a
    move a design can make, and it is never the effect of changing a design variable.

    Examples
    --------
    >>> import numpy as np
    >>> from hyperbolic_trade_space import (
    ...     HyperbolicTradeSpace, design_tensions, make_frontier_data)
    >>> X, _ = make_frontier_data(300, 3, random_state=0)
    >>> est = HyperbolicTradeSpace(temperature=20.0).fit(X)
    >>> dt = design_tensions(est, X[:2])
    >>> dt.tensions.shape, dt.term.tolist()
    ((2, 3, 3), [0, 0])
    >>> bool(np.allclose(dt.tensions[:, 0, 1] * dt.tensions[:, 1, 0], 1.0))
    True
    """
    check_is_fitted(estimator)
    if (preconditioner is None) != (attributes is None):
        raise ValueError("give both preconditioner and attributes, or neither")
    X = check_array(X, dtype=np.float64, ensure_min_features=1)
    n, d = X.shape
    if d != estimator.n_features_in_:
        raise ValueError(
            f"X has {d} features, but the estimator expects {estimator.n_features_in_}"
        )
    if (X < 0).any():
        raise ValueError("Negative values in data")
    W = np.atleast_2d(estimator.exponents_)
    K = W.shape[0]
    keep = (X > 0).all(axis=1)
    U = np.log(np.where(keep[:, None], X, 1.0))
    scores = U @ W.T - np.asarray(estimator.log_offset_, dtype=float)[None, :]
    term = np.where(keep, np.argmax(scores, axis=1), -1)
    by_term = np.stack([_tension_cells(W[k], U, threshold) for k in range(K)], axis=1)
    by_term[~keep] = np.nan
    own = np.where(keep, term, 0)
    tensions = by_term[np.arange(n), own]
    srt = np.sort(scores, axis=1)[:, ::-1]
    margin = srt[:, 0] - srt[:, 1] if K > 1 else np.full(n, np.inf)
    margin = np.where(keep, margin, np.nan)

    attribute = attribute_own = None
    if preconditioner is not None:
        check_is_fitted(preconditioner, "log_scale_")
        S = check_array(attributes, dtype=np.float64, ensure_min_features=1)
        if S.shape != X.shape:
            raise ValueError(f"attributes have shape {S.shape}, but X has shape {X.shape}")
        alpha = np.asarray(preconditioner.orientation_, float) / np.asarray(
            preconditioner.log_scale_, float
        )
        x = S + np.asarray(preconditioner.shift_, float)[None, :]
        attribute = np.full((n, K, d, d), np.nan)
        for k in range(K):
            wa = W[k] * alpha
            part = W[k] > threshold
            with np.errstate(divide="ignore", invalid="ignore"):
                TA = -(wa[:, None] / wa[None, :]) * (x[:, None, :] / x[:, :, None])
            TA = np.where(part[None, :, None], TA, 0.0)
            TA = np.where(part[None, None, :], TA, np.nan)
            TA[:, np.arange(d), np.arange(d)] = np.nan
            attribute[keep, k] = TA[keep]
        attribute_own = attribute[np.arange(n), own]
        attribute_own[~keep] = np.nan
    return DesignTensions(
        term=term.astype(int),
        tensions=tensions,
        by_term=by_term,
        margin=margin,
        attribute_tensions=attribute_own,
        attribute_by_term=attribute,
    )
