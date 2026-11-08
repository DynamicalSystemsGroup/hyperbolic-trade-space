# WP4b — Review report (second pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP4b-scope-of-work.md` with Amendment 1 (R-14 to its relative clauses), Amendment 2 (momentum enforced as feasibility) and Amendment 3 (physically consistent scenario, stop rule restated) |
| **Scope approval verified** | The project has no PRs, so the recorded act is `work-packages/WP4b-decisions.md`: "Scope approval (approval gate)", supervisor mzargham, verbatim "okay proceed", document at `d27c177` (draft 4 plus the toaster amendment), defaults list approved as one item. Amendment 1: verbatim "Amend R-14 to its intent; keep the dataset". Amendment 2: verbatim "Enforce as feasibility" and "Fix the stale help text, accept the rest". Amendment 3: verbatim "Reopen levers for a physically consistent scenario" (recorded in `53afc54`; scope text `f099ddf`). The amendment texts match the recorded choices. Records typed by the agent, decisions are the supervisor's. |
| **Work reviewed** | `main`. WP4b delivery commits `5dfbc8c`, `379dee0`, `c89b5d0`, `b8fd0cc`, `7704ab7`, and the amendment 3 delivery `354bffd` (dataset, model constants, tests, probe note). Records: `aa1f1f1`, `6b88cda`, `4e2acf6`, `d721d12`, `53afc54`, `f099ddf`, `914fe63`. HEAD at review start `4f5d211` (a WP6 review commit by a parallel reviewer). Start for diffs `5dfbc8c~1`; WP4 state `932bbe4` / `a9fc4f2`. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4b-decisions.md`, after this report |

A fresh reviewer who built none of WP4b and wrote none of its earlier reviews (this replaces the first-pass report, `70081fb`). Every command below was run in this session with `unset VIRTUAL_ENV`. Review only: nothing was repaired; the one trial edit was undone with `git checkout` and `git status` is clean. R-13 is judged as the supervisor asked: unmet, and under the Amendment 3 stop rule.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/cubesat_tradespace.sysml`; amendment 3 changed only the small and medium wheel `maxMomentum` (0.005 -> 0.010, 0.020 -> 0.030 N m s) and the doc comment (`git diff 354bffd~1 354bffd`). |
| D-2 | met | `examples/adcs/cubesat_model.py`: scenario defaults now `SLEW_DEG = 30.0`, `T_END = 600.0`; nothing else changed. |
| D-3 | met | `generate_dataset.py`: help text and docstring now say cubesat default 30 degrees / 600 s (the stale-help fix of the round-1 disposition is verified). |
| D-4 | met | `data/adcs_designs_cubesat.csv`: 1000 rows, 33 columns, `slew_deg`/`t_end_s`/`max_step_s` columns, regenerated at 30 degrees, 600 s. |
| D-5 | met | `uv lock --check`: "Resolved 173 packages". |
| D-6 | met (with 4 strict xfails) | `REQUIRE_OPENSYSML=1 uv run pytest -q -rx tests/test_cubesat_model.py tests/test_adcs_enrichment.py`: 32 passed, 4 xfailed in 27 s. The xfails are `test_a_`, `test_b_`, `test_c_`, `test_e_` of `test_adcs_enrichment.py`, all `strict=True` with the same reason string citing amendment 3. (The brief says five xfails; the full suite has five, but the fifth is WP3's scikit-learn check, `tests/test_sklearn_compat.py`; WP4b owns four.) |
| D-7 | met, with defects | Probe note updated (levers table, committed dataset, WP7 facts). Two defects: stale text and an unsupported mass argument (G-2, G-3). |
| D-8 | met | `WP4b-decisions.md` holds the approval, amendments 1 to 3 and the stop-rule record; acceptance is pending. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `git diff 932bbe4..HEAD -- examples/adcs/adcs_sim.py` empty; `git diff a9fc4f2..HEAD --stat` over `adcs_sim.py`, `tests/test_adcs_case.py`, `design_space.py` and `adcs_designs.csv`: empty. `pytest tests/test_adcs_case.py`: 16 passed. |
| R-2 | met | Original CSV, `design_space.py` and `test_adcs_case.py` untouched in the diff; the WP4 reproducibility tests pass in the full suite. No separate test of the defaults (accepted in round 1 as part of G-5). |
| R-3 | met | `test_cubesat_model.py` model-load, self-check, units and negative-control tests pass (25 tests). |
| R-4 | met | `test_editing_a_range_or_enum_literal_changes_the_sampler` and `test_no_duplicated_constants_in_python` pass. Amendment 3 edited the latter to strip the three scenario lines (`SLEW_DEG`, `T_END`, `MAX_STEP`) from the scan; scenario numbers are not model constants (the scope allows scenario parameters in Python), and the wheel momentum numbers (the model constants that changed) live only in the SysML. |
| R-5 | met | Unchanged code path; `test_run_sweep_over_panel_span_matches_python_accounting` and the accounting test pass. |
| R-6 | met | `test_flags_equal_independent_python_evaluation`, `test_flags_negative_controls` pass. |
| R-7 | met | Trial: set `panelMass=0.0` in `CubesatModel.sim_params`; `pytest tests/test_cubesat_model.py` gave 4 failed (`test_mass_accounting_identity`, `test_baseline_inertia_pin`, `test_panel_span_raises_inertia_and_slows_the_slew`, `test_dataset_reproducible_first_20`), 21 passed. Restored with `git checkout`; tree clean. |
| R-8 | met | `test_battery_capacity_raises_mass_and_inertia`, `test_baseline_inertia_pin` pass (baseline inertia unaffected by the amendment). |
| R-9 | met | `test_available_power_caps_the_usable_torque`, `test_slew_energy_nonnegative_and_grows_with_angle` pass. Power cap below the class torque in 32 of 1000 designs (3.2 %, all large wheels), minimum available power 11.1 W (own computation). |
| R-10 | met | `test_mass_accounting_identity` passes. |
| R-11 | met | `test_measure_returns_attributes_and_flags`, `test_attributes_are_documented` pass; on the feasible set all nine attributes are positive (780 rows). |
| R-12 | met | `uv lock --check` ok; the fixture fails hard with a named cause, `REQUIRE_OPENSYSML=1` in CI; green runs below. |
| R-13 | **not met, under the stop rule** | Details below. Clauses (a), (b), (c) and the pointing-mass part of (e) fail; (d) and the rest of (e) hold. Four tests carry strict xfail with the reason. Thresholds and method unchanged (checked in the test file). |
| R-14 | met (amended) | Own computation on the 780 feasible rows: median `torque_saturated_frac` small 0.0409, medium 0.0152, large 0.0080, ratio 5.1 (need 3); median settling small 128.3 s, medium 67.1 s, large 69.3 s, ratio 1.85 (need 1.25). `test_torque_binds_for_small_wheels` passes, no marker. Note the medium/large settling medians are indistinguishable (finding below). |
| R-15 | met | 1000 designs; settled share 0.978; feasible 780 (78 %); violation shares settled 0.022, momentum_ok 0.081, power_ok 0.000, dod_ok 0.131 (own pandas run equals the note). |
| R-16 | met | `-k reproduc` passes (first 20 against the committed CSV; 40 twice identical); the recorded command in the test now carries `--slew-deg 30 --t-end 600`. |
| R-17 | partly met | The note records every attempt, constants, near-frontier sizes and explanations, and states plainly that the agility-mass tension is absent. Defects: stale sections and an unsupported mass argument (G-2, G-3). |
| R-18 | met | SysML reads as a plausible cubesat; wheel momentum-to-torque ratios 33, 15, 10 s, inside the stated public range. |
| R-19 | met | `uv run pytest -q`: 841 passed, 8 skipped, 5 xfailed (71 s; 4 WP4b strict xfails + 1 WP3 sklearn). `ruff check .`: All checks passed. `ruff format --check .`: 95 files already formatted. `uv lock --check`: ok. `git diff --stat 5dfbc8c~1..HEAD` over non-`work-packages` paths lists the deliverables, `pyproject.toml`, `uv.lock`, `.github/workflows/test.yml` (the cache edit recorded in the first review) and other packages' files (WP3, WP6). Amendment 3 touched only the 7 files listed in `git diff --stat 354bffd~1 354bffd` (note, model, SysML, generator, CSV, two test files). |
| R-20 | met | Grep of all commit messages in `5dfbc8c~1..HEAD` for `co-authored`, `generated with`, `claude`: 0. All commits author and committer Michael Zargham. `gh run list --limit 40`: every WP4b push is green, including `354bffd` (1m39s). Red runs in the window: `8f49253` (WP6) and `f635a04` (WP3), both failing `tests/test_narrative.py::test_no_wp3_signatures_quoted` ("limitations.md quotes select_temperature"), fixed by `d0a2c0d`; neither is WP4b's. The run for `4f5d211` was still in progress. |

### R-13 on the committed dataset (independent hand probe)

Own script (not the test's functions): feasible = settled and `power_ok` and `momentum_ok` and every attribute positive (780 rows); reciprocal orientation for settling, pointing, mass, effort, peak slew power and depth of discharge, direct for margin, balance and reserve; log; standardize; `solve_lp(U, 0.0)`; 300-point grid on tau for `frac_above_` nearest 0.10; near-frontier |log V| < 1/tau; Pearson of oriented log-metrics; 100 bootstrap resamples seeded 0.

| Quantity | Mine | Implementer's | Threshold and verdict |
|---|---|---|---|
| Contending set at tau = inf | settling .310, pointing .044, effort .433, depth of discharge .006, power margin .207 (size 5); mass 0.000 | same, mass 0.000 | (a) needs size >= 3 (holds), a power attribute (holds) and mass >= 0.05: **fails on mass** |
| Working tau, frac_above | 47.5, 0.100 | 46.1, 0.1013 | about 0.10 |
| Near-frontier rows (small / medium / large) | 75 (55 / 16 / 4) | 76 (56 / 16 / 4) | |
| Bootstrap support (100) | mass **0.01** (median 0.000); power margin 0.73, depth of discharge 0.72, energy balance 0.46, reserve 0.18; settling, pointing, effort 1.00 | mass 0.01, margin 0.73, dod 0.72 | (b) needs mass and a power attribute >= 0.90 with median >= 0.05: **fails on both** (best power attribute 0.73; mass 0.01) |
| Settling-mass association | **-0.08** | -0.09 | (c) needs <= -0.30: **fails**; the wheel-class clause (>= 2 classes with >= 10 near rows: small 55, medium 16) holds |
| Power tensions | mass with depth of discharge -0.57; pointing with peak slew power -0.50 | -0.57, -0.50 | (d) holds |
| Previous tensions | settling-effort -0.95, pointing-effort -0.64, **pointing-mass -0.26**, settling-pointing +0.63 | -0.95, -0.63, -0.26, +0.63 | (e): pointing-mass **fails** (-0.26 against -0.30); the other three hold |

All of the implementer's numbers reproduce, within the tau tolerance (46.1 against my 47.5). The `tension_report` agreement test passes.

Claim checks:
- dod filter: `dod_ok` false on 131 rows; of these 0 have `eclipse_reserve_wh > 0`; `dod_ok` true with reserve <= 0: 0. So `dod_ok` false is exactly a non-positive reserve and the positivity filter already excludes those rows; feasible = settled and `power_ok` and `momentum_ok` and positive attributes = 780, and `dod_ok` is true on all of them. Claim confirmed. (Without the positivity filter the settled, power, momentum set is 897.)
- Per class: feasible small 239 of 344, medium 279 of 345, large 262 of 311. Small-wheel designs are feasible in meaningful numbers, as claimed.

## Independent verification of the findings

**(1) Physics, momentum consistency.** I loaded the model, took the inertia of every design through `sim_params` and the existing `inertia_tensor`, and applied the bound theta_max = h_max^2 / (T J) with the committed wheel numbers (T 0.3, 2, 10 mN m; h_max 10, 30, 100 mN m s).
- J_xx over the 1000 designs: 0.226 to 0.986 kg m^2, 10th/50th/90th percentile 0.251/0.361/0.783 (the note says 0.23 to 0.99, which matches, but "median about 0.5"; the actual median is 0.36, a small slip).
- theta_max at J_min / median / J_max: small 84 / 53 / 19 degrees; medium 114 / 71 / 26; large 254 / 159 / 58. Share of designs whose bound is at least 30 degrees: small 0.83, medium 0.93, large 1.00. Observed `momentum_ok` share: small 0.808, medium 0.957, large 1.000. The bound is conservative as the note says (a PD law brakes earlier): of the designs the bound calls feasible, 253 of 285 small and 314 of 320 medium are actually momentum_ok. So the 30 degree scenario is momentum-consistent: no class is wiped out, and small wheels lose 19 % to large-inertia designs, a boundary.
- At the previous 90 degree scenario every small design (theta_max <= 85 degrees even at J_min) was infeasible by the bound, consistent with the earlier 98 %.

**(2) R-13 hand probe:** reproduced above; every number in the brief (contending set, mass exponent 0.000, bootstrap 0.01, settling-mass -0.09 vs mine -0.08, pointing-mass -0.26, near-frontier per class 56/16/4 vs mine 55/16/4) matches.

**(3) Adjustments and discipline.** Three adjustments are recorded with reasoning and numbers (table "Every attempt" in the note): 1: 10 degrees, wheels unchanged; 2: 20 degrees and momentum capacities 5 -> 10 and 20 -> 30 mN m s (momentum-to-torque ratio 33, 15, 10 s, within the stated public range of 5 to 20 s); 3: 30 degrees, capacities as in 2. Each row carries feasible counts per class, R-14 numbers, contending set, mass bootstrap, settling-mass and near-frontier sizes. The simulation-only scan (first 200 designs at 30 and 40 degrees, between adjustments 2 and 3) is declared with its purpose and results, and the note states R-13 was not evaluated on it. Judgment on discipline:
- Adjustment 2 reached mass exponent 0.046 (miss of (a) by 0.004; bootstrap 0.69) and still failed (c) and (e). The next move (30 degrees) took mass to 0.000, so it did not chase the near-pass; it is justified in physics terms (the largest angle at which about 80 % of small wheels stay momentum-feasible, read from the scan) and the scan's R-14-type outputs (saturation and settling per class) were what it read. That is a defensible physical reading, but it is also the direction (more torque binding) that the failing clauses need, and the scan read quantities close to R-14's. I find no sign of tuning to pass R-13; I also cannot verify from git that the Step A reasoning was written "before any simulation", since the note arrives in one commit (`354bffd`). This is a G-4 item for the supervisor, not a defect.
- Adjustment 2 moved two levers at once (angle and capacities), as the first-round G-1 observation already noted for adjustments 2 and 3 of the original series; the supervisor dispositioned that kind of bundling "accept as is" in round 1 and Amendment 3 itself allowed the capacity lever.
- The committed dataset is the third attempt; the scope does not say which attempt to commit when the stop rule triggers. Attempt 2 (20 degrees) was closer on (a) and (b) (bootstrap 0.69) but its small-wheel saturation ratio and settling are similar and (c)/(e) fail in all three. Choice of the 30 degree dataset is the implementer's and is stated.

**(4) The finding itself.** "1 % settling time is set by the slow pole Kp / (4 Kd), so medium and large wheels settle in the same time" is supported by the data:
- For large wheels, corr(log settling, log(Kd/Kp)) = 0.993 and the median ratio of settling to 4.6 x 4 Kd/Kp is 0.98; medium 0.895 and 1.00; small 0.368 and 1.14 (small wheels depart because torque binds).
- Median settling by quintile of Kd/Kp (large / medium / small, seconds): (0.3,1.4] 15.5 / 34.5 / 186; (1.4,2.6] 34.6 / 39.6 / 87; (2.6,5.2] 67.6 / 67.8 / 89; (5.2,10.7] 125 / 140 / 138; (10.7,32] 277 / 281 / 338. Medium and large coincide except in the highest-gain-ratio quintile, where large settles twice as fast.
- Regression of log settling on log(Kd/Kp) and class dummies: R^2 0.53 with the ratio alone, 0.66 with classes; coefficient on small +0.79, on medium +0.20 (large is the base).
- One part of the stated argument is **not supported**: "wheel class moves total mass by at most 1.4 kg of about 14 kg while panel span, battery capacity and tracker grade move it by several kg". From the CSV: panel mass 0.26 to 0.85 kg, battery mass 0.14 to 1.43 kg, tracker 0.15 to 0.90 kg, wheels 0.36 to 1.80 kg (3 wheels). Wheel class is the largest single mass lever (std 0.60 kg of a total std 0.84 kg; correlation of wheel class with total mass on the feasible set 0.75). Mass is absent from the contending set not because wheel class barely moves it, but because heavier wheels do not buy faster settling (medium and large settle alike), so mass and settling do not trade along wheel class. That is a correction to the explanation, not to the numbers (G-2).

Observations on levers the amendment did not allow (for the supervisor, not defects):
- Settling metric: the 1 % last-exceed criterion in the unchanged `adcs_sim.py` is dominated by the slow pole; a 5 % or 2 % criterion, a time to first entry, or peak slew rate would respond more to torque. Changing it means changing the metric definition (and the simulator is a non-goal if done there; it could be implemented in the new layer from the stored history).
- Gain box: wheel class only separates settling at high Kp/Kd (Kd/Kp below about 1.4: large 15 s, medium 35 s, small 186 s). Narrowing Kd to a lower range or sampling the gain ratio so that more designs sit in that region would let torque bind across classes; it is a design-space change, not a scenario change.
- Wheel mass spread: large (0.60 kg) against small (0.12 kg) is a deliberate factor of five; a larger spread, or a scaling of wheel mass with momentum capacity (which grows 10x), would raise the mass lever.
- Slew angle as a sampled scenario variable rather than a constant; or per-class slew limits set from h_max^2/(T J), so each class operates at its own boundary.
- The 90 degree scenario's "rich" result rested on momentum-violating designs (Amendment 2), so the earlier tension was partly an artefact; the present result is more honest and the supervisor may prefer it as the notebook's story (feasibility boundary instead of frontier tension).

**(5) The two WP7 facts.** (a) Power never limits a slew: verified (3.2 % of designs have a power-capped torque, all large wheels; `power_ok` true everywhere; power margin on the feasible set 6.99 to 67.99 W, median 27.6 W, matching the note's 7.0 to 68 and 27.6). (b) Redundant pairs updated: power margin with energy balance 0.966 (own computation 0.966), reserve with depth of discharge 0.921 (own 0.921) over the feasible set, and 1.00 and 0.90 over near-frontier rows; accounting near-identities. Mass associations near the frontier: depth of discharge -0.57, reserve -0.45 (note -0.46), energy balance -0.38 and margin -0.37 (note -0.35), within the tau tolerance. Class counts on the feasible set (239/279/262) and the note's near-frontier counts agree with mine.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-8 exist at the stated paths | met | See Deliverables (D-7 with defects, G-2, G-3). |
| R-1 to R-20 pass as checked | **not met** | R-13 fails (a), (b), (c) and the pointing-mass clause of (e); the stop rule of Amendment 3 has triggered. R-17 is partly met. All others met. |
| The richness conditions R-13 and R-14 hold on the committed dataset | **not met** | R-14 holds; R-13 does not (see the table). |
| Non-goals untouched | met | See below. |

Because R-13 is unmet under the stop rule, good enough is not met; only a supervisor scope decision changes that.

## Outside the scope

- **Out-of-scope changes:** none beyond those accepted in round 1 (`.github/workflows/test.yml`, `pyproject.toml`, `uv.lock`, the comment-only edit to `extended_design_space.sysml`). Amendment 3 touched the seven files listed under R-19, all deliverable paths.
- **Non-goals touched:** none. `adcs_sim.py` byte-identical; no estimator, solver, coordinates, WP2/WP3 or notebook change by WP4b; no `sysml-toolkit` dependency; the original CSV and WP4 tests untouched.

## Observations (not counted as failures)

- Stale text in the probe note: "Status against R-14 (amended)" still says "R-13 (all of a to e) holds on the final dataset" with the 0.237 numbers, and "Final constants and scenario" still lists the 90 degree scenario and 5 mN m s small momentum (its heading says superseded). A reader skimming will get contradictory statements (G-3).
- The note's Step A table uses the pre-adjustment wheel momenta (5 and 20 mN m s) and a median J of 0.5; actual median 0.36.
- The R-15 sentence in the amendment 2 section ("feasible > 50 %") is historical.
- The 4 xfails are in four separate tests with one shared reason; a reader seeing "5 xfailed" in the suite should know one belongs to WP3.
- Strict xfail means that if a later change made (a) pass, the suite would fail (XPASS), a useful tripwire.
- The finding (feasibility boundary instead of frontier tension) is a legitimate and instructive outcome; it also matches what the scope anticipated for small wheels. The pointing-mass clause of (e) at -0.26 is a near miss.
- Previously dispositioned items (round 1, `WP4b-decisions.md`): G-1 (scans and multi-constant adjustments) accept as is; G-2 (momentum) decided "Enforce as feasibility" (amendment 2); G-3 (threshold margin) accept as is; G-4 (comment edit) accept as is; G-5 (small items): fix stale help text (done, verified), rest accept as is. G-6 (WP7 facts) has no recorded disposition; it is carried below as G-6.

## Open decisions (for the supervisor)

- **G-1. R-13 is unmet under the Amendment 3 stop rule** (a, b, c, and the pointing-mass clause of e; R-14 holds). Whether to accept this as a recorded finding changes the definition of good enough, so "accept as is" needs a scope amendment (for example, R-13 recorded as a finding with the notebook stating that wheel class appears as a feasibility boundary); "fix before acceptance" means reopening levers (see the observations, for example the settling metric or gain box) as another amendment; "follow-up work package" means accepting the rest and moving the richness question to a later package. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-2.** The probe note's mass argument ("wheel class moves mass by at most 1.4 kg; panel, battery, tracker several kg") is contradicted by the data (wheel class is the largest mass lever; the real reason is that heavier wheels do not settle faster). The numbers in the note are right; the explanation of R-17 is wrong in this clause. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-3.** Stale and contradictory text in the probe note (the R-14 status section claims R-13 a to e hold; the final-constants section lists the 90 degree scenario). — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-4.** Adjustment discipline under Amendment 3: one declared scan that read R-14-type quantities, adjustment 2 changing two levers, the choice of attempt 3 over attempt 2, and the "written before any simulation" ordering not verifiable from git. I found no sign of tuning to R-13. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-5.** Small items: the suite shows 5 xfails (4 WP4b, 1 WP3); no test of the defaults (carried from round 1, previously accepted); median J in the note. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-6.** The two WP7 facts and the updated redundant-pair correlations are verified and should be carried into WP7's scope, together with the finding that wheel class acts as a feasibility boundary. — options: accept as is (WP7 will carry them) / fix before acceptance / follow-up work package. **pending**

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

**Do not recommend acceptance yet**, because R-13, a requirement and a good-enough item, is unmet, and the stop rule of Amendment 3 hands that to the supervisor: I cannot recommend acceptance of a package whose approved richness condition fails. Everything else is met on evidence I ran myself: the full suite (841 passed, 4 WP4b strict xfails), both WP4b test files under `REQUIRE_OPENSYSML=1`, ruff, lock, attribution, authors and CI are clean; `adcs_sim.py` and the WP4 tests are untouched; a coupling-break trial fails four tests; R-14 holds; the 30 degree scenario is verifiably momentum-consistent with meaningful small-wheel feasibility; and my independent probe reproduces every number the implementer reports. If the supervisor decides, by a scope amendment, that R-13 is to be recorded as a finding (wheel class acts as a feasibility boundary, not a frontier tension) and fixes the probe-note defects G-2 and G-3, the recommendation would become *recommend acceptance with the listed gaps noted*; that is the supervisor's scope decision, not mine. The alternative is a further amendment reopening the levers listed under (4).

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
