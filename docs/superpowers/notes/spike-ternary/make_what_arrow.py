"""Spike: the three-pane figure with a black arrow in the first pane (throwaway).

    uv run python docs/superpowers/notes/spike-ternary/make_what_arrow.py <path to paper/figures>
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, sys.argv[1])
import figure1 as F  # noqa: E402

d = F.figure1_data()
us = d["u"][d["design"]]
top = us - d["logV"][d["design"]]          # uniform scaling carries the design onto the surface
fig = F.figure1()
axm = fig.axes[0]
axm.add_patch(FancyArrowPatch(np.exp(us), np.exp(top), arrowstyle="-|>", mutation_scale=11, color=F.HIGHLIGHT, lw=2.0, zorder=8))
fig.savefig(Path(__file__).parent / "what-with-arrow.png", dpi=200)
print("pane 1 arrow from", np.round(np.exp(us), 2), "to", np.round(np.exp(top), 2))
