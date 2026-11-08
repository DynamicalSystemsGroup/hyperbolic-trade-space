# WP4b — Review report (sixth pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP4b-scope-of-work.md` with Amendments 1 to 6 (R-14 relative clauses; momentum enforced; physically consistent 30 degree scenario; slew-time attribute and ten attributes; aggressive-gain box and momentum utilisation levers; Amendment 6: the aggressive-gain dataset is the primary case dataset on which R-13, R-14, R-15 are evaluated, the 30 degree baseline is the regime comparison whose null result is a recorded finding) |
| **Scope approval verified** | The project has no PRs; the recorded act is `work-packages/WP4b-decisions.md`: "Scope approval (approval gate)", supervisor mzargham, verbatim "okay proceed", document at `d27c177`. Amendments 1 to 5, the round-4 dispositions ("Both, as two regimes"; "Fix G-6 note, G-5 to follow-up, accept the rest") and the round-5 disposition ("Fix all three", review `2a4051e`) are recorded verbatim in the same file; Amendment 6 applies "Both, as two regimes". |
| **Work reviewed** | `main` at `f1e38ca`. Since the fifth pass (`2a4051e`): `9208aa9` and `de2f758` (status table, WP7 scope), `7df6a40` (round-5 disposition), `f1e38ca` (the three fixes). Earlier delivery as before (`5dfbc8c` to `93d162c`). Start for diffs `5dfbc8c~1`; WP4 state `932bbe4` (simulator) and `9680193` (WP4 tests, CSV, design space). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4b-decisions.md`, after this report |

A fresh reviewer who built none of WP4b and wrote none of its earlier reviews; replaces the fifth-pass report. Every command was run in this session with `unset VIRTUAL_ENV`. Review only: six trial edits were made and undone with `git checkout`; `git status` is clean. The review is a complete one from step 1 against the amended scope; R-13, R-14 and R-15 are evaluated on the PRIMARY dataset `adcs_designs_cubesat_gains.csv`, and the baseline is checked through its regime-comparison assertions.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/cubesat_tradespace.sysml` (baseline `designSpace`, `AggressiveGainSpace`/`aggressiveGains`: Kp 0.2 to 2.0, Kd 0.3 to 1.5 at lines 157 to 160); `git diff 7a175a4..HEAD -- examples src` empty. |
| D-2 | met | `examples/adcs/cubesat_model.py`: client load, sampling from model ranges, `GAIN_BOXES`, `add_momentum_utilisation`; unchanged since `7a175a4`. |
| D-3 | met | `generate_dataset.py` additive flags (`--model`, `--gain-box`); defaults unchanged. |
| D-4 | met | Primary CSV last changed in `7a175a4` (`git diff 7a175a4 HEAD --stat` empty); baseline CSV last changed in `a27502e` (`git diff 6c8c3e9 HEAD --stat` empty). |
| D-5 | met | `uv lock --check`: "Resolved 173 packages". |
| D-6 | met | `REQUIRE_OPENSYSML=1 uv run pytest -q tests/test_cubesat_model.py tests/test_adcs_enrichment.py`: **73 passed**, no skip, no xfail, 50 s. |
| D-7 | met, with wording-level defects | See "Probe note checks" (G-D, G-E). |
| D-8 | met | `WP4b-decisions.md`: approval, amendments 1 to 5, round 4 and round 5 dispositions verbatim, follow-up candidates; acceptance pending. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `git diff 932bbe4..HEAD --stat -- examples/adcs/adcs_sim.py` empty (byte-identical). `git diff 9680193..HEAD --stat -- tests/test_adcs_case.py examples/adcs/data/adcs_designs.csv examples/adcs/design_space.py` empty. WP4 tests pass in the full suite. |
| R-2 | met | Original CSV, WP4 tests, design space untouched; generator defaults unchanged. |
| R-3, R-5, R-6, R-8 to R-10 | met | Pass inside the 73 model and enrichment tests and the full suite; code unchanged since `7a175a4`. |
| R-4 | met | Test passes; code unchanged since the fourth-pass trial. New trial 6 below (gain-box coupling) also fails as it should. |
| R-7 | met | Panel monotonicity tests pass. |
| R-11 | met | Attributes test passes; utilisation derived on read. |
| R-12 | met | `uv lock --check` ok; hard-failing fixture; `REQUIRE_OPENSYSML=1` in CI. |
| R-13, PRIMARY (gains, 10 attributes) | **met** (a to e) | Own hand probe below; tests `test_a_` to `test_e_` pass on `gains` and `gains_headroom`; `test_d_` on all four. |
| R-13, baseline (comparison) | not met, as the recorded finding (a, b, c fail; d, e hold) | Not a failure under Amendment 6; asserted in two-sided bands by `test_regime_comparison_stock_gains` (passes). |
| R-14 (primary) | met | Saturated ratio small/large 13.08 (needs 3); settling ratio 4.85 (needs 1.25). Baseline 5.12 / 1.85. |
| R-15 (primary) | met | 1000 designs; settled 0.976; feasible 706 = 191 / 248 / 267; momentum violations small 37.2 %, medium 17.4 %, large 0. Baseline: settled 0.978, feasible 780 = 239 / 279 / 262. |
| R-16 | met | Reproducibility tests pass locally; aggressive-box tolerances (rtol 1e-3, saturated fraction 10 %) are the recorded stopgap (follow-up). |
| R-17 | met | Note records reasoning before data, results per lever, mechanisms, the miss list, conditions, two-regimes table. |
| R-18 | met | SysML unchanged in substance. |
| R-19 | met | `uv run pytest`: **882 passed, 8 skipped, 1 xfailed** (92 s; the xfail is WP3 scikit-learn, not WP4b). `ruff check .`: All checks passed. `ruff format --check .`: 97 files already formatted. `uv lock --check`: ok. Diff outside scope: none (below). |
| R-20 | met, with three red runs recorded | Message grep (`co-authored`, `generated with`, `claude`, case-insensitive) over `5dfbc8c~1..HEAD` (66 commits): 0; over all commits for co-authored / generated with: 0. All 170 commits author and committer Michael Zargham. CI below. |

