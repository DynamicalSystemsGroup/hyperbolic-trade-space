# ruff: noqa  (a record script of the WP30 data gate, kept as run; not part of the package)
"""WP23 data gate, D-9 part 3: the conclusions, computed by the case's own functions.

Three configurations through ``case.py`` at dev 8507bd9, defaults unchanged:

* ``old10``: the old v2 files (byte-equal to the frozen generation the paper reads) with the
  paper's ten-metric ``CUBESAT`` spec: the paper's numbers as committed;
* ``old9``: the old files with the nine-metric spec (slew time out): the column change alone;
* ``new9``: the new files with the nine-metric spec: the regeneration of record.

Usage: ``uv run python conclusions.py <old data dir> <new repo root> <out.json>``.
"""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "examples" / "adcs"))
import case  # noqa: E402

OLD = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[3])
NEW_DATA = ROOT / "examples" / "adcs" / "data" / "v2"

EIGHT = tuple(case.CUBESAT.attributes[:8])


def eight_spec(data_dir):
    """The WP23 close-out spec (eight metrics, four design variables, 90,643 USD launch budget)."""
    spec = case.CUBESAT
    return dataclasses.replace(
        spec,
        data_dir=Path(data_dir),
        attributes=EIGHT,
        short={a: spec.short[a] for a in EIGHT},
        units={a: spec.units[a] for a in EIGHT},
        orientation={a: spec.orientation[a] for a in EIGHT},
        subsystems={a: spec.subsystems[a] for a in EIGHT},
        design_vars=spec.design_vars[:4],
        requirements={**spec.requirements, "total_mass_kg": (90643.0 / 6000.0, "kg")},
    )


CONFIGS = {
    "old8": eight_spec(OLD),
    "new8": eight_spec(NEW_DATA),
    "new13": dataclasses.replace(case.CUBESAT, data_dir=NEW_DATA),
}


def j(x):
    if isinstance(x, (np.floating, float)):
        return float(x)
    if isinstance(x, (np.integer, int)):
        return int(x)
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    return x


def df_rows(df):
    return [{k: j(v) for k, v in r.items()} for r in df.to_dict("records")]


def top(names, w, n=3):
    order = np.argsort(-np.asarray(w))[:n]
    return [(names[i], float(w[i])) for i in order]


def near_counts(study, est, band):
    """Near-frontier rows per term at a band, from the estimator (no report)."""
    labels = est.cell_ if est.n_terms > 1 else np.zeros(len(study.M), int)
    near = np.abs(est.training_log_v_) < band
    return [int(((labels == k) & near).sum()) for k in range(est.n_terms)]


def term_report(study, fits, K):
    """facet_table at the K = 1 band, else at the fit's own band, else the refusals."""
    out = {"K": K}
    try:
        out["table"] = df_rows(case.term_table(study, fits, K=K))
        out["band"] = f"K = 1 band 1/tau = {fits[1].band:.5g}"
        return out
    except ValueError as first:
        out["refused_at_k1_band"] = str(first)
    try:
        out["table"] = df_rows(case.term_table(study, {K: fits[K]}, K=K))
        out["band"] = f"the K = {K} fit's own band 1/tau = {fits[K].band:.5g}"
    except ValueError as second:
        out["refused_at_own_band"] = str(second)
        out["table"] = None
    return out


