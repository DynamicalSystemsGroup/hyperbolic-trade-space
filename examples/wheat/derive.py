"""WP45 wheat test record: derive the grain-and-straw table from the manual download, then fit.

The download from e-RA is behind a form and was a manual step (``manifest.toml``). This script does
the rest from the zip or its ``yield_data.csv`` under ``examples/wheat/data/`` (ignored by git;
either is checked against the manifest):

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
import io
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import fitkit  # noqa: E402

fitkit.read_threads()

import pandas as pd  # noqa: E402


def derive(df, grain, straw, year=None, plot=None, treatment=None, cultivar=None, extra=()):
    """The straw-recorded subset: rows with both yields present and strictly positive.

    Raises ``KeyError`` naming a missing column, so a source that changed fails loudly.
    """
    keep = {c: c for c in (grain, straw, year, plot, treatment, cultivar, *extra) if c}
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
    from tradespace import LogAffinePreconditioner

    pre = LogAffinePreconditioner(orientation=1, shift=0.0, scaler="standard")
    return pre.fit_transform(x[["grain", "straw"]].to_numpy(float))


def harvest_index(x):
    """Grain over grain plus straw, per row (the harvest index on the recorded dry matter)."""
    return x["grain"] / (x["grain"] + x["straw"])


def level_biomass_correlation(x, tau, seed=0):
    """Correlation of log V (K = 1 at ``tau``) with log biomass (grain + straw), two decimals."""
    import numpy as np

    from tradespace import HyperbolicTradeSpace

    est = HyperbolicTradeSpace(temperature=tau, random_state=seed).fit(condition(x))
    log_v = est.score_samples(condition(x))
    log_b = np.log(x["grain"].to_numpy(float) + x["straw"].to_numpy(float))
    return round(float(np.corrcoef(log_v, log_b)[0, 1]), 2)


def check(path, m):
    """Verify the zip (the download of record) or the extracted CSV against the manifest."""
    name = Path(path).name
    if name == m["file"]:
        fitkit.verify(path, m)
    elif name == m["csv_file"]:
        fitkit.verify(path, {k[4:]: v for k, v in m.items() if k.startswith("csv_")})
    else:
        raise RuntimeError(f"{name} is neither {m['file']} nor {m['csv_file']} of the manifest")


def record(path):
    """Write the file's size and hashes into the manifest (a text edit, keys kept in place)."""
    path = Path(path)
    text = (HERE / "manifest.toml").read_text(encoding="utf-8")
    for key, val in (
        ("file", f'"{path.name}"'),
        ("size", str(path.stat().st_size)),
        ("md5", f'"{fitkit.file_hash(path, "md5")}"'),
        ("sha256", f'"{fitkit.file_hash(path, "sha256")}"'),
    ):
        text = re.sub(rf"^{key} = .*$", f"{key} = {val}", text, flags=re.M)
    (HERE / "manifest.toml").write_text(text, encoding="utf-8")


COLUMNS = {
    "grain": "grain",
    "straw": "straw",
    "year": "harvest_year",
    "plot": "plot",
    "treatment": "fertilizer_code",
    "cultivar": "cultivar",
    "nitrogen": "total_fertilizer_n_amount",
    "cropping": "cropping",
    "section": "section",
}
PRIMARY = "primary"


def read_table(path, m):
    """The yield table from the CSV, or from inside the zip; '*' (no value) reads as missing."""
    path = Path(path)
    if path.name == m["file"]:
        with zipfile.ZipFile(path) as zf:
            raw = zf.read(m["csv_path_in_zip"])
        return pd.read_csv(io.BytesIO(raw), low_memory=False, na_values=["*"])
    return pd.read_csv(path, low_memory=False, na_values=["*"])


def variants(x):
    """The primary table and the one-thing-changed sensitivities, as (label, frame)."""
    yield PRIMARY, x
    yield "winter_wheat_only", x[x["cropping"] == "winter wheat"]
    yield "n_at_least_96", x[x["nitrogen"] >= 96]
    yield "modern_only", x[x["cultivar"] != "Cappelle Desprez"]
    yield "n_at_least_96_modern", x[(x["nitrogen"] >= 96) & (x["cultivar"] != "Cappelle Desprez")]
    yield "section_1_only", x[x["section"] == 1]


def cultivar_table(x):
    """Per cultivar at N >= 96: rows, years, median biomass (grain + straw) and harvest index."""
    y = x[x["nitrogen"] >= 96].copy()
    y["biomass"] = y["grain"] + y["straw"]
    y["hi"] = harvest_index(y)
    g = y.groupby("cultivar").agg(
        rows=("grain", "size"),
        first=("year", "min"),
        last=("year", "max"),
        biomass=("biomass", "median"),
        grain=("grain", "median"),
        hi=("hi", "median"),
    )
    return {
        k: {kk: float(vv) for kk, vv in v.items()} for k, v in g.sort_values("first").iterrows()
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--record", action="store_true")
    for k, v in COLUMNS.items():
        ap.add_argument(f"--{k}", default=v)
    a = ap.parse_args(argv)
    if a.record:
        return record(a.file)
    m = fitkit.load_manifest(HERE / "manifest.toml")
    check(a.file, m)
    df = read_table(a.file, m)
    if a.list:
        print(list(df.columns))
        print(df.head())
        return None
    keep = {
        a.grain: "grain",
        a.straw: "straw",
        a.year: "year",
        a.plot: "plot",
        a.treatment: "treatment",
        a.cultivar: "cultivar",
        a.nitrogen: "nitrogen",
        a.cropping: "cropping",
        a.section: "section",
    }
    x = derive(
        df,
        a.grain,
        a.straw,
        a.year,
        a.plot,
        a.treatment,
        a.cultivar,
        extra=[a.nitrogen, a.cropping, a.section],
    )
    x = x.rename(columns={k: v for k, v in keep.items() if k not in ("grain", "straw")})
    (HERE / "derived").mkdir(exist_ok=True)
    x.to_csv(HERE / "derived" / "grain_straw.csv", index=False)
    (HERE / "derived" / "LICENCE-DATA.txt").write_text(
        f"{m['licence_text']}\n\nAttribution: {m['attribution']}\nSource: {m['landing_page']}\n"
        f"Licence: {m['licence_url']}\nThis table is derived: rows with grain and straw both "
        "recorded and positive, selected columns only.\n",
        encoding="utf-8",
    )
    results = {
        "counts": {
            "rows_in_table": len(df),
            "grain_present": int(pd.to_numeric(df[a.grain], errors="coerce").notna().sum()),
            "straw_present": int(pd.to_numeric(df[a.straw], errors="coerce").notna().sum()),
            "both_positive": len(x),
        },
        "cultivars": cultivar_table(x),
        "runs": {},
    }
    for label, frame in variants(x):
        res = fitkit.fit_read(
            condition(frame),
            ["grain", "straw"],
            k2=(label == PRIMARY),
            taus=(3.0, 10.0, 30.0, 100.0),
        )
        res["rows"] = len(frame)
        res["harvest_index_median"] = float(harvest_index(frame).median())
        if label == PRIMARY:
            res["corr_log_v_log_biomass"] = level_biomass_correlation(frame, res["tau_selected"])
        results["runs"][label] = res
        print(label, res["n"], res["n_lemma"], res["exponents_k1"], flush=True)
    fitkit.dump(results, HERE / "results.json")
    return None


if __name__ == "__main__":
    main()
