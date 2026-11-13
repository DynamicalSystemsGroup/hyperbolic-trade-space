"""Are the tau = inf guard stops duplicate facets (two identical planes)?"""
import numpy as np
from sklearn.utils import check_random_state
from hyperbolic_trade_space.datasets import make_frontier_data
from hyperbolic_trade_space.solvers import _solve_terms_once
kw = {"min_exponent": 0.0, "penalty": None, "alpha": 0.0, "tol": 1e-10, "max_iter": 500}
seeds5 = check_random_state(0).randint(0, 2**31 - 1, size=5)
for s, j in [(0, 0), (0, 3), (1, 3), (3, 2), (8, 2), (9, 1), (9, 3), (16, 1), (17, 4)]:
    U = np.log(make_frontier_data(400, 4, n_terms=3, random_state=s)[0])
    r = _solve_terms_once(U, 3, np.inf, seeds5[j], 50, kw)
    D = np.abs(r.W[:, None] - r.W[None]).max(-1)
    iu = np.triu_indices(3, 1)
    S = U @ r.W.T - r.beta
    ties = (np.sort(S, 1)[:, -1] - np.sort(S, 1)[:, -2] < 1e-12).sum()
    print(f"seed {s:2d} restart {j}: {r.message!r:22s} min pairwise |W_k - W_l|_inf = {D[iu].min():.1e}; "
          f"rows tied to 1e-12: {ties}; facet sizes {np.bincount(r.labels, minlength=3).tolist()}")
