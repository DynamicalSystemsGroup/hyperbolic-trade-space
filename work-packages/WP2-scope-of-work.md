# WP2 — Scope of work: Core estimator (solvers, chart, PosynomialInvariantForm)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP2-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP2-decisions.md`, after the review report `work-packages/WP2-review.md` |

## Purpose

WP1 fixed the mathematics (log-mean-exp objective, gradient, convexity, simplex chart, invariant form). WP2 builds the
numerical core and the scikit-learn estimator that implements it for K = 1 (monomial), so that conditioning,
prediction, analysis, the case study and the documentation (WP3, WP4, WP7, WP8) have a working, conformant
`PosynomialInvariantForm` to build on. The estimator must match the derivation chain's formulas; the chain grounds
and interprets it, and where the implementation departs from a hypothesis of the chain (for example R1, or a finite
sample), the departure is reported as a diagnostic, not hidden.

## Goals

- G1. Solvers (spec §5 `solvers.py`) compute the entropic soft-maximum fit: β is the log-mean-exp, w* the minimizer over the simplex, with support weights, by an LP at τ = ∞ and a warm-started SLSQP at finite τ.
- G2. Coordinates (spec §5 `coordinates.py`) provide an invertible chart (log V and d−1 log-ratio coordinates Z) from an ILR basis satisfying the L8/A7 hypotheses (B Bᵀ = I, B 1 = 0) and an ALR alternative.
- G3. `PosynomialInvariantForm` (spec §5 `estimator.py`) is a decomposition-style scikit-learn transformer with the domain methods `invariant_value`, `novelty_score`, `project`, `improvement_factors`, `level_set`, K = 1 only, and the documented fitted attributes and diagnostics.
- G4. The estimator conforms to scikit-learn per spec §7 and `docs/superpowers/notes/sklearn-conformance.md`, checked by `parametrize_with_checks`.
- G5. Synthetic frontier data generators (spec §5 `datasets.py`) support recovery and shape tests, and the predictive tests of WP3.
- G6. The implementation is shown to match the WP1 derivation chain numerically (a cross-check, not a re-proof).

## Non-goals

