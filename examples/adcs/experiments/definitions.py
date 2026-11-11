"""Declared experiments: the five frozen datasets (adopted) and the cubesat ``v2`` generation.

Definitions only. Oracles and samplers are named here and resolved lazily by ``resolve_oracle``
and ``resolve_sampler``, so importing this module needs no runtime. Part 15.4 runs the ``v2``
experiments: ``experiments/cubesat_oracle.py`` has the ``build(experiment)`` and
``build_sampler(experiment)`` factories; ``experiments/check_designs.py`` has those of the
check-design flow.

The model the ``v2`` experiments read is ``V2_MODEL``, the adopted ``model_v2/cubesat.sysml``;
the environment variable ``EXPERIMENTS_MODEL`` (a path relative to the repository root) points a
run at another file, such as a round's revision beside it (WP23's loop), with no edit here.
The ledger entry records the path and hash of whichever model was read.
"""

from __future__ import annotations

import dataclasses
import importlib
import os
from collections.abc import Callable

from .experiment import AdoptedSpec, Experiment

ADCS = "examples/adcs"
V2_DIR = f"{ADCS}/data/v2"
V2_MODEL = os.environ.get("EXPERIMENTS_MODEL") or f"{ADCS}/model_v2/cubesat.sysml"
V2_CODE = (
    f"{ADCS}/experiments/cubesat_oracle.py",
    f"{ADCS}/experiments/feasibility.py",
    f"{ADCS}/adcs_sim.py",
)
V2_CHECK_CODE = (*V2_CODE, f"{ADCS}/experiments/check_designs.py")
V2_SCENARIO = "nominalSlew"  # the model's scenario part (slew 30 degrees, 600 s, 0.5 s step)
CHECK_SEED = 20261108  # the seed of the pool and of the check designs (make_check_designs.SEED)
# Designs per regime of the two main datasets (WP30, "Sampling"): the paper assumes nothing about
# how the designs were drawn, so the sample is a design choice of the case. Design i depends only on
# (seed, i), so the first 1000 designs are the earlier sample. The count is the largest round number
# for which the whole regeneration fits the hour at three workers: the oracle took 203 s per 1000
# designs (work-packages/WP30-build-notes.md, "Sampling"), and the regeneration is the two datasets
# plus the sensitivity record's five regenerations of both, 12 x N designs.
SAMPLE_PER_REGIME = 2000

# Oracle and sampler names -> "module:factory"; a factory takes the (sweep-cell) Experiment.
ORACLES: dict[str, str] = {
    "cubesat-v2": "experiments.cubesat_oracle:build",
    "check-passthrough": "experiments.check_designs:build_passthrough",
    "check-cubesat-v2": "experiments.check_designs:build_check_oracle",
    "legacy-geostationary": "experiments.legacy_oracle:build",
}
SAMPLERS: dict[str, str] = {
    "cubesat-v2": "experiments.cubesat_oracle:build_sampler",
    "check-proposer": "experiments.check_designs:build_proposer",
    "check-designs": "experiments.check_designs:build_checks",
    "shared-subspace": "experiments.legacy_oracle:build_shared_sampler",
}


def _resolve(registry: dict[str, str], name: str) -> Callable:
    try:
        target = registry[name]
    except KeyError:
        raise KeyError(f"unknown name {name!r}; known: {sorted(registry)}") from None
    module, attr = target.split(":")
    return getattr(importlib.import_module(module), attr)


def resolve_oracle(name: str) -> Callable:
    """The oracle factory registered under ``name`` (imports its module on demand)."""
    return _resolve(ORACLES, name)


def resolve_sampler(name: str) -> Callable:
    """The sampler factory registered under ``name`` (imports its module on demand)."""
    return _resolve(SAMPLERS, name)


def _v2(
    id_,
    file,
    count,
    gain_box,
    parents=(),
    oracle="cubesat-v2",
    sampler="cubesat-v2",
    seed=0,
    code=V2_CODE,
    inputs=None,
):
    return Experiment(
        id=id_,
        output=f"{V2_DIR}/{file}",
        count=count,
        seed=seed,
        oracle=oracle,
        sampler=sampler,
        scenario=V2_SCENARIO,
        gain_box=gain_box,
        model_path=V2_MODEL,
        evidence_kind="simulation",
        code=code,
        parents=parents,
        inputs=dict(inputs or {}),
    )


# The three hand-written candidates of the check designs (the same as make_check_designs.CANDIDATES;
# a test ties them). They are design points, not model constants.
CANDIDATES = (
    dict(name="fast_effort_hungry", wheel_class="large", st_grade="medium", panel_span_m=0.55,
         battery_wh=90.0, Kp=1.8, Kd=1.4),
    dict(name="precise_heavy_sensor", wheel_class="large", st_grade="fine", panel_span_m=0.8,
         battery_wh=140.0, Kp=1.2, Kd=1.0),
    dict(name="light_slow", wheel_class="small", st_grade="coarse", panel_span_m=0.35,
         battery_wh=40.0, Kp=0.25, Kd=0.4),
)  # fmt: skip

