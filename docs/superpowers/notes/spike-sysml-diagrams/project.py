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


# =================================================================================================
# View 1: the assembly
# =================================================================================================
def assembly(m, byid, P):
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
    out.append(
        "  Gains Kp and Kd: one range per dataset (baseline, aggressive)"
    )
    for g in ("Kp", "Kd"):
        spans = {
            b: f"{gb(b, g + 'Min')} .. {gb(b, g + 'Max')}"
            for b in boxes
        }
        if len(set(spans.values())) == 1:
            out.append(
                f"  {g}: {next(iter(spans.values()))} (both datasets)"
            )
        else:
            out.append(
                f"  {g}: "
                + "; ".join(
                    f"{v} ({b.removesuffix('Gains')} gains)"
                    for b, v in spans.items()
                )
            )
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


def behavioural(m, byid, P):
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
        SKIN.format(nodesep=8, ranksep=36),
        f"scale {COLUMN_WIDTH} width",
        "",
    ]
    bands = list(order)
    # layout: subsystems fed by the measurement come first, so the measurement box sits beside them and
    # the analysis box beside the rest; no source arrow then crosses another subsystem
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
    for s in bands:
        out.append(f'package "{s}" {{')
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
            out.append("  " + req_box(r))
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
    out.append(
        f'rectangle "requirements with no line to a traded metric" as xNoLine #FFFFFF;line:gray;line.dashed;text:gray {{'
    )
    for r in no_line:
        sat = ", ".join(sorted(satisfied_by[r])) or "none in the model"
        ver = ", ".join(sorted(verified_by[r])) or "none in the model"
        out.append(
            f'  rectangle "**{short(r)}**\\n<<requirement def>>\\n<<satisfy>> {sat}\\n<<verify>> {ver}" as {nid(short(r))} {REQ_COLOUR}'
        )
    for u, v in zip(no_line, no_line[1:]):
        out.append(
            f"  {nid(short(u))} -[hidden]right-> {nid(short(v))}"
        )
    out.append("}")
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
    for r, n, strength, ev in rel:
        if strength == "strong":
            out.append(
                f"{nid(short(r))} -[#{RELATION_COLOUR[1:]},thickness=2]-> {nid(n)} : {ev}"
            )
        elif strength == "moe":
            # requirement -> the MoE box (once per requirement and MoE) -> the metric it reads
            if (r, ev) not in drawn_moe:
                out.append(
                    f"{nid(short(r))} -[#{RELATION_COLOUR[1:]},thickness=2]-> {nid(ev)} : {ev}"
                )
                drawn_moe.add((r, ev))
            if (ev, n) not in drawn_moe:
                kind, ident = METRIC_ELEMENT[n]
                out.append(
                    f"{nid(ev)} -[#{RELATION_COLOUR[1:]},thickness=2]-> {nid(n)} : {ident}"
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
    a = ap.parse_args()
    m, byid = load(pathlib.Path(a.model))
    od = pathlib.Path(a.outdir)
    od.mkdir(parents=True, exist_ok=True)
    (od / "assembly_view.puml").write_text(assembly(m, byid, a.package))
    text, facts = behavioural(m, byid, a.package)
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
