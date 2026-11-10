"""The SysML-backed cubesat oracle and sampler (WP15 15.4): configuration to attributes and flags.

``CubesatOracle`` satisfies ``experiments.oracle.Oracle`` for the v2 model
(``model_v2/cubesat.sysml``). Nothing about the case is copied here: the design ranges, the
enumerations and their alternatives, the gain box, the scenario (slew angle, horizon, step, the
band, the settling fraction) and every accounting constant are read from the model, which is
also where the accounting, the attributes and the feasibility are computed:

* **configure**: each design becomes a ``Cubesat`` part of the loaded model (one load per chunk);
* **measure**: the unchanged ``adcs_sim.simulate_adcs`` integrates the slew (SysML cannot), on the
  parameters the configuration implies; the measured quantities are the only numbers that enter
  the model from Python. The settling time is the hold time by event detection (WP16 Amendment 2,
  WP23 G5): the first time after which the attitude error stays inside the band of the model's
  settling fraction, located as the last falling root of the error on the dense RK45 solution
  (``settling_time_method="events"``, the default; ``"steps"`` reads it off the accepted steps,
  the generation before WP23);
* **account**: the model's ``analysis def SlewExperiment`` takes the measured quantities and
  returns the eight attributes it computes (the settling time is measured and passes into the
  row unchanged);
* **feasibility**: the four flags are the verdicts of the model's named requirements
  (``feasibility.FeasibilityChecker``, engine ``run``, evidence ``observed``). They are
  observations of single configurations; the solver's classification of regions before simulation
  (``exclusion.py``) is recorded by ``build`` in the ledger entry.

The output keys are those of the frozen ``cubesat_model.measure`` less the slew-time columns
(``slew_time_s``, ``slew_time_05deg_s``; the case has one time metric, WP23 G5), in the frozen
CSV column order, followed by the scenario columns ``slew_deg``, ``t_end_s``, ``max_step_s`` that
``evaluate`` appends. Construction fails with ``cubesat_model.OpenSysMLUnavailable`` (a named
cause) when the runtime cannot start.

``build(experiment)`` and ``build_sampler(experiment)`` are the factories ``definitions.py``
registers; they read the model the experiment names (relative to the repository root).

**Event detection, the mechanism.** On each accepted RK45 step the dense interpolant is a quartic
per state component, so ``|q_vec|**2 - s**2 |q|**2`` is a degree-8 polynomial on the step; its
falling roots are the times the error falls through the threshold, a pass inside one step
included (``band_entries``). The times are read on a second integration of the same dynamics at
``CROSSING_RTOL`` and ``CROSSING_ATOL`` (``crossing_times``); every other quantity stays on
``simulate_adcs`` at the record's tolerances.
"""

from __future__ import annotations

import math
import multiprocessing as mp
import os
from collections.abc import Mapping
from pathlib import Path

import numpy as np
import pandas as pd
from adcs_sim import (
    BASELINE,
    SimConfig,
    _euler_equations,
    _gravity_gradient_torque,
    _pd_control,
    _quaternion_derivative,
    make_config,
    simulate_adcs,
)
from opensysml.values import Quantity
from scipy.integrate import solve_ivp

from . import ledger as lg
from .feasibility import FeasibilityChecker
from .runner import LogUniformSampler

