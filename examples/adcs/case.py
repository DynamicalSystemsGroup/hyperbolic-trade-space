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
(60, 10)
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

    @property
    def names(self):
        """Plain names of the attributes, in column order."""
        return [self.short[a] for a in self.attributes]

    @property
    def category(self):
        """The first covariate (the colour category), or None."""
        return next(iter(self.covariates), None)


_ATTRS = (
    "settling_time_s", "slew_time_s", "pointing_error_deg", "total_mass_kg", "control_effort",
    "power_margin_w", "energy_balance_wh", "eclipse_reserve_wh", "peak_slew_power_w", "dod_eclipse",
)  # fmt: skip
_NAMES = (
    "settling time", "slew time", "pointing error", "total mass", "control effort",
    "power margin", "energy balance", "eclipse reserve", "peak slew power", "depth of discharge",
)  # fmt: skip
_UNITS = ("s", "s", "deg", "kg", "torque.s, proxy", "W", "Wh", "Wh", "W", "fraction")
_ORIENT = (-1, -1, -1, -1, -1, +1, +1, +1, -1, -1)

CUBESAT = CaseSpec(
    name="cubesat attitude determination and control",
    data_dir=HERE / "data",
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
        "four metrics": ("slew_time_s", "pointing_error_deg", "control_effort", "total_mass_kg"),
        "settling time and slew time": ("settling_time_s", "slew_time_s"),
    },
    view="four metrics",
    association_pairs=(
        ("settling time", "total mass"),
        ("slew time", "total mass"),
        ("pointing error", "control effort"),
        ("settling time", "pointing error"),
        ("slew time", "control effort"),
        ("settling time", "slew time"),
    ),
    checks_file="check_designs_cubesat.csv",
    predictions_file="check_predictions_cubesat.csv",
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
        Number of facets; ``K = 1`` is the monomial frontier.
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
    """The exponent of each metric at the fitted frontier, K = 1 or per facet.

    Parameters
    ----------
    study : Study
    fit : Fit

    Returns
    -------
    pandas.DataFrame
        One row per metric; one column ``exponent w`` (K = 1) or ``facet k`` per facet.
    """
    W = np.atleast_2d(fit.estimator.exponents_)
    cols = ["exponent w"] if len(W) == 1 else [f"facet {k + 1}" for k in range(len(W))]
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
        Columns ``K``, ``tau``, ``band 1/tau``, ``objective_``, ``frac_above_``, ``facet rows``,
        ``facet shares``, ``max gap``, ``status``, ``gamma`` (margin), ``radius``, ``bound``.
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
    """Certificate columns of the fits: status, largest facet gap, margin, radius, bound.

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


def _reports(study, fit, band=None, **kw):
    hts, _, _ = _lib()
    band = fit.band if band is None else band
    r = hts.tension_report(fit.estimator, study.M, band=band, **kw)
    return r if isinstance(r, list) else [r]


def _sorted_contending(rep, names):
    order = np.argsort(-rep.contending_exponents)
    return [names[rep.contending_set[i]] for i in order]


def tension_table(study, fit, band=None):
    """Per facet: the contending set (largest exponent first) and the facts of its report.

    Parameters
    ----------
    study : Study
    fit : Fit
    band : float, optional
        Near-frontier band of the report; default ``1 / tau``.

    Returns
    -------
    pandas.DataFrame
        Columns ``facet``, ``n_lemma``, ``near-frontier``, ``contending set``,
        ``largest exponents``.
    """
    _, k_terms, _ = _lib()
    rows = []
    for k, rep in enumerate(_reports(study, fit, band)):
        rows.append({
            "facet": k + 1, "n_lemma": rep.n_lemma, "near-frontier": rep.n_near_frontier,
            "contending set": ", ".join(_sorted_contending(rep, study.names)),
            "largest exponents": k_terms.top(study.names, rep.exponents, 3),
        })  # fmt: skip
    return pd.DataFrame(rows)


def facet_table(study, fits, K=3, band=None):
    """One row of facts per facet of the K-term fit, with the facet's first-order gap.

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
        Columns ``facet``, ``rows``, ``contending set``, ``n_lemma``, ``largest exponents``,
        ``near-frontier``, ``reach beta_k``, ``share``, ``gap G_k``.
    """
    _, k_terms, _ = _lib()
    fit = fits[K]
    est = fit.estimator
    if band is None:
        band = fits[1].band if 1 in fits else fit.band
    sizes = np.bincount(est.facet_, minlength=K) if K > 1 else [len(study.M)]
    out = []
    for k, rep in enumerate(_reports(study, fit, band)):
        out.append({
            "facet": k + 1, "rows": int(sizes[k]),
            "contending set": ", ".join(_sorted_contending(rep, study.names)),
            "n_lemma": rep.n_lemma, "largest exponents": k_terms.top(study.names, rep.exponents),
            "near-frontier": rep.n_near_frontier, "reach beta_k": float(est.log_offset_[k]),
            "share": float(est.facet_share_[k]) if K > 1 else 1.0,
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


def tau_sweep_figure(study, fit):
    """Fraction above V = 1, effective size and exponents across temperature.

    Parameters
    ----------
    study : Study
    fit : Fit
        The selected K = 1 fit (marked on the first two panels).

    Returns
    -------
    matplotlib.figure.Figure
    """
    hts, _, plotting = _lib()
    plt = _plt()
    sweep = tau_sweep(study)
    fin = sweep[np.isfinite(sweep.tau)]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
    axes[0].semilogx(fin.tau, fin.frac_above, "o-", color=plotting.DATA_COLOR)
    axes[0].axhline(study.spec.target_frac, color=plotting.FRONTIER_COLOR, lw=0.8)
    axes[0].set(xlabel="temperature tau", ylabel="fraction above V = 1")
    axes[1].semilogx(fin.tau, fin.n_eff, "o-", color=plotting.DATA_COLOR)
    axes[1].set(xlabel="temperature tau", ylabel="effective sample size")
    for ax in axes[:2]:
        ax.axvline(fit.tau, color=plotting.BAND_COLOR, lw=3)
    W = np.array(
        [
            hts.HyperbolicTradeSpace(temperature=t, random_state=study.spec.seed)
            .fit(study.M)
            .exponents_[0]
            for t in sweep.tau
        ]
    )
    im = axes[2].imshow(W.T, cmap="Greys", aspect="auto", vmin=0, vmax=0.3)
    axes[2].set_xticks(
        range(len(sweep)), [f"{t:.0f}" if np.isfinite(t) else "inf" for t in sweep.tau],
        rotation=60, fontsize=7,
    )  # fmt: skip
    axes[2].set_yticks(range(len(study.names)), study.names, fontsize=7)
    axes[2].set(xlabel="tau")
    fig.colorbar(im, ax=axes[2])
    fig.tight_layout()
    return fig


def log_plane_figure(study, fit, band=None):
    """Log-plane slices of the fit, one per pair of each facet's two largest exponents.

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
        Panel titles name the facets drawn.
    """
    hts, k_terms, plotting = _lib()
    plt = _plt()
    est, M = fit.estimator, study.M
    band = fit.band if band is None else band
    U = np.log(M)
    labels = plotting.facet_labels(est, M)
    pairs = k_terms.slice_pairs(est)
    fig, axes = plt.subplots(1, len(pairs), figsize=(5 * len(pairs), 5.4), squeeze=False)
    for ax, (j, k) in zip(axes[0], pairs, strict=True):
        keep, ws, bs = k_terms._slice(est, U, labels, band, j, k)
        sh = hts.HyperbolicTradeSpace(temperature=fit.tau, n_terms=len(keep))
        sh.exponents_, sh.log_offset_ = np.array(ws), np.array(bs)
        plotting.plot_log_plane(sh, M[:, [j, k]], color=labels, band=band, ax=ax)
        for lim, col in ((ax.set_xlim, j), (ax.set_ylim, k)):
            lo, hi = U[:, col].min(), U[:, col].max()
            lim(lo - 0.1 * (hi - lo), hi + 0.1 * (hi - lo))
        ax.set_xlabel("log of the " + cond_label(study, study.attrs[j]), fontsize=7)
        ax.set_ylabel("log of the " + cond_label(study, study.attrs[k]), fontsize=7)
        noun = "facet" if len(keep) == 1 else "facets"
        names = ", ".join(str(f + 1) for f in keep)
        ax.set_title(
            f"{study.names[j]} and {study.names[k]}\n{noun} {names} drawn",
            fontsize=9,
        )
    fig.tight_layout()
    return fig


def coordinates_figure(study, fit, band=None):
    """Position along the frontier: two pairs of chart coordinates, shaded by facet.

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
    labels = plotting.facet_labels(fit.estimator, study.M) if fit.K > 1 else _colors(study)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, c in zip(axes, [(0, 1), (0, 2)], strict=True):
        if max(c) >= Z.shape[1]:
            c = (0, Z.shape[1] - 1)
        plotting.plot_frontier_coordinates(Z[:, list(c)], logv, color=labels, band=band, ax=ax)
        ax.set_xlabel(f"Z{c[0]} (log-ratio coordinate along the frontier, dimensionless)")
        ax.set_ylabel(f"Z{c[1]} (log-ratio coordinate along the frontier, dimensionless)")
    fig.tight_layout()
    return fig


