# WP3 — Review report (second pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP3-scope-of-work.md` |
| **Scope approval verified** | The recorded act is a verbal approval in chat, typed into `work-packages/WP3-decisions.md` by the agent (commit 83f4038): "okay proceed", given for four gates together; defaults list approved as one item, open decisions none. The project has no PRs, so `gh pr view` does not apply. Previously dispositioned as G-1 (accept as is). |
| **Work reviewed** | WP3 commits 7f82d43, 348644c, ca095e5, 494145a, c793e10, 0815c82, plus the round-1 fix f635a04 (G-2) and d0a2c0d (limitations.md follow-up). Head checked at d0a2c0d on main. WP4b and WP6 commits in the range are not reviewed here. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP3-decisions.md`, after this report |

Reviewer: a fresh session that built none of WP3 and wrote none of its reviews. This is a complete rerun from step 1 after the round-1 fix. Review only; trial edits were reverted with `git checkout` and never committed.

Commands run at d0a2c0d: plain `unset VIRTUAL_ENV; uv run pytest -q` gave **844 passed, 8 skipped, 1 xfailed** (the 8 skips are sklearn array-API checks; the one xfail is WP3's `check_regressor_multioutput`; WP4b's xfail is gone after its amendment). Doctests run in the default run (`addopts = "--doctest-modules"`). `uv run ruff check .` passed; `ruff format --check .` reported 94 files formatted; `uv lock --check` resolved 173 packages. `git log --format=%B | grep -ciE 'co-authored|generated with'` returned 0; all 117 commits are authored Michael Zargham. `gh run list --limit 6`: success at d0a2c0d, failure at 8f49253 (WP6) and f635a04 (WP3), success on the three earlier runs.

**Red runs in the WP3 range** (checked with `gh run list --limit 30` and `gh run view --log-failed`): two, both with the same cause. f635a04 (WP3, G-2 fix) and 8f49253 (WP6) failed `tests/test_narrative.py::test_no_wp3_signatures_quoted`: "limitations.md quotes select_temperature". The f635a04 text in `docs/limitations.md` named `select_temperature`. d0a2c0d replaced it with "see the API page" and CI is green again. No other red run in the range (all earlier WP3 pushes were green). R-21 says "CI green on every push"; this was not true for two pushes, and was repaired within five minutes.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `src/hyperbolic_trade_space/preconditioning.py`: `LogAffinePreconditioner`, `frontier_in_original_units` |
| D-2 | met | `tuning.py`: `select_temperature` |
| D-3 | met | `gaps.py`: `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca` |
| D-4 | met | `tensions.py`: `tension_report`, frozen `TensionReport` |
| D-5 | met | `predictive.py`: `TradeSpaceRegressor` |
| D-6 | met | `plotting.py`: the four named functions plus `plot_tensions` |
| D-7 | met | `docs/preconditioning.md` |
| D-8 | met | `docs/api.md` |
| D-9 | met | `tests/test_preconditioning.py`, `test_tuning.py`, `test_gaps.py`, `test_tensions.py`, `test_predictive.py`, `test_plotting.py`, `test_docs.py`; preconditioner and regressor blocks in `test_sklearn_compat.py` |
| D-10 | met | `__init__.py` exports `LogAffinePreconditioner`, `frontier_in_original_units`, `select_temperature`, `TradeSpaceRegressor`, `tension_report` (the scope's defaults list) |
| D-11 | met | `work-packages/WP3-decisions.md` holds the approval and the round-1 dispositions; acceptance entry is "pending" by design |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `pytest tests/test_preconditioning.py`: 52 passed. Fitted attributes `scaler_`, `log_scale_`, `log_offset_`, `orientation_`, `shift_` present; my scratch round trip on nine mixed-orientation columns is 1.2e-15 (relative). |
| R-2 | met | Same file: unit log-std, robust log-IQR, "Negative values in data". |
| R-3 | met | Pull-back matches `score_samples` to 1e-9 and the labelled L9 cross-check passes. Trial (a): multiplying `exponents_orig` by 1.01 gives 21 failed, 31 passed in `test_preconditioning.py`. |
| R-4 | met, narrowed range now documented | `test_tuning.py` passes. I re-measured `frac_above_` on `make_frontier_data(400, 5, noise=0.05)`, seeds 1 to 3, tau = logspace(-1, 4, 16): from about 0.52 to 0.60 at tau 0.1, a bump above 0.5 below tau of about 3, then strictly nonincreasing for tau >= 3 on all three seeds, ending near 0.012. See the G-2 judgment below. |
| R-5 | met | `test_gaps.py` passes (isolated point, 2-D disc, 1-D gap, hull restriction, d-1 in {1,2,3}). |
| R-6 | met | `frontier_targets` V = 1 and round trip tested, with and without a preconditioner. |
| R-7 | met | `test_orient_by_pca_equals_report_directions`. |
| R-8 | met | Exponents equal `exponents_[0]`; exchange rate matrix −w_k/w_j. Trial (b): removing the minus sign gives 3 failed, 34 passed in `test_tensions.py`. |
| R-8a | met | Independent check below. |
| R-9 | met | Aligned pair positive, traded pair negative, with stated margins; closure effect in docstring, `closure_note` and a dedicated test. |
| R-10 | met | First direction within 5 degrees of the planted spread over seeds 0 to 2. |
| R-11 | met | Too-few-rows `ValueError`, d = 1 trivial report, band defaults, frozen and deterministic. |
| R-12 | met | `test_predictive.py` passes (fit, predict, `predict_coordinates`, `predict_novelty`, `predict_std`, coordinate-space `score`, order independence). |
| R-13 | met with deviation (G-3) | Coordinates and log V match truth within the stated tolerances; `predict_std` exercised with a GP. No row beyond the true frontier is planted, as in round 1. |
| R-14 | met | `TransformedTargetRegressor` test, and the docstring says why the wrapper does not replace the class. |
| R-15 | met | See check (a). |
| R-16 | met | `test_plotting.py` passes under Agg; each function returns Axes. |
| R-17 | met | `test_docs.py` passes (lemma tags 1 to 10, ledger ids, bib keys). |
| R-18 | met | Every exported name is in `api.md`; K > 1 and kernel sections say "documented, not built". |
| R-19 | met | Numpydoc docstrings; doctests run in the default run and pass. |
| R-20 | met | Suite, ruff, format and lock pass. WP3 commits touch only deliverable paths, `__init__.py` and `work-packages/`; but see Outside the scope for f635a04. |
| R-21 | met with a recorded exception | Attribution grep 0; authors all Michael Zargham; CI green at head; two red pushes (f635a04, 8f49253) described above, both repaired by d0a2c0d. |

### Checks asked of the reviewer

**(a) sklearn conformance.** `test_sklearn_compat.py`: 389 passed, 8 skipped, 1 xfailed. `LogAffinePreconditioner` passes `parametrize_with_checks(..., xfail_strict=True)` with an empty expected-failures dict. `TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace())` passes with exactly one documented expected failure, `check_regressor_multioutput`, with a written reason (sklearn 1.9.1 feeds negative y from `make_regression` and does not apply the positive-target tag for that check; multi-output shapes are covered in `test_predictive.py`). The compat instances use scalar orientation (not the scope's `[-1,1,1]` sample), as the scope's default allowed with a comment.

**(b) Tension report, independent run.** Planted supports of size 2, 3, 4, 5 in d = 5 with new seeds 11 and 12, n = 700, my own generator (not the test file's): at tau = inf the contending sets are exactly {0,1}, {0,1,2}, {0,1,2,3} and {0..4}, with `lemma_name` dilemma, trilemma, 4-lemma, 5-lemma and exponents equal to the planted weights (for example [0.4, 0.35, 0.25]). At tau = 5 on the size-3 case the working weights are [0.408, 0.333, 0.253, 0.006, 0.000] against planted [0.4, 0.35, 0.25, 0, 0]: smoothed, with the free metrics near zero. A fit with `min_exponent=0.05` makes `tension_report` emit the `UserWarning` ("estimator.min_exponent = 0.05 > 0 floors the working exponents; the n-lemma read..."). Part 1 reports exponents, exchange rates, participation; the report distinguishes exact membership (`contending_set`) from weak participation.

**(c) Nine-attribute preconditioner scratch check.** Nine columns, scales 1e-2 to 1e3, orientation `[1,-1,-1,1,-1,1,-1,-1,1]`, scalers standard and robust: metrics finite and strictly positive; round trip 1.2e-15 and 1.3e-15; all five named attributes plus `inverse_transform`, `get_feature_names_out`, `n_features_in_` present (`feature_names_in_` absent for ndarray input, as expected); `select_temperature` returns tau 10.7 (standard) and 15.4 (robust) with `frac_above_` 0.10 and 0.0925; `frontier_in_original_units` returns keys `exponents_orig`, `log_const`, `shift` and each exponent's sign agrees with its orientation; `tension_report` returns a 9-lemma on random data (no planted frontier), as expected.

**(d) Trials.** (a) `exponents_orig` times 1.01: 21 failures; (b) exchange-rate sign flip: 3 failures. Both reverted with `git checkout`; `git status` clean.

## G-2 fix judged

What the tests assert (`tests/test_tuning.py::test_tau_sweep_is_monotone_from_half_toward_zero`): `frac_above_` nonincreasing on tau >= 3 over a 16-point logspace grid from 0.1 to 1e4 (seed 1), `0.4 < frac_above_(0.1) < 0.65`, final `< 0.05`, `n_eff_` from near N toward d.

- The `select_temperature` docstring says monotone fall "for tau of about 3 and above", non-monotone below, may overshoot 0.5 below about 3, bracket-only requirement with `ValueError` otherwise, and "Keep bounds[0] near or above 3 for a unique answer". Matches the test. One small tension: the default `bounds=(1e-1, 1e4)` has `bounds[0]` far below 3, so the default call is outside the advice; the docstring does not say so. Minor.
- `docs/api.md` states the same range, the same 0.4 to 0.65 bound at tau = 0.1 and refers to the test. Matches the test. Its phrase "decreases monotonically toward 0" above 3 is what the test checks on one seed and a 16-point grid; I confirmed it on seeds 1 to 3. Not a proof, and the text attributes it to the test, not a lemma.
- What L5 proves: log-mean-exp lies between the mean and the maximum of the scores and recovers the maximum with a log(n)/tau gap (the limit tau -> 0 to the mean is the standard limit; the docs cite L5 for the bounds). The claim "tends toward what lies above the mean rather than the median" is explicitly marked in `api.md` as "the project's reading ..., not proved by L5", and in the docstring as "the project's reading". So the median remark is marked as the project's reading in both places. The data agree (overshoot to 0.52 to 0.60 on three seeds).
- Verdict: the fix is adequate and consistent with the tests and with L5; no overclaim found.

limitations.md changes. f635a04 edited `docs/limitations.md`, which is not among the files the G-2 disposition named (`select_temperature` docstring, docs/api.md). Of the changes there, the small-tau sentence (the "very low temperature" passage) is G-2-related and reasonable: it states the weights approach uniform and the soft maximum approaches the mean (L5), and `frac_above_` is not monotone there. d0a2c0d then changed its pointer from "see `select_temperature` in `docs/api.md`" to "see the API page", which is necessary because `test_no_wp3_signatures_quoted` forbids `limitations.md` naming WP3 functions, and was the repair of the red CI. Appropriate in itself. But f635a04 also contains two edits in the same file that have nothing to do with G-2: the K > 1 "tighten the bound" sentence now says "expected to tighten ... (a conjecture, not proved)", and the L10 sentence now says the shift-equivariance and soft-maximum limit are proved while homogeneity, projection and novelty carrying over is "expected from the construction, not proved". These match the WP6 review's G-3 (reword claims), commit 8f49253 came 40 seconds later with WP6 rewording; the two appear to have been mixed through concurrent work on the same file. They are WP6 content, committed under a WP3 message, and not named in WP3's fix. They are correct reductions of claims and harmless, but are out of the scope of the G-2 fix. See G-5.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-11 exist | met | See Deliverables |
| R-1 to R-21 pass as checked | met, with G-3 (R-13) and the CI note on R-21 | See Requirements |
| Non-goals untouched | met | No WP3 commit touches `derivation/`, `solvers.py`, `coordinates.py`, `estimator.py`, `datasets.py` or `references.bib`; only `__init__.py` exports; no K > 1 or kernel code; no WP6/WP7 content except the f635a04 limitations.md lines (G-5) |
| Expected-failures dict has a reason for every entry | met | Preconditioner dict empty; regressor dict has one reasoned entry |

## Outside the scope

- **Out-of-scope changes:** `docs/limitations.md` in f635a04 and d0a2c0d (WP6's file, not a WP3 deliverable): one G-2 sentence and one pointer change (appropriate), plus two unrelated K > 1 claim rewordings (G-5). The range diff `83f4038..HEAD` also contains WP4b files (`examples/adcs/*`, `pyproject.toml`, `uv.lock`, `.github/workflows/test.yml`, `tests/test_cubesat_model.py`, `tests/test_adcs_enrichment.py`) and WP6 files (`docs/method.md`, `why-and-how.md`, `limitations.md`, `tests/test_narrative.py`, the spec); they belong to other packages.
- **Non-goals touched:** none.

## Observations (not counted as failures)

- The default `bounds[0] = 0.1` of `select_temperature` lies in the non-monotone region that the docstring now advises against.
- `participating` (threshold 1e-3) flags free metrics at finite tau when their smoothed weights are about 0.01 (seen at tau 5: 0.006); `contending_set` is the exact reading.
- `predict_std` ignores chart-fit uncertainty; `TradeSpaceRegressor` needs strictly positive y.
- The decisions file's date (2026-11-08) is a day after the commit timestamps (UTC versus local).

## Follow-up candidates

- **G-3** (R-13): no planted beyond-frontier row. `make_configured_frontier_data` never exceeds log V = 0, so the novelty test shows sign and ordering against the tau = 10 soft frontier, not detection of a genuinely beyond-frontier design. It needs a hook in WP2's `datasets.py` (a WP3 non-goal to change). Recorded disposition: follow-up candidate.

## Previously dispositioned (recorded in WP3-decisions.md)

| Gap | Recorded disposition | State in this pass |
|---|---|---|
| G-1 approval wording | accept as is | unchanged |
| G-2 small-tau `frac_above_` | fix before acceptance | fix delivered (f635a04, d0a2c0d); judged adequate above |
| G-3 beyond-frontier novelty | follow-up candidate | listed above |
| G-4 observations | accept as is | unchanged (README status table has since been updated in a2f33f4) |

## Open decisions (for the supervisor)

New gaps pending a disposition:

- **G-5.** f635a04 (a WP3-labelled commit for the G-2 fix) also changed two unrelated K > 1 claims in `docs/limitations.md` (WP6's file, matching WP6 review G-3), and the same commit and 8f49253 pushed red CI (cause fixed in d0a2c0d). Options: accept as is / fix before acceptance / follow-up work package
- **G-6.** The `select_temperature` default `bounds=(1e-1, 1e4)` starts below the tau of about 3 that the new docstring says to stay above, and the docstring does not say the default is outside that advice. Options: accept as is / fix before acceptance / follow-up work package

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 to G-4 | as recorded above | decisions file, round 1 |
| G-5 | pending | |
| G-6 | pending | |

## Recommendation

Recommend acceptance with the listed gaps noted, provisional until G-5 and G-6 have dispositions: every requirement R-1 to R-21 passed when I ran it at d0a2c0d (844 passed, ruff, format, lock, attribution and authors clean, CI green at head), the independent planted-support runs recover exact supports of size 2 to 5 at tau = inf and warn on `min_exponent > 0`, the single expected failure has a genuine documented reason, the nine-attribute preconditioner works, both trials fail the tests, and the G-2 fix matches what the tests assert and what L5 proves, with the median remark marked as the project's reading. The remaining weaknesses are G-3 (a follow-up candidate), the two red pushes now repaired, and the stray limitations.md edits, which reduce claims and do no harm.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