PACKAGE = "CubesatTradeSpaceV2"
CONFIG_NAMES = ("panel_span_m", "battery_wh", "wheel_class", "st_grade", "Kp", "Kd")
# the nine traded metrics (WP23 G5: one time metric, the settling time)
ATTRIBUTE_NAMES = (
    "settling_time_s",
    "pointing_error_deg",
    "total_mass_kg",
    "control_effort",
    "power_margin_w",
    "energy_balance_wh",
    "eclipse_reserve_wh",
    "peak_slew_power_w",
    "dod_eclipse",
)
FLAG_NAMES = ("settled", "momentum_ok", "power_ok", "dod_ok")
# the model's analysis returns the eight attributes it computes in this order, each read in this
# unit; the settling time is measured and enters the row from the measurement
_COMPUTED_NAMES = ATTRIBUTE_NAMES[1:]
_COMPUTED_UNITS = (
    "SI::degree",
    "SI::kg",
    "SI::N*SI::m*SI::s",
    "SI::W",
    "SI::W*SI::h",
    "SI::W*SI::h",
    "SI::W",
    None,
)
# the keys of the frozen ``cubesat_model.measure`` less the slew-time columns, in order
OUTPUT_NAMES = (
    "settling_time_s",
    "pointing_error_deg",
    "total_mass_kg",
    "adcs_mass_kg",
    "control_effort",
    "power_margin_w",
    "energy_balance_wh",
    "eclipse_reserve_wh",
    "peak_slew_power_w",
    "dod_eclipse",
    "settled",
    "momentum_ok",
    "torque_saturated_frac",
    "power_ok",
    "dod_ok",
    "peak_momentum_nms",
    "panel_mass_kg",
    "battery_mass_kg",
    "generated_power_w",
    "available_power_w",
    "usable_torque_nm",
    "slew_loss_energy_wh",
)
SCENARIO_COLUMNS = ("slew_deg", "t_end_s", "max_step_s")
DESIGN_COLUMNS = ("design_id", "seed", "wheel_class", "st_grade", *CONFIG_NAMES[:2], "Kp", "Kd")
# how the settling time is read: ``"events"`` (the hold time by event detection, the measurement
# of record since WP23) or ``"steps"`` (off the accepted steps, the generation before it)
SETTLING_METHODS = ("events", "steps")
CHUNK = 10  # designs per model load, as in the frozen generator
_EDGE = 1e-9  # relative slack at the range edges (float round trip through the model)


class ScenarioError(ValueError):
    """The experiment names a scenario or gain box the model does not declare."""


def _quantity_value(model, quantity, unit: str | None) -> float:
    if isinstance(quantity, list):
        quantity = quantity[0]
    if isinstance(quantity, Quantity):
        return float(quantity.in_unit(model.eval(f"1.0 [{unit}]").unit))
    return float(quantity)


class ModelReader:
    """Reads of the v2 model a caller needs: ranges, enumerations, alternatives, scenario."""

    def __init__(self, model, package: str = PACKAGE):
        self.model, self.package = model, package
        self._units: dict[str, object] = {}

    def unit(self, expression: str):
        if expression not in self._units:
            self._units[expression] = self.model.eval(f"1.0 [{expression}]").unit
        return self._units[expression]

    def read(self, expression: str, unit: str | None = None, model=None) -> float:
        m = model or self.model
        out = m.eval(f"{self.package}::{expression}")
        if isinstance(out, list):
            out = out[0]
        if isinstance(out, Quantity):
            return float(out.in_unit(self.unit(unit)))
        return float(out)

    def literals(self, enum: str) -> list[str]:
        return [c.name for c in self.model.find(f"{self.package}::{enum}").children()]

    def alternatives(self, abstract: str, enum_attr: str) -> dict[str, str]:
        """Concrete specializations of an abstract part def, keyed by their enumeration literal."""
        target = f"{self.package}::{abstract}"
        table = {}
        for q in self.model.query(
            scope=[self.package],
            where={"property": "@type", "operator": "=", "value": "PartDefinition"},
        ):
            if any(sp.target_id == target for sp in self.model.find(q.id).specializations):
                lit = self.model.instantiate(q.id).get(enum_attr)
                table[(lit.name or lit.literal_id).split("::")[-1]] = q.id
        return table

    def gain_box(self, box: str) -> dict[str, float]:
        part = f"{box}Gains"
        try:
            return {k: self.read(f"{part}.{k}") for k in ("KpMin", "KpMax", "KdMin", "KdMax")}
        except Exception as exc:
            raise ScenarioError(f"gain box {box!r}: the model declares no part {part!r}") from exc

    def ranges(self) -> dict[str, tuple[float, float]]:
        r = self.read
        return {
            "panel_span_m": tuple(r(f"designRanges.panelSpan{k}", "SI::m") for k in ("Min", "Max")),
            "battery_wh": tuple(
                r(f"designRanges.batteryCapacity{k}", "SI::W*SI::h") for k in ("Min", "Max")
            ),
        }

    def scenario(self, name: str) -> dict[str, float]:
        try:
            r = self.read
            return {
                "slew_deg": r(f"{name}.slewAngle", "SI::degree"),
                "t_end_s": r(f"{name}.horizon", "SI::s"),
                "max_step_s": r(f"{name}.timeStep", "SI::s"),
                "band_deg": r(f"{name}.slewBand", "SI::degree"),
                "settling_fraction": r(f"{name}.settlingFraction"),
            }
        except Exception as exc:
            raise ScenarioError(f"scenario {name!r}: the model declares no such part") from exc


