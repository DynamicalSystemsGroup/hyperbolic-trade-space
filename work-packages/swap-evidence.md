# Swap evidence: this Mac against the CI run (ubuntu, amd64), WP10 and WP15

Measured without Docker. Sources: the failing CI logs of the dev `Tests` runs 42572757374
(commit a7eebde) and 42560520228 (commit 33f63b1), read with `gh run view --log`; and native
re-runs on this Mac (macOS arm64) of the check designs, with the regeneration perturbed at the
level of one unit in the last place.

## What the logs contain, and what they do not

A failed `np.testing.assert_allclose` prints the arrays of the first failing column only, and the
test checks the columns in file order, so the CI logs hold **only `torque_saturated_frac` of the six
check designs** (it is column 25 of 34). Everything the test checked before it passed on CI: the
text columns, the four feasibility flags (`settled`, `momentum_ok`, `power_ok`, `dod_ok`) exactly,
and the first 24 numeric columns, which include all ten fitted attributes, within rtol 1e-3
(1e-6 absolute; 0.5 s for the time columns). The last nine columns (`adcs_mass_kg` to
`slew_loss_energy_wh`) were never reached on CI, and the first-20-design tests of both datasets
passed on CI, but their per-column numbers are not printed. The spread of those columns between the
Mac and CI is therefore **not measurable from the logs**; what is known is that it lies inside the
tolerances above. Per-column spreads between CI and this Mac for the first twenty designs cannot be
given for the same reason.

Mac against the committed files (the committed files were produced on this Mac): the six check
designs and the first twenty designs of each dataset regenerate with relative differences of at most
4e-9 in every column, which is the printed precision of the CSV (nine significant digits); flags and
labels are identical.

## `torque_saturated_frac`, six check designs

| design | committed (Mac) | CI run 42560520228 | CI run 42572757374 | abs diff to CI (max of the two runs) |
|---|---|---|---|---|
| 0 | 0.017870 | 0.021513 | 0.020074 | 0.00364 |
| 1 | 0.026906 | 0.029083 | 0.029806 | 0.00290 |
| 2 | 0.118411 | 0.119084 | 0.119665 | 0.00125 |
| 3 | 0.080260 | 0.082973 | 0.079710 | 0.00271 |
| 4 | 0.172100 | 0.171472 | 0.173222 | 0.00112 |
| 5 | 0.007925 | 0.007925 | 0.007925 | 0 |

The two CI runs differ from each other as well (the model file `model_v2/cubesat.sysml` and the
runner changed between those commits, so this is not by itself evidence of nondeterminism on CI).
Relative differences reach 20 percent on design 0 (limit in the test: rtol 0.1), at most 8 percent
on the others; absolute differences are at most 0.0036.

## Why it moves

`torque_saturated_frac` is `mean(sat)` over the **accepted steps of an adaptive RK45 integration**
(`adcs_sim.simulate_adcs`: `rtol=1e-10`, `atol=1e-12`, `max_step=0.5`, 360 s), where `sat` is true
when a torque component is at the wheel limit. It is a count divided by the number of steps, for
example 24 of 1343 steps for design 0. A step is accepted or rejected by comparing an error
estimate with the tolerance, so a difference of one unit in the last place in the inputs or in a
maths-library call (`exp`, `cos`, the linear-algebra routine) changes the step sequence by a few
steps and moves the count by whole steps. It is a discrete statistic of the step sequence, not a
smooth function of the design, while the continuous outputs (times, masses, energies) are smooth in
the trajectory and move by about 1e-9.

Measured here on this Mac: multiplying `Kp`, `Kd`, `panel_span_m` and `battery_wh` of the six check
designs by 1 + 1e-15 changes the step counts (design 0: 1343 steps and 24 saturated become 1347 and
28; the fraction moves from 0.01787 to 0.02079) and the same at 1e-13 and 1e-11 (design 0 reaches
0.02151 = 29 of 1348, exactly the value CI run 42560520228 printed). Over 60 draws of a random
relative perturbation of at most 1e-12 on those four inputs, the step counts range over 1342 to 1348
for design 0 and 1377 to 1393 for design 3, and the saturated fraction deviates from the committed
value by at most:

| design | max abs deviation | range of the fraction over the 60 draws |
|---|---|---|
| 0 | 0.00364 | 0.01787 to 0.02151 |
| 1 | 0.00292 | 0.02399 to 0.02981 |
| 2 | 0.00270 | 0.11571 to 0.12110 |
| 3 | 0.00804 | 0.07759 to 0.08830 |
| 4 | 0.00548 | 0.16945 to 0.17758 |
| 5 | 0 | 0.00793 |

Over all six designs the maximum is 0.0080 and the 95th percentile 0.0038. The two CI values per
design and the Mac value all lie inside the ranges of this ensemble, so a perturbation at the level
of rounding reproduces the differences seen on CI. No change of outcome accompanies it: the settled, momentum, power and depth-of-discharge flags are
identical on every one of the 60 perturbed draws. The fitted attributes move as follows over the same
60 draws (maximum relative deviation per attribute): `pointing_error_deg` 7e-13, `total_mass_kg`
1e-13, `power_margin_w` 3e-12, `peak_slew_power_w` 1e-12, `energy_balance_wh` 3e-9,
`dod_eclipse` 2e-9, `eclipse_reserve_wh` 6e-9, `control_effort` 7e-5, but `settling_time_s` 1.3e-2
and `slew_time_s` 1.1e-2. The two time columns are also read off the step sequence (the first or
last step at which the error crosses a threshold), and their largest absolute deviation was 0.48 s
against the test's absolute allowance of 0.5 s (`cmp.TIME_COLUMNS`, atol 0.5): on CI these passed,
but the margin is thin, and a CI run on another maths library could cross it. This is recorded for
the driver; the test has not been changed.

## Proposed absolute tolerance (the driver sets it)

An **absolute** tolerance, `atol = 0.01` on `torque_saturated_frac` (no relative term), for the
check-design test; the first-20 tests keep their existing `sat_rtol` unless the driver decides
otherwise. Reason: the quantity is a step count over about 1340 steps; its deviation under rounding
is a few steps (up to about 11, which is 0.008 here) whatever the value, so the error is absolute in
the number of steps and not proportional to the fraction. A relative tolerance is wrong at both
ends: it is too strict for small fractions (design 0 at 0.018 moved 20 percent for 5 steps) and
unneeded for large ones. 0.01 is 1.25 times the largest deviation in the ensemble and 2.8 times the
largest seen on CI, about 13 steps in 1340. It is a weak check for design 5 (0.0079) and says only
that the fraction stays small there; the substantive checks of the design remain the exact flags and
the 1e-3 relative checks on the ten fitted attributes.

## Status of the currently failing test

`tests/test_v2_data.py::test_the_check_designs_regenerate_within_the_tolerances` is **failing on CI
(ubuntu, amd64) and passing on this Mac, awaiting the driver's tolerance decision**. Its tolerance
(rtol 1e-1 on this column) has not been changed.

## Is `torque_saturated_frac` fitted?

No. It is a **diagnostic column only**. The ten fitted attributes are `settling_time_s`,
`slew_time_s`, `pointing_error_deg`, `total_mass_kg`, `control_effort`, `power_margin_w`,
`energy_balance_wh`, `eclipse_reserve_wh`, `peak_slew_power_w` and `dod_eclipse` (`ATTRIBUTES` in
`examples/adcs/make_check_designs.py`; `ATTRIBUTE_NAMES` of the v2 oracle). The oracle's
`FLAG_NAMES` are the four feasibility flags and exclude it; it is an auxiliary output carried in the
files (`FLAGS` in `experiments/check_designs.py`) and compared in the tests only.

## Outcomes unchanged

Every quantity visible in the CI logs agrees in kind with this Mac: the flags and the fitted
attributes of the check designs passed their tests on CI, so no propose-predict-check outcome, no
feasibility flag and no fitted quantity differs between the Mac and CI as far as the logs show.
The logs do not print the propose-predict-check outcome itself; it is derived from the fitted
attributes, which agree within 1e-3.

## Environment of record, for the other three tests

On this Mac the SHA-256 of the 900-row planted table is `c127dd4c...`, equal to the committed
digest; CI (amd64) gives `f6c45d25...`. Figure 1's data hash is `f9d7219d...` here and `4040cb8e...`
on CI. The pin `FIGURE1_HASH` is now the `4040cb8e...` value, asserted only with
`HTS_ENVIRONMENT_OF_RECORD=1`. The list of such values is `paper/environment_values.toml`.

## Sensitivity of the conclusions to the step-quantized times

Generated by `examples/adcs/experiments/sensitivity.py` (WP16 Amendment 1, D-6); no Docker.

**Method.** Each of the two cubesat datasets (primary, aggressive gain box; baseline, stock gain box) and the six check designs were regenerated 5 times through the clean oracle (`CubesatOracle`; the sampler, design ids and seeds of the v2 generation; the same worker pool) with `Kp`, `Kd`, `panel_span_m` and `battery_wh` of every design multiplied by `1 + e`, `e` uniform in [-1e-12, 1e-12] per design and variable from `numpy.random.default_rng(seed)`, seeds 1, 2, 3, 4, 5. The regenerated files were written to a scratch directory (never `examples/adcs/data`, never the ledger). For each regeneration `case.py` was run as the paper runs it: the one-term fit with the temperature re-selected, the K = 2 and K = 3 fits (`spec.seed`), the regime comparison, the nondominated counts, the candidates and propose-predict-check (the regressor refit on the regenerated primary data; the recorded predictions; the check designs regenerated with the same kind of perturbation, and, as a second reading, the committed check measurements). Every table of Appendix D and every generated sentence of the case sections was computed, and each quantity is compared at the precision the paper prints it (tables at four significant digits, temperatures at one decimal, sentences verbatim). The facets of K = 2 and K = 3 are compared as labelled and, separately, as an unlabelled set.

Run time of the regenerations on this Mac: 6 minutes.

### Verdict on the conclusions

**NOT IDENTICAL: at least one listed conclusion differs; see the rows below.**

| conclusion | quantities compared | across 5 regenerations and committed |
|---|---|---|
| the contending sets (K = 1, both regimes; each facet at K = 3) | 20 | IDENTICAL |
| each facet's leading metrics | 8 | IDENTICAL |
| the signs of the tensions (the six reported pairs, both regimes) | 24 | IDENTICAL |
| the selected temperatures (K = 1, 2, 3, both regimes) | 6 | IDENTICAL |
| the certificate statuses (K = 1, 2, 3, both regimes) | 6 | IDENTICAL |
| the regime comparison | 25 | NOT IDENTICAL: regime \| tau, frac_above_, n_eff_ \| primary; regime \| tau, frac_above_, n_eff_ \| stock; regime \| band 1/tau, near-frontier designs \| primary; regime \| settling time, total mass \| primary; regime \| slew time, total mass \| primary; regime \| settling time, pointing error \| primary; regime \| slew time, control effort \| primary; regime \| settling time, slew time \| primary |
| the nondominated counts | 25 | NOT IDENTICAL: sentence \| nondominated \| text; nondominated \| primary \| four metrics \| nondominated; nondominated \| primary \| four metrics \| share; nondominated \| primary \| settling time and slew time \| nondominated; nondominated \| primary \| settling time and slew time \| share; nondominated \| stock \| four metrics \| nondominated; nondominated \| stock \| four metrics \| share |
| the check designs' outcomes (pass or miss) | 6 | IDENTICAL |

### Headline quantities that print differently

The committed value and each regeneration's value, for the quantities of the verdict, the nondominated counts and the paper's generated sentences that change at the printed precision.

| quantity | committed | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 |
|---|---|---|---|---|---|---|
| sentence \| nondominated \| text | On the cubesat table, of 706 feasible designs, the nondominated sets hold 671 on 10, 146 on 4 and 8 on 2 attributes respectively. | On the cubesat table, of 706 feasible designs, the nondominated sets hold 671 on 10, 145 on 4 and 8 on 2 attributes respectively. | On the cubesat table, of 706 feasible designs, the nondominated sets hold 671 on 10, 146 on 4 and 7 on 2 attributes respectively. | On the cubesat table, of 706 feasible designs, the nondominated sets hold 671 on 10, 145 on 4 and 7 on 2 attributes respectively. | On the cubesat table, of 706 feasible designs, the nondominated sets hold 671 on 10, 146 on 4 and 7 on 2 attributes respectively. | On the cubesat table, of 706 feasible designs, the nondominated sets hold 671 on 10, 145 on 4 and 8 on 2 attributes respectively. |
| sentence \| temperature \| text | The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16.2 designs. | The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16.1 designs. | The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16.1 designs. | The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16.0 designs. | The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16.1 designs. | The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16.1 designs. |
| sentence \| K sweep \| text | The mean slack falls from 0.204 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3. The facets of the K = 3 fit hold facet shares 0.089, 0.133 and 0.778 and contending sets of 6, 6 and 7 metrics; their union has 9 metrics, of which peak slew power, power margin and settling time are absent from the K = 1 set. The solver declares the status certified at K = 2 and 3, with the largest facet gap 1.1e-14, the smallest assignment margin 0.00022 and the smallest stable radius 1.8e-05. | The mean slack falls from 0.203 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3. The facets of the K = 3 fit hold facet shares 0.087, 0.152 and 0.761 and contending sets of 6, 6 and 7 metrics; their union has 9 metrics, of which peak slew power, power margin and settling time are absent from the K = 1 set. The solver declares the status certified at K = 2 and 3, with the largest facet gap 1.2e-14, the smallest assignment margin 0.00121 and the smallest stable radius 9.9e-05. | The mean slack falls from 0.203 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3. The facets of the K = 3 fit hold facet shares 0.068, 0.136 and 0.795 and contending sets of 6, 6 and 7 metrics; their union has 9 metrics, of which peak slew power, power margin and settling time are absent from the K = 1 set. The solver declares the status certified at K = 2 and 3, with the largest facet gap 5.4e-15, the smallest assignment margin 0.00121 and the smallest stable radius 9.9e-05. | The mean slack falls from 0.203 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3. The facets of the K = 3 fit hold facet shares 0.068, 0.136 and 0.795 and contending sets of 6, 6 and 7 metrics; their union has 9 metrics, of which peak slew power, power margin and settling time are absent from the K = 1 set. The solver declares the status certified at K = 2 and 3, with the largest facet gap 7.7e-15, the smallest assignment margin 0.00162 and the smallest stable radius 1.3e-04. | The mean slack falls from 0.203 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3. The facets of the K = 3 fit hold facet shares 0.065, 0.152 and 0.783 and contending sets of 6, 6 and 7 metrics; their union has 9 metrics, of which peak slew power, power margin and settling time are absent from the K = 1 set. The solver declares the status certified at K = 2 and 3, with the largest facet gap 1.7e-14, the smallest assignment margin 0.00135 and the smallest stable radius 1.1e-04. | The mean slack falls from 0.203 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3. The facets of the K = 3 fit hold facet shares 0.087, 0.152 and 0.761 and contending sets of 6, 6 and 7 metrics; their union has 9 metrics, of which peak slew power, power margin and settling time are absent from the K = 1 set. The solver declares the status certified at K = 2 and 3, with the largest facet gap 4.4e-15, the smallest assignment margin 0.00081 and the smallest stable radius 6.6e-05. |
| sentence \| certificate \| text | As printed by the solver on the primary regime, K = 1: status not_applicable, largest facet gap 4.7e-06; K = 2: status certified, largest facet gap 3.9e-15; K = 3: status certified, largest facet gap 1.1e-14. | As printed by the solver on the primary regime, K = 1: status not_applicable, largest facet gap 3.6e-06; K = 2: status certified, largest facet gap 7.7e-15; K = 3: status certified, largest facet gap 1.2e-14. | As printed by the solver on the primary regime, K = 1: status not_applicable, largest facet gap 4.0e-06; K = 2: status certified, largest facet gap 2.7e-15; K = 3: status certified, largest facet gap 5.4e-15. | As printed by the solver on the primary regime, K = 1: status not_applicable, largest facet gap 3.8e-06; K = 2: status certified, largest facet gap 5.8e-15; K = 3: status certified, largest facet gap 7.7e-15. | As printed by the solver on the primary regime, K = 1: status not_applicable, largest facet gap 4.1e-06; K = 2: status certified, largest facet gap 3.1e-15; K = 3: status certified, largest facet gap 1.7e-14. | As printed by the solver on the primary regime, K = 1: status not_applicable, largest facet gap 4.3e-06; K = 2: status certified, largest facet gap 2.1e-15; K = 3: status certified, largest facet gap 4.4e-15. |
| regime \| tau, frac_above_, n_eff_ \| primary | 38.1, 0.096, 16.2 | 38.1, 0.096, 16.1 | 38.1, 0.096, 16.1 | 38.1, 0.096, 16.0 | 38.1, 0.096, 16.1 | 38.1, 0.096, 16.1 |
| regime \| tau, frac_above_, n_eff_ \| stock | 41.7, 0.104, 14.5 | 41.7, 0.104, 14.5 | 41.7, 0.105, 14.5 | 41.7, 0.104, 14.5 | 41.7, 0.104, 14.5 | 41.7, 0.105, 14.5 |
| regime \| band 1/tau, near-frontier designs \| primary | 0.0262, 51 | 0.0262, 51 | 0.0262, 52 | 0.0262, 51 | 0.0262, 51 | 0.0262, 51 |
| regime \| settling time, total mass \| primary | -0.54 (-0.34) | -0.54 (-0.33) | -0.54 (-0.34) | -0.54 (-0.33) | -0.54 (-0.34) | -0.54 (-0.33) |
| regime \| slew time, total mass \| primary | -0.48 (-0.33) | -0.48 (-0.33) | -0.48 (-0.34) | -0.48 (-0.33) | -0.48 (-0.33) | -0.48 (-0.33) |
| regime \| settling time, pointing error \| primary | +0.18 (+0.20) | +0.18 (+0.19) | +0.18 (+0.19) | +0.18 (+0.20) | +0.18 (+0.20) | +0.18 (+0.19) |
| regime \| slew time, control effort \| primary | -0.87 (-0.83) | -0.87 (-0.83) | -0.87 (-0.84) | -0.87 (-0.83) | -0.87 (-0.83) | -0.87 (-0.83) |
| regime \| settling time, slew time \| primary | +0.91 (+0.88) | +0.91 (+0.88) | +0.90 (+0.87) | +0.91 (+0.88) | +0.91 (+0.87) | +0.91 (+0.88) |
| nondominated \| primary \| four metrics \| nondominated | 146 | 145 | 146 | 145 | 146 | 145 |
| nondominated \| primary \| four metrics \| share | 0.2068 | 0.2054 | 0.2068 | 0.2054 | 0.2068 | 0.2054 |
| nondominated \| primary \| settling time and slew time \| nondominated | 8 | 8 | 7 | 7 | 7 | 8 |
| nondominated \| primary \| settling time and slew time \| share | 0.01133 | 0.01133 | 0.009915 | 0.009915 | 0.009915 | 0.01133 |
| nondominated \| stock \| four metrics \| nondominated | 157 | 158 | 158 | 157 | 157 | 157 |
| nondominated \| stock \| four metrics \| share | 0.2013 | 0.2026 | 0.2026 | 0.2013 | 0.2013 | 0.2013 |
| sentence \| candidates \| text | The 3 measured candidates have energy differentials between -0.144 and -0.072; 0 of them lie beyond the fitted reference surface. Their ranks among the training designs run from 0.59 to 0.77. | The 3 measured candidates have energy differentials between -0.144 and -0.071; 0 of them lie beyond the fitted reference surface. Their ranks among the training designs run from 0.59 to 0.78. | The 3 measured candidates have energy differentials between -0.144 and -0.071; 0 of them lie beyond the fitted reference surface. Their ranks among the training designs run from 0.59 to 0.77. | The 3 measured candidates have energy differentials between -0.144 and -0.071; 0 of them lie beyond the fitted reference surface. Their ranks among the training designs run from 0.59 to 0.78. | The 3 measured candidates have energy differentials between -0.144 and -0.071; 0 of them lie beyond the fitted reference surface. Their ranks among the training designs run from 0.59 to 0.78. | The 3 measured candidates have energy differentials between -0.144 and -0.071; 0 of them lie beyond the fitted reference surface. Their ranks among the training designs run from 0.59 to 0.78. |
| predict \| proposal_1 \| measured log V | -0.09002 | -0.08924 | -0.08982 | -0.09054 | -0.09057 | -0.08964 |
| predict \| proposal_1 \| difference | -0.02101 | -0.02022 | -0.02081 | -0.02153 | -0.02156 | -0.02062 |
| predict \| proposal_1 \| \|diff\| / band | 0.3229 | 0.3108 | 0.3199 | 0.3309 | 0.3314 | 0.317 |
| predict \| proposal_1 \| \|\|dZ\|\| | 0.08802 | 0.08853 | 0.08935 | 0.09074 | 0.08877 | 0.08856 |
| predict \| proposal_1 \| \|\|dZ\|\| / band | 1.353 | 1.361 | 1.373 | 1.395 | 1.364 | 1.361 |
| predict \| proposal_2 \| measured log V | -0.07974 | -0.07877 | -0.07974 | -0.08036 | -0.08074 | -0.07905 |
| predict \| proposal_2 \| difference | -0.0221 | -0.02113 | -0.0221 | -0.02272 | -0.0231 | -0.02141 |
| predict \| proposal_2 \| \|diff\| / band | 0.3397 | 0.3248 | 0.3397 | 0.3492 | 0.3551 | 0.3291 |
| predict \| proposal_2 \| \|\|dZ\|\| | 0.1439 | 0.1439 | 0.1439 | 0.1445 | 0.1439 | 0.1439 |
| predict \| proposal_2 \| \|\|dZ\|\| / band | 2.211 | 2.212 | 2.212 | 2.222 | 2.212 | 2.211 |
| predict \| proposal_3 \| measured log V | -0.2084 | -0.2108 | -0.2109 | -0.2093 | -0.2078 | -0.2106 |
| predict \| proposal_3 \| difference | -0.04593 | -0.04836 | -0.04848 | -0.04682 | -0.04539 | -0.04813 |
| predict \| proposal_3 \| \|diff\| / band | 0.706 | 0.7433 | 0.7451 | 0.7197 | 0.6977 | 0.7397 |
| predict \| proposal_3 \| \|\|dZ\|\| | 0.2007 | 0.2007 | 0.2007 | 0.2017 | 0.2008 | 0.2008 |
| predict \| proposal_3 \| \|\|dZ\|\| / band | 3.085 | 3.085 | 3.085 | 3.1 | 3.086 | 3.086 |

