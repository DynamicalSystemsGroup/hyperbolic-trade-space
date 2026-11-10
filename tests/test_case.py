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

# Slow module: shared fixtures cost minutes (verification in tiers); not in the fast suite.
pytestmark = pytest.mark.slow

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


def test_subsystem_mapping_is_data_and_covers_every_attribute():
    """Each attribute has one subsystem in the spec; the model's grouping is 3 + 5 + 1."""
    spec = case.CUBESAT
    assert set(spec.subsystems) == set(spec.attributes)
    assert set(spec.subsystem_order) == set(spec.subsystems.values())
    counts = {g: list(spec.subsystems.values()).count(g) for g in spec.subsystem_order}
    assert counts == {"controls": 3, "power and energy": 4, "mass": 1}
    assert spec.subsystems_of(["total mass", "pointing error"]) == ["controls", "mass"]
    assert spec.subsystems_of(["settling time"]) == ["controls"]


def test_load_study_filters_and_conditions(small):
    assert small.M.shape == (N, 8) and (small.M > 0).all()
    assert len(small.raw) == 1000 and len(small.feasible) == N
    assert small.feasible.settled.all() and small.feasible.momentum_ok.all()
    assert small.names[0] == "settling time" and small.names[-1] == "depth of discharge"
    assert "metrics__settling_time_s" in small.conditioner.get_feature_names_out()
    assert "metrics__slew_time_s" not in small.conditioner.get_feature_names_out()


def test_feasible_mask_counts_on_frozen_data(primary, stock):
    """R-19 of the WP23 close-out: ``dod_ok`` is a flag of the case, and the feasible sets stay 706
    and 780 (the eclipse reserve's positivity removed exactly the ``dod_ok`` failures, 131 per
    regime, before the reserve left the metric set)."""
    assert "dod_ok" in case.CUBESAT.flags
    assert len(primary.feasible) == 706 and len(stock.feasible) == 780
    assert int(case.feasible_mask(primary.raw).sum()) == 706
    for study in (primary, stock):
        assert int((~study.raw.dod_ok).sum()) == 131


def test_feasibility_table_cascade(primary):
    t = case.feasibility_table(primary)
    assert list(t.condition) == [
        "settled",
        "power_ok",
        "momentum_ok",
        "dod_ok",
        "all attributes positive",
    ]
    assert t.remaining.iloc[-1] == 706 and t.remaining.is_monotonic_decreasing
    assert t["removed in this order"].sum() == 1000 - 706


def test_conditioning_table(small):
    t = case.conditioning_table(small)
    assert list(t.index) == small.names and len(t) == 8
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


def test_term_and_tension_tables_small(small):
    fits = case.k_fits(small, Ks=(1, 2))
    band = 0.08
    f = case.term_table(small, fits, K=2, band=band)
    assert list(f.term) == [1, 2] and f.share.between(0, 1).all()
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
    assert list(t.view) == ["all attributes", "four metrics"]
    assert (t["of"] == N).all() and t.nondominated.is_monotonic_decreasing
    assert t.nondominated.min() >= 1


def test_view_study_columns(small):
    v = case.view_study(small)
    assert v.M.shape == (N, 4) and v.names == [
        "settling time", "pointing error", "control effort", "total mass",
    ]  # fmt: skip
    assert v.preconditioner.n_features_in_ == 4


def test_regime_comparison_small():
    t = case.regime_comparison(n_max=N)
    assert list(t.columns) == ["quantity", "primary", "stock"]
    assert "contending set" in set(t.quantity) and len(t) == 6 + len(case.CUBESAT.association_pairs)


@pytest.mark.slow
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