def tension_figure(study, fit, band=None):
    """Association among the near-frontier designs, one map per facet.

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
    reps = _reports(study, fit, band)
    fig, axes = plt.subplots(1, len(reps), figsize=(7 * len(reps), 6.4), squeeze=False)
    plotting.plot_tensions(reps if len(reps) > 1 else reps[0], names=study.names,
                           ax=axes[0] if len(reps) > 1 else axes[0][0])  # fmt: skip
    for ax in axes[0]:
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=7)
    fig.tight_layout()
    return fig


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
        1, len(spec.regimes), figsize=(7 * len(spec.regimes), 6), squeeze=False
    )
    for ax, regime in zip(axes[0], spec.regimes, strict=True):
        st = load_study(regime, spec, n_max)
        rep = _reports(st, fit_study(st))[0]
        plotting.plot_tensions(rep, names=st.names, ax=ax)
        ax.set_title(regime + ": " + ax.get_title(), fontsize=9)
        plt.setp(ax.get_xticklabels(), rotation=40, ha="right", fontsize=7)
    fig.tight_layout()
    return fig


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
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, cols in zip(axes, [(0, 1), (0, 2)], strict=True):
        plotting.plot_frontier_coordinates(
            Z[:, list(cols)], logv, band=1.0 / reg.tau,
            targets=preds[[f"pred_z{c + 1}" for c in cols]].to_numpy(), ax=ax,
        )  # fmt: skip
        ax.scatter(Zm[:, cols[0]], Zm[:, cols[1]], marker="D", s=40,
                   color=plotting.CATEGORY_COLORS[3], zorder=5)  # fmt: skip
        for i in range(len(Zm)):
            ax.annotate(str(i + 1), (Zm[i, cols[0]], Zm[i, cols[1]]), xytext=(4, 4),
                        textcoords="offset points", fontsize=8)  # fmt: skip
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
