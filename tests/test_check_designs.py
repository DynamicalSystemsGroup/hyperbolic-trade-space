"""Checks on the cached check designs (WP7, D-3); reads only the two committed CSV files."""

import pathlib

import pandas as pd

DATA = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs" / "data"
CHECKS = DATA / "check_designs_cubesat.csv"
PREDS = DATA / "check_predictions_cubesat.csv"
ATTRS = [
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
FLAGS = ["settled", "momentum_ok", "power_ok", "dod_ok"]


def test_check_designs_rows_and_roles():
    df = pd.read_csv(CHECKS)
    assert len(df) == 6
    assert (df.role == "candidate").sum() == 3
    assert (df.role == "proposal").sum() == 3
    assert df.design_id.is_unique
    for col in ["role", "design_id", *CONFIG, *ATTRS, *FLAGS]:
        assert col in df.columns


def test_check_designs_inside_the_aggressive_box_and_ranges():
    df = pd.read_csv(CHECKS)
    assert df.Kp.between(0.2, 2.0).all() and df.Kd.between(0.3, 1.5).all()
    assert df.panel_span_m.between(0.3, 1.0).all() and df.battery_wh.between(20, 200).all()


def test_predictions_recorded_for_the_proposals_only():
    preds = pd.read_csv(PREDS)
    assert len(preds) == 3 and (preds.role == "proposal").all()
    for col in [
        "pred_log_v",
        "pred_z1",
        "pred_std_slew_time_s",
        "pred_std_total_mass_kg",
        "tau",
        "band",
        *CONFIG,
    ]:
        assert col in preds.columns
    checks = pd.read_csv(CHECKS)
    prop = checks[checks.role == "proposal"].set_index("design_id")
    assert set(prop.index) == set(preds.design_id)
    # the simulated proposals use exactly the configurations that were predicted
    for _, r in preds.iterrows():
        for c in ["panel_span_m", "battery_wh", "Kp", "Kd"]:
            assert abs(prop.loc[r.design_id, c] - r[c]) <= 1e-6 * abs(r[c])
        assert prop.loc[r.design_id, "wheel_class"] == r.wheel_class
    # predictions carry no measured attribute columns (they were fixed before the simulation)
    assert not set(ATTRS) & set(preds.columns)


def _small_regressor():
    """A TradeSpaceRegressor fitted on 12 rows of two metrics (a GP on three features)."""
    import numpy as np
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
    from sklearn.pipeline import make_pipeline

    from hyperbolic_trade_space import (
        HyperbolicTradeSpace,
        LogAffinePreconditioner,
        TradeSpaceRegressor,
    )

    rng = np.random.default_rng(0)
    X = rng.uniform(size=(12, 3))
    Y = np.exp(np.column_stack([X[:, 0] - X[:, 1], X[:, 1] + 0.3 * X[:, 2]]))
    ts = make_pipeline(
        LogAffinePreconditioner(orientation=[-1, -1], scaler="standard"),
        HyperbolicTradeSpace(temperature=5.0),
    )
    gp = GaussianProcessRegressor(
        kernel=ConstantKernel(1.0) * RBF(np.ones(3)) + WhiteKernel(0.1), normalize_y=True
    )
    return TradeSpaceRegressor(gp, ts).fit(X, Y), rng.uniform(size=(10, 3))


def test_chunked_prediction_equals_the_one_shot_prediction():
    import numpy as np
    from experiments.check_designs import _predict_chunked

    reg, F = _small_regressor()
    Z, lv = reg.predict_coordinates(F)
    Zc, lvc = _predict_chunked(reg, F, chunk=3)
    assert Zc.shape == Z.shape and lvc.shape == (len(F),)
    np.testing.assert_allclose(Zc, Z, rtol=0, atol=1e-8)  # blocked BLAS rounds at ~1e-11 here
    np.testing.assert_allclose(
        lvc, np.ravel(lv), rtol=0, atol=1e-8
    )  # blocked BLAS rounds at ~1e-11 here


def test_no_prediction_call_exceeds_the_chunk_size():
    from experiments.check_designs import _predict_chunked

    reg, F = _small_regressor()
    sizes = []
    real = reg.predict_coordinates

    class Spy:
        def predict_coordinates(self, X):
            sizes.append(len(X))
            return real(X)

    _predict_chunked(Spy(), F, chunk=3)
    assert sizes == [3, 3, 3, 1]
