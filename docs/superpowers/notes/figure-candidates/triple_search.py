"""The S-5 search: every metric triple, both regimes, K = 1, 2, 3.

Run from the repository root::

    uv run python \
        docs/superpowers/notes/figure-candidates/triple_search.py OUT

For each of the 56 triples of the eight metrics on each regime the
triple's columns are conditioned as the case conditions them (per
column) and the temperature is selected by the case's rule at each K
(``case.fit_study``). Per term the search records the rows in its cell,
the near-frontier rows in it (|score| < 1/tau), the contending set (the
exact-maximum exponents on the cell's rows above ``SUPPORT``) and the
largest exponent change over 3 restarts and 4 bootstrap resamples,
terms matched by nearest exponent vector. A term has a real region when
its cell holds at least ``MIN_NEAR`` near-frontier designs (the case's
guard for an association reading, ten) and the change is at most
``TOL`` and the fit's certificate status is ``certified`` (K >= 2;
at K = 1 there is one term and no certificate). ``texture`` counts
real regions with pairwise different contending sets.
"""

import itertools
import json
import sys
import warnings
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "examples" / "adcs"), str(ROOT / "scripts")]
import case  # noqa: E402
import k_terms  # noqa: E402

MIN_NEAR = case.MIN_NEAR_FRONTIER
TOL = 0.10
# an exact-maximum exponent counts in the support from the case's
# co-contender level
SUPPORT = case.CO_CONTENDER


def _match(W0, W1):
    """Per base term, exponent change to its nearest refit term."""
    d = np.abs(W0[:, None, :] - W1[None, :, :]).max(axis=2)
    return d.min(axis=1)


def one(args):
    try:
        return _one(args)
    except (
        Exception
    ) as e:  # a fit that cannot be made is a row, not a crash
        regime, tri = args
        return [
            dict(
                regime=regime,
                triple=list(tri),
                K=0,
                status=f"error {type(e).__name__}: {e}",
            )
        ]


def _one(args):
    warnings.simplefilter("ignore")
    regime, tri = args
    st = case.load_study(regime)
    attrs = tuple(st.attrs[j] for j in tri)
    cond, M = case._condition(st.feasible, attrs, st.spec)
    sub = case.Study(
        st.spec, regime, st.raw, st.feasible, attrs, M, cond
    )
    rows = []
    rng = np.random.default_rng(0)
    for K in (1, 2, 3):
        rec = dict(
            regime=regime, triple=[st.names[j] for j in tri], K=K
        )
        try:
            f = case.fit_study(sub, K=K)
        except ValueError:
            rec["status"] = "tau not bracketed"
            rows.append(rec)
            continue
        est = f.estimator
        W = np.atleast_2d(est.exponents_)
        try:
            reps = case.term_reports(est, M, f.band)
        except (
            ValueError
        ) as e:  # a term with under two near-frontier rows
            rec["status"] = f"no report: {e}"
            rows.append(rec)
            continue
        lab = est.assign_cells(M) if K > 1 else np.zeros(len(M), int)
        dev = np.zeros(K)
        if K > 1:
            fits = [(M, s) for s in (1, 2, 3)]
            for _ in range(4):
                fits.append((M[rng.integers(0, len(M), len(M))], 0))
            for X, s in fits:
                try:
                    W1 = np.atleast_2d(
                        k_terms.fit_k(X, K, f.tau, s).exponents_
                    )
                    dev = np.maximum(dev, _match(W, W1))
                except (
                    ValueError
                ):  # a refit that cannot be made is unstable
                    dev[:] = np.inf
        try:
            status = (
                k_terms.certificate(est)["status"]
                if K > 1
                else "not_applicable"
            )
        except Exception as e:
            status = f"error {type(e).__name__}"
        cert_ok = status in ("certified", "not_applicable")
        terms = []
        for k, r in enumerate(reps):
            ex = np.zeros(len(tri))
            ex[list(r.contending_set)] = r.contending_exponents
            cs = [int(j) for j in np.nonzero(ex >= SUPPORT)[0]]
            terms.append(
                dict(
                    rows=int((lab == k).sum()),
                    near=int(r.n_near_frontier),
                    contending=cs,
                    exact=[round(float(x), 3) for x in ex],
                    dev=round(float(min(dev[k], 9.0)), 3),
                    w=[round(float(x), 3) for x in W[k]],
                    real=bool(
                        r.n_near_frontier >= MIN_NEAR
                        and dev[k] <= TOL
                        and cert_ok
                    ),
                )
            )
        real = [t for t in terms if t["real"]]
        rec.update(
            tau=round(f.tau, 2),
            status=status,
            terms=terms,
            n_real=len(real),
            texture=len({tuple(t["contending"]) for t in real}),
        )
        rows.append(rec)
    return rows


def main():
    sel = (
        int(sys.argv[2]) if len(sys.argv) > 2 else None
    )  # a quick test
    jobs = [
        (r, t)
        for r in ("primary", "stock")
        for t in itertools.combinations(range(8), 3)
    ]
    jobs = jobs[:sel] if sel else jobs
    with Pool(8) as p:
        out = [x for rows in p.imap(one, jobs) for x in rows]
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
