# Mathematics

This page sets out the mathematics of posynomial invariant form in the order of the pipeline. It is
discursive on purpose: each result is stated, said in words, tied to the lemma that proves it, and
tied to the hypotheses that lemma needs. The lemmas are plain-SymPy scripts in `derivation/`
(L1 to L14) and are machine-checked; machine verification shows that a formula follows from stated
hypotheses, and it is for a human to judge whether those hypotheses are reasonable for the problem
at hand. Throughout, formulas carry a tag comment naming the lemma that proves them, or marking
them as definitions, and the sections close with a small table pointing to the code that
implements them. Agreement of the code with the formulas is cross-checked in
`tests/test_matches_derivation.py`, which evaluates the lemmas' SymPy expressions at seeded numeric
instances and compares them with what the package returns. That check shows the code implements
the expressions; it does not re-prove them.

**Map and territory.** All models are wrong, some are useful, and a model is useful for a specific
purpose in a specific situation; here the purpose is improving trade studies. The formal results
below are properties of mathematical objects, conditioned on assumptions that we cannot certify
for a given table of designs, and the implementation is a numerical approximation of those objects.
Results are read in light of the gaps ledger,
`docs/superpowers/notes/abstraction-gaps.md`, which
records for each place where the map and the territory part the assumption that bridges it, what
cannot be proved, the evidence on how sensitive the results are, and what that means for reading
them. The rest of the text states the formal results exactly and cites the ledger instead of
repeating its conditions. The companion pages are [Why and how to use it](why-and-how.md) and
[Extensions and limitations](limitations.md); the words for the mathematics are fixed in the
register, `docs/superpowers/notes/notation.md`.

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
(the INHERITED axioms I1 to I9); those are listed with their statements in the ledger and in the
lemma headers. The six conditions in the table are the ones that carry interpretive weight: the
regularity conditions R1 and R2, the conditioning assumption A4, and the three fallback
hypotheses F5, F10 and F12 that we introduced because a step resisted abstract simplification in
SymPy. For R1, R2, F5, F10 and F12 the role and failure mode are quoted verbatim from the ledger.
The ledger records no role or failure mode for A4 (it is a plain posited axiom), so the entries
for A4 are written here and marked as such. The register of mathematical expressions in
`docs/superpowers/notes/notation.md` fixes the names of the objects these conditions are about.

| id | statement | interpretive role | failure mode |
|---|---|---|---|
| R1 | the balanced point lies in the relative interior of a facet of the frontier with positive normal; this is a statement about the hard-support (tau = infinity) geometry and does not imply that the finite-tau minimizer of J_tau is interior | makes the KKT balanced point a genuine interior frontier point, so the gradient condition identifies w* as the facet normal and the improvement factors and elasticities can be read as trade-offs along the frontier; where the fitted minimizer has w_j > 0 the equal-gradient condition holds on those coordinates | at a vertex, an edge or a facet with a zero normal component the gradient condition holds only as a subgradient inclusion: w* is not unique, some elasticities are undefined, and the frontier reading degrades to the weaker invariant-form reading; at finite tau the multiplicity of the observations can put the minimizer on the simplex boundary even when the hard-support geometry is balanced, and then only the full simplex KKT (g_j >= lambda, w_j (g_j - lambda) = 0) holds, with equal gradients on the positive-weight coordinates only |
| R2 | positive assignment margin: gamma = min_i [s_i,k(i) - max_{k != k(i)} s_ik] > 0, where s_ik = w_k.u_i - beta_k, so every row has a unique maximizing facet | gives unique maximizing facets and an assignment-stable neighborhood (radius gamma / (2 max_i \|\|(u_i, -1)\|\|_2)) on which the multi-facet objective equals its fixed-assignment expression, so Proposition 3 applies: a fit whose facets are exactly optimal is a local minimizer, and with gap-bounded facets Corollary 4 bounds the remaining improvement | ridge rows: a frontier row on two facet planes has margin zero at tau = infinity, and duplicate facets give identical scores; the neighborhood is then empty, Proposition 3 does not apply, and termination reports stationary_without_margin: the fit is first-order stationary per facet (levels 1 and 2) with no local-optimality claim |
| A4 | conditioning is log-affine and invertible: log m_j = alpha_j log(a_j + s_j) + b_j with alpha_j != 0 (negative alpha_j marks a cost attribute) | A4 is posited, so the ledger records none; stated here: it makes the pull-back to raw attributes an exact, invertible log-affine map (L9), so the fitted frontier can be read in the units of the attributes and negative exponents mark cost attributes | stated here: if conditioning is not log-affine and invertible (or is poorly chosen), the pulled-back formula no longer describes the attributes, the exponents $w$ describe the conditioned metrics only, and a different conditioning answers a different question |
| F5 | max representation for L5: the maximum of the scores is a symbol M with s_i <= M for all i in 1..n and s_{i0} = M for some i0 in 1..n | lets the tau -> infinity limit and the bound LME <= max be proved for symbolic n (sympy has no symbolic-n max and cannot take limits through the symbolic Sum): M - (log n)/tau <= LME <= M is squeezed with sympy.limit | the statement is about the actual maximum only when M really is max_i s_i; if M is any upper bound that is not attained the lower squeeze bound is lost and the limit is only an upper bound on the true limit |
| F10 | max representation for L10: the maximum over the K terms of x_k = theta_k.u - beta_k is a symbol M with x_k <= M for all k in 1..K and x_{k0} = M for some k0 in 1..K | lets lim_{kappa->inf} Phi_K = max_k x_k and the bounds max <= Phi_K <= max + (log K)/kappa be proved for symbolic K (same squeeze as F5), so the extension reads as a soft maximum of K affine log-scores | as F5: if M is not attained by some term the lower bound Phi_K >= M is lost and only the upper bound M + (log K)/kappa on the limit is available |
| F12 | min representation for L12 and L13: the minimum m of a finite family x_j (the gradient components g_j in L12, the row gaps in L13) is a symbol with x_j >= m for all j and x_{j0} = m for some j0 | lets the simplex gap G = g.w - min_j g_j and the bound min_{v in simplex} g.v = m be proved for symbolic d (sympy has no symbolic-d min): g.v - m = sum_j v_j (g_j - m) >= 0, attained at the vertex e_{j0} | as F5: if m is only a lower bound that is not attained, g.v >= m holds but the minimum over the simplex may exceed m, and G = g.w - m is then an upper bound on the first-order gap rather than its value |

