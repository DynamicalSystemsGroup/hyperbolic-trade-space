# Design spec: posynomial-invariant-form

Date: 2026-11-07. Supervisor and author of the method: Michael Zargham (`mzargham`). This document
is the persisted form of the approved plan. Executing agents read it together with the notes in
`docs/superpowers/notes/`, the procedure in `work-packages/README.md`, and the repo `CLAUDE.md`.

## 1. Intent

A method for large-scale trade studies. Less like regression, more like feature engineering: from
noisy, biased observations of a design problem it learns a hyperbolic "space", a nonlinear subspace
characterizing the trade-offs, built from a multiplicative combination of the metrics instead of a
linear one. The data are configuration variables (features) concatenated with empirically assessed
attributes. Metrics are conditioned to be strictly positive, larger-is-better and similarly
scaled; the admissibility set is modelled in log-metric space; the frontier is the unit level set
of a monomial V(m) = Π_j m_j^{w_j} (a generalized hyperbolic surface in metric space, a hyperplane
in log space), uncovered by generalized-geometric-program fitting to level sets. The learned
coordinates are log V (distance from the frontier) and d−1 log-ratio coordinates Z (position along
it). Uses: level sets, holes (white space), novelty of a concept (V − 1), prediction of where a
proposed configuration would fall, and reading the frontier's shape back in design variables.

## 2. Decisions (settled with the supervisor; do not relitigate)

- **Model.** Posynomial frontier; K = 1 (monomial) solver first because it is easiest. K > 1 is a
  generalized geometric program (GGP) needing a different solver: API and mathematics documented as
  the extension, not built. Research direction: kernel methods, admissible only while the programs
  remain GGPs; documented with supporting literature. Architecture must not preclude either.
  "Invariant form" = the normalized representation in which the frontier is exactly V = 1.
- **Fit.** Soft supporting hyperplane: w* = argmin over the simplex of the log-mean-exp (entropic)
  soft maximum of w·u over the data; β = that minimum (§4 says why log-mean-exp).
- **Generality.** Arbitrary d; arrays and indexed symbols everywhere, never x,y,z / a,b,c in code.
- **Scope.** The package covers identification and analysis. Prior stages are described by domains
  and codomains; the example fills them with existing scientific-Python tools.
- **Nomenclature.** configuration c (design variables) → attributes a (evaluation outcomes) →
  metrics m (conditioned attributes).
- **Kind of model.** A learned coordinate chart, kin to log-ratio (compositional) PCA: like PCA it
  identifies a direction and coordinates from data; unlike PCA the criterion is the one-sided soft
  maximum (a frontier direction, not a variance direction) and w lives on the simplex (a positive
  index with elasticities, not a contrast). Docs explain the supervisor's "hyperbolic PCA" sense and
  disambiguate it from PCA in negative-curvature geometry (HoroPCA and relatives).
- **API.** Aligned with scikit-learn's unsupervised/decomposition family: `fit`, `transform` (Z and
  log V), `inverse_transform`, `fit_transform`, `score_samples` (log V), `exponents_` as the
  `components_` analogue (one row per term), `n_terms` as the capacity parameter; no `predict` on the
  estimator. The design table enters through a `ColumnTransformer`: columns the analyst conditions
  into metrics (attributes, and configuration variables given a user-supplied positive ordinal
  mapping) go to the estimator, the rest pass through as covariates. Prediction emerges as a
  supervised composition: a regressor from configuration variables to chart coordinates predicts
  where a proposed configuration without measurements would fall (predicted log V, V − 1, Z),
  implemented with `TransformedTargetRegressor` plus a thin wrapper.
- **Theory grounds, it does not have to match (supervisor, 2026-11-07).** Theoretical results need
  not match the implementation exactly. Theorems may carry hypotheses we cannot certify for the
  spaces we sample (well-conditioned metrics, the balanced point in a facet's relative interior,
  log-convexity where white space is read). "All models are wrong, some are useful": the theory's
  job is to ground the work and to explain how to understand and interpret results, including the
  method's limitations. Every such hypothesis is explicit in the ledger with its interpretive role
  and its failure mode; it is not a defect to be minimized.
- **Proofs.** Docs discursive; every load-bearing result gets a SymPy axiom/lemma script in the
  hc-marimo plain-SymPy pattern (not a `symproof` dependency: not on PyPI, tree mid-merge),
  mirroring symproof's ledger conventions so the chain can be lifted into sealed bundles later.
