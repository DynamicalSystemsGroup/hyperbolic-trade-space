"""WP45 perovskite test record: fetch, condition, fit, read.

``uv run python examples/perovskite/run.py`` fetches the archive named in ``manifest.toml`` into
``examples/perovskite/data/`` (ignored by git; hash-checked), conditions the default-scan JV
attributes, fits K = 1 and K = 2, and writes ``results.json`` beside this file. The expected
n-lemma is in ``tests/data/wp45/perovskite/test-record.md``, committed before the first
fit.

Conditioning rule (the primary table): Voc, Jsc, FF of the default scan, all larger is better
(orientation +1, shift 0, standard scaler of the log); rows with a missing attribute, a zero or
negative value, or FF above 1 are dropped. PCE is derived (the product of the three over the input
power) and is set aside. The sensitivities below change one thing each.
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

ATTR = ["JV_default_Voc", "JV_default_Jsc", "JV_default_FF"]
NAMES = ["Voc", "Jsc", "FF"]
PRIMARY = "primary"


def load(manifest=None, cache=HERE / "data"):
    """The raw table (all 410 columns) from the verified archive."""
    m = manifest or fitkit.load_manifest(HERE / "manifest.toml")
    folder = fitkit.fetch_zip(m, cache)
    return pd.read_csv(folder / m["table"], low_memory=False)


def feasible(df, cols=ATTR):
    """Rows with every attribute present and positive, and FF at most 1."""
    x = df.dropna(subset=cols)
    x = x[(x[cols] > 0).all(axis=1)]
    return x[x["JV_default_FF"] <= 1.0]


def condition(x, scaler="standard", cols=ATTR):
    """Orientation +1 for every column: the metrics are the attributes, standardized in log."""
    from hyperbolic_trade_space import LogAffinePreconditioner

    pre = LogAffinePreconditioner(orientation=1, shift=0.0, scaler=scaler)
    return pre.fit_transform(x[cols].to_numpy(float))


def variants(raw):
    """The primary table and the one-thing-changed sensitivities, as (label, frame, options)."""
    x = feasible(raw)
    gap = pd.to_numeric(x["Perovskite_band_gap"], errors="coerce")
    yield PRIMARY, x, {}
    yield "caps_Voc2_Jsc40", x[(x.JV_default_Voc <= 2.0) & (x.JV_default_Jsc <= 40.0)], {}
    yield "scaler_robust", x, {"scaler": "robust"}
    yield "cells_only", x[x["Module"].astype(str) == "False"], {}
    yield "deduplicated", x.drop_duplicates(subset=ATTR), {}
    yield "gap_1.5_to_1.7", x[(gap >= 1.5) & (gap <= 1.7)], {}
    y = feasible(raw, [*ATTR, "JV_default_PCE"])
    yield "with_PCE", y, {"cols": [*ATTR, "JV_default_PCE"], "names": [*NAMES, "PCE"]}


def main():
    raw = load()
    counts = {
        "rows_in_table": len(raw),
        "complete_Voc_Jsc_FF": int(raw.dropna(subset=ATTR).shape[0]),
        "positive_all": int((raw.dropna(subset=ATTR)[ATTR] > 0).all(axis=1).sum()),
        "after_FF_le_1": len(feasible(raw)),
    }
    results = {"counts": counts, "runs": {}}
    for label, frame, opt in variants(raw):
        cols = opt.get("cols", ATTR)
        names = opt.get("names", NAMES)
        M = condition(frame, opt.get("scaler", "standard"), cols)
        res = fitkit.fit_read(
            M, names, k2=(label == PRIMARY), taus=(3.0, 10.0, 30.0, 100.0, np.inf)
        )
        res["rows"] = len(frame)
        results["runs"][label] = res
        print(
            label, res["n"], res["n_lemma"], res["contending_set"], res["exponents_k1"], flush=True
        )
    fitkit.dump(results, HERE / "results.json")


if __name__ == "__main__":
    main()
