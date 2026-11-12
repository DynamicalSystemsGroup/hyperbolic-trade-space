# Examples

## A cubesat trade study across power, mass and attitude control

For the reader who wants a worked case: a synthetic satellite demonstrator, [a cubesat model](paper:sect-case-construction) coupling power, mass and attitude control. Thirteen metrics are compared under two controller-gain settings. Here a simulation measures the attributes; a fielded system's measured attributes would enter
the same table and fit.

The primary regime's table has 2,134 feasible designs of 3,000. With the fit temperature chosen by `select_temperature` for a tenth of designs
above V = 1:

- **One term.** The tension report finds a contending set (metrics that trade off) of seven metrics (unit cost, available power,
  pointing error, fleet cost, momentum headroom, settling time, depth of discharge): a 7-lemma.
- **Two terms.** The case is read at K = 2, the K the [choosing-K checks](user-guide/choosing-k.md) pick. At the
  one-term temperature (`case.mean_slack_fixed_tau`) the mean slack falls from 0.122 to 0.043. At the
  two-term fit's own temperature, status `certified`, the terms have contending sets of 8 and 7 metrics and
  shares of 74 and 26 percent of the near-frontier designs: the larger adds peak slew power to the
  one-term contending set, and the smaller is that set.
- **A second table.** The stock-gains table gives a different one-term
  contending set.

## The one-term fit, drawn

This block draws the one-term fit's tension report from the committed table:

```python {.runnable}
import sys

sys.path.insert(0, "examples/adcs")
import case

study = case.load_study("primary")
fit = case.fit_study(study, K=1)
case.tension_figure(study, fit)
```

<figure markdown>
![Heatmap of the association among thirteen conditioned metrics near the frontier; seven metrics are outlined as the contending set.](generated/figures/adcs-tensions-light.png#only-light)
![Heatmap of the association among thirteen conditioned metrics near the frontier; seven metrics are outlined as the contending set.](generated/figures/adcs-tensions-dark.png#only-dark)
<figcaption>Figure 5. The tension report of the one-term fit: cells, the correlation of the log-metrics near the frontier; outlined, the contending set; grey, below the participation threshold.</figcaption>
</figure>

## Choosing K on the case

The [choosing-K checks](user-guide/choosing-k.md) on both regimes, each at its K = 1 temperature ([recipe](user-guide/choosing-k.md#the-temperature)).

```python {.runnable}
import numpy as np
from hyperbolic_trade_space import HyperbolicTradeSpace


def fit_k(M, K, tau, seed=0):
    return HyperbolicTradeSpace(
        n_terms=K, temperature=tau, random_state=seed
    ).fit(M)


def sweep(M, tau, Ks):
    """One line per K at one temperature; returns the mean slacks."""
    slack = []
    for K in Ks:
        fit = fit_k(M, K, tau)
        t = fit.termination_
        print(
            f"K={K} slack={fit.mean_slack_:.3f}"
            f" thinnest={fit.term_share_.min():.2f}"
            f" {t.status} radius={t.radius:.0e}"
        )
        slack.append(fit.mean_slack_)
    print("drops", -np.diff(slack).round(3))
    return np.array(slack)


def movement(M, K, tau, draws=2, seed=0):
    """Largest distance to the nearest term of a refit on a resample."""
    ref = fit_k(M, K, tau)
    rng = np.random.default_rng(seed)
    moved = np.zeros(K)
    for s in range(draws):
        W = fit_k(M[rng.choice(len(M), len(M))], K, tau, s).exponents_
        d = np.abs(W[:, None] - ref.exponents_).sum(axis=2)
        moved = np.maximum(moved, d.min(axis=0))
    return moved.max()


studies = {r: case.load_study(r) for r in ("primary", "stock")}
taus = {r: case.fit_study(s, K=1).tau for r, s in studies.items()}
for r, s in studies.items():
    print(r)
    sweep(s.M, taus[r], range(1, 6))
```

The primary regime drops by 0.078, then 0.023, 0.012 and 0.005: a break at K = 2, where the
thinnest term holds 0.28 (0.21 at K = 3). The stock regime drops by 0.055, 0.031, 0.012 and 0.010,
bending with no break, so the mean slack cannot choose K; its thinnest term holds 0.35 at K = 2 and
0.13 at K = 3.

```python {.runnable}
for K in (2, 3, 4):
    M, tau = studies["primary"].M, taus["primary"]
    print(
        K, np.round([movement(M, K, tau, seed=s) for s in range(3)], 2)
    )
```

Over three draws the primary regime's movement is 0.18 to 0.20 at K = 2, 0.15 to 0.29 at K = 3 and
0.14 to 0.95 at K = 4. The ranges overlap, so this check excludes none.

## Requirements read after the fit

The fit ignores the model's six requirements. Read after it, each has a pass share,
the near-frontier designs it excludes and a price at the one-term frontier, in band widths and, for the costs and the mass, USD:

```text
# case.requirements_summary()
requirement      pass             near excluded       price, bands
(primary | stock)
peak slew power  58.8 | 64.1 %    108/238 | 145/293   0 | 0
pointing error   95.2 | 65.6 %    8/238 | 118/293     0.08 | 0.79
control effort   57.4 | 88.5 %    95/238 | 32/293     0 | 0.91
total mass       94.6 | 95.2 %    12/238 | 9/293      0.24 | 1.55
unit cost        76.2 | 75.8 %    64/238 | 66/293     5.31 | 1.22
fleet cost       71.4 | 71.0 %    57/238 | 85/293     1.50 | 0.49
all jointly      25.7 | 22.2 %    178/238 | 241/293
excess over the limit, median excluded design (USD)
total mass       1,880 | 1,730 USD of launch per satellite
unit cost        35,200 | 27,300 USD per satellite
fleet cost       1,130,000 | 1,140,000 USD per fleet
```

Refitted on three design sets, the one-term contending set barely moves. The third keeps the designs that meet the four performance thresholds; the two cost limits are read after the fit:

```text
# case.design_sets_summary()
primary, all designs (3000): unit cost, available power, pointing error,
  fleet cost, momentum headroom, settling time, depth of discharge
primary, feasible (2134): unit cost, available power, pointing error,
  fleet cost, momentum headroom, settling time, depth of discharge
primary, thresholds met (814): momentum headroom, settling time,
  available power, unit cost, pointing error, fleet cost, depth of
  discharge
stock, all designs (3000): available power, momentum headroom, total
  mass, unit cost, pointing error, settling time, fleet cost, depth of
  discharge
stock, feasible (2355): momentum headroom, available power, total mass,
  settling time, pointing error, depth of discharge, unit cost, fleet
  cost
stock, thresholds met (882): momentum headroom, settling time, available
  power, unit cost, total mass, pointing error
```

## Three metrics as shares of a total

A ternary plot places a design by its shares of a total among three metrics. This block draws two triples of
the primary regime, two terms each, with one key:

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

The triples show how to read the figure; they are not findings. What the case leaves out is listed on [the case page](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/blob/main/examples/adcs/case-model.md#what-the-case-leaves-out).

## Run it

[`examples/adcs/`](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/tree/main/examples/adcs/)
holds the design space, the evaluation model, the seeded datasets, the figures and
`k_terms.py`, which fits one, two and three terms to each regime:

```bash
uv run python examples/adcs/k_terms.py
```
