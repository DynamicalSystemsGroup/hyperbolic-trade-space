# Broadbalk wheat: grain against straw

## The dataset

Grain and straw yields from the Broadbalk wheat experiment, 1968 to 2022, published by the Electronic Rothamsted Archive as [doi:10.23637/rbk1-yld6822-01](https://doi.org/10.23637/rbk1-yld6822-01) (Glendining and Poulton, 2023) under CC BY 4.0. The download sits behind a form, so a reader fetches it by hand and rebuilds the derived table with `uv run python examples/wheat/derive.py examples/wheat/data/01-YLD6822.zip`. The committed derived table, `examples/wheat/derived/grain_straw.csv`, is what the code below reads: 3,753 plot-years with both yields recorded and positive, 44 percent of the archive's 8,573, in columns grain, straw, year, plot, treatment, cultivar, nitrogen, cropping and section.

## Metrics and configuration

The metrics are grain and straw. The configuration is the treatment, the cultivar and the year.

## The conditioning rule

Grain and straw are both larger is better. Each yield is taken in logs and given a standard scaler, orientation +1, shift 0 ([conditioning](../user-guide/conditioning.md)).

## The fit

The temperature is the one that puts a tenth of the rows above the frontier: 8.3, a band of 0.12 in log V. At one term grain's exponent is 0.45 and straw's 0.55, the contending set is both, and the association of the two log yields near the frontier is -0.87.

```python {.runnable}
import pandas as pd
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    select_temperature,
)
from hyperbolic_trade_space.plotting import plot_log_plane

path = "examples/wheat/derived/grain_straw.csv"
raw = pd.read_csv(path)[["grain", "straw"]].to_numpy()
pre = LogAffinePreconditioner(
    orientation=1, shift=0.0, scaler="standard"
)
M = pre.fit_transform(raw)
tau = select_temperature(M, target_frac_above=0.1, bounds=(3.0, 1e4))
fit = HyperbolicTradeSpace(temperature=tau, random_state=0).fit(M)
ax = plot_log_plane(fit, M, band=1 / tau)
ax.set_xlabel("log grain, standardized")
ax.set_ylabel("log straw, standardized")
print(round(tau, 1), fit.exponents_.round(2))
```

<figure markdown>
![Log plane of standardized grain against straw yields: a cloud of plot-years with the fitted frontier as a falling straight line above it and a grey band of near-frontier plot-years under the line.](../generated/figures/wheat-log-plane-light.png#only-light)
![Log plane of standardized grain against straw yields: a cloud of plot-years with the fitted frontier as a falling straight line above it and a grey band of near-frontier plot-years under the line.](../generated/figures/wheat-log-plane-dark.png#only-dark)
<figcaption>Figure 10. Broadbalk plot-years in the log plane of grain and straw: the line is the fitted frontier and the grey band, 0.12 wide in log V, holds the plot-years nearest to it.</figcaption>
</figure>

At two terms, at the same temperature, the terms carry shares of 0.57 and 0.43 of the near-frontier rows and the fit is certified. The mean level below the frontier falls from 0.859 to 0.748.
With two metrics the frontier is a line in log units, the simplex a segment, and the chart one position and one level. The second term has grain alone as its contending set, a limit on grain with straw free, which one term cannot show; it holds in 7 of the 15 rows of the conditioning ladder, so it is read as conditional.

## The named trade-off

The named trade-off is the harvest index, grain over grain plus straw: old and modern cultivars reach similar biomass, and the modern ones put more of it in grain ([@austin1980genetic; @austin1993old]). The negative association is that dilemma. At nitrogen of at least 96 kg per hectare the median harvest index is 0.52 for Cappelle Desprez (1968 to 1978) and 0.76 for Zyatt (2019 to 2022), at median total biomass of 8.97 and 8.75 t per hectare.

## What moves across the ladder

Grain's exponent runs from 0.29, with no scaler, to 0.72, in Section 1 and in modern cultivars at nitrogen of at least 96. That subset takes straw's weight from 0.55 to 0.28. The dilemma and a negative association, -0.62 to -0.90, hold in every row of the scaler, cap, subset and trend variants.

Biomass, a function of grain and straw, takes exponent 0.00 and leaves the fit unchanged; the harvest index, the other function of the two, displaces grain, whose exponent falls to 0.00, and the second term goes. Rotating the two log yields before the fit and pulling the frontier back weights grain and straw by 0.71 and -0.23, or -0.11 and 0.71 with the second component reversed: a frontier that rewards less of one yield, with no ceiling. Two metrics leave nothing to reduce. A principal component analysis after the fit gives one direction, grain against straw.

## The check on your own dataset

Refit the dataset with one conditioning change at a time: scaler, caps, a subset, a trend removed. Read the contending set, the sign of the association near the frontier, each exponent's range and whether the second term's contending set is one metric. A weight that moves with the scaler is the scaler's.

## What the example cannot show

The table is the straw-recorded subset, not the experiment. Cultivar is confounded with decade and weather, so the cultivar comparison describes and does not test breeding.
