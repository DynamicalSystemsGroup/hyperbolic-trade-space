# WP35 stage 1b readout: does HoroPCA do what this work does? A falsifiable hypothesis, a designed experiment, results, interpretation

Written for the assistant; the options at the end are the supervisor's, through the assistant. The earlier readout
(`../spike/readout.md`, "the first spike") is the starting point; this one answers the supervisor's amendment of
2026-11-12 (`WP35-decisions.md`, entry 13165e8): a hypothesis an experiment can refute, the experiment, the
results, the interpretation, and a part on how the formalism and solvers differ.

**Head.** The hypothesis and its refutation conditions were committed with the experiment's scripts at
`830cf54` (pushed to `dev`) before any table was generated or any method run on one; the outputs
(`results.json`, `summary.txt`, `results_methods.json.gz`) are committed after it. **Every pre-registered part
survived**: no refuting result was observed (section 3). On tables where the edge is present and the spread is
set apart from it by construction, this work recovered the planted vector in every one of the 54 tables of
arms A and B (absolute cosine at least 0.9995, exponent error, the sum of absolute differences, at most 0.041); PCA's first component and HoroPCA's first direction (R = 0.25 and R = 1) recovered it in
every cell where it is the direction of largest spread and in no cell where another direction is larger (the tied cell aside); and on tables with no
edge this work did not recover it while PCA did where the vector was the direction of largest spread. The methods
estimate different things, which is the complementarity the supervisor asks for. The limits of that reading are in
section 7.

## 1. The hypothesis and the refutation conditions, verbatim as committed at `830cf54`

Quoted from `hypothesis.md` at `830cf54` (the terms, the hypothesis with its parts, the decision rule), with the headings one level down; the experiment's design text of that file is summarised in section 2 and stands in the file.

> ### Terms used below (one plain line each)
> 
> - **Edge.** A planted vector w with positive entries summing to one, and a bound: every row of the table satisfies
>   w . log m <= beta, and a fraction of the rows (here 30 percent) lies exactly on the plane w . log m = beta.
>   This is what the method estimates, and w is its exponent vector.
> - **Spread.** Variance of the log-metrics along a direction (what PCA ranks and HoroPCA's objective is a
>   curved-space version of).
> - **Spread ratio rho.** For a table built by construction A below: the standard deviation of the log-metrics along
>   w (unit-length) divided by their standard deviation along the largest-spread direction orthogonal to w. By
>   construction rho > 1 puts w as the direction of largest spread, rho < 1 puts a different direction first.
> - **Recovered.** A method recovers w on a table when the absolute cosine between the method's direction and w is at
>   least 0.9 (angle at most 25.8 degrees). For this work the direction is the fitted exponent vector; for PCA it is
>   the first principal component; for HoroPCA it is the best-loss restart's first ideal point (k = 1). The threshold
>   is fixed here, before the run; the chance rate for it (a uniformly random direction in R^4, a random point of the
>   simplex for this work) is computed and printed by `experiment_summary.py`, and both are reported next to the results.
> - **Recovery rate.** Recovered tables divided by tables in a cell (a cell = one arm at one setting).
> 
> ### The hypothesis
> 
> **H (one sentence).** This work estimates the edge and PCA and HoroPCA estimate the spread, so a table in which the
> edge and the spread are decoupled by construction separates them: this work recovers w whenever the edge is present,
> whatever the spread; PCA and HoroPCA recover w only when w is also the direction of largest spread; and on a table
> without an edge this work does not recover w, while PCA still does wherever w is the direction of largest spread.
> 
> The hypothesis is split into parts, each with the result that refutes it.
> 
> **H1 (this work follows the edge).** On every table that has the edge present (arms A and B below), this work
> recovers w in a share of at least 0.9 of the tables of every cell, at every spread ratio.
> *Refuted by:* any cell of arm A or arm B in which this work's recovery rate is below 0.9.
> 
> **H2 (PCA and HoroPCA follow the spread).** In arm A, PCA's first component recovers w when rho >= 2 (rate at least
> 0.9) and does not when rho <= 0.5 (rate at most 0.1). The same for HoroPCA k = 1 at R = 0.25 and R = 1 (its
> embedding scales that make it a nearly flat patch or a moderately curved cloud). No prediction is made for HoroPCA at
> R = 3, where the earlier spike saw restart-to-restart differences; it is reported, not tested.
> *Refuted by:* (a) PCA's or HoroPCA's recovery rate at rho <= 0.5 above 0.1; or (b) their rate at rho >= 2 below 0.9.
> Either means the first direction of these methods does not simply follow the spread, or that it follows the edge.
> 
> **H3 (the earlier agreement was the generator's, and the edge is what this work reads).** In arm B (the package's
> own generator, which puts all depth along the all-ones direction, with w moved away from the uniform vector by
> t in {0, 0.3, 0.6, 0.9}), PCA's first component has a recovery rate of at most 0.2 at t = 0.9 (the cosine of w with
> the all-ones direction is then 0.54), while this work's rate stays at least 0.9.
> *Refuted by:* PCA's rate at t = 0.9 above 0.2.
> 
> **H4 (without an edge this work does not find w).** In arm C (a Gaussian cloud with the same spread ratio as arm A at
> rho = 2 and rho = 0.5, and no edge: the position along w is symmetric, not capped), this work's recovery rate is at
> most 0.2 in both cells, and at rho = 2 PCA's first component recovers w at a rate of at least 0.9.
> *Refuted by:* this work's rate above 0.2 in either cell; or PCA's rate at rho = 2 below 0.9.
> 
> **Part not in H.** The smallest-variance component of PCA is orthogonal to the directions of largest spread; on a
> thin slab, where w carries the least spread, it will be w. That is reported (a column) because it is the
> strongest case for PCA; it is excluded from H2 because the analyst cannot select that component without already
> knowing w.
> 
> ### The decision rule
> 
> The hypothesis **survives** if no refuting result above is observed; it is **refuted** if any is, and the readout
> says which part. A part that fails does not rescue the others: each is reported with its cell rates and counts.
> No threshold, cell or seed is changed after the first output is seen. Anything run beyond what is listed here is
> labelled exploratory in the readout.

