# WP4b — Review report (fifth pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP4b-scope-of-work.md` with Amendments 1 to 6 (R-14 relative clauses; momentum enforced; physically consistent 30 degree scenario; slew-time attribute and ten attributes; aggressive-gain box and momentum utilisation levers; Amendment 6: the aggressive-gain dataset is the primary case dataset on which R-13, R-14, R-15 are evaluated, the 30 degree baseline is the regime comparison whose null result is a recorded finding) |
| **Scope approval verified** | The project has no PRs; the recorded act is `work-packages/WP4b-decisions.md`: "Scope approval (approval gate)", supervisor mzargham, verbatim "okay proceed", document at `d27c177`. Amendments 1 to 5 and the round-4 dispositions ("Both, as two regimes"; "Fix G-6 note, G-5 to follow-up, accept the rest") are recorded verbatim in the same file; Amendment 6 is committed in `5665272` and applies the supervisor's "Both, as two regimes". |
| **Work reviewed** | `main` at `93d162c`. Since the fourth pass (`2258281`): `a104195` (decisions), `5665272` (Amendment 6), `5c252f7` (regime structure in the suite, complete miss list, conditions, two-regimes table, follow-up candidates), `93d162c` (line length). Earlier delivery as in the fourth pass (`5dfbc8c` to `620cfc8`). Start for diffs `5dfbc8c~1`; WP4 state `932bbe4` (simulator) and `9680193` (WP4 tests, CSV, design space). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4b-decisions.md`, after this report |

A fresh reviewer who built none of WP4b and wrote none of its earlier reviews; replaces the fourth-pass report. Every command was run in this session with `unset VIRTUAL_ENV`. Review only: four trial edits were made and undone with `git checkout`; `git status` is clean. The review is a complete one from step 1 against the amended scope; R-13, R-14 and R-15 are evaluated on the PRIMARY dataset `adcs_designs_cubesat_gains.csv`, and the baseline is checked through its regime-comparison assertions.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/cubesat_tradespace.sysml` (baseline `designSpace`, `AggressiveGainSpace`/`aggressiveGains`); unchanged since `7a175a4` (`git diff 7a175a4..HEAD -- examples src` empty). |
| D-2 | met | `examples/adcs/cubesat_model.py` loads the model through `opensysml`, samples from model ranges, `GAIN_BOXES`, `wheel_capacities()`, `add_momentum_utilisation`; unchanged since `7a175a4`. |
| D-3 | met | `generate_dataset.py` additive flags (`--model`, `--gain-box`); defaults unchanged. |
| D-4 | met | Primary `adcs_designs_cubesat_gains.csv`: last changed `7a175a4`, `git diff 7a175a4 HEAD --stat` empty. Baseline `adcs_designs_cubesat.csv`: last changed `a27502e`, `git diff 6c8c3e9 HEAD --stat` empty. |
| D-5 | met | `uv lock --check`: "Resolved 173 packages". `pyproject.toml` last changed `5dfbc8c`. |
| D-6 | met | `REQUIRE_OPENSYSML=1 uv run pytest -q tests/test_cubesat_model.py tests/test_adcs_enrichment.py`: **73 passed**, no xfail, no skip, 50 s. No `xfail`/`EXPECTED_FAIL` remains in either test file (grep). |
| D-7 | met, with wording-level staleness | Probe note updated (see "Probe note checks"). |
| D-8 | met | `WP4b-decisions.md` holds approval, amendments 1 to 5, round-4 dispositions verbatim, follow-up candidates; acceptance pending. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `git diff 932bbe4..HEAD --stat -- examples/adcs/adcs_sim.py` empty (byte-identical). `git diff 9680193..HEAD --stat -- tests/test_adcs_case.py examples/adcs/data/adcs_designs.csv examples/adcs/design_space.py` empty. WP4 tests pass in the full suite. |
| R-2 | met | Original CSV, WP4 tests, design space untouched; defaults of the generator unchanged. |
| R-3 to R-6, R-8 to R-10 | met | Pass inside the 73 model and enrichment tests and the full suite; `cubesat_model.py`, `.sysml`, `generate_dataset.py` have no change since `7a175a4`. |
| R-4 | met | Test passes; trial on a model copy was done in the fourth pass and the code is unchanged since. |
| R-7 | met | Panel monotonicity tests pass. |
| R-11 | met | Attributes test passes; momentum utilisation is derived on read and documented. |
| R-12 | met | `uv lock --check` ok; hard-failing fixture; `REQUIRE_OPENSYSML=1` in CI. |
| R-13, PRIMARY (gains, 10 attributes) | **met** (a to e) | Own hand probe, below. Tests `test_a_`, `test_b_`, `test_c_`, `test_e_` run on `gains` and `gains_headroom` and pass; `test_d_` runs on all four. |
| R-13, baseline (comparison) | **not met, as the recorded finding** (a, b, c fail; d, e hold) | Not a failure of the package under Amendment 6. Asserted by `test_regime_comparison_stock_gains[baseline]` (passes). |
| R-14 (primary) | met | Small/large saturated ratio 13.08 (needs 3), settling ratio 4.85 (needs 1.25) on the feasible set. Baseline for comparison 5.12 / 1.85. |
| R-15 (primary) | met | 1000 designs; settled 0.976; feasible 706 (191 / 248 / 267); momentum violations small 37.2 %, medium 17.4 %, large 0 %. Baseline: settled 0.978, feasible 780 (239 / 279 / 262). |
| R-16 | met | `test_dataset_reproducible_first_20` over both CSVs and `..._same_platform_exact` pass locally. Tolerances for the aggressive box are widened (rtol 1e-3, saturated fraction 10 %); see G-5 follow-up. |
| R-17 | met | The note records reasoning before data, results per lever, mechanisms, the miss list (now checked as complete save one item, G-A below), conditions of the finding, the two-regimes table. |
| R-18 | met | SysML unchanged in substance. |
| R-19 | met | `uv run pytest`: **882 passed, 8 skipped, 1 xfailed** (94 s; the xfail is the WP3 scikit-learn check, none is WP4b). `ruff check .`: All checks passed. `ruff format --check .`: 97 files already formatted. `uv lock --check`: ok. Diff outside scope: see below. |
| R-20 | met, with three red runs recorded | `git log 5dfbc8c~1..HEAD` message grep (case-insensitive `co-authored`, `generated with`, `claude`): 0. All 61 commits authored and committed by Michael Zargham. CI below. |