### Deviation of the ten fitted attributes from the committed data

Primary (1000 designs): largest relative / absolute deviation from the committed file, per column and regeneration.

| column | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | max rel | max abs |
|---|---|---|---|---|---|---|---|
| settling_time_s | 9.9e-03 / 4.8e-01 | 9.0e-03 / 4.8e-01 | 1.2e-02 / 4.9e-01 | 1.0e-02 / 4.6e-01 | 1.0e-02 / 4.8e-01 | 1.2e-02 | 4.9e-01 |
| slew_time_s | 4.3e-02 / 4.3e-01 | 4.6e-02 / 3.9e-01 | 6.3e-01 / 2.1e+01 | 4.0e-02 / 4.6e-01 | 3.8e-02 / 4.7e-01 | 6.3e-01 | 2.1e+01 |
| pointing_error_deg | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| total_mass_kg | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| control_effort | 1.3e-04 / 2.3e-05 | 1.1e-04 / 2.0e-05 | 1.3e-04 / 2.3e-05 | 1.0e-04 / 2.6e-05 | 1.7e-04 / 3.1e-05 | 1.7e-04 | 3.1e-05 |
| power_margin_w | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| energy_balance_wh | 1.3e-08 / 2.0e-07 | 1.5e-08 / 2.0e-07 | 9.8e-09 / 2.0e-07 | 1.3e-08 / 2.0e-07 | 9.9e-09 / 2.0e-07 | 1.5e-08 | 2.0e-07 |
| eclipse_reserve_wh | 2.9e-07 / 2.0e-07 | 5.1e-07 / 2.0e-07 | 4.2e-07 / 2.0e-07 | 3.0e-07 / 2.0e-07 | 4.7e-07 / 2.0e-07 | 5.1e-07 | 2.0e-07 |
| peak_slew_power_w | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| dod_eclipse | 1.7e-08 / 4.0e-09 | 2.7e-08 / 4.0e-09 | 2.1e-08 / 4.0e-09 | 2.5e-08 / 5.0e-09 | 1.8e-08 / 5.0e-09 | 2.7e-08 | 5.0e-09 |

Designs whose `settling_time_s` moved by more than 0.5 s: seed 1: 0 of 1000; seed 2: 0 of 1000; seed 3: 0 of 1000; seed 4: 0 of 1000; seed 5: 0 of 1000.

Designs whose `slew_time_s` moved by more than 0.5 s: seed 1: 0 of 1000; seed 2: 0 of 1000; seed 3: 1 of 1000; seed 4: 0 of 1000; seed 5: 0 of 1000.

Changed against the committed file: seed 1: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 2: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 3: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 4: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 5: 0 flag cells, 0 feasibility verdicts, 0 label cells.

Baseline (1000 designs): largest relative / absolute deviation from the committed file, per column and regeneration.

| column | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | max rel | max abs |
|---|---|---|---|---|---|---|---|
| settling_time_s | 1.1e-02 / 4.8e-01 | 9.1e-03 / 4.9e-01 | 9.7e-03 / 4.8e-01 | 1.1e-02 / 4.9e-01 | 8.6e-03 / 4.8e-01 | 1.1e-02 | 4.9e-01 |
| slew_time_s | 2.9e-02 / 4.5e-01 | 3.2e-02 / 4.4e-01 | 2.5e-02 / 4.2e-01 | 3.4e-02 / 4.5e-01 | 2.3e-02 / 4.4e-01 | 3.4e-02 | 4.5e-01 |
| pointing_error_deg | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| total_mass_kg | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| control_effort | 8.9e-05 / 1.1e-05 | 8.3e-05 / 7.4e-06 | 8.0e-05 / 8.8e-06 | 8.7e-05 / 7.7e-06 | 8.7e-05 / 1.1e-05 | 8.9e-05 | 1.1e-05 |
| power_margin_w | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| energy_balance_wh | 6.5e-09 / 1.0e-07 | 2.8e-09 / 1.0e-07 | 6.2e-09 / 1.0e-07 | 4.9e-09 / 1.0e-07 | 2.9e-09 / 1.0e-07 | 6.5e-09 | 1.0e-07 |
| eclipse_reserve_wh | 8.5e-08 / 1.0e-07 | 2.4e-08 / 1.0e-07 | 2.6e-08 / 1.0e-07 | 3.0e-08 / 1.0e-07 | 2.7e-08 / 1.0e-07 | 8.5e-08 | 1.0e-07 |
| peak_slew_power_w | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| dod_eclipse | 8.7e-09 / 1.0e-09 | 7.3e-09 / 1.0e-09 | 1.2e-08 / 1.0e-09 | 1.2e-08 / 1.0e-09 | 1.0e-08 / 1.0e-09 | 1.2e-08 | 1.0e-09 |

Designs whose `settling_time_s` moved by more than 0.5 s: seed 1: 0 of 1000; seed 2: 0 of 1000; seed 3: 0 of 1000; seed 4: 0 of 1000; seed 5: 0 of 1000.

Designs whose `slew_time_s` moved by more than 0.5 s: seed 1: 0 of 1000; seed 2: 0 of 1000; seed 3: 0 of 1000; seed 4: 0 of 1000; seed 5: 0 of 1000.

Changed against the committed file: seed 1: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 2: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 3: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 4: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 5: 0 flag cells, 0 feasibility verdicts, 0 label cells.

Check designs (6): largest relative / absolute deviation from the committed file, per column and regeneration.

| column | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | max rel | max abs |
|---|---|---|---|---|---|---|---|
| settling_time_s | 1.7e-03 / 1.1e-01 | 1.1e-02 / 4.0e-01 | 2.0e-03 / 5.0e-02 | 2.1e-03 / 6.3e-02 | 2.8e-03 / 2.0e-01 | 1.1e-02 | 4.0e-01 |
| slew_time_s | 1.4e-03 / 1.7e-02 | 9.3e-04 / 1.1e-02 | 2.2e-03 / 2.6e-02 | 2.3e-03 / 2.8e-02 | 6.2e-04 / 7.5e-03 | 2.3e-03 | 2.8e-02 |
| pointing_error_deg | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| total_mass_kg | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| control_effort | 8.1e-06 / 6.2e-07 | 2.0e-05 / 1.5e-06 | 3.3e-05 / 2.5e-06 | 1.6e-05 / 1.3e-06 | 5.5e-06 / 2.7e-07 | 3.3e-05 | 2.5e-06 |
| power_margin_w | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| energy_balance_wh | 2.7e-09 / 1.0e-08 | 2.7e-09 / 1.0e-08 | 0.0e+00 / 0.0e+00 | 2.7e-09 / 1.0e-08 | 0.0e+00 / 0.0e+00 | 2.7e-09 | 1.0e-08 |
| eclipse_reserve_wh | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 4.7e-09 / 1.0e-08 | 0.0e+00 / 0.0e+00 | 4.7e-09 | 1.0e-08 |
| peak_slew_power_w | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |
| dod_eclipse | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 / 0.0e+00 | 0.0e+00 | 0.0e+00 |

Designs whose `settling_time_s` moved by more than 0.5 s: seed 1: 0 of 6; seed 2: 0 of 6; seed 3: 0 of 6; seed 4: 0 of 6; seed 5: 0 of 6.

Designs whose `slew_time_s` moved by more than 0.5 s: seed 1: 0 of 6; seed 2: 0 of 6; seed 3: 0 of 6; seed 4: 0 of 6; seed 5: 0 of 6.

Changed against the committed file: seed 1: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 2: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 3: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 4: 0 flag cells, 0 feasibility verdicts, 0 label cells; seed 5: 0 flag cells, 0 feasibility verdicts, 0 label cells.

### Every quantity the paper reports

Per quantity: the committed value, the minimum and maximum over the 5 regenerations (numbers; `-` for text and truth values), how many regenerations print the same as the committed value, and whether anything changes at the printed precision.

#### sentence

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| nondominated \| text | On the cubesat table, of 706 feasible designs, the nondominated sets hold 671 on 10, 146 on 4 and 8 on 2 attributes respectively. | - | - | 0/5 | YES |
| datasets \| text | The primary regime evaluates 1000 designs and keeps 706 as feasible; the stock regime evaluates 1000 and keeps 780. Each design carries 10 attributes. | - | - | 5/5 | no |
| temperature \| text | The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10), the band 1/tau is 0.0262 and the effective sample size is 16.2 designs. | - | - | 0/5 | YES |
| K = 1 contending \| text | At K = 1 the fit reports a 6-lemma: total mass, slew time, energy balance, control effort, pointing error and depth of discharge contend, and settling time, power margin, eclipse reserve and peak slew power do not constrain the frontier at that facet. | - | - | 5/5 | no |
| K sweep \| text | The mean slack falls from 0.204 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3. The facets of the K = 3 fit hold facet shares 0.089, 0.133 and 0.778 and contending sets of 6, 6 and 7 metrics; their union has 9 metrics, of which peak slew power, power margin and settling time are absent from the K = 1 set. The solver declares the status certified at K = 2 and 3, with the largest facet gap 1.1e-14, the smallest assignment margin 0.00022 and the smallest stable radius 1.8e-05. | - | - | 0/5 | YES |
| certificate \| text | As printed by the solver on the primary regime, K = 1: status not_applicable, largest facet gap 4.7e-06; K = 2: status certified, largest facet gap 3.9e-15; K = 3: status certified, largest facet gap 1.1e-14. | - | - | 0/5 | YES |
| regime \| text | The two regimes return a 6-lemma and a 6-lemma that share 3 metrics (control effort, pointing error and slew time). Only the primary regime has depth of discharge, energy balance and total mass contending; only the stock regime has eclipse reserve, power margin and settling time. | - | - | 5/5 | no |
| candidates \| text | The 3 measured candidates have energy differentials between -0.144 and -0.072; 0 of them lie beyond the fitted reference surface. Their ranks among the training designs run from 0.59 to 0.77. | - | - | 0/5 | YES |
| predict-check \| text | Of 3 proposals, the predicted energy differential lies within the band 1/tau = 0.0651 of the measured one for 3, and the predicted position along the frontier lies within the band for 0; the position errors run from 1.4 to 3.1 bands. | - | - | 5/5 | no |

#### regime

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| dataset \| primary | adcs_designs_cubesat_gains.csv | - | - | 5/5 | no |
| dataset \| stock | adcs_designs_cubesat.csv | - | - | 5/5 | no |
| feasible n \| primary | 706 (191 / 248 / 267) | - | - | 5/5 | no |
| feasible n \| stock | 780 (239 / 279 / 262) | - | - | 5/5 | no |
| tau, frac_above_, n_eff_ \| primary | 38.1, 0.096, 16.2 | - | - | 0/5 | YES |
| tau, frac_above_, n_eff_ \| stock | 41.7, 0.104, 14.5 | - | - | 3/5 | YES |
| band 1/tau, near-frontier designs \| primary | 0.0262, 51 | - | - | 4/5 | YES |
| band 1/tau, near-frontier designs \| stock | 0.0240, 103 | - | - | 5/5 | no |
| n_lemma \| primary | 6 | - | - | 5/5 | no |
| n_lemma \| stock | 6 | - | - | 5/5 | no |
| contending set \| primary | total mass, slew time, energy balance, control effort, pointing error, depth of discharge | - | - | 5/5 | no |
| contending set \| stock | control effort, slew time, power margin, settling time, pointing error, eclipse reserve | - | - | 5/5 | no |
| settling time, total mass \| primary | -0.54 (-0.34) | - | - | 2/5 | YES |
| settling time, total mass \| stock | -0.12 (-0.02) | - | - | 5/5 | no |
| slew time, total mass \| primary | -0.48 (-0.33) | - | - | 4/5 | YES |
| slew time, total mass \| stock | -0.10 (-0.03) | - | - | 5/5 | no |
| pointing error, control effort \| primary | -0.36 (-0.48) | - | - | 5/5 | no |
| pointing error, control effort \| stock | -0.70 (-0.77) | - | - | 5/5 | no |
| settling time, pointing error \| primary | +0.18 (+0.20) | - | - | 2/5 | YES |
| settling time, pointing error \| stock | +0.69 (+0.75) | - | - | 5/5 | no |
| slew time, control effort \| primary | -0.87 (-0.83) | - | - | 4/5 | YES |
| slew time, control effort \| stock | -0.96 (-0.95) | - | - | 5/5 | no |
| settling time, slew time \| primary | +0.91 (+0.88) | - | - | 3/5 | YES |
| settling time, slew time \| stock | +0.99 (+0.99) | - | - | 5/5 | no |

#### fit

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary K=1 \| frac_above_ | 0.09632 | 0.09632 | 0.09632 | 5/5 | no |
| primary K=1 \| n_eff_ | 16.18 | 16 | 16.1 | 0/5 | YES |
| primary K=1 \| tau selected (raw) | 38.1 | 38.1 | 38.1 | 5/5 | no |
| primary K=2 \| tau selected (raw) | 113.2 | 113.2 | 113.2 | 5/5 | no |
| primary K=3 \| tau selected (raw) | 195.2 | 195.2 | 195.2 | 5/5 | no |
| stock K=1 \| frac_above_ | 0.1038 | 0.1038 | 0.1051 | 3/5 | YES |
| stock K=1 \| n_eff_ | 14.48 | 14.5 | 14.53 | 0/5 | YES |
| stock K=1 \| tau selected (raw) | 41.72 | 41.72 | 41.72 | 5/5 | no |
| stock K=2 \| tau selected (raw) | 78.75 | 78.75 | 78.75 | 5/5 | no |
| stock K=3 \| tau selected (raw) | 162.8 | 162.8 | 162.8 | 5/5 | no |

#### tau

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary K=1 \| tau selected (printed .1f) | 38.1 | - | - | 5/5 | no |
| primary K=2 \| tau selected (printed .1f) | 113.2 | - | - | 5/5 | no |
| primary K=3 \| tau selected (printed .1f) | 195.2 | - | - | 5/5 | no |
| stock K=1 \| tau selected (printed .1f) | 41.7 | - | - | 5/5 | no |
| stock K=2 \| tau selected (printed .1f) | 78.7 | - | - | 5/5 | no |
| stock K=3 \| tau selected (printed .1f) | 162.8 | - | - | 5/5 | no |

#### contending

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary K=1 facet 1 \| set | total mass, slew time, energy balance, control effort, pointing error, depth of discharge | - | - | 5/5 | no |
| primary K=1 facet 1 \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary K=3 facet 1 \| set | control effort, slew time, energy balance, pointing error, depth of discharge, settling time | - | - | 5/5 | no |
| primary K=3 facet 1 \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary K=3 facet 2 \| set | energy balance, control effort, slew time, settling time, pointing error, depth of discharge | - | - | 5/5 | no |
| primary K=3 facet 2 \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary K=3 facet 3 \| set | peak slew power, total mass, pointing error, slew time, depth of discharge, power margin, settling time | - | - | 5/5 | no |
| primary K=3 facet 3 \| n_lemma | 7 | 7 | 7 | 5/5 | no |
| primary K=2 facets as an unlabelled set \| sets | control effort, slew time, energy balance, total mass, pointing error, depth of discharge, eclipse reserve / control effort, slew time, energy balance ;; peak slew power, pointing error, slew time, settling time, power margin, depth of discharge, total mass / peak slew power, pointing error, total mass | - | - | 5/5 | no |
| primary K=3 facets as an unlabelled set \| sets | control effort, slew time, energy balance, pointing error, depth of discharge, settling time / control effort, slew time, energy balance ;; energy balance, control effort, slew time, settling time, pointing error, depth of discharge / energy balance, control effort, slew time ;; peak slew power, total mass, pointing error, slew time, depth of discharge, power margin, settling time / peak slew power, total mass, pointing error | - | - | 5/5 | no |
| stock K=1 facet 1 \| set | control effort, slew time, power margin, settling time, pointing error, eclipse reserve | - | - | 5/5 | no |
| stock K=1 facet 1 \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| stock K=3 facet 1 \| set | control effort, slew time, settling time, energy balance, pointing error, depth of discharge | - | - | 5/5 | no |
| stock K=3 facet 1 \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| stock K=3 facet 2 \| set | peak slew power, slew time, pointing error, total mass, power margin, depth of discharge, control effort | - | - | 5/5 | no |
| stock K=3 facet 2 \| n_lemma | 7 | 7 | 7 | 5/5 | no |
| stock K=3 facet 3 \| set | energy balance, control effort, slew time, settling time, depth of discharge | - | - | 5/5 | no |
| stock K=3 facet 3 \| n_lemma | 5 | 5 | 5 | 5/5 | no |
| stock K=2 facets as an unlabelled set \| sets | control effort, slew time, energy balance, pointing error, depth of discharge / control effort, slew time, energy balance ;; energy balance, control effort, slew time, settling time, depth of discharge / energy balance, control effort, slew time | - | - | 5/5 | no |
| stock K=3 facets as an unlabelled set \| sets | control effort, slew time, settling time, energy balance, pointing error, depth of discharge / control effort, slew time, settling time ;; energy balance, control effort, slew time, settling time, depth of discharge / energy balance, control effort, slew time ;; peak slew power, slew time, pointing error, total mass, power margin, depth of discharge, control effort / peak slew power, pointing error, total mass | - | - | 5/5 | no |

#### leading

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary K=1 facet 1 \| metrics | slew time, control effort, energy balance | - | - | 5/5 | no |
| primary K=3 facet 1 \| metrics | control effort, slew time, energy balance | - | - | 5/5 | no |
| primary K=3 facet 2 \| metrics | energy balance, control effort, slew time | - | - | 5/5 | no |
| primary K=3 facet 3 \| metrics | peak slew power, total mass, pointing error | - | - | 5/5 | no |
| stock K=1 facet 1 \| metrics | control effort, slew time, power margin | - | - | 5/5 | no |
| stock K=3 facet 1 \| metrics | control effort, slew time, settling time | - | - | 5/5 | no |
| stock K=3 facet 2 \| metrics | peak slew power, pointing error, total mass | - | - | 5/5 | no |
| stock K=3 facet 3 \| metrics | energy balance, control effort, slew time | - | - | 5/5 | no |

#### certificate

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| 1 \| max gap | 4.724e-06 | 3.624e-06 | 4.285e-06 | 0/5 | YES |
| primary \| 1 \| status | not_applicable | - | - | 5/5 | no |
| primary \| 1 \| gamma | nan | nan | nan | 5/5 | no |
| primary \| 1 \| radius | nan | nan | nan | 5/5 | no |
| primary \| 1 \| bound | 4.724e-06 | 3.624e-06 | 4.285e-06 | 0/5 | YES |
| primary \| 2 \| max gap | 3.941e-15 | 2.082e-15 | 7.661e-15 | 0/5 | YES |
| primary \| 2 \| status | certified | - | - | 5/5 | no |
| primary \| 2 \| gamma | 0.0008297 | 0.001166 | 0.001644 | 0/5 | YES |
| primary \| 2 \| radius | 6.763e-05 | 9.502e-05 | 0.000134 | 0/5 | YES |
| primary \| 2 \| bound | 3.721e-15 | 1.957e-15 | 5.244e-15 | 0/5 | YES |
| primary \| 3 \| max gap | 1.066e-14 | 4.385e-15 | 1.721e-14 | 0/5 | YES |
| primary \| 3 \| status | certified | - | - | 5/5 | no |
| primary \| 3 \| gamma | 0.0002201 | 0.0008062 | 0.001908 | 0/5 | YES |
| primary \| 3 \| radius | 1.794e-05 | 6.571e-05 | 0.0001555 | 0/5 | YES |
| primary \| 3 \| bound | 5.02e-15 | 3.199e-15 | 7.756e-15 | 0/5 | YES |
| stock \| 1 \| max gap | 1.816e-05 | 1.297e-05 | 1.55e-05 | 0/5 | YES |
| stock \| 1 \| status | not_applicable | - | - | 5/5 | no |
| stock \| 1 \| gamma | nan | nan | nan | 5/5 | no |
| stock \| 1 \| radius | nan | nan | nan | 5/5 | no |
| stock \| 1 \| bound | 1.816e-05 | 1.297e-05 | 1.55e-05 | 0/5 | YES |
| stock \| 2 \| max gap | 1.86e-15 | 9.159e-16 | 3.775e-15 | 0/5 | YES |
| stock \| 2 \| status | certified | - | - | 5/5 | no |
| stock \| 2 \| gamma | 0.001575 | 0.001292 | 0.001562 | 0/5 | YES |
| stock \| 2 \| radius | 0.0001259 | 0.0001033 | 0.0001249 | 0/5 | YES |
| stock \| 2 \| bound | 1.707e-15 | 7.216e-16 | 2.803e-15 | 0/5 | YES |
| stock \| 3 \| max gap | 9.104e-15 | 5.287e-15 | 1.404e-14 | 0/5 | YES |
| stock \| 3 \| status | certified | - | - | 5/5 | no |
| stock \| 3 \| gamma | 0.001487 | 0.001161 | 0.001434 | 0/5 | YES |
| stock \| 3 \| radius | 0.0001189 | 9.282e-05 | 0.0001147 | 0/5 | YES |
| stock \| 3 \| bound | 7.026e-15 | 4.039e-15 | 8.484e-15 | 0/5 | YES |

