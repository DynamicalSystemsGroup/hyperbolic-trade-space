# hyperbolic-trade-space

For analysts with a table of evaluated designs, to learn which metrics trade: the
[docs](https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/docs/),
[the paper](https://dynamicalsystemsgroup.github.io/hyperbolic-trade-space/paper/), `examples/adcs/` for a
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

- `src/hyperbolic_trade_space/`: the Python package (fit a frontier, read its tensions).
- `docs/`: the user guide and API reference, built into the docs site; `docs/superpowers/` holds the notes the checks
  apply (conventions, notation, source lists).
- `paper/`: the paper as two notebooks and what rebuilds them; `site/` is the root page that links the docs and the paper.
- `examples/adcs/`: the cubesat attitude-control case study the paper uses: model, data, experiments, system model.
- `derivation/`: the proofs of the method's results as SymPy scripts, one per lemma.
- `tests/`: the test suite; `scripts/`: build and check tools.
- `claims_register.toml`: each claim the paper and docs make and what backs it.
- `glossary.yaml`: the terms, one name per object; `history.yaml`: the record behind the history and acknowledgements page.
- `CHANGELOG.md`: what changed, by work package.
- `work-packages/`: the build's record (scopes, reviews, decisions, round outputs, build notes, outlines and spike
  folders); not needed to use the method.
- `CLAUDE.md`: conventions for contributors working with Claude Code.
- `mkdocs.yml`, `Dockerfile`, `pyproject.toml`, `uv.lock`, `.python-version`: build and environment files;
  `LICENSE`; `.github/` (the CI workflows), `.gitattributes`, `.gitignore` and `.dockerignore`: repository settings.
