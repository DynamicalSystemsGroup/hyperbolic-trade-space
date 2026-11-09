"""Plotting helpers with one visual vocabulary (matplotlib only, imported lazily).

Every function accepts an optional ``ax``, creates a figure when it is ``None``, draws, and
returns the ``Axes``. Nothing here calls ``plt.show()``; backends are the caller's business.

Visual vocabulary (module constants, shared by every function)
---------------------------------------------------------------
* **Frontier** ``V = 1`` (``log V = 0``): black (``FRONTIER_COLOR``), a line, plane or surface.
* **Near-frontier band** (``-band <= log V <= 0``, default ``1/tau``, ``0.1`` at ``tau = inf``):
  grey (``BAND_COLOR``), a shaded strip or region; where no region can be shaded, the points
  inside it are grey.
* **Holes** (white space found by ``hyperbolic_trade_space.gaps``): red (``HOLE_COLOR``).
* **Targets** (frontier points to aim for): open markers (no fill, black edge).
* **Data and categories**: the first colour of one qualitative, colour-blind-safe palette
  (``CATEGORY_COLORS``) for plain data, successive colours for categories.
* **Tension** (``plot_tensions``): a diverging map (``TENSION_CMAP``), negative association
  (tension) to positive (aligned); the contending set is outlined in black.

Examples
--------
>>> import matplotlib
>>> matplotlib.use("Agg")
>>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
>>> from hyperbolic_trade_space.plotting import plot_frontier_coordinates
>>> X, _ = make_frontier_data(100, 3, random_state=0)
>>> hts = HyperbolicTradeSpace().fit(X)
>>> Z = hts.transform(X)
>>> ax = plot_frontier_coordinates(Z[:, :-1], Z[:, -1])
>>> ax.get_xlabel()
'Z0'
"""

import numpy as np
from sklearn.utils.validation import check_is_fitted

FRONTIER_COLOR = "black"
BAND_COLOR = "0.7"
HOLE_COLOR = "#D55E00"
CATEGORY_COLORS = ("#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#F0E442")
DATA_COLOR = CATEGORY_COLORS[0]
TENSION_CMAP = "PuOr"
PARTICIPATION = 1e-3  # a facet participates in a metric above this exponent (tension report's)

__all__ = [
    "BAND_COLOR",
    "CATEGORY_COLORS",
    "DATA_COLOR",
    "FRONTIER_COLOR",
    "HOLE_COLOR",
    "TENSION_CMAP",
    "facet_labels",
    "plot_frontier_coordinates",
    "plot_frontier_surface_3d",
    "plot_log_plane",
    "plot_tensions",
    "plot_v_by_variable",
]


def _plt():
    import matplotlib.pyplot as plt

    return plt


def _axes(ax, projection=None):
    if ax is not None:
        return ax
    fig = _plt().figure()
    return fig.add_subplot(projection=projection) if projection else fig.add_subplot()


def _band(estimator, band):
    if band is not None:
        return float(band)
    tau = getattr(estimator, "temperature", np.inf)
    return 0.1 if not np.isfinite(tau) else 1.0 / float(tau)


def _point_colors(color, n, mask=None):
    """Per-point colours: categories from the palette, or data colour (band points grey)."""
    if color is None:
        cols = np.array([DATA_COLOR] * n, dtype=object)
        if mask is not None:
            cols[mask] = BAND_COLOR
        return list(cols), None
    color = np.asarray(color)
    cats, codes = np.unique(color, return_inverse=True)
    pal = [CATEGORY_COLORS[i % len(CATEGORY_COLORS)] for i in range(len(cats))]
    return [pal[c] for c in codes], (cats, pal)


def _category_legend(ax, cats_pal):
    if cats_pal is None:
        return
    from matplotlib.lines import Line2D

    cats, pal = cats_pal
    handles = [
        Line2D([], [], marker="o", linestyle="", color=c, label=str(k))
        for k, c in zip(cats, pal, strict=True)
    ]
    ax.legend(handles=handles, frameon=False)


def facet_labels(estimator, X):
    """Facet of each row of ``X`` as ``"facet 1" .. "facet K"``, for ``color=`` (``K > 1``)."""
    return np.array([f"facet {k + 1}" for k in estimator.assign_facets(X)])


