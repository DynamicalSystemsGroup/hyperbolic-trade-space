# sect-future

## Q1. What does this section convey?

It lists the directions the authors leave open, each paired with an assumption the paper made (one term, sharp weights, the analyst's choice of K, small K, log-affine conditioning, continuous variables, a log-convex envelope, illustrative hardware values, the search, Q1 to Q4, other lifecycle cases), and closes with a speculative idea: scoring a new technology by how far above V = 1 it is forecast to sit.

## Q2. Which sentence of the story does it serve?

None directly. The nearest are main-results item 6 ("Open: Q1 to Q4 ... and the monotonicity of the search (Section 7)") and the abstract's "any kernel that keeps that compatibility generalizes the method", but the story places both elsewhere: item 6 names Section 6 and Section 7 for the open questions, and the kernel sentence is a claim about the method, not a promise of future work.

## Q3. Verdict

does not advance.

No sentence of the story needs a future-work list. The pieces that touch the story (Q1 to Q4, the search's convergence, GGP-compatible kernels) are already pointed to Section 6 and Section 7 by item 6, so this section only restates them as open, and the rest (selection rules for K, discrete variables, datasheet values, dents and holes, configuration management of a fielded system) are new directions that no story sentence asks for. The final remark is labelled by the authors themselves as "not a result".

## Q4. If "repeats"

Not my verdict. For the open questions alone (Q1 to Q4 and the search's convergence), Section 6 Results (unit sect-results) and Section 7 Search of the design space (unit sect-search) already carry them, according to main-results item 6. The list of assumptions it walks through appears to be the one Appendix E (unit appendix-e) names; I have not read that unit.

## Q6. Boxed statements

none

## Q9. Read twice and still could not place

- "Beyond one term, K > 1 is built": if K > 1 is already built, I cannot tell what the future work in this item is; the sentence states a present fact where the others state a gap.
- "beyond sharp weights with smoothing on request, a nonsmooth search on the tangent cones of the ridges, whose generalized gradient is the convex hull of the active normals": "sharp weights", "smoothing on request" and "ridges" are not defined in the story, and I cannot tell what object has the kinks or which search would tolerate them.
- "GGP-compatible kernels, the generalization the search motivates": I cannot tell how the search motivates kernels; the abstract presents kernels as already generalizing the method.
- "Beyond a log-convex envelope, the detection of dents and holes": the story does not say the surface is a log-convex envelope, or what a dent or hole would be.
- "how far above $V=1$ it is forecast to sit": the story defines the surface as where the invariant value equals one and names V only in item 3 ("a maximizer of V"); it does not say that V and the invariant value are the same quantity, so I could not be sure what "above V = 1" means here. The $V=1$ also appears as raw LaTeX source on the page, not rendered.
