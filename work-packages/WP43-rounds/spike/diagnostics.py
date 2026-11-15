"""Post-hoc diagnostic (after the results were read; not a protocol measure): is the LQ surface
monotone?

For the whole-table LQ fit of each regime: the partial derivatives of ``f`` at the
rows, ``w + Q u``; the fraction of (row, metric) pairs with a negative partial and the size of
the most negative, against the largest exponent. Writes ``results/lq_monotone.md``.
"""

import pickle
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run  # noqa: E402

lines = [
    "| regime | fit | pairs with a negative partial | most negative partial "
    "| largest exponent w | rows with any negative partial below -0.01 |",
    "|---|---|---|---|---|---|",
]
for r, name in [(r, n) for r in run.REGIMES for n in ("LQ", "LQm")]:
    with open(run.CACHE / f"{r}_{name}.pkl", "rb") as fh:
        m = pickle.load(fh)
    U = np.log(run.load(r).M)
    g = m.w[None, :] + ((U @ m.B.T) @ m.S) @ m.B
    lines.append(
        f"| {r} | {name} | {(g < 0).mean():.3f} | {g.min():.3f} | {m.w.max():.3f} "
        f"| {(g < -0.01).any(axis=1).mean():.3f} |"
    )
(HERE / "results" / "lq_monotone.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
