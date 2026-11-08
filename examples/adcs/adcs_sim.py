"""Numerical ADCS simulation for the geostationary-satellite trade-space case (WP4).

Ported from ``analysis/numerical.py`` and ``analysis/symbolic.py`` of
DynamicalSystemsGroup/ADCS-lifecycle-demo (numpy/scipy parts only).

Copyright 2026 Michael Zargham

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. See the License for the specific language governing permissions and limitations under
the License.

Departures from the source are marked ``# CHANGED:``. The simulation produces observations of the
model, not of a physical system. Pitfalls kept visible: settling time is quantized by
``max_step`` and censored at the horizon; wheel momentum is observed, not enforced; all hardware
values are illustrative.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

# Baseline parameters (source structural/parameters.ttl).
BASELINE: dict[str, float] = {
    "mass": 550.0,
    "bodyLength": 0.90,
    "bodyWidth": 1.00,
    "bodyHeight": 1.10,
    "orbitalRate": 7.2722e-05,
    "panelSpan": 2.50,
    "panelChord": 0.90,
    "panelMass": 30.0,
    "antennaDiameter": 0.80,
    "antennaOffset": 0.75,
    "antennaMass": 18.0,
    "maxTorque": 0.1,
    "maxMomentum": 4.0,
    "wheelMass": 2.5,
    "stAccuracy": 5.0,
    "stUpdateRate": 4.0,
    "stMass": 2.0,
    "gyroARW": 0.0017,
    "gyroBias": 0.0001,
    "controlBandwidth": 1.0,
    "imuMass": 0.5,
    "Kp": 1.0,
    "Kd": 10.0,
}

SRP_TORQUE_NM = (
    1e-5  # CHANGED: constant solar-radiation-pressure torque (illustrative, GEO-typical)
)
GG_THETA_MAX_RAD = np.radians(0.1)  # worst-case angle used for the gravity-gradient bound


def inertia_tensor(params: dict[str, float]) -> tuple[float, float, float]:
    """Composite principal inertia (Jxx, Jyy, Jzz) in kg m^2.

    Box bus, two thin-plate panels offset along Y (centre at Ly/2 + span/2) and a disk antenna
    offset along Z, combined with the parallel-axis theorem. CHANGED: numeric port of the
    source's symbolic ``build_inertia_tensor_symbolic``.

    >>> tuple(round(j, 2) for j in inertia_tensor(BASELINE))
    (327.14, 107.48, 303.45)
    """
    m, lx, ly, lz = (params[k] for k in ("mass", "bodyLength", "bodyWidth", "bodyHeight"))
    mp, span, chord = params["panelMass"], params["panelSpan"], params["panelChord"]
    ma, da, za = params["antennaMass"], params["antennaDiameter"], params["antennaOffset"]

    bus = np.array([ly**2 + lz**2, lx**2 + lz**2, lx**2 + ly**2]) * m / 12
    y = ly / 2 + span / 2
    panel_cm = np.array([span**2, chord**2, span**2 + chord**2]) * mp / 12
    panel = panel_cm + mp * np.array([y**2, 0.0, y**2])
    r = da / 2
    ant_cm = np.array([r**2 / 4, r**2 / 4, r**2 / 2]) * ma
    ant = ant_cm + ma * np.array([za**2, za**2, 0.0])
    total = bus + 2 * panel + ant
    return float(total[0]), float(total[1]), float(total[2])


def pointing_budget(
    params: dict[str, float], Kp: float, st_accuracy_arcsec: float
) -> dict[str, float]:
    """Analytic steady pointing error budget.

    theta_ss = 4 (tau_gg_max + tau_srp) / Kp (the source's effective stiffness Kp/4 on theta),
    tau_gg_max = 3 n^2 max(|Jz - Jy|, |Jz - Jx|) * 0.1 deg. CHANGED: the constant SRP torque is
    added (it does not enter the simulated dynamics). Total error is the root-sum-square of
    theta_ss and the star-tracker floor stAccuracy / 3600 deg.
    """
    jx, jy, jz = inertia_tensor(params)
    n = params["orbitalRate"]
    tau_gg = 3 * n**2 * max(abs(jz - jy), abs(jz - jx)) * GG_THETA_MAX_RAD
    theta_ss_deg = float(np.degrees(4 * (tau_gg + SRP_TORQUE_NM) / Kp))
    floor_deg = st_accuracy_arcsec / 3600.0
    return {
        "tau_gg_max": float(tau_gg),
        "theta_ss_deg": theta_ss_deg,
        "st_floor_deg": floor_deg,
        "pointing_error_deg": float(np.hypot(theta_ss_deg, floor_deg)),
    }


@dataclass
class SimConfig:
    """Simulation configuration, everything needed to reproduce."""

    Jxx: float
    Jyy: float
    Jzz: float
    Kp: float
    Kd: float
    n_orbital: float
    max_torque: float
    max_momentum: float
    t_span: tuple[float, float]
    max_step: float = 0.5
    q0: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    omega0: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class SimResult:
    """Simulation output, time histories of all state variables."""

    t: np.ndarray
    q: np.ndarray
    omega: np.ndarray
    tau_ctrl: np.ndarray
    tau_gg: np.ndarray
    h_wheel: np.ndarray
    config: SimConfig

    def summary(self) -> dict:
        """Key metrics. Settling time is the last time the error exceeds 1 % of the initial."""
        theta_err_deg = np.degrees(2 * np.linalg.norm(self.q[:, :3], axis=1))
        if theta_err_deg[0] > 0:
            exceeded = np.where(theta_err_deg > 0.01 * theta_err_deg[0])[0]
            settling_time = float(self.t[exceeded[-1] if len(exceeded) > 0 else 0])
        else:
            settling_time = 0.0
        h_mag = np.linalg.norm(self.h_wheel, axis=1)
        torque_mag = np.linalg.norm(self.tau_ctrl, axis=1)
        sat = np.any(np.abs(self.tau_ctrl) >= self.config.max_torque - 1e-12, axis=1)
        return {
            "final_error_deg": float(theta_err_deg[-1]),
            "peak_error_deg": float(np.max(theta_err_deg)),
            "settling_time_s": settling_time,
            "peak_wheel_momentum": float(np.max(h_mag)),
            "peak_control_torque": float(np.max(np.abs(self.tau_ctrl))),
            "final_omega_norm": float(np.linalg.norm(self.omega[-1])),
            "duration_s": float(self.t[-1]),
            "n_steps": len(self.t),
            # CHANGED: control effort and saturation fraction added for the trade study.
            "control_effort": float(np.trapezoid(torque_mag, self.t)),
            "torque_saturated_frac": float(np.mean(sat)),
        }


def _gravity_gradient_torque(q: np.ndarray, J: np.ndarray, n: float) -> np.ndarray:
    """Linearized gravity gradient torque at GEO."""
    return np.array(
        [
            3 * n**2 * (J[2] - J[1]) * q[0],
            3 * n**2 * (J[2] - J[0]) * q[1],
            0.0,
        ]
    )


def _pd_control(
    q: np.ndarray, omega: np.ndarray, Kp: float, Kd: float, max_torque: float
) -> np.ndarray:
    """PD law tau = -Kp/2 q_vec - Kd omega, clipped per axis to max_torque."""
    return np.clip(-Kp / 2 * q[:3] - Kd * omega, -max_torque, max_torque)


def _quaternion_derivative(q: np.ndarray, omega: np.ndarray) -> np.ndarray:
    qx, qy, qz, qw = q
    wx, wy, wz = omega
    return 0.5 * np.array(
        [
            qw * wx - qz * wy + qy * wz,
            qz * wx + qw * wy - qx * wz,
            -qy * wx + qx * wy + qw * wz,
            -qx * wx - qy * wy - qz * wz,
        ]
    )


def _euler_equations(omega: np.ndarray, J: np.ndarray, tau: np.ndarray) -> np.ndarray:
    return (tau - np.cross(omega, J * omega)) / J


def simulate_adcs(config: SimConfig) -> SimResult:
    """Integrate the nonlinear quaternion + Euler dynamics with PD control and gravity gradient."""
    J = np.array([config.Jxx, config.Jyy, config.Jzz])

    def dynamics(t, state):
        q = state[:4] / np.linalg.norm(state[:4])
        omega = state[4:7]
        tau = _pd_control(q, omega, config.Kp, config.Kd, config.max_torque)
        tau = tau + _gravity_gradient_torque(q, J, config.n_orbital)
        return np.concatenate([_quaternion_derivative(q, omega), _euler_equations(omega, J, tau)])

    x0 = np.array([*config.q0, *config.omega0])
    sol = solve_ivp(
        dynamics,
        config.t_span,
        x0,
        method="RK45",
        max_step=config.max_step,
        rtol=1e-10,
        atol=1e-12,
    )  # CHANGED: dense_output dropped (never used)
    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")

    t = sol.t
    q = sol.y[:4].T
    q = q / np.linalg.norm(q, axis=1, keepdims=True)
    omega = sol.y[4:7].T

    # CHANGED: vectorised recomputation of the torques; same values as the source loop.
    tau_ctrl = np.clip(
        -config.Kp / 2 * q[:, :3] - config.Kd * omega, -config.max_torque, config.max_torque
    )
    tau_gg = np.zeros_like(omega)
    tau_gg[:, 0] = 3 * config.n_orbital**2 * (J[2] - J[1]) * q[:, 0]
    tau_gg[:, 1] = 3 * config.n_orbital**2 * (J[2] - J[0]) * q[:, 1]
    dt = np.diff(t, prepend=t[0])
    h_wheel = np.cumsum(tau_ctrl * dt[:, None], axis=0)  # wheel momentum = integral of tau_ctrl

    return SimResult(
        t=t, q=q, omega=omega, tau_ctrl=tau_ctrl, tau_gg=tau_gg, h_wheel=h_wheel, config=config
    )


def make_config(
    params: dict[str, float],
    Kp: float,
    Kd: float,
    wheel: dict[str, float] | None = None,
    t_end: float = 360.0,
    initial_error_deg: float = 10.0,
    max_step: float = 0.5,
    axis: int = 0,
) -> SimConfig:
    """Build a SimConfig for a slew of ``initial_error_deg`` about body ``axis`` (default X).

    ``wheel`` supplies ``maxTorque`` and ``maxMomentum`` (defaults: the baseline wheel).
    CHANGED: replaces the source's ``make_config_from_params`` (numeric inertia, explicit gains).
    """
    jxx, jyy, jzz = inertia_tensor(params)
    wheel = wheel or {}
    half = np.radians(initial_error_deg) / 2
    q0 = [0.0, 0.0, 0.0, float(np.cos(half))]
    q0[axis] = float(np.sin(half))
    return SimConfig(
        Jxx=jxx,
        Jyy=jyy,
        Jzz=jzz,
        Kp=float(Kp),
        Kd=float(Kd),
        n_orbital=params["orbitalRate"],
        max_torque=wheel.get("maxTorque", params["maxTorque"]),
        max_momentum=wheel.get("maxMomentum", params["maxMomentum"]),
        t_span=(0.0, float(t_end)),
        max_step=max_step,
        q0=tuple(q0),
    )


def run_step_response(
    params: dict[str, float], Kp: float, Kd: float, t_end: float = 360.0
) -> SimResult:
    """Standard step response: 10 degree slew about X, source tolerances."""
    return simulate_adcs(make_config(params, Kp, Kd, t_end=t_end))
