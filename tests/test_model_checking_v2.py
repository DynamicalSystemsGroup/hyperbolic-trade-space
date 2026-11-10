# ruff: noqa: E501
"""Model checking of the v2 cubesat model (WP15 part 15.2).

Four layers, each with a negative control:

* requirements, ``satisfy`` and ``verification def`` in the model (R-4);
* the four feasibility flags produced by verifying the model's requirements, not by an inequality in
  Python (R-3, ``experiments/feasibility.py``);
* claims over every in-range configuration, decided by the ``solve`` engine (z3) with the evidence
  strength recorded (R-5), and the solver's exclusion of infeasible regions and model variants
  before any simulation (``experiments/exclusion.py``); the Python flags on simulated samples are
  observations that agree with the solver's classification;
* the analysis and the sweep (R-7), the static checks of the pinned toolkit (R-6, D-8) and the
  probe record (R-8).

Fixtures FAIL by name, never skip: when the opensysml client cannot start, when ``z3`` is not on
``PATH`` (``uv sync`` installs ``z3-solver`` from the ``case`` group), and when the pinned toolkit
is not provisioned (the message carries the exact provisioning command).
"""

from __future__ import annotations

import ast
import hashlib
import io
import json
import math
import os
import re
import shutil
import tarfile

import cubesat_model as cm
import pytest
from experiments import exclusion as ex
from experiments import feasibility as fz
from experiments import probes, toolkit
from experiments.exclusion import (
    battery_region,
    classify_region,
    classify_regions,
    power_region,
    wheel_region,
)
from opensysml.values import Quantity
from test_system_model_v2 import ATTRIBUTES, MODEL, TEXT, V2, P, _measure_slew, _rel

ADCS_DIR = MODEL.parents[1]
FAST = {"t_end": 600.0, "max_step": 1.0}
PROBE_RECORD = ADCS_DIR / "experiments" / "probes" / "probe-record.md"

# The four claims the model states (section 5) with the answer recorded for each: engine ``solve``,
# question ``holds``, status and evidence strength. A claim an engine does not reach is recorded in
# UNREACHED with the reason, and is asserted undecided.
CLAIMS = {
    "MassAccountingIdentity": ("holds", "proved"),
    "GeneratedPowerMonotoneInSpan": ("holds", "proved"),
    "PowerRequirementHoldsInRange": ("holds", "proved"),
    "SmallBatteryViolatesDepthOfDischarge": ("holds", "proved"),
}
# A false variant of each claim (text edit) and the answer the solver must give: ``violated``.
CLAIM_CONTROLS = {
    "MassAccountingIdentity": (
        "== c.panelPlus.mass + c.panelMinus.mass + c.antenna.mass",
        "== c.panelPlus.mass + c.antenna.mass",
    ),
    "GeneratedPowerMonotoneInSpan": ("<= 81.627336 [W/m] * s2)", "> 81.627336 [W/m] * s2)"),
    "PowerRequirementHoldsInRange": ("- t > 0.0 [W])", "- t > 20.0 [W])"),
    "SmallBatteryViolatesDepthOfDischarge": ("cap <= 26.5 [W*h]", "cap <= 28.0 [W*h]"),
}
UNREACHED = {
    "MassPositiveByCalc": "invocation not translatable for solving: a claim that invokes a calc "
    "def is outside the solver's subset (undecided on every engine)",
}
FLAGS = tuple(fz.FLAG_REQUIREMENTS)


def with_members(text: str, members: str) -> str:
    """The model text with ``members`` appended to its package."""
    body = text.rstrip()
    assert body.endswith("}")
    return body[:-1] + "\n" + members + "\n}\n"


# ---------------------------------------------------------------------------------------------
# fixtures (named failures, never skips)
# ---------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def v2():
    """The model (the one adopted at WP23's data gate)."""
    try:
        return V2(TEXT)
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


@pytest.fixture(scope="module")
def solver():
    if not ex.solver_available():
        pytest.fail(
            "the solve engine needs z3 or cvc5 on PATH and none was found: `uv sync` installs "
            "z3-solver from the `case` group; run through `uv run` (or `uv run --with z3-solver`)",
            pytrace=False,
        )


@pytest.fixture(scope="module")
def frozen():
    try:
        return cm.load_model()
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


@pytest.fixture(scope="module")
def toolkit_bin():
    try:
        return toolkit.locate()
    except FileNotFoundError as exc:
        pytest.fail(str(exc), pytrace=False)


@pytest.fixture(scope="module")
def pool(v2, frozen):
    """300 designs from the aggressive box (seed 11), configured in the model, with controls.

    Controls (design ids from 10000): a panel far below the range (``power_ok`` must fail) and a
    battery at the bottom of the range with the coarse tracker.
    """
    agg = cm.load_model(gain_box="aggressive")
    designs = [dict(r) for _, r in agg.sample_designs(300, seed=11).iterrows()]
    base = dict(designs[0])
    controls = [
        {**base, "design_id": 10000, "panel_span_m": 0.1, "wheel_class": "medium"},
        {**base, "design_id": 10001, "battery_wh": 20.0, "st_grade": "medium"},
    ]
    loaded, symbols = v2.configure(designs + controls)
    return {
        "designs": designs,
        "symbols": dict(zip((int(d["design_id"]) for d in designs), symbols, strict=False)),
        "controls": {"tiny_panel": symbols[-2], "tiny_battery": symbols[-1]},
        "model": loaded,
        "frozen": frozen,
        "checker": fz.FeasibilityChecker(loaded, P),
        "v2": v2,
    }


