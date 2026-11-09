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


def temperature_selection() -> Md:
    """The K = 1 fit across temperatures, per regime.

    Returns
    -------
    Md
    """
    parts = [f"{_cite(r)}:\n\n" + frame_table(case.tau_sweep(s)) for r, s in _studies().items()]
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
        parts.append(f"{_cite(r)}:\n\n" + frame_table(case.k_table(s, _fits(r))))
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
            f"{_cite(r)}, K = 1:\n\n" + frame_table(case.exponent_table(s, k1))
            + f"\n\n{_cite(r)}, K = 3:\n\n" + frame_table(case.exponent_table(s, k3))
            + f"\n\n{_cite(r)}, K = 3, per facet:\n\n"
            + frame_table(case.facet_table(s, {1: k1, 3: k3}))
        )  # fmt: skip
    return Md("\n\n".join(parts))


def regime_comparison() -> Md:
    """The regimes through the identical pipeline, side by side.

    Returns
    -------
    Md
    """
    cites = ", ".join(DATASET_LABELS[r] for r in case.CUBESAT.regimes)
    table = case.regime_comparison()
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
    parts = [f"{_cite(r)}:\n\n" + frame_table(case.certificate_table(_fits(r)))
             for r in _studies()]  # fmt: skip
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
    parts = [f"{_cite(r)}:\n\n" + frame_table(case.nondominated_counts(s))
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
    return Md(f"{_cite('primary')}:\n\n" + frame_table(case.predict_check(s, reg)))


def sensitivity_variants() -> Md:
    """The K = 1 fit under variants of the pipeline's choices, per regime.

    Returns
    -------
    Md
        The target fraction halved and doubled, the robust scaler and each named view, against the
        baseline, with how many metrics of the baseline's contending set each variant shares.
    """
    parts = [f"{_cite(r)}:\n\n" + frame_table(case.sensitivity_table(s))
             for r, s in _studies().items()]  # fmt: skip
    return Md("\n\n".join(parts))


def refits_by_category() -> Md:
    """The K = 1 fit refit within each level of the first covariate, per regime.

    Returns
    -------
    Md
    """
    parts = [f"{_cite(r)}:\n\n" + frame_table(case.category_refits(s))
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
        + frame_table(case.candidate_table(_study("primary"), _fits("primary")[1]))
    )
