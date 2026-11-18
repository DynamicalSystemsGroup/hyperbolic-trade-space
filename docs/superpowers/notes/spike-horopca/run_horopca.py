"""Step B (the spike's own venv, never the repository's): HoroPCA and ordinary PCA on the paper's tables.

    python run_horopca.py <path to the HoroPCA clone> tables.npz results.json

Embedding. Log-metrics are Euclidean coordinates, so HoroPCA's input is made by (i) centring on the
mean of the log-metrics, (ii) dividing by one scalar s so the largest centred norm is R_MAX (a dial
for how far from the origin the cloud sits, hence how hyperbolic the geometry the method sees),
(iii) the exponential map at the origin of the Poincare ball (curvature -1, the repository's
convention: tangent norm r lands at hyperbolic distance 2r from the origin).  Then the repository's
own pipeline: Frechet mean, reflection taking it to the origin, HoroPCA.fit.  The ideal points the
method returns are mapped back by the same (involutive) reflection to the unreflected ball, whose
boundary directions are directions in the centred log-metric space.
"""
import json, sys
from pathlib import Path
import numpy as np
import torch

clone, tables, outp = sys.argv[1:4]
sys.path.insert(0, clone)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compat  # noqa: E402
compat.install()
import geom.poincare as poincare  # noqa: E402
from learning.frechet import Frechet  # noqa: E402
from learning.pca import HoroPCA  # noqa: E402
from utils.metrics import frechet_var_approx  # noqa: E402

torch.set_default_dtype(torch.float64)
T = np.load(tables, allow_pickle=True)
names = sorted({k.split("/")[0] for k in T.files if k.endswith("/logM")})
R_MAXES = [0.25, 1.0, 3.0]  # tangent norm of the farthest point: hyperbolic distance 0.5, 2, 6
N_RUNS = 5
N_MAX = 500  # the repository's variance objective is O(n^2 d) per step with autograd: 2,134 points took >10 min per k=2 run


def unit(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def subspace_alignment(Qs, w):
    """||P_Q w|| for unit w: 1 when w lies in the span of the rows of Qs."""
    B, _ = np.linalg.qr(Qs.T)
    return float(np.linalg.norm(B.T @ unit(w)))


def targets(name):
    out = {}
    if f"{name}/planted" in T.files:
        for i, w in enumerate(T[f"{name}/planted"]):
            out[f"planted t{i+1}"] = w
    for K in (1, 2):
        for i, w in enumerate(T[f"{name}/fitK{K}"]):
            out[f"fit K={K} t{i+1}"] = w
    return out


def score(Qs, tg):
    """Per target: |cos| of the best single component, and the alignment of the span."""
    res = {}
    for tn, w in tg.items():
        cos = np.abs(unit(Qs) @ unit(w))
        res[tn] = {"best_cos": float(cos.max()), "span": subspace_alignment(Qs, w)}
    return res


results = {}
for name in names:
    L = T[f"{name}/logM"]
    if len(L) > N_MAX:  # seeded subsample for HoroPCA only; PCA below uses the same rows
        L = L[np.random.default_rng(0).choice(len(L), N_MAX, replace=False)]
    n, d = L.shape
    tg = targets(name)
    Lc = L - L.mean(0)
    res = {"n": n, "d": d, "pca": {}, "horopca": {}}
    # --- ordinary PCA on the centred log-metrics
    U, S, Vt = np.linalg.svd(Lc, full_matrices=False)
    ev = S**2 / (S**2).sum()
    res["pca"]["explained"] = ev[:3].tolist()
    for k in (1, 2):
        res["pca"][f"k{k}"] = {"explained": float(ev[:k].sum()), "scores": score(Vt[:k], tg)}
    # where along the PC list does each target sit (largest |cos| over all PCs, and which PC)
    res["pca"]["target_best_pc"] = {
        tn: {"pc": int(np.abs(Vt @ unit(w)).argmax()) + 1, "cos": float(np.abs(Vt @ unit(w)).max())}
        for tn, w in tg.items()
    }
    res["pca"]["sign_pure_pc"] = [bool(np.all(v >= 0) or np.all(v <= 0)) for v in Vt[:3]]
    # --- HoroPCA after the embedding
    for R in R_MAXES:
        s = np.linalg.norm(Lc, axis=1).max() / R
        u = torch.from_numpy(Lc / s)
        z = poincare.expmap0(u)
        fr = Frechet(lr=1e-2, eps=1e-5, max_steps=5000)
        mu, conv = fr.mean(z, return_converged=True)
        x = poincare.reflect_at_zero(z, mu)
        tang_check = float(np.abs(poincare.logmap0(z).numpy() - u.numpy()).max())  # tpca == pca
        entry = {"R_max": R, "frechet_mean_norm": float(mu.norm()), "frechet_converged": bool(conv),
                 "logmap_expmap_roundtrip_err": tang_check}
        v_orig = frechet_var_approx(poincare.pairwise_distance(x))
        for k in (1, 2):
            runs = []
            for seed in range(N_RUNS):
                torch.manual_seed(seed)
                m = HoroPCA(dim=d, n_components=k, lr=5e-2, max_steps=500)
                m.fit(x, iterative=False, optim=True)
                Q = m.get_components().detach()
                with torch.no_grad():
                    loss = float(m.compute_loss(x, Q))
                    xp = m._project(x, Q)
                    v_proj = frechet_var_approx(poincare.pairwise_distance(xp))
                # ideal points back to the unreflected ball: boundary directions in log-metric space
                Qb = poincare.reflect_at_zero(Q, mu).numpy()
                Qb = Qb / np.linalg.norm(Qb, axis=1, keepdims=True)
                runs.append({"seed": seed, "loss": loss, "explained": v_proj / v_orig,
                             "scores_unreflected": score(Qb, tg), "scores_reflected": score(Q.numpy(), tg),
                             "Q_unreflected": Qb.tolist()})
            best = min(runs, key=lambda r: r["loss"])
            entry[f"k{k}"] = {"best": best, "explained_all_runs": [r["explained"] for r in runs],
                              "loss_all_runs": [r["loss"] for r in runs]}
            print(name, f"R={R}", f"k={k}", "explained", round(best["explained"], 3),
                  "fm", round(entry["frechet_mean_norm"], 3), flush=True)
        res["horopca"][str(R)] = entry
    results[name] = res
json.dump(results, open(outp, "w", encoding="utf-8"), indent=1)
