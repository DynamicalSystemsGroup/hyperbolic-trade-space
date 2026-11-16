"""WP72 market maker: the invariant fit on a Uniswap v2 pair's reserves, event by event.

``uv run python work-packages/WP72-rounds/amm.py`` reads ``data/amm/reserves.csv`` (written by
``fetch_amm.py``; hashes in ``amm-manifest.toml``) and writes ``results_amm.md`` and
``figures/amm-chart.png``.

A stretch is the run of rows between two reserve changes that are not swaps (``Mint``, ``Burn`` or a
bare ``sync``); the row of such an event opens the next stretch, since its reserves are those after
the event. Metrics: the two reserves in token units (DAI and WETH, 18 decimals each), logged.
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
sys.path.insert(0, str(HERE))

from common import md_table  # noqa: E402
from estimator import InvariantFit, pca_minor, simplex_min_variance, within_scatter  # noqa: E402

from hyperbolic_trade_space import HyperbolicTradeSpace, select_temperature  # noqa: E402

DATA = HERE / "data" / "amm" / "reserves.csv"
FIG = HERE / "figures"


def fmt(w):
    return "(" + ", ".join(f"{x:.4f}" for x in w) + ")"


def main():
    df = pd.read_csv(DATA, dtype={"reserve0": object, "reserve1": object})
    M = np.column_stack(
        [df.reserve0.map(int).to_numpy(float) / 1e18, df.reserve1.map(int).to_numpy(float) / 1e18]
    )
    U = np.log(M)
    liq = (df.event != "Swap").to_numpy()
    stretch = np.cumsum(liq)
    n_str = int(np.sum(np.bincount(stretch) >= 2))

    fit = InvariantFit().fit(M, groups=stretch)
    S_W, S_T, _ = within_scatter(U, stretch)
    pw, pw_ok = pca_minor(S_W)
    pt, pt_ok = pca_minor(S_T)
    vals_w = np.linalg.eigvalsh(S_W)
    tau = select_temperature(M, target_frac_above=0.1, bounds=(3.0, 1e4))
    front = HyperbolicTradeSpace(temperature=tau, random_state=0).fit(M)

    # groups unknown: the order fallback, its breaks against the recorded liquidity events
    order = InvariantFit(fallback="order").fit(M)
    found = np.flatnonzero(np.diff(order.group_labels_) > 0) + 1
    true = np.flatnonzero(liq[1:]) + 1
    hit = np.intersect1d(found, true)

    # the level: per-swap change of log V within stretches (the 0.3 per cent fee stays in the pool)
    lv = U @ fit.exponents_
    dlv = np.diff(lv)
    same = stretch[1:] == stretch[:-1]
    swap_d = dlv[same]
    ev = df.event.to_numpy()[1:]
    mb_d = dlv[np.isin(ev, ("Mint", "Burn"))]
    sy_d = dlv[ev == "sync"]
    big = np.abs(mb_d) > np.abs(swap_d).max()
    r0 = [int(x) for x in df.reserve0]
    r1 = [int(x) for x in df.reserve1]
    k_int = [a * b for a, b in zip(r0, r1, strict=True)]
    is_swap = df.event.to_numpy()[1:] == "Swap"
    k_up = sum(k_int[i + 1] > k_int[i] for i in np.flatnonzero(is_swap))
    n_sw = int(is_swap.sum())
    half = np.array([0.5, 0.5])
    size, ratio = U.sum(axis=1), U[:, 0] - U[:, 1]
    corr = [
        np.corrcoef(size[stretch == s], ratio[stretch == s])[0, 1]
        for s in np.unique(stretch)
        if np.sum(stretch == s) > 2
    ]
    mb_idx = np.flatnonzero(np.isin(df.event.to_numpy(), ("Mint", "Burn")))
    mb_hit = np.intersect1d(found, mb_idx)
    dz = np.diff(U[:, 0] - U[:, 1])[same]

    rows = [
        {
            "estimator": "invariant fit, stretches given",
            "w (DAI, WETH)": fmt(fit.exponents_),
            "note": f"within_share {fit.within_share_:.2e}, flatness {fit.flatness_:.2e}",
        },
        {
            "estimator": "invariant fit, order fallback (no labels)",
            "w (DAI, WETH)": fmt(order.exponents_),
            "note": (
                f"{len(found)} breaks found; {len(hit)} of the {len(true)} recorded non-swap "
                f"events and {len(mb_hit)} of the {len(mb_idx)} Mint and Burn events among them"
            ),
        },
        {
            "estimator": "invariant fit, no groups",
            "w (DAI, WETH)": fmt(simplex_min_variance(S_T)),
            "note": "minimum variance on the simplex of the whole table",
        },
        {
            "estimator": "PCA within stretches, minor axis",
            "w (DAI, WETH)": fmt(pw) if pw_ok else "off simplex",
            "note": f"eigenvalues {vals_w[0]:.2e} and {vals_w[1]:.2e}",
        },
        {
            "estimator": "PCA pooled, minor axis",
            "w (DAI, WETH)": fmt(pt) if pt_ok else "off simplex",
            "note": "",
        },
        {
            "estimator": f"frontier fit, tau = {tau:.1f} (a tenth above)",
            "w (DAI, WETH)": fmt(front.exponents_[0]),
            "note": "the boundary of the cloud, not the level",
        },
    ]
    res = pd.DataFrame(rows)
    counts = df.event.value_counts().to_dict()
    with open(HERE / "results_amm.md", "w") as f:
        f.write("# WP72 market maker: results\n\n")
        f.write(
            f"Uniswap v2 DAI/WETH pair, blocks {df.block.min()} to {df.block.max()}: "
            f"{len(df)} reserve updates ({counts}); {n_str} stretches of two or more rows.\n\n"
        )
        f.write(md_table(res))
        f.write("\n\n## The level within and between stretches\n\n")
        f.write(
            f"- Per swap, within a stretch: median change of log V {np.median(swap_d):.2e}, "
            f"largest {np.abs(swap_d).max():.2e}; median absolute change of log(DAI/WETH) "
            f"{np.median(np.abs(dz)):.2e}, largest {np.abs(dz).max():.2e}.\n"
            f"- In exact integers, the product of the reserves rises at {k_up} of {n_sw} swaps "
            f"(the 0.3 per cent fee stays in the pool); the sum of the per-swap changes of "
            f"log V over the window is {swap_d.sum():.2e}. Within-group variance of log V at "
            f"(1/2, 1/2): {half @ S_W @ half:.3e}; at the fitted w: {fit.within_var_:.3e}; "
            f"median within-stretch correlation of log(DAI WETH) with log(DAI/WETH): "
            f"{np.nanmedian(corr):.2f}.\n"
            f"- At a Mint or Burn: median absolute change of log V {np.median(np.abs(mb_d)):.2e}, "
            f"largest {np.abs(mb_d).max():.2e}; {big.sum()} of {len(mb_d)} exceed the largest "
            f"single-swap change. At a bare sync: largest absolute change "
            f"{np.abs(sy_d).max():.2e}.\n"
            f"- Over the window: log V from {lv.min():.4f} to {lv.max():.4f}; "
            f"log(DAI/WETH) from {(U[:, 0] - U[:, 1]).min():.4f} to "
            f"{(U[:, 0] - U[:, 1]).max():.4f}.\n"
        )
    print(res.to_string())
    figures(df, U, lv, liq, stretch, fit)


def figures(df, U, lv, liq, stretch, fit):
    """The chart of the reserves: the trade coordinate against the level, in event order."""
    FIG.mkdir(exist_ok=True)
    for old in ("amm-level-and-trade.png", "amm-log-plane.png"):
        (FIG / old).unlink(missing_ok=True)
    mb = np.isin(df.event.to_numpy(), ("Mint", "Burn"))
    z = U[:, 0] - U[:, 1]
    fig, ax = plt.subplots(figsize=(6.4, 4.4), constrained_layout=True)
    sc = ax.scatter(z, lv - lv[0], s=3, c=np.arange(len(lv)), cmap="viridis", lw=0)
    ax.scatter(
        z[mb],
        (lv - lv[0])[mb],
        s=26,
        facecolors="none",
        edgecolors="#c2410c",
        lw=1.0,
        label="row after a Mint or Burn",
    )
    fig.colorbar(sc, ax=ax, label="reserve update (event order)")
    ax.set_xlabel("log(DAI / WETH), the trade (price) coordinate")
    ax.set_ylabel("log V - log V(first row), the level")
    w = fit.exponents_
    ax.set_title(
        f"Uniswap v2 DAI/WETH, w = ({w[0]:.3f}, {w[1]:.3f}): swaps run along a level,\n"
        "Mint and Burn step between levels",
        fontsize=9,
    )
    ax.legend(fontsize=8, loc="lower left", frameon=False)
    fig.savefig(FIG / "amm-chart.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
