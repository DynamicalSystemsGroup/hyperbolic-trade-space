"""The cost model of the cubesat (WP30 stage 3b; spikes D and D2; WP30-decisions.md, OD1, OD2).

* R-4: every part and the assembly line has a total price that is a fixed base plus a learning
  curve in the fleet size: nondecreasing and concave in ``n``, its unit cost falling, equal to the
  single-unit price at ``n = 1``; the fleet cost is the unit cost times ``n``; every term is a
  posynomial in ``(n, span, capacity)`` (``experiments/cost_form.py``, plain SymPy). A planted
  anti-learning slope fails the checks (negative control).
* R-5: the model's calcs reproduce spike D2's 2026 table to the dollar for the baseline
  (368,320, 261,621, 202,334 and 168,259 USD per satellite at 1, 3, 10 and 30; launch 93,040 USD
  per satellite) and its three configurations at one satellite (368,320, 287,520, 526,760), and
  equal the ladder script's repricing (spike D's curves with the 2026 coefficients, run without
  output side effects) on sampled designs to 1e-12.
* R-6, in code: the fleet size is drawn from a generator of its own, integers 1 to 30, so no
  existing draw moves; the fleet size changes the two cost columns of the oracle and nothing else.
* R-7 and OD2 (a): the two cost limits are the supervisor's values (350,000 USD a satellite,
  6,000,000 USD a fleet) with the coverage statement in the model's text; the requirements read the
  configuration's own fleet size and are verdicts only (no flag).

Fixtures FAIL by name (never skip) when the opensysml client cannot start.
"""

from __future__ import annotations

import importlib
import pathlib
import re

import cubesat_model as cm
import numpy as np
import pandas as pd
import pytest
from experiments import cost_form as cf
from experiments import cubesat_oracle as co
from experiments import definitions as df
from experiments import feasibility as fz
from experiments.runner import LogUniformSampler

ADCS = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs"
MODEL = ADCS / "model_v2" / "cubesat.sysml"
TEXT = MODEL.read_text()
ROOT = pathlib.Path(__file__).resolve().parents[1]
LADDERS = ROOT / "scripts/wp30_cost_ladders.py"
P = co.PACKAGE
NAMED = {  # the model's three named configurations (section 7), at one satellite
    "baseline": dict(wheel_class="medium", st_grade="medium", panel_span_m=0.6, battery_wh=80.0),
    "compact": dict(wheel_class="small", st_grade="coarse", panel_span_m=0.35, battery_wh=40.0),
    "agile": dict(wheel_class="large", st_grade="fine", panel_span_m=0.8, battery_wh=140.0),
}
GAINS = dict(Kp=0.5, Kd=1.0)  # the cost does not read the gains
FLEET = (1, 2, 3, 5, 10, 17, 30)


@pytest.fixture(scope="module")
def oracle():
    try:
        return co.CubesatOracle(TEXT, "nominalSlew", "aggressive", workers=1)
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