#### nondominated

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| all attributes \| columns | 10 | 10 | 10 | 5/5 | no |
| primary \| all attributes \| nondominated | 671 | 671 | 671 | 5/5 | no |
| primary \| all attributes \| of | 706 | 706 | 706 | 5/5 | no |
| primary \| all attributes \| share | 0.9504 | 0.9504 | 0.9504 | 5/5 | no |
| primary \| four metrics \| columns | 4 | 4 | 4 | 5/5 | no |
| primary \| four metrics \| nondominated | 146 | 145 | 146 | 2/5 | YES |
| primary \| four metrics \| of | 706 | 706 | 706 | 5/5 | no |
| primary \| four metrics \| share | 0.2068 | 0.2054 | 0.2068 | 2/5 | YES |
| primary \| settling time and slew time \| columns | 2 | 2 | 2 | 5/5 | no |
| primary \| settling time and slew time \| nondominated | 8 | 7 | 8 | 2/5 | YES |
| primary \| settling time and slew time \| of | 706 | 706 | 706 | 5/5 | no |
| primary \| settling time and slew time \| share | 0.01133 | 0.009915 | 0.01133 | 2/5 | YES |
| stock \| all attributes \| columns | 10 | 10 | 10 | 5/5 | no |
| stock \| all attributes \| nondominated | 732 | 732 | 732 | 5/5 | no |
| stock \| all attributes \| of | 780 | 780 | 780 | 5/5 | no |
| stock \| all attributes \| share | 0.9385 | 0.9385 | 0.9385 | 5/5 | no |
| stock \| four metrics \| columns | 4 | 4 | 4 | 5/5 | no |
| stock \| four metrics \| nondominated | 157 | 157 | 158 | 3/5 | YES |
| stock \| four metrics \| of | 780 | 780 | 780 | 5/5 | no |
| stock \| four metrics \| share | 0.2013 | 0.2013 | 0.2026 | 3/5 | YES |
| stock \| settling time and slew time \| columns | 2 | 2 | 2 | 5/5 | no |
| stock \| settling time and slew time \| nondominated | 2 | 2 | 2 | 5/5 | no |
| stock \| settling time and slew time \| of | 780 | 780 | 780 | 5/5 | no |
| stock \| settling time and slew time \| share | 0.002564 | 0.002564 | 0.002564 | 5/5 | no |

#### D k_table

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| 1 \| tau | 38.1 | 38.1 | 38.1 | 5/5 | no |
| primary \| 1 \| band 1/tau | 0.0262 | 0.0262 | 0.0262 | 5/5 | no |
| primary \| 1 \| objective_ | 0.2036 | 0.2029 | 0.2035 | 0/5 | YES |
| primary \| 1 \| frac_above_ | 0.09632 | 0.09632 | 0.09632 | 5/5 | no |
| primary \| 1 \| facet rows | [706] | - | - | 5/5 | no |
| primary \| 1 \| facet shares | [1.0] | - | - | 5/5 | no |
| primary \| 1 \| max gap | 4.724e-06 | 3.624e-06 | 4.285e-06 | 0/5 | YES |
| primary \| 1 \| status | not_applicable | - | - | 5/5 | no |
| primary \| 1 \| gamma | nan | nan | nan | 5/5 | no |
| primary \| 1 \| radius | nan | nan | nan | 5/5 | no |
| primary \| 1 \| bound | 4.724e-06 | 3.624e-06 | 4.285e-06 | 0/5 | YES |
| primary \| 2 \| tau | 113.2 | 113.2 | 113.2 | 5/5 | no |
| primary \| 2 \| band 1/tau | 0.0088 | 0.0088 | 0.0088 | 5/5 | no |
| primary \| 2 \| objective_ | 0.1384 | 0.1382 | 0.1384 | 1/5 | YES |
| primary \| 2 \| frac_above_ | 0.09632 | 0.09773 | 0.09915 | 0/5 | YES |
| primary \| 2 \| facet rows | [332, 374] | - | - | 0/5 | YES |
| primary \| 2 \| facet shares | [0.371, 0.629] | - | - | 0/5 | YES |
| primary \| 2 \| max gap | 3.941e-15 | 2.082e-15 | 7.661e-15 | 0/5 | YES |
| primary \| 2 \| status | certified | - | - | 5/5 | no |
| primary \| 2 \| gamma | 0.0008297 | 0.001166 | 0.001644 | 0/5 | YES |
| primary \| 2 \| radius | 6.763e-05 | 9.502e-05 | 0.000134 | 0/5 | YES |
| primary \| 2 \| bound | 3.721e-15 | 1.957e-15 | 5.244e-15 | 0/5 | YES |
| primary \| 3 \| tau | 195.2 | 195.2 | 195.2 | 5/5 | no |
| primary \| 3 \| band 1/tau | 0.0051 | 0.0051 | 0.0051 | 5/5 | no |
| primary \| 3 \| objective_ | 0.1173 | 0.1168 | 0.1172 | 0/5 | YES |
| primary \| 3 \| frac_above_ | 0.09773 | 0.0949 | 0.09632 | 0/5 | YES |
| primary \| 3 \| facet rows | [201, 188, 317] | - | - | 0/5 | YES |
| primary \| 3 \| facet shares | [0.089, 0.133, 0.778] | - | - | 0/5 | YES |
| primary \| 3 \| max gap | 1.066e-14 | 4.385e-15 | 1.721e-14 | 0/5 | YES |
| primary \| 3 \| status | certified | - | - | 5/5 | no |
| primary \| 3 \| gamma | 0.0002201 | 0.0008062 | 0.001908 | 0/5 | YES |
| primary \| 3 \| radius | 1.794e-05 | 6.571e-05 | 0.0001555 | 0/5 | YES |
| primary \| 3 \| bound | 5.02e-15 | 3.199e-15 | 7.756e-15 | 0/5 | YES |
| stock \| 1 \| tau | 41.72 | 41.72 | 41.72 | 5/5 | no |
| stock \| 1 \| band 1/tau | 0.024 | 0.024 | 0.024 | 5/5 | no |
| stock \| 1 \| objective_ | 0.1312 | 0.1312 | 0.1312 | 5/5 | no |
| stock \| 1 \| frac_above_ | 0.1038 | 0.1038 | 0.1051 | 3/5 | YES |
| stock \| 1 \| facet rows | [780] | - | - | 5/5 | no |
| stock \| 1 \| facet shares | [1.0] | - | - | 5/5 | no |
| stock \| 1 \| max gap | 1.816e-05 | 1.297e-05 | 1.55e-05 | 0/5 | YES |
| stock \| 1 \| status | not_applicable | - | - | 5/5 | no |
| stock \| 1 \| gamma | nan | nan | nan | 5/5 | no |
| stock \| 1 \| radius | nan | nan | nan | 5/5 | no |
| stock \| 1 \| bound | 1.816e-05 | 1.297e-05 | 1.55e-05 | 0/5 | YES |
| stock \| 2 \| tau | 78.75 | 78.75 | 78.75 | 5/5 | no |
| stock \| 2 \| band 1/tau | 0.0127 | 0.0127 | 0.0127 | 5/5 | no |
| stock \| 2 \| objective_ | 0.1059 | 0.1059 | 0.1059 | 5/5 | no |
| stock \| 2 \| frac_above_ | 0.09231 | 0.09103 | 0.09359 | 2/5 | YES |
| stock \| 2 \| facet rows | [390, 390] | - | - | 5/5 | no |
| stock \| 2 \| facet shares | [0.694, 0.306] | - | - | 2/5 | YES |
| stock \| 2 \| max gap | 1.86e-15 | 9.159e-16 | 3.775e-15 | 0/5 | YES |
| stock \| 2 \| status | certified | - | - | 5/5 | no |
| stock \| 2 \| gamma | 0.001575 | 0.001292 | 0.001562 | 0/5 | YES |
| stock \| 2 \| radius | 0.0001259 | 0.0001033 | 0.0001249 | 0/5 | YES |
| stock \| 2 \| bound | 1.707e-15 | 7.216e-16 | 2.803e-15 | 0/5 | YES |
| stock \| 3 \| tau | 162.8 | 162.8 | 162.8 | 5/5 | no |
| stock \| 3 \| band 1/tau | 0.0061 | 0.0061 | 0.0061 | 5/5 | no |
| stock \| 3 \| objective_ | 0.09287 | 0.09277 | 0.09285 | 0/5 | YES |
| stock \| 3 \| frac_above_ | 0.09359 | 0.09231 | 0.09359 | 3/5 | YES |
| stock \| 3 \| facet rows | [284, 149, 347] | - | - | 5/5 | no |
| stock \| 3 \| facet shares | [0.077, 0.59, 0.333] | - | - | 0/5 | YES |
| stock \| 3 \| max gap | 9.104e-15 | 5.287e-15 | 1.404e-14 | 0/5 | YES |
| stock \| 3 \| status | certified | - | - | 5/5 | no |
| stock \| 3 \| gamma | 0.001487 | 0.001161 | 0.001434 | 0/5 | YES |
| stock \| 3 \| radius | 0.0001189 | 9.282e-05 | 0.0001147 | 0/5 | YES |
| stock \| 3 \| bound | 7.026e-15 | 4.039e-15 | 8.484e-15 | 0/5 | YES |

#### D exponents K=1

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| settling time \| exponent w | 0 | 0 | 5.979e-17 | 3/5 | YES |
| primary \| slew time \| exponent w | 0.2395 | 0.2397 | 0.2406 | 0/5 | YES |
| primary \| pointing error \| exponent w | 0.1022 | 0.102 | 0.1022 | 3/5 | YES |
| primary \| total mass \| exponent w | 0.1796 | 0.1783 | 0.1792 | 0/5 | YES |
| primary \| control effort \| exponent w | 0.1974 | 0.1977 | 0.1985 | 0/5 | YES |
| primary \| power margin \| exponent w | 3.53e-17 | 0 | 1.035e-17 | 0/5 | YES |
| primary \| energy balance \| exponent w | 0.1902 | 0.19 | 0.1901 | 0/5 | YES |
| primary \| eclipse reserve \| exponent w | 5.631e-17 | 0 | 2.801e-17 | 0/5 | YES |
| primary \| peak slew power \| exponent w | 0 | 0 | 7.145e-17 | 3/5 | YES |
| primary \| depth of discharge \| exponent w | 0.09107 | 0.09061 | 0.09097 | 0/5 | YES |
| stock \| settling time \| exponent w | 0.02602 | 0.02612 | 0.02656 | 0/5 | YES |
| stock \| slew time \| exponent w | 0.3316 | 0.331 | 0.3315 | 0/5 | YES |
| stock \| pointing error \| exponent w | 0.0237 | 0.02373 | 0.02378 | 0/5 | YES |
| stock \| total mass \| exponent w | 3.364e-17 | 0 | 8.656e-17 | 0/5 | YES |
| stock \| control effort \| exponent w | 0.4295 | 0.4295 | 0.4296 | 2/5 | YES |
| stock \| power margin \| exponent w | 0.1757 | 0.1757 | 0.1757 | 5/5 | no |
| stock \| energy balance \| exponent w | 0 | 0 | 2.501e-16 | 2/5 | YES |
| stock \| eclipse reserve \| exponent w | 0.01344 | 0.01343 | 0.01346 | 0/5 | YES |
| stock \| peak slew power \| exponent w | 3.729e-17 | 0 | 6.526e-17 | 0/5 | YES |
| stock \| depth of discharge \| exponent w | 7.461e-18 | 0 | 2.337e-17 | 0/5 | YES |

#### D exponents K=3

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| settling time \| facet 1 | 0 | 0 | 4.425e-18 | 3/5 | YES |
| primary \| settling time \| facet 2 | 0.02204 | 0.0219 | 0.02202 | 0/5 | YES |
| primary \| settling time \| facet 3 | 0.01602 | 0.01577 | 0.01603 | 1/5 | YES |
| primary \| slew time \| facet 1 | 0.3655 | 0.3624 | 0.364 | 0/5 | YES |
| primary \| slew time \| facet 2 | 0.2164 | 0.2163 | 0.2165 | 2/5 | YES |
| primary \| slew time \| facet 3 | 0.09206 | 0.09207 | 0.09262 | 0/5 | YES |
| primary \| pointing error \| facet 1 | 0.03992 | 0.04153 | 0.04393 | 0/5 | YES |
| primary \| pointing error \| facet 2 | 0.01525 | 0.01515 | 0.01519 | 0/5 | YES |
| primary \| pointing error \| facet 3 | 0.1747 | 0.1744 | 0.1747 | 4/5 | YES |
| primary \| total mass \| facet 1 | 0 | 8.562e-18 | 6.988e-17 | 0/5 | YES |
| primary \| total mass \| facet 2 | 0.00246 | 0.00253 | 0.002584 | 0/5 | YES |
| primary \| total mass \| facet 3 | 0.1823 | 0.1822 | 0.1831 | 2/5 | YES |
| primary \| control effort \| facet 1 | 0.4294 | 0.4268 | 0.4282 | 0/5 | YES |
| primary \| control effort \| facet 2 | 0.3076 | 0.3074 | 0.3074 | 0/5 | YES |
| primary \| control effort \| facet 3 | 5.155e-18 | 0 | 8.635e-18 | 0/5 | YES |
| primary \| power margin \| facet 1 | 4.351e-17 | 0 | 9.2e-17 | 0/5 | YES |
| primary \| power margin \| facet 2 | 0 | 0 | 3.294e-17 | 3/5 | YES |
| primary \| power margin \| facet 3 | 0.06965 | 0.06963 | 0.0699 | 0/5 | YES |
| primary \| energy balance \| facet 1 | 0.1417 | 0.1418 | 0.142 | 0/5 | YES |
| primary \| energy balance \| facet 2 | 0.434 | 0.4341 | 0.4342 | 0/5 | YES |
| primary \| energy balance \| facet 3 | 0 | 0 | 6.577e-17 | 3/5 | YES |
| primary \| eclipse reserve \| facet 1 | 0 | 0 | 4.352e-17 | 3/5 | YES |
| primary \| eclipse reserve \| facet 2 | 0 | 0 | 2.398e-17 | 2/5 | YES |
| primary \| eclipse reserve \| facet 3 | 0 | 0 | 6.291e-17 | 2/5 | YES |
| primary \| peak slew power \| facet 1 | 1.068e-16 | 0 | 8.722e-17 | 0/5 | YES |
| primary \| peak slew power \| facet 2 | 0 | 0 | 9.94e-17 | 4/5 | YES |
| primary \| peak slew power \| facet 3 | 0.3801 | 0.3786 | 0.3801 | 2/5 | YES |
| primary \| depth of discharge \| facet 1 | 0.02352 | 0.02421 | 0.02512 | 0/5 | YES |
| primary \| depth of discharge \| facet 2 | 0.00226 | 0.002343 | 0.002402 | 0/5 | YES |
| primary \| depth of discharge \| facet 3 | 0.08526 | 0.08524 | 0.08558 | 1/5 | YES |
| stock \| settling time \| facet 1 | 0.1109 | 0.1107 | 0.1125 | 0/5 | YES |
| stock \| settling time \| facet 2 | 0.01731 | 0.01728 | 0.01761 | 1/5 | YES |
| stock \| settling time \| facet 3 | 0.08963 | 0.08913 | 0.09042 | 0/5 | YES |
| stock \| slew time \| facet 1 | 0.261 | 0.2593 | 0.2613 | 0/5 | YES |
| stock \| slew time \| facet 2 | 0.1448 | 0.1442 | 0.1449 | 1/5 | YES |
| stock \| slew time \| facet 3 | 0.1986 | 0.1977 | 0.1992 | 0/5 | YES |
| stock \| pointing error \| facet 1 | 0.0507 | 0.0506 | 0.05112 | 0/5 | YES |
| stock \| pointing error \| facet 2 | 0.1547 | 0.1547 | 0.1549 | 2/5 | YES |
| stock \| pointing error \| facet 3 | 0.001255 | 0.001021 | 0.001495 | 0/5 | YES |
| stock \| total mass \| facet 1 | 0 | 0 | 1.702e-16 | 2/5 | YES |
| stock \| total mass \| facet 2 | 0.1477 | 0.1477 | 0.1478 | 4/5 | YES |
| stock \| total mass \| facet 3 | 2.333e-16 | 0 | 4.206e-16 | 0/5 | YES |
| stock \| control effort \| facet 1 | 0.4876 | 0.4874 | 0.4877 | 2/5 | YES |
| stock \| control effort \| facet 2 | 0.02312 | 0.0227 | 0.02315 | 0/5 | YES |
| stock \| control effort \| facet 3 | 0.3363 | 0.3362 | 0.3364 | 2/5 | YES |
| stock \| power margin \| facet 1 | 1.667e-17 | 0 | 5.972e-17 | 0/5 | YES |
| stock \| power margin \| facet 2 | 0.0869 | 0.08677 | 0.08692 | 0/5 | YES |
| stock \| power margin \| facet 3 | 0 | 0 | 8.152e-17 | 4/5 | YES |
| stock \| energy balance \| facet 1 | 0.08241 | 0.08189 | 0.08268 | 1/5 | YES |
| stock \| energy balance \| facet 2 | 2.261e-17 | 0 | 3.053e-17 | 0/5 | YES |
| stock \| energy balance \| facet 3 | 0.3554 | 0.3552 | 0.3558 | 1/5 | YES |
| stock \| eclipse reserve \| facet 1 | 7.052e-17 | 0 | 5.939e-17 | 0/5 | YES |
| stock \| eclipse reserve \| facet 2 | 0 | 0 | 4.85e-17 | 2/5 | YES |
| stock \| eclipse reserve \| facet 3 | 9.629e-18 | 0 | 1.037e-16 | 0/5 | YES |
| stock \| peak slew power \| facet 1 | 0 | 0 | 2.68e-16 | 2/5 | YES |
| stock \| peak slew power \| facet 2 | 0.3585 | 0.3584 | 0.359 | 1/5 | YES |
| stock \| peak slew power \| facet 3 | 2.036e-16 | 0 | 1.871e-16 | 0/5 | YES |
| stock \| depth of discharge \| facet 1 | 0.007429 | 0.007377 | 0.00746 | 0/5 | YES |
| stock \| depth of discharge \| facet 2 | 0.06695 | 0.06695 | 0.06699 | 1/5 | YES |
| stock \| depth of discharge \| facet 3 | 0.01882 | 0.01866 | 0.01887 | 0/5 | YES |

