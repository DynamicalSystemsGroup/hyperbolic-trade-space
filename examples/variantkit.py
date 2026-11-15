"""Shared steps of the WP59 variant scripts: one fit-and-read for a conditioned table, the
quantile map, and the PCA and ICA rewritings of a table of metrics.

Nothing here is imported by the package; ``examples/<case>/variants.py`` import it from their
parent folder, as ``run.py`` imports ``fitkit``. The fit is the one ``fitkit.fit_read`` makes (same
temperature rule, same seeds), without its table over temperatures.
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path

import numpy as np


def quantile_metrics(A, orient):
    """Metrics from the ranks of each attribute: positive, larger is better.

    Each column ``o * a`` (``o`` the orientation, +1 or -1) goes through scikit-learn's
    ``QuantileTransformer`` with a uniform output ``q`` in [0, 1]. The uniform value is shifted
    into [1/n, 1] by ``u = 1/n + (1 - 1/n) q`` and the metric is ``m = exp(u)``, so the
    log-metric is ``u``, a rank on a unit interval, and the metric is positive.
    """
    from sklearn.preprocessing import QuantileTransformer

    A = np.asarray(A, float) * np.asarray(orient, float)
    n = A.shape[0]
    q = QuantileTransformer(
        n_quantiles=min(1000, n), output_distribution="uniform", random_state=0
    ).fit_transform(A)
    return np.exp(1.0 / n + (1.0 - 1.0 / n) * q)


def _num(x):
    x = float(x)
    return None if not math.isfinite(x) else x


def fit_variant(M, names, k2=True, target=0.10, seed=0):
    """Fit conditioned metrics at the temperature that puts ``target`` of rows above the surface.

    Returns a JSON-ready dict: rows, tau, K = 1 exponents, the contending set at tau = infinity and
    its exponents, elasticities and near-frontier association (every pair), the band, the loadings
    of the first spread direction, and K = 2 (shares, exponents per term, mean slack, the sets).
    A failure is recorded under ``error``; nothing is written to stderr.
    """
    from hyperbolic_trade_space import HyperbolicTradeSpace, select_temperature, trade_off_report

    M = np.asarray(M, float)
    names = list(names)
    d = len(names)
    out = {"rows": int(M.shape[0]), "metrics": names}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            tau = float(select_temperature(M, target_frac_above=target, bounds=(3.0, 1e4)))
            est = HyperbolicTradeSpace(temperature=tau, random_state=seed).fit(M)
            rep = trade_off_report(est, M)
        except Exception as err:  # recorded, not raised: a variant that cannot be fit is a finding
            out["error"] = f"{type(err).__name__}: {str(err)[:200]}"
            return out
        out.update(
            tau=tau,
            band=float(rep.band),
            frac_above=float(est.frac_above_),
            n_eff=float(est.n_eff_),
            exponents=dict(zip(names, map(float, est.exponents_[0]), strict=True)),
            contending_set=[names[j] for j in rep.contending_set],
            n_lemma=int(rep.n_lemma),
            contending_exponents=dict(
                zip(
                    [names[j] for j in rep.contending_set],
                    map(float, rep.contending_exponents),
                    strict=True,
                )
            ),
            n_near_frontier=int(rep.n_near_frontier),
            elasticities={
                f"{names[j]}|{names[k]}": _num(rep.elasticities[j, k])
                for j in range(d)
                for k in range(d)
                if j != k
            },
            association={
                f"{names[i]}|{names[j]}": _num(rep.association[i, j])
                for i in range(d)
                for j in range(i + 1, d)
            },
        )
        if rep.spread_loadings.shape[0]:
            out["spread_first_direction"] = {
                "loadings": dict(zip(names, map(float, rep.spread_loadings[0]), strict=True)),
                "explained": float(rep.explained_spread[0]),
            }
        if k2 and M.shape[0] >= 40:
            try:
                e2 = HyperbolicTradeSpace(
                    n_terms=2, temperature=tau, random_state=seed, n_restarts=5
                ).fit(M)
                share = [float(s) for s in e2.term_share_]
                terms = [dict(zip(names, map(float, w), strict=True)) for w in e2.exponents_]
                second = int(np.argmin(share))
                try:
                    sets = [[names[j] for j in r.contending_set] for r in trade_off_report(e2, M)]
                except ValueError as err:
                    sets = str(err)[:200]
                out["k2"] = {
                    "shares": share,
                    "terms": terms,
                    "second_term_index": second,
                    "second_term_share": share[second],
                    "second_term_exponents": terms[second],
                    "mean_slack": float(e2.mean_slack_),
                    "mean_slack_k1": float(est.mean_slack_),
                    "contending_sets": sets,
                    "status": getattr(e2.termination_, "status", None),
                }
            except Exception as err:
                out["k2"] = {"error": f"{type(err).__name__}: {str(err)[:200]}"}
    return out


def signed_scores(Z, kind, k, seed=0):
    """The first ``k`` PCA or ICA scores of the log-metrics ``Z``, as positive metrics.

    ``Z`` holds the conditioned log-metrics (one column per metric). Each score is the projection
    on a component, centred, divided by its standard deviation (so the log-score has unit spread,
    as the standard scaler gives the metrics), and exponentiated: ``m = exp(score)``. The sign of
    each component is chosen so that its largest absolute loading is positive. Returns the metrics,
    the loadings (components by metrics, signed) and, for PCA, the explained variance ratios.
    """
    from sklearn.decomposition import PCA, FastICA

    if kind == "pca":
        model = PCA(n_components=k, svd_solver="full").fit(Z)
        W = model.components_
        ratios = [float(r) for r in model.explained_variance_ratio_]
    else:
        model = FastICA(
            n_components=k, whiten="unit-variance", random_state=seed, max_iter=2000, tol=1e-4
        ).fit(Z)
        W = model.components_
        ratios = None
    S = (Z - Z.mean(0)) @ W.T
    sign = np.sign(W[np.arange(k), np.abs(W).argmax(axis=1)])
    W, S = W * sign[:, None], S * sign[None, :]
    S = (S - S.mean(0)) / S.std(0)
    W = W / np.linalg.norm(W, axis=1, keepdims=True)
    return np.exp(S), W, ratios


def communality(Z, k=2):
    """Share of each column's variance carried by the first ``k`` principal components of ``Z``.

    ``Z`` is standardised first, so the shares are comparable across columns.
    """
    from sklearn.decomposition import PCA

    Zs = (Z - Z.mean(0)) / Z.std(0)
    p = PCA(n_components=k, svd_solver="full").fit(Zs)
    load = p.components_.T * np.sqrt(p.explained_variance_)
    return (load**2).sum(axis=1) / Zs.var(0, ddof=1), p


def dump(result, path):
    """Write a result dict as sorted, indented JSON."""
    Path(path).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
