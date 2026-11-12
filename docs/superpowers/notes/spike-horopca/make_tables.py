"""Step A (repository environment): the paper's own tables and our fits, written to tables.npz.

Run: ``uv run python docs/superpowers/notes/spike-horopca/make_tables.py``.
Tables: planted (make_frontier_data, seeds from tests/test_soft_fit.py) and the cubesat log-metrics of
record in both regimes (examples/adcs/case.py, load_study).  For each, our K = 1 and K = 2 fits.
"""
import sys, warnings
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "examples" / "adcs"))
from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data  # noqa: E402
import case as C  # noqa: E402

warnings.simplefilter("ignore")
out = {}

def record(name, X, planted=None):
    out[f"{name}/logM"] = np.log(X)
    if planted is not None:
        out[f"{name}/planted"] = np.atleast_2d(planted)
    return X

# planted tables (seeds as in tests/test_soft_fit.py)
for name, args, kw in [
    ("planted_K1_s0", (400, 4), dict(random_state=0)),
    ("planted_K2_s7", (300, 3), dict(n_terms=2, random_state=7)),
    ("planted_K3_s0", (400, 4), dict(n_terms=3, random_state=0)),
    ("planted_K3_s4", (400, 4), dict(n_terms=3, random_state=4)),
]:
    X, info = make_frontier_data(*args, **kw)
    record(name, X, info["exponents"])
    for K in (1, 2):
        est = HyperbolicTradeSpace(n_terms=K, temperature=50.0, random_state=0).fit(X)
        out[f"{name}/fitK{K}"] = np.atleast_2d(est.exponents_)

# the cubesat tables of record
for regime in ("primary", "stock"):
    st = C.load_study(regime)
    name = f"cubesat_{regime}"
    record(name, st.M)
    out[f"{name}/names"] = np.array(st.names)
    for K in (1, 2):
        ft = C.fit_study(st, K=K)
        out[f"{name}/fitK{K}"] = np.atleast_2d(ft.estimator.exponents_)
        out[f"{name}/tauK{K}"] = np.array(ft.tau)
    print(name, st.M.shape, "tau K1/K2", out[f"{name}/tauK1"], out[f"{name}/tauK2"])
np.savez(Path(__file__).parent / "tables.npz", **out)
print({k: v.shape for k, v in out.items() if "logM" in k})
