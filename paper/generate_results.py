"""Appendix D: extended results, what the method found in the table of metrics.

Each table cites its dataset by the label that Appendix C defines
(:data:`generate_model.DATASET_LABELS`) and repeats nothing else from C: no variable range,
constraint, scenario constant or conditioning rule appears here (R-26). The tables are produced by
calls into the case module and the package; none is typed.
"""

from __future__ import annotations

import itertools
from functools import cache

import case
import numpy as np
from generate_model import DATASET_LABELS, PLANTED, _associations, _one_axis_sentence, planted_table
from paper_common import Md, frame_table, md_table
from paper_stability import residue_bound, stable, stable_frame, summary


def _cite(regime) -> str:
    return f"Dataset {DATASET_LABELS[regime]}"


# The temperature of the planted-data fit: a fit setting, stated with the record it produces.
PLANTED_TAU = 20.0


@cache
def _study(regime):
    return case.load_study(regime)


@cache
def _fits(regime):
    return case.k_fits(_study(regime))


def _studies():
    return {r: _study(r) for r in case.CUBESAT.regimes}


def _t(df, prefix, key=None):
    return frame_table(stable_frame(df, prefix, key))


def _exponents(df, prefix):
    """An exponent table as the datasets allow, with an exact zero spelled as a residue is.

    Both are an exponent under the participation threshold (``RESIDUE``); the solver leaves either
    an exact 0 or a residue, and the table has one spelling for it.
    """
    out = stable_frame(df, prefix, "metric")
    for col in out.columns:
        if col != "metric":
            out[col] = [
                residue_bound(v, zero=True) if isinstance(v, float) else v for v in out[col]
            ]
    return out


def _terms(regime, ft, K=3):
    """The K-term table with each moving quantity stated as the datasets allow.

    ``ft`` is the K-term table in the estimator's order. The leading exponents
    are named in the order they hold in every dataset; their values are those of the exponent
    table, to the digits that held.
    """
    table = stable_frame(ft, f"D terms K={K} | {regime}", "term")
    three = lambda v: f"{v:.3f}"  # noqa: E731
    for i, text in enumerate(table["largest exponents"]):
        label = int(ft["term"].iloc[i])
        pairs = [part.rsplit(" ", 1)[0] for part in text.split(", ")]
        table.iat[i, table.columns.get_loc("largest exponents")] = ", ".join(
            f"{name} " + stable(f"D exponents K={K} | {regime} | {name} | term {label}", three)
            for name in pairs
        )
    return table


def temperature_selection() -> Md:
    """The K = 1 fit across temperatures, per regime.

    Returns
    -------
    Md
    """
    parts = [
        f"{_cite(r)}:\n\n" + _t(case.tau_sweep(s), f"D tau_sweep | {r}")
        for r, s in _studies().items()
    ]
    return Md("\n\n".join(parts))


def k_diagnostics() -> Md:
    """The K = 1, 2, 3 diagnostic table with the certificate columns, per regime.

    Returns
    -------
    Md
        Temperature re-selected at each K; the certificate columns are the solver's record.
    """
    parts = []
    for r, s in _studies().items():
        kt = case.k_table(s, _fits(r))
        parts.append(f"{_cite(r)}:\n\n" + _t(kt, f"D k_table | {r}", "K"))
    return Md("\n\n".join(parts))


def exponents_and_terms() -> Md:
    """Exponents per metric at K = 1, at the case's K and at K = 3, and the term tables, per regime.

    Returns
    -------
    Md
    """
    parts = []
    for r, s in _studies().items():
        k1, kc = _fits(r)[1], _fits(r)[case.CASE_K]
        ftc = case.term_table(s, _fits(r), K=case.CASE_K)
        exp3 = case.exponent_table(s, _fits(r)[3])
        ft3 = case.term_table(s, {1: k1, 3: _fits(r)[3]})
        parts.append(
            f"{_cite(r)}, K = 1:\n\n"
            + frame_table(_exponents(case.exponent_table(s, k1), f"D exponents K=1 | {r}"))
            + f"\n\n{_cite(r)}, K = {case.CASE_K}:\n\n"
            + frame_table(
                _exponents(case.exponent_table(s, kc), f"D exponents K={case.CASE_K} | {r}")
            )
            + f"\n\n{_cite(r)}, K = {case.CASE_K}, per term:\n\n"
            + frame_table(_terms(r, ftc, case.CASE_K))
            + _thin_terms(ftc)
            + f"\n\n{_cite(r)}, K = 3:\n\n"
            + frame_table(_exponents(exp3, f"D exponents K=3 | {r}"))
            + f"\n\n{_cite(r)}, K = 3, per term:\n\n"
            + frame_table(_terms(r, ft3))
            + _thin_terms(ft3)
            + _summed_text(r, _fits(r))
        )  # fmt: skip
    return Md("\n\n".join(parts) + "\n\n" + _one_axis_sentence())


