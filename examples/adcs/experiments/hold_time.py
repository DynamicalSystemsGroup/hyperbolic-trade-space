"""The settling time by event detection: the hold time (WP16 Amendment 2), held for now.

The supervisor's quantity (``work-packages/WP16-decisions.md``): the hold time, the settling time
in control language, the first time after which the pointing error stays inside the band of the
model's settling fraction; computed as the last exit from that band. ``HoldTimeOracle`` is
``cubesat_oracle.CubesatOracle`` with that one reading changed; every other quantity, the slew
times among them, is the base oracle's (read off the accepted steps of ``simulate_adcs``).

The committed generation and the ledger hash ``cubesat_oracle.py``; the event path lives here so
that they stay unchanged until the regeneration after WP23 adopts it. ``make_oracle(...,
settling_time_method="steps" | "events")`` is the switch; ``"steps"`` is the default.

**Mechanism.** On each accepted RK45 step the dense interpolant is a quartic per state component,
so ``|q_vec|**2 - s**2 |q|**2`` is a degree-8 polynomial on the step; its falling roots are the
times the error falls through the threshold, a pass inside one step included (``band_entries``).
The times are read on a second integration of the same dynamics at ``CROSSING_RTOL`` and
``CROSSING_ATOL`` (``crossing_times``).
"""

from __future__ import annotations

import math
from collections.abc import Mapping

import numpy as np
from adcs_sim import (
    SimConfig,
    _euler_equations,
    _gravity_gradient_torque,
    _pd_control,
    _quaternion_derivative,
    make_config,
)
from scipy.integrate import solve_ivp

from .cubesat_oracle import CubesatOracle

SETTLING_METHODS = ("steps", "events")


def _state_error_deg(y: np.ndarray) -> float:
    """Attitude error of one raw state, its quaternion normalised as ``simulate_adcs`` does."""
    q = y[:4] / np.linalg.norm(y[:4])
    return float(np.degrees(2 * np.linalg.norm(q[:3])))


# Bernstein basis of degree 8 on [0, 1]: b = a @ _BERNSTEIN for power coefficients a (ascending)
_DEG = 8
_BERNSTEIN = np.array(
    [
        [math.comb(j, i) / math.comb(_DEG, i) if i <= j else 0.0 for j in range(_DEG + 1)]
        for i in range(_DEG + 1)
    ]
)


def _square(c: np.ndarray) -> np.ndarray:
    """Ascending coefficients of ``p(x)**2`` for each row of ``c`` (``(n, 5)`` to ``(n, 9)``)."""
    out = np.zeros((c.shape[0], 2 * c.shape[1] - 1))
    for i in range(c.shape[1]):
        out[:, i : i + c.shape[1]] += c[:, i : i + 1] * c
    return out


def band_entries(interpolants, threshold_deg: float) -> np.ndarray:
    """Every time the attitude error of the dense solution falls through ``threshold_deg``.

    On each accepted step RK45's interpolant is a quartic in ``x = (t - t_old) / h`` per state
    component, so ``|q_vec|**2 - s**2 |q|**2`` (``s = radians(threshold) / 2``; the error is
    ``degrees(2 |q_vec| / |q|)``) is a polynomial of degree 8 on ``x`` in ``[0, 1]``. Its sign
    changes are the crossings, found on every step, including a pass through the band that
    begins and ends inside one step (which a sign test at the step ends cannot see). Steps whose
    Bernstein coefficients share one sign have no root and are skipped; on the others the real
    roots in ``(0, 1]`` where the polynomial decreases are kept (an entry; a tangency, where it
    touches without crossing, is not one).
    """
    s2 = (np.radians(threshold_deg) / 2) ** 2
    t_old = np.array([d.t_old for d in interpolants])
    h = np.array([d.h for d in interpolants])
    y_old = np.stack([d.y_old[:4] for d in interpolants])
    Q = np.stack([d.Q[:4] for d in interpolants])  # (n, 4, 4): powers x .. x**4
    c = np.concatenate([y_old[:, :, None], h[:, None, None] * Q], axis=2)  # (n, 4, 5)
    sq = [_square(c[:, k]) for k in range(4)]
    f = (1 - s2) * (sq[0] + sq[1] + sq[2]) - s2 * sq[3]
    b = f @ _BERNSTEIN
    candidates = np.flatnonzero(~((b > 0).all(axis=1) | (b < 0).all(axis=1)))
    out = []
    for i in candidates:
        poly = np.polynomial.Polynomial(f[i])
        deriv = poly.deriv()
        for r in poly.roots():
            if abs(r.imag) > 1e-9 or not 0.0 < r.real <= 1.0:
                continue
            x = r.real
            for _ in range(2):  # Newton on the polynomial: the root to rounding
                d = deriv(x)
                x = x - poly(x) / d if d else x
            if 0.0 < x <= 1.0 and deriv(x) < 0:
                out.append(t_old[i] + x * h[i])
    return np.unique(np.asarray(out, float))


