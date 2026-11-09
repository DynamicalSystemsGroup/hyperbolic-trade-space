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
* **Ternary plot** (``plot_ternary``): the shares of a total among three metrics (or three groups
  of metrics) as a triangle; a facet's exponent vector is a marker (its own shape, numbered), the
  regions are tinted by the facet that dominates, and the facets use the palette's colours.
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
    "plot_ternary",
    "plot_v_by_variable",
    "ternary_marker_values",
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


# ---- the ternary plot -------------------------------------------------------------------------

_SQ3 = np.sqrt(3.0) / 2.0
_TERN_BIG = 0.12  # an exponent above this makes its metric part of the trade-off a facet names
_TERN_FIGSIZE = (6.4, 6.1)  # inches, when the function makes the figure
_TERN_REF = 7.0 * 1.08 / 1.07  # axes width (in) at which the label sizes below are stated
_TERN_LABEL_SIZES = (15.0, 14.5, 14.0)  # points at the reference width; the largest that fits
_TERN_LABEL_MARGIN = 0.004  # clear space, in plane units, between a label's box and any border
_TERN_MARKERS = (("*", 420), ("D", 150), ("s", 170), ("^", 200), ("v", 200), ("P", 190))
_TERN_LEVELS = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.97)  # equal-V lines, as fractions of the peak
_TERN_BLUE, _TERN_AMBER, _TERN_GREEN = CATEGORY_COLORS[:3]
_TERN_SCHEMES = {
    "light": {"ink": "#1a1a1a", "plate": "#ffffff", "dots": "#7d7d7d", "mix": ("#ffffff", 0.80)},
    "dark": {"ink": "#e8e6e1", "plate": "#221f1e", "dots": "#a5a19a", "mix": ("#191817", 0.62)},
}


def _ternary_project(top, left, right):
    """Barycentric (top, left, right) to plane coordinates; the corner of ``top`` is up."""
    top, right = np.asarray(top, float), np.asarray(right, float)
    return right + top / 2.0, _SQ3 * top


def _hex(h):
    return np.array([int(h[i : i + 2], 16) for i in (1, 3, 5)]) / 255.0


def _close(x):
    x = np.asarray(x, float)
    return x / x.sum(axis=-1, keepdims=True)


def _ternary_scheme(scheme):
    """``"light"`` or ``"dark"``; ``"auto"`` reads the label colour of the active style."""
    if scheme in _TERN_SCHEMES:
        return scheme
    if scheme != "auto":
        raise ValueError(f"scheme must be 'light', 'dark' or 'auto', got {scheme!r}")
    import matplotlib.colors as mc

    r, g, b = mc.to_rgb(_plt().rcParams["axes.labelcolor"])
    return "dark" if 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.5 else "light"


def _ternary_says(w, names):
    """The trade-off a facet with exponent vector ``w`` names, in words, read from its exponents."""
    big = [j for j in np.argsort(-w) if w[j] > _TERN_BIG]
    if len(big) >= len(w):
        return "all three trade"
    if len(big) < 2:
        return f"{names[int(np.argmax(w))]} alone"
    return f"{names[big[0]]} trades\nagainst {names[big[1]]}"


def _ternary_colours(W):
    """Facet colours: a facet that trades all three metrics is amber, the others blue, green, ..."""
    W = np.atleast_2d(W)
    rest = iter(c for c in CATEGORY_COLORS if c != _TERN_AMBER)
    tri = int(np.argmax(W.min(axis=1)))
    tri = tri if W[tri].min() > _TERN_BIG else -1
    return {k: (_TERN_AMBER if k == tri else next(rest)) for k in range(len(W))}


def _ternary_geometry(estimator, X):
    """What the triangle needs of a fit and its table: metrics' logs, typical sizes, spread."""
    W, beta = _fitted_chart(estimator, 3)
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or X.shape[1] != 3 or (X <= 0).any():
        raise ValueError("X must be a table of three strictly positive metrics")
    U = np.log(X)
    P = U - U.mean(axis=1, keepdims=True)  # position: the level direction removed
    colmean = P.mean(axis=0)  # log of each metric's typical size, up to a common factor
    return {
        "U": U,
        "colmean": colmean,
        "spread": float(2.0 * (P - colmean).std()),
        "W": W,
        "beta": beta,
    }


