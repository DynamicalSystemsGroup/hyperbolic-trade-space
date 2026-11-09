"""Spike, third pass: the chosen Why image, iterated (throwaway).

    uv run --with mpltern python docs/superpowers/notes/spike-ternary/make_why3.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpltern  # noqa: F401
import numpy as np
from matplotlib.colors import ListedColormap, to_rgba

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

OUT = Path(__file__).parent
BLUE, AMBER, GREEN, INK = "#0072B2", "#E69F00", "#009E73", "#1a1a1a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})


def close(x):
    x = np.asarray(x, float)
    return x / x.sum(axis=-1, keepdims=True)


X, info = make_frontier_data(900, 3, n_terms=3, random_state=11)
ts = HyperbolicTradeSpace(n_terms=3, temperature=50.0, random_state=0).fit(X)
W, beta = ts.exponents_, np.asarray(ts.log_offset_).ravel()
U = np.log(X)
rowmean = U.mean(axis=1, keepdims=True)
P = U - rowmean                      # position: the level direction removed
colmean = P.mean(axis=0, keepdims=True)
s = 2.0 * (P - colmean).std()
comp = close(np.exp((P - colmean) / s))
logv = ts.score_samples(X)
near = np.abs(logv) < 0.2

# which trade-off binds at each position of the triangle (exact: argmax_k w_k.p - beta_k)
n = 220
a, b = np.meshgrid(np.linspace(0.002, 0.996, n), np.linspace(0.002, 0.996, n))
m = a + b < 0.998
t, l = a[m], b[m]
r = 1 - t - l
c = np.column_stack([t, l, r])
clr = np.log(c) - np.log(c).mean(axis=1, keepdims=True)
p = s * clr + colmean
region = np.argmax(p @ W.T - beta[None, :], axis=1)

# colours: the facet that trades all three is amber (the middle of the What figure)
tri = int(np.argmax(W.min(axis=1)))                     # the facet with every exponent well above zero
others = [k for k in range(3) if k != tri]
col = {tri: AMBER, others[0]: BLUE, others[1]: GREEN}
names = ["metric 1", "metric 2", "metric 3"]


def says(k):
    w = W[k]
    big = [j for j in np.argsort(-w) if w[j] > 0.12]
    if len(big) >= 3:
        return "all three trade"
    return f"{names[big[0]]} trades\nagainst {names[big[1]]}"


fig = plt.figure(figsize=(7.4, 6.2))
ax = fig.add_axes([0.17, 0.10, 0.66, 0.80], projection="ternary")
for axis, lab in zip((ax.taxis, ax.laxis, ax.raxis), ["favours metric 1", "favours\nmetric 2", "favours\nmetric 3"]):
    axis.set_ticks([]); axis.set_label_position("corner"); axis.set_label_rotation_mode("horizontal")
    axis.label.set_fontsize(14); axis.label.set_fontweight("bold"); axis.label.set_color(INK)
ax.set_tlabel("favours metric 1"); ax.set_llabel("favours\nmetric 2"); ax.set_rlabel("favours\nmetric 3")
for sp in ax.spines.values():
    sp.set_linewidth(1.4); sp.set_color(INK)

pale = lambda h, f=0.80: tuple(f + (1 - f) * v for v in to_rgba(h)[:3])  # noqa: E731  (blend with white, no alpha)
cm = ListedColormap([pale(col[k]) for k in range(3)])
ax.tripcolor(t, l, r, region, cmap=cm, vmin=-0.5, vmax=2.5, shading="flat", rasterized=True, zorder=0)
ax.scatter(comp[~near, 0], comp[~near, 1], comp[~near, 2], s=7, color="#7d7d7d", alpha=0.55, linewidths=0, zorder=2)
for k in range(3):
    mk = near & (ts.facet_ == k)
    ax.scatter(comp[mk, 0], comp[mk, 1], comp[mk, 2], s=30, color=col[k], linewidths=0.6, edgecolors="white", zorder=3)

# one label per region, set where the region has few designs, on a white plate
spot = {"all three trade": (0.60, 0.33, 0.07), "against metric 1": (0.34, 0.05, 0.61), "against metric 2": (0.05, 0.50, 0.45)}
for k in range(3):
    txt = says(k)
    cen = next(v for key, v in spot.items() if key in txt.replace("\n", " "))
    ax.text(cen[0], cen[1], cen[2], txt, ha="center", va="center", fontsize=11.5, fontweight="bold", color=INK,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=col[k], lw=2.0), zorder=6)

fig.savefig(OUT / "why3-regions.png", dpi=170)
plt.close(fig)
print("exponents", np.round(W, 2).tolist(), "labels", [says(k).replace("\n", " ") for k in range(3)], "region shares", [round(float((region == k).mean()), 2) for k in range(3)])
