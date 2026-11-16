# The table of metrics: the stock regime's first rows and every pair's association

Appendix C.5 prints the primary regime's first rows and the pairs at |Spearman| 0.5 or above; this file holds the stock regime's first rows and all the pairs of traded metrics over the feasible designs of both regimes. The tables are `generate_model.metric_table` and `generate_model.metric_associations`, read from the data of record (`examples/adcs/data/v2/`) and written by `uv run python paper/generate_supplement.py`.

Each metric is `m_j = exp((o_j log(a_j + s_j) - c_j) / k_j)` for attribute `a_j`, with orientation `o_j` (+1 larger is better, -1 smaller is better), shift `s_j = 0`, and the offset `c_j` and log scale `k_j` of the conditioning above. The table of metrics, one row per kept design and one column per metric, is where the model ends and the method begins.

Dataset cubesat-stock: 2,355 designs by 13 metrics; the first 5 rows:

| design | settling time | pointing error | total mass | control effort | power margin | energy balance | peak slew power | depth of discharge | momentum headroom | available power | battery peak power ratio | unit cost | fleet cost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.3169 | 0.4014 | 0.2554 | 3.22 | 1.041 | 1.151 | 0.5758 | 1.307 | 8.282 | 1.014 | 1.292 | 0.4129 | 0.7742 |
| 1 | 2.748 | 2.221 | 1.004 | 0.3103 | 3.31 | 2.817 | 1.798 | 1.143 | 0.2992 | 3.198 | 1.323 | 0.2909 | 4.805 |
| 2 | 1.066 | 1.325 | 1.253 | 0.8952 | 1.345 | 1.345 | 2.128 | 4.031 | 0.3149 | 1.191 | 4.59 | 1.051 | 2.586 |
| 3 | 0.5491 | 1.018 | 1.281 | 1.029 | 4.743 | 3.669 | 2.128 | 1.008 | 0.2775 | 4.707 | 1.199 | 0.2447 | 4.59 |
| 4 | 0.8696 | 0.8995 | 1.669 | 0.9562 | 3.906 | 3.177 | 2.128 | 0.7237 | 0.2596 | 3.805 | 0.87 | 1.144 | 0.6259 |

