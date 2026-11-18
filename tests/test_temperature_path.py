"""WP46 D-1: the temperature path (``plotting.temperature_path`` and ``plot_temperature_path``).

The planted table is a known frontier (``make_frontier_data``); the case table is the cubesat's
(slow tests: R-1, the helper reproduces Figure 4's lower panel of ``examples/adcs/case.py``).
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from tradespace import HyperbolicTradeSpace, make_frontier_data
from tradespace.plotting import plot_temperature_path, temperature_path


@pytest.fixture(autouse=True)
def _close():
    yield
    plt.close("all")


@pytest.fixture(scope="module")
def planted():
    X, _ = make_frontier_data(200, 4, noise=0.05, random_state=3)
    est = HyperbolicTradeSpace(temperature=30.0, random_state=0).fit(X)
    return est, X


def test_path_exponents_are_on_the_simplex_and_the_limit_is_last(planted):
    est, X = planted
    path = temperature_path(est, X, temperatures=[4.0, 10.0, 30.0, 100.0, 400.0])
    assert path["temperature"].tolist() == [4.0, 10.0, 30.0, 100.0, 400.0, np.inf]
    assert path["exponents"].shape == (6, 4) and (path["exponents"] >= 0).all()
    assert np.allclose(path["exponents"].sum(axis=1), 1.0)
    assert path["fit_index"] == 2
    assert path["frac_above"][-1] == 0.0  # the supporting envelope has no design above it
    assert (np.diff(path["n_eff"]) <= 1e-9).all()  # a harder maximum leans on fewer designs


def test_the_fit_temperature_is_inserted_unless_a_grid_point_is_within_two_percent(planted):
    est, X = planted
    near = temperature_path(est, X, temperatures=[10.0, 30.4, 90.0])
    assert near["temperature"].tolist() == [10.0, 30.4, 90.0, np.inf] and near["fit_index"] == 1
    far = temperature_path(est, X, temperatures=[10.0, 90.0])
    assert far["temperature"].tolist() == [10.0, 30.0, 90.0, np.inf] and far["fit_index"] == 1


def test_path_at_the_fit_temperature_is_the_fit(planted):
    est, X = planted
    path = temperature_path(est, X, temperatures=[10.0, 90.0])
    assert np.allclose(path["exponents"][path["fit_index"]], est.exponents_[0])
    assert path["frac_above"][path["fit_index"]] == pytest.approx(est.frac_above_)


def test_the_default_sweep_is_twelve_log_spaced_temperatures_and_the_limit(planted):
    est, X = planted
    path = temperature_path(est, X)
    assert 13 <= len(path["temperature"]) <= 14 and path["temperature"][-1] == np.inf
    assert path["temperature"][0] == pytest.approx(3.0)
    assert path["temperature"][-2] == pytest.approx(1000.0)


def test_an_infinite_fit_temperature_has_no_ring(planted):
    _, X = planted
    est = HyperbolicTradeSpace(temperature=np.inf, random_state=0).fit(X)
    path = temperature_path(est, X, temperatures=[10.0, 90.0])
    assert path["fit_index"] == 2
    axs = plot_temperature_path(est, X, temperatures=[10.0, 90.0])
    assert len(axs) == 3


def test_the_helper_refuses_several_terms_and_bad_temperatures(planted):
    est, X = planted
    multi = HyperbolicTradeSpace(n_terms=2, temperature=30.0, random_state=0).fit(X)
    with pytest.raises(ValueError, match="n_terms=1"):
        temperature_path(multi, X)
    with pytest.raises(ValueError, match="positive and finite"):
        temperature_path(est, X, temperatures=[10.0, np.inf])
    with pytest.raises(ValueError, match="positive and finite"):
        temperature_path(est, X, temperatures=[-1.0, 10.0])


def test_the_figure_draws_one_line_per_participating_metric_and_marks_the_fit(planted):
    est, X = planted
    axs = plot_temperature_path(est, X, temperatures=[5.0, 30.0, 200.0], names=list("abcd"))
    assert len(axs) == 3
    ax = axs[2]
    lines = [ln for ln in ax.get_lines() if len(ln.get_xdata()) > 2]
    names = [t.get_text() for t in ax.texts]
    assert len(lines) == len(names) and set(names) <= set("abcd")
    ys = np.array([ln.get_ydata() for ln in lines])
    assert (ys.sum(axis=0) <= 1 + 1e-9).all() and (ys.max(axis=1) > 1e-3).all()
    labels = [t.get_text() for t in ax.get_xticklabels()]
    bold = [i for i, t in enumerate(ax.get_xticklabels()) if t.get_fontweight() == "bold"]
    assert labels[-1] == "∞ (limit)" and labels[bold[0]] == "30" and len(bold) == 1
    assert axs[0].get_ylabel() == "fraction of designs above V = 1"
    assert axs[1].get_ylabel() == "effective sample size"
    dashed = [ln for ln in axs[0].get_lines() if ln.get_linestyle() == "--"]
    assert len(dashed) == 1 and dashed[0].get_ydata()[0] == pytest.approx(0.10)


def test_the_figure_takes_axes_and_default_names(planted):
    est, X = planted
    _fig, axes = plt.subplots(1, 3)
    axs = plot_temperature_path(
        est, X, temperatures=[5.0, 200.0], axes=axes, target_frac_above=None
    )
    assert axs[0] is axes[0] and not [ln for ln in axs[0].get_lines() if ln.get_linestyle() == "--"]
    assert all(t.get_text().startswith("m") for t in axs[2].texts)


@pytest.mark.slow
def test_the_helper_reproduces_the_case_figure_lines_to_the_printed_exponents():
    """R-1 on a sample of the case: the helper's lines are those of ``tau_sweep_lines_figure``."""
    import case

    study = case.load_study("primary", n_max=300)
    fit = case.fit_study(study)
    fig = case.tau_sweep_lines_figure(study, fit)
    theirs = np.array([ln.get_ydata() for ln in fig.axes[2].get_lines() if len(ln.get_xdata()) > 2])
    ours_axes = plot_temperature_path(
        fit.estimator,
        study.M,
        temperatures=np.geomspace(*study.spec.tau_bounds, 12),
        names=study.names,
    )
    ours = np.array([ln.get_ydata() for ln in ours_axes[2].get_lines() if len(ln.get_xdata()) > 2])
    assert [t.get_text() for t in ours_axes[2].texts] == [t.get_text() for t in fig.axes[2].texts]
    assert np.allclose(ours, theirs, atol=5e-4)  # the printed exponents are to three places


