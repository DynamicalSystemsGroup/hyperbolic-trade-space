# WP2 — Review report (fourth pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP2-scope-of-work.md` (approved at 67fff4e) |
| **Scope approval verified** | Recorded act: verbal approval typed into `work-packages/WP2-decisions.md` (commit bcfe110, authored Michael Zargham, after 67fff4e). Supervisor's words as recorded: "double check with the github cli but then let's move forward". `gh run list` shows CI success on 67fff4e and bcfe110. Conditional in wording, typed by the agent (G-1, dispositioned). |
| **Work reviewed** | WP2 commits c8e0f6e..5c3dc1c on main: c8e0f6e 6ab5f5c 5600a4c c14bbfa bfadf36 880a4ec 6b5a6a5 454b227 07f8b67 a60b57c 76f93f1, and the G-5 fix 5c3dc1c. Head checked at a9fc4f2 (WP4/WP5 record only; no source change after 5c3dc1c). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP2-decisions.md`, after this report |

Reviewer: a fresh session that built none of WP2 and wrote none of the earlier reviews. This replaces the third pass (ea3105b). The whole review was rerun from step 1 after the G-5 fix (supervisor's choice "Fix WP2 tolerance to 1e-10", recorded in `WP2-decisions.md`). The only change since the third review is 5c3dc1c: three tolerances (module docstring, the 12-case test, the negative control's first assertion) went from 1e-9 to 1e-10 in `tests/test_matches_derivation.py`. Review only; nothing was repaired.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `src/hyperbolic_trade_space/solvers.py` (287 lines) |
| D-2 | met | `coordinates.py` (150 lines) |
| D-3 | met | `estimator.py` (516 lines) and `__init__.py` exports |
| D-4 | met | `datasets.py` (195 lines) |
| D-5 | met | `tests/test_solvers.py`, `test_coordinates.py`, `test_datasets.py`, `test_estimator.py` present |
| D-6 | met | `tests/test_sklearn_compat.py` |
| D-7 | met | `tests/test_matches_derivation.py` (283 lines) |
| D-8 | met | `work-packages/WP2-decisions.md` (approval record, round 1 and round 2 dispositions); acceptance entry "pending" by design |

## Requirements

Plain `unset VIRTUAL_ENV; uv run pytest -q`: **381 passed, 3 skipped** (sklearn array-API checks, `SCIPY_ARRAY_API` unset). `pytest --collect-only -q` lists 23 `src/...` doctest items, so doctests run by default (`testpaths = ["tests", "src"]`).

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `tests/test_solvers.py` passes. Trial (c) (drop the 1/N) makes 15 tests fail in the solver, estimator and derivation-match files. |
| R-2 | met | `test_solvers.py` includes `check_grad`; passes |
| R-3 | met | hand-built LP, duals sum to 1; passes |
| R-4 | met | SLSQP agrees with LP at tau=1e3; `SolveResult` frozen with the seven fields |
| R-5 | met | `tests/test_coordinates.py` passes (ILR d=2..8, ALR invertible, round trip, shift invariance, d=1) |
| R-6 | met | `tests/test_datasets.py` passes |
| R-7 | met | recovery d in {2,3,5}: < 1e-6 at tau=inf, < 2e-2 at tau=1e3; passes |
| R-8 | met | fit invariants test passes |
| R-9 | met | rescaling, replication, interior density, permutation, Gaussian offset (N=40000, rel 5e-2); pass |
| R-10 | met | round trip, `transform[:, -1] == score_samples`, `project`, `improvement_factors`, `level_set`; pass |
| R-11 | met | `novelty_score` V-1, calibrated, leave-one-out super-efficiency; pass |
| R-12 | met | d=1, zero metric, negative/non-finite, `n_terms=2`, all-zero rows; pass |
| R-13 | met | Pipeline, ColumnTransformer, feature names; pass |
| R-14 | met | non-check tests in `test_sklearn_compat.py` pass; no `predict`/`decision_function`/`score` defined in `src/` |
| R-15 | met | `EXPECTED_FAILURES: dict[str, str] = {}`, `xfail_strict=True`, three instances; `uv run pytest tests/test_sklearn_compat.py`: 146 passed, 3 skipped. The array-API skips are expected. |
| R-16 | met | Formula-level group at TOL=1e-10 (L1, L2, L3, L5, L7, L8). The fitted-model group (`test_fitted_model_matches_chain_L1_L7_L8`, 12 cases: seeds 0,1,2 x d 3,4 x tau 4, inf; and `test_fitted_model_check_negative_control`) now asserts `< 1e-10`, the literal R-16 value (5c3dc1c). Worst discrepancy measured by running `chain_vs_model` on all 12 cases: **1.7e-15** (cases span 5.6e-16 to 1.65e-15), so the tolerance has about five orders of margin. Negative control (outputs times 1+1e-6): discrepancy **1.00e-06**, above its 1e-7 threshold, so the check is live. Fitted attributes are only read. |
| R-17 | met | 23 doctests collected and pass; numpydoc sections present (fit_transform inherits `TransformerMixin`'s docstring, as in the third pass) |
| R-18 | met | `uv run pytest -q` 381 passed, 3 skipped; `uv run ruff check .` all checks passed; `uv run ruff format --check .` 60 files already formatted; `uv lock --check` resolved 153 packages. See Outside the scope for the diff. |
| R-19 | met | `git log --format=%B \| grep -ciE 'co-authored-by\|generated with'` returns 0; `git log --format=%an` shows 77 commits, all Michael Zargham. `gh run list --limit 5`: all five completed success, including 5c3dc1c (run 42440965392) and head a9fc4f2 (42441005139). |

## Reviewer trials (restored with `git checkout`, nothing committed; `git status --short` empty afterwards)

Fitted-model tests = the 13 tests of the G-2 group. Wider set = `test_matches_derivation.py`, `test_solvers.py`, `test_estimator.py` (84 tests).

| Trial | Edit | Fitted-model tests | Wider set |
|---|---|---|---|
| (a) | `invariant_value` returns 1.001 * V | 13 failed | 20 failed |
| (b) | `improvement_factors` returns 1.001 * result | 13 failed | 15 failed |
| (c) | chart inverse `from_frontier_coordinates`: `U + 1e-3` | 13 failed | 24 failed |
| (d) | `log_mean_exp`: `b=1.0 / s.size` -> `b=1.0` | 13 passed (offset is read from the fit) | 15 failed (formula-level L1/L2, solver and estimator tests catch it) |

The fitted-model group detects 0.1% perturbations of `invariant_value`, `improvement_factors` and the chart inverse at the 1e-10 tolerance. A broken `log_mean_exp` is caught by the other tests, not by this group, as in earlier passes.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-8 exist at the stated paths | met | Deliverables table |
| R-1 to R-19 pass as checked, with evidence | met | Requirements table |
| Non-goals untouched | met | No preconditioner, `select_temperature`, regressor, gaps, plotting or K>1 code in `src/`; no `predict`/`score`/`decision_function`; `pyproject.toml` dependencies unchanged |
| Expected-failures dict, if non-empty, has reasons | met | Empty |

Definition of good, observed (not graded): names match the spec; docstrings cite lemmas; `n_eff_`, `frac_above_`, `training_log_v_` expose finite-sample departures; the solver layer has no scikit-learn import.

## Outside the scope

- **Out-of-scope changes by WP2 commits:** none. The WP2 commits touch only `src/hyperbolic_trade_space/{__init__,solvers,coordinates,datasets,estimator}.py`, `tests/test_{solvers,coordinates,datasets,estimator,sklearn_compat,matches_derivation}.py`, `pyproject.toml` (`testpaths`, the R-17 doctest option) and `work-packages/`. 5c3dc1c touches only `tests/test_matches_derivation.py` (3 insertions, 3 deletions).
- **Other packages in the range c8e0f6e^..5c3dc1c:** WP4 (`examples/adcs/`, `tests/test_adcs_case.py`, adcs-port note, `pythonpath` gained `examples/adcs`) and WP5 (`docs/literature.md`, `docs/references.bib`, `tests/test_references.py`), plus 7f3d589, a WP5 correction of one sentence in the design spec (`git diff --stat 67fff4e..HEAD -- docs/superpowers/specs`: 7 insertions, 3 deletions). None is WP2's. No change under `derivation/`.
- **Non-goals touched:** none.

## Observations (not counted as failures)

- CI history: earlier WP2-labelled commits were red (lint at 880a4ec; a WP4 platform-float test), which is G-4 (dispositioned); the last five runs including head are green.
- The scope file's Status line still reads "DRAFT" (G-1, dispositioned).
- Spec sections 4, 5, 7 and the conformance note were checked through the scope's requirements and tests rather than line by line; no divergence found.
- The chart-inverse comparison in the fitted-model group uses a formula derived in the test (`ell = log V + beta - w.B^T Z`), not a chain expression (noted in the third pass; not a gap under R-16's wording).

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop. Counts: G-1 to G-5, all dispositioned (4 accept as is, 1 fix before acceptance, now verified fixed); no new gap raised in this pass.

## Gap dispositions

Records are in `work-packages/WP2-decisions.md` (rounds 1 and 2) and follow the decision loop (`~/.claude/skills/CLAUDE.md`).

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 Approval record wording and date; Status line DRAFT | accept as is (WP2-decisions.md, round 1) | Supervisor's choice |
| G-2 Cross-check injected fitted attributes for L1, L7 | fix before acceptance (round 1); fixed in 76f93f1, verified in the third pass and again here (trials a to c) | Whole review rerun |
| G-3 Documented departures from scope defaults | accept as is (round 1) | Supervisor's choice |
| G-4 880a4ec red on lint; CI red on earlier WP2 commits | accept as is (round 1) | Supervisor's choice |
| G-5 Fitted-model cross-check tolerance 1e-9 vs R-16's 1e-10 | fix before acceptance (round 2: "Fix WP2 tolerance to 1e-10"); fixed in 5c3dc1c, verified here (worst 1.7e-15; all 13 tests pass at 1e-10) | Whole review rerun |

## Recommendation

Recommend acceptance, because all of R-1 to R-19 are met at head a9fc4f2 with run evidence (381 passed, 3 skipped; 23 doctests collected by default; ruff, format and lock clean; zero attribution lines; all 77 commits authored by Michael Zargham; CI green on the last five runs including 5c3dc1c and head; expected-failures dict empty), the G-5 tolerance is now the literal 1e-10 with a worst fitted-model discrepancy of 1.7e-15 and a live negative control, the trials show the fitted-model group still detects perturbations, no gap is pending, and no non-goal or out-of-scope change by WP2 was found.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