def test_tau_sweep_figure_marks_the_fit_temperature_and_orders_the_rows(small, small_fit):
    """The redraw's requirements (WP19-figure-review.md, "Heatmap redraw (fourth PM, after WP23's
    rounds)" and its "redraw 2"): the fit temperature is one outlined, bold-labelled column of the
    grid (the sweep's own column when within 2 %, else inserted), its exponents are printed in
    that column only, rows are ordered by the exponent there with the white rows last in the
    study's order, the colour scale runs from the floor to ``vmax``, the limit column is named,
    and the effective sample size is written at the fit temperature."""
    import matplotlib.pyplot as plt

    fig = case.tau_sweep_figure(small, small_fit, title="a title", vmax=0.5)
    grid = fig.axes[2]
    labels = [t.get_text() for t in grid.get_xticklabels()]
    bold = [i for i, t in enumerate(grid.get_xticklabels()) if t.get_fontweight() == "bold"]
    assert fig.get_suptitle() == "a title" and labels[-1] == "∞ (limit)" and len(bold) == 1
    sel = bold[0]
    assert abs(float(labels[sel]) - small_fit.tau) <= 0.02 * small_fit.tau + 0.5
    W = grid.images[0].get_array()
    assert W.shape == (len(small.names), len(labels))
    w = np.where(W[:, sel] > case.EXPONENT_FLOOR, W[:, sel], 0.0)
    assert np.all(np.diff(w) <= 0)  # largest exponent at the top row
    rows = [t.get_text() for t in grid.get_yticklabels()]
    whites = [rows[r] for r in range(len(w)) if w[r] == 0]
    assert whites == [n for n in small.names if n in whites]  # white rows last, study order
    printed = [t.get_text() for t in grid.texts]
    assert len(printed) == int((w > 0).sum()) and all(p[0] in "0<" for p in printed)
    assert grid.images[0].get_clim() == (case.EXPONENT_FLOOR, 0.5)
    assert any(t.get_text().startswith("n_eff = ") for t in fig.axes[1].texts)
    assert case.regime_word(small) == "primary"
    plt.close(fig)


def test_sensitivity_table_has_the_variants_and_the_baseline_shares_all(primary):
    t = case.sensitivity_table(primary)
    spec = primary.spec
    assert t.variant.tolist() == [
        "baseline", "target fraction halved", "target fraction doubled", "robust scaler",
        *[f"view: {v}" for v in spec.views],
    ]  # fmt: skip
    assert t.loc[0, "shared with baseline"] == t.loc[0, "n_lemma"]
    assert (t.frac_above_ >= 0).all() and (t.tau > 0).all()
    # halving the target fraction raises the temperature, doubling it lowers it
    assert t.tau[1] > t.tau[0] > t.tau[2]
    again = case.sensitivity_table(primary)
    pd.testing.assert_frame_equal(t, again)


def test_category_refits_cover_each_level_and_partition_the_designs(primary):
    t = case.category_refits(primary)
    levels = primary.spec.covariates[primary.spec.category]
    assert t[primary.spec.category].tolist() == list(levels)
    assert t.designs.sum() == len(primary.feasible)
    assert (t.frac_above_ >= 0).all() and (t.n_eff_ > 0).all()


def test_scaler_option_changes_the_conditioning_and_is_standard_by_default(small):
    assert case.conditioner_for(small.attrs).transformers[0][1].scaler == "standard"
    robust = case._rebuilt(small, scaler="robust")
    assert robust.preconditioner.scaler == "robust"
    assert not np.allclose(robust.M, small.M)
    assert robust.M.shape == small.M.shape and len(robust.feasible) == len(small.feasible)


# ---- the frozen data: counts and the K = 1, 2, 3 record -----------------------------------


def test_nondominated_counts_on_frozen_primary(primary):
    t = case.nondominated_counts(primary).set_index("view")
    assert t.nondominated.tolist() == [659, 126]
    assert (t["of"] == 706).all()
    assert t.share.round(3).tolist() == [0.933, 0.178]


# the record of k3-cubesat.md, as printed: tau, objective_, frac_above_, term rows, gamma, radius
RECORD = {
    "primary": {
        1: (38.10, 0.2434, 0.092, [706]),
        2: (94.42, 0.1823, 0.095, [414, 292]),
        3: (113.22, 0.1458, 0.099, [162, 181, 363]),
    },
    "stock": {
        1: (45.68, 0.1786, 0.104, [780]),
        2: (71.92, 0.1417, 0.100, [454, 326]),
        3: (113.22, 0.0927, 0.094, [251, 184, 345]),
    },
}
MARGIN = {
    ("primary", 2): (0.000697, 0.000057), ("primary", 3): (0.001213, 0.000100),
    ("stock", 2): (0.001413, 0.000120), ("stock", 3): (0.000091, 0.000008),
}  # fmt: skip
GAP_K1 = {"primary": 8.7e-6, "stock": 1.29e-5}


