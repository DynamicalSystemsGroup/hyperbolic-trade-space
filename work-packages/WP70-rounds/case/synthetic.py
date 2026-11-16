"""WP70 synthetic portfolio: the iron triangle with m = 2 quality metrics, a planted answer.

``uv run python work-packages/WP70-rounds/case/synthetic.py``  generate, fit under two
conditionings, write ``results_synthetic.json`` and ``figures/synthetic-association.png``.

The design is ``../synthetic.md``. In short: a portfolio of projects, each with a planned duration
and budget and their actuals, delivered story points and two quality metrics (mean days between
escaped defects; a user-acceptance score). The larger-is-better quantities, plan over actual for
time and money, story points and the two quality metrics, are drawn around a planted two-term
frontier (``make_frontier_data``): term 1 is the iron triangle (time, money, scope trade; quality
free), term 2 squeezes the first quality metric against scope and time; the user-acceptance score
is in neither term (a planted non-participant). Slack is then derived from plan and actual as a
share of the plan, as a project office would report it.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "examples"))
sys.path.insert(0, str(HERE))

import casekit  # noqa: E402
import fitkit  # noqa: E402

fitkit.read_threads()

import numpy as np  # noqa: E402

NAMES = ["schedule slack", "budget slack", "scope", "defect interval", "acceptance"]
PLANTED = np.array(
    [
        [0.30, 0.30, 0.40, 0.00, 0.00],  # term 1: the iron triangle, quality free
        [0.25, 0.00, 0.25, 0.50, 0.00],  # term 2: defects against scope and schedule
    ]
)
# typical log-spread of each larger-is-better quantity in raw units (plan/actual, story points,
# days between escaped defects, acceptance score)
LOG_SPREAD = np.array([0.25, 0.30, 0.8, 0.6, 0.15])
LOG_CENTRE = np.log([1.0, 1.0, 120.0, 30.0, 7.0])


def generate(n=300, noise=0.05, seed=7):
    """A synthetic portfolio: plans, actuals, story points, two quality metrics, and the truth."""
    from hyperbolic_trade_space import make_frontier_data

    X, info = make_frontier_data(
        n,
        5,
        exponents=PLANTED,
        n_terms=2,
        noise=noise,
        frontier_fraction=0.3,
        interior_scale=0.5,
        random_state=seed,
    )
    u = np.log(X)
    sd = u.std(axis=0)
    raw_log = LOG_CENTRE + LOG_SPREAD * (u - u.mean(axis=0)) / sd
    good = np.exp(raw_log)  # larger-is-better quantities in raw units
    rng = np.random.default_rng(seed + 1)
    plan_days = np.exp(rng.normal(np.log(90), 0.4, n))
    plan_cost = 4.0 * good[:, 2] * np.exp(rng.normal(0, 0.2, n))  # thousands, ~ story points
    actual_days = plan_days / good[:, 0]
    actual_cost = plan_cost / good[:, 1]
    table = {
        "plan_days": plan_days,
        "actual_days": actual_days,
        "plan_cost": plan_cost,
        "actual_cost": actual_cost,
        "story_points": good[:, 2],
        "defect_interval_days": good[:, 3],
        "acceptance": good[:, 4],
    }
    # the planted exponents as a standard scaler of the raw logs sees them: w_j * sd(u_j),
    # renormalized (the raw units' spread cancels; only the planted log-spread remains)
    implied = PLANTED * sd
    implied = implied / implied.sum(axis=1, keepdims=True)
    return table, {"term": info["term"], "frontier_mask": info["frontier_mask"], "implied": implied}


def condition(t, form="ratio", shift=None, scaler="standard"):
    """Five metrics: ``form='ratio'`` plan over actual, ``'share'`` 1 - actual/plan + shift."""
    from hyperbolic_trade_space import LogAffinePreconditioner

    if form == "ratio":
        s_t = t["plan_days"] / t["actual_days"]
        s_b = t["plan_cost"] / t["actual_cost"]
        sh = [0.0] * 5
    else:
        s_t = 1.0 - t["actual_days"] / t["plan_days"]
        s_b = 1.0 - t["actual_cost"] / t["plan_cost"]
        sh = [shift, shift, 0.0, 0.0, 0.0]
    A = np.column_stack([s_t, s_b, t["story_points"], t["defect_interval_days"], t["acceptance"]])
    pre = LogAffinePreconditioner(orientation=1, shift=sh, scaler=scaler)
    return pre.fit_transform(A)


def worst_overrun(t):
    """The largest actual-over-plan ratio of time or money in the portfolio."""
    days = t["actual_days"] / t["plan_days"]
    cost = t["actual_cost"] / t["plan_cost"]
    return float(max(days.max(), cost.max()))


def match(W, planted):
    """L1 distance of each planted term to its nearest fitted term."""
    W = np.atleast_2d(W)
    return [float(np.abs(W - p).sum(axis=1).min()) for p in planted]


def main():
    res = {"planted": PLANTED.tolist(), "names": NAMES, "runs": {}}
    for noise in (0.05, 0.15):
        t, truth = generate(noise=noise)
        worst = worst_overrun(t)
        shift = float(np.ceil(worst))
        res[f"worst_overrun_noise_{noise}"] = worst
        for label, M in (
            ("plan over actual", condition(t)),
            (f"share of plan, shift {shift:g}", condition(t, "share", shift)),
            (f"share of plan, shift {4 * shift:g}", condition(t, "share", 4 * shift)),
        ):
            r = casekit.fit_read(M, NAMES)
            W2 = [list(e.values()) for e in r["k2"]["exponents"]]
            r["k2"]["distance_to_planted"] = match(W2, truth["implied"])
            r["k2"]["implied_planted"] = truth["implied"].tolist()
            key = f"noise {noise}: {label}"
            res["runs"][key] = r
            print(
                key,
                np.round(list(r["exponents_k1"].values()), 2),
                r["contending_set"],
                "| K2",
                np.round(W2, 2).tolist(),
                np.round(r["k2"]["distance_to_planted"], 2),
                flush=True,
            )
    fitkit.dump(res, HERE / "results_synthetic.json")
    figure(*generate(noise=0.05))


def figure(t, truth):
    """The association panels of the K = 2 fit under the ratio conditioning."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from hyperbolic_trade_space import (
        HyperbolicTradeSpace,
        select_temperature,
        trade_off_report,
    )
    from hyperbolic_trade_space.plotting import plot_association

    M = condition(t)
    tau = float(select_temperature(M, target_frac_above=0.1, bounds=(3.0, 1e4)))
    e2 = HyperbolicTradeSpace(n_terms=2, temperature=tau, random_state=0, n_restarts=5).fit(M)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        reps = trade_off_report(e2, M, band=casekit._band(e2.training_log_v_, tau))
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    plot_association(reps, names=NAMES, ax=axs)
    for a in axs:
        plt.setp(a.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()
    (HERE / "figures").mkdir(exist_ok=True)
    fig.savefig(HERE / "figures" / "synthetic-association.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
