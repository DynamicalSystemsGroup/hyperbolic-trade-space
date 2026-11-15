# WP43 spike protocol (D-1)

Written and committed before any fit of the spike. The readout's numbers follow this file's measures; any change
after the first fit is an amendment appended at the end, with the reason and the commit at which it was made,
and the readout says which numbers it touches.

## Question

The one-term line in the adjusted plane (Figure 5) leaves a visible downward bend at the upper right of the
case's table. Is that bend more terms' work, or a kernel's: a model that is not a posynomial but keeps the fit
and the designer's problem convex? Where does that class end?

## Models

Every model scores a row by `log V(u)`, `u = log m`, and calls a row beyond the surface when `log V > 0`.
All fits take the conditioned metrics of the case (`case.load_study`), strictly positive, larger is better.

| id | model | fitted by | selection of tau |
|---|---|---|---|
| K1 | one term, `log V = w.u - beta` | the package as shipped (`HyperbolicTradeSpace`, `n_terms=1`) | `select_temperature`, target 0.10 above, bounds (3, 1e3) |
| K1c | one term, same criterion as LQ (control) | `models.py`, cvxpy, `Q = 0` | as K1 (own bisection, below) |
| K2 | two terms, sharp (`term_temperature = inf`) | the package, `n_terms=2`, `random_state=0`, five restarts | `select_temperature` with `n_terms=2` |
| K3 | three terms, sharp | the package, `n_terms=3` | `select_temperature` with `n_terms=3` |
| K2s | two terms, soft | the package, `n_terms=2`, `term_temperature = tau` (the K2 value of that fit), `term_aggregation="mean"` (the log-mean-exp convention) | the K2 tau of the same fold; the soft fit's own training fraction above is recorded |
| LQ | one log-quadratic term, `log V = w.u + (1/2) u'Qu - beta`, `w` on the simplex, `Q = B'SB`, `S` positive semidefinite (`B` the Helmert chart, so `Q1 = 0`) | `models.py`, cvxpy | own bisection, below |

The LQ and K1c criterion is the mean slack of the model it reports, the criterion the package's K > 1 fits use:
minimise `LME_tau(f(u_i)) - mean_i f(u_i)` over `(w, S)` (`tau = inf`: `max_i f(u_i) - mean_i f(u_i)`, the exact
maximum), with `f(u) = w.u + (1/2) u'Qu`, `beta = LME_tau(f(u_i))` over the training rows (the log-mean-exp, never
the unnormalised sum), and `log V = f(u) - beta`. The package's one-term fit minimises `beta` alone; with `Q`
free that criterion has `Q = 0` as a minimiser for every table (adding `Q` to a fixed `w` only raises every
`f(u_i)`, so the maximum cannot fall), so it cannot tell a curved surface from a plane. This is why the K1c control
is fitted: it separates the effect of `Q` from the effect of the criterion.

Solver of LQ and K1c: cvxpy with Clarabel; SCS if Clarabel does not return `optimal`. The solver status is
recorded per fit; a fit that is neither `optimal` nor `optimal_inaccurate` is dropped from a mean and counted.

Bisection of tau for LQ and K1c, as `select_temperature`: bounds (3, 1e3), `log tau` halved until the training
fraction above 0.10 is met to within 0.01 or 12 halvings, whichever first; the nearest tau is kept.
When the package's `select_temperature` cannot bracket the target in a fold (`ValueError`, as can happen for
K > 1), the tau selected on the regime's full table for that model is used and the fold is flagged.

## Tables

**Data of record.** The two regimes of the cubesat case, `case.load_study("primary")` and `("stock")`
(`examples/adcs/data/v2`), 13 metrics, 2134 and 2355 feasible rows. The two regimes are fitted separately.
The conditioning of the table is fitted once on the whole regime (an affine map of the log attributes, the same
for every model); it is not refitted per fold.

**Planted tables** (a generator extended from `make_frontier_data`; `generators.py`). Four metrics, noise 0,
30 per cent frontier rows, interior depth `-Exp(1)`, the generator's seeded Gaussian chart coordinates and
exponents. Twenty tables per kind, table seeds 0 to 19, each with a fresh test sample of 2000 rows from the
same planted truth (seed 1000 + table seed).