@pytest.fixture(scope="module")
def spike():
    """Spike D's curves with the 2026 coefficients: the ladder script's price functions."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("wp30_cost_ladders", LADDERS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return type("Spike", (), module.load_prices())


def _row(i: int, config: dict, n: float) -> dict:
    return {"design_id": i, **config, **GAINS, "fleet_size": float(n)}


def _eval(loaded, expression: str, unit: str | None = None) -> float:
    out = loaded.eval(f"{P}::{expression}")
    out = out[0] if isinstance(out, list) else out
    if unit is not None:
        out = out.in_unit(loaded.eval(f"1.0 [{unit}]").unit)
    return float(out)


@pytest.fixture(scope="module")
def fleet_cases(oracle):
    """The three named configurations at every fleet size, loaded as one model."""
    rows, keys = [], []
    for name, config in NAMED.items():
        for n in FLEET:
            keys.append((name, n))
            rows.append(_row(len(rows), config, n))
    loaded, symbols = oracle._configure(rows)
    return loaded, dict(zip(keys, symbols, strict=True))


# ---------------------------------------------------------------------------------------------
# R-5: the spike's table, to the dollar
# ---------------------------------------------------------------------------------------------
def test_the_models_prices_are_the_spikes_table(fleet_cases):
    loaded, sym = fleet_cases
    build = {k: _eval(loaded, f"FleetBuildCost({s})") for k, s in sym.items()}
    launch = {k: _eval(loaded, f"LaunchCost({s})") for k, s in sym.items()}
    assert round(build[("baseline", 1)]) == 368_320
    assert round(build[("compact", 1)]) == 287_520
    assert round(build[("agile", 1)]) == 526_760
    per_unit = {n: round(build[("baseline", n)] / n) for n in (1, 3, 10, 30)}
    assert per_unit == {1: 368_320, 3: 261_621, 10: 202_334, 30: 168_259}
    assert round(launch[("baseline", 1)]) == 93_040 == round(launch[("baseline", 30)])
    assert _eval(loaded, f"MassAccounting({sym[('baseline', 1)]})", "SI::kg") == pytest.approx(
        13.291, abs=1e-3
    )
    # the traded metrics: build plus launch, per satellite and for the fleet
    unit = {n: _eval(loaded, f"UnitCost({sym[('baseline', n)]})") for n in (1, 3, 10, 30)}
    fleet = {n: _eval(loaded, f"FleetCost({sym[('baseline', n)]})") for n in (1, 3, 10, 30)}
    assert {n: round(u) for n, u in unit.items()} == {
        1: 461_360,
        3: 354_661,
        10: 295_374,
        30: 261_299,
    }
    assert {n: round(f) for n, f in fleet.items()} == {
        1: 461_360,
        3: 1_063_983,
        10: 2_953_739,
        30: 7_838_981,
    }


def test_the_model_equals_the_spikes_script_on_sampled_designs(oracle, spike):
    """The spike's ``fleet_build`` and launch (an independent Python implementation of the same
    relations) against the model's calcs, for sampled configurations at sampled fleet sizes."""
    exp = df.EXPERIMENTS["v2-primary"]
    designs = co.build_sampler(exp).draw(12, 0)
    rows = [
        {**r.to_dict(), "design_id": i, "fleet_size": float(n)}
        for i, (_, r) in enumerate(designs.iterrows())
        for n in (1, 7)
    ]
    rows = [{**r, "design_id": i} for i, r in enumerate(rows)]
    loaded, symbols = oracle._configure(rows)
    for r, sym in zip(rows, symbols, strict=True):
        args = (r["wheel_class"], r["st_grade"], r["panel_span_m"], r["battery_wh"])
        want_build = spike.fleet_build(*args, r["fleet_size"])
        assert _eval(loaded, f"FleetBuildCost({sym})") == pytest.approx(want_build, rel=1e-12)
        mass = _eval(loaded, f"MassAccounting({sym})", "SI::kg")
        assert mass == pytest.approx(spike.mass_of(*args), rel=1e-12)
        assert _eval(loaded, f"FleetCost({sym})") == pytest.approx(
            want_build + spike.LAUNCH_RATE * mass * r["fleet_size"], rel=1e-12
        )
        assert _eval(loaded, f"UnitCost({sym})") == pytest.approx(
            (want_build + spike.LAUNCH_RATE * mass * r["fleet_size"]) / r["fleet_size"], rel=1e-12
        )


# ---------------------------------------------------------------------------------------------
# R-4: the form the supervisor named
# ---------------------------------------------------------------------------------------------
def _totals(loaded, sym) -> dict[str, float]:
    return {
        p: _eval(loaded, f"{p.capitalize()}Total({sym})")
        for p in ("bus", "panel", "battery", "wheel", "tracker", "assembly")
    }


def test_each_total_is_nondecreasing_and_concave_and_its_unit_cost_falls(fleet_cases):
    loaded, sym = fleet_cases
    for name in NAMED:
        by_n = {n: _totals(loaded, sym[(name, n)]) for n in FLEET}
        for part in by_n[1]:
            t = np.array([by_n[n][part] for n in FLEET], float)
            n = np.array(FLEET, float)
            assert (np.diff(t) > 0).all(), (name, part)  # nondecreasing, strictly here
            slopes = np.diff(t) / np.diff(n)
            assert (np.diff(slopes) < 0).all(), (name, part)  # concave: slopes fall
            assert (np.diff(t / n) < 0).all(), (name, part)  # the unit cost falls
            # a fixed base: a positive offset at every fleet size
            assert t[0] > 0 and t[-1] / t[0] < n[-1], (name, part)


def test_the_fleet_cost_is_the_unit_cost_times_n_and_the_launch_is_linear(fleet_cases):
    loaded, sym = fleet_cases
    for name in NAMED:
        fleet = np.array([_eval(loaded, f"FleetCost({sym[(name, n)]})") for n in FLEET])
        unit = np.array([_eval(loaded, f"UnitCost({sym[(name, n)]})") for n in FLEET])
        launch = np.array([_eval(loaded, f"LaunchCost({sym[(name, n)]})") for n in FLEET])
        build = np.array([_eval(loaded, f"FleetBuildCost({sym[(name, n)]})") for n in FLEET])
        n = np.array(FLEET, float)
        np.testing.assert_allclose(fleet, unit * n, rtol=1e-9)  # F = U n
        np.testing.assert_allclose(fleet, build + launch * n, rtol=1e-12)
        assert (np.diff(fleet) > 0).all() and (np.diff(unit) < 0).all()
        np.testing.assert_allclose(launch, launch[0], rtol=1e-12)  # launch per satellite constant


