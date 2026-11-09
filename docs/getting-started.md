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

The output is `trilemma [0 1 2]` and then `[0.3  0.37 0.33]`.

The chart of the same fit draws each design by its position along the frontier:

```python {.runnable}
from hyperbolic_trade_space.plotting import plot_frontier_coordinates

chart = ts.transform(X)
plot_frontier_coordinates(chart[:, :-1], chart[:, -1])
```

<figure markdown>
![The 300 designs in the plane of the two position coordinates Z0 and Z1; the designs nearest the frontier are ringed in black.](generated/figures/first-fit-light.png#only-light)
![The 300 designs in the plane of the two position coordinates Z0 and Z1; the designs nearest the frontier are ringed in black.](generated/figures/first-fit-dark.png#only-dark)
<figcaption>Figure 1. The 300 designs of the first fit, placed by two position coordinates; the ringed designs lie nearest the frontier.</figcaption>
</figure>

## Reading the output

`fit` learned one exponent per metric, summing to one. `report.contending_set` lists the metrics that
contend at the edge of the table: here all three, an n-lemma with n = 3, which the report names a
trilemma. The set is found from the data and not chosen in advance. `report.exponents` are the
fitted weights at the working temperature; their ratios are the exchange rates between the contending
metrics (`report.exchange_rates`).

The fitted object has more to give. `ts.score_samples(X)` is the log of V for each design, the energy
differential to the fitted reference surface: negative inside, positive beyond. `ts.transform(X)`
is the chart, `d - 1` position coordinates plus that log V, and `ts.inverse_transform` undoes it.

## Your own data

Real attributes are rarely positive, larger-is-better and comparably scaled. Turning them into
metrics is the first step of the [user guide](user-guide/conditioning.md), with
`LogAffinePreconditioner`. From there the guide follows the order of a study: [fit](user-guide/fitting.md),
[read the tensions](user-guide/tensions.md), [use the chart](user-guide/chart.md).
