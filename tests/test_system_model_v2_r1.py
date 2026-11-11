"""Tests for the WP22 content of the cubesat SysML model: one model, two views, metrics traced.

``model_v2/cubesat.sysml`` is the model adopted at WP23's data gate (``WP23-decisions.md``); the
WP22 version it replaced (adopted at WP22d, in history at d3018ba) and the WP15 version (2d13465)
stay in history only. WP22 added requirement definitions over the traded metrics' own quantities,
a measured ``peakTorque`` in ``SlewMeasurement``, ``verify`` objectives for each, and the two views
marked in the file. WP23 G5 removed slew time (``SlewTimeRequirement``, ``SlewBandRequirement``
and the measured ``slewTime``): the case has one time metric, the settling time, and the sets below
are stated without them; WP23 D-1 gave the four metrics WP22 left open a requirement each. The
tests hold the scope's guards: the model loads and checks clean (R-8), every covered metric has a
requirement and a ``verify`` (R-1, R-2), no traded metric is open (R-3), the numeric literals added
to the WP15 model are the recorded measurement and the one illustrative constant WP23 typed (R-4),
regenerated designs equal the committed method's results (R-6), and both views regenerate from the
model, change with it, and are the committed views (R-9). The toolkit gates (R-8) on this file run
in ``test_model_checking_v2.py``.
"""

from __future__ import annotations

import importlib.util
import os
import pathlib
import re
import warnings

import cubesat_model as cm
import pytest
from opensysml.values import Quantity
from test_system_model_v2 import (
    ADCS_DIR,
    ATTRIBUTES,
    TEXT,
    V2,
    P,
    _measure_slew,
    _rel,
)

# The views generator (WP22's spike, kept there as the record) and the committed views it writes.
PROJECT = ADCS_DIR.parents[1] / "docs/superpowers/notes/spike-sysml-diagrams/project.py"
VIEWS = ADCS_DIR / "model_v2" / "views"
# The requirement definitions of the WP15 model (sha256 28dbeeb23cf4..., commit 2d13465), which
# the swap replaced; WP22 added one per newly covered metric.
WP15_REQUIREMENTS = {
    "PowerRequirement",
    "SettledRequirement",
    "MomentumRequirement",
    "DepthOfDischargeRequirement",
    "SlewBandRequirement",
}
# The slew-time requirements, gone with the slew time (WP23 G5): the band requirement folds with
# the slew-time requirement into SettledRequirement.
SLEW_REQUIREMENTS = {"SlewTimeRequirement", "SlewBandRequirement"}
# The requirement definitions WP22 added, less slew time and less the eclipse reserve's (WP22 added
# it; the WP23 close-out removed it with its calc: it restated the depth-of-discharge requirement).
WP22_REQUIREMENTS = (WP15_REQUIREMENTS - SLEW_REQUIREMENTS) | {
    "PowerMarginRequirement",
    "EnergyBalanceRequirement",
}
# The numeric literals of the WP15 model's code (comments and docs removed), read from that file
# at the gate; WP22 may add recorded measurements only (R-4).
WP15_LITERALS = frozenset(
    {
        *("0.0", "2.0e-6", "7.70613052023095e-06", "0.0003", "1.13e-3", "1.7453292519943296e-3"),
        *("0.002", "0.00466041037173962", "0.010", "0.01", "0.03", "0.030", "0.1", "0.100"),
        *("0.12", "0.15", "0.2", "0.226", "0.25", "0.28", "0.3", "0.340", "0.34", "0.35", "0.4"),
        *("0.5", "0.60", "0.6", "0.7", "0.8", "0.9", "0.90", "1.0", "1.2", "1.5", "2.0", "2"),
        *("2.5", "3", "3.0", "3.141592653589793", "4.0", "8.0", "10.0", "12.0", "16.0", "20.0"),
        *("26.5", "30.0", "40.0", "80.0", "81.627336", "140.0", "180.0", "180.1904772571943"),
        *("200.0", "600.0", "1361.0", "3600.0", "5.0e4"),
    }
)

