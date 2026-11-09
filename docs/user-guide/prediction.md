# Predicting from configuration

`TradeSpaceRegressor(regressor, trade_space)` answers a question the unsupervised estimator cannot:
where would a configuration without measurements fall? It composes two fits. `fit(X_config,
Y_metrics)` fits a clone of `trade_space` on the metrics, then fits a clone of `regressor` from
configuration to the chart coordinates.

```python {.runnable}
from sklearn.ensemble import RandomForestRegressor
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    TradeSpaceRegressor,
    make_configured_frontier_data,
)

C, Y, info = make_configured_frontier_data(
    300, 3, 2, random_state=0
)
reg = TradeSpaceRegressor(
    RandomForestRegressor(n_estimators=20, random_state=0),
    HyperbolicTradeSpace(temperature=20.0),
).fit(C, Y)
print(reg.predict(C[:2]).shape, reg.predict_novelty(C[:2]).round(2))
```

## Methods

- `predict(X_config)`: metrics, through the inverse chart.
- `predict_coordinates(X_config)`: the pair `(Z, log_v)`.
- `predict_novelty(X_config)`: V - 1, positive where the design is predicted beyond the surface.
- `predict_std(X_config)`: the regressor's `return_std` propagated by the delta method; raises
  `AttributeError` if the regressor does not provide it.
- `score`: R-squared in coordinate space, not in metric units.

Coordinates, not metrics, are the regression target, so the surrogate's error carries into the
novelty prediction. A one-dimensional `y` is accepted for a single metric. `trade_space` may be a
`Pipeline` ending in a `HyperbolicTradeSpace`, such as a preconditioner followed by the estimator.

## Using it

A predicted position inherits the surrogate's error and extrapolation risk, and is conditional on
the fitted trade space. A configuration predicted beyond V = 1 is a proposal for the next
evaluation to run, to be checked, not a result. The regressor declares `positive_only` targets and
raises `ValueError` on negative `y`.
