# Research spike (2026-11-08): the per-facet refit step of the K > 1 alternation

Run for WP9 gap G-1 at the supervisor's request (`work-packages/WP9-decisions.md`). Throwaway: the scripts here are kept for reproducibility only; nothing in the package depends on them.

Supervisor's question (verbatim): "what function did this fulfill and what are some ways to handle
that function which is better fit with our evidence".

Throwaway code and all outputs: this folder (`docs/superpowers/notes/spike-facet-refit/`; spike code, not part of the package and not imported by it).
Nothing in the repository was changed. Every command below is run from the repository root with
`<folder>` = `docs/superpowers/notes/spike-facet-refit`.

## 1. The function of the per-facet step

Inside the alternation (assign rows to K facets, refit each facet, repeat), the per-facet step is a
map from a hard assignment to, for each facet k:

1. a direction `w_k` on the simplex (the facet's n-lemma: which metrics contend, at what exchange
   rates);
2. an offset `beta_k`, the facet's reach, which must stay a *support value* of the data in direction
   `w_k` so that `V = 1` is the frontier, `coefficients_ = exp(-kappa beta_k)` and L11 keep their
   K = 1 meaning;
3. through `argmax_k (w_k . u - beta_k)`, the next assignment.

Evidence available to the step: all N rows (a bounded cloud, whose support is what a facet of an
upper envelope touches); the facet's own rows (a sliver: a cone of the chart that does not contain
the origin); the facet's near-frontier rows (the rows that actually lie on the facet; 2 to 160 in
practice, 2-11 on the failing planted seeds); noise; and the fact that facets can be small. Two
kinds of evidence are in play: *where the facet's rows are* (the region, carried by all its rows,
interior ones included) and *where the frontier of that region is* (carried only by its
near-frontier rows).

## 2. Ways to fulfil the function

| | Direction `w_k` from | `beta_k` | Assumes | Monotone objective |
|---|---|---|---|---|
| A. per-facet min-max (approved default) | `argmin_w J_tau` over the facet's own rows | `J_tau` over own rows (not a support value of the data) | the facet's rows enclose the origin of the chart (false for a sliver) | none that is meaningful |
| B. supporting hyperplane tightest on the facet (built) | `argmin_w J_tau(Uw) - mean_k(u).w` over all rows | `J_tau(Uw_k)` over all rows (support) | the facet's rows, interior included, locate its plane (one-sided per-partition least squares; at tau = inf the LP `min beta - mean_k w.u s.t. w.u_i <= beta`) | yes: mean slack |
| C. responsibility-weighted soft maximum | `argmin_w (1/tau) log sum_i r_ik exp(tau w.u_i)`, `r_ik` soft membership (softmax of facet scores) or hard with floor eps | support over all rows | the weights, not the geometry, decide what the facet supports | no |
| D. tangent plane of the facet's near-frontier rows | smallest-variance direction of the facet's rows within the band of its plane, as a QP on the simplex (`min w^T S w`, a constrained TLS normal); first step and facets with < d+1 near rows fall back to B | support over all rows | the frontier rows of a facet lie on one hyperplane in log space (true of a monomial facet); needs >= d+1 of them | no; converged 14-19 of 20 in practice |
| E. shrinkage: D pulled toward B | `min w^T S w / tr S + (lam0/n_near) ||w - w_B||^2`, lam0 = 1 | support over all rows | D for well-populated facets, B for sparse ones, continuously | no |
| F. no direction refit | fixed candidate directions (4000 Dirichlet samples + the K = 1 fit) each with its support value; a facet takes the candidate that touches (slack < band) most of its rows | support, precomputed | the right directions are in the candidate set (DEA-like scalarization sweep; Charnes, Cooper and Rhodes 1978 for the support-hyperplane view; Magnani and Boyd 2009 for the partition scheme) | yes on a finite set; converged 20 of 20 |

C at tau = inf is undefined (a weighted maximum ignores the weights: with any floor it is the K = 1
LP, with none it is A). D connects to the tension report: the report's principal directions are the
largest-variance directions of the near-frontier rows' chart coordinates Z (in-frontier spread); D's
normal is the complementary smallest-variance direction in u-space, the same PCA read from the other
end.

## 3. Measurements

