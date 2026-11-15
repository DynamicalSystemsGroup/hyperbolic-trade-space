# Conditioning and feature engineering: a readout for the decision analyst

The analyst turns attributes into strictly positive, larger-is-better metrics, and each choice in that step can change the answer. Three public tables were refitted with one choice changed at a time: perovskite solar cells (40,045 rows, three metrics), amniote life histories (2,770 rows, four) and Broadbalk wheat (3,753 rows, two). The numbers are in `examples/<case>/variants.json`, from `examples/<case>/variants.py`.

The check for every choice is the same. Refit with the choice changed, with the fit temperature at infinity for the contending set and at the temperature the rule chose for the rest, and compare three quantities: the contending set, the sign of each near-frontier association from `trade_off_report`, and the exponents. If the set and the signs move, the choice decided the result and the analysis states it.

## Choices before the fit

### Orientation of every metric

Each time or cost attribute is a larger-is-better metric only after it is inverted. In the amniote table, maturity in days is a time cost, so the metric is earliness. Read as larger is better, maturity changes the result: the association of longevity with maturity goes from -0.97 (earliness) to +0.84, the contending set goes from longevity, litter size and earliness to longevity and litters per year, and the exponent on maturity falls from 0.36 to 0.02. A quantile map does not repair it (+0.76, the same set).

State for each attribute whether more is better, with the reason. Flip each time or cost attribute once and refit; a changed set or sign means the orientation decided the result. Perovskite and wheat have no time or cost metric, so this choice does not arise.

### The scaler

The fit temperature is a number per unit of log-spread, so a scaler makes one temperature mean the same thing for every metric. With no scaler one metric takes nearly all the exponent, and which one is an artefact of the raw units: in the amniote table earliness takes 1.00 and the others 0.00, at a fit temperature of 3.4; in the perovskite table FF takes 0.99 and the Voc-Jsc association turns positive (+0.29); in the wheat table straw takes 0.71.

The standard scaler takes the log-spread as the metric's scale; the robust scaler takes the interquartile range, which suits a few extreme rows; a quantile map keeps only the rank order; it evens the exponents (amniote 0.41, 0.14, 0.14, 0.30) and raises the fit temperature (27.6 amniote, 29.4 perovskite, 25.9 wheat). Refit under all three; in every case the contending set and the association signs held.

### Extremes

An exact maximum is set by the largest rows. The perovskite table has five rows with Voc above 2 V or Jsc above 40 mA/cm2, probably module or unit entries. Capping them (40,040 rows) moves the exponents from 0.17, 0.41, 0.42 to 0.24, 0.75, 0.02 and the Voc-Jsc association from -0.14 to -0.82. Look at the largest values of every attribute, cap or remove entries that cannot be real, and refit. In the wheat table capping at the 1st and 99th percentile moved nothing (grain 0.44 against 0.45).

### Derived metrics

A metric that is a function of the others absorbs them. Perovskite PCE added as a fourth metric takes exponent 0.50 and FF falls to 0.00. Amniote annual fecundity, litter size times litters per year, takes 0.00 and changes no other number. Wheat biomass, grain plus straw, takes 0.00. The wheat harvest index, grain over grain plus straw, displaces grain (exponent 0.00): the set becomes straw and the index, and the second term whose contending set is grain alone goes. A derived metric takes the exponent or takes none. Fit the underlying attributes and set the derived ones aside; to test a candidate, add it as an extra metric: an exponent of 0.00 means it added nothing, a changed set means it replaced the attributes it summarizes.

### The covariate

In the amniote table body mass is the covariate. It was kept, partialled out (the linear effect of log mass removed from each log metric) or dropped (six more species). Dropping it moved no exponent by more than 0.01. Partialling it out left the longevity-earliness association at -0.93 against -0.97 and added litters per year to the contending set, with the exponents at 0.48, 0.12, 0.06, 0.33. Where a covariate is a size or scale, compare the three treatments; if the set and the signs hold, keep the simplest.

### Chaining with PCA before the fit

