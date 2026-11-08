# WP3 — Scope of work: Conditioning, prediction and analysis toolkit

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP3-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP3-decisions.md`, after the review report `work-packages/WP3-review.md` |

## Purpose

WP2 delivered the identification stage (`HyperbolicTradeSpace`). The method's other stages are the analyst's
conditioning of attributes into metrics (stage 2) and the analysis built on the learned chart (stage 4): choosing the
temperature, finding holes and targets, reading the tensions that define the trade-offs, predicting where a proposed
configuration would fall, and plotting. WP3 builds these as scikit-learn-compatible tools, and writes the two documents
that explain them (`docs/preconditioning.md`, `docs/api.md`), so that the case notebook (WP7) needs nothing but data and
interpretation. The supervisor's framing (spec §2, "Tensions, not variance") is carried by a new tension report: the model
finds the tensions that define the trade-offs, as PCA finds variance components.

## Goals

- G1. A log-affine preconditioner that conditions positive-valued attributes into larger-is-better metrics, invertibly, and a function that pulls the learned frontier back to original attribute units (spec §5 `preconditioning.py`; WP1 L9).
- G2. Temperature selection by bisection to a target `frac_above_` (spec §5 `tuning.py`).
- G3. Gap and white-space tools: k-NN gap scores, hole finding in the chart, frontier targets mapped back to metrics and attributes, and PCA orientation of near-frontier coordinates (spec §5 `gaps.py`).
- G4. A tension report that states which metrics are in tension, which are aligned, the principal tension directions, and the contending set discovered by the fit, an n-lemma of any size n (spec §2, "Tensions, not variance" and "n-lemmas are discovered, not assumed").
- G5. `TradeSpaceRegressor`: prediction from configuration as a supervised composition (spec §4, §5 `predictive.py`).
- G6. Plotting helpers with one documented visual vocabulary (spec §5 `plotting.py`).
- G7. scikit-learn conformance for the preconditioner and the regressor (spec §7, conformance note).
- G8. Two documents: `docs/preconditioning.md` and `docs/api.md` (as built, and as it extends to K > 1 and kernel methods), each claim citing a WP1 lemma or ledger entry or a WP5 bibliography key.

## Non-goals

- No change to WP1 or WP2 deliverables (`derivation/`, `solvers.py`, `coordinates.py`, `estimator.py`, `datasets.py`) except adding exports to `__init__.py`; if a defect in them is found, stop and propose an amendment.
- No K > 1 solver and no kernel methods; `docs/api.md` documents their API shape only (spec §4).
- No mathematics narrative, why/how page or limitations page (WP6), notebook (WP7), ADCS data or code (WP4, WP7), site or MkDocs configuration (WP8).
- No interactive plotting and no new plotting dependency (matplotlib only).
- No automatic discovery of several regional tensions or successive tensions by deflation: the tension report describes the K = 1 fit only (a research question for later, spec §2).
- No new bibliography entries except as needed for a cited claim, added under the WP5 hygiene rules (resolved by DOI or stable URL, `verified` field, test passes).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `src/hyperbolic_trade_space/preconditioning.py`: `LogAffinePreconditioner`, `frontier_in_original_units` | G1, G7 |
| D-2 | `src/hyperbolic_trade_space/tuning.py`: `select_temperature` | G2 |
| D-3 | `src/hyperbolic_trade_space/gaps.py`: `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca` | G3 |
| D-4 | `src/hyperbolic_trade_space/tensions.py`: `tension_report` and its result type | G4 |
| D-5 | `src/hyperbolic_trade_space/predictive.py`: `TradeSpaceRegressor` | G5, G7 |
| D-6 | `src/hyperbolic_trade_space/plotting.py` | G6 |
| D-7 | `docs/preconditioning.md` | G1, G8 |
| D-8 | `docs/api.md` | G1–G8 |
| D-9 | Tests: `tests/test_preconditioning.py`, `test_tuning.py`, `test_gaps.py`, `test_tensions.py`, `test_predictive.py`, `test_plotting.py`, `test_docs.py`, and the preconditioner and regressor instances added to `tests/test_sklearn_compat.py` | G1–G8 |
| D-10 | Package exports in `src/hyperbolic_trade_space/__init__.py` | G1–G6 |
| D-11 | `work-packages/WP3-decisions.md` (approval record) | G1–G8 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `LogAffinePreconditioner(orientation, shift, scaler)` computes z = o·log(X + shift), fits the scaler on finite z, and transforms to exp(scaled z) with zeros mapping to 0; `inverse_transform` is exact; fitted `scaler_`, `log_scale_`, `log_offset_`, `orientation_`, `shift_` exist; round trip holds to 1e-10 with mixed orientation (+1 larger-is-better, −1 smaller-is-better) and nonzero shift | `uv run pytest tests/test_preconditioning.py` |
| R-2 | After conditioning, each metric column has unit log-standard-deviation (for `scaler="standard"`) over its finite entries; with `scaler="robust"` the log-IQR is normalized; negatives (after shift) raise `ValueError` "Negative values in data" | `test_preconditioning.py` |
| R-3 | `frontier_in_original_units(estimator, preconditioner)` returns `dict(exponents_orig, log_const, shift)` and, evaluated on raw attributes, reproduces the pipeline's `score_samples` (preconditioner then estimator) to 1e-9; it agrees with the WP1 L9 pull-back formula V = e^{w·b − β} Π (a_j + s_j)^{w_j α_j} evaluated from the ctx | `test_preconditioning.py` (cross-check against the chain, labelled) |
| R-4 | `select_temperature(X, target_frac_above=0.10, bounds, tol, **params)` bisects log τ and returns a temperature whose fitted `frac_above_` is within `tol` of the target on planted data; a τ sweep shows `frac_above_` monotone nonincreasing from about 0.5 toward 0 and `n_eff_` moving from N toward d | `test_tuning.py` |
| R-5 | `knn_gap_scores(Z, k)` returns one score per point and flags an isolated planted point; `find_holes(Z, resolution, threshold)` finds a planted disc hole in 2-D charts and a planted gap in 1-D, restricts to the hull (`Delaunay.find_simplex`), and supports d−1 ∈ {1, 2, 3}, raising `ValueError` otherwise | `test_gaps.py` |
| R-6 | `frontier_targets(Z_points, estimator, preconditioner=None)` maps (Z, log V = 0) to metrics, and to attributes when a preconditioner is given; the returned points have V = 1 and round-trip to the same Z | `test_gaps.py` |
| R-7 | `orient_by_pca(Z, mask)` returns a rotation of the chart coordinates oriented by PCA of the masked (near-frontier) rows, with the sign convention fixed; it equals the `tension_report` principal directions when called on the same rows | `test_gaps.py`, `test_tensions.py` |
| R-8 | `tension_report` part 1: lists metrics with w_j > threshold as participating and the rest as free, the exponents, and the matrix of exchange rates (the elasticity −w_k/w_j of WP1 L7); the rows are consistent with the fitted `exponents_` | `test_tensions.py` |
| R-8a | `tension_report` also reports the contending set at τ = ∞: the support of the LP solution computed from the same data with `min_exponent = 0` (exact zeros), alongside the working-τ weights, labelled as the discovered n-lemma at the balanced point with n the size of the support (n = 1, 2, 3, ... for any d, with no prior choice of which metrics or how many); it states that `min_exponent` must be 0 for this reading and warns if the fitted estimator has `min_exponent > 0`; the report distinguishes exact membership (τ = ∞) from weak participation (small working-τ weights) | `test_tensions.py`: planted frontiers whose true normals have support size 2, 3 and 4 in d = 5, and one with a free metric (w_j = 0), recover the planted supports at τ = ∞ and show smoothed weights at finite τ; the warning test for `min_exponent > 0` |
| R-9 | `tension_report` part 2: for near-frontier designs (|log V| < band), computes the pairwise association (sign and strength) of log-metrics; on planted data with a designated traded pair and a designated aligned pair, the traded pair has negative association and the aligned pair positive association, with margins stated in the test; the report states the closure effect (a binding constraint induces negative association among participating metrics) in its docstring | `test_tensions.py` |
| R-10 | `tension_report` part 3: PCA of the near-frontier Z coordinates, with principal tension directions, explained spread, and loadings mapped back to metrics through the chart basis; on planted data whose frontier spread is concentrated in a known direction, the first direction recovers it within a stated angle | `test_tensions.py` |
| R-11 | `tension_report` handles degenerate input explicitly: fewer than a stated minimum number of near-frontier points raises or warns as documented, d = 1 returns the trivial report, and a `band` default of 1/τ (0.1 at τ = ∞) is documented; the report is deterministic | `test_tensions.py` |
| R-12 | `TradeSpaceRegressor(regressor, trade_space)` follows the regressor contract: `fit(X_config, Y_metrics)` fits `trade_space` on Y then `regressor` on X → chart coordinates; `predict` returns metrics via `inverse_transform`; `predict_coordinates` returns (Z, log V); `predict_novelty` returns V − 1; `predict_std` works when the regressor supports `return_std`; `score` is R² in coordinate space, documented; no sample-order dependence | `test_predictive.py` |
| R-13 | Prediction on planted configuration data (`make_configured_frontier_data`): predicted log V and Z match held-out truth within stated tolerances; a planted beyond-frontier configuration gets predicted novelty > 0; `predict_std` plumbing is exercised with a Gaussian-process or bootstrap regressor | `test_predictive.py` |
| R-14 | `TradeSpaceRegressor` is interoperable with `sklearn.compose.TransformedTargetRegressor` (2-D y handling verified) or the test documents why the wrapper is used instead | `test_predictive.py` |
| R-15 | `parametrize_with_checks(..., expected_failed_checks=..., xfail_strict=True)` passes for `LogAffinePreconditioner` (default and with orientation) and `TradeSpaceRegressor` with a linear regressor, added to `tests/test_sklearn_compat.py` beside the WP2 instances; the expected-failures dict is explicit, every entry carries a written reason, and the goal is empty | `uv run pytest tests/test_sklearn_compat.py`; inspect the dict |
| R-16 | Each plotting function (`plot_frontier_surface_3d`, `plot_log_plane`, `plot_frontier_coordinates`, `plot_v_by_variable`, and one for the tension report) returns a matplotlib `Axes`, runs headless with the Agg backend, and uses the documented visual vocabulary of the module docstring | `test_plotting.py` (smoke) and inspection |
| R-17 | `docs/preconditioning.md` explains the conditioning stage (orientation, reference point, scaling, invertibility, diagnostics, the pull-back to attributes) in discursive prose; every load-bearing claim cites a lemma tag (L1–L10) or a ledger id (A1–A7, I1–I6, R1, F5, F10) or a bibliography key in the `[@key]` form | `test_docs.py`; inspection |
| R-18 | `docs/api.md` documents the public API as built (every exported name, its role, its stage) and as it extends to K > 1 and kernel methods (`n_terms`, `term_temperature`, `exponents_` of shape (n_terms, d), `log_offset_`, Φ-based definitions so any term set plugs in), citing WP5 keys for the posynomial/GGP and kernel literature, and states that the extensions are documented, not built | `test_docs.py` (every exported public name appears in `api.md`; every cited key and lemma tag resolves); inspection |
| R-19 | Numpydoc docstrings (Parameters, Attributes, Returns, Notes, Examples) on every public class and function, with doctests that run under the default `uv run pytest` | `uv run pytest`; inspection |
| R-20 | The whole suite, linters and lock pass and nothing outside scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff --stat <start>..HEAD` shows changes only to the deliverable paths, `pyproject.toml` (only if a test option needs it), `docs/references.bib` (only per the non-goal exception) and `work-packages/` | run the commands; inspect the diff |
| R-21 | No AI attribution lines; commits authored as Michael Zargham; CI green on every push | `git log` grep returns 0; `gh run list` |

