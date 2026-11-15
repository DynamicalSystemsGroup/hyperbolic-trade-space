# Amniote life histories

Maturity in days is a time cost, so the metric is earliness, its inverse. That orientation is a
judgement the analyst states, and it decides the result. Read the other way, with later maturity as
better, the contending set changes from longevity, litter size and earliness to longevity and
litters per year, and the association of longevity with maturity goes from -0.97 to +0.84.

## The dataset

The Amniote life-history database [@myhrvold2015amniote], compiled from published studies by
Myhrvold and colleagues, holds 21,322 species of mammals, birds and reptiles in 36 columns. It is
released under CC0 1.0 (data DOI 10.6084/m9.figshare.3563457.v1). The command

```bash
uv run python examples/amniote/run.py
```

downloads the 6.5 MB archive, checks it against `examples/amniote/manifest.toml` and refits every
number on this page in about a minute.

The attributes are maximum longevity (years), litter or clutch size, litters or clutches per year,
female maturity (days) and adult body mass (grams). The table writes a missing value as
-999. Read as missing, the complete cases with all five attributes strictly positive are 2,770
species, 13 percent of the table: 1,548 mammals, 1,028 birds and 194 reptiles.

## The conditioning rule

`LogAffinePreconditioner` takes the log of each attribute and applies a standard scaler.

- Longevity: larger is better.
- Litter size: larger is better.
- Litters per year: larger is better.
- Earliness: maturity in days with orientation -1, because time to maturity is a cost.

Body mass is the covariate. Three treatments are fitted: kept in the metrics, partialled out (the linear effect of log mass removed from each
log-metric) and dropped, which adds six species. The contending set and the signs hold under all
three, with one change: partialling out mass adds litters per year to the set.

Annual fecundity, litter size times litters per year, is a function of two metrics already present.
Added as a fifth metric it takes exponent 0.00 and changes no other number, so it is set aside.

## The fit

At K = 1 the fit temperature is 10.7, chosen so that a tenth of species lie above the surface. The
contending set is longevity, litter size and earliness. At K = 2 and the same temperature the
terms hold 0.66 and 0.34 of the near-frontier species, and the mean slack falls from 0.412 to
0.345, status `certified`. The second term puts more weight on fecundity and less on longevity.

```python {.runnable}
import sys

sys.path.insert(0, ".")
from examples.amniote import run
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    select_temperature,
)
from hyperbolic_trade_space.plotting import plot_ternary

x = run.complete(run.load())
cols = [run.COLS[i] for i in (0, 3, 2)]
M = run.condition(x, cols=cols, orient=[1, -1, 1])
tau = select_temperature(M, 0.10, bounds=(3, 1e4))
fit = HyperbolicTradeSpace(temperature=tau, random_state=0).fit(M)
names = ["longevity", "earliness", "litters per year"]
plot_ternary(fit, M, names=names, lines=True)
```

<figure markdown>
![Triangle with longevity, earliness and litters per year at its corners; 2,770 species as points, lines of equal value and a numbered star at the fit's exponent vector, between longevity and earliness.](../generated/figures/amniote-ternary-light.png#only-light)
![Triangle with longevity, earliness and litters per year at its corners; 2,770 species as points, lines of equal value and a numbered star at the fit's exponent vector, between longevity and earliness.](../generated/figures/amniote-ternary-dark.png#only-dark)
<figcaption>Figure 9. Species as shares of longevity, earliness and litters per year; the star is the exponent vector of the one-term fit to these three, between longevity and earliness, with lines of equal value. Litter size is in the page's fit, not in this figure.</figcaption>
</figure>

## The named trade-off

The fast-slow continuum sets long life against early, fecund reproduction and has been re-evaluated
for mammals [@bielby2007fast]. Here the strongest trade-off is longevity against earliness, and
litters per year carries the fecundity side.

Across the standard, robust and quantile scalers and the three mass treatments, with maturity
inverted, longevity and earliness are in the contending set in every row. Their near-frontier
association is -0.89 to -0.97, and longevity against litters per year is -0.60 to -0.67. Longevity
against litter size is -0.04 to -0.17: litter size contends, but is nearly unrelated to longevity.

The exponents move across the same rows: longevity 0.41 to 0.53, earliness 0.30 to 0.36, litter
size 0.09 to 0.15, litters per year 0.00 to 0.14. The set and the signs are the reading, not one exponent. With no scaler earliness takes all the exponent: the raw units decide the fit.

## The check on your own dataset

State for each attribute whether more is better, with the reason. Flip each time or cost metric
once and refit. Compare the contending set and the signs of the association from `trade_off_report`
between the two fits. If either changes, the orientation decided the result and the analysis says
so. A quantile map does not repair a wrong direction: with maturity not inverted it gives +0.76 and
the same set.

## What the example cannot show

There is no designer: a point on the frontier is a species that evolved, not a design. The complete cases are the well-studied end of the table.
