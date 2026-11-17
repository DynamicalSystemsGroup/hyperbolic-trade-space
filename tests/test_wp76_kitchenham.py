"""WP76 Kitchenham-CSC example: the case model is the statement of record; provenance; records.

The data-dependent run (``examples/kitchenham/run.py --fetch``) downloads the file of record and is
not in the suite; the committed derived table is what the page's blocks and these tests read. The
constants of ``run.py`` and ``variants.py`` are held equal to the elements of
``examples/kitchenham/kitchenham.sysml`` (scope R-8), the manifest names its source, DOI and
licence (R-7), the exclusion rule drops what it says (R-7), and the page and the verification
record quote ``results.json`` and ``variants.json`` (R-1, R-3, R-4).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "examples"
CASE = EX / "kitchenham"
sys.path.insert(0, str(EX))
import fitkit  # noqa: E402

P = "KitchenhamIronTriangle"


def _load(script):
    path = CASE / script
    spec = importlib.util.spec_from_file_location(f"wp76_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def run():
    return _load("run.py")


@pytest.fixture(scope="module")
def variants():
    sys.path.insert(0, str(CASE))
    return _load("variants.py")


@pytest.fixture(scope="module")
def model():
    """The case model, loaded strictly; a named-cause failure when the client cannot start."""
    import opensysml

    try:
        conn = opensysml.connect()
        return conn.load_from_content(
            (CASE / "kitchenham.sysml").read_text(encoding="utf-8"), strict=True
        )
    except Exception as exc:  # the cause is the message; never a skip
        pytest.fail(f"the opensysml client could not load the case model: {exc}", pytrace=False)


def _ev(model, expr):
    return model.eval(f"{P}::{expr}")


# ---------------------------------------------------------------- R-7: provenance
def test_manifest_names_source_doi_licence_and_exclusions():
    m = fitkit.load_manifest(CASE / "manifest.toml")
    assert m["doi"].startswith("10.5281/zenodo.")
    assert m["licence"].startswith("CC BY") and m["licence_url"].startswith("https://")
    assert m["attribution"] and m["url"] and m["landing_page"]
    assert m["size"] == 7877 and len(m["sha256"]) == 64 and len(m["md5"]) == 32
    assert m["rows"] - m["excluded_rows"] == m["kept_rows"] == 141
    assert m["paper_doi"] == "10.1016/S0164-1212(02)00021-3"


def test_cached_file_of_record_matches_manifest():
    m = fitkit.load_manifest(CASE / "manifest.toml")
    f = CASE / "data" / m["file"]
    if not f.exists():
        pytest.skip("file of record not fetched")
    fitkit.verify(f, m)


def test_derived_table_is_the_record(run):
    x = run.load_derived()
    assert len(x) == 141 and (x["planned_duration"] > 0).all()
    assert list(x.columns[-3:]) == run.COLS
    res = json.loads((CASE / "results.json").read_text(encoding="utf-8"))
    d = res["describe"]
    assert d["rows_in_table"] == 145 and d["rows_kept"] == 141 and d["rows_excluded"] == 4
    assert d["no_estimated_completion"] == 3
    assert res["provenance"]["package_version"]
    assert len(res["provenance"]["git_sha"]) == 40
    lic = (CASE / "derived" / "LICENCE-DATA.txt").read_text(encoding="utf-8")
    assert "CC BY 4.0" in lic and "10.5281/zenodo.268457" in lic


def test_derive_keeps_rows_with_a_positive_planned_duration(run):
    df = pd.DataFrame(
        {
            "project": [1, 2, 3, 4],
            "client": [1, 1, 2, 2],
            "type": ["D", "P", "D", "D"],
            "start": pd.to_datetime(["2000-01-01"] * 4),
            "duration": [100.0, 50.0, 80.0, 60.0],
            "effort": [1000.0, 500.0, 800.0, 600.0],
            "afp": [100.0, 50.0, 80.0, 60.0],
            "est_completion": pd.to_datetime(["2000-04-10", None, "1999-12-01", "2000-03-01"]),
            "first_estimate": [900.0, 500.0, 800.0, 700.0],
            "estimate_method": ["EO"] * 4,
        }
    )
    x = run.derive(df)
    assert list(x["project"]) == [1, 4]  # no completion date, and one that precedes its start
    assert x["sched"].iloc[0] == pytest.approx(1 - 100 / 100)
    assert x["budget"].iloc[0] == pytest.approx(1 - 1000 / 900)
    M = run.condition(x)
    assert M.shape == (2, 3) and (M > 0).all()
    with pytest.raises(ValueError, match="Negative"):
        run.condition(x, shift=0.0)


def test_conditioning_keeps_every_project_positive(run):
    x = run.load_derived()
    for kw in (
        {},
        {"scaler": "robust"},
        {"scaler": None},
        {"shift": 20.0},
        {"shift": 40.0},
        {"shift": 3.0, "cap": 3.0},
        {"ratio": True},
    ):
        M = run.condition(x, **kw)
        assert M.shape == (141, 3) and np.isfinite(M).all() and (M > 0).all(), kw


# ---------------------------------------------------------------- R-8: the model of record
def test_model_loads_strictly_with_one_package_and_its_sections(model):
    text = (CASE / "kitchenham.sysml").read_text(encoding="utf-8")
    assert sum(line.startswith("package ") for line in text.splitlines()) == 1
    for n in range(1, 10):
        assert f"// {n}. " in text, n
    assert text.count("doc /*") >= 30


def test_primary_rule_constants_equal_the_model(run, model):
    assert _ev(model, "primary.shift") == run.SHIFT
    assert str(_ev(model, "primary.scaler")).endswith(run.SCALER)
    assert _ev(model, "primary.capOverrunAt") == 0.0
    assert _ev(model, "primary.planOverActual") is False
    for name in ("schedule", "budget", "scope"):
        assert str(_ev(model, f"{name}Orientation")).endswith("largerIsBetter")
    assert run.ORIENTATION == [1, 1, 1]
    assert _ev(model, "plannedDurationBound") == 0.0


def test_fit_and_band_constants_equal_the_model(run, variants, model):
    assert _ev(model, "fitRule.targetFractionAbove") == run.TARGET_FRAC_ABOVE
    assert (
        _ev(model, "fitRule.temperatureLowerBound"),
        _ev(model, "fitRule.temperatureUpperBound"),
    ) == run.TAU_BOUNDS
    assert _ev(model, "fitRule.seed") == run.SEED
    assert _ev(model, "fitRule.twoTermRestarts") == run.K2_RESTARTS
    assert _ev(model, "bandRule.minNearFrontier") == run.MIN_NEAR
    assert _ev(model, "bandRule.reportGuard") == run.MIN_NEAR_REPORT
    assert tuple(_ev(model, "bandRule.ladderCounts")) == variants.BAND_COUNTS
    assert _ev(model, "influenceRule.exponentMoveThreshold") == variants.MOVE


def test_alternatives_equal_the_models_parts(run, variants, model):
    """Each ladder rung's conditioning call is the model's part of the same name."""
    x = run.load_derived()
    model_parts = {
        "robust_scaler": "robustScaler",
        "no_scaler": "noScaler",
        "shift_20": "shift20",
        "shift_40": "shift40",
        "cap_3_shift_3": "cap3Shift3",
        "plan_over_actual": "planOverActualRule",
    }
    ladder = {label: M for label, _, M in variants.conditioning_ladder(x)}
    for label, part in model_parts.items():
        shift = _ev(model, f"{part}.shift")
        cap = _ev(model, f"{part}.capOverrunAt") or None
        ratio = _ev(model, f"{part}.planOverActual")
        scaler = str(_ev(model, f"{part}.scaler")).split("::")[-1]
        scaler = None if scaler == "none" else scaler
        M = run.condition(x, shift=shift, scaler=scaler, cap=cap, ratio=ratio)
        np.testing.assert_allclose(M, ladder[label], err_msg=label)


def test_model_calcs_agree_with_the_python(run, model):
    x = run.load_derived().iloc[:5]
    for _, r in x.iterrows():
        share = _ev(model, f"SlackShare(actual = {r.duration}, plan = {r.planned_duration})")
        assert float(share[0] if hasattr(share, "__len__") else share) == pytest.approx(r.sched)
    lv = np.array([0.01, -0.02, 0.5, -0.9, 0.03, 0.0])
    band = _ev(model, "NearFrontierBand(tau = 100.0, bandHoldingMinRows = 0.0)")
    assert float(band[0] if hasattr(band, "__len__") else band) == pytest.approx(0.01)
    assert run.band_for(lv, 100.0, k=2) == pytest.approx(max(0.01, 0.01 * 1.0001))
    pat = _ev(
        model, "HeadlinePattern(scheduleScope = -0.7, budgetScope = -0.9, scheduleBudget = 0.4)"
    )
    assert pat is True
    pat = _ev(
        model, "HeadlinePattern(scheduleScope = -0.7, budgetScope = -0.9, scheduleBudget = -0.4)"
    )
    assert pat is False


def test_project_types_in_the_model_are_the_tables(run, model):
    x = run.load_derived()
    literals = [c.name for c in model.find(f"{P}::ProjectType").children()]
    assert set(x["type"].dropna()) <= set(literals)
    assert literals == sorted(literals, key=str.lower)
    assert int(x["type"].isna().sum()) == 10  # ten projects carry no type code


# ------------------------------------------- R-1, R-3, R-4: the page quotes the results
MINUS = "\u2212"  # the page writes negative numbers with a minus sign
SB, SS, BS = "schedule slack|budget slack", "schedule slack|scope", "budget slack|scope"


def _neg(s):
    return s.replace("-", MINUS)


def _results():
    return json.loads((CASE / "results.json").read_text(encoding="utf-8"))


def _variants():
    return json.loads((CASE / "variants.json").read_text(encoding="utf-8"))


def _page():
    return (ROOT / "docs/examples/kitchenham.md").read_text(encoding="utf-8")


def _pattern(a):
    return a[SS] < 0 and a[BS] < 0 and a[SB] > 0


def test_page_quotes_the_primary_fit():
    r, page = _results(), _page()
    d, p = r["describe"], r["runs"]["primary"]
    assert f"{d['rows_in_table']} software projects" in page and "141 of the 145" in page
    assert f"{d['worst_schedule_overrun_ratio']:.1f} times the planned duration" in page
    assert round(d["share_exactly_on_schedule"], 2) == 0.24 and "A quarter of the projects" in page
    assert f"frontier is {p['tau_selected']:.1f}" in page
    w = p["exponents_k1"]
    assert (
        f"{w['schedule slack']:.2f} for schedule slack, {w['budget slack']:.2f} for budget slack "
        f"and {w['scope']:.2f} for scope" in page
    )
    assert set(p["contending_set"]) == set(p["metrics"]) and p["n_lemma"] == 3
    assert p["band_widened"] and p["n_near_frontier"] == 15
    assert f"holds fifteen projects, {p['band']:.3f} in log V" in page
    a = p["association"]
    assert (
        _neg(
            f"is {a[SB]:+.2f}, of schedule slack with scope {a[SS]:.2f} and of budget slack with "
            f"scope {a[BS]:.2f}"
        )
        in page
    )
    assert _pattern(a)
    k2 = p["k2"]
    assert k2["term_share"] == [1.0, 0.0] and k2["status"] == "certified"
    assert f"falls from {p['mean_slack_k1']:.3f} to {k2['mean_slack']:.3f}" in page


def test_page_states_the_headline_only_where_the_checks_hold():
    """R-3: the sign pattern holds on exactly the rows the page says, and nowhere wider."""
    v, page = _variants(), _page()
    cond = v["conditioning"]
    scaled = [k for k in cond if k != "no_scaler"]
    assert len(scaled) == 6
    assert all(cond[k]["holds_pattern"] for k in scaled)
    assert not cond["no_scaler"]["holds_pattern"]
    assert cond["no_scaler"]["exponents_k1"]["scope"] == pytest.approx(0.0, abs=1e-6)
    assert "With no scaler scope's exponent is 0.00" in page
    neg = [cond[k]["association"][pr] for k in scaled for pr in (SS, BS)]
    pos = [cond[k]["association"][SB] for k in scaled]
    assert _neg(f"{max(neg):.2f} to {min(neg):.2f}") in page
    assert f"{min(pos):+.2f} to {max(pos):+.2f}" in page
    sched = [cond[k]["exponents_k1"]["schedule slack"] for k in scaled]
    scope = [cond[k]["exponents_k1"]["scope"] for k in scaled]
    assert f"from {min(sched):.2f} to {max(sched):.2f}, scope's from {min(scope):.2f}" in page
    assert f"to {max(scope):.2f}." in page
    bands = v["bands"]
    assert all(b["holds_pattern"] for b in bands)
    assert [b["n_near_frontier"] for b in bands] == [12, 10, 15, 20, 25]
    sb = [b["association"][SB] for b in bands]
    sc = [b["association"][pr] for b in bands for pr in (SS, BS)]
    assert f"from {max(sb):+.2f} to {min(sb):+.2f}" in page
    assert _neg(f"from {max(sc):.2f} to {min(sc):.2f}") in page
    loo = v["influence"]["leave_one_out"]
    assert loo["rows"] == 141
    assert f"{loo['rows_holding_pattern']} of {loo['rows']} refits" in page
    assert loo["rows_with_a_sign_flip"] == [16]
    flip = next(r for r in loo["per_row"] if r["project"] == 16)
    assert (
        _neg(f"without project 16 the slacks' association is {flip['association'][SB]:.2f}") in page
    )
    ex = v["influence"]["extremes"]
    big = ex["without_largest_project"]
    assert (
        f"({big['afp_removed']:,.0f} function points) it is {big['association'][SB]:+.2f}" in page
    )
    worst = ex["without_worst_schedule_overrun"]
    assert f"exponent falls to {worst['exponents_k1']['schedule slack']:.2f}" in page
    assert all(e["holds_pattern"] for e in ex.values())


def test_page_reports_the_subsets_openly():
    v, page = _variants(), _page()
    s = v["subsets"]
    d, p, c = s["type_D"], s["type_P"], s["client_2"]
    assert d["holds_pattern"] and not p["holds_pattern"] and not c["holds_pattern"]
    a = d["association"]
    assert (
        _neg(
            f"In the {d['rows']} development projects the pattern holds "
            f"({a[SB]:+.2f}, {a[SS]:.2f}, {a[BS]:.2f})"
        )
        in page
    )
    assert (
        f"In the {p['rows']} perfective-maintenance projects and the largest client's {c['rows']}"
        in page
    )
    assert _neg(f"({p['association'][SB]:.2f} and {c['association'][SB]:.2f})") in page
    assert p["association"][SS] < 0 and c["association"][SS] < 0


def test_page_makes_no_quality_or_causal_claim():
    """R-6: observational, portfolio-specific; nothing on quality measures as further sides."""
    page = _page().lower()
    for phrase in ("3 + m", "quality measures as", "causes", "because of", "in general"):
        assert phrase not in page, phrase
    assert "says nothing about quality" in page
