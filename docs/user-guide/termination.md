# Reading `termination_` and `conditioning_`

Every fit records how it stopped. At one term the fit is a convex program and its answer is the
minimizer. With several terms it alternates between weights from the current model and refitting each
facet; the record says which of three levels it meets.

```python {.runnable}
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    make_frontier_data,
)

X, info = make_frontier_data(400, 4, n_terms=3, random_state=0)
ts = HyperbolicTradeSpace(
    n_terms=3, temperature=50.0, random_state=0
).fit(X)
t = ts.termination_
print(t.status, t.max_gap < 1e-8, t.gamma > 0)
print(ts.conditioning_.round(1))
```

## The three levels

1. Descent: no step made the mean slack worse (`mean_slack_`, defined at every number of terms).
2. Numerical stationarity: no first-order improvement is left. The facet gap G_k measures what
   remains.
3. Conditional local optimality: if no design sits exactly on a seam between facets, small changes
   to the facets cannot change which facet dominates which design, so the fixed assignment is optimal.
   The assignment margin is the smallest gap by which a row's facet beats the runner-up; the stable radius
   is the perturbation provably leaving every facet unchanged.

## Statuses

`termination_.status` is one of:

- `certified`: assignment fixed, residuals within `eps_feas`, `max_gap` within `eps_kkt`, no empty
  facet, margin positive. All three levels hold.
- `stationary_without_margin`: the same, with margin at most `eps_feas` or an empty facet. Levels 1
  and 2 only. At infinite temperature this happens when a frontier row lies on two facet planes or two
  facets coincide.
- `uncertified`: assignment fixed, a residual or the gap above tolerance.
- `guard_stop`: an iteration raised the mean slack by more than `guard_tol`. Not converged.
- `iteration_cap`: `max_iter` reached. Not converged.
- `not_applicable`: one term, `facet_step="tangent"`, a `penalty`, one metric, fewer designs than
  facets, or a soft fit at infinite temperature. Not a failure.

`fit` warns (a `ConvergenceWarning` naming the status and the largest gap) for `uncertified`,
`guard_stop` and `iteration_cap`.

A soft fit (finite `term_temperature`) has no assignment, so no margin:

- `certified`: weighted gaps within `eps_kkt` and `min_curvature` above `eps_feas`, a strict local
  minimizer of the soft objective.
- `stationary`: the gaps hold, the curvature does not: a saddle or a flat direction.

## The fields

- `status`, `reason`, `n_iter`; `max_gap`, `gaps` (`nan` for an empty facet) and `shares`.
- `bound`: the share-weighted sum of facet gaps, bounding the distance from the fixed-assignment
  optimum.
- `gamma`, `radius`: the margin and stable radius, `nan` at one term.
- Residuals, `objective_change`, `assignment_changes`, `n_empty`, tolerances: diagnostics.
- `min_curvature`: soft fit only, the smallest curvature on the active face; `nan` otherwise.
  A soft fit leaves `gamma`, `radius` and `bound` `nan`.

The tolerances are module constants of `hyperbolic_trade_space.solvers`, not parameters: `EPS_KKT` =
1e-8, `EPS_FEAS` = 1e-9, `GUARD_TOL` = 1e-12, `POLISH_STEPS` = 5.

## `conditioning_`

The smallest eigenvalue of the restricted Hessian at each facet's fit, over the participating
exponents (above 1e-3), one per facet. A small value marks a nearly flat direction (weakly identified exponents). It is `nan` at infinite
temperature and for a facet with fewer than two participating exponents.

## How small is a small margin

The margin `gamma` is in score units (log metrics), the scale of the band 1/tau; `radius` is
`gamma / (2R)`, with R the largest norm of a row (u, -1). Compare `gamma` with the median margin,
the median gap between a design's best and second-best facet score: far below it, a few designs sit
on a seam and most do not.

```python {.runnable}
import numpy as np

S = np.log(X) @ ts.exponents_.T - ts.log_offset_
top = np.sort(S, axis=1)
print(t.gamma, 1 / 50.0, np.median(top[:, -1] - top[:, -2]), t.radius)
```

On this table at tau = 50, `gamma` is 0.0020 against a band of 0.02 and a median margin of 0.21:
level 3 holds, for perturbations well under the band.

## What to decide from it

`certified` says the run is a local optimum (of its fixed assignment, or of the soft objective), nothing about other restarts. A small `conditioning_` or `n_eff_` says to widen the sample or read exponents loosely.
