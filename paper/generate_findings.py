"""Sentences of the paper's case sections whose numbers the case module produces.

Nothing here is typed: every count, temperature and name is read from the objects that
:mod:`case` returns, so the prose regenerates with the data (at the swap of the model, for
example). Each function returns an :class:`~paper_common.Md` of one or two plain sentences.
"""

from __future__ import annotations

import dataclasses

import case
import numpy as np
import pandas as pd
from paper_common import Md, appendix_link, md_table, thousands
from paper_stability import cell, entry, stable, summary

_C7 = appendix_link("sub-c-7", "Appendix C.7")
_D3 = appendix_link("sub-d-3", "Appendix D.3")
_D5 = appendix_link("sub-d-5", "Appendix D.5")
_D8 = appendix_link("sub-d-8", "Appendix D.8")
_D11 = appendix_link("sub-d-11", "Appendix D.11")
_D14 = appendix_link("sub-d-14", "Appendix D.14")
_C5 = appendix_link("sub-c-5", "Appendix C.5")
_E = appendix_link("appendix-e", "Appendix E")
_D15 = appendix_link("sub-d-15", "Appendix D.15")
_C8 = appendix_link("sub-c-8", "Appendix C.8")


def _and(items) -> str:
    items = [str(i) for i in items]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _span(groups) -> str:
    """Subsystems as a phrase; 'and' inside a name (power and energy) is kept apart by 'plus'."""
    groups = list(groups)
    if len(groups) <= 1:
        return "".join(groups)
    return ", ".join(groups[:-1]) + (" plus " if len(groups) == 2 else ", plus ") + groups[-1]


def _contending(study, fit) -> list[str]:
    row = case.tension_table(study, fit).iloc[0]
    return [s.strip() for s in row["contending set"].split(",")]


def _a(n: int) -> str:
    """The indefinite article before a number read aloud: "an" before eight, eleven, eighteen and
    the eighties and eight hundreds, "a" before every other (a 7-lemma, an 8-lemma, a 9-lemma,
    an 11-lemma, a 12-lemma, an 18-lemma).

    >>> [f"{_a(n)} {n}" for n in (1, 7, 8, 9, 10, 11, 12, 18, 19, 80, 100, 800, 1100)]
    ['a 1', 'a 7', 'an 8', 'a 9', 'a 10', 'an 11', 'a 12', 'an 18', 'a 19', 'an 80', 'a 100', \
'an 800', 'a 1100']
    """
    digits = str(abs(int(n)))
    head = int(digits[: len(digits) % 3 or 3])  # the leading group, read as "<head> thousand ..."
    an = head in (8, 11, 18) or 80 <= head <= 89 if head < 100 else head // 100 == 8
    return "an" if an else "a"


_NUMBER_WORDS = {
    2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
    10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
    16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
}  # fmt: skip


def nondominated_sentence(study) -> Md:
    """Nondominated counts of the study's table on each view, with what a range means.

    The sentence stands in section 1, before any other number of the case, so it says what a range
    is: the spread of a number over the regenerations of the data under rounding-level
    perturbation; when no count moves, it says so and what a range would mean.
    """
    df = case.nondominated_counts(study).sort_values("columns")
    n = int(df["of"].iloc[0])
    spec = study.spec
    parts = []
    for r in df.itertuples():
        count = thousands(stable(f"nondominated | {study.regime} | {r.view} | nondominated"))
        if r.view in spec.views:  # a named view: its attributes, named
            names = _and(spec.short[a] for a in spec.views[r.view])
            parts.append(f"{count} on {int(r.columns)} attributes ({names})")
        else:
            parts.append(f"{count} on all {int(r.columns)}")
    runs = _NUMBER_WORDS.get(len(summary()["seeds"]), len(summary()["seeds"]))
    if any(" to " in p for p in parts):
        tail = (
            f"(a range is the spread over {runs} regenerations of the data under rounding-level "
            f"perturbation, {_D11})"
        )
    else:
        tail = (
            f"(counts that hold over {runs} regenerations of the data under rounding-level "
            f"perturbation; a number that moves over them is printed as a range, {_D11})"
        )
    return Md(
        f"Of {thousands(n)} feasible cubesat designs, the nondominated set holds "
        f"{_and(parts)} {tail}."
    )


def attributes_sentence(study) -> Md:
    """The attributes of the case grouped by subsystem (the spec's one mapping, ``subsystems``)."""
    spec = study.spec
    n = len(spec.attributes)
    parts = [
        f"{g} ({_and(spec.short[a] for a in spec.attributes if spec.subsystems[a] == g)})"
        for g in spec.subsystem_order
    ]
    return Md(
        f"Each configuration is evaluated once into {_NUMBER_WORDS.get(n, n)} attributes: "
        f"{', '.join(parts[:-1])} and {parts[-1]}."
    )


