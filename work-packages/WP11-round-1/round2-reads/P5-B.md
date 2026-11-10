Cell: P5-B (persona P5, depth B); model: sonnet; date: 2026-11-10
Slice commit: c6d0fff (staged build in the stage worktree, served at 127.0.0.1:8790); reader prompt: prompts/P5-B.txt

REPORT (reader P5-B: optimization researcher, working from the briefing and the nine figures only)

1. What this is about

A way to describe a trade study. Each design has several positive, larger-is-better "metrics". The paper fits a "reference surface" to the cloud of designs in log-metric space. The surface is a level set V = 1 of a weighted geometric mean of the metrics, V = prod m_j^{w_j}, with w on the simplex. The exponent w_j is read as the elasticity of metric j. The fit takes the weights that minimize a soft maximum (log-mean-exp, temperature tau) of the scores w·u over the designs. So it is a soft, simplex-constrained supporting-hyperplane fit. As tau goes to infinity it becomes an LP: minimize beta subject to w·u_i <= beta for all i. With K > 1 the surface is a log-sum-exp of K such affine pieces (a "posynomial"). The K > 1 objective is not convex, and an alternating scheme with weaker guarantees is used for it. The case study is an 8-metric cubesat trade (power, mass, attitude control).

2. The main result

For K = 1 the claims look sound to me, and I checked several of them by hand.
- Convexity: Theorem 3 gives d²/dt² J = tau·Var_p(v·u) >= 0. This is the standard log-sum-exp variance identity, stated honestly as convex and not strictly convex.
- Theorem 2 gives the simplex KKT conditions.
- Lemma 1 is the Frank-Wolfe-type gap G = g·w − min_j g_j bounding f − f*.
- Theorem 4 (LME bounds), Theorem 5 (elasticities and the improvement factor V^{-1/w_j}), Proposition 2 (Gaussian cumulant) and Theorem 8 (max_k x_k <= Phi_K <= max_k x_k + log K/kappa) all check out.

For K > 1 the paper makes three graded claims, and I think the grading is honest.
- Level 1: the objective is monotone non-increasing, with no convergence claim (Theorem 11).
- Level 2: a numerical stationarity gap, with a stable radius for the assignment (Lemma 1, Lemma 2).
- Level 3: local optimality, conditional on every term minimizing its own objective and on the assignment being stable with a strictly positive margin (Proposition 3). Global optimality is not claimed.

There is also a second-order certificate for the soft fit (Theorem 12). The empirical claim is that the multi-term fit separates "contending sets" that one term blends. For example, Figure 8 shows terms with different supports and exponents, and Figure 9 shows two regimes with different supports.

3. What I would do next

- Reproduce the K = 1 LP and the soft fit on a small instance and check Theorems 2, 3 and Lemma 1 numerically.
- Test whether the "contending set" (the support of the tau = infinity LP optimum) is stable. I would perturb or bootstrap the designs, look for non-unique LP optima, and vary the 1e-9 support threshold and the solver.
- Run the K > 1 alternation from many random restarts and see how often it reaches different local minima. The Corollary 1 bound is stated to apply only to the returned run, not across restarts.
- Check what happens to w when one metric's units or scale are changed. Proposition 1 covers only a uniform shift of all metrics, not a per-metric shift.
- Build a case where the true attainable set is not convex in log space and see what the fit does.

4. What I would tell a colleague

It is a clean convex fit (soft supporting hyperplane on the simplex) with an interpretable weight vector, plus a deliberately modest, honestly graded heuristic for the non-convex K > 1 extension. The K = 1 mathematics is textbook-correct. The K > 1 guarantees are weaker than "converges to a minimizer", and the paper says so. Anything about "contending sets" is a statement about an LP vertex support, and I would treat it carefully (see parts 5 and 6). The figures that actually check the fit are the level chart (Figure 7) and the temperature sweep (Figure 4). The slice plots (Figures 5 and 6) cannot validate the fit, as their own captions say.

5. What I think the method does not do