@pytest.fixture(scope="module")
def measured(pool):
    """Slew measurements (coarse step) for the designs a test asks for, cached by design id."""
    cache: dict[int, dict] = {}

    def get(design_ids):
        need = [i for i in design_ids if i not in cache]
        if need:
            by_id = {int(d["design_id"]): d for d in pool["designs"]}
            for i, cfg in zip(
                need, pool["frozen"].configure([by_id[i] for i in need]), strict=True
            ):
                cache[i] = _measure_slew(pool["frozen"], cfg, **FAST)
        return [cache[i] for i in design_ids]

    return get


def _subset(pool, predicate, n):
    out = [d for d in pool["designs"] if predicate(d)]
    assert len(out) >= n, f"only {len(out)} sampled designs satisfy the predicate"
    return out[:n]


# ---------------------------------------------------------------------------------------------
# R-4: requirements, satisfy, verification defs
# ---------------------------------------------------------------------------------------------
# The requirements over the traded metrics' own quantities (none a flag). WP22 (WP22d) added one
# per newly covered metric; WP23 D-1 folded the slew-time and slew-band requirements into
# SettledRequirement and gave the four metrics that had none one each (pointing error, control
# effort, peak slew power, the total mass through the launch cost), each satisfied by the baseline
# and verified in the case that can decide it (before or after the slew is measured). Round 2 (the
# coupling check, WP23-review.md) added BatteryPeakPowerRequirement, the pack's rating against the
# eclipse peak load, verified in the slew case: the pin is the model adopted at the data gate. The
# close-out (WP23-closeout-scope-of-work.md, D-11) removed EclipseReserveRequirement (the
# depth-of-discharge requirement restated) and states that the baseline configuration fails the
# pointing-error requirement at the supervisor's 0.0085 degree (a negated ``satisfy``).
METRIC_REQUIREMENTS = {
    "PowerMarginRequirement",
    "EnergyBalanceRequirement",
    "PointingErrorRequirement",
    "ControlEffortRequirement",
    "PeakSlewPowerRequirement",
    "LaunchBudgetRequirement",
    "BatteryPeakPowerRequirement",
}
_FLAG_DEFS = set(fz.FLAG_REQUIREMENTS.values())
# The WP22 version's requirement on the band being entered (the slew time's censoring): gone with
# the slew time (WP23 D-1 folded it into SettledRequirement), and the checker neither names nor
# reads it (WP23 D-3: the slew time left the measurement).
SLEW_BAND = "SlewBandRequirement"
REQUIREMENTS = {
    "defs": _FLAG_DEFS | METRIC_REQUIREMENTS,
    "satisfy": 11,
    "not satisfied by the baseline": {"PointingErrorRequirement"},
    "verified": {
        "ConfigurationVerification": {
            "PowerRequirement",
            "PointingErrorRequirement",
            "LaunchBudgetRequirement",
        },
        "SlewVerification": {
            "SettledRequirement",
            "MomentumRequirement",
            "DepthOfDischargeRequirement",
            "PowerMarginRequirement",
            "EnergyBalanceRequirement",
            "ControlEffortRequirement",
            "PeakSlewPowerRequirement",
            "BatteryPeakPowerRequirement",
        },
    },
}


def _kinds(model, kind):
    return {
        q.properties["name"]: q
        for q in model.query(scope=[P], where={"property": "@type", "operator": "=", "value": kind})
    }


def test_requirements_are_declared_one_per_flag(v2):
    """R-3/R-4: the four flags are named requirement definitions; the others bound the traded
    metrics (none of them is a flag): the eight of ``METRIC_REQUIREMENTS``."""
    defs = set(_kinds(v2.model, "RequirementDefinition"))
    assert set(fz.FLAG_REQUIREMENTS.values()) <= defs
    assert defs == REQUIREMENTS["defs"]


def test_verification_defs_name_the_requirements_they_verify(v2):
    """R-4: each verification def names its requirements (read from the model by query)."""
    verified: dict[str, set[str]] = {}
    for name in _kinds(v2.model, "VerificationCaseDefinition"):
        found = set()
        for q in v2.model.query(scope=[f"{P}::{name}"]):
            if q.properties.get("@type") == "SatisfyRequirementUsage":
                found.add(q.properties["type"].split("::")[-1])
        verified[name] = found
    assert verified == REQUIREMENTS["verified"]
    assert set(fz.FLAG_REQUIREMENTS.values()) <= set().union(*verified.values())
    assert set().union(*verified.values()) == REQUIREMENTS["defs"]


def test_satisfy_statements_hold_on_the_baseline(v2):
    """R-4: one `satisfy` statement per requirement ties it to the baseline (eleven since the WP23
    close-out); all hold (engine run). The pointing-error one is negated, ``not satisfy``: the
    model states that the baseline configuration fails that requirement (0.0155 against 0.0085
    degree), and the engine finds the statement true."""
    verdicts = v2.model.verify_satisfaction()
    assert len(verdicts) == REQUIREMENTS["satisfy"] == len(REQUIREMENTS["defs"])
    assert all(v.holds and v.status == "holds" for v in verdicts)
    negated = {v.element for v in verdicts if v.element.startswith("not satisfy")}
    assert negated == {"not satisfy baselinePointingError by cubesatBaseline"}
    for req in REQUIREMENTS["not satisfied by the baseline"]:
        v = v2.model.verify_requirement(f"{P}::{req}", subject=f"{P}::cubesatBaseline")
        assert v.status == "violated" and not v.holds, req
    assert {v.engine for v in verdicts} == {"run"}
    assert {v.strength for v in verdicts} == {"observed"}
    assert v2.model.satisfied()
    satisfy = v2.model.query(
        scope=[P], where={"property": "@type", "operator": "=", "value": "SatisfyRequirementUsage"}
    )
    assert len(satisfy) >= REQUIREMENTS["satisfy"]


