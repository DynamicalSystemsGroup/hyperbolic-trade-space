"""WP10 D-4: the case module (``examples/adcs/case.py``) that the paper calls.

Fast tests run each function on a small sample; the record tests run the data of record and compare
with the K record that ``examples/adcs/k_terms.py`` prints (pinned below; the older K-record note,
ten metrics, left at the WP23 close-out and is in history at bf2a83c) and the paper's
nondominated counts.
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

N = 300  # small sample: the first N feasible designs (thirteen metrics need over 150 for K = 2)
ADCS = Path(__file__).resolve().parents[1] / "examples" / "adcs"


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
    """Each attribute has one subsystem in the spec; the model's grouping is 4 + 6 + 1 + 2 (the
    momentum headroom joined the controls at WP30, D-1 (a) of spike C; the available power and the
    battery peak power ratio joined the power and energy group, "No floating requirements"; the
    unit cost and the fleet cost form the cost group, WP30 OD1 (a))."""
    spec = case.CUBESAT
    assert set(spec.subsystems) == set(spec.attributes)
    assert set(spec.subsystem_order) == set(spec.subsystems.values())
    counts = {g: list(spec.subsystems.values()).count(g) for g in spec.subsystem_order}
    assert counts == {"controls": 4, "power and energy": 6, "mass": 1, "cost": 2}
    assert spec.subsystems_of(["total mass", "pointing error"]) == ["controls", "mass"]
    assert spec.subsystems_of(["settling time"]) == ["controls"]


def test_load_study_filters_and_conditions(small):
    assert small.M.shape == (N, 13) and (small.M > 0).all()
    assert len(small.raw) == 3000 and len(small.feasible) == N
    assert small.feasible.settled.all() and small.feasible.momentum_ok.all()
    assert small.names[0] == "settling time" and small.names[-1] == "fleet cost"
    assert "metrics__settling_time_s" in small.conditioner.get_feature_names_out()
    assert "metrics__slew_time_s" not in small.conditioner.get_feature_names_out()


DOD_FAILS_PRIMARY, DOD_FAILS_STOCK = 389, 388


def test_feasible_mask_counts_on_frozen_data(primary, stock):
    """R-19 of the WP23 close-out: ``dod_ok`` is a flag of the case. The feasible sets are 706 and
    780 on the first 1,000 designs of each regime (unchanged at the WP30 gate) and 2,134 and 2,355
    on the 3,000 designs of the gate's sample."""
    assert "dod_ok" in case.CUBESAT.flags
    assert len(primary.feasible) == 2134 and len(stock.feasible) == 2355
    assert int(case.feasible_mask(primary.raw).sum()) == 2134
    assert int(case.feasible_mask(primary.raw.iloc[:1000]).sum()) == 706
    assert int(case.feasible_mask(stock.raw.iloc[:1000]).sum()) == 780
    assert [int((~st.raw.dod_ok).sum()) for st in (primary, stock)] == [
        DOD_FAILS_PRIMARY,
        DOD_FAILS_STOCK,
    ]


def test_feasibility_table_cascade(primary):
    t = case.feasibility_table(primary)
    assert list(t.condition) == [
        "settled",
        "power_ok",
        "momentum_ok",
        "dod_ok",
        "all attributes positive",
    ]
    assert t.remaining.iloc[-1] == 2134 and t.remaining.is_monotonic_decreasing
    assert t["removed in this order"].sum() == 3000 - 2134


def test_conditioning_table(small):
    t = case.conditioning_table(small)
    assert list(t.index) == small.names and len(t) == 13
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