- It does not recover the Pareto boundary. The surface is a log-space supporting envelope, so it can only touch Pareto points on the log-convex hull. Definition 1 distinguishes these objects, but I would stress it.
- Any K, including K = 3, gives a surface that is a log-sum-exp of affine functions. Its sublevel set is therefore convex in log-metric space. The model cannot represent a log-space non-convex front.
- It gives no global optimality for K > 1. Convergence and stationarity are explicitly not claimed (Theorem 11).
- It gives no statistical guarantee. Proposition 2 is a population identity with "no consistency claim". There is no uncertainty on w, on the support, or on the choice of tau.
- It does not choose tau by principle. Figure 4 chooses the tau at which the fraction above V = 1 first meets a target of 0.1. That is a tuning rule, similar to picking a quantile level. At that tau the effective sample size is only 23 (Figure 4), so the fit is carried by a few dozen designs.
- Theorem 9 is weaker than the Section 1 sentence "a maximizer of V is Pareto-efficient". Theorem 9 gives only weak efficiency in general, and efficiency when every w_j > 0. In the fits several w_j are exactly zero (control effort, power margin, peak slew power in Figure 4).
- Conditioning of the metrics is outside the method. The minimizer w depends on how each metric is scaled and offset, because a per-column shift adds a linear term w·c to the objective. This is my own derivation, not something I saw stated.

6. Where I was confused or stopped

- Definition 2: "$V(m)=\prod_j m_j^{w_j}$ and, with the reach $\beta$ (Definition 7), $\log V=w\cdot u-\beta$." V is defined without beta, and log V is then given with it. Theorem 1 ("$V(me^{-\beta})=e^{-\beta}V(m)$, so $\log V=w\cdot u-\beta$") does not settle which object V denotes. Is u = log m or log m minus beta? Is V "the product" or "the product times e^{-beta}"?
- The objective J_tau is used throughout (Proposition 1, Theorem 2) but is never defined in what I was given. I inferred J_tau(w) = LME_tau(Uw).
- Theorem 3 and the Section 1 sentence "The one-term fit is a geometric program, convex in the logarithmic variables". Convexity in w is shown. I did not see how the simplex and w >= 0 constraints become GP constraints. I guess it is "monomial equality and inequality in e^w", which is consistent with Theorem 10 (iii) "a generalized posynomial in $e^{w}$". I would want that stated.
- Theorem 10 (i): "a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general". The step from "a convex symmetric program would have a symmetric (all-terms-equal) minimizer" to "so the actual objective is not convex" is not closed by what is stated. It needs the observation that the actual optima have unequal terms. As boxed, the inference is incomplete.
- Definition 6 and "It is found, not assumed": the contending set is "the support (exponents above 10^-9) of the exact-maximum fit". No hypothesis of a unique LP optimum is listed. LP optima can be non-unique, and the support of a vertex solution is solver- and tolerance-dependent. The figures suggest this matters.
  - Figure 9 shows power margin and energy balance associated at 0.99. In the stock regime power margin is outlined (w=0.18) and energy balance is not (w=0.02). In the primary regime the roles are reversed.
  - Pointing error and peak slew power are at -0.95 in Figure 9 (primary), and at -1.00 in Figure 8 for term 3. In term 3 pointing error is outlined and peak slew power (w=0.61) is outlined too, but in Figure 9 (primary) peak slew power is grey and not outlined.
  - So which of two near-duplicate metrics is "contending" looks arbitrary to me.