def test_baseline_measurement_is_a_recorded_measurement(v2, frozen):
    """The defaults the satisfy statements use are the baseline's measured slew (0.5 s step)."""
    cfg = frozen.configure(
        [
            {
                "design_id": 0,
                "panel_span_m": 0.6,
                "battery_wh": 80.0,
                "wheel_class": "medium",
                "st_grade": "medium",
                "Kp": 0.03,
                "Kd": 0.3,
            }
        ]
    )[0]
    got = _measure_slew(frozen, cfg, t_end=600.0, max_step=0.5)
    read = lambda k, u=None: v2.read(f"baselineMeasurement.{k}", u)  # noqa: E731
    # The recorded values come from an adaptive ODE integration; two platforms agree to about 1e-8
    # (observed 1.8e-9 between macOS and Linux). The requirement is agreement within the
    # reproducibility tolerance the frozen data's own tests state (rtol 1e-3, times within 0.5 s).
    rtol = 1e-3
    assert read("settlingTime", "SI::s") == pytest.approx(got["settling_time"], rel=rtol, abs=0.5)
    assert read("peakMomentum", "SI::N*SI::m*SI::s") == pytest.approx(
        got["peak_momentum"], rel=rtol
    )
    assert read("torqueSquaredIntegral") == pytest.approx(got["torque_squared_integral"], rel=rtol)
    assert got["censored"] is False


def test_negative_control_satisfy_fails_on_an_out_of_range_part(v2):
    """R-4: a `satisfy` of the power requirement by a panel far below the range is not satisfied."""
    members = """
    part tinySat : Cubesat {
        :>> panelSpan default = 0.1 [m];
        part :>> wheel : MediumWheel;
        part :>> tracker : MediumTracker;
    }
    requirement tinyPower : PowerRequirement;
    satisfy tinyPower by tinySat;
    """
    m = v2.connection.load_from_content(with_members(v2.text, members), strict=True)  # loads clean
    verdicts = m.verify_satisfaction()
    assert [v.holds for v in verdicts].count(False) == 1
    bad = next(v for v in verdicts if not v.holds)
    assert bad.status == "violated" and bad.strength == "witnessed"
    assert not m.satisfied()


# ---------------------------------------------------------------------------------------------
# R-3: the flags are verdicts of the model's requirements
# ---------------------------------------------------------------------------------------------
def test_feasibility_module_has_no_inequality_on_quantities():
    """R-3: no ordering comparison appears in experiments/feasibility.py."""
    tree = ast.parse((ADCS_DIR / "experiments" / "feasibility.py").read_text())
    ordering = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)
    bad = [
        n.lineno
        for n in ast.walk(tree)
        if isinstance(n, ast.Compare) and any(isinstance(op, ordering) for op in n.ops)
    ]
    assert bad == [], f"ordering comparison at lines {bad}"


def test_requirement_names_in_the_checker_exist_in_the_model(v2):
    """The checker's flag requirements exist in the model and are the only requirements it
    names; the WP22 version's slew-band requirement is gone (the slew time left the measurement,
    WP23 D-3; the model folded it into SettledRequirement)."""
    defs = set(_kinds(v2.model, "RequirementDefinition"))
    assert set(fz.FLAG_REQUIREMENTS.values()) <= defs
    assert set(fz._ARGUMENTS) <= set(fz.FLAG_REQUIREMENTS.values())
    assert SLEW_BAND not in defs
    assert set(fz.FLAG_REQUIREMENTS.values()) == defs - METRIC_REQUIREMENTS


@pytest.fixture(scope="module")
def sample20(pool, measured):
    """20 sampled designs: the measurement, the checker's flags and the frozen oracle's output."""
    ids = [int(d["design_id"]) for d in pool["designs"][:20]]
    meas = measured(ids)
    cfgs = pool["frozen"].configure(pool["designs"][:20])
    rows = []
    for i, m, cfg in zip(ids, meas, cfgs, strict=True):
        sym = pool["symbols"][i]
        rows.append(
            {
                "id": i,
                "symbol": sym,
                "measured": m,
                "flags": pool["checker"].flags(sym, m),
                "frozen": pool["frozen"].measure(cfg, **FAST),
            }
        )
    return rows


@pytest.mark.slow
def test_flags_equal_an_independent_python_evaluation_on_20_designs(sample20, v2, pool, capsys):
    """R-3: the verified flags equal the same inequalities evaluated in Python (and the frozen oracle)."""
    max_dod = v2.read("environment.maxDepthOfDischarge")
    horizon = v2.read("nominalSlew.horizon", "SI::s")
    caps = pool["frozen"].wheel_capacities()
    by_id = {int(d["design_id"]): d for d in pool["designs"]}
    for row in sample20:
        f, out = row["flags"], row["frozen"]
        independent = {
            "settled": row["measured"]["settling_time"] < horizon,
            "momentum_ok": row["measured"]["peak_momentum"]
            <= caps[by_id[row["id"]]["wheel_class"]],
            "power_ok": out["available_power_w"] > 0.0,
            "dod_ok": out["dod_eclipse"] <= max_dod,
        }
        assert f == independent, f"design {row['id']}"
        assert f == {k: out[k] for k in FLAGS}, f"design {row['id']} vs the frozen oracle"
    seen = {k: {r["flags"][k] for r in sample20} for k in FLAGS}
    with capsys.disabled():
        print(f"\n[flags] values seen over 20 designs: { {k: sorted(v) for k, v in seen.items()} }")
    assert seen["settled"] == {True, False} or seen["momentum_ok"] == {True, False}


