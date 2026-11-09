# Examples

## A cubesat trade study across power, mass and attitude control

The worked case is a cubesat model coupling power, mass and attitude control: bus, antenna, inertial unit,
controller, wheel and tracker alternatives, solar panel and battery. Ten attributes are compared under two controller-gain settings: settling time, slew time, pointing error,
control effort, power margin, energy balance, eclipse reserve, peak slew power, depth of discharge and total
mass. `LogAffinePreconditioner` conditions the feasible designs for `HyperbolicTradeSpace`.
In this design loop the simulation measures the attributes (committed here as tables), and a fielded system's measured attributes would enter the same table and the same fit.

The aggressive-gains table has 706 feasible designs. With the fit temperature chosen by `select_temperature` for a tenth of the
designs above V = 1:

- **One term.** The tension report finds a contending set (metrics that trade off) of six metrics (total mass, slew time,
  energy balance, control effort, pointing error, depth of discharge): a 6-lemma, found from the data with no prior choice of which
  metrics or how many.
- **Three terms.** The mean slack falls from 0.204 at one term to 0.117 at three, and the status is
  `certified`. The three facets have contending sets of 6, 6 and 7 metrics. The largest facet holds
  78 percent of the near-frontier share and is the only one containing total mass and peak slew
  power; the other two are built on control effort, slew time and energy balance.
- **A second table.** The stock-gains table gives a different one-term contending set, so the
  finding depends on the regime evaluated.

These are observations of the fit, not explanations. Reading them in physical terms is the
engineer's work.

## The one-term fit, drawn

The case module in `examples/adcs/case.py` runs the study from the committed table. These blocks
draw the tension report and the first two chart coordinates of the one-term fit:

```python {.runnable}
import sys

sys.path.insert(0, "examples/adcs")
import case

study = case.load_study("primary")
fit = case.fit_study(study, K=1)
case.tension_figure(study, fit)
```

<figure markdown>
![Heatmap of the association among ten conditioned metrics near the frontier; six metrics are outlined as the contending set.](generated/figures/adcs-tensions-light.png#only-light)
![Heatmap of the association among ten conditioned metrics near the frontier; six metrics are outlined as the contending set.](generated/figures/adcs-tensions-dark.png#only-dark)
<figcaption>Figure 6. The tension report of the one-term fit to the aggressive-gains table. The six outlined metrics are the contending set; grey labels mark metrics that do not participate.</figcaption>
</figure>

```python {.runnable}
from hyperbolic_trade_space.plotting import plot_frontier_coordinates

chart = fit.estimator.transform(study.M)
plot_frontier_coordinates(chart[:, :-1], chart[:, -1])
```

<figure markdown>
![The 706 feasible designs in the plane of the first two position coordinates Z0 and Z1, with the designs nearest the frontier ringed in black.](generated/figures/adcs-coordinates-light.png#only-light)
![The 706 feasible designs in the plane of the first two position coordinates Z0 and Z1, with the designs nearest the frontier ringed in black.](generated/figures/adcs-coordinates-dark.png#only-dark)
<figcaption>Figure 7. The 706 feasible designs by their first two position coordinates; the ringed designs lie nearest the frontier.</figcaption>
</figure>

## Three metrics as shares of a total

A ternary plot places a design by its shares of a total among three metrics. This block fits a
synthetic table (`make_frontier_data`) and draws it with lines of equal V:

```python {.runnable}
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    make_frontier_data,
)
from hyperbolic_trade_space.plotting import plot_ternary

X, _ = make_frontier_data(900, 3, n_terms=3, random_state=11)
ts = HyperbolicTradeSpace(
    n_terms=3, temperature=50.0, random_state=0
).fit(X)
plot_ternary(ts, X, lines=True)
```

<figure markdown>
![A triangle whose corners are three metrics, tinted in three regions by the facet that dominates, with designs as points, a numbered marker for each facet's exponent vector, and lines of equal V closing around each marker.](generated/figures/ternary-planted-light.png#only-light)
![A triangle whose corners are three metrics, tinted in three regions by the facet that dominates, with designs as points, a numbered marker for each facet's exponent vector, and lines of equal V closing around each marker.](generated/figures/ternary-planted-dark.png#only-dark)
<figcaption>Figure 8. Designs by shares of three metrics: regions, numbered exponent vectors, lines of equal V.</figcaption>
</figure>

How to read this plot:

- A corner is the whole total in one metric; an edge splits it between two.
- A numbered marker is a facet's exponent vector, where that facet's V is largest for a fixed total.
  V, the invariant value, also depends on the total, so a marker is not where V = 1.
- A region is where one facet dominates, named by the metrics that trade there: an analysis of the
  fit, not a label on a design.
- A design mostly in metric 3 with a little metric 1 is in the blue region, where metric 3 trades
  against metric 1.

```python {.runnable}
from hyperbolic_trade_space.plotting import ternary_marker_values

values = ternary_marker_values(ts, X)
print(values.round(2).to_string(index=False))
print("lines at", values.attrs["levels"])
```

Key: a row is a marker, its shares of the total, and V there as a fraction of the highest marker's V.

Limits: three parts only; the analyst's choice of metrics can flatter the result; the triangle is for reading, not measuring distance; a ten-metric case does not separate in three, so none is drawn for the cubesat.

## Run it

The code, data and figures are in the repository under
[`examples/adcs/`](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/tree/main/examples/adcs/):
the design space and evaluation model, the committed seeded datasets, the figures, and
`k_terms.py`, which reproduces the one-, two- and three-term fits:

```bash
uv run python examples/adcs/k_terms.py
```

The same steps apply to any table of designs: condition, `select_temperature`, fit, then read the
[tension report](user-guide/tensions.md) and the [termination record](user-guide/termination.md).
