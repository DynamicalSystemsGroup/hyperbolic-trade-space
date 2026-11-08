# WP4b — Scope of work: ADCS case enrichment

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP4b-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4b-decisions.md`, after the review report `work-packages/WP4b-review.md` |

## Purpose

The supervisor requires the example case to be rich enough that the fitted model exposes tensions that were not
asserted a priori and that are recognizable and intuitive once explained (spec §8). The probe of the accepted WP4
dataset (`docs/superpowers/notes/adcs-tensions-probe.md`) found settling vs effort, pointing vs effort and pointing
vs mass (through star-tracker grade), with settling and pointing aligned, but not agility vs mass through wheel
class: mass was nearly inert in the contending set (exponent 0.006 at τ = ∞), torque limits bound only about 7 % of the
time for small wheels and under 1 % for large wheels, and wheel class moved the median settling time only from 301 s to
264 s. The supervisor decided (WP7-decisions.md, "Enrich as a separate package WP4b") to enrich the case before the
notebook (WP7) is written. WP4b changes the scenario and design-space layer so that wheel class matters for agility,
regenerates the dataset, and shows by the probe, in the spec's terms, that the case now exposes the intended tensions
while keeping the three already exposed.

## Goals

- G1. A scenario and an illustrative wheel-class set in which torque limits bind, so that wheel class (torque, momentum capacity, mass) trades agility against mass.
- G2. An additive extension of the design-space and generator layers (new options, defaults unchanged) and a new committed, seed-stable dataset generated with the enriched scenario; the WP4 deliverables stay intact.
- G3. Tests that make the case's richness a checked property: the probe's acceptance conditions run as tests on the committed dataset.
- G4. The probe note records the diagnosis, every lever tried and the final result.

## Non-goals

- No change to the simulator port (`examples/adcs/adcs_sim.py`: physics, inertia, controller), its regression pins or its source-port tests.
- No change to the estimator, solvers, coordinates, the analysis toolkit (WP2, WP3) or the notebook (WP7).
- No rewrite or replacement of the WP4 deliverables: the original CSV, its tests and its generator behaviour under default options are unchanged.
- No calibration to real hardware: all new values are labelled illustrative.
- No choice of the "right" set of tensions: the acceptance check asks that the fit exposes contention that is recognizable, not that it matches a list fixed in advance for any metric beyond the conditions in R-7.
- No new dependencies.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `examples/adcs/design_space.py`: additive scenario options (slew angle, horizon) and an enriched wheel-class set; defaults reproduce the WP4 behaviour | G1, G2 |
| D-2 | `examples/adcs/generate_dataset.py`: additive flags selecting the scenario and the wheel set; default behaviour unchanged | G2 |
| D-3 | `examples/adcs/data/adcs_designs_enriched.csv`: committed dataset, seed 0, same columns as the original plus scenario columns | G2, G3 |
| D-4 | `tests/test_adcs_case.py` additions (scenario options, reproducibility of the enriched dataset) and `tests/test_adcs_enrichment.py` (the probe's acceptance conditions as tests) | G3 |
| D-5 | `docs/superpowers/notes/adcs-tensions-probe.md` updated: levers tried, final configuration, results | G4 |
| D-6 | `examples/adcs/extended_design_space.sysml` updated to describe the enriched wheel set and scenario (documentation only) | G1 |
| D-7 | `work-packages/WP4b-decisions.md` (approval record) | G1–G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `examples/adcs/adcs_sim.py` is byte-identical to its WP4 state, and every WP4 test (inertia, regression pins at 78.0, 87.4, 120.5 and 310.6 s, port and design-space tests) passes unchanged | `git diff <start>..HEAD -- examples/adcs/adcs_sim.py` empty; `uv run pytest tests/test_adcs_case.py` |
| R-2 | The design-space and generator extensions are additive: with default options `evaluate_design`, `sample_designs` and `generate_dataset.py` produce exactly the WP4 results, and the original `adcs_designs.csv` is unchanged | the existing WP4 reproducibility tests pass; `git diff` shows the original CSV untouched; a new test checks the defaults |
| R-3 | The enriched wheel set (default name `WHEEL_CLASSES_ENRICHED`) has small/medium/large with strictly increasing maxTorque, maxMomentum and mass, a wider maxTorque spread than the WP4 set (at least a factor 10 from small to large), values labelled illustrative in the docstring and the SysML text | inspection; test of ordering and spread |
| R-4 | In the enriched scenario torque limits bind: the median `torque_saturated_frac` of small-wheel designs is at least 0.25 and at least three times that of large-wheel designs, and the median settling time of small-wheel designs is at least 1.25 times that of large-wheel designs | `tests/test_adcs_enrichment.py` on the committed enriched CSV |
| R-5 | The enriched dataset has at least 1000 designs, the same columns as the original plus the scenario columns (`slew_deg`, `wheel_set`), a settled fraction of at least 0.85, finite positive attributes, and the share of designs violating `momentum_ok` is reported by a test (a flag, not a metric) | `test_adcs_enrichment.py`; pandas inspection |
| R-6 | The enriched dataset is seed-stable: for the first 20 designs, regenerating with the recorded options reproduces the committed rows with the WP4 per-column tolerances (categorical and flags equal, settling within 0.5 s, continuous columns rtol 1e-4, `torque_saturated_frac` rtol 2e-2), and 40 designs regenerated twice on the same platform are identical | `uv run pytest tests/test_adcs_case.py -k enriched` |
| R-7 | Probe acceptance, conditioning the four attributes by hand as in the probe note (reciprocal orientation, log, standardize, settled designs only), fitting `HyperbolicTradeSpace` at τ = ∞ (`min_exponent = 0`) and at the working τ with `frac_above_` ≈ 0.10, and using the near-frontier rows |log V| < 1/τ: (a) the contending set at τ = ∞ has size at least 3 and includes mass with exponent at least 0.05; (b) mass is in the support in at least 90 % of 100 bootstrap resamples of the designs, with median exponent at least 0.05; (c) the pooled near-frontier association of settling with mass is at most −0.30 (agility against mass), with at least two wheel classes represented by at least 10 near-frontier designs each; (d) the previously exposed tensions are retained: settling–effort, pointing–effort and pointing–mass associations are each at most −0.30 and settling–pointing is not negative | `test_adcs_enrichment.py` (the hand version of the probe, deterministic seeds); when the WP3 tension report is available the same quantities are also computed with `tension_report` and must agree |
| R-8 | Each exposed tension is physically explicable: the probe note gives, for agility vs mass, settling vs effort, pointing vs effort and pointing vs mass, the mechanism and the design variable through which it acts, and states any tension that appears but is not recognizable | inspection of the probe note |
| R-9 | The probe note records every lever tried (including ones that did not help), the final configuration and values, and the results of R-7 with near-frontier sample sizes | inspection |
| R-10 | The full suite, linters and lock pass and nothing outside scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff --stat <start>..HEAD` shows only the deliverable paths and `work-packages/` | run the commands; inspect the diff |
| R-11 | No AI attribution lines; commits authored as Michael Zargham; CI green on every push | `git log` grep returns 0; `gh run list` |