@pytest.mark.parametrize("flag", FLAGS)
def test_flag_has_a_negative_control(flag, pool):
    """R-3: for each flag a deliberately infeasible input gives False (witnessed), a feasible True."""
    chk, base = pool["checker"], f"{P}::cubesatBaseline"
    if flag == "settled":
        good, bad = (
            chk.verify(flag, base, {"settling_time": 100.0}),
            chk.verify(flag, base, {"settling_time": 600.0}),
        )
    elif flag == "momentum_ok":
        good, bad = (
            chk.verify(flag, base, {"peak_momentum": 0.001}),
            chk.verify(flag, base, {"peak_momentum": 0.05}),
        )
    elif flag == "power_ok":
        good, bad = chk.verify(flag, base), chk.verify(flag, pool["controls"]["tiny_panel"])
    else:
        good = chk.verify(flag, base, {"torque_squared_integral": 1e-6})
        bad = chk.verify(flag, base, {"torque_squared_integral": 1e5})
        small = chk.verify(flag, pool["controls"]["tiny_battery"], {"torque_squared_integral": 0.0})
        assert (
            not small.holds and small.status == "violated"
        )  # a 20 Wh battery cannot carry the eclipse
    assert good.holds and good.engine == "run" and good.strength == "observed", flag
    assert not bad.holds and bad.status == "violated" and bad.strength == "witnessed", flag


def test_the_checker_reads_no_slew_band_requirement(pool):
    """The slew time's censoring left the measurement with the slew time (WP23 D-3), so the checker
    names no slew-band requirement and translates no `censored` key, and the model declares none
    (folded into SettledRequirement)."""
    chk, defs = pool["checker"], _kinds(pool["v2"].model, "RequirementDefinition")
    assert not hasattr(fz, "SLEW_BAND_REQUIREMENT") and not hasattr(chk, "slew_band_entered")
    assert "censored" not in {key for _, key, _ in fz._ARGUMENTS.values()}
    assert SLEW_BAND not in defs


# ---------------------------------------------------------------------------------------------
# R-5: claims over every in-range configuration
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("claim", sorted(CLAIMS))
def test_claim_holds_with_recorded_evidence(claim, v2, solver, capsys):
    """R-5: the solve engine answers `holds` for each claim, with the strength recorded."""
    v = v2.model.verify_constraint(f"{P}::{claim}", engine="solve", question="holds")
    with capsys.disabled():
        print(f"\n[claim] {claim}: engine {v.engine} {v.status} ({v.strength})")
    assert (v.status, v.strength) == CLAIMS[claim], (
        f"claim {claim}: {v.status} {v.strength} {v.error}"
    )
    assert v.engine == "solve"


@pytest.mark.parametrize("claim", sorted(CLAIM_CONTROLS))
def test_claim_negative_control_is_violated_with_a_witness(claim, v2, solver):
    """R-5: a false variant of each claim is `violated`, witnessed, with a counterexample."""
    old, new = CLAIM_CONTROLS[claim]
    assert v2.text.count(old) == 1, claim
    m = cm.get_connection().load_from_content(v2.text.replace(old, new), strict=True)
    v = m.verify_constraint(f"{P}::{claim}", engine="solve", question="holds")
    assert (v.status, v.strength) == ("violated", "witnessed"), f"claim {claim}: {v.status}"
    assert v.witness, claim


def test_claim_literals_are_the_models_own_numbers(v2):
    """The claims restate the accounting with literals; each literal is tied to its source here."""
    k = ex._Constants(v2.model, P)
    start = v2.text.index("constraint def MassAccountingIdentity")
    claims = v2.text[start : v2.text.index("// END 15.2")]
    num = lambda pattern: float(re.search(pattern, claims).group(1))  # noqa: E731
    assert num(r"([\d.]+) \[W/m\] \* s1") == pytest.approx(k.generation_per_span(), rel=1e-9)
    assert num(r"- ([\d.]+) \[W\] - t > ") == pytest.approx(k.env("housekeepingLoad", "SI::W"))
    assert num(r"t \+ ([\d.]+) \[W\]\) \*") == pytest.approx(
        k.baseline("wheelCount") * k.env("wheelIdlePower", "SI::W")
    )
    assert num(r"\* ([\d.]+) \[h\] \+ e") == pytest.approx(k.env("eclipseDuration", "SI::h"))
    assert num(r"e > ([\d.]+) \* cap") == pytest.approx(k.env("maxDepthOfDischarge"))
    assert num(r"s >= ([\d.]+) \[m\]") == pytest.approx(
        k.num(f"{P}::designRanges.panelSpanMin", "SI::m")
    )
    assert num(r"s <= ([\d.]+) \[m\]") == pytest.approx(
        k.num(f"{P}::designRanges.panelSpanMax", "SI::m")
    )
    lo, hi = k.tracker_power_range()
    assert num(r"t >= ([\d.]+) \[W\]") == pytest.approx(lo)
    assert num(r"t <= ([\d.]+) \[W\]\)") == pytest.approx(hi)
    assert num(r"cap >= ([\d.]+) \[W\*h\]") == pytest.approx(
        k.num(f"{P}::designRanges.batteryCapacityMin", "SI::W*SI::h")
    )


def test_mass_claim_restates_the_calc_bodies():
    """The mass identity is stated over the bodies of MassAccounting and StructureMass (drift guard)."""
    text = TEXT

    def body(calc):
        m = re.search(rf"calc def {calc} \{{.*?return : \w+ =(.*?);\s*\}}", text, re.S)
        return " ".join(m.group(1).split()).replace("c.wheelCount", "3.0")

    claim = text[text.index("constraint def MassAccountingIdentity") :]
    claim = " ".join(claim[: claim.index("}")].split())
    assert body("MassAccounting") in claim
    assert body("StructureMass") in claim