## 2. The experiment as run

Scripts: `experiment_tables.py` (repository environment: generates the tables, fits this work),
`experiment_methods.py` (the first spike's environment: PCA and the authors' HoroPCA, every restart recorded),
`experiment_summary.py` (the tables below, with the chance rates). Outputs: `results.json` (cells),
`summary.txt` (the printed tables), `results_methods.json.gz` (per table, per restart). 70 tables (arm A 30, arm B 24,
arm C 12, arm D 4), 3 embedding scales, k = 1 and 2, 5 restarts: 2,100 HoroPCA fits, about 17 minutes on 9 cores.

What happened that is not in the hypothesis file:

- The first run of `experiment_tables.py` stopped at arm D: the spread diagnostic used the dimension 4 where one
  earlier table has 3 metrics. The one line was corrected (`len(w)` for `D`), and the script was run again from the
  top; arms A to C came out identical, because every table is generated from its seed. No threshold, cell or seed
  changed. The corrected script is the committed one.
- The empirical spread ratio of each cell is stored with each table (`results.json`, `spread_ratio_empirical_median`):
  A: 3.74, 1.87, 0.94, 0.47, 0.23 for the intended rho = 4, 2, 1, 0.5, 0.25; C: 1.98 and 0.50 for 2 and 0.5. The
  construction does what it says. At rho = 1 the two directions tie (0.94), so which comes first is arbitrary;
  the cell is reported, and no hypothesis statement touches it.
- "Share of the planted vector recovered" is measured as the length of the projection of the unit vector w onto
  the span of the first two components (1 means w lies in that plane; 0 means it is perpendicular). It is a length,
  not a squared share.
- The numbers are counts of tables (or restarts) that reach |cos| at least 0.9 (the threshold fixed in section 1).
  Chance for that threshold: a uniformly random direction in R^4 reaches it with probability 0.037; a random point
  of the simplex, compared with a random planted point of the simplex, 0.152 (400,000 draws,
  `experiment_summary.py`).

## 3. Results