Settings: `make_frontier_data(400, 4, n_terms=3, random_state=s)`, s = 0..19, tau in {inf, 50};
pass = exponent error (max abs after Hungarian matching) < 0.05 and >= 90 % of frontier rows on the
right facet (the R-1 criterion). "slack" is the common evaluation objective: mean slack with
support offsets `J_tau(Uw_k)` recomputed for every method. Variants: C_hard eps = 0.2; C_soft
kappa = tau, floor 1e-3; E lam0 = 1; F 4000 candidates. Code: `methods.py`.

### 3a. Oracle: each step applied once to the TRUE labels (isolates the step from the dynamics)

`uv run python <folder>/bench_oracle.py` (`oracle.txt`, `oracle.csv`). Facet exponent error
(median / max) by the facet's number of frontier rows; 60 facets per tau.

tau = inf:

| method | <=4 rows (2 facets) | 5-11 (2) | 12-30 (10) | >30 (46) | facets to 0.05 |
|---|---|---|---|---|---|
| A | 0.857 / 0.884 | 0.356 / 0.601 | 0.377 / 0.832 | 0.649 / 0.967 | 0 / 60 |
| B | 0.018 / 0.035 | 0.001 / 0.001 | 0.000 / 0.000 | 0.000 / 0.000 | 60 / 60 |
| D | 0.018 / 0.035 | 0.036 / 0.047 | 0.007 / 0.016 | 0.004 / 0.016 | 60 / 60 |
| E | 0.018 / 0.035 | 0.017 / 0.020 | 0.006 / 0.014 | 0.004 / 0.012 | 60 / 60 |
| F | 0.032 / 0.041 | 0.020 / 0.026 | 0.022 / 0.031 | 0.018 / 0.047 | 60 / 60 |

tau = 50:

| method | <=4 | 5-11 | 12-30 | >30 | facets to 0.05 |
|---|---|---|---|---|---|
| A | 0.866 / 0.902 | 0.349 / 0.587 | 0.377 / 0.830 | 0.632 / 0.957 | 0 / 60 |
| B | 0.037 / 0.049 | 0.023 / 0.031 | 0.007 / 0.011 | 0.004 / 0.010 | 60 / 60 |
| C_hard | 0.075 / 0.077 | 0.062 / 0.076 | 0.151 / 0.252 | 0.289 / 0.587 | 1 / 60 |
| C_soft | 0.113 / 0.183 | 0.036 / 0.041 | 0.071 / 0.160 | 0.124 / 0.366 | 12 / 60 |
| D | 0.037 / 0.049 | 0.038 / 0.047 | 0.007 / 0.014 | 0.002 / 0.007 | 60 / 60 |
| E | 0.037 / 0.049 | 0.026 / 0.030 | 0.006 / 0.013 | 0.002 / 0.007 | 60 / 60 |
| F | 0.034 / 0.041 | 0.020 / 0.026 | 0.021 / 0.045 | 0.018 / 0.047 | 60 / 60 |

Readings. A is ill-posed in principle (0 of 60 with perfect labels; the LP on the true rows of
seed 0 returns `[0.416, 0, 0.119, 0.465]` for planted `[0.212, 0.334, 0.245, 0.209]`). Given the
true partition, B recovers every facet, including those with 2-4 frontier rows, because the facet's
roughly 130 interior rows carry its location. So the per-facet step is not what fails on seeds 1,
3, 8, 16; the alternation does. C has no useful middle: at working temperatures the outside rows'
weights `exp(tau s)` dominate any floor, so C_hard with eps >= 1e-3 is the K = 1 fit repeated K
times (checked at eps = 0, 1e-6, 1e-3, 0.2, 5 on seed 0), and C_soft behaves the same.

### 3b. Planted alternation from one common initialization

`uv run python <folder>/bench_planted.py solver` (the built solver's initialization: K random rows
as centres in the Helmert chart, seed 12345 for every method and data seed; `planted_solver.txt`,
`.csv`) and `uv run python <folder>/bench_planted.py flipped` (planted labels with 20 % random
flips; `planted_flipped.txt`, `.csv`).

Solver initialization, tau = inf:

