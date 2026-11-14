"""WP45 wheat test record: derive the grain-and-straw table from the manual download, then fit.

The download from e-RA is behind a form and is a manual step (``manifest.toml``). This script does
the rest from the CSV the supervisor places under ``examples/wheat/data/`` (ignored by git):

``uv run python examples/wheat/derive.py --list FILE.csv``   show the columns and the first rows;
``uv run python examples/wheat/derive.py --record FILE``      write the file's size and hashes into
                                                            ``manifest.toml``;
``uv run python examples/wheat/derive.py FILE.csv --grain COL --straw COL --year COL [--plot COL]
[--treatment COL] [--cultivar COL]``   derive ``derived/grain_straw.csv`` (rows with both yields
present and positive; the derived table is committed with ``LICENCE-DATA.txt`` beside it, CC BY 4.0
allows it) and fit ``results.json``.

Two metrics, both larger is better, orientation +1, shift 0, standard scaler of the log; the surface
is a line in log units and the simplex a segment.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import fitkit  # noqa: E402

fitkit.read_threads()

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def derive(df, grain, straw, year=None, plot=None, treatment=None, cultivar=None):
    """The straw-recorded subset: rows with both yields present and strictly positive.

    Raises ``KeyError`` naming a missing column, so a source that changed fails loudly.
    """
    keep = {c: c for c in (grain, straw, year, plot, treatment, cultivar) if c}
    missing = [c for c in keep if c not in df.columns]
    if missing:
        raise KeyError(f"columns not in the file: {missing}; have {list(df.columns)}")
    x = df[list(keep)].copy()
    x[grain] = pd.to_numeric(x[grain], errors="coerce")
    x[straw] = pd.to_numeric(x[straw], errors="coerce")
    x = x.dropna(subset=[grain, straw])
    x = x[(x[grain] > 0) & (x[straw] > 0)]
    return x.rename(columns={grain: "grain", straw: "straw"})


def condition(x):
    """Grain and straw as larger-is-better metrics (orientation +1, standard log scaler)."""
    from hyperbolic_trade_space import LogAffinePreconditioner

    pre = LogAffinePreconditioner(orientation=1, shift=0.0, scaler="standard")
    return pre.fit_transform(x[["grain", "straw"]].to_numpy(float))


def harvest_index(x):
    """Grain over grain plus straw, per row (the harvest index on the recorded dry matter)."""
    return x["grain"] / (x["grain"] + x["straw"])


def record(path):
    """Write the file's size and hashes into the manifest (a text edit, keys kept in place)."""
    path = Path(path)
    text = (HERE / "manifest.toml").read_text()
    for key, val in (
        ("file", f'"{path.name}"'),
        ("size", str(path.stat().st_size)),
        ("md5", f'"{fitkit.file_hash(path, "md5")}"'),
        ("sha256", f'"{fitkit.file_hash(path, "sha256")}"'),
    ):
        text = re.sub(rf"^{key} = .*$", f"{key} = {val}", text, flags=re.M)
    (HERE / "manifest.toml").write_text(text)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--record", action="store_true")
    for k in ("grain", "straw", "year", "plot", "treatment", "cultivar"):
        ap.add_argument(f"--{k}")
    a = ap.parse_args(argv)
    if a.record:
        return record(a.file)
    m = fitkit.load_manifest(HERE / "manifest.toml")
    if m["md5"]:
        fitkit.verify(a.file, m)
    df = pd.read_csv(a.file, low_memory=False)
    if a.list or not (a.grain and a.straw):
        print(list(df.columns))
        print(df.head())
        return None
    x = derive(df, a.grain, a.straw, a.year, a.plot, a.treatment, a.cultivar)
    (HERE / "derived").mkdir(exist_ok=True)
    x.to_csv(HERE / "derived" / "grain_straw.csv", index=False)
    (HERE / "derived" / "LICENCE-DATA.txt").write_text(
        f"{m['licence_text']}\n\nAttribution: {m['attribution']}\nSource: {m['landing_page']}\n"
        f"Licence: {m['licence_url']}\nThis table is derived: rows with grain and straw both "
        "recorded and positive, selected columns only.\n"
    )
    res = fitkit.fit_read(condition(x), ["grain", "straw"], taus=(3.0, 10.0, 30.0, 100.0, np.inf))
    res["rows"] = len(x)
    res["harvest_index_median"] = float(harvest_index(x).median())
    fitkit.dump(res, HERE / "results.json")
    print(res["n"], res["n_lemma"], res["exponents_k1"])
    return None


if __name__ == "__main__":
    main()