### CI (`gh run list --limit 10`, plus failures in the last 40)

The latest ten runs (from `f1e38ca` back to `af8b08d`) are all success; the latest, `f1e38ca`, in 2m00s. Three red runs earlier, causes confirmed with `gh run view --log-failed`, all the aggressive-box first-20 reproducibility test: `7a175a4` (continuous column, 1 of 20, max abs difference 2.3e-5, rtol 1e-4), `4897434` (note-only commit, same code; `torque_saturated_frac` 3 of 20, abs 0.0027), `be9ea7d` (3 of 20, abs 0.0061). Fixed by `620cfc8`; no red run since.

## Independent hand probe on the PRIMARY dataset

Own script (`/private/tmp/claude-501/s/probe.py`, not committed): feasible = settled, `power_ok`, `momentum_ok`, every attribute positive; reciprocal orientation for the seven smaller-is-better, direct for the three larger-is-better; log; standardize; `solve_lp(U, 0)`; fixed tau scan 25 to 50; near-frontier |log V| < 1/tau; 100 bootstrap resamples seeded 0.

| Quantity | Note | My probe |
|---|---|---|
| feasible n (s/m/l) | 706 = 191/248/267 | 706 = 191/248/267 |
| contending set at tau = inf | slew .201, mass .223, energy balance .169, effort .143, pointing .135, DoD .129 | identical, all six |
| mass bootstrap support | 1.00 | 1.00 (median .200) |
| settling-mass / slew-mass at tau 35.2 | -0.503 / -0.453 | -0.503 / -0.453 (exact; tau 25 to 40: -0.50 to -0.65 / -0.42 to -0.62; tau 50: -0.30 / -0.41, the edge) |
| pointing-effort / settling-pointing at 35.2 | -0.349 / +0.143 | -0.349 / +0.143 (tau 25 to 50: -0.33 to -0.43; +0.21 to -0.07, so settling-pointing at tau 50 is slightly negative: thin margin, disclosed) |
| near-frontier rows (s/m/l) at 35.2 | 21 / 36 / 7 | 21 / 36 / 7 |
| R-14 | 13.1 / 4.85 | 13.08 / 4.85 |
| (a) to (e) | pass | pass |

