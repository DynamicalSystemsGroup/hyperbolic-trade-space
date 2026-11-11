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
TEXT = MODEL.read_text(encoding="utf-8")
P = "CubesatTradeSpaceV2"
FAST = {"t_end": 600.0, "max_step": 1.0}  # coarser than the dataset (0.5 s), for tests only

# The model adopted at WP23's data gate (WP23-decisions.md); the WP22 version it replaced is in
# history at d3018ba, the WP15 version at 2d13465. What WP23 changed against the WP22 version is
# stated once, here: the slew time left (WP16: one time metric, the settling time; the slew-time
# and slew-band requirements fold into SettledRequirement, the measurement lost `slewTime` and
# `censored`, the scenario lost the sensitivity band), a launch cost (calc `LaunchCost`, the MoE on
# the total mass) and a part `Budgets` of proposed thresholds entered, and the line cap grew by the
# four requirement defs, the calc, the part and the MoE/MoP docs it added. Round 2 (the coupling
# check, WP23-review.md) added the battery's discharge rating, the calcs `BatteryPeakPower` and
# `EclipsePeakLoad` and the requirement that reads them; the cap grew by those. The close-out
# (WP23-closeout-scope-of-work.md, D-11): the eclipse reserve's calc and requirement left (its
# requirement was the depth-of-discharge requirement restated), and the four thresholds became the
# supervisor's literal values.
# The calc defs of the WP22 version, every one kept with its body (pinned so the set is readable
# here; the bodies' equality with the frozen oracle is R-6 of test_system_model_v2_r1.py).
WP22_CALCS = {
    "AdcsMass", "AvailablePower", "BaseLoad", "DampingRatio", "DepthOfDischarge",
    "DominantPoleRate", "EclipseDemand", "EnergyBalance", "GeneratedPower",
    "GravityGradientTorque", "InertiaX", "InertiaY", "InertiaZ", "IsTorqueLimited",
    "LinearSlewTime", "MassAccounting", "NaturalFrequency", "OrbitPeriod", "PeakSlewPower",
    "PointingError", "PowerMargin", "SlewLossEnergy", "SlewTimeEstimate", "StructureMass",
    "TorqueLimitedSlewTime", "UsableWheelTorque",
}  # fmt: skip
EXPECT = {
    "line_cap": 1200,
    "calcs": {
        "LaunchCost",
        "BatteryPeakPower",
        "EclipsePeakLoad",
        "MomentumHeadroom",
        # "No floating requirements": the battery peak power over the eclipse peak load, traded
        "BatteryPeakPowerRatio",
        # WP30 stage 3b, the cost model (section 3): the pricing curve, the single-unit prices that
        # read the configuration, each part's total, the fleet's build cost, the two traded costs
        "PartTotal",
        "PanelPrice",
        "BatteryPrice",
        "WheelPrice",
        "TrackerPrice",
        "BusTotal",
        "PanelTotal",
        "BatteryTotal",
        "WheelTotal",
        "TrackerTotal",
        "AssemblyTotal",
        "FleetBuildCost",
        "FleetCost",
        "UnitCost",
    },
    "parts": {"Budgets"},
}

SECTIONS = [
    "1. CONFIGURATION SPACE",
    "2. THE CUBESAT",
    "3. ACCOUNTING",
    "4. SCENARIOS",
    "5. REQUIREMENTS, SATISFACTION AND VERIFICATION",  # header continues "(assessment view; ...)"
    "6. THE EXPERIMENT",
    "7. NAMED CONFIGURATIONS",
]
# The ten attributes the experiment computes (the eclipse reserve left at the close-out; the
# momentum headroom joined at WP30, stage 3a; the available power and the battery peak power ratio
# after "No floating requirements"), in order, with the unit each is read in. The
# settling time is measured, not computed: the oracle takes it from the measurement, so the
# analysis neither receives nor returns it.
ATTRIBUTES = [
    ("pointing_error_deg", "SI::degree"),
    ("total_mass_kg", "SI::kg"),
    ("control_effort", "SI::N*SI::m*SI::s"),
    ("power_margin_w", "SI::W"),
    ("energy_balance_wh", "SI::W*SI::h"),
    ("peak_slew_power_w", "SI::W"),
    ("dod_eclipse", None),
    ("momentum_headroom", None),
    ("available_power_w", "SI::W"),
    ("battery_peak_power_ratio", None),
]


