"""Appendix C: the case's model, how the table of metrics came to be.

Everything here describes the pipeline up to the method's input and nothing the method computes:
no exponent, temperature, value of V, term, reach or share appears in any table (R-26). The tables
are produced from the case module's spec and data by calls into ``case``; none is typed. Datasets
are named once, by the labels of :data:`DATASET_LABELS`, which the tables of Appendix D cite.
"""

from __future__ import annotations

import hashlib
import json
from functools import cache

import case
import numpy as np
import pandas as pd
from paper_common import Md, frame_table, md_table
from paper_paths import ROOT

LEDGER = ROOT / "examples" / "adcs" / "experiments" / "ledger" / "ledger.jsonl"

# The label of each dataset, defined once here and cited by Appendix D.
DATASET_LABELS = {
    "primary": "cubesat-primary",
    "stock": "cubesat-stock",
    "planted": "planted-3-term",
}
# The planted example: a synthetic table with known terms (how it is generated, not fitted).
PLANTED = {
    "n_samples": 900,
    "n_features": 4,
    "n_terms": 3,
    "exponents": [[0.5, 0.5, 0, 0], [0, 0.5, 0.5, 0], [0, 0, 0.5, 0.5]],
    "noise": 0.0,
    "random_state": 0,
}


def planted_table():
    """The planted table of rows and its generator's record.

    Returns
    -------
    tuple
        ``(X, info)`` as returned by ``make_frontier_data`` with the settings of :data:`PLANTED`.
    """
    from hyperbolic_trade_space import make_frontier_data

    return make_frontier_data(**PLANTED)


def _spec(spec=None):
    return case.CUBESAT if spec is None else spec


def _label(regime):
    return DATASET_LABELS.get(regime, regime)


# Which part of the model produces each attribute: the file of examples/adcs and the name in it.
# A test checks that each name occurs in its file; nothing here is a number.
PRODUCERS = {
    "settling_time_s": ("adcs_sim.py", "simulate_adcs", "measured: on the integrated slew"),
    "pointing_error_deg": ("cubesat_model.py", "pointing_error_deg", "computed: pointing budget"),
    "total_mass_kg": ("cubesat_tradespace.sysml", "MassAccounting", "computed: accounting"),
    "control_effort": ("adcs_sim.py", "simulate_adcs", "measured: on the integrated slew"),
    "power_margin_w": ("cubesat_tradespace.sysml", "PowerMargin", "computed: accounting"),
    "energy_balance_wh": ("cubesat_tradespace.sysml", "EnergyBalance", "computed: accounting"),
    "peak_slew_power_w": ("cubesat_tradespace.sysml", "PeakSlewPower", "computed: accounting"),
    "dod_eclipse": ("cubesat_tradespace.sysml", "DepthOfDischarge", "computed: accounting"),
}


def configuration_space(spec=None) -> Md:
    """The design variables with their declared ranges, levels and sampled extent per regime.

    Returns
    -------
    Md
        One table of numeric variables and one of categorical variables.
    """
    spec = _spec(spec)
    raw = {r: pd.read_csv(spec.data_dir / f) for r, f in spec.regimes.items()}
    num = []
    for v in spec.design_vars:
        lo, hi = spec.ranges.get(v, (float("nan"), float("nan")))
        row = [v, lo, hi]
        for r in raw:
            row += [raw[r][v].min(), raw[r][v].max()]
        num.append(row)
    heads = ["Design variable", "Declared min", "Declared max"]
    for r in raw:
        heads += [f"{_label(r)} min", f"{_label(r)} max"]
    cat = []
    for v, levels in spec.covariates.items():
        cat.append([v, ", ".join(levels)] + [
            ", ".join(f"{lv}: {int((raw[r][v] == lv).sum())}" for lv in levels) for r in raw
        ])  # fmt: skip
    cheads = ["Covariate", "Ordered levels"] + [f"{_label(r)} designs per level" for r in raw]
    return Md(md_table(heads, num) + "\n\n" + md_table(cheads, cat))


def evaluation(spec=None) -> Md:
    """The attributes with columns, units and orientation, and the scenario constants.

    Returns
    -------
    Md
    """
    spec = _spec(spec)
    attrs = md_table(
        ["Attribute", "Column", "Unit", "Larger is better"],
        [[spec.short[a], a, spec.units[a], "yes" if spec.orientation[a] > 0 else "no"]
         for a in spec.attributes],
    )  # fmt: skip
    raw = pd.read_csv(spec.data_dir / next(iter(spec.regimes.values())))
    const = [[c, raw[c].iloc[0]] for c in raw.columns if raw[c].nunique() == 1
             and c not in spec.flags]  # fmt: skip
    return Md(attrs + "\n\n" + md_table(["Scenario constant (column)", "Value"], const))


