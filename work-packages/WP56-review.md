# WP56 review: Sections 7 to 9 (the second unit, branch `wp56p`)

The second unit rewrote the prose of Sections 7, 8 and 9 of `paper/paper.ipynb` on the figures the first unit landed
(dev b8846a3). Goals G1, G2, G5 and G6 of `WP56-scope-of-work.md`; G3 and G4 landed with the first unit. This file
holds the before-and-after table of every claim, number and figure in the three sections (G6), the R-1 table of
sentences about the cubesat model with their records, the checks and their outputs, and the screenshots with their
cold reads (`WP56-rounds/prose/`).

## Words (R-5)

Two counts. The scope's measure (G6, R-5: 1,336, 1,426 and 558 at WP55's head, 3,320 together) is the words of the
Markdown cells as typed (`wc -w` of the cell sources, captions included, generated sentences not). The ledger's
measure (`tests/test_paper.py::words_by_section`) is what renders, generated sentences included.

| Section | typed Markdown, dev b8846a3 | typed Markdown, after | rendered with generated sentences, dev b8846a3 | after |
|---|---|---|---|---|
| 7 Case construction | 1,101 | 1,003 | 1,482 | 1,215 |
| 8 Case analysis | 1,033 | 1,066 | 1,901 | 1,929 |
| 9 Discussion | 558 | 493 | 803 | 494 |
| together | 2,692 | 2,562 (R-5: at or below 3,320) | 4,186 | 3,638 |

At WP55's head (98d9753) the typed counts were 1,336, 1,426 and 558 (3,320) and the rendered 1,718, 2,299 and 803.
Section 8 grew by 28 rendered words against dev b8846a3: it gained the requirements after the fit with their
excluded counts, the three stakeholders and the collapse with its refit, the decision on the new rules and the
sentence naming its calls and data (G2), and lost the known-answer paragraph, the K temperatures, the
strict-convexity remark, the percentile rule, the two-stakeholder paragraph, the pick's tension and the caption's
caveats. The length ledger has a `[[cut]]` row per section lowering each ceiling to its count after.

## R-1: every sentence about the cubesat model, with its record