def _fitted_chart(estimator, d_required=None):
    """Exponent rows ``(K, d)`` and offsets ``(K,)``; ``K = 1`` is the single frontier."""
    check_is_fitted(estimator, "exponents_")
    W = np.atleast_2d(np.asarray(estimator.exponents_, dtype=float))
    if d_required is not None and W.shape[1] != d_required:
        raise ValueError(f"this plot needs {d_required} metrics; the estimator has {W.shape[1]}")
    return W, np.asarray(estimator.log_offset_, dtype=float).ravel()


def plot_log_plane(estimator, X, color=None, band=None, ax=None):
    """Two metrics in the log plane: data, the frontier line and the near-frontier band.

    Parameters
    ----------
    estimator : HyperbolicTradeSpace
        Fitted on two metrics.
    X : array-like of shape (n_samples, 2)
        Positive metrics to scatter (typically the training data).
    color : array-like of shape (n_samples,), default=None
        Optional categories, coloured from ``CATEGORY_COLORS``. For ``n_terms > 1`` the default
        (or ``"facet"``) colours by facet, legend ``facet 1 .. facet K``.
    band : float, default=None
        Band width in ``log V``; default ``1/tau`` (``0.1`` at ``tau = inf``). For ``n_terms > 1``
        the black line is the envelope ``Phi_K = 0`` (the hard maximum of the facet lines) and the
        band the strip down to ``Phi_K = -band``; a facet is drawn only where it has weight on
        both plotted metrics (exponents above ``PARTICIPATION``), and no envelope is drawn if none.
    ax : matplotlib Axes, default=None

    Returns
    -------
    matplotlib.axes.Axes
        Axes in ``log m0`` vs ``log m1``; the frontier is the black line ``w.u = beta``.

    Examples
    --------
    >>> import matplotlib
    >>> matplotlib.use("Agg")
    >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
    >>> X, _ = make_frontier_data(80, 2, random_state=0)
    >>> ax = plot_log_plane(HyperbolicTradeSpace().fit(X), X)
    >>> ax.get_xlabel()
    'log m0'
    """
    W, bk = _fitted_chart(estimator, 2)
    w, beta = W[0], bk[0]
    X = np.asarray(X, dtype=float)
    if np.any(X <= 0):
        raise ValueError("plot_log_plane needs strictly positive metrics")
    u = np.log(X)
    if len(W) > 1 and (color is None or isinstance(color, str)):
        color = facet_labels(estimator, X)
    b = _band(estimator, band)
    ax = _axes(ax)
    if len(W) > 1:
        # envelope Phi_K = 0: the lowest facet line m1(m0), over facets that bound m1 from above
        g, ok = np.linspace(u[:, 0].min(), u[:, 0].max(), 200), W.min(axis=1) > PARTICIPATION

        def edge(s):
            return np.min((bk[ok] - s - np.outer(g, W[ok, 0])) / W[ok, 1], axis=1)

        if ok.any():
            ax.fill_between(
                g, edge(b), edge(0.0), color=BAND_COLOR, alpha=0.5, linewidth=0,
                label=f"band (log V >= -{b:.3g})",
            )  # fmt: skip
            ax.plot(g, edge(0.0), color=FRONTIER_COLOR, label="frontier V = 1 (envelope)")
    else:
        n2 = float(w @ w)
        p = beta * w / n2
        t = np.array([w[1], -w[0]]) / np.sqrt(n2)
        s = 1.1 * max(np.abs((u - p) @ t).max(), 1e-9)
        lo, hi = p - s * t, p + s * t
        shift = b * w / n2
        ax.fill(
            [lo[0], hi[0], hi[0] - shift[0], lo[0] - shift[0]],
            [lo[1], hi[1], hi[1] - shift[1], lo[1] - shift[1]],
            color=BAND_COLOR,
            alpha=0.5,
            linewidth=0,
            label=f"band (log V >= -{b:.3g})",
        )
        ax.plot([lo[0], hi[0]], [lo[1], hi[1]], color=FRONTIER_COLOR, label="frontier V = 1")
    cols, cats = _point_colors(color, len(u))
    ax.scatter(u[:, 0], u[:, 1], c=cols, s=14, zorder=3)
    ax.set_xlabel("log m0")
    ax.set_ylabel("log m1")
    if cats is None:
        ax.legend(frameon=False)
    else:
        _category_legend(ax, cats)
    return ax