def attribute_sources(spec=None) -> Md:
    """Which part of the model produces each attribute, in the order of the evaluation table.

    Returns
    -------
    Md
        One row per attribute: how it is obtained (measured on the slew or computed by the
        accounting), the file of ``examples/adcs`` and the name in it that produces it.
    """
    spec = _spec(spec)
    rows = [[spec.short[a], f"`{PRODUCERS[a][0]}`", f"`{PRODUCERS[a][1]}`", PRODUCERS[a][2]]
            for a in spec.attributes]  # fmt: skip
    return Md(md_table(["Attribute", "File", "Name in the file", "How it is obtained"], rows))


def feasibility(spec=None) -> Md:
    """The feasibility conditions applied in order, per regime, from the case module.

    Returns
    -------
    Md
    """
    spec = _spec(spec)
    parts = []
    for r in spec.regimes:
        tab = case.feasibility_table(case.load_study(r, spec))
        parts.append(f"Dataset {_label(r)}:\n\n" + frame_table(tab))
    return Md("\n\n".join(parts))


def conditioning(spec=None) -> Md:
    """Each attribute's orientation, raw range and conditioned range, per regime.

    Returns
    -------
    Md
    """
    spec = _spec(spec)
    parts = []
    for r in spec.regimes:
        tab = case.conditioning_table(case.load_study(r, spec))
        parts.append(f"Dataset {_label(r)}:\n\n" + frame_table(tab.rename_axis("attribute"), True))
    return Md("\n\n".join(parts))


def metric_table(spec=None, n=5) -> Md:
    """The table of metrics, the method's input: its definition and its first rows per dataset.

    Parameters
    ----------
    spec : case.CaseSpec, optional
    n : int, default 5
        Rows shown per dataset.

    Returns
    -------
    Md
        The rule that turns an attribute into a metric, then per dataset the number of designs and
        the first ``n`` rows of the metric table (one column per metric, strictly positive,
        larger is better). Nothing is fitted to it here.
    """
    spec = _spec(spec)
    parts = [
        "Each metric is `m_j = exp((o_j log(a_j + s_j) - c_j) / k_j)` for attribute `a_j`, with "
        "orientation `o_j` (+1 larger is better, -1 smaller is better), shift `s_j = 0`, and "
        "the offset `c_j` and log scale `k_j` of the conditioning above. The table of metrics, "
        "one row per kept design and one column per metric, is where the model ends and the method "
        "begins."
    ]
    for r in spec.regimes:
        st = case.load_study(r, spec)
        head = pd.DataFrame(st.M[:n], columns=st.names).rename_axis("design").reset_index()
        parts.append(
            f"Dataset {_label(r)}: {st.M.shape[0]} designs by {st.M.shape[1]} metrics; "
            f"the first {n} rows:\n\n" + frame_table(head)
        )
    return Md("\n\n".join(parts))


