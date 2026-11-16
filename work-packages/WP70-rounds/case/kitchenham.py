"""WP70 case study on real projects: the iron triangle's three sides in the Kitchenham-CSC table.

``uv run python work-packages/WP70-rounds/case/kitchenham.py --fetch``  download into ``data/``
(git-ignored), check against ``manifest.toml``, derive, fit, write ``results_kitchenham.json`` and
the figures under ``figures/``.

One row is one software project (145, from one company, 1994 to 1999). The table carries a plan
and an actual for effort and for duration, and the delivered size in function points: the three
sides, with no quality measure (m = 0).

Attributes, before conditioning:

- schedule slack, share of plan: ``1 - actual duration / planned duration``; planned duration is
  the estimated completion date minus the actual start date;
- budget slack, share of plan: ``1 - actual effort / first estimate of effort`` (effort in hours
  is the budget the table records);
- scope: adjusted function points delivered.

The slack shares are negative for an overrun. The primary conditioning adds the package's shift,
10, to both (the worst overruns in the table are 8.9 times the planned duration and 5.9 times the
first estimate, so every shifted value is positive, the worst at 2.1); the ladder changes one
thing at a time.
"""

from __future__ import annotations

import argparse
import io
import sys
import urllib.request
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "examples"))

import fitkit  # noqa: E402

sys.path.insert(0, str(HERE))

import casekit  # noqa: E402

fitkit.read_threads()

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

NAMES = ["schedule slack", "budget slack", "scope"]
COLS = ["sched", "budget", "scope"]
PRIMARY_SHIFT = 10.0


def fetch(m):
    """Download the file of record into ``data/`` (once) and verify it."""
    data = HERE / "data"
    data.mkdir(exist_ok=True)
    path = data / m["file"]
    if not path.exists():
        urllib.request.urlretrieve(m["url"], path)
    fitkit.verify(path, m)
    return path


def read_arff(path):
    """The project table from the ARFF file; '?' reads as missing."""
    body = Path(path).read_text(encoding="utf-8-sig").split("@data", 1)[1].strip()
    cols = [
        "project",
        "client",
        "type",
        "start",
        "duration",
        "effort",
        "afp",
        "est_completion",
        "first_estimate",
        "estimate_method",
    ]
    df = pd.read_csv(io.StringIO(body), names=cols, na_values=["?"])
    df["start"] = pd.to_datetime(df["start"])
    df["est_completion"] = pd.to_datetime(df["est_completion"])
    return df


def derive(df):
    """Plans, actuals and the three attributes; drops rows without a positive planned duration."""
    x = df.copy()
    x["planned_duration"] = (x["est_completion"] - x["start"]).dt.days
    x = x.dropna(subset=["planned_duration"])
    x = x[x["planned_duration"] > 0].copy()
    x["sched_overrun"] = x["duration"] / x["planned_duration"]
    x["budget_overrun"] = x["effort"] / x["first_estimate"]
    x["sched"] = 1.0 - x["sched_overrun"]
    x["budget"] = 1.0 - x["budget_overrun"]
    x["scope"] = x["afp"]
    return x


def condition(x, shift=PRIMARY_SHIFT, scaler="standard", cap=None, ratio=False):
    """The attributes as strictly positive, larger-is-better metrics.

    ``shift`` is added to both slack shares (scope is not shifted); ``cap`` limits each overrun
    ratio before the shift; ``ratio=True`` uses plan over actual for both slacks instead (no
    shift needed: the log is the overrun's log with the sign turned).
    """
    from hyperbolic_trade_space import LogAffinePreconditioner

    a = x[COLS].to_numpy(float).copy()
    if ratio:
        a[:, 0] = 1.0 / x["sched_overrun"].to_numpy()
        a[:, 1] = 1.0 / x["budget_overrun"].to_numpy()
        s = [0.0, 0.0, 0.0]
    else:
        if cap is not None:
            a[:, 0] = 1.0 - np.minimum(x["sched_overrun"].to_numpy(), cap)
            a[:, 1] = 1.0 - np.minimum(x["budget_overrun"].to_numpy(), cap)
        s = [shift, shift, 0.0]
    pre = LogAffinePreconditioner(orientation=1, shift=s, scaler=scaler)
    return pre.fit_transform(a)


