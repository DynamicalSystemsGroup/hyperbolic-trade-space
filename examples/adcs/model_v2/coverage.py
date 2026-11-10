"""The coverage table of the cubesat model (WP23 D-2): decision elements against traded metrics.

Two tables, written to ``views/coverage.md`` and ``views/coverage.csv`` from the model:

1. **Decision element x traded metric.** The decision elements are the configuration variables the
   assembly view marks: the swaps (an abstract part whose alternatives an enumeration selects:
   ``WheelClass``, ``TrackerGrade``) and the tunes (an attribute stated with ``default``:
   ``panelSpan``, ``batteryCapacity``, ``Kp``, ``Kd``). The *structural* column walks the model
   through the opensysml client, from each traded metric (the analysis's return entry, or the
   measurement attribute the analysis passes through) back through the calc definitions it invokes,
   the attributes those read on the configuration, the redefinitions that bind a part's attribute to
   a root variable, and the measurement's stated simulator inputs, to the configuration variables.
   The *empirical* column changes each decision element one at a time at the three named
   configurations of the model and counts an effect when a metric moves by more than ``EFFECT``
   relative. A cell where the two columns disagree is a finding (listed under the table and in
   ``work-packages/WP23-review.md``).

2. **Traded metric -> MoE or MoP, requirement, verification.** The mark is the first word of the
   ``doc`` on the metric's element; the requirement is the one whose constraint reads the metric's
   own quantity (its calc, its measurement attribute, or the attribute through the MoE calc that
   reads it); the verification case is the one whose objective verifies that requirement.

3. **Coupling between subsystems, as a design structure matrix.** The configuration values feed the
   subsystems' calcs; the subsystems exchange named coupling variables (the pack mass from the power
   subsystem to the mass accounting, the inertia and the structure mass from the mass accounting to
   the slew, the usable torque from the power subsystem to the slew, the peak torque and the
   integral of the squared torque from the slew back to the power subsystem); the metrics and the
   requirements are read off the subsystems. The three subsystems are the CaseSpec's (the
   behavioural view's); the placement of each calc in one of them is the analyst's decomposition,
   stated once in ``SUBSYSTEM_OF``; every edge is read from the model (``Coupling``). The test is
   connectivity: every configuration value feeds a subsystem and reaches a traded metric (the
   structural column of table 1), every metric is read off a subsystem, and the graph is connected.

The empirical column runs the slews through the case's oracle (``experiments.cubesat_oracle``)
on the same model text, and the table says which model text the oracle ran. Nothing numeric about
the case is typed here: ranges, enumerations, the named configurations and every effect are read
from the model or measured through the oracle. The column names of the dataset (the interface
contract's) name the oracle's outputs.

    uv run python examples/adcs/model_v2/coverage.py [--model PATH] [--out DIR] [--no-empirical]

Default model: ``cubesat.sysml`` beside this file (the adopted model since WP23's data gate);
default output directory: ``views/`` beside this file. Three runs on one machine give byte-identical
files; the committed files are generated in the container of record (``paper/container/README.md``),
because the slew's measured quantities, the settling time above all (read on the integrator's time
grid), differ between platforms beyond the two digits the tables print.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import pathlib
import re
import sys
import warnings
from dataclasses import dataclass, field

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_MODEL = HERE / "cubesat.sysml"
DEFAULT_OUT = HERE / "views"
PACKAGE = "CubesatTradeSpaceV2"
EFFECT = 1e-9  # relative change below which a metric is said not to move
TUNE_FACTOR = 1.1  # the one-at-a-time change of a tune (or its inverse at the top of a range)
MARKS = ("MoE", "MoP")
# the dataset column (interface contract) that carries each traded metric, by the metric's name
METRIC_COLUMNS = {
    "settling time": "settling_time_s",
    "pointing error": "pointing_error_deg",
    "total mass": "total_mass_kg",
    "control effort": "control_effort",
    "power margin": "power_margin_w",
    "energy balance": "energy_balance_wh",
    "eclipse reserve": "eclipse_reserve_wh",
    "peak slew power": "peak_slew_power_w",
    "depth of discharge": "dod_eclipse",
}
# the oracle's configuration keys for the model's decision elements
ORACLE_KEYS = {
    "WheelClass": "wheel_class",
    "TrackerGrade": "st_grade",
    "panelSpan": "panel_span_m",
    "batteryCapacity": "battery_wh",
    "Kp": "Kp",
    "Kd": "Kd",
}


def plain(name: str) -> str:
    """``PointingError`` or ``pointingError`` -> ``pointing error``."""
    return re.sub(r"(?<!^)(?=[A-Z])", " ", name).lower()


def ref(x):
    return x["@id"] if isinstance(x, dict) else x


def short(qn: str) -> str:
    return qn.split("::")[-1].split("__")[-1]


# =================================================================================================
# The model, read through the client
# =================================================================================================
class ModelGraph:
    """The model's elements by id (``to_api_json``) and the reads the coverage walk makes."""

    def __init__(self, text: str, package: str = PACKAGE):
        import opensysml

        warnings.simplefilter("ignore")
        self.text, self.package = text, package
        self.model = opensysml.connect().load_from_content(text, strict=True)
        self.byid = {e["@id"]: e for e in json.loads(self.model.to_api_json().content)}
        self.pre = package + "__"
        self.redefines = {}  # redefining feature id -> redefined feature id
        for e in self.byid.values():
            if e["@type"] == "Redefinition":
                self.redefines[ref(e["redefiningFeature"])] = ref(e["redefinedFeature"])
        self.redefined_by: dict[str, set[str]] = {}
        for a, b in self.redefines.items():
            self.redefined_by.setdefault(b, set()).add(a)
        self.typing = {
            ref(e["typedFeature"]): ref(e["type"])
            for e in self.byid.values()
            if e["@type"] == "FeatureTyping"
        }
        self.cubesat = self.pre + "Cubesat"
        self.parts = {  # part usage name of Cubesat -> its part def id
            short(i): self.typing[i]
            for i, e in self.byid.items()
            if e["@type"] == "PartUsage" and ref(e.get("owner")) == self.cubesat
        }
        self.abstract = {
            i
            for i, e in self.byid.items()
            if e["@type"] == "PartDefinition" and e.get("isAbstract")
        }
        self.enums = {i for i, e in self.byid.items() if e["@type"] == "EnumerationDefinition"}
        self.swaps = {}  # abstract part def id -> enumeration def id (the selector)
        for d in self.abstract:
            for a in self.children(d, "AttributeUsage"):
                if self.typing.get(a) in self.enums:
                    self.swaps[d] = self.typing[a]
        self.root_tunes = {
            short(a) for a in self.children(self.cubesat, "AttributeUsage") if self.is_default(a)
        }

    # -- small reads -----------------------------------------------------------------------------
    def children(self, owner: str, kind: str | None = None) -> list[str]:
        return [
            i
            for i, e in self.byid.items()
            if ref(e.get("owner")) == owner and (kind is None or e["@type"] == kind)
        ]

    def inside(self, root: str) -> list[dict]:
        """The elements under ``root``: an element's id begins with its owner's id and an
        underscore (``X__member``, ``X_pvalue``, ``X_pvalue_pa0``)."""
        return [e for i, e in self.byid.items() if i.startswith(root + "_")]

    def is_default(self, feature: str) -> bool:
        return bool(self.byid[feature].get("isDefault"))

    def has_value(self, feature: str) -> bool:
        return (feature + "_pvalue") in self.byid

    def doc(self, element: str) -> str:
        """The prose of the ``doc`` comments directly under an element."""
        out = []
        for i, e in self.byid.items():
            if (
                e["@type"] == "Documentation"
                and i.startswith(element + "__")
                and "__" not in i[len(element) + 2 :]
            ):
                src = e.get("sysx:sourceText", "")
                src = re.sub(r"^\s*doc\s*/\*", "", src).replace("*/", "")
                out.append(" ".join(src.split()))
        return " ".join(out)

    def mark(self, element: str) -> str | None:
        """``MoE`` or ``MoP`` when the element's doc begins with it."""
        word = self.doc(element).split(":")[0].strip()
        return word if word in MARKS else None

    def kinds(self, kind: str) -> list[str]:
        return [
            i
            for i, e in self.byid.items()
            if e["@type"] == kind and ref(e.get("owner")) == self.package
        ]

    def value(self, quantity, unit: str | None = None) -> float:
        from opensysml.values import Quantity

        if isinstance(quantity, list):
            quantity = quantity[0]
        if isinstance(quantity, Quantity):
            if unit is None:
                return float(quantity.magnitude)
            return float(quantity.in_unit(self.model.eval(f"1.0 [{unit}]").unit))
        return float(quantity)

    # -- the dependency walk: an element to the decision elements it depends on ------------------
    def deps(self, feature: str, usage: str | None = None, seen: set | None = None) -> set[str]:
        """Decision elements a feature depends on, read in the context of a Cubesat part usage.

        ``feature`` is an attribute of ``Cubesat`` or of a part definition; ``usage`` the Cubesat
        part usage (``panelPlus``) whose body may redefine it onto a root variable.
        """
        seen = set() if seen is None else seen
        key = (feature, usage)
        if key in seen:
            return set()
        seen.add(key)
        owner = ref(self.byid[feature].get("owner"))
        if usage is not None:  # the part usage's body may redefine the attribute
            bound = f"{self.cubesat}__{usage}__{short(feature)}"
            if self.redefines.get(bound) == feature and self.has_value(bound):
                return self.expr_deps(bound + "_pvalue", owner, usage, seen)
        if owner == self.cubesat and short(feature) in self.root_tunes:
            return {short(feature)}
        if self.has_value(feature):
            out = self.expr_deps(feature + "_pvalue", owner, usage, seen)
            if self.is_default(feature) and owner != self.cubesat:
                out.add(short(feature))  # a defaulted attribute of a part: a tune (Kp, Kd)
            return out
        if owner in self.swaps and feature in {
            self.redefines[r] for r in self.redefined_by.get(feature, ())
        }:
            return {short(self.swaps[owner])}  # the alternatives redefine it: the swap
        if owner in self.swaps:
            return {short(self.swaps[owner])}
        return set()

    def expr_deps(self, root: str, definition: str, usage: str | None, seen: set) -> set[str]:
        """Decision elements an expression reads: chains, references and calc invocations."""
        out: set[str] = set()
        for e in [*self.inside(root), self.byid[root]]:
            kind = e["@type"]
            if kind == "InvocationExpression" and e.get("function"):
                fn = ref(e["function"])
                if self.byid.get(fn, {}).get("@type") == "CalculationDefinition":
                    out |= self.calc_deps(fn, seen)
            elif kind == "FeatureChainExpression":
                out |= self.chain_deps(e.get("sysx:sourceText", ""), definition, usage, seen)
            elif kind == "FeatureReferenceExpression" and e.get("referent"):
                target = ref(e["referent"])
                t = self.byid.get(target)
                if t is None or t["@type"] not in ("AttributeUsage", "ReferenceUsage"):
                    continue
                if ref(t.get("owner")) in (self.cubesat, definition):
                    out |= self.deps(target, usage, seen)
        return out

    def chain_deps(self, text: str, definition: str, usage: str | None, seen: set) -> set[str]:
        """``c.panelPlus.area``, ``wheel.maxMomentum``, ``span`` read on the configuration."""
        names = [t.strip() for t in text.replace(" ", "").split(".") if t.strip()]
        if not names:
            return set()
        if names[0] in ("environment", "nominalSlew", "budgets", "baselineMeasurement"):
            return set()  # constants and the recorded measurement
        if names[0] not in self.parts and f"{self.cubesat}__{names[0]}" not in self.byid:
            if len(names) > 1 and (
                names[1] in self.parts or f"{self.cubesat}__{names[1]}" in self.byid
            ):
                names = names[1:]  # drop the subject parameter (c, cubesat, self)
            else:
                return set()
        if names[0] in self.parts:
            part, attr = names[0], names[1] if len(names) > 1 else None
            if attr is None:
                return set()
            target = f"{self.parts[part]}__{attr}"
            return self.deps(target, part, seen) if target in self.byid else set()
        target = f"{self.cubesat}__{names[0]}"
        return self.deps(target, None, seen) if target in self.byid else set()

    def calc_deps(self, calc: str, seen: set | None = None) -> set[str]:
        """Decision elements a calc def reads through its subject, transitively through the calcs
        it invokes. Its other ``in`` parameters are bound by the caller (measured quantities)."""
        seen = set() if seen is None else seen
        if ("calc", calc) in seen:
            return set()
        seen.add(("calc", calc))
        return self.expr_deps(calc, calc, None, seen)

    def calc_measured_inputs(self, calc: str, seen: set | None = None) -> bool:
        """Whether the calc, or one it invokes, takes an ``in`` parameter that is neither the
        subject (a Cubesat) nor a scenario: a quantity the analysis binds from the measurement."""
        seen = set() if seen is None else seen
        if calc in seen:
            return False
        seen.add(calc)
        for p in self.children(calc, "ReferenceUsage"):
            t = self.typing.get(p)
            if t not in (self.cubesat, self.pre + "Scenario") and "return" not in p:
                src = self.byid[p].get("sysx:sourceText", "")
                if src.strip().startswith("in "):
                    return True
        for e in self.inside(calc):
            if e["@type"] == "InvocationExpression" and e.get("function"):
                fn = ref(e["function"])
                is_calc = self.byid.get(fn, {}).get("@type") == "CalculationDefinition"
                if is_calc and self.calc_measured_inputs(fn, seen):
                    return True
        return False

    # -- the measurement's stated inputs ----------------------------------------------------------
    def measurement_inputs(self) -> list[str]:
        """The configuration inputs the simulator reads, stated in ``SlewMeasurement``'s doc."""
        doc = self.doc(self.pre + "SlewMeasurement")
        m = re.search(r"inputs of the configuration:\s*(.*?);", doc)
        if not m:
            raise ValueError("SlewMeasurement's doc does not state the inputs the simulator reads")
        return [t.strip() for t in m.group(1).split(",") if t.strip()]

    def measured_deps(self) -> set[str]:
        out: set[str] = set()
        for name in self.measurement_inputs():
            out |= self.chain_deps(name, self.cubesat, None, set())
        return out

    # -- the traded metrics -----------------------------------------------------------------------
    def metrics(self) -> list[Metric]:
        """The traded metrics: the measurement attributes marked MoE/MoP that the analysis passes
        through, then the analysis's return entries in order."""
        analysis = next(iter(self.kinds("AnalysisCaseDefinition")))
        params = {short(p): p for p in self.children(analysis, "ReferenceUsage")}
        measurement = self.pre + "SlewMeasurement"
        out = []
        for a in self.children(measurement, "AttributeUsage"):
            if self.mark(a) and short(a) not in params:
                out.append(
                    Metric(plain(short(a)), "measured", a, self.mark(a), self.measured_deps())
                )
        tuple_root = analysis + "__attributes_pvalue"
        entries = sorted(
            (i for i in self.byid if re.fullmatch(re.escape(tuple_root) + r"_pa\d+", i)),
            key=lambda i: int(i.rsplit("_pa", 1)[1]),
        )
        for entry in entries:
            e = self.byid[entry]
            kind = e["@type"]
            measured = any(
                ref(x.get("referent")) in params.values() and short(ref(x["referent"])) != "cubesat"
                for x in [*self.inside(entry), e]
                if x["@type"] == "FeatureReferenceExpression" and x.get("referent")
            )
            if kind == "InvocationExpression":
                calc = ref(e["function"])
                deps = self.calc_deps(calc)
                if measured or self.calc_measured_inputs(calc):
                    deps |= self.measured_deps()
                out.append(Metric(plain(short(calc)), "calc", calc, self.mark(calc), deps))
            elif kind == "FeatureChainExpression":
                attr = f"{self.cubesat}__{e['sysx:sourceText'].split('.')[-1].strip()}"
                out.append(
                    Metric(plain(short(attr)), "attribute", attr, self.mark(attr), self.deps(attr))
                )
            elif kind == "FeatureReferenceExpression":
                name = short(ref(e["referent"]))
                attr = f"{measurement}__{name}"
                out.append(
                    Metric(plain(name), "measured", attr, self.mark(attr), self.measured_deps())
                )
        return out

    # -- requirements and verification cases ------------------------------------------------------
    def requirement_of(self, metric: Metric) -> tuple[str | None, str, str | None]:
        """The requirement that reads the metric's quantity: (requirement, how, MoE calc)."""
        for r in self.kinds("RequirementDefinition"):
            body = self.inside(r)
            if metric.kind == "calc":
                if any(
                    e["@type"] == "InvocationExpression"
                    and ref(e.get("function")) == metric.element
                    for e in body
                ):
                    return r, f"invokes {short(metric.element)}", None
            elif metric.kind == "measured":
                for e in body:
                    if (
                        e["@type"] == "FeatureChainExpression"
                        and e.get("sysx:sourceText", "").replace(" ", "")
                        == f"baselineMeasurement.{short(metric.element)}"
                    ):
                        return r, f"reads the measured {short(metric.element)}", None
            else:  # an attribute of the configuration, read directly or through an MoE calc
                attr = short(metric.element)
                for e in body:
                    if e["@type"] != "FeatureChainExpression":
                        continue
                    chain = e.get("sysx:sourceText", "").replace(" ", "").split(".")
                    if len(chain) == 2 and chain[1] == attr:
                        return r, f"reads c.{attr}", None
                    if len(chain) == 2:
                        via = f"{self.cubesat}__{chain[1]}"
                        if via in self.byid and self.mark(via + "_pvalue_fn") is None:
                            calcs = [
                                ref(x["function"])
                                for x in self.inside(via)
                                if x["@type"] == "InvocationExpression"
                            ]
                            for c in calcs:
                                reads = any(
                                    x["@type"] == "FeatureChainExpression"
                                    and x.get("sysx:sourceText", "")
                                    .replace(" ", "")
                                    .endswith("." + attr)
                                    for x in self.inside(c)
                                )
                                if reads and self.mark(c) == "MoE":
                                    return r, f"reads c.{chain[1]} = {short(c)}(c), the MoE", c
        return None, "none", None

    def verified_in(self, requirement: str) -> list[str]:
        out = []
        for v in self.kinds("VerificationCaseDefinition"):
            for e in self.inside(v):
                if e["@type"] == "RequirementUsage" and self.typing.get(e["@id"]) == requirement:
                    out.append(short(v))
        return sorted(set(out))

    def decision_elements(self) -> list[tuple[str, str]]:
        """(name, kind) for the swaps (by selector enumeration) then the tunes, in model order."""
        swaps = [
            (short(self.swaps[self.parts[p]]), "swap")
            for p in self.parts
            if self.parts[p] in self.swaps
        ]
        tunes = [
            (t, "tune") for t in self.children(self.cubesat, "AttributeUsage") if self.is_default(t)
        ]
        tunes = [(short(t), k) for t, k in tunes]
        for p, d in self.parts.items():
            for a in self.children(d, "AttributeUsage"):
                bound = f"{self.cubesat}__{p}__{short(a)}"
                if self.is_default(a) and bound not in self.redefines:
                    tunes.append((short(a), "tune"))
        return swaps + tunes

    # -- the named configurations -----------------------------------------------------------------
    def named_configurations(self) -> dict[str, dict]:
        out = {}
        for name in ("cubesatBaseline", "cubesatAgile", "cubesatCompact"):
            inst = self.model.instantiate(f"{self.package}::{name}")
            wheel = inst.get("wheel").get("wheelClass")
            tracker = inst.get("tracker").get("grade")
            out[name] = {
                "panel_span_m": self.value(inst.get("panelSpan"), "SI::m"),
                "battery_wh": self.value(inst.get("batteryCapacity"), "SI::W*SI::h"),
                "wheel_class": (wheel.name or wheel.literal_id).split("::")[-1],
                "st_grade": (tracker.name or tracker.literal_id).split("::")[-1],
                "Kp": float(inst.get("controller").get("Kp")),
                "Kd": float(inst.get("controller").get("Kd")),
            }
        return out

    def literals(self, enum: str) -> list[str]:
        return [c.name for c in self.model.find(f"{self.package}::{enum}").children()]


