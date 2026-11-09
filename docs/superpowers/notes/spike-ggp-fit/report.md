# Research sprint: the model, the fit and the analysis of the several-term case

Date 2026-11-09. Driver's spike on the supervisor's direction (`work-packages/WP10-decisions.md`):
"i don't think each config needs to be in a unique facet. i think you may be getting confused
between the fitting and the analysis. fitting a model and interpreting it are different. any config
is likely to have a projection onto each facet but analysis tells us which dominates."

Scripts: `check_fit.py` (run in a clean checkout at a17ecf6; planted tables A, 900 x 3, and B,
400 x 4, three terms, temperature 50). Source read: Boyd, Kim, Vandenberghe and Hassibi 2007,
sections 5.3, 5.4, 8.3 to 8.5 and 9.1.

## Verdict

He is right on both counts, and the driver's question to him was wrongly framed.

1. **A design does not need a unique facet in the fit.** In the code as it stands every facet is
   already fitted against every design. A fit that gives each design a weight on every term recovers
   the planted exponents as well as the one that gives it a single label.
2. **The driver had put an analysis step inside the description of the fit.** "Assigning designs to
   facets" is the analysis of the current model. The fit only needs, for each term, weights saying
   which designs that term should be tight against.
3. **On "the resulting program is a GGP":** exactly true once those weights are given; not true of
   the unsupervised problem as one program in the sense of the source the paper cites; true of it in
   an older sense of the same words. Details below.

## The three things, apart

| | What it is | Does a design belong to one facet? |
|---|---|---|
| Model | `Phi(u) = (1/kappa) log sum_k exp(kappa (w_k . u - beta_k))`; a posynomial to the power 1/kappa; the maximum of the terms at kappa = inf | No. Every design has a score under every term |
| Fit | choose the exponents `w_k`; each offset is `beta_k = J_tau(U w_k)`, the soft support over all designs; the objective is the mean slack `F = -mean_i Phi(u_i)` | No. See findings 1 and 4 |
| Analysis | for a design, the term with the largest score dominates; the contending set, the elasticities and the facet shares are read from that | Yes, by definition of "dominates", ties aside |

## Findings

**1. Every design constrains every facet (in the code today).** The offset of each facet is the
log-mean-exp over all rows (difference from the code's value: 0). Computed over the facet's own rows
it would sit 0.016 to 0.029 lower. Between 2 and 7 percent of each facet's support weight is carried
by designs that another facet dominates. Every design has a slack under every facet; 73 of 900
(A) and 25 of 400 (B) lie within 0.05 of two or more facets.

**2. As one program in the log variables, the several-term fit is not convex.** Take the fit and
the same fit with two terms renamed: the same model, the same F. At the midpoint of the two in the
log variables F rises by 0.18 (A) and 0.14 (B); a convex objective cannot rise there. The general
reason is symmetry: a program that is convex in the terms and treats them alike keeps, among its
optima, the point where all terms are equal, which is a one-term model (F at that point: 0.889
against 0.631 for the fit on A; 0.854 against 0.664 on B). So no formulation that is convex in the
terms and symmetric in them can return distinct facets as its only answer. What breaks the symmetry
is the weights.

**3. With the weights given, fitting all terms is one generalized geometric program.** For weights
`A` (N by K), the objective is `sum_k (n_k/N) [J_tau(U w_k) - ubar_k . w_k]` with `ubar_k` the
weighted mean log metric. Convexity: 0 violations in 2000 random pairs. In `x = exp(w)` its
exponential is a product of positive powers of posynomials and monomials, a generalized posynomial
(relative gap 2e-16), under monomial constraints: a GGP in the sense of the tutorial's section 5.4.
This program bounds the fit's objective from above for every W and touches it at the model the
weights came from (largest excess 0.0e+00; gap at the anchor 2e-16). The bound is the
arithmetic-geometric mean inequality applied to the sum over terms, the monomial approximation of
the tutorial's section 9.1.

**4. A fit with no unique facet per design works.** Weights `softmax_k(kappa x_ik)` from the
current model, then the program of finding 3, repeated. The objective fell at every step in every
run.

| kappa | max exponent error vs planted, A | B | designs whose largest weight is below 0.9, A | B |
|---|---|---|---|---|
| 5 | 0.459 | 0.229 | 727 of 900 | 339 of 400 |
| 20 | 0.0130 | 0.0111 | 232 | 129 |
| 50 | 0.0129 | 0.0071 | 100 | 48 |
| 200 | 0.0130 | 0.0078 | 25 | 9 |
| inf (one label each; the package today) | 0.0132 | 0.0086 | 0 | 0 |

At kappa = 20 a quarter to a third of the designs carry real weight on more than one term and the
planted exponents are recovered to the same accuracy. Very soft weights (kappa = 5) blur the facets.
The single label is the limit kappa = inf of this scheme, a choice of the implementation and not of
the method.

**5. The sources.** The tutorial treats the one-term fit as the simple case, and says of the
K-term fits that they are local: "the final posynomial approximation obtained can depend on the
initial one" (section 8.5; section 8.4 says the same of the max-monomial fit). Section 9.1 describes
programs of GP form that are not GPs, solved by a sequence of GPs from monomial approximations,
local. It also notes that some authors use "generalized geometric program" for that wider,
non-convex class. So the sentence "the resulting program is a generalized geometric program" is
true in that usage and false in the usage of the source the paper cites; which usage the glossary
adopts decides it.

## What the driver got wrong

- The abstract and section 6 described the fit as "assigning designs to facets", and section 6 gives
  that as the reason the fit is not convex ("the assignment ... is combinatorial"). The reason is
  finding 2 (the objective in the terms, by symmetry), which holds with soft weights and no
  assignment at all.
- The question put to the supervisor offered wordings before the mathematics had been looked at
  from his side.

## What would align the paper with this (proposals, nothing changed)

1. **Abstract** (he has agreed the wording "GGP compatible"): one n-lemma is a monomial, fitted by
   a convex program solved directly; several trade-offs active at once are a posynomial, compatible
   with generalized geometric programming; kernels that keep that compatibility are the extension.
2. **Section 6:** state the fit without membership. The objective; why it is not convex in the terms
   (symmetry); the alternation as "weights from the current model, then one GGP for all terms";
   the single label named as the limit the package uses. Move "which facet dominates" to the
   analysis.
3. **Glossary:** "generalized geometric program" in the tutorial's sense, with the older sense in
   its `not` field.
4. **Derivations (three short scripted steps):** the symmetric optimum of a symmetric convex
   program; the arithmetic-geometric mean bound and its tightness; the fixed-weight program as a
   generalized posynomial in exp(w).
5. **Code (a decision for him):** the term temperature kappa is used today to evaluate the model
   and not to fit it. Fitting with weights at the same kappa would make the fit minimize the slack
   of the model it reports. It changes fitted numbers slightly, so it is a package of its own.

## A separate finding, for his judgment

The several-term refit minimizes the mean slack, `J_tau(U w) - ubar . w`. The one-term fit minimizes
the level, `J_tau(U w)`. They are different objectives: on the planted tables their one-term
answers differ by 0.046 (A) and 0.020 (B) in an exponent. They also behave differently under a
change of one metric's units: multiplying metric 1 by ten moves the one-term exponents by up to
0.036 and leaves the three-term exponents unchanged (0.0). The dependence of the one-term fit on
per-metric scale is documented as the reason conditioning matters. That the several-term fit does
not share it, and that the several-term objective at K = 1 is not the one-term objective, is not
stated anywhere the driver could find; the paper's sentence that the extension "reduces to the
one-facet fit" is true of the model and not of the objective.