def _thin_terms(ft) -> str:
    """One sentence per term whose near-frontier designs miss the guard of the association reading.

    The row of such a term stands: its exponents, cell, share and contending set are the fit's;
    only the association reading, which needs the rows, is not made (``case.has_reading``).
    """
    out = ""
    for label, n in zip(ft["term"], ft["near-frontier"], strict=True):
        if int(n) < case.MIN_NEAR_FRONTIER:
            reason = case.thin_reason(n)
            out += (
                f"\n\nTerm {int(label)}: {reason}; its row above is the fit's, and its "
                "association cells are empty."
            )
    return out


def regime_comparison() -> Md:
    """The regimes through the identical pipeline, side by side.

    Returns
    -------
    Md
    """
    cites = ", ".join(DATASET_LABELS[r] for r in case.CUBESAT.regimes)
    table = regime_table()
    # The dataset file names and sizes are Appendix C's; this table keeps what the method found.
    table = table[~table["quantity"].isin(["dataset", "feasible n"])]
    return Md(f"Datasets {cites}:\n\n" + frame_table(table) + "\n\n" + _one_axis_sentence())


def termination_records() -> Md:
    """The solver's termination records for the planted data and the case.

    Returns
    -------
    Md
        Status, largest term gap, margin, radius and the Corollary bound, as printed by the code,
        and the planted terms' recovery (largest exponent deviation after matching terms).
    """
    import k_terms

    X, info = planted_table()
    est = k_terms.fit_k(X, PLANTED["n_terms"], PLANTED_TAU, 0)
    planted_rec = k_terms.summary({PLANTED["n_terms"]: est}, X)
    W, P = np.atleast_2d(est.exponents_), np.asarray(info["exponents"], float)
    dev = min(
        float(np.abs(W[list(perm)] - P).max())
        for perm in itertools.permutations(range(len(P)))
    )  # fmt: skip
    parts = [f"{_cite(r)}:\n\n" + _t(case.certificate_table(_fits(r)), f"certificate | {r}", "K")
             for r in _studies()]  # fmt: skip
    for col in ("max gap", "bound"):  # residues of the polish: a bound, not digits
        planted_rec[col] = [residue_bound(v) for v in planted_rec[col]]
    parts.append(f"Dataset {DATASET_LABELS['planted']}, temperature {PLANTED_TAU:g}:\n\n"
                 + frame_table(planted_rec))  # fmt: skip
    parts.append(md_table(["Planted terms", "Largest exponent deviation after matching terms"],
                          [[len(P), dev]]))  # fmt: skip
    return Md("\n\n".join(parts))


def nondominated() -> Md:
    """Nondominated counts on all attributes and on each named view, per regime.

    Returns
    -------
    Md
    """
    parts = [f"{_cite(r)}:\n\n" + _t(case.nondominated_counts(s), f"nondominated | {r}", "view")
             for r, s in _studies().items()]  # fmt: skip
    return Md("\n\n".join(parts))


def propose_predict_check() -> Md:
    """Propose, predict, check: predicted against measured chart position of each proposal.

    Returns
    -------
    Md
        The table for the primary regime, mixed results included.
    """
    s = case.load_study("primary")
    reg = case.fit_regressor(s)
    return Md(f"{_cite('primary')}:\n\n" + _t(case.predict_check(s, reg), "predict", "proposal"))


def sensitivity_variants() -> Md:
    """The K = 1 fit under variants of the pipeline's choices, per regime.

    Returns
    -------
    Md
        The target fraction halved and doubled, the robust scaler and each named view, against the
        baseline, with how many metrics of the baseline's contending set each variant shares.
    """
    parts = [f"{_cite(r)}:\n\n" + _t(case.sensitivity_table(s), f"D sensitivity | {r}", "variant")
             for r, s in _studies().items()]  # fmt: skip
    return Md("\n\n".join(parts))


def refits_by_category() -> Md:
    """The K = 1 fit refit within each level of the first covariate, per regime.

    Returns
    -------
    Md
    """
    parts = [f"{_cite(r)}:\n\n" + _t(case.category_refits(s), f"D refits | {r}", "wheel_class")
             for r, s in _studies().items()]  # fmt: skip
    return Md("\n\n".join(parts))


