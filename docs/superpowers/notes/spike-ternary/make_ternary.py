"""Spike: ternary plots for reading tensions (throwaway; not package code).

    PYTHONPATH=examples/adcs uv run --with mpltern python docs/superpowers/notes/spike-ternary/make_ternary.py

Draws four figures beside this file. mpltern is not a project dependency; the spike borrows it.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpltern  # noqa: F401  (registers the "ternary" projection)
import numpy as np

import case
from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

OUT = Path(__file__).parent
FACET = ["#1b9e77", "#d95f02", "#7570b3"]
GREY = "#9a9a9a"


def tern(fig, pos, labels, title=None):
    ax = fig.add_subplot(pos, projection="ternary")
    ax.set_tlabel(labels[0]); ax.set_llabel(labels[1]); ax.set_rlabel(labels[2])
    ax.taxis.set_label_position("corner"); ax.laxis.set_label_position("corner"); ax.raxis.set_label_position("corner")
    ax.grid(alpha=0.25)
    for a in (ax.taxis, ax.laxis, ax.raxis):
        a.set_ticks([0.2, 0.4, 0.6, 0.8])
        a.set_tick_params(labelsize=7)
    if title:
        ax.set_title(title, pad=22, fontsize=11)
    return ax


def close(x):
    x = np.asarray(x, float)
    return x / x.sum(axis=-1, keepdims=True)


def centred(M, scale=None):
    """Compositions of metrics, centred (and scaled) in log-ratio space so the cloud fills the triangle."""
    U = np.log(M)
    U = U - U.mean(axis=1, keepdims=True)           # remove the overall level: position only
    U = U - U.mean(axis=0, keepdims=True)           # centre the cloud (perturbation by the centre)
    s = scale or (2.0 * U.std())
    return close(np.exp(U / s)), s


# ---------------------------------------------------------------- figure A: a planted three-metric table
X, info = make_frontier_data(600, 3, n_terms=3, random_state=11)
ts = HyperbolicTradeSpace(n_terms=3, temperature=50.0, random_state=0).fit(X)
W = ts.exponents_
Wp = np.asarray(info["exponents"]) if "exponents" in info else None
logv = ts.score_samples(X)
near = np.abs(logv) < 0.15
print("A planted", None if Wp is None else np.round(Wp, 2).tolist(), "fitted", np.round(W, 2).tolist(), "status", ts.termination_.status)

fig = plt.figure(figsize=(11, 5.2))
ax = tern(fig, 121, ["metric 0", "metric 1", "metric 2"], "What contends: each facet's exponents")
if Wp is not None:
    ax.scatter(Wp[:, 0], Wp[:, 1], Wp[:, 2], s=170, facecolors="none", edgecolors="k", linewidths=1.3, label="planted")
for k in range(3):
    ax.scatter(W[k, 0], W[k, 1], W[k, 2], s=90, color=FACET[k], zorder=3, label=f"fitted facet {k + 1}")
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.12, 1.08))
ax.text(0.5, -0.13, "corner: one metric binds   edge: a dilemma   interior: a trilemma", transform=ax.transAxes, ha="center", fontsize=8.5)

comp, s = centred(X)
ax = tern(fig, 122, ["metric 0", "metric 1", "metric 2"], "Where designs sit: balance of the metrics")
ax.scatter(comp[~near, 0], comp[~near, 1], comp[~near, 2], s=5, color=GREY, alpha=0.35, linewidths=0)
for k in range(3):
    m = near & (ts.facet_ == k)
    ax.scatter(comp[m, 0], comp[m, 1], comp[m, 2], s=14, color=FACET[k], alpha=0.9, linewidths=0, label=f"near the frontier, facet {k + 1}")
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.14, 1.08))
ax.text(0.5, -0.13, "grey: designs inside the frontier (their level is not shown here)", transform=ax.transAxes, ha="center", fontsize=8.5)
fig.tight_layout()
fig.savefig(OUT / "A-planted.png", dpi=160)
plt.close(fig)

# ---------------------------------------------------------------- the cubesat fits
prim = case.load_study("primary")
stock = case.load_study("stock")
fits = case.k_fits(prim)                       # K = 1, 2, 3
f1, f3 = fits[1], fits[3]
fs = case.fit_study(stock, K=1)
names = prim.names
attrs = list(prim.attrs)
print("attrs", attrs)
w1 = f1.estimator.exponents_[0]
ws = fs.estimator.exponents_[0]
W3 = f3.estimator.exponents_
share3 = f3.estimator.facet_share_
print("K=1 primary", dict(zip(names, np.round(w1, 3))))
print("K=1 stock  ", dict(zip(names, np.round(ws, 3))))
for k in range(3):
    print(f"K=3 facet {k + 1} share {share3[k]:.2f}", dict(zip(names, np.round(W3[k], 3))))

GROUPS = {
    "performance\n(slew, settling, pointing)": ["slew_time_s", "settling_time_s", "pointing_error_deg"],
    "energy\n(effort, margins, reserve)": ["control_effort", "power_margin_w", "energy_balance_wh", "eclipse_reserve_wh", "peak_slew_power_w", "dod_eclipse"],
    "mass": ["total_mass_kg"],
}
assert sorted(sum(GROUPS.values(), [])) == sorted(attrs), (sorted(sum(GROUPS.values(), [])), sorted(attrs))
G = np.array([[a in g for a in attrs] for g in GROUPS.values()], float)   # 3 x d


def amal(w):
    return np.asarray(w) @ G.T


# temperature path of the one-facet fit
taus = [*np.geomspace(*prim.spec.tau_bounds, 14), np.inf]
path = np.array([HyperbolicTradeSpace(temperature=t, random_state=prim.spec.seed).fit(prim.M).exponents_[0] for t in taus])

# ---------------------------------------------------------------- figure B: ten metrics amalgamated into three groups
fig = plt.figure(figsize=(11, 5.4))
labels = list(GROUPS)
ax = tern(fig, 121, labels, "Cubesat: where the weight of each tension lies")
a1, as_, A3 = amal(w1), amal(ws), amal(W3)
ax.scatter(*a1, s=150, marker="s", color="k", zorder=4, label="one facet, primary regime")
ax.scatter(*as_, s=150, marker="s", facecolors="none", edgecolors="k", linewidths=1.6, zorder=4, label="one facet, stock regime")
for k in range(3):
    ax.scatter(*A3[k], s=80 + 600 * share3[k], color=FACET[k], alpha=0.9, zorder=3, label=f"facet {k + 1} of three (share {share3[k]:.2f})")
ax.legend(fontsize=7.5, loc="upper right", bbox_to_anchor=(1.2, 1.1))
ax.text(0.5, -0.16, "exponents summed within each group; marker area follows the facet's share", transform=ax.transAxes, ha="center", fontsize=8.5)

ax = tern(fig, 122, labels, "The same fit as the maximum hardens")
P = amal(path)
ax.plot(P[:, 0], P[:, 1], P[:, 2], color="k", lw=1.2)
ax.scatter(P[:-1, 0], P[:-1, 1], P[:-1, 2], c=np.log10(taus[:-1]), cmap="viridis", s=28, zorder=3)
ax.scatter(*P[-1], s=140, marker="*", color="crimson", zorder=4, label="exact maximum")
ax.scatter(*a1, s=110, marker="s", color="k", zorder=4, label=f"selected temperature ({f1.tau:.0f})")
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.12, 1.08))
ax.text(0.5, -0.16, "one-facet fit from soft (dark) to hard (light) temperature", transform=ax.transAxes, ha="center", fontsize=8.5)
fig.tight_layout()
fig.savefig(OUT / "B-cubesat-groups.png", dpi=160)
plt.close(fig)
print("B amalgamated K=1 primary", np.round(a1, 3), "stock", np.round(as_, 3), "K=3", np.round(A3, 3).tolist())

# ---------------------------------------------------------------- figure C: a sub-composition (the three metrics both regimes share)
trio = ["slew_time_s", "pointing_error_deg", "control_effort"]
idx = [attrs.index(a) for a in trio]
tl = [names[i] for i in idx]


def sub(w):
    w = np.asarray(w)[..., idx]
    return close(w), w.sum(axis=-1)


fig = plt.figure(figsize=(11, 5.4))
ax = tern(fig, 121, tl, "Exchange rates among three metrics")
for w, kw, lab in [(w1, dict(marker="s", color="k"), "one facet, primary"), (ws, dict(marker="s", facecolors="none", edgecolors="k", linewidths=1.6), "one facet, stock")]:
    c, tot = sub(w)
    ax.scatter(*c, s=150, zorder=4, label=f"{lab} (these three carry {tot:.2f})", **kw)
for k in range(3):
    c, tot = sub(W3[k])
    ax.scatter(*c, s=80 + 600 * share3[k], color=FACET[k], alpha=0.9, zorder=3, label=f"facet {k + 1} (carry {tot:.2f})")
ax.legend(fontsize=7.5, loc="upper right", bbox_to_anchor=(1.22, 1.1))
ax.text(0.5, -0.16, "a point's distances to two sides are in the ratio of the two exponents:\nthe exchange rate between those metrics", transform=ax.transAxes, ha="center", fontsize=8.5)

lv = f3.estimator.score_samples(prim.M)
nr = np.abs(lv) < 1.0 / f3.tau
lab3 = f3.estimator.facet_
comp, s = centred(prim.M[:, idx])
ax = tern(fig, 122, tl, "Cubesat designs: balance of the same three")
ax.scatter(comp[~nr, 0], comp[~nr, 1], comp[~nr, 2], s=5, color=GREY, alpha=0.3, linewidths=0)
for k in range(3):
    m = nr & (lab3 == k)
    ax.scatter(comp[m, 0], comp[m, 1], comp[m, 2], s=22, color=FACET[k], alpha=0.95, linewidths=0, label=f"near the frontier, facet {k + 1} ({m.sum()})")
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.14, 1.08))
ax.text(0.5, -0.16, "conditioned metrics, centred and scaled in log-ratio space", transform=ax.transAxes, ha="center", fontsize=8.5)
fig.tight_layout()
fig.savefig(OUT / "C-cubesat-three-metrics.png", dpi=160)
plt.close(fig)

# ---------------------------------------------------------------- figure D: stability drawn where it lives (bootstrap of the three-facet exponents)
rng = np.random.default_rng(0)
fig = plt.figure(figsize=(5.8, 5.4))
ax = tern(fig, 111, labels, "How firm is each facet? 40 resamples")
ref = W3
n = prim.M.shape[0]
for b in range(40):
    Xb = prim.M[rng.integers(0, n, n)]
    e = HyperbolicTradeSpace(n_terms=3, temperature=f3.tau, random_state=prim.spec.seed).fit(Xb)
    Wb = e.exponents_
    # match resampled facets to the reference facets by nearest exponents
    from itertools import permutations
    perm = min(permutations(range(3)), key=lambda p: sum(np.abs(Wb[list(p)] - ref).sum(axis=1)))
    A = amal(Wb[list(perm)])
    for k in range(3):
        ax.scatter(*A[k], s=12, color=FACET[k], alpha=0.45, linewidths=0)
for k in range(3):
    ax.scatter(*A3[k], s=120, color=FACET[k], edgecolors="k", linewidths=1.0, zorder=4, label=f"facet {k + 1}")
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.12, 1.08))
fig.tight_layout()
fig.savefig(OUT / "D-cubesat-stability.png", dpi=160)
plt.close(fig)
print("done")
