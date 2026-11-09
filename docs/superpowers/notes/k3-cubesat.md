# K = 3 on the cubesat datasets (WP9, D-6, Amendment 3)

Record of what the K = 1, 2, 3 fits report on the two cubesat datasets. Observed, not proved: every
number below is printed by `examples/adcs/k_terms.py`; the readings are plain descriptions of
those numbers, not explanations. Same feasibility filter and conditioning (standard scaler, ten
metrics) as the WP7 notebook. **Temperature is re-selected at each K** by the K = 1 criterion:
`select_temperature` with target `frac_above_` 0.10 (a tenth of designs above V = 1) and bounds
(3, 1e3), applied to the K-term fit (`n_terms=K`, `random_state=0`, estimator default
`facet_step` and `n_restarts`, `term_temperature` at its default of infinity). The band
1/tau therefore means the same thing at every K. The K = 1 rows are those of the earlier record
(tau 38.10 primary, 41.72 stock). Bisection bracketed the target at every K and returned a tau
within the tolerance 0.01 with no warning.

Each fit's stopping record (`termination_`) supplies the last five columns of the summary tables:
the largest facet first-order gap G_k, the status, the assignment margin gamma, the stable radius
and the Corollary 4 bound on the objective's distance to the fixed-assignment optimum. Status
"certified" means the assignment is fixed, the feasibility residuals are within tolerance, the gap
is at most 1e-8 and gamma is positive. At K = 1 the solver takes the single-facet shortcut: status
"not applicable", no margin or radius, and the gap is a diagnostic of the one facet's fit
(4.7e-06 primary, 1.8e-05 stock).

Contending sets are the tau = infinity LP support on each facet's own rows (`tension_report`, one
report per facet), largest exponent first. One choice to state: at the re-selected tau the K = 2
and 3 bands 1/tau are narrow (0.005 to 0.013), which leaves some facets with 3 to 6 designs inside
their own band, and `tension_report` refuses fewer than 10. The reports, the near-frontier counts,
the slices and the shading therefore use K = 1's band (0.0262 primary, 0.0240 stock) at every K, so
that the counts are comparable; the fit itself uses 1/tau_K. With that band every facet has at least
17 near-frontier designs. The contending sets and n-lemmas do not depend on the band.

## Primary regime (aggressive gains, `adcs_designs_cubesat_gains.csv`)

706 feasible designs.

| K | tau | band 1/tau | objective_ | frac_above_ | facet rows | facet shares | max gap | status | gamma | radius | Corollary bound |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 38.10 | 0.0262 | 0.2036 | 0.096 | 706 | 1.0 | 4.7e-06 | not applicable | - | - | 4.7e-06 |
| 2 | 113.22 | 0.0088 | 0.1384 | 0.096 | 332, 374 | 0.371, 0.629 | 3.9e-15 | certified | 0.00083 | 0.000068 | 3.7e-15 |
| 3 | 195.18 | 0.0051 | 0.1173 | 0.098 | 201, 188, 317 | 0.089, 0.133, 0.778 | 1.1e-14 | certified | 0.00022 | 0.000018 | 5.0e-15 |

K = 3 facets at tau = 195.18:

| facet | rows | contending set | n-lemma | largest working exponents | near-frontier | reach beta_k | share | gap G_k |
|---|---|---|---|---|---|---|---|---|
| 1 | 201 | control effort, slew time, energy balance, pointing error, depth of discharge, settling time | 6 | control effort 0.429, slew time 0.365, energy balance 0.142 | 17 | 0.346 | 0.089 | 1.1e-14 |
| 2 | 188 | energy balance, control effort, slew time, settling time, pointing error, depth of discharge | 6 | energy balance 0.434, control effort 0.308, slew time 0.216 | 33 | 0.477 | 0.133 | 5.2e-15 |
| 3 | 317 | peak slew power, total mass, pointing error, slew time, depth of discharge, power margin, settling time | 7 | peak slew power 0.380, total mass 0.182, pointing error 0.175 | 126 | 0.451 | 0.778 | 1.4e-15 |

K = 2 facets at tau = 113.22:

| facet | rows | contending set | n-lemma | largest working exponents | near-frontier | reach beta_k | share | gap G_k |
|---|---|---|---|---|---|---|---|---|
| 1 | 332 | control effort, slew time, energy balance, total mass, pointing error, depth of discharge, eclipse reserve | 7 | control effort 0.365, slew time 0.323, energy balance 0.264 | 35 | 0.321 | 0.371 | 3.9e-15 |
| 2 | 374 | peak slew power, pointing error, slew time, settling time, power margin, depth of discharge, total mass | 7 | peak slew power 0.515, pointing error 0.200, total mass 0.107 | 88 | 0.493 | 0.629 | 3.5e-15 |