def candidate_designs() -> Md:
    """The measured candidate designs scored against the K = 1 fit of the primary regime.

    Returns
    -------
    Md
    """
    return Md(
        f"{_cite('primary')}:\n\n"
        + frame_table(
            stable_frame(
                case.candidate_table(_study("primary"), _fits("primary")[1]),
                "candidate",
                "candidate",
            )
        )
    )


def regime_table():
    """``case.regime_comparison()`` with the moving quantities stated as the datasets allow.

    The rows that join several numbers in one string are rebuilt from the quantities the results
    file holds: the effective sample size and the fraction above V = 1, the near-frontier count and
    the Pearson and Spearman associations.
    """
    table = case.regime_comparison().copy()
    rows = table.set_index("quantity")
    for regime in case.CUBESAT.regimes:
        tau, _, _ = rows.at["tau, frac_above_, n_eff_", regime].split(", ")
        frac = stable(f"fit | {regime} K=1 | frac_above_", lambda v: f"{v:.3f}")
        n_eff = stable(f"fit | {regime} K=1 | n_eff_", lambda v: f"{v:.1f}")
        rows.at["tau, frac_above_, n_eff_", regime] = f"{tau}, {frac}, {n_eff}"
        band, _ = rows.at["band 1/tau, near-frontier designs", regime].split(", ")
        near = stable(f"fit | {regime} K=1 | near-frontier designs")
        rows.at["band 1/tau, near-frontier designs", regime] = f"{band}, {near}"
        for a, b in (
            q.split(", ")
            for q in rows.index
            if q.count(", ") == 1
            and q[0].islower()
            and f"tension | {regime} | {q} | pearson" in _names()
        ):
            q = f"{a}, {b}"
            pe = _signed(stable(f"tension | {regime} | {q} | pearson", lambda v: f"{v:+.2f}"))
            sp = _signed(stable(f"tension | {regime} | {q} | spearman", lambda v: f"{v:+.2f}"))
            rows.at[q, regime] = f"{pe} ({sp})"
    return rows.reset_index()


def _signed(text):
    """Every number of a stable text with its sign (``+0.90 to +0.91``)."""
    return " to ".join(p if p.startswith(("-", "+")) else f"+{p}" for p in text.split(" to "))


def _names():
    from paper_stability import summary

    return summary()["quantities"]


# -- D.11: stability of the conclusions under rounding-level jitter ----------------------------

CONCLUSIONS = (
    ("the contending sets (K = 1 and each term at K = 3)", ("contending |",), ""),
    ("each term's leading metrics", ("leading |",), ""),
    ("the signs of the reported tensions", ("tension |",), "sign"),
    ("the fit temperatures, to the printed 0.1", ("tau |",), ""),
    ("the certificate statuses", ("certificate |",), "| status"),
    ("the pass or miss of each check design", ("predict |", "predict, committed checks |"),
     "outcome"),
    ("the count of nondominated designs on all attributes",
     ("nondominated |",), "| all attributes | nondominated"),
)  # fmt: skip


def _verdict_rows():
    qs = summary()["quantities"]
    rows = []
    for label, prefixes, suffix in CONCLUSIONS:
        names = [n for n in qs if n.startswith(prefixes) and n.endswith(suffix)]
        rows.append([label, len(names), all(qs[n]["identical"] for n in names)])
    return rows


def _moving_rows():
    """The reported quantities that move at the printed precision, with their printed text."""
    q = summary()["quantities"]
    four = lambda v: format(v, ".4g")  # noqa: E731
    groups = []
    for r in case.CUBESAT.regimes:
        groups += [
            (f"nondominated, {v}, {r}", f"nondominated | {r} | {v} | nondominated", None)
            for v in case.CUBESAT.views
        ]
        groups += [
            (f"fraction above V = 1, K = 1, {r}", f"fit | {r} K=1 | frac_above_", four),
            (f"effective sample size, K = 1, {r}", f"fit | {r} K=1 | n_eff_", four),
            (f"near-frontier designs, K = 1, {r}", f"fit | {r} K=1 | near-frontier designs", None),
        ]
        groups += [
            (f"{kind}, {pair}, {r}", f"tension | {r} | {pair} | {kind}", four)
            for pair in (f"{a}, {b}" for a, b in case.CUBESAT.association_pairs)
            for kind in ("pearson", "spearman")
        ]
        groups += [
            (f"term {k} share, K = 3, {r}", f"D terms K=3 | {r} | {k} | share", four)
            for k in (1, 2, 3)
        ]
        groups += [
            (f"{what}, K = {K}, {r}", f"certificate | {r} | {K} | {col}", four)
            for K in (2, 3)
            for what, col in (("largest term gap", "max gap"), ("margin", "gamma"),
                              ("radius", "radius"))
        ]  # fmt: skip
    rows = []
    for label, name, orig in groups:
        e = q.get(name)
        if not e or "min" not in e:
            continue
        fmt = orig or (lambda v: str(round(v)))
        if fmt(e["min"]) == fmt(e["max"]):
            continue
        cols = [
            residue_bound(e[k]) if abs(e[k]) < 1e-12 else fmt(e[k])
            for k in ("committed", "min", "max")
        ]
        rows.append([label, *cols, stable(name, orig)])
    return rows


