"""The fit-and-read routine of the WP70 case studies.

The routine of ``examples/fitkit.py`` with one change: the near-frontier band is ``1 / tau`` unless
that holds fewer than ``MIN_NEAR`` rows, in which case it is widened to the smallest band that
holds them, and the widening is recorded (a portfolio of a hundred-odd projects at a tenth above
the frontier often leaves fewer than ten rows inside ``1 / tau``).
"""

from __future__ import annotations

import warnings

import numpy as np

MIN_NEAR = 15


def _band(log_v, tau, k=MIN_NEAR):
    """``1 / tau``, or the smallest band holding ``k`` rows when that is wider."""
    a = np.sort(np.abs(log_v[np.isfinite(log_v)]))
    need = float(a[min(k, len(a)) - 1]) * 1.0001 if len(a) else np.inf
    return max(1.0 / tau, need)


def _report(est, M, names, band):
    from hyperbolic_trade_space import trade_off_report

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rep = trade_off_report(est, M, band=band, min_near_frontier=min(MIN_NEAR, 10))
    one = rep if not isinstance(rep, list) else None
    reps = [rep] if one is not None else rep
    out = []
    for r in reps:
        out.append(
            {
                "contending_set": [names[j] for j in r.contending_set],
                "contending_exponents": [float(v) for v in r.contending_exponents],
                "n_lemma": int(r.n_lemma),
                "band": float(r.band),
                "n_near_frontier": int(r.n_near_frontier),
                "association": {
                    f"{names[i]}|{names[j]}": float(r.association[i, j])
                    for i in range(len(names))
                    for j in range(i + 1, len(names))
                },
            }
        )
    return rep, out


def fit_read(M, names, target=0.10, k2=True, seed=0):
    """Temperature, K = 1 and K = 2 fits, and the trade-off report, as a JSON-ready dict."""
    from hyperbolic_trade_space import HyperbolicTradeSpace, select_temperature

    M = np.asarray(M, float)
    names = list(names)
    tau = float(select_temperature(M, target_frac_above=target, bounds=(3.0, 1e4)))
    est = HyperbolicTradeSpace(temperature=tau, random_state=seed).fit(M)
    band = _band(est.training_log_v_, tau)
    _, rep = _report(est, M, names, band)
    out = {
        "n": int(M.shape[0]),
        "metrics": names,
        "tau_selected": tau,
        "frac_above": float(est.frac_above_),
        "exponents_k1": dict(zip(names, map(float, est.exponents_[0]), strict=True)),
        "band_widened": bool(band > 1.0 / tau),
        "mean_slack_k1": float(est.mean_slack_),
        **rep[0],
    }
    if k2 and M.shape[0] >= 40:
        e2 = HyperbolicTradeSpace(n_terms=2, temperature=tau, random_state=seed, n_restarts=5).fit(
            M
        )
        k2out = {
            "exponents": [dict(zip(names, map(float, w), strict=True)) for w in e2.exponents_],
            "term_share": [float(s) for s in e2.term_share_],
            "mean_slack": float(e2.mean_slack_),
            "status": getattr(e2.termination_, "status", None),
        }
        try:
            _, r2 = _report(e2, M, names, max(1.0 / tau, band))
            k2out["terms"] = r2
        except ValueError as err:
            k2out["terms"] = str(err)[:200]
        out["k2"] = k2out
    return out
