# The chart, holes and plots

A fitted model gives every design two kinds of coordinate. One is log V, the energy differential (level offset)
to the fitted reference surface: negative inside, positive beyond. The other `d - 1` say where along the surface the design sits,
free of overall scale. Together they are a reversible rewriting of the metrics.

```python {.runnable}
import numpy as np
from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

X, info = make_frontier_data(300, 3, random_state=0)
ts = HyperbolicTradeSpace(temperature=20.0).fit(X)
chart = ts.transform(X)                      # columns: Z (d - 1 of them), then log V
Z, log_v = chart[:, :-1], chart[:, -1]
print(np.allclose(ts.inverse_transform(chart), X), np.allclose(ts.score_samples(X), log_v))
```

`transform` returns the chart, `inverse_transform` inverts it, and `score_samples` is log V alone. A
row with a zero metric has `nan` coordinates and no inverse.

## Reading log V

V is a factor of improvement: doubling every metric doubles V. `invariant_value(X)` returns V,
`project(X)` returns the design moved onto V = 1 by scaling all its metrics together, and
`improvement_factors(X)` gives, per metric, the factor on that metric alone that reaches V = 1 (`inf`
where the exponent is numerically zero). At a finite temperature some training designs lie beyond
V = 1 by construction, so a score is meaningful relative to the band of width 1/tau: compare
`tau * log V` and the rank of log V among training scores, not V - 1 alone. A score beyond the
surface is not a verdict that the design is wanted, feasible or safe.

For a multi-term fit, log V is the soft maximum over facets, and `improvement_factors` uses each
row's active facet.

## Holes and white space

Plot the position coordinates and the designs spread over the trade space; gaps in that picture are
candidates for white space (`hyperbolic_trade_space.gaps`):

- `knn_gap_scores(Z, k=5)`: mean distance to the k nearest neighbours, normalized by its median.
- `find_holes(Z, resolution=50, threshold=2.0)`: grid points inside the convex hull of Z that sit far
  from every design; supports `d - 1` of 1, 2 or 3.
- `frontier_targets(Z_points, estimator, preconditioner=None)`: sets log V = 0 at given positions and
  maps back to metrics and, with a preconditioner, to attributes.
- `orient_by_pca(Z, mask=None)`: rotates to the principal axes of the masked rows.

A hole is a candidate and not a verdict. An empty region can be an opportunity, a categorical
stratum that cannot be occupied, or simply unsampled. The score cannot tell these apart; you decide.
The surface is also log-convex, so structure that is not log-convex is invisible to it.

## Plots

`hyperbolic_trade_space.plotting` provides `plot_log_plane`, `plot_frontier_surface_3d`,
`plot_frontier_coordinates`, `plot_v_by_variable` and `plot_tensions`. Each accepts an optional `ax`
and returns a matplotlib `Axes`; nothing calls `plt.show()`. They share one vocabulary, declared as
module constants (`FRONTIER_COLOR`, `BAND_COLOR`, `HOLE_COLOR`, `CATEGORY_COLORS`, `DATA_COLOR`,
`TENSION_CMAP`). For a multi-term fit the plots draw every facet, and `facet_labels(estimator, X)`
gives a per-row label to pass as `color=`.
