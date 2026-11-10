"""The v2 check designs: propose, predict, then simulate (WP15 15.4), through the runner and ledger.

The flow mirrors ``make_check_designs.py`` (WP7), as two ledgered experiments:

``v2-check-predictions``
    The sampler (``Proposer``) fits ``TradeSpaceRegressor`` on the feasible designs of the ``v2``
    primary data (the parent entry's output), takes the most isolated, well-separated holes of the
    data's chart and maps each to the configuration of a seeded pool whose predicted
    ``[Z | log V]`` is nearest. The oracle (``Passthrough``) measures nothing: the file is the
    proposals with their predictions. It is committed, and its entry recorded, before the
    simulation entry exists.
``v2-check-designs``
    The sampler (``Checks``) joins the hand-written candidates (declared in the experiment's
    ``inputs``) to the committed proposals; the oracle (``CheckOracle``) simulates all six once
    with the ``v2`` cubesat oracle and lays the columns out as the frozen check-design file.

Only the estimator names pinned by the WP14 contract are used. The ranges, enumerations and
scenario come from the model through ``CubesatOracle``; the method parameters (pool size, hole
finder settings) are the frozen script's and sit in this file; the reach is set by the rule stated
at WP23's data gate (``REACH_QUANTILE``, below), where the frozen script typed a constant.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from . import ledger as lg
from .cubesat_oracle import ATTRIBUTE_NAMES, CONFIG_NAMES, SCENARIO_COLUMNS, build, build_sampler

POOL = 100_000
# The reach: a hole counts as reachable when a seeded configuration is predicted within it, in
# [Z | 2 log V] distance. WP7 typed 0.35 for the slew-time view with no stated rule; the rule stated
# at WP23's data gate (WP23-decisions.md, "The proposer's reach on the settling-time view") is the
# 2nd percentile of the nearest predicted distances from the pool to the HOLES most isolated holes
# of the view in use, computed from the data at run time (on the slew-time view it returns 0.351,
# the value WP7 used in effect). The proposer returns the reachable, separated holes it finds, up
# to the count asked, and prints how many: fewer is a result, not a failure.
REACH_QUANTILE = 0.02
HOLES = 300  # the most isolated holes the proposer reads
METRICS = ("settling_time_s", "pointing_error_deg", "control_effort", "total_mass_kg")
LEAD = ("role", "design_id", "name", "seed", *CONFIG_NAMES, *ATTRIBUTE_NAMES)
FLAGS = ("settled", "momentum_ok", "power_ok", "dod_ok", "torque_saturated_frac")


def _path(experiment, key: str, root: Path | None = None) -> Path:
    try:
        return Path(root or lg.REPO_ROOT) / experiment.inputs[key]
    except KeyError:
        raise ValueError(f"{experiment.id}: inputs lack {key!r}") from None


def _ranges_and_levels(experiment, root):
    """Ranges (aggressive gain box) and enumeration levels, read from the experiment's model."""
    sampler = build_sampler(experiment, root)
    return sampler.log_ranges, sampler.categorical


def _features(df: pd.DataFrame, ranges, levels) -> np.ndarray:
    """Configuration -> regressor features in [0, 1]: log-scaled continuous, ordinal categories."""
    cols = []
    for c in ("panel_span_m", "battery_wh", "Kp", "Kd"):
        lo, hi = ranges[c]
        cols.append((np.log(df[c].to_numpy(float)) - np.log(lo)) / (np.log(hi) - np.log(lo)))
    for c in ("wheel_class", "st_grade"):
        order = {w: i / (len(levels[c]) - 1) for i, w in enumerate(levels[c])}
        cols.append(df[c].map(order).to_numpy(float))
    return np.column_stack(cols)


def _std(reg, F, p):
    """Standard deviations of the ``p`` predicted metrics (attribute units); NaN if unavailable."""
    try:
        return np.asarray(reg.predict_std(F), float).reshape(-1)[:p]
    except (AttributeError, ValueError, NotImplementedError):
        return np.full(p, np.nan)


