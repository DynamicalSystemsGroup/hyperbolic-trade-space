# Note: ADCS tension probe (does the current dataset expose recognizable, unasserted tensions?)

Date 2026-11-08. A read-only probe by the project manager, run before WP7 is scoped, on the accepted WP2 estimator
(`HyperbolicTradeSpace`) and the accepted WP4 dataset (`examples/adcs/data/adcs_designs.csv`, 1000 designs, seed 0).
Nothing here is committed code: the script was a scratch file. The WP3 tension report does not exist yet, so its
three parts were computed by hand with the same definitions as the WP3 scope.

## Method

- Rows: `settled` designs only (960 of 1000; the settling time of unsettled designs is censored at `t_end`).
- Conditioning by hand: each attribute becomes a larger-is-better log-metric u = −log(attribute), standardized to zero
  mean and unit standard deviation over the rows used; the estimator is given exp(u). Orientation is the reciprocal
  for all four (settling time, pointing error, mass, control effort), as the notebook will do with
  `LogAffinePreconditioner(orientation=[-1]*4)`. The standardization fixes the reference point, so the facet found is
  the one tangent at the balanced point of this conditioning (spec §4).
- Fits: τ = ∞ (LP, `min_exponent = 0`) for the contending set; a working τ found by bisection so that `frac_above_`
  is about 0.10.
- Near-frontier rows: |log V| < 1/τ at the working τ. Association is the Pearson correlation of u among those rows;
  tension directions are the PCA of the near-frontier Z (loadings mapped to metrics by `basis_`).
- Repeated on subsets by wheel class and by star-tracker grade.

## Results, all designs (n = 960)

- Contending set at τ = ∞: all four metrics, with exponents settling 0.202, pointing 0.143, mass 0.006, effort 0.649.
  Mass is in the support but almost inert (0.006).
- Working τ = 21.7: settling 0.198, pointing 0.146, mass 0.094, effort 0.562; 89 near-frontier rows, n_eff 16.9.
- Association among near-frontier designs: settling–effort −0.97 (tension), pointing–effort −0.73 (tension),
  pointing–mass −0.71 (tension), settling–pointing +0.62 (aligned), settling–mass −0.22, mass–effort +0.24.
- Principal tension directions: the first (72 % of the spread) loads settling +0.51, pointing +0.48, mass −0.54,
  effort −0.46: designs trade fast settling and good pointing against effort and mass together; the second (24 %)
  separates settling from pointing and effort.
- Unrestricted correlations of the four log-metrics over all designs are weak (|r| ≤ 0.37), so the structure above is
  frontier structure, not a global correlation.

## Results by subset

| subset | n | contending set at τ = ∞ (exponents) | notable near-frontier associations |
|---|---|---|---|
| wheel small | 332 | pointing .43, mass .55, effort .03 (size 3) | pointing–mass −1.00, pointing–effort −0.62 |
| wheel medium | 326 | pointing .42, mass .55, effort .03 (size 3) | pointing–mass −1.00, pointing–effort −0.87 |
| wheel large | 302 | pointing .41, mass .56, effort .04 (size 3) | pointing–mass −1.00, settling–effort −0.90 |
| ST coarse | 334 | settling .01, pointing .84, effort .15 (size 3) | pointing–effort −0.96, settling–effort −0.87 |
| ST medium | 327 | settling .05, pointing .50, mass .02, effort .43 (size 4) | pointing–effort −0.95, settling–effort −0.89 |
| ST fine | 299 | settling .14, pointing .25, effort .61 (size 3) | pointing–effort −0.99, settling–effort −0.98 |

Within a wheel class, mass takes three values (one per star-tracker grade), so the −1.00 pointing–mass association
there is the star-tracker grade itself: finer tracker, better pointing, more mass. Within a star-tracker grade, mass
varies only through the wheel class and is inert (exponent 0.00 to 0.02).

## Reading

What a spacecraft engineer would recognize, and the fit exposed without being told:

1. Settling speed against control effort (r = −0.97 near the frontier; the dominant exponent is on effort). Fast
   slews cost actuation effort. Recognizable.
2. Pointing against control effort (r = −0.73). The pointing budget is dominated by the steady-state error under the
   solar-pressure torque, which falls as 1/Kp, and high gains cost effort. Recognizable once explained.
3. Pointing against mass, through the star-tracker grade (r = −0.71 over all designs; −1.00 within a wheel class).
   A better sensor weighs more. Recognizable.
4. Settling and pointing are aligned (+0.62): both improve with the proportional gain. This is the co-movement the
   WP4 review noted; the fit reports it as alignment, not as tension.

What was not exposed:

5. Agility against mass through wheel class. Mass is weakly involved over all designs (τ = ∞ exponent 0.006, working
   0.094), and within a star-tracker grade it is inert. Wheel class changes settling little (median settling 301 s for
   small wheels against 264 s for large), because torque limits rarely bind (torque-saturated time fraction 0.7 % for
   large wheels, 7 % for small) and the gains dominate. The one place small wheels show up is the momentum flag
   (13.7 % of small-wheel designs violate it, none of the others), and the flag is not a metric.

## Caveats

- Near-frontier samples are small (89 rows over all designs, 19 to 34 per subset): the associations and the
  exponents below about 0.03 are noisy, and the LP support is sensitive to a few vertex designs. The 0.006 on mass is
  at the level of that sensitivity.
- The result depends on the hand conditioning (standardized reciprocals). A different reference point would pick
  another facet. The notebook will have to show the conditioning diagnostics and, ideally, a sensitivity check.
- Mass takes only nine discrete values, so any association with it is largely a statement about hardware strata.

## Verdict for the driver

The current dataset exposes three recognizable, unasserted tensions (settling vs effort, pointing vs effort, pointing
vs mass via star-tracker grade) and one recognizable alignment (settling and pointing). The contending set at τ = ∞ has
size 4 over all designs, with mass nearly inert, and size 3 within each wheel class and star-tracker grade. It does not
expose the agility-vs-mass story through wheel class, which the spec names as a candidate tension. Whether the
requirement ("recognizable and intuitive once explicated") is met by the first three alone, or the case should be
enriched so that wheel class matters (scenarios where small wheels saturate, a wider hardware spread, or a power-like
attribute), is a decision for the supervisor; WP7's scope carries it as an open decision.
