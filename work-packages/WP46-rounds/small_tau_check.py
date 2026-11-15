"""WP46 D-3: the small-temperature fit against a direct minimum-variance fit on the simplex.

    uv run python work-packages/WP46-rounds/small_tau_check.py

The log-metrics of the data of record (primary regime) are centred and of unit spread, so by L22 the
leading term of the soft maximum is (tau/2) w'Cw, C the covariance of the log-metrics. The check
fits the estimator at tau = 3 (the sweep's smallest temperature) and at smaller temperatures, solves
min w'Cw over the simplex directly (SLSQP), and prints the largest gap and the exponents to the
three places the case prints them.
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "examples" / "adcs"), str(ROOT / "src")]

import case  # noqa: E402

import hyperbolic_trade_space as hts  # noqa: E402

study = case.load_study("primary")
U = np.log(study.M)
C = np.cov(U.T, bias=True)
d = U.shape[1]
res = minimize(
    lambda w: w @ C @ w,
    np.ones(d) / d,
    jac=lambda w: 2 * C @ w,
    bounds=[(0, 1)] * d,
    constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
    method="SLSQP",
    options={"ftol": 1e-15, "maxiter": 1000},
)
w_mv = res.x
print(
    f"table: {U.shape[0]} designs, {d} metrics; "
    f"|mean of log-metrics| max {abs(U.mean(0)).max():.1e}"
)
print(f"minimum-variance fit: variance {w_mv @ C @ w_mv:.6f}, converged {res.success}")
print(f"{'tau':>6} {'largest gap':>12} {'agree to 3 places':>18}")
for tau in (0.01, 0.1, 1.0, 3.0):
    est = hts.HyperbolicTradeSpace(temperature=tau, random_state=study.spec.seed)
    w = est.fit(study.M).exponents_[0]
    gap = np.abs(w - w_mv).max()
    same = bool((np.round(w, 3) == np.round(w_mv, 3)).all())
    print(f"{tau:>6g} {gap:>12.4f} {same!s:>18}")
w3 = (
    hts.HyperbolicTradeSpace(temperature=3.0, random_state=study.spec.seed)
    .fit(study.M)
    .exponents_[0]
)
print()
print(f"{'metric':<26} {'tau = 3':>8} {'min variance':>13}")
for name, a, b in zip(study.names, w3, w_mv, strict=True):
    print(f"{name:<26} {a:>8.3f} {b:>13.3f}")

supports = {
    tau: int(
        (
            hts.HyperbolicTradeSpace(temperature=tau, random_state=0).fit(study.M).exponents_[0]
            > 1e-3
        ).sum()
    )
    for tau in (0.01, 0.1, 1.0, 3.0)
}
print()
print("metrics with an exponent above 1e-3, minimum variance:", int((w_mv > 1e-3).sum()), supports)
print(
    "exponents differing at three places at tau = 3:",
    int((np.round(w3, 3) != np.round(w_mv, 3)).sum()),
)