# -- the settling time: off the steps, or by event detection ---------------------------------------
def _attitude_error_deg(res) -> np.ndarray:
    return np.degrees(2 * np.linalg.norm(res.q[:, :3], axis=1))


def _last_outside(res, fraction: float) -> float:
    """Last accepted step at which the error exceeds ``fraction`` of its start (``"steps"``)."""
    err = _attitude_error_deg(res)
    if err[0] <= 0:
        return 0.0
    outside = np.flatnonzero(err > fraction * err[0])
    return float(res.t[outside[-1] if len(outside) else 0])


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
    """For each named threshold, every time the attitude error falls through it.

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


def hold_time(entries: np.ndarray, final_deg: float, threshold_deg: float, horizon: float):
    """The settling time by event detection: the last time the error falls through
    ``threshold_deg``, the first time after which it stays below; the horizon if it ends above;
    0 for a zero start."""
    if threshold_deg <= 0:
        return 0.0
    if final_deg > threshold_deg:
        return float(horizon)
    return float(entries[-1]) if len(entries) else 0.0


class CubesatOracle:
    """Configuration in, attributes and flags out, for one scenario and gain box of the v2 model.

    Parameters
    ----------
    model_text : str
        The text of ``model_v2/cubesat.sysml``.
    scenario : str
        The model's scenario part (default ``nominalSlew``).
    gain_box : str
        ``baseline`` or ``aggressive``: reads the model's ``<name>Gains`` part; configurations
        outside it raise ``ValueError``.
    workers : int or None
        Processes for ``evaluate`` (``None``: ``EXPERIMENTS_WORKERS`` or CPU count minus one;
        1: serial). Designs are measured in chunks of 10; the result is the same for any count.
    connection : object, optional
        An opensysml connection; by default the process's own (``cubesat_model.get_connection``,
        which raises ``OpenSysMLUnavailable`` naming the cause).
    settling_time_method : str
        ``"events"`` (default): the hold time by event detection on the dense solution;
        ``"steps"``: the last accepted step outside the band (the generation before WP23).
    """

    config_names = CONFIG_NAMES
    attribute_names = ATTRIBUTE_NAMES
    flag_names = FLAG_NAMES

    def __init__(
        self,
        model_text: str,
        scenario: str = "nominalSlew",
        gain_box: str = "aggressive",
        *,
        workers: int | None = None,
        connection=None,
        settling_time_method: str = "events",
    ):
        if settling_time_method not in SETTLING_METHODS:
            raise ValueError(
                f"settling_time_method: {settling_time_method!r} is not one of {SETTLING_METHODS}"
            )
        if connection is None:
            import cubesat_model as cm

            connection = cm.get_connection()
        self.model_text = model_text
        self.scenario_name, self.gain_box_name = scenario, gain_box
        self.settling_time_method = settling_time_method
        self.workers = workers
        self.connection = connection
        self.model = connection.load_from_content(model_text, strict=True)
        self.reader = ModelReader(self.model)
        self.scenario = self.reader.scenario(scenario)
        self.gains = self.reader.gain_box(gain_box)
        self.ranges = {
            **self.reader.ranges(),
            "Kp": (self.gains["KpMin"], self.gains["KpMax"]),
            "Kd": (self.gains["KdMin"], self.gains["KdMax"]),
        }
        self.wheel_classes = self.reader.literals("WheelClass")
        self.tracker_grades = self.reader.literals("TrackerGrade")
        self.wheels = self.reader.alternatives("ReactionWheel", "wheelClass")
        self.trackers = self.reader.alternatives("StarTracker", "grade")
        engines = [e for e in connection.list_engines() if e.ready]
        info = connection.server_info()
        self.runtime_info = {
            "runtime": info.version,
            "engines": sorted(e.name for e in engines),
            "scenario": scenario,
            "gain_box": gain_box,
            "settling_time_method": settling_time_method,
        }

    # -- validation ----------------------------------------------------------------------------
    def validate(self, configuration: Mapping) -> None:
        """Raise ``ValueError`` naming the variable for a missing, out-of-range or unknown value."""
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
            slack = _EDGE * max(abs(lo), abs(hi))
            if not lo - slack <= float(value) <= hi + slack:
                raise ValueError(f"{name}: {value!r} is outside the model's range [{lo}, {hi}]")

    # -- one chunk -----------------------------------------------------------------------------
    def _configure(self, rows: list[dict]):
        def num(x):
            return f"{float(x):.17e}"

        usages = "".join(
            f"    part cfg_{int(r['design_id'])} : {PACKAGE}::Cubesat {{\n"
            f"        :>> panelSpan default = {num(r['panel_span_m'])} [SI::m];\n"
            f"        :>> batteryCapacity default = {num(r['battery_wh'])} [SI::W*SI::h];\n"
            f"        part :>> wheel : {self.wheels[r['wheel_class']]};\n"
            f"        part :>> tracker : {self.trackers[r['st_grade']]};\n"
            f"        part :>> controller {{ :>> Kp default = {num(r['Kp'])};"
            f" :>> Kd default = {num(r['Kd'])}; }}\n    }}\n"
            for r in rows
        )
        loaded = self.connection.load_from_content(
            self.model_text + "\npackage Configurations {\n" + usages + "}\n", strict=True
        )
        return loaded, [f"Configurations::cfg_{int(r['design_id'])}" for r in rows]

    def _parameters(self, inst, loaded) -> dict:
        """The inputs of the unchanged inertia model, taken from the configuration's parts."""
        rd, kg, m = self.reader, "SI::kg", "SI::m"

        def v(q, unit):
            return _quantity_value(loaded, q, unit)

        bus, panel, ant = inst.get("bus"), inst.get("panelPlus"), inst.get("antenna")
        wheel = inst.get("wheel")
        params = dict(BASELINE)
        params.update(
            mass=v(inst.get("structureMass"), kg),
            bodyLength=v(bus.get("bodyLength"), m),
            bodyWidth=v(bus.get("bodyWidth"), m),
            bodyHeight=v(bus.get("bodyHeight"), m),
            panelSpan=v(panel.get("span"), m),
            panelChord=v(panel.get("chord"), m),
            panelMass=v(panel.get("mass"), kg),
            antennaDiameter=v(ant.get("diameter"), m),
            antennaOffset=v(ant.get("offset"), m),
            antennaMass=v(ant.get("mass"), kg),
            orbitalRate=rd.read("environment.orbitalRate", "SI::rad/SI::s", loaded),
            maxTorque=v(inst.get("usableWheelTorque"), "SI::N*SI::m"),
            maxMomentum=v(wheel.get("maxMomentum"), "SI::N*SI::m*SI::s"),
            Kp=float(inst.get("controller").get("Kp")),
            Kd=float(inst.get("controller").get("Kd")),
        )
        return params

    def _sim_config(self, params: dict) -> SimConfig:
        sc = self.scenario
        return make_config(
            params,
            params["Kp"],
            params["Kd"],
            wheel={"maxTorque": params["maxTorque"], "maxMomentum": params["maxMomentum"]},
            t_end=sc["t_end_s"],
            initial_error_deg=sc["slew_deg"],
            max_step=sc["max_step_s"],
        )

    def _settling_time(self, sim: SimConfig, res) -> float:
        """The settling time of ``res`` by ``settling_time_method`` (module docstring)."""
        fraction = self.scenario["settling_fraction"]
        if self.settling_time_method == "steps":
            return _last_outside(res, fraction)
        threshold = fraction * _state_error_deg(np.array([*sim.q0, *sim.omega0]))
        entries, final = crossing_times(sim, {"settle": threshold})["settle"]
        return hold_time(entries, final, threshold, sim.t_span[1])

    def _measure_slew(self, params: dict) -> dict:
        """Integrate the slew with ``adcs_sim.simulate_adcs`` (the measurement of record)."""
        sc = self.scenario
        sim = self._sim_config(params)
        res = simulate_adcs(sim)
        summ = res.summary()
        tau = np.linalg.norm(res.tau_ctrl, axis=1)
        return {
            "torque_squared_integral": float(np.trapezoid(tau**2, res.t)),
            "peak_torque": float(np.max(tau)),
            "peak_momentum": summ["peak_wheel_momentum"],
            "settling_time": self._settling_time(sim, res),
            "control_effort": summ["control_effort"],
            "torque_saturated_frac": summ["torque_saturated_frac"],
            "censored": bool(not np.any(_attitude_error_deg(res) < sc["band_deg"])),
        }

    def _analyse(self, loaded, symbol: str, measured: dict) -> dict:
        """The nine attributes by name: eight from the model's analysis, the settling time measured.

        The settling time is measured, not computed; the analysis neither receives nor returns
        it, and it enters the row unchanged.
        """
        u = self.reader.unit
        args = {
            "torqueSquaredIntegral": measured["torque_squared_integral"],
            "peakTorque": Quantity(measured["peak_torque"], u("SI::N*SI::m")),
            "peakMomentum": Quantity(measured["peak_momentum"], u("SI::N*SI::m*SI::s")),
            "controlEffort": Quantity(measured["control_effort"], u("SI::N*SI::m*SI::s")),
            "censored": measured["censored"],
        }
        out = loaded.run_analysis(
            f"{PACKAGE}::SlewExperiment", subject=symbol, named_arguments=args
        )
        computed = {
            name: _quantity_value(loaded, q, unit)
            for name, unit, q in zip(
                _COMPUTED_NAMES, _COMPUTED_UNITS, out.outputs["attributes"], strict=True
            )
        }
        return {"settling_time_s": measured["settling_time"], **computed}

    def _one(self, loaded, symbol: str, checker: FeasibilityChecker) -> dict:
        inst = loaded.instantiate(symbol)
        measured = self._measure_slew(self._parameters(inst, loaded))
        attrs = self._analyse(loaded, symbol, measured)
        flags = checker.flags(symbol, measured)
        w, kg = "SI::W", "SI::kg"

        def v(q, unit):
            return _quantity_value(loaded, q, unit)

        loss = loaded.eval(f"{PACKAGE}::SlewLossEnergy({measured['torque_squared_integral']:.17e})")
        out = {
            **attrs,
            "adcs_mass_kg": v(inst.get("adcsMass"), kg),
            **flags,
            "torque_saturated_frac": measured["torque_saturated_frac"],
            "peak_momentum_nms": measured["peak_momentum"],
            "panel_mass_kg": v(inst.get("panelPlus").get("mass"), kg),
            "battery_mass_kg": v(inst.get("battery").get("mass"), kg),
            "generated_power_w": v(inst.get("generatedPower"), w),
            "available_power_w": v(inst.get("availablePower"), w),
            "usable_torque_nm": v(inst.get("usableWheelTorque"), "SI::N*SI::m"),
            "slew_loss_energy_wh": v(loss, "SI::W*SI::h"),
        }
        return {k: out[k] for k in OUTPUT_NAMES}

    def evaluate_chunk(self, rows: list[dict]) -> list[dict]:
        """Measure ``rows`` (dicts with the design columns); one model load for the chunk."""
        for r in rows:
            self.validate(r)
        loaded, symbols = self._configure(rows)
        checker = FeasibilityChecker(loaded, PACKAGE)
        return [self._one(loaded, s, checker) for s in symbols]

    # -- the Oracle protocol -------------------------------------------------------------------
    def __call__(self, configuration: Mapping[str, float | str]) -> dict[str, float | bool]:
        """One configuration to the output keys (attributes, flags, auxiliary)."""
        row = {"design_id": 0, **{k: v for k, v in dict(configuration).items()}}
        return self.evaluate_chunk([row])[0]

    def evaluate(self, designs: pd.DataFrame) -> pd.DataFrame:
        """The designs, the measured and the scenario columns; rows in ``design_id`` order."""
        ordered = designs.sort_values("design_id").reset_index(drop=True)
        rows = [r.to_dict() for _, r in ordered.iterrows()]
        for r in rows:
            self.validate(r)
        chunks = [rows[i : i + CHUNK] for i in range(0, len(rows), CHUNK)]
        workers = self.workers
        if workers is None:
            workers = int(os.environ.get("EXPERIMENTS_WORKERS", max(1, (os.cpu_count() or 2) - 1)))
        if workers > 1 and len(chunks) > 1:
            spec = (
                self.model_text,
                self.scenario_name,
                self.gain_box_name,
                self.settling_time_method,
            )
            with mp.get_context("spawn").Pool(workers) as pool:
                parts = pool.map(_worker_chunk, [(spec, c) for c in chunks], chunksize=1)
        else:
            parts = [self.evaluate_chunk(c) for c in chunks]
        measured = pd.DataFrame([r for part in parts for r in part], columns=list(OUTPUT_NAMES))
        scenario = pd.DataFrame(
            {k: [self.scenario[k]] * len(ordered) for k in SCENARIO_COLUMNS}, index=ordered.index
        )
        return pd.concat([ordered, measured, scenario], axis=1)


