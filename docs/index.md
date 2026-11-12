# hyperbolic-trade-space

For an analyst with a table of evaluated designs. The [paper](paper:sect-problem) makes the argument for the method; the [project page](../) links it, these docs and the package.

`hyperbolic_trade_space` learns the shape of a design trade space from evaluated designs. Give it a
table of designs, each scored on several metrics where larger is better, and it fits a frontier
model in the posynomial invariant form: a sum of monomial terms, where a monomial term (a product of
powers of the metrics) is one trade-off. It then tells you which metrics contend, with what
elasticity, where each design sits relative to the fitted reference surface, and where the table has gaps.

It is a scikit-learn estimator (`fit`, `transform`, `inverse_transform`, `score_samples`) in the
unsupervised and feature-engineering family, beside PCA: PCA finds where the data spread, this finds
where they stop, and the two chain.

- [Use it on my own table](getting-started.md): install and run a first fit.
- [Bring my own system model, and know what must hold](getting-started.md#your-own-data)
- [Place it beside PCA and scikit-learn](user-guide/overview.md)
- [Read the limits](user-guide/limitations.md)
- [See the worked case](examples.md): a cubesat trade study, a synthetic satellite demonstrator.

The user guide, API, theory, glossary and further reading are in the navigation menu.
