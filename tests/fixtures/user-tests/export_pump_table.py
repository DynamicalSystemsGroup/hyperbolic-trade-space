"""Export the pump trade table from ``pump_trade.sysml``.

Draws designs (impeller diameter, shaft speed, blade width ratio) log-uniformly in the ranges
stated in the model, has the model evaluate its four calculations (flow, head, shaft power, mass)
for each, and writes one row per design. The numbers come from the model's calcs through the
``opensysml`` client; none is copied here. Run from the repository root::

    uv run python tests/fixtures/user-tests/export_pump_table.py [OUT.csv]
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MODEL = HERE / "pump_trade.sysml"
TABLE = HERE / "pump_table.csv"
RANGES = {"diameter_m": (0.08, 0.35), "speed_rpm": (900.0, 3600.0), "width_ratio": (0.05, 0.30)}
CALCS = {"flow_lps": "Flow", "head_m": "Head", "power_kw": "ShaftPower", "mass_kg": "Mass"}
N_DESIGNS = 200
SEED = 7


def designs(n: int = N_DESIGNS, seed: int = SEED) -> list[tuple[float, float, float]]:
    """Log-uniform draws in the model's ranges, rounded to the precision the table keeps."""
    rng = np.random.default_rng(seed)
    cols = [
        np.round(np.exp(rng.uniform(np.log(lo), np.log(hi), n)), 4) for lo, hi in RANGES.values()
    ]
    return list(zip(*(c.tolist() for c in cols), strict=True))


def export_rows(model_text: str, rows=None) -> list[dict]:
    """Evaluate every calc of the model at every design; one dict per design."""
    import opensysml

    connection = opensysml.connect()
    try:
        model = connection.load_from_content(model_text, strict=True)
        out = []
        for i, (d, n, w) in enumerate(rows if rows is not None else designs()):
            row = {"design_id": i, "diameter_m": d, "speed_rpm": n, "width_ratio": w}
            for column, calc in CALCS.items():
                value = model.eval(f"PumpTrade::{calc}({d!r}, {n!r}, {w!r})")
                value = value[0] if isinstance(value, list) else value
                row[column] = round(float(value), 4)
            out.append(row)
        return out
    finally:
        connection.close()


def write_csv(rows: list[dict], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else TABLE
    write_csv(export_rows(MODEL.read_text(encoding="utf-8")), out)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