Abbreviations: "rec" = recovered (|cos| at least 0.9); counts are tables out of 6 (arm A, B, C) with 5
restarts each for HoroPCA. "HoroPCA" is the best-loss restart's first ideal point (k = 1). "PCA last PC" is the
smallest-variance component, the part of the hypothesis that is excluded from H2.

### 3a. Arm A: the edge is the same in every row; only the spread changes (H1, H2)

| rho (empirical) | this work rec (median cos, median L1) | PCA PC1 rec (median cos) | HoroPCA k=1 rec at R = 0.25 / 1 / 3 | restarts that rec of 30, same R | PCA last PC rec |
|---|---|---|---|---|---|
| 4 (3.74) | 6/6 (1.000, 0.025) | 6/6 (1.000) | 6/6, 6/6, 6/6 | 30, 30, 30 | 0/6 |
| 2 (1.87) | 6/6 (1.000, 0.025) | 6/6 (1.000) | 6/6, 6/6, 6/6 | 30, 30, 30 | 0/6 |
| 1 (0.94, a tie) | 6/6 (1.000, 0.024) | 1/6 (0.184) | 0/6, 0/6, 0/6 | 3, 4, 1 | 0/6 |
| 0.5 (0.47) | 6/6 (1.000, 0.021) | 0/6 (0.015) | 0/6, 0/6, 0/6 | 0, 0, 0 | 0/6 |
| 0.25 (0.23) | 6/6 (1.000, 0.017) | 0/6 (0.006) | 0/6, 0/6, 0/6 | 0, 0, 0 | 5/6 |

### 3b. Arm B: the package's generator, the planted vector moved away from the all-ones direction (H1, H3)

t is the distance from the uniform vector toward a vertex; cos(w, all-ones) is 1, 0.89, 0.69, 0.54.

| t | this work rec (median cos, median L1) | PCA PC1 rec (median cos) | HoroPCA k=1 rec at R = 0.25 / 1 / 3 | restarts rec of 30 | PCA last PC rec |
|---|---|---|---|---|---|
| 0 | 6/6 (1.000, 0.006) | 6/6 (0.995) | 6/6, 6/6, 5/6 | 30, 30, 25 | 0/6 |
| 0.3 | 6/6 (1.000, 0.006) | 0/6 (0.809) | 0/6, 0/6, 0/6 | 0, 0, 0 | 0/6 |
| 0.6 | 6/6 (1.000, 0.006) | 0/6 (0.486) | 0/6, 0/6, 0/6 | 0, 0, 0 | 0/6 |
| 0.9 | 6/6 (1.000, 0.006) | 0/6 (0.278) | 0/6, 0/6, 0/6 | 0, 0, 0 | 5/6 |

### 3c. Arm C: no edge, a symmetric cloud with the same spread as arm A (H4)

| rho | this work rec (median cos [min, max]) | PCA PC1 rec (median cos) | HoroPCA k=1 rec at R = 0.25 / 1 / 3 | restarts rec of 30 |
|---|---|---|---|---|
| 2 | 0/6 (0.318 [0.180, 0.370]) | 6/6 (1.000) | 6/6, 6/6, 6/6 | 30, 30, 26 |
| 0.5 | 0/6 (0.577 [0.306, 0.820]) | 0/6 (0.013) | 0/6, 0/6, 0/6 | 0, 0, 0 |

### 3d. The share of the vector in the plane of two components (k = 2), arm A

Number of tables (of 6) whose span alignment is at least 0.9. HoroPCA k = 2 is the best-loss restart.

| rho | PCA, first two PCs | HoroPCA k = 2 at R = 0.25 / 1 / 3 | restarts rec of 30, same R |
|---|---|---|---|
| 4, 2, 1 | 6/6 | 6/6, 6/6, 6/6 | 30, 30, 30 |
| 0.5 | 6/6 | 6/6, 6/6, 4/6 | 30, 30, 22 |
| 0.25 | 0/6 | 0/6, 0/6, 0/6 | 0, 1, 0 |

This is the design showing: at rho = 0.5 the planted direction is the second-largest spread (0.5 against 1 for the
nuisance and 0.3 for the others), so a plane of two components contains it; at rho = 0.25 it is the smallest, so no
plane of the first two does.

