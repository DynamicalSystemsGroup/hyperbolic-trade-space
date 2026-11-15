# WP59: perovskite solar cells, the conditioning ladder and the chains

Source: `examples/perovskite/variants.json`, written by `uv run --frozen python examples/perovskite/variants.py`. The temperature puts a tenth of rows above the surface. The primary row reproduces the record (tau 18.8, exponents 0.17, 0.41, 0.42, K = 2 shares 0.976 and 0.024). The table has no covariate and no time or cost metric, so the ladder has no mass or orientation step.

## Ladder

| variant | rule | rows | tau | set at tau = inf | Voc/Jsc/FF (PCE) | assoc. Voc-Jsc/Voc-FF/Jsc-FF | Voc to Jsc elasticity | band | K = 2 shares | second term Voc/Jsc/FF | slack K=2/K=1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| primary | the record: log, standard scaler | 40,045 | 18.8 | Voc,Jsc,FF | 0.17/0.41/0.42 | -0.14/-0.39/-0.63 | -2.36 | 0.053 | 0.976/0.024 | 0.27/0.00/0.73 | 0.560/0.594 |
| no_scaler | pure log | 40,045 | 33.3 | Voc,FF | 0.01/0.00/0.99 | +0.29/-0.05/-0.03 | -0.00 | 0.030 | 0.742/0.258 | 0.12/0.00/0.88 | 0.141/0.197 |
| robust_scaler | robust scaler of the log | 40,045 | 13.7 | Voc,Jsc,FF | 0.12/0.27/0.61 | -0.13/-0.39/-0.64 | -2.35 | 0.073 | 0.958/0.042 | 0.13/0.00/0.87 | 0.797/0.886 |
| quantile | uniform quantile, shifted into (0, 1] | 40,045 | 29.4 | Voc,Jsc,FF | 0.43/0.29/0.28 | -0.50/-0.44/-0.39 | -0.68 | 0.034 | 0.504/0.496 | 0.00/0.77/0.23 | 0.259/0.319 |
| extremes_capped | Voc at most 2 V, Jsc at most 40 (S1) | 40,040 | 25.9 | Voc,Jsc,FF | 0.24/0.75/0.02 | -0.82/+0.23/-0.27 | -3.11 | 0.039 | 0.852/0.148 | 0.36/0.19/0.45 | 0.403/0.491 |
| pce_added | PCE added as a fourth metric (S6) | 39,980 | 22.8 | Voc,Jsc,FF,PCE | 0.14/0.36/0.00/0.50 | -0.69/-0.05/-0.34 | -2.65 | 0.044 | 0.986/0.014 | 0.26/0.02/0.72/0.00 | 0.517/0.595 |

After the fit, the first direction of the near-frontier spread sets Voc (0.76) against FF (-0.64) in the primary row (63 percent) and FF (-0.81) against Jsc (0.46) and Voc (0.36) under the cap.

## Chains

PCA before the fit acts on the standardized log-metrics. Screen: a column is carried when the first two components hold at least 0.75 of its variance; the carried columns are fitted. Rewriting: the first two or three scores, centred, scaled to unit spread and exponentiated so they are positive, each component signed so its largest loading is positive; the scores are fitted. ICA (FastICA) ran the same two ways because PCA changed the reading: the screen dropped a contending metric, or a rewriting had fewer contending scores than scores.

| table | rows | fit of all columns | screen carries | fit of carried | PCA, 2 scores | PCA, 3 scores | ICA, 2 scores | ICA, 3 scores |
|---|---|---|---|---|---|---|---|---|
| Voc, Jsc, FF | 40,045 | Voc,Jsc,FF | 2 of 3 | Voc,FF | PCA1 | PCA1,PCA3 | ICA1,ICA2 | ICA1,ICA2,ICA3 |
| 12 JV columns | 7,871 | default_Voc,reverse_Jsc,forward_Jsc | 7 of 12 | default_Voc,reverse_Jsc | PCA1,PCA2 | PCA1,PCA2 | ICA1,ICA2 | ICA1,ICA2,ICA3 |
| default scan JV, end-of-test PCE, T80 | 1,408 | default_Voc,default_Jsc,end_of_experiment_PCE | 1 of 6 | none to fit | PCA1,PCA2 | PCA1,PCA3 | ICA1,ICA2 | ICA1,ICA2 |

## What stayed fixed

Voc, Jsc and FF are the contending set in every three-metric row except the unscaled one; with PCE added the set grows and FF falls to exponent 0.00. Voc and Jsc are negatively associated in every row except the unscaled one (-0.13 to -0.82), Jsc and FF in every scaled row (-0.27 to -0.64). K = 2 lowers the mean slack in every row (slack is in each row's own units).

## What moved

The weights, across the scaled rows: Voc 0.12 to 0.43, Jsc 0.27 to 0.75, FF 0.00 to 0.61, and the elasticity of Jsc against Voc from -0.68 to -3.11. The reading to report is the set and the signs with the range of the weights.

With no scaler the weight goes to FF (0.99), the attribute whose log varies least (standard deviation 0.24, against 0.35 and 0.68), the set is Voc and FF, and the Voc-Jsc association turns positive (+0.29).

## What the chains did

Device metrics. The first component loads the three alike (0.57, 0.59, 0.57; 62 percent): the overall level of a cell. The second sets Voc (0.76) against FF (-0.64), the third Jsc (0.80) against FF (-0.51) and Voc (-0.31). The screen drops Jsc, which holds 0.65 of its variance in the first two, so the fit sets Voc against FF and loses the pair the physics names. Two scores put all the weight on the level score; three give level against the third, Jsc against FF and Voc. ICA with three scores returns near-axis components (FF 0.96, Voc 0.98, Jsc 0.95), all in the set, the primary reading again.

Twelve JV columns. Default and reverse scans load alike to two decimals, so which scan holds the weight is arbitrary: the set is default Voc, reverse Jsc and forward Jsc. The components are the level, then Voc (0.52) against FF (-0.26), a dilemma (association -0.92).

JV and stability (1,408 rows). The second component is stability: T80 0.69, end-of-test PCE 0.68. Two scores put level and stability both in the set (association -0.91). Three scores drop stability (exponent 0.00) and bring in Voc against FF. The stability result depends on how many scores are kept.
