"""Tension report: which metrics contend, which move together, along which directions designs trade.

The model is built to find *tensions*, not variance. PCA picks the directions of largest spread
(where the data are free); the fit picks the positive combination ``w`` of log-metrics with the
smallest upper extent, the binding constraint among larger-is-better metrics. The
report reads that structure at three levels, all for the K = 1 fit (one tension; several regional
tensions are the K > 1 extension, below, and a deflation search for successive tensions is a
research question). At K > 1 the same three levels are read once per facet, on the rows assigned to
that facet (``assign_facets``), and a list of K
reports is returned:

1. **Participation and elasticities.** Metrics with ``w_j > threshold`` participate, the rest are
   free at the balanced point; the elasticity of metric ``k`` against metric ``j`` along the
   frontier is ``-w_k / w_j``.
2. **The contending set (n-lemma).** At ``tau = inf`` the fit is a linear program whose solution is
   sparse, with exact zero exponents; the support is the set of metrics that contend, of any size
   ``n`` and without a prior choice of which or how many. At a working finite ``tau`` the weights
   are smoothed, so small weights mean weak participation rather than membership. This reading needs
   ``min_exponent = 0``, since a positive floor masks the sparsity.
3. **Association and tension directions among near-frontier designs** (``|log V| < band``): the
   pairwise association of log-metrics (negative = traded, positive = aligned), and the PCA of the
   near-frontier chart coordinates ``Z`` whose principal directions are the exercised trade-offs,
   with loadings on the metrics through the chart basis.

Limits, stated here because the report cannot state them for you: a *tension* is a binding
constraint, a *correlation* is only a co-movement; near the frontier ``w . u`` is almost
constant, so the **closure effect** forces some negative association among participating metrics
even where no designer ever traded them; the result depends on the ``band``; and K = 1 finds
one facet (at K > 1 each facet's contending set is the ``tau = inf`` LP support on that facet's rows
centred on their mean, as in the facet refit, since the raw rows of one facet do not enclose the
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

__all__ = ["TensionReport", "tension_report"]

_CLOSURE_NOTE = (
    "Closure effect: near the frontier w . u is nearly constant, so a binding constraint induces "
    "negative association among participating metrics even where no designer traded them. Read "
    "negative association as tension only together with the exponents and the principal tension "
    "directions; positive association among participating metrics is the stronger evidence of "
    "alignment."
)
_NAMES = {1: "monolemma", 2: "dilemma", 3: "trilemma"}


@dataclass(frozen=True, eq=False)
class TensionReport:
    """Result of ``tension_report`` (immutable; arrays are not copied).

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
    tension_directions : ndarray of shape (d-1, d-1)
        Unit principal directions in chart coordinates ``Z`` of the near-frontier rows (rows).
    tension_loadings : ndarray of shape (d-1, d)
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
    tension_directions: np.ndarray
    tension_loadings: np.ndarray
    explained_spread: np.ndarray
    contending_set: np.ndarray
    contending_exponents: np.ndarray
    n_lemma: int
    lemma_name: str
    band: float
    n_near_frontier: int


def _lemma_name(n):
    return _NAMES.get(n, f"{n}-lemma")


def tension_report(
    estimator, X, band=None, min_near_frontier=10, threshold=1e-3, association="pearson"
):
    """Report the tensions of a fitted trade space (a list of K reports when ``n_terms = K > 1``).

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
    TensionReport or list of TensionReport
        One report at ``n_terms = 1``; at ``n_terms = K > 1`` a list of K, one per facet, each on
        the rows assigned to that facet with the facet's exponents, near-frontier rows
        (``|Phi_K| < band``), tension directions and loadings (through ``basis_[k]``).

    Raises
    ------
    ValueError
        If ``association`` is unknown or fewer than ``min_near_frontier`` rows are near the
        frontier; the message gives the ``band`` (and the fit temperature that matches it, since the
        default band is ``1 / tau``) that would hold ``min_near_frontier`` rows; at K > 1 it names
        the facet.

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
    ...     HyperbolicTradeSpace, make_frontier_data, tension_report)
    >>> X, _ = make_frontier_data(400, 3, random_state=0)
    >>> est = HyperbolicTradeSpace(temperature=np.inf).fit(X)
    >>> rep = tension_report(est, X)
    >>> rep.lemma_name, rep.contending_set.tolist(), rep.tension_directions.shape
    ('trilemma', [0, 1, 2], (2, 2))

    At ``n_terms = 3`` there is one report per facet:

    >>> W = [[.5, .5, 0, 0], [0, .5, .5, 0], [0, 0, .5, .5]]
    >>> X, _ = make_frontier_data(900, 4, exponents=W, n_terms=3, random_state=0)
    >>> est = HyperbolicTradeSpace(
    ...     n_terms=3, temperature=20.0, random_state=0).fit(X)
    >>> sorted(r.contending_set.tolist() for r in tension_report(est, X))
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
    lab = estimator.assign_facets(X)[finite]
    reports = []
    for k in range(K):
        r = lab == k
        Uk, wk, Bk = U[r], estimator.exponents_[k], estimator.basis_[k]
        reports.append(_report(Uk, Zf[r], lvf[r], wk, Uk - Uk.mean(0), Bk, *args, f"facet {k}: "))
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
            # the smallest band that holds min_near_frontier rows of this facet (strict inequality)
            need = float(np.nextafter(float(f"{have[min_near_frontier - 1]:.2g}"), np.inf))
            if need <= have[min_near_frontier - 1]:
                need = float(f"{have[min_near_frontier - 1] * 1.1:.2g}")
            hint = (
                f"use a larger band, band={need:g} (the smallest round band with "
                f"{min_near_frontier} rows on this facet), or fit at temperature={1.0 / need:.3g} "
                f"(the band is 1/temperature), or "
                f"lower min_near_frontier"
            )
        else:
            hint = (
                f"this facet owns only {have.size} usable rows; lower min_near_frontier to "
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

    return TensionReport(
        participating=participating,
        exponents=w,
        elasticities=rates,
        association=np.atleast_2d(assoc),
        association_kind=association,
        closure_note=_CLOSURE_NOTE,
        tension_directions=dirs,
        tension_loadings=load,
        explained_spread=evr,
        contending_set=support,
        contending_exponents=lp_w[support],
        n_lemma=n_lemma,
        lemma_name=_lemma_name(n_lemma),
        band=band,
        n_near_frontier=n_near,
    )
