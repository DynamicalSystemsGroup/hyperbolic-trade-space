"""Tests for the r1 cubesat SysML model (WP22 round 1): one model, two views, metrics traced.

``model_v2/cubesat_r1.sysml`` lives beside ``cubesat.sysml``, which the committed data and the paper
cite and which these tests leave untouched. Round 1 adds requirement definitions over the traded
metrics' own quantities, a measured ``slewTime`` and ``peakTorque`` in ``SlewMeasurement``,
``verify`` objectives for each, and the two views marked in the file. The tests hold the scope's
guards: the model loads and checks clean (R-8), every covered metric has a requirement and a
``verify`` (R-1, R-2), the open metrics are named (R-3), thresholds are values the model already
states (R-4),
the old model is unchanged (R-14), regenerated designs equal the committed method's results (R-6)
and both views regenerate from the model and change with it (R-9).
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import pathlib
import re
import warnings

import cubesat_model as cm
import pytest
from experiments import toolkit
from experiments.exclusion import solver_available
from opensysml.values import Quantity
from test_system_model_v2 import (
    ADCS_DIR,
    ATTRIBUTES,
    V2,
    P,
    _measure_slew,
    _rel,
)
from test_system_model_v2 import (
    MODEL as OLD_MODEL,
)

R1 = ADCS_DIR / "model_v2" / "cubesat_r1.sysml"
R1_TEXT = R1.read_text()
OLD_TEXT = OLD_MODEL.read_text()
PROJECT = ADCS_DIR.parents[1] / "docs/superpowers/notes/spike-sysml-diagrams/project.py"

# The six metrics of the first round, with the requirement def over each one's own quantity.
COVERED = {
    "settling time": "SettledRequirement",
    "slew time": "SlewTimeRequirement",
    "power margin": "PowerMarginRequirement",
    "energy balance": "EnergyBalanceRequirement",
    "eclipse reserve": "EclipseReserveRequirement",
    "depth of discharge": "DepthOfDischargeRequirement",
}
# Traded with no requirement in the model: each needs a bound the configuration does not state.
OPEN = ["pointing error", "control effort", "total mass", "peak slew power"]
VIEW_SECTIONS = {
    "1. CONFIGURATION SPACE (configuration view)",
    "2. THE CUBESAT (configuration view)",
    "3. ACCOUNTING (assessment view)",
    "4. SCENARIOS (assessment view)",
    "5. REQUIREMENTS, SATISFACTION AND VERIFICATION (assessment view",
    "6. THE EXPERIMENT (assessment view)",
    "7. NAMED CONFIGURATIONS (configuration view)",
}


@pytest.fixture(scope="module")
def r1():
    try:
        return V2(R1_TEXT)
    except cm.OpenSysMLUnavailable as exc:
        flag = " (REQUIRE_OPENSYSML is set)" if os.environ.get("REQUIRE_OPENSYSML") else ""
        pytest.fail(f"the opensysml client could not start{flag}: {exc}", pytrace=False)


@pytest.fixture(scope="module")
def old():
    try:
        return V2(OLD_TEXT)
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


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


def _kinds(model, kind):
    return {
        q.properties["name"]: q
        for q in model.query(scope=[P], where={"property": "@type", "operator": "=", "value": kind})
    }


def _verified(model) -> dict[str, set[str]]:
    out = {}
    for name in _kinds(model, "VerificationCaseDefinition"):
        found = set()
        for q in model.query(scope=[f"{P}::{name}"]):
            if q.properties.get("@type") == "SatisfyRequirementUsage":
                found.add(q.properties["type"].split("::")[-1])
        out[name] = found
    return out


def _code(text: str) -> str:
    """The model text without its comments and ``doc`` blocks."""
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    return re.sub(r"//[^\n]*", " ", text)


# ---------------------------------------------------------------------------------------------
# the model loads and checks clean; the two views are marked; the old model is untouched
# ---------------------------------------------------------------------------------------------
def test_strict_load_self_check_one_package_and_the_two_views_marked(r1):
    """The r1 model loads strictly, holds its self check, and names its two views."""
    assert r1.model.ok
    assert not [d for d in r1.model.diagnostics if d.severity == "error"]
    assert r1.model.self_check().status == "holds"
    assert len(re.findall(r"^package\s", R1_TEXT, flags=re.M)) == 1
    headers = re.findall(r"^    // (\d\. [^\n:]*)", R1_TEXT, flags=re.M)
    assert len(headers) == 7
    for want in VIEW_SECTIONS:
        assert any(h.startswith(want) for h in headers), want
    assert "CONFIGURATION view" in R1_TEXT and "ASSESSMENT view" in R1_TEXT


def test_the_old_model_is_unchanged_and_r1_only_adds_to_its_accounting():
    """R-14: the old file is what the ledger recorded; r1 keeps every calc def body as it was."""
    from experiments import ledger as lg

    entries = [
        e
        for e in lg.read(lg.LEDGER_PATH)
        if e.get("model_path") == "examples/adcs/model_v2/cubesat.sysml"
    ]
    assert entries[-1]["model_sha256"] == hashlib.sha256(OLD_MODEL.read_bytes()).hexdigest()
    old_calcs = re.findall(r"calc def \w+ \{.*?\n    \}", _code(OLD_TEXT), flags=re.S)
    assert len(old_calcs) >= 20
    for calc in old_calcs:
        assert calc in _code(R1_TEXT)


def test_numeric_literals_added_are_recorded_measurements_only():
    """R-4: the numeric literals r1 adds to the old code are recorded measurements, no threshold.

    The measured slew time (round 1) and the measured control effort of the baseline (round 2).
    """
    number = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
    added = set(number.findall(_code(R1_TEXT))) - set(number.findall(_code(OLD_TEXT)))
    assert added == {"133.6904772571943", "0.009490621914197469"}


# ---------------------------------------------------------------------------------------------
# R-1, R-2, R-3: requirements, satisfy, verify; the open metrics named
# ---------------------------------------------------------------------------------------------
def test_requirement_defs_are_the_old_five_plus_one_per_new_metric(r1, old):
    defs = set(_kinds(r1.model, "RequirementDefinition"))
    assert defs == set(_kinds(old.model, "RequirementDefinition")) | {
        "SlewTimeRequirement",
        "EclipseReserveRequirement",
        "PowerMarginRequirement",
        "EnergyBalanceRequirement",
    }


def test_each_covered_metric_has_a_verify_in_a_verification_case(r1):
    """R-2: the opensysml client lists the verification cases and what each verifies."""
    verified = _verified(r1.model)
    assert verified["ConfigurationVerification"] == {"PowerRequirement"}
    assert verified["SlewVerification"] == {
        "SettledRequirement",
        "MomentumRequirement",
        "DepthOfDischargeRequirement",
        "SlewBandRequirement",
        *(COVERED[m] for m in ("slew time", "power margin", "energy balance", "eclipse reserve")),
    }
    assert set(COVERED.values()) <= set().union(*verified.values())


def test_every_requirement_is_satisfied_by_the_baseline(r1):
    verdicts = r1.model.verify_satisfaction()
    assert len(verdicts) == 9
    assert all(v.holds and v.status == "holds" and v.engine == "run" for v in verdicts)
    assert r1.model.satisfied()


def test_open_metrics_are_named_in_the_verification_cases_and_nowhere_covered(r1):
    """R-3: the model says which traded metrics no requirement reads, in the verification docs."""
    docs = " ".join(re.findall(r"verification def \w+ \{\s*doc /\*(.*?)\*/", R1_TEXT, flags=re.S))
    docs = " ".join(docs.split())
    for metric in OPEN:
        assert metric in docs, metric
    assert not set(OPEN) & set(COVERED)


def test_baseline_measurement_has_the_recorded_slew_time_and_peak_torque(r1, frozen):
    """The new measured defaults are the baseline's measured slew (0.5 s step)."""
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
    read = lambda k, u: r1.read(f"baselineMeasurement.{k}", u)  # noqa: E731
    assert read("slewTime", "SI::s") == pytest.approx(got["slew_time"], rel=1e-3, abs=0.5)
    assert read("peakTorque", "SI::N*SI::m") == pytest.approx(got["peak_torque"], rel=1e-3)
    # round 2: control effort is a measurement of the slew too (it was an unbound analysis input)
    assert read("controlEffort", "SI::N*SI::m*SI::s") == pytest.approx(
        got["control_effort"], rel=1e-3
    )