def plot_frontier_surface_3d(estimator, X=None, z_index=None, grid=25, color=None, ax=None):
    """Three metrics: the frontier surface ``m_z = f(m_x, m_y)`` with the data around it.

    Parameters
    ----------
    estimator : HyperbolicTradeSpace
        Fitted on three metrics.
    X : array-like of shape (n_samples, 3), default=None
        Positive metrics to scatter; also sets the plotted range (default: the unit cube around
        ``exp(beta)``).
    z_index : int, default=None
        Metric drawn on the vertical axis; default the one with the largest exponent.
    grid : int, default=25
        Grid points per horizontal axis.
    color : array-like of shape (n_samples,), default=None
        Optional categories for the points. Without it, near-frontier points are grey; for
        ``n_terms > 1`` points are coloured by facet and the surface is the lowest facet plane
        (the envelope ``Phi_K = 0``).
    ax : Axes3D, default=None
        Must be a 3-D axes when given.

    Returns
    -------
    mpl_toolkits.mplot3d.axes3d.Axes3D
        The frontier is the black wireframe surface ``V = 1`` (metric units).

    Examples
    --------
    >>> import matplotlib
    >>> matplotlib.use("Agg")
    >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
    >>> X, _ = make_frontier_data(80, 3, random_state=0)
    >>> ax = plot_frontier_surface_3d(HyperbolicTradeSpace().fit(X), X)
    >>> ax.name
    '3d'
    """
    W, bk = _fitted_chart(estimator, 3)
    z = int(np.argmax(W.max(axis=0))) if z_index is None else int(z_index)
    if not 0 <= z < 3 or W[:, z].max() <= 0:
        raise ValueError("z_index must select a metric with a positive exponent")
    x, y = [i for i in range(3) if i != z]
    ax = _axes(ax, projection="3d")
    if X is not None:
        X = np.asarray(X, dtype=float)
        if np.any(X <= 0):
            raise ValueError("plot_frontier_surface_3d needs strictly positive metrics")
        lo, hi = X.min(axis=0), X.max(axis=0)
    else:
        lo = hi = None
    gx = np.linspace(*(np.log([lo[x], hi[x]]) if lo is not None else (-1, 1)), grid)
    gy = np.linspace(*(np.log([lo[y], hi[y]]) if lo is not None else (-1, 1)), grid)
    GX, GY = np.meshgrid(gx, gy)
    # the lowest facet plane over the facets that bound m_z from above (one plane at K = 1)
    GZ = np.min(
        [(bk[k] - W[k, x] * GX - W[k, y] * GY) / W[k, z] for k in range(len(W)) if W[k, z] > 0],
        axis=0,
    )
    zmax = np.log(hi[z]) if hi is not None else GZ.max()
    zmin = np.log(lo[z]) if lo is not None else GZ.min()
    GZ = np.where((zmax >= GZ) & (zmin <= GZ), GZ, np.nan)
    ax.plot_wireframe(
        np.exp(GX), np.exp(GY), np.exp(GZ), color=FRONTIER_COLOR, linewidth=0.5, alpha=0.6
    )
    if X is not None:
        band = _band(estimator, None)
        near = estimator.score_samples(X) >= -band
        if len(W) > 1 and (color is None or isinstance(color, str)):
            color = facet_labels(estimator, X)
        cols, cats = _point_colors(color, len(X), near)
        ax.scatter(X[:, x], X[:, y], X[:, z], c=cols, s=10)
        _category_legend(ax, cats)
    ax.set_xlabel(f"m{x}")
    ax.set_ylabel(f"m{y}")
    ax.set_zlabel(f"m{z}")
    return ax


