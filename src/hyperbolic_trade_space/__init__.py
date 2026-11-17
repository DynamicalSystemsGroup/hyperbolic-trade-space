"""Hyperbolic trade space: learn the shape of a design trade space (the posynomial invariant form).

A scikit-learn estimator that fits a posynomial frontier to a table of conditioned metrics and
reports which of them trade off and how steeply.

Documentation: https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/docs/
"""

from .datasets import make_configured_frontier_data, make_frontier_data
from .estimator import HyperbolicTradeSpace
from .preconditioning import LogAffinePreconditioner, frontier_in_original_units
from .predictive import TradeSpaceRegressor
from .tensions import design_tensions, tension_matrix, trade_off_report
from .tuning import select_temperature

__version__ = "0.1.0"

__all__ = [
    "HyperbolicTradeSpace",
    "LogAffinePreconditioner",
    "TradeSpaceRegressor",
    "__version__",
    "design_tensions",
    "frontier_in_original_units",
    "make_configured_frontier_data",
    "make_frontier_data",
    "select_temperature",
    "tension_matrix",
    "trade_off_report",
]
