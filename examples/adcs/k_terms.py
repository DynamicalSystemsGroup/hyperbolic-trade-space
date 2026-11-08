"""K = 1, 2, 3 posynomial fits of the two cubesat datasets (WP9, D-6).

Run ``uv run python examples/adcs/k_terms.py``. Same feasibility filter, conditioning and
temperature selection as ``adcs_trade_study.ipynb``; prints the per-facet record and saves
``figures/k3_*_<regime>.png``. Nothing is simulated.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder

from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    select_temperature,
    tension_report,
)
from hyperbolic_trade_space.plotting import (
    facet_labels,
    plot_frontier_coordinates,
    plot_log_plane,
    plot_tensions,
)

HERE = Path(__file__).resolve().parent
DATA, FIGS = HERE / "data", HERE / "figures"
REGIMES = {"primary": "adcs_designs_cubesat_gains.csv", "stock": "adcs_designs_cubesat.csv"}
ATTRS = [
    "settling_time_s", "slew_time_s", "pointing_error_deg", "total_mass_kg", "control_effort",
    "power_margin_w", "energy_balance_wh", "eclipse_reserve_wh", "peak_slew_power_w", "dod_eclipse",
]  # fmt: skip
SHORT = dict(zip(ATTRS, [
    "settling time", "slew time", "pointing error", "total mass", "control effort",
    "power margin", "energy balance", "eclipse reserve", "peak slew power", "depth of discharge",
], strict=True))  # fmt: skip
UNITS = dict(zip(ATTRS, [
    "s", "s", "deg", "kg", "torque.s, proxy", "W", "Wh", "Wh", "W", "fraction",
], strict=True))  # fmt: skip
ORIENT = dict(zip(ATTRS, [-1, -1, -1, -1, -1, +1, +1, +1, -1, -1], strict=True))
WHEELS, TRACKERS = ["small", "medium", "large"], ["coarse", "medium", "fine"]
DESIGN_VARS = ["panel_span_m", "battery_wh", "Kp", "Kd"]
NAMES = [SHORT[a] for a in ATTRS]


def cond_label(a):
    """Axis label of a conditioned metric, in attribute terms."""
    inv = "inverse " if ORIENT[a] < 0 else ""
    return f"conditioned {SHORT[a]} ({inv}{UNITS[a]}; larger is better)"


def make_conditioner(attrs):
    """The notebook's ColumnTransformer: attributes -> metrics; covariates -> codes."""
    return ColumnTransformer(
        [
            ("metrics", LogAffinePreconditioner(orientation=[ORIENT[a] for a in attrs],
                                                scaler="standard"), list(attrs)),
            ("covariates", OrdinalEncoder(categories=[WHEELS, TRACKERS]),
             ["wheel_class", "st_grade"]),
            ("design", "passthrough", DESIGN_VARS),
        ],
        verbose_feature_names_out=True,
    ).set_output(transform="pandas")  # fmt: skip


def load_metrics(path, n_max=None):
    """Feasible rows of a dataset (the notebook's filter) and their conditioned metrics."""
    raw = pd.read_csv(path)
    ok = raw.settled & raw.power_ok & raw.momentum_ok & (raw[ATTRS] > 0).all(axis=1)
    feasible = raw[ok].reset_index(drop=True)
    if n_max:
        feasible = feasible.iloc[:n_max]
    table = make_conditioner(ATTRS).fit_transform(feasible)
    return feasible, table[[f"metrics__{a}" for a in ATTRS]].to_numpy()


def fit_k(M, K, tau, seed=0):
    """K-term fit at temperature tau."""
    return HyperbolicTradeSpace(temperature=tau, n_terms=K, random_state=seed).fit(M)


def reports(est, M):
    """List of per-facet TensionReports (a one-element list at K = 1)."""
    r = tension_report(est, M)
    return r if isinstance(r, list) else [r]


def top(names, w, n=3):
    """The n largest exponents, named."""
    return ", ".join(f"{names[j]} {w[j]:.3f}" for j in np.argsort(-w)[:n])


def contend(rep):
    """Contending set as sorted metric names (largest exponent first)."""
    order = np.argsort(-rep.contending_exponents)
    return [NAMES[rep.contending_set[i]] for i in order]