### 3e. Arm D: the first spike's four planted tables, refit, every restart recorded

Cosine of the best-loss HoroPCA k = 1 direction at R = 0.25 / 1 / 3 (the restart range at R = 3 in brackets), PCA's first
component, and this work's matched fitted term. "Spread ratio" is the standard deviation along term 1 over the
standard deviation along the largest orthogonal direction (computed for term 1 only).

| Table, term | spread ratio | this work | PCA PC1 | HoroPCA k=1 |
|---|---|---|---|---|
| K=1, seed 0 | 1.77 | 1.000 | 0.985 | 0.99 / 0.97 / 0.90 [0.90, 0.96] |
| K=2, seed 7, term 1 | 0.82 | 1.000 | 0.586 | 0.55 / 0.48 / 0.41 [0.41, 0.55] |
| term 2 | n/a | 1.000 | 0.653 | 0.62 / 0.55 / 0.48 [0.48, 0.60] |
| K=3, seed 0, term 1 | 1.82 | 1.000 | 0.992 | 0.99 / 0.99 / 0.98 [0.97, 0.98] |
| term 2 | n/a | 1.000 | 0.827 | 0.82 / 0.82 / 0.78 [0.68, 0.78] |
| term 3 | n/a | 1.000 | 0.778 | 0.77 / 0.74 / 0.69 [0.69, 0.82] |
| K=3, seed 4, term 1 | 1.19 | 1.000 | 0.789 | 0.78 / 0.74 / 0.68 [0.68, 0.77] |
| term 2 | n/a | 1.000 | 0.495 | 0.48 / 0.42 / 0.35 [0.35, 0.55] |
| term 3 | n/a | 1.000 | 0.644 | 0.63 / 0.59 / 0.54 [0.54, 0.72] |

These agree with the first spike's numbers to the second decimal (the same seeds, restarts 0 to 4). The
restart ranges are new: at R = 0.25 the five restarts of a table differ by at most 0.07 in cosine, at R = 3 by up to 0.20
(K=1, 0.90 to 0.96; K=3 seed 4 term 2, 0.35 to 0.55). In arm C at rho = 2 and R = 3, four of 30
restarts fell below 0.9 (smallest 0.41), where the other 26 reached 0.9 or more. At R = 3 the Busemann (k = 1)
objective is not unique across restarts; at R = 0.25 it is.

### 3f. The verdict, by part

| Part | Refuting result | Observed | Verdict |
|---|---|---|---|
| H1 | any cell of arm A or B with this work's rate below 0.9 | 9 cells, each 6/6 (and the 4 tables of arm D, 9 terms, each matched at cosine 1.000) | survives |
| H2 (a) | PCA PC1 or HoroPCA k=1 (R = 0.25, 1) above 0.1 at rho <= 0.5 | PCA 0/6, 0/6; HoroPCA 0/6 in both cells at both scales | survives |
| H2 (b) | their rate below 0.9 at rho >= 2 | PCA 6/6, 6/6; HoroPCA 6/6 at R = 0.25 and R = 1 in both cells | survives |
| H3 | PCA PC1 above 0.2 at t = 0.9 | 0/6; this work 6/6 | survives |
| H4 | this work above 0.2 in either arm C cell, or PCA below 0.9 at rho = 2 | this work 0/6 and 0/6; PCA 6/6 | survives |
| exploratory, HoroPCA R = 3, not tested | none attached | k=1 rec 6/6 at rho >= 2 (arm A), 5/6 in arm B at t = 0 | reported |
| part not in H, thin slab | none attached | PCA's smallest-variance component recovers w in 5/6 at rho = 0.25 and 5/6 at t = 0.9, and in none of the other nine cells (arms A, B and C) | reported |

## 4. What the results say

1. *This work reads the edge.* Its fitted exponents lie within 0.041 in summed absolute error (median 0.006 to 0.025 by cell) of the planted vector in
   every table with an edge, whether w is the direction of largest spread (rho = 4), the smallest (rho = 0.25), or the
   package's depth axis is perpendicular to it (arm B, t = 0.9). It does not do so when the edge is removed and the same
   spread kept (arm C): the fitted vector there has no relation to w (median cosine 0.32 and 0.58; no table reaches 0.9). The planted vector and the spread of the
   rows were separated, and the fit followed the edge.
