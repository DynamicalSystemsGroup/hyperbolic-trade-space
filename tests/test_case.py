"""WP10 D-4: the case module (``examples/adcs/case.py``) that the paper calls.

Fast tests run each function on a small sample; the record tests run the frozen data and compare
with ``docs/superpowers/notes/k3-cubesat.md`` and the paper's nondominated counts.
"""

import doctest
import subprocess
import sys
import time
from pathlib import Path

import case
import numpy as np
import pandas as pd
import pytest

N = 150  # small sample: the first N feasible designs


@pytest.fixture(scope="module")
def small():
    return case.load_study("primary", n_max=N)


@pytest.fixture(scope="module")
def small_fit(small):
    return case.fit_study(small)


@pytest.fixture(scope="module")
def primary():
    return case.load_study("primary")


@pytest.fixture(scope="module")
def primary_fits(primary):
    return case.k_fits(primary)


@pytest.fixture(scope="module")
def stock():
    return case.load_study("stock")


@pytest.fixture(scope="module")
def stock_fits(stock):
    return case.k_fits(stock)


# ---- small-sample behaviour of every function ----------------------------------------------


def test_load_study_filters_and_conditions(small):
    assert small.M.shape == (N, 10) and (small.M > 0).all()
    assert len(small.raw) == 1000 and len(small.feasible) == N
    assert small.feasible.settled.all() and small.feasible.momentum_ok.all()
    assert small.names[0] == "settling time" and small.names[-1] == "depth of discharge"
    assert "metrics__slew_time_s" in small.conditioner.get_feature_names_out()


def test_feasible_mask_counts_on_frozen_data(primary, stock):
    assert len(primary.feasible) == 706 and len(stock.feasible) == 780
    assert int(case.feasible_mask(primary.raw).sum()) == 706


def test_feasibility_table_cascade(primary):
    t = case.feasibility_table(primary)
    assert list(t.condition) == ["settled", "power_ok", "momentum_ok", "all attributes positive"]
    assert t.remaining.iloc[-1] == 706 and t.remaining.is_monotonic_decreasing
    assert t["removed in this order"].sum() == 1000 - 706


def test_conditioning_table(small):
    t = case.conditioning_table(small)
    assert list(t.index) == small.names and len(t) == 10
    assert set(t.orientation) == {"reciprocal", "direct"}
    assert np.allclose(t["m min"], small.M.min(axis=0))


def test_fit_study_holds_the_target_fraction(small_fit):
    assert small_fit.K == 1 and small_fit.band == pytest.approx(1 / small_fit.tau)
    assert abs(small_fit.estimator.frac_above_ - 0.10) <= 0.02
    assert 3 <= small_fit.tau <= 1e3


def test_fit_is_deterministic(small, small_fit):
    again = case.fit_study(small)
    assert again.tau == small_fit.tau
    assert np.array_equal(again.estimator.exponents_, small_fit.estimator.exponents_)


def test_exponent_table_and_fit_line(small, small_fit):
    t = case.exponent_table(small, small_fit)
    assert list(t.metric) == small.names
    assert t["exponent w"].sum() == pytest.approx(1.0)
    line = case.fit_line(small, small_fit)
    assert line["sum of exponents"].iloc[0] == pytest.approx(1.0) and line.n.iloc[0] == N


def test_tau_sweep_monotone(small):
    t = case.tau_sweep(small, taus=[5.0, 20.0, 100.0, np.inf])
    assert list(t.tau) == [5.0, 20.0, 100.0, np.inf]
    assert t.frac_above.between(0, 1).all() and t.n_eff.gt(0).all()
    assert (t["largest w"] > 0).all() and t["largest at"].isin(small.names).all()


def test_k_sweep_small_sample_has_certificate_columns(small):
    t = case.k_sweep(small, Ks=(1, 2))
    assert list(t.K) == [1, 2]
    assert {"max gap", "status", "gamma", "radius", "bound"} <= set(t.columns)
    assert t.status.iloc[0] == "not_applicable" and np.isnan(t.gamma.iloc[0])
    assert t.status.iloc[1] in {"certified", "stationary_without_margin"}
    assert t.objective_.is_monotonic_decreasing