| metric a | metric b | Spearman, cubesat-primary | Pearson, cubesat-primary | Spearman, cubesat-stock | Pearson, cubesat-stock | one axis |
|---|---|---|---|---|---|---|
| energy balance | available power | +1.000 | +0.977 | +1.000 | +0.979 | cubesat-primary, cubesat-stock |
| power margin | available power | +0.982 | +0.973 | +0.988 | +0.980 | no |
| power margin | energy balance | +0.982 | +0.955 | +0.987 | +0.962 | no |
| depth of discharge | battery peak power ratio | +0.971 | +0.970 | +0.975 | +0.974 | no |
| total mass | peak slew power | +0.864 | +0.833 | +0.817 | +0.779 | no |
| total mass | unit cost | +0.742 | +0.713 | +0.720 | +0.693 | no |
| peak slew power | unit cost | +0.677 | +0.604 | +0.594 | +0.525 | no |
| peak slew power | momentum headroom | -0.617 | -0.639 | -0.460 | -0.437 | no |
| settling time | peak slew power | -0.606 | -0.619 | -0.303 | -0.356 | no |
| settling time | total mass | -0.558 | -0.545 | -0.177 | -0.188 | no |
| available power | unit cost | -0.522 | -0.508 | -0.525 | -0.503 | no |
| energy balance | unit cost | -0.512 | -0.449 | -0.516 | -0.452 | no |
| settling time | momentum headroom | +0.511 | +0.345 | -0.406 | -0.459 | no |
| total mass | momentum headroom | -0.487 | -0.437 | -0.396 | -0.383 | no |
| total mass | available power | -0.467 | -0.481 | -0.418 | -0.426 | no |
| total mass | energy balance | -0.459 | -0.421 | -0.411 | -0.380 | no |
| pointing error | peak slew power | -0.449 | -0.232 | -0.374 | -0.278 | no |
| power margin | unit cost | -0.441 | -0.407 | -0.463 | -0.426 | no |
| total mass | control effort | +0.395 | +0.403 | +0.290 | +0.298 | no |
| settling time | control effort | -0.379 | -0.279 | -0.838 | -0.836 | no |
| settling time | unit cost | -0.358 | -0.327 | -0.070 | -0.075 | no |
| control effort | peak slew power | +0.352 | +0.371 | +0.308 | +0.338 | no |
| total mass | power margin | -0.345 | -0.328 | -0.320 | -0.305 | no |
| control effort | energy balance | -0.340 | -0.321 | -0.264 | -0.259 | no |
| control effort | available power | -0.340 | -0.352 | -0.263 | -0.278 | no |
| total mass | depth of discharge | -0.331 | -0.346 | -0.345 | -0.361 | no |
| pointing error | unit cost | -0.327 | -0.332 | -0.178 | -0.208 | no |
| control effort | unit cost | +0.326 | +0.327 | +0.240 | +0.244 | no |
| unit cost | fleet cost | -0.322 | -0.475 | -0.340 | -0.490 | no |
| pointing error | total mass | -0.308 | -0.324 | -0.193 | -0.221 | no |
| control effort | power margin | -0.291 | -0.291 | -0.214 | -0.217 | no |
| momentum headroom | unit cost | -0.269 | -0.231 | -0.179 | -0.173 | no |
| power margin | momentum headroom | -0.257 | -0.297 | -0.212 | -0.223 | no |
| peak slew power | available power | -0.246 | -0.246 | -0.122 | -0.118 | no |
| energy balance | peak slew power | -0.235 | -0.205 | -0.113 | -0.096 | no |
| peak slew power | battery peak power ratio | +0.233 | +0.255 | +0.213 | +0.243 | no |
| pointing error | control effort | -0.227 | -0.117 | -0.583 | -0.538 | no |
| control effort | momentum headroom | +0.213 | +0.276 | +0.525 | +0.561 | no |
| total mass | fleet cost | +0.182 | +0.149 | +0.172 | +0.141 | no |
| momentum headroom | battery peak power ratio | -0.173 | -0.169 | -0.108 | -0.099 | no |
| settling time | battery peak power ratio | -0.161 | -0.161 | -0.086 | -0.091 | no |
| peak slew power | fleet cost | +0.157 | +0.106 | +0.147 | +0.101 | no |
| total mass | battery peak power ratio | -0.138 | -0.149 | -0.184 | -0.196 | no |
| available power | fleet cost | -0.130 | -0.113 | -0.121 | -0.100 | no |
| energy balance | fleet cost | -0.127 | -0.103 | -0.118 | -0.092 | no |
| momentum headroom | available power | -0.126 | -0.139 | -0.143 | -0.147 | no |
| energy balance | momentum headroom | -0.126 | -0.138 | -0.143 | -0.141 | no |
| settling time | available power | +0.124 | +0.135 | -0.036 | -0.042 | no |
| settling time | energy balance | +0.124 | +0.117 | -0.035 | -0.036 | no |
| pointing error | momentum headroom | -0.120 | -0.078 | -0.423 | -0.400 | no |
| power margin | fleet cost | -0.114 | -0.098 | -0.108 | -0.089 | no |
| pointing error | energy balance | -0.108 | -0.114 | -0.085 | -0.095 | no |
| pointing error | fleet cost | -0.104 | -0.093 | -0.055 | -0.041 | no |
| available power | battery peak power ratio | -0.102 | -0.106 | -0.062 | -0.063 | no |
| energy balance | battery peak power ratio | -0.101 | -0.096 | -0.061 | -0.060 | no |
| power margin | peak slew power | -0.098 | -0.048 | +0.001 | +0.046 | no |
| settling time | fleet cost | -0.091 | -0.086 | -0.021 | -0.020 | no |
| battery peak power ratio | unit cost | +0.089 | +0.090 | +0.044 | +0.045 | no |
| pointing error | available power | -0.087 | -0.066 | -0.074 | -0.070 | no |
| pointing error | power margin | -0.085 | -0.062 | -0.092 | -0.088 | no |
| control effort | battery peak power ratio | +0.083 | +0.092 | +0.075 | +0.081 | no |
| power margin | battery peak power ratio | -0.059 | -0.049 | -0.026 | -0.018 | no |
| control effort | fleet cost | +0.056 | +0.045 | +0.043 | +0.034 | no |
| settling time | pointing error | +0.055 | +0.009 | +0.567 | +0.503 | no |
| momentum headroom | fleet cost | -0.051 | -0.033 | -0.055 | -0.040 | no |
| depth of discharge | unit cost | -0.042 | -0.038 | -0.054 | -0.051 | no |
| depth of discharge | available power | -0.040 | -0.040 | -0.033 | -0.033 | no |
| energy balance | depth of discharge | -0.039 | -0.037 | -0.032 | -0.032 | no |
| power margin | depth of discharge | -0.037 | -0.034 | -0.028 | -0.027 | no |
| pointing error | depth of discharge | -0.035 | -0.036 | -0.011 | -0.011 | no |
| peak slew power | depth of discharge | +0.032 | +0.023 | +0.031 | +0.032 | no |
| pointing error | battery peak power ratio | -0.028 | -0.025 | -0.038 | -0.035 | no |
| depth of discharge | fleet cost | -0.020 | -0.012 | -0.005 | +0.001 | no |
| depth of discharge | momentum headroom | -0.008 | -0.008 | -0.006 | -0.006 | no |
| settling time | depth of discharge | -0.007 | -0.008 | -0.006 | -0.002 | no |
| settling time | power margin | +0.006 | -0.004 | -0.091 | -0.110 | no |
| control effort | depth of discharge | -0.006 | +0.000 | -0.004 | -0.003 | no |
| battery peak power ratio | fleet cost | +0.004 | +0.008 | +0.015 | +0.018 | no |

Pairs at |Spearman| 0.99 or above, read as one axis with their two exponents summed per term: primary regime: energy balance and available power; stock regime: energy balance and available power.
