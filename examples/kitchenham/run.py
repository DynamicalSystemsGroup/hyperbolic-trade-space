"""WP76 Kitchenham-CSC example: fetch the project table, derive the three sides, fit, record.

``uv run python examples/kitchenham/run.py --fetch``   download the file of record into ``data/``
(git-ignored), verify it against ``manifest.toml``, derive ``derived/projects.csv``, fit and write
``results.json``. ``--file PATH`` reads a local copy of the file of record instead (verified the
same way). ``--check`` refits from the committed derived table and compares with the committed
``results.json`` (every value but the run's own provenance), the reproduction check of R-1.

One row is one software project (145, one company, 1994 to 1999: Kitchenham, Pfleeger, McColl and
Eagan 2002). The table carries a first estimate and an actual for effort (hours), an estimated
completion date and an actual duration (days), and the delivered size in adjusted function points:
the three sides of the iron triangle, with no quality measure. Effort stands for the budget.

Attributes, before conditioning (each stated in ``kitchenham.sysml``, the case model, whose values
``tests/test_wp76_kitchenham.py`` holds equal to the constants below):

- schedule slack, share of plan: ``1 - actual duration / planned duration``, planned duration the
  estimated completion date minus the actual start date;
- budget slack, share of plan: ``1 - actual effort / first estimate``;
- scope: adjusted function points delivered.

A slack share is negative for an overrun. The primary conditioning adds the shift 10 to both
slacks (the worst overruns are 8.9 times the planned duration and 5.9 times the estimate, so every
shifted value is positive, the smallest 2.1), leaves scope unshifted, and gives each log a standard
scaler; orientation +1 for all three. The WP70 probe's script is in history at
``git show 4f81a4ea:work-packages/WP70-rounds/case/kitchenham.py``; the derivation is carried over.
"""

from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import urllib.request
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import fitkit  # noqa: E402

fitkit.read_threads()

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

