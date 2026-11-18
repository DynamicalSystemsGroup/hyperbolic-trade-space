"""The facts the bridge page (docs/bridge.md, WP41) states about the case's committed record.

Reads the committed v2 prediction and check-design files of the data of record; runs nothing.
"""

import pathlib

import pandas as pd

V2 = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs" / "data" / "v2"
CONFIG = ["panel_span_m", "battery_wh", "wheel_class", "st_grade", "Kp", "Kd", "fleet_size"]


def test_two_of_the_three_case_proposals_are_one_configuration():
    preds = pd.read_csv(V2 / "check_predictions_cubesat.csv")
    cfg = preds[CONFIG]
    assert len(cfg) == 3 and len(cfg.drop_duplicates()) == 2
    assert cfg.iloc[0].equals(cfg.iloc[2])


def test_the_case_proposals_fail_depth_of_discharge_and_the_candidates_pass():
    checks = pd.read_csv(V2 / "check_designs_cubesat.csv")
    prop, cand = checks[checks.role == "proposal"], checks[checks.role == "candidate"]
    assert len(prop) == 3 and not prop.dod_ok.any()
    assert prop[["settled", "momentum_ok", "power_ok"]].all().all()
    assert cand.dod_ok.all()