class Proposer:
    """Sampler of ``v2-check-predictions``: fit on the v2 primary data, propose three designs."""

    def __init__(self, experiment, root: Path | None = None):
        self.experiment, self.root = experiment, root
        self.ranges, self.levels = _ranges_and_levels(experiment, root)
        self.primary = _path(experiment, "primary", root)

    def feasible_primary(self) -> pd.DataFrame:
        df = pd.read_csv(self.primary)
        attrs = list(ATTRIBUTE_NAMES)
        # dod_ok since the WP23 close-out: the depth-of-discharge failures left the training rows
        # through the eclipse reserve's positivity until the reserve left the metric set
        ok = df.settled & df.power_ok & df.momentum_ok & df.dod_ok & (df[attrs] > 0).all(axis=1)
        return df[ok].reset_index(drop=True)

    def draw(self, n: int, seed: int) -> pd.DataFrame:
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

        ranges, levels = self.ranges, self.levels
        fe = self.feasible_primary()
        Y = fe[list(METRICS)].to_numpy(float)
        pre = LogAffinePreconditioner(orientation=[-1] * len(METRICS), scaler="standard")
        tau = select_temperature(pre.fit_transform(Y), target_frac_above=0.10, bounds=(3, 1e3))
        ts = make_pipeline(
            LogAffinePreconditioner(orientation=[-1] * len(METRICS), scaler="standard"),
            HyperbolicTradeSpace(temperature=tau),
        )
        gp = GaussianProcessRegressor(
            kernel=ConstantKernel(1.0) * RBF(length_scale=np.ones(6)) + WhiteKernel(0.1),
            normalize_y=True,
            n_restarts_optimizer=2,
            random_state=0,
        )
        reg = TradeSpaceRegressor(gp, ts).fit(_features(fe, ranges, levels), Y)
        chart = reg.trade_space_.transform(Y)  # [Z | log V] of the data
        Z_data = chart[:, :-1]
        holes, scores = find_holes(Z_data, resolution=30, threshold=2.0)

        # Holes are candidates, not verdicts: take the most isolated (up to HOLES) whose best
        # configuration in the seeded pool is predicted within the reach of (Z_hole, 0), then n of
        # them separated by 1.5 median nearest-neighbour distances.
        nn = cKDTree(Z_data).query(Z_data, k=2)[0][:, 1]
        sep = 1.5 * float(np.median(nn))
        rng = np.random.default_rng(int(seed))
        pool = pd.DataFrame(
            {
                "panel_span_m": np.exp(rng.uniform(*np.log(ranges["panel_span_m"]), POOL)),
                "battery_wh": np.exp(rng.uniform(*np.log(ranges["battery_wh"]), POOL)),
                "Kp": np.exp(rng.uniform(*np.log(ranges["Kp"]), POOL)),
                "Kd": np.exp(rng.uniform(*np.log(ranges["Kd"]), POOL)),
                "wheel_class": rng.choice(levels["wheel_class"], POOL),
                "st_grade": rng.choice(levels["st_grade"], POOL),
            }
        )
        Zp, lvp = reg.predict_coordinates(_features(pool, ranges, levels))
        lvp = np.ravel(lvp)
        nearest = []  # per isolated hole: the index of the nearest pool design and its distance
        for h in holes[:HOLES]:
            dist = np.sqrt(((Zp - h) ** 2).sum(axis=1) + (2 * lvp) ** 2)
            i = int(np.argmin(dist))
            nearest.append((i, float(dist[i])))
        reach = float(np.quantile([d for _, d in nearest], REACH_QUANTILE))
        chosen, best_i, best_d, chosen_scores = [], [], [], []
        for h, sc, (i, d) in zip(holes[:HOLES], scores[:HOLES], nearest, strict=True):
            if d > reach or any(np.linalg.norm(h - c) <= sep for c in chosen):
                continue
            chosen.append(h)
            best_i.append(i)
            best_d.append(d)
            chosen_scores.append(float(sc))
            if len(chosen) == n:
                break
        print(
            f"reach {reach:.4f} (quantile {REACH_QUANTILE} of the nearest predicted distances of"
            f" the {len(nearest)} most isolated holes); {len(chosen)} of {n} proposals"
        )

        rows = []
        for k, h in enumerate(chosen):
            cfg = pool.iloc[[best_i[k]]]
            F = _features(cfg, ranges, levels)
            z, lv = reg.predict_coordinates(F)
            sd = _std(reg, F, len(METRICS))
            row = {"role": "proposal", "design_id": 1004 + k, "name": f"proposal_{k + 1}"}
            row.update(cfg.iloc[0].to_dict())
            for j in range(Z_data.shape[1]):
                row[f"target_z{j + 1}"] = float(h[j])
            for j in range(Z_data.shape[1]):
                row[f"pred_z{j + 1}"] = float(z[0, j])
            row["pred_log_v"] = float(np.ravel(lv)[0])
            for name, v in zip(METRICS, sd, strict=True):
                row[f"pred_std_{name}"] = float(v)
            row["hole_score"] = chosen_scores[k]
            row["distance_to_target"] = best_d[k]
            row["tau"] = float(tau)
            row["band"] = 1.0 / float(tau)
            row["n_train"] = len(fe)
            rows.append(row)
        return pd.DataFrame(rows)


