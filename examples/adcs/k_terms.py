"""K = 1, 2, 3 posynomial fits of the two cubesat datasets (WP9, D-6).

Run ``uv run python examples/adcs/k_terms.py``. Feasibility filter, conditioning and
temperature selection as in the paper; prints the per-term record. Nothing is simulated.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder

from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    select_temperature,
)
from hyperbolic_trade_space.plotting import PARTICIPATION

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "v2"  # the data of record (WP23)
REGIMES = {"primary": "adcs_designs_cubesat_gains.csv", "stock": "adcs_designs_cubesat.csv"}
ATTRS = [
    "settling_time_s", "pointing_error_deg", "total_mass_kg", "control_effort",
    "power_margin_w", "energy_balance_wh", "eclipse_reserve_wh", "peak_slew_power_w", "dod_eclipse",
]  # fmt: skip
SHORT = dict(zip(ATTRS, [
    "settling time", "pointing error", "total mass", "control effort",
    "power margin", "energy balance", "eclipse reserve", "peak slew power", "depth of discharge",
], strict=True))  # fmt: skip
ORIENT = dict(zip(ATTRS, [-1, -1, -1, -1, +1, +1, +1, -1, -1], strict=True))
WHEELS, TRACKERS = ["small", "medium", "large"], ["coarse", "medium", "fine"]
DESIGN_VARS = ["panel_span_m", "battery_wh", "Kp", "Kd"]
NAMES = [SHORT[a] for a in ATTRS]


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


def select_tau(M, K, target=0.10):
    """tau of the K-term fit by the K = 1 criterion: a tenth of designs above V = 1."""
    return select_temperature(
        M, target_frac_above=target, bounds=(3, 1e3), n_terms=K, random_state=0
    )


def reports(est, M, band=None):
    """List of per-term TensionReports (a one-element list at K = 1), the guard per term.

    ``case.term_reports``: every term is reported from the estimator; the association reading of
    a term without ten near-frontier rows is not drawn (``case.has_reading``).
    """
    import case

    band = (1 / float(est.temperature)) if band is None else band
    return case.term_reports(est, M, band)


def top(names, w, n=3):
    """The n largest exponents, named."""
    return ", ".join(f"{names[j]} {w[j]:.3f}" for j in np.argsort(-w)[:n])


def contend(rep):
    """Contending set as sorted metric names (largest exponent first)."""
    order = np.argsort(-rep.contending_exponents)
    return [NAMES[rep.contending_set[i]] for i in order]


def term_record(est, reps, rows):
    """One row of facts per term."""
    out = []
    for k, rep in enumerate(reps):
        out.append({
            "term": k + 1, "rows": int(rows[k]), "contending set": ", ".join(contend(rep)),
            "n_lemma": rep.n_lemma, "largest exponents": top(NAMES, rep.exponents),
            "near-frontier": rep.n_near_frontier, "reach beta_k": float(est.log_offset_[k]),
            "share": float(est.term_share_[k]) if est.n_terms > 1 else 1.0,
            "gap G_k": float(est.termination_.gaps[k]),
        })  # fmt: skip
    return pd.DataFrame(out)


def _slice(est, U, labels, band, j, k):
    """Terms drawable in the (j, k) log plane, with their exponents and offsets there.

    A term is drawn only where it has weight on both plotted metrics (exponents above the
    plotting module's participation threshold, the tension report's).
    """
    W, keep, ws, bs = est.exponents_, [], [], []
    rest = [i for i in range(U.shape[1]) if i not in (j, k)]
    for f in range(len(W)):
        s = W[f, j] + W[f, k]
        near = (labels == f"cell {f + 1}") & (np.abs(est.training_log_v_) < band)
        if min(W[f, j], W[f, k]) <= PARTICIPATION or not near.any():
            continue
        bs.append((est.log_offset_[f] - W[f, rest] @ np.median(U[near][:, rest], axis=0)) / s)
        ws.append([W[f, j] / s, W[f, k] / s])
        keep.append(f)
    return keep, ws, bs


def slice_pairs(est):
    """Metric pairs for the log-plane slices: per term its two largest exponents, de-duplicated."""
    pairs = []
    for w in est.exponents_:
        pair = tuple(sorted(int(i) for i in np.argsort(-w)[:2]))
        if pair not in pairs:
            pairs.append(pair)
    return pairs


def relation(rep1, reps3):
    """How the K = 1 contending set relates to the K = 3 terms' sets."""
    s1 = {NAMES[j] for j in rep1.contending_set}
    sets = [{NAMES[j] for j in r.contending_set} for r in reps3]
    union = set().union(*sets)
    lines = [f"K=1 set ({len(s1)}): {sorted(s1)}"]
    for k, s in enumerate(sets):
        lines.append(
            f"  term {k + 1}: shares {len(s & s1)} of {len(s)}; only in term: {sorted(s - s1)}; "
            f"K=1 members absent: {sorted(s1 - s)}"
        )
    lines.append(
        f"  union of terms ({len(union)}): K=1 subset of union: {s1 <= union}; "
        f"in union not in K=1: {sorted(union - s1)}; in K=1 not in union: {sorted(s1 - union)}"
    )
    return "\n".join(lines)


