# WP7 — Scope of work: ADCS case notebook

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP7-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP7-decisions.md`, after the review report `work-packages/WP7-review.md` |

## Purpose

The notebook is the embodied demonstration of the method (spec §8, `docs/superpowers/notes/presentation-framing.md`): a
reader follows a real trade study from the dataset to the learned trade space, sees what the fit says contends, reads
the figures, and does the human validation that the tests cannot do. Per the supervisor's requirement on the case
(spec §8), the fitted model must expose tensions that were not asserted a priori and that are recognizable and
intuitive once explained; the notebook never asserts a trilemma, it reports what the fit found and then explains it.
An early probe of the dataset (`docs/superpowers/notes/adcs-tensions-probe.md`) found three recognizable tensions
and one alignment, and did not expose the agility-versus-mass story through wheel class; OD1 below asks how to
proceed.

## Goals

- G1. An executed, committed Jupyter notebook `examples/adcs/adcs_trade_study.ipynb`, organized by pipeline stage, that reads only the cached dataset and runs end to end with the accepted toolkit (WP2, WP3, WP4).
- G2. The conditioning stage is shown and diagnosed: covariates encoded with explicit category orders, the four attributes conditioned by `LogAffinePreconditioner(orientation=[-1]*4)`, with diagnostics and a sensitivity check on the reference point.
- G3. The fit, its diagnostics, the temperature selection and a τ sweep are shown, with the figures of the frontier (3-D surface for settling, pointing, mass; full d = 4 fit; log-space plane; frontier coordinates with holes and white-space targets).
- G4. The case requirement: the tension report exposes a contending set of size at least 2 that was not asserted, with pairwise tension and alignment and principal tension directions, and each exposed tension is explained in physical terms in the interpretation.
- G5. Use of the analysis tools on the case: V by wheel class, star-tracker grade and gains; per-category refits; three hand-written candidate designs scored (novelty, improvement factors); the frontier pulled back to attribute units.
- G6. Propose, predict, then check: `TradeSpaceRegressor` predicts where three proposed configurations would fall, the simulator evaluates them (cached), and predicted versus measured log V and Z are compared against the band 1/τ.
- G7. The notebook frames its own epistemics: machine verification (tests, lemmas) versus human validation (reading figures, explaining tensions), and states the limits of the case (stratified mass, censored settling time, illustrative hardware, dependence on conditioning).

## Non-goals

- No change to the toolkit (WP1, WP2, WP3), to the simulator or dataset (WP4), or to the documentation pages (WP6, WP8); defects found there are reported as amendments or follow-up work.
- No case enrichment in this package: enriching the dataset, if decided (OD1), is a separate amendment of WP4 or a new package that is accepted before WP7 executes.
- No claim that a trilemma or any named n-lemma exists before the fit reports it; no preference or recommendation among designs (novelty is not preference).
- No site, MkDocs or CI publishing work (WP8); no re-execution of the notebook in CI.
- No new dependencies beyond the existing `notebooks` dependency group.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `examples/adcs/adcs_trade_study.ipynb`, executed, with outputs and embedded figures | G1–G7 |
| D-2 | `examples/adcs/figures/*.png`: static copies of the notebook's figures | G3, G4 |
| D-3 | `examples/adcs/data/check_designs.csv`: the cached simulator results for the three proposed configurations (and the three hand-written candidates if simulated) | G5, G6 |
| D-4 | `docs/superpowers/notes/adcs-tensions-probe.md`, updated with the probe rerun on the WP3 tension report and the gate decision (step 0 of execution) | G4 |
| D-5 | `tests/test_notebook.py`: reads the executed notebook JSON and checks structure and outputs | G1, G4–G7 |
| D-6 | `work-packages/WP7-decisions.md` (approval record) | G1–G7 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `uv run jupyter nbconvert --execute --to notebook` on the notebook (with the `notebooks` group installed) completes without error from a clean clone, reading only `examples/adcs/data/adcs_designs.csv` and `check_designs.csv` and no simulator run beyond the three cached check designs | reviewer runs the command in a fresh clone |
| R-2 | The committed notebook is executed: every code cell has outputs, no cell has an error output, and the figures are embedded; static PNG copies exist in `examples/adcs/figures/` | `uv run pytest tests/test_notebook.py`; inspection |
| R-3 | Sections follow the stages in order: load and filter feasible designs; conditioning (`ColumnTransformer` with `OrdinalEncoder` on explicit category orders for covariates, `LogAffinePreconditioner(orientation=[-1]*4)` for the four attributes) and its diagnostics; temperature selection, fit, diagnostics table, τ sweep; frontier figures; frontier coordinates, holes and white-space targets; tensions; V by category and per-category refits; candidates; pull-back; propose-predict-check; validation and limits | `test_notebook.py` (section headings present in order); inspection |
| R-4 | Conditioning diagnostics show unit log-spread of each metric and the fraction of rows used; a sensitivity check refits with at least two alternative reference points (for example standardizing by robust statistics, or shifting the reference by a stated multiple of the log-spread) and reports whether the contending set and the dominant tensions persist | inspection of the executed outputs |
| R-5 | `select_temperature` hits the target `frac_above_` within its tolerance; the diagnostics table shows `exponents_`, `n_eff_`, `frac_above_`, τ and the objective; the τ sweep shows `frac_above_` monotone nonincreasing from about 0.5 toward 0 and `n_eff_` from N toward d | `test_notebook.py` parses the table output; inspection of the sweep |
| R-6 | Figures: the V = 1 surface in (settling, pointing, mass) hugging the upper envelope of the designs, the full d = 4 fit, the log-space plane, frontier coordinates colored by a covariate with holes and white-space targets marked; each figure has titles and axis labels in original-attribute terms where meaningful | inspection of figures and PNGs |
| R-7 | The notebook reports the tension report for the fitted trade space: the contending set at τ = ∞ with its size, the working-τ exponents, the pairwise association of log-metrics among near-frontier designs, and the principal tension directions with loadings; the contending set has size at least 2 and is reported by the fit, not asserted: no markdown or code cell names a dilemma, trilemma or n-lemma, or a particular tension, before the report output that shows it | `test_notebook.py` (the report output has `n_lemma >= 2`; no cell before the report cell contains the words dilemma, trilemma, n-lemma or the names of tensions the report is to expose); inspection |
| R-8 | Every tension and every alignment that the report exposes is explained in physical terms in the interpretation (the mechanism, the design variable through which it acts, and a statement of what would change it), the explanation follows the report output, and tensions the report does not expose are not claimed | inspection by the reviewer against the executed outputs |
| R-9 | Tools applied on the case: V by wheel class, star-tracker grade, Kp and Kd; per-category refits with the contending sets compared; three hand-written candidates with measured attributes scored (novelty V − 1, calibrated novelty, improvement factors); the frontier pulled back to attribute units and checked against the pipeline's `score_samples` | `test_notebook.py` for presence of outputs; inspection |
| R-10 | Propose-predict-check: `TradeSpaceRegressor` is fitted on (Kp, Kd, wheel class, ST grade) → coordinates; predictions for three proposed configurations are recorded before the check simulations; the cached simulator results (`check_designs.csv`) are compared with the predictions for log V and Z against the band 1/τ, and the comparison is reported whether or not it is within the band | `test_notebook.py` (comparison table present; `check_designs.csv` has three rows); inspection of the order of cells |
| R-11 | The notebook states explicitly: mass is stratified by hardware (nine discrete values) so gaps between strata are structural; settling time is quantized by the step size and censored at `t_end` (the `settled` flag is used); momentum is observed, not enforced (a flag); hardware values are illustrative; the near-frontier sample sizes behind each association | `test_notebook.py` (key phrases present in markdown cells); inspection |
| R-12 | A final section separates what the machine verified (tests, WP1 lemmas, with pointers) from what the human validates (reading the tensions, judging explanations, holes as opportunities or structure), and lists the conditions of the theory that the case touches (ledger R1, the conditioning choice) with their failure modes | inspection |
| R-13 | Step 0 gate: before the notebook is written, the probe is rerun with the WP3 tension report on the final conditioning and recorded in `docs/superpowers/notes/adcs-tensions-probe.md`; if the report shows a contending set of size < 2 or no tension that can be explained physically, execution stops and the driver is told (problem-level) | note updated; commit history shows the note before the notebook |
| R-14 | Suite, linters and lock pass and nothing outside scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff --stat` shows only `examples/adcs/` (notebook, figures, check data), `docs/superpowers/notes/adcs-tensions-probe.md`, `tests/test_notebook.py` and `work-packages/` | run the commands; inspect the diff |
| R-15 | No AI attribution lines; commits authored as Michael Zargham; CI green on every push; the notebook JSON contains no machine-specific paths or credentials | `git log` grep returns 0; `gh run list`; grep of the notebook |

## Definition of good

- A reader meets the case in the order the method does (embodied hook first, then small visible steps), and the figures tell the story without the text.
- The tensions that the fit exposes feel inevitable once explained: the explanations are mechanism-level and tied to design variables, and the notebook shows what happens to them under the sensitivity check.
- Honest about what the data cannot support: small near-frontier samples, hardware strata, dependence on conditioning, and any tension the case does not exhibit.
- Propose-predict-check is a real test: predictions are fixed before the check, and a miss is reported and discussed rather than hidden.
- The notebook reads like the supervisor's SciPy paper prescribes: a consistent visual vocabulary (that of the plotting module), notation quickstart in the body, credit to sources.

## Definition of good enough

- Deliverables D-1 to D-6 exist at the stated paths.
- R-1 to R-15 pass as checked, with evidence in the review report.
- The tension report shows a contending set of size at least 2 that was not asserted, and every tension and alignment it exposes is explained physically (R-7, R-8).
- Non-goals untouched (no toolkit, dataset or documentation changes; no enrichment inside this package).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item. Execution waits for the acceptance of WP3 (and, per OD1, for any enrichment).

- Notebook authored with `nbformat` from a script kept out of the repository (the notebook is the artifact), executed with `jupyter nbconvert --execute --to notebook --inplace`, kernel `python3` of the project environment *(default)*.
- Covariate encoding *(default)*: `OrdinalEncoder` with explicit category orders (wheel class small < medium < large; star-tracker grade coarse < medium < fine) for the covariates, passed through next to the metrics; the four attributes go to `LogAffinePreconditioner(orientation=[-1]*4)`, `scaler="standard"`, then to `HyperbolicTradeSpace`, as one `ColumnTransformer` + `Pipeline`.
- Feasible filter *(default)*: keep `settled` designs for the fit (the censored settling time is not a measurement); report the number removed and the `momentum_ok` violations separately; the notebook says that violations are concentrated in the small wheel class and are not filtered unless stated.
- Temperature *(default)*: `select_temperature(target_frac_above=0.10)`; τ sweep over a log grid of 12 values in (1, 1e3) plus τ = ∞.
- Sensitivity check *(default)*: three conditionings (standardize; robust scaler; standardize with the reference shifted by +0.5 log-spread on all metrics); report the contending set, the dominant exponent and the first tension direction for each.
- Figures *(default)*: matplotlib via the plotting module; 3-D surface for (settling, pointing, mass) with the full d = 4 fit shown as projections; one qualitative palette for categories; PNG at 150 dpi.
- Candidates and proposals *(default)*: three hand-written candidate designs chosen to span the trade space (a fast and expensive-effort design, a precise and heavy design, a light and slow design) with measured attributes by running the simulator once (cached in `check_designs.csv` with the three proposals, 6 rows, column `role` = candidate or proposal); proposals are chosen from the regressor's predicted white-space targets or hole locations and fixed before simulation.
- Regressor *(default)*: `TradeSpaceRegressor(RandomForestRegressor(random_state=0), HyperbolicTradeSpace(...))` or a Gaussian-process regressor if `predict_std` is shown; the choice is stated in the notebook.
- `tests/test_notebook.py` *(default)*: uses only `json` and `re` on the committed notebook; no execution; skipped never; checks section headings in order, no error outputs, the tension report output has `n_lemma >= 2`, ordering constraint of R-7, key phrases of R-11, the comparison table of R-10, and that PNG files exist.
- Step 0 probe *(default)*: reproduce the probe with `tension_report` on the final conditioning (settled rows, standardized reciprocals), append the result to the probe note, and apply the R-13 gate.
- Number of near-frontier rows is displayed next to every association and direction *(default)*.
- Prose *(default)*: discursive, no emojis, defines each term once, cites lemma tags and WP5 keys where used; the interpretation sections are written after the corresponding outputs are known and are marked as the author's interpretation (human validation).
- Commits prefixed "WP7: "; probe note, check data, notebook, figures, test, then status table and decisions file; every push green and attribution-free *(default)*.

## Open decisions (for the supervisor)

- **OD1.** The probe (`docs/superpowers/notes/adcs-tensions-probe.md`) shows the current dataset exposes three recognizable, unasserted tensions (settling vs effort, pointing vs effort, pointing vs mass through star-tracker grade) and one alignment (settling with pointing), but not the agility-vs-mass story through wheel class (mass is nearly inert in the contending set; torque limits rarely bind). Should the case be enriched before WP7 executes, or should WP7 proceed with the current dataset? — options: (a) proceed with the current dataset and have the notebook report that wheel class does not appear as a tension in these data / (b) enrich the case first by amending WP4 (wider hardware spread, a scenario in which small wheels saturate, and/or an additional cost-like attribute such as power or sensor cost, labelled illustrative) / (c) enrich the case first as a new package WP4b, scoped and accepted separately.
