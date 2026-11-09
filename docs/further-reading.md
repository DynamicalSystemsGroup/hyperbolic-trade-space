# Further reading

The sources the method builds on, by what you may want from each. This is a short list and not a
survey.

**Using the package**

- scikit-learn and its API design [@pedregosa2011scikit; @buitinck2013api]: the conventions the
  estimators follow.
- Boyd and Vandenberghe, *Convex Optimization* [@boyd2004convex]: the notation used on these pages.

**Geometric programming and posynomials**

- A tutorial on geometric programming [@boyd2007tutorial]: posynomials and generalized posynomials,
  the family the multi-term fit stays inside.
- Fitting softmax-affine functions to data so they remain compatible with geometric programming
  [@hoburg2016data] is the source of the multi-term fit.
- Fitting convex piecewise-linear functions by alternating partition and refit [@magnani2009convex]:
  the second source of the multi-term fit.
- Reweighted $\ell_1$ minimization [@candes2008enhancing]: the sparsity option, `penalty="reweighted_l1"`.

**Charts and neighbouring methods**

- Isometric log-ratio transformations for compositional data [@egozcue2003isometric] and principal
  component analysis of compositional data [@aitchison1983principal]: the neighbours of the chart.
- Kernel PCA [@schoelkopf1998nonlinear]: the kin of the documented kernel direction, which is not
  built.
- HoroPCA [@chami2021horopca]: principal component analysis in hyperbolic space, which this package
  is not.
- Data envelopment analysis [@charnes1978measuring]: a frontier estimator from efficiency
  analysis, the nearest neighbour outside engineering design.
