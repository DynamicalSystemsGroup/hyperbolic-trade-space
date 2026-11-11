"""Noise injected into the cubesat attributes: the noise-ridge corollary against it (WP29).

The data of record carry no noise of their own: they are deterministic simulator output, and the
rows of a repeated evaluation are identical. The noise here is injected as a design choice of this
experiment. Each raw attribute r_j is multiplied by exp(delta * z), z ~ N(0, 1) (a log-error of size
delta, to first order a relative error of size delta, the same for every attribute), the table is
conditioned again with the analyst's own steps (log, orient, standardise) and refitted at the clean
fit's temperature. The scaler that divides each log-attribute by its log spread s_j turns the error
delta into the noise sigma_j = delta / s_j in the conditioned metric (L18). What the table shows
belongs to the fit and the conditioning together; it is not a property of the model, and not a
statement that the cubesat is noisy.

Columns, per regime and delta: ``conditioning_`` of the clean fit; the largest component of the
shift the corollary of Appendix B (L20) predicts on the active face, with Sigma = diag(sigma_j^2);
the largest component of the mean measured shift of the exponents over 8 repetitions (seeds 100 to
107); the largest spread of a component across the repetitions; the contending-set overlap
(Jaccard index of the exponents above 1e-3, 1 = same set). Run from the repository root:

    uv run python examples/adcs/noise_injection.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import case

from hyperbolic_trade_space import HyperbolicTradeSpace

REPS = 8
DELTAS = (0.005, 0.02, 0.05, 0.10)
SEED0 = 100
SUPPORT = 1e-3  # an exponent above this counts as contending


def log_spread(study):
    """s_j: the log standard deviation of each raw attribute on the feasible designs."""
    return np.array([np.log(study.feasible[a].to_numpy(float)).std() for a in study.attrs])


def inject(study, delta, rng):
    """The feasible table with every attribute multiplied by exp(delta z), z ~ N(0, 1)."""
    noisy = study.feasible.copy()
    for a in study.attrs:
        noisy[a] = noisy[a].to_numpy(float) * np.exp(delta * rng.standard_normal(len(noisy)))
    return noisy


def predicted_shift(M, w0, tau, sigma):
    """L20's first-order shift -(P C P)^+ P Sigma w on the active face, Sigma = diag(sigma^2)."""
    U = np.log(np.asarray(M, float))
    act = np.flatnonzero(w0 > SUPPORT)
    z = tau * (U @ w0)
    p = np.exp(z - z.max())
    p /= p.sum()
    mu = U.T @ p
    C = (U - mu).T @ ((U - mu) * p[:, None])
    k = len(act)
    P = np.eye(k) - np.ones((k, k)) / k
    shift = np.zeros(len(w0))
    shift[act] = -np.linalg.pinv(P @ C[np.ix_(act, act)] @ P) @ P @ (sigma[act] ** 2 * w0[act])
    return shift


def regime_rows(regime):
    """(header lines, table rows) for one sampling regime."""
    study = case.load_study(regime)
    fit = case.fit_study(study)
    tau = fit.tau
    w0 = np.ravel(fit.estimator.exponents_)
    cond = float(np.ravel(fit.estimator.conditioning_)[0])
    s = log_spread(study)
    head = [
        f"regime {regime}: N = {study.M.shape[0]}, tau = {tau:.2f}, conditioning_ = {cond:.3f}",
        "log spread s_j: " + ", ".join(f"{a} {x:.3f}" for a, x in zip(study.attrs, s, strict=True)),
        "contending set of the clean fit: "
        + ", ".join(a for a, x in zip(study.attrs, w0, strict=True) if x > SUPPORT),
    ]
    rows = []
    for delta in DELTAS:
        sig = delta / s
        pred = np.abs(predicted_shift(study.M, w0, tau, sig)).max()
        shifts, jac = [], []
        for r in range(REPS):
            rng = np.random.default_rng(SEED0 + r)
            _, m_noisy = case._condition(inject(study, delta, rng), study.attrs, study.spec)
            wn = np.ravel(HyperbolicTradeSpace(temperature=tau).fit(m_noisy).exponents_)
            shifts.append(wn - w0)
            a0, a1 = set(np.flatnonzero(w0 > SUPPORT)), set(np.flatnonzero(wn > SUPPORT))
            jac.append(len(a0 & a1) / len(a0 | a1))
        shifts = np.array(shifts)
        rows.append(
            [
                regime,
                f"{cond:.3f}",
                f"{100 * delta:.1f}",
                f"{pred:.3f}",
                f"{np.abs(shifts.mean(axis=0)).max():.3f}",
                f"{shifts.std(axis=0).max():.3f}",
                f"{np.mean(jac):.2f}",
            ]
        )
    return head, rows


COLUMNS = (
    "regime",
    "conditioning_",
    "delta (%)",
    "predicted largest shift",
    "measured largest shift (mean)",
    "spread of the draws",
    "contending-set Jaccard",
)


def main():
    print(__doc__.split("Columns")[0].strip())
    for regime in ("primary", "stock"):
        head, rows = regime_rows(regime)
        print("\n" + "\n".join(head) + "\n")
        print("| " + " | ".join(COLUMNS[2:]) + " |")
        print("|" + "---|" * (len(COLUMNS) - 2))
        print("\n".join("| " + " | ".join(r[2:]) + " |" for r in rows))


if __name__ == "__main__":
    main()
