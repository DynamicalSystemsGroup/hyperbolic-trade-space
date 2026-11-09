# API

The public interface, by what each name is for. The [API reference](api-reference.md) renders the
numpydoc docstrings of every name; the [user guide](user-guide/overview.md) shows them in use. The
package follows the scikit-learn conventions [@pedregosa2011scikit; @buitinck2013api]: parameters
stored verbatim, validation in `fit`, fitted attributes ending in an underscore. Dimension is
arbitrary: `d` metrics and `d - 1` chart coordinates.

- [`LogAffinePreconditioner`](user-guide/conditioning.md), a transformer: attributes to
  larger-is-better metrics, invertible.
- [`frontier_in_original_units`](user-guide/conditioning.md), a function: the fitted surface as a
  monomial in raw attributes.
- [`HyperbolicTradeSpace`](user-guide/fitting.md), a transformer: fits the surface and gives the
  chart of position and log V. Fitted attributes for every number of terms include `exponents_`,
  `facet_`, `coefficients_`, `facet_share_`, `objective_` (what the solver minimized) and
  `mean_slack_` (the mean slack, to compare fits across numbers of terms).
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
- `__version__`: the package version.

Submodules are used by import path:

- `hyperbolic_trade_space.gaps`: `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca`
  ([chart](user-guide/chart.md)).
- `hyperbolic_trade_space.tensions`: `TensionReport`, the object `tension_report` returns.
- `hyperbolic_trade_space.plotting`: `plot_tensions`, `plot_log_plane`, `plot_frontier_surface_3d`,
  `plot_frontier_coordinates`, `plot_v_by_variable`, `facet_labels`.
- `hyperbolic_trade_space.solvers`: the multi-term solver, the `Termination` record and the
  certificate functions ([Reading termination](user-guide/termination.md)).
