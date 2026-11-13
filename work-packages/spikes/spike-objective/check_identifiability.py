"""Seeds 1, 3, 8, 16 at tau = inf: does B's found facet contain the sparse planted facet's frontier
rows exactly (slack < 1e-9) with different exponents? And the dimension of the family of hyperplanes
through those rows: a hyperplane w.u = beta in R^d with sum w = 1 through m affinely independent
points has d - m free parameters (d = 4).
uv run python <folder>/check_identifiability.py
"""

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from methods import evaluate, match, refit_B, solver_init
from objectives import alternate_traced

from hyperbolic_trade_space.datasets import make_frontier_data

for s in [1, 3, 8, 16]:
    X, info = make_frontier_data(400, 4, n_terms=3, random_state=s)
    U = np.log(X)
    fr, fac, Wt = info["frontier_mask"], info["facet"], info["exponents"]
    n_front = np.bincount(fac[fr], minlength=3)
    k_sparse = int(np.argmin(n_front))
    rows = np.where(fr & (fac == k_sparse))[0]
    W, beta, lab, conv, n_iter, _ = alternate_traced(
        U, solver_init(U, 3, 12345), 3, np.inf, refit_B
    )
    perm = match(W, Wt)  # fitted r -> planted perm[r]
    r = int(np.where(perm == k_sparse)[0][0])
    sl = beta[r] - U[rows] @ W[r]
    rank = np.linalg.matrix_rank(np.c_[U[rows], np.ones(len(rows))])
    err, right, _ = evaluate(U, W, beta, lab, np.inf, info)
    print(
        f"seed {s}: sparse planted facet {k_sparse} has {len(rows)} frontier rows (affine rank {rank}); "
        f"found facet matched to it has slack on them {np.round(sl, 10).tolist()}, exponents {W[r].round(3).tolist()} "
        f"vs planted {Wt[k_sparse].round(3).tolist()} (max abs {np.abs(W[r] - Wt[k_sparse]).max():.3f}); "
        f"free parameters of hyperplanes through them: {4 - rank}; run err {err:.3f}, right {right:.2f}"
    )
