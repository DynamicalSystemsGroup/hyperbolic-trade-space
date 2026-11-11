# ruff: noqa: E501
"""Exclude infeasible regions and model variants before any simulation (WP15 15.2, the solver side).

A region of the configuration space (a battery capacity range, a wheel class with a range of
inertias on the nominal slew, a panel span range) is stated as a box over scalar variables. With the
model's constants read from the model, the feasibility condition of that region is restated over
the same scalars, and the opensysml ``solve`` engine (z3) is asked two questions about two
constraint definitions appended to the model's text::

    <stem>Sat    (region) and (condition)           question ``satisfiable``
    <stem>Holds  (region) implies (condition)       question ``holds``

* ``excluded``: ``Sat`` is ``unsatisfiable`` (proved): no configuration of the region is feasible, so
  none is simulated;
* ``all-feasible``: ``Holds`` is ``holds`` (proved): every configuration of the region is feasible;
* ``mixed``: ``Sat`` is ``satisfiable`` and ``Holds`` is ``violated``: keep the region and test each
  point (the model's requirements, ``feasibility.py``).

A model variant is the model's text with alternative literal ranges or constants
(``model_variant``); the same classification of its whole design space (``design_space_regions``)
excludes a variant in which no configuration is feasible. ``exclusion_record`` turns a
classification into the dict a ledger entry stores: the region, the claim, the engine, the verdict,
the evidence strength and the witness.

Basis of each condition. ``power`` and ``depth_of_discharge`` restate the model's accounting
exactly (``PowerRequirement`` and ``DepthOfDischargeRequirement`` before the slew energy is known;
the slew energy enters as a stated range, default zero). ``momentum`` restates the closed-form
bang-bang peak momentum ``sqrt(torque * angle * inertia)`` against the wheel class capacity (the OD2
approximation): the ODE overshoots it, so ``excluded`` is a necessary-condition result that the
simulation confirms, and ``all-feasible`` means feasible by the closed form, not by the ODE.

The solver needs ``z3`` (or ``cvc5``) on ``PATH``; without it ``SolverUnavailable`` is raised.
"""

from __future__ import annotations

import hashlib
import math
import os
import os
import re
import shutil
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

CONDITIONS = ("power", "depth_of_discharge", "momentum")
BASIS = {
    "power": "exact accounting (PowerRequirement)",
    "depth_of_discharge": "exact accounting (DepthOfDischargeRequirement), slew energy as stated",
    "momentum": "closed-form bang-bang momentum sqrt(torque*angle*inertia) (OD2 approximation)",
}
VERDICTS = ("excluded", "all-feasible", "mixed", "undecided")


class SolverUnavailable(RuntimeError):
    """The ``solve`` engine needs ``z3`` or ``cvc5`` on ``PATH``; none was found."""


def solver_available() -> bool:
    """Whether ``z3`` or ``cvc5`` can be run, putting the ``z3-solver`` wheel's directory on ``PATH`` if needed.

    The wheel installs its executable as ``<prefix>/bin/z3`` (``z3.exe`` on Windows), and a virtual
    environment on Windows puts only ``Scripts`` on ``PATH``; the engine finds the solver by ``PATH``,
    so the directory is added to this process's ``PATH`` when it is the only place the solver is.
    """
    if shutil.which("z3") or shutil.which("cvc5"):
        return True
    wheel_bin = Path(sys.prefix) / "bin"
    if shutil.which("z3", path=str(wheel_bin)):
        os.environ["PATH"] = str(wheel_bin) + os.pathsep + os.environ.get("PATH", "")
        return True
    return False