def frozen_battery_peak_power_ratio(cfg, want: dict) -> float:
    """The battery peak power ratio of a configuration of the frozen model: the pack's rated power
    (1.0 per hour times the capacity, the model's discharge rate) over the eclipse peak load
    (the 12 W housekeeping load plus the peak slew power). The frozen model has no such metric
    (WP30, "No floating requirements"); this is the model's calc read in Python."""
    return cfg.design["battery_wh"] * 1.0 / (12.0 + want["peak_slew_power_w"])


class V2:
    """The loaded v2 model and the reads a Python caller makes of it (no number is copied here)."""

    def __init__(self, text: str, name: str = "adopted", path: pathlib.Path = MODEL):
        self.connection = cm.get_connection()
        self.text, self.name, self.path = text, name, path
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
        """Run the model's analysis on a configuration; the computed attributes by name."""
        unit = self.unit
        args = {
            "torqueSquaredIntegral": measured["torque_squared_integral"],
            "peakTorque": Quantity(measured["peak_torque"], unit("SI::N*SI::m")),
            "peakMomentum": Quantity(measured["peak_momentum"], unit("SI::N*SI::m*SI::s")),
            "controlEffort": Quantity(measured["control_effort"], unit("SI::N*SI::m*SI::s")),
        }
        if "in censored" in self.text:  # the adopted model's analysis takes the slew censoring
            args["censored"] = bool(measured["censored"])
        out = model.run_analysis(f"{P}::SlewExperiment", subject=symbol, named_arguments=args)
        return {
            name: self.value(q, u)
            for (name, u), q in zip(ATTRIBUTES, out.outputs["attributes"], strict=True)
        }


@pytest.fixture(scope="module")
def v2():
    """The model, loaded; a named-cause failure, never a skip, when the client cannot start."""
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
    assert len(re.findall(r"^package\s", v2.text, flags=re.M)) == 1
    assert f"package {P} " in v2.text
    assert "illustrative" in v2.text.lower() and "documentation of a demonstration" in v2.text


def test_symbol_kinds_by_query(v2):
    """R-1: the model declares each kind of element the sections promise."""
    assert _symbols(v2, "EnumerationDefinition") == {"WheelClass", "TrackerGrade"}
    parts = _symbols(v2, "PartDefinition")
    assert {"ReactionWheel", "SmallWheel", "MediumWheel", "LargeWheel"} <= parts
    assert {"StarTracker", "CoarseTracker", "MediumTracker", "FineTracker"} <= parts
    assert {"Cubesat", "Bus", "SolarPanel", "Battery", "Controller", "GainBox"} <= parts
    assert {"DesignRanges", "Environment", "Scenario"} | EXPECT["parts"] <= parts
    calcs = _symbols(v2, "CalculationDefinition")
    assert EXPECT["calcs"] <= calcs
    assert {
        "MassAccounting",
        "StructureMass",
        "AdcsMass",
        "GeneratedPower",
        "AvailablePower",
    } <= calcs
    assert {"UsableWheelTorque", "SlewLossEnergy", "EclipseDemand", "DepthOfDischarge"} <= calcs
    assert {"EnergyBalance", "PeakSlewPower", "PowerMargin"} <= calcs
    assert "EclipseReserve" not in calcs  # the close-out: the depth of discharge carries it
    assert {"InertiaX", "InertiaY", "InertiaZ", "PointingError"} <= calcs
    assert {
        "TorqueLimitedSlewTime",
        "LinearSlewTime",
        "SlewTimeEstimate",
        "IsTorqueLimited",
    } <= calcs
    # the slew experiment, and the two cost analyses (WP30: an analysis's result refuses equal
    # entries and the unit cost equals the fleet cost at one satellite)
    assert _symbols(v2, "AnalysisCaseDefinition") == {
        "SlewExperiment", "UnitCostExperiment", "FleetCostExperiment",
    }  # fmt: skip
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
    text = TEXT
    positions = [text.index(f"// {title}") for title in SECTIONS]
    assert positions == sorted(positions)
    for pos in positions:
        header_end = text.index("// ====", pos)  # the closing rule of the header
        assert text[header_end:].lstrip("/= \n").startswith(("doc /*", "part def", "calc def")), (
            text[pos : pos + 60]
        )
    for title in SECTIONS[:4] + SECTIONS[5:6]:
        pos = text.index(f"// {title}")
        nxt = text.index("// ====", text.index("// ====", pos) + 10)
        assert "doc /*" in text[pos:nxt], title