- **Demo.** ADCS geosat trade study with two categorical hardware choices; minimal numpy/scipy code
  copied from `/Users/z/Documents/GitHub/adcs-lifecycle-demo`; Jupyter notebook.
- **Docs and site.** Markdown + LaTeX; GitHub Pages site as executable specification paired with
  narrative, framed by the supervisor's SciPy 2026 paper (Tall's three worlds); literature review
  and BibTeX as their own package.
- **Tooling.** uv for reproducibility; Python 3.12; src layout; package `hyperbolic_trade_space`.
- **Process.** Gated work packages per `github.com/mzargham/claude-skills`; Sonnet 5.5 as project
  manager and implementer from WP1 on; verbal approvals for now, release controls after the first
  release; no AI attribution lines on commits, PRs or documents.

Agent defaults (changeable at the relevant scope gate): MkDocs Material for the site; estimator
class name `HyperbolicTradeSpace` and package `hyperbolic_trade_space` (decided by the supervisor
at the WP2 gate, 2026-11-08; the method keeps the name "posynomial invariant form"); Z oriented for plots and hole detection by ordinary PCA of near-frontier Z (for K = 1
only w is learned, Z is a canonical basis); demo physics additions in §8.

## 3. Pipeline stages and contracts

Notation: N designs, d metrics, M ∈ ℝ^{N×d}_{>0}, U = log M with rows u_i, Δ the simplex, P the law
of u induced by stages 0–2, A = supp P the admissibility set in log space.

| Stage | Map | Codomain / contract | Owner |
|---|---|---|---|
| 0 Sampling | choose c_i | 𝒞, mixed types, any scheme, may be sparse or biased | analyst |
| 1 Evaluation | f: 𝒞 × Ω → 𝒜 | attributes a ∈ 𝒜 ⊆ ℝ^q, mixed, noisy | blackbox |
| 2 Conditioning | g: 𝒜 (and chosen c) → ℳ = ℝ^d_{>0} | positive, larger-is-better, comparable log-spread, chosen reference point; log-affine per metric, invertible on the metric block; other columns pass through as covariates | analyst, sklearn tools |
| 3 Identification | finite subsets of ℳ → (w, β); chart Ψ: ℳ → (Z, log V) | shape model, invertible chart, diagnostics | this package |
| 4 Analysis | level sets, holes in Z, novelty, pull-back of F through g⁻¹, interpretation vs covariates, prediction from configuration (supervised composition c → (Z, log V)) | | this package + sklearn regressors |

Stage 3 consumes a positive matrix and presumes nothing else; pull-back to attributes uses g⁻¹;
association with configurations is through the data (f is not invertible) or through the
supervised composition of stage 4.

## 4. Mathematics

**Model.** V(m) = Π_j m_j^{w_j}, w ∈ Δ; log V = w·u − β; F = {w·u = β}; level sets are parallel
hyperplanes. Σw = 1 ⇒ weighted geometric mean, homogeneous of degree 1; β is absorbed by
m̃ = m·e^{−β}, the invariant form Π m̃_j^{w_j} = 1.

**Fit.** J_τ(w) = (1/τ) log((1/N) Σ_i exp(τ w·u_i)); w* = argmin_{w∈Δ} J_τ; β = J_τ(w*). Convex
program; ∇J = Uᵀp, p = softmax(τUw) (envelope-weighted centroid); interior KKT ⇒ components of Uᵀp
equal. Diagnostics: p_i, n_eff = 1/Σp_i², frac_above. τ is in units of 1/(log-spread): after
conditioning, useful range ~3–100, default 10; τ→0 degenerates to a vertex; `select_temperature`
bisects log τ for a target frac_above. Optional `min_exponent` floor.

**What the stage learns, and why it is shape** (each claim cites its lemma, §6):
1. ρ_τ(w) = (1/τ) log E_P exp(τ w·u) is convex in w, nondecreasing in τ, → E[w·u] as τ→0 and ↑ the
   support function h_A(w) = ess sup w·u as τ→∞; h_A determines conv A. The method reads a softened
   support function of the admissibility set over positive directions; K = 1 reads one direction.
