# WP4b — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP4b-scope-of-work.md`, including Amendment 1 (R-14 to its two relative clauses) |
| **Scope approval verified** | The project has no PRs, so the recorded act is `work-packages/WP4b-decisions.md`: "Scope approval (approval gate)", supervisor mzargham, verbatim "okay proceed", document at `d27c177` (draft 4 plus the toaster amendment), defaults list approved as one item. "Scope amendment 1: R-14 threshold" records the verbatim choice "Amend R-14 to its intent; keep the dataset"; the amendment text (`aa1f1f1`) drops only the absolute 0.25 and keeps both relative clauses, which is what the choice says. Records typed by the agent, decisions are the supervisor's. |
| **Work reviewed** | `main` at `d0a2c0d`. WP4b commits: `5dfbc8c` (SysML model, model layer, tests, `case` group), `379dee0` (dataset, richness tests, probe note, workflow edit), `c89b5d0` (amendment applied, final numbers, WP7 facts); records `aa1f1f1`, `6b88cda`, `a2f33f4`, `d27c177`. Commits after `d0a2c0d` are other packages' review reports. Start for diffs: `5dfbc8c~1` (`494145a`); WP4 state: `932bbe4` (delivery) and `a9fc4f2` (WP4 acceptance). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4b-decisions.md`, after this report |