def datasets_sentence(primary, stock) -> Md:
    """How many designs each regime drew and kept, and how they were drawn.

    The draw is the experiments' sampler (``LogUniformSampler``): log-uniform in the tuned ranges,
    uniform over the swapped parts and the integer fleet size, one count for both regimes.
    """
    a, b = primary, stock
    n = len(a.raw)
    return Md(
        f"The primary regime evaluates {thousands(len(a.raw))} designs and keeps "
        f"{thousands(len(a.feasible))} as feasible; the stock regime evaluates "
        f"{thousands(len(b.raw))} and keeps {thousands(len(b.feasible))}. "
        f"Each design carries {_NUMBER_WORDS.get(len(a.attrs), len(a.attrs))} attributes. "
        f"The designs are drawn at random, {thousands(n)} per "
        f"regime: a design choice of the case, since the method assumes nothing about how they "
        f"were drawn."
    )


def participation_sentence() -> Md:
    """The traded metrics that enter no contending set, and why (Appendix C.5).

    A metric participates when it is in the contending set of some term of some fit at K = 1 to
    the deepest K the case fits, in either regime. A metric that never does is read with its
    strongest partner among those that do: the lowest, over the regimes, of the Spearman
    association with that partner (``case.association_all_pairs``).
    """
    import generate_results as gr

    regs = list(case.CUBESAT.regimes)
    names = list(gr._study(regs[0]).names)
    used, depth = set(), 0
    for r in regs:
        st = gr._study(r)
        for K, fit in gr._fits(r).items():
            depth = max(depth, K)
            for rep in case._reports(st, fit):
                used |= {st.names[j] for j in rep.contending_set}
    out = [n for n in names if n not in used]
    if not out:
        return Md(
            f"Each of the {_NUMBER_WORDS.get(len(names), len(names))} traded metrics enters a "
            f"contending set at K = 1 to {depth} "
            f"in a regime."
        )
    rho = {}
    for r in regs:
        t = case.association_all_pairs(gr._study(r))
        for x, y, v in zip(t["metric a"], t["metric b"], t["spearman"], strict=True):
            rho.setdefault(frozenset((x, y)), []).append(abs(float(v)))
    best = {
        n: max(((min(rho[frozenset((n, m))]), m) for m in used), key=lambda p: p[0]) for n in out
    }
    low = int(min(v for v, _ in best.values()) * 100) / 100
    return Md(
        f"Of the {_NUMBER_WORDS.get(len(names), len(names))} traded metrics, "
        f"{_NUMBER_WORDS.get(len(out), len(out))}, "
        f"{_and('the ' + n for n in out)}, enter no contending set at K = 1 to {depth} in either "
        f"regime: each is nearly one axis with a metric that does (Spearman at least {low:.2f}, "
        f"{_C5})."
    )


def _target_variants_keep_the_set(study) -> bool:
    """Whether the K = 1 contending set is the baseline's with the target halved and doubled."""
    t = case.sensitivity_table(study).set_index("variant")
    sets = {v: set(s.strip() for s in t.loc[v, "contending set"].split(",")) for v in t.index}
    base = sets["baseline"]
    return all(sets[v] == base for v in ("target fraction halved", "target fraction doubled"))


def temperature_sentence(study, fit) -> Md:
    """The fit temperature and what it leaves above V = 1; what the effective sample size counts.

    The second sentence reads the effective sample size (the glossary's definition: the inverse
    sum of squares of the support weights, so the designs the soft maximum weighs as if equally)
    and says whether the contending set holds with the target fraction halved and doubled (D.5);
    the digits that hold are D.11's.
    """
    r = study.regime
    frac = stable(f"fit | {r} K=1 | frac_above_", lambda v: f"{v:.3f}")
    n_eff = stable(f"fit | {r} K=1 | n_eff_", lambda v: f"{v:.1f}")
    band = stable("sentence | temperature | band", lambda v: f"{v:.4f}")
    holds = (
        "holds with the target fraction halved or doubled"
        if _target_variants_keep_the_set(study)
        else "changes with the target fraction halved or doubled"
    )
    return Md(
        f"The fit temperature is tau = {fit.tau:.1f}: a fraction {frac} of "
        f"designs lies above V = 1 (the target is {study.spec.target_frac:.2f}), the band "
        f"1/tau is {band} and the effective sample size is {n_eff} designs. The effective "
        f"sample size is the inverse sum of squares of the support weights, the softmax weights "
        f"of the designs in the fit: the designs the soft maximum weighs as if equally, so the "
        f"exponents at the fit temperature rest on about that many of the "
        f"{thousands(len(study.M))} "
        f"designs. The contending set {holds} ({_D5})."
    )


def k1_sentence(study, fit) -> Md:
    """The K = 1 contending set: the support of the exact-maximum fit, and its exponents.

    The R1 clause is checked on both regimes by
    ``tests/test_paper.py::test_the_regimes_contending_set_is_the_unique_lp_optimum_not_a_solver_choice``.
    """
    rep = case._reports(study, fit)[0]
    names = _contending(study, fit)
    w = {study.names[j]: float(rep.exponents[j]) for j in rep.contending_set}
    two = lambda n: stable(  # noqa: E731
        f"D exponents K=1 | {study.regime} | {n} | exponent w", lambda v: f"{v:.2f}"
    )
    low, high = min(w, key=w.get), max(w, key=w.get)
    return Md(
        f"At K = 1 the exact-maximum fit has {_a(len(names))} {len(names)}-lemma across "
        f"{_span(study.spec.subsystems_of(names))}: {_and(names)} contend, with "
        f"exponents at the fit temperature from {two(low)} to {two(high)}. "
        "R1 of Section 5 holds on both regimes: the exact-maximum optimum is one point, so the "
        "support is not a solver's choice."
    )