def test_marked_region_for_part_15_2_is_filled_in_section_five():
    """The requirements region is marked once, sits in section 5, and 15.2 filled it."""
    text = TEXT
    assert text.count("// BEGIN 15.2") == 1 and text.count("// END 15.2") == 1
    begin, end = text.index("// BEGIN 15.2"), text.index("// END 15.2")
    assert begin < end and "requirement def" in text[begin:end]
    assert text.index(f"// {SECTIONS[4]}") < begin < text.index(f"// {SECTIONS[5]}")


def test_every_constant_has_a_doc_rationale():
    """Illustrative-only: constants sit under doc comments, as in the frozen model.

    The length cap was 700 lines for the WP15 model and 730 for the WP22 model (729 lines). WP23
    added four requirement defs, the launch-cost calc, the budgets part and an MoE/MoP doc on each
    traded metric (round 1, 831 lines), then the battery rating, two calcs and the battery peak
    power requirement (round 2, 871 lines); the cap was 900 there, which held the model where
    round 2 left it. WP30 stage 3a took it to 898 (the momentum headroom) and stage 3b added the
    cost model the scope (G3 to G5) asks for: the fleet size, six per-part pricing curves with
    their prices and shares, the fleet and unit costs, two requirements and two analyses (about
    230 lines, most of them the rationale of each price and curve) and the final values added each
    part's source and date and the coverage statement (about 45 lines); the cap is 1200
    (``EXPECT``): the model stays one readable file (WP22 definition of good).
    """
    text = TEXT
    assert text.count("doc /*") >= 18
    assert len(text.splitlines()) <= EXPECT["line_cap"]


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
    assert v2.read("nominalSlew.settlingFraction") == pytest.approx(0.01)
    assert "slewBandSensitivity" not in v2.text  # left with the slew time (WP23 D-1)


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
    text = TEXT
    edited = (
        text.replace("panelSpanMax : LengthValue = 1.0 [m]", "panelSpanMax : LengthValue = 1.2 [m]")
        .replace("slewAngle : PlaneAngleValue = 30.0", "slewAngle : PlaneAngleValue = 45.0")
        .replace("fine", "sharp")
    )
    assert edited != text
    copy = V2(edited)
    assert copy.span_range()[1] == pytest.approx(1.2)
    assert copy.read("nominalSlew.slewAngle", "SI::degree") == pytest.approx(45.0)
    assert copy.literals("TrackerGrade") == ["coarse", "medium", "sharp"]
    assert "sharp" in copy.alternatives("StarTracker", "grade")


