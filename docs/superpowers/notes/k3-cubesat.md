# K = 3 on the cubesat datasets (WP9, D-6)

Record of what the K = 1, 2, 3 fits report on the two cubesat datasets. Observed, not proved: every
number below is printed by `examples/adcs/k_terms.py`; the readings are plain descriptions of
those numbers, not explanations. Same feasibility filter, conditioning (standard scaler, ten
metrics) and temperature selection as the WP7 notebook: tau is chosen on the K = 1 fit
(`select_temperature`, target `frac_above_` 0.10, bounds (3, 1e3)) and then used unchanged at
K = 2 and 3; `random_state=0`, estimator default restarts, `term_temperature` at its default
(infinity). Contending sets are the tau = infinity LP support on each facet's own rows
(`tension_report`, one report per facet), largest exponent first.

## Primary regime (aggressive gains, `adcs_designs_cubesat_gains.csv`)

706 feasible designs, tau = 38.10, band 1/tau = 0.0262.

| facet | rows | contending set | n-lemma | largest working exponents | near-frontier | reach beta_k | share |
|---|---|---|---|---|---|---|---|
| 1 | 302 | peak slew power, pointing error, slew time, total mass, power margin, depth of discharge, settling time | 7 | peak slew power 0.484, pointing error 0.195, total mass 0.126 | 158 | 0.442 | 0.669 |
| 2 | 190 | energy balance, control effort, slew time, settling time, pointing error, depth of discharge | 6 | energy balance 0.450, control effort 0.302, slew time 0.222 | 51 | 0.416 | 0.216 |
| 3 | 214 | control effort, slew time, energy balance, pointing error, depth of discharge | 5 | control effort 0.430, slew time 0.357, energy balance 0.122 | 27 | 0.276 | 0.114 |

| K | objective_ | frac_above_ | facet rows | facet shares |
|---|---|---|---|---|
| 1 | 0.2036 | 0.096 | 706 | 1.0 |
| 2 | 0.0900 | 0.261 | 378, 328 | 0.839, 0.161 |
| 3 | 0.0529 | 0.382 | 302, 190, 214 | 0.669, 0.216, 0.114 |

K = 1 contending set (6): control effort, depth of discharge, energy balance, pointing error,
slew time, total mass (working exponents slew time 0.240, control effort 0.197, energy balance
0.190, total mass 0.180, pointing error 0.102, depth of discharge 0.091).

Relation of the K = 1 set to the facets: it is a subset of the union of the three facet sets (the
union has nine metrics; peak slew power, power margin and settling time are in the union and not
in K = 1). Facet 1 shares four of its seven metrics with it (lacks control effort and energy
balance); facet 2 shares five of six (lacks total mass, adds settling time); facet 3 shares all
five of its metrics (lacks total mass). Total mass is in the contending set of facet 1 only.

## Stock-gains regime (`adcs_designs_cubesat.csv`)

780 feasible designs, tau = 41.72, band 1/tau = 0.0240.

| facet | rows | contending set | n-lemma | largest working exponents | near-frontier | reach beta_k | share |
|---|---|---|---|---|---|---|---|
| 1 | 290 | control effort, slew time, settling time, energy balance, pointing error, depth of discharge | 6 | control effort 0.491, slew time 0.238, settling time 0.148 | 63 | 0.195 | 0.307 |
| 2 | 135 | peak slew power, slew time, pointing error, total mass, power margin, depth of discharge, control effort | 7 | peak slew power 0.370, slew time 0.172, pointing error 0.158 | 33 | 0.548 | 0.161 |
| 3 | 355 | energy balance, control effort, slew time, settling time, depth of discharge | 5 | control effort 0.351, energy balance 0.331, slew time 0.189 | 109 | 0.206 | 0.532 |

| K | objective_ | frac_above_ | facet rows | facet shares |
|---|---|---|---|---|
| 1 | 0.1312 | 0.104 | 780 | 1.0 |
| 2 | 0.0678 | 0.204 | 394, 386 | 0.617, 0.383 |
| 3 | 0.0326 | 0.338 | 290, 135, 355 | 0.307, 0.161, 0.532 |