def choosing_k_sentence() -> Md:
    """The K the paper's choosing-K checks pick for the case, and why (Appendix D.15).

    Read from :func:`generate_results.choosing_k_tables`: the K at which the mean slack drops most,
    the drop at the next K, and the thinnest term's share at the pick and at the next K (each K's
    own temperature). The movement under resampling stays in Appendix D.15.
    """
    import generate_results as gr

    tabs = gr.choosing_k_tables()
    picks = {r: case.chosen_k(t) for r, t in tabs.items()}
    if len(set(picks.values())) != 1:
        raise ValueError(f"the regimes pick different K: {picks}")
    K = case.CASE_K
    if set(picks.values()) != {K}:
        raise ValueError(f"the checks pick K = {picks}, the case reads K = {K}")

    def both(col, k, fmt):
        return _and(fmt(t.set_index("K").loc[k, col]) for t in tabs.values())

    two = lambda v: f"{v:.2f}"  # noqa: E731
    regimes = _and(f"the {r} regime" for r in tabs)
    return Md(
        f"**{_NUMBER_WORDS[K].capitalize()} terms.** The package's checks for choosing K ({_D15}) "
        f"pick K = {K} on {regimes}: the mean "
        f"slack, read at the K = 1 temperature, drops most at K = {K} ({both('drop', K, two)}) "
        f"and less at K = {K + 1} ({both('drop', K + 1, two)}). The thinnest term holds "
        f"{both('thinnest share, own tau', K, two)} of the near-frontier designs at K = {K} and "
        f"{both('thinnest share, own tau', K + 1, two)} at K = {K + 1}, the step where a thin term "
        f"appears."
    )


def terms_sentence(study, fits) -> Md:
    """The case's terms (``case.CASE_K``): their contending sets against the K = 1 set, any term
    without an association reading, and the term shares.

    The terms are in the estimator's order, descending term share. The shares are printed to two
    digits, the precision the reading uses; Appendix D.3 has the rows.
    """
    K = case.CASE_K
    ft = case.term_table(study, fits, K=K)
    sets = [set(s.strip() for s in x.split(",")) for x in ft["contending set"]]
    union = set().union(*sets)
    k1 = set(_contending(study, fits[1]))
    new = sorted(union - k1)
    leads = [x.split(", ")[0].rsplit(" ", 1)[0] for x in ft["largest exponents"]]
    led = [m for m in new if m in leads]
    verb = "leads a term of its own" if len(led) == 1 else "each lead a term of their own"
    if not new:
        absent = "none is absent from the K = 1 set"
    elif led == new:
        absent = f"{_and(new)}, absent from the K = 1 set, {verb}"
    else:
        absent = f"{_and(new)} {'is' if len(new) == 1 else 'are'} absent from the K = 1 set"
        absent += f", and {_and(led)} {verb}" if led else ""
    thin = [
        f"term {int(row.term)} has no association reading ({row._5} near-frontier designs of the "
        f"{_NUMBER_WORDS[case.MIN_NEAR_FRONTIER]} the reading needs)"
        for row in ft.itertuples(index=False)
        if row._5 < case.MIN_NEAR_FRONTIER
    ]  # ``_5`` is the near-frontier count (pandas names the columns with spaces by position)
    shares = _and(f"{v:.2f}" for v in ft["share"])
    terms = _and(int(k) for k in ft["term"])
    return Md(
        f"The K = {K} terms have contending sets (exact-maximum supports) of "
        f"{_and(ft['n_lemma'])} metrics; {absent}. "
        + (f"{thin[0].capitalize()}; the term shares" if thin else "The term shares")
        + f" are {shares} for terms {terms} ({_D3})."
    )