@dataclass
class Metric:
    name: str
    kind: str  # calc | attribute | measured
    element: str
    mark: str | None
    structural: set = field(default_factory=set)


# =================================================================================================
# The empirical column: one-at-a-time changes through the oracle
# =================================================================================================
def empirical(
    graph: ModelGraph, metrics: list[Metric], elements, model_path: pathlib.Path
) -> tuple[dict, str]:
    """``{(element, metric): max relative change over the named configurations}`` and a note on
    which model text the oracle ran (the same text the structural column was read from)."""
    sys.path.insert(0, str(HERE.parent))
    from experiments.cubesat_oracle import CubesatOracle

    text = graph.text
    oracles: dict[str, CubesatOracle] = {}

    def oracle_for(cfg):
        for box in ("aggressive", "baseline"):
            if box not in oracles:
                oracles[box] = CubesatOracle(text, "nominalSlew", box, workers=1)
            o = oracles[box]
            lo_p, hi_p = o.ranges["Kp"]
            lo_d, hi_d = o.ranges["Kd"]
            if lo_p <= cfg["Kp"] <= hi_p and lo_d <= cfg["Kd"] <= hi_d:
                return o
        raise ValueError(f"no gain box of the model holds Kp={cfg['Kp']}, Kd={cfg['Kd']}")

    def changed(cfg, element, kind, oracle):
        key = ORACLE_KEYS[element]
        new = dict(cfg)
        if kind == "swap":
            levels = graph.literals(element)
            new[key] = levels[(levels.index(cfg[key]) + 1) % len(levels)]
        else:
            lo, hi = oracle.ranges[key]
            value = cfg[key] * TUNE_FACTOR
            new[key] = value if value <= hi else cfg[key] / TUNE_FACTOR
            assert lo <= new[key] <= hi, (element, new[key])
        return new

    effects: dict[tuple[str, str], float] = {}
    for cfg in graph.named_configurations().values():
        oracle = oracle_for(cfg)
        base = oracle(cfg)
        for element, kind in elements:
            moved = oracle(changed(cfg, element, kind, oracle))
            for m in metrics:
                col = METRIC_COLUMNS[m.name]
                a, b = float(base[col]), float(moved[col])
                rel = abs(b - a) / max(abs(a), 1e-300)
                effects[(element, m.name)] = max(effects.get((element, m.name), 0.0), rel)
    note = (
        f"the oracle (`experiments/cubesat_oracle.py`) ran on `{model_path.name}` "
        f"(sha256 {hashlib.sha256(text.encode()).hexdigest()[:12]}), the model text of the "
        "structural column"
    )
    return effects, note


