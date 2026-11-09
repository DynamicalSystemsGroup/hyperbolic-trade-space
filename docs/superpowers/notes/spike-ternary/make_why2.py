"""Spike, second pass: Why images that carry the top-level story (throwaway).

    PYTHONPATH=examples/adcs uv run --with mpltern python docs/superpowers/notes/spike-ternary/make_why2.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpltern  # noqa: F401
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

import case

OUT = Path(__file__).parent
BLUE, AMBER, GREEN, INK = "#0072B2", "#E69F00", "#009E73", "#1a1a1a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})


def close(x):
    x = np.asarray(x, float)
    return x / x.sum(axis=-1, keepdims=True)


def triangle(fig, rect, corners):
    ax = fig.add_axes(rect, projection="ternary")
    for a, lab in zip((ax.taxis, ax.laxis, ax.raxis), corners):
        a.set_ticks([])
        a.set_label_position("corner")
        a.set_label_rotation_mode("horizontal")
        a.label.set_fontsize(15)
        a.label.set_fontweight("bold")
        a.label.set_color(INK)
    ax.set_tlabel(corners[0]); ax.set_llabel(corners[1]); ax.set_rlabel(corners[2])
    ax.set_facecolor("#f6f4ef")
    for s in ax.spines.values():
        s.set_linewidth(1.4); s.set_color(INK)
    return ax


prim = case.load_study("primary")
fits = case.k_fits(prim)
f1, f3 = fits[1], fits[3]
attrs = list(prim.attrs)
GROUPS = {
    "controls": ["slew_time_s", "settling_time_s", "pointing_error_deg", "control_effort"],
    "power": ["power_margin_w", "energy_balance_wh", "eclipse_reserve_wh", "peak_slew_power_w", "dod_eclipse"],
    "mass": ["total_mass_kg"],
}
U = np.log(prim.M)
S = np.column_stack([U[:, [attrs.index(a) for a in g]].mean(axis=1) for g in GROUPS.values()])  # log of each subsystem's geometric mean
P = S - S.mean(axis=1, keepdims=True)
P = P - P.mean(axis=0, keepdims=True)
comp = close(np.exp(P / (1.6 * P.std())))
lv = f1.estimator.score_samples(prim.M)                      # energy differential at one facet
q = np.clip((lv - np.quantile(lv, 0.05)) / (0.0 - np.quantile(lv, 0.05)), 0, 1)   # 0 far inside, 1 at the surface
near = np.abs(lv) < 1.5 / f1.tau
print("designs", len(lv), "near the frontier", int(near.sum()), "log V range", round(lv.min(), 2), round(lv.max(), 2))

# ---------- A: no single best design
cmap = LinearSegmentedColormap.from_list("ink", ["#d9d4c7", "#8f8a7c", INK])
fig = plt.figure(figsize=(7.2, 6.4))
ax = triangle(fig, [0.1, 0.12, 0.8, 0.72], ["controls", "power", "mass"])
o = np.argsort(q)
ax.scatter(comp[o, 0], comp[o, 1], comp[o, 2], c=q[o], cmap=cmap, s=14 + 26 * q[o] ** 2, linewidths=0, alpha=0.9)
ax.scatter(comp[near, 0], comp[near, 1], comp[near, 2], s=95, facecolors="none", edgecolors=AMBER, linewidths=1.8, zorder=4)
fig.text(0.5, 0.955, "No single best design", ha="center", fontsize=18, fontweight="bold", color=INK)
fig.text(0.5, 0.905, f"{len(lv)} feasible cubesat designs, each placed by the subsystem it favours", ha="center", fontsize=11, color="#444")
fig.text(0.5, 0.055, "darker: closer to the best attainable      ringed: at the frontier, and they do not agree on what to favour", ha="center", fontsize=10, color="#333")
fig.savefig(OUT / "why2-A-no-single-best.png", dpi=170)
plt.close(fig)

# ---------- A2: the same, the frontier designs coloured by the trade-off that binds them (three facets)
lv3 = f3.estimator.score_samples(prim.M)
near3 = np.abs(lv3) < 1.5 / f3.tau
lab = f3.estimator.facet_
sh = f3.estimator.facet_share_
order = np.argsort(sh)
cols = {order[0]: BLUE, order[1]: AMBER, order[2]: GREEN}
fig = plt.figure(figsize=(7.2, 6.4))
ax = triangle(fig, [0.1, 0.12, 0.8, 0.72], ["controls", "power", "mass"])
ax.scatter(comp[~near3, 0], comp[~near3, 1], comp[~near3, 2], color="#cfcabd", s=12, linewidths=0, alpha=0.8)
for k in order:
    m = near3 & (lab == k)
    ax.scatter(comp[m, 0], comp[m, 1], comp[m, 2], color=cols[k], s=70, linewidths=0.8, edgecolors="white", zorder=4)
fig.text(0.5, 0.955, "The best designs trade different things", ha="center", fontsize=18, fontweight="bold", color=INK)
fig.text(0.5, 0.905, f"{len(lv)} feasible cubesat designs, each placed by the subsystem it favours", ha="center", fontsize=11, color="#444")
fig.text(0.5, 0.055, "grey: inside the frontier      colour: at the frontier, by the trade-off that binds there", ha="center", fontsize=10, color="#333")
fig.savefig(OUT / "why2-A2-different-trades.png", dpi=170)
plt.close(fig)
print("near3 by facet", [int((near3 & (lab == k)).sum()) for k in order])
print("done")
