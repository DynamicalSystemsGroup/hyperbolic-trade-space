"""Sentences of the paper's case sections whose numbers the case module produces.

Nothing here is typed: every count, temperature and name is read from the objects that
:mod:`case` returns, so the prose regenerates with the data (at the swap of the model, for
example). Each function returns an :class:`~paper_common.Md` of one or two plain sentences.
"""

from __future__ import annotations

import case
import numpy as np
from paper_common import Md


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
    parts = [f"{int(r.nondominated)} on {int(r.columns)}" for r in df.itertuples()]
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
    e = fit.estimator
    return Md(
        f"The selected temperature is tau = {fit.tau:.1f}: a fraction {e.frac_above_:.3f} of "
        f"designs lies above V = 1 (the target is {study.spec.target_frac:.2f}), the band "
        f"1/tau is {fit.band:.4f} and the effective sample size is {e.n_eff_:.1f} designs."
    )


def k1_sentence(study, fit) -> Md:
    """The K = 1 contending set."""
    names = _contending(study, fit)
    rest = [n for n in study.names if n not in names]
    return Md(
        f"At K = 1 the fit reports a {len(names)}-lemma: {_and(names)} contend, and "
        f"{_and(rest)} do not constrain the frontier at that facet."
    )


def k_sweep_sentence(study, fits) -> Md:
    """Mean slack by K, the facets at K = 3 and what the solver declared."""
    t = case.k_table(study, fits)
    obj = {int(r.K): r.objective_ for r in t.itertuples()}
    cert = t[t["K"] > 1]
    ft = case.facet_table(study, fits, K=max(fits), band=fits[1].band)
    sets = [set(s.strip() for s in x.split(",")) for x in ft["contending set"]]
    union = set().union(*sets)
    k1 = set(_contending(study, fits[1]))
    new = sorted(union - k1)
    return Md(
        f"The mean slack falls from {obj[1]:.3f} at K = 1 to {obj[2]:.3f} at K = 2 and "
        f"{obj[3]:.3f} at K = 3. The facets of the K = 3 fit hold facet shares "
        f"{_and(f'{s:.3f}' for s in ft['share'])} and contending sets of "
        f"{_and(ft['n_lemma'])} metrics; their union has {len(union)} metrics, of which "
        f"{_and(new) if new else 'none'} are absent from the K = 1 set. The solver declares "
        f"the status {_and(sorted(set(cert['status'])))} at K = 2 and 3, with the largest "
        f"facet gap {cert['max gap'].max():.1e}, the smallest assignment margin "
        f"{cert['gamma'].min():.5f} and the smallest stable radius {cert['radius'].min():.1e}."
    )


def certificate_sentence(fits) -> Md:
    """What the solver reports at each K (the Numerical badge of section 6)."""
    t = case.certificate_table(fits)
    rows = [
        f"K = {int(r['K'])}: status {r['status']}, largest facet gap {r['max gap']:.1e}"
        for _, r in t.iterrows()
    ]
    return Md("As printed by the solver on the primary regime, " + "; ".join(rows) + ".")


def regime_sentence() -> Md:
    """The contending sets of the two regimes through the identical pipeline."""
    t = case.regime_comparison().set_index("quantity")
    regs = list(case.CUBESAT.regimes)
    sets = {r: set(s.strip() for s in t.loc["contending set", r].split(",")) for r in regs}
    a, b = regs[0], regs[1]
    return Md(
        f"The two regimes return a {t.loc['n_lemma', a]}-lemma and a {t.loc['n_lemma', b]}-lemma "
        f"that share {len(sets[a] & sets[b])} metrics ({_and(sorted(sets[a] & sets[b]))}). "
        f"Only the {a} regime has {_and(sorted(sets[a] - sets[b]))} contending; only the {b} "
        f"regime has {_and(sorted(sets[b] - sets[a]))}."
    )


def candidates_sentence(table) -> Md:
    """Where the measured candidates sit against the K = 1 reference surface."""
    lv = table["log V"]
    rk = table["rank among training"]
    beyond = int((lv > 0).sum())
    return Md(
        f"The {len(table)} measured candidates have energy differentials between "
        f"{lv.min():.3f} and {lv.max():.3f}; {beyond} of them lie beyond the fitted reference "
        f"surface. Their ranks among the training designs run from {rk.min():.2f} to "
        f"{rk.max():.2f}."
    )


def predict_check_sentence(table, reg) -> Md:
    """The mixed result of propose, predict, check."""
    n = len(table)
    lv = int(table["log V within band"].sum())
    z = int(table["Z within band"].sum())
    return Md(
        f"Of {n} proposals, the predicted energy differential lies within the band "
        f"1/tau = {1 / reg.tau:.4f} of the measured one for {lv}, and the predicted position "
        f"along the frontier lies within the band for {z}; the position errors run from "
        f"{table['||dZ|| / band'].min():.1f} to {table['||dZ|| / band'].max():.1f} bands."
    )


def planted_sentence() -> Md:
    """The planted example's size."""
    from generate_model import planted_table

    X, info = planted_table()
    k, d = np.asarray(info["exponents"]).shape
    return Md(f"The planted table has {len(X)} rows, {d} metrics and {k} planted facets.")
