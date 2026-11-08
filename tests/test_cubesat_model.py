"""Tests for the SysML cubesat configuration space and its Python model layer (WP4b, phase 1).

Every test that needs the opensysml runtime goes through the module-scoped ``cubesat`` fixture,
which FAILS (never skips) with a message naming the cause when the client cannot start. CI should
set ``REQUIRE_OPENSYSML=1``; the flag only makes the message say so, the behaviour is the same.
Reproducibility tests (``-k reproduc``) regenerate designs of the committed dataset (phase 2).
"""

from __future__ import annotations

import math
import os
import pathlib
import re
import subprocess
import sys
from types import SimpleNamespace

import cubesat_model as cm
import numpy as np
import pytest
from adcs_sim import inertia_tensor
from opensysml.errors import ModelError

ADCS_DIR = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs"
SYSML = (ADCS_DIR / "cubesat_tradespace.sysml").read_text()
PKG = cm.PKG
FAST = {"t_end": 1500.0, "max_step": 2.0}  # coarser steps than the dataset, for tests only


@pytest.fixture(scope="module")
def cubesat():
    """The loaded model; a named-cause failure, never a skip, when the client cannot start."""
    try:
        return cm.load_model()
    except cm.OpenSysMLUnavailable as exc:
        flag = " (REQUIRE_OPENSYSML is set)" if os.environ.get("REQUIRE_OPENSYSML") else ""
        pytest.fail(f"the opensysml client could not start{flag}: {exc}", pytrace=False)


def _design(**kw) -> dict:
    d = {
        "design_id": 0,
        "seed": 0,
        "wheel_class": "medium",
        "st_grade": "medium",
        "panel_span_m": 0.6,
        "battery_wh": 80.0,
        "Kp": 0.05,
        "Kd": 0.5,
    }
    d.update(kw)
    return d


def _env(model, name, unit=None):
    return model._eval_value(f"{PKG}::environment.{name}", unit)


# ---------------------------------------------------------------------------------------------
# R-3: the model loads strictly and has the required content
# ---------------------------------------------------------------------------------------------
def _symbols(model, kind):
    return {
        q.properties["name"]
        for q in model.model.query(
            scope=[PKG], where={"property": "@type", "operator": "=", "value": kind}
        )
    }


def test_model_loads_strict_and_has_required_symbols(cubesat):
    """R-3: strict load, no diagnostics; required definitions are present."""
    assert cubesat.model.ok
    assert not [d for d in cubesat.model.diagnostics if d.severity == "error"]
    parts = _symbols(cubesat, "PartDefinition")
    for name in ("Cubesat", "Bus", "SolarPanel", "Battery", "ReactionWheel", "StarTracker"):
        assert name in parts
    assert "Controller" in parts
    assert {"WheelClass", "TrackerGrade"} <= _symbols(cubesat, "EnumerationDefinition")
    assert {"MassAccounting", "GeneratedPower", "EclipseReserve"} <= _symbols(
        cubesat, "CalculationDefinition"
    )
    assert {"PowerOK", "DepthOfDischargeOK"} <= _symbols(cubesat, "ConstraintDefinition")
    assert "ModelTest" in _symbols(cubesat, "AnalysisCaseDefinition")
    assert "cubesatBaseline" in _symbols(cubesat, "PartUsage")


def test_model_self_check_and_model_test_analysis(cubesat):
    """R-3: the reflective validation finds nothing; the documented model test runs."""
    assert cubesat.model.self_check().status == "holds"
    out = cubesat.model.run_analysis(f"{PKG}::ModelTest", subject=f"{PKG}::cubesatBaseline")
    assert "totalMass" in str(out)


def test_attributes_carry_units(cubesat):
    """R-3/R-18: every quantity-typed attribute of the wheel and tracker tables has a unit."""
    for abstract in ("ReactionWheel", "StarTracker"):
        for alt in (cubesat.wheels if abstract == "ReactionWheel" else cubesat.trackers).values():
            facts = cubesat.model.find(alt.part_def).attribute_facts()
            quantities = [f for f in facts if f.type.startswith(("ISQ", "SI"))]
            assert quantities and all(f.unit for f in quantities), alt.part_def
    text = SYSML
    assert "illustrative" in text.lower() and "documentation of a demonstration" in text


