"""Generate the seeded ADCS trade-space dataset (WP4).

Usage (from the repository root)::

    uv run python examples/adcs/generate_dataset.py --n 1000 --seed 0 --workers 8 --force

Skips generation when the output exists unless ``--force``. Rows are sorted by ``design_id`` and
floats are written with ``%.9g``. ``--fast`` uses the coarse test settings (``FAST_SIM``).

WP4b adds the illustrative cubesat model (SysML configuration space read through ``opensysml``)::

    uv run python examples/adcs/generate_dataset.py --model cubesat --n 1000 --seed 0 --force

``--model adcs`` (default) is the unchanged WP4 behaviour. ``--model cubesat`` writes
``data/adcs_designs_cubesat.csv`` by default; ``--slew-deg`` and ``--t-end`` set the scenario
(defaults 10 deg / 900 s for adcs, the values of ``cubesat_model`` for cubesat: 30 deg / 600 s).
``--gain-box aggressive`` (amendment 5) samples Kp, Kd from the model's ``aggressiveGains`` part
and writes ``data/adcs_designs_cubesat_gains.csv``; the default ``baseline`` is unchanged.
Each cubesat worker process opens its own ``opensysml`` connection. The cubesat columns are those
returned by ``CubesatModel.measure`` (including ``slew_time_s`` and ``slew_time_05deg_s``).
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
CUBESAT_OUT = pathlib.Path(__file__).resolve().parent / "data" / "adcs_designs_cubesat.csv"
GAINS_OUT = pathlib.Path(__file__).resolve().parent / "data" / "adcs_designs_cubesat_gains.csv"
CUBESAT_CHUNK = 10
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


def _worker_init():
    """Each worker opens its own opensysml connection (never one inherited across a fork)."""
    import cubesat_model as cm

    cm._CONNECTION = None
    cm._DEFAULT = None


def _evaluate_chunk(args):
    rows, kwargs = args
    import cubesat_model as cm

    return cm.load_model().evaluate_designs(pd.DataFrame(rows), **kwargs)


def generate_cubesat(
    n: int,
    seed: int,
    workers: int = 1,
    fast: bool = False,
    slew_deg: float | None = None,
    t_end: float | None = None,
    gain_box: str = "baseline",
) -> pd.DataFrame:
    """Sample ``n`` cubesat designs from the SysML model and measure them.

    Designs are measured in chunks (one model load per chunk); with ``workers`` > 1 a spawned
    process pool is used and each worker holds its own client connection. The scenario is
    recorded in the ``slew_deg``, ``t_end_s`` and ``max_step_s`` columns.
    """
    import cubesat_model as cm

    kwargs = {
        "slew_deg": cm.SLEW_DEG if slew_deg is None else slew_deg,
        "t_end": cm.T_END if t_end is None else t_end,
        "max_step": cm.MAX_STEP,
    }
    if fast:
        kwargs["max_step"] = FAST_SIM["max_step"]
    designs = cm.load_model(gain_box=gain_box).sample_designs(n, seed)
    chunks = [
        ([r.to_dict() for _, r in designs.iloc[i : i + CUBESAT_CHUNK].iterrows()], kwargs)
        for i in range(0, n, CUBESAT_CHUNK)
    ]
    if workers > 1:
        with mp.get_context("spawn").Pool(workers, initializer=_worker_init) as pool:
            parts = pool.map(_evaluate_chunk, chunks, chunksize=1)
    else:
        parts = [_evaluate_chunk(c) for c in chunks]
    out = pd.concat(parts, ignore_index=True)
    out["slew_deg"] = kwargs["slew_deg"]
    out["t_end_s"] = kwargs["t_end"]
    out["max_step_s"] = kwargs["max_step"]
    return out.sort_values("design_id").reset_index(drop=True)


def generate(
    n: int,
    seed: int,
    workers: int = 1,
    fast: bool = False,
    model: str = "adcs",
    slew_deg: float | None = None,
    t_end: float | None = None,
    gain_box: str = "baseline",
) -> pd.DataFrame:
    """Sample ``n`` designs and evaluate them (in a process pool when ``workers`` > 1)."""
    if model == "cubesat":
        return generate_cubesat(n, seed, workers, fast, slew_deg, t_end, gain_box)
    designs = sample_designs(n, seed)
    kwargs = dict(FAST_SIM) if fast else {}
    if t_end is not None:
        kwargs["t_end"] = t_end
    if slew_deg is not None:
        kwargs["initial_error_deg"] = slew_deg
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
    p.add_argument("--model", choices=["adcs", "cubesat"], default="adcs")
    p.add_argument(
        "--slew-deg", type=float, default=None, help="slew angle (default 10 / cubesat 30)"
    )
    p.add_argument(
        "--t-end", type=float, default=None, help="horizon in s (default 900 / cubesat 600)"
    )
    p.add_argument(
        "--gain-box",
        choices=["baseline", "aggressive"],
        default="baseline",
        help="cubesat Kp, Kd ranges read from the SysML model (aggressive: amendment 5, lever i)",
    )
    p.add_argument("--out", type=pathlib.Path, default=None)
    p.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    p.add_argument("--force", action="store_true", help="overwrite an existing output file")
    p.add_argument("--fast", action="store_true", help="coarse settings (tests only)")
    a = p.parse_args(argv)
    if a.out is None:
        a.out = CUBESAT_OUT if a.model == "cubesat" else DEFAULT_OUT
        if a.model == "cubesat" and a.gain_box == "aggressive":
            a.out = GAINS_OUT
    if a.out.exists() and not a.force:
        print(f"{a.out} exists; skipping (use --force to regenerate)")
        return 0
    if a.gain_box != "baseline" and a.model != "cubesat":
        p.error("--gain-box applies to --model cubesat only")
    df = generate(a.n, a.seed, a.workers, a.fast, a.model, a.slew_deg, a.t_end, a.gain_box)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.out, index=False, float_format="%.9g")
    print(f"wrote {len(df)} designs to {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
