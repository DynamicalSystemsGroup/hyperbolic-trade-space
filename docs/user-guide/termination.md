# Reading `termination_` and `conditioning_`

Every fit carries a record of how it stopped. At one term the fit is a convex program and its answer
is the minimizer. With several terms the fit alternates between assigning designs to facets and
refitting each facet, and the record says which of three levels the returned run meets.

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

1. Descent: no step made the mean slack worse (`mean_slack_` is that quantity, defined at every number
   of terms; `objective_` is what the solver minimized: the soft maximum at one term, the mean slack
   at several).
2. Numerical stationarity: each facet sits where no first-order improvement is left. The facet gap
   G_k measures what remains; at infinite temperature it is the linear-programming duality gap.
3. Conditional local optimality: if no design sits exactly on the seam between two facets, small
   changes to the facets cannot change which facet owns which design, and the fixed assignment is
   optimal. The assignment margin is the smallest gap by which a row's facet beats the runner-up; the
   stable radius is the size of perturbation that provably leaves every row's facet unchanged.

## Statuses

`termination_.status` is one of:

- `certified`: assignment fixed, residuals within `eps_feas`, `max_gap` within `eps_kkt`, no empty
  facet, margin positive. All three levels hold.
- `stationary_without_margin`: the same, with margin at most `eps_feas` or an empty facet. Levels 1
  and 2 only, with no local-optimality claim.
- `uncertified`: assignment fixed, a residual or the gap above tolerance. Do not rely on the fit;
  `fit` warns.
- `guard_stop`: an iteration raised the mean slack by more than `guard_tol`. Not converged; `fit`
  warns.
- `iteration_cap`: `max_iter` reached. Not converged; `fit` warns.
- `not_applicable`: one term, `facet_step="tangent"`, a `penalty`, one metric, or fewer designs than
  facets. Not a failure; the gaps are diagnostics only.

The warnings are scikit-learn `ConvergenceWarning`s that name the status and the largest gap. A
guard stop or an iteration cap is never reported as `certified`.

At infinite temperature the margin is zero when a frontier row lies on two facet planes or two
facets coincide; the status is then `stationary_without_margin`.

## The fields

- `status`, `reason`, `n_iter`: the status, the solver's stop message, the refit iterations.
- `max_gap`, `gaps`, `shares`: the largest facet gap, the gap of each facet (`nan` for an empty
  one), and each facet's row share.
- `bound`: the share-weighted sum of facet gaps, a bound on the objective's distance from the
  fixed-assignment optimum for this run. It does not compare restarts.
- `gamma`, `radius`: the assignment margin and the stable radius. Both are `nan` at one term: with no
  competing facet there is no runner-up to beat, so the margin is undefined, not infinite.
- `sum_residual`, `floor_residual`, `offset_residual`, `objective_change`, `assignment_changes`,
  `n_empty`: feasibility and step diagnostics.
- `eps_kkt`, `eps_feas`, `guard_tol`: the tolerances in force.

The tolerances are module constants of `hyperbolic_trade_space.solvers`, not parameters:
`EPS_KKT` = 1e-8, `EPS_FEAS` = 1e-9, `GUARD_TOL` = 1e-12, and `POLISH_STEPS` = 5 reduced-Newton steps
after each finite-temperature facet refit. The certificate functions (`simplex_gap`, `facet_gap`,
`assignment_margin`, `fixed_assignment_bound`) are in the same module.

## `conditioning_`

Shape `(n_terms,)`: the smallest eigenvalue of the restricted Hessian of the objective at each
facet's fit, taken over the participating exponents (above 1e-3). A small value marks a nearly flat
direction, so weakly identified exponents; compare it with `n_eff_`, which says how many designs
carry the fit. It is `nan` at infinite temperature and for a facet with fewer than two participating
exponents.

## What to decide from it

`certified` says the returned run is a local optimum of its fixed assignment; it says nothing about
other restarts or about optimality beyond the fixed assignment. A small `conditioning_` or `n_eff_` says to widen the sample or
read the exponents loosely. A degenerate input (one valid row) returns uniform exponents and a
`UserWarning`.