#### D facets K=3

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| 1 \| rows | 201 | 202 | 202 | 0/5 | YES |
| primary \| 1 \| contending set | control effort, slew time, energy balance, pointing error, depth of discharge, settling time | - | - | 5/5 | no |
| primary \| 1 \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary \| 1 \| largest exponents | control effort 0.429, slew time 0.365, energy balance 0.142 | - | - | 0/5 | YES |
| primary \| 1 \| near-frontier | 17 | 17 | 18 | 2/5 | YES |
| primary \| 1 \| reach beta_k | 0.3464 | 0.3442 | 0.3457 | 0/5 | YES |
| primary \| 1 \| share | 0.08889 | 0.06522 | 0.08696 | 0/5 | YES |
| primary \| 1 \| gap G_k | 1.066e-14 | 1.749e-15 | 1.721e-14 | 0/5 | YES |
| primary \| 2 \| rows | 188 | 187 | 187 | 0/5 | YES |
| primary \| 2 \| contending set | energy balance, control effort, slew time, settling time, pointing error, depth of discharge | - | - | 5/5 | no |
| primary \| 2 \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary \| 2 \| largest exponents | energy balance 0.434, control effort 0.308, slew time 0.216 | - | - | 0/5 | YES |
| primary \| 2 \| near-frontier | 33 | 33 | 33 | 5/5 | no |
| primary \| 2 \| reach beta_k | 0.4774 | 0.4771 | 0.4776 | 1/5 | YES |
| primary \| 2 \| share | 0.1333 | 0.1364 | 0.1522 | 0/5 | YES |
| primary \| 2 \| gap G_k | 5.163e-15 | 1.443e-15 | 7.744e-15 | 0/5 | YES |
| primary \| 3 \| rows | 317 | 317 | 317 | 5/5 | no |
| primary \| 3 \| contending set | peak slew power, total mass, pointing error, slew time, depth of discharge, power margin, settling time | - | - | 5/5 | no |
| primary \| 3 \| n_lemma | 7 | 7 | 7 | 5/5 | no |
| primary \| 3 \| largest exponents | peak slew power 0.380, total mass 0.182, pointing error 0.175 | - | - | 4/5 | YES |
| primary \| 3 \| near-frontier | 126 | 125 | 126 | 2/5 | YES |
| primary \| 3 \| reach beta_k | 0.4505 | 0.4498 | 0.4506 | 3/5 | YES |
| primary \| 3 \| share | 0.7778 | 0.7609 | 0.7955 | 0/5 | YES |
| primary \| 3 \| gap G_k | 1.36e-15 | 6.245e-16 | 1.193e-14 | 0/5 | YES |
| stock \| 1 \| rows | 284 | 284 | 284 | 5/5 | no |
| stock \| 1 \| contending set | control effort, slew time, settling time, energy balance, pointing error, depth of discharge | - | - | 5/5 | no |
| stock \| 1 \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| stock \| 1 \| largest exponents | control effort 0.488, slew time 0.261, settling time 0.111 | - | - | 1/5 | YES |
| stock \| 1 \| near-frontier | 20 | 20 | 21 | 4/5 | YES |
| stock \| 1 \| reach beta_k | 0.2564 | 0.2562 | 0.2568 | 1/5 | YES |
| stock \| 1 \| share | 0.07692 | 0.07895 | 0.1053 | 0/5 | YES |
| stock \| 1 \| gap G_k | 9.104e-15 | 1.721e-15 | 1.404e-14 | 0/5 | YES |
| stock \| 2 \| rows | 149 | 149 | 149 | 5/5 | no |
| stock \| 2 \| contending set | peak slew power, slew time, pointing error, total mass, power margin, depth of discharge, control effort | - | - | 5/5 | no |
| stock \| 2 \| n_lemma | 7 | 7 | 7 | 5/5 | no |
| stock \| 2 \| largest exponents | peak slew power 0.359, pointing error 0.155, total mass 0.148 | - | - | 4/5 | YES |
| stock \| 2 \| near-frontier | 71 | 71 | 72 | 3/5 | YES |
| stock \| 2 \| reach beta_k | 0.5892 | 0.5892 | 0.5897 | 2/5 | YES |
| stock \| 2 \| share | 0.5897 | 0.5385 | 0.5789 | 0/5 | YES |
| stock \| 2 \| gap G_k | 5.079e-15 | 6.939e-16 | 4.455e-15 | 0/5 | YES |
| stock \| 3 \| rows | 347 | 347 | 347 | 5/5 | no |
| stock \| 3 \| contending set | energy balance, control effort, slew time, settling time, depth of discharge | - | - | 5/5 | no |
| stock \| 3 \| n_lemma | 5 | 5 | 5 | 5/5 | no |
| stock \| 3 \| largest exponents | energy balance 0.355, control effort 0.336, slew time 0.199 | - | - | 0/5 | YES |
| stock \| 3 \| near-frontier | 47 | 47 | 47 | 5/5 | no |
| stock \| 3 \| reach beta_k | 0.2874 | 0.2872 | 0.2878 | 1/5 | YES |
| stock \| 3 \| share | 0.3333 | 0.3421 | 0.3684 | 0/5 | YES |
| stock \| 3 \| gap G_k | 6.162e-15 | 5.287e-15 | 8.119e-15 | 0/5 | YES |

#### D tau_sweep

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| row 1 \| tau | 3 | 3 | 3 | 5/5 | no |
| primary \| row 1 \| frac_above | 0.4533 | 0.4504 | 0.4533 | 2/5 | YES |
| primary \| row 1 \| n_eff | 588.8 | 588.8 | 589.3 | 1/5 | YES |
| primary \| row 1 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 1 \| largest w | 0.244 | 0.2441 | 0.2451 | 0/5 | YES |
| primary \| row 1 \| largest at | slew time | - | - | 5/5 | no |
| primary \| row 2 \| tau | 5.087 | 5.087 | 5.087 | 5/5 | no |
| primary \| row 2 \| frac_above | 0.4037 | 0.4008 | 0.4037 | 1/5 | YES |
| primary \| row 2 \| n_eff | 462.1 | 462.2 | 462.6 | 0/5 | YES |
| primary \| row 2 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 2 \| largest w | 0.246 | 0.246 | 0.2468 | 2/5 | YES |
| primary \| row 2 \| largest at | slew time | - | - | 5/5 | no |
| primary \| row 3 \| tau | 8.626 | 8.626 | 8.626 | 5/5 | no |
| primary \| row 3 \| frac_above | 0.3314 | 0.3286 | 0.3314 | 3/5 | YES |
| primary \| row 3 \| n_eff | 291 | 291.1 | 291.4 | 0/5 | YES |
| primary \| row 3 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 3 \| largest w | 0.2476 | 0.2477 | 0.2483 | 0/5 | YES |
| primary \| row 3 \| largest at | slew time | - | - | 5/5 | no |
| primary \| row 4 \| tau | 14.63 | 14.63 | 14.63 | 5/5 | no |
| primary \| row 4 \| frac_above | 0.2436 | 0.2422 | 0.245 | 2/5 | YES |
| primary \| row 4 \| n_eff | 137.7 | 137.8 | 137.9 | 0/5 | YES |
| primary \| row 4 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 4 \| largest w | 0.2483 | 0.2483 | 0.2489 | 1/5 | YES |
| primary \| row 4 \| largest at | slew time | - | - | 5/5 | no |
| primary \| row 5 \| tau | 24.8 | 24.8 | 24.8 | 5/5 | no |
| primary \| row 5 \| frac_above | 0.1558 | 0.1544 | 0.1558 | 4/5 | YES |
| primary \| row 5 \| n_eff | 46.9 | 46.72 | 46.83 | 0/5 | YES |
| primary \| row 5 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 5 \| largest w | 0.2462 | 0.2463 | 0.247 | 0/5 | YES |
| primary \| row 5 \| largest at | slew time | - | - | 5/5 | no |
| primary \| row 6 \| tau | 42.06 | 42.06 | 42.06 | 5/5 | no |
| primary \| row 6 \| frac_above | 0.08499 | 0.08499 | 0.08499 | 5/5 | no |
| primary \| row 6 \| n_eff | 12.79 | 12.63 | 12.72 | 0/5 | YES |
| primary \| row 6 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 6 \| largest w | 0.237 | 0.2372 | 0.2381 | 0/5 | YES |
| primary \| row 6 \| largest at | slew time | - | - | 5/5 | no |
| primary \| row 7 \| tau | 71.32 | 71.32 | 71.32 | 5/5 | no |
| primary \| row 7 \| frac_above | 0.04533 | 0.04391 | 0.04533 | 4/5 | YES |
| primary \| row 7 \| n_eff | 5.332 | 5.29 | 5.324 | 0/5 | YES |
| primary \| row 7 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 7 \| largest w | 0.2196 | 0.2196 | 0.2202 | 1/5 | YES |
| primary \| row 7 \| largest at | slew time | - | - | 5/5 | no |
| primary \| row 8 \| tau | 120.9 | 120.9 | 120.9 | 5/5 | no |
| primary \| row 8 \| frac_above | 0.02266 | 0.02266 | 0.02266 | 5/5 | no |
| primary \| row 8 \| n_eff | 3.959 | 3.939 | 3.959 | 1/5 | YES |
| primary \| row 8 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 8 \| largest w | 0.2114 | 0.2108 | 0.2114 | 1/5 | YES |
| primary \| row 8 \| largest at | total mass | - | - | 5/5 | no |
| primary \| row 9 \| tau | 205.1 | 205.1 | 205.1 | 5/5 | no |
| primary \| row 9 \| frac_above | 0.01558 | 0.01558 | 0.01558 | 5/5 | no |
| primary \| row 9 \| n_eff | 3.573 | 3.56 | 3.573 | 1/5 | YES |
| primary \| row 9 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 9 \| largest w | 0.2192 | 0.2187 | 0.2192 | 1/5 | YES |
| primary \| row 9 \| largest at | total mass | - | - | 5/5 | no |
| primary \| row 10 \| tau | 347.8 | 347.8 | 347.8 | 5/5 | no |
| primary \| row 10 \| frac_above | 0.01275 | 0.01275 | 0.01275 | 5/5 | no |
| primary \| row 10 \| n_eff | 3.346 | 3.338 | 3.346 | 1/5 | YES |
| primary \| row 10 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 10 \| largest w | 0.2215 | 0.2212 | 0.2215 | 4/5 | YES |
| primary \| row 10 \| largest at | total mass | - | - | 5/5 | no |
| primary \| row 11 \| tau | 589.7 | 589.7 | 589.7 | 5/5 | no |
| primary \| row 11 \| frac_above | 0.01133 | 0.01133 | 0.01133 | 5/5 | no |
| primary \| row 11 \| n_eff | 3.229 | 3.222 | 3.229 | 1/5 | YES |
| primary \| row 11 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 11 \| largest w | 0.222 | 0.2218 | 0.222 | 4/5 | YES |
| primary \| row 11 \| largest at | total mass | - | - | 5/5 | no |
| primary \| row 12 \| tau | 1000 | 1000 | 1000 | 5/5 | no |
| primary \| row 12 \| frac_above | 0.009915 | 0.009915 | 0.009915 | 5/5 | no |
| primary \| row 12 \| n_eff | 3.197 | 3.189 | 3.197 | 1/5 | YES |
| primary \| row 12 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 12 \| largest w | 0.2222 | 0.222 | 0.2222 | 3/5 | YES |
| primary \| row 12 \| largest at | total mass | - | - | 5/5 | no |
| primary \| row 13 \| tau | inf | inf | inf | 5/5 | no |
| primary \| row 13 \| frac_above | 0 | 0 | 0 | 5/5 | no |
| primary \| row 13 \| n_eff | 3.191 | 3.182 | 3.191 | 1/5 | YES |
| primary \| row 13 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| primary \| row 13 \| largest w | 0.2228 | 0.2228 | 0.2228 | 5/5 | no |
| primary \| row 13 \| largest at | total mass | - | - | 5/5 | no |
| stock \| row 1 \| tau | 3 | 3 | 3 | 5/5 | no |
| stock \| row 1 \| frac_above | 0.45 | 0.45 | 0.45 | 5/5 | no |
| stock \| row 1 \| n_eff | 719.3 | 719.3 | 719.3 | 5/5 | no |
| stock \| row 1 \| metrics with w>1e-3 | 7 | 7 | 7 | 5/5 | no |
| stock \| row 1 \| largest w | 0.417 | 0.417 | 0.417 | 5/5 | no |
| stock \| row 1 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 2 \| tau | 5.087 | 5.087 | 5.087 | 5/5 | no |
| stock \| row 2 \| frac_above | 0.4205 | 0.4205 | 0.4218 | 3/5 | YES |
| stock \| row 2 \| n_eff | 627.7 | 627.7 | 627.7 | 5/5 | no |
| stock \| row 2 \| metrics with w>1e-3 | 7 | 7 | 7 | 5/5 | no |
| stock \| row 2 \| largest w | 0.418 | 0.418 | 0.418 | 5/5 | no |
| stock \| row 2 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 3 \| tau | 8.626 | 8.626 | 8.626 | 5/5 | no |
| stock \| row 3 \| frac_above | 0.3705 | 0.3705 | 0.3705 | 5/5 | no |
| stock \| row 3 \| n_eff | 445.5 | 445.4 | 445.6 | 2/5 | YES |
| stock \| row 3 \| metrics with w>1e-3 | 7 | 7 | 7 | 5/5 | no |
| stock \| row 3 \| largest w | 0.4194 | 0.4194 | 0.4194 | 5/5 | no |
| stock \| row 3 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 4 \| tau | 14.63 | 14.63 | 14.63 | 5/5 | no |
| stock \| row 4 \| frac_above | 0.2897 | 0.2897 | 0.2897 | 5/5 | no |
| stock \| row 4 \| n_eff | 207.5 | 207.5 | 207.6 | 3/5 | YES |
| stock \| row 4 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 4 \| largest w | 0.4212 | 0.4212 | 0.4212 | 5/5 | no |
| stock \| row 4 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 5 \| tau | 24.8 | 24.8 | 24.8 | 5/5 | no |
| stock \| row 5 \| frac_above | 0.1923 | 0.1923 | 0.1923 | 5/5 | no |
| stock \| row 5 \| n_eff | 54.38 | 54.36 | 54.39 | 1/5 | YES |
| stock \| row 5 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 5 \| largest w | 0.4241 | 0.4241 | 0.4241 | 5/5 | no |
| stock \| row 5 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 6 \| tau | 42.06 | 42.06 | 42.06 | 5/5 | no |
| stock \| row 6 \| frac_above | 0.1026 | 0.1026 | 0.1026 | 5/5 | no |
| stock \| row 6 \| n_eff | 14.26 | 14.28 | 14.31 | 0/5 | YES |
| stock \| row 6 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 6 \| largest w | 0.4296 | 0.4296 | 0.4297 | 4/5 | YES |
| stock \| row 6 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 7 \| tau | 71.32 | 71.32 | 71.32 | 5/5 | no |
| stock \| row 7 \| frac_above | 0.03205 | 0.03077 | 0.03205 | 4/5 | YES |
| stock \| row 7 \| n_eff | 8.454 | 8.459 | 8.474 | 0/5 | YES |
| stock \| row 7 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 7 \| largest w | 0.4331 | 0.4331 | 0.4331 | 5/5 | no |
| stock \| row 7 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 8 \| tau | 120.9 | 120.9 | 120.9 | 5/5 | no |
| stock \| row 8 \| frac_above | 0.01923 | 0.01923 | 0.01923 | 5/5 | no |
| stock \| row 8 \| n_eff | 7.344 | 7.333 | 7.343 | 0/5 | YES |
| stock \| row 8 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 8 \| largest w | 0.434 | 0.434 | 0.434 | 5/5 | no |
| stock \| row 8 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 9 \| tau | 205.1 | 205.1 | 205.1 | 5/5 | no |
| stock \| row 9 \| frac_above | 0.01282 | 0.01282 | 0.01282 | 5/5 | no |
| stock \| row 9 \| n_eff | 6.724 | 6.685 | 6.713 | 0/5 | YES |
| stock \| row 9 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 9 \| largest w | 0.4341 | 0.4341 | 0.4342 | 4/5 | YES |
| stock \| row 9 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 10 \| tau | 347.8 | 347.8 | 347.8 | 5/5 | no |
| stock \| row 10 \| frac_above | 0.01154 | 0.01154 | 0.01154 | 5/5 | no |
| stock \| row 10 \| n_eff | 6.106 | 6.019 | 6.085 | 0/5 | YES |
| stock \| row 10 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 10 \| largest w | 0.4341 | 0.4342 | 0.4342 | 0/5 | YES |
| stock \| row 10 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 11 \| tau | 589.7 | 589.7 | 589.7 | 5/5 | no |
| stock \| row 11 \| frac_above | 0.01026 | 0.01026 | 0.01026 | 5/5 | no |
| stock \| row 11 \| n_eff | 5.351 | 5.241 | 5.326 | 0/5 | YES |
| stock \| row 11 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 11 \| largest w | 0.4342 | 0.4342 | 0.4343 | 3/5 | YES |
| stock \| row 11 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 12 \| tau | 1000 | 1000 | 1000 | 5/5 | no |
| stock \| row 12 \| frac_above | 0.01026 | 0.01026 | 0.01026 | 5/5 | no |
| stock \| row 12 \| n_eff | 4.735 | 4.681 | 4.724 | 0/5 | YES |
| stock \| row 12 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 12 \| largest w | 0.4342 | 0.4342 | 0.4343 | 2/5 | YES |
| stock \| row 12 \| largest at | control effort | - | - | 5/5 | no |
| stock \| row 13 \| tau | inf | inf | inf | 5/5 | no |
| stock \| row 13 \| frac_above | 0 | 0 | 0 | 5/5 | no |
| stock \| row 13 \| n_eff | 4.531 | 4.521 | 4.531 | 1/5 | YES |
| stock \| row 13 \| metrics with w>1e-3 | 6 | 6 | 6 | 5/5 | no |
| stock \| row 13 \| largest w | 0.4341 | 0.4342 | 0.4342 | 0/5 | YES |
| stock \| row 13 \| largest at | control effort | - | - | 5/5 | no |

