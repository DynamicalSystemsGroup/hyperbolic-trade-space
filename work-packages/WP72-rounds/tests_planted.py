"""WP72 planted tests: the invariant fit recovers planted exponents; the baselines do what they do.

``uv run python work-packages/WP72-rounds/tests_planted.py`` writes ``results_planted.csv`` and
``results_planted.md`` beside this file and exits non-zero if a recovery check fails.

A planted table: ``g`` groups of ``n`` rows; row ``i`` of group ``k`` has chart position
``z_i = c_k + N(0, I)`` (trade spread 1, group centre ``c_k ~ N(0, z_shift^2 I)``) and level
``ell_k + N(0, noise^2)`` (``ell_k ~ N(0, level_spread^2)``), placed on the level set by the shift
property: ``u = B^T z + (level - w . B^T z) 1`` (L1: ``w . 1 = 1``; L8: ``B`` the chart basis).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import md_table  # noqa: E402
from estimator import (  # noqa: E402
    InvariantFit,
    column_null,
    pca_minor,
    simplex_min_variance,
    two_term_invariant,
    within_scatter,
)

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data  # noqa: E402
from hyperbolic_trade_space.coordinates import helmert_basis  # noqa: E402

TOL_CLEAN = 1e-6
TOL_NOISY = 1e-2
SEEDS = range(5)


def plant(
    w, n_groups=6, n_per=100, level_spread=1.0, noise=0.0, z_shift=1.0, confusion=0.0, seed=0
):
    """A planted table ``(M, given_labels, true_labels)`` with invariant ``w``, group-ordered."""
    rng = np.random.default_rng(seed)
    w = np.asarray(w, float)
    d = len(w)
    B = helmert_basis(d)
    true = np.repeat(np.arange(n_groups), n_per)
    centres = rng.normal(scale=z_shift, size=(n_groups, d - 1))
    levels = rng.normal(scale=level_spread, size=n_groups)
    Z = centres[true] + rng.normal(size=(len(true), d - 1))
    X = Z @ B
    lev = levels[true] + rng.normal(scale=noise, size=len(true))
    U = X + (lev - X @ w)[:, None]
    given = true.copy()
    flip = rng.random(len(true)) < confusion
    given[flip] = rng.integers(0, n_groups, flip.sum())
    return np.exp(U), given, true


def plant_two_term(W, b, kappa=1.0, n_groups=6, n_per=100, level_spread=1.0, z_shift=1.0, seed=0):
    """Rows on level sets of ``Phi = (1/kappa) log(e^{kappa w1.u} + e^{kappa (w2.u + b)})``."""
    rng = np.random.default_rng(seed)
    W = np.asarray(W, float)
    d = W.shape[1]
    B = helmert_basis(d)
    g = np.repeat(np.arange(n_groups), n_per)
    centres = rng.normal(scale=z_shift, size=(n_groups, d - 1))
    X = (centres[g] + rng.normal(size=(len(g), d - 1))) @ B
    phi0 = np.logaddexp(kappa * X @ W[0], kappa * (X @ W[1] + b)) / kappa
    lev = rng.normal(scale=level_spread, size=n_groups)[g]
    return np.exp(X + (lev - phi0)[:, None]), g  # Phi(u + t 1) = Phi(u) + t (L10)


def err(w_hat, w):
    return float(np.max(np.abs(np.asarray(w_hat) - np.asarray(w))))


def methods(M, given, w, n_groups):
    """Every estimator on one table: max-abs exponent error of each (nan: PCA off the simplex)."""
    U = np.log(M)
    S_W, S_T, _ = within_scatter(U, given)
    pw, pw_ok = pca_minor(S_W)
    pt, pt_ok = pca_minor(S_T)
    fit = InvariantFit().fit(M, groups=given)
    order = InvariantFit(fallback="order").fit(M)
    levels = InvariantFit(fallback="levels", n_levels=n_groups).fit(M)
    front = HyperbolicTradeSpace(temperature=20.0, random_state=0).fit(M)
    return {
        "invariant fit (groups given)": err(fit.exponents_, w),
        "invariant fit (order fallback)": err(order.exponents_, w),
        "invariant fit (levels fallback)": err(levels.exponents_, w),
        "invariant fit (no groups)": err(simplex_min_variance(S_T), w),
        "PCA within groups": err(pw, w) if pw_ok else np.nan,
        "PCA pooled": err(pt, w) if pt_ok else np.nan,
        "frontier fit (tau=20)": err(front.exponents_[0], w),
        "within_share": fit.within_share_,
    }


def sweep(name, cases, **fixed):
    rows = []
    for label, w, kw in cases:
        res = [
            methods(*plant(w, seed=s, **{**fixed, **kw})[:2], w, fixed.get("n_groups", 6))
            for s in SEEDS
        ]
        df = pd.DataFrame(res)
        med = df.median(skipna=False)
        # PCA: report the median only when it lands on the simplex in every seed
        row = {
            "sweep": name,
            "case": label,
            "d": len(w),
            "w": "(" + ", ".join(f"{x:g}" for x in w) + ")",
        }
        row.update(med.to_dict())
        rows.append(row)
    return rows


def main():
    rows = []
    W2a, W2b, W3 = (0.7, 0.3), (0.5, 0.5), (0.5, 0.3, 0.2)

    # S1: clean tables, groups differ in level only (z_shift 0) and in level and position (1)
    for zs in (0.0, 1.0):
        rows += sweep(
            "clean",
            [(f"z_shift={zs}", w, {}) for w in (W2a, W2b, W3)],
            z_shift=zs,
        )
    # S2: noise on the level (trade spread 1)
    for w in (W2a, W3):
        rows += sweep(
            "noise",
            [(f"noise={s}", w, {"noise": s}) for s in (0.01, 0.03, 0.1, 0.3, 1.0)],
            z_shift=1.0,
        )
    # S3: group confusion (a fraction of rows relabelled at random), noise 0.03
    for w in (W2a, W3):
        rows += sweep(
            "confusion",
            [(f"confusion={p}", w, {"confusion": p}) for p in (0.1, 0.3, 0.5, 0.9)],
            z_shift=1.0,
            noise=0.03,
        )
    # S4: level spread between groups, groups at one position (z_shift 0), noise 0.03
    for w in (W2a, W3):
        rows += sweep(
            "level spread",
            [(f"level_spread={s}", w, {"level_spread": s}) for s in (0.3, 1.0, 3.0, 10.0)],
            z_shift=0.0,
            noise=0.03,
        )
    res = pd.DataFrame(rows)

    # S5: two-term invariants
    two = []
    for label, W, b in (
        ("log(m1 + m2), biomass-like", np.eye(2), 0.0),
        ("(0.8,0.2) and (0.2,0.8), b=0.3", np.array([[0.8, 0.2], [0.2, 0.8]]), 0.3),
    ):
        M, g = plant_two_term(W, b, seed=0)
        Wh, bh, wv = two_term_invariant(np.log(M), g, n_restarts=20)
        mono = InvariantFit().fit(M, groups=g)
        two.append(
            {
                "case": label,
                "max |W - W*|": err(Wh, W),
                "|b - b*|": abs(bh - b),
                "within var (K=2)": wv,
                "monomial w": "(" + ", ".join(f"{x:.3f}" for x in mono.exponents_) + ")",
                "monomial within_share": mono.within_share_,
            }
        )
    two = pd.DataFrame(two)

    # S6: no invariant: a frontier-bounded cloud
    null_rows = []
    for d in (2, 3):
        X, info = make_frontier_data(600, d, random_state=0)
        rng = np.random.default_rng(1)
        g_rand = rng.integers(0, 6, len(X))
        given = InvariantFit().fit(X, groups=g_rand)
        lev = InvariantFit(fallback="levels", n_levels=6).fit(X)
        nul = column_null(X, InvariantFit(fallback="levels", n_levels=6), n_perm=20)
        front = HyperbolicTradeSpace(temperature=20.0, random_state=0).fit(X)
        null_rows.append(
            {
                "d": d,
                "planted frontier w": "(" + ", ".join(f"{x:.3f}" for x in info["exponents"]) + ")",
                "frontier fit error": err(front.exponents_[0], info["exponents"]),
                "random groups: within_share": given.within_share_,
                "random groups: flatness": given.flatness_,
                "levels fallback: within_share": lev.within_share_,
                "levels fallback: flatness": lev.flatness_,
                "column-permuted null within_share (median, min)": (
                    f"{np.median(nul):.3f}, {nul.min():.3f}"
                ),
            }
        )
    null = pd.DataFrame(null_rows)

    res.to_csv(HERE / "results_planted.csv", index=False)
    with open(HERE / "results_planted.md", "w") as f:
        f.write("# WP72 planted tests: results\n\n")
        f.write(
            "Max-abs error of the recovered exponent vector, median over 5 seeds; 6 groups of 100 "
            "rows; trade spread 1; blank: PCA's minor axis off the simplex in at least one seed. "
            "Frontier fit at tau = 20.\n\n"
        )
        f.write(md_table(res))
        f.write("\n\n## Two-term invariants (K = 2, kappa = 1)\n\n")
        f.write(md_table(two))
        f.write(
            "\n\n## No invariant: a frontier-bounded cloud (`make_frontier_data`, 600 rows)\n\n"
        )
        f.write(md_table(null))
        f.write("\n")

    # checks
    clean = res[res.sweep == "clean"]
    fails = []
    if not (clean["invariant fit (groups given)"] < TOL_CLEAN).all():
        fails.append("clean recovery with groups given")
    if not (clean["invariant fit (order fallback)"] < TOL_CLEAN).all():
        fails.append("clean recovery, order fallback")
    noisy = res[(res.sweep == "noise") & res.case.isin(["noise=0.01", "noise=0.03", "noise=0.1"])]
    if not (noisy["invariant fit (groups given)"] < TOL_NOISY).all():
        fails.append("recovery within 0.01 at level noise up to 0.1")
    if not (two["max |W - W*|"] < 1e-3).all():
        fails.append("two-term recovery")
    if not (null["random groups: within_share"] > 0.9).all():
        fails.append("random groups report a poor fit")
    print(res.to_string())
    print(two.to_string())
    print(null.to_string())
    if fails:
        print("FAILED:", fails)
        sys.exit(1)
    print("all planted checks passed")


if __name__ == "__main__":
    main()
