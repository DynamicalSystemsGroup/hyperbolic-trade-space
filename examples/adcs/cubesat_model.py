"""The illustrative cubesat model layer (WP4b): SysML configuration space, Python model test.

``cubesat_tradespace.sysml`` is the single source of truth for the configuration space and the
accounting; this module reads it through the ``opensysml`` client and holds no copy of its
numbers (no wheel or tracker tables, no ranges, no constants of the power or mass budgets):

* **configure**: ``CubesatModel.sample_designs`` draws concrete design variables (one
  ``SeedSequence`` child seed per design, so design ``i`` does not depend on ``n``; categorical
  choices from the enumerations, continuous ones log-uniform in the model's ranges) and
  ``CubesatModel.configure`` instantiates each as a ``part : Cubesat`` of the model (all designs of
  a call are assembled into one source text, loaded once);
* **account**: mass, panel and battery mass, generated and available power, usable wheel torque
  are the values of the model's ``calc def`` accounting, read from the instance;
* **measure**: ``CubesatModel.measure`` (or the module-level ``measure``) runs the unchanged
  simulator ``adcs_sim.simulate_adcs`` on the inertia the model implies, with the wheel torque
  capped by the available power, implements the cubesat pointing budget here (``adcs_sim.py`` is
  untouched), and has the model evaluate the energy accounting and verify its constraints.

Attributes returned by ``measure`` (S = smaller is better, L = larger is better), each with the
mechanism through which it depends on the design variables:

``settling_time_s`` (S): last time the slew error exceeds 1 % of its start. Panel span and
battery capacity raise the slew-axis inertia (panel mass and lever arm; battery mass in the bus),
which slows the slew; Kp and Kd set the response; the wheel class and the available power cap the
torque, which stretches the slew when the cap binds (more generated power -> larger panels ->
more torque but more inertia).
``pointing_error_deg`` (S): root-sum-square of the steady error ``4 (tau_gg + tau_dist) / Kp`` and
the star-tracker floor (grade). Inertia enters through the gravity-gradient torque; Kp lowers the
steady error; a finer tracker lowers the floor.
``total_mass_kg`` (S): the model's mass accounting: bus + battery + two panels + antenna + three
wheels + tracker + IMU, so it grows with span, capacity, wheel class and tracker grade.
``control_effort`` (S): integral of the norm of the control torque over the horizon, from the
simulation (gains, inertia, torque cap).
``power_margin_w`` (L): generated power minus housekeeping minus the peak slew draw (wheels and
sensors). Grows with panel span, falls with the tracker grade and with the peak torque the gains
and wheel class allow.
``energy_balance_wh`` (L): orbit-average surplus: generation over the sunlit arc minus the base
load over the orbit minus the slew loss energy. Grows with span, falls with the tracker grade.
``eclipse_reserve_wh`` (L): usable battery energy (capacity x maximum depth of discharge) minus the
eclipse demand. Grows with battery capacity, falls with the tracker grade and slew loss energy.
``peak_slew_power_w`` (S): peak electrical power of wheels and sensors during the slew; grows with
the peak torque (a large wheel with high gains) and the tracker grade.
``dod_eclipse`` (S): eclipse demand divided by battery capacity; falls with capacity.

Flags: ``settled``, ``momentum_ok`` (peak wheel momentum within the class maximum),
``torque_saturated_frac`` (as in WP4), ``power_ok`` and ``dod_ok`` (the model's constraints,
verified per concrete configuration). Scenario numbers (slew angle, horizon, step) are
parameters of ``measure``, not model constants. All numbers are illustrative.
"""

from __future__ import annotations

import atexit
import os
import pathlib
from collections.abc import Mapping
from dataclasses import dataclass, field

import numpy as np
import opensysml
import pandas as pd
from adcs_sim import BASELINE, GG_THETA_MAX_RAD, inertia_tensor, make_config, simulate_adcs
from opensysml.values import Quantity

MODEL_PATH = pathlib.Path(__file__).resolve().parent / "cubesat_tradespace.sysml"
PKG = "CubesatTradeSpace"

# Scenario defaults (not model constants): 90 degree slew about X, horizon 450 s, step 0.5 s
# (adjustment 3 of the WP4b record in docs/superpowers/notes/adcs-tensions-probe.md).
SLEW_DEG = 90.0
T_END = 450.0
MAX_STEP = 0.5

DESIGN_COLUMNS = [
    "design_id",
    "seed",
    "wheel_class",
    "st_grade",
    "panel_span_m",
    "battery_wh",
    "Kp",
    "Kd",
]