def stability() -> Md:
    """Which conclusions are identical across the datasets regenerated under jitter, and which
    printed quantities move.

    Returns
    -------
    Md
        A table with the verdict on each conclusion and a table of the printed quantities that
        move, read from the committed results file of ``sensitivity.py``.
    """
    s = summary()
    eps, n = s["perturbation"]["relative_half_width"], len(s["seeds"])
    n_all = len(s["quantities"])
    cites = " and ".join(DATASET_LABELS[r] for r in case.CUBESAT.regimes)
    moving = [e for e in s["quantities"].values() if "min" in e and not e["identical"]]
    head = (
        "The control effort and the saturated fraction are sums over the accepted steps of an "
        "adaptive integration and the settling time is detected on its dense solution, so a "
        f"relative change of {eps:g} in a design variable moves them (gap G-17). Datasets "
        f"{cites} and the six check designs were regenerated {n} times with `Kp`, `Kd`, the "
        "panel span and the battery capacity of every design multiplied by 1 + e, e uniform in "
        f"[-{eps:g}, {eps:g}], and every quantity this paper reports was recomputed ({n_all} "
        f"quantities, of which {len(moving)} numbers move at all). The regenerations ran on the "
        "authors' machine and the committed data in the environment of record, so a range also "
        "holds the two platforms' difference. A quantity that moves is printed in this paper to "
        f"the digits that held in all {n + 1} datasets (the committed one and the {n} "
        "regenerated), as a range where not even two digits did, and as a bound where it is a "
        "numerical residue."
    )
    verdict = md_table(
        ["Conclusion", "Quantities compared", f"Across the committed data and {n} regenerations"],
        [[a, b, "identical" if c else "differs"] for a, b, c in _verdict_rows()],
    )
    moving_tab = md_table(
        ["Quantity", "Committed", "Minimum", "Maximum", "Printed in this paper as"],
        _moving_rows(),
    )
    return Md(
        f"{head}\n\n{verdict}\n\nThe printed quantities that move, with the committed value, the "
        f"minimum and maximum over the {n + 1} datasets and the text this paper prints:\n\n"
        f"{moving_tab}"
    )


OWN_ROWS_SEEDS = 20
"""Planted tables for the own-rows comparison (the spike's twenty seeds, three terms each)."""
OWN_ROWS_TOLERANCE = 0.05
"""A term is recovered when its largest exponent error is within this."""


def own_rows_refit() -> Md:
    """The refit of a term on its own rows against the support refit, given the true labels.

    Planted tables of 400 rows, 4 metrics and 3 terms (``make_frontier_data``, seeds 0 to 19)
    are fitted once per term with the true labels given, so the alternation plays no part: the
    plain ``K = 1`` fit on the term's own cell, and the support refit that the solver uses (the
    fit of all rows with the log-metrics centred at the term's mean). The same comparison is
    ``docs/superpowers/notes/spike-facet-refit/bench_oracle.py`` (methods A and B).

    Returns
    -------
    Md
        Per temperature: the terms, the terms each refit recovers to within
        :data:`OWN_ROWS_TOLERANCE` and the largest exponent error of each.
    """
    from hyperbolic_trade_space import make_frontier_data
    from hyperbolic_trade_space.solvers import solve_slsqp

    rows = []
    for tau in (np.inf, 50.0):
        err = {"own": [], "support": []}
        for seed in range(OWN_ROWS_SEEDS):
            X, info = make_frontier_data(400, 4, n_terms=3, random_state=seed)
            U, lab = np.log(X), np.asarray(info["term"])
            for k, planted in enumerate(np.asarray(info["exponents"])):
                mine = U[lab == k]
                w_own = solve_slsqp(mine, tau).w
                w_sup = solve_slsqp(U - mine.mean(axis=0), tau).w
                err["own"].append(float(np.abs(w_own - planted).max()))
                err["support"].append(float(np.abs(w_sup - planted).max()))
        n = len(err["own"])
        count = {k: sum(e <= OWN_ROWS_TOLERANCE for e in v) for k, v in err.items()}
        rows.append([
            "infinity" if np.isinf(tau) else f"{tau:g}", n,
            f"{count['own']} of {n}", f"{max(err['own']):.2f}",
            f"{count['support']} of {n}", f"{max(err['support']):.3f}",
        ])  # fmt: skip
    return Md(
        f"Dataset {DATASET_LABELS['planted']}, the generator of Appendix C at 400 rows and seeds 0 "
        f"to {OWN_ROWS_SEEDS - 1}, the true labels given:\n\n"
        + md_table(
            [
                "Temperature",
                "Planted terms",
                "Own-rows refit recovers",
                "Largest error, own rows",
                "Support refit recovers",
                "Largest error, support",
            ],
            rows,
        )
    )


