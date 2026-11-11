"""WP16 D-1 / R-1: the model is what is evaluated.

A scratch copy of the v2 model with one accounting constant changed (the bus mass) must give
different attributes through the oracle than the committed model. The check is itself tested: a
stub oracle that ignores the model and returns the committed values is detected. The oracle's
model path is the committed file, whose sha256 is the one the ledger's current entries record.

Fails by name (never skips) when the opensysml client cannot start.
"""

from __future__ import annotations

import dataclasses
import pathlib

import cubesat_model as cm
import pandas as pd
import pytest
from experiments import cubesat_oracle as co
from experiments import definitions as df
from experiments import ledger as lg

REPO = pathlib.Path(__file__).resolve().parents[1]
ADCS = REPO / "examples" / "adcs"
MODEL = ADCS / "model_v2" / "cubesat.sysml"
TEXT = MODEL.read_text(encoding="utf-8")
V2_PRIMARY = ADCS / "data" / "v2" / "adcs_designs_cubesat_gains.csv"
BUS_MASS = "attribute mass : MassValue = 10.0 [kg];"
MUTANT = TEXT.replace(BUS_MASS, "attribute mass : MassValue = 11.0 [kg];")
MOVED = ("total_mass_kg", "pointing_error_deg")  # the bus mass enters the mass and the inertia


def _config() -> dict:
    row = pd.read_csv(V2_PRIMARY).iloc[0]
    return {
        k: row[k]
        for k in ("wheel_class", "st_grade", "panel_span_m", "battery_wh", "Kp", "Kd", "fleet_size")
    }


def committed_values() -> dict:
    """What the committed generation holds for the configuration of ``_config``."""
    return pd.read_csv(V2_PRIMARY).iloc[0].to_dict()


def assert_model_is_evaluated(make_oracle) -> dict:
    """Fail unless changing one accounting constant of the model text changes the attributes.

    ``make_oracle(text)`` returns a callable mapping a configuration to a row. Returns the moved
    attributes (name -> (committed model, mutated model)) when the check passes.
    """
    assert MUTANT != TEXT, "the mutation did not change the model text"
    cfg = _config()
    base, mutated = make_oracle(TEXT)(cfg), make_oracle(MUTANT)(cfg)
    moved = {k: (base[k], mutated[k]) for k in co.ATTRIBUTE_NAMES if base[k] != mutated[k]}
    assert moved, "the attributes do not depend on the model text: the oracle ignores the model"
    return moved


@pytest.fixture(scope="module")
def real_oracle():
    cache: dict[str, co.CubesatOracle] = {}

    def make(text: str):
        if text not in cache:
            try:
                cache[text] = co.CubesatOracle(text, "nominalSlew", "aggressive", workers=1)
            except cm.OpenSysMLUnavailable as exc:
                pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)
        return cache[text]

    return make


def test_a_changed_accounting_constant_changes_the_attributes(real_oracle):
    moved = assert_model_is_evaluated(real_oracle)
    base, mutated = moved["total_mass_kg"]
    assert mutated - base == pytest.approx(1.0, rel=1e-9)  # exactly the 1 kg added to the bus
    assert set(MOVED) <= set(moved), sorted(moved)


def test_the_unmutated_model_reproduces_the_committed_values(real_oracle):
    """The baseline of the comparison is the committed generation, not another computation."""
    got, want = real_oracle(TEXT)(_config()), committed_values()
    for k in co.ATTRIBUTE_NAMES:
        assert got[k] == pytest.approx(want[k], rel=1e-3), k  # the reproducibility rtol


def test_the_check_detects_a_stub_that_ignores_the_model():
    """The check is meaningful: an oracle returning the committed values whatever the text is
    caught."""

    def stub(text):
        return lambda cfg: committed_values()

    with pytest.raises(AssertionError, match="ignores the model"):
        assert_model_is_evaluated(stub)


def test_the_oracles_model_path_is_the_committed_file_the_ledger_hashes():
    exp = df.EXPERIMENTS["v2-primary"]
    assert (REPO / exp.model_path).resolve() == MODEL.resolve()
    assert co._model_text(dataclasses.replace(exp, inputs={}), None) == TEXT
    entries = lg.read(lg.LEDGER_PATH)
    for name in df.EXPERIMENTS:
        cur = lg.latest(entries, name)
        assert cur["model_path"] == exp.model_path
        assert cur["model_sha256"] == lg.sha256_file(MODEL), name


def test_the_steps_path_evaluates_the_model_too():
    """The default oracle reads the settling time by event detection (WP16 Amendment 2, WP23);
    with the step read-off of the generation before, the mutated model still moves the
    attributes (the check is the same; only the time's reading differs)."""
    cache: dict[str, co.CubesatOracle] = {}

    def make(text: str):
        if text not in cache:
            try:
                cache[text] = co.CubesatOracle(
                    text, "nominalSlew", "aggressive", workers=1, settling_time_method="steps"
                )
            except cm.OpenSysMLUnavailable as exc:
                pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)
        return cache[text]

    moved = assert_model_is_evaluated(make)
    assert set(MOVED) <= set(moved), sorted(moved)
    assert moved["total_mass_kg"][1] - moved["total_mass_kg"][0] == pytest.approx(1.0, rel=1e-9)