@dataclass(frozen=True)
class Region:
    """A box over the scalars of one feasibility condition.

    ``box`` maps a variable to ``(lo, hi)`` (``None`` means the model's own range). Variables:
    ``power``: ``span_m``, ``tracker_w``; ``depth_of_discharge``: ``capacity_wh``, ``tracker_w``,
    ``slew_energy_wh``; ``momentum``: ``inertia_kgm2`` (``wheel_class`` selects the table entry and
    ``torque_nm`` overrides the class maximum torque).
    """

    name: str
    condition: str
    box: Mapping[str, tuple[float, float] | None] = field(default_factory=dict)
    wheel_class: str | None = None
    torque_nm: float | None = None

    def __post_init__(self):
        if self.condition not in CONDITIONS:
            raise ValueError(f"condition must be one of {CONDITIONS}, got {self.condition!r}")
        for k, v in self.box.items():
            if v is not None and not v[0] <= v[1]:
                raise ValueError(f"region {self.name}: empty interval for {k}: {v}")


def power_region(span_m=None, tracker_w=None, *, name: str | None = None) -> Region:
    return Region(name or "power", "power", {"span_m": span_m, "tracker_w": tracker_w})


def battery_region(
    capacity_wh=None, tracker_w=None, slew_energy_wh=(0.0, 0.0), *, name: str | None = None
) -> Region:
    box = {"capacity_wh": capacity_wh, "tracker_w": tracker_w, "slew_energy_wh": slew_energy_wh}
    return Region(name or "battery", "depth_of_discharge", box)


def wheel_region(wheel_class: str, inertia_kgm2, *, torque_nm=None, name: str | None = None):
    return Region(
        name or f"wheel-{wheel_class}",
        "momentum",
        {"inertia_kgm2": tuple(inertia_kgm2)},
        wheel_class,
        torque_nm,
    )


def design_space_regions() -> list[Region]:
    """The model's whole design space, per condition that needs no extra input: for a variant.

    Power and depth of discharge only. The momentum condition is left out on purpose: it depends on
    the inertia, which depends on the panel span and the configuration, and it is the closed-form
    approximation (the ODE peak exceeds it), so an all-feasible verdict from it would claim more
    than the simulation gives. A wheel region can still be classified on its own
    (``wheel_region``), where ``excluded`` is a necessary-condition result.
    """
    return [power_region(name="design-space power"), battery_region(name="design-space battery")]


@dataclass(frozen=True)
class Classification:
    """The solver's answer for one region."""

    region: Region
    verdict: str
    claim: str
    satisfiable: tuple[str, str]  # (status, strength) of the conjunction
    holds: tuple[str, str]  # (status, strength) of the implication
    box: Mapping[str, tuple[float, float]]  # the resolved box
    witness_feasible: Mapping[str, float]
    witness_violation: Mapping[str, float]
    engine: str = "solve"
    model_sha256: str = ""

    @property
    def excluded(self) -> bool:
        return self.verdict == "excluded"


# -- reading the model ----------------------------------------------------------------------------
def _source(model_text_or_path) -> str:
    if isinstance(model_text_or_path, os.PathLike):
        return Path(model_text_or_path).read_text()
    text = str(model_text_or_path)
    if "\n" not in text and text.endswith(".sysml") and Path(text).exists():
        return Path(text).read_text()
    return text


def _package(text: str) -> str:
    m = re.search(r"^package\s+(\w+)", text, flags=re.M)
    if not m:
        raise ValueError("no package declaration in the model text")
    return m.group(1)


def _connection(connection=None):
    if connection is not None:
        return connection
    try:
        import cubesat_model

        return cubesat_model.get_connection()
    except ImportError:
        import opensysml

        return opensysml.connect()


def lit(x: float) -> str:
    return f"{float(x):.12g}"