def plot_frontier_coordinates(Z, log_v, color=None, holes=None, targets=None, band=None, ax=None):
    """Designs in the chart: position along the frontier and distance from it.

    One coordinate (two metrics): ``Z0`` against ``log V``, the frontier ``log V = 0`` as a black
    line, the band as a grey strip. Two or more coordinates: the ``Z0``-``Z1`` plane, with
    near-frontier points (``log V >= -band``) ringed in black.

    Parameters
    ----------
    Z : array-like of shape (n_samples, n_metrics - 1)
        Chart coordinates (at least one column).
    log_v : array-like of shape (n_samples,)
    color : array-like of shape (n_samples,), default=None
        Optional categories, coloured from ``CATEGORY_COLORS``. For ``K > 1`` pass
        ``facet_labels(estimator, X)`` to colour by facet (``log V = 0`` is already the envelope).
    holes : array-like of shape (n_holes, n_metrics - 1), default=None
        Hole locations, drawn red.
    targets : array-like of shape (n_targets, n_metrics - 1), default=None
        Frontier targets, drawn as open markers.
    band : float, default=None
        Band width in ``log V``; default ``0.1``.
    ax : matplotlib Axes, default=None

    Returns
    -------
    matplotlib.axes.Axes

    Examples
    --------
    >>> import matplotlib
    >>> matplotlib.use("Agg")
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> ax = plot_frontier_coordinates(
    ...     rng.normal(size=(30, 2)), -rng.exponential(size=30))
    >>> ax.get_ylabel()
    'Z1'
    """
    Z = np.asarray(Z, dtype=float)
    if Z.ndim == 1:
        Z = Z[:, None]
    if Z.shape[1] == 0:
        raise ValueError("a single metric has no frontier coordinates to plot")
    log_v = np.asarray(log_v, dtype=float)
    b = 0.1 if band is None else float(band)
    near = log_v >= -b
    ax = _axes(ax)
    cols, cats = _point_colors(color, len(Z))
    holes = None if holes is None else np.atleast_2d(np.asarray(holes, dtype=float))
    targets = None if targets is None else np.atleast_2d(np.asarray(targets, dtype=float))
    if Z.shape[1] == 1:
        ax.axhspan(-b, 0, color=BAND_COLOR, alpha=0.5, linewidth=0, label="band")
        ax.axhline(0, color=FRONTIER_COLOR, label="frontier V = 1")
        ax.scatter(Z[:, 0], log_v, c=cols, s=14, zorder=3)
        if holes is not None:
            ax.scatter(
                holes[:, 0], np.zeros(len(holes)), c=HOLE_COLOR, marker="|", s=120, label="holes"
            )
        if targets is not None:
            ax.scatter(
                targets[:, 0],
                np.zeros(len(targets)),
                facecolors="none",
                edgecolors=FRONTIER_COLOR,
                s=60,
                label="targets",
            )
        ax.set_ylabel("log V")
    else:
        ax.scatter(
            Z[:, 0],
            Z[:, 1],
            c=cols,
            s=14,
            edgecolors=np.where(near, FRONTIER_COLOR, "none"),
            linewidths=0.8,
            zorder=3,
        )
        if holes is not None:
            ax.scatter(holes[:, 0], holes[:, 1], c=HOLE_COLOR, marker="s", s=14, alpha=0.5)
        if targets is not None:
            ax.scatter(
                targets[:, 0],
                targets[:, 1],
                facecolors="none",
                edgecolors=FRONTIER_COLOR,
                s=60,
                zorder=4,
            )
        ax.set_ylabel("Z1")
    ax.set_xlabel("Z0")
    _category_legend(ax, cats)
    if Z.shape[1] == 1 and cats is None:
        ax.legend(frameon=False)
    return ax


def plot_v_by_variable(values, log_v, color=None, band=None, ax=None, label=None):
    """``log V`` against one covariate, numeric or categorical.

    Parameters
    ----------
    values : array-like of shape (n_samples,)
        A configuration or covariate. Strings or objects are treated as categories (one column
        each, deterministic jitter).
    log_v : array-like of shape (n_samples,)
    color : array-like of shape (n_samples,), default=None
        Optional categories for the points.
    band : float, default=None
        Band width in ``log V``; default ``0.1``.
    ax : matplotlib Axes, default=None
    label : str, default=None
        Horizontal axis label.

    Returns
    -------
    matplotlib.axes.Axes
        The black line is the frontier ``log V = 0``, the grey strip the band.

    Examples
    --------
    >>> import matplotlib
    >>> matplotlib.use("Agg")
    >>> import numpy as np
    >>> ax = plot_v_by_variable(
    ...     np.array(["a", "b", "a"]), np.array([-0.2, -0.1, -0.5]))
    >>> [t.get_text() for t in ax.get_xticklabels()]
    ['a', 'b']
    """
    values = np.asarray(values)
    log_v = np.asarray(log_v, dtype=float)
    b = 0.1 if band is None else float(band)
    ax = _axes(ax)
    ax.axhspan(-b, 0, color=BAND_COLOR, alpha=0.5, linewidth=0)
    ax.axhline(0, color=FRONTIER_COLOR)
    cols, cats = _point_colors(color, len(values))
    if values.dtype.kind in "OUS" or values.dtype.kind == "b":
        levels, codes = np.unique(values.astype(str), return_inverse=True)
        jitter = 0.12 * np.random.default_rng(0).uniform(-1, 1, len(values))
        ax.scatter(codes + jitter, log_v, c=cols, s=14, zorder=3)
        ax.set_xticks(range(len(levels)), [str(v) for v in levels])
    else:
        ax.scatter(values.astype(float), log_v, c=cols, s=14, zorder=3)
    ax.set_xlabel("" if label is None else label)
    ax.set_ylabel("log V")
    _category_legend(ax, cats)
    return ax


