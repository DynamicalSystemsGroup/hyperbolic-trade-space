# WP35 stage 1b: hypothesis and refutation conditions (written before any new table is generated or any method is run on one)

Date: 2026-11-12. This file and the three scripts `experiment_tables.py`, `experiment_methods.py`, `experiment_summary.py` are committed together in one commit; the run's outputs
(`results.json`, `summary.txt`) are committed after it, so the commit hash of this file precedes every output.
Reasoning on the earlier spike (`../spike/readout.md`, section 2) is the only evidence seen so far: its four planted
tables and two cubesat tables, where the best match to a planted vector was the leading direction of spread only
in some cases. Nothing in this file has been run.

## Terms used below (one plain line each)

- **Edge.** A planted vector w with positive entries summing to one, and a bound: every row of the table satisfies
  w . log m <= beta, and a fraction of the rows (here 30 percent) lies exactly on the plane w . log m = beta.
  This is what the method estimates, and w is its exponent vector.
- **Spread.** Variance of the log-metrics along a direction (what PCA ranks and HoroPCA's objective is a
  curved-space version of).
- **Spread ratio rho.** For a table built by construction A below: the standard deviation of the log-metrics along
  w (unit-length) divided by their standard deviation along the largest-spread direction orthogonal to w. By
  construction rho > 1 puts w as the direction of largest spread, rho < 1 puts a different direction first.
- **Recovered.** A method recovers w on a table when the absolute cosine between the method's direction and w is at
  least 0.9 (angle at most 25.8 degrees). For this work the direction is the fitted exponent vector; for PCA it is
  the first principal component; for HoroPCA it is the best-loss restart's first ideal point (k = 1). The threshold
  is fixed here, before the run; the chance rate for it (a uniformly random direction in R^4, a random point of the
  simplex for this work) is computed and printed by `experiment_summary.py`, and both are reported next to the results.
- **Recovery rate.** Recovered tables divided by tables in a cell (a cell = one arm at one setting).

## The hypothesis

**H (one sentence).** This work estimates the edge and PCA and HoroPCA estimate the spread, so a table in which the
edge and the spread are decoupled by construction separates them: this work recovers w whenever the edge is present,
whatever the spread; PCA and HoroPCA recover w only when w is also the direction of largest spread; and on a table
without an edge this work does not recover w, while PCA still does wherever w is the direction of largest spread.

The hypothesis is split into parts, each with the result that refutes it.

**H1 (this work follows the edge).** On every table that has the edge present (arms A and B below), this work
recovers w in a share of at least 0.9 of the tables of every cell, at every spread ratio.
*Refuted by:* any cell of arm A or arm B in which this work's recovery rate is below 0.9.

**H2 (PCA and HoroPCA follow the spread).** In arm A, PCA's first component recovers w when rho >= 2 (rate at least
0.9) and does not when rho <= 0.5 (rate at most 0.1). The same for HoroPCA k = 1 at R = 0.25 and R = 1 (its
embedding scales that make it a nearly flat patch or a moderately curved cloud). No prediction is made for HoroPCA at
R = 3, where the earlier spike saw restart-to-restart differences; it is reported, not tested.
*Refuted by:* (a) PCA's or HoroPCA's recovery rate at rho <= 0.5 above 0.1; or (b) their rate at rho >= 2 below 0.9.
Either means the first direction of these methods does not simply follow the spread, or that it follows the edge.

**H3 (the earlier agreement was the generator's, and the edge is what this work reads).** In arm B (the package's
own generator, which puts all depth along the all-ones direction, with w moved away from the uniform vector by
t in {0, 0.3, 0.6, 0.9}), PCA's first component has a recovery rate of at most 0.2 at t = 0.9 (the cosine of w with
the all-ones direction is then 0.54), while this work's rate stays at least 0.9.
*Refuted by:* PCA's rate at t = 0.9 above 0.2.

**H4 (without an edge this work does not find w).** In arm C (a Gaussian cloud with the same spread ratio as arm A at
rho = 2 and rho = 0.5, and no edge: the position along w is symmetric, not capped), this work's recovery rate is at
most 0.2 in both cells, and at rho = 2 PCA's first component recovers w at a rate of at least 0.9.
*Refuted by:* this work's rate above 0.2 in either cell; or PCA's rate at rho = 2 below 0.9.

**Part not in H.** The smallest-variance component of PCA is orthogonal to the directions of largest spread; on a
thin slab, where w carries the least spread, it will be w. That is reported (a column) because it is the
strongest case for PCA; it is excluded from H2 because the analyst cannot select that component without already
knowing w.

