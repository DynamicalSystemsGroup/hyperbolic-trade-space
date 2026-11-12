# hyperbolic-trade-space

Python package `hyperbolic_trade_space` (import alias `hts`); the method is the *posynomial invariant form*.
It learns which metrics of a design table trade. The
[docs](https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/docs/) say where to start.

```bash
git clone https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space
cd hyperbolic-trade-space && uv sync   # Python 3.12; run with `uv run`
```

```python
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    make_frontier_data,
    tension_report,
)

A, _ = make_frontier_data(300, 3, random_state=0)  # your table goes here
A[:, 1] = 10 / A[:, 1]  # pretend column 1: smaller is better
M = LogAffinePreconditioner(orientation=[1, -1, 1]).fit_transform(A)
ts = HyperbolicTradeSpace(temperature=20.0).fit(M)
print(tension_report(ts, M).exponents.round(2))
```

## Layout

- `src/hyperbolic_trade_space/` — the package
- `derivation/` — SymPy axiom and lemma scripts
- `examples/adcs/` — the ADCS trade-study case
- `docs/` — the docs site's pages
- `work-packages/` — scopes, reviews and decision records per work package, and the 0.1 state
