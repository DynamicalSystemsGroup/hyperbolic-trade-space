"""WP59 wheat: the conditioning ladder and the chains, one change at a time from the primary rule.

``uv run python examples/wheat/variants.py`` reads the committed derived table
(``derived/grain_straw.csv``, 3,753 rows) and writes ``variants.json``. If the archive of record is
in ``examples/wheat/data/`` its hashes are checked against ``manifest.toml``; the derived table's
row count is checked against the record's either way.

Primary rule (the WP45 record): grain and straw, both larger is better, orientation +1, shift 0,
standard scaler of the log; the temperature is the one that puts a tenth of the rows above the
surface (bounds 3 to 10^4). Each variant changes one thing and says what in ``rule``.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import fitkit  # noqa: E402

fitkit.read_threads()

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from derive import PRIMARY, condition, harvest_index  # noqa: E402
from derive import variants as record_subsets  # noqa: E402

ROWS_OF_RECORD = 3753
SEED = 0


def standard_exp(logs):
    """Centre and scale each log column to unit standard deviation, then exponentiate."""
    z = (logs - logs.mean(axis=0)) / logs.std(axis=0)
    return np.exp(z)


def quantile_map(raw):
    """Rank-based metric: uniform quantile output u shifted into (0, 1], then exp(u').

    ``u' = (1 + (n - 1) u) / n`` puts the smallest row at 1/n and the largest at 1, so ``exp(u')``
    is strictly positive (between 1 and e) and larger is better.
    """
    from sklearn.preprocessing import QuantileTransformer

    n = raw.shape[0]
    qt = QuantileTransformer(
        n_quantiles=min(1000, n), output_distribution="uniform", random_state=SEED
    )
    u = qt.fit_transform(raw)
    return np.exp((1.0 + (n - 1) * u) / n)


def pca_rewrite(M, flip=()):
    """PCA on the standardized log-metrics, scores centred and exponentiated.

    Each component is oriented so that its largest-magnitude loading is positive (the first on
    ties); ``flip`` lists components whose sign is then reversed. Returns the rewritten metrics,
    the loadings (rows are components, columns the log-metrics) and the explained-variance ratio.
    """
    from sklearn.decomposition import PCA

    Z = np.log(M)
    pca = PCA().fit(Z)
    L = pca.components_.copy()
    for k in range(L.shape[0]):
        lead = int(np.argmax(np.abs(L[k]) >= np.abs(L[k]).max() - 1e-12))
        if L[k, lead] < 0:
            L[k] = -L[k]
    for k in flip:
        L[k] = -L[k]
    scores = (Z - pca.mean_) @ L.T
    return np.exp(scores), L, pca.explained_variance_ratio_


def clean(obj):
    """JSON-ready: numpy scalars to Python, nan and inf to None."""
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [clean(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return clean(obj.tolist())
    if isinstance(obj, (np.floating, float)):
        return None if not np.isfinite(obj) else float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    return obj


def read(M, names, extra=None):
    """The record's reading of one variant: fit_read plus elasticities and the spread direction."""
    from tradespace import HyperbolicTradeSpace, trade_off_report

    res = fitkit.fit_read(M, names, taus=(), k2=True, seed=SEED)
    res.pop("by_temperature", None)
    tau = res["tau_selected"]
    est = HyperbolicTradeSpace(temperature=tau, random_state=SEED).fit(M)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rep = trade_off_report(est, M)
    res["elasticities"] = {
        f"{names[j]}|{names[k]}": float(rep.elasticities[j, k])
        for j in range(len(names))
        for k in range(len(names))
        if j != k
    }
    res["log_spread"] = [float(s) for s in np.log(M).std(axis=0)]
    res["pca_after_fit"] = {
        "loadings": [dict(zip(names, map(float, row), strict=True)) for row in rep.spread_loadings],
        "explained": [float(v) for v in rep.explained_spread],
    }
    res["at_tau_bound"] = bool(tau <= 3.0 + 1e-6 or tau >= 1e4 - 1e-6)
    k2 = res.get("k2")
    if k2 and isinstance(k2["contending_sets"], list):
        k2["ceiling_terms"] = [
            {"metric": s[0], "share": sh}
            for s, sh in zip(k2["contending_sets"], k2["term_share"], strict=True)
            if len(s) == 1
        ]
    if extra:
        res.update(extra)
    return clean(res)


