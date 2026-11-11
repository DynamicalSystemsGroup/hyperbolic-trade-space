"""Noise injected into the cubesat attributes: what a measurement error does to the fit (WP29).

The data of record carry no noise of their own: they are deterministic simulator output, and the
rows of a repeated evaluation are identical. The noise here is injected as a design choice of this
experiment. Each raw attribute r_j is multiplied by exp(delta * z), z ~ N(0, 1) (a log-error of size
delta, to first order a relative error of size delta, the same for every attribute), the table is
conditioned again with the analyst's own steps (log, orient, standardise) and refitted at the clean
fit's temperature. What the table shows belongs to the fit-plus-conditioning pair: the scaler that
divides each log-attribute by its log spread s_j turns the error delta into the noise
sigma_j = delta / s_j in the conditioned metric (L18), and the fit reads that noise. It is not a
property of the model, and not a statement that the cubesat is noisy.

Columns, per regime and delta (mean over 8 repetitions, seeds 100 to 107): the largest change of
an exponent; the contending-set overlap (Jaccard index of the exponents above 1e-3, 1 = same set);
the shift of the fitted offset; the value L6 gives for that shift with the per-metric noise
sigma_j (L18, diagonal covariance); and with one sigma, the mean of the sigma_j (the equal-noise
reading of A5). Run from the repository root:

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


def regime_rows(regime):
    """(header lines, table rows) for one sampling regime."""
    study = case.load_study(regime)
    fit = case.fit_study(study)
    tau = fit.tau
    w0 = np.ravel(fit.estimator.exponents_)
    off0 = float(fit.estimator.log_offset_[0])
    s = log_spread(study)
    head = [
        f"regime {regime}: N = {study.M.shape[0]}, tau = {tau:.2f}",
        "log spread s_j: " + ", ".join(f"{a} {x:.3f}" for a, x in zip(study.attrs, s, strict=True)),
        "contending set of the clean fit: "
        + ", ".join(a for a, x in zip(study.attrs, w0, strict=True) if x > SUPPORT),
    ]
    rows = []
    for delta in DELTAS:
        sig = delta / s
        l6_diag = tau * float((w0**2) @ (sig**2)) / 2
        l6_iso = tau * float(sig.mean() ** 2 * (w0 @ w0)) / 2
        dw, jac, dsh = [], [], []
        for r in range(REPS):
            rng = np.random.default_rng(SEED0 + r)
            _, m_noisy = case._condition(inject(study, delta, rng), study.attrs, study.spec)
            e = HyperbolicTradeSpace(temperature=tau).fit(m_noisy)
            wn = np.ravel(e.exponents_)
            dw.append(np.abs(wn - w0).max())
            a0, a1 = set(np.flatnonzero(w0 > SUPPORT)), set(np.flatnonzero(wn > SUPPORT))
            jac.append(len(a0 & a1) / len(a0 | a1))
            dsh.append(float(e.log_offset_[0]) - off0)
        rows.append(
            f"| {100 * delta:.1f} | {sig.min():.3f} to {sig.max():.3f} | {np.mean(dw):.3f} | "
            f"{np.mean(jac):.2f} | {np.mean(dsh):.3f} | {l6_diag:.3f} | {l6_iso:.3f} |"
        )
    return head, rows


def main():
    print(__doc__.split("Columns")[0].strip())
    for regime in ("primary", "stock"):
        head, rows = regime_rows(regime)
        print("\n" + "\n".join(head) + "\n")
        print(
            "| delta (%) | sigma_j range | largest exponent change | contending-set Jaccard | "
            "offset shift | L6, sigma_j | L6, one sigma |"
        )
        print("|---|---|---|---|---|---|---|")
        print("\n".join(rows))


if __name__ == "__main__":
    main()
