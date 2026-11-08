# WP3 — Review report (third pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP3-scope-of-work.md` |
| **Scope approval verified** | Verbal approval in chat, typed into `work-packages/WP3-decisions.md` by the agent (commit 83f4038): "okay proceed", for four gates together; defaults list approved as one item, open decisions none. The project has no PRs, so `gh pr view` does not apply. Previously dispositioned as G-1 (accept as is). |
| **Work reviewed** | WP3 commits 7f82d43, 348644c, ca095e5, 494145a, c793e10, 0815c82; round-1 fix f635a04 (G-2) and d0a2c0d; round-2 fix 07fe9d3 (G-6). Head 7704ab7 on main. WP4b and WP6 commits in the range are not reviewed here. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP3-decisions.md`, after this report |

Reviewer: a fresh session that built none of WP3 and wrote none of its reviews. Complete rerun from step 1 after the G-6 fix. Review only; trial edits were reverted with `git checkout` and never committed (`git status` clean).

Commands run at 7704ab7: plain `unset VIRTUAL_ENV; uv run pytest -q`: **839 passed, 8 skipped, 6 xfailed**. The 8 skips are sklearn array-API checks. Of the 6 xfails, 1 is WP3's (`check_regressor_multioutput`, documented) and 5 are WP4b's strict xfails in `tests/test_adcs_enrichment.py` (the WP4b amendment-2 stop rule; not WP3). The count is lower than the last pass (844 passed) only because WP4b's amendment 2 moved five tests from pass to xfail. Doctests run in the default run. Per-file: `test_preconditioning.py` 52, `test_tuning.py` 18, `test_gaps.py` 20, `test_tensions.py` 37, `test_predictive.py` 14, `test_plotting.py` 8, `test_docs.py` 9 passed; `test_sklearn_compat.py` 389 passed, 8 skipped, 1 xfailed. `uv run ruff check .` passed; `ruff format --check .` 95 files formatted; `uv lock --check` resolved 173 packages. `git log --format=%B | grep -ciE 'co-authored|generated with'` returned 0; all 129 commits authored Michael Zargham. `gh run list --limit 8`: all eight success, head 7704ab7 green.

**Red runs in the WP3 range** (`gh run list --limit 40` and `gh run view --log-failed`): two, same cause. f635a04 (WP3, G-2 fix) and 8f49253 (WP6) failed `tests/test_narrative.py::test_no_wp3_signatures_quoted` ("limitations.md quotes select_temperature"). d0a2c0d fixed it; every later run is green. Recorded in `WP3-decisions.md` round 2 as G-5, accept as is.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `src/hyperbolic_trade_space/preconditioning.py` |
| D-2 | met | `tuning.py` (`select_temperature`) |
| D-3 | met | `gaps.py` (four functions) |
| D-4 | met | `tensions.py` (`tension_report`, frozen `TensionReport`) |
| D-5 | met | `predictive.py` (`TradeSpaceRegressor`) |
| D-6 | met | `plotting.py` |
| D-7 | met | `docs/preconditioning.md` |
| D-8 | met | `docs/api.md` |
| D-9 | met | seven test files present and passing (counts above); preconditioner and regressor blocks in `test_sklearn_compat.py` |
| D-10 | met | `__init__.py` exports the five defaults-list names |
| D-11 | met | `WP3-decisions.md`: approval, round 1, round 2, follow-up list; acceptance entry "pending" by design |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `pytest tests/test_preconditioning.py`: 52 passed. Scratch below: attributes present, round trip 6e-15. |
| R-2 | met | same file (unit log-std, robust log-IQR, "Negative values in data") |
| R-3 | met | pull-back vs `score_samples` to 1e-9 and labelled L9 cross-check pass. Trial (a): `exponents_orig` times 1.01 gives 21 failed, 31 passed. |
| R-4 | met | `test_tuning.py` 18 passed. Re-measured `frac_above_` on `make_frontier_data(400, 5, noise=0.05)` seeds 1 to 3 at tau 0.1, 1, 3, 10, 1e3: seed 1 0.54/0.525/0.45/0.34/0.013; seed 3 0.60/0.555/0.46/0.34/0.015. Bump above 0.5 below tau ≈ 3, nonincreasing after. |
| R-5 | met | `test_gaps.py` 20 passed |
| R-6 | met | `frontier_targets` V = 1 and round trip tested, with and without a preconditioner |
| R-7 | met | `test_orient_by_pca_equals_report_directions` |
| R-8 | met | exponents equal `exponents_[0]`; rates are −w_k/w_j. Trial (b): sign removed gives 3 failed, 34 passed. |
| R-8a | met | independent run below |
| R-9 | met | traded pair negative, aligned pair positive, margins in test; closure effect in docstring and `closure_note` |
| R-10 | met | first direction recovers planted spread within the stated angle |
| R-11 | met | too-few-rows `ValueError`, d = 1 trivial report, band default, frozen, deterministic |
| R-12 | met | `test_predictive.py` 14 passed |
| R-13 | met with deviation (G-3) | no planted beyond-frontier row; `make_configured_frontier_data` never exceeds log V = 0. Follow-up list. |
| R-14 | met | `TransformedTargetRegressor` test and documented reason |
| R-15 | met | check (a) |
| R-16 | met | `test_plotting.py` 8 passed under Agg |
| R-17 | met | `test_docs.py` 9 passed |
| R-18 | met | every exported name in `api.md`; extensions marked "documented, not built" |
| R-19 | met | numpydoc docstrings; doctests run in the default run |
| R-20 | met | suite, ruff, format, lock pass. `git diff --stat 83f4038..HEAD` over `src/` shows only the seven WP3 modules plus `__init__.py` (no `derivation/`, `solvers.py`, `coordinates.py`, `estimator.py`, `datasets.py`, no `references.bib`). Other files in the range belong to WP4b and WP6. |
| R-21 | met with a recorded exception | attribution grep 0; authors all Michael Zargham; CI green at head; two red pushes described above (G-5, dispositioned) |

### Checks asked of the reviewer

**(a) sklearn conformance.** `LogAffinePreconditioner` passes `parametrize_with_checks(..., xfail_strict=True)` with an empty expected-failures dict. `TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace())` has exactly one documented expected failure, `check_regressor_multioutput`, with a written reason (sklearn feeds negative y and does not apply the positive-target tag there; multi-output shapes are covered in `test_predictive.py`). Compat instances use scalar orientation, which the scope's default allowed with a comment.

**(b) Tension report, independent.** My own generator (library `from_frontier_coordinates` and `helmert_basis`, random supports, n = 800, d = 5, seeds 31 and 32, different mixture of on, near and far rows from the test file). At tau = inf the contending set equals the planted support exactly in all eight cases (sizes 2, 3, 4, 5; names dilemma, trilemma, 4-lemma, 5-lemma), with exponents equal to the planted weights to 3 decimals (for example seed 32 size 3: [0.222, 0.322, 0.456]). Earlier with a cruder generator (no exact frontier points in the free directions) the LP returned extra support members at 0.001 weight; that is a finite-sample artefact of my first generator, not of the library. Working tau = 5 on a size-3 case: [0.286, 0.328, 0.382, 0.004, 0.000] against planted [0.293, 0.318, 0.389, 0, 0]. `min_exponent=0.05` emits the `UserWarning` ("estimator.min_exponent = 0.05 > 0 floors the working exponen..."). Exact membership (`contending_set`) is distinct from weak participation.

**(c) Nine-attribute preconditioner.** Nine columns, scales 1e-2 to 1e3, orientation `[1,-1,-1,1,-1,1,-1,-1,1]`, shift 0.5, scalers standard and robust: metrics finite and positive; round trip relative error 6.0e-15 for both; `scaler_`, `log_scale_`, `log_offset_`, `orientation_`, `shift_`, `n_features_in_` all present; `get_feature_names_out` works; `frontier_in_original_units` returns `exponents_orig`, `log_const`, `shift`.

**(d) Trials.** (a) 21 failures, (b) 3 failures; both reverted, tree clean.

## G-6 judged (07fe9d3)

Added to the `select_temperature` docstring and `docs/api.md`: the default `bounds[0] = 0.1` is wider than the recommended tau of about 3; bisection tolerates it because it only needs the target bracketed by the ends of `bounds` (`ValueError` otherwise); below tau ≈ 3 the response is not monotone, so the returned tau is a root of the bracket search; pass `bounds=(3, ...)` for the useful range.

- Accurate against `tests/test_tuning.py`: the sweep test asserts nonincreasing only for tau ≥ 3 and 0.4 < `frac_above_`(0.1) < 0.65; `test_not_bracketed_raises` asserts the `ValueError`. I confirmed on seeds 1 to 3 with default bounds that targets 0.05 to 0.30 return tau of 13 to 133, all in the monotone region, so the default bounds are harmless for those targets. For a target inside the bump (0.55, seed 3) the default call returns tau 1.24, a root in the non-monotone zone and not unique; for 0.55 on seeds 1 and 2 it raises "not bracketed". This matches the sentence ("a root of the bracket search"), though the sentence does not give an example.
- Consistent with L5: L5 gives the soft maximum between the mean and the maximum, which supports the small-tau limit; the sentence does not claim more, and the "mean rather than median" reading remains marked as the project's reading elsewhere in the same paragraph.
- Consistent between docstring and `api.md`: same content, same advice, same `ValueError` clause. Not contradicted by the earlier "Keep `bounds[0]` near or above 3" line (which it explains).
- Remaining wording point (minor, not a gap): "a root of the bracket search" is terse, and "is not monotone below tau ≈ 3" is attributed to measurement on the planted data, not proved.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-11 exist | met | Deliverables table |
| R-1 to R-21 pass as checked | met, with G-3 (R-13) and G-5 (R-21 note) | Requirements table |
| Non-goals untouched | met | R-20 evidence; no K > 1 or kernel code; WP6 limitations.md lines from f635a04 dispositioned as G-5 |
| Expected-failures dict reasoned | met | preconditioner empty; regressor one reasoned entry |

## Outside the scope

- **Out-of-scope changes:** `docs/limitations.md` in f635a04 and d0a2c0d (WP6's file; G-5, accepted as is). The range diff also contains WP4b files and WP6 files that belong to other packages. 07fe9d3 touches only `tuning.py`, `docs/api.md`, `WP3-decisions.md` (all in scope).
- **Non-goals touched:** none.

## Observations (not counted as failures)

- `participating` (threshold 1e-3) can flag free metrics at finite tau (0.004 at tau 5 in my run); `contending_set` is the exact reading.
- `predict_std` ignores chart-fit uncertainty; `TradeSpaceRegressor` needs strictly positive y.
- Five strict xfails in the suite are WP4b's, not WP3's; the whole-suite count therefore changes with WP4b.

## Previously dispositioned (recorded in WP3-decisions.md)

| Gap | Recorded disposition | State in this pass |
|---|---|---|
| G-1 approval wording | accept as is | unchanged |
| G-2 small-tau `frac_above_` | fix before acceptance | delivered (f635a04, d0a2c0d); still adequate |
| G-3 beyond-frontier novelty | follow-up (round 1 candidate; round 2 on the follow-up list) | listed in decisions file; needs WP2's generator |
| G-4 observations | accept as is | unchanged |
| G-5 limitations.md edits and red CI | accept as is (round 2) | unchanged; red cause re-verified from logs |
| G-6 default `bounds[0]` note | fix before acceptance (round 2: "Fix G-6 docstring line, accept the rest") | delivered (07fe9d3); judged above |

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop. No new gaps found in this pass.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1, G-2, G-4 | as recorded, round 1 | decisions file |
| G-3 | follow-up work package (list) | needs a hook in WP2's `datasets.py` |
| G-5 | accept as is | decisions file, round 2 |
| G-6 | fix delivered | 07fe9d3 |

## Recommendation

Recommend acceptance with the listed gaps noted: every requirement R-1 to R-21 passed when I ran it at 7704ab7 (suite, ruff, format, lock, attribution and authors clean, CI green at head), the independent planted-support runs recover exact supports of size 2 to 5 and warn on `min_exponent > 0`, the single expected failure has a documented reason, both trials fail the tests, and the G-6 sentence is accurate against the tests and L5 and consistent between docstring and `api.md`. Remaining gaps are G-3 (follow-up list), G-5 (accepted) and the two historical red pushes, repaired.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
