# Literature

## Introduction and how to read this page

This page places posynomial invariant form among the work it descends from and sits beside. It is a
lineage review, not a survey. Every reference was resolved against a live bibliographic record while
this page was written (see the `verified` field of each entry in `references.bib`), and every
citation below is written in the mkdocs-bibtex form, an at-sign and the bib key inside square brackets. Where a record was checked but the passage was not read, the
entry says so; the text below then claims only what the title, abstract or table of contents
supports.

Three kinds of statement appear. **Classical** means a source the method inherits a definition or a
theorem from. **Borrowed** means a construction taken over with a change of purpose. **The
supervisor's combination** means a claim about how the pieces fit together or about priority and
novelty; no source establishes these, and they are marked as such. The review does not assert that
the method is new. The last section collects what the sources do not say.

The method, in one paragraph: metrics are strictly positive and larger-is-better; their logarithms
are scored by a weighted geometric mean $V(m)=\prod_j m_j^{w_j}$ with weights $w$ on the simplex,
fitted so that the data lie on or below the surface $V=1$, using a log-mean-exp (entropic) soft
maximum of $w\cdot\log m$ over the data. Extensions replace the single monomial by a generalized
posynomial. The mathematics is in the method pages and the derivation ledger; here we only locate
it.

## Cobb-Douglas production functions and Shephard distance functions

A weighted geometric mean of inputs with exponents summing to one is the Cobb-Douglas form with
constant returns to scale, introduced as a production function in a 1928 paper
[@cobb1928theory]. The homogeneity of degree one that we impose through $\sum_j w_j = 1$ is the
constant-returns restriction of that form. This is classical, and we use the form with outputs or
attributes in place of inputs.

Shephard's distance function describes a technology by how far a bundle can be scaled toward or away
from the technology's boundary, as an alternative to a production function
[@shephard1970theory]; the multi-output treatment and its duality theory are in [@fare1995multi],
whose second chapter is titled "Distance Functions". The reading of $V$ as the factor by which a
design must be scaled to reach the frontier is a distance-function reading. That is how the
supervisor's spec uses it; the sources give the distance function, not this application. Farrell's
paper on the measurement of productive efficiency [@farrell1957measurement] is a classical
neighbour in the same tradition (the record was checked; the paper was not read).

## Deterministic and stochastic frontiers

Aigner and Chu estimated an industry production function so that observed outputs do not exceed the
function, a deterministic frontier, with estimation by mathematical programming [@aigner1968estimating]
(the record was checked; the paper itself was not read). Aigner, Lovell and Schmidt formulated
and estimated stochastic frontier production function models [@aigner1977formulation] (record only). Our fit is also a one-sided criterion, since a soft maximum penalizes
points above the surface. The relationship to stochastic frontier analysis stated in the spec
(that it describes the same geometry as a regression with one-sided error) is the supervisor's
reading. The corrected-OLS (COLS) variant named in the spec is not separately sourced; see Appendix
A.

## Data envelopment analysis, super-efficiency and Malmquist indices

Data envelopment analysis (DEA) was introduced by Charnes, Cooper and Rhodes as a linear-programming
measure of the relative efficiency of decision-making units [@charnes1978measuring]. The data's
convex hull is the limit object in the spec's hierarchy "K = 1 tangent, K-facet softmax, hull".

Closest prior art for scoring a design against the frontier of the others is DEA
super-efficiency, which ranks efficient units by allowing scores above one [@andersen1993procedure].
Malmquist indices, applied by Fare, Grosskopf, Norris and Zhang to 17 OECD countries, decompose
productivity change into technical change (a frontier shift) and efficiency change
[@fare1994productivity]. Both are prior art for the idea that a point can lie beyond a previously
estimated frontier and that the displacement is informative. The difference from this method, as the
spec states it, is parametric: here the frontier is a smooth log-linear (later posynomial) surface
fitted with a soft maximum, so that the factor $V-1$, elasticities and projections are available in
closed form. Whether that difference matters in practice is untested by any cited source.

## Entropic risk and the softened support function

The objective $J_\tau(w)=\tfrac1\tau\log \tfrac1N\sum_i \exp(\tau\, w\cdot u_i)$ is the sample version
of an entropic risk functional. Föllmer's notes define the entropic risk measure
$\rho_{H,\beta}(X)=\tfrac1\beta\log E_P[\exp(-\beta X)]$ and state that as $\beta$ increases from
0 to infinity it moves from the risk-neutral assessment (the mean) to the worst case (the essential
supremum) [@foellmer2026entropic]. Setting $X=-w\cdot u$ and $\beta=\tau$ gives our $\rho_\tau$ and
its limits: the mean as $\tau\to0$ and the essential supremum of $w\cdot u$, which is the support
function of the data's support in direction $w$, as $\tau\to\infty$. This identification is our
algebra applied to the cited definition. Ahmadi-Javid's entropic value-at-risk is a related
coherent risk measure built on the same exponential moment and relative entropy
[@ahmadijavid2012entropic]; we do not use it, and cite it to avoid confusion between the two.