def test_negative_control_broken_model_fails_strict_load(cubesat):
    """R-3 negative control: a broken source must not load strictly."""
    broken = SYSML.replace("attribute mass : MassValue = 10.0 [kg];", "attribute mass : Nope = 1;")
    with pytest.raises(ModelError):
        cm.CubesatModel(broken)


# ---------------------------------------------------------------------------------------------
# R-12: clear failure when the client cannot start
# ---------------------------------------------------------------------------------------------
def test_unavailable_binary_gives_named_cause():
    """R-12: a bad OPENSYSML_BINARY fails with a message naming the cause, not a skip.

    Run in a fresh interpreter: a client already connected in this process would be reused.
    """
    code = (
        "import cubesat_model as cm\n"
        "try:\n"
        "    cm.get_connection()\n"
        "except cm.OpenSysMLUnavailable as exc:\n"
        "    print('NAMED:', exc)\n"
    )
    env = dict(os.environ, OPENSYSML_BINARY="/nonexistent/sysml-grpc", PYTHONPATH=str(ADCS_DIR))
    done = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        cwd=ADCS_DIR,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert "NAMED: opensysml service binary unavailable" in done.stdout, done.stdout + done.stderr


# ---------------------------------------------------------------------------------------------
# R-4: nothing duplicated; the sampler reads the model
# ---------------------------------------------------------------------------------------------
def test_sampler_reads_enums_and_ranges_from_the_model(cubesat):
    designs = cubesat.sample_designs(300, seed=0)
    lo, hi = cubesat.panel_span_range
    assert designs.panel_span_m.between(lo, hi).all()
    assert set(designs.wheel_class) == set(cubesat.wheel_classes) == {"small", "medium", "large"}
    assert set(designs.st_grade) == set(cubesat.tracker_grades)
    assert designs.Kp.between(*cubesat.kp_range).all()
    assert designs.battery_wh.between(*cubesat.battery_wh_range).all()


def test_editing_a_range_or_enum_literal_changes_the_sampler(cubesat):
    """R-4: a copy of the model with a narrower range and an extra literal drives the sampler."""
    edited = SYSML.replace(
        "panelSpanMin : LengthValue = 0.3 [m]", "panelSpanMin : LengthValue = 0.8 [m]"
    )
    assert edited != SYSML
    edited = edited.replace(
        "enum def WheelClass { small; medium; large; }",
        "enum def WheelClass { small; medium; large; huge; }",
    )
    edited = edited.replace(
        "    abstract part def StarTracker {",
        "    part def HugeWheel :> ReactionWheel {\n"
        "        :>> wheelClass = WheelClass::huge;\n"
        "        :>> maxTorque = 0.05 [N*m];\n"
        "        :>> maxMomentum = 0.5 [N*m*s];\n"
        "        :>> mass = 2.0 [kg];\n"
        "    }\n"
        "    abstract part def StarTracker {",
    )
    model = cm.CubesatModel(edited)
    assert model.panel_span_range[0] == pytest.approx(0.8)
    designs = model.sample_designs(200, seed=0)
    assert designs.panel_span_m.min() >= 0.8
    assert "huge" in set(designs.wheel_class)
    assert cubesat.sample_designs(200, seed=0).panel_span_m.min() < 0.8