# The traded metrics covered by WP22 (six in its first round; slew time left with WP23 G5, the
# eclipse reserve with the WP23 close-out), with the requirement def over each one's own quantity.
COVERED = {
    "settling time": "SettledRequirement",
    "power margin": "PowerMarginRequirement",
    "energy balance": "EnergyBalanceRequirement",
    "depth of discharge": "DepthOfDischargeRequirement",
}
# The four WP22 left open (each needed a bound the configuration did not state), covered by WP23
# D-1 on the loop's proposed thresholds (the total mass through its launch-cost MoE).
WP23_COVERED = {
    "pointing error": "PointingErrorRequirement",
    "control effort": "ControlEffortRequirement",
    "total mass": "LaunchBudgetRequirement",
    "peak slew power": "PeakSlewPowerRequirement",
}
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
    """The model (the fixture keeps its round-1 name)."""
    try:
        return V2(TEXT)
    except cm.OpenSysMLUnavailable as exc:
        flag = " (REQUIRE_OPENSYSML is set)" if os.environ.get("REQUIRE_OPENSYSML") else ""
        pytest.fail(f"the opensysml client could not start{flag}: {exc}", pytrace=False)


@pytest.fixture(scope="module")
def frozen():
    try:
        return cm.load_model()
    except cm.OpenSysMLUnavailable as exc:
        pytest.fail(f"the opensysml client could not start: {exc}", pytrace=False)


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
# the model loads and checks clean; the two views are marked
# ---------------------------------------------------------------------------------------------
def test_strict_load_self_check_one_package_and_the_two_views_marked(r1):
    """The model loads strictly, holds its self check, and names its two views."""
    assert r1.model.ok
    assert not [d for d in r1.model.diagnostics if d.severity == "error"]
    assert r1.model.self_check().status == "holds"
    assert len(re.findall(r"^package\s", TEXT, flags=re.M)) == 1
    headers = re.findall(r"^    // (\d\. [^\n:]*)", TEXT, flags=re.M)
    assert len(headers) == 7
    for want in VIEW_SECTIONS:
        assert any(h.startswith(want) for h in headers), want
    assert "CONFIGURATION view" in TEXT and "ASSESSMENT view" in TEXT


def test_numeric_literals_added_are_the_recorded_measurement_and_the_launch_rate():
    """R-4: the numeric literals added to the WP15 code are the baseline's measured control effort
    (WP22 round 2; its measured slew time left with the slew time, WP23 G5) and the illustrative
    launch rate (WP23 G2, labelled like the model's other constants), and the supervisor's four
    thresholds (the WP23 close-out, ``WP23-decisions.md``, "The four thresholds"): 0.008495
    degree, 0.05922 N.m.s, 2.6 W and 90,643 USD, each with its doc in ``budgets``;
    ``test_system_model_v2.py`` reads them through the toolkit.
    """
    number = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
    added = set(number.findall(_code(TEXT))) - WP15_LITERALS
    assert added == {"0.009490621914197469", "6000.0", "0.008495", "0.05922", "2.6", "90643.0"}
    assert "launchRate : Real = 6000.0" in _code(TEXT)
    assert "133.6904772571943" not in added  # the baseline's slew time, gone with slewTime


# ---------------------------------------------------------------------------------------------
# R-1, R-2, R-3: requirements, satisfy, verify; the open metrics named
# ---------------------------------------------------------------------------------------------
def test_requirement_defs_hold_the_wp22_set_and_no_slew_time_requirement(r1):
    """The WP15 and WP22 requirement definitions less the two slew-time ones (WP23 G5), and one
    per metric WP22 left open (WP23 D-1); the full set is pinned in test_model_checking_v2.py."""
    defs = set(_kinds(r1.model, "RequirementDefinition"))
    assert defs >= WP22_REQUIREMENTS | set(WP23_COVERED.values())
    assert not defs & SLEW_REQUIREMENTS


def test_each_covered_metric_has_a_verify_in_a_verification_case(r1):
    """R-2: the opensysml client lists the verification cases and what each verifies."""
    verified = _verified(r1.model)
    assert "PowerRequirement" in verified["ConfigurationVerification"]
    assert verified["SlewVerification"] >= {
        "SettledRequirement",
        "MomentumRequirement",
        "DepthOfDischargeRequirement",
        *(COVERED[m] for m in ("power margin", "energy balance")),
    }
    everything = set().union(*verified.values())
    assert set(COVERED.values()) | set(WP23_COVERED.values()) <= everything
    assert not everything & SLEW_REQUIREMENTS


