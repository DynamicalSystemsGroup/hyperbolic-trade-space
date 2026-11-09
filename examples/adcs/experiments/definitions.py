"""Declared experiments: the five frozen datasets (adopted) and the cubesat ``v2`` generation.

Definitions only. Oracles and samplers are named here and resolved lazily by ``resolve_oracle``
and ``resolve_sampler``, so importing this module needs no runtime. Part 15.4 runs the ``v2``
experiments; it writes ``experiments/cubesat_oracle.py`` with a ``build(experiment)`` factory
returning the oracle and a ``build_sampler(experiment)`` factory returning the sampler.
"""

from __future__ import annotations

import importlib
from collections.abc import Callable

from .experiment import AdoptedSpec, Experiment

ADCS = "examples/adcs"
V2_DIR = f"{ADCS}/data/v2"
V2_MODEL = f"{ADCS}/model_v2/cubesat.sysml"
V2_CODE = (f"{ADCS}/experiments/cubesat_oracle.py", f"{ADCS}/adcs_sim.py")

# Oracle and sampler names -> "module:factory"; a factory takes the (sweep-cell) Experiment.
ORACLES: dict[str, str] = {"cubesat-v2": "experiments.cubesat_oracle:build"}
SAMPLERS: dict[str, str] = {"cubesat-v2": "experiments.cubesat_oracle:build_sampler"}


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


def _v2(id_, file, count, gain_box, parents=(), oracle="cubesat-v2", sampler="cubesat-v2"):
    return Experiment(
        id=id_,
        output=f"{V2_DIR}/{file}",
        count=count,
        seed=0,
        oracle=oracle,
        sampler=sampler,
        scenario="slew30deg-600s-0p5s",
        gain_box=gain_box,
        model_path=V2_MODEL,
        evidence_kind="simulation",
        code=V2_CODE,
        parents=parents,
    )


# Order is the ledger order: predictions precede the check-design simulation, both follow primary.
V2: tuple[Experiment, ...] = (
    _v2("v2-primary", "adcs_designs_cubesat_gains.csv", 1000, "aggressive"),
    _v2("v2-baseline", "adcs_designs_cubesat.csv", 1000, "baseline"),
    _v2(
        "v2-check-predictions",
        "check_predictions_cubesat.csv",
        3,
        "aggressive",
        parents=("v2-primary",),
        oracle="cubesat-v2",
        sampler="cubesat-v2",
    ),
    _v2(
        "v2-check-designs",
        "check_designs_cubesat.csv",
        6,
        "aggressive",
        parents=("v2-check-predictions",),
    ),
)
EXPERIMENTS: dict[str, Experiment] = {e.id: e for e in V2}

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
        command="uv run python examples/adcs/generate_dataset.py --n 1000 --seed 0 --workers 8 --force",
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
            "exact": ["design_id", "seed", "wheel_class", "st_grade", "settled", "momentum_ok",
                      "power_ok", "dod_ok"],  # fmt: skip
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
            "exact": ["design_id", "seed", "wheel_class", "st_grade", "settled", "momentum_ok",
                      "power_ok", "dod_ok"],  # fmt: skip
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
        command=(
            "REQUIRE_OPENSYSML=1 uv run python examples/adcs/make_check_designs.py predict"
        ),
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
        command=(
            "REQUIRE_OPENSYSML=1 uv run python examples/adcs/make_check_designs.py simulate"
        ),
        model_path=_TRADESPACE,
        code=(f"{ADCS}/make_check_designs.py", *_CUBESAT[1:]),
        tolerances={
            "test": "tests/test_check_designs.py (rows, roles, columns, box; no regeneration test)",
            "regeneration": "none; simulated once after the predictions were committed",
        },
        parents=("adopted-check_predictions_cubesat",),
    ),
)
