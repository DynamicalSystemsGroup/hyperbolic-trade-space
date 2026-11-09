# Scaling Decision Analysis with Hyperbolic Trade Space Identification

(What a reader who skims sees: the section headings, the paper's own list of main results, the boxed statements with their proofs withheld, and the figure and table captions. Mathematics is shown as it reads aloud.)

## Section headings

- Abstract
- 1 The decision problem
- 2 Prior art, by family
- 3 Preliminaries and notation
- 4 Definitions
- 5 Methods
- 6 Results
  - 6.1 The fit and its geometry
  - 6.2 The algorithm for several facets
  - 6.3 Open questions
- 7 Search of the design space (preliminary)
- 8 Case construction
- 9 Case analysis
- 10 Discussion
- 11 Reproducibility and your own case
- 12 Future work and final remark
- 13 Acknowledgments and process
- 14 Works cited

## Main results (as the paper lists them)

Main results (Section 6; each has hypotheses, a sketch and a script). The fitted reference surface is the unit level set of a degree-one weighted geometric mean, not the Pareto boundary (Theorem 1). The one-facet fit is a geometric program, convex in the logarithmic variables (Theorem 2, Theorem 3); its exponents are elasticities and its chart is reversible (Theorem 5, Theorem 6). With one term the posynomial extension is the monomial, and a maximizer of V is Pareto-efficient (Theorem 8, Theorem 9). The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration (Theorem 10, Theorem 11, Lemma 1, Lemma 2, Proposition 3); a soft fit has a second-order certificate (Theorem 12). Numerical: the status a fit reaches. Open: Q1 to Q4 and the search's monotonicity. On a cubesat model coupling power, mass and attitude control the facets separate contending sets that one facet blends (Section 9). Organization. Appendices: A notation, B proofs, C model, D results, E assumptions, F reproducibility, G prior art.

Section 2 opens: We claim no priority. Table 1 says what each family produces, what we share, how we differ and where to read it. Appendix G is the larger register; it is not exhaustive and says for every entry what this work does differently, extends or adds.

## Statements (definitions, theorems, lemmas, propositions; proofs withheld)

- Definition 1 (Three objects): The fitted reference surface is V=1 at finite τ, where the posynomial equals one; some designs lie beyond it. The supporting envelope is the τ=∞ fit, which none exceeds. The Pareto boundary is the nondominated set of the attainable set, a property of the system.
- Definition 2 (Invariant form): For w∈Δ, V(m)=∏_j m_j^{w_j} and, with a fitted offset β, log V = w·u − β. By analogy with a potential, designs of equal V stand at the same level, and log V, the energy differential, is a design's level relative to the reference surface V=1: negative inside, positive beyond. A difference of levels is the same along every path between two designs. It is neither a physical energy nor a Euclidean distance. Where several trade-offs are active at once, the model is a sum of such terms, one per facet.
- Definition 3 (Posynomial): V_K(m) = (Σ_{k=1}^K c_k ∏_j m_j^{κ w_kj})^{1/κ} with w_k ∈ Δ and c_k = e^{−κ β_k} is the 1/κ power of a posynomial, a sum of monomials (Theorem 8); Φ_K(u) = (1/κ) log Σ_k e^{κ(w_k·u − β_k)} is its logarithm. Two temperatures say how soft each maximum is, over designs and over facets; at infinity each is exact.
- Definition 4 (Temperatures and band): The fit temperature τ>0 sets how hard the maximum is (τ=∞ is exact); the term temperature κ>0 how sharply facets meet. The near-frontier band is |log V| < 1/τ: in the soft maximum a design inside it weighs within a factor e of one on the surface. The chart separates where a design sits along the surface from its energy differential, how far it is from the surface in levels and not in Euclidean distance.
- Definition 5 (The chart): Z = Bu, with B Bᵀ = I and B1 = 0, is the position along the frontier, free of overall scale. (Z, log V) is the chart, a reversible rewriting of the metrics; log V is the energy differential (level offset): the level of a potential relative to the reference surface, negative inside, positive beyond.
- Definition 6 (The n-lemma): The contending set of facet k is the support (exponents above 1e-9) of the exact-maximum (τ=∞) fit to the facet's rows; its size n_k names it. It is found, not assumed. Working-temperature exponents grade the members, and a member can carry a small one.
- Definition 7 (Reach and share): The reach β_k is the support value of the data in direction w_k. The facet share is the fraction of near-frontier designs that facet k dominates; it shows which facets carry most of the frontier and depends on the band.
- Definition 8 (Elasticity): Along facet k, d log m_j / d log m_i = −w_ki / w_kj, the percent change of j per percent change of i.
- Definition 9 (Ascent direction): On facet k the tangent space {v : w_k·v = 0} trades contending metrics at constant V; the normal w_k is the gradient of log V.
- Theorem 1 (Homogeneity and the invariant form, L1). Derived. Hypotheses: A1 (metrics positive), A2 (exponents on the simplex). For k>0: V(km) = k V(m) and V(m / V(m)) = 1; V(m e^{−β}) = e^{−β} V(m), so log V = w·u − β.
- Proposition 1 (Uniform shift, L2). Derived. Hypotheses: A1, A2, A3; w∈Δ. J_τ(w; U + c 1ᵀ) = J_τ(w; U) + c: β moves by c and w* is unchanged.
- Theorem 2 (Gradient and the simplex KKT conditions, L3). Derived. Hypotheses: A2; R1 for the facet-normal reading; w minimizes J_τ on Δ. ∇J_τ = Uᵀ p, p = softmax(τ U w). With g = ∇J_τ(w), λ = w·g: g_j ≥ λ and w_j (g_j − λ) = 0. Balanced hard-support geometry does not imply an interior minimizer at finite τ.
- Theorem 3 (Convexity of the fit, L4). Derived. Hypotheses: A1, A3. d²/dt² J_τ(w + t v) at 0 = τ Var_p(v·u) ≥ 0: J_τ is convex, not claimed strictly.
- Theorem 4 (Log-mean-exp against log-sum-exp, L5). Derived. Hypotheses: A3; F5 (the maximum is attained). LSE_τ = LME_τ + (log N)/τ; mean ≤ LME_τ ≤ max_i s_i and LME_τ ≥ max_i s_i − (log N)/τ; the mean and the maximum are the limits.
- Proposition 2 (Gaussian cumulant, L6). Derived. Hypotheses: A2, A3, A5, I5 (moment generating functions multiply); a population identity, with no consistency claim. (1/τ) log E e^{τ w·ε} = τ σ² ‖w‖² / 2.
- Theorem 5 (Elasticities and improvement factors, L7). Derived. Hypotheses: A1, A2; w_j ≠ 0; the frontier is the hyperplane {w·u = β}. On it d log m_j / d log m_k = −w_k / w_j. Improving metric j alone by V^{−1/w_j}, or every metric by 1/V, reaches V=1.
- Theorem 6 (The chart, L8). Derived. Hypotheses: A7; I6 (Q Qᵀ = I implies Qᵀ Q = I). Z(u + c1) = Z(u) and u = Bᵀ Z + (1/d)(1ᵀ u) 1: the map between u and (position, log-scale) is a bijection, and Q = [B; 1ᵀ/√d] is orthogonal.
- Theorem 7 (Pull-back to attributes, L9). Derived. Hypotheses: A2, A4: log m_j = α_j log(a_j + s_j) + b_j, α_j ≠ 0. V = e^{w·b − β} ∏_j (a_j + s_j)^{w_j α_j}, and conditioning is invertible; negative w_j α_j marks a cost attribute.
- Theorem 8 (The posynomial extension, L10). Derived. Hypotheses: A1, A6; F10 (the maximum is attained) for the limit. Φ_K(u + c1) = Φ_K(u) + c; Φ_1 = w_1·u − β_1; max_k x_k ≤ Φ_K ≤ max_k x_k + (log K)/κ with x_k = w_k·u − β_k; e^{κ Φ_K} is a posynomial in m.
- Theorem 9 (A maximizer of V is Pareto-efficient, L11). Derived. Hypotheses: A2. The converse is not claimed. A maximizer of V is weakly efficient in all d metrics, and efficient when every w_j > 0; at K>1, κ=∞, through an active term.
- Theorem 10 (Soft-weight alternation, L16). Derived. Hypotheses: A1, A2, A3, A6; I14 (Jensen); I15 (generalized posynomial). With weights α_ik = softmax_k(κ s_ik) from the current model: (i) a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general; (ii) the soft model's slack is bounded above by the fixed-weight objective, with equality at the weights' own model; (iii) the fixed-weight objective is a generalized posynomial in e^w.
- Theorem 11 (Level 1, descent, L15). Derived. Hypotheses: A8 (a partition into nonempty cells); F12 (the minimum is attained); step B, unpenalized, with support offsets β_k = J_τ(U w_k) and each refit an exact minimizer of f_k. One accepted iteration does not raise the mean slack F: reassigning each row to its maximizing facet lowers or keeps F, and refitting each facet on the new cells does likewise. Convergence and stationarity are not claimed.
- Lemma 1 (Level 2, numerical stationarity: the facet gap, L12). Derived. Hypotheses: A2; the first-order convexity inequality I8; F12 for symbolic d; f_k convex by Theorem 3. With g = ∇f_k(w), the facet gap is G_k(w) = g·w − min_j g_j = Σ_j w_j (g_j − min_l g_l) ≥ 0, and 0 ≤ f_k(w) − f_k* ≤ G_k(w). G_k = 0 exactly when the simplex KKT conditions of Theorem 2 hold. At τ=∞, with the LP duals, G_k is the LP duality gap.
- Lemma 2 (Assignment margin and stable radius, L13). Derived. Hypotheses: R2 (γ>0); F12; I9 (Cauchy-Schwarz). If every facet score changes by at most δ with 2δ < γ, each row's maximizing facet is unchanged and unique. This holds whenever every (w_k, β_k) moves by less than the stable radius r = γ / (2 max_i ‖(u_i, −1)‖₂), sufficient; tightness is not claimed.
- Proposition 3 (Level 3, conditional local optimality, L14). Derived. Hypotheses: A8; R2; every w_k minimizes f_k over Δ. On the assignment-stable neighbourhood, with offsets β'_k = J_τ(U w'_k), F(W') − F(W) = Σ_k (n_k/N)(f_k(w'_k) − f_k(w_k)) ≥ 0, so W is a local minimizer of the mean slack. Global optimality is not claimed.
- Theorem 12 (Soft-fit certificate, L17). Derived. Hypotheses: A1, A2, A3, A6; I16 (second-order sufficient conditions); finite τ and κ; the first-order conditions hold exactly at the point, not within a tolerance. At a feasible point of the soft-weight fit where the first-order (KKT) conditions hold, if the Hessian H = D − κM of the soft objective is positive definite on the tangent space of the active face, the point is a strict local minimizer; D and M are both positive semidefinite, D the weighted within-term curvature and κM the designs' ambiguity between terms.

## Figures and tables (captions)

- Table 1: The families of prior art closest to this work: what each produces, what it shares with this work, how this work differs, and the sources.
- Figure 1: The K = 1 fit across temperatures on the primary regime. Top left: the fraction of designs above V = 1 against the temperature tau, with the target fraction as a horizontal line. Top right: the effective sample size. Bottom: the exponent of each metric. The vertical bar marks the temperature selected.
- Figure 2: Log-metric planes of the K = 1 fit (primary regime), one per pair of the facet's largest exponents, with the near-frontier band.
- Figure 3: Log-metric planes of the K = 3 fit with the near-frontier band; designs coloured by facet, lines the facets.
- Figure 4: The chart of the K = 3 fit: the first three position coordinates, coloured by facet, near-frontier designs outlined.
- Figure 5: Association among the near-frontier designs of each K = 3 facet (negative: tension). Outlined: the contending set, the support of the exact-maximum fit; w is the fitted exponent, small for some members.
- Figure 6: The two regimes: association among near-frontier designs at K = 1, primary above, stock below; outlined: the contending set.
- Figure 7: Predicted (open circles) and measured (diamonds) chart position of each proposed design.
