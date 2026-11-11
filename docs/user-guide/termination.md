# Reading `termination_` and `conditioning_`

Every fit records how it stopped.

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

1. Descent: no step made the mean slack worse (`mean_slack_`).
2. Numerical stationarity: no first-order improvement is left. The term gap G_k measures what
   remains.
3. Conditional local optimality: if no design sits exactly on a seam between terms, small changes
   to the terms cannot change any design's assignment, so the fixed assignment is optimal. The
   assignment margin is the smallest gap by which a row's term beats the runner-up; the stable
   radius is the perturbation provably leaving every design's assignment unchanged.

## Statuses

`termination_.status` is one of:

- `certified`: assignment fixed, residuals within `eps_feas`, `max_gap` within `eps_kkt`, no empty
  cell, margin positive: all three levels.
- `stationary_without_margin`: the same, with margin at most `eps_feas` or an empty cell. Levels 1
  and 2.
- `uncertified`: assignment fixed, a residual or the gap above tolerance.
- `guard_stop`: an iteration raised the mean slack by more than `guard_tol`. Not converged.
- `iteration_cap`: alternation cap reached, fit kept; warned only when gap or last objective
  change exceeds `tol`.
- `not_applicable`: one term, `refit_step="tangent"`, a `penalty`, one metric, fewer designs than
  terms, or a soft fit at infinite tau.

`fit` warns for `uncertified` and `guard_stop`.

A soft fit weighs every term: no assignment, no margin.

- `certified`: term gaps within `eps_kkt` and `min_curvature` above `eps_feas`, a strict local
  minimizer of the soft objective.
- `stationary`: the gaps hold, the curvature does not: a saddle or a flat direction.
- `uncertified`: as above.

## The fields

- `status`, `reason`, `n_iter`; `max_gap`, `gaps` (`nan` for an empty cell) and `shares`, the
  row shares, each cell's fraction of all designs (`term_share_` counts near-frontier designs only).
- `n_distinct_terms`: terms whose exponent vectors differ by more than 1e-3.
- `bound`: the row-share-weighted sum of term gaps, bounding the distance from the fixed-assignment
  optimum.
- `gamma`, `radius`: the margin and stable radius, `nan` at one term.
- `sum_residual`, `floor_residual`, `offset_residual`, `objective_change`, `assignment_changes`, `n_empty`, tolerances: diagnostics.
- `min_curvature`: a soft fit's smallest curvature; `nan` otherwise.
  A soft fit leaves `gamma`, `radius` and `bound` `nan`.

The tolerances are module constants of `hyperbolic_trade_space.solvers`, not parameters: `EPS_KKT` =
1e-8, `EPS_FEAS` = 1e-9, `GUARD_TOL` = 1e-12, `POLISH_STEPS` = 5.

## `conditioning_`

The smallest eigenvalue of the restricted Hessian over the participating
exponents (above 1e-3), one per term. A small value marks a nearly flat direction. It is `nan` at infinite
temperature and for a term with fewer than two participating exponents.

Why it matters: along a flat direction many exponent vectors fit almost equally well, so the reported
exponents and the contending set are not pinned by the data; two metrics that move together in log space
cause it. How it is computed: the Hessian of the objective at the fit is the temperature times the
support-weighted covariance of the log-metrics, restricted to the participating exponents and to
directions that keep their sum fixed; the smallest eigenvalue is read off, and the fit is untouched. On
your own problem, read `conditioning_` after `fit`, comparing fits at one temperature because the value
scales with it. A value far below a comparable fit's is a prompt for feature engineering: drop or combine
the metrics that move together, change the [conditioning](conditioning.md), refit and see whether it rises.
The block sets `min_exponent=0.1`, a floor that keeps the duplicate in the fit; at the default of zero the fit gives it a zero exponent and `conditioning_` prints 12.4.

```python {.runnable}
import numpy as np
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    make_frontier_data,
)

Xf, _ = make_frontier_data(400, 3, random_state=0)
Xr = Xf.copy()
rng = np.random.default_rng(0)
# the second metric nearly repeats the first
Xr[:, 1] = Xr[:, 0] * np.exp(1e-3 * rng.standard_normal(400))
for data in (Xf, Xr):
    fit = HyperbolicTradeSpace(temperature=20.0, min_exponent=0.1).fit(
        data
    )
    print(fit.conditioning_)
```

## How small is a small margin

The margin `gamma` is in score units (log metrics), the scale of the band 1/tau. Level 3 holds
whenever `gamma` is positive, as the status says. The median margin, the median gap between a design's best and
second-best term score, says how typical the tightest design is: a `gamma` far below it means a few
designs sit near a seam and most do not; those few are the ones to watch under resampling.

```python {.runnable}
import numpy as np

S = np.log(X) @ ts.exponents_.T - ts.log_offset_
top = np.sort(S, axis=1)
print(t.gamma, 1 / 50.0, np.median(top[:, -1] - top[:, -2]), t.radius)
```

On this table at tau = 50, `gamma` is 0.0020 and the median margin 0.21: level 3 holds, and the
tightest design sits a hundredfold nearer a seam than the typical one.

## What to decide from it

Keep three claims apart. [`certified`](paper:thm-certificate) is the first: a local optimum of the objective, not of other restarts. The second, a description of the observed designs, is read from `mean_slack_`. The
third, that it holds outside the table or supports a decision, the certificate does not make: check it
on held-out evaluations.
