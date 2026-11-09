"""Project the loaded SysML v2 model to PlantUML text for two paper figures.

Reads the model through the opensysml Python API (query, eval, to_api_json); the metric to model
identifier table and the layout choices below are the only things typed here (parameters).

    uv run python project.py MODEL.sysml OUTDIR [--package NAME]

writes OUTDIR/assembly_view.puml (what a configuration is and how the parts assemble) and
OUTDIR/behavioural_view.puml (subsystems, requirements, the ten traded metrics, how the metrics are
obtained). Revision 2 (2026-11-09): the first slot-2 candidate is withdrawn.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import warnings

import opensysml

warnings.simplefilter("ignore")

REPO = pathlib.Path(__file__).resolve().parents[4]

# ---- layout parameters (PlantUML / Graphviz controls; no model content) ------------------------
COLUMN_WIDTH = 700                      # px, the paper's column; PlantUML `scale N width`
ASSEMBLY_DIRECTION = "top to bottom direction"
BEHAVIOUR_DIRECTION = "left to right direction"
ASSEMBLY_LINETYPE = "polyline"             # skinparam linetype: ortho | polyline (default splines)
BEHAVIOUR_LINETYPE = "polyline"
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
TAG_CATEGORICAL = ("swap", "#F6C98B")   # a part is replaced by one of its alternatives
TAG_CONTINUOUS = ("tune", "#9CC8EE")    # a parameter of a part takes a value in a range

# ---- behavioural view: the model's identifier for each traded metric (names from CaseSpec) ------
# kind: calc = a calc def the analysis returns; attr = a Cubesat attribute the analysis returns;
#       input = an analysis `in` parameter returned unchanged; measured = a SlewMeasurement quantity
#       (or, with None, a quantity the model names only in prose) passed through unchanged.
METRIC_ELEMENT = {
    "settling time": ("measured", "settlingTime"),
    "slew time": ("measured", None),
    "pointing error": ("calc", "PointingError"),
    "total mass": ("attr", "totalMass"),
    "control effort": ("input", "controlEffort"),
    "power margin": ("calc", "PowerMargin"),
    "energy balance": ("calc", "EnergyBalance"),
    "eclipse reserve": ("calc", "EclipseReserve"),
    "peak slew power": ("calc", "PeakSlewPower"),
    "depth of discharge": ("calc", "DepthOfDischarge"),
}
# the analyst's reading, used only where the model leaves a requirement with no related metric:
# the subsystem the requirement lands on (CaseSpec groups metrics, not requirements)
ANALYST_SUBSYSTEM = {"MomentumRequirement": "controls"}
# name used in the model's prose for a measured quantity, to find documentary relations
PROSE_NAME = {"slew time": "slew time", "settling time": "settling time"}
REQ_COLOUR = "#FDEBD0"
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
        if e["@type"] == "Documentation" and i.startswith(prefix_id + "__") and "__" not in i[len(prefix_id) + 2:]:
            out.append(" ".join(e.get("sysx:sourceText", "").replace("/*", " ").replace("*/", " ").split()))
    return " ".join(out)


# =================================================================================================
# View 1: the assembly
# =================================================================================================
def assembly(m, byid, P):
    rows = {r.id: r.properties | {"@type": r.type} for r in m.query(scope=P)}
    kids = lambda owner: [p for p in rows.values() if p.get("owner") == owner]  # noqa: E731
    cub = f"{P}::Cubesat"
    default_attrs = {ref(e["featureWithValue"]) for e in byid.values()
                     if e["@type"] == "FeatureValue" and e.get("isDefault")}
    parts = [p for p in kids(cub) if p["@type"] == "PartUsage"]
    abstract = {p["@id"] for p in rows.values() if p["@type"] == "PartDefinition" and p.get("isAbstract") == "true"}
    alts: dict = {}
    for p in rows.values():
        if p["@type"] == "PartDefinition" and p.get("general") in abstract:
            alts.setdefault(p["general"], []).append(p["name"])
    enum_lits: dict = {}
    for p in rows.values():
        if p["@type"] == "EnumerationUsage":
            enum_lits.setdefault(p["owner"], []).append(p["name"])
    selector = {}
    for d in abstract:
        for a in kids(d):
            if a["@type"] == "AttributeUsage" and a.get("type") in enum_lits:
                selector[d] = a["type"]

    # continuous variables: defaulted attributes of the root, each placed ONCE in the part definition
    # whose usage binds it (a redefinition `:>> span = Cubesat::panelSpan`); defaulted attributes of
    # other part definitions that are bound from the root are the same variable, not new ones.
    var_at: dict = {}                   # part def qualified name -> [variable names]
    bound_names: dict = {}              # part def -> redefined feature names (span, capacity)
    root_vars = [p for p in kids(cub) if p["@type"] == "AttributeUsage" and jid(p["@id"]) in default_attrs]
    for v in root_vars:
        vid = jid(v["@id"])
        for e in byid.values():
            if e["@type"] in ("FeatureReferenceExpression", "FeatureChainExpression") \
                    and e.get("referent") and ref(e["referent"]) == vid:
                parts_of = e["@id"].split("__")
                if len(parts_of) > 3 and parts_of[1] == "Cubesat":
                    usage = next((p for p in parts if p["name"] == parts_of[2]), None)
                    if usage and v["name"] not in var_at.setdefault(usage["type"], []):
                        var_at[usage["type"]].append(v["name"])
                        bound_names.setdefault(usage["type"], set()).add(parts_of[3].split("_pvalue")[0])
    for d in {p["type"] for p in parts}:
        for a in kids(d):
            if a["@type"] == "AttributeUsage" and jid(a["@id"]) in default_attrs \
                    and a["name"] not in bound_names.get(d, set()):
                var_at.setdefault(d, []).append(a["name"])

    def tag(kind, name):
        word, colour = kind
        return f"  <back:{colour}><b> {word} </b></back> {name}"

    out = ["@startuml", ASSEMBLY_DIRECTION, f"skinparam linetype {ASSEMBLY_LINETYPE}",
           SKIN.format(nodesep=12, ranksep=34), f"scale {COLUMN_WIDTH} width", ""]
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
    for p in parts:
        t = p["type"]
        for a in sorted(alts.get(t, [])):
            define(f"{P}::{a}", False)
    for p in parts:
        t = p["type"]
        for a in sorted(alts.get(t, [])):
            out.append(f"{short(t)} <|-- {a}")

    pr = lambda n: fmt(m.eval(f"{P}::designRanges.{n}"))  # noqa: E731
    gb = lambda inst, n: fmt(m.eval(f"{P}::{inst}.{n}"))  # noqa: E731
    out.append("")
    out.append("legend bottom")
    out.append("  **Configuration variables** (each marked once, in the part it belongs to)")
    out.append(tag(TAG_CATEGORICAL, "categorical: a part is swapped for one of its alternatives"))
    out.append(tag(TAG_CONTINUOUS, "continuous: a parameter of a part is tuned within a range"))
    out.append("  ")
    out.append("  **Levels and ranges** (read from the model)")
    for d, en in sorted(selector.items()):
        out.append(f"  {short(en)}: {' | '.join(enum_lits[en])}")
    out.append(f"  panelSpan: {pr('panelSpanMin')} .. {pr('panelSpanMax')}")
    out.append(f"  batteryCapacity: {pr('batteryCapacityMin')} .. {pr('batteryCapacityMax')}")
    for inst in ("baselineGains", "aggressiveGains"):
        out.append(f"  {inst}: Kp {gb(inst, 'KpMin')} .. {gb(inst, 'KpMax')}, Kd {gb(inst, 'KdMin')} .. {gb(inst, 'KdMax')}")
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
        self.calcs = {i for i, e in byid.items() if e["@type"] == "CalculationDefinition"}
        self.cub_attrs = {short(i): i for i, e in byid.items()
                          if e["@type"] == "AttributeUsage" and e["@id"].startswith(self.pre + "Cubesat__")
                          and e["@id"].count("__") == self.pre.count("__") + 1}
        self._direct: dict = {}

    def inside(self, root_id):
        return [e for i, e in self.byid.items() if i.startswith((root_id + "__", root_id + "_pvalue"))]

    def direct(self, root_id) -> set:
        """Calc defs invoked inside root_id, plus those behind a Cubesat attribute it reads (c.availablePower)."""
        if root_id in self._direct:
            return self._direct[root_id]
        found = set()
        for e in self.inside(root_id):
            if e["@type"] == "InvocationExpression" and e.get("function") and ref(e["function"]) in self.calcs:
                found.add(ref(e["function"]))
            elif e["@type"] == "FeatureChainExpression":
                last = e.get("sysx:sourceText", "").split(".")[-1].strip()
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
    metrics = [(spec.short[a], spec.subsystems[a]) for a in spec.attributes]
    order = list(spec.subsystem_order)
    assert {n for n, _ in metrics} == set(METRIC_ELEMENT), "METRIC_ELEMENT must name every traded metric"
    pre = P.replace("::", "__") + "__"
    rd = Reads(byid, P)

    # --- the model's requirement, satisfy, verify and analysis elements -------------------------
    reqs = sorted(i for i, e in byid.items() if e["@type"] == "RequirementDefinition" and ref(e["owner"]) == pre[:-2])
    typing = {}
    for t in byid.values():
        if t["@type"] == "FeatureTyping":
            typing[ref(t["typedFeature"])] = ref(t["type"])
    satisfied_by = {r: set() for r in reqs}
    for e in byid.values():
        if e["@type"] == "SatisfyRequirementUsage":
            req_usage = ref(e["subsets"])
            if typing.get(req_usage) in satisfied_by:
                satisfied_by[typing[req_usage]].add(short(ref(e["subject"])))
    verified_by = {r: set() for r in reqs}
    for vid, v in byid.items():
        if v["@type"] == "VerificationCaseDefinition":
            for e in byid.values():
                if e["@type"] == "RequirementUsage" and e["@id"].startswith(vid + "__") and typing.get(e["@id"]) in verified_by:
                    verified_by[typing[e["@id"]]].add(short(vid))
    analysis = next(i for i, e in byid.items() if e["@type"] == "AnalysisCaseDefinition")
    a_inv = {ref(e["function"]) for e in rd.inside(analysis) if e["@type"] == "InvocationExpression" and e.get("function")}
    a_chain = {e.get("sysx:sourceText", "").split(".")[-1].strip() for e in rd.inside(analysis) if e["@type"] == "FeatureChainExpression"}
    a_refs = {short(ref(e["referent"])) for e in rd.inside(analysis) if e["@type"] == "FeatureReferenceExpression" and e.get("referent")}
    a_text = doc_text(byid, pre[:-2]).replace("-", " ")   # the package-level prose of section 6
    meas_attrs = {short(i) for i, e in byid.items() if e["@type"] == "AttributeUsage" and i.startswith(pre + "SlewMeasurement__")}

    # --- where each metric comes from; check the table against the model -----------------------------
    origin, mcalc = {}, {}
    for name, _ in metrics:
        kind, ident = METRIC_ELEMENT[name]
        if kind == "calc":
            assert pre + ident in a_inv, f"analysis does not return {ident}"
            origin[name], mcalc[name] = "analysis", pre + ident
        elif kind == "attr":
            assert ident in a_chain, f"analysis does not return cubesat.{ident}"
            origin[name], mcalc[name] = "analysis", None
        elif kind == "input":
            assert ident in a_refs, f"analysis has no parameter {ident}"
            origin[name], mcalc[name] = "measurement", None
        else:
            assert ident is None or ident in meas_attrs, f"SlewMeasurement has no {ident}"
            assert name in a_text, f"model prose does not say {name} is measured"
            origin[name], mcalc[name] = "measurement", None

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
    rel = []   # (req, metric, strength, evidence)
    for r in reqs:
        rdir, rcl, rmeas = rd.direct(r), rd.closure(r), rd.measured(r)
        rdoc = doc_text(byid, r).replace("-", " ")
        for name, _ in metrics:
            kind, ident = METRIC_ELEMENT[name]
            same = []
            if kind == "measured" and ident in rmeas:
                same.append(ident)
            same += [short(c) for c in sorted(rdir & m_direct(name))]
            if same:
                rel.append((r, name, "strong", ", ".join(same)))
                continue
            up = [short(c) for c in sorted(rcl & m_closure(name))]
            if up:
                rel.append((r, name, "weak", ", ".join(up)))
                continue
            if PROSE_NAME.get(name) and PROSE_NAME[name] in rdoc:
                rel.append((r, name, "prose", "prose"))

    def req_subsystem(r):
        votes = [dict(metrics)[n] for rr, n, _, _ in rel if rr == r]
        if votes:
            return max(order, key=lambda s: votes.count(s))
        return ANALYST_SUBSYSTEM.get(short(r), "unassigned")

    band = {r: req_subsystem(r) for r in reqs}
    related = {n for _, n, _, _ in rel}

    # --- PlantUML ------------------------------------------------------------------------------
    nid = lambda s: "x" + "".join(ch for ch in s.title() if ch.isalnum())  # noqa: E731
    out = ["@startuml", BEHAVIOUR_DIRECTION, f"skinparam linetype {BEHAVIOUR_LINETYPE}",
           SKIN.format(nodesep=8, ranksep=36), f"scale {COLUMN_WIDTH} width", ""]
    bands = order + (["unassigned"] if "unassigned" in band.values() else [])
    for s in bands:
        out.append(f'package "{s}" {{')
        idx = {n: k for k, (n, _) in enumerate(metrics)}
        smets = sorted((n for n, sub in metrics if sub == s),
                       key=lambda n: (n not in related, origin[n] != "measurement", idx[n]))
        first = lambda r: min((smets.index(n) for rr, n, _, _ in rel if rr == r and n in smets), default=99)  # noqa: E731
        sreqs = sorted((r for r in reqs if band[r] == s), key=first)
        anchors = []
        for r in sreqs:
            sat = ", ".join(sorted(satisfied_by[r])) or "none in the model"
            ver = ", ".join(sorted(verified_by[r])) or "none in the model"
            lands = "" if any(rr == r for rr, _, _, _ in rel) else "\\n**no traded metric reads it**"
            out.append(f'  rectangle "**{short(r)}**\\n<<requirement def>>\\n<<satisfy>> {sat}\\n<<verify>> {ver}{lands}" as {nid(short(r))} {REQ_COLOUR}')
            anchors.append(nid(short(r)))
        if not sreqs:
            out.append(f'  rectangle "no requirement def\\nlands on this subsystem" as {nid("none" + s)} #FFFFFF;line:gray;line.dashed;text:gray')
            anchors.append(nid("none" + s))
        for n in smets:
            style = "#E3F1E3" if n in related else "#FFFFFF;line:black;line.dashed"
            out.append(f'  rectangle "{n}" as {nid(n)} {style}')
        out.append("}")
        for a in anchors[:1]:
            for n in smets:
                out.append(f"{a} -[hidden]-> {nid(n)}")
    out.append("")
    out.append('rectangle "**SlewExperiment**\\n<<analysis def>>\\nreturns eight\\nattributes from the\\nconfiguration and the\\nmeasured inputs" as xAnalysis #D5F0DC')
    out.append('rectangle "**SlewMeasurement**\\nmeasured slew:\\nsimulation here;\\nfield data when\\nfielded" as xMeasure #EEEEEE')
    out.append("xMeasure -[hidden]down-> xAnalysis")
    out.append("")
    for r, n, strength, ev in rel:
        if strength == "strong":
            out.append(f"{nid(short(r))} -[#{RELATION_COLOUR[1:]},thickness=2]-> {nid(n)} : {ev}")
        else:
            out.append(f"{nid(short(r))} -[#{RELATION_COLOUR[1:]},dashed]-> {nid(n)} : {ev}")
    for name, _ in metrics:
        src = "xAnalysis" if origin[name] == "analysis" else "xMeasure"
        out.append(f"{nid(name)} <-[#{SOURCE_COLOUR[1:]}]- {src}")
    out.append("")
    out.append("legend bottom")
    out.append("  **Requirement - metric** (orange, requirement to metric; evidence on the line)")
    out.append("  thick: the requirement and the metric read the same calc or measured quantity")
    out.append("  dashed: they share only a calc further upstream, or the model's prose says so (prose)")
    out.append("  green metric: a requirement relation exists in the model; dashed white: traded, none in the model")
    out.append("  **Source** (grey): from the analysis def, or from the measurement of the slew")
    out.append("  Requirement placement in a subsystem is the analyst's reading (CaseSpec groups metrics)")
    out.append("end legend")
    out.append("@enduml")
    return "\n".join(out) + "\n", {"rel": rel, "reqs": reqs, "band": band, "metrics": metrics,
                                    "origin": origin, "satisfied": satisfied_by, "verified": verified_by}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("outdir")
    ap.add_argument("--package", default="CubesatTradeSpaceV2")
    ap.add_argument("--facts", action="store_true", help="print the derived relations")
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
            print(short(r), "band:", facts["band"][r], "satisfy:", sorted(facts["satisfied"][r]), "verify:", sorted(facts["verified"][r]))
    print("ok")