#### D sensitivity

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| baseline \| setting | target 0.1, standard scaler, all | - | - | 5/5 | no |
| primary \| baseline \| tau | 38.1 | 38.1 | 38.1 | 5/5 | no |
| primary \| baseline \| frac_above_ | 0.09632 | 0.09632 | 0.09632 | 5/5 | no |
| primary \| baseline \| n_eff_ | 16.18 | 16 | 16.1 | 0/5 | YES |
| primary \| baseline \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary \| baseline \| contending set | total mass, slew time, energy balance, control effort, pointing error, depth of discharge | - | - | 5/5 | no |
| primary \| baseline \| largest exponent at | slew time | - | - | 5/5 | no |
| primary \| baseline \| shared with baseline | 6 | 6 | 6 | 5/5 | no |
| primary \| target fraction halved \| setting | target 0.05 | - | - | 5/5 | no |
| primary \| target fraction halved \| tau | 65.68 | 65.68 | 65.68 | 5/5 | no |
| primary \| target fraction halved \| frac_above_ | 0.05666 | 0.05382 | 0.05666 | 1/5 | YES |
| primary \| target fraction halved \| n_eff_ | 5.825 | 5.773 | 5.812 | 0/5 | YES |
| primary \| target fraction halved \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary \| target fraction halved \| contending set | total mass, slew time, energy balance, control effort, pointing error, depth of discharge | - | - | 5/5 | no |
| primary \| target fraction halved \| largest exponent at | slew time | - | - | 5/5 | no |
| primary \| target fraction halved \| shared with baseline | 6 | 6 | 6 | 5/5 | no |
| primary \| target fraction doubled \| setting | target 0.2 | - | - | 5/5 | no |
| primary \| target fraction doubled \| tau | 18.43 | 18.43 | 18.43 | 5/5 | no |
| primary \| target fraction doubled \| frac_above_ | 0.1997 | 0.1997 | 0.2011 | 4/5 | YES |
| primary \| target fraction doubled \| n_eff_ | 89.76 | 89.72 | 89.83 | 0/5 | YES |
| primary \| target fraction doubled \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary \| target fraction doubled \| contending set | total mass, slew time, energy balance, control effort, pointing error, depth of discharge | - | - | 5/5 | no |
| primary \| target fraction doubled \| largest exponent at | slew time | - | - | 5/5 | no |
| primary \| target fraction doubled \| shared with baseline | 6 | 6 | 6 | 5/5 | no |
| primary \| robust scaler \| setting | log-IQR scaling | - | - | 5/5 | no |
| primary \| robust scaler \| tau | 54.77 | 54.77 | 54.77 | 5/5 | no |
| primary \| robust scaler \| frac_above_ | 0.1048 | 0.1048 | 0.1048 | 5/5 | no |
| primary \| robust scaler \| n_eff_ | 28.86 | 28.86 | 29.02 | 1/5 | YES |
| primary \| robust scaler \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary \| robust scaler \| contending set | peak slew power, total mass, pointing error, eclipse reserve, energy balance, settling time | - | - | 5/5 | no |
| primary \| robust scaler \| largest exponent at | total mass | - | - | 5/5 | no |
| primary \| robust scaler \| shared with baseline | 3 | 3 | 3 | 5/5 | no |
| primary \| view: four metrics \| setting | 4 attributes | - | - | 5/5 | no |
| primary \| view: four metrics \| tau | 15.37 | 15.37 | 15.37 | 5/5 | no |
| primary \| view: four metrics \| frac_above_ | 0.1091 | 0.1076 | 0.1091 | 3/5 | YES |
| primary \| view: four metrics \| n_eff_ | 20.64 | 20.33 | 20.61 | 0/5 | YES |
| primary \| view: four metrics \| n_lemma | 4 | 4 | 4 | 5/5 | no |
| primary \| view: four metrics \| contending set | control effort, slew time, pointing error, total mass | - | - | 5/5 | no |
| primary \| view: four metrics \| largest exponent at | control effort | - | - | 5/5 | no |
| primary \| view: four metrics \| shared with baseline | 4 | 4 | 4 | 5/5 | no |
| primary \| view: settling time and slew time \| setting | 2 attributes | - | - | 5/5 | no |
| primary \| view: settling time and slew time \| tau | 6.201 | 6.201 | 6.201 | 5/5 | no |
| primary \| view: settling time and slew time \| frac_above_ | 0.09773 | 0.09773 | 0.09773 | 5/5 | no |
| primary \| view: settling time and slew time \| n_eff_ | 23.96 | 23.43 | 24.29 | 0/5 | YES |
| primary \| view: settling time and slew time \| n_lemma | 2 | 2 | 2 | 5/5 | no |
| primary \| view: settling time and slew time \| contending set | slew time, settling time | - | - | 5/5 | no |
| primary \| view: settling time and slew time \| largest exponent at | settling time | - | - | 5/5 | no |
| primary \| view: settling time and slew time \| shared with baseline | 1 | 1 | 1 | 5/5 | no |
| stock \| baseline \| setting | target 0.1, standard scaler, all | - | - | 5/5 | no |
| stock \| baseline \| tau | 41.72 | 41.72 | 41.72 | 5/5 | no |
| stock \| baseline \| frac_above_ | 0.1038 | 0.1038 | 0.1051 | 3/5 | YES |
| stock \| baseline \| n_eff_ | 14.48 | 14.5 | 14.53 | 0/5 | YES |
| stock \| baseline \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| stock \| baseline \| contending set | control effort, slew time, power margin, settling time, pointing error, eclipse reserve | - | - | 5/5 | no |
| stock \| baseline \| largest exponent at | control effort | - | - | 5/5 | no |
| stock \| baseline \| shared with baseline | 6 | 6 | 6 | 5/5 | no |
| stock \| target fraction halved \| setting | target 0.05 | - | - | 5/5 | no |
| stock \| target fraction halved \| tau | 54.77 | 54.77 | 54.77 | 5/5 | no |
| stock \| target fraction halved \| frac_above_ | 0.05769 | 0.05641 | 0.05769 | 1/5 | YES |
| stock \| target fraction halved \| n_eff_ | 9.96 | 9.97 | 9.993 | 0/5 | YES |
| stock \| target fraction halved \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| stock \| target fraction halved \| contending set | control effort, slew time, power margin, settling time, pointing error, eclipse reserve | - | - | 5/5 | no |
| stock \| target fraction halved \| largest exponent at | control effort | - | - | 5/5 | no |
| stock \| target fraction halved \| shared with baseline | 6 | 6 | 6 | 5/5 | no |
| stock \| target fraction doubled \| setting | target 0.2 | - | - | 5/5 | no |
| stock \| target fraction doubled \| tau | 24.2 | 24.2 | 24.2 | 5/5 | no |
| stock \| target fraction doubled \| frac_above_ | 0.1974 | 0.1974 | 0.1974 | 5/5 | no |
| stock \| target fraction doubled \| n_eff_ | 58.48 | 58.46 | 58.5 | 0/5 | YES |
| stock \| target fraction doubled \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| stock \| target fraction doubled \| contending set | control effort, slew time, power margin, settling time, pointing error, eclipse reserve | - | - | 5/5 | no |
| stock \| target fraction doubled \| largest exponent at | control effort | - | - | 5/5 | no |
| stock \| target fraction doubled \| shared with baseline | 6 | 6 | 6 | 5/5 | no |
| stock \| robust scaler \| setting | log-IQR scaling | - | - | 5/5 | no |
| stock \| robust scaler \| tau | 59.98 | 59.98 | 59.98 | 5/5 | no |
| stock \| robust scaler \| frac_above_ | 0.1013 | 0.1 | 0.1013 | 4/5 | YES |
| stock \| robust scaler \| n_eff_ | 9.588 | 9.579 | 9.609 | 0/5 | YES |
| stock \| robust scaler \| n_lemma | 5 | 5 | 5 | 5/5 | no |
| stock \| robust scaler \| contending set | control effort, slew time, energy balance, pointing error, eclipse reserve | - | - | 5/5 | no |
| stock \| robust scaler \| largest exponent at | control effort | - | - | 5/5 | no |
| stock \| robust scaler \| shared with baseline | 4 | 4 | 4 | 5/5 | no |
| stock \| view: four metrics \| setting | 4 attributes | - | - | 5/5 | no |
| stock \| view: four metrics \| tau | 22.1 | 22.1 | 22.1 | 5/5 | no |
| stock \| view: four metrics \| frac_above_ | 0.09744 | 0.09744 | 0.09744 | 5/5 | no |
| stock \| view: four metrics \| n_eff_ | 14.97 | 14.92 | 14.97 | 2/5 | YES |
| stock \| view: four metrics \| n_lemma | 2 | 2 | 2 | 5/5 | no |
| stock \| view: four metrics \| contending set | control effort, slew time | - | - | 5/5 | no |
| stock \| view: four metrics \| largest exponent at | control effort | - | - | 5/5 | no |
| stock \| view: four metrics \| shared with baseline | 2 | 2 | 2 | 5/5 | no |
| stock \| view: settling time and slew time \| setting | 2 attributes | - | - | 5/5 | no |
| stock \| view: settling time and slew time \| tau | 4.313 | 4.313 | 4.313 | 5/5 | no |
| stock \| view: settling time and slew time \| frac_above_ | 0.1077 | 0.1077 | 0.109 | 4/5 | YES |
| stock \| view: settling time and slew time \| n_eff_ | 20.47 | 20.26 | 20.57 | 0/5 | YES |
| stock \| view: settling time and slew time \| n_lemma | 2 | 2 | 2 | 5/5 | no |
| stock \| view: settling time and slew time \| contending set | slew time, settling time | - | - | 5/5 | no |
| stock \| view: settling time and slew time \| largest exponent at | slew time | - | - | 5/5 | no |
| stock \| view: settling time and slew time \| shared with baseline | 2 | 2 | 2 | 5/5 | no |

#### D refits

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| small \| designs | 191 | 191 | 191 | 5/5 | no |
| primary \| small \| tau | 336.5 | 336.5 | 336.5 | 5/5 | no |
| primary \| small \| frac_above_ | 0.09424 | 0.09424 | 0.09424 | 5/5 | no |
| primary \| small \| n_eff_ | 5.467 | 5.467 | 5.467 | 5/5 | no |
| primary \| small \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| primary \| small \| contending set | pointing error, total mass, peak slew power, depth of discharge, power margin, control effort | - | - | 5/5 | no |
| primary \| small \| largest exponent at | pointing error | - | - | 5/5 | no |
| primary \| medium \| designs | 248 | 248 | 248 | 5/5 | no |
| primary \| medium \| tau | 135.8 | 124 | 135.8 | 4/5 | YES |
| primary \| medium \| frac_above_ | 0.09677 | 0.09677 | 0.1048 | 4/5 | YES |
| primary \| medium \| n_eff_ | 9.442 | 9.424 | 9.915 | 0/5 | YES |
| primary \| medium \| n_lemma | 7 | 7 | 7 | 5/5 | no |
| primary \| medium \| contending set | pointing error, peak slew power, total mass, depth of discharge, power margin, control effort, slew time | - | - | 5/5 | no |
| primary \| medium \| largest exponent at | pointing error | - | - | 5/5 | no |
| primary \| large \| designs | 267 | 267 | 267 | 5/5 | no |
| primary \| large \| tau | 113.2 | 113.2 | 113.2 | 5/5 | no |
| primary \| large \| frac_above_ | 0.1086 | 0.1086 | 0.1086 | 5/5 | no |
| primary \| large \| n_eff_ | 14.97 | 14.99 | 15.21 | 0/5 | YES |
| primary \| large \| n_lemma | 7 | 7 | 7 | 5/5 | no |
| primary \| large \| contending set | power margin, total mass, pointing error, depth of discharge, control effort, peak slew power, slew time | - | - | 5/5 | no |
| primary \| large \| largest exponent at | power margin | - | - | 5/5 | no |
| stock \| small \| designs | 239 | 239 | 239 | 5/5 | no |
| stock \| small \| tau | 113.2 | 113.2 | 113.2 | 5/5 | no |
| stock \| small \| frac_above_ | 0.1004 | 0.09623 | 0.1004 | 4/5 | YES |
| stock \| small \| n_eff_ | 11.27 | 11.23 | 11.31 | 0/5 | YES |
| stock \| small \| n_lemma | 7 | 7 | 7 | 5/5 | no |
| stock \| small \| contending set | control effort, slew time, power margin, total mass, pointing error, depth of discharge, eclipse reserve | - | - | 5/5 | no |
| stock \| small \| largest exponent at | control effort | - | - | 5/5 | no |
| stock \| medium \| designs | 279 | 279 | 279 | 5/5 | no |
| stock \| medium \| tau | 78.75 | 65.68 | 78.75 | 3/5 | YES |
| stock \| medium \| frac_above_ | 0.09319 | 0.09319 | 0.1039 | 3/5 | YES |
| stock \| medium \| n_eff_ | 11.25 | 11.24 | 13.49 | 1/5 | YES |
| stock \| medium \| n_lemma | 6 | 6 | 6 | 5/5 | no |
| stock \| medium \| contending set | control effort, slew time, power margin, pointing error, depth of discharge, total mass | - | - | 5/5 | no |
| stock \| medium \| largest exponent at | control effort | - | - | 5/5 | no |
| stock \| large \| designs | 262 | 262 | 262 | 5/5 | no |
| stock \| large \| tau | 78.75 | 78.75 | 78.75 | 5/5 | no |
| stock \| large \| frac_above_ | 0.1069 | 0.1031 | 0.1069 | 4/5 | YES |
| stock \| large \| n_eff_ | 12.28 | 12.27 | 12.3 | 1/5 | YES |
| stock \| large \| n_lemma | 7 | 7 | 7 | 5/5 | no |
| stock \| large \| contending set | control effort, power margin, slew time, settling time, total mass, pointing error, depth of discharge | - | - | 5/5 | no |
| stock \| large \| largest exponent at | control effort | - | - | 5/5 | no |

#### tension

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| primary \| settling time, total mass \| pearson sign | - | - | - | 5/5 | no |
| primary \| settling time, total mass \| spearman sign | - | - | - | 5/5 | no |
| primary \| settling time, total mass \| pearson | -0.5418 | -0.5418 | -0.5413 | 1/5 | YES |
| primary \| settling time, total mass \| spearman | -0.3369 | -0.3387 | -0.3317 | 0/5 | YES |
| primary \| slew time, total mass \| pearson sign | - | - | - | 5/5 | no |
| primary \| slew time, total mass \| spearman sign | - | - | - | 5/5 | no |
| primary \| slew time, total mass \| pearson | -0.4816 | -0.4816 | -0.4795 | 2/5 | YES |
| primary \| slew time, total mass \| spearman | -0.3337 | -0.338 | -0.3337 | 4/5 | YES |
| primary \| pointing error, control effort \| pearson sign | - | - | - | 5/5 | no |
| primary \| pointing error, control effort \| spearman sign | - | - | - | 5/5 | no |
| primary \| pointing error, control effort \| pearson | -0.3574 | -0.3577 | -0.3574 | 4/5 | YES |
| primary \| pointing error, control effort \| spearman | -0.4815 | -0.4815 | -0.4752 | 4/5 | YES |
| primary \| settling time, pointing error \| pearson sign | + | - | - | 5/5 | no |
| primary \| settling time, pointing error \| spearman sign | + | - | - | 5/5 | no |
| primary \| settling time, pointing error \| pearson | 0.1809 | 0.179 | 0.181 | 0/5 | YES |
| primary \| settling time, pointing error \| spearman | 0.2001 | 0.194 | 0.1976 | 0/5 | YES |
| primary \| slew time, control effort \| pearson sign | - | - | - | 5/5 | no |
| primary \| slew time, control effort \| spearman sign | - | - | - | 5/5 | no |
| primary \| slew time, control effort \| pearson | -0.8733 | -0.8733 | -0.8717 | 4/5 | YES |
| primary \| slew time, control effort \| spearman | -0.8315 | -0.8386 | -0.8315 | 4/5 | YES |
| primary \| settling time, slew time \| pearson sign | + | - | - | 5/5 | no |
| primary \| settling time, slew time \| spearman sign | + | - | - | 5/5 | no |
| primary \| settling time, slew time \| pearson | 0.9064 | 0.9006 | 0.9065 | 2/5 | YES |
| primary \| settling time, slew time \| spearman | 0.875 | 0.8735 | 0.8757 | 0/5 | YES |
| stock \| settling time, total mass \| pearson sign | - | - | - | 5/5 | no |
| stock \| settling time, total mass \| spearman sign | - | - | - | 5/5 | no |
| stock \| settling time, total mass \| pearson | -0.1191 | -0.1192 | -0.1189 | 0/5 | YES |
| stock \| settling time, total mass \| spearman | -0.02058 | -0.02099 | -0.0198 | 0/5 | YES |
| stock \| slew time, total mass \| pearson sign | - | - | - | 5/5 | no |
| stock \| slew time, total mass \| spearman sign | - | - | - | 5/5 | no |
| stock \| slew time, total mass \| pearson | -0.1001 | -0.1002 | -0.1 | 0/5 | YES |
| stock \| slew time, total mass \| spearman | -0.03441 | -0.03452 | -0.03408 | 2/5 | YES |
| stock \| pointing error, control effort \| pearson sign | - | - | - | 5/5 | no |
| stock \| pointing error, control effort \| spearman sign | - | - | - | 5/5 | no |
| stock \| pointing error, control effort \| pearson | -0.702 | -0.702 | -0.702 | 5/5 | no |
| stock \| pointing error, control effort \| spearman | -0.7689 | -0.7689 | -0.7689 | 5/5 | no |
| stock \| settling time, pointing error \| pearson sign | + | - | - | 5/5 | no |
| stock \| settling time, pointing error \| spearman sign | + | - | - | 5/5 | no |
| stock \| settling time, pointing error \| pearson | 0.686 | 0.6857 | 0.6861 | 1/5 | YES |
| stock \| settling time, pointing error \| spearman | 0.7463 | 0.7453 | 0.7471 | 0/5 | YES |
| stock \| slew time, control effort \| pearson sign | - | - | - | 5/5 | no |
| stock \| slew time, control effort \| spearman sign | - | - | - | 5/5 | no |
| stock \| slew time, control effort \| pearson | -0.9589 | -0.9589 | -0.9589 | 5/5 | no |
| stock \| slew time, control effort \| spearman | -0.9542 | -0.9542 | -0.9539 | 3/5 | YES |
| stock \| settling time, slew time \| pearson sign | + | - | - | 5/5 | no |
| stock \| settling time, slew time \| spearman sign | + | - | - | 5/5 | no |
| stock \| settling time, slew time \| pearson | 0.9852 | 0.9852 | 0.9852 | 5/5 | no |
| stock \| settling time, slew time \| spearman | 0.9928 | 0.9926 | 0.9929 | 0/5 | YES |

#### candidate

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| fast_effort_hungry \| wheel_class | large | - | - | 5/5 | no |
| fast_effort_hungry \| st_grade | medium | - | - | 5/5 | no |
| fast_effort_hungry \| log V | -0.115 | -0.1152 | -0.1147 | 0/5 | YES |
| fast_effort_hungry \| novelty V-1 | -0.1086 | -0.1088 | -0.1084 | 0/5 | YES |
| fast_effort_hungry \| rank among training | 0.6686 | 0.6657 | 0.6686 | 2/5 | YES |
| fast_effort_hungry \| tau*log V | -4.381 | -4.388 | -4.37 | 0/5 | YES |
| precise_heavy_sensor \| wheel_class | large | - | - | 5/5 | no |
| precise_heavy_sensor \| st_grade | fine | - | - | 5/5 | no |
| precise_heavy_sensor \| log V | -0.07174 | -0.07123 | -0.07054 | 0/5 | YES |
| precise_heavy_sensor \| novelty V-1 | -0.06923 | -0.06875 | -0.06811 | 0/5 | YES |
| precise_heavy_sensor \| rank among training | 0.772 | 0.7748 | 0.7776 | 0/5 | YES |
| precise_heavy_sensor \| tau*log V | -2.733 | -2.714 | -2.687 | 0/5 | YES |
| light_slow \| wheel_class | small | - | - | 5/5 | no |
| light_slow \| st_grade | coarse | - | - | 5/5 | no |
| light_slow \| log V | -0.1436 | -0.1441 | -0.1438 | 0/5 | YES |
| light_slow \| novelty V-1 | -0.1338 | -0.1342 | -0.134 | 0/5 | YES |
| light_slow \| rank among training | 0.5949 | 0.5921 | 0.5949 | 2/5 | YES |
| light_slow \| tau*log V | -5.471 | -5.49 | -5.479 | 0/5 | YES |

#### predict

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| regressor \| tau | 15.37 | 15.37 | 15.37 | 5/5 | no |
| proposal_1 \| predicted log V | -0.06901 | -0.06901 | -0.06901 | 5/5 | no |
| proposal_1 \| measured log V | -0.09002 | -0.09057 | -0.08924 | 0/5 | YES |
| proposal_1 \| difference | -0.02101 | -0.02156 | -0.02022 | 0/5 | YES |
| proposal_1 \| \|diff\| / band | 0.3229 | 0.3108 | 0.3314 | 0/5 | YES |
| proposal_1 \| log V within band | True | - | - | 5/5 | no |
| proposal_1 \| \|\|dZ\|\| | 0.08802 | 0.08853 | 0.09074 | 0/5 | YES |
| proposal_1 \| \|\|dZ\|\| / band | 1.353 | 1.361 | 1.395 | 0/5 | YES |
| proposal_1 \| Z within band | False | - | - | 5/5 | no |
| proposal_2 \| predicted log V | -0.05764 | -0.05764 | -0.05764 | 5/5 | no |
| proposal_2 \| measured log V | -0.07974 | -0.08074 | -0.07877 | 1/5 | YES |
| proposal_2 \| difference | -0.0221 | -0.0231 | -0.02113 | 1/5 | YES |
| proposal_2 \| \|diff\| / band | 0.3397 | 0.3248 | 0.3551 | 1/5 | YES |
| proposal_2 \| log V within band | True | - | - | 5/5 | no |
| proposal_2 \| \|\|dZ\|\| | 0.1439 | 0.1439 | 0.1445 | 4/5 | YES |
| proposal_2 \| \|\|dZ\|\| / band | 2.211 | 2.211 | 2.222 | 1/5 | YES |
| proposal_2 \| Z within band | False | - | - | 5/5 | no |
| proposal_3 \| predicted log V | -0.1624 | -0.1624 | -0.1624 | 5/5 | no |
| proposal_3 \| measured log V | -0.2084 | -0.2109 | -0.2078 | 0/5 | YES |
| proposal_3 \| difference | -0.04593 | -0.04848 | -0.04539 | 0/5 | YES |
| proposal_3 \| \|diff\| / band | 0.706 | 0.6977 | 0.7451 | 0/5 | YES |
| proposal_3 \| log V within band | True | - | - | 5/5 | no |
| proposal_3 \| \|\|dZ\|\| | 0.2007 | 0.2007 | 0.2017 | 2/5 | YES |
| proposal_3 \| \|\|dZ\|\| / band | 3.085 | 3.085 | 3.1 | 2/5 | YES |
| proposal_3 \| Z within band | False | - | - | 5/5 | no |
| proposal_1 \| outcome | log V pass, position miss | - | - | 5/5 | no |
| proposal_2 \| outcome | log V pass, position miss | - | - | 5/5 | no |
| proposal_3 \| outcome | log V pass, position miss | - | - | 5/5 | no |

#### predict, committed checks

| quantity | committed | min | max | regenerations printing as committed | changes at printed precision |
|---|---|---|---|---|---|
| proposal_1 \| predicted log V | -0.06901 | -0.06901 | -0.06901 | 5/5 | no |
| proposal_1 \| measured log V | -0.09002 | -0.09035 | -0.08918 | 0/5 | YES |
| proposal_1 \| difference | -0.02101 | -0.02134 | -0.02017 | 0/5 | YES |
| proposal_1 \| \|diff\| / band | 0.3229 | 0.31 | 0.328 | 0/5 | YES |
| proposal_1 \| log V within band | True | - | - | 5/5 | no |
| proposal_1 \| \|\|dZ\|\| | 0.08802 | 0.08793 | 0.09033 | 0/5 | YES |
| proposal_1 \| \|\|dZ\|\| / band | 1.353 | 1.352 | 1.388 | 0/5 | YES |
| proposal_1 \| Z within band | False | - | - | 5/5 | no |
| proposal_2 \| predicted log V | -0.05764 | -0.05764 | -0.05764 | 5/5 | no |
| proposal_2 \| measured log V | -0.07974 | -0.08074 | -0.07877 | 1/5 | YES |
| proposal_2 \| difference | -0.0221 | -0.02311 | -0.02113 | 1/5 | YES |
| proposal_2 \| \|diff\| / band | 0.3397 | 0.3248 | 0.3551 | 1/5 | YES |
| proposal_2 \| log V within band | True | - | - | 5/5 | no |
| proposal_2 \| \|\|dZ\|\| | 0.1439 | 0.1439 | 0.1445 | 4/5 | YES |
| proposal_2 \| \|\|dZ\|\| / band | 2.211 | 2.211 | 2.222 | 1/5 | YES |
| proposal_2 \| Z within band | False | - | - | 5/5 | no |
| proposal_3 \| predicted log V | -0.1624 | -0.1624 | -0.1624 | 5/5 | no |
| proposal_3 \| measured log V | -0.2084 | -0.2109 | -0.2078 | 0/5 | YES |
| proposal_3 \| difference | -0.04593 | -0.04848 | -0.04539 | 0/5 | YES |
| proposal_3 \| \|diff\| / band | 0.706 | 0.6977 | 0.7451 | 0/5 | YES |
| proposal_3 \| log V within band | True | - | - | 5/5 | no |
| proposal_3 \| \|\|dZ\|\| | 0.2007 | 0.2007 | 0.2017 | 2/5 | YES |
| proposal_3 \| \|\|dZ\|\| / band | 3.085 | 3.085 | 3.1 | 2/5 | YES |
| proposal_3 \| Z within band | False | - | - | 5/5 | no |
| proposal_1 \| outcome | log V pass, position miss | - | - | 5/5 | no |
| proposal_2 \| outcome | log V pass, position miss | - | - | 5/5 | no |
| proposal_3 \| outcome | log V pass, position miss | - | - | 5/5 | no |