def test_tau_sweep_lines_figure_draws_one_line_per_participating_metric(small, small_fit):
    """Final round, request 56: the lower panel is a line per metric with an exponent above the
    floor somewhere in the sweep (the last position the limit), named at its right end, a ring at
    the fit temperature, and the exponents of the drawn lines sum to at most one at every
    temperature. No colour scale: the readers could not read the sweep's change in one."""
    import matplotlib.pyplot as plt

    fig = case.tau_sweep_lines_figure(small, small_fit, title="a title")
    ax = fig.axes[2]
    assert fig.get_suptitle() == "a title" and len(fig.axes) == 3
    lines = [ln for ln in ax.get_lines() if len(ln.get_xdata()) > 2]
    drawn = [t.get_text() for t in ax.texts]
    assert len(lines) == len(drawn) and set(drawn) <= set(small.names)
    ys = np.array([ln.get_ydata() for ln in lines])
    assert ys.shape[1] == len(ax.get_xticklabels()) and (ys.sum(axis=0) <= 1 + 1e-9).all()
    assert (ys.max(axis=1) > case.EXPONENT_FLOOR).all()
    labels = [t.get_text() for t in ax.get_xticklabels()]
    bold = [i for i, t in enumerate(ax.get_xticklabels()) if t.get_fontweight() == "bold"]
    assert labels[-1] == "∞ (limit)" and len(bold) == 1
    assert abs(float(labels[bold[0]]) - small_fit.tau) <= 0.02 * small_fit.tau + 0.5
    assert any(t.get_text().startswith("n_eff = ") for t in fig.axes[1].texts)
    assert not [i for i in ax.images]  # a line chart, not a heat map
    plt.close(fig)


def test_spread_labels_keep_the_order_and_a_gap():
    ys = case._spread_labels([0.1, 0.1, 0.1], 0.02)
    assert np.allclose(np.diff(np.sort(ys)), 0.02) and ys.min() == 0.1


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
    assert t.nondominated.tolist() == [2134, 236]  # with thirteen metrics no design is dominated
    assert (t["of"] == 2134).all()
    assert t.share.round(3).tolist() == [1.0, 0.111]


# the K record on the thirteen-metric data of record (the WP30 gate: 3,000 designs per regime, host-
# recorded), as k_terms.py prints it: tau, objective_, frac_above_, term rows; then gamma and radius
# (the radius scales with the number of metrics)
RECORD = {
    "primary": {
        1: (41.72, 0.121792, 0.0979, [2134]),
        2: (113.22, 0.087426, 0.0951, [934, 1200]),
        3: (135.76, 0.069274, 0.1078, [459, 621, 1054]),
    },
    "stock": {
        1: (45.68, 0.114827, 0.1062, [2355]),
        2: (103.40, 0.099601, 0.1023, [986, 1369]),
        3: (135.76, 0.080296, 0.0960, [705, 797, 853]),
    },
}
MARGIN = {
    ("primary", 2): (0.0003768, 0.0000255), ("primary", 3): (0.0004214, 0.0000285),
    ("stock", 2): (0.000263, 0.0000175), ("stock", 3): (0.0001, 0.0000066),
}  # fmt: skip
GAP_K1 = {"primary": 6.96e-6, "stock": 3.17e-5}


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
    assert sorted(f["rows"]) == [459, 621, 1054]
    assert sorted(f.share.round(3)) == [0.061, 0.344, 0.594]
    assert sorted(f["n_lemma"]) == [7, 8, 8]
    assert sorted(f["near-frontier"]) == [50, 188, 297]
    assert (f["gap G_k"] < 1e-12).all()
    big = f.loc[f.share.idxmax()]
    assert big["contending set"].startswith("peak slew power, pointing error")
    assert big["largest exponents"].startswith("peak slew power 0.417")


def test_case_k_terms_equal_the_primary_record(primary, primary_fits):
    """The terms of the case's several-term reading (K = 2): in the estimator's order, the larger
    term first (descending term share), to the precision the reading needs."""
    f = case.term_table(primary, primary_fits, K=case.CASE_K)
    assert list(f.term) == [1, 2] and list(f.share.round(2)) == [0.74, 0.26]
    assert list(f["rows"]) == [1200, 934] and list(f["near-frontier"]) == [318, 119]
    assert sorted(f["n_lemma"]) == [7, 8] and (f["gap G_k"] < 1e-12).all()
    assert f["largest exponents"].iloc[0].startswith("peak slew power 0.4")
    assert f["largest exponents"].iloc[1].startswith("unit cost 0.2")


