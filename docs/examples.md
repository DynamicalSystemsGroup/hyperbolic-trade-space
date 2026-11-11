# Examples

## A cubesat trade study across power, mass and attitude control

[The worked case](paper:sect-case-construction) is a cubesat model coupling power, mass and attitude control. Eight attributes are
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

## The one-term fit, drawn

`examples/adcs/case.py` runs the study from the committed table; this block draws the one-term
fit's tension report:

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
<figcaption>Figure 5. The tension report of the one-term fit: cells, the correlation of the log-metrics near the frontier; outlined, the contending set; grey, metrics that do not participate.</figcaption>
</figure>

## Requirements read after the fit

The fit ignores the model's four threshold requirements. Read after it, each has a pass share,
the near-frontier designs it excludes and a price at the one-term frontier, in band widths:

```text
# case.requirements_summary()
requirement      pass             near excluded       price, bands
(primary | stock)
peak slew power  58.8 | 64.1 %    108/238 | 145/293   0 | 0
pointing error   95.2 | 65.6 %    8/238 | 118/293     0.08 | 0.79
control effort   57.4 | 88.5 %    95/238 | 32/293     0 | 0.91
total mass       94.6 | 95.2 %    12/238 | 9/293      0.24 | 1.55
all jointly      38.1 | 37.5 %    148/238 | 210/293
```

Refitted on three design sets in one conditioning, the one-term contending set barely moves:

```text
# case.design_sets_summary()
primary, all designs (3000): unit cost, available power, pointing error,
  fleet cost, momentum headroom, settling time, depth of discharge
primary, feasible (2134): unit cost, available power, pointing error,
  fleet cost, momentum headroom, settling time, depth of discharge
primary, requirements met (814): momentum headroom, settling time,
  available power, unit cost, pointing error, fleet cost, depth of
  discharge
stock, all designs (3000): available power, momentum headroom, total
  mass, unit cost, pointing error, settling time, fleet cost, depth of
  discharge
stock, feasible (2355): momentum headroom, available power, total mass,
  settling time, pointing error, depth of discharge, unit cost, fleet
  cost
stock, requirements met (882): momentum headroom, settling time,
  available power, unit cost, total mass, pointing error
```

## Three metrics as shares of a total

A ternary plot places a design by its shares of a total among three metrics. This block fits two triples of
the primary regime, two terms each, and draws both with one key:

```python {.runnable}
import sys

sys.path.insert(0, "examples/adcs")
import case

fits = case.ternary_pair_fits()
case.ternary_pair_figure(fits)
```

<figure markdown>
<a href="../generated/figures/ternary-cubesat-light.png" markdown="span">![Two triangles side by side, each with three metrics at its corners, tinted in two regions, with designs as points, a numbered marker for each term's exponent vector, lines of equal V and a dashed line where the leading term changes; one key below both. A: pointing error, total mass, control effort. B: settling time, control effort, depth of discharge.](generated/figures/ternary-cubesat-light.png#only-light)</a>
<a href="../generated/figures/ternary-cubesat-dark.png" markdown="span">![Two triangles side by side, each with three metrics at its corners, tinted in two regions, with designs as points, a numbered marker for each term's exponent vector, lines of equal V and a dashed line where the leading term changes; one key below both. A: pointing error, total mass, control effort. B: settling time, control effort, depth of discharge.](generated/figures/ternary-cubesat-dark.png#only-dark)</a>
<figcaption>Figure 6. A: one region trades pointing error against control effort, the other total mass against pointing error. B: one region trades settling time against control effort; the other region is depth of discharge alone. Shows: where each term leads and where its V peaks. Does not show: groups of designs, the values of V on the lines, a cause.</figcaption>
</figure>

Reading it:

- A corner is the whole total in one metric; an edge splits it between two.
- A numbered marker is a term's exponent vector, where that term's V is largest for a fixed total.
  V, the invariant value, also depends on the total, so a marker is not where V = 1.
- A region is where one term is the largest: an analysis of the fit, not a label on a
  design.

```python {.runnable}
from hyperbolic_trade_space.plotting import ternary_marker_values

for name, (study, est) in fits.items():
    print(name, study.names)
    print(
        ternary_marker_values(est, study.M, study.names)
        .round(2)
        .to_string(index=False)
    )
```

Each row is a marker: its shares and V there, relative to the highest marker's.

The triples came from a search of all 56 triples in each regime at one, two and three
terms (336 fits, 275 made). A term counts when its cell holds at least ten near-frontier designs, its
exponents move by at most 0.10 under restarts and resamples and the fit is certified; 55 fits have two
counting terms with different contending sets.

## Run it

[`examples/adcs/`](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/tree/main/examples/adcs/)
holds the design space, the evaluation model, the seeded datasets, the figures and
`k_terms.py`, which fits one, two and three terms to each regime:

```bash
uv run python examples/adcs/k_terms.py
```

Per regime it prints a per-K summary at a temperature re-selected per K, the per-term record, the same
two at the one-term temperature (the comparison above) and a seed check at three terms. A fit's record is `fit.estimator.termination_`, read on the
[termination page](user-guide/termination.md).