K = 1 contending set (6): total mass, slew time, energy balance, control effort, pointing error,
depth of discharge (working exponents slew time 0.240, control effort 0.197, energy balance
0.190, total mass 0.180, pointing error 0.102, depth of discharge 0.091).

Relation of the K = 1 set to the facets: at K = 3 it is a subset of the union of the facet sets
(nine metrics; peak slew power, power margin and settling time are in the union and not in K = 1).
Facets 1 and 2 each share five of their six metrics with it (each lacks total mass, each adds
settling time); facet 3 shares four of seven (lacks control effort and energy balance; adds peak
slew power, power margin, settling time). At K = 2 the union has ten metrics and also contains
the K = 1 set: facet 1 shares six of seven (adds eclipse reserve), facet 2 four of seven.

## Stock-gains regime (`adcs_designs_cubesat.csv`)

780 feasible designs.

| K | tau | band 1/tau | objective_ | frac_above_ | facet rows | facet shares | max gap | status | gamma | radius | Corollary bound |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 41.72 | 0.0240 | 0.1312 | 0.104 | 780 | 1.0 | 1.8e-05 | not applicable | - | - | 1.8e-05 |
| 2 | 78.75 | 0.0127 | 0.1059 | 0.092 | 390, 390 | 0.694, 0.306 | 1.9e-15 | certified | 0.001575 | 0.000126 | 1.7e-15 |
| 3 | 162.78 | 0.0061 | 0.0929 | 0.094 | 284, 149, 347 | 0.077, 0.590, 0.333 | 9.1e-15 | certified | 0.001487 | 0.000119 | 7.0e-15 |

K = 3 facets at tau = 162.78:

| facet | rows | contending set | n-lemma | largest working exponents | near-frontier | reach beta_k | share | gap G_k |
|---|---|---|---|---|---|---|---|---|
| 1 | 284 | control effort, slew time, settling time, energy balance, pointing error, depth of discharge | 6 | control effort 0.488, slew time 0.261, settling time 0.111 | 20 | 0.256 | 0.077 | 9.1e-15 |
| 2 | 149 | peak slew power, slew time, pointing error, total mass, power margin, depth of discharge, control effort | 7 | peak slew power 0.359, pointing error 0.155, total mass 0.148 | 71 | 0.589 | 0.590 | 5.1e-15 |
| 3 | 347 | energy balance, control effort, slew time, settling time, depth of discharge | 5 | energy balance 0.355, control effort 0.336, slew time 0.199 | 47 | 0.287 | 0.333 | 6.2e-15 |

K = 2 facets at tau = 78.75:

| facet | rows | contending set | n-lemma | largest working exponents | near-frontier | reach beta_k | share | gap G_k |
|---|---|---|---|---|---|---|---|---|
| 1 | 390 | energy balance, control effort, slew time, settling time, depth of discharge | 5 | energy balance 0.357, control effort 0.337, slew time 0.261 | 67 | 0.258 | 0.694 | 1.9e-15 |
| 2 | 390 | control effort, slew time, energy balance, pointing error, depth of discharge | 5 | control effort 0.487, slew time 0.377, energy balance 0.086 | 29 | 0.219 | 0.306 | 1.6e-15 |

K = 1 contending set (6): control effort, slew time, power margin, settling time, pointing error,
eclipse reserve (working exponents control effort 0.430, slew time 0.332, power margin 0.176,
settling time 0.026, pointing error 0.024, eclipse reserve 0.013).

Relation: the K = 1 set is not a subset of the union at K = 2 or 3 (eclipse reserve is in K = 1
and in no facet; at K = 2 power margin is also absent). At K = 3 facet 1 shares four of six (lacks
eclipse reserve, power margin; adds depth of discharge, energy balance), facet 2 four of seven
(lacks eclipse reserve, settling time; adds depth of discharge, peak slew power, total mass),
facet 3 three of five (lacks eclipse reserve, pointing error, power margin; adds depth of
discharge, energy balance). The union has nine metrics, four of them (depth of discharge, energy
balance, peak slew power, total mass) not in K = 1.

## Diagnostic: tau fixed at its K = 1 value (the earlier record)

The same fits with K = 1's tau reused at K = 2 and 3, which shows the effect of not re-selecting.

