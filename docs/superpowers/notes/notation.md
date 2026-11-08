# Note: notation and interpretations (settled with the supervisor, 2026-11-08)

Source of the paper's notation block (WP10) and the vocabulary of the K > 1 package (WP9). Each
row: the symbol, its name, what it means in the model, the PCA analogue where one helps, and the
name in code. Rows marked "WP9" are new or changed by the solver package. Settled in chat with
the supervisor; his verbatim remarks are in `work-packages/WP9-decisions.md` and
`work-packages/WP10-decisions.md`. Wording is for the record; the paper presents it more briefly.

Reader model (the supervisor's): multivariate calculus, linear algebra, convex optimization.
Mathematical notation follows Boyd and Vandenberghe (`boyd2004convex`); data and estimator terms
follow the scikit-learn documentation.

| Symbol | Name | Interpretation | PCA analogue | In code |
|---|---|---|---|---|
| $N$ | number of designs | rows of the table; each a configuration that was evaluated | `n_samples` | `n_samples` |
| $d$ | number of metrics | the length of the metric vector; how many things you care about; the dimension the trade space lives in | number of variables | `n_features` |
| $c$ | configuration | the design variables the engineer chooses (wheel class, gains); not fitted; carried as covariates | | configuration columns |
| $a$ | attributes | what the evaluation returns (seconds, kilograms); raw, mixed units and directions | | attribute columns |
| $m\in\mathbb{R}^d_{++}$ | metrics | the conditioned attributes: positive, larger is better, comparable log-spread; the input to the fit | the data matrix $X$ | `X`, shape `(N, d)` |
| $u=\log m$ | log-metrics | the tractable space; every fit happens here; a monomial becomes a hyperplane | | `U` |
| $K$ | number of terms | how many monomials the frontier has; how many distinct trade-off regimes the fit may find; the analyst's choice (WP9 OD1: no automatic selection) | number of components retained | `n_terms` |
| $w_k\in\Delta$ ($\theta_k$ in L10) | exponent vector of term $k$ | the $k$-th monomial: a point on the simplex over the $d$ metrics; its positive entries say which metrics contend on that facet and its ratios give the exchange rates; sparse by design | the $k$-th principal component (a direction), but on the simplex and not orthogonal to the others | `exponents_[k]`, shape `(K, d)` |
| $n_k=\lvert\{j: w_{kj}>0\}\rvert$ | size of the n-lemma of term $k$ | how many of the $d$ metrics contend on facet $k$; a dilemma is 2, a trilemma 3; found, not assumed | | `TensionReport.n_lemma` per facet (WP9: a list) |
| $\beta_k$, $e^{\beta_k}$, $c_k=e^{-\kappa\beta_k}$ | reach of term $k$; its lead coefficient | how far the achievable region extends in the direction of trade-off $k$: $\beta_k$ is the support value of the data in direction $w_k$, $e^{\beta_k}$ the best composite score of facet $k$'s contending metrics that any design reaches, and $c_k$ the rescaling that puts that reach at $V=1$. Comparing $\beta_k$ across facets says which trade-offs the designs have pushed furthest; a uniform shift of the metrics moves every $\beta_k$ by the same amount (L2), so the comparison is invariant and the absolute level is relative to the conditioning's reference point. At $K=1$ the normalization sets $\beta$ to zero and $c$ to one. | the singular value: how far the data extend along the component, except one-sided: the reach of the edge rather than the spread of the middle | `log_offset_[k]`; `coefficients_` (WP9) |
| $\mathrm{share}_k$ | facet share | the fraction of near-frontier designs assigned to facet $k$; which facets explain most of the frontier | the explained-variance ratio | `facet_share_` (WP9) |
| $V(m)=\prod_j m_j^{w_j}$ ($K=1$) | invariant value | a weighted geometric mean of the metrics; doubling all metrics doubles $V$ (L1), so $V$ reads as a factor of improvement | the score along a component | `score_samples` returns $\log V$ |
| $V_K(m)=\big(\sum_k c_k\prod_j m_j^{\kappa w_{kj}}\big)^{1/\kappa}$ | the posynomial | the $K$-term value; its level surfaces exist at every value; $V=1$ is placed at the frontier by normalization so results read as factors of improvement | | WP9 |
| $\Phi_K(u)=\tfrac1\kappa\log\sum_k\exp(\kappa(w_k\cdot u-\beta_k))$ | log of $V_K$ | softmax-affine in log space; a soft maximum of the $K$ hyperplanes; at $\kappa\to\infty$ the hard max, the envelope (L10) | | WP9 |
| $V=1$, $\Phi=0$ | the frontier | the fitted edge of the achievable; inside is $V<1$, beyond is $V>1$ | | |
| $\log V$ | distance from the frontier | one coordinate of the chart; negative inside, positive beyond | | `transform(X)[:, -1]` |
| $Z\in\mathbb{R}^{d-1}$ | position along the frontier | the other $d-1$ chart coordinates (Helmert log-ratios, L8); free of overall scale; where in the trade space a design sits; holes in $Z$ are white space | the scores in the component basis | `transform(X)[:, :-1]`, `basis_` |
| $(Z,\log V)\leftrightarrow m$ | the chart | the reversible transformation between metric space and the fitting space (L8, L9); nothing is lost either way | | `transform`, `inverse_transform` |
| $\tau$ | fit temperature | how hard the maximum is in the one-sided fit; $\tau=\infty$ is the exact maximum (a linear program); finite $\tau$ gives a band of near-frontier designs of half-width $1/\tau$ in $\log V$ (L5); chosen so a target fraction of designs lies above $V=1$ | | `temperature`, `select_temperature` |
| $\kappa$ | term temperature | how sharply the $K$ facets meet: $\kappa\to\infty$ is a crisp envelope with corners; finite $\kappa$ rounds the corners | | `term_temperature` (reserved today; used in WP9) |
| $p_i$ | support weights | the softmax weights of the designs in the fit (L3); which designs hold up the frontier; their inverse sum of squares is the effective sample size | | `support_weights_`, `n_eff_` |
| contending set | support of $w$ at $\tau=\infty$ | the metrics with positive exponent in the exact-maximum fit; the n-lemma's members | the nonzero loadings of a sparse component | `TensionReport.contending_set` |
| $-w_k/w_j$ | exchange rate between metrics $j$ and $k$ | the percentage of metric $k$ you get for a percentage of metric $j$ given up, on that facet; constant within a facet, different between facets (L7) | | `TensionReport.exchange_rates` |
| facet of design $i$ | assignment | which term is active for design $i$ (the largest $w_k\cdot u_i-\beta_k$); defines the regions of the manifold | cluster membership | `facet_`, `assign_facets(X)` (WP9) |
| `min_exponent` | floor rule | the existing way to keep a metric in or out of the product: a lower bound on every exponent; with the $\tau=\infty$ support and the working-temperature threshold, the existing sparsity rule | | parameter |
| `penalty`, `alpha` | sparsity regularization | the regularization-based alternative (WP9 OD4): reweighted $\ell_1$ on the simplex (Candès, Wakin and Boyd 2008) drives small exponents to exact zero; `alpha` sets how hard; exact zeros are safe (a zero exponent removes the metric from the product; the log/exp hazard is a zero metric, which is masked) | the sparsity knob of sparse PCA | parameters (WP9) |
| improvement factor | | the factor on one metric alone that brings a design to $V=1$: $V^{-1/w_j}$ (L7) | | `TensionReport`, L7 |
| $T_k=\{v: w_k\cdot v=0\}$ and its normal $w_k=\nabla_u\log V$ on facet $k$ | tangent space and ascent direction of term $k$ | On facet $k$ the level surfaces of $V$ are flat in log space, so the tangent space is the set of moves that trade one contending metric for another at the facet's exchange rates and leave $V$ unchanged (L7); the normal, $w_k$, is the gradient of $\log V$ (L3): the steepest way up the level surfaces, pushing exactly the contending metrics in proportion to their exponents. Chained back through the conditioning (L9: $\partial\log V/\partial\log a_j=w_{kj}\alpha_j a_j/(a_j+s_j)$) and through the evaluation map, $\nabla_c\log V=J_f(c)^{\top}\nabla_a\log V$, it is a direction in configuration space: which design variables to change, and in what proportion, to move a design up toward $V=1$ and beyond. $J_f$ has no closed form and is estimated (finite differences on the simulator, or the gradient of the supervised regressor $c\mapsto\log V$). The data are not exhaustive, so a step the fit predicts would cross $V=1$ is a proposal for the next experiment: trade-off breaking as a hypothesis to test, and a way to scope new experiments dynamically. Discussion and Future work in the paper. | moving in $T_k$ keeps $V$ and moving along $w_k$ changes it, so the normal plays the role the component direction plays in PCA | elasticities and exchange rates (`TensionReport`, L7); the log-space gradient is `exponents_[k]`; the chain to configurations is future work (`TradeSpaceRegressor` is the supervised map today) |
| A1–A6, I1–I4, F5, F10 (+ I7 in WP9) | the ledger | what the theory assumes, inherits or falls back on, each with its interpretive role and failure mode | | `derivation/axioms.py` |

Words. "Term", "monomial" and "facet" are one object seen three ways: the term of the posynomial,
the product of powers, the flat piece of the frontier in log space. The paper says so once, then
uses "facet" for the geometry and "term" for the algebra. The level surfaces of $V$ are the
"energy levels": the tangent space is motion on a level, the normal is motion between levels, and
"better" is up. "n-lemma" is per facet: at $K=3$ there are three contending sets, and "the
6-lemma" of the WP7 notebook is "the single facet's 6-lemma at $K=1$".

Left out on purpose: novelty $V-1$ as a score for new capabilities is the paper's final remark
(future work), not a notation of the body.