def test_no_duplicated_constants_in_python():
    """R-4: the wheel and tracker tables and the design-space bounds are not copied into Python."""
    py = (ADCS_DIR / "cubesat_model.py").read_text()
    code = "\n".join(
        line for line in py.splitlines() if not line.lstrip().startswith(("#", '"', "*"))
    )
    code = re.sub(r'""".*?"""', "", code, flags=re.S)
    # scenario parameters (slew angle, horizon, step, slew-time bands) are not model constants
    code = re.sub(
        r"^(SLEW_DEG|T_END|MAX_STEP|SLEW_BAND_DEG|SLEW_BAND_SENSITIVITY_DEG) = .*$",
        "",
        code,
        flags=re.M,
    )
    code = code.replace("1.0 [", "[")  # unit constructors in expressions, not table values
    tables = re.findall(
        r"part def (?:Small|Medium|Large|Coarse|Fine)\w+ :> .*?\n    }\n", SYSML, flags=re.S
    ) + re.findall(
        r"part def (?:DesignSpace|AggressiveGainSpace) \{.*?\n    }\n", SYSML, flags=re.S
    )
    assert len(tables) >= 8
    numbers = set()
    for block in tables:
        for tok in re.findall(r"= ([0-9][0-9.eE+-]*)", block):
            numbers.add(tok)
    assert numbers
    for tok in sorted(numbers):
        assert not re.search(rf"(?<![\w.]){re.escape(tok)}(?![\w.])", code), tok


def test_aggressive_gain_box_is_read_from_the_model(cubesat):
    """Amendment 5, lever i: the gain box is a part of the SysML model, selected by name."""
    aggressive = cm.load_model(gain_box="aggressive")
    assert cubesat.gain_box == "baseline" and aggressive.gain_box == "aggressive"
    assert cubesat.kp_range == pytest.approx((0.03, 1.0))  # the default is unchanged
    assert aggressive.kp_range == pytest.approx((0.2, 2.0))
    assert aggressive.kd_range == pytest.approx((0.3, 1.5))
    base = cubesat.sample_designs(50, seed=0)
    gains = aggressive.sample_designs(50, seed=0)
    for col in ("wheel_class", "st_grade", "panel_span_m", "battery_wh"):
        assert (base[col] == gains[col]).all(), col  # same designs, different gains
    assert gains.Kp.between(0.2, 2.0).all() and gains.Kd.between(0.3, 1.5).all()
    with pytest.raises(ValueError):
        cm.CubesatModel(SYSML, gain_box="nonsense")
    # R-4: the box is the model's: editing the model's range changes the sampler
    edited = SYSML.replace("attribute KpMin : Real = 0.2;", "attribute KpMin : Real = 0.5;")
    assert edited != SYSML
    assert cm.CubesatModel(edited, gain_box="aggressive").kp_range[0] == pytest.approx(0.5)


def test_wheel_capacities_and_momentum_utilisation(cubesat):
    """Lever ii: capacity from the model's wheel table; utilisation is peak / capacity."""
    import pandas as pd

    cap = cubesat.wheel_capacities()
    assert cap == pytest.approx({"small": 0.010, "medium": 0.030, "large": 0.100})
    df = pd.DataFrame(
        {
            "wheel_class": ["small", "medium", "large"],
            "peak_momentum_nms": [0.005, 0.045, 0.02],
            "momentum_ok": [True, False, True],
        }
    )
    out = cm.add_momentum_utilisation(df, cap)
    assert out.momentum_utilisation.tolist() == pytest.approx([0.5, 1.5, 0.2])
    assert ((out.momentum_utilisation <= 1) == out.momentum_ok).all()
    assert out.momentum_headroom_nms.tolist() == pytest.approx([0.005, -0.015, 0.08])
    assert "momentum_utilisation" not in df.columns  # the input is not modified
    with pytest.raises(ValueError):
        cm.add_momentum_utilisation(df.assign(wheel_class="huge"), cap)


def test_sampler_is_seed_stable_and_independent_of_n(cubesat):
    a = cubesat.sample_designs(5, seed=3)
    b = cubesat.sample_designs(12, seed=3)
    assert a.equals(b.iloc[:5].reset_index(drop=True))
    assert not a.equals(cubesat.sample_designs(5, seed=4))


