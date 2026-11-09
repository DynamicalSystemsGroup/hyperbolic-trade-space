"""The legacy geostationary oracle (WP15 OD1): the frozen Python design space behind the protocol.

``LegacyGeostationaryOracle`` satisfies ``experiments.oracle.Oracle`` over the frozen
``design_space.evaluate_design`` and its simulator (``adcs_sim``). Both are read-only here: nothing
in them is edited, copied or re-derived, so the oracle returns exactly what the frozen generator
wrote to ``data/adcs_designs.csv`` for the same design. The configuration is the frozen one
(wheel class, star-tracker grade, Kp, Kd, panel and antenna mass), the scenario is the frozen 10
degree slew on a 900 s horizon, and the keys are the frozen CSV columns after the configuration.

It needs no SysML tool and no ``opensysml``: the frozen model is plain Python. The shared-subspace
experiment (``scope-sensitivity-shared-subspace`` in ``definitions.py``) reads the *v2* model to
find the variables the two variants have in common, so the sampler of that experiment, not this
oracle, needs ``opensysml``.

The module also has the factories ``definitions.py`` registers and ``side_by_side``, which joins
the two oracles' outputs of the shared experiment on ``design_id``. What the comparison reveals is
a later study; nothing here interprets it.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import design_space as ds
import pandas as pd
from adcs_sim import BASELINE

from . import ledger as lg
from .oracle import evaluate_rows
from .runner import LogUniformSampler

CONFIG_NAMES = ("wheel_class", "st_grade", "Kp", "Kd", "panel_mass_kg", "antenna_mass_kg")
ATTRIBUTE_NAMES = ("settling_time_s", "pointing_error_deg", "adcs_mass_kg", "control_effort")
FLAG_NAMES = ("settled", "momentum_ok")
AUXILIARY_NAMES = ("torque_saturated_frac", "peak_momentum_nms")


class LegacyGeostationaryOracle:
    """Configuration in, the four frozen attributes and two flags out (geostationary variant).

    Parameters
    ----------
    t_end, max_step, initial_error_deg : float, optional
        The frozen scenario (``design_space.evaluate_design`` defaults: 900 s, 0.5 s, 10 degrees).

    Notes
    -----
    A configuration with an unknown wheel class or tracker grade, or Kp or Kd outside the frozen
    ranges, or a non-positive mass, raises ``ValueError`` naming the variable.
    """

    config_names = CONFIG_NAMES
    attribute_names = ATTRIBUTE_NAMES
    flag_names = FLAG_NAMES

    def __init__(
        self, t_end: float = 900.0, max_step: float = 0.5, initial_error_deg: float = 10.0
    ):
        self.scenario = {
            "t_end": float(t_end),
            "max_step": float(max_step),
            "initial_error_deg": float(initial_error_deg),
        }
        self.ranges = {"Kp": ds.KP_RANGE, "Kd": ds.KD_RANGE}
        self.wheel_classes = list(ds.WHEEL_CLASSES)
        self.tracker_grades = list(ds.STAR_TRACKERS)

    def validate(self, configuration: Mapping) -> None:
        """Raise ``ValueError`` naming the variable for a missing, unknown or out-of-range value."""
        for name, levels in (
            ("wheel_class", self.wheel_classes),
            ("st_grade", self.tracker_grades),
        ):
            value = configuration.get(name)
            if value not in levels:
                raise ValueError(f"{name}: {value!r} is not one of {levels}")
        for name, (lo, hi) in self.ranges.items():
            value = configuration.get(name)
            if value is None:
                raise ValueError(f"{name}: missing")
            if not lo * (1 - 1e-9) <= float(value) <= hi * (1 + 1e-9):
                raise ValueError(f"{name}: {value!r} is outside the frozen range [{lo}, {hi}]")
        for name in ("panel_mass_kg", "antenna_mass_kg"):
            value = configuration.get(name)
            if value is None or not float(value) > 0:
                raise ValueError(f"{name}: {value!r} is not a positive mass")

    def __call__(self, configuration: Mapping[str, float | str]) -> dict[str, float | bool]:
        """One configuration to the frozen ``evaluate_design`` mapping."""
        self.validate(configuration)
        return ds.evaluate_design(dict(configuration), **self.scenario)

    def evaluate(self, designs: pd.DataFrame) -> pd.DataFrame:
        """The designs joined with their outputs, rows in ``design_id`` order."""
        return evaluate_rows(self, designs)


def nominal_masses() -> dict[str, float]:
    """The frozen baseline panel and antenna mass (the unperturbed values of the design space)."""
    return {"panel_mass_kg": BASELINE["panelMass"], "antenna_mass_kg": BASELINE["antennaMass"]}


# -- the shared configuration subspace -----------------------------------------------------------
def shared_subspace(v2_oracle) -> dict:
    """The configuration variables the two variants have in common, and what each fixes.

    ``v2_oracle`` is a ``CubesatOracle``. Wheel class and tracker grade are shared by name over
    the levels both declare; Kp is shared over the overlap of the v2 gain box and the frozen Kp
    range. Kd is a common name, but the two ranges do not overlap (different plant), so Kd is
    *fixed* in each variant at a declared value rather than varied. Every other variable belongs to
    one variant only (panel span and battery for v2; panel and antenna mass for the frozen one) and
    is fixed at a declared value. The result is JSON-serialisable; the ledger records it.
    """
    legacy = LegacyGeostationaryOracle()
    kp_lo = max(v2_oracle.ranges["Kp"][0], legacy.ranges["Kp"][0])
    kp_hi = min(v2_oracle.ranges["Kp"][1], legacy.ranges["Kp"][1])
    if not kp_lo < kp_hi:
        raise ValueError("the two variants' Kp ranges do not overlap")
    return {
        "varied": {
            "categorical": {
                "wheel_class": [w for w in v2_oracle.wheel_classes if w in legacy.wheel_classes],
                "st_grade": [g for g in v2_oracle.tracker_grades if g in legacy.tracker_grades],
            },
            "log_ranges": {"Kp": [kp_lo, kp_hi]},
        },
        "fixed_v2": dict(FIXED_V2),
        "fixed_legacy": {"Kd": BASELINE["Kd"], **nominal_masses()},
        "not_shared": {
            "v2_only": ["panel_span_m", "battery_wh"],
            "legacy_only": ["panel_mass_kg", "antenna_mass_kg"],
            "disjoint_ranges": ["Kd"],
        },
        "scenarios": {
            "v2": "nominalSlew of the v2 model (read from the model by the oracle)",
            "legacy": dict(legacy.scenario),
        },
    }


# design points of the v2 oracle that the frozen variant has no counterpart for (the model's own
# defaults for the span and the capacity; a Kd inside the v2 gain box); declared, not read
FIXED_V2 = {"panel_span_m": 0.6, "battery_wh": 80.0, "Kd": 1.0}


def build(experiment, root: Path | None = None, workers: int | None = None):
    """The legacy oracle for ``experiment`` (the frozen scenario; no model is read)."""
    return LegacyGeostationaryOracle()


class _FixedColumns:
    """A sampler of the varied shared variables with the variant's fixed columns appended."""

    def __init__(self, base: LogUniformSampler, fixed: Mapping[str, float]):
        self.base, self.fixed = base, dict(fixed)

    def draw(self, n: int, seed: int) -> pd.DataFrame:
        out = self.base.draw(n, seed)
        for k, v in self.fixed.items():
            out[k] = float(v)
        return out

    __call__ = draw