class _Constants:
    """The model's numbers a condition needs, read with ``eval`` (none is a constant of this module)."""

    def __init__(self, model, package: str):
        self.model, self.pkg = model, package
        self.cache: dict[str, float] = {}

    def num(self, expression: str, unit: str | None = None, subject: str | None = None) -> float:
        key = f"{expression}|{unit}|{subject}"
        if key not in self.cache:
            m = self.model
            out = m.eval(expression, subject=subject) if subject else m.eval(expression)
            out = out[0] if isinstance(out, list) else out
            if hasattr(out, "in_unit"):
                out = out.in_unit(m.eval(f"1.0 [{unit}]").unit)
            self.cache[key] = float(out)
        return self.cache[key]

    def env(self, name: str, unit: str | None = None) -> float:
        return self.num(f"{self.pkg}::environment.{name}", unit)

    def baseline(self, expression: str, unit: str | None = None) -> float:
        return self.num(expression, unit, subject=f"{self.pkg}::cubesatBaseline")

    def alternatives(self, abstract: str, attr: str) -> dict[str, str]:
        """Concrete specializations of an abstract part def, keyed by their enumeration literal."""
        target, table = f"{self.pkg}::{abstract}", {}
        where = {"property": "@type", "operator": "=", "value": "PartDefinition"}
        for q in self.model.query(scope=[self.pkg], where=where):
            if any(sp.target_id == target for sp in self.model.find(q.id).specializations):
                literal = self.model.instantiate(q.id).get(attr)
                table[(literal.name or literal.literal_id).split("::")[-1]] = q.id
        return table

    def alt_value(self, symbol: str, attr: str, unit: str) -> float:
        q = self.model.instantiate(symbol).get(attr)
        q = q[0] if isinstance(q, list) else q
        return float(q.in_unit(self.model.eval(f"1.0 [{unit}]").unit))

    def tracker_power_range(self) -> tuple[float, float]:
        alts = self.alternatives("StarTracker", "grade").values()
        powers = [self.alt_value(s, "power", "SI::W") for s in alts]
        return min(powers), max(powers)

    def generation_per_span(self) -> float:
        """Generated power per metre of panel span, W/m: flux * efficiencies * two wings * chord."""
        eff = 1.0
        for k in ("cellEfficiency", "packingFactor", "degradation", "incidenceFactor"):
            eff *= self.env(k)
        flux = self.env("solarFlux", "SI::W/SI::m**2")
        inst = self.model.instantiate(f"{self.pkg}::cubesatBaseline")
        chord = inst.get("panelPlus").get("chord")
        chord = float((chord[0] if isinstance(chord, list) else chord).in_unit(self._unit("SI::m")))
        return flux * eff * 2.0 * chord

    def _unit(self, expression: str):
        return self.model.eval(f"1.0 [{expression}]").unit


def _resolve(region: Region, k: _Constants) -> dict[str, tuple[float, float]]:
    p = k.pkg
    span = (
        k.num(f"{p}::designRanges.panelSpanMin", "SI::m"),
        k.num(f"{p}::designRanges.panelSpanMax", "SI::m"),
    )
    cap = (
        k.num(f"{p}::designRanges.batteryCapacityMin", "SI::W*SI::h"),
        k.num(f"{p}::designRanges.batteryCapacityMax", "SI::W*SI::h"),
    )
    defaults = {
        "span_m": span,
        "capacity_wh": cap,
        "tracker_w": k.tracker_power_range(),
        "slew_energy_wh": (0.0, 0.0),
    }
    wanted = {
        "power": ("span_m", "tracker_w"),
        "depth_of_discharge": ("capacity_wh", "tracker_w", "slew_energy_wh"),
        "momentum": ("inertia_kgm2",),
    }[region.condition]
    out = {}
    for var in wanted:
        given = region.box.get(var)
        if given is None:
            if var not in defaults:
                raise ValueError(f"region {region.name}: {var} needs an interval")
            given = defaults[var]
        out[var] = (float(given[0]), float(given[1]))
    return out


def _between(var: str, lo: float, hi: float, unit: str) -> str:
    return f"{var} >= {lit(lo)} [{unit}] and {var} <= {lit(hi)} [{unit}]"


