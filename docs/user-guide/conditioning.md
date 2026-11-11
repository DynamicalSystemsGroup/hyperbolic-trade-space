# Conditioning

The fit consumes a strictly positive matrix of larger-is-better metrics. Real evaluations produce
attributes: kilograms, dollars, error rates, counts, some of them better when small. The map from
attributes to metrics is yours to choose, because it is part of the question you ask: a stable fitted
direction answers that question as conditioned and is not a context-free discovery. The package
supplies `LogAffinePreconditioner`, which implements the family of maps the method allows, and
`frontier_in_original_units`, which reports the fitted reference surface back in the units you started with.

```python {.runnable}
import numpy as np
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
)

rng = np.random.default_rng(0)
# three raw attributes
A = np.exp(rng.normal(size=(200, 3))) * [1.0, 10.0, 100.0]
# the second attribute is smaller-is-better
pre = LogAffinePreconditioner(orientation=[1, -1, 1])
M = pre.fit_transform(A)
print(np.allclose(pre.inverse_transform(M), A))
```

## Orientation

Each column is larger-is-better (orientation +1) or smaller-is-better (orientation -1). A
smaller-is-better attribute is inverted in log space and comes out larger-is-better. Orientation is
a judgement about the problem, and a wrong sign is not detected: the fit finds a surface for the
wrongly oriented metric. The cheap diagnostic is the sign of the pulled-back exponent below.

## Shift and reference point

Logarithms need positive arguments. `shift` moves the argument to `a + shift`; it must keep every
value nonnegative, and `ValueError` with "Negative values in data" is raised otherwise. A shift is a
decision about where the scale begins, and different shifts give different fits. Leave it at zero
unless an attribute legitimately reaches zero.

The reference point is the attribute value that maps to metric 1; it is the centre removed by the
scaler and stored as `log_offset_`. It fixes what V = 1 means in practice.

## Scaling

After the logarithm a scaler is fitted per column. `scaler="standard"` gives each metric unit
log-standard-deviation; `"robust"` normalizes the interquartile range instead and suits data where a
few extreme designs would dominate; `None` keeps the pure power law. A scikit-learn scaler instance
works if it is affine per column. The reason to scale is the temperature of the next page: it is
quoted in inverse log-spread, so equal log-spread makes one temperature mean the same for every
column.

## Zeros and infeasible rows

An entry at exactly `-shift` maps to metric 0, and the scaler ignores it. The estimator tolerates
zero metrics: such a row has V = 0 and no support weight, and its chart coordinates are `nan`.
For a smaller-is-better attribute a raw zero is the best value, so mapping it to metric 0 is
bookkeeping and not a verdict; shift the column if that matters.

Infeasible rows are not the preconditioner's job. Remove designs that violate a constraint or failed
to evaluate before conditioning, so the fitted scale describes feasible designs only.

## Diagnostics

None proves a conditioning right; they show whether the story is sensible.

- After `"standard"` scaling, `np.log(M).std(axis=0)` is one in every finite column.
- `inverse_transform(transform(X))` returns `X`; the conditioning is exactly invertible.
- The pulled-back exponent on a raw attribute is `w_j * alpha_j`. A sign that disagrees with what
  you believe about that attribute is a prompt to revisit orientation or shift.
- Refit under a second reasonable conditioning, the other scaler or a modest change of shift. If the
  contending set moves, the finding depends on the conditioning, and should be reported that way.
- After a fit, `conditioning_` reads the same question from the fit itself: a value far below a comparable fit's marks
  metrics that move together; [Termination](termination.md#conditioning_) shows how to read it.

## The pull-back to attributes

For a fitted single-term estimator, `frontier_in_original_units(estimator, preconditioner)` returns
`exponents_orig`, `log_const` and `shift`. The surface is again a monomial, now in the raw
attributes: a negative exponent marks a smaller-is-better attribute. Evaluate
`log_const + exponents_orig @ np.log(X + shift)` to get log V for raw rows. The function needs a
single-term fit; a multi-term fit is not a monomial in the attributes.