Baseline, same script: contending set of six without mass (effort .434, slew .253, power margin .179, settling .081, pointing .040, reserve .013), mass bootstrap support 0.00, settling-mass -0.11 to -0.22 across tau 25 to 50 (note -0.129), slew-mass -0.10 to -0.20 (note -0.109), pointing-effort -0.62 to -0.72, settling-pointing +0.59 to +0.72, near-frontier small-dominated (78 / 23 / 1 at the note's tau). Kd/Kp median 1.058 against 3.95. Median saturated fraction (feasible): baseline 0.041 / 0.015 / 0.008, primary 0.165 / 0.044 / 0.0126.

## G-A verified (miss list)

Recomputed from the CSVs on the feasible set: large-wheel median saturated fraction 0.0079 (baseline) to 0.0126 (aggressive), +58 %, while small goes 0.041 to 0.165 (note: "not far more", correct); small/large ratio 5.12 to 13.08 (the "may shrink" prediction missed, recorded); slew-time medians 33.0 / 13.8 s aggressive, ratio 2.39 (predicted about 3), baseline 82.7 / 51.8 s, ratio 1.6 (recorded). Predictions in commit `75823dc` compared one by one with the note's miss list: momentum violations, slew times, feasible share, settling class ratio, effort/pointing dominating, lever iii, saturation (both clauses), slew ratio: all recorded. Held items (heavier wheels faster; medians rise for every class; association range; lever ii alone fails; R-14 clause 1) check out. No unrecorded miss found. **G-A: fixed.** (Cosmetic: the "Expectation against result" paragraph in Amendment 5 results, which says only the three momentum/slew/feasible items were "wrong in size", is complemented by, not contradicted by, the complete list.)

## G-B verified (two-sided bands)

`test_regime_comparison_stock_gains` now asserts, for the baseline: feasible counts exact (780 = 239/279/262), settling-mass within 0.10 of -0.129, slew-mass of -0.109, pointing-mass of -0.357 (and at most -0.30), mass weight within 0.02 of 0, bootstrap support at most 0.05, near-frontier small within 15 of 78, medium within 15 of 23, large at most 5; for the headroom dataset the recorded 0.060 etc. with bands. Drift trials, each in the working copy and restored by `git checkout`: (1) recorded settling-mass center -0.129 changed to -0.329: baseline test fails (`assert 0.2001 <= 0.1`); (2) near-frontier small center 78 changed to 20: baseline test fails (`assert 58 <= 15`); (3) headroom mass-weight center 0.060 changed to 0.130: headroom test fails (`assert 0.0702 <= 0.03`). **G-B: fixed.** Observation: the association bands (plus or minus 0.10) are about as wide as the tau-grid variation of the baseline associations (-0.11 to -0.22 across tau 25 to 50), so they catch a regime change rather than a small drift; that is the stated purpose.

## Probe note checks

- **G-C labels:** "Status against R-14" now says BASELINE and points to the primary; the old numbers are labelled phase 2 (90 degree); "Facts for WP7" opens with "BASELINE dataset" and adds a PRIMARY paragraph; the lever (i) prediction carries "both predictions missed". Mostly fixed. Residuals below (G-D, G-E).
- **Scope status line:** reads "DRAFT (draft 4, amended five times: see Amendments 1 to 6). Approved by the recorded act below." Amendments 1 to 6 are six; "five" is a miscount, and "DRAFT" remains although approved. Wording-level (G-E).
- **Primary-dataset facts recomputed:** power-cap share 3.2 % of all designs (32 designs, all large wheels), 3.5 % of the feasible set (25 of 706): **confirmed**; `power_ok` True for all: confirmed; power margin on the feasible set 6.9 to 65.9 W, median 24.7: confirmed. Redundant pairs: power margin with energy balance 0.960, eclipse reserve with depth of discharge 0.923 (the oriented correlation; the raw log correlation is -0.923, a sign flip by orientation), slew with settling 0.698 and 0.867 among near-frontier rows at tau 35.2 (baseline 0.947 and 0.985): **confirmed**. Near-frontier 21 / 36 / 7 at tau 35.2: confirmed; mass associations with pointing -0.66, settling -0.50, slew -0.45: confirmed.
- **New defect found (G-D, wording-level, factual):** the new PRIMARY facts paragraph (line 451) states "aggressive gains Kp 0.3 to 3", but the committed box is Kp 0.2 to 2.0, Kd 0.3 to 1.5 (SysML lines 157 to 160; CSV Kp 0.2005 to 1.9987, Kd 0.3001 to 1.4995; the note's own reasoning, line 604). "Kp 0.3 to 3.0" is the paper-only box rejected in the reasoning (line 609). No verdict is affected; the paragraph is a "Facts for WP7" item and WP7 reads it.
- **Stale residuals (G-E, wording-level):** line 166 "not either committed dataset" ok, but line 179 still says "3.2 % of final-dataset designs" and line 207 says the phase 2 numbers "do not describe the committed dataset" followed by "Final constants and scenario ... Kp 0.03 to 1.0 / Kd 0.3 to 1.5", which is the baseline box only (the primary box differs); the scope status line miscount above. They are chronologically labelled and do not change a verdict.
- **Conditional on the stiff-loop regime:** yes ("Conditions of the finding"). **Thin margins disclosed:** yes (pointing-effort -0.35 against -0.30; settling-pointing +0.15 against 0.0; 7 large-wheel rows; my tau scan confirms the edge at tau 50).
- **Follow-up item present:** yes. `WP4b-decisions.md` "Follow-up candidates": generator nondeterminism (CI 3.8 % then 6.2 % on saturated fraction; 10 % tolerance a stopgap; not part of WP4b), plus unused levers.

## Trials (all undone with `git checkout`; `git status` clean)

1. Utilisation derivation changed to `peak / (2 * cap)`: 3 failed (`test_momentum_utilisation_matches_the_momentum_flag[headroom]`, `[gains_headroom]`, `test_wheel_capacities_and_momentum_utilisation`), 70 passed.
2. Gain-box coupling (`"aggressive"` mapped to `designSpace`): `test_aggressive_gain_box_is_read_from_the_model` and `test_dataset_reproducible_first_20[aggressive-csv1]` fail, 29 passed.
3. to 5. G-B drift trials above (3 failures).

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-8 exist | met | Deliverables. |
| R-1 to R-20 pass as checked | met | R-13 and R-14 met on the primary dataset; baseline recorded as the regime finding. |
| R-13 and R-14 hold on the committed (primary) dataset | met | Own probe. |
| Non-goals untouched | met | Below. |

## Outside the scope

- **Out-of-scope changes:** none by WP4b. `git diff 2a4051e..HEAD --stat` lists the probe note, `tests/test_adcs_enrichment.py`, `work-packages/{README,WP4b-decisions,WP4b-scope-of-work,WP7-scope-of-work}.md` (README and WP7 are status/scope workflow edits, not WP4b deliverables). Whole range, as in earlier passes: `src/`, docs and WP3/WP6 tests belong to other packages; `.github/workflows/test.yml` is a 12-line CI change in `379dee0` (R-19 allowance); the repository-rename edit is `a469aa2`.
- **Non-goals touched:** none. `adcs_sim.py` byte-identical; no estimator, solver, coordinates, WP2/WP3 or notebook change by WP4b; no `sysml-toolkit` dependency; WP4 CSV, tests and design space untouched; both cubesat CSVs untouched since their generating commits (`7a175a4`, `a27502e`).

## Observations (not counted as failures)

- G-A, G-B fixed and verified; G-C mostly fixed; two wording-level residuals (G-D, G-E). No substantive finding; no verdict changes.
- The primary result rests on a deliberately stiff regime; disclosed and carried into the finding text.
- The full suite shows one non-WP4b xfail (WP3 scikit-learn).
- Previously dispositioned and recorded in `WP4b-decisions.md`: G-1 "Both, as two regimes" (applied by Amendment 6); G-3, G-4, G-7, G-8 accept as is; G-6 miss list fixed; G-5 reproducibility tolerance to follow-up; round 5 "Fix all three" (G-A, G-B, G-C) applied in `f1e38ca` and verified above. Earlier rounds: stale help text fixed, "Enforce as feasibility", "Reopen levers for a physically consistent scenario", "One physics-justified lever: slew-time attribute", "try both new levers then report back".

## Open decisions (for the supervisor)

Two new wording-level gaps; neither affects a good-enough item or a non-goal, so they go to the supervisor as one item.

- **G-D.** The PRIMARY facts paragraph in the probe note gives the aggressive box as "Kp 0.3 to 3"; the committed box is Kp 0.2 to 2.0, Kd 0.3 to 1.5. Wording-level (factual typo). — options: accept as is / fix before acceptance / follow-up work package
- **G-E.** Residual stale labels: "final-dataset" (line 179), the "Final constants and scenario" sentence (line 207) naming only the baseline gain box, and the scope status line "DRAFT (draft 4, amended five times: see Amendments 1 to 6)" (six amendments; still "DRAFT"). Wording-level. — options: accept as is / fix before acceptance / follow-up work package

Proposed: "accept G-D and G-E as is, or pick any to act on". G-D is the one most worth correcting since WP7 consumes the facts paragraph.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-D | pending | |
| G-E | pending | |
| G-A, G-B, G-C (fifth pass) | fix before acceptance, recorded "Fix all three"; fixed in `f1e38ca`, verified (G-C partly, see G-E) | `WP4b-decisions.md`, round 5 |
| Previously dispositioned (see Observations) | as recorded | accept as is / fixed / follow-up as quoted in `WP4b-decisions.md` |
| Follow-up: generator nondeterminism, 10 % tolerance stopgap | follow-up work package (recorded) | `WP4b-decisions.md`, "Follow-up candidates"; not part of WP4b |

## Recommendation

**Recommend acceptance with the listed gaps noted.** Every deliverable and requirement is met against the amended scope: R-13 (a to e), R-14 and R-15 hold on the primary aggressive-gain dataset and my independent probe reproduces the note's numbers exactly (contending set, mass 0.223 with bootstrap support 1.00, settling-mass -0.503, feasible 706 = 191/248/267); the baseline's null result is asserted in verified two-sided bands (three drift trials fail as they should) and recorded as a finding; the prediction-miss list is now complete against the predictions of `75823dc`; the full suite (882 passed), ruff, format and lock are clean; the last ten CI runs are green and the three earlier red runs have confirmed causes; `adcs_sim.py`, the WP4 tests and both cubesat CSVs are untouched; authorship and attribution are clean. The two new gaps are wording-level (a mistyped gain box in a facts paragraph, residual stale labels and a status-line miscount) and pending the supervisor's disposition.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