| method | pass/20 | pass on {1,3,8,16} | median err | mean right | mean slack | converged/20 | mean iters | s/run |
|---|---|---|---|---|---|---|---|---|
| A | 0 | 0 | 0.432 | 0.285 | 0.965 | 10 | 36.2 | 0.085 |
| B | 12 | 0 | 0.000 | 0.920 | 0.694 | 17 | 11.8 | 0.063 |
| D | 16 | 1 | 0.013 | 0.969 | 0.698 | 14 | 18.4 | 0.118 |
| E | 15 | 1 | 0.011 | 0.956 | 0.699 | 15 | 16.4 | 0.102 |
| F | 9 | 0 | 0.060 | 0.890 | 0.738 | 20 | 2.8 | 0.013 |

Solver initialization, tau = 50:

| method | pass/20 | pass on {1,3,8,16} | median err | mean right | mean slack | converged/20 | mean iters | s/run |
|---|---|---|---|---|---|---|---|---|
| A | 0 | 0 | 0.463 | 0.328 | 0.892 | 11 | 31.8 | 0.162 |
| B | 14 | 0 | 0.011 | 0.918 | 0.646 | 20 | 8.1 | 0.089 |
| C_hard | 0 | 0 | 0.260 | 0.067 | 0.842 | 0 | 50 | 0.474 |
| C_soft | 0 | 0 | 0.276 | 0.100 | 0.856 | 0 | 50 | 0.478 |
| D | 16 | 1 | 0.007 | 0.941 | 0.645 | 18 | 10.5 | 0.127 |
| E | 16 | 1 | 0.007 | 0.948 | 0.645 | 20 | 6.8 | 0.081 |
| F | 12 | 1 | 0.045 | 0.851 | 0.663 | 20 | 3.6 | 0.031 |

Failing seeds, solver initialization (exponent error / fraction of frontier rows right):

| seed, tau | min frontier rows | A | B | D | E | F |
|---|---|---|---|---|---|---|
| 1, inf | 3 | 0.818 / 0.06 | 0.113 / 0.98 | 0.195 / 0.96 | 0.170 / 0.98 | 0.122 / 0.97 |
| 3, inf | 6 | 0.976 / 0.48 | 0.200 / 0.52 | 0.111 / 0.89 | 0.230 / 0.91 | 0.195 / 0.95 |
| 8, inf | 11 | 0.234 / 0.09 | 0.108 / 0.91 | **0.014 / 0.99** | **0.013 / 0.99** | 0.194 / 0.83 |
| 16, inf | 2 | 0.315 / 0.02 | 0.402 / 0.97 | 0.281 / 0.98 | 0.279 / 0.98 | 0.295 / 0.98 |
| 1, 50 | 3 | 0.818 / 0.42 | 0.132 / 0.85 | 0.141 / 0.71 | 0.073 / 0.83 | 0.099 / 0.68 |
| 3, 50 | 6 | 0.466 / 0.18 | 0.112 / 0.94 | **0.022 / 0.96** | **0.029 / 0.96** | **0.015 / 0.94** |
| 8, 50 | 11 | 0.804 / 0.40 | 0.210 / 0.52 | 0.224 / 0.83 | 0.236 / 0.84 | 0.194 / 0.82 |
| 16, 50 | 2 | 0.342 / 0.55 | 0.265 / 0.80 | 0.279 / 0.68 | 0.277 / 0.68 | 0.286 / 0.72 |

Flipped-label initialization (20 % flips), pass/20 (in parentheses: pass on the 4 bad seeds):

| method | tau = inf | tau = 50 | converged inf / 50 | median err inf / 50 |
|---|---|---|---|---|
| A | 0 (0) | 0 (0) | 7 / 12 | 0.592 / 0.315 |
| B | 19 (3) | 17 (1) | 19 / 20 | 0.000 / 0.010 |
| C_hard | undefined | 0 (0) | - / 0 | - / 0.270 |
| C_soft | undefined | 0 (0) | - / 0 | - / 0.281 |
| D | 18 (2) | 18 (2) | 15 / 19 | 0.010 / 0.007 |
| E | 19 (3) | 19 (3) | 18 / 20 | 0.007 / 0.007 |
| F | 14 (0) | 17 (1) | 20 / 20 | 0.033 / 0.033 |

Seed 16 (a facet with 2 frontier rows) fails for every method from the flipped start at tau = inf
(error 0.437 for B, D and E alike).

### 3c. Five restarts (the built solver's seeds), best common slack kept

`uv run python <folder>/bench_restarts.py` (`restarts.txt`, `restarts.csv`).

