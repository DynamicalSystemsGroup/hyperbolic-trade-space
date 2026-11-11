"""The cost-limit ladders of WP30 (D-6): the share of the feasible designs each limit admits.

For each regime and each fleet size n, the unit cost (build and launch, per satellite) and the
fleet cost (build and launch, whole fleet) of every feasible design are priced at that n, and the
ladder is the share of the feasible designs at or under each candidate limit. The supervisor reads
the two limits from these rows (``WP30-decisions.md``, OD3 (a)); this script prints them and, with
``--write``, writes ``work-packages/WP30-rounds/cost-ladders.md``.

Prices are the spike's table (``spike-D-cubesat-economics/economics.py``, which the model's
``cubesat.sysml`` states: relative difference below 1e-12). A design's cost depends on its
configuration, its fleet size and its total mass only, so the ladders are priced from the data's
design columns at every n; when the data carry ``fleet_size`` and ``unit_cost_usd`` (the
regenerated v2 data), the repricing is checked against them at each design's own fleet size and
the script exits 2 on a difference above 1e-9. ``--no-launch`` prices the build only, which
reproduces the spike's ``admit-shares.txt``.

    uv run python scripts/wp30_cost_ladders.py [--data DIR] [--write] [--no-launch]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPIKE = ROOT / "work-packages/WP23-rounds/spikes/spike-D-cubesat-economics/economics.py"
OUT = ROOT / "work-packages/WP30-rounds/cost-ladders.md"
REGIMES = {  # label: file (the ledger's v2-baseline and v2-primary outputs)
    "baseline": "adcs_designs_cubesat.csv",
    "primary": "adcs_designs_cubesat_gains.csv",
}
FLAGS = ("settled", "momentum_ok", "power_ok", "dod_ok")
FLEET_SIZES = (1, 3, 10, 30)
ALL_SIZES = tuple(range(1, 31))  # the sampler draws n uniform on the integers 1 to 30
UNIT_LIMITS = tuple(range(200_000, 500_001, 50_000))
FLEET_LIMITS = (500_000, 1_000_000, 2_000_000, 3_000_000, 4_000_000, 6_000_000, 8_000_000)
CHECK_TOLERANCE = 1e-9


def load_prices(path: Path = SPIKE) -> dict:
    """The spike's price functions, run without its report (the file ends in ``main()``)."""
    text = path.read_text().rstrip()
    if not text.endswith("main()"):
        raise ValueError(f"{path} no longer ends in main(); read the table another way")
    namespace = {"__file__": str(path), "__name__": "economics"}
    exec(compile(text[: -len("main()")], str(path), "exec"), namespace)
    return namespace


def feasible_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """The designs for which every feasibility flag holds."""
    flags = frame[list(FLAGS)].astype(str).eq("True").all(axis=1)
    return frame[flags].reset_index(drop=True)


def price(econ: dict, frame: pd.DataFrame, n: int | np.ndarray, launch: bool = True):
    """(fleet cost, unit cost) of each design in ``frame`` at fleet size ``n`` (scalar or array)."""
    n = np.broadcast_to(np.asarray(n, dtype=float), (len(frame),))
    fleet = np.empty(len(frame))
    for i, r in enumerate(frame.itertuples(index=False)):
        build = econ["fleet_build"](r.wheel_class, r.st_grade, r.panel_span_m, r.battery_wh, n[i])
        fleet[i] = build + (econ["LAUNCH_RATE"] * r.total_mass_kg * n[i] if launch else 0.0)
    return fleet, fleet / n


def check_against_data(econ: dict, frame: pd.DataFrame, launch: bool = True) -> float | None:
    """Largest relative difference between the repricing and the data's own cost columns at each
    design's own fleet size; None when the data have no cost columns (before the regeneration)."""
    if not {"fleet_size", "unit_cost_usd", "fleet_cost_usd"} <= set(frame.columns):
        return None
    fleet, unit = price(econ, frame, frame["fleet_size"].to_numpy(), launch)
    rel_f = np.abs(fleet / frame["fleet_cost_usd"].to_numpy() - 1)
    rel_u = np.abs(unit / frame["unit_cost_usd"].to_numpy() - 1)
    return float(max(rel_f.max(), rel_u.max()))


