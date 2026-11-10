"""The SysML-backed cubesat oracle and sampler (WP15 15.4): configuration to attributes and flags.

``CubesatOracle`` satisfies ``experiments.oracle.Oracle`` for the v2 model
(``model_v2/cubesat.sysml``). Nothing about the case is copied here: the design ranges, the
enumerations and their alternatives, the gain box, the scenario (slew angle, horizon, step, the
two bands, the settling fraction) and every accounting constant are read from the model, which is
also where the accounting, the attributes and the feasibility are computed:

* **configure**: each design becomes a ``Cubesat`` part of the loaded model (one load per chunk);
* **measure**: the unchanged ``adcs_sim.simulate_adcs`` integrates the slew (SysML cannot), on the
  parameters the configuration implies; the measured quantities are the only numbers that enter
  the model from Python;
* **account**: the model's ``analysis def SlewExperiment`` takes the measured quantities and
  returns the eight attributes it computes (the settling and slew times are measured and pass
  into the row unchanged);
* **feasibility**: the four flags are the verdicts of the model's named requirements
  (``feasibility.FeasibilityChecker``, engine ``run``, evidence ``observed``). They are
  observations of single configurations; the solver's classification of regions before simulation
  (``exclusion.py``) is recorded by ``build`` in the ledger entry.

The output keys are those of the frozen ``cubesat_model.measure``, in the frozen CSV column order,
followed by the scenario columns ``slew_deg``, ``t_end_s``, ``max_step_s`` that ``evaluate``
appends. Construction fails with ``cubesat_model.OpenSysMLUnavailable`` (a named cause) when the
runtime cannot start.

``build(experiment)`` and ``build_sampler(experiment)`` are the factories ``definitions.py``
registers; they read the model the experiment names (relative to the repository root).
"""

from __future__ import annotations

import multiprocessing as mp
import os
from collections.abc import Mapping
from pathlib import Path

import numpy as np
import pandas as pd
from adcs_sim import BASELINE, make_config, simulate_adcs
from opensysml.values import Quantity

from . import ledger as lg
from .feasibility import FeasibilityChecker
from .runner import LogUniformSampler

PACKAGE = "CubesatTradeSpaceV2"
CONFIG_NAMES = ("panel_span_m", "battery_wh", "wheel_class", "st_grade", "Kp", "Kd")
ATTRIBUTE_NAMES = (
    "settling_time_s",
    "slew_time_s",
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
# unit; the settling and slew times are measured and enter the row from the measurement
_COMPUTED_NAMES = ATTRIBUTE_NAMES[2:]
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
# the keys of the frozen ``cubesat_model.measure``, in order (the frozen CSV columns after Kd)
OUTPUT_NAMES = (
    "settling_time_s",
    "slew_time_s",
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
    "slew_time_05deg_s",
    "slew_loss_energy_wh",
)
SCENARIO_COLUMNS = ("slew_deg", "t_end_s", "max_step_s")
DESIGN_COLUMNS = ("design_id", "seed", "wheel_class", "st_grade", *CONFIG_NAMES[:2], "Kp", "Kd")
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
                "band_sensitivity_deg": r(f"{name}.slewBandSensitivity", "SI::degree"),
                "settling_fraction": r(f"{name}.settlingFraction"),
            }
        except Exception as exc:
            raise ScenarioError(f"scenario {name!r}: the model declares no such part") from exc


def _attitude_error_deg(res) -> np.ndarray:
    return np.degrees(2 * np.linalg.norm(res.q[:, :3], axis=1))


def _first_inside(res, band_deg: float) -> float:
    """First time the attitude error falls below the band; the last time (censored) if never."""
    inside = np.flatnonzero(_attitude_error_deg(res) < band_deg)
    return float(res.t[inside[0]] if len(inside) else res.t[-1])


def _last_outside(res, fraction: float) -> float:
    """Last time the error exceeds ``fraction`` of its start (the settling time)."""
    err = _attitude_error_deg(res)
    if err[0] <= 0:
        return 0.0
    outside = np.flatnonzero(err > fraction * err[0])
    return float(res.t[outside[-1] if len(outside) else 0])


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
    ):
        if connection is None:
            import cubesat_model as cm

            connection = cm.get_connection()
        self.model_text = model_text
        self.scenario_name, self.gain_box_name = scenario, gain_box
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

    def _measure_slew(self, params: dict) -> dict:
        """Integrate the slew with ``adcs_sim.simulate_adcs`` (the measurement of record)."""
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
        res = simulate_adcs(sim)
        summ = res.summary()
        tau = np.linalg.norm(res.tau_ctrl, axis=1)
        return {
            "torque_squared_integral": float(np.trapezoid(tau**2, res.t)),
            "peak_torque": float(np.max(tau)),
            "peak_momentum": summ["peak_wheel_momentum"],
            "settling_time": _last_outside(res, sc["settling_fraction"]),
            "slew_time": _first_inside(res, sc["band_deg"]),
            "slew_time_sensitivity": _first_inside(res, sc["band_sensitivity_deg"]),
            "control_effort": summ["control_effort"],
            "torque_saturated_frac": summ["torque_saturated_frac"],
            "censored": bool(not np.any(_attitude_error_deg(res) < sc["band_deg"])),
        }

    def _analyse(self, loaded, symbol: str, measured: dict) -> dict:
        """The ten attributes by name: eight from the model's analysis, two from the measurement.

        The settling time and the slew time are measured, not computed; the analysis neither
        receives nor returns them, and they enter the row unchanged.
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
        return {
            "settling_time_s": measured["settling_time"],
            "slew_time_s": measured["slew_time"],
            **computed,
        }

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
            "slew_time_05deg_s": measured["slew_time_sensitivity"],
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
        """One configuration to the frozen ``measure`` keys (attributes, flags, auxiliary)."""
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
            spec = (self.model_text, self.scenario_name, self.gain_box_name)
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
    (text, scenario, gain_box), rows = args
    key = (hash(text), scenario, gain_box)
    if key not in _WORKER:
        _WORKER.clear()
        _WORKER[key] = CubesatOracle(text, scenario, gain_box, workers=1)
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