A fresh reviewer who built none of WP4b and wrote none of its earlier reviews. Every command below was run in this session with `unset VIRTUAL_ENV`. Review only: nothing was repaired. Trial edits were made in the working tree and undone with `git checkout`; none was committed.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/cubesat_tradespace.sysml` (352 lines) read in full. Contains the part defs, enums, ranges, calc defs, constraint defs, `analysis def ModelTest` and `part cubesatBaseline`. |
| D-2 | met | `examples/adcs/cubesat_model.py` read in full. Loads through `opensysml`, samples from the model, instantiates, evaluates calcs and constraints through the client, `measure()` calls the unchanged simulator. |
| D-3 | met | `generate_dataset.py` diff is additive (`--model`, `--slew-deg`, `--t-end`, spawned pool for cubesat). Ran `--model cubesat --n 20 --seed 0 --workers 2` and the default `--n 20 --seed 0`: both reproduce the committed rows (settling difference 0.0, same columns). |
| D-4 | met | `data/adcs_designs_cubesat.csv`: 1000 rows, 33 columns, seed 0; `design_id` 0..999; scenario columns `slew_deg`, `t_end_s`, `max_step_s`. |
| D-5 | met | `pyproject.toml`: `case = ["opensysml>=0.12.1"]`, `default-groups = ["dev", "case"]`; `uv.lock` +333 lines; `uv lock --check`: "Resolved 173 packages". |
| D-6 | met | `tests/test_cubesat_model.py` (25 tests) and `tests/test_adcs_enrichment.py` (10 tests); with `REQUIRE_OPENSYSML=1`: 35 passed. |
| D-7 | met | `docs/superpowers/notes/adcs-tensions-probe.md` updated (client verification, levers, R-13 and R-14, explanations, WP7 facts). |
| D-8 | met | `work-packages/WP4b-decisions.md` holds the approval, the amendment, the pre-approval decisions; acceptance pending this report. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `git diff 932bbe4..HEAD -- examples/adcs/adcs_sim.py` empty (0 lines), same for `a9fc4f2..HEAD`. `git diff a9fc4f2..HEAD -- tests/test_adcs_case.py` empty; `design_space.py` and `adcs_designs.csv` also unchanged. `pytest tests/test_adcs_case.py` passes inside the full suite. |
| R-2 | met | `git diff 5dfbc8c~1..HEAD` shows `adcs_designs.csv`, `design_space.py` and `test_adcs_case.py` untouched. The default generator run (`--n 20 --seed 0`) reproduces the first 20 committed WP4 rows. There is no new test of the defaults: the check rests on the unchanged WP4 reproducibility tests, which call the modified `generate` with defaults and pass (G-5). |
| R-3 | met | `test_model_loads_strict_and_has_required_symbols`, `test_model_self_check_and_model_test_analysis`, `test_attributes_carry_units`, `test_negative_control_broken_model_fails_strict_load` pass. Part defs for cubesat, bus, panel, battery, wheel, tracker, controller; enums `WheelClass`, `TrackerGrade` with concrete specializations; ranges as `*Min/*Max` attributes; calc defs (`MassAccounting` and others); constraint defs `PowerOK`, `DepthOfDischargeOK`; `analysis def ModelTest`. |
| R-4 | met | Trial (own script): copy of the model with `batteryCapacityMax` 200 to 40 gave sampled maximum 39.97 against 199.49 for the original; renaming `small` to `tiny` in the enum and its specialization gave wheel classes `{medium, large, tiny}`; adding a literal `huge` without a part table raises "enum literals of ReactionWheel without a part definition". The committed tests do the same (`test_editing_a_range_or_enum_literal_changes_the_sampler`). Grep of `cubesat_model.py` for the table and range numbers (0.0003, 0.002, 0.010, 1361, 0.28, 140, 5e4, 2.5, 12.0, 1.13e-3 and so on) finds none; `test_no_duplicated_constants_in_python` scans the SysML tables against the code. Scenario numbers (90 deg, 450 s, 0.5 s) are Python constants, which the scope allows ("scenario numbers are parameters of `measure`"). |
| R-5 | met | Read `cubesat_model.py`: `configure` appends `part cfg_i : Cubesat {...}` usages to the model text and calls `loaded.instantiate`; `accounting` reads `totalMass`, `generatedPower`, `usableWheelTorque` and so on from the instance, which the SysML calcs compute; the energy and power attributes are `model.eval` of `SlewLossEnergy`, `EnergyBalance`, `EclipseReserve`, `PeakSlewPower`, `PowerMargin`, `DepthOfDischarge`. The Python recomputation appears only in tests as the independent check. `test_run_sweep_over_panel_span_matches_python_accounting` (8 rows, 1e-12) and `test_accounting_matches_independent_python_formulas` pass. |
| R-6 | met | `_holds` calls `verify_constraint(..., engine=<from list_engines>)` for `powerOk` and `dodOk` and raises on a verdict error. `test_flags_equal_independent_python_evaluation` passes (flags equal plain Python on 8 designs). Negative controls `test_flags_negative_controls`: 20 Wh battery with fine tracker gives `dod_ok=False`; 60 W housekeeping gives `power_ok=False` and the 1 % torque cap. Dataset shares: `power_ok` violated 0.0 (all true, minimum available power 11.1 W), `dod_ok` 0.131. |
| R-7 | met | Panel mass = density x span x chord (SysML `PanelMass`) and generated power proportional to area (ratio 2.0 to 1e-12). `test_panel_span_raises_inertia_and_slows_the_slew` passes. Trial below: zeroing `panelMass` in `sim_params` fails this test. |
| R-8 | met | `test_battery_capacity_raises_mass_and_inertia` and `test_baseline_inertia_pin` (Jxx, Jyy, Jzz = 0.4006, 0.2058, 0.3171 from `inertia_tensor`, structure mass 11.7714) pass. Trial below: subtracting battery mass from the structure mass fails both. |
| R-9 | met | `test_available_power_caps_the_usable_torque` (including `sqrt(P/(3c))` to 1e-9) and `test_slew_energy_nonnegative_and_grows_with_angle` pass. The cap enters `make_config` through the wheel argument. Observed: it bites in 3.2 % of designs (see WP7 fact (a)). |
| R-10 | met | `test_mass_accounting_identity` passes to 1e-9 on 6 sampled designs, including the equality of the model's total with the mass sent to the simulator (structure + 2 panels + antenna). |
| R-11 | met | `test_measure_returns_attributes_and_flags` (all nine attributes and five flags, finite; positive on the feasible designs) and `test_attributes_are_documented` pass. CSV: 0 non-finite values in the nine attributes; positive on all 772 feasible rows. The pointing budget is implemented in the new layer (`pointing_error_deg`). The module docstring gives a mechanism per attribute. |
| R-12 | met | `uv lock --check` passes. With `OPENSYSML_BINARY=/nope`, `test_unavailable_binary_gives_named_cause` passes ("NAMED: opensysml service binary unavailable"); the fixture uses `pytest.fail`, never skip. `.github/workflows/test.yml` sets `REQUIRE_OPENSYSML=1` and caches `~/.opensysml` keyed on the locked version. CI passed with the first-use download (see R-20). The "if cheap" cache-directory test for download, checksum mismatch and cache hit was not written (not required: G-5). |
| R-13 | met | See the independent hand probe below. |
| R-14 | met (amended) | Own computation on the CSV: median `torque_saturated_frac` small 0.2366, medium 0.0429, large 0.0139, ratio 17.0 (need 3); median settling 247.3 s small, 100.7 s medium, 76.3 s large, ratio 3.24 (need 1.25). `test_torque_binds_for_small_wheels` passes, no xfail marker (the one xfail in the suite is a scikit-learn check in WP3). |
| R-15 | met | 1000 designs; settled 0.888; new columns present (`test_dataset_shape_and_columns`); violation shares `settled` 0.112, `momentum_ok` 0.551, `power_ok` 0.000, `dod_ok` 0.131 (my pandas run equals the probe note). The test only asserts the shares are in [0, 1] and prints them; the numbers are in the note. |
| R-16 | met | `-k reproduc` passes (first 20 against the committed CSV with the WP4 tolerances; 40 designs twice, identical). I also ran the recorded CLI command for 20 designs with 2 workers: settling difference 0.0, mass difference 0.0. The test calls `generate_cubesat` directly rather than the CLI; the CLI path was checked by me. |
| R-17 | met | Probe note read in full. Each tension has a mechanism and a variable: agility against mass through wheel class; power tensions (energy balance against mass through panel span, depth of discharge and reserve against mass through battery capacity, peak slew power against settling and pointing); settling-effort and pointing-effort through Kp and Kd; pointing-mass through tracker grade. Unrecognizable or secondary items are stated (mass-effort and mass-peak-power alignments; margin/balance identity). It records the failed levers (table of adjustments 0 to 3), the final constants, near-frontier sizes, and what the client provided. Details in the observations (G-1). |
| R-18 | met | SysML read. 12U body 0.226 x 0.226 x 0.340 m, total mass 11.9 to 16.1 kg, wheel torques 0.3 / 2 / 10 mN.m, momentum 5 / 20 / 100 mN.m.s, panel area 0.2 to 0.68 m2, battery 20 to 200 Wh at 140 Wh/kg, tracker 30 / 10 / 2 arcsec at 0.15 / 0.35 / 0.9 kg. Units on all attributes; the couplings are visible in `GeneratedPower`, `UsableWheelTorque`, `MassAccounting`, `StructureMass`; header states "documentation of a demonstration" and "illustrative", and mentions `sysmlv2 check|fmt|viz`. It reads as a plausible cubesat. One physical caveat: 55 % of designs exceed the wheel momentum capacity (G-2). |
| R-19 | met | `uv run pytest -q`: 844 passed, 8 skipped, 1 xfailed (70 s; the xfail is WP3's sklearn check; the skips are not WP4b's, none arises from the client). `ruff check .`: All checks passed. `ruff format --check .`: 94 files already formatted. `uv lock --check`: ok. `git diff --stat 5dfbc8c~1..HEAD` lists WP3 and WP6 paths too (other packages' commits in the same range); the WP4b-attributable changes are listed under "Outside the scope". |
| R-20 | met | `git log 5dfbc8c~1..HEAD` grep for `co-authored`, `generated with`, `claude`: 0 matches. All 13 commits in the range: author and committer Michael Zargham. `gh run list`: all WP4b pushes succeeded (`5dfbc8c`, `379dee0`, `6b88cda`, `a2f33f4`, `aa1f1f1`), each with the opensysml download or cache. Two red runs in the range, neither WP4b's: `f635a04` (WP3) and `8f49253` (WP6), both failing `tests/test_narrative.py::test_no_wp3_signatures_quoted` ("limitations.md quotes select_temperature"); fixed by `d0a2c0d`, green. `c89b5d0` has no run of its own (pushed together with `8f49253`, whose red run therefore covered it, red for the WP6/WP3 reason above); its content is green at `d0a2c0d`. |

### R-13 independent hand probe

I rewrote the probe from the scope text (own script, not the test's functions): feasible designs = settled and `power_ok` and `dod_ok` (772, all nine attributes positive); reciprocal for settling, pointing, mass, effort, peak slew power, depth of discharge; direct for margin, balance, reserve; log; standardize; `solve_lp(U, 0.0)`; a 200-point grid on tau for `frac_above_` nearest 0.10; near rows |log V| < 1/tau; Pearson of oriented log-metrics; 100 bootstrap resamples seeded 0.

| Quantity | Mine | Implementer's | Threshold |
|---|---|---|---|
| Contending set at tau = inf | size 6: settling .137, pointing .151, mass .266, effort .163, dod .065, energy balance .219 | size 6, identical values | size >= 3, mass and a power attribute >= 0.05 (a) |
| Working tau, frac_above | 20.49, 0.1036 (grid); the test's bisection gives 20.81, 0.0997 | 20.8, 0.0997 | about 0.10 |
| Near-frontier rows | 93 at my tau; 87 at the test's tau | 87 | |
| Bootstrap support | mass 100 % (median .179), energy balance 100 % (.213) | same | >= 90 %, median >= 0.05 (b) |
| Settling-mass | -0.54 at my tau; -0.575 at the test's tau | -0.57 | <= -0.30 (c) |
| Wheel classes near frontier | medium 45, small 38, large 10 (my tau); 43 / 34 / 10 (test's tau) | 43 / 34 / 10 | >= 2 classes with >= 10 (c) |
| Power tensions | mass-dod -0.61, mass-reserve -0.59, settling-peak slew power -0.72 | -0.63, -0.60, -0.75 | one <= -0.30 (d) |
| Previous tensions | settling-effort -0.87, pointing-effort -0.57, pointing-mass -0.62, settling-pointing +0.50 | -0.88, -0.57, -0.61, +0.50 | <= -0.30, <= -0.30, <= -0.30, not negative (e) |

All of (a) to (e) hold. The small differences come from the tau tolerance only. Retained observation: the large-wheel near-frontier count is exactly 10 at both temperatures (the threshold is 10), so (c) has no margin on that clause (G-3). The hand-probe agreement test with `tension_report` passes.

### Trials (not committed)

- Zeroing `panelMass` in `CubesatModel.sim_params`: 4 failed (`test_mass_accounting_identity`, `test_baseline_inertia_pin`, `test_panel_span_raises_inertia_and_slows_the_slew`, `test_dataset_reproducible_first_20`). Restored with `git checkout`.
- Removing the battery mass from the structure mass passed to the simulator: 4 failed (`test_mass_accounting_identity`, `test_baseline_inertia_pin`, `test_battery_capacity_raises_mass_and_inertia`, `test_dataset_reproducible_first_20`). Restored; `git status` clean.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-8 exist | met | See Deliverables. |
| R-1 to R-20 pass as checked, with evidence; the model is used through `opensysml` (R-3 to R-6); R-13 and R-14 hold on the committed dataset | met | See Requirements. The client use is real: instance values, `eval` of calcs, `verify_constraint`, `run_sweep`. |
| Non-goals untouched | met, with one comment-only touch | See below. |

## Outside the scope

- **Out-of-scope changes (WP4b commits only):**
  - `.github/workflows/test.yml` (+12 lines, `379dee0`): reads the locked `opensysml` version from `uv.lock`, caches `~/.opensysml` with `actions/cache@v4` keyed on OS and version, sets `REQUIRE_OPENSYSML: "1"` for the test step. Scope-permitted (R-19, CI default) and minimal; CI is green with it.
  - `pyproject.toml` (+3/-1) and `uv.lock` (+333): the `case` dependency group in `default-groups`; scope-permitted (D-5). The package's runtime dependencies are unchanged.
  - `examples/adcs/extended_design_space.sysml` (+2 comment lines in `379dee0`): a WP4 deliverable (documentation file, not parsed by code). Comment only, pointing to the new model. No deliverable of WP4b lists it (G-4).
  - `work-packages/` records and `README.md` status: expected.
  - The diff over `5dfbc8c~1..HEAD` also contains WP3 and WP6 files (`docs/api.md`, `method.md`, `preconditioning.md`, `limitations.md`, `src/hyperbolic_trade_space/*`, `tests/test_docs.py`, their reviews). Those belong to other packages' commits and are not attributed to WP4b.
- **Non-goals touched:** none. `adcs_sim.py` byte-identical; no estimator, solver, coordinate, WP3 or notebook change by WP4b; no `sysml-toolkit` dependency; original CSV, WP4 tests and `design_space.py` untouched. The only touch is the two-line comment above.

## Observations (not counted as failures)

- **WP7 fact (a), verified.** Power never limits a slew in this dataset. Power-capped usable torque (usable below the class maximum) occurs in 32 of 1000 designs (3.2 %), all large wheels (10.3 % of large-wheel designs), all with panel span at most 0.34 m; `power_ok` is true for every design (minimum available power 11.1 W). The power attributes reach the controls only through mass and inertia. Power tensions are energy-sizing tensions (panel and battery against mass), not power-limited slews. WP7 should say so.
- **WP7 fact (b), verified.** Near-redundant pairs on the 772 feasible rows: power margin with energy balance, Pearson 0.990 raw, 0.965 on logs (0.98 near the frontier); eclipse reserve with depth of discharge -0.884 raw, -0.969 against the log of depth, -0.922 on logs, 0.95 near the frontier as oriented metrics. They are accounting near-identities and should not be read as independent findings (the contending set holds energy balance and depth of discharge, never the partner of either).
- **Disclosure (i): pre-adjustment scans.** The probe note says the implementer ran simulation-only scans (60 to 90 designs; gain multipliers, slew 45 and 90 degrees, horizons 200 to 1500 s, Kd ranges, small-wheel torque) before the three recorded adjustments and did not evaluate R-13 on any scan. I cannot verify the scans (they were not kept). The scope allows "adjusted at most three times if R-13 or R-14 fail"; the scans did not use the acceptance test but did inform which constants to move, so the three-adjustment limit is soft in practice. The supervisor should judge whether the scans count.
- **Disclosure (i): adjustments 2 and 3 each changed several constants.** Adjustment 2 changed Kp and Kd ranges, horizon and slew angle; adjustment 3 changed Kp and Kd ranges (to values between adjustment 0 and 2), the small-wheel `maxTorque` (0.5 to 0.3 mN.m) and the horizon. Counting each bundle as one adjustment is the implementer's reading of "at most three times total"; the scope does not say whether a bundle is one. The final model differs from the approved defaults list in: Kp 0.03 to 1.0 (default 0.003 to 0.1), Kd 0.3 to 1.5 (default 0.03 to 1.0), small wheel 0.3 mN.m (default 0.5), slew 90 degrees (default 45, escalation to 90 was allowed), horizon 450 s, total mass 11.9 to 16.1 kg (default text "about 13 to 18"). All are recorded in the note and the SysML header. The plausibility rule ("not tuned until a test passes") is a judgment: adjustment 3 moved the small-wheel torque toward the very 0.25 threshold that the supervisor later dropped as arbitrary, and still missed it; the 0.3 mN.m value is within the stated public range. This is a judgment for the supervisor; I found no sign of tuning to R-13 (R-13 passed on the final dataset without being the target).
- **Reading the R-14 history.** The amendment text says no new simulation was run; `git show 379dee0` already contained the dataset with 0.237, and `c89b5d0` changed only the test and the note. Consistent.
- **Stale help text.** `generate_dataset.py --help` says "--slew-deg ... (default 10 / cubesat 45)" while the cubesat default is 90 (the docstring and note are right).
- **Weak assertion.** In `test_hand_probe_agrees_with_tension_report`, the contending-set clause passes if the report's set is a superset of the hand set (`or ... >=`), looser than "must agree". The association matrix check (1e-9) and near-frontier count are strict.
- **Interpretive limits for WP7.** Near-frontier samples are small (87 rows; 10 to 43 per wheel class); associations are noisy at the 0.1 level. Over all 772 feasible rows margin and balance are strongly aligned with other attributes only through mass.

## Open decisions (for the supervisor)

- **G-1.** Pre-adjustment simulation scans and the two multi-constant adjustments (observations under (i)): the supervisor to judge whether the three-adjustment limit and the plausibility rule were respected — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-2.** 55 % of designs have `momentum_ok = False` (small wheels 93 % violate, medium 65 %, large 3 %): the 90 degree slew needs more angular momentum than most wheels store and the simulator does not clip momentum. The flag is informational, not a feasibility flag, and is not in the fit's feasible set; a cubesat reader may find the large violated share less sensible than R-18 intends. The scope (R-11) asks only that the flag exist. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-3.** R-13(c) passes with exactly 10 large-wheel near-frontier designs (threshold 10); small changes of tau or of the sample would flip it; the check is a seed-0 result, not a robust one. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-4.** Comment-only edit to `examples/adcs/extended_design_space.sysml`, a WP4 deliverable that no WP4b deliverable lists. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-5.** Small items taken together: no new test of the default generator behaviour (R-2 rests on the unchanged WP4 tests and my run); the "if cheap" cache-directory test of R-12 not written; stale `--slew-deg` help text; the lenient contending-set clause in the tension-report agreement test. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-6.** The two WP7 facts (power never limits a slew; near-redundant margin/balance and reserve/depth pairs) are verified and should be carried into WP7's scope. — options: accept as is (WP7 will carry them) / fix before acceptance / follow-up work package. **pending**

## Gap dispositions

Resolved through the decision loop (`~/.claude/skills/CLAUDE.md`); records go in `work-packages/WP4b-decisions.md`.

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 | pending | |
| G-2 | pending | |
| G-3 | pending | |
| G-4 | pending | |
| G-5 | pending | |
| G-6 | pending | |

## Recommendation

Provisional, until every gap has a disposition: recommend acceptance with the listed gaps noted, because every requirement R-1 to R-20 is met on evidence I ran myself: the full suite (844 passed), ruff and lock checks are clean; `adcs_sim.py`, the WP4 tests and the original CSV are untouched; the SysML model is genuinely used (instances, calcs, `verify_constraint`, sweeps; ranges and enums read from the model, confirmed by a copy-edit trial; two coupling-break trials fail tests); and my independent probe reproduces the implementer's R-13 and R-14 numbers (contending set of size 6 including mass 0.266, settling-mass -0.57 at the test's temperature, retained tensions). The gaps are judgments (how the tuning history is read, the momentum flag, a thin large-wheel count) and housekeeping, none of which makes a requirement fail.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
