# WP43 readout: beyond the posynomial, the kernel direction tested

Stage 1 (research spike) and stage 2 (decide) of the six-stage lifecycle. The protocol is `protocol.md`
(committed first, with three amendments, each dated by its commit and labelled; amendments 2 and 3 were made after
results were read and say so). Every number below is read from `results/`, written by
`uv run --with cvxpy python work-packages/WP43-rounds/spike/run.py all` (the scripts are in history at d0a97cd) from the repository root (environment in
`results/environment.txt`; `pyproject.toml` and `uv.lock` are unchanged). Nothing in `src/`, `paper/` or `docs/`
(beyond the D-4 note) changed.

## 1. The class (G1)

The definition and its two facts are on one page, `kernel-direction.md` (removed; `git show 4a76229:docs/superpowers/notes/kernel-direction.md`), for the glossary
entry to cite. In short:

- **Class.** Score `log V(u) = f_theta(u)` with `theta` in a convex set, `f_theta(u)` affine in `theta`, convex in `u`
  for each `theta` in the set, and `f_theta(u + s 1) = f_theta(u) + s`. Members: the monomial `w.u - beta`; the
  log-quadratic term `w.u + (1/2) u'Qu - beta`, `Q` positive semidefinite with `Q1 = 0` (the translog form of
  Christensen, Jorgenson and Lau 1973, doi 10.2307/1927992, with its restrictions). The finite maximum and the soft
  maximum of members score as members but their parameters no longer enter linearly: the fit is then the
  partition-and-refit scheme, a local optimum, as for `K > 1` (L4's note says the same of the posynomial).
- **Fact 1, the fit is convex in the parameters:** log-sum-exp of functions affine in the parameters minus a linear
  function (Boyd and Vandenberghe 2004, 3.1.5, 3.2.2; for the monomial L4 and Boyd, Kim, Vandenberghe and Hassibi
  2007; for the log-quadratic term a semidefinite program).
- **Fact 2, the designer's problem is convex in log-metrics:** `{f_theta <= 0}` is a convex set in `u`.
- **What it cannot represent:** a non-log-convex edge (a notch); measured in section 4.
- **Which word.** A generalized posynomial in `m` has `log f(e^u)` growing at most linearly in `u`; the
  log-quadratic term grows quadratically for `Q != 0`. So the log-quadratic term is in the class and is **not** a
  generalized geometric program in the metrics: "GGP" names a proper part of the class, "log-convex" (the word
  assumption (vi) already uses, convex in `u`) names the class. In the geometric-programming literature the metric-side
  name is log-log convex (Agrawal, Diamond and Boyd 2019, doi 10.1007/s11590-019-01422-z, record read in Crossref).
  The sentence of the paper that says "kernels that keep the model a GGP" is narrower than what the spike supports.
  The two papers' DOIs are resolved (Crossref); neither is in `docs/references.bib` yet, and entering them is the
  integrate stage's.

## 2. The comparison on the case (G2)

Models, measures and rules are the protocol's. Five folds, same folds for every model, tau selected on each training
fold to a training fraction above of 0.10 (except K2s, which takes K2's tau). Full tables of both regimes:
`results/real_summary.md`. Slack is in units of log V; "d vs K1" is the paired difference over the folds with its
standard error in brackets.

**primary regime, held-out rows** (2134 rows, 13 metrics; plane: first plotted metric available power)

| model | held-out slack | d vs K1 | held-out above | right-tail slack | right-tail above |
|---|---|---|---|---|---|
| K1 one term | 0.1400 | 0 | 0.098 | 0.1408 | 0.060 |
| K2 sharp | 0.0978 | -0.0422 (0.0023) | 0.099 | 0.1226 | 0.035 |
| K2s soft | 0.1012 | -0.0388 (0.0024) | 0.076 | 0.1276 | 0.026 |
| K3 sharp | 0.0803 | -0.0597 (0.0023) | 0.098 | 0.0865 | 0.129 |
| LQ log-quadratic | 0.0530 | -0.0870 (0.0032) | 0.098 | 0.0435 | 0.134 |
| LQm monotone (post hoc) | 0.0864 | -0.0536 (0.0024) | 0.101 | 0.0774 | 0.106 |

**stock regime** (2355 rows; plane: first plotted metric momentum headroom)

| model | held-out slack | d vs K1 | held-out above | right-tail slack | right-tail above |
|---|---|---|---|---|---|
| K1 one term | 0.1324 | 0 | 0.105 | 0.1125 | 0.190 |
| K2 sharp | 0.1136 | -0.0188 (0.0041) | 0.099 | 0.1140 | 0.101 |
| K2s soft | 0.1168 | -0.0156 (0.0040) | 0.074 | 0.1180 | 0.081 |
| K3 sharp | 0.0888 | -0.0436 (0.0037) | 0.099 | 0.0820 | 0.120 |
| LQ log-quadratic | 0.0720 | -0.0605 (0.0028) | 0.105 | 0.0853 | 0.139 |
| LQm monotone (post hoc) | 0.0942 | -0.0383 (0.0025) | 0.105 | 0.0977 | 0.142 |

The K1c control (one term by the mean-slack criterion) is within 0.001 of K1 in both regimes, so the criterion is
not what separates LQ from K1. No fit was dropped or flagged; Clarabel returned `optimal_inaccurate` on the LQ
programs with the same objective at tighter tolerances (amendment 1).

**The protocol's verdicts, as the four rules give them.** All held-out rows: **a kernel's work** in both regimes (LQ is
below the best posynomial, K3, by 0.027 on primary and 0.017 on stock, standard errors 0.002 and 0.001, at the same
held-out fraction above). Right tail: primary **a kernel's work** (LQ below K2, the best posynomial that hugs in the
tail under the above-fraction condition, by 0.079), stock **more terms' work** (K3 and LQ tie within two standard
errors). The tail verdicts differ between regimes and are reported unmerged. In the tail of primary, K3 and LQ sit
lower with more rows above (0.13 against K1's 0.06), so that tail comparison is not like for like.

**What the verdict leaves out, found after the rules were applied (amendment 2).**

1. The LQ surface is not monotone in the metrics. On the whole table 25 to 29 per cent of the (row, metric)
   pairs have a negative partial derivative of `f`, as low as -2.4 (primary) and -3.5 (stock) against exponents of at
   most 0.34 (`results/lq_monotone.md`): raising a metric lowers the level at those rows, which a larger-is-better
   score should not do. Its extra gain over K3 is that freedom.
2. With the linear constraint `w + Qu >= 0` at every row (LQm, same folds), the log-quadratic term is monotone at the
   rows (most negative partial about -1e-9) and its held-out slack is above K3's by 0.006 on primary and 0.005 on
   stock (standard errors 0.0007 and 0.0013) and below K2's by 0.011 and 0.019. So **a usable log-quadratic term does
   about what three posynomial terms do, a little less**, on this case.
3. Parameters: LQ has 13 + 78 free numbers against K3's 3 x 13, so a gap between LQ and K3 mixes shape and capacity.
   A run with more terms (K = 4 to 7 on the same folds) is the capacity-matched control; it is not in this protocol.

**The answer to the drawing's question.** On this case the bend is mostly more terms' work: a second term removes
0.042 (primary) and 0.019 (stock) of the held-out slack of the one-term line and a third removes 0.060 and 0.044; the
monotone log-quadratic term removes 0.054 and 0.038, between the second and third terms. The unconstrained
log-quadratic term removes more (0.087 and 0.061), but at a surface that is not a valid trade surface. Whether a kernel
beats many terms at the same parameter count is not answered here. In the plane (`figures/plane_primary.png`,
`figures/plane_stock.png`, every design at its level against the plane's first metric), the one-term panel's cloud
arches under the line, and the multi-term and log-quadratic panels flatten it; a figure review by the project's loop is
not part of this spike.

**Solve times** (`results/times_summary.md`; serial, median of three fits at the selected tau, then one selection with
fit; Apple M1 Max, other jobs on the machine):

| regime / model | tau | fit, median (s) | min | max | tau selection and fit (s) |
|---|---|---|---|---|---|
| primary / K1 | 41.72 | 0.02 | 0.02 | 0.02 | 0.19 |
| primary / K1c | 41.72 | 0.13 | 0.13 | 0.46 | 0.86 |
| primary / K2 | 113.22 | 1.65 | 1.65 | 1.66 | 11.80 |
| primary / K3 | 135.76 | 4.08 | 4.07 | 4.09 | 37.01 |
| primary / K2s | 113.22 | 3.12 | 3.04 | 3.14 | nan |
| primary / LQ | 403.46 | 81.85 | 81.82 | 82.90 | 263.49 |
| stock / K1 | 45.68 | 0.03 | 0.03 | 0.04 | 0.22 |
| stock / K1c | 45.68 | 0.17 | 0.17 | 0.19 | 0.94 |
| stock / K2 | 103.40 | 2.89 | 2.73 | 2.89 | 28.16 |
| stock / K3 | 135.76 | 7.08 | 6.87 | 7.22 | 50.16 |
| stock / K2s | 103.40 | 3.66 | 3.65 | 3.67 | nan |
| stock / LQ | 162.78 | 39.18 | 38.01 | 39.55 | 203.07 |

(K2s takes K2's tau, so has no selection of its own; K1c is the control; LQm was not timed.)

At the selected tau the log-quadratic fit takes 39 to 82 s: about ten times the three-term fit (4 to 7 s) and three orders
more than the one-term fit (0.02 to 0.03 s), a semidefinite program on 2100 to 2400 rows and 13 metrics; the tau
bisection takes it to 200 to 260 s.

## 3. More test cases than the cubesat (G3)

Twenty planted tables per kind, 400 rows, 4 metrics, noise 0, fitted sharp; recovery on 2000 fresh rows of the same
truth (`results/planted_summary.md`). Root-mean-square error of `log V` against the truth, median of the twenty tables
(frontier rows / all rows):

| kind | K1 | K2 | K3 | LQ |
|---|---|---|---|---|
| T three-term edge | 0.540 / 0.538 | 0.212 / 0.213 | **0.000 / 0.000** (recovered) | 0.247 / 0.245 |
| Q log-quadratic edge | 0.565 / 0.569 | 0.328 / 0.340 | 0.284 / 0.279 | **0.000 / 0.000** (recovered) |
| D dent | **0.000 / 0.000** | 0.027 / 0.028 | 0.034 / 0.038 | **0.000 / 0.000** |

(recovered: median frontier error at most 0.05 and overall at most 0.10, the protocol's threshold). Each kind in a
model's class is recovered to rounding (T by K3, Q by LQ at both ranks), and each kind outside it is not: K1 to K3 and
LQ miss the log-quadratic edge by 0.28 to 0.57 and LQ misses the three-term edge by 0.25. The dent is recovered by the
convex models because the removed ball does not move the edge they follow (section 4). K2 and K3 on the dent are off by
0.03 because they are local optima of the partition-and-refit (iteration-cap warnings in the log).

## 4. The boundary case (R-6)

On the twenty dent tables (about 410 rows left of 450; `removed` in the CSV is 40 for seed 0) every model in the class
leaves the notch the same way (`figures/dent.png`, table `results/planted_summary.md`, kind D):

| model | level at the notch's centre (median, min) | mean slack of the rim rows | rim rows above the surface |
|---|---|---|---|
| K1, K1c, K2, K3, LQ | 0.0000, 0.0000 | 0.3766 to 0.3778 | 0.000 |

A surface that followed the notch would read -1 at its centre; all five read 0, the edge the convex hull of the rows
implies, and the rows around the notch lie below the surface by the same mean slack to within 0.002 in every model:
no model gains on the rim, none puts a rim row above. The class cannot represent the notch; the readout's figure shows
the removed rows, hollow, inside the ball.

## 5. The extension point, designed not built (G4)

What the estimator needs in order to admit a feature map and a convex parameter set without reimplementation, read
from `estimator.py` and `solvers.py`:

- **One new object, the surface.** `phi(U)` returning `log V` (homogeneous: `phi(U + s 1) = phi(U) + s`), and
  `fit(U, tau) -> parameters`. The posynomial of today is the surface whose parameters are `(W, log_offset_)` and
  whose `phi` is the existing `_phi(U @ W.T - b)`. The chart's inverse is already closed form for any homogeneous
  `phi` (`_inverse`: `u = base + (log V - phi(base)) 1`), so `_chart`, `_inverse`, `score_samples`, `transform`
  and `inverse_transform` change only in the one line that calls `phi`.
- **One new parameter, a string of immutable default** (`form="posynomial"`, then `"log_quadratic"`), validated in
  `fit` as sklearn conformance asks; `n_terms` and `term_temperature` keep meaning for the posynomial form and are
  rejected (or ignored with a stated rule) for the others. A user-supplied surface object is the later generalization.
- **The convex objective of the programs in this spike** is the mean-slack criterion
  `LME_tau(f(u_i)) - mean f(u_i)` over `(w, S)` with `S = B'QB` positive semidefinite, optionally with `w + Qu_i >= 0`
  at the rows (the monotone form, LQm); at `tau = inf` the exact maximum, a linear and semidefinite program. This is
  `models.py` of the spike (`QuadModel`, about 70 lines of cvxpy); the existing `solve_lp` and `solve_slsqp` stay for
  the monomial.
- **Where the consumers read the posynomial's parameters:** `exponents_` and `log_offset_` are read in
  `estimator.py` (15 places), `preconditioning.py`, `plotting.py` (5) and `tensions.py` (4). The elasticity of a
  log-quadratic surface is the row-dependent gradient `w + Q u`, not a constant `w`: `improvement_factors`, the
  tensions and the contending-set reading need that generalization, and are the larger part of the build, not the
  estimator. The termination certificate (`Termination`) is the posynomial's; the log-quadratic program's status is the
  solver's.
- **Solver route.** cvxpy with Clarabel (exponential and semidefinite cones; used here), SCS as fallback (eleven times
  slower on these programs and less accurate). Scipy's constrained solvers (SLSQP with `S = L L'`) would make the
  program non-convex in `L` and lose Fact 1. Clarabel reported `optimal_inaccurate` with the objective unchanged to
  six digits under tighter settings (amendment 1); the build stage should record the status as the spike does.
- **Lock needs** (in this environment, `uv run --with cvxpy`): cvxpy 1.9.3 and, new to the lock, clarabel 0.11.1, scs
  3.3.1, osqp 1.1.3, qdldl 0.1.9.post1, highspy 1.16.0, sparsediffpy 0.6.1; numpy and scipy are already locked. As an
  optional extra (`[project.optional-dependencies]`), so the core install stays numpy, scipy and scikit-learn.
- **The exact maximum as an LP or an SDP:** the monomial at `tau = inf` is the existing LP; the log-quadratic term is an
  SDP (`cp.max` of an affine-in-`(w, S)` expression with a PSD variable).

## 6. The documentation's Examples section, outlined (G5)

One new Examples section, built from this spike's runs for the build stage (each figure to go through the figure
review; each number to be generated, not typed):

1. **The bend in the plane.** The one-term line against the cubesat table, the level against the plane's first metric
   (`figures/plane_primary.png` is the draft): where the cloud arches under the line, with the held-out slack of the
   one-term fit (0.140 primary).
2. **More terms against a kernel.** Held-out slack and fraction above for K1, K2, K3, the log-quadratic term and its
   monotone form on the same folds (the tables of section 2), the non-monotonicity of the unconstrained term stated
   with its number, and the solve times. The reading rule of the protocol in two sentences.
3. **The boundary case.** The dent (`figures/dent.png`): the notch, the three fits passing over it, the notch level
   at 0 for all of them; with the planted three-term and log-quadratic edges as the two tables each model does and
   does not recover (section 3's matrix).

## 7. Plain options for the build stage, and for the paper's word

For the build stage (the supervisor chooses; none is marked):

- A. Build the surface object and the log-quadratic form (monotone form, with its constraint) as an optional extra of
  the estimator, with the consumers (elasticity, improvement factors, tensions) generalized to a row-dependent gradient.
- B. Build the surface object with the log-quadratic form, and leave the consumers to read the posynomial form only
  (the log-quadratic surface scores and charts; tension reading stays posynomial).
- C. First run the capacity-matched control (K = 4 to 7 on the same folds) to learn whether a kernel beats many terms,
  then decide A or B.
- D. Build nothing in 0.1: write the Examples section and the extension-point design into the documentation as the
  future-direction page, with the numbers above.

For the word in the paper's three sentences on alternatives (the abstract's kernel sentence, Section 10's "The kernel
direction", Section 12's "kernels that keep the model a generalized geometric program (GGP) in the metrics"):

- W1. Keep "GGP" (the sentence is true and narrower: posynomial kernels are GGP; the log-quadratic one is not).
- W2. Change "GGP" to "log-convex" (as assumption (vi) says "log-convex envelope"): the class the spike defines and
  tests.
- W3. Say "kernels that keep the model convex in the log-metrics", with no class name.

## 8. Not done, and what the reader needs to rerun

- The reviewer's rerun of `run.py` and the figure review of `figures/*.png` (as rendered, in a browser or as images)
  are the next step; the spike's two figures are drafts.
- Capacity-matched control (option C) and a second case beyond the cubesat's two regimes (a public table, WP44's
  Broadbalk or others, with licence and source named by that package) are not run.
- Single case, two regimes of one model; the verdict is for that table.
- Solve times were measured with other jobs on the machine; they show orders of magnitude, not precise ratios.
