"""Spike, fifth pass: lines of equal V at a fixed TOTAL, not a fixed geometric mean (throwaway).

The fourth pass held the geometric mean of the metrics fixed. Each facet's log V is then linear in
the position, so V cannot peak inside the triangle: it ran off the page. A triangle is read as
shares of a total. With S the sum of the (rescaled) metrics and c = m / S the shares,

    V_k(m) = e^{-beta_k} prod_j m_j^{w_kj} = e^{-beta_k} * S * prod_j c_j^{w_kj}     (sum_j w_kj = 1)

so at a fixed total V_k peaks at c = w_k exactly: the facet's exponent vector is a point of the
triangle, and it is where that facet's V is largest.

    uv run --with mpltern python docs/superpowers/notes/spike-ternary/make_why5.py
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
logv = ts.score_samples(X)
near = np.abs(logv) < 0.2
P = U - U.mean(axis=1, keepdims=True)
colmean = P.mean(axis=0)                       # log of each metric's typical size (up to a common factor)
s_old = float(2.0 * (P - colmean).std())
print("designs: largest log V", round(float(logv.max()), 3), "share above 0.05:", round(float((logv > 0.05).mean()), 3),
      "share above 0:", round(float((logv > 0).mean()), 3))
print("true exponents", np.round(info["exponents"], 3).tolist() if isinstance(info, dict) and "exponents" in info else "n/a")
print("fitted exponents", np.round(W, 3).tolist(), "old display power s =", round(s_old, 3))

tri = int(np.argmax(W.min(axis=1)))
others = [k for k in range(3) if k != tri]
col = {tri: AMBER, others[0]: BLUE, others[1]: GREEN}
pale = lambda hx, f=0.80: tuple(f + (1 - f) * v for v in to_rgba(hx)[:3])  # noqa: E731
names = ["metric 1", "metric 2", "metric 3"]


def says(k):
    w = W[k]
    big = [j for j in np.argsort(-w) if w[j] > 0.12]
    return "all three trade" if len(big) >= 3 else f"{names[big[0]]} trades\nagainst {names[big[1]]}"


n = 300
a, b = np.meshgrid(np.linspace(0.0015, 0.997, n), np.linspace(0.0015, 0.997, n))
msk = a + b < 0.9985
t, l = a[msk], b[msk]
r = 1 - t - l
c = np.column_stack([t, l, r])


def draw(s, tag, with_designs=True):
    """Shares c_j = (m_j / typical_j)^(1/s) / L, L their sum; the level is s log L. s = 1 is the plain sum."""
    Y = np.exp((U - colmean) / s)
    L = Y.sum(axis=1)
    comp = Y / L[:, None]
    lev = s * np.log(L)
    ak = W @ colmean - beta                                   # facet constants in these units
    Fd = ak[None, :] + s * (np.log(comp) @ W.T)
    assert np.abs(lev + Fd.max(axis=1) - logv).max() < 1e-10  # log V = level + f(position), exactly
    G = ak[None, :] + s * (np.log(c) @ W.T)
    f = G.max(axis=1)
    region = G.argmax(axis=1)
    peak = ak + s * (np.log(np.clip(W, 1e-300, None)) * W).sum(axis=1)   # facet k's own value at c = w_k
    own = [int(np.argmax(ak + s * (np.log(np.clip(W[k], 1e-300, None)) @ W.T))) for k in range(3)]
    top = float(max(peak[k] for k in range(3) if own[k] == k)) if any(own[k] == k for k in range(3)) else float(f.max())
    print(f"[{tag}] s={s:.3f}  facet peak (log V - level) {np.round(peak, 3).tolist()}  region at each facet's own exponent vector {own}")
    fig = plt.figure(figsize=(7.4, 6.2))
    ax = fig.add_axes([0.17, 0.10, 0.66, 0.80], projection="ternary")
    for axis in (ax.taxis, ax.laxis, ax.raxis):
        axis.set_ticks([]); axis.set_label_position("corner"); axis.set_label_rotation_mode("horizontal")
        axis.label.set_fontsize(14); axis.label.set_fontweight("bold"); axis.label.set_color(INK)
    ax.set_tlabel("favours metric 1"); ax.set_llabel("favours\nmetric 2"); ax.set_rlabel("favours\nmetric 3")
    for sp in ax.spines.values():
        sp.set_linewidth(1.4); sp.set_color(INK)
    ax.tripcolor(t, l, r, region, cmap=ListedColormap([pale(col[k]) for k in range(3)]), vmin=-0.5, vmax=2.5,
                 shading="flat", rasterized=True, zorder=0)
    if with_designs:
        ax.scatter(comp[~near, 0], comp[~near, 1], comp[~near, 2], s=6, color="#7d7d7d", alpha=0.45, linewidths=0, zorder=2)
        for k in range(3):
            mk = near & (ts.facet_ == k)
            ax.scatter(comp[mk, 0], comp[mk, 1], comp[mk, 2], s=22, color=col[k], linewidths=0.5, edgecolors="white", zorder=3)
    ratios = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.97])           # V as a fraction of the highest peak
    ax.tricontour(t, l, r, f - top, levels=np.log(ratios), colors=[INK], linewidths=1.0, linestyles="solid", zorder=4)
    for k in range(3):                                                     # each facet's exponent vector, as a point
        ax.scatter([W[k, 0]], [W[k, 1]], [W[k, 2]], marker="*", s=420, color=col[k], edgecolors=INK, linewidths=1.4, zorder=8, clip_on=False)
    fig.savefig(OUT / f"why5-{tag}.png", dpi=170)
    plt.close(fig)
    return comp


draw(1.0, "A-fixed-total")
draw(1.0, "B-fixed-total-map", with_designs=False)
draw(s_old, "C-fixed-total-old-spread")
