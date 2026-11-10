"""Sentences of the paper's case sections whose numbers the case module produces.

Nothing here is typed: every count, temperature and name is read from the objects that
:mod:`case` returns, so the prose regenerates with the data (at the swap of the model, for
example). Each function returns an :class:`~paper_common.Md` of one or two plain sentences.
"""

from __future__ import annotations

import case
import numpy as np
from paper_common import Md, appendix_link
from paper_facets import aligned
from paper_stability import stable, summary

_D11 = appendix_link("sub-d-11", "Appendix D.11")
_D14 = appendix_link("sub-d-14", "Appendix D.14")
_D15 = appendix_link("sub-d-15", "Appendix D.15")


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


_NUMBER_WORDS = {
    2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
    10: "ten",
}  # fmt: skip


def nondominated_sentence(study) -> Md:
    """Nondominated counts of the study's table on each view, with what a range means.

    The sentence stands in section 1, before any other number of the case, so it says what a range
    is: the spread of a number over the regenerations of the data under rounding-level
    perturbation; when no count moves, it says so and what a range would mean.
    """
    df = case.nondominated_counts(study).sort_values("columns")
    n = int(df["of"].iloc[0])
    parts = [
        f"{stable(f'nondominated | {study.regime} | {r.view} | nondominated')} on {int(r.columns)}"
        for r in df.itertuples()
    ]
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
        f"Of {n} feasible cubesat designs, the nondominated sets hold {_and(parts)} attributes "
        f"{tail}."
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
    """How many designs each regime drew and kept."""
    a, b = primary, stock
    return Md(
        f"The primary regime evaluates {len(a.raw)} designs and keeps {len(a.feasible)} as "
        f"feasible; the stock regime evaluates {len(b.raw)} and keeps {len(b.feasible)}. "
        f"Each design carries {len(a.attrs)} attributes."
    )


def temperature_sentence(study, fit) -> Md:
    """The fit temperature and what it leaves above V = 1."""
    r = study.regime
    frac = stable(f"fit | {r} K=1 | frac_above_", lambda v: f"{v:.3f}")
    n_eff = stable(f"fit | {r} K=1 | n_eff_", lambda v: f"{v:.1f}")
    band = stable("sentence | temperature | band", lambda v: f"{v:.4f}")
    return Md(
        f"The fit temperature is tau = {fit.tau:.1f}: a fraction {frac} of "
        f"designs lies above V = 1 (the target is {study.spec.target_frac:.2f}), the band "
        f"1/tau is {band} and the effective sample size is {n_eff} designs."
    )


