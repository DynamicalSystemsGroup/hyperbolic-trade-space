"""Hyperbolic trade space: learn the shape of a design trade space (the posynomial invariant form).

Package code arrives in later work packages (see ``work-packages/README.md``).
"""

from .datasets import make_configured_frontier_data, make_frontier_data
from .estimator import HyperbolicTradeSpace
from .preconditioning import LogAffinePreconditioner, frontier_in_original_units
from .tensions import tension_report
from .predictive import TradeSpaceRegressor
from .tuning import select_temperature

__version__ = "0.0.1"

__all__ = [
    "HyperbolicTradeSpace",
    "LogAffinePreconditioner",
    "TradeSpaceRegressor",
    "__version__",
    "frontier_in_original_units",
    "make_configured_frontier_data",
    "make_frontier_data",
    "select_temperature",
    "tension_report",
]