def _ternary_shares(fit, s):
    """Each design as shares c_j = (m_j / typical_j)^(1/s) / L, L their sum (s = 1: plain sum)."""
    return _close(np.exp((fit["U"] - fit["colmean"]) / s))


def _ternary_region_of(fit, s, top, left, right):
    """The binding facet at barycentric positions: argmax_k a_k + s * sum_j w_kj log c_j."""
    W = fit["W"]
    a = W @ fit["colmean"] - fit["beta"]
    c = np.stack([top, left, right], axis=-1)
    with np.errstate(divide="ignore"):
        g = a + s * (np.log(np.clip(c, 1e-300, None)) @ W.T)
    return g.argmax(axis=-1), g


def _ternary_grid(n):
    """Plane grid of the triangle: x, y, barycentric (top, left, right), and the inside mask."""
    x, y = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, _SQ3, int(n * _SQ3)))
    top = y / _SQ3
    right = x - top / 2.0
    left = 1.0 - top - right
    inside = (top > 1e-3) & (left > 1e-3) & (right > 1e-3)
    return x, y, top, left, right, inside


def _ternary_regions(fit, s, n=500):
    """The regions on a grid of the triangle: (barycentric points, region index per point)."""
    _, _, top, left, right, inside = _ternary_grid(n)
    t, lf, r = top[inside], left[inside], right[inside]
    return np.column_stack([t, lf, r]), _ternary_region_of(fit, s, t, lf, r)[0]


def _ternary_peak(fit, s):
    """The highest of the facets' own peaks (log V less the level), at their exponent vectors."""
    W = fit["W"]
    a = W @ fit["colmean"] - fit["beta"]
    logw = np.log(np.clip(W, 1e-300, None))
    peak = a + s * (logw * W).sum(axis=1)
    own = [int(np.argmax(a + s * (logw[k] @ W.T))) for k in range(len(W))]
    own_peaks = [peak[k] for k in range(len(W)) if own[k] == k]
    return float(max(own_peaks)) if own_peaks else float((a[None] + s * logw @ W.T).max())


def _ternary_marker_logv(fit, s):
    """log V (less the level) of the fit at each facet's exponent vector, in the lines' units:
    the same ``g`` the regions and lines are drawn from, evaluated at the marker positions."""
    W = fit["W"]
    a = W @ fit["colmean"] - fit["beta"]
    logw = np.log(np.clip(W, 1e-300, None))
    return (a[None] + s * logw @ W.T).max(axis=1)


def _ternary_marker_fractions(fit, s):
    """V at each marker as a fraction of the highest marker's V (one total; the total cancels)."""
    return np.exp(_ternary_marker_logv(fit, s) - _ternary_peak(fit, s))