def _statement(region: Region, k: _Constants, box: dict) -> tuple[str, str, str]:
    """(parameters, assume, require) of the region's condition over scalar features."""
    wh = "SI::W*SI::h"
    if region.condition == "power":
        params = "in s : LengthValue; in t : PowerValue;"
        assume = f"{_between('s', *box['span_m'], 'SI::m')} and {_between('t', *box['tracker_w'], 'SI::W')}"
        hk = k.env("housekeepingLoad", "SI::W")
        require = f"{lit(k.generation_per_span())} [SI::W/SI::m] * s - {lit(hk)} [SI::W] - t > 0.0 [SI::W]"
    elif region.condition == "depth_of_discharge":
        params = "in cap : EnergyValue; in t : PowerValue; in e : EnergyValue;"
        assume = (
            f"{_between('cap', *box['capacity_wh'], wh)} and {_between('t', *box['tracker_w'], 'SI::W')}"
            f" and {_between('e', *box['slew_energy_wh'], wh)}"
        )
        hk = k.env("housekeepingLoad", "SI::W")
        idle = k.baseline("wheelCount") * k.env("wheelIdlePower", "SI::W")
        hours = k.env("eclipseDuration", "SI::h")
        dod = k.env("maxDepthOfDischarge")
        require = (
            f"({lit(hk)} [SI::W] + t + {lit(idle)} [SI::W]) * {lit(hours)} [SI::h] + e"
            f" <= {lit(dod)} * cap"
        )
    else:
        alts = k.alternatives("ReactionWheel", "wheelClass")
        if region.wheel_class not in alts:
            raise ValueError(
                f"unknown wheel class {region.wheel_class!r}; model has {sorted(alts)}"
            )
        sym = alts[region.wheel_class]
        tau = region.torque_nm
        if tau is None:
            tau = k.alt_value(sym, "maxTorque", "SI::N*SI::m")
        h = k.alt_value(sym, "maxMomentum", "SI::N*SI::m*SI::s")
        theta = math.radians(k.num(f"{k.pkg}::nominalSlew.slewAngle", "SI::degree"))
        params = "in inertia : MomentOfInertiaValue;"
        assume = _between("inertia", *box["inertia_kgm2"], "SI::kg*SI::m**2")
        require = (
            f"{lit(tau)} [SI::N*SI::m] * {lit(theta)} * inertia"
            f" <= {lit(h)} [SI::N*SI::m*SI::s] * {lit(h)} [SI::N*SI::m*SI::s]"
        )
    return params, assume, require


def _stem(i: int, region: Region) -> str:
    return f"Region{i}{region.condition.title().replace('_', '')}"


# witness values arrive in the runtime's base units (energies mJ, powers mW, mass g); the region's
# variables are reported in Wh, W, m and kg m^2.
_WITNESS = {
    "cap": ("capacity_wh", 1 / 3.6e6),
    "e": ("slew_energy_wh", 1 / 3.6e6),
    "t": ("tracker_w", 1e-3),
    "s": ("span_m", 1.0),
    "inertia": ("inertia_kgm2", 1e-3),
}


def _witness(v) -> dict[str, float]:
    out = {}
    for w in v.witness or []:
        val = w.value
        name, scale = _WITNESS.get(w.feature.split("::")[-1], (w.feature.split("::")[-1], 1.0))
        out[name] = float(f"{float(getattr(val, 'value', val)) * scale:.9g}")
    return out


def classify_regions(model_text_or_path, regions, *, connection=None) -> list[Classification]:
    """Classify ``regions`` against one model (a path or its text); one load for all of them."""
    if not solver_available():
        raise SolverUnavailable(
            "the solve engine needs z3 or cvc5 on PATH (the `case` dependency group installs "
            "z3-solver; run through `uv run`, or `uv run --with z3-solver`)"
        )
    text = _source(model_text_or_path)
    package = _package(text)
    conn = _connection(connection)
    digest = hashlib.sha256(text.encode()).hexdigest()
    constants = _Constants(conn.load_from_content(text, strict=True), package)
    body, defs, planned = text.rstrip(), "", []
    if not body.endswith("}"):
        raise ValueError("the model text must end with the closing brace of its package")
    for i, region in enumerate(regions):
        box = _resolve(region, constants)
        params, assume, require = _statement(region, constants, box)
        stem = _stem(i, region)
        defs += (
            f"\n    constraint def {stem}Sat {{ {params} ({assume}) and ({require}) }}"
            f"\n    constraint def {stem}Holds {{ {params} ({assume}) implies ({require}) }}"
        )
        planned.append((region, box, stem, f"{params} ({assume}) implies ({require})"))
    model = conn.load_from_content(body[:-1] + defs + "\n}\n", strict=True)
    out = []
    for region, box, stem, claim in planned:
        sat = model.verify_constraint(
            f"{package}::{stem}Sat", engine="solve", question="satisfiable"
        )
        hol = model.verify_constraint(f"{package}::{stem}Holds", engine="solve", question="holds")
        if sat.status == "unsatisfiable" and sat.strength == "proved":
            verdict = "excluded"
        elif hol.status == "holds" and hol.strength == "proved":
            verdict = "all-feasible"
        elif sat.status == "satisfiable" and hol.status == "violated":
            verdict = "mixed"
        else:
            verdict = "undecided"
        out.append(
            Classification(
                region=region,
                verdict=verdict,
                claim=claim,
                satisfiable=(sat.status, sat.strength),
                holds=(hol.status, hol.strength),
                box=box,
                witness_feasible=_witness(sat) if sat.status == "satisfiable" else {},
                witness_violation=_witness(hol) if hol.status == "violated" else {},
                model_sha256=digest,
            )
        )
    return out