def build_shared_sampler(experiment, root: Path | None = None) -> _FixedColumns:
    """The sampler of the shared subspace for ``experiment`` (``inputs['variant']``: v2 or legacy).

    The varied columns are drawn identically for both variants (same seed, same ranges), so the
    two outputs are for the same wheel, tracker and Kp on every row; the fixed columns differ.
    The subspace is read from the v2 model (``experiment.inputs['subspace_model']``).
    """
    from . import cubesat_oracle as co

    model = Path(root or lg.REPO_ROOT) / experiment.inputs["subspace_model"]
    v2 = co.CubesatOracle(model.read_text(), workers=1)
    sub = shared_subspace(v2)
    base = LogUniformSampler(
        sub["varied"]["categorical"], {k: tuple(v) for k, v in sub["varied"]["log_ranges"].items()}
    )
    experiment.inputs["shared_subspace"] = sub  # the ledger entry names it
    fixed = sub["fixed_v2"] if experiment.inputs["variant"] == "v2" else sub["fixed_legacy"]
    return _FixedColumns(base, fixed)


# -- the two outputs side by side -----------------------------------------------------------------
def side_by_side(v2: pd.DataFrame, legacy: pd.DataFrame) -> pd.DataFrame:
    """Join the two oracles' outputs of the shared experiment on ``design_id``.

    The shared design columns appear once; every output column both oracles return appears as
    ``<name>_v2`` and ``<name>_legacy``. Rows must be the same designs (the shared columns equal).
    """
    shared = ["design_id", "seed", "wheel_class", "st_grade", "Kp"]
    a = v2.sort_values("design_id").reset_index(drop=True)
    b = legacy.sort_values("design_id").reset_index(drop=True)
    if not a[shared].equals(b[shared]):
        raise ValueError("the two outputs are not for the same shared designs")
    common = [
        c
        for c in (*ATTRIBUTE_NAMES, *FLAG_NAMES, *AUXILIARY_NAMES)
        if c in a.columns and c in b.columns
    ]
    out = a[shared].copy()
    for c in common:
        out[f"{c}_v2"] = a[c]
        out[f"{c}_legacy"] = b[c]
    return out