Quantities compared: 740; changing at the printed precision: 328.

Those that change: `sentence | nondominated | text`; `sentence | temperature | text`; `sentence | K sweep | text`; `sentence | certificate | text`; `regime | tau, frac_above_, n_eff_ | primary`; `regime | tau, frac_above_, n_eff_ | stock`; `regime | band 1/tau, near-frontier designs | primary`; `regime | settling time, total mass | primary`; `regime | slew time, total mass | primary`; `regime | settling time, pointing error | primary`; `regime | slew time, control effort | primary`; `regime | settling time, slew time | primary`; `fit | primary K=1 | n_eff_`; `certificate | primary | 1 | max gap`; `certificate | primary | 1 | bound`; `certificate | primary | 2 | max gap`; `certificate | primary | 2 | gamma`; `certificate | primary | 2 | radius`; `certificate | primary | 2 | bound`; `certificate | primary | 3 | max gap`; `certificate | primary | 3 | gamma`; `certificate | primary | 3 | radius`; `certificate | primary | 3 | bound`; `nondominated | primary | four metrics | nondominated`; `nondominated | primary | four metrics | share`; `nondominated | primary | settling time and slew time | nondominated`; `nondominated | primary | settling time and slew time | share`; `D k_table | primary | 1 | objective_`; `D k_table | primary | 1 | max gap`; `D k_table | primary | 1 | bound`; `D k_table | primary | 2 | objective_`; `D k_table | primary | 2 | frac_above_`; `D k_table | primary | 2 | facet rows`; `D k_table | primary | 2 | facet shares`; `D k_table | primary | 2 | max gap`; `D k_table | primary | 2 | gamma`; `D k_table | primary | 2 | radius`; `D k_table | primary | 2 | bound`; `D k_table | primary | 3 | objective_`; `D k_table | primary | 3 | frac_above_`; `D k_table | primary | 3 | facet rows`; `D k_table | primary | 3 | facet shares`; `D k_table | primary | 3 | max gap`; `D k_table | primary | 3 | gamma`; `D k_table | primary | 3 | radius`; `D k_table | primary | 3 | bound`; `D exponents K=1 | primary | settling time | exponent w`; `D exponents K=1 | primary | slew time | exponent w`; `D exponents K=1 | primary | pointing error | exponent w`; `D exponents K=1 | primary | total mass | exponent w`; `D exponents K=1 | primary | control effort | exponent w`; `D exponents K=1 | primary | power margin | exponent w`; `D exponents K=1 | primary | energy balance | exponent w`; `D exponents K=1 | primary | eclipse reserve | exponent w`; `D exponents K=1 | primary | peak slew power | exponent w`; `D exponents K=1 | primary | depth of discharge | exponent w`; `D exponents K=3 | primary | settling time | facet 1`; `D exponents K=3 | primary | settling time | facet 2`; `D exponents K=3 | primary | settling time | facet 3`; `D exponents K=3 | primary | slew time | facet 1`; `D exponents K=3 | primary | slew time | facet 2`; `D exponents K=3 | primary | slew time | facet 3`; `D exponents K=3 | primary | pointing error | facet 1`; `D exponents K=3 | primary | pointing error | facet 2`; `D exponents K=3 | primary | pointing error | facet 3`; `D exponents K=3 | primary | total mass | facet 1`; `D exponents K=3 | primary | total mass | facet 2`; `D exponents K=3 | primary | total mass | facet 3`; `D exponents K=3 | primary | control effort | facet 1`; `D exponents K=3 | primary | control effort | facet 2`; `D exponents K=3 | primary | control effort | facet 3`; `D exponents K=3 | primary | power margin | facet 1`; `D exponents K=3 | primary | power margin | facet 2`; `D exponents K=3 | primary | power margin | facet 3`; `D exponents K=3 | primary | energy balance | facet 1`; `D exponents K=3 | primary | energy balance | facet 2`; `D exponents K=3 | primary | energy balance | facet 3`; `D exponents K=3 | primary | eclipse reserve | facet 1`; `D exponents K=3 | primary | eclipse reserve | facet 2`; `D exponents K=3 | primary | eclipse reserve | facet 3`; `D exponents K=3 | primary | peak slew power | facet 1`; `D exponents K=3 | primary | peak slew power | facet 2`; `D exponents K=3 | primary | peak slew power | facet 3`; `D exponents K=3 | primary | depth of discharge | facet 1`; `D exponents K=3 | primary | depth of discharge | facet 2`; `D exponents K=3 | primary | depth of discharge | facet 3`; `D facets K=3 | primary | 1 | rows`; `D facets K=3 | primary | 1 | largest exponents`; `D facets K=3 | primary | 1 | near-frontier`; `D facets K=3 | primary | 1 | reach beta_k`; `D facets K=3 | primary | 1 | share`; `D facets K=3 | primary | 1 | gap G_k`; `D facets K=3 | primary | 2 | rows`; `D facets K=3 | primary | 2 | largest exponents`; `D facets K=3 | primary | 2 | reach beta_k`; `D facets K=3 | primary | 2 | share`; `D facets K=3 | primary | 2 | gap G_k`; `D facets K=3 | primary | 3 | largest exponents`; `D facets K=3 | primary | 3 | near-frontier`; `D facets K=3 | primary | 3 | reach beta_k`; `D facets K=3 | primary | 3 | share`; `D facets K=3 | primary | 3 | gap G_k`; `D tau_sweep | primary | row 1 | frac_above`; `D tau_sweep | primary | row 1 | n_eff`; `D tau_sweep | primary | row 1 | largest w`; `D tau_sweep | primary | row 2 | frac_above`; `D tau_sweep | primary | row 2 | n_eff`; `D tau_sweep | primary | row 2 | largest w`; `D tau_sweep | primary | row 3 | frac_above`; `D tau_sweep | primary | row 3 | n_eff`; `D tau_sweep | primary | row 3 | largest w`; `D tau_sweep | primary | row 4 | frac_above`; `D tau_sweep | primary | row 4 | n_eff`; `D tau_sweep | primary | row 4 | largest w`; `D tau_sweep | primary | row 5 | frac_above`; `D tau_sweep | primary | row 5 | n_eff`; `D tau_sweep | primary | row 5 | largest w`; `D tau_sweep | primary | row 6 | n_eff`; `D tau_sweep | primary | row 6 | largest w`; `D tau_sweep | primary | row 7 | frac_above`; `D tau_sweep | primary | row 7 | n_eff`; `D tau_sweep | primary | row 7 | largest w`; `D tau_sweep | primary | row 8 | n_eff`; `D tau_sweep | primary | row 8 | largest w`; `D tau_sweep | primary | row 9 | n_eff`; `D tau_sweep | primary | row 9 | largest w`; `D tau_sweep | primary | row 10 | n_eff`; `D tau_sweep | primary | row 10 | largest w`; `D tau_sweep | primary | row 11 | n_eff`; `D tau_sweep | primary | row 11 | largest w`; `D tau_sweep | primary | row 12 | n_eff`; `D tau_sweep | primary | row 12 | largest w`; `D tau_sweep | primary | row 13 | n_eff`; `D sensitivity | primary | baseline | n_eff_`; `D sensitivity | primary | target fraction halved | frac_above_`; `D sensitivity | primary | target fraction halved | n_eff_`; `D sensitivity | primary | target fraction doubled | frac_above_`; `D sensitivity | primary | target fraction doubled | n_eff_`; `D sensitivity | primary | robust scaler | n_eff_`; `D sensitivity | primary | view: four metrics | frac_above_`; `D sensitivity | primary | view: four metrics | n_eff_`; `D sensitivity | primary | view: settling time and slew time | n_eff_`; `D refits | primary | medium | tau`; `D refits | primary | medium | frac_above_`; `D refits | primary | medium | n_eff_`; `D refits | primary | large | n_eff_`; `fit | stock K=1 | frac_above_`; `fit | stock K=1 | n_eff_`; `certificate | stock | 1 | max gap`; `certificate | stock | 1 | bound`; `certificate | stock | 2 | max gap`; `certificate | stock | 2 | gamma`; `certificate | stock | 2 | radius`; `certificate | stock | 2 | bound`; `certificate | stock | 3 | max gap`; `certificate | stock | 3 | gamma`; `certificate | stock | 3 | radius`; `certificate | stock | 3 | bound`; `nondominated | stock | four metrics | nondominated`; `nondominated | stock | four metrics | share`; `D k_table | stock | 1 | frac_above_`; `D k_table | stock | 1 | max gap`; `D k_table | stock | 1 | bound`; `D k_table | stock | 2 | frac_above_`; `D k_table | stock | 2 | facet shares`; `D k_table | stock | 2 | max gap`; `D k_table | stock | 2 | gamma`; `D k_table | stock | 2 | radius`; `D k_table | stock | 2 | bound`; `D k_table | stock | 3 | objective_`; `D k_table | stock | 3 | frac_above_`; `D k_table | stock | 3 | facet shares`; `D k_table | stock | 3 | max gap`; `D k_table | stock | 3 | gamma`; `D k_table | stock | 3 | radius`; `D k_table | stock | 3 | bound`; `D exponents K=1 | stock | settling time | exponent w`; `D exponents K=1 | stock | slew time | exponent w`; `D exponents K=1 | stock | pointing error | exponent w`; `D exponents K=1 | stock | total mass | exponent w`; `D exponents K=1 | stock | control effort | exponent w`; `D exponents K=1 | stock | energy balance | exponent w`; `D exponents K=1 | stock | eclipse reserve | exponent w`; `D exponents K=1 | stock | peak slew power | exponent w`; `D exponents K=1 | stock | depth of discharge | exponent w`; `D exponents K=3 | stock | settling time | facet 1`; `D exponents K=3 | stock | settling time | facet 2`; `D exponents K=3 | stock | settling time | facet 3`; `D exponents K=3 | stock | slew time | facet 1`; `D exponents K=3 | stock | slew time | facet 2`; `D exponents K=3 | stock | slew time | facet 3`; `D exponents K=3 | stock | pointing error | facet 1`; `D exponents K=3 | stock | pointing error | facet 2`; `D exponents K=3 | stock | pointing error | facet 3`; `D exponents K=3 | stock | total mass | facet 1`; `D exponents K=3 | stock | total mass | facet 2`; `D exponents K=3 | stock | total mass | facet 3`; `D exponents K=3 | stock | control effort | facet 1`; `D exponents K=3 | stock | control effort | facet 2`; `D exponents K=3 | stock | control effort | facet 3`; `D exponents K=3 | stock | power margin | facet 1`; `D exponents K=3 | stock | power margin | facet 2`; `D exponents K=3 | stock | power margin | facet 3`; `D exponents K=3 | stock | energy balance | facet 1`; `D exponents K=3 | stock | energy balance | facet 2`; `D exponents K=3 | stock | energy balance | facet 3`; `D exponents K=3 | stock | eclipse reserve | facet 1`; `D exponents K=3 | stock | eclipse reserve | facet 2`; `D exponents K=3 | stock | eclipse reserve | facet 3`; `D exponents K=3 | stock | peak slew power | facet 1`; `D exponents K=3 | stock | peak slew power | facet 2`; `D exponents K=3 | stock | peak slew power | facet 3`; `D exponents K=3 | stock | depth of discharge | facet 1`; `D exponents K=3 | stock | depth of discharge | facet 2`; `D exponents K=3 | stock | depth of discharge | facet 3`; `D facets K=3 | stock | 1 | largest exponents`; `D facets K=3 | stock | 1 | near-frontier`; `D facets K=3 | stock | 1 | reach beta_k`; `D facets K=3 | stock | 1 | share`; `D facets K=3 | stock | 1 | gap G_k`; `D facets K=3 | stock | 2 | largest exponents`; `D facets K=3 | stock | 2 | near-frontier`; `D facets K=3 | stock | 2 | reach beta_k`; `D facets K=3 | stock | 2 | share`; `D facets K=3 | stock | 2 | gap G_k`; `D facets K=3 | stock | 3 | largest exponents`; `D facets K=3 | stock | 3 | reach beta_k`; `D facets K=3 | stock | 3 | share`; `D facets K=3 | stock | 3 | gap G_k`; `D tau_sweep | stock | row 2 | frac_above`; `D tau_sweep | stock | row 3 | n_eff`; `D tau_sweep | stock | row 4 | n_eff`; `D tau_sweep | stock | row 5 | n_eff`; `D tau_sweep | stock | row 6 | n_eff`; `D tau_sweep | stock | row 6 | largest w`; `D tau_sweep | stock | row 7 | frac_above`; `D tau_sweep | stock | row 7 | n_eff`; `D tau_sweep | stock | row 8 | n_eff`; `D tau_sweep | stock | row 9 | n_eff`; `D tau_sweep | stock | row 9 | largest w`; `D tau_sweep | stock | row 10 | n_eff`; `D tau_sweep | stock | row 10 | largest w`; `D tau_sweep | stock | row 11 | n_eff`; `D tau_sweep | stock | row 11 | largest w`; `D tau_sweep | stock | row 12 | n_eff`; `D tau_sweep | stock | row 12 | largest w`; `D tau_sweep | stock | row 13 | n_eff`; `D tau_sweep | stock | row 13 | largest w`; `D sensitivity | stock | baseline | frac_above_`; `D sensitivity | stock | baseline | n_eff_`; `D sensitivity | stock | target fraction halved | frac_above_`; `D sensitivity | stock | target fraction halved | n_eff_`; `D sensitivity | stock | target fraction doubled | n_eff_`; `D sensitivity | stock | robust scaler | frac_above_`; `D sensitivity | stock | robust scaler | n_eff_`; `D sensitivity | stock | view: four metrics | n_eff_`; `D sensitivity | stock | view: settling time and slew time | frac_above_`; `D sensitivity | stock | view: settling time and slew time | n_eff_`; `D refits | stock | small | frac_above_`; `D refits | stock | small | n_eff_`; `D refits | stock | medium | tau`; `D refits | stock | medium | frac_above_`; `D refits | stock | medium | n_eff_`; `D refits | stock | large | frac_above_`; `D refits | stock | large | n_eff_`; `tension | primary | settling time, total mass | pearson`; `tension | primary | settling time, total mass | spearman`; `tension | primary | slew time, total mass | pearson`; `tension | primary | slew time, total mass | spearman`; `tension | primary | pointing error, control effort | pearson`; `tension | primary | pointing error, control effort | spearman`; `tension | primary | settling time, pointing error | pearson`; `tension | primary | settling time, pointing error | spearman`; `tension | primary | slew time, control effort | pearson`; `tension | primary | slew time, control effort | spearman`; `tension | primary | settling time, slew time | pearson`; `tension | primary | settling time, slew time | spearman`; `tension | stock | settling time, total mass | pearson`; `tension | stock | settling time, total mass | spearman`; `tension | stock | slew time, total mass | pearson`; `tension | stock | slew time, total mass | spearman`; `tension | stock | settling time, pointing error | pearson`; `tension | stock | settling time, pointing error | spearman`; `tension | stock | slew time, control effort | spearman`; `tension | stock | settling time, slew time | spearman`; `candidate | fast_effort_hungry | log V`; `candidate | fast_effort_hungry | novelty V-1`; `candidate | fast_effort_hungry | rank among training`; `candidate | fast_effort_hungry | tau*log V`; `candidate | precise_heavy_sensor | log V`; `candidate | precise_heavy_sensor | novelty V-1`; `candidate | precise_heavy_sensor | rank among training`; `candidate | precise_heavy_sensor | tau*log V`; `candidate | light_slow | log V`; `candidate | light_slow | novelty V-1`; `candidate | light_slow | rank among training`; `candidate | light_slow | tau*log V`; `sentence | candidates | text`; `predict | proposal_1 | measured log V`; `predict | proposal_1 | difference`; `predict | proposal_1 | |diff| / band`; `predict | proposal_1 | ||dZ||`; `predict | proposal_1 | ||dZ|| / band`; `predict | proposal_2 | measured log V`; `predict | proposal_2 | difference`; `predict | proposal_2 | |diff| / band`; `predict | proposal_2 | ||dZ||`; `predict | proposal_2 | ||dZ|| / band`; `predict | proposal_3 | measured log V`; `predict | proposal_3 | difference`; `predict | proposal_3 | |diff| / band`; `predict | proposal_3 | ||dZ||`; `predict | proposal_3 | ||dZ|| / band`; `predict, committed checks | proposal_1 | measured log V`; `predict, committed checks | proposal_1 | difference`; `predict, committed checks | proposal_1 | |diff| / band`; `predict, committed checks | proposal_1 | ||dZ||`; `predict, committed checks | proposal_1 | ||dZ|| / band`; `predict, committed checks | proposal_2 | measured log V`; `predict, committed checks | proposal_2 | difference`; `predict, committed checks | proposal_2 | |diff| / band`; `predict, committed checks | proposal_2 | ||dZ||`; `predict, committed checks | proposal_2 | ||dZ|| / band`; `predict, committed checks | proposal_3 | measured log V`; `predict, committed checks | proposal_3 | difference`; `predict, committed checks | proposal_3 | |diff| / band`; `predict, committed checks | proposal_3 | ||dZ||`; `predict, committed checks | proposal_3 | ||dZ|| / band`.

### Reading (written by the implementer, not generated)

**NOT IDENTICAL.** Under perturbations of relative size 1e-12 in the four continuous inputs, the
contending sets (K = 1 and each facet at K = 3, both regimes), each facet's leading metrics, the signs
of the six reported tensions in both regimes, the selected temperatures at the printed one decimal
(38.1, 41.7 and the K = 2, 3 values), the certificate statuses (`not_applicable`, `certified`,
`certified`) and the pass or miss outcome of every check design are identical in all five
regenerations and the committed data, and so are the flags and feasibility verdicts of all 2000
designs. Not identical at the printed precision: the nondominated counts (the primary four-metric
view 146 becomes 145 in seeds 1, 3 and 5; the two-attribute view 8 becomes 7 in seeds 2, 3 and 4; the
stock four-metric view 157 becomes 158 in seeds 1 and 2; the all-attribute count 671 and the stock
counts of the other views do not move); the regime comparison (the effective sample size 16.2 prints
as 16.0 or 16.1; the near-frontier count 51 prints as 52 in seed 2; the stock `frac_above_` 0.104
prints as 0.105; five association values move by 0.01); the K = 3 facet shares (0.089, 0.133, 0.778
become 0.065 to 0.087, 0.136 to 0.152, 0.761 to 0.795); and the quantities of the solver's
termination record that are numerical residues (largest facet gap near 1e-14, margin, radius), the
exponents that are zero to within 1e-16, and the tables of Appendix D that print them.

The deviation of the data is larger than the earlier evidence found for one design. In
the primary dataset `slew_time_s` of design 763 (medium wheel, Kp 1.63, Kd 0.35) is 33.44 s committed
and 12.53 s in seed 3, a jump of 20.9 s (relative 0.63): the first accepted step at which the error
falls under the band is a different step because the error trajectory touches the band at an earlier
step in the perturbed run (its 0.5-degree slew time moves from 33.44 s to 64.90 s the other way). All
other deviations of the two time columns are at most 0.49 s (relative 1.2e-2 for settling, 4.6e-2
for slew time over the rest), as before. The control effort moves by up to 1.7e-4 relative and the
other fitted attributes by at most 6e-7. This rules out reading the quantization as only a
sub-second effect on the percent scale: a single design's slew time can change by a factor of
almost three when a trajectory grazes the band.

These findings are for the supervisor under the stop condition of R-4 (the wording of the
conclusions that change is his to judge); nothing was interpreted away here.

## Amendment 2, first regeneration trial (not committed), 2026-11-10