def shares(values: np.ndarray, limits) -> list[float]:
    """Percent of ``values`` at or under each limit."""
    return [100.0 * float(np.mean(values <= x)) for x in limits]


def ladders(econ: dict, feasible: pd.DataFrame, launch: bool = True) -> dict:
    """Unit and fleet ladders: ``{"unit": {n or "free": [percent per limit]}, "fleet": ...}``.

    ``"free"`` averages over every n from 1 to 30 (the sampler's uniform draw)."""
    out = {"unit": {}, "fleet": {}}
    per_n = {n: price(econ, feasible, n, launch) for n in ALL_SIZES}
    for key, idx, limits in (("fleet", 0, FLEET_LIMITS), ("unit", 1, UNIT_LIMITS)):
        rows = {n: shares(per_n[n][idx], limits) for n in ALL_SIZES}
        out[key] = {n: rows[n] for n in FLEET_SIZES}
        out[key]["free"] = list(np.mean([rows[n] for n in ALL_SIZES], axis=0))
    return out


def table(title: str, limits, rows: dict, note: str) -> str:
    head = ["limit (USD)", *(f"n = {n}" for n in FLEET_SIZES), "n free (1 to 30)"]
    lines = [f"{title}", "", note, "", "| " + " | ".join(head) + " |"]
    lines.append("|" + "---|" * len(head))
    for j, x in enumerate(limits):
        cells = [f"{rows[n][j]:.1f}" for n in (*FLEET_SIZES, "free")]
        lines.append(f"| {x:,} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def report(results: dict, launch: bool) -> str:
    cost = "build and launch" if launch else "build only (no launch)"
    parts = [
        "# WP30 cost-limit ladders (D-6)",
        "",
        f"Share of the feasible designs (percent) at or under each candidate limit; cost is {cost}."
        " Generated by `scripts/wp30_cost_ladders.py`; the supervisor picks one rung per limit.",
    ]
    for label, (count, ladder, check) in results.items():
        parts += ["", f"## Regime: {label} ({count} feasible designs)", ""]
        if check is None:
            parts.append("Priced from the design columns; the data carry no cost columns to check.")
        else:
            parts.append(
                f"Repricing checked against the data's cost columns: max relative {check:.1e}."
            )
        parts += [
            "",
            table(
                "### Unit cost limit (USD per satellite, read at the design's own n)",
                UNIT_LIMITS,
                ladder["unit"],
                "Columns are the fleet size every feasible design is priced at.",
            ),
            "",
            table(
                "### Fleet cost limit (USD, whole fleet)",
                FLEET_LIMITS,
                ladder["fleet"],
                "Columns are the fleet size every feasible design is priced at.",
            ),
        ]
    return "\n".join(parts) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", type=Path, default=ROOT / "examples/adcs/data/v2")
    ap.add_argument("--write", action="store_true", help=f"write {OUT.relative_to(ROOT)}")
    ap.add_argument("--no-launch", action="store_true", help="price the build only (the spike)")
    a = ap.parse_args(argv)
    launch = not a.no_launch
    econ = load_prices()
    results, bad = {}, False
    for label, file in REGIMES.items():
        frame = pd.read_csv(a.data / file)
        check = check_against_data(econ, frame, launch)
        if check is not None and check > CHECK_TOLERANCE:
            print(f"{label}: repricing differs from the data's cost columns by {check:.2e}")
            bad = True
        feasible = feasible_rows(frame)
        results[label] = (len(feasible), ladders(econ, feasible, launch), check)
    text = report(results, launch)
    print(text)
    if bad:
        return 2
    if a.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(text)
        print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
