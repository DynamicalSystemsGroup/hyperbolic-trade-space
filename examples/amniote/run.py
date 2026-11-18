"""WP45 amniote test record: fetch, condition, fit, read.

``uv run python examples/amniote/run.py`` fetches the archive named in ``manifest.toml`` into
``examples/amniote/data/`` (ignored by git; hash-checked), conditions the complete-case life-history
table, fits K = 1 and K = 2 and writes ``results.json`` beside this file. The expected n-lemma is
in ``tests/data/wp45/amniote/test-record.md``, committed before the first fit.

Conditioning rule (the primary table, "keep mass"): complete cases of maximum longevity, litter or
clutch size, litters or clutches per year, female maturity and adult body mass, with the -999
sentinel read as missing. Metrics: longevity (larger is better), litter size (larger), litters per
year (larger), earliness of maturity (maturity in days, smaller is better, orientation -1);
shift 0,
standard scaler of the log. Body mass is the covariate: the primary table keeps its effect in the
metrics; the variant "partial_out_mass" removes the linear effect of log mass from every log metric.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import fitkit  # noqa: E402

fitkit.read_threads()

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

COLS = [
    "maximum_longevity_y",
    "litter_or_clutch_size_n",
    "litters_or_clutches_per_y",
    "female_maturity_d",
]
NAMES = ["longevity", "litter_size", "litters_per_year", "earliness"]
ORIENT = [1, 1, 1, -1]
MASS = "adult_body_mass_g"
PRIMARY = "keep_mass"


def load(manifest=None, cache=HERE / "data"):
    """The raw table with the -999 sentinel read as missing."""
    m = manifest or fitkit.load_manifest(HERE / "manifest.toml")
    folder = fitkit.fetch_zip(m, cache)
    return pd.read_csv(folder / m["table"], low_memory=False, na_values=[m["sentinel"]])


def complete(df, cols=COLS):
    """Complete cases of the metric columns and the mass covariate, strictly positive."""
    x = df.dropna(subset=[*cols, MASS])
    return x[(x[[*cols, MASS]] > 0).all(axis=1)]


def condition(x, cols=COLS, orient=ORIENT, partial_out=False, scaler="standard"):
    """Log-affine conditioning; optionally remove the linear effect of log mass first.

    With ``partial_out`` the log of each attribute (with its orientation sign) is regressed on
    log mass by least squares and the residual is conditioned, so the metric is how a species
    stands against others of its mass.
    """
    from sklearn.preprocessing import StandardScaler

    from tradespace import LogAffinePreconditioner

    A = x[cols].to_numpy(float)
    if not partial_out:
        return LogAffinePreconditioner(orientation=orient, shift=0.0, scaler=scaler).fit_transform(
            A
        )
    z = np.log(A) * np.asarray(orient, float)
    lm = np.log(x[MASS].to_numpy(float))
    D = np.column_stack([np.ones_like(lm), lm])
    coef, *_ = np.linalg.lstsq(D, z, rcond=None)
    res = z - D @ coef
    sc = StandardScaler() if scaler == "standard" else None
    return np.exp(sc.fit_transform(res) if sc else res)


def variants(raw):
    """The primary table and the one-thing-changed sensitivities, as (label, frame, options)."""
    x = complete(raw)
    yield PRIMARY, x, {}
    yield "partial_out_mass", x, {"partial_out": True}
    yield "maturity_not_inverted", x, {"orient": [1, 1, 1, 1]}
    yield "scaler_robust", x, {"scaler": "robust"}
    for cls in ("Mammalia", "Aves", "Reptilia"):
        yield f"class_{cls}", x[x["class"] == cls], {}
    yield "mammals_partial_out", x[x["class"] == "Mammalia"], {"partial_out": True}
    g = complete(raw, [*COLS, "gestation_d"])
    yield (
        "mammals_with_gestation",
        g,
        {
            "cols": [*COLS, "gestation_d"],
            "orient": [*ORIENT, -1],
            "names": [*NAMES, "gestation_speed"],
        },
    )


def main():
    raw = load()
    cols_all = [*COLS, MASS]
    counts = {
        "rows_in_table": len(raw),
        **{f"present_{c}": int(raw[c].notna().sum()) for c in cols_all},
        "complete_cases": len(complete(raw)),
        **{f"complete_{k}": int(v) for k, v in complete(raw)["class"].value_counts().items()},
        "complete_orders": int(complete(raw)["order"].nunique()),
        "complete_with_gestation": len(complete(raw, [*COLS, "gestation_d"])),
    }
    results = {"counts": counts, "runs": {}}
    for label, frame, opt in variants(raw):
        cols = opt.get("cols", COLS)
        names = opt.get("names", NAMES)
        M = condition(
            frame,
            cols=cols,
            orient=opt.get("orient", ORIENT),
            partial_out=opt.get("partial_out", False),
            scaler=opt.get("scaler", "standard"),
        )
        res = fitkit.fit_read(M, names, k2=label in (PRIMARY, "partial_out_mass"))
        res["rows"] = len(frame)
        results["runs"][label] = res
        print(
            label, res["n"], res["n_lemma"], res["contending_set"], res["exponents_k1"], flush=True
        )
    fitkit.dump(results, HERE / "results.json")


if __name__ == "__main__":
    main()
