"""Run the prototype on the case (primary regime) at K = 1 and K = 2, against finite differences.

    MPLCONFIGDIR=$(mktemp -d) uv run --frozen python work-packages/WP42-rounds/spike/case_run.py

Writes ``results.json`` and ``matrices.npz`` beside this file; the fits are recomputed
on every run (about a minute); nothing is cached on disk.

The finite-difference check treats the fitted estimator as a black box: ``score_samples`` is the
level (the fit's own function); for a step ``h`` in metric i it solves for the metric j that keeps
the level, and compares the central slope with the formula.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "examples" / "adcs"))
sys.path.insert(0, str(ROOT / "paper"))
sys.path.insert(0, str(HERE))

import case  # noqa: E402
import prototype as P  # noqa: E402


def load():
    """The case's study and its K = 1 and K = 2 fits, refitted on every run (no cache on disk)."""
    study = case.load_study("primary")
    return study, case.k_fits(study, (1, 2))


def level(est, m):
    return float(est.score_samples(np.asarray(m, float)[None])[0])


def fd_metric(est, m0, i, j, h=1e-4):
    """Central finite-difference slope d m_j / d m_i along the level set through ``m0``."""
    target = level(est, m0)
    out = []
    for sgn in (+1, -1):
        m = np.array(m0, float)
        m[i] *= 1 + sgn * h

        def f(lj, m=m):
            mm = m.copy()
            mm[j] = np.exp(lj)
            return level(est, mm) - target

        lj0 = np.log(m0[j])
        try:
            lj = brentq(f, lj0 - 0.05, lj0 + 0.05, xtol=1e-14, rtol=1e-14)
        except ValueError:
            return np.nan, None
        mm = m.copy()
        mm[j] = np.exp(lj)
        out.append((m[i], mm[j], tuple(est.assign_cells(mm[None]))))
    (xi1, xj1, c1), (xi2, xj2, c2) = out
    same_cell = c1 == c2
    return (xj1 - xj2) / (xi1 - xi2), same_cell


def fd_attribute(est, pre_t, raw0, attrs, i, j, h=1e-4):
    """Central FD slope d s_j / d s_i in attribute units (the raw columns), level held."""

    def lev(raw):
        return level(est, pre_t(raw))

    target = lev(raw0)
    out = []
    for sgn in (+1, -1):
        raw = np.array(raw0, float)
        raw[i] *= 1 + sgn * h

        def f(sj, raw=raw):
            r = raw.copy()
            r[j] = sj
            return lev(r) - target

        try:
            sj = brentq(f, raw0[j] * 0.9, raw0[j] * 1.1, xtol=1e-14 * raw0[j], rtol=1e-14)
        except ValueError:
            return np.nan
        out.append((raw[i], sj))
    (a1, b1), (a2, b2) = out
    return (b1 - b2) / (a1 - a2)


def check_matrix(est, k, u, T, rng_pairs=None):
    """Compare every nonblank, non-zero-by-threshold cell of ``T`` with FD; zero cells too."""
    m0 = np.exp(u)
    d = len(u)
    errs, rows = [], []
    for i in range(d):
        for j in range(d):
            if i == j or np.isnan(T[i, j]):
                continue
            fd, same = fd_metric(est, m0, i, j)
            if np.isnan(fd):
                continue
            rel = abs(fd - T[i, j]) / max(abs(T[i, j]), 1e-12) if T[i, j] != 0 else abs(fd)
            errs.append(rel)
            rows.append((i, j, float(T[i, j]), float(fd), float(rel), bool(same)))
    return rows