class OpenSysMLUnavailable(RuntimeError):
    """The opensysml client could not start; the message names the cause."""


_CONNECTION = None


def get_connection():
    """One client connection per process; fails with a message naming the cause.

    Causes: service binary unavailable (``OPENSYSML_BINARY`` bad, or no binary and no network),
    download failed (network), checksum mismatch (corrupted download), trust failure (signature
    verification of the release failed or sigstore is unavailable).
    """
    global _CONNECTION
    if _CONNECTION is not None:
        return _CONNECTION
    try:
        _CONNECTION = opensysml.connect()
    except opensysml.SigstoreUnavailableError as exc:
        raise OpenSysMLUnavailable(
            f"opensysml trust failure (sigstore unavailable): {exc}"
        ) from exc
    except (opensysml.UnsignedReleaseError, opensysml.ManifestSignatureError) as exc:
        raise OpenSysMLUnavailable(f"opensysml trust failure (release signature): {exc}") from exc
    except opensysml.ChecksumMismatchError as exc:
        raise OpenSysMLUnavailable(f"opensysml download failed (checksum mismatch): {exc}") from exc
    except Exception as exc:
        where = os.environ.get("OPENSYSML_BINARY")
        cause = (
            f"service binary unavailable (OPENSYSML_BINARY={where})"
            if where
            else "service binary unavailable or download failed"
        )
        raise OpenSysMLUnavailable(f"opensysml {cause}: {type(exc).__name__}: {exc}") from exc
    atexit.register(_CONNECTION.close)
    return _CONNECTION


def _literal(value) -> str:
    """Enumeration literal name from a client EnumLiteral (``WheelClass::small`` -> ``small``)."""
    return (value.name or value.literal_id).split("::")[-1]


def _num(x: float) -> str:
    """A lossless SysML real literal."""
    return f"{float(x):.17e}"


@dataclass
class Alternative:
    """A concrete part definition selected by one enumeration literal, with its attribute table."""

    literal: str
    part_def: str
    values: dict = field(default_factory=dict)


@dataclass
class Configuration:
    """One concrete configuration: a ``part : Cubesat`` of the loaded model, instantiated."""

    design: dict
    symbol: str
    model: object
    instance: object


