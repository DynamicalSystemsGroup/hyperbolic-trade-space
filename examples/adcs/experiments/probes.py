# ruff: noqa: E501
"""Probes of the SysML runtime and the model-checking toolkit, run against the live runtime (WP15, 15.2).

Eleven probes, each a small function returning ``{name, ok, observation, evidence}``:

1. cross-source ``import``; 2. a false ``assert satisfy`` loading without a diagnostic; 3. ``satisfy``
target kinds; 4. ``verify_requirement`` and ``verify_satisfaction`` on the cubesat baseline and a
negative control; 5. ``verify_constraint(question="holds")`` on the ``smt`` and ``solve`` engines, the
evidence strength, the range-bounded claims, and the exclusion of infeasible configurations and model
variants before simulation; 6. ``run_analysis`` with ``in`` parameters, ``run_sweep`` (grid, ``samples`` +
``seed``); 7. ``record_run`` and ``run_runs``; 8. unit labels from ``eval``; 9. ``query`` and
``to_api_json``; 10. the engine list and its readiness; 11. the model-checking toolkit (release assets,
checksums, a local build).

``EXPECTED`` holds the recorded facts of each probe. ``run_all()`` runs every probe; a probe is ``ok`` when its
observed ``facts`` equal the recorded ones, so a test detects a changed behaviour of the runtime or the
toolkit. The narrative record is ``probes/probe-record.md``; ``--write`` rewrites its generated table.

Run as a script::

    uv run python examples/adcs/experiments/probes.py [--write] [--network]

``--network`` also compares probe 11 with the published release assets (needs ``gh``). Environment: the
``solve`` and ``smt`` engines need ``z3`` (or ``cvc5``) on ``PATH``; ``SYSMLV2_BIN`` and ``SYSMLV2_LIB``
name a built toolkit binary and a standard-library directory for the local part of probe 11.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import warnings
from collections import Counter

import opensysml

HERE = pathlib.Path(__file__).resolve().parent
MODEL_PATH = HERE.parent / "cubesat_tradespace.sysml"
RECORD_PATH = HERE / "probes" / "probe-record.md"
PKG = "CubesatTradeSpace::"
BEGIN, END = "<!-- probes:begin -->", "<!-- probes:end -->"

TOOLKIT_VERSION = "v0.12.0"
TOOLKIT_REPO = "Open-MBEE/sysml-toolkit"
# Release v0.12.0 as published on 2026-11-08T23:27:14Z: asset name -> (size in bytes, sha256 published
# with the asset). Recorded, not downloaded; ``SHA256SUMS`` is itself an asset (869 bytes).
RELEASE_ASSETS = {
    "SHA256SUMS": (869, "aec6b4244b265e06675c57e2e2170489fbd49fa9a5cd9afa3af92c2f8680bfc9"),
    "SIZES.md": (669, "d16665390c129646bfad88cf3b9561d4211d1b8a8aeb5f932a4605002466989f"),
    "sysml-wasm-0.12.0.tgz": (
        16049331,
        "1c905c0edfcd3abaf23a82a71e770a52d2cef69a9b06f4e6ad7e49a4aaea08f2",
    ),
    "sysmlv2-0.12.0-aarch64-apple-darwin.tar.gz": (
        5593394,
        "d2a2208e8b9ffbd570176d6122bfabf494e3344e67f65b9a87e8889c56238195",
    ),
    "sysmlv2-0.12.0-aarch64-unknown-linux-gnu.tar.gz": (
        5905427,
        "21b1dfad0ea82b0dd379a988276c91e07256ee1958af38fdb81e25ae0a3c724a",
    ),
    "sysmlv2-0.12.0-aarch64-unknown-linux-musl.tar.gz": (
        5844612,
        "10f43f21a7899de1c8698797c11d05b1fdbe3bfeec48898e6c2555ffb514bf70",
    ),
    "sysmlv2-0.12.0-x86_64-apple-darwin.tar.gz": (
        6055486,
        "2a89c4ef1bb33fd5bf5bcf3f7430f9a1f4029f1981480152e307709ffe4b41c8",
    ),
    "sysmlv2-0.12.0-x86_64-pc-windows-msvc.zip": (
        5972068,
        "a9f0daca2cb7697447fc77e59d4eaded37a55fa195181e0d722794a8182c3971",
    ),
    "sysmlv2-0.12.0-x86_64-unknown-linux-gnu.tar.gz": (
        6300846,
        "0f17df5c0eefbfc1715e98a30c533476a7323c2d20145065589fbf7d2227d497",
    ),
    "sysmlv2-0.12.0-x86_64-unknown-linux-musl.tar.gz": (
        6379052,
        "c84bb9cd0b79e67c4819d8646bc4e5123211b8c0922770a17fdf9a65ab26fd68",
    ),
}

# Recorded facts: what each probe observed at opensysml 0.12.1 / toolkit v0.12.0 on darwin-arm64 with
# z3 on PATH. A probe is ok when its observed facts equal these.
EXPECTED: dict[str, dict] = {
    "cross_source_import": {
        "single_source_unresolved": True,
        "load_of_one_file_unresolved": True,
        "parse_sources_resolves": True,
        "parse_sources_order_free": True,
        "concatenation_resolves": True,
        "bare_import_is_error": True,
    },
    "false_assert_satisfy": {
        "loads_ok": True,
        "strict_load_accepts": True,
        "diagnostics": 0,
        "verdict_holds": [False, True],
        "satisfied": False,
        "false_verdict_strength": "witnessed",
    },
    "satisfy_target_kinds": {
        "requirement_def": False,
        "requirement_usage": True,
        "part_usage": False,
        "inline_requirement_usage": True,
        "verify_requirement_accepts_def_with_subject": True,
    },
    "verify_requirement_satisfaction": {
        "baseline_mass_kg": 13.2914,
        "satisfaction_verdicts": [True, False],
        "budget_ok": [True, "observed", "run"],
        "negative_control": [False, "violated", "witnessed"],
        "quantity_argument_by_limit_and_subject": {
            "20.0kg_baseline": True,
            "20.0kg_heavy": True,
            "5.0kg_baseline": False,
            "5.0kg_heavy": False,
        },
        "real_argument_for_quantity_parameter": ["undecided", True],
        "per_configuration_dod_constraint": [True, False],
        "per_configuration_power_constraint": True,
    },
    "holds_and_exclusion": {
        "solver_on_path": True,
        "model_with_probes_loads": True,
        "calc_invocation_claim_by_engine": {
            "smt": ["undecided", ""],
            "solve": ["undecided", ""],
            "check": ["undecided", ""],
            "auto": ["undecided", ""],
            "all": ["undecided", ""],
        },
        "calc_invocation_reason": True,
        "scalar_claim_by_engine": {
            "smt": ["undecided", "not covered"],
            "solve": ["holds", "proved"],
            "check": ["undecided", "not covered"],
            "auto": ["holds", "proved"],
            "all": ["holds", "proved"],
        },
        "smt_reason": "smt answers over every schedule; the que",
        "scalar_claims_on_solve": {
            "ProbeMassIdentity": ["holds", "proved"],
            "ProbeMassIdentityFalse": ["violated", "witnessed"],
            "ProbePowerMonotone": ["holds", "proved"],
            "ProbePowerMonotoneFalse": ["violated", "witnessed"],
            "ProbeRangeBounded": ["holds", "proved"],
            "ProbeRangeBoundedFalse": ["violated", "witnessed"],
            "ProbePowerOkEverywhere": ["holds", "proved"],
            "ProbeScalarFalse": ["violated", "witnessed"],
        },
        "scalar_violation_witnessed": True,
        "regions": {
            "ProbeBatteryTooSmall": "exclude",
            "ProbeBatteryLarge": "all_feasible",
            "ProbeBatteryFull": "mixed",
            "ProbeSmallWheelLowInertia": "all_feasible",
            "ProbeSmallWheelHighInertia": "exclude",
            "ProbeSmallWheelFullInertia": "mixed",
            "ProbeLargeWheelFullInertia": "all_feasible",
        },
        "region_evidence": {
            "ProbeBatteryTooSmall": [["unsatisfiable", "proved"], ["violated", "witnessed"]],
            "ProbeBatteryLarge": [["satisfiable", "witnessed"], ["holds", "proved"]],
            "ProbeBatteryFull": [["satisfiable", "witnessed"], ["violated", "witnessed"]],
            "ProbeSmallWheelLowInertia": [["satisfiable", "witnessed"], ["holds", "proved"]],
            "ProbeSmallWheelHighInertia": [["unsatisfiable", "proved"], ["violated", "witnessed"]],
            "ProbeSmallWheelFullInertia": [["satisfiable", "witnessed"], ["violated", "witnessed"]],
            "ProbeLargeWheelFullInertia": [["satisfiable", "witnessed"], ["holds", "proved"]],
        },
        "threshold_battery_wh": [26.6, 28.8],
        "threshold_small_wheel_inertia_kgm2": 0.6366,
    },
    "analysis_and_sweep": {
        "named_and_positional_agree": True,
        "run_analysis_engine": ["run", "observed"],
        "missing_in_parameter": "ExecutionError",
        "grid_endpoints_inclusive": True,
        "grid_product_rows_first_slowest": True,
        "samples_flag": [True, False],
        "same_seed_same_rows": True,
        "row_i_independent_of_n": True,
        "other_seed_differs": True,
        "uniform_draw_fraction_below_10_in_1_to_1000_small": True,
        "log_draw_through_exponent_fraction_below_10_near_third": True,
        "dimensionless_parameter_times_unit_inside_case": True,
        "quantity_typed_parameter_in_range": "ExecutionError: type mismatch",
    },
    "record_and_runs": {
        "record_names": [["Records::Cost_run1"], ["Records::Cost_run1"], ["Records::Cost_run2"]],
        "loaded_model_unchanged_by_record_run": True,
        "record_definition": ["Records", "Records::CostRun"],
        "sweep_records": [3, ["sweep"]],
        "provenance_has_timestamp": True,
        "provenance_tool": ["v0.12.1"],
        "record_returns_run": True,
        "runs_reproducible": True,
        "run_i_independent_of_n": True,
        "other_seed_differs": True,
        "ordinary_analysis_case_in_run_runs": "refused: needs Simulation::MonteCarlo",
    },
    "unit_labels": {
        "labels": {
            "totalMass": "kg",
            "generatedPower": "SI::'kg⋅m²⋅s⁻³'",
            "availablePower": "SI::'kg⋅m²⋅s⁻³'",
            "usableWheelTorque": "SI::'N⋅m'",
        },
        "unsimplified_power_label": True,
        "in_unit_converts": True,
        "generated_power_w": 48.9764,
        "product_label": "SI::'kg⋅m²⋅s⁻²'",
        "product_in_wh": 7.2,
    },
    "query_blind_spots": {
        "load_errors": 0,
        "duplicate_member_warnings": True,
        "query_sees_satisfy_and_connection": [2, 1],
        "unnamed_ids_use_at_numbers": True,
        "api_json_lists_them_too": [2, 1],
        "api_json_with_duplicate_members_ok": True,
        "api_json_warning": ["ExperimentalFeatureWarning"],
        "query_scope_is_a_package_name": True,
    },
    "engines": {
        "engines": {
            "check": [True, ["holds", "outcomes", "sensitive"]],
            "explore": [True, ["outcomes"]],
            "run": [True, ["evaluate"]],
            "smt": [True, ["holds", "sensitive"]],
            "solve": [True, ["holds", "satisfiable"]],
            "sweep": [True, ["sweep"]],
            "tool:fmi": [False, ["compute"]],
        },
        "readiness_without_solver_on_path": "{'check': True, 'explore': True, 'run': True, "
        "'smt': False, 'solve': False, 'sweep': True, "
        "'tool:fmi': False}",
        "fmi_reason": "OPENSYSML_FMI_RUNNER is not set: the fmi",
    },
    "toolkit": {
        "prebuilt_binary_targets": [
            "aarch64-apple-darwin",
            "aarch64-unknown-linux-gnu",
            "aarch64-unknown-linux-musl",
            "x86_64-apple-darwin",
            "x86_64-pc-windows-msvc",
            "x86_64-unknown-linux-gnu",
            "x86_64-unknown-linux-musl",
        ],
        "checksum_asset": True,
        "every_asset_has_published_sha256": True,
        "on_pypi": False,
        "source_build_route": "cargo build --release -p sysmlv2-cli (toolchain from "
        "rust-toolchain.toml)",
        "needs_standard_library_directory": True,
        "solver": "z3 subprocess",
    },
}


# -- helpers --------------------------------------------------------------------------------------
_CONN = None


def connection():
    """One client connection per process."""
    global _CONN
    if _CONN is None:
        _CONN = opensysml.connect()
    return _CONN


def platform_tag() -> str:
    return f"{sys.platform}-{platform.machine()}"


def stamp() -> str:
    version = connection().server_info().version.lstrip("v")
    return f"observed at opensysml {version} / toolkit {TOOLKIT_VERSION} on {platform_tag()}"


def frozen_source() -> str:
    return MODEL_PATH.read_text(encoding="utf-8")


def frozen_body() -> str:
    """The frozen model without its closing brace, so a probe can append members to its package."""
    text = frozen_source().rstrip()
    assert text.endswith("}")
    return text[:-1]


def diag_lines(model) -> list[str]:
    return [str(d) for d in model.diagnostics]


def errors_of(model) -> list[str]:
    return [d for d in diag_lines(model) if ": error:" in d]


def number(model, expression: str, unit: str | None = None, subject: str | None = None) -> float:
    """A model value as a float, converted to ``unit`` (a unit expression) when it is a quantity."""
    out = model.eval(expression, subject=subject) if subject else model.eval(expression)
    if isinstance(out, list):
        out = out[0]
    if hasattr(out, "in_unit"):
        return float(out.in_unit(model.eval(f"1.0 [{unit}]").unit))
    return float(out)


def lit(x: float) -> str:
    return f"{float(x):.12g}"


def verdict_row(v) -> dict:
    return {
        "holds": v.holds,
        "status": v.status,
        "strength": v.strength,
        "engine": v.engine,
        "error": str(v.error)[:140] if v.error else "",
        "witness": {w.feature.split("::")[-1]: w.value for w in (v.witness or [])},
    }


def ask(model, kind: str, fqn: str, **kwargs) -> dict:
    fn = model.verify_constraint if kind == "constraint" else model.verify_requirement
    return verdict_row(fn(fqn, **kwargs))


def finish(name: str, facts: dict, observation: str, evidence: dict | None = None) -> dict:
    return {
        "name": name,
        "ok": facts == EXPECTED.get(name),
        "observation": f"{stamp()}: {observation}",
        "evidence": {"facts": facts, **(evidence or {})},
    }


# -- 1. cross-source import -----------------------------------------------------------------------
_PKG_A = "package A { private import ScalarValues::*; part def P { attribute m : Real = 2.0; } }"
_PKG_B = "package B { private import ScalarValues::*; private import A::*; part q : P; }"


def probe_cross_source_import() -> dict:
    conn = connection()
    alone = conn.load_from_content(_PKG_B)
    bare = conn.load_from_content("package C { import ScalarValues::*; }")
    with tempfile.TemporaryDirectory() as tmp:
        a, b = pathlib.Path(tmp, "a.sysml"), pathlib.Path(tmp, "b.sysml")
        a.write_text(_PKG_A, encoding="utf-8")
        b.write_text(_PKG_B, encoding="utf-8")
        by_path_alone = conn.load(str(b))
        joined = conn.parse_sources([str(a), str(b)], strict=True)
        reverse = conn.parse_sources([("b", _PKG_B), ("a", _PKG_A)], strict=True)
    concat = conn.load_from_content(_PKG_A + "\n" + _PKG_B, strict=True)
    facts = {
        "single_source_unresolved": not alone.ok
        and any("unresolved reference: A" in d for d in diag_lines(alone)),
        "load_of_one_file_unresolved": not by_path_alone.ok,
        "parse_sources_resolves": joined.ok and number(joined, "m", subject="B::q") == 2.0,
        "parse_sources_order_free": reverse.ok,
        "concatenation_resolves": concat.ok,
        "bare_import_is_error": not bare.ok
        and any("without a visibility indicator" in d for d in diag_lines(bare)),
    }
    return finish(
        "cross_source_import",
        facts,
        "an import across separately loaded sources resolves only through parse_sources "
        "(paths or named inline documents, any order); load and load_from_content see one source; "
        "concatenation still works; every import needs an explicit visibility.",
        {"documents": list(joined.documents)[-2:]},
    )


# -- 2. a false assert satisfy ---------------------------------------------------------------------
_SATISFY_BASE = """package S { private import ScalarValues::*;
 part def V { attribute mass : Real = 5.0; }
 requirement def Light { subject v : V; require constraint { v.mass < 3.0 } }
 requirement def Heavy { subject v : V; require constraint { v.mass > 3.0 } }
 part car : V;
 requirement light : Light;
 requirement heavy : Heavy;
"""


def probe_false_assert_satisfy() -> dict:
    conn = connection()
    text = _SATISFY_BASE + " assert satisfy light by car;\n assert satisfy heavy by car;\n}"
    loose = conn.load_from_content(text)
    strict = conn.load_from_content(text, strict=True)
    verdicts = loose.verify_satisfaction()
    facts = {
        "loads_ok": loose.ok,
        "strict_load_accepts": strict.ok,
        "diagnostics": len(loose.diagnostics),
        "verdict_holds": [v.holds for v in verdicts],
        "satisfied": loose.satisfied(),
        "false_verdict_strength": verdicts[0].strength,
    }
    return finish(
        "false_assert_satisfy",
        facts,
        "a false assert satisfy loads with no diagnostic, also under strict=True; only "
        "verify_satisfaction (holds False, strength witnessed) and satisfied() (False) show it.",
    )


# -- 3. satisfy target kinds ------------------------------------------------------------------------
def probe_satisfy_target_kinds() -> dict:
    conn = connection()
    facts = {}
    for label, line in {
        "requirement_def": "satisfy Light by car;",
        "requirement_usage": "satisfy light by car;",
        "part_usage": "satisfy car by car;",
        "inline_requirement_usage": "satisfy requirement own : Light by car;",
    }.items():
        m = conn.load_from_content(_SATISFY_BASE + " " + line + "\n}")
        facts[label] = m.ok
    m = conn.load_from_content(_SATISFY_BASE + "}")
    v = m.verify_requirement("S::Light", subject="S::car")
    facts["verify_requirement_accepts_def_with_subject"] = v.status == "violated"
    return finish(
        "satisfy_target_kinds",
        facts,
        "satisfy accepts a requirement usage (named, or declared inline) and refuses a requirement "
        "definition and a part usage as target ('satisfy target must be a requirement usage'); "
        "verify_requirement takes a requirement definition with a subject.",
    )


# -- 4. verify_requirement and verify_satisfaction on the cubesat ------------------------------------
_CUBESAT_REQS = """
 requirement def MassBudget {
   subject c : Cubesat;
   attribute limit : MassValue default = 20.0 [kg];
   require constraint { c.totalMass <= limit }
 }
 requirement def MassBudgetArg {
   subject c : Cubesat;
   in limit : MassValue;
   require constraint { c.totalMass <= limit }
 }
 requirement budgetOk : MassBudget;
 requirement budgetTight : MassBudget { attribute :>> limit = 5.0 [kg]; }
 satisfy budgetOk by cubesatBaseline;
 assert satisfy budgetTight by cubesatBaseline;
 part heavySat : Cubesat {
   :>> panelSpan default = 1.0 [SI::m];
   :>> batteryCapacity default = 200.0 [SI::W*SI::h];
   part :>> wheel : LargeWheel;
   part :>> tracker : FineTracker;
 }
}"""


def probe_verify_requirement_satisfaction() -> dict:
    conn = connection()
    m = conn.load_from_content(frozen_body() + _CUBESAT_REQS, strict=True)
    base = PKG + "cubesatBaseline"
    heavy = PKG + "heavySat"
    sat = m.verify_satisfaction()
    ok_req = ask(m, "requirement", PKG + "budgetOk", subject=base)
    tight = ask(m, "requirement", PKG + "budgetTight", subject=base)
    kg = lambda x: m.eval(f"{x} [SI::kg]")  # noqa: E731
    by_arg = {
        f"{lim}kg_{label}": ask(
            m,
            "requirement",
            PKG + "MassBudgetArg",
            subject=subj,
            named_arguments={"limit": kg(lim)},
        )["holds"]
        for lim in (20.0, 5.0)
        for label, subj in (("baseline", base), ("heavy", heavy))
    }
    plain = ask(
        m,
        "requirement",
        PKG + "MassBudgetArg",
        subject=base,
        named_arguments={"limit": 20.0},
    )
    usage = [
        ask(
            m,
            "constraint",
            PKG + "Cubesat::dodOk",
            subject=base,
            named_arguments={"slewEnergy": m.eval(f"{e} [SI::W*SI::h]")},
        )["holds"]
        for e in (0.5, 50.0)
    ]
    power = ask(m, "constraint", PKG + "Cubesat::powerOk", subject=base)
    facts = {
        "baseline_mass_kg": round(number(m, "totalMass", "SI::kg", subject=base), 4),
        "satisfaction_verdicts": [v.holds for v in sat],
        "budget_ok": [ok_req["holds"], ok_req["strength"], ok_req["engine"]],
        "negative_control": [tight["holds"], tight["status"], tight["strength"]],
        "quantity_argument_by_limit_and_subject": by_arg,
        "real_argument_for_quantity_parameter": [
            plain["status"],
            "type mismatch" in plain["error"],
        ],
        "per_configuration_dod_constraint": usage,
        "per_configuration_power_constraint": power["holds"],
    }
    return finish(
        "verify_requirement_satisfaction",
        facts,
        "on the frozen baseline (13.2914 kg) a 20 kg mass-budget requirement holds (engine run, "
        "strength observed) and a 5 kg control is violated (witnessed); verify_satisfaction returns one "
        "verdict per satisfy and assert satisfy; an in-parameter takes a Quantity from eval, a plain "
        "number is refused as a type mismatch; the model's own constraint usages evaluate per "
        "configuration (slew energy 0.5 Wh passes, 50 Wh fails).",
        {"satisfaction": [(v.kind, v.holds) for v in sat]},
    )


# -- 5. holds on smt/solve, and exclusion before simulation -----------------------------------------
def solver_present() -> bool:
    try:
        from .exclusion import solver_available
    except ImportError:  # run as a script, outside the package
        return shutil.which("z3") is not None or shutil.which("cvc5") is not None
    return solver_available()


def classify(model, stem: str) -> dict:
    """Classify a region by two constraints ``<stem>Sat`` (conjunction) and ``<stem>Holds`` (implication)."""
    sat = ask(model, "constraint", PKG + stem + "Sat", engine="solve", question="satisfiable")
    holds = ask(model, "constraint", PKG + stem + "Holds", engine="solve", question="holds")
    if sat["status"] == "unsatisfiable" and sat["strength"] == "proved":
        verdict = "exclude"
    elif holds["status"] == "holds" and holds["strength"] == "proved":
        verdict = "all_feasible"
    elif sat["status"] == "satisfiable" and holds["status"] == "violated":
        verdict = "mixed"
    else:
        verdict = "undecided"
    return {
        "verdict": verdict,
        "satisfiable": [sat["status"], sat["strength"]],
        "holds": [holds["status"], holds["strength"]],
        "witness_of_violation": holds["witness"],
    }


def region_pair(stem: str, params: str, assume: str, require: str) -> str:
    """Two constraint definitions: the conjunction (satisfiable?) and the implication (holds?)."""
    return (
        f" constraint def {stem}Sat {{ {params} ({assume}) and ({require}) }}\n"
        f" constraint def {stem}Holds {{ {params} ({assume}) implies ({require}) }}\n"
    )


def accounting_body(source: str, calc: str) -> str:
    """The returned expression of a calc def in the frozen source, with ``wheelCount`` as 3.0."""
    m = re.search(rf"calc def {calc} \{{.*?return : \w+ = (.*?);\s*\}}", source, re.S)
    assert m, calc
    return " ".join(m.group(1).split()).replace("c.wheelCount", "3.0")


def probe_holds_and_exclusion() -> dict:
    conn = connection()
    src = frozen_source()
    # claims restated over scalars: the model's own accounting bodies, extracted from its text
    mass_total = accounting_body(src, "MassAccounting")
    mass_struct = accounting_body(src, "StructureMass")
    base_text = frozen_body()
    probe_defs = """
 constraint def ProbeCalcClaim { in c : Cubesat; MassAccounting(c) > 0.0 [kg] }
 constraint def ProbeScalarSmt { in x : LengthValue; in y : LengthValue; (x <= y) implies (2.0 * x <= 2.0 * y) }
 constraint def ProbeScalarFalse { in x : LengthValue; in y : LengthValue; (x <= y) implies (2.0 * x >= 2.0 * y + 1.0 [SI::m]) }
 part probeSmallWheel : SmallWheel;
 part probeLargeWheel : LargeWheel;
 part probeCoarse : CoarseTracker;
 part probeFine : FineTracker;
 part probePanel : SolarPanel;
