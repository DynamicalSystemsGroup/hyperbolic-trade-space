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
