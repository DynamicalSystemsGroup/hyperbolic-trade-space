"""Hyperbolic trade space: learn the shape of a design trade space (the posynomial invariant form).

Package code arrives in later work packages (see ``work-packages/README.md``).
"""

from .datasets import make_configured_frontier_data, make_frontier_data
from .estimator import HyperbolicTradeSpace

__version__ = "0.0.1"

__all__ = [
    "HyperbolicTradeSpace",
    "__version__",
    "make_configured_frontier_data",
    "make_frontier_data",
]