def classify_region(model_text_or_path, region: Region, *, connection=None) -> Classification:
    """Classify one region: ``excluded``, ``all-feasible``, ``mixed`` (or ``undecided``)."""
    return classify_regions(model_text_or_path, [region], connection=connection)[0]


# -- model variants -------------------------------------------------------------------------------
def model_variant(model_text: str, edits: Mapping[str, str]) -> str:
    """The model text with alternative literals: each key occurs exactly once and is replaced."""
    text = model_text
    for old, new in edits.items():
        if text.count(old) != 1:
            raise ValueError(f"variant edit {old!r} matches {text.count(old)} times, expected 1")
        if old == new:
            raise ValueError(f"variant edit {old!r} changes nothing")
        text = text.replace(old, new)
    return text


def classify_variant(
    model_text_or_path, edits: Mapping[str, str], regions=None, *, connection=None
) -> list[Classification]:
    """Classify the design space of the variant ``edits`` makes of a model (all of it by default)."""
    variant = model_variant(_source(model_text_or_path), edits)
    return classify_regions(variant, regions or design_space_regions(), connection=connection)


def variant_excluded(classifications) -> bool:
    """A variant is excluded when some feasibility condition holds nowhere in its design space."""
    return any(c.excluded for c in classifications)


# -- the ledger record ----------------------------------------------------------------------------
def exclusion_record(
    classification: Classification, *, variant: Mapping[str, str] | None = None, note: str = ""
) -> dict:
    """What was excluded (or kept) and why, as a JSON-serialisable dict for a ledger entry."""
    c, r = classification, classification.region
    if c.verdict == "excluded":
        why = (
            f"no configuration in the region satisfies the {r.condition} condition: the region "
            "and the condition are jointly unsatisfiable (proved by the solve engine); none is simulated"
        )
    elif c.verdict == "all-feasible":
        why = f"every configuration in the region satisfies the {r.condition} condition (proved)"
    elif c.verdict == "mixed":
        why = "the region has feasible and infeasible configurations; kept, each point is tested"
    else:
        why = "the solver did not decide; the region is kept"
    return {
        "kind": "exclusion",
        "region": {
            "name": r.name,
            "condition": r.condition,
            "box": {k: list(v) for k, v in c.box.items()},
            "wheel_class": r.wheel_class,
            "torque_nm": r.torque_nm,
        },
        "claim": c.claim,
        "engine": c.engine,
        "verdict": c.verdict,
        "excluded": c.excluded,
        "satisfiable": list(c.satisfiable),
        "holds": list(c.holds),
        "witness_feasible": dict(c.witness_feasible),
        "witness_violation": dict(c.witness_violation),
        "witness_units": "the region variables' units (Wh, W, m, kg m^2)",
        "basis": BASIS[r.condition],
        "reason": why + (f" ({note})" if note else ""),
        "model_sha256": c.model_sha256,
        "variant": dict(variant) if variant else None,
    }