- Figure 8 title: "term 1: 4-lemma (4 metrics in the exact-maximum support)" together with "Too few near-frontier designs for an association reading: 3 of ten". An exact-maximum support of 4 metrics is reported for a term whose cell has very few near-frontier designs. Is that support meaningful, or an LP degeneracy artifact?
- Figure 8, term 3: the outlined energy balance has w=0.00 (grey), while the unoutlined power margin and depth of discharge have w=0.02. The caption says this ("an outlined metric can be grey"). It makes the relation between the tau-finite exponents and the tau-infinity support unclear.
- Theorem 11: "step B, unpenalized, with support offsets $\beta_k=J_\tau(Uw_k)$ and each refit an exact minimizer of $f_k$" and "One accepted iteration does not raise the mean slack $F$". "Step B", "unpenalized" and "accepted" are undefined here. Is J in the offset over the cell's rows or all rows? Definition 7 says "the soft maximum of their scores along it" without saying whose.
- Proposition 3: "On the assignment-stable neighbourhood, with offsets $\beta'_k=J_\tau(Uw'_k)$". Local minimality is shown for the fixed-assignment objective. I see that R2 (a strictly positive margin gamma) makes F coincide with it nearby. But "every $w_k$ minimizes $f_k$" can only hold up to numerical tolerance in practice. This is acknowledged for Theorem 12 ("not within a tolerance"). Then the certificate's hypothesis is, as far as I can tell, never exactly met by a numerical run. Corollary 1 gives an approximate version, but with a bound only on F against the fixed-assignment optimum, not on F against the true optimum.
- Theorem 12: "positive definite on the tangent space of the active face". Standard second-order sufficiency with inequality constraints w >= 0 needs the critical cone. The tangent space of the active face is enough only under strict complementarity. Strict complementarity is not among the listed hypotheses.
- Theorem 12 also has Hessian H = D − κM with D and M both PSD. That is an indefinite difference, so the certificate is a real condition, not automatic. It is not clear how often it holds in the case study, and nothing says whether it was checked there.
- Definition 4: "the near-frontier band is $|\log V|<1/\tau$ ... one inside the band weighs within a factor $e$ of one on the surface". I verified the factor-e claim from the softmax. But the cell sizes and "term share" depend on this band (Definition 7: "depends on the band"), which depends on tau, which was chosen from a target fraction. So several downstream quantities, including Figure 8's "fewer than ten near-frontier designs" rule, inherit a chosen tuning parameter.
- Figure 7: "The surface is the flat line log V = 0 ... a design above the line lies beyond the surface". A few designs sit above the line by up to about 0.05, and most designs are far below it (down to about -1.0). The caption does not say which tau and kappa produced the K = 3 fit shown. The grey band half-width looks like about 0.026, which matches 1/38.1, but that is for K = 1 in Figure 4.
- Figure 6 caption: "so a design can lie above the line here and still be inside the surface". This is correct for a slice with other metrics frozen. It means Figures 5 and 6 cannot show the fit is good. In the top panel of Figure 6 a visible cloud lies above the line at left, and a diagonal arm lies far below it. I could not tell from the figure what that structure is (the caption does not say).
- Theorem 5 and Definition 8 use k for a metric index in one and a term index in the other.
- Definition 9 is named "Ascent direction" but describes the tangent space of constant V and the gradient of log V. The name does not match the content.
- Main results: "PCA and the fit are chained ... a reading and not a result" and "Numerical: the status a fit reaches. Open: Q1 to Q4 and the search's monotonicity." I cannot see Q1 to Q4 here.
- Hypothesis labels (A1 to A8, I5 to I16, F5, F10, F12, R1, R2, L5.25) are cited but not defined in what I was given. I could judge hypotheses only by their parenthetical glosses.

7. Terms I had to guess

- n-lemma / contending set: the number or set of metrics with strictly positive exponent in the tau = infinity LP solution for a term. A corner is a "monolemma" (one metric binds), an edge a dilemma, the interior a trilemma. This is a name for the support of an LP vertex.
- reach (beta): the soft maximum of the scores w·u over designs, i.e. the intercept of the supporting surface.
- cell: the set of designs whose largest term is a given term, a hard partition of rows.
- term share: the fraction of near-frontier designs in a term's cell.
- near-frontier band: |log V| < 1/tau.
- energy differential / level / log V: signed distance below the reference surface in log units, negative inside.
- position coordinates Z: the d−1 orthonormal coordinates orthogonal to the all-ones direction, the log-scale direction removed.
- conditioned metrics: raw attributes transformed by an invertible monotone map into strictly positive, larger-is-better numbers (logarithm applied afterward).
- primary / stock regime: two settings of the controller gains, aggressive versus default.
- participation threshold: exponent at most 0.001 counts as not participating (white cells in Figure 4).
- slack: how far below the surface a design sits (nonnegative shortfall), whose mean over designs is F.
- association: the Pearson correlation of the log-metrics among near-frontier designs in a cell, descriptive and not part of the model.
- effective sample size n_eff: I took it as 1/sum p_i² for the softmax weights p, i.e. how many designs actually carry the fit at that tau.
- kappa: the term temperature, controlling how sharply the K terms meet.

8. Whether I would go on to read the whole paper

Yes, though selectively. The K = 1 part has statements I could check and found correct, and it is the kind of soft-LP-on-a-simplex object I know how to evaluate. I would read the proofs of Theorems 2, 3 and 8 only to confirm the hypotheses used. I would read Theorems 10 to 12 and Proposition 3 closely, because that is where the gap risk lies: the "not convex in the terms" argument, the exact-hypothesis requirement of the certificate, and the missing strict complementarity. I would also want to see how the contending-set support is computed, and whether any uniqueness or tolerance handling is documented, since the figures suggest the support is fragile when metrics are nearly collinear. I would skim the cubesat model material (Figures 2 and 3). Stated reason: the mathematics is stated with its hypotheses and its limits more openly than most papers I read, so it is worth the time. My open concerns are about robustness, not about stated results being false.