@pytest.mark.slow
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
        assert sorted(r["term rows"]) == sorted(rows)
    assert t.loc[1, "max gap"] == pytest.approx(GAP_K1[regime], rel=0.05)
    assert t.loc[1, "status"] == "not_applicable"
    for K in (2, 3):
        r = t.loc[K]
        assert r.status == "certified" and r["max gap"] < 1e-12
        assert r.gamma == pytest.approx(MARGIN[regime, K][0], abs=5e-7)
        assert r.radius == pytest.approx(MARGIN[regime, K][1], abs=5e-7)


def test_k3_terms_equal_the_primary_record(primary, primary_fits):
    f = case.term_table(primary, primary_fits, K=3)
    assert sorted(f["rows"]) == [162, 181, 363]
    assert sorted(f.share.round(3)) == [0.034, 0.241, 0.724]
    assert sorted(f["n_lemma"]) == [4, 5, 5]
    assert sorted(f["near-frontier"]) == [3, 21, 73]
    assert (f["gap G_k"] < 1e-12).all()
    big = f.loc[f.share.idxmax()]
    assert big["contending set"].startswith("peak slew power, pointing error")
    assert big["largest exponents"].startswith("peak slew power 0.612")


def test_thin_term_is_reported_from_the_estimator_and_gets_its_reason(primary, primary_fits):
    """WP23 data gate: the guard of ten is applied per term, the thin term's reading replaced."""
    import matplotlib.pyplot as plt

    fit, band = primary_fits[3], primary_fits[1].band
    reps = case.term_reports(fit.estimator, primary.M, band)
    assert len(reps) == 3 and case.MIN_NEAR_FRONTIER == 10
    thin = [r for r in reps if not case.has_reading(r)]
    assert [r.n_near_frontier for r in thin] == [3]
    assert case.thin_reason(thin[0].n_near_frontier) == (
        "too few near-frontier designs for an association reading: 3 of ten"
    )
    with pytest.raises(ValueError, match="3 of ten"):
        case._reports(primary, fit, band)
    fig = case.tension_figure(primary, fit, band=band)
    texts = [t.get_text().lower() for ax in fig.axes for t in ax.texts]
    assert any("3 of ten" in t.replace("\n", " ") for t in texts)
    plt.close(fig)


def test_k1_contending_set_equals_the_record(primary, primary_fits, stock, stock_fits):
    p = case.tension_table(primary, primary_fits[1]).iloc[0]
    assert p["contending set"] == (
        "total mass, energy balance, pointing error, depth of discharge, settling time"
    )
    assert p.n_lemma == 5 and p["near-frontier"] == 56
    s = case.tension_table(stock, stock_fits[1]).iloc[0]
    assert set(s["contending set"].split(", ")) == {
        "control effort", "settling time", "power margin", "pointing error", "depth of discharge",
    }  # fmt: skip
    assert s["near-frontier"] == 77


def test_regime_comparison_on_frozen_data():
    t = case.regime_comparison().set_index("quantity")
    assert t.loc["feasible n", "primary"] == "706 (191 / 248 / 267)"
    assert t.loc["band 1/tau, near-frontier designs", "primary"] == "0.0262, 56"
    assert t.loc["band 1/tau, near-frontier designs", "stock"] == "0.0219, 77"


# ---- candidates and propose-predict-check -----------------------------------------------------


@pytest.fixture(scope="module")
def regressor(primary):
    return case.fit_regressor(primary)


def test_candidates_are_scored(primary, primary_fits):
    t = case.candidate_table(primary, primary_fits[1])
    assert list(t.candidate) == ["fast_effort_hungry", "precise_heavy_sensor", "light_slow"]
    assert (t["log V"] < 0).all() and (t["rank among training"].between(0, 1)).all()
    assert t["log V"].idxmax() == 1  # the precise heavy-sensor design is the nearest to V = 1


@pytest.mark.slow
def test_refit_reproduces_the_recorded_predictions(primary, regressor):
    t = case.proposals_table(primary, regressor)
    assert len(t) == 3 and (t["max |recorded - refit|"] < 1e-6).all()
    assert regressor.tau == pytest.approx(10.69, abs=0.01)


