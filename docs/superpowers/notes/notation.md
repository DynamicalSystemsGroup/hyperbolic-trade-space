# The register: mathematical expressions and their meaning in the paper (settled with the supervisor, 2026-11-08)

This note is the register (the supervisor, 2026-11-08: "a separate supporting table for
mathematical expressions and their meaning in the context of our paper ... we can resolve
wordsmithing for math concepts in the register so we don't end up with destructive resonance or
limit cycles in prose"). For each expression it fixes the formal object, the one phrase the prose
uses for it, what it is not, and where it is defined or proved. Wording disputes about the
mathematics are settled here, once; the prose uses the register's phrase and does not re-argue it.
It is published as the paper's supporting table (Appendix A of the supporting material).

Source of the paper's notation block (WP10) and the vocabulary of the K > 1 package (WP9). Each
row: the symbol, its name, what it means in the model, the PCA analogue where one helps, the name
in code, what it is not, and where it is defined or proved. Rows marked "WP9" are new or changed
by the solver package; rows marked "WP13" by the response to the external review. Settled in chat
with the supervisor; his verbatim remarks are in `work-packages/WP9-decisions.md`,
`work-packages/WP10-decisions.md` and `work-packages/external-review-2026-11.md`. Wording is for
the record; the paper presents it more briefly. Lemma ids (L1 to L14) are the scripts in
`derivation/`; ledger ids (A, I, R, F) are the entries of `derivation/axioms.py`; G-ids are the
rows of `docs/superpowers/notes/abstraction-gaps.md`.

Reader model (the supervisor's): multivariate calculus, linear algebra, convex optimization.
Mathematical notation follows Boyd and Vandenberghe (`boyd2004convex`); data and estimator terms
follow the scikit-learn documentation.

| Symbol | Name | Interpretation | PCA analogue | In code | What it is not | Where defined |
|---|---|---|---|---|---|---|
| $N$ | number of designs | rows of the table; each a configuration that was evaluated | `n_samples` | `n_samples` | a sample drawn from the attainable set; the designs are chosen by a simulator or an analyst (G-12) | `docs/method.md`, The model |
| $d$ | number of metrics | the length of the metric vector; how many things you care about; the dimension the trade space lives in | number of variables | `n_features` | the number of configuration variables | `docs/method.md`, The model; A0 |
| $c$ | configuration | the design variables the engineer chooses (wheel class, gains); not fitted; carried as covariates | | configuration columns | an input of the fit; the fit sees attributes and metrics only | `docs/method.md`, Prediction from configuration |
| $a$ | attributes | what the evaluation returns (seconds, kilograms); raw, mixed units and directions. The evaluation is a black box to the method: a simulator behind a system model, a physical test, or a human assessment (the supervisor: "we're keeping an abstraction of config variables and measured attributes so our method is relevant even as tools move, or in cases where scoring comes from physical systems or human assessments") | | attribute columns | metrics: attributes are not conditioned, positive or oriented | `docs/method.md`, The pipeline; A4 |
| $m\in\mathbb{R}^d_{++}$ | metrics | the conditioned attributes: positive, larger is better, comparable log-spread; the input to the fit | the data matrix $X$ | `X`, shape `(N, d)` | the raw attributes; zero is tolerated in data and masked in the fit (G-5) | A1, A4; L9 |
| $u=\log m$ | log-metrics | the tractable space; every fit happens here; a monomial becomes a hyperplane | | `U` | the chart coordinates $Z$ | L1; A1 |
| $K$ | number of terms | how many monomials the frontier has; how many distinct trade-off regimes the fit may find; the analyst's choice (WP9 OD1: no automatic selection) | number of components retained | `n_terms` | a selected or estimated quantity; the fit does not choose $K$ | L10; A6; `docs/method.md`, The posynomial and GGP extension |
| $w_k\in\Delta$ ($\theta_k$ in L10) | exponent vector of term $k$ | the $k$-th monomial: a point on the simplex over the $d$ metrics; its positive entries say which metrics contend on that facet and its ratios give the elasticities; sparse by design | the $k$-th principal component (a direction), but on the simplex and not orthogonal to the others | `exponents_[k]`, shape `(K, d)` | a loading vector with sign or unit norm; $\lVert w\rVert_1=1$ and $w\ge0$ (A2); unique only where the restricted Hessian is positive definite (G-2) | A2; L3 (KKT), L4 |
| $n_k=\lvert\{j: w_{kj}>0\}\rvert$ | size of the n-lemma of term $k$ | how many of the $d$ metrics contend on facet $k$; a dilemma is 2, a trilemma 3; found, not assumed | | `TensionReport.n_lemma` per facet (WP9: a list) | a count of metrics in tension in the data; it counts exponents above the participation threshold | L3; G-2 |
| $\beta_k$, $e^{\beta_k}$, $c_k=e^{-\kappa\beta_k}$ | reach of term $k$; its lead coefficient | how far the achievable region extends in the direction of trade-off $k$: $\beta_k$ is the support value of the data in direction $w_k$, $e^{\beta_k}$ the best composite score of facet $k$'s contending metrics that any design reaches, and $c_k$ the rescaling that puts that reach at $V=1$. Comparing $\beta_k$ across facets says which trade-offs the designs have pushed furthest; a uniform shift of the metrics moves every $\beta_k$ by the same amount (L2), so the comparison is invariant and the absolute level is relative to the conditioning's reference point. At $K=1$ the normalization sets $\beta$ to zero and $c$ to one. | the singular value: how far the data extend along the component, except one-sided: the reach of the edge rather than the spread of the middle | `log_offset_[k]`; `coefficients_` (WP9) | an unbiased measurement of the attainable limit: it is the log-mean-exp of a finite sample (G-3), and the Pareto boundary may lie beyond it (G-1) | L2, L5 (log-mean-exp), L10 ($c_k$) |
| $\mathrm{share}_k$ | facet share | the fraction of near-frontier designs assigned to facet $k$; which facets explain most of the frontier | the explained-variance ratio | `facet_share_` (WP9) | the fraction of all designs on the facet (`Termination.shares` is that, the row share $\lvert C_k\rvert/N$); depends on the band $1/\tau$ (G-9) | `docs/method.md`, The posynomial and GGP extension |
| facet $k$; term $k$ | facet; term; monomial | one object seen three ways: the term of the posynomial, the product of powers, the flat piece of the fitted surface in log space; the prose says "facet" for the geometry and "term" for the algebra | a cluster and its component | `exponents_[k]`, `log_offset_[k]` | a face of the Pareto boundary or of the data's convex hull | L10 |
| $V(m)=\prod_j m_j^{w_j}$ ($K=1$) | invariant value | a weighted geometric mean of the metrics; doubling all metrics doubles $V$ (L1), so $V$ reads as a factor of improvement | the score along a component | `score_samples` returns $\log V$ | a probability or a bounded score; $V>1$ is possible at finite $\tau$ (G-1) | L1; A1, A2 |
| $V_K(m)=\big(\sum_k c_k\prod_j m_j^{\kappa w_{kj}}\big)^{1/\kappa}$ | the posynomial | the $K$-term value; its level surfaces exist at every value; $V=1$ is placed at the fitted reference surface by normalization so results read as factors of improvement | | WP9 | a sum of the term values at $\kappa=\infty$ (there it is their maximum) | L10; I4; A6 |
| $\Phi_K(u)=\tfrac1\kappa\log\sum_k\exp(\kappa(w_k\cdot u-\beta_k))$ | log of $V_K$ | softmax-affine in log space; a soft maximum of the $K$ hyperplanes, within $(\log K)/\kappa$ above the hard maximum; at $\kappa\to\infty$ the hard maximum, the envelope | | WP9 | a log-mean-exp (that is the form of $\beta$): $\Phi_K$ is the log-sum-exp of the scores, with $\max_k x_k\le\Phi_K\le\max_k x_k+(\log K)/\kappa$ | L10, F10 |
| $\Phi(u)=w\cdot u-\beta=0$, $V=1$ at finite $\tau$ ($\beta=J_\tau(Uw)$) | fitted reference surface | the object the fit returns at finite $\tau$: the level $V=1$ of the fitted invariant; inside is $V<1$, beyond is $V>1$; rows above it exist by construction (`frac_above_`). The prose says "fitted reference surface", or "frontier" where the context fixes this object | | `exponents_`, `log_offset_`, `temperature` finite; `frac_above_` | the Pareto boundary; a bound that no design exceeds | L3, L5; G-1 |
| $\max_i w\cdot u_i=\beta$ ($\tau=\infty$) | supporting envelope | the $\tau=\infty$ fit: the exact maximum, a linear program; the hyperplane that supports the observed rows from above, with none above it. The prose says "supporting envelope" | | `temperature=np.inf` | an envelope of the attainable set; it is determined by the sample (its extreme rows) | L5 (limit), I1 (LP duality); G-1 |
| $\{y\ \text{attainable}:\ \text{no attainable } y'\ge y,\ y'\ne y\}$ | Pareto boundary | the set of nondominated points of the attainable set, a property of the system the data sample. The prose says "Pareto boundary". L11: a maximizer of $V$ is weakly efficient; the converse is not claimed | | none; on planted data the planted facets (`info["frontier_mask"]`) | the fitted reference surface or the supporting envelope; identified with them by no lemma | L11; A1, A2; G-1, G-13 |
| $\log V=\Phi(u)$ | energy differential (level offset) | the potential $\Phi(u)=w\cdot u-\beta$ evaluated at the design, relative to the fitted reference surface's zero level; a path-independent difference; equal by L1 and L2 to the uniform log-scaling step that carries the design onto the surface (the improvement factor's logarithm); negative inside, positive beyond. Per facet, $s_{ik}=w_k\cdot u_i-\beta_k$ is the energy differential of design $i$ against facet $k$ (the wording of L13); at $K>1$, $\log V=\Phi_K$ of the scores. The prose says "energy differential" or "level offset"; "distance" only in the sense below | | `transform(X)[:, -1]`, `score_samples` | a Euclidean distance: the signed Euclidean distance to the hyperplane is $\Phi(u)/\lVert w\rVert_2$ | L1, L2, L13; `docs/method.md`, The chart |
| $Z\in\mathbb{R}^{d-1}$ | position along the frontier | the other $d-1$ chart coordinates (Helmert log-ratios, L8); free of overall scale; where in the trade space a design sits; holes in $Z$ are white space | the scores in the component basis | `transform(X)[:, :-1]`, `basis_` | a position on the Pareto boundary; it is a position on the log-ratio chart | L8; A7, I6 |
| $(Z,\log V)\leftrightarrow m$ | the chart | the reversible transformation between metric space and the fitting space (L8, L9); nothing is lost either way | | `transform`, `inverse_transform` | defined for a row with a zero metric: such a row has $Z=$ `nan` and no inverse (G-5) | L8, L9 |
| $\tau$ | fit temperature | how hard the maximum is in the one-sided fit; $\tau=\infty$ is the exact maximum (a linear program); finite $\tau$ gives a band of near-frontier designs, $\lvert\log V\rvert<1/\tau$ (the code's convention; $J_\tau$ is within $(\log n)/\tau$ of the maximum, L5); chosen so a target fraction of designs lies above $V=1$ | | `temperature`, `select_temperature` | a noise level or a model parameter fitted from the data; re-selected at each $K$ (G-9) | L5; A3; G-9 |
| $\kappa$ | term temperature | how sharply the $K$ facets meet: $\kappa\to\infty$ is a crisp envelope with corners; finite $\kappa$ rounds the corners | | `term_temperature` (reserved today; used in WP9) | the fit temperature $\tau$ | L10; A6 |
| $p_i$ | support weights | the softmax weights of the designs in the fit (L3); which designs hold up the fitted surface; their inverse sum of squares is the effective sample size | | `support_weights_`, `n_eff_` | probabilities of a sampling model | L3; A3 |
| contending set | support of $w$ at $\tau=\infty$ | the metrics with positive exponent in the exact-maximum fit; the n-lemma's members | the nonzero loadings of a sparse component | `TensionReport.contending_set` | the metrics above the participation threshold at the working temperature (those are the participants); a statement about the whole system | L3, I1; G-2, G-12 |
| participation threshold | participating exponent | a working-temperature exponent above $10^{-3}$ (`PARTICIPATION_THRESHOLD`) participates; at or below $10^{-12}$ (`EPS_ZERO_EXPONENT`) it is numerically zero; the LP support uses $10^{-9}$ | the loading cutoff of a sparse component | `PARTICIPATION_THRESHOLD`, `EPS_ZERO_EXPONENT`, `tension_report(threshold=...)` | a statistical test; "numerically zero" is not "mathematically zero" | G-2, G-5 |
| `conditioning_` | conditioning of the exponents | the smallest eigenvalue of the restricted Hessian $\tau(U^\top\mathrm{diag}(p)U-(U^\top p)(U^\top p)^\top)$ of $J_\tau$ at each facet's fit, on the simplex tangent space and the participating exponents; small means a nearly flat direction | the gap to the next eigenvalue | `conditioning_`, shape `(n_terms,)`; `nan` at $\tau=\infty$ | a confidence interval; it is a local sensitivity of the objective at the fit | L3, L4, R1; G-2 |
| $-w_k/w_j$ | elasticity between metrics $j$ and $k$ | along the facet, $\mathrm{d}\log m_j/\mathrm{d}\log m_k=-w_k/w_j$: the percentage change of metric $j$ per percentage change of metric $k$; constant within a facet, different between facets (L7) | | `TensionReport.elasticities` | a causal exchange or an intervention effect: a feature of the conditioned empirical model (G-3) | L7; A1, A2; G-3 |
| facet of design $i$ | assignment | which term is active for design $i$ (the largest $w_k\cdot u_i-\beta_k$); defines the regions of the manifold | cluster membership | `facet_`, `assign_facets(X)` (WP9) | an identity that survives ties between scores (G-10); the facet index is a label | L13; R2; G-10 |
| $G_k(w_k)=g\cdot w_k-\min_jg_j$ | facet gap (WP13) | the first-order gap of facet $k$'s refit $f_k(w)=J_\tau(Uw)-\bar u_k\cdot w$ on the simplex, $g=\nabla f_k(w_k)$; $0\le f_k(w_k)-f_k^*\le G_k$; zero iff the simplex KKT holds; at $\tau=\infty$, with the LP duals, the LP duality gap | the residual of an eigenvalue problem | `facet_gap`, `simplex_gap`, `Termination.gaps`, `Termination.max_gap` | the distance to the optimum; it bounds the objective error only where $f_k$ is convex (I8), so it is a diagnostic under the penalty or the tangent step (G-8) | L12; L3 (KKT), L4; I8, F12 |
| $F(W)-F^*_{\text{fixed}}\le\sum_k\frac{\lvert C_k\rvert}{N}G_k$ | Corollary bound (WP13) | for the fixed assignment of the returned run, the mean slack exceeds the fixed-assignment optimum by at most the share-weighted sum of the facet gaps | | `Termination.bound`, `fixed_assignment_bound` | a bound across restarts (G-15) | L14 |
| $\gamma=\min_i[s_{i,k(i)}-\max_{k\ne k(i)}s_{ik}]$ | assignment margin (WP13) | the smallest gap by which a row's facet beats the runner-up; positive means unique maximizing facets | | `assignment_margin`, `Termination.gamma` | the objective's margin; zero on ridge rows at $\tau=\infty$ and for identical facets (G-10) | L13; R2 |
| $\gamma/(2\max_i\lVert(u_i,-1)\rVert_2)$ | stable radius (WP13) | any perturbation of every $(w_k,\beta_k)$ with Euclidean norm below it leaves each row's maximizing facet unchanged | | `Termination.radius` | a bound on estimation error; sufficient, not tight | L13; I9, R2 |
| status | termination status (WP13) | which of the three levels the returned run meets: `certified` (assignment fixed, residuals at most $10^{-9}$, $\max_kG_k\le10^{-8}$, no empty facet, $\gamma>10^{-9}$), `stationary_without_margin`, `uncertified`, `guard_stop`, `iteration_cap`, `not_applicable` | | `termination_.status`, `Termination` | a statement about the choice among restarts (G-15); `not_applicable` is not a failure (G-8) | L12 to L14; G-15, G-16 |
| level 1, 2, 3 | the three levels of guarantee (WP13) | 1 descent of the mean slack (step B, up to the guard tolerance $10^{-12}$); 2 numerical stationarity (per-facet gap and feasibility residuals within tolerance); 3 conditional local optimality of the fixed assignment (Proposition 3, step B, unpenalized, support offsets) | | `Termination` fields | global optimality or convergence (G-14) | L12 (levels 1, 2), L13, L14 (level 3); I7 |
| `min_exponent` | floor rule | the existing way to keep a metric in or out of the product: a lower bound on every exponent; with the $\tau=\infty$ support and the working-temperature threshold, the existing sparsity rule | | parameter | a regularizer | `docs/api.md`; G-2 |
| `penalty`, `alpha` | sparsity regularization | the regularization-based alternative (WP9 OD4): reweighted $\ell_1$ on the simplex (Candès, Wakin and Boyd 2008) drives small exponents to exact zero; `alpha` sets how hard; exact zeros are safe (a zero exponent removes the metric from the product; the log/exp hazard is a zero metric, which is masked) | the sparsity knob of sparse PCA | parameters (WP9) | covered by Proposition 3: the status is `not_applicable` (G-8) | `docs/api.md`; G-8 |
| improvement factor | | the factor on one metric alone that brings a design to $V=1$: $V^{-1/w_j}$ (L7) | | `TensionReport`, L7 | the factor that brings the design to the Pareto boundary | L7 |
| $T_k=\{v: w_k\cdot v=0\}$ and its normal $w_k=\nabla_u\log V$ on facet $k$ | tangent space and ascent direction of term $k$ | On facet $k$ the level surfaces of $V$ are flat in log space, so the tangent space is the set of moves that trade one contending metric for another at the facet's elasticities and leave $V$ unchanged (L7); the normal, $w_k$, is the gradient of $\log V$ (L3): the steepest way up the level surfaces, pushing exactly the contending metrics in proportion to their exponents. Chained back through the conditioning (L9: $\partial\log V/\partial\log a_j=w_{kj}\alpha_j a_j/(a_j+s_j)$) and through the evaluation map, $\nabla_c\log V=J_f(c)^{\top}\nabla_a\log V$, it is a direction in configuration space: which design variables to change, and in what proportion, to move a design up toward $V=1$ and beyond. $J_f$ has no closed form and is estimated (finite differences on the simulator, or the gradient of the supervised regressor $c\mapsto\log V$). The data are not exhaustive, so a step the fit predicts would cross $V=1$ is a proposal for the next experiment: trade-off breaking as a hypothesis to test, and a way to scope new experiments dynamically. Discussion and Future work in the paper. | moving in $T_k$ keeps $V$ and moving along $w_k$ changes it, so the normal plays the role the component direction plays in PCA | elasticities (`TensionReport`, L7); the log-space gradient is `exponents_[k]`; the chain to configurations is future work (`TradeSpaceRegressor` is the supervised map today) | a verified intervention: a step across $V=1$ is a hypothesis for the next experiment (G-3, G-13) | L3, L7, L9 |
| A0 to A7, I1 to I9, R1, R2, F5, F10, F12 (I7 solver level) | the ledger | what the theory assumes, inherits or falls back on, each with its interpretive role and failure mode; the WP13 entries are I8, I9, F12 and R2 below | | `derivation/axioms.py` | a list of defects: hypotheses are interpretive conditions | `docs/superpowers/notes/proof-conventions.md`; `derivation/run.py` (audit) |
| I8, I9, F12, R2 (WP13) | the ledger entries of the three levels | I8 first-order convexity inequality (Boyd and Vandenberghe 3.1.3): turns the facet gap into an objective bound; I9 Cauchy-Schwarz: gives the stable radius; F12 minimum representation (as F5, F10): the symbolic-$d$ minimum in L12 and L13; R2 positive assignment margin: the hypothesis of Proposition 3, which fails on ridge rows and for identical facets, where the status is `stationary_without_margin` | | `derivation/axioms.py` | assumptions about the data that hold by construction: R2 is checked on the fit and reported in `termination_` (G-16) | L12 (I8, F12), L13 (F12, I9, R2), L14 (R2); G-10, G-16 |

Words. "Term", "monomial" and "facet" are one object seen three ways: the term of the posynomial,
the product of powers, the flat piece of the fitted surface in log space. The paper says so once,
then uses "facet" for the geometry and "term" for the algebra. The level surfaces of $V$ are the
"energy levels": the tangent space is motion on a level, the normal is motion between levels, and
"better" is up. "n-lemma" is per facet: at $K=3$ there are three contending sets, and "the
6-lemma" of the WP7 notebook is "the single facet's 6-lemma at $K=1$".

Three objects carry the word "frontier" in everyday use and the prose names them by the register's
phrases: "fitted reference surface" for the finite-$\tau$ $\Phi=0$ object, "supporting envelope"
for the $\tau=\infty$ object, "Pareto boundary" for the attainable set's. "Frontier" alone is
allowed where the context fixes the object. $\log V$ is the "energy differential" or the "level
offset"; "distance" is used only in the sense of the energy differential row (the signed Euclidean
distance to the hyperplane is $\Phi(u)/\lVert w\rVert_2$). The assignment margin, the stable radius
and the facet gap are named as in their rows. A zero exponent below $10^{-12}$ is "numerically
zero"; "mathematically zero" is reserved for the formal object.

Left out on purpose: novelty $V-1$ as a score for new capabilities is the paper's final remark
(future work), not a notation of the body.

## Register phrases

Each phrase below appears in the documents under `docs/` taken together (a test checks this).

- `fitted reference surface`
- `supporting envelope`
- `Pareto boundary`
- `energy differential`
- `level offset`
- `facet gap`
- `assignment margin`
- `stable radius`
- `participation threshold`
- `numerically zero`
- `regime`

## Forbidden phrases

Each phrase below is absent from the documents under `docs/` other than this note and the review
records in `work-packages/` (a test checks this). The replacement is the register's phrase.

- `Euclidean distance to the frontier`
- `distance to the frontier`
- `distance from the frontier`
- `unbiased estimator`
- `unbiased estimate`
- `consistent estimator`
- `statistically consistent`
- `globally optimal`
- `global optimum`
- `empirical envelope`
- `the true frontier`
- `guaranteed to find`
- `the three regimes`

The word `regime` denotes a gain-box dataset of the case (the primary regime, aggressive controller
gains, or the stock regime), and only that. A facet of the fit is a facet, never a regime: the
forbidden phrase `the three regimes` is the misuse. (The shorter "three regimes" cannot be listed:
the preserved snapshot `paper-sources/method.md` says "needs three regimes", and a snapshot is not
edited.)
