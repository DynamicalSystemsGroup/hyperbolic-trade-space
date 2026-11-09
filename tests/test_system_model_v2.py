"""Tests for the v2 cubesat SysML model (WP15 part 15.1): one model, no constants in Python.

Every test that needs the opensysml runtime goes through the module-scoped ``v2`` fixture, which
FAILS (never skips) with a message naming the cause when the client cannot start. The tests read
the model the way a Python caller does (the query pattern in the model's top comment) and compare
it with the frozen oracle ``cubesat_model`` (the equivalence evidence): accounting quantities, the
ranges and the experiment's attributes. The slew itself is integrated by ``adcs_sim`` (the
measurement of record); the closed-form approximation in the model is compared with it on a sample.
"""

from __future__ import annotations

import math
import os
import pathlib
import re

import cubesat_model as cm
import numpy as np
import pytest
from adcs_sim import make_config, simulate_adcs
from opensysml.errors import ModelError
from opensysml.values import Quantity

ADCS_DIR = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs"
MODEL = ADCS_DIR / "model_v2" / "cubesat.sysml"
TEXT = MODEL.read_text()
P = "CubesatTradeSpaceV2"
FAST = {"t_end": 600.0, "max_step": 1.0}  # coarser than the dataset (0.5 s), for tests only

SECTIONS = [
    "1. CONFIGURATION SPACE",
    "2. THE CUBESAT",
    "3. ACCOUNTING",
    "4. SCENARIOS",
    "5. REQUIREMENTS, SATISFACTION AND VERIFICATION (15.2)",
    "6. THE EXPERIMENT",
    "7. NAMED CONFIGURATIONS",
]
# The eight attributes the experiment computes, in order, with the unit each is read in. The
# settling time and the slew time are measured, not computed: the oracle takes them from the
# measurement, so the analysis neither receives nor returns them.
ATTRIBUTES = [
    ("pointing_error_deg", "SI::degree"),
    ("total_mass_kg", "SI::kg"),
    ("control_effort", "SI::N*SI::m*SI::s"),
    ("power_margin_w", "SI::W"),
    ("energy_balance_wh", "SI::W*SI::h"),
    ("eclipse_reserve_wh", "SI::W*SI::h"),
    ("peak_slew_power_w", "SI::W"),
    ("dod_eclipse", None),
]


