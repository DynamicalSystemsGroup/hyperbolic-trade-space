"""WP45 test-record scripts: manifests, loud failure on a changed source, conditioning steps.

The data-dependent runs (``examples/*/run.py``) are not in the suite: they download archives. These
tests cover what does not need the data: each manifest names its source, DOI and licence (R-1);
``verify`` fails loudly when a file's size or hash is not the manifest's; the cleaning rules drop
what they say they drop; and where a cached archive is present its hash is checked against the
manifest.
"""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

EX = Path(__file__).resolve().parents[1] / "examples"
sys.path.insert(0, str(EX))
import fitkit  # noqa: E402


def _load(case, script):
    path = EX / case / script
    spec = importlib.util.spec_from_file_location(f"wp45_{case}_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("case", ["perovskite", "amniote", "wheat"])
def test_manifest_names_source_doi_licence(case):
    m = fitkit.load_manifest(EX / case / "manifest.toml")
    assert m["doi"].startswith("10.")
    assert m["licence"].startswith("CC")
    assert m["attribution"] and (m.get("url") or m.get("landing_page"))


@pytest.mark.parametrize("case", ["perovskite", "amniote"])
def test_cached_archive_matches_manifest(case):
    m = fitkit.load_manifest(EX / case / "manifest.toml")
    z = EX / case / "data" / m["file"]
    if not z.exists():
        pytest.skip("archive not fetched")
    fitkit.verify(z, m)


def test_verify_fails_loudly(tmp_path):
    f = tmp_path / "a.bin"
    f.write_bytes(b"abc")
    good = {"size": 3, "md5": fitkit.file_hash(f, "md5"), "sha256": fitkit.file_hash(f, "sha256")}
    fitkit.verify(f, good)
    with pytest.raises(RuntimeError, match="size"):
        fitkit.verify(f, {**good, "size": 4})
    with pytest.raises(RuntimeError, match="md5"):
        fitkit.verify(f, {**good, "md5": "0" * 32})
    with pytest.raises(RuntimeError, match="sha256"):
        fitkit.verify(f, {**good, "sha256": "0" * 64})


def test_perovskite_feasibility_rule():
    run = _load("perovskite", "run.py")
    df = pd.DataFrame(
        {
            "JV_default_Voc": [1.0, 1.1, np.nan, 0.0, 1.0],
            "JV_default_Jsc": [20.0, 21.0, 20.0, 20.0, 20.0],
            "JV_default_FF": [0.7, 0.8, 0.7, 0.7, 1.4],
        }
    )
    assert len(run.feasible(df)) == 2
    M = run.condition(run.feasible(df))
    assert M.shape == (2, 3) and (M > 0).all()


def test_amniote_sentinel_and_orientation(tmp_path):
    run = _load("amniote", "run.py")
    raw = pd.DataFrame(
        {
            "class": ["Mammalia"] * 6,
            "maximum_longevity_y": [10.0, 20, 30, 40, -999, 50],
            "litter_or_clutch_size_n": [1.0, 2, 3, 4, 5, 6],
            "litters_or_clutches_per_y": [1.0, 2, 3, 4, 5, 6],
            "female_maturity_d": [100.0, 200, 300, 400, 500, 600],
            "adult_body_mass_g": [10.0, 20, 30, 40, 50, 60],
        }
    )
    f = tmp_path / "t.csv"
    raw.to_csv(f, index=False)
    got = pd.read_csv(f, na_values=[-999])
    x = run.complete(got)
    assert len(x) == 5
    M = run.condition(x)
    # maturity is inverted: the latest-maturing species has the smallest metric
    assert np.argmin(M[:, 3]) == len(x) - 1
    Mp = run.condition(x, partial_out=True)
    assert Mp.shape == M.shape and (Mp > 0).all()


def test_wheat_derive_keeps_rows_with_both_yields():
    d = _load("wheat", "derive.py")
    df = pd.DataFrame(
        {"g": [5.0, 6.0, np.nan, 7.0], "s": [4.0, np.nan, 3.0, 0.0], "yr": [1, 2, 3, 4]}
    )
    x = d.derive(df, "g", "s", year="yr")
    assert list(x.columns) == ["grain", "straw", "yr"] and len(x) == 1
    with pytest.raises(KeyError, match="columns not in the file"):
        d.derive(df, "grain", "s")
    assert d.condition(x.assign(grain=[5.0], straw=[4.0])).shape == (1, 2)