2. At τ = ∞ the fit is the LP min_{w∈Δ} max_i w·u_i = max_{λ∈Δ_N} min_j (Uᵀλ)_j (LP duality): the
   supporting hyperplane of conv A at its most balanced point (on the diagonal ray when all w_j > 0:
   all conditioned metrics equally good relative to the stage-2 reference). w* is the local normal
   (elasticities) there; moving the reference traces other facets.
3. Shape, not density: at τ = ∞ the result depends on P only through A; at finite τ a point at depth
   δ below the envelope has weight e^{−τδ}, so interior density matters only in a boundary layer of
   depth ~1/τ.
4. Noise: for u = u^true + ε, ε i.i.d., ρ_τ gains (1/τ) log E exp(τ w·ε); Gaussian N(0, σ²I) gives
   τσ²‖w‖²/2: a known β offset plus a mild ridge toward balanced exponents.
5. Consistency and the β normalization: the sample functional converges to ρ_τ (LLN, uniformly on
   Δ), so ŵ, β̂ converge; replication leaves the limit unchanged. The unnormalized log-sum-exp equals
   the log-mean-exp + (log N)/τ, diverges with N, and never lets a point exceed V = 1. ρ_τ is the
   entropic risk functional (mean ↔ essential supremum).
6. Invariances: uniform scaling shifts β by log k and leaves w, V unchanged; permutation
   equivariance; per-metric rescaling (stage 2) changes which facet is tangent (documented lever);
   (Z, log V) is a linear bijection of log space with Z independent of w.
7. Identifiability: w* unique iff the balanced point is in the relative interior of a facet with
   positive normal; finite τ gives uniqueness when Cov_p(u) is positive definite. Report n_eff.
8. Hyperbolic reading: V → 0 as any m_j → 0; no metric can be sacrificed entirely.

**Interpretation.** Elasticities d log m_j / d log m_k = −w_k/w_j on F (shape, not preference);
improvement factor for metric j alone V^{−1/w_j}; projection m/V; coordinates Z = U Bᵀ with B a
Helmert/ILR basis of 1^⊥ (or ALR log-ratios); holes = regions of Z with no near-frontier points
(|log V| < band), scored by k-NN / grid distance inside the hull; pull-back
log m_j = α_j log(a_j + s_j) + b_j ⇒ V = e^{w·b − β} Π (a_j + s_j)^{w_j α_j}, negative exponents mark
cost attributes. Design-variable reading: color by covariates, mean V and near-frontier share per
category, correlation of log V with continuous design variables, per-category refits. The estimator
itself fits no surrogate; surrogates live in the prediction composition.

**Novelty and white space.** Scoring a measured or hypothetical attribute vector evaluates the
learned chart after the fitted preconditioner; V − 1 is the uniform factor by which a frontier
design must improve to reach it (L1); stochastic frontier analysis describes the same geometry as a
regression with one-sided error. Prior art (verified 2026-11-07): DEA super-efficiency (Andersen &
Petersen, Management Science 39(10) 1993, doi 10.1287/mnsc.39.10.1261: scores > 1 beyond the
frontier of the others); Malmquist frontier shift (Färe, Grosskopf, Norris & Zhang, AER 84(1) 1994,
66–83); Shephard output distance function; DEA targets; Pareto gap/spacing metrics. Caveats to
build in: (1) noise band: `frac_above_` of training designs exceed V = 1 by construction, so provide
calibrated novelty (rank of log V among training scores, τ·log V) next to V − 1; (2) optimism off
the balanced point: far-from-diagonal designs have V ≪ 1 even when locally on the frontier, so V − 1
is reliable near the balanced region and conservative elsewhere (K > 1 tightens it); flag points
whose Z lies outside the training Z-hull; (3) holes are attainable only if the trade space is
log-convex there, and structural gaps (categorical strata) are not opportunities: human validation
decides; (4) novelty ≠ preference.

**Prediction from configuration.** Given a proposed configuration without measured attributes,
where it would fall is a supervised question: regress chart coordinates on configuration variables
over the designs that have both, then read predicted log V (distance to or beyond the frontier),
predicted V − 1 (expected novelty) and predicted Z (where along the frontier). Prediction inherits
the surrogate's error and extrapolation risk and is conditional on the fitted trade space; it
belongs to the composition, not to the unsupervised estimator.

