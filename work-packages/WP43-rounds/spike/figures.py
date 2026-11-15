"""Plane figures of the spike (protocol.md, Figures): the adjusted plane per model, and the dent."""

from __future__ import annotations

import pickle
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import generators as gen  # noqa: E402
import models  # noqa: E402
import run  # noqa: E402

RES, CACHE = HERE / "results", HERE / "cache"
FIG = HERE / "figures"
INK, DESIGN, HELD = "#1c1c1c", "0.72", "0.35"
PANELS = ["K1", "K2", "K2s", "K3", "LQ", "LQm"]
PANEL_TITLE = {
    "K1": "one term (package)",
    "K1c": "one term, mean-slack fit",
    "K2": "two terms, sharp",
    "K2s": "two terms, soft",
    "K3": "three terms, sharp",
    "LQ": "one log-quadratic term",
    "LQm": "log-quadratic term, monotone",
}


def plane_panel(ax, model, M, j, held, title):
    """One panel: every design at (its first plotted metric, its level ``log V``).

    The surface is ``log V = 0``.
    """
    U = np.log(M)
    lv = model.log_v(U)
    ax.scatter(U[~held, j], lv[~held], s=5, color=DESIGN, linewidth=0, zorder=2, rasterized=True)
    ax.scatter(U[held, j], lv[held], s=5, color=HELD, linewidth=0, zorder=2.5, rasterized=True)
    ax.axhline(0.0, color=INK, lw=1.6, zorder=3)
    ax.set_title(title, fontsize=10)
    return int((~np.isfinite(lv)).sum())


def real_figure(regime):
    info = run.plane_info(regime)
    s = run.load(regime)
    M = s.M
    j = info["j"]
    _, te = next(iter(KFold(5, shuffle=True, random_state=0).split(np.arange(len(M)))))
    held = np.zeros(len(M), bool)
    held[te] = True
    fig, axes = plt.subplots(3, 2, figsize=(8, 10.6), sharex=True, sharey=True)
    nan_counts = {}
    for ax, name in zip(axes.ravel(), PANELS, strict=True):
        with open(CACHE / f"{regime}_{name}.pkl", "rb") as fh:
            model = pickle.load(fh)
        nan_counts[name] = plane_panel(ax, model, M, j, held, PANEL_TITLE[name])
    for ax in axes[-1]:
        ax.set_xlabel(f"log of the conditioned {s.names[j]}", fontsize=10)
    for ax in axes[:, 0]:
        ax.set_ylabel("level of the design, log V\n(0 is the surface)", fontsize=10)
    axes[0, 0].set_ylim(-0.7, 0.2)
    from matplotlib.lines import Line2D

    axes[0, 0].legend(
        handles=[
            Line2D([], [], marker="o", ls="", color=DESIGN, label="a design"),
            Line2D([], [], marker="o", ls="", color=HELD, label="a design held out in fold 0"),
            Line2D([], [], color=INK, label="the surface, log V = 0"),
        ],
        frameon=False,
        fontsize=8,
        loc="lower left",
    )
    fig.tight_layout()
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / f"plane_{regime}.png", dpi=100)
    plt.close(fig)
    return nan_counts


def dent_figure(seed=0):
    X, truth = gen.planted_d(seed)
    B = gen.helmert_basis(gen.D)
    zc = truth["z_c"]
    base = truth["info"]
    t_all = base["Z"] @ zc
    perp = np.linalg.norm(base["Z"] - np.outer(t_all, zc), axis=1)
    dist = np.sqrt(((base["Z"] - zc) ** 2).sum(axis=1) + base["log_v"] ** 2)
    sel = perp < 0.5
    gone = dist < gen.RHO
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.scatter(
        t_all[sel & ~gone], base["log_v"][sel & ~gone], s=16, color=DESIGN, linewidth=0, zorder=2
    )
    ax.scatter(
        t_all[sel & gone],
        base["log_v"][sel & gone],
        s=22,
        facecolor="none",
        edgecolor=INK,
        linewidth=0.8,
        zorder=2.5,
    )
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(1 + gen.RHO * np.cos(th), gen.RHO * np.sin(th), color=INK, lw=0.9, ls=":", zorder=3)
    t = np.linspace(-2.5, 3.0, 200)
    pts = np.outer(t, zc) @ B
    pts = (
        pts + (0.0 - pts @ truth["w"])[:, None]
    )  # on the truth's frontier along the line through z_c
    styles = {"K1": ("-", 1.6), "K3": ("--", 1.4), "LQ": ("-.", 1.4)}
    for name, (ls, lw) in styles.items():
        m, *_ = models.fit_model(name, X, sharp=True)
        ax.plot(
            t,
            m.log_v(pts),
            color=INK,
            ls=ls,
            lw=lw,
            zorder=4,
            label=PANEL_TITLE[name] + " (the fits coincide)",
        )
    ax.scatter(
        [],
        [],
        s=22,
        facecolor="none",
        edgecolor=INK,
        linewidth=0.8,
        label="a row removed, with the ball's rim dotted",
    )
    ax.set_ylim(-3.2, 0.9)
    ax.set_xlim(-2.5, 3.0)
    ax.set_xlabel("position along the direction of the removed ball's centre, in chart units")
    ax.set_ylabel("level log V of the planted truth\n(and of each fit along the truth's edge)")
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    ax.set_title("the removed ball leaves a notch the fits pass over", fontsize=10)
    fig.tight_layout()
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / "dent.png", dpi=100)
    plt.close(fig)


def main():
    for r in run.REGIMES:
        if (CACHE / f"{r}_K1.pkl").exists():
            print(r, "undefined designs per panel:", real_figure(r))
    dent_figure()


if __name__ == "__main__":
    main()