_WORKER: dict = {}


def _worker_chunk(args):
    """Pool worker: its own client connection and oracle (never one inherited across a fork)."""
    (text, scenario, gain_box, method), rows = args
    key = (hash(text), scenario, gain_box, method)
    if key not in _WORKER:
        _WORKER.clear()
        _WORKER[key] = CubesatOracle(
            text, scenario, gain_box, workers=1, settling_time_method=method
        )
    return _WORKER[key].evaluate_chunk(rows)


# -- the factories definitions.py registers ----------------------------------------------------
def _model_text(experiment, root: Path | None = None) -> str:
    if not experiment.model_path:
        raise ValueError(f"{experiment.id}: the cubesat oracle needs a model_path")
    return (Path(root or lg.REPO_ROOT) / experiment.model_path).read_text()


def _names(experiment) -> tuple[str, str]:
    return experiment.scenario or "nominalSlew", experiment.gain_box or "aggressive"


def build(experiment, root: Path | None = None, workers: int | None = None) -> CubesatOracle:
    """The oracle for ``experiment`` (its model, scenario and gain box).

    The first call for an experiment classifies the model's design space with the solver
    (``exclusion.py``) and stores the record in ``experiment.inputs["exclusion"]``, which the
    runner copies into the ledger entry; a model variant in which no configuration is feasible
    raises ``ExcludedVariant`` and nothing is simulated.
    """
    text = _model_text(experiment, root)
    scenario, gain_box = _names(experiment)
    oracle = CubesatOracle(text, scenario, gain_box, workers=workers)
    if "exclusion" not in experiment.inputs:
        experiment.inputs["exclusion"] = exclusion_block(text, oracle.connection)
        if experiment.inputs["exclusion"]["variant_excluded"]:
            raise ExcludedVariant(
                f"{experiment.id}: no configuration of the model is feasible; not simulated"
            )
    return oracle


