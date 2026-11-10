---
world: symbolic
---

# API

This page documents the public interface as built, stage by stage, including the $K>1$ posynomial
fit (built for small $K$), and then the kernel methods, which are **documented, not built**. Pipeline stages
are those of [Mathematics](method.md): stage 2 conditioning, stage 3 identification, stage 4
analysis. Dimension is arbitrary: $d$ metrics, $d-1$ chart coordinates. The package follows the
scikit-learn conventions [@pedregosa2011scikit; @buitinck2013api]: parameters stored verbatim,
validation in `fit`, fitted attributes ending in an underscore.

## Overview

| Name | Kind | Role | Stage |
|---|---|---|---|
| `LogAffinePreconditioner` | transformer | attributes to larger-is-better metrics, invertible (A4, L9) | 2 |
| `frontier_in_original_units` | function | fitted frontier as a monomial in raw attributes (L9) | 2 and 4 |
| `HyperbolicTradeSpace` | transformer | fit the frontier; chart $[Z\mid\log V]$ (L1 to L5, L8) | 3 |
| `select_temperature` | function | choose $\tau$ by target fraction above the frontier (L5) | 3 |
| `make_frontier_data` | function | synthetic data with a planted frontier | testing |
| `make_configured_frontier_data` | function | planted frontier with configuration variables | testing |
| `tension_report` | function | which metrics contend, align, and the directions of trade | 4 |
| `TradeSpaceRegressor` | regressor | metrics, coordinates and novelty from configuration | 4 |
| `__version__` | string | package version | |