def test_negative_control_broken_copy_fails_the_strict_load():
    """R-1 negative control: a broken source must not load strictly."""
    text = TEXT
    broken = text.replace("attribute mass : MassValue = 10.0 [kg];", "attribute mass : Nope = 1;")
    assert broken != text
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
        # the frozen model has no momentum headroom: it is the wheel class capacity over the peak
        # momentum measured here (the inverse of the utilisation, WP4b), so it is compared as that
        want["momentum_headroom"] = (
            frozen.sim_params(cfg)["maxMomentum"] / measured["peak_momentum"]
        )
        want["battery_peak_power_ratio"] = frozen_battery_peak_power_ratio(cfg, want)
        got = v2.experiment(loaded, sym, measured)
        assert list(got) == [name for name, _ in ATTRIBUTES]
        for name, _ in ATTRIBUTES:
            diff = _rel(got[name], want[name])
            if diff > worst:
                worst, worst_key = diff, name
    with capsys.disabled():
        print(
            f"\n[equivalence] the ten computed traded metrics, 5 configs: "
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
    body = v2.text[v2.text.index("analysis def SlewExperiment") :]
    body = body[: body.index("\n    }\n")]
    assert "settlingTime" not in body and "slewTime" not in body


# ---------------------------------------------------------------------------------------------
# WP23 D-1: what the gate's model adds and removes against the WP22 version (R-4, R-5 of WP23)
# ---------------------------------------------------------------------------------------------
def test_the_calc_defs_are_the_wp22_set_plus_the_adds(v2):
    """WP23 changed no accounting: the calc defs are the WP22 version's (``WP22_CALCS``, every
    body kept; their agreement with the frozen oracle is R-6 of test_system_model_v2_r1.py) plus
    the launch cost (round 1) and the battery's peak power and the eclipse peak load (round 2),
    none of the three traded, WP30's momentum headroom, the ninth traded metric (D-1 (a) of
    spike C, WP30-decisions.md), the battery peak power ratio (traded with the available power, "No floating requirements"),
        and the cost model of WP30 stage 3b (spike D; the unit cost and
    the fleet cost are the tenth and eleventh traded metrics, OD1 (a))."""
    calcs = set(re.findall(r"^    calc def (\w+)", v2.text, flags=re.M))
    assert calcs == WP22_CALCS | EXPECT["calcs"]
    assert _symbols(v2, "CalculationDefinition") >= calcs


def test_slew_time_has_left_the_measurement_and_the_requirements(v2):
    """WP23 R-5 on the model: no slew-time quantity, requirement or censoring remains; the settling
    time is the one time metric and its requirement carries the fold. The closed-form calcs of
    section 4 keep their names (the comparison code reads them)."""
    text = v2.text
    code = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
    assert "slewTime" not in code and "censored" not in code
    assert "SlewTimeRequirement" not in code and "SlewBandRequirement" not in code
    assert "slewBandSensitivity" not in code
    defs = _symbols(v2, "RequirementDefinition")
    assert "SettledRequirement" in defs and "slew-band requirements" in text
    assert "settlingTime" in text[text.index("part def SlewMeasurement") :]


def test_launch_cost_is_the_rate_times_the_total_mass_and_increases_with_it(v2):
    """WP23 R-4: launch cost = rate x total mass at the three named configurations (read from the
    model, nothing typed here), so the ordering by cost is the ordering by mass; the launch budget
    requirement reads it and holds on the baseline."""
    rate = v2.read("environment.launchRate")
    assert rate > 0
    rows = []
    for config in ("cubesatCompact", "cubesatBaseline", "cubesatAgile"):
        inst = v2.model.instantiate(f"{P}::{config}")
        mass = v2.value(inst.get("totalMass"), "SI::kg")
        cost = v2.value(inst.get("launchCost"))
        assert cost == pytest.approx(rate * mass, rel=1e-12), config
        rows.append((mass, cost))
    assert rows == sorted(rows) and rows[0][1] < rows[1][1] < rows[2][1]
    budget = v2.read("budgets.launchBudget")
    # 105,770 USD: 15.11 kg at the rate (the supervisor's mass of 15.107 kg, restated at 7,000
    # USD/kg from 90,643 USD at 6,000: WP30 OD4 (a))
    assert budget == pytest.approx(rate * 15.11, abs=1.0)
    verdict = v2.model.verify_requirement(
        f"{P}::LaunchBudgetRequirement", subject=f"{P}::cubesatBaseline"
    )
    assert verdict.holds and verdict.status == "holds"


def test_the_four_thresholds_are_the_supervisors_values(v2):
    """The four thresholds are the supervisor's choice from the loop's ladder (WP23-decisions.md,
    "The four thresholds", and "Keep 0.0085 deg"), literal values in ``budgets`` read through the
    toolkit: 0.008495 degree, 0.05922 N.m.s, 2.6 W and the launch budget (90,643 USD at 6,000
    USD/kg, restated at WP30 as 105,770 USD at 7,000 USD/kg, OD4 (a)). The baseline configuration
    meets three of them and fails the pointing-error requirement (0.0155 against 0.0085 degree),
    which the model states with a negated ``satisfy``."""
    want = {
        "pointingErrorLimit": (0.008495, "SI::degree"),
        "controlEffortLimit": (0.05922, "SI::N*SI::m*SI::s"),
        "peakSlewPowerLimit": (2.6, "SI::W"),
        "launchBudget": (105770.0, None),
    }
    for limit, (value, unit) in want.items():
        assert v2.read(f"budgets.{limit}", unit) == pytest.approx(value, rel=1e-12), limit
    assert "margin" not in re.sub(
        r"/\*.*?\*/|//[^\n]*",
        "",
        v2.text[v2.text.index("part def Budgets") : v2.text.index("part budgets")],
        flags=re.S,
    )
    base = f"{P}::cubesatBaseline"
    for requirement in (
        "ControlEffortRequirement",
        "PeakSlewPowerRequirement",
        "LaunchBudgetRequirement",
    ):
        v = v2.model.verify_requirement(f"{P}::{requirement}", subject=base)
        assert v.holds and v.engine == "run", requirement
    v = v2.model.verify_requirement(f"{P}::PointingErrorRequirement", subject=base)
    assert v.status == "violated" and not v.holds
    pointing = v2.value(v2.model.eval(f"{P}::PointingError({base})"), "SI::degree")
    assert pointing == pytest.approx(0.015535, rel=1e-4) and pointing > 0.008495
    assert "not satisfy baselinePointingError by cubesatBaseline;" in v2.text


# ---------------------------------------------------------------------------------------------
# The closed-form slew approximation against the ODE (OD2)
# ---------------------------------------------------------------------------------------------
@pytest.mark.slow
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


# ---------------------------------------------------------------------------------------------
# WP26 R-4: the views a SysML v2 view editor draws, in their own file beside the model
# ---------------------------------------------------------------------------------------------
VIEWS = ADCS_DIR / "model_v2" / "views.sysml"
STAKEHOLDERS = ADCS_DIR / "model_v2" / "stakeholders.sysml"  # WP27: the stakeholder view exposes it
S = "CubesatStakeholders"


def test_views_file_loads_with_the_model_and_every_exposed_name_resolves(v2):
    """WP26 R-4: ``views.sysml`` applied after ``cubesat.sysml`` (and, since WP27, after
    ``stakeholders.sysml``, which its stakeholder view exposes) as one model loads strictly; it
    declares one package of views and nothing else; every name a view exposes is an element of
    the model; and the model's own elements are the same with the views as without them."""
    views = VIEWS.read_text(encoding="utf-8")
    assert re.findall(r"^package\s+(\w+)", views, flags=re.M) == ["CubesatViews"]
    assert P not in re.findall(r"^package\s+(\w+)", views, flags=re.M)
    both = v2.connection.load_from_content(
        TEXT + "\n" + STAKEHOLDERS.read_text(encoding="utf-8") + "\n" + views, strict=True
    )
    assert both.ok
    assert not [d for d in both.diagnostics if d.severity == "error"]
    declared = re.findall(r"^\s*view\s+(\w+)\s*:\s*(\w+)\s*\{", views, flags=re.M)
    assert {n for n, _ in declared} == {
        "assembly", "alternatives", "configurations", "metrics", "requirements", "metricCarriers",
        "stakeholders",
    }  # fmt: skip
    assert {k for _, k in declared} <= {"GeneralView", "InterconnectionView"}
    for name, _ in declared:
        assert both.find(f"CubesatViews::{name}") is not None, name
    # each exposed name without its ``::*`` (members of) suffix: the model's package or an element
    exposed = re.findall(r"^\s*expose\s+([\w:]+?)(?:::\*)?;", views, flags=re.M)
    assert exposed and all(e == P or e.startswith((f"{P}::", f"{S}::")) for e in exposed)
    for e in sorted(set(exposed)):
        assert both.find(e) is not None, e

    def names(model):
        return {
            q.properties["name"]
            for kind in ("PartDefinition", "PartUsage", "RequirementDefinition",
                         "RequirementUsage", "CalculationDefinition")
            for q in model.query(
                scope=[P], where={"property": "@type", "operator": "=", "value": kind}
            )
        }  # fmt: skip

    assert names(both) == names(v2.model)


# ---------------------------------------------------------------------------------------------
# WP27 R-1, R-2, R-7: who cares (stakeholders.sysml), the trace, the roll-ups read by no output
# ---------------------------------------------------------------------------------------------
REQUIREMENT_DEFS = {
    "SettledRequirement", "MomentumRequirement", "PowerRequirement",
    "DepthOfDischargeRequirement", "PointingErrorRequirement", "ControlEffortRequirement",
    "PeakSlewPowerRequirement", "BatteryPeakPowerRequirement", "LaunchBudgetRequirement",
    "PowerMarginRequirement", "EnergyBalanceRequirement",
    "UnitCostRequirement", "FleetCostRequirement",
}  # fmt: skip
STAKEHOLDER_PARTS = {"sponsor": "Sponsor", "operator": "Operator"}


@pytest.fixture(scope="module")
def who_cares(v2):
    """``cubesat.sysml`` with ``stakeholders.sysml`` and ``views.sysml``, loaded strictly."""
    text = (
        TEXT
        + "\n"
        + STAKEHOLDERS.read_text(encoding="utf-8")
        + "\n"
        + VIEWS.read_text(encoding="utf-8")
    )
    return v2.connection.load_from_content(text, strict=True)


def _concerns(model) -> dict[str, list[tuple[str, str]]]:
    """Each concern usage with its requirement usages: (name, the requirement def typing it)."""
    out = {}
    for q in model.query(
        scope=[S], where={"property": "@type", "operator": "=", "value": "ConcernUsage"}
    ):
        reqs = []
        for ch in model.find(q.id).children():
            if ch.kind == "requirementUsage":
                (typing,) = [s for s in ch.facts().specializations if s.kind == "typing"]
                reqs.append((ch.name, typing.target_id.split("::")[-1]))
        out[q.id.split("::")[-1]] = reqs
    return out


def test_stakeholders_file_loads_strictly_and_its_names_resolve(who_cares):
    """WP27 R-1: the three files load as one model strictly; the stakeholders, the concerns, the
    verification cases, the roll-ups and the stakeholder view are found; a misspelt name fails."""
    assert who_cares.ok
    for name in ("sponsor", "operator", "lowCost", "longLife", "pointingAndSlewing",
                 "powerAndEnergy", "configurationEvidence", "slewEvidence", "CostToBuild",
                 "EffectiveLife", "EvidenceCase"):  # fmt: skip
        assert who_cares.find(f"{S}::{name}") is not None, name
    assert who_cares.find("CubesatViews::stakeholders") is not None
    broken = STAKEHOLDERS.read_text(encoding="utf-8").replace(
        "verify lowCost.launchBudget;", "verify lowCost.launchBudgt;"
    )
    with pytest.raises(ModelError, match="launchBudgt"):
        cm.get_connection().load_from_content(TEXT + "\n" + broken, strict=True)


def test_the_trace_from_who_cares_to_every_requirement_is_complete(who_cares):
    """WP27 R-2: every concern is held by a stakeholder (bound to the sponsor or the operator) and
    is decomposed into at least one requirement; every one of the model's thirteen requirement defs
    serves at least one concern (so every traded metric's requirement reaches one); and every
    requirement a concern holds is verified by a verification case with evidence pointers."""
    stk = STAKEHOLDERS.read_text(encoding="utf-8")
    concerns = _concerns(who_cares)
    assert set(concerns) == {"lowCost", "longLife", "pointingAndSlewing", "powerAndEnergy"}
    holder = r"concern\s+(\w+)\s*:\s*\w+\s*\{.*?stakeholder\s*:>>\s*s\s*=\s*(\w+);"
    held_by = dict(re.findall(holder, stk, flags=re.S))
    assert set(held_by) == set(concerns)
    assert set(held_by.values()) == set(STAKEHOLDER_PARTS)
    for part, kind in STAKEHOLDER_PARTS.items():
        assert who_cares.find(f"{S}::{part}").facts().type.resolved_id == f"{S}::{kind}"
    assert all(reqs for reqs in concerns.values())
    served = {d for reqs in concerns.values() for _, d in reqs}
    assert served == REQUIREMENT_DEFS == _symbols_in(who_cares, P, "RequirementDefinition")
    verified = set(re.findall(r"^\s*verify\s+(\w+)\.(\w+);", stk, flags=re.M))
    held = {(c, r) for c, reqs in concerns.items() for r, _ in reqs}
    assert verified == held, held ^ verified


def _symbols_in(model, package: str, kind: str) -> set[str]:
    return {
        q.properties["name"]
        for q in model.query(
            scope=[package], where={"property": "@type", "operator": "=", "value": kind}
        )
    }


def test_the_rollups_are_illustrative_and_read_by_no_output(who_cares):
    """WP27 R-7: each roll-up's doc says illustrative and names what it rolls up; no roll-up name
    appears in the oracle, the coverage table, the view generator, the data or the contract; the
    roll-ups evaluate on the named configurations (cost to build rises with the agile corner's
    larger wheels and finer tracker; effective life rises with the battery capacity)."""
    stk = STAKEHOLDERS.read_text(encoding="utf-8")
    for calc, rolls_up in (("CostToBuild", "cost model"), ("EffectiveLife", "depth of discharge")):
        body = stk[stk.index(f"calc def {calc}") :]
        doc = " ".join(body[body.index("doc /*") : body.index("*/")].split())
        assert doc.startswith("doc /* Illustrative roll-up"), calc
        assert rolls_up in doc, calc
    names = ("CostToBuild", "EffectiveLife", "UnitCosts", "BatteryLife", "unitCosts", "batteryLife")
    root = ADCS_DIR.parents[1]
    readers = [
        *ADCS_DIR.glob("*.py"), *(ADCS_DIR / "experiments").glob("*.py"),
        ADCS_DIR / "model_v2" / "coverage.py",
        root / "docs" / "superpowers" / "notes" / "spike-sysml-diagrams" / "project.py",
        root / "work-packages" / "interface-contract.toml",
        *(p for p in (ADCS_DIR / "data").rglob("*") if p.suffix in {".csv", ".json"}),
    ]  # fmt: skip
    for path in readers:
        text = path.read_text(errors="ignore", encoding="utf-8")
        assert not [n for n in names if re.search(rf"\b{n}\b", text)], path
    cost = {
        c: who_cares.eval(f"{S}::CostToBuild({P}::{c})")[0]
        for c in ("cubesatCompact", "cubesatBaseline", "cubesatAgile")
    }
    assert cost["cubesatCompact"] < cost["cubesatBaseline"] < cost["cubesatAgile"]
    slew = f"{P}::SlewLossEnergy({P}::baselineMeasurement.torqueSquaredIntegral)"
    life = {
        c: who_cares.eval(f"{S}::EffectiveLife({P}::{c}, {slew})")[0]
        for c in ("cubesatCompact", "cubesatBaseline", "cubesatAgile")
    }
    assert life["cubesatCompact"] < life["cubesatBaseline"] < life["cubesatAgile"]


CONTRAST_NEGATED = {  # WP27-decisions.md (16:20): the contrasts' verdicts, as the engine finds them
    "not satisfy lowCost::launchBudget by cubesatAgile",
    "not satisfy lowCost::unitCost by cubesatAgile",
    "not satisfy lowCost::unitCost by cubesatCompact",
    "not satisfy pointingAndSlewing::controlEffort by cubesatAgile",
    "not satisfy powerAndEnergy::peakSlewPower by cubesatAgile",
    "not satisfy pointingAndSlewing::pointingError by cubesatCompact",
}


def test_the_baselines_verdict_on_each_concern_is_checked_by_the_engine(who_cares):
    """WP27 D-4 (the sponsor saw no verdict in the stakeholder layer): each concern's requirement
    carries the baseline configuration's verdict as a ``satisfy`` or ``not satisfy`` statement in
    ``stakeholders.sysml``; the toolkit's engine checks every statement of the three files (thirteen
    of the model, fourteen per named configuration of the concerns) and all hold, the baseline's
    pointing-error ones negated; stating the baseline's pointing-error verdict as satisfied is
    false (negative control)."""
    verdicts = who_cares.verify_satisfaction()
    assert len(verdicts) == 13 + 3 * 14
    assert all(v.holds and v.status == "holds" and v.engine == "run" for v in verdicts)
    negated = {v.element for v in verdicts if v.element.startswith("not satisfy")}
    assert (
        negated
        == {
            "not satisfy baselinePointingError by cubesatBaseline",
            "not satisfy pointingAndSlewing::pointingError by cubesatBaseline",
            "not satisfy baselineUnitCost by cubesatBaseline",
            "not satisfy lowCost::unitCost by cubesatBaseline",
        }
        | CONTRAST_NEGATED
    )
    flipped = STAKEHOLDERS.read_text(encoding="utf-8").replace(
        "not satisfy pointingAndSlewing.pointingError by cubesatBaseline",
        "satisfy pointingAndSlewing.pointingError by cubesatBaseline",
    )
    wrong = cm.get_connection().load_from_content(TEXT + "\n" + flipped, strict=True)
    bad = [v for v in wrong.verify_satisfaction() if not v.holds]
    assert [v.element for v in bad] == [
        "satisfy pointingAndSlewing::pointingError by cubesatBaseline"
    ]


CONTRASTS = {  # the model's two contrasts, as the oracle configures them (section 7 of the model)
    "agile": {"panel_span_m": 0.8, "battery_wh": 140.0, "wheel_class": "large",
              "st_grade": "fine", "Kp": 1.5, "Kd": 1.2},
    "compact": {"panel_span_m": 0.35, "battery_wh": 40.0, "wheel_class": "small",
                "st_grade": "coarse", "Kp": 0.25, "Kd": 0.4},
}  # fmt: skip


@pytest.mark.parametrize("name", sorted(CONTRASTS))
def test_the_contrasts_measurements_are_recorded_measurements(who_cares, frozen, name):
    """The measurement each contrast's verdicts bind (``agileMeasurement``,
    ``compactMeasurement`` in ``stakeholders.sysml``) is its slew integrated as the baseline's was
    recorded (600 s horizon, 0.5 s step), within the reproducibility tolerance the baseline's
    own test states (rtol 1e-3, times within 0.5 s)."""
    cfg = frozen.configure([{"design_id": 0, **CONTRASTS[name]}])[0]
    got = _measure_slew(frozen, cfg, t_end=600.0, max_step=0.5)
    assert got["censored"] is False

    def read(k, unit=None):
        value = who_cares.eval(f"{S}::{name}Measurement.{k}")
        return float(value.in_unit(who_cares.eval(f"1.0 [{unit}]").unit) if unit else value)

    rtol = 1e-3
    momentum = "SI::N*SI::m*SI::s"
    assert read("settlingTime", "SI::s") == pytest.approx(got["settling_time"], rel=rtol, abs=0.5)
    assert read("peakTorque", "SI::N*SI::m") == pytest.approx(got["peak_torque"], rel=rtol)
    assert read("peakMomentum", momentum) == pytest.approx(got["peak_momentum"], rel=rtol)
    assert read("controlEffort", momentum) == pytest.approx(got["control_effort"], rel=rtol)
    assert read("torqueSquaredIntegral") == pytest.approx(got["torque_squared_integral"], rel=rtol)


def test_the_contrasts_verdicts_rest_on_their_own_measurements(who_cares):
    """WP27-decisions.md (16:20): the agile and compact configurations' verdicts on each concern's
    requirement, engine-checked. A requirement that reads a measured quantity defaults to the
    baseline's measurement, so each such statement binds its ``in`` parameter to the contrast's
    recorded measurement; the engine evaluates the binding, not the default: the agile control
    effort verdict, negated with the agile measurement, holds as ``satisfy`` once the binding is
    the baseline's (the slew the default would have read), and stating a negated verdict as
    satisfied is false (negative controls)."""
    verdicts = who_cares.verify_satisfaction()
    contrasts = [
        v for v in verdicts if v.element.endswith(("by cubesatAgile", "by cubesatCompact"))
    ]
    assert len(contrasts) == 2 * 14
    assert all(v.holds for v in contrasts)
    assert {v.element for v in contrasts if v.element.startswith("not ")} == CONTRAST_NEGATED
    stk = STAKEHOLDERS.read_text(encoding="utf-8")
    negated = "not satisfy pointingAndSlewing.controlEffort by cubesatAgile {"
    assert stk.count(negated) == 1
    flipped = stk.replace(negated, negated[len("not ") :])
    wrong = cm.get_connection().load_from_content(TEXT + "\n" + flipped, strict=True)
    assert [v.element for v in wrong.verify_satisfaction() if not v.holds] == [
        "satisfy pointingAndSlewing::controlEffort by cubesatAgile"
    ]
    rebound = flipped.replace(
        "in controlEffort = agileMeasurement.controlEffort;",
        "in controlEffort = baselineMeasurement.controlEffort;",
    )
    assert rebound != flipped
    other = cm.get_connection().load_from_content(TEXT + "\n" + rebound, strict=True)
    assert all(v.holds for v in other.verify_satisfaction())