def build_sampler(experiment, root: Path | None = None) -> LogUniformSampler:
    """The sampler for ``experiment``: categoricals and log ranges read from its model."""
    scenario, gain_box = _names(experiment)
    oracle = CubesatOracle(_model_text(experiment, root), scenario, gain_box, workers=1)
    return LogUniformSampler(
        {"wheel_class": oracle.wheel_classes, "st_grade": oracle.tracker_grades},
        {k: oracle.ranges[k] for k in ("panel_span_m", "battery_wh", "Kp", "Kd")},
    )


class ExcludedVariant(RuntimeError):
    """The solver proved that no configuration of the model variant is feasible."""


def exclusion_block(model_text: str, connection=None) -> dict:
    """Classify the model's declared design space with the solver; the dict for the ledger entry.

    Each region of ``exclusion.design_space_regions`` is classified ``excluded`` (jointly
    unsatisfiable: not simulated), ``all-feasible`` or ``mixed`` (kept: every configuration is
    simulated and the flags are observations). ``excluded_regions`` lists what was excluded.
    """
    from . import exclusion as ex

    classes = ex.classify_regions(model_text, ex.design_space_regions(), connection=connection)
    records = [ex.exclusion_record(c) for c in classes]
    return {
        "engine": "solve",
        "policy": (
            "regions of the declared ranges are classified before simulation; a region proved "
            "infeasible is excluded, any other is kept and each design is simulated; the four "
            "flags are then observations of the measured slew, not the definition of feasibility"
        ),
        "regions": records,
        "excluded_regions": [r["region"]["name"] for r in records if r["excluded"]],
        "variant_excluded": ex.variant_excluded(classes),
        "verdicts": {r["region"]["name"]: r["verdict"] for r in records},
        "model_sha256": classes[0].model_sha256 if classes else None,
    }