2. *PCA and HoroPCA's first direction read the spread.* They recover w only where w is the leading axis of spread
   (rho >= 2 in A and C; t = 0 in B) and not where it is not (rho <= 0.5; t >= 0.3). Arm C is the clearest case: in the
   cloud with no edge at all, PCA and HoroPCA recover w exactly at rho = 2, because the cloud is long in that
   direction, while this work finds nothing there. In arm B, the package's own generator, the first spike's agreement
   was about the generator: depth lies along the all-ones vector, and the default planted vectors are near it
   (cos 0.99). Moving w away (t = 0.3: cos 0.89) makes PCA's first component miss it (median cosine 0.81, 0 of 6) with the
   edge unchanged.
3. *The earlier statement is now tested.* "Recovered only where the generator made them the direction of largest
   spread" was a causal claim about one set of tables; arm A varies exactly that factor, one at a time, with the
   edge fixed, and the recovery switches at rho of about 1, as the factor does (3a). The claim is now supported for
   PCA and for HoroPCA at R = 0.25 and R = 1, and stays an observation for R = 3.
4. *The plane of two components is not a rescue.* At rho = 0.5 the plane of the first two PCs or HoroPCA components
   contains w (6/6) because w is the second-largest spread; at rho = 0.25 it does not (0/6). Whether w lies in the
   plane depends on where it ranks in the spread, not on whether an edge is present (arm C at rho = 0.5: also 6/6).
5. *The smallest-variance component is the strong case for PCA, and it depends on the shape of the table.* On a
   thin slab (rho = 0.25 and arm B at t = 0.9) the last PC recovers w in 5 of 6 tables. The analyst cannot pick that
   component without knowing w; and in the other nine cells (arms A, B and C) the last PC does not recover it. It is a coincidence of the slab: w is the thinnest direction when
   the edge is the only narrow feature of the cloud.
6. *HoroPCA at R = 0.25 and R = 1 behaves like PCA here; at R = 3 it differs in a way that is not the edge.* At R = 0.25 and
   R = 1 its recovery counts equal PCA's in every cell of 3a to 3c except the tied cell (rho = 1).
   At R = 3 the restarts disagree (arm C, 26 of 30; arm B t = 0, 25 of 30; arm A rho = 1, an arbitrary choice
   between two tied axes).

## 5. How the formalism and the solvers differ

Plain statements, each with its source. Code locations are in the authors' clone at commit
`c9a99967a62688711f6b63dab3baee53fe2d8430` (github.com/HazyResearch/HoroPCA; no licence file; nothing of it is vendored;
PyTorch 2.15.0 here, 1.8.1 in their `requirements.txt`; one call shimmed from outside, `torch.solve`, `compat.py` of the
first spike) and in this repository's `src/`.

