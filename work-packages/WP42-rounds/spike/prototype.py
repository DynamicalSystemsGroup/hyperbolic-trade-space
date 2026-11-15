"""Prototype (not in ``src/``): the term's tension matrix and a design's tensions.

Two objects, kept apart:

* ``term_tension_matrix``: the term's tension matrix, from the fit, at the term's balanced point.
* ``design_tensions``: a design's tensions, from the data, the same formula at the design's metric
  ratios (the term the design is assigned to), in metrics and, through the conditioning, in the
  attributes' own units.

Formulas (``lemma_tension.py``): along term k, with exponents ``w``,

    T[i, j]  = d m_j / d m_i = -(w_i / w_j) (m_j / m_i)                      (metrics)
    TA[i, j] = d s_j / d s_i = -(w_i alpha_i)/(w_j alpha_j) (a_j+s_j)/(a_i+s_i)   (attributes)

Cells: negative where i and j both carry an exponent; zero (0.0) where i carries none and j does;
blank (NaN) where j carries none.  ``T[j, i] = 1 / T[i, j]`` where both are nonzero.
"""

from __future__ import annotations

import numpy as np

PARTICIPATION = 1e-3  # the package's participation threshold (tension_report, plot_tensions)


def softmax_weights(U, w, tau):
    """Weights p_i proportional to exp(tau * u_i . w) on the rows of ``U``; exact max at inf."""
    s = U @ w
    if np.isinf(tau):
        p = (s >= s.max() - 1e-12).astype(float)
    else:
        e = np.exp(tau * (s - s.max()))
        p = e
    return p / p.sum()


def balanced_point(U_term, w, tau):
    """The term's balanced point in log-metrics: the softmax-weighted mean log-metric of its rows.

    ``U_term``: log-metric rows assigned to the term; ``w``: its exponents; ``tau``: the fit
    temperature (the fit already computes the same weights).
    """
    return softmax_weights(U_term, w, tau) @ U_term


def term_tension_matrix(w, u_point, threshold=PARTICIPATION):
    """The d x d tension matrix of one term at a point of log-metrics ``u_point``.

    Returns ``T`` with ``T[i, j] = d m_j / d m_i`` along the term; NaN where j carries no
    exponent (blank), 0.0 where i carries none and j does (zero).
    """
    w = np.asarray(w, float)
    u = np.asarray(u_point, float)
    d = len(w)
    part = w > threshold
    T = np.full((d, d), np.nan)
    for i in range(d):
        for j in range(d):
            if i == j or not part[j]:
                continue  # diagonal is not drawn; blank where j carries no exponent
            T[i, j] = 0.0 if not part[i] else -(w[i] / w[j]) * np.exp(u[j] - u[i])
    return T


def elasticity_matrix(w, threshold=PARTICIPATION):
    """The log-log form: -w_i / w_j (constant on the term); same cells as ``T``."""
    w = np.asarray(w, float)
    d = len(w)
    part = w > threshold
    E = np.full((d, d), np.nan)
    for i in range(d):
        for j in range(d):
            if i != j and part[j]:
                E[i, j] = -(w[i] / w[j]) if part[i] else 0.0
    return E


def conditioning_of(study):
    """(alpha, a) of the conditioning ``log m = alpha log(a + s) + b`` of a case study."""
    pre = study.conditioner.named_transformers_["metrics"]
    alpha = np.asarray(pre.orientation_, float) / np.asarray(pre.log_scale_, float)
    return alpha, np.asarray(pre.shift_, float)


def attribute_tension(w, alpha, x, i, j):
    """d s_j / d s_i in attribute units on a term, at the design with ``x = a + s`` (shifted raw).

    Returns NaN (blank) if j carries no exponent, 0.0 if i carries none.
    """
    if w[j] <= PARTICIPATION:
        return np.nan
    if w[i] <= PARTICIPATION:
        return 0.0
    return -(w[i] * alpha[i]) / (w[j] * alpha[j]) * x[j] / x[i]


def design_tensions(estimator, m_row, raw_row=None, alpha=None, a=None):
    """A design's tension matrix, from its metric ratios, on the term it is assigned to.

    ``m_row``: the design's metrics; ``raw_row``: its attributes (for the attribute-unit matrix).
    Returns a dict: ``term``, ``T`` (metrics), ``TA`` (attributes or None), ``margin`` (the score
    gap between the assigned term and the next, a measure of nearness to a seam), and ``other``
    (the other terms' matrices at the same ratios, reported and never merged).
    """
    m_row = np.asarray(m_row, float)
    u = np.log(m_row)
    W, beta = estimator.exponents_, estimator.log_offset_
    scores = W @ u - beta
    k = int(np.argmax(scores))
    srt = np.sort(scores)[::-1]
    margin = float(srt[0] - srt[1]) if len(srt) > 1 else float("inf")
    mats = [term_tension_matrix(W[q], u) for q in range(len(W))]
    TA = None
    if raw_row is not None:
        x = np.asarray(raw_row, float) + a
        d = len(m_row)
        TA = np.full((d, d), np.nan)
        for i in range(d):
            for j in range(d):
                if i != j:
                    TA[i, j] = attribute_tension(W[k], alpha, x, i, j)
    return {"term": k, "T": mats[k], "TA": TA, "margin": margin,
            "other": {q: mats[q] for q in range(len(W)) if q != k}}  # fmt: skip
