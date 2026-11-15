# From the chart back to a design

For an analyst who has picked a point on the chart and wants a design under it.

The way from a design to its chart point is a computation: evaluate the configuration, condition the
attributes into metrics, read the chart. The way back loses invertibility, at one step only. This page says
which route back exists for which point, what a design proposed for a point is worth, and how to find out.
It is the bridge to [the search of Section 7](paper:sect-search), which is future work.

## Where invertibility is lost

The conditioning is invertible ([pull-back to attributes](paper:thm-pullback)) and so is the chart
([the chart theorem](paper:thm-chart)), so a chart point maps back to attributes and to metrics. The step that does not invert is the evaluation, from
configuration to attributes, in three ways:

- many configurations can give one outcome, so a point's preimage is not one configuration;
- not every point is the outcome of any configuration, so a preimage can be empty;
- an evaluation can differ from one run to the next, so one configuration can land at more than one point.

## Two routes back

**The sampled route.** A point with a datum is a row of your table, so its configuration is the row's. This is
a lookup. Nothing is conjectured, although a noisy evaluation may land the same configuration elsewhere next
time.

**The conjecture route.** A point without a datum has no known configuration. A **proposal** is a
configuration chosen for it, together with the chart point the regressor predicts for that configuration and a
tolerance. It is a conjecture until it is **checked**, for three reasons: the regressor predicts and does not
evaluate, the preimage is not unique so a **selection rule** has to pick, and the design, once built and
measured, may land somewhere else.

## Propose and predict

`TradeSpaceRegressor` is the prediction half. It maps a configuration to the chart point, and the regression
error carries into the position and the level, not into raw metrics.
[The prediction page](user-guide/prediction.md) has its methods. A selection rule is yours to choose; the
case's code uses one, nearest in a seeded pool: of many random configurations, take the one predicted nearest
the target.

```python {.runnable}
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    TradeSpaceRegressor,
    make_configured_frontier_data,
)

C, Y, _ = make_configured_frontier_data(300, 3, 2, random_state=0)
reg = TradeSpaceRegressor(
    RandomForestRegressor(n_estimators=30, random_state=0),
    HyperbolicTradeSpace(temperature=20.0),
).fit(C, Y)

# a target: a position in the chart, not any row's
# (the level is handled by lv below)
Z_target = reg.predict_coordinates(C)[0].mean(axis=0)

# selection rule: of 5,000 random configurations,
# the one predicted nearest the target
rng = np.random.default_rng(0)
pool = rng.uniform(C.min(0), C.max(0), size=(5000, C.shape[1]))
Zp, lv = reg.predict_coordinates(pool)
distance = np.sqrt(
    ((Zp - Z_target) ** 2).sum(axis=1) + (2 * lv) ** 2
)  # the level counts double
c = pool[[distance.argmin()]]
z_pred, lv_pred = reg.predict_coordinates(c)
print("proposal", c.round(2))
print("predicted position", z_pred.round(2), "log V", lv_pred.round(2))
```

Other rules differ in what they hold fixed: the smallest change from a design you name stays close to
something known to evaluate. None is a property of the model.

## Check, and the three outcomes

Build or evaluate the proposed configuration, and compare the chart point of its measured metrics with the
predicted one. The tolerance is the band $1/\tau$ of the fit by default, $\tau$ its fit temperature, on the position and on log V.
One of three things happens.

- **Confirmed.** The design is feasible and the measured point is within the tolerance of the predicted
  one. The prediction held at this design; one confirmed design is not a rate.
- **Refuted.** The design is feasible and the measured point is farther. The measurement is a row the table
  lacked: append it and rerun the fit.
- **Infeasible.** The design fails a feasibility condition, so it is not a design for this problem. Keep the
  row with its flags and refit.

A refuted proposal costs one evaluation and returns a row the table lacked, which is what a refit needs.

The bridge serves both aims of the search: a proposal at white space seeks a design that fills it, and a
proposal beyond the fitted reference surface pushes it outward. Both are settled by the same check.

On the cubesat case the check ran once on three proposals. Each landed within the band of its predicted
point, and each failed the depth-of-discharge condition, so the case's reading is that they reached the surface
by spending the battery ([Appendix D.10](paper:sub-d-10)). Two of the three are the same configuration, since two
white-space points had one pooled configuration nearest.

## The outer loop, and what is open

Propose, evaluate, append the row, refit, and repeat: the outer loop of the paper's Section 7 is the refit. It
need not move outward at every step. The conjecture is that it is a
submartingale, a process that rises in expectation: outward in expectation, with a convergence result when the expected progress ceases. This is
future work, and no conditions under which it holds are derived.

## What this release ships

- Shipped: `TradeSpaceRegressor` and its methods, and the sampled route (a lookup).
- Shipped as case code, not as package functions: the pooled proposal and the check of the cubesat case
  (`examples/adcs/experiments/check_designs.py`, `case.predict_check`).
- Not shipped, planned for the next release: package functions for proposing and for checking, a choice of
  selection rule, and a demonstration of the loop with a Monte Carlo evaluation of each proposal.
- Not studied: when the loop converges.