- **three-term** (kind T): `make_frontier_data(400, 4, n_terms=3, exponents=[[.5,.5,0,0],[0,.5,.5,0],[0,0,.5,.5]],
  noise=0, random_state=seed)`, the table of Appendix C.7 at 400 rows.
- **log-quadratic edge** (kind Q): the generator's chart coordinates `z` and level `log V` with the planted
  `f(u) = w.u + (1/2) z'Sz`, `u = B'z + s 1`, `s = log V - w.B'z - (1/2) z'Sz`, `w` the generator's one-term
  exponents for the seed, `S = c V V'` with `V` a seeded orthonormal (d - 1) x r matrix, `c = 0.5`. Seeds 0 to 9
  have `r = 1`; seeds 10 to 19 have `r = 2`. Rows: 400. The truth's `log V` is the planted `log V`.
- **dent** (kind D): a one-term planted table of 450 rows (`make_frontier_data(450, 4, random_state=seed)`), then
  every row inside the ball of radius `rho = 1` in the space `(z, log V)` centred at `(z_c, 0)` is removed, where
  `z_c` has norm 1 and a seeded direction. The rows left (about 400; the count is recorded) have a notch in their
  edge that no convex surface can follow. The truth is the one-term plane the table was drawn from.

## Held-out protocol (R-3)

Five folds over rows, `sklearn.model_selection.KFold(5, shuffle=True, random_state=0)`, separately within each
table (a regime, or a planted table, is its own stratum). Every model of a table sees the same folds. For each
fold: select tau, fit on the four training folds, score the held-out fold. Planted tables are fitted sharp
(`tau = inf`, `term_temperature = inf`; K2s is not run on them) because they have no noise; the data of record are
fitted at the selected tau.

## Measures

Per model, per fold, on the held-out rows (`s_i = -log V_i`):