| # | Sentence (section) | Record checked | Verdict |
|---|---|---|---|
| 1 | "a fleet of identical 12U-class cubesats whose power, mass and attitude control are coupled, described by a SysML v2 system model" (7) | `examples/adcs/model_v2/cubesat.sysml` header: the illustrative 12U-class cubesat; WP23 round 2's coupling check (pack mass, inertia, usable torque exchanged among power, mass and the slew); WP30's cost model of a fleet of identical satellites; `model_v2/coverage.py` part 3 (the coupling table) | matches; register C973 |
| 2 | the problem as a triple: seven design variables, four feasibility conditions and six requirements (7) | `cubesat.sysml` section 1 (wheelClass, grade, panelSpan, batteryCapacity, Kp, Kd; fleetSize 1 to 30) and section 5 (13 requirement defs); `case.CUBESAT.flags`, `.requirements`, `.cost_requirements` | matches |
| 3 | swap the wheel and the tracker, tune panel span, battery capacity and the gains; the fleet size is no part and the assembly view does not draw it (7) | `model_v2/views/assembly_view.puml` (swap: wheelClass, grade; tune: panelSpan, batteryCapacity, Kp, Kd; no fleet), `test_the_body_states_the_marks_the_coverage_and_the_draw` | matches; C495 re-anchored |
| 4 | "the unit cost falls as the fleet grows and the fleet cost, the unit cost times the fleet size, rises" (7) | `cubesat.sysml` FleetCost (pricing curves, nondecreasing in fleetSize) and UnitCost (FleetCost / fleetSize); data of record ratio 1 to 6e-9 | matches; C633 |
| 5 | thirteen attributes by subsystem (7, generated) | `case.CUBESAT.subsystems` (the behavioural view's grouping, the analyst's) | matches |
| 6 | "The SysML v2 model states thirteen requirements, one for each traded metric", four feasibility conditions (settle, momentum, power, depth of discharge), six after the fit, three filter nothing (7) | `cubesat.sysml` section 5; `generate_findings.FEASIBILITY_REQUIREMENTS` (the flag each requirement's verdict sets, `cubesat_oracle.py` "feasibility"); the generator asserts the three bounds on the feasible designs of both regimes (minimum 1.46, 6.5 W, 0.95 W h) | matches; C498 re-anchored, C674 re-anchored to the generator |
| 7 | the pointing error, the unit cost and the fleet cost are MoEs, the other ten MoPs (7) | `model_v2/views/coverage.csv` (generated from the docs' first words, WP23 D-2) | matches; C492 |
| 8 | "A fourth MoE, the fleet's coverage probability, is derived from the fleet size and the pointing error and is not traded" (7) | `model_v2/stakeholders.sysml` section 5 (`CoverageProbability`, doc "MoE"; reads fleetSize and PointingError); the column is not in the data of record (`test_coverage_column_on_the_data_of_record`) | matches; C974 |
| 9 | Table 2: each metric's mark, requirement and stage, the limits 0.008495 degree, 0.05922 N.m.s, 2.6 W, launch cost 105,770 USD at 7,000 USD per kg, 350,000 USD per satellite, 6,000,000 USD per fleet (7, generated) | `coverage.csv` (mark, requirement) and `case.CUBESAT` (stage, limits), which `test_requirements_are_the_models_budgets` holds to `cubesat.sysml` part `budgets` and `environment.launchRate` | matches; new test `test_the_requirement_order_table_is_the_models_marks_in_the_cases_order` |
| 10 | "the slew is integrated in Python, and every other attribute and the four feasibility verdicts are computed by the SysML v2 model's calcs and requirements" (7) | `experiments/cubesat_oracle.py` docstring (measure, account, feasibility); `test_the_flags_come_from_the_requirements_not_from_python` | matches; C975 |
| 11 | the gain ranges of the two regimes (7) | Appendix C.1's table (generated from the model's gain boxes); `test_the_regimes_gain_ranges_are_the_ones_section_8_states` | matches; C663 |
| 12 | the baseline configuration: a fleet of one, medium wheel, medium tracker, 0.6 m, 80 Wh, Kp 0.03, Kd 0.3; pointing error 0.0155 degree, unit cost 461,360 USD; fails the pointing-error and unit-cost requirements (7, generated) | `cubesat.sysml` section 7 (`cubesatBaseline`) and the `not satisfy` statements; `case.CUBESAT.baseline_configuration`; the behavioural view's boxes ("not satisfied by cubesatBaseline") | matches. Finding: the model's header says 63.7 % of the baseline regime pass the pointing requirement; the data of record give 65.6 % (the generated sentence; C403's note already records the typed 63.7 % as an earlier record). The model's comment is stale; recorded for `review/open-questions.md`, not edited (a non-goal) |
| 13 | "fleet cost is unit cost times fleet size, so the sponsor's objective rides on the manufacturer's and the fleet size" (8) | `cubesat.sysml` UnitCost = FleetCost / fleetSize; `fleet_refit_sentence` asserts the ratio on every feasible row (6e-9) | matches; C977 |
| 14 | the coverage probability "the probability that at least one satellite of the fleet covers a target in the planning period"; the SysML v2 model defines it and its two constants (8) | `stakeholders.sysml` `CoverageProbability` doc and `CoverageAssumptions`; `test_coverage_probability_in_the_model_is_the_pipelines` (first unit) | matches |
| 15 | "The decision gives each of three objectives to one stakeholder" (8) | `WP56-decisions.md` (his mapping); `case.STAKEHOLDER_OF`. The SysML v2 model's `stakeholders.sysml` names two stakeholders (sponsor, operator); the manufacturer is the decision's, so the sentence is said of the decision, not of the model | matches as worded |
| 16 | "such a revision of the cost model enters as a new table, and the same calls test whether the collapse holds" (8) | `case.fleet_ternary_study` and `case.fit_study` read the table; `fleet_refit_sentence` refits it | matches |
| 17 | Table 3's baseline row: coverage probability 0.032, level -0.330 (8, generated) | `decision()` scores the model's baseline with the K = 2 fit and the model's coverage formula | matches |
| 18 | "it was traced to the SysML v2 model's definition of the fleet cost and checked on every row of the data" (9) | as 13 | matches; C985 |
| 19 | "The decision problem is the SysML v2 model's requirements and measures of effectiveness, with one stakeholder per objective of the decision" (9) | as 6, 7, 15 | matches |
| 20 | "the coverage probability's two constants are mission assumptions the operator supplies" (9) | `CoverageAssumptions` doc | matches; C986 |
| 21 | "The case's hardware values are illustrative and its costs a lower bound on a full costing; the case has no schedule, no payload and a flat launch price" (9) | `cubesat.sysml` header ("Every number is illustrative"), `stakeholders.sysml` lowCost ("a lower bound on a full costing"), the launch rate; `test_appendix_c8_states_what_the_model_file_says_about_cost_and_what_is_left_out` | matches; C501 re-anchored |

Stale sentences rewritten or cut: "Our case is a cubesat model coupling ..." ("model" without its object); "the decision
table's fleets are four and more" (the table now holds fleets of 1, 4, 10 and 25); "The case's two stakeholders: the
operator cares about the pointing error, the sponsor about the unit cost and the fleet cost" (contradicted the
three-stakeholder mapping and the operator's measure); the table rows "operator alone" and "between them" on
pointing error; "Theorem 7 gives the rates in the attributes' own units" (the pull-back, L9, is Theorem 8 in the
built paper; the generator now counts the number from the notebook, `_theorem_number`).

## G6: every claim, number and figure of Sections 7 to 9, before and after

| Item | Before (dev b8846a3) | After | Generator or record |
|---|---|---|---|
| The case, its coupling | "Our case is a cubesat model coupling power, mass and attitude control" | the fleet of identical 12U-class cubesats, coupled, with the SysML v2 model named | `cubesat.sysml`; C973 |
| Precedent | none | the CubeSat design problem among OpenMDAO's applications | Gray et al. 2019, Section 7 and Table 13, read in the MDO Lab preprint by this unit; C972 |
| The problem as a triple | none | displayed (maximize, with respect to, subject to) | `cubesat.sysml` sections 1 and 5 |
| Design variables, fleet size 1 to 30, the two costs not collinear | Section 7 | Section 7, reworded | C495, C633 |
| "worked example of design optimization, not a study of either use" | Section 7 | cut (Section 1 says the two uses) | none |
| Black box to the method | Section 7 and Discussion "Cross-application" | Discussion, once | C031 re-anchored; C117, C118 retired |
| Figure 4 (assembly), Figure 5 (behavioural), Figure 6 (temperature) | Section 7 | unchanged, captions untouched | first unit; `fig-tau` now referenced from Section 7's provenance paragraph |
| Thirteen attributes by subsystem | generated | unchanged | `attributes_sentence` |
| Participation (two metrics in no contending set) | generated, Section 7 | to D.3 (moved file) | `participation_sentence`; C491, C629 keep their generator anchors |
| Requirements: thirteen, four feasibility, six after the fit, three filter nothing | three paragraphs with counts | one sentence and Table 2 | `requirement_order_table`; C498, C674 |
| Ladder provenance of the four thresholds | Section 7 | to D.17 (moved file) | C500 retired |
| MoE and MoP | Section 7 | Section 7 and Table 2, once | `coverage.csv`; C492 |
| Coverage probability as a fourth MoE | none | Section 7 and Table 2 | `stakeholders.sysml`; C974 |
| Pricing detail (covered cost, launch slot, 8,000,000 USD budget) | Section 7 | cut (C.8 holds it) | C493 retired |
| "The hardware values ... illustrative", no schedule, no payload, flat launch price | Section 7 | Section 9's limits | C501 re-anchored |
| Data provenance | Appendix C pointers only | one sentence (oracle) and "Appendix C.6 names each table with the command that wrote it" | `cubesat_oracle.py`; C975 |
| Regimes' gain ranges | Section 7 | Section 7 | C663 |
| Conditioning, standard scaler | Section 7 | Section 7 | C426 |
| Baseline configuration | its pointing error and one share | its configuration, two attributes, two requirements failed, two shares; Table 3's first row | `baseline_requirement_sentence`; C403 re-anchored |
| 3,000 designs per regime, 2,134 and 2,355 feasible | generated | unchanged | `datasets_sentence` |
| Fit temperature, band, effective sample | generated | unchanged | `temperature_sentence` |
| Robust scaler; resampling not assessed at K = 1 | generated, Section 7 | to D.5 and the open questions | `temperature_variants_sentence`; C627, C628 |
| Planted tables, 16 of 20 | Section 7 (count) and Section 8 (detail) | Section 8, the count once, at K = 2 | `planted_sentence`; `recovery_sentence` to D.14 |
| Nondominated counts | generated, opens Section 8 | opens Section 8, with one sentence that says what it leaves | `nondominated_sentence` |
| K = 1 seven-lemma, Figure 7 | Section 8 | unchanged | `k1_sentence` |
| Choosing K | generated | unchanged | `choosing_k_sentence` |
| K temperatures and bands (G-9) | Section 8 | to D.15 | `k_temperatures_sentence` |
| Figure 8 (chart), Figure 9 (tension) | Section 8 | unchanged | first unit |
| Terms: contending sets 8 and 7, "leads term 1" | generated | 8 and 7; "carries the largest exponent of term 1 (0.43)"; total mass on term 2 drawn in the matrix outside its contending set (0.0064) | `terms_sentence`; C983; the cold read's defect 2 |
| Elasticity -0.9 | generated, plain "alpha_i/alpha_j", "Theorem 7" | -0.9 per percent, the matrix's -2.8 per unit, $\alpha_i/\alpha_j$ as MathML, Theorem 8 | `elasticity_sentence`; C624, C984; defects 1 and 3 |
| "worth most on the term" | undefined in prose | defined in one sentence (exponent over conditioned value at the balanced point) | `case.tension_order`; C976; defect 4 |
| Strict convexity; pairs counted as one | Section 8 | to D.4 | C409 retired |
| Regimes 7- and 8-lemma | generated | unchanged | `regime_sentence` |
| Propose, predict, check: percentile rule, never clipped | Section 8 | to D.10 | C391, C041 retired |
| Propose, predict, check: errors within the band | generated | unchanged | `predict_check_sentence` |
| Proposals fail depth of discharge | Section 8 and Discussion | Section 8, one sentence | C404; `predict_reading` to D.10 |
| Requirements after the fit as constraints with excluded counts | Discussion pointer to D.17 | Section 8, generated (178 of 238 jointly; 108, 95, 64, 57, 12, 8) | `requirements_sentence`; C982; stability entries `requirement | primary | ...` (none moved) |
| Design sets before the fit | Discussion, generated | Section 8 | `design_sets_sentence`; C407 |
| Unconstrained-then-constrained | Discussion | Section 8 | C406 re-anchored |
| Three stakeholders, coverage definition, the collapse | Figure 10 caption only | Section 8 paragraph (his sentences) | `WP56-decisions.md`; C977 |
| Figure 10 | Section 8 | unchanged, now introduced by its paragraph | first unit; C971 |
| Identity 6e-9; two-term refit 0.14/0.86, 0.54/0.46, 0.000 | `WP56-rounds/figures/ternary-values.txt` | Section 8, generated beside its call | `fleet_refit_sentence`; C978, C977 |
| Revised cost scaling checked by refitting | none | one sentence | his words, 14:03 EST |
| Decision paragraph | two stakeholders; fine-tracker question (0.56 M USD); picks 5 and 4 satellites | three stakeholders; manufacturer and operator pick 25 satellites (234,000 USD each, 5.85 M USD, 0.98); sponsor 4 (1.13 M USD, 0.46); between them 10 (2.88 M USD, 0.76) of the 17 nondominated on fleet cost and coverage | `decision_sentence`; C979, C980; C596 to C608, C625 retired; stability entries added (none moved) |
| Table 3 | six rows on pointing error, unit cost, fleet cost | five rows on fleet cost, unit cost, coverage probability | `decision_table`; C981; C615 retired |
| Table caption caveats ("does not tell the schedule ...") | caption | cut (Section 9's limits) | C618 retired |
| The pick's tension (-1.4 M USD per arcsecond) | Section 8 | to D.19, reworded or retired by WP57c | `tension_sentence`; C797, C798 |
| Closing: the decision, the code and data | none | one paragraph (Table 3, `case.k_fits`, `decision`, F.3, F.2) | C987 |
| Interpretation is human validation; verify and validate | two paragraphs | one paragraph, with the case's check of the collapse | C985 (the check) |
| Value proposition | none | "What the case showed" (Section 1's sentence answered) | the case's generated sentences above |
| The three layers | none | one paragraph | Section 2 |
| Three claims | Discussion | queued for WP57d (`assumptions-queue.md`) | C039 retired, C040 re-anchored |
| Why a surface; Trade-offs beyond the first, PCA; Novelty and white space; The kernel direction | Discussion | queued for WP57d | C114, C121, C122, C123 retired |
| What propose, predict, check showed | Discussion, generated | to D.10 | `predict_reading`; C397 to C399, C405 keep their anchors |
| Limits | "Limits, in brief", and caveats in Sections 7, 8 and the table caption | one passage, the last of Section 9 | C043, C112, C113, C119, C120, C501, C986 |

## The register

Retired (30), each with its sentence: C039, C041, C109, C114, C116, C117, C118, C121, C122, C123, C391, C409, C493,
C500, C596, C597, C598, C599, C600, C601, C602, C603, C604, C605, C606, C607, C608, C615, C618, C625. Re-anchored
or narrowed to the new wording: C031, C040, C111, C112, C113, C119, C120, C403, C406, C495, C498, C501, C624, C637,
C674. Added: C972 to C987 (16). The OpenMDAO read (C972) is recorded here, since the WP10 reading pass is a closed
record of 56 rows: Gray et al. (2019), MDO Lab preprint, Section 7 "Applications" and Table 13: "a satellite MDO
problem that maximized the data downloaded by varying satellite design parameters (related to solar panels,
antenna, and radiators) as well as time dependent variables", disciplines orbit dynamics, attitude dynamics, cell
illumination, temperature, solar power, energy storage and communication; the code at github.com/OpenMDAO/CADRE.

## Moved and queued

`WP56-rounds/moved-to-appendix.md`: eleven typed paragraphs or sentences and six generated sentences for Appendix C
and D (WP57c), with what each target already holds, and the note that D.19's rule paragraph must follow the new
rules. `WP57-rounds/assumptions-queue.md`: seven entries for WP57d (Three claims, Why a surface, Trade-offs beyond
the first, Novelty and white space, The kernel direction, the Appendix B sentence, the resampling sentence).

## Tests changed

The decision tests follow the three-stakeholder rules (picks, counts, phrases, the perturbed record, the caption);
tests that read a moved generated sentence read its generator (`_moved`); the disclosure test admits "SysML v2" in
the body (the supervisor's rule that "model" names its object; the case is narrated from the SysML v2 system model)
and still refuses the tools; the float count is 13 (Table 2). New: the requirement-order table, the refit sentence,
the requirements sentence, the terms and elasticity sentences against Figure 9, the limits stated once at the end of
Section 9 (R-4).

## The checks, with their outputs

| Check | Command | Output |
|---|---|---|
| Notebook re-executed | `MPLCONFIGDIR=<warm cache> uv run python paper/execute_notebooks.py paper.ipynb` (from `paper/`) | "executed paper.ipynb", exit 0; the outputs equal the generators' (the generated cells patched during the unit were compared with the full re-execution: identical) |
| Fast suite | `uv run pytest -q -m "not slow" -n auto` (warm `MPLCONFIGDIR`) | 2,091 passed, 17 skipped, 2 xfailed, exit 0; without the warm font cache four plotting tests and three diagnostic-pair fixtures fail on "Failed to find font DejaVu Sans" (the environment, as in the first unit) |
| Slow paper tests | `uv run pytest -q -m slow -n auto tests/test_paper.py` | 30 passed, exit 0 |
| Register | `uv run pytest -q tests/test_claims_register.py` | 21 passed |
| Lint, format, lock | `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check` | all checks passed; 620 files formatted; resolved 194 packages |
| Residuals | `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` | exit 1 as on dev; `paper/paper.ipynb` at or below dev b8846a3 on every count (hedges 6 = 6, intensifiers 3 < 4, dense paragraphs 29 < 37, long sentences 66 < 69, undefined terms 20 = 20; parentheses, long parentheses and deep clauses no longer above the baseline); the rises in `docs/`, `site/` and the glossary long-forms are dev's |
| Vocabulary | `uv run python scripts/check_vocabulary.py` | 0 new violation(s), 67 known |
| Proof map | `uv run python -m derivation.proofmap` | PROOF MAP OK: 22 lemma files, 549 tagged steps (unchanged) |
| Data of record, derivations, supporting material | `git diff --stat -- examples/adcs/data derivation paper/supporting_material.ipynb` | empty |
| Stability of the new quantities | `paper/stability_extra.py` quantities on the five regenerations (scratch `sensrun-out`, which reproduces every committed decision entry exactly), merged into `stability_extra.json` | 25 new entries, none moved; no existing entry changed |
| Build | `cd paper && BASE_URL=/paper uv run --frozen myst build --html` | exit 0, no warning; served on port 8857; captures in `WP56-rounds/prose/` |