def test_every_requirement_is_satisfied_by_the_baseline(r1):
    verdicts = r1.model.verify_satisfaction()
    assert len(verdicts) >= len(WP22_REQUIREMENTS)  # the seven, plus WP23's additions
    assert all(v.holds and v.status == "holds" and v.engine == "run" for v in verdicts)
    assert r1.model.satisfied()


def test_no_traded_metric_is_open_and_the_verification_docs_name_each(r1):
    """R-3 after WP23 D-1: the four metrics WP22 named open in the verification docs each have a
    requirement now, and the docs name every covered metric (the total mass through the launch
    cost); no traded metric is left without one."""
    docs = " ".join(re.findall(r"verification def \w+ \{\s*doc /\*(.*?)\*/", TEXT, flags=re.S))
    docs = " ".join(docs.split())
    for metric in (*COVERED, *WP23_COVERED):
        assert metric in docs, metric
    assert not set(WP23_COVERED) & set(COVERED)
    defs = set(_kinds(r1.model, "RequirementDefinition"))
    assert set(WP23_COVERED.values()) <= defs
    assert "open" not in docs.lower() or "no requirement" not in docs.lower()


def test_baseline_measurement_has_the_recorded_peak_torque_and_control_effort(r1, frozen):
    """The measured defaults WP22 added are the baseline's measured slew (0.5 s step); the slew
    time among them left with WP23 G5."""
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
    assert read("peakTorque", "SI::N*SI::m") == pytest.approx(got["peak_torque"], rel=1e-3)
    assert "slewTime" not in _code(TEXT)  # the measurement has one time: settlingTime
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
def test_regenerated_designs_equal_the_frozen_oracle(box, r1, frozen):
    """R-6: the analysis (eight attributes), the flags and the new requirements' verdicts agree.

    Same seed, both gain boxes. Attributes: the model's analysis equals the frozen oracle to 1e-9;
    the four flags the model's requirements decide equal the frozen flags; each new requirement's
    verdict equals an independent Python reading of the frozen attribute. (Equality with the WP15
    model was shown at the gate; ``WP22-review.md``, gate comparison report.)
    """
    designs = _designs(box)
    loaded, symbols = r1.configure(designs)
    frozen_cfgs = frozen.configure(designs)
    ms = r1.model.eval(f"{P}::nominalSlew.horizon")
    assert float(r1.value(ms, "SI::s")) == 600.0
    worst = 0.0
    for sym, cfg in zip(symbols, frozen_cfgs, strict=True):
        measured = _measure_slew(frozen, cfg, t_end=600.0, max_step=0.5)
        want = frozen.measure(cfg)
        # the frozen model has no momentum headroom (WP30, D-1 (a)): the wheel class capacity over
        # the peak momentum, the inverse of the utilisation WP4b reads
        want["momentum_headroom"] = (
            frozen.sim_params(cfg)["maxMomentum"] / measured["peak_momentum"]
        )
        got = r1.experiment(loaded, sym, measured)
        for name, _ in ATTRIBUTES:
            worst = max(worst, _rel(got[name], want[name]))
        args = {
            "settlingTime": Quantity(measured["settling_time"], r1.unit("SI::s")),
            "peakTorque": Quantity(measured["peak_torque"], r1.unit("SI::N*SI::m")),
            "peakMomentum": Quantity(measured["peak_momentum"], r1.unit("SI::N*SI::m*SI::s")),
            "torqueSquaredIntegral": measured["torque_squared_integral"],
        }
        power = loaded.verify_requirement(f"{P}::PowerRequirement", subject=sym)
        assert bool(power.holds) == want["power_ok"]
        assert _verdict(loaded, sym, args, "SettledRequirement") == want["settled"]
        assert _verdict(loaded, sym, args, "MomentumRequirement") == want["momentum_ok"]
        assert _verdict(loaded, sym, args, "DepthOfDischargeRequirement") == want["dod_ok"]
        assert _verdict(loaded, sym, args, "PowerMarginRequirement") == (
            want["power_margin_w"] >= 0
        )
        assert _verdict(loaded, sym, args, "EnergyBalanceRequirement") == (
            want["energy_balance_wh"] >= 0
        )
    assert worst < 1e-9, worst


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
    _, behaviour, facts = _views(project, TEXT, tmp_path)
    drawn = {(project.short(r), n): ev for r, n, s, ev in facts["rel"] if s == "strong"}
    for metric, req in COVERED.items():
        assert (req, metric) in drawn, (req, metric)
    assert {n for _, n in drawn} >= set(COVERED)  # WP23's model adds lines for the four open
    assert set(facts["related"]) >= set(COVERED)
    assert "slew time" not in facts["metric_element"]  # one time metric (WP23 G5)
    # the four WP22 left open have their line (WP23 D-1): three read the metric's own quantity, the
    # launch budget reads the launch cost, the MoE drawn as a box between it and the total mass
    moe = {(project.short(r), n): ev for r, n, s, ev in facts["rel"] if s == "moe"}
    for metric, req in WP23_COVERED.items():
        assert (req, metric) in drawn or (req, metric) in moe, (req, metric)
    assert moe == {("LaunchBudgetRequirement", "total mass"): "LaunchCost"}
    assert "(no requirement)" not in behaviour  # no dashed box: no open metric remains
    # the MoE is two lines: requirement to launch cost (a requirement line, thickness 2) and launch
    # cost to the total mass (revision 7: dashed, a derived-from line, not a requirement line)
    assert behaviour.count("thickness=2") == len(drawn) + len(moe)
    assert behaviour.count("dashed,thickness=3") == len(moe)
    assert "dashed]" not in behaviour  # no other dashed or prose-only relation line
    # round 2: control effort is a SlewMeasurement attribute, so its source is the measurement
    assert facts["metric_element"]["control effort"] == ("measured", "controlEffort")
    assert facts["origin"]["control effort"] == "measurement"