def _sha256(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ledger(path=LEDGER):
    """The experiment ledger's entries by output hash, the latest of equal hashes (empty if absent).

    A file is found by its hash, so a byte copy of a ledger output names the entry too.
    """
    if not path.exists():
        return {}
    entries = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return {e["output_sha256"]: e for e in entries if e.get("output_sha256")}


def _command(entry, rel) -> str:
    """The command of a ledger entry, or the ledger's own run of it when the entry records none."""
    if not entry:
        return "none"
    command = entry.get("inputs", {}).get("command")
    if command:
        return command
    base = entry["id"].split("@")[0]
    run = f"PYTHONPATH=examples/adcs uv run python -m experiments run {base} --supersede"
    return run if entry["output_path"] == rel else f"{run}, then a byte copy to {rel}"


def datasets(spec=None) -> Md:
    """The datasets: label, regime, file, provenance (ledger entry, command, hash), sizes.

    Returns
    -------
    Md
        One row per dataset, the planted one included; ``SHA-256`` is computed from the file, and
        ``Ledger hash`` is the hash the experiment ledger recorded for it.
    """
    spec = _spec(spec)
    ledger = _ledger()
    rows = []
    for r, f in spec.regimes.items():
        path = spec.data_dir / f
        rel = path.resolve().relative_to(ROOT).as_posix()
        raw = pd.read_csv(path)
        digest = _sha256(path)
        entry = ledger.get(digest, {})
        rows.append([
            _label(r), r, rel, entry.get("id", "none"), _command(entry, rel), len(raw),
            int(case.feasible_mask(raw, spec).sum()), digest, entry.get("output_sha256", "none"),
        ])  # fmt: skip
    X, _ = planted_table()
    call = "make_frontier_data(" + ", ".join(f"{k}={v}" for k, v in PLANTED.items()) + ")"
    digest = hashlib.sha256(np.ascontiguousarray(X).tobytes()).hexdigest()
    rows.append(
        [_label("planted"), "synthetic", "none", "none", call, len(X), len(X), digest, "none"]
    )
    heads = ["Label", "Regime", "File", "Ledger entry", "Command", "Designs sampled",
             "Designs kept", "SHA-256", "Ledger hash"]  # fmt: skip
    return Md(md_table(heads, rows))


def planted_example() -> Md:
    """How the planted table is generated: the generator's arguments and the planted terms.

    Returns
    -------
    Md
        The settings of :data:`PLANTED` and the planted exponents, one row per term.
    """
    p = PLANTED
    settings = md_table(
        ["Argument of make_frontier_data", "Value"],
        [[k, v] for k, v in p.items() if k != "exponents"],
    )
    terms = md_table(
        ["Planted term", *[f"metric {j + 1}" for j in range(p["n_features"])]],
        [[f"term {k + 1}", *w] for k, w in enumerate(p["exponents"])],
    )
    return Md(f"Dataset {_label('planted')}:\n\n" + settings + "\n\n" + terms)


@cache
def _associations(regime):
    return case.association_all_pairs(case.load_study(regime))


def _one_axis_sentence() -> str:
    """The association step's outcome in one sentence, from the data (C.5, D.3, D.4)."""
    named = {r: case.one_axis_pairs(_associations(r)) for r in case.CUBESAT.regimes}
    strongest = {r: _associations(r).iloc[0] for r in case.CUBESAT.regimes}
    tops = "; ".join(
        f"Dataset {DATASET_LABELS[r]}: {s['metric a']} and {s['metric b']}, {s['spearman']:+.3f}"
        for r, s in strongest.items()
    )
    if not any(named.values()):
        return (
            f"No pair of traded metrics reaches |Spearman| {case.ONE_AXIS:g} over the feasible "
            f"designs, so no pair is read as one axis and every exponent is read on its own; the "
            f"strongest pair, {tops}. A pair at or above {case.ONE_AXIS:g} would be named one axis "
            "and its two exponents read summed per term."
        )
    pairs = "; ".join(
        f"Dataset {DATASET_LABELS[r]}: " + ", ".join(f"{a} and {b}" for a, b in p)
        for r, p in named.items()
        if p
    )
    return (
        f"Pairs at |Spearman| {case.ONE_AXIS:g} or above, read as one axis with their two "
        f"exponents summed per term: {pairs}."
    )


def metric_associations() -> Md:
    """Every pair of traded metrics over the feasible designs, both datasets side by side.

    Returns
    -------
    Md
        The association step of the case analysis (``case.association_all_pairs``): Spearman and
        Pearson of the conditioned log metrics, pairs at ``|Spearman| >= case.ONE_AXIS`` named
        one axis; then the outcome in one sentence.
    """
    regimes = list(case.CUBESAT.regimes)
    tables = {r: _associations(r).set_index(["metric a", "metric b"]) for r in regimes}
    first = tables[regimes[0]]
    rows = []
    for a, b in first.index:
        row = [a, b]
        for r in regimes:
            x = tables[r].loc[(a, b)]
            row += [f"{x['spearman']:+.3f}", f"{x['pearson']:+.3f}"]
        named = [DATASET_LABELS[r] for r in regimes if tables[r].loc[(a, b), "one axis"]]
        row.append(", ".join(named) or "no")
        rows.append(row)
    headers = ["metric a", "metric b"]
    for r in regimes:
        headers += [f"Spearman, {DATASET_LABELS[r]}", f"Pearson, {DATASET_LABELS[r]}"]
    headers.append("one axis")
    return Md(md_table(headers, rows) + "\n\n" + _one_axis_sentence())