## Definition of good

- The enriched case tells an engineer's story: small wheels are slow and light, large wheels fast and heavy, and the fit finds that on its own, alongside the sensor and gain tensions already found.
- The enrichment is minimal and physically plausible: one scenario change and one wheel-class set, with values a spacecraft engineer would find reasonable for illustration, not tuned until a test passes.
- The probe note is an honest record, including levers that failed, so WP7 can interpret the result without surprise.
- The WP4 deliverables are untouched and the enriched dataset sits beside the original.

## Definition of good enough

- Deliverables D-1 to D-7 exist at the stated paths.
- R-1 to R-11 pass as checked, with evidence in the review report; in particular the probe conditions of R-7 hold on the committed enriched dataset.
- Non-goals untouched (no simulator, estimator, toolkit or notebook change).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item. WP4b is independent of WP3 and may start as soon as its scope is approved; if the WP3 tension report is available at review it is also run (R-7).

- Levers, in this order of preference *(default)*: (1) a larger slew angle so that the controller saturates (`initial_error_deg` is already an argument of `evaluate_design`), starting at 45° with horizon `t_end = 1200` s and `max_step = 0.5`; (2) the enriched wheel set `WHEEL_CLASSES_ENRICHED` with a wider maxTorque spread and wheel masses that make the mass difference between classes comparable to the star-tracker difference; (3) only if (1) and (2) fail R-7, a steeper slew angle (up to 90°) or a shorter horizon; the additional-attribute lever is not used (see OD1).
- Starting values for the enriched wheel set *(default, illustrative)*: small (maxTorque 0.02 N·m, maxMomentum 1 N·m·s, mass 0.8 kg), medium (0.10, 4, 2.5), large (0.50, 16, 6.0); the values are chosen for physical plausibility first, and may be adjusted at most three times if R-4 or R-7 fail, with every attempt recorded in the probe note (R-9).
- Scenario options *(default)*: `evaluate_design(row, t_end=900.0, max_step=0.5, initial_error_deg=10.0, wheel_set="original")`; `wheel_set` in {"original", "enriched"}; `sample_designs` is unchanged (the wheel class names are the same, only the table differs); the dataset columns gain `slew_deg` and `wheel_set` *(default)*.
- Generator flags *(default)*: `--slew-deg` (default 10.0), `--wheel-set` (default "original"), `--t-end` (default 900.0); `--out` for the enriched run is `examples/adcs/data/adcs_designs_enriched.csv`; the exact command is recorded in the probe note and in the CSV's sibling test.
- Dataset size *(default)*: 1000 designs, seed 0; if the near-frontier counts needed by R-7(c) are insufficient at 1000 designs, the dataset is generated with 2000 designs and the change is recorded.
- Probe method *(default)*: exactly the probe note's method (settled designs, standardized reciprocal log-metrics, τ = ∞ LP with `min_exponent = 0`, working τ by bisection to `frac_above_` ≈ 0.10, near-frontier |log V| < 1/τ, Pearson association, PCA of near-frontier Z); bootstrap with 100 resamples seeded 0; thresholds as in R-7.
- Tests *(default)*: `tests/test_adcs_enrichment.py` fits `HyperbolicTradeSpace` and uses `solvers.solve_lp` on the committed enriched CSV; it takes a few seconds; no simulation is run in it.
- The sibling reproducibility test in `tests/test_adcs_case.py` regenerates 20 designs with the recorded options and compares to the CSV with the WP4 per-column tolerances; the same-platform exactness test uses 40 designs twice *(default)*.
- SysML text *(default)*: add a `part def` set for the enriched wheel classes and a `scenario` item for the slew; still documentation only.
- Commits prefixed "WP4b: "; options and wheel set with tests, then the dataset, then the probe note, then status table and decisions file; every push green and attribution-free *(default)*.
- If after the allowed adjustments R-7 does not hold, execution stops and the driver is told (a problem-level change: the case cannot be made to expose the intended tensions with these levers) *(default)*.

## Open decisions (for the supervisor)

- **OD1.** Should the enrichment also add one additional cost-like attribute (a fifth metric, for example a power proxy derived from wheel torque or a sensor cost, labelled illustrative), or keep the case at the four attributes? A fifth attribute changes the case (d = 5, the notebook's 3-D surface and four-attribute probe) and the WP7 scope. — options: (a) keep four attributes; the enrichment is the scenario and the wheel set only / (b) add one illustrative power proxy attribute as a fifth metric / (c) add one illustrative sensor-cost attribute as a fifth metric
