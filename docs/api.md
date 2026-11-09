# API

The public interface, by what each name is for. The [API reference](api-reference.md) renders the
numpydoc docstrings of every name; the [user guide](user-guide/overview.md) shows them in use. The
package follows the scikit-learn conventions [@pedregosa2011scikit; @buitinck2013api]: parameters
stored verbatim, validation in `fit`, fitted attributes ending in an underscore. Dimension is
arbitrary: `d` metrics and `d - 1` chart coordinates.

| Name | Kind | Role | Guide |
|---|---|---|---|
| `LogAffinePreconditioner` | transformer | attributes to larger-is-better metrics, invertible | [Conditioning](user-guide/conditioning.md) |
| `frontier_in_original_units` | function | fitted surface as a monomial in raw attributes | [Conditioning](user-guide/conditioning.md) |
| `HyperbolicTradeSpace` | transformer | fit the surface; chart of position and log V | [Fitting](user-guide/fitting.md) |
| `select_temperature` | function | choose the temperature by target fraction above V = 1 | [Fitting](user-guide/fitting.md) |
| `make_frontier_data` | function | seeded synthetic data with a planted frontier | [Fitting](user-guide/fitting.md) |
| `make_configured_frontier_data` | function | the same with configuration variables | [Prediction](user-guide/prediction.md) |
| `tension_report` | function | contending set, exchange rates, tension directions | [Tensions](user-guide/tensions.md) |
| `TradeSpaceRegressor` | regressor | metrics, coordinates and novelty from configuration | [Prediction](user-guide/prediction.md) |
| `__version__` | string | package version | |

Submodules are used by import path:

- `hyperbolic_trade_space.gaps`: `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca`
  ([chart](user-guide/chart.md)).
- `hyperbolic_trade_space.tensions`: `TensionReport`, the object `tension_report` returns.
- `hyperbolic_trade_space.plotting`: `plot_tensions`, `plot_log_plane`, `plot_frontier_surface_3d`,
  `plot_frontier_coordinates`, `plot_v_by_variable`, `facet_labels`.
- `hyperbolic_trade_space.solvers`: the multi-term solver, the `Termination` record and the
  certificate functions ([Reading termination](user-guide/termination.md)).
