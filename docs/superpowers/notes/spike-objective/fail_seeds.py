"""Fail seeds of the five-restart selection table (bench_c.py printed them empty: `d.select` is a
DataFrame method, the column must be indexed as d["select"]). uv run python <folder>/fail_seeds.py"""

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
mg = pd.read_csv(HERE / "recovery_restarts.csv")
mg["pass"] = (mg.err < 0.05) & (mg.right >= 0.9)
for tau in [np.inf, 50.0]:
    d = mg[mg.tau == tau]
    print(f"tau = {tau}")
    for step in ["B", "D"]:
        for sel in ["O0", "O1", "T", "T0", "O2", "O3", "O4", "O5"]:
            dd = d[(d.step == step) & (d["select"] == sel)]
            fails = dd[~dd["pass"]]
            print(
                f"  {step} sel:{sel}: pass {int(dd['pass'].sum())}/20, fail seeds {sorted(fails.seed.tolist())}, "
                f"err on 1,3,8,16: {[round(float(dd[dd.seed == s].err.iloc[0]), 3) for s in [1, 3, 8, 16]]}"
            )
