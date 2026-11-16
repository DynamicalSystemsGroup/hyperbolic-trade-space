# WP72 readout: learning the invariant rather than the trade (stage 1, a research spike)

The same posynomial invariant form, fitted by a second, two-sided loss, finds a conserved quantity from data without
being told it: the reserves of a Uniswap v2 pool give exponents (0.4989, 0.5011) against the mechanism's (1/2, 1/2),
and planted invariants come back to 4e-10 on clean tables. On the Broadbalk table the same fit says that biomass is a
size set mostly by year and treatment, not a quantity conserved within any grouping the table offers.

Files, all under `work-packages/WP72-rounds/`: `estimator.py` (the variant), `tests_planted.py` and
`results_planted.md` (G2), `wheat.md`, `wheat.py`, `results_wheat.md` (G3), `amm.md`, `fetch_amm.py`, `amm.py`,
`amm-manifest.toml`, `results_amm.md` (G4), figures in `figures/`.

## 1. The variant (G1)

**The form is unchanged.** Metrics $m\in\mathbb{R}^d_{>0}$, $u=\log m$, exponents $w\in\Delta$, and
$\log V=w\cdot u$; the level set $V=\text{const}$ is the hyperbola $m_1^{w_1}m_2^{w_2}=\text{const}$ of the paper's
definitions, and the chart is $(Z,\log V)$ with $Z=Bu$ (L8). The reach $\beta$ is not fitted: each group has its own
level.

**The loss is two-sided.** The rows carry group labels $g(i)$; a group is a set of rows taken to share the
invariant (one pool between liquidity events; one year and treatment). With $\bar u_g$ the mean log-metric of group
$g$ and $N_W$ the rows in groups of two or more, the pooled within-group scatter is
$S_W=\frac1{N_W}\sum_g\sum_{i\in g}(u_i-\bar u_g)(u_i-\bar u_g)^\top$, and the invariant fit is

$$
\begin{array}{ll}
\text{minimize} & w^\top S_W w\\
\text{subject to} & w\ge0,\quad \mathbf 1^\top w=1,
\end{array}
$$

with variable $w\in\mathbb{R}^d$. The loss is the pooled within-group variance of $\log V$; $S_W$ is positive
semidefinite, so the problem is a convex quadratic program (Boyd and Vandenberghe, Section 4.4). The level of group
$g$ is $\ell_g=w^\star\cdot\bar u_g$, an output. With one group, $S_W$ is the covariance of the table and the problem
is the long-only minimum-variance portfolio of the log columns (Markowitz 1952).

**The frontier fit is one-sided.** The paper's fitting problem (`eq-fit`) minimizes $\operatorname{lme}_\tau(Uw)$, the
soft maximum of the scores: the data lie below the level set and the fit finds how far they reach. The invariant fit
asks how little the scores spread within a group. The two meet at small temperature: on centred metrics the
log-mean-exp is $\frac\tau2 w^\top Cw+O(\tau^2)$ (L22), so the leading term of the frontier loss is the variance of
the scores; the invariant fit takes that term group by group, each group centred on its own mean. L22 does not prove
that the minimizers converge, and nothing here does.

**Scale moves are free on the simplex.** By L1, $w\cdot\mathbf 1=1$, so a row moved by $t\mathbf 1$ (every metric
multiplied by $e^t$) has its $\log V$ moved by $t$ for every $w\in\Delta$. In the chart the move changes $\log V$ and
leaves $Z$ fixed (L8: $Z(u+c\mathbf 1)=Z(u)$); a move along a level set changes $Z$ and leaves $\log V$ fixed. The
market maker's two controls are these two moves: a liquidity event scales both reserves, a swap runs along
$x_1x_2=z$. Group offsets along $\mathbf 1$ therefore add one constant to $w^\top Sw$ on the simplex and do not move
its minimizer, which is why the first differences of an ordered table (liquidity steps included) already point at
the invariant. In a finite sample the groups also sit at different positions $Z$, the cross terms do move the
pooled minimizer, and the groups are needed: pooled, the planted error is 0.019 at a level spread of 1 and 0.18 at
10 (100 rows a group).

**Against PCA in log space.** The minor axis of $S_W$ minimizes $v^\top S_Wv$ on $\|v\|=1$; when it has one sign,
renormalized to the simplex it is the invariant fit (identical on the market maker and on clean planted tables).
What the invariant fit adds: the simplex, so that $V$ is homogeneous of degree one and reads as a level in the
metrics' units (L1); the groups, so that the between-group spread does not enter; and the level $\ell_g$ as an
output. Pooled PCA, normalized by $\|v\|=1$, is pulled away from $\mathbf 1$ by the between-group spread: its minor
axis leaves the simplex once the level spread reaches the trade spread (planted, level spread 1 and above). When the
within-group minor axis has mixed signs, as on every grouping of the wheat table, no level is conserved and the fit
returns the minimum-variance point of the simplex; the report says so.