def test_thin_term_is_reported_from_the_estimator_and_gets_its_reason(primary, primary_fits):
    """WP23 data gate: the guard of ten is applied per term, the thin term's reading replaced."""
    import matplotlib.pyplot as plt

    # at the data of the WP30 gate every term has the rows at the K = 1 band (188, 297, 50); half
    # the K = 3 fit's own band leaves the third term with three
    fit, band = primary_fits[3], 0.5 * primary_fits[3].band
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
    texts = [t.get_text().replace("\n", " ") for ax in fig.axes for t in ax.texts]
    assert any(t == "3 near-frontier designs; no association reading" for t in texts)
    assert len(fig.axes) == 6  # every term drawn: three panels, three colour bars
    plt.close(fig)


def test_k1_contending_set_equals_the_record(primary, primary_fits, stock, stock_fits):
    p = case.tension_table(primary, primary_fits[1]).iloc[0]
    assert p["contending set"] == (
        "unit cost, available power, pointing error, fleet cost, momentum headroom, settling time, "
        "depth of discharge"
    )
    assert p.n_lemma == 7 and p["near-frontier"] == 238
    s = case.tension_table(stock, stock_fits[1]).iloc[0]
    assert set(s["contending set"].split(", ")) == {
        "momentum headroom", "available power", "total mass", "settling time", "pointing error",
        "depth of discharge", "unit cost", "fleet cost",
    }  # fmt: skip
    assert s.n_lemma == 8 and s["near-frontier"] == 293


def test_regime_comparison_on_frozen_data():
    t = case.regime_comparison().set_index("quantity")
    assert t.loc["feasible n", "primary"] == "2134 (548 / 707 / 879)"
    assert t.loc["band 1/tau, near-frontier designs", "primary"] == "0.0240, 238"
    assert t.loc["band 1/tau, near-frontier designs", "stock"] == "0.0219, 293"


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
    assert len(t) == 3 and (t["max |recorded - refit|"] < 1e-5).all()
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
    # A cold subprocess with an empty PATH starts slower on Windows (2.4 s observed on the runner).
    limit = 5.0 if sys.platform == "win32" else 2.0
    assert float(dt) < limit
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
    assert t.loc["baseline", "tau"] == pytest.approx(41.7158, rel=1e-4)  # the K = 1 record
    assert t.loc["baseline", "n_lemma"] == 7
    r = case.category_refits(primary)
    assert r.designs.tolist() == [548, 707, 879]


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


def test_chosen_k_is_the_k_where_the_largest_drop_in_the_mean_slack_lands():
    table = pd.DataFrame({"K": [1, 2, 3, 4], "drop": [np.nan, 0.08, 0.02, 0.01]})
    assert case.chosen_k(table) == 2
    assert case.chosen_k(table.assign(drop=[np.nan, 0.02, 0.09, 0.01])) == 3
    assert case.CASE_K in case.CHOOSE_KS and case.chosen_k(table) == case.CASE_K


def test_choosing_k_table_reads_the_one_term_temperature_and_each_ks_own(small):
    fits = case.k_fits(small, Ks=(1, 2))
    t = case.choosing_k_table(small, fits, Ks=(1, 2))
    assert list(t.columns) == ["K", "mean slack", "drop", "thinnest share",
                               "thinnest share, own tau", "movement"]  # fmt: skip
    assert list(t.K) == [1, 2] and np.isnan(t["drop"].iloc[0]) and np.isnan(t.movement.iloc[0])
    fixed = case.mean_slack_fixed_tau(small, fits)  # the one-term temperature, the same fits
    assert np.allclose(t["mean slack"], fixed.mean_slack_)
    assert t["drop"].iloc[1] == pytest.approx(t["mean slack"].iloc[0] - t["mean slack"].iloc[1])
    assert t["thinnest share, own tau"].iloc[1] == pytest.approx(
        fits[2].estimator.term_share_.min()
    )
    assert 0 < t.movement.iloc[1] <= 2  # summed absolute differences of exponents summing to one


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
    # the title wraps onto two lines (it ran under the colour bar); the words are the same
    assert " ".join(ax.get_title().split()) == (
        f"term 1: {rep.lemma_name} ({n} metric{plural} in the contending set)"
    )
    from matplotlib.patches import Rectangle

    assert sum(isinstance(p, Rectangle) for p in ax.patches) == n  # the outlined members
    plt.close(fig)