The chart axiom A7 is also worth reading in the ledger's own words. Its role: "makes Z the
scale-free coordinates of the metric vector: Z is blind to a common multiplicative scale (a shift
of u along 1), and with the log-scale it gives an isometric linear bijection, so Gaussian noise and
distances can be read in Z". Its failure mode: "if B 1 != 0 the chart sees the overall scale and Z
is not invariant; if B B^T != I the chart is not isometric, so noise in u is not isotropic in Z and
distances in Z distort those in u". The Helmert basis used by the code is one realization of A7.

How to read the table. R1 concerns the single-term fit: when the balanced point is not in the
relative interior of a facet with positive normal, the fitted exponents are a subgradient choice,
not an identified trade-off, and even when it is, a finite-temperature minimizer can sit on the
boundary of the simplex (see [the fit](#the-fit)). R2 concerns the multi-facet fit: it is the
condition under which the solver's fixed assignment is a local optimum and not only a stationary
point (see [three levels](#three-levels-of-guarantee)), and it fails on ridge rows at
$\tau=\infty$. F5, F10 and F12 concern only the proofs: they say the symbol $M$ (or $m$) is the
actual maximum (or minimum), so they hold by construction for the quantity they name and cost the
reader nothing in practice; we list them because the ledger lists every hypothesis a proof used.
A4 is the condition analysts control: the interpretation of $w$ is an interpretation of the
conditioned metrics, and different conditioning gives a different, equally legitimate, question.

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

**Three objects.** Three surfaces in log space carry the word frontier, and the text keeps them
apart by name. The *fitted reference surface* is the level set $V=1$ ($\Phi=0$) of the fitted
model at its working temperature $\tau$; it is smooth, and since the soft maximum lies at or below
the maximum (L5) some designs have $V>1$ by construction. The *$\tau=\infty$ supporting envelope*
is the hard empirical object: at $\tau=\infty$ each fitted hyperplane supports the data, so no
design has $V>1$. The *Pareto boundary* is the boundary of the attainable set, the designs that
no attainable design dominates; L11 relates maximizers of $V$ to it, and nothing identifies either
fitted surface with it. The prose says frontier where the context fixes which is meant.

The scored quantity $\log V=w\cdot u-\beta$ is the *energy differential* (level offset) of a design
to the frontier: the potential $\Phi(u)=w\cdot u-\beta$ relative to the frontier's zero level, a
path-independent difference, equal by L1 and L2 to the uniform log-scaling step that carries the
design onto the frontier; negative inside and positive beyond. It is not a Euclidean
distance: the signed Euclidean distance from $u$ to the hyperplane is $\log V/\|w\|_2$.

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
designs nearest the envelope (the support weights). Write $g=U^\top p$. The fit is a minimization
over the simplex, so the first-order conditions are the full simplex conditions, with
$\lambda=w\cdot g$ the multiplier of the constraint $\mathbf 1\cdot w=1$:

$$
g_j\ge\lambda\ \ (j=1,\dots,d),\qquad w_j\,(g_j-\lambda)=0 .
$$
<!-- lemma: L3 -->

The gradient is equal to $\lambda$ on every coordinate with $w_j>0$ and may exceed it on a
coordinate with $w_j=0$. The equal-gradient reading, all components of $U^\top p$ equal
(balance), therefore holds on the positive-weight coordinates, and on all $d$ coordinates exactly
when the minimizer is interior to the simplex. Balanced hard-support geometry does not imply an
interior finite-temperature minimizer: L3 constructs an instance whose $\tau=\infty$ optimum is
balanced and whose finite-$\tau$ minimizer is on the boundary, with $g_j>\lambda$ at the inactive
$j$, because the multiplicity of the observations moves the soft maximum. R1 is a statement about
the hard-support geometry and carries no such implication. Needs: A2, A3 for the conditions, and
R1 for the reading of $w$ as the facet normal of the hard-support geometry. L3 takes the
Lagrangian conditions as given; it does not prove that the minimizer exists or is unique, nor
anything about the sign of $\lambda$.

**Convexity.** The fit is a convex program because, along any line,

$$
\frac{d^2}{dt^2}J_\tau(w+tv)\Big|_{t=0}=\tau\,\mathrm{Var}_p(v\cdot u)
=\frac\tau2\sum_{i,k}p_ip_k\,(s_i-s_k)^2\ \ge 0 ,
$$
<!-- lemma: L4 -->

where $s_i=v\cdot u_i$. Each term is a positive weight times a square, so the sum is nonnegative.
Needs: A1 (so $w\cdot u_i$ and $v\cdot u_i$ are real) and A3. L4 proves convexity of the objective,
not strict convexity; existence, uniqueness and stability are separate statements, made under
[Existence, uniqueness, stability](#what-the-stage-learns-and-why-it-is-shape) below. The code
reports the effective sample size $n_\mathrm{eff}=1/\sum_ip_i^2$ so the analyst can see how many
designs carry the fit.

| Formula | Implementation | Cross-check |
|---|---|---|
| $\mathrm{LME}_\tau(s)$, $\tau=\infty\Rightarrow\max$ | `solvers.log_mean_exp` | `test_matches_derivation.py` (L5 group), L5 `verify` |
| $p=\mathrm{softmax}(\tau Uw)$ | `solvers.support_weights` | L3 `verify` |
| $J_\tau$ and $\nabla J_\tau=U^\top p$ | `solvers.objective_and_grad` | `test_matches_derivation.py` (L3 group) |
| $\tau=\infty$ fit (linear program) | `solvers.solve_lp` | LP duality, I1 (checked numerically in the solver tests) |
| finite-$\tau$ fit | `solvers.solve_slsqp` | gradient and simplex KKT cross-check (L3) |
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

**4. Noise.** Under the log-space Gaussian model, $u=u^{\rm true}+\varepsilon$ with $\varepsilon_j$
i.i.d. $N(0,\sigma^2)$ and independent across $j$ (A5), the population objective gains
$\frac1\tau\log\mathbb{E}\exp(\tau\,w\cdot\varepsilon)$, and L6 (using I5 for the product of moment
generating functions) is the population identity

$$
\frac1\tau\log\mathbb{E}\exp(\tau\,w\cdot\varepsilon)=\frac{\tau\sigma^2\|w\|^2}{2}.
$$
<!-- lemma: L6 -->

The identity is between population quantities; it states the cumulant and is not a finite-sample
statement. Since the term is smallest where $w$ is uniform, in the population objective it acts as
a ridge toward balanced exponents. Needs: A2, A5, I5.

**5. The normalization.** The $1/N$ normalization of L5 (see the fit) makes the sample functional
an average, so $\beta$ is a property of the shape of the data and not of the number of designs;
replicating the sample leaves it unchanged (checked in the tests, I2). No statement of consistency
or finite-sample unbiasedness is made. One would need independence, integrability and
identifiability of the minimizer, entered as conditions in the gaps ledger, and neither L5 nor L6
supplies them.

**6. Invariances.** Uniform scaling shifts $\beta$ by $\log k$ and leaves $w$ and $V$ unchanged
(L2, L1). Permuting the metrics permutes $w$ (a symmetry of the objective, covered by the tests, not
a lemma). Rescaling a single metric changes which facet is tangent; this is the documented lever
of stage 2 and is outside L2. L8 gives the bijection between $u$ and $(Z,\text{log-scale})$; the passage to
$(Z,\log V)$ is an invertible affine change of coordinates that uses A2 and the fitted $w$ (our step, not part of L8), with $Z$
independent of $w$ (see the chart below).

**7. Existence, uniqueness and stability.** Three statements, kept apart. Let
$H=\tau\big(U^\top\mathrm{diag}(p)\,U-(U^\top p)(U^\top p)^\top\big)$ be the Hessian of $J_\tau$ at
the fit, so that $v^\top Hv=\tau\,\mathrm{Var}_p(v\cdot u)$ (L4); let $S$ be the set of participating
coordinates, $T$ an orthonormal basis of $\{v\in\mathbb{R}^{S}:\mathbf 1\cdot v=0\}$ and
$H_S=T^\top H_{SS}T$ the restricted Hessian.

*Existence.* The simplex is compact and $J_\tau$ is continuous, so a minimizer exists for every
finite table and every $\tau\in(0,\infty)$ (the extreme value theorem, not a lemma); at
$\tau=\infty$ the linear program has an optimal vertex.

*Uniqueness.* $J_\tau$ is convex (L4), so the minimizers form a convex set. A minimizer with
$H_S\succ0$ on its support $S$ and $g_j>\lambda$ off $S$ is a strict local minimizer and so the
only one. L4 proves $H\succeq0$; positive definiteness of $H_S$ is a property of the table at the
fit, not a theorem, and the fit reports it through `conditioning_`.

*Stability.* To first order a perturbation $\delta g$ of the gradient, from a change of the data
or of $\tau$, moves the exponents by $\delta w=-T H_S^{-1}T^\top\delta g_S$, so
$\|\delta w\|\le\|T^\top\delta g_S\|/\lambda_{\min}(H_S)$. Nearly correlated metrics make
$\lambda_{\min}(H_S)$ small: a change of $\tau$ then moves $w$ along the flat direction while the
objective changes only by about $\tfrac12\lambda_{\min}\|\delta w\|^2$. The estimator exposes
$\lambda_{\min}(H_S)$ per facet as `conditioning_`, with $S$ the coordinates above the
participation threshold; it is `nan` at $\tau=\infty$, where $J_\tau$ is not twice differentiable,
and for a facet with fewer than two participating exponents.

*Tolerances.* A metric participates when $w_j>10^{-3}$ (`PARTICIPATION_THRESHOLD`, the threshold of
the tension report). The contending set is the support of the $\tau=\infty$ linear-program
exponents, $w_j>10^{-9}$. An exponent at or below $10^{-12}$ (`EPS_ZERO_EXPONENT`) is numerically
zero, and scoring then treats it as an exact zero ($0\cdot\log0:=0$). An exponent is
mathematically zero when the exact minimizer has $w_j=0$, which complementary slackness allows
whenever $g_j>\lambda$.

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

The fitted exponents and exchange rates are features of the conditioned empirical model: they
describe how the sampled, conditioned designs trade, and they are not a causal exchange that
changing a design variable would reproduce.

**The chart.** Coordinates are the log-ratio chart together with the energy differential to the frontier:

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
position along the frontier and $\log V$ the energy differential (level offset) from it. The Helmert basis is one realization
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

**A maximizer of $V$ is Pareto-efficient (L11).** For $w\in\Delta$ and a design that is better in every metric,
$u'=u+\delta$ with $\delta\ge0$,

$$
w\cdot u'-w\cdot u=\sum_{j=1}^{d}w_j\,(u'_j-u_j)\ge0 ,
$$
<!-- lemma: L11 -->

which is strict as soon as one metric with $w_j>0$ is strictly better. L11 (A1, A2) proves this
for symbolic $d$, and so $V(u')\ge V(u)$ with strict inequality under the same condition. Hence a
design that maximizes $V$ over a set of designs is not dominated in the contending metrics by any
member of the set: it is weakly efficient in all $d$ metrics, and efficient when every exponent is
positive. At $K>1$ and $\kappa=\infty$ the same holds for $\Phi_K$ through a term active at the
maximizer: if $u'\ge u$ were no worse, the active term would score $u'$ at least as high, so it
gains nothing in the metrics that term uses (L11, which proves it at symbolic $d$).

L11 does not state the converse. Weighted-sum scalarization reaches only the part of a Pareto front
that some $w$ supports (the log-convex part, here); a front point on a non-log-convex part is
efficient and is the maximizer of $V$ for no $w$ [@miettinen1999nonlinear; @ehrgott2005multicriteria].
L11 also does not say which $w$ to use, nor that the fitted frontier is the true front.

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
   is locally on the frontier, because a single hyperplane is tangent only at one place. Our
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
both, then read the predicted $\log V$ (energy differential to or beyond the frontier), the predicted $V-1$
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

In the fit and in the code the exponent vector of term $k$ is written $w_k=\theta_k$ (the
`exponents_` rows). Softmax-affine functions are compatible with geometric programming (I4, Hoburg,
Kirschen and Abbeel [@hoburg2016data]), and $V_K$ is a generalized posynomial
[@boyd2007tutorial]; L10 verifies the posynomial identity (the coefficients are
$c_k=e^{-\kappa\beta_k}$) $\exp(\kappa\Phi_K)=\sum_ke^{-\kappa\beta_k}\prod_jm_j^{\kappa\theta_{kj}}$
for symbolic $K$ and $d$. Because each $\theta_k$ is on the simplex, L10 gives the shift
equivariance, the identity that the homogeneity, projection and invariant-form arguments rest on
(whether novelty carries over unchanged is expected from the construction, not proved by L10):

$$
\Phi_K(u+c\mathbf 1)=\Phi_K(u)+c,\qquad \Phi_1(u)=\theta_1\cdot u-\beta_1,
$$
<!-- lemma: L10 -->

and, with $x_k=\theta_k\cdot u-\beta_k$ and the maximum carried as the F10 symbol,

$$
\max_kx_k\le\Phi_K(u)\le\max_kx_k+\frac{\log K}{\kappa},\qquad
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
log-convex envelope, $K$ terms, plus a non-convex residual, the holes.

### The solver for small $K$

L10 proves identities; it says nothing about how to choose $(w_k,\beta_k)$ from data. The fit of
an envelope with $K$ facets is not a convex program (the assignment of designs to facets is
combinatorial), so the estimator uses the partition-and-refit scheme that Magnani and Boyd give for
maxima of affine functions [@magnani2009convex], adapted to the one-sided entropic fit of this
page. The estimator is built for small $K$ (the case study uses $K=3$); scalability to large $K$ and
speed are future work. In the style of Boyd and Vandenberghe's algorithm boxes [@boyd2004convex]:

> **given** log-metrics $u_1,\dots,u_N$ (rows with a zero metric are set aside), the number of
> terms $K$, the fit temperature $\tau$ (A3), a number of restarts, an iteration cap.
>
> **for each restart** (the seeds are drawn from `random_state`):
>
> 1. *Initialize.* Choose $K$ rows at random as centres. Map every row to the chart coordinates
>    $z_i=Bu_i$ (the Helmert coordinates of L8, in which the overall scale is projected out) and
>    give it the label $k(i)$ of the nearest centre.
> 2. *Refit (step B, the default).* For each facet $k$, with $\bar u_k$ the mean of its rows, find the supporting
>    hyperplane $w_k=\arg\min_{w\in\Delta}\ J_\tau(Uw)-\bar u_k\cdot w$ over **all** $N$ rows (at finite
>    $\tau$, polish the solver's answer with five reduced-Newton steps on the active set), and set
>    $\beta_k=J_\tau(Uw_k)$. Compute the objective, the mean slack
>    $\bar s=\frac1N\sum_i\big(\beta_{k(i)}-w_{k(i)}\cdot u_i\big)$.
>
> **repeat**
>
> 3. *Reassign.* $k'(i)=\arg\max_k\ (w_k\cdot u_i-\beta_k)$.
> 4. If $k'=k$, **stop**: the assignment is fixed.
> 5. *Refit* on $k'$ as in step 2, giving $\bar s'$. If $\bar s'>\bar s+10^{-12}$ reject the iteration and
>    **stop** with the previous state (the monotone guard); otherwise accept it.
>
> **until** the assignment is fixed, the guard fires or the iteration cap (50) is reached.
>
> **return** the restart with the smallest $\bar s$: exponents $w_k$, offsets $\beta_k$ and labels,
> with the stopping declaration of that restart (below).
>
> (With `facet_step="tangent"`, step D below replaces $w_k$ in the refits after the first, the guard
> in step 5 is not applied, and the iterate with the smallest $\bar s$ is returned.)

**The per-facet problem as step 2 solves it.** The refit is written $J_\tau(Uw)-\bar u_k\cdot w$,
where $J_\tau(Uw)$ is the objective of the fit section applied to **all** rows. It is the entropic
fit with the log-metrics centred at the facet's mean, so it is the same convex program as the
$K=1$ fit (`solvers.solve_slsqp`, or the linear program at $\tau=\infty$) on shifted data. Read
geometrically, $w_k$ is the supporting hyperplane of the whole cloud that is tightest on the
facet's rows: at the solution $\beta_k-w_k\cdot\bar u_k$ is the mean slack of the facet's own rows
below the soft supporting hyperplane, and $\beta_k$ is a support value of all $N$ rows, so that
$V=1$ is the frontier and the coefficients $e^{-\kappa\beta_k}$ keep the meaning they have at
$K=1$. Call this step B (the `facet_step="support"` default).

The alternative, refitting facet $k$ by the plain $K=1$ fit on its own rows only, is the own-rows
refit. Measured on the planted $K=3$, $d=4$ frontiers with the **true** labels given, so that the
alternation plays no part, it recovers 0 of 60 planted facets (the linear program on the true rows
of seed 0 returns $(0.416,0,0.119,0.465)$ for the planted $(0.212,0.334,0.245,0.209)$), while step B
recovers 60 of 60, including facets with only two to four frontier rows, because the facet's
roughly 130 interior rows locate it
(`docs/superpowers/notes/spike-facet-refit/`, section 3a). The reading of why is under
[what is only observed](#what-is-proved-what-is-inherited-what-is-only-observed). At $K=1$ the
solver reduces to the single-term fit of the fit section (`solvers.solve_terms` returns the
`solvers.solve_slsqp` result).

**The objective.** The alternation minimizes the mean slack $\bar s$, the average over rows of
the gap between the row's own facet plane and the row. It is the $K>1$ analogue of the $K=1$
reach: at $K=1$ the objective is the reach $J_\tau(w)$, the size of the envelope above the cloud;
at $K>1$ the sum of the facets' reaches is degenerate (every facet would repeat the $K=1$ fit),
and the non-degenerate size of a $K$-facet envelope against the whole cloud is the mean slack, the
one-sided volume between the cloud and the envelope (the one-sided $L^1$ criterion of Magnani and
Boyd's max-affine fit [@magnani2009convex]). Under step B each half-step does not increase it:
reassignment picks for every row the term with the largest score, which is the smallest slack, and
the refit minimizes a convex function of $w_k$ of which the previous $w_k$ is a feasible point.
The guard enforces the monotonicity in the code regardless of how well the inner solver
converged. The measured fraction of half-steps in which the mean slack got worse is 0.000 for
both the reassignment and the refit of step B, at $\tau=\infty$ and at $\tau=50$ (the second
spike, table 1); every other objective the spike tried (touch counts, band means, entropic
variants) worsens in some half-steps of B, or is constant at $\tau=\infty$. The scheme stops at a
fixed assignment, the guard or the iteration cap, and returns a fit whose stopping record says
which of the three levels below hold; the restarts keep the best of several by mean slack.

**Step D, the evidence-driven alternative.** With `facet_step="tangent"` the direction of facet
$k$ is taken from the rows that actually lie on it. Its near-frontier rows are its own rows within
$1/\tau$ of its support plane ($0.1$ at $\tau=\infty$, as elsewhere in the toolkit); when there
are at least $d+1$ of them, $w_k$ is their smallest-variance direction, a constrained
total-least-squares normal on the simplex (the complementary end of the principal-component read
that the tension report takes of the same rows), and when there are fewer the facet falls back to
step B. The first refit is always step B, $\beta_k$ is the support value over all rows in both
steps, and the sparsity penalty acts on step B only. D is more robust than B to a wrong
assignment in mid-alternation, since misassigned interior rows are not near the plane and do not
pull it (16 against 12 passes of 20 from one common start at $\tau=\infty$; first spike,
section 3b). **The mean slack is not monotone under D**: it rises in 35 to 50 percent of D's
refits at $\tau=\infty$ and 35 percent at $\tau=50$ (second spike, table 1), nothing is monotone
under it, and a guard on the mean slack would remove its gain. The code therefore applies the
guard to B only; under D the loop stops at a fixed assignment or the cap and returns the iterate
with the lowest mean slack that it saw, so the returned fit is no worse by that measure than any
visited, but the sequence of iterates need not decrease.

**Which step the paper presents.** Both steps are kept in the code and the evidence base
(supervisor's decision at the acceptance gate of WP9), but the paper presents the mean-slack
approach, step B, because of its monotone guarantee: the objective it minimizes is an
interpretable quantity (the envelope's one-sided volume) that cannot rise, and it is the default.
Step D is offered as the alternative that uses the near-frontier evidence directly, with its
non-monotonicity disclosed.

### Three levels of guarantee

The multi-facet fit carries three statements of increasing strength, and the stopping declaration
below says which of them hold for a returned fit. They are not equivalent: a small change of the
objective, a stop at the iteration cap or a small gap does not by itself establish local
optimality. They are stated for step B (`facet_step="support"`), unpenalized, with the support
offsets $\beta_k=J_\tau(Uw_k)$ only. Write $C_k$ for the rows assigned to facet $k$, $n_k=|C_k|$,
$\bar u_k$ for their mean log-metric, and

$$
f_k(w)=J_\tau(Uw)-\bar u_k\cdot w,\qquad
F(W)=\frac1N\sum_{i}\big(\beta_{k(i)}-w_{k(i)}\cdot u_i\big)=\sum_{k}\frac{n_k}{N}\,f_k(w_k),
$$
<!-- lemma: L12, L14 -->

the facet refit, convex by L4, and the mean slack. The second equality regroups the rows by facet
and uses $\beta_k=J_\tau(Uw_k)$ (L14, needs A2).

#### Level 1: descent

In exact arithmetic each half-step of step B leaves the mean slack unchanged or lowers it:
reassignment gives each row its largest score, which is its smallest slack, and the refit
minimizes the convex $f_k$ (L4), of which the previous $w_k$ is a feasible point. The code enforces
it up to the guard tolerance $10^{-12}$ (`GUARD_TOL`). Descent says the loop does not undo its
progress; it does not say that the point where it stops is stationary or optimal.

#### Level 2: numerical stationarity

**Lemma 1 (L12).** For the facet refit $f_k$ on the simplex, with
$g=\nabla f_k(w)=U^\top\mathrm{softmax}(\tau Uw)-\bar u_k$, the first-order gap (the facet gap) is

$$
G_k(w)=\max_{v\in\Delta}\,g\cdot(w-v)=g\cdot w-\min_j g_j=\sum_j w_j\,\big(g_j-\min_l g_l\big)\ \ge0,
$$
<!-- lemma: L12 -->

and $0\le f_k(w)-f_k^*\le G_k(w)$, with $G_k(w)=0$ exactly when the simplex KKT conditions of L3
hold ($g_j\ge\lambda$, $w_j(g_j-\lambda)=0$, $\lambda=w\cdot g$). Needs: A2, A3, the first-order
convexity inequality I8 for the bound, and the min representation F12 for symbolic $d$.

The gap is the residual of the KKT conditions as one number, and it bounds how far the facet's
objective is from its optimum. At $\tau=\infty$ the refit is a linear program, and with its dual
weights $p$ the gap is $f_k(w)-\min_j(U^\top p-\bar u_k)_j$, the primal objective minus the dual
objective: the linear-programming duality gap (I1, L12), zero at an optimal primal-dual pair. The
solver keeps the duals; uniform weights on tied rows give a valid but loose bound. At finite $\tau$
SLSQP stops with $G_k$ of order $10^{-5}$ although its point is within $10^{-11}$ of $f_k^*$, so
the bound is loose by six orders there; the solver therefore polishes each facet with five
reduced-Newton steps on the active set (`POLISH_STEPS`), which bring $G_k$ to about $10^{-15}$ on
the planted data. A fit is numerically stationary when every nonempty facet has
$G_k\le\varepsilon_{\rm KKT}=10^{-8}$ (`EPS_KKT`).

#### Level 3: conditional local optimality

**Lemma 2 (L13).** Let $s_{ik}=w_k\cdot u_i-\beta_k$ be the energy differential of design $i$
against facet $k$, $k(i)$ its maximizing facet, and

$$
\gamma=\min_i\Big[s_{i\,k(i)}-\max_{k\ne k(i)}s_{ik}\Big]
$$
<!-- lemma: L13 -->

the assignment margin. If every facet score changes by at most $\delta$ with $2\delta<\gamma$, the
maximizing facet of every row is unchanged and unique. By Cauchy-Schwarz (I9) this holds whenever
every facet's parameters $(w_k,\beta_k)$ move by less than

$$
r=\frac{\gamma}{2\max_i\big\|(u_i,-1)\big\|_2}
$$
<!-- lemma: L13 -->

in Euclidean norm. The bound $r$ is the stable radius, and the ball it defines is the
assignment-stable neighbourhood. Needs: R2 ($\gamma>0$), F12, I9. The
radius is sufficient and not tight.

**Proposition 3 (L14).** Suppose the margin is positive (R2), every facet is nonempty, and every
$w_k$ minimizes $f_k$ over the simplex. Then on the assignment-stable neighbourhood, with support
offsets $\beta'_k=J_\tau(Uw'_k)$,

$$
F(W')-F(W)=\sum_k\frac{n_k}{N}\big(f_k(w'_k)-f_k(w_k)\big)\ \ge0,
$$
<!-- lemma: L14 -->

so $W$ is a local minimizer of the mean slack. The full objective, the mean over rows of the
smallest slack, equals the fixed-assignment expression $F$ there because R2 keeps each row's
maximizing facet. Needs: A2, R2. Global optimality and global convergence are not claimed.

**Corollary 4 (L14).** With $F^*_{\rm fixed}=\sum_k\frac{n_k}{N}f_k^*$ the optimum of the objective
at the fixed assignment, the facet gaps of Lemma 1 give the approximate certificate

$$
0\le F(W)-F^*_{\rm fixed}\le\sum_k\frac{n_k}{N}\,G_k(w_k).
$$
<!-- lemma: L14 -->

The right side is reported as the Corollary bound. It is a bound for the assignment of the returned
run, not across restarts.

**What step D, the penalty and `min_exponent` do to each level.** Level 3 is for step B,
unpenalized, with support offsets only; Proposition 3 needs $w_k$ to minimize $f_k$ and
$\beta_k=J_\tau(Uw_k)$. Level 1 holds for step B alone: the mean slack is not monotone under
step D. Level 2 is reported at every setting and certifies only the unpenalized $f_k$: under step D
the exponent $w_k$ is a total-least-squares normal, not the minimizer of $f_k$, so $G_k>0$ is
expected and measures how far the normal sits from the support optimum; under the penalty the
refit minimizes a different objective, and the gap of the unpenalized $f_k$ is a diagnostic. The
status is `not_applicable` for both. With `min_exponent` $m>0$ the feasible set is
$\{w\ge m,\ \mathbf 1\cdot w=1\}$ and the implemented gap is measured to it,
$G=g\cdot w-m\,\mathbf 1\cdot g-(1-dm)\min_jg_j$ (`solvers.simplex_gap`); the lemmas are proved
for the simplex ($m=0$) and the floored form is implemented and tested at $m=0$.

#### The stopping declaration

When a restart stops, its returned fit is declared with a `Termination` record
(`solvers.TermsResult.termination`, exposed as `termination_` on the estimator). The tolerances
are module constants: $\varepsilon_{\rm KKT}=10^{-8}$ (`EPS_KKT`) for the maximal facet gap,
$\varepsilon_{\rm feas}=10^{-9}$ (`EPS_FEAS`) for the feasibility residuals (the exponents sum to
one, the floor holds) and for the positivity of the margin, $10^{-12}$ (`GUARD_TOL`) for the guard,
five Newton steps (`POLISH_STEPS`), and an iteration cap of 50. The record holds the status, the
iterations, the feasibility and offset residuals, the maximal gap, the Corollary bound, the
objective change at the last accepted step, the assignment changes (rows whose argmax differs from
the returned label), the number of empty facets, the margin and radius, and the per-facet gaps and
shares. The stopping rule is the fixed assignment, not a small objective change, and the record
reports both.

| status | what holds | what is claimed |
|---|---|---|
| `certified` | assignment fixed; residuals at most $\varepsilon_{\rm feas}$; $\max_kG_k\le\varepsilon_{\rm KKT}$; no empty facet; $\gamma>\varepsilon_{\rm feas}$ | levels 1 to 3: Proposition 3 up to the facet gaps, which Corollary 4 bounds and the record reports |
| `stationary_without_margin` | the same, with $\gamma\le\varepsilon_{\rm feas}$ (a row ties between facets, for example two identical facets) or an empty facet | levels 1 and 2; R2 fails and no local-optimality claim is made |
| `uncertified` | assignment fixed, but a residual or the gap exceeds its tolerance | level 1 only |
| `guard_stop` | an iteration raised the mean slack by more than $10^{-12}$; the previous state was returned | level 1 only; reported apart from `certified` |
| `iteration_cap` | the cap of 50 was reached | level 1 only; reported apart from `certified` |
| `not_applicable` | step D, a penalty, or the $K=1$, $d=1$, $N<K$ shortcut | the gaps are diagnostics |

The estimator raises a `ConvergenceWarning` for `uncertified`, `guard_stop` and `iteration_cap`.

**Measured certificates.** On the planted data (`make_frontier_data(400, 4, n_terms=3, random_state=s)`,
$s=0,\dots,19$; `solve_terms(U, 3, tau, random_state=0)`, the estimator's call) every chosen run
stops on a fixed assignment with no empty facet:

| $\tau$ | `certified` | `stationary_without_margin` | $\max_kG_k$ (largest) | $\gamma$ (min / median / max) | radius $r$ (median) | Corollary bound (median) |
|---|---|---|---|---|---|---|
| $\infty$ | 16 of 20 | 4 of 20 (seeds 1, 3, 8, 16) | $2\times10^{-15}$ | $4\times10^{-17}$ / $5.3\times10^{-4}$ / $5.9\times10^{-3}$ | $2.2\times10^{-5}$ | $4.7\times10^{-16}$ |
| 50 | 20 of 20 | none | $5\times10^{-15}$ | $2.5\times10^{-4}$ / $1.1\times10^{-3}$ / $2.2\times10^{-3}$ | $4.6\times10^{-5}$ | $1.5\times10^{-15}$ |

At $\tau=\infty$ the four zero-margin seeds are the four recovery failures of step B below: a
frontier row lies on two facet planes. The case-study record
(`docs/superpowers/notes/k3-cubesat.md`) carries the same columns for the cubesat fits.

| Formula | Implementation | Cross-check |
|---|---|---|
| $f_k$, $F(W)$ | `solvers.facet_objective`, `solvers.fixed_assignment_bound` | L14 `verify`; solver tests |
| $G_k$ | `solvers.simplex_gap`, `solvers.facet_gap` | L12 `verify`; LP duality gap and $0\le f-f^*\le G$ in the solver tests |
| $\gamma$, $r$ | `solvers.assignment_margin` | L13 `verify`; perturbation tests within the radius |
| Corollary bound | `solvers.fixed_assignment_bound`, the `bound` field of `solvers.Termination` | L14 `verify`; solver tests against independent per-facet solves |
| stopping declaration | `solvers.Termination`, `termination_` | solver and estimator tests |

**Measured recovery.** On the planted generator at $K=3$, $d=4$, $N=400$ (30 percent of the rows
on the frontier; `make_frontier_data(400, 4, n_terms=3, random_state=s)`, $s=0,\dots,19$), with the
estimator defaults, five restarts and `random_state=0`, a seed passes when the matched exponents
are within 0.05 of the planted ones and at least 90 percent of the frontier rows are on the right
facet. Step B recovers 16 of 20 at $\tau=\infty$ (failing seeds 1, 3, 8, 16) and 16 of 20 at $\tau=50$
(1, 3, 8, 16); step D recovers 16 of 20 at $\tau=\infty$ (1, 3, 8, 16) and 17 of 20 at $\tau=50$
(1, 3, 16). The guard tolerance moved one entry: step B at $\tau=\infty$ recovered 17 of 20
(failing 1, 3, 16) before it, and seed 8 now stops in a different local optimum. The failures have
one cause. Seeds 1, 3 and 16 have a facet with only five or six
frontier rows (or fewer in the planted draw, before the generator's top-up), so the facet is
barely determined and its mean-slack optimum sits in a local optimum that no restart escaped;
seed 8 is a local optimum with a well-populated facet (11 frontier rows). The generator at
`n_terms=K` guarantees at least $d+1$ frontier rows per facet. That condition is **necessary**:
a facet with fewer frontier rows than dimensions is not determined by them, every edge-only
objective is flat across the family of hyperplanes through them, and no restart of either step
passed on such a facet (second spike, section 2). It is **not sufficient**: seeds 3 and 8 satisfy
it and still fail in some settings, and a thin facet near the bound leaves local optima. The claim
is therefore the measured rate on these 20 seeds under the generator's conditions, not a
guarantee of recovery. The two spikes hold the measurements and the throwaway scripts that
produced them: `docs/superpowers/notes/spike-facet-refit/` (the per-facet step: oracle recovery,
the alternation from common starts) and `docs/superpowers/notes/spike-objective/` (the objective:
monotonicity, identifiability, selection among restarts).

After the fit, scoring uses $\Phi_K$ with the hard offsets $\beta_k$ kept. At the default
$\kappa=\infty$ the score is the exact maximum $\max_k(w_k\cdot u-\beta_k)$; at finite $\kappa$ it
is the softmax of L10, which lies within $(\log K)/\kappa$ above the maximum (L10, F10), a gap that
is disclosed and not renormalized. The chart $[Z\mid\log V]$ keeps $Z=Bu$ and uses $\log
V=\Phi_K(u)$; because $B\mathbf 1=0$ (A7) and $\Phi_K$ is shift-equivariant (L10), a chart point
maps back in closed form, $u=B^{+}Z+\big(\log V-\Phi_K(B^{+}Z)\big)\mathbf 1$, exactly for every
$\kappa$ (L8, L10). Each facet has its own exponents, so the tensions of the analysis toolkit are
read facet by facet: one contending set, one set of exchange rates (L7) and one reach $\beta_k$ per
facet, with the facet's share of the near-frontier designs as the analogue of explained variance.

**The sparsity option.** The existing rules that keep a metric out of a term are the floor
`min_exponent` (a lower bound on every exponent), the support of the $\tau=\infty$ linear
program, and a threshold on the working-temperature weights. The solver also offers a
regularization-based alternative, as a keyword argument: `penalty="reweighted_l1"` with weight
`alpha`. On the simplex the plain $\ell_1$ norm is constant, so the penalty is the reweighted
$\ell_1$ of Candès, Wakin and Boyd [@candes2008enhancing]: after the unpenalized solve, three rounds
minimize $J_\tau(w)+\alpha\sum_jw_j/(w^{\text{prev}}_j+\epsilon)$, starting from the previous
round, and entries below $10^{-8}$ are set to exact zero. A zero exponent removes the metric from
the product (the hazard of the logarithm is a zero metric, which is masked), so the zeros are
safe. With `alpha=0` the fit is exactly the unpenalized one. The penalty acts at finite $\tau$ and
is passed to every facet's refit; at $\tau=\infty$ the linear program is returned unchanged. That
it helps recover the planted zeros is checked on a planted sparse facet in the solver tests; that
it picks the right metrics on real data is not claimed.

### What is proved, what is inherited, what is only observed

**Proved.** The identities of $\Phi_K$ (the posynomial form, shift equivariance, the $K=1$
reduction, the bounds and the limit) are L10; that a maximizer of $V$ is Pareto-efficient is L11,
in Interpretation. The chart inverse above is L8 and L10 combined. The simplex KKT conditions and
the finite-temperature boundary example are L3, and the Gaussian cumulant is a population identity
(L6). Levels 2 and 3 of the multi-facet fit are Lemma 1 (L12), Lemma 2 (L13), Proposition 3 and
Corollary 4 (L14), each under the hypotheses stated with it; level 1 is argued from L4 above and is
not a lemma.

**Inherited.** That alternating partition and refit stops at a local optimum rather than cycling
is the result of Magnani and Boyd for the least-squares max-affine problem (ledger entry I7). Our
objective (mean slack) and refit (a supporting hyperplane of the entropic fit) are different, so I7
is the pattern the scheme follows and not a theorem about this objective; what protects against
cycling here is the monotone guard and the iteration cap. I7 states a local optimum, with the
failure mode that the limit depends on the initial partition; restarts mitigate it. I7 is a solver-level inherited entry, a result the implementation leans on that no lemma consumes (the rule is in the proof conventions, "Solver-level inherited entries"). The first-order convexity inequality (I8), Cauchy-Schwarz (I9) and LP duality (I1) are the inherited steps of Lemmas 1 and 2.

**Only observed.** (i) Recovery on planted data: on planted $K=3$, $d=4$ frontiers at $N=400$ the
exponents are recovered to 0.05 in 16 or 17 of 20 seeds for either step and either $\tau$ (step B
16 and 16, step D 16 and 17, at $\tau=\infty$ and $50$), not in every seed; the failures are
planted facets with only five or six frontier rows, trapped in local optima, and one seed with a
well-populated facet (see the measured recovery above). At $N=600$ with half the rows on the
frontier the rate was 19 or 20 of 20. (ii) The cubesat record
(`docs/superpowers/notes/k3-cubesat.md`) reports the $K=1,2,3$ fits on two datasets. The mean
slack at $K=3$ is 0.117 against 0.204 at $K=1$ in the primary regime (0.093 against 0.131 in the stock regime), at a temperature re-selected at each $K$; the $K=3$ objective agrees across five seeds to
within $2\times10^{-6}$ in the primary regime, and in the stock regime one seed of five reaches a worse optimum (0.114 against 0.093). (iii) The temperature is re-selected at each $K$ by
the $K=1$ criterion, a tenth of the designs above $V=1$: $\tau$ is 38.1, 113 and 195 at $K=1,2,3$ in the primary regime and `frac_above_` is 0.096, 0.096 and 0.098. Reusing the $K=1$ $\tau$ instead raises the fraction (0.096, 0.261, 0.382), because each facet is a supporting hyperplane at that $\tau$ but the envelope is the maximum over facets; that table is kept in the record as a diagnostic. Whether the target fraction should differ by $K$ is open. (iv) The sliver: refitting a facet on its own rows tilts to a simplex vertex on the planted data
(0 of 60 facets recovered from the true labels). That the rows of one facet lie in a cone of the
chart that does not enclose the origin, so that the minimizer of their support function is a
vertex, is the reading of that measurement and not a theorem; a minimizer in the interior of an
edge is possible. (v) Which status a fit reaches is measured, not proved: the table of certificates
above is for 20 planted seeds. None of these is a guarantee on other data. **Nothing is claimed
about global optimality.**

### Simplifying assumptions

The solver makes simplifying assumptions. For each we name it, defend it and say how we would go
beyond it.

1. **Hard assignment, with smoothing on request.**
   The facets are assigned and fitted at $\kappa=\infty$, a hard maximum with kinks (ridges where
   two terms tie). Smoothness matters for gradients, level sets and plots, which want a
   differentiable $\Phi_K$. *Defence:* the smooth $\Phi_K$ is available on request by setting
   `term_temperature` $=\kappa$, which leaves the facets unchanged and moves the score by at most
   $(\log K)/\kappa$ (L10, F10); the kinks sit exactly on the ridges, where the facet labels
   change, so smoothing rounds a corner and does not change the facets. *Beyond:* future work. We
   expect, and have not shown, that the searches built on this frontier tolerate the kinks. At a
   ridge a maximum of smooth functions has a tangent cone, and its generalized gradient is the
   convex hull of the normals $w_k$ of the active terms, which is the object that
   common-direction and subgradient methods already work with. A nonsmooth search on the tangent
   cones of the ridges, and the choice of $\kappa$ by its effect on that search, are the way
   beyond.

2. **A fixed assignment, with restarts.** The partition-and-refit loop stops at a fixed assignment
   of a non-convex problem, stationary per facet and, when the margin is positive, a local optimum
   (levels 2 and 3; I7 is the pattern the scheme follows), and which one depends on the initial
   centres. *Defence:* every refit is
   convex, the objective never increases under the default step (the guard), the restarts keep the
   best of several (five by default), and on the planted and cubesat data the optimum was
   reproducible across seeds (observed above). Thin facets (five or six frontier rows) are the
   known trap. *Beyond:* a global search or a certificate of global optimality; none is claimed.

3. **The analyst chooses $K$.** There is no automatic selection of the number of terms
   (supervisor's decision OD1). *Defence:* the right $K$ is a modelling choice about how many
   trade-off regimes to distinguish, in the way the number of retained components is for PCA, and a
   criterion would hide it. The diagnostic is a table of the objective and `frac_above_` by $K$,
   read like a scree plot (for the cubesat primary regime the mean slack is 0.2036, 0.0900 and
   0.0529 at $K=1,2,3$; the objective falls with $K$ by construction, so it cannot choose $K$ by
   itself). *Beyond:* a selection rule, for example one that penalizes complexity or uses held-out
   designs, is future work.

4. **Small $K$ only.** The solver is a Python loop of convex fits, with restarts, tested at
   $K\le3$. *Defence:* the case study needs three regimes, and a small $K$ keeps each facet's
   contending set readable. *Beyond:* scalability and performance (many terms, many designs) are
   future work.

5. **The per-facet step: the mean-slack supporting hyperplane.** A facet's plane is fitted against
   all rows, not only its own (step B), and the alternation minimizes the mean slack. *Defence:*
   the own-rows refit is ill-posed (0 of 60 planted facets recovered even from the true labels,
   against 60 of 60 for B); the plane is the one the facet would have as a support of the whole
   data set, which is what makes it an upper envelope; and the mean slack is the $K>1$ analogue of
   the $K=1$ reach and is monotone under either half-step, which is why the paper presents this
   approach. The cost is that a facet is influenced by rows that another facet owns, and that the
   mean slack prefers to split a large facet rather than keep a sparse one, so a facet with five
   or six frontier rows can be lost to a local optimum (measured above). *Beyond:* two
   alternatives were built and measured and are parked. A non-monotone evidence step, D
   (`facet_step="tangent"`, kept in the code), takes the direction from the near-frontier rows and
   recovers about as often (16 or 17 of 20) but gives up the guarantee. A frontier-weighted
   objective (a slack counted on near-frontier rows only, or an entropic variant) was measured
   against the mean slack and was not better: edge-only objectives are flat on facets with too few
   frontier rows, and the exact minimizer of the entropic variant destroyed the fit on planted and
   cubesat data. A joint fit of all terms would remove the facet-by-facet dependence. None is
   claimed.

6. **A log-convex envelope.** $\Phi_K$ is convex in $u$, so the frontier is a log-convex
   envelope, plus a residual (holes) that no $K$ represents. *Defence:* this is the form that
   stays inside geometric programming (I4) and keeps the later optimization convex. *Beyond:* the
   kernel methods under the GGP constraint below, which keep a posynomial form with more terms.

| Formula | Implementation | Cross-check |
|---|---|---|
| $\Phi_K$, argmax assignment, partition-and-refit | `solvers.solve_terms`, `HyperbolicTradeSpace.assign_facets` | L10 `verify`; planted $K=3$ recovery in the solver and estimator tests |
| supporting-hyperplane refit (step B), tangent step (D), sparsity option | `solvers.solve_slsqp` (centred data; `penalty`, `alpha`), `solvers.solve_terms(facet_step=...)` | solver tests, both steps on planted data |
| `n_terms`, `exponents_` | `HyperbolicTradeSpace.fit` | estimator tests |
| $\Phi_K(u+c\mathbf 1)=\Phi_K(u)+c$, chart inverse | `HyperbolicTradeSpace.inverse_transform` | L10 `verify`; round-trip tests |
| $w\cdot u'\ge w\cdot u$ for $u'\ge u$ | the maximizer of `HyperbolicTradeSpace.score_samples` | L11 `verify` (symbolic) |
| $G_k$, $\gamma$, $r$, the Corollary bound, the status | `solvers.Termination`, `termination_`, `conditioning_` | L12 to L14 `verify`; solver and estimator tests |

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

From the definition, $\exp(\tau\cdot\text{log-mean-exp})$ is the mean of exponentials of affine terms in the log data, which is a posynomial in the data (a sum of monomials with positive coefficients $1/N$), and
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
| L3 | gradient, full simplex KKT and the finite-temperature boundary example (R1 for the facet-normal reading) | the fit, shape not density |
| L4 | convexity (not strict) | the fit, identifiability |
| L5 | LSE versus LME, temperature limits (F5) | the fit, support function |
| L6 | Gaussian cumulant, a population identity | noise |
| L7 | elasticities, improvement factors | interpretation, tensions |
| L8 | the chart | interpretation, prediction |
| L9 | pull-back | interpretation |
| L10 | extension $\Phi_K$ (F10) | the GGP extension |
| L11 | a maximizer of $V$ is Pareto-efficient (converse not claimed) | the GGP extension, interpretation |
| L12 | Lemma 1: facet first-order gap, $0\le f-f^*\le G$, the LP duality gap at $\tau=\infty$ (I8, F12) | three levels, level 2 |
| L13 | Lemma 2: assignment margin and explicit stable radius (I9, F12, R2) | three levels, level 3 |
| L14 | Proposition 3 and Corollary 4: assignment-stable local optimality, approximate certificate (R2) | three levels, level 3 |