def facet_record(est, reps, rows):
    """One row of facts per facet."""
    out = []
    for k, rep in enumerate(reps):
        out.append({
            "facet": k + 1, "rows": int(rows[k]), "contending set": ", ".join(contend(rep)),
            "n_lemma": rep.n_lemma, "largest exponents": top(NAMES, rep.exponents),
            "near-frontier": rep.n_near_frontier, "reach beta_k": float(est.log_offset_[k]),
            "share": float(est.facet_share_[k]) if est.n_terms > 1 else 1.0,
        })  # fmt: skip
    return pd.DataFrame(out)


def _slice(est, U, labels, tau, j, k):
    """Facets drawable in the (j, k) log plane, with their exponents and offsets there."""
    W, keep, ws, bs = est.exponents_, [], [], []
    rest = [i for i in range(U.shape[1]) if i not in (j, k)]
    for f in range(len(W)):
        s = W[f, j] + W[f, k]
        near = (labels == f"facet {f + 1}") & (np.abs(est.training_log_v_) < 1 / tau)
        if min(W[f, j], W[f, k]) < 0.05 * s or s < 0.02 or not near.any():
            continue
        bs.append((est.log_offset_[f] - W[f, rest] @ np.median(U[near][:, rest], axis=0)) / s)
        ws.append([W[f, j] / s, W[f, k] / s])
        keep.append(f)
    return keep, ws, bs


def log_plane_slices(est, M, labels, tau, axes):
    """2-D slices of the K = 3 fit: the three metric pairs on which most facets have weight."""
    U, W = np.log(M), est.exponents_
    d = M.shape[1]
    cand = [(j, k) for j in range(d) for k in range(j + 1, d)]
    score = {}
    for c in cand:
        kept = _slice(est, U, labels, tau, *c)[0]
        score[c] = (len(kept), W[np.ix_(kept, list(c))].sum())
    pairs = sorted(cand, key=lambda c: score[c], reverse=True)[:3]
    for ax, (j, k) in zip(axes, pairs, strict=True):
        keep, ws, bs = _slice(est, U, labels, tau, j, k)
        sh = HyperbolicTradeSpace(temperature=tau, n_terms=len(keep))
        sh.exponents_, sh.log_offset_ = np.array(ws), np.array(bs)
        plot_log_plane(sh, M[:, [j, k]], color=labels, ax=ax)
        for lim, col in ((ax.set_xlim, j), (ax.set_ylim, k)):
            lo, hi = U[:, col].min(), U[:, col].max()
            lim(lo - 0.1 * (hi - lo), hi + 0.1 * (hi - lo))
        ax.set_xlabel("log of the " + cond_label(ATTRS[j]), fontsize=7)
        ax.set_ylabel("log of the " + cond_label(ATTRS[k]), fontsize=7)
        ax.set_title(
            f"{SHORT[ATTRS[j]]} and {SHORT[ATTRS[k]]}; facets {[f + 1 for f in keep]} drawn",
            fontsize=9,
        )


