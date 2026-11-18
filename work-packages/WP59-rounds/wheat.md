# WP59 wheat: the conditioning ladder and the chains

Grain (g) and straw (s), Broadbalk's straw-recorded plot-years. Each row changes one thing from the primary rule (orientation +1, shift 0, standard scaler of the log, tau at a tenth of rows above the surface; band 1/tau); subsets refit it on their rows. The quantile row maps the uniform output u to u' = (1 + (n - 1)u)/n and takes exp(u'). Plus h adds the harvest index g/(g+s) as a third metric, plus b biomass g+s. PCA rows rotate the standardized log-metrics, centre and exponentiate the scores, and sign each component so its largest loading is positive (p2 is g minus s; the last row reverses it). Elasticity: percent change of the second metric per percent of the first (straw per h in the h row). Source: `examples/wheat/variants.json`.

| row | rows | tau | set, tau = inf | exponents | elasticity | assoc. | K = 2 terms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| primary: standard scaler | 3,753 | 8.3 | g+s | 0.45 / 0.55 | -0.80 | -0.87 | g+s 0.57; g 0.43 |
| no scaler | 3,753 | 10.7 | g+s | 0.29 / 0.71 | -0.40 | -0.77 | g 0.53; g+s 0.47 |
| robust scaler | 3,753 | 8.3 | g+s | 0.51 / 0.49 | -1.02 | -0.85 | g+s 0.55; g 0.45 |
| quantile map | 3,753 | 25.9 | g+s | 0.48 / 0.52 | -0.91 | -0.90 | s 0.50; g 0.50 |
| capped 1st, 99th percentile | 3,753 | 8.3 | g+s | 0.44 / 0.56 | -0.80 | -0.88 | s 0.52; g 0.48 |
| winter wheat | 3,640 | 8.3 | g+s | 0.45 / 0.55 | -0.81 | -0.87 | g+s 0.57; g 0.43 |
| N at least 96 | 2,811 | 6.4 | g+s | 0.51 / 0.49 | -1.04 | -0.87 | g+s 0.51; g 0.49 |
| modern cultivars | 2,331 | 10.7 | g+s | 0.60 / 0.40 | -1.49 | -0.81 | g 0.64; g+s 0.36 |
| N at least 96, modern | 1,768 | 8.3 | g+s | 0.72 / 0.28 | -2.63 | -0.82 | g 0.69; s 0.31 |
| Section 1 | 1,043 | 9.4 | g+s | 0.72 / 0.28 | -2.60 | -0.68 | g+s 0.72; g+s 0.28 |
| plus h | 3,753 | 17.7 | s+h | 0.00 / 0.46 / 0.54 | -1.16 | -0.99 | s+h 0.64; s+h 0.36 |
| plus b | 3,753 | 8.3 | g+s | 0.45 / 0.55 / 0.00 | -0.80 | -0.87 | g+s 0.57; g 0.43 |
| year trend removed | 3,753 | 6.4 | g+s | 0.53 / 0.47 | -1.13 | -0.62 | g 0.65; g+s 0.35 |
| PCA before fit | 3,753 | 10.7 | p1+p2 | 0.34 / 0.66 | -0.50 | -0.95 | p1+p2 0.57; p1+p2 0.42 |
| PCA before fit, p2 reversed | 3,753 | 9.4 | p1+p2 | 0.42 / 0.58 | -0.72 | -0.97 | p1+p2 0.71; p1+p2 0.29 |

## Reading

**Fixed.** A dilemma (n = 2) and a negative association near the frontier (-0.62 to -0.99) in every row, whatever the scaler, cap, subset or year trend.

**Moved.** The weights. Grain's exponent runs from 0.29 (no scaler; grain's log-spread 0.64, straw's 0.80) to 0.72 (Section 1; N at least 96, modern). Robust, quantile and cap give 0.51, 0.48 and 0.44 against 0.45. Narrowing to modern cultivars at N at least 96 cuts straw's weight from 0.55 to 0.28 and the elasticity of straw per grain from -0.80 to -2.6. Tau follows the log-spread: 25.9 under the quantile map.

**Derived metrics.** Biomass takes exponent 0.00 and leaves the primary fit unchanged. The harvest index displaces grain (exponent 0.00): the set becomes straw and index, and the K = 2 grain ceiling goes.

**Year.** Straw falls 1.5 percent a year; grain has no trend. Without it the association is -0.62 and grain's exponent 0.53; the dilemma and the grain ceiling stay.

**Chains.** PCA after the fit gives one direction, grain against straw (loadings 0.71 and -0.71; 99 to 100 percent of the spread), a restatement of the line. PCA before the fit rotates two columns; p1 carries 84 percent of the variance. The fit on p1 and p2 pulled back to the standardized log yields weights 0.71 on grain and -0.23 on straw, or -0.11 and 0.71 with p2 reversed: a frontier that rewards less of one yield, by a sign convention, with no K = 2 ceiling. Not a useful chain here.

**K = 2.** The grain ceiling (a term whose set is grain alone, share 0.43 to 0.65) holds in the primary, winter, robust, N at least 96, modern, no-scaler and year-removed rows. The cap, the quantile map and N at least 96, modern add a straw ceiling. Section 1, the h row and the PCA rows have none.
