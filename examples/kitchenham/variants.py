"""WP76 Kitchenham-CSC: the sensitivity study, one change at a time from the primary rule.

``uv run python examples/kitchenham/variants.py`` reads the committed derived table
(``derived/projects.csv``, 141 projects) and writes ``variants.json``:

- ``conditioning``: the ladder of WP70 (the primary rule; the robust scaler; no scaler; shifts 20
  and 40; a cap on the overrun ratios at 3 with shift 3; plan over actual with no shift), each a
  one-change variant with its rule stated;
- ``subsets``: the primary rule on development projects only, on perfective-maintenance projects
  only (the table's type P) and on the largest client only;
- ``bands``: the primary fit's near-frontier association at ``1 / tau`` and at the smallest band
  holding 10, 15, 20 and 25 projects;
- ``influence``: every project left out in turn (the fit temperature held at the primary's so the
  change is the row's), with the rows whose removal changes a sign of the near-frontier association
  or moves an exponent by ``MOVE`` or more; and the named extremes (the largest project, the worst
  schedule overrun, the worst budget overrun) removed one at a time with the temperature reselected;
- ``headline``: the sign pattern the page states (scope against both slacks, the two slacks
  together) and, for each table, which rows hold it.

The constants are ``run.py``'s, which ``tests/test_wp76_kitchenham.py`` holds equal to the case
model ``kitchenham.sysml``.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import fitkit  # noqa: E402

fitkit.read_threads()

import numpy as np  # noqa: E402
import run  # noqa: E402

ROWS_OF_RECORD = 141
MOVE = 0.05  # an exponent move of this size or more marks a row as influential
BAND_COUNTS = (10, 15, 20, 25)
PAIRS = ("schedule slack|scope", "budget slack|scope", "schedule slack|budget slack")


def pattern(assoc):
    """The headline's sign pattern: scope against both slacks, the two slacks together."""
    return bool(
        assoc["schedule slack|scope"] < 0
        and assoc["budget slack|scope"] < 0
        and assoc["schedule slack|budget slack"] > 0
    )


def conditioning_ladder(x):
    """(label, rule, M) for the primary rule and its one-change variants."""
    yield (
        "primary",
        "share of plan for both slacks with shift 10, scope unshifted, standard scaler of the "
        "logs, orientation +1 for all three; temperature at a tenth of projects above V = 1",
        run.condition(x),
    )
    yield (
        "robust_scaler",
        "robust scaler of the logs (unit interquartile range)",
        run.condition(x, scaler="robust"),
    )
    yield (
        "no_scaler",
        "scaler None: the pure logs of the shifted shares and of scope",
        run.condition(x, scaler=None),
    )
    yield "shift_20", "shift 20 on both slacks", run.condition(x, shift=20.0)
    yield "shift_40", "shift 40 on both slacks", run.condition(x, shift=40.0)
    yield (
        "cap_3_shift_3",
        "each overrun ratio capped at 3 before the share is taken, shift 3",
        run.condition(x, shift=3.0, cap=3.0),
    )
    yield (
        "plan_over_actual",
        "plan over actual for both slacks (the overrun's reciprocal), no shift",
        run.condition(x, ratio=True),
    )


def subsets(x):
    """(label, rule, frame) for the project-type and client contrasts of WP70."""
    yield "type_D", "development projects only (type D)", x[x["type"] == "D"]
    yield "type_P", "perfective-maintenance projects only (type P)", x[x["type"] == "P"]
    yield "client_2", "the largest client only (client 2)", x[x["client"] == 2]


def read_variant(M, rule, rows):
    """``run.read`` with the rule and row count, and whether the headline pattern holds."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = run.read(M)
    res["rule"] = rule
    res["rows"] = int(rows)
    res["holds_pattern"] = pattern(res["association"])
    return res


def band_ladder(x, primary):
    """The primary fit's association at ``1 / tau`` and at bands holding 10, 15, 20, 25 rows."""
    M = run.condition(x)
    est, tau = run.fit_k1(M, primary["tau_selected"])
    lv = est.training_log_v_
    out = []
    bands = [("1_over_tau", 1.0 / tau)] + [
        (f"{k}_rows", run.smallest_band(lv, k)) for k in BAND_COUNTS
    ]
    for label, band in bands:
        try:
            rep = run.report_dict(est, M, run.NAMES, band)[0]
            row = {
                "label": label,
                "band": float(band),
                "n_near_frontier": rep["n_near_frontier"],
                "association": rep["association"],
                "holds_pattern": pattern(rep["association"]),
            }
        except ValueError as err:
            row = {"label": label, "band": float(band), "error": str(err)[:200]}
        out.append(row)
    return out