# ---------------------------------------------------------------------------------------------
# R-6: regenerated designs equal the committed method's results (both gain boxes)
# ---------------------------------------------------------------------------------------------
# The ``in`` parameter each requirement reads, and the measured quantity that binds it.
PARAM = {
    "SettledRequirement": "settlingTime",
    "MomentumRequirement": "peakMomentum",
    "DepthOfDischargeRequirement": "torqueSquaredIntegral",
    "SlewTimeRequirement": "slewTime",
    "EclipseReserveRequirement": "torqueSquaredIntegral",
    "PowerMarginRequirement": "peakTorque",
    "EnergyBalanceRequirement": "torqueSquaredIntegral",
}


def _verdict(model, symbol, args, req):
    """The model's verdict on one requirement of one configuration (measurement bound by name)."""
    v = model.verify_requirement(
        f"{P}::{req}", subject=symbol, named_arguments={PARAM[req]: args[PARAM[req]]}
    )
    assert v.status in ("holds", "violated"), (req, v.status)
    return bool(v.holds)


def _designs(frozen_box: str, n: int = 6, seed: int = 3):
    return [
        dict(r) for _, r in cm.load_model(gain_box=frozen_box).sample_designs(n, seed).iterrows()
    ]


@pytest.mark.parametrize("box", ["baseline", "aggressive"])
def test_regenerated_designs_equal_the_frozen_oracle_and_the_old_model(box, r1, old, frozen):
    """R-6: the analysis (eight attributes), the flags and the new requirements' verdicts agree.

    Same seed, both gain boxes. Attributes: the r1 analysis equals the frozen oracle to 1e-9 and
    the old v2 model exactly; the four flags the r1 requirements decide equal the frozen flags; each
    new requirement's verdict equals an independent Python reading of the frozen attribute.
    """
    designs = _designs(box)
    loaded, symbols = r1.configure(designs)
    old_loaded, old_symbols = old.configure(designs)
    frozen_cfgs = frozen.configure(designs)
    ms = r1.model.eval(f"{P}::nominalSlew.horizon")
    assert float(r1.value(ms, "SI::s")) == 600.0
    worst = 0.0
    for sym, osym, cfg in zip(symbols, old_symbols, frozen_cfgs, strict=True):
        measured = _measure_slew(frozen, cfg, t_end=600.0, max_step=0.5)
        want = frozen.measure(cfg)
        got = r1.experiment(loaded, sym, measured)
        was = old.experiment(old_loaded, osym, measured)
        assert got == was  # identical to the old model: nothing in the analysis changed
        for name, _ in ATTRIBUTES:
            worst = max(worst, _rel(got[name], want[name]))
        args = {
            "settlingTime": Quantity(measured["settling_time"], r1.unit("SI::s")),
            "slewTime": Quantity(measured["slew_time"], r1.unit("SI::s")),
            "peakTorque": Quantity(measured["peak_torque"], r1.unit("SI::N*SI::m")),
            "peakMomentum": Quantity(measured["peak_momentum"], r1.unit("SI::N*SI::m*SI::s")),
            "torqueSquaredIntegral": measured["torque_squared_integral"],
        }
        power = loaded.verify_requirement(f"{P}::PowerRequirement", subject=sym)
        assert bool(power.holds) == want["power_ok"]
        assert _verdict(loaded, sym, args, "SettledRequirement") == want["settled"]
        assert _verdict(loaded, sym, args, "MomentumRequirement") == want["momentum_ok"]
        assert _verdict(loaded, sym, args, "DepthOfDischargeRequirement") == want["dod_ok"]
        assert _verdict(loaded, sym, args, "DepthOfDischargeRequirement") == _verdict(
            old_loaded, osym, args, "DepthOfDischargeRequirement"
        )
        assert _verdict(loaded, sym, args, "SlewTimeRequirement") == (want["slew_time_s"] < 600.0)
        assert _verdict(loaded, sym, args, "EclipseReserveRequirement") == (
            want["eclipse_reserve_wh"] >= 0
        )
        assert _verdict(loaded, sym, args, "PowerMarginRequirement") == (
            want["power_margin_w"] >= 0
        )
        assert _verdict(loaded, sym, args, "EnergyBalanceRequirement") == (
            want["energy_balance_wh"] >= 0
        )
    assert worst < 1e-9, worst


