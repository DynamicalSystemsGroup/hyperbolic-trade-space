# tradespace

For an analyst with a table of evaluated designs, or of observed cases: reported devices, species, plot-years, finished projects. The [project page](../) links these docs, the package and the working paper's abstract.

- [Use it on my own table](getting-started.md): install and run a first fit.
- [Bring my own system model, and know what must hold](getting-started.md#your-own-data)
- [Place it beside principal component analysis, or PCA, and scikit-learn](user-guide/overview.md)
- [Read the limits](user-guide/limitations.md)
- [See the worked case](examples.md): a cubesat trade study, a synthetic satellite demonstrator.
- [Pick a point on the chart and get a design](bridge.md): the route back and how to check it.

`tradespace` learns the shape of a design trade space from evaluated designs. Give it a
table of designs, each scored on several metrics where larger is better, and it fits a frontier
model in the posynomial invariant form: a sum of terms, where a term (a product of
powers of the metrics) is one trade-off. It then tells you which metrics contend, with what
elasticity, where each design sits relative to the fitted reference surface, and where the table has white space.

A first fit, on a synthetic table of 300 designs scored on 3 metrics:

```python {.runnable}
from tradespace import (
    HyperbolicTradeSpace,
    make_frontier_data,
    trade_off_report,
)
from tradespace.plotting import plot_log_plane

X, info = make_frontier_data(300, 3, random_state=0)
ts = HyperbolicTradeSpace(temperature=20.0).fit(X)
report = trade_off_report(ts, X)
print(report.lemma_name, report.contending_set)
print(report.exponents.round(2))
X2 = X[:, :2]
ts2 = HyperbolicTradeSpace(temperature=20.0).fit(X2)
plot_log_plane(ts2, X2, band=0.5)
```

<figure markdown>
![Designs in the log plane of two metrics: the frontier is a straight line, and the designs scatter below it, a few just beyond it, and the nearest ones lie in a grey band under the line.](generated/figures/first-fit-light.png#only-light)
![Designs in the log plane of two metrics: the frontier is a straight line, and the designs scatter below it, a few just beyond it, and the nearest ones lie in a grey band under the line.](generated/figures/first-fit-dark.png#only-dark)
<figcaption>The same fit on two of the metrics: the line is the fitted frontier, the designs fall below it or just beyond it, and the grey band holds those nearest to it.</figcaption>
</figure>

It is a scikit-learn estimator (`fit`, `transform`, `inverse_transform`, `score_samples`) in
unsupervised learning, beside PCA: PCA finds where the data spread, this finds where they stop, and
the two chain.

The argument and the proofs are the working paper's; its abstract is on the [project page](../), and the full text builds from the repository.
