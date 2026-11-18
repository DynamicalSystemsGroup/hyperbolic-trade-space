# Third paper unit: the record defects, each settled from the record before the sentence was edited

Requests 93 to 165 of `triage/wave-5.md` to `wave-7.md`. Each entry says what the record shows, where, and what the
sentence now says. A sentence the record does not back is narrowed or dropped; none is given a caveat.

**136 (Theorem 10 (ii), the bound).** `derivation/lemma_16_soft_fit_alternation.py`, step L16.43 (verify): the mean of the
nonnegative Jensen slacks gives `F <= G_alpha - E`, with `E = (1/(kappa N)) sum_i H_i`, the mean entropy of the weights over
kappa, constant in W; L16.41: equality at the weights' own model. The docstring's "F(W) <= G_alpha(W)" is the weaker bound
(E is nonnegative) and the equality needs E. The statement now carries `G_alpha`, `E` and `F <= G_alpha - E`. The script's
docstring says "G_alpha less the constant E" in one place and "F <= G_alpha" in another (derivation is not this unit's file;
for the supervisor).

**97 (Theorem 10 (i)).** L16.34 to L16.37: the average of the K cyclic shifts of W is the all-equal point (L16.34); a convex
symmetric F is at most F(W) there (L16.35); the exact instance has F(all-equal) - F(W) above 0.004 (L16.37). So one symmetric
point, the shift average of this W, shows non-convexity; the minimum over all symmetric points is not needed. The reader's
objection (G05) does not hold; the statement now names the point.

**98, 139 (Theorem 11, the finite stop).** L15.17 to L15.22: a repeated partition pins both drops to zero; with unique term
minimizers (H1) and a fixed tie rule (H2) the refit returns the same exponents and the next assignment is the same, so the
loop stops; the partitions before the stop are pairwise distinct and there are K^N, so at most K^N + 1 iterations. The
docstring says K^N is a count and not a rate. D.14's text records fits "at the iteration cap, depending on the platform"
with the term gap below `tol` in 40 of 40: cited in the statement.

**99, 118 (Corollary 1).** L20 step 1: `J^R = J_tau + (tau/2) w'Sigma w` exactly, row by row; "the rows need not be
independent". The wave-5 note says L20 imports A10; it does not: `AXIOMS_USED = ["A1", "A3", "A5", "A9", "I9", "I18", "R3"]`,
and A10 is L18's (a multiplicative attribute error mapped to the conditioned noise). So the statement says A10 is not used
and what it is for; Section 3's list now names it. The expectation inside the logarithm is `J^R`, "the logarithm of the
expectation of the noisy sum, not the expectation of the logarithm" (docstring). The shift is `delta`, so the simplex's
Delta is free; P is the projector onto the face's tangent space (L20.55).

**107, 108, 109, 110 (Theorems 6 to 9).** L8 holds for any B with `B B^T = I`, `B 1 = 0` (the Helmert basis is a
realization); L10.8 (shift equivariance) gives the K > 1 clause of Theorem 6 in one line; L9's route is the exponential of a
sum, the intercepts giving `w.b`; L10.18 and L10.19 give the maximum at kappa = infinity as the maximum of monomials (I15
admits it); L11's step 5 uses a term active at the maximizer.

**135 (Definition 6 against D.13).** D.13 compares two fits with the true labels given: the plain K = 1 fit on the cell's rows
as they are (`solve_slsqp(mine, tau)`), which recovers 0 of 60 planted terms (largest error 0.97 at the exact maximum), and
the fit of all rows with the log-metrics centred at the cell's mean (the refit of record), 60 of 60 (0.001; 0.037 at
tau = 50). The contending set is a third fit (the cell's rows alone, centred on their own mean, tau = infinity) that D.13
does not test. The sentence now gives the two counts, drops "ill-posed" (the problem is convex and has minimizers) and says
what the third fit is, without a claim about its recovery. D.13's column "Support refit" is now "All-rows refit", since
"support" means three things (request 124).

**137 (R1 on both regimes).** The only check in the record is `test_the_regimes_contending_set_is_the_unique_lp_optimum_not_a_solver_choice`:
reduced costs vanish on the support and are positive off it, the tight rows carry the dual weights, the active system has
full column rank, both HiGHS methods agree. That is uniqueness of the K = 1 exact-maximum optimum. R1 itself needs the
balanced point in the relative interior of a facet of the hull with a positive normal, which cannot hold with zero exponents
(the case has a 7-lemma and an 8-lemma in 13 metrics) and which L3.9 and L7 take as a hypothesis. Narrowed: the sentence
says the optimum is one point, so the support is not the solver's choice.

**142 (D.19 against Section 9).** The 548 / 11 / 1 are over all designs passing the six requirements: 11 are nondominated
among the 548, 1 of the 11 is in the band. The shortlist's 28 are the 548 inside the band of both fits, and nondominance
among the 28 alone gives 5 on pointing error and fleet cost (8 with unit cost). Two sets; the sentence says so with both
counts, generated from `decision()`. The earlier "well inside the frontier" clause, which no record backed, is gone.

**143 (Appendix E against D).** The unit-1 regeneration (747fb01) left four stale statements in
`docs/superpowers/notes/abstraction-gaps.md`: G-7 and G-13 said "17/20 at tau = infinity" (D.14: 16 of 20 at both
temperatures, failing seeds 1, 3, 8 and 16); G-7 gave the true-label error as "median 0.018, max 0.035 at tau = infinity"
(D.13: 0.001 at infinity, 0.037 at 50); G-17 said "346 of the 817 quantities" where D.11 says 345 numbers move. The
sensitivity record has 346 quantities not identical, 345 of them numbers and one a generated sentence (the certificate's);
259 of the numbers move by more than 1e-12. G-17 says so. G-14 said "seed 8 passes at 5" restarts, which D.14 (seed 8 not
recovered at the default five) contradicts; the clause is dropped. G-9's tau, band and fraction columns match D.1 and D.2.
A test pins the E rows to D's numbers.

**138 (the polish).** `solvers.py`: `POLISH_STEPS = 5` reduced-Newton steps after each finite-tau term refit
(`_newton_polish`), a joint Newton polish after the soft alternation (`_soft_polish`, 30 steps); G-16: "SLSQP alone left
4.7e-5 at tau = 50, none of 60 terms certified at 1e-8". B.2 and the stopping declaration say it, and that the status is at
the polished point and the guarantees at the exact minimizers.

**148 (L19).** No derivation file imports `L19_RESULT` and no paper table names an L19 step. B.2 says it bounds the noise
shift of the offset and no result of the paper uses it.

**165 (dropped).** G09 reads the unit-cost against fleet-cost association as -0.44 and +0.56. Figure 7 prints -0.44 (term 1)
and -0.56 (term 2): both negative. There is no sign change to explain.

**94 (alt text).** Set from the caption's first sentence where the notebook is executed.
