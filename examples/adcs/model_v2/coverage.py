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

The empirical column runs the slews through the case's oracle (``experiments.cubesat_oracle``),
which reads the adopted ``cubesat.sysml``; the revision ``cubesat_r2.sysml`` changes no calculation
of it (``tests/test_system_model_v2.py`` pins that), so the empirical column of either model is the
same and the table says which model text the oracle ran. Nothing numeric about the case is typed
here: ranges, enumerations, the named configurations and every effect are read from the model or
measured through the oracle. The column names of the dataset (the interface contract's) name the
oracle's outputs.

    uv run python examples/adcs/model_v2/coverage.py [--model PATH] [--out DIR] [--no-empirical]

Default model: ``cubesat_r2.sysml`` beside this file (the gate swaps the default); default output
directory: ``views/`` beside this file. Three runs on one machine give byte-identical files.
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
DEFAULT_MODEL = HERE / "cubesat_r2.sysml"
ADOPTED_MODEL = HERE / "cubesat.sysml"
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
def empirical(graph: ModelGraph, metrics: list[Metric], elements) -> tuple[dict, str]:
    """``{(element, metric): max relative change over the named configurations}`` and a note on
    which model text the oracle ran."""
    sys.path.insert(0, str(HERE.parent))
    from experiments.cubesat_oracle import CubesatOracle

    text = ADOPTED_MODEL.read_text()
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
        f"the oracle (`experiments/cubesat_oracle.py`) ran on `{ADOPTED_MODEL.name}` "
        f"(sha256 {hashlib.sha256(text.encode()).hexdigest()[:12]}); the revision keeps every "
        f"calculation of it, so the column holds for both"
    )
    return effects, note


# =================================================================================================
# The tables
# =================================================================================================
def build(model_path: pathlib.Path, with_empirical: bool = True) -> dict:
    text = model_path.read_text()
    graph = ModelGraph(text)
    metrics = graph.metrics()
    elements = graph.decision_elements()
    effects, note = empirical(graph, metrics, elements) if with_empirical else ({}, "not run")
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
    out += ["", f"Empirical column: {result['empirical_note']}.", ""]
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
    out.append("")
    return "\n".join(out)


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
        rel = "" if r["max_relative_change"] is None else f"{r['max_relative_change']:.3e}"
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
