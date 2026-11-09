"""Sentences of the paper's case sections whose numbers the case module produces.

Nothing here is typed: every count, temperature and name is read from the objects that
:mod:`case` returns, so the prose regenerates with the data (at the swap of the model, for
example). Each function returns an :class:`~paper_common.Md` of one or two plain sentences.
"""

from __future__ import annotations

import case
import numpy as np
from paper_common import Md, Scroll
from paper_stability import stable


def _and(items) -> str:
    items = [str(i) for i in items]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _contending(study, fit) -> list[str]:
    row = case.tension_table(study, fit).iloc[0]
    return [s.strip() for s in row["contending set"].split(",")]


def nondominated_sentence(study) -> Md:
    """Nondominated counts of the study's table on each view."""
    df = case.nondominated_counts(study)
    n = int(df["of"].iloc[0])
    parts = [
        f"{stable(f'nondominated | {study.regime} | {r.view} | nondominated')} on {int(r.columns)}"
        for r in df.itertuples()
    ]
    return Md(
        f"On the cubesat table, of {n} feasible designs, the nondominated sets hold "
        f"{_and(parts)} attributes respectively."
    )


def datasets_sentence(primary, stock) -> Md:
    """How many designs each regime drew and kept."""
    a, b = primary, stock
    return Md(
        f"The primary regime evaluates {len(a.raw)} designs and keeps {len(a.feasible)} as "
        f"feasible; the stock regime evaluates {len(b.raw)} and keeps {len(b.feasible)}. "
        f"Each design carries {len(a.attrs)} attributes."
    )


def temperature_sentence(study, fit) -> Md:
    """The selected temperature and what it leaves above V = 1."""
    r = study.regime
    frac = stable(f"fit | {r} K=1 | frac_above_", lambda v: f"{v:.3f}")
    n_eff = stable(f"fit | {r} K=1 | n_eff_", lambda v: f"{v:.1f}")
    band = stable("sentence | temperature | band", lambda v: f"{v:.4f}")
    return Md(
        f"The selected temperature is tau = {fit.tau:.1f}: a fraction {frac} of "
        f"designs lies above V = 1 (the target is {study.spec.target_frac:.2f}), the band "
        f"1/tau is {band} and the effective sample size is {n_eff} designs."
    )


def k1_sentence(study, fit) -> Md:
    """The K = 1 contending set."""
    names = _contending(study, fit)
    rest = [n for n in study.names if n not in names]
    return Md(
        f"At K = 1 the fit reports a {len(names)}-lemma: {_and(names)} contend, and the other "
        f"{len(rest)} do not constrain the frontier at that facet."
    )


def k_sweep_sentence(study, fits) -> Md:
    """Mean slack by K and the contending sets of the K = 3 facets.

    The facet shares, gaps, margins and radii are Appendix D's tables (D.3, D.8).
    """
    t = case.k_table(study, fits)
    r = study.regime
    obj = {
        int(row.K): stable(f"D k_table | {r} | {int(row.K)} | objective_", lambda v: f"{v:.3f}")
        for row in t.itertuples()
    }
    ft = case.facet_table(study, fits, K=max(fits), band=fits[1].band)
    sets = [set(s.strip() for s in x.split(",")) for x in ft["contending set"]]
    union = set().union(*sets)
    k1 = set(_contending(study, fits[1]))
    new = sorted(union - k1)
    return Md(
        f"The mean slack falls from {obj[1]} at K = 1 to {obj[2]} at K = 2 and "
        f"{obj[3]} at K = 3. The K = 3 facets have contending sets of {_and(ft['n_lemma'])} "
        f"metrics; of their {len(union)} in all, {_and(new) if new else 'none'} are absent from "
        f"the K = 1 set."
    )


def certificate_sentence(fits) -> Md:
    """What the solver declares for K > 1 on the primary regime (section 6, Numerical)."""
    t = case.certificate_table(fits)
    multi = t[t["K"] > 1]
    gaps = [
        stable(f"certificate | primary | {int(k)} | max gap", lambda v: f"{v:.1e}")
        for k in multi["K"]
    ]
    gap = gaps[0] if len(set(gaps)) == 1 else _and(gaps)
    ks = _and(int(k) for k in multi["K"])
    return Md(
        f"On the primary regime the solver declares the status "
        f"{_and(sorted(set(multi['status'])))} at K = {ks}, with the largest facet gap {gap}."
    )


def regime_sentence() -> Md:
    """The contending sets of the two regimes through the identical pipeline."""
    t = case.regime_comparison().set_index("quantity")
    regs = list(case.CUBESAT.regimes)
    sets = {r: set(s.strip() for s in t.loc["contending set", r].split(",")) for r in regs}
    a, b = regs[0], regs[1]
    return Md(
        f"The two regimes return a {t.loc['n_lemma', a]}-lemma and a {t.loc['n_lemma', b]}-lemma "
        f"that share {len(sets[a] & sets[b])} metrics ({_and(sorted(sets[a] & sets[b]))}); "
        f"the {a} regime alone has {_and(sorted(sets[a] - sets[b]))}, the {b} regime alone "
        f"{_and(sorted(sets[b] - sets[a]))}."
    )


def candidates_table(study, fit) -> Scroll:
    """The measured candidates scored against the K = 1 fit, as a table that scrolls sideways."""
    return Scroll(case.candidate_table(study, fit).to_html(border=0, float_format="{:.4g}".format))


def candidates_sentence(table) -> Md:
    """Where the measured candidates sit against the K = 1 reference surface."""
    lv = table["log V"]
    beyond = int((lv > 0).sum())
    three = lambda v: f"{v:.3f}"  # noqa: E731
    return Md(
        f"The {len(table)} measured candidates have lowest energy differential "
        f"{stable('sentence | candidates | lowest log V', three)} and highest "
        f"{stable('sentence | candidates | highest log V', three)}, and {beyond} of them lie "
        f"beyond the fitted reference surface."
    )


def predict_check_sentence(table, reg) -> Md:
    """The mixed result of propose, predict, check."""
    n = len(table)
    lv = int(table["log V within band"].sum())
    z = int(table["Z within band"].sum())
    one = lambda v: f"{v:.1f}"  # noqa: E731
    return Md(
        f"Of {n} proposals, the predicted energy differential lies within the regressor's own "
        f"band 1/tau = {stable('sentence | predict-check | band', lambda v: f'{v:.4f}')} of the "
        f"measured one for {lv}, and the predicted position within that band for {z}; the smallest "
        f"position error is {stable('sentence | predict-check | lowest position error', one)} "
        f"bands, the largest {stable('sentence | predict-check | highest position error', one)}."
    )


def planted_sentence() -> Md:
    """The planted example's size."""
    from generate_model import planted_table

    X, info = planted_table()
    k, d = np.asarray(info["exponents"]).shape
    return Md(f"The planted table has {len(X)} rows, {d} metrics and {k} planted facets.")