def test_certificate_table_matches_termination(small):
    fits = case.k_fits(small, Ks=(1, 2))
    c = case.certificate_table(fits)
    assert list(c.columns) == ["K", "max gap", "status", "gamma", "radius", "bound"]
    assert c["max gap"].iloc[1] == fits[2].estimator.termination_.max_gap
    assert c.status.iloc[1] == fits[2].estimator.termination_.status


def test_facet_and_tension_tables_small(small):
    fits = case.k_fits(small, Ks=(1, 2))
    band = 0.08
    f = case.facet_table(small, fits, K=2, band=band)
    assert list(f.facet) == [1, 2] and f.share.between(0, 1).all()
    assert f["rows"].sum() == N and (f["n_lemma"] >= 1).all()
    assert np.allclose(f["gap G_k"], fits[2].estimator.termination_.gaps)
    t = case.tension_table(small, fits[1], band=band)
    assert len(t) == 1 and t["near-frontier"].iloc[0] >= 10
    assert set(t["contending set"].iloc[0].split(", ")) <= set(small.names)


def test_association_table(small, small_fit):
    t = case.association_table(small, small_fit)
    assert list(t.columns) == ["metric a", "metric b", "pearson", "spearman"]
    assert len(t) == len(case.CUBESAT.association_pairs)
    assert t[["pearson", "spearman"]].abs().max().max() <= 1.0


def test_nondominated_mask():
    X = np.array([[1, 3], [2, 2], [3, 1], [1, 1], [2, 2]])
    assert case.nondominated_mask(X).tolist() == [True, True, True, False, True]


def test_nondominated_counts_small(small):
    t = case.nondominated_counts(small)
    assert list(t.view) == ["all attributes", "four metrics", "settling time and slew time"]
    assert (t["of"] == N).all() and t.nondominated.is_monotonic_decreasing
    assert t.nondominated.min() >= 1


def test_view_study_columns(small):
    v = case.view_study(small)
    assert v.M.shape == (N, 4) and v.names == [
        "slew time", "pointing error", "control effort", "total mass",
    ]  # fmt: skip
    assert v.preconditioner.n_features_in_ == 4


def test_regime_comparison_small():
    t = case.regime_comparison(n_max=N)
    assert list(t.columns) == ["quantity", "primary", "stock"]
    assert "contending set" in set(t.quantity) and len(t) == 6 + len(case.CUBESAT.association_pairs)


def test_figures_return_figures_and_do_not_save(small, small_fit, tmp_path, monkeypatch):
    import matplotlib.pyplot as plt

    monkeypatch.chdir(tmp_path)
    fits = case.k_fits(small, Ks=(1, 2))
    figs = [
        case.tau_sweep_figure(small, small_fit),
        case.log_plane_figure(small, small_fit, band=0.1),
        case.log_plane_figure(small, fits[2], band=0.08),
        case.coordinates_figure(small, small_fit),
        case.coordinates_figure(small, fits[2], band=0.08),
        case.tension_figure(small, fits[2], band=0.08),
        case.regime_figure(n_max=N),
    ]
    assert all(isinstance(f, plt.Figure) for f in figs)
    for f in figs:
        plt.close(f)
    assert list(tmp_path.iterdir()) == []


# ---- the frozen data: counts and the K = 1, 2, 3 record -----------------------------------


def test_nondominated_counts_on_frozen_primary(primary):
    t = case.nondominated_counts(primary).set_index("view")
    assert t.nondominated.tolist() == [671, 146, 8]
    assert (t["of"] == 706).all()
    assert t.share.round(3).tolist() == [0.950, 0.207, 0.011]


# the record of k3-cubesat.md, as printed: tau, objective_, frac_above_, facet rows, gamma, radius
RECORD = {
    "primary": {
        1: (38.10, 0.2036, 0.096, [706]),
        2: (113.22, 0.1384, 0.096, [332, 374]),
        3: (195.18, 0.1173, 0.098, [201, 188, 317]),
    },
    "stock": {
        1: (41.72, 0.1312, 0.104, [780]),
        2: (78.75, 0.1059, 0.092, [390, 390]),
        3: (162.78, 0.0929, 0.094, [284, 149, 347]),
    },
}
MARGIN = {
    ("primary", 2): (0.000830, 0.000068), ("primary", 3): (0.000220, 0.000018),
    ("stock", 2): (0.001575, 0.000126), ("stock", 3): (0.001487, 0.000119),
}  # fmt: skip
GAP_K1 = {"primary": 4.7e-6, "stock": 1.8e-5}