# ---------------------------------------------------------------------------------------------
# R-5, R-10: accounting by the model
# ---------------------------------------------------------------------------------------------
def test_run_sweep_over_panel_span_matches_python_accounting(cubesat):
    """R-5: run_sweep (grid) of the model's PanelMass reproduces areal density x span x chord."""
    m = cubesat.model
    metre = cubesat.unit("SI::m")
    chord = cubesat.value(cubesat.baseline().instance.get("panelPlus").get("chord"), "SI::m")
    density = _env(cubesat, "panelArealDensity", "SI::kg/SI::m**2")
    table = m.run_sweep(
        f"{PKG}::PanelMass",
        {"span": (Q(0.3, metre), Q(1.0, metre), Q(0.1, metre))},
        named_arguments={"chord": Q(chord, metre)},
        engine="sweep",
    )
    assert len(table) == 8 and not table.failures
    for row in table.rows:
        span = cubesat.value(row.inputs["span"], "SI::m")
        got = cubesat.value(row.outputs["result"][0], "SI::kg")
        assert got == pytest.approx(density * span * chord, rel=1e-12)


def test_accounting_matches_independent_python_formulas(cubesat):
    """R-5/R-7/R-8: configuration accounting by the model equals the formulas, from model data."""
    d = _design(panel_span_m=0.45, battery_wh=120.0, wheel_class="large", st_grade="fine")
    cfg = cubesat.configure([d])[0]
    acc = cubesat.accounting(cfg)
    density = _env(cubesat, "panelArealDensity", "SI::kg/SI::m**2")
    spec = _env(cubesat, "batterySpecificEnergy")
    chord = cubesat.sim_params(cfg)["panelChord"]
    assert acc["panel_mass_kg"] == pytest.approx(density * 0.45 * chord, rel=1e-12)
    assert acc["battery_mass_kg"] == pytest.approx(120.0 / spec, rel=1e-12)
    flux = _env(cubesat, "solarFlux", "SI::W/SI::m**2")
    factor = math.prod(
        _env(cubesat, k)
        for k in ("cellEfficiency", "packingFactor", "degradation", "incidenceFactor")
    )
    area = 2 * 0.45 * chord
    assert acc["generated_power_w"] == pytest.approx(flux * factor * area, rel=1e-12)
    ratio = cubesat.accounting(cubesat.configure([_design(panel_span_m=0.9)])[0])
    assert ratio["generated_power_w"] / cubesat.accounting(
        cubesat.configure([_design(panel_span_m=0.45)])[0]
    )["generated_power_w"] == pytest.approx(2.0, rel=1e-12)  # R-7: proportional to area


def test_mass_accounting_identity(cubesat):
    """R-10: total = bus + battery + 2 panels + antenna + 3 wheels + tracker + IMU = sim input."""
    for d in cubesat.sample_designs(6, seed=1).to_dict("records"):
        cfg = cubesat.configure([d])[0]
        i, v = cfg.instance, cubesat.value
        parts = (
            v(i.get("bus").get("mass"), "SI::kg")
            + v(i.get("battery").get("mass"), "SI::kg")
            + v(i.get("panelPlus").get("mass"), "SI::kg")
            + v(i.get("panelMinus").get("mass"), "SI::kg")
            + v(i.get("antenna").get("mass"), "SI::kg")
            + 3 * v(i.get("wheel").get("mass"), "SI::kg")
            + v(i.get("tracker").get("mass"), "SI::kg")
            + v(i.get("imu").get("mass"), "SI::kg")
        )
        acc = cubesat.accounting(cfg)
        assert acc["total_mass_kg"] == pytest.approx(parts, abs=1e-9)
        p = cubesat.sim_params(cfg)
        assert p["mass"] + 2 * p["panelMass"] + p["antennaMass"] == pytest.approx(parts, abs=1e-9)


# ---------------------------------------------------------------------------------------------
# R-7, R-8, R-9: couplings
# ---------------------------------------------------------------------------------------------
def _inertia(cubesat, **kw):
    return inertia_tensor(cubesat.sim_params(cubesat.configure([_design(**kw)])[0]))


