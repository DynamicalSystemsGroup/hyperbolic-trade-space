"""Spike C: the three requirements that read no traded metric, read on the data of record.

Run from the repository root:

    uv run python work-packages/WP23-rounds/spikes/spike-C-requirements-no-traded-metric/analysis.py

Read-only: it reads ``examples/adcs/data/v2/`` through ``examples/adcs/case.py`` and writes nothing.
Each requirement's quantity is rebuilt from the dataset's columns with the model's constants
(``cubesat.sysml``): the wheel classes' momentum capacities (part defs SmallWheel, MediumWheel,
LargeWheel), the housekeeping load and the battery's discharge rate (part ``environment``).

1. PowerRequirement            c.availablePower > 0 W              column available_power_w
2. MomentumRequirement         peakMomentum <= c.momentumCapacity  peak_momentum_nms, capacity
3. BatteryPeakPowerRequirement EclipsePeakLoad <= BatteryPeakPower 12 W + peak_slew_power_w against
                                                                   1.0 /h * battery_wh

Each slack is stated two ways, larger is better: the ratio (limit over load, dimensionless, above 1
when the requirement holds) and the difference (limit minus load, in the requirement's unit).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "examples" / "adcs"))

import case  # noqa: E402

# the model's constants (cubesat.sysml): wheel maxMomentum, environment.housekeepingLoad,
# environment.batteryDischargeRate
CAPACITY_NMS = {"small": 0.010, "medium": 0.030, "large": 0.100}
HOUSEKEEPING_W = 12.0
DISCHARGE_RATE_PER_H = 1.0
NEAR_DUPLICATE = 0.95

CANDIDATES = {
    # name: (requirement, unit, function of the raw table)
    "available power": (
        "PowerRequirement",
        "W",
        lambda d: d["available_power_w"],
    ),
    "momentum headroom ratio": (
        "MomentumRequirement",
        "1",
        lambda d: d["wheel_class"].map(CAPACITY_NMS) / d["peak_momentum_nms"],
    ),
    "momentum headroom": (
        "MomentumRequirement",
        "N.m.s",
        lambda d: d["wheel_class"].map(CAPACITY_NMS) - d["peak_momentum_nms"],
    ),
    "battery peak power ratio": (
        "BatteryPeakPowerRequirement",
        "1",
        lambda d: (
            DISCHARGE_RATE_PER_H * d["battery_wh"] / (HOUSEKEEPING_W + d["peak_slew_power_w"])
        ),
    ),
    "battery peak power headroom": (
        "BatteryPeakPowerRequirement",
        "W",
        lambda d: (
            DISCHARGE_RATE_PER_H * d["battery_wh"] - (HOUSEKEEPING_W + d["peak_slew_power_w"])
        ),
    ),
}


def oriented(df, spec):
    """The eight traded attributes oriented larger-is-better (sign times the log), by short name."""
    return pd.DataFrame(
        {spec.short[a]: spec.orientation[a] * np.log(df[a].to_numpy()) for a in spec.attributes},
        index=df.index,
    )


def section(title):
    print(f"\n## {title}\n")


def main():
    spec = case.CUBESAT
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 30)
    for regime in spec.regimes:
        study = case.load_study(regime)
        raw, feas = study.raw, study.feasible
        print(f"\n# regime {regime}: {len(raw)} designs, {len(feas)} feasible")

        section("1. Each requirement over all designs (does it ever fail?)")
        rows = []
        for name, (req, unit, f) in CANDIDATES.items():
            q = f(raw)
            limit = 1.0 if "ratio" in name else 0.0
            rows.append(
                {
                    "quantity": name,
                    "requirement": req,
                    "unit": unit,
                    "fails (all designs)": int((q <= limit).sum()),
                    "min (all)": q.min(),
                    "max (all)": q.max(),
                }
            )
        print(pd.DataFrame(rows).to_string(index=False))
        print(
            "flag columns over all designs: power_ok false",
            int((~raw["power_ok"].astype(bool)).sum()),
            "; momentum_ok false",
            int((~raw["momentum_ok"].astype(bool)).sum()),
            "(battery peak power has no flag column)",
        )

        section("2. Spread over the feasible designs (the set the fit reads)")
        rows = []
        for name, (_req, unit, f) in CANDIDATES.items():
            q = f(feas).to_numpy(dtype=float)
            rows.append(
                {
                    "quantity": name,
                    "unit": unit,
                    "min": q.min(),
                    "max": q.max(),
                    "max/min": q.max() / q.min() if q.min() > 0 else np.nan,
                    "CV": q.std() / q.mean(),
                    "distinct": len(np.unique(np.round(q, 12))),
                    "non-positive": int((q <= 0).sum()),
                }
            )
        for a in spec.attributes:  # the traded metrics' spread, for comparison
            q = feas[a].to_numpy(dtype=float)
            rows.append(
                {
                    "quantity": f"[traded] {spec.short[a]}",
                    "unit": spec.units[a],
                    "min": q.min(),
                    "max": q.max(),
                    "max/min": q.max() / q.min(),
                    "CV": q.std() / q.mean(),
                    "distinct": len(np.unique(np.round(q, 12))),
                    "non-positive": int((q <= 0).sum()),
                }
            )
        print(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:.4g}"))

        section("3. Spearman of each candidate (larger is better) with the eight traded metrics")
        lm = oriented(feas, spec)
        C = pd.DataFrame({n: f(feas).astype(float) for n, (_, _, f) in CANDIDATES.items()})
        rho = pd.concat([C, lm], axis=1).rank().corr()
        table = rho.loc[list(CANDIDATES), list(lm.columns)]
        print(table.to_string(float_format=lambda x: f"{x:+.3f}"))
        print(f"\nnear-duplicates (|Spearman| >= {NEAR_DUPLICATE}):")
        hits = [
            (c, m, table.loc[c, m])
            for c in table.index
            for m in table.columns
            if abs(table.loc[c, m]) >= NEAR_DUPLICATE
        ]
        for c, m, r in hits or [("none", "", np.nan)]:
            print(f"  {c} ~ {m}: {r:+.4f}")
        print("\nstrongest traded metric per candidate:")
        for c in table.index:
            m = table.loc[c].abs().idxmax()
            print(f"  {c}: {m} {table.loc[c, m]:+.3f}")
        print("\nSpearman among the candidates:")
        print(
            rho.loc[list(CANDIDATES), list(CANDIDATES)].to_string(
                float_format=lambda x: f"{x:+.3f}"
            )
        )
        print(
            "\nfor reference, the paper's named near pair: power margin ~ energy balance "
            f"{rho.loc['power margin', 'energy balance']:+.4f}"
        )

        section("4. What explains each candidate (Spearman within the design variables)")
        for name, (_, _, f) in CANDIDATES.items():
            q = f(feas).astype(float)
            parts = []
            for v in ("panel_span_m", "battery_wh", "Kp", "Kd"):
                parts.append(f"{v} {pd.Series(q).corr(feas[v], method='spearman'):+.2f}")
            by_cell = feas.assign(q=q).groupby(["wheel_class", "st_grade"])["q"].median()
            print(f"{name}: " + ", ".join(parts))
            print(
                "   median by wheel class:",
                feas.assign(q=q).groupby("wheel_class")["q"].median().round(4).to_dict(),
            )
            print(
                "   median by tracker grade:",
                feas.assign(q=q).groupby("st_grade")["q"].median().round(4).to_dict(),
            )
            del by_cell

        section("5. The K = 1 fit with each candidate added (ratio forms), same rule as the case")
        base = case.fit_study(study, K=1)
        ex = case.exponent_table(study, base).set_index("metric")["exponent w"]
        out = {"eight (of record)": ex}
        adds = {
            "+ available power": ["available power"],
            "+ momentum headroom ratio": ["momentum headroom ratio"],
            "+ battery peak power ratio": ["battery peak power ratio"],
            "+ all three": [
                "available power",
                "momentum headroom ratio",
                "battery peak power ratio",
            ],
        }
        taus = {"eight (of record)": base.tau}
        for label, names in adds.items():
            cols = {}
            for n in names:
                col = "cand_" + n.replace(" ", "_")
                cols[n] = col
            raw2 = raw.copy()
            for n, col in cols.items():
                raw2[col] = CANDIDATES[n][2](raw2).astype(float)
            attrs = tuple(spec.attributes) + tuple(cols.values())
            spec2 = case.replace(
                spec,
                attributes=attrs,
                short={**spec.short, **{c: n for n, c in cols.items()}},
                units={**spec.units, **{c: CANDIDATES[n][1] for n, c in cols.items()}},
                orientation={**spec.orientation, **{c: +1 for c in cols.values()}},
                subsystems={**spec.subsystems, **{c: "power and energy" for c in cols.values()}},
            )
            feas2 = raw2[case.feasible_mask(raw2, spec2)].reset_index(drop=True)
            assert len(feas2) == len(feas), "a candidate changed the feasible set"
            cond, M = case._condition(feas2, attrs, spec2)
            st2 = case.Study(spec2, regime, raw2, feas2, attrs, M, cond)
            fit = case.fit_study(st2, K=1)
            taus[label] = fit.tau
            out[label] = case.exponent_table(st2, fit).set_index("metric")["exponent w"]
        tab = pd.DataFrame(out)
        print(tab.to_string(float_format=lambda x: f"{x:.3f}", na_rep="-"))
        print("tau:", {k: round(v, 3) for k, v in taus.items()})


if __name__ == "__main__":
    main()