class V2:
    """The loaded v2 model and the reads a Python caller makes of it (no number is copied here)."""

    def __init__(self, text: str):
        self.connection = cm.get_connection()
        self.text = text
        self.model = self.connection.load_from_content(text, strict=True)

    # -- units and values ------------------------------------------------------------------
    def unit(self, expression: str):
        return self.model.eval(f"1.0 [{expression}]").unit

    def value(self, quantity, unit: str | None = None) -> float:
        if isinstance(quantity, list):
            quantity = quantity[0]
        if isinstance(quantity, Quantity):
            return float(quantity.in_unit(self.unit(unit)))
        return float(quantity)

    def read(self, expression: str, unit: str | None = None) -> float:
        return self.value(self.model.eval(f"{P}::{expression}"), unit)

    # -- the configuration space, read from the model ---------------------------------------
    def span_range(self):
        return tuple(self.read(f"designRanges.panelSpan{k}", "SI::m") for k in ("Min", "Max"))

    def battery_range(self):
        names = ("Min", "Max")
        return tuple(self.read(f"designRanges.batteryCapacity{k}", "SI::W*SI::h") for k in names)

    def gain_box(self, box: str):
        return {k: self.read(f"{box}.{k}") for k in ("KpMin", "KpMax", "KdMin", "KdMax")}

    def literals(self, enum: str):
        return [c.name for c in self.model.find(f"{P}::{enum}").children()]

    def alternatives(self, abstract: str, enum_attr: str) -> dict[str, str]:
        """Concrete specializations of an abstract part def, keyed by their enumeration literal."""
        target = f"{P}::{abstract}"
        table = {}
        for q in self.model.query(
            scope=[P], where={"property": "@type", "operator": "=", "value": "PartDefinition"}
        ):
            if any(sp.target_id == target for sp in self.model.find(q.id).specializations):
                literal = self.model.instantiate(q.id).get(enum_attr)
                table[(literal.name or literal.literal_id).split("::")[-1]] = q.id
        return table

    # -- configurations ---------------------------------------------------------------------
    def configure(self, designs: list[dict]):
        """Instantiate each design as a ``Cubesat`` in a second package of the same loaded text."""
        wheels = self.alternatives("ReactionWheel", "wheelClass")
        trackers = self.alternatives("StarTracker", "grade")
        usages = "".join(
            f"    part cfg_{int(d['design_id'])} : {P}::Cubesat {{\n"
            f"        :>> panelSpan default = {d['panel_span_m']:.17e} [SI::m];\n"
            f"        :>> batteryCapacity default = {d['battery_wh']:.17e} [SI::W*SI::h];\n"
            f"        part :>> wheel : {wheels[d['wheel_class']]};\n"
            f"        part :>> tracker : {trackers[d['st_grade']]};\n"
            f"        part :>> controller {{ :>> Kp default = {d['Kp']:.17e};"
            f" :>> Kd default = {d['Kd']:.17e}; }}\n    }}\n"
            for d in designs
        )
        loaded = self.connection.load_from_content(
            self.text + "\npackage Configurations {\n" + usages + "}\n", strict=True
        )
        return loaded, [f"Configurations::cfg_{int(d['design_id'])}" for d in designs]

    def experiment(self, model, symbol: str, measured: dict) -> dict:
        """Run the model's analysis on a configuration; the eight computed attributes by name."""
        unit = self.unit
        args = {
            "torqueSquaredIntegral": measured["torque_squared_integral"],
            "peakTorque": Quantity(measured["peak_torque"], unit("SI::N*SI::m")),
            "peakMomentum": Quantity(measured["peak_momentum"], unit("SI::N*SI::m*SI::s")),
            "controlEffort": Quantity(measured["control_effort"], unit("SI::N*SI::m*SI::s")),
            "censored": bool(measured["censored"]),
        }
        out = model.run_analysis(f"{P}::SlewExperiment", subject=symbol, named_arguments=args)
        return {
            name: self.value(q, u)
            for (name, u), q in zip(ATTRIBUTES, out.outputs["attributes"], strict=True)
        }


@pytest.fixture(scope="module")
def v2():
    """The loaded v2 model; a named-cause failure, never a skip, when the client cannot start."""
    try:
        return V2(TEXT)
    except cm.OpenSysMLUnavailable as exc:
        flag = " (REQUIRE_OPENSYSML is set)" if os.environ.get("REQUIRE_OPENSYSML") else ""
        pytest.fail(f"the opensysml client could not start{flag}: {exc}", pytrace=False)


@pytest.fixture(scope="module")
def frozen():
    """The frozen oracle (the WP4b model), loaded once."""
    try:
        return cm.load_model()
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


@pytest.fixture(scope="module")
def sample(frozen):
    """Eight designs from the frozen sampler (aggressive gain box ranges are read below)."""
    return cm.load_model(gain_box="aggressive").sample_designs(8, seed=3)


def _rel(a: float, b: float) -> float:
    return abs(a - b) / max(abs(b), 1e-300)


def _symbols(v2: V2, kind: str) -> set[str]:
    return {
        q.properties["name"]
        for q in v2.model.query(
            scope=[P], where={"property": "@type", "operator": "=", "value": kind}
        )
    }


# ---------------------------------------------------------------------------------------------
# R-1: one file, one package, strict load, sections in order
# ---------------------------------------------------------------------------------------------
def test_strict_load_self_check_and_one_package(v2):
    """R-1: strict load, no error diagnostics, self_check holds, one package, illustrative."""
    assert v2.model.ok
    assert not [d for d in v2.model.diagnostics if d.severity == "error"]
    assert v2.model.self_check().status == "holds"
    assert len(re.findall(r"^package\s", TEXT, flags=re.M)) == 1
    assert f"package {P} " in TEXT
    assert "illustrative" in TEXT.lower() and "documentation of a demonstration" in TEXT