def k1_sentence(study, fit) -> Md:
    """The K = 1 contending set: the support of the exact-maximum fit, and its exponents."""
    rep = case._reports(study, fit)[0]
    names = _contending(study, fit)
    w = {study.names[j]: float(rep.exponents[j]) for j in rep.contending_set}
    two = lambda n: stable(  # noqa: E731
        f"D exponents K=1 | {study.regime} | {n} | exponent w", lambda v: f"{v:.2f}"
    )
    low, high = min(w, key=w.get), max(w, key=w.get)
    return Md(
        f"At K = 1 the exact-maximum fit has a {len(names)}-lemma across "
        f"{_span(study.spec.subsystems_of(names))}: {_and(names)} contend, with "
        f"exponents at the fit temperature from {two(low)} to {two(high)}."
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
    return Md(
        f"The mean slack falls from {own[1]} at K = 1 to {own[2]} at K = 2 and {own[3]} at "
        f"K = 3, at the temperatures {tau[1]}, {tau[2]} and {tau[3]}; refitted at the K = 1 "
        f"temperature it falls to {fixed[2]} and {fixed[3]} ({_D15}). The "
        f"K = 3 facets have contending sets (exact-maximum supports) of {_and(ft['n_lemma'])} "
        f"metrics; {absent}."
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


def designs_on_a_seam(study, fit) -> tuple[int, int]:
    """The designs whose best-minus-second-best facet score is below the band 1/tau, and all.

    A margin below the band shows only that at least one design is within the band of a seam;
    this is the count. On the committed primary data at K = 3 the nearest gap is about 9 per
    cent of the band away from it, so the count does not move with rounding-level jitter.
    """
    e = fit.estimator
    scores = np.log(study.M) @ np.atleast_2d(e.exponents_).T - e.log_offset_
    top = np.sort(scores, axis=1)
    return int(np.sum(top[:, -1] - top[:, -2] < fit.band)), len(top)


def margin_sentence(study, fits) -> Md:
    """How to read the size of the margin and the stable radius, with this case's values.

    The margin and the radius are read against the band 1/tau and against the median gap between
    a design's best and second-best facet score (Appendix D.8); the designs within the band of a
    seam are counted (:func:`designs_on_a_seam`).
    """
    r, K = study.regime, max(fits)
    four = lambda v: format(v, ".4g")  # noqa: E731
    n, N = designs_on_a_seam(study, fits[K])
    return Md(
        f"At K = {K} the margin is {stable(f'certificate | {r} | {K} | gamma', four)} and the "
        f"stable radius {stable(f'certificate | {r} | {K} | radius', four)}, against a band 1/tau "
        f"of {stable(f'D k_table | {r} | {K} | band 1/tau', lambda v: f'{v:.4f}')} and a median "
        f"best-minus-second-best score of "
        f"{stable(f'margin | {r} | {K} | median margin', lambda v: f'{v:.3f}')}: a margin below "
        f"the band puts at least one design within the band of a seam, here {n} of the {N}, and "
        f"the certificate covers changes under the radius only."
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
        f"the {len(rows)} failures have {_and(rows)} frontier rows on their thinnest facet ({_D14})"
        if same
        else f"the failures differ between the temperatures ({_D14})"
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
    spec = case.CUBESAT
    ga, gb = spec.subsystems_of(sets[a]), spec.subsystems_of(sets[b])
    only = [g for g in ga if g not in gb]
    point = f": {_span(only)} enters only in the {a} regime" if only else ""
    return Md(
        f"The regimes return a {t.loc['n_lemma', a]}-lemma and a {t.loc['n_lemma', b]}-lemma "
        f"sharing {len(sets[a] & sets[b])} metrics ({_and(sorted(sets[a] & sets[b]))}); "
        f"the {a} regime alone has {_and(sorted(sets[a] - sets[b]))}, the {b} regime alone "
        f"{_and(sorted(sets[b] - sets[a]))}. The {b} set spans "
        f"{_span(gb)}{point}."
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

    Reads the same table as :func:`predict_check_sentence`, and the recorded predictions and the
    measured check designs of the spec for what the proposals are: how many distinct
    configurations, and how many meet the model's depth-of-discharge requirement (``dod_ok``),
    which the proposer's training rows (the spec's feasibility flags) do not filter on.
    """
    import pandas as pd

    spec = case.CUBESAT
    n = len(table)
    lv = int(table["log V within band"].sum())
    z = int(table["Z within band"].sum())
    preds = pd.read_csv(spec.data_dir / spec.predictions_file)
    configs = len(preds[list(spec.design_vars) + list(spec.covariates)].drop_duplicates())
    checks = pd.read_csv(spec.data_dir / spec.checks_file)
    dod = int(checks.loc[checks["role"] == "proposal", "dod_ok"].sum())
    k = n - configs + 1
    same = (
        f" {_NUMBER_WORDS.get(k, k).capitalize()} of them are one configuration." if k > 1 else ""
    )
    fail = (
        f" {'All' if dod == 0 else f'{n - dod} of the'} {n} fail the model's depth-of-discharge "
        "requirement: the proposer trains on the designs that settle, stay within the momentum "
        "budget and keep positive power, and its chart has no depth-of-discharge axis."
        if dod < n
        else ""
    )
    return Md(
        f"**What propose, predict, check showed.**{same} It showed that the regressor places "
        "the energy differential of a proposal "
        f"within its band ({lv} of {n}), the easy part. It did not show that it places the "
        f"position along the frontier ({z} of {n}).{fail} "
        f"{_NUMBER_WORDS.get(n, n).capitalize()} proposals illustrate and do not estimate a rate. "
        "A predicted crossing of V = 1 remains a hypothesis."
    )


def planted_sentence() -> Md:
    """The planted example's size."""
    from generate_model import planted_table

    X, info = planted_table()
    k, d = np.asarray(info["exponents"]).shape
    return Md(f"The planted table has {len(X)} rows, {d} metrics and {k} planted facets.")
