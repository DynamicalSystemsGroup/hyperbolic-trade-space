"""Appendix C: the case's model, how the table of metrics came to be.

Everything here describes the pipeline up to the method's input and nothing the method computes:
no exponent, temperature, value of V, facet, reach or share appears in any table (R-26). The tables
are produced from the case module's spec and data by calls into ``case``; none is typed. Datasets
are named once, by the labels of :data:`DATASET_LABELS`, which the tables of Appendix D cite.
"""

from __future__ import annotations

import hashlib
import json

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
    "planted": "planted-3-facet",
}
# The planted example: a synthetic table with known facets (how it is generated, not fitted).
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


def _sha256(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ledger(path=LEDGER):
    """The experiment ledger's entries by output path (empty if the ledger is absent)."""
    if not path.exists():
        return {}
    entries = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return {e["output_path"]: e for e in entries if e.get("output_path")}


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
        rel = f"examples/adcs/data/{f}"
        raw = pd.read_csv(path)
        entry = ledger.get(rel, {})
        rows.append([
            _label(r), r, rel, entry.get("id", "none"),
            entry.get("inputs", {}).get("command", "none"), len(raw),
            int(case.feasible_mask(raw, spec).sum()), _sha256(path),
            entry.get("output_sha256", "none"),
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
    """How the planted table is generated: the generator's arguments and the planted facets.

    Returns
    -------
    Md
        The settings of :data:`PLANTED` and the planted exponents, one row per facet.
    """
    p = PLANTED
    settings = md_table(
        ["Argument of make_frontier_data", "Value"],
        [[k, v] for k, v in p.items() if k != "exponents"],
    )
    facets = md_table(
        ["Planted facet", *[f"metric {j + 1}" for j in range(p["n_features"])]],
        [[f"facet {k + 1}", *w] for k, w in enumerate(p["exponents"])],
    )
    return Md(f"Dataset {_label('planted')}:\n\n" + settings + "\n\n" + facets)
