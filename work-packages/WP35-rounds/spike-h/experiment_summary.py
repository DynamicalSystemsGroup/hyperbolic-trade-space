"""Step 3 (repository environment): the experiment's tables of rates and counts.

    uv run python work-packages/WP35-rounds/spike-h/experiment_summary.py <tables.npz> \
        <results_methods.json> <results.json> > summary.txt
"""

import json
import sys
from collections import defaultdict

import numpy as np

THRESH = 0.9
R_LIST = ["0.25", "1.0", "3.0"]


def unit(v):
    return v / np.linalg.norm(v)


def chance(d=4, n=400_000, seed=0):
    rng = np.random.default_rng(seed)
    g = rng.standard_normal((n, d))
    g /= np.linalg.norm(g, axis=1, keepdims=True)
    x = rng.dirichlet(np.ones(d), n)
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    w = rng.dirichlet(np.ones(d), n)
    w /= np.linalg.norm(w, axis=1, keepdims=True)
    return float((np.abs(g[:, 0]) >= THRESH).mean()), float(((x * w).sum(1) >= THRESH).mean())


def cell_of(name):
    p = name.split("/")
    return "/".join(p[:-1]) if p[0] != "D" else name


def main(tables, methods, out):
    T = np.load(tables)
    with open(methods, encoding="utf-8") as fh:
        M = json.load(fh)
    rows = defaultdict(lambda: defaultdict(list))
    detail = {}
    for name, res in M.items():
        W, fit = T[f"{name}/w"], T[f"{name}/fit"]
        cell = cell_of(name)
        for ti, w in enumerate(W):
            key = cell if len(W) == 1 else f"{cell}#term{ti + 1}"
            f = fit[ti]
            ours = float(unit(f) @ unit(w))
            r = rows[key]
            r["ours_cos"].append(ours)
            r["ours_l1"].append(float(np.abs(f - w).sum()))
            r["pca_pc1"].append(res["pca"]["k1"][ti]["first"])
            r["pca_span2"].append(res["pca"]["k2"][ti]["span"])
            r["pca_last"].append(res["pca"]["last"][ti]["first"])
            r["pca_any"].append(res["pca"]["all"][ti]["best"])
            for R in R_LIST:
                h = res["horopca"][R]
                for k in (1, 2):
                    runs = h[f"k{k}"]["runs"]
                    b = runs[h[f"k{k}"]["best"]]["scores"][ti]
                    allr = [x["scores"][ti]["best"] for x in runs]
                    r[f"h{R}k{k}_best"].append(b["best"] if k == 1 else b["span"])
                    r[f"h{R}k{k}_rec"].append(
                        sum(a >= THRESH for a in allr)
                        if k == 1
                        else sum(x["scores"][ti]["span"] >= THRESH for x in runs)
                    )
                    r[f"h{R}k{k}_min"].append(
                        min(allr) if k == 1 else min(x["scores"][ti]["span"] for x in runs)
                    )
                    r[f"h{R}k{k}_max"].append(
                        max(allr) if k == 1 else max(x["scores"][ti]["span"] for x in runs)
                    )
        detail[name] = {"sd_w": float(T[f"{name}/sd"][0]), "sd_top_orth": float(T[f"{name}/sd"][1])}
    ch_dir, ch_simplex = chance()
    print(
        f"threshold |cos| >= {THRESH}; chance rate: uniform random direction in R^4 {ch_dir:.3f}; "
        f"random simplex point (this work) {ch_simplex:.3f}\n"
    )
    res_out = {
        "threshold": THRESH,
        "chance_direction": ch_dir,
        "chance_simplex": ch_simplex,
        "cells": {},
    }
    hdr = (
        "cell",
        "tables",
        "ours rec",
        "ours cos med [min,max]",
        "ours L1 med",
        "PCA PC1 rec",
        "PC1 cos med",
        "PCA 2-span rec",
        "PCA last rec",
    )
    print(" | ".join(hdr))
    for key in sorted(rows):
        r = rows[key]
        n = len(r["ours_cos"])
        rec = lambda xs: sum(x >= THRESH for x in xs)  # noqa: E731
        sdw = [detail[nm]["sd_w"] for nm in M if cell_of(nm) == key.split("#")[0]]
        sdo = [detail[nm]["sd_top_orth"] for nm in M if cell_of(nm) == key.split("#")[0]]
        c = {
            "n": n,
            "ours_rec": rec(r["ours_cos"]),
            "ours_cos": [
                float(np.median(r["ours_cos"])),
                float(min(r["ours_cos"])),
                float(max(r["ours_cos"])),
            ],
            "ours_l1_median": float(np.median(r["ours_l1"])),
            "pca_pc1_rec": rec(r["pca_pc1"]),
            "pca_pc1_cos_median": float(np.median(r["pca_pc1"])),
            "pca_span2_rec": rec(r["pca_span2"]),
            "pca_last_rec": rec(r["pca_last"]),
            "pca_any_rec": rec(r["pca_any"]),
            "spread_ratio_empirical_median": float(np.median(np.array(sdw) / np.array(sdo))),
        }
        for R in R_LIST:
            for k in (1, 2):
                c[f"horo_R{R}_k{k}"] = {
                    "best_rec": rec(r[f"h{R}k{k}_best"]),
                    "best_median": float(np.median(r[f"h{R}k{k}_best"])),
                    "restart_min": float(min(r[f"h{R}k{k}_min"])),
                    "restart_max": float(max(r[f"h{R}k{k}_max"])),
                    "restarts_recovering": int(sum(r[f"h{R}k{k}_rec"])),
                    "restarts_total": 5 * n,
                }
        res_out["cells"][key] = c
        print(
            f"{key} | {n} | {c['ours_rec']}/{n} | {c['ours_cos'][0]:.3f} [{c['ours_cos'][1]:.3f},"
            f"{c['ours_cos'][2]:.3f}] | {c['ours_l1_median']:.3f} | {c['pca_pc1_rec']}/{n} | "
            f"{c['pca_pc1_cos_median']:.3f} | {c['pca_span2_rec']}/{n} | {c['pca_last_rec']}/{n}"
        )
    print(
        "\nHoroPCA (k=1: |cos| of the first ideal point; k=2: span alignment). best-loss restart"
        " recovering / tables;"
        " [min, max] over all restarts of all tables in the cell; restarts recovering / restarts"
    )
    for key in sorted(res_out["cells"]):
        c = res_out["cells"][key]
        parts = []
        for R in R_LIST:
            for k in (1, 2):
                h = c[f"horo_R{R}_k{k}"]
                parts.append(
                    f"R={R} k={k}: {h['best_rec']}/{c['n']} med {h['best_median']:.2f} "
                    f"[{h['restart_min']:.2f},{h['restart_max']:.2f}] "
                    f"{h['restarts_recovering']}/{h['restarts_total']}"
                )
        print(f"{key} | " + " | ".join(parts))
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res_out, fh, indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