| regime | K | tau | objective_ | frac_above_ | facet rows | facet shares | max gap | status | gamma | radius |
|---|---|---|---|---|---|---|---|---|---|---|
| primary | 1 | 38.10 | 0.2036 | 0.096 | 706 | 1.0 | | 4.7e-06 | not applicable | - | - |
| primary | 2 | 38.10 | 0.0900 | 0.261 | 378, 328 | 0.839, 0.161 | | 1.8e-15 | certified | 0.001484 | 0.000121 |
| primary | 3 | 38.10 | 0.0529 | 0.382 | 302, 190, 214 | 0.669, 0.216, 0.114 | | 9.9e-16 | certified | 0.000588 | 0.000048 |
| stock | 1 | 41.72 | 0.1312 | 0.104 | 780 | 1.0 | | 1.8e-05 | not applicable | - | - |
| stock | 2 | 41.72 | 0.0678 | 0.204 | 394, 386 | 0.617, 0.383 | | 6.4e-16 | certified | 0.001167 | 0.000093 |
| stock | 3 | 41.72 | 0.0326 | 0.338 | 290, 135, 355 | 0.307, 0.161, 0.532 | | 2.3e-15 | certified | 0.000641 | 0.000051 |

`frac_above_` rises with K at a fixed tau (0.096, 0.261, 0.382 primary). Each facet is a supporting
hyperplane at the same tau, but the envelope is the maximum over facets, so the fraction of
designs above it is not controlled by the K = 1 tau; this is why tau is re-selected above.

What re-selection changed at K = 3. Primary: tau rises from 38.1 to 195, the facet sizes move from
302, 190, 214 to 201, 188, 317, and the facet with peak slew power grows to 0.778 of the share
(0.669 before), while the two control-effort and energy-balance facets shrink and now both include
settling time (before, only the second did); the peak-slew-power facet loses nothing from its set
(it still has seven metrics) and its largest exponents are now peak slew power, total mass,
pointing error (before peak slew power, pointing error, total mass). Stock: tau rises from 41.7 to
163; sizes move from 290, 135, 355 to 284, 149, 347 and the contending sets are unchanged; the
peak-slew-power facet's share rises from 0.161 to 0.590 and the facet with control effort 0.488
falls from 0.307 to 0.077. The mean slack (`objective_`) at K = 3 is 0.117 against 0.204 at K = 1
(primary) and 0.093 against 0.131 (stock), where at the fixed tau it was about a quarter of K = 1.

## Stability over seeds 0 to 4 (K = 3, at the re-selected tau)

Primary (tau 195.18): `objective_` 0.11733 for all five seeds (differences below 2e-6);
`frac_above_` 0.098 (0.099 for seeds 2 and 4); sorted shares (0.089, 0.133, 0.778) in every seed;
the contending sets are identical in every seed.

Stock (tau 162.78): seeds 0, 1, 3, 4 agree (`objective_` 0.09287, `frac_above_` 0.0936, shares
0.077, 0.333, 0.590, the same sets). Seed 2 reaches a different, worse local optimum: `objective_`
0.1143, `frac_above_` 0.0756, shares 0.2, 0.24, 0.56, and different contending sets. This is the
solver's documented local-optimum behaviour (I7); the record reports seed 0, the lowest
objective. Five restarts per fit are the default and were not changed.

Certificates (seeds 0 to 4, K = 3, re-selected tau): every fit of both regimes has status
certified. Primary: max gap 1.1e-14 to 1.2e-14, gamma 0.00022 (seeds 0, 1, 3) and 0.001001 (seeds
2, 4), radius 0.000018 and 0.000082, bound 4.7e-15 to 5.0e-15. Stock: max gap 9.1e-15 (seed 2:
1.1e-14), gamma 0.001487 (seed 2: 0.000873), radius 0.000119 (seed 2: 0.000070), bound 7.0e-15
(seed 2: 6.1e-15). The worse local optimum of stock seed 2 is certified for its own assignment;
the certificate does not compare restarts.

## Changes from WP13

The record was regenerated after the finite-tau Newton polish and the guard tolerance 1e-12
(`solvers.py`, commits 03c8b1a to 1e9ae03). The old output is that of commit fc2363e, run
unchanged; the new output adds the certificate columns and a per-facet gap column and changes
nothing else at the precision of this record.

- Every K = 1 row (tau, band, objective_, frac_above_, facet rows, shares, the contending set and
  exponents) is unchanged to the printed digits (six decimals for objective_ and frac_above_).
- Every K = 2 and 3 row of the summary tables, the diagnostic table, the seed-stability tables
  (objective_, frac_above_, sorted shares, contending sets) and the per-facet tables (rows,
  contending sets, n-lemmas, exponents to three decimals, near-frontier counts, shares) is
  unchanged to the printed digits.
