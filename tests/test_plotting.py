"""Plotting smoke tests (Agg backend): each function returns an Axes and uses the vocabulary."""

import re
from pathlib import Path
from types import SimpleNamespace

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
from hyperbolic_trade_space import plotting as P


@pytest.fixture(autouse=True)
def _close():
    yield
    plt.close("all")


def colors_of(ax):
    out = set()
    for line in ax.lines:
        out.add(matplotlib.colors.to_hex(line.get_color()))
    return out


def test_log_plane_draws_frontier_line_in_black_and_band_in_grey():
    X, _ = make_frontier_data(100, 2, random_state=0)
    ax = P.plot_log_plane(HyperbolicTradeSpace(np.inf).fit(X), X)
    assert isinstance(ax, Axes)
    assert matplotlib.colors.to_hex(P.FRONTIER_COLOR) in colors_of(ax)
    assert any(
        np.allclose(p.get_facecolor()[:3], matplotlib.colors.to_rgb(P.BAND_COLOR))
        for p in ax.patches
    )
    # the frontier line is w.u = beta
    hts = HyperbolicTradeSpace(np.inf).fit(X)
    xs, ys = ax.lines[0].get_data()
    w, beta = hts.exponents_[0], hts.log_offset_[0]
    np.testing.assert_allclose(w[0] * np.array(xs) + w[1] * np.array(ys), beta, atol=1e-9)


def test_log_plane_wrong_dimension_and_categories():
    X, _ = make_frontier_data(50, 3, random_state=0)
    with pytest.raises(ValueError, match="needs 2 metrics"):
        P.plot_log_plane(HyperbolicTradeSpace().fit(X), X)
    X2, _ = make_frontier_data(50, 2, random_state=0)
    ax = P.plot_log_plane(HyperbolicTradeSpace().fit(X2), X2, color=np.arange(50) % 3)
    assert ax.get_legend() is not None


def test_surface_3d_returns_3d_axes_and_validates():
    X, _ = make_frontier_data(80, 3, random_state=1)
    hts = HyperbolicTradeSpace().fit(X)
    ax = P.plot_frontier_surface_3d(hts, X)
    assert isinstance(ax, Axes) and ax.name == "3d"
    assert P.plot_frontier_surface_3d(hts).name == "3d"
    with pytest.raises(ValueError, match="positive exponent"):
        P.plot_frontier_surface_3d(HyperbolicTradeSpace(min_exponent=0.0).fit(X), X, z_index=7)
    fig = plt.figure()
    own = fig.add_subplot(projection="3d")
    assert P.plot_frontier_surface_3d(hts, X, ax=own) is own


def test_frontier_coordinates_one_and_two_coordinates_and_overlays():
    rng = np.random.default_rng(0)
    X1, _ = make_frontier_data(60, 2, random_state=0)
    Z = HyperbolicTradeSpace().fit(X1).transform(X1)
    ax = P.plot_frontier_coordinates(Z[:, :-1], Z[:, -1], holes=[[0.5]], targets=[[0.1], [0.2]])
    assert isinstance(ax, Axes) and ax.get_ylabel() == "log V"
    Z2 = rng.normal(size=(40, 2))
    ax = P.plot_frontier_coordinates(
        Z2, -rng.exponential(size=40), color=np.arange(40) % 2, holes=[[0, 0]], targets=[[1, 1]]
    )
    assert ax.get_ylabel() == "Z1"
    with pytest.raises(ValueError, match="no frontier coordinates"):
        P.plot_frontier_coordinates(np.empty((5, 0)), np.zeros(5))


def test_v_by_variable_numeric_and_categorical_and_existing_ax():
    rng = np.random.default_rng(0)
    lv = -rng.exponential(size=30)
    assert isinstance(P.plot_v_by_variable(rng.normal(size=30), lv), Axes)
    ax = P.plot_v_by_variable(np.array(["x", "y", "z"] * 10), lv, color=np.arange(30) % 2)
    assert [t.get_text() for t in ax.get_xticklabels()] == ["x", "y", "z"]
    _, own = plt.subplots()
    assert P.plot_v_by_variable(np.arange(30), lv, ax=own, label="Kp") is own


def make_report(d=3):
    A = np.eye(d)
    A[0, 1] = A[1, 0] = -0.6
    return SimpleNamespace(
        participating=np.array([True, True] + [False] * (d - 2)),
        exponents=np.array([0.5, 0.5] + [0.0] * (d - 2)),
        association=A,
        tension_directions=np.zeros((0, d - 1)),
        tension_loadings=np.zeros((0, d)),
        contending_set=np.array([0, 1]),
        n_lemma=2,
    )


