"""Spike: candidate "Why" images for the index page, as ternary plots (throwaway).

    PYTHONPATH=examples/adcs uv run --with mpltern python docs/superpowers/notes/spike-ternary/make_why.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpltern  # noqa: F401
import numpy as np

import case
from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

OUT = Path(__file__).parent
C = ["#0072B2", "#E69F00", "#009E73"]          # the palette of the three-pane figure
GREY = "#b5b5b5"


def close(x):
    x = np.asarray(x, float)
    return x / x.sum(axis=-1, keepdims=True)


def tern(fig, pos, labels):
    ax = fig.add_subplot(pos, projection="ternary")
    ax.set_tlabel(labels[0]); ax.set_llabel(labels[1]); ax.set_rlabel(labels[2])
    for a in (ax.taxis, ax.laxis, ax.raxis):
        a.set_label_position("corner"); a.set_ticks([]); a.label.set_fontsize(12); a.label.set_fontweight("bold")
    return ax


# ---- Y1: schematic, three metrics, three facets: what trades depends on where you are
X, info = make_frontier_data(900, 3, n_terms=3, random_state=11)
ts = HyperbolicTradeSpace(n_terms=3, temperature=50.0, random_state=0).fit(X)
W = ts.exponents_
order = np.argsort(-W[:, 0])                      # stable colours
logv = ts.score_samples(X)
near = np.abs(logv) < 0.2
U = np.log(X); U = U - U.mean(1, keepdims=True); U = U - U.mean(0, keepdims=True)
comp = close(np.exp(U / (2.0 * U.std())))

fig = plt.figure(figsize=(6.4, 6.0))
ax = tern(fig, 111, ["more of metric 1", "more of metric 2", "more of metric 3"])
ax.scatter(comp[~near, 0], comp[~near, 1], comp[~near, 2], s=6, color=GREY, alpha=0.35, linewidths=0)
names = ["metric 1", "metric 2", "metric 3"]
for c, k in enumerate(order):
    m = near & (ts.facet_ == k)
    ax.scatter(comp[m, 0], comp[m, 1], comp[m, 2], s=20, color=C[c], alpha=0.9, linewidths=0)
    w = W[k]
    big = [names[j] for j in np.argsort(-w) if w[j] > 0.12]
    txt = " against ".join(big[:2]) if len(big) == 2 else ", ".join(big[:-1]) + " and " + big[-1]
    cen = comp[m].mean(0)
    ax.text(cen[0], cen[1], cen[2], f"here:\n{txt}", color="k", fontsize=9.5, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C[c], lw=1.6, alpha=0.92))
ax.set_title("What trades against what\ndepends on where a design sits", fontsize=13, pad=26)
fig.text(0.5, 0.035, "each dot is an evaluated design; colour: the trade-off that binds it at the frontier", ha="center", fontsize=9)
fig.savefig(OUT / "why-1-schematic.png", dpi=170, bbox_inches="tight")
plt.close(fig)

# ---- Y2: the cubesat itself, by subsystem
prim, stock = case.load_study("primary"), case.load_study("stock")
fits = case.k_fits(prim)
f1, f3, fs = fits[1], fits[3], case.fit_study(stock, K=1)
attrs = list(prim.attrs)
GROUPS = {
    "controls": ["slew_time_s", "settling_time_s", "pointing_error_deg", "control_effort"],
    "power": ["power_margin_w", "energy_balance_wh", "eclipse_reserve_wh", "peak_slew_power_w", "dod_eclipse"],
    "mass": ["total_mass_kg"],
}
assert sorted(sum(GROUPS.values(), [])) == sorted(attrs)
G = np.array([[a in g for a in attrs] for g in GROUPS.values()], float)
amal = lambda w: np.asarray(w) @ G.T  # noqa: E731
a1, as_, A3, sh = amal(f1.estimator.exponents_[0]), amal(fs.estimator.exponents_[0]), amal(f3.estimator.exponents_), f3.estimator.facet_share_
print("subsystem weights  primary", np.round(a1, 2), " stock", np.round(as_, 2), " facets", np.round(A3, 2).tolist(), "shares", np.round(sh, 2))

fig = plt.figure(figsize=(6.4, 6.0))
ax = tern(fig, 111, ["controls", "power", "mass"])
ax.grid(alpha=0.2)
o3 = np.argsort(sh)
for c, k in enumerate(o3):
    ax.scatter(*A3[k], s=140 + 900 * sh[k], color=C[c], alpha=0.85, zorder=3)
ax.scatter(*a1, s=170, marker="s", color="k", zorder=4)
ax.scatter(*as_, s=170, marker="s", facecolors="white", edgecolors="k", linewidths=2, zorder=4)
def note(ax, p, q, text, ha="center"):
    ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color="k", lw=0.8, zorder=2)
    ax.text(q[0], q[1], q[2], text, fontsize=9, ha=ha, va="center", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9))


note(ax, a1, (0.60, 0.10, 0.30), "one summary of the\naggressive-gain designs")
note(ax, as_, (0.74, 0.24, 0.02), "stock gains:\nmass is not in play", ha="right")
note(ax, A3[o3[-1]], (0.16, 0.38, 0.46), "most designs: all three\nsubsystems trade")
ax.set_title("One cubesat, several trade-offs:\nwhere the tension lies, by subsystem", fontsize=13, pad=26)
fig.text(0.5, 0.035, "a point near a corner: that subsystem carries the trade-off; circles: three regions of the frontier, sized by share", ha="center", fontsize=8.5)
fig.savefig(OUT / "why-2-cubesat.png", dpi=170, bbox_inches="tight")
plt.close(fig)

# ---- Y3: the familiar triangle made literal: corner, edge, interior
fig = plt.figure(figsize=(6.4, 6.0))
ax = tern(fig, 111, ["metric 1", "metric 2", "metric 3"])
pts = {"one metric binds": (0.94, 0.03, 0.03), "a dilemma:\ntwo metrics trade": (0.5, 0.5, 0.0), "a trilemma:\nall three trade": (0.36, 0.30, 0.34)}
for c, (lab, p) in enumerate(pts.items()):
    ax.scatter(*p, s=420, color=C[c], zorder=3)
    off = {0: (0.80, 0.02, 0.18), 1: (0.50, 0.68, -0.18), 2: (0.20, 0.30, 0.50)}[c]
    ax.text(*off, lab, fontsize=11, ha="center", va="center", color=C[c], fontweight="bold")
ax.set_title("Every trade-off has a place:\ncorner, edge or interior", fontsize=13, pad=26)
fig.text(0.5, 0.035, "the weights a fitted facet puts on three metrics, drawn where they sum to one", ha="center", fontsize=9)
fig.savefig(OUT / "why-3-places.png", dpi=170, bbox_inches="tight")
plt.close(fig)
print("done")