def test_at_one_satellite_each_total_is_its_single_unit_price(fleet_cases):
    loaded, sym = fleet_cases
    for name in NAMED:
        s = sym[(name, 1)]
        totals = _totals(loaded, s)
        singles = {
            "bus": _eval(loaded, "prices.bus") + _eval(loaded, "prices.antenna")
            + _eval(loaded, "prices.imu"),
            "panel": _eval(loaded, f"PanelPrice({s})"),
            "battery": _eval(loaded, f"BatteryPrice({s})"),
            "wheel": _eval(loaded, f"WheelPrice({s})"),
            "tracker": _eval(loaded, f"TrackerPrice({s})"),
            "assembly": _eval(loaded, "prices.assembly"),
        }  # fmt: skip
        for part, price in singles.items():
            assert totals[part] == pytest.approx(price, rel=1e-12), (name, part)
        assert _eval(loaded, f"FleetBuildCost({s})") == pytest.approx(sum(singles.values()))


def _form_checks(oracle, text: str) -> dict[str, bool]:
    """The posynomial-form checks on the constants read from the model ``text``."""
    other = co.CubesatOracle(text, "nominalSlew", "aggressive", workers=1)
    grid = [(0.3, 20.0), (1.0, 20.0), (0.3, 200.0), (0.7, 90.0)]
    base = dict(wheel_class="medium", st_grade="medium", **GAINS, fleet_size=1.0)
    loaded, symbols = other._configure(
        [{**base, "design_id": i, "panel_span_m": s, "battery_wh": b}
         for i, (s, b) in enumerate(grid)]
    )  # fmt: skip
    rows = [(sym, s, b) for sym, (s, b) in zip(symbols, grid, strict=True)]
    return cf.checks(cf.constants(loaded, P, rows))


def test_every_term_is_a_posynomial_in_n_span_and_capacity(oracle):
    """R-4: the plain-SymPy reading of ``cost_form.py`` on the constants the model states."""
    got = _form_checks(oracle, TEXT)
    assert all(got.values()), [k for k, v in got.items() if not v]
    assert len(got) == 7


def test_a_planted_anti_learning_slope_fails_the_form_checks(oracle):
    """Negative control: a slope above one (the unit cost would rise with the fleet) is caught."""
    planted = TEXT.replace("attribute busSlope : Real = 0.90;", "attribute busSlope : Real = 1.10;")
    assert planted != TEXT
    got = _form_checks(oracle, planted)
    assert not got["each total is concave in n"] and not got["each unit cost falls in n"]
    assert got["each total at n = 1 is its unit price"]  # the identity does not read the slope


# ---------------------------------------------------------------------------------------------
# R-6 in code: the fleet size is its own draw
# ---------------------------------------------------------------------------------------------
def test_the_fleet_size_is_drawn_from_a_generator_of_its_own():
    exp = df.EXPERIMENTS["v2-primary"]
    smp = co.build_sampler(exp)
    designs = smp.draw(1000, exp.seed)
    old = LogUniformSampler(smp.categorical, smp.log_ranges).draw(1000, exp.seed)
    assert list(designs.columns) == [*old.columns, "fleet_size"]
    pd.testing.assert_frame_equal(designs[list(old.columns)], old, check_exact=True)
    n = designs["fleet_size"]
    assert n.between(1, 30).all() and (n == n.round()).all()
    assert set(n.astype(int)) == set(range(1, 31))  # the whole range appears in 1000 designs
    # design i depends only on (seed, i): the first five of a short draw are the first five
    pd.testing.assert_frame_equal(smp.draw(5, exp.seed), designs.head(5))
    # and the range is the model's
    assert smp.integer_ranges == {"fleet_size": (1, 30)}


def test_the_fleet_size_changes_the_two_cost_columns_and_nothing_else(oracle):
    cfg = {**NAMED["baseline"], **GAINS}
    one, many = oracle({**cfg, "fleet_size": 1.0}), oracle({**cfg, "fleet_size": 30.0})
    assert list(one) == list(many)
    differ = {k for k in one if one[k] != many[k]}
    assert differ == {"unit_cost_usd", "fleet_cost_usd"}
    assert many["fleet_cost_usd"] == pytest.approx(many["unit_cost_usd"] * 30, rel=1e-9)
    assert one["fleet_cost_usd"] == pytest.approx(one["unit_cost_usd"], rel=1e-12)
    # a configuration with no fleet size is a fleet of one
    assert oracle(cfg) == one
    with pytest.raises(ValueError, match="fleet_size"):
        oracle({**cfg, "fleet_size": 31.0})


