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