Typed by the WP16 stream. Code at f5ed834 (event detection for the settling time and both slew times; reverted by
77844c5 when the trial stopped), tooling at a1b898e (`rerun_events.py`, reverted by fd73da8). Image `hts-wp16`,
id `sha256:a21ce70142b0dd108601e0903f689e8f15d9f2a3c65506ee693d02a42e6176bb`, linux/arm64, built at a1b898e and
removed afterwards. Primary and baseline regenerated (entries `v2-primary@5`, clean, and `v2-baseline@5`, dirty
because the primary output was uncommitted in the container); the run stopped at `v2-check-predictions@5`. Nothing
was committed to the data or the ledger. The analysis ran on the Mac with `sensitivity.quantities` on the image's two
datasets, the committed predictions and the six committed check designs re-measured with the new oracle. Scratch
evidence kept: `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp16-scratch/` (`gen1/` CSVs and ledger, `cmp/report.txt`, `cmp/quantities.json`, `gen.log`).

**Mechanism.** On each accepted RK45 step the dense interpolant makes `|q_vec|^2 - s^2 |q|^2` a degree-8
polynomial; its falling roots are the entries into the band, including a pass through the band that begins and ends
inside one step (a sign test at step ends, as `solve_ivp` events do, misses it). Times are read on a second
integration of the same dynamics at rtol 1e-13, atol 1e-16; every other quantity stays on `simulate_adcs` (rtol
1e-10). Under the D-6 jitter (1e-12) the times move by at most 1.5e-10 relative (5e-8 at the record tolerance).
Design 763: its error passes through the 1 degree band between 12.06 s and 12.53 s, inside one 0.5 s step; the first
entry is 12.058 s under every seed (not a graze).

**Data against the committed files.** Settling time up to 0.50 s later (976 of 1000 rows, primary); slew time up to
0.5 s earlier, design 763 by 21.4 s and one more design by more than 0.5 s; `slew_time_05deg_s` up to 76.7 s
(in-step passes through the 0.5 degree band). Other columns differ by platform rounding within their tolerances
(`torque_saturated_frac` at most 0.0095). No flag changed in either dataset.

| conclusion | committed against trial |
|---|---|
| contending sets at K = 1, both regimes | identical |
| contending sets at K = 3, primary | changed: facet 1 loses settling time (6 to 5 metrics); facet 3 same set |
| contending sets at K = 3, stock | changed: facets renumbered (G-10) and the 7-metric facet gains settling time (7 to 8) |
| each facet's leading metrics | primary identical; stock the same three triples, renumbered |
| signs of the six tensions; selected temperatures; certificate statuses | identical |
| check designs' outcomes (committed proposals, re-measured) | identical: three times log V pass, position miss |
| check-design proposer at REACH 0.35 on the trial primary | 2 of 3 reachable holes (the committed distances were 0.327 to 0.348) |
| nondominated counts | ten metrics 671 of 706 identical; four metrics 146 to 145, stock 157 to 158 |
| feasibility flags | identical, all 2000 designs |
| numbers moved | primary n_eff 16.2 to 15.5, near-frontier 51 to 57 (stock 103 to 106), association values by up to 0.04 |

**Cause.** The settling time read as the last exit is systematically later than the last step found outside the
band (up to one step, 0.5 s), which moves its participation at one K = 3 facet in each regime; the slew metric's
change moves the proposer's chart. The supervisor has since made the hold time (the settling time) the case's one time
metric and moved the regeneration after WP23 (`WP16-decisions.md`), so these conclusions are superseded by that
regeneration's data gate.

## WP23 data gate: old v2 (WP22 model, slew time, step-read settling time) against new v2 (WP23 model, nine metrics, event-detected settling time)

Written 2026-11-10 by the comparison stream of WP23 (D-9, R-13) at `dev` 8507bd9. Old files: the
committed state at `dev` 71a5f74, kept outside the repository in the session scratch folder
`wp23-gate-old/` with `SHA256SUMS.txt`; their four datasets are byte-equal to the frozen generation
under `examples/adcs/data/` that the paper reads (`4dc4ae0b8ebe`, `9450713cd78c`, `5794b7218dd9`,
`3e06e69bb345`), so "old" below is also "the paper as committed". New files: the regeneration of
record in `hts-paper` `3c7cfc8a2e27` at 2b2e94e (`work-packages/WP23-rounds/gate/README.md`,
`paper/container/RECORD.md`). Every number here was computed by a script kept in the session
scratch folder `wp23cmp/` (not committed): `files_compare.py` (parts 1 and 2; output
`files_compare.md`), `conclusions.py` (part 3: `case.py` at 8507bd9, defaults unchanged, on three
configurations; `conclusions.json`, rendered by `render.py` into `conclusions.md`),
`mac_remeasure.py` and `mac_flags.py` (the named rows re-measured on this Mac with the oracle of
record; `mac_remeasure.md`), `reach_check.py` (the proposer's rule replayed on three views;
`reach_check.md`). The three configurations of `conclusions.py` separate the causes: **old10**, the
old files with the paper's ten-metric `CUBESAT` spec (the paper's numbers as committed); **old9**,
the old files with the nine-metric spec (the column change alone: slew time out, the four-metric
view of the check carrying the settling time, the three slew-time association pairs gone);
**new9**, the new files with the nine-metric spec (the regeneration of record). A quantity equal
in old9 and new9 but not in old10 moved because of the column change; a quantity that differs
between old9 and new9 moved because of the regenerated data (the event-detected settling time and
the platform of record).

### Changed conclusions (read first)

Each item: what the paper prints today, what the new data gives, and the cause.

1. **The K = 1 contending sets are 5-lemmas, not 6-lemmas, in both regimes.** Primary regime: total
   mass, slew time, energy balance, control effort, pointing error, depth of discharge (6) becomes
   total mass, energy balance, pointing error, depth of discharge, settling time (5); the leading
   metric changes from slew time (0.240) to total mass (0.358). Baseline regime: control effort,
   slew time, power margin, settling time, pointing error, eclipse reserve (6) becomes control
   effort, settling time, power margin, pointing error, depth of discharge (5); control effort leads
   both (0.430, 0.432). Cause: the column change (old9 and new9 agree on every set and on every
   exponent to three decimals). The selected temperature at K = 1 is 38.1 in the primary regime
   in all three configurations; in the baseline regime 41.7 becomes 45.7 (column change).