def test_symbol_kinds_by_query(v2):
    """R-1: the model declares each kind of element the sections promise."""
    assert _symbols(v2, "EnumerationDefinition") == {"WheelClass", "TrackerGrade"}
    parts = _symbols(v2, "PartDefinition")
    assert {"ReactionWheel", "SmallWheel", "MediumWheel", "LargeWheel"} <= parts
    assert {"StarTracker", "CoarseTracker", "MediumTracker", "FineTracker"} <= parts
    assert {"Cubesat", "Bus", "SolarPanel", "Battery", "Controller", "GainBox"} <= parts
    assert {"DesignRanges", "Environment", "Scenario"} <= parts
    calcs = _symbols(v2, "CalculationDefinition")
    assert {
        "MassAccounting",
        "StructureMass",
        "AdcsMass",
        "GeneratedPower",
        "AvailablePower",
    } <= calcs
    assert {"UsableWheelTorque", "SlewLossEnergy", "EclipseDemand", "DepthOfDischarge"} <= calcs
    assert {"EclipseReserve", "EnergyBalance", "PeakSlewPower", "PowerMargin"} <= calcs
    assert {"InertiaX", "InertiaY", "InertiaZ", "PointingError"} <= calcs
    assert {
        "TorqueLimitedSlewTime",
        "LinearSlewTime",
        "SlewTimeEstimate",
        "IsTorqueLimited",
    } <= calcs
    assert _symbols(v2, "AnalysisCaseDefinition") == {"SlewExperiment"}
    usages = _symbols(v2, "PartUsage")
    assert {
        "designRanges",
        "baselineGains",
        "aggressiveGains",
        "nominalSlew",
        "environment",
    } <= usages
    assert {"cubesatBaseline", "cubesatAgile", "cubesatCompact"} <= usages


def test_sections_in_order_each_with_header_and_doc():
    """R-1: the seven sections appear in the stated order, each followed by a doc comment."""
    positions = [TEXT.index(f"// {title}") for title in SECTIONS]
    assert positions == sorted(positions)
    for pos in positions:
        header_end = TEXT.index("// ====", pos)  # the closing rule of the header
        assert TEXT[header_end:].lstrip("/= \n").startswith(("doc /*", "part def", "calc def")), (
            TEXT[pos : pos + 60]
        )
    for title in SECTIONS[:4] + SECTIONS[5:6]:
        pos = TEXT.index(f"// {title}")
        nxt = TEXT.index("// ====", TEXT.index("// ====", pos) + 10)
        assert "doc /*" in TEXT[pos:nxt], title


def test_marked_region_for_part_15_2_is_filled_in_section_five():
    """The requirements region is marked once, sits in section 5, and 15.2 filled it."""
    assert TEXT.count("// BEGIN 15.2") == 1 and TEXT.count("// END 15.2") == 1
    begin, end = TEXT.index("// BEGIN 15.2"), TEXT.index("// END 15.2")
    assert begin < end and "requirement def" in TEXT[begin:end]
    assert TEXT.index(f"// {SECTIONS[4]}") < begin < TEXT.index(f"// {SECTIONS[5]}")


def test_every_constant_has_a_doc_rationale():
    """Illustrative-only: constants sit under doc comments, as in the frozen model."""
    assert TEXT.count("doc /*") >= 18
    assert len(TEXT.splitlines()) <= 700


