"""Spike, fourth pass: lines of equal V on the triangle (throwaway).

log V splits exactly into two parts: log V(m) = t + h(p), with t the mean of the log metrics (the
overall level, the direction the triangle drops) and h(p) = max_k (w_k . p - beta_k) a function of
the position in the triangle only. So V is not a function of position, but its level lines are:
the lines h = const are the lines of equal V among designs at one overall level, the same family
for every level. The frontier V = 1 sits at the level t = -h(p) above each position.

    uv run --with mpltern python docs/superpowers/notes/spike-ternary/make_why4.py
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
level = U.mean(axis=1)
P = U - level[:, None]
colmean = P.mean(axis=0, keepdims=True)
s = 2.0 * (P - colmean).std()
comp = close(np.exp((P - colmean) / s))
logv = ts.score_samples(X)
near = np.abs(logv) < 0.2
hP = (P @ W.T - beta[None, :]).max(axis=1)
assert np.abs(level + hP - logv).max() < 1e-12          # the split is exact

n = 260
a, b = np.meshgrid(np.linspace(0.002, 0.996, n), np.linspace(0.002, 0.996, n))
m = a + b < 0.998
t, l = a[m], b[m]
r = 1 - t - l
c = np.column_stack([t, l, r])
clr = np.log(c) - np.log(c).mean(axis=1, keepdims=True)
p = s * clr + colmean
G = p @ W.T - beta[None, :]
region = np.argmax(G, axis=1)
h = G.max(axis=1)
h0 = float((colmean @ W.T - beta[None, :]).max())        # the average mix (the centre of the triangle)
rel = h - h0                                             # log V relative to the average mix, same overall level

tri = int(np.argmax(W.min(axis=1)))
others = [k for k in range(3) if k != tri]
col = {tri: AMBER, others[0]: BLUE, others[1]: GREEN}
pale = lambda hx, f=0.80: tuple(f + (1 - f) * v for v in to_rgba(hx)[:3])  # noqa: E731
names = ["metric 1", "metric 2", "metric 3"]
STEP = 0.25
levels = np.arange(-0.5, 1.5 + 1e-9, STEP)


def says(k):
    w = W[k]
    big = [j for j in np.argsort(-w) if w[j] > 0.12]
    return "all three trade" if len(big) >= 3 else f"{names[big[0]]} trades\nagainst {names[big[1]]}"


def frame(figsize=(7.4, 6.2)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0.17, 0.10, 0.66, 0.80], projection="ternary")
    for axis in (ax.taxis, ax.laxis, ax.raxis):
        axis.set_ticks([]); axis.set_label_position("corner"); axis.set_label_rotation_mode("horizontal")
        axis.label.set_fontsize(14); axis.label.set_fontweight("bold"); axis.label.set_color(INK)
    ax.set_tlabel("favours metric 1"); ax.set_llabel("favours\nmetric 2"); ax.set_rlabel("favours\nmetric 3")
    for sp in ax.spines.values():
        sp.set_linewidth(1.4); sp.set_color(INK)
    return fig, ax


def regions(ax):
    cm = ListedColormap([pale(col[k]) for k in range(3)])
    ax.tripcolor(t, l, r, region, cmap=cm, vmin=-0.5, vmax=2.5, shading="flat", rasterized=True, zorder=0)


def lines(ax, color=INK, lw=1.0, zero_lw=2.2):
    cs = ax.tricontour(t, l, r, rel, levels=levels, colors=[color], linewidths=lw, linestyles="solid", zorder=4)
    ax.tricontour(t, l, r, rel, levels=[0.0], colors=[color], linewidths=zero_lw, linestyles="solid", zorder=4)
    return cs


def xy(q):
    q = np.asarray(q, float)
    return q[..., 2] + 0.5 * q[..., 0], np.sqrt(3) / 2 * q[..., 0]


def arrow(ax, start, end, text, dy=0.045):
    """A black arrow across the lines, in the direction V rises at one overall level."""
    (x0, y0), (x1, y1) = xy(start), xy(end)
    ang = np.degrees(np.arctan2(y1 - y0, x1 - x0))
    ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], color=INK, lw=2.6, zorder=7, solid_capstyle="butt")
    ax.plot([end[0]], [end[1]], [end[2]], marker=(3, 0, ang - 90), ms=13, color=INK, zorder=8)
    mid = (np.asarray(start) + np.asarray(end)) / 2 + np.array([dy, -dy / 2, -dy / 2])
    ax.text(mid[0], mid[1], mid[2], text, ha="center", va="bottom", fontsize=11.5, fontweight="bold", color=INK,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9), zorder=9)


ARROW = ((0.30, 0.28, 0.42), (0.30, 0.07, 0.63))

# ---- A: the chosen image with the lines of equal V drawn over the regions
fig, ax = frame()
regions(ax)
ax.scatter(comp[~near, 0], comp[~near, 1], comp[~near, 2], s=6, color="#7d7d7d", alpha=0.45, linewidths=0, zorder=2)
for k in range(3):
    mk = near & (ts.facet_ == k)
    ax.scatter(comp[mk, 0], comp[mk, 1], comp[mk, 2], s=22, color=col[k], linewidths=0.5, edgecolors="white", zorder=3)
lines(ax)
arrow(ax, *ARROW, "V rises")
fig.savefig(OUT / "why4-A-lines-on-regions.png", dpi=170)
plt.close(fig)

# ---- B: the lines alone on the regions, no designs: the triangle as a map of the method
fig, ax = frame()
regions(ax)
lines(ax)
arrow(ax, *ARROW, "V rises")
spot = {"all three trade": (0.62, 0.31, 0.07), "against metric 1": (0.50, 0.03, 0.47), "against metric 2": (0.06, 0.52, 0.42)}
for k in range(3):
    txt = says(k)
    cen = next(v for key, v in spot.items() if key in txt.replace("\n", " "))
    ax.text(cen[0], cen[1], cen[2], txt, ha="center", va="center", fontsize=11, fontweight="bold", color=INK,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=col[k], lw=2.0), zorder=9)
fig.savefig(OUT / "why4-B-lines-only.png", dpi=170)
plt.close(fig)

# ---- C: every design coloured by its own log V over the lines: position does not fix V
fig, ax = frame(figsize=(8.2, 6.2))
ax.tricontour(t, l, r, rel, levels=levels, colors=["#9a9a9a"], linewidths=0.9, linestyles="solid", zorder=1)
order = np.argsort(-logv)
sc = ax.scatter(comp[order, 0], comp[order, 1], comp[order, 2], c=np.clip(logv[order], -2.5, 0.0), cmap="cividis",
                s=20, linewidths=0.3, edgecolors="white", zorder=3)
cax = fig.add_axes([0.89, 0.25, 0.022, 0.5])
cb = fig.colorbar(sc, cax=cax)
cb.set_label("log V of the design\n(0 = on the frontier)", fontsize=10)
fig.savefig(OUT / "why4-C-designs-by-logV.png", dpi=170, bbox_inches="tight")
plt.close(fig)

# ---- E: the same map in log-ratio coordinates, where the method is straight: each region is a
# polygon, and inside it the lines of equal V are parallel and evenly spaced (one exponent vector)
ex = lambda q: (q[..., 2] - q[..., 1]) / np.sqrt(2)                       # noqa: E731  right = metric 3
ey = lambda q: (2 * q[..., 0] - q[..., 1] - q[..., 2]) / np.sqrt(6)       # noqa: E731  up = metric 1
Q = P - colmean
rad = float(np.percentile(np.hypot(ex(Q), ey(Q)), 97))
g = np.linspace(-rad, rad, 500)
gx, gy = np.meshgrid(g, g)
q = np.stack([2 * gy / np.sqrt(6), -gx / np.sqrt(2) - gy / np.sqrt(6), gx / np.sqrt(2) - gy / np.sqrt(6)], axis=-1)
Gs = (q + colmean) @ W.T - beta
relE = Gs.max(axis=-1) - h0
regE = Gs.argmax(axis=-1)
fig, ax = plt.subplots(figsize=(7.0, 6.6))
ax.imshow(regE, extent=[-rad, rad, -rad, rad], origin="lower", cmap=ListedColormap([pale(col[k]) for k in range(3)]),
          vmin=-0.5, vmax=2.5, interpolation="nearest", zorder=0)
lev = np.arange(np.floor(relE.min() / STEP) * STEP, relE.max(), STEP)
cs = ax.contour(gx, gy, relE, levels=lev, colors=[INK], linewidths=1.0, linestyles="solid", zorder=4)
ax.contour(gx, gy, relE, levels=[0.0], colors=[INK], linewidths=2.2, linestyles="solid", zorder=4)
ax.clabel(cs, levels=[v for v in lev if abs(v / 0.5 - round(v / 0.5)) < 1e-9], fmt=lambda v: f"{v:+.1f}" if abs(v) > 1e-9 else "0", fontsize=9.5, inline=True)
ins = (np.abs(ex(Q)) < rad) & (np.abs(ey(Q)) < rad)
ax.scatter(ex(Q)[ins & ~near], ey(Q)[ins & ~near], s=6, color="#7d7d7d", alpha=0.45, linewidths=0, zorder=2)
for k in range(3):
    mk = ins & near & (ts.facet_ == k)
    ax.scatter(ex(Q)[mk], ey(Q)[mk], s=22, color=col[k], linewidths=0.5, edgecolors="white", zorder=3)
# the three directions of the triangle, as a compass in the corner
cx, cy, L = -0.74 * rad, 0.70 * rad, 0.17 * rad
for j, lab in enumerate(["metric 1", "metric 2", "metric 3"]):
    d = np.zeros(3); d[j] = 1.0; d -= 1 / 3
    dx, dy = float(ex(d)), float(ey(d)); nrm = np.hypot(dx, dy)
    ax.annotate("", xy=(cx + L * dx / nrm, cy + L * dy / nrm), xytext=(cx, cy), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6), zorder=9)
    ax.text(cx + 1.45 * L * dx / nrm, cy + 1.45 * L * dy / nrm, lab, ha="center", va="center", fontsize=10, fontweight="bold", color=INK,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85), zorder=9)
ax.set_xlim(-rad, rad); ax.set_ylim(-rad, rad); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_linewidth(1.2); sp.set_color(INK)
fig.savefig(OUT / "why4-E-log-ratio-plane.png", dpi=170, bbox_inches="tight")
plt.close(fig)

print("exponents", np.round(W, 3).tolist())
print("range of rel over the cloud (5..95%)", np.percentile(hP - h0, [5, 50, 95]).round(2).tolist(), "step", STEP)
print("line spacing per region (in log-ratio units), step / |w_k - 1/3|:", [round(float(STEP / np.linalg.norm(W[k] - 1 / 3)), 3) for k in range(3)])