# ---------------------------------------------------------------------------------------------
# R-8: the toolkit gates, with the pinned binary
# ---------------------------------------------------------------------------------------------
def test_toolkit_check_lint_and_verify_solve_pass_on_r1(toolkit_bin):
    assert toolkit_bin.check(R1).returncode == 0
    summary = toolkit_bin.lint(R1)["summary"]
    assert summary["errors"] == 0 and summary["warnings"] == 0, summary
    if not solver_available():
        pytest.fail(
            "the solve engine needs z3 or cvc5 on PATH (`uv run` provides z3)", pytrace=False
        )
    out = toolkit_bin.verify_solve(R1)
    assert out.returncode == 0, out.stdout[-500:] + out.stderr[-500:]
    assert "0 violated" in out.stdout


# ---------------------------------------------------------------------------------------------
# R-1, R-9: the views are generated from the model's elements and change with it
# ---------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def project():
    spec = importlib.util.spec_from_file_location("wp22_project", PROJECT)
    mod = importlib.util.module_from_spec(spec)
    with warnings.catch_warnings():
        spec.loader.exec_module(mod)
    return mod


def _views(project, text: str, tmp_path: pathlib.Path):
    path = tmp_path / "m.sysml"
    path.write_text(text)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m, byid = project.load(path)
        assembly = project.assembly(m, byid, P)
        behaviour, facts = project.behavioural(m, byid, P)
    return assembly, behaviour, facts