- The only changed numbers are the per-facet reach beta_k at the sixth decimal (the record shows
  it to three, so no table in this note changes). Old to new, as printed by the script:

| regime | K | facet | reach beta_k old | new |
|---|---|---|---|---|
| primary | 2 | 1 | 0.321029 | 0.321030 |
| primary | 2 | 2 | 0.492784 | 0.492783 |
| primary | 3 | 2 | 0.477358 | 0.477357 |
| primary | 3 | 3 | 0.450506 | 0.450505 |
| primary | 3 (tau 38.10) | 2 | 0.416293 | 0.416292 |
| stock | 2 | 1 | 0.258447 | 0.258448 |
| stock | 2 | 2 | 0.218955 | 0.218954 |
| stock | 3 | 1 | 0.256436 | 0.256435 |
| stock | 3 | 3 | 0.287391 | 0.287390 |
| stock | 3 (tau 41.72) | 2 | 0.547746 | 0.547745 |

- The spike's Table 3 (before the polish) reported max G_k of 2.2e-5 to 3.5e-5 at the selected
  temperatures, gamma 2.2e-4 to 1.5e-3 and radius 1.8e-5 to 1.2e-4. After the polish the gaps are
  1e-14 and below; gamma and radius agree with the spike's ranges (primary 0.00022 and 0.000018,
  stock 0.001487 and 0.000119 at seed 0).
- The three log-plane figures per regime are regenerated; the two log-plane PNGs differ from the
  earlier ones in 113 (primary) and 210 (stock) of 1.9 million pixels, from the same sixth-decimal
  shifts.
- Run time of the script: 60 s (50 s before).

## Plain observations

- Facet structure is consistent with the data being a mixture of regimes: the mean slack falls
  from K = 1 to K = 3 in both regimes (primary 0.204 to 0.117, stock 0.131 to 0.093), at a
  temperature that keeps the fraction above V = 1 near 0.10.
- Both regimes give a facet whose largest exponent is on peak slew power (primary 0.380, stock
  0.359) and which is the only facet containing total mass (K = 3, both regimes). The other two facets are
  built on control effort, slew time and energy balance. That facet carries 0.778 of the share in
  the primary regime and 0.590 in the stock regime.
- The K = 1 sets differ between regimes (primary: mass, energy balance, depth of discharge; stock:
  power margin, eclipse reserve).
- Facet contending sets are 5 to 7 metrics of ten, large n-lemmas; the LP support of a facet's rows
  is generally larger than the number of metrics with large working exponent.
- Every facet of both regimes has at least 17 near-frontier designs in K = 1's band (smallest:
  primary facet 1), so `tension_report` raised no error at the default `min_near_frontier = 10`
  once that band was used; in the narrower band 1/tau_K it would (3 to 6 designs for some K = 3
  facets), and the record does not use it. The solvers converged with the estimator defaults.

## Figures

`examples/adcs/figures/k3_log_planes_<regime>.png`, `k3_frontier_coordinates_<regime>.png`,
`k3_tensions_<regime>.png`, with `<regime>` in `primary`, `stock`; 150 dpi, the plotting module's
colour vocabulary (facet colours from `CATEGORY_COLORS`); drawn from the re-selected K = 3 fit.

A log-plane panel draws a facet's envelope only where that facet has weight on both plotted
metrics (exponents above 1e-3, the tension report's participation threshold). The panels are the
pair of metrics with each facet's two largest exponents, de-duplicated, so every facet is drawn
in at least one panel; each panel title names the facets drawn. Viewed:

- primary: (slew time, control effort) draws facets 1 and 2 (envelope visible as one black line
  with the grey band along the data's lower edge); (control effort, energy balance) draws facets 1
  and 2 (a kinked envelope, visible); (total mass, peak slew power) draws facet 3 (a straight line
  visible at the upper right, above most points, because peak slew power takes few distinct
  values in the data).
- stock: (slew time, control effort) draws facets 1, 2 and 3 (kinked envelope, visible);
  (pointing error, peak slew power) draws facet 2 (straight line visible above the data, which
  sit on a few discrete peak-slew-power levels); (control effort, energy balance) draws facets 1
  and 3 (kinked envelope, visible).

Every facet appears in a panel with a visible envelope, so no facet lacks a legible slice; the
two slices with peak slew power are the least informative (discrete values). The coordinates
figures (band: K = 1's) and the tension maps (one per facet; contending set outlined) are the
more readable figures; ten-metric slices of a K = 3 fit are projections, and the data scatter off
the slice plane.

## Reproduce

```
uv run python examples/adcs/k_terms.py   # about 60 s
uv run pytest tests/test_k_terms_case.py
```
