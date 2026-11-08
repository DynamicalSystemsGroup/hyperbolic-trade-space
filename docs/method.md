# Mathematics

This page sets out the mathematics of posynomial invariant form in the order of the pipeline. It is
discursive on purpose: each result is stated, said in words, tied to the lemma that proves it, and
tied to the hypotheses that lemma needs. The lemmas are plain-SymPy scripts in `derivation/`
(L1 to L10) and are machine-checked; machine verification shows that a formula follows from stated
hypotheses, and it is for a human to judge whether those hypotheses are reasonable for the problem
at hand. Throughout, formulas carry a tag comment naming the lemma that proves them, or marking
them as definitions, and the sections close with a small table pointing to the code that
implements them. Agreement of the code with the formulas is cross-checked in
`tests/test_matches_derivation.py`, which evaluates the lemmas' SymPy expressions at seeded numeric
instances and compares them with what the package returns. That check shows the code implements
the expressions; it does not re-prove them.

A word about stance. All models are wrong and some are useful. The theory below is here to ground
the method and to explain how to read its output, including where the reading stops being
justified. It does not have to match the implementation line for line, and it may carry hypotheses
that we cannot certify for the spaces we sample. Those hypotheses are listed together in
[Conditions of the theory](#conditions-of-the-theory), each with what it buys and what is lost
without it; they are the method's limitations, carried openly, not defects to be minimized. The
companion pages are [Why and how to use it](why-and-how.md) and
[Extensions and limitations](limitations.md).

## The pipeline and where the mathematics sits

Notation: $N$ designs, $d$ metrics, $M\in\mathbb{R}^{N\times d}_{>0}$, $U=\log M$ with rows $u_i$,
$\Delta$ the probability simplex, $P$ the law of $u$ induced by the stages before identification,
and $A=\operatorname{supp}P$ the admissibility set in log space. The vocabulary is fixed: a
configuration $c$ (design variables) is evaluated into attributes $a$ (evaluation outcomes), which
the analyst conditions into metrics $m$ (strictly positive, larger-is-better).

| Stage | Map | Contract | Owner |
|---|---|---|---|
| 0 Sampling | choose $c_i$ | mixed types, any scheme, may be sparse or biased | analyst |
| 1 Evaluation | $f:\mathcal C\times\Omega\to\mathcal A$ | attributes, mixed, noisy | blackbox |
| 2 Conditioning | $g:\mathcal A\to\mathcal M=\mathbb{R}^d_{>0}$ | positive, larger-is-better, comparable log-spread, chosen reference point; log-affine per metric and invertible on the metric block; other columns pass through as covariates | analyst, with scikit-learn tools |
| 3 Identification | finite subsets of $\mathcal M\to(w,\beta)$; chart $\Psi:\mathcal M\to(Z,\log V)$ | shape model, invertible chart, diagnostics | this package |
| 4 Analysis | level sets, holes in $Z$, novelty, pull-back through $g^{-1}$, interpretation against covariates, prediction from configuration | supervised composition $c\mapsto(Z,\log V)$ | this package and scikit-learn regressors |

The identification stage consumes a positive matrix and presumes nothing else. Pull-back to
attributes uses $g^{-1}$, which exists because conditioning is log-affine and invertible (A4, see
below). Association with configurations goes through the data, since $f$ is not invertible, or
through the supervised composition of stage 4. The package covers stages 3 and 4; conditioning is
the analyst's job, done with scikit-learn tools.

## Conditions of the theory

Every result below rests on some of the hypotheses of the ledger `derivation/axioms.py`. Most are
modelling choices we declare (the POSITED axioms A0 to A7) or textbook theorems we use and cite
(the INHERITED axioms I1 to I6); those are listed with their statements in the ledger and in the
lemma headers. The four conditions in the table are the ones that carry interpretive weight: the
regularity condition R1, the conditioning assumption A4, and the two fallback hypotheses F5 and
F10 that we introduced because a step resisted abstract simplification in SymPy. For R1, F5 and
F10 the role and failure mode are quoted verbatim from the ledger. The ledger records no role or
failure mode for A4 (it is a plain posited axiom), so the entries for A4 are written here and
marked as such.

| id | statement | interpretive role | failure mode |
|---|---|---|---|
| R1 | the balanced point lies in the relative interior of a facet of the frontier with positive normal | makes the KKT balanced point a genuine interior frontier point, so the gradient condition identifies w* as the facet normal and the improvement factors and elasticities can be read as trade-offs along the frontier | at a vertex, an edge or a facet with a zero normal component the gradient condition holds only as a subgradient inclusion: w* is not unique, some elasticities are undefined, and the frontier reading degrades to the weaker invariant-form reading |
| A4 | conditioning is log-affine and invertible: log m_j = alpha_j log(a_j + s_j) + b_j with alpha_j != 0 (negative alpha_j marks a cost attribute) | A4 is posited, so the ledger records none; stated here: it makes the pull-back to raw attributes an exact, invertible log-affine map (L9), so the fitted frontier can be read in the units of the attributes and negative exponents mark cost attributes | stated here: if conditioning is not log-affine and invertible (or is poorly chosen), the pulled-back formula no longer describes the attributes, the exponents $w$ describe the conditioned metrics only, and a different conditioning answers a different question |
| F5 | max representation for L5: the maximum of the scores is a symbol M with s_i <= M for all i in 1..n and s_{i0} = M for some i0 in 1..n | lets the tau -> infinity limit and the bound LME <= max be proved for symbolic n (sympy has no symbolic-n max and cannot take limits through the symbolic Sum): M - (log n)/tau <= LME <= M is squeezed with sympy.limit | the statement is about the actual maximum only when M really is max_i s_i; if M is any upper bound that is not attained the lower squeeze bound is lost and the limit is only an upper bound on the true limit |
| F10 | max representation for L10: the maximum over the K terms of x_k = theta_k.u - beta_k is a symbol M with x_k <= M for all k in 1..K and x_{k0} = M for some k0 in 1..K | lets lim_{kappa->inf} Phi_K = max_k x_k and the bound Phi_K <= max be proved for symbolic K (same squeeze as F5), so the extension reads as a soft maximum of K affine log-scores | as F5: if M is not attained by some term the lower squeeze bound M - (log K)/kappa is lost and only an upper bound on the limit is available |

The chart axiom A7 is also worth reading in the ledger's own words. Its role: "makes Z the
scale-free coordinates of the metric vector: Z is blind to a common multiplicative scale (a shift
of u along 1), and with the log-scale it gives an isometric linear bijection, so Gaussian noise and
distances can be read in Z". Its failure mode: "if B 1 != 0 the chart sees the overall scale and Z
is not invariant; if B B^T != I the chart is not isometric, so noise in u is not isotropic in Z and
distances in Z distort those in u". The Helmert basis used by the code is one realization of A7.

How to read the table. R1 is the condition that most often fails in practice and the one that
changes the interpretation most: when the balanced point is not in the relative interior of a facet
with positive normal, the fitted exponents are a subgradient choice, not an identified trade-off.
F5 and F10 concern only the proofs of the temperature limits: they say the symbol $M$ is the actual
maximum, so they hold by construction for the quantity they name and cost the reader nothing in
practice; we list them because the ledger lists every hypothesis a proof used. A4 is the condition
analysts control: the interpretation of $w$ is an interpretation of the conditioned metrics, and
different conditioning gives a different, equally legitimate, question.

## The model

The frontier is the unit level set of a weighted geometric mean of the metrics. With exponents
$w\in\Delta$ (A2) and $u=\log m$ (A1),

$$
V(m)=\prod_{j=1}^{d} m_j^{w_j}=\exp\!\Big(\sum_{j=1}^{d} w_j u_j\Big).
$$
<!-- lemma: L1 -->

By L1 this form is homogeneous of degree one, because the exponents sum to one:

$$
V(k\,m)=k\,V(m)\quad(k>0),\qquad V\!\Big(\frac{m}{V(m)}\Big)=1 .
$$
<!-- lemma: L1 -->

The second identity is the invariant form: dividing a design by its own score places it exactly on
the surface $V=1$. With an offset $\beta$ fitted from the data (next section), the scored quantity
is

$$
\log V=w\cdot u-\beta,\qquad \tilde m=m\,e^{-\beta},\qquad V(\tilde m)=e^{-\beta}V(m),
$$
<!-- lemma: L1 -->

so the frontier $F=\{w\cdot u=\beta\}$ is a hyperplane in log space and the level sets of $V$ are
parallel hyperplanes; in metric space the frontier is a generalized hyperbolic surface
$\prod_j m_j^{w_j}=e^{\beta}$. Needs: A1 (so the logarithm exists) and A2 (so the degree is one,
not $\sum_j w_j$). L1 says nothing about how $w$ or $\beta$ are fitted.

The adjective hyperbolic refers to this shape and nothing else: $V\to0$ as any metric $m_j$ with
$w_j>0$ tends to zero, so no metric that participates can be sacrificed entirely. It is not
negative-curvature geometry; see [Extensions and limitations](limitations.md) for the
disambiguation from hyperbolic PCA [@chami2021horopca]. A metric with $w_j=0$ does not enter $V$.

| Formula | Implementation | Cross-check |
|---|---|---|
| $V=\exp(w\cdot u-\beta)$, $V(km)=kV(m)$ | `HyperbolicTradeSpace.invariant_value` | `test_matches_derivation.py` (L1 group), L1 `verify` |
| $m/V$ | `HyperbolicTradeSpace.project` | L1 `verify`; estimator tests |

## The fit

The fit asks for the positive combination of log-metrics along which the data have the smallest
upper extent, using a smooth (entropic) soft maximum. Let $s_i=w\cdot u_i$ and let $\tau>0$ be the
temperature (A3). The objective is the log-mean-exp of the scores,

$$
J_\tau(w)=\frac1\tau\log\Big(\frac1N\sum_{i=1}^{N}\exp(\tau\,w\cdot u_i)\Big),\qquad
w^*=\arg\min_{w\in\Delta}J_\tau(w),\qquad \beta=J_\tau(w^*).
$$
<!-- definition -->

The normalization $1/N$ matters. By L5, the unnormalized log-sum-exp equals the log-mean-exp plus
$(\log N)/\tau$,

$$
\mathrm{LSE}_\tau(s)=\mathrm{LME}_\tau(s)+\frac{\log N}{\tau},\qquad
\mathrm{mean}(s)\le\mathrm{LME}_\tau(s)\le\max_i s_i\le\mathrm{LSE}_\tau(s).
$$
<!-- lemma: L5 -->

L5 proves the exact identity $\mathrm{LSE}_\tau=\mathrm{LME}_\tau+(\log N)/\tau$, so the
log-sum-exp is at least the maximum and exceeds the log-mean-exp by an offset that grows with the
sample size $N$; it proves no more about the size of the excess over the maximum itself (that excess
is only bounded above by $(\log N)/\tau$). Our reading, not a lemma, is that an unnormalized sum
would therefore tie $\beta$ to the number of designs sampled and would not let a point exceed
$V=1$ in the intended way, whereas the log-mean-exp stays between the mean and the maximum, so
$\beta$ is a property of the data's shape. This is why $\beta$ is always the log-mean-exp and never the unnormalized sum. Needs: A3,
and the F5 symbol for the maximum in the squeeze (F5 holds when $M$ really is $\max_i s_i$).

The temperature has two limits, also by L5 (under F5 for the second):

$$
\lim_{\tau\to0}\mathrm{LME}_\tau(s)=\mathrm{mean}(s),\qquad
\lim_{\tau\to\infty}\mathrm{LME}_\tau(s)=\max_i s_i,\qquad
\max_i s_i-\frac{\log N}{\tau}\le\mathrm{LME}_\tau(s)\le\max_i s_i .
$$
<!-- lemma: L5 -->

As $\tau\to0$ the soft maximum tends to the mean and the softmax weights tend to uniform (the mean by L5; the weights by their definition in L3). Our
reading, not proved here, is that the fit then moves toward a vertex of the simplex (the metric with the
smallest mean), by the limit of the minimization; as $\tau\to\infty$ it becomes the worst-case linear program. In units of inverse log-spread, a
working range after conditioning is roughly 3 to 100, default 10. Uniform scaling of all metrics
by $k$ shifts the data by $c=\log k$ along the diagonal, and by L2

$$
J_\tau(w;U+c\mathbf 1^{\top})=J_\tau(w;U)+c ,
$$
<!-- lemma: L2 -->

so $\beta$ moves by $c$ and $w^*$ is unchanged. Needs: A2, A3. L2 is silent about per-metric
rescaling, which changes the facet (the documented lever of stage 2).

**Gradient and balance.** For any direction $v$, differentiating through the sum gives

$$
\nabla J_\tau(w)=\sum_{i=1}^{N}p_i\,u_i=U^{\top}p,\qquad
p_i=\frac{\exp(\tau\,w\cdot u_i)}{\sum_{l}\exp(\tau\,w\cdot u_l)},
$$
<!-- lemma: L3 -->

so the gradient is the envelope-weighted centroid of the data, the weights $p$ concentrating on the
designs nearest the envelope (the support weights). If the minimizer is an interior point of the
simplex, the Lagrange condition says all components of $U^\top p$ are equal (balance):

$$
(U^{\top}p)_{1}=(U^{\top}p)_{2}=\cdots=(U^{\top}p)_{d}=\lambda .
$$
<!-- lemma: L3 -->

Needs: A2, A3, and R1 for the premise. L3 takes stationarity of the Lagrangian at an interior
point as its hypothesis; it does not prove that the minimizer is interior, nor that it exists or is
unique, nor anything about the sign of $\lambda$. When R1 fails the balance equation holds only as
a subgradient inclusion with active nonnegativity constraints (see the table).

**Convexity.** The fit is a convex program because, along any line,

$$
\frac{d^2}{dt^2}J_\tau(w+tv)\Big|_{t=0}=\tau\,\mathrm{Var}_p(v\cdot u)
=\frac\tau2\sum_{i,k}p_ip_k\,(s_i-s_k)^2\ \ge 0 ,
$$
<!-- lemma: L4 -->

where $s_i=v\cdot u_i$. Each term is a positive weight times a square, so the sum is nonnegative.
Needs: A1 (so $w\cdot u_i$ and $v\cdot u_i$ are real) and A3. L4 proves convexity of the objective,
not strict convexity: uniqueness of the minimizer on the simplex would need $\mathrm{Var}_p>0$ on
the tangent space, a rank condition on the differences $u_i-u_k$ that is not proved. The code
reports the effective sample size $n_\mathrm{eff}=1/\sum_ip_i^2$ so the analyst can see how many
designs carry the fit.

| Formula | Implementation | Cross-check |
|---|---|---|
| $\mathrm{LME}_\tau(s)$, $\tau=\infty\Rightarrow\max$ | `solvers.log_mean_exp` | `test_matches_derivation.py` (L5 group), L5 `verify` |
| $p=\mathrm{softmax}(\tau Uw)$ | `solvers.support_weights` | L3 `verify` |
| $J_\tau$ and $\nabla J_\tau=U^\top p$ | `solvers.objective_and_grad` | `test_matches_derivation.py` (L3 group) |
| $\tau=\infty$ fit (linear program) | `solvers.solve_lp` | LP duality, I1 (checked numerically in the solver tests) |
| finite-$\tau$ fit | `solvers.solve_slsqp` | gradient and KKT cross-check (L3) |
| shift by $c$ | `HyperbolicTradeSpace.fit` | `test_matches_derivation.py` (L2 group) |

## What the stage learns, and why it is shape

Eight statements say what the fitted $(w,\beta)$ is, in terms of the admissibility set $A$ and not
of the density of the samples. Each names the lemma behind it and the hypotheses it rests on.

**1. A softened support function.** The population counterpart of $J_\tau$ is the entropic risk
functional

$$
\rho_\tau(w)=\frac1\tau\log\mathbb{E}_P\exp(\tau\,w\cdot u),
$$
<!-- definition -->

nondecreasing in $\tau$ (a standard property of the entropic risk functional, not a lemma here),
tending to $\mathbb{E}[w\cdot u]$ as $\tau\to0$ and increasing to the support function
$h_A(w)=\operatorname{ess\,sup}\,w\cdot u$ as $\tau\to\infty$ (L5 proves the sample versions of the
two limits; the passage to the population quantities is recorded there as a remark resting on I2
and I3). A closed convex set is determined by its support function (I3, a
theorem of convex analysis [@rockafellar1970convex]), so the full support function (all directions) determines
the log-convex hull of the admissibility set. That a softened support function over positive directions
conveys that hull when read at finitely many directions is our reading, not I3; the method reads it at one direction ($K=1$). Convexity of $\rho_\tau$ in $w$ is
L4 for the sample version. This is the entropic risk measure read from the mean to the worst case
[@foellmer2026entropic], applied to $-w\cdot u$; it is not the entropic value-at-risk
[@ahmadijavid2012entropic]. The method reads one direction ($K=1$) of that support function. Needs:
A3, I3 (a cited theorem, not proved here), F5 for the limits.

**2. Linear-programming duality at $\tau=\infty$.** There the fit is

$$
\min_{w\in\Delta}\max_i w\cdot u_i=\max_{\lambda\in\Delta_N}\min_j (U^{\top}\lambda)_j .
$$
<!-- definition -->

This is the strong duality of linear programs (I1 [@boyd2004convex]), taken as inherited and
checked numerically against the solvers; it is not one of the SymPy lemmas. Read geometrically, the
fit is the supporting hyperplane of the convex hull of $A$ at its most balanced point: on the
diagonal ray when every $w_j>0$, where all conditioned metrics are equally good relative to the
stage-2 reference. The vector $w^*$ is the local normal there, and its entries are elasticities;
moving the reference (a stage-2 choice) traces other facets. This reading needs R1 (balanced point
in the relative interior of a facet with positive normal) and is the one that degrades first when
R1 fails.

**3. Shape, not density.** At $\tau=\infty$ the result depends on $P$ only through $A$. At finite
$\tau$ the weight $p_i\propto e^{\tau w\cdot u_i}$ of a design at depth $\delta$ below the envelope
carries a factor $e^{-\tau\delta}$ (L3's softmax weights), so interior density matters only in a
boundary layer of depth about $1/\tau$. Needs: A3. The depth statement is a reading of the L3
weights, not a separate lemma.

**4. Noise.** If $u=u^{\rm true}+\varepsilon$ with independent $\varepsilon$, the objective gains
$\frac1\tau\log\mathbb{E}\exp(\tau\,w\cdot\varepsilon)$. For i.i.d. Gaussian noise (A5) this is,
by L6 (using I5 for the product of moment generating functions),

$$
\frac1\tau\log\mathbb{E}\exp(\tau\,w\cdot\varepsilon)=\frac{\tau\sigma^2\|w\|^2}{2}.
$$
<!-- lemma: L6 -->

L6 proves the cumulant $\tau\sigma^2\|w\|^2/2$. Reading it as a known offset in $\beta$ plus a
mild ridge toward balanced exponents (the term is smallest when $w$ is uniform) is the project's
interpretation of that added convex term, not part of L6. Needs: A2, A5, I5. L6 says nothing about
non-Gaussian or dependent noise.

**5. Consistency and the normalization.** The sample functional converges to $\rho_\tau$ by the
strong law of large numbers (I2, recorded in the L5 docstring; checked in the tests by replication,
which leaves the sample functional unchanged). Under I2, and given the convexity of the sample
functional in $w$ (L4, which is not strict), we expect $\hat w$ and $\hat\beta$ to converge to the
minimizer and the offset of $\rho_\tau$; this is an expectation, not a proved result. L5 disclaims
consistency, and neither pointwise-to-uniform convergence on $\Delta$ nor convergence of the
minimizers is proved in the lemmas. The $1/N$ normalization of L5 (see the fit) is what makes $\beta$ a limit at all.

**6. Invariances.** Uniform scaling shifts $\beta$ by $\log k$ and leaves $w$ and $V$ unchanged
(L2, L1). Permuting the metrics permutes $w$ (a symmetry of the objective, covered by the tests, not
a lemma). Rescaling a single metric changes which facet is tangent; this is the documented lever
of stage 2 and is outside L2. L8 gives the bijection between $u$ and $(Z,\text{log-scale})$; the passage to
$(Z,\log V)$ is an invertible affine change of coordinates that uses A2 and the fitted $w$ (our step, not part of L8), with $Z$
independent of $w$ (see the chart below).

**7. Identifiability.** $w^*$ is unique when the balanced point lies in the relative interior of a
facet with positive normal (R1); the lemmas use R1 as a hypothesis and do not prove it. At finite
$\tau$, uniqueness would follow from positive definiteness of $\mathrm{Cov}_p(u)$ on the tangent
space, which L4 does not prove (it gives only the nonnegativity). With small samples the fit may be
weakly determined; the code reports $n_\mathrm{eff}$ and the fraction of points above the surface.

**8. Hyperbolic reading.** $V\to0$ as any participating metric tends to zero, from the product form
(L1, definition of $V$). Needs: A1 and $w_j>0$ for the metric in question.

## Tensions, not variance

The construction is easiest to place by contrast with principal component analysis. PCA finds the
directions of greatest spread: where the data are free. The fit does the opposite kind of thing.
It minimizes the soft maximum of $w\cdot u$ over the simplex, which picks the positive combination
along which the data have the smallest upper extent: the binding constraint among larger-is-better
metrics. The normal $w$ is the tension that defines the frontier. Metrics with $w_j>0$
participate (the contending set at $\tau=\infty$; at finite $\tau$ participation is graded), and their ratios $w_k/w_j$ are the exchange rates (the elasticities of L7, see
Interpretation). A metric with $w_j=0$ is free at the balanced point: the frontier places no
constraint on it there.

Spread is not discarded; it moves to the chart. Along the frontier, the spread of near-frontier
designs in $Z$ occurs only in directions where metrics were actually traded. Its principal
directions, the principal components of near-frontier $Z$, are the exercised trade-offs, and a pair
of metrics whose log-values move together there is aligned, not in tension. The analysis toolkit
(its API is documented in `api.md`) reports, by concept, which metrics participate and with what
exponents, pairwise tension versus alignment among near-frontier designs, and principal tension
directions in $Z$ with their loadings. The fit itself does not say that every pair of
participating metrics is in tension; that is what the near-frontier analysis in $Z$ adds.

This PCA contrast has limits, stated plainly. $K=1$ finds one tension, at the balanced point. A
trade space with several regional tensions is what the $K>1$ extension is for. A deflation-style
search for successive tensions, in the way PCA extracts successive components, is a research
question and is not claimed here. The word hyperbolic is used for the shape of $V$, not for
curved geometry, and is unrelated to PCA in negative-curvature geometry [@chami2021horopca].
The method is kin to log-ratio PCA [@aitchison1983principal; @aitchison1986statistical]: like PCA
it identifies a direction and coordinates from data, but its criterion is a one-sided soft maximum
and its $w$ lives on the simplex, a positive index with elasticities, not a contrast.

### n-lemmas are discovered, not assumed

Engineering practice names dilemmas and trilemmas freely, but such names are more often heuristics
than findings. We use the term n-lemma once, with this meaning: an n-lemma is a facet of the
admissibility set whose normal has exactly $n$ positive exponents, so that $n$ metrics contend on
it; dilemma and trilemma are the cases $n=2$ and $n=3$. The fit discovers the contending set as
the support of $w$, with no prior choice of which metrics contend or how many, and $d$ is
arbitrary. It also parameterizes the contention, by the exponents, which are the exchange rates.

The reading depends on temperature. At $\tau=\infty$ the linear program is sparse and zero
exponents are exact; at a working finite $\tau$ the solution is smooth, and small exponents mean
weak participation, not absence. The `min_exponent` parameter of the estimator imposes a floor on
the exponents and therefore masks sparsity: it must be $0$ for the n-lemma reading. With $K=1$ the
fit reveals the contention at the balanced point only; a trade space with several regional
n-lemmas, one contending set per facet, is what the $K>1$ extension is for. The documentation never
asserts that a particular case has a trilemma; it reports what the fit says contends and then asks
whether the result is explicable. Needs: R1 (the balanced point on a facet with positive normal;
at a vertex or an edge the contending set is ambiguous) and A4 (the contenders are conditioned
metrics).

## Interpretation

Given the fit, five tools read it back in engineering terms.

**Elasticities and improvement factors.** Along the frontier $F$ the local trade-off between two
metrics is, by L7,

$$
\frac{\partial\log m_j}{\partial\log m_k}\bigg|_{F}=-\frac{w_k}{w_j}\quad(j\ne k),
$$
<!-- lemma: L7 -->

and the factor by which the single metric $j$ alone must improve to reach the frontier is

$$
f_j=V^{-1/w_j},\qquad\text{uniform improvement: scale every metric by }V^{-1}.
$$
<!-- lemma: L7 -->

Both hold with $w_j\neq0$; R1 supplies $w_j>0$ at the balanced point. They are shape quantities,
not preferences: the elasticity says how metrics trade on the surface, not how they should be
traded. L7 proves them for $F$ itself, the hyperplane $\{w\cdot u=\beta\}$ in log space, where $w_j\ne0$ (for the improvement factor, with $V$ the score against that hyperplane); it does not say that the elasticities are those of the
balanced point; that identification needs the fit (L3) and R1. The projection of a design onto
the frontier along the diagonal is $m/V$ (L1).

**The chart.** Coordinates are the log-ratio chart together with the distance to the frontier:

$$
Z=B\,u\ \ (\text{rows } Z_i = u_iB^{\top}),\qquad u=B^{\top}Z+\frac{\mathbf 1^{\top}u}{d}\,\mathbf 1,
\qquad Z(u+c\mathbf 1)=Z(u),
$$
<!-- lemma: L8 -->

with $B$ a $(d-1)\times d$ matrix satisfying $BB^{\top}=I$ and $B\mathbf 1=0$ (A7), and the
orthogonal completion $Q=[B;\ \mathbf 1^{\top}/\sqrt d]$ satisfying $QQ^{\top}=Q^{\top}Q=I$ (I6).
L8 proves that $u\leftrightarrow(Z,\text{log-scale})$ is a bijection. Because $\log V=w\cdot u-\beta$
and $w$ sums to one (A2), $w\cdot u=\mathbf 1^\top u/d+w\cdot B^\top Z$ is affine in
$(Z,\text{log-scale})$ with a nonzero coefficient on the log-scale, so the pair $(Z,\log V)$ is an
invertible affine change of coordinates on log space (this last step is ours, using A2 and the
fitted $w$, not part of L8); $Z$ is the
position along the frontier and $\log V$ the distance from it. The Helmert basis is one realization
of A7 and the code also offers additive log-ratio coordinates; L8 holds for any $B$ satisfying A7,
not specifically for Helmert. It does not prove that such a $B$ exists for every $d$ (the Helmert
basis is checked concretely as a realization). The chart is in the spirit of isometric log-ratio
coordinates [@egozcue2003isometric] (our reading). Needs: A7, I6, and A2 (the simplex, for the step to $\log V$).

**Pull-back to attributes.** If conditioning is log-affine per metric, $\log m_j=\alpha_j\log(a_j+s_j)+b_j$
with $\alpha_j\ne0$ (A4), then by L9

$$
V=e^{\,w\cdot b-\beta}\prod_{j=1}^{d}(a_j+s_j)^{w_j\alpha_j},
$$
<!-- lemma: L9 -->

so the frontier can be read in the raw attributes' units, with negative exponents $w_j\alpha_j$
marking cost attributes. The conditioning is invertible, so the pull-back is a bijection. L9 does
not say that a given conditioning is appropriate: A4 is posited, and if conditioning is not
log-affine and invertible the pulled-back reading loses its meaning (see the table).

**Reading design variables.** Covariates (configuration variables the analyst passed through) are
related to the chart by colouring, by mean $V$ and near-frontier share per category, by the
correlation of $\log V$ with continuous variables and by per-category refits. These are
descriptive uses of the fitted coordinates; the estimator fits no surrogate.

| Formula | Implementation | Cross-check |
|---|---|---|
| $-w_k/w_j$ | `HyperbolicTradeSpace.exponents_` (read as elasticities) | `test_matches_derivation.py` (L7 group) |
| $V^{-1/w_j}$ | `HyperbolicTradeSpace.improvement_factors` | L7 `verify`; estimator tests |
| $B$, $Z=Bu$, round trip | `coordinates.helmert_basis`, `coordinates.alr_basis` | `test_matches_derivation.py` (L8 group) |
| $(Z,\log V)$ and back | `coordinates.to_frontier_coordinates`, `coordinates.from_frontier_coordinates`, `HyperbolicTradeSpace.transform`, `HyperbolicTradeSpace.inverse_transform` | `test_matches_derivation.py` (L8 group) |
| pull-back $V(a)$ | the analysis toolkit (preconditioning; API in `api.md`) | L9 `verify` |

## Novelty and white space

Scoring a measured or hypothetical attribute vector evaluates the learned chart after the fitted
preconditioner. The score $V-1$ is the uniform factor by which a frontier design must improve to
reach the scored design: by L1, a design $m$ with $V(m)=v$ is obtained from a frontier design by
scaling all metrics by $v$, so $V-1$ is the relative improvement. It is implemented as
`HyperbolicTradeSpace.novelty_score`, with a calibrated variant described below. Stochastic
frontier analysis [@aigner1977formulation] treats the same geometry as a regression with one-sided
error; that parallel is our reading, not a result of those sources. The nearest prior art for
scoring a design against the frontier of the others is DEA super-efficiency
[@andersen1993procedure]; the Malmquist index decomposes a displacement into a frontier shift and
an efficiency change [@fare1994productivity]. What differs here, as a matter of form, is that the
frontier is a smooth parametric surface, so the factor $V-1$, the elasticities and the projections
are available in closed form; whether that matters in practice is not established by any source we
cite.

Four caveats are part of the method.

1. **Noise band.** At finite $\tau$ some training designs exceed $V=1$ by construction (the
   fraction above is reported). The calibrated novelty therefore reports the rank of $\log V$
   among training scores and $\tau\log V$ next to $V-1$: a design is novel only relative to the
   band of order $1/\tau$.
2. **Optimism off the balanced point.** Far from the diagonal a design has $V\ll1$ even when it
   is locally on the frontier, because a single hyperplane is tangent only at one place. our
   reading (spec section 4, no lemma behind it) is that $V-1$ is reliable near the balanced
   region and conservative elsewhere; points whose $Z$ lies outside the
   training hull of $Z$ are flagged. The $K>1$ extension is expected to tighten this (a conjecture). This caveat is the failure
   mode of R1 and of the one-facet model, stated again.
3. **Holes versus strata.** Holes are regions of $Z$ with no near-frontier points ($|\log V|$
   below a band), scored by nearest-neighbour or grid distance inside the hull. A hole is an
   attainable opportunity only if the trade space is log-convex there; structural gaps (categorical
   strata) are not opportunities. Human validation decides. The fit is a log-convex envelope; no
   $K$ represents non-log-convex structure.
4. **Novelty is not preference.** $V-1$ says how far beyond the learned surface a design lies,
   not whether anyone wants it.

## Prediction from configuration

Given a proposed configuration with no measured attributes, where it would fall is a supervised
question: regress the chart coordinates on the configuration variables over the designs that have
both, then read the predicted $\log V$ (distance to or beyond the frontier), the predicted $V-1$
(expected novelty) and the predicted $Z$ (where along the frontier). The prediction inherits the
surrogate's error and extrapolation risk and is conditional on the fitted trade space. It belongs
to the composition of a regressor with the chart, not to the unsupervised estimator, which has no
predict method; it is implemented in the analysis toolkit, with the regressor chosen by the analyst.
The chart is exactly invertible (L8 with A2 and A7), which is why a prediction in $(Z,\log V)$ maps back to
metrics through the estimator's inverse transform.

## Lineage

We stand on well-known ground and claim nothing about priority. The weighted geometric mean with
exponents summing to one is the constant-returns Cobb-Douglas form [@cobb1928theory]; reading $V$
as the factor by which a bundle must be scaled to reach the boundary is a distance-function
reading [@shephard1970theory; @fare1995multi], and efficiency measurement in this tradition goes
back to [@farrell1957measurement]. Deterministic frontiers estimated by mathematical programming
are credited to [@aigner1968estimating] (on a secondary record); the statistical version to
[@afriat1972efficiency], extended by [@richmond1974estimating] and [@greene1980maximum]; corrected
OLS, defined in the survey [@battese1992frontier] (an OLS fit with the intercept raised by the
largest residual), is a distinct estimator from ours, which uses a smooth soft maximum over a
simplex-constrained geometric mean. Stochastic frontiers are [@aigner1977formulation]. Data
envelopment analysis [@charnes1978measuring] is a linear-programming measure of the relative
efficiency of decision-making units. The hierarchy $K=1$ tangent, $K$-facet soft maximum, hull of
the data (in log space, the data's log-convex hull) is the project's own framing from the
design spec, not a statement taken from the DEA literature. The entropic risk functional is the source of
$\rho_\tau$ [@foellmer2026entropic], and log-ratio PCA of compositional data
[@aitchison1983principal; @aitchison1986statistical] is the kin in feature engineering, with
isometric log-ratio coordinates in [@egozcue2003isometric]. Combining these pieces in one
estimator is our design; the sources establish the pieces, not the combination. The full review,
with the verification status of each source, is in `literature.md`.

## The posynomial and GGP extension

The model above is the one-term case. The extension replaces the single monomial by a generalized
posynomial,

$$
V_K(m)=\Big(\sum_{k=1}^{K}c_k\prod_{j=1}^{d}m_j^{\kappa\,\theta_{kj}}\Big)^{1/\kappa},\qquad
\theta_k\in\Delta,\ \kappa>0,
$$
<!-- definition -->

whose logarithm in log space is a softmax-affine function,

$$
\Phi_K(u)=\frac1\kappa\log\sum_{k=1}^{K}\exp\!\big(\kappa(\theta_k\cdot u-\beta_k)\big).
$$
<!-- definition -->

Softmax-affine functions are compatible with geometric programming (I4, Hoburg, Kirschen and
Abbeel [@hoburg2016data]), and $V_K$ is a generalized posynomial [@boyd2007tutorial]; L10 verifies
the posynomial identity (the coefficients are $c_k=e^{-\kappa\beta_k}$)
$\exp(\kappa\Phi_K)=\sum_ke^{-\kappa\beta_k}\prod_jm_j^{\kappa\theta_{kj}}$
for symbolic $K$ and $d$. Because each $\theta_k$ is on the simplex, L10 gives the shift
equivariance, the identity that the homogeneity, projection and invariant-form arguments rest on
(whether novelty carries over unchanged is expected from the construction, not proved by L10):

$$
\Phi_K(u+c\mathbf 1)=\Phi_K(u)+c,\qquad \Phi_1(u)=\theta_1\cdot u-\beta_1,
$$
<!-- lemma: L10 -->

and, with $x_k=\theta_k\cdot u-\beta_k$ and the maximum carried as the F10 symbol,

$$
\max_kx_k-\frac{\log K}{\kappa}\le\Phi_K(u)\le\max_kx_k,\qquad
\lim_{\kappa\to\infty}\Phi_K(u)=\max_kx_k .
$$
<!-- lemma: L10 -->

At $K=1$ this is the monomial fit; as $\kappa\to\infty$ it is a max of monomials, the form fitted
by convex piecewise-linear regression (maxima of affine functions) [@magnani2009convex]. That the
max of affine functions is the $\kappa\to\infty$ limit of the softmax-affine form is the
project's own statement (L10 proves the limit; Magnani and Boyd do not state this link). Needs: A2, A6, I4 for the GP
statement, and F10 for the limit (F10 holds when the symbol is the true maximum). What $K$ buys:
$K=1$ is one facet, with constant trade-off rates (in log space the analogue of weighted-sum
scalarization, a hypothesis we do not rely on); $K>1$ is any log-convex admissibility set with up
to $K$ facets, with regionally varying elasticities. We conjecture that this reduces the off-diagonal
optimism that confounds white space, in the limit only as far as the log-convex envelope fits; this
is expected from the construction and is neither proved by L10 nor tested. No $K$ represents non-log-convex structure: the picture is a
log-convex envelope, $K$ terms, plus a non-convex residual, the holes. L10 proves identities;
it does not provide a $K>1$ solver and proves nothing about fitted parameters. The solver, a
non-convex envelope fit with per-facet support and a selection of $(K,\kappa)$, is a later
package, and the estimator raises `NotImplementedError` for more than one term, pointing here. A
solver-free intermediate is to refit $K=1$ at several reference points.

| Formula | Implementation | Cross-check |
|---|---|---|
| $\Phi_K$, $K=1$ reduction | documented extension, not built | L10 `verify` (symbolic, no code counterpart) |
| `n_terms`, `exponents_` | `HyperbolicTradeSpace.fit` (rejects `n_terms != 1`) | estimator tests |

## Research direction: kernel methods under the GGP constraint

Kernel PCA performs PCA in a feature space defined implicitly by a kernel
[@schoelkopf1998nonlinear], and is the feature-engineering kin for this direction. The research
question is which kernel expansions remain generalized posynomials in $m$. Admissible ones are
those built from positive combinations, powers and max or softmax of monomials, in other words
exponentials of affine functions of $u$. A Gaussian radial basis function in log space is
log-quadratic and excluded. A natural candidate is a softmax-affine expansion anchored on support
designs,

$$
\Phi(u)=\frac1\kappa\log\sum_{i\in S}\exp\!\big(\kappa\,\theta_i\cdot(u-u_i)\big).
$$
<!-- definition -->

By definition, the data-level log-mean-exp is already a posynomial in the data (a sum of exponentials of affine terms in the log data, normalized by $1/N$), and
the dual weights $p_i$ of the fit are support weights; the support-vector analogy is a hypothesis
to examine, not a result. Open questions are choosing $S$ from $p_i$, the local normals
$\theta_i$, the roles of $\tau$ and $\kappa$, overfitting toward the data's convex hull, and
whether novelty and white-space semantics survive. The estimator's design (any term set
$\{(\theta_k,\beta_k)\}$ plugs in through $\Phi$) is meant not to preclude this direction. Nothing
here is built and nothing is claimed beyond its admissibility criterion.

## Summary of lemma coverage

| Lemma | Result | Where used above |
|---|---|---|
| L1 | homogeneity, invariant form | the model, projection, novelty |
| L2 | uniform shift | the fit, invariances |
| L3 | gradient and balanced KKT (premise R1) | the fit, shape not density |
| L4 | convexity (not strict) | the fit, identifiability |
| L5 | LSE versus LME, temperature limits (F5) | the fit, support function |
| L6 | Gaussian cumulant | noise |
| L7 | elasticities, improvement factors | interpretation, tensions |
| L8 | the chart | interpretation, prediction |
| L9 | pull-back | interpretation |
| L10 | extension $\Phi_K$ (F10) | the GGP extension |