# Order is the ledger order: predictions precede the check-design simulation, both follow primary.
V2: tuple[Experiment, ...] = (
    _v2("v2-primary", "adcs_designs_cubesat_gains.csv", SAMPLE_PER_REGIME, "aggressive"),
    _v2("v2-baseline", "adcs_designs_cubesat.csv", SAMPLE_PER_REGIME, "baseline"),
    _v2(
        "v2-check-predictions",
        "check_predictions_cubesat.csv",
        3,
        "aggressive",
        parents=("v2-primary",),
        oracle="check-passthrough",
        sampler="check-proposer",
        seed=CHECK_SEED,
        code=V2_CHECK_CODE,
        inputs={
            "stage": "predict: fit on the feasible v2 primary designs, propose; nothing measured",
            "primary": f"{V2_DIR}/adcs_designs_cubesat_gains.csv",
            "metrics": [
                "settling_time_s",
                "pointing_error_deg",
                "control_effort",
                "total_mass_kg",
            ],
            "pool": 100000,
            "reach": 0.35,
        },
    ),
    _v2(
        "v2-check-designs",
        "check_designs_cubesat.csv",
        6,
        "aggressive",
        parents=("v2-check-predictions",),
        oracle="check-cubesat-v2",
        sampler="check-designs",
        seed=CHECK_SEED,
        code=V2_CHECK_CODE,
        inputs={
            "stage": "simulate: the candidates and the committed proposals, once each",
            "predictions": f"{V2_DIR}/check_predictions_cubesat.csv",
            "candidates": [dict(c) for c in CANDIDATES],
        },
    ),
)

# The scope-sensitivity experiment (OD1): the v2 oracle and the legacy geostationary oracle on the
# same designs of the configuration variables they share (wheel class, tracker grade, Kp; Kd is
# fixed in each, the other variables belong to one variant). The study of what the two reveal is a
# later candidate; this is the definition and a small run (20 designs).
SHARED_ID = "scope-sensitivity-shared-subspace"
SCOPE_DIR = f"{ADCS}/data/scope-sensitivity"
SHARED_SEED = 20261109
SHARED_COUNT = 20
_SHARED_COMMON = {
    "subspace": "wheel_class, st_grade, Kp (overlap of the two Kp ranges); Kd fixed per variant",
    "subspace_model": V2_MODEL,
}
SHARED_V2 = Experiment(
    id=f"{SHARED_ID}-v2",
    output=f"{SCOPE_DIR}/scope_sensitivity_v2.csv",
    count=SHARED_COUNT,
    seed=SHARED_SEED,
    oracle="cubesat-v2",
    sampler="shared-subspace",
    scenario=V2_SCENARIO,
    gain_box="aggressive",
    model_path=V2_MODEL,
    evidence_kind="simulation",
    code=(*V2_CODE, f"{ADCS}/experiments/legacy_oracle.py"),
    inputs={**_SHARED_COMMON, "variant": "v2", "group": SHARED_ID},
)
SHARED_LEGACY = Experiment(
    id=f"{SHARED_ID}-legacy",
    output=f"{SCOPE_DIR}/scope_sensitivity_legacy.csv",
    count=SHARED_COUNT,
    seed=SHARED_SEED,
    oracle="legacy-geostationary",
    sampler="shared-subspace",
    evidence_kind="simulation",
    code=(
        f"{ADCS}/adcs_sim.py",
        f"{ADCS}/design_space.py",
        f"{ADCS}/experiments/legacy_oracle.py",
    ),
    inputs={
        **_SHARED_COMMON,
        "variant": "legacy",
        "group": SHARED_ID,
        "scenario_legacy": "10 degree slew, 900 s, 0.5 s step (design_space.evaluate_design)",
        "legacy_dataset": "adopted-adcs_designs",
    },
)
# an id on the command line may name a group: its members run in this order
GROUPS: dict[str, tuple[Experiment, ...]] = {SHARED_ID: (SHARED_V2, SHARED_LEGACY)}
EXPERIMENTS: dict[str, Experiment] = {e.id: e for e in V2}
SHARED_EXPERIMENTS: dict[str, Experiment] = {e.id: e for e in GROUPS[SHARED_ID]}


def revise(exp: Experiment, entries: list[dict]) -> Experiment:
    """The declaration ``exp`` as a re-run: id ``<id>@<n>``, superseding its current entry.

    Parents are re-pointed at the current entries of the parent experiments, so a re-run chain
    (primary, predictions, check designs) records the new hashes. Raises ``KeyError`` when ``exp``
    has no current entry to supersede.
    """
    from . import ledger as lg

    old = lg.latest(entries, exp.id)
    if old is None:
        raise KeyError(f"{exp.id!r} has no current ledger entry to supersede")
    n = 2 if "@" not in old["id"] else int(old["id"].rsplit("@", 1)[1]) + 1
    parents = []
    for p in exp.parents:
        cur = lg.latest(entries, p)
        parents.append(cur["id"] if cur else p)
    return dataclasses.replace(
        exp, id=f"{exp.id}@{n}", parents=tuple(parents), supersedes=(old["id"],)
    )


