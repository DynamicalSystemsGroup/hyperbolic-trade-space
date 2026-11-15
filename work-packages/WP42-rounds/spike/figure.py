"""The term's tension matrix, drawn per term (the redraw of Figure 7), and the figure before.

    MPLCONFIGDIR=$(mktemp -d) uv run --frozen python work-packages/WP42-rounds/spike/figure.py

Writes into ``images/``: ``before.png`` (Figure 7 as it stands on dev), ``after-replace.png``
(the tension matrix per term, in place of the correlations), ``after-beside.png`` (both, side
by side, at a width the page column does not hold: the evidence for the option that replaces)
and ``after-replace-dark.png``.

Recipe: ``figure-review.md`` (the loop is ``docs/superpowers/notes/figure-review.md``).
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "examples" / "adcs"))
sys.path.insert(0, str(HERE))

import case  # noqa: E402
import prototype as P  # noqa: E402
from case_run import load  # noqa: E402

IMG = HERE / "images"
CMAP = "BrBG"  # diverging about |tension| = 1; not the association figure's PuOr
LIM = 1.3  # colour limits: |tension| from 10**-LIM to 10**LIM


def _schemes(dark):
    if dark:
        return {"face": "#191817", "ink": "#e8e6e1", "grey": "#4a4744", "blank": "#2a2725",
                "dim": "#8a8680"}  # fmt: skip
    return {"face": "white", "ink": "#1a1a1a", "grey": "#d9d9d9", "blank": "white",
            "dim": "#aaaaaa"}  # fmt: skip


def _fmt(v):
    a = abs(v)
    return f"{-a:.2f}" if a < 1 else (f"{-a:.1f}" if a < 10 else f"{-a:.0f}")


def draw_term(ax, names, w, T, title, dark=False, fs=9.0, colorbar=True):
    """One term's tension matrix. Rows: the metric that rises (i); columns: the one that gives
    way (j). Metrics are ordered by the term's exponent, largest first, so the cells that carry
    a number sit together and the empty and zero cells fall in the margins."""
    c = _schemes(dark)
    order = np.argsort(-np.asarray(w), kind="stable")
    d = len(w)
    Tm = T[np.ix_(order, order)]
    part = np.asarray(w)[order] > P.PARTICIPATION
    logT = np.full((d, d), np.nan)
    neg = Tm < 0
    logT[neg] = np.log10(-Tm[neg])
    norm = TwoSlopeNorm(vcenter=0.0, vmin=-LIM, vmax=LIM)
    cmap = plt.get_cmap(CMAP)
    ax.set_facecolor(c["face"])
    # blank (j carries none) stays empty; the diagonal and the zero cells get their own fill
    for i in range(d):
        for j in range(d):
            if i == j:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fc=c["grey"], ec="none"))
            elif np.isnan(Tm[i, j]):
                ax.add_patch(
                    plt.Rectangle(
                        (j - 0.5, i - 0.5), 1, 1, fc=c["blank"], ec=c["grey"], lw=0.4, ls=":"
                    )
                )
            elif Tm[i, j] == 0:
                ax.add_patch(
                    plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fc=c["face"], ec=c["grey"], lw=0.4)
                )
                ax.text(j, i, "0", ha="center", va="center", fontsize=fs, color=c["dim"])
            else:
                col = cmap(norm(logT[i, j]))
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fc=col, ec="none"))
                lum = 0.2126 * col[0] + 0.7152 * col[1] + 0.0722 * col[2]
                ax.text(
                    j,
                    i,
                    _fmt(Tm[i, j]),
                    ha="center",
                    va="center",
                    fontsize=fs,
                    color="black" if lum > 0.5 else "white",
                )
    ax.set_xlim(-0.5, d - 0.5)
    ax.set_ylim(d - 0.5, -0.5)
    ax.set_aspect("equal")
    lab = [f"{names[k]}  w={np.asarray(w)[k]:.2f}" for k in order]
    ax.set_xticks(range(d), [names[k] for k in order], rotation=90, fontsize=fs, color=c["ink"])
    ax.set_yticks(range(d), lab, fontsize=fs, color=c["ink"])
    for tl, p in zip(ax.get_xticklabels(), part, strict=True):
        tl.set_color(c["ink"] if p else c["dim"])
    for tl, p in zip(ax.get_yticklabels(), part, strict=True):
        tl.set_color(c["ink"] if p else c["dim"])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("metric that gives way (j)", fontsize=fs, color=c["ink"])
    ax.set_ylabel("metric that rises (i)", fontsize=fs, color=c["ink"])
    ax.set_title(
        title + "\neach cell: change in the column metric per unit rise of the row metric",
        fontsize=fs + 1,
        color=c["ink"],
    )
    n = int(part.sum())
    if n < d - 1:  # the key sits in the empty corner, where the structure it names is
        ax.text(
            n - 0.4,
            1.2,
            "Empty column: that metric carries\nno exponent on this term, so\n"
            "it is not read as giving way.",
            ha="left",
            va="center",
            fontsize=fs - 0.5,
            color=c["ink"],
        )
        ax.text(
            n - 0.4,
            3.4,
            "Row of 0: that metric carries no\nexponent, so raising it moves\n"
            "nothing along the term.",
            ha="left",
            va="center",
            fontsize=fs - 0.5,
            color=c["ink"],
        )
    if colorbar:
        sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        cb = ax.figure.colorbar(sm, ax=ax, fraction=0.035, pad=0.03)
        cb.set_ticks([-1, 0, 1], labels=["0.1", "1", "10"])
        cb.set_label("size of the tension (log scale)", fontsize=fs, color=c["ink"])
        cb.ax.tick_params(labelsize=fs, colors=c["ink"])
        cb.outline.set_visible(False)
    return ax


def term_inputs(study, fit):
    est = fit.estimator
    U = np.log(study.M)
    cells = est.assign_cells(study.M)
    out = []
    for k in range(len(est.exponents_)):
        w = est.exponents_[k]
        u = P.balanced_point(U[cells == k], w, float(fit.tau))
        out.append((w, P.term_tension_matrix(w, u)))
    return out


def title_for(k, w):
    n = int((np.asarray(w) > P.PARTICIPATION).sum())
    return f"term {k + 1}: {n} of {len(w)} metrics carry an exponent"


def draw_compact(names, terms, path):
    """The same matrix cut to the metrics that carry an exponent (the negative-edit option): the
    zero rows and the empty columns are dropped and one line names the metrics left out."""
    fig, axes = plt.subplots(len(terms), 1, figsize=(7.0, 5.9 * len(terms)))
    for k, (ax, (w, T)) in enumerate(zip(np.atleast_1d(axes), terms, strict=True)):
        keep = np.flatnonzero(np.asarray(w) > P.PARTICIPATION)
        gone = [names[i] for i in range(len(w)) if i not in set(keep)]
        draw_term(
            ax,
            [names[i] for i in keep],
            np.asarray(w)[keep],
            T[np.ix_(keep, keep)],
            title_for(k, w),
        )
        ax.set_xlabel(
            "metric that gives way (j)\nno exponent on this term, so not shown: " + ", ".join(gone)
        )
    fig.tight_layout()
    fig.savefig(path, dpi=100, bbox_inches="tight")
    plt.close(fig)


def main():
    IMG.mkdir(exist_ok=True)
    study, fits = load()
    fit = fits[2]
    shutil.copy(ROOT / "paper" / "figures" / "fig-tensions-case.png", IMG / "before.png")
    terms = term_inputs(study, fit)
    names = study.names
    for dark in (False, True):
        c = _schemes(dark)
        fig, axes = plt.subplots(
            len(terms), 1, figsize=(8.0, 7.4 * len(terms)), facecolor=c["face"]
        )
        for k, (ax, (w, T)) in enumerate(zip(np.atleast_1d(axes), terms, strict=True)):
            draw_term(ax, names, w, T, title_for(k, w), dark=dark)
        fig.tight_layout()
        fig.savefig(
            IMG / ("after-replace-dark.png" if dark else "after-replace.png"),
            dpi=100,
            facecolor=c["face"],
            bbox_inches="tight",
        )
        plt.close(fig)
    draw_compact(names, terms, IMG / "after-compact.png")
    # beside: the data correlations of Figure 7 next to the tension matrix, same term
    _, _, plotting = case._lib()
    reps = case._all_terms(study, fit)
    fig, axes = plt.subplots(len(terms), 2, figsize=(16.0, 7.4 * len(terms)))
    for k, (w, T) in enumerate(terms):
        plotting.plot_tensions(reps[k], names=names, ax=axes[k, 0])
        axes[k, 0].set_title(
            f"term {k + 1}: association among its near-frontier designs", fontsize=10
        )
        plt.setp(axes[k, 0].get_xticklabels(), rotation=90, fontsize=8)
        plt.setp(axes[k, 0].get_yticklabels(), fontsize=8)
        draw_term(axes[k, 1], names, w, T, title_for(k, w))
    fig.tight_layout()
    fig.savefig(IMG / "after-beside.png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    print("wrote", sorted(p.name for p in IMG.glob("*.png")))


if __name__ == "__main__":
    main()
