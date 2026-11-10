"""The case module: every computation the paper shows is one call into this file.

The module takes a *table of designs* (configurations and their evaluated attributes) through the
whole analysis: load, feasibility, conditioning, temperature selection and fit at K = 1, the K sweep
with the certificate columns, the tension report, the regime comparison, nondominated counts,
candidate designs and propose-predict-check. Everything specific to the cubesat is **data**: the
:class:`CaseSpec` named :data:`CUBESAT` lists the regimes and their files, the attributes with
names, units and orientations, the covariates and design variables, the feasibility flag columns,
the named attribute views and the check files. Another table runs through the same functions by
passing another :class:`CaseSpec` (``dataclasses.replace(CUBESAT, ...)`` or a new instance).

Functions are pure: importing the module does no work, nothing is written to disk, every random
choice has an explicit seed, and the figure helpers return matplotlib ``Figure`` objects. Nothing
is simulated; the evaluation of a configuration into attributes is the data.

The heavy libraries are imported when a function first needs them, so ``import case`` is fast.
Name-free helpers are taken from ``k_terms`` (the WP9 record script) rather than duplicated.

Examples
--------
>>> study = load_study("primary", n_max=60)
>>> study.M.shape
(60, 9)
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, NamedTuple

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class CaseSpec:
    """Everything about a table that the analysis needs to know, as data.

    Parameters
    ----------
    name : str
        Case label.
    data_dir : pathlib.Path
        Directory of the CSV files.
    regimes : dict of str to str
        Regime name to CSV file name; the first regime is the primary one.
    attributes : tuple of str
        Attribute columns, strictly positive where feasible.
    short, units : dict of str to str
        Plain name and unit of each attribute.
    orientation : dict of str to int
        ``-1`` if smaller is better (reciprocal), ``+1`` if larger is better.
    covariates : dict of str to tuple of str
        Ordinal covariate columns with their ordered levels (the first is the colour category).
    design_vars : tuple of str
        Numeric configuration columns.
    flags : tuple of str
        Boolean feasibility columns; feasible means all hold and every attribute is positive.
    views : dict of str to tuple of str
        Named attribute subsets (nondominated counts, the four-metric view).
    view : str
        The view the propose-predict-check procedure uses.
    association_pairs : tuple of (str, str)
        Metric pairs (short names) reported in the regime comparison.
    checks_file, predictions_file : str
        Measured check designs and recorded predictions (``role`` column: candidate or proposal).
    ranges : dict of str to (float, float)
        Design-variable ranges, used to scale the regressor features.
    target_frac : float
        Target fraction of designs above V = 1 for the temperature selection.
    tau_bounds : (float, float)
        Bracket of the temperature selection.
    seed : int
        Seed of every fit.
    subsystems : dict of str to str
        Subsystem of each attribute (the model's own grouping: controls, power and energy, mass);
        the single source of every sentence that says which subsystems a set of metrics spans.
    subsystem_order : tuple of str
        The order in which subsystems are listed in a sentence.
    """

    name: str
    data_dir: Path
    regimes: dict
    attributes: tuple
    short: dict
    units: dict
    orientation: dict
    covariates: dict = field(default_factory=dict)
    design_vars: tuple = ()
    flags: tuple = ()
    views: dict = field(default_factory=dict)
    view: str = ""
    association_pairs: tuple = ()
    checks_file: str = ""
    predictions_file: str = ""
    ranges: dict = field(default_factory=dict)
    target_frac: float = 0.10
    tau_bounds: tuple = (3.0, 1e3)
    seed: int = 0
    subsystems: dict = field(default_factory=dict)
    subsystem_order: tuple = ()

    @property
    def names(self):
        """Plain names of the attributes, in column order."""
        return [self.short[a] for a in self.attributes]

    @property
    def category(self):
        """The first covariate (the colour category), or None."""
        return next(iter(self.covariates), None)

    def subsystems_of(self, names) -> list:
        """Subsystems spanned by plain-named metrics, in the order of ``subsystem_order``.

        Parameters
        ----------
        names : iterable of str
            Plain names of attributes (the values of ``short``).

        Returns
        -------
        list of str
            Distinct subsystems of ``names``.
        """
        by_name = {self.short[a]: self.subsystems[a] for a in self.attributes}
        wanted = {by_name[n] for n in names}
        order = self.subsystem_order or tuple(dict.fromkeys(by_name.values()))
        return [g for g in order if g in wanted]


_ATTRS = (
    "settling_time_s", "pointing_error_deg", "total_mass_kg", "control_effort",
    "power_margin_w", "energy_balance_wh", "eclipse_reserve_wh", "peak_slew_power_w", "dod_eclipse",
)  # fmt: skip
_NAMES = (
    "settling time", "pointing error", "total mass", "control effort",
    "power margin", "energy balance", "eclipse reserve", "peak slew power", "depth of discharge",
)  # fmt: skip
_SUBSYSTEMS = (
    "controls", "controls", "mass", "controls",
    "power and energy", "power and energy", "power and energy", "power and energy",
    "power and energy",
)  # fmt: skip
_UNITS = ("s", "deg", "kg", "torque.s, proxy", "W", "Wh", "Wh", "W", "fraction")
_ORIENT = (-1, -1, -1, -1, +1, +1, +1, -1, -1)

CUBESAT = CaseSpec(
    name="cubesat attitude determination and control",
    data_dir=HERE / "data" / "v2",  # the data of record (ledger entries @5, WP23)
    regimes={"primary": "adcs_designs_cubesat_gains.csv", "stock": "adcs_designs_cubesat.csv"},
    attributes=_ATTRS,
    short=dict(zip(_ATTRS, _NAMES, strict=True)),
    units=dict(zip(_ATTRS, _UNITS, strict=True)),
    orientation=dict(zip(_ATTRS, _ORIENT, strict=True)),
    covariates={
        "wheel_class": ("small", "medium", "large"),
        "st_grade": ("coarse", "medium", "fine"),
    },
    design_vars=("panel_span_m", "battery_wh", "Kp", "Kd"),
    flags=("settled", "power_ok", "momentum_ok"),
    views={
        "four metrics": (
            "settling_time_s",
            "pointing_error_deg",
            "control_effort",
            "total_mass_kg",
        ),
    },
    view="four metrics",
    association_pairs=(
        ("settling time", "total mass"),
        ("pointing error", "control effort"),
        ("settling time", "pointing error"),
    ),
    checks_file="check_designs_cubesat.csv",
    predictions_file="check_predictions_cubesat.csv",
    subsystems=dict(zip(_ATTRS, _SUBSYSTEMS, strict=True)),
    subsystem_order=("controls", "power and energy", "mass"),
    ranges={
        "panel_span_m": (0.3, 1.0),
        "battery_wh": (20.0, 200.0),
        "Kp": (0.2, 2.0),
        "Kd": (0.3, 1.5),
    },
)


@dataclass
class Study:
    """A loaded table of one regime, ready for fitting.

    Attributes
    ----------
    spec : CaseSpec
    regime : str
    raw : pandas.DataFrame
        The CSV as read.
    feasible : pandas.DataFrame
        The feasible rows, re-indexed.
    attrs : tuple of str
        The attributes the metrics were built from (the spec's, or a view's).
    M : numpy.ndarray
        Conditioned metrics (strictly positive, larger is better), one column per attribute.
    conditioner : sklearn.compose.ColumnTransformer
        The fitted conditioning transformer (metrics, covariate codes, design variables).
    """

    spec: CaseSpec
    regime: str
    raw: pd.DataFrame
    feasible: pd.DataFrame
    attrs: tuple
    M: np.ndarray
    conditioner: Any

    @property
    def names(self):
        """Plain names of the study's attributes."""
        return [self.spec.short[a] for a in self.attrs]

    @property
    def preconditioner(self):
        """The fitted LogAffinePreconditioner inside the conditioner."""
        return self.conditioner.named_transformers_["metrics"]


class Fit(NamedTuple):
    """A selected temperature and the fitted K-term estimator."""

    tau: float
    estimator: Any
    K: int

    @property
    def band(self):
        """Near-frontier band 1 / tau."""
        return 1.0 / self.tau


def _lib():
    """The heavy imports, taken when first needed."""
    import k_terms

    import hyperbolic_trade_space as hts
    from hyperbolic_trade_space import plotting

    return hts, k_terms, plotting


def _plt():
    import matplotlib.pyplot as plt

    return plt


FIGURE_WIDTH_IN = 8.0
"""Width of every figure in inches; at ``FIGURE_DPI`` it is 800 px, under the 842 px figure column
of the site at 1280 px, so a figure is shown at its natural size and not scaled down."""
FIGURE_DPI = 100
FIGURE_MIN_FONT_PT = 9.0
"""The smallest type in any figure: 9 pt at 100 dpi is 12.5 px, the body's small print."""


def _legible(fn):
    """Draw the figure with every text at least ``FIGURE_MIN_FONT_PT``, at ``FIGURE_DPI``.

    The panels of a figure are laid out one per row by the function itself; this decorator sets the
    type sizes of the drawing, raises any smaller text (the package's annotations) to the floor,
    lays the figure out again and checks that no text is below it.
    """
    import functools

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        from matplotlib.text import Text

        plt = _plt()
        size = FIGURE_MIN_FONT_PT
        rc = {"font.size": size, "axes.titlesize": size, "axes.labelsize": size,
              "xtick.labelsize": size, "ytick.labelsize": size, "legend.fontsize": size,
              "figure.dpi": FIGURE_DPI}  # fmt: skip
        with plt.rc_context(rc):
            fig = fn(*args, **kwargs)
            fig.canvas.draw()
            for _ in range(2):
                for t in fig.findobj(Text):
                    if t.get_text().strip() and t.get_fontsize() < size:
                        t.set_fontsize(size)
                fig.tight_layout()
                fig.canvas.draw()
            small = [t.get_text() for t in fig.findobj(Text)
                     if t.get_text().strip() and t.get_fontsize() < size]  # fmt: skip
            assert not small, f"text below {size} pt in {fn.__name__}: {small[:3]}"
        return fig

    return wrapper


def _wrap(text, width=48):
    """A long axis label on several lines."""
    import textwrap

    return "\n".join(textwrap.wrap(text, width))


def feasible_mask(raw, spec=CUBESAT):
    """Boolean mask of the feasible rows: every flag holds and every attribute is positive.

    Parameters
    ----------
    raw : pandas.DataFrame
    spec : CaseSpec

    Returns
    -------
    pandas.Series of bool
    """
    ok = pd.Series(True, index=raw.index)
    for f in spec.flags:
        ok &= raw[f].astype(bool)
    return ok & (raw[list(spec.attributes)] > 0).all(axis=1)


def conditioner_for(attrs, spec=CUBESAT, scaler="standard"):
    """The ColumnTransformer: attributes to metrics, covariates to codes, design variables through.

    Parameters
    ----------
    attrs : sequence of str
    spec : CaseSpec
    scaler : {"standard", "robust"}, default "standard"
        The log-space scaler of the conditioning (unit log standard deviation or unit log IQR).

    Returns
    -------
    sklearn.compose.ColumnTransformer
        Unfitted, with pandas output.
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OrdinalEncoder

    from hyperbolic_trade_space import LogAffinePreconditioner

    parts = [
        (
            "metrics",
            LogAffinePreconditioner(
                orientation=[spec.orientation[a] for a in attrs], scaler=scaler
            ),
            list(attrs),
        )
    ]
    if spec.covariates:
        parts.append(
            (
                "covariates",
                OrdinalEncoder(categories=[list(v) for v in spec.covariates.values()]),
                list(spec.covariates),
            )
        )
    if spec.design_vars:
        parts.append(("design", "passthrough", list(spec.design_vars)))
    return ColumnTransformer(parts, verbose_feature_names_out=True).set_output(transform="pandas")


def _condition(feasible, attrs, spec, scaler="standard"):
    cond = conditioner_for(attrs, spec, scaler)
    table = cond.fit_transform(feasible)
    return cond, table[[f"metrics__{a}" for a in attrs]].to_numpy()


def load_study(regime="primary", spec=CUBESAT, n_max=None):
    """Read a regime's table, filter to the feasible designs and condition them.

    Parameters
    ----------
    regime : str
        A key of ``spec.regimes``.
    spec : CaseSpec
    n_max : int, optional
        Keep only the first ``n_max`` feasible designs (small samples for tests).

    Returns
    -------
    Study
    """
    raw = pd.read_csv(Path(spec.data_dir) / spec.regimes[regime])
    feasible = raw[feasible_mask(raw, spec)].reset_index(drop=True)
    if n_max:
        feasible = feasible.iloc[:n_max].reset_index(drop=True)
    cond, M = _condition(feasible, spec.attributes, spec)
    return Study(spec, regime, raw, feasible, tuple(spec.attributes), M, cond)


def view_study(study, view=None):
    """The same designs conditioned on a named subset of the attributes (a subset view).

    Parameters
    ----------
    study : Study
    view : str, optional
        A key of ``spec.views``; default ``spec.view``.

    Returns
    -------
    Study
    """
    attrs = tuple(study.spec.views[view or study.spec.view])
    cond, M = _condition(study.feasible, attrs, study.spec)
    return Study(study.spec, study.regime, study.raw, study.feasible, attrs, M, cond)


def feasibility_table(study):
    """The feasibility conditions applied in order: how many fail alone and how many each removes.

    Parameters
    ----------
    study : Study

    Returns
    -------
    pandas.DataFrame
        Columns ``condition``, ``fails alone``, ``removed in this order``, ``remaining``.
    """
    raw, spec = study.raw, study.spec
    checks = {f: raw[f].astype(bool) for f in spec.flags}
    checks["all attributes positive"] = (raw[list(spec.attributes)] > 0).all(axis=1)
    alive, rows = pd.Series(True, index=raw.index), []
    for name, ok in checks.items():
        newly = int((alive & ~ok).sum())
        alive &= ok
        rows.append({"condition": name, "fails alone": int((~ok).sum()),
                     "removed in this order": newly, "remaining": int(alive.sum())})  # fmt: skip
    return pd.DataFrame(rows)


def conditioning_table(study):
    """Per attribute: orientation, raw range, log-spread, and the range of the conditioned metric.

    Parameters
    ----------
    study : Study

    Returns
    -------
    pandas.DataFrame
        Indexed by the attribute's plain name.
    """
    spec, pre = study.spec, study.preconditioner
    return pd.DataFrame(
        {
            "orientation": ["reciprocal" if spec.orientation[a] < 0 else "direct"
                            for a in study.attrs],
            "raw min": study.feasible[list(study.attrs)].min().to_numpy(),
            "raw max": study.feasible[list(study.attrs)].max().to_numpy(),
            "log-spread k": pre.log_scale_,
            "std of log m": np.log(study.M).std(axis=0),
            "m min": study.M.min(axis=0),
            "m max": study.M.max(axis=0),
        },
        index=study.names,
    )  # fmt: skip


def fit_study(study, K=1, target=None):
    """Select the temperature by the fraction-above criterion and fit the K-term estimator.

    Parameters
    ----------
    study : Study
    K : int, default 1
        Number of terms; ``K = 1`` is the monomial frontier.
    target : float, optional
        Target ``frac_above_``; default ``spec.target_frac``.

    Returns
    -------
    Fit
        ``(tau, estimator, K)``; ``estimator`` is fitted with ``random_state = spec.seed``.
    """
    hts, k_terms, _ = _lib()
    spec = study.spec
    tau = hts.select_temperature(
        study.M,
        target_frac_above=spec.target_frac if target is None else target,
        bounds=spec.tau_bounds,
        n_terms=K,
        random_state=spec.seed,
    )
    return Fit(float(tau), k_terms.fit_k(study.M, K, tau, spec.seed), K)


def exponent_table(study, fit):
    """The exponent of each metric at the fitted frontier, K = 1 or per term.

    Parameters
    ----------
    study : Study
    fit : Fit

    Returns
    -------
    pandas.DataFrame
        One row per metric; one column ``exponent w`` (K = 1) or ``term k`` per term.
    """
    W = np.atleast_2d(fit.estimator.exponents_)
    cols = ["exponent w"] if len(W) == 1 else [f"term {k + 1}" for k in range(len(W))]
    return pd.DataFrame(W.T, index=study.names, columns=cols).rename_axis("metric").reset_index()


def fit_line(study, fit):
    """One-row summary of a fit: temperature, fraction above V = 1, effective size, slack, offset.

    Parameters
    ----------
    study : Study
    fit : Fit

    Returns
    -------
    pandas.DataFrame
    """
    e = fit.estimator
    return pd.DataFrame([{
        "K": fit.K, "tau": fit.tau, "band 1/tau": fit.band, "frac_above_": e.frac_above_,
        "n_eff_": e.n_eff_, "objective_": e.objective_, "n": len(study.M),
        "sum of exponents": float(np.atleast_2d(e.exponents_)[0].sum()),
    }])  # fmt: skip


def tau_sweep(study, taus=None):
    """The K = 1 fit across temperatures: fraction above V = 1, effective size, exponent spread.

    Parameters
    ----------
    study : Study
    taus : sequence of float, optional
        Default: twelve log-spaced values over ``spec.tau_bounds`` and infinity.

    Returns
    -------
    pandas.DataFrame
    """
    hts, _, _ = _lib()
    if taus is None:
        taus = [*np.geomspace(*study.spec.tau_bounds, 12), np.inf]
    rows = []
    for t in taus:
        e = hts.HyperbolicTradeSpace(temperature=t, random_state=study.spec.seed).fit(study.M)
        w = e.exponents_[0]
        rows.append({"tau": t, "frac_above": e.frac_above_, "n_eff": e.n_eff_,
                     "metrics with w>1e-3": int((w > 1e-3).sum()), "largest w": w.max(),
                     "largest at": study.names[int(w.argmax())]})  # fmt: skip
    return pd.DataFrame(rows)


def _rebuilt(study, feasible=None, scaler="standard"):
    """A study on other rows or another scaler, conditioned afresh on the study's attributes."""
    feasible = study.feasible if feasible is None else feasible.reset_index(drop=True)
    cond, M = _condition(feasible, study.attrs, study.spec, scaler)
    return Study(study.spec, study.regime, study.raw, feasible, study.attrs, M, cond)


def _fit_row(study, fit, baseline=None):
    """One summary row of a K = 1 fit: temperature, fraction above, size, contending set."""
    e, rep = fit.estimator, _reports(study, fit)[0]
    contending = _sorted_contending(rep, study.names)
    row = {
        "tau": fit.tau,
        "frac_above_": e.frac_above_,
        "n_eff_": e.n_eff_,
        "n_lemma": rep.n_lemma,
        "contending set": ", ".join(contending),
        "largest exponent at": study.names[int(np.argmax(np.ravel(e.exponents_)))],
    }
    if baseline is not None:
        row["shared with baseline"] = len(set(contending) & set(baseline))
    return row, contending


def sensitivity_table(study):
    """The K = 1 fit under variants of the pipeline's choices, against the baseline.

    Variants: the target fraction above ``V = 1`` halved and doubled, the robust (log-IQR) scaler
    in place of the standard one, and each named view of the attributes (``spec.views``).

    Parameters
    ----------
    study : Study
        Built on all attributes (the ten-attribute fit).

    Returns
    -------
    pandas.DataFrame
        One row per variant: its setting, the selected temperature, ``frac_above_``, ``n_eff_``,
        the contending set, the largest exponent's metric and how many metrics of the baseline's
        contending set the variant's contending set shares.
    """
    spec = study.spec
    target = spec.target_frac
    base_row, base = _fit_row(study, fit_study(study))
    setting = f"target {target:g}, standard scaler, all"
    rows = [{"variant": "baseline", "setting": setting, **base_row,
             "shared with baseline": len(base)}]  # fmt: skip

    def add(variant, setting, st, fit):
        row, _ = _fit_row(st, fit, base)
        rows.append({"variant": variant, "setting": setting, **row})

    for label, t in (
        ("target fraction halved", target / 2),
        ("target fraction doubled", 2 * target),
    ):
        add(label, f"target {t:g}", study, fit_study(study, 1, t))
    robust = _rebuilt(study, scaler="robust")
    add("robust scaler", "log-IQR scaling", robust, fit_study(robust))
    for name in spec.views:
        v = view_study(study, name)
        add(f"view: {name}", f"{len(v.attrs)} attributes", v, fit_study(v))
    return pd.DataFrame(rows)


def category_refits(study):
    """The K = 1 fit refit within each level of the first covariate (the colour category).

    Parameters
    ----------
    study : Study
        Built on all attributes (the ten-attribute fit).

    Returns
    -------
    pandas.DataFrame
        One row per level of ``spec.category``: its designs, the temperature selected on them,
        ``frac_above_``, ``n_eff_``, the contending set and the largest exponent's metric. Empty
        when the spec has no covariate.
    """
    spec = study.spec
    rows = []
    for level in spec.covariates.get(spec.category, ()):
        sub = study.feasible[study.feasible[spec.category] == level]
        st = _rebuilt(study, sub)
        row, _ = _fit_row(st, fit_study(st))
        rows.append({spec.category: level, "designs": len(sub), **row})
    return pd.DataFrame(rows)


def k_fits(study, Ks=(1, 2, 3)):
    """Fits at each K, temperature re-selected at each K by the same criterion.

    Parameters
    ----------
    study : Study
    Ks : sequence of int

    Returns
    -------
    dict of int to Fit
    """
    return {K: fit_study(study, K) for K in Ks}


def k_table(study, fits):
    """The diagnostic table of a K sweep, with the certificate columns.

    Parameters
    ----------
    study : Study
    fits : dict of int to Fit
        As returned by :func:`k_fits`.

    Returns
    -------
    pandas.DataFrame
        Columns ``K``, ``tau``, ``band 1/tau``, ``objective_``, ``frac_above_``, ``term rows``,
        ``term shares``, ``max gap``, ``status``, ``gamma`` (margin), ``radius``, ``bound``.
    """
    _, k_terms, _ = _lib()
    return k_terms.summary({K: f.estimator for K, f in fits.items()}, study.M)


def k_sweep(study, Ks=(1, 2, 3)):
    """Fit at K = 1, 2, 3 and return the diagnostic table (the K-sweep record).

    Parameters
    ----------
    study : Study
    Ks : sequence of int

    Returns
    -------
    pandas.DataFrame
        As :func:`k_table`.
    """
    return k_table(study, k_fits(study, Ks))


def certificate_table(fits):
    """Certificate columns of the fits: status, largest term gap, margin, radius, bound.

    Parameters
    ----------
    fits : dict of int to Fit

    Returns
    -------
    pandas.DataFrame
        One row per K. At K = 1 the status is ``not_applicable`` and margin and radius are NaN.
    """
    _, k_terms, _ = _lib()
    return pd.DataFrame([{"K": K, **k_terms.certificate(f.estimator)} for K, f in fits.items()])


def mean_slack_by_k(study, fits):
    """The mean slack of each fit, from the estimator's ``mean_slack_``, at each fit's own tau.

    Parameters
    ----------
    study : Study
    fits : dict of int to Fit
        As returned by :func:`k_fits` (the temperature is re-selected at each K).

    Returns
    -------
    pandas.DataFrame
        Columns ``K``, ``tau`` and ``mean_slack_``. The temperatures differ from row to row, so the
        rows are not compared like for like; :func:`mean_slack_fixed_tau` does that.
    """
    return pd.DataFrame(
        [{"K": K, "tau": f.tau, "mean_slack_": float(f.estimator.mean_slack_)}
         for K, f in fits.items()]
    )  # fmt: skip


def mean_slack_fixed_tau(study, fits, tau=None):
    """The mean slack at K = 1, 2, 3 refitted at one temperature (default: the K = 1 temperature).

    Parameters
    ----------
    study : Study
    fits : dict of int to Fit
        As returned by :func:`k_fits`; its keys are the K to refit.
    tau : float, optional
        The common temperature; default the temperature selected for the smallest K.

    Returns
    -------
    pandas.DataFrame
        Columns ``K``, ``tau`` and ``mean_slack_``; ``mean_slack_`` is comparable across ``K`` at
        a fixed temperature (``objective_`` is not).
    """
    _, k_terms, _ = _lib()
    tau = fits[min(fits)].tau if tau is None else float(tau)
    return pd.DataFrame(
        [{"K": K, "tau": tau,
          "mean_slack_": float(k_terms.fit_k(study.M, K, tau, study.spec.seed).mean_slack_)}
         for K in fits]
    )  # fmt: skip


def margin_scale(study, fits):
    """The assignment margin and stable radius of the several-term fits against two scales.

    Parameters
    ----------
    study : Study
    fits : dict of int to Fit
        As returned by :func:`k_fits`; the K = 1 fit has no competing term and is left out.

    Returns
    -------
    pandas.DataFrame
        Columns ``K``, ``band 1/tau``, ``gamma`` (the margin), ``radius``, and ``median margin``,
        the median over the rows of the gap between a row's best and second-best term score.
        The margin is read against the band and against the median margin.
    """
    rows = []
    U = np.log(study.M)
    for K, f in fits.items():
        if K == 1:
            continue
        e = f.estimator
        top = np.sort(U @ np.atleast_2d(e.exponents_).T - e.log_offset_, axis=1)
        t = e.termination_
        rows.append({"K": K, "band 1/tau": f.band, "gamma": float(t.gamma),
                     "radius": float(t.radius),
                     "median margin": float(np.median(top[:, -1] - top[:, -2]))})  # fmt: skip
    return pd.DataFrame(rows)


def pca_directions(study, fit, n=3, leading=3):
    """Principal directions of the near-frontier chart coordinates of the fit (its first term).

    The tension report already runs a principal component analysis on the chart coordinates ``Z``
    of the near-frontier designs; this table reads it: the share of the spread along each of the
    first ``n`` directions and the metrics that load most on it.

    Parameters
    ----------
    study : Study
    fit : Fit
        A K = 1 fit (the first term's report is read).
    n : int, default 3
        Directions listed.
    leading : int, default 3
        Metrics listed per direction.

    Returns
    -------
    pandas.DataFrame
        Columns ``direction``, ``share of spread`` and ``leading loadings``; the overall sign of
        a direction is arbitrary, so each is signed with its largest loading positive.
    """
    rep = _reports(study, fit)[0]
    rows = []
    for i in range(min(n, len(rep.explained_spread))):
        load = np.asarray(rep.tension_loadings[i], float)
        load = load if load[np.argmax(np.abs(load))] > 0 else -load
        top = np.argsort(-np.abs(load))[:leading]
        rows.append({
            "direction": i + 1, "share of spread": float(rep.explained_spread[i]),
            "leading loadings": ", ".join(f"{study.names[j]} {load[j]:+.2f}" for j in top),
        })  # fmt: skip
    return pd.DataFrame(rows)


MIN_NEAR_FRONTIER = 10
"""The guard of the association reading: the near-frontier rows a term needs (the library's 10)."""


def term_reports(estimator, M, band, **kw):
    """Every term's tension report, the guard of ten applied per term and not over all terms.

    The library's ``tension_report`` refuses a fit at K > 1 when any one term has fewer than
    ``min_near_frontier`` near-frontier rows. The fit itself (exponents, cells, shares, the
    contending sets on each term's rows) exists for every term, and only the association
    reading needs the rows, so the report is called with the library's guard set to zero and
    the same guard, :data:`MIN_NEAR_FRONTIER`, is applied here term by term (:func:`has_reading`);
    the band is the one given, never widened.

    Parameters
    ----------
    estimator : HyperbolicTradeSpace
        A fitted estimator.
    M : array of shape (n, d)
        Its metrics.
    band : float
        The near-frontier band.
    **kw
        Passed to ``tension_report`` (``association``).

    Returns
    -------
    list of TensionReport
        One per term; a term without the rows carries an association it does not stand behind,
        which :func:`has_reading` tells apart and no caller reads.
    """
    hts, _, _ = _lib()
    r = hts.tension_report(estimator, M, band=band, min_near_frontier=0, **kw)
    return r if isinstance(r, list) else [r]


def has_reading(rep) -> bool:
    """Whether a term's near-frontier rows meet the guard of the association reading."""
    return rep.n_near_frontier >= MIN_NEAR_FRONTIER


def thin_reason(n_near: int) -> str:
    """The one sentence that replaces the association reading of a term without the rows.

    >>> thin_reason(3)
    'too few near-frontier designs for an association reading: 3 of ten'
    """
    return f"too few near-frontier designs for an association reading: {int(n_near)} of ten"


def _all_terms(study, fit, band=None, **kw):
    """Every term's report at the band (default the fit's), the guard applied per term."""
    return term_reports(fit.estimator, study.M, fit.band if band is None else band, **kw)


def _reports(study, fit, band=None, **kw):
    """The reports for an association reading: every term must meet the guard, else it refuses."""
    reps = _all_terms(study, fit, band, **kw)
    for k, rep in enumerate(reps):
        if not has_reading(rep):
            raise ValueError(f"term {k + 1}: {thin_reason(rep.n_near_frontier)}")
    return reps


def term_tension_panels(reps, names, axes, plotting, who="term"):
    """One association panel per term on ``axes``; a term without the rows gets its reason.

    The panel of a thin term is left empty but for the sentence of :func:`thin_reason`, so the
    figure keeps one row per term and says why one is not drawn.
    """
    for k, (ax, rep) in enumerate(zip(axes, reps, strict=True)):
        if has_reading(rep):
            plotting.plot_tensions(rep, names=names, ax=ax)
            ax.set_title(_member_title(rep, f"{who} {k + 1}"))
        else:
            ax.set_axis_off()
            ax.set_title(_member_title(rep, f"{who} {k + 1}"))
            ax.text(0.5, 0.5, _wrap(thin_reason(rep.n_near_frontier), 40).capitalize(), ha="center",
                    va="center", transform=ax.transAxes)  # fmt: skip


def _sorted_contending(rep, names):
    order = np.argsort(-rep.contending_exponents)
    return [names[rep.contending_set[i]] for i in order]


def tension_table(study, fit, band=None):
    """Per term: the contending set (largest exponent first) and the facts of its report.

    Parameters
    ----------
    study : Study
    fit : Fit
    band : float, optional
        Near-frontier band of the report; default ``1 / tau``.

    Returns
    -------
    pandas.DataFrame
        Columns ``term``, ``n_lemma``, ``near-frontier``, ``contending set``,
        ``largest exponents``.
    """
    _, k_terms, _ = _lib()
    rows = []
    for k, rep in enumerate(_all_terms(study, fit, band)):
        rows.append({
            "term": k + 1, "n_lemma": rep.n_lemma, "near-frontier": rep.n_near_frontier,
            "contending set": ", ".join(_sorted_contending(rep, study.names)),
            "largest exponents": k_terms.top(study.names, rep.exponents, 3),
        })  # fmt: skip
    return pd.DataFrame(rows)


def term_table(study, fits, K=3, band=None):
    """One row of facts per term of the K-term fit, with the term's first-order gap.

    Parameters
    ----------
    study : Study
    fits : dict of int to Fit
        As returned by :func:`k_fits`; the report band defaults to the K = 1 band when K = 1 is
        present (the same band at every K), else the fit's own.
    K : int
        Which fit.
    band : float, optional

    Returns
    -------
    pandas.DataFrame
        Columns ``term``, ``rows``, ``contending set``, ``n_lemma``, ``largest exponents``,
        ``near-frontier``, ``reach beta_k``, ``share``, ``gap G_k``.
    """
    _, k_terms, _ = _lib()
    fit = fits[K]
    est = fit.estimator
    if band is None:
        band = fits[1].band if 1 in fits else fit.band
    sizes = np.bincount(est.cell_, minlength=K) if K > 1 else [len(study.M)]
    out = []
    for k, rep in enumerate(_all_terms(study, fit, band)):
        out.append({
            "term": k + 1, "rows": int(sizes[k]),
            "contending set": ", ".join(_sorted_contending(rep, study.names)),
            "n_lemma": rep.n_lemma, "largest exponents": k_terms.top(study.names, rep.exponents),
            "near-frontier": rep.n_near_frontier, "reach beta_k": float(est.log_offset_[k]),
            "share": float(est.term_share_[k]) if K > 1 else 1.0,
            "gap G_k": float(est.termination_.gaps[k]),
        })  # fmt: skip
    return pd.DataFrame(out)


def association_table(study, fit, pairs=None):
    """Association among the near-frontier designs for named metric pairs (Pearson and Spearman).

    Parameters
    ----------
    study : Study
    fit : Fit
        A K = 1 fit.
    pairs : sequence of (str, str), optional
        Short metric names; default ``spec.association_pairs``.

    Returns
    -------
    pandas.DataFrame
        Columns ``metric a``, ``metric b``, ``pearson``, ``spearman``.
    """
    rep = _reports(study, fit)[0]
    rep_s = _reports(study, fit, association="spearman")[0]
    names = study.names
    rows = []
    for a, b in pairs or study.spec.association_pairs:
        i, j = names.index(a), names.index(b)
        rows.append({"metric a": a, "metric b": b, "pearson": float(rep.association[i, j]),
                     "spearman": float(rep_s.association[i, j])})  # fmt: skip
    return pd.DataFrame(rows)


def regime_comparison(spec=CUBESAT, n_max=None):
    """The regimes through the identical pipeline, side by side.

    Parameters
    ----------
    spec : CaseSpec
    n_max : int, optional

    Returns
    -------
    pandas.DataFrame
        One row per quantity, one column per regime (the first regime is the primary one).
    """
    res = {}
    for regime in spec.regimes:
        st = load_study(regime, spec, n_max)
        fit = fit_study(st)
        rep = _reports(st, fit)[0]
        res[regime] = (st, fit, rep, _reports(st, fit, association="spearman")[0])
    cat = spec.category
    levels = spec.covariates.get(cat, ())

    def feasible_n(st, fit, rep, rep_s):
        by = " / ".join(str(int((st.feasible[cat] == lv).sum())) for lv in levels)
        return f"{len(st.feasible)} ({by})" if levels else str(len(st.feasible))

    def tau_line(st, fit, rep, rep_s):
        e = fit.estimator
        return f"{fit.tau:.1f}, {e.frac_above_:.3f}, {e.n_eff_:.1f}"

    rows = {
        "dataset": lambda st, fit, rep, rep_s: spec.regimes[st.regime],
        "feasible n": feasible_n,
        "tau, frac_above_, n_eff_": tau_line,
        "band 1/tau, near-frontier designs": lambda st, fit, rep, rep_s: (
            f"{rep.band:.4f}, {rep.n_near_frontier}"
        ),
        "n_lemma": lambda st, fit, rep, rep_s: str(rep.n_lemma),
        "contending set": lambda st, fit, rep, rep_s: ", ".join(_sorted_contending(rep, st.names)),
    }
    table = {q: {rg: fn(*res[rg]) for rg in res} for q, fn in rows.items()}
    for a, b in spec.association_pairs:
        table[f"{a}, {b}"] = {}
        for rg, (st, _, r, s) in res.items():
            i, j = st.names.index(a), st.names.index(b)
            table[f"{a}, {b}"][rg] = f"{r.association[i, j]:+.2f} ({s.association[i, j]:+.2f})"
    return pd.DataFrame(table).T.rename_axis("quantity").reset_index()


def nondominated_mask(X):
    """Rows of ``X`` that no other row dominates (larger is better in every column).

    Parameters
    ----------
    X : array of shape (n, d)

    Returns
    -------
    numpy.ndarray of bool, shape (n,)
    """
    pts = np.asarray(X, float)
    keep = np.ones(len(pts), bool)
    for i, row in enumerate(pts):
        keep[i] = not ((pts >= row).all(axis=1) & (pts > row).any(axis=1)).any()
    return keep


def nondominated_counts(study):
    """Nondominated designs among the feasible ones, for all attributes and for each named view.

    Parameters
    ----------
    study : Study
        Built on all attributes.

    Returns
    -------
    pandas.DataFrame
        Columns ``view``, ``columns``, ``nondominated``, ``of``, ``share``.
    """
    spec = study.spec
    views = {"all attributes": tuple(study.attrs), **{k: tuple(v) for k, v in spec.views.items()}}
    rows = []
    for name, attrs in views.items():
        idx = [study.attrs.index(a) for a in attrs]
        n = int(nondominated_mask(study.M[:, idx]).sum())
        rows.append({"view": name, "columns": len(attrs), "nondominated": n, "of": len(study.M),
                     "share": n / len(study.M)})  # fmt: skip
    return pd.DataFrame(rows)


def _features(spec, df):
    """Configuration to regressor features in [0, 1]: log-scaled variables, ordinal categories."""
    cols = []
    for c in spec.design_vars:
        lo, hi = spec.ranges[c]
        cols.append((np.log(df[c].to_numpy(float)) - np.log(lo)) / (np.log(hi) - np.log(lo)))
    for c, levels in spec.covariates.items():
        step = {v: i / max(len(levels) - 1, 1) for i, v in enumerate(levels)}
        cols.append(df[c].map(step).to_numpy(float))
    return np.column_stack(cols)


def candidate_table(study, fit):
    """Measured candidate designs scored against the K = 1 frontier of the study.

    Parameters
    ----------
    study : Study
        Built on all attributes (the ten-attribute fit).
    fit : Fit

    Returns
    -------
    pandas.DataFrame
        Columns ``candidate``, covariates, ``log V``, ``novelty V-1``, ``rank among training``,
        ``tau*log V``.
    """
    spec, est = study.spec, fit.estimator
    checks = pd.read_csv(Path(spec.data_dir) / spec.checks_file)
    cand = checks[checks.role == "candidate"].reset_index(drop=True)
    Mc = np.asarray(study.preconditioner.transform(cand[list(study.attrs)]))
    cal = est.novelty_score(Mc, calibrated=True)
    out = pd.DataFrame({"candidate": cand["name"], **{c: cand[c] for c in spec.covariates}})
    out["log V"] = est.score_samples(Mc)
    out["novelty V-1"] = est.novelty_score(Mc)
    out["rank among training"] = cal[:, 0]
    out["tau*log V"] = cal[:, 1]
    return out


def white_space_targets(study, n=3, resolution=30, threshold=2.0):
    """The most isolated holes of the chart and the attributes that put a design on V = 1 there.

    Parameters
    ----------
    study : Study
        A subset view (see :func:`view_study`).
    n : int
        Number of well-separated holes.
    resolution, threshold : int, float
        Grid and isolation threshold of ``find_holes``.

    Returns
    -------
    pandas.DataFrame
        ``hole score`` and one column per attribute in attribute units.
    """
    from hyperbolic_trade_space.gaps import find_holes, frontier_targets

    fit = fit_study(study)
    chart = fit.estimator.transform(study.M)
    Z = chart[:, :-1]
    holes, hscore = find_holes(Z, resolution=resolution, threshold=threshold)
    nn = np.sort(np.linalg.norm(Z[:, None] - Z[None], axis=2), axis=1)[:, 1]
    sep, pick = 1.5 * np.median(nn), []
    for h in holes:
        if all(np.linalg.norm(h - p) > sep for p in pick):
            pick.append(h)
        if len(pick) == n:
            break
    pick = np.array(pick)
    tg = frontier_targets(pick, fit.estimator, study.preconditioner)
    spec = study.spec
    tab = pd.DataFrame(
        tg["attributes"], columns=[f"{spec.short[a]} ({spec.units[a]})" for a in study.attrs]
    )
    tab.insert(
        0, "hole score", hscore[[int(np.argmin(np.linalg.norm(holes - p, axis=1))) for p in pick]]
    )
    return tab


class Regressor(NamedTuple):
    """The configuration-to-chart regressor of the subset view and its trade-space temperature."""

    model: Any
    tau: float
    view: Study


def fit_regressor(study, view=None):
    """Fit the Gaussian-process regressor from configuration to the chart ``[Z | log V]`` of a view.

    Parameters
    ----------
    study : Study
        Built on all attributes (the feasible designs and spec are used).
    view : str, optional
        A key of ``spec.views``; default ``spec.view``.

    Returns
    -------
    Regressor
        ``(model, tau, view_study)``; deterministic (seeded GP restarts).
    """
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
    from sklearn.pipeline import make_pipeline

    from hyperbolic_trade_space import (
        HyperbolicTradeSpace,
        LogAffinePreconditioner,
        TradeSpaceRegressor,
        select_temperature,
    )

    spec = study.spec
    vs = view_study(study, view)
    orient = [spec.orientation[a] for a in vs.attrs]
    Y = vs.feasible[list(vs.attrs)].to_numpy(float)
    pre = LogAffinePreconditioner(orientation=orient, scaler="standard")
    tau = select_temperature(
        pre.fit_transform(Y), target_frac_above=spec.target_frac, bounds=spec.tau_bounds
    )
    ts = make_pipeline(
        LogAffinePreconditioner(orientation=orient, scaler="standard"),
        HyperbolicTradeSpace(temperature=tau),
    )
    X = _features(spec, vs.feasible)
    gp = GaussianProcessRegressor(
        kernel=ConstantKernel(1.0) * RBF(length_scale=np.ones(X.shape[1])) + WhiteKernel(0.1),
        normalize_y=True,
        n_restarts_optimizer=2,
        random_state=spec.seed,
    )
    return Regressor(TradeSpaceRegressor(gp, ts).fit(X, Y), float(tau), vs)


def proposals_table(study, reg):
    """The recorded proposals with the regressor's predictions refit now and their agreement.

    Parameters
    ----------
    study : Study
    reg : Regressor
        From :func:`fit_regressor`.

    Returns
    -------
    pandas.DataFrame
        The recorded ``pred_log_v`` and ``pred_z*`` columns, the refit's, and the largest absolute
        difference per proposal.
    """
    spec = study.spec
    preds = pd.read_csv(Path(spec.data_dir) / spec.predictions_file)
    zc = [c for c in preds.columns if c.startswith("pred_z")]
    Zp, lvp = reg.model.predict_coordinates(_features(spec, preds))
    refit = np.c_[Zp, np.ravel(lvp)]
    rec = preds[[*zc, "pred_log_v"]].to_numpy()
    out = preds[["name", *spec.covariates, "hole_score", "distance_to_target"]].copy()
    out["recorded log V"] = preds["pred_log_v"].to_numpy()
    out["refit log V"] = refit[:, -1]
    out["max |recorded - refit|"] = np.abs(refit - rec).max(axis=1)
    return out


def predict_check(study, reg):
    """Propose, predict, check: predicted against measured chart position of each proposal.

    Parameters
    ----------
    study : Study
    reg : Regressor
        From :func:`fit_regressor`.

    Returns
    -------
    pandas.DataFrame
        Columns ``proposal``, ``predicted log V``, ``measured log V``, ``difference``,
        ``|diff| / band``, ``log V within band``, ``||dZ||``, ``||dZ|| / band``, ``Z within band``.
        The predictions are the recorded ones (the file is the authority).
    """
    spec = study.spec
    preds = pd.read_csv(Path(spec.data_dir) / spec.predictions_file)
    checks = pd.read_csv(Path(spec.data_dir) / spec.checks_file)
    meas = checks[checks.role == "proposal"].reset_index(drop=True)
    attrs = list(reg.view.attrs)
    chart = reg.model.trade_space_.transform(meas[attrs].to_numpy(float))
    Zm, lvm = chart[:, :-1], chart[:, -1]
    zc = [c for c in preds.columns if c.startswith("pred_z")]
    band = 1.0 / reg.tau
    rows = []
    for i, r in preds.iterrows():
        dz = float(np.linalg.norm(Zm[i] - r[zc].to_numpy(float)))
        dl = float(lvm[i] - r.pred_log_v)
        rows.append({
            "proposal": r["name"], "predicted log V": r.pred_log_v, "measured log V": lvm[i],
            "difference": dl, "|diff| / band": abs(dl) / band, "log V within band": abs(dl) <= band,
            "||dZ||": dz, "||dZ|| / band": dz / band, "Z within band": dz <= band,
        })  # fmt: skip
    return pd.DataFrame(rows)


def _colors(study):
    cat = study.spec.category
    if cat is None:
        return None
    levels = list(study.spec.covariates[cat])
    return study.feasible[cat].map({v: f"{i + 1} {v}" for i, v in enumerate(levels)}).to_numpy()


def cond_label(study, a):
    """Axis label of a conditioned metric, in attribute terms.

    Parameters
    ----------
    study : Study
    a : str
        Attribute column.

    Returns
    -------
    str
    """
    s = study.spec
    inv = "inverse " if s.orientation[a] < 0 else ""
    return f"conditioned {s.short[a]} ({inv}{s.units[a]}; larger is better)"


_REGIME_WORDS = {"stock": "baseline"}
"""The regime key of a CaseSpec and the word a figure prints for it (WP23: "primary regime" and
"baseline regime" are the two names; the key ``stock`` stays in the data files)."""

EXPONENT_FLOOR = 1e-3
"""An exponent at or below this is drawn white in the sweep figure (the participation threshold)."""


def regime_word(study):
    """The name of a study's regime as a figure prints it.

    Parameters
    ----------
    study : Study

    Returns
    -------
    str
        ``"baseline"`` for the key ``stock``; otherwise the key itself.

    Examples
    --------
    >>> from types import SimpleNamespace
    >>> regime_word(SimpleNamespace(regime="stock"))
    'baseline'
    >>> regime_word(SimpleNamespace(regime="primary"))
    'primary'
    """
    return _REGIME_WORDS.get(study.regime, study.regime)


def _exponent_cmap(plt):
    """Greys from a visible light grey to black, white below the floor."""
    from matplotlib.colors import LinearSegmentedColormap

    greys = plt.get_cmap("Greys")(np.linspace(0.3, 1.0, 256))
    return LinearSegmentedColormap.from_list("exponent", greys).with_extremes(under="white")


def _colorbar_ticks(vmin, vmax):
    """The ends of the colour scale and the round values between them, clear of the ends."""
    inner = [v for v in np.arange(0.1, vmax, 0.1) if min(v - vmin, vmax - v) > 0.08 * vmax]
    return [vmin, *inner, vmax], [f"{vmin:g}", *[f"{v:.1f}" for v in inner], f"{vmax:.2f}"]


FIT_COLUMN_TOLERANCE = 0.02
"""A fit temperature within this relative distance of a sweep temperature is drawn as that
column, outlined, instead of as an inserted column (the two would be pixel-alike)."""


def _sweep_with_fit(taus, tau):
    """The finite sweep temperatures with the fit temperature among them, its index, and
    whether it was inserted.

    Examples
    --------
    >>> _sweep_with_fit([10.0, 20.0, 40.0], 20.3)
    (array([10., 20., 40.]), 1, False)
    >>> _sweep_with_fit([10.0, 20.0, 40.0], 25.0)
    (array([10., 20., 25., 40.]), 2, True)
    """
    taus = np.asarray(taus, dtype=float)
    rel = np.abs(taus - tau) / taus
    if rel.min() <= FIT_COLUMN_TOLERANCE:
        return taus, int(rel.argmin()), False
    taus = np.sort([*taus, tau])
    return taus, int(np.searchsorted(taus, tau)), True


@_legible
def tau_sweep_figure(study, fit, title=None, vmax=None):
    """The K = 1 fit against the fit temperature: fraction above V = 1, effective size, exponents.

    The fit temperature is a column of the exponent grid (``_sweep_with_fit``: the sweep's column
    within ``FIT_COLUMN_TOLERANCE`` of it, else a column inserted), outlined, its exponents printed
    in the cells, and marked on the top panels by a vertical line with the effective sample size
    at it. Rows are ordered by the exponent at that column, largest at the top; rows white there
    come last, in the study's order. The colour scale runs from ``EXPONENT_FLOOR`` (white at or
    below it) to ``vmax``; two regimes drawn side by side share one ``vmax``.

    Parameters
    ----------
    study : Study
    fit : Fit
        The K = 1 fit at the fit temperature.
    title : str, optional
        The figure's title; default names the regime (``regime_word``).
    vmax : float, optional
        Top of the colour scale; default the largest exponent of the sweep.

    Returns
    -------
    matplotlib.figure.Figure
    """
    from matplotlib.patches import Rectangle

    hts, _, plotting = _lib()
    plt = _plt()
    spec = study.spec
    finite, sel, inserted = _sweep_with_fit(np.geomspace(*spec.tau_bounds, 12), fit.tau)
    sweep = tau_sweep(study, taus=[*finite, np.inf])
    fin = sweep[np.isfinite(sweep.tau)]
    W = np.array(
        [
            hts.HyperbolicTradeSpace(temperature=t, random_state=spec.seed)
            .fit(study.M)
            .exponents_[0]
            for t in sweep.tau
        ]
    )
    at_fit = np.where(W[sel] > EXPONENT_FLOOR, W[sel], 0.0)
    order = np.argsort(-at_fit, kind="stable")
    names = [study.names[i] for i in order]
    vmax = float(W.max()) if vmax is None else float(vmax)

    fig = plt.figure(figsize=(FIGURE_WIDTH_IN, 7.0))
    grid = fig.add_gridspec(2, 2, height_ratios=[1, 1.45])
    axes = [fig.add_subplot(grid[0, 0]), fig.add_subplot(grid[0, 1]), fig.add_subplot(grid[1, :])]
    axes[0].semilogx(fin.tau, fin.frac_above, "o-", color=plotting.DATA_COLOR, ms=4)
    axes[0].axhline(spec.target_frac, color=plotting.FRONTIER_COLOR, lw=0.8, ls="--")
    axes[0].annotate(
        f"target {spec.target_frac:g}", (fin.tau.iloc[-1], spec.target_frac),
        xytext=(0, 3), textcoords="offset points", ha="right", va="bottom",
    )  # fmt: skip
    axes[0].set(xlabel="fit temperature tau", ylabel="fraction of designs above V = 1")
    axes[1].semilogx(fin.tau, fin.n_eff, "o-", color=plotting.DATA_COLOR, ms=4)
    n_eff = float(fit.estimator.n_eff_)
    axes[1].annotate(
        f"n_eff = {n_eff:.0f}", (fit.tau, n_eff), xytext=(6, 10), textcoords="offset points"
    )
    axes[1].set(xlabel="fit temperature tau", ylabel="effective sample size")
    for ax in axes[:2]:
        ax.axvline(fit.tau, color=plotting.FRONTIER_COLOR, lw=1.5)

    im = axes[2].imshow(
        W[:, order].T, cmap=_exponent_cmap(plt), aspect="auto", vmin=EXPONENT_FLOOR, vmax=vmax
    )
    labels = [f"{t:.0f}" if np.isfinite(t) else "∞ (limit)" for t in sweep.tau]
    if inserted:
        labels[sel] = f"{fit.tau:.1f}"
    axes[2].set_xticks(range(len(sweep)), labels, rotation=60)
    axes[2].get_xticklabels()[sel].set_fontweight("bold")
    axes[2].tick_params(axis="x", pad=6)  # before the long tick: tick_params resets every tick
    axes[2].xaxis.get_major_ticks()[sel].tick1line.set_markersize(8)  # shows past the ring
    axes[2].set_yticks(range(len(names)), names)
    axes[2].set_xticks(np.arange(len(sweep) + 1) - 0.5, minor=True)
    axes[2].set_yticks(np.arange(len(names) + 1) - 0.5, minor=True)
    axes[2].grid(which="minor", color="white", lw=1)
    axes[2].tick_params(which="minor", length=0)
    # a ring on any grey, above the grid lines (the axis draws at 1.5: hence the long tick)
    for color, lw, z in (("white", 5, 2.0), (plotting.FRONTIER_COLOR, 2, 2.1)):
        axes[2].add_patch(Rectangle(
            (sel - 0.5, -0.5), 1, len(names), fill=False, lw=lw, edgecolor=color,
            clip_on=False, zorder=z,
        ))  # fmt: skip
    for r, w in enumerate(at_fit[order]):
        if w > 0:
            dark = (w - EXPONENT_FLOOR) / (vmax - EXPONENT_FLOOR) > 0.45
            axes[2].text(
                sel, r, f"{w:.2f}" if w >= 0.005 else "<0.01", ha="center", va="center",
                color="white" if dark else "black", zorder=3,
            )  # fmt: skip
    axes[2].set(
        xlabel="fit temperature tau",
        title="K = 1 exponent of each metric; the outlined column is the fit temperature",
    )
    ticks, ticklabels = _colorbar_ticks(EXPONENT_FLOOR, vmax)
    cbar = fig.colorbar(im, ax=axes[2], extend="min", ticks=ticks, pad=0.02)
    cbar.set_ticklabels(ticklabels)
    cbar.set_label("exponent w (white: at most 0.001)")
    fig.suptitle(
        title or f"The K = 1 fit against the fit temperature tau, {regime_word(study)} regime"
    )
    fig.tight_layout()
    return fig


@_legible
def log_plane_figure(study, fit, band=None):
    """Log-plane slices of the fit, one per pair of each term's two largest exponents.

    Parameters
    ----------
    study : Study
    fit : Fit
        K = 1 or K > 1.
    band : float, optional
        Near-frontier band; default ``1 / tau``.

    Returns
    -------
    matplotlib.figure.Figure
        Panel titles name the terms drawn.
    """
    hts, k_terms, plotting = _lib()
    plt = _plt()
    est, M = fit.estimator, study.M
    band = fit.band if band is None else band
    U = np.log(M)
    labels = plotting.cell_labels(est, M)
    pairs = k_terms.slice_pairs(est)
    fig, axes = plt.subplots(len(pairs), 1, figsize=(FIGURE_WIDTH_IN, 4.6 * len(pairs)),
                             squeeze=False)  # fmt: skip
    for ax, (j, k) in zip(axes[:, 0], pairs, strict=True):
        keep, ws, bs = k_terms._slice(est, U, labels, band, j, k)
        sh = hts.HyperbolicTradeSpace(temperature=fit.tau, n_terms=len(keep))
        sh.exponents_, sh.log_offset_ = np.array(ws), np.array(bs)
        plotting.plot_log_plane(sh, M[:, [j, k]], color=labels, band=band, ax=ax)
        for lim, col in ((ax.set_xlim, j), (ax.set_ylim, k)):
            lo, hi = U[:, col].min(), U[:, col].max()
            lim(lo - 0.1 * (hi - lo), hi + 0.1 * (hi - lo))
        ax.set_xlabel(_wrap("log of the " + cond_label(study, study.attrs[j]), 80))
        ax.set_ylabel(_wrap("log of the " + cond_label(study, study.attrs[k]), 44))
        noun = "term" if len(keep) == 1 else "terms"
        names = ", ".join(str(f + 1) for f in keep)
        ax.set_title(
            f"{study.names[j]} and {study.names[k]}\n{noun} {names} drawn",
        )
    fig.tight_layout()
    return fig


@_legible
def coordinates_figure(study, fit, band=None):
    """Position along the frontier: two pairs of chart coordinates, shaded by cell.

    Parameters
    ----------
    study : Study
    fit : Fit
    band : float, optional

    Returns
    -------
    matplotlib.figure.Figure
    """
    _, _, plotting = _lib()
    plt = _plt()
    band = fit.band if band is None else band
    chart = fit.estimator.transform(study.M)
    Z, logv = chart[:, :-1], chart[:, -1]
    labels = plotting.cell_labels(fit.estimator, study.M) if fit.K > 1 else _colors(study)
    fig, axes = plt.subplots(2, 1, figsize=(FIGURE_WIDTH_IN, 8.4))
    for ax, c in zip(axes, [(0, 1), (0, 2)], strict=True):
        if max(c) >= Z.shape[1]:
            c = (0, Z.shape[1] - 1)
        plotting.plot_frontier_coordinates(Z[:, list(c)], logv, color=labels, band=band, ax=ax)
        ax.set_xlabel(f"Z{c[0]} (log-ratio coordinate along the frontier, dimensionless)")
        ax.set_ylabel(
            _wrap(f"Z{c[1]} (log-ratio coordinate along the frontier, dimensionless)", 40)
        )
    fig.tight_layout()
    return fig


def _member_title(rep, who):
    """A panel title that says what the count counts: the members of the exact-maximum support.

    The panel outlines the contending set (the support of the exact-maximum fit on the term's
    rows, the tension report's) on the diagonal; the exponent in each label is the working
    temperature's, which grades how strongly a member contends and can be small.
    """
    n = int(rep.n_lemma)
    plural = "s" if n != 1 else ""
    return f"{who}: {rep.lemma_name} ({n} metric{plural} in the exact-maximum support)"


@_legible
def tension_figure(study, fit, band=None):
    """Association among the near-frontier designs, one map per term.

    A term whose near-frontier rows do not meet the guard (:func:`has_reading`) gets the sentence
    of :func:`thin_reason` in place of its map, set above the next map (below the last), so it
    takes the height of its sentence and not of a panel.

    Parameters
    ----------
    study : Study
    fit : Fit
    band : float, optional

    Returns
    -------
    matplotlib.figure.Figure
    """
    _, _, plotting = _lib()
    plt = _plt()
    reps = _all_terms(study, fit, band)
    shown = [k for k, r in enumerate(reps) if has_reading(r)]
    if not shown:  # no map at all: one row per term, each its sentence
        fig, axes = plt.subplots(len(reps), 1, figsize=(FIGURE_WIDTH_IN, 0.8 * len(reps)),
                                 squeeze=False)  # fmt: skip
        term_tension_panels(reps, study.names, axes[:, 0], plotting)
        fig.tight_layout()
        return fig
    fig, axes = plt.subplots(len(shown), 1, figsize=(FIGURE_WIDTH_IN, 6.8 * len(shown)),
                             squeeze=False)  # fmt: skip
    axes = axes[:, 0]
    for ax, k in zip(axes, shown, strict=True):
        plotting.plot_tensions(reps[k], names=study.names, ax=ax)
        ax.set_title(_member_title(reps[k], f"term {k + 1}"))
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    for k, rep in enumerate(reps):
        if has_reading(rep):
            continue
        title = _member_title(rep, f"term {k + 1}")
        note = f"{title}\n{thin_reason(rep.n_near_frontier).capitalize()}"
        after = [i for i, j in enumerate(shown) if j > k]
        if after:  # above the next map's title
            ax = axes[after[0]]
            ax.annotate(note, (0.5, 1), xycoords="axes fraction", xytext=(0, 30),
                        textcoords="offset points", ha="center", va="bottom")  # fmt: skip
        else:  # below the last map's tick labels
            ax = axes[-1]
            ax.annotate(note, (0.5, 0), xycoords=ax.xaxis.get_tightbbox, xytext=(0, -12),
                        textcoords="offset points", ha="center", va="top")  # fmt: skip
    fig.tight_layout()
    return fig


@_legible
def regime_figure(spec=CUBESAT, n_max=None):
    """The tension maps of every regime side by side.

    Parameters
    ----------
    spec : CaseSpec
    n_max : int, optional

    Returns
    -------
    matplotlib.figure.Figure
    """
    _, _, plotting = _lib()
    plt = _plt()
    fig, axes = plt.subplots(
        len(spec.regimes), 1, figsize=(FIGURE_WIDTH_IN, 6.8 * len(spec.regimes)), squeeze=False
    )
    for ax, regime in zip(axes[:, 0], spec.regimes, strict=True):
        st = load_study(regime, spec, n_max)
        rep = _reports(st, fit_study(st))[0]
        plotting.plot_tensions(rep, names=st.names, ax=ax)
        ax.set_title(_member_title(rep, regime))
        plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
    fig.tight_layout()
    return fig


@_legible
def predict_check_figure(study, reg):
    """Predicted (open) and measured (filled diamond) chart positions of the proposals.

    Parameters
    ----------
    study : Study
    reg : Regressor

    Returns
    -------
    matplotlib.figure.Figure
    """
    _, _, plotting = _lib()
    plt = _plt()
    spec = study.spec
    preds = pd.read_csv(Path(spec.data_dir) / spec.predictions_file)
    checks = pd.read_csv(Path(spec.data_dir) / spec.checks_file)
    meas = checks[checks.role == "proposal"].reset_index(drop=True)
    vs = reg.view
    fit = fit_study(vs)
    chart = fit.estimator.transform(vs.M)
    Z, logv = chart[:, :-1], chart[:, -1]
    Zm = reg.model.trade_space_.transform(meas[list(vs.attrs)].to_numpy(float))[:, :-1]
    fig, axes = plt.subplots(2, 1, figsize=(FIGURE_WIDTH_IN, 8.4))
    for ax, cols in zip(axes, [(0, 1), (0, 2)], strict=True):
        plotting.plot_frontier_coordinates(
            Z[:, list(cols)], logv, band=1.0 / reg.tau,
            targets=preds[[f"pred_z{c + 1}" for c in cols]].to_numpy(), ax=ax,
        )  # fmt: skip
        ax.scatter(Zm[:, cols[0]], Zm[:, cols[1]], marker="D", s=40,
                   color=plotting.CATEGORY_COLORS[3], zorder=5)  # fmt: skip
        for i in range(len(Zm)):
            ax.annotate(str(i + 1), (Zm[i, cols[0]], Zm[i, cols[1]]), xytext=(4, 4),
                        textcoords="offset points")  # fmt: skip
    fig.tight_layout()
    return fig


def with_spec(spec=CUBESAT, **changes):
    """A copy of the spec with fields replaced (the way to point the functions at another table).

    Parameters
    ----------
    spec : CaseSpec
    **changes
        Field names of :class:`CaseSpec` and their new values.

    Returns
    -------
    CaseSpec
    """
    return replace(spec, **changes)
