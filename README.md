# tradespace

For analysts with a table of evaluated designs, or of observed cases (reported devices, species,
plot-years, finished projects), to learn which metrics trade. See the
[docs](https://dynamicalsystemsgroup.github.io/tradespace/docs/),
[the paper](https://dynamicalsystemsgroup.github.io/tradespace/paper/) and `examples/adcs/` for a
case study.

```bash
git clone https://github.com/DynamicalSystemsGroup/tradespace
cd tradespace && uv sync
# package only: uv sync --no-default-groups; uv run --no-default-groups
```

```python
from tradespace import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    make_frontier_data,
    trade_off_report,
)

A, _ = make_frontier_data(300, 3, random_state=0)
A[:, 1] = 10 / A[:, 1]  # pretend column 1: smaller is better
M = LogAffinePreconditioner(orientation=[1, -1, 1]).fit_transform(A)
ts = HyperbolicTradeSpace(temperature=20.0).fit(M)  # real table: `select_temperature`
print(trade_off_report(ts, M).exponents.round(2))
```

## Layout

- `src/tradespace/`: the Python package (fit a frontier, read its trade-offs).
- `docs/`: the user guide and API reference, built into the docs site.
- `paper/`: the paper as two notebooks and what rebuilds them; `site/` is the root page that links the docs and the paper.
- `examples/adcs/`: the cubesat attitude-control case study the paper uses: model, data, experiments, system model.
- `derivation/`: the proofs of the method's results as SymPy scripts, one per lemma.
- `tests/`: the test suite; `scripts/`: build and check tools.
- `claims_register.toml`: each claim the paper and docs make and what backs it.
- `glossary.yaml`: the terms, one name per object; `history.yaml`: the record behind the history and acknowledgements page.
- `CHANGELOG.md`: what changed, by work package.
- `work-packages/`: the build's record; not needed to use the method.
- `GOVERNANCE.md`: the release rules, the file that declares their settings (`.github/governance.toml`) and the check that runs first in CI.
- `CLAUDE.md`: conventions for contributors working with Claude Code.
- `mkdocs.yml`, `Dockerfile`, `pyproject.toml`, `uv.lock`, `.python-version`: build and environment files.
- `LICENSE`, `.github/` (CI workflows) and the dot-files `.gitattributes`, `.gitignore`, `.dockerignore`: license and repository settings.
