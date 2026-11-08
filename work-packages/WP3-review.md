# WP3 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP3-scope-of-work.md` |
| **Scope approval verified** | The recorded act is a verbal approval in chat, typed into `work-packages/WP3-decisions.md` by the agent (commit 83f4038, authored Michael Zargham, 2026-11-07 22:31 -0500): "okay proceed", given for four gates presented together (WP2 acceptance; WP3, WP6, WP4b approvals). The file records approved, defaults list approved as one item, open decisions none. The project has no PRs, so `gh pr view` does not apply; the quote is agent-typed and cannot be independently confirmed from git. See G-1. |
| **Work reviewed** | WP3 commits 7f82d43 (preconditioning, tuning), 348644c (gaps, tensions), ca095e5 (predictive, plotting, regressor block), 494145a, c793e10 (export sort), 0815c82 (docs and docs checks) on main. Head checked at 379dee0. WP6 and WP4b commits interleaved in the range are not reviewed here. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP3-decisions.md`, after this report |

Reviewer: a fresh session that built none of WP3. Review only; nothing was repaired. Trial edits were reverted with `git checkout` and never committed.

Commands run: plain `unset VIRTUAL_ENV; uv run pytest -q` gave **843 passed, 8 skipped, 2 xfailed** (the 8 skips are sklearn array-API checks; of the 2 xfails, one is WP3's `check_regressor_multioutput`, the other is WP4b's work-in-progress xfail). The eight WP3 test files plus the compat file alone gave **547 passed, 8 skipped, 1 xfailed**. `uv run pytest -q --doctest-modules src` gave 41 passed, and `addopts = "--doctest-modules"` is set in `pyproject.toml`, so doctests run in the default run. `ruff check .` passed; `ruff format --check .` reported 93 files formatted; `uv lock --check` resolved 173 packages. The attribution grep over all commit messages (`co-authored|generated with`) returned 0. All commits are authored Michael Zargham. `gh run list --limit 6` shows six successes, including every WP3 push (the WP3 docs commit 0815c82, 494145a, c793e10, ca095e5).

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `preconditioning.py` (313 lines): `LogAffinePreconditioner`, `frontier_in_original_units` |
| D-2 | met | `tuning.py` (106 lines): `select_temperature` |
| D-3 | met | `gaps.py` (218 lines): `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca` |
| D-4 | met | `tensions.py` (254 lines): `tension_report`, frozen `TensionReport` |
| D-5 | met | `predictive.py` (249 lines): `TradeSpaceRegressor` |
| D-6 | met | `plotting.py` (455 lines): the four named functions plus `plot_tensions` |
| D-7 | met | `docs/preconditioning.md` (192 lines, about 2100 words) |
| D-8 | met | `docs/api.md` (210 lines, about 1900 words) |
| D-9 | met | `tests/test_preconditioning.py`, `test_tuning.py`, `test_gaps.py`, `test_tensions.py`, `test_predictive.py`, `test_plotting.py`, `test_docs.py`; preconditioner and regressor blocks in `test_sklearn_compat.py` |
| D-10 | met | `__init__.py` exports exactly the five defaults names; `gaps` and `plotting` used through submodules as the defaults say |
| D-11 | met | `work-packages/WP3-decisions.md` exists with the approval record; acceptance entry is "pending" by design |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `test_preconditioning.py` passes (37 tests). Round trip to 1e-10 is parametrized over seeds 0 to 2 and scalers standard, robust, None and MinMax, with mixed orientation `[1,-1,-1,1]` and a nonzero per-column shift. Fitted attributes `scaler_`, `log_scale_`, `log_offset_`, `orientation_`, `shift_` are asserted. |
| R-2 | met | Unit log-std to 1e-10; robust log-IQR normalized to 1 ignoring zeros; negatives raise "Negative values in data" in fit, transform and inverse_transform. |
| R-3 | met | Pull-back matches pipeline `score_samples` to 1e-9 over 18 cases, and the labelled L9 cross-check evaluates the WP1 chain expression (`L9["target"]`, `V_derived`) to 1e-10 with a negative control. Trial (a): scaling `exponents_orig` by 1.01 makes 21 tests in the file fail. |
| R-4 | met with deviation | Bisection hits targets 0.05, 0.10, 0.20 within 0.01 over three seeds; bracket errors raise. The sweep claim differs from the scope's wording, see G-2. I measured seed 1, n=400: frac_above_ is 0.52, 0.57, 0.53, 0.485, 0.455, 0.343, 0.048, 0.007 at tau 0.1, 0.3, 1, 2, 3, 10, 100, 1e4, and n_eff_ is 395, 381, 316, 254, 218, 122, 5.8, 1.9. |
| R-5 | met | `knn_gap_scores` flags the isolated point for three seeds; the planted 2-D disc is located to one grid cell; the 1-D gap is found; hull restriction, d−1 in {1, 2, 3} and ValueError otherwise are tested. |
| R-6 | met | `frontier_targets` gives V = 1, round trip to 1e-9, with a stand-in and with a real preconditioner. |
| R-7 | met | `orient_by_pca` rotation, sign convention and mask are tested; `test_orient_by_pca_equals_report_directions` ties it to the report. |
| R-8 | met | Exponents equal `est.exponents_[0]`, exchange rate matrix is −w_k/w_j with NaN rows for non-participants and reciprocal pairs. Trial (b): removing the minus sign makes 3 tests fail. |
| R-8a | met | See check (b) below. Planted sizes 2, 3, 4 and 5 in d=5, three seeds each, recover the support exactly at tau=inf. The `min_exponent > 0` warning test passes. |
| R-9 | met | Aligned pair (0,1) association 0.93; traded pair (2,3) −0.98 in my run; the test margins are > 0.5 and < −0.5. The closure effect is in the module docstring, in `closure_note`, and in a dedicated test. |
| R-10 | met | First direction within 5 degrees of the planted spread for three seeds; loadings map back through `basis_`. |
| R-11 | met | Too few near-frontier rows raise ValueError naming a larger band; d = 1 gives the trivial report; band default is 1/tau and 0.1 at infinity; report is deterministic and frozen. |
| R-12 | met | `fit`, `predict`, `predict_coordinates`, `predict_novelty`, `predict_std` (via `available_if` on `return_std`), coordinate-space `score` R², order independence and the 1-D y case are all tested. |
| R-13 | met with deviation | Coordinates and log V match truth (median < 1e-3, p90 < 1e-2; R² > 0.999) with a fixed-kernel GP. `predict_std` is exercised with a GP and a Monte Carlo cross-check. There is no planted beyond-frontier configuration, see G-3. |
| R-14 | met | `TransformedTargetRegressor` composes with the chart (`check_inverse=False`) and its `predict` equals the regressor's to 1e-8; the docstring says why the wrapper does not replace the class. |
| R-15 | met | Preconditioner dict is empty; four instances pass. Regressor dict has one entry, `check_regressor_multioutput`, with a written reason; see check (a). |
| R-16 | met | Agg backend in `test_plotting.py`; each function returns Axes; vocabulary constants are in the module docstring; a test checks black frontier and grey band; no import of matplotlib at package import. |
| R-17 | met | `test_docs.py` passes. `preconditioning.md` cites lemma tags and ledger ids (A1, A4, L9 and others) and has no `[@key]`, which the "or" in R-17 allows. |
| R-18 | met | Every `__all__` name and every submodule function appears in `api.md`; five bibliography keys all resolve; K > 1 and kernel sections are headed "documented, not built". |
| R-19 | met | Numpydoc docstrings with seeded doctests; 41 doctests in `src` pass in the default run. |
| R-20 | met | Suite, ruff, format and lock pass (above). The WP3 commits alone touch only the deliverable paths and exports. The range diff also contains `pyproject.toml`, `uv.lock`, `examples/`, `docs/method.md` etc., all from WP4b and WP6 commits; see Outside the scope. |
| R-21 | met | Attribution grep 0; authors all Michael Zargham; CI green on every WP3 push. |

### Checks asked of the reviewer

**(a) sklearn conformance.** `LogAffinePreconditioner` passes `parametrize_with_checks` with `xfail_strict=True` and an empty expected-failure dict for four instances (default, `orientation=-1`, `orientation=-1, shift=0.5, scaler="robust"`, `scaler=None`). It follows the note: mixins on the left, `OneToOneFeatureMixin`, `__sklearn_tags__` with `positive_only=True`, no `_more_tags`, no `predict` or `score_samples`, verbatim `__init__`, negatives raise "Negative values in data". `TradeSpaceRegressor` passes with one expected failure. The reason is genuine: the installed sklearn 1.9.1 source for `check_regressor_multioutput` builds `y` with `make_regression(n_targets=5)` and never calls `_enforce_estimator_tags_y`, so it feeds negative y to an estimator that declares `target_tags.positive_only=True`; fitting a log-chart on negative y cannot succeed without abandoning the design. Multi-output shapes are covered by `test_predictive.py`. The deviation to note: the scope asked for an instance `LogAffinePreconditioner(orientation=[-1,1,1])`, and the delivered instances use scalar `orientation=-1`, because the checks fit several widths (comment in the test, scope allowed "otherwise the default only, with the reason in a comment"). The vector form is covered in `test_preconditioning.py` (`ColumnTransformer` with `[-1, 1]`).

**(b) Tension report.** I ran planted supports on seeds 3 and 4 (not the test seeds) in d=5. Sizes 2, 3, 4 and 5 give dilemma, trilemma, 4-lemma, 5-lemma and the exact supports at tau=inf. Working-tau weights differ: for the size-3 case at tau=5 the exponents were [0.4704, 0.3173, 0.1802, 0.0121, 0.0200] against the planted [0.5, 0.3, 0.2, 0, 0]. The free-metric weights at finite tau were 0.0 to 0.03 at tau=5 and 0.0 to 0.008 at tau=20: often exactly 0, otherwise tiny. The `min_exponent=0.05` estimator emits the UserWarning. `closure_note` is present. On a random cloud with no planted frontier (n=500, d=5) the LP support is all five metrics (a 5-lemma). Wording: honest. The module docstring, `api.md` and the field docs say that small working-tau weights mean "weak participation, not membership" and that exact membership is the tau=inf support. One caution for the reader: `participating` uses `threshold=1e-3`, so at finite tau a free metric with weight 0.01 or 0.02 is flagged `participating=True`; the report distinguishes this only through `contending_set`. See G-4.

**(c) R-4.** Confirmed: frac_above_ overshoots 0.5 at small tau (0.57 at tau=0.3) and is not monotone below tau of about 3. The test asserts monotonicity only for tau >= 3 and bounds the small-tau value to (0.4, 0.65); the test comment says so. This is a narrowing of the scope's "monotone nonincreasing from about 0.5 toward 0". The finding is real (the soft maximum tends to the mean of the scores, not the median), the monotone range is where the temperature is used (the estimator doc already says the useful range is 3 to 100), and `select_temperature` brackets and checks the ends. It is disclosed in the test but not in `docs/api.md` or the `select_temperature` docstring. See G-2.

**(d) R-13.** Confirmed: `make_configured_frontier_data` never exceeds log V = 0, so no beyond-frontier configuration is planted. The novelty test fits tau = 10, where the soft frontier lies below some exact-frontier points, and asserts predicted novelty > 0 for held-out true-frontier configurations and < 0 for those with true log V < −0.5. The module docstring states "held-out frontier configurations are predicted beyond the learned (soft) frontier", which is a fair description, but it does not say that no row genuinely beyond the true frontier was tested. The test shows the sign and ordering of novelty, not detection of a real beyond-frontier design. See G-3.

**(e) Docs.** `test_docs.py` (offline) checks bibliography keys, lemma tags 1 to 10, ledger ids against `derivation.axioms.AXIOMS`, and API coverage; all pass. The implementer's one flagged unsupported claim (`api.md` line 197: no cited source treats GP-restricted kernels) is stated in the text. The pages agree with `method.md` and `limitations.md` on K > 1 as documented not built, the closure effect, and R1. `preconditioning.md` discloses that a zero of a smaller-is-better attribute maps to metric 0 (the worst), though the attribute value is the best; users must shift. `preconditioning.md` line 162 says the cubesat orientation is "a vector of nine signs".

**(f) Nine-attribute case.** Scratch check at `/private/tmp/claude-501/s/f.py`: 9 columns, mixed orientation `[1,-1,-1,1,-1,1,-1,-1,1]`, log-normal data with widely differing scales (1e-2 to 1e3), robust scaler. Metrics strictly positive; round trip to 9e-16 (relative); `select_temperature` returned tau = 22.07; `frontier_in_original_units` matches `score_samples` to 6e-16; the sign of every original-unit exponent equals its orientation; `tension_report` returned a 9-lemma. The preconditioner handles the case in principle.

**(g) Trials.** (a) multiplying `exponents_orig` by 1.01 in `preconditioning.py`: 21 failures in `test_preconditioning.py`; (b) dropping the minus sign in `exchange_rates`: 3 failures in `test_tensions.py`. Both restored; `git status` clean.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-11 exist | met | See Deliverables |
| R-1 to R-21 pass as checked | met, with the deviations G-2 and G-3 | See Requirements |
| Non-goals untouched | met | No diff to `derivation/`, `solvers.py`, `coordinates.py`, `estimator.py`, `datasets.py`, `references.bib` from WP3 commits; only `__init__.py` exports; no K > 1 or kernel code (only documentation in `api.md`); no WP6, WP7 or WP4 content in WP3 commits |
| Expected-failures dict has a reason for every entry | met | Preconditioner dict empty; regressor dict has one entry with a reason, verified against the sklearn source |

## Outside the scope

- **Out-of-scope changes:** none in the WP3 commits (7f82d43, 348644c, ca095e5, 494145a, c793e10, 0815c82). The range diff `83f4038..HEAD` also shows `pyproject.toml` (a `case` dependency group), `uv.lock`, `examples/adcs/*`, `tests/test_cubesat_model.py`, `docs/superpowers/notes/adcs-tensions-probe.md` (WP4b), and `docs/method.md`, `limitations.md`, `why-and-how.md`, `tests/test_narrative.py`, the spec edit (WP6). These belong to other packages. The `pyproject.toml` change is not a WP3 test-option change; it is a WP4b change that now sits in the default groups, which makes `uv run pytest` depend on the `opensysml` install.
- **Non-goals touched:** none. `work-packages/README.md` still lists WP3 as "in progress"; the defaults list mentioned a status-table update after the documents, which has not happened.

## Observations (not counted as failures)

- The scalar-orientation instance in the compat tests differs from the scope's `[-1,1,1]` sample; the scope's own default permitted this with a stated reason.
- `TradeSpaceRegressor` requires strictly positive y, while the preconditioner tolerates zeros; a pipeline `trade_space` with zero attributes will be rejected at the regressor (documented in the error message).
- `predict_std` treats coordinate errors as independent and ignores the uncertainty of the chart fit (docstring says independence; the chart-fit part is not mentioned).
- The decisions file's date (2026-11-08) is a day after the commit's timestamp (2026-11-07 22:31 -0500); this is probably a UTC versus local-time difference.

## Open decisions (for the supervisor)

- **G-1.** The scope approval is a single "okay proceed" given for four gates at once and typed into the decisions file by the agent. Is this the approval the scope names? Options: accept as is / fix before acceptance / follow-up work package
- **G-2.** R-4 deviation: `frac_above_` is not monotone nonincreasing below tau of about 3 (overshoots 0.5); the test asserts monotonicity from tau of 3, and the scope said "monotone nonincreasing from about 0.5 toward 0". The deviation is disclosed only in a test comment. Options: accept as is / fix before acceptance / follow-up work package
- **G-3.** R-13 deviation: no genuinely beyond-frontier configuration is planted (the generator never exceeds log V = 0); the novelty test uses the tau = 10 soft frontier and shows sign and ordering only. Options: accept as is / fix before acceptance / follow-up work package
- **G-4.** Observations to accept as one item: `participating` at the default threshold flags free metrics at finite tau; `README.md` status table not updated; `pyproject.toml` default groups now include WP4b's `case`; scalar orientation in the compat instance; `predict_std` ignores chart-fit uncertainty. Options: accept as is / fix before acceptance / follow-up work package

## Gap dispositions

Each gap is resolved through the decision loop (`~/.claude/skills/CLAUDE.md`). Decision records go in `work-packages/WP3-decisions.md`.

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 | pending | |
| G-2 | pending | |
| G-3 | pending | |
| G-4 | pending | |

## Recommendation

Provisional, pending the gap dispositions: recommend acceptance with the listed gaps noted, because every requirement R-1 to R-21 passed when I ran it, the full suite (843 passed), ruff, the lock check and CI are green, the planted-support recovery for sizes 2 to 5 is exact at tau=inf and the tension report is honest about weak participation, the single expected failure has a genuine reason, no non-goal was touched, and the trials (perturbed pull-back exponent, flipped exchange-rate sign) fail the tests as they should. The two deviations (R-4 monotone range, R-13 novelty without a planted beyond-frontier row) narrow what two tests show, and the supervisor should decide whether they are acceptable.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
