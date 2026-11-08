"""Design space and design evaluation for the ADCS trade-space case (WP4).

Two categorical hardware choices (reaction-wheel class, star-tracker grade), two continuous gains
(Kp, Kd, log-uniform) and a ~10 % lognormal perturbation of panel and antenna mass. Hardware class
values are ILLUSTRATIVE, not calibrated to real products. Because mass is dominated by the
hardware class, the mass attribute is stratified: gaps between strata are structural.

``evaluate_design`` runs the simulator for a 10 degree X slew and returns the four attributes:

* ``settling_time_s``: last time the error exceeds 1 % of the initial error (quantized by
  ``max_step``; censored at ``t_end``, in which case ``settled`` is False and the value is kept);
* ``pointing_error_deg``: analytic, RSS of steady disturbance error (gravity gradient + constant
  SRP torque, over effective stiffness proportional to Kp) and the star-tracker floor;
* ``adcs_mass_kg``: 3 wheels + star tracker + IMU;
* ``control_effort``: integral of the norm of the control torque over the simulated slew.

Flags: ``settled``, ``momentum_ok`` (peak wheel momentum <= wheel class maxMomentum; momentum is
observed, not enforced by the simulation), ``torque_saturated_frac``. Peak momentum is also
returned as ``peak_momentum_nms``.
"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd
from adcs_sim import BASELINE, make_config, pointing_budget, simulate_adcs

# (maxTorque N m, maxMomentum N m s, mass kg); illustrative.
WHEEL_CLASSES: dict[str, tuple[float, float, float]] = {
    "small": (0.05, 2.0, 1.5),
    "medium": (0.1, 4.0, 2.5),
    "large": (0.2, 8.0, 4.0),
}
# (accuracy arcsec 1 sigma, mass kg); illustrative.
STAR_TRACKERS: dict[str, tuple[float, float]] = {
    "coarse": (15.0, 1.0),
    "medium": (5.0, 2.0),
    "fine": (1.5, 3.5),
}
KP_RANGE = (0.5, 16.0)
KD_RANGE = (5.0, 60.0)
MASS_SIGMA = 0.10
N_WHEELS = 3

# Coarser settings for tests only: much faster, different quantization of settling time.
FAST_SIM = {"t_end": 400.0, "max_step": 2.0}

CONFIG_COLUMNS = [
    "design_id",
    "seed",
    "wheel_class",
    "st_grade",
    "Kp",
    "Kd",
    "panel_mass_kg",
    "antenna_mass_kg",
]


def sample_designs(n: int, rng_or_seed: int | np.random.Generator = 0) -> pd.DataFrame:
    """Draw ``n`` designs with one child seed per design.

    An integer seed uses ``SeedSequence(seed).spawn(n)``, so design i does not depend on n. A
    ``Generator`` draws the n child seeds from its bit stream. Wheel class and star-tracker grade
    are uniform; Kp and Kd log-uniform in ``KP_RANGE`` / ``KD_RANGE``; panel and antenna mass are
    multiplied by independent lognormal factors (sigma = 0.10, median 1).
    """
    if isinstance(rng_or_seed, np.random.Generator):
        child_seeds = [int(s) for s in rng_or_seed.integers(0, 2**62, size=n)]
    else:
        children = np.random.SeedSequence(int(rng_or_seed)).spawn(n)
        child_seeds = [int(c.generate_state(1, dtype=np.uint64)[0] >> 2) for c in children]
    wheels, sts = list(WHEEL_CLASSES), list(STAR_TRACKERS)
    rows = []
    for i, cs in enumerate(child_seeds):
        g = np.random.default_rng(cs)
        w, s = g.integers(len(wheels)), g.integers(len(sts))
        kp = float(np.exp(g.uniform(*np.log(KP_RANGE))))
        kd = float(np.exp(g.uniform(*np.log(KD_RANGE))))
        fp, fa = np.exp(MASS_SIGMA * g.standard_normal(2))
        rows.append(
            {
                "design_id": i,
                "seed": cs,
                "wheel_class": wheels[w],
                "st_grade": sts[s],
                "Kp": kp,
                "Kd": kd,
                "panel_mass_kg": float(BASELINE["panelMass"] * fp),
                "antenna_mass_kg": float(BASELINE["antennaMass"] * fa),
            }
        )
    return pd.DataFrame(rows, columns=CONFIG_COLUMNS)


def evaluate_design(
    row: Mapping | pd.Series,
    t_end: float = 900.0,
    max_step: float = 0.5,
    initial_error_deg: float = 10.0,
) -> dict:
    """Simulate one design and return its attributes and feasibility flags as a dict."""
    max_torque, max_momentum, wheel_mass = WHEEL_CLASSES[row["wheel_class"]]
    st_accuracy, st_mass = STAR_TRACKERS[row["st_grade"]]
    params = dict(BASELINE)
    params.update(
        panelMass=float(row["panel_mass_kg"]),
        antennaMass=float(row["antenna_mass_kg"]),
        maxTorque=max_torque,
        maxMomentum=max_momentum,
        wheelMass=wheel_mass,
        stAccuracy=st_accuracy,
        stMass=st_mass,
    )
    cfg = make_config(
        params,
        row["Kp"],
        row["Kd"],
        wheel={"maxTorque": max_torque, "maxMomentum": max_momentum},
        t_end=t_end,
        initial_error_deg=initial_error_deg,
        max_step=max_step,
    )
    s = simulate_adcs(cfg)
    summ = s.summary()
    pointing = pointing_budget(params, float(row["Kp"]), st_accuracy)
    return {
        "settling_time_s": summ["settling_time_s"],
        "pointing_error_deg": pointing["pointing_error_deg"],
        "adcs_mass_kg": N_WHEELS * wheel_mass + st_mass + params["imuMass"],
        "control_effort": summ["control_effort"],
        "settled": bool(summ["settling_time_s"] < t_end),
        "momentum_ok": bool(summ["peak_wheel_momentum"] <= max_momentum),
        "torque_saturated_frac": summ["torque_saturated_frac"],
        "peak_momentum_nms": summ["peak_wheel_momentum"],
    }