That a closed convex set is determined by its support function is a standard theorem of convex
analysis [@rockafellar1970convex] (section 13 of that book is titled "Support Functions"; the text
of the section was not read). We use it to say what a softened support function over positive
directions carries.

## Log-ratio analysis and PCA

Aitchison's work on the statistical analysis of compositional data [@aitchison1986statistical]
includes principal component analysis of compositional data [@aitchison1983principal] (records
only). Egozcue and co-authors introduced isometric logratio transformations for compositional data
analysis [@egozcue2003isometric]. The method's chart $Z=Bu$, with $B$ an orthonormal basis of the
sum-zero subspace, is in the spirit of an isometric log-ratio chart (our reading of the title; the
definition was not read), and the spec calls the method "kin to"
log-ratio PCA. Two differences are the spec's, not the sources': our criterion is a one-sided soft
maximum rather than variance, and the exponents $w$ live on the simplex rather than as a contrast.

## Geometric programming and generalized posynomials

Boyd, Kim, Vandenberghe and Hassibi give the standard tutorial on geometric programming, including
posynomials and generalized posynomials [@boyd2007tutorial]. Geometric programming for aircraft design is an application of GP in the same research line
[@hoburg2014geometric] (record only). Hoburg, Kirschen
and Abbeel fit softmax-affine functions to data so that the fitted functions are compatible with GP
posynomial constraints, with max-monomial and posynomial fitting as special cases
[@hoburg2016data]; this is the source for the spec's statement that a log-sum-exp of affine terms is
GP-compatible, which is inherited axiom I4. Magnani and Boyd fit convex piecewise-linear functions to
data, and the max of affine functions is the $\kappa\to\infty$ limit of the softmax-affine form
[@magnani2009convex]. Our extension to $K>1$ terms with a shared temperature is the supervisor's
design built on these; the sources fit regression surfaces, while we fit an envelope, which the
sources do not do (the spec flags this as the reason a later package is needed).

## Kernel PCA and its disambiguation from hyperbolic PCA

Kernel PCA performs PCA in a feature space defined implicitly by a kernel [@schoelkopf1998nonlinear].
The spec's research direction, kernel expansions that stay inside the class of generalized
posynomials, takes kernel PCA as a feature-engineering kin only; no source addresses kernels
restricted to GP-compatible forms, and the support-vector analogy is a hypothesis of the spec.

The supervisor's phrase "hyperbolic PCA" refers to the hyperbolic reading in spec section 4: the
score $V$ tends to zero as any metric tends to zero, so no metric can be sacrificed entirely. This
is not PCA in negative-curvature geometry. HoroPCA extends the components of PCA (subspace
parameterization, projection and a variance objective) to data in hyperbolic space with horospherical
projections [@chami2021horopca]. The two uses of "hyperbolic" are unrelated, and the documentation
should keep them apart.

## Pareto fronts, hypervolume and tradespace exploration

Zitzler and Thiele compare multiobjective evolutionary algorithms with a strength Pareto approach
[@zitzler1999multiobjective]; the spec's seed notes cite it for hypervolume, which was not
confirmed from the abstract (record only). Ross, Hastings and co-authors describe multi-attribute tradespace exploration as a front
end to space system design [@ross2004multi]; this is the application setting for the ADCS case study
and the closest named prior art for exploring a design space by its attributes. Neither source
fits a parametric frontier of the kind used here. The spec also lists Pareto "gap" and "spacing"
metrics; no source for those was verified (Appendix A).

## Convex analysis, duality and probability foundations

The inherited axioms of the derivation ledger rest on standard theorems; their sources are listed in
Appendix B. Convex optimization duality is in [@boyd2004convex], whose section 5.2.3 treats strong
duality and Slater's condition and states a refined condition for affine constraints. Convergence of
sample means and the moment generating function of a sum of independent variables are textbook
probability [@billingsley2012probability]. The two-sided inverse of a square matrix is textbook
matrix analysis [@horn2012matrix]. For the last three the records were checked but the passages were
not read.

## scikit-learn's API and design

The estimator follows scikit-learn's conventions. The library is described in [@pedregosa2011scikit],
and the design of its API (a consistent interface across learning and processing components, which
supports composition) is in [@buitinck2013api]. The conformance requirements are in the project notes,
not in these sources.

## Framing sources