# =================================================================================================
# The coupling graph: configuration values -> subsystem calcs -> coupling variables -> metrics
# =================================================================================================
# The analyst's decomposition of the model into the CaseSpec's three subsystems (the behavioural
# view's), named here once: each calc def, each computed attribute of a part def (``Part.attr``) and
# the slew measurement (the simulator, ``SlewMeasurement``) belongs to one subsystem. Everything
# else about the graph is read from the model: which configuration attribute each calc reads, which
# calc or measured quantity each calc takes from another subsystem (the coupling variables, named as
# the model names them), and which metric and requirement is read off each subsystem. A calc the
# metrics and requirements reach that is not placed here stops the build by name. The constants
# (the environment, the scenario, the budgets, the fixed parts bus, antenna and IMU) are not nodes.
SUBSYSTEM_OF = {
    "controls": {"SlewMeasurement", "GravityGradientTorque", "PointingError"},
    "power and energy": {
        "SolarPanel.area",
        "SolarPanel.mass",
        "Battery.mass",
        "GeneratedPower",
        "BaseLoad",
        "AvailablePower",
        "UsableWheelTorque",
        "SlewLossEnergy",
        "EclipseDemand",
        "DepthOfDischarge",
        "EclipseReserve",
        "OrbitPeriod",
        "EnergyBalance",
        "PeakSlewPower",
        "PowerMargin",
        "BatteryPeakPower",
        "EclipsePeakLoad",
    },
    "mass": {
        "MassAccounting",
        "StructureMass",
        "AdcsMass",
        "LaunchCost",
        "InertiaX",
        "InertiaY",
        "InertiaZ",
    },
}
CONSTANT_PARTS = ("environment", "nominalSlew", "budgets")
MEASUREMENT = "SlewMeasurement"
SIMULATOR = "adcs_sim.simulate_adcs"


