Cell: P5-C (persona P5, depth C); model: default (the session's default model); date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P5-C.txt

Report of reader P5-C (optimization researcher), written from the briefing alone.

1. What this is about

The paper proposes an unsupervised fit for trade-study tables. Given N designs with d strictly positive, larger-is-better metrics, it takes logs (U = log M) and looks for a weight vector w on the probability simplex that minimizes an entropic soft maximum of the projected scores w·u_i, namely J_τ(w) = (1/τ) log mean_i exp(τ w·u_i). The optimal w* defines a weighted geometric mean V(m) = Π m_j^{w_j}, scaled so that V = 1 is a soft upper support of the data (about 10 % of designs lie beyond it, by the choice of τ). The level set V = 1 is a hyperplane in log space; the exponents w_j are read as elasticities (−w_i/w_j), the support of w as the set of metrics "in tension", log V as a level coordinate, and an orthonormal zero-sum basis supplies the remaining d−1 coordinates along the hyperplane. For K > 1 the model becomes a max (κ = ∞) or a 1/κ-power of a sum (finite κ) of such monomials, fitted by a k-means-style alternation between assigning designs to their best term and refitting each term by a convex program. The whole thing is packaged as a scikit-learn transformer and exercised on a simulated cubesat with 706 feasible designs and 8 metrics, plus a planted synthetic table.

In optimization terms: K = 1 is minimization of a log-sum-exp of affine functions over the simplex (convex, smooth, essentially a Frank-Wolfe-friendly problem); K > 1 is a max-affine, one-sided fitting problem of the Magnani-Boyd type, nonconvex, attacked by block-coordinate descent.

2. The main result

As a piece of mathematics the main result is modest and, as far as the main text lets me check, correct: the one-term fit is a convex program on the simplex (Theorem 3 gives the second directional derivative as τ times a softmax-weighted variance, which is right), its KKT conditions on the simplex are stated correctly (Theorem 2), log-mean-exp sits between the mean and the max within (log N)/τ (Theorem 4), and the chart (Z, log V) is a bijection with u because w·1 = 1 (Theorem 6 plus one triangular step the text does not spell out). For several terms the paper claims exactly what a Lloyd-type scheme can claim and no more: monotone descent of the joint objective (Theorem 11), a Frank-Wolfe-type gap per term that bounds suboptimality of each convex subproblem (Lemma 1), and local optimality of the returned W inside an assignment-stable ball whose radius is set by the margin (Lemma 2, Proposition 3). Theorem 10(i) has a neat argument for nonconvexity by permutation symmetry and Jensen. Theorem 10(ii) is the Gibbs variational inequality for log-sum-exp, i.e. the soft alternation is a majorize-minimize scheme.

The empirical result is that on the cubesat, one term produces a five-metric tension at exponents 0.14 to 0.36 determined by an effective sample of about 23 designs, and three terms split it into sets of 4, 5 and 5 metrics, with control effort and peak slew power each leading a term. The paper is careful to say that mean slack falls with K by construction and that K is the analyst's choice.

My honest summary: nothing claimed as Derived appears false, but the guarantees are the guarantees of coordinate descent on a nonconvex problem, dressed accurately rather than up, and the "certificate" for the K = 3 fit of record covers perturbations smaller than 1.2e-4 in parameter norm.

3. What I would do next with it

(a) Resolve the discrepancy between equation (1) and equation (2) at K = 1. Equation (1) minimizes J_τ(w). Equation (2) with K = 1 minimizes f_1(w) = J_τ(Uw) − ū·w. These coincide only if ū·w is constant on the simplex, i.e. if the log-metrics are mean-centred (ū = c·1). J_τ is equivariant under a uniform shift (Proposition 1) but not under per-metric shifts: J_τ(w; U + 1 b^T) = J_τ(w; U) + w·b, so the minimizer of (1) depends on where the analyst places each metric's origin b_j, while f_1 does not. The text says conditioning "shifts and scales to unit log-spread" but never states that it centres. I would pin down which objective the estimator actually minimizes at K = 1 and whether ū = 0 is guaranteed by the conditioning; if not, the claimed meaning of w* ("the direction of smallest upper extent") is origin-dependent in a way Proposition 1 does not cover.

(b) Check the second-order certificate (Theorem 12) for strict complementarity. The theorem tests positive definiteness of H = D − κM on "the tangent space of the active face". For inequality constraints w_kj ≥ 0 that are active with a zero multiplier, the critical cone is strictly larger than that tangent space, and positive definiteness on the tangent space is then not sufficient for a strict local minimizer. The hypothesis list names the first-order conditions and "I16" but not strict complementarity. Either it is assumed and should be stated, or the certificate is incomplete at boundary points.

(c) Correct or clarify the direction of the geometric-programming claim. Section 5 says the one-term fit is "convex after the change of variables x = e^w". J_τ is already convex in w; in x = e^w the objective becomes a posynomial (not convex in x), and the simplex becomes a monomial equality Π x_j = e with x_j ≥ 1. The GP's convex form is the original problem in w. Section 1 says it right ("convex in the logarithmic variables"); Section 5 says it backwards.

(d) State what can be proved for free. With exact refits and finitely many partitions, the sharp alternation terminates in finitely many iterations at a partition-stable point (the standard Lloyd argument, needing only that F strictly decreases whenever the partition changes or that ties are broken consistently). The paper declines to claim convergence; finite termination is elementary and distinct from the hopeless Q1 (global convergence). Likewise Theorem 10(ii) already yields monotone descent for the soft alternation as an MM scheme, which is not stated.

(e) Test whether the n-lemma is well defined. Definition 6 takes the support of the τ = ∞ LP solution. An LP on the simplex can have a non-unique optimal face, and then the support depends on the solver (vertex versus interior-point). R1 is the right condition, but I would verify it numerically on the case (compute the optimal face, or check uniqueness by perturbation) before printing "5-lemma" as a finding.

(f) Perturb per-metric offsets b_j and scales, and report how the exponents and supports move. The paper does this for τ (Appendix D.5) but the sensitivity that matters mathematically, given (a), is to the origin of each log-metric.

4. What I would tell a colleague about it

It is a one-sided, entropic variant of max-affine fitting in log space, with the exponent vectors constrained to the simplex so the fitted monomials are homogeneous of degree one. The K = 1 problem is a clean convex program (log-sum-exp over the simplex) and everything said about it is standard and holds. The K > 1 problem is nonconvex and the paper is unusually honest about that: it offers descent, a per-term Frank-Wolfe gap, and k-means-style local optimality inside a margin ball, and says in print that global optimality, convergence and consistency are not claimed. Each result has stated hypotheses and a script. The interpretive layer (elasticities, "tensions", n-lemmas) rests on the fit touching the data's upper support in a direction that the sampling actually exercised; the authors say as much. Two things I would warn about: the K = 1 objective in Section 5 and the one implied by Section 6.2 differ unless the log-metrics are centred, and the soft-fit second-order certificate needs strict complementarity it does not state. Also, the default fit is sharp (κ = ∞), yet the only certificate theorem is for soft fits, so be careful what "certified" means for the fit of record. Expect no uncertainty quantification: the K = 1 fit of 706 designs is carried by an effective sample of 23.

5. What I think the method does not do

- It does not find the Pareto boundary; it fits a log-convex upper support of the sample, and it says so (Definition 1, Q4). Theorem 9 is only the classical sufficiency of weighted-sum scalarization in log space, which does not make any sampled near-frontier design efficient; it concerns maximizers over the attainable set.
- It gives no global optimality for K > 1 and no convergence theorem, only descent and a very local certificate; at K = 3 the stable radius is 1.2e-4 and 11 of 706 designs sit within a band of a seam.
- It is not statistical inference: no sampling distribution, no confidence on exponents, no consistency (Q2), and Proposition 2 is a population identity that does not connect to the sample LME.
- It does not choose K, τ sets the band by a 10 % convention, and the exponents and supports depend on the conditioning (origin and scale per metric); a "stable fitted direction answers that question" is the paper's own framing.
- It cannot represent non-log-convex structure (dents, holes); Φ_K is convex in u by construction.
- Discrete design variables produce step-function metrics (Figure 6, bottom; Figure 8, term 3's −1.00 association between pointing error and peak slew power), so some "tensions" are deterministic artefacts of swaps rather than continuous trade-offs; Figure 4's caption admits this in passing.
- At K > 1 the per-term evidence can be very thin: term 1 at K = 3 has 3 near-frontier designs (Figure 8), yet it is reported as a term that control effort "leads".
- Homogeneity (Theorem 1) holds in conditioned metric space only; after the pull-back the exponents w_j α_j do not sum to one and the shifts s_j break log-linearity in the attributes.

6. Where I was confused or stopped (with the passage quoted)

- "At finite τ one term is a geometric program, convex after the change of variables x=e^{w} (Appendix B, L4.14 to L4.24)". J_τ is convex in w as it stands; the change x = e^w produces the posynomial (nonconvex) form. The direction is reversed relative to "convex in the logarithmic variables" in Section 1.

- "w^*=\arg\min_{w\in\Delta}J_\tau(w)" (equation 1) against "f_k(w)=J_\tau(Uw)-\bar u_k\cdot w" and "F(W)=\sum_k\tfrac{n_k}{N}f_k(w_k)" (equation 2). At K = 1 these are different objectives unless ū is a multiple of 1. I stopped here for some time; nothing in the main text says the conditioning centres the log-metrics.

- "if the Hessian H=D-\kappa M of the soft objective is positive definite on the tangent space of the active face, the point is a strict local minimizer". Without strict complementarity the critical cone is larger than this tangent space. I could not tell whether the appendix assumes it.

- "The gradient and the Hessian agree with finite differences on an exact instance." Offered as part of a proof sketch for a result labelled Derived. Finite-difference agreement on one instance is a numerical check, not a derivation of the Hessian formula.

- "On the primary regime the solver declares the status certified at K = 2 and 3, with the largest term gap below 1e-12." and, earlier, "For a soft fit, certified means that the second-order test holds (Theorem 12)". The default fit is sharp (κ = ∞). I could not determine whether the K = 2, 3 fits of record are sharp or soft, and hence what "certified" means for them. The Discussion compounds this: "That the optimizer reached a local minimizer of the objective is the certificate (Theorem 12)", though Theorem 12 applies only at finite κ.

- "The contending set of term k is the support (exponents above 10^-9) of the exact-maximum (τ=∞) fit to the term's cell" against "Every term is fitted against every design" and "Refitting a term on its own rows is ill-posed (observed on planted data, Appendix D.13)". Is the contending set computed from an LP on the cell's rows alone (said to be ill-posed), or from f_k at τ = ∞ (soft max over all rows minus the cell mean)? The two can have different supports.

- "Derived. Hypotheses. A3; F5 (the maximum is attained)." (Theorem 4) and similar "F10", "F12" hypotheses elsewhere. For a finite set of scores, or a continuous function on the compact simplex, attainment is automatic. These read as artefacts of a symbolic script with symbolic N or d, not hypotheses the argument uses.

- "R1: the balanced point lies in the relative interior of a facet of the supporting envelope with positive normal". I do not know what "the balanced point" is; it is not defined in the main text. R1 is also stated for the τ = ∞ envelope but invoked in Theorem 2 at finite τ.

- "a maximizer of V is Pareto-efficient (Theorem 8, Theorem 9)" presented in Section 2 as where Pareto methods and the fit "meet in one result". It is the standard sufficiency of weighted-sum scalarization; no sampled design is a maximizer of V over the attainable set, so I did not see what work the theorem does for the fitted surface.

- "The planted table has 900 rows, 4 metrics and 3 planted terms." (Section 8) against "On 20 planted tables (400 rows, 4 metrics)" (Section 9) and Figure 1's "(all of it: d = 3)". Three descriptions of planted data that do not match one another; the Section 8 sentence also sits between the τ numbers and "Figure 4 shows how the temperature is selected", where it has no referent.

- "step B, unpenalized, with support offsets" in Theorem 11's hypotheses. Step B is not defined in the main text; "unpenalized" implies a penalized variant exists that is also not described.

- "At K = 3 the margin is 0.00121 and the stable radius 0.0001209". I did not stop on the arithmetic but on the consequence: the local-optimality guarantee covers a ball of radius about 1e-4 in (w, β). That is correct and honestly reported, but it makes Level 3 close to vacuous for the fit of record.

7. Terms I had to guess

- "energy differential": log V, the signed level relative to the fitted hyperplane. The text says it is an analogy with a potential; I read it simply as the residual w·u − β.
- "reach" β_k: the log-mean-exp of the scores along w_k, i.e. the soft support function value in direction w_k.
- "balanced point": I guessed either the minimizer w* or the point of tangency of the fitted hyperplane with the envelope; the text never says.
- "cell": the set of designs whose largest term score is term k (a Voronoi-like region in score space).
- "contending set" / "n-lemma": the support of the τ = ∞ exponent vector and its cardinality; I took "n-lemma" as a coined name for an n-way trade-off.
- "term share": the fraction of near-frontier designs in each cell.
- "effective sample size": I assumed the Kish quantity 1/Σ p_i² of the softmax weights p = softmax(τUw).
- "mean slack": F(W), the mean over designs of β_{k(i)} − w_{k(i)}·u_i.
- "stable radius": a Lipschitz-type bound on parameter perturbations that preserve every design's argmax term.
- "term gap": the Frank-Wolfe gap g·w − min_j g_j on the simplex, which the text does not name as such.
- "I5, I6, I8, I9, I10, I11, I12, I14, I15, I16" and "F5, F10, F12": I guessed these index imported standard facts (I) and formal attainment assumptions (F) in an appendix ledger.
- "step B": one half of the alternation, presumably the per-term refit given the assignment.
- "hyperbolic" in the title: the level sets of a weighted geometric mean are hyperbola-like surfaces in metric space; the paper confirms this is unrelated to hyperbolic geometry.
- "primary regime" / "stock regime": aggressive versus stock controller gains, two datasets from the same simulator.
- "MoE" / "MoP": measure of effectiveness / measure of performance (systems-engineering vocabulary, defined in passing).
- "soft support": the τ-smoothed support function of the data, by analogy with a supporting hyperplane.
- "participation threshold": the 1e-3 cutoff below which an exponent is displayed as white or grey.

8. Whether I would read the appendices, and why

Yes, selectively, and with specific questions rather than for general interest. Appendix B for L4 (to see which way the GP change of variables is actually taken and whether convexity is proved in w or in x), L14 and L13 (to check the local-optimality argument and the Cauchy-Schwarz constant), L16 (to see whether (ii) is indeed the Gibbs inequality and whether descent for the soft alternation falls out), and L17 (to see whether strict complementarity is assumed in the second-order certificate and whether the Hessian is derived symbolically or only checked by finite differences). Appendix B.2 for the alternation steps, to settle how β_k and the contending sets are computed and what "step B, unpenalized" means. Appendix E, the gaps ledger, because the main text promises that it records what cannot be proved and the evidence on sensitivity, which is exactly what a referee of this paper needs. Appendix D.13 and D.14 for the ill-posedness observation and the four planted failures, and D.5 for the τ sensitivity. I would also look for whether the conditioning centres the log-metrics, since the (1)-versus-(2) question depends on it, and that may be in Appendix C or F.

I would not read Appendix G (the prior-art register) or the reproducibility ledger in F, which are not where the mathematics stands or falls. If Appendix B turns out to repeat the main text's sketches at the same altitude rather than closing the arguments, I would stop there.