2. **The per-term report refuses on the primary regime at K = 3, at both documented bands.** At the
   K = 1 band (1/tau = 0.0262) term 2's cell (181 rows, share 0.034) has 3 near-frontier rows; at
   the K = 3 fit's own band (0.0088) term 1's cell has 7 and term 2's 1; the report's guard is 10.
   The library's message numbers terms from 0 (`facet 1: only 3 near-frontier rows`, `facet 0:
   only 7`), which `k3_record.md` read as term 1 at both bands; the counts above are from the
   estimator's assignments (`conclusions.py`, `near_at_k1_band`, `near_at_own_band`). It refuses on
   old9 too (2 rows and 8 rows), so the cause is the column change, not the regeneration. Nothing
   was loosened: the fit is reported from the estimator (exponents per term, cells, shares, the
   certificate), as `k3_record.md` reports it. Consequence for the paper: `num-k-sweep` (the
   sentence reads `facet_table`), `fig-tensions-k3` (`case.tension_figure` at the K = 1 band) and
   Appendix D.3 cannot be generated on the new primary data as the cells stand; the K = 2 report
   does not refuse (13 near-frontier rows in the smaller cell).
3. **The K = 3 fits change in both regimes.** Primary: terms with contending sets of 6, 6 and 7
   metrics and shares 0.089, 0.133, 0.778 become three terms led by energy balance (0.416, with
   total mass 0.240 and settling time 0.185), control effort (0.397, with settling time 0.367 and
   energy balance 0.193) and peak slew power (0.612, with pointing error 0.227), shares 0.241,
   0.034, 0.724 (reported from the exponents, item 2). Baseline: sets of 6, 7 and 5 become 5, 6 and
   4; term 3's leading metric changes from energy balance (0.355) to control effort (0.353, energy
   balance 0.347); shares 0.077, 0.590, 0.333 become 0.118, 0.451, 0.431. Cause: the column change
   for the sets and the leading metrics (old9 equals new9 in every set); the event-detected settling
   time for the shares (old9 to new9: baseline 0.500 to 0.451 and 0.375 to 0.431, primary by at most
   0.017), the same size as the shares' spread under the 1e-12 jitter of WP16 D-6 above. The
   selected temperatures at K = 2 and 3 move with the columns: primary 113.2 and 195.2 become 94.4
   and 113.2; baseline 78.8 and 162.8 become 71.9 and 113.2.
4. **The check changes in kind.** Old: three proposals on the slew-time view at WP7's reach 0.35,
   three distinct designs, log V within the band for 3 of 3 and position for 0 of 3 (position
   errors 1.4 to 3.1 bands), `dod_ok` False for 2 of 3. New: three proposals on the settling-time
   view at the reach of the stated rule (0.6222, the 2nd percentile of the pool's nearest predicted
   distances to the 300 most isolated holes; the rule replayed here returns 0.3510 on the old view
   and 0.6222 on the new data, and the files' three distances on each: `reach_check.md`), two of
   them one configuration (proposal_1 and proposal_3: medium wheel, fine tracker, 0.3037 m, 25.4
   Wh, Kp 1.78, Kd 0.50; the regressor tau 15.37 becomes 10.69, the band 0.065 becomes 0.094),
   log V within the band for 3 of 3 and **position within the band for 1 of 3** (proposal_2 at
   0.51 bands; the other two rows are the one design at 1.05 bands), `dod_ok` **False for 3 of
   3**. Cause of the new proposals: the view change and the rule (CR-3); cause of the coincidence:
   the regenerated data, since the rule on the old data with the new view admits three holes
   mapped to three distinct pool designs (42750, 37780, 50305 at 0.5798, 0.5843, 0.5514) and on the
   new data the third hole's nearest pool design is 37780 again (0.5552). What `dod_ok` False on all
   three means for the check section: the proposer trains on the rows that are settled, within the
   momentum budget and power-positive (`feasible_primary`, as WP7 did) and the chart has no
   depth-of-discharge axis, so it proposes at the small end of the battery range (22 to 25 Wh),
   where the model's depth-of-discharge requirement is violated; the paper's sentences
   (`num-predict`, `num-predict-reading`: "did not show that it places the position (0 of 3)")
   change, and whether a proposal that fails a requirement of the model counts as a check is the
   supervisor's reading, not the gate's.
5. **Counts and values the paper prints, moved.** Nondominated: 671 of 706 on 10 attributes
   becomes 659 on 9; the four-metric view 146 becomes 126 (the view now carries the settling time);
   the two-attribute view (settling time and slew time, 8) no longer exists; baseline 732 on 10
   becomes 725 on 9 and 157 becomes 152. Effective sample size at K = 1: 16.2 becomes 23.1
   (primary; column change), 14.5 becomes 14.6 (baseline). Near-frontier designs at K = 1: 51
   becomes 56, 103 becomes 77. Mean slack: 0.204, 0.138, 0.117 becomes 0.243, 0.182, 0.146
   (primary); 0.131, 0.106, 0.093 becomes 0.179, 0.142, 0.093 (baseline); refitted at the K = 1
   temperature 0.090, 0.053 becomes 0.132, 0.088 and 0.068, 0.033 becomes 0.114, 0.046. Candidates:
   0 of 3 beyond the surface in every configuration; their log V move from -0.115, -0.072, -0.144 to
   -0.197, -0.153, -0.171 and their ranks from 0.59 to 0.77 to 0.53 to 0.62 (column change).
6. **Two association signs are not stable, the rest hold.** Primary (settling time, pointing
   error): +0.18 (+0.20) becomes +0.03 (+0.15), and old9 gives -0.03 (+0.11): the Pearson value is
   a residue whose sign moves with the data; baseline (settling time, total mass): -0.12 (-0.02)
   becomes -0.12 (+0.04): the Spearman sign changes. Every other reported sign is identical;
   (settling time, total mass) in the primary regime moves from -0.54 (-0.34) to -0.50 (-0.50);
   the three slew-time pairs cease to exist.
7. **Unchanged:** the certificate statuses (`not_applicable`, `certified`, `certified` in both
   regimes); the feasibility flags and the feasible sets (706 and 780; no design's flag changed);
   the settled flag that cannot move (verified below); the two metric redundancies (Spearman among
   the feasible designs, old and new: eclipse reserve with depth of discharge -0.9994 in both
   regimes; power margin with energy balance +0.9824 primary and +0.9880 baseline), which stand as
   readings for the supervisor's decision on the metric set (WP23 OD7).

### 1. The files

| dataset | old sha256 | new sha256 | rows | columns old / new | out | in |
|---|---|---|---|---|---|---|
| `data/v2/adcs_designs_cubesat_gains.csv` (primary) | `4dc4ae0b8ebe` | `0bc823ceaf51` | 1000 | 35 / 33 | `slew_time_s`, `slew_time_05deg_s` | none |
| `data/v2/adcs_designs_cubesat.csv` (baseline) | `9450713cd78c` | `4ec7514e9ac5` | 1000 | 35 / 33 | the same two | none |
| `data/v2/check_predictions_cubesat.csv` | `5794b7218dd9` | `6b65b2843a99` | 3 | 25 / 25 | `pred_std_slew_time_s` | `pred_std_settling_time_s` |
| `data/v2/check_designs_cubesat.csv` | `3e06e69bb345` | `b6facc345c68` | 6 | 34 / 32 | the same two | none |
| `data/scope-sensitivity/scope_sensitivity_v2.csv` | `97193d955a73` | `3e0d7df6cab8` | 20 | 35 / 33 | the same two | none |
| `tests/data/v2_first_designs_of_record.csv` | `1943d76cb2a6` | `894277fb237c` | 20 | 35 / 33 | the same two | none |
| `model_v2/views/coverage.csv` | `2213a8a1a03e` | `494b10e96198` | 92 | 8 / 8 | none | none |

Ledger: 29 entries old, 34 new; the five added (`v2-primary@5` superseding `@4`, `v2-baseline@5`,
`v2-check-predictions@5`, `v2-check-designs@5`, `scope-sensitivity-shared-subspace-v2@4`
superseding `@3`) carry the new outputs' hashes above, `model_sha256` `fb1dbd061610` (the WP23
model; the superseded entries carry `0a0b4a4b64d1`, the WP22 model), commit 2b2e94e, `git_dirty`
False, platform `Linux-6.8.0-50-generic-aarch64-with-glibc2.41`, image `3c7cfc8a2e27`. The old
`@4` entries were made on this Mac (macOS arm64) at 6ed13ed with the bytes of `@2` (2d13465).

### 2. Every moved number, column by column

**The two 1000-design tables.** Design ids, seeds and categorical values agree on every row. Of
the 32 shared columns, 24 are identical in both tables: the four configuration columns, pointing
error, total mass, ADCS mass, power margin, peak slew power, the four flags, the panel and battery
masses, generated and available power, usable torque, and the three scenario columns. The eight
that move, with the generation's tolerance (primary: rtol 1e-3; baseline: rtol 1e-4; settling time
within 0.5 s; saturated fraction rtol 0.1 and 0.02):

| column | primary: rows moved / beyond tolerance, largest move (id) | baseline: rows moved / beyond, largest move (id) | cause |
|---|---|---|---|
| `settling_time_s` | 976 / 0; +0.499 s (93), relative 0.030 (858); mean +0.142 s | 978 / 0; +0.498 s (16), relative 0.030 (787); mean +0.208 s | the read-off (below) |
| `control_effort` | 669 / 0; 1.4e-5 (973), relative 7.4e-5 (515) | 282 / 1; 1.2e-5 (466), relative 1.2e-4 (488) | the platform's accepted steps (below) |
| `torque_saturated_frac` | 514 / 3; 0.0095 (23), relative 0.133 (781) | 168 / 35; 0.0071 (360), relative 0.185 (354) | the platform's accepted steps (CR-2) |
| `peak_momentum_nms` | 122 / 0; relative 3.3e-5 | 59 / 0; relative 1.5e-5 | the same steps (a cumulative sum over them) |
| `slew_loss_energy_wh` | 655 / 0; relative 7.3e-5 | 272 / 0; relative 2.3e-5 | the same steps (the torque-squared integral) |
| `energy_balance_wh`, `eclipse_reserve_wh`, `dod_eclipse` | 59, 129, 116 / 0; relative at most 1.9e-7 | 7, 27, 23 / 0; at most 8.8e-8 | the slew loss energy enters them; at the CSV's ninth digit |

*The settling time.* It is later in 976 of 1000 primary and 978 of 1000 baseline designs, never
earlier, by at most 0.4993 s (less than one integration step, `max_step_s` 0.5 in both files), and
equal on the 24 and 22 designs at the horizon (600 s). Mechanism: the old read-off took the last
accepted step at which the error was outside the band (`_last_outside`); the event-detected time is
the last exit itself, which lies inside the step after that point (`crossing_times`, `hold_time`:
the dense RK45 solution at rtol 1e-13, WP16 D-7). Re-measured on this Mac with the oracle of record
(`mac_remeasure.md`), the event-detected time equals the container's on all 14 re-measured dataset
rows to 8e-7 s and on the three candidates to the ninth digit, and exceeds the Mac's own step
read-off by 0.000 to 0.499 s: the read-off is the whole cause.

*The control effort, and the saturated fraction.* Both are sums over the accepted steps of
`simulate_adcs` (the trapezoid of |torque|; the share of steps at the cap), whose code is unchanged
since the old files' commit (`git diff 2d13465 HEAD -- examples/adcs/adcs_sim.py` is empty; the
event detection runs a second integration for the times only). The accepted-step sequence differs
between the Mac (old files) and the container (linux/arm64): every row whose saturated fraction
moved also has a control-effort move (514 of 514 primary, 168 of 168 baseline; Spearman 0.78 and
0.79 between the sizes of the two moves), and the candidates isolate the platform from the code:
with their exact inputs the Mac now reproduces the old file's control effort and saturated fraction
to all nine digits for all three, while the container's differ (saturated fraction 0.02691 to
0.02763 and 0.1184 to 0.1203 on two of them; control effort by 6e-8 relative). The one baseline row
beyond tolerance, design 488 (medium wheel, medium tracker, Kp 0.718, Kd 0.359), moves by 1.2e-4
relative against the baseline entry's rtol 1e-4, ten times tighter than the primary's 1e-3; the
moves are the same size in both regimes (99th percentile 4.8e-5 and 4.4e-5), so the tolerance, not
the row, is why one crosses. The dataset rows re-measured on the Mac from the CSV's nine-digit
inputs differ from the old file by the same order (control effort up to 8.7e-5 relative, saturated
fraction up to 0.009): a rounding of 1e-9 in the inputs moves the step sequence as the 1e-12 jitter
of D-6 did, so that part of the re-measurement is a rounding test, not a platform test, and the
candidates are the platform test. Neither column is fitted; the three primary rows beyond the
saturation tolerance (54, 161, 781, large wheels at 0.02 to 0.03) and 25 of the 35 baseline rows
have saturated fractions below 0.09, where one or two accepted steps out of a few hundred are a
tenth of the value.

**The feasibility flags.** Primary: settled 976 True / 24 False, momentum_ok 812 / 188, power_ok
1000 / 0, dod_ok 869 / 131; baseline: 978 / 22, 919 / 81, 1000 / 0, 869 / 131; identical old and
new, and no design's flag changed (`files_compare.md`; `mac_flags.py` found no flag difference on the
re-measured rows either). The settled flag cannot move: `settled` equals `settling_time_s < 600`
on every new row, the largest settled settling time is 594.9 s (primary) and 598.2 s (baseline), no
design lies within 0.5 s below the horizon in either file, and the read-off moves a time by less
than 0.5 s and never earlier.

**The check predictions** (3 rows): every numeric column differs, because the rows are new
proposals (item 4): the configurations (old: medium/fine 0.337 m 21.7 Wh Kp 0.74 Kd 0.32;
small/fine 0.313 m 22.1 Wh Kp 1.06 Kd 1.12; large/fine 0.301 m 199.9 Wh Kp 0.51 Kd 1.16; new:
medium/fine 0.3037 m 25.40 Wh Kp 1.782 Kd 0.505, twice, and medium/fine 0.3001 m 21.96 Wh Kp 0.835
Kd 0.313), the targets, predictions, scores (3.40, 3.32, 3.27 to 4.85, 4.85, 4.83), distances
(0.348, 0.340, 0.327 to 0.587, 0.579, 0.555), tau 15.37 to 10.69, band 0.0651 to 0.0935; `n_train`
706 and the tracker grade (fine) are the same. **The check designs** (6 rows): the three candidates
reproduce with the settling time later by 0.087, 0.089 and 0.078 s and the saturated fraction moved
on two (platform; every other column identical to nine digits); the three proposal rows are the new
designs, so all 24 numeric columns of theirs move and `dod_ok` on the row named proposal_3 reads
True then False (a different design). **The scope-sensitivity table** (20 rows): settling time
later by up to 0.389 s, control effort by up to 2e-5 relative, saturated fraction by up to 0.0024,
nothing beyond tolerance, flags identical. **The first-20 recording**: only the settling time moves
(19 rows, up to +0.46 s); control effort and saturated fraction are identical on all 20 (the
container's and the Mac's steps agree on these designs). **The coverage table**: 4 of 736 cells,
all `max_relative_change` of the settling-time row of a decision element: TrackerGrade 1.7e-2 to
2.1e-2, batteryCapacity 9.1e-3 to 3.1e-3, Kp 9.4e-2 to 9.3e-2, Kd 2.1e-1 to 2.2e-1; every
structural and empirical verdict unchanged.

Moved in all: 8 columns of each 1000-design table (3,240 and 1,816 row values), 19 numeric
columns and one categorical of the predictions (all 3 rows), 24 numeric columns and one flag of the
check designs (3 to 6 rows each), 5 columns of the scope table, 1 of the first-20 recording, 4
coverage cells; beyond tolerance: 3 + 35 saturated-fraction rows and 1 control-effort row, and
every column of the proposal rows (CR-2 to CR-4).

### 3. The conclusions, item by item

Computed by `case.py` (`load_study`, `k_fits`, `tension_table`, `facet_table`,
`certificate_table`, `mean_slack_by_k`, `mean_slack_fixed_tau`, `association_table`,
`regime_comparison`, `nondominated_counts`, `candidate_table`, `fit_regressor`, `predict_check`)
with the spec's defaults (target 0.10, bounds (3, 1000), seed 0). "Identical" means equal at the
precision the paper prints (sets and names exactly; temperatures to one decimal; associations to
two; counts exactly; shares and slack to three decimals).

**Primary regime** (706 feasible of 1000 in every configuration).

| item | old10 (the paper) | old9 (columns only) | new9 (the gate) | verdict, cause |
|---|---|---|---|---|
| K = 1 tau, band, frac above, n_eff | 38.1, 0.0262, 0.096, 16.2 | 38.1, 0.0262, 0.091, 23.1 | 38.1, 0.0262, 0.092, 23.1 | tau identical; n_eff changed (columns); frac moved 0.004 |
| K = 1 contending set (n-lemma; near-frontier) | total mass, slew time, energy balance, control effort, pointing error, depth of discharge (6; 51) | total mass, energy balance, pointing error, depth of discharge, settling time (5; 56) | the same as old9 (5; 56) | changed (columns) |
| K = 1 leading metrics | slew time 0.240, control effort 0.197, energy balance 0.190 | total mass 0.358, energy balance 0.184, pointing error 0.164 | the same as old9 | changed (columns) |
| K = 2, K = 3 tau | 113.2, 195.2 | 94.4, 113.2 | 94.4, 113.2 | changed (columns) |
| K = 2 per term: sets (n-lemma), leading, shares | 7 and 7; control effort 0.365 / peak slew power 0.515; 0.371, 0.629 | 5 and 5; peak slew power 0.583 / settling time 0.363; 0.828, 0.172 | 5 and 5; peak slew power 0.582 / settling time 0.364; 0.800, 0.200 | sets and leading changed (columns); shares moved 0.028 (data) |
| K = 3 per term: report | sets of 6, 6, 7; leading control effort 0.429 / energy balance 0.434 / peak slew power 0.380 | refused at both bands (2 and 8 rows) | refused at both bands (3 and 7 rows) | changed (columns); item 2 |
| K = 3 per term from the estimator: leading, cells, shares | as above; 201, 188, 317 rows; 0.089, 0.133, 0.778 | energy balance 0.415 / control effort 0.396 / peak slew power 0.612; 162, 181, 363; 0.258, 0.032, 0.710 | energy balance 0.416 / control effort 0.397 / peak slew power 0.612; 162, 181, 363; 0.241, 0.034, 0.724 | leading changed (columns); shares moved 0.017 (data) |
| certificate K = 1, 2, 3 | not_applicable, certified, certified | the same | the same | identical; residues: gap 1.1e-14 to 3.3e-15, margin 0.00022 to 0.00121, radius 1.8e-5 to 1.0e-4 |
| mean slack K = 1, 2, 3 (own tau; at the K = 1 tau) | 0.204, 0.138, 0.117 (0.090, 0.053) | 0.243, 0.182, 0.146 (0.131, 0.087) | 0.243, 0.182, 0.146 (0.132, 0.088) | changed (columns) |
| settling time, total mass | -0.54 (-0.34) | -0.43 (-0.43) | -0.50 (-0.50) | sign identical; values moved (both causes) |
| pointing error, control effort | -0.36 (-0.48) | -0.35 (-0.49) | -0.36 (-0.50) | sign identical; Spearman moved 0.02 |
| settling time, pointing error | +0.18 (+0.20) | -0.03 (+0.11) | +0.03 (+0.15) | Pearson sign not stable (item 6) |
| slew time pairs (3) | -0.48 (-0.33), -0.87 (-0.83), +0.91 (+0.88) | none | none | cease to exist (columns) |
| nondominated: all; four metrics; two times | 671 of 706 on 10; 146 on 4 (0.207); 8 on 2 | 660 on 9; 125 on 4 (0.177); view gone | 659 on 9; 126 on 4 (0.179); view gone | changed (columns; then 1 by data) |
| candidates: log V; beyond; ranks | -0.115, -0.072, -0.144; 0; 0.59 to 0.77 | -0.197, -0.152, -0.172; 0; 0.53 to 0.62 | -0.197, -0.153, -0.171; 0; 0.53 to 0.62 | beyond identical; values changed (columns) |
| regressor tau, band | 15.37, 0.0651 | (no check: the recorded predictions are on the other view) | 10.69, 0.0935 | changed (view) |
| check: log V pass; position pass; position errors | 3 of 3; 0 of 3; 1.35, 2.21, 3.09 bands | - | 3 of 3; 1 of 3; 1.05, 0.51, 1.05 bands | changed in kind (item 4) |
| proposals' distance to target against the reach | 0.348, 0.340, 0.327 within 0.35 (typed) | - | 0.587, 0.579, 0.555 within 0.6222 (the rule) | changed (the rule and the view) |

**Baseline regime** (780 feasible of 1000 in every configuration; `case.py` keys it `stock`).

| item | old10 (the paper) | old9 (columns only) | new9 (the gate) | verdict, cause |
|---|---|---|---|---|
| K = 1 tau, band, frac above, n_eff | 41.7, 0.0240, 0.104, 14.5 | 45.7, 0.0219, 0.103, 13.7 | 45.7, 0.0219, 0.104, 14.6 | tau changed (columns); n_eff 14.5 to 14.6 (13.7 in old9: both causes) |
| K = 1 contending set (n-lemma; near-frontier) | control effort, slew time, power margin, settling time, pointing error, eclipse reserve (6; 103) | control effort, settling time, power margin, pointing error, depth of discharge (5; 76) | the same set (5; 77) | changed (columns) |
| K = 1 leading metrics | control effort 0.430, slew time 0.332, power margin 0.176 | control effort 0.432, settling time 0.318, power margin 0.170 | control effort 0.432, settling time 0.319, power margin 0.178 | leader identical; second changed (columns) |
| K = 2, K = 3 tau | 78.8, 162.8 | 71.9, 113.2 | 71.9, 113.2 | changed (columns) |
| K = 2 per term: sets, leading, shares | 5 and 5; energy balance 0.357 / control effort 0.487; 0.694, 0.306 | 4 and 5; control effort 0.364 / control effort 0.509; 0.571, 0.429 | 4 and 5; control effort 0.363 / control effort 0.508; 0.562, 0.438 | changed (columns); shares moved 0.009 (data) |
| K = 3 per term: sets (n-lemma) | 6, 7, 5 (report at the K = 1 band) | 5, 6, 4 | 5, 6, 4 | changed (columns) |
| K = 3 leading per term | control effort 0.488 / peak slew power 0.359 / energy balance 0.355 | control effort 0.509 / peak slew power 0.431 / control effort 0.353 | control effort 0.507 / peak slew power 0.428 / control effort 0.353 | term 3's leader changed (columns; energy balance 0.347 second) |
| K = 3 cells, shares | 284, 149, 347; 0.077, 0.590, 0.333 | 251, 184, 345; 0.125, 0.500, 0.375 | 251, 184, 345; 0.118, 0.451, 0.431 | cells changed (columns); shares moved up to 0.056 (data) |
| certificate K = 1, 2, 3 | not_applicable, certified, certified | the same | the same | identical; residues: margin 0.0015 to 9e-5, radius 1.2e-4 to 7.7e-6 |
| mean slack K = 1, 2, 3 (own tau; at the K = 1 tau) | 0.131, 0.106, 0.093 (0.068, 0.033) | 0.180, 0.142, 0.093 (0.114, 0.046) | 0.179, 0.142, 0.093 (0.114, 0.046) | changed (columns) |
| settling time, total mass | -0.12 (-0.02) | -0.08 (+0.07) | -0.12 (+0.04) | Spearman sign not stable (item 6) |
| pointing error, control effort | -0.70 (-0.77) | -0.63 (-0.70) | -0.65 (-0.70) | sign identical; values moved (columns) |
| settling time, pointing error | +0.69 (+0.75) | +0.63 (+0.71) | +0.66 (+0.71) | sign identical; values moved (columns) |
| slew time pairs (3) | -0.10 (-0.03), -0.96 (-0.95), +0.99 (+0.99) | none | none | cease to exist (columns) |
| nondominated: all; four metrics; two times | 732 of 780 on 10; 157 on 4 (0.201); 2 on 2 | 724 on 9; 150 on 4 (0.192); gone | 725 on 9; 152 on 4 (0.195); gone | changed (columns; then 1 and 2 by data) |

**The regime sentence** (`num-regimes`, from `regime_comparison`): "a 6-lemma and a 6-lemma
sharing 3 metrics (control effort, pointing error, slew time)" becomes "a 5-lemma and a 5-lemma
sharing 3 metrics (depth of discharge, pointing error, settling time); the primary regime alone
has energy balance and total mass, the baseline regime alone control effort and power margin". **The redundancies**: identical old and new (item 7),
because neither column moved. **The settled flag**: part 2.

### 4. The slots whose axis or metric set changes with the swap

`paper/paper.ipynb` (cell ids by `nbformat`; the notebook was not edited):

- `num-attributes` (54), `num-datasets` (59): "ten attributes" and "carries 10 attributes" become nine.
- `fig-tau-sweep` (61) with `fig-tau-sweep-caption` and `-lines` (62, 63): the heatmap's rows are the
  spec's attributes (ten to nine; the slew-time row goes); the gate's drawing is
  `WP23-rounds/gate/heatmap.png`.
- `num-temperature` (64): n_eff 16.2 becomes 23.1; the band and tau stand.
- `num-k1` (71): the 6-lemma becomes the 5-lemma of item 1, exponents 0.09 to 0.24 become 0.14 to 0.36.
- `fig-planes-k1-caption` and `-lines` (72, 73) and the static `paper/figures/fig-planes-k1.png`
  (`paper/figures/planes.py`): the K = 1 plane is the two heaviest metrics of the term, slew time and
  control effort today; on the new data total mass and energy balance.
- `fig-planes-k3-caption` and `-lines` (75, 76) and `fig-planes-k3.png`: the three slices are each
  term's two heaviest metrics (today control effort with slew time, energy balance with control
  effort, peak slew power with total mass; new: energy balance with total mass, control effort with
  settling time, peak slew power with pointing error); the caption's sentence on the bottom panel
  (peak slew power) follows the new panel; `fig-chart-level` (77, 78) and `fig-chart-level.png`:
  the chart of the nine-metric K = 3 fit; the caption's "the first of nine position coordinates"
  becomes eight.
- `fig-tensions-k3` (79) with (80, 81): the per-term heatmaps' metric lists (nine); on the primary
  regime the generator refuses at the K = 1 band (item 2).
- `num-k-sweep` (82) and `sec-case-analysis-3` (83): the mean slack values, the K = 3 n-lemmas and
  the "absent from the K = 1 set" metrics; the sentence reads `facet_table` and refuses on the
  primary regime (item 2).
- `fig-regimes` (84) with (85, 86) and `num-regimes` (87): `case.regime_figure` draws the spec's
  association pairs (six today, three without the slew time) and the two contending sets.
- `num-candidates` (90): the log V range -0.144 to -0.072 becomes -0.197 to -0.153; the ranks.
- `num-predict` (94), `num-predict-reading` (96): 0 of 3 positions becomes 1 of 3; the band 0.0651
  becomes 0.0935; the position errors 1.4 to 3.1 bands become 0.5 to 1.1; two proposals one design.
- `num-nondominated` (6): the counts of item 5 and the views (the two-attribute view goes).
- `num-certificates` (48), `num-margin` (49): statuses stand; the residues printed as bounds move.
- `fig-behavioural-caption` (56): the image is already the WP23 view (8507bd9); its text still says
  "dashed: a metric traded with no requirement on it (control effort, pointing error, peak slew
  power, total mass)", which the WP23 model's four requirements make stale; `fig-assembly-caption`
  (53): the image is updated, the text to be read against it.

`paper/supporting_material.ipynb`: Appendix C's attribute tables (`tab-C-evaluation` 20,
`tab-C-attribute_sources` 21, `tab-C-metric_table` 27, `tab-C-datasets` 29: `generate_model.py`
still lists `slew_time_s` with its source `cubesat_model.py`); every Appendix D table
(`tab-D-temperature_selection` 35, `tab-D-k_diagnostics` 37, `tab-D-exponents_and_facets` 39 (the
exponent columns lose a row; the per-term table refuses on the primary regime), `tab-D-regime_comparison`
41 (the three slew-time pairs go), `tab-D-sensitivity_variants` 43, `tab-D-refits_by_category` 45,
`tab-D-candidate_designs` 47, `tab-D-termination_records` 49, `tab-D-margin_reading` 51,
`tab-D-nondominated` 53, `tab-D-propose_predict_check` 55, `tab-D-stability` 57 (reads
`examples/adcs/experiments/reports/sensitivity.json`, whose quantities include the slew-time pairs and
the two-attribute view: the D-6 regeneration must be re-run on the new data and spec for the
`stable()` ranges), `tab-D-conditioning_diagnostic` 59, `tab-D-own_rows_refit` 61,
`tab-D-mean_slack_fixed` 67, `tab-D-pca_chain` 70); `tab-E-gaps` (73: G-17 names the slew time's
grazing); Appendix F's tables (`tab-F-commands` 81, `tab-F-reproduction` 83: the data hashes and
ledger ids). Also `paper/environment_values.toml` and `environment_reference.npz` (the
`v2_first_designs_rows` values of the environment of record) and `paper/paper_stability.py`'s
docstring (names `slew_time_s`).

`docs/examples.md`: the prose ("Ten attributes ... slew time", the 6-lemma with slew time, "contending
sets of 6, 6 and 7 metrics", "78 percent", "the other two are built on control effort, slew time
and energy balance", "mean slack falls from 0.204 ... to 0.117") and the two generated figures
`adcs-tensions` (ten metrics, six outlined) and `adcs-coordinates` ("nine position coordinates",
"212 ringed designs"); no other docs page names the slew time. `examples/adcs/k_terms.py` and
`case.py`'s `CUBESAT` spec (ten attributes, the two views, six pairs) are the paper's inputs and
change with the paper's move (WP16 order step (4)); `examples/adcs/figures/k3_*.png` are its outputs.

Already updated at the gate: the model's two views (`fig-assembly-view.png`, `fig-behavioural-view.png`
at revision 5, byte copies), the coverage table, the change register and the v1-v2 comparison report.

### 5. The paper's move onto the data of record

Written by the paper stream at `dev` ea46637 (code, prose) and its regeneration in `hts-paper`
`f7b7585c7c58` (`paper/container/RECORD.md`, "Regeneration of the paper on the data of record"). The paper
reads `data/v2/` directly (`CUBESAT.data_dir`, `k_terms.DATA`); the four frozen files under `data/` are
untouched, because a byte copy over them made `experiments verify` report four drifts on the adopted entries
(the contract's `case.data_dir` still names `data/`: an amendment for the contract's owner). The `CUBESAT` spec has nine attributes, the four-metric view
(settling time, pointing error, control effort, total mass) and three association pairs. **The per-term
mechanism (item 2):** the guard of the library's `tension_report` is bypassed at the call
(`min_near_frontier=0`) and reapplied per term at ten in `case.py` (`case.term_reports`, with `has_reading`
and `thin_reason`); every term is reported from the estimator (exponents, cell, share, contending set), and
a term with fewer than ten near-frontier rows (term 2 of the primary K = 3 fit, 3 at the K = 1 band) has no
association map: its panel of `fig-tensions-k3` and of `k3_tensions_primary.png` carries "too few
near-frontier designs for an association reading: 3 of ten", and Appendix D.3 states it under the per-term
table. The association readings at K = 1 still refuse a thin term. `k_terms.run_regime` and the D-6
analysis use the same helper.

Every cell whose source or output changed (`paper.ipynb` P, `supporting_material.ipynb` S), with its cause:
an item of the changed conclusions above (1 to 7), "column change" (the slew time out), "regeneration" (the
regenerated values), or "prose follows" (a sentence written to the new figure or number).

| cell | what changed | cause |
|---|---|---|
| P `num-nondominated` | 659 on 9, 126 on 4; the two-attribute view gone; no count moves under the jitter, so the sentence says what a range would be | 5 |
| P `num-margin` | margin 0.00121, radius 9.94e-05 to 9.95e-05, band 0.0088, median 0.237 | 3 |
| P `num-attributes`, `num-datasets` | nine attributes | column change |
| P `fig-assembly-caption` | the claim that the view draws ranges dropped (they are in C.1); "Shows" says levels | prose follows (revision 6 view) |
| P `fig-behavioural-caption` | the dashed clause gone (every traded metric is read by a requirement); sources as the revision 6 view draws them | prose follows |
| P `fig-tau-sweep` (image), `-caption`, `-lines` | nine rows; Redraw 2's caption and lines, "insensitivity to tau" struck | column change; prose follows (WP19 Redraw 2) |
| P `num-temperature` | n_eff 23.1, fraction 0.092 | 5 |
| P `num-k1` | the 5-lemma, exponents 0.14 to 0.36 | 1 |
| P `fig-planes-k1-caption`, `-lines`, `fig-planes-k1.png` | the pair is total mass and energy balance; seven other metrics | 1; prose follows |
| P `fig-planes-k3-caption`, `fig-planes-k3.png` | slices total mass/energy balance, settling time/control effort, pointing error/peak slew power; the bottom-panel sentence (tracker-grade columns, six bands, the large wheel's cloud) | 3; prose follows |
| P `fig-chart-level-caption`, `fig-chart-level.png` | eight position coordinates (the axis label computes it) | column change |
| P `fig-tensions-k3` (image), `-caption`, `-lines` | three panels, term 2 replaced by its reason; caption says so | 2 (the per-term rule) |
| P `num-k-sweep` | mean slack 0.243, 0.182, 0.146 at 38, 94, 113; fixed 0.13, 0.09; sets of 5, 4, 5; control effort and peak slew power, absent at K = 1, each lead a term (the sharper content of the blend claim, C034, which stands) | 3; 2 |
| P `fig-regimes` (image), `num-regimes` | 5-lemma and 5-lemma sharing depth of discharge, pointing error, settling time; three pairs | 1; 6; column change |
| P `num-candidates` | log V -0.197 to -0.153 | 5 |
| P `sec-case-analysis-5` | the radius rule for both views (0.6222 here, 0.351 on the old view where 0.35 was typed) | 4 |
| P `num-predict` | band 0.0935, position 1 of 3, errors 0.5 to 1.1 bands | 4 |
| P `num-predict-reading` | two proposals one configuration; position 1 of 3; all three fail the depth-of-discharge requirement, with the reason | 4 |
| S `app-C-job`, `app-D-job` | nine attributes; the jitter is in the design variables | column change; prose follows |
| S `tab-C-evaluation`, `tab-C-attribute_sources`, `tab-C-conditioning`, `tab-C-metric_table` | nine rows or columns | column change |
| S `tab-C-datasets` | the files are `data/v2/`; ledger entries v2-primary@5, v2-baseline@5 found by hash, their run command, new hashes | regeneration |
| S `tab-D-temperature_selection`, `tab-D-k_diagnostics`, `tab-D-termination_records`, `tab-D-margin_reading`, `tab-D-mean_slack_fixed`, `tab-D-conditioning_diagnostic` | new temperatures, slack, shares, residues, conditioning | 1; 3; 5 |
| S `tab-D-exponents_and_facets` | nine-row exponent tables; the per-term table for all three terms with term 2's sentence | 3; 2 |
| S `tab-D-regime_comparison` | three pairs; the new sets and associations | 6; column change |
| S `tab-D-sensitivity_variants`, `tab-D-refits_by_category`, `tab-D-candidate_designs`, `tab-D-nondominated`, `tab-D-propose_predict_check`, `tab-D-pca_chain` | new values; one view | 5; 4; column change |
| S `tab-D-stability` | the D-6 record rerun on the new model (693 quantities, 80 move at the printed precision, every conclusion identical); the head says what moves now and that the regenerations ran on the Mac | regeneration |
| S `tab-E-gaps` | G-2 and G-17 rows written to the nine-metric facts | column change; regeneration |
| S `tab-F-toolchain`, `tab-F-reproduction` | the commit and platform of the build; the case's files read from `data/v2/` | regeneration |

Unchanged as D-9 item 7 says: `num-certificates`, `num-recovery` (no stderr, no warning since 18d0064) and
`tab-D-planted_recovery`, `tab-C-feasibility`, `tab-C-configuration_space`.