# ---------------------------------------------------------------------------------------------
# R-2: ranges, enumerations, gain boxes and scenario numbers are queryable model elements
# ---------------------------------------------------------------------------------------------
def test_ranges_enums_gain_boxes_and_scenario_agree_with_the_frozen_model(v2, frozen):
    """The v2 model carries the frozen numbers, read by the query pattern of its top comment."""
    base = cm.load_model(gain_box="baseline")
    assert v2.span_range() == pytest.approx(frozen.panel_span_range, rel=1e-12)
    assert v2.battery_range() == pytest.approx(frozen.battery_wh_range, rel=1e-12)
    box = v2.gain_box("baselineGains")
    assert (box["KpMin"], box["KpMax"]) == pytest.approx(base.kp_range)
    assert (box["KdMin"], box["KdMax"]) == pytest.approx(base.kd_range)
    box = v2.gain_box("aggressiveGains")
    agg = cm.load_model(gain_box="aggressive")
    assert (box["KpMin"], box["KpMax"]) == pytest.approx(agg.kp_range)
    assert (box["KdMin"], box["KdMax"]) == pytest.approx(agg.kd_range)
    assert v2.literals("WheelClass") == frozen.wheel_classes
    assert v2.literals("TrackerGrade") == frozen.tracker_grades
    assert set(v2.alternatives("ReactionWheel", "wheelClass")) == set(frozen.wheel_classes)
    assert set(v2.alternatives("StarTracker", "grade")) == set(frozen.tracker_grades)
    assert v2.read("nominalSlew.slewAngle", "SI::degree") == pytest.approx(cm.SLEW_DEG)
    assert v2.read("nominalSlew.horizon", "SI::s") == pytest.approx(cm.T_END)
    assert v2.read("nominalSlew.timeStep", "SI::s") == pytest.approx(cm.MAX_STEP)
    assert v2.read("nominalSlew.slewBand", "SI::degree") == pytest.approx(cm.SLEW_BAND_DEG)
    sens = v2.read("nominalSlew.slewBandSensitivity", "SI::degree")
    assert sens == pytest.approx(cm.SLEW_BAND_SENSITIVITY_DEG)


def test_wheel_tables_match_the_frozen_model(v2, frozen):
    """Momentum capacity of every wheel class equals the frozen model's."""
    alts = v2.alternatives("ReactionWheel", "wheelClass")
    got = {
        lit: v2.value(v2.model.instantiate(sym).get("maxMomentum"), "SI::N*SI::m*SI::s")
        for lit, sym in alts.items()
    }
    assert got == pytest.approx(frozen.wheel_capacities(), rel=1e-12)


def test_edit_a_copy_changes_what_a_query_returns():
    """R-2: editing a range, an enum literal or a scenario value in a copy changes the reads."""
    edited = (
        TEXT.replace("panelSpanMax : LengthValue = 1.0 [m]", "panelSpanMax : LengthValue = 1.2 [m]")
        .replace("slewAngle : PlaneAngleValue = 30.0", "slewAngle : PlaneAngleValue = 45.0")
        .replace("fine", "sharp")
    )
    assert edited != TEXT
    copy = V2(edited)
    assert copy.span_range()[1] == pytest.approx(1.2)
    assert copy.read("nominalSlew.slewAngle", "SI::degree") == pytest.approx(45.0)
    assert copy.literals("TrackerGrade") == ["coarse", "medium", "sharp"]
    assert "sharp" in copy.alternatives("StarTracker", "grade")


def test_negative_control_broken_copy_fails_the_strict_load():
    """R-1 negative control: a broken source must not load strictly."""
    broken = TEXT.replace("attribute mass : MassValue = 10.0 [kg];", "attribute mass : Nope = 1;")
    assert broken != TEXT
    with pytest.raises(ModelError):
        cm.get_connection().load_from_content(broken, strict=True)