class Coupling:
    """The directed graph of the model's evaluation, read through ``ModelGraph``.

    Nodes: the configuration values (``("config", name)``), the calcs (``("calc", Name)``), the
    computed attributes of the parts (``("part", usage, attr)``), the slew measurement
    (``("measurement",)``), the traded metrics (``("metric", name)``) and the requirements
    (``("req", Name)``). An edge ``(source, node)`` carries the set of names under which ``node``
    reads ``source`` (``wheel.mass``, ``structureMass``, ``peakTorque``, ``InertiaX``): the model's
    own names for the quantities, which are the coupling variables when the two ends sit in
    different subsystems.
    """

    def __init__(self, graph: ModelGraph, metrics: list[Metric]):
        self.g = graph
        self.edges: dict[tuple, set[str]] = {}
        self.visited: set = set()
        self.nodes: set[tuple] = set()
        g = graph
        self.cubesat_attrs = {short(a): a for a in g.children(g.cubesat, "AttributeUsage")}
        self.in_params: dict[str, list[tuple[str, str]]] = {}  # calc id -> [(name, type id)]
        for i, e in g.byid.items():
            if e["@type"] in (
                "CalculationDefinition",
                "RequirementDefinition",
                "AnalysisCaseDefinition",
            ):
                self.in_params[i] = [
                    (short(ref(f)), g.typing.get(ref(f)))
                    for f in e.get("ownedFeature", [])
                    if g.byid.get(ref(f), {}).get("direction") == "in"
                ]
        # the measurement: the simulator reads the stated inputs
        self.nodes.add(("measurement",))
        for name in g.measurement_inputs():
            self.read(self.resolve_chain(name, None), ("measurement",), self.label(name))
        # the metrics, from the analysis's return entries and the measurement
        analysis = next(iter(g.kinds("AnalysisCaseDefinition")))
        env = {p: ("measured", p) for p, t in self.in_params[analysis] if t != g.cubesat}
        tuple_root = analysis + "__attributes_pvalue"
        entries = {}
        for m in metrics:
            if m.kind == "measured":
                self.read(("measured", short(m.element)), ("metric", m.name), short(m.element))
        for i in g.byid:
            if re.fullmatch(re.escape(tuple_root) + r"_pa\d+", i):
                entries[int(i.rsplit("_pa", 1)[1])] = i
        by_element = {m.element: m for m in metrics}
        for _, entry in sorted(entries.items()):
            e = g.byid[entry]
            if e["@type"] == "InvocationExpression":
                calc = ref(e["function"])
                self.invoke(entry, ("metric", by_element[calc].name), None, env)
            elif e["@type"] == "FeatureChainExpression":
                attr = f"{g.cubesat}__{e['sysx:sourceText'].split('.')[-1].strip()}"
                m = by_element[attr]
                self.read(
                    self.resolve_chain(e["sysx:sourceText"], None), ("metric", m.name), short(attr)
                )
            elif e["@type"] == "FeatureReferenceExpression":
                name = short(ref(e["referent"]))
                m = by_element[f"{g.pre}{MEASUREMENT}__{name}"]
                self.read(("measured", name), ("metric", m.name), name)
        # the requirements: the constraint, with the `in` parameters bound by their defaults
        for r in g.kinds("RequirementDefinition"):
            env = {}
            for p, t in self.in_params[r]:
                if t == g.cubesat:
                    continue
                default = g.byid.get(f"{r}__{p}_pvalue", {}).get("sysx:sourceText", "")
                src = self.resolve_chain(default, None) if default else None
                env[p] = src
            for c in g.children(r, "ConstraintUsage"):
                self.walk(c, ("req", short(r)), (r, None), env)
        self.subsystem = {n: self.place(n) for n in self.nodes}

    # -- recording --------------------------------------------------------------------------------
    def read(self, source, node, label: str) -> None:
        if source is None:
            return
        self.nodes.add(node)
        if source[0] not in ("config", "measured"):
            self.nodes.add(source)
        self.edges.setdefault((source, node), set()).add(label)

    def place(self, node) -> str | None:
        if node[0] == "calc":
            name = node[1]
        elif node[0] == "part":
            name = f"{short(self.g.parts[node[1]])}.{node[2]}"
        elif node[0] == "measurement":
            name = MEASUREMENT
        else:
            return None
        for s, members in SUBSYSTEM_OF.items():
            if name in members:
                return s
        raise KeyError(
            f"{name} is reached by a metric or a requirement but belongs to no subsystem"
        )

    # -- the walk ----------------------------------------------------------------------------
    def calc_params(self, calc: str) -> list[tuple[str, str]]:
        return self.in_params.get(calc, [])

    def invoke(self, inv: str, into, context, env: dict):
        """An invocation of a calc: bind its parameters from the arguments, visit it, and return
        its node (the caller reads it under the calc's name)."""
        g = self.g
        calc = ref(g.byid[inv]["function"])
        node = ("calc", short(calc))
        bound = {}
        for k, (p, t) in enumerate(self.calc_params(calc)):
            if t == g.cubesat:
                continue
            arg = f"{inv}_pa{k}"
            bound[p] = self.resolve_arg(arg, context, env) if arg in g.byid else None
        self.visit_calc(calc, bound)
        if into is not None:
            self.read(node, into, short(calc))
        return node

    def resolve_arg(self, arg: str, context, env: dict):
        g = self.g
        e = g.byid[arg]
        kind = e["@type"]
        if (
            kind == "InvocationExpression"
            and g.byid.get(ref(e.get("function")), {}).get("@type") == "CalculationDefinition"
        ):
            return self.invoke(arg, None, context, env)
        if kind == "FeatureReferenceExpression" and e.get("referent"):
            name = short(ref(e["referent"]))
            if name in env:
                return env[name]
            return self.resolve_chain(name, context)
        if kind == "FeatureChainExpression":
            return self.resolve_chain(e.get("sysx:sourceText", ""), context)
        return None

    def visit_calc(self, calc: str, env: dict) -> None:
        key = (calc, tuple(sorted((k, v) for k, v in env.items() if v is not None)))
        if key in self.visited:
            return
        self.visited.add(key)
        node = ("calc", short(calc))
        self.nodes.add(node)
        for p, src in env.items():
            if src is not None:
                self.read(src, node, self.source_label(src, p))
        for f in self.g.byid[calc].get("ownedFeature", []):
            if self.g.byid.get(ref(f), {}).get("direction") == "out":
                self.walk(ref(f) + "_pvalue", node, (calc, None), env)

    def visit_part_attr(self, usage: str, attr: str) -> None:
        node = ("part", usage, attr)
        if node in self.visited:
            return
        self.visited.add(node)
        self.nodes.add(node)
        definition = self.g.parts[usage]
        self.walk(f"{definition}__{attr}_pvalue", node, (definition, usage), {})

    def walk(self, root: str, into, context, env: dict) -> None:
        """The reads of the expression under ``root``, attributed to ``into``."""
        g = self.g
        if root not in g.byid:
            return
        elements = [*g.inside(root), g.byid[root]]
        invocations = [
            e["@id"]
            for e in elements
            if e["@type"] == "InvocationExpression"
            and g.byid.get(ref(e.get("function")), {}).get("@type") == "CalculationDefinition"
        ]
        outer = [
            i for i in invocations if not any(i.startswith(j + "_") for j in invocations if j != i)
        ]
        for i in outer:
            self.invoke(i, into, context, env)
        chains = [e for e in elements if e["@type"] == "FeatureChainExpression"]
        chain_ids = [e["@id"] for e in chains]

        def under(i: str, roots) -> bool:
            return any(i.startswith(r + "_") for r in roots)

        for e in chains:
            i = e["@id"]
            if under(i, outer) or under(i, [c for c in chain_ids if c != i]):
                continue
            text = e.get("sysx:sourceText", "")
            self.read(self.resolve_chain(text, context), into, self.label(text))
        for e in elements:
            if e["@type"] != "FeatureReferenceExpression" or not e.get("referent"):
                continue
            i = e["@id"]
            if under(i, outer) or under(i, chain_ids):
                continue
            target = ref(e["referent"])
            if not target.startswith(g.pre):
                continue  # a unit or a library function
            name = short(target)
            if name in env:
                if env[name] is not None:
                    self.read(env[name], into, self.source_label(env[name], name))
                continue
            t = g.byid.get(target, {})
            if t.get("@type") != "AttributeUsage":
                continue
            label = f"{context[1]}.{name}" if context and context[1] else name
            self.read(self.resolve_chain(name, context), into, label)

    # -- resolving a name to its source ------------------------------------------------------------
    @staticmethod
    def source_label(src, fallback: str) -> str:
        """The model's name for a bound source: a calc's name, a part attribute's path, or the
        measured quantity's name."""
        if src[0] == "calc":
            return src[1]
        if src[0] == "part":
            return f"{src[1]}.{src[2]}"
        return fallback

    def label(self, text: str) -> str:
        """The model's name for a read: the chain without its subject; a Cubesat attribute that
        only renames a part's attribute (``momentumCapacity = wheel.maxMomentum``) carries it."""
        names = [t.strip() for t in text.replace(" ", "").split(".") if t.strip()]
        if names and names[0] in ("c", "cubesat", "self") and len(names) > 1:
            names = names[1:]
        if len(names) == 1 and names[0] in self.cubesat_attrs:
            attr = self.cubesat_attrs[names[0]]
            if self.g.has_value(attr):
                body = [*self.g.inside(attr + "_pvalue"), self.g.byid[attr + "_pvalue"]]
                if not any(e["@type"] == "InvocationExpression" for e in body):
                    chains = [e for e in body if e["@type"] == "FeatureChainExpression"]
                    if chains:
                        return f"{names[0]} ({chains[0]['sysx:sourceText'].strip()})"
        return ".".join(names)

    def resolve_chain(self, text: str, context):
        """The source a chain reads: a configuration value, a calc, a computed part attribute, a
        measured quantity, or None for a constant."""
        g = self.g
        names = [
            t.strip() for t in text.replace(" ", "").replace("::", ".").split(".") if t.strip()
        ]
        if not names:
            return None
        if names[0] in CONSTANT_PARTS:
            return None
        if names[0] == "baselineMeasurement":
            return ("measured", names[1]) if len(names) > 1 else None
        if names[0] == "Cubesat" and len(names) > 1:
            names = names[1:]
        if names[0] not in g.parts and names[0] not in self.cubesat_attrs:
            if len(names) > 1 and (names[1] in g.parts or names[1] in self.cubesat_attrs):
                names = names[1:]
            elif context is not None and context[1] is not None:
                names = [context[1], *names]  # a bare attribute inside a part def: its usage
            else:
                return None
        if names[0] in g.parts:
            if len(names) < 2:
                return None
            usage, attr = names[0], names[1]
            definition = g.parts[usage]
            feature = f"{definition}__{attr}"
            if feature not in g.byid:
                return None
            if definition in g.swaps:
                return ("config", short(g.swaps[definition]))
            bound = f"{g.cubesat}__{usage}__{attr}"
            if g.redefines.get(bound) == feature and g.has_value(bound):
                refs = [
                    short(ref(x["referent"]))
                    for x in [*g.inside(bound + "_pvalue"), g.byid[bound + "_pvalue"]]
                    if x["@type"] == "FeatureReferenceExpression" and x.get("referent")
                ]
                tunes = [r for r in refs if r in g.root_tunes]
                return ("config", tunes[0]) if tunes else None
            if g.is_default(feature):
                return ("config", attr)
            if self.is_computed(feature):
                self.visit_part_attr(usage, attr)
                return ("part", usage, attr)
            return None
        attr = self.cubesat_attrs[names[0]]
        if names[0] in g.root_tunes:
            return ("config", names[0])
        if not g.has_value(attr):
            return None
        body = [*g.inside(attr + "_pvalue"), g.byid[attr + "_pvalue"]]
        for e in body:
            if (
                e["@type"] == "InvocationExpression"
                and g.byid.get(ref(e.get("function")), {}).get("@type") == "CalculationDefinition"
            ):
                calc = ref(e["function"])
                self.visit_calc(calc, {})
                return ("calc", short(calc))
        for e in body:
            if e["@type"] == "FeatureChainExpression":
                return self.resolve_chain(e.get("sysx:sourceText", ""), None)
        return None

    def is_computed(self, feature: str) -> bool:
        """A part-def attribute whose value reads another attribute of the model (not only units
        and literals) or invokes a calc."""
        g = self.g
        for e in [*g.inside(feature + "_pvalue"), g.byid[feature + "_pvalue"]]:
            fn = g.byid.get(ref(e.get("function")), {}) if e.get("function") else {}
            if e["@type"] == "InvocationExpression" and fn.get("@type") == "CalculationDefinition":
                return True
            if e["@type"] == "FeatureReferenceExpression" and e.get("referent"):
                t = g.byid.get(ref(e["referent"]), {})
                owner = ref(t.get("owner"))
                if t.get("@type") == "AttributeUsage" and owner not in (g.pre + "Environment",):
                    return True
        return False

    # -- the design structure matrix ---------------------------------------------------------
    def node_name(self, node) -> str:
        if node[0] == "calc":
            return node[1]
        if node[0] == "part":
            return f"{node[1]}.{node[2]}"
        if node[0] == "measurement":
            return f"{MEASUREMENT} ({SIMULATOR})"
        return str(node[1])

    def line(self, node) -> int:
        g = self.g
        if node[0] == "calc":
            return g.byid[g.pre + node[1]].get("sysx:sourceLine", 0)
        if node[0] == "part":
            return g.byid[f"{g.parts[node[1]]}__{node[2]}"].get("sysx:sourceLine", 0)
        return 0

    def dsm(
        self, configs: list[str], subsystems: list[str], metrics: list[str], structural: dict
    ) -> dict:
        """Cells of the design structure matrix and the connectivity test.

        ``structural`` is table 1's structural column, ``{(configuration value, metric): bool}``:
        the metrics a configuration value reaches are read from it (the calc-level walk), since a
        subsystem that two configuration values feed does not pass every one of them to every
        metric it reads off (the gains reach the controls, not the mass accounting).
        """
        members = {
            s: sorted(
                (n for n in self.nodes if self.subsystem.get(n) == s),
                key=lambda n: (self.line(n), self.node_name(n)),
            )
            for s in subsystems
        }
        cells: dict[tuple[str, str], set[str]] = {}
        read_off_metrics: dict[str, list[str]] = {s: [] for s in subsystems}
        read_off_reqs: dict[str, set[str]] = {s: set() for s in subsystems}
        for (src, dst), labels in self.edges.items():
            s_sub = "controls" if src[0] == "measured" else self.subsystem.get(src)
            if dst[0] == "metric":
                if s_sub is not None:
                    read_off_metrics[s_sub].append(dst[1])
                continue
            if dst[0] == "req":
                if s_sub is not None:
                    read_off_reqs[s_sub].add(dst[1])
                continue
            d_sub = self.subsystem.get(dst)
            if src[0] == "config":
                cells.setdefault((src[1], d_sub), set()).update(labels)
            elif s_sub is not None and d_sub is not None and s_sub != d_sub:
                cells.setdefault((s_sub, d_sub), set()).update(labels)
        for s in subsystems:
            read_off_metrics[s] = [m for m in metrics if m in read_off_metrics[s]]
        # connectivity over configuration values, subsystems and metrics
        succ: dict[str, set[str]] = {}
        for (a, b), labels in cells.items():
            if labels:
                succ.setdefault(a, set()).add(b)
        for s in subsystems:
            for m in read_off_metrics[s]:
                succ.setdefault(s, set()).add(m)
        nodes = [*configs, *subsystems, *metrics]

        feeds = {c: [s for s in subsystems if cells.get((c, s))] for c in configs}
        reached = {c: [m for m in metrics if structural.get((c, m))] for c in configs}
        undirected: dict[str, set[str]] = {n: set() for n in nodes}
        for a, bs in succ.items():
            for b in bs:
                undirected[a].add(b)
                undirected[b].add(a)
        seen, stack = {nodes[0]}, [nodes[0]]
        while stack:
            x = stack.pop()
            for y in undirected[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        n_edges = sum(len(v) for v in succ.values())
        return {
            "subsystems": subsystems,
            "members": {s: [self.node_name(n) for n in members[s]] for s in subsystems},
            "cells": {k: sorted(v) for k, v in cells.items()},
            "metrics_read_off": read_off_metrics,
            "requirements_read_off": {s: sorted(v) for s, v in read_off_reqs.items()},
            "feeds": feeds,
            "reached": reached,
            "unreached_metrics": [m for m in metrics if not any(m in r for r in reached.values())],
            "unfed": [c for c in configs if not feeds[c]],
            "connected": seen == set(nodes),
            "n_nodes": len(nodes),
            "n_edges": n_edges,
        }


def coupling(graph: ModelGraph, metrics: list[Metric], elements, structural: dict) -> dict:
    """The design structure matrix of the model, with the CaseSpec's subsystem order."""
    sys.path.insert(0, str(HERE.parent))
    import case

    spec = case.CUBESAT
    order = list(spec.subsystem_order)
    if set(order) != set(SUBSYSTEM_OF):
        raise ValueError(f"the subsystems {sorted(SUBSYSTEM_OF)} are not the CaseSpec's {order}")
    c = Coupling(graph, metrics)
    out = c.dsm([e for e, _ in elements], order, [m.name for m in metrics], structural)
    # the subsystem each metric is read off agrees with the CaseSpec's placement of the metric
    by_name = {spec.short[a]: spec.subsystems[a] for a in spec.attributes}
    for s in order:
        for m in out["metrics_read_off"][s]:
            if by_name.get(m, s) != s:
                raise ValueError(f"{m} is read off {s} but the CaseSpec places it in {by_name[m]}")
    return out


# =================================================================================================
# The tables
# =================================================================================================
def build(model_path: pathlib.Path, with_empirical: bool = True) -> dict:
    text = model_path.read_text()
    graph = ModelGraph(text)
    metrics = graph.metrics()
    elements = graph.decision_elements()
    effects, note = (
        empirical(graph, metrics, elements, model_path) if with_empirical else ({}, "not run")
    )
    rows = []
    for element, kind in elements:
        for m in metrics:
            structural = element in m.structural
            rel = effects.get((element, m.name))
            emp = None if rel is None else rel > EFFECT
            rows.append(
                {
                    "decision_element": element,
                    "kind": kind,
                    "metric": m.name,
                    "structural": structural,
                    "empirical": emp,
                    "max_relative_change": rel,
                    "agree": None if emp is None else structural == emp,
                }
            )
    table2 = []
    for m in metrics:
        req, how, _via = graph.requirement_of(m)
        table2.append(
            {
                "metric": m.name,
                "mark": m.mark or "none",
                "element": short(m.element),
                "kind": m.kind,
                "requirement": short(req) if req else "none",
                "how": how,
                "verified_in": ", ".join(graph.verified_in(req)) if req else "none",
            }
        )
    return {
        "model": model_path,
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "elements": elements,
        "metrics": metrics,
        "rows": rows,
        "table2": table2,
        "coupling": coupling(
            graph,
            metrics,
            elements,
            {(r["decision_element"], r["metric"]): r["structural"] for r in rows},
        ),
        "empirical_note": note,
        "measurement_inputs": graph.measurement_inputs(),
    }


def _yn(v) -> str:
    return "-" if v is None else ("yes" if v else "no")


def render_md(result: dict) -> str:
    rel = (
        result["model"].relative_to(HERE.parents[2])
        if HERE.parents[2] in result["model"].parents
        else result["model"]
    )
    metrics = [m.name for m in result["metrics"]]
    out = [
        "# Coverage table of the cubesat model",
        "",
        f"Generated by `examples/adcs/model_v2/coverage.py` from `{rel}` (sha256 "
        f"{result['sha256'][:12]}). Decision elements: the swaps and tunes of the assembly view. "
        "Traded metrics: the measurement attributes marked MoE or MoP that the analysis passes "
        "through, then the analysis's return entries in order.",
        "",
        "## Decision element x traded metric",
        "",
        "Each cell: `structural / empirical`. Structural: a path in the model from the metric back "
        "to the decision element (calc invocations, attribute reads, redefinitions, the "
        "measurement's stated simulator inputs). Empirical: a one-at-a-time change of the element "
        f"at the three named configurations moves the metric by more than {EFFECT:g} relative "
        f"(tunes by a factor {TUNE_FACTOR}, swaps to the next level); the largest relative change "
        "over the three in parentheses. `*` marks a disagreement (a finding).",
        "",
        "| decision element | kind | " + " | ".join(metrics) + " |",
        "|---|---|" + "---|" * len(metrics),
    ]
    by = {(r["decision_element"], r["metric"]): r for r in result["rows"]}
    for element, kind in result["elements"]:
        cells = []
        for m in metrics:
            r = by[(element, m)]
            cell = f"{_yn(r['structural'])} / {_yn(r['empirical'])}"
            if r["max_relative_change"] is not None:
                cell += f" ({r['max_relative_change']:.1e})"
            if r["agree"] is False:
                cell += " *"
            cells.append(cell)
        out.append(f"| {element} | {kind} | " + " | ".join(cells) + " |")
    out += [
        "",
        f"Empirical column: {result['empirical_note']}. The magnitudes are printed to two "
        "significant digits: a relative change of a quantity the slew measures differs between "
        "platforms in its fourth digit, and the settling time, read on the integrator's own time "
        "grid (`adcs_sim`: quantized by the step), differs by up to a step, so a relative change "
        "in its column is an order of magnitude, not a value; the committed magnitudes are the "
        "environment of record's (`paper/container/README.md`).",
        "",
    ]
    findings = [r for r in result["rows"] if r["agree"] is False]
    out.append(
        "Disagreements (findings): "
        + (
            "none."
            if not findings
            else "; ".join(
                f"{r['decision_element']} -> {r['metric']} (structural {_yn(r['structural'])}, "
                f"empirical {_yn(r['empirical'])}, largest relative change "
                f"{r['max_relative_change']:.1e})"
                for r in findings
            )
            + "."
        )
    )
    empty = [e for e, _ in result["elements"] if not any(by[(e, m)]["structural"] for m in metrics)]
    out.append(
        "Decision elements with no structural path to any metric: "
        + (", ".join(empty) or "none")
        + "."
    )
    out += [
        "",
        "Simulator inputs stated on the measurement: "
        + ", ".join(result["measurement_inputs"])
        + ".",
        "",
        "## Traded metric -> MoE or MoP, requirement, verification",
        "",
        "| traded metric | mark | element | requirement that reads it | how | verified in |",
        "|---|---|---|---|---|---|",
    ]
    for t in result["table2"]:
        out.append(
            f"| {t['metric']} | {t['mark']} | {t['element']} ({t['kind']}) | {t['requirement']} | "
            f"{t['how']} | {t['verified_in']} |"
        )
    out += ["", *render_coupling_md(result["coupling"], result["elements"]), ""]
    return "\n".join(out)


def render_coupling_md(c: dict, elements) -> list[str]:
    """The design structure matrix: rows feed columns."""
    subs = c["subsystems"]
    head = ["## Coupling between subsystems (a design structure matrix)", ""]
    head += [
        "Rows feed columns, in the form of the design structure matrix of the MDAO literature (an "
        "XDSM without its process line). A configuration row names the configuration attributes "
        "the column subsystem's calcs read, as the model names them; a subsystem row names the "
        "coupling variables the column subsystem reads from it; the diagonal names the subsystem's "
        "own calcs (the measurement is the simulator); the last two columns name the traded "
        "metrics and the requirements read off each subsystem. The subsystems are the three of the "
        "behavioural view; which calc belongs to which is the analyst's decomposition "
        "(`SUBSYSTEM_OF` in `coverage.py`); every cell is read from the model. The constants of "
        "the environment, the scenario, the budgets and the fixed parts (bus, antenna, IMU) are "
        "not shown.",
        "",
        "| feeds &rarr; | " + " | ".join(subs) + " | metrics read off | requirements read off |",
        "|---|" + "---|" * (len(subs) + 2),
    ]
    rows = []
    for element, kind in elements:
        cells = [", ".join(c["cells"].get((element, s), [])) or "&nbsp;" for s in subs]
        rows.append(f"| {element} ({kind}) | " + " | ".join(cells) + " | &nbsp; | &nbsp; |")
    for s in subs:
        cells = []
        for s2 in subs:
            if s2 == s:
                cells.append("*" + ", ".join(c["members"][s]) + "*")
            else:
                cells.append(", ".join(c["cells"].get((s, s2), [])) or "&nbsp;")
        rows.append(
            f"| **{s}** | "
            + " | ".join(cells)
            + f" | {', '.join(c['metrics_read_off'][s]) or '&nbsp;'}"
            + f" | {', '.join(c['requirements_read_off'][s]) or '&nbsp;'} |"
        )
    n_metrics = sum(len(c["metrics_read_off"][s]) for s in subs)
    feeds = "; ".join(
        f"{e} feeds {', '.join(c['feeds'][e])} and reaches {len(c['reached'][e])} of "
        f"{n_metrics} metrics"
        for e, _ in elements
    )
    tail = [
        "",
        "Connectivity: "
        + (
            "every configuration value feeds at least one subsystem"
            if not c["unfed"]
            else "configuration values feeding no subsystem: " + ", ".join(c["unfed"])
        )
        + " and reaches at least one traded metric by the structural column of the first table ("
        + feeds
        + "); "
        + (
            "every traded metric is read off a subsystem"
            if not c["unreached_metrics"]
            else "metrics no configuration value reaches: " + ", ".join(c["unreached_metrics"])
        )
        + "; the graph of configuration values, subsystems and metrics "
        + ("is connected" if c["connected"] else "is NOT connected")
        + f" ({c['n_nodes']} nodes, {c['n_edges']} edges).",
        "",
        "The controls and the power subsystem feed each other (cells on both sides of the "
        "diagonal): the usable wheel torque is a quantity of the configuration, computed before "
        "the slew, and the peak torque and the integral of the squared torque are read after it, "
        "so the model resolves the loop in one pass, with no fixed-point iteration.",
    ]
    return head + rows + tail


def render_csv(result: dict) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(
        [
            "table",
            "decision_element",
            "kind",
            "metric",
            "structural",
            "empirical",
            "max_relative_change",
            "agree",
        ]
    )
    for r in result["rows"]:
        rel = "" if r["max_relative_change"] is None else f"{r['max_relative_change']:.1e}"
        w.writerow(
            [
                "coverage",
                r["decision_element"],
                r["kind"],
                r["metric"],
                _yn(r["structural"]),
                _yn(r["empirical"]),
                rel,
                _yn(r["agree"]),
            ]
        )
    w.writerow(["table", "metric", "mark", "element", "kind", "requirement", "how", "verified_in"])
    for t in result["table2"]:
        w.writerow(
            [
                "metrics",
                t["metric"],
                t["mark"],
                t["element"],
                t["kind"],
                t["requirement"],
                t["how"],
                t["verified_in"],
            ]
        )
    c = result["coupling"]
    w.writerow(["table", "from", "to", "variables"])
    for element, _ in result["elements"]:
        for s in c["subsystems"]:
            if c["cells"].get((element, s)):
                w.writerow(["coupling", element, s, "; ".join(c["cells"][(element, s)])])
    for s in c["subsystems"]:
        w.writerow(["coupling", s, s, "; ".join(c["members"][s])])
        for s2 in c["subsystems"]:
            if s2 != s and c["cells"].get((s, s2)):
                w.writerow(["coupling", s, s2, "; ".join(c["cells"][(s, s2)])])
        w.writerow(["coupling", s, "metrics read off", "; ".join(c["metrics_read_off"][s])])
        w.writerow(
            ["coupling", s, "requirements read off", "; ".join(c["requirements_read_off"][s])]
        )
    w.writerow(
        [
            "coupling",
            "connectivity",
            "connected" if c["connected"] else "not connected",
            f"{c['n_nodes']} nodes; {c['n_edges']} edges; "
            f"unfed: {'; '.join(c['unfed']) or 'none'}; "
            f"unreached: {'; '.join(c['unreached_metrics']) or 'none'}",
        ]
    )
    return buf.getvalue()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--model", type=pathlib.Path, default=DEFAULT_MODEL)
    ap.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT)
    ap.add_argument("--no-empirical", action="store_true", help="structural column only")
    a = ap.parse_args(argv)
    result = build(a.model.resolve(), with_empirical=not a.no_empirical)
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "coverage.md").write_text(render_md(result))
    (a.out / "coverage.csv").write_text(render_csv(result))
    findings = [r for r in result["rows"] if r["agree"] is False]
    print(f"wrote {a.out / 'coverage.md'} and coverage.csv; {len(findings)} disagreement(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
