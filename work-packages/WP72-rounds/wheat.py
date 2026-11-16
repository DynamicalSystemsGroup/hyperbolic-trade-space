"""WP72 wheat: the invariant fit on Broadbalk grain and straw, with and without groups.

``uv run python work-packages/WP72-rounds/wheat.py`` reads the committed derived table
``examples/wheat/derived/grain_straw.csv`` (Glendining and Poulton 2023,
doi:10.23637/rbk1-yld6822-01, CC BY 4.0; hashes in ``examples/wheat/manifest.toml``) and writes
``results_wheat.md`` and two figures under ``figures/``.

Metrics: grain and straw in t/ha, logged, no scaler, so the exponents read directly (a standard
scaler would rescale them by the pull-back of L9).
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from common import md_table  # noqa: E402
from estimator import (  # noqa: E402
    InvariantFit,
    pca_minor,
    simplex_min_variance,
    two_term_invariant,
    within_scatter,
)

from hyperbolic_trade_space import HyperbolicTradeSpace, select_temperature  # noqa: E402

TABLE = ROOT / "examples" / "wheat" / "derived" / "grain_straw.csv"
FIG = HERE / "figures"

GROUPINGS = {
    "none (one group)": [],
    "cultivar": ["cultivar"],
    "treatment": ["treatment"],
    "year": ["year"],
    "plot": ["plot"],
    "year x section": ["year", "section"],
    "year x treatment": ["year", "treatment"],
}


def labels(df, cols):
    if not cols:
        return np.zeros(len(df), int)
    return df[cols].astype(str).agg("|".join, axis=1).factorize()[0]


def share(f, groups):
    """Within-group share of the variance of a per-row score ``f``."""
    f = np.asarray(f, float)
    S_W, S_T, _ = within_scatter(f[:, None], groups)
    return float(S_W[0, 0] / S_T[0, 0])


def main():
    df = pd.read_csv(TABLE)
    M = df[["grain", "straw"]].to_numpy(float)
    U = np.log(M)
    log_biomass = np.log(M.sum(axis=1))
    rows = []
    fits = {}
    rng = np.random.default_rng(0)
    for name, cols in GROUPINGS.items():
        g = labels(df, cols)
        fit = InvariantFit().fit(M, groups=g)
        fits[name] = (fit, g)
        S_W, S_T, n_used = within_scatter(U, g)
        pw, ok = pca_minor(S_W)
        perm = [
            InvariantFit().fit(M, groups=rng.permutation(g)).within_share_
            for _ in range(20 if cols else 0)
        ]
        rows.append(
            {
                "grouping": name,
                "groups (>= 2 rows)": int(sum(np.bincount(g) >= 2)),
                "rows used": n_used,
                "w (grain, straw)": f"({fit.exponents_[0]:.3f}, {fit.exponents_[1]:.3f})",
                "within_share": fit.within_share_ if cols else np.nan,
                "shuffled-label null": float(np.median(perm)) if perm else np.nan,
                "flatness": fit.flatness_,
                "within sd log V": float(np.sqrt(fit.within_var_)),
                "within sd trade": float(fit.trade_sd_[0]),
                "share: log biomass": share(log_biomass, g) if cols else np.nan,
                "share: log grain": share(U[:, 0], g) if cols else np.nan,
                "share: log(grain/straw)": share(U[:, 0] - U[:, 1], g) if cols else np.nan,
                "PCA within (simplex)": f"({pw[0]:.3f}, {pw[1]:.3f})" if ok else "off simplex",
            }
        )
    res = pd.DataFrame(rows)

    # baselines on the whole table
    tau = select_temperature(M, target_frac_above=0.1, bounds=(3.0, 1e4))
    front = HyperbolicTradeSpace(temperature=tau, random_state=0).fit(M)
    _, S_T, _ = within_scatter(U, np.zeros(len(U), int))
    pt, pt_ok = pca_minor(S_T)
    vals, vecs = np.linalg.eigh(S_T)

    # K = 2 on the grouping that conserves most
    g_yt = fits["year x treatment"][1]
    W2, b2, wv2 = two_term_invariant(U, g_yt, n_restarts=10)
    fit_yt = fits["year x treatment"][0]

    with open(HERE / "results_wheat.md", "w") as f:
        f.write("# WP72 wheat: results\n\n")
        f.write(
            f"{len(df)} plot-years of `examples/wheat/derived/grain_straw.csv`; metrics grain and "
            "straw in t/ha, logged, no scaler. `share: X` is the within-group share of the "
            "variance of X; the shuffled-label null is the median `within_share` over 20 "
            "random permutations of the group labels.\n\n"
        )
        f.write(md_table(res))
        f.write("\n\n## Baselines on the whole table\n\n")
        f.write(
            f"- Frontier fit (no scaler), tau = {tau:.1f} by `select_temperature` (a tenth above): "
            f"w = ({front.exponents_[0, 0]:.3f}, {front.exponents_[0, 1]:.3f}).\n"
            f"- PCA of log(grain, straw), whole table: eigenvalues {vals[0]:.4f} and "
            f"{vals[1]:.4f}; "
            f"major axis ({vecs[0, 1]:.3f}, {vecs[1, 1]:.3f}); minor axis "
            f"({vecs[0, 0]:.3f}, {vecs[1, 0]:.3f})"
            + (f", on the simplex ({pt[0]:.3f}, {pt[1]:.3f})" if pt_ok else ", off the simplex")
            + ".\n"
            f"- Invariant fit with no groups (minimum variance on the simplex): "
            f"({simplex_min_variance(S_T)[0]:.3f}, {simplex_min_variance(S_T)[1]:.3f}).\n"
        )
        f.write("\n## Two terms within year x treatment\n\n")
        f.write(
            f"K = 2, kappa = 1: W = ({W2[0, 0]:.3f}, {W2[0, 1]:.3f}) and "
            f"({W2[1, 0]:.3f}, {W2[1, 1]:.3f}), b = {b2:.3f}; within variance {wv2:.5f} against "
            f"{fit_yt.within_var_:.5f} for the monomial and "
            f"{within_scatter(log_biomass[:, None], g_yt)[0][0, 0]:.5f} for log biomass "
            "(the two-term invariant with W = I, b = 0).\n"
        )
    print(res.to_string())
    print("frontier", front.exponents_, "tau", tau, "pca", vals, vecs, "K2", W2, b2, wv2)

    figures(df, U, fit_yt, g_yt, res)


def figures(df, U, fit, g, res):
    FIG.mkdir(exist_ok=True)
    w = fit.exponents_
    # 1. the log plane: every plot-year in grey; three year x treatment groups in colour, each with
    # its level line w . u = level, the found trade direction along it
    fig, ax = plt.subplots(figsize=(6.4, 5.2), constrained_layout=True)
    ax.scatter(U[:, 0], U[:, 1], s=4, c="0.78", lw=0, label="all plot-years")
    sizes = np.bincount(g)
    picks = []
    for want in (("Nil",), ("N4(P)KMg", "N3PK(Na)Mg", "N3PKNaMg")):
        cand = [k for k in np.flatnonzero(sizes >= 6) if df.treatment.to_numpy()[g == k][0] in want]
        if cand:
            picks.append(cand[len(cand) // 2])
    colours = ["#1b6ca8", "#c2410c", "#2f855a"]
    t = np.linspace(-1.2, 1.2, 2)
    tangent = np.array([w[1], -w[0]]) / np.hypot(*w)
    for k, col in zip(picks, colours, strict=False):
        rows = g == k
        lev = fit.levels_[k]
        label = f"{df.year.to_numpy()[rows][0]}, {df.treatment.to_numpy()[rows][0]}"
        ax.scatter(U[rows, 0], U[rows, 1], s=22, color=col, label=label, zorder=3)
        c = U[rows].mean(axis=0)
        p = c + np.outer(t, tangent)
        ax.plot(p[:, 0], p[:, 1], color=col, lw=1.2, zorder=2)
        ax.annotate(
            f"log V = {lev:.2f}",
            p[0],
            color=col,
            fontsize=8,
            xytext=(-3, 0),
            textcoords="offset points",
            va="center",
            ha="right",
        )
    ax.set_xlabel("log grain (t/ha)")
    ax.set_ylabel("log straw (t/ha)")
    ax.set_title(
        f"Invariant fit within year x treatment: w = ({w[0]:.2f}, {w[1]:.2f});\n"
        "lines: the level set through two groups; their plot-years spread along the size\n"
        "(up and to the right) as much as along the level set",
        fontsize=9,
    )
    ax.set_aspect("equal")
    ax.legend(fontsize=8, loc="upper left", frameon=False)
    fig.savefig(FIG / "wheat-level-sets.png", dpi=150)
    plt.close(fig)

    # 2. within-group share of variance by grouping
    r = res[res.grouping != "none (one group)"].iloc[::-1]
    fig, ax = plt.subplots(figsize=(6.4, 4.0), constrained_layout=True)
    y = np.arange(len(r))
    series = [
        ("within_share", "invariant fit log V", "#1b6ca8", "o"),
        ("share: log biomass", "log biomass", "#2f855a", "s"),
        ("share: log(grain/straw)", "log(grain/straw), the trade", "#c2410c", "D"),
        ("shuffled-label null", "shuffled labels", "0.5", "x"),
    ]
    for col, lab, colour, mk in series:
        ax.scatter(r[col], y, label=lab, color=colour, marker=mk, s=28, zorder=3)
    ax.set_yticks(y, r.grouping)
    ax.set_xlim(0, 1.02)
    ax.set_xlabel("share of the variance left within groups (0: conserved within groups)")
    ax.grid(axis="x", color="0.9")
    ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=2, frameon=False)
    fig.savefig(FIG / "wheat-within-share.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
