"""Aggregate the planted-table sweeps: per K, the medians and the recovery rate (WP31 spike).

uv run python work-packages/WP31-readout/aggregate.py > planted-summary.txt
"""

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
for k0 in (2, 3):
    d = pd.concat([pd.read_csv(p) for p in sorted(HERE.glob(f"planted-K{k0}?.csv"))])
    d["all_recovered"] = d.recovered_planted == d.n_planted
    d["certified"] = d.status.isin(["certified", "not_applicable"])
    g = d.groupby("K").agg(
        tables=("table", "nunique"),
        slack=("mean_slack", "median"),
        min_share=("min_term_share", "median"),
        min_row_share=("min_row_share", "median"),
        splinter=("splinter", "median"),
        splinter_max=("splinter", "max"),
        planted_found=("recovered_planted", "mean"),
        all_found=("all_recovered", "mean"),
        spurious=("spurious", "mean"),
        cond=("min_conditioning", "median"),
        radius=("radius", "median"),
        certified=("certified", "mean"),
    )
    print(f"planted K0 = {k0}, 400 rows, 4 metrics, tau 50; medians over tables\n")
    print(g.to_string(float_format=lambda v: f"{v:.4g}"), "\n")
