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

### 6. Review of the paper's move (fresh reviewer)

Reviewed 2026-11-10 at `dev` ff5eb39 (the unit's commits ea46637 and 628df90, and the driver's image reads
after them), in a worktree from `origin/dev` with `uv sync --locked`. Nothing in the tree was changed but this
part. Screenshots and figure copies are in the session scratch folder `paperreview-renders/` (not committed),
named below.

**Run.**

- `uv run pytest -q -n auto` on `test_paper`, `test_case`, `test_k_terms_case`, `test_notebook`,
  `test_paper_sources`, `test_paper_static_figures`, `test_narrative`, `test_claims_register`,
  `test_sensitivity`, `test_gaps` (no marker deselects slow tests): 298 passed, 4 skipped. The skips are the
  gated ones: three need `PAPER_EXECUTE=1`, one `PAPER_BUILD=1` with Node 22.
- The three `PAPER_EXECUTE=1` tests, run here on the Mac (the unit's record names no run of them): 1 passed
  (`test_a_different_facet_order_...`), 2 failed. `test_generated_tables_do_not_move_under_platform_perturbation`:
  `sentence num-margin` moves with the restart order (finding 1). `test_notebooks_execute_from_a_clean_kernel_...`:
  `tab-C-datasets` differs only in the planted table's hash (Mac `c127dd4c...`, committed `b17d4f8f...` from the
  container); that hash is unchanged since before the unit, and Appendix F.2 confines exact comparisons to the
  environment of record, so this one is the platform, not the move.
- `PYTHONPATH=examples/adcs uv run python -m experiments verify`: 34 entries (11 current), 0 drifts.
- `uv run python scripts/check_vocabulary.py`: 70 violations, 0 known: 14 in `src/` docstrings, 41 in the two
  paper notebooks, 14 in `docs/`, 1 in `glossary.yaml`. The same check at ea46637^ gives 71; the unit
  introduced none and removed one ('across temperature').
- Both notebooks' output cells (18 and 37 outputs): no `stderr` stream, no error output, no `Warning`, no
  `Traceback`.
- `uv run python scripts/stage_site.py --serve` built the docs and both paper pages (port 8765 was held by
  another process; served on 8779) and was stopped afterwards. Console: debug messages only, no error.
- The two view PNGs are byte copies of `examples/adcs/model_v2/views/{assembly,behavioural}_view.png` at 0fab294
  (views generator revision 6).

**Figures, cold sentence first, then the caption and lines read against it.**

| figure (file in `paperreview-renders/`) | cold sentence from the image alone | verdict |
|---|---|---|
| `paper-fig-tau-sweep.png` | The fraction above V = 1 and the effective sample fall as tau grows; at the marked tau = 38.1 (n_eff = 23) the K = 1 exponent sits on five metrics led by total mass (0.36), the same five at every tau, control effort dropping out above about 25. | Caption claims what the image shows: exponents printed in the outlined column, n_eff at the line, white rows last, scale top 0.36 = the sweep's largest (D.1: 0.3587). Finding 9 on the lines. |
| `paper-fig-planes-k1.png` | Designs in the log total mass, log energy balance plane, a wide cloud crossed by one straight line with many designs above it. | Pair is total mass and energy balance; the caption's slice sentence explains the designs above the line. Passes. |
| `paper-fig-planes-k3.png` | Three slices, one straight labelled segment each (facet 1, 2, 3); the bottom slice is discrete: a tight left column, a middle group, a wide right band, and two levels of bands. | Passes except finding 6 (the "three columns" sentence). |
| `paper-fig-chart-level.png` | Most designs lie below the flat line log V = 0 at every Z0; a few reach or cross it. | Passes; "first of eight" is right for nine metrics. |
| `paper-fig-tensions-k3.png` | Two correlation matrices of the nine metrics with a five-cell outlined set each, and between them a panel holding only "Too few near-frontier designs for an association reading: 3 of ten". | Two term panels and the thin term's sentence, as the caption says. Findings 7 and 8. |
| `paper-fig-regimes.png` | The two regimes outline different five-metric sets: total mass and energy balance only in primary, control effort and power margin only in stock; three shared. | Matches `num-regimes` and D.4. Passes. |
| `paper-fig-nlemma.png` | Three exponent vectors on a triangle, each in a corner, edge or interior face beside its planted ring. | Bytes only changed; passes. |
| `paper-fig-assembly-view.png` | The cubesat's part tree with swap tags on wheel and tracker and tune tags on panel, battery and controller. | Caption no longer claims ranges are drawn. Passes. |
| `paper-fig-behavioural-view.png` | Requirements grouped by subsystem, each with an orange line to one green traded metric; a measured-slew box and an analysis box supply the metrics; three requirements at top read none. | The dashed clause is gone. Finding 10. |
| `adcs-k3_*.png` (six) | Scatter planes and position planes with designs coloured by facet; per-term tension matrices with term 2 empty. | Not in the paper. Finding 11. |

`figure1.png`, `fig-chart-k3.png` and `fig-predict-check.png` were not changed by the unit and are not on the paper
page; not judged.

**Pages seen** (browser pane, 1280 px wide, dark scheme; then 375 px). Paper: `paper-00-abstract.jpg` to
`paper-24-12-13-14.jpg` (every section; case construction and case analysis screen by screen, `paper-09` to
`paper-22`). Supporting material: `supp-A.jpg`, `supp-B.jpg`, `supp-C-C1.jpg`, `supp-C2.jpg`, `supp-C4.jpg`,
`supp-C6-C7.jpg`, `supp-D-D1.jpg`, `supp-D2-D3a.jpg`, `supp-D3b-term2-sentence.jpg`, `supp-D4-D5.jpg`,
`supp-D6-D7.jpg`, `supp-D9-D10.jpg`, `supp-D11.jpg`, `supp-D12-D13.jpg`, `supp-D14.jpg`, `supp-D15-D16.jpg`,
`supp-E.jpg`, `supp-F-F1.jpg`, `supp-F4.jpg`, `supp-G.jpg`; the full page text of both pages,
`page-text-paper-1280.txt` and `page-text-supporting-material-1280.txt`. Phone: `mobile375-paper-top.jpg`,
`mobile375-paper-fig8.jpg`. Mathematics rendered, no raw markup, no stderr or warning text, every paper figure
present at 725 px (the two views at their native 700 px) with its caption. At 375 px the page does not scroll
sideways (tables scroll in their boxes); figure text is small there, which is not a requirement.