1. **slack**: the mean of `s_i` over the held-out rows with `log V_i <= 0` (rows below the surface).
2. **above**: the fraction of held-out rows with `log V_i > 1e-9`; beside it the training fraction above of the
   same fit (the fit's convention: 0.10 by the tau selection; K2s and the K > 1 fits that cannot reach it differ).
3. **band**: the fraction of held-out rows with `|log V_i| < 1/tau` of the fit.
4. **right tail slack** and **right tail above**: measures 1 and 2 over the held-out rows whose first plotted
   metric (`x = u_j`, `(j, k)` the first of `k_terms.slice_pairs` of the K1 fit on the regime's whole table, the
   plane of Figure 5) is in the top quintile of `x` of the regime's whole table. This is the upper right of the
   plane, where the bend is drawn. The left tail (bottom quintile) is reported beside it.
5. **solve time**: wall clock of one fit, tau selection excluded, on the full regime table, the median of three
   serial runs on the machine of the run (no parallel jobs); tau selection time is reported separately.

On planted tables, also from the fit on all 400 rows and the 2000 fresh test rows (the truth's `log V` known):

6. **frontier error**: root mean square of `log V_fit - log V_true` over the test rows with `log V_true = 0`
   (dent: over the test rows of the undented truth, which are all the truth's rows; the notch is read with 7).
7. **overall error**: the same over all test rows.
8. **notch level** (kind D only): `log V_fit` at the truth's frontier point at `z_c` (the centre of the removed
   ball). A surface that followed the notch would read `-rho = -1`; a convex surface cannot, and reads near 0
   or above. Also the mean slack and the fraction above over the **rim rows** of the table (rows between `rho` and
   `2 rho` from the ball's centre).

Reading thresholds (fixed here): a planted truth is **recovered** by a model when the median over the twenty tables
of the frontier error is at most 0.05 and of the overall error at most 0.10.

## The comparison and the rule that reads it

For each regime and for each measure 1 and 4, the paired difference to K1 per fold, `D_m = measure_m - measure_K1`,
its mean over the five folds and its standard error (`sd / sqrt(5)`). A model **hugs better** than K1 when its
mean slack difference is below `-2` standard errors and its held-out fraction above is not above K1's by more
than 0.02 (a model that merely sits lower is not hugging). Let `B` be the best of K2, K2s and K3 by mean
held-out slack under the same fraction-above condition. The verdict on the bend, per regime, by these rules in order:

1. If no model hugs better than K1: "none of these models hugs the bend out of sample".
2. If LQ's mean slack is below B's by more than `2` standard errors (paired): "a kernel's work".
3. If LQ's is above B's by more than `2` standard errors, or within `2` of it while B hugs better than K1:
   "more terms' work" (the posynomial reaches what the kernel reaches).
4. Otherwise (LQ hugs better than K1, B does not): "a kernel's work".

The same rules are applied to the right tail slack, and the verdict of each is reported; if they differ, both are
reported, with no merging.

On planted tables: recovery by the thresholds above per kind and model, the median and the quartiles of each
error; the matrix of kind by model is the class boundary measured: a kind in the class (T by K3, Q by LQ) is
recovered, a kind outside a model's class is not, and the dent's notch level is near 0 or above for every model.

## Figures

For each regime, one figure of the adjusted plane per model (K1, K2, K3, K2s, LQ), from the models fitted on the
whole table: the K1 fit's two heaviest metrics `(j, k)` on the axes; the other metrics held at the coordinate-wise
median of K1's near-frontier rows; the vertical coordinate of each design is the `u_k` that puts the design at its
own level `log V` with the others at that median (a 1-D root find along `u_k`), so that the surface is the curve
`log V = 0` in the plane and a design's distance below it is its level; designs one grey, the surface black, the
held-out rows (of fold 0) a second dark grey. For K1 this is Figure 5's construction with the median taken
coordinate-wise. Judged by the project's figure review (`docs/superpowers/notes/figure-review.md`), as rendered.
A boundary figure for kind D: one table (seed 0), the plane of two metrics, the removed ball's rim, and the K1, K3,
LQ surfaces.

## Environment and reproduction (R-2)

`uv run --with cvxpy python work-packages/WP43-rounds/spike/run.py <stage>` from the repository root, stages
`real`, `planted`, `times`, `figures`, `all`. No change to `pyproject.toml` or `uv.lock`; the cvxpy version and
its solvers are recorded by `run.py` in `results/environment.txt`. Seeds: folds 0, table seeds 0 to 19, test seeds
1000 + table seed, package `random_state=0`, `S` orthonormal basis seed 500 + table seed. Every number in the
readout is read from `results/` written by `run.py`.

## Amendments

1. Before any result was read (smoke test of the LQ solve at one temperature on the primary table):
   Clarabel returns `optimal_inaccurate` on the log-quadratic programs, with the same objective to six digits under
   tighter tolerances (0.022886 at tau = 50 and 0.046948 at tau = inf on the first 600 rows, run with default and
   tightened settings), and SCS is eleven times slower. Rule now: Clarabel's `optimal` and `optimal_inaccurate`
   are both accepted and the status is recorded; SCS is used only when Clarabel raises or returns no solution.
   The rule on dropping fits is unchanged.
2. **After the results of `real` and `planted` were read** (post hoc, so the readout labels it so): the whole-table
   LQ fit of each regime has a negative partial derivative of `f` at about a quarter of the (row, metric) pairs, as
   low as -2.4 against exponents of at most 0.34 (`results/lq_monotone.md`, from `diagnostics.py`): the surface of the
   protocol's LQ is not monotone in the metrics, which a larger-is-better score should be. Added: **LQm**, LQ with
   the linear constraint `w + Q u_i >= 0` at every training row, fitted with the same folds, the same tau selection
   and the same measures (`run.py lqm`, `results/real_fits_lqm.csv`). It is shown beside the protocol's table and
   does not enter the verdicts of the four rules, which are those of the protocol as written. No model was removed
   and no measure changed. Also noted: LQ has 1 + 12 x 13 / 2 free parameters against K3's 39, so a gain of LQ over K3
   mixes shape and capacity; a capacity-matched run (more terms) is not in this protocol and is left to the readout's
   options.
3. **Figures** (post hoc, before the readout was written): the plane construction of the Figures section is not
   defined for a model that is flat or not monotone in the vertical metric (three-term sharp has a term with exponent
   0 on it; the unconstrained log-quadratic term is convex in it), so every design was placed at (its first plotted
   metric, its level `log V`) with the surface the line `log V = 0`. For K1 this is Figure 5's plane up to the factor
   `w_k` and a flip of the vertical axis; the same axes in every panel make the models comparable. The panels are
   K1, K2, K2s, K3, LQ and LQm (K1c, a control that coincides with K1, is not drawn). The boundary figure draws the
   removed ball and three fits along the line through the notch centre.
