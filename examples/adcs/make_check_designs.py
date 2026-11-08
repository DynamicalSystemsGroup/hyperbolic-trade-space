"""Propose, predict, then check: the six check designs of the ADCS notebook (WP7, D-3).

Two stages, run once, in this order and committed in this order (the predictions file is committed
before the simulation results exist)::

    REQUIRE_OPENSYSML=1 uv run python examples/adcs/make_check_designs.py predict
    REQUIRE_OPENSYSML=1 uv run python examples/adcs/make_check_designs.py simulate

``predict`` fits a ``TradeSpaceRegressor`` (Gaussian process on the configuration -> chart
coordinates ``[Z | log V]``) on the feasible designs of the primary dataset
(``adcs_designs_cubesat_gains.csv``; feasible = settled and power_ok and momentum_ok), with the
trade space fitted on the four metrics slew time, pointing error, control effort and total mass
(a subset view: hole finding supports up to three chart coordinates). It takes the most isolated,
well-separated holes of the data's chart, maps each to the configuration (from a seeded pool of
random draws inside the aggressive gain box and the model's variable ranges) whose predicted
``[Z | log V]`` is nearest the target ``(Z_hole, 0)``, and writes the three proposals with their
predictions (log V, Z and ``predict_std``) to ``data/check_predictions_cubesat.csv``. The three
hand-written candidates (a fast effort-hungry design, a precise heavy-sensor design, a light slow
design) are fixed in ``CANDIDATES`` below; they are not predicted.

``simulate`` reads the candidates and the committed proposals and measures all six once through
``cubesat_model.measure`` with the aggressive gain-box option (needs the opensysml runtime), and
writes ``data/check_designs_cubesat.csv`` (column ``role``: candidate or proposal). The notebook
only reads the two files; it never simulates and never regenerates them.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DATA = HERE / "data"
PRIMARY = DATA / "adcs_designs_cubesat_gains.csv"
PREDICTIONS = DATA / "check_predictions_cubesat.csv"
CHECKS = DATA / "check_designs_cubesat.csv"

SEED = 20261108
POOL = 100000
REACH = 0.35  # predicted [Z | 2 log V] distance within which a hole counts as reachable
METRICS = ["slew_time_s", "pointing_error_deg", "control_effort", "total_mass_kg"]
ATTRIBUTES = [
    "settling_time_s",
    "slew_time_s",
    "pointing_error_deg",
    "total_mass_kg",
    "control_effort",
    "power_margin_w",
    "energy_balance_wh",
    "eclipse_reserve_wh",
    "peak_slew_power_w",
    "dod_eclipse",
]
CONFIG = ["panel_span_m", "battery_wh", "wheel_class", "st_grade", "Kp", "Kd"]
WHEELS = ["small", "medium", "large"]
TRACKERS = ["coarse", "medium", "fine"]
# Hand-written candidates, inside the aggressive gain box (Kp 0.2-2.0, Kd 0.3-1.5) and the model
# ranges (panel span 0.3-1.0 m, battery 20-200 Wh).
CANDIDATES = [
    dict(name="fast_effort_hungry", wheel_class="large", st_grade="medium", panel_span_m=0.55,
         battery_wh=90.0, Kp=1.8, Kd=1.4),
    dict(name="precise_heavy_sensor", wheel_class="medium", st_grade="fine", panel_span_m=0.8,
         battery_wh=140.0, Kp=1.2, Kd=1.0),
    dict(name="light_slow", wheel_class="small", st_grade="coarse", panel_span_m=0.35,
         battery_wh=40.0, Kp=0.25, Kd=0.4),
]  # fmt: skip


def feasible_primary() -> pd.DataFrame:
    df = pd.read_csv(PRIMARY)
    ok = df.settled & df.power_ok & df.momentum_ok & (df[ATTRIBUTES] > 0).all(axis=1)
    return df[ok].reset_index(drop=True)


def features(df: pd.DataFrame, ranges: dict) -> np.ndarray:
    """Configuration -> regressor features in [0, 1]: log-scaled continuous, ordinal categories."""
    cols = []
    for c in ["panel_span_m", "battery_wh", "Kp", "Kd"]:
        lo, hi = ranges[c]
        cols.append((np.log(df[c].to_numpy(float)) - np.log(lo)) / (np.log(hi) - np.log(lo)))
    cols.append(df["wheel_class"].map({w: i / 2 for i, w in enumerate(WHEELS)}).to_numpy(float))
    cols.append(df["st_grade"].map({t: i / 2 for i, t in enumerate(TRACKERS)}).to_numpy(float))
    return np.column_stack(cols)


def model_ranges() -> dict:
    from cubesat_model import load_model

    m = load_model(gain_box="aggressive")
    return {
        "panel_span_m": tuple(m.panel_span_range),
        "battery_wh": tuple(m.battery_wh_range),
        "Kp": tuple(m.kp_range),
        "Kd": tuple(m.kd_range),
    }


def predict() -> pd.DataFrame:
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
    from sklearn.pipeline import make_pipeline

    from hyperbolic_trade_space import (
        HyperbolicTradeSpace,
        LogAffinePreconditioner,
        TradeSpaceRegressor,
        select_temperature,
    )
    from hyperbolic_trade_space.gaps import find_holes

    ranges = model_ranges()
    fe = feasible_primary()
    Y = fe[METRICS].to_numpy(float)
    pre = LogAffinePreconditioner(orientation=[-1] * len(METRICS), scaler="standard")
    tau = select_temperature(pre.fit_transform(Y), target_frac_above=0.10, bounds=(3, 1e3))
    ts = make_pipeline(
        LogAffinePreconditioner(orientation=[-1] * len(METRICS), scaler="standard"),
        HyperbolicTradeSpace(temperature=tau),
    )
    gp = GaussianProcessRegressor(
        kernel=ConstantKernel(1.0) * RBF(length_scale=np.ones(6)) + WhiteKernel(0.1),
        normalize_y=True,
        n_restarts_optimizer=2,
        random_state=0,
    )
    reg = TradeSpaceRegressor(gp, ts).fit(features(fe, ranges), Y)
    chart = reg.trade_space_.transform(Y)  # [Z | log V] of the data
    Z_data = chart[:, :-1]
    holes, scores = find_holes(Z_data, resolution=30, threshold=2.0)

    # Holes are candidates, not verdicts: some lie where no configuration of the box reaches. Take
    # the most isolated holes (up to 300) whose best configuration in the seeded pool is predicted
    # within REACH of (Z_hole, 0), then three of them separated by 1.5 median NN distances.
    from scipy.spatial import cKDTree

    nn = cKDTree(Z_data).query(Z_data, k=2)[0][:, 1]
    sep = 1.5 * float(np.median(nn))
    rng = np.random.default_rng(SEED)
    pool = pd.DataFrame(
        {
            "panel_span_m": np.exp(rng.uniform(*np.log(ranges["panel_span_m"]), POOL)),
            "battery_wh": np.exp(rng.uniform(*np.log(ranges["battery_wh"]), POOL)),
            "Kp": np.exp(rng.uniform(*np.log(ranges["Kp"]), POOL)),
            "Kd": np.exp(rng.uniform(*np.log(ranges["Kd"]), POOL)),
            "wheel_class": rng.choice(WHEELS, POOL),
            "st_grade": rng.choice(TRACKERS, POOL),
        }
    )
    Fp = features(pool, ranges)
    Zp, lvp = reg.predict_coordinates(Fp)
    lvp = np.ravel(lvp)
    chosen, best_i, best_d, chosen_scores = [], [], [], []
    for h, sc in zip(holes[:300], scores[:300]):
        dist = np.sqrt(((Zp - h) ** 2).sum(axis=1) + (2 * lvp) ** 2)
        i = int(np.argmin(dist))
        if dist[i] > REACH or any(np.linalg.norm(h - c) <= sep for c in chosen):
            continue
        chosen.append(h)
        best_i.append(i)
        best_d.append(float(dist[i]))
        chosen_scores.append(float(sc))
        if len(chosen) == 3:
            break
    if len(chosen) < 3:
        raise RuntimeError("fewer than three reachable, separated holes; raise REACH")

    rows = []
    for k, h in enumerate(chosen):
        i = best_i[k]
        cfg = pool.iloc[[i]]
        z, lv = reg.predict_coordinates(features(cfg, ranges))
        zs, lvs = _std(reg, features(cfg, ranges), Z_data.shape[1])
        row = {"role": "proposal", "design_id": 1004 + k, "name": f"proposal_{k + 1}"}
        row.update(cfg.iloc[0].to_dict())
        for j in range(Z_data.shape[1]):
            row[f"target_z{j + 1}"] = float(h[j])
        for j in range(Z_data.shape[1]):
            row[f"pred_z{j + 1}"] = float(z[0, j])
        row["pred_log_v"] = float(np.ravel(lv)[0])
        for j in range(Z_data.shape[1]):
            row[f"pred_std_z{j + 1}"] = float(zs[j])
        row["pred_std_log_v"] = float(lvs)
        row["hole_score"] = chosen_scores[k]
        row["distance_to_target"] = best_d[k]
        row["tau"] = float(tau)
        row["band"] = 1.0 / float(tau)
        row["n_train"] = len(fe)
        rows.append(row)
    return pd.DataFrame(rows)


def _std(reg, F, p):
    """predict_std per output column ([Z | log V]); falls back on NaN if unavailable."""
    try:
        s = np.atleast_2d(np.asarray(reg.predict_std(F), float))
        return s[0, :p], s[0, p]
    except (AttributeError, ValueError, NotImplementedError):
        return np.full(p, np.nan), np.nan


def simulate() -> pd.DataFrame:
    import cubesat_model as cm

    props = pd.read_csv(PREDICTIONS)
    rows = []
    for k, c in enumerate(CANDIDATES):
        rows.append({"role": "candidate", "design_id": 1001 + k, **c})
    for _, r in props.iterrows():
        rows.append(
            {"role": "proposal", "design_id": int(r.design_id), "name": r["name"]}
            | {c: r[c] for c in CONFIG}
        )
    model = cm.load_model(gain_box="aggressive")
    out = []
    for r in rows:
        cfg = {c: r[c] for c in CONFIG} | {"design_id": r["design_id"], "seed": SEED}
        res = model.measure(cfg)
        out.append(r | {"seed": SEED} | res)
    df = pd.DataFrame(out)
    lead = ["role", "design_id", "name", "seed", *CONFIG, *ATTRIBUTES]
    flags = ["settled", "momentum_ok", "power_ok", "dod_ok", "torque_saturated_frac"]
    rest = [c for c in df.columns if c not in lead + flags]
    return df[lead + flags + rest]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("stage", choices=["predict", "simulate"])
    a = ap.parse_args(argv)
    if a.stage == "predict":
        df = predict()
        df.to_csv(PREDICTIONS, index=False, float_format="%.9g")
        print(df.T.to_string())
    else:
        if not PREDICTIONS.exists():
            raise SystemExit("run the predict stage and commit its output first")
        df = simulate()
        df.to_csv(CHECKS, index=False, float_format="%.9g")
        print(df.T.to_string())


if __name__ == "__main__":
    main()
