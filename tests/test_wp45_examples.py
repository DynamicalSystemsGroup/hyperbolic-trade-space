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


def _record(case):
    return (EX.parent / "work-packages" / "WP45-rounds" / case / "test-record.md").read_text(
        encoding="utf-8"
    )


def _results(case):
    import json

    return json.loads((EX / case / "results.json").read_text(encoding="utf-8"))


def test_perovskite_record_quotes_the_results():
    r, text = _results("perovskite"), _record("perovskite")
    p = r["runs"]["primary"]
    assert f"{p['rows']:,}" in text and f"{r['counts']['rows_in_table']:,}" in text
    assert f"tau = {p['tau_selected']:.1f}" in text
    assert p["n_lemma"] == 3 and set(p["contending_set"]) == {"Voc", "Jsc", "FF"}
    for run in r["runs"].values():
        assert {"Voc", "Jsc"} <= set(run["contending_set"])
        assert run["association"]["Voc|Jsc"] < 0
    k2 = p["k2"]
    assert f"{k2['mean_slack']:.3f}" in text and f"{k2['mean_slack_k1']:.3f}" in text
    assert f"{k2['term_share'][0]:.3f}" in text


def test_amniote_record_quotes_the_results():
    r, text = _results("amniote"), _record("amniote")
    p = r["runs"]["keep_mass"]
    assert f"{r['counts']['complete_cases']:,}" in text
    assert f"{p['tau_selected']:.1f}" in text
    for label, run in r["runs"].items():
        if label != "maturity_not_inverted":
            assert {"longevity", "litter_size"} <= set(run["contending_set"]), label
    assert p["association"]["longevity|earliness"] < -0.9
    k2 = p["k2"]
    assert f"{k2['mean_slack']:.3f}" in text and f"{k2['mean_slack_k1']:.3f}" in text
    assert r["runs"]["maturity_not_inverted"]["n_lemma"] == 2


def test_wheat_record_quotes_the_results():
    r, text = _results("wheat"), _record("wheat")
    c, p = r["counts"], r["runs"]["primary"]
    for v in (c["rows_in_table"], c["grain_present"], c["straw_present"], c["both_positive"]):
        assert f"{v:,}" in text
    assert f"{p['tau_selected']:.1f}" in text
    page = (Path(__file__).resolve().parents[1] / "docs/examples/wheat.md").read_text(
        encoding="utf-8"
    )
    assert f"{p['corr_log_v_log_biomass']:.2f}" in page
    for label, run in r["runs"].items():
        assert run["n_lemma"] == 2, label
        assert run["association"]["grain|straw"] < 0, label
        assert f"{run['rows']:,}" in text, label
    k2 = p["k2"]
    assert f"{k2['mean_slack']:.3f}" in text and f"{k2['mean_slack_k1']:.3f}" in text
    assert k2["contending_sets"][1] == ["grain"]
    cult = r["cultivars"]
    assert (
        cult["Cappelle Desprez"]["hi"]
        < 0.55
        < min(v["hi"] for k, v in cult.items() if k != "Cappelle Desprez")
    )


def test_wheat_check_accepts_the_zip_or_the_csv_hashes(tmp_path):
    d = _load("wheat", "derive.py")
    f = tmp_path / "yield_data.csv"
    f.write_text("a\n1\n", encoding="utf-8")
    m = {
        "file": "x.zip",
        "csv_file": "yield_data.csv",
        "csv_size": f.stat().st_size,
        "csv_md5": fitkit.file_hash(f, "md5"),
        "csv_sha256": fitkit.file_hash(f, "sha256"),
    }
    d.check(f, m)
    with pytest.raises(RuntimeError, match="neither"):
        d.check(tmp_path / "other.csv", m)
    f.write_text("a\n2\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="md5"):
        d.check(f, m)
