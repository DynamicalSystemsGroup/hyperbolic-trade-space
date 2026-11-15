# WP59: amniote life histories, the conditioning ladder

Source: `examples/amniote/variants.json`, written by `uv run --frozen python examples/amniote/variants.py`. Metrics: longevity (L), litter size (S), litters per year (Y), earliness of maturity (E, maturity in days inverted). The temperature puts a tenth of rows above the surface. The primary row reproduces the record: tau 10.7, exponents 0.51, 0.09, 0.04, 0.36, shares 0.66 and 0.34, mean slack 0.345 against 0.412.

| variant | rule | rows | tau | set at tau = inf | L/S/Y/E | assoc. L-E/L-Y/L-S | L to E elasticity | band | K = 2 shares | second term L/S/Y/E | slack K=2/K=1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| primary | the record: log, standard scaler, maturity inverted, mass left in | 2,770 | 10.7 | L,S,E | 0.51/0.09/0.04/0.36 | -0.97/-0.66/-0.06 | -0.70 | 0.094 | 0.66/0.34 | 0.36/0.19/0.11/0.34 | 0.345/0.412 |
| no_scaler | pure log | 2,770 | 3.4 | E | 0.00/0.00/0.00/1.00 | -0.21/-0.32/-0.12 | none | 0.294 | 0.58/0.42 | 0.10/0.41/0.28/0.21 | -0.017/1.554 |
| robust_scaler | robust scaler of the log | 2,770 | 12.1 | L,S,E | 0.53/0.15/0.00/0.31 | -0.97/-0.67/-0.04 | -0.59 | 0.083 | 0.68/0.32 | 0.28/0.36/0.10/0.26 | 0.249/0.318 |
| quantile | uniform quantile, shifted into (0, 1] | 2,770 | 27.6 | L,S,E | 0.41/0.14/0.14/0.30 | -0.89/-0.64/-0.06 | -0.74 | 0.036 | 0.52/0.48 | 0.73/0.00/0.05/0.22 | 0.064/0.111 |
| maturity_not_inverted | maturity read as larger is better | 2,770 | 3.4 | L,Y | 0.51/0.08/0.39/0.02 | +0.84/-0.91/-0.26 | -0.04 | 0.294 | 0.66/0.34 | 0.22/0.25/0.48/0.05 | 0.334/0.475 |
| mass_partialled_out | log mass regressed out of each log metric | 2,770 | 8.3 | L,S,Y,E | 0.48/0.12/0.06/0.33 | -0.93/-0.60/-0.17 | -0.69 | 0.121 | 0.72/0.28 | 0.15/0.24/0.19/0.42 | 0.415/0.471 |
| mass_dropped | mass not required | 2,776 | 10.7 | L,S,E | 0.51/0.09/0.04/0.35 | -0.97/-0.66/-0.06 | -0.70 | 0.094 | 0.66/0.34 | 0.36/0.20/0.11/0.34 | 0.346/0.412 |
| annual_fecundity_added | S times Y added as a fifth metric (F) | 2,770 | 10.7 | L,S,E | 0.51/0.09/0.04/0.36 +F 0.00 | -0.97/-0.66/-0.06 | -0.70 | 0.094 | 0.66/0.34 | 0.36/0.19/0.11/0.34 | 0.345/0.412 |
| maturity_not_inverted_quantile | two changes: maturity not inverted, quantile map | 2,770 | 13.7 | L,Y | 0.26/0.17/0.44/0.13 | +0.76/-0.82/-0.24 | -0.47 | 0.073 | 0.60/0.40 | 0.09/0.00/0.12/0.79 | 0.047/0.119 |

Association is the near-frontier correlation of log-metrics. Mean slack is in each row's own units, so K = 2 is compared with K = 1 within a row. After the fit, the first direction of the near-frontier spread loads longevity 0.68, earliness -0.59 and litters per year -0.35 in the primary row, and within 0.07 of those under the robust scaler, the quantile map, mass dropped and mass partialled out.

## What stayed fixed

With maturity inverted and a scaler used, longevity and earliness are in the contending set and their association is -0.89 to -0.97. Longevity against litters per year stays at -0.60 to -0.67 and against litter size near zero (-0.04 to -0.17). Longevity holds the largest exponent in every such row (0.41 to 0.53). Not requiring mass adds six species and moves no exponent by more than 0.01. Annual fecundity takes exponent 0.00, since it is a function of two metrics already present. K = 2 lowers the mean slack in every row.

## What moved

The weights. Earliness runs 0.30 to 0.36, litter size 0.09 to 0.15, litters per year 0.00 to 0.14. The quantile map evens them (0.41, 0.14, 0.14, 0.30), moves tau to 27.6, and splits K = 2 nearly in half (0.52 and 0.48). Partialling out mass adds litters per year to the set. The set and the signs are readings; the weights are not.

## The scaler test

With no scaler one metric takes all the weight: earliness 1.00, a monolemma, with tau 3.4. The standard deviations of the log attributes differ (0.58 for litters per year, 1.04 for maturity), so the units decide the fit. A scaler is required; the set survives the choice among them.

## The orientation lesson

Maturity is a time cost, so the metric is its inverse and the orientation is -1 in the log. Left uninverted, the fit treats late maturity as good: longevity and maturity align (+0.84 against -0.97), the set becomes longevity with litters per year, the exponent on maturity falls to 0.02, and the band widens to 0.294. The quantile map reproduces the flip (+0.76, same set), so a different scaler does not repair a wrong direction.

An analyst states for each attribute whether more is better, with the reason (time to maturity is a cost), then flips each time or cost attribute once and refits. If the contending set or an association sign changes, the orientation decided the result and the analysis states it. Here it did: the trade-off the table shows is longevity against early maturity, and the uninverted table shows longevity agreeing with lateness.

## Chaining

PCA after the fit gives the same first direction across the scaled rows. PCA before the fit is the perovskite experiment; this table has four metrics.
