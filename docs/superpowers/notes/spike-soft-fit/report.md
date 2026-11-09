# Spike: fitting the several-term model with a weight on every term (is it reasonable for 0.1?)

Date 2026-11-09. Driver's spike on the supervisor's direction (`work-packages/WP10-decisions.md`,
"After the research sprint"): "do a spike now to assess the change. i prefer to make this update
for the first release if possible but only if the spike deems it reasonable".

Script: `soft_fit.py`, run in a clean checkout at a17ecf6. It is the package's own loop
(`solvers._solve_terms_once`: the same start, the same refit of each facet over all rows, the same
polish, guard and cap) with one change: each design carries the weights `softmax_k(kappa * score_ik)`
in place of the label of its dominant facet. `kappa = inf` is the package's loop.

## Verdict

Reasonable for 0.1, in a contained form: the fit uses soft weights when the term temperature kappa
is finite and is exactly today's fit at the default (kappa = inf). No committed number changes.
What the change buys is that the fit minimizes the slack of the model it reports, and that no design
needs a unique facet. It does not buy accuracy.

## What was measured

**Planted tables** (`make_frontier_data(400, 4, n_terms=3, random_state=0..19)`, five starts each;
recovered = exponent error below 0.05 after matching and at least 90 percent of the frontier rows
under the right facet).