def test_a_claim_no_engine_reaches_is_recorded_with_its_reason(v2, solver):
    """R-5: a claim that invokes a calc def is undecided on every engine; the reason is recorded."""
    members = "constraint def MassPositiveByCalc { in c : Cubesat; MassAccounting(c) > 0.0 [kg] }"
    m = v2.connection.load_from_content(with_members(v2.text, members), strict=True)
    for engine in ("smt", "solve", "check", "auto"):
        v = m.verify_constraint(f"{P}::MassPositiveByCalc", engine=engine, question="holds")
        assert v.status == "undecided", f"{engine}: {v.status}"
    v = m.verify_constraint(f"{P}::MassPositiveByCalc", engine="solve", question="holds")
    assert (
        "not translatable" in str(v.error) and "not translatable" in UNREACHED["MassPositiveByCalc"]
    )
    # the smt engine answers no constraint claim at all: it answers over schedules
    s = m.verify_constraint(f"{P}::MassAccountingIdentity", engine="smt", question="holds")
    assert s.status == "undecided"


# ---------------------------------------------------------------------------------------------
# The solver's exclusion of regions and model variants before simulation
# ---------------------------------------------------------------------------------------------
# region, verdict, (Sat status/strength), (Holds status/strength); the cases of probe-record.md section 5
EXCLUSION_CASES = [
    (battery_region((20, 26)), "excluded", ("unsatisfiable", "proved"), ("violated", "witnessed")),
    (battery_region((29, 200)), "all-feasible", ("satisfiable", "witnessed"), ("holds", "proved")),
    (battery_region((20, 200)), "mixed", ("satisfiable", "witnessed"), ("violated", "witnessed")),
    (
        wheel_region("small", (0.70, 0.90)),
        "excluded",
        ("unsatisfiable", "proved"),
        ("violated", "witnessed"),
    ),
    (
        wheel_region("small", (0.18, 0.60)),
        "all-feasible",
        ("satisfiable", "witnessed"),
        ("holds", "proved"),
    ),
    (
        wheel_region("small", (0.18, 0.90)),
        "mixed",
        ("satisfiable", "witnessed"),
        ("violated", "witnessed"),
    ),
    (
        wheel_region("large", (0.18, 0.90)),
        "all-feasible",
        ("satisfiable", "witnessed"),
        ("holds", "proved"),
    ),
    (power_region(), "all-feasible", ("satisfiable", "witnessed"), ("holds", "proved")),
    (
        power_region((0.05, 0.15)),
        "excluded",
        ("unsatisfiable", "proved"),
        ("violated", "witnessed"),
    ),
]


@pytest.fixture(scope="module")
def classified(v2, solver):
    regions = [c[0] for c in EXCLUSION_CASES]
    return classify_regions(v2.path, regions, connection=v2.connection)


@pytest.mark.parametrize("i", range(len(EXCLUSION_CASES)))
def test_region_classification_matches_the_probe_record(i, classified):
    """Verified cases of the probe record: excluded / all-feasible / mixed, with the evidence."""
    region, verdict, sat, holds = EXCLUSION_CASES[i]
    c = classified[i]
    label = f"{region.name} {dict(region.box)}"
    assert c.verdict == verdict, label
    assert c.satisfiable == sat and c.holds == holds, label
    assert c.engine == "solve"
    assert c.excluded == (verdict == "excluded")
    if verdict == "excluded":
        assert c.witness_violation and not c.witness_feasible
    if verdict == "mixed":
        assert c.witness_violation and c.witness_feasible


def test_exclusion_thresholds_agree_with_the_arithmetic(v2, solver):
    """The solver's boundaries equal the closed forms: battery floor 26.6 Wh, inertia 0.6366."""
    k = ex._Constants(v2.model, P)
    lo, _ = k.tracker_power_range()
    floor = (k.env("housekeepingLoad", "SI::W") + lo + 0.9) * k.env("eclipseDuration", "SI::h")
    floor /= k.env("maxDepthOfDischarge")
    assert floor == pytest.approx(26.6)
    model = v2.path
    just_below = classify_region(model, battery_region((20, floor - 0.01), tracker_w=(lo, lo)))
    just_above = classify_region(model, battery_region((floor + 0.01, 200), tracker_w=(lo, lo)))
    assert (just_below.verdict, just_above.verdict) == ("excluded", "all-feasible")
    small = k.alternatives("ReactionWheel", "wheelClass")["small"]
    tau = k.alt_value(small, "maxTorque", "SI::N*SI::m")
    h = k.alt_value(small, "maxMomentum", "SI::N*SI::m*SI::s")
    limit = h * h / (tau * math.radians(k.num(f"{P}::nominalSlew.slewAngle", "SI::degree")))
    assert limit == pytest.approx(0.6366, abs=1e-4)
    edge = (limit - 0.001, limit + 0.001)
    assert classify_region(model, wheel_region("small", (0.18, edge[0]))).verdict == "all-feasible"
    assert classify_region(model, wheel_region("small", (edge[1], 0.9))).verdict == "excluded"


def test_slew_energy_bound_moves_the_all_feasible_boundary(v2, solver):
    """A stated slew energy range enters the condition: 29 to 200 Wh is all feasible at zero energy,
    mixed when up to 1 Wh of slew loss is allowed, and 40 to 200 Wh is all feasible at 2 Wh."""
    model = v2.path
    assert classify_region(model, battery_region((29, 200))).verdict == "all-feasible"
    assert (
        classify_region(model, battery_region((29, 200), slew_energy_wh=(0, 1))).verdict == "mixed"
    )
    assert (
        classify_region(model, battery_region((40, 200), slew_energy_wh=(0, 2))).verdict
        == "all-feasible"
    )


