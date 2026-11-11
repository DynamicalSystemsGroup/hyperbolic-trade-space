# sect-results

## Q1. What the section conveys

It states, with hypotheses, a sketch and a script for each, the results the method rests on. For the one-term fit: homogeneity, convexity, the optimality conditions, elasticities and the reversible chart. For the posynomial extension: Pareto efficiency of a maximizer. For the several-term fit, which is not convex: three levels of guarantee and a soft-fit certificate. It then gives the measured termination status on the case and lists four open questions.

## Q2. Which sentence of the story it serves

Main results 1, 2, 3, 4 and 6. Item 1 cites Theorem 1, item 2 cites Theorems 2, 3, 5 and 6, item 3 cites Theorems 8 and 9, item 4 cites Theorems 10 to 12, Lemmas 1 and 2 and Proposition 3, and item 6 is the "Numerical" paragraph and the open questions Q1 to Q4. In the abstract it backs "transforms into a convex program and is solved directly", "with elasticities" and "a reversible chart".

## Q3. Verdict

advances. Section 1 names Section 6 as the home of main results 1 to 4 and 6, and no other unit is named as carrying the boxed statements; the appendices hold the full proofs, not the statements the story points to. Without this section, the story's claims of convexity, global minimizers, elasticities, reversibility, Pareto efficiency and the levels of guarantee would have nothing on the page to stand on.

## Q4. If "repeats"

Not applicable.

## Q6. Boxed statements

- Theorem 1 (Homogeneity and the invariant form (L1)): advances. Main result 1; it is what makes "a weighted geometric mean that doubles when every metric doubles" true.
- Proposition 1 (Uniform shift (L2)): does not advance. No story sentence asks for it; it supports the offset's meaning and the shift property used in Theorem 8.
- Theorem 2 (Gradient and the simplex KKT conditions (L3)): advances. Main result 2.
- Theorem 3 (Convexity of the fit (L4)): advances. Main result 2 ("every minimizer is global").
- Theorem 4 (Log-mean-exp against log-sum-exp (L5)): does not advance. No story sentence cites it; it supports the squeeze that Theorem 8 reuses and the project's choice of the log-mean-exp.
- Proposition 2 (Gaussian cumulant (L6)): does not advance. The story mentions noise only as something a method must handle; this population identity is not cited and is not used by any later box in the section.
- Theorem 5 (Elasticities and improvement factors (L7)): advances. Main result 2 and the abstract's "elasticities".
- Theorem 6 (The chart (L8)): advances. Main result 2 ("its chart is reversible") and the abstract's "reversible chart".
- Theorem 7 (Pull-back to attributes (L9)): does not advance. No story sentence asks to read the result back in attributes. The nearest is "a configuration is evaluated into attributes whose trade-offs the fit reads", which does not need it.
- Theorem 8 (The posynomial extension (L10)): advances. Main result 3 and the abstract's GGP compatibility.
- Theorem 9 (A maximizer of V is Pareto-efficient (L11)): advances. Main result 3.
- Theorem 10 (Soft-weight alternation (L16)): advances. Main result 4 ("not convex in the terms").
- Theorem 11 (Level 1, descent (L15)): advances. Main result 4, first level.
- Lemma 1 (Level 2, numerical stationarity: the term gap (L12)): advances. Main result 4, second level.
- Lemma 2 (Assignment margin and stable radius (L13)): advances. Main result 4; it is the tool for the third level, and the case's stable radius comes from it.
- Proposition 3 (Level 3, conditional local optimality (L14)): advances. Main result 4, third level.
- Corollary 1 (Approximate certificate (L14)): advances. Item 4 does not cite it by name, but the stopping declaration ("certified" for a sharp fit) invokes it, and item 4 names the stopping declaration.
- Theorem 12 (Soft-fit certificate (L17)): advances. Main result 4 ("a soft fit has a second-order certificate").

## Q9. Read twice and still could not place

- "Refitting a term on its own rows alone ... is ill-posed" next to Theorem 11's hypothesis "step B, the refit of each term on its cell": I could not tell whether step B is the ill-posed plain fit or $f_k$, or what "$f_k$ itself on the cell's rows" means when the text says "the refit of record is $f_k$ over all rows".
- "R1 is a statement about the exact-maximum ($\tau=\infty$) geometry; it does not imply that the finite-$\tau$ minimizer is interior", next to the hypothesis "R1's relation at the fit temperature". Read together, these leave unclear whether the facet-normal reading holds at the fit's $\tau$.
- "at $K>1$, $\kappa=\infty$, through an active term" (Theorem 9): too compressed to tell what is claimed at $K>1$.
- "for a soft fit ... stationary that the term gaps hold and the curvature is not positive": the term gaps are defined for the sharp, per-term $f_k$, and I could not place what they mean for a soft fit.
- Main result 3, "With one term the posynomial extension is the monomial": the section gives this as the formula $\Phi_1=w_1\cdot u-\beta_1$ inside Theorem 8. The sentence is fine, but at first I could not find where it is stated.