def main():
    study, fits = load()
    names = study.names
    alpha, a_shift = P.conditioning_of(study)
    out = {"names": list(names), "alpha": alpha.tolist(), "case": {}}
    npz = {}
    for K in (1, 2):
        est = fits[K].estimator
        tau = float(fits[K].tau)
        U = np.log(study.M)
        cells = est.assign_cells(study.M)
        W = est.exponents_
        res = {"tau": tau, "exponents": W.tolist(), "log_offset": est.log_offset_.tolist(),
               "terms": []}  # fmt: skip
        for k in range(len(W)):
            rows = U[cells == k]
            u_star = P.balanced_point(rows, W[k], tau)
            T = P.term_tension_matrix(W[k], u_star)
            E = P.elasticity_matrix(W[k])
            sc = W @ u_star - est.log_offset_
            assigned = int(np.argmax(sc))
            srt = np.sort(sc)[::-1]
            cmp = check_matrix(est, k, u_star, T)
            rel = np.array([r[4] for r in cmp])
            nonzero = np.array([r[2] != 0 for r in cmp])
            # elasticity from the formula in log-log form against the log-log FD
            res["terms"].append({
                "term": k + 1, "n_rows": len(rows),
                "balanced_point_log_metrics": u_star.tolist(),
                "level_at_balanced_point_own_score": float(W[k] @ u_star - est.log_offset_[k]),
                "assigned_term_at_balanced_point": assigned + 1,
                "score_margin_to_next": float(srt[0] - srt[1]) if len(srt) > 1 else None,
                "n_cells_nonblank": int(np.isfinite(T).sum() - 0),
                "n_cells_negative": int((T < 0).sum()),
                "n_cells_zero": int((T == 0).sum()),
                "n_cells_blank": int((np.isnan(T)).sum() - len(u_star)),
                "fd_cells_checked": len(cmp),
                "fd_max_rel_error_nonzero": float(rel[nonzero].max()) if nonzero.any() else None,
                "fd_max_abs_zero_cells": float(max([r[3] for r in cmp if r[2] == 0] or [0])),
                "fd_all_same_cell": all(r[5] for r in cmp),
            })  # fmt: skip
            npz[f"K{K}_term{k + 1}_T"] = T
            npz[f"K{K}_term{k + 1}_E"] = E
            npz[f"K{K}_term{k + 1}_u"] = u_star
        out["case"][f"K{K}"] = res

    # the picked design: between the operator's and the sponsor's measures (Section 9)
    from generate_findings import decision

    dec = decision(study, fits)
    pick = dec.picks["between"]
    idx = int(np.flatnonzero(study.feasible["design_id"].to_numpy() == pick["design_id"])[0])
    m_row = study.M[idx]
    raw_cols = list(study.spec.attributes)
    raw_row = study.feasible[raw_cols].to_numpy(float)[idx]
    pre = study.conditioner.named_transformers_["metrics"]
    est2 = fits[2].estimator
    des = P.design_tensions(est2, m_row, raw_row, alpha, a_shift)
    k = des["term"]
    pe = names.index("pointing error")
    uc = names.index("unit cost")
    fc = names.index("fleet cost")
    attrs = {n: c for n, c in zip(names, raw_cols, strict=True)}

    def to_metrics(raw):
        import pandas as pd

        return np.asarray(pre.transform(pd.DataFrame([np.asarray(raw, float)], columns=raw_cols)))[
            0
        ]

    class _Wrap:
        def __init__(self, e):
            self.e = e

    def pre_t(raw):
        return to_metrics(raw)

    pairs = {}
    for label, (i, j) in {
        "pointing error -> fleet cost": (pe, fc),
        "pointing error -> unit cost": (pe, uc),
        "fleet cost -> pointing error": (fc, pe),
        "unit cost -> pointing error": (uc, pe),
    }.items():
        t_m = float(des["T"][i, j])
        t_a = float(des["TA"][i, j])
        fd_m, same_m = fd_metric(est2, m_row, i, j)
        fd_a = fd_attribute(est2, pre_t, raw_row, raw_cols, i, j)
        other = {q + 1: float(M[i, j]) for q, M in des["other"].items()}
        pairs[label] = {
            "T_metrics": t_m, "fd_metrics": float(fd_m), "same_cell": bool(same_m),
            "T_attribute_units": t_a, "fd_attribute_units": float(fd_a),
            "T_metrics_other_term_same_ratios": other,
            "attribute_i": attrs[names[i]], "attribute_j": attrs[names[j]],
            "raw_i": float(raw_row[i]), "raw_j": float(raw_row[j]),
            "alpha_i": float(alpha[i]), "alpha_j": float(alpha[j]),
        }  # fmt: skip
    out["picked_design"] = {
        "design_id": str(pick["design_id"]),
        "configuration": f"{pick['wheel_class']} wheel, {pick['st_grade']} tracker, "
                         f"fleet {int(pick['fleet_size'])}",
        "term": k + 1, "score_margin_to_other_term": des["margin"],
        "level_log_V_K2": float(pick["log V K=2"]),
        "exponents_of_its_term": est2.exponents_[k].tolist(),
        "pairs": pairs,
    }  # fmt: skip
    # the same design at K = 1 (one term; no seam)
    est1 = fits[1].estimator
    des1 = P.design_tensions(est1, m_row, raw_row, alpha, a_shift)
    out["picked_design"]["K1"] = {
        lab: {"T_metrics": float(des1["T"][i, j]), "T_attribute_units": float(des1["TA"][i, j])}
        for lab, (i, j) in {"pointing error -> fleet cost": (pe, fc),
                            "pointing error -> unit cost": (pe, uc)}.items()
    }  # fmt: skip
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    np.savez(HERE / "matrices.npz", names=np.array(names), **npz)
    print(json.dumps(out["picked_design"], indent=1)[:3000])
    for K in ("K1", "K2"):
        for t in out["case"][K]["terms"]:
            print(K, {k: v for k, v in t.items() if k != "balanced_point_log_metrics"})


if __name__ == "__main__":
    main()
