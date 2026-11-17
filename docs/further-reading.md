# Further reading

The sources the method builds on, by what you may want from each.

The working paper (its abstract on the [project page](../); the full text builds from `paper/` in the repository; the lemma scripts under `derivation/`) carries the literature review, the formal results and the worked example.

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
- Kernel principal component analysis [@schoelkopf1998nonlinear]: the related method for the documented kernel direction, which is not
  built.
- HoroPCA [@chami2021horopca]: the nearest analog in setting; it fits a frame by a non-convex loss, this work a convex soft maximum over the simplex.
- Data envelopment analysis [@charnes1978measuring]: a frontier estimator from efficiency
  analysis, the nearest neighbour outside engineering design.