def test_baseline_inertia_pin(cubesat):
    """R-8: the baseline's inertia from the model's own formula through ``inertia_tensor``."""
    params = cubesat.sim_params(cubesat.baseline())
    jxx, jyy, jzz = inertia_tensor(params)
    assert (jxx, jyy, jzz) == pytest.approx((0.4006, 0.2058, 0.3171), abs=5e-5)
    assert params["mass"] == pytest.approx(11.771428571, abs=1e-8)


def test_panel_span_raises_inertia_and_slows_the_slew(cubesat):
    """R-7: span up -> inertia about the slew axis up -> settling time up (others fixed)."""
    spans = [0.3, 0.6, 1.0]
    jxx = [_inertia(cubesat, panel_span_m=s)[0] for s in spans]
    assert jxx == sorted(jxx) and jxx[0] < jxx[-1]
    # Lightly damped gains: for heavily overdamped designs the slow pole Kp / (4 Kd) does not
    # depend on the inertia, so settling time would not follow the inertia there.
    gains = {"Kp": 0.1, "Kd": 0.1}
    settle = [
        cubesat.measure(_design(panel_span_m=s, **gains), **FAST)["settling_time_s"] for s in spans
    ]
    assert settle == sorted(settle) and settle[0] < settle[-1]


def test_battery_capacity_raises_mass_and_inertia(cubesat):
    """R-8: capacity up -> battery mass, total mass, inertia up."""
    caps = [20.0, 80.0, 200.0]
    cfgs = [cubesat.configure([_design(battery_wh=c)])[0] for c in caps]
    mass = [cubesat.accounting(c)["total_mass_kg"] for c in cfgs]
    batt = [cubesat.accounting(c)["battery_mass_kg"] for c in cfgs]
    jxx = [inertia_tensor(cubesat.sim_params(c))[0] for c in cfgs]
    assert mass == sorted(mass) and batt == sorted(batt) and jxx == sorted(jxx)
    assert mass[0] < mass[-1] and jxx[0] < jxx[-1]


def test_available_power_caps_the_usable_torque(cubesat):
    """R-9: less available power -> lower usable torque (large wheel, fine tracker)."""
    caps = []
    for span in (0.3, 0.5, 1.0):
        acc = cubesat.accounting(
            cubesat.configure([_design(panel_span_m=span, wheel_class="large", st_grade="fine")])[0]
        )
        caps.append((acc["available_power_w"], acc["usable_torque_nm"]))
    caps.sort()
    assert caps[0][0] < caps[1][0] < caps[2][0]
    assert caps[0][1] < caps[1][1] <= caps[2][1]
    c = _env(cubesat, "wheelLossCoefficient")
    assert caps[0][1] == pytest.approx(math.sqrt(caps[0][0] / (3 * c)), rel=1e-9)


def test_slew_energy_nonnegative_and_grows_with_angle(cubesat):
    """R-9: the energy used during the slew is nonnegative and increases with the slew angle."""
    energy = [
        cubesat.measure(_design(wheel_class="large"), slew_deg=a, **FAST)["slew_loss_energy_wh"]
        for a in (10.0, 30.0, 60.0)
    ]
    assert all(e >= 0 for e in energy) and energy == sorted(energy) and energy[0] < energy[-1]


# ---------------------------------------------------------------------------------------------
# R-6, R-11: attributes and flags
# ---------------------------------------------------------------------------------------------
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
FLAGS = ["settled", "momentum_ok", "torque_saturated_frac", "power_ok", "dod_ok"]


@pytest.fixture(scope="module")
def sample_rows(cubesat):
    designs = cubesat.sample_designs(8, seed=0)
    return cubesat.evaluate_designs(designs, **FAST)


def test_measure_returns_attributes_and_flags(sample_rows):
    """R-11: all ten attributes and five flags, finite; strictly positive when feasible."""
    for col in ATTRIBUTES + FLAGS + ["adcs_mass_kg"]:
        assert col in sample_rows.columns
    assert np.isfinite(sample_rows[ATTRIBUTES].to_numpy(dtype=float)).all()
    ok = sample_rows[sample_rows.settled & sample_rows.power_ok & sample_rows.dod_ok]
    assert len(ok) > 0
    assert (ok[ATTRIBUTES] > 0).all().all()
    assert (ok.eclipse_reserve_wh >= 0).all()