def save_figures(regime, est, M, reps, tau, figs=FIGS):
    """The three K = 3 figures of one regime, 150 dpi."""
    figs.mkdir(exist_ok=True)
    labels = facet_labels(est, M)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    log_plane_slices(est, M, labels, tau, axes)
    fig.suptitle(f"K = 3 log-plane slices, {regime} gains; colour: facet", y=1.0)
    fig.tight_layout()
    fig.savefig(figs / f"k3_log_planes_{regime}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    chart = est.transform(M)
    Z, logv = chart[:, :-1], chart[:, -1]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, c in zip(axes, [(0, 1), (0, 2)], strict=True):
        plot_frontier_coordinates(Z[:, list(c)], logv, color=labels, band=1 / tau, ax=ax)
        ax.set_xlabel(f"Z{c[0]} (log-ratio coordinate along the frontier, dimensionless)")
        ax.set_ylabel(f"Z{c[1]} (log-ratio coordinate along the frontier, dimensionless)")
    fig.suptitle(f"Position along the K = 3 frontier, {regime} gains; colour: facet", y=1.0)
    fig.tight_layout()
    fig.savefig(figs / f"k3_frontier_coordinates_{regime}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(21, 7))
    plot_tensions(reps, names=NAMES, ax=axes)
    for ax in axes:
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=6)
        plt.setp(ax.get_yticklabels(), fontsize=6)
    fig.suptitle(f"Association among near-frontier designs per facet, {regime} gains", y=1.0)
    fig.tight_layout()
    fig.savefig(figs / f"k3_tensions_{regime}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def relation(rep1, reps3):
    """How the K = 1 contending set relates to the K = 3 facets' sets."""
    s1 = {NAMES[j] for j in rep1.contending_set}
    sets = [{NAMES[j] for j in r.contending_set} for r in reps3]
    union = set().union(*sets)
    lines = [f"K=1 set ({len(s1)}): {sorted(s1)}"]
    for k, s in enumerate(sets):
        lines.append(
            f"  facet {k + 1}: shares {len(s & s1)} of {len(s)}; only in facet: {sorted(s - s1)}; "
            f"K=1 members absent: {sorted(s1 - s)}"
        )
    lines.append(
        f"  union of facets ({len(union)}): K=1 subset of union: {s1 <= union}; "
        f"in union not in K=1: {sorted(union - s1)}; in K=1 not in union: {sorted(s1 - union)}"
    )
    return "\n".join(lines)


def run_regime(regime, seeds=range(5), n_max=None, figs=FIGS, make_figures=True, verbose=True):
    """Fit one regime at K = 1, 2, 3; print and return the record."""
    feasible, M = load_metrics(DATA / REGIMES[regime], n_max)
    tau = select_temperature(M, target_frac_above=0.10, bounds=(3, 1e3))
    fits = {K: fit_k(M, K, tau) for K in (1, 2, 3)}
    reps = {K: reports(fits[K], M) for K in fits}
    p = print if verbose else (lambda *a, **k: None)
    p(f"\n{'=' * 78}\nREGIME {regime}: {REGIMES[regime]}; feasible {len(feasible)}; "
      f"tau = {tau:.2f} (K=1, target 0.10), band 1/tau = {1 / tau:.4f}")  # fmt: skip
    diag = []
    for K, e in fits.items():
        sizes = np.bincount(e.facet_, minlength=K) if K > 1 else [len(M)]
        share = e.facet_share_ if K > 1 else [1.0]
        diag.append({"K": K, "objective_": e.objective_, "frac_above_": e.frac_above_,
                     "facet rows": list(map(int, sizes)),
                     "facet shares": [round(float(s), 3) for s in share]})  # fmt: skip
    diag = pd.DataFrame(diag)
    sizes3 = np.bincount(fits[3].facet_, minlength=3)
    rec = facet_record(fits[3], reps[3], sizes3)
    with pd.option_context("display.width", 250, "display.max_colwidth", 120):
        p("\nK = 3 per facet:\n" + rec.to_string(index=False))
        p("\nK = 1, 2, 3 diagnostic:\n" + diag.to_string(index=False))
    p("\nK = 1 vs K = 3 contending sets:\n" + relation(reps[1][0], reps[3]))
    p("K = 1 exponents: " + top(NAMES, reps[1][0].exponents, 6))
    stab = []
    for s in seeds:
        e = fit_k(M, 3, tau, s)
        r = reports(e, M)
        sig = " | ".join(sorted("+".join(sorted(contend(x))) for x in r))
        stab.append({"seed": s, "objective_": e.objective_, "frac_above_": e.frac_above_,
                     "shares (sorted)": sorted(round(float(x), 3) for x in e.facet_share_),
                     "contending sets": sig})  # fmt: skip
    stab = pd.DataFrame(stab)
    with pd.option_context("display.width", 300, "display.max_colwidth", 200):
        p("\nK = 3 stability over seeds:\n" + stab.to_string(index=False))
    if make_figures:
        save_figures(regime, fits[3], M, reps[3], tau, figs)
    return {
        "figs": figs,
        "tau": tau,
        "fits": fits,
        "reports": reps,
        "record": rec,
        "diag": diag,
        "stab": stab,
    }


def main(argv=None):
    """Run both regimes."""
    for regime in REGIMES:
        run_regime(regime)


if __name__ == "__main__":
    main(sys.argv[1:])
