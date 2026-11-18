# tradespace

[![PyPI](https://img.shields.io/pypi/v/tradespace)](https://pypi.org/project/tradespace/)
[![Python](https://img.shields.io/pypi/pyversions/tradespace)](https://pypi.org/project/tradespace/)
[![Tests](https://github.com/DynamicalSystemsGroup/tradespace/actions/workflows/test.yml/badge.svg?branch=dev)](https://github.com/DynamicalSystemsGroup/tradespace/actions/workflows/test.yml?query=branch%3Adev)

`tradespace` learns the shape of a design trade space from evaluated designs, with estimators that
work in scikit-learn pipelines. For analysts with a table of evaluated designs, or of observed cases
(reported devices, species, plot-years, finished projects), to learn which metrics trade.

[Getting started](https://dynamicalsystemsgroup.github.io/tradespace/docs/getting-started/) ·
[Examples](#examples) ·
[API reference](https://dynamicalsystemsgroup.github.io/tradespace/docs/api-reference/) ·
[Contribute](CONTRIBUTING.md#start-contributing) ·
[Report a bug](https://github.com/DynamicalSystemsGroup/tradespace/issues/new?template=bug.yml)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://dynamicalsystemsgroup.github.io/tradespace/ternary-planted-dark.png">
  <img alt="A triangle of three metrics tinted in three regions, with designs as points, a numbered marker at each term's exponent vector and lines of equal value closing around each marker; each region is labelled by the trade-off that leads there." src="https://dynamicalsystemsgroup.github.io/tradespace/ternary-planted-light.png">
</picture>

A constructed table of three metrics, fitted with three terms: each design sits by its shares of
the three metrics, one shaded region is where all three trade and the other two are where one
metric trades against another, and each numbered marker is a term's characteristic point.

- [Documentation](https://dynamicalsystemsgroup.github.io/tradespace/docs/): getting started, the
  user guide, the examples and the API reference.
- [Root page](https://dynamicalsystemsgroup.github.io/tradespace/): the method on one page, with
  the docs, the package and the working paper's abstract. The working paper's full text builds from
  the repository (`paper/`).

## Install

`tradespace` requires Python 3.12. Install it from PyPI:

```bash
pip install tradespace
```

In a [uv](https://docs.astral.sh/uv/) project, run `uv add tradespace`.
For development, install uv and [just](https://just.systems/man/en/packages.html), then run
`just setup` in your checkout. Run `just check` before submitting a change, or `just` to list commands.
See [Start contributing](CONTRIBUTING.md#start-contributing) for the checkout instructions.

## A first fit

A synthetic table: 300 designs scored on 3 metrics, all positive and larger-is-better, with a
planted frontier.

```python
from tradespace import (
    HyperbolicTradeSpace,
    make_frontier_data,
    trade_off_report,
)

X, info = make_frontier_data(300, 3, random_state=0)
ts = HyperbolicTradeSpace(temperature=20.0).fit(X)
report = trade_off_report(ts, X)
print(report.lemma_name, report.contending_set)
print(report.exponents.round(2))
```

```text
trilemma [0 1 2]
[0.3  0.37 0.33]
```

All three metrics contend at the edge of the table, a trilemma. The exponents are the fitted
weights at the fit temperature; their ratios are the elasticities between the contending metrics.
[Getting started](https://dynamicalsystemsgroup.github.io/tradespace/docs/getting-started/)
continues from this fit: the log-plane figure, the chart, and what must hold of your own table.

## Examples

Four public datasets, each fitted on its own page with its provenance and what the fit cannot
show: [perovskite solar cells](https://dynamicalsystemsgroup.github.io/tradespace/docs/examples/perovskite/),
[amniote life histories](https://dynamicalsystemsgroup.github.io/tradespace/docs/examples/amniote/),
[Broadbalk wheat](https://dynamicalsystemsgroup.github.io/tradespace/docs/examples/wheat/) and
[Kitchenham software projects](https://dynamicalsystemsgroup.github.io/tradespace/docs/examples/kitchenham/).
The [cubesat case study](https://dynamicalsystemsgroup.github.io/tradespace/docs/examples/) the
working paper uses, a synthetic satellite demonstrator with its SysML v2 system model, is in
`examples/adcs/`.

## Contributing

Report bugs, improve the docs or add a reproducible example. Follow the
[contributor quickstart](CONTRIBUTING.md#start-contributing) to set up a checkout and run checks.
Small fixes need no issue. Discuss new methods and public API changes in an issue before implementing them.

Code owners follow the [release rules](GOVERNANCE.md) and
[release instructions](https://dynamicalsystemsgroup.github.io/tradespace/docs/code-owners/).
All contributors must follow the [code of conduct](CODE_OF_CONDUCT.md).
Report vulnerabilities through the [security policy](SECURITY.md).

See [CHANGELOG.md](CHANGELOG.md) for release changes and [CITATION.cff](CITATION.cff) to cite the package.
The license is MIT.

## Layout

- `src/tradespace/`: the package.
- `docs/`: the documentation site's pages.
- `examples/`: the five examples' data, provenance and analysis code; `examples/adcs/` holds the
  cubesat system model.
- `paper/`: the working paper and what rebuilds it; `site/`: the root page.
- `derivation/`: the proofs of the method's results as SymPy scripts, one per lemma.
- `tests/` and `scripts/`: the test suite, the build and check tools.
- `work-packages/` and `notes/`: the build's record and working notes; not needed to use the package.