Submodules used by import path: `hyperbolic_trade_space.gaps` (`knn_gap_scores`, `find_holes`,
`frontier_targets`, `orient_by_pca`), `hyperbolic_trade_space.tensions` (`TensionReport`) and
`hyperbolic_trade_space.plotting` (the plotting helpers). They are stage 4 tools.
`hyperbolic_trade_space.solvers` holds the solvers and the certificate functions of stage 3
([Stopping record](#stopping-record-conditioning-and-conventions)).

## Stage 2: conditioning

**`LogAffinePreconditioner(orientation=None, shift=0.0, scaler="standard")`.** Computes
$z=o\log(X+s)$, scales it, and returns $m=\exp(\text{scaled }z)$. Zeros ($X+s=0$) map to $0$;
negatives raise `ValueError` "Negative values in data". Fitted: `scaler_`, `log_scale_`,
`log_offset_`, `orientation_`, `shift_`. `inverse_transform` is exact. This is the conditioning of
assumption A4 and the map in lemma L9. The full discussion is in [Preconditioning](preconditioning.md).

**`frontier_in_original_units(estimator, preconditioner)`.** Returns `exponents_orig`
($w_j\alpha_j$), `log_const` ($w\cdot b-\beta$) and `shift`, the closed form of L9 for a
single-term fit (A1, A2, A4).

## Stage 3: identification

**`HyperbolicTradeSpace`.** Parameters `temperature` ($\tau>0$ or `np.inf`, A3), `min_exponent`,
`coordinates` (`"ilr"` or `"alr"`), `n_terms` ($K$, default 1), `term_temperature` ($\kappa$,
default `np.inf`), `tol`, `max_iter`, `penalty` and `alpha` (the sparsity option), `random_state`.
Fitted attributes: `exponents_` of shape `(n_terms, d)`, `log_offset_` of shape `(n_terms,)`,
`support_weights_`, `n_eff_`, `frac_above_`, `objective_`, `n_iter_`, `basis_`, `training_log_v_`,
`termination_` and `conditioning_` (and, for $K>1$, `facet_`, `coefficients_` and `facet_share_`; see the $K>1$ section below). `transform` is the invertible chart $[Z\mid\log V]$ (L8, A7); `inverse_transform`
inverts it; `score_samples` returns $\log V$ (L1); `invariant_value` and `project` give $V$ and the
projection to the frontier. It has no `predict`: it follows the decomposition-family semantics of
scikit-learn. Frontier $V\le1$ is attainable, $V=1$ the frontier (L1, A2).

**`select_temperature(X, target_frac_above=0.10, bounds=(0.1, 1e4), tol=0.01, **params)`.**
Bisects $\log\tau$ so that the fitted `frac_above_` is within `tol` of the target. The temperature's
units are inverse log-spread, so the answer depends on the conditioning (L5); the bracket ends are
checked and a `ValueError` is raised when the target is not bracketed.

The fitted `frac_above_` is not monotone in $\tau$ for small $\tau$. By L5 the log-mean-exp lies
between the mean and the maximum of the scores and tends to the mean as $\tau\to0$ and to the
maximum as $\tau\to\infty$; so below $\tau\approx3$ `frac_above_` can overshoot $0.5$ (the
project's reading of the mean limit, not proved by L5: the fraction tends toward what lies above the
mean of the scores rather than the median), and above it decreases monotonically toward $0$ (the
test asserts this on $\tau\ge3$ and $0.4<$ `frac_above_` $<0.65$ at $\tau=0.1$). `select_temperature`
only needs the target bracketed by the two ends of `bounds`. A $\tau$ below about 3 is outside the
documented useful range (see `docs/limitations.md`). The default `bounds[0]` $=0.1$ is wider than
the recommended $\tau\gtrsim3$; bisection tolerates it because it needs only that the target be
bracketed by the ends of `bounds` (a `ValueError` otherwise), but below $\tau\approx3$ the response
is not monotone, so the returned $\tau$ is a root of the bracket search. Callers who need the useful
range should pass `bounds=(3, ...)`.

**`make_frontier_data`, `make_configured_frontier_data`.** Seeded generators of positive data with a
planted frontier (the second also returns a configuration matrix and a smooth map from configuration
to metrics), used by the tests and by the examples (A1, A2). `make_frontier_data(..., n_terms=K)`
plants the envelope $\max_k(w_k\cdot u-\beta)$ of $K$ monomials (`exponents` of shape `(K, d)`,
by default $K$ random draws at least 0.3 apart in $\ell_1$) and also returns `facet`, the planted
facet of each row in `info`; `n_terms=1` reproduces the single-facet generator exactly. At `n_terms=K` the generator guarantees at least $d+1$ frontier rows on every planted facet
(a facet with fewer is not determined by its frontier rows, so recovery is not identifiable);
this is necessary for recovery and not sufficient, and the recovery claim is the measured rate
above.

### Stopping record, conditioning and conventions

**`termination_`.** A frozen `hyperbolic_trade_space.solvers.Termination` holding the stopping
declaration of the chosen run; the levels it reports are stated in
[Mathematics](method.md#three-levels-of-guarantee) (Lemma 1, L12; Lemma 2, L13; Proposition 3 and
Corollary 4, L14). Its fields:

- `status`, `reason`, `n_iter`: the status (below), the solver's stop message and the
  partition-and-refit iterations of the run.
- `sum_residual`, `floor_residual`, `offset_residual`: $\max_k|\mathbf 1\cdot w_k-1|$, the largest
  violation of the `min_exponent` floor, and $\max_k|\beta_k-J_\tau(Uw_k)|$.
- `max_gap`, `gaps`, `shares`: the largest facet gap $G_k$ (the LP duality gap at $\tau=\infty$),
  the gap of every facet (`nan` for an empty one) and the row share $n_k/N$ of every facet.
- `bound`: the approximate-certificate bound (L14) $\sum_k\frac{n_k}{N}G_k$ on $F(W)-F^*_{\rm fixed}$, for the
  assignment of this run.
- `objective_change`, `assignment_changes`, `n_empty`: the change of the mean slack at the last
  accepted step, the rows whose argmax differs from the returned label, and the empty facets.
- `gamma`, `radius`: the assignment margin $\gamma$ and the assignment-stable radius
  $\gamma/(2\max_i\|(u_i,-1)\|_2)$; `inf` for $K=1$.
- `eps_kkt`, `eps_feas`, `guard_tol`: the tolerances used.

The statuses are `"certified"` (assignment fixed, residuals within `eps_feas`, `max_gap` within
`eps_kkt`, no empty facet, $\gamma>$ `eps_feas`), `"stationary_without_margin"` (the same with
$\gamma\le$ `eps_feas` or an empty facet: levels 1 and 2 only), `"uncertified"` (assignment fixed,
a residual or the gap above its tolerance), `"guard_stop"` (an iteration raised the mean slack by
more than `guard_tol`), `"iteration_cap"` (`max_iter` reached) and `"not_applicable"`
(`facet_step="tangent"`, a `penalty`, or the $K=1$, $d=1$, $N<K$ shortcut, where the gaps are
read-only diagnostics). The last two stops are never reported as `"certified"`. The tolerances
are module constants of `hyperbolic_trade_space.solvers`, re-exported by
`hyperbolic_trade_space.estimator`, and not parameters: `EPS_KKT` $=10^{-8}$, `EPS_FEAS` $=10^{-9}$,
`GUARD_TOL` $=10^{-12}$, `POLISH_STEPS` $=5$ (reduced-Newton steps after each finite-$\tau$ facet
refit). `fit` raises a scikit-learn `ConvergenceWarning` naming the status and the largest gap for
`"uncertified"`, `"guard_stop"` and `"iteration_cap"`.

**The certificate functions** (`hyperbolic_trade_space.solvers`): `simplex_gap(g, w,
min_exponent=0.0)`, the gap $g\cdot w-\min_jg_j$ of a gradient $g$ at a feasible $w$ (with the
floor, the gap to the floored simplex); `facet_objective(U, w, ubar, tau)`, $f_k$;
`facet_gap(U, w, ubar, tau, min_exponent=0.0, p=None)`, $G_k$ (at $\tau=\infty$ the LP duality gap
for the dual weights `p`, by default the dual of the facet's linear program); `assignment_margin(U,
W, beta)`, the pair $(\gamma,r)$; `fixed_assignment_bound(U, W, labels, tau, min_exponent=0.0,
P=None)`, the triple `(bound, gaps, F)`; and `single_facet_termination`, the record of a
single-facet fit. `solve_terms` returns a `TermsResult` whose `termination` field is the record.

**`conditioning_`**, shape `(n_terms,)`. The smallest eigenvalue of the restricted Hessian of
$J_\tau$ at each facet's fit, $\tau\big(U^\top\mathrm{diag}(p)U-(U^\top p)(U^\top p)^\top\big)$
restricted to the simplex tangent space and to the participating exponents
($w_j>$ `PARTICIPATION_THRESHOLD` $=10^{-3}$); a small value marks a nearly flat direction and so
weakly identified exponents ([Mathematics](method.md#what-the-stage-learns-and-why-it-is-shape),
statement 7). It is `nan` at $\tau=\infty$ and for a facet with fewer than two participating
exponents, and it is read-only.

**The zero-metric rule.** In the fit, a row with a zero metric is set aside: its support weight is
0, it is excluded from the objective, its $Z$ is `nan` and it has no inverse. In scoring, $\log V$
is the continuous extension of the monomial,
$\log V=\sum_{j:\,w_j>10^{-12}}w_j\log m_j-\beta$ with $0\log0:=0$ (`EPS_ZERO_EXPONENT`
$=10^{-12}$): a zero metric on a numerically zero exponent leaves $\log V$ finite, and a zero metric
on a participating exponent gives $V=0$, $\log V=-\infty$. At $K>1$ each facet's score follows the
same rule.

**The degenerate-input convention.** With a single valid row the fitted object does not exist; `fit`
returns uniform exponents as a declared convention and emits a `UserWarning` saying so. With $d=1$
the exponent is 1.

## Stage 4: analysis

### Gaps and white space (`hyperbolic_trade_space.gaps`)

- `knn_gap_scores(Z, k=5)`: mean distance to the $k$ nearest neighbours, normalized by its median.
- `find_holes(Z, resolution=50, threshold=2.0)`: grid cells inside the convex hull of $Z$ scored by
  distance to the nearest data point; supports $d-1\in\{1,2,3\}$. A hole is a candidate, not a
  verdict: a region with no near-frontier points can be an opportunity or a structural stratum,
  and human validation decides (see [Extensions and limitations](limitations.md)).
- `frontier_targets(Z_points, estimator, preconditioner=None)`: sets $\log V=0$ at given chart
  coordinates and maps back to metrics (L8) and, if a preconditioner is given, to attributes (L9).
- `orient_by_pca(Z, mask=None)`: rotation to the principal axes of the masked rows, with a fixed
  sign convention; returns `(Z_rotated, components, explained_variance_ratio)`.

### The tension report (`tension_report`)

`tension_report(estimator, X, band=None, min_near_frontier=10, threshold=1e-3, association="pearson")`
returns a frozen `TensionReport`. The model is built to find tensions, not variance: the fit picks
the positive combination of log-metrics with the smallest upper extent (L3, L4), a binding
constraint, where PCA picks the directions of largest spread. The report has three parts, plus the
contending set.

1. **Participation and exchange rates.** `participating` marks the metrics with exponent above
   `threshold` (default $10^{-3}$, the participation threshold); the rest are free at the balanced point. `exponents` are the working-temperature
   weights, `exchange_rates[j, k]` $=-w_k/w_j$, the elasticity of metric $k$ against $j$ along
   the frontier (L7), `nan` where $w_j$ is not above threshold. The reading needs the balanced
   point on the relative interior of a facet with a positive normal (R1).
2. **Association among near-frontier designs.** For rows with $|\log V|<$ `band`, `association` is
   the Pearson (or Spearman) correlation matrix of the log-metrics: negative means traded,
   positive means aligned. `closure_note` states the closure effect: near the frontier $w\cdot u$
   is almost constant (L1), so a binding constraint induces negative association among participating
   metrics even where no designer traded them. Association is evidence of tension only together
   with the exponents and the directions.
3. **Tension directions.** `tension_directions` are the principal directions of the near-frontier
   $Z$ (unit vectors in chart coordinates), `tension_loadings` the same directions as loadings on
   the log-metrics through the chart basis (L8, A7), and `explained_spread` the share of near-frontier
   variance along each. They equal `orient_by_pca` on the same rows.

**The contending set, the n-lemma reading.** `contending_set`, `contending_exponents`, `n_lemma` and
`lemma_name` give the support of the solution at $\tau=\infty$ (exponents above $10^{-9}$). At $\tau=\infty$ the fit is a linear
program (I1) whose solution is generically sparse, with exact zero exponents; the support is the set
of metrics that contend at the balanced point, of any size $n$ and with no prior choice of which or
how many: a monolemma ($n=1$), dilemma, trilemma, then an $n$-lemma. At a finite working $\tau$ the
weights are smoothed (L5), so a small weight means weak participation, not membership; the report
keeps the two distinct. **Caveat: `min_exponent` must be 0 for this reading.** A positive floor
forces every exponent to be at least `min_exponent` and so masks the sparsity. The report solves the
$\tau=\infty$ program itself with `min_exponent = 0` on the log of the supplied rows, independent of
the fitted temperature and floor, and issues a `UserWarning` when the estimator was fitted with
`min_exponent > 0` because its working weights are floored.

Degenerate input is explicit: fewer than `min_near_frontier` near-frontier rows raises
`ValueError` suggesting a larger band or temperature; $d=1$ returns a trivial report with empty
directions; `band=None` means $1/\tau$ for finite $\tau$ and $0.1$ at $\tau=\infty$. The report is
deterministic. At $K>1$ the function returns a **list** of $K$ reports, one per facet, each computed on the
rows assigned to that facet with the facet's exponents, near-frontier rows $|\Phi_K|<$ `band`,
and directions and loadings through `basis_[k]`; a facet with fewer than `min_near_frontier`
near-frontier rows raises `ValueError` naming the facet. Its limits: each report describes one
facet, so one tension; it depends on the band; and a tension is a binding constraint while a
correlation is only a co-movement. A deflation search for successive tensions is a research
question with no claim made.

### Prediction from configuration (`TradeSpaceRegressor`)

**`TradeSpaceRegressor(regressor, trade_space)`** is a supervised composition: `fit(X_config,
Y_metrics)` clones and fits `trade_space` on the metrics, then clones and fits `regressor` on
configuration to chart coordinates $[Z\mid\log V]$ (L8). `predict` returns metrics through the
inverse chart; `predict_coordinates` returns `(Z, log_v)`; `predict_novelty` returns $V-1$ (novel
where positive; L1); `predict_std` propagates the regressor's `return_std` by the delta method and
raises `AttributeError` if the regressor lacks it; `score` is $R^2$ in coordinate space, not in
metric units. Coordinates, not metrics, are the regression target, so the surrogate's error is
inherited honestly by the novelty prediction. A 1-D `y` is accepted for a single metric. The
`trade_space` may be a `Pipeline` ending in a `HyperbolicTradeSpace`, for example a preconditioner
followed by the estimator.

**Documented expected failure.** In `tests/test_sklearn_compat.py` the regressor instance carries
one entry, `check_regressor_multioutput`. scikit-learn's check builds `y` with `make_regression`,
which contains negative values, and does not apply the target-tag enforcement that the other
regressor checks use; the regressor declares `target_tags.positive_only=True` and, because the metrics
are log-transformed by the chart (A1), raises `ValueError` on negative `y`, which is the intended
behaviour. Multi-output fit and predict shapes are covered separately by `tests/test_predictive.py`
for $d=3$ and $d=1$. The dict is run with `xfail_strict=True`, so the entry would fail the suite if the
check ever started passing. `LogAffinePreconditioner` and `HyperbolicTradeSpace` have empty
expected-failure dicts.

### Plotting (`hyperbolic_trade_space.plotting`)

`plot_log_plane`, `plot_frontier_surface_3d`, `plot_frontier_coordinates`, `plot_v_by_variable` and
`plot_tensions` each accept an optional `ax`, return a matplotlib `Axes`, and share one visual
vocabulary declared as module constants: `FRONTIER_COLOR` (frontier $V=1$, black), `BAND_COLOR`
(near-frontier band, grey), `HOLE_COLOR` (white space), `CATEGORY_COLORS` (one qualitative palette),
`DATA_COLOR`, and `TENSION_CMAP` (diverging, tension to aligned). Targets are open markers.
Matplotlib is imported lazily and nothing calls `plt.show()`. For a fit with $K>1$ the plots
draw every facet (the log plane shows the facets with weight on both plotted metrics) and
`facet_labels(estimator, X)` returns `"facet 1"` to `"facet K"` for each row, to pass as `color=`
so that the data are coloured by the facet that is active there.

## The posynomial fit, $K>1$

The single monomial is the one-term case of the generalized posynomial

$$
V_K(m)=\Big(\sum_{k=1}^{K}c_k\prod_{j=1}^{d}m_j^{\kappa w_{kj}}\Big)^{1/\kappa},\qquad
\Phi_K(u)=\frac1\kappa\log\sum_{k=1}^{K}\exp\!\big(\kappa(w_k\cdot u-\beta_k)\big),
$$
<!-- definition: L10 -->

with each $w_k$ on the simplex and $\kappa>0$ (A6). $\Phi_K$ is softmax-affine and compatible
with geometric programming (I4) [@hoburg2016data; @boyd2007tutorial]; the identity
$\exp(\kappa\Phi_K)=\sum_ke^{-\kappa\beta_k}\prod_jm_j^{\kappa w_{kj}}$, the shift equivariance
$\Phi_K(u+c\mathbf 1)=\Phi_K(u)+c$ that carries homogeneity, projection and novelty over, and the
bounds $\max_kx_k\le\Phi_K\le\max_kx_k+(\log K)/\kappa$ are proved in L10 (A2, A6, F10). It is built
for small $K$: `n_terms=K` fits the facets by partition and refit
(`hyperbolic_trade_space.solvers.solve_terms`; the algorithm, what is proved and inherited (I7)
and the simplifying assumptions are in [Mathematics](method.md#the-solver-for-small-k)).
Nothing is claimed about global optimality; scalability and performance are future work.

**Parameters.** `n_terms` is $K$. `term_temperature` is $\kappa$, default `np.inf` (the exact
maximum of the facets); it is distinct from `temperature` ($\tau$, the data-level soft maximum of
every facet's fit). A finite $\kappa$ rounds the corners of the score and leaves the facets
unchanged; the score lies within $(\log K)/\kappa$ above the maximum (L10) and the gap is not
renormalized. `penalty="reweighted_l1"` with `alpha` $\ge0$ is the sparsity option for the exponents
of every facet [@candes2008enhancing]; `alpha=0` leaves the fit unchanged and it acts at finite
`temperature` only. `random_state` seeds the facet initializations (five restarts, the best
kept); `max_iter` caps the inner SLSQP of each facet fit.

`n_restarts` (default 5) is the number of seeded initializations of the alternation, the one with
the lowest mean slack being kept; it has no effect at `n_terms=1`. More restarts cost time and buy
some robustness, but they are not a cure for a local optimum: the restart is chosen by the mean
slack, and on the planted seeds that fail, extra restarts did not recover them (see the
limitations page). The default path is the five
restarts of the earlier releases, unchanged.

`facet_step` chooses the per-facet step of the alternation and has no effect at `n_terms=1`.
`"support"` (the default, step B) fits each facet as the supporting hyperplane of all rows that is
tightest on the facet's rows; the mean slack $\frac1N\sum_i(\beta_{k(i)}-w_{k(i)}\cdot u_i)$ does
not increase under either half-step, a guard enforces it, and this is the step the paper
presents. `"tangent"` (step D) takes the direction from the facet's near-frontier rows (its own
rows within $1/\tau$ of its support plane, $0.1$ at $\tau=\infty$) when there are at least $d+1$
of them and falls back to step B otherwise; the mean slack is **not** monotone under it, so the
loop returns the lowest-objective iterate it visited. Measured recovery on 20 planted seeds
($K=3$, $d=4$, $N=400$): step B 16 of 20 at $\tau=\infty$ and 16 of 20 at $\tau=50$, step D 16
and 17; the failures are facets with only five or six frontier rows trapped in local optima, and
nothing is claimed about global optimality ([Mathematics](method.md#the-solver-for-small-k)).
Any other value raises `ValueError`.

**Fitted attributes** (the shapes at $K=1$ are the same with $K=1$):

- `exponents_`, shape `(K, d)`: row $k$ is $w_k$, on the simplex (A6).
- `log_offset_`, shape `(K,)`: entry $k$ is $\beta_k=J_\tau(Uw_k)$, the soft supporting offset of
  facet $k$ over the rows.
- `basis_`, shape `(K, d-1, d)`: the chart matrix $B$ stacked $K$ times, because the chart does not
  depend on $w$ and $Z$ is identical for every facet (L8).
- `facet_`, shape `(N,)`: the training assignment $\arg\max_k(w_k\cdot u-\beta_k)$, with $-1$ for a
  row with a zero metric.
- `coefficients_`, shape `(K,)`: the posynomial coefficients $c_k=e^{-\kappa\beta_k}$ of $V_K$
  (L10); at $\kappa=\infty$ the convention $\kappa=1$ gives $e^{-\beta_k}$.
- `facet_share_`, shape `(K,)`: the share of near-frontier training rows ($|\log V|<1/\tau$, or $0.1$
  at $\tau=\infty$) assigned to each facet, the analogue of explained variance; zeros if there are
  none.
- `termination_`: the stopping record of the chosen run and `conditioning_`, shape `(K,)`, the
  smallest restricted-Hessian eigenvalue per facet (see [Stopping record](#stopping-record-conditioning-and-conventions)).
- `objective_`: for $K>1$, the mean slack $\frac1N\sum_i(\beta_{k(i)}-w_{k(i)}\cdot u_i)$ of the
  partition fit. `support_weights_` combines each facet's weights on its own rows, scaled by its row
  share (sum 1).

**Methods at $K>1$.** `assign_facets(X)` returns the index of the active facet of each row (the
$\arg\max_k(w_k\cdot\log m-\beta_k)$; $-1$ for a zero metric; all zeros at $K=1$).
`score_samples` returns $\log V=\Phi_K(u)$ (L10), `transform` the chart $[Z\mid\Phi_K(u)]$, and
`inverse_transform` its inverse in closed form: since $B\mathbf 1=0$ and $\Phi_K$ is shift
equivariant, $u=B^{+}Z+(\log V-\Phi_K(B^{+}Z))\mathbf 1$, exact for every $\kappa$ because $Z$ is
the same for every facet (L8, L10). `tension_report` returns a list of $K$ reports, as above.
`invariant_value` and `project` use the score $\Phi_K$ (L10), and `improvement_factors` uses the exponents of each row's active facet (L7). A maximizer of $V$ is
Pareto-efficient in the contending metrics (L11, A1, A2); the converse is not claimed.

**Where `frontier_in_original_units`, exchange rates and contending sets apply.** Pieces that read
one $w$ describe one facet; at $K>1$ they apply facet by facet, which is how regionally varying
elasticities and several regional tensions are read.

See [Mathematics](method.md#the-posynomial-and-ggp-extension) and
[Extensions and limitations](limitations.md).

## Kernel methods (documented, not built)

The research direction is expansions in a feature space that remain generalized posynomials, so that
the programs stay geometric programs. Kernel PCA [@schoelkopf1998nonlinear] is the kin for the
feature-engineering idea; no source cited here treats kernels restricted to GP-compatible forms. The
candidate is a softmax-affine expansion anchored on support designs,

$$
\Phi(u)=\frac1\kappa\log\sum_{i\in S}\exp\!\big(\kappa\,\theta_i\cdot(u-u_i)\big),
$$
<!-- definition -->

which is again of the form $\Phi$ above, so the API shape is the same: a term set, `exponents_` of
shape `(n_terms, d)`, `log_offset_`, and `term_temperature`. A Gaussian radial basis function in log
space is log-quadratic and falls outside the family. Selecting support designs, the local normals,
the roles of the two temperatures, overfitting toward the data's convex hull and whether the novelty
and white-space semantics survive are open questions. Nothing here is built, and nothing is claimed
beyond the admissibility criterion; see [Mathematics](method.md#research-direction-kernel-methods-under-the-ggp-constraint).