**The report.** `within_share` $=w^\top S_Ww/w^\top S_Tw$, the share of the variance of $\log V$ left within groups
(0: the level belongs to the group; 1: the groups explain nothing), read against the same number for shuffled
labels; and `flatness`, the within-group spread of the level along $w/\|w\|$ over the largest within-group spread
along the level set (0 for a conserved quantity; near or above 1 when a group's rows differ more in size than in
trade). The trade directions are the principal directions of $S_W$ on the tangent space $\{x:w\cdot x=0\}$.

**Groups unknown.** Two fallbacks, both in `estimator.py`. *Order*: for rows in time order, fit $w$ to the first
differences, cut the rows where $|\Delta\log V|$ exceeds a multiple of its robust scale, refit within the pieces.
*Levels*: cluster the values of $\log V$ (one-dimensional k-means), refit, alternate. The second is circular, since
clustering on $\log V$ makes groups of small level spread on any table; on a frontier-bounded cloud with no
invariant it reports `within_share` 0.036 against 0.054 for column-permuted tables, and a flatness of 0.26 where a
conserved quantity gives 0.005.

**K > 1.** The invariant becomes $\Phi=\frac1\kappa\log\sum_k e^{\kappa(w_k\cdot u+b_k)}$, the paper's posynomial
(L10) with the reaches free. L10's shift property $\Phi(u+t\mathbf 1)=\Phi(u)+t$ carries the scale-move argument to
$K$ terms. The loss, the within-group variance of $\Phi$, is not convex in $(w_k,b_k)$, and the package's
several-term machinery does not carry it: that machinery assigns each design to its largest term, while an additive
invariant (at $\kappa=1$, a sum of monomials) has every term active at every row. Here it is a direct minimization
over softmax parameters with 20 restarts; it recovers two planted two-term invariants to 1.5e-8. Log biomass,
$\log(\text{grain}+\text{straw})$, is the case $W=I$, $b=0$, $\kappa=1$. A stable-swap pool's invariant mixes a
constant-sum and a constant-product term (Egorov 2019); whether it is a posynomial of this shape is not checked.