NAMES = ["schedule slack", "budget slack", "scope"]
COLS = ["sched", "budget", "scope"]
ORIENTATION = [1, 1, 1]  # larger is better for every side
SHIFT = 10.0  # added to both slack shares (not to scope); kitchenham.sysml `Conditioning::shift`
SCALER = "standard"  # of the logs
TARGET_FRAC_ABOVE = 0.10  # the fit temperature puts a tenth of the projects above V = 1
TAU_BOUNDS = (3.0, 1e4)
MIN_NEAR = 15  # the band widens to the smallest band holding this many rows (the WP70 rule)
MIN_NEAR_REPORT = 10  # the report's own guard, left at the package default
SEED = 0
K2_RESTARTS = 5
ARFF_COLUMNS = [
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
DERIVED = HERE / "derived" / "projects.csv"


def fetch(m):
    """Download the file of record into ``data/`` (once) and verify it against the manifest."""
    data = HERE / "data"
    data.mkdir(exist_ok=True)
    path = data / m["file"]
    if not path.exists():
        urllib.request.urlretrieve(m["url"], path)
    fitkit.verify(path, m)
    return path


def read_arff(path):
    """The project table from the ARFF file; ``?`` reads as missing."""
    body = Path(path).read_text(encoding="utf-8-sig").split("@data", 1)[1].strip()
    df = pd.read_csv(io.StringIO(body), names=ARFF_COLUMNS, na_values=["?"])
    df["start"] = pd.to_datetime(df["start"])
    df["est_completion"] = pd.to_datetime(df["est_completion"])
    return df


def derive(df):
    """Plans, actuals and the three attributes; keeps rows whose planned duration is positive."""
    x = df.copy()
    x["planned_duration"] = (x["est_completion"] - x["start"]).dt.days
    x = x.dropna(subset=["planned_duration"])
    x = x[x["planned_duration"] > 0].copy()
    x["planned_duration"] = x["planned_duration"].astype(int)
    x["sched_overrun"] = x["duration"] / x["planned_duration"]
    x["budget_overrun"] = x["effort"] / x["first_estimate"]
    x["sched"] = 1.0 - x["sched_overrun"]
    x["budget"] = 1.0 - x["budget_overrun"]
    x["scope"] = x["afp"]
    keep = [
        "project",
        "client",
        "type",
        "planned_duration",
        "duration",
        "first_estimate",
        "effort",
        "afp",
        "sched_overrun",
        "budget_overrun",
        *COLS,
    ]
    return x[keep].reset_index(drop=True)


def condition(x, shift=SHIFT, scaler=SCALER, cap=None, ratio=False):
    """The attributes as strictly positive, larger-is-better metrics.

    ``shift`` is added to both slack shares (scope is not shifted); ``cap`` limits each overrun
    ratio before the shift; ``ratio=True`` uses plan over actual for both slacks instead (no shift:
    the log is the overrun's log with its sign turned).
    """
    from hyperbolic_trade_space import LogAffinePreconditioner

    a = x[COLS].to_numpy(float).copy()
    if ratio:
        a[:, 0] = 1.0 / x["sched_overrun"].to_numpy(float)
        a[:, 1] = 1.0 / x["budget_overrun"].to_numpy(float)
        s = [0.0, 0.0, 0.0]
    else:
        if cap is not None:
            a[:, 0] = 1.0 - np.minimum(x["sched_overrun"].to_numpy(float), cap)
            a[:, 1] = 1.0 - np.minimum(x["budget_overrun"].to_numpy(float), cap)
        s = [shift, shift, 0.0]
    pre = LogAffinePreconditioner(orientation=ORIENTATION, shift=s, scaler=scaler)
    return pre.fit_transform(a)


def band_for(log_v, tau, k=MIN_NEAR):
    """``1 / tau``, or the smallest band holding ``k`` rows when ``1 / tau`` holds fewer."""
    a = np.sort(np.abs(log_v[np.isfinite(log_v)]))
    need = float(a[min(k, len(a)) - 1]) * 1.0001 if len(a) else np.inf
    return max(1.0 / tau, need)


def smallest_band(log_v, k):
    """The smallest band holding ``k`` rows."""
    a = np.sort(np.abs(log_v[np.isfinite(log_v)]))
    return float(a[min(k, len(a)) - 1]) * 1.0001


def report_dict(est, M, names, band):
    """The trade-off report at ``band`` as a JSON-ready dict (one dict per term for K > 1)."""
    from hyperbolic_trade_space import trade_off_report

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rep = trade_off_report(est, M, band=band, min_near_frontier=MIN_NEAR_REPORT)
    reps = rep if isinstance(rep, list) else [rep]
    out = []
    for r in reps:
        out.append(
            {
                "contending_set": [names[j] for j in r.contending_set],
                "contending_exponents": [float(v) for v in r.contending_exponents],
                "n_lemma": int(r.n_lemma),
                "band": float(r.band),
                "n_near_frontier": int(r.n_near_frontier),
                "association": {
                    f"{names[i]}|{names[j]}": float(r.association[i, j])
                    for i in range(len(names))
                    for j in range(i + 1, len(names))
                },
            }
        )
    return out


def fit_k1(M, tau=None):
    """The K = 1 fit at the selected temperature (or at ``tau``); returns (estimator, tau)."""
    from hyperbolic_trade_space import HyperbolicTradeSpace, select_temperature

    if tau is None:
        tau = float(select_temperature(M, target_frac_above=TARGET_FRAC_ABOVE, bounds=TAU_BOUNDS))
    return HyperbolicTradeSpace(temperature=tau, random_state=SEED).fit(M), tau


def read(M, names=NAMES, k2=True, min_near=MIN_NEAR):
    """Temperature, the K = 1 fit and its report at the band rule, and the K = 2 assessment."""
    from hyperbolic_trade_space import HyperbolicTradeSpace

    M = np.asarray(M, float)
    est, tau = fit_k1(M)
    band = band_for(est.training_log_v_, tau, k=min_near)
    rep = report_dict(est, M, names, band)[0]
    out = {
        "n": int(M.shape[0]),
        "metrics": list(names),
        "tau_selected": tau,
        "frac_above": float(est.frac_above_),
        "exponents_k1": dict(zip(names, map(float, est.exponents_[0]), strict=True)),
        "mean_slack_k1": float(est.mean_slack_),
        "band_1_over_tau": 1.0 / tau,
        "band_widened": bool(band > 1.0 / tau),
        **rep,
    }
    if k2 and M.shape[0] >= 40:
        e2 = HyperbolicTradeSpace(
            n_terms=2, temperature=tau, random_state=SEED, n_restarts=K2_RESTARTS
        ).fit(M)
        k2out = {
            "exponents": [dict(zip(names, map(float, w), strict=True)) for w in e2.exponents_],
            "term_share": [float(s) for s in e2.term_share_],
            "mean_slack": float(e2.mean_slack_),
            "status": getattr(e2.termination_, "status", None),
        }
        try:
            k2out["terms"] = report_dict(e2, M, names, band)
        except ValueError as err:
            k2out["terms"] = str(err)[:240]
        out["k2"] = k2out
    return out


def describe(df, x):
    """Counts and medians a project manager reads first."""
    return {
        "rows_in_table": len(df),
        "rows_kept": len(x),
        "rows_excluded": int(len(df) - len(x)),
        "no_estimated_completion": int(df["est_completion"].isna().sum()),
        "projects_by_type": {k: int(v) for k, v in x["type"].value_counts().sort_index().items()},
        "projects_by_client": {
            str(k): int(v) for k, v in x["client"].value_counts().sort_index().items()
        },
        "median_schedule_overrun_ratio": float(x["sched_overrun"].median()),
        "median_budget_overrun_ratio": float(x["budget_overrun"].median()),
        "share_on_or_under_schedule": float((x["sched_overrun"] <= 1.0).mean()),
        "share_on_or_under_budget": float((x["budget_overrun"] <= 1.0).mean()),
        "share_exactly_on_schedule": float((x["sched_overrun"] == 1.0).mean()),
        "worst_schedule_overrun_ratio": float(x["sched_overrun"].max()),
        "worst_budget_overrun_ratio": float(x["budget_overrun"].max()),
        "smallest_shifted_slack": float(
            min((SHIFT + x["sched"]).min(), (SHIFT + x["budget"]).min())
        ),
        "median_function_points": float(x["afp"].median()),
        "largest_function_points": float(x["afp"].max()),
        "log_correlation_all_rows": {
            f"{a}|{b}": float(np.corrcoef(np.log(x[a]), np.log(x[b]))[0, 1])
            for a, b in [
                ("sched_overrun", "budget_overrun"),
                ("sched_overrun", "afp"),
                ("budget_overrun", "afp"),
            ]
        },
    }


def frontier_projects(x, res):
    """The near-frontier projects of the primary fit, in plan-and-actual terms."""
    M = condition(x)
    est, _tau = fit_k1(M, res["tau_selected"])
    lv = est.training_log_v_
    near = np.abs(lv) < res["band"]
    cols = ["sched_overrun", "budget_overrun", "afp"]

    def summ(f):
        return {c: float(f[c].median()) for c in cols} | {"rows": len(f)}

    rows = x.loc[near, ["project", "type", "client", *cols]].copy()
    rows["log_v"] = lv[near]
    return {
        "near_frontier": summ(x[near]),
        "all": summ(x),
        "near_frontier_rows": json.loads(rows.to_json(orient="records")),
    }


def provenance():
    """The package version and the Git SHA of the run (the memo's G1)."""
    import hyperbolic_trade_space

    def git(*args):
        try:
            return subprocess.run(
                ["git", *args], cwd=HERE, capture_output=True, text=True, check=True
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return None

    sha = git("rev-parse", "HEAD")
    dirty = git("status", "--porcelain", "--", str(HERE)) if sha else None
    return {
        "package_version": hyperbolic_trade_space.__version__,
        "git_sha": sha,
        "git_dirty": None if dirty is None else bool(dirty),
    }


def write_derived(x, m):
    """The derived table and its licence note, committed under CC BY 4.0."""
    DERIVED.parent.mkdir(exist_ok=True)
    x.to_csv(DERIVED, index=False)
    (DERIVED.parent / "LICENCE-DATA.txt").write_text(
        f"{m['licence_text']}\n\nAttribution: {m['attribution']}\nSource: {m['landing_page']}\n"
        f"Licence: {m['licence_url']}\nThis table is derived from the source file: the 141 "
        "projects with a positive planned duration, with the planned duration (days), the overrun "
        "ratios and the three attributes (schedule slack and budget slack as shares of plan, scope "
        "in adjusted function points) computed from the source's columns.\n",
        encoding="utf-8",
    )


def results(df, x):
    """Everything ``results.json`` holds."""
    res = {"describe": describe(df, x), "provenance": provenance(), "runs": {}}
    res["runs"]["primary"] = read(condition(x))
    res["frontier_projects"] = frontier_projects(x, res["runs"]["primary"])
    return res


def load_derived():
    """The committed derived table."""
    return pd.read_csv(DERIVED)


def check():
    """Refit from the committed derived table; compare with the committed results (R-1)."""
    x = load_derived()
    committed = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    fresh = {"runs": {"primary": read(condition(x))}}
    fresh["frontier_projects"] = frontier_projects(x, fresh["runs"]["primary"])
    a = json.dumps({k: committed[k] for k in fresh}, sort_keys=True)
    b = json.dumps(fresh, sort_keys=True)
    if a != b:
        raise SystemExit("results.json differs from a fresh run on the derived table")
    print("results.json reproduced from derived/projects.csv (provenance keys excluded)")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="download the file of record if absent")
    ap.add_argument("--file", default=None, help="a local copy of the file of record")
    ap.add_argument("--check", action="store_true", help="the reproduction check (R-1)")
    a = ap.parse_args(argv)
    if a.check:
        return check()
    m = fitkit.load_manifest(HERE / "manifest.toml")
    path = Path(a.file) if a.file else (fetch(m) if a.fetch else HERE / "data" / m["file"])
    fitkit.verify(path, m)
    df = read_arff(path)
    x = derive(df)
    write_derived(x, m)
    res = results(df, x)
    p = res["runs"]["primary"]
    print(
        f"n={p['n']} tau={p['tau_selected']:.2f} w={np.round(list(p['exponents_k1'].values()), 3)} "
        f"set={p['contending_set']} band={p['band']:.4f} near={p['n_near_frontier']} "
        f"assoc={ {k: round(v, 2) for k, v in p['association'].items()} }"
    )
    fitkit.dump(res, HERE / "results.json")
    return None


if __name__ == "__main__":
    main()