# ---------------------------------------------------------------------------------------------
# Equivalence with the frozen oracle
# ---------------------------------------------------------------------------------------------
def test_accounting_calcs_reproduce_the_frozen_accounting(v2, frozen, sample, capsys):
    """The model's accounting equals the frozen model's on sampled configurations (1e-9 rel)."""
    designs = [dict(r) for _, r in sample.iterrows()]
    loaded, symbols = v2.configure(designs)
    old = frozen.configure(designs)
    worst = 0.0
    for d, sym, cfg in zip(designs, symbols, old, strict=True):
        inst = loaded.instantiate(sym)
        want = frozen.accounting(cfg)
        got = {
            "total_mass_kg": v2.value(inst.get("totalMass"), "SI::kg"),
            "structure_mass_kg": v2.value(inst.get("structureMass"), "SI::kg"),
            "panel_mass_kg": v2.value(inst.get("panelPlus").get("mass"), "SI::kg"),
            "battery_mass_kg": v2.value(inst.get("battery").get("mass"), "SI::kg"),
            "generated_power_w": v2.value(inst.get("generatedPower"), "SI::W"),
            "available_power_w": v2.value(inst.get("availablePower"), "SI::W"),
            "usable_torque_nm": v2.value(inst.get("usableWheelTorque"), "SI::N*SI::m"),
        }
        for key, value in want.items():
            worst = max(worst, _rel(got[key], value))
        cap = v2.value(inst.get("momentumCapacity"), "SI::N*SI::m*SI::s")
        worst = max(worst, _rel(cap, frozen.wheel_capacities()[d["wheel_class"]]))
        meas_adcs = frozen.sim_params(cfg)
        adcs_mass = 3 * meas_adcs["wheelMass"] + meas_adcs["stMass"] + meas_adcs["imuMass"]
        worst = max(worst, _rel(v2.value(inst.get("adcsMass"), "SI::kg"), adcs_mass))
    with capsys.disabled():
        print(f"\n[equivalence] accounting, {len(designs)} configs: max rel diff {worst:.2e}")
    assert worst < 1e-9


def _measure_slew(frozen, cfg, t_end=FAST["t_end"], max_step=FAST["max_step"]):
    """Integrate the slew with the frozen parameters (the measurement of record)."""
    params = frozen.sim_params(cfg)
    sim = make_config(
        params,
        params["Kp"],
        params["Kd"],
        wheel={"maxTorque": params["maxTorque"], "maxMomentum": params["maxMomentum"]},
        t_end=t_end,
        initial_error_deg=cm.SLEW_DEG,
        max_step=max_step,
    )
    res = simulate_adcs(sim)
    summ = res.summary()
    tau = np.linalg.norm(res.tau_ctrl, axis=1)
    err_deg = np.degrees(2 * np.linalg.norm(res.q[:, :3], axis=1))
    return {
        "torque_squared_integral": float(np.trapezoid(tau**2, res.t)),
        "peak_torque": float(np.max(tau)),
        "peak_momentum": summ["peak_wheel_momentum"],
        "settling_time": summ["settling_time_s"],
        "slew_time": cm.slew_time(res, cm.SLEW_BAND_DEG),
        "control_effort": summ["control_effort"],
        "censored": bool(not np.any(err_deg < cm.SLEW_BAND_DEG)),
    }


def test_analysis_reproduces_the_frozen_attributes(v2, frozen, sample, capsys):
    """run_analysis on the measured slew equals the frozen attributes (1e-9 rel, 5 configs)."""
    designs = [dict(r) for _, r in sample.head(5).iterrows()]
    loaded, symbols = v2.configure(designs)
    old = frozen.configure(designs)
    worst, worst_key = 0.0, ""
    for sym, cfg in zip(symbols, old, strict=True):
        measured = _measure_slew(frozen, cfg)
        want = frozen.measure(cfg, **FAST)
        got = v2.experiment(loaded, sym, measured)
        assert list(got) == [name for name, _ in ATTRIBUTES]
        for name, _ in ATTRIBUTES:
            diff = _rel(got[name], want[name])
            if diff > worst:
                worst, worst_key = diff, name
    with capsys.disabled():
        print(
            f"\n[equivalence] eight computed attributes, 5 configs: "
            f"max rel diff {worst:.2e} ({worst_key})"
        )
    assert worst < 1e-9