@pytest.mark.parametrize("regime", ["primary", "stock"])
def test_k_sweep_equals_the_record(regime, request):
    study = request.getfixturevalue(regime)
    fits = request.getfixturevalue(f"{regime}_fits")
    t = case.k_table(study, fits).set_index("K")
    for K, (tau, obj, frac, rows) in RECORD[regime].items():
        r = t.loc[K]
        assert r.tau == pytest.approx(tau, abs=0.006)
        assert r.objective_ == pytest.approx(obj, abs=6e-5)
        assert r.frac_above_ == pytest.approx(frac, abs=6e-4)
        assert sorted(r["facet rows"]) == sorted(rows)
    assert t.loc[1, "max gap"] == pytest.approx(GAP_K1[regime], rel=0.05)
    assert t.loc[1, "status"] == "not_applicable"
    for K in (2, 3):
        r = t.loc[K]
        assert r.status == "certified" and r["max gap"] < 1e-12
        assert r.gamma == pytest.approx(MARGIN[regime, K][0], abs=5e-7)
        assert r.radius == pytest.approx(MARGIN[regime, K][1], abs=5e-7)


def test_k3_facets_equal_the_primary_record(primary, primary_fits):
    f = case.facet_table(primary, primary_fits, K=3)
    assert sorted(f["rows"]) == [188, 201, 317]
    assert sorted(f.share.round(3)) == [0.089, 0.133, 0.778]
    assert sorted(f["n_lemma"]) == [6, 6, 7]
    assert sorted(f["near-frontier"]) == [17, 33, 126]
    assert (f["gap G_k"] < 1e-12).all()
    big = f.loc[f.share.idxmax()]
    assert big["contending set"].startswith("peak slew power, total mass, pointing error")
    assert big["largest exponents"].startswith("peak slew power 0.380")


def test_k1_contending_set_equals_the_record(primary, primary_fits, stock, stock_fits):
    p = case.tension_table(primary, primary_fits[1]).iloc[0]
    assert p["contending set"] == (
        "total mass, slew time, energy balance, control effort, pointing error, depth of discharge"
    )
    assert p.n_lemma == 6 and p["near-frontier"] == 51
    s = case.tension_table(stock, stock_fits[1]).iloc[0]
    assert set(s["contending set"].split(", ")) == {
        "control effort", "slew time", "power margin", "settling time", "pointing error",
        "eclipse reserve",
    }  # fmt: skip
    assert s["near-frontier"] == 103


def test_regime_comparison_on_frozen_data():
    t = case.regime_comparison().set_index("quantity")
    assert t.loc["feasible n", "primary"] == "706 (191 / 248 / 267)"
    assert t.loc["band 1/tau, near-frontier designs", "primary"] == "0.0262, 51"
    assert t.loc["band 1/tau, near-frontier designs", "stock"] == "0.0240, 103"


# ---- candidates and propose-predict-check -----------------------------------------------------


@pytest.fixture(scope="module")
def regressor(primary):
    return case.fit_regressor(primary)


def test_candidates_are_scored(primary, primary_fits):
    t = case.candidate_table(primary, primary_fits[1])
    assert list(t.candidate) == ["fast_effort_hungry", "precise_heavy_sensor", "light_slow"]
    assert (t["log V"] < 0).all() and (t["rank among training"].between(0, 1)).all()
    assert t["log V"].idxmax() == 1  # the precise heavy-sensor design is the nearest to V = 1


def test_refit_reproduces_the_recorded_predictions(primary, regressor):
    t = case.proposals_table(primary, regressor)
    assert len(t) == 3 and (t["max |recorded - refit|"] < 1e-6).all()
    assert regressor.tau == pytest.approx(15.37, abs=0.01)


def test_predict_check_within_the_band(primary, regressor):
    t = case.predict_check(primary, regressor)
    assert list(t.proposal) == ["proposal_1", "proposal_2", "proposal_3"]
    assert t["log V within band"].all() and (t["|diff| / band"] < 1).all()
    assert (t["difference"] < 0).all()  # measured log V below predicted for all three


def test_white_space_targets(primary):
    t = case.white_space_targets(case.view_study(primary))
    assert len(t) == 3 and t["hole score"].min() > 2.0
    assert "total mass (kg)" in t.columns


