# The K = 1 fit at each temperature of the sweep, both regimes

The sweep behind the fit temperature of each regime; the paper's figure of the sweep draws the primary regime. The table is `generate_results.temperature_selection`, read from the data of record and written by `uv run python paper/generate_supplement.py`.

Each row is the K = 1 fit at the temperature tau. The columns give the fraction of designs above V = 1, the effective sample size, the number of metrics with an exponent above 0.001, and the largest exponent with its metric. The fit temperature is chosen so that the fraction above V = 1 reaches the target 0.10, the rule of Section 5.

Dataset cubesat-primary:

| tau | frac_above | n_eff | metrics with w>1e-3 | largest w | largest at |
|---|---|---|---|---|---|
| 3 | 0.4527 | 1984 | 8 | 0.2252 | unit cost |
| 5.087 | 0.4231 | 1745 | 8 | 0.2259 | unit cost |
| 8.626 | 0.3627 | 1256 | 8 | 0.2268 | unit cost |
| 14.63 | 0.2727 | 613.2 | 8 | 0.228 | unit cost |
| 24.8 | 0.1809 | 202.6 | 8 | 0.2339 | unit cost |
| 42.06 | 0.09653 | 72.6 | 8 | 0.2576 | unit cost |
| 71.32 | 0.0492 | 33.74 | 7 | 0.2755 | unit cost |
| 120.9 | 0.02812 | 16.98 | 7 | 0.2741 | unit cost |
| 205.1 | 0.01687 | 10.15 | 7 | 0.273 | unit cost |
| 347.8 | 0.008903 | 7.44 | 7 | 0.2726 | unit cost |
| 589.7 | 0.007029 | 6.415 | 7 | 0.273 | unit cost |
| 1000 | 0.005155 | 6.086 | 7 | 0.2735 | unit cost |
| inf | 0 | 3.835 | 7 | 0.274 | unit cost |

Dataset cubesat-stock:

| tau | frac_above | n_eff | metrics with w>1e-3 | largest w | largest at |
|---|---|---|---|---|---|
| 3 | 0.4921 | 2193 | 9 | 0.2166 | total mass |
| 5.087 | 0.4577 | 1957 | 9 | 0.2073 | total mass |
| 8.626 | 0.4017 | 1490 | 9 | 0.1915 | total mass |
| 14.63 | 0.3176 | 816.6 | 9 | 0.1756 | momentum headroom |
| 24.8 | 0.2157 | 255.8 | 9 | 0.1798 | available power |
| 42.06 | 0.1163 | 58.38 | 9 | 0.1901 | available power |
| 71.32 | 0.06072 | 21.39 | 9 | 0.202 | momentum headroom |
| 120.9 | 0.03567 | 12.07 | 9 | 0.2237 | momentum headroom |
| 205.1 | 0.01953 | 7.497 | 8 | 0.229 | momentum headroom |
| 347.8 | 0.009342 | 4.984 | 8 | 0.2304 | momentum headroom |
| 589.7 | 0.005945 | 4.261 | 8 | 0.2325 | momentum headroom |
| 1000 | 0.004671 | 4.08 | 8 | 0.2335 | momentum headroom |
| inf | 0 | 3.916 | 8 | 0.2352 | momentum headroom |
