# Examples

## A cubesat trade study across power, mass and attitude control

The worked case is a cubesat model coupling power, mass and attitude control. Eight attributes are
compared under two controller-gain settings: settling time, pointing error, control effort, power margin, energy balance, peak slew power, depth of discharge and total
mass. `LogAffinePreconditioner` conditions the feasible designs for `HyperbolicTradeSpace`. In this
design loop a simulation measures the attributes; a fielded system's measured attributes would enter
the same table and fit.

The primary regime's table (aggressive controller gains) has 706 feasible designs. With the fit temperature chosen by `select_temperature` for a tenth of designs
above V = 1:

- **One term.** The tension report finds a contending set (metrics that trade off) of five metrics (total mass, energy balance,
  pointing error, depth of discharge, settling time): a 5-lemma, found from the data, not chosen beforehand.
- **Three terms.** At the one-term temperature (`case.mean_slack_fixed_tau`) the mean slack falls
  from 0.243 to 0.132 at two terms and 0.088 at three, status `certified`. The three terms have
  contending sets of 5, 4 and 5 metrics and term shares of 17, 10 and 73 percent of the near-frontier
  designs: the largest alone contains peak slew power, the smallest alone contains control effort,
  and the other is the one-term contending set.
- **A second table.** The stock-gains table gives a different one-term
  contending set, so the finding depends on the regime.
- **No metric twice.** No pair of the eight metrics reaches a rank correlation of 0.99 over the
  feasible designs, so each exponent is read on its own.

These are observations of the fit, not explanations; the physical reading is the engineer's work.

## The one-term fit, drawn

`examples/adcs/case.py` runs the study from the committed table; these blocks draw the one-term
fit's tension report and first two chart coordinates:

```python {.runnable}
import sys

sys.path.insert(0, "examples/adcs")
import case

study = case.load_study("primary")
fit = case.fit_study(study, K=1)
case.tension_figure(study, fit)
```

<figure markdown>
![Heatmap of the association among eight conditioned metrics near the frontier; five metrics are outlined as the contending set.](generated/figures/adcs-tensions-light.png#only-light)
![Heatmap of the association among eight conditioned metrics near the frontier; five metrics are outlined as the contending set.](generated/figures/adcs-tensions-dark.png#only-dark)
<figcaption>Figure 6. The tension report of the one-term fit: cells, the correlation of the log-metrics near the frontier; outlined, the contending set; grey, metrics that do not participate.</figcaption>
</figure>

```python {.runnable}
from hyperbolic_trade_space.plotting import plot_frontier_coordinates

chart = fit.estimator.transform(study.M)
plot_frontier_coordinates(chart[:, :-1], chart[:, -1])
```

<figure markdown>
![The 706 feasible designs in the plane of the first two position coordinates Z0 and Z1, with the designs nearest the frontier ringed in black.](generated/figures/adcs-coordinates-light.png#only-light)
![The 706 feasible designs in the plane of the first two position coordinates Z0 and Z1, with the designs nearest the frontier ringed in black.](generated/figures/adcs-coordinates-dark.png#only-dark)
<figcaption>Figure 7. The 706 feasible designs by Z0 and Z1, the first two of seven position coordinates, meaningless alone; 193 ringed designs lie nearest the frontier. It shows coverage, not the frontier.</figcaption>
</figure>

## Requirements read after the fit

The fit ignores the model's four threshold requirements. Read after it, each has a pass share,
the near-frontier designs it excludes and a price at the one-term frontier, in band widths:

```text
# case.requirements_summary()
requirement      pass             near excluded   price, bands
(primary | stock)
peak slew power  62.2 | 67.3 %    0/56 | 2/77     0 | 0
pointing error   95.0 | 63.7 %    1/56 | 42/77    0.07 | 0.56
control effort   58.9 | 90.0 %    18/56 | 1/77    0 | 7.92
total mass       94.9 | 95.6 %    0/56 | 1/77     0 | 0
all jointly      40.8 | 38.7 %    19/56 | 43/77
```

Refitted on three design sets in one conditioning, the one-term contending set barely moves:

```text
# case.design_sets_summary()
primary, all designs (1000): total mass, energy balance, pointing error,
  depth of discharge, settling time
primary, feasible (706): total mass, energy balance, pointing error,
  depth of discharge, settling time
primary, requirements met (288): total mass, energy balance, pointing
  error, depth of discharge, settling time
stock, all designs (1000): control effort, settling time, power margin,
  pointing error, total mass
stock, feasible (780): control effort, settling time, power margin,
  pointing error, depth of discharge
stock, requirements met (302): control effort, settling time, energy
  balance, pointing error, depth of discharge
```

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
![A triangle whose corners are three metrics, tinted in three regions by the term that is largest there, with designs as points, a numbered marker for each term's exponent vector, and lines of equal V closing around each marker.](generated/figures/ternary-planted-light.png#only-light)
![A triangle whose corners are three metrics, tinted in three regions by the term that is largest there, with designs as points, a numbered marker for each term's exponent vector, and lines of equal V closing around each marker.](generated/figures/ternary-planted-dark.png#only-dark)
<figcaption>Figure 8. Designs by shares of three metrics: regions, numbered exponent vectors, lines of equal V.</figcaption>
</figure>

Reading it:

- A corner is the whole total in one metric; an edge splits it between two.
- A numbered marker is a term's exponent vector, where that term's V is largest for a fixed total.
  V, the invariant value, also depends on the total, so a marker is not where V = 1.
- A region is where one term is the largest, named by the metrics that trade there: an analysis of the
  fit, not a label on a design.

```python {.runnable}
from hyperbolic_trade_space.plotting import ternary_marker_values

values = ternary_marker_values(ts, X)
print(values.round(2).to_string(index=False))
print("lines at", values.attrs["levels"])
```

Each row is a marker, its shares of the total, and V there as a fraction of the highest marker's V.

Limits: three parts only; the choice of metrics can flatter the result; it is for reading, not measuring distance; eight metrics do not separate in three, so none is drawn for the cubesat.

## Run it

[`examples/adcs/`](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/tree/main/examples/adcs/)
holds the design space, the evaluation model, the seeded datasets, the figures and
`k_terms.py`, which fits one, two and three terms to each regime:

```bash
uv run python examples/adcs/k_terms.py
```

Per regime it prints a per-K summary at a temperature re-selected per K (columns `tau`, `band 1/tau`,
`objective_`, equal here to `mean_slack_`, `frac_above_`, `term rows`, `term shares`, `max gap`,
`status`, `gamma`, `radius`, `bound`), the per-term record (contending set, largest exponents,
near-frontier designs, reach, share, gap), the same two at the one-term temperature (the comparison
above) and a seed check at three terms. A fit's record is `fit.estimator.termination_`, read on the
[termination page](user-guide/termination.md).
