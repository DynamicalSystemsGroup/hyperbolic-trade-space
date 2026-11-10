"""Project the loaded SysML v2 model to PlantUML text for two paper figures.

Reads the model through the opensysml Python API (query, eval, to_api_json). Nothing about the case
is typed here that the model can state: each traded metric (its name and subsystem from the CaseSpec)
is found in the model by its own name (``settling time`` -> ``settlingTime``, ``eclipse reserve`` ->
``EclipseReserve``), the requirement-metric relations are read from the elements, and the metrics with
no requirement are checked against the model's own statement of them (the verification cases' docs).
Typed here: layout parameters, colours, and the analyst's subsystem for a requirement no metric reads.

    uv run python project.py MODEL.sysml OUTDIR [--package NAME]

writes OUTDIR/assembly_view.puml (what a configuration is and how the parts assemble) and
OUTDIR/behavioural_view.puml (subsystems, requirements, the traded metrics, how the metrics are
obtained). Revision 2 (2026-11-09): the first slot-2 candidate is withdrawn. Revision 3 (WP23 round
1): the metric list is the CaseSpec's filtered to the metrics the model carries (the revision
``cubesat_r2.sysml`` has no slew time); a metric's MoE or MoP mark (the first word of the ``doc`` on
its element) is written in its box; a calc the model marks MoE that is not itself traded (the launch
cost on the total mass) is drawn as a box between the requirement that reads it and the metric it
reads. On a model without marks (the adopted ``cubesat.sysml``) the output is unchanged.
Revision 4 (WP23 round 3, the round-1 cold reads' dispositions; ``--revision 4``, default 3 until the
data gate swaps the committed views): the legend of each view is cut to what the image needs (the
colour key; the rest is the caption's, ``INTENT.md``); one colour rule, orange a requirement, green a
traded metric, yellow a derived quantity that is not traded, the MoE or MoP mark by stereotype only;
the requirement boxes carry the name and only what differs between them (the verification case),
and a requirement that reads no traded metric carries its constraint in the model's words; the
requirement-metric relation is a headless line (a shared quantity) and the source lines keep the one
arrowhead (where a metric comes from); the subsystem lanes are titled as the analyst's grouping; the
assembly legend names the untagged parts as fixed and the gain ranges by regime (read from
``experiments/definitions.py``).
Revision 5 (WP23 round 4, the round-3 cold reads' dispositions; ``--revision 5``): the short line
from the launch cost to the total mass (two boxes at one rank) carries the element the two share,
``totalMass``, so the chain requirement -> launch cost -> total mass reads at 700 px (a label on the
requirement's line too would cost the whole figure 0.65 px of type: a label between ranks widens the
layout); the group of requirements that read no
traded metric is titled in those words, in the body's black; the assembly legend keeps the two tag
keys and the untagged rule, and the levels and ranges go to the caption (``assembly_caption.md``,
written beside the views, still read from the model).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import warnings

import opensysml

warnings.simplefilter("ignore")

REPO = pathlib.Path(__file__).resolve().parents[4]

# ---- layout parameters (PlantUML / Graphviz controls; no model content) ------------------------
COLUMN_WIDTH = 700  # px, the paper's column; PlantUML `scale N width`
ASSEMBLY_DIRECTION = "top to bottom direction"
BEHAVIOUR_DIRECTION = "left to right direction"
ASSEMBLY_LINETYPE = (
    "polyline"  # skinparam linetype: ortho | polyline (default splines)
)
BEHAVIOUR_LINETYPE = "polyline"
# layout control: blank lines in the analysis box, so that it is tall enough to meet every metric it feeds
# with its own, separate line (round 3: two lines met at one point; the long diagonals shorten)
ANALYSIS_BOX_PAD = 14
SKIN = """skinparam shadowing false
skinparam defaultFontName SansSerif
skinparam defaultFontSize 12
skinparam ClassBackgroundColor white
skinparam ClassBorderColor #404040
skinparam ClassAttributeIconSize 0
skinparam ArrowColor #404040
skinparam RectangleBackgroundColor white
skinparam RectangleBorderColor #404040
skinparam PackageBackgroundColor #F7F7F7
skinparam PackageBorderColor #909090
skinparam LegendBackgroundColor white
skinparam LegendBorderColor #909090
skinparam nodesep {nodesep}
skinparam ranksep {ranksep}
hide circle
hide empty members
"""
# the two kinds of configuration variable: one tag style, one colour each, used nowhere else
TAG_CATEGORICAL = (
    "swap",
    "#F6C98B",
)  # a part is replaced by one of its alternatives
TAG_CONTINUOUS = (
    "tune",
    "#9CC8EE",
)  # a parameter of a part takes a value in a range

# ---- behavioural view: the model's element for a traded metric is found by the metric's own name ----
# kind: calc = a calc def the analysis returns; attr = a Cubesat attribute the analysis returns;
#       input = an analysis `in` parameter returned unchanged; measured = a SlewMeasurement quantity.
# the analyst's reading, used only where the model leaves a requirement with no related metric:
# the subsystem the requirement lands on (CaseSpec groups metrics, not requirements)
# name used in the model's prose for a measured quantity, to find documentary relations
PROSE_NAME = {
    "slew time": "slew time",
    "settling time": "settling time",
}


def camel(metric: str, upper: bool) -> str:
    """``eclipse reserve`` -> ``EclipseReserve`` (calc def) or ``eclipseReserve`` (an attribute)."""
    words = metric.split()
    head = words[0].title() if upper else words[0]
    return head + "".join(w.title() for w in words[1:])


def plain_name(ident: str) -> str:
    """``LaunchCost`` -> ``launch cost`` (the inverse of ``camel``)."""
    return re.sub(r"(?<!^)(?=[A-Z])", " ", ident).lower()


REQ_COLOUR = "#FDEBD0"
COVERED_COLOUR = "#E3F1E3"  # a metric some requirement reads
MOE_COLOUR = "#FFF4C2"  # an MoE the model computes from a traded metric, read by a requirement
MARKS = ("MoE", "MoP")


def mark_of(byid, element_id: str) -> str | None:
    """``MoE`` or ``MoP`` when the element's own doc begins with it (the model's mark)."""
    word = (
        doc_text(byid, element_id)
        .removeprefix("doc ")
        .split(":")[0]
        .strip()
    )
    return word if word in MARKS else None


ANALYSIS_COLOUR = (
    "#E1D8F0"  # the analysis def: its own colour, shared with no metric
)
MEASURE_COLOUR = "#E4E4E4"
RELATION_COLOUR = "#B5541C"
SOURCE_COLOUR = "#6B6B6B"


# ---- model access ---------------------------------------------------------------------------------
def load(path: pathlib.Path):
    conn = opensysml.connect()
    m = conn.load_from_content(path.read_text(), strict=False)
    assert m.ok, m.diagnostics
    els = json.loads(m.to_api_json().content)
    return m, {e["@id"]: e for e in els}


def ref(x):
    return x["@id"] if isinstance(x, dict) else x


def jid(qn: str) -> str:
    return qn.replace("::", "__")


def short(qn: str) -> str:
    return qn.split("::")[-1].split("__")[-1]


def fmt(v) -> str:
    mag = getattr(v, "magnitude", v)
    try:
        s = f"{float(mag):g}"
    except Exception:
        return str(v)
    unit = getattr(getattr(v, "unit", None), "text", None)
    return f"{s} {unit}" if unit else s


def doc_text(byid, prefix_id: str) -> str:
    """Prose of the `doc` comments directly under an element (its id plus a numbered suffix)."""
    out = []
    for i, e in byid.items():
        if (
            e["@type"] == "Documentation"
            and i.startswith(prefix_id + "__")
            and "__" not in i[len(prefix_id) + 2 :]
        ):
            out.append(
                " ".join(
                    e.get("sysx:sourceText", "")
                    .replace("/*", " ")
                    .replace("*/", " ")
                    .split()
                )
            )
    return " ".join(out)


def regime_of_gain_box() -> dict:
    """``{"aggressive": "primary", "baseline": "baseline"}``: the regime each gain box samples, read
    from the experiment definitions (``v2-primary`` samples the aggressive box); the box's own name
    when the definitions cannot be read."""
    try:
        sys.path.insert(0, str(REPO / "examples" / "adcs"))
        from experiments import definitions

        return {
            e.gain_box: e.id.removeprefix("v2-")
            for e in definitions.V2
            if e.id in ("v2-primary", "v2-baseline")
        }
    except Exception:
        return {}


def constraint_text(byid, req_id: str) -> str:
    """The requirement's ``require constraint { ... }`` in the model's own words (the braces' content)."""
    for i, e in byid.items():
        if e["@type"] == "ConstraintUsage" and i.startswith(
            req_id + "__"
        ):
            text = " ".join(e.get("sysx:sourceText", "").split())
            if "{" in text and "}" in text:
                return text[
                    text.index("{") + 1 : text.rindex("}")
                ].strip()
    return ""


# =================================================================================================
# View 1: the assembly
# =================================================================================================
def assembly(m, byid, P, revision=3, caption=None):
    rows = {
        r.id: r.properties | {"@type": r.type} for r in m.query(scope=P)
    }
    kids = lambda owner: [
        p for p in rows.values() if p.get("owner") == owner
    ]  # noqa: E731
    cub = f"{P}::Cubesat"
    default_attrs = {
        ref(e["featureWithValue"])
        for e in byid.values()
        if e["@type"] == "FeatureValue" and e.get("isDefault")
    }
    parts = [p for p in kids(cub) if p["@type"] == "PartUsage"]
    abstract = {
        p["@id"]
        for p in rows.values()
        if p["@type"] == "PartDefinition"
        and p.get("isAbstract") == "true"
    }
    alts: dict = {}
    for p in rows.values():
        if (
            p["@type"] == "PartDefinition"
            and p.get("general") in abstract
        ):
            alts.setdefault(p["general"], []).append(p["name"])
    enum_lits: dict = {}
    for p in rows.values():
        if p["@type"] == "EnumerationUsage":
            enum_lits.setdefault(p["owner"], []).append(p["name"])
    selector = {}
    for d in abstract:
        for a in kids(d):
            if (
                a["@type"] == "AttributeUsage"
                and a.get("type") in enum_lits
            ):
                selector[d] = a["type"]

    # continuous variables: defaulted attributes of the root, each placed ONCE in the part definition
    # whose usage binds it (a redefinition `:>> span = Cubesat::panelSpan`); defaulted attributes of
    # other part definitions that are bound from the root are the same variable, not new ones.
    var_at: dict = {}  # part def qualified name -> [variable names]
    bound_names: dict = {}  # part def -> redefined feature names (span, capacity)
    root_vars = [
        p
        for p in kids(cub)
        if p["@type"] == "AttributeUsage"
        and jid(p["@id"]) in default_attrs
    ]
    for v in root_vars:
        vid = jid(v["@id"])
        for e in byid.values():
            if (
                e["@type"]
                in (
                    "FeatureReferenceExpression",
                    "FeatureChainExpression",
                )
                and e.get("referent")
                and ref(e["referent"]) == vid
            ):
                parts_of = e["@id"].split("__")
                if len(parts_of) > 3 and parts_of[1] == "Cubesat":
                    usage = next(
                        (p for p in parts if p["name"] == parts_of[2]),
                        None,
                    )
                    if usage and v["name"] not in var_at.setdefault(
                        usage["type"], []
                    ):
                        var_at[usage["type"]].append(v["name"])
                        bound_names.setdefault(
                            usage["type"], set()
                        ).add(parts_of[3].split("_pvalue")[0])
    for d in {p["type"] for p in parts}:
        for a in kids(d):
            if (
                a["@type"] == "AttributeUsage"
                and jid(a["@id"]) in default_attrs
                and a["name"] not in bound_names.get(d, set())
            ):
                var_at.setdefault(d, []).append(a["name"])

    def tag(kind, name):
        word, colour = kind
        return f"  <back:{colour}><b> {word} </b></back> {name}"

    out = [
        "@startuml",
        ASSEMBLY_DIRECTION,
        f"skinparam linetype {ASSEMBLY_LINETYPE}",
        SKIN.format(nodesep=12, ranksep=34),
        f"scale {COLUMN_WIDTH} width",
        "",
    ]
    out.append('class "Cubesat\\n<<part def>>" as Cubesat #E8EEF7')
    declared: set = set()

    def define(defqn, ranked):
        if defqn in declared:
            return
        declared.add(defqn)
        n = short(defqn)
        kind = "abstract part def" if defqn in abstract else "part def"
        body = []
        if defqn in selector:
            body.append(tag(TAG_CATEGORICAL, short(selector[defqn])))
        for v in var_at.get(defqn, []):
            body.append(tag(TAG_CONTINUOUS, v))
        used = ", ".join(p["name"] for p in parts if p["type"] == defqn)
        title = f"**{n}**" + (f"\\n({used})" if used else "")
        title += "\\n<<abstract>>" if defqn in abstract else ""
        out.append(f'class "{title}" as {n} {{')
        out.extend(body)
        out.append("}")

    for p in parts:
        define(p["type"], True)
    for p in parts:
        t = p["type"]
        if f"Cubesat *-- {short(t)}" not in out:
            out.append(f"Cubesat *-- {short(t)}")

    def literal_rank(t, alt):
        """Position of the enum literal the alternative's part def binds (``:>> grade = TrackerGrade::fine``)."""
        lits = [short(x) for x in enum_lits.get(selector.get(t), [])]
        pre_alt = f"{P}::{alt}".replace("::", "__") + "__"
        for i, e in byid.items():
            if i.startswith(pre_alt) and i.endswith(
                "_pvalue_preferent"
            ):
                lit = short(ref(e["memberElement"]))
                if lit in lits:
                    return lits.index(lit)
        return len(lits)

    ordered = {
        p["type"]: sorted(
            alts.get(p["type"], []),
            key=lambda a, t=p["type"]: (literal_rank(t, a), a),
        )
        for p in parts
    }
    for p in parts:
        t = p["type"]
        for a in ordered[t]:
            define(f"{P}::{a}", False)
    for p in parts:
        t = p["type"]
        for a in ordered[t]:
            out.append(f"{short(t)} <|-- {a}")

    pr = lambda n: fmt(m.eval(f"{P}::designRanges.{n}"))  # noqa: E731
    gb = lambda inst, n: fmt(m.eval(f"{P}::{inst}.{n}"))  # noqa: E731
    out.append("")
    out.append("legend bottom")
    out.append(
        "  **Configuration variables** (each marked once, in the part it belongs to)"
    )
    out.append(
        tag(
            TAG_CATEGORICAL,
            "categorical: a part is swapped for one of its alternatives",
        )
    )
    out.append(
        tag(
            TAG_CONTINUOUS,
            "continuous: a parameter of a part is tuned within a range",
        )
    )
    if revision >= 4:
        fixed = [
            short(d)
            for d in dict.fromkeys(p["type"] for p in parts)
            if d not in selector and not var_at.get(d)
        ]
        untagged = (
            "untagged: fixed"
            if revision >= 5
            else "no tag: a fixed part"
        )
        out.append(f"  {untagged} ({', '.join(fixed)})")
    # revision 5: the levels and ranges are the caption's; the legend keeps the tag keys
    legend_end = len(out) if revision >= 5 else None
    out.append("  ")
    out.append("  **Levels and ranges** (read from the model)")
    for d, en in sorted(selector.items()):
        out.append(f"  {short(en)}: {' | '.join(enum_lits[en])}")
    out.append(
        f"  panelSpan: {pr('panelSpanMin')} .. {pr('panelSpanMax')}"
    )
    out.append(
        f"  batteryCapacity: {pr('batteryCapacityMin')} .. {pr('batteryCapacityMax')}"
    )
    boxes = [
        short(p["@id"])
        for p in rows.values()
        if p["@type"] == "PartUsage"
        and p.get("owner") == P
        and short(p.get("type", "")) == "GainBox"
    ]
    if revision >= 4:
        regime = regime_of_gain_box()
        label = lambda b: (
            f"{regime.get(b.removesuffix('Gains'), b)} regime"
        )  # noqa: E731
        out.append("  Gains Kp and Kd: one range per regime")
        both = "both regimes"
    else:
        label = lambda b: f"{b.removesuffix('Gains')} gains"  # noqa: E731
        out.append(
            "  Gains Kp and Kd: one range per dataset (baseline, aggressive)"
        )
        both = "both datasets"
    for g in ("Kp", "Kd"):
        spans = {
            b: f"{gb(b, g + 'Min')} .. {gb(b, g + 'Max')}"
            for b in boxes
        }
        if len(set(spans.values())) == 1:
            out.append(f"  {g}: {next(iter(spans.values()))} ({both})")
        else:
            out.append(
                f"  {g}: "
                + "; ".join(
                    f"{v} ({label(b)})" for b, v in spans.items()
                )
            )
    if legend_end is not None:
        ranges = [line.strip() for line in out[legend_end + 2 :]]
        if caption is not None:
            caption.extend(ranges)
        del out[legend_end:]
    out.append("end legend")
    out.append("@enduml")
    return "\n".join(out) + "\n"


# =================================================================================================
# View 2: the behavioural view (subsystems, requirements, traded metrics)
# =================================================================================================
class Reads:
    """What each definition reads, derived from the model JSON by id prefix (an element's id begins
    with its owner's id)."""

    def __init__(self, byid, P):
        self.byid, self.P = byid, P
        self.pre = P.replace("::", "__") + "__"
        self.calcs = {
            i
            for i, e in byid.items()
            if e["@type"] == "CalculationDefinition"
        }
        self.cub_attrs = {
            short(i): i
            for i, e in byid.items()
            if e["@type"] == "AttributeUsage"
            and e["@id"].startswith(self.pre + "Cubesat__")
            and e["@id"].count("__") == self.pre.count("__") + 1
        }
        self._direct: dict = {}

    def inside(self, root_id):
        return [
            e
            for i, e in self.byid.items()
            if i.startswith((root_id + "__", root_id + "_pvalue"))
        ]

    def direct(self, root_id) -> set:
        """Calc defs invoked inside root_id, plus those behind a Cubesat attribute it reads (c.availablePower)."""
        if root_id in self._direct:
            return self._direct[root_id]
        found = set()
        for e in self.inside(root_id):
            if (
                e["@type"] == "InvocationExpression"
                and e.get("function")
                and ref(e["function"]) in self.calcs
            ):
                found.add(ref(e["function"]))
            elif e["@type"] == "FeatureChainExpression":
                last = (
                    e.get("sysx:sourceText", "").split(".")[-1].strip()
                )
                if last in self.cub_attrs:
                    found |= self.direct(self.cub_attrs[last])
        self._direct[root_id] = found
        return found

    def closure(self, root_id) -> set:
        seen, todo = set(), list(self.direct(root_id))
        while todo:
            c = todo.pop()
            if c not in seen:
                seen.add(c)
                todo.extend(self.direct(c))
        return seen

    def measured(self, root_id) -> set:
        """Names X of `baselineMeasurement.X` read inside root_id."""
        out = set()
        for e in self.inside(root_id):
            if e["@type"] == "FeatureChainExpression":
                s = e.get("sysx:sourceText", "").replace(" ", "")
                if s.startswith("baselineMeasurement."):
                    out.add(s.split(".", 1)[1])
        return out


def behavioural(m, byid, P, revision=3):
    sys.path.insert(0, str(REPO / "examples" / "adcs"))
    import case  # the CaseSpec: the metrics, in order, and their subsystems

    spec = case.CUBESAT
    metrics = [
        (spec.short[a], spec.subsystems[a]) for a in spec.attributes
    ]
    order = list(spec.subsystem_order)
    pre = P.replace("::", "__") + "__"
    rd = Reads(byid, P)

    # --- the model's requirement, satisfy, verify and analysis elements -------------------------
    reqs = sorted(
        i
        for i, e in byid.items()
        if e["@type"] == "RequirementDefinition"
        and ref(e["owner"]) == pre[:-2]
    )
    typing = {}
    for t in byid.values():
        if t["@type"] == "FeatureTyping":
            typing[ref(t["typedFeature"])] = ref(t["type"])
    satisfied_by = {r: set() for r in reqs}
    for e in byid.values():
        if e["@type"] == "SatisfyRequirementUsage":
            req_usage = ref(e["subsets"])
            if typing.get(req_usage) in satisfied_by:
                satisfied_by[typing[req_usage]].add(
                    short(ref(e["subject"]))
                )
    verified_by = {r: set() for r in reqs}
    for vid, v in byid.items():
        if v["@type"] == "VerificationCaseDefinition":
            for e in byid.values():
                if (
                    e["@type"] == "RequirementUsage"
                    and e["@id"].startswith(vid + "__")
                    and typing.get(e["@id"]) in verified_by
                ):
                    verified_by[typing[e["@id"]]].add(short(vid))
    analysis = next(
        i
        for i, e in byid.items()
        if e["@type"] == "AnalysisCaseDefinition"
    )
    a_inv = {
        ref(e["function"])
        for e in rd.inside(analysis)
        if e["@type"] == "InvocationExpression" and e.get("function")
    }
    a_chain = {
        e.get("sysx:sourceText", "").split(".")[-1].strip()
        for e in rd.inside(analysis)
        if e["@type"] == "FeatureChainExpression"
    }
    a_refs = {
        short(ref(e["referent"]))
        for e in rd.inside(analysis)
        if e["@type"] == "FeatureReferenceExpression"
        and e.get("referent")
    }
    a_text = doc_text(byid, pre[:-2]).replace(
        "-", " "
    )  # the package-level prose of section 6
    meas_attrs = {
        short(i)
        for i, e in byid.items()
        if e["@type"] == "AttributeUsage"
        and i.startswith(pre + "SlewMeasurement__")
    }

    # --- where each metric comes from: the element of the model that carries the metric's name ------
    # a CaseSpec metric the model has no element for is not traded by this model (the revision of
    # WP23 has no slew time) and leaves the list
    origin, mcalc, METRIC_ELEMENT, mark, element_of = {}, {}, {}, {}, {}
    for name, _ in list(metrics):
        calc_id, attr_id = pre + camel(name, True), camel(name, False)
        if calc_id in rd.calcs and calc_id in a_inv:
            kind, ident = "calc", camel(name, True)
            origin[name], mcalc[name] = "analysis", calc_id
            element_of[name] = calc_id
        elif attr_id in rd.cub_attrs and attr_id in a_chain:
            kind, ident = "attr", attr_id
            origin[name], mcalc[name] = "analysis", None
            element_of[name] = rd.cub_attrs[attr_id]
        elif attr_id in meas_attrs:
            kind, ident = "measured", attr_id
            origin[name], mcalc[name] = "measurement", None
            element_of[name] = pre + "SlewMeasurement__" + attr_id
        elif attr_id in a_refs:
            kind, ident = "input", attr_id
            origin[name], mcalc[name] = "measurement", None
            element_of[name] = pre + "SlewMeasurement__" + attr_id
        else:
            metrics = [m for m in metrics if m[0] != name]
            continue
        METRIC_ELEMENT[name] = (kind, ident)
        mark[name] = (
            mark_of(byid, element_of[name])
            if element_of[name] in byid
            else None
        )
    assert metrics, "the model carries none of the CaseSpec's metrics"
    idx = {n: k for k, (n, _) in enumerate(metrics)}
    # calcs the model marks MoE that are not traded themselves: an MoE computed from a traded metric
    # (the launch cost from the total mass), drawn between the requirement that reads it and the
    # metric it reads
    moe_calcs = {
        c: (
            short(c),
            [
                n
                for n, (k, ident) in METRIC_ELEMENT.items()
                if (
                    k == "attr"
                    and rd.cub_attrs[ident]
                    in {
                        rd.cub_attrs[
                            e.get("sysx:sourceText", "")
                            .split(".")[-1]
                            .strip()
                        ]
                        for e in rd.inside(c)
                        if e["@type"] == "FeatureChainExpression"
                        and e.get("sysx:sourceText", "")
                        .split(".")[-1]
                        .strip()
                        in rd.cub_attrs
                    }
                )
                or (k == "calc" and mcalc[n] in rd.direct(c))
            ],
        )
        for c in rd.calcs
        if mark_of(byid, c) == "MoE" and c not in set(mcalc.values())
    }

    # metric -> the calcs it reads directly / transitively
    def m_direct(name):
        kind, ident = METRIC_ELEMENT[name]
        if kind == "calc":
            return {mcalc[name]} | rd.direct(mcalc[name])
        if kind == "attr":
            return rd.direct(rd.cub_attrs[ident])
        return set()

    def m_closure(name):
        s = set(m_direct(name))
        for c in list(s):
            s |= rd.closure(c)
        return s

    # --- relations requirement - metric, with the evidence for each -------------------------------
    rel = []  # (req, metric, strength, evidence)
    for r in reqs:
        rdir, rcl, rmeas = rd.direct(r), rd.closure(r), rd.measured(r)
        rdoc = doc_text(byid, r).replace("-", " ")
        for name, _ in metrics:
            kind, ident = METRIC_ELEMENT[name]
            same = []
            if kind == "measured" and ident in rmeas:
                same.append(ident)
            # strong: the requirement invokes the metric's own calc, or the calc that computes the
            # metric's attribute (MassAccounting for total mass); not a calc the metric's calc
            # invokes (PowerMargin calls PeakSlewPower, and the peak-slew-power requirement is not
            # a bound on the power margin)
            if kind == "calc":
                own = {mcalc[name]}
            elif kind == "attr":
                own = rd.direct(rd.cub_attrs[ident])
            else:
                own = set()
            same += [short(c) for c in sorted(rdir & own)]
            if same:
                rel.append((r, name, "strong", ", ".join(same)))
                continue
            up = [short(c) for c in sorted(rcl & m_closure(name))]
            if up:
                rel.append((r, name, "weak", ", ".join(up)))
                continue
            if PROSE_NAME.get(name) and PROSE_NAME[name] in rdoc:
                rel.append((r, name, "prose", "prose"))
        # the requirement reads an MoE calc that reads the metric: a line through the MoE box
        for c, (cname, reads) in moe_calcs.items():
            if c in rdir:
                for name in reads:
                    rel.append((r, name, "moe", cname))

    # a requirement is placed in a subsystem by every relation it has (rel_all), but a line is drawn only
    # where the requirement reads the metric itself (strong) or the MoE computed from it (moe). A shared
    # upstream calc is not a bound on the metric (PowerMargin calls PeakSlewPower, and no requirement
    # bounds the peak slew power).
    rel_all = rel
    rel = [x for x in rel_all if x[2] in ("strong", "moe")]

    def req_subsystem(r):
        votes = [dict(metrics)[n] for rr, n, _, _ in rel if rr == r]
        return (
            max(order, key=lambda s: votes.count(s)) if votes else None
        )

    band = {r: req_subsystem(r) for r in reqs}
    no_line = sorted(
        r for r in reqs if band[r] is None
    )  # the requirements no traded metric reads
    related = {n for _, n, _, _ in rel}
    # a metric with no requirement is open: the model says so itself, in a verification case's doc
    ver_docs = " ".join(
        doc_text(byid, vid)
        for vid, v in byid.items()
        if v["@type"] == "VerificationCaseDefinition"
    )
    ver_docs = " ".join(ver_docs.replace("-", " ").split())
    for name, _ in metrics:
        if name not in related:
            assert name in ver_docs, (
                f"{name!r} is traded with no requirement and no verification case doc says so"
            )

    # a requirement whose doc says it is "the same statement as the <other> requirement" says so in its box
    # (the picture then carries what the caption would otherwise): the first sentence of the doc, then the twin
    def same_as(r):
        d = doc_text(byid, r).replace("-", " ").removeprefix("doc ")
        k = d.find("same statement as the ")
        if k < 0:
            return None
        tail = d[k + len("same statement as the ") :].lower()
        twin = next(
            (
                short(o)
                for o in reqs
                if o != r
                and " ".join(
                    re.findall(r"[A-Z][a-z]*", short(o))
                ).lower()
                in tail
            ),
            None,
        )
        first = d.split(":")[0].split(". ")[0].strip().rstrip(".")
        return first, twin

    # --- PlantUML ------------------------------------------------------------------------------
    nid = lambda s: (
        "x" + "".join(ch for ch in s.title() if ch.isalnum())
    )  # noqa: E731
    out = [
        "@startuml",
        BEHAVIOUR_DIRECTION,
        f"skinparam linetype {BEHAVIOUR_LINETYPE}",
        # revision 5: nodesep is the gap between boxes at one rank (the launch cost and the
        # total mass): 16 gives their line room for its label; height, not width, pays for it
        SKIN.format(
            nodesep=16 if revision >= 5 else 8,
            ranksep=36 if revision < 4 else 12,
        ),
        f"scale {COLUMN_WIDTH} width",
        "",
    ]
    bands = list(order)
    # layout: subsystems fed by the measurement come first, so the measurement box sits beside them and
    # the analysis box beside the rest; no source arrow then crosses another subsystem
    last_stack_head = None
    bands = sorted(
        bands,
        key=lambda s: (
            -sum(
                origin[n] == "measurement"
                for n, sub in metrics
                if sub == s
            )
        ),
    )
    # revision 4: what every requirement box shares is said once in the caption; a box carries only
    # what differs between the requirements (the verification case, the satisfying configuration)
    sat_differs = (
        len({tuple(sorted(v)) for v in satisfied_by.values()}) > 1
    )
    ver_differs = (
        len({tuple(sorted(v)) for v in verified_by.values()}) > 1
    )

    def req_box_r4(r, with_constraint=False):
        lines = [f"**{short(r)}**"]
        if with_constraint:
            lines.append(constraint_text(byid, r))
        if ver_differs:
            lines.append(
                ", ".join(sorted(verified_by[r]))
                or "verified: none in the model"
            )
        if sat_differs:
            lines.append(
                "satisfied by "
                + (", ".join(sorted(satisfied_by[r])) or "none")
            )
        sa = same_as(r)
        if sa:
            lines += [f"{sa[0]};", f"same statement as {sa[1]}"]
        body = "\\n".join(lines)
        return f'rectangle "{body}" as {nid(short(r))} {REQ_COLOUR}'

    lane = (
        (lambda s: f"{s} (the analyst's grouping)")
        if revision >= 4
        else (lambda s: s)
    )  # noqa: E731
    for s in bands:
        out.append(f'package "{lane(s)}" {{')
        smets = sorted(
            (n for n, sub in metrics if sub == s),
            key=lambda n: (
                n not in related,
                origin[n] != "measurement",
                idx[n],
            ),
        )
        first = lambda r: min(
            (
                smets.index(n)
                for rr, n, _, _ in rel
                if rr == r and n in smets
            ),
            default=99,
        )  # noqa: E731
        sreqs = sorted((r for r in reqs if band[r] == s), key=first)
        with_line = [r for r in sreqs]

        def req_box(r):
            sat = (
                ", ".join(sorted(satisfied_by[r]))
                or "none in the model"
            )
            ver = (
                ", ".join(sorted(verified_by[r])) or "none in the model"
            )
            sa = same_as(r)
            extra = (
                f"\\n{sa[0]};\\nsame statement as {sa[1]}" if sa else ""
            )
            return (
                f'rectangle "**{short(r)}**\\n<<requirement def>>\\n<<satisfy>> {sat}\\n<<verify>> {ver}{extra}" '
                f"as {nid(short(r))} {REQ_COLOUR}"
            )

        for r in with_line:
            out.append(
                "  " + (req_box_r4(r) if revision >= 4 else req_box(r))
            )
        if not sreqs:
            out.append(
                f'  rectangle "no requirement def\\nlands on this subsystem" as {nid("none" + s)} #FFFFFF;line:gray;line.dashed;text:gray'
            )
        # an MoE box in the subsystem of the metric it reads
        for c, (cname, reads) in moe_calcs.items():
            if any(dict(metrics)[n] == s for n in reads):
                out.append(
                    f'  rectangle "{plain_name(cname)}\\n<<MoE>>\\n{cname}" as {nid(cname)} {MOE_COLOUR}'
                )
        for n in smets:
            label = f"{n}\\n<<{mark[n]}>>" if mark.get(n) else n
            if revision >= 4:
                # the element the requirement reads (the metric's calc or measured attribute), in
                # the box; the line then carries no label and the ranks sit closer
                read = sorted(
                    {
                        ev
                        for rr, nn, st, ev in rel
                        if nn == n and st == "strong"
                    }
                    | {
                        METRIC_ELEMENT[n][1]
                        for rr, nn, st, ev in rel
                        if nn == n and st == "moe"
                    }
                )
                if read:
                    label += "\\n" + ", ".join(read)
            if n in related:
                out.append(
                    f'  rectangle "{label}" as {nid(n)} {COVERED_COLOUR}'
                )
            else:
                out.append(
                    f'  rectangle "{label}\\n(no requirement)" as {nid(n)} #FFFFFF;line:black;line.dashed'
                )
        out.append("}")
        # order inside the subsystem: the requirements with a line above those without; metrics top to bottom
        stack = [nid(short(r)) for r in with_line] + (
            [nid("none" + s)] if not sreqs else []
        )
        for u, v in zip(stack, stack[1:]):
            out.append(f"{u} -[hidden]right-> {v}")
        smets_last = smets[-1] if smets else None
        for u, v in zip(smets, smets[1:]):
            out.append(f"{nid(u)} -[hidden]right-> {nid(v)}")
        if stack and smets:
            out.append(f"{stack[0]} -[hidden]-> {nid(smets[0])}")
        last_stack_head = stack[0] if stack else last_stack_head
    if revision >= 5:
        group_title = "requirements that read no traded metric"
        group_text = ""  # the body's black: the title is read with the lane titles
    elif revision >= 4:
        group_title, group_text = (
            "requirements reading no traded metric",
            ";text:gray",
        )
    else:
        group_title = "requirements with no line to a traded metric"
        group_text = ";text:gray"
    out.append(
        f'rectangle "{group_title}" as xNoLine #FFFFFF;line:gray;line.dashed{group_text} {{'
    )
    for r in no_line:
        if revision >= 4:
            out.append("  " + req_box_r4(r, with_constraint=True))
            continue
        sat = ", ".join(sorted(satisfied_by[r])) or "none in the model"
        ver = ", ".join(sorted(verified_by[r])) or "none in the model"
        out.append(
            f'  rectangle "**{short(r)}**\\n<<requirement def>>\\n<<satisfy>> {sat}\\n<<verify>> {ver}" as {nid(short(r))} {REQ_COLOUR}'
        )
    chain = "-[hidden]->" if revision >= 4 else "-[hidden]right->"
    for u, v in zip(no_line, no_line[1:]):
        out.append(f"  {nid(short(u))} {chain} {nid(short(v))}")
    out.append("}")
    if revision >= 4 and last_stack_head:
        # the group hangs off the last lane's first requirement: it then spans the lanes' width
        # and adds no rank; the lanes' width is what the column scales
        out.append(f"{last_stack_head} -[hidden]right-> xNoLine")
    else:
        out.append(f"xNoLine -[hidden]right-> {nid(smets_last)}")
    out.append("")
    n_analysis = sum(v == "analysis" for v in origin.values())
    pad = "\\n" * ANALYSIS_BOX_PAD
    out.append(
        f'rectangle "**SlewExperiment**\\n<<analysis def>>\\ncomputes {n_analysis} of the {len(metrics)}\\nmetrics from the\\nconfiguration and the\\nmeasured inputs{pad}" as xAnalysis {ANALYSIS_COLOUR}'
    )
    out.append(
        f'rectangle "**SlewMeasurement**\\nmeasured slew:\\nsimulation here;\\nfield data when\\nfielded" as xMeasure {MEASURE_COLOUR}'
    )
    out.append("xMeasure -[hidden]right-> xAnalysis")
    out.append("")
    drawn_moe = set()
    head = (
        "-" if revision >= 4 else "->"
    )  # a shared quantity has no direction; a source does
    tag = (lambda ev: "") if revision >= 4 else (lambda ev: f" : {ev}")  # noqa: E731
    # revision 5: the MoE box and the metric it reads sit at one rank, joined by a short line that
    # was missed cold; it carries the element the two share (totalMass). The requirement's line to
    # the MoE box stays unlabelled: a label between ranks widens the whole layout (0.65 px of type)
    # and the box it lands on names the element (LaunchCost).
    moe_tag = (lambda ev: f" : {ev}") if revision >= 5 else tag  # noqa: E731
    for r, n, strength, ev in rel:
        if strength == "strong":
            out.append(
                f"{nid(short(r))} -[#{RELATION_COLOUR[1:]},thickness=2]{head} {nid(n)}{tag(ev)}"
            )
        elif strength == "moe":
            # requirement -> the MoE box (once per requirement and MoE) -> the metric it reads
            if (r, ev) not in drawn_moe:
                out.append(
                    f"{nid(short(r))} -[#{RELATION_COLOUR[1:]},thickness=2]{head} {nid(ev)}{tag(ev)}"
                )
                drawn_moe.add((r, ev))
            if (ev, n) not in drawn_moe:
                kind, ident = METRIC_ELEMENT[n]
                # revision 4: the MoE box sits at the metrics' rank, beside the metric it reads
                # (a same-rank line), so the mass lane adds no rank to the layout
                side = "right" if revision >= 4 else ""
                out.append(
                    f"{nid(ev)} -[#{RELATION_COLOUR[1:]},thickness=2]{side}{head} {nid(n)}{moe_tag(ident)}"
                )
                drawn_moe.add((ev, n))
        else:
            raise AssertionError(
                "only strong and moe relations are drawn"
            )
    for name, _ in metrics:
        src = "xAnalysis" if origin[name] == "analysis" else "xMeasure"
        out.append(f"{nid(name)} <-[#{SOURCE_COLOUR[1:]}]- {src}")
    out.append("")
    if revision >= 4:
        out.append("legend bottom")
        out.append(
            "  orange: requirement; green: traded metric; yellow: derived, not traded"
        )
        out.append("end legend")
        out.append("@enduml")
        return "\n".join(out) + "\n", {
            "rel": rel,
            "rel_all": rel_all,
            "metric_element": METRIC_ELEMENT,
            "related": related,
            "reqs": reqs,
            "band": band,
            "metrics": metrics,
            "origin": origin,
            "satisfied": satisfied_by,
            "verified": verified_by,
        }
    out.append("legend bottom")
    out.append(
        "  **Requirement - metric** (orange line, requirement to metric; the shared quantity on the line)"
    )
    out.append(
        "  every line: the requirement and the metric read the same calc or measured quantity"
    )
    if any(mark.values()):
        out.append(
            "  <<MoE>> / <<MoP>>: the model's mark on each traded metric, a measure of effectiveness"
            " (a stakeholder's) or of performance (the engineer's scenario)"
        )
    if moe_calcs:
        out.append(
            "  yellow: an MoE the model computes from a traded metric; the requirement reads the MoE"
            " and the MoE reads the metric (two lines)"
        )
    unrelated = [n for n, _ in metrics if n not in related]
    out.append(
        '  green: a requirement reads the metric; dashed, "no requirement": traded, no requirement reads it'
        if unrelated
        else "  green: a requirement reads the metric (every traded metric has one)"
    )
    if unrelated:
        out.append(
            "  (the model names each of those as open in its verification cases)"
        )
    out.append(
        "  **Source** (grey line): from the analysis def (lilac) or from the measurement of the slew (grey)"
    )
    out.append(
        "  Requirement placement in a subsystem is the analyst's reading (CaseSpec groups metrics)"
    )
    out.append("end legend")
    out.append("@enduml")
    return "\n".join(out) + "\n", {
        "rel": rel,
        "rel_all": rel_all,
        "metric_element": METRIC_ELEMENT,
        "related": related,
        "reqs": reqs,
        "band": band,
        "metrics": metrics,
        "origin": origin,
        "satisfied": satisfied_by,
        "verified": verified_by,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("outdir")
    ap.add_argument("--package", default="CubesatTradeSpaceV2")
    ap.add_argument(
        "--facts",
        action="store_true",
        help="print the derived relations",
    )
    ap.add_argument(
        "--revision",
        type=int,
        default=3,
        choices=(3, 4, 5),
        help="drawing revision (3: the committed views of the adopted model; 4: WP23 round 3; 5: WP23 round 4)",
    )
    a = ap.parse_args()
    m, byid = load(pathlib.Path(a.model))
    od = pathlib.Path(a.outdir)
    od.mkdir(parents=True, exist_ok=True)
    caption: list = []
    (od / "assembly_view.puml").write_text(
        assembly(m, byid, a.package, a.revision, caption)
    )
    if a.revision >= 5:
        (od / "assembly_caption.md").write_text(
            "Levels and ranges (read from the model by the views generator):\n\n"
            + "".join(f"- {line}\n" for line in caption)
        )
    text, facts = behavioural(m, byid, a.package, a.revision)
    (od / "behavioural_view.puml").write_text(text)
    if a.facts:
        for r, n, s, ev in facts["rel"]:
            print(f"{short(r):32s} {n:20s} {s:7s} {ev}")
        for r in facts["reqs"]:
            print(
                short(r),
                "band:",
                facts["band"][r],
                "satisfy:",
                sorted(facts["satisfied"][r]),
                "verify:",
                sorted(facts["verified"][r]),
            )
    print("ok")