# ---- after the fit: associations, requirements, design sets (the WP23 close-out) --------------


@pytest.mark.parametrize("regime", ["primary", "stock"])
def test_association_step_covers_every_pair_and_names_the_one_axis_pairs(regime, request):
    """R-25: 78 pairs of the thirteen traded metrics; the named set is the pairs at |Spearman|
    >= 0.99 (on the data of the WP30 gate: the available power and the energy balance, one axis
    at 0.9996 in the spike's data; the power margin and the energy balance stay below, 0.982 and
    0.988), and the summed reading sums that pair's exponents."""
    study = request.getfixturevalue(regime)
    t = case.association_all_pairs(study)
    assert len(t) == 78 and case.ONE_AXIS == 0.99
    assert {frozenset(p) for p in zip(t["metric a"], t["metric b"], strict=True)} == {
        frozenset((a, b)) for i, a in enumerate(study.names) for b in study.names[i + 1 :]
    }
    named = case.one_axis_pairs(t)
    assert named == [
        (a, b) for a, b, s in zip(t["metric a"], t["metric b"], t["spearman"], strict=True)
        if abs(s) >= 0.99
    ]  # fmt: skip
    # host-recorded at the gate: the pair spike C found, nothing else
    assert [frozenset(p) for p in named] == [frozenset(("available power", "energy balance"))]
    top = t.iloc[0]
    assert {top["metric a"], top["metric b"]} == {"available power", "energy balance"}
    assert top["spearman"] > 0.999
    fits = case.k_fits(study)
    summed = case.summed_exponents(study, fits, named)
    a, b = named[0]
    # one table across K: no pair column, the metrics' own names, the sum
    assert list(summed.columns) == ["K", "term", a, b, "sum"]
    assert sorted(set(summed["K"])) == sorted(fits)
    assert len(summed) == sum(K for K in fits)
    assert np.allclose(summed["sum"], summed[a] + summed[b])


def test_requirements_are_the_models_budgets():
    """The case's four thresholds are the literals of the model's part ``budgets``."""
    import re

    text = (ADCS / "model_v2" / "cubesat.sysml").read_text(encoding="utf-8")
    lit = {
        name: float(v)
        for name, v in re.findall(
            r"attribute (\w+Limit|launchBudget) : \w+ = ([\d.]+(?:e\d+)?)", text
        )
    }
    rate = float(re.search(r"launchRate : Real = ([\d.]+)", text).group(1))
    req = {a: lim for a, (lim, _) in case.CUBESAT.requirements.items()}
    assert req == {
        "peak_slew_power_w": lit["peakSlewPowerLimit"],
        "pointing_error_deg": lit["pointingErrorLimit"],
        "control_effort": lit["controlEffortLimit"],
        "total_mass_kg": lit["launchBudget"] / rate,
    }
    cost = {a: lim for a, (lim, _) in case.CUBESAT.cost_requirements.items()}
    assert cost == {
        "unit_cost_usd": lit["unitCostLimit"],
        "fleet_cost_usd": lit["fleetCostLimit"],
    }


def test_every_cost_requirement_is_read_at_the_designs_own_fleet_size(primary):
    """No floating requirement: the unit cost limit is read on each design's own cost column, so no
    single satellite clears it (the supervisor's words), and the fleet cost limit on the fleet's."""
    feas = primary.feasible
    assert not (feas.loc[feas["fleet_size"] == 1, "unit_cost_usd"] <= 350000.0).any()
    for a, share in (("unit_cost_usd", 0.762), ("fleet_cost_usd", 0.714)):
        ok = case.requirement_mask(feas, only=a)
        assert ok.mean() == pytest.approx(share, abs=5e-4)
    assert case.requirement_mask(feas).mean() > case.requirement_mask(feas, costs=True).mean()


