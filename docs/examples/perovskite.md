# Perovskite solar cells

## The dataset

<!-- register: examples/perovskite/results.json counts; manifest.toml -->

The Perovskite Database Project extracts device data from peer-reviewed perovskite papers [@jacobsson2021open]. Version 1.0.1 (doi:10.5281/zenodo.5837035, licence CC BY 4.0, credited to that paper) holds 42,443 devices in 410 columns. The fetch downloads the 3.3 MB archive, stops if its size or hash differs from `manifest.toml`, then fits and writes `results.json`; it takes a few minutes.

```bash
uv run python examples/perovskite/run.py
```

The attributes are three columns of the default scan: open-circuit voltage Voc, short-circuit current density Jsc and fill factor FF. Power conversion efficiency (PCE) is their product over the input power, so it is derived and set aside. Rows with a missing, zero or negative attribute, or FF above 1, are dropped, leaving 40,045.

## The conditioning rule

<!-- register: examples/perovskite/variants.json ladder.primary.rule -->

Voc, Jsc and FF are already larger-is-better, so every orientation is +1 and nothing is inverted or shifted. Each metric is the log of its attribute divided by its spread (the standard scaler), so one fit temperature means the same for the three. Without a scaler, FF, whose log varies least, takes 0.99 and the Voc-Jsc association turns positive (+0.29). The dataset has no time or cost attribute.

## The fit

<!-- register: examples/perovskite/results.json runs.primary: tau_selected, k2 -->

The fit temperature is 18.8, chosen so that a tenth of the rows lie above the fitted surface. At K = 2 the same temperature gives term shares of 0.976 and 0.024 and a mean slack of 0.560 against 0.594 at K = 1. One term carries the dataset; the small term holds 2.4 percent of the rows and puts Jsc's exponent at 0.

## The named trade-off

The detailed-balance limit calculates efficiency with the band gap as a parameter [@shockley1961detailed]. Voc against Jsc is the pair expected to trade.

<!-- register: examples/perovskite/variants.json ladder: primary, robust_scaler, quantile, extremes_capped -->

Voc, Jsc and FF are all in the contending set, so the n-lemma is 3. Across the standard scaler, the robust scaler, the quantile map and the cap on five rows, each exponent moves: Voc from 0.12 to 0.43, Jsc from 0.27 to 0.75, FF from 0.02 to 0.61. The page gives each exponent as a range; the set and the signs are the reading: the near-frontier association of Voc with Jsc is negative in all four, from -0.13 to -0.82, so the pair the physics names is traded. Jsc with FF is negative in all four (-0.27 to -0.64), and Voc with FF is negative in three (-0.39 to -0.44) and +0.23 under the cap. In the standard-scaler fit the strongest pair is Jsc with FF (-0.63), not Voc with Jsc (-0.14). The set was the whole set in all four, so its membership says little and the signs carry the reading.

## The extremes rule

An exact maximum is set by the largest rows. Five rows have Voc above 2 V or Jsc above 40 mA/cm2, probably module or unit entries. Capping them moves the Voc-Jsc association from -0.14 to -0.82. List the largest values of every attribute, cap or remove entries that cannot be real, refit, and state the cap.

## Derived metrics

Added as a fourth metric, PCE takes exponent 0.50 and FF falls to 0.00: a derived metric absorbs the attributes it summarizes.

## The check on your own dataset

Refit with one conditioning choice changed and compare the contending set, the signs of the near-frontier association and the exponents. If the set or a sign moves, the choice decided the result and the analysis states it.

```python
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    trade_off_report,
)

fit = HyperbolicTradeSpace(temperature=tau).fit(M)
report = trade_off_report(fit, M)
report.contending_set, report.association, fit.exponents_
```

## Shares of the three metrics

<!-- register: examples/perovskite/results.json runs.primary: exponents_k1, contending_set -->

```python {.runnable}
import sys

sys.path.insert(0, ".")
from examples.perovskite import run
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    select_temperature,
)
from hyperbolic_trade_space.plotting import plot_ternary

M = run.condition(run.feasible(run.load()))
tau = select_temperature(M, 0.10, bounds=(3, 1e4))
fit = HyperbolicTradeSpace(temperature=tau, random_state=0).fit(M)
plot_ternary(fit, M, names=run.NAMES, lines=True)
```

<figure markdown>
![Triangle with Voc at the top, Jsc at the lower left and FF at the lower right. Forty thousand devices are grey points, most of them in the lower middle, with the near-frontier devices larger. One tinted region fills the triangle, labelled all three trade, and a star marks the fit's exponent vector inside the cloud, below the middle.](../generated/figures/perovskite-ternary-light.png#only-light)
![Triangle with Voc at the top, Jsc at the lower left and FF at the lower right. Forty thousand devices are grey points, most of them in the lower middle, with the near-frontier devices larger. One tinted region fills the triangle, labelled all three trade, and a star marks the fit's exponent vector inside the cloud, below the middle.](../generated/figures/perovskite-ternary-dark.png#only-dark)
<figcaption>Figure 8. The 40,045 devices as shares of Voc, Jsc and FF. One region covers the triangle, where all three trade; the star is the one-term fit's exponent vector, and the contours are equal V at a fixed total.</figcaption>
</figure>

## What the example cannot show

The frontier is the field's published best, not a physical limit: publication favours efficient devices, and a few thousand papers supply the rows. No decision-maker is posed on the dataset, so it has no objectives, and the default scan is whichever scan the authors called default.