| | HoroPCA | This work |
|---|---|---|
| What is estimated | k directions (a frame) in negative-curvature space that maximize the variance of the points projected onto them | exponent vectors (one per term) on a simplex that make a soft maximum of the weighted log-metrics as small as possible, i.e. the one-sided edge |
| The data enter through | all rows, symmetrically: pairwise hyperbolic distances (k > 1, `learning/pca.py` `HoroPCA.compute_variance`, L274-285) or the variance of Busemann values (k = 1, `compute_loss`, L287-306); a row's depth below an edge is not special | a soft maximum over rows, which is dominated by the rows nearest the edge; `solvers.py` `log_mean_exp` (L111), `objective_and_grad` (L184) |
| Criterion | variance, a two-sided quantity, maximized (the loss is its negative, L287) | log-mean-exp, a one-sided quantity, minimized |
| Parameter space | unit vectors on the sphere, orthonormalized by Gram-Schmidt at every step (`pca.py` `gram_schmidt`, L59-76; `keep_orthogonal=True`, L249-254); a Stiefel-type manifold, not convex | the simplex (non-negative, summing to one); convex |
| Convexity | the objective is not convex in the frame; the repository gives no argument that it is | `J_tau` is convex on the simplex: the second directional derivative is `tau` times a weighted variance, at least zero, checked in `derivation/lemma_04_convexity.py` (a plain-SymPy pencil-and-paper check, not a formal verification) |
| Solver | Adam (`torch.optim.Adam`, `pca.py` L123), a fixed 500 steps at learning rate 0.05 (the authors' command line sets both: `main.py` L34 and L109; the class default is `max_steps=100`), gradient clipping at 1e5 (L132), no convergence test | `tau = inf`: a linear program (`solvers.py` `solve_lp`, `scipy.optimize.linprog`, L214-262); finite `tau`: SLSQP with an analytic Jacobian (`solve_slsqp`, L285), warm-started from the linear program; K > 1: assign rows to terms, refit each term (`_solve_terms_once` L1239, `_refit` L1217) |
| Starting point and repeats | random normal components (`torch.randn`, `pca.py` L23); restarts are the caller's choice (`--n-runs`, `main.py` L37, default 5); different restarts end in different optima (section 3e) | the linear program's vertex, deterministic; K > 1 uses the seeded `random_state` for the initial assignment |
| Certificate | none: the final loss is not accompanied by a bound on its distance from the best | a first-order gap at the returned point: `simplex_gap` (`solvers.py` L368) gives `0 <= f(w) - f* <= G` by convexity; `term_gap` (L428) per term and `soft_certificate` (L1029) for the K-term form; a termination record in the fitted object |
| Closed form | none for HoroPCA: `fit_spectral` raises `NotImplementedError` in the base class (L150-156) and `HoroPCA` does not override it; the paper's conclusion lists a closed form as future work (arXiv 2106.03306) | the linear program at `tau = inf`; none at finite `tau` (SLSQP) |
| Where the local method enters | the frame (nonconvex), through the restarts | only the K-term assignment: each refit is solved globally, the assignment is a local method |
| Interface | `torch.nn.Module` with `fit(x, iterative, optim)`; no `get_params`, `set_params`, `check_is_fitted`, `inverse_transform` or `score_samples`; projection loses d - k coordinates | scikit-learn transformer of the decomposition family (`fit`, `transform`, `inverse_transform`, `score_samples`; `parametrize_with_checks`); the chart is reversible |
| Data prerequisite | points in the Poincare ball with Frechet mean at the origin (the script centres them by gradient iteration, `learning/frechet.py` L8, called at `main.py` L97) | strictly positive larger-is-better metrics (conditioning is the analyst's step) |

The formalism differs because the question does. HoroPCA's question is: in which directions does a cloud in curved
space spread, with curved-space projections that keep Busemann coordinates (the paper's Section 3, three
generalizations: the subspace, the projection, the variance). This work's question is: which products of powers of the
metrics bound the table from above, and how tightly. The first has the data as a cloud; the second has it as a region
whose boundary is wanted.

## 6. Answers to the readers' criticisms of the earlier Appendix G passage

**Definitions, one plain line each.**

- *PC (principal component).* A direction in the table's space (here log-metric space) ranked by how much the table
  spreads along it: PC1 spreads most, the last spreads least.
- *Absolute cosine, |cos|.* How well two directions agree, ignoring sign (a component's sign is arbitrary): 1 when
  they lie along the same line, 0 when perpendicular; 0.9 is an angle of 25.8 degrees.
- *Recovered.* |cos| of the method's direction with the planted vector at least 0.9, fixed before the run (section 1);
  chance for a random direction in R^4 is 0.037, and 0.152 for the fitted exponents of this work.
- *Alignment of the first two (span alignment).* The length of the projection of the unit planted vector onto the plane
  of the first two components: 1 when it lies in that plane, 0 when perpendicular.
- *R (scale of the embedding).* The tangent-space radius of the farthest point after the table is centred and scaled to
  fit the Poincare ball (curvature -1); the point then sits at hyperbolic distance 2R from the origin. R = 0.25 is a
  nearly flat patch; R = 3 pushes the farthest points toward the boundary, where the geometry is far from flat. The
  table is ours; the scale is our choice, and three values are shown.
- *Distortion.* The authors' measure of an embedding: the mean over pairs of nodes of |embedded distance - graph
  distance| divided by the graph distance (`utils/metrics.py` `avg_distortion_measures`, L9-24); 0 means all distances
  kept, smaller is better.
- *Frame.* The k orthonormal directions HoroPCA optimizes at once (for k = 2, a pair); "variance over frames" is its
  objective as a function of the frame.
- *Horosphere.* In hyperbolic space, the curved surface that stands where a hyperplane perpendicular to a direction
  would in flat space: a limit of spheres growing toward one point at infinity (an ideal point); the Busemann function
  gives a point's position relative to it, and a horospherical projection slides a point along its horosphere onto the
  chosen subspace.

**The earlier numbers kept or dropped, with source and command.**

- *Distortion 0.20 against 0.84 on the authors' small tree.* Kept as the check that the code is theirs. Source:
  `docs/superpowers/notes/spike-horopca/smalltree_run.txt`; command, from inside the clone:
  `python <spike-horopca>/run_main.py <clone> --dataset smalltree --model horopca --dim 10 --n-components 2 --n-runs 3`
  (and `--model pca` for 0.84). The README of the authors reports 0.19 for HoroPCA. It is a measure on a graph; it is not
  a measure on our tables and is not used as one.
- *The loadings -0.41 and +0.40 on the cubesat primary table.* Source: `analysis.txt` lines 176-181 (total mass -0.409,
  available power +0.402, PC1); command `python analyze.py tables.npz results.json` of the first spike. Not carried
  into Appendix H: sign patterns of a loading say how the sample spreads, and the arm A to C results make that point with
  the planted vector known, without a table of real metrics whose "truth" is our own fit.
- *0.068 against 0.325 at R = 3.* Source: `analysis.txt` (cubesat primary; HoroPCA k = 1 explained 0.068, PCA PC1 0.325).
  The two numbers are not like for like: HoroPCA's "explained" is the ratio of mean squared pairwise hyperbolic
  distances of the projected points to those of the data; PCA's is a variance share; the two coincide only in the flat
  limit. Dropped from Appendix H as a comparison; the restart spread of section 3e carries the R = 3 point instead.
- *Authors' code.* Commit `c9a99967a62688711f6b63dab3baee53fe2d8430`; PyTorch 2.15.0; numpy 2.5.4, scipy 1.18.1, networkx
  3.7, Python 3.12; the single shim above.
- *"This work K = 1 / 2 term" on the cubesat rows.* The target there is this work's own fitted exponent vector for the
  cubesat table (tau chosen by the fraction-above criterion; 41.7 and 113.2 for K = 1, 2 in the primary regime). It is an
  estimate by the method being compared, not a ground truth: no planted vector exists for the cubesat. The rows show
  that PCA's and HoroPCA's directions are far from what this work estimates (span alignment 0.02 to 0.39); they
  cannot show which is right. Arms A to D, where the vector is planted, are the evidence for the hypothesis; the
  cubesat rows are context.

## 7. Reading limits

- The embedding is ours. Log-metrics are Euclidean coordinates; putting them in a Poincare ball needs a centre, a
  scale R and a map, all chosen by us (three scales; centre at the mean; exponential map at the origin). A different
  embedding (another base point, per-coordinate scaling) could change HoroPCA's directions; it would not change PCA's.
  What a second embedding would add: whether HoroPCA's R = 3 behaviour is a property of that embedding or of the
  method. Not run.
- The tables are not tree-like (Gromov four-point relative delta 0.26 to 0.33 planted, 0.45 to 0.46 cubesat, against
  0.00 for the authors' tree; `gromov.txt`). HoroPCA's published results are for tree-like data; nothing here tests it
  there, and nothing here says it is worse there.
- A construction of our making: one nuisance direction with standard deviation 1, two more at 0.3; noise-free tables;
  30 percent of rows on the edge; d = 4, n = 300; this work's temperature fixed at 50. That is a favourable setting for
  this work, and a clean one for the logic. Noisy edges, fewer edge rows, more metrics and an unknown temperature are
  not tested.
- Six tables per cell. A rate of 6/6 observed is consistent with a true rate as low as 0.61 at one-sided 95 percent;
  the refutation rules in section 1 were written on observed rates, and the verdicts above are on that rule. The
  spread is large between cells (0 or 6 of 6), not within them, and every cell's rate sits at an end.
- k at most 2, HoroPCA's default hyperparameters, five restarts. A tuned HoroPCA, more restarts or a different optimizer
  could change the R = 3 rows, not the structure of the argument (the objective ranks spread).
- Targets are directions in log-metric space. A principal component and an edge normal are compared as vectors in the
  same space, which is what "recovered" means here; a PCA user would not call an edge normal a component, and the
  comparison is about which vector each method returns.
- The arm-D tables and the cubesat rows are the first spike's; their reading is unchanged.

## 8. Interpretation, and the plain options

**What is established.** Under the pre-registered rule the hypothesis survived. The first direction of PCA and of
HoroPCA (R = 0.25, 1) follows the spread of the rows; this work follows the edge. A table can have the same edge and any
spread, and then they part: so they do different things. That makes them complementary: a PCA of a table says along
which combinations the sampled designs spread; this work says where the table stops. The paper already chains them:
Appendix D.16 runs a principal component analysis on the chart coordinates of the near-frontier designs in a term's
cell (`orient_by_pca`, `tension_report`, `src/hyperbolic_trade_space/gaps.py`, `tensions.py`), which reads the trade-offs
the sampling exercised, "a reading and not a result". A HoroPCA of the chart is the same kind of chain and has not been
run here. What is not established: that HoroPCA is "worse" at anything it was built for, that no embedding of
the log-metrics gives it the edge, or anything about the cubesat beyond context.

**Question 1: how much of this enters Appendix H.**
- (a) The hypothesis, the experiment's design, the arm A, B and C tables (3a to 3d), the verdict table and the
  interpretation; arm D, the first spike's cubesat rows and the loadings stay in the notes folder and the readouts.
- (b) As (a), with arm D's table (3e) as the bridge to the first spike's tables, and one sentence on the cubesat rows
  naming their target as this work's own estimate.
- (c) As (b), and the first spike's loadings and the 0.068 against 0.325 comparison, each with its command and source
  and the like-for-like caveat of section 6.

**Question 2: the second embedding.**
- (a) Run before the appendix is written: one other embedding of the same tables (for example another centre or
  per-metric scaling), the same hypothesis and rule, reported beside the first.
- (b) Not run; the appendix states the embedding as ours, and what a second would add, in the reading limits.

**Question 3: the chain.**
- (a) Appendix H states the chain in words, pointing at D.16.
- (b) A third arm runs HoroPCA (and PCA) on this work's chart of arm A, to show them reading what the chart leaves,
  the spread along the edge; a new experiment with its own hypothesis, run before it is claimed.
- (c) Neither: the pointer to D.16 alone.

**Question 4: the claim about thin slabs.**
- (a) Report the smallest-variance component as the part not in H (as here), with the 5/6 counts at rho = 0.25 and t = 0.9
  and the reason it is not a method (the analyst has to know w).
- (b) Leave it out of Appendix H and keep it in this readout.

**Question 5: the threshold.**
- (a) 0.9 stays, with the chance rate beside it (0.037 and 0.152).
- (b) The tables also print counts at 0.8 and 0.95 (the summary can, from the stored cosines).

## 9. Files and commands

- Pre-registration: `work-packages/WP35-rounds/spike-h/hypothesis.md` with the three scripts, at `830cf54`.
- Run: `uv run python work-packages/WP35-rounds/spike-h/experiment_tables.py <tables.npz> docs/superpowers/notes/spike-horopca/tables.npz`;
  `<spike env>/bin/python work-packages/WP35-rounds/spike-h/experiment_methods.py <clone> docs/superpowers/notes/spike-horopca <tables.npz> <results_methods.json> 9`;
  `uv run python work-packages/WP35-rounds/spike-h/experiment_summary.py <tables.npz> <results_methods.json> results.json > summary.txt`.
- Results: `results.json`, `summary.txt`, `results_methods.json.gz` in this folder. The tables (`tables.npz`, 0.76 MB) are not
  committed; they regenerate from the seeds.
- The environment of the authors' code is the first spike's (`docs/superpowers/notes/spike-horopca/README.md`).