def test_requirements_table_prices_each_requirement_as_spike_b(primary, primary_fits, stock,
                                                                stock_fits):  # fmt: skip
    """R-26: the pass fractions, the near-frontier designs excluded and the prices of spike B
    (`WP23-rounds/spikes/spike-B-requirements-and-the-fit.md`, sections 1 and 2)."""
    p = case.requirements_table(primary, primary_fits[1]).set_index("requirement")
    s = case.requirements_table(stock, stock_fits[1]).set_index("requirement")
    # the four threshold requirements, the unit and fleet cost requirements, then all six jointly
    assert p["pass (feasible)"].round(3).tolist() == [0.588, 0.952, 0.574, 0.946, 0.762, 0.714,
                                                      0.257]  # fmt: skip
    assert s["pass (feasible)"].round(3).tolist() == [0.641, 0.656, 0.885, 0.952, 0.758, 0.710,
                                                      0.222]  # fmt: skip
    assert p["near-frontier excluded"].tolist() == ["108 of 238", "8 of 238", "95 of 238",
                                                    "12 of 238", "64 of 238", "57 of 238",
                                                    "178 of 238"]  # fmt: skip
    assert s["near-frontier excluded"].tolist() == ["145 of 293", "118 of 293", "32 of 293",
                                                    "9 of 293", "66 of 293", "85 of 293",
                                                    "241 of 293"]  # fmt: skip
    assert p.loc["unit cost", "limit"] == "350,000 USD per satellite"
    assert p.loc["fleet cost", "limit"] == "6,000,000 USD per fleet"
    assert p.loc["unit cost", "price (bands)"] == pytest.approx(5.31, abs=0.01)
    assert s.loc["fleet cost", "price (bands)"] == pytest.approx(0.49, abs=0.01)
    assert p.loc["pointing error", "price (log V)"] == pytest.approx(0.0019, abs=1e-4)
    assert s.loc["pointing error", "price (bands)"] == pytest.approx(0.79, abs=0.01)
    assert s.loc["control effort", "price (bands)"] == pytest.approx(0.91, abs=0.01)
    assert p.loc["control effort", "price (log V)"] == 0.0  # zero exponent: no price at K = 1
    assert s.loc["control effort", "largest elasticities"] == (
        "depth of discharge -0.77; pointing error -0.72"
    )


@pytest.mark.slow
def test_design_sets_share_the_feasible_conditioning():
    """R-27, OD10 (a): three sets per regime in the feasible set's conditioning; sizes; the
    one-term contending set of the constrained set against the feasible set's."""
    sets = {r: case.design_sets(r) for r in case.CUBESAT.regimes}
    t = case.design_sets_table(sets=sets).set_index(["regime", "set"])
    assert t["designs"].tolist() == [3000, 2134, 814, 3000, 2355, 882]
    for by_set in sets.values():
        conds = {id(st.conditioner) for st, _ in by_set.values()}
        assert len(conds) == 1  # one conditioning for every set
    feasible = t.loc[("primary", "feasible"), "contending set"]
    # the same seven metrics; the order is by exponent and moves with the set (WP30 gate)
    met = t.loc[("primary", "thresholds met"), "contending set"]
    assert set(met.split(", ")) == set(feasible.split(", "))
    place = case.design_sets_placement(sets=sets)
    assert len(place) == 14 and set(place["design"]) >= {"baseline configuration", "proposal_2"}
    base = place[place.design == "baseline configuration"]
    assert not base["meets the thresholds"].any()  # it fails the pointing-error threshold


@pytest.mark.slow
def test_the_baseline_configuration_is_the_oracles():
    """The case's record of the baseline configuration is what the v2 oracle measures."""
    from experiments import cubesat_oracle as co

    text = (ADCS / "model_v2" / "cubesat.sysml").read_text(encoding="utf-8")
    oracle = co.CubesatOracle(text, "nominalSlew", "baseline", workers=1)
    base = case.CUBESAT.baseline_configuration
    got = oracle({k: base[k] for k in co.CONFIG_NAMES})
    for k in (*co.ATTRIBUTE_NAMES, *co.FLAG_NAMES):
        assert got[k] == pytest.approx(base[k], rel=1e-6), k


def _docs_block(first_line):
    text = (ADCS.parents[1] / "docs" / "examples.md").read_text(encoding="utf-8")
    start = text.index("```text\n" + first_line + "\n") + len("```text\n" + first_line + "\n")
    return text[start : text.index("```", start)].rstrip("\n")