**Lineage.** Cobb–Douglas / Shephard distance function with homogeneity imposed; deterministic
frontiers (programming-based: Aigner & Chu 1968; statistical: Afriat 1972, extended by Richmond
1974 and Greene 1980) and corrected OLS (COLS: OLS fit, intercept raised by the largest residual so
no observation lies above the frontier, as defined in Battese 1992; no single originator is named
in the sources read); stochastic frontiers (Aigner, Lovell & Schmidt 1977); DEA as the hull limit;
entropic risk measure for ρ_τ; log-ratio PCA (Aitchison) as feature-engineering kin. Sources and
their verification status are in `docs/references.bib` and `docs/literature.md` (WP5); an earlier
draft of this sentence attributed COLS to Aigner & Chu 1968, which the sources do not support.

**Extension: posynomial / GGP (documented, not built).** V_K(m) = (Σ_k c_k Π_j m_j^{κ w_kj})^{1/κ},
w_k ∈ Δ, κ > 0; in log space Φ(u) = (1/κ) log Σ_k exp(κ(θ_k·u − β_k)), a softmax-affine function
(Hoburg, Kirschen & Abbeel 2016: GP-compatible, containing max-monomial and posynomial fitting);
V_K is a generalized posynomial (Boyd, Kim, Vandenberghe & Hassibi 2007). Simplex-normalized terms
⇒ Φ(u + c1) = Φ(u) + c, so homogeneity, projection, invariant form and novelty carry over; K = 1
recovers the monomial; κ→∞ gives the max of monomials (Magnani & Boyd 2009). What K buys: K = 1 is
one facet (constant trade-off rates, the log-space analogue of weighted-sum scalarization); K > 1 is
any log-convex admissibility set with up to K facets (regionally varying elasticities, the full GP
class) and removes most of the off-diagonal optimism that confounds white space. No K represents
non-log-convex structure (holes, strata, dents): shape = log-convex envelope (K terms) + non-convex
residual (holes). Hierarchy K = 1 tangent → K-facet SMA → data's log-convex hull (DEA); larger K
needs per-facet support and selection of (K, κ): non-convex fit (envelope analogue of the
Magnani–Boyd partition, or GPfit-style ISMA adapted from regression to envelope), hence a later
package. Solver-free intermediate: refit K = 1 at several reference points. Demonstration test for
later: planted two-facet frontier; K = 1 under-scores one region, K = 2 recovers both. API shape:
`n_terms`, `term_temperature`, `exponents_` (n_terms, d), `log_offset_` (n_terms,).

**Research direction: kernel methods under the GGP constraint (documented, not built).** Admissible
kernels are those whose expansion is a generalized posynomial in m (positive combinations, powers,
max/softmax of monomials; exponential-of-affine in u); a Gaussian RBF in log space is log-quadratic
and excluded. Natural candidate: softmax-affine expansion anchored on support designs,
Φ(u) = (1/κ) log Σ_{i∈S} exp(κ θ_i·(u − u_i)). Our data-level log-mean-exp is already a posynomial in
the data and the LP duals p_i are support weights; the support-vector analogy is a hypothesis to
examine. Open: choosing S from p_i, local normals θ_i, roles of τ and κ, overfitting toward the DEA
hull, survival of novelty/white-space semantics. API implication now: Φ-based definitions so any
term set {(θ_k, β_k)} plugs in; kernel PCA is the feature-engineering kin to cite.

## 5. Package (src/hyperbolic_trade_space/)

- `solvers.py` (numpy/scipy): `log_mean_exp(s, tau)` (τ=inf → max), `support_weights(s, tau)`
  (softmax; τ=inf → argmax, ties averaged), `objective_and_grad(w, U, tau)`, `solve_lp(U,
  min_exponent)` via `linprog(method="highs")` on (w, t): min t s.t. Uw ≤ t·1, Σw = 1,
  w ≥ min_exponent, duals → p; `solve_slsqp(U, tau, min_exponent, w0, tol, max_iter)` with analytic
  jac, warm-started from the LP; `SolveResult(w, beta, p, objective, n_iter, success, message)`.
  Always `scipy.special.logsumexp(tau*s, b=1/N)/tau`. Rows with −∞ (zero metrics) are masked by the
  caller.
