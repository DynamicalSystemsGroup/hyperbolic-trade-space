# Theory in brief

This page states the model so the user guide reads without gaps. It gives definitions and no proofs.

## The invariant form

Let $m\in\mathbb{R}^d_{>0}$ be the metrics of a design, positive and larger-is-better, and $u=\log m$.
The model scores a design by a weighted geometric mean

$$
\begin{aligned}
V(m)&=\prod_{j=1}^{d} m_j^{\,w_j},\\
w_j&\ge 0,\quad \sum_j w_j=1 .
\end{aligned}
$$

Because the weights sum to one, $V(\lambda m)=\lambda V(m)$: doubling every metric doubles V. So V
reads as a factor of improvement, which is what "invariant" refers to. A sum of such products, a
posynomial, extends one term to K terms and keeps the programs inside geometric programming.

## V = 1 is the fitted reference surface

The fit chooses $w$ and an offset $\beta$ so that the data lie on or below the surface
$\log V=w\cdot u-\beta=0$, using the log-mean-exp (entropic) soft maximum of $w\cdot u$ over the
designs. With one term this is a convex program. Three objects answer to the word frontier, and the
text names them:

- the **fitted reference surface**, V = 1 at the working temperature tau; it is smooth, so a few
  designs lie beyond it;
- the **supporting envelope**, the same fit at tau = infinity: the exact maximum, a linear program,
  with no design above it;
- the **Pareto boundary**, the nondominated set of the attainable designs, a property of the system
  and not of the fit. The fit does not identify the other two with it.

Inside the surface V < 1; beyond it V > 1, and V - 1 says by how much. The logarithm, $\log V$, is the
energy differential (level offset) to the surface.

## The chart

Let $B$ be a basis of the sum-zero subspace of $\mathbb{R}^d$ (a Helmert log-ratio basis by default).
Each design has the coordinates

$$
\big(Z,\ \log V\big),\qquad Z=Bu\in\mathbb{R}^{d-1},
$$

where $Z$ is free of overall scale and says where along the surface the design sits, and $\log V$ says
how far from it. The map is reversible for every row with strictly positive metrics: nothing is lost
either way. Holes in the $Z$ plane are candidates for white space.

## Exchange rates and the n-lemma

On the surface $w\cdot u=\beta$, the level surface is flat in log space, so moving along it trades
the contending metrics at constant rates:

$$
\frac{\mathrm{d}\log m_j}{\mathrm{d}\log m_k}=-\frac{w_k}{w_j}.
$$

The metrics with positive weight at tau = infinity are the contending set, and its size n is the
n-lemma (a dilemma is n = 2, a trilemma n = 3). It is found from the data and not assumed: the fit at
tau = infinity is a linear program whose solution is generically sparse. At a finite working
temperature a small weight means weak participation, set by a participation threshold. With K
terms there is one contending set per facet, and exchange rates vary between facets.

## What the model assumes

Metrics are positive and larger-is-better (conditioning is yours to choose); the surface is log-convex;
at one term the exchange rates are constant; designs are chosen by an evaluator and not drawn from
the attainable set. The [limitations](user-guide/limitations.md) page says what each means when you
act on a result.

The argument itself lives in the project repository, in the derivation scripts under `derivation/`
and the README there, and the full account will be in the paper when it is published.
