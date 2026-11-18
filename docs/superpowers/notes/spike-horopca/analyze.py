"""Step C: tables for the readout from results.json (HoroPCA subsample) and tables.npz (PCA on every row).

    python analyze.py tables.npz results.json
"""
import json, sys
import numpy as np

T = np.load(sys.argv[1], allow_pickle=True)
R = json.load(open(sys.argv[2], encoding="utf-8"))
unit = lambda v: v / np.linalg.norm(v, axis=-1, keepdims=True)


def span(Q, w):
    B, _ = np.linalg.qr(Q.T)
    return float(np.linalg.norm(B.T @ unit(w)))


for name, r in R.items():
    L = T[f"{name}/logM"]
    Lc = L - L.mean(0)
    _, S, Vt = np.linalg.svd(Lc, full_matrices=False)
    ev = S**2 / (S**2).sum()
    print(f"\n=== {name}  (full table n={len(L)}, d={L.shape[1]}; HoroPCA on n={r['n']})")
    print("PCA explained variance PC1..4 (all rows):", np.round(ev[:4], 3), " PC1+PC2:", round(ev[:2].sum(), 3))
    tg = {}
    if f"{name}/planted" in T.files:
        tg.update({f"planted t{i+1}": w for i, w in enumerate(T[f"{name}/planted"])})
    tg.update({f"fitK1 t{i+1}": w for i, w in enumerate(T[f"{name}/fitK1"])})
    tg.update({f"fitK2 t{i+1}": w for i, w in enumerate(T[f"{name}/fitK2"])})
    if f"{name}/planted" in T.files:
        P = T[f"{name}/planted"]
        for tn, w in tg.items():
            if tn.startswith("fit"):
                best = max(abs(unit(w) @ unit(p)) for p in P)
                print(f"   cos({tn}, nearest planted term) = {best:.3f}")
    print("PCA (all rows)  target: [best-PC index (|cos|)] | span(PC1) span(PC1,2)")
    for tn, w in tg.items():
        c = np.abs(Vt @ unit(w))
        print(f"   {tn:12s} PC{c.argmax()+1} ({c.max():.2f}) | {span(Vt[:1], w):.2f} {span(Vt[:2], w):.2f}   w={np.round(w, 2)}" if len(w) <= 4 else
              f"   {tn:12s} PC{c.argmax()+1} ({c.max():.2f}) | {span(Vt[:1], w):.2f} {span(Vt[:2], w):.2f}")
    print("HoroPCA (subsample), best of 5 runs by loss. R_max: FM-offset | k=1 expl, k=2 expl | span k=1, k=2 per target (unreflected) | run-to-run explained range")
    for R_, e in r["horopca"].items():
        row = f"   R={R_}: |mu|={e['frechet_mean_norm']:.3f} | {e['k1']['best']['explained']:.3f}, {e['k2']['best']['explained']:.3f}"
        for k in ("k1", "k2"):
            lo, hi = min(e[k]["explained_all_runs"]), max(e[k]["explained_all_runs"])
            row += f" [{k} runs {lo:.3f}-{hi:.3f}]"
        print(row)
        for tn in tg:
            key = tn.replace("fitK", "fit K=").replace("planted t", "planted t")
            s1 = e["k1"]["best"]["scores_unreflected"][key]["best_cos"]
            s2 = e["k2"]["best"]["scores_unreflected"][key]["span"]
            print(f"        {tn:12s} k=1 |cos| {s1:.2f}   k=2 span {s2:.2f}")
    print("PCA (subsample) explained k=1,2:", round(r["pca"]["k1"]["explained"], 3), round(r["pca"]["k2"]["explained"], 3))

# --- loadings beside exponents (cubesat primary, planted K=1), and the Frechet-mean offsets
print("\n=== loadings beside exponents")
for name in ("cubesat_primary", "planted_K1_s0"):
    L = T[f"{name}/logM"]; Lc = L - L.mean(0)
    _, S, Vt = np.linalg.svd(Lc, full_matrices=False)
    names_ = list(T[f"{name}/names"]) if f"{name}/names" in T.files else [f"m{j+1}" for j in range(L.shape[1])]
    w = T[f"{name}/fitK1"][0]
    print(name)
    print(f"  {'metric':28s} {'fit K=1 w':>9s} {'PC1':>7s} {'PC2':>7s}")
    for j, nm in enumerate(names_):
        print(f"  {nm:28s} {w[j]:9.3f} {Vt[0,j]*np.sign(Vt[0].sum()):7.3f} {Vt[1,j]:7.3f}")
    print("  PC1 sign-pure:", bool(np.all(Vt[0] >= 0) or np.all(Vt[0] <= 0)), " PC2 sign-pure:", bool(np.all(Vt[1] >= 0) or np.all(Vt[1] <= 0)),
          " fit w sum:", round(float(w.sum()), 3), " zero exponents:", int((w < 1e-6).sum()))
print("\nFrechet-mean offsets |mu| (Poincare ball):")
for name, r in R.items():
    print(" ", name, {k: float(f"{e['frechet_mean_norm']:.2e}") for k, e in r["horopca"].items()}, "converged", all(e["frechet_converged"] for e in r["horopca"].values()))