Numbers in prose against their tables, all equal: 659 and 126 (D.9; 725 and 152 for stock); n_eff 23.1 and 56
near-frontier designs (D.4, D.5); the K = 1 5-lemma and exponents 0.14 to 0.36 (D.3: 0.1363 to 0.3577); the K = 3
shares 0.241, 0.034, 0.724 and sets of 5, 4, 5 (D.2, D.3); control effort and peak slew power leading terms 2 and
3 (D.3: 0.397, 0.612); margin 0.00121, radius 9.94e-05 to 9.95e-05, band 0.0088, median 0.237 (D.8); mean slack
0.243, 0.182, 0.146 at 38, 94, 113 and 0.13, 0.09 refitted (D.2, D.15: 0.132, 0.088); candidates -0.197 to -0.153
(D.7); the check 3 of 3 and 1 of 3, errors 0.5 to 1.1 bands, band 0.0935 (D.10: 0.506 to 1.05; 0.0484 / 0.517).
The reach 0.6222 has no table (finding 4).

**Findings.** One finding blocks (a failing gated test). Otherwise the pages build, every number in prose equals
its table, and every regenerated figure shows what its caption says, with the narrowings below.

1. Blocks (a failing test). `num-margin`: with the restart order shifted (`paper_perturb.py --restarts 7`) the
   sentence's count "here 11 of the 706" becomes "here 10 of the 706"; every other number in it holds.
   `num-margin` is not in `[perturbation].moves_under_restart_shift` of `paper/environment_values.toml`, so
   `test_generated_tables_do_not_move_under_platform_perturbation` fails. The count is printed exactly although
   it moves: print it as the range over restart orders, or bound it, or move the name to the list with its audit
   line; which is the paper stream's call.
2. Does not block (wording, claim). `num-predict-reading`: the paragraph opens "Two of them are one
   configuration." with no antecedent (it stands in section 10, a section after the proposals), as the builder
   reported; and it closes "Three proposals illustrate and do not estimate a rate" although two of the three
   are one design (D.10 rows proposal_1 and proposal_3 identical): two distinct designs were checked.
