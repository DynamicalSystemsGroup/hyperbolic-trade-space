"""The quantities added to the paper after the sensitivity run, measured on the same datasets.

``examples/adcs/experiments/sensitivity.py`` regenerates both cubesat datasets five times under
perturbations of one part in 10^12 and records what the paper reported at the time. The paper has
since added a few numbers (the median assignment
margin, the share of spread along the principal directions of the near-frontier chart, and the
decision section's counts, pointing errors and prices). This
module computes those on the committed data and on the five regenerations, and writes the committed
file ``stability_extra.json`` that :mod:`paper_stability` reads beside the sensitivity file, so the
paper prints each of them to the digits that held.

From the repository root, with the regenerations in a scratch directory (the output of
``experiments.sensitivity regenerate``; nothing here writes inside ``examples/adcs/data``)::

    PYTHONPATH=examples/adcs uv run python paper/stability_extra.py SCRATCH
"""

from __future__ import annotations

import dataclasses
import json
import math
import sys
from pathlib import Path

import paper_paths  # noqa: F401  (puts the repository on sys.path)
from paper_paths import PAPER

RESULT = PAPER / "stability_extra.json"
SEEDS = (1, 2, 3, 4, 5)


def quantities(data_dir=None) -> dict:
    """Every added quantity on the files of ``data_dir`` (default: the committed data).

    Names are ``group | regime | row | column``, as in the sensitivity file.
    """
    import case

    spec = case.CUBESAT
    if data_dir is not None:
        spec = dataclasses.replace(spec, data_dir=data_dir)
    q: dict = {}
    for regime in spec.regimes:
        study = case.load_study(regime, spec)
        fits = case.k_fits(study)
        for row in case.margin_scale(study, fits).itertuples():
            q[f"margin | {regime} | {row.K} | median margin"] = float(row._5)
        if regime == "primary":
            for row in case.pca_directions(study, fits[1]).itertuples():
                q[f"pca | {regime} | {row.direction} | share of spread"] = float(row._2)
                parts = [part.rsplit(" ", 1) for part in row._3.split(", ")]
                q[f"pca | {regime} | {row.direction} | leading metrics"] = ", ".join(
                    name for name, _ in parts
                )
                for rank, (_, loading) in enumerate(parts, 1):
                    q[f"pca | {regime} | {row.direction} | loading {rank}"] = float(loading)
    q.update(decision_quantities(spec))
    return q


DECISION_PICKS = ("sponsor", "cheapest unit", "operator", "between", "balanced", "fine")
"""The named designs of ``generate_findings.decision`` (the roles, not the design ids)."""


def decision_quantities(spec) -> dict:
    """The decision section's quantities (WP39): the counts and the named designs' measures.

    Counts are integers; per named design (by role, as the section names them) the pointing
    error, the unit cost, the fleet cost and the design id; the cost of the fine tracker. Names
    are ``decision | primary | what | column``.
    """
    import case
    import generate_findings as gf

    study = case.load_study("primary", spec)
    d = gf.decision(study, case.k_fits(study, (1, case.CASE_K)))
    q: dict = {f"decision | primary | count | {k}": int(v) for k, v in d.counts.items()}
    for role in DECISION_PICKS:
        row = d.picks[role]
        q[f"decision | primary | {role} | design"] = str(int(row["design_id"]))
        for col in ("pointing_error_deg", "unit_cost_usd", "fleet_cost_usd"):
            q[f"decision | primary | {role} | {col}"] = float(row[col])
    q["decision | primary | fine tracker | extra fleet cost"] = float(gf._tracker_cost(d))
    return q


def summarize(committed: dict, runs: dict[str, dict]) -> dict:
    """Per quantity: the committed value and, for numbers, the range over all the datasets."""
    out = {}
    for name, value in committed.items():
        values = [run[name] for run in runs.values()]
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            lo, hi = min([value, *values]), max([value, *values])
            out[name] = {"committed": value, "min": lo, "max": hi, "identical": lo == hi}
        else:
            out[name] = {"committed": value, "identical": all(v == value for v in values)}
    return out


def write(scratch) -> Path:
    """Compute on the committed data and on ``scratch/seed1`` to ``seed5`` and write the file."""
    scratch = Path(scratch)
    committed = quantities()
    runs = {f"seed{s}": quantities(scratch / f"seed{s}") for s in SEEDS}
    record = {
        "seeds": list(SEEDS),
        "perturbation": {"relative_half_width": 1e-12,
                         "variables": ["Kp", "Kd", "panel_span_m", "battery_wh"]},
        "quantities": summarize(committed, runs),
    }  # fmt: skip
    for e in record["quantities"].values():
        for key in ("committed", "min", "max"):
            if key in e and isinstance(e[key], float) and not math.isfinite(e[key]):
                raise ValueError("a non-finite quantity cannot be recorded")
    RESULT.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return RESULT


if __name__ == "__main__":
    print(write(sys.argv[1]))