## The decision rule

The hypothesis **survives** if no refuting result above is observed; it is **refuted** if any is, and the readout
says which part. A part that fails does not rescue the others: each is reported with its cell rates and counts.
No threshold, cell or seed is changed after the first output is seen. Anything run beyond what is listed here is
labelled exploratory in the readout.

## The experiment (what the scripts do)

Common: d = 4 metrics, n = 300 rows, 6 table seeds per cell (seeds 100 to 105), no noise, 30 percent of rows
on the edge, beta = 0; this work's fit is `HyperbolicTradeSpace(n_terms=1, temperature=50.0, random_state=0)` as in the
earlier spike; PCA is the SVD of the centred log-metrics; HoroPCA is the authors' code (commit c9a9996), embedded as
in the earlier spike (centre, one scale so the farthest point has tangent norm R, exponential map at the origin), at
R in {0.25, 1, 3}, k in {1, 2}, 5 random restarts (torch seeds 0 to 4), Adam, learning rate 0.05, 500 steps, the
repository's defaults; the restart with the lowest final loss is "best", and the spread over the 5 restarts is
recorded for every cell (minimum, maximum, and the number of restarts that recover w).

- **Arm A (construction: edge in the plane, spread chosen freely in the plane).** For each seed, w is drawn from
  the uniform distribution on the simplex, redrawn until every entry is at least 0.05. Let u-hat be w/|w| and g the
  first of an orthonormal basis of the space orthogonal to w, both seeded. A row is
  u = a u-hat + xi1 g + xi2 q2 + xi3 q3, with q2, q3 completing the basis, xi1 ~ N(0, 1), xi2, xi3 ~ N(0, 0.3^2),
  and a = (log V)/|w|, where log V = 0 for 30 percent of the rows (the edge) and -Exp(m) for the rest. m is set
  from rho: m = rho |w| / 0.954 (0.954 = standard deviation of log V per unit m for this mixture), so the standard
  deviation of u along u-hat is rho and along g is 1. Cells: rho in {4, 2, 1, 0.5, 0.25}. Metrics are exp(u).
  In this table the edge (the plane w . u = 0 holding 30 percent of the rows) is identical in every cell; only the
  spread changes. *Refutation conditions:* H1, H2.
- **Arm B (the package's own generator, with w moved off the all-ones direction).** `make_frontier_data(300, 4,
  exponents=w_t)` with w_t = (1 - t) (1/4, 1/4, 1/4, 1/4) + t (1, 0, 0, 0) for t in {0, 0.3, 0.6, 0.9}, seeds 100
  to 105 (the generator's own Gaussian chart and exponential depth along the all-ones direction). The cosines of w_t
  with the all-ones direction are 1, 0.89, 0.69, 0.54. *Refutation conditions:* H1, H3.
- **Arm C (no edge).** Arm A's construction with a (the position along u-hat) drawn from N(0, rho^2) instead of
  from the capped log V, rho in {2, 0.5}: a symmetric cloud with the same spread and no edge. *Refutation
  condition:* H4.
- **Arm D (the tables of the earlier spike).** The four planted tables of the earlier spike (K = 1 seed 0; K = 2
  seed 7; K = 3 seeds 0 and 4), each term as a target, re-run with all five restarts recorded per cell. For
  context only; no refutation rule is attached.

Measures per table and method: the absolute cosine with w; the share of w recovered by two components, the
norm of the projection of unit w onto the span of the first two components (k = 2; 1 means w lies in the span);
the recovery indicator at 0.9. For this work also the L1 error of the exponent vector, sum_j |w_hat_j - w_j|.
Reported per cell: counts and rates of recovery, medians and ranges of the cosines, and for HoroPCA the spread over
restarts. Spread ratio is verified on each generated table (empirical standard deviations along u-hat and along
the top orthogonal direction are stored) so that a miscalibrated construction is visible.

## What was run before this file was committed (disclosed)

A smoke test of the construction of arm A and arm C at seed 999, a seed outside every cell (rho = 2 and 0.5 with
the edge, rho = 2 without it): generate the table, check the empirical spread ratio equals the intended one, fit
this work, take PCA's first component. Its purpose was to see that the construction and the fit run and that
the spread ratio is as designed; the seed is not used in any cell. A timing run of the authors' HoroPCA on one table
of the earlier spike (2.8 s for k = 1 and 4.1 s for k = 2 at n = 300) set the size of the experiment.