def test_analysis_with_equal_measured_times_needs_no_workaround(v2):
    """The runtime refuses a unique tuple with two equal entries; the analysis returns computed
    attributes only, so a measurement whose settling time equals its slew time is analysed in
    one call, whatever the two values are."""
    measured = {
        "torque_squared_integral": 1e-5,
        "peak_torque": 1e-3,
        "peak_momentum": 4e-3,
        "settling_time": 14.398119154048933,
        "slew_time": 14.398119154048933,
        "control_effort": 1e-2,
        "censored": False,
    }
    got = v2.experiment(v2.model, f"{P}::cubesatBaseline", measured)
    assert list(got) == [name for name, _ in ATTRIBUTES]
    assert len(set(got.values())) == len(ATTRIBUTES)
    body = TEXT[TEXT.index("analysis def SlewExperiment") :]
    body = body[: body.index("\n    }\n")]
    assert "settlingTime" not in body and "slewTime" not in body


# ---------------------------------------------------------------------------------------------
# The closed-form slew approximation against the ODE (OD2)
# ---------------------------------------------------------------------------------------------
def test_closed_form_slew_time_against_the_ode(v2, frozen, capsys):
    """The closed-form slew time tracks the ODE slew time within a loose factor on 10 configs.

    Regimes. The estimate is the larger of the bang-bang time (torque-limited) and the linear
    dominant-pole time, both to the 1 degree band. On this sample (seed 5, aggressive gain box)
    it lies within 25 percent of the ODE in both regimes (ratios 0.79 to 1.25; median error 21
    percent where the cap binds, 11 percent in the linear regime). The bound asserted is loose
    (0.5 to 2): the approximation ignores the braking profile of the saturated PD law and the
    nonlinearity of sin(theta/2), so it is for model checking, not a replacement for the ODE.
    """
    agg = cm.load_model(gain_box="aggressive")
    designs = [dict(r) for _, r in agg.sample_designs(10, seed=5).iterrows()]
    loaded, symbols = v2.configure(designs)
    old = frozen.configure(designs)
    rows = []
    for sym, cfg in zip(symbols, old, strict=True):
        ode = _measure_slew(frozen, cfg, **{"t_end": 600.0, "max_step": 0.5})["slew_time"]
        est = v2.value(loaded.eval(f"{P}::SlewTimeEstimate({sym}, {P}::nominalSlew)"), "SI::s")
        limited = loaded.eval(f"{P}::IsTorqueLimited({sym}, {P}::nominalSlew)")
        limited = limited[0] if isinstance(limited, list) else limited
        rows.append((ode, est, bool(limited)))
    ratios = np.array([est / ode for ode, est, _ in rows])
    rel_err = np.abs(ratios - 1.0)
    mask = np.array([limited for _, _, limited in rows])
    with capsys.disabled():
        print(
            "\n[closed-form slew vs ODE, 10 configs] ratio estimate/ODE min "
            f"{ratios.min():.2f} median {np.median(ratios):.2f} max {ratios.max():.2f}; relative "
            f"error median {np.median(rel_err):.1%} max {rel_err.max():.1%}; "
            f"torque-limited in {sum(r[2] for r in rows)} of {len(rows)}; "
            f"median error torque-limited {np.median(rel_err[mask]):.1%}, "
            f"linear {np.median(rel_err[~mask]):.1%}"
        )
    assert ratios.min() > 0.5 and ratios.max() < 2.0
    assert np.median(rel_err) < 0.35


def test_both_slew_regimes_occur_across_the_named_configurations(v2):
    """IsTorqueLimited separates a torque-limited configuration from a linear one."""
    verdict = {}
    for name in ("cubesatBaseline", "cubesatAgile", "cubesatCompact"):
        out = v2.model.eval(f"{P}::IsTorqueLimited({P}::{name}, {P}::nominalSlew)")
        verdict[name] = bool(out[0] if isinstance(out, list) else out)
    assert True in verdict.values() and False in verdict.values(), verdict


def test_baseline_reads_as_documented(v2):
    """The named baseline has the frozen baseline mass and the medium wheel torque."""
    inst = v2.model.instantiate(f"{P}::cubesatBaseline")
    assert v2.value(inst.get("totalMass"), "SI::kg") == pytest.approx(13.29142857142857, rel=1e-12)
    assert math.isclose(v2.value(inst.get("usableWheelTorque"), "SI::N*SI::m"), 0.002)