K = 1 contending set (6): control effort, eclipse reserve, pointing error, power margin, settling
time, slew time (working exponents control effort 0.430, slew time 0.332, power margin 0.176,
settling time 0.026, pointing error 0.024, eclipse reserve 0.013).

Relation: here the K = 1 set is not a subset of the union (eclipse reserve is in K = 1 and in no
facet). Facet 1 shares four of six (lacks eclipse reserve, power margin; adds depth of discharge,
energy balance), facet 2 four of seven (lacks eclipse reserve, settling time; adds depth of
discharge, peak slew power, total mass), facet 3 three of five (lacks eclipse reserve, pointing
error, power margin; adds depth of discharge, energy balance). The union has nine metrics, four
of them (depth of discharge, energy balance, peak slew power, total mass) not in K = 1.

## Stability over seeds 0 to 4 (K = 3, same tau)

Primary: `objective_` 0.05292 for all five seeds (differences below 2e-6); `frac_above_` 0.381
to 0.382; sorted facet shares (0.113 to 0.118, 0.209 to 0.218, 0.669 to 0.678). The contending
sets are the same in every seed except one entry: the second and third facets are the
energy-balance and the control-effort facets, and in seeds 0, 1 and 4 the control-effort facet
lacks settling time (the table above), in seeds 2 and 3 it has it (six metrics). The facet with
peak slew power (seven metrics) is identical in all seeds.

Stock: `objective_` 0.03260 for all five seeds; `frac_above_` 0.338 (0.337 for seed 4); shares
(0.160 to 0.161, 0.306 to 0.307, 0.532 to 0.534); contending sets identical in all seeds.

## Plain observations

- Facet structure is consistent with the data being a mixture of regimes: at K = 3 the mean slack
  (`objective_`) is about a quarter of its K = 1 value in both regimes (0.0529
  against 0.2036; 0.0326 against 0.1312).
- Both regimes give a facet whose largest exponent is on peak slew power (primary 0.484, stock
  0.370) and which is the only facet containing total mass; the other two facets are built on
  control effort, slew time and energy balance. The roles of these facets in the share ranking
  are different: that facet carries 0.669 of near-frontier designs in the primary regime and
  0.161 in the stock regime.
- The K = 1 sets differ between regimes (primary: mass, energy balance, depth of discharge;
  stock: power margin, eclipse reserve).
- Facet contending sets are 5 to 7 metrics of ten, large n-lemmas; the LP support of a facet's
  rows is generally larger than the number of metrics with large working exponent.
- `frac_above_` rises with K at the fixed tau (0.096, 0.261, 0.382 primary), where it was set to
  0.10 only at K = 1. Each facet is a supporting hyperplane at the same tau, but the envelope is the
  maximum over facets, so the fraction of designs above it is not controlled by the K = 1 tau. It is reported, not
  re-tuned; a K-specific temperature is a separate decision.
- Every facet of both regimes has at least 27 near-frontier designs (smallest: primary facet 3), so `tension_report` raised no error at the default
  `min_near_frontier = 10`. No facet is near-empty (smallest 135 rows). The K = 2 and 3
  solvers converged with the estimator defaults.
- Two-dimensional log-plane slices of a ten-metric fit are hard to read: a slice draws only the
  facets with weight on both plotted metrics, and the data scatter widely off the slice plane.
  The coordinates figure and the tension maps are the more readable figures.

## Figures

`examples/adcs/figures/k3_log_planes_<regime>.png`, `k3_frontier_coordinates_<regime>.png`,
`k3_tensions_<regime>.png`, with `<regime>` in `primary`, `stock`; 150 dpi, the plotting module's
colour vocabulary (facet colours from `CATEGORY_COLORS`).

## Reproduce

```
uv run python examples/adcs/k_terms.py
uv run pytest tests/test_k_terms_case.py
```