def build(x):
    """Yield (label, rule, rows, M, names, extra) for every variant, primary first."""
    gs = ["grain", "straw"]
    raw = x[gs].to_numpy(float)
    primary_rule = (
        "grain and straw, orientation +1, shift 0, standard scaler of the log; "
        "temperature at a tenth of rows above the surface"
    )
    yield PRIMARY, primary_rule, len(x), condition(x), gs, {}

    from tradespace import LogAffinePreconditioner

    yield (
        "no_scaler",
        "scaler None: the pure log of the raw yields (t per hectare)",
        len(x),
        LogAffinePreconditioner(orientation=1, shift=0.0, scaler=None).fit_transform(raw),
        gs,
        {},
    )
    yield (
        "robust",
        "robust scaler of the log (unit interquartile range)",
        len(x),
        LogAffinePreconditioner(orientation=1, shift=0.0, scaler="robust").fit_transform(raw),
        gs,
        {},
    )
    yield (
        "quantile_uniform",
        "QuantileTransformer uniform output u, shifted into (0, 1] as (1 + (n - 1) u) / n, then "
        "exp: m = exp(u') in (1, e]",
        len(x),
        quantile_map(raw),
        gs,
        {},
    )
    lo, hi = np.percentile(raw, [1, 99], axis=0)
    capped = np.clip(raw, lo, hi)
    yield (
        "capped_1_99",
        "each yield capped at its 1st and 99th percentile before the primary conditioning",
        len(x),
        LogAffinePreconditioner(orientation=1, shift=0.0, scaler="standard").fit_transform(capped),
        gs,
        {
            "cap_low": dict(zip(gs, map(float, lo), strict=True)),
            "cap_high": dict(zip(gs, map(float, hi), strict=True)),
        },
    )

    for label, frame in record_subsets(x):
        if label == PRIMARY:
            continue
        yield (
            label,
            f"primary rule on the subset: {label.replace('_', ' ')}",
            len(frame),
            condition(frame),
            gs,
            {},
        )

    hi_ = harvest_index(x).to_numpy(float)
    bio = (x["grain"] + x["straw"]).to_numpy(float)
    for label, col, name, what in (
        ("plus_harvest_index", hi_, "harvest_index", "grain / (grain + straw)"),
        ("plus_biomass", bio, "biomass", "grain + straw"),
    ):
        M3 = LogAffinePreconditioner(orientation=1, shift=0.0, scaler="standard").fit_transform(
            np.c_[raw, col]
        )
        yield (
            label,
            f"primary rule with a third metric, {name} = {what}, larger is better; "
            "a function of the other two",
            len(x),
            M3,
            [*gs, name],
            {},
        )

    logs = np.log(raw)
    yr = x["year"].to_numpy(float)
    A = np.c_[np.ones_like(yr), yr - yr.mean()]
    coef, *_ = np.linalg.lstsq(A, logs, rcond=None)
    resid = logs - A @ coef
    yield (
        "year_partialled",
        "linear trend in year removed from each log-metric (least squares), then the standard "
        "scaler",
        len(x),
        standard_exp(resid),
        gs,
        {
            "trend_per_year": dict(zip(gs, map(float, coef[1]), strict=True)),
            "trend_share_of_variance": {
                g: float(1 - resid[:, i].var() / logs[:, i].var()) for i, g in enumerate(gs)
            },
        },
    )

    M = condition(x)
    S, L, evr = pca_rewrite(M)
    pca_extra = {
        "loadings": [dict(zip(gs, map(float, row), strict=True)) for row in L],
        "explained_variance_ratio": [float(v) for v in evr],
    }
    for label, flip, rule in (
        (
            "pca_before_fit",
            (),
            "PCA of the primary standardized log-metrics; scores centred and exponentiated; each "
            "component's largest-magnitude loading made positive",
        ),
        (
            "pca_before_fit_pc2_flipped",
            (1,),
            "as pca_before_fit with the second component's sign reversed",
        ),
    ):
        S, L2, _ = pca_rewrite(M, flip=flip)
        yield label, rule, len(x), S, ["pc1", "pc2"], {**pca_extra, "loadings_used": L2.tolist()}


def pulled_back(res, loadings):
    """Exponents of a rotated fit on the standardized log grain and straw: L^T w."""
    w = np.array([res["exponents_k1"]["pc1"], res["exponents_k1"]["pc2"]])
    return dict(zip(["grain", "straw"], map(float, np.array(loadings).T @ w), strict=True))


def main():
    m = fitkit.load_manifest(HERE / "manifest.toml")
    z = HERE / "data" / m["file"]
    if z.exists():
        fitkit.verify(z, m)
    csv = HERE / "derived" / "grain_straw.csv"
    x = pd.read_csv(csv)
    if len(x) != ROWS_OF_RECORD:
        raise RuntimeError(f"{csv.name}: {len(x)} rows, the record has {ROWS_OF_RECORD}")
    out = {
        "derived_sha256": fitkit.file_hash(csv, "sha256"),
        "archive_checked": z.exists(),
        "rows": len(x),
        "variants": {},
    }
    for label, rule, rows, M, names, extra in build(x):
        res = read(M, names, extra={"rule": rule, "rows": rows, **extra})
        if label.startswith("pca_before_fit"):
            res["pulled_back_exponents"] = clean(pulled_back(res, extra["loadings_used"]))
        out["variants"][label] = res
        print(label, res["n"], res["n_lemma"], flush=True)
    fitkit.dump(out, HERE / "variants.json")


if __name__ == "__main__":
    main()