# ---- the claims of docs/user-guide/temperature.md (its example table and its sweep) -------------


@pytest.fixture(scope="module")
def page():
    from tradespace import select_temperature

    X, _ = make_frontier_data(
        300, 5, exponents=[0.45, 0.3, 0.15, 0.1, 0.0], noise=0.05, random_state=0
    )
    tau = select_temperature(X, 0.10, bounds=(3, 1e4))
    est = HyperbolicTradeSpace(temperature=tau, random_state=0).fit(X)
    return X, est, temperature_path(est, X)


def test_page_a_metric_leaves_the_support_between_tau_83_and_88(page):
    X, _, path = page
    taus, w = path["temperature"], path["exponents"]
    assert w[path["fit_index"], 4] > 1e-3  # participates at the fit temperature
    assert w[-1, 4] <= 1e-12  # numerically zero at infinity
    for tau, expect_zero in ((83.0, False), (88.0, True), (500.0, True)):
        e = HyperbolicTradeSpace(temperature=tau, random_state=0).fit(X)
        assert (e.exponents_[0, 4] <= 1e-12) == expect_zero
    assert taus[-1] == np.inf


def test_page_the_contending_set_and_how_far_its_exponents_move(page):
    _, _, path = page
    w = path["exponents"]
    assert (w[-1, :4] > 1e-9).all() and w[-1, 4] <= 1e-9  # the first four contend
    moves = w[:, :4].max(axis=0) - w[:, :4].min(axis=0)
    assert moves.max() < 0.09 and moves.argmax() == 2


def test_page_the_price_in_effective_sample_size(page):
    X, est, path = page
    assert len(X) == 300
    assert path["n_eff"][0] == pytest.approx(162, abs=0.5)  # tau = 3
    assert est.n_eff_ == pytest.approx(5.3, abs=0.05) and est.frac_above_ == pytest.approx(
        0.1, abs=0.01
    )
    assert path["n_eff"][-1] == pytest.approx(1.3, abs=0.05)  # tau = infinity


def test_page_a_higher_target_gives_a_lower_temperature_and_more_designs_in_the_fit(page):
    from tradespace import select_temperature

    X, _, _ = page
    rows = []
    for target in (0.05, 0.10, 0.20, 0.30):
        t = select_temperature(X, target, bounds=(3, 1e4))
        e = HyperbolicTradeSpace(temperature=t, random_state=0).fit(X)
        rows.append((t, e.frac_above_, e.n_eff_))
    taus, fracs, neffs = np.array(rows).T
    assert (np.diff(taus) < 0).all() and (np.diff(neffs) > 0).all() and (np.diff(fracs) > 0).all()


def test_page_the_support_weights_become_uniform_as_tau_falls_to_zero(page):
    X, _, _ = page
    e = HyperbolicTradeSpace(temperature=0.01, random_state=0).fit(X)
    assert e.n_eff_ > 0.99 * len(X)