def certificate(est):
    """The fit's stopping record as columns: max term gap, status, margin, radius, bound."""
    t = est.termination_
    return {"max gap": t.max_gap, "status": t.status, "gamma": t.gamma, "radius": t.radius,
            "bound": t.bound}  # fmt: skip


def summary(fits, M):
    """One row per K: objective, fraction above V = 1, term rows and shares, certificate."""
    rows = []
    for K, e in fits.items():
        sizes = np.bincount(e.cell_, minlength=K) if K > 1 else [len(M)]
        share = e.term_share_ if K > 1 else [1.0]
        rows.append({"K": K, "tau": round(float(e.temperature), 2),
                     "band 1/tau": round(1 / float(e.temperature), 4),
                     "objective_": e.objective_, "frac_above_": e.frac_above_,
                     "term rows": list(map(int, sizes)),
                     "term shares": [round(float(x), 3) for x in share],
                     **certificate(e)})  # fmt: skip
    return pd.DataFrame(rows)


def run_regime(regime, seeds=range(5), n_max=None, verbose=True):
    """Fit one regime at K = 1, 2, 3 with tau re-selected at each K; print and return the record."""
    feasible, M = load_metrics(DATA / REGIMES[regime], n_max)
    taus = {K: select_tau(M, K) for K in (1, 2, 3)}
    fits = {K: fit_k(M, K, taus[K]) for K in taus}
    # near-frontier rows (the reports) are those within the K = 1 band at every K:
    # at the re-selected tau the K-term bands are narrower and leave terms with 3 to 6 rows
    band = 1 / taus[1]
    reps = {K: reports(fits[K], M, band) for K in fits}
    fixed = {K: fits[1] if K == 1 else fit_k(M, K, taus[1]) for K in (1, 2, 3)}
    p = print if verbose else (lambda *a, **k: None)
    p(f"\n{'=' * 78}\nREGIME {regime}: {REGIMES[regime]}; feasible {len(feasible)}; "
      "tau re-selected at each K (target 0.10 of designs above V = 1); "
      f"near-frontier band for reports and slices {band:.4f} (K = 1's)")  # fmt: skip
    diag = summary(fits, M)
    fixed_diag = summary(fixed, M)
    with pd.option_context("display.width", 250, "display.max_colwidth", 140):
        p("\nRE-SELECTED fits, K = 1, 2, 3:\n" + diag.to_string(index=False))
        for K in (2, 3):
            sizes = np.bincount(fits[K].cell_, minlength=K)
            rec_k = term_record(fits[K], reps[K], sizes)
            p(f"\nK = {K} per term (re-selected tau = {taus[K]:.2f}):\n"
              + rec_k.to_string(index=False))  # fmt: skip
            p(f"\nK = 1 vs K = {K} contending sets:\n" + relation(reps[1][0], reps[K]))
            if K == 3:
                rec = rec_k
        p(f"\nK = 1 (tau = {taus[1]:.2f}) contending set and exponents: "
          + ", ".join(contend(reps[1][0])) + "\nK = 1 exponents: "
          + top(NAMES, reps[1][0].exponents, 6))  # fmt: skip
        p("\nDIAGNOSTIC, fixed tau (K = 1's tau reused at K = 2, 3):\n"
          + fixed_diag.to_string(index=False))  # fmt: skip
        fixed_rec = term_record(
            fixed[3], reports(fixed[3], M, band), np.bincount(fixed[3].cell_, minlength=3)
        )
        p("\nDIAGNOSTIC K = 3 per term at fixed tau:\n" + fixed_rec.to_string(index=False))
    stab = []
    for s in seeds:
        e = fit_k(M, 3, taus[3], s)
        r = reports(e, M, band)
        sig = " | ".join(sorted("+".join(sorted(contend(x))) for x in r))
        stab.append({"seed": s, "objective_": e.objective_, "frac_above_": e.frac_above_,
                     "shares (sorted)": sorted(round(float(x), 3) for x in e.term_share_),
                     **certificate(e), "contending sets": sig})  # fmt: skip
    stab = pd.DataFrame(stab)
    with pd.option_context("display.width", 300, "display.max_colwidth", 200):
        p(f"\nK = 3 stability over seeds at the re-selected tau = {taus[3]:.2f}:\n"
          + stab.to_string(index=False))  # fmt: skip
    return {
        "tau": taus[1],
        "taus": taus,
        "fits": fits,
        "reports": reps,
        "record": rec,
        "diag": diag,
        "fixed": fixed,
        "fixed_diag": fixed_diag,
        "stab": stab,
    }


def main(argv=None):
    """Run both regimes."""
    for regime in REGIMES:
        run_regime(regime)


if __name__ == "__main__":
    main(sys.argv[1:])