def test_negative_controls_of_the_exclusion_helper(v2, solver, monkeypatch):
    """A feasible region is not excluded; malformed input is refused; no solver is a named error."""
    model = v2.path
    assert not classify_region(model, battery_region((100, 200))).excluded
    with pytest.raises(ValueError, match="empty interval"):
        battery_region((26, 20))
    with pytest.raises(ValueError, match="unknown wheel class"):
        classify_region(model, wheel_region("huge", (0.2, 0.3)))
    with pytest.raises(ValueError, match="matches 0 times"):
        ex.model_variant(v2.text, {"no such literal": "x"})
    monkeypatch.setattr(shutil, "which", lambda name: None)
    with pytest.raises(ex.SolverUnavailable, match="z3"):
        classify_region(model, battery_region((20, 26)))


VARIANTS = {
    "housekeeping load 90 W": (
        {
            "attribute housekeepingLoad : PowerValue = 12.0 [W];": "attribute housekeepingLoad : PowerValue = 90.0 [W];"
        },
        True,
    ),
    "depth of discharge 0.03": (
        {
            "attribute maxDepthOfDischarge : Real = 0.3;": "attribute maxDepthOfDischarge : Real = 0.03;"
        },
        True,
    ),
    "depth of discharge 0.6": (
        {
            "attribute maxDepthOfDischarge : Real = 0.3;": "attribute maxDepthOfDischarge : Real = 0.6;"
        },
        False,
    ),
}


@pytest.mark.parametrize("name", sorted(VARIANTS))
def test_model_variants_are_excluded_before_simulation(name, v2, solver):
    """A variant whose design space holds no feasible configuration is excluded; others are kept."""
    edits, expect_excluded = VARIANTS[name]
    got = ex.classify_variant(v2.path, edits, connection=v2.connection)
    assert ex.variant_excluded(got) is expect_excluded, [(c.region.name, c.verdict) for c in got]


def test_the_unedited_model_is_a_kept_variant(v2, solver):
    got = classify_regions(v2.path, ex.design_space_regions(), connection=v2.connection)
    assert [c.verdict for c in got] == ["all-feasible", "mixed"] and not ex.variant_excluded(got)


def test_exclusion_record_is_a_ledger_ready_dict(v2, solver):
    """The record names the region, the claim, the engine, the verdict, the strength and the witness."""
    edits = VARIANTS["depth of discharge 0.03"][0]
    got = ex.classify_variant(v2.path, edits, connection=v2.connection)
    excluded = next(c for c in got if c.excluded)
    rec = ex.exclusion_record(excluded, variant=edits, note="variant")
    assert json.loads(json.dumps(rec)) == rec  # JSON round trip: it can enter a ledger entry
    assert rec["kind"] == "exclusion" and rec["engine"] == "solve" and rec["excluded"] is True
    assert rec["verdict"] == "excluded" and rec["satisfiable"] == ["unsatisfiable", "proved"]
    assert rec["region"]["condition"] == "depth_of_discharge" and rec["region"]["box"]
    assert "implies" in rec["claim"] and rec["witness_violation"] and rec["variant"] == edits
    assert "unsatisfiable" in rec["reason"] and rec["basis"].startswith("exact accounting")
    assert len(rec["model_sha256"]) == 64
    kept = ex.exclusion_record(classify_region(v2.path, battery_region((20, 200))))
    assert kept["excluded"] is False and kept["verdict"] == "mixed"


# -- the Python flags are observations that agree with the solver ------------------------------
def test_dod_flag_agrees_with_the_excluded_battery_region(pool, measured, solver):
    """Every sampled design in a battery region the solver excludes simulates dod_ok False."""
    region = battery_region((20, 26))
    assert classify_region(pool["v2"].path, region, connection=pool["v2"].connection).excluded
    designs = _subset(pool, lambda d: 20 <= d["battery_wh"] <= 26, 4)
    for d, m in zip(designs, measured([int(d["design_id"]) for d in designs]), strict=True):
        flags = pool["checker"].flags(pool["symbols"][int(d["design_id"])], m)
        assert flags["dod_ok"] is False, f"design {d['design_id']} at {d['battery_wh']:.1f} Wh"


def test_dod_flag_agrees_with_the_all_feasible_battery_region(pool, measured, solver):
    """With the slew loss bounded by 2 Wh, every sampled design from 40 Wh up simulates dod_ok True."""
    region = battery_region((40, 200), slew_energy_wh=(0, 2))
    assert (
        classify_region(pool["v2"].path, region, connection=pool["v2"].connection).verdict
        == "all-feasible"
    )
    designs = _subset(pool, lambda d: d["battery_wh"] >= 40, 6)
    for d, m in zip(designs, measured([int(d["design_id"]) for d in designs]), strict=True):
        flags = pool["checker"].flags(pool["symbols"][int(d["design_id"])], m)
        assert flags["dod_ok"] is True, f"design {d['design_id']}"


def test_power_flag_agrees_with_the_solver_on_span_regions(pool, v2, solver):
    """Panels in the excluded span region are power_ok False; panels over the range are True."""
    assert classify_region(v2.path, power_region((0.05, 0.15)), connection=v2.connection).excluded
    spans = [0.05, 0.1, 0.15]
    designs = [
        {**pool["designs"][0], "design_id": 20000 + i, "panel_span_m": s}
        for i, s in enumerate(spans)
    ]
    loaded, symbols = v2.configure(designs)
    chk = fz.FeasibilityChecker(loaded, P)
    assert [chk.flags(s)["power_ok"] for s in symbols] == [False] * 3
    assert (
        classify_region(v2.path, power_region(), connection=v2.connection).verdict == "all-feasible"
    )
    rows = _subset(pool, lambda d: True, 20)
    assert all(
        pool["checker"].flags(pool["symbols"][int(d["design_id"])])["power_ok"] for d in rows
    )