def test_the_picture_reads_cold_requirements_apart_sources_distinct_no_long_detours(
    project, tmp_path
):
    """Round 2 (reviewer B-1, B-3, B-4, B-5): what a reader sees in the behavioural view's text."""
    _, behaviour, facts = _views(project, TEXT, tmp_path)
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
    boxes = [x for x in behaviour.splitlines() if x.lstrip().startswith("rectangle")]
    assert sum(analysis in x for x in boxes) == 1  # the legend's swatch is not a box
    # each source arrow ends at a metric of the subsystem it sits beside: one analysis box, one
    # measurement box, eleven edges at most (no arrow from a source to a package)
    assert behaviour.count("<-[#6B6B6B]-") == len(facts["metrics"])


def test_assembly_alternatives_in_enum_order_and_the_legend_names_what_is_drawn(project, tmp_path):
    """Round 2 (A-1, A-2): alternatives follow the enum; the legend names nothing absent."""
    assembly, _, _ = _views(project, TEXT, tmp_path)
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
    # revision 5 (WP23 round 4): the legend keeps the tag keys; the levels and ranges, the gain
    # ranges by regime among them, are the caption's, written by the generator from the model
    assert "swap" in legend and "tune" in legend and "untagged" in legend
    assert "Kp:" not in legend and "Kd:" not in legend
    caption: list = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m, byid = project.load(tmp_path / "m.sysml")
        project.assembly(m, byid, P, caption=caption)
    assert any(x.startswith("Kp:") for x in caption) and any(x.startswith("Kd:") for x in caption)
    # revision 6 (WP23 post-gate view-consistency unit, disposition C): the caption ties each regime
    # name to the model's gain box (the legend still names neither)
    kp = next(x for x in caption if x.startswith("Kp:"))
    assert "baseline regime, baselineGains" in kp and "primary regime, aggressiveGains" in kp
    # one identifier level in the tags: the swap tags name attributes, as the tune tags do; the
    # caption gives the enum behind each swap
    assert "swap </b></back> wheelClass" in assembly and "swap </b></back> grade" in assembly
    assert "TrackerGrade" not in "".join(x for x in assembly.splitlines() if "swap </b>" in x)
    assert (
        "wheelClass (enum WheelClass):" in caption[0] and "grade (enum TrackerGrade):" in caption[1]
    )
    committed = (VIEWS / "assembly_caption.md").read_text().splitlines()[2:]
    assert committed == [f"- {x}" for x in caption]