class CubesatModel:
    """The loaded SysML model plus everything the Python layer reads from it."""

    def __init__(self, source: str, connection=None):
        self.source = source
        self.connection = connection if connection is not None else get_connection()
        self.model = self.connection.load_from_content(source, strict=True)
        self._units: dict[str, object] = {}
        self.engine = self._evaluation_engine()
        self._read_structure()

    @classmethod
    def from_path(cls, path=MODEL_PATH, connection=None) -> CubesatModel:
        return cls(pathlib.Path(path).read_text(), connection)

    def _evaluation_engine(self) -> str:
        """The name of a ready engine that answers ``evaluate`` questions, from ``list_engines``."""
        for info in self.connection.list_engines():
            if info.ready and "evaluate" in info.answers:
                return info.name
        raise OpenSysMLUnavailable("no ready opensysml engine answers 'evaluate' questions")

    # -- units and values ---------------------------------------------------------------------
    def unit(self, expression: str):
        """A client Unit built by the model's own evaluator, e.g. ``"SI::W*SI::h"``."""
        if expression not in self._units:
            self._units[expression] = self.model.eval(f"1.0 [{expression}]").unit
        return self._units[expression]

    def value(self, quantity, unit_expression: str | None = None) -> float:
        """A feature value as a float: a Quantity converted to ``unit_expression``."""
        if isinstance(quantity, Quantity):
            if unit_expression is None:
                raise ValueError("a unit expression is required for a quantity")
            return float(quantity.in_unit(self.unit(unit_expression)))
        return float(quantity)

    def _eval_value(self, expression: str, unit_expression: str | None = None) -> float:
        out = self.model.eval(expression)
        if isinstance(out, list):
            out = out[0]
        return self.value(out, unit_expression)

    # -- structure read from the model --------------------------------------------------------
    def _read_structure(self) -> None:
        m = self.model
        ds = f"{PKG}::designSpace"
        self.panel_span_range = (
            self._eval_value(f"{ds}.panelSpanMin", "SI::m"),
            self._eval_value(f"{ds}.panelSpanMax", "SI::m"),
        )
        self.battery_wh_range = (
            self._eval_value(f"{ds}.batteryCapacityMin", "SI::W*SI::h"),
            self._eval_value(f"{ds}.batteryCapacityMax", "SI::W*SI::h"),
        )
        self.kp_range = (self._eval_value(f"{ds}.KpMin"), self._eval_value(f"{ds}.KpMax"))
        self.kd_range = (self._eval_value(f"{ds}.KdMin"), self._eval_value(f"{ds}.KdMax"))
        self.wheel_classes = [c.name for c in m.find(f"{PKG}::WheelClass").children()]
        self.tracker_grades = [c.name for c in m.find(f"{PKG}::TrackerGrade").children()]
        self.wheels = self._alternatives("ReactionWheel", "wheelClass", self.wheel_classes)
        self.trackers = self._alternatives("StarTracker", "grade", self.tracker_grades)

    def _alternatives(self, abstract: str, enum_attr: str, literals: list[str]) -> dict:
        """Concrete specializations of an abstract part def, keyed by their enumeration literal."""
        target = f"{PKG}::{abstract}"
        table = {}
        for q in self.model.query(
            scope=[PKG], where={"property": "@type", "operator": "=", "value": "PartDefinition"}
        ):
            sym = self.model.find(q.id)
            if not any(sp.target_id == target for sp in sym.specializations):
                continue
            inst = self.model.instantiate(q.id)
            lit = _literal(inst.get(enum_attr))
            table[lit] = Alternative(lit, q.id, {})
        missing = [lit for lit in literals if lit not in table]
        if missing:
            raise ValueError(f"enum literals of {abstract} without a part definition: {missing}")
        return {lit: table[lit] for lit in literals}

    # -- configure -----------------------------------------------------------------------------
    def sample_designs(self, n: int, seed: int = 0) -> pd.DataFrame:
        """Draw ``n`` designs from the model's enumerations and ranges, one child seed each.

        Design ``i`` depends only on ``(seed, i)``, not on ``n``. Categorical variables are
        uniform over the enumeration literals; continuous ones are log-uniform in the ranges.
        """
        children = np.random.SeedSequence(int(seed)).spawn(n)
        child_seeds = [int(c.generate_state(1, dtype=np.uint64)[0] >> 2) for c in children]
        rows = []
        for i, cs in enumerate(child_seeds):
            g = np.random.default_rng(cs)
            w = self.wheel_classes[g.integers(len(self.wheel_classes))]
            s = self.tracker_grades[g.integers(len(self.tracker_grades))]
            rows.append(
                {
                    "design_id": i,
                    "seed": cs,
                    "wheel_class": w,
                    "st_grade": s,
                    "panel_span_m": float(np.exp(g.uniform(*np.log(self.panel_span_range)))),
                    "battery_wh": float(np.exp(g.uniform(*np.log(self.battery_wh_range)))),
                    "Kp": float(np.exp(g.uniform(*np.log(self.kp_range)))),
                    "Kd": float(np.exp(g.uniform(*np.log(self.kd_range)))),
                }
            )
        return pd.DataFrame(rows, columns=DESIGN_COLUMNS)

    def configure(self, designs) -> list[Configuration]:
        """Instantiate each design as a ``Cubesat`` of the model (one load per call)."""
        rows = (
            [r.to_dict() for _, r in designs.iterrows()]
            if isinstance(designs, pd.DataFrame)
            else [dict(d) for d in designs]
        )
        usages = []
        for r in rows:
            wheel = self.wheels[r["wheel_class"]].part_def
            tracker = self.trackers[r["st_grade"]].part_def
            usages.append(
                f"    part cfg_{int(r['design_id'])} : {PKG}::Cubesat {{\n"
                f"        :>> panelSpan default = {_num(r['panel_span_m'])} [SI::m];\n"
                f"        :>> batteryCapacity default = {_num(r['battery_wh'])} [SI::W*SI::h];\n"
                f"        part :>> wheel : {wheel};\n"
                f"        part :>> tracker : {tracker};\n"
                f"        part :>> controller {{ :>> Kp default = {_num(r['Kp'])};"
                f" :>> Kd default = {_num(r['Kd'])}; }}\n"
                f"    }}\n"
            )
        text = self.source + "\npackage Configurations {\n" + "".join(usages) + "}\n"
        loaded = self.connection.load_from_content(text, strict=True)
        return [
            Configuration(
                r,
                sym := f"Configurations::cfg_{int(r['design_id'])}",
                loaded,
                loaded.instantiate(sym),
            )
            for r in rows
        ]

    def baseline(self) -> Configuration:
        """The model's own ``cubesatBaseline`` configuration."""
        sym = f"{PKG}::cubesatBaseline"
        return Configuration({"design_id": -1}, sym, self.model, self.model.instantiate(sym))

    # -- account and measure -------------------------------------------------------------------
    def _calc(self, cfg: Configuration, expression: str, unit_expression: str) -> float:
        out = cfg.model.eval(f"{PKG}::{expression}")
        return self.value(out[0] if isinstance(out, list) else out, unit_expression)

    def accounting(self, cfg: Configuration) -> dict:
        """Mass and power accounting values of a configuration, as read from the instance."""
        i = cfg.instance
        v = self.value
        return {
            "total_mass_kg": v(i.get("totalMass"), "SI::kg"),
            "structure_mass_kg": v(i.get("structureMass"), "SI::kg"),
            "panel_mass_kg": v(i.get("panelPlus").get("mass"), "SI::kg"),
            "battery_mass_kg": v(i.get("battery").get("mass"), "SI::kg"),
            "generated_power_w": v(i.get("generatedPower"), "SI::W"),
            "available_power_w": v(i.get("availablePower"), "SI::W"),
            "usable_torque_nm": v(i.get("usableWheelTorque"), "SI::N*SI::m"),
        }

    def sim_params(self, cfg: Configuration) -> dict:
        """The parameters of the existing inertia model, taken from the configuration."""
        i, v = cfg.instance, self.value
        bus, panel, ant = i.get("bus"), i.get("panelPlus"), i.get("antenna")
        wheel, tracker, imu = i.get("wheel"), i.get("tracker"), i.get("imu")
        acc = self.accounting(cfg)
        params = dict(BASELINE)
        params.update(
            mass=acc["structure_mass_kg"],
            bodyLength=v(bus.get("bodyLength"), "SI::m"),
            bodyWidth=v(bus.get("bodyWidth"), "SI::m"),
            bodyHeight=v(bus.get("bodyHeight"), "SI::m"),
            panelSpan=v(panel.get("span"), "SI::m"),
            panelChord=v(panel.get("chord"), "SI::m"),
            panelMass=acc["panel_mass_kg"],
            antennaDiameter=v(ant.get("diameter"), "SI::m"),
            antennaOffset=v(ant.get("offset"), "SI::m"),
            antennaMass=v(ant.get("mass"), "SI::kg"),
            orbitalRate=self._eval_value(f"{PKG}::environment.orbitalRate", "SI::rad/SI::s"),
            maxTorque=acc["usable_torque_nm"],
            maxMomentum=v(wheel.get("maxMomentum"), "SI::N*SI::m*SI::s"),
            wheelMass=v(wheel.get("mass"), "SI::kg"),
            stAccuracy=v(tracker.get("accuracy"), "SI::arcsec"),
            stMass=v(tracker.get("mass"), "SI::kg"),
            imuMass=v(imu.get("mass"), "SI::kg"),
            Kp=float(i.get("controller").get("Kp")),
            Kd=float(i.get("controller").get("Kd")),
        )
        return params

    def pointing_error_deg(self, params: dict) -> float:
        """Cubesat pointing budget: the WP4 form with the cubesat inertia, rate and disturbance.

        ``theta_ss = 4 (tau_gg + tau_dist) / Kp``; the total is the root-sum-square of ``theta_ss``
        and the star-tracker floor ``stAccuracy / 3600`` degrees.
        """
        jx, jy, jz = inertia_tensor(params)
        n = params["orbitalRate"]
        tau_gg = 3 * n**2 * max(abs(jz - jy), abs(jz - jx)) * GG_THETA_MAX_RAD
        tau_dist = self._eval_value(f"{PKG}::environment.disturbanceTorque", "SI::N*SI::m")
        theta_ss_deg = float(np.degrees(4 * (tau_gg + tau_dist) / params["Kp"]))
        return float(np.hypot(theta_ss_deg, params["stAccuracy"] / 3600.0))

    def measure(
        self,
        configuration,
        t_end: float = T_END,
        max_step: float = MAX_STEP,
        slew_deg: float = SLEW_DEG,
    ) -> dict:
        """The model test: configuration in, attributes and flags out (see the module docstring)."""
        cfg = (
            configuration
            if isinstance(configuration, Configuration)
            else self.configure([configuration])[0]
        )
        acc = self.accounting(cfg)
        params = self.sim_params(cfg)
        sim = make_config(
            params,
            params["Kp"],
            params["Kd"],
            wheel={"maxTorque": params["maxTorque"], "maxMomentum": params["maxMomentum"]},
            t_end=t_end,
            initial_error_deg=slew_deg,
            max_step=max_step,
        )
        res = simulate_adcs(sim)
        summ = res.summary()
        tau = np.linalg.norm(res.tau_ctrl, axis=1)
        tau2_integral = float(np.trapezoid(tau**2, res.t))
        peak_torque = float(np.max(tau))
        energy_j = self._eval_value(f"{PKG}::SlewLossEnergy({_num(tau2_integral)})", "SI::J")
        j, wh = "SI::J", "SI::W*SI::h"
        ctx = f"{cfg.symbol}, {_num(energy_j)} [SI::J]"
        adcs_mass = (
            int(cfg.instance.get("wheelCount")) * params["wheelMass"]
            + params["stMass"]
            + params["imuMass"]
        )
        power_ok = self._holds(cfg, f"{PKG}::Cubesat::powerOk")
        dod_ok = self._holds(
            cfg,
            f"{PKG}::Cubesat::dodOk",
            named_arguments={"slewEnergy": Quantity(energy_j, self.unit(j))},
        )
        return {
            "settling_time_s": summ["settling_time_s"],
            "pointing_error_deg": self.pointing_error_deg(params),
            "total_mass_kg": acc["total_mass_kg"],
            "adcs_mass_kg": adcs_mass,
            "control_effort": summ["control_effort"],
            "power_margin_w": self._calc(
                cfg, f"PowerMargin({cfg.symbol}, {_num(peak_torque)} [SI::N*SI::m])", "SI::W"
            ),
            "energy_balance_wh": self._calc(cfg, f"EnergyBalance({ctx})", wh),
            "eclipse_reserve_wh": self._calc(cfg, f"EclipseReserve({ctx})", wh),
            "peak_slew_power_w": self._calc(
                cfg, f"PeakSlewPower({cfg.symbol}, {_num(peak_torque)} [SI::N*SI::m])", "SI::W"
            ),
            "dod_eclipse": self._dod(cfg, ctx),
            "settled": bool(summ["settling_time_s"] < t_end),
            "momentum_ok": bool(summ["peak_wheel_momentum"] <= params["maxMomentum"]),
            "torque_saturated_frac": summ["torque_saturated_frac"],
            "power_ok": power_ok,
            "dod_ok": dod_ok,
            "peak_momentum_nms": summ["peak_wheel_momentum"],
            "panel_mass_kg": acc["panel_mass_kg"],
            "battery_mass_kg": acc["battery_mass_kg"],
            "generated_power_w": acc["generated_power_w"],
            "available_power_w": acc["available_power_w"],
            "usable_torque_nm": acc["usable_torque_nm"],
            "slew_loss_energy_wh": self.value(Quantity(energy_j, self.unit(j)), wh),
        }

    def _dod(self, cfg: Configuration, ctx: str) -> float:
        out = cfg.model.eval(f"{PKG}::DepthOfDischarge({ctx})")
        return float(out[0] if isinstance(out, list) else out)

    def _holds(self, cfg: Configuration, constraint: str, **kw) -> bool:
        verdict = cfg.model.verify_constraint(
            constraint, subject=cfg.symbol, engine=self.engine, **kw
        )
        if verdict.error:
            raise RuntimeError(f"verification of {constraint} failed: {verdict.error}")
        return bool(verdict.holds)

    def evaluate_designs(self, designs, **kw) -> pd.DataFrame:
        """Configure and measure every design; the designs joined with their measurements."""
        configs = self.configure(designs)
        meas = pd.DataFrame([self.measure(c, **kw) for c in configs])
        base = pd.DataFrame([c.design for c in configs])
        return pd.concat([base, meas], axis=1)


_DEFAULT: CubesatModel | None = None


def load_model(path=MODEL_PATH, connection=None) -> CubesatModel:
    """Load the model once per process (the default model is cached); fails with a named cause."""
    global _DEFAULT
    if path == MODEL_PATH and connection is None:
        if _DEFAULT is None:
            _DEFAULT = CubesatModel.from_path(path)
        return _DEFAULT
    return CubesatModel.from_path(path, connection)


def sample_designs(n: int, seed: int = 0, model: CubesatModel | None = None) -> pd.DataFrame:
    """Sample ``n`` designs from the model's enumerations and ranges."""
    return (model or load_model()).sample_designs(n, seed)


def measure(configuration: Mapping | Configuration, model: CubesatModel | None = None, **kw):
    """The model test: ``measure(configuration)`` -> attributes and flags (module docstring)."""
    return (model or load_model()).measure(configuration, **kw)