| method | tau = inf pass/20 | fail seeds | tau = 50 pass/20 | fail seeds |
|---|---|---|---|---|
| B | 16 | 1, 3, 8, 16 | 16 | 1, 3, 8, 16 |
| D | 17 | 1, 3, 16 | 17 | 1, 3, 16 |
| E | 17 | 1, 3, 16 | 17 | 1, 3, 16 |
| F | 14 | 1, 3, 4, 8, 11, 16 | 15 | 1, 3, 8, 14, 16 |

(The review's 17/20 for the built B at tau = inf differs on seed 8; this spike's loop has no
monotone guard and selects restarts by the recomputed common slack, so the runs are not
bit-identical.)

**The planted solution is not the mean-slack optimum on the failing seeds.** At tau = inf, the
mean slack of the planted (W, support beta) versus B's found solution: seed 1: 0.6554 vs 0.6510;
seed 3: 0.7333 vs 0.7310; seed 8: 0.6757 vs 0.6745; seed 16: 0.6638 vs 0.6636; on the other 16 seeds
the planted solution has the lower slack. So on those seeds a method that minimizes mean slack
*should* return the found partition: splitting a well-populated facet in two buys more slack than
fitting a facet that only 2-11 frontier rows exercise. D and E recover seed 8 precisely because
they do not minimize mean slack; they follow the frontier rows. (At tau = 50 the planted exponents
are not the finite-tau optimum anyway, so the comparison is uninformative there.)

### 3d. Cubesat primary table, K = 3, seeds 0..4

`uv run python <folder>/bench_cubesat.py` (`cubesat.txt`, `cubesat.csv`). N = 706 feasible rows,
d = 10, tau = 38.10 (K = 1, target 0.10), band 0.0262. Initialization: the solver's, seed s, shared
by all methods. "Sets" = metrics with exponent > 0.05 per facet (the tension report's LP contending
set is not recomputed here). "dev" = max abs exponent difference from the seed-0 fit after facet
matching.

| method | slack mean (sd) | converged/5 | mean iters | s/run | distinct set signatures | dev vs seed 0 (seeds 1..4) |
|---|---|---|---|---|---|---|
| A | 0.188 (0.019) | 2 | 39.2 | 0.34 | 4 of 5 | 0.000, 0.647, 0.898, 0.230 |
| B | 0.057 (0.009) | 5 | 11.2 | 0.22 | 2 of 5 | 0.526, 0.003, 0.003, 0.005 |
| C_hard | 0.177 (0.001) | 0 | 50 | 0.92 | 2 of 5 | 0.032, 0.000, 0.000, 0.015 |
| C_soft | 0.178 (0.002) | 0 | 50 | 0.93 | 5 of 5 | 0.022, 0.038, 0.028, 0.032 |
| D | 0.059 (0.009) | 4 | 20.6 | 0.48 | 2 of 5 | 0.475, 0.016, 0.015, 0.021 |
| E | 0.058 (0.009) | 4 | 18.4 | 0.42 | 3 of 5 | 0.523, 0.024, 0.008, 0.008 |
| F | 0.175 (0.019) | 5 | 2.8 | 0.06 | 5 of 5 | 0.176, 0.199, 0.199, 0.140 |

B, D and E land in the same basin on seeds 0, 2, 3, 4 (slack 0.0529 for B, 0.0545-0.0560 for D,
0.0538-0.0540 for E; shares about 0.65 / 0.23 / 0.12; n-lemmas 5-6 / 4 / 3) and all three fall into
the same other local optimum on seed 1 (slack 0.072-0.075), so the seed-1 deviation is the
alternation's local optimum, not the step. Facet sets of B in the main basin: {control effort, slew
time, energy balance, pointing error} | {energy balance, control effort, slew time} | {peak slew
power, pointing error, total mass, slew time, power margin}; D's third facet adds depth of discharge
(exponent just above 0.05). A: shares and sets change with the seed; two seeds give one set repeated
three times. C: the three facets are the K = 1 fit (identical 6-lemma three times; slack 0.177
against the K = 1 level 0.2036), the predicted degeneracy. F: in d = 10 a 4000-point Dirichlet
sample cannot resolve directions (5 signatures of 5, slack 0.175).

### 3e. Code size and runtime