def ladder(x):
    """(label, metrics) of the primary conditioning and its one-change variants."""
    yield "primary: shift 10, standard", condition(x)
    yield "robust scaler", condition(x, scaler="robust")
    yield "no scaler", condition(x, scaler=None)
    yield "shift 20", condition(x, shift=20.0)
    yield "shift 40", condition(x, shift=40.0)
    yield "cap overrun at 3, shift 3", condition(x, shift=3.0, cap=3.0)
    yield "plan over actual (no shift)", condition(x, ratio=True)
    d = x[x["type"] == "D"]
    yield "development projects only", condition(d)
    p = x[x["type"] == "P"]
    yield "type P projects only", condition(p)
    c2 = x[x["client"] == 2]
    yield "client 2 only", condition(c2)


def figures(x, out):
    """The ternary of the primary K = 1 fit and its association panel (the band of ``casekit``)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from hyperbolic_trade_space import (
        HyperbolicTradeSpace,
        select_temperature,
        trade_off_report,
    )
    from hyperbolic_trade_space.plotting import plot_association, plot_ternary

    M = condition(x)
    tau = float(select_temperature(M, target_frac_above=0.1, bounds=(3.0, 1e4)))
    est = HyperbolicTradeSpace(temperature=tau, random_state=0).fit(M)
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    plot_ternary(est, M, names=NAMES, ax=ax, scheme="light")
    fig.savefig(out / "kitchenham-ternary.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rep = trade_off_report(est, M, band=casekit._band(est.training_log_v_, tau))
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    plot_association(rep, names=NAMES, ax=ax)
    fig.savefig(out / "kitchenham-association.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def describe(x):
    """Counts and medians a project manager reads first."""
    on_or_under = lambda s: float((s <= 1.0).mean())  # noqa: E731
    return {
        "rows_in_table": None,
        "rows_kept": len(x),
        "median_schedule_overrun_ratio": float(x["sched_overrun"].median()),
        "median_budget_overrun_ratio": float(x["budget_overrun"].median()),
        "share_on_or_under_schedule": on_or_under(x["sched_overrun"]),
        "share_on_or_under_budget": on_or_under(x["budget_overrun"]),
        "share_exactly_on_schedule": float((x["sched_overrun"] == 1.0).mean()),
        "worst_schedule_overrun_ratio": float(x["sched_overrun"].max()),
        "worst_budget_overrun_ratio": float(x["budget_overrun"].max()),
        "median_function_points": float(x["afp"].median()),
        "log_correlation": {
            f"{a}|{b}": float(np.corrcoef(np.log(x[a]), np.log(x[b]))[0, 1])
            for a, b in [
                ("sched_overrun", "budget_overrun"),
                ("sched_overrun", "afp"),
                ("budget_overrun", "afp"),
            ]
        },
    }


def frontier_projects(x):
    """The near-frontier projects of the primary fit in plan-and-actual terms, against all rows."""
    from hyperbolic_trade_space import HyperbolicTradeSpace, select_temperature

    M = condition(x)
    tau = float(select_temperature(M, target_frac_above=0.1, bounds=(3.0, 1e4)))
    est = HyperbolicTradeSpace(temperature=tau, random_state=0).fit(M)
    lv = est.training_log_v_
    near = np.abs(lv) < casekit._band(lv, tau)
    cols = ["sched_overrun", "budget_overrun", "afp"]

    def summ(f):
        return {c: float(f[c].median()) for c in cols} | {"rows": len(f)}

    top = x.iloc[np.argsort(-lv)[:15]]
    return {
        "near_frontier": summ(x[near]),
        "all": summ(x),
        "top_15_by_log_v": summ(top),
        "near_frontier_rows": x.loc[near, ["project", "type", *cols]].to_dict("records"),
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="download the file of record if absent")
    ap.add_argument("--file", default=None, help="a local copy of the file of record")
    a = ap.parse_args(argv)
    m = fitkit.load_manifest(HERE / "manifest.toml")
    if a.file:
        path = Path(a.file)
        fitkit.verify(path, m)
    else:
        path = fetch(m) if a.fetch else HERE / "data" / m["file"]
        fitkit.verify(path, m)
    df = read_arff(path)
    x = derive(df)
    res = {"describe": describe(x), "runs": {}}
    res["describe"]["rows_in_table"] = len(df)
    for label, M in ladder(x):
        r = casekit.fit_read(M, NAMES)
        res["runs"][label] = r
        print(
            f"{label:32s} n={r['n']:3d} tau={r['tau_selected']:7.2f} "
            f"w={np.round(list(r['exponents_k1'].values()), 2)} set={r['contending_set']} "
            f"assoc={ {k: round(v, 2) for k, v in r['association'].items()} }",
            flush=True,
        )
    res["frontier_projects"] = frontier_projects(x)
    fitkit.dump(res, HERE / "results_kitchenham.json")
    (HERE / "figures").mkdir(exist_ok=True)
    figures(x, HERE / "figures")


if __name__ == "__main__":
    main()
