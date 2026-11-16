# WP72 wheat: results

3753 plot-years of `examples/wheat/derived/grain_straw.csv`; metrics grain and straw in t/ha, logged, no scaler. `share: X` is the within-group share of the variance of X; the shuffled-label null is the median `within_share` over 20 random permutations of the group labels.

| grouping | groups (>= 2 rows) | rows used | w (grain, straw) | within_share | shuffled-label null | flatness | within sd log V | within sd trade | share: log biomass | share: log grain | share: log(grain/straw) | PCA within (simplex) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| none (one group) | 1 | 3753 | (0.831, 0.169) |  |  | 1.06 | 0.632 | 0.706 |  |  |  | off simplex |
| cultivar | 9 | 3753 | (0.814, 0.186) | 0.984 | 0.998 | 1.18 | 0.627 | 0.634 | 0.978 | 0.981 | 0.729 | off simplex |
| treatment | 60 | 3753 | (0.602, 0.398) | 0.354 | 0.984 | 1.34 | 0.385 | 0.397 | 0.339 | 0.469 | 0.791 | off simplex |
| year | 55 | 3753 | (0.823, 0.177) | 0.913 | 0.985 | 1.19 | 0.604 | 0.601 | 0.908 | 0.906 | 0.58 | off simplex |
| plot | 188 | 3753 | (0.810, 0.190) | 0.345 | 0.953 | 0.909 | 0.371 | 0.491 | 0.333 | 0.358 | 0.672 | off simplex |
| year x section | 205 | 3753 | (1.000, 0.000) | 0.695 | 0.947 | 0.797 | 0.534 | 0.67 | 0.79 | 0.695 | 0.283 | off simplex |
| year x treatment | 972 | 3671 | (0.414, 0.586) | 0.15 | 0.728 | 1.28 | 0.263 | 0.286 | 0.175 | 0.296 | 0.428 | off simplex |

## Baselines on the whole table

- Frontier fit (no scaler), tau = 10.7 by `select_temperature` (a tenth above): w = (0.286, 0.714).
- PCA of log(grain, straw), whole table: eigenvalues 0.1580 and 0.8952; major axis (0.584, 0.812); minor axis (-0.812, 0.584), off the simplex.
- Invariant fit with no groups (minimum variance on the simplex): (0.831, 0.169).

## Two terms within year x treatment

K = 2, kappa = 1: W = (1.000, 0.000) and (0.000, 1.000), b = 0.723; within variance 0.06347 against 0.06907 for the monomial and 0.06746 for log biomass (the two-term invariant with W = I, b = 0).
