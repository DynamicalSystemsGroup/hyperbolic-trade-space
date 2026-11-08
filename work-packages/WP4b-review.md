# WP4b — Review report (fourth pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP4b-scope-of-work.md` with Amendments 1 to 5 (R-14 relative clauses; momentum enforced; physically consistent 30 degree scenario; slew-time attribute and ten attributes; aggressive-gain box and momentum utilisation levers) |
| **Scope approval verified** | The project has no PRs, so the recorded act is `work-packages/WP4b-decisions.md`: "Scope approval (approval gate)", supervisor mzargham, verbatim "okay proceed", document at `d27c177`. Amendment 1 "Amend R-14 to its intent; keep the dataset"; amendment 2 "Enforce as feasibility" and "Fix the stale help text, accept the rest"; amendment 3 "Reopen levers for a physically consistent scenario"; amendment 4 "One physics-justified lever: slew-time attribute"; amendment 5 "try both new levers then report back" (record `5b1d087`, scope text `78c39c8`, both before the reasoning commit `75823dc`). Records typed by the agent, decisions are the supervisor's. |
| **Work reviewed** | `main` at `620cfc8`. Amendment 5 delivery: scope `78c39c8`, reasoning note `75823dc` (01:09:22), generating commit `7a175a4` (01:16:58), results note `4897434`, tolerance fixes `be9ea7d`, `620cfc8`. Earlier delivery as in the third pass (`5dfbc8c` to `6c8c3e9`). Start for diffs `5dfbc8c~1`; WP4 state `932bbe4` (simulator) and `9680193` (WP4 tests, CSV, design space). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4b-decisions.md`, after this report |

A fresh reviewer who built none of WP4b and wrote none of its earlier reviews; replaces the third-pass report. Every command was run in this session with `unset VIRTUAL_ENV`. Review only: two trial edits were made and undone with `git checkout`; `git status` is clean. The review covers BOTH datasets: the 30 degree baseline `adcs_designs_cubesat.csv` and the aggressive-gain dataset `adcs_designs_cubesat_gains.csv`, plus the two utilisation variants. Which dataset stands is the supervisor's decision; this report does not choose.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `cubesat_tradespace.sysml`: amendment 5 adds `part def AggressiveGainSpace` (KpMin 0.2, KpMax 2.0, KdMin 0.3, KdMax 1.5) and `part aggressiveGains`; the baseline `designSpace` is unchanged (`git diff 6c8c3e9 HEAD`). |
| D-2 | met | `cubesat_model.py`: `GAIN_BOXES` maps `baseline` to `designSpace` and `aggressive` to `aggressiveGains`, the sampler reads Kp, Kd from the selected part; `CubesatModel.wheel_capacities()` reads `maxMomentum` per wheel class through the client; `add_momentum_utilisation(df, capacities)` returns a copy. |
| D-3 | met | `generate_dataset.py`: additive `--gain-box {baseline,aggressive}`, default unchanged; `--gain-box` with `--model adcs` is an error. |
| D-4 | met | Baseline CSV: last changed `a27502e` (amendment 4), not touched since (`git diff 6c8c3e9 HEAD --stat -- adcs_designs_cubesat.csv` empty). New `adcs_designs_cubesat_gains.csv`: 1000 rows, same 35 columns, 30 degrees, 600 s, seed 0, aggressive box. Utilisation is derived on read; no CSV rewritten. |
| D-5 | met | `uv lock --check`: "Resolved 173 packages". |
| D-6 | met (5 strict xfails, all WP4b, all per dataset) | `REQUIRE_OPENSYSML=1 uv run pytest -q -rx tests/test_cubesat_model.py tests/test_adcs_enrichment.py`: 74 passed, 5 xfailed in 49 s. xfails: `test_a_`, `test_b_`, `test_c_` on `[baseline]`; `test_c_` and `test_e_` on `[headroom]`. No xfail on `[gains]` or `[gains_headroom]`. |
| D-7 | met | Probe note: "Amendment 5: three levers" (reasoning) and "Amendment 5: results". |
| D-8 | met | `WP4b-decisions.md` holds approval, amendments 1 to 5 verbatim; acceptance pending. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `git diff 932bbe4..HEAD -- examples/adcs/adcs_sim.py` empty (byte-identical); `git diff 9680193..HEAD --stat -- adcs_sim.py tests/test_adcs_case.py adcs_designs.csv design_space.py` empty. WP4 tests pass in the full suite. |
| R-2 | met | Original CSV, `design_space.py`, WP4 tests untouched; default generator behaviour unchanged. |
| R-3 | met | Model tests pass under `REQUIRE_OPENSYSML=1`. |
| R-4 | met | Test `test_no_duplicated_constants_in_python` passes. My trial on a COPY of the model (`/private/tmp/claude-501/scratch/copy.sysml`, aggressive box edited to KpMin 0.5, KdMax 0.9): copy aggressive ranges (0.5, 2.0) and (0.3, 0.9), copy baseline ranges unchanged (0.03, 1.0), (0.3, 1.5); the sampler's Kp minimum moves 0.202 to 0.503 and Kd maximum 1.498 to 0.899 with wheel and span columns identical. No gain-box number appears in Python (grep of 0.2, 2.0, 0.3, 1.5 in `cubesat_model.py`: no hits). |
| R-5, R-6, R-8, R-9, R-10 | met | Pass inside the 74 model and enrichment tests and the full suite (unchanged code paths). |
| R-7 | met | Panel monotonicity tests pass. |
| R-11 | met | Attributes test passes; eleventh attribute is derived on read, not a `measure` column, and is documented. |
| R-12 | met | `uv lock --check` ok; hard-failing fixture; `REQUIRE_OPENSYSML=1` in CI. |
| R-13, baseline (10 attributes) | **not met** (a, b, c fail; d, e hold) | Own probe below. Pre-agreed finding under Amendment 4. |
| R-13, baseline + utilisation (11, lever ii) | **not met** (c, e fail; a, b, d hold) | Own probe below. |
| R-13, gains (10, lever i) | **met** (a to e hold) | Own probe below. |
| R-13, gains + utilisation (11, lever iii) | **met** (a to e hold) | Own probe below. |
| R-14, baseline / gains | met / met | Saturated ratio small/large 5.12 / 13.08 (needs 3); settling ratio 1.85 / 4.85 (needs 1.25) on the feasible sets (tests pass). |
| R-15 | met | Gains: 1000 designs, settled 0.976, feasible 706 (191 / 248 / 267); momentum violations small 37.2 %, medium 17.4 %, large 0 %. Baseline: feasible 780 (239 / 279 / 262). |
| R-16 | met | `test_dataset_reproducible_first_20` (parametrized over both CSVs) and `..._same_platform_exact` pass locally; see verification 4 for the widened tolerances. |
| R-17 | met | The note records reasoning before data, results per lever, the physical mechanism, the miss list (incomplete, see G-6), caveats. |
| R-18 | met | SysML unchanged in substance apart from the new part. |
| R-19 | met | `uv run pytest`: 883 passed, 8 skipped, 6 xfailed (93 s; 5 WP4b strict xfails plus 1 WP3 scikit-learn xfail). `ruff check .`: All checks passed. `ruff format --check .`: 97 files already formatted. `uv lock --check`: ok. Diff outside scope: see below. |
| R-20 | met, with three red runs recorded | Attribution grep over `5dfbc8c~1..HEAD` (case-insensitive `co-authored`, `generated with`, `claude`): 0 matches. All 55 commits authored and committed by Michael Zargham. CI: see below. |

### CI (`gh run list --limit 10`)

Latest is green (`620cfc8`, 3m54s). The implementer reported two red runs on the first-20 reproducibility test; there were **three**, all on `test_dataset_reproducible_first_20[aggressive-csv1]`:

| Commit | Cause (from `gh run view --log-failed`) |
|---|---|
| `7a175a4` (generating commit) | continuous column mismatch, 1 of 20 designs, max relative difference 1.25e-4 against rtol 1e-4 (CI runner versus the author's platform) |
| `4897434` (note-only commit, same code) | `torque_saturated_frac` mismatch, 3 of 20, max relative difference 0.0378 against rtol 2e-2; the continuous columns passed this time |
| `be9ea7d` (rtol 1e-3 on continuous columns) | `torque_saturated_frac` mismatch, 3 of 20, max relative difference 0.0620 against 2e-2 |

Fixed by `620cfc8` (sat fraction rtol 10 % for the aggressive box). Earlier red runs in the window belong to WP3/WP6 (third pass). No other red runs in the last 10.

### R-13 per dataset, my own probe

Script `/private/tmp/claude-501/scratch/probe.py` (not committed). Feasible = settled and `power_ok` and `momentum_ok`, all attributes positive. Orientation: reciprocal (u = -log) for settling, slew time, pointing, mass, effort, peak slew power, depth of discharge and for utilisation (smaller is better); direct (+log) for power margin, energy balance, eclipse reserve; standardize; `solve_lp(U, 0)`; tau grid (60 points, 2 to 300) to the nearest `frac_above_` of 0.10, via `HyperbolicTradeSpace(temperature=tau)`; near-frontier |log V| < 1/tau; bootstrap 100 resamples seed 0. Implementer's numbers in brackets.

| | gains (lever i) | gains + util (lever iii) | baseline + util (lever ii) | baseline |
|---|---|---|---|---|
| feasible n (s/m/l) | 706 (191/248/267) [706] | same | 780 (239/279/262) [780] | same |
| contending set at tau = inf | 6: slew .201, **mass .223**, energy balance .169, effort .143, pointing .135, depth of discharge .129 [identical] | 6: **mass .249**, util .214, power margin .170, slew .141, depth of discharge .122, pointing .104 [identical] | 8: slew .304, effort .296, power margin .193, util .086, **mass .060**, pointing .030, dod .027, reserve .005 [identical] | 6: effort .434, slew .253, margin .179, settling .081, pointing .040, reserve .013; mass 0 [identical] |
| working tau / frac_above | 35.9 / 0.099 [35.2] | 59.8 / 0.096 [58.8] | 50.4 / 0.103 [51.4] | 42.5 / 0.103 [42.8] |
| near-frontier rows (s/m/l) | 63 (21/36/6) [64: 21/36/7] | 79 (0/49/30) [80: 0/49/31] | 88 (15/45/28) [80: 15/41/24] | 102 (78/23/1) [102] |
| mass bootstrap support (median) | 1.00 (0.200) [1.00 (0.200)] | 1.00 (0.249) [1.00 (0.249)] | 0.99 (0.060) [0.99 (0.060)] | 0.00 [0.00] |
| best power attribute support | energy balance 1.00, dod 1.00 | power margin 1.00, dod 1.00 | power margin 1.00 | margin 0.66 |
| settling-mass / slew-mass | **-0.475 / -0.422** [-0.503 / -0.453] | -0.322 / -0.132 [-0.329 / -0.139] | -0.082 / -0.036 [-0.126 / -0.078] | -0.126 / -0.107 [-0.129 / -0.109] |
| pointing-mass | -0.675 [-0.658] | -0.541 [-0.539] | -0.095 [-0.114] | -0.349 [-0.357] |
| settling-effort / pointing-effort / settling-pointing | -0.649 / -0.354 / +0.151 | -0.387 / -0.465 / +0.189 | -0.961 / -0.736 / +0.716 | -0.950 / -0.700 / +0.684 |
| strongest power tensions | peak slew power-pointing -0.68, -settling -0.65 | peak slew power-util -0.57, energy balance-mass -0.56 | dod-mass -0.59, reserve-mass -0.49 | dod-mass -0.65 |
| R-14 ratios | 13.08, 4.85 [13.1, 4.85] | same | 5.12, 1.85 | 5.12, 1.85 |
| (a) (b) (c) (d) (e) | pass pass pass pass pass | pass pass pass pass pass | pass pass **fail** pass **fail** (pointing-mass -0.095) | **fail fail fail** pass pass |

Differences from the implementer come from the tau grid and, for a few cells (gains settling-mass -0.475 against -0.503; baseline+util near-frontier 88 against 80), the working tau. No verdict changes. Robustness of the gains pass across the working tau (rerun at tau 25, 30, 36, 42, 50, 60, `/private/tmp/claude-501/scratch/rob.py`): settling-mass -0.65, -0.55, -0.48, -0.55, -0.30, -0.39; slew-mass -0.62, -0.56, -0.42, -0.52, -0.41, -0.54; pointing-effort -0.34, -0.43, -0.36, -0.34, -0.35, -0.50 (always at or below -0.30 but close); settling-pointing +0.18 down to -0.07 at tau 50 and +0.00 at 60 (not negative, with one value at the edge); two classes with 10 or more near-frontier rows at every tau up to 42 (at tau 50 and 60 only medium and small at 18 and 13, and 16 and 13). The gains pass is not a tau-edge artefact, but (e)'s pointing-effort clause has little margin.

Other facts reproduced (feasible set, medians small / medium / large). Gains: saturated fraction 0.162 / 0.043 / 0.012, settling 104 / 41 / 22 s, 1 degree slew time 33 / 18 / 14 s, total mass 12.63 / 13.22 / 14.36 kg, utilisation 0.807 / 0.631 / 0.334. Baseline: saturated 0.040 / 0.015 / 0.008, settling 130 / 67 / 70 s, slew 84 / 51 / 52 s, utilisation 0.58 / 0.384 / 0.125. Utilisation is at most 1 exactly where `momentum_ok` is true (0 mismatches over 1000 rows in each CSV; feasible maximum 0.994 and 0.998).

## Independent verification asked for

**(1) Ordering.** `75823dc` (01:09:22) changes only the probe note (+97 lines); `7a175a4` (01:16:58) is the first commit with code and the new CSV; the reasoning section of the note is unchanged in HEAD apart from the added results heading (diff of the section between `75823dc` and HEAD: one added heading line). The scope amendment (`78c39c8`, `5b1d087`) precedes both. Ordering is verified from git; git cannot show that nobody simulated privately before 01:09 (the note states only non-dynamic numbers, inertia and closed-form bounds). The reasoning also names the alternative boxes considered on paper and rejected, and says "I do not predict a pass". Predictions that missed: the implementer lists momentum violations (predicted ~25 % small, ~7 % medium; observed 37.2 %, 17.4 %), 1 degree slew times (55 to 65 / 25 to 30 / 15 to 20 s; observed 33 / 18 / 14 s), feasible share (about 75 %; 70.6 %), and association size (within range). The implementer's list is incomplete; I found three more misses (G-6): the settling class ratio predicted "about 1.5 to 2.5" (observed 4.85); "control effort and the pointing attribute ... expected to keep dominating" (observed: mass has the largest weight, 0.223, effort 0.143, pointing 0.135); the lever (iii) expectation "a pass of (c) at best" (observed full pass) and no expectation of the small wheels leaving the near frontier (0 rows). Held: lever ii alone fails (it fails on (c) and (e)); heavier wheels faster; R-14 clause 1 holds (the stated concern that it would shrink was wrong, ratio 13.1).

**(2) Hand probe.** Reproduced above for gains and baseline + utilisation (and for the other two).

**(3) Physics of the aggressive box.** Inertia of the 1000 sampled designs through the model and `inertia_tensor` (script `/private/tmp/claude-501/scratch/phys.py`): Jxx 0.226 to 0.986, median 0.361 kg m2, as the note states. With the linearisation in the note (J theta'' + Kd theta' + (Kp/4) theta = 0, zeta = Kd / sqrt(J Kp), slow pole Kp / (4 Kd)): on the actual dataset Kd/Kp has median 1.06 (baseline 3.95), 96.6 % of designs at or below 5 (baseline 57.2 %; note: 97.8 % on independent draws), 76 % at or below 2; zeta median 1.34, below 0.5 for 4.7 % (note 5.3 %), below 0.7 for 16 %, below 1 (underdamped) for 33 %; slow-pole time constant 4 Kd/Kp has median 4.2 s (baseline 15.8 s). Kd range is the baseline's, only Kp is raised (floor 6.7 times, ceiling 2 times), so Kd/Kp falls by moving Kp; the share of Kd/Kp at or below 5 is the Amendment 5 target (authorized). Consistency with the slow-pole analysis: yes, the box moves the 4 Kd/Kp tail from 16 s to 4 s so that the bang-bang part (50 s small, 19 s medium, 8.5 s large at median inertia) is no longer hidden; the measured correlation of log slew time with log(Kd/Kp) falls (0.79 / 0.89 / 0.97 small / medium / large, from 0.97 / 0.99 / 1.00) and settling-slew correlation falls to 0.698, as it should if the wheel now sets the time. Judgement: the choice is physics-reasoned and recorded before any simulation, with rejected alternatives disclosed and no iteration; it is not tuning toward a test threshold. But it is constructed so the result appears: the note states the aim "to make the demand exceed the cap of every class from the first instant ... so the class sets the speed". The proportional demand at the start of a 30 degree slew (0.13 Kp = 26 to 260 mN m) is above every wheel cap (0.3 to 10 mN m, and below by the available-power cap), so the loop is saturated by design; the gains are far above actuator authority, a legitimate (and common) saturating PD, with a price visible in the data: 37 % of small and 17 % of medium designs fail momentum from overshoot. The finding is therefore conditional on a stiff-loop regime and should say so (G-4).

**(4) Reproducibility tolerance.** `tests/test_cubesat_model.py` lines 562 to 568: continuous columns rtol 1e-4 baseline, 1e-3 aggressive (observed 1.25e-4 at the first red run, margin 8 times); saturated fraction 2 % baseline, 10 % aggressive (observed 3.8 % and 6.2 % in two CI runs of the same simulation code, margin 1.6 times). Documented in the test comment and in the note. Justified by observed CI differences; the baseline tolerances are unchanged. Caveats: it is reactive (set after each red run), the observations show CI itself differs from run to run for identical code (3.8 % then 6.2 %), so the 10 % margin is thin and the test could still flake; and the committed gains CSV was generated on the author's platform. The widening leaves the same-platform exactness test (40 designs twice) as the strict check. Does not affect the enrichment tests, which read the committed CSV only (G-5).

**(5) Lever (ii).** Definition is `peak_momentum_nms` / `maxMomentum` of the design's wheel class, oriented smaller is better (u = -log), at most 1 exactly where `momentum_ok` (0 mismatches in either CSV; `test_momentum_utilisation_matches_the_momentum_flag` asserts it on both utilisation datasets). Capacities (10 / 30 / 100 mN m s) are read from the SysML model through the client (`wheel_capacities()` instantiates each wheel part def; the enrichment fixture uses it; a unit test checks an unknown class raises and the input frame is not modified). The CSVs are not rewritten (`git diff` empty for the baseline; the gains CSV is new in `7a175a4` and has no utilisation column). The ratio form is justified in the note before data; the difference form was run as a declared sensitivity (baseline: mass 0.025, settling-mass -0.253, slew-mass -0.238, still fails; gains: all pass).

**(6) R-4 trial**: see R-4 above (passes for the new gain box part).

**(7) Near-frontier sample caveats.** Gains: large wheels have 6 (mine) or 7 (implementer) near-frontier rows (5 to 22 across tau 25 to 42; 0 at tau 50), so statements about large wheels on that frontier are weak; the two classes with at least 10 are small 21 and medium 36. Gains + utilisation: small wheels have 0 near-frontier rows (medium 49, large 30): the pooled settling-mass association -0.32 comes from medium and large wheels only, so lever (iii) does not show the class that motivates the trade (small wheels, the most torque-limited) on the frontier; slew-mass there is only -0.13. Baseline + utilisation: 15 / 45 / 28 in mine, 15 / 41 / 24 in the implementer's. Baseline: 78 / 23 / 1.

**(8) WP7 implications (observations; which dataset WP7 uses is the supervisor's decision).**
- If the baseline stands: R-13 stays unmet (a, b, c), the tension report finds mass absent (exponent 0, bootstrap 0.00), wheel class appears as a feasibility boundary (small wheels lose 19.2 % of designs) and not as a frontier trade; the finding wording is "agility against mass not found with these measures and this gain box"; settling-effort (-0.95), pointing-effort (-0.70), settling-pointing aligned (+0.68) and pointing-mass (-0.35) are strong; three strict xfails stay, and lever (ii) would add two more; WP7's narrative must state that the null is partly built in (slew time and settling correlate 0.947) and that it depends on the slow pole (Kd/Kp median 3.95).
- If the gains dataset stands: R-13 holds in full, no xfail on it; the tension report shows mass in the contending set (0.22), settling-mass -0.48 to -0.50 and slew-mass -0.42 to -0.45 (heavier wheels buy faster slews), pointing-mass -0.66, strong peak-slew-power tensions (-0.65 to -0.68), and wheel class both a boundary (37 % of small designs) and a frontier trade. But the earlier findings weaken: settling-effort -0.65 (from -0.95), pointing-effort -0.35 (near the -0.30 line), settling-pointing +0.15 (from +0.68, nearly independent, "aligned" no longer holds as a strong claim); settling and slew correlation 0.698 (less redundant); large wheels rest on 6 to 7 near-frontier rows. The finding wording must include the regime: stiff loop with demand above actuator authority, a choice of the case; the baseline CSV remains the comparison (the richness failure is a property of the gain box, per the note). The notebook should disclose that the dataset was chosen after the baseline failed R-13, with the baseline retained.
- If a utilisation variant stands: eleven attributes (d = 11), the notebook must derive utilisation from the model's capacities; with gains + utilisation small wheels are absent from the near frontier (0 rows) and slew-mass is weak (-0.14); with baseline + utilisation R-13 fails (c, e).
- Either way: WP7's dataset path, attribute set and finding text follow the supervisor's choice; the third-pass facts (power never limits a slew; redundant pairs) need rechecking on the gains dataset (not rerun here).

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-8 exist | met | See Deliverables. |
| R-1 to R-20 pass as checked | met on the gains and gains+utilisation datasets; **not met (R-13) on baseline and baseline+utilisation** | See R-13 per dataset. |
| R-13 and R-14 hold on the committed dataset | depends on which dataset stands: holds on gains (a to e; R-14), fails on baseline | Supervisor's choice (G-1). |
| Non-goals untouched | met | See below. |

## Outside the scope

- **Out-of-scope changes:** none by WP4b in amendment 5. `git diff 6c8c3e9 HEAD --stat -- . ':!work-packages' ':!docs/superpowers/notes' ':!examples/adcs' ':!tests/test_adcs_enrichment.py' ':!tests/test_cubesat_model.py'` lists only `CLAUDE.md` and the spec (both one-line title edits from the repository rename `a469aa2`, a supervisor-driven change, not WP4b). `work-packages/` changes are WP7, WP8, README and WP4b records. Earlier accepted extras (the `.github/workflows/test.yml` cache edit, `pyproject.toml`, `uv.lock`, comment edit to `extended_design_space.sysml`) are unchanged since the third pass.
- **Non-goals touched:** none. `adcs_sim.py` byte-identical; no estimator, solver, coordinates, WP2/WP3 or notebook change; no `sysml-toolkit` dependency; WP4 CSV, tests and `design_space.py` untouched; baseline cubesat CSV untouched since `a27502e`.

## Trials (undone)

1. Utilisation derivation: divide by `2 * cap` in `add_momentum_utilisation`: `test_wheel_capacities_and_momentum_utilisation`, `test_momentum_utilisation_matches_the_momentum_flag[headroom]` and `[gains_headroom]` fail (3 failed, 71 passed, 5 xfailed). Restored by `git checkout`.
2. Gain-box coupling: map `aggressive` to `designSpace`: `test_aggressive_gain_box_is_read_from_the_model` and `test_dataset_reproducible_first_20[aggressive-csv1]` fail (2 failed, 72 passed, 5 xfailed). Restored by `git checkout`. `git status` clean afterwards.

## Observations (not counted as failures)

- Strict xfails per dataset are a tripwire and are correct for the baseline and lever ii; they would become dead weight if the baseline stops being a tested dataset.
- Slew time and settling are still near-redundant on the baseline (0.947) and less so on gains (0.698).
- Gains pointing-effort (-0.35) and settling-pointing (+0.15) are close to their (e) thresholds; settling-mass at tau 50 is -0.30 (edge). The pass at the working tau is robust over tau 25 to 42.
- The implementer's R-13 table is matched by my probe within the tau-grid tolerance on every verdict.
- Earlier dispositions on record: first round G-1, G-3, G-4, rest of G-5 accept as is, stale help text fixed (verified); G-2 momentum "Enforce as feasibility"; second-pass R-13 stop rule answered "Reopen levers..." then "One physics-justified lever: slew-time attribute"; third-pass G-1 (R-13 under the stop rule) answered "try both new levers then report back" (amendment 5, this delivery); third-pass G-2, G-3, G-4 were left pending and are carried forward as G-6 (partly) and G-8 below.

## Open decisions (for the supervisor)

- **G-1. Which dataset stands.** R-13 holds on `adcs_designs_cubesat_gains.csv` (lever i, 10 attributes) and with utilisation (lever iii, 11 attributes); it fails on the baseline (a, b, c) and on baseline + utilisation (c, e). Choosing which dataset the notebook and WP7 read, and so whether R-13 stands as met or recorded as a finding, is the supervisor's decision. — options: accept as is (record a chosen dataset and the R-13 outcome for it) / fix before acceptance / follow-up work package. **pending**
- **G-2. If the baseline stands:** R-13 (a, b, c) remains unmet under the Amendment 4 and 5 stop rule, with five strict xfails; the supervisor would record R-13 as the finding. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-3. Thin margins on the gains pass:** pointing-effort -0.35 (threshold -0.30), settling-pointing +0.15, large-wheel near-frontier 6 to 7 rows, and in lever iii small wheels 0 near-frontier rows. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-4. Conditional regime of the aggressive box:** the box is physics-reasoned and written before data, but built so the wheel is the bottleneck (demand above every cap from the first instant, 37 % of small designs infeasible on momentum); the finding is valid for a stiff-loop regime and the notebook should say so. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-5. Reproducibility tolerance for the aggressive box** (rtol 1e-3, saturated fraction 10 %): justified by observed CI differences, documented, but reactive and thin (10 % against 6.2 % observed; three red runs, causes above, the implementer reported two). — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-6. Incomplete miss list in the note:** the note's "expectation against result" omits the settling class ratio (predicted 1.5 to 2.5, observed 4.85) and the expectation that effort and pointing would dominate (mass has the largest weight). — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-7. WP7 consequences** (item 8 above) depend on G-1 and should be carried into WP7's scope after the choice. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-8. Small items carried from the third pass:** the note's "55 %" wheel-mass variance share is feasible-set-specific; the ordering evidence cannot exclude private earlier simulation; the full suite shows one non-WP4b xfail (WP3). — options: accept as is / fix before acceptance / follow-up work package. **pending**

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
| G-7 | pending | |
| G-8 | pending | |
| Previously dispositioned (see Observations) | as recorded | accept as is / fixed / amendments 2 to 5 as quoted in `WP4b-decisions.md` |

## Recommendation

**Do not recommend acceptance yet: every gap is pending and the standing dataset is not chosen.** The evidence supports the following. R-13 is met on the aggressive-gain dataset (lever i) and on gains + utilisation (lever iii) and is not met on the baseline or baseline + utilisation; R-14 holds on all. All other requirements are met: full suite (883 passed, 5 WP4b strict xfails), `REQUIRE_OPENSYSML=1` tests, ruff, lock, attribution (0), authorship, `adcs_sim.py` byte-identical, WP4 tests and the baseline CSV untouched, CI green on the latest run (three earlier red runs on one reproducibility test, causes above). My independent probe reproduces every implementer verdict, the reasoning note was committed before the generating commit, and the trials break tests as they should. Lever (i) is the sufficient lever; lever (ii) alone does not pass and lever (iii) adds a correlated attribute that removes small wheels from the near frontier. Choosing which dataset stands (G-1), and so whether R-13 is recorded as met or as a finding, is the supervisor's decision; once G-1 to G-8 have dispositions the recommendation can be restated (with the gains dataset standing and the gaps noted, the evidence would support acceptance with the listed gaps noted).

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