def conditioning_diagnostic() -> Md:
    """The conditioning of the exponents, ``conditioning_``, per regime, K and term.

    Returns
    -------
    Md
        The smallest eigenvalue of the restricted Hessian of the objective at each term's fit, to
        two digits: a small value flags a nearly flat direction (weak identifiability of the
        exponents); a read-only diagnostic of the estimator.
    """
    parts = []
    for r in _studies():
        rows = [
            [K, k + 1, f"{v:.2g}"]
            for K, f in _fits(r).items()
            for k, v in enumerate(np.atleast_1d(f.estimator.conditioning_))
        ]
        parts.append(
            f"{_cite(r)}:\n\n"
            + md_table(["K", "Term", "`conditioning_` (smallest eigenvalue)"], rows)
        )
    return Md("\n\n".join(parts))


# -- D.14: the planted example, twenty tables --------------------------------------------------

RECOVERY_SEEDS = 20
"""Planted tables for the recovery count (``make_frontier_data``, seeds 0 to 19)."""
RECOVERY_TAUS = (np.inf, 50.0)
"""The exact maximum and a working temperature."""
RECOVERY_ROWS = 400
"""Rows of each planted table (four metrics, three terms)."""
RECOVERY_RIGHT = 0.9
"""A table is recovered when at least this fraction of its frontier rows lie on the right term."""


@cache
def recovery_runs() -> tuple:
    """The fit of every planted table at every temperature, as the solver's defaults make it.

    ``HyperbolicTradeSpace(n_terms=3, random_state=0)`` with five restarts, the planted terms
    matched to the fitted ones by the permutation that minimizes the largest exponent error. A
    table is recovered when that error is under :data:`OWN_ROWS_TOLERANCE` and at least
    :data:`RECOVERY_RIGHT` of its frontier rows lie on the right term.

    Returns
    -------
    tuple of dict
        Per table and temperature: ``seed``, ``tau``, ``rows_on_thinnest`` (frontier rows of the
        planted term with fewest), ``error``, ``right``, ``status``, ``max_gap`` (the largest
        term gap at termination), ``tol`` (the solver tolerance it is read against) and
        ``recovered``.
    """
    from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data

    out = []
    for tau in RECOVERY_TAUS:
        for seed in range(RECOVERY_SEEDS):
            X, info = make_frontier_data(RECOVERY_ROWS, 4, n_terms=3, random_state=seed)
            planted = np.asarray(info["exponents"], float)
            truth, front = np.asarray(info["term"]), np.asarray(info["frontier_mask"])
            est = HyperbolicTradeSpace(temperature=tau, n_terms=3, random_state=0).fit(X)
            fitted = np.atleast_2d(est.exponents_)
            error, perm = min(
                (float(np.abs(fitted[list(p)] - planted).max()), p)
                for p in itertools.permutations(range(3))
            )
            back = {fit_k: k for k, fit_k in enumerate(perm)}
            mapped = np.array([back[f] for f in np.asarray(est.cell_)])
            right = float((mapped[front] == truth[front]).mean())
            out.append({
                "seed": seed, "tau": tau, "error": error, "right": right,
                "rows_on_thinnest": int(min((front & (truth == k)).sum() for k in range(3))),
                "status": est.termination_.status,
                "max_gap": float(est.termination_.max_gap),
                "tol": float(est.tol),
                "recovered": error < OWN_ROWS_TOLERANCE and right >= RECOVERY_RIGHT,
            })  # fmt: skip
    return tuple(out)


