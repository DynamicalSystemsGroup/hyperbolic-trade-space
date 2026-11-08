# WP2 — Review report (second pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP2-scope-of-work.md` (approved at 67fff4e) |
| **Scope approval verified** | Recorded act: verbal approval typed into `work-packages/WP2-decisions.md` (commit bcfe110, authored Michael Zargham, after 67fff4e). Supervisor's words as recorded: "double check with the github cli but then let's move forward". `gh run list` shows CI success on 67fff4e and bcfe110. The record is conditional in wording, typed by the agent, dated 2026-11-08 against a 2026-11-07 commit date (see G-1). |
| **Work reviewed** | `67fff4e..b95a0d4` on main. WP2 commits: c8e0f6e 6ab5f5c 5600a4c c14bbfa bfadf36 880a4ec 6b5a6a5, and fixes 454b227 07f8b67 a60b57c (WP4/WP5 commits interleaved are not reviewed here) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP2-decisions.md`, after this report |

Reviewer: a fresh session that did not build WP2 or write the first review. This replaces the first review (5099f1f). Review only; nothing was repaired.

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

Plain `unset VIRTUAL_ENV; uv run pytest -q` at b95a0d4: **366 passed, 3 skipped** (skips are sklearn array-API checks, `SCIPY_ARRAY_API` unset). `pytest --collect-only` lists 23 `src/...::` doctest items, so doctests are collected by default (`testpaths = ["tests", "src"]`, `--doctest-modules`).

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
| R-16 | met, with a limitation (see G-2) | `test_matches_derivation.py` evaluates stored SymPy expressions (L1, L2, L3, L5, L7, L8) at a seeded d=3, n=5 instance and compares to solvers, chart and estimator at TOL=1e-10; the offset-of-a-fit comparison is now 1e-10 too (a60b57c). Trial (c) shows it fails when the improvement factor is perturbed. Limitation: for L1 and L7 the test fits an estimator and then overwrites `exponents_` and `log_offset_` with the instance values, so it checks the formulas of `invariant_value` and `improvement_factors` against the chain, not fitted outputs; only the L2 offset comparison uses a genuinely fitted attribute. The labelling as a cross-check (not a proof) is accurate. |
| R-17 | met | Default run collects 23 doctests and passes. An introspection audit of every public class, function and method for Parameters / Returns / Attributes (classes) / Examples found only `fit_transform` (inherited from `TransformerMixin`) without its own Examples. |
| R-18 | met | pytest as above; `uv run ruff check .` all checks passed; `uv run ruff format --check .` 60 files already formatted; `uv lock --check` resolved 153 packages, no change. Diff of `67fff4e..HEAD` excluding `work-packages/`: WP2 paths plus `pyproject.toml` (see Outside the scope). |
| R-19 | met | `git log --format=%B \| grep -ciE 'co-authored-by\|generated with'` returns 0 over all commits; all 61 commits authored "Michael Zargham". CI on head b95a0d4: `gh run list` shows **success**. |

## Reviewer trials (restored with `git checkout`, nothing committed; `git status --short` empty afterwards)

| Trial | Edit | Result |
|---|---|---|
| (a) | `solvers.py` line 112: drop the 1/N normalization (`b=1.0 / s.size` -> `b=1.0`) | 15 failed, 56 passed over `test_solvers.py`, `test_matches_derivation.py`, `test_estimator.py` (e.g. `test_fit_invariants[...-10.0/1000.0]`, `test_row_replication_leaves_fit_unchanged[20.0]`, `test_d1`) |
| (b) | `coordinates.py` line 148: add 1e-3 to the chart inverse | 27 failed, 54 passed over `test_coordinates.py`, `test_matches_derivation.py`, `test_estimator.py` (round trips, `test_level_set`, `test_d1`) |
| (c) | `estimator.py` `improvement_factors`: exponent scaled by 1.01 | `test_matches_derivation.py::test_L7_improvement_factor_and_elasticity` fails (expected 0.29848901 +- 3e-11); 1 failed, 5 passed |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-8 exist at the stated paths | met | Deliverables table |
| R-1 to R-19 pass as checked, with evidence | met | Requirements table, run at b95a0d4 |
| Non-goals untouched | met | No preconditioner, `select_temperature`, regressor, gaps, plotting or K>1 code in `src/`; no `predict`/`score`/`decision_function`; no new runtime dependency (`pyproject.toml` dependencies unchanged); `git diff 67fff4e..HEAD -- derivation docs/superpowers/specs` has no WP2 changes |
| Expected-failures dict, if non-empty, has reasons | met | Empty |

Definition of good, observed (not graded): names match the spec; docstrings cite lemmas; `n_eff_`, `frac_above_`, `training_log_v_` expose finite-sample departures; the solver layer has no scikit-learn import; overflow handled, `improvement_factors` now treats exponents below 1e-12 as zero without an overflow warning (07f8b67, tested).

## Outside the scope

- **Out-of-scope changes by WP2 commits:** none. The seven original WP2 commits touch only the D-1..D-7 paths and `__init__.py`; fixes 454b227 (`pyproject.toml` testpaths, `solvers.py` docstring), 07f8b67 (`estimator.py`, `test_estimator.py`), a60b57c (`test_matches_derivation.py`) are within the deliverables. `pyproject.toml` changes in the range: `testpaths = ["tests", "src"]` (WP2, the R-17 fix; R-18 allows pyproject changes "only if a test option needs it") and `pythonpath` gaining `examples/adcs` (WP4).
- **Other packages in the range:** WP4 (`examples/adcs/`, `tests/test_adcs_case.py`) and WP5 (`docs/literature.md`, `docs/references.bib`, `tests/test_references.py`) files, plus their review/decision files. Not WP2's; reviewed in their own reports.
- **Non-goals touched:** none.

## Observations (not counted as failures)

- Still present from the first review: the approval record wording and date (G-1); the cross-check injecting fitted attributes (G-2); the documented departures from the scope defaults (G-3); one red commit, 880a4ec (G-4).
- CI history: c14bbfa is not listed; runs on 3864a8a, bfadf36, 880a4ec, 6b5a6a5, 5099f1f, 087f2ed and a60b57c were red, the head b95a0d4 is green. The failure on the WP2 commits was the WP4 platform-float test, not a WP2 test; the head fix widened that WP4 test's rtol to 3e-2 (the WP4 scope's R-9 amendment is flagged as pending in 234ee2c).
- The scope file's own Status line still reads "DRAFT" (the approval is recorded in `WP2-decisions.md` and the README status table says "in progress").
- Spec sections 4, 5, 7 were checked through the scope's requirements and tests rather than a line-by-line spec read; I found no divergence.
- Planted-hole round trip and `select_temperature` remain WP3's.

## Open decisions (for the supervisor)

- **G-1.** Approval record: conditional wording ("double check with the github cli but then let's move forward"), typed by the agent, dated 2026-11-08 while commits are dated 2026-11-07 (likely UTC versus local); the scope Status line still says DRAFT. — options: accept as is / fix before acceptance / follow-up work package
- **G-2.** The cross-check overrides `exponents_` and `log_offset_` after fitting for L1 and L7, so those lemmas are checked on formulas, not on fitted values (L2 offset uses a real fit). — options: accept as is / fix before acceptance / follow-up work package
- **G-3.** Documented departures consistent with the scope defaults: validation order in `fit` (data checks before parameter checks); all-zero input raises; `inf` improvement factors where w_j < 1e-12 or V = 0 (the stated rule was w_j = 0; the threshold is a documented widening); calibrated novelty ranks against finite training log V. — options: accept as is / fix before acceptance / follow-up work package
- **G-4.** Commit 880a4ec was red on lint for one commit (fixed by 6b5a6a5), and several WP2-labelled commits had red CI because of a WP4 test; the head is green. — options: accept as is / fix before acceptance / follow-up work package

## Gap dispositions

Records go in `work-packages/WP2-decisions.md` through the decision loop (`~/.claude/skills/CLAUDE.md`).

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 Approval record wording and date; Status line DRAFT | pending | |
| G-2 Cross-check injects fitted attributes for L1, L7 | pending | |
| G-3 Documented departures from scope defaults | pending | |
| G-4 880a4ec red on lint; CI red on earlier WP2 commits | pending | |

## Recommendation

Provisional, pending the gap dispositions: recommend acceptance with the listed gaps noted, because all of R-1 to R-19 are met at head b95a0d4 with run evidence (366 passed, doctests collected by default, ruff, format and lock clean, zero attribution lines, CI green, expected-failures dict empty), the three reviewer trials are all caught, and no non-goal or out-of-scope change by WP2 was found. The remaining gaps are record-keeping and test-depth observations, none affecting a good-enough item.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
