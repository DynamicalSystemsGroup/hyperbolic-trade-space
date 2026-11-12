# hyperbolic-trade-space

For analysts with a table of evaluated designs, to learn which metrics trade: the
[docs](https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/docs/), the paper, `examples/adcs/` for a
case study.

```bash
git clone https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space
cd hyperbolic-trade-space && uv sync
# package only: uv sync --no-default-groups; uv run --no-default-groups
```

```python
from hyperbolic_trade_space import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    make_frontier_data,
    tension_report,
)

A, _ = make_frontier_data(300, 3, random_state=0)
A[:, 1] = 10 / A[:, 1]  # pretend column 1: smaller is better
M = LogAffinePreconditioner(orientation=[1, -1, 1]).fit_transform(A)
ts = HyperbolicTradeSpace(temperature=20.0).fit(M)  # real table: `select_temperature`
print(tension_report(ts, M).exponents.round(2))
```

## Layout

- `src/hyperbolic_trade_space/` — the package
- `docs/` — the docs site
- `paper/`, `site/` — the paper, the root page
- `scripts/`, `tests/` — build tools, tests
- `derivation/` — SymPy axioms and lemmas
- `examples/adcs/` — the ADCS case study
- `work-packages/` — scopes and decisions