On the perovskite table, PCA on the standardized log-metrics was used two ways. As a screen, a column is carried when the first two components hold at least 0.75 of its variance. The screen dropped Jsc, which holds 0.65, and the fit then set Voc against FF and lost the pair the physics names. As a rewriting, the scores are centred, scaled, exponentiated to be positive and signed so each component's largest loading is positive. The first component loads the three metrics alike (0.57, 0.59, 0.57): the overall level of a device. Two scores put all the exponent on that level. The scores are a change of representation: a positive leading loading orients a score and says nothing about whether a stakeholder wants more of it; each component needs its own reading. On JV with stability the result depended on whether two or three scores were kept (stability in the set at two, out at three).

At two metrics it is not a chain. In the wheat table PCA before the fit rotates two columns; the fit on the scores pulled back gives grain 0.71 and straw -0.23, or -0.11 and 0.71 with the second component reversed, a frontier that rewards less of one yield. Fit the metrics and the scores and compare the sets.

### The chain the package runs after the fit

PCA on the near-frontier chart is the package's chain. It reads the spread of the near-frontier designs; the check is to compare the first direction's loadings (`trade_off_report`, `spread_loadings`) across the ladder's rows. It gave the same first direction across scaled rows in the amniote table (longevity 0.68, earliness -0.59, litters per year -0.35 in the primary row, within 0.07 under the robust scaler, the quantile map, mass dropped and mass partialled out). In the wheat table it gave one direction, grain against straw (0.71 and -0.71, 99 to 100 percent of the spread), a restatement of the line. In the perovskite table it set Voc (0.76) against FF (-0.64).

## What the three cases say in common

The contending set and the association signs held under the scaler ladder; the exponents did not. In the perovskite table the set is Voc, Jsc and FF in every three-metric row but the unscaled one and Voc-Jsc is negative in every other row (-0.13 to -0.82), while Voc runs 0.12 to 0.43, Jsc 0.27 to 0.75 and FF 0.02 to 0.61 (0.00 only when PCE is added); the elasticity of Jsc with respect to Voc runs -0.68 to -3.11. In the amniote table longevity and earliness stay in the set with association -0.89 to -0.97, longevity against litters per year at -0.60 to -0.67, while earliness runs 0.30 to 0.36 and litters per year 0.00 to 0.14. In the wheat table the dilemma and a negative association (-0.62 to -0.90) hold under every scaler, cap, subset and year trend, while grain runs 0.29 to 0.72.

The fit temperature (the WP45 records' sweeps, not the ladder) moved the exponents little where the fit is settled: amniote longevity 0.48 to 0.51 and wheat grain 0.43 to 0.45 between tau 3 and 100. The perovskite exponents move below tau about 10 (FF 0.00, 0.31, 0.42, 0.43, 0.43 at tau 3, 10, 18.8, 30 and infinity) and are flat above it.

The cases differ in what decided the reading: orientation in the amniote table, five rows in the perovskite table, and in the wheat table the harvest index and the subset, which moved grain from 0.45 to 0.72 and the elasticity of straw with respect to grain from -0.80 to -2.6.

## What each page shows and states

**Perovskite.** Show the contending set and the three association signs with each exponent's range across the scaler and the cap, not one exponent. State the cap on five rows and its reason (it moves Voc-Jsc from -0.14 to -0.82). State that PCE is set aside because it takes FF's exponent.

**Amniote.** Show the set (longevity, litter size, earliness), the longevity-earliness association (-0.89 to -0.97) and the exponents as ranges. State the orientation with its reason (maturity is a time cost; uninverted the association is +0.84), that annual fecundity is set aside because it is a function of two metrics, and that mass kept, partialled out or dropped leaves the set and the signs.

**Wheat.** Show the dilemma and the association range (-0.62 to -0.90), with grain's exponent as a range (0.29 to 0.72) and the subset that moves it. State that biomass and the harvest index are set aside: biomass takes 0.00, and the index displaces grain. State that PCA before the fit is not used at two metrics.
