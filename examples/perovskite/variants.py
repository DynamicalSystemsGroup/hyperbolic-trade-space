"""WP59 conditioning ladder and chains on the perovskite table.

``uv run --frozen python examples/perovskite/variants.py`` loads the cached archive through
``run.load`` (manifest checks run on every load), fits the record's primary rule and the variants
below, one change at a time, then the chains with PCA (and ICA where PCA changes the reading), and
writes ``variants.json`` beside this file. The fit, the temperature rule (a tenth of rows above the
surface) and the seeds are those of ``run.py``. The existing chain, PCA after the fit on the
near-frontier chart, is the ``spread_first_direction`` of every fit.

The table has no covariate and no time or cost metric to orient: Voc, Jsc and FF are
larger-is-better as recorded.

Chains: the screen is PCA on the conditioned log-metrics; a column is carried when the first two
components hold at least 0.75 of its variance (``CARRY``), and the carried columns are fitted. The
rewriting fits the first k scores as metrics (``variantkit.signed_scores``: centred, unit spread,
exponentiated, each component signed so its largest loading is positive).
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
import run  # noqa: E402
import variantkit  # noqa: E402

CARRY = 0.75
SCANS = {"default": "JV_default_", "reverse": "JV_reverse_scan_", "forward": "JV_forward_scan_"}
QUANT = ["Voc", "Jsc", "FF", "PCE"]
JV12 = [f"{p}{q}" for p in SCANS.values() for q in QUANT]
JV12_NAMES = [f"{s}_{q}" for s in SCANS for q in QUANT]
STAB = ["Stability_PCE_end_of_experiment", "Stability_PCE_T80"]
JV_STAB = [*(f"JV_default_{q}" for q in QUANT), *STAB]
JV_STAB_NAMES = [*(f"default_{q}" for q in QUANT), "end_of_experiment_PCE", "T80_hours"]


def complete(raw, cols):
    """Rows with every column present and positive, and every fill factor at most 1."""
    x = raw.dropna(subset=cols)
    x = x[(x[cols] > 0).all(axis=1)]
    for c in cols:
        if c.endswith("_FF"):
            x = x[x[c] <= 1.0]
    return x


def ladder(raw):
    """The ladder as (label, rule, frame, metric columns, names, options)."""
    x = run.feasible(raw)
    cols, names = run.ATTR, run.NAMES
    yield (
        "primary",
        "record's rule: Voc, Jsc, FF of the default scan, log, standard scaler",
        x,
        cols,
        names,
        {},
    )
    yield (
        "no_scaler",
        "pure log, no scaler (metric = attribute in V, mA/cm2, fraction)",
        x,
        cols,
        names,
        {"scaler": None},
    )
    yield (
        "robust_scaler",
        "robust scaler of the log (median and interquartile range)",
        x,
        cols,
        names,
        {"scaler": "robust"},
    )
    yield (
        "quantile",
        "QuantileTransformer uniform of each attribute, shifted into (0, 1]",
        x,
        cols,
        names,
        {"quantile": True},
    )
    yield (
        "extremes_capped",
        "Voc at most 2 V and Jsc at most 40 mA/cm2 (record's S1)",
        x[(x.JV_default_Voc <= 2.0) & (x.JV_default_Jsc <= 40.0)],
        cols,
        names,
        {},
    )
    yield (
        "pce_added",
        "derived PCE added as a fourth metric (record's S6)",
        run.feasible(raw, [*cols, "JV_default_PCE"]),
        [*cols, "JV_default_PCE"],
        [*names, "PCE"],
        {},
    )


def metrics(frame, cols, opt):
    """The conditioned metrics of one frame."""
    if opt.get("quantile"):
        return variantkit.quantile_metrics(frame[cols].to_numpy(float), [1] * len(cols))
    return run.condition(frame, opt.get("scaler", "standard"), cols)


def screen(M, names):
    """PCA screen of conditioned metrics: communalities in the first two components and loadings."""
    Z = np.log(M)
    comm, p = variantkit.communality(Z, 2)
    carried = [n for n, c in zip(names, comm, strict=True) if c >= CARRY]
    return {
        "communality_first_two": dict(zip(names, map(float, comm), strict=True)),
        "explained_variance_ratio": [float(r) for r in p.explained_variance_ratio_],
        "loadings": [dict(zip(names, map(float, row), strict=True)) for row in p.components_],
        "carried": carried,
        "rule": f"carried when the first two components hold at least {CARRY} of its variance",
    }


def rewrite(M, names, kind, k):
    """Fit the first k PCA or ICA scores of the conditioned log-metrics as metrics."""
    S, W, ratios = variantkit.signed_scores(np.log(M), kind, k)
    comp = [f"{kind.upper()}{i + 1}" for i in range(k)]
    res = variantkit.fit_variant(S, comp, k2=True)
    res["components"] = [dict(zip(names, map(float, w), strict=True)) for w in W]
    if ratios:
        res["explained_variance_ratio"] = ratios
    res["rule"] = (
        f"first {k} {kind.upper()} scores of the conditioned log-metrics, centred, unit spread, "
        "exponentiated; each component signed so its largest loading is positive"
    )
    return res


def chain(frame, cols, names, label):
    """The screen, the fit of the carried columns, and the rewritings of one table."""
    out = {"rows": len(frame), "columns": names}
    M = metrics(frame, cols, {})
    base = variantkit.fit_variant(M, names, k2=True)
    out["all_columns_fit"] = base
    sc = screen(M, names)
    out["screen"] = sc
    keep = [i for i, n in enumerate(names) if n in sc["carried"]]
    if 2 <= len(keep) < len(names):
        sub = variantkit.fit_variant(M[:, keep], [names[i] for i in keep], k2=True)
        sub["rule"] = "the carried columns of the screen, primary conditioning"
        out["screened_fit"] = sub
    else:
        out["screened_fit"] = {
            "note": "the screen carries "
            f"{len(keep)} of {len(names)} columns, so there is no smaller table to fit"
        }
    ks = [2, 3] if len(names) >= 3 else [2]
    out["pca_rewriting"] = {f"k{k}": rewrite(M, names, "pca", k) for k in ks}
    ref = set(base.get("contending_set", []))
    dropped = ref - set(sc["carried"])
    short = [k for k, r in out["pca_rewriting"].items() if r.get("n_lemma", 99) < int(k[1:])]
    changes = bool(dropped) or bool(short)
    out["pca_changes_reading"] = {
        "changed": changes,
        "screen_drops_from_contending_set": sorted(dropped),
        "rewritings_with_fewer_contending_scores_than_scores": short,
    }
    if changes:
        out["ica_rewriting"] = {f"k{k}": rewrite(M, names, "ica", k) for k in ks}
    print(label, "chain done", out["pca_changes_reading"]["changed"], flush=True)
    return out


def main():
    raw = run.load()
    out = {"ladder": {}, "chains": {}, "carry_threshold": CARRY}
    for label, rule, frame, cols, names, opt in ladder(raw):
        res = variantkit.fit_variant(metrics(frame, cols, opt), names, k2=True)
        res["rule"] = rule
        out["ladder"][label] = res
        print(label, res.get("n_lemma"), res.get("contending_set"), flush=True)
    x = run.feasible(raw)
    out["log_spread_of_attributes"] = {
        n: float(np.log(x[c]).std()) for n, c in zip(run.NAMES, run.ATTR, strict=True)
    }
    out["chains"]["device_metrics"] = chain(x, run.ATTR, run.NAMES, "device")
    out["chains"]["jv_twelve"] = chain(complete(raw, JV12), JV12, JV12_NAMES, "jv12")
    out["chains"]["jv_and_stability"] = chain(
        complete(raw, JV_STAB), JV_STAB, JV_STAB_NAMES, "jv_stab"
    )
    variantkit.dump(out, HERE / "variants.json")


if __name__ == "__main__":
    main()