## Definition of good

- A reader of `tension_report` output understands the trade-off structure of a data set at a glance: which metrics pull against each other, which move together, and along which directions designs have actually traded.
- The tension report states its own limits: K = 1 finds one tension; the closure effect on pairwise association; the dependence on the band; the difference between a tension (a binding constraint) and a mere correlation.
- Prediction is honest about inherited error: coordinates, not metrics, are the regression target; novelty predictions carry the surrogate's uncertainty where it exists.
- The documents are discursive and traceable: an interested reader can follow every claim to a lemma, a ledger condition or a source, and sees the conditions under which the tools mislead (R1, conditioning choices, strata).
- The toolkit composes with scikit-learn the way an analyst would expect (pipelines, `ColumnTransformer`, `TransformedTargetRegressor`).

## Definition of good enough

- Deliverables D-1 to D-11 exist at the stated paths.
- R-1 to R-21 pass as checked, with evidence in the review report.
- Non-goals untouched (no WP1/WP2 changes beyond exports, no K > 1 or kernel code, no WP6 or WP7 content).
- The expected-failures dict, if non-empty, has a stated reason for every entry.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item. Execution waits for WP2's acceptance.

- Module layout as spec §5 plus `tensions.py`; exports in `__init__.py`: `LogAffinePreconditioner`, `frontier_in_original_units`, `select_temperature`, `TradeSpaceRegressor`, `tension_report`; the `gaps` and `plotting` functions are used through their submodules *(default)*.
- `LogAffinePreconditioner(orientation=None, shift=0.0, scaler="standard")` per spec §5: `orientation` is a sequence of ±1 per column (default all +1), `shift` a scalar or per-column array, `scaler` in {"standard", "robust", None} or a scikit-learn scaler instance; `OneToOneFeatureMixin` and `TransformerMixin`; tags `positive_only=True` (zeros tolerated, negatives raise `check_non_negative` "Negative values in data") *(default)*.
- `frontier_in_original_units` returns exponents on the raw attributes (w_j α_j), the log constant (w·b − β) and the shift; documented as the closed form of WP1 L9 *(default)*.
- `select_temperature` by bisection on log τ within `bounds=(1e-1, 1e4)`, at most 60 iterations, monotonicity assumed and checked at the bracket ends; returns the temperature; raises `ValueError` if the target is not bracketed *(default)*.
- Gap tools *(default)*: `knn_gap_scores` uses `scipy.spatial.cKDTree` (mean distance to the k nearest neighbours, normalized by the median); `find_holes` evaluates a regular grid of `resolution` points per axis over the bounding box, keeps cells inside the hull, scores them by distance to the nearest data point and marks holes above `threshold` times the median nearest-neighbour distance; `frontier_targets` takes Z points, sets log V = 0 and maps back through `from_frontier_coordinates` and, if given, the preconditioner's inverse.
- `orient_by_pca(Z, mask)` returns `(Z_rotated, components, explained_variance_ratio)`, with component signs fixed so the largest-magnitude loading is positive *(default)*.
- Tension report *(default)*:
  - `tension_report(estimator, X, band=None, min_near_frontier=10, threshold=1e-3) -> TensionReport` (a frozen dataclass).
  - `band=None` means 1/τ for finite τ and 0.1 at τ = ∞.
  - Part 1: `participating` (bool per metric, w_j > threshold), `exponents`, `exchange_rates` (matrix of −w_k/w_j, NaN where w_j = 0).
  - Contending set *(default)*: `contending_set` (indices where the τ = ∞ LP exponent exceeds 1e-9), `contending_exponents` (the LP exponents), `n_lemma` (the support size), `lemma_name` ("monolemma" for 1, "dilemma", "trilemma", then "n-lemma" with n spelled as a number), plus the working-τ `exponents` for comparison; the LP is solved with `solvers.solve_lp(U, min_exponent=0.0)` on the log of the estimator's training rows, independent of the fitted τ and `min_exponent`; a `UserWarning` is issued when `estimator.min_exponent > 0` because the working weights are floored.
  - Part 2: `association` is the Pearson correlation matrix of the log-metrics among near-frontier rows (|log V| < band); negative means tension, positive aligned; a `closure_note` string states the closure effect; Spearman is optionally available through an `association="spearman"` argument.
  - Part 3: `tension_directions` (unit vectors in Z), `tension_loadings` (the same directions mapped back to metrics through `basis_`), `explained_spread`.
  - Fewer than `min_near_frontier` near-frontier rows raises `ValueError` with a message suggesting a larger band or temperature; d = 1 returns a trivial report with empty directions.
  - Tests build planted data inside the test module with a chosen Z covariance and `coordinates.from_frontier_coordinates` (no change to `datasets.py`).