def _tau_name(tau) -> str:
    return "infinity" if np.isinf(tau) else f"{tau:g}"


def planted_recovery() -> Md:
    """Does the fit recover a known answer: twenty planted tables, at two temperatures.

    Only what is the same on every platform is printed. At the exact maximum a row of the frontier
    can lie on two term planes (gap G-10), so the status a failing fit stops with and its error
    values follow the platform's tie-breaking and are not printed; at temperature 50 the status
    and the errors are the same on macOS arm64 and Linux amd64 and are printed.

    Returns
    -------
    Md
        The count of tables recovered at each temperature and, for each table not recovered at
        either, the frontier rows of its thinnest planted term, whether it was recovered at the
        exact maximum and at temperature 50, and at temperature 50 the solver's status, the largest
        exponent error and the share of frontier rows on the right term.
    """
    runs = recovery_runs()
    hot, warm = RECOVERY_TAUS
    summary_rows = []
    for tau in RECOVERY_TAUS:
        mine = [r for r in runs if r["tau"] == tau]
        bad = [r for r in mine if not r["recovered"]]
        summary_rows.append([
            _tau_name(tau), len(mine), f"{len(mine) - len(bad)} of {len(mine)}",
            ", ".join(str(r["seed"]) for r in bad) or "none",
        ])  # fmt: skip
    by = {(r["seed"], r["tau"]): r for r in runs}
    seeds = sorted({r["seed"] for r in runs if not r["recovered"]})
    yes_no = lambda r: "yes" if r["recovered"] else "no"  # noqa: E731
    failures = [
        [s, by[s, hot]["rows_on_thinnest"], yes_no(by[s, hot]), yes_no(by[s, warm]),
         by[s, warm]["status"], f"{by[s, warm]['error']:.2f}", f"{by[s, warm]['right']:.2f}"]
        for s in seeds
    ]  # fmt: skip
    thin = sorted({r["rows_on_thinnest"] for r in runs if r["recovered"]})
    tol = {r["tol"] for r in runs}.pop()
    below = sum(r["max_gap"] < tol for r in runs)
    cap_above = sum(r["status"] == "iteration_cap" and r["max_gap"] >= tol for r in runs)
    return Md(
        f"Dataset {DATASET_LABELS['planted']}, the generator of Appendix C at {RECOVERY_ROWS} "
        f"rows, 4 metrics and 3 terms, seeds 0 to {RECOVERY_SEEDS - 1}, the solver's defaults "
        f"(five restarts, `random_state = 0`). A table is recovered when the largest error of "
        f"the exponents, after matching fitted to planted terms, is under {OWN_ROWS_TOLERANCE} "
        f"and at least {RECOVERY_RIGHT:.0%} of its frontier rows lie on the right term.\n\n"
        + md_table(["Temperature", "Planted tables", "Recovered", "Seeds not recovered"],
                   summary_rows)
        + "\n\nThe tables not recovered, with the frontier rows of their thinnest planted term "
        "(a term needs at least 5 frontier rows, one more than there are metrics, to be "
        "determined by them), whether each was recovered at the exact maximum and at temperature "
        f"{warm:g}, and at temperature {warm:g} the solver's status, the largest exponent error "
        "and the share of frontier rows on the right term:\n\n"
        + md_table(["Seed", "Frontier rows, thinnest term", "Recovered at the exact maximum",
                    f"Recovered at temperature {warm:g}", f"Status at {warm:g}",
                    f"Largest error at {warm:g}", f"Frontier rows on the right term at {warm:g}"],
                   failures)
        + "\n\nAt the exact maximum the fit of each of these tables stops without a margin "
        "(`stationary_without_margin`) or at the iteration cap, depending on the platform, "
        "and its errors move with it, so neither is printed: a frontier row on two term planes "
        "ties at the exact maximum and the platform's argmax and linear-program vertex choice "
        "resolve the tie (gap G-10). Whichever status a fit stopped with, its largest term gap "
        f"at termination was below `tol` ({tol:g}) in {below} of the {len(runs)} fits (level 2, "
        "numerical stationarity, L12), so a stop at the iteration cap is the labels not settling "
        f"and not a term left unsolved; {cap_above or 'none'} of the fits stopped at the cap with "
        "a gap at or above `tol`. What does not depend on the platform is the count "
        f"and the seeds: {len(runs) // len(RECOVERY_TAUS) - len(seeds)} of {RECOVERY_SEEDS} "
        "tables were recovered, and the seeds above failed, at both temperatures on macOS arm64 "
        f"and on Linux amd64. Every table recovered has at least {min(thin)} frontier rows on "
        f"each planted term. At temperature {warm:g} the status and the errors, printed to two "
        "digits, were the same on both platforms."
    )  # fmt: skip