def regime_block(study, fits):
    names = study.names
    b = {"n_raw": len(study.raw), "n_feasible": len(study.M), "metrics": names}
    for K, f in fits.items():
        e = f.estimator
        b[f"K{K}"] = {
            "tau": float(f.tau), "band": float(f.band), "frac_above_": float(e.frac_above_),
            "n_eff_": float(e.n_eff_), "objective_": float(e.objective_),
            "mean_slack_": float(e.mean_slack_),
            "exponents": [[float(w) for w in row] for row in np.atleast_2d(e.exponents_)],
            "leading": [top(names, row) for row in np.atleast_2d(e.exponents_)],
            "rows": [int(x) for x in (np.bincount(e.cell_, minlength=K) if K > 1 else [len(study.M)])],
            "shares": [float(x) for x in (e.term_share_ if K > 1 else [1.0])],
            "reach": [float(x) for x in np.atleast_1d(e.log_offset_)],
            "near_at_k1_band": near_counts(study, e, fits[1].band),
            "near_at_own_band": near_counts(study, e, f.band),
            "certificate": {k: j(v) for k, v in case._lib()[1].certificate(e).items()},
        }  # fmt: skip
    # K = 1 report (the contending set)
    try:
        b["K1"]["report"] = df_rows(case.tension_table(study, fits[1]))[0]
    except ValueError as exc:
        b["K1"]["report_refused"] = str(exc)
    for K in (2, 3):
        b[f"K{K}"]["report"] = term_report(study, fits, K)
    b["mean_slack_by_k"] = df_rows(case.mean_slack_by_k(study, fits))
    b["mean_slack_fixed_tau"] = df_rows(case.mean_slack_fixed_tau(study, fits))
    b["association"] = df_rows(case.association_table(study, fits[1]))
    # the two redundancies among the feasible designs (Spearman of the raw attributes)
    f = study.feasible
    b["redundancy_spearman"] = {
        "power margin, energy balance": float(
            f["power_margin_w"].corr(f["energy_balance_wh"], method="spearman")
        ),
        "available power, energy balance": float(
            f["available_power_w"].corr(f["energy_balance_wh"], method="spearman")
        )
        if "available_power_w" in f
        else None,
        "battery peak power ratio, depth of discharge": float(
            f["battery_peak_power_ratio"].corr(f["dod_eclipse"], method="spearman")
        )
        if "battery_peak_power_ratio" in f
        else None,
    }
    b["nondominated"] = df_rows(case.nondominated_counts(study))
    return b


result = {}
for cname, spec in CONFIGS.items():
    print(f"== {cname}: {spec.data_dir} ({len(spec.attributes)} metrics)", flush=True)
    block = {"data_dir": str(spec.data_dir), "metrics": [spec.short[a] for a in spec.attributes]}
    studies = {r: case.load_study(r, spec) for r in spec.regimes}
    fits = {r: case.k_fits(s) for r, s in studies.items()}
    for r in spec.regimes:
        block[r] = regime_block(studies[r], fits[r])
        print(
            f"   {r}: K1 tau {fits[r][1].tau:.2f}, K2 {fits[r][2].tau:.2f}, K3 {fits[r][3].tau:.2f}",
            flush=True,
        )
    block["regime_comparison"] = df_rows(case.regime_comparison(spec))
    prim = studies["primary"]
    block["candidates"] = df_rows(case.candidate_table(prim, fits["primary"][1]))
    # propose-predict-check: the recorded predictions are on the view of their own generation
    # (old files: the slew-time view; new files: the settling-time view), so old9 has no check
    if True:
        reg = case.fit_regressor(prim)
        pc = case.predict_check(prim, reg)
        block["predict_check"] = {
            "tau": float(reg.tau),
            "band": float(1 / reg.tau),
            "rows": df_rows(pc),
        }
        block["proposals_refit"] = df_rows(case.proposals_table(prim, reg))
        print(f"   regressor tau {reg.tau:.3f}", flush=True)
    preds = pd.read_csv(spec.data_dir / spec.predictions_file)
    block["predictions_file"] = df_rows(
        preds[
            [
                "name",
                "wheel_class",
                "st_grade",
                "hole_score",
                "distance_to_target",
                "tau",
                "band",
                "pred_log_v",
            ]
        ]
    )
    checks = pd.read_csv(spec.data_dir / spec.checks_file)
    block["checks_file_flags"] = df_rows(
        checks[
            [
                "name",
                "role",
                "settled",
                "momentum_ok",
                "power_ok",
                "dod_ok",
                "settling_time_s",
                "dod_eclipse",
                "battery_wh",
            ]
        ]
    )
    result[cname] = block

OUT.write_text(json.dumps(result, indent=1))
print(f"wrote {OUT}")