Non-blank, non-docstring lines of the refit step in `methods.py`, helpers included (B's 9 lines are
shared by D and E): A 9; B 9; C 24; D 26 (TLS normal QP + near-row selection + fallback); E 29; F
about 22 (class). Runtime per alternation on the planted data (N = 400, d = 4): A 0.09-0.17 s, B
0.03-0.09 s, C 0.47 s, D 0.07-0.13 s, E 0.04-0.10 s, F 0.01-0.03 s; cubesat (N = 706, d = 10): B
0.22 s, D 0.48 s, E 0.42 s, C 0.92 s, F 0.06 s.

## 4. Assessment against our evidence

| | evidence used | small facet / few frontier rows | `beta_k` a support value | monotone objective | code |
|---|---|---|---|---|---|
| A | own rows only | fails always (0/60 even with true labels); tilts to a vertex | no (own-row J) | no | 9 lines |
| B | all rows; the facet's region (its mean) | robust: interior rows locate the facet (recovers 2-4-row facets given the labels); but its objective prefers to split a big facet rather than keep a sparse one (3c) | yes | yes (mean slack) | built; 9 lines |
| C | all rows, weighted | degenerate at working tau: the K = 1 fit repeated | yes | no | +24; not viable |
| D | the facet's near-frontier rows (where the frontier designs lie), B for the rest | needs >= d+1 near rows, else B; more robust than B to a wrong assignment mid-alternation (16 vs 12 single-init passes at tau = inf) because misassigned interior rows are not near the plane and do not pull it | yes (recomputed over all rows) | no; converged 14-19 of 20; a guard on the common slack would restore monotonicity at the cost of D's gain on seed 8 | +26 |
| E | D shrunk to B by 1/n_near | best of the lot on the 4 bad seeds (3/4 from the flipped start; seed 8 to 0.011-0.013) | yes | no | +29; one constant |
| F | candidate directions + touch counts | resolution-limited: fine in d = 4 (median err 0.03-0.06), useless in d = 10 | yes | yes (finite set) | +22 and a 4000 x N slack matrix |

What the evidence says the function needs: the facet's *direction* is evidence about where the
frontier designs lie (D's evidence; the tension report already reads these rows) and the facet's
*location* when there are too few frontier designs is evidence about the region (B's evidence);
`beta_k` must be the support value over all rows in every case (A is the only candidate that
violates this). The failures on seeds 1, 3, 16 are not a step problem under any candidate: the data
give a facet 2-6 frontier rows, and the mean-slack objective itself prefers another partition (3c).

## 5. Ranking (a comparison for the supervisor, not a decision)

1. **E (or D with the B fallback): B's hyperplane as the base, the tangent plane of the facet's
   near-frontier rows as the direction where the facet has >= d+1 of them.** Uses the evidence a
   facet is about (its frontier designs), keeps `beta_k` a support value, is the most accurate step
   on the oracle for facets with > 30 rows (0.002 vs B's 0.004 at tau = 50), gives the highest
   recovery from every start (16-19/20 vs B's 12-19/20), and recovers seed 8. Costs: about 30 lines,
   no monotone objective (either a documented non-monotone step or a guard on the common slack), one
   constant (lam0; or the hard switch at d+1 near rows, which is D).
2. **B as is**, with the documentation corrected: the step is sound (60/60 on the oracle); the
   remaining failures are the objective's optimum on under-sampled facets, not a defect, and should
   be described that way (G-5 wording). Zero code.
3. **F** only as an initializer or a sanity sweep in low d; not a refit.
4. **C**: drop. **A**: drop (ill-posed in principle and in measurement).

## 6. Open questions a package would have to settle

- Objective: keep mean slack (B's; monotone; prefers splitting big facets) or accept a non-monotone
  evidence-driven step (D/E) with a guard, or define a frontier-weighted slack (slack of near-frontier
  rows only) that both D and B could minimize; which one the planted recovery test should certify.
- The near-frontier band for D (1/tau, or 0.1 at tau = inf, as elsewhere) and the minimum count
  (d+1) below which the facet falls back to B; whether noise > 0 planted data changes the picture
  (this spike used noise = 0, as the R-1 test does).
- Whether `tension_report`'s per-facet contending set (today the LP on centred facet rows, i.e. B)
  should become the support of the fitted `w_k` so that report and fit agree under D/E.
- Whether the recovery claim in the docs should be stated as "17/20, and the failures are seeds
  where the mean-slack optimum is not the planted partition", with the slack numbers above.
