# WP2 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP2-scope-of-work.md` (approved at 67fff4e per the decisions file) |
| **Scope approval verified** | Recorded in `work-packages/WP2-decisions.md` (section "Scope approval", commit bcfe110): supervisor (mzargham), verbatim "double check with the github cli but then let's move forward"; the file's own disposition line is "driver's reading", approval of the scope and its defaults as one item, open decisions none. The project has no PRs, so this is the recorded act the scope names (a chat quote typed by the agent). The review cannot confirm the chat itself. The approval wording is conditional ("double check ... but then") and the record is dated 2026-11-08 while the commits are dated 2026-11-07 (local time, -0500; CI timestamps are 2026-11-08 UTC, so this is probably a timezone artifact). Both are recorded as G-4. The pre-approval naming decisions (class `HyperbolicTradeSpace`, package `hyperbolic_trade_space`) are quoted in the same file and match the code. |
| **Work reviewed** | `main` at `6b5a6a5`, after `git pull --rebase`. WP2 commits: c8e0f6e, 6ab5f5c, 5600a4c, c14bbfa, bfadf36, 880a4ec, 6b5a6a5. Diff base for the out-of-scope check: `bcfe110^`. Working tree clean at start. All trial edits were restored with `git checkout` and none committed. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP2-decisions.md`, after this report |

The reviewer did not build WP2. Every command below was run in this session with `unset VIRTUAL_ENV; uv run ...`.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `src/hyperbolic_trade_space/solvers.py` (272 lines). Read in full: `log_mean_exp` via `logsumexp(tau*s, b=1/N)/tau`, `support_weights`, `objective_and_grad`, `solve_lp` (`linprog(method="highs")`, duals from `res.ineqlin.marginals`), `solve_slsqp` (analytic jac, LP warm start), frozen `SolveResult` with the seven spec fields. Imports numpy and scipy only. |
| D-2 | met | `coordinates.py` (150 lines): `helmert_basis`, `alr_basis`, `to_frontier_coordinates`, `from_frontier_coordinates`; d = 1 gives shape (0, 1). |
| D-3 | met | `estimator.py` (515 lines) and `__init__.py` exporting `HyperbolicTradeSpace`, `make_frontier_data`, `make_configured_frontier_data`, `__version__`. |
| D-4 | met | `datasets.py` (195 lines), both generators. |
| D-5 | met | `tests/test_solvers.py` (102), `test_coordinates.py` (66), `test_datasets.py` (61), `test_estimator.py` (321). |
| D-6 | met | `tests/test_sklearn_compat.py` (68). |
| D-7 | met | `tests/test_matches_derivation.py` (203). |
| D-8 | met for the approval record; acceptance entry pending | `WP2-decisions.md` holds the approval record and the pre-approval naming decisions. The "Acceptance" section reads "pending `work-packages/WP2-review.md`", as it should before sign-off. See G-4 for wording and date observations. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `uv run pytest tests/test_solvers.py`: 15 passed. `test_lme_matches_naive` (tau 0.1, 1, 10, rel 1e-12), `test_lme_stable_and_inf` (tau 1e5 on 100.0, returns 100.0 at inf, a -inf entry gets weight 0), `test_support_weights` (ties within 1e-14 averaged; tau 0.5 to 1e4 nonnegative, sum 1). Trial (a) below shows the test fails when the normalization is broken. |
| R-2 | met | `test_gradient_check` at tau 0.5, 5, 100 uses `scipy.optimize.check_grad` with tolerance `1e-5*max(1, tau)`. The gradient in code is `U.T @ p`. |
| R-3 | met | `test_lp_hand_built` (answer w = (.5,.5), t = .5, duals (.5,.5,0) sum 1) and `test_lp_asymmetric_and_floor` (w = (1/3, 2/3), floor 0.5 case, KKT `p @ U` equal). |
| R-4 | met | `test_slsqp_agrees_with_lp` d in {2,3,5}: SLSQP at tau 1e3 within 2e-2 of the LP, LP within 1e-6 of the planted w, `0 <= lp.beta - sq.beta <= log(N)/tau`; `SolveResult` fields read in source. |
| R-5 | met | `test_coordinates.py`: 25 passed (ILR B Bᵀ = I and B1 = 0 at d = 2..8 to 1e-12, ALR round trip, shift invariance, d = 1 zero columns, -inf rows). Trial (b) shows the round-trip tests fail when the inverse is scaled. |
| R-6 | met | `test_datasets.py`: 5 passed; `make_frontier_data` returns `(X, info)` with keys `exponents, log_offset, basis, frontier_mask, Z, log_v` (noise level read in source/tests); `make_configured_frontier_data` returns `(X_config, Y_metrics, info)`. |
| R-7 | met | `test_recovery_tau_inf` d in {2,3,5} asserts exponents within 1e-6 and offset within 1e-6; `test_recovery_tau_1e3` asserts 2e-2. Both pass, with the stated tolerances. |
| R-8 | met | `test_fit_invariants` over tau in {inf, 10, 1e3} and min_exponent in {0, 0.1}: simplex and floor, p >= 0 and sum 1, 1 <= n_eff <= N, at inf `frac_above_ == 0` and max V <= 1 + 1e-9, at finite tau 0 < frac_above < 0.5, `n_iter_ >= 1`. |
| R-9 | met | Rescaling shifts beta by log 3 (tau inf and 20) leaving w and scores unchanged; replication x3; interior density (`interior_scale` 0.3 vs 3.0, same frontier mask) at tau inf to 1e-6 and at tau 2e3 to 2e-2; row and column permutation equivariance; Gaussian offset test: N = 40000, sigma 0.2, tau 5, `rel=5e-2` against tau sigma² ‖w‖²/2, matching the scope default. All pass. |
| R-10 | met | `test_chart_roundtrip_and_score_samples` (ilr and alr, tau inf and 10: inverse(transform) to rtol 1e-9, last column equals `score_samples`, `fit_transform` equal), `test_project_and_improvement_factors_land_on_frontier` (V of project = 1; multiplying each metric by its factor gives V = 1 to 1e-9), `test_level_set` (V = value for 1, 0.5, 2, and same Z). |
| R-11 | met | `test_novelty_score` (V - 1; calibrated rank equals the empirical fraction recomputed independently in the test; second column tau·log V, log V at inf); `test_leave_one_out_super_efficiency` refits without each support row at tau inf and checks V >= 1 - 1e-9. |
| R-12 | met | `test_d1`, `test_single_sample_gives_balanced_exponents`, `test_zero_metric_row` (tau inf and 10: V 0, log V -inf, p 0, Z nan, no inverse, fit equal to the fit without the zero row), `test_negative_and_nonfinite_raise` (message "Negative values in data" on fit and transform; NaN and inf), `test_n_terms_not_implemented`, `test_invalid_params_raise_in_fit_not_init`. |
| R-13 | met | `test_pipeline_and_feature_names` (Pipeline, clone, names `ilr0, ilr1, log_v`, `alr0, alr1, log_v`, the "input_features should have length equal" error) and `test_column_transformer_passes_metrics_and_covariates` (passthrough column, names, `set_output(transform="pandas")`, `feature_names_in_`). |
| R-14 | met | `test_sklearn_compat.py`: no `predict`, `decision_function`, `score`, `predict_proba` on the class; `score_samples`, `transform`, `inverse_transform`, `fit_transform`, `get_feature_names_out` present; no `_more_tags` or `_get_tags`; tags `positive_only=True`, `sparse=False` through `__sklearn_tags__`; `__init__` stores `object()` sentinels verbatim; new fitted attributes all end in `_`; `n_iter_ >= 1` at tau inf (LP) and 10 (SLSQP). Inspection against the note: see "Conformance read" below. |
| R-15 | met | `EXPECTED_FAILURES: dict[str, str] = {}` (empty), passed as `expected_failed_checks=lambda est: EXPECTED_FAILURES` with `xfail_strict=True`, over `HyperbolicTradeSpace()`, `(temperature=np.inf)`, `(coordinates="alr")`. `uv run pytest tests/test_sklearn_compat.py -q`: 146 passed, 3 skipped (144 parametrized check items, of which 3 are skipped, plus 5 other tests in the file). The 3 skips are `SCIPY_ARRAY_API is not set: not checking array_api input`, one per instance, an environment condition, not an expected failure. |
| R-16 | met | `uv run pytest tests/test_matches_derivation.py`: 6 passed. See "Cross-check read" below; trial (c) shows it fails when `improvement_factors` is perturbed. |
| R-17 | **not met as checked** (G-1) | The stated check is `uv run pytest` with doctest-modules enabled. `testpaths = ["tests"]` means the default command collects 0 doctests from `src/`: default `uv run pytest -q` gives 342 passed, 3 skipped; `uv run pytest -q tests src` gives 364 passed, 3 skipped (22 doctests). With the explicit path all doctests pass. Docstring audit by script (Parameters, Returns, Examples for functions and methods; Parameters, Attributes, Examples for classes) over all public items in the four modules: everything complete except `SolveResult`, which has Attributes but no Parameters or Examples section. |
| R-18 | met, with an observation (G-3) | `uv run pytest -q tests src`: 364 passed, 3 skipped. `uv run ruff check .`: All checks passed. `uv run ruff format --check .`: 58 files already formatted. `uv lock --check`: Resolved 153 packages. Diff check below. CI is red on the head (G-3). |
| R-19 | met | `git log --format=%B \| grep -ciE 'co-authored-by\|generated with'` over all of main returns 0. `git log --format='%an\|%cn' bcfe110^..HEAD`: 14 commits, all "Michael Zargham" for author and committer. The "CI check" half was not run locally; see G-3 for CI state. |

### Conformance read (estimator.py against the note)

- `fit` calls `validate_data(self, X, reset=True, dtype=float64)` first (through `_log_metrics`); `transform`, `score_samples`, `improvement_factors` and the domain methods go through `_coordinates`, which runs `check_is_fitted` then `validate_data(reset=False)`. `inverse_transform` calls `check_is_fitted`, `check_array` and a width check with the sklearn-style message, as the note prescribes (never wrapped by `set_output`). `project` calls `check_array` after `score_samples`; `level_set` uses `check_array` and a width check. The width-mismatch test passes for `transform`, `score_samples` and `inverse_transform`.
- Tags: only `__sklearn_tags__`, calling `super()` first. Mixin order `(TransformerMixin, BaseEstimator)`. No `predict`/`score`/`decision_function`.
- Negatives: `check_non_negative(X, "HyperbolicTradeSpace (input X)")` and the message "Negative values in data" is tested for fit and transform. Zeros are tolerated as -inf rows. NaN/inf come from the default `validate_data`.
- `n_iter_`: `max(int(n_iter), 1)`; LP path uses `nit` (clamped to >= 1), the d = 1 and one-sample paths set 1.
- `get_feature_names_out(input_features=None)`: object ndarray of the transform width, ValueError "input_features should have length equal to number of features", plus a check against `feature_names_in_`. `set_output` works because the method exists (pandas output asserted through `ColumnTransformer`).
- `EXPECTED_FAILURES` is truly empty and `xfail_strict=True`, so any expected failure that passes would fail the run; with an empty dict nothing is excused. 144 parametrized check items, 0 failed, 3 skipped (array API, environment).
- Not in the note's list but worth recording: `__init__` stores parameters verbatim (sentinel test); `_check_params` raises `ValueError` from `fit`, and `NotImplementedError` for `n_terms != 1` only after the other parameters validate.

### Cross-check read (R-16): not tautological

`test_matches_derivation.py` builds the chain once with `run_chain(verbose=False)` and substitutes seeded numbers (d = 3, n = 5, 1-based indices) into the stored SymPy expressions (`L1["V"]`, `V_tilde`, `Vk`; `L2["J"]`, `J_shifted`, `J_shifted_reduced`; `L5["LME"]`, `LSE`, `offset`, `mean`, `lme_minus_M_lower`; `L3["dJ"]`, `p_def`, `KKT.lhs`, `dsimplex`; `L7["logf_star"]`, `f_star`, `logV_new`, `x_sol`, `dG`; `L8["Z"]`, `shifted`, `ell`). Each is compared to what `solvers`, `coordinates` or the estimator return, at 1e-10 (the offset-of-a-fit comparison uses 1e-8, which is looser than R-16's 1e-10; see G-5). The chain values are computed by SymPy evaluation of the lemma expression, independently of the numpy code, so the comparison can fail. Trial (c) confirmed this for L7. Two weaknesses, neither a failure of R-16: `test_L1` and `test_L7` overwrite `exponents_` and `log_offset_` on a fitted estimator to inject the seeded `w` and beta (this is a legitimate way to test the formula, but it bypasses the fit), and the L1 comparison multiplies the chain's V by `exp(-beta)` by hand because the chain's `V` has no offset.

### Departures documented by the implementer

- **Validation order in `fit`:** `validate_data` and non-negativity run before parameter validation, because `min_exponent < 1/d` needs d. Consequence: invalid parameters on negative data raise the negative-data error first. Harmless; the scope says "validated in `fit`".
- **All-zero input raises `ValueError`:** consistent with the scope default ("if every row is masked, `fit` raises"); tested. A sklearn check could in principle feed all-zero data; the 144 checks pass, so none does.
- **`improvement_factors` is `inf` where w_j = 0 or V = 0:** per the scope default. Observation (G-5): the test is `w == 0` exactly. At finite tau SLSQP can return a numerically tiny but nonzero exponent. Reviewer probe (planted w = (.5,.5,0), noise 0.02, tau 10): `exponents_ = [0.5127, 0.4873, 3.4e-17]`, and `improvement_factors` returned finite-but-astronomical or overflowed values with a RuntimeWarning "overflow encountered in exp" (the maximum of column 3 was `inf` only because of overflow). The result is correct (inf) but it is reached by overflow with a warning, not by the stated rule.
- **`novelty_score(calibrated=True)` ranks against finite training log V:** documented in the docstring; zero-metric training rows are excluded from the rank denominator. Matches the scope default (an empirical fraction of training log V <= the query's), applied to the finite ones. Consistent with the test.

## Trials (reviewer-run, restored, nothing committed)

| Trial | Edit | Result |
|---|---|---|
| (a) | `solvers.py`: `logsumexp(tau * s, b=1.0 / s.size) / tau` changed to `logsumexp(tau * s) / tau` (drops the 1/N normalization) | `pytest tests/test_solvers.py tests/test_estimator.py tests/test_matches_derivation.py tests/test_sklearn_compat.py`: **15 failed**, 201 passed; failures include `test_slsqp_agrees_with_lp[2,3,5]`, `test_fit_invariants[...-10.0/1000.0]` ("assert 0 < 0.0"), `test_row_replication_leaves_fit_unchanged[20.0]`, `test_d1`, `test_L2_objective_and_shift`, `test_L5_log_mean_exp`. Re-run on `tests/test_solvers.py` alone: 7 failed, including `test_lme_matches_naive[0.1, 1.0, 10.0]`, `test_lme_stable_and_inf` and `test_slsqp_agrees_with_lp[2,3,5]`. Restored with `git checkout`. |
| (b) | `coordinates.py`: inverse base scaled `Zf @ (2 * np.linalg.pinv(B)).T` | **22 failed**, 58 passed (`test_coordinates.py` round trips for ilr and alr at d up to 8, `test_minus_inf_rows`, `test_chart_roundtrip_and_score_samples` x4, `test_level_set` x2, `test_L8_chart_relations`). Restored. |
| (c) | `estimator.py` `improvement_factors`: exponent scaled by 1.01 (`np.exp(-1.01 * log_v / w)`) | **2 failed**, 53 passed: `test_matches_derivation.py::test_L7_improvement_factor_and_elasticity` and `test_estimator.py::test_project_and_improvement_factors_land_on_frontier`. Restored. `git status --short` empty afterwards. |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-8 exist at the stated paths | met | See Deliverables table. D-8 acceptance entry is pending by design. |
| R-1 to R-19 pass as checked, with evidence in the review report | **not met** for R-17 as literally checked; all others met | R-17: the default `uv run pytest` does not run the `src/` doctests (G-1). The doctests themselves pass when run with `tests src`. |
| Non-goals untouched (no preconditioner, tuning, gaps, plotting, regressor, K > 1 code) | met | `grep -nE 'Preconditioner|select_temperature|gaps|plotting|TradeSpaceRegressor|predict' src/hyperbolic_trade_space/*.py` finds no implementation; the only `n_terms` handling is the validation and the `NotImplementedError` for `n_terms != 1`. No `predict`, `score` or `decision_function`. No new runtime dependency (`pyproject.toml` unchanged by WP2 commits; sklearn pin is `>=1.8`). |
| Expected-failures dict, if non-empty, has a stated reason for every entry | met (empty, also meets the definition of good) | `EXPECTED_FAILURES = {}`. |

Definition of good, observed (not graded): names match the spec (`exponents_`, `log_offset_`, `support_weights_`, `n_eff_`, `frac_above_`); docstrings cite the lemma (L1 to L8); the solver layer imports no scikit-learn; `frac_above_`, `n_eff_` and `training_log_v_` surface the finite-sample departure from the chain; overflow is handled in `log_mean_exp`/`support_weights` (but see G-5 for `improvement_factors`).

## Outside the scope

- **Out-of-scope changes:** none by WP2 commits. `git show --stat` of the seven WP2 commits lists only `src/hyperbolic_trade_space/{solvers,coordinates,datasets,estimator,__init__}.py` and `tests/test_{solvers,coordinates,datasets,estimator,sklearn_compat,matches_derivation}.py`. `git diff --stat bcfe110^..HEAD` shows 26 files; the other 19 belong to WP4 (`examples/adcs/`, `tests/test_adcs_case.py`, `WP4-decisions.md`) and WP5 (`docs/literature.md`, `docs/references.bib`, `tests/test_references.py`, `WP5-review.md`, `WP5-decisions.md`), plus `pyproject.toml` (one line, `pythonpath` gained `examples/adcs`, by WP4) and `work-packages/README.md` (3 lines, status/approval wording from bcfe110). WP2 commits did not touch `pyproject.toml` or the Status table; the scope's "Status table" update did not occur in WP2 commits, so the Status table still shows whatever bcfe110 left (not checked further).
- **Non-goals touched:** none. `git diff bcfe110^..HEAD -- derivation docs/superpowers/specs` is empty (no derivation or spec change).

## Observations (not counted as failures)

- **CI is red on main.** `gh run list`: the runs for 3864a8a, bfadf36, 880a4ec and 6b5a6a5 all conclude "failure". The log of each shows one failing test, `tests/test_adcs_case.py::test_dataset_reproducible_first_20` (WP4: `control_effort` differs at the 1e-5 relative level, platform float variation against the committed pin; "1 failed, 341 passed" at the head), and no WP2 test failed. It passes locally. This is a WP4 matter but it means "main stays green on every push" (WP2 default) did not hold, and R-19's "CI check" cannot be reported green. Commit 880a4ec was also red on ruff: `git show 880a4ec:tests/test_matches_derivation.py | ruff check` reports 1 error (a loop variable not bound in a lambda, B023); `6b5a6a5` fixed it, so the lint failure lasted one commit.
- The scope's own R-17 check names a command (`uv run pytest`) that cannot do what the requirement needs under `testpaths = ["tests"]`; the wording is a scope issue as much as a delivery issue.
- The tau-looser tolerances in the cross-check: the offset-of-a-fit comparison is 1e-8, not 1e-10 as R-16 says (the fit is a numerical solve, so 1e-10 would be unrealistic; stated here for the record).
- Array-API checks are skipped in this environment (`SCIPY_ARRAY_API` unset); the estimator declares `array_api_support=False` by default, so this is expected.
- Gap to the spec's test list that is WP3's: planted-hole round trip, `select_temperature` hit.
- Date oddity in `WP2-decisions.md` (G-4).

## Open decisions (for the supervisor)

- **G-1.** R-17 not met as checked: the default `uv run pytest` collects no `src/` doctests (22 doctests run only with `uv run pytest tests src`); `SolveResult` has no Parameters/Examples section. Options: accept as is / fix before acceptance (for example `testpaths = ["tests", "src"]` and an Examples line on `SolveResult`) / follow-up work package.
- **G-2.** `improvement_factors` returns `inf` for a metric with a numerically tiny but nonzero exponent only through overflow with a RuntimeWarning, since the guard is `w == 0` exactly (probe above). Options: accept as is / fix before acceptance / follow-up work package.
- **G-3.** CI is red on main at the head (WP4 test `test_dataset_reproducible_first_20`; no WP2 test fails), and commit 880a4ec was also red on lint for one commit (fixed by 6b5a6a5). Options: accept as is / fix before acceptance / follow-up work package.
- **G-4.** The approval record: conditional wording ("double check with the github cli but then let's move forward"), typed by the agent and dated 2026-11-08 against commits dated 2026-11-07 local (probably UTC vs local); the scope file's own Status line still says DRAFT. Options: accept as is / fix before acceptance / follow-up work package.
- **G-5.** Smaller items, put as one item: the R-16 offset-of-a-fit comparison uses 1e-8 rather than 1e-10; the cross-check overrides fitted attributes to inject `w` and beta; the four documented departures (validation order, all-zero rows raise, `inf` improvement factors where w_j = 0, calibrated novelty ranks against finite training log V) are consistent with the scope defaults. Options: accept as is / pick any to fix before acceptance / follow-up work package.

## Gap dispositions

Resolved through the decision loop (`~/.claude/skills/CLAUDE.md`); records go in `work-packages/WP2-decisions.md`.

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 R-17 default command does not run `src/` doctests; `SolveResult` lacks Examples | pending | |
| G-2 `improvement_factors` inf via overflow for near-zero exponents | pending | |
| G-3 CI red at head (WP4 test); 880a4ec lint-red for one commit | pending | |
| G-4 Approval record wording and date; scope Status line | pending | |
| G-5 Cross-check tolerance and attribute override; documented departures | pending | |

## Recommendation

Provisional, pending the gap dispositions: do not recommend acceptance yet, because R-17 is not met as the scope states it (the default `uv run pytest` runs no doctests from `src/`) and the CI run on the head is red. Everything else checks out: all other requirements pass with evidence, the scikit-learn checks pass with an empty expected-failures dict, the cross-check against the WP1 chain is a real comparison (it fails when the improvement factor is perturbed), the three mutation trials are caught, and no non-goal or out-of-scope change was found in the WP2 commits. If the supervisor accepts G-1 and G-3 as is, or fixes them, this becomes "recommend acceptance with the listed gaps noted".

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
