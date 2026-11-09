"""Candidate redraws of Figure 7 (plot_frontier_coordinates, the cubesat one-term fit).

    uv run python docs/superpowers/notes/figure-candidates/figure7_candidates.py

Writes fig7-a-depth.png, fig7-b-principal.png, fig7-c-stripes.png beside this script, from the
committed aggressive-gains table (examples/adcs/case.py), deterministic. Nothing here is on a page.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "examples" / "adcs"))
import case  # noqa: E402

from hyperbolic_trade_space.plotting import plot_frontier_coordinates  # noqa: E402

BLUE, ORANGE, GREY = "#0072B2", "#D55E00", "#bbbbbb"
SIZE, DPI = (7.0, 4.2), 110

study = case.load_study("primary")
fit = case.fit_study(study, K=1)
chart = fit.estimator.transform(study.M)
Z, logv = chart[:, :-1], chart[:, -1]
band_docs = (
    0.1  # the band the present figure rings with (the plotting default)
)

# (a) depth against one position coordinate: the frontier is the line log V = 0.
fig, ax = plt.subplots(figsize=SIZE)
plot_frontier_coordinates(Z[:, :1], logv, band=band_docs, ax=ax)
ax.set_xlabel(
    "Z0 (a position along the frontier; its meaning is the basis's, not a metric's)"
)
ax.set_ylabel("log V (0 = on the frontier, negative = inside)")
ax.set_title(
    f"{len(Z)} designs; {int((logv >= -band_docs).sum())} within {band_docs} of the frontier",
    fontsize=10,
)
ax.legend(loc="lower left", fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig7-a-depth.png", dpi=DPI)
plt.close(fig)

# (b) near-frontier designs in their two leading principal directions, axes named by loadings.
rep = case._reports(study, fit)[0]
D = np.asarray(rep.tension_directions)
load = np.asarray(rep.tension_loadings, float)
near = logv >= -fit.band
mu = Z[near].mean(0)
S = (Z - mu) @ D[:2].T
names = study.names


def axis_name(i):
    row = load[i]
    row = row if row[np.argmax(np.abs(row))] > 0 else -row
    sign = 1 if load[i][np.argmax(np.abs(load[i]))] > 0 else -1
    S[:, i] *= sign
    top = np.argsort(-np.abs(row))[:3]
    share = rep.explained_spread[i]
    return f"direction {i + 1} ({share:.0%} of spread): " + ", ".join(
        f"{names[j]} {row[j]:+.2f}" for j in top
    )


xl, yl = axis_name(0), axis_name(1)
fig, ax = plt.subplots(figsize=SIZE)
ax.scatter(
    S[~near, 0],
    S[~near, 1],
    s=10,
    c=GREY,
    label=f"other designs ({(~near).sum()})",
)
ax.scatter(
    S[near, 0],
    S[near, 1],
    s=22,
    c=BLUE,
    edgecolors="black",
    linewidths=0.5,
    label=f"within {fit.band:.3f} of the frontier ({near.sum()})",
)
ax.set_xlabel(xl, fontsize=7.5)
ax.set_ylabel("\n".join(yl.split(": ")), fontsize=7.5)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig7-b-principal.png", dpi=DPI)
plt.close(fig)

# (c) the present plot, coloured by the star-tracker grade (the stripes), ringing as before.
grade = study.feasible["st_grade"].to_numpy()
fig, ax = plt.subplots(figsize=SIZE)
cols = {"coarse": ORANGE, "medium": "#009E73", "fine": BLUE}
nr = logv >= -band_docs
for g, col in cols.items():
    m = grade == g
    ax.scatter(
        Z[m, 0],
        Z[m, 1],
        s=14,
        c=col,
        edgecolors=np.where(nr[m], "black", "none"),
        linewidths=0.8,
        label=f"star tracker: {g}",
    )
ax.set_xlabel("Z0")
ax.set_ylabel("Z1")
ax.legend(fontsize=8, loc="lower left")
fig.tight_layout()
fig.savefig(HERE / "fig7-c-stripes.png", dpi=DPI)
plt.close(fig)

# What the data say about the stripes (printed, recorded in work-packages/WP8a-figure-review.md).
for g in cols:
    z1 = Z[grade == g, 1]
    print(
        f"st_grade {g}: n={len(z1)}, Z1 mean {z1.mean():+.2f}, sd {z1.std():.2f}"
    )
print("Z1 overall sd", round(Z[:, 1].std(), 2))
