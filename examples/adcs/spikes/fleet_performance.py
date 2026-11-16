"""WP56 spike: three candidate definitions of a fleet-performance aggregate for the cubesat case.

Run ``MPLCONFIGDIR=... uv run --frozen python examples/adcs/spikes/fleet_performance.py``.

Each candidate is a function of the fleet size n and the pointing error e of a design (columns of
the data of record), increasing in n with diminishing returns and decreasing in e. Each is fitted
with the unit cost and the fleet cost as a three-metric table (the costs conditioned as the case
conditions them, smaller is better; the aggregate larger is better), at K = 1 and K = 2 with the
case's temperature rule, and drawn as a ternary. The decision's rules of Section 9 are applied to
each fit's shortlist and the picks compared across the definitions and across their constants.
Writes ``fleet_performance.json`` and ``work-packages/WP56-rounds/ternary/<candidate>.png``.
Nothing here changes the case code, the data or the model.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(ROOT / "paper"))

import case  # noqa: E402

E_REQ = case.CUBESAT.requirements["pointing_error_deg"][0]  # the pointing requirement, degree
OUT_DIR = ROOT / "work-packages" / "WP56-rounds" / "ternary"
PERF = "fleet_performance"
UNIT, FLEET = "unit_cost_usd", "fleet_cost_usd"
ATTRS = (FLEET, UNIT, PERF)  # corners: sponsor, manufacturer, operator
RULES = ("sponsor", "manufacturer", "operator", "between", "balanced")


# ---- the candidates: n fleet size, e pointing error (degree), constants as keyword arguments


def coverage(n, e, p0, e0):
    """(a) Coverage of a target set by n independent satellites, each succeeding with p(e).

    p(e) = p0 exp(-e / e0); P = 1 - (1 - p(e))^n, the probability that a target is covered by at
    least one satellite in the planning period (dimensionless, in [0, 1)).
    """
    return 1.0 - (1.0 - p0 * np.exp(-e / e0)) ** n


def capacity(n, e, n0, e0):
    """(b) Observation capacity: n / (1 + n / n0) satellite-equivalents times e0 / (e0 + e)."""
    return n / (1.0 + n / n0) * e0 / (e0 + e)


def revisit(n, e, n0, ew, t0=1.0):
    """(c) Refreshes per day: one over (latency t0 + revisit time T1 / (n w(e))), n0 = T1 / t0.

    w(e) = exp(-(e / ew)^2) is the share of a footprint that still holds the target when the
    pointing is off by e; the revisit time of one satellite is T1 = n0 t0 days.
    """
    w = np.exp(-((e / ew) ** 2))
    return 1.0 / (t0 * (1.0 + n0 / (n * w)))


CANDIDATES = {
    "coverage": {
        "fn": coverage,
        "label": "coverage probability",
        "base": {"p0": 0.2, "e0": E_REQ},
        "levels": {"p0": (0.1, 0.4), "e0": (E_REQ / 2, 2 * E_REQ)},
    },
    "capacity": {
        "fn": capacity,
        "label": "observation capacity",
        "base": {"n0": 10.0, "e0": E_REQ},
        "levels": {"n0": (5.0, 20.0), "e0": (E_REQ / 2, 2 * E_REQ)},
    },
    "revisit": {
        "fn": revisit,
        "label": "refresh rate",
        "base": {"n0": 10.0, "ew": E_REQ},
        "levels": {"n0": (5.0, 20.0), "ew": (E_REQ / 2, 2 * E_REQ)},
    },
}


# ---- the three-metric study


def make_study(name, consts, regime="primary", spec0=case.CUBESAT):
    """The feasible designs of a regime with the aggregate added, conditioned on three metrics."""
    full = case.load_study(regime, spec0)
    df = full.feasible.copy()
    df[PERF] = CANDIDATES[name]["fn"](
        df["fleet_size"].to_numpy(float), df["pointing_error_deg"].to_numpy(float), **consts
    )
    spec = case.with_spec(
        spec0,
        attributes=ATTRS,
        short={**spec0.short, PERF: "fleet performance"},
        units={**spec0.units, PERF: "aggregate"},
        orientation={**spec0.orientation, PERF: +1},
    )
    cond, M = case._condition(df, ATTRS, spec)
    return case.Study(spec, regime, full.raw, df, ATTRS, M, cond)


def fit_pair(study):
    return {1: case.fit_study(study, 1), 2: case.fit_study(study, 2)}


def _signs(rep):
    names = ("fleet cost", "unit cost", "fleet performance")
    out = {}
    for i, j in ((0, 1), (0, 2), (1, 2)):
        out[f"{names[i]} / {names[j]}"] = round(float(rep.association[i, j]), 3)
    return out


def fit_record(study, fits):
    """The fit table of one candidate: the facts the readout reports."""
    band = fits[1].band
    names = study.names
    rec = {"band": band}
    for K, fit in fits.items():
        est = fit.estimator
        reps = case.term_reports(est, study.M, band)
        terms = []
        for k, rep in enumerate(reps):
            thin = not case.has_reading(rep)
            terms.append(
                {
                    "term": k + 1,
                    "exponents": {
                        n: round(float(w), 4) for n, w in zip(names, rep.exponents, strict=True)
                    },
                    "contending set": case._sorted_contending(rep, names),
                    "n_lemma": int(rep.n_lemma),
                    "near-frontier": int(rep.n_near_frontier),
                    "elasticities": {
                        f"{names[i]} wrt {names[j]}": round(float(rep.elasticities[i, j]), 3)
                        for i in range(3)
                        for j in range(3)
                        if i != j and np.isfinite(rep.elasticities[i, j])
                    },
                    "association": None if thin else _signs(rep),
                    "share": float(est.term_share_[k]) if K > 1 else 1.0,
                    "rows": int(np.bincount(est.cell_, minlength=K)[k]) if K > 1 else len(study.M),
                }
            )
        rec[f"K={K}"] = {"tau": fit.tau, "terms": terms}
    lv1 = np.abs(fits[1].estimator.score_samples(study.M))
    rec["near-frontier at the K=1 band, K=1 fit"] = int((lv1 < band).sum())
    return rec


# ---- the decision rules of Section 9 on a three-metric fit


def decide(study, fits):
    """The shortlist and the picks of each rule, as design ids, with the top five by level."""
    df, M = study.feasible, study.M
    f1, f2 = fits[1], fits[2]
    six = case.requirement_mask(df, study.spec, costs=True).to_numpy()
    lv1 = f1.estimator.score_samples(M)
    lv2 = f2.estimator.score_samples(M)
    work = six & (np.abs(lv1) < f1.band) & (np.abs(lv2) < f1.band)
    lev = np.log(M) @ f2.estimator.exponents_.T - f2.estimator.log_offset_
    out = df.assign(lv1=lv1, lv2=lv2, gap=np.abs(lev[:, 0] - lev[:, 1]))
    w = out[work].sort_values([FLEET, "design_id"]).reset_index(drop=True)
    p, f = w[PERF].to_numpy(), w[FLEET].to_numpy()
    scaled = np.column_stack([(p.max() - p) / np.ptp(p), (f - f.min()) / np.ptp(f)])
    idx = {
        "sponsor": int(np.argmin(f)),
        "manufacturer": int(np.argmin(w[UNIT].to_numpy())),
        "operator": int(np.argmax(p)),
        "between": int(np.argmin(scaled.max(axis=1))),
        "balanced": int(np.argmin(w["gap"].to_numpy())),
    }
    top = w.sort_values(["lv2", "design_id"], ascending=[False, True]).head(5)
    return {
        "n_feasible": len(df),
        "n_six_pass": int(six.sum()),
        "n_shortlist": len(w),
        "shortlist_ids": [int(i) for i in w["design_id"]],
        "picks": {r: int(w.iloc[i]["design_id"]) for r, i in idx.items()},
        "top5_by_level": [int(i) for i in top["design_id"]],
    }, w


def describe(df, design_id):
    r = df[df["design_id"] == design_id].iloc[0]
    return {
        "design_id": int(design_id),
        "fleet_size": int(r["fleet_size"]),
        "wheel": r["wheel_class"],
        "tracker": r["st_grade"],
        "pointing_error_deg": float(r["pointing_error_deg"]),
        "unit_cost_usd": float(r[UNIT]),
        "fleet_cost_usd": float(r[FLEET]),
    }


def within_section9(name, consts, s9):
    """The operator's and the in-between pick on Section 9's shortlist (the 13-metric fits').

    Only the definition of the aggregate moves; the sponsor's and manufacturer's picks do not
    depend on it.
    """
    w = s9.working
    p = CANDIDATES[name]["fn"](
        w["fleet_size"].to_numpy(float), w["pointing_error_deg"].to_numpy(float), **consts
    )
    f = w[FLEET].to_numpy()
    scaled = np.column_stack([(p.max() - p) / np.ptp(p), (f - f.min()) / np.ptp(f)])
    ids = {"operator": int(np.argmax(p)), "between": int(np.argmin(scaled.max(axis=1)))}
    return {r: describe(w, int(w.iloc[i]["design_id"])) for r, i in ids.items()}


# ---- the ternary of one candidate


def figure(name, study, fit, consts, formula):
    from matplotlib.lines import Line2D

    _, _, plotting = case._lib()
    plt = case._plt()
    est = fit.estimator
    scheme = "light"
    width, height, side = 5.6, 5.5, 3.7

    @case._legible
    def draw():
        fig = plt.figure(figsize=(width, height))
        with case._ternary_house_style():
            sch = plotting._TERN_SCHEMES[scheme]
            ax = fig.add_axes([0.9 / width, 1.45 / height, side / width, side / height])
            plotting.plot_ternary(
                est, study.M, names=list(study.names), lines=True, ax=ax, scheme=scheme
            )
            case._ternary_border_and_callouts(ax, est, study.M, scheme)
            ax.set_title(
                formula,
                loc="left",
                fontsize=case.FIGURE_MIN_FONT_PT + 2,
                fontweight="bold",
                color=sch["ink"],
            )
            col = plotting._ternary_colours(est.exponents_)
        ink = sch["ink"]
        keys = [
            Line2D([], [], marker="o", ls="", ms=7, mfc=sch["dots"], mec=sch["plate"]),
            Line2D([], [], color=case._TERN_BORDER[scheme], lw=2.2, ls=(0, (6, 3))),
        ]
        text = [
            "a design, placed by its shares of the three metrics",
            "dashed line: where the leading term changes",
        ]
        for k in range(len(est.exponents_)):
            m = plotting._TERN_MARKERS[k][0]
            keys.append(Line2D([], [], marker=m, ls="", ms=10, mfc=col[k], mec=ink, mew=1.1))
            text.append(f"{case._TERN_SHAPE[m]}: the exponent vector of term {k + 1}")
        fig.legend(
            keys,
            text,
            loc="lower center",
            ncol=1,
            frameon=False,
            labelcolor=ink,
            fontsize=case.FIGURE_MIN_FONT_PT + 0.5,
            bbox_to_anchor=(0.5, 0.0),
        )
        return fig

    fig = draw()
    path = OUT_DIR / f"{name}.png"
    fig.savefig(path, dpi=160, facecolor="white")
    plt.close(fig)
    return path


FORMULAS = {
    "coverage": "(a) coverage: 1 - (1 - p(e))^n",
    "capacity": "(b) capacity: n/(1 + n/n0) * e0/(e0 + e)",
    "revisit": "(c) refresh rate: 1/(t0 + T1/(n w(e)))",
}


def main():
    from generate_findings import decision

    s9 = decision()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = {
        "pointing_requirement_deg": E_REQ,
        "regime": "primary",
        "candidates": {},
        "section9_picks": {
            k: describe(s9.working, int(v["design_id"])) for k, v in s9.picks.items()
        },
    }
    base_picks = {}
    for name, c in CANDIDATES.items():
        st = make_study(name, c["base"])
        fits = fit_pair(st)
        dec, _ = decide(st, fits)
        rec = {
            "label": c["label"],
            "constants": c["base"],
            "fit": fit_record(st, fits),
            "decision": dec,
            "picks": {r: describe(st.feasible, i) for r, i in dec["picks"].items()},
            "top5": [describe(st.feasible, i) for i in dec["top5_by_level"]],
            "perf_range": [float(st.feasible[PERF].min()), float(st.feasible[PERF].max())],
            "within_section9_shortlist": within_section9(name, c["base"], s9),
            "figure": str(figure(name, st, fits[2], c["base"], FORMULAS[name]).relative_to(ROOT)),
        }
        base_picks[name] = dec
        # the same designs: how alike the three aggregates rank them
        rec["perf_series"] = st.feasible[PERF].to_numpy()
        rec["_df"] = st.feasible
        # constants varied one at a time by a factor of two each way
        var = []
        for const, levels in c["levels"].items():
            for lv in levels:
                consts = {**c["base"], const: lv}
                s2 = make_study(name, consts)
                f2 = fit_pair(s2)
                d2, _ = decide(s2, f2)
                var.append(
                    {
                        "constant": const,
                        "value": lv,
                        "factor": lv / c["base"][const],
                        "picks": d2["picks"],
                        "top5": d2["top5_by_level"],
                        "picks_described": {
                            r: describe(s2.feasible, i) for r, i in d2["picks"].items()
                        },
                        "within_section9_shortlist": within_section9(name, consts, s9),
                        "n_shortlist": d2["n_shortlist"],
                        "K1 contending": case._sorted_contending(
                            case.term_reports(f2[1].estimator, s2.M, f2[1].band)[0], s2.names
                        ),
                        "same as base": {r: d2["picks"][r] == dec["picks"][r] for r in RULES},
                        "top5 overlap": len(set(d2["top5_by_level"]) & set(dec["top5_by_level"])),
                    }
                )
        rec["variations"] = var
        # the stock-gain regime, base constants
        sk = make_study(name, c["base"], regime="stock")
        fk = fit_pair(sk)
        dk, _ = decide(sk, fk)
        rec["stock"] = {
            "picks": {r: describe(sk.feasible, i) for r, i in dk["picks"].items()},
            "n_shortlist": dk["n_shortlist"],
            "K1 contending": case._sorted_contending(
                case.term_reports(fk[1].estimator, sk.M, fk[1].band)[0], sk.names
            ),
        }
        result["candidates"][name] = rec
    # across the three definitions at the base constants
    names = list(CANDIDATES)
    cross = {"picks": {r: {n: base_picks[n]["picks"][r] for n in names} for r in RULES}}
    cross["same pick across the three"] = {
        r: len(set(cross["picks"][r].values())) == 1 for r in RULES
    }
    cross["same configuration (wheel, tracker, fleet size) across the three"] = {
        r: len(
            {
                (d["wheel"], d["tracker"], d["fleet_size"])
                for n in names
                for d in [result["candidates"][n]["picks"][r]]
            }
        )
        == 1
        for r in RULES
    }
    sets = {n: set(base_picks[n]["shortlist_ids"]) for n in names}
    cross["shortlist overlap"] = {
        f"{a}/{b}": [len(sets[a] & sets[b]), len(sets[a] | sets[b])]
        for i, a in enumerate(names)
        for b in names[i + 1 :]
    }
    cross["top5 overlap"] = {
        f"{a}/{b}": len(set(base_picks[a]["top5_by_level"]) & set(base_picks[b]["top5_by_level"]))
        for i, a in enumerate(names)
        for b in names[i + 1 :]
    }
    ser = pd.DataFrame({n: result["candidates"][n]["perf_series"] for n in names})
    cross["spearman of the aggregates over the feasible designs"] = {
        f"{a}/{b}": round(float(ser[a].corr(ser[b], method="spearman")), 4)
        for i, a in enumerate(names)
        for b in names[i + 1 :]
    }
    df0 = result["candidates"][names[0]]["_df"]
    cross["spearman of each aggregate with the fleet size"] = {
        n: round(float(ser[n].corr(df0["fleet_size"], method="spearman")), 4) for n in names
    }
    cross["spearman of each aggregate with the pointing error"] = {
        n: round(float(ser[n].corr(df0["pointing_error_deg"], method="spearman")), 4) for n in names
    }
    for n in names:
        del result["candidates"][n]["perf_series"], result["candidates"][n]["_df"]
    # stability tallies
    tally = {}
    for n in names:
        v = result["candidates"][n]["variations"]
        tally[n] = {r: sum(not x["same as base"][r] for x in v) for r in RULES}
        tally[n]["variations"] = len(v)
    cross["constants varied: variations (of the variations) where the pick changes"] = tally
    # the coarse reading of each rule: the configuration ranges over the three definitions and over
    # every variation of every constant (fifteen fits), and within Section 9's shortlist
    coarse = {}
    for r in RULES:
        ds = []
        for n in names:
            ds.append(result["candidates"][n]["picks"][r])
            ds += [v["picks_described"][r] for v in result["candidates"][n]["variations"]]
        coarse[r] = {
            "fleet size": [min(d["fleet_size"] for d in ds), max(d["fleet_size"] for d in ds)],
            "trackers": sorted({d["tracker"] for d in ds}),
            "wheels": sorted({d["wheel"] for d in ds}),
            "distinct designs": len({d["design_id"] for d in ds}),
            "fits": len(ds),
        }
    cross["coarse: each rule over the three definitions and every variation"] = coarse
    in9 = {}
    for r in ("operator", "between"):
        ds = []
        for n in names:
            ds.append(result["candidates"][n]["within_section9_shortlist"][r])
            ds += [v["within_section9_shortlist"][r] for v in result["candidates"][n]["variations"]]
        in9[r] = {
            "fleet size": [min(d["fleet_size"] for d in ds), max(d["fleet_size"] for d in ds)],
            "trackers": sorted({d["tracker"] for d in ds}),
            "distinct designs": len({d["design_id"] for d in ds}),
            "design ids": sorted({d["design_id"] for d in ds}),
            "evaluations": len(ds),
            "at base": {
                n: result["candidates"][n]["within_section9_shortlist"][r]["design_id"]
                for n in names
            },
        }
    cross["within Section 9's shortlist (the operator's and the in-between pick)"] = in9
    cross["Section 9's own operator and in-between picks, pointing error as the measure"] = {
        r: result["section9_picks"][r]["design_id"] for r in ("operator", "between")
    }
    result["across"] = cross
    (HERE / "fleet_performance.json").write_text(
        json.dumps(result, indent=1, default=float), encoding="utf-8"
    )
    print("wrote", HERE / "fleet_performance.json")


if __name__ == "__main__":
    main()
