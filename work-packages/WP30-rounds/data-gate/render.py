# ruff: noqa  (a record script of the WP30 data gate, kept as run; not part of the package)
"""Render conclusions.json as side-by-side Markdown (old10 | old9 | new9)."""

import json
import sys
from pathlib import Path

q = json.load(open(sys.argv[1]))
C = ["old8", "new8", "new13"]
L = []


def p(s=""):
    L.append(s)


def table(h, rows):
    p()
    p("| " + " | ".join(h) + " |")
    p("|" + "---|" * len(h))
    for r in rows:
        p("| " + " | ".join(str(c) for c in r) + " |")
    p()


def lead(x):
    return ", ".join(f"{n} {w:.3f}" for n, w in x)


def cset(rep):
    return rep["contending set"] if rep else "-"


for r in ("primary", "stock"):
    p(f"## {r} regime")
    rows = []
    for c in C:
        b = q[c][r]
        rows.append(
            [c, b["n_feasible"], len(b["metrics"])]
            + [
                f"{b[f'K{K}']['tau']:.2f} / {b[f'K{K}']['band']:.4f} / {b[f'K{K}']['frac_above_']:.3f} / {b[f'K{K}']['n_eff_']:.1f}"
                for K in (1, 2, 3)
            ]
        )
    table(["config", "feasible", "metrics", "K=1 tau/band/frac/n_eff", "K=2", "K=3"], rows)
    rows = []
    for c in C:
        b = q[c][r]["K1"]
        rep = b.get("report")
        rows.append(
            [
                c,
                cset(rep),
                rep["n_lemma"] if rep else b.get("report_refused"),
                rep["near-frontier"] if rep else "-",
                lead(b["leading"][0]),
                " ".join(f"{w:.3g}" for w in b["exponents"][0]),
            ]
        )
    table(
        ["config", "K=1 contending set", "n-lemma", "near-frontier", "leading", "exponents"], rows
    )
    for K in (2, 3):
        rows = []
        for c in C:
            b = q[c][r][f"K{K}"]
            rep = b["report"]
            tab = rep.get("table")
            for k in range(K):
                t = tab[k] if tab else None
                rows.append(
                    [
                        c,
                        k + 1,
                        b["rows"][k],
                        f"{b['shares'][k]:.3f}",
                        cset(t),
                        t["n_lemma"] if t else "-",
                        t["near-frontier"] if t else "-",
                        lead(b["leading"][k]),
                        f"{b['near_at_k1_band'][k]}/{b['near_at_own_band'][k]}",
                        f"{b['reach'][k]:.4f}",
                    ]
                )
            rows.append(
                [
                    c,
                    "band",
                    rep.get("band", "-"),
                    rep.get("refused_at_k1_band", "")[:160],
                    rep.get("refused_at_own_band", "")[:160],
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
            )
        table(
            [
                "config",
                "term",
                "rows",
                "share",
                f"K={K} contending set",
                "n-lemma",
                "near-frontier (report)",
                "leading exponents",
                "near rows at K1 band / own band",
                "reach",
            ],
            rows,
        )
    rows = []
    for c in C:
        b = q[c][r]
        for K in (1, 2, 3):
            ce = b[f"K{K}"]["certificate"]
            rows.append(
                [
                    c,
                    K,
                    ce["status"],
                    f"{ce['max gap']:.2g}",
                    f"{ce['gamma']:.3g}" if ce["gamma"] == ce["gamma"] else "-",
                    f"{ce['radius']:.3g}" if ce["radius"] == ce["radius"] else "-",
                    f"{b[f'K{K}']['mean_slack_']:.4f}",
                    f"{[x['mean_slack_'] for x in b['mean_slack_fixed_tau'] if x['K'] == K][0]:.4f}",
                    f"{b[f'K{K}']['objective_']:.4f}",
                ]
            )
    table(
        [
            "config",
            "K",
            "status",
            "max gap",
            "gamma",
            "radius",
            "mean slack (own tau)",
            "mean slack (K=1 tau)",
            "objective",
        ],
        rows,
    )
    rows = []
    pairs = sorted({f"{a['metric a']}, {a['metric b']}" for c in C for a in q[c][r]["association"]})
    for pr in pairs:
        row = [pr]
        for c in C:
            m = [a for a in q[c][r]["association"] if f"{a['metric a']}, {a['metric b']}" == pr]
            row.append(
                f"{m[0]['pearson']:+.2f} ({m[0]['spearman']:+.2f})" if m else "(no slew time)"
            )
        rows.append(row)
    table(["pair (pearson (spearman))", *C], rows)
    rows = []
    for k in (
        "power margin, energy balance",
        "available power, energy balance",
        "battery peak power ratio, depth of discharge",
    ):
        rows.append(
            [k]
            + [
                (
                    f"{q[c][r]['redundancy_spearman'].get(k):+.4f}"
                    if q[c][r]["redundancy_spearman"].get(k) is not None
                    else "-"
                )
                for c in C
            ]
        )
    table(["Spearman among feasible designs", *C], rows)
    rows = []
    views = []
    for c in C:
        for v in q[c][r]["nondominated"]:
            if v["view"] not in views:
                views.append(v["view"])
    for v in views:
        row = [v]
        for c in C:
            m = [x for x in q[c][r]["nondominated"] if x["view"] == v]
            row.append(
                f"{m[0]['nondominated']} of {m[0]['of']} on {m[0]['columns']} ({m[0]['share']:.4f})"
                if m
                else "(view does not exist)"
            )
        rows.append(row)
    table(["nondominated view", *C], rows)
p("## regime comparison table (case.regime_comparison)")
for c in C:
    p(f"### {c}")
    table(
        ["quantity", "primary", "stock"],
        [[x["quantity"], x["primary"], x["stock"]] for x in q[c]["regime_comparison"]],
    )
p("## candidates (K = 1, primary)")
for c in C:
    p(f"### {c}")
    table(
        list(q[c]["candidates"][0].keys()),
        [
            [(f"{v:.4g}" if isinstance(v, float) else v) for v in x.values()]
            for x in q[c]["candidates"]
        ],
    )
p("## propose-predict-check (primary)")
for c in ("old8", "new13"):
    pc = q[c]["predict_check"]
    p(f"### {c}: regressor tau {pc['tau']:.4f}, band {pc['band']:.4f}")
    table(
        list(pc["rows"][0].keys()),
        [[(f"{v:.4g}" if isinstance(v, float) else v) for v in x.values()] for x in pc["rows"]],
    )
    table(
        list(q[c]["proposals_refit"][0].keys()),
        [
            [(f"{v:.4g}" if isinstance(v, float) else v) for v in x.values()]
            for x in q[c]["proposals_refit"]
        ],
    )
p("## predictions and checks files")
for c in ("old8", "new13"):
    p(f"### {c}")
    table(
        list(q[c]["predictions_file"][0].keys()),
        [
            [(f"{v:.4g}" if isinstance(v, float) else v) for v in x.values()]
            for x in q[c]["predictions_file"]
        ],
    )
    table(
        list(q[c]["checks_file_flags"][0].keys()),
        [
            [(f"{v:.4g}" if isinstance(v, float) else v) for v in x.values()]
            for x in q[c]["checks_file_flags"]
        ],
    )
Path(sys.argv[2]).write_text("\n".join(L) + "\n")
print("\n".join(L))