- No `LogAffinePreconditioner`, `frontier_in_original_units`, `select_temperature`, `TradeSpaceRegressor`, `gaps.py` or `plotting.py` (WP3).
- No K > 1 solver and no kernel methods: `n_terms != 1` raises `NotImplementedError` (spec §2).
- No documentation pages, notebook, ADCS code or site (WP3, WP4, WP6, WP7, WP8); docstrings and doctests are in scope.
- No change to `derivation/` or to the spec; if a formula in the spec or the chain turns out wrong, stop and propose an amendment. Reconciling the spec's per-lemma axiom lists with the WP1 ledger is WP6's job.
- No `predict`, `decision_function` or `score` on the estimator (spec §2, §7).
- No new runtime dependencies beyond those in `pyproject.toml` (numpy, scipy, scikit-learn, pandas, matplotlib, sympy).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `src/posynomial_invariant_form/solvers.py` | G1 |
| D-2 | `src/posynomial_invariant_form/coordinates.py` | G2 |
| D-3 | `src/posynomial_invariant_form/estimator.py` and package exports in `__init__.py` | G3, G4 |
| D-4 | `src/posynomial_invariant_form/datasets.py` | G5 |
| D-5 | `tests/test_solvers.py`, `test_coordinates.py`, `test_datasets.py`, `test_estimator.py` | G1–G3, G5 |
| D-6 | `tests/test_sklearn_compat.py` | G4 |
| D-7 | `tests/test_matches_derivation.py` | G6 |
| D-8 | `work-packages/WP2-decisions.md` (approval record) | G1–G6 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `log_mean_exp(s, tau)` equals the naive `log(mean(exp(tau*s)))/tau` where the naive form is finite, is stable for large `tau*s`, and returns `max(s)` at `tau = inf`; `support_weights` is the softmax (at `tau = inf` argmax with ties averaged), nonnegative and summing to 1 | `uv run pytest tests/test_solvers.py` |
| R-2 | `objective_and_grad(w, U, tau)` returns the objective and the gradient `Uᵀ p`; the gradient passes `scipy.optimize.check_grad` | `test_solvers.py` |
| R-3 | `solve_lp` solves min t s.t. U w ≤ t·1, Σw = 1, w ≥ min_exponent on a hand-built problem with a known answer; the duals are the support weights and sum to 1 | `test_solvers.py` |
| R-4 | At τ = 1e3 the SLSQP solution agrees with the LP solution; `SolveResult` carries `w, beta, p, objective, n_iter, success, message` | `test_solvers.py` |
| R-5 | The basis functions return `B` with `B Bᵀ = I` and `B 1 = 0` for ILR (Helmert) at d = 2..8 to 1e-12; the ALR chart is invertible; `from_frontier_coordinates(to_frontier_coordinates(U)) = U` to 1e-12; Z is invariant to `u + c·1`; `d = 1` gives Z with zero columns | `test_coordinates.py` |
| R-6 | `make_frontier_data` returns `(X, info)` with the planted exponents, log offset, chart, frontier mask and noise level in `info`, is reproducible for a fixed `random_state`, and has all X positive; `make_configured_frontier_data` also returns the known configuration → metrics map | `test_datasets.py` |
| R-7 | Recovery: on planted frontiers for d ∈ {2,3,5}, the fitted `exponents_` agree with the planted w within 1e-6 at τ = inf and within 2e-2 at τ = 1e3 | `test_estimator.py` |
| R-8 | Fit invariants: `exponents_` on the simplex and ≥ `min_exponent`; `support_weights_` ≥ 0 and sum 1; 1 ≤ `n_eff_` ≤ N; at τ = inf `frac_above_` = 0 and max V ≤ 1 + 1e-9; at finite τ 0 < `frac_above_` < 0.5 | `test_estimator.py` |
| R-9 | Shape tests: uniform rescaling shifts β by log k and leaves w and V unchanged; row replication leaves the fit unchanged; interior-density changes leave the fit unchanged at τ = inf (and within tolerance at large τ); permutation equivariance; Gaussian noise offset of β ≈ τσ²‖w‖²/2 within a stated tolerance | `test_estimator.py` |
| R-10 | Chart and domain methods: `inverse_transform(transform(X))` returns X to 1e-9; `transform(X)[:, -1]` equals `score_samples(X)`; `invariant_value(project(X))` = 1; applying `improvement_factors` to the corresponding metric lands on V = 1; points from `level_set(Z, value)` have V = value and map back to the same Z | `test_estimator.py` |
| R-11 | Novelty: `novelty_score(X)` = V − 1; with `calibrated=True` returns the rank among training log V and τ·log V; the leave-one-out super-efficiency test (remove a frontier point, refit at τ = inf, it scores ≥ 1) passes | `test_estimator.py` |
| R-12 | Edge cases: d = 1 works (Z has no columns); a zero metric gives V = 0, log V = −∞, support weight 0 and the row is excluded from the objective; negative values raise `ValueError` matching "Negative values in data"; NaN/inf raise `ValueError`; `n_terms=2` raises `NotImplementedError` | `test_estimator.py` |
| R-13 | Composition: the estimator works in a `Pipeline` and behind a `ColumnTransformer` that passes metric columns to it and other columns through as covariates; `get_feature_names_out` returns `ilr0.., log_v` (or `alr0..`) of the transform width | `test_estimator.py` |
| R-14 | The estimator has no `predict`, `decision_function` or `score`; has `score_samples`, `transform`, `inverse_transform`, `fit_transform`, `get_feature_names_out`; sets tags only through `__sklearn_tags__` (`positive_only=True`, not sparse); `__init__` stores parameters verbatim and validation happens in `fit`; fitted attributes end in `_`; `n_iter_` ≥ 1 on both the LP and SLSQP paths | `test_sklearn_compat.py` and inspection against the conformance note |
| R-15 | `parametrize_with_checks(..., expected_failed_checks=..., xfail_strict=True)` runs over the estimator at default settings, at `temperature=inf` and at `coordinates="alr"`; the expected-failures dict is explicit, each entry has a written reason, and the goal is empty | `uv run pytest tests/test_sklearn_compat.py`; inspect the dict |
| R-16 | Match to the derivation chain: for seeded small instances, the solver's objective, gradient and offset, the chart relations, the improvement factor and V agree with the corresponding WP1 ctx expressions (L1, L2, L3, L5, L7, L8) numerically to 1e-10; this is labelled a cross-check of the implementation against the chain | `uv run pytest tests/test_matches_derivation.py` |
| R-17 | Numpydoc docstrings (Parameters, Attributes, Returns, Notes, Examples) on every public class and function; the examples run as doctests | `uv run pytest` (doctest-modules is enabled) and inspection |
| R-18 | The whole suite, linters and lock pass and nothing outside scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff --stat <start>..HEAD` shows changes only to the deliverable paths, `pyproject.toml` (only if a test dependency or option needs it), `work-packages/` and the Status table | run the commands; inspect the diff |
| R-19 | No AI attribution lines; commits authored as Michael Zargham | `git log --format=%B \| grep -ciE 'co-authored-by\|generated with'` returns 0; CI check |

## Definition of good

- The code reads as the spec and the chain: names match (`exponents_`, `log_offset_`, `support_weights_`, `n_eff_`, `frac_above_`), formulas are visibly the ones of L1–L10, docstrings point to the lemma that grounds each formula.
- Departures from the chain's hypotheses are surfaced as diagnostics (`n_eff_`, `frac_above_`, a check on R1-type degeneracy such as exponents on the floor) rather than silently assumed.
- Numerically robust: no overflow at large τ, zeros handled, deterministic.
- The expected-failures dict of the scikit-learn checks is empty.
- The code is small and flat; the solver layer has no scikit-learn dependency.

## Definition of good enough

- Deliverables D-1 to D-8 exist at the stated paths.
- R-1 to R-19 pass as checked, with evidence in the review report.
- Non-goals untouched (no preconditioner, tuning, gaps, plotting, regressor, K > 1 code).
- The expected-failures dict, if non-empty, has a stated reason for every entry.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item.

- Estimator class name `PosynomialInvariantForm` *(default; the spec lists a rename such as `HyperbolicTradeSpace` as an option at this gate; this scope keeps the spec's name)*.
- Public exports in `__init__.py`: `PosynomialInvariantForm`, `make_frontier_data`, `make_configured_frontier_data`, `__version__`; `solvers` and `coordinates` are imported as submodules, not re-exported *(default)*.
- `temperature` accepts a float > 0 or `np.inf`; `min_exponent` in [0, 1/d); `coordinates` in {"ilr", "alr"}; `n_terms` an int ≥ 1; `tol` > 0; `max_iter` ≥ 1; all validated in `fit` with `ValueError` *(default)*. `term_temperature` is stored and ignored for K = 1 *(default)*.
- Parameter defaults exactly as spec §5: `temperature=10.0, min_exponent=0.0, coordinates="ilr", n_terms=1, term_temperature=np.inf, tol=1e-10, max_iter=500` *(default)*.
- `n_terms != 1` raises `NotImplementedError("n_terms > 1 is a documented extension (spec section 4); only n_terms=1 is implemented")` from `fit` *(default)*.
- `SolveResult` is a frozen dataclass with the spec's fields *(default)*; `solve_lp` uses `scipy.optimize.linprog(method="highs")` and takes the duals from `res.ineqlin.marginals` (sign and normalization fixed so they are the support weights) *(default)*.
- `support_weights` at τ = inf: ties detected with relative tolerance 1e-12 and averaged *(default)*.
- Zero metrics: rows with any zero entry get u = −∞ and are masked from the solver; their V = 0, log V = −∞, p = 0; `frac_above_` and `n_eff_` are computed over unmasked rows; if every row is masked, `fit` raises `ValueError` *(default)*. Minimum samples: `ensure_min_samples=1`; with 1 sample the fit returns the balanced exponents and the single row has V = 1 *(default)*.
- `d = 1` shortcut: `exponents_ = [[1.0]]`, β = log-mean-exp of u at the given τ, Z has zero columns, `transform` returns the single column `log_v` *(default)*.
- Charts: ILR rows are the Helmert basis `(1,…,1,−k,0,…)/√(k(k+1))`, as used in the WP1 realization check; ALR uses the last metric as the reference (Z_j = u_j − u_d, j < d), which is invertible but not orthonormal, so only ILR satisfies the L8/A7 hypotheses *(default)*. Feature names `ilr0..ilr{d-2}` or `alr0..alr{d-2}` then `log_v` *(default)*.
- `transform` returns `[Z | log V]` in the original metric columns' order; `inverse_transform` maps back to metric values via `from_frontier_coordinates` and exponentiates; rows with log V = −∞ are not invertible and give NaN in Z, which is documented *(default)*.
- `project(X)` = X / V, with NaN rows where V = 0 *(default)*. `invariant_value` = exp(log V). `improvement_factors` returns an (n, d) array V^{−1/w_j}, with `inf` where w_j = 0 or V = 0 *(default)*.
- `novelty_score(X, calibrated=False)` = V − 1; with `calibrated=True` returns an (n, 2) array: the empirical fraction of training log V that are ≤ the query's (right-sided), and τ·log V (log V itself when τ is infinite) *(default)*.
- `level_set(Z, value=1.0)` takes Z of shape (n, d−1) and returns metric points (n, d) with V = `value` (log V = log value) *(default)*.
- Fit diagnostics definitions *(default)*: `support_weights_` = softmax weights at the solution (LP duals at τ = ∞); `n_eff_` = 1/Σp²; `frac_above_` = fraction of training rows with V > 1 (strict, with tolerance 1e-9 at τ = ∞); `objective_` = J_τ at w* (β); `log_offset_` = [β]; `basis_` = the chart matrix; `training_log_v_` = log V of the training rows; `n_iter_` = SLSQP iterations, and 1 on the LP-only path.
- Algorithm *(default)*: always solve the LP first; if τ is finite run SLSQP from the LP solution with analytic Jacobian, `ftol=tol`, `maxiter=max_iter`; always compute via `scipy.special.logsumexp(tau*s, b=1/N)/tau`.
- `make_frontier_data` follows spec §5 exactly (Z ~ N(0, I), frontier rows log V = noise·N(0,1), interior rows log V = −Exp(`interior_scale`), mapped back through the ILR chart; planted exponents default to a seeded random simplex point bounded away from the boundary; `info` keys `exponents, log_offset, basis, frontier_mask, Z, log_v`) *(default)*. `make_configured_frontier_data(n_samples, n_features, n_config, ...)` returns `(X_config, Y_metrics, info)` where the metrics are a known smooth map of the configuration (log-affine plus a small nonlinear term) plus frontier structure *(default)*.
- Test tolerances and seeds as in spec §5 where stated; otherwise fixed seeds (0, 1, 2) and tolerances stated in the test file *(default)*. Gaussian-noise offset test uses N ≥ 20000 and rtol 5e-2 *(default)*.
- `tests/test_matches_derivation.py` imports `derivation` through the existing `pythonpath` setting, builds the WP1 ctx once via `run_chain(verbose=False)`, and substitutes seeded values (d = 3, n = 5) into the stored expressions *(default)*.
- sklearn compat: three parametrized instances (default; `temperature=np.inf`; `coordinates="alr"`); `expected_failed_checks` starts empty and each entry added must carry a reason; the preconditioner and regressor instances are added to this file in WP3 *(default)*.
- Docstring style numpydoc; doctests use fixed seeds and print rounded values *(default)*.
- Ruff configuration unchanged (line length 100); commits prefixed "WP2: "; one commit per module with its tests, then the compatibility tests, then the status table and decisions file; decisions file `work-packages/WP2-decisions.md` and review file `work-packages/WP2-review.md` follow the WP1 format *(default)*.
- Implementation order *(default)*: solvers, coordinates, datasets, estimator, compat tests, matching tests, TDD per module; main stays green on every push (CI rejects red builds and attribution lines).

## Open decisions (for the supervisor)

None at problem level: spec §2, §5 and §7, the conformance note and the confirmed breakdown answer them. The Agent's defaults list above is the one item for the supervisor to approve or change at the scope gate.
