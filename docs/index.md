# hyperbolic-trade-space

`hyperbolic_trade_space` learns the shape of a design trade space from evaluated designs. Give it a
table of designs, each scored on several metrics where larger is better, and it fits a frontier
model in the posynomial invariant form. It then tells you which metrics contend, at what exchange
rate, where each design sits relative to the fitted reference surface, and where the table has gaps.

It is a scikit-learn estimator (`fit`, `transform`, `inverse_transform`, `score_samples`) in the
unsupervised and feature-engineering family, beside PCA: PCA finds where the data spread, this finds
where they stop, and the two chain.

## Where to start

- [Getting started](getting-started.md): install from source and run a first fit.
- [User guide](user-guide/overview.md): one page per task, from conditioning your attributes to
  reading what the fit reports.
- [API](api.md) and [API reference](api-reference.md): the public names and their docstrings.
- [Examples](examples.md): a spacecraft attitude-control trade study.
- [Theory in brief](theory.md): the model on one page.
- [Glossary](generated/glossary.md): the terms the package uses.
- [Further reading](further-reading.md): the sources the method builds on.

The [project page](../) links the paper, which is where the argument for the method is made, these
docs and the package.