- `TradeSpaceRegressor(regressor, trade_space)`: `trade_space` is cloned at fit; `regressor` is cloned and fitted on X → `trade_space.transform(Y)`; for a single metric (d = 1) a 1-D y is accepted and reshaped; target tags `target_tags.positive=True` and `multi_output` handled to satisfy the regressor checks; `predict_std` returns the regressor's standard deviation propagated to metrics by the delta method only when the regressor supports `return_std`, otherwise raises `AttributeError` *(default)*.
- Regressor `score` is R² in coordinate space, uniform average over coordinates *(default)*.
- Plotting *(default)*: all functions accept an optional `ax`, return it, import matplotlib lazily, and share a vocabulary declared in the module docstring and constants (frontier V = 1 in black, near-frontier band in grey, holes in red, targets as open markers, categories from one qualitative palette); functions: `plot_frontier_surface_3d`, `plot_log_plane`, `plot_frontier_coordinates(Z, log_v, color=None, holes=None)`, `plot_v_by_variable`, `plot_tensions(report)`.
- Docs *(default)*: Markdown with LaTeX; lemma tags written `L<n>` and ledger ids as `A1`, `R1`, `F5`; citations as `[@key]` using keys already in `docs/references.bib`; `test_docs.py` checks that every `[@key]` resolves to the bib, every `L<n>` is in 1..10, every ledger id exists in `derivation/axioms.py`, and every exported public name is mentioned in `docs/api.md`.
- Tolerances *(default)*: recovery tolerances stated in each test file; seeds 0, 1, 2; band-related tests use planted data with n ≥ 400.
- sklearn compat additions *(default)*: instances `LogAffinePreconditioner()`, `LogAffinePreconditioner(orientation=[-1, 1, 1])` where the check data allows (otherwise the default only, with the reason in a comment), and `TradeSpaceRegressor(LinearRegression(), HyperbolicTradeSpace())`; `expected_failed_checks` starts empty.
- Numpydoc docstrings with seeded doctests; ruff unchanged; commits prefixed "WP3: ", one commit per module with its tests, then the documents, then the status table and decisions file; every push green and attribution-free (CI rejects both) *(default)*.
- Order *(default)*: preconditioning, tuning, gaps, tensions, predictive, plotting, docs, compat tests; TDD per module.

## Open decisions (for the supervisor)

None at problem level: spec §2 (including "Tensions, not variance"), §4, §5, §7, the conformance note and the confirmed breakdown answer them. The Agent's defaults list above is the one item for the supervisor to approve or change at the scope gate.
