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
  `cell_`, `coefficients_`, `term_share_`, `loss_` (what the solver minimized) and
  `mean_slack_`, to compare fits across numbers of terms.
- [`select_temperature`](user-guide/fitting.md), a function: chooses the temperature by a target
  fraction above V = 1 ([the path against tau](user-guide/temperature.md)).
- [`make_frontier_data`](user-guide/fitting.md), a function: seeded synthetic data with a planted
  frontier.
- [`make_configured_frontier_data`](user-guide/prediction.md), a function: the same with
  configuration variables.
- [`trade_off_report`, `tension_matrix`, `design_tensions`](user-guide/tensions.md), functions: contending
  set and elasticities; the slope of one metric against another.
- [`TradeSpaceRegressor`](user-guide/prediction.md), a regressor: metrics, coordinates and novelty
  from configuration.

Submodules are used by import path:

- `tradespace.coordinates`: `helmert_basis`, `alr_basis`, `to_frontier_coordinates`,
  `from_frontier_coordinates`, the chart's bases and its two maps ([fitting](user-guide/fitting.md)).
- `tradespace.gaps`: `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca`
  ([chart](user-guide/chart.md)).
- `tradespace.tensions`: `TradeOffReport`, `DesignTensions`: what the functions return.
- `tradespace.plotting`: `plot_association`, `plot_log_plane`, `plot_frontier_surface_3d`,
  `plot_frontier_coordinates`, `plot_v_by_variable`, `plot_ternary`, `ternary_marker_values`,
  `cell_labels`, `plot_temperature_path`, `temperature_path` ([the fit temperature](user-guide/temperature.md)).
- `tradespace.estimator`: `EPS_ZERO_EXPONENT` (`1e-12`). An exponent at or below it is
  numerically zero, so `score_samples` reads a zero metric there as `0 log 0 := 0`.
  `PARTICIPATION_THRESHOLD` (`1e-3`). An exponent above it participates. It is the threshold of
  `trade_off_report` and of `conditioning_`.
- `tradespace.solvers`: the multi-term solver, the `Termination` record and the
  certificate functions ([Reading termination](user-guide/termination.md)).

## Reference

### `HyperbolicTradeSpace`

::: tradespace.HyperbolicTradeSpace
    options:
      show_root_heading: false
      heading_level: 4

### `LogAffinePreconditioner`

::: tradespace.LogAffinePreconditioner
    options:
      show_root_heading: false
      heading_level: 4

### `TradeSpaceRegressor`

::: tradespace.TradeSpaceRegressor
    options:
      show_root_heading: false
      heading_level: 4

### `design_tensions`

::: tradespace.design_tensions
    options:
      show_root_heading: false
      heading_level: 4

### `frontier_in_original_units`

::: tradespace.frontier_in_original_units
    options:
      show_root_heading: false
      heading_level: 4

### `make_configured_frontier_data`

::: tradespace.make_configured_frontier_data
    options:
      show_root_heading: false
      heading_level: 4

### `make_frontier_data`

::: tradespace.make_frontier_data
    options:
      show_root_heading: false
      heading_level: 4

### `select_temperature`

::: tradespace.select_temperature
    options:
      show_root_heading: false
      heading_level: 4

### `tension_matrix`

::: tradespace.tension_matrix
    options:
      show_root_heading: false
      heading_level: 4

### `trade_off_report`

::: tradespace.trade_off_report
    options:
      show_root_heading: false
      heading_level: 4

### `__version__`

::: tradespace.__version__
    options:
      show_root_heading: false
      heading_level: 4
