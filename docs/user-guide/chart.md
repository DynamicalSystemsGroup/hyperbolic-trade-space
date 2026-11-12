# The chart, holes and plots

A fitted model gives every design two kinds of coordinate. One is log V, the energy differential (level offset)
to the fitted reference surface: negative inside, positive beyond. The other `d - 1` say where along the surface the design sits,
free of overall scale. Together they are a reversible rewriting of the metrics.

```python {.runnable}
import numpy as np
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    make_frontier_data,
)

X, info = make_frontier_data(300, 3, random_state=0)
ts = HyperbolicTradeSpace(temperature=20.0).fit(X)
# columns: Z (d - 1 of them), then log V
chart = ts.transform(X)
Z, log_v = chart[:, :-1], chart[:, -1]
print(
    np.allclose(ts.inverse_transform(chart), X),
    np.allclose(ts.score_samples(X), log_v),
)
```

`transform` returns the chart, `inverse_transform` inverts it, and `score_samples` is log V alone. A
row with a zero metric has `nan` coordinates and no inverse.

With two metrics the chart is the log plane itself:

```python {.runnable}
from hyperbolic_trade_space.plotting import plot_log_plane

X2, _ = make_frontier_data(300, 2, random_state=0)
ts2 = HyperbolicTradeSpace(temperature=20.0).fit(X2)
plot_log_plane(ts2, X2)
```

<figure markdown>
![Designs in the log plane of two metrics, a straight frontier line, and a grey band of near-frontier designs below it.](../generated/figures/log-plane-light.png#only-light)
![Designs in the log plane of two metrics, a straight frontier line, and a grey band of near-frontier designs below it.](../generated/figures/log-plane-dark.png#only-dark)
<figcaption>Figure 4. One term in the log plane: the line is V = 1; the grey strip below it is log V from -1/tau to 0.</figcaption>
</figure>

## Reading log V

V is a factor of improvement: doubling every metric doubles V. Three methods read it:

- `invariant_value(X)` returns V.
- `project(X)` returns the design moved onto V = 1 by scaling all its metrics together.
- `improvement_factors(X)` gives, per metric, the factor on that metric alone that reaches V = 1
  (`inf` where the exponent is numerically zero).

At a finite temperature some training designs lie beyond V = 1 by construction, so a score is
meaningful relative to the near-frontier band, |log V| below 1/tau. Compare `tau * log V` and the rank of log V among
training scores, not V - 1 alone. A score beyond the surface is not a verdict that the design is
wanted, feasible or safe.

For a multi-term fit, log V is the maximum over terms at the default `term_temperature=inf`, and
`improvement_factors` uses each row's assigned term.

## Holes and white space

Gaps in the designs' spread over the position coordinates are candidates for white space
(`hyperbolic_trade_space.gaps`):

- `knn_gap_scores(Z, k=5)`: mean distance to the k nearest neighbours, normalized by its median.
- `find_holes(Z, resolution=50, threshold=2.0)`: grid points inside the convex hull of Z that sit far
  from every design; supports `d - 1` of 1, 2 or 3.
- `frontier_targets(Z_points, estimator, preconditioner=None)`: sets log V = 0 at given positions and
  maps back to metrics and, with a preconditioner, to attributes.
- `orient_by_pca(Z, mask=None)`: rotates to the principal axes of the masked rows.

Holes of a three-metric fit, most isolated first:

```python {.runnable}
from hyperbolic_trade_space.gaps import find_holes

X3, _ = make_frontier_data(300, 3, random_state=0)
ts3 = HyperbolicTradeSpace(temperature=20.0).fit(X3)
chart3 = ts3.transform(X3)
holes, scores = find_holes(chart3[:, :-1], resolution=30, threshold=3.0)
print(len(holes), scores[:3].round(2))
```

A hole is a candidate and not a verdict. An empty region can be an opportunity, a categorical
stratum that cannot be occupied, or simply unsampled. The score cannot tell these apart; you decide.
The surface is also log-convex, so structure that is not log-convex is invisible to it.

## Plots

`hyperbolic_trade_space.plotting` provides six plots:

- `plot_log_plane`: two metrics, the data, the frontier and its band.
- `plot_frontier_surface_3d`: three metrics, the frontier surface.
- `plot_frontier_coordinates(Z, log_v)`: the chart, the columns of `ts.transform(X)`, with optional
  holes and targets.
- `plot_v_by_variable`: log V against a configuration variable.
- `plot_tensions`: the tension report as a heatmap.
- `plot_ternary`: three metrics as shares of a total, with the region each term dominates
  ([example](../examples.md#three-metrics-as-shares-of-a-total)); `ternary_marker_values` gives V at its markers.

Each accepts an optional `ax` and returns a matplotlib `Axes`; nothing calls `plt.show()`. The designs are one colour by default, whatever the number of terms; in
`plot_log_plane` and `plot_frontier_surface_3d`, `color="cell"` colours them by cell, the term that
scores each highest (`cell_labels(estimator, X)`), and any other string raises `ValueError`.