def test_every_covered_metric_has_a_thick_line_from_its_requirement(project, tmp_path):
    """R-1: the relation is read from the model; each covered metric has one, the open ones none."""
    _, behaviour, facts = _views(project, R1_TEXT, tmp_path)
    drawn = {(project.short(r), n): ev for r, n, s, ev in facts["rel"] if s == "strong"}
    for metric, req in COVERED.items():
        assert (req, metric) in drawn, (req, metric)
    assert {n for _, n in drawn} == set(COVERED)
    assert set(facts["related"]) == set(COVERED)
    for metric in OPEN:
        # dashed, and captioned in its own box (round 2)
        assert re.search(
            rf'rectangle "{metric}\\n\(no requirement\)" as \w+ [^\n]*line\.dashed', behaviour
        )
    assert behaviour.count("thickness=2") == len(drawn)
    assert "dashed]" not in behaviour  # no dashed or prose-only relation line
    assert facts["metric_element"]["slew time"] == ("measured", "slewTime")
    # round 2: control effort is a SlewMeasurement attribute, so its source is the measurement
    assert facts["metric_element"]["control effort"] == ("measured", "controlEffort")
    assert facts["origin"]["control effort"] == "measurement"


def test_the_picture_reads_cold_requirements_apart_sources_distinct_no_long_detours(
    project, tmp_path
):
    """Round 2 (reviewer B-1, B-3, B-4, B-5): what a reader sees in the behavioural view's text."""
    _, behaviour, facts = _views(project, R1_TEXT, tmp_path)
    # requirements with no line are in one separate group, not among those with lines
    group = behaviour[
        behaviour.index("as xNoLine") : behaviour.index("\n}\n", behaviour.index("as xNoLine"))
    ]
    no_line = {project.short(r) for r in facts["reqs"]} - {
        project.short(r) for r, *_ in facts["rel"]
    }
    assert no_line and all(f"**{r}**" in group for r in no_line)
    for r, *_ in facts["rel"]:
        assert f"**{project.short(r)}**" not in group
    # the analysis box has a colour no metric box has
    covered, analysis = project.COVERED_COLOUR, project.ANALYSIS_COLOUR
    assert covered != analysis and "xAnalysis " + analysis in behaviour
    assert behaviour.count(analysis) == 1
    # each source arrow ends at a metric of the subsystem it sits beside: one analysis box, one
    # measurement box, eleven edges at most (no arrow from a source to a package)
    assert behaviour.count("<-[#6B6B6B]-") == len(facts["metrics"])


def test_assembly_alternatives_in_enum_order_and_the_legend_names_what_is_drawn(project, tmp_path):
    """Round 2 (A-1, A-2): alternatives follow the enum; the legend names nothing absent."""
    assembly, _, _ = _views(project, R1_TEXT, tmp_path)
    for abstract, order in (
        ("ReactionWheel", ["SmallWheel", "MediumWheel", "LargeWheel"]),
        ("StarTracker", ["CoarseTracker", "MediumTracker", "FineTracker"]),
    ):
        lines = [x for x in assembly.splitlines() if x.startswith(f"{abstract} <|--")]
        assert [x.split("-- ")[1] for x in lines] == order
        declared = [
            x
            for x in assembly.splitlines()
            if x.startswith("class") and any(f"**{a}**" in x for a in order)
        ]
        assert [next(a for a in order if f"**{a}**" in x) for x in declared] == order
    legend = assembly[assembly.index("legend bottom") :]
    assert "baselineGains" not in legend and "aggressiveGains" not in legend
    assert "Kp:" in legend and "Kd:" in legend


def test_views_change_only_with_what_was_edited_and_are_stable(project, tmp_path):
    """R-9: an added alternative changes the assembly only, an added requirement the behaviour."""
    a0, b0, _ = _views(project, R1_TEXT, tmp_path)
    again = _views(project, R1_TEXT, tmp_path)
    assert (a0, b0) == again[:2]
    alt = (
        R1_TEXT.rstrip()[:-1]
        + "\n    part def XLWheel :> ReactionWheel {\n"
        + (
            "        :>> wheelClass = WheelClass::large;\n        :>> maxTorque = 0.010 [N*m];\n"
            "        :>> maxMomentum = 0.100 [N*m*s];\n        :>> mass = 0.60 [kg];\n    }\n}\n"
        )
    )
    a1, b1, _ = _views(project, alt, tmp_path)
    assert a1 != a0 and "XLWheel" in a1 and b1 == b0
    req = R1_TEXT.rstrip()[:-1] + (
        "\n    requirement def MassRequirement {\n        subject c : Cubesat;\n"
        "        require constraint { c.totalMass < 20.0 [kg] }\n    }\n}\n"
    )
    a2, b2, _ = _views(project, req, tmp_path)
    assert a2 == a0 and b2 != b0 and "MassRequirement" in b2