def test_predict_check_within_the_band(primary, regressor):
    t = case.predict_check(primary, regressor)
    assert list(t.proposal) == ["proposal_1", "proposal_2", "proposal_3"]
    assert t["log V within band"].all() and (t["|diff| / band"] < 1).all()
    assert (t["difference"] > 0).all()  # measured log V above predicted for all three


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
    views = case.with_spec(views={"one": ("settling_time_s",)})
    t = case.nondominated_counts(case.load_study("primary", views, n_max=100))
    assert list(t.view) == ["all attributes", "one"]
    only_stock = case.with_spec(regimes={"stock": "adcs_designs_cubesat.csv"})
    assert list(case.regime_comparison(only_stock, n_max=N).columns) == ["quantity", "stock"]
    assert case.CUBESAT.flags == ("settled", "power_ok", "momentum_ok", "dod_ok")  # frozen
    with pytest.raises(AttributeError):
        case.CUBESAT.flags = ()


def test_a_second_table_runs_without_cubesat_edits(tmp_path):
    rng = np.random.default_rng(7)
    n = 200
    u = rng.dirichlet([2.0, 2.0, 2.0], n)  # points under a planted term w.x = 1
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
        "load_study", "fit_study", "k_sweep", "k_table", "term_table", "tension_table",
        "nondominated_counts", "regime_comparison", "predict_check", "candidate_table",
        "log_plane_figure", "feasible_mask",
    ):  # fmt: skip
        doc = getattr(case, name).__doc__
        assert "Parameters\n    ----------" in doc and "Returns\n    -------" in doc, name


def test_sensitivity_and_refits_on_frozen_primary(primary):
    t = case.sensitivity_table(primary).set_index("variant")
    assert t.loc["baseline", "tau"] == pytest.approx(38.0961, rel=1e-4)  # the K = 1 record
    assert t.loc["baseline", "n_lemma"] == 5
    r = case.category_refits(primary)
    assert r.designs.tolist() == [191, 248, 267]


# ---- the cold reads of WP10, round 2: the mean slack across K, the margin scale, PCA, titles ----


def test_mean_slack_by_k_reads_the_estimator_and_the_fixed_tau_refit_shares_one_temperature(small):
    fits = case.k_fits(small, Ks=(1, 2))
    own = case.mean_slack_by_k(small, fits)
    assert list(own.columns) == ["K", "tau", "mean_slack_"]
    assert np.allclose(own.mean_slack_, [f.estimator.mean_slack_ for f in fits.values()])
    fixed = case.mean_slack_fixed_tau(small, fits)
    assert (fixed.tau == fits[1].tau).all()
    assert fixed.mean_slack_.iloc[0] == pytest.approx(own.mean_slack_.iloc[0])
    assert fixed.mean_slack_.iloc[1] <= fixed.mean_slack_.iloc[0] + 1e-9  # falls with K


def test_margin_scale_has_the_multi_term_fits_only_and_the_median_exceeds_the_margin(small):
    fits = case.k_fits(small, Ks=(1, 2))
    table = case.margin_scale(small, fits)
    assert list(table["K"]) == [2]
    row = table.iloc[0]
    assert row["gamma"] > 0 and row["radius"] > 0 and row["radius"] < row["gamma"]
    assert row["median margin"] >= row["gamma"]
    assert row["band 1/tau"] == pytest.approx(1.0 / fits[2].tau)


def test_pca_directions_are_the_tension_reports_own_principal_directions(small, small_fit):
    table = case.pca_directions(small, small_fit)
    rep = case._reports(small, small_fit)[0]
    assert list(table["direction"]) == [1, 2, 3]
    assert np.allclose(table["share of spread"], rep.explained_spread[:3])
    assert table["share of spread"].is_monotonic_decreasing
    for text in table["leading loadings"]:
        assert len(text.split(", ")) == 3 and "+" in text.split(", ")[0]


def test_panel_titles_count_the_exact_maximum_support_and_outline_exactly_those(small, small_fit):
    import matplotlib.pyplot as plt

    rep = case._reports(small, small_fit)[0]
    fig = case.tension_figure(small, small_fit)
    ax = fig.axes[0]
    n = rep.n_lemma
    plural = "s" if n != 1 else ""
    assert ax.get_title() == (
        f"term 1: {rep.lemma_name} ({n} metric{plural} in the exact-maximum support)"
    )
    from matplotlib.patches import Rectangle

    assert sum(isinstance(p, Rectangle) for p in ax.patches) == n  # the outlined members
    plt.close(fig)