def test_slew_time_definition_and_ordering(cubesat, sample_rows):
    """Amendment 4: first entry below 1 degree (0.5 degree column), never after the 1 % settling."""
    assert "slew_time_05deg_s" in sample_rows.columns
    r = sample_rows
    assert (r.slew_time_s > 0).all()
    assert (r.slew_time_s <= r.slew_time_05deg_s).all()
    assert (r.slew_time_05deg_s <= r.settling_time_s + 1e-9).all()  # 0.5 deg > 1 % of 30 deg
    assert (r.slew_time_s <= FAST["t_end"]).all()


def test_slew_time_helper_first_entry_and_censoring():
    t = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    err = np.radians(np.array([30.0, 5.0, 0.8, 2.0, 0.1]))  # re-exits after 2 s: first entry wins
    res = SimpleNamespace(
        t=t, q=np.column_stack([np.sin(err / 2), 0 * err, 0 * err, np.cos(err / 2)])
    )
    assert cm.slew_time(res, 1.0) == 2.0
    assert cm.slew_time(res, 0.5) == 4.0
    assert cm.slew_time(res, 0.01) == 4.0  # never entered: censored at the horizon


def test_attributes_are_documented():
    """R-11: each attribute is documented with its mechanism in the module docstring."""
    doc = cm.__doc__
    for name in ATTRIBUTES + FLAGS:
        assert f"``{name}``" in doc, name


def test_flags_equal_independent_python_evaluation(cubesat, sample_rows):
    """R-6: ``power_ok`` and ``dod_ok`` from the model's constraints equal plain Python."""
    hk = _env(cubesat, "housekeepingLoad", "SI::W")
    idle = _env(cubesat, "wheelIdlePower", "SI::W")
    ecl_h = _env(cubesat, "eclipseDuration", "SI::h")
    max_dod = _env(cubesat, "maxDepthOfDischarge")
    from_python_power, from_python_dod = [], []
    for _, r in sample_rows.iterrows():
        tracker = cubesat.trackers[r.st_grade]
        p_tr = cubesat.value(cubesat.model.instantiate(tracker.part_def).get("power"), "SI::W")
        from_python_power.append(r.generated_power_w - hk - p_tr > 0)
        demand = (hk + p_tr + 3 * idle) * ecl_h + r.slew_loss_energy_wh
        from_python_dod.append(demand <= max_dod * r.battery_wh)
    assert list(sample_rows.power_ok) == from_python_power
    assert list(sample_rows.dod_ok) == from_python_dod


def test_flags_negative_controls(cubesat):
    """R-6 negative controls: a flag is False when the constraint is violated."""
    small = cubesat.measure(_design(battery_wh=20.0, st_grade="fine"), **FAST)
    assert small["dod_ok"] is False and small["eclipse_reserve_wh"] < 0
    heavy = SYSML.replace(
        "housekeepingLoad : PowerValue = 12.0 [W]", "housekeepingLoad : PowerValue = 60.0 [W]"
    )
    assert heavy != SYSML
    starved = cm.CubesatModel(heavy).measure(_design(), **FAST)
    assert starved["power_ok"] is False and starved["available_power_w"] < 0
    assert starved["usable_torque_nm"] == pytest.approx(0.01 * 0.002)  # 1 % of the medium wheel


def test_sampled_run_sweep_is_reproducible_and_log_capable(cubesat):
    """Verification record: run_sweep draws are reproducible, prefix-stable, log via log10."""
    src = (
        "package Q { private import ScalarValues::*;\n"
        "  calc def Samp { in logSpan : Real; in logCap : Real;\n"
        "    return : Real = 10.0 ** logSpan * 1000.0 + 10.0 ** logCap; } }"
    )
    m = cubesat.connection.load_from_content(src, strict=True)

    def draw(n, seed):
        t = m.run_sweep(
            "Q::Samp", {"logSpan": (-0.5, 0.0), "logCap": (1.0, 2.3)}, samples=n, seed=seed
        )
        return [(r.inputs["logSpan"], r.inputs["logCap"]) for r in t.rows]

    assert draw(4, 0) == draw(4, 0)
    assert draw(4, 0) == draw(9, 0)[:4]
    assert draw(4, 0) != draw(4, 1)