DOCS_LABELS = {"primary": "primary", "stock": "stock"}  # the regimes as the paper names them


def test_the_docs_requirements_block_is_the_case_modules():
    """The docs' case page prints ``requirements_summary`` (R-26), generated, not typed."""
    assert _docs_block("# case.requirements_summary()") == case.requirements_summary(
        labels=DOCS_LABELS
    )


def test_the_requirements_prices_are_also_in_currency():
    """The excess column converts the price to USD (P8 final read F3): the median of the excluded
    near-frontier designs' value over the limit, USD per satellite for the unit cost, USD per
    fleet for the fleet cost, and the total mass at the launch rate; none for the other three."""
    for regime in case.CUBESAT.regimes:
        study = case.load_study(regime)
        fit = case.fit_study(study)
        table = case.requirements_table(study, fit).set_index("requirement")
        near = np.abs(fit.estimator.score_samples(study.M)) < fit.band
        for attr, rate in (
            ("unit_cost_usd", 1.0),
            ("fleet_cost_usd", 1.0),
            ("total_mass_kg", case.LAUNCH_USD_PER_KG),
        ):
            limit = (case.CUBESAT.requirements | case.CUBESAT.cost_requirements)[attr][0]
            over = near & ~(study.feasible[attr].to_numpy() <= limit)
            want = float(np.median(study.feasible.loc[over, attr].to_numpy() - limit)) * rate
            assert table.loc[case.CUBESAT.short[attr], "excess (USD)"] == pytest.approx(want)
        assert case.LAUNCH_USD_PER_KG == 7000.0
        assert table["excess (USD)"].notna().sum() == 3
        assert table.loc["all jointly", "excess (USD)"] != table.loc["all jointly", "excess (USD)"]
    text = case.requirements_summary(labels=DOCS_LABELS)
    assert "unit cost        35,200 | 27,300 USD per satellite" in text
    assert "fleet cost       1,130,000 | 1,140,000 USD per fleet" in text
    assert "total mass       1,880 | 1,730 USD of launch per satellite" in text


@pytest.mark.slow
def test_the_docs_design_sets_block_is_the_case_modules():
    """The docs' case page prints ``design_sets_summary`` (R-27), generated, not typed."""
    assert _docs_block("# case.design_sets_summary()") == case.design_sets_summary(
        labels=DOCS_LABELS
    )


def test_ternary_pair_figure_is_two_panels_one_key_and_the_regions_the_page_names():
    """Figure 6 of the examples page (supervisor, WP28-decisions): panel A and panel B, each fitted
    with two terms, one shared key; the words are read from the fits' exponents."""
    import matplotlib
    from matplotlib.text import Text

    from hyperbolic_trade_space import plotting

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    schemes, sizes = plotting._TERN_SCHEMES, plotting._TERN_LABEL_SIZES
    fits = case.ternary_pair_fits()
    assert list(fits) == ["A", "B"]
    assert [est.exponents_.shape[0] for _, est in fits.values()] == [2, 2]
    fig = case.ternary_pair_figure(fits)
    assert plotting._TERN_SCHEMES is schemes and plotting._TERN_LABEL_SIZES is sizes
    assert len(fig.axes) == 2 and len(fig.legends) == 1 and len(fig.legends[0].get_texts()) == 5

    def words(ax):
        found = ax.findobj(lambda a: (a.get_gid() or "").startswith("ternary-label-"))
        return {" ".join(t.get_text().split()) for t in found}

    assert words(fig.axes[0]) == {
        "pointing error trades against control effort",
        "total mass trades against pointing error",
    }
    assert words(fig.axes[1]) == {
        "settling time trades against control effort",
        "depth of discharge alone",
    }
    small = [t.get_text() for t in fig.findobj(Text) if t.get_text().strip() and
             t.get_fontsize() < case.FIGURE_MIN_FONT_PT]  # fmt: skip
    assert not small, small
    for _, est in fits.values():  # no design colouring by cell: one neutral colour
        assert est.exponents_.sum(axis=1) == pytest.approx(1.0)
    plt.close(fig)
