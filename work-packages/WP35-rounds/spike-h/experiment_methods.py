"""Step 2 (the spike's own environment, never the repository's): PCA and HoroPCA on the tables.

    python experiment_methods.py <HoroPCA clone> <earlier spike dir> <tables.npz> \
        <results_methods.json> [workers]

The embedding and the repository calls are those of the earlier spike
(docs/superpowers/notes/spike-horopca/run_horopca.py): centre, one scale so the farthest point has
tangent norm R, exponential map at the origin, Frechet mean and reflection, HoroPCA.fit
(Adam, lr 0.05, 500 steps) from 5 random restarts (torch seeds 0 to 4). Every restart is recorded.
"""

import json
import multiprocessing as mp
import sys
from pathlib import Path

import numpy as np

R_LIST, K_LIST, SEEDS_TORCH = [0.25, 1.0, 3.0], [1, 2], range(5)


def unit(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def scores(Qs, W):
    """Per target: |cos| of each row of Qs, the best and first of them, and the span alignment."""
    B, _ = np.linalg.qr(Qs.T)
    out = []
    for w in W:
        c = np.abs(unit(Qs) @ unit(w))
        out.append(
            {
                "cos": c.tolist(),
                "best": float(c.max()),
                "first": float(c[0]),
                "span": float(np.linalg.norm(B.T @ unit(w))),
            }
        )
    return out


def work(args):
    clone, spike, name, L, W = args
    import torch

    torch.set_num_threads(1)
    sys.path.insert(0, clone)
    sys.path.insert(0, spike)
    import compat

    compat.install()
    import geom.poincare as poincare
    from learning.frechet import Frechet
    from learning.pca import HoroPCA
    from utils.metrics import frechet_var_approx

    torch.set_default_dtype(torch.float64)
    n, d = L.shape
    Lc = L - L.mean(0)
    _u, S, Vt = np.linalg.svd(Lc, full_matrices=False)
    ev = S**2 / (S**2).sum()
    res = {
        "n": n,
        "d": d,
        "pca": {
            "explained": ev.tolist(),
            "k1": scores(Vt[:1], W),
            "k2": scores(Vt[:2], W),
            "all": scores(Vt, W),
            "last": scores(Vt[-1:], W),
        },
        "horopca": {},
    }
    for R in R_LIST:
        s = np.linalg.norm(Lc, axis=1).max() / R
        z = poincare.expmap0(torch.from_numpy(Lc / s))
        mu, conv = Frechet(lr=1e-2, eps=1e-5, max_steps=5000).mean(z, return_converged=True)
        x = poincare.reflect_at_zero(z, mu)
        v_orig = frechet_var_approx(poincare.pairwise_distance(x))
        ent = {"frechet_mean_norm": float(mu.norm()), "frechet_converged": bool(conv)}
        for k in K_LIST:
            runs = []
            for sd in SEEDS_TORCH:
                torch.manual_seed(sd)
                m = HoroPCA(dim=d, n_components=k, lr=5e-2, max_steps=500)
                m.fit(x, iterative=False, optim=True)
                Q = m.get_components().detach()
                with torch.no_grad():
                    loss = float(m.compute_loss(x, Q))
                    v_proj = frechet_var_approx(poincare.pairwise_distance(m._project(x, Q)))
                Qb = poincare.reflect_at_zero(Q, mu).numpy()
                runs.append(
                    {
                        "seed": sd,
                        "loss": loss,
                        "explained": float(v_proj / v_orig),
                        "scores": scores(Qb, W),
                    }
                )
            ent[f"k{k}"] = {"runs": runs, "best": int(np.argmin([r["loss"] for r in runs]))}
        res["horopca"][str(R)] = ent
    print(name, "done", flush=True)
    return name, res


if __name__ == "__main__":
    clone, spike, tables, outp = sys.argv[1:5]
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    T = np.load(tables)
    names = sorted({k[: -len("/logM")] for k in T.files if k.endswith("/logM")})
    jobs = [(clone, str(Path(spike)), nm, T[f"{nm}/logM"], T[f"{nm}/w"]) for nm in names]
    with mp.get_context("spawn").Pool(workers) as pool:
        results = dict(pool.imap_unordered(work, jobs))
    with open(outp, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=0)