def test_momentum_flag_agrees_with_the_excluded_wheel_region(pool, measured, v2, solver):
    """Small wheel, inertia 0.70 to 0.90 kg m^2 on the 30 degree slew: excluded; each sampled
    design in the region simulates momentum_ok False."""
    assert classify_region(
        v2.path, wheel_region("small", (0.70, 0.90)), connection=v2.connection
    ).excluded
    designs = _in_inertia(pool, "small", 0.70, 0.90, 6)
    for d, m in zip(designs, measured([int(d["design_id"]) for d in designs]), strict=True):
        flags = pool["checker"].flags(pool["symbols"][int(d["design_id"])], m)
        assert flags["momentum_ok"] is False, f"design {d['design_id']}"


def _in_inertia(pool, wheel, lo, hi, n):
    chosen = []
    for d in pool["designs"]:
        if d["wheel_class"] != wheel:
            continue
        sym = pool["symbols"][int(d["design_id"])]
        ix = pool["v2"].value(pool["model"].eval(f"{P}::InertiaX({sym})"), "SI::kg*SI::m**2")
        if lo <= ix <= hi:
            chosen.append(d)
        if len(chosen) == n:
            return chosen
    raise AssertionError(
        f"only {len(chosen)} sampled {wheel}-wheel designs have inertia in [{lo}, {hi}]"
    )


def test_momentum_closed_form_is_optimistic_against_the_ode(pool, measured, v2, solver):
    """Recorded finding: the closed-form bang-bang momentum is a lower estimate of the ODE's.

    For the small wheel with inertia 0.18 to 0.60 kg m^2 the solver says all feasible (closed form);
    the ODE puts the peak momentum above the closed form in the torque-limited cases, and some of
    those sampled designs exceed the wheel's capacity: `all-feasible` of the momentum condition is a
    statement about the approximation (OD2), `excluded` is the confirmed direction.
    """
    region = wheel_region("small", (0.18, 0.60))
    assert classify_region(v2.path, region, connection=v2.connection).verdict == "all-feasible"
    designs = _in_inertia(pool, "small", 0.18, 0.60, 8)
    meas = measured([int(d["design_id"]) for d in designs])
    flags = [
        pool["checker"].flags(pool["symbols"][int(d["design_id"])], m)["momentum_ok"]
        for d, m in zip(designs, meas, strict=True)
    ]
    assert False in flags and True in flags, flags
    k = ex._Constants(v2.model, P)
    small = k.alternatives("ReactionWheel", "wheelClass")["small"]
    tau = k.alt_value(small, "maxTorque", "SI::N*SI::m")
    theta = math.radians(k.num(f"{P}::nominalSlew.slewAngle", "SI::degree"))
    over = 0
    for d, m in zip(designs, meas, strict=True):
        sym = pool["symbols"][int(d["design_id"])]
        ix = v2.value(pool["model"].eval(f"{P}::InertiaX({sym})"), "SI::kg*SI::m**2")
        over += m["peak_momentum"] > math.sqrt(tau * theta * ix)
    assert over >= len(designs) // 2


# ---------------------------------------------------------------------------------------------
# R-7: analysis and sweep
# ---------------------------------------------------------------------------------------------
@pytest.mark.slow
def test_run_analysis_with_the_measured_slew_equals_the_frozen_oracle(sample20, pool):
    """R-7: the eight computed attributes of run_analysis on a configuration plus the Python
    measurement equal the frozen oracle's output (1e-9 relative), and the flags are those the requirements give."""
    worst = 0.0
    for row in sample20:
        got = pool["v2"].experiment(pool["model"], row["symbol"], row["measured"])
        for name, _ in ATTRIBUTES:
            worst = max(worst, _rel(got[name], row["frozen"][name]))
    assert worst < 1e-9


def test_run_sweep_over_the_measured_energy_integral_reproduces_the_accounting(v2):
    """R-7: a grid sweep of SlewExperiment over the integral of |tau|^2 reproduces the Python-side
    energy accounting (eclipse depth of discharge, the last attribute) on every grid row.

    The design variables are features of the subject, which `run_sweep` does not range over; the
    sweepable input is the Real `torqueSquaredIntegral` (probe 6: a range cannot bind a quantity).
    """
    unit = v2.unit
    named = {
        "peakTorque": Quantity(0.002, unit("SI::N*SI::m")),
        "peakMomentum": Quantity(0.004, unit("SI::N*SI::m*SI::s")),
        "controlEffort": Quantity(0.1, unit("SI::N*SI::m*SI::s")),
    }
    if "in censored" in v2.text:  # the adopted model's analysis takes the slew censoring
        named["censored"] = False
    table = v2.model.run_sweep(
        f"{P}::SlewExperiment",
        {"torqueSquaredIntegral": (0.0, 1.0e-3, 2.5e-4)},
        subject=f"{P}::cubesatBaseline",
        named_arguments=named,
    )
    assert len(table.rows) == 5 and not table.failures
    base = f"{P}::cubesatBaseline"
    k = ex._Constants(v2.model, P)
    load = (
        k.env("housekeepingLoad", "SI::W")
        + k.baseline("tracker.power", "SI::W")
        + k.baseline("wheelCount") * k.env("wheelIdlePower", "SI::W")
    )
    cap = k.baseline("battery.capacity", "SI::W*SI::h")
    for row in table.rows:
        tsi = float(row.inputs["torqueSquaredIntegral"])
        energy_wh = k.env("wheelLossCoefficient") * tsi / 3600.0
        want = (load * k.env("eclipseDuration", "SI::h") + energy_wh) / cap
        got = v2.value(row.outputs["attributes"][6])
        assert got == pytest.approx(want, rel=1e-9), (base, tsi)