| Fit temperature | Weights | Recovered of 20 | Single starts recovered of 100 | Mean exponent error | Seconds per fit |
|---|---|---|---|---|---|
| 50 | one label (today) | 16 | 79 | 0.063 | 0.62 |
| 50 | soft, kappa = 50 (= tau) | 16 | 77 | 0.053 | 1.24 |
| 50 | soft, kappa = 200 | 16 | 79 | 0.063 | 1.07 |
| 50 | soft, kappa = 20 | 16 | 69 | 0.058 | 1.03 |
| 50 | soft, kappa = 10 | 15 | 57 | 0.073 | 0.88 |
| inf | one label (today) | 18 | 70 | 0.045 | 0.08 |
| inf | soft, kappa = 200 | 17 | 59 | 0.047 | 0.08 |
| inf | soft, kappa = 20 | 15 | 53 | 0.064 | 0.08 |
| 10 (the estimator's default) | one label (today) | 5 | 21 | 0.093 | 0.94 |
| 10 | soft, kappa = 10 (= tau) | 7 | 33 | 0.081 | 2.16 |

The objective fell at every step of every run (the package's guard never fired). Soft weights at
kappa near tau recover as often as one label, with slightly smaller exponent error at finite tau;
very soft weights recover less often; the cost is about twice the time.

**The cubesat case** (both regimes, K = 2 and 3, the temperatures the paper selects; compared with
the package's fit).

| Weights | Contending sets and leading metrics the same as the package's | Largest exponent difference | Dominant facet agrees on |
|---|---|---|---|
| soft, kappa = tau | all four fits | 0.003 | 99.7 percent of designs or more |
| soft, kappa = 50 | all four fits | 0.008 | 98.8 percent or more |
| soft, kappa = 20 | two of four | 0.45 (two facets merged in one fit) | 50 percent in that fit |

Sharpness has to be read on the scale of the scores, which is the scale of 1 / tau. A kappa far
below tau blurs facets into one. kappa = tau is the natural setting and reproduced every conclusion.

## What the change touches

| Area | Change | Size |
|---|---|---|
| `solvers.py` | weights in place of labels in the loop when kappa is finite; the refit's mean becomes a weighted mean; the guard watches the soft objective | about 40 lines |
| `estimator.py` | pass kappa to the solver; `mean_slack_` is the slack of the reported model; `facet_`, shares and contending sets stay the analysis by dominant term | small |
| Termination | the fixed-assignment certificate (margin, stable radius, the bound of Corollary 4, the status "certified") is defined for one label per design and does not apply to a soft fit. Descent and stationarity do. One new status, "stationary", for a soft fit whose weights are self-consistent and whose weighted gaps are within tolerance | a contract amendment |
| Derivations | descent is the bound already in scope (WP10 R-41 (ii)); one more step: the gradient of the soft objective in a term's exponents is that term's weighted refit gradient, so the weighted gaps are its first-order conditions | one scripted step |
| Tests | four tests assert that a finite kappa leaves the facets unchanged; they are replaced by: the limit kappa to infinity reproduces today's fit, descent, the soft objective no higher than at the hard fit, recovery at kappa = tau no worse on the benchmark seeds | about eight tests |
| Docs and paper | the user guide's line on the term temperature; the termination page; section 6 names both; no number, table or figure changes | wording |

## Risks, stated

- **No accuracy gain to point to.** The reason to do it is that the fit matches the method as its
  author describes it and the model the estimator reports.
- **A new knob can be misused.** A kappa well below tau merges facets. Guidance (kappa on the scale
  of tau) and the existing analysis of coincident facets are the mitigation; the default is
  unchanged.
- **Local optimality is not certified for a soft fit.** The package would say so through the new
  status. Nothing is claimed that is not derived.
- **The meaning of a documented parameter changes:** today a finite term temperature rounds the
  corners of the evaluated model and leaves the facets as fitted; after the change it also fits
  with soft weights. Nothing released depends on it.

## Addendum (2026-11-09): a certificate of local optimality for the soft fit

The supervisor, on the risk "local optimality is not certified for a soft fit": "we need to chase
this cascade one more level ... can we get another certification method for the soft fit". Yes.
Script: `certificate.py`.

**The idea.** With one label per design the objective has kinks where a label changes, so the
package certifies the fixed assignment and needs a margin to say the labels hold nearby. With soft
weights the objective is smooth, so the classical second-order test applies to the objective itself,
with no assignment and no margin.

**The formulas** (alpha_ik the weights, p_k the support weights of facet k, utilde_k the
support-weighted mean, v_ik = u_i - utilde_k, n_k = sum_i alpha_ik):

    gradient in term k:   (n_k / N) (utilde_k - ubar_k^alpha)          the weighted refit gradient
    Hessian:              H = D - kappa M
        D = blockdiag((n_k / N) tau Cov_{p_k}(u))      >= 0   each term's own convex fit
        d' M d = mean_i Var_{k ~ alpha_i}(v_ik . d_k)  >= 0   how undecided the designs are between terms

The Hessian matches finite differences of the gradient to 3e-10. The curvature is each term's convex
curvature minus kappa times the ambiguity of the designs. A design with a clear dominant term adds
nothing to the second part; only designs near a junction of facets do. The package's margin is the
statement that this part vanishes: at the one-label fit the smallest curvature of H climbs to that
of D as kappa grows (2.21, 2.22, 2.34, 2.48, 2.55 against 2.57).

**The certificate.** (1) First order: every term's weighted gap within the package's tolerance
(1e-8). (2) Second order: H positive definite on the tangent space of the active face of the
product of simplices (exponents at their bound with a strictly positive multiplier are fixed; the
others are free, which is the conservative choice). Then the fit is a strict local minimizer of the
soft objective. The inherited result is the second-order sufficient condition for a smooth problem
with linear constraints (Nocedal and Wright, chapter 12), to be declared in the ledger beside I10.

**What was measured.**

| Point | First-order gap | Smallest curvature | Certified | Objective in sampled feasible directions |
|---|---|---|---|---|
| Planted table A, soft fit, kappa = tau | 2e-16 | 2.20 | yes | rises in all |
| Planted table B, soft fit, kappa = tau | 2e-16 | 0.93 | yes | rises in all |
| Twenty benchmark tables, kappa = tau | below 1e-8 | 0.13 to 2.3 (median) | 20 of 20 | |
| Cubesat, primary, K = 2 and 3 | 1e-15, 2e-15 | 0.027, 0.031 | yes, yes | rises in all |
| Cubesat, stock, K = 2 and 3 | 5e-16, 3e-15 | 0.124, 0.022 | yes, yes | rises in all |
| All terms equal to the one-term answer, kappa = tau | 8e-16 (stationary) | -17.0 | no: a saddle | falls in some |

- The test tells a minimum from a saddle. The point where all terms coincide is stationary to
  rounding and is rejected by its curvature, and the objective does fall from it.
- Certified is not recovered: 20 of 20 benchmark fits are certified local minima and 16 of 20 are
  the planted answer. The package's one-label certificate behaves the same way. Neither is a
  certificate of the global minimum.
- A Newton step on the same Hessian, restricted to the active face, drives the first-order gap from
  about 1e-6 (where the alternation alone stops) to rounding, moving the exponents by less than
  1e-5. It is the joint analogue of the facet polish the package already has.

**Limits.**

- Finite fit temperature only. At tau = inf the objective is not smooth and the test does not apply.
- A radius can be stated but is not useful yet. From a worst-case bound on the third derivative
  (the diameter of the data, tau and kappa) the Hessian stays positive within about 1e-7 of the
  fit: valid and far too cautious. A sharper bound is future work; the quantity to report is the
  smallest curvature.
- A by-product, not a rule: the all-equal point is a minimum below kappa = 0.42 (A) and 1.29 (B)
  and a saddle above. That is the sharpness below which distinct facets cannot exist at all. Facets
  merged in pairs at much higher values (the cubesat fit at kappa = 20), so it does not replace the
  guidance that kappa is read on the scale of tau.

**Cost in the package.** The Hessian is K d by K d (30 by 30 on the cubesat): one function, one
eigenvalue problem, the polish. Derivations: the gradient (already in WP17), the Hessian and its two
positive semidefinite parts, and one ledger entry for the inherited theorem.

