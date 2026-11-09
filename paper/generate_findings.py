"""Sentences of the paper's case sections whose numbers the case module produces.

Nothing here is typed: every count, temperature and name is read from the objects that
:mod:`case` returns, so the prose regenerates with the data (at the swap of the model, for
example). Each function returns an :class:`~paper_common.Md` of one or two plain sentences.
"""

from __future__ import annotations

import case
import numpy as np
from paper_common import Md
from paper_facets import aligned
from paper_stability import stable, summary


def _and(items) -> str:
    items = [str(i) for i in items]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _contending(study, fit) -> list[str]:
    row = case.tension_table(study, fit).iloc[0]
    return [s.strip() for s in row["contending set"].split(",")]


_NUMBER_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def nondominated_sentence(study) -> Md:
    """Nondominated counts of the study's table on each view, with what a range means.

    The sentence stands in section 1, where the first range appears, so it says what a range is:
    the spread of the count over the regenerations of the data under rounding-level perturbation.
    """
    df = case.nondominated_counts(study).sort_values("columns")
    n = int(df["of"].iloc[0])
    parts = [
        f"{stable(f'nondominated | {study.regime} | {r.view} | nondominated')} on {int(r.columns)}"
        for r in df.itertuples()
    ]
    runs = len(summary()["seeds"])
    return Md(
        f"Of {n} feasible cubesat designs, the nondominated sets hold {_and(parts)} attributes "
        f"(a range is the spread over {_NUMBER_WORDS.get(runs, runs)} regenerations of the data "
        f"under rounding-level perturbation, Appendix D.11)."
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
    """The K = 1 contending set: the support of the exact-maximum fit, and its exponents."""
    rep = case._reports(study, fit)[0]
    names = _contending(study, fit)
    rest = [n for n in study.names if n not in names]
    w = {study.names[j]: float(rep.exponents[j]) for j in rep.contending_set}
    two = lambda n: stable(  # noqa: E731
        f"D exponents K=1 | {study.regime} | {n} | exponent w", lambda v: f"{v:.2f}"
    )
    low, high = min(w, key=w.get), max(w, key=w.get)
    return Md(
        f"At K = 1 the exact-maximum fit has a {len(names)}-lemma: {_and(names)} contend, with "
        f"working-temperature exponents from {two(low)} to {two(high)}; the other {len(rest)} "
        f"do not."
    )


def k_sweep_sentence(study, fits) -> Md:
    """Mean slack by K at each K's temperature and at one temperature, and the K = 3 facets.

    The mean slack is the estimator's ``mean_slack_``; the temperature is re-selected at each K,
    so the first comparison is not like for like and the second holds the temperature at K = 1's.
    The facet shares, gaps, margins and radii are Appendix D's tables (D.3, D.8, D.15).
    """
    r = study.regime
    three = lambda v: f"{v:.3f}"  # noqa: E731
    own = {K: stable(f"kslack | {r} | {K} | mean_slack_", three) for K in (1, 2, 3)}
    two = lambda v: f"{v:.2f}"  # noqa: E731
    fixed = {K: stable(f"kslack fixed | {r} | {K} | mean_slack_", two) for K in (1, 2, 3)}
    tau = {
        K: stable(f"fit | {r} K={K} | tau selected (raw)", lambda v: f"{v:.0f}") for K in (1, 2, 3)
    }
    ft = aligned(r, study, fits)[1]
    sets = [set(s.strip() for s in x.split(",")) for x in ft["contending set"]]
    union = set().union(*sets)
    k1 = set(_contending(study, fits[1]))
    new = sorted(union - k1)
    return Md(
        f"The mean slack falls from {own[1]} at K = 1 to {own[2]} at K = 2 and {own[3]} at "
        f"K = 3, at the temperatures {tau[1]}, {tau[2]} and {tau[3]}; refitted at the K = 1 "
        f"temperature it falls to {fixed[2]} and {fixed[3]} (Appendix D.15). The "
        f"K = 3 facets have contending sets (exact-maximum supports) of {_and(ft['n_lemma'])} "
        f"metrics; {_and(new) if new else 'none'} are absent from the K = 1 set."
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


def margin_sentence(study, fits) -> Md:
    """How to read the size of the margin and the stable radius, with this case's values.

    The margin and the radius are read against the band 1/tau and against the median gap between
    a design's best and second-best facet score (Appendix D.8).
    """
    r, K = study.regime, max(fits)
    four = lambda v: format(v, ".4g")  # noqa: E731
    return Md(
        f"At K = {K} the margin is {stable(f'certificate | {r} | {K} | gamma', four)} and the "
        f"stable radius {stable(f'certificate | {r} | {K} | radius', four)}, against a band 1/tau "
        f"of {stable(f'D k_table | {r} | {K} | band 1/tau', lambda v: f'{v:.4f}')} and a median "
        f"best-minus-second-best score of "
        f"{stable(f'margin | {r} | {K} | median margin', lambda v: f'{v:.3f}')}: a margin below "
        f"the band puts a few designs on a seam, and the certificate covers changes under the "
        f"radius only."
    )


def recovery_sentence() -> Md:
    """Whether the fit recovers a known answer: the planted tables of Appendix D.14."""
    import generate_results as gr

    runs = gr.recovery_runs()
    by_tau = {tau: [r for r in runs if r["tau"] == tau] for tau in gr.RECOVERY_TAUS}
    n = len(by_tau[gr.RECOVERY_TAUS[0]])
    good = [sum(r["recovered"] for r in rs) for rs in by_tau.values()]
    bad = {tau: sorted(r["seed"] for r in rs if not r["recovered"]) for tau, rs in by_tau.items()}
    same = len({tuple(b) for b in bad.values()}) == 1
    first = by_tau[gr.RECOVERY_TAUS[0]]
    rows = sorted(r["rows_on_thinnest"] for r in first if not r["recovered"])
    if len(set(good)) == 1:
        temps = f"{good[0]}, at the exact maximum and at temperature {gr.RECOVERY_TAUS[1]:g}"
    else:
        temps = " and ".join(
            f"{g} at the exact maximum" if np.isinf(t) else f"{g} at temperature {t:g}"
            for g, t in zip(good, gr.RECOVERY_TAUS, strict=True)
        )
    tail = (
        f"the {len(rows)} failures have {_and(rows)} frontier rows on their thinnest facet "
        f"(Appendix D.14)"
        if same
        else "the failures differ between the temperatures (Appendix D.14)"
    )
    return Md(
        f"**A known answer.** On {n} planted tables ({gr.RECOVERY_ROWS} rows, 4 metrics) "
        f"the fit recovers all three facets to within {gr.OWN_ROWS_TOLERANCE} in {temps}; {tail}."
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
        f"measured one for {lv}, and the predicted position within that band for {z}; position "
        f"errors run from {stable('sentence | predict-check | lowest position error', one)} to "
        f"{stable('sentence | predict-check | highest position error', one)} bands."
    )


def predict_reading(table, reg) -> Md:
    """What propose, predict, check showed and did not, for the Discussion.

    Reads the same table as :func:`predict_check_sentence`; the position errors are that's.
    """
    n = len(table)
    lv = int(table["log V within band"].sum())
    z = int(table["Z within band"].sum())
    return Md(
        f"**What propose, predict, check showed.** It showed that the regressor places the "
        f"energy differential of a proposal within its band ({lv} of {n}), the easy part. It did "
        f"not show that it places the position along the frontier ({z} of {n}), and {n} "
        f"proposals illustrate and do not estimate a rate. A predicted crossing of V = 1 remains "
        f"a hypothesis."
    )


def planted_sentence() -> Md:
    """The planted example's size."""
    from generate_model import planted_table

    X, info = planted_table()
    k, d = np.asarray(info["exponents"]).shape
    return Md(f"The planted table has {len(X)} rows, {d} metrics and {k} planted facets.")
