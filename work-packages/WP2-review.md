# WP2 — Review report (third pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP2-scope-of-work.md` (approved at 67fff4e) |
| **Scope approval verified** | Recorded act: verbal approval typed into `work-packages/WP2-decisions.md` (commit bcfe110, authored Michael Zargham, after 67fff4e). Supervisor's words as recorded: "double check with the github cli but then let's move forward". `gh run list` shows CI success on 67fff4e and bcfe110. The record is conditional in wording, typed by the agent, dated 2026-11-08 against a 2026-11-07 commit date (see G-1). |
| **Work reviewed** | `c8e0f6e..76f93f1` on main, head checked at 4ce27d4. WP2 commits: c8e0f6e 6ab5f5c 5600a4c c14bbfa bfadf36 880a4ec 6b5a6a5, fixes 454b227 07f8b67 a60b57c, and the G-2 fix 76f93f1 (WP4/WP5 commits interleaved are not reviewed here) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP2-decisions.md`, after this report |

Reviewer: a fresh session that built none of WP2 and wrote none of the earlier reviews. This replaces the second pass (e84bd7f). The whole review was rerun from step 1 after the G-2 fix (supervisor's disposition recorded in `WP2-decisions.md`). Review only; nothing was repaired.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `src/hyperbolic_trade_space/solvers.py` (287 lines) |
| D-2 | met | `coordinates.py` (150 lines) |
| D-3 | met | `estimator.py` (516 lines) and `__init__.py` exports |
| D-4 | met | `datasets.py` (195 lines) |
| D-5 | met | `tests/test_solvers.py`, `test_coordinates.py`, `test_datasets.py`, `test_estimator.py` present |
| D-6 | met | `tests/test_sklearn_compat.py` |
| D-7 | met | `tests/test_matches_derivation.py` |
| D-8 | met | `work-packages/WP2-decisions.md`; acceptance entry "pending" by design |

## Requirements

Plain `unset VIRTUAL_ENV; uv run pytest -q` at 4ce27d4 (code identical to 76f93f1 for WP2 paths): **381 passed, 3 skipped** (skips are sklearn array-API checks, `SCIPY_ARRAY_API` unset). `pytest --collect-only` lists 23 `src/...::` doctest items, so doctests are collected by default (`testpaths = ["tests", "src"]`, `--doctest-modules`).

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `tests/test_solvers.py` passes (naive-form match, stability, tau=inf max, softmax and tie-averaging). Trial (a) below breaks the 1/N normalization and the suite fails. |
| R-2 | met | `test_solvers.py` includes `check_grad`; passes |
| R-3 | met | `test_solvers.py` hand-built LP with duals summing to 1; passes |
| R-4 | met | `test_slsqp_agrees_with_lp` at tau=1e3; `SolveResult` frozen dataclass with the seven fields, now with Parameters and Examples (454b227) |
| R-5 | met | `tests/test_coordinates.py` passes (ILR d=2..8, ALR invertible, round trip, shift invariance, d=1). Tolerances in file are 1e-12 per the scope. |
| R-6 | met | `tests/test_datasets.py` passes |
| R-7 | met | `test_recovery_tau_inf` (d=2,3,5): max error < 1e-6; `test_recovery_tau_1e3`: < 2e-2. Exactly the scope's bounds. |
| R-8 | met | `test_fit_invariants` over (min_exponent, tau); frac_above_ = 0 and max V <= 1+1e-9 at tau=inf; 0 < frac_above_ < 0.5 at finite tau |
| R-9 | met | Rescaling, row replication, permutation equivariance at 1e-6..1e-8. Interior-density test replaces interior rows with a sparser draw and requires equal exponents at tau=inf (1e-6) and at tau=2e3 (2e-2); a real test of the claim. Gaussian offset test: N=40000 (scope asks >= 20000), rel 5e-2 as the scope default states. |
| R-10 | met | Round trip rtol 1e-9; `transform[:, -1] == score_samples`; `invariant_value(project(X)) = 1` (atol 1e-9); improvement factors land on V=1 (1e-9); `level_set` V=value (rtol 1e-9) and maps back to Z (1e-9). |
| R-11 | met | `test_novelty_score` checks V-1, the empirical rank (right-sided, finite training log V), tau*log V and log V at inf; `test_leave_one_out_super_efficiency` on every support row at tau=inf, >= 1-1e-9 |
| R-12 | met | `test_d1`, `test_zero_metric_row`, `test_negative_and_nonfinite_raise`, `test_n_terms_not_implemented`, `test_all_rows_zero_raises` pass |
| R-13 | met | `test_pipeline_and_feature_names`, `test_column_transformer_passes_metrics_and_covariates` pass |
| R-14 | met | `test_sklearn_compat.py` non-check tests pass (no predict/decision_function/score; tags via `__sklearn_tags__` only, `positive_only=True`, not sparse; `__init__` verbatim; fitted attributes end in `_`; `n_iter_ >= 1` at tau=inf and finite) |
| R-15 | met | `EXPECTED_FAILURES: dict = {}`, `xfail_strict=True`, three instances (default, tau=inf, ALR); 144 parametrized checks collected; `uv run pytest tests/test_sklearn_compat.py`: 146 passed, 3 skipped. Independent judgment: conformance claim is substantiated; the empty dict is not hiding anything (xfail_strict would flag an unused entry, and there are none). Array-API skips are expected (`array_api_support=False`). |
| R-16 | met | `test_matches_derivation.py` evaluates stored SymPy expressions (L1, L2, L3, L5, L7, L8) at a seeded d=3, n=5 instance against solvers, chart and estimator at TOL=1e-10 (the formula-level group). Since 76f93f1 a second group, `test_fitted_model_matches_chain_L1_L7_L8` (12 cases: seeds 0,1,2 x d 3,4 x tau 4, inf) and `test_fitted_model_check_negative_control`, fits `HyperbolicTradeSpace` on `make_frontier_data` and compares fitted `invariant_value`, `project`, `improvement_factors`, `transform` (Z and log V) and `inverse_transform` (plus the round trip) to the chain's L1 `V_tilde`, L7 `f_star` and L8 `Z` evaluated at the fitted `exponents_[0]`, `log_offset_[0]`, `basis_`, to 1e-9 (not 1e-10 as R-16 words it; a sensible fitted-value tolerance, see G-5). I read the group: `grep` for assignments to `est.*_` in it finds none; fitted attributes are only read. Trials below confirm it detects perturbations. See G-2 verdict below. |
| R-17 | met | Default run collects 23 doctests and passes. An introspection audit of every public class, function and method for Parameters / Returns / Attributes (classes) / Examples found only `fit_transform` (inherited from `TransformerMixin`) without its own Examples. |
| R-18 | met | `uv run pytest -q` 381 passed, 3 skipped; `uv run ruff check .` all checks passed; `uv run ruff format --check .` 60 files already formatted; `uv lock --check` resolved 153 packages, no change. WP2 commits (c8e0f6e..76f93f1, WP2-labelled) touch only the D-1..D-7 paths, `__init__.py` and `pyproject.toml` (see Outside the scope). |
| R-19 | met | `git log --format=%B \| grep -ciE 'co-authored-by\|generated with'` returns 0 over all commits; all 69 commits authored "Michael Zargham" (`git log --format=%an`). `gh run list --limit 5`: runs on 76f93f1, ef79e83, b138b6d, eae37e0 success; run on head 4ce27d4 completed success (`gh run view 42440079285`). |

## Reviewer trials (restored with `git checkout`, nothing committed; `git status --short` empty afterwards)

Fitted-model tests = `test_fitted_model_matches_chain_L1_L7_L8` plus `test_fitted_model_check_negative_control` (13 tests).

| Trial | Edit | Result |
|---|---|---|
| (a) G-2 | `estimator.py` `invariant_value`: result times 1.001 | 13 failed (all fitted-model tests) |
| (b) G-2 | `estimator.py` `improvement_factors`: result times 1.001 | 13 failed |
| (c) | `solvers.py` `log_mean_exp`: drop the 1/N normalization (`b=1.0 / s.size` -> `b=1.0`) | Fitted-model tests still pass (13 passed): the offset is read from the fit, so the chain check is self-consistent. Across `test_matches_derivation.py`, `test_solvers.py`, `test_estimator.py`: 15 failed, 69 passed (the formula-level L1/L2 tests and the solver and estimator tests catch it) |
| (d) | `coordinates.py` `from_frontier_coordinates`: add 1e-3 to `U` | 13 failed in the fitted-model tests (chart inverse caught) |
| (e) | `estimator.py` `inverse_transform`: result times 1.001 | 13 failed |

The new test detects perturbations of `invariant_value`, `improvement_factors` and the chart inverse at the level of fitted outputs. A broken `log_mean_exp` is not caught by it (it consumes the fitted offset as given) but is caught by the other tests, as in the second pass.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-8 exist at the stated paths | met | Deliverables table |
| R-1 to R-19 pass as checked, with evidence | met | Requirements table, run at 4ce27d4 |
| Non-goals untouched | met | No preconditioner, `select_temperature`, regressor, gaps, plotting or K>1 code in `src/`; no `predict`/`score`/`decision_function`; no new runtime dependency (`pyproject.toml` dependencies unchanged); `git diff 67fff4e..HEAD -- derivation docs/superpowers/specs` has no WP2 changes |
| Expected-failures dict, if non-empty, has reasons | met | Empty |

Definition of good, observed (not graded): names match the spec; docstrings cite lemmas; `n_eff_`, `frac_above_`, `training_log_v_` expose finite-sample departures; the solver layer has no scikit-learn import; overflow handled, `improvement_factors` now treats exponents below 1e-12 as zero without an overflow warning (07f8b67, tested).

## Outside the scope

- **Out-of-scope changes by WP2 commits:** none. The WP2 commits (c8e0f6e 6ab5f5c 5600a4c c14bbfa bfadf36 880a4ec 6b5a6a5 454b227 07f8b67 a60b57c 76f93f1) touch only `src/hyperbolic_trade_space/{__init__,solvers,coordinates,datasets,estimator}.py`, `tests/test_{solvers,coordinates,datasets,estimator,sklearn_compat,matches_derivation}.py` and `pyproject.toml` (`testpaths = ["tests", "src"]`, the R-17 doctest fix; R-18 allows pyproject changes if a test option needs it). 76f93f1 touches only `tests/test_matches_derivation.py`. `pythonpath` also gained `examples/adcs` in the range, from WP4. No change under `derivation/` or `docs/superpowers/specs`.
- **Other packages in the range:** WP4 (`examples/adcs/`, `tests/test_adcs_case.py`, adcs-port note) and WP5 (`docs/literature.md`, `docs/references.bib`, `tests/test_references.py`) plus their review and decision files. Not WP2's.
- **Non-goals touched:** none (no preconditioner, `select_temperature`, regressor, gaps, plotting or K>1 code; no `predict`/`score`/`decision_function`; no new runtime dependency).

## Observations (not counted as failures)

- G-2 assessment: **genuinely fixed.** The new group fits real estimators on seeded data, overwrites no fitted attribute, compares fitted outputs to the chain's L1/L7/L8 expressions evaluated at the fitted values, and fails when `invariant_value`, `improvement_factors`, `inverse_transform` or the chart inverse is perturbed by 1e-3 relative; the built-in negative control (perturb 1e-6, expects discrepancy > 1e-7) is itself live. Residual limits: the chain's L7 expression takes `u_pt` from the data and fitted offset, and the inverse-chart comparison uses a formula derived in the test (`ell = log V + beta - w.B^T Z`), not a chain expression; `log_mean_exp` correctness is covered by the formula-level and solver tests rather than by this group.
- G-1, G-3, G-4 are still present as recorded in the second pass, and carry the supervisor's recorded disposition (accept as is).
- G-5 (new): R-16 says 1e-10; the fitted-model group uses 1e-9 (fits to a numerical tolerance, `tol` default 1e-10, SLSQP at finite tau).
- CI history: several earlier WP2-labelled commits were red because of a WP4 platform-float test (fixed at b95a0d4 by widening its rtol); the head and the last five runs are green. The scope file's own Status line still reads "DRAFT".
- Spec sections 4, 5, 7 were checked through the scope's requirements and tests rather than a line-by-line read; no divergence found.

## Open decisions (for the supervisor)

- **G-5.** The fitted-model cross-check uses a 1e-9 tolerance where R-16 reads 1e-10. — options: accept as is / fix before acceptance / follow-up work package

Items G-1 to G-4 were dispositioned by the supervisor ("Fix G-2 before acceptance"; G-1, G-3, G-4 accept as is); G-2 is now fixed (above).

## Gap dispositions

Records are in `work-packages/WP2-decisions.md` (round 1) and go through the decision loop (`~/.claude/skills/CLAUDE.md`).

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 Approval record wording and date; Status line DRAFT | accept as is (WP2-decisions.md) | Supervisor's round 1 choice |
| G-2 Cross-check injects fitted attributes for L1, L7 | fix before acceptance (WP2-decisions.md); fix delivered in 76f93f1 and verified in this pass | Whole review rerun; trials above |
| G-3 Documented departures from scope defaults | accept as is (WP2-decisions.md) | Supervisor's round 1 choice |
| G-4 880a4ec red on lint; CI red on earlier WP2 commits | accept as is (WP2-decisions.md) | Supervisor's round 1 choice |
| G-5 Fitted-model cross-check tolerance 1e-9 vs R-16's 1e-10 | pending | New item |

## Recommendation

Recommend acceptance with the listed gaps noted (G-5 still needs the supervisor's disposition), because all of R-1 to R-19 are met at head 4ce27d4 with run evidence (381 passed, 3 skipped; doctests collected by default; ruff, format and lock clean; zero attribution lines; all commits authored by Michael Zargham; CI green at head; expected-failures dict empty), G-2 is genuinely fixed and demonstrated by trial (perturbing `invariant_value`, `improvement_factors` or the chart inverse fails the new fitted-model tests), and no non-goal or out-of-scope change by WP2 was found.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
