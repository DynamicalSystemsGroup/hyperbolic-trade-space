"""The package-user fixtures: the generators reproduce the committed tables; no satellite words."""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "user-tests"
SATELLITE = re.compile(
    r"satellite|cubesat|spacecraft|orbit|attitude|adcs|slew|pointing|reaction.wheel|star.tracker",
    re.IGNORECASE,
)
PUBLIC_FILES = ["plain_table.csv", "pump_table.csv", "pump_trade.sysml", "export_pump_table.py"]


def _load(name):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, FIXTURES / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plain_table_reproduces_and_needs_conditioning():
    built = _load("make_plain_table").build()
    committed = pd.read_csv(FIXTURES / "plain_table.csv")
    pd.testing.assert_frame_equal(built, committed, check_exact=False, rtol=1e-9)
    numeric = committed.drop(columns=["sample", "batch"])
    assert (numeric > 0).all().all()
    # the scales differ by orders of magnitude and two columns are smaller-is-better
    medians = numeric.median()
    assert medians.max() / medians.min() > 50
    assert list(committed.columns) == [
        "sample",
        "batch",
        "strength_mpa",
        "weight_kg",
        "stiffness_gpa",
        "cost_usd",
    ]


def test_pump_table_reproduced_by_the_script_from_the_model(tmp_path):
    pytest.importorskip("opensysml")
    module = _load("export_pump_table")
    try:
        rows = module.export_rows((FIXTURES / "pump_trade.sysml").read_text(encoding="utf-8"))
    except Exception as exc:  # the client cannot start: name the cause, never pass silently
        pytest.fail(f"the opensysml client could not export the pump table: {exc!r}")
    out = tmp_path / "pump_table.csv"
    module.write_csv(rows, out)
    built, committed = pd.read_csv(out), pd.read_csv(FIXTURES / "pump_table.csv")
    pd.testing.assert_frame_equal(built, committed)
    assert np.isfinite(committed.to_numpy()).all()
    assert (committed.drop(columns="design_id") > 0).all().all()


@pytest.mark.parametrize("name", PUBLIC_FILES)
def test_no_satellite_vocabulary(name):
    text = (FIXTURES / name).read_text(encoding="utf-8")
    assert SATELLITE.search(text) is None


def test_pump_model_shares_nothing_with_the_case():
    adcs = Path(__file__).resolve().parents[1] / "examples" / "adcs" / "model_v2"
    case_calcs = set(
        re.findall(r"calc def (\w+)", (adcs / "cubesat.sysml").read_text(encoding="utf-8"))
    )
    pump_calcs = set(
        re.findall(r"calc def (\w+)", (FIXTURES / "pump_trade.sysml").read_text(encoding="utf-8"))
    )
    assert pump_calcs == {"Flow", "Head", "Efficiency", "ShaftPower", "Mass"}
    assert not (pump_calcs & case_calcs)