- `coordinates.py`: `helmert_basis(d)`, `alr_basis(d)`, `to_frontier_coordinates(U, w, beta, B) →
  (Z, log_v)`, `from_frontier_coordinates(Z, log_v, w, beta, B) → U`; d = 1 ⇒ Z has 0 columns.
- `estimator.py`: `class HyperbolicTradeSpace(TransformerMixin, BaseEstimator)`;
  `__init__(temperature=10.0, min_exponent=0.0, coordinates="ilr", n_terms=1,
  term_temperature=np.inf, tol=1e-10, max_iter=500)`; `n_terms != 1` → NotImplementedError pointing
  to the documented extension. `fit(X, y=None)`: validate, reject negatives, allow zeros (−∞ row:
  V = 0, log V = −∞, p = 0, excluded from the mean), d = 1 shortcut, LP always then SLSQP if τ finite,
  diagnostics. Methods: `transform` = [Z | log V] (invertible chart), `inverse_transform`,
  `fit_transform`, `score_samples` = log V; domain methods `invariant_value` = V, `novelty_score(X,
  calibrated=False)` = V − 1 or (rank among training log V, τ·log V), `project` = X/V,
  `improvement_factors` = V^{−1/w_j}, `level_set(Z, value=1.0)` → metric points on {V = value};
  `get_feature_names_out` (`ilr0..`, `log_v`); `__sklearn_tags__`. No `predict`, `decision_function`
  or `score`. Fitted: `exponents_` (n_terms, d), `log_offset_` (n_terms,), `support_weights_`,
  `n_eff_`, `frac_above_`, `objective_`, `n_iter_` (≥ 1 also on the LP path), `basis_`,
  `training_log_v_`, `n_features_in_`, `feature_names_in_`.
- `predictive.py`: `TradeSpaceRegressor(regressor, trade_space)` (RegressorMixin, BaseEstimator):
  `fit(X_config, Y_metrics)` fits `trade_space` (a `HyperbolicTradeSpace` or a Pipeline of
  preconditioner + estimator) on Y, then `regressor` on X_config → `trade_space.transform(Y)`;
  `predict(X_config)` → predicted metrics via `inverse_transform`; `predict_coordinates` → (Z,
  log V); `predict_novelty`; `predict_std` when the regressor supports `return_std`; `score` = R² in
  coordinate space (documented). Built on or interoperable with
  `sklearn.compose.TransformedTargetRegressor` (verify 2-D y support at implementation).
- `preconditioning.py`: `class LogAffinePreconditioner(OneToOneFeatureMixin, TransformerMixin,
  BaseEstimator)` `(orientation=None, shift=0.0, scaler="standard"|"robust"|None|instance)`:
  z = o·log(X + shift), scaler fit on finite z, transform = exp(scaled z) (zeros → 0), exact
  `inverse_transform`; fitted `scaler_`, `log_scale_` (α), `log_offset_` (b), `orientation_`,
  `shift_`. `frontier_in_original_units(estimator, preconditioner) → dict(exponents_orig,
  log_const, shift)`.
- `tuning.py`: `select_temperature(X, target_frac_above=0.10, bounds=(1e-1, 1e4), tol=0.01,
  **params)` by bisection on log τ.
- `gaps.py`: `knn_gap_scores(Z, k=5)` (cKDTree); `find_holes(Z, resolution=50, threshold=2.0)` for
  d−1 ∈ {1,2,3} (grid, distance to nearest point, hole = far and inside the hull via
  `Delaunay.find_simplex`); `frontier_targets(Z_points, estimator, preconditioner=None)` mapping
  (Z, log V = 0) back to metrics and, if given, attributes; `orient_by_pca(Z, mask)` for display.
- `datasets.py`: `make_frontier_data(n_samples, n_features, exponents=None, log_offset=0.0,
  frontier_fraction=0.3, interior_scale=1.0, noise=0.0, random_state=None) → (X, info)`: Z ~ N(0,I),
  frontier rows log V = noise·N(0,1), interior rows log V = −Exp(scale), mapped back through the
  chart; identifiable when the frontier Z-hull contains 0. `make_configured_frontier_data(...)` adds
  a known configuration → metrics map for `predictive` tests.
- `plotting.py` (lazy matplotlib, return Axes): `plot_frontier_surface_3d`, `plot_log_plane`,
  `plot_frontier_coordinates(Z, log_v, color, holes)`, `plot_v_by_variable`.