def _ternary_wraps(text, names):
    """The label's own wrap, then the same words on one to four lines (a name is a unit)."""
    import re

    pattern = "|".join([re.escape(n) for n in sorted(names, key=len, reverse=True)] + [r"\S+"])
    units = re.findall(pattern, text.replace("\n", " "))
    out = [text]
    for lines in (2, 3, 4, 1):
        per = -(-len(units) // lines)
        alt = "\n".join(" ".join(units[i : i + per]) for i in range(0, len(units), per))
        if alt not in out:
            out.append(alt)
    return out


def _ternary_box(ax, text, size, ink, plate, edge):
    """A label drawn at the origin; returns the text artist and its box half-extents (plane units),
    read from the renderer (the bounding box includes the round box around the words)."""
    t = ax.text(
        0,
        0,
        text,
        ha="center",
        va="center",
        fontsize=size,
        fontweight="bold",
        color=ink,
        bbox={"boxstyle": "round,pad=0.3", "fc": plate, "ec": edge, "lw": 2.0},
        zorder=6,
    )
    ax.figure.canvas.draw()
    bb = t.get_bbox_patch().get_window_extent(ax.figure.canvas.get_renderer())
    (x0, y0), (x1, y1) = ax.transData.inverted().transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
    return t, (x1 - x0) / 2.0, (y1 - y0) / 2.0


def _ternary_labels(fit, comp, s, ax, ink, plate, col, names, scale=1.0):
    """Draw each facet's label inside its own region and return ``{facet: text artist}``.

    The rule reads the fit. On a fine grid of the triangle the region of facet k is where
    ``k = argmax_k w_k . p - beta_k``. A label's box (its extent as the renderer measures it, in
    plane units, plus a margin) is placed only where it lies wholly in its region, so it crosses
    neither a border with another region nor an edge of the triangle: the feasible centres are the
    region's grid points eroded by the box. Of those the chosen one maximises the distance to the
    region's border less the local density of designs (a Gaussian-smoothed count, bandwidth 0.04;
    the distance counts a quarter as much).
    The largest of the label sizes that has a feasible centre is used, with the wrap (the same
    words on one to four lines) whose best centre scores highest. Nothing in the rule depends on
    the colour scheme, so the light and dark images get the same placement.
    """
    from scipy import ndimage

    n = 500
    x, y, top, left, right, inside = _ternary_grid(n)
    reg = np.full(top.shape, -1, int)
    reg[inside] = _ternary_region_of(fit, s, top[inside], left[inside], right[inside])[0]
    dx = x[0, 1] - x[0, 0]
    dy = y[1, 0] - y[0, 0]
    px, py = _ternary_project(comp[:, 0], comp[:, 1], comp[:, 2])
    hist, _, _ = np.histogram2d(
        py,
        px,
        bins=[y.shape[0], x.shape[1]],
        range=[[-dy / 2, _SQ3 + dy / 2], [-dx / 2, 1 + dx / 2]],
    )
    density = ndimage.gaussian_filter(hist, sigma=0.04 / dx)
    density /= density.max()
    out = {}
    for k in range(len(fit["W"])):
        mask = reg == k
        if not mask.any():
            continue
        dist = ndimage.distance_transform_edt(mask) * dx
        text = _ternary_says(fit["W"][k], names)
        for size in _TERN_LABEL_SIZES:
            best = None
            for variant in _ternary_wraps(text, names):
                t, hw, hh = _ternary_box(ax, variant, size * scale, ink, plate, col[k])
                nx = int(np.ceil((hw + _TERN_LABEL_MARGIN) / dx))
                ny = int(np.ceil((hh + _TERN_LABEL_MARGIN) / dy))
                ok = ndimage.binary_erosion(mask, structure=np.ones((2 * ny + 1, 2 * nx + 1), bool))
                score = np.where(ok, 0.25 * dist / dist.max() - density, -np.inf)
                i, j = np.unravel_index(np.argmax(score), score.shape)
                if ok.any() and (best is None or score[i, j] > best[0]):
                    if best is not None:
                        best[1].remove()
                    best = (score[i, j], t, (x[i, j], y[i, j]))
                else:
                    t.remove()
            if best is not None:  # the best wrap at the largest size that fits
                best[1].set_position(best[2])
                best[1].set_gid(f"ternary-label-{k}")
                out[k] = best[1]
                break
        else:
            raise RuntimeError(f"no room for the label of facet {k} inside its region")
    return out


def _ternary_parts(W, names, groups):
    """Corner names and the exponents on them: the metrics themselves (``d = 3``) or, with
    ``groups``, each facet's exponents summed within three groups (exact: exponents add)."""
    d = W.shape[1]
    names = [f"metric {j + 1}" for j in range(d)] if names is None else [str(n) for n in names]
    if len(names) != d:
        raise ValueError(f"names has {len(names)} entries; the estimator has {d} metrics")
    if groups is None:
        if d != 3:
            raise ValueError(f"a ternary plot needs 3 metrics, got {d}; pass groups= for more")
        return names, W
    if len(groups) != 3:
        raise ValueError(f"groups must have three entries, got {len(groups)}")
    members = [
        [names.index(m) if isinstance(m, str) else int(m) for m in g] for g in groups.values()
    ]
    flat = sorted(j for g in members for j in g)
    if flat != list(range(d)):
        raise ValueError("groups must put every metric in exactly one group")
    return list(groups), np.column_stack([W[:, g].sum(axis=1) for g in members])


def ternary_marker_values(estimator, X, names=None):
    """The values attained at the numbered markers of ``plot_ternary(..., lines=True)``.

    One row per marker: its shape and number, the facet's exponent vector (the shares of the total
    at which the marker sits, one column per metric) and the value of V attained there, in the
    units of the equal-V lines: a fraction of the highest marker's value, so that row reads 1.00.
    It is computed by the code that draws the lines and the markers.

    Parameters
    ----------
    estimator : HyperbolicTradeSpace
        A fitted estimator with three metrics.
    X : array-like of shape (n_samples, 3)
        The table of strictly positive metrics the plot is drawn with (the fitted table).
    names : sequence of str, default=None
        One name per metric, for the share columns. Default ``"metric 1"``, ``"metric 2"``,
        ``"metric 3"``.

    Returns
    -------
    pandas.DataFrame
        Columns ``marker`` (Matplotlib shape code), ``number`` (the numeral drawn beside it),
        ``share of <name>`` for each metric and ``V`` (fraction of the highest marker's V).
        ``df.attrs["levels"]`` holds the fractions at which the equal-V lines are drawn.

    Notes
    -----
    *Total.* A position of the lines plot is a set of shares of a total: the sum of the three
    metrics, each in units of its typical size (its geometric mean over ``X``, up to a factor
    common to all three). The lines plot spreads nothing by a power (that is only done without
    ``lines``, to fill the triangle with the designs): the shares are plain shares. V scales with
    the total S as ``log V = log S + g(c)``, so at any one fixed total the ratios of V between
    positions are those of ``exp g``, and a fraction of the highest marker's V does not depend on
    the total chosen.

    Examples
    --------
    >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
    >>> from hyperbolic_trade_space.plotting import ternary_marker_values
    >>> X, _ = make_frontier_data(300, 3, n_terms=3, random_state=11)
    >>> ts = HyperbolicTradeSpace(n_terms=3, temperature=50.0, random_state=0).fit(X)
    >>> table = ternary_marker_values(ts, X)
    >>> list(table["number"])
    [1, 2, 3]
    >>> float(table["V"].max())
    1.0
    >>> table.attrs["levels"][0], table.attrs["levels"][-1]
    (0.3, 0.97)
    """
    import pandas as pd

    W, _ = _fitted_chart(estimator, 3)
    names = _ternary_parts(W, names, None)[0]
    fit = _ternary_geometry(estimator, X)
    frac = _ternary_marker_fractions(fit, 1.0)
    table = pd.DataFrame(
        {
            "marker": [_TERN_MARKERS[k % len(_TERN_MARKERS)][0] for k in range(len(W))],
            "number": np.arange(1, len(W) + 1),
            **{f"share of {n}": W[:, j] for j, n in enumerate(names)},
            "V": frac,
        }
    )
    table.attrs["levels"] = list(_TERN_LEVELS)
    return table


def plot_ternary(
    estimator, X=None, names=None, groups=None, lines=False, near=0.2, ax=None, scheme="auto"
):
    """Shares of a total among three metrics, as a triangle: where the facets dominate and peak.

    A position in the triangle is a set of shares of a total among three metrics (the corner of a
    metric is all the total in that metric). Each facet's exponent vector sums to one, so it is a
    point of the triangle (a numbered marker of its own shape), and it is where that facet's V is
    largest at a fixed total. With the table ``X`` the triangle is tinted by region, the facet
    that dominates there, and the designs are points. A region is an analysis of the fit, not a
    label on a design. V also depends on the total, so a marker is not where V = 1.

    Parameters
    ----------
    estimator : HyperbolicTradeSpace
        A fitted estimator with three metrics, or with more when ``groups`` is given.
    X : array-like of shape (n_samples, 3), default=None
        The table of strictly positive metrics (the fitted table). When given, the triangle is
        tinted by region, each region is named in words read from the exponents, and the designs
        are drawn: those within ``near`` of the frontier in their facet's colour, the rest grey.
        Without it only the exponent markers are drawn.
    names : sequence of str, default=None
        One name per metric of the estimator: the corners (``d = 3``) or the members of
        ``groups``. Default ``"metric 1"``, ``"metric 2"``, ``"metric 3"``.
    groups : dict, default=None
        Three groups as ``{group name: members}``, members being metric names (from ``names``) or
        column indices, together using every metric once. Each facet's exponents are summed within
        the group, which is exact, so the triangle shows where the facet's weight lies. The
        grouping is the analyst's choice. Not combined with ``X`` or ``lines``.
    lines : bool, default=False
        Overlay lines of equal V at a fixed total (at 0.97 down to 0.3 of the highest peak) and
        the exponent markers. The shares are then plain shares of the total; without ``lines``
        they are spread by a power so that the designs fill the triangle.
    near : float, default=0.2
        Designs with ``|log V| < near`` are drawn in their facet's colour.
    ax : matplotlib.axes.Axes, default=None
        Axes to draw in; a new figure is made when ``None``. The axes are switched off and given
        equal aspect.
    scheme : {"auto", "light", "dark"}, default="auto"
        The ink and tints. ``"auto"`` follows the label colour of the active Matplotlib style.

    Returns
    -------
    matplotlib.axes.Axes
        The artists carry ids: ``ternary-star-k`` (the marker of facet k), ``ternary-star-label-k``
        and, with ``X``, ``ternary-label-k`` (the region's words).

    See Also
    --------
    ternary_marker_values : the values attained at the numbered markers, as a table.

    Notes
    -----
    The barycentric projection is ``x = right + top / 2``, ``y = sqrt(3) / 2 * top``. With the
    typical size of a metric divided out and S the sum of the three, ``log V = log S + max_k
    (a_k + sum_j w_kj log c_j)`` for shares ``c``, so at a fixed total facet k peaks at ``c = w_k``.

    Examples
    --------
    >>> import matplotlib
    >>> matplotlib.use("Agg")
    >>> import numpy as np
    >>> from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data
    >>> from hyperbolic_trade_space.plotting import plot_ternary
    >>> X, _ = make_frontier_data(300, 3, n_terms=3, random_state=11)
    >>> ts = HyperbolicTradeSpace(n_terms=3, temperature=50.0, random_state=0).fit(X)
    >>> ax = plot_ternary(ts, X, lines=True)
    >>> star = ax.findobj(lambda a: a.get_gid() == "ternary-star-0")[0]
    >>> bool(np.allclose(star.get_offsets()[0], _ternary_project(*ts.exponents_[0][[0, 1, 2]])))
    True
    >>> bool(np.allclose(ts.exponents_.sum(axis=1), 1.0))
    True
    """
    W, _ = _fitted_chart(estimator)
    names, Wt = _ternary_parts(W, names, groups)
    if groups is not None and (X is not None or lines):
        raise ValueError("groups= draws the exponent markers only; omit X and lines")
    if lines and X is None:
        raise ValueError("lines= needs the table X")
    sch = _TERN_SCHEMES[_ternary_scheme(scheme)]
    ink = sch["ink"]
    col = _ternary_colours(Wt)
    K = len(Wt)

    if ax is None:
        ax = _plt().figure(figsize=_TERN_FIGSIZE).add_axes([0.0, 0.0, 1.0, 1.0])
    lims = {"xlim": (-0.04, 1.04), "ylim": (-0.13, _SQ3 + 0.075)}
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.set(**lims)
    ax.patch.set_alpha(0.0)
    ax.apply_aspect()
    scale = np.clip(round(ax.get_window_extent().width / ax.figure.dpi / _TERN_REF, 2), 0.4, 1.5)

    if X is not None:
        fit = _ternary_geometry(estimator, X)
        s = 1.0 if lines else fit["spread"]
        comp = _ternary_shares(fit, s)
        logv = np.asarray(estimator.score_samples(np.asarray(X, float)), float)
        facet = np.asarray(estimator.assign_facets(np.asarray(X, float)))
        near_mask = np.abs(logv) < near
        x, y, top, left, right, inside = _ternary_grid(900)
        g, f = np.zeros(top.shape, int), np.full(top.shape, np.nan)
        reg, gv = _ternary_region_of(fit, s, top[inside], left[inside], right[inside])
        g[inside], f[inside] = reg, gv.max(axis=-1)
        mix, frac = sch["mix"]
        rgba = np.zeros((*top.shape, 4))
        for k in range(K):
            rgba[g == k, :3] = frac * _hex(mix) + (1 - frac) * _hex(col[k])
        rgba[..., 3] = inside.astype(float)
        ax.imshow(
            rgba,
            extent=(0, 1, 0, _SQ3),
            origin="lower",
            interpolation="nearest",
            zorder=0,
            aspect="equal",
        )
        ax.set(**lims)
        px, py = _ternary_project(comp[:, 0], comp[:, 1], comp[:, 2])
        ax.scatter(
            px[~near_mask],
            py[~near_mask],
            s=7,
            color=sch["dots"],
            alpha=0.55,
            linewidths=0,
            zorder=2,
        )
        for k in range(K):
            mk = near_mask & (facet == k)
            ax.scatter(
                px[mk],
                py[mk],
                s=30,
                color=col[k],
                linewidths=0.6,
                edgecolors=sch["plate"],
                zorder=3,
            )
        if lines:
            ratios = np.array(_TERN_LEVELS)
            ax.contour(
                x,
                y,
                f - _ternary_peak(fit, s),
                levels=np.log(ratios),
                colors=[ink],
                linewidths=1.0,
                linestyles="solid",
                zorder=4,
            )

    if lines or X is None:  # the exponent vectors, each a numbered marker of its own shape
        for k in range(K):
            marker, size = _TERN_MARKERS[k % len(_TERN_MARKERS)]
            sx, sy = _ternary_project(*Wt[k])
            star = ax.scatter(
                [sx],
                [sy],
                marker=marker,
                s=size * scale**2,
                color=col[k],
                edgecolors=ink,
                linewidths=1.4,
                zorder=8,
                clip_on=False,
            )
            star.set_gid(f"ternary-star-{k}")
            dx, dy = 0.5 - sx, _SQ3 / 3.0 - sy  # the number sits toward the middle of the triangle
            norm = float(np.hypot(dx, dy)) or 1.0
            lab = ax.text(
                sx + 0.05 * dx / norm,
                sy + 0.05 * dy / norm,
                str(k + 1),
                ha="center",
                va="center",
                fontsize=13 * scale,
                fontweight="bold",
                color=ink,
                bbox={"boxstyle": "round,pad=0.2", "fc": sch["plate"], "ec": col[k], "lw": 1.6},
                zorder=9,
            )
            lab.set_gid(f"ternary-star-label-{k}")

    ax.plot([0, 0.5, 1, 0], [0, _SQ3, 0, 0], color=ink, lw=1.4, solid_joinstyle="miter", zorder=5)
    if X is not None:
        _ternary_labels(fit, comp, s, ax, ink, sch["plate"], col, names, scale)
    corner = {"fontsize": 15 * scale, "fontweight": "bold", "color": ink, "zorder": 6}
    ax.text(0.5, _SQ3 + 0.035, f"favours {names[0]}", ha="center", va="bottom", **corner)
    ax.text(-0.03, -0.03, f"favours\n{names[1]}", ha="left", va="top", **corner)
    ax.text(1.03, -0.03, f"favours\n{names[2]}", ha="right", va="top", **corner)
    return ax
