# Reading the tension report

`tension_report(estimator, X)` returns a frozen `TensionReport` that says which metrics contend and
how they trade. The model looks for the binding constraint, so the report describes a tension, where
PCA would describe spread.

```python {.runnable}
from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data, tension_report

X, info = make_frontier_data(300, 3, random_state=0)
ts = HyperbolicTradeSpace(temperature=20.0).fit(X)
report = tension_report(ts, X)
print(report.contending_set, report.n_lemma, report.lemma_name)
print(report.exchange_rates.round(2))
```

## The contending set and the n-lemma

`contending_set` holds the metrics with positive exponent in the exact-maximum fit (tau = infinity,
exponents above 1e-9). `n_lemma` is its size and `lemma_name` names it: monolemma, dilemma,
trilemma, then an n-lemma. The set is found, not assumed: a facet of the achievable region on which
exactly n metrics contend. The report solves the tau = infinity program itself, independent of the
fitted temperature. `min_exponent` must be 0 for this reading, because a positive floor masks the
sparsity; the report warns when the estimator was fitted with a floor.

## Participation and exchange rates

At the working temperature the exponents are smoothed, so a small one means weak participation, not
membership. `participating` marks metrics whose exponent exceeds the participation threshold
(`threshold`, default 1e-3); an exponent at or below 1e-12 is numerically zero. `exchange_rates[j, k]`
is the elasticity along the surface: the percentage change of metric j per percentage change of
metric k, constant on a facet and `nan` where metric j does not participate. It
describes a feature of the fitted model, not a causal exchange.

## Association among near-frontier designs

For designs with absolute log V below `band` (by default 1/tau, or 0.1 at infinite tau),
`association` is the Pearson or Spearman correlation of the log-metrics: negative is traded, positive
is aligned. Near the surface the weighted sum of log-metrics is almost constant, so a binding
constraint produces negative association even where no designer traded the metrics (`closure_note`
says so). Treat association as evidence only together with the exponents and the directions.

## Tension directions

`tension_directions` are the principal directions of the near-frontier chart coordinates,
`tension_loadings` the same as loadings on the log-metrics, and `explained_spread` the share of
variance along each. They equal `orient_by_pca` on the same rows. This is how the method chains with
PCA: the spread along the surface is the set of trade-offs the designs exercised.

## With several terms

At K > 1 the function returns a list of K reports, one per facet, each on the rows assigned to that
facet. A facet with fewer than `min_near_frontier` (default 10) near-frontier rows raises
`ValueError`; widen `band` or lower `min_near_frontier`.

## What it cannot say

Each report describes one facet and so one tension, depends on the band, and is a statement about
the sampled table: tensions the sampling never exercised cannot appear. Whether a contending set is
a recognizable dilemma is for the engineer to decide.