# -- D.15: choosing K for the case -----------------------------------------------------------------


@cache
def choosing_k_tables() -> dict:
    """The choosing-K table of each regime (:func:`case.choosing_k_table`), fitted once."""
    return {r: case.choosing_k_table(_study(r), _fits(r)) for r in _studies()}


def choosing_k() -> Md:
    """The paper's choosing-K checks on the case, per regime, with the K they pick.

    Returns
    -------
    Md
        Per regime a table with one row per K: the mean slack at the K = 1 temperature and its
        drop, the thinnest term's share at that temperature and at the K's own, and the movement
        under resampling; then the K the checks pick (:func:`case.chosen_k`).
    """
    parts = []
    for r, t in choosing_k_tables().items():
        tau1 = _fits(r)[1].tau
        dash = lambda v, f: "-" if np.isnan(v) else format(v, f)  # noqa: E731
        rows = [
            [int(x["K"]), format(x["mean slack"], ".3f"), dash(x["drop"], ".3f"),
             format(x["thinnest share"], ".2f"), format(x["thinnest share, own tau"], ".2f"),
             dash(x["movement"], ".2f")]
            for _, x in t.iterrows()
        ]  # fmt: skip
        head = ["K", f"`mean_slack_` at the K = 1 temperature, {tau1:.1f}",
                "Drop from the K before", "Thinnest term's share, same temperature",
                "Thinnest term's share, K's own", "Largest movement under resampling"]  # fmt: skip
        parts.append(
            f"{_cite(r)}:\n\n"
            + md_table(head, rows)
            + f"\n\nThe checks pick K = {case.chosen_k(t)}."
        )
    return Md("\n\n".join(parts))


# -- D.8 (margin): how to read the size of a margin ------------------------------------------------


def margin_reading() -> Md:
    """The assignment margin and stable radius against the band and the median margin.

    Returns
    -------
    Md
        Per regime and K > 1: the margin, the stable radius, the band 1/tau, and the median over
        the designs of the gap between best and second-best term score.
    """
    parts = []
    for r in _studies():
        rows = []
        for K in (2, 3):
            rows.append([
                K,
                stable(f"certificate | {r} | {K} | gamma"),
                stable(f"certificate | {r} | {K} | radius"),
                stable(f"D k_table | {r} | {K} | band 1/tau"),
                stable(f"margin | {r} | {K} | median margin", lambda v: f"{v:.3f}"),
            ])  # fmt: skip
        parts.append(
            f"{_cite(r)}:\n\n"
            + md_table(["K", "Margin (gamma)", "Stable radius", "Band 1/tau",
                        "Median best-minus-second-best term score"], rows)
        )  # fmt: skip
    return Md("\n\n".join(parts))


# -- D.16: chaining with PCA -----------------------------------------------------------------------


def pca_chain() -> Md:
    """Principal directions of the near-frontier chart coordinates, on the primary regime.

    Returns
    -------
    Md
        The share of spread along each of the first three directions and the metrics that load
        most on it, signed with the largest loading positive; the tension report's own analysis.
    """
    study, fits = _study("primary"), _fits("primary")
    table = case.pca_directions(study, fits[1])
    rows = []
    for row in table.itertuples():
        share = stable(f"pca | primary | {row.direction} | share of spread", lambda v: f"{v:.3f}")
        loads = []
        for rank, part in enumerate(row._3.split(", "), 1):
            name = part.rsplit(" ", 1)[0]
            value = _signed(
                stable(f"pca | primary | {row.direction} | loading {rank}", lambda v: f"{v:+.2f}")
            )
            loads.append(f"{name} {value}")
        rows.append([row.direction, share, ", ".join(loads)])
    return Md(
        f"{_cite('primary')}, K = 1, designs with |log V| under the band 1/tau:\n\n"
        + md_table(["Direction", "Share of the spread of the chart coordinates",
                    "Leading loadings on the metrics"], rows)
    )  # fmt: skip


# ---- the WP23 close-out: associations of every pair, the requirements, the design sets ----------
def _summed_text(regime, fits) -> str:
    """The summed exponent reading of the named pairs, or nothing when none is named."""
    pairs = case.one_axis_pairs(_associations(regime))
    if not pairs:
        return ""
    s = _study(regime)
    ks = (1, case.CASE_K, 3)
    parts = [frame_table(case.summed_exponents(s, fits[K], pairs), floatfmt=".3f") for K in ks]
    where = ", ".join(f"K = {K}" for K in ks)
    return f"\n\n{_cite(regime)}, named pairs summed per term ({where}):\n\n" + "\n\n".join(parts)


