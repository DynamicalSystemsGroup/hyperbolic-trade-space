# Getting started

## Install

The package is installed from source for now. It needs Python 3.12 and uses
[uv](https://docs.astral.sh/uv/) for a reproducible environment:

```bash
git clone \
  https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space
cd hyperbolic-trade-space
uv sync
```

Run everything with `uv run`, for example `uv run python first_fit.py`.

## A first fit

The table below is synthetic: 300 designs scored on 3 metrics, all positive and larger-is-better,
with a planted frontier.

```python {.runnable}
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    make_frontier_data,
    tension_report,
)

X, info = make_frontier_data(300, 3, random_state=0)
ts = HyperbolicTradeSpace(temperature=20.0).fit(X)
report = tension_report(ts, X)
print(report.lemma_name, report.contending_set)
print(report.exponents.round(2))
```

The output is `trilemma [0 1 2]` and then `[0.3  0.37 0.33]`. `temperature`, the one parameter
set, is tau, how hard the maximum is; the band of near-frontier designs has width 1/tau
([choosing the temperature](user-guide/fitting.md#choosing-the-temperature)).

The idea is easiest to see with two of the metrics, where the model is a line. In the log plane of
metrics 0 and 1 the designs lie on or just beyond a straight frontier, and the grey strip under the line
is the region up to 0.5 below the frontier in log V:

```python {.runnable}
from hyperbolic_trade_space.plotting import plot_log_plane

X2 = X[:, :2]
ts2 = HyperbolicTradeSpace(temperature=20.0).fit(X2)
plot_log_plane(ts2, X2, band=0.5)
```

<figure markdown>
![Designs in the log plane of two metrics: the frontier is a straight line, and the designs scatter below it, a few just beyond it, and the nearest ones lie in a grey band under the line.](generated/figures/first-fit-light.png#only-light)
![Designs in the log plane of two metrics: the frontier is a straight line, and the designs scatter below it, a few just beyond it, and the nearest ones lie in a grey band under the line.](generated/figures/first-fit-dark.png#only-dark)
<figcaption>Figure 1. The first fit seen on two metrics: the line is the fitted frontier, the designs fall below it or just beyond it, and the grey band holds those nearest to it.</figcaption>
</figure>

## Reading the output

`fit` learned one exponent per metric, summing to one. `report.contending_set` lists the metrics that
contend at the edge of the table: here all three, an n-lemma with n = 3, which the report names a
trilemma. The set is found from the data and not chosen in advance. `report.exponents` are the
fitted weights at the fit temperature; their ratios are the elasticities between the contending
metrics, with a minus sign (`report.elasticities`).

The fitted object has more to give. `ts.score_samples(X)` is, for each design, the log of V, the
invariant value: a weighted geometric mean of the metrics, 1 on the fitted reference surface, so
negative inside and positive beyond. `ts.transform(X)` is the chart, `d - 1` position coordinates plus that log V, and `ts.inverse_transform` undoes it.

## Your own data

Real attributes are rarely positive, larger-is-better and comparably scaled. Turning them into
metrics is the first step of the [user guide](user-guide/conditioning.md), with
`LogAffinePreconditioner`. From there the guide follows the order of a study: [fit](user-guide/fitting.md),
[read the tensions](user-guide/tensions.md), [use the chart](user-guide/chart.md).