Tests (pytest): `test_solvers` (LME vs naive; τ=inf = max; `check_grad`; hand-built LP; LP vs SLSQP
at τ=1e3; duals sum to 1); `test_coordinates` (orthonormal ⊥ 1; round trip 1e-12; Z invariant to
u + c1); `test_datasets`; `test_estimator` (recovery d ∈ {2,3,5} at τ=inf < 1e-6 and τ=1e3 < 2e-2;
simplex and floor; p ≥ 0, Σp = 1, 1 ≤ n_eff ≤ N; τ=inf ⇒ frac_above 0 and max V ≤ 1+1e-9; finite τ ⇒
0 < frac_above < 0.5; shape tests: uniform rescaling, replication, interior-density insensitivity,
permutation equivariance, Gaussian noise offset ≈ τσ²‖w‖²/2; chart round trip; `transform[:, -1] ==
score_samples`; `invariant_value(project(X)) == 1`; improvement factor lands on V = 1; a point on
the hyperplane in a planted hole has V = 1 and round-trips to attributes; leave-one-out
super-efficiency: a frontier point removed and refit at τ=inf scores ≥ 1; d = 1; zero → V 0;
negative/NaN → ValueError; `n_terms=2` → NotImplementedError; ColumnTransformer + Pipeline; feature
names; `select_temperature` hits target); `test_predictive` (known configuration → metrics map:
predicted log V and Z match held-out truth within tolerance; a planted beyond-frontier
configuration gets predicted novelty > 0; `predict_std` plumbing); `test_sklearn_compat`
(`parametrize_with_checks` over the estimator at default, τ=inf and `coordinates="alr"`, the
preconditioner, and `TradeSpaceRegressor` with a linear regressor; `expected_failed_checks` an
explicit reasoned dict, goal empty; `xfail_strict=True`); `test_preconditioning` (round trip with
mixed orientation and shift; unit log-std; `frontier_in_original_units` reproduces the pipeline's
`score_samples`); `test_gaps` (planted disc hole in 2-D; 1-D gap; targets round-trip);
`test_plotting` smoke.

## 6. Derivation scripts (derivation/, SymPy, hc-marimo pattern)

