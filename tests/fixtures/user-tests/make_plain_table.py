"""Write ``plain_table.csv``: a synthetic materials-style table with no model behind it.

The rows come from the package's ``make_frontier_data`` (four larger-is-better metrics around a
planted frontier) and are then turned into raw attributes the way measured data arrives: each
column gets its own unit scale, and two of them (``weight_kg``, ``cost_usd``) are smaller-is-better,
so the table needs conditioning before a fit. A ``sample`` id and a ``batch`` label are columns
that are not attributes. Run from the repository root::

    uv run python tests/fixtures/user-tests/make_plain_table.py [OUT.csv]
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from hyperbolic_trade_space import make_frontier_data

HERE = Path(__file__).resolve().parent
TABLE = HERE / "plain_table.csv"
EXPONENTS = [0.5, 0.5, 0.0, 0.0]
N_SAMPLES = 250


def build() -> pd.DataFrame:
    X, _ = make_frontier_data(N_SAMPLES, 4, exponents=EXPONENTS, noise=0.02, random_state=3)
    rng = np.random.default_rng(3)
    return pd.DataFrame(
        {
            "sample": np.arange(N_SAMPLES),
            "batch": rng.choice(["A", "B", "C"], N_SAMPLES),
            "strength_mpa": np.round(120.0 * X[:, 0], 4),
            "weight_kg": np.round(40.0 / X[:, 1], 4),
            "stiffness_gpa": np.round(30.0 * X[:, 2], 4),
            "cost_usd": np.round(900.0 / X[:, 3], 4),
        }
    )


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else TABLE
    build().to_csv(out, index=False, lineterminator="\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