# The crossing times are read on their own integration of the same dynamics, at tighter
# tolerances than the record's (rtol 1e-10, atol 1e-12, which every other quantity keeps): at the
# record's tolerances the located time still moves with the step sequence by up to about 5e-8
# relative under a 1e-12 jitter of the inputs; at these, by at most about 1.5e-10 (WP16
# Amendment 2, R-9; measured on designs 0, 5, 17, 400, 763 and the six check designs).
CROSSING_RTOL, CROSSING_ATOL = 1e-13, 1e-16


def _dynamics(config: SimConfig):
    """The right-hand side of ``adcs_sim.simulate_adcs``, from its own functions."""
    J = np.array([config.Jxx, config.Jyy, config.Jzz])

    def dynamics(t, state):
        q = state[:4] / np.linalg.norm(state[:4])
        omega = state[4:7]
        tau = _pd_control(q, omega, config.Kp, config.Kd, config.max_torque)
        tau = tau + _gravity_gradient_torque(q, J, config.n_orbital)
        return np.concatenate([_quaternion_derivative(q, omega), _euler_equations(omega, J, tau)])

    return dynamics


def _solve(config: SimConfig, rtol: float, atol: float, dense_output: bool = False):
    """``simulate_adcs``'s ``solve_ivp`` call (RK45, the scenario's ``max_step``) at ``rtol``."""
    sol = solve_ivp(
        _dynamics(config),
        config.t_span,
        np.array([*config.q0, *config.omega0]),
        method="RK45",
        max_step=config.max_step,
        rtol=rtol,
        atol=atol,
        dense_output=dense_output,
    )
    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")
    return sol


def crossing_times(config: SimConfig, thresholds_deg: Mapping[str, float]) -> dict:
    """For each named threshold, every time the attitude error falls through it (WP16 Amendment 2).

    The slew is integrated as ``simulate_adcs`` integrates it, at ``CROSSING_RTOL`` and
    ``CROSSING_ATOL``, keeping the dense output, and the entries are located on its interpolant
    (``band_entries``): event detection on the error minus the threshold, including a pass
    through the band shorter than a step. Returns ``{name: (entry times, final error in deg)}``.
    """
    sol = _solve(config, CROSSING_RTOL, CROSSING_ATOL, dense_output=True)
    final = _state_error_deg(sol.y[:, -1])
    return {
        n: (np.asarray(band_entries(sol.sol.interpolants, v), float), final)
        for n, v in thresholds_deg.items()
    }


def _hold_time(entries: np.ndarray, final_deg: float, threshold_deg: float, horizon: float):
    """The settling time by event detection (the hold time): the last time the error falls
    through ``threshold_deg``, the first time after which it stays below; the horizon if it ends
    above; 0 for a zero start."""
    if threshold_deg <= 0:
        return 0.0
    if final_deg > threshold_deg:
        return float(horizon)
    return float(entries[-1]) if len(entries) else 0.0


def hold_time(entries: np.ndarray, final_deg: float, threshold_deg: float, horizon: float):
    """The last time the error falls through ``threshold_deg``, the first time after which it
    stays below; the horizon if it ends above; 0 for a zero start."""
    if threshold_deg <= 0:
        return 0.0
    if final_deg > threshold_deg:
        return float(horizon)
    return float(entries[-1]) if len(entries) else 0.0


class HoldTimeOracle(CubesatOracle):
    """``CubesatOracle`` whose settling time is the hold time by event detection.

    ``evaluate`` runs serially (the base pool builds base oracles); the path is held for the
    regeneration after WP23, which moves it into ``cubesat_oracle.py``.
    """

    settling_time_method = "events"

    def __init__(self, *args, **kwargs):
        kwargs["workers"] = 1
        super().__init__(*args, **kwargs)

    def _measure_slew(self, params: dict) -> dict:
        out = super()._measure_slew(params)
        sc = self.scenario
        sim = make_config(
            params,
            params["Kp"],
            params["Kd"],
            wheel={"maxTorque": params["maxTorque"], "maxMomentum": params["maxMomentum"]},
            t_end=sc["t_end_s"],
            initial_error_deg=sc["slew_deg"],
            max_step=sc["max_step_s"],
        )
        threshold = sc["settling_fraction"] * _state_error_deg(np.array([*sim.q0, *sim.omega0]))
        entries, final = crossing_times(sim, {"settle": threshold})["settle"]
        out["settling_time"] = hold_time(entries, final, threshold, sim.t_span[1])
        return out


def make_oracle(*args, settling_time_method: str = "steps", **kwargs) -> CubesatOracle:
    """The oracle for ``settling_time_method``: ``"steps"`` (default, the committed generation's
    ``CubesatOracle``) or ``"events"`` (``HoldTimeOracle``)."""
    if settling_time_method not in SETTLING_METHODS:
        raise ValueError(
            f"settling_time_method: {settling_time_method!r} is not one of {SETTLING_METHODS}"
        )
    cls = CubesatOracle if settling_time_method == "steps" else HoldTimeOracle
    return cls(*args, **kwargs)