def test_plot_tensions_with_stand_in_report():
    ax = P.plot_tensions(make_report(), names=["mass", "power", "cost"])
    assert isinstance(ax, Axes)
    assert ax.get_title() == "dilemma (2 metrics contend)"
    assert len(ax.patches) == 2  # contending set outlined
    assert ax.get_images()[0].get_cmap().name == P.TENSION_CMAP
    assert P.plot_tensions(SimpleNamespace(**{**vars(make_report(4)), "n_lemma": 5})).get_title()
    one = make_report(3)
    one.n_lemma, one.contending_set = 1, np.array([0])
    assert P.plot_tensions(one).get_title().startswith("monolemma")


def test_module_does_not_import_matplotlib_at_import_time():
    import subprocess
    import sys

    code = "import sys, hyperbolic_trade_space.plotting; sys.exit('matplotlib' in sys.modules)"
    assert subprocess.run([sys.executable, "-c", code], check=False).returncode == 0


def test_plot_tensions_with_real_report():
    from hyperbolic_trade_space import tensions

    X, _ = make_frontier_data(500, 3, random_state=0)
    hts = HyperbolicTradeSpace().fit(X)
    report = tensions.tension_report(hts, X, band=0.5)
    ax = P.plot_tensions(report, names=["a", "b", "c"])
    assert isinstance(ax, Axes)
    assert ax.get_title().startswith(report.lemma_name)
    assert len(ax.patches) == report.n_lemma


def _k3(d):
    X, _ = make_frontier_data(300, d, n_terms=3, random_state=0)
    return X, HyperbolicTradeSpace(n_terms=3, temperature=np.inf, random_state=0).fit(X)


def _texts(ax):
    out = [ax.get_xlabel(), ax.get_ylabel(), ax.get_title()]
    out += [t.get_text() for t in ax.get_legend().get_texts()] if ax.get_legend() else []
    return " ".join(out).lower()


def test_log_plane_k3_draws_envelope_and_facet_legend():
    X, hts = _k3(2)
    ax = P.plot_log_plane(hts, X)
    g, y = ax.lines[0].get_data()
    u = np.log(X)
    W, b = hts.exponents_, hts.log_offset_
    phi = np.max(np.outer(g, W[:, 0]) + np.outer(y, W[:, 1]) - b, axis=1)
    assert matplotlib.colors.to_hex(P.FRONTIER_COLOR) in colors_of(ax)
    assert np.all(phi[np.isfinite(phi)] <= 1e-9) and np.isfinite(y).all() and len(u) == 300
    labels = [t.get_text() for t in ax.get_legend().get_texts()]
    # platform drift may relabel or empty a facet (WP9 post-review fix 2): test the set only
    assert set(labels) <= {f"facet {k + 1}" for k in range(3)} and len(labels) >= 2
    assert "red" not in _texts(ax)
    assert P.plot_log_plane(hts, X, color="facet").get_legend() is not None


def test_surface_k3_and_coordinates_facet_colouring():
    X, hts = _k3(3)
    ax = P.plot_frontier_surface_3d(hts, X)
    assert ax.name == "3d" and len(ax.collections) >= 2
    assert "facet 1" in _texts(ax) and "red" not in _texts(ax)
    Z = hts.transform(X)
    ax = P.plot_frontier_coordinates(Z[:, :-1], Z[:, -1], color=P.facet_labels(hts, X))
    assert "facet 1" in _texts(ax) and "red" not in _texts(ax)


def test_plot_tensions_list_of_reports_side_by_side():
    axs = P.plot_tensions([make_report(), make_report()], names=["a", "b", "c"])
    assert len(axs) == 2 and axs[1].get_title().startswith("facet 2: dilemma")
    assert isinstance(P.plot_tensions(make_report()), Axes)


def test_log_plane_k3_draws_facet_only_where_it_has_weight_on_both_metrics():
    hts = HyperbolicTradeSpace(n_terms=2, temperature=np.inf)
    hts.exponents_ = np.array([[0.5, 0.5], [0.0005, 1.0]])  # facet 2 below the threshold on m0
    hts.log_offset_ = np.array([0.0, -50.0])  # would dominate the envelope if it were drawn
    hts.n_features_in_ = 2
    X = np.exp(np.random.default_rng(0).normal(size=(40, 2)))
    ax = P.plot_log_plane(hts, X, color=np.arange(40) % 2)
    g, y = ax.lines[0].get_data()
    assert np.allclose(y, (0.0 - 0.5 * g) / 0.5)  # facet 1's line only
    hts.exponents_ = np.array([[0.0005, 1.0], [1.0, 0.0005]])  # no facet has weight on both
    assert len(P.plot_log_plane(hts, X, color=np.arange(40) % 2).lines) == 0


