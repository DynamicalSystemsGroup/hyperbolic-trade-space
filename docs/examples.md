# Examples

## A spacecraft attitude-control trade study

The worked case is a small-satellite attitude determination and control (ADCS) study. A system model
and simulator evaluate each design into ten attributes:
settling time, slew time, pointing error, total mass, control effort, power margin, energy balance,
eclipse reserve, peak slew power and depth of discharge. Mixed orientations and units go through
`LogAffinePreconditioner`, infeasible designs are removed first, and the conditioned metrics go to
`HyperbolicTradeSpace`. Nothing is simulated by the package; the evaluated tables are committed.

The aggressive-gains table has 706 feasible designs. With the temperature selected for a tenth of the
designs above V = 1:

- **One term.** The tension report finds a contending set of six metrics (total mass, slew time,
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
draw the tension report and the chart of the one-term fit:

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
case.coordinates_figure(study, fit)
```

<figure markdown>
![Two scatter plots of the feasible designs in pairs of chart coordinates, coloured by reaction-wheel class, with the designs nearest the frontier ringed in black.](generated/figures/adcs-coordinates-light.png#only-light)
![Two scatter plots of the feasible designs in pairs of chart coordinates, coloured by reaction-wheel class, with the designs nearest the frontier ringed in black.](generated/figures/adcs-coordinates-dark.png#only-dark)
<figcaption>Figure 7. The 706 feasible designs by position along the frontier, coloured by wheel class; the ringed designs lie nearest the frontier.</figcaption>
</figure>

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