def k_temperatures_sentence(study, fits) -> Md:
    """Each K's own fit temperature and band, selected by the one rule, and which band the figures
    and the association reading use (the K = 1 band at every K, gap G-9)."""
    r = study.regime
    Ks = [K for K in sorted(fits) if K <= case.CASE_K]
    taus = [stable(f"fit | {r} K={K} | tau selected (raw)", lambda v: f"{v:.0f}") for K in Ks]
    bands = [stable(f"D k_table | {r} | {K} | band 1/tau", lambda v: f"{v:.4f}") for K in Ks]
    return Md(
        f"Each K selects its own fit temperature by the same rule: "
        f"tau = {_and(taus)} at K = {_and(Ks)}, with bands 1/tau of {_and(bands)}. The figures "
        f"and the association reading use the K = 1 band at every K (gap G-9, {_E})."
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
    soft = [not np.isinf(fits[int(k)].estimator.term_temperature) for k in multi["K"]]
    kind = "soft" if all(soft) else "sharp" if not any(soft) else "sharp and soft"
    return Md(
        f"On the primary regime the fits of record are {kind}; the solver declares the status "
        f"{_and(sorted(set(multi['status'])))} at K = {ks}, with the largest term gap {gap}."
    )


def designs_on_a_seam(study, fit) -> tuple[int, int]:
    """The designs whose best-minus-second-best term score is below the band 1/tau, and all.

    A margin below the band shows only that at least one design is within the band of a seam;
    this is the count. On the primary data at K = 3 three gaps lie within 4 per cent of the band,
    so the count is the winning restart's: 11 in the fit of record, 10 with the restart order
    shifted (``paper/environment_values.toml``, ``[perturbation]``).
    """
    e = fit.estimator
    scores = np.log(study.M) @ np.atleast_2d(e.exponents_).T - e.log_offset_
    top = np.sort(scores, axis=1)
    return int(np.sum(top[:, -1] - top[:, -2] < fit.band)), len(top)


def margin_sentence(study, fits) -> Md:
    """How to read the size of the margin and the stable radius, with this case's values.

    The margin and the radius are read against the band 1/tau and against the median gap between
    a design's best and second-best term score (Appendix D.8); the designs within the band of a
    seam are counted (:func:`designs_on_a_seam`).
    """
    r, K = study.regime, case.CASE_K
    four = lambda v: format(v, ".4g")  # noqa: E731
    n, N = designs_on_a_seam(study, fits[K])
    times = f"{float(f'{fits[K].band / (fits[K].estimator.termination_.gamma / 2):.2g}'):g}"
    held = [entry(f"contending | {r} K={K} term {k} | set") for k in range(1, K + 1)]
    sets = (
        f"the contending sets themselves hold under rounding-level jitter ({_D11})"
        if held and all(e is not None and e.get("identical") for e in held)
        else f"whether the contending sets hold under rounding-level jitter is read in {_D11}"
    )
    return Md(
        f"At K = {K} the margin is {stable(f'certificate | {r} | {K} | gamma', four)} and the "
        f"stable radius {stable(f'certificate | {r} | {K} | radius', four)}, against a band 1/tau "
        f"of {stable(f'D k_table | {r} | {K} | band 1/tau', lambda v: f'{v:.4f}')} and a median "
        f"best-minus-second-best score of "
        f"{stable(f'margin | {r} | {K} | median margin', lambda v: f'{v:.3f}')}: a margin below "
        f"the band puts at least one design within the band of a seam, here {thousands(n)} of "
        f"the {thousands(N)}, and "
        f"the certificate covers changes under the radius only. For the {_NUMBER_WORDS[K]}-term "
        f"split: the local optimality certified covers changes of the term scores under half the "
        f"margin, about {times} times smaller than the band, so which term those {n} designs "
        f"fall to is not a finding; {sets}."
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
        f"the {len(rows)} failures have {_and(rows)} frontier rows on their thinnest term ({_D14})"
        if same
        else f"the failures differ between the temperatures ({_D14})"
    )
    return Md(
        f"**A known answer.** On the {n} planted tables the fit recovers all three terms to "
        f"within {gr.OWN_ROWS_TOLERANCE} in {temps}; {tail}."
    )


def _straddling_pair(regs, sets):
    """The strongest-associated pair of traded metrics, when it is the same pair in both regimes
    and has one metric in each regime's own part of the contending set: ``((x, y), {regime:
    spearman})`` with ``x`` in the first regime's own part, else ``None``.

    The association is Spearman over the feasible designs (``case.association_all_pairs``,
    the table of D.3 and D.4).
    """
    a, b = regs
    strongest = {}
    for r in regs:
        row = case.association_all_pairs(case.load_study(r)).iloc[0]
        strongest[r] = (frozenset((row["metric a"], row["metric b"])), float(row["spearman"]))
    pair = strongest[a][0]
    if strongest[b][0] != pair:
        return None
    own_a, own_b = pair & (sets[a] - sets[b]), pair & (sets[b] - sets[a])
    if len(own_a) != 1 or len(own_b) != 1:
        return None
    return (next(iter(own_a)), next(iter(own_b))), {r: strongest[r][1] for r in regs}


def regime_sentence() -> Md:
    """The contending sets of the two regimes through the identical pipeline.

    Where the strongest-associated pair of traded metrics has one member in each regime's own
    part of the set, the sentence names the pair with its association and counts it as one when
    it says what each regime alone has (the text before it says why: Theorem 3 gives convexity,
    not strict convexity, so the split of an exponent between two metrics that move together is
    not read as a finding).
    """
    t = case.regime_comparison().set_index("quantity")
    regs = list(case.CUBESAT.regimes)
    sets = {r: set(s.strip() for s in t.loc["contending set", r].split(",")) for r in regs}
    a, b = regs[0], regs[1]
    spec = case.CUBESAT
    ga, gb = spec.subsystems_of(sets[a]), spec.subsystems_of(sets[b])
    only_a, only_b = [g for g in ga if g not in gb], [g for g in gb if g not in ga]
    point = "".join(
        f": {_span(only)} enters only in the {r} regime"
        for r, only in ((a, only_a), (b, only_b))
        if only
    )
    own_a, own_b = sets[a] - sets[b], sets[b] - sets[a]
    pair = _straddling_pair(regs, sets)
    if pair:
        (x, y), rho = pair
        own_a, own_b = own_a - {x}, own_b - {y}
        middle = (
            f"; {x} and {y}, one in each regime's own part, are the strongest-associated pair "
            f"of traded metrics (Spearman {rho[a]:+.3f} and {rho[b]:+.3f} over the feasible "
            f"designs, {_D3}); counting them as one, the {a} regime alone has "
            f"{_and(sorted(own_a))}, the {b} regime alone {_and(sorted(own_b))}"
        )
    elif own_b and not own_a:
        middle = f"; the {a} set lies inside the {b} set, which adds {_and(sorted(own_b))}"
    elif own_a and not own_b:
        middle = f"; the {b} set lies inside the {a} set, which adds {_and(sorted(own_a))}"
    else:
        middle = (
            f"; the {a} regime alone has {_and(sorted(own_a))}, the {b} regime alone "
            f"{_and(sorted(own_b))}"
        )
    return Md(
        f"The regimes return {_a(t.loc['n_lemma', a])} {t.loc['n_lemma', a]}-lemma and "
        f"{_a(t.loc['n_lemma', b])} {t.loc['n_lemma', b]}-lemma "
        f"sharing {len(sets[a] & sets[b])} metrics ({_and(sorted(sets[a] & sets[b]))})"
        f"{middle}. The {b} set spans {_span(gb)}{point}."
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

    Reads the same table as :func:`predict_check_sentence`, and the recorded predictions and the
    measured check designs of the spec for what the proposals are: how many distinct
    configurations, how many meet the model's depth-of-discharge requirement (``dod_ok``), their
    batteries and depths of discharge, and where they sit on the four-metric view (spike A of the
    WP23 close-out: they reached that frontier by spending the battery).
    """
    import pandas as pd

    spec = case.CUBESAT
    n = len(table)
    lv = int(table["log V within band"].sum())
    z = int(table["Z within band"].sum())
    preds = pd.read_csv(spec.data_dir / spec.predictions_file)
    configs = len(preds[list(spec.design_vars) + list(spec.covariates)].drop_duplicates())
    checks = pd.read_csv(spec.data_dir / spec.checks_file)
    props = checks[checks["role"] == "proposal"]
    dod = int(props["dod_ok"].sum())
    k = n - configs + 1
    words = lambda v: _NUMBER_WORDS.get(v, v)  # noqa: E731
    same = (
        f" {words(k).capitalize()} of the {words(n)} proposals are one configuration."
        if k > 1
        else ""
    )
    designs = f" of {words(configs)} designs" if configs < n else ""
    band = float((table["difference"] / table["|diff| / band"]).iloc[0])
    lo, hi = spec.ranges["battery_wh"]
    far = float(table["measured log V"].abs().max())
    where = "inside" if far < band else "against"
    joined = lambda xs, f: " and ".join(f.format(x) for x in sorted(set(xs)))  # noqa: E731
    fail = (
        " They reached the four-metric frontier they were aimed at by spending the battery. "
        f"Their measured log V is within {far:.3f} of V = 1, {where} the band {band:.3f}. "
        "Their batteries are "
        f"{joined(props['battery_wh'].round(0), '{:.0f}')} Wh, at the bottom of the {lo:g} to "
        f"{hi:g} Wh range, and {'all' if dod == 0 else f'{n - dod} of the'} {n} fail the model's "
        "depth-of-discharge requirement at "
        f"{joined(props['dod_eclipse'].round(2), '{:.2f}')}. The proposer's chart is the "
        "four-metric view, which has no depth-of-discharge axis. A proposer that also predicts "
        "the feasibility flags, and proposes only designs predicted to meet them, is future work."
        if dod < n
        else ""
    )
    return Md(
        f"**What propose, predict, check showed.**{same} It showed that the regressor places "
        "the energy differential of a proposal "
        f"within its band ({lv} of {n}), the easy part. It did not show that it places the "
        f"position along the frontier ({z} of {n}).{fail} "
        f"{words(n).capitalize()} proposals{designs} illustrate and do not estimate a rate. "
        "A predicted crossing of V = 1 remains a hypothesis."
    )


SWAP_SET = ("pointing error", "peak slew power")
"""The metrics the swapped parts, the tracker grade and the wheel class, step (the bottom panel
of the planes figure: columns and bands; Appendix C.2): a term led by two of them trades
across the swapped parts' alternatives rather than along one continuous trade."""


def elasticity_sentence(study, fits) -> Md:
    """One elasticity read as a number from a term's exponents (Theorem 5), and the term whose
    two leading metrics the swaps set.

    The pair is the K = 1 fit's two heaviest metrics (the pair the K = 1 plane draws); the term is
    the case's term (``case.CASE_K`` terms, in the estimator's order) that carries the largest
    exponent of the heavier one. The number is ``-w_i / w_j``: the percent of the heavier metric
    given up per percent gained in the other.
    """
    ft = case.term_table(study, fits, K=case.CASE_K)
    rep1 = case._reports(study, fits[1])[0]
    order = np.argsort(-rep1.exponents)
    a, b = study.names[order[0]], study.names[order[1]]
    ja, jb = study.names.index(a), study.names.index(b)
    W = np.atleast_2d(fits[case.CASE_K].estimator.exponents_)
    live = int(np.argmax(W[:, ja]))
    k = live + 1
    text = f"{float(W[live, jb] / W[live, ja]):.1f}"
    swaps = []
    for row in ft.itertuples(index=False):
        leaders = [x.rsplit(" ", 1)[0] for x in str(row._4).split(", ")[:2]]
        if all(m in SWAP_SET for m in leaders):
            swaps.append(f"Term {int(row.term)}'s two leading metrics, {_and(leaders)},")
    tail = (
        " "
        + " ".join(
            f"{head} are stepped by the swaps of the tracker grade and the wheel class, so its "
            "elasticity is read across the swapped parts' alternatives rather than along one "
            "continuous trade."
            for head in swaps
        )
        if swaps
        else ""
    )
    return Md(
        f"On term {k} the elasticity between {a} and {b} is -{text}: along the term, one percent "
        f"gained in {b} is {text} percent given up in {a}.{tail}"
    )


def planted_sentence() -> Md:
    """The worked example of Appendix C.7, the planted table of the case sections, with its size.

    The twenty tables the case analysis fits (D.14), drawn by the same generator, are named where
    they are read (:func:`recovery_sentence`); the n-lemma figure's three-metric table is named by
    the text that precedes this sentence.
    """
    from generate_model import planted_table

    X, info = planted_table()
    k, d = np.asarray(info["exponents"]).shape
    return Md(f"The worked example of {_C7} has {len(X)} rows, {d} metrics and {k} planted terms.")


# ---- the decision (WP39): the closing subsection of Section 9 and Appendix D's table -------------
# One function, ``decision``, computes every number from the study and its fits; the paragraph, the
# six-row table and the 28-design table are formatted from its result and nothing else is typed.


@dataclasses.dataclass(frozen=True)
class Decision:
    """Everything the case's closing decision reads (see :func:`decision`).

    Attributes
    ----------
    counts : dict of str to int
        ``feasible``, ``six_pass``, ``working`` (the shortlist), ``nondominated`` (on pointing
        error and fleet cost, over all six-pass designs) and ``nondominated_in_band`` (of those,
        the ones in the shortlist), ``nondominated_working`` (nondominated within the shortlist).
    working : pandas.DataFrame
        The shortlist ordered by fleet cost, with ``log V K=2``, ``log V K=1``, ``term 1 level``,
        ``term 2 level``, ``nd`` and ``nd unit`` (nondominated on pointing error with fleet
        cost, and with unit cost).
    picks : dict of str to pandas.Series
        The named designs: ``sponsor`` (cheapest fleet cost), ``cheapest unit`` (cheapest unit
        cost), ``operator`` (smallest pointing error), ``between`` (minimax regret on pointing
        error and fleet cost), ``balanced`` (smallest gap between the two term levels), and
        ``fine`` (cheapest fleet cost among the fine-tracker designs).
    baseline : dict
        The model's baseline configuration with its ``log V K=2``.
    fleet_budget, unit_limit : float
        The fleet-cost and unit-cost limits of the requirements.
    """

    counts: dict
    working: pd.DataFrame
    picks: dict
    baseline: dict
    fleet_budget: float
    unit_limit: float


def _shortlist(study, fits):
    """The feasible designs that pass all six requirements (mask), those among them within the
    band of both fits (mask), and the level log V at K = 1 and at the case's K, per design."""
    f1, fk = fits[1], fits[case.CASE_K]
    six = case.requirement_mask(study.feasible, study.spec, costs=True).to_numpy()
    lv1 = f1.estimator.score_samples(study.M)
    lvk = fk.estimator.score_samples(study.M)
    inside = (np.abs(lv1) < f1.band) & (np.abs(lvk) < f1.band)
    return six, six & inside, lv1, lvk


def decision(study=None, fits=None) -> Decision:
    """The shortlist and the named designs of the case, computed from the data of record.

    The shortlist is the feasible designs that pass all six requirements and lie within the
    near-frontier band (the K = 1 band, at every K, as in Section 9) of both the K = 1 and the
    case's K fit. Every named design is asserted to lie in the shortlist and to pass the six
    requirements.

    Parameters
    ----------
    study : case.Study, optional
        Default: the primary regime.
    fits : dict of int to case.Fit, optional
        Fits at K = 1 and ``case.CASE_K``; default ``case.k_fits(study, (1, CASE_K))``.

    Returns
    -------
    Decision
    """
    study = study or case.load_study("primary")
    fits = fits or case.k_fits(study, (1, case.CASE_K))
    spec, df = study.spec, study.feasible
    fk = fits[case.CASE_K]
    six, work, lv1, lvk = _shortlist(study, fits)
    levels = np.log(study.M) @ fk.estimator.exponents_.T - fk.estimator.log_offset_
    out = df.assign(**{"log V K=1": lv1, "log V K=2": lvk, "term 1 level": levels[:, 0],
                       "term 2 level": levels[:, 1]})  # fmt: skip
    # the shortlist's own order: fleet cost, then design id
    w = out[work].sort_values(["fleet_cost_usd", "design_id"]).reset_index(drop=True)
    pe, fc = w["pointing_error_deg"].to_numpy(), w["fleet_cost_usd"].to_numpy()
    w["nd"] = case.nondominated_mask(-np.column_stack([pe, fc]))
    w["nd unit"] = case.nondominated_mask(-np.column_stack([pe, w["unit_cost_usd"].to_numpy()]))
    all_six = out[six]
    nd_all = case.nondominated_mask(-all_six[["pointing_error_deg", "fleet_cost_usd"]].to_numpy())
    nd_ids = set(all_six["design_id"][nd_all])
    scaled = np.column_stack([(pe - pe.min()) / np.ptp(pe), (fc - fc.min()) / np.ptp(fc)])
    gap = np.abs(w["term 1 level"] - w["term 2 level"]).to_numpy()
    fine = np.flatnonzero((w["st_grade"] == "fine").to_numpy())
    picks = {
        "sponsor": w.iloc[int(np.argmin(fc))],
        "cheapest unit": w.iloc[int(np.argmin(w["unit_cost_usd"].to_numpy()))],
        "operator": w.iloc[int(np.argmin(pe))],
        "between": w.iloc[int(np.argmin(scaled.max(axis=1)))],
        "balanced": w.iloc[int(np.argmin(gap))],
        "fine": w.iloc[fine[int(np.argmin(fc[fine]))]],
    }
    ids = set(w["design_id"])
    for name, row in picks.items():  # R-6: named designs are in the shortlist and pass all six
        assert row["design_id"] in ids, name
        raw = df[df["design_id"] == row["design_id"]]
        assert case.requirement_mask(raw, spec, costs=True).all(), name
    base = dict(spec.baseline_configuration)
    frame = pd.DataFrame([base])
    for c in (*spec.covariates, *spec.design_vars):
        if c not in frame:
            frame[c] = 0.0
    cols = [f"metrics__{a}" for a in spec.attributes]
    Mb = study.conditioner.transform(frame)[cols].to_numpy()
    base["log V K=2"] = float(fk.estimator.score_samples(Mb)[0])
    counts = {
        "feasible": len(df),
        "six_pass": int(six.sum()),
        "working": len(w),
        "nondominated": len(nd_ids),
        "nondominated_in_band": len(nd_ids & ids),
        "nondominated_working": int(w["nd"].sum()),
    }
    return Decision(counts, w, picks, base,
                    spec.cost_requirements["fleet_cost_usd"][0],
                    spec.cost_requirements["unit_cost_usd"][0])  # fmt: skip


def _config(row) -> str:
    """A design's executive-table configuration: wheel class, tracker grade, fleet size."""
    return (f"{row['wheel_class']} wheel, {row['st_grade']} tracker, "
            f"fleet {int(row['fleet_size'])}")  # fmt: skip


def _musd(x: float) -> str:
    return f"{x / 1e6:.2f}"


def _thousand_usd(x: float) -> str:
    return f"{round(x, -3):,.0f}"


def _held(name: str, value: float, orig=str) -> str:
    """``value`` as the decision's stability entry ``name`` prints it: ``orig(value)`` where the
    quantity did not move over the five regenerations, the digits that held where it did.

    The entry must exist (a quantity the stability study has not measured is an error, not a
    silent exact print). A value outside the measured range belongs to a different record than
    the one measured and prints as it is.
    """
    e = entry(f"decision | primary | {name}")
    if e is None or "min" not in e:
        raise KeyError(f"decision | primary | {name!r} is not in the stability results")
    if not e["min"] <= value <= e["max"]:
        return orig(value)
    shown = cell(f"decision | primary | {name}", value, orig)
    return shown if isinstance(shown, str) else orig(value)


def _count(d: Decision, key: str) -> str:
    return _held(f"count | {key}", d.counts[key], lambda v: str(round(v)))


def _tracker_cost(d: Decision) -> float:
    """What the fine tracker adds to the fleet cost: the cheapest fine design against the cheapest
    design of the shortlist, in USD."""
    return float(d.picks["fine"]["fleet_cost_usd"] - d.picks["sponsor"]["fleet_cost_usd"])


def decision_sentence(d: Decision) -> Md:
    """The closing paragraph of Section 9: the question the method hands the two executives.

    Narrated dollars are to the nearest 1,000 or 0.01 M USD; the tables give them exactly.
    """
    p = d.picks
    sp, bw = p["sponsor"], p["between"]
    assert bw["st_grade"] == "fine" and sp["st_grade"] != "fine", "premise of the paragraph"
    for role in ("sponsor", "between", "fine"):  # the same design in every regeneration
        assert entry(f"decision | primary | {role} | design")["identical"], role
    tracker = lambda r: f"{r['wheel_class']}-wheel, {r['st_grade']}-tracker"  # noqa: E731
    one = lambda v: f"{v:.1g}"  # noqa: E731
    held = lambda role, col, orig: _held(f"{role} | {col}", p[role][col], orig)  # noqa: E731
    return Md(
        f"**What the executives decide.** The case's two stakeholders: the operator cares "
        f"about the pointing error, the sponsor about the unit cost and the fleet cost. "
        f"The requirements and the frontier "
        f"cut {thousands(_count(d, 'feasible'))} feasible designs to {_count(d, 'working')} that "
        f"pass all six requirements and lie in the near-frontier band of both fits, the simpler "
        f"and the richer. One question remains, "
        f"and it is theirs: whether a fine star tracker, which brings the pointing error from "
        f"about {held('sponsor', 'pointing_error_deg', one)} to "
        f"{held('fine', 'pointing_error_deg', one)} degree, is worth about "
        f"{_held('fine tracker | extra fleet cost', _tracker_cost(d), lambda v: f'{v / 1e6:.2f}')}"
        f" M USD of a {d.fleet_budget / 1e6:g} M USD fleet cost limit. "
        f"If it is, the fleet of {int(bw['fleet_size'])} {tracker(bw)} satellites at "
        f"{held('between', 'fleet_cost_usd', _musd)} M USD "
        f"({held('between', 'unit_cost_usd', _thousand_usd)} USD each) "
        f"gives up the least of either measure among the {_count(d, 'nondominated_working')} of "
        f"the {_count(d, 'working')} that no other beats on both; "
        f"if not, the fleet of {int(sp['fleet_size'])} {tracker(sp)} satellites at "
        f"{held('sponsor', 'fleet_cost_usd', _musd)} M USD is cheapest. The method prices the "
        f"question and does not answer it; the numbers are nominal ({_C8})."
    )


def decision_detail_sentence(d: Decision) -> Md:
    """What the fit adds to a two-measure view, for Appendix D: the nondominated designs over all
    six-pass designs and how many of them lie in the shortlist."""
    from generate_model import DATASET_LABELS

    return Md(
        f"Dataset {DATASET_LABELS['primary']}: over all {_count(d, 'six_pass')} designs that pass "
        f"the six requirements, "
        f"{_count(d, 'nondominated')} are nondominated on pointing error and fleet cost, and "
        f"{_count(d, 'nondominated_in_band')} of them lies within the band of both fits; the "
        f"others reach their cost or pointing error by lying well inside the frontier."
    )


def decision_baseline_sentence() -> Md:
    """The stock-gain regime's funnel in one sentence, for Appendix D.19: the same shortlist rule
    applied to the second regime of the case. Counts are exact on the data of record."""
    from generate_model import DATASET_LABELS

    study = case.load_study("stock")
    six, work, *_ = _shortlist(study, case.k_fits(study, (1, case.CASE_K)))
    return Md(
        f"Dataset {DATASET_LABELS['stock']}: the baseline regime (stock gains) has "
        f"{thousands(len(study.feasible))} feasible designs, "
        f"{int(six.sum())} that pass the six requirements and {int(work.sum())} within the band "
        f"of both fits."
    )


def decision_table(d: Decision) -> Md:
    """The six-row table of Section 9: the rule, the configuration, the three measures and the
    level (log V at the case's K), exact."""
    p = d.picks
    rows = [("baseline configuration", None, d.baseline)]
    rows += [
        ("sponsor alone", "sponsor", p["sponsor"]),
        ("operator alone", "operator", p["operator"]),
        ("between them", "between", p["between"]),
        ("balanced between the terms", "balanced", p["balanced"]),
        ("cheapest unit cost", "cheapest unit", p["cheapest unit"]),
    ]

    def held(role, col, r, fmt):  # the baseline is not a pick: no stability entry, exact
        return fmt(r[col]) if role is None else _held(f"{role} | {col}", r[col], fmt)

    return Md(md_table(
        ["rule", "configuration", "pointing error (degree)", "unit cost (USD)",
         "fleet cost (USD)", "level"],
        [(n, _config(r), held(k, "pointing_error_deg", r, lambda v: f"{v:.5f}"),
          held(k, "unit_cost_usd", r, lambda v: f"{v:,.0f}"),
          held(k, "fleet_cost_usd", r, lambda v: f"{v:,.0f}"), f"{r['log V K=2']:+.3f}")
         for n, k, r in rows],
    ))  # fmt: skip


def _marks(r) -> str:
    """Nondominated on pointing error and fleet cost, on pointing error and unit cost, or both."""
    on = [n for n, k in (("fleet cost", "nd"), ("unit cost", "nd unit")) if r[k]]
    return " and ".join(on)


def decision_designs_table(d: Decision) -> Md:
    """Appendix D's table: the shortlist ordered by fleet cost, exact, with the nondominated
    designs (on pointing error and fleet cost) marked."""
    from generate_model import DATASET_LABELS

    w = d.working
    return Md(f"Dataset {DATASET_LABELS['primary']}:\n\n" + md_table(
        ["design", "wheel / tracker", "panel (m)", "battery (Wh)", "Kp", "Kd", "fleet",
         "pointing error (degree)", "unit cost (USD)", "fleet cost (USD)", "level (K=2)",
         "level (K=1)", "term 1 level (K=2)", "term 2 level (K=2)",
         "nondominated on pointing error and"],
        [(int(r["design_id"]), f"{r['wheel_class']} / {r['st_grade']}",
          f"{r['panel_span_m']:.2f}", f"{r['battery_wh']:.0f}", f"{r['Kp']:.2f}",
          f"{r['Kd']:.2f}", int(r["fleet_size"]), f"{r['pointing_error_deg']:.5f}",
          f"{r['unit_cost_usd']:,.0f}", f"{r['fleet_cost_usd']:,.0f}",
          f"{r['log V K=2']:+.4f}", f"{r['log V K=1']:+.4f}", f"{r['term 1 level']:+.4f}",
          f"{r['term 2 level']:+.4f}", _marks(r))
         for _, r in w.iterrows()],
    ))  # fmt: skip


def decision_designs() -> Md:
    """Appendix D's table of the shortlist, computed from the data of record (one call)."""
    return decision_designs_table(decision())


def decision_detail() -> Md:
    """What the fit adds to a two-measure view, computed from the data of record (one call)."""
    return decision_detail_sentence(decision())