def requirements_at_the_frontier() -> Md:
    """The six requirements read after the fit of record, per dataset.

    Returns
    -------
    Md
        ``case.requirements_table`` on the K = 1 fit of each dataset: the limit, the share of the
        feasible designs that pass it, the near-frontier designs it excludes, the exponent, the
        price at the frontier (log V and band widths) and the two largest elasticities; a last row
        reads the six jointly.
    """
    parts = []
    for r, s in _studies().items():
        t = case.requirements_table(s, _fits(r)[1]).copy()
        t["pass (feasible)"] = [f"{100 * x:.1f} %" for x in t["pass (feasible)"]]
        for col, fmt in (("K = 1 exponent", ".3f"), ("price (log V)", ".4f"),
                         ("price (bands)", ".2f")):  # fmt: skip
            t[col] = ["" if np.isnan(x) else format(0.0 if abs(x) < 5e-5 else x, fmt)
                      for x in t[col]]  # fmt: skip
        parts.append(f"{_cite(r)}:\n\n" + frame_table(t))
    return Md("\n\n".join(parts))


@cache
def _design_sets():
    return {r: case.design_sets(r) for r in case.CUBESAT.regimes}


def design_sets_comparison() -> Md:
    """Constrained against unconstrained: the fit on all designs, the feasible ones, and the
    feasible ones that meet the four performance thresholds, per dataset, in one conditioning.

    Returns
    -------
    Md
        ``case.design_sets_table`` (size, temperature, the one-term contending set and leading
        exponents, the zero set, the three terms with their shares) and
        ``case.design_sets_placement`` (the baseline configuration and the check designs scored
        by each set's one-term fit: log V, in band widths, and the share of the set's designs
        below it).
    """
    sets = _design_sets()
    fits_t = case.design_sets_table(sets=sets).copy()
    fits_t["regime"] = [DATASET_LABELS[r] for r in fits_t["regime"]]
    fits_t["tau"] = [f"{x:.1f}" for x in fits_t["tau"]]
    fits_t = fits_t.rename(columns={"regime": "dataset"})
    place = case.design_sets_placement(sets=sets).copy()
    place["regime"] = [DATASET_LABELS[r] for r in place["regime"]]
    place = place.rename(columns={"regime": "dataset"})
    cites = ", ".join(DATASET_LABELS[r] for r in case.CUBESAT.regimes)
    return Md(
        f"Datasets {cites}. The fit on each design set:\n\n"
        + frame_table(fits_t)
        + "\n\nThe baseline configuration and the check designs in each set's one-term fit, "
        "log V (in band widths, share of the set's designs below):\n\n" + frame_table(place)
    )


def injected_noise() -> Md:
    """The noise-ridge corollary (L20) against measurement error injected into the cubesat data.

    The data of record carry no noise of their own; ``examples/adcs/noise_injection.py`` multiplies
    each raw attribute by ``exp(delta z)`` (a design choice of this experiment), conditions the
    table again and refits at the clean fit's temperature.

    Returns
    -------
    Md
        Per regime and ``delta``: ``conditioning_`` of the clean fit, the largest component of the
        shift the corollary predicts, of the measured mean shift and of its spread over the
        draws, and the contending-set overlap.
    """
    import noise_injection

    rows = []
    for regime in case.CUBESAT.regimes:
        rows += [[DATASET_LABELS[regime], *r[1:]] for r in noise_injection.regime_rows(regime)[1]]
    return Md(
        f"Datasets {' and '.join(DATASET_LABELS[r] for r in case.CUBESAT.regimes)}: the data of "
        "record carry no noise of their own; the noise is injected as a design choice "
        "of this experiment (`examples/adcs/noise_injection.py`): each raw attribute is multiplied "
        "by exp(delta z), z standard normal, the table is conditioned again and refitted at the "
        "clean fit's temperature, and the measured columns are over eight draws. The predicted "
        "shift is the corollary's formula on the support of the clean fit (its exponents above "
        "0.001), where the corollary holds while the zero exponents stay zero; the last column "
        "shows where noise lifts one. The noise of each metric is delta divided by the log spread "
        "of its attribute. What the table shows belongs "
        "to the fit and the conditioning together.\n\n"
        + md_table(list(noise_injection.COLUMNS), rows)
    )