def test_log_plane_k1_unchanged_by_the_envelope_rule():
    X, _ = make_frontier_data(80, 2, random_state=0)
    ax = P.plot_log_plane(HyperbolicTradeSpace().fit(X), X)
    assert len(ax.lines) == 1 and ax.get_legend() is not None


def test_tension_annotations_contrast_with_their_cell():
    A = np.array([[1.0, -1.0, 0.0], [-1.0, 1.0, 0.1], [0.0, 0.1, 1.0]])
    r = SimpleNamespace(
        participating=np.array([True, True, False]),
        exponents=np.array([0.5, 0.5, 0.0]),
        association=A,
        contending_set=np.array([0, 1]),
        n_lemma=2,
    )
    ax = P.plot_tensions(r)
    im = ax.images[0]
    texts = {t.get_text(): t for t in ax.texts if t.get_text()[:1] in "-01"}
    assert len(ax.texts) >= 9
    for t in ax.texts[:9]:
        v = float(t.get_text())
        rgba = im.cmap(im.norm(v))
        lum = 0.2126 * rgba[0] + 0.7152 * rgba[1] + 0.0722 * rgba[2]
        assert t.get_color() == ("black" if lum > 0.5 else "white")
    assert {t.get_color() for t in ax.texts[:9]} == {"black", "white"}
    assert texts


# ---- plot_ternary (WP18) ----------------------------------------------------------------------


@pytest.fixture(scope="module")
def planted3():
    X, _ = make_frontier_data(400, 3, n_terms=3, random_state=11)
    return X, HyperbolicTradeSpace(n_terms=3, temperature=50.0, random_state=0).fit(X)


def _by_gid(ax, prefix):
    found = ax.findobj(lambda a: re.fullmatch(prefix + r"\d+", a.get_gid() or "") is not None)
    return {int(a.get_gid().rsplit("-", 1)[1]): a for a in found}


def test_ternary_markers_sit_at_the_exponent_vectors(planted3):
    X, ts = planted3
    ax = P.plot_ternary(ts, X, lines=True)
    assert isinstance(ax, Axes)
    stars = _by_gid(ax, "ternary-star-")
    assert set(stars) == {0, 1, 2}
    for k, art in stars.items():
        x, y = art.get_offsets()[0]
        top = y / (np.sqrt(3) / 2)
        right = x - top / 2
        np.testing.assert_allclose([top, 1 - top - right, right], ts.exponents_[k], atol=1e-12)
    # colour is not the only cue: each marker has its own shape and a numbered label
    assert len({a.get_paths()[0].vertices.tobytes() for a in stars.values()}) == 3
    assert {int(t.get_text()) for t in _by_gid(ax, "ternary-star-label-").values()} == {1, 2, 3}


def test_ternary_fixed_total_identity_and_peak(planted3):
    """log V = log S + max_k (a_k + sum_j w_kj log c_j) at shares of the total, to 1e-10, and
    facet k's piece is largest among all shares at c = w_k."""
    X, ts = planted3
    fit = P._ternary_geometry(ts, X)
    W = fit["W"]
    a = W @ fit["colmean"] - fit["beta"]
    c = P._ternary_shares(fit, 1.0)
    S = np.exp(fit["U"] - fit["colmean"]).sum(axis=1)
    np.testing.assert_allclose(
        np.log(S) + (a + np.log(c) @ W.T).max(axis=1), ts.score_samples(X), atol=1e-10
    )
    rng = np.random.default_rng(0)
    cs = rng.dirichlet(np.ones(3), size=3000)
    for w in W:
        assert w @ np.log(np.clip(w, 1e-300, None)) >= (np.log(cs) @ w).max() - 1e-12


def test_ternary_regions_partition_the_triangle(planted3):
    X, ts = planted3
    fit = P._ternary_geometry(ts, X)
    pts, reg = P._ternary_regions(fit, fit["spread"], n=120)
    assert np.allclose(pts.sum(axis=1), 1.0) and (pts > 0).all()
    assert set(np.unique(reg)) == {0, 1, 2}
    a = fit["W"] @ fit["colmean"] - fit["beta"]
    assert (reg == (a + fit["spread"] * (np.log(pts) @ fit["W"].T)).argmax(axis=1)).all()


