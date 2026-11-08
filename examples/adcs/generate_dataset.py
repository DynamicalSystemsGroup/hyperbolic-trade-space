"""Generate the seeded ADCS trade-space dataset (WP4).

Usage (from the repository root)::

    uv run python examples/adcs/generate_dataset.py --n 1000 --seed 0 --workers 8 --force

Skips generation when the output exists unless ``--force``. Rows are sorted by ``design_id`` and
floats are written with ``%.9g``. ``--fast`` uses the coarse test settings (``FAST_SIM``).
"""

from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from design_space import FAST_SIM, evaluate_design, sample_designs

DEFAULT_OUT = pathlib.Path(__file__).resolve().parent / "data" / "adcs_designs.csv"
COLUMNS = [
    "design_id",
    "seed",
    "wheel_class",
    "st_grade",
    "Kp",
    "Kd",
    "panel_mass_kg",
    "antenna_mass_kg",
    "settling_time_s",
    "pointing_error_deg",
    "adcs_mass_kg",
    "control_effort",
    "settled",
    "momentum_ok",
    "torque_saturated_frac",
    "peak_momentum_nms",
]


def _evaluate(args):
    row, kwargs = args
    return evaluate_design(row, **kwargs)


def generate(n: int, seed: int, workers: int = 1, fast: bool = False) -> pd.DataFrame:
    """Sample ``n`` designs and evaluate them (in a process pool when ``workers`` > 1)."""
    designs = sample_designs(n, seed)
    kwargs = dict(FAST_SIM) if fast else {}
    jobs = [(r.to_dict(), kwargs) for _, r in designs.iterrows()]
    if workers > 1:
        with mp.Pool(workers) as pool:
            results = pool.map(_evaluate, jobs, chunksize=4)
    else:
        results = [_evaluate(j) for j in jobs]
    out = pd.concat([designs, pd.DataFrame(results)], axis=1)
    return out.sort_values("design_id")[COLUMNS].reset_index(drop=True)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--n", type=int, default=1000)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT)
    p.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    p.add_argument("--force", action="store_true", help="overwrite an existing output file")
    p.add_argument("--fast", action="store_true", help="coarse settings (tests only)")
    a = p.parse_args(argv)
    if a.out.exists() and not a.force:
        print(f"{a.out} exists; skipping (use --force to regenerate)")
        return 0
    df = generate(a.n, a.seed, a.workers, a.fast)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.out, index=False, float_format="%.9g")
    print(f"wrote {len(df)} designs to {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
