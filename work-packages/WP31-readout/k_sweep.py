"""WP31 spike: a K sweep and what the large-K limit does (cubesat, both regimes; planted tables).

    uv run python work-packages/WP31-readout/k_sweep.py cubesat primary  > cubesat-primary.csv
    uv run python work-packages/WP31-readout/k_sweep.py cubesat stock    > cubesat-stock.csv
    uv run python work-packages/WP31-readout/k_sweep.py planted 3 0 10   > planted-K3.csv
    uv run python work-packages/WP31-readout/k_sweep.py planted 2 0 10   > planted-K2.csv

One CSV row per (table, K), all at one fixed temperature (the K = 1 selection for the cubesat,
50 for the planted tables), the solver's defaults, random_state 0. Columns: mean slack, the
smallest term share and smallest row share, the largest term gap, status, assignment margin,
stable radius, the smallest conditioning, the splinter measure (the largest, over terms and
WP31_B (default three) bootstrap resamples, of the summed absolute exponent distance to the
nearest resampled term; at most 2), and for planted tables the planted terms recovered (a fitted term within 0.05 in
largest absolute exponent difference).
"""

import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "examples" / "adcs"))

from hyperbolic_trade_space import HyperbolicTradeSpace as H  # noqa: E402
from hyperbolic_trade_space import make_frontier_data  # noqa: E402

KS = range(1, 9)
B = int(os.environ.get("WP31_B", "3"))
COLS = (
    "table,K,tau,mean_slack,min_term_share,min_row_share,max_gap,status,gamma,radius,"
    "min_conditioning,splinter,recovered_planted,n_planted,spurious"
)


def splinter(M, K, tau, ref):
    """Largest over terms and resamples of the distance to the nearest resampled term."""
    rng = np.random.default_rng(0)
    moved = np.zeros(K)
    for s in range(B):
        W = H(n_terms=K, temperature=tau, random_state=s).fit(M[rng.choice(len(M), len(M))])
        d = np.abs(W.exponents_[:, None] - ref.exponents_).sum(axis=2)
        moved = np.maximum(moved, d.min(axis=0))
    return float(moved.max())


def row(name, M, K, tau, truth=None):
    """One CSV row."""
    e = H(n_terms=K, temperature=tau, random_state=0).fit(M)
    t = e.termination_
    rows = np.bincount(e.cell_, minlength=K) / len(M)
    rec = n = spur = ""
    if truth is not None:
        T = np.asarray(truth)
        d = np.abs(e.exponents_[:, None] - T[None]).max(axis=2)
        rec, n = int((d.min(axis=0) < 0.05).sum()), len(T)
        spur = int((d.min(axis=1) >= 0.05).sum())
    cond = np.nanmin(e.conditioning_)
    return (
        f"{name},{K},{tau:.3f},{e.mean_slack_:.5f},{e.term_share_.min():.4f},{rows.min():.4f},"
        f"{t.max_gap:.2e},{t.status},{t.gamma:.3e},{t.radius:.3e},{cond:.4f},"
        f"{splinter(M, K, tau, e):.3f},{rec},{n},{spur}"
    )


def main(argv):
    """Dispatch."""
    print(COLS)
    if argv[0] == "cubesat":
        import case

        s = case.load_study(argv[1])
        tau = case.fit_study(s, K=1).tau
        for K in KS:
            print(row(argv[1], s.M, K, tau), flush=True)
    else:
        k0, lo, hi = map(int, argv[1:4])
        for seed in range(lo, hi):
            X, info = make_frontier_data(400, 4, n_terms=k0, random_state=seed)
            for K in KS:
                print(row(f"K0={k0}/seed{seed}", X, K, 50.0, info["exponents"]), flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