def test_the_analysis_box_names_what_needs_no_slew_and_the_caption_is_the_committed_one(
    project, tmp_path
):
    """Disposition B: the analysis box names what the analysis returns and what needs no slew."""
    _, behaviour, facts = _views(project, TEXT, tmp_path)
    box = next(x for x in behaviour.splitlines() if "as xAnalysis" in x)
    assert "returns 7 of 8" in box and "pointing error" in box and "total mass" in box
    # the control effort and the settling time come from the measurement (disposition G3-P2-6)
    assert "control effort\\n(passed on)" in box and "settling time\\n(not returned)" in box
    cap = facts["caption"]
    assert (
        "returns 7 of the 8" in cap[0] and "settling time is read from `SlewMeasurement`" in cap[0]
    )
    assert "ConfigurationVerification" in cap[1] and "SlewVerification" in cap[1]
    assert "coverage.md" in cap[2] and "coverage.md" in cap[3]
    # revision 9 (the WP23 close-out): the negated satisfy is drawn and named, not read as satisfied
    assert "`cubesatBaseline` satisfies every requirement but `PointingErrorRequirement`" in cap[4]
    assert facts["fails"][f"{P}__PointingErrorRequirement"] == {"cubesatBaseline"}
    box = next(x for x in behaviour.splitlines() if "**PointingErrorRequirement**" in x)
    assert "not satisfied by cubesatBaseline" in box
    committed = (VIEWS / "behavioural_caption.md").read_text().splitlines()[2:]
    assert committed == [f"- {x}" for x in cap]


def test_the_legend_names_every_colour_and_line_kind_and_the_type_has_a_floor(project, tmp_path):
    """G-3 blocks (revision 7): the legend carries each colour and line kind drawn; the caption the
    MoE rule; the smallest type of the committed view at its 700 px width is the paper's 12.5 px."""
    _, behaviour, facts = _views(project, TEXT, tmp_path)
    legend = behaviour[behaviour.index("legend bottom") :]
    for colour in (
        project.REQ_COLOUR,
        project.COVERED_COLOUR,
        project.MOE_COLOUR,
        project.ANALYSIS_COLOUR,
        project.MEASURE_COLOUR,
    ):
        assert f"<back:{colour}>" in legend, colour
    for kind in ("requirement reads metric", "computed from", "value comes from"):
        assert kind in legend, kind
    assert project.RELATION_COLOUR in legend and project.SOURCE_COLOUR in legend
    assert "A metric marked MoE is a measure of effectiveness" in "".join(facts["caption"])
    assert "pointing error and the launch cost" in "".join(facts["caption"])
    svg = (VIEWS / "behavioural_view.svg").read_text()
    sizes = [float(s) for s in re.findall(r'font-size="([0-9.]+)"', svg)]
    assert min(sizes) >= 12.5, min(sizes)


def test_views_change_only_with_what_was_edited_and_are_stable(project, tmp_path):
    """R-9: an added alternative changes the assembly only, an added requirement the behaviour."""
    a0, b0, _ = _views(project, TEXT, tmp_path)
    again = _views(project, TEXT, tmp_path)
    assert (a0, b0) == again[:2]
    alt = (
        TEXT.rstrip()[:-1]
        + "\n    part def XLWheel :> ReactionWheel {\n"
        + (
            "        :>> wheelClass = WheelClass::large;\n        :>> maxTorque = 0.010 [N*m];\n"
            "        :>> maxMomentum = 0.100 [N*m*s];\n        :>> mass = 0.60 [kg];\n    }\n}\n"
        )
    )
    a1, b1, _ = _views(project, alt, tmp_path)
    assert a1 != a0 and "XLWheel" in a1 and b1 == b0
    req = TEXT.rstrip()[:-1] + (
        "\n    requirement def MassRequirement {\n        subject c : Cubesat;\n"
        "        require constraint { c.totalMass < 20.0 [kg] }\n    }\n}\n"
    )
    a2, b2, _ = _views(project, req, tmp_path)
    assert a2 == a0 and b2 != b0 and "MassRequirement" in b2


def test_committed_views_are_the_generators_output_on_the_model(project, tmp_path):
    """R-9: three runs give the same text, and it is the committed views of the model."""
    runs = [_views(project, TEXT, tmp_path)[:2] for _ in range(3)]
    assert runs[0] == runs[1] == runs[2]
    assembly, behaviour = runs[0]
    assert (VIEWS / "assembly_view.puml").read_text() == assembly
    assert (VIEWS / "behavioural_view.puml").read_text() == behaviour
    for name in ("assembly_view", "behavioural_view"):
        for ext in ("svg", "png"):
            assert (VIEWS / f"{name}.{ext}").stat().st_size > 0, f"{name}.{ext}"