_LEMMA_NAMES = {1: "monolemma", 2: "dilemma", 3: "trilemma"}


def _annotation_color(rgba):
    """White or black text, whichever contrasts with the cell colour ``rgba`` (by luminance)."""
    r, g, b = (float(c) for c in rgba[:3])
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "black" if luminance > 0.5 else "white"


def plot_tensions(report, names=None, ax=None):
    """One heatmap per report: a list of reports (one per facet at ``K > 1``) goes side by side.

    Returns the ``Axes`` for a single report and a list of ``Axes`` for a list; ``ax`` is then a
    sequence of axes. See ``_tension_panel`` for what each panel draws.
    """
    if not isinstance(report, (list, tuple)):
        return _tension_panel(report, names, ax)
    axs = ax if ax is not None else _plt().subplots(1, len(report), squeeze=False)[1][0]
    out = [_tension_panel(r, names, a) for r, a in zip(report, axs, strict=True)]
    for k, a in enumerate(out):
        a.set_title(f"facet {k + 1}: {a.get_title()}")
    return out


def _tension_panel(report, names=None, ax=None):
    """Association among near-frontier designs, with exponents and the contending set.

    Draws the association matrix of the log-metrics (negative: tension, positive: aligned) as a
    heatmap in ``TENSION_CMAP``. Tick labels carry each metric's frontier exponent; metrics that
    do not participate are labelled in grey; the contending set (the metrics that define the
    ``n``-lemma) is outlined in black on the diagonal.

    Parameters
    ----------
    report : TensionReport
        From ``hyperbolic_trade_space.tensions.tension_report``. Only these attributes are
        used: ``participating`` (bool per metric), ``exponents`` (per metric), ``association``
        (``d x d``), ``contending_set`` (metric indices), ``n_lemma`` (int). The principal
        ``tension_directions`` and ``tension_loadings`` are reported numerically and not drawn.
    names : sequence of str, default=None
        Metric names; default ``m0, m1, ...``.
    ax : matplotlib Axes, default=None

    Returns
    -------
    matplotlib.axes.Axes

    Examples
    --------
    >>> import matplotlib
    >>> matplotlib.use("Agg")
    >>> import numpy as np
    >>> from types import SimpleNamespace
    >>> r = SimpleNamespace(participating=np.array([True, True, False]),
    ...     exponents=np.array([0.5, 0.5, 0.0]),
    ...     association=np.array([[1, -0.6, 0.1], [-0.6, 1, 0.0], [0.1, 0.0, 1]]),
    ...     contending_set=np.array([0, 1]), n_lemma=2)
    >>> plot_tensions(r, names=["mass", "power", "cost"]).get_title()
    'dilemma (2 metrics contend)'
    """
    A = np.asarray(report.association, dtype=float)
    w = np.asarray(report.exponents, dtype=float)
    part = np.asarray(report.participating, dtype=bool)
    d = A.shape[0]
    names = [f"m{j}" for j in range(d)] if names is None else [str(n) for n in names]
    ax = _axes(ax)
    im = ax.imshow(A, cmap=TENSION_CMAP, vmin=-1.0, vmax=1.0)
    ax.figure.colorbar(im, ax=ax, label="association (negative = tension)")
    for i in range(d):
        for j in range(d):
            ax.text(
                j,
                i,
                f"{A[i, j]:.2f}",
                ha="center",
                va="center",
                fontsize=8,
                color=_annotation_color(im.cmap(im.norm(A[i, j]))),
            )
    labels = [f"{names[j]}\nw={w[j]:.2f}" for j in range(d)]
    ax.set_xticks(range(d), labels)
    ax.set_yticks(range(d), labels)
    for tick_set in (ax.get_xticklabels(), ax.get_yticklabels()):
        for tick, p in zip(tick_set, part, strict=True):
            tick.set_color(FRONTIER_COLOR if p else BAND_COLOR)
    from matplotlib.patches import Rectangle

    for j in np.atleast_1d(report.contending_set):
        ax.add_patch(
            Rectangle((j - 0.5, j - 0.5), 1, 1, fill=False, edgecolor=FRONTIER_COLOR, linewidth=2)
        )
    n = int(report.n_lemma)
    ax.set_title(f"{_LEMMA_NAMES.get(n, f'{n}-lemma')} ({n} metric{'s' if n != 1 else ''} contend)")
    return ax