3. Does not block (vocabulary). One object, two names on adjacent figures: the unit's new text says "term"
   (`fig-tensions-k3` caption, lines and panel titles; D.3's "Term 2: ..." sentence; the tail of `num-k-sweep`),
   while `fig-planes-k3` labels the same pieces "facet 1, 2, 3", D.3's table heads its column "facet", and
   `num-k-sweep` says both in one sentence ("The K = 3 facets have contending sets ...; control effort and peak
   slew power ... each lead a term of their own"). No new sentence uses "facet".
4. Does not block (claim backing). `sec-case-analysis-5`: the reach values 0.6222 and 0.351 are typed in a
   markdown cell; no generated value, test or claims-register entry pins them (their source is CR-3 of
   `change-register.md` and the comment in `experiments/check_designs.py`).
5. Does not block (claim backing). `tab-D-stability` head (`paper/generate_results.py`): "moves the control effort
   by up to two parts in ten thousand and the settling time by about a microsecond". The settling-time bound is
   in `paper/container/RECORD.md` ("at most 1e-6 s"); the control-effort figure is in no committed record found
   (`sensitivity.json` holds the reported quantities, not attribute movement; CR-2's 1.2e-4 is the platform
   difference, not the jitter).
6. Does not block (caption narrower than the image). `fig-planes-k3-caption`: "the tracker grade places the
   pointing error in three columns" and "both metrics are set mostly by the discrete choices". The image shows a
   tight coarse column and a medium group, but the fine grade spreads over about 1.5 log units of pointing error
   (0.4 to 1.9): a band, not a column. Narrow to three groups with the fine grade's spread wide.
7. Does not block (ink is data; candidate cut). `fig-tensions-k3.png`: term 2's empty panel takes about a third
   of the figure's height (about 500 px at page width) to carry one sentence that the caption and D.3 already
   carry. Dropping the panel would stop nothing.
8. Does not block (wording). `fig-tensions-k3-caption` "w is the fitted exponent, small for some members": on the
   new data term 3's member energy balance prints w=0.00 in grey (D.3: below 1e-12) while the non-members power
   margin and depth of discharge print 0.02; "small" undersells zero, and a cold reader sees an outlined grey
   label beside unoutlined black ones.
9. Does not block (wording). `fig-tau-sweep-lines`: "nor the small values apart off the outlined column (the
   scale is linear)" does not parse.
10. Does not block (caption against image). `fig-behavioural-caption` says the analysis "returns the rest" (seven
   grey lines leave the analysis box), while the box in the image reads "returns 8 of the 9 metrics ... Passed on
   as measured: control effort" and the control effort's line comes from the slew measurement. Consistent in
   substance; a cold reader counts seven against eight.
11. Does not block the paper. `examples/adcs/figures/k3_log_planes_*.png` and `k3_frontier_coordinates_*.png`,
    regenerated by the unit through `k_terms.py`, colour designs by facet ("colour: facet"), the cluster idiom
    `figure-review.md` forbids; `k3_tensions_primary.png`'s title says "per facet" over panels that say "term",
    and term 2's title sits above the other two. They are read by `docs/superpowers/notes/k3-cubesat.md` and the
    interface contract, not by the paper.
12. Does not block (candidate cut). `sec-case-analysis-5`'s parenthesis "on the earlier view with the slew time
    the rule gives 0.351, where 0.35 had been typed with no rule": the paper's reader never meets the earlier view;
    this is the record's history (CR-3). Cutting it would stop nothing for the reader.
13. Does not block (legibility). `tab-C-datasets` is 1976 px wide in an 822 px column; it scrolls in its box and
    the hashes are off-screen until scrolled (`supp-C6-C7.jpg`).
14. Blocks on Linux (the driver's dispatch on 628df90, 4a04e72; added by the PM). `tests/test_soft_fit.py::
    test_r2_default_cubesat_fits_equal_the_recording[primary]` and `[stock]`: the WP17 R-2 recording of the default
    cubesat fits (`tests/data/soft_fit_default_reference.npz`) is the old data's, and the case now reads the data of
    record (the recorded K = 2 tau 113.2 against 94.4 observed). A miss of the unit's slot list: the recording reads
    the case data but is not a paper cell. Fixed forward by its own unit (the recording regenerated in `hts-paper`
    f7b7585c7c58 on the data of record).

### 7. Dispositions of the review's findings

Written by the paper stream at `dev` 5270bf2 (code, prose; built locally as 2155775) and f8877b2 (regenerated in `hts-paper` `8e91e07fb08f`,
`paper/container/RECORD.md`, "Regeneration after the review of the paper's move").

1. Done (listed). `num-margin`'s count is a count at a threshold: in the fit of record two designs' best-minus-second-best
   gaps lie 4 per cent of the band below it and one 3 per cent above; the restart-shifted fit (`--restarts 7`) is another
   optimum (term 3's exponents differ) and counts 10. Both satisfy the sentence's claim (at least one design within the
   band of a seam). A bound or range could not be printed from the fit of record alone, so `sentence num-margin` is in
   `[perturbation].moves_under_restart_shift` with an audit row in `paper/environment_values.toml`, and the docstring of
   `designs_on_a_seam` (which said the count does not move) states it. Mac: the perturbation test failed before on
   `num-margin` only and passes after; it passes in the image.
2. Done. "Two of the three proposals are one configuration."; "Three proposals of two designs illustrate and do not
   estimate a rate." (the count of designs computed from the predictions file).
3. Left: WP24's (the facet/term naming); no new use of "facet" in prose.
4. Done (narrowed). The typed 0.6222 and 0.351 are gone; the sentence states the rule ("a radius that a stated rule
   sets from the data: the 2nd percentile of the pool's nearest predicted distances to the 300 most isolated holes");
   `test_the_proposers_radius_is_the_stated_rule_of_the_check_designs` pins the rule's constants in `check_designs.py`
   and that no value is typed. With 12, the parenthesis on the slew-time view is cut.
5. Done (dropped). "by up to two parts in ten thousand and the settling time by about a microsecond" is out of the D.11
   head: `sensitivity.json` holds no attribute movement and the regenerated datasets are not committed (the scratch
   regenerations give 1.46e-4 relative and 1e-6 s at most). G-17's evidence column in `abstraction-gaps.md` still
   prints "1.5×10⁻⁴ relative" with `sensitivity.json` as its source: for the gap ledger's owner.
6. Done. "three groups: two narrow columns (coarse at the left, then medium) and a wide band for the fine grade".
7. Done. The thin term has no row of its own: its title and sentence stand above term 3's map (60 px against about 250),
   `case.tension_figure`; the caption says "a sentence in its place says so".
8. Done. "w is the exponent at the fit temperature, grey below the participation threshold, so an outlined metric can
   be grey"; `test_cr1` pins the new words.
9. Done. "nor the values off the outlined column, where close exponents share a grey".
10. Done. "the measured slew supplies the settling time and the control effort, which the analysis passes on, and the
    analysis computes the other seven".
11. Left: `k_terms.py` and its figures are another unit's.
12. Done with 4.
13. Left: not a requirement at phone width.
14. Left: the soft-fit unit's.

Additions: Section 8 names MoE and MoP once (length ledger row, Case construction, 39 words with finding 10's caption
words); claims register rows C391 to C399 (the radius rule, the thin term's caption and sentence, the per-term leaders of
`num-k-sweep`, the stability head's two facts, the check reading's 3 of 3 and 1 of 3, the duplicate proposal, the
depth-of-discharge failures).

## WP23 close-out: nine metrics against eight (the supervisor's thresholds, the eclipse reserve out, `dod_ok` a flag), one regeneration on the host

Old: `dev` at bf2a83c (the data gate's `@5` entries, made in the container `hts-paper`, model
`fb1dbd061610`). New: `dev` at b4d0132 (`@6` entries made on the host, macOS arm64, model
`13c10e1c5ef5`; `WP23-closeout-scope-of-work.md`, D-15, D-16). Written by the close-out's executor
from `git show bf2a83c:<path>` against the committed files; every number below is read from those
two trees.

### Changed conclusions (read first)

1. **No conclusion of the paper changes.** The data's sampling, seeds, scenario constants, designs and
   flags are unchanged on all 2000 designs; the eclipse reserve leaves the metric set and `dod_ok`
   enters the case's flags, which together remove the same 131 designs per regime as before (706
   and 780 feasible). The one-term fits (temperatures, objectives, contending sets, near-frontier
   counts 56 and 77; the primary's exponents to the printed digits, the stock's within 3e-04) are
   unchanged; the three-term fits keep their term types, with the stock regime's assignment moving
   by 1 to 3 rows per term and the primary's terms 1 and 2 trading labels (G-10; no prose reads a
   term's number).
2. **Counts that say "nine" say "eight"** (the attributes, the metrics of the nondominated count, the
   behavioural view's caption, Appendix C's tables). The stock regime's nondominated set on all
   attributes falls from 725 to 724 of 780 (one metric fewer can only shrink it); the primary's
   stays 659.
3. **The certificate's stable radius moves** (it scales with the number of metrics): primary K = 2
   from 5.72e-05 to 6.95e-05, primary K = 3 from 9.94e-05 to 1.21e-04; the stock K = 3 margin from
   9.1e-05 to 3.5e-04 with its radius, the assignment having moved. Statuses stay `certified`.
4. **The sentence on the proposals changes in kind**: the check reading now says that they reached the
   four-metric frontier by spending the battery and fail the depth-of-discharge requirement (spike A),
   with a flag-predicting proposer as future work; the earlier clause on the training rows went.
5. **New readings, not moved ones**: the association step (no pair at |Spearman| 0.99; strongest
   power margin and energy balance, 0.982 and 0.988), the requirements read after the fit and the
   three design sets (Appendix D.17); under one conditioning (OD10 (a)) the requirements change the
   one-term contending set by at most one metric, against spike A's own-rows reading (section 6).

### 1. The files

| file | old sha256 (first 12) | new sha256 (first 12) |
|---|---|---|
| `examples/adcs/model_v2/cubesat.sysml` | `fb1dbd061610` | `13c10e1c5ef5` |
| `examples/adcs/data/v2/adcs_designs_cubesat_gains.csv` (`v2-primary@6`) | `0bc823ceaf51` | `d601d82833b6` |
| `examples/adcs/data/v2/adcs_designs_cubesat.csv` (`v2-baseline@6`) | `4ec7514e9ac5` | `9d1f4849ba46` |
| `examples/adcs/data/v2/check_predictions_cubesat.csv` (`v2-check-predictions@6`) | `6b65b2843a99` | `48493bf3f6e6` |
| `examples/adcs/data/v2/check_designs_cubesat.csv` (`v2-check-designs@6`) | `b6facc345c68` | `e3f22d93c7d7` |
| `examples/adcs/data/scope-sensitivity/scope_sensitivity_v2.csv` (`scope-sensitivity-shared-subspace-v2@5`) | `3e0d7df6cab8` | `fd46402c2f61` |
| `examples/adcs/experiments/ledger/ledger.jsonl` | `266dc9b6eea1` | `4508e1770176` |
| `tests/data/v2_first_designs_of_record.csv` | `894277fb237c` | `81241be0b883` |
| `tests/data/soft_fit_default_reference.npz` | `7011617302f7` | `eaa4f647baeb` |
| `examples/adcs/model_v2/views/coverage.md` / `.csv` | `3b730b298d88` / `494b10e96198` | `987500abd780` / `a0488048fedc` |
| `examples/adcs/model_v2/views/behavioural_view.puml` | `c4617a968930` | `2a1b0c9336b0` |
| `examples/adcs/experiments/reports/v1-v2-comparison.md` | `cd52c45a1cbc` | `1a4264f81854` |
| `examples/adcs/experiments/reports/change-register.md` | `273e4318e183` | `e8969c16fd8f` |
| `examples/adcs/experiments/reports/sensitivity.json` | `1fc844ed6d27` | `469bbf138a7a` |
| `paper/stability_extra.json` | `ceae76fbb442` | `82bf1d401168` |
| `paper/paper.ipynb` / `paper/supporting_material.ipynb` | `0eddd5ed4f78` / `5cccd2be6d09` | `53f401409388` / `33dcb0f73991` |

The five ledger entries: none dirty, platform `macOS-26.5.2-arm64-arm-64bit`, `git_commit` 931dbd8
(the pre-rebase hash of 4409920; the trees of the hashed code files are equal), times 15:49 to 15:51
UTC, the note naming the close-out and the host. `PYTHONPATH=examples/adcs uv run python -m
experiments verify`: 39 entries (11 current), 0 drifts. Wall times: `ledger_gate.py --host` 221 s
(run three times: the first two were discarded, below), the first-20 recording 11 s, `coverage.py`
16 s, `experiments.sensitivity regenerate` 18 min, `analyse` 3 min, `stability_extra.py` 3 min,
`build_figures.py` 81 s, the two notebooks 140 s.

Two runs were discarded before the run of record, both with the ledger and data restored to the
committed state: the first because the executor edited `case.py` in the tree while it ran (two
entries marked dirty); the second because `check_designs.Proposer` trained on 811 rows, not 706: its
filter (settled, power_ok, momentum_ok, every traded metric positive) had relied on the reserve's
positivity to drop the depth-of-discharge failures, a second hidden dependency of the A1 call, fixed
by `dod_ok` in its filter (4409920) before the run of record.

### 2. Every moved number, column by column

**The two 1000-design tables.** `eclipse_reserve_wh` gone (cause: the reserve's calc left the model,
D-11; CR-5). Every other column inside the reproducibility tolerances of the frozen files; against
the gate's container files (old) the host's values differ in `control_effort` (445 primary, 161
baseline rows above 1e-6 relative; largest 7.4e-05 and 1.2e-04), `torque_saturated_frac` (514, 168;
largest 0.13 and 0.23 relative, 0.009 absolute), `peak_momentum_nms` (12, 3; largest 3.3e-05) and
`slew_loss_energy_wh` (232, 69; largest 7.3e-05). Cause: the platform (the adaptive integrator's
accepted steps differ between the container and the Mac, the gate's CR-2); the host's files are back
inside tolerance of the frozen Mac files, so the gate's CR-2 is retired. The settling time, the flags,
the categorical values and every accounting column are equal to `%.9g` on all 2000 designs.

**The check predictions and designs.** The same three proposals (two configurations) at the reach
0.6222, as at the gate; predicted coordinates and scores differ by at most 5e-05 relative, the
simulated rows as the tables above (control effort 2e-06 absolute, saturated fraction 0.004). Cause:
the platform. `eclipse_reserve_wh` gone from the designs file.

**The first-20 recording and the scope-sensitivity file.** As the tables: the reserve's column gone,
the platform's differences in the step-summed columns.

**The case's records** (old: the nine-metric fit on the gate's data; new: the eight-metric fit).

| quantity | old | new | cause |
|---|---|---|---|
| feasible designs | 706, 780 | 706, 780 | `dod_ok` removes the 131 per regime the reserve's positivity removed (Appendix C.3 gains a `dod_ok` row: 131 fail, 105 and 117 removed; "all attributes positive" now removes 0) |
| K = 1 tau, objective, frac above | 38.10, 0.2434, 0.092; 45.68, 0.1786, 0.104 | equal | the reserve carried no exponent at K = 1 |
| K = 1 contending sets, exponents | as recorded | primary equal to the printed digits; stock within 3e-04 (pointing error 0.03924 to 0.03927, depth of discharge 0.01163 to 0.01195; the reserve's 0.00037 gone) | the reserve's small stock exponent redistributed |
| K = 1 stock gap (single-term diagnostic) | 1.29e-05 | 1.24e-05 | the metric set |
| K = 3 primary terms | rows 162 / 181 / 363, shares 0.24 / 0.03 / 0.72; the thin term is term 2 | equal as a set; terms 1 and 2 trade labels in D.2 and D.3, the thin term is now term 1 | the restart that wins (G-10); no sentence reads a term's number |
| K = 3 stock terms | rows 251 / 184 / 345; frac above 0.0936; peak slew power 0.428 | 253 / 185 / 342; 0.0910; 0.424 | the metric set: a row near a seam moves |
| stable radius K = 2 / K = 3 primary; K = 2 stock | 5.72e-05 / 9.94e-05; 1.195e-04 | 6.95e-05 / 1.21e-04; 1.327e-04 | the radius scales with the dimension |
| margin / radius K = 3 stock | 9.1e-05 / 7.7e-06 | 3.5e-04 / 3.3e-05 | the assignment moved (row above) |
| zero sets across tau | primary: power margin, eclipse reserve, peak slew power; stock: peak slew power | primary: power margin, peak slew power; stock: peak slew power | the reserve left |
| nondominated on all attributes | 659 of 706 (9); 725 of 780 (9) | 659 (8); 724 (8) | one attribute fewer |
| D.1 temperature sweep, stock | metrics with w > 1e-3: 8, 7, 7, 7 | 7, 6, 6, 6 (n_eff 370.2, 147.6, 45.02, 16.68) | the reserve contended at low tau |
| D.5 robust scaler | primary tau 54.77, 6-lemma with the reserve; stock tau 65.68 | 78.75 both; the reserve's place taken by depth of discharge | the reserve's log-IQR scale entered the robust conditioning |
| D.6 large-wheel refit | 7-lemma with the reserve | 6-lemma | the reserve left |
| D.4 stock associations | settling-mass -0.12 (+0.04); pointing-effort -0.65 (-0.70); settling-pointing +0.66 (+0.71) | -0.10 (+0.05); -0.63 (-0.69); +0.63 (+0.70) | the report's association is read in the fit's coordinates over all metrics |
| D.12 conditioning diagnostic, K = 3 | 9, 9.3; 0.21 | 9.3, 9; 0.23 | the term labels (G-10) and the metric set |
| D.16 PCA directions | 0.437, 0.238, 0.173 with the reserve loading | 0.444, 0.238, 0.159; depth of discharge in its place | the reserve left the chart |
| D.10 propose-predict-check | 0.0484, 1.05 | 0.04836, 1.055 | printed digits under the regenerated stability record |

### 3. The conclusions, item by item

- Contending sets (K = 1, both regimes; each term at K = 3): unchanged in membership and order.
- Leaders: unchanged (total mass 0.358; control effort 0.432; at K = 3 peak slew power 0.612 primary,
  0.424 stock against 0.428).
- K = 3 term types: unchanged in both regimes; the thin term (3 near-frontier designs, primary)
  remains thin.
- Zero sets: the reserve leaves the primary's; nothing enters.
- Temperatures: unchanged at every K in both regimes.
- Certificates: all `certified` at K = 2, 3; gaps below 1e-12; radii and the stock K = 3 margin move
  (section 2).
- Check outcomes: unchanged (energy differential within the band 3 of 3, position 1 of 3); the
  proposals still fail `dod_ok`, now said with spike A's reading.
- Counts: feasible 706 and 780; near-frontier 56 and 77; nondominated 659 and 724 (725 before).
- Flags: `settled`, `momentum_ok`, `power_ok`, `dod_ok` equal on every design; `dod_ok` is now one of
  the case's flags (`case.CUBESAT.flags`).
- The thresholds move no flag: they are requirements read after the fit, not feasibility flags.

### 4. The paper's and the docs' slots, by cell id, with cause

Paper (`paper/paper.ipynb`): `num-attributes`, `num-datasets`, `num-nondominated` (nine to eight);
`sec-case-construction-1` (eight MoPs to seven) and `fig-behavioural-caption` (eight metrics; the
analysis computes six; the negated satisfy said) for the reserve's removal; `sec-case-construction-1b`
(the four requirements and the baseline's failure of the pointing-error requirement, 63.7 %),
`sec-case-analysis-5` (the proposals' sentence), `sec-discussion` (the two candidate sentences) and
`num-predict-reading` (spike A's finding) for D-18; `num-margin` (the radius); `num-k-sweep` (term
labels); `fig-tau-sweep`, `fig-tensions-k3`, `fig-regimes` and the static figures `fig-planes-k1`,
`fig-planes-k3`, `fig-chart-level`, `fig-nlemma`, `fig-behavioural-view` (redrawn without the
reserve).

Supporting material: `app-C-job`, `tab-C-evaluation`, `tab-C-attribute_sources`,
`tab-C-conditioning`, `tab-C-metric_table` (the reserve's row gone); `tab-C-feasibility` (the
`dod_ok` row); `tab-C-datasets` (the `@6` entries and hashes); new `app-C-5-associations`,
`tab-C-metric_associations`; `tab-D-temperature_selection`, `tab-D-k_diagnostics`,
`tab-D-exponents_and_terms` (and the association sentence), `tab-D-regime_comparison` (and the
sentence), `tab-D-sensitivity_variants`, `tab-D-refits_by_category`, `tab-D-termination_records`,
`tab-D-margin_reading`, `tab-D-nondominated`, `tab-D-propose_predict_check`, `tab-D-stability`,
`tab-D-conditioning_diagnostic`, `tab-D-pca_chain` (section 2's causes); new `app-D-req`,
`tab-D-requirements_at_the_frontier`, `app-D-req-sets`, `tab-D-design_sets_comparison` (D.17);
`tab-E-gaps` (the mathematics as the `{math}` role, R-31); `tab-F-toolchain` (the platform of the
build, the host) and `tab-F-reproduction` (the new table functions listed).

Docs (`docs/examples.md`): eight attributes; the "No metric twice" bullet; the new section
"Requirements read after the fit" (two generated text blocks); the alt texts and caption (eight
metrics, seven position coordinates); the ternary limit (an eight-metric case). The figures rebuild
from the data.

Added after the acceptance review (its G-2 and O-5; the fix-forward): `fig-planes-k1-caption`,
`fig-planes-k1-lines` and `fig-planes-k3-caption` ("the other seven metrics" to six: a plane shows two
of the eight) and `fig-chart-level-caption` ("the first of eight position coordinates" to seven: d
metrics give d − 1 position coordinates), markdown only, for the reserve's removal; `tab-E-gaps` (its
rows G-2 and G-17 read the eight-metric data: "eight-metric data", "eight fitted attributes", "659 of
706 on eight attributes", "74 of 685 quantities" not identical at the printed precision, counted from
`sensitivity.json` by `sensitivity._fmt`'s rule, the same rule that gives 80 of 693 on the gate's
file; M3 and M5 re-measured: the stock regime's K = 3 conditioning 9.28, 0.214, 10.1 to 9.32, 0.228,
10.2, and at τ/2 and 2τ the stock fit keeps six participants, not seven and six; the primary's numbers
unchanged), from `docs/superpowers/notes/abstraction-gaps.md`; `tab-C-metric_associations`,
`tab-D-exponents_and_terms`, `tab-D-regime_comparison` (the association sentence names the regimes as
the paper does, "primary regime", "stock regime", not the dataset labels; the driver's decision on
O-5). Those four output cells were re-executed on the host and spliced; every other cell of
`supporting_material.ipynb` is byte-equal. Docs: the regimes "primary | stock" in both generated
blocks and "the primary regime's table (aggressive controller gains)" in the opening paragraph, for
the same decision.

### 5. What the regeneration is not

No change to `src/`, `derivation/`, the frozen `examples/adcs/data/*.csv` or the v1 model. The
exact-equality branches (the container of record, `HTS_ENVIRONMENT_OF_RECORD=1`) are not re-pinned
here: the first-20 recording, the soft-fit reference (now `recorded_on` darwin arm64), the
environment reference and `RECORD.md` are the driver's container regression at the gate.

### 6. OD10 (a): spike A's own-rows numbers against the feasible set's conditioning

Spike A conditioned each design set on its own rows; the close-out applies the feasible set's
conditioning to every set (`case.design_sets`, the temperature rule the same, each set's
temperature selected on its rows). Only the "all designs" and "requirements met" rows can differ
(the feasible rows are the fit of record in both).

| regime, set | spike A (own rows) | close-out (feasible set's conditioning) |
|---|---|---|
| primary, all designs (U8) | tau 38.1; total mass 0.324, energy balance 0.221, pointing error 0.160; set total mass, energy balance, pointing error, settling time, depth of discharge | tau 31.8; total mass 0.357, energy balance 0.181, pointing error 0.163; the feasible set's order |
| primary, requirements met (R) | tau 65.7; **pointing error 0.296, peak slew power 0.240, total mass 0.158**; a 6-lemma with peak slew power and power margin; zero: energy balance, eclipse reserve; K = 3 shares 0.70 / 0.20 / 0.10 led by pointing error | tau 65.7; **total mass 0.357, energy balance 0.184, pointing error 0.177**; the feasible set's 5-lemma; zero: control effort, power margin, peak slew power; K = 3 every term led by peak slew power and pointing error (0.09 / 0.18 / 0.73) |
| stock, all designs (U8) | tau 31.8; control effort 0.407, settling time 0.310, power margin 0.205; set control effort, settling time, power margin, pointing error, total mass | tau 29.0; 0.414, 0.334, 0.190; the same set |
| stock, requirements met (R) | tau 31.8; power margin 0.215, control effort 0.205, total mass 0.188; a 6-lemma; zero: energy balance, eclipse reserve, peak slew power | tau 54.8; control effort 0.441, settling time 0.305, energy balance 0.212; control effort, settling time, energy balance, pointing error, depth of discharge; zero: total mass, power margin, peak slew power |

Reading: the constrained set's changed contending set in spike A (pointing error against peak slew
power, primary) was the re-conditioning of the 288 rows, as spike B's section 4 found; in one
conditioning the constrained set keeps the feasible set's contending set in the primary regime and
swaps power margin for energy balance (Spearman 0.988 over the feasible designs) in the stock
regime, and the three-term fit of the constrained set is what moves (the peak-slew/pointing term
covers it). The Discussion's candidate follows this table, not the spike's: the requirements cut
designs (19 of 56 and 43 of 77 near-frontier designs), not what the frontier trades.

**Added after the acceptance review (its G-3).** The rest of what differs from spike A, each with
spike A's value, the recomputed value (`case.design_sets_table`, `case.design_sets_placement` at
ebd7dfe's data) and the cause.

| item | spike A | close-out | cause |
|---|---|---|---|
| stock, requirements met, three-term fit (term: two largest exponents; share) | energy balance 0.36, control effort 0.28 (0.63) / control effort 0.44, settling time 0.30 (0.00) / total mass 0.27, pointing error 0.21 (0.38) | control effort 0.293, energy balance 0.272 (0.60) / control effort 0.461, settling time 0.300 (0.00) / peak slew power 0.356, total mass 0.216 (0.40) | the conditioning rule (OD10 (a)); the third term gains peak slew power ahead of total mass |
| placement, "all designs" column | read on U9 (nine metrics, positivity only): baseline configuration −0.46 primary, −0.07 stock; fast_effort_hungry −0.20, −0.14; precise_heavy_sensor −0.15, +0.02; light_slow −0.18, −0.34 | read on U8 (all 1000 designs, eight metrics) in the feasible set's conditioning: −0.499, −0.075; −0.166, −0.125; −0.125, +0.031; −0.147, −0.356 | the set (U9 against U8: the reserve left the metrics) and the conditioning rule |
| placement, "requirements met" column | baseline configuration −0.93 primary (rank 0.00), −0.26 stock (0.27); fast_effort_hungry −1.42 (0.00), −0.40 (0.10); precise_heavy_sensor −1.06 (0.00), −0.31 (0.20); light_slow −0.07 (0.65), −0.24 (0.32) | −0.566 (share below 0.01), −0.030 (0.80); −0.257 (0.22), −0.196 (0.38); −0.191 (0.36), −0.131 (0.51); −0.227 (0.27), −0.420 (0.15) | the conditioning rule: spike A re-conditioned the 288 and 302 rows, so the large-wheel candidates fell outside the constrained set's range ("seven times further off"); in the feasible set's conditioning in the primary regime they sit 0.04 to 0.06 below their feasible-fit level |
| placement, the proposals | "not placeable" (a nine-metric fit's conditioning refuses a non-positive reserve) | placed in every column: primary −0.543 / −0.570 / −0.591 (proposals 1 and 3), −0.630 / −0.660 / −0.688 (proposal 2); stock −1.034 / −1.146 / −1.503, −0.843 / −0.956 / −1.362; flagged as failing the flags (`dod_ok`) | the eight metrics (the reserve left), so the conditioning accepts them |

The "feasible" column equals spike A's F column at its printed digits for every design (for example
the baseline configuration −0.52 and −0.06; spike A printed K = 1 / K = 3, the table prints K = 1
with the band count and the share below). The reading above stands: in one conditioning the
requirements-met fit places the candidates near where the feasible fit does, and spike A's
extrapolation remark (rank 0.00 for the large wheels) was the re-conditioning.

### 7. Two notes from the acceptance review (G-4, O-1)

**R-17's grep (G-4).** `experiments/compare.py` keeps `eclipse_reserve_wh` in `ORIENTATION` and
`POWER` on purpose: the v1-v2 report reads the frozen v1 frames, which carry the column; a comment at
the lists now says so. `experiments/cubesat_oracle.py`'s docstring names the reserve only to say the
oracle's output leaves it out (lines 25 to 27), which is the data of record; the file is hashed by
the ledger (`code` of the v2 entries), so it changes only with a regeneration and is left as is.

**The pointing-error pass share (O-1).** 95.0 % (D.17, the docs page) is exact for the model's limit:
671 of the 706 feasible primary designs have a pointing error at or below 0.008495 degree (95.04 %).
94.9 % (the model's doc in `cubesat.sysml`, `case-model.md`, `WP23-decisions.md`) is the share at the
ladder's unrounded 95th percentile, 0.0084945 degree (linear interpolation), which admits 670 (94.90 %):
one design, at 0.00849489 degree, lies between the percentile and the rounded limit. The generated
tables keep the exact share; `cubesat.sysml` is ledger-hashed and not changed here, and
`case-model.md` is outside this unit's files: making them print 95.0 % is a later edit (the model's
doc at its next regeneration).


## WP30 data gate: eight metrics on 1,000 designs against thirteen metrics on 3,000 designs

Written 2026-11-11 by the gate runner of WP30 (D-8, R-6, R-9). Old: the WP23 close-out state at `dev`
b22821e (ledger entries `v2-primary@8`, `v2-baseline@8`, `v2-check-predictions@8`, `v2-check-designs@8`,
`scope-sensitivity-shared-subspace-v2@7`; eight traded metrics, 1,000 designs per regime, regenerated in
the container `hts-paper`). New: the host regeneration on macOS arm64 at the branch head (`v2-primary@11`,
`v2-baseline@11`, `v2-check-predictions@11`, `v2-check-designs@11`, `scope-sensitivity-shared-subspace-v2@10`;
thirteen traded metrics, 3,000 designs per regime, nine workers, 9.2 minutes for the five entries,
`git_dirty` false, model hash `fe6de947d18f`). The container run is the reference later (step 14); this
section is the host's. Three configurations through `case.py` (script and output committed in
`work-packages/WP30-rounds/data-gate/`: `conclusions.py`, `render.py`, `conclusions.md`, `k-record.txt`):
**old8**, the old files with the eight-metric spec (the paper as committed); **new8**, the new files
with the same eight-metric spec (what the regeneration and the larger sample change on their own); **new13**,
the new files with the thirteen-metric spec of the case. A quantity equal in old8 and new8 but not in new13
moved because of the new metrics; a quantity that differs between old8 and new8 moved because of the
data (the sample size and the platform).

### Changed conclusions (read first)

1. **The baseline regime's K = 1 trade is led by the energy-balance axis, then the momentum headroom,
   the settling time and the total mass; the control effort is out of the lead.** Old: control effort,
   settling time, power margin, pointing error, depth of discharge (5), led by control effort 0.432 then
   settling time 0.319. New: momentum headroom, available power, total mass, settling time, pointing
   error, depth of discharge, unit cost, fleet cost (8), led by available power 0.192, momentum headroom
   0.181, settling time 0.159, total mass 0.131, control effort 0.076. The available power is one axis
   with the energy balance (Spearman +0.9997, both regimes), so the 0.192 is that axis's weight (the
   energy balance carries exponent zero beside it). Cause: the momentum headroom (new8 keeps control
   effort 0.435 and settling time 0.318 leading, so neither the sample nor the platform moved the
   lead; the new metrics did).
2. **The primary regime's K = 1 trade is led by the unit cost; the total mass has left the set.** Old:
   total mass 0.358, energy balance 0.184, pointing error 0.164 (set of 5: total mass, energy balance,
   pointing error, depth of discharge, settling time). New: unit cost 0.257, available power 0.197,
   pointing error 0.156, fleet cost 0.151, momentum headroom 0.107, settling time 0.068 (set of 7: unit
   cost, available power, pointing error, fleet cost, momentum headroom, settling time, depth of
   discharge); the total mass has exponent 0.021 and is no longer contending. Cause: the cost metrics
   price the mass (new8 keeps total mass 0.349 leading).
3. **Which metrics the fit weights.** Pairs at or above 0.99 (Spearman among the feasible designs):
   available power with energy balance, +0.9997 in both regimes (the association step's merge); no other
   pair. Pairs at or above 0.95: power margin with energy balance (+0.982 primary, +0.987 baseline) and
   with available power (+0.982, +0.988); depth of discharge with the battery peak power ratio (-0.971,
   -0.975). Exponents at K = 1: power margin 0 in both regimes, energy balance 0 (primary, 1.8e-17) and 0
   (baseline), the battery peak power ratio 0 in both (1e-20 or less), the available power 0.197 and 0.192,
   the momentum headroom 0.107 and 0.181 (takes part). These are the three readings of "No floating
   requirements": the power requirement reads an axis the fit weights, the battery requirement a metric
   at exponent zero, the momentum requirement a metric that takes part.
4. **Counts.** Feasible designs: 706 and 780 on the first 1,000 rows (no design's four flags changed:
   `settled`, `power_ok`, `momentum_ok`, `dod_ok` are equal row by row), 2,134 and 2,355 on the 3,000.
   Nondominated designs on all attributes: 659 of 706 and 724 of 780 on eight metrics become 2,134 of
   2,134 and 2,355 of 2,355 on thirteen (with thirteen metrics no feasible design is dominated); the
   four-metric view 126 and 152 become 236 of 2,134 and 306 of 2,355 (new8 gives the same, so the larger
   sample alone moved it).
5. **K = 2 and K = 3, by regime (term rows, shares, contending sets).** Primary K = 2: old terms of 414
   and 292 rows (shares 0.800, 0.200); new 934 and 1,200 rows (0.262, 0.738): term 1 unit cost, available
   power, fleet cost, momentum headroom, pointing error, settling time, depth of discharge (7), term 2
   peak slew power, pointing error, unit cost, available power, fleet cost, momentum headroom, settling
   time, depth of discharge (8). Primary K = 3: new terms of 621, 1,054 and 459 rows (0.344, 0.594, 0.061),
   led by energy balance 0.384, peak slew power 0.417 and momentum headroom 0.223; old 181, 162 and 363
   rows (0.034, 0.241, 0.724). Baseline K = 2: old 454 and 326 rows (0.562, 0.438); new 986 and 1,369
   (0.754, 0.246), term 1 led by peak slew power 0.378, term 2 by settling time 0.223 with available power
   0.204 and control effort 0.185. Baseline K = 3: old 253, 185 and 342 rows (0.115, 0.462, 0.423); new 853,
   705 and 797 (0.405, 0.061, 0.534): term 1 energy balance 0.371, term 2 control effort 0.373 with settling
   time 0.354, term 3 peak slew power 0.371. The per-term report does not refuse in either regime at
   either K (near-frontier rows per term at the K = 1 band: primary 188, 297, 50; baseline 175, 38, 261).
   The K = 1 set is contained in the union of the K = 2 terms in both regimes except as follows: baseline
   K = 3, where total mass (a K = 1 member) is in no term's set (union of 10, K = 1 not a subset).
6. **Selected temperatures and effective sample size.** K = 1: primary 38.10 becomes 41.72 (new8 26.50:
   the sample changes the temperature, the metrics move it back), baseline 45.68 stays 45.68 (new8 29.01).
   K = 2: 94.42 becomes 113.22 and 71.92 becomes 103.40. K = 3: 113.22 becomes 135.76 in both regimes.
   Effective sample size at K = 1: 23.1 becomes 73.6 (primary) and 14.6 becomes 47.9 (baseline); the
   near-frontier designs at K = 1: 56 and 77 become 238 and 293.
7. **Certificates unchanged in status:** `not_applicable`, `certified`, `certified` at K = 1, 2, 3 in both
   regimes; the margins at K = 2 and 3 are 0.000377 and 0.000421 (primary), 0.000263 and 0.000100
   (baseline), the stable radii 0.000026, 0.000029, 0.000017 and 0.000007 (were 0.000697, 0.001213,
   0.001413, 0.000350 and 0.000069, 0.000121, 0.000133, 0.000033). K = 3 over five seeds: one solution,
   certified every seed. The K = 3 record has no row where the fit refuses.
8. **The check.** Three proposals at reach 0.6947 (the stated rule on the new pool); proposal_1 and
   proposal_3 are one design again (medium wheel, fine tracker). Log V within the band for 3 of 3 and
   position within the band for **3 of 3** (was 1 of 3: 1.05, 0.51 and 1.05 bands); `dod_ok` False for 3 of
   3 as before. The three named candidates' log V: fast_effort_hungry -0.197 becomes -0.162, precise_heavy_sensor
   -0.153 becomes -0.130, light_slow -0.171 becomes **-0.402** (rank among the training designs 0.58 becomes
   0.006: on thirteen metrics the light, slow candidate is far beyond the sample's frontier, by the cost
   metrics). The candidates remain 0 of 3 beyond the surface.
9. **Association signs.** Primary (settling time, pointing error): +0.03 (+0.15) becomes +0.36 (+0.47);
   (settling time, total mass) -0.50 (-0.50) becomes -0.46 (-0.46); (pointing error, control effort)
   -0.36 (-0.50) becomes -0.52 (-0.66). Baseline (settling time, total mass): -0.10 (+0.05) becomes -0.16
   (-0.14), **the Spearman sign changes**; (settling time, pointing error) +0.63 (+0.70) becomes +0.68 (+0.76);
   (pointing error, control effort) -0.63 (-0.69) becomes -0.69 (-0.77).
10. **Platform.** The first 1,000 rows' inputs (design variables, categories, seeds) and the flags equal the
    old ones exactly. The outputs differ because the old files are the container's (Linux) and the new the
    host's: settling time by at most 5.4e-9 relative, energy balance 1.3e-8, depth of discharge 1.7e-8 (last
    digits), control effort 7.4e-5 (primary) and 1.2e-4 (baseline), peak momentum 3.3e-5, slew loss energy 7.3e-5,
    and the torque-saturated fraction by up to 0.13 and 0.23 relative (the registered platform difference
    of the first section of this file). "Equal exactly" (R-6) is therefore the container run's to show (step 14);
    on the host the first 1,000 rows agree to the tolerances above and the flags agree exactly.
11. **Cost limits** (`work-packages/WP30-rounds/cost-ladders.md`, repriced from the configurations and checked
    against the data's cost columns to 5.5e-9, which is the nine-digit rounding of the files): share of the
    feasible designs at or under the unit cost limit of 350,000 USD: 0 percent at a fleet of one (the
    baseline configuration costs 461,360 USD with launch), 37.2 and 34.5 percent at three satellites
    (primary, baseline), 78.1 and 77.9 at ten, 95.4 and 95.7 at thirty, 77.5 and 77.2 averaged over the
    free fleet size 1 to 30. At the fleet cost limit of 6,000,000 USD: 100 percent through ten satellites,
    0 at thirty, 69.7 and 69.2 averaged over the free size; at 8,000,000 USD, 42.7 and 40.8 at thirty, 91.4 and 91.2 averaged. The three
    calibration fractions of `WP30-decisions.md` (82, 71 and 93 percent) were on the earlier coefficients.
12. **Unchanged:** the four flags of every design in the first 1,000 rows; the two feasible counts on them
    (706 and 780); the certificate statuses; the six check designs (three candidates, three proposals).

### 1. The files

| dataset | old rows | new rows | columns old / new | added | removed |
|---|---|---|---|---|---|
| `data/v2/adcs_designs_cubesat_gains.csv` (primary) | 1000 | 3000 | 32 / 37 | `fleet_size`, `momentum_headroom`, `battery_peak_power_ratio`, `unit_cost_usd`, `fleet_cost_usd` | none |
| `data/v2/adcs_designs_cubesat.csv` (baseline) | 1000 | 3000 | 32 / 37 | the same five | none |
| `data/v2/check_predictions_cubesat.csv` | 3 | 3 | 25 / 26 | `fleet_size` | none |
| `data/v2/check_designs_cubesat.csv` | 6 | 6 | 31 / 36 | the same five | none |
| `data/scope-sensitivity/scope_sensitivity_v2.csv` | 20 | 20 | | the same columns | none |

`available_power_w` was an auxiliary column and is now a traded metric (same column, moved up). The
three named candidates keep a fleet of one; the proposals and the check designs keep the fleet size the
pool draws (the gate's choice, recorded in `WP30-build-notes.md`). Output hashes (12 hex): `v2-primary@11`
`e4ab2fca5c74`, `v2-baseline@11` `57c208c91c59`, `v2-check-predictions@11` `05649b15348c`,
`v2-check-designs@11` `1cab3bafa3fe`, `scope-sensitivity-shared-subspace-v2@10` `25425be01309`. The
run was repeated on a clean tree after a first run written with an uncommitted tree: the outputs are
bit-identical (`@10` and `@11` carry the same hashes). The 2,000-design run (`@9`) is history too. The five
older ledger entries that hash `cubesat_model.py` or `legacy_oracle.py` (four adopted v1 datasets and the
legacy shared-subspace sample) were re-adopted as `<id>@2` with `experiments adopt --readopt`: new code
hashes, the frozen outputs unchanged, `verify` reports 0 drifts.

### 2. The full tables

Every number above is in `work-packages/WP30-rounds/data-gate/conclusions.md` (old8 | new8 | new13 side by
side: temperatures, contending sets, term tables at K = 2 and 3, certificates, association pairs,
redundancies, nondominated counts, regime comparison, candidates, propose-predict-check) and the K = 1, 2, 3
record in `k-record.txt`.