"""
    seed = conn.load_from_content(base_text + probe_defs + "}", strict=True)
    n_wheels = number(seed, "wheelCount", subject=PKG + "cubesatBaseline")
    hk = number(seed, PKG + "environment.housekeepingLoad", "SI::W")
    idle = number(seed, PKG + "environment.wheelIdlePower", "SI::W")
    eclipse_h = number(seed, PKG + "environment.eclipseDuration", "SI::h")
    dod = number(seed, PKG + "environment.maxDepthOfDischarge")
    p_lo = number(seed, "power", "SI::W", subject=PKG + "probeCoarse")
    p_hi = number(seed, "power", "SI::W", subject=PKG + "probeFine")
    flux = number(seed, PKG + "environment.solarFlux", "SI::W/SI::m**2")
    eff = 1.0
    for k in ("cellEfficiency", "packingFactor", "degradation", "incidenceFactor"):
        eff *= number(seed, PKG + "environment." + k)
    chord = number(seed, "chord", "SI::m", subject=PKG + "probePanel")
    span_lo = number(seed, PKG + "designSpace.panelSpanMin", "SI::m")
    span_hi = number(seed, PKG + "designSpace.panelSpanMax", "SI::m")
    cap_lo = number(seed, PKG + "designSpace.batteryCapacityMin", "SI::W*SI::h")
    cap_hi = number(seed, PKG + "designSpace.batteryCapacityMax", "SI::W*SI::h")
    tau_s = number(seed, "maxTorque", "SI::N*SI::m", subject=PKG + "probeSmallWheel")
    h_s = number(seed, "maxMomentum", "SI::N*SI::m*SI::s", subject=PKG + "probeSmallWheel")
    tau_l = number(seed, "maxTorque", "SI::N*SI::m", subject=PKG + "probeLargeWheel")
    h_l = number(seed, "maxMomentum", "SI::N*SI::m*SI::s", subject=PKG + "probeLargeWheel")
    theta = 30.0 * 3.141592653589793 / 180.0  # the 30 degree slew of cubesat_model.SLEW_DEG
    gen_per_m = flux * eff * 2.0 * chord  # generated power per metre of panel span, W/m

    wh = "[SI::W*SI::h]"
    defs = ""
    # accounting identity over the model's own bodies (free scalar features of the subject)
    defs += (
        " constraint def ProbeMassIdentity { in c : Cubesat; "
        f"({mass_total}) - ({mass_struct}) == c.panelPlus.mass + c.panelMinus.mass + c.antenna.mass }}\n"
    )
    defs += (
        " constraint def ProbeMassIdentityFalse { in c : Cubesat; "
        f"({mass_total}) - ({mass_struct}) == c.panelPlus.mass + c.antenna.mass }}\n"
    )
    # monotonicity of generated power in panel span (constants read from the model, as literals)
    gen = lambda s: f"{lit(gen_per_m)} [SI::W/SI::m] * {s}"  # noqa: E731
    defs += (
        " constraint def ProbePowerMonotone { in s1 : LengthValue; in s2 : LengthValue; "
        f"(s1 <= s2) implies ({gen('s1')} <= {gen('s2')}) }}\n"
    )
    defs += (
        " constraint def ProbePowerMonotoneFalse { in s1 : LengthValue; in s2 : LengthValue; "
        f"(s1 <= s2) implies ({gen('s1')} > {gen('s2')}) }}\n"
    )
    # range-bounded claims over the model's own span range
    in_span = f"s >= {lit(span_lo)} [SI::m] and s <= {lit(span_hi)} [SI::m]"
    defs += (
        " constraint def ProbeRangeBounded { in s : LengthValue; "
        f"({in_span}) implies ({gen('s')} <= {lit(gen_per_m * span_hi)} [SI::W]) }}\n"
    )
    defs += (
        " constraint def ProbeRangeBoundedFalse { in s : LengthValue; "
        f"({in_span}) implies ({gen('s')} < {lit(gen_per_m * span_hi)} [SI::W]) }}\n"
    )
    tr = f"t >= {lit(p_lo)} [SI::W] and t <= {lit(p_hi)} [SI::W]"
    defs += (
        " constraint def ProbePowerOkEverywhere { in s : LengthValue; in t : PowerValue; "
        f"({in_span} and {tr}) implies ({gen('s')} - {lit(hk)} [SI::W] - t > 0.0 [SI::W]) }}\n"
    )
    # infeasible regions: battery too small for the eclipse base load (any slew energy >= 0)
    base_load = f"({lit(hk)} [SI::W] + t + {lit(n_wheels * idle)} [SI::W])"
    dod_ok = f"{base_load} * {lit(eclipse_h)} [SI::h] <= {lit(dod)} * cap"
    for stem, lo, hi in (
        ("ProbeBatteryTooSmall", cap_lo, 26.0),
        ("ProbeBatteryLarge", 29.0, cap_hi),
        ("ProbeBatteryFull", cap_lo, cap_hi),
    ):
        assume = (
            f"cap >= {lit(lo)} {wh} and cap <= {lit(hi)} {wh} and t >= {lit(p_lo)} [SI::W] "
            f"and t <= {lit(p_hi)} [SI::W]"
        )
        defs += region_pair(stem, "in cap : EnergyValue; in t : PowerValue;", assume, dod_ok)
    # infeasible regions: a wheel whose momentum store cannot hold a bang-bang slew (tau*theta*I <= h^2)
    for stem, tau, h, lo, hi in (
        ("ProbeSmallWheelLowInertia", tau_s, h_s, 0.18, 0.60),
        ("ProbeSmallWheelHighInertia", tau_s, h_s, 0.70, 0.90),
        ("ProbeSmallWheelFullInertia", tau_s, h_s, 0.18, 0.90),
        ("ProbeLargeWheelFullInertia", tau_l, h_l, 0.18, 0.90),
    ):
        assume = (
            f"inertia >= {lit(lo)} [SI::kg*SI::m**2] and inertia <= {lit(hi)} [SI::kg*SI::m**2]"
        )
        require = f"{lit(tau)} [SI::N*SI::m] * {lit(theta)} * inertia <= {lit(h)} [SI::N*SI::m*SI::s] * {lit(h)} [SI::N*SI::m*SI::s]"
        defs += region_pair(stem, "in inertia : MomentOfInertiaValue;", assume, require)

    m = conn.load_from_content(base_text + probe_defs + defs + "}")
    load_errors = errors_of(m)

    present = solver_present()
    engines = {}
    for eng in ("smt", "solve", "check", "auto", "all"):
        engines[eng] = {
            "calc_invocation": ask(
                m, "constraint", PKG + "ProbeCalcClaim", engine=eng, question="holds"
            ),
            "scalar_true": ask(
                m, "constraint", PKG + "ProbeScalarSmt", engine=eng, question="holds"
            ),
        }
    solved = {
        name: ask(m, "constraint", PKG + name, engine="solve", question="holds")
        for name in (
            "ProbeMassIdentity",
            "ProbeMassIdentityFalse",
            "ProbePowerMonotone",
            "ProbePowerMonotoneFalse",
            "ProbeRangeBounded",
            "ProbeRangeBoundedFalse",
            "ProbePowerOkEverywhere",
            "ProbeScalarFalse",
        )
    }
    regions = {
        stem: classify(m, stem)
        for stem in (
            "ProbeBatteryTooSmall",
            "ProbeBatteryLarge",
            "ProbeBatteryFull",
            "ProbeSmallWheelLowInertia",
            "ProbeSmallWheelHighInertia",
            "ProbeSmallWheelFullInertia",
            "ProbeLargeWheelFullInertia",
        )
    }
    # arithmetic cross-check of the thresholds the solver found
    cap_min_lo = (hk + n_wheels * idle + p_lo) * eclipse_h / dod
    cap_min_hi = (hk + n_wheels * idle + p_hi) * eclipse_h / dod
    inertia_limit_small = h_s * h_s / (tau_s * theta)

    def cell(r):
        return [r["status"], r["strength"]]

    facts = {
        "solver_on_path": present,
        "model_with_probes_loads": not load_errors,
        "calc_invocation_claim_by_engine": {
            e: cell(v["calc_invocation"]) for e, v in engines.items()
        },
        "calc_invocation_reason": "not translatable"
        in engines["solve"]["calc_invocation"]["error"],
        "scalar_claim_by_engine": {e: cell(v["scalar_true"]) for e, v in engines.items()},
        "smt_reason": engines["smt"]["scalar_true"]["error"][:40],
        "scalar_claims_on_solve": {k: cell(v) for k, v in solved.items()},
        "scalar_violation_witnessed": bool(solved["ProbeScalarFalse"]["witness"]),
        "regions": {k: v["verdict"] for k, v in regions.items()},
        "region_evidence": {k: [v["satisfiable"], v["holds"]] for k, v in regions.items()},
        "threshold_battery_wh": [round(cap_min_lo, 3), round(cap_min_hi, 3)],
        "threshold_small_wheel_inertia_kgm2": round(inertia_limit_small, 4),
    }
    return finish(
        "holds_and_exclusion",
        facts,
        "holds on a claim that invokes a calc def is undecided on every engine ('invocation not "
        "translatable'); the smt engine answers no constraint claim (it answers schedules); the solve "
        "engine (needs z3) proves claims restated over scalar features (strength proved, witness when "
        "violated), including range-bounded ones; a region of the design space or a model variant is "
        "excluded before simulation when the conjunction of its range and the feasibility condition is "
        "unsatisfiable (proved); the battery and slew-momentum regions classify as exclude, "
        "all_feasible and mixed.",
        {"regions": regions, "engines": engines, "claims": solved},
    )


# -- 6. run_analysis and run_sweep -------------------------------------------------------------------
_ANALYSIS = """package T { private import ScalarValues::*; private import ISQ::*; private import SI::*;
 part def Veh { attribute mass : MassValue = 1500.0 [kg]; }
 part car : Veh;
 analysis def Cost { subject v : Veh; in rate : Real; in days : Real; return total : Real = rate * days * 2.0; }
 analysis def Energy { subject v : Veh; in wh : Real; return joules : EnergyValue = wh * 1.0 [W*h]; }
 analysis def EnergyQ { subject v : Veh; in e : EnergyValue; return doubled : EnergyValue = e * 2.0; }
 calc def Add { in p : Real; in q : Real; return r : Real = p + q; }
 calc def Ten { in e : Real; return v : Real = 10.0 ** e; }
 calc def Ident { in x : Real; return y : Real = x; }
}"""


def probe_analysis_and_sweep() -> dict:
    m = connection().load_from_content(_ANALYSIS, strict=True)
    named = m.run_analysis("T::Cost", subject="T::car", named_arguments={"rate": 3.0, "days": 4.0})
    positional = m.run_analysis("T::Cost", subject="T::car", arguments=[3.0, 4.0])
    try:
        m.run_analysis("T::Cost", subject="T::car", named_arguments={"rate": 3.0})
        missing = "no error"
    except Exception as exc:
        missing = type(exc).__name__
    grid1 = m.run_sweep(
        "T::Cost", {"rate": (1.0, 3.0, 1.0)}, subject="T::car", named_arguments={"days": 2.0}
    )
    grid2 = m.run_sweep("T::Add", {"p": (1.0, 3.0, 1.0), "q": (10.0, 20.0, 10.0)})
    ranges = {"p": (1.0, 3.0), "q": (10.0, 20.0)}
    s4 = m.run_sweep("T::Add", ranges, samples=4, seed=7)
    s4b = m.run_sweep("T::Add", ranges, samples=4, seed=7)
    s6 = m.run_sweep("T::Add", ranges, samples=6, seed=7)
    s4c = m.run_sweep("T::Add", ranges, samples=4, seed=8)
    rows = lambda t: [tuple(r.inputs.items()) for r in t]  # noqa: E731
    uni = m.run_sweep("T::Ident", {"x": (1.0, 1000.0)}, samples=400, seed=3)
    low = sum(r.inputs["x"] < 10 for r in uni) / len(uni)
    logd = m.run_sweep("T::Ten", {"e": (0.0, 3.0)}, samples=400, seed=3)
    logfrac = sum(r.outputs["result"][0] < 10 for r in logd) / len(logd)
    wh = m.run_sweep("T::Energy", {"wh": (0.0, 2.0, 1.0)}, subject="T::car")
    try:
        m.run_sweep("T::EnergyQ", {"e": (0.0, 2.0, 1.0)}, subject="T::car")
        quantity_range = "accepted"
    except Exception as exc:
        quantity_range = (
            f"{type(exc).__name__}: type mismatch" if "type mismatch" in str(exc) else str(exc)[:80]
        )
    facts = {
        "named_and_positional_agree": named.outputs == positional.outputs == {"total": [24.0]},
        "run_analysis_engine": [named.engine, named.strength],
        "missing_in_parameter": missing,
        "grid_endpoints_inclusive": [r.outputs["total"][0] for r in grid1] == [4.0, 8.0, 12.0],
        "grid_product_rows_first_slowest": [(r.inputs["p"], r.inputs["q"]) for r in grid2][:3]
        == [(1.0, 10.0), (1.0, 20.0), (2.0, 10.0)]
        and len(grid2) == 6,
        "samples_flag": [s4.sampled, grid1.sampled],
        "same_seed_same_rows": rows(s4) == rows(s4b),
        "row_i_independent_of_n": rows(s6)[:4] == rows(s4),
        "other_seed_differs": rows(s4c) != rows(s4),
        "uniform_draw_fraction_below_10_in_1_to_1000_small": low < 0.05,
        "log_draw_through_exponent_fraction_below_10_near_third": 0.25 < logfrac < 0.4,
        "dimensionless_parameter_times_unit_inside_case": [
            round(float(r.outputs["joules"][0].in_unit(m.eval("1.0 [SI::W*SI::h]").unit)), 6)
            for r in wh
        ]
        == [0.0, 1.0, 2.0],
        "quantity_typed_parameter_in_range": quantity_range,
    }
    return finish(
        "analysis_and_sweep",
        facts,
        "run_analysis binds in parameters by name or position and fails on a missing one; run_sweep "
        "grids are inclusive with a step and first-range-slowest; samples+seed is reproducible, row i "
        "does not depend on n, and the draw is uniform (no log range, so a log range is drawn through an "
        "exponent parameter); a range cannot bind a quantity-typed parameter, so the case takes a "
        "dimensionless parameter and applies the unit inside.",
    )


# -- 7. record_run and run_runs ----------------------------------------------------------------------
_RUNS = """package R { private import ScalarValues::*; private import RandomFunctions::*;
 part def Veh { attribute mass : Real = 5.0; }
 part car : Veh;
 analysis def Cost { subject v : Veh; in rate : Real; in days : Real; return total : Real = rate * days * 2.0; }
 action def Draw { out x : Real; assign x := uniform(0.0, 10.0); }
}"""


def probe_record_and_runs() -> dict:
    m = connection().load_from_content(_RUNS, strict=True)
    args = {"rate": 3.0, "days": 4.0}
    one = m.record_run("R::Cost", subject="R::car", named_arguments=args)
    again = m.record_run("R::Cost", subject="R::car", named_arguments=args)
    joined = connection().parse_sources([("model", _RUNS), ("recorded", one.source)], strict=True)
    two = joined.record_run("R::Cost", subject="R::car", named_arguments={"rate": 1.0, "days": 4.0})
    swept = m.record_run(
        "R::Cost", subject="R::car", named_arguments={"days": 4.0}, ranges={"rate": (1.0, 3.0, 1.0)}
    )
    stamped = re.findall(r'runAt = "([^"]+)"', one.source)
    kinds = re.findall(r'kind = "(\w+)"', swept.source)
    r1 = m.run_runs(action="R::Draw", runs=3, seed=1)
    r1b = m.run_runs(action="R::Draw", runs=3, seed=1)
    r5 = m.run_runs(action="R::Draw", runs=5, seed=1)
    r3c = m.run_runs(action="R::Draw", runs=3, seed=2)
    xs = lambda r: [row.outputs["x"][0] for row in r.rows]  # noqa: E731
    try:
        m.run_runs(analysis="R::Cost", runs=3, seed=1, subject="R::car")
        plain_case = "accepted"
    except Exception as exc:
        plain_case = (
            "refused: needs Simulation::MonteCarlo" if "MonteCarlo" in str(exc) else str(exc)[:80]
        )
    facts = {
        "record_names": [one.records, again.records, two.records],
        "loaded_model_unchanged_by_record_run": one.records == again.records,
        "record_definition": [one.package, one.definition],
        "sweep_records": [len(swept.records), sorted(set(kinds))],
        "provenance_has_timestamp": bool(stamped),
        "provenance_tool": re.findall(r'tool = "([^"]+)"', one.source),
        "record_returns_run": one.run.outputs == {"total": [24.0]},
        "runs_reproducible": xs(r1) == xs(r1b),
        "run_i_independent_of_n": xs(r5)[:3] == xs(r1),
        "other_seed_differs": xs(r3c) != xs(r1),
        "ordinary_analysis_case_in_run_runs": plain_case,
    }
    return finish(
        "record_and_runs",
        facts,
        "record_run returns the runs as a new Records document (Records::Cost_run1; one part per sweep row) "
        "and leaves the loaded model unchanged, so numbering continues only when the recorded document "
        "is loaded with the model through parse_sources (Cost_run2); each record is stamped with runAt (a wall-clock time: a ledger comparison must "
        "ignore it) and the tool version; run_runs repeats an action with modeled randomness, "
        "reproducibly per seed with run i independent of the count, and takes an analysis case only if "
        "it specializes Simulation::MonteCarlo.",
        {"recorded_source_head": one.source[:240]},
    )


# -- 8. unit labels from eval ------------------------------------------------------------------------
def probe_unit_labels() -> dict:
    m = connection().load_from_content(frozen_source(), strict=True)
    base = PKG + "cubesatBaseline"
    labels = {}
    for expr in ("totalMass", "generatedPower", "availablePower", "usableWheelTorque"):
        q = m.eval(expr, subject=base)
        q = q[0] if isinstance(q, list) else q
        labels[expr] = q.unit.text
    watt = m.eval("1.0 [SI::W]").unit
    energy = m.eval("12.0 [SI::W]*0.6 [SI::h]")
    energy = energy[0] if isinstance(energy, list) else energy
    gen = m.eval("generatedPower", subject=base)
    gen = gen[0] if isinstance(gen, list) else gen
    facts = {
        "labels": labels,
        "unsimplified_power_label": labels["generatedPower"] != "SI::W",
        "in_unit_converts": round(float(gen.in_unit(watt)), 6)
        == round(number(m, "generatedPower", "SI::W", base), 6),
        "generated_power_w": round(float(gen.in_unit(watt)), 4),
        "product_label": energy.unit.text,
        "product_in_wh": round(float(energy.in_unit(m.eval("1.0 [SI::W*SI::h]").unit)), 6),
    }
    return finish(
        "unit_labels",
        facts,
        "a value of a plain unit keeps its label (kg), a product or quotient comes back with the "
        "unsimplified base-unit label (kg*m^2*s^-3 for a power), the magnitude is right, and in_unit "
        "converts to the unit the analyst names.",
    )


# -- 9. query and to_api_json ------------------------------------------------------------------------
_QUERY = """package Q { private import ScalarValues::*;
 part def V { attribute mass : Real default = 5.0; }
 requirement def Light { subject v : V; require constraint { v.mass < 3.0 } }
 part car : V; part truck : V;
 requirement light : Light;
 satisfy light by car;
 assert satisfy light by truck;
 connection def Link { end part a : V; end part b : V; }
 connection : Link connect car to truck;
 part def Redecl { attribute x : Real = 1.0; attribute x : Real = 2.0; }
 part def Redecl2 :> V { attribute :>> mass = 7.0; attribute :>> mass = 8.0; }
}"""


def probe_query_blind_spots() -> dict:
    m = connection().load_from_content(_QUERY)
    q = m.query(scope=["Q"])
    kinds = Counter(x.type for x in q)
    unnamed = sorted(x.id for x in q if x.type in {"SatisfyRequirementUsage", "ConnectionUsage"})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        api = json.loads(m.to_api_json().content)
    api_kinds = Counter(e.get("@type") for e in api if isinstance(e, dict))
    facts = {
        "load_errors": len(errors_of(m)),
        "duplicate_member_warnings": sum("Duplicate of" in d for d in diag_lines(m)) > 0,
        "query_sees_satisfy_and_connection": [
            kinds["SatisfyRequirementUsage"],
            kinds["ConnectionUsage"],
        ],
        "unnamed_ids_use_at_numbers": all("::@" in i for i in unnamed) and len(unnamed) == 3,
        "api_json_lists_them_too": [
            api_kinds["SatisfyRequirementUsage"],
            api_kinds["ConnectionUsage"],
        ],
        "api_json_with_duplicate_members_ok": len(api) > 0,
        "api_json_warning": sorted({w.category.__name__ for w in caught}),
        "query_scope_is_a_package_name": kinds["PartDefinition"] == 3,
    }
    return finish(
        "query_blind_spots",
        facts,
        "at 0.12.1 query sees the unnamed satisfy and connection usages (ids Q::@n) and to_api_json "
        "loads and serializes a package with duplicate-name and doubly redefined members; to_api_json "
        "raises ExperimentalFeatureWarning, so the form is not a stable interface.",
        {"kinds": dict(kinds), "unnamed": unnamed},
    )


# -- 10. engine list and readiness -------------------------------------------------------------------
def probe_engines() -> dict:
    conn = connection()
    info = {e.name: (e.ready, sorted(e.answers)) for e in conn.list_engines()}
    without_solver = ""
    if solver_present():
        path = os.pathsep.join(
            d
            for d in os.environ.get("PATH", "").split(os.pathsep)
            if not (pathlib.Path(d, "z3").exists() or pathlib.Path(d, "cvc5").exists())
        )
        code = (
            "import opensysml;c=opensysml.connect();"
            "print({e.name:e.ready for e in c.list_engines()})"
        )
        out = subprocess.run(
            [sys.executable, "-c", code],
            env={**os.environ, "PATH": path},
            capture_output=True,
            text=True,
        )
        without_solver = out.stdout.strip()
    facts = {
        "engines": {k: [v[0], v[1]] for k, v in sorted(info.items())},
        "readiness_without_solver_on_path": without_solver,
        "fmi_reason": next(
            (e.unavailable for e in conn.list_engines() if e.name == "tool:fmi"), ""
        )[:40],
    }
    return finish(
        "engines",
        facts,
        "list_engines reports check, explore, run, smt, solve and sweep ready and tool:fmi unavailable "
        "(OPENSYSML_FMI_RUNNER unset); smt and solve become not ready when no z3 or cvc5 is on PATH, so "
        "a solving step needs the solver installed and a test that needs it fails by name.",
    )


# -- 11. the model-checking toolkit ------------------------------------------------------------------
_TOOLKIT_SNIPPET = """package Tank {
    private import ScalarValues::*;
    attribute capacity : Real[1];
    attribute demand : Real[1] = 13.3 * 0.6;
    assert constraint inRange { capacity >= 20.0 & capacity <= 25.0 }
    assert constraint feasible { demand <= 0.3 * capacity }
}
"""


def gh_release_assets() -> dict[str, tuple[int, str]]:
    out = subprocess.run(
        ["gh", "release", "view", TOOLKIT_VERSION, "--repo", TOOLKIT_REPO, "--json", "assets"],
        capture_output=True,
        text=True,
        check=True,
    )
    return {
        a["name"]: (a["size"], a["digest"].removeprefix("sha256:"))
        for a in json.loads(out.stdout)["assets"]
    }


def toolkit_local() -> dict:
    """Run check, lint and verify --solve with a locally built or installed binary, if there is one."""
    binary = os.environ.get("SYSMLV2_BIN") or shutil.which("sysmlv2")
    if not binary:
        return {"binary": "not obtained"}
    lib = os.environ.get("SYSMLV2_LIB")
    extra = ["--lib", lib] if lib else []
    with tempfile.TemporaryDirectory() as tmp:
        snippet = pathlib.Path(tmp, "tank.sysml")
        snippet.write_text(_TOOLKIT_SNIPPET, encoding="utf-8")
        frozen = str(MODEL_PATH)
        env = {**os.environ, "SYSMLV2_CACHE_DIR": tmp}

        def run(*args):
            return subprocess.run([binary, *args, *extra], capture_output=True, text=True, env=env)

        version = subprocess.run(
            [binary, "--version"], capture_output=True, text=True
        ).stdout.strip()
        check = run("check", str(snippet))
        lint = run("lint", "--format", "json", frozen)
        solve = run("verify", str(snippet), "--solve")
        frozen_solve = run("verify", frozen, "--solve")
    return {
        "binary": binary,
        "version": version,
        "check_exit": check.returncode,
        "lint_summary": json.loads(lint.stdout)["summary"] if lint.stdout.strip() else None,
        "verify_solve_exit": solve.returncode,
        "verify_solve": solve.stdout.strip().splitlines(),
        "verify_frozen_model": frozen_solve.stdout.strip().splitlines()[-3:],
    }


def probe_toolkit(network: bool = False) -> dict:
    triples = sorted(
        n.split("0.12.0-")[1].split(".")[0] for n in RELEASE_ASSETS if n.startswith("sysmlv2-")
    )
    facts = {
        "prebuilt_binary_targets": triples,
        "checksum_asset": "SHA256SUMS" in RELEASE_ASSETS,
        "every_asset_has_published_sha256": all(len(h) == 64 for _, h in RELEASE_ASSETS.values()),
        "on_pypi": False,
        "source_build_route": "cargo build --release -p sysmlv2-cli (toolchain from rust-toolchain.toml)",
        "needs_standard_library_directory": True,
        "solver": "z3 subprocess",
    }
    evidence: dict = {"assets": RELEASE_ASSETS, "local": toolkit_local()}
    live_matches = True
    if network:
        live = gh_release_assets()
        live_matches = live == RELEASE_ASSETS
        evidence["live"] = live
    result = finish(
        "toolkit",
        facts,
        "v0.12.0 publishes prebuilt archives for seven targets (aarch64 and x86_64 apple-darwin, "
        "linux gnu and musl for both, x86_64 windows) with a SHA256SUMS asset and a sha256 digest on every asset; "
        "it is not on PyPI; check, lint --format json and verify --solve run from a source build in "
        "about a minute, need a standard-library directory (--lib) and z3 on PATH, and read "
        "usage-level assert constraints (see the record).",
        evidence,
    )
    result["ok"] = result["ok"] and live_matches
    return result


PROBES = [
    probe_cross_source_import,
    probe_false_assert_satisfy,
    probe_satisfy_target_kinds,
    probe_verify_requirement_satisfaction,
    probe_holds_and_exclusion,
    probe_analysis_and_sweep,
    probe_record_and_runs,
    probe_unit_labels,
    probe_query_blind_spots,
    probe_engines,
    probe_toolkit,
]


def run_all(network: bool = False) -> list[dict]:
    """Run the eleven probes against the live runtime; each result has ``name``, ``ok``,
    ``observation`` and ``evidence``."""
    results = []
    for fn in PROBES:
        try:
            results.append(fn(network) if fn is probe_toolkit else fn())
        except Exception as exc:  # a probe that cannot run is a result, not a crash
            name = fn.__name__.removeprefix("probe_")
            results.append(
                {
                    "name": name,
                    "ok": False,
                    "observation": f"probe failed: {type(exc).__name__}: {str(exc)[:300]}",
                    "evidence": {"facts": {}},
                }
            )
    return results


def mismatches(results: list[dict]) -> list[str]:
    """Names of the probes whose observed facts differ from the recorded ones."""
    return [r["name"] for r in results if not r["ok"]]


def generated_table(results: list[dict]) -> str:
    rows = ["| probe | recorded result holds | observation |", "|---|---|---|"]
    for r in results:
        rows.append(f"| `{r['name']}` | {'yes' if r['ok'] else 'NO'} | {r['observation']} |")
    return "\n".join(rows)


def write_record(results: list[dict]) -> None:
    text = RECORD_PATH.read_text(encoding="utf-8")
    block = f"{BEGIN}\n{generated_table(results)}\n{END}"
    new = re.sub(re.escape(BEGIN) + ".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    RECORD_PATH.write_text(new, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--write", action="store_true", help="rewrite the generated table of probes/probe-record.md"
    )
    parser.add_argument(
        "--network", action="store_true", help="compare probe 11 with the published release"
    )
    parser.add_argument(
        "--facts", action="store_true", help="print each probe's observed facts as JSON"
    )
    args = parser.parse_args(argv)
    results = run_all(network=args.network)
    for r in results:
        print(f"{'ok ' if r['ok'] else 'NO '} {r['name']}: {r['observation']}")
        if args.facts:
            print(json.dumps(r["evidence"]["facts"], indent=1, sort_keys=True, default=str))
    bad = mismatches(results)
    if args.write:
        write_record(results)
    print("changed vs recorded:", bad or "none")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