**Abstract spaces, not enumerated instances (supervisor's direction, 2026-11-07).** The chain
works at symbolic dimension d, symbolic sample count n and symbolic term count K: metrics and data
as `IndexedBase` (m_j, u_ij) with symbolic bounds, exponents w_j with the simplex constraint
Σ_j w_j = 1 carried as a substitutable `Sum`, sums and products as `Sum`/`Product` over symbolic
ranges, and the chart as a `MatrixSymbol` basis B with its defining properties (B Bᵀ = I, B 1 = 0)
taken as hypotheses. Identities are verified in log space, where everything is linear in sums.
Concrete instantiation (e.g. d = 3, n = 3) is only a secondary cross-check substituted into the
abstract identity, never the proof; any step that resists abstract simplification falls back to a
clearly labelled inherited axiom or an explicitly stated hypothesis, recorded in the ledger.

Layout mirrors `/Users/z/Documents/GitHub/hc-marimo/derivation/` (see
`docs/superpowers/notes/proof-conventions.md`): `symbols.py` (abstract symbol namespace: d, n, K,
indices i, j, k, `IndexedBase` m, u, w, θ, β, τ, κ, σ, c; `SYMBOL_ASSUMPTIONS` mapping each strong
Symbol assumption to its licensing axiom), `axioms.py` (frozen dataclass; tags POSITED /
INHERITED-with-citation / REGULARITY), `lemma_NN_<slug>.py` (`TITLE`, `STATEMENT`, `AXIOMS_USED`,
`derive(ctx)`, `verify(ctx)`, "what this proves / does not prove" docstring), `run.py` (`CHAIN`,
`run_chain`, `print_audit` ledger DERIVED / POSITED / INHERITED / REGULARITY),
`tests/test_derivation.py` (full abstract chain; per lemma; concrete cross-check by substitution;
no phantom axioms; inherited are cited; load-bearing Symbol assumptions declared).

Axioms: POSITED A1 metrics positive; A2 exponents on the simplex; A3 τ > 0; A4 conditioning
log-affine and invertible (α_j ≠ 0); A5 noise i.i.d. N(0, σ²I); A6 κ > 0 and each term on the
simplex. INHERITED: I1 LP strong duality (Boyd & Vandenberghe, Convex Optimization §5.2); I2 strong
law of large numbers; I3 a closed convex set is determined by its support function (Rockafellar,
Convex Analysis §13); I4 softmax-affine functions are GP-compatible (Hoburg et al. 2016).
REGULARITY R1: the balanced point lies in the relative interior of a facet with positive normal.
I1 is checked numerically in pytest (primal vs dual), I2 by the replication test.

Lemmas: L1 homogeneity and invariant form, V(k·m) = k·V(m), V(m/V) = 1 [A1, A2]; L2 uniform shift
J_τ(w; U + c1ᵀ) = J_τ(w; U) + c [A2, A3]; L3 gradient = Σ_i p_i u_i and balanced KKT [A3]; L4
convexity: second directional derivative = τ·Var_p(v·u) = (τ/2) ΣΣ p_i p_k (s_i − s_k)² ≥ 0 [A3]; L5
LSE = LME + (log n)/τ, LSE − max ≥ 0 (strictly > 0 for n ≥ 2), lim_{τ→∞} LME = max, lim_{τ→0} LME = mean, mean ≤ LME ≤ max
[A3]; L6 Gaussian cumulant (1/τ) log E exp(τ w·ε) = τσ²‖w‖²/2 via `sympy.stats` [A2, A5]; L7
elasticities −w_k/w_j and improvement factors [A1, A2]; L8 Helmert chart: BBᵀ = I, B1 = 0, round
trip, Z(u + c1) = Z(u) [A2]; L9 pull-back formula [A1, A2, A4]; L10 extension: Φ_2(u + c1) =
Φ_2(u) + c, K = 1 reduction, lim_{κ→∞} Φ_2 = max [A2, A6]. SymPy pitfalls: avoid eager evaluation of
inequalities; helper symbols for bounded quantities; `sympy.limit` under explicit assumptions with
the result recorded as an equality; ordering assumption s_1 > s_2 instead of `Max`.

## 7. scikit-learn conformance (requirement)

See `docs/superpowers/notes/sklearn-conformance.md` for the rules with sources. Summary: pin
`scikit-learn>=1.8`; immutable-default keyword params stored verbatim and validated in `fit`;
`validate_data` with `reset=True` in fit and `reset=False` after `check_is_fitted` elsewhere;
negatives raise `ValueError` "Negative values in data"; zeros tolerated (−∞ semantics) because the
`positive_only` checks shift data to a minimum of exactly 0; tags only via `__sklearn_tags__`;
mixins left of `BaseEstimator`; fitted attributes end in one `_`; `n_iter_ ≥ 1`;
`get_feature_names_out` of the transform width; decomposition-family semantics (`score_samples`, no
`predict`/`score`/`decision_function` on the transformer); `TradeSpaceRegressor` follows the
regressor contract; `parametrize_with_checks(..., expected_failed_checks=..., xfail_strict=True)`;
numpydoc docstrings with doctests.

## 8. ADCS demo (examples/adcs/)

See `docs/superpowers/notes/adcs-port.md` for the source files, baseline values and regression
pins. Demo modelling defaults (confirm at the WP4 scope gate): a constant solar-radiation-pressure
disturbance torque (illustrative GEO-typical ~1e-5 N·m) so steady pointing error depends
continuously on Kp instead of being set by the star-tracker floor; total pointing error = RSS(θ_ss,
floor); control effort ∫‖τ‖dt over the slew as a continuous power/energy proxy; peak wheel momentum
as a feasibility flag (h_peak ≤ maxMomentum), not a metric; hardware class values labelled
illustrative.

Files: `adcs_sim.py` (port, `BASELINE`, `inertia_tensor`, `pointing_budget`, `make_config`);
`design_space.py` (`WHEEL_CLASSES` small/medium/large = (0.05, 2, 1.5), (0.1, 4, 2.5), (0.2, 8, 4.0)
for maxTorque N·m / maxMomentum N·m·s / mass kg; `STAR_TRACKERS` coarse/medium/fine = (15, 1.0),
(5, 2.0), (1.5, 3.5) arcsec / kg; `KP_RANGE`, `KD_RANGE` log-uniform; `sample_designs(n, rng)` with
~10 % lognormal perturbation of panel and antenna mass and a child seed per design;
`evaluate_design(row, t_end=900, ...)` → settling_time_s, pointing_error_deg, adcs_mass_kg
(3 wheels + ST + IMU), control_effort, flags settled / momentum_ok / torque_saturated_frac;
`FAST_SIM` for tests); `generate_dataset.py` (argparse `--n 1000 --seed 0 --out
data/adcs_designs.csv --workers --force --fast`, multiprocessing, skip if present; CSV committed);
`extended_design_space.sysml` (documentation only); `adcs_trade_study.ipynb` organised by stage:
load and filter feasible; `ColumnTransformer` with `OrdinalEncoder` (explicit category orders) for
covariates and `LogAffinePreconditioner(orientation=[-1]*4)` for the four attributes, conditioning
diagnostics; `select_temperature`, fit, diagnostics table, τ sweep; 3-D surface for (settling,
pointing, mass) and full d = 4 fit; log-space plane; frontier coordinates with holes and white-space
targets; V by wheel class, ST grade, Kp, Kd; per-category refits; three hand-written candidates
with measured attributes scored (novelty, improvement factors); frontier pulled back to attribute
units; propose, predict, then check: `TradeSpaceRegressor` on (Kp, Kd, wheel class, ST grade) →
coordinates predicts where three proposed configurations would fall, the simulator then evaluates
them, and predicted vs measured log V and Z are compared against the band 1/τ. Reads only the
cached CSV (plus the three check simulations, cached too); committed executed with static PNGs;
says explicitly that mass is stratified by hardware so gaps between strata are structural. Tests:
inertia ≈ (327.14, 107.48, 303.45); regression pins; `evaluate_design` × 3 with `FAST_SIM`;
reproducible sampling. Pitfalls: settling time quantized by `max_step` and censored at `t_end`
(keep `settled`); momentum observed not enforced (flag); dataset at max_step 0.5.

## 9. Site, docs and reproducibility

See `docs/superpowers/notes/presentation-framing.md`. Site (MkDocs Material, `pymdownx.arithmatex`,
`mkdocs-jupyter`, `mkdocstrings[python]`, `mkdocs-bibtex`; landing page with cards): Home; Why and
how to use it; Mathematics (`docs/method.md` with lemma tags); Derivations (generated ledger);
Preconditioning (`docs/preconditioning.md`); Case: ADCS trade study; Verification & validation
(generated); API (`docs/api.md`: as built and as it extends to K > 1 and kernel methods) and API
reference; Extensions and limitations; Literature (`docs/literature.md` from `docs/references.bib`).
`scripts/build_generated.py` writes generated pages. `.github/workflows/publish.yml`: checkout →
`astral-sh/setup-uv` → `uv sync --locked` → `uv run pytest` → derivation run → `uv run mkdocs build`
→ `upload-pages-artifact` → `deploy-pages` on main only; PRs build without deploying; the notebook
is rendered, never re-executed, in CI.

Reproducibility: committed `uv.lock` and `.python-version`; every documented command is `uv run`;
CI uses `uv sync --locked` and `uv lock --check`; seeded data generation; tolerances, never
equality, in numeric tests.

## 10. Verification (acceptance evidence, consolidated across packages)

- `uv run pytest` green including `test_derivation.py`, `test_sklearn_compat.py` with an explicit
  (ideally empty) expected-failures dict, the shape tests and `test_predictive.py`;
  `uv run python derivation/run.py` prints PASS for L1–L10 at d ∈ {2,3,4} and the ledger.
- `uv run python examples/adcs/generate_dataset.py --n 1000 --seed 0` reproduces the committed CSV
  within tolerance; regression pins match the source repo within ±0.2 s.
- `uv run jupyter nbconvert --execute --to notebook examples/adcs/adcs_trade_study.ipynb` runs from
  the cached data; figures show the V = 1 surface hugging the upper envelope, frac_above near target,
  candidates scored, white-space targets pulled back to attributes, and predicted vs simulated
  coordinates for the proposed configurations within the stated band.
- Synthetic sanity: planted exponents recovered; τ sweep shows frac_above monotone from ~0.5 to 0
  and n_eff from N toward d.
- `uv run mkdocs build --strict` succeeds; every formula in `docs/method.md` matches the code and a
  lemma; every citation key resolves; `uv sync --locked` from a clean clone reproduces the
  environment.
