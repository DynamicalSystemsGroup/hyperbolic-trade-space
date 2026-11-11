# Choosing K

The fit never selects the number of terms K; you do. Every check below reads fits at one
temperature, selected at K = 1 ([Fitting](fitting.md#choosing-the-temperature)): `mean_slack_` is
comparable across K only there, and `objective_` not at all. No check decides K alone, so each is
given with what it cannot say.

## Methods

- **Mean slack against K.** Fit `n_terms` = 1, 2, ... and read the drop in `mean_slack_` per added
  term. A break, one large drop then small ones, marks a K worth keeping. The mean slack falls with
  every added term by construction, and a table may show no break.
- **Thinnest term.** `term_share_.min()` is the share of the near-frontier designs in the thinnest
  term's cell; a term of few designs is a few designs fitted alone. It says a term is thin, not
  which K is right, and it depends on the band.
- **Movement under resampling.** Refit on resamples of the rows and measure how far each term's
  exponent vector sits from the nearest term of the refit (summed absolute differences, at most 2).
  It is noisy: draws of one procedure differ by several tenths on the cubesat below, so it offers no
  threshold.
- **Planted check.** Fit `make_frontier_data(n_terms=K0)` at your number of designs and metrics to
  see how recovery looks on a table of your shape. It tests the method there, not your table's K.
- **The certificate.** `termination_.status` and `termination_.radius` say the optimizer finished
  and the assignments hold under small changes of the terms. Every fit below is certified at every
  K tried, so it does not say K is right.
- **`conditioning_`.** The smallest eigenvalue per term flags a nearly flat direction
  ([Termination](termination.md#conditioning_)). It compares metrics within a fit, not numbers of
  terms.

Two helpers carry the first three checks.

```python {.runnable}
import sys

import numpy as np
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    make_frontier_data,
)

sys.path.insert(0, "examples/adcs")
import case


def fit_k(M, K, tau, seed=0):
    return HyperbolicTradeSpace(
        n_terms=K, temperature=tau, random_state=seed
    ).fit(M)


def sweep(M, tau, Ks, planted=None):
    """One line per K at one temperature; returns the mean slacks."""
    slack = []
    for K in Ks:
        fit = fit_k(M, K, tau)
        t = fit.termination_
        assert t.status in ("certified", "not_applicable")
        line = (
            f"K={K} slack={fit.mean_slack_:.3f}"
            f" thinnest={fit.term_share_.min():.2f}"
            f" {t.status} radius={t.radius:.0e}"
        )
        if planted is not None:
            d = np.abs(fit.exponents_[:, None] - planted[None]).max(
                axis=2
            )
            line += (
                f" found={(d.min(axis=0) < 0.05).sum()}"
                f" unmatched={(d.min(axis=1) >= 0.05).sum()}"
            )
        print(line)
        slack.append(fit.mean_slack_)
    drops = -np.diff(slack)
    print("drops", drops.round(3))
    assert (drops > 0).all() and drops[-1] > 0.002
    return np.array(slack)


def movement(M, K, tau, draws=2, seed=0):
    """Largest distance to the nearest term of a refit on a resample."""
    ref = fit_k(M, K, tau)
    rng = np.random.default_rng(seed)
    moved = np.zeros(K)
    for s in range(draws):
        W = fit_k(M[rng.choice(len(M), len(M))], K, tau, s).exponents_
        d = np.abs(W[:, None] - ref.exponents_).sum(axis=2)
        moved = np.maximum(moved, d.min(axis=0))
    return moved.max()
```

## A planted table

The answer is known. `found` counts planted terms matched by a fitted term (largest exponent
difference under 0.05); `unmatched` counts fitted terms matching none.

```python {.runnable}
for K0, seed in ((2, 0), (3, 0), (3, 1)):
    X, info = make_frontier_data(400, 4, n_terms=K0, random_state=seed)
    print(f"planted K0 = {K0}, table {seed}")
    sweep(X, 50.0, range(1, 6), np.asarray(info["exponents"]))
```

With two planted terms the mean slack drops by 0.108 at K = 2 and by 0.005 or less after; both
terms are found at K = 2. With three, table 0 drops by 0.163 and 0.029, then 0.005 or less, and all
three are found at K = 3. Table 1 drops by 0.181, then 0.006 or less, and finds two of the three at
every K: the break reads the terms the fit recovers, not the number planted. Past the break the
mean slack keeps falling, by 0.003 or more at K = 5.

```python {.runnable}
X, _ = make_frontier_data(400, 4, n_terms=3, random_state=0)
for K in (3, 5):
    print(
        K, np.round([movement(X, K, 50.0, seed=s) for s in range(2)], 2)
    )
```

On table 0 the movement is 0.04 and 0.02 at K = 3, and 0.23 and 0.24 at K = 5.

## The cubesat

The two regimes of the [examples](../examples.md), each at its K = 1 temperature.

```python {.runnable}
studies = {r: case.load_study(r) for r in ("primary", "stock")}
taus = {r: case.fit_study(s, K=1).tau for r, s in studies.items()}
for r, s in studies.items():
    print(r)
    sweep(s.M, taus[r], range(1, 6))
```

The stock regime drops by 0.065 and 0.068, then 0.011 and 0.004: a break at K = 3, where the
thinnest term holds 0.17. The primary regime drops by 0.112, 0.044, 0.017 and 0.010: the curve
bends with no break, so the mean slack cannot choose K, and its thinnest term holds 0.07 already at
K = 2. Every fit is certified, with a stable radius from 3e-06 to 1e-04.

```python {.runnable}
for K in (2, 3, 4):
    M, tau = studies["primary"].M, taus["primary"]
    print(
        K, np.round([movement(M, K, tau, seed=s) for s in range(3)], 2)
    )
```

Over three draws the primary regime's movement is 0.09 to 0.45 at K = 2, 0.25 to 0.69 at K = 3 and
0.17 to 0.54 at K = 4. The ranges overlap, so this check excludes none.

## Large K and the elbow in PCA

The elbow heuristic for the number of principal components is the nearest kin of the first check,
and a break reads the same way. The limit differs: variance explained ends at d components, while
here K has no ceiling and the mean slack no floor. In every sweep above it is still falling at the
largest K tried, fitted terms matching no planted term appear beyond K0, and the thinnest term's
share reaches 0.00 on the two-term table at K = 5. A break is read together with the thinnest-term
and resampling checks, and a table can have none.
