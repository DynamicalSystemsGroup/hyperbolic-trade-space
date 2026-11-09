"""Project the loaded SysML v2 model to PlantUML text for two paper figures.

Reads the model through the opensysml Python API (query, eval, to_api_json); nothing about the
model is typed here except presentation choices (parameters below).

    uv run python project.py MODEL.sysml OUTDIR [--package NAME]

writes OUTDIR/slot1_configuration.puml and OUTDIR/slot2_attributes.puml.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import warnings

import opensysml

warnings.simplefilter("ignore")

# ---- presentation parameters (no model content) ---------------------------------------------
DIRECTION = "left to right direction"
SKIN = """skinparam shadowing false
skinparam defaultFontName SansSerif
skinparam defaultFontSize 13
skinparam ClassBackgroundColor white
skinparam ClassBorderColor #404040
skinparam ArrowColor #404040
skinparam RectangleBackgroundColor white
skinparam nodesep 12
skinparam ranksep 30
hide circle
hide empty members
"""
PRUNE_UNREACHABLE = True            # drop calcs no root reaches (the closed-form slew estimate, unused here)
SLOT2_OMIT_CONSTRAINT_DEFS = True   # the solver claims restate the accounting; selection, not a hand edit


def load(path: pathlib.Path, pkg: str):
    conn = opensysml.connect()
    m = conn.load_from_content(path.read_text(), strict=False)
    assert m.ok, m.diagnostics
    els = json.loads(m.to_api_json().content)
    byid = {e["@id"]: e for e in els}
    return m, byid


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


def top_scope(byid, e, pkg_id):
    """The element directly under the package that contains e."""
    seen = 0
    while e is not None and seen < 50:
        o = e.get("owner")
        if o is None:
            return None
        if ref(o) == pkg_id:
            return e
        e = byid.get(ref(o))
        seen += 1
    return None


def slot1(m, byid, P):
    rows = {r.id: r.properties | {"@type": r.type} for r in m.query(scope=P)}
    kids = lambda owner: [p for p in rows.values() if p.get("owner") == owner]  # noqa: E731
    out = ["@startuml", DIRECTION, SKIN]
    cub = f"{P}::Cubesat"
    # design variables: attributes of a part def whose value is stated with `default`
    default_attrs = set()
    for e in byid.values():
        if e["@type"] == "FeatureValue" and e.get("isDefault"):
            default_attrs.add(ref(e["featureWithValue"]))
    var_attrs = [p for p in kids(cub) if p["@type"] == "AttributeUsage" and jid(p["@id"]) in default_attrs]
    out.append('class "Cubesat\\n<<part def>>" as Cubesat #E8EEF7 {')
    out.append("  .. design variables ..")
    for p in var_attrs:
        out.append(f"  {p['name']} : {short(p['type'])}")
    out.append("}")
    # parts of Cubesat
    parts = [p for p in kids(cub) if p["@type"] == "PartUsage"]
    abstract = {p["@id"] for p in rows.values() if p["@type"] == "PartDefinition" and p.get("isAbstract") == "true"}
    alts = {}
    for p in rows.values():
        if p["@type"] == "PartDefinition" and p.get("general") in abstract:
            alts.setdefault(p["general"], []).append(p["name"])
    enum_lits = {}
    for p in rows.values():
        if p["@type"] == "EnumerationUsage":
            enum_lits.setdefault(p["owner"], []).append(p["name"])
    declared = set()
    def define(defqn):
        if defqn in declared:
            return
        declared.add(defqn)
        n = short(defqn)
        r = rows.get(defqn, {})
        kind = "abstract part def" if defqn in abstract else "part def"
        out.append(f'class "{n}\\n<<{kind}>>" as {n} {{')
        for a in kids(defqn):
            if a["@type"] == "AttributeUsage" and jid(a["@id"]) in default_attrs:
                out.append(f"  {a['name']} : {short(a['type'])}   (variable)")
        out.append("}")
    selector_enum = {}
    for d in abstract:
        for a in kids(d):
            if a["@type"] == "AttributeUsage" and a.get("type") in enum_lits:
                selector_enum[d] = a["type"]
    for p in parts:
        t = p["type"]
        define(t)
        out.append(f'Cubesat *-- "{p["name"]}" {short(t)}')
        if t in alts:
            for a in sorted(alts[t]):
                define(f"{P}::{a}")
                out.append(f"{short(t)} <|-- {a}")
            if t in selector_enum:
                en = selector_enum[t]
                lits = " | ".join(enum_lits[en])
                out.append(f'note bottom of {short(t)} : choice (design variable) {short(en)}: {lits}')
    # numeric ranges from designRanges and GainBox instances, read by eval
    notes = []
    for a in kids(f"{P}::DesignRanges"):
        pass
    pr = lambda n: fmt(m.eval(f"{P}::designRanges.{n}"))  # noqa: E731
    gb = lambda inst, n: fmt(m.eval(f"{P}::{inst}.{n}"))  # noqa: E731
    out.append('note right of Cubesat')
    out.append("  **ranges (read from the model)**")
    out.append(f"  panelSpan: {pr('panelSpanMin')} .. {pr('panelSpanMax')}")
    out.append(f"  batteryCapacity: {pr('batteryCapacityMin')} .. {pr('batteryCapacityMax')}")
    for inst in ("baselineGains", "aggressiveGains"):
        out.append(f"  {inst}: Kp {gb(inst,'KpMin')} .. {gb(inst,'KpMax')}, Kd {gb(inst,'KdMin')} .. {gb(inst,'KdMax')}")
    out.append("end note")
    out.append("@enduml")
    return "\n".join(out) + "\n"


def slot2(m, byid, P):
    rows = {r.id: r.properties | {"@type": r.type} for r in m.query(scope=P)}
    pkg_id = P
    types = {"CalculationDefinition": "calc def", "RequirementDefinition": "requirement def",
             "AnalysisCaseDefinition": "analysis def", "ConstraintDefinition": "constraint def",
             "VerificationCaseDefinition": "verification def"}
    nodes = {}
    for e in byid.values():
        if e["@type"] in types and ref(e["owner"]) == pkg_id and e["@type"] != "ConstraintDefinition":
            nodes[e["@id"]] = e
        if e["@type"] == "ConstraintDefinition" and ref(e["owner"]) == pkg_id and not SLOT2_OMIT_CONSTRAINT_DEFS:
            nodes[e["@id"]] = e
    # analysis case definitions may appear as another type; find by query rows
    for r in rows.values():
        if r["@type"] in types and r.get("owner") == pkg_id and r["@id"].replace("::", "__") not in nodes:
            e = byid.get(r["@id"].replace("::", "__"))
            if e is not None and r["@type"] != "ConstraintDefinition":
                nodes[e["@id"]] = e
    cub_id = f"{P}::Cubesat".replace("::", "__")
    edges = set()
    for e in byid.values():
        fn = e.get("function") if e["@type"] == "InvocationExpression" else None
        if not fn:
            continue
        tgt = ref(fn)
        sc = top_scope(byid, e, pkg_id)
        if sc is None or tgt not in nodes:
            continue
        src = sc["@id"]
        if src in nodes or src == cub_id:
            if src != tgt:
                edges.add((src, tgt))
    # selection: keep what is reachable from the roots (Cubesat, analysis and requirement defs)
    if PRUNE_UNREACHABLE:
        roots = {cub_id} | {i for i, e in nodes.items() if e["@type"] in ("AnalysisCaseDefinition", "RequirementDefinition")}
        keep, frontier = set(roots), list(roots)
        while frontier:
            x = frontier.pop()
            for s_, t_ in edges:
                if s_ == x and t_ not in keep:
                    keep.add(t_); frontier.append(t_)
        nodes = {i: e for i, e in nodes.items() if i in keep}
        edges = {(s_, t_) for s_, t_ in edges if s_ in keep and t_ in keep}
    sat = []
    for e in byid.values():
        if e["@type"] == "SatisfyRequirementUsage":
            req = byid[ref(e["subsets"])]
            rt = [byid[ref(x)] for x in byid.values() if False]
            # requirement usage typed by a requirement def: find its typing
            typ = None
            for t in byid.values():
                if t["@type"] == "FeatureTyping" and ref(t.get("typedFeature", {"@id": ""})) == req["@id"]:
                    typ = ref(t["type"])
            sat.append((typ, ref(e["subject"])))
    def nm(i):
        return short(byid[i]["qualifiedName"]) if i in byid else short(i)
    out = ["@startuml", DIRECTION, SKIN]
    out.append('class "Cubesat (configuration c)\\n<<part def>>" as Cubesat #E8EEF7')
    for i, e in nodes.items():
        st = types[e["@type"]]
        color = {"calc def": "", "requirement def": " #FDEBD0", "analysis def": " #D5F0DC",
                 "verification def": " #EEEEEE"}[st]
        out.append(f'class "{nm(i)}\\n<<{st}>>" as {nm(i)}{color}')
    for s, t in sorted(edges):
        a = "Cubesat" if s == cub_id else nm(s)
        out.append(f"{a} --> {nm(t)}")
    for typ, subj in sat:
        if typ in nodes:
            out.append(f'{nm(typ)} ..> {nm(subj)} : <<satisfy>>')
    out.append("@enduml")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("model"); ap.add_argument("outdir"); ap.add_argument("--package", default="CubesatTradeSpaceV2")
    a = ap.parse_args()
    m, byid = load(pathlib.Path(a.model), a.package)
    od = pathlib.Path(a.outdir); od.mkdir(parents=True, exist_ok=True)
    (od / "slot1_configuration.puml").write_text(slot1(m, byid, a.package))
    (od / "slot2_attributes.puml").write_text(slot2(m, byid, a.package))
    print("ok")