# ---------------------------------------------------------------------------------------------
# R-6: static checks (self_check, and the pinned toolkit)
# ---------------------------------------------------------------------------------------------
def test_self_check_holds_with_the_region_filled(v2):
    assert v2.model.self_check().status == "holds" and v2.model.ok


def test_toolkit_check_passes_on_v2(toolkit_bin, v2):
    out = toolkit_bin.check(v2.path)
    assert out.returncode == 0, out.stderr[-500:]


def test_toolkit_lint_reports_no_errors_or_warnings_on_v2(toolkit_bin, v2):
    summary = toolkit_bin.lint(v2.path)["summary"]
    assert summary["errors"] == 0 and summary["warnings"] == 0, summary


def test_toolkit_verify_solve_runs_on_v2(toolkit_bin, v2, solver):
    out = toolkit_bin.verify_solve(v2.path)
    assert out.returncode == 0, out.stdout[-500:] + out.stderr[-500:]
    assert "0 violated" in out.stdout


def test_toolkit_verify_solve_negative_control(toolkit_bin, solver, tmp_path):
    """verify --solve flags a jointly unsatisfiable range (exit 1, VIOLATED)."""
    snippet = tmp_path / "tank.sysml"
    snippet.write_text(probes._TOOLKIT_SNIPPET)
    out = toolkit_bin.verify_solve(snippet)
    assert out.returncode == 1 and "VIOLATED" in out.stdout


def test_toolkit_reports_the_pinned_version(toolkit_bin):
    assert toolkit.version(toolkit_bin.binary) == toolkit.load_pin()["toolkit"]["version_output"]


# -- the pin and the provisioning helper (no network) ---------------------------------------------
def test_pin_agrees_with_the_probe_record_assets():
    pin = toolkit.load_pin()
    assert pin["toolkit"]["tag"] == probes.TOOLKIT_VERSION
    record = PROBE_RECORD.read_text()
    for triple, asset in pin["toolkit"]["assets"].items():
        size, digest = probes.RELEASE_ASSETS[asset["name"]]
        assert (asset["size"], asset["sha256"]) == (size, digest), triple
        assert asset["sha256"] in record and len(asset["sha256"]) == 64
    assert re.fullmatch(r"[0-9a-f]{40}", pin["toolkit"]["commit"])
    assert re.fullmatch(r"[0-9a-f]{40}", pin["stdlib"]["commit"])


def test_platform_triples_cover_the_pinned_assets():
    pin = toolkit.load_pin()["toolkit"]["assets"]
    assert toolkit.platform_triple("Darwin", "arm64") in pin
    assert toolkit.platform_triple("Linux", "x86_64") in pin
    assert toolkit.platform_triple("Windows", "AMD64") in pin


def test_an_archive_that_differs_from_the_pin_is_refused(tmp_path):
    f = tmp_path / "a.tar.gz"
    f.write_bytes(b"not the release")
    with pytest.raises(ValueError, match="size"):
        toolkit.verify_archive(f, 5, "0" * 64)
    with pytest.raises(ValueError, match="sha256"):
        toolkit.verify_archive(f, f.stat().st_size, hashlib.sha256(b"other").hexdigest())
    toolkit.verify_archive(f, f.stat().st_size, hashlib.sha256(b"not the release").hexdigest())


def test_extraction_takes_only_the_binary_member(tmp_path):
    archive = tmp_path / "t.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for name, data in (("pkg/sysmlv2", b"#!/bin/sh\necho x\n"), ("../evil", b"no")):
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    dest = tmp_path / "bin" / "sysmlv2"
    toolkit._extract_binary(archive, "sysmlv2", dest)
    assert dest.read_bytes().startswith(b"#!") and os.access(dest, os.X_OK)
    assert not (tmp_path / "evil").exists() and sorted(
        p.name for p in tmp_path.rglob("*") if p.is_file()
    ) == ["sysmlv2", "t.tar.gz"]


def test_a_missing_toolkit_names_the_provisioning_command(monkeypatch, tmp_path):
    monkeypatch.setenv("SYSML_TOOLKIT_BIN", str(tmp_path / "absent"))
    monkeypatch.setenv("SYSML_TOOLKIT_LIB", str(tmp_path / "absent-lib"))
    with pytest.raises(FileNotFoundError) as e:
        toolkit.locate()
    assert toolkit.FETCH_COMMAND in str(e.value) and "SYSML_TOOLKIT_BIN" in str(e.value)


# ---------------------------------------------------------------------------------------------
# R-8: the probe record and the engines
# ---------------------------------------------------------------------------------------------
def test_engine_names_of_the_probe_record_exist(v2):
    """R-8: the engines the record lists are in list_engines(); readiness as recorded."""
    engines = {e.name: e for e in v2.connection.list_engines()}
    record = PROBE_RECORD.read_text()
    for name in ("check", "explore", "run", "smt", "solve", "sweep", "tool:fmi"):
        assert name in engines, f"engine {name} listed in the probe record is not in list_engines()"
        assert name in record
    assert all(engines[n].ready for n in ("check", "explore", "run", "smt", "solve", "sweep")) or (
        not ex.solver_available()
    )


@pytest.fixture(scope="module")
def probe_results(solver):
    return {r["name"]: r for r in probes.run_all()}


@pytest.mark.parametrize("name", [p.__name__.removeprefix("probe_") for p in probes.PROBES])
def test_probe_still_holds(name, probe_results):
    """R-8: re-running a probe gives the facts the record holds; the failure names the probe."""
    r = probe_results[name]
    assert r["ok"], f"probe {name} no longer matches the recorded result: {r['observation'][:300]}"