def leave_one_out(x, primary):
    """Every project left out in turn at the primary temperature; the rows that matter."""
    M = run.condition(x)
    tau = primary["tau_selected"]
    w0 = np.array([primary["exponents_k1"][n] for n in run.NAMES])
    a0 = primary["association"]
    per_row = []
    for i in range(M.shape[0]):
        Mi = np.delete(M, i, axis=0)
        est, _ = run.fit_k1(Mi, tau)
        w = est.exponents_[0]
        band = run.band_for(est.training_log_v_, tau)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            rep = run.report_dict(est, Mi, run.NAMES, band)[0]
        a = rep["association"]
        per_row.append(
            {
                "project": int(x["project"].iloc[i]),
                "exponents": dict(zip(run.NAMES, map(float, w), strict=True)),
                "max_exponent_move": float(np.abs(w - w0).max()),
                "association": a,
                "sign_flips": [p for p in PAIRS if np.sign(a[p]) != np.sign(a0[p])],
                "holds_pattern": pattern(a),
                "near_frontier_in_primary": bool(
                    int(x["project"].iloc[i]) in {r["project"] for r in primary_near_rows(primary)}
                ),
            }
        )
    moves = np.array([r["max_exponent_move"] for r in per_row])
    return {
        "temperature_held_at": tau,
        "move_threshold": MOVE,
        "rows": len(per_row),
        "rows_holding_pattern": int(sum(r["holds_pattern"] for r in per_row)),
        "rows_with_a_sign_flip": [r["project"] for r in per_row if r["sign_flips"]],
        "rows_moving_an_exponent": [
            r["project"] for r in per_row if r["max_exponent_move"] >= MOVE
        ],
        "largest_exponent_move": float(moves.max()),
        "largest_exponent_move_project": int(per_row[int(moves.argmax())]["project"]),
        "association_range": {
            p: [
                float(min(r["association"][p] for r in per_row)),
                float(max(r["association"][p] for r in per_row)),
            ]
            for p in PAIRS
        },
        "per_row": per_row,
    }


def primary_near_rows(primary):
    """The near-frontier rows of the primary fit, from ``results.json``."""
    import json

    res = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    return res["frontier_projects"]["near_frontier_rows"]


def extremes(x):
    """The named extremes removed one at a time, the temperature reselected."""
    picks = {
        "without_largest_project": x["afp"].idxmax(),
        "without_worst_schedule_overrun": x["sched_overrun"].idxmax(),
        "without_worst_budget_overrun": x["budget_overrun"].idxmax(),
    }
    out = {}
    for label, idx in picks.items():
        frame = x.drop(index=idx)
        res = read_variant(
            run.condition(frame),
            f"primary rule without project {int(x.loc[idx, 'project'])}",
            len(frame),
        )
        res["project_removed"] = int(x.loc[idx, "project"])
        res["afp_removed"] = float(x.loc[idx, "afp"])
        out[label] = res
    return out


def main():
    x = run.load_derived()
    if len(x) != ROWS_OF_RECORD:
        raise RuntimeError(f"{run.DERIVED.name}: {len(x)} rows, the record has {ROWS_OF_RECORD}")
    out = {
        "derived_sha256": fitkit.file_hash(run.DERIVED, "sha256"),
        "rows": len(x),
        "headline": {
            "pattern": "schedule slack|scope < 0 and budget slack|scope < 0 and "
            "schedule slack|budget slack > 0, near the frontier",
        },
        "conditioning": {},
        "subsets": {},
    }
    for label, rule, M in conditioning_ladder(x):
        out["conditioning"][label] = read_variant(M, rule, M.shape[0])
        r = out["conditioning"][label]
        print(f"{label:22s} n={r['n']} tau={r['tau_selected']:6.1f} holds={r['holds_pattern']}")
    primary = out["conditioning"]["primary"]
    for label, rule, frame in subsets(x):
        out["subsets"][label] = read_variant(run.condition(frame), rule, len(frame))
        r = out["subsets"][label]
        print(f"{label:22s} n={r['n']} tau={r['tau_selected']:6.1f} holds={r['holds_pattern']}")
    out["bands"] = band_ladder(x, primary)
    out["influence"] = {"leave_one_out": leave_one_out(x, primary), "extremes": extremes(x)}
    h = out["headline"]
    h["conditioning_rows_holding"] = [
        k for k, v in out["conditioning"].items() if v["holds_pattern"]
    ]
    h["subset_rows_holding"] = [k for k, v in out["subsets"].items() if v["holds_pattern"]]
    h["band_rows_holding"] = [b["label"] for b in out["bands"] if b.get("holds_pattern")]
    h["extremes_holding"] = [
        k for k, v in out["influence"]["extremes"].items() if v["holds_pattern"]
    ]
    h["leave_one_out_holding"] = out["influence"]["leave_one_out"]["rows_holding_pattern"]
    fitkit.dump(out, HERE / "variants.json")
    print(
        "bands",
        [(b["label"], b.get("n_near_frontier"), b.get("holds_pattern")) for b in out["bands"]],
    )
    loo = out["influence"]["leave_one_out"]
    print(
        "loo holding",
        loo["rows_holding_pattern"],
        "flips",
        loo["rows_with_a_sign_flip"],
        "moves",
        loo["rows_moving_an_exponent"],
        "max",
        round(loo["largest_exponent_move"], 3),
    )
    print(
        "extremes",
        {k: (v["rows"], v["holds_pattern"]) for k, v in out["influence"]["extremes"].items()},
    )


if __name__ == "__main__":
    main()