**In scikit-learn's terms.** `InvariantFit` is a transformer of the decomposition family, like the frontier fit:
`fit(X, groups=None)` identifies $w$ (groups as a fit parameter, as scikit-learn's splitters take them),
`score_samples` returns $\log V$, `transform` returns the chart $(Z,\log V)$ with the package's Helmert basis. It is
a spike: no `parametrize_with_checks`, no metadata routing, no `inverse_transform`.

## 2. Results

### Planted tables (G2, R-1)

Six groups of 100 rows, trade spread 1 along the level set, group levels $\sim N(0,1)$, group positions
$\sim N(0,1)$; max-absolute exponent error, median of 5 seeds; full table in `results_planted.md`.

| table | invariant fit, groups given | order fallback | pooled, no groups | PCA within | PCA pooled | frontier fit, tau = 20 |
|---|---|---|---|---|---|---|
| clean, d = 2 and 3 | 4e-10 or less | 4e-10 or less | 0.09 to 0.11 | 1e-16 | off simplex | 0.018 to 0.025 |
| level noise 0.1, d = 2 / 3 | 0.0032 / 0.0031 | 0.023 / 0.11 | 0.087 / 0.11 | 0.0021 / 0.0056 | off simplex | 0.021 / 0.024 |
| level noise 1, d = 2 / 3 | 0.032 / 0.031 | 0.060 / 0.14 | 0.060 / 0.14 | off simplex | off simplex | 0.25 / 0.19 |
| 10 % rows mislabelled, d = 2 / 3 | 0.036 / 0.047 | labels unused | labels unused | 0.074 / off | off simplex | 0.019 / 0.023 |
| 50 % rows mislabelled, d = 2 / 3 | 0.073 / 0.089 | labels unused | labels unused | off simplex | off simplex | 0.019 / 0.023 |

- **Tolerance met:** clean recovery below 1e-6 with groups given and with the order fallback (checked); below 0.01 at
  level noise up to 0.1 (checked; the error is about 0.03 times the level noise).
- **Where it fails:** the order fallback past level noise 0.03 at d = 3 (0.019) and 0.1 at d = 2 (0.023); the levels
  fallback past noise 0.1 (0.05 and 0.10 at 0.3). Mislabelled rows bias the fit at once (0.036 at 10 per cent) but the
  report shows it: `within_share` rises from 0.001 to 0.20 at 10 per cent and 0.77 at 50.
- **The frontier fit nearly recovers the invariant on these tables**, 0.018 to 0.025, because the top group lies on
  its own level set and that level set is its supporting envelope; it leans on that one group and degrades with level
  noise (0.25 at noise 1). On the market maker it does not recover it.
- **Two terms:** $\log(m_1+m_2)$ and the pair $(0.8,0.2)$, $(0.2,0.8)$ with $b=0.3$ are recovered to 5e-10 and
  1.5e-8; a monomial fitted to the same tables leaves `within_share` 0.16 and 0.036.
- **No invariant:** on `make_frontier_data` (600 rows, d = 2 and 3) with random groups, `within_share` is 0.993 and
  0.985 and the flatness 1.36 and 1.55: a poor fit, reported as one.

### Broadbalk (G3)

Grain and straw in t/ha, 3,753 plot-years ([doi:10.23637/rbk1-yld6822-01](https://doi.org/10.23637/rbk1-yld6822-01)).

| grouping | w (grain, straw) | within_share | shuffled labels | flatness |
|---|---|---|---|---|
| year x treatment (972 groups) | (0.414, 0.586) | 0.150 | 0.728 | 1.28 |
| treatment | (0.602, 0.398) | 0.354 | 0.984 | 1.34 |
| year x section | (1.000, 0.000) | 0.695 | 0.947 | 0.80 |
| none | (0.831, 0.169) | | | 1.06 |

Year and treatment carry the level (15 per cent of its variance left within, against 73 for shuffled labels), and
log biomass does nearly as well (17.5). Within a group the plot-years spread along the size as much as along the
level set (flatness 1.28; above 0.8 in every grouping), so the level is not conserved inside any group. Within a
year and section it is the shape, log(grain/straw), that the plot-years share (28 per cent left within, against 79
for log biomass). The frontier fit on the same metrics gives (0.286, 0.714). Biomass, in the fit's own numbers, is a
size that the groups set, not an invariant the plot-years conserve.

### The market maker (G4)

Uniswap v2 DAI/WETH, 4,327 reserve updates over 30,000 blocks of August 2021, read from the public chain; his
pointer, [danlessa/uniswap](https://github.com/danlessa/uniswap) (MIT), holds the v1 analysis and model but no table
(`amm.md`).

| estimator | w (DAI, WETH) |
|---|---|
| invariant fit, 105 stretches between liquidity events given | (0.4989, 0.5011); within_share 6.3e-5, flatness 5.2e-3 |
| order fallback, no labels | (0.5008, 0.4992) |
| PCA within stretches | (0.4989, 0.5011) |
| pooled (invariant fit or PCA) | (0.520, 0.480) |
| frontier fit, tau = 152.6 | (0.000, 1.000) |

Within a stretch log V moves by 1e-8 a swap at the median; a Mint or Burn moves it by up to 6.6e-3. The 0.0011 off
(1/2, 1/2) is the 0.3 per cent fee: the product of the reserves rises at every swap, and the rise correlates with
the price inside a stretch. The order fallback catches 38 of the 39 liquidity events but cuts 975 times, because a
fee step on a large swap is as big as a small deposit. The frontier fit goes to a vertex: on a cloud this thin its
boundary carries no information about the level.

## 3. What it tells the method's users

**A dependence screen.** Before a frontier fit, the invariant fit on a candidate grouping says whether some balanced
combination of the metrics is the group's and not the design's. A small `within_share` against shuffled labels with
a small flatness is a conserved quantity (the pool); a small `within_share` with a flatness near 1 is a size that the
grouping sets (the wheat); neither is a trade. A user who sees the second learns that the metrics rise together with
something in the configuration, and that a frontier fit across groups will mix the size into the trade: the wheat
example's level V, which tracks biomass, is that mixing seen from the frontier side.

**The size-against-shape reading.** The chart already separates the two moves: $\log V$ is the size along
$\mathbf 1$ and $Z$ the shape (L8). The invariant fit names which way the rows of a group move in it: horizontally
for the market maker (the trade), vertically and horizontally alike for a Broadbalk year and treatment, vertically
for a year and section (size varies, the split is kept). One plot, $Z$ against $\log V$ coloured by group or by
order (`figures/amm-chart.png`), carries the reading.

**What it does not do.** It does not find groups that the data do not label: the levels fallback manufactures them
and the order fallback needs an order and a gap between the trade's noise and the level's steps. It keeps the model,
the fit and the analysis apart as the frontier fit does: the form is the model's, the loss is the fit's, and calling
a found $w$ an invariant of the system is the analyst's judgement, made on the flatness and the null.

## 4. What the package would expose, and at what cost

- **An estimator class**, `InvariantFit`, beside `HyperbolicTradeSpace`: the convex QP for $K=1$, groups as a fit
  parameter, the order fallback, `transform`, `inverse_transform` and `score_samples` on the existing chart. Cost:
  about 250 lines in `src/`, `parametrize_with_checks` with `groups=None` as the checks' path, metadata routing for
  `groups`, numpydoc with doctests.
- **A report**, `within_share`, flatness and the shuffled-label null for each candidate grouping (the wheat table's
  rows). Cost: one function, about 60 lines.
- **A plot**, the chart coloured by group or order. Cost: one function in `plotting.py`, reusing
  `plot_frontier_coordinates`.
- **Derivation:** the scale-move statement (a corollary of L1 with L8) and the group-by-group reading of L22, as
  lemma steps; the convexity of the QP is a citation.
- **Docs:** one page with the market maker as its example; the data need a durable source (the free public endpoint
  used here limits each query to a narrow block range and refuses Python's HTTP client) or his own table.
- **$K>1$:** nonconvex, a separate solver with restarts and no certificate; the largest cost and the least tested.

## 5. Decisions that are his

1. **What the variant becomes.** (a) A second estimator of the package, with its report and plot. (b) A section in
   the docs: the size-against-shape reading on the existing chart, with the computation as a recipe. (c) A readout in
   `notes/directions/` and nothing more for now.
2. **How groups enter.** (a) The user supplies them; no fallback. (b) The order fallback for time-ordered tables, with
   its limits stated. (c) Both fallbacks, each reported against a permutation null.
3. **The market-maker data for the next stage.** (a) The v2 DAI/WETH window fetched here. (b) His v1 ETH/DAI history,
   rebuilt from the collaborator repository's BigQuery query (needs a Google Cloud account he holds). (c) Both.
4. **Several terms.** (a) Kept a stated extension, tested on planted tables only. (b) Built in the next stage against
   a stable-swap pool's reserves.
5. **The wheat example (WP71).** (a) It cites this finding in a sentence: biomass is a size set by year and
   treatment, not conserved within groups. (b) It stays with V against biomass alone.

## Sources

- Boyd, S. and Vandenberghe, L. (2004), *Convex Optimization*, Cambridge University Press,
  [doi:10.1017/CBO9780511804441](https://doi.org/10.1017/CBO9780511804441).
- Glendining, M. and Poulton, P. (2023), *Broadbalk Wheat annual grain and straw yields 1968-2022*, Electronic
  Rothamsted Archive, [doi:10.23637/rbk1-yld6822-01](https://doi.org/10.23637/rbk1-yld6822-01), CC BY 4.0.
- Markowitz, H. (1952), Portfolio selection, *The Journal of Finance* 7(1), 77-91,
  [doi:10.1111/j.1540-6261.1952.tb01525.x](https://doi.org/10.1111/j.1540-6261.1952.tb01525.x).
- Adams, H., Zinsmeister, N. and Robinson, D. (2020), *Uniswap v2 Core*,
  [app.uniswap.org/whitepaper.pdf](https://app.uniswap.org/whitepaper.pdf).
- Egorov, M. (2019), *StableSwap: efficient mechanism for Stablecoin liquidity*,
  [classic.curve.fi/files/stableswap-paper.pdf](https://classic.curve.fi/files/stableswap-paper.pdf).
- danlessa/uniswap, *Uniswap cadCAD models and data analyses*, commit `cd768a7`, MIT,
  [github.com/danlessa/uniswap](https://github.com/danlessa/uniswap).
- Uniswap v2 DAI/WETH pair, Ethereum mainnet,
  [`0xa478c2975ab1ea89e8196811f51a7b7ade33eb11`](https://etherscan.io/address/0xa478c2975ab1ea89e8196811f51a7b7ade33eb11),
  blocks 12,959,744 to 12,989,743, read through [eth.drpc.org](https://drpc.org)
  ([JSON-RPC API](https://ethereum.org/en/developers/docs/apis/json-rpc/)); hashes in `amm-manifest.toml`.