def test_ternary_lines_are_off_by_default_and_add_contours_and_markers(planted3):
    import inspect

    X, ts = planted3
    assert inspect.signature(P.plot_ternary).parameters["lines"].default is False
    plain, lined = P.plot_ternary(ts, X), P.plot_ternary(ts, X, lines=True)
    assert not _by_gid(plain, "ternary-star-")
    assert len(lined.collections) > len(plain.collections)
    assert _by_gid(plain, "ternary-label-").keys() == {0, 1, 2}  # the regions are named in words


def test_ternary_names_schemes_and_ax(planted3):
    X, ts = planted3
    _fig, ax = plt.subplots(figsize=(4, 4))
    names = ["cost", "speed", "range"]
    assert P.plot_ternary(ts, X, names=names, ax=ax, scheme="dark") is ax
    words = " ".join(t.get_text() for t in ax.texts)
    assert "favours cost" in words and "metric 1" not in words
    assert matplotlib.colors.to_hex(ax.lines[-1].get_color()) == "#e8e6e1"
    with plt.rc_context({"axes.labelcolor": "#e8e6e1"}):
        assert P._ternary_scheme("auto") == "dark"
    assert P._ternary_scheme("auto") == "light"
    with pytest.raises(ValueError, match="scheme"):
        P.plot_ternary(ts, X, scheme="blue")
    with pytest.raises(ValueError, match="strictly positive"):
        P.plot_ternary(ts, X * 0.0)


def test_ternary_groups_sum_the_exponents_exactly():
    X, _ = make_frontier_data(300, 6, n_terms=2, random_state=3)
    ts = HyperbolicTradeSpace(n_terms=2, temperature=30.0, random_state=0).fit(X)
    names = list("abcdef")
    groups = {"p": ["a", "b"], "q": ["c"], "r": [3, 4, 5]}
    ax = P.plot_ternary(ts, names=names, groups=groups)
    W = ts.exponents_
    want = np.column_stack([W[:, [0, 1]].sum(1), W[:, [2]].sum(1), W[:, [3, 4, 5]].sum(1)])
    assert np.allclose(want.sum(axis=1), 1.0)
    stars = {
        k: v for k, v in _by_gid(ax, "ternary-star-").items() if v.get_gid() == f"ternary-star-{k}"
    }
    for k, art in stars.items():
        x, y = art.get_offsets()[0]
        top = y / (np.sqrt(3) / 2)
        np.testing.assert_allclose([top, 1 - top - (x - top / 2), x - top / 2], want[k], atol=1e-12)
    assert "favours p" in " ".join(t.get_text() for t in ax.texts)
    with pytest.raises(ValueError, match="exactly one group"):
        P.plot_ternary(ts, names=names, groups={"p": ["a"], "q": ["b"], "r": ["c"]})
    with pytest.raises(ValueError, match="needs 3 metrics"):
        P.plot_ternary(ts, names=names)
    with pytest.raises(ValueError, match="omit X"):
        P.plot_ternary(ts, X, names=names, groups=groups)


def test_ternary_cubesat_groups_are_the_docs_example_and_the_group_sums_hold():
    """WP18 R-7: the docs' grouping (power, mass, attitude control) is a partition of the ten
    metrics, each facet's grouped vector is the group sum of ``exponents_`` and sums to one, and
    the caption's claim holds: only facet 3 carries mass (0.18)."""
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "examples" / "adcs"))
    import case

    study = case.load_study("primary")
    est = case.fit_study(study, K=3).estimator
    groups = {
        "power": [
            "power margin",
            "energy balance",
            "eclipse reserve",
            "peak slew power",
            "depth of discharge",
        ],
        "mass": ["total mass"],
        "attitude control": ["settling time", "slew time", "pointing error", "control effort"],
    }
    ax = P.plot_ternary(est, names=study.names, groups=groups)
    idx = [[study.names.index(n) for n in g] for g in groups.values()]
    want = np.column_stack([est.exponents_[:, g].sum(axis=1) for g in idx])
    assert np.allclose(want.sum(axis=1), 1.0)
    assert (want[:2, 1] < 0.005).all() and round(float(want[2, 1]), 2) == 0.18
    for k, art in _by_gid(ax, "ternary-star-").items():
        x, y = art.get_offsets()[0]
        top = y / (np.sqrt(3) / 2)
        np.testing.assert_allclose([top, 1 - top - (x - top / 2), x - top / 2], want[k], atol=1e-12)