class Passthrough:
    """The oracle of ``v2-check-predictions``: nothing is measured; the proposals are the output."""

    config_names = CONFIG_NAMES
    attribute_names: tuple[str, ...] = ()
    flag_names: tuple[str, ...] = ()

    def __call__(self, configuration):
        return {}

    def evaluate(self, designs: pd.DataFrame) -> pd.DataFrame:
        return designs.sort_values("design_id").reset_index(drop=True)


class Checks:
    """Sampler of ``v2-check-designs``: the declared candidates and the committed proposals."""

    def __init__(self, experiment, root: Path | None = None):
        self.experiment = experiment
        self.predictions = _path(experiment, "predictions", root)

    def draw(self, n: int, seed: int) -> pd.DataFrame:
        rows = [
            {"role": "candidate", "design_id": 1001 + k, **dict(c)}
            for k, c in enumerate(self.experiment.inputs["candidates"])
        ]
        for _, r in pd.read_csv(self.predictions).iterrows():
            rows.append(
                {"role": "proposal", "design_id": int(r.design_id), "name": r["name"]}
                | {c: r[c] for c in CONFIG_NAMES}
            )
        out = pd.DataFrame(rows)
        out["seed"] = int(seed)
        if len(out) != n:
            raise ValueError(f"{self.experiment.id}: {len(out)} check designs, count says {n}")
        return out


class CheckOracle:
    """The cubesat oracle with the frozen check-design layout (no scenario columns)."""

    def __init__(self, inner):
        self.inner = inner
        self.config_names = inner.config_names
        self.attribute_names = inner.attribute_names
        self.flag_names = inner.flag_names
        self.runtime_info = getattr(inner, "runtime_info", None)

    def __call__(self, configuration):
        return self.inner(configuration)

    def evaluate(self, designs: pd.DataFrame) -> pd.DataFrame:
        table = self.inner.evaluate(designs).drop(columns=list(SCENARIO_COLUMNS))
        lead = [*LEAD, *FLAGS]
        rest = [c for c in table.columns if c not in lead]
        return table[[*lead, *rest]]


# -- the factories definitions.py registers ------------------------------------------------------
def build_proposer(experiment) -> Proposer:
    return Proposer(experiment)


def build_checks(experiment) -> Checks:
    return Checks(experiment)


def build_passthrough(experiment) -> Passthrough:
    return Passthrough()


def build_check_oracle(experiment) -> CheckOracle:
    return CheckOracle(build(experiment))
