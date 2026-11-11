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
adopted at WP23's gate has no slew time); a metric's MoE or MoP mark (the first word of the ``doc`` on
its element) is written in its box; a calc the model marks MoE that is not itself traded (the launch
cost on the total mass) is drawn as a box between the requirement that reads it and the metric it
reads. On a model without marks (the adopted ``cubesat.sysml``) the output is unchanged.
Revision 4 (WP23 round 3, the round-1 cold reads' dispositions; ``--revision 4``): the legend of
each view is cut to what the image needs (the colour key; the rest is the caption's, ``INTENT.md``); one colour rule, orange a requirement, green a
traded metric, yellow a derived quantity that is not traded, the MoE or MoP mark by stereotype only;
the requirement boxes carry the name and only what differs between them (the verification case),
and a requirement that reads no traded metric carries its constraint in the model's words; the
requirement-metric relation is a headless line (a shared quantity) and the source lines keep the one
arrowhead (where a metric comes from); the subsystem lanes are titled as the analyst's grouping; the
assembly legend names the untagged parts as fixed and the gain ranges by regime (read from
``experiments/definitions.py``).
Revision 5 (WP23 round 4, the round-3 cold reads' dispositions; the default since the data gate
swapped the committed views, ``--revision 3`` draws the earlier ones): the short line
from the launch cost to the total mass (two boxes at one rank) carries the element the two share,
``totalMass``, so the chain requirement -> launch cost -> total mass reads at 700 px (a label on the
requirement's line too would cost the whole figure 0.65 px of type: a label between ranks widens the
layout); the group of requirements that read no
traded metric is titled in those words, in the body's black; the assembly legend keeps the two tag
keys and the untagged rule, and the levels and ranges go to the caption (``assembly_caption.md``,
written beside the views, still read from the model).
Revision 9 (WP23 close-out, the default): a negated ``satisfy`` (``not satisfy R by X``, the model's
statement that the configuration X fails the requirement R; the baseline configuration and the
pointing-error requirement) is read apart from the satisfied ones: the requirement's box says
"not satisfied by X" and the caption names it; earlier revisions read every ``satisfy`` as satisfied.
Revision 9, WP30 (the momentum headroom traded; D-2 (a) of spike C): the caption names each requirement
in the box with its computed reason, the sentence ``examples/adcs/model_v2/coverage.py`` prints in
``coverage.md`` from the same computation (``box_reasons``), for the model the command line is given.
"""

from __future__ import annotations

import argparse
import importlib.util
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
def assembly(m, byid, P, revision=6, caption=None):
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
    selector_attr = {}  # revision 6: the swap tag names the attribute, as the tune tags do
    for d in abstract:
        for a in kids(d):
            if (
                a["@type"] == "AttributeUsage"
                and a.get("type") in enum_lits
            ):
                selector[d] = a["type"]
                selector_attr[d] = a["name"]

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

    if revision >= 6:
        # revision 6: the composition lines are routed clear of the box headers by the order of the
        # parts in the row. Lines run from the root down to each box's top edge, and a line passes
        # a neighbour at the same height with a margin of only (slope x gap): the boxes of the
        # greatest height (the abstract parts and the part with most tags) are spread along the row
        # with a shorter box between any two, and the shorter boxes keep the model's order.
        def box_rows(t):
            n = 1 + (1 if any(p["type"] == t for p in parts) else 0)
            n += 1 if t in abstract else 0
            return (
                n + (1 if t in selector else 0) + len(var_at.get(t, []))
            )

        kinds_in_order = list(dict.fromkeys(p["type"] for p in parts))
        tallest = max(box_rows(t) for t in kinds_in_order)
        tall = [t for t in kinds_in_order if box_rows(t) == tallest]
        short_ = [t for t in kinds_in_order if box_rows(t) != tallest]
        slots = [
            round(k * (len(kinds_in_order) - 1) / max(len(tall) - 1, 1))
            for k in range(len(tall))
        ]
        row = [None] * len(kinds_in_order)
        for slot, t in zip(slots, tall):
            row[slot] = t
        fill = iter(short_)
        row = [t if t is not None else next(fill) for t in row]
        parts = sorted(parts, key=lambda p: row.index(p["type"]))

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
            body.append(
                tag(
                    TAG_CATEGORICAL,
                    selector_attr[defqn]
                    if revision >= 6
                    else short(selector[defqn]),
                )
            )
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
        # revision 6: the swap is named by its attribute, as in its tag; the enum is the type of that
        # attribute and the coverage table's name for the decision element
        name = (
            f"{selector_attr[d]} (enum {short(en)})"
            if revision >= 6
            else short(en)
        )
        out.append(f"  {name}: {' | '.join(enum_lits[en])}")
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
            + (f", {b}" if revision >= 6 else "")
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


def box_reasons(path) -> dict:
    """The sentence for each requirement in the box, by requirement name (WP30, D-2 (a)).

    Computed by ``coverage.box_reasons`` from the model at ``path`` and the data of record, so the
    caption and ``coverage.md`` print one sentence; None where the requirement has no reason.
    """
    spec = importlib.util.spec_from_file_location(
        "coverage_table",
        REPO / "examples" / "adcs" / "model_v2" / "coverage.py",
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = (
        module  # dataclasses resolve annotations through sys.modules
    )
    spec.loader.exec_module(module)
    graph = module.ModelGraph(pathlib.Path(path).read_text())
    return {
        r["requirement"]: r["sentence"]
        for r in module.box_reasons(graph, graph.metrics())
    }


def behavioural(m, byid, P, revision=9, reasons=None):
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
    fails_by = {
        r: set() for r in reqs
    }  # revision 9: the negated satisfy statements
    for e in byid.values():
        if e["@type"] == "SatisfyRequirementUsage":
            req_usage = ref(e["subsets"])
            if typing.get(req_usage) in satisfied_by:
                negated = revision >= 9 and e.get("isNegated")
                (fails_by if negated else satisfied_by)[
                    typing[req_usage]
                ].add(short(ref(e["subject"])))
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

    # --- what the analysis returns, and which returned entries need no slew ---------------------------
    # the analysis's `in` parameters other than its subject are the measured inputs; a returned entry
    # needs the slew when its expression reads one of them, or its calc (or the attribute's) reads
    # the baseline measurement
    params = {
        i
        for i, e in byid.items()
        if e["@type"] == "ReferenceUsage"
        and i.startswith(analysis + "__")
        and i.count("__") == analysis.count("__") + 1
        and short(i) not in ("cubesat", "attributes")
    }
    entry_root = analysis + "__attributes_pvalue_pa"

    def entry_of(name):
        kind, ident = METRIC_ELEMENT[name]
        for i, e in byid.items():
            if not (
                i.startswith(entry_root)
                and i[len(entry_root) :].isdigit()
            ):
                continue
            if (
                kind == "calc"
                and e.get("function")
                and ref(e["function"]) == mcalc[name]
            ):
                return i
            if (
                kind == "attr"
                and e["@type"] == "FeatureChainExpression"
                and e.get("sysx:sourceText", "").split(".")[-1].strip()
                == ident
            ):
                return i
        return None

    def needs_slew(name):
        kind, ident = METRIC_ELEMENT[name]
        if origin[name] == "measurement":
            return True
        entry = entry_of(name)
        reads = (  # the entry's nested expressions have ids beginning with its own
            [
                e
                for i, e in byid.items()
                if i == entry or i.startswith(entry + "_p")
            ]
            if entry
            else []
        )
        if any(
            e["@type"] == "FeatureReferenceExpression"
            and e.get("referent")
            and ref(e["referent"]) in params
            for e in reads
        ):
            return True
        roots = (
            {mcalc[name]} | rd.closure(mcalc[name])
            if kind == "calc"
            else {rd.cub_attrs[ident]} | rd.direct(rd.cub_attrs[ident])
        )
        roots = roots | {c for r in roots for c in rd.closure(r)}
        return any(rd.measured(r) for r in roots)

    cfg_only = [
        n
        for n, _ in metrics
        if origin[n] == "analysis" and not needs_slew(n)
    ]
    # returned = computed by the analysis, or an `in` of the analysis returned unchanged
    passed = [
        n
        for n, _ in metrics
        if origin[n] == "measurement" and camel(n, False) in a_refs
    ]
    returned = [
        n for n, _ in metrics if origin[n] == "analysis"
    ] + passed
    read_only = [
        n
        for n, _ in metrics
        if origin[n] == "measurement" and n not in passed
    ]
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
            nodesep=(24 if revision >= 7 else 16)
            if revision >= 5
            else 8,
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
        len(
            {
                tuple(sorted(v))
                for r, v in satisfied_by.items()
                if not fails_by[r]
            }
        )
        > 1
    )
    ver_differs = (
        len({tuple(sorted(v)) for v in verified_by.values()}) > 1
    )

    def req_box_r4(r, with_constraint=False):
        lines = [f"**{short(r)}**"]
        if with_constraint:
            c_text = constraint_text(byid, r)
            if revision >= 7:
                # revision 7: the statement breaks before its comparison, so a box is no wider than
                # its name and the three boxes of the group stand side by side in the column
                c_text = re.sub(
                    r" (<=|>=|==|<|>) ", r"\\n\1 ", c_text, count=1
                )
            lines.append(c_text)
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
        if fails_by[r]:
            # revision 9: the model states that this configuration fails the requirement
            lines.append(
                "not satisfied by " + ", ".join(sorted(fails_by[r]))
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
    if revision >= 7:
        # revision 7: the box says what the analysis returns and where the rest comes from, in
        # lines short enough that the box does not set the width of the view (G3-P2-6, P3-3)
        said = ",\\n".join(cfg_only)
        from_meas = " and\\n".join(
            [f"{n}\\n(passed on)" for n in passed]
            + [f"{n}\\n(not returned)" for n in read_only]
        )
        box = (
            f"**SlewExperiment**\\n<<analysis def>>\\nreturns {len(returned)} of {len(metrics)}"
            f"\\nmetrics. No slew\\nfor {said}.\\nFrom the\\nmeasurement:\\n{from_meas}."
        )
        if revision >= 8:
            # revision 8 (G3r7-P3-2): "No slew for" read as "not returned"; say they are returned,
            # computed from the configuration without a slew
            box = (
                f"**SlewExperiment**\\n<<analysis def>>\\nreturns {len(returned)} of {len(metrics)}"
                f"\\nmetrics, computed\\nwith no slew:\\n{said}.\\nFrom the\\nmeasurement:\\n{from_meas}."
            )
        out.append(
            f'rectangle "{box}{pad}" as xAnalysis {ANALYSIS_COLOUR}'
        )
    elif revision >= 6:
        # the analysis returns the computed entries and the `in` it passes on; what needs no slew
        # is named in the box (the picture implied every entry needs the measured slew)
        said = ",\\n".join(cfg_only)
        passes = ", ".join(passed)
        box = (
            f"**SlewExperiment**\\n<<analysis def>>\\nreturns {len(returned)} of the {len(metrics)}"
            f"\\nmetrics. Computed with\\nno slew, from the\\nconfiguration alone:\\n{said}."
            f"\\nPassed on as\\nmeasured:\\n{passes}."
        )
        out.append(
            f'rectangle "{box}{pad}" as xAnalysis {ANALYSIS_COLOUR}'
        )
    else:
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
                # revision 7: this line is not a requirement reading a metric (the MoE is computed
                # from the metric); it is dashed, and the legend names the kind
                style = "dashed," if revision >= 7 else ""
                width = 3 if revision >= 7 else 2
                out.append(
                    f"{nid(ev)} -[#{RELATION_COLOUR[1:]},{style}thickness={width}]{side}{head} {nid(n)}{moe_tag(ident)}"
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
        if revision >= 7:
            # revision 7 (G3-P2-2, P3-2, P3-1): every colour and every line kind the drawing uses,
            # in the fewest words; the rest is the caption's
            out.append(
                f"  <back:{REQ_COLOUR}> requirement </back> <back:{COVERED_COLOUR}> traded metric </back>"
                f" <back:{MOE_COLOUR}> derived, not traded </back>"
            )
            out.append(
                f"  <back:{ANALYSIS_COLOUR}> analysis </back> <back:{MEASURE_COLOUR}> measurement </back>"
            )
            out.append(
                f"  <color:{RELATION_COLOUR}>━━</color> requirement reads metric"
                f"   <color:{RELATION_COLOUR}>┅┅┅</color> computed from"
                f"   <color:{SOURCE_COLOUR}>──▶</color> value comes from"
            )
        else:
            out.append(
                "  orange: requirement; green: traded metric; yellow: derived, not traded"
            )
        out.append("end legend")
        out.append("@enduml")
        cap = []
        moes = [n for n, _ in metrics if mark.get(n) == "MoE"] + [
            plain_name(short(c)) for c in moe_calcs
        ]
        if revision >= 6:
            ver_of = lambda names: sorted(  # noqa: E731
                {
                    c
                    for n in names
                    for r, nn, st, ev in rel
                    if nn == n
                    for c in verified_by[r]
                }
            )
            cap = [
                f"The analysis `SlewExperiment` returns {len(returned)} of the {len(metrics)} traded "
                f"metrics. The {', '.join(read_only)} is read from `SlewMeasurement` and is not "
                f"returned. The {', '.join(passed)} is an input of the analysis that it returns "
                "unchanged, so its arrow starts at `SlewMeasurement`, where the value is measured.",
                f"The {' and the '.join(cfg_only)} are computed from the configuration alone, with "
                "no slew; their requirements are verified in "
                f"`{', '.join(ver_of(cfg_only))}`, the others in "
                f"`{', '.join(sorted({c for r in reqs for c in verified_by[r]} - set(ver_of(cfg_only))))}`.",
                "The groups are the analyst's grouping of the metrics (the model has no such "
                "structure); a requirement stands in the group of the metric it reads. The "
                f"{len(no_line)} requirements that read no traded metric stand apart here, each "
                "for the reason below; the coupling table of `coverage.md` lists each under the "
                "group of the calc it reads.",
                *[
                    (reasons or {}).get(short(r))
                    or f"`{short(r)}`: no reason stated."
                    for r in no_line
                ],
                "Not drawn: the coupling variables between the groups and the measured inputs the "
                "analysis takes. They are the cells of the coupling table of `coverage.md`.",
            ]
            if revision >= 9 and any(fails_by.values()):
                failing = sorted(
                    {x for v in fails_by.values() for x in v}
                )
                cap.append(
                    f"`{', '.join(failing)}` satisfies every requirement but "
                    + " and ".join(
                        f"`{short(r)}`" for r in reqs if fails_by[r]
                    )
                    + ", which the model states it fails (`not satisfy`)."
                )
            if revision >= 7:
                cap.append(
                    "A metric marked MoE is a measure of effectiveness, one a stakeholder states "
                    f"without knowing the design (here the {' and the '.join(moes)}); a metric marked "
                    "MoP is a measure of performance under the engineer's scenario (here the others). "
                    "The dashed line joins a derived quantity to the metric it is computed from.",
                )
        return "\n".join(out) + "\n", {
            "caption": cap,
            "rel": rel,
            "rel_all": rel_all,
            "metric_element": METRIC_ELEMENT,
            "related": related,
            "reqs": reqs,
            "band": band,
            "metrics": metrics,
            "origin": origin,
            "satisfied": satisfied_by,
            "fails": fails_by,
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
        default=9,
        choices=(3, 4, 5, 6, 7, 8, 9),
        help="drawing revision (3: the views committed before WP23's data gate; 4: WP23 round 3; "
        "5: WP23 round 4, the committed views of the data gate; 6: the post-gate view-consistency "
        "unit; 7: the G-3 blocks of the behavioural view; 8: the analysis box's one line; 9: the negated satisfy (the WP23 close-out), the committed views since)",
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
    text, facts = behavioural(
        m,
        byid,
        a.package,
        a.revision,
        reasons=box_reasons(a.model) if a.revision >= 9 else None,
    )
    (od / "behavioural_view.puml").write_text(text)
    if a.revision >= 6:
        (od / "behavioural_caption.md").write_text(
            "Sources, verification and groups (read from the model by the views generator):\n\n"
            + "".join(f"- {line}\n" for line in facts["caption"])
        )
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
