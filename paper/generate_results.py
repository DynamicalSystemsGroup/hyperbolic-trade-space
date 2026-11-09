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
from generate_model import DATASET_LABELS, PLANTED, planted_table
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


def _facets(regime, study, k1, k3):
    """The K = 3 facet table with each moving quantity stated as the datasets allow.

    The leading exponents are named in the order they hold in every dataset; their values are those
    of the exponent table, to the digits that held.
    """
    table = stable_frame(
        case.facet_table(study, {1: k1, 3: k3}), f"D facets K=3 | {regime}", "facet"
    )
    three = lambda v: f"{v:.3f}"  # noqa: E731
    for i, text in enumerate(table["largest exponents"]):
        pairs = [part.rsplit(" ", 1)[0] for part in text.split(", ")]
        table.iat[i, table.columns.get_loc("largest exponents")] = ", ".join(
            f"{name} " + stable(f"D exponents K=3 | {regime} | {name} | facet {i + 1}", three)
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
        parts.append(f"{_cite(r)}:\n\n" + _t(case.k_table(s, _fits(r)), f"D k_table | {r}", "K"))
    return Md("\n\n".join(parts))


def exponents_and_facets() -> Md:
    """Exponents per metric at K = 1 and K = 3, and the facet tables, per regime.

    Returns
    -------
    Md
    """
    parts = []
    for r, s in _studies().items():
        k1, k3 = _fits(r)[1], _fits(r)[3]
        parts.append(
            f"{_cite(r)}, K = 1:\n\n"
            + _t(case.exponent_table(s, k1), f"D exponents K=1 | {r}", "metric")
            + f"\n\n{_cite(r)}, K = 3:\n\n"
            + _t(case.exponent_table(s, k3), f"D exponents K=3 | {r}", "metric")
            + f"\n\n{_cite(r)}, K = 3, per facet:\n\n"
            + frame_table(_facets(r, s, k1, k3))
        )  # fmt: skip
    return Md("\n\n".join(parts))


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
    return Md(f"Datasets {cites}:\n\n" + frame_table(table))


def termination_records() -> Md:
    """The solver's termination records for the planted data and the case.

    Returns
    -------
    Md
        Status, largest facet gap, margin, radius and the Corollary bound, as printed by the code,
        and the planted facets' recovery (largest exponent deviation after matching facets).
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
    parts.append(md_table(["Planted facets", "Largest exponent deviation after matching facets"],
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
    ("the contending sets (K = 1 and each facet at K = 3)", ("contending |",), ""),
    ("each facet's leading metrics", ("leading |",), ""),
    ("the signs of the reported tensions", ("tension |",), "sign"),
    ("the selected temperatures, to the printed 0.1", ("tau |",), ""),
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
            for v in ("four metrics", "settling time and slew time")
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
            (f"facet {k} share, K = 3, {r}", f"D facets K=3 | {r} | {k} | share", four)
            for k in (1, 2, 3)
        ]
        groups += [
            (f"{what}, K = {K}, {r}", f"certificate | {r} | {K} | {col}", four)
            for K in (2, 3)
            for what, col in (("largest facet gap", "max gap"), ("margin", "gamma"),
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
        "The settling time and the slew time are read off the accepted steps of an adaptive "
        f"integration, so a relative change of {eps:g} in a design variable can move them by up "
        "to half a second, and by much more where the error trajectory grazes the settling band "
        f"(gap G-17). Datasets {cites} and the six check designs were regenerated {n} "
        "times with `Kp`, `Kd`, the panel span and the battery capacity of every design "
        f"multiplied by 1 + e, e uniform in [-{eps:g}, {eps:g}], and every quantity this paper "
        f"reports was recomputed ({n_all} quantities, of which {len(moving)} numbers move at "
        "all). A quantity that moves is printed in this paper to the digits that held in all "
        f"{n + 1} datasets (the committed one and the {n} regenerated), as a range where not "
        "even two digits did, and as a bound where it is a numerical residue."
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
