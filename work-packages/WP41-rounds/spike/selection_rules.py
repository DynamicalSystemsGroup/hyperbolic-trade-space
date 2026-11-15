# ruff: noqa: E402, B023
"""WP41 spike: three selection rules for the conjecture route, run once each on the case.

    MPLCONFIGDIR=$(mktemp -d) uv run python work-packages/WP41-rounds/spike/selection_rules.py

The data of record: the v2 primary table (examples/adcs/data/v2), the four-metric view, the
regressor, chart, temperature and seeded pool of ``experiments/check_designs.py`` (the committed
proposals of ``v2-check-predictions@12`` are recomputed first and compared). Targets: the hole
centres of the three committed proposals (``target_z*``, log V = 0) plus the next NEXT isolated,
separated holes of the same chart (predicted only). Each rule maps a target to a configuration;
distance of a predicted chart point to a target is sqrt(|dZ|^2 + (2 log V)^2), as in the existing
rule. A rule reaches a target within the proposer's reach (the 2nd percentile of the nearest
pool distances over the 300 most isolated holes) or within the band 1/tau. The proposals for the
first three targets are then built (measured once through the v2 oracle) and checked with the
tests of ``case.predict_check``: confirmed when the design is feasible and both |dlogV| and ||dZ||
between measured and predicted chart point are within the band, infeasible when a feasibility flag
fails, refuted otherwise.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
ADCS = ROOT / "examples" / "adcs"
sys.path.insert(0, str(ADCS))
from experiments import check_designs as cd
from experiments import cubesat_oracle as co
from experiments import definitions as defs
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.pipeline import make_pipeline

from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    TradeSpaceRegressor,
    select_temperature,
)
from hyperbolic_trade_space.gaps import find_holes

NEXT = 7
EXP = {e.id: e for e in defs.V2}
proposer = cd.Proposer(EXP["v2-check-predictions"])
ranges, levels = proposer.ranges, proposer.levels
fe = proposer.feasible_primary()
Y = fe[list(cd.METRICS)].to_numpy(float)
pre = LogAffinePreconditioner(orientation=[-1] * 4, scaler="standard")
tau = select_temperature(pre.fit_transform(Y), target_frac_above=0.10, bounds=(3, 1e3))
band = 1.0 / float(tau)
ts = make_pipeline(
    LogAffinePreconditioner(orientation=[-1] * 4, scaler="standard"),
    HyperbolicTradeSpace(temperature=tau),
)
gp = GaussianProcessRegressor(
    kernel=ConstantKernel(1.0) * RBF(length_scale=np.ones(6)) + WhiteKernel(0.1),
    normalize_y=True,
    n_restarts_optimizer=2,
    random_state=0,
)
F_data = cd._features(fe, ranges, levels)
reg = TradeSpaceRegressor(gp, ts).fit(F_data, Y)
chart = reg.trade_space_.transform(Y)
Z_data = chart[:, :-1]

# the seeded pool of the proposer (same draws as Proposer.draw)
seed, P = defs.CHECK_SEED, cd.POOL
rng = np.random.default_rng(seed)
fleet = np.random.default_rng(np.random.SeedSequence(seed, spawn_key=(1,)))
lo_n, hi_n = ranges["fleet_size"]
pool = pd.DataFrame(
    {
        "panel_span_m": np.exp(rng.uniform(*np.log(ranges["panel_span_m"]), P)),
        "battery_wh": np.exp(rng.uniform(*np.log(ranges["battery_wh"]), P)),
        "Kp": np.exp(rng.uniform(*np.log(ranges["Kp"]), P)),
        "Kd": np.exp(rng.uniform(*np.log(ranges["Kd"]), P)),
        "wheel_class": rng.choice(levels["wheel_class"], P),
        "st_grade": rng.choice(levels["st_grade"], P),
        "fleet_size": fleet.integers(lo_n, hi_n + 1, P).astype(float),
    }
)
F_pool = cd._features(pool, ranges, levels)
Zp, lvp = cd._predict_chunked(reg, F_pool)


def dist_to(target, Z, lv):
    return np.sqrt(((Z - target) ** 2).sum(axis=-1) + (2 * lv) ** 2)


holes, scores = find_holes(Z_data, resolution=30, threshold=2.0)
nearest = [float(dist_to(h, Zp, lvp).min()) for h in holes[: cd.HOLES]]
reach = float(np.quantile(nearest, cd.REACH_QUANTILE))
nn = cKDTree(Z_data).query(Z_data, k=2)[0][:, 1]
sep = 1.5 * float(np.median(nn))

# the three committed proposals' targets, and the next separated holes
committed = pd.read_csv(ADCS / "data" / "v2" / "check_predictions_cubesat.csv")
targets = [
    committed.loc[k, ["target_z1", "target_z2", "target_z3"]].to_numpy(float) for k in range(3)
]
extra = []
for h in holes[: cd.HOLES]:
    if any(np.linalg.norm(h - c) <= sep for c in targets + extra):
        continue
    extra.append(h)
    if len(extra) == NEXT:
        break
targets += extra
tree = cKDTree(Z_data)


def pool_row(i):
    return F_pool[i], float(pool.fleet_size.iloc[i])


def rule_pool(target, ref):
    """The existing rule: the pooled configuration whose predicted point is nearest the target."""
    d = dist_to(target, Zp, lvp)
    i = int(np.argmin(d))
    return (*pool_row(i), d[i])


def rule_reference(target, ref):
    """Smallest change from the reference design among pool points predicted within the reach."""
    d = dist_to(target, Zp, lvp)
    ok = np.flatnonzero(d <= reach)
    if len(ok) == 0:
        i = int(np.argmin(d))
        return (*pool_row(i), d[i])
    i = ok[int(np.argmin(np.abs(F_pool[ok] - ref[0]).sum(axis=1)))]
    return (*pool_row(i), d[i])


def rule_search(target, ref):
    """Search over the surrogate: box on the four continuous features, the nine categorical
    combinations enumerated, L-BFGS-B from several starts, minimising the predicted distance."""
    best = (None, np.inf)
    r = np.random.default_rng(1)
    for w in (0.0, 0.5, 1.0):
        for t in (0.0, 0.5, 1.0):

            def f(x):
                Z, lv = reg.predict_coordinates(np.r_[x, w, t].reshape(1, -1))
                return float(dist_to(target, Z[0], np.ravel(lv)[0]))

            for s in range(4):
                x0 = r.uniform(0, 1, 4) if s else ref[0][:4]
                res = minimize(f, x0, bounds=[(0, 1)] * 4, method="L-BFGS-B")
                if res.fun < best[1]:
                    best = (np.r_[res.x, w, t], res.fun)
    return best[0], ref[1], best[1]


RULES = {
    "nearest in pool": rule_pool,
    "smallest change": rule_reference,
    "surrogate search": rule_search,
}


def config_of(F, fleet_size):
    out = {}
    for j, c in enumerate(["panel_span_m", "battery_wh", "Kp", "Kd"]):
        lo, hi = ranges[c]
        out[c] = float(np.exp(np.log(lo) + F[j] * (np.log(hi) - np.log(lo))))
    out["wheel_class"] = levels["wheel_class"][round(F[4] * 2)]
    out["st_grade"] = levels["st_grade"][round(F[5] * 2)]
    out["fleet_size"] = fleet_size
    return out


rows = []
for k, tg in enumerate(targets):
    j = int(tree.query(tg)[1])
    ref = (F_data[j], float(fe.fleet_size.iloc[j]))  # the datum nearest the target
    for name, rule in RULES.items():
        F, fs, _ = rule(tg, ref)
        z, lv = reg.predict_coordinates(F.reshape(1, -1))
        d = float(dist_to(tg, z[0], np.ravel(lv)[0]))
        rows.append(
            dict(
                target=k + 1,
                rule=name,
                reach=d,
                in_reach=d <= reach,
                in_band=d <= band,
                change=float(np.abs(F - ref[0]).sum()),
                pred=np.r_[z[0], np.ravel(lv)[0]],
                cfg=config_of(F, fs),
            )
        )
df = pd.DataFrame(rows)
print(
    f"proposer reach = {reach:.4f}; tau = {tau:.3f}, band = {band:.4f}, n_train = {len(fe)}, "
    f"targets = {len(targets)} (3 committed + {NEXT})"
)
# the existing rule must reproduce the committed proposals
mine = df[(df.rule == "nearest in pool") & (df.target <= 3)]
same = [
    all(
        abs(r.cfg[c] - committed.loc[r.target - 1, c]) < 1e-6 * max(1, abs(r.cfg[c]))
        for c in ("panel_span_m", "battery_wh", "Kp", "Kd")
    )
    and r.cfg["wheel_class"] == committed.loc[r.target - 1, "wheel_class"]
    for _, r in mine.iterrows()
]
print("existing rule reproduces the committed proposals:", same)
summ = df.groupby("rule").agg(
    in_reach=("in_reach", "sum"),
    in_band=("in_band", "sum"),
    median_distance=("reach", "median"),
    median_change=("change", "median"),
)
print(summ.to_string())
print(df.pivot(index="target", columns="rule", values="reach").round(3).to_string())

# build and measure the first three targets, once per rule, and check
oracle = co.build(EXP["v2-check-designs"], workers=1)
rec = []
for _, r in df[df.target <= 3].iterrows():
    res = oracle(r.cfg)
    m = np.array([[res[a] for a in cd.METRICS]], float)
    flags = {f: bool(res[f]) for f in ("settled", "power_ok", "momentum_ok", "dod_ok")}
    c = np.ravel(reg.trade_space_.transform(m))
    dz = float(np.linalg.norm(c[:-1] - r.pred[:-1]))
    dl = float(c[-1] - r.pred[-1])
    ok = abs(dl) <= band and dz <= band
    out = "infeasible" if not all(flags.values()) else ("confirmed" if ok else "refuted")
    rec.append(
        dict(
            target=int(r.target),
            rule=r.rule,
            pred_dist=round(r.reach, 4),
            dZ=round(dz, 4),
            dlogV=round(dl, 4),
            failed=",".join(k for k, v in flags.items() if not v) or "-",
            outcome=out,
        )
    )
print(pd.DataFrame(rec).to_string(index=False))
for _, r in df[df.target <= 3].iterrows():
    print(
        r.target,
        r.rule,
        {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.cfg.items()},
    )