_SRC = (f"{ADCS}/adcs_sim.py", f"{ADCS}/design_space.py")
_GEN = f"{ADCS}/generate_dataset.py"
_CUBESAT = (_GEN, f"{ADCS}/cubesat_model.py", *_SRC)
_TRADESPACE = f"{ADCS}/cubesat_tradespace.sysml"
_SAME_PLATFORM = "40 designs regenerated twice on one platform are identical"

# Tolerances of the reproducibility tests that cover each file (first 20 designs regenerated).
FROZEN: tuple[AdoptedSpec, ...] = (
    AdoptedSpec(
        id="adopted-adcs_designs",
        output=f"{ADCS}/data/adcs_designs.csv",
        command=(
            "uv run python examples/adcs/generate_dataset.py --n 1000 --seed 0 --workers 8 --force"
        ),
        model_path=None,
        code=(_GEN, *_SRC),
        tolerances={
            "test": "tests/test_adcs_case.py::test_dataset_reproducible_first_20",
            "exact": ["design_id", "wheel_class", "st_grade", "settled", "momentum_ok"],
            "continuous_rtol": 1e-4,
            "continuous_atol": 1e-12,
            "torque_saturated_frac_rtol": 2e-2,
            "settling_time_s_atol": 0.5,
            "same_platform": _SAME_PLATFORM,
        },
        note="the WP4 oracle (Python design space); the legacy oracle of OD1",
    ),
    AdoptedSpec(
        id="adopted-adcs_designs_cubesat",
        output=f"{ADCS}/data/adcs_designs_cubesat.csv",
        command=(
            "uv run python examples/adcs/generate_dataset.py --model cubesat --n 1000 --seed 0"
            " --slew-deg 30 --t-end 600 --force"
        ),
        model_path=_TRADESPACE,
        code=_CUBESAT,
        tolerances={
            "test": "tests/test_cubesat_model.py::test_dataset_reproducible_first_20",
            "exact": [
                "design_id",
                "seed",
                "wheel_class",
                "st_grade",
                "settled",
                "momentum_ok",
                "power_ok",
                "dod_ok",
            ],
            "continuous_rtol": 1e-4,
            "continuous_atol": 1e-6,
            "torque_saturated_frac_rtol": 2e-2,
            "time_columns_atol": 0.5,
            "time_columns": ["settling_time_s", "slew_time_s", "slew_time_05deg_s"],
            "same_platform": _SAME_PLATFORM,
        },
    ),
    AdoptedSpec(
        id="adopted-adcs_designs_cubesat_gains",
        output=f"{ADCS}/data/adcs_designs_cubesat_gains.csv",
        command=(
            "uv run python examples/adcs/generate_dataset.py --model cubesat --gain-box aggressive"
            " --n 1000 --seed 0 --slew-deg 30 --t-end 600 --force"
        ),
        model_path=_TRADESPACE,
        code=_CUBESAT,
        tolerances={
            "test": "tests/test_cubesat_model.py::test_dataset_reproducible_first_20",
            "exact": [
                "design_id",
                "seed",
                "wheel_class",
                "st_grade",
                "settled",
                "momentum_ok",
                "power_ok",
                "dod_ok",
            ],
            "continuous_rtol": 1e-3,
            "continuous_atol": 1e-6,
            "torque_saturated_frac_rtol": 1e-1,
            "time_columns_atol": 0.5,
            "time_columns": ["settling_time_s", "slew_time_s", "slew_time_05deg_s"],
            "same_platform": _SAME_PLATFORM,
        },
        note="primary regime (aggressive gain box)",
    ),
    AdoptedSpec(
        id="adopted-check_predictions_cubesat",
        output=f"{ADCS}/data/check_predictions_cubesat.csv",
        command=("REQUIRE_OPENSYSML=1 uv run python examples/adcs/make_check_designs.py predict"),
        model_path=_TRADESPACE,
        code=(f"{ADCS}/make_check_designs.py", f"{ADCS}/cubesat_model.py"),
        tolerances={
            "test": "tests/test_check_designs.py (rows, roles, columns; no regeneration test)",
            "regeneration": "none; committed once, before the simulation file exists",
        },
        parents=("adopted-adcs_designs_cubesat_gains",),
        note="fits the package at the generating commit; the package files are not hashed here",
    ),
    AdoptedSpec(
        id="adopted-check_designs_cubesat",
        output=f"{ADCS}/data/check_designs_cubesat.csv",
        command=("REQUIRE_OPENSYSML=1 uv run python examples/adcs/make_check_designs.py simulate"),
        model_path=_TRADESPACE,
        code=(f"{ADCS}/make_check_designs.py", *_CUBESAT[1:]),
        tolerances={
            "test": "tests/test_check_designs.py (rows, roles, columns, box; no regeneration test)",
            "regeneration": "none; simulated once after the predictions were committed",
        },
        parents=("adopted-check_predictions_cubesat",),
    ),
)
