"""Facets of a live fit matched to the facets of the committed data by their exponent vectors.

The facets of a multi-term fit have no natural order: another platform, thread count or restart
order can return the same facets permuted. The committed jitter data (``sensitivity.json``) label
the K = 3 facets by the order of the committed fit, so a live facet is given the label of the
stored facet whose exponent vector is nearest in the L1 distance, one live facet to one stored
facet (an assignment, ``scipy.optimize.linear_sum_assignment``). The tables of Appendix D
(D.2, D.3, D.8) and the K-sweep sentence take their facet labels from here, never from the index.

>>> import numpy as np
>>> stored = np.array([[0.0, 1.0], [1.0, 0.0], [0.5, 0.5]])
>>> match_labels(stored[[2, 0, 1]], stored)
[3, 1, 2]
"""

from __future__ import annotations

import numpy as np
import paper_paths  # noqa: F401  (puts the repository on sys.path)
from paper_stability import summary
from scipy.optimize import linear_sum_assignment

K_LABELLED = 3
"""The K whose facets the committed data label."""


def match_labels(live: np.ndarray, stored: np.ndarray) -> list[int]:
    """The stored label (from 1) of each live facet, by nearest exponent vector, one to one.

    Parameters
    ----------
    live, stored : ndarray of shape (K, n_metrics)
        Exponent vectors, one row per facet, metrics in the same order.

    Returns
    -------
    list of int
        ``labels[i]`` is the 1-based stored facet that live facet ``i`` is matched to.
    """
    cost = np.abs(live[:, None, :] - stored[None, :, :]).sum(axis=2)
    rows, cols = linear_sum_assignment(cost)
    labels = [0] * len(live)
    for i, j in zip(rows, cols, strict=True):
        labels[i] = int(j) + 1
    return labels


def stored_exponents(regime: str, metrics) -> np.ndarray:
    """The committed K = 3 exponents, shape ``(3, n_metrics)``, from the sensitivity record."""
    q = summary()["quantities"]
    return np.array(
        [
            [q[f"D exponents K=3 | {regime} | {m} | facet {k}"]["committed"] for m in metrics]
            for k in range(1, K_LABELLED + 1)
        ],
        dtype=float,
    )


def exponent_labels(regime: str, exp_df) -> list[int]:
    """Labels of the facets of ``case.exponent_table`` (columns ``facet k``) at K = 3."""
    cols = [c for c in exp_df.columns if c.startswith("facet ")]
    if len(cols) != K_LABELLED:
        return list(range(1, len(cols) + 1))
    live = exp_df[cols].to_numpy(dtype=float).T
    return match_labels(live, stored_exponents(regime, exp_df["metric"]))


def relabel_exponents(exp_df, labels):
    """The exponent table with column ``facet i`` renamed to its label, columns in label order."""
    cols = [f"facet {i + 1}" for i in range(len(labels))]
    out = exp_df.rename(columns={c: f"facet {lab}" for c, lab in zip(cols, labels, strict=True)})
    order = [c for c in out.columns if not c.startswith("facet ")] + [
        f"facet {k}" for k in sorted(labels)
    ]
    return out[order]


def relabel_rows(ft, labels):
    """A per-facet table (column ``facet``) with the labels given and the rows in label order."""
    out = ft.copy()
    out["facet"] = labels
    return out.sort_values("facet").reset_index(drop=True)


def order_lists(kt, labels):
    """The ``facet rows`` and ``facet shares`` lists of ``case.k_table`` in a fixed order.

    The K = 3 lists follow the labels; those of every other K > 1 (facets the committed data do
    not label) are put in descending order of rows, an order that does not depend on the fit.
    """
    out = kt.copy()
    for i in range(len(out)):
        rows, shares = list(out.iloc[i]["facet rows"]), list(out.iloc[i]["facet shares"])
        if len(rows) < 2:
            continue
        if len(rows) == K_LABELLED and len(labels) == K_LABELLED:
            order = sorted(range(len(rows)), key=lambda p: labels[p])
        else:
            order = sorted(range(len(rows)), key=lambda p: (-rows[p], -shares[p]))
        out.iat[i, out.columns.get_loc("facet rows")] = [rows[p] for p in order]
        out.iat[i, out.columns.get_loc("facet shares")] = [shares[p] for p in order]
    return out


def aligned(regime: str, study, fits):
    """The K = 3 tables of a regime with stored facet labels: ``(exponents, facets, k_table)``.

    Parameters
    ----------
    regime : str
    study : Study
    fits : dict of int to Fit
        K = 1 and K = 3 are read.
    """
    import case

    exp = case.exponent_table(study, fits[3])
    labels = exponent_labels(regime, exp)
    ft = relabel_rows(case.facet_table(study, {1: fits[1], 3: fits[3]}), labels)
    kt = order_lists(case.k_table(study, fits), labels)
    return relabel_exponents(exp, labels), ft, kt, labels
