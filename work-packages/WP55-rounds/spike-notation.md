# Spike: notation and layout in the Boyd lineage (WP55 prework)

## Sources

**Boyd and Vandenberghe, Convex Optimization (2004).** https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf; read Sections 1.6, 4.1.1, one proof and the exercises. A problem is a displayed template, `minimize f0(x) subject to fi(x) ≤ 0, i = 1,…,m`, then prose naming each part: "We call x ∈ Rn the optimization variable". Domain, feasible set, optimal value p⋆ (an infimum) and optimal set are each one sentence, followed at once by small examples. Functions carry types, `f : Rp → Rq`, with `dom f`. Notation is explained in prose (1.6) with a list at the back. Definitions are prose with the term in italics, no boxes. Proofs sit inline under a plain heading ("Proof of first-order convexity condition") after the result, by cases, in "we" prose.

**Boyd, Kim, Vandenberghe, Hassibi, "A tutorial on geometric programming" (2007).** DOI 10.1007/s11081-007-9001-7; https://web.stanford.edu/~boyd/papers/pdf/gp_tutorial.pdf; read Sections 1 to 2.5. Order: variables, monomial `c x1^a1 … xn^an` "where c > 0 and ai ∈ R, is called a monomial function", how it differs from the algebra term, closure properties, lists of examples and non-examples, posynomial, standard form with `fi(x) ≤ 1`, a numeric example counting n, m and p, then the convex form by `yi = log xi`. No theorems or proofs; results are cited to BV.

**Hoburg and Abbeel, "Geometric programming for aircraft design optimization," AIAA J. 52(11), 2014.** DOI 10.2514/1.J052732; https://people.eecs.berkeley.edu/~pabbeel/papers/2014-AIAA-GP-aircraft-design.pdf (Early Edition; no arXiv version exists). A nomenclature list precedes the introduction. Section II fixes "power law notation" `u^a ≡ ∏ uj^aj`, defines monomial and posynomial with a worked sentence (lift is a monomial in u = (ρ, V, CL, S)), then standard form. A small example precedes the full design; constants and solutions get tables. No theorems; guarantees are three bullets (Optimality, Robustness, Speed).

**Magnani and Boyd, "Convex piecewise-linear fitting," Optim. Eng. 10 (2009).** DOI 10.1007/s11081-008-9045-3; https://web.stanford.edu/~boyd/papers/pdf/cvx_pwl_fit.pdf; read in full. "We consider the problem of fitting some given data (u1,y1),…,(um,ym)", then `minimize J(f) subject to f ∈ F` "with variable f", the RMS fit named, easy special cases first. The alternating method is a numbered algorithm, called a heuristic for locally optimal fits, read as Gauss-Newton; Section 3.3 shows a limit cycle. No theorems; assumptions appear at the point of use ("assume that for each data point ui there is a unique j").

**scikit-learn user guide, Decomposing signals in components.** https://scikit-learn.org/stable/modules/decomposition.html; only this page (the linear-models page was not read). `X` has samples as rows; `n_samples`, `n_features`, `n_components` serve math and code alike. Objectives are `argmin` displays with a `subject to` line; each Greek hyperparameter is tied to a code name in prose ("η corresponds to `topic_word_prior`"). No notation table; caveats in Note boxes.

## What the paper's Sections 3 to 6 do differently

- "Mathematical notation follows Boyd and Vandenberghe" is about the text; the lineage states the notation and moves on.
- "The model." gives `J_τ(w)` and `w* ∈ argmin_{w∈Δ}` in an aligned block; the template with its variable, domain and optimal value is absent, so β is never named as an optimal value.
- "A1: metrics are strictly positive." runs through A11 in one paragraph before any result uses them; R1 to R3 ("R1: at the exact-maximum") are long sentences with several cross-references each.
- Every theorem opens "Derived. Hypotheses." and every proof sketch is followed by a "Script" box; BV and the tutorial state results in prose and keep proofs apart.
- "The invariant value V is a weighted geometric mean" uses V before its formula-first definition; no power-law shorthand is fixed.
- "Three objects carry the word frontier" and the n-lemma definition run many sentences and mix thresholds with conventions; BV gives one term per sentence.
- "Where several trade-offs are active at once" brings in K, κ and τ with no bridge to the tutorial's c_k, a_k and log change of variables.
- "Results are read in light of the gaps ledger" and "{ref}Appendix A is the full register" are about the text.

## Recommendations

1. State the fit in the BV template, `minimize J_τ(w) subject to w ≥ 0, 1ᵀw = 1`, "with variable w ∈ R^d", and name β the optimal value (BV 4.1.1).
2. Introduce monomial, posynomial, then log form with `m^w ≡ ∏ m_j^{w_j}` and the map c_k = e^{-κβ_k}, a_k = κw_k (tutorial 2; Hoburg II).
3. Keep M, N, d, say once that they are n_samples and n_features, and tie τ and κ to code names in prose (scikit-learn).
4. Give V its type and domain, `V : R^d_{++} → R_{++}`, where it is defined (BV 1.6).
5. Keep A1 to A3 in Section 3; state A4 to A11 and R1 to R3 in the result that uses them (Magnani and Boyd).
6. Write theorems as "Suppose … Then …" plus one display; drop the Derived and Hypotheses labels and the Script box; end "Proof: Appendix B, L7" (BV, tutorial).
7. Move proofs, scripts and thresholds to the appendix; keep a one-sentence idea only where the claim is not evident (BV inline-proof habit).
8. Define one term per sentence, prose first (tutorial 2.1), and split the n-lemma definition; the K > 1 alternation is a numbered heuristic with a local guarantee (Magnani and Boyd 3.3).
9. Add a table of at most twelve rows (symbol, meaning, code name) ending Section 3; the full register stays in Appendix A (Hoburg nomenclature, BV back list).
10. Delete sentences about the text; cite the convention in the reference list only.