def test_predict_check_figure(primary, regressor):
    import matplotlib.pyplot as plt

    fig = case.predict_check_figure(primary, regressor)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


# ---- the data-as-config rule ---------------------------------------------------------------


def test_swapping_the_spec_changes_the_behaviour():
    default = case.load_study("primary", n_max=None)
    lax = case.load_study("primary", case.with_spec(flags=("settled",)))
    assert len(lax.feasible) > len(default.feasible)
    views = case.with_spec(views={"one": ("slew_time_s",)})
    t = case.nondominated_counts(case.load_study("primary", views, n_max=100))
    assert list(t.view) == ["all attributes", "one"]
    only_stock = case.with_spec(regimes={"stock": "adcs_designs_cubesat.csv"})
    assert list(case.regime_comparison(only_stock, n_max=N).columns) == ["quantity", "stock"]
    assert case.CUBESAT.flags == ("settled", "power_ok", "momentum_ok")  # the original is frozen
    with pytest.raises(AttributeError):
        case.CUBESAT.flags = ()


def test_a_second_table_runs_without_cubesat_edits(tmp_path):
    rng = np.random.default_rng(7)
    n = 200
    u = rng.dirichlet([2.0, 2.0, 2.0], n)  # points under a planted facet w.x = 1
    slack = np.exp(-rng.exponential(0.3, n))
    A = pd.DataFrame(u * slack[:, None] * 5 + 0.05, columns=["fuel", "range", "cost"])
    A["ok"] = True
    A["x1"] = rng.uniform(0.0, 1.0, n)
    A.to_csv(tmp_path / "planted.csv", index=False)
    spec = case.CaseSpec(
        name="planted",
        data_dir=tmp_path,
        regimes={"only": "planted.csv"},
        attributes=("fuel", "range", "cost"),
        short={"fuel": "fuel", "range": "range", "cost": "cost"},
        units={"fuel": "kg", "range": "km", "cost": "usd"},
        orientation={"fuel": +1, "range": +1, "cost": +1},
        design_vars=("x1",),
        flags=("ok",),
        views={"pair": ("fuel", "range")},
    )
    st = case.load_study("only", spec)
    assert st.M.shape == (n, 3) and st.preconditioner.n_features_in_ == 3
    fit = case.fit_study(st)
    assert case.exponent_table(st, fit)["exponent w"].sum() == pytest.approx(1.0)
    assert case.feasibility_table(st).remaining.iloc[-1] == n
    assert case.nondominated_counts(st).nondominated.iloc[0] >= 1
    t = case.k_sweep(st, Ks=(1, 2))
    assert list(t.K) == [1, 2]
    import matplotlib.pyplot as plt

    plt.close(case.tau_sweep_figure(st, fit))


# ---- no import-time work ---------------------------------------------------------------------


def test_import_is_fast_and_pure(tmp_path):
    here = Path(case.__file__).parent
    code = (
        "import sys, time, os; t = time.perf_counter(); import case; dt = time.perf_counter() - t;"
        "print(dt, 'sklearn' in sys.modules, 'k_terms' in sys.modules, len(os.listdir('.')))"
    )
    out = subprocess.run(
        [sys.executable, "-c", code], cwd=tmp_path, capture_output=True, text=True, check=True,
        env={"PYTHONPATH": str(here), "PATH": "", "SYSTEMROOT": ""},
    )  # fmt: skip
    dt, sk, kt, nfiles = out.stdout.split()
    assert float(dt) < 2.0
    assert (sk, kt) == ("False", "False") and nfiles == "0"


def test_the_module_import_in_process_is_cheap():
    t = time.perf_counter()
    import importlib

    importlib.reload(case)
    assert time.perf_counter() - t < 2.0


def test_docstrings_run_and_are_numpydoc():
    assert doctest.testmod(case, optionflags=doctest.ELLIPSIS).failed == 0
    for name in (
        "load_study", "fit_study", "k_sweep", "k_table", "facet_table", "tension_table",
        "nondominated_counts", "regime_comparison", "predict_check", "candidate_table",
        "log_plane_figure", "feasible_mask",
    ):  # fmt: skip
        doc = getattr(case, name).__doc__
        assert "Parameters\n    ----------" in doc and "Returns\n    -------" in doc, name