The documentation is framed by the supervisor's SciPy 2026 paper [@zargham2026derivations], which
argues that SymPy with NumPy, SciPy and matplotlib in one notebook lets scientists work in all three
of Tall's modes of mathematical learning. Tall's three worlds are set out in [@tall2013how] and, for
the transition to formal thinking, in [@tall2008transition]. Sfard's account of mathematical
conceptions as both processes and objects is [@sfard1991dual]. The glass-box principle is attributed by the supervisor's paper to Buchberger
[@buchberger1990should] (the record, titled "Should Students Learn Integration Rules?", was checked,
not the argument), and Artigue's study of instrumentation in computer algebra environments
[@artigue2002learning] supports taking the technical-conceptual relation seriously. Dubinsky and Tall
discuss advanced mathematical thinking and the computer [@dubinsky1991advanced]. These sources
motivate the presentation; they say nothing about the method itself.

## What is the supervisor's combination, and what the sources do not say

- Combining a one-sided entropic soft maximum, a simplex-constrained geometric mean, and an
  isometric log-ratio chart into one estimator is the supervisor's design. The sources establish
  each piece separately; none establishes the combination.
- Priority and novelty are not established here. Super-efficiency [@andersen1993procedure], Malmquist
  indices [@fare1994productivity], stochastic frontiers [@aigner1977formulation] and Pareto-based
  metrics [@zitzler1999multiobjective] are close neighbours that do part of the same job.
- That $V-1$ is a calibrated novelty score, that holes in $Z$ are opportunities, and that a
  surrogate regression predicts position on the frontier are claims of the spec, resting on its own
  derivations and caveats, not on the literature.
- That the single-term fit is a useful analogue of weighted-sum scalarization, and that the
  support-vector analogy holds for kernel extensions, are hypotheses.
- Theory here grounds and interprets; it does not have to match the implementation. This position is
  the supervisor's.

## Appendix A: candidates dropped or limited

| Candidate | Where it came from | Disposition and reason |
|---|---|---|
| Original source of corrected OLS (COLS) | spec section 4 lineage | Not sourced. No record for a COLS origin was resolved; the attribution "COLS (Aigner & Chu 1968...)" in the spec was not confirmed. Not cited. |
| Malmquist index original papers (Caves, Christensen, Diewert; Malmquist) | implied by the Malmquist line | Not resolved, not cited. [@fare1994productivity] is cited for its own application. |
| Pareto gap and spacing metrics | spec section 4 | No source verified. Only hypervolume is sourced [@zitzler1999multiobjective]. |
| Kolmogorov's strong law (original paper) | `derivation/axioms.py` I2 | Not resolved; the textbook [@billingsley2012probability] is used instead. |
| GPfit software documentation (gpfit.readthedocs.io) | references-verified note | Not fetched in this package; not cited. The paper [@hoburg2016data] is. |
| Föllmer and Schied on convex risk measures | considered | Not needed once Föllmer's notes were verified; not cited. |
| COLS and Greene, Winsten | considered | Searches did not resolve a source whose content was read; dropped. |

Corrections to the seed notes found while verifying (observations for the supervisor, nothing was
changed in the spec or notes):

- The Dubinsky and Tall chapter is listed there as "Tall & Dubinsky (1991)"; the Crossref record has
  Dubinsky first and dates the online record 2002.
- Magnani and Boyd is cited there as 2009 (volume 10, March 2009 print); the paper was published
  online 2008-03-25.
- The Crossref record for the Princeton reissue of Shephard misspells the author as "Shepherd"; the
  entry uses the correct spelling and says so.
- The Föllmer PDF carries the date October 15, 2026, which looks like a compile date; its year is
  recorded as unknown.
- The fourth author of Fare et al. (1994) is Zhongyang Zhang.
- Aigner-Chu, Cobb-Douglas and Fare et al. have no DOI in Crossref; their stable URLs are an EconBiz
  record, the JSTOR stable URL and the IDEAS page, as the `verified` fields say.

## Appendix B: sources for the inherited axioms

| Axiom | Statement (from `derivation/axioms.py`) | Source key |
|---|---|---|
| I1 | LP strong duality: min over the simplex of max of $w\cdot u_i$ equals the dual max-min | [@boyd2004convex] (section 5.2.3) |
| I2 | Strong law of large numbers | [@billingsley2012probability] |
| I3 | A closed convex set is determined by its support function | [@rockafellar1970convex] (section 13) |
| I4 | Softmax-affine (log-sum-exp of affine) functions are GP-compatible | [@hoburg2016data] |
| I5 | The moment generating function of a sum of independent variables is the product | [@billingsley2012probability] |
| I6 | For square $Q$, $QQ^T=I$ implies $Q^TQ=I$ | [@horn2012matrix] |

I1, I2, I3, I5 and I6 rest on textbook records whose passages were checked by table of contents or
bibliographic record only (strong duality in section 5.2.3 of the first was read in the authors' PDF).
I4 is supported by the abstract of the cited paper, which states GP compatibility for the softmax
functions of affine terms it fits; the full text is not read here.