# ---------------------------------------------------------------------------------------------
# R-7, OD2 (a): the supervisor's limits and verdicts
# ---------------------------------------------------------------------------------------------
def _req_doc(requirement: str) -> str:
    body = TEXT[TEXT.index(f"requirement def {requirement} ") :]
    return " ".join(body[: body.index("*/")].split())


def _doc_of(attribute: str) -> str:
    body = TEXT[TEXT.index(f"attribute {attribute} :") :]
    return " ".join(body[: body.index("*/")].split())


EXCLUSIONS = (  # the coverage statement's exclusion list, in the supervisor's order
    "the payload and its instruments",
    "communications and the payload interface",
    "flight software",
    "environmental testing beyond the assembly line",
    "licensing",
    "a ground station network and operations",
    "the launch slot minimum",
    "broker fees",
)


def test_the_two_cost_limits_are_the_supervisors_values_with_the_coverage_statement():
    """WP30-decisions.md, 2026-11-11: 350,000 USD a satellite and 6,000,000 USD a fleet on the
    covered cost, the full fleet budget 8,000,000 USD; no placeholder is left in the model, and
    each limit's text, and its requirement's, states what the cost covers and leaves out."""
    assert "PLACEHOLDER" not in TEXT.upper() and "PENDING HIS CONFIRMATION" not in TEXT
    assert "unitCostLimit : Real = 350000.0" in TEXT and "fleetCostLimit : Real = 6.0e6" in TEXT
    for name, text in (
        ("UnitCostRequirement", _req_doc("UnitCostRequirement")),
        ("FleetCostRequirement", _req_doc("FleetCostRequirement")),
    ):
        assert "lower bound on a full costing" in text, name
        positions = [text.index(item) for item in EXCLUSIONS]
        assert positions == sorted(positions), name  # in the supervisor's order
        assert "1U series can sit below 40,000 USD a unit" in text, name
        assert "50 kg" in text and "not modelled" in text, name
    # the cost model's own header states it too (the calcs' text), in the same order
    header = " ".join(TEXT[TEXT.index("COVERAGE.") :].split())[:1500]
    assert "lower bound on a full costing" in header
    positions = [header.index(item) for item in EXCLUSIONS[:7]]
    assert positions == sorted(positions)
    for name in ("fleetCostLimit", "FleetCostRequirement"):
        text = _doc_of(name) if name[0].islower() else _req_doc(name)
        assert "8,000,000 USD" in text and "2,000,000 USD" in text, name


def test_the_cost_requirements_are_verdicts_and_read_the_configurations_own_fleet_size(
    oracle, fleet_cases
):
    loaded, sym = fleet_cases

    def holds(requirement: str, subject: str) -> bool:
        v = loaded.verify_requirement(f"{P}::{requirement}", subject=subject)
        assert v.status in ("holds", "violated")
        return bool(v.holds)

    # the baseline's unit cost falls with the fleet and crosses the 350,000 USD limit between 3
    # satellites (354,661) and 5 (325,213); its fleet cost passes at 17 satellites (4.72 million)
    # and fails at 30 (7.84 million), over the 6,000,000 USD limit
    assert [holds("UnitCostRequirement", sym[("baseline", n)]) for n in FLEET] == [
        False,
        False,
        False,
        True,
        True,
        True,
        True,
    ]
    assert holds("FleetCostRequirement", sym[("baseline", 17)])
    assert not holds("FleetCostRequirement", sym[("baseline", 30)])
    # no single satellite of the three clears the unit cost limit (the supervisor: "its fine")
    assert not any(holds("UnitCostRequirement", sym[(name, 1)]) for name in NAMED)
    # verdict only: neither requirement is a flag (the feasible sets stay the physics')
    assert not {"UnitCostRequirement", "FleetCostRequirement"} & set(fz.FLAG_REQUIREMENTS.values())
    assert co.FLAG_NAMES == ("settled", "momentum_ok", "power_ok", "dod_ok")
    assert re.search(r"verdict", _doc_of("unitCostLimit"))


def test_the_model_and_the_oracle_name_the_cost_columns_once():
    assert co.ATTRIBUTE_NAMES[-2:] == ("unit_cost_usd", "fleet_cost_usd")
    assert co.CONFIG_NAMES[-1] == "fleet_size" and len(co.ATTRIBUTE_NAMES) == 11
    assert importlib.import_module("case").CUBESAT.attributes == co.ATTRIBUTE_NAMES