class Q:
    """Tiny alias for the client's Quantity, used where a unit object is already in hand."""

    def __new__(cls, magnitude, unit):
        from opensysml.values import Quantity

        return Quantity(magnitude, unit)


# ---------------------------------------------------------------------------------------------
# R-16: reproducibility of the committed dataset (run with ``-k reproduc``)
# ---------------------------------------------------------------------------------------------
# Recorded command; the cubesat defaults are --slew-deg 30 --t-end 600 (amendment 3, final).
GENERATE_COMMAND = (
    "uv run python examples/adcs/generate_dataset.py --model cubesat --n 1000 --seed 0"
    " --slew-deg 30 --t-end 600 --force"
)
CUBESAT_CSV = ADCS_DIR / "data" / "adcs_designs_cubesat.csv"
# Amendment 5, lever i: the aggressive-gain dataset beside the baseline (the baseline is untouched).
GAINS_GENERATE_COMMAND = (
    "uv run python examples/adcs/generate_dataset.py --model cubesat --gain-box aggressive"
    " --n 1000 --seed 0 --slew-deg 30 --t-end 600 --force"
)
GAINS_CSV = ADCS_DIR / "data" / "adcs_designs_cubesat_gains.csv"
DATASETS = [("baseline", CUBESAT_CSV), ("aggressive", GAINS_CSV)]


def _generate(n, workers=1, gain_box="baseline"):
    import generate_dataset as gd

    return gd.generate_cubesat(n, 0, workers=workers, gain_box=gain_box)


def test_generator_cli_has_the_cubesat_flags():
    out = subprocess.run(
        [sys.executable, str(ADCS_DIR / "generate_dataset.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0
    for flag in ("--model", "--slew-deg", "--t-end", "--gain-box"):
        assert flag in out.stdout


@pytest.mark.parametrize(("gain_box", "csv"), DATASETS)
def test_dataset_reproducible_first_20(cubesat, gain_box, csv):
    """Regenerate the first 20 designs with the recorded options; WP4 per-column tolerances."""
    import pandas as pd

    committed = pd.read_csv(csv)
    fresh = _generate(20, gain_box=gain_box)
    head = committed.iloc[:20].reset_index(drop=True)
    assert list(head.columns) == list(fresh.columns)
    exact = ["design_id", "seed", "wheel_class", "st_grade"]
    flags = ["settled", "momentum_ok", "power_ok", "dod_ok"]
    for col in exact + flags:
        assert (head[col].to_numpy() == fresh[col].to_numpy()).all(), col
    special = {"settling_time_s", "slew_time_s", "slew_time_05deg_s", "torque_saturated_frac"}
    for col in head.columns:
        if col in exact + flags or col in special:
            continue
        np.testing.assert_allclose(head[col], fresh[col], rtol=1e-4, atol=1e-6, err_msg=col)
    np.testing.assert_allclose(
        head.torque_saturated_frac, fresh.torque_saturated_frac, rtol=2e-2, atol=1e-12
    )
    for col in ("settling_time_s", "slew_time_s", "slew_time_05deg_s"):
        np.testing.assert_allclose(head[col], fresh[col], atol=0.5, err_msg=col)


@pytest.mark.parametrize("gain_box", ["baseline", "aggressive"])
def test_dataset_reproducible_same_platform_exact(cubesat, gain_box):
    """40 designs regenerated twice on the same platform are identical."""
    import pandas as pd

    pd.testing.assert_frame_equal(
        _generate(40, gain_box=gain_box), _generate(40, gain_box=gain_box)
    )
