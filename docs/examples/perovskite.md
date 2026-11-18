# Perovskite solar cells

## Where the devices come from

<!-- register: examples/perovskite/results.json counts; manifest.toml -->

The Perovskite Database Project extracted the metal-halide perovskite solar cells reported in peer-reviewed papers into one open table [@jacobsson2021open]. Version 1.0.1 (doi:10.5281/zenodo.5837035, licence CC BY 4.0, credited to that paper) holds 42,443 devices in 410 columns. A row is one reported device. The fetch downloads the 3.3 MB archive, stops if its size or hash differs from `manifest.toml`, then fits and writes `results.json`.

```bash
uv run python examples/perovskite/run.py
```

## The attributes

```text
attribute  meaning                       unit     column          orient
Voc        open-circuit voltage          V        JV_default_Voc  +1
Jsc        short-circuit current density mA/cm2   JV_default_Jsc  +1
FF         fill factor: delivered power  fraction JV_default_FF   +1
           over Voc times Jsc
set aside: PCE, power conversion efficiency (JV_default_PCE), the
           product of the three over the input power
```

All three come from the current-voltage scan the authors called default. Rows with a missing, zero or negative attribute, or FF above 1, are dropped, leaving 40,045.

## What the fit is asked

In the detailed-balance limit the band gap sets both the voltage a cell can reach and the current it can collect [@shockley1961detailed]. Among the best reported devices, does Voc trade against Jsc, with a negative association near the frontier, or does the fill factor carry the trade?

## The fit

<!-- register: examples/perovskite/variants.json ladder.primary.rule -->

All three are larger-is-better, so nothing is inverted or shifted. Each metric is the log of its attribute divided by its spread (the standard scaler), so one [fit temperature](../generated/glossary.md) means the same for the three. Without a scaler, FF, whose log varies least, takes 0.99 and the Voc-Jsc association turns positive (+0.29).

<!-- register: examples/perovskite/results.json runs.primary: tau_selected, k2 -->

The fit temperature is 18.8, chosen so that a tenth of the rows lie above the fitted surface. At K = 2 the same temperature gives term shares of 0.976 and 0.024 and a mean slack of 0.560 against 0.594 at K = 1. The small term holds 2.4 percent of the rows and puts Jsc's exponent at 0.

<!-- register: examples/perovskite/results.json runs.primary: exponents_k1, contending_set -->

```python {.runnable}
import sys

sys.path.insert(0, ".")
from examples.perovskite import run
from tradespace import (
    HyperbolicTradeSpace,
    select_temperature,
)
from tradespace.plotting import plot_ternary

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

<!-- register: examples/perovskite/variants.json ladder: primary, robust_scaler, quantile, extremes_capped -->

Voc, Jsc and FF are all in the [contending set](../generated/glossary.md), so the n-lemma is 3. Across the standard scaler, the robust scaler, the quantile map and the cap on five rows, each exponent moves: Voc from 0.12 to 0.43, Jsc from 0.27 to 0.75, FF from 0.02 to 0.61. The near-frontier association of Voc with Jsc is negative in all four, from -0.13 to -0.82. Jsc with FF is negative in all four (-0.27 to -0.64), and Voc with FF is negative in three (-0.39 to -0.44) and +0.23 under the cap. In the standard-scaler fit the strongest pair is Jsc with FF (-0.63), not Voc with Jsc (-0.14).

**The extremes.** An exact maximum is set by the largest rows. Five rows have Voc above 2 V or Jsc above 40 mA/cm2, probably module or unit entries. Capping them moves the Voc-Jsc association from -0.14 to -0.82. Cap or remove entries that cannot be real, refit, and state the cap.

**A derived metric.** Added as a fourth metric, power conversion efficiency (PCE) takes exponent 0.50 and FF falls to 0.00: a derived metric absorbs the attributes it summarizes.

**The check on your own dataset.** Refit with one conditioning choice changed. If the contending set or a sign of the near-frontier association moves, the choice decided the result, and the analysis states it.

```python
from tradespace import (
    HyperbolicTradeSpace,
    trade_off_report,
)

fit = HyperbolicTradeSpace(temperature=tau).fit(M)
report = trade_off_report(fit, M)
report.contending_set, report.association, fit.exponents_
```

## What the fit says

Near the frontier of reported devices, voltage is gained at the cost of current under every conditioning choice: the pair the detailed-balance limit names is traded. It is not the only trade, nor the strongest in the standard-scaler fit, and its size depends on five suspect rows. All three metrics contend in each of the four conditioning fits, so the signs carry the reading, not the set or one exponent.

## What the example cannot show

The frontier is the field's published best, not a physical limit: publication favours efficient devices, and a few thousand papers supply the rows. The band gap is not a metric, so the fit cannot say the gap moves a device along the trade. No decision-maker is posed on the dataset, so it has no objectives, and the default scan is whichever scan the authors called default.
