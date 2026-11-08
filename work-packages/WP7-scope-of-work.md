# WP7 — Scope of work: ADCS case notebook (draft 3, two regimes of the SysML-modelled cubesat)

| | |
|---|---|
| **Status** | DRAFT (draft 3). Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP7-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP7-decisions.md`, after the review report `work-packages/WP7-review.md` |

## Purpose

The notebook is the embodied demonstration of the method (spec §8, `docs/superpowers/notes/presentation-framing.md`): a reader follows a real trade study from the dataset to the learned trade space, sees what the fit says contends, reads the figures, and does the human validation that the tests cannot do. Per the supervisor's requirement on the case (spec §8), the fitted model must expose tensions that were not asserted a priori and that are recognizable and intuitive once explained; the notebook never asserts a trilemma, it reports what the fit found and then explains it.

The case is the SysML-modelled cubesat of WP4b (`examples/adcs/cubesat_tradespace.sysml`), studied in two regimes of the controller gains, both at the momentum-consistent 30° scenario, 600 s horizon, seed 0, with ten attributes (supervisor: "Both, as two regimes", recorded in `WP4b-decisions.md`):

- the **primary dataset** `examples/adcs/data/adcs_designs_cubesat_gains.csv`, an aggressive-gain box (Kp 0.2 to 2.0, Kd 0.3 to 1.5; median Kd/Kp 1.06), in which the loop is driven hard enough for the wheel to be the bottleneck; 706 of 1000 designs are feasible (small 191, medium 248, large 267); the contending set at τ = ∞ has size 6 (slew time 0.201, total mass 0.223, energy balance 0.169, control effort 0.143, pointing 0.135, depth of discharge 0.129) and the settling–mass and slew-time–mass associations are about −0.5 and −0.45;
- the **regime comparison** `examples/adcs/data/adcs_designs_cubesat.csv`, the stock-gain box (median Kd/Kp 3.9), in which the 1 % settling time and the slew time are set by the slow pole of the PD loop; 780 of 1000 designs are feasible, the contending set has size 6 without total mass, and the agility–mass association is about −0.1.

The notebook's reading of wheel class is therefore: both a feasibility boundary and a frontier tension when the wheel is the bottleneck (the aggressive regime); a feasibility boundary only in the baseline regime. The shape of the trade space is conditional on the operating regime, and the notebook says so. In the primary dataset 37 % of small-wheel designs fail momentum, a third of the designs are underdamped (4.7 % with damping ratio below 0.5), large wheels contribute only 7 near-frontier designs, and two margins are thin (pointing–effort about −0.35 against a −0.30 threshold, settling–pointing about +0.14); these are disclosed in the notebook. Execution waits for WP4b's acceptance.

## Goals

- G1. An executed, committed Jupyter notebook `examples/adcs/adcs_trade_study.ipynb`, organized by pipeline stage, that reads only the cached datasets and runs end to end with the accepted toolkit (WP2, WP3, WP4b).
- G2. The conditioning stage is shown and diagnosed on the ten attributes with mixed orientations, and a sensitivity check on the reference point and on the redundant attributes is reported.
- G3. The fit, its diagnostics, the temperature selection and a τ sweep are shown, with figures of the frontier at readable dimension (chosen three-metric subsets for the 3-D surfaces, the full fit's log-plane projections, frontier coordinates with holes and white-space targets from subset refits).
- G4. The case requirement: the tension report (not a hand probe) exposes a contending set of size at least 2 that was not asserted, with the pairwise tension and alignment and the principal tension directions, and each exposed tension is explained physically; near-redundant attributes are reported as aligned, not as independent tensions.
- G5. The two-regime result of WP4b is reported and explained: on the primary dataset wheel class is both a feasibility boundary (momentum) and a frontier tension (agility against mass); in the baseline regime it is a feasibility boundary only; the notebook shows the regime comparison and says the shape of the trade space depends on the operating regime.
- G6. The analysis tools applied to the case: V by wheel class, star-tracker grade, panel span, battery capacity and gains; per-category refits; three hand-written candidates scored; the frontier pulled back to attribute units.
- G7. Propose, predict, then check: `TradeSpaceRegressor` predicts where three proposed configurations would fall, the simulator evaluates them (cached), and predicted versus measured log V and Z are compared against the band 1/τ.
- G8. The notebook frames its own epistemics: machine verification (tests, lemmas) versus human validation, and states the limits of the case (stratified hardware, censored times, illustrative values, dependence on conditioning, small near-frontier samples, power never limiting a slew).

## Non-goals

- No change to the toolkit (WP1, WP2, WP3), to the simulator, model or dataset (WP4, WP4b), or to the documentation pages (WP6, WP8); defects found there are reported as amendments or follow-up work.
- No new simulation of the dataset; only the three proposed configurations (and the three hand-written candidates) are simulated once and cached.
- No claim that a trilemma or any named n-lemma exists before the fit reports it; no claim of an agility-against-mass tension before the report shows it, and none for the baseline regime; no preference or recommendation among designs (novelty is not preference).
- No site, MkDocs or CI publishing work (WP8); no re-execution of the notebook in CI.
- No new dependencies beyond the existing `notebooks` dependency group.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `examples/adcs/adcs_trade_study.ipynb`, executed, with outputs and embedded figures | G1–G8 |
| D-2 | `examples/adcs/figures/*.png`: static copies of the notebook's figures | G3, G4 |
| D-3 | `examples/adcs/data/check_designs_cubesat.csv`: cached simulator results for the three hand-written candidates and the three proposed configurations (column `role`) | G6, G7 |
| D-4 | `docs/superpowers/notes/adcs-tensions-probe.md`: updated with the rerun of the probe by the WP3 tension report (step 0) | G4 |
| D-5 | `tests/test_notebook.py`: reads the executed notebook JSON and checks structure and outputs | G1, G4–G8 |
| D-6 | `work-packages/WP7-decisions.md` (approval record) | G1–G8 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `uv run jupyter nbconvert --execute --to notebook` on the notebook (with the `notebooks` group installed) completes without error from a clean clone, reading only `adcs_designs_cubesat_gains.csv`, `adcs_designs_cubesat.csv` (the regime comparison) and `check_designs_cubesat.csv`, with no opensysml runtime needed and no simulation | reviewer runs the command in a fresh clone |
| R-2 | The committed notebook is executed: every code cell has outputs, no cell has an error output, figures are embedded; static PNG copies exist in `examples/adcs/figures/` | `uv run pytest tests/test_notebook.py`; inspection |
| R-3 | Sections follow the stages in order: load the primary dataset and define the feasible set (settled ∧ power_ok ∧ momentum_ok; 706 of 1000; `dod_ok` is reported but is not a filter because the depth of discharge is a metric); conditioning (`ColumnTransformer` with `OrdinalEncoder` on explicit category orders for the covariates, `LogAffinePreconditioner` with per-attribute orientation for the ten attributes) and its diagnostics; temperature selection, fit, diagnostics table, τ sweep; frontier figures; frontier coordinates, holes and white-space targets; tensions; V by category and per-category refits; candidates; pull-back; propose-predict-check; the regime comparison with the baseline dataset; validation and limits | `test_notebook.py` (section headings in order); inspection |
| R-4 | Conditioning uses the orientations of the probe (reciprocal for settling, slew time, pointing, mass, effort, peak slew power and depth of discharge; direct for power margin, energy balance and eclipse reserve), shows unit log-spread of each metric, and reports the number of rows removed by each feasibility condition; a sensitivity check refits with at least two alternatives (the robust scaler; the reference shifted by a stated multiple of the log-spread; and a refit dropping one of each near-redundant pair) and reports whether the contending set and the dominant tensions persist | inspection of the executed outputs |
| R-5 | `select_temperature` hits the target `frac_above_` within its tolerance, using bounds that stay at τ ≥ 3 (the documented useful range); the diagnostics table shows `exponents_`, `n_eff_`, `frac_above_`, τ and the objective; the τ sweep is drawn over the useful range, with the small-τ non-monotone region described | `test_notebook.py` parses the table output; inspection |
| R-6 | Figures: the V = 1 surface for two chosen three-metric subsets (default: slew time, pointing error, control effort; and total mass, eclipse reserve, power margin) from subset refits, each hugging the upper envelope of the designs; log-plane projections of the full fit; frontier coordinates colored by a covariate with holes and white-space targets marked (from a subset refit with at most four metrics, since hole finding supports up to three chart coordinates); titles and axis labels in original-attribute terms | inspection of figures and PNGs |
| R-7 | The notebook reports the tension report (`tension_report`) for the fitted trade space: the contending set at τ = ∞ with its size, the working-τ exponents, the pairwise association among near-frontier designs and the principal tension directions with loadings, with the number of near-frontier designs shown; the contending set has size at least 2 and is reported by the fit, not asserted: no markdown or code cell names a dilemma, trilemma or n-lemma, or a particular tension, before the report output that shows it | `test_notebook.py` (the report output has `n_lemma >= 2`; no cell before the report cell contains the words dilemma, trilemma, n-lemma or the names of the exposed tensions); inspection |
| R-8 | Every tension and alignment that the report exposes is explained in physical terms in the interpretation (the mechanism, the design variable through which it acts, and what would change it), after the report output; the near-redundant pairs (settling and slew time; power margin and energy balance; eclipse reserve and depth of discharge) are reported as aligned (accounting near-identities), not as separate findings; the thin margins of the primary result (pointing–effort, settling–pointing) are disclosed; tensions the report does not expose are not claimed | inspection by the reviewer against the executed outputs |
| R-9 | The two-regime result is reported: on the primary dataset the notebook shows per-wheel-class feasibility (momentum) and states that wheel class is both a feasibility boundary and a frontier tension (total mass in the contending set; settling–mass and slew-time–mass associations at most −0.30), with the near-frontier counts per class (small, medium, large) and the observation that large wheels contribute only a few near-frontier designs; a regime-comparison section runs the same conditioning and tension report on the baseline dataset and states that there total mass is absent from the contending set and wheel class is a feasibility boundary only; the interpretation says that the shape of the trade space depends on the operating regime (Kd/Kp, the slow pole) | `test_notebook.py` (key phrases present; the primary report output has total mass in the contending set; the baseline report output has it absent); inspection |
| R-10 | Tools applied on the case: V by wheel class, star-tracker grade, panel span, battery capacity, Kp and Kd; per-category refits with the contending sets compared; three hand-written candidates with measured attributes scored (novelty V − 1, calibrated novelty, improvement factors); the frontier pulled back to attribute units and checked against the pipeline's `score_samples` | `test_notebook.py` for presence of outputs; inspection |
| R-11 | Propose-predict-check: `TradeSpaceRegressor` is fitted on the configuration (panel span, battery capacity, wheel class, star-tracker grade, Kp, Kd) → coordinates; predictions for three proposed configurations are recorded before the check simulations; the cached results are compared with the predictions for log V and Z against the band 1/τ, and the comparison is reported whether or not it is within the band | `test_notebook.py` (comparison table present; `check_designs_cubesat.csv` has six rows with roles); inspection of the order of cells |
| R-12 | The notebook states explicitly: hardware is stratified (wheel classes, tracker grades, discrete masses) so gaps between strata are structural; the aggressive-gain regime is a stiff-loop regime (a third of the designs underdamped, 4.7 % with damping ratio below 0.5) chosen so that the wheel is the bottleneck, and 37 % of its small-wheel designs fail momentum; slew and settling times are censored at the horizon (the `settled` flag is used); momentum is enforced as feasibility; hardware values are illustrative; power never limits a slew in this dataset (torque capped by power in about 3 % of baseline designs, all with large wheels; power reaches the controls through mass and inertia; the corresponding share for the primary dataset is read from the data and reported); near-frontier sample sizes accompany every association | `test_notebook.py` (key phrases present); inspection |
| R-13 | A final section separates what the machine verified (tests, WP1 lemmas, with pointers) from what the human validates (reading the tensions, judging the explanations, holes as opportunities or structure), and lists the conditions of the theory that the case touches (ledger R1, A4, the conditioning choice and the operating regime) with their failure modes | inspection |
| R-14 | Step 0 gate: before the notebook is written, the probe is rerun with the WP3 tension report on the final conditioning and recorded in `docs/superpowers/notes/adcs-tensions-probe.md`; if the report shows a contending set of size < 2 or no tension that can be explained physically, execution stops and the driver is told | note updated; commit history shows the note before the notebook |
| R-15 | Suite, linters and lock pass and nothing outside scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff --stat` shows only `examples/adcs/` (notebook, figures, check data), the probe note, `tests/test_notebook.py` and `work-packages/` | run the commands; inspect the diff |
| R-16 | No AI attribution lines; commits authored as Michael Zargham; CI green on every push; the notebook JSON contains no machine-specific paths or credentials | `git log` grep returns 0; `gh run list`; grep of the notebook |

## Definition of good

- A reader meets the case in the order the method does (embodied hook first, then small visible steps), and the figures tell the story without the text.
- The tensions that the fit exposes feel inevitable once explained: the explanations are mechanism-level and tied to design variables, and the notebook shows what happens to them under the sensitivity checks.
- The notebook is honest about what the case does not show: no agility-against-mass tension, wheel class as a feasibility boundary, near-redundant attributes, small near-frontier samples, hardware strata, dependence on conditioning.
- Propose-predict-check is a real test: predictions are fixed before the check, and a miss is reported and discussed rather than hidden.
- The notebook reads as the SciPy paper prescribes: a consistent visual vocabulary (that of the plotting module), a notation quickstart in the body, credit to sources.

## Definition of good enough

- Deliverables D-1 to D-6 exist at the stated paths.
- R-1 to R-16 pass as checked, with evidence in the review report.
- The tension report shows a contending set of size at least 2 that was not asserted, every tension and alignment it exposes is explained physically, and the WP4b finding is reported (R-7 to R-9).
- Non-goals untouched (no toolkit, dataset or documentation changes).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item. Execution waits for the acceptance of WP4b.

- Notebook authored with `nbformat` from a script kept out of the repository (the notebook is the artifact), executed with `jupyter nbconvert --execute --to notebook --inplace`, kernel `python3` of the project environment *(default)*.
- Attributes and feasible set *(default)*: the ten attributes of the dataset (`settling_time_s`, `slew_time_s`, `pointing_error_deg`, `total_mass_kg`, `control_effort`, `power_margin_w`, `energy_balance_wh`, `eclipse_reserve_wh`, `peak_slew_power_w`, `dod_eclipse`); the extra column `slew_time_05deg_s` and `peak_momentum_nms` are not metrics; feasible = settled ∧ power_ok ∧ momentum_ok (706 of 1000 designs in the primary dataset, 780 in the baseline); `dod_ok` is reported, not a filter (a violated `dod_ok` coincides with a non-positive eclipse reserve, so those designs are excluded for that reason).
- Covariate encoding *(default)*: `OrdinalEncoder` with explicit category orders (wheel small < medium < large; tracker coarse < medium < fine) for the covariates, passed through next to the metrics together with the continuous design variables (panel span, battery capacity, Kp, Kd); the ten attributes go through `LogAffinePreconditioner` with a per-column orientation list and `scaler="standard"`, then `HyperbolicTradeSpace`, as one `ColumnTransformer` + `Pipeline`.
- Temperature *(default)*: `select_temperature(target_frac_above=0.10, bounds=(3, 1e3))`; τ sweep over a log grid of 12 values in (3, 1e3) plus τ = ∞.
- Figures *(default)*: matplotlib via the plotting module; 3-D surfaces from refits on the chosen three-metric subsets; PNG at 150 dpi; one qualitative palette for categories.
- Hole finding and targets *(default)*: from a refit on four metrics (slew time, pointing error, control effort, total mass) so that the chart has three coordinates; the notebook says it is a subset view.
- Tension report *(default)*: `tension_report(est, X, band=None)` on the full ten-attribute fit and, for comparison, on the four-metric subset; association Pearson with Spearman shown once as a check; the number of near-frontier designs per wheel class is printed next to it.
- Sensitivity check *(default)*: standardize (baseline); robust scaler; standardize with the reference shifted by +0.5 log-spread on all metrics; and a refit on the eight metrics left after dropping `slew_time_s` and `energy_balance_wh` (one of each near-redundant pair kept in turn as a check); report the contending set, the dominant exponent and the first tension direction for each.
- Regime comparison *(default)*: the same pipeline (conditioning, `select_temperature` at the same target, `tension_report`) is run on the baseline dataset and shown side by side with the primary one in a table (feasible counts, contending set with exponents, mass exponent, agility–mass associations, near-frontier counts per class, Kd/Kp medians), with the two-regimes table of the probe note as the reference; no further datasets are used.
- Candidates and proposals *(default)*: three hand-written candidate designs chosen to span the trade space (a fast, effort-hungry design; a precise, heavy-sensor design; a light, slow design) and three proposals chosen from the predicted white-space targets and fixed before simulation; configured inside the primary dataset's aggressive gain box and simulated once through `cubesat_model.measure` with the aggressive gain-box option (requires the opensysml runtime, run once outside the notebook by a script not kept in the repository, or kept in `examples/adcs/` if the reviewer asks) and cached in `check_designs_cubesat.csv` with a `role` column.
- Regressor *(default)*: trained on the primary dataset's feasible designs, `TradeSpaceRegressor(GaussianProcessRegressor(...), HyperbolicTradeSpace(...))` so `predict_std` can be shown, or a random forest if the Gaussian process does not fit in reasonable time; the choice is stated in the notebook; the trade space inside is fitted on the preconditioned metrics.
- `tests/test_notebook.py` *(default)*: uses only `json` and `re` on the committed notebook; no execution; checks section headings in order, no error outputs, the tension report output has `n_lemma >= 2`, the ordering constraint of R-7, key phrases of R-9 and R-12, the comparison table of R-11, and that the PNG files exist.
- Step 0 probe *(default)*: reproduce the probe with `tension_report` on the final conditioning (feasible rows, orientations as above) for both datasets and append the result to the probe note, applying the R-14 gate; the expected result is the one recorded in the note (primary: contending set of size 6 with total mass; baseline: size 6 without total mass).
- Prose *(default)*: discursive, no emojis, each term defined once, lemma tags and WP5 keys where used; the interpretation sections are written after the outputs are known and marked as the author's interpretation (human validation); the near-redundant pairs are explained as accounting identities (slew time is about 0.74 of settling time in the baseline regime; margin and balance; reserve and depth of discharge); the notebook discloses the underdamped share, the momentum failures of small wheels, the thin margins and the few large-wheel near-frontier designs of the primary dataset.
- Commits prefixed "WP7: "; probe note, check data, notebook, figures, test, then status table and decisions file; every push green and attribution-free *(default)*.

## Open decisions (for the supervisor)

None at problem level: spec §8, the supervisor's "Both, as two regimes" decision and the amendments recorded in `WP4b-decisions.md` answer them. The Agent's defaults list above is the one item for the supervisor to approve or change at the scope gate.