### CI (`gh run list --limit 10`)

Latest seven runs (`620cfc8` through `93d162c`) are green, the latest `93d162c` in 4m05s. Three red runs in the window, all in the aggressive-box first-20 reproducibility test, causes confirmed from `gh run view --log-failed`:

| Commit | Cause |
|---|---|
| `7a175a4` | continuous column, 1 of 20 designs, max relative difference 1.25e-4 against rtol 1e-4 |
| `4897434` (note-only commit, same code) | `torque_saturated_frac`, 3 of 20, max relative difference 0.0378 against 2e-2 |
| `be9ea7d` | `torque_saturated_frac`, 3 of 20, max relative difference 0.0620 against 2e-2 |

Fixed by `620cfc8`. No red run since.

## Independent hand probe on the PRIMARY dataset

Own script (feasible = settled, `power_ok`, `momentum_ok`; reciprocal orientation for smaller-is-better, direct for the three larger-is-better; log; standardize; `solve_lp(U, 0)`; tau grid for `frac_above_` near 0.10; near-frontier |log V| < 1/tau; 100 bootstrap resamples seeded 0). Compared with the probe note:

| Quantity | Note | My probe |
|---|---|---|
| feasible n (s/m/l) | 706 = 191/248/267 | 706 = 191/248/267 |
| contending set at tau = inf | slew .201, mass .223, energy balance .169, effort .143, pointing .135, DoD .129 | identical (all six) |
| mass bootstrap support | 1.00 | 1.00 (median .200) |
| settling-mass / slew-mass | -0.503 / -0.453 | -0.475 / -0.422 (working tau 35.9 against the note's 35.2; differences are the tau grid) |
| pointing-effort / settling-pointing | -0.349 / +0.143 | -0.354 / +0.151 |
| near-frontier rows (s/m/l) | 21 / 36 / 7 | 21 / 36 / 6 |
| R-14 | 13.1 / 4.85 | 13.08 / 4.85 |
| (a) to (e) | pass | pass |

Baseline, same script: contending set of six with no mass (settling .081, slew .253, pointing .040, effort .434, power margin .179, reserve .013), mass support 0.00, settling-mass -0.126, slew-mass -0.107, pointing-effort -0.70, settling-pointing +0.684, near-frontier 78 / 23 / 1. The note's "Two regimes" table matches within the tau-grid tolerance on every row (baseline settling-mass -0.129, slew-mass -0.109, pointing-effort -0.701, settling-pointing +0.681). Median Kd/Kp 1.06 against 3.95 (table: 1.06, 3.9); underdamped share 33.4 %, damping below 0.5 for 4.7 % (note: 33 %, 4.7 %). Median saturated fraction by class on the feasible sets: baseline 0.040 / 0.015 / 0.008, primary 0.162 / 0.043 / 0.012.

## Regime-comparison assertions are not vacuous (trials, undone)

1. Pointed the `baseline` dataset at the primary CSV (equivalent to the baseline numbers becoming the primary's): `test_regime_comparison_stock_gains[baseline]` fails (`assert -0.503 > -0.3`). Restored.
2. Perturbed the committed baseline CSV in a working copy (large-wheel settling and slew times divided by 5): both `test_regime_comparison_stock_gains[baseline]` and `[headroom]` fail (`assert -0.706 > -0.3`, `-0.761 > -0.3`). Restored by `git checkout`.
3. Utilisation derivation (`peak / (2 * cap)`): 3 failed (`test_momentum_utilisation_matches_the_momentum_flag[headroom]`, `[gains_headroom]`, `test_wheel_capacities_and_momentum_utilisation`), 70 passed. Restored.
4. Gain-box coupling (fourth-pass trial, code unchanged since): `aggressive` mapped to `designSpace` fails `test_aggressive_gain_box_is_read_from_the_model` and the aggressive reproducibility test.

Observation (wording-level, G-B): Amendment 6 says the baseline tests "assert the recorded baseline numbers within stated tolerances"; the regime test asserts one-sided thresholds (associations above -0.30, mass weight below 0.05 or 0.10, bootstrap support below 0.10, near-frontier small above medium and large at most 5, pointing-mass at most -0.30) that the recorded numbers satisfy with margin, not the numbers within a tolerance band. A drift of the baseline from -0.13 to -0.25 would pass. The tests do detect a regime flip (trials 1 and 2).

## Probe note checks

- **Miss list complete?** Compared with the predictions written in `75823dc` (momentum violations, 1 degree slew times, feasible share, settling class ratio, effort and pointing dominating, lever iii outcome, associations, lever ii alone failing, R-14 clause 1 at risk): every miss is now recorded, with one exception (G-A below, wording-level): `75823dc` predicted "more torque saturation for every class ... large wheels saturate far more than at baseline" and that the small/large saturation ratio "may shrink"; observed, large-wheel median saturated fraction goes from 0.008 to 0.012 (barely) and the ratio rises from 5.12 to 13.1. The "R-14 clause 1 holds" line under "held" covers the pass but not that the shrink and large-wheel predictions were wrong. A second small omission: the predicted small/large 1 degree slew-time ratio of about 3 (observed 33/14 = 2.4) is only implicit in the slew-time miss.
- **Conditional on the stiff-loop regime:** yes ("Conditions of the finding": the wheel-class tension appears only when the loop is driven hard enough for the wheel to be the bottleneck; at the stock gains a feasibility boundary only; a third of the designs underdamped, 4.7 % below 0.5, 37 % of small-wheel designs fail momentum).
- **Thin margins disclosed:** yes (pointing-effort -0.35 against -0.30; settling-pointing +0.15 against 0.0; large-wheel near-frontier 6 to 7 rows; lever iii small wheels 0 rows). My robustness rerun across tau 25 to 60 is in the fourth-pass probe and the code is unchanged; settling-mass at tau 50 was -0.30 (edge).
- **"Two regimes" table matches the numbers:** yes (above).
- **Stale statements:** the amendment 5 result disposition was updated (xfail sentence superseded, pointer to the regime test). Remaining stale text (wording-level, G-C): the section "Status against R-14 (amended)" opens "Status after amendment 4 (final) ... on the committed dataset" and "Facts for WP7 interpretation" opens "Final (amendment 4) ... (d) R-13 (a), (b), (c) fail", and "committed dataset" in those sections means the baseline, whereas Amendment 6 makes the gains CSV primary. They are chronologically labelled but still say "final". The scope-of-work status line still reads "DRAFT (draft 4)" and its good-enough text says "the committed dataset" (Amendment 6 clarifies the meaning; the header was never refreshed).
- **Follow-up item present:** yes. `WP4b-decisions.md`: round-4 disposition (G-5 to follow-up) and a "Follow-up candidates" section ("Generator nondeterminism (review G-5)": run-to-run nondeterminism of the generator on identical code, likely adaptive-step integration sensitivity, CI differed 3.8 % then 6.2 % on the saturated fraction; the 10 % tolerance and rtol 1e-3 are a stopgap; to be replaced by a fixed-step or tighter-tolerance integration or a documented cause), plus unused levers (peak slew rate, wheel mass scaled with capacity, a milder gain box, the headroom difference). **Recorded here as well:** investigate the generator's run-to-run nondeterminism; the 10 % saturated-fraction tolerance is a stopgap; not part of WP4b.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-8 exist | met | See Deliverables. |
| R-1 to R-20 pass as checked | met | R-13 and R-14 met on the primary dataset; baseline recorded as the regime finding. |
| R-13 and R-14 hold on the committed (primary) dataset | met | Own probe. |
| Non-goals untouched | met | See below. |

## Outside the scope

- **Out-of-scope changes:** none by WP4b since the fourth pass. `git diff 2258281..HEAD --stat` lists only the probe note, `tests/test_adcs_enrichment.py`, `work-packages/{README,WP4b-decisions,WP4b-scope-of-work,WP8-scope-of-work}.md` (WP8 and README are status-table edits made by the supervisor's workflow, not WP4b deliverables). Over the whole range from `5dfbc8c~1`, `src/`, `docs/api.md`, `docs/method.md`, `tests/test_docs.py` and similar belong to WP3 and WP6 commits (checked with `git log` per path); `.github/workflows/test.yml` is a 12-line CI change in `379dee0` (recorded in earlier reviews, R-19 allowance); `CLAUDE.md` and the spec title are the repository-rename edit `a469aa2`.
- **Non-goals touched:** none. `adcs_sim.py` byte-identical; no estimator, solver, coordinates, WP2/WP3 or notebook change by WP4b; no `sysml-toolkit` dependency; WP4 CSV, tests and design space untouched; both cubesat CSVs untouched since their generating commits.

## Observations (not counted as failures)

- G-A, G-B, G-C above are wording-level; none changes a verdict. No substantive new finding.
- The package's primary-case result rests on a deliberately stiff regime (see conditions); this is disclosed and carried into the finding text.
- The full suite shows one non-WP4b xfail (WP3 scikit-learn).
- Previously dispositioned (fourth pass round, recorded in `WP4b-decisions.md`): G-1 standing dataset "Both, as two regimes" (applied by Amendment 6, verified); G-3 thin margins, G-4 conditional regime, G-7 WP7 consequences, G-8 small items: accept as is (the finding is stated as conditional on the stiff-loop regime, verified present); G-6 prediction-miss list: fix before acceptance (done in `5c252f7`, verified with the one small residual G-A); G-5 reproducibility tolerance: follow-up (recorded, verified); G-2 (baseline stands): moot, Amendment 6. Earlier rounds: first-round G-1, G-3, G-4, rest of G-5 accept as is, stale help text fixed; G-2 momentum "Enforce as feasibility"; "Reopen levers for a physically consistent scenario"; "One physics-justified lever: slew-time attribute"; "try both new levers then report back".

## Open decisions (for the supervisor)

- **G-A.** Miss list residual: the lever (i) predictions "large wheels saturate far more" and "small/large saturation ratio may shrink" (observed: large 0.008 to 0.012, ratio 5.1 to 13.1) and the small/large slew-time ratio (about 3 predicted, 2.4 observed) are not listed as misses. Wording-level. — options: accept as is / fix before acceptance / follow-up work package
- **G-B.** Regime-comparison assertions are one-sided thresholds rather than recorded numbers within tolerance bands (Amendment 6 wording). Wording-level. — options: accept as is / fix before acceptance / follow-up work package
- **G-C.** Stale "final (amendment 4)" and "committed dataset" labels in two probe-note sections and the scope status line "DRAFT (draft 4)". Wording-level. — options: accept as is / fix before acceptance / follow-up work package

Proposed as one item per the decision loop (none affects a good-enough item or a non-goal): "accept G-A, G-B, G-C as is, or pick any to act on".

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-A | pending | |
| G-B | pending | |
| G-C | pending | |
| Previously dispositioned (see Observations) | as recorded | accept as is / fixed / follow-up as quoted in `WP4b-decisions.md` |
| Follow-up: generator nondeterminism, 10 % tolerance stopgap | follow-up work package (recorded) | `WP4b-decisions.md`, "Follow-up candidates"; not part of WP4b |

## Recommendation

**Recommend acceptance with the listed gaps noted.** Against the amended scope every deliverable and requirement is met: R-13 (a to e), R-14 and R-15 hold on the primary aggressive-gain dataset and my independent probe reproduces the note's numbers (contending set, mass 0.223 with bootstrap support 1.00, settling-mass about -0.5, feasible 706 = 191/248/267); the baseline's null result is asserted by non-vacuous regime-comparison tests (trials fail as they should) and recorded as a finding; the full suite is 882 passed with no WP4b xfail, ruff, format and lock are clean, CI is green on the last seven runs, `adcs_sim.py`, the WP4 tests and both cubesat CSVs are untouched, authorship and attribution are clean, and the follow-up item is recorded. The three new gaps are wording-level and are pending the supervisor's one-item disposition; the finding is correctly stated as conditional on the stiff-loop regime with thin margins disclosed.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
