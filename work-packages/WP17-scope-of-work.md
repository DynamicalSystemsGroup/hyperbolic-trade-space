# WP17 — Scope of work: the several-term fit with soft weights (the fit at the model's own sharpness)

**Status:** approved for execution by the driver under the mandate (`release-candidate.md`), on the
supervisor's conditional direction quoted below; for his review at the PR. **Supervisor:** mzargham.
**Date:** 2026-11-09. **Evidence:** `docs/superpowers/notes/spike-ggp-fit/report.md`,
`docs/superpowers/notes/spike-soft-fit/report.md`.

## Origin

The supervisor, verbatim: "i don't think each config needs to be in a unique facet ... any config is
likely to have a projection onto each facet but analysis tells us which dominates." And, on putting
it in the code: "do a spike now to assess the change. i prefer to make this update for the first
release if possible but only if the spike deems it reasonable". The spike deems it reasonable in the
contained form scoped here.

## Goal

When the term temperature kappa is finite, the estimator fits the several-term model with a weight
on every term for every design (the weights of the model itself), so the fit minimizes the slack of
the model it reports. At the default (kappa = inf) the fit is exactly today's.

## Non-goals

No change to any default. No change to any committed number, table, figure or dataset. No automatic
choice of kappa, no annealing schedule. No certificate of local optimality for a soft fit. No change
to the one-term fit.

## Deliverables and requirements

- R-1. `solvers.solve_terms` and the estimator: with finite `term_temperature` the loop uses the
  weights `softmax_k(kappa * (w_k . u_i - beta_k))`, the refit of facet k is the supporting
  hyperplane over all rows centred at the weighted mean, the guard watches the soft objective.
  *Check:* a test that the soft objective never rises across the returned history on the benchmark
  tables.
- R-2. *The default is untouched.* With `term_temperature = np.inf` every fitted attribute is
  identical to the fit before this package on the planted benchmark and on the cubesat fits.
  *Check:* a test against values recorded before the change; the whole existing suite, with only
  the four tests named in the spike's readout rewritten.
- R-3. *The limit.* As kappa grows the soft fit approaches the hard one. *Check:* a test at a large
  finite kappa against the hard fit, with a stated tolerance.
- R-4. *The fit serves its model.* The soft objective at the soft fit is no higher than at the hard
  fit. *Check:* a test on the benchmark tables.
- R-5. *Recovery is no worse at kappa = tau.* *Check:* the spike's benchmark as a test at
  tau = 50 (16 of 20 for both), with the spike's criterion.
- R-6. *Analysis stays analysis.* `facet_`, the facet shares, the contending sets and the
  elasticities are read from the dominant term as today; `mean_slack_` is the slack of the reported
  model; the docstrings say which is fit and which is analysis.
- R-7. *Termination.* For a soft fit the fixed-assignment quantities (margin, radius, the bound) are
  not asserted; a status "stationary" reports self-consistent weights with weighted gaps within
  tolerance; the interface contract is amended (the status, the meaning of `term_temperature`).
  *Check:* the contract test; tests of the status on a converged and on a capped run.
- R-8. *One scripted step:* the gradient of the soft objective in a term's exponents is that term's
  weighted refit gradient (with the offset tied to the support value), so the weighted gaps are the
  first-order conditions. Appendix B regenerated in the same push. *Check:* the proof-map checker.
- R-9. *Words.* The user guide (fitting, termination), the API page, the glossary's "term
  temperature" and "assignment", and section 6 of the paper say what a finite kappa now does, give
  the guidance that kappa is read on the scale of tau, and claim nothing beyond R-1 to R-8. *Check:*
  the vocabulary tool and the claims register; the driver's browser read.

## Good enough

R-1 to R-9 checked; the suite green on both platforms; `uv lock --check`; no AI attribution; the
driver re-runs the spike's cubesat comparison against the built estimator at kappa = tau and finds
the same contending sets and leading metrics.

## Order and ownership

After the first push of WP10 Amendment 4 (which renames a field in `tensions.py`). This package owns
`src/hyperbolic_trade_space/solvers.py` and `estimator.py` and their tests; the lemma step and the
words are coordinated by the PM with the owners of the derivations and of the paper.

## Agent's defaults

The trigger is the existing parameter (no new parameter); the new status is named "stationary";
tolerances reuse `EPS_KKT` and `EPS_FEAS`; the benchmark's seeds and criterion are the spike's.
