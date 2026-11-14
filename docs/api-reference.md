# API

For a coder calling the package. It follows the scikit-learn conventions [@pedregosa2011scikit; @buitinck2013api]: parameters
stored verbatim, validation in `fit`, fitted attributes ending in an underscore. Dimension is
arbitrary: `d` metrics and `d - 1` chart coordinates.

- [`LogAffinePreconditioner`](user-guide/conditioning.md), a transformer: attributes to
  larger-is-better metrics, invertible.
- [`frontier_in_original_units`](user-guide/conditioning.md), a function: the fitted reference surface as a
  monomial in raw attributes.
- [`HyperbolicTradeSpace`](user-guide/fitting.md), a transformer: fits the surface and gives the
  chart of position and log V. Fitted attributes for every number of terms include `exponents_`,
  `cell_`, `coefficients_`, `term_share_`, `objective_` (what the solver minimized) and
  `mean_slack_`, to compare fits across numbers of terms.
- [`select_temperature`](user-guide/fitting.md), a function: chooses the temperature by a target
  fraction above V = 1.
- [`make_frontier_data`](user-guide/fitting.md), a function: seeded synthetic data with a planted
  frontier.
- [`make_configured_frontier_data`](user-guide/prediction.md), a function: the same with
  configuration variables.
- [`tension_report`](user-guide/tensions.md), a function: contending set, elasticities and
  tension directions.
- [`TradeSpaceRegressor`](user-guide/prediction.md), a regressor: metrics, coordinates and novelty
  from configuration.

Submodules are used by import path:

- `hyperbolic_trade_space.coordinates`: `helmert_basis`, `alr_basis`, `to_frontier_coordinates`,
  `from_frontier_coordinates`, the chart's bases and its two maps ([fitting](user-guide/fitting.md)).
- `hyperbolic_trade_space.gaps`: `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca`
  ([chart](user-guide/chart.md)).
- `hyperbolic_trade_space.tensions`: `TensionReport`, the object `tension_report` returns.
- `hyperbolic_trade_space.plotting`: `plot_tensions`, `plot_log_plane`, `plot_frontier_surface_3d`,
  `plot_frontier_coordinates`, `plot_v_by_variable`, `plot_ternary`, `ternary_marker_values`,
  `cell_labels`.
- `hyperbolic_trade_space.estimator`: `EPS_ZERO_EXPONENT` (`1e-12`). An exponent at or below it is
  numerically zero, so `score_samples` reads a zero metric there as `0 log 0 := 0`.
  `PARTICIPATION_THRESHOLD` (`1e-3`). An exponent above it participates. It is the threshold of
  `tension_report` and of `conditioning_`.
- `hyperbolic_trade_space.solvers`: the multi-term solver, the `Termination` record and the
  certificate functions ([Reading termination](user-guide/termination.md)).

## Reference

### `HyperbolicTradeSpace`

::: hyperbolic_trade_space.HyperbolicTradeSpace
    options:
      show_root_heading: false
      heading_level: 4

### `LogAffinePreconditioner`

::: hyperbolic_trade_space.LogAffinePreconditioner
    options:
      show_root_heading: false
      heading_level: 4

### `TradeSpaceRegressor`

::: hyperbolic_trade_space.TradeSpaceRegressor
    options:
      show_root_heading: false
      heading_level: 4

### `frontier_in_original_units`

::: hyperbolic_trade_space.frontier_in_original_units
    options:
      show_root_heading: false
      heading_level: 4

### `make_configured_frontier_data`

::: hyperbolic_trade_space.make_configured_frontier_data
    options:
      show_root_heading: false
      heading_level: 4

### `make_frontier_data`

::: hyperbolic_trade_space.make_frontier_data
    options:
      show_root_heading: false
      heading_level: 4

### `select_temperature`

::: hyperbolic_trade_space.select_temperature
    options:
      show_root_heading: false
      heading_level: 4

### `tension_report`

::: hyperbolic_trade_space.tension_report
    options:
      show_root_heading: false
      heading_level: 4

### `__version__`

::: hyperbolic_trade_space.__version__
    options:
      show_root_heading: false
      heading_level: 4
