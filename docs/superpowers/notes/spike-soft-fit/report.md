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
