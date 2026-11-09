# WP10 claims review (Amendment 5, R-43): the claims pass

Stream P5. Method: `docs/superpowers/notes/claims-review.md`, "The requirement" and "The mechanism", steps 1 to 3.

**Pinned commit:** `78f5e1cf984d4589a9232717023f408358c25803` (`origin/dev` when the pass began). Every pointer, fragment and verdict below is as of this commit; edits to the paper and the docs after it are swept by the register test, not re-run here.

## What was done

1. **Units.** 42 units with text (plus the bibliography directive, which has none): one per second-level section of `paper/paper.ipynb` (the Results section split at its three third-level headings, as the paper numbers them 6.1 to 6.3), one per appendix of `paper/supporting_material.ipynb`, one per page of `docs/` that the site navigation lists (14 pages), `site/index.html` and `README.md`. The reader-visible text of each (markdown cells and the markdown outputs of the cells that print prose or tables) was staged outside the repository.
2. **Step 1, extraction.** One fresh-context agent per unit, handed only that unit's text, no repository access. Each listed claims as a verbatim fragment of at least six words and a kind (M, R, S, L, P).
3. **Step 2, backing.** Separate agents with read-only access to a detached checkout of the pinned commit, one per chunk of at most 40 claims (a unit with more claims has several chunks), gave a pointer in the register's syntax or `none`, and a verdict. A claim already covered by a row of `claims_register.toml` is shown as `registered:Cnnn`.
4. **Step 3, dispositions** (the rules are below). Nothing was edited: no prose, no `claims_register.toml`, no test.

## Result

| | Count |
|---|---|
| Units with text | 42 |
| Claims extracted and looked up | 1184 |
| Verdict: backed | 908 |
| Verdict: broader than its backing | 184 |
| Verdict: unbacked | 92 |
| Disposition: keep | 756 |
| Disposition: narrow | 105 |
| Disposition: drop (recorded as candidates) | 55 |
| Disposition: to the driver | 93 |
| Routed to P1 (paper sections 4 and 6) | 115 |
| Routed to P6 (docs examples and soft-fit wording) | 60 |
| Proposed register rows (the TOML block at the end) | 338 |

### Disposition rules applied

- backed: **keep**.
- Broader than its backing, or unbacked, in a claim of kind R, S, L or P: **narrow** (to what the note says is backed) or **drop** (unbacked; each is the unbacked detail itself and is listed in "Candidates for later"). No claim was judged to need only a small implied step to be backed; none is marked "back it".
- Broader or unbacked in a claim of kind M (it would change a mathematical statement), or in the abstract (U01), the discussion (U14) or the final remark (U16) (it would change a conclusion): **to the driver**, not dispositioned.
- Claims in paper sections 4 (Definitions) and 6 (Results, 6.1 to 6.3), and in `docs/examples.md` and the soft-fit wording of `docs/user-guide/fitting.md`, which P1 and P6 are rewriting now: **routed**, with the verdict recorded and no final disposition, whatever the verdict.
- A pointer `definition` means the extractor listed a gloss that the lookup found to be a definition or statement of intent; it is kept, not counted as a backed claim in the register.

### Findings about the pass itself

- **Generated prose is invisible to the register's fragment check.** `tests/test_claims_register.py` reads the markdown cells of a notebook only. Most of Appendices A, C to G and of the paper's prior-art table are the markdown output of a generator cell; claims there are backed by the generator and its test, and are looked up here, but a row for them would fail the checker's fragment test. Of the 756 claims kept, only 338 are proposed as rows because of this, because their pointer is a definition or an existing row, or because their pointer is not yet in the register's syntax (for example a kind R claim with no generator or test named); those are kept and stay in the unit tables. Extending `_source_text` to include markdown outputs would let them be registered; that change is the follow-up unit's or the driver's call, not this stream's.
- **Fragments shorter than six words.** The extractors returned some (mostly typeset formulas); they are in the tables with an `S` in the id (for example `U08-S01`) and have a verdict but cannot be rows.

## Units

| Unit | Source | Section | Claims | Backed | Broader | Unbacked |
|---|---|---|---|---|---|---|
| U01 | `paper/paper.ipynb` | paper front | 11 | 10 | 0 | 1 |
| U02 | `paper/paper.ipynb` | paper The decision problem | 28 | 21 | 4 | 3 |
| U03 | `paper/paper.ipynb` | paper Prior art, by family | 43 | 34 | 9 | 0 |
| U04 | `paper/paper.ipynb` | paper Preliminaries and notation | 13 | 11 | 1 | 1 |
| U05 | `paper/paper.ipynb` | paper Definitions | 18 | 16 | 1 | 1 |
| U06 | `paper/paper.ipynb` | paper Methods | 30 | 20 | 9 | 1 |
| U07 | `paper/paper.ipynb` | paper Results | 3 | 2 | 1 | 0 |
| U08 | `paper/paper.ipynb` | paper The fit and its geometry | 51 | 50 | 1 | 0 |
| U09 | `paper/paper.ipynb` | paper The algorithm for several facets | 41 | 39 | 2 | 0 |
| U10 | `paper/paper.ipynb` | paper Open questions | 2 | 2 | 0 | 0 |
| U11 | `paper/paper.ipynb` | paper Search of the design space (preliminary) | 8 | 5 | 1 | 2 |
| U12 | `paper/paper.ipynb` | paper Case construction | 12 | 11 | 1 | 0 |
| U13 | `paper/paper.ipynb` | paper Case analysis | 21 | 15 | 3 | 3 |
| U14 | `paper/paper.ipynb` | paper Discussion | 25 | 18 | 4 | 3 |
| U15 | `paper/paper.ipynb` | paper Reproducibility and your own case | 4 | 2 | 2 | 0 |
| U16 | `paper/paper.ipynb` | paper Future work and final remark | 6 | 4 | 0 | 2 |
| U17 | `paper/paper.ipynb` | paper Acknowledgments and process | 5 | 3 | 2 | 0 |
| U18 | `paper/paper.ipynb` | paper Works cited | 0 | 0 | 0 | 0 |
| U19 | `paper/supporting_material.ipynb` | supp front | 0 | 0 | 0 | 0 |
| U20 | `paper/supporting_material.ipynb` | supp Appendix A. Notation and terms | 38 | 28 | 8 | 2 |
| U21 | `paper/supporting_material.ipynb` | supp Appendix B. Proofs, step for step with their scripts | 70 | 67 | 1 | 2 |
| U22 | `paper/supporting_material.ipynb` | supp Appendix C. The case's model: how the table of metrics came to be | 31 | 28 | 3 | 0 |
| U23 | `paper/supporting_material.ipynb` | supp Appendix D. Extended results: what the method found in the table | 117 | 107 | 10 | 0 |
| U24 | `paper/supporting_material.ipynb` | supp Appendix E. Assumptions and abstraction gaps | 127 | 58 | 35 | 34 |
| U25 | `paper/supporting_material.ipynb` | supp Appendix F. Computational reproducibility | 77 | 50 | 22 | 5 |
| U26 | `paper/supporting_material.ipynb` | supp Appendix G. Register of prior art | 13 | 10 | 3 | 0 |
| U27 | `docs/index.md` | docs index | 11 | 7 | 3 | 1 |
| U28 | `docs/getting-started.md` | docs getting-started | 15 | 10 | 1 | 4 |
| U29 | `docs/api.md` | docs api | 19 | 19 | 0 | 0 |
| U30 | `docs/api-reference.md` | docs api-reference | 1 | 0 | 1 | 0 |
| U31 | `docs/examples.md` | docs examples | 27 | 23 | 3 | 1 |
| U32 | `docs/theory.md` | docs theory | 26 | 20 | 6 | 0 |
| U33 | `docs/further-reading.md` | docs further-reading | 18 | 12 | 2 | 4 |
| U34 | `docs/user-guide/overview.md` | docs user-guide/overview | 19 | 17 | 2 | 0 |
| U35 | `docs/user-guide/conditioning.md` | docs user-guide/conditioning | 32 | 27 | 2 | 3 |
| U36 | `docs/user-guide/fitting.md` | docs user-guide/fitting | 48 | 33 | 7 | 8 |
| U37 | `docs/user-guide/tensions.md` | docs user-guide/tensions | 32 | 25 | 4 | 3 |
| U38 | `docs/user-guide/chart.md` | docs user-guide/chart | 35 | 28 | 6 | 1 |
| U39 | `docs/user-guide/prediction.md` | docs user-guide/prediction | 13 | 13 | 0 | 0 |
| U40 | `docs/user-guide/termination.md` | docs user-guide/termination | 37 | 26 | 11 | 0 |
| U41 | `docs/user-guide/limitations.md` | docs user-guide/limitations | 30 | 15 | 11 | 4 |
| U42 | `site/index.html` | site index | 21 | 18 | 1 | 2 |
| U43 | `README.md` | README | 6 | 4 | 1 | 1 |
| U18 | `paper/paper.ipynb` | Works cited | 0 | | | |

Empty extractions, with the reason: **U18** (Works cited) is a bibliography directive only and has no prose. **U19** (the supporting material's front matter) has one line of title and was extracted and found to hold no claim. Appendix B's two listings of the derivation scripts and Appendix G's two generated registers (G.1 the register of prior art, G.2 the reading pass) were left out of the staged text: they are the backing (the lemma scripts and the cited-claims audit), not prose to be backed; the claims of the prose around them are in U21 and U26.

## Routed items

### To the driver (changes a mathematical statement or a conclusion)

93 claims. Each is shown in its unit table below with disposition "to the driver"; the list here is the same set in brief.

| Id | Kind | Fragment | Verdict | Why |
|---|---|---|---|---|
| U01-C009 | M | geometric programming (GGP), and the method may be generalized to any kernel that keeps that | unbacked | Kernel generalization 'to any kernel that keeps that compatibility': no lemma, test or contract; documented extension only (CLAUDE.md); PM may reclassify as scope/intent or drop |
| U02-C012 | M | But variance says where the data are free and nothing about trade-offs | unbacked | About PCA's criterion vs trade-offs; no lemma step, no audit row (jolliffe row covers only dimensionality/interpretability/information loss); could be narrowed to the author's judgment (reading). |
| U02-C013 | M | Objectives may align in one region and oppose in another. | unbacked | No lemma step states that objectives align in one region and oppose in another (L7 gives facet-specific elasticities, L10 the K-term model, neither says alignment); an existence claim about the model, unproved. |
| U02-C025 | M | With one term the posynomial extension is the monomial, and a maximizer of V is Pareto-efficient | broader than its backing | K=1 reduction is L10.9 (backed for the model). 'A maximizer of V is Pareto-efficient' is broader than L11: weakly efficient always (L11.18), efficient only when every w_j > 0 (L11.19); section 3 of the paper words it 'with positive exponents'. Same wording as registered C018. |
| U02-C026 | M | The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration | broader than its backing | Nonconvexity is shown only for the soft objective on an exact small instance (L16.37), not in general nor for the sharp fit; three levels are registered C020; 'stopping declaration' is the Termination status of the interface contract, not a lemma step. |
| U03-C004 | M | A one-sided envelope of the data, a score per unit \| One exponent vector per facet | broader than its backing | 'One exponent vector per facet' is backed (L10.19 one theta_k per monomial; exponents_ shape (K,d)); the DEA half 'a one-sided envelope of the data' is not attributed: row 17 says not in the abstract, row 16 not accessible |
| U03-C011 | M | this method fits an envelope, the one-sided boundary of the data | broader than its backing | one-sided boundary holds at tau=inf and K=1 (frac_above_==0, V.max()<=1); at finite temperature rows lie above V=1 by construction (glossary fitted-reference-surface) and at K>1 the facets are not supporting planes |
| U04-S01 | M | some designs lie beyond it | broader than its backing | Glossary says rows above the reference surface exist by construction; L5 gives LME<=max so the top row has V>=1, strictness (some design beyond it) needs non-constant scores and is not a stated step |
| U06-C001 | M | otherwise exponents are a subgradient choice, not an identified trade-off | broader than its backing | L3.9/L3.11 prove identification (equal gradients) under R1; the converse 'otherwise a subgradient choice' is only the R1 failure_mode text in the ledger (axioms.py), no tagged step |
| U06-C003 | M | the factor $1/N$ makes it a property of the shape of the data, not the number of designs | broader than its backing | L5.6 gives LSE-LME=log(n)/tau only; invariance to the number of designs (row replication) is numeric, and I2 is a recorded remark no step uses; 'shape of the data' is wider than replication |
| U06-C011 | M | a convention that keeps one extreme design from setting the surface | broader than its backing | rationale: L5.24 shows tau=inf is set by the maximum; no step or test shows a finite tau at 10 percent keeps one design from setting the surface (n_eff_ 14-16 in D.5 is only descriptive) |
| U06-C012 | M | a scaler equalizes log-spread so one $\tau$ serves every metric | broader than its backing | the scaler equalizing log-spread is tested; 'so one tau serves every metric' is a purpose with no backing |
| U06-C013 | M | rescaling one metric changes which facet is tangent | broader than its backing | L2 covers a uniform shift only (w unchanged); no lemma/test for rescaling one metric; the sensitivity table shows the robust scaler (all metrics) changing the contending set |
| U06-C027 | M | it is exactly invertible ({prf:ref}`thm-pullback`) and stays inside geometric programming | broader than its backing | invertibility backed (L9.4/L9.6); 'stays inside geometric programming' has no step: L9.5 gives the monomial-in-(a+s) form but no GP statement, and (a+s)^negative power is not a posynomial in a |
| U06-C028 | M | $\Phi_K$ is convex in $u$, which keeps later optimization convex | broader than its backing | no lemma step or test states Phi_K convex in u (L10.7 shows e^(kappa Phi_K) posynomial; convexity is inherited I4, cited); 'keeps later optimization convex' not backed |
| U06-S02 | M | no $K$ represents non-log-convex structure | unbacked | no step or test shows the model class excludes non-log-convex structure; it would follow from convexity of Phi_K, itself unproved (see C028) |
| U11-C004 | M | chained back through the conditioning and the evaluation to a direction in configuration space, estimated by finite differences or a supervised regressor | broader than its backing | L9 covers only exact pull-back under log-affine conditioning; chain through a general evaluation and finite-difference or regressor estimate has no lemma (search-prior-art L12 is a note, not a derivation) |
| U11-C006 | M | Because evaluation is noisy, the procedure resembles a diffusion with drift along the tangent spaces. | unbacked | Analogy to a diffusion with drift on tangent spaces; no lemma, test or source |
| U13-C012 | M | Mean slack falls with K by construction and cannot choose it | unbacked | by construction is unsupported: temperature is re-selected at each K and no lemma step states nested-family monotonicity of the mean slack; only the observed fall is pinned (RECORD) |
| U13-C013 | M | The same pipeline on the baseline regime separates the problem's contribution from the gains' | unbacked | interpretive claim that the regimes separate the problem's contribution from the gains'; only the contrast of the two contending sets is generated |
| U14-C003 | M | A hole in the chart is an opportunity only where the trade space is log-convex around it, which the data cannot prove. | unbacked | No lemma step on holes or opportunity; lemma_11 docstring only says non-log-convex front parts are not reached by a w (not a tagged step); 'data cannot prove' is unbacked; narrow to judgment wording or drop |
| U14-C012 | P | An answer far from the frontier is hard to justify | broader than its backing | Worded as fact, kind P; no source; allowed only as the author's experience, so rewording as such is needed (e.g. 'In our experience ...') or drop |
| U14-C013 | P | the analysis must rerun on empirical data to support configuration management | broader than its backing | Worded as fact, kind P; no source; allowed only if worded and marked as the author's experience/judgment, else drop |
| U14-C017 | M | One facet is tangent at one place and is conservative off it. | broader than its backing | L10.9/L10.15 (Phi_K at or above each facet term) give a lower bound but 'tangent at one place' and 'conservative off it' (relative to what) are in no step or test |
| U14-C021 | M | Tensions the sampling never exercised cannot appear. | unbacked | No lemma step or test that a facet absent from the sample cannot be recovered; truism of fitting, needs a one-line test (planted facet unsampled) or drop |
| U14-C023 | M | so $V-1$ is a relative improvement, meaningful relative to the band $1/\tau$. | broader than its backing | V-1 as a relative improvement is L1.5/L7.9 (scaling by 1/V reaches V=1); 'meaningful relative to the band 1/tau' is in no step (band 1/tau is the regressor's own resolution, not tied to V-1 in a lemma) |
| U14-S01 | M | Small samples determine exponents weakly. | unbacked | No sample-size test or lemma; n_eff is reported but no sweep or step shows exponents are weakly determined by small samples |
| U16-C002 | M | whose generalized gradient is the convex hull of the active normals | unbacked | no lemma or audit row states the generalized gradient of a max (Clarke: hull of active gradients); only a subgradient inclusion in axioms.py failure_mode; standard fact but unbacked here |
| U16-S01 | M | should tolerate the kinks | unbacked | prediction ('should') resting on the unbacked generalized-gradient claim; no lemma or test on nonsmooth search |
| U20-C009 | M | a name for the fitted reference surface, which is a level set of a posynomial | broader than its backing | Level set of a posynomial holds at finite kappa (L10.7: exp(kappa Phi_K) = sum of monomials = 1). At the default kappa = infinity (sharp weights) the surface is max_k(monomial_k) = 1, a level set of a generalized posynomial, not of a posynomial (L10.18). Narrow to 'finite term temperature' or say 'of a posynomial (of the max of monomials at infinite term temperature)' |
| U20-C010 | M | the logarithmic change of variables makes it a convex program | broader than its backing | Backed for a geometric program (I13 via L4.23/L4.24: log change gives the convex form). The same fragment also stands in the generalized-geometric-program entry, where no step states that a GGP becomes convex under the log change (Boyd 2007 s5.4 only, not in an audit row) |
| U20-C011 | M | the several-facet fit as one program, which is not convex in the terms (L16) | broader than its backing | L16 (i) shows the soft-weight (finite kappa, tau=kappa=1, two terms) objective is not convex 'in general' by an exact instance. No step covers the sharp-weight (kappa = infinity, minimum over facets) several-facet fit; I13 failure_mode says it is not a GP as a whole, which is not a nonconvexity proof |
| U20-C013 | M | and added variables turn it into a geometric program | unbacked | No lemma step, ledger entry or audit row states the GGP-to-GP reduction by added variables: I15 cites Boyd 2007 s5.3/5.4 only for the definition; reading_pass n=37 read s5.3 and s8; references-verified.md records s5.4 as 'any GP is a GGP'. Add a reading_pass row on s5.4 or drop the clause |
| U20-C015 | M | a design problem that uses the fitted model is one, and so is the fit with its weights given | broader than its backing | The fit-with-weights-given half is backed (see C012). 'A design problem that uses the fitted model is one' has no step: the model part is a (generalized) posynomial in m (L10.7, L10.18) but the design problem is a GGP only if the objective, other constraints and the map from design variables to metrics are GGP-compatible; the black-box configuration-to-attributes map is not |
| U20-C016 | M | the level set V = 1 of the fitted invariant, where the posynomial sum equals one | broader than its backing | definition of the surface as V = 1 is fine (L1.6); the gloss 'where the posynomial sum equals one' holds for finite kappa (L10.7) and only in the limit at kappa = infinity (max of monomials = 1, L10.18) |
| U20-C030 | M | gamma divided by twice the largest row norm | broader than its backing | backed only for the augmented row (u_i, -1), norm sqrt(\|\|u_i\|\|^2 + 1) (L13 U >= 1; solvers.assignment_margin doctest); 'row norm' read as \|\|u_i\|\| gives a larger, unproved radius |
| U23-C050 | M | The margin gamma is in score units, the scale of the band 1/tau; below the band, a change as small as the band can move a design to another facet. | broader than its backing | L13.7 gives sufficiency only (score changes below gamma/2 keep the facets); 'a change as small as the band can move a design' is not stated (the lemma says the radius is not proved tight), and 'scale of the band 1/tau' is a reading, not a step |
| U23-C051 | M | far below it, a few designs sit on a seam and most do not. | broader than its backing | gamma is the minimum gap (L13); 'far below the median gap, a few designs sit on a seam and most do not' is not in any step: a small min gap says one row is near a seam, not how many; only 'at least half have gap >= median' follows |
| U23-C052 | M | The stable radius is gamma divided by twice the largest norm of a row of the log-metrics with a final entry of minus one, so it is smaller than the margin and is sufficient, not tight. | broader than its backing | radius = gamma/(2U) with U>=1 (hypothesis symbol U_ in L13) gives smaller than gamma and sufficient (L13.7, L13.11, doctest); 'not tight' is stronger than the lemma, which only declines to prove tightness |
| U23-C083 | M | a small value flags a nearly flat direction, so weakly identified exponents. | broader than its backing | L4.3 gives the curvature along a direction (tau Var_p); small smallest eigenvalue = small curvature is immediate, but 'so weakly identified exponents' is an interpretation with no lemma (L4 states uniqueness is not proved; G-2 and G-12 list it as a bridging assumption) |
| U23-C098 | M | a frontier row on two facet planes ties at the exact maximum and the platform's argmax and linear-program vertex choice resolve the tie | broader than its backing | no lemma step says a row on two facet planes ties (L13 assumes positive margin, R2); the tie and the platform's argmax/LP vertex resolution are empirical, in the G-10 ledger and CI runs, only partly tested |
| U23-C102 | M | a facet needs at least 5 frontier rows, one more than there are metrics, to be determined by them | broader than its backing | only the generator's rule (d+1 frontier rows per planted facet) is tested; no lemma says fewer cannot determine a facet, and d points already fix a plane in d log-metrics given the sum-to-one normalization, so 'needs at least d+1' is a design rule, not a stated necessity |
| U24-C006 | M | Fraction above $V=1$ is a property of $(\tau,K)$ | unbacked | no lemma step; the dependence on (tau,K) is shown only by the numbers of C002-C004 (R), not by an M step |
| U24-C007 | M | at finite $\tau$ with $\beta=J_\tau(Uw)$ (L3, L5); $V>1$ is possible. | broader than its backing | L5.15 gives LME<=max so the top row has log V>=0 (L1.7 log V=w.u-beta); strict V>1 not tagged (needs non-constant scores); only the numbers (C002) show V>1 occurs |
| U24-C009 | M | only the log-convex part of a Pareto front is reached by some $w$ (L11) | broader than its backing | L11 proves maximizer => weakly efficient only; that only the log-convex part of a front is reached (supporting-hyperplane direction) is not a tagged step |
| U24-C011 | M | positive definite on the participating coordinates (L3, L4, R1) | broader than its backing | L4.3 gives second derivative tau Var_p (PSD, convex); positive definiteness is not proved (L4 docstring: strict convexity needs a rank condition) and G-2 lists it as unprovable |
| U24-C019 | M | a small `conditioning_` marks a flat direction in which two fits with equal objective differ in $w$ | broader than its backing | L4.3 gives curvature tau Var_p along a direction; small eigenvalue means nearly flat, not that two fits with equal objective exist (equal vs nearly equal, local second order) |
| U24-C025 | M | for one row it is $\min_w w\cdot u_1$, attained at the vertex on the row's smallest log-metric | broader than its backing | for n=1 mean=LME=max gives J=w.u_1 (L5.14, L5.15); the vertex at the smallest log-metric is an elementary LP fact with no tagged step |
| U24-C031 | M | $w_j=10^{-13}$ gives a finite score and $w_j=10^{-11}$ gives $-\infty$ on the same row | unbacked | the 1e-12 cut is in code (EPS_ZERO_EXPONENT, _zero_limit_scores) but no test sets w_j=1e-13 and 1e-11 on one row; test uses exponent exactly 0 |
| U24-C036 | M | The plain fit on a facet's own rows has its support function minimized at a vertex of the simplex | unbacked | no lemma; ledger itself says observed, not proved; and its own example (own-rows LP returns 0.416,0,0.119,0.465) is not a vertex |
| U24-C037 | M | (edge-interior optimizers exist for other geometries) | unbacked | existence of edge-interior optimizers is asserted without example or lemma (the seed-0 own-rows LP is a face-interior point, but is not cited for this) |
| U24-C042 | M | A facet with fewer affinely independent frontier rows than $d$ does not determine its hyperplane | unbacked | linear-algebra fact (d-m free parameters); no lemma step states it; spike check_identifiability.py only counts |
| U24-C087 | M | The contending set is the support of $w$; identified only where the restricted Hessian is positive definite | broader than its backing | support definition is the glossary's; but 'identified only where the restricted Hessian is positive definite' (necessity, and uniqueness) is not proved: L4 shows convexity only and states it does NOT prove strict convexity or uniqueness |
| U24-C097 | M | (one hyperplane is not tangent where the boundary curves) | unbacked | geometric remark with no lemma step (L10/L11 do not state it); source is docs/user-guide/limitations.md prose |
| U24-C098 | M | No theorem for the multi-facet alternation beyond I7 (the partition-and-refit pattern of Magnani and Boyd) and the three levels (L12 to L14), all local. | broader than its backing | 'all local' and no global theorem are backed (L14 'does NOT prove global'; I7 is local); but 'the three levels (L12 to L14)' omits L15 (descent is proved) and L16/L17 are also theorems about the alternation |
| U24-C103 | M | Every $K>1$ result is a local optimum of its run, reported with `random_state` | broader than its backing | L14 gives a local minimizer only for step B, unpenalized, positive margin R2, exact facet optima; statuses stationary_without_margin, uncertified, guard_stop, iteration_cap, the tangent step and the penalty carry no local-optimality claim (ledger G-8, G-10), so 'every K>1 result' is broader |
| U24-C111 | M | it is sufficient, attained only for changes parallel to the design vector | broader than its backing | sufficiency is L13.11 (L13 says tightness is not proved); 'attained only for changes parallel to the design vector' is the Cauchy-Schwarz equality case, found only in the I9 failure_mode text, not a tagged step |
| U27-C008 | M | PCA finds where the data spread, this finds | broader than its backing | PCA (spread) half is the definition of PCA (L-type, jolliffe2016principal); no lemma step; as an M claim there is no lemma, only tests of orient_by_pca; recast as S/L. |
| U27-C009 | M | where they stop, and the two chain. | broader than its backing | 'where they stop' is backed at tau=inf only (V<=1 for all rows); at finite tau a tenth of designs lie above V=1; 'chain' backed as S (tension directions = PCA of near-frontier Z), not an M lemma step; also no lemma. |
| U32-C009 | M | The fit chooses $w$ and an offset $\beta$ so that the data lie on or below the surface | broader than its backing | 'on or below' holds only at tau=infinity (beta = max); at finite tau beta = LME <= max (L5.15), so rows lie beyond the surface, as the next bullet itself says |
| U32-C011 | M | V = 1 at the working temperature tau; it is smooth, so a few | broader than its backing | L5.15 (LME <= max) gives the top design on or beyond V=1; 'a few designs' (a count) is not stated by any step |
| U32-C017 | M | The map is reversible for every row with strictly positive metrics: nothing is lost | broader than its backing | L8 proves the bijection of (log-scale, Z) i.e. u, not of (Z, log V); the step to log V = w.u - beta is untagged (the test pins the round trip on data only) |
| U32-C021 | M | tau = infinity is a linear program whose solution is generically sparse. | broader than its backing | LP part backed (L12.31); 'generically sparse' is not proven, only pinned on planted sparse supports (an LP vertex is sparse, but no step or test says generic) |
| U32-C024 | M | larger-is-better (conditioning is yours to choose); the surface is log-convex; | broader than its backing | Positivity/larger-is-better are assumptions; 'log-convex surface' is not a tagged step (L10.7 posynomial; L4 convexity is in w, not in log m) |
| U34-C002 | M | this method finds the positive combination of the metrics along which the data stop, | broader than its backing | L3 gives KKT/optimality of the fitted weights and L1 the invariant form; neither states the data 'stop' along the combination (a descriptive gloss of the fit; no global guarantee, see C020) |
| U34-C005 | M | weights sum to one, and the metrics with non-negligible weight are the ones that contend. | broader than its backing | sum to one is the simplex axiom (L1, A2) and tested; 'non-negligible weight = contend' holds exactly only at tau=inf; at finite tau weights are smoothed and participation depends on a threshold (the test says so) |
| U35-C010 | M | decision about where the scale begins, and different shifts give different fits. | unbacked | No lemma or test shows different attribute shifts give different fits; L2 is the uniform shift of log data, a different statement |
| U35-C017 | M | quoted in inverse log-spread, so equal log-spread makes one temperature mean the same for every | unbacked | No lemma step or test shows the temperature is in inverse log-spread units or that equal log-spread equalizes its meaning across columns |
| U37-C002 | M | The model looks for the binding constraint, so the report describes a tension, where | unbacked | no lemma step or test says the fit finds the binding constraint or contrasts it with PCA; module docstring only |
| U37-C009 | M | `min_exponent` must be 0 for this reading, because a positive floor masks the | unbacked | no lemma step; only the warning is tested (software), and the LP being recomputed with min_exponent=0; 'masks the sparsity' (a floor forces all exponents >= floor, tests/test_estimator.py::test_fit_invariants checks w.min() >= min_exponent) is a small step not tagged |
| U37-C011 | M | At the working temperature the exponents are smoothed, so a small one means weak participation, not | broader than its backing | pinned only on one planted trilemma example (free-metric weights < half the members'); no lemma that smoothing gives non-membership in general |
| U37-C021 | M | constraint produces negative association even where no designer traded the metrics (`closure_note` | broader than its backing | pinned on one planted example and the closure_note text; no lemma that a binding constraint forces negative association in general |
| U37-C027 | M | along the surface is the set of trade-offs the designs exercised. | broader than its backing | interpretive: pinned only for a planted spread; 'the trade-offs the designs exercised' is a reading, no lemma |
| U38-C012 | M | At a finite temperature some training designs lie beyond V = 1 by construction | broader than its backing | L5.15 only gives LME <= max (so the top design has V >= 1); strictly 'some beyond' is asserted only on planted data (0 < frac_above_ < 0.5), not proved in general |
| U38-C013 | M | meaningful relative to the band of width 1/tau. | unbacked | no test pins the band width 1/tau as the right reading scale (plotting _band default is a convention; L5.16 gives log n/tau); advice sentence |
| U38-C026 | M | The surface is also log-convex, so structure that is not log-convex is invisible to it. | broader than its backing | L10.7 gives the model as a posynomial in m; log-convexity of the surface in log metrics and the 'invisible' consequence are not a tagged step |
| U40-C008 | M | to the facets cannot change which facet dominates which design, so the fixed assignment is optimal. | broader than its backing | L14 Prop 3 gives a local minimizer of the full objective, under exact facet optima, no penalty, step-B offsets (beta=J_tau); 'the fixed assignment is optimal' omits local and the hypotheses (lemma not covering a tolerance eps_kkt) |
| U40-C033 | M | the median gap between a design's best and second-best facet score: far below it, a few designs sit | broader than its backing | gamma is the minimum gap, so far below the median says at least one design is near a seam and (by the median) at least half are not; 'a few designs' is not implied; no lemma or test states it |
| U40-C036 | M | `certified` says the run is a local optimum (of its fixed assignment, or of the soft objective), nothing about other restarts. | broader than its backing | Prop 3 and the second-order test are for exact first-order conditions and exact facet optima; the run is certified only within eps_kkt/eps_feas, a numerical tolerance L17 says is not covered |
| U41-C002 | M | reference or the scale of one metric changes which facet is tangent. | broader than its backing | L2 proves only the uniform shift (exponents unchanged) and says per-metric shifts change the facet is NOT proved (spec item 6); no test or lemma shows which facet is tangent changes under reference/scale moves |
| U41-C003 | M | Dents, holes and disconnected regions are invisible to it | broader than its backing | L10.4 gives exp(kappa Phi_K) a posynomial and L4 convexity of J, but no step states that dents/holes/disconnected regions are invisible; L11 only says non-log-convex front parts are not reached by any w |
| U41-C004 | M | number of terms represents them. A hole is an opportunity | broader than its backing | Same as C003: any K-term model is a posynomial (log-convex), but 'no number of terms represents them' is not a stated step |
| U41-C005 | M | A hole is an opportunity only if the trade space is log-convex around it. | unbacked | Conditional about when a hole is an opportunity; no lemma, test or source states it |
| U41-C007 | M | Away from that point a design can score below 1 while locally on the frontier. | unbacked | No lemma or test shows a design can score below 1 yet be locally on the (true) frontier away from the balanced point |
| U41-C008 | M | If the balanced point sits on a vertex or | broader than its backing | L7 gives elasticities only for w_j != 0 (undefined at w_j = 0); non-uniqueness of the exponents at a vertex/edge is not proved in any lemma step or test |
| U41-C009 | M | exponents are not unique and some elasticities are undefined. | broader than its backing | Same as C008: undefined elasticity supported by L7 (w_j in the denominator); 'exponents are not unique' not stated in a step |
| U41-C013 | M | Judge a score against the band 1/tau. | broader than its backing | Advice; 1/tau is the default near-frontier band (tension_report test), but L5 gives the LME offset from the max as up to (log n)/tau, not 1/tau; no lemma states 1/tau as the scale of scores beyond V = 1 |
| U41-C015 | M | tau of about 3 the soft maximum approaches the mean. | broader than its backing | L5.4 proves LME -> mean only as tau -> 0; the threshold 'about 3' appears only in fitting.md/tuning.py docstring, with no test or lemma |
| U41-C016 | M | With few designs, or designs that barely differ near the edge, exponents are | unbacked | No test, lemma or run shows exponents are weakly determined for few or near-edge-clustered designs |
| U41-C024 | M | More restarts do not cure this; a larger sample or `facet_step="tangent"` | broader than its backing | Restarts half only in G-14 text (WP9-review: 5, 20, 50 restarts, no failing seed recovered); no test/generator pins it; 'larger sample or facet_step=tangent can help' has no run: the test covers identifiable tables only, not the failing seeds |
| U41-C026 | M | Elasticities are shape, not preference, and not causal. | broader than its backing | L7 says elasticities are shape quantities, not preferences; 'not causal' is not stated in a step or test |
| U41-C027 | M | A prediction inherits the surrogate's error and the fitted trade | unbacked | Caution on inherited surrogate error; no lemma, test or source asserts it (test_predict_check_within_the_band checks a band, not inheritance) |
| U43-C002 | M | Pareto frontier, together with an invertible coordinate chart (position along the frontier, and | broader than its backing | Chart invertibility is backed (L8.14 round trip, L9.6 conditioning); 'unit level set is the Pareto frontier' is broader than L11 (a V-maximizer is efficient, converse not claimed; fitted frontier is not the true front); narrow to 'a model of the frontier' |

### Routed to P1 (paper sections 4 and 6)

115 claims in units U05, U07, U08, U09, U10 (backed 109, broader 5, unbacked 1). The ones that are not backed, for P1 to settle while rewriting:

| Id | Kind | Fragment | Verdict | Why |
|---|---|---|---|---|
| U05-C009 | M | in the soft maximum a design inside it weighs within a factor $e$ of one on the surface | unbacked | No lemma step or test states the weight ratio: the soft-max weight e^{tau(w.u-beta)} = e^{tau log V} lies in (1/e, e) when \|log V\|<1/tau is a one-line fact from L3 support weights / L5 terms, untagged; tests/test_paper.py::test_cr3 only checks the phrase is present. Candidate to back with a tagged step or narrow. |
| U05-C016 | M | the normal $w_k$ is the steepest ascent of $\log V$ | broader than its backing | L7.4 gives the directional derivative dG(v)=w.v of G=w.u-beta, so w_k is the gradient and the tangent part is backed; 'steepest' ascent (Cauchy-Schwarz, Euclidean metric on log-metrics u) is not a tagged step and no test pins it. |
| U07-C002 | M | it has three levels of guarantee (L16, L15, L12 to L14) and, for a soft fit, a certificate (L17) | broader than its backing | L16 is the soft-weight alternation (not a sharp-weight level), so (L16, L15, L12 to L14) lists four groups for three levels; the three levels are L15, L12, L13-L14 (as the Main results sentence says); L17 certificate is correct |
| U08-C040 | M | That only the log-convex part of a front is reached by some $w$ is our statement, not a cited one. | broader than its backing | Provenance backed (reading_pass n=14,15: citations removed, stated as own) but the content 'only the log-convex part is reached by some w' has no tagged step (L11 docstring only, which still cites Miettinen/Ehrgott and says converse not proved). |
| U09-C038 | R | a margin below the band puts a few designs on a seam, and the certificate covers changes under the radius only | broader than its backing | Second half (certificate covers changes under the radius) is L13.7/L13.11. First half: gamma is the minimum gap, so gamma below the band only shows at least one design within the band of a seam; 'a few designs' has no count pinned anywhere (no test or generator counts designs inside the band) |
| U09-S02 | M | sufficient and not tight | broader than its backing | Sufficiency is L13.11; 'not tight' is not shown: lemma_13 docstring says it does NOT prove the radius is tight (the confined instance uses 0.9 of the radius), nor that it is loose; reword to sufficient, tightness not claimed |

### Routed to P6 (docs examples and soft-fit wording)

60 claims in `docs/examples.md` (U31) and `docs/user-guide/fitting.md` (U36) (backed 43, broader 9, unbacked 8). The ones that are not backed:

| Id | Kind | Fragment | Verdict | Why |
|---|---|---|---|---|
| U31-C010 | R | 78 percent of the near-frontier share and is the only one containing total mass and peak slew | broader than its backing | 78 percent (share 0.778) and big facet starting 'peak slew power, total mass' are pinned; 'only one containing total mass and peak slew power' not asserted (run confirms the other two lack both, but no test checks the other contending sets) |
| U31-C011 | R | power; the other two are built on control effort, slew time and energy balance. | unbacked | run shows facets 1,2 largest exponents are control effort/slew time/energy balance, but no test asserts the other two facets' sets or exponents |
| U31-C020 | M | A design mostly in metric 3 with a little metric 1 is in the blue region, where metric 3 trades | broader than its backing | worked reading of the figure ('blue region', metric 3 vs metric 1) is an illustration on the planted table; no test pins the colours or which metrics trade in the region; a how-to-read example |
| U31-C022 | R | case do not separate in three metrics, so none is drawn for the cubesat. | broader than its backing | no generator or test shows ten-metric cubesat designs do not separate in three metrics; only that plot_ternary refuses X with groups (ValueError); the 'do not separate' result is unbacked |
| U36-C010 | S | `mean_slack_` is the mean gap between facet and design, defined at every number of terms; compare | broader than its backing | Gap to the dominant facet holds for the label fit; at finite term_temperature and K>1 it is the slack of the soft surface Phi_K; 'compare at a fixed temperature' is docstring only, no test. |
| U36-C017 | M | reference surface with a band of near-frontier designs of width 1/tau, and a few designs beyond | broader than its backing | Band 1/tau is the tension_report/facet_share_ convention (pinned), not a bound (L5.16 gives log N / tau); 'a few designs beyond V=1' only pinned as 0<frac<0.5, and frac is about 1/2 at tau<3. |
| U36-C018 | M | V = 1. Tau is in units of inverse log-spread, so it depends on the conditioning. | unbacked | Units claim (tau scales log-scores; scaling u by c equals tau->c*tau) is in docstrings only; no lemma step or test; one-line derivation, candidate to back. |
| U36-C022 | M | `frac_above_` is not monotone in tau. | unbacked | 'Not monotone' (below tau about 3) is only a comment in tests/test_tuning.py::test_tau_sweep_is_monotone_from_half_toward_zero, which asserts monotone for tau>=3 on one table; the non-monotone half is not asserted. |
| U36-C026 | S | (`n_restarts`, default 5) keeping the best. `assign_facets(X)` reads which facet | broader than its backing | Default 5 and assign_facets == facet_ pinned; 'keeping the best' (min objective over restarts) is in solve_terms but no test asserts it. |
| U36-C030 | S | - `facet_step` is `"support"` (default) or `"tangent"`, which is not monotone and carries no | broader than its backing | Default support and tangent -> not_applicable (no local-optimality status) pinned; 'is not monotone' is stated as fact but only 'best iterate kept' is tested (comment); should read 'has no monotonicity guarantee'. |
| U36-C033 | P | variation between restarts. Resample: a facet whose exponents change between bootstrap resamples | unbacked | Rule of thumb (restart variation; a facet that changes under resampling is a splinter and K too large) has no source or test and is not worded as the author's judgement; only the K=4 run illustrates it (cold-read note is anecdotal). |
| U36-C034 | R | The mean slack falls from 0.855 at K = 1 to 0.692, 0.664 and 0.658: the third term is the last that | unbacked | Values 0.855, 0.692, 0.664, 0.658 reproduced by running the page's block (K=1..4, tau=50) but no test or generator file pins them; 'third term is the last that pays' is a reading. |
| U36-C036 | R | 0.00 to 0.07 at K = 4: the fourth facet changes with the sample. | unbacked | K=4 smallest exponent 0.00 0.03 0.00 0.07 reproduced by running the block; not pinned by any test. |
| U36-C037 | M | With several terms the facets are not | broader than its backing | General claim about every K>1 fit rests on instances (K=2 table seed 777 floor above 0.10; cubesat frac>0.25); no lemma; estimator docstring even says each facet is a supporting hyperplane over all rows. |
| U36-C038 | R | supporting planes, so `frac_above_` levels off above zero as tau grows (about 0.30 on the table of | broader than its backing | Levels off above zero pinned for the K=2 table (not bracketed at 0.10, floor target reachable); 'about 0.30' reproduced by me (0.30 at tau=1e3, 1e4) but not pinned by any test. |
| U36-C043 | R | `temperature`, that holds enough. On that table at tau = 50 the band 0.02 holds five designs of | unbacked | No generator or test pins 'five designs at band 0.02'; the test only checks the named band holds >=10 rows |
| U36-C044 | R | facet 0 and 0.025 holds ten. | unbacked | No generator or test pins 'ten designs at 0.025' for facet 0; unpinned number |

## Candidates for later (dropped as unbacked)

Each is an unbacked detail of kind R, S, L or P; the disposition is to drop it. Recorded here so that backing it later, if wanted, starts from the list.

| Id | Kind | Fragment | What is missing |
|---|---|---|---|
| U02-C009 | P | but the computational alternatives are bespoke and opaque | 'computational alternatives are bespoke and opaque' is a general claim about the world; no audit row, source or reading marking; prior_art mbse row says nothing of bespoke/opaque. |
| U04-C009 | P | All models are wrong, some are useful, and a model is useful for a specific purpose in a specific situation | Box aphorism uncited: no Box entry in docs/references.bib, prior_art.yaml or reading_pass.yaml; cite a verified source, mark as the author's maxim, or drop |
| U11-C001 | P | A trade study also decides what to evaluate next, today by expert intuition or exhaustive sampling. | Practice claim about how trade studies choose evaluations today; no source or reading marker (search-prior-art.md is not an audit row) |
| U13-C006 | R | with working-temperature exponents from 0.09 to 0.24 | no test pins 0.09 to 0.24; num-k1 is not in NUM_CELLS and only the phrase is asserted; values match sensitivity.json (0.0906 to 0.2406 range, committed 0.091 and 0.2395) |
| U20-C014 | L | the older use of the phrase for signomial programs | Lead only: references-verified.md says Boyd 2007 s9.1 notes some authors use the name for the wider nonconvex class; test_build_generated.py only asserts the word 'signomial' is in the not field. No audit row (prior_art/reading_pass) with verdict supported for this sentence |
| U21-C046 | S | it returns the restart with the smallest mean slack | solve_terms returns min(runs, key=objective) but no test pins best-of-restarts (test_n_restarts_default only checks 5 == default) |
| U21-C065 | S | \| Also run every computed step \| `uv run python -m derivation.proofmap --execute` \| | --execute exists in proofmap.main/run_chain_check but no test exercises it or asserts its behaviour |
| U24-C014 | R | Halving or doubling $\tau$ at $K=1$ moves the largest exponent by 0.008 and 0.022 (primary) | M5 recipe is prose in abstraction-gaps.md; no generator or test prints 0.008 and 0.022 |
| U24-C015 | R | 0.045 and 0.056 (stock), with six participants throughout (M5) | M5 numbers (0.045, 0.056, six participants) have no generator or test |
| U24-C016 | R | One primary $K=3$ facet has 7, 5, 3 exponents above | M3 count of exponents above 1e-3, 1e-2, 0.03 has no generator or test (test_k3_facets pins n_lemma 6,6,7 at the 1e-9 threshold, not these) |
| U24-C018 | R | (exponents below about 0.03 move with a few vertex rows) | a caveat in adcs-tensions-probe.md (noisy below about 0.03, sensitive to a few vertex designs); a judgment, no generator or test |
| U24-C021 | R | the ratio of the fitted offset shift to $\tau\sigma^2\lVert w\rVert^2/2=0.038$ is 1.072 (N=400, sd of the shift 0.0061) | M1 ratio 1.072 (N=400, sd 0.0061) from prose recipe only; test pins N=40000 one seed |
| U24-C032 | R | zeroing metric 4 (exponent 0) in 10% and 30% of $N=400$ rows moves the fitted exponents by at most 0.0008 and 0.0013 | M4 numbers 0.0008 and 0.0013 from prose recipe (noise 0.05, alpha 0.01, N=400); no generator or test (test_zero_metric_row adds one row at 1e-9) |
| U24-C039 | R | (median error 0.857 for facets with at most 4 frontier rows, 0.649 above 30) | medians 0.857 and 0.649 only in spike oracle.txt (bench_oracle.py, older data with facets of <=4 frontier rows, which the generator no longer makes); own_rows_refit prints largest errors only; no test |
| U24-C041 | R | the own-rows LP on seed 0 returns $(0.416,0,0.119,0.465)$ for the planted $(0.212,0.334,0.245,0.209)$ | own-rows LP vector only in spike-facet-refit README/oracle.txt (bench_oracle.py); no test pins it |
| U24-C044 | R | seed 1 has 3 rows, 1 free parameter; seed 16 has 2 rows, 2 free; seed 3 has 6 rows, 0 free | rows and free parameters only in spike-objective README section 2 (check_identifiability.py); no test pins them |
| U24-C045 | R | With true labels step B recovers all 60 facets, including those with 2 to 4 frontier rows | 60/60 with true labels only in spike-facet-refit README/oracle.txt; no test uses true labels |
| U24-C046 | R | Alternation recovery is 17/20 and 16/20 at $\tau=\infty$, 50 | 17/20 and 16/20 only in WP9-review/WP13-decisions and spike; no test pins the 20-seed rates |
| U24-C047 | R | failing seeds 1, 3, 16 and 8; fewest frontier rows 5, 6, 5, 11 | failing seeds and their frontier-row minima only in WP9-review/spike; tests assert only >=5 rows for 4 seeds |
| U24-C053 | R | Recovery, 20 seeds: support 17/20 ($\tau=\infty$), 16/20 (50); tangent 16/20, 17/20 | 17/20, 16/20 (support) and 16/20, 17/20 (tangent) not pinned by any test; WP9-review/spike only |
| U24-C054 | R | tangent seed 8 at $\tau=\infty$ has error 0.054 against the 0.05 criterion | seed 8 tangent error 0.054 only in WP9-review; test_tangent_recovers_planted_facets covers seeds 0,2,0,4 only |
| U24-C062 | R | At $K=3$ some facets hold 3 to 6 designs in their own band. | 3 to 6 designs in own band only in k3-cubesat.md; no test or generator cell pins it |
| U24-C064 | R | Objective stable to $2\times10^{-6}$ over seeds 0 to 4 (primary) | 2e-6 over seeds 0 to 4 only in k3-cubesat.md; tests run seed 0 only; stability_extra.json is a different measure |
| U24-C072 | R | $\gamma\le0$ in 8 at $\tau=\infty$, 0 at $\tau=50$ | spike 100-restart counts (8 and 0) only in spike-certificates README tables 1 and 2; no test |
| U24-C073 | R | the 9 guard events at $\tau=\infty$ were round-off, 8 of them two identical facets | 9 guard events, 8 duplicate facets only in spike-certificates README/dup_facets.py; no test pins the counts |
| U24-C074 | R | $\gamma=9\times10^{-16}$ on 3 of 5 seeds (one tied row) | gamma 9e-16 on 3 of 5 stock seeds only in spike-certificates README table 3; no test |
| U24-C083 | R | the largest exponent error (median over seeds) is 0.013, 0.018, 0.011 at $N=200$, 2000, 20000 for $\tau=\infty$ (no decay) and 0.008, 0.007, 0.003 for $\tau=50$ | M2 numbers (0.013, 0.018, 0.011; 0.008, 0.007, 0.003) exist only as the ledger's recipe M2; no generator script or test pins them (test_recovery_tau_inf is noise-free) |
| U24-C091 | R | Mass has $\tau=\infty$ exponent 0.006 and working 0.094 over all designs in the probe | comes from the 2026-11-08 probe note on a 4-metric 960-design set (tau 21.7); the note says its script was a scratch file, nothing committed; no generator or test |
| U24-C092 | R | A stock $K=3$ facet has exponents of 0.0013 and 0.0188 near the threshold (M3). | M3 recipe only; the values 0.0013 and 0.0188 appear in no committed record, test or script output (k3-cubesat.md lists largest exponents only) |
| U24-C095 | R | 20 seeds, $N=400$, $d=4$, $K=3$: support step 17/20 ($\tau=\infty$), 16/20 (50); failures are facets with 5 to 11 frontier rows | 17/20 and 16/20 on 20 seeds at N=400 are recorded in work-packages/WP9-review.md (reviewer's run); no test pins them (the tests use four favourable seeds), failures at 5 to 11 frontier rows likewise only in review |
| U24-C101 | R | at $\tau=\infty$ 0.1224 (2 seeds) and 0.1447 (3 seeds) | 0.1224 (2 seeds) and 0.1447 (3 seeds) match spike-certificates README table 3 (stock, tau=inf) but are pinned by no test |
| U24-C102 | R | Planted seeds 1, 3, 8, 16 with 5, 20, 50 restarts: no failing seed recovered; seed 8 passes at 5 and fails at 20 and 50 | recorded in WP9-review.md third review from a scratch script outside the repo (/private/tmp/.../rec2.py); sentence lacks the scope (default step, tau=inf for seed 8); no test |
| U24-C105 | R | assignment fixed in 89 ($\tau=\infty$) and 100 ($\tau=50$), guard in 9 and 0, 50-iteration cap in 2 and 0 | numbers match spike-certificates README table 2 (100 restarts per tau, run_planted.py output committed) but no test pins them; the spike predates the guard tolerance |
| U24-C119 | R | The times moved by at most 0.49 s except one design | 0.49 s appears in work-packages/swap-evidence.md (five regenerations); sensitivity.json and test_sensitivity pin no time-column maximum (tests use synthetic tables) |
| U24-C120 | R | 763, whose slew time went from 33.44 s to 12.53 s | design 763, 33.44 s to 12.53 s, appears only in work-packages/swap-evidence.md; no committed result file or test pins it |
| U25-C001 | S | - **The repository keeps:** the code, the tests, the lock file, the Dockerfile and the ledger. | The repository keeps: list of artifacts; code, tests, lock file, Dockerfile exist but the 'ledger' (axiom or experiment ledger) is not pinned by any test; intent statement of appendix content |
| U25-C015 | S | \| Node.js \| v23.7.0 \| not pinned by uv.lock; MyST requires 22 or newer \| | Node version is observed from node --version; no test; 'MyST requires 22 or newer' appears in Dockerfile comment and a test skip reason only |
| U25-C016 | R | \| Interpreter of this build \| 3.12.12 \| observed when the cell ran \| | observed value (platform.python_version); no test pins it (nor can it); 3.12.12 not asserted |
| U25-C017 | R | \| Platform of this build \| macOS-26.5.2-arm64-arm-64bit \| observed when the cell ran \| | observed value (platform.platform); no test pins it |
| U25-C032 | S | because the builder renders the pages through a temporary server that stops when the build ends | explanation of builder behavior; only in paper/BROWSER_NOTES.md (observation of the build), no test or cited source |
| U27-C010 | R | a cubesat trade study across power, mass and attitude control | Description of the page's example; examples.md numbers are covered by other rows; no R-number here, but grouping power/mass/attitude control is pinned by tests/test_cubesat_model.py (WP18 R-7 partition test) - treat as scope statement; no gen/test pair for 'a trade study' as R. |
| U28-C003 | R | The output is `trilemma [0 1 2]` and then `[0.3  0.37 0.33]`. | exact printed output [0.3 0.37 0.33] at temperature 20 on make_frontier_data(300,3,random_state=0) is not pinned by any test (blocks are only executed); doctest in tensions.py uses 400 rows at tau=inf |
| U28-C004 | R | metrics 0 and 1 the designs lie on or just beyond a straight frontier, and the grey band marks those | test pins how the line and band are drawn on a 100-row table, not that these designs lie on or just beyond the frontier; data behaviour not pinned |
| U28-C008 | R | contend at the edge of the table: here all three, an n-lemma with n = 3, which the report names a | that all three contend with n=3 trilemma on this table is not pinned: doctest is 400 rows tau=inf, test_k1_is_a_single_report uses the same call only for type; naming rule is pinned by test_contending_set_recovers_planted_support |
| U28-C014 | P | Real attributes are rarely positive, larger-is-better and comparably scaled. | general statement about real attributes, no source and not worded as the author's experience; reword as judgment (reading) or drop |
| U33-C002 | L | Boyd and Vandenberghe, *Convex Optimization* [@boyd2004convex]: the notation used on these pages. | no reading_pass/prior_art row for boyd2004convex; the notation claim is the author's alignment, mark as reading or add an audit row |
| U33-C011 | L | Isometric log-ratio transformations for compositional data [@egozcue2003isometric] and principal | reading_pass n36 egozcue2003isometric verdict not accessible (title only); the fragment is just the title, narrow or accept as bibliographic |
| U33-C012 | L | component analysis of compositional data [@aitchison1983principal]: the neighbours of the chart. | aitchison1983principal (n34) and egozcue (n36) not accessible; 'neighbours of the chart' is the author's comparison, word as judgment (reading) or drop |
| U33-C017 | L | Data envelopment analysis [@charnes1978measuring]: a frontier estimator from efficiency | reading_pass n16 charnes1978measuring verdict not accessible; row says only title-level scoring is kept |
| U35-C006 | S | a judgement about the problem, and a wrong sign is not detected: the fit finds a surface for the | No test or doc claim backs that a wrongly oriented fit is undetected; tests only reject orientation entries other than +1/-1 |
| U36-C035 | R | Over the four resamples the smallest exponent stays within 0.07 to 0.08 at K = 3 and ranges from | K=3 smallest exponent 0.08 0.08 0.07 0.07 reproduced by running the page's block; not pinned by any test. |
| U37-C004 | R | all three off-diagonal cells are negative, and all three metrics are outlined as contending. | no generator/test pins the signs of this figure's off-diagonals or outlines (tests only check images exist/differ; -0.38..-0.62 only in WP8a review note) |
| U42-C005 | R | the coloured dots are at the frontier. | Coloured dots are those with \|log V\| < near=0.2 (near the fitted reference surface, not the Pareto frontier); no test pins which dots are coloured; test_site only checks the caption text |
| U42-C012 | R | The black arrow is the same step in each pane: a design's energy differential to the fitted reference surface. | The arrow is drawn as one uniform scaling in each pane in the generator, but no test asserts the arrow or its equality across panes (test_figure1_has_three_panes checks titles and words only) |
| U43-C006 | R | Status: WP0 (setup) complete; the package code arrives in later work packages. | Stale: states the package code is yet to arrive, but src/hyperbolic_trade_space (estimator, solvers, plotting, etc.) exists with tests; no WP status backing; update or drop |

## Claims narrowed (broader than their backing, not mathematics)

| Id | Kind | Fragment | How it is broader (narrow to this) |
|---|---|---|---|
| U02-C019 | R | On this case, with the number of designs and of metrics, dominance stops shortlisting: its nondominated set nears the whole table. | Counts vary with number of metrics only (671/706 = 95% at 10 attributes, but 146 (21%) at 4 and 8 at 2); no run varies the number of designs; 'nears the whole table' holds at 10 attributes only. |
| U02-C028 | R | On a cubesat model coupling power, mass and attitude control the facets separate contending sets that one facet blends | Tests pin the K=1 six-metric contending set and only the largest K=3 facet's set (test_paper only checks the phrase 'different contending sets' appears); nothing asserts the three K=3 sets are separated sub-sets of what K=1 blends, nor the power/mass/attitude coupling. |
| U03-C002 | L | Returns no coordinate system and no exponents | audit records only what Pareto methods return (nondominated sets, rows 12-13); that they return no coordinate system and no exponents is the paper's own contrast (prior_art differs cell), not read in any source |
| U03-C005 | L | The Cobb-Douglas production form, and the Shephard distance function | Shephard half: row 24 (partly; table sentence supported, publisher description only); Cobb-Douglas half: row 23 not accessible, identification stated as the paper's own |
| U03-C006 | L | Estimates frontier production functions \| A one-sided criterion on log-linear residuals | 'Estimates frontier production functions' backed by row 27 (supported: LP/QP, COLS, ML, stochastic frontiers); 'one-sided criterion on log-linear residuals' (a shared feature) is not recorded in row 27 (log-linear form not noted) |
| U03-C007 | L | A one-sided criterion on log-linear residuals | our half backed (at tau=inf all rows on or below the fit, V.max()<=1; slack nonnegative L5.4); the literature half 'log-linear residuals' not recorded in row 27 (one-sided error is) |
| U03-C009 | L | PCA of compositional data \| an isometric logratio chart | rows 34-36 not accessible (titles only, no supported verdict) for 'PCA of compositional data' and 'isometric logratio'; only our chart's orthonormality (L8) is backed |
| U03-C027 | L | where DEA obtains weights unit by unit | 'weights obtained from the data' read (row 17), but 'unit by unit' (a weight set per unit) appears only in a secondary paraphrase of Charnes (row 16, not accessible); rows 20-21 say self-chosen weights not named in the abstracts |
| U03-C037 | L | The chart is in the spirit of log-ratio coordinates for compositional data | rows 34-36 not accessible, 'in the spirit of' is the author's comparison; only the orthonormal sum-zero chart (L8) is backed, not any property of log-ratio coordinates |
| U06-C010 | R | halving or doubling it leaves the contending sets unchanged | 'it' is the target fraction; the test asserts only n_lemma == shared-with-baseline per variant (variant set within baseline's), not equality of sets; printed table does show identical sets in both regimes |
| U06-S01 | R | the case needs three facets | K=3 facet table is pinned, but 'needs' is broader: the paper itself says three facets is the analyst's choice and mean slack cannot choose K |
| U12-C004 | S | Feasibility removes designs that do not settle, saturate the momentum budget or discharge the battery too deeply. | feasibility flags are settled, power_ok, momentum_ok plus all attributes positive; dod_ok (battery depth) is not a flag, and power_ok (available power) is not named in the sentence |
| U13-C003 | R | At K = 1 the fit reports one tension at the balanced point | one facet at K=1 is by construction (706 rows), but 'at the balanced point' is not asserted by any test or defined in the register; nothing pins a single tension row |
| U13-C007 | R | At K = 3 the tension separates into three facets with different contending sets | tests pin the K=3 facet sizes (6,6,7) and the largest facet's set start only; that the three sets differ is not asserted |
| U13-S01 | R | the finding: their sets differ | 'the finding: their sets differ' (the K=3 sets differ from one another and from K=1) is not asserted; sizes and one facet's set are pinned |
| U15-C001 | R | Every figure, table and reported number comes from a call into a tested module | Backed for figures and tables (one reproduction row each, structural test). 'Every ... reported number' is broader: numbers typed in prose are not shown to be generated, and no test pins that; the row test checks rows exist, not that each call lies in a tested module. |
| U15-C002 | R | gives the pinned toolchain, the environment of record, the commands and one row per item | Toolchain, commands and one row per figure/table are generated and tested; 'the environment of record' (F.2) is still a placeholder shell awaiting the container package, so that part is unbacked. |
| U17-C003 | L | in a process modelled on the harness described in [@zargham2026incose] | Audit row paper/reading_pass.yaml n=56 read only the Crossref abstract (LLM assistance regulated by deterministic testing, human sign-off) and its verdict is 'accessible (own work)', status supervisor, not 'supported'; 'modelled on the harness' is the author's own process claim. |
| U17-C004 | L | whose deterministic checks and named human approver are the verification mechanism this paper inherits | Same row n=56: abstract matches 'deterministic checks and named human approver', but the verdict is not 'supported' (listed for the supervisor) and 'the verification mechanism this paper inherits' goes past what the abstract states. |
| U20-C001 | S | an input of the fit; the fit sees attributes and metrics only | Contract s3 backs 'configuration columns not fitted, carried as covariates' and HyperbolicTradeSpace.fit takes metrics; but TradeSpaceRegressor.fit(X, y) takes configurations as X (predictive.py), and 'the fit sees attributes' conflicts with C004 (the fit sees metrics; attributes only via the separate conditioning step). Narrow to: configuration is not an input of the frontier fit; the fit sees metrics. |
| U20-S01 | S | an exponent below EPS_ZERO_EXPONENT | code and docstrings treat an exponent 'at or below' EPS_ZERO_EXPONENT (1e-12, pinned at test_estimator.py:511) as numerically zero; glossary says 'below'. Wording only: change to 'at or below' |
| U21-C040 | S | the fit minimizes the mean slack | Tests pin the objective as the mean slack and a non-increasing history, not that the fit attains the minimum: alternation with restarts reaches a local one, L16 does not prove convergence, and the tangent step is not monotone. |
| U22-C005 | S | \| settling time \| `adcs_sim.py` \| `simulate_adcs` \| measured: on the integrated slew \| | file and name pinned (name occurs in file); 'measured: on the integrated slew' is a typed label, not asserted by a test |
| U22-C006 | S | \| pointing error \| `cubesat_model.py` \| `pointing_error_deg` \| computed: pointing budget \| | file and name pinned; 'computed: pointing budget' is a typed label, not asserted by a test |
| U22-C007 | S | \| total mass \| `cubesat_tradespace.sysml` \| `MassAccounting` \| computed: accounting \| | name MassAccounting occurs in the sysml and a mass identity test exists; 'computed: accounting' label itself is typed, not asserted |
| U23-C065 | R | so a relative change of 1e-12 in a design variable can move them by up to half a second, and by much more where the error trajectory grazes the settling band | the gap G-17 ledger records times moving by at most 0.49 s except design 763 (33.44 s to 12.53 s), which supports 'up to half a second' and 'much more where it grazes'; the sentence is a fixed string in stability() and no test asserts the 0.5 s figure against the results file (test_cubesat_model asserts atol=0.5 on regenerated data only) |
| U23-C082 | S | The diagnostic `conditioning_` of the estimator is the smallest eigenvalue of the restricted Hessian at each facet's fit | eigenvalue value is asserted at K=1 only; at K>1 the test checks shape and positivity, not the value; also the Hessian is restricted to the participating exponents, which the sentence omits |
| U23-C084 | S | It is read only and takes no part in a status. | read only is pinned at K=1 (exponents equal the reference solve); 'takes no part in a status' holds by code order (termination_ is set before _conditioning) but no test asserts the status is independent of it |
| U23-C097 | R | At the exact maximum the fit of each of these tables stops without a margin (`stationary_without_margin`) or at the iteration cap, depending on the platform | the sentence is hard-coded in the generator, not computed; test_r1_planted_certificates accepts either status for a zero-margin seed but pins only seeds 1, 3, 16 (and at most 6) as zero-margin, seed 8 is not pinned; 'depending on the platform' rests on the G-10 ledger and CI run ids, not on a test |
| U24-C002 | R | at $\tau=38.10$ it is 0.096, 0.261, 0.382 for $K=1,2,3$ (primary) | k3-cubesat.md fixed-tau table matches; test pins only tau 38.10 and last-row fixed-tau fraction >0.25, not 0.096/0.261/0.382 (K=1 0.096 pinned in test_case RECORD) |
| U24-C003 | R | and 0.104, 0.204, 0.338 at $\tau=41.72$ (stock) | table matches k3-cubesat.md; test pins only tau 41.72 and fixed-tau K=3 fraction >0.25, not 0.204/0.338 |
| U24-C013 | R | Cubesat `conditioning_` (M3): $K=1$ 1.12 (primary), 0.522 (stock) | committed output (staleness test) pins 2 digits only: 1.1 and 0.52; the 3-digit 1.12 and 0.522 are not printed or pinned |
| U24-C022 | R | 1.023 (N=4000, sd of the shift 0.0014), 0.992 (N=40000, sd of the shift 0.0012), five seeds each | test pins N=40000, one seed, ratio within 5e-2; N=4000 (1.023), the sds and the five-seed means are not generated or tested |
| U24-C026 | R | For the row $(1,2,3)$ the convention's objective $w\cdot u_1$ is 0.597 against the infimum 0 at the vertex | arithmetic checked: log(6)/3=0.5973, infimum 0; test pins w=1/3 and beta=w.u (score 0) but no test or generator prints 0.597 or the infimum |
| U24-C040 | R | step B 60/60 (median error at most 0.018 at $\tau=\infty$, at most 0.037 at $\tau=50$) | 60/60 pinned; medians 0.018 and 0.037 are spike figures (oracle.txt), generator prints largest error 0.001 (inf) and 0.037 (50), no medians, no test |
| U24-C048 | R | Cubesat: smallest near-frontier count of a $K=3$ facet is 17 | test pins primary K=3 near-frontier counts [17,33,126]; stock not asserted; claim says cubesat generally |
| U24-C052 | R | Half-steps in which the objective rises: refit step B 0.000 at $\tau=\infty$ and 50; step D 0.501 and 0.349 | B zero rise pinned; D's 0.501 and 0.349 only in spike-objective README table 1a (no test; tangent test says only not monotone) |
| U24-C063 | R | Mean slack at fixed $\tau$ is about a quarter of $K=1$'s, at re-selected $\tau$ 0.117 against 0.204 (primary) and 0.093 against 0.131 (stock) | re-selected objectives 0.117/0.204, 0.093/0.131 pinned; 'about a quarter at fixed tau' (0.0529, 0.0326) not pinned by any test |
| U24-C070 | R | $\gamma$ at or below $10^{-9}$ on seeds 1, 3, 8, 16 and above it on the other 16 | tests pin 16 seeds above EPS_FEAS=1e-9 and {1,3,16} among the zero-margin; seed 8 as the fourth is not asserted |
| U24-C075 | S | Platform: facet numbering and an emptied facet differ by platform | platform dependence recorded in reviews; tests only compare after matching, none asserts the difference |
| U24-C076 | S | The Linux CI run 42540318424 resolved one tied row differently from macOS | WP13-decisions records Linux-only tied-row failures but not run id 42540318424; id unverifiable in repo |
| U24-C078 | R | run 42541322671 on Linux stopped a tied seed at the iteration cap where macOS reports stationary without margin | WP13-decisions records a tied tau=inf seed stopping at the cap on Linux, not run id 42541322671; id unverifiable in repo |
| U24-C084 | R | Objective stable over seeds in the cubesat record (primary 0.11733 for seeds 0 to 4) | test pins objective_ 0.1173 (abs 6e-5) for the default seed only; stability over seeds 0 to 4 and the 5th digit rest on k3-cubesat.md and the spike table, not a test (test_k_terms_case runs seeds=[0]) |
| U24-C100 | R | Stock cubesat $K=3$, $\tau=162.78$: `objective_` 0.09287 on four seeds and 0.11427 on one | 0.09287 on four seeds and 0.11427 on one match spike-certificates README table 3 and k3-cubesat.md; the test pins only the seed-0 value 0.0929 (abs 6e-5), not the four/one split or 0.11427 |
| U24-C107 | R | Passing restarts exist among five on seeds 3 and 8 | spike README: passing restarts among five on seeds 3 and 8 at tau=inf; at tau=50 the default step has 0 on both (step D has 3 and 5), and WP9-review G3-1 says the counts hold only at tau=inf; sentence carries no scope; no test |
| U24-C108 | R | and the mean-slack selector does not choose them. | reviewer's third review says the mean-slack selector does not pick them (seed 8 at tau inf, default step, lost at 20 and 50 restarts); scope of tau and step not stated in the sentence and no test |
| U24-C112 | R | Planted fits: maximum facet gap $\le10^{-12}$ after the polish (SLSQP alone left $4.7\times10^{-5}$ at $\tau=50$, none of 60 facets certified at $10^{-8}$) | max gap <= 1e-12 is asserted on 20 seeds; 'SLSQP alone left 4.7e-5, none of 60 facets certified at 1e-8' is spike-certificates table 4 only (the polish test checks seed 0 above 1e-8, not 4.7e-5 or all 60) |
| U24-C114 | R | Cubesat $K=3$ certified: gap $2.6\times10^{-14}$, $\gamma=2.2\times10^{-4}$, radius $1.8\times10^{-5}$ (primary) | gamma 2.2e-4 and radius 1.8e-5 pinned (abs 5e-7); the gap 2.6e-14 is pinned only as < 1e-12 and appears in no record (k3-cubesat.md gives 1.1e-14 for primary K=3 seed 0): number unverified, likely wrong |
| U24-C115 | R | gap $1.1\times10^{-14}$, $\gamma=1.5\times10^{-3}$, radius $1.2\times10^{-4}$ (stock) | gamma 1.5e-3 (0.001487) and radius 1.2e-4 (0.000119) pinned; gap 1.1e-14 pinned only as < 1e-12 and k3-cubesat.md gives 9.1e-15 for stock seed 0 (1.1e-14 is seed 2): number does not match the record |
| U24-C116 | S | The status states which of the three levels the fit meets: descent always, stationarity per facet when the gap is small, local optimality of the fixed assignment only when `certified`. | statuses and certified conditions are tested; 'descent always' holds for step B unpenalized (monotone history tested) but not for the tangent step or the penalty (status not_applicable; ledger G-8 half-steps rise), and guard_stop/iteration_cap are not mentioned |
| U24-C118 | R | a relative change of $10^{-12}$ in a design variable moves the time by a small fraction of a step | an assumption the same row's evidence contradicts for design 763 (slew time 33.44 s to 12.53 s); no measurement of the deviation as a fraction of the step is recorded or tested |
| U24-C123 | R | all flags and feasibility verdicts, and the count 671 of 706 | count 671 of 706 is in sensitivity.json (identical, 671/706) and test_case.py:241 asserts 671 on committed data; but flags and feasibility verdicts (0 changed) appear only in swap-evidence.md and the report, with no test pinning them. |
| U24-C124 | R | the nondominated counts on reduced views (146 to 145, 8 to 7, stock 157 to 158) | values match sensitivity.json (146 to 145, 8 to 7, stock 157 to 158); the test pins the primary ranges only, nothing pins stock 157 to 158. |
| U24-C125 | R | the regime comparison (effective sample size 16.2 printed 16.0 or 16.1, near-frontier count 51 to 52, stock fraction above 0.104 to 0.105, five association values by 0.01) | values match (n_eff 16.2 vs 16.0/16.1 per swap-evidence per-seed table, near-frontier 51 to 52, stock frac 0.1038 to 0.1051, five primary association pairs move, spread at most 0.007 so 'by 0.01' is the printed step); no test pins these min/max values, only committed-inside-range. |
| U24-C126 | R | the paper prints those quantities as ranges over the five regenerations | a test pins ranges for nondominated counts, K=3 facet shares and n_eff in the temperature sentence; not every listed quantity (near-frontier, stock fraction, associations) has a test that the paper prints its range. |
| U25-C003 | S | \| Package manager \| uv 0.9.18 \| uv.lock (format revision 3) \| | test pins only the prefix '\| Package manager \| uv '; 'uv 0.9.18' is the local uv --version at run time (matches Dockerfile ARG UV_VERSION); revision 3 matches uv.lock |
| U25-C004 | S | \| Locked packages \| 176 \| uv.lock \| | stale: uv.lock now has 178 packages (9ec8c4a added pytest-xdist); committed output says 176; test checks the generator, not the committed count |
| U25-C011 | S | \| hyperbolic-trade-space \| 0.0.1 \| pyproject.toml; this repository \| | 0.0.1 matches pyproject.toml but no test asserts the project row |
| U25-C018 | R | \| Commit \| f6c5df378b94de1c7d878de056447a448971eeba \| observed when the cell ran, in a checkout \| | test checks only form of the commit (40 hex, not found or empty); the hash is an observation, and the 'in a checkout' note is covered by the git-absence test only |
| U25-C019 | S | The tests assume a git checkout of the repository: a few read its history | 'a few read its history' true (test_v2_data, test_experiments use git log/diff); but test_cr18 only checks the prose; no-checkout behavior is not tested |
| U25-C020 | S | in a copy made without it they skip with a reason. | narrower truth: without history test_v2_data fails explicitly (pytest.fail) or passes silently (ordering check), test_experiments fail on git diff/log; none skip with a reason |
| U25-C021 | S | The last row of the table regenerates one row of F.4, the cells it needs included. | wrong row: the last row of the commands table is the myst build; regenerate_row is second to last (probably 'the penultimate row'); the script and test (two rows) are fine |
| U25-C022 | S | \| uv sync --locked \| install the locked environment \| exits 0 \| | CI runs the command; 'exits 0' is not a test assertion; test_container only checks the Dockerfile contains it |
| U25-C023 | S | \| uv lock --check \| check that the lock matches pyproject.toml \| exits 0 \| | lock_cmd 'uv lock --check' is in the contract and CI; exit 0 not asserted by a test |
| U25-C024 | S | \| uv run pytest \| run the test suite, doctests included \| all tests pass \| | CI runs uv run pytest; the pass is the CI result, not a test; doctests enabled in pyproject (not re-verified here) |
| U25-C025 | S | \| uv run python -m derivation.run \| run the chain L1 to L17 \| every lemma reports PASS \| | derivation/run.py prints PASS per lemma and 'ALL LEMMAS PASS'; the named test runs main() == 0 and checks ALL LEMMAS PASS and L1 -> L17; 'L1 to L17' is generated from lemma files (last = 17) |
| U25-C026 | S | \| uv run python -m derivation.proofmap \| check the proof map against the scripts \| exits 0 \| | only that derivation/proofmap.py exists and the command is listed; 'exits 0' not tested by name |
| U25-C027 | S | \| uv run python paper/execute_notebooks.py \| execute both notebooks from a clean kernel and write the outputs \| exits 0; the outputs are unchanged when the data and the seeds are: `git diff --stat -- paper/paper.ipynb paper/supporting_material.ipynb` then shows only the commit and platform lines of the toolchain table, and `PAPER_EXECUTE=1 uv run pytest tests/test_paper.py -k clean_kernel` compares every other text output of a fresh run with the committed one \| | clean_kernel test (gated PAPER_EXECUTE) compares all text outputs but skips tab-F-toolchain entirely; 'git diff --stat shows only commit and platform lines' is untested (Node, interpreter lines also observed) |
| U25-C028 | S | \| uv run python paper/regenerate_row.py ROW \| regenerate one row of the table in F.4 (ROW is its first column): runs the cells that row needs and prints the table or saves the figure, writing nothing in the repository \| prints the table, equal to that cell's committed output, or names the figure file \| | test pins equality with committed output for two table rows (tab-A-register, tab-F-commands) and SystemExit for an unknown row; 'writes nothing in the repository' and figure-saving untested |
| U25-C029 | S | \| cd paper && uv run myst build --html \| build the paper as a static site, written to paper/_build/html \| exits 0, with no error reported; it prints a line that a server started on a local port, because the builder renders the pages through a temporary server that stops when the build ends \| | gated (PAPER_BUILD) test asserts returncode 0, no error mark, index.html exists; the server-line remark rests on paper/BROWSER_NOTES.md (observation) only |
| U25-C030 | S | shows only the commit and platform lines of the toolchain table | test skips tab-F-toolchain wholly, so it does not show that only the commit and platform lines differ; the git diff claim is untested |
| U25-C054 | S | \| tab-C-planted_example \| `planted_example()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-C-planted_example of supporting_material.ipynb \| | Row and call pinned; Reads column is the CASE_DATA default but the function builds synthetic data with make_frontier_data, reads no CSV |
| U25-C066 | S | \| tab-D-stability \| `stability()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-stability of supporting_material.ipynb \| | Row and call pinned; Reads column is the CASE_DATA default but the function reads the committed stability records (paper_stability), not only the CSVs |
| U25-C067 | S | \| tab-D-conditioning_diagnostic \| `conditioning_diagnostic()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-conditioning_diagnostic of supporting_material.ipynb \| | Row and call pinned; Reads column is the CASE_DATA default but the function Reads default CASE_DATA not verified for this function |
| U25-C068 | S | \| tab-D-own_rows_refit \| `own_rows_refit()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-own_rows_refit of supporting_material.ipynb \| | Row and call pinned; Reads column is the CASE_DATA default but the function runs make_frontier_data seeds, reads no CSV |
| U25-C069 | S | \| tab-D-planted_recovery \| `planted_recovery()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-planted_recovery of supporting_material.ipynb \| | Row and call pinned; Reads column is the CASE_DATA default but the function runs make_frontier_data seeds, reads no CSV |
| U25-C070 | S | \| tab-D-mean_slack_fixed \| `mean_slack_fixed()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-mean_slack_fixed of supporting_material.ipynb \| | Row and call pinned; Reads column is the CASE_DATA default but the function reads the committed stability ledger, not only the CSVs |
| U26-C003 | R | Its entries are the works and families most immediately relevant to the method | Tests pin only that outline families have entries; "most immediately relevant" is the author's selection judgement, not checked; reword as selection or back by reading. |
| U26-C007 | R | A sentence was kept where the verdict is supported | No test asserts supported implies kept, and rows 45 and 46 are supported yet reworded (other half of the sentence); narrow to "kept where supported, except where another part was reworded". |
| U26-C011 | R | checked each sentence of {numref}`section %s <sect-problem>` and {numref}`section %s <sect-prior-art>` | No test or mapping shows that every attribution sentence of the two sections (plus L11 sketch, process paragraph) has a row; only the 56 rows exist; completeness is unchecked. |
| U27-C011 | S | The [project page](../) links the paper, which is where the argument for the method is made | Link '../' resolves (test_site), but test_site asserts the paper page says 'The paper is in preparation' so 'links the paper' is true only as a link to the paper route; 'where the argument is made' is intent. |
| U28-C002 | R | The table below is synthetic: 300 designs scored on 3 metrics, all positive and larger-is-better, | test pins positivity for a 500x4 table, not this 300x3 call (planted frontier yes); the run block is only executed by test_docs::test_runnable_blocks_execute; no test pins 300 designs/3 metrics here |
| U30-C001 | S | Generated from the numpydoc docstrings of the public names. | Page is mkdocstrings ::: directives for exactly the contract public names (test_site); but numpydoc style is asserted for only 3 names (HyperbolicTradeSpace, select_temperature, tension_report), not all public names |
| U32-C026 | S | The argument itself lives in the project repository, in the derivation scripts under `derivation/` | derivation scripts exist; the sentence goes on to name a README there and derivation/ has no README |
| U33-C001 | S | scikit-learn and its API design [@pedregosa2011scikit; @buitinck2013api]: the conventions the | S half backed (parametrize_with_checks, empty expected failures); the two cited works have no audit row in prior_art.yaml/reading_pass.yaml, so attributing the conventions to them is unbacked |
| U33-C006 | L | [@hoburg2016data] is the source of the multi-term fit. | audit supports only the abstract's content; 'the source of the multi-term fit' attributes the package's fit to it, beyond what was read |
| U35-C015 | S | few extreme designs would dominate; `None` keeps the pure power law. | Only invertibility with scaler=None is tested; no test asserts log_offset_=0, log_scale_=1 (pure power law), only the docstring says it |
| U35-C032 | S | single-term fit; a multi-term fit is not a monomial in the attributes. | Not-a-monomial for K>1 is the posynomial sum (L10); the code raises ValueError for n_terms != 1 but no test asserts it (test_pullback_errors covers width and unfitted only) |
| U36-C021 | P | for real data the default 0.10 is a common start. | Default 0.10 pinned and used in the case studies; 'a common start' (field practice) is unsourced and not worded as the author's own practice. |
| U37-C013 | S | (`threshold`, default 1e-3); an exponent at or below 1e-12 is numerically zero. | default 1e-3 only exercised via nan rows, not asserted as the default; the 1e-12 numerically-zero cutoff is in the glossary only, no test |
| U38-C007 | S | With two metrics the chart is the log plane itself: | the chart (Z, log V) is a linear re-coordinatization of the log plane (log V = w.u - beta), not the log plane itself; the plot_log_plane axes are the log metrics |
| U38-C023 | R | Figure 4. One facet in the log plane: the line is V = 1, and the band below it has width 1/tau. | the line being V=1 (w.u=beta) and a grey band are tested; band width 1/tau (plotting _band default) is not pinned by any test |
| U38-C032 | S | Each accepts an optional `ax` and returns a matplotlib `Axes`; nothing calls `plt.show()`. | ax/Axes return tested for several plots; 'nothing calls plt.show()' is stated only in the module docstring (no test); plot_tensions given a list returns a list of Axes |
| U38-C034 | S | For a multi-term fit the plots draw every facet | plot_log_plane draws a facet only where it has weight on both metrics (tested), so not literally every facet |
| U40-C011 | S | - `stationary_without_margin`: the same, with margin at most `eps_feas` or an empty facet. Levels 1 | margin<=eps_feas branch pinned (status stationary_without_margin, seed 1); the empty-facet branch is pinned only as 'status != certified' with n_empty==1; code in _termination |
| U40-C016 | S | `fit` warns (a `ConvergenceWarning` naming the status and the largest gap) for `uncertified`, | warning naming status and 'max facet gap' pinned for iteration_cap and guard_stop; no test produces uncertified and its warning (only _WARN_STATUSES in estimator.py) |
| U40-C018 | S | - `certified`: weighted gaps within `eps_kkt` and `min_curvature` above `eps_feas`, a strict local | L17.44 gives a strict local minimizer only at exact first-order conditions; L17 states a numerical tolerance on the gaps (eps_kkt) is not covered |
| U40-C019 | S | - `stationary`: the gaps hold, the curvature does not: a saddle or a flat direction. | pins gap<=eps_kkt with curvature < -1 (saddle) via soft_certificate, not the status string 'stationary'; 'flat direction' (curvature near 0) is not tested |
| U40-C020 | S | - `status`, `reason`, `n_iter`; `max_gap`, `gaps` (`nan` for an empty facet) and `shares`. | fields exist and gaps shape/max pinned; 'nan for an empty facet' is in the fixed_assignment_bound docstring and code, no test asserts nan gaps |
| U40-C027 | S | The smallest eigenvalue of the restricted Hessian at each facet's fit, over the participating | value pinned for a one-term fit with all exponents participating (Helmert-restricted eigenvalue); the restriction to participating exponents above 1e-3 is pinned only as a constant and a finite sparse case |
| U40-C034 | R | On this table at tau = 50, `gamma` is 0.0020 against a band of 0.02 and a median margin of 0.21: | I ran it: gamma 0.002017, band 0.02, median margin 0.205 (0.21); the page's block prints them but no test pins these values (test_docs only executes the block; test_r1 pins 1e-4<gamma<1e-2 on another table) |
| U40-C035 | R | level 3 holds, for perturbations well under the band. | L13 guarantees score changes below gamma/2 = 0.001 (5% of the 0.02 band); 'well under the band' is vague and the numbers are unpinned |
| U41-C022 | R | it recovers the planted facets in 16 or 17; failures are facets with | Generator and test pin 16 of 20 at both temperatures (seeds 1, 3, 8, 16 fail); '16 or 17' is broader: 17 comes only from the spike/review (seed 8 differs), not the pinned run |
| U41-C023 | R | five or six frontier rows. More restarts do not cure this | Pinned thinnest-facet frontier rows of the failures are 5, 6, 11, 5 (seeds 1, 3, 8, 16): seed 8 has 11, so 'five or six' is too narrow |
| U42-C017 | S | its guarantees. Each box carries a badge, derived, checked numerically or open; the red box | Backed for the badges on the paper's lemma blocks and the open-questions list; no test checks the map image paper-map.webp itself shows badges on each box or a red box of open questions |

## Per unit: the claims

Columns: id, kind, fragment (verbatim from the rendered text), pointer, verdict, disposition. A note follows for any claim that is not simply backed.

### U01: paper front (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U01-C001 | P | A trade study must produce an answer and a justification an accountable executive can follow. | reading | backed | keep |
| U01-C002 | P | Principal component analysis (PCA) is trusted as reproducible and interpretable, but explains | bib:jolliffe2016principal reading | backed | keep |
| U01-C003 | M | variance, not trade-offs. We explain tensions. | bib:jolliffe2016principal definition | backed | keep |
| U01-C004 | M | the data underlying the table, not the Pareto boundary, and gives the data a coordinate system; | lemma:L8 lemma:L11 glossary:chart | backed | keep |
| U01-C005 | M | A reversible chart separates a design's position along | registered:C010 lemma:L8 glossary:chart | backed | keep |
| U01-C006 | M | the surface from its energy differential, its level relative to the surface. Each facet reports | registered:C009 lemma:L8 glossary:energy-differential | backed | keep |
| U01-C007 | M | Modelling a single n-lemma fits a monomial, which transforms into a convex program and is solved directly; when | lemma:L10.9 lemma:L4.13 lemma:L4.24 test:tests/test_solvers.py::test_slsqp_agrees_with_lp | backed | keep |
| U01-C008 | M | several trade-offs are active at once the model is a posynomial, compatible with generalized | registered:C007 lemma:L10.7 lemma:L10.19 | backed | keep |
| U01-C009 | M | geometric programming (GGP), and the method may be generalized to any kernel that keeps that Note: Kernel generalization 'to any kernel that keeps that compatibility': no lemma, test or contract; documented extension only (CLAUDE.md); PM may reclassify as scope/intent or drop | none | unbacked | to the driver |
| U01-C010 | S | compatibility. Our implementation mirrors the structure of PCA as an unsupervised learning | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator test:tests/test_sklearn_compat.py::test_tags_only_through_sklearn_tags func:src/hyperbolic_trade_space/estimator.py::HyperbolicTradeSpace | backed | keep |
| U01-C011 | R | the fit identifies the trade-offs among the metrics those subsystems set. | gen:examples/adcs/case.py::facet_table test:tests/test_case.py::test_k3_facets_equal_the_primary_record test:tests/test_case.py::test_k1_contending_set_equals_the_record test:tests/test_case.py::test_subsystem_mapping_is_data_and_covers_every_attribute | backed | keep |

### U02: paper The decision problem (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U02-C001 | P | Decision analysis has two products: an answer, and a justification an accountable executive can follow and defend. | reading | backed | keep |
| U02-C002 | L | It seeks responsible choice among conflicting objectives [@keeney1993decisions] | bib:keeney1993decisions | backed | keep |
| U02-C003 | L | and clear conversation with the decision-maker [@howard1988decision] | bib:howard1988decision | backed | keep |
| U02-C004 | P | The justification is the hard product: the process turning much data into little must be recognized, reproducible, rigorous. | reading | backed | keep |
| U02-C005 | P | A trade study is a document: a grid, a table, a ranking by weighted criteria | reading | backed | keep |
| U02-C006 | L | a ranking by weighted criteria; surveys compare them [@baker2012survey] | bib:baker2012survey | backed | keep |
| U02-C007 | L | The weights are human judgments, susceptible to bias in trade studies [@smith2007ameliorating; @chilli2026decision] | bib:smith2007ameliorating bib:chilli2026decision | backed | keep |
| U02-C008 | L | Systems engineering is moving from document-based [@henderson2021value] to model-based practice [@madni2018model] | bib:henderson2021value bib:madni2018model | backed | keep |
| U02-C009 | P | but the computational alternatives are bespoke and opaque Note: 'computational alternatives are bespoke and opaque' is a general claim about the world; no audit row, source or reading marking; prior_art mbse row says nothing of bespoke/opaque. | none | unbacked | drop |
| U02-C010 | P | To displace it, a method must handle real data's scale, complexity and noise interpretably. | definition | backed | keep |
| U02-C011 | L | PCA reduces dimensionality and increases interpretability while minimizing information loss [@jolliffe2016principal] | bib:jolliffe2016principal | backed | keep |
| U02-C012 | M | But variance says where the data are free and nothing about trade-offs Note: About PCA's criterion vs trade-offs; no lemma step, no audit row (jolliffe row covers only dimensionality/interpretability/information loss); could be narrowed to the author's judgment (reading). | none | unbacked | to the driver |
| U02-C013 | M | Objectives may align in one region and oppose in another. Note: No lemma step states that objectives align in one region and oppose in another (L7 gives facet-specific elasticities, L10 the K-term model, neither says alignment); an existence claim about the model, unproved. | none | unbacked | to the driver |
| U02-C014 | M | The surface is not the Pareto boundary, and the table and its reading are views | definition lemma:L11.19 | backed | keep |
| U02-C015 | M | the chart, a reversible rewriting of the metrics as a position along the surface and a level relative to it | registered:C010 | backed | keep |
| U02-C016 | M | Each facet names the metrics that contend on it with elasticities | lemma:L7.5 glossary:elasticity glossary:contending-set | backed | keep |
| U02-C017 | S | Our implementation mirrors the structure of PCA as an unsupervised learning method for feature engineering | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples | backed | keep |
| U02-C018 | S | and the two chain: {ref}`Appendix D.16 <sub-d-16>` reads the principal directions | gen:paper/generate_results.py::pca_chain test:tests/test_paper.py::test_cr11_chaining_with_pca_is_worked_on_the_case_in_d16 | backed | keep |
| U02-C019 | R | On this case, with the number of designs and of metrics, dominance stops shortlisting: its nondominated set nears the whole table. Note: Counts vary with number of metrics only (671/706 = 95% at 10 attributes, but 146 (21%) at 4 and 8 at 2); no run varies the number of designs; 'nears the whole table' holds at 10 attributes only. | gen:examples/adcs/case.py::nondominated_counts test:tests/test_case.py::test_nondominated_counts_on_frozen_primary | broader than its backing | narrow |
| U02-C020 | R | Of 706 feasible cubesat designs, the nondominated sets hold 7 to 8 on 2, 145 to 146 on 4 and 671 on 10 attributes | gen:paper/generate_findings.py::nondominated_sentence gen:examples/adcs/case.py::nondominated_counts test:tests/test_case.py::test_nondominated_counts_on_frozen_primary test:tests/test_paper.py::test_generated_sentences_quote_the_ranges_from_the_results_file | backed | keep |
| U02-C021 | R | a range is the spread over five regenerations of the data under rounding-level perturbation | gen:paper/generate_findings.py::nondominated_sentence test:tests/test_paper.py::test_results_file_records_the_five_seeds_and_the_perturbation | backed | keep |
| U02-C022 | M | The fitted reference surface is the unit level set of a degree-one weighted geometric mean, not the Pareto boundary | lemma:L1.5 lemma:L1.6 glossary:invariant-value glossary:fitted-reference-surface glossary:pareto-boundary | backed | keep |
| U02-C023 | M | The one-facet fit is a geometric program, convex in the logarithmic variables | lemma:L4.23 lemma:L4.24 glossary:geometric-program | backed | keep |
| U02-C024 | M | its exponents are elasticities and its chart is reversible | lemma:L7.5 lemma:L8.14 glossary:elasticity glossary:chart | backed | keep |
| U02-C025 | M | With one term the posynomial extension is the monomial, and a maximizer of V is Pareto-efficient Note: K=1 reduction is L10.9 (backed for the model). 'A maximizer of V is Pareto-efficient' is broader than L11: weakly efficient always (L11.18), efficient only when every w_j > 0 (L11.19); section 3 of the paper words it 'with positive exponents'. Same wording as registered C018. | lemma:L10.9 lemma:L11.18 lemma:L11.19 | broader than its backing | to the driver |
| U02-C026 | M | The several-facet fit, not convex in the terms, has three levels of guarantee and a stopping declaration Note: Nonconvexity is shown only for the soft objective on an exact small instance (L16.37), not in general nor for the sharp fit; three levels are registered C020; 'stopping declaration' is the Termination status of the interface contract, not a lemma step. | lemma:L16.37 lemma:L15 lemma:L12 lemma:L13 lemma:L14 registered:C020 file:work-packages/interface-contract.md | broader than its backing | to the driver |
| U02-C027 | M | a soft fit has a second-order certificate | registered:C011 | backed | keep |
| U02-C028 | R | On a cubesat model coupling power, mass and attitude control the facets separate contending sets that one facet blends Note: Tests pin the K=1 six-metric contending set and only the largest K=3 facet's set (test_paper only checks the phrase 'different contending sets' appears); nothing asserts the three K=3 sets are separated sub-sets of what K=1 blends, nor the power/mass/attitude coupling. | gen:examples/adcs/case.py::facet_table test:tests/test_case.py::test_k3_facets_equal_the_primary_record test:tests/test_case.py::test_k1_contending_set_equals_the_record | broader than its backing | narrow |

### U03: paper Prior art, by family (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U03-C001 | L | Returns a nondominated set of designs | bib:zitzler1999multiobjective bib:deb2002fast file:paper/reading_pass.yaml | backed | keep |
| U03-C002 | L | Returns no coordinate system and no exponents Note: audit records only what Pareto methods return (nondominated sets, rows 12-13); that they return no coordinate system and no exponents is the paper's own contrast (prior_art differs cell), not read in any source | file:paper/reading_pass.yaml file:paper/prior_art.yaml | broader than its backing | narrow |
| U03-C003 | L | Evaluates the relative efficiency of each decision-making unit | bib:banker1984some bib:charnes1978measuring file:paper/reading_pass.yaml | backed | keep |
| U03-C004 | M | A one-sided envelope of the data, a score per unit \| One exponent vector per facet Note: 'One exponent vector per facet' is backed (L10.19 one theta_k per monomial; exponents_ shape (K,d)); the DEA half 'a one-sided envelope of the data' is not attributed: row 17 says not in the abstract, row 16 not accessible | lemma:L10.19 glossary:exponent-vector glossary:facet test:tests/test_estimator.py::test_n_terms_above_one_is_implemented file:paper/reading_pass.yaml | broader than its backing | to the driver |
| U03-C005 | L | The Cobb-Douglas production form, and the Shephard distance function Note: Shephard half: row 24 (partly; table sentence supported, publisher description only); Cobb-Douglas half: row 23 not accessible, identification stated as the paper's own | bib:shephard1970theory bib:cobb1928theory file:paper/reading_pass.yaml | broader than its backing | narrow |
| U03-C006 | L | Estimates frontier production functions \| A one-sided criterion on log-linear residuals Note: 'Estimates frontier production functions' backed by row 27 (supported: LP/QP, COLS, ML, stochastic frontiers); 'one-sided criterion on log-linear residuals' (a shared feature) is not recorded in row 27 (log-linear form not noted) | bib:battese1992frontier file:paper/reading_pass.yaml | broader than its backing | narrow |
| U03-C007 | L | A one-sided criterion on log-linear residuals Note: our half backed (at tau=inf all rows on or below the fit, V.max()<=1; slack nonnegative L5.4); the literature half 'log-linear residuals' not recorded in row 27 (one-sided error is) | bib:battese1992frontier lemma:L5.4 test:tests/test_estimator.py::test_fit_invariants file:paper/reading_pass.yaml | broader than its backing | narrow |
| U03-C008 | L | Finds uncorrelated components that successively maximize variance | bib:jolliffe2016principal file:paper/reading_pass.yaml | backed | keep |
| U03-C009 | L | PCA of compositional data \| an isometric logratio chart Note: rows 34-36 not accessible (titles only, no supported verdict) for 'PCA of compositional data' and 'isometric logratio'; only our chart's orthonormality (L8) is backed | lemma:L8 bib:aitchison1983principal bib:egozcue2003isometric file:paper/reading_pass.yaml | broader than its backing | narrow |
| U03-C010 | L | Geometric programming with generalized posynomials \| The model class, the K > 1 refit scheme | bib:boyd2007tutorial bib:magnani2009convex lemma:L16 glossary:generalized-posynomial file:paper/reading_pass.yaml | backed | keep |
| U03-C011 | M | this method fits an envelope, the one-sided boundary of the data Note: one-sided boundary holds at tau=inf and K=1 (frac_above_==0, V.max()<=1); at finite temperature rows lie above V=1 by construction (glossary fitted-reference-surface) and at K>1 the facets are not supporting planes | glossary:supporting-envelope glossary:fitted-reference-surface test:tests/test_estimator.py::test_fit_invariants test:tests/test_tuning.py::test_several_terms_unreachable_target_says_what_to_try | broader than its backing | to the driver |
| U03-C012 | L | PCA in an implicit feature space | bib:schoelkopf1998nonlinear file:paper/reading_pass.yaml | backed | keep |
| U03-C013 | L | Value-focused broad exploration of design alternatives | bib:ross2005tradespace file:paper/reading_pass.yaml | backed | keep |
| U03-C014 | S | this method fits and reports a coordinate system and a score | test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples | backed | keep |
| U03-C015 | L | Decision analysis with a normative versus descriptive distinction | bib:howard1988decision file:paper/reading_pass.yaml | backed | keep |
| U03-C016 | M | The weights are fitted from the data's edge, not elicited | test:tests/test_estimator.py::test_interior_density_insensitive_at_tau_inf_and_large_tau lemma:L3 | backed | keep |
| U03-C017 | L | MBSE centred on the system model as the sole source of truth | bib:madni2018model file:paper/reading_pass.yaml | backed | keep |
| U03-C018 | L | Pareto methods return a nondominated set and find its members by scalarization | bib:miettinen1999nonlinear bib:ehrgott2005multicriteria file:paper/reading_pass.yaml | backed | keep |
| U03-C019 | L | evolutionary algorithms generate such sets [@zitzler1999multiobjective; @deb2002fast] | bib:zitzler1999multiobjective bib:deb2002fast file:paper/reading_pass.yaml | backed | keep |
| U03-C020 | R | Dominance is a hard comparison that stops discriminating, on this case, as metrics are added | gen:paper/generate_findings.py::nondominated_sentence test:tests/test_paper.py::test_cr7_16_the_first_screen_says_what_scales_and_keeps_the_three_objects_apart test:tests/test_paper.py::test_generated_sentences_quote_the_ranges_from_the_results_file | backed | keep |
| U03-C021 | S | while the fit returns an exponent vector per facet, a band of near-frontier designs and an effective sample size | test:tests/test_estimator.py::test_fit_invariants test:tests/test_estimator.py::test_k_terms_attributes_conventions test:tests/test_estimator.py::test_n_terms_above_one_is_implemented | backed | keep |
| U03-C022 | M | a maximizer of V with positive exponents is Pareto-efficient | lemma:L11.17 lemma:L11.19 glossary:invariant-value | backed | keep |
| U03-C023 | M | the theorem gives efficiency of a maximizer, not the converse | lemma:L11.17 lemma:L11.19 | backed | keep |
| U03-C024 | L | It scores each unit against the data by mathematical programming, with weights obtained from the data | bib:banker1984some file:paper/reading_pass.yaml | backed | keep |
| U03-C025 | L | a super-efficiency variant ranks efficient units against a reference technology spanned by all other units | bib:andersen1993procedure file:paper/reading_pass.yaml | backed | keep |
| U03-C026 | L | Malmquist indices run across data sets | bib:fare1994productivity file:paper/reading_pass.yaml | backed | keep |
| U03-C027 | L | where DEA obtains weights unit by unit Note: 'weights obtained from the data' read (row 17), but 'unit by unit' (a weight set per unit) appears only in a secondary paraphrase of Charnes (row 16, not accessible); rows 20-21 say self-chosen weights not named in the abstracts | bib:banker1984some file:paper/reading_pass.yaml | broader than its backing | narrow |
| U03-C028 | L | practice has added weights restrictions [@allen1997weights] and protocols | bib:allen1997weights bib:dyson2001pitfalls file:paper/reading_pass.yaml | backed | keep |
| U03-C029 | S | We fit one exponent vector per facet, a global named structure | test:tests/test_estimator.py::test_fit_invariants test:tests/test_estimator.py::test_n_terms_above_one_is_implemented file:work-packages/interface-contract.toml glossary:exponent-vector | backed | keep |
| U03-C030 | M | Our facets are piecewise log-linear with constant elasticities within a facet | lemma:L7.5 lemma:L10.9 lemma:L10.18 lemma:L10.19 glossary:facet glossary:elasticity | backed | keep |
| U03-C031 | M | Our metrics are larger-is-better with homogeneity from the simplex | lemma:L1.5 lemma:L1.8 lemma:L11.7 glossary:metrics glossary:invariant-value | backed | keep |
| U03-C032 | M | Our boundary is a soft maximum with a temperature, a band and an effective sample size | lemma:L5.15 lemma:L5.16 lemma:L5.24 glossary:temperature glossary:support-weights test:tests/test_estimator.py::test_k_terms_attributes_conventions | backed | keep |
| U03-C033 | S | We solve one convex program and K refits, and return coordinates with a pull-back to attribute units | lemma:L4 test:tests/test_solvers.py::test_slsqp_agrees_with_lp test:tests/test_solvers.py::test_terms_k1_equals_slsqp_and_degenerate test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples | backed | keep |
| U03-C034 | M | The weighted geometric mean with exponents summing to one has the constant-returns Cobb-Douglas form | lemma:L1.5 lemma:L1.8 glossary:invariant-value | backed | keep |
| U03-C035 | L | Shephard's characterization of a technology by its distance function | bib:shephard1970theory file:paper/reading_pass.yaml | backed | keep |
| U03-C036 | L | Frontier estimation by programming, corrected least squares and one-sided error is the family of one-sided fits | bib:battese1992frontier file:paper/reading_pass.yaml | backed | keep |
| U03-C037 | L | The chart is in the spirit of log-ratio coordinates for compositional data Note: rows 34-36 not accessible, 'in the spirit of' is the author's comparison; only the orthonormal sum-zero chart (L8) is backed, not any property of log-ratio coordinates | lemma:L8 bib:aitchison1983principal bib:egozcue2003isometric file:paper/reading_pass.yaml | broader than its backing | narrow |
| U03-C038 | L | The model class and refit scheme come from geometric programming and max-affine fitting | bib:boyd2007tutorial bib:hoburg2016data bib:magnani2009convex file:paper/reading_pass.yaml | backed | keep |
| U03-C039 | M | the soft maximum is an entropic risk functional | bib:foellmer2026entropic lemma:L5 glossary:temperature file:paper/reading_pass.yaml | backed | keep |
| U03-C040 | L | Kernel PCA is the feature-engineering kin of the direction | bib:schoelkopf1998nonlinear file:paper/reading_pass.yaml | backed | keep |
| U03-C041 | L | "hyperbolic" here is unrelated to hyperbolic PCA | bib:chami2021horopca file:paper/reading_pass.yaml | backed | keep |
| U03-C042 | L | Tradespace exploration lets an analyst explore designs | bib:ross2005tradespace bib:stump2009visual file:paper/reading_pass.yaml | backed | keep |
| U03-C043 | L | We did not find the combination in the sources reviewed | file:paper/prior_art.yaml test:tests/test_paper.py::test_prior_art_cites_resolve_in_the_bibliography | backed | keep |

### U04: paper Preliminaries and notation (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U04-C001 | L | Mathematical notation follows Boyd and Vandenberghe [@boyd2004convex] | definition file:docs/superpowers/notes/notation.md | backed | keep |
| U04-C002 | L | estimator terms follow the scikit-learn documentation | definition file:docs/superpowers/notes/notation.md | backed | keep |
| U04-C003 | M | the evaluation is a black box to the method | file:work-packages/interface-contract.md | backed | keep |
| U04-C004 | R | is one instance behind that abstraction, not part of the method | file:work-packages/interface-contract.md | backed | keep |
| U04-C005 | P | so the method stays relevant as tools move or where scoring comes from physical systems or human judgment | reading file:work-packages/interface-contract.md | backed | keep |
| U04-C006 | M | The formal results are properties of mathematical objects, conditioned on assumptions that we cannot certify for a given table of designs | file:derivation/axioms.py file:docs/superpowers/notes/abstraction-gaps.md | backed | keep |
| U04-C007 | S | the implementation approximates those objects numerically | file:docs/superpowers/notes/abstraction-gaps.md | backed | keep |
| U04-C008 | R | which records for each place where the map and the territory part the assumption that bridges it | gen:paper/generate_gaps.py::gaps_table test:tests/test_paper.py::test_gaps_table_has_every_ledger_row | backed | keep |
| U04-C009 | P | All models are wrong, some are useful, and a model is useful for a specific purpose in a specific situation Note: Box aphorism uncited: no Box entry in docs/references.bib, prior_art.yaml or reading_pass.yaml; cite a verified source, mark as the author's maxim, or drop | none | unbacked | drop |
| U04-C010 | M | A posynomial is a sum of monomials. | definition glossary:posynomial | backed | keep |
| U04-C011 | M | A term, a monomial and a facet are one object | definition glossary:facet glossary:term glossary:monomial lemma:L10.19 | backed | keep |
| U04-C012 | M | The supporting envelope is the $\tau=\infty$ fit, which none exceeds. | lemma:L5 glossary:supporting-envelope | backed | keep |
| U04-S01 | M | some designs lie beyond it Note: Glossary says rows above the reference surface exist by construction; L5 gives LME<=max so the top row has V>=1, strictness (some design beyond it) needs non-constant scores and is not a stated step | lemma:L5 glossary:fitted-reference-surface | broader than its backing | to the driver |

### U05: paper Definitions (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U05-C001 | M | weighted geometric mean of the metrics; doubling every metric doubles it | registered:C002 | backed | routed to P1 |
| U05-C002 | M | It stays the same along a trade-off, hence invariant. | registered:C003 | backed | routed to P1 |
| U05-C003 | M | A difference of levels is the same along every path between two designs. | registered:C005 | backed | routed to P1 |
| U05-C004 | M | It is neither a physical energy nor a Euclidean distance. | registered:C006 | backed | routed to P1 |
| U05-C005 | M | is a design's level relative to the reference surface | registered:C004 | backed | routed to P1 |
| U05-C006 | M | negative inside, positive beyond. A difference of levels | registered:C004 | backed | routed to P1 |
| U05-C007 | M | the model is a sum of such terms, one per facet | registered:C007 | backed | routed to P1 |
| U05-C008 | M | is the $1/\kappa$ power of a posynomial, a sum of monomials | lemma:L10.7 lemma:L10.19 glossary:posynomial | backed | routed to P1 |
| U05-C009 | M | in the soft maximum a design inside it weighs within a factor $e$ of one on the surface Note: No lemma step or test states the weight ratio: the soft-max weight e^{tau(w.u-beta)} = e^{tau log V} lies in (1/e, e) when \|log V\|<1/tau is a one-line fact from L3 support weights / L5 terms, untagged; tests/test_paper.py::test_cr3 only checks the phrase is present. Candidate to back with a tagged step or narrow. | none | unbacked | routed to P1 |
| U05-C010 | M | is the position along the frontier, free of overall scale | lemma:L8.6 lemma:L8.4 glossary:position-along-the-frontier | backed | routed to P1 |
| U05-C011 | M | is the chart, a reversible rewriting of the metrics | registered:C010 | backed | routed to P1 |
| U05-C012 | M | and a member can carry a small one | definition | backed | routed to P1 |
| U05-C013 | M | it shows which facets carry most of the frontier and depends on the band | definition | backed | routed to P1 |
| U05-C014 | M | the percent change of $j$ per percent change of $i$ | lemma:L7.5 glossary:elasticity | backed | routed to P1 |
| U05-C015 | M | trades contending metrics at constant $V$ | lemma:L7.4 lemma:L7.5 lemma:L1 | backed | routed to P1 |
| U05-C016 | M | the normal $w_k$ is the steepest ascent of $\log V$ Note: L7.4 gives the directional derivative dG(v)=w.v of G=w.u-beta, so w_k is the gradient and the tangent part is backed; 'steepest' ascent (Cauchy-Schwarz, Euclidean metric on log-metrics u) is not a tagged step and no test pins it. | lemma:L7.4 | broader than its backing | routed to P1 |
| U05-S01 | M | is its logarithm. | lemma:L10.7 lemma:L10.19 glossary:posynomial | backed | routed to P1 |
| U05-S02 | M | at infinity each is exact | registered:C008 | backed | routed to P1 |

### U06: paper Methods (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U06-C001 | M | otherwise exponents are a subgradient choice, not an identified trade-off Note: L3.9/L3.11 prove identification (equal gradients) under R1; the converse 'otherwise a subgradient choice' is only the R1 failure_mode text in the ledger (axioms.py), no tagged step | lemma:L3.11 lemma:L3.9 file:derivation/axioms.py | broader than its backing | to the driver |
| U06-C002 | M | At $K=1$ the frontier is the unit level set of $V$. | lemma:L10.9 lemma:L1.6 glossary:fitted-reference-surface | backed | keep |
| U06-C003 | M | the factor $1/N$ makes it a property of the shape of the data, not the number of designs Note: L5.6 gives LSE-LME=log(n)/tau only; invariance to the number of designs (row replication) is numeric, and I2 is a recorded remark no step uses; 'shape of the data' is wider than replication | lemma:L5.6 test:tests/test_derivation.py::test_replication_invariance test:tests/test_estimator.py::test_row_replication_leaves_fit_unchanged | broader than its backing | to the driver |
| U06-C004 | M | At $\tau=\infty$ the fit is a linear program. | lemma:L5.24 lemma:L12.31 func:src/hyperbolic_trade_space/solvers.py::solve_lp test:tests/test_solvers.py::test_lp_gap_equals_duality_gap_and_uniform_ties_is_a_valid_bound | backed | keep |
| U06-C005 | M | At finite $\tau$ one facet is a geometric program, convex after the change of variables $x=e^{w}$ | lemma:L4.24 lemma:L4.23 glossary:geometric-program | backed | keep |
| U06-C006 | M | $V_K$ is a generalized posynomial, the term maximum at the default $\kappa=\infty$ | lemma:L10.7 lemma:L10.18 lemma:L10.19 glossary:generalized-posynomial | backed | keep |
| U06-C007 | L | generalized posynomial, the term maximum at the default $\kappa=\infty$ [@boyd2007tutorial] | bib:boyd2007tutorial file:paper/reading_pass.yaml | backed | keep |
| U06-C008 | M | Several facets alternate weights with one program for all terms | lemma:L16.49 lemma:L16.43 lemma:L16.30 | backed | keep |
| U06-C009 | S | $\tau$ puts a target fraction of designs above $V=1$: 10 percent here | test:tests/test_tuning.py::test_selected_temperature_hits_target func:src/hyperbolic_trade_space/tuning.py::select_temperature test:tests/test_case.py::test_sensitivity_and_refits_on_frozen_primary | backed | keep |
| U06-C010 | R | halving or doubling it leaves the contending sets unchanged Note: 'it' is the target fraction; the test asserts only n_lemma == shared-with-baseline per variant (variant set within baseline's), not equality of sets; printed table does show identical sets in both regimes | gen:paper/generate_results.py::sensitivity_variants gen:examples/adcs/case.py::sensitivity_table test:tests/test_paper.py::test_cr3_the_target_and_the_band_carry_their_reason_and_the_sensitivity_holds | broader than its backing | narrow |
| U06-C011 | M | a convention that keeps one extreme design from setting the surface Note: rationale: L5.24 shows tau=inf is set by the maximum; no step or test shows a finite tau at 10 percent keeps one design from setting the surface (n_eff_ 14-16 in D.5 is only descriptive) | lemma:L5.16 lemma:L5.24 | broader than its backing | to the driver |
| U06-C012 | M | a scaler equalizes log-spread so one $\tau$ serves every metric Note: the scaler equalizing log-spread is tested; 'so one tau serves every metric' is a purpose with no backing | test:tests/test_preconditioning.py::test_unit_log_standard_deviation test:tests/test_preconditioning.py::test_robust_normalizes_log_iqr_and_ignores_zeros | broader than its backing | to the driver |
| U06-C013 | M | rescaling one metric changes which facet is tangent Note: L2 covers a uniform shift only (w unchanged); no lemma/test for rescaling one metric; the sensitivity table shows the robust scaler (all metrics) changing the contending set | gen:examples/adcs/case.py::sensitivity_table lemma:L2.8 | broader than its backing | to the driver |
| U06-C014 | S | Zeros are tolerated in data and masked in the fit, negative values are rejected | test:tests/test_estimator.py::test_zero_metric_row test:tests/test_estimator.py::test_negative_and_nonfinite_raise | backed | keep |
| U06-C015 | M | the pull-back to attribute units is exact | lemma:L9.5 lemma:L9.6 test:tests/test_preconditioning.py::test_pullback_matches_L9_chain_formula | backed | keep |
| U06-C016 | S | An exponent above the participation threshold ($10^{-3}$) participates | definition glossary:participation-threshold test:tests/test_estimator.py::test_constants_are_reexported test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact | backed | keep |
| U06-C017 | M | one at or below $10^{-12}$ is numerically zero, not mathematically so | definition glossary:numerically-zero test:tests/test_estimator.py::test_constants_are_reexported | backed | keep |
| U06-C018 | S | The fit is a scikit-learn transformer of the decomposition family | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score file:docs/superpowers/notes/sklearn-conformance.md | backed | keep |
| U06-C019 | S | `fit` identifies exponents and offsets, `transform` returns the chart | test:tests/test_estimator.py::test_fit_invariants test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples | backed | keep |
| U06-C020 | S | `inverse_transform` reverses it, `score_samples` returns the energy differential | test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples glossary:energy-differential | backed | keep |
| U06-C021 | S | It has no `predict`: prediction composes a supervised regressor with the chart. | test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score test:tests/test_predictive.py::test_trade_space_can_be_a_pipeline_and_regressor_a_pipeline | backed | keep |
| U06-C022 | S | *One facet at $K=1$:* constant elasticities; $K>1$ is built. | lemma:L7.5 test:tests/test_estimator.py::test_k_terms_recovers_planted_facets test:tests/test_estimator.py::test_n_terms_above_one_is_implemented | backed | keep |
| U06-C023 | S | facets are fitted at $\kappa=\infty$ with kinks on the ridges | lemma:L10.18 test:tests/test_soft_fit.py::test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone work-packages/interface-contract.md | backed | keep |
| U06-C024 | M | a finite $\kappa$ moves the score by at most $(\log K)/\kappa$ | lemma:L10.15 lemma:L10.16 | backed | keep |
| U06-C025 | M | by construction, leaves the facets unchanged | definition lemma:L10.16 | backed | keep |
| U06-C026 | M | fitting at a finite $\kappa$ is the soft fit of {numref}`Section %s <sect-results>`, which does change them | registered:C012 | backed | keep |
| U06-C027 | M | it is exactly invertible ({prf:ref}`thm-pullback`) and stays inside geometric programming Note: invertibility backed (L9.4/L9.6); 'stays inside geometric programming' has no step: L9.5 gives the monomial-in-(a+s) form but no GP statement, and (a+s)^negative power is not a posynomial in a | lemma:L9.4 lemma:L9.6 lemma:L9.5 | broader than its backing | to the driver |
| U06-C028 | M | $\Phi_K$ is convex in $u$, which keeps later optimization convex Note: no lemma step or test states Phi_K convex in u (L10.7 shows e^(kappa Phi_K) posynomial; convexity is inherited I4, cited); 'keeps later optimization convex' not backed | lemma:L10.7 bib:hoburg2016data | broader than its backing | to the driver |
| U06-S01 | R | the case needs three facets Note: K=3 facet table is pinned, but 'needs' is broader: the paper itself says three facets is the analyst's choice and mean slack cannot choose K | gen:examples/adcs/case.py::facet_table test:tests/test_case.py::test_k3_facets_equal_the_primary_record test:tests/test_paper.py::test_cr8_the_k_comparison_says_the_temperature_differs_and_d15_fixes_it | broader than its backing | narrow |
| U06-S02 | M | no $K$ represents non-log-convex structure Note: no step or test shows the model class excludes non-log-convex structure; it would follow from convexity of Phi_K, itself unproved (see C028) | none | unbacked | to the driver |

### U07: paper Results (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U07-C001 | M | The several-facet fit is not convex; it has three levels of guarantee | lemma:L16 registered:C013 | backed | routed to P1 |
| U07-C002 | M | it has three levels of guarantee (L16, L15, L12 to L14) and, for a soft fit, a certificate (L17) Note: L16 is the soft-weight alternation (not a sharp-weight level), so (L16, L15, L12 to L14) lists four groups for three levels; the three levels are L15, L12, L13-L14 (as the Main results sentence says); L17 certificate is correct | lemma:L15 lemma:L12 lemma:L13 lemma:L14 lemma:L17 | broader than its backing | routed to P1 |
| U07-C003 | M | the fit as a convex program (L3 to L5) | registered:C013 lemma:L3 lemma:L4 lemma:L5 | backed | routed to P1 |

### U08: paper The fit and its geometry (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U08-C001 | M | The invariant value scales with the metrics (L1) | lemma:L1.5 glossary:invariant-value | backed | routed to P1 |
| U08-C002 | M | shifting every log-metric by a constant moves the offset by that constant and leaves the exponents unchanged | registered:C014 lemma:L2.6 lemma:L2.8 | backed | routed to P1 |
| U08-C003 | M | A1 gives $V=\exp(w\cdot u)$; A2 turns scaling by $k$ into the addition of $\log k$. | lemma:L1.2 lemma:L1.5 | backed | routed to P1 |
| U08-C004 | M | $J_\tau(w;U+c\mathbf 1^\top)=J_\tau(w;U)+c$: $\beta$ moves by $c$ and $w^*$ is unchanged. | lemma:L2.5 lemma:L2.6 lemma:L2.8 | backed | routed to P1 |
| U08-C005 | M | Weights summing to one shift every score by $c$, and the log-mean-exp is shift-equivariant. | lemma:L2.1 lemma:L2.2 | backed | routed to P1 |
| U08-C006 | M | The one-facet fit has simplex optimality conditions (L3) | registered:C015 lemma:L3.15 lemma:L3.23 | backed | routed to P1 |
| U08-C007 | M | is convex (L4), and uses the log-mean-exp | registered:C015 lemma:L4.13 | backed | routed to P1 |
| U08-C008 | M | which differs from the log-sum-exp by a constant (L5) | registered:C015 lemma:L5.6 | backed | routed to P1 |
| U08-C009 | M | Balanced hard-support geometry does not imply an interior minimizer at finite $\tau$. | lemma:L3.28 lemma:L3.29 lemma:L3.35 | backed | routed to P1 |
| U08-C010 | M | Active simplex constraints are affine with independent gradients | lemma:L3.16 lemma:L3.17 lemma:L3.19 | backed | routed to P1 |
| U08-C011 | M | $J_\tau$ is convex, not claimed strictly. | lemma:L4.12 lemma:L4.13 | backed | routed to P1 |
| U08-C012 | M | The curvature is $\tau$ times a $p$-weighted variance, nonnegative on every line | lemma:L4.3 lemma:L4.12 | backed | routed to P1 |
| U08-C013 | M | the mean and the maximum are the limits. | lemma:L5.22 lemma:L5.24 | backed | routed to P1 |
| U08-C014 | M | shifting by the maximum squeezes the sum between one and $N$ unit-size terms. | lemma:L5.7 lemma:L5.11 lemma:L5.16 | backed | routed to P1 |
| U08-C015 | M | the soft maximum of Gaussian noise has a closed form (L6) | registered:C016 lemma:L6.8 | backed | routed to P1 |
| U08-C016 | M | along a facet the exponents are elasticities and give the improvement factors to $V=1$ (L7) | registered:C016 lemma:L7.5 lemma:L7.7 | backed | routed to P1 |
| U08-C017 | M | a population identity, with no consistency claim. | lemma:L6.8 | backed | routed to P1 |
| U08-C018 | M | The moment generating function of an independent sum is the product of its factors. | lemma:L6.2 | backed | routed to P1 |
| U08-C019 | M | Improving metric $j$ alone by $V^{-1/w_j}$, or every metric by $1/V$, reaches $V=1$. | lemma:L7.7 lemma:L7.9 | backed | routed to P1 |
| U08-C020 | M | A tangent $e_k+xe_j$ has derivative $w_k+xw_j$. | lemma:L7.4 | backed | routed to P1 |
| U08-C021 | M | Scaling $m_j$ by $f$ adds $w_j\log f$ to $\log V$. | lemma:L7.6 | backed | routed to P1 |
| U08-C022 | M | Identifying these rates with the fit needs {prf:ref}`thm-kkt` and R1. | lemma:L7 | backed | routed to P1 |
| U08-C023 | M | The chart is a reversible rewriting of the log-metrics (L8) | registered:C017 lemma:L8.14 | backed | routed to P1 |
| U08-C024 | M | under log-affine conditioning the pull-back to attributes is exact (L9) | registered:C017 lemma:L9.5 lemma:L9.6 | backed | routed to P1 |
| U08-C025 | M | $Z(u+c\mathbf 1)=Z(u)$ and $u=B^\top Z+\frac1d(\mathbf 1^\top u)\mathbf 1$ | lemma:L8.6 lemma:L8.14 | backed | routed to P1 |
| U08-C026 | M | the map between $u$ and (position, log-scale) is a bijection, and $Q=[B;\mathbf 1^\top/\sqrt d]$ is orthogonal. | lemma:L8.3 lemma:L8.7 lemma:L8.10 lemma:L8.14 | backed | routed to P1 |
| U08-C027 | M | $B\mathbf 1=0$ kills the shift; the blocks of $QQ^\top$ and I6 give the round trip. | lemma:L8.5 lemma:L8.7 lemma:L8.8 lemma:L8.3 lemma:L8.14 | backed | routed to P1 |
| U08-C028 | M | $V=e^{w\cdot b-\beta}\prod_j(a_j+s_j)^{w_j\alpha_j}$, and conditioning is invertible | lemma:L9.5 lemma:L9.6 | backed | routed to P1 |
| U08-C029 | M | negative $w_j\alpha_j$ marks a cost attribute. | lemma:L9.5 | backed | routed to P1 |
| U08-C030 | M | the offset enters only through $\sum_jw_j=1$. | lemma:L9.7 | backed | routed to P1 |
| U08-C031 | M | With several terms, $V_K$ is the $1/\kappa$ power of a posynomial | registered:C018 lemma:L10.7 | backed | routed to P1 |
| U08-C032 | M | its logarithm lies within $(\log K)/\kappa$ of its largest term (L10) | registered:C018 lemma:L10.15 lemma:L10.16 | backed | routed to P1 |
| U08-C033 | M | a maximizer of $V$ is Pareto-efficient, and the converse is not claimed (L11) | registered:C018 lemma:L11.17 | backed | routed to P1 |
| U08-C034 | M | $e^{\kappa\Phi_K}$ is a posynomial in $m$. | lemma:L10.7 lemma:L10.19 | backed | routed to P1 |
| U08-C035 | M | Simplex exponents turn the shift into $c$ in every term | lemma:L10.1 lemma:L10.8 | backed | routed to P1 |
| U08-C036 | M | each term is a monomial (I4: log-sum-exp of affine functions is GP-compatible). | lemma:L10.19 bib:hoburg2016data | backed | routed to P1 |
| U08-C037 | M | A maximizer of $V$ is weakly efficient in all $d$ metrics, and efficient when every $w_j>0$ | lemma:L11.18 lemma:L11.19 | backed | routed to P1 |
| U08-C038 | M | at $K>1$, $\kappa=\infty$, through an active term. | lemma:L11.13 | backed | routed to P1 |
| U08-C039 | M | the gain $\sum_jw_j\delta_j$ is a sum of nonnegative terms | lemma:L11.4 lemma:L11.5 | backed | routed to P1 |
| U08-C040 | M | That only the log-convex part of a front is reached by some $w$ is our statement, not a cited one. Note: Provenance backed (reading_pass n=14,15: citations removed, stated as own) but the content 'only the log-convex part is reached by some w' has no tagged step (L11 docstring only, which still cites Miettinen/Ehrgott and says converse not proved). | lemma:L11 file:paper/reading_pass.yaml | broader than its backing | routed to P1 |
| U08-S01 | M | For $k>0$: $V(km)=kV(m)$ and $V(m/V(m))=1$ | lemma:L1.5 lemma:L1.6 | backed | routed to P1 |
| U08-S02 | M | $V(me^{-\beta})=e^{-\beta}V(m)$, so $\log V=w\cdot u-\beta$ | lemma:L1.7 | backed | routed to P1 |
| U08-S03 | M | $\nabla J_\tau=U^\top p$, $p=\mathrm{softmax}(\tau Uw)$. | lemma:L3.15 | backed | routed to P1 |
| U08-S04 | M | $g_j\ge\lambda$ and $w_j(g_j-\lambda)=0$. | lemma:L3.24 lemma:L3.25 | backed | routed to P1 |
| U08-S05 | M | $\frac{d^2}{dt^2}J_\tau(w+tv) | lemma:L4.3 lemma:L4.12 lemma:L4.13 | backed | routed to P1 |
| U08-S06 | M | $\mathrm{LSE}_\tau=\mathrm{LME}_\tau+(\log N)/\tau$ | lemma:L5.6 | backed | routed to P1 |
| U08-S07 | M | $\mathrm{mean}\le\mathrm{LME}_\tau\le\max_is_i$ and $\mathrm{LME}_\tau\ge\max_is_i-(\log N)/\tau$ | lemma:L5.14 lemma:L5.15 lemma:L5.16 | backed | routed to P1 |
| U08-S08 | M | $\frac1\tau\log\mathbb{E}\,e^{\tau w\cdot\varepsilon}=\tau\sigma^2\lVert w\rVert^2/2$. | lemma:L6.8 | backed | routed to P1 |
| U08-S09 | M | On it $\mathrm{d}\log m_j/\mathrm{d}\log m_k=-w_k/w_j$. | lemma:L7.5 | backed | routed to P1 |
| U08-S10 | M | $\Phi_K(u+c\mathbf 1)=\Phi_K(u)+c$; $\Phi_1=w_1\cdot u-\beta_1$; | lemma:L10.8 lemma:L10.9 | backed | routed to P1 |
| U08-S11 | M | $\max_kx_k\le\Phi_K\le\max_kx_k+(\log K)/\kappa$ with $x_k=w_k\cdot u-\beta_k$ | lemma:L10.15 lemma:L10.16 | backed | routed to P1 |

### U09: paper The algorithm for several facets (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U09-C001 | M | each offset $\beta_k=J_\tau(Uw_k)$ is the support over all rows | definition | backed | routed to P1 |
| U09-C002 | M | By symmetry in the terms $F$ is not convex ({prf:ref}`thm-soft`, part i) | lemma:L16.35 lemma:L16.37 | backed | routed to P1 |
| U09-C003 | L | so the estimator adapts the alternation of Magnani and Boyd [@magnani2009convex] | bib:magnani2009convex file:paper/reading_pass.yaml file:paper/prior_art.yaml | backed | routed to P1 |
| U09-C004 | S | The package fits with sharp weights at the default term temperature (infinity) and with soft weights at a finite one | registered:C019 | backed | routed to P1 |
| U09-C005 | S | a soft fit is certified by the second-order test ({prf:ref}`thm-certificate`) | registered:C019 | backed | routed to P1 |
| U09-C006 | M | The sharp weights give one label per design, $k(i)=\arg\max_ks_{ik}$ | definition | backed | routed to P1 |
| U09-C007 | M | a convex program symmetric in the terms attains its minimum with all terms equal, so the objective over all terms is not convex in them in general | lemma:L16.35 lemma:L16.37 | backed | routed to P1 |
| U09-C008 | M | the soft model's slack is bounded above by the fixed-weight objective, with equality at the weights' own model | lemma:L16.41 lemma:L16.42 lemma:L16.43 | backed | routed to P1 |
| U09-C009 | M | the fixed-weight objective is a generalized posynomial in $e^{w}$ | lemma:L16.49 lemma:L16.31 | backed | routed to P1 |
| U09-C010 | M | Cyclic shifts of the terms and Jensen's inequality give (i) and (ii); (iii) is a product of powers of posynomials. | lemma:L16.6 lemma:L16.35 lemma:L16.14 lemma:L16.31 | backed | routed to P1 |
| U09-C011 | R | Refitting a facet on its own rows is ill-posed (observed on planted data | gen:paper/generate_results.py::own_rows_refit test:tests/test_paper.py::test_the_claims_of_c1_have_their_true_basis | backed | routed to P1 |
| U09-C012 | M | The sharp-weight fit meets three levels of guarantee, none global | registered:C020 | backed | routed to P1 |
| U09-C013 | M | One accepted iteration does not raise the mean slack $F$ | lemma:L15.16 | backed | routed to P1 |
| U09-C014 | M | reassigning each row to its maximizing facet lowers or keeps $F$, and refitting each facet on the new cells does likewise | lemma:L15.12 lemma:L15.15 | backed | routed to P1 |
| U09-C015 | M | Reassignment gives each row the least of its slacks; the refit minimizes a convex $f_k$ of which the previous $w_k$ is a feasible point. | lemma:L15.10 lemma:L15.8 lemma:L12.13 lemma:L12.24 | backed | routed to P1 |
| U09-C016 | M | the facet gap is $G_k(w)=g\cdot w-\min_jg_j=\sum_jw_j(g_j-\min_lg_l)\ge0$, and $0\le f_k(w)-f_k^*\le G_k(w)$ | lemma:L12.17 lemma:L12.15 lemma:L12.23 lemma:L12.24 | backed | routed to P1 |
| U09-C017 | M | $G_k=0$ exactly when the simplex KKT conditions of {prf:ref}`thm-kkt` hold | lemma:L12.21 | backed | routed to P1 |
| U09-C018 | M | At $\tau=\infty$, with the LP duals, $G_k$ is the LP duality gap. | lemma:L12.28 lemma:L12.31 lemma:L12.32 | backed | routed to P1 |
| U09-C019 | M | Since $w$ is on the simplex, $g\cdot v-\min_jg_j\ge0$ for every $v$ | lemma:L12.15 lemma:L12.14 | backed | routed to P1 |
| U09-C020 | M | If every facet score changes by at most $\delta$ with $2\delta<\gamma$, each row's maximizing facet is unchanged and unique. | lemma:L13.7 | backed | routed to P1 |
| U09-C021 | M | This holds whenever every $(w_k,\beta_k)$ moves by less than the stable radius | lemma:L13.11 lemma:L13.10 | backed | routed to P1 |
| U09-C022 | M | Each row's gap to every other facet falls by at most $2\delta$; Cauchy-Schwarz bounds a score change. | lemma:L13.5 lemma:L13.10 | backed | routed to P1 |
| U09-C023 | M | so $W$ is a local minimizer of the mean slack | lemma:L14.18 | backed | routed to P1 |
| U09-C024 | M | R2 keeps each row's maximizing facet, so the objective equals $F$ there; regroup the rows by facet, each term nonnegative. | lemma:L14.16 lemma:L14.6 lemma:L14.17 lemma:L14.18 | backed | routed to P1 |
| U09-C025 | M | The bound is for the returned run, not across restarts. | definition | backed | routed to P1 |
| U09-C026 | M | Apply $f_k-f_k^*\le G_k$ of {prf:ref}`lem-gap` termwise with the weights $n_k/N$. | lemma:L14.19 lemma:L14.20 lemma:L14.10 | backed | routed to P1 |
| U09-C027 | M | At a finite term temperature a second-order test certifies a strict local minimizer (L17). | registered:C021 | backed | routed to P1 |
| U09-C028 | M | if the Hessian $H=D-\kappa M$ of the soft objective is positive definite on the tangent space of the active face, the point is a strict local minimizer | lemma:L17.44 lemma:L17.21 | backed | routed to P1 |
| U09-C029 | M | $D$ and $M$ are both positive semidefinite | lemma:L17.39 lemma:L17.40 | backed | routed to P1 |
| U09-C030 | M | The gradient and the Hessian agree with finite differences on an exact instance. | lemma:L17.24 lemma:L17.47 lemma:L17.48 | backed | routed to P1 |
| U09-C031 | M | $D$ is a sum of covariances and $M$ of variances, so both are positive semidefinite | lemma:L17.37 lemma:L17.38 lemma:L17.39 lemma:L17.40 | backed | routed to P1 |
| U09-C032 | M | the constraints are affine, so the second-order sufficient condition (I16) applies to the objective's own Hessian | lemma:L17.18 lemma:L17.41 lemma:L17.44 | backed | routed to P1 |
| U09-C033 | S | Each returned fit carries the levels it meets | file:work-packages/interface-contract.md test:tests/test_interface_contract.py::test_r1_termination_fields_statuses_and_report_fields test:tests/test_estimator.py::test_termination_record_for_k_terms | backed | routed to P1 |
| U09-C034 | S | Whether a fit is stationary within tolerance, and so its status, is measured, not proved. | definition | backed | routed to P1 |
| U09-C035 | R | the solver declares the status certified at K = 2 and 3, with the largest facet gap below 1e-12 | gen:paper/generate_findings.py::certificate_sentence test:tests/test_paper.py::test_generated_sentences_committed_output_is_current test:tests/test_case.py::test_k_sweep_equals_the_record | backed | routed to P1 |
| U09-C036 | R | At K = 3 the margin is 0.00022 to 0.0019 and the stable radius 1.8e-05 to 0.00016 | gen:paper/generate_findings.py::margin_sentence test:tests/test_paper.py::test_generated_sentences_committed_output_is_current test:tests/test_case.py::test_k_sweep_equals_the_record | backed | routed to P1 |
| U09-C037 | R | a band 1/tau of 0.0051 and a median best-minus-second-best score of 0.18 | gen:paper/generate_findings.py::margin_sentence test:tests/test_paper.py::test_generated_sentences_committed_output_is_current test:tests/test_case.py::test_margin_scale_has_the_multi_facet_fits_only_and_the_median_exceeds_the_margin | backed | routed to P1 |
| U09-C038 | R | a margin below the band puts a few designs on a seam, and the certificate covers changes under the radius only Note: Second half (certificate covers changes under the radius) is L13.7/L13.11. First half: gamma is the minimum gap, so gamma below the band only shows at least one design within the band of a seam; 'a few designs' has no count pinned anywhere (no test or generator counts designs inside the band) | lemma:L13.11 lemma:L13.7 | broader than its backing | routed to P1 |
| U09-S01 | M | with $f_k$ convex by {prf:ref}`thm-convex` | lemma:L12.13 lemma:L4.3 | backed | routed to P1 |
| U09-S02 | M | sufficient and not tight Note: Sufficiency is L13.11; 'not tight' is not shown: lemma_13 docstring says it does NOT prove the radius is tight (the confined instance uses 0.9 of the radius), nor that it is loose; reword to sufficient, tightness not claimed | lemma:L13.11 | broader than its backing | routed to P1 |
| U09-S03 | M | $0\le F(W)-F^*_{\text{fixed}}\le\sum_k\frac{n_k}{N}G_k(w_k)$ | lemma:L14.10 lemma:L14.19 lemma:L14.20 | backed | routed to P1 |

### U10: paper Open questions (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U10-C001 | M | Q1: global convergence of the alternation, not pursued. | file:docs/superpowers/notes/abstraction-gaps.md test:tests/test_paper.py::test_badges_are_present_and_the_open_questions_are_marked test:tests/test_paper.py::test_gaps_table_has_every_ledger_row | backed | routed to P1 |
| U10-S01 | M | Four questions are not established | file:docs/superpowers/notes/abstraction-gaps.md test:tests/test_paper.py::test_badges_are_present_and_the_open_questions_are_marked test:tests/test_paper.py::test_gaps_table_has_every_ledger_row | backed | routed to P1 |

### U11: paper Search of the design space (preliminary) (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U11-C001 | P | A trade study also decides what to evaluate next, today by expert intuition or exhaustive sampling. Note: Practice claim about how trade studies choose evaluations today; no source or reading marker (search-prior-art.md is not an audit row) | none | unbacked | drop |
| U11-C002 | M | The fitted facets say where better is, so sampling can be trade-off aware. | definition | backed | keep |
| U11-C003 | M | on each facet the normal is an ascent direction in log space | lemma:L1.7 lemma:L10 | backed | keep |
| U11-C004 | M | chained back through the conditioning and the evaluation to a direction in configuration space, estimated by finite differences or a supervised regressor Note: L9 covers only exact pull-back under log-affine conditioning; chain through a general evaluation and finite-difference or regressor estimate has no lemma (search-prior-art L12 is a note, not a derivation) | lemma:L9 | broader than its backing | to the driver |
| U11-C005 | M | a categorical variable is a finite comparison | definition | backed | keep |
| U11-C006 | M | Because evaluation is noisy, the procedure resembles a diffusion with drift along the tangent spaces. Note: Analogy to a diffusion with drift on tangent spaces; no lemma, test or source | none | unbacked | to the driver |
| U11-C007 | M | Outward monotonicity is stated for the exact maximum and not for the soft one; neither has a lemma here. | definition | backed | keep |
| U11-C008 | M | The theory treats variables as continuous within a category. | definition | backed | keep |

### U12: paper Case construction (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U12-C001 | R | Our case is a cubesat model coupling power, mass and attitude control. | gen:examples/adcs/cubesat_model.py::measure test:tests/test_cubesat_model.py::test_measure_returns_attributes_and_flags test:tests/test_paper.py::test_the_case_is_described_as_power_mass_and_attitude_control | backed | keep |
| U12-C002 | R | Each configuration is evaluated once into ten attributes: controls (settling time, slew time, pointing error and control effort) | gen:paper/generate_findings.py::attributes_sentence test:tests/test_case.py::test_subsystem_mapping_is_data_and_covers_every_attribute test:tests/test_paper.py::test_the_case_is_described_as_power_mass_and_attitude_control | backed | keep |
| U12-C003 | R | power and energy (power margin, energy balance, eclipse reserve, peak slew power and depth of discharge) and mass (total mass) | gen:paper/generate_findings.py::attributes_sentence test:tests/test_case.py::test_subsystem_mapping_is_data_and_covers_every_attribute test:tests/test_paper.py::test_the_case_is_described_as_power_mass_and_attitude_control | backed | keep |
| U12-C004 | S | Feasibility removes designs that do not settle, saturate the momentum budget or discharge the battery too deeply. Note: feasibility flags are settled, power_ok, momentum_ok plus all attributes positive; dod_ok (battery depth) is not a flag, and power_ok (available power) is not named in the sentence | test:tests/test_case.py::test_feasibility_table_cascade func:examples/adcs/case.py::feasible_mask | broader than its backing | narrow |
| U12-C005 | M | Conditioning orients each attribute, shifts and scales it to unit log-spread and keeps the map invertible. | test:tests/test_preconditioning.py::test_unit_log_standard_deviation test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift lemma:L9 | backed | keep |
| U12-C006 | R | The hardware values of the case are illustrative and not datasheet values | file:examples/adcs/cubesat_tradespace.sysml file:examples/adcs/cubesat_model.py definition | backed | keep |
| U12-C007 | R | The primary regime evaluates 1000 designs and keeps 706 as feasible | gen:paper/generate_findings.py::datasets_sentence test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data test:tests/test_case.py::test_feasibility_table_cascade test:tests/test_v2_data.py | backed | keep |
| U12-C008 | R | the stock regime evaluates 1000 and keeps 780 | gen:paper/generate_findings.py::datasets_sentence test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data test:tests/test_v2_data.py | backed | keep |
| U12-C009 | R | The selected temperature is tau = 38.1: a fraction 0.096 of designs lies above V = 1 (the target is 0.10) | gen:paper/generate_findings.py::temperature_sentence test:tests/test_case.py::test_k_sweep_equals_the_record | backed | keep |
| U12-C010 | R | the band 1/tau is 0.0262 and the effective sample size is 16 designs. | gen:paper/generate_findings.py::temperature_sentence test:tests/test_case.py::test_regime_comparison_on_frozen_data test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U12-C011 | R | The planted table has 900 rows, 4 metrics and 3 planted facets. | gen:paper/generate_findings.py::planted_sentence test:tests/test_paper.py::test_planted_table_agrees_with_the_reference_values test:tests/test_paper.py::test_planted_example_is_reproducible_and_has_known_facets | backed | keep |
| U12-S01 | R | Each design carries 10 attributes. | gen:paper/generate_findings.py::datasets_sentence test:tests/test_case.py::test_conditioning_table test:tests/test_cubesat_model.py::test_measure_returns_attributes_and_flags | backed | keep |

### U13: paper Case analysis (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U13-C001 | R | the fit recovers all three facets to within 0.05 in 16, at the exact maximum and at temperature 50 | gen:paper/generate_findings.py::recovery_sentence test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C002 | R | the 4 failures have 5, 5, 6 and 11 frontier rows on their thinnest facet | gen:paper/generate_findings.py::recovery_sentence test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C003 | R | At K = 1 the fit reports one tension at the balanced point Note: one facet at K=1 is by construction (706 rows), but 'at the balanced point' is not asserted by any test or defined in the register; nothing pins a single tension row | gen:paper/generate_findings.py::k1_sentence test:tests/test_case.py::test_k1_contending_set_equals_the_record | broader than its backing | narrow |
| U13-C004 | R | At K = 1 the exact-maximum fit has a 6-lemma across controls, power and energy, plus mass | gen:paper/generate_findings.py::k1_sentence test:tests/test_case.py::test_k1_contending_set_equals_the_record test:tests/test_paper.py::test_generated_sentences_name_the_subsystems_from_the_one_mapping | backed | keep |
| U13-C005 | R | total mass, slew time, energy balance, control effort, pointing error and depth of discharge contend | gen:paper/generate_findings.py::k1_sentence test:tests/test_case.py::test_k1_contending_set_equals_the_record | backed | keep |
| U13-C006 | R | with working-temperature exponents from 0.09 to 0.24 Note: no test pins 0.09 to 0.24; num-k1 is not in NUM_CELLS and only the phrase is asserted; values match sensitivity.json (0.0906 to 0.2406 range, committed 0.091 and 0.2395) | gen:paper/generate_findings.py::k1_sentence | unbacked | drop |
| U13-C007 | R | At K = 3 the tension separates into three facets with different contending sets Note: tests pin the K=3 facet sizes (6,6,7) and the largest facet's set start only; that the three sets differ is not asserted | gen:paper/generate_findings.py::k_sweep_sentence test:tests/test_case.py::test_k3_facets_equal_the_primary_record | broader than its backing | narrow |
| U13-C008 | R | The mean slack falls from 0.20 at K = 1 to 0.138 at K = 2 and 0.117 at K = 3, at the temperatures 38, 113 and 195 | gen:paper/generate_findings.py::k_sweep_sentence test:tests/test_case.py::test_k_sweep_equals_the_record test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C009 | R | refitted at the K = 1 temperature it falls to 0.09 and 0.05 | gen:paper/generate_findings.py::k_sweep_sentence test:tests/test_paper.py::test_cr8_the_k_comparison_says_the_temperature_differs_and_d15_fixes_it test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C010 | R | The K = 3 facets have contending sets (exact-maximum supports) of 6, 6 and 7 metrics | gen:paper/generate_findings.py::k_sweep_sentence test:tests/test_case.py::test_k3_facets_equal_the_primary_record | backed | keep |
| U13-C011 | R | peak slew power, power margin and settling time are absent from the K = 1 set | gen:paper/generate_findings.py::k_sweep_sentence test:tests/test_case.py::test_k1_contending_set_equals_the_record test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C012 | M | Mean slack falls with K by construction and cannot choose it Note: by construction is unsupported: temperature is re-selected at each K and no lemma step states nested-family monotonicity of the mean slack; only the observed fall is pinned (RECORD) | none | unbacked | to the driver |
| U13-C013 | M | The same pipeline on the baseline regime separates the problem's contribution from the gains' Note: interpretive claim that the regimes separate the problem's contribution from the gains'; only the contrast of the two contending sets is generated | none | unbacked | to the driver |
| U13-C014 | R | The regimes return a 6-lemma and a 6-lemma sharing 3 metrics (control effort, pointing error and slew time) | gen:paper/generate_findings.py::regime_sentence test:tests/test_case.py::test_k1_contending_set_equals_the_record test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C015 | R | the primary regime alone has depth of discharge, energy balance and total mass, the stock regime alone eclipse reserve, power margin and settling time | gen:paper/generate_findings.py::regime_sentence test:tests/test_case.py::test_k1_contending_set_equals_the_record test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C016 | R | The stock set spans controls plus power and energy: mass enters only in the primary regime | gen:paper/generate_findings.py::regime_sentence test:tests/test_paper.py::test_generated_sentences_name_the_subsystems_from_the_one_mapping | backed | keep |
| U13-C017 | R | The 3 measured candidates have lowest energy differential -0.144 and highest -0.072 to -0.071, and 0 of them lie beyond the fitted reference surface | gen:paper/generate_findings.py::candidates_sentence test:tests/test_case.py::test_candidates_are_scored test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C018 | R | Of 3 proposals, the predicted energy differential lies within the regressor's own band 1/tau = 0.0651 of the measured one for 3 | gen:paper/generate_findings.py::predict_check_sentence test:tests/test_case.py::test_predict_check_within_the_band test:tests/test_case.py::test_refit_reproduces_the_recorded_predictions test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C019 | R | the predicted position within that band for 0; position errors run from 1.4 to 3.1 bands | gen:paper/generate_findings.py::predict_check_sentence test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U13-C020 | S | A regressor from configuration to chart coordinates predicts where proposals fall | test:tests/test_predictive.py::test_recovers_planted_coordinates test:tests/test_case.py::test_predict_check_within_the_band | backed | keep |
| U13-S01 | R | the finding: their sets differ Note: 'the finding: their sets differ' (the K=3 sets differ from one another and from K=1) is not asserted; sizes and one facet's set are pinned | test:tests/test_case.py::test_k3_facets_equal_the_primary_record | broader than its backing | narrow |

### U14: paper Discussion (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U14-C001 | M | The exponents and elasticities are features of the conditioned empirical model | lemma:L7.5 glossary:elasticity | backed | keep |
| U14-C002 | M | they describe how the sampled designs trade, and not a causal exchange that changing a variable would reproduce | glossary:elasticity lemma:L7.5 | backed | keep |
| U14-C003 | M | A hole in the chart is an opportunity only where the trade space is log-convex around it, which the data cannot prove. Note: No lemma step on holes or opportunity; lemma_11 docstring only says non-log-convex front parts are not reached by a w (not a tagged step); 'data cannot prove' is unbacked; narrow to judgment wording or drop | none | unbacked | to the driver |
| U14-C004 | M | Novelty $V-1$ says how far beyond the fitted reference surface a design lies, not whether anyone wants it. | lemma:L1.6 lemma:L7.9 glossary:novelty | backed | keep |
| U14-C005 | M | Machine verification shows that a formula follows from its hypotheses and that the code agrees | test:tests/test_proof_map.py::test_record_holds_every_step_with_tag_prose_and_code test:tests/test_proof_map.py::test_checker_passes_on_the_committed_record | backed | keep |
| U14-C006 | M | it does not show that the hypotheses suit a table | definition | backed | keep |
| U14-C007 | S | gives one line of code to read each proof step against | test:tests/test_paper.py::test_appendix_b_shows_every_result_of_the_record_with_derived_counts test:tests/test_proof_map.py::test_record_holds_every_step_with_tag_prose_and_code | backed | keep |
| U14-C008 | R | the regressor places the energy differential of a proposal within its band (3 of 3) | gen:paper/generate_findings.py::predict_reading test:tests/test_case.py::test_predict_check_within_the_band test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U14-C009 | R | It did not show that it places the position along the frontier (0 of 3) | gen:paper/generate_findings.py::predict_reading test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U14-C010 | R | 3 proposals illustrate and do not estimate a rate | gen:paper/generate_findings.py::predict_reading test:tests/test_case.py::test_predict_check_within_the_band test:tests/test_paper.py::test_generated_sentences_committed_output_is_current | backed | keep |
| U14-C011 | M | A predicted crossing of V = 1 remains a hypothesis. | definition | backed | keep |
| U14-C012 | P | An answer far from the frontier is hard to justify Note: Worded as fact, kind P; no source; allowed only as the author's experience, so rewording as such is needed (e.g. 'In our experience ...') or drop | reading | broader than its backing | to the driver |
| U14-C013 | P | the analysis must rerun on empirical data to support configuration management Note: Worded as fact, kind P; no source; allowed only if worded and marked as the author's experience/judgment, else drop | reading | broader than its backing | to the driver |
| U14-C014 | S | How the attributes were produced is a black box to the method, so the same functions serve a simulator | file:work-packages/interface-contract.md test:tests/test_case.py::test_a_second_table_runs_without_cubesat_edits | backed | keep |
| U14-C015 | S | Another table runs through the same calls. | test:tests/test_case.py::test_a_second_table_runs_without_cubesat_edits | backed | keep |
| U14-C016 | M | The fitted surface is a log-convex envelope. | lemma:L10.7 | backed | keep |
| U14-C017 | M | One facet is tangent at one place and is conservative off it. Note: L10.9/L10.15 (Phi_K at or above each facet term) give a lower bound but 'tangent at one place' and 'conservative off it' (relative to what) are in no step or test | lemma:L10.9 | broader than its backing | to the driver |
| U14-C018 | M | The exponents depend on the conditioning. | lemma:L9.5 | backed | keep |
| U14-C019 | M | K = 1 finds one tension; several regional tensions need K > 1. | lemma:L10.9 | backed | keep |
| U14-C020 | L | as PCA extracts components, is a research question | bib:jolliffe2016principal file:paper/reading_pass.yaml | backed | keep |
| U14-C021 | M | Tensions the sampling never exercised cannot appear. Note: No lemma step or test that a facet absent from the sample cannot be recovered; truism of fitting, needs a one-line test (planted facet unsampled) or drop | none | unbacked | to the driver |
| U14-C022 | M | a design with $V=v$ is a frontier design scaled by $v$ | lemma:L1.5 lemma:L1.6 | backed | keep |
| U14-C023 | M | so $V-1$ is a relative improvement, meaningful relative to the band $1/\tau$. Note: V-1 as a relative improvement is L1.5/L7.9 (scaling by 1/V reaches V=1); 'meaningful relative to the band 1/tau' is in no step (band 1/tau is the regressor's own resolution, not tied to V-1 in a lemma) | lemma:L1.5 lemma:L7.9 | broader than its backing | to the driver |
| U14-S01 | M | Small samples determine exponents weakly. Note: No sample-size test or lemma; n_eff is reported but no sweep or step shows exponents are weakly determined by small samples | none | unbacked | to the driver |
| U14-S02 | S | Nothing here is built. | definition | backed | keep |

### U15: paper Reproducibility and your own case (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U15-C001 | R | Every figure, table and reported number comes from a call into a tested module Note: Backed for figures and tables (one reproduction row each, structural test). 'Every ... reported number' is broader: numbers typed in prose are not shown to be generated, and no test pins that; the row test checks rows exist, not that each call lies in a tested module. | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | broader than its backing | narrow |
| U15-C002 | R | gives the pinned toolchain, the environment of record, the commands and one row per item Note: Toolchain, commands and one row per figure/table are generated and tested; 'the environment of record' (F.2) is still a placeholder shell awaiting the container package, so that part is unbacked. | gen:paper/generate_repro.py::toolchain gen:paper/generate_repro.py::commands test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version test:tests/test_paper.py::test_f_commands_exist_in_the_repository test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | broader than its backing | narrow |
| U15-C003 | S | supply configurations, attributes and a conditioning rule, and use the same calls | file:work-packages/interface-contract.md test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples test:tests/test_docs.py::test_runnable_blocks_execute | backed | keep |
| U15-C004 | S | the package documentation is the user's guide | file:docs/user-guide/overview.md test:tests/test_docs.py::test_runnable_blocks_exist_where_the_guide_promises_them | backed | keep |

### U16: paper Future work and final remark (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U16-C001 | S | Beyond one facet, K > 1 is built | test:tests/test_estimator.py::test_n_terms_above_one_is_implemented test:tests/test_estimator.py::test_k_terms_recovers_planted_facets | backed | keep |
| U16-C002 | M | whose generalized gradient is the convex hull of the active normals Note: no lemma or audit row states the generalized gradient of a max (Clarke: hull of active gradients); only a subgradient inclusion in axioms.py failure_mode; standard fact but unbacked here | none | unbacked | to the driver |
| U16-C003 | M | a nonsmooth search on the tangent cones of the ridges | definition | backed | keep |
| U16-C004 | M | GGP-compatible kernels, the generalization the search motivates | lemma:L16.31 definition | backed | keep |
| U16-C005 | M | needs a convergence theorem, and Q2 to Q4 need their own conditions | lemma:L15 definition | backed | keep |
| U16-S01 | M | should tolerate the kinks Note: prediction ('should') resting on the unbacked generalized-gradient claim; no lemma or test on nonsmooth search | none | unbacked | to the driver |

### U17: paper Acknowledgments and process (`paper/paper.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U17-C001 | P | Work was done in supervisor-gated work packages: a written scope the author approved before execution, and a review afterwards. | reading | backed | keep |
| U17-C002 | P | AI coding assistance (Claude Code, Anthropic) drafted code, derivation scripts and text inside those packages | reading | backed | keep |
| U17-C003 | L | in a process modelled on the harness described in [@zargham2026incose] Note: Audit row paper/reading_pass.yaml n=56 read only the Crossref abstract (LLM assistance regulated by deterministic testing, human sign-off) and its verdict is 'accessible (own work)', status supervisor, not 'supported'; 'modelled on the harness' is the author's own process claim. | bib:zargham2026incose | broader than its backing | narrow |
| U17-C004 | L | whose deterministic checks and named human approver are the verification mechanism this paper inherits Note: Same row n=56: abstract matches 'deterministic checks and named human approver', but the verdict is not 'supported' (listed for the supervisor) and 'the verification mechanism this paper inherits' goes past what the abstract states. | bib:zargham2026incose | broader than its backing | narrow |
| U17-S01 | M | The derivations are machine-checked. | test:tests/test_derivation.py::test_each_lemma_verifies test:tests/test_derivation.py::test_full_chain_runs | backed | keep |

### U18: paper Works cited (`paper/paper.ipynb`)

No claims (see above).

### U19: supp front (`paper/supporting_material.ipynb`)

No claims (see above).

### U20: supp Appendix A. Notation and terms (`paper/supporting_material.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U20-C001 | S | an input of the fit; the fit sees attributes and metrics only Note: Contract s3 backs 'configuration columns not fitted, carried as covariates' and HyperbolicTradeSpace.fit takes metrics; but TradeSpaceRegressor.fit(X, y) takes configurations as X (predictive.py), and 'the fit sees attributes' conflicts with C004 (the fit sees metrics; attributes only via the separate conditioning step). Narrow to: configuration is not an input of the frontier fit; the fit sees metrics. | file:work-packages/interface-contract.md | broader than its backing | narrow |
| U20-C002 | M | metrics; attributes are not conditioned, positive or oriented | file:work-packages/interface-contract.md lemma:L9.1 | backed | keep |
| U20-C003 | S | zero is tolerated in data and masked in the fit | test:tests/test_estimator.py::test_zero_metric_row test:tests/test_estimator.py::test_zero_metric_with_zero_exponent_equals_the_formal_limit | backed | keep |
| U20-C004 | S | part of the fit; the fit consumes metrics | file:work-packages/interface-contract.md | backed | keep |
| U20-C005 | M | a probability or a bounded score; V above 1 is possible at finite temperature | lemma:L1.5 lemma:L1.7 lemma:L5.15 glossary:invariant-value | backed | keep |
| U20-C006 | M | its logarithm is affine in the log-metrics | lemma:L10.19 lemma:L10.9 lemma:L1.4 glossary:monomial | backed | keep |
| U20-C007 | M | the invariant, which is a root of the sum | registered:C018 lemma:L10.7 glossary:posynomial | backed | keep |
| U20-C008 | M | a function of the class closed under sums, products, positive powers and maxima that contains the posynomials | lemma:L16.31 bib:boyd2007tutorial glossary:generalized-posynomial | backed | keep |
| U20-C009 | M | a name for the fitted reference surface, which is a level set of a posynomial Note: Level set of a posynomial holds at finite kappa (L10.7: exp(kappa Phi_K) = sum of monomials = 1). At the default kappa = infinity (sharp weights) the surface is max_k(monomial_k) = 1, a level set of a generalized posynomial, not of a posynomial (L10.18). Narrow to 'finite term temperature' or say 'of a posynomial (of the max of monomials at infinite term temperature)' | lemma:L10.7 lemma:L10.18 glossary:fitted-reference-surface | broader than its backing | to the driver |
| U20-C010 | M | the logarithmic change of variables makes it a convex program Note: Backed for a geometric program (I13 via L4.23/L4.24: log change gives the convex form). The same fragment also stands in the generalized-geometric-program entry, where no step states that a GGP becomes convex under the log change (Boyd 2007 s5.4 only, not in an audit row) | lemma:L4.24 lemma:L4.23 | broader than its backing | to the driver |
| U20-C011 | M | the several-facet fit as one program, which is not convex in the terms (L16) Note: L16 (i) shows the soft-weight (finite kappa, tau=kappa=1, two terms) objective is not convex 'in general' by an exact instance. No step covers the sharp-weight (kappa = infinity, minimum over facets) several-facet fit; I13 failure_mode says it is not a GP as a whole, which is not a nonconvexity proof | lemma:L16.37 lemma:L16.35 lemma:L16.36 glossary:geometric-program | broader than its backing | to the driver |
| U20-C012 | M | with the weights given, the fit of all terms is a generalized geometric program | lemma:L16.49 lemma:L16.31 lemma:L4.18 lemma:L4.21 | backed | keep |
| U20-C013 | M | and added variables turn it into a geometric program Note: No lemma step, ledger entry or audit row states the GGP-to-GP reduction by added variables: I15 cites Boyd 2007 s5.3/5.4 only for the definition; reading_pass n=37 read s5.3 and s8; references-verified.md records s5.4 as 'any GP is a GGP'. Add a reading_pass row on s5.4 or drop the clause | none | unbacked | to the driver |
| U20-C014 | L | the older use of the phrase for signomial programs Note: Lead only: references-verified.md says Boyd 2007 s9.1 notes some authors use the name for the wider nonconvex class; test_build_generated.py only asserts the word 'signomial' is in the not field. No audit row (prior_art/reading_pass) with verdict supported for this sentence | none | unbacked | drop |
| U20-C015 | M | a design problem that uses the fitted model is one, and so is the fit with its weights given Note: The fit-with-weights-given half is backed (see C012). 'A design problem that uses the fitted model is one' has no step: the model part is a (generalized) posynomial in m (L10.7, L10.18) but the design problem is a GGP only if the objective, other constraints and the map from design variables to metrics are GGP-compatible; the black-box configuration-to-attributes map is not | lemma:L16.49 lemma:L10.7 | broader than its backing | to the driver |
| U20-C016 | M | the level set V = 1 of the fitted invariant, where the posynomial sum equals one Note: definition of the surface as V = 1 is fine (L1.6); the gloss 'where the posynomial sum equals one' holds for finite kappa (L10.7) and only in the limit at kappa = infinity (max of monomials = 1, L10.18) | lemma:L10.7 lemma:L1.6 glossary:fitted-reference-surface | broader than its backing | to the driver |
| U20-C017 | M | the Pareto boundary, or a bound that no design exceeds | lemma:L11.17 lemma:L5.15 glossary:fitted-reference-surface | backed | keep |
| U20-C018 | M | the hyperplane of the infinite-temperature fit, found by a linear program | lemma:L12.9 lemma:L12.31 lemma:L5.24 test:tests/test_solvers.py::test_lp_hand_built test:tests/test_solvers.py::test_slsqp_agrees_with_lp glossary:supporting-envelope | backed | keep |
| U20-C019 | M | the potential evaluated at the design, a path-independent difference | registered:C005 registered:C004 glossary:energy-differential | backed | keep |
| U20-C020 | M | the single-metric scaling that carries the design to V = 1 | lemma:L7.7 lemma:L7.8 glossary:improvement-factor | backed | keep |
| U20-C021 | M | the reversible map from metrics to (Z, log V) | registered:C010 lemma:L8.14 glossary:chart | backed | keep |
| U20-C022 | M | defined for a row with a zero metric | test:tests/test_estimator.py::test_zero_metric_row test:tests/test_estimator.py::test_zero_metric_with_zero_exponent_equals_the_formal_limit lemma:L9.4 | backed | keep |
| U20-C023 | M | the Helmert log-ratio coordinates of the chart | lemma:L8.4 test:tests/test_coordinates.py::test_helmert_orthonormal_kernel glossary:position-along-the-frontier | backed | keep |
| U20-C024 | M | a noise level or a model parameter fitted from the data | test:tests/test_sklearn_compat.py::test_init_stores_parameters_verbatim lemma:L6.8 glossary:temperature | backed | keep |
| U20-C025 | M | the softmax weights of the rows in the log-mean-exp | lemma:L3.12 lemma:L3.15 | backed | keep |
| U20-C026 | M | the support of the exponent vector at infinite temperature | definition | backed | keep |
| U20-C027 | M | the derivative of one log-metric with respect to another along the facet; a ratio of exponents | lemma:L7.5 glossary:elasticity | backed | keep |
| U20-C028 | M | the maximizing term of the posynomial at the design | definition lemma:L13.1 lemma:L15.4 | backed | keep |
| U20-C029 | M | an identity that survives ties between scores | lemma:L13.3 lemma:L13.7 test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets | backed | keep |
| U20-C030 | M | gamma divided by twice the largest row norm Note: backed only for the augmented row (u_i, -1), norm sqrt(\|\|u_i\|\|^2 + 1) (L13 U >= 1; solvers.assignment_margin doctest); 'row norm' read as \|\|u_i\|\| gives a larger, unproved radius | lemma:L13.11 func:src/hyperbolic_trade_space/solvers.py::assignment_margin | broader than its backing | to the driver |
| U20-C031 | S | the smallest eigenvalue of the restricted Hessian of the objective on the simplex tangent space | test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue | backed | keep |
| U20-C032 | M | the barycentric image of the shares of three metrics (x = right + top / 2, y = sqrt(3) / 2 * top) | func:src/hyperbolic_trade_space/plotting.py::plot_ternary test:tests/test_plotting.py::test_ternary_markers_sit_at_the_exponent_vectors | backed | keep |
| U20-C033 | M | a facet's exponent vector sums to one, so it is a point of the triangle | lemma:L1.1 func:src/hyperbolic_trade_space/plotting.py::plot_ternary test:tests/test_plotting.py::test_ternary_markers_sit_at_the_exponent_vectors | backed | keep |
| U20-C034 | M | where that facet's V is largest at a fixed total | registered:C001 test:tests/test_plotting.py::test_ternary_fixed_total_identity_and_peak | backed | keep |
| U20-C035 | M | the three shares sum to one | definition test:tests/test_plotting.py::test_ternary_regions_partition_the_triangle | backed | keep |
| U20-C036 | M | the set of share positions where one facet attains the maximum in log V; the regions partition the triangle | definition test:tests/test_plotting.py::test_ternary_regions_partition_the_triangle | backed | keep |
| U20-C037 | S | compiled from `glossary.yaml` and never typed | gen:paper/generate_register.py::register_table test:tests/test_paper.py::test_register_table_equals_the_glossary test:tests/test_paper.py::test_register_committed_output_is_current | backed | keep |
| U20-S01 | S | an exponent below EPS_ZERO_EXPONENT Note: code and docstrings treat an exponent 'at or below' EPS_ZERO_EXPONENT (1e-12, pinned at test_estimator.py:511) as numerically zero; glossary says 'below'. Wording only: change to 'at or below' | test:tests/test_estimator.py::test_zero_metric_with_zero_exponent_equals_the_formal_limit func:src/hyperbolic_trade_space/estimator.py::EPS_ZERO_EXPONENT | broader than its backing | narrow |

### U21: supp Appendix B. Proofs, step for step with their scripts (`paper/supporting_material.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U21-C001 | S | Each proof is one file of `derivation/`, and each step of the proof is one line of that file. | test:tests/test_proof_map.py::test_record_holds_every_step_with_tag_prose_and_code test:tests/test_proof_map.py::test_an_untagged_assert_in_verify_fails test:tests/test_paper.py::test_appendix_b_lines_resolve_to_the_scripts_text | backed | keep |
| U21-C002 | S | The address of a step is its file and its tag | test:tests/test_paper.py::test_appendix_b_lines_resolve_to_the_scripts_text test:tests/test_paper.py::test_every_step_tag_of_the_record_appears_once_in_a_proof_and_none_is_empty | backed | keep |
| U21-C003 | S | and the tag is unique within the file. | test:tests/test_proof_map.py::test_a_duplicate_tag_fails | backed | keep |
| U21-C004 | R | The record holds 18 results in 17 files and 364 steps. | gen:paper/generate_proofs.py::how_to_read test:tests/test_paper.py::test_appendix_b_shows_every_result_of_the_record_with_derived_counts test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C005 | S | Every step is a line of code, including a step that cites a result | test:tests/test_proof_map.py::test_record_holds_every_step_with_tag_prose_and_code | backed | keep |
| U21-C006 | S | **computed** (244 steps): SymPy derives the step's condition and the line asserts it. | test:tests/test_proof_map.py::test_a_changed_script_step_fails_naming_the_step test:tests/test_proof_map.py::test_a_falsified_fact_breaks_the_step_that_rests_on_it test:tests/test_paper.py::test_proof_kinds_are_compiled_from_the_ledger_and_the_earlier_proofs | backed | keep |
| U21-C007 | S | **by a declared axiom** (111 steps): the line applies an entry of the axiom ledger that the script imported by name | test:tests/test_proof_map.py::test_imported_applied_and_declared_ledger_names_are_the_same_set test:tests/test_paper.py::test_proof_kinds_are_compiled_from_the_ledger_and_the_earlier_proofs | backed | keep |
| U21-C008 | S | the entry's wording and citation are shown beside the step, and the link gives the import line | test:tests/test_paper.py::test_proof_kinds_are_compiled_from_the_ledger_and_the_earlier_proofs | backed | keep |
| U21-C009 | S | **by a proved result** (9 steps): the line applies the result of an earlier proof that the script imported | test:tests/test_proof_map.py::test_the_four_dependencies_are_declared_by_import_and_applied_by_steps test:tests/test_proof_map.py::test_an_imported_result_that_no_step_applies_fails test:tests/test_paper.py::test_proof_kinds_are_compiled_from_the_ledger_and_the_earlier_proofs | backed | keep |
| U21-C010 | S | There is no kind for an argument made only in prose. | test:tests/test_proof_map.py::test_record_holds_every_step_with_tag_prose_and_code test:tests/test_proof_map.py::test_an_untagged_assert_in_verify_fails | backed | keep |
| U21-C011 | S | A step that SymPy cannot derive is an explicit hypothesis or an entry of the ledger. | test:tests/test_proof_map.py::test_a_hypothesis_must_quote_the_statement test:tests/test_proof_map.py::test_every_hypothesis_of_the_statements_is_listed_in_the_record test:tests/test_proof_map.py::test_a_symbol_with_a_sign_assumption_made_directly_fails | backed | keep |
| U21-C012 | R | Two results may share a file (L14 proves Proposition 3 and Corollary 4) | gen:paper/generate_proofs.py::proof_map test:tests/test_proof_map.py::test_a_result_sharing_a_file_owns_its_own_steps | backed | keep |
| U21-C013 | S | each names the same file and owns its own steps. | test:tests/test_proof_map.py::test_a_result_sharing_a_file_owns_its_own_steps test:tests/test_paper.py::test_appendix_b_names_each_results_file_statement_and_hypotheses | backed | keep |
| U21-C014 | S | every step of the prose has exactly one line of code, the lines are in the order of the prose | test:tests/test_paper.py::test_every_step_tag_of_the_record_appears_once_in_a_proof_and_none_is_empty test:tests/test_proof_map.py::test_the_order_of_steps_in_the_file_is_the_tag_order test:tests/test_paper.py::test_appendix_b_lines_resolve_to_the_scripts_text test:tests/test_proof_map.py::test_a_gap_in_the_numbering_fails | backed | keep |
| U21-C015 | S | every computed line passes, and neither a line nor a sentence can change without the checker reporting the step. | test:tests/test_proof_map.py::test_checker_passes_on_the_committed_record test:tests/test_proof_map.py::test_a_changed_script_step_fails_naming_the_step test:tests/test_proof_map.py::test_a_changed_prose_step_fails_naming_the_step | backed | keep |
| U21-C016 | S | What it cannot establish is that a sentence means what its line computes | definition | backed | keep |
| U21-C017 | M | L1. Homogeneity and invariant form: V(k m) = k V(m), V(m / V) = 1 | lemma:L1 | backed | keep |
| U21-C018 | M | L2. Uniform shift: J_tau(w; U + c 1^T) = J_tau(w; U) + c | lemma:L2 | backed | keep |
| U21-C019 | M | L3. gradient of the soft-maximum objective and the full simplex KKT conditions | lemma:L3 | backed | keep |
| U21-C020 | M | L4. convexity of the soft-maximum objective (second directional derivative = tau Var_p) | lemma:L4 | backed | keep |
| U21-C021 | M | L5. LSE = LME + log(n)/tau; mean <= LME <= max; tau limits | lemma:L5 | backed | keep |
| U21-C022 | M | L6. Gaussian cumulant of a weighted noise sum | lemma:L6 | backed | keep |
| U21-C023 | M | L7. Elasticities -w_k/w_j on the frontier; improvement factor V^(-1/w_j) | lemma:L7 | backed | keep |
| U21-C024 | M | L8. Sum-zero (Helmert-type) chart and scale/shape bijection | lemma:L8 | backed | keep |
| U21-C025 | M | L9. Pull-back: V = e^{w.b - beta} prod_j (a_j + s_j)^{w_j alpha_j} | lemma:L9 | backed | keep |
| U21-C026 | M | L10. Extension Phi_K: shift equivariance, K = 1 reduction, kappa -> infinity = max | lemma:L10 | backed | keep |
| U21-C027 | M | L11. A V-maximizer is Pareto-efficient (weighted-sum scalarization; converse not claimed) | lemma:L11 | backed | keep |
| U21-C028 | M | L12. facet first-order gap: 0 <= f(w) - f* <= G, G = 0 iff the simplex KKT holds | lemma:L12 | backed | keep |
| U21-C029 | M | L13. assignment margin: score changes below gamma/2 keep the maximizing facets; explicit radius | lemma:L13 | backed | keep |
| U21-C030 | M | L14. Proposition 3 \| `lemma_14_assignment_stable.py` \| 16 \| 9 \| 6 \| 1 \| | lemma:L14 gen:paper/generate_proofs.py::proof_map test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C031 | M | L15. descent (Level 1): reassignment and facet refit do not increase the mean slack | lemma:L15 | backed | keep |
| U21-C032 | M | L16. soft-weight alternation: symmetry, the fixed-weight bound and the generalized posynomial | lemma:L16 | backed | keep |
| U21-C033 | M | L17. the soft-fit certificate: Hessian D - kappa M and the second-order test | lemma:L17 | backed | keep |
| U21-C034 | R | \| L1. Homogeneity and invariant form: V(k m) = k V(m), V(m / V) = 1 \| `lemma_01_homogeneity.py` \| 8 \| 4 \| 4 \| 0 \| | gen:paper/generate_proofs.py::proof_map test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C035 | R | \| L3. gradient of the soft-maximum objective and the full simplex KKT conditions \| `lemma_03_gradient_kkt.py` \| 35 \| 26 \| 9 \| 0 \| | gen:paper/generate_proofs.py::proof_map test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C036 | R | \| L16. soft-weight alternation: symmetry, the fixed-weight bound and the generalized posynomial \| `lemma_16_soft_fit_alternation.py` \| 49 \| 31 \| 18 \| 0 \| | gen:paper/generate_proofs.py::proof_map test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C037 | R | \| L17. the soft-fit certificate: Hessian D - kappa M and the second-order test \| `lemma_17_soft_fit_certificate.py` \| 52 \| 44 \| 8 \| 0 \| | gen:paper/generate_proofs.py::proof_map test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C038 | S | every facet is fitted against every design, each offset | test:tests/test_solvers.py::test_corollary_bound_on_every_planted_fit test:tests/test_solvers.py::test_r1_planted_certificates | backed | keep |
| U21-C039 | S | each offset $\beta_k=J_\tau(Uw_k)$ being the support over all rows | test:tests/test_solvers.py::test_corollary_bound_on_every_planted_fit test:tests/test_solvers.py::test_r1_planted_certificates test:tests/test_solvers.py::test_terms_k1_equals_slsqp_and_degenerate | backed | keep |
| U21-C040 | S | the fit minimizes the mean slack Note: Tests pin the objective as the mean slack and a non-increasing history, not that the fit attains the minimum: alternation with restarts reaches a local one, L16 does not prove convergence, and the tangent step is not monotone. | test:tests/test_solvers.py::test_terms_monotone_history_and_stops test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized | broader than its backing | narrow |
| U21-C041 | S | The alternation takes weights from the current model and then solves one program for all terms | func:src/hyperbolic_trade_space/solvers.py::soft_weights lemma:L16.11 test:tests/test_soft_fit.py::test_r1_the_soft_objective_never_rises_across_the_history | backed | keep |
| U21-C042 | S | The package uses the sharp limit of the weights, one label per design | test:tests/test_soft_fit.py::test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone test:tests/test_soft_fit.py::test_r3_the_limit_kappa_to_infinity_is_the_label_fit | backed | keep |
| U21-C043 | S | the program then separates into one convex program per term | lemma:L16.44 lemma:L4 | backed | keep |
| U21-C044 | S | For each restart the package starts from random centres in the chart | func:src/hyperbolic_trade_space/solvers.py::solve_terms | backed | keep |
| U21-C045 | S | if the mean slack rose, stop with the previous state | test:tests/test_solvers.py::test_guard_stop_returns_the_consistent_previous_state | backed | keep |
| U21-C046 | S | it returns the restart with the smallest mean slack Note: solve_terms returns min(runs, key=objective) but no test pins best-of-restarts (test_n_restarts_default only checks 5 == default) | none | unbacked | drop |
| U21-C047 | M | the fixed-weight objective bounds the soft model's mean slack from above and equals it at the model the weights came from | lemma:L16.43 lemma:L16.41 | backed | keep |
| U21-C048 | M | it is a generalized posynomial in $e^{w}$, so its minimization is a generalized geometric program | lemma:L16.49 lemma:L16.31 | backed | keep |
| U21-C049 | L | a generalized geometric program in the sense of Boyd et al. [@boyd2007tutorial] | bib:boyd2007tutorial file:paper/reading_pass.yaml | backed | keep |
| U21-C050 | M | L16 does not prove that the alternation converges. | lemma:L16 | backed | keep |
| U21-C051 | M | the gradient and the Hessian $D-\kappa M$ of its objective | lemma:L17.34 lemma:L17.35 | backed | keep |
| U21-C052 | M | the second-order test that certifies a strict local minimizer | lemma:L17.44 | backed | keep |
| U21-C053 | S | The label belongs to the package and not to the model | test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis file:work-packages/interface-contract.md | backed | keep |
| U21-C054 | P | which facet dominates a design is analysis of the fitted model | test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis file:work-packages/interface-contract.md | backed | keep |
| U21-C055 | S | The checker passes only when: every proof names one file; every step of every file belongs to exactly one proof | test:tests/test_proof_map.py::test_every_lemma_file_is_in_the_record_in_chain_order test:tests/test_proof_map.py::test_a_result_sharing_a_file_owns_its_own_steps test:tests/test_paper.py::test_every_step_tag_of_the_record_appears_once_in_a_proof_and_none_is_empty | backed | keep |
| U21-C056 | S | the prose steps and the script steps correspond one to one and in order | test:tests/test_proof_map.py::test_the_order_of_steps_in_the_file_is_the_tag_order test:tests/test_proof_map.py::test_a_gap_in_the_numbering_fails test:tests/test_proof_map.py::test_an_untagged_assert_in_verify_fails | backed | keep |
| U21-C057 | S | every step by a declared axiom applies an entry that exists in the ledger and that the file imports | test:tests/test_proof_map.py::test_a_ledger_import_that_no_step_applies_fails test:tests/test_proof_map.py::test_a_ledger_entry_used_on_an_untagged_line_fails test:tests/test_proof_map.py::test_importing_a_name_that_is_not_a_ledger_entry_fails | backed | keep |
| U21-C058 | S | a proved result is imported from an earlier proof and applied by a step; no premise hides in a signed symbol | test:tests/test_proof_map.py::test_an_imported_result_that_no_step_applies_fails test:tests/test_proof_map.py::test_a_proved_result_used_on_an_untagged_line_fails test:tests/test_proof_map.py::test_a_symbol_with_a_sign_assumption_made_directly_fails | backed | keep |
| U21-C059 | S | the fingerprint of each step (its tag, prose and line of code) and of each ledger entry equals the record's. | test:tests/test_proof_map.py::test_a_changed_script_step_fails_naming_the_step test:tests/test_proof_map.py::test_a_changed_prose_step_fails_naming_the_step test:tests/test_proof_map.py::test_a_changed_ledger_entry_fails | backed | keep |
| U21-C060 | R | \| SHA-256 of the record \| `f5466ab7cffd7a96ab858edb06621dfddd5dc6b15ed9c1a740613d92b1989d0c` \| | gen:paper/generate_proofs.py::checker test:tests/test_paper.py::test_appendix_b_closes_with_the_checkers_table | backed | keep |
| U21-C061 | R | \| Record version \| 2 \| | gen:paper/generate_proofs.py::checker test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C062 | R | \| Lemma files, steps \| 17, 364 \| | gen:paper/generate_proofs.py::checker test:tests/test_paper.py::test_appendix_b_closes_with_the_checkers_table | backed | keep |
| U21-C063 | R | \| Ledger entries fingerprinted \| 30 \| | gen:paper/generate_proofs.py::checker test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C064 | S | \| Check the scripts against the record \| `uv run python -m derivation.proofmap` \| | test:tests/test_proof_map.py::test_checker_passes_on_the_committed_record test:tests/test_paper.py::test_appendix_b_closes_with_the_checkers_table | backed | keep |
| U21-C065 | S | \| Also run every computed step \| `uv run python -m derivation.proofmap --execute` \| Note: --execute exists in proofmap.main/run_chain_check but no test exercises it or asserts its behaviour | none | unbacked | drop |
| U21-C066 | S | \| Refresh the record (deliberate; prints what moved) \| `uv run python -m derivation.proofmap --update` \| | test:tests/test_proof_map.py::test_update_rewrites_the_record_and_prints_the_steps_that_moved | backed | keep |
| U21-C067 | R | \| `lemma_04_convexity.py` \| A1, A2, A3, I11, I13 \| L3_RESULT \| L4_RESULT \| 24 \| 0 \| | gen:paper/generate_proofs.py::checker test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C068 | R | \| `lemma_14_assignment_stable.py` \| A8, R2 \| L12_RESULT, L13_RESULT \| L14_RESULT \| 20 \| 1 \| | gen:paper/generate_proofs.py::checker test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C069 | R | \| `lemma_13_margin.py` \| F12, I9, R2 \| none \| L13_RESULT \| 17 \| 10 \| | gen:paper/generate_proofs.py::checker test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |
| U21-C070 | R | \| `lemma_11_pareto.py` \| A2 \| none \| none \| 20 \| 5 \| | gen:paper/generate_proofs.py::checker test:tests/test_paper.py::test_appendix_b_committed_output_is_current | backed | keep |

### U22: supp Appendix C. The case's model: how the table of metrics came to be (`paper/supporting_material.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U22-C001 | S | The repository keeps:** the SysML model file, the evaluation code, the experiment ledger and the data. | test:tests/test_paper.py::test_each_attribute_has_a_producer_that_exists_in_its_file test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C002 | R | \| Kp \| 0.2 \| 2 \| 0.2005 \| 1.999 \| 0.03011 \| 0.999 \| | gen:paper/generate_model.py::configuration_space test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C003 | R | \| wheel_class \| small, medium, large \| small: 344, medium: 345, large: 311 \| small: 344, medium: 345, large: 311 \| | gen:paper/generate_model.py::configuration_space test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C004 | R | \| st_grade \| coarse, medium, fine \| coarse: 347, medium: 342, fine: 311 \| coarse: 347, medium: 342, fine: 311 \| | gen:paper/generate_model.py::configuration_space test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C005 | S | \| settling time \| `adcs_sim.py` \| `simulate_adcs` \| measured: on the integrated slew \| Note: file and name pinned (name occurs in file); 'measured: on the integrated slew' is a typed label, not asserted by a test | gen:paper/generate_model.py::attribute_sources test:tests/test_paper.py::test_each_attribute_has_a_producer_that_exists_in_its_file | broader than its backing | narrow |
| U22-C006 | S | \| pointing error \| `cubesat_model.py` \| `pointing_error_deg` \| computed: pointing budget \| Note: file and name pinned; 'computed: pointing budget' is a typed label, not asserted by a test | gen:paper/generate_model.py::attribute_sources test:tests/test_paper.py::test_each_attribute_has_a_producer_that_exists_in_its_file | broader than its backing | narrow |
| U22-C007 | S | \| total mass \| `cubesat_tradespace.sysml` \| `MassAccounting` \| computed: accounting \| Note: name MassAccounting occurs in the sysml and a mass identity test exists; 'computed: accounting' label itself is typed, not asserted | gen:paper/generate_model.py::attribute_sources test:tests/test_paper.py::test_each_attribute_has_a_producer_that_exists_in_its_file test:tests/test_cubesat_model.py::test_mass_accounting_identity | broader than its backing | narrow |
| U22-C008 | R | \| power margin \| power_margin_w \| W \| yes \| | gen:paper/generate_model.py::evaluation test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C009 | R | \| momentum_ok \| 188 \| 165 \| 811 \| | gen:paper/generate_model.py::feasibility test:tests/test_case.py::test_feasibility_table_cascade test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C010 | R | \| all attributes positive \| 131 \| 105 \| 706 \| | gen:paper/generate_model.py::feasibility test:tests/test_case.py::test_feasibility_table_cascade test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C011 | R | \| power_ok \| 0 \| 0 \| 976 \| | gen:paper/generate_model.py::feasibility test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C012 | R | \| momentum_ok \| 81 \| 81 \| 897 \| | gen:paper/generate_model.py::feasibility test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C013 | R | \| all attributes positive \| 131 \| 117 \| 780 \| | gen:paper/generate_model.py::feasibility test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C014 | R | \| eclipse reserve \| direct \| 0.008278 \| 51.95 \| 1.305 \| 1 \| 0.004308 \| 3.503 \| | gen:paper/generate_model.py::conditioning test:tests/test_case.py::test_conditioning_table test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C015 | R | \| total mass \| reciprocal \| 11.9 \| 16.06 \| 0.06581 \| 1 \| 0.07706 \| 7.388 \| | gen:paper/generate_model.py::conditioning test:tests/test_case.py::test_conditioning_table test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C016 | R | \| settling time \| reciprocal \| 7.517 \| 597.9 \| 0.9222 \| 1 \| 0.1297 \| 14.92 \| | gen:paper/generate_model.py::conditioning test:tests/test_case.py::test_conditioning_table test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C017 | M | Each metric is `m_j = exp((o_j log(a_j + s_j) - c_j) / k_j)` for attribute `a_j` | lemma:L9.1 test:tests/test_paper.py::test_the_metric_rule_reproduces_the_table_of_metrics gen:paper/generate_model.py::metric_table | backed | keep |
| U22-C018 | S | The table of metrics, one row per kept design and one column per metric, is where the model ends | definition | backed | keep |
| U22-C019 | R | Dataset cubesat-primary: 706 designs by 10 metrics; the first 5 rows: | gen:paper/generate_model.py::metric_table test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C020 | R | Dataset cubesat-stock: 780 designs by 10 metrics; the first 5 rows: | gen:paper/generate_model.py::metric_table test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C021 | R | \| 0 \| 1.099 \| 0.5606 \| 1.859 \| 0.2572 \| 1.656 \| 0.9351 \| 1.299 \| 1.587 \| 0.2554 \| 1.342 \| | gen:paper/generate_model.py::metric_table test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C022 | R | \| 0 \| 0.3214 \| 0.3075 \| 0.41 \| 0.2446 \| 3.123 \| 1.019 \| 1.139 \| 1.577 \| 0.5293 \| 1.338 \| | gen:paper/generate_model.py::metric_table test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-C023 | R | \| cubesat-primary \| primary \| examples/adcs/data/adcs_designs_cubesat_gains.csv \| adopted-adcs_designs_cubesat_gains \| | gen:paper/generate_model.py::datasets test:tests/test_paper.py::test_c_defines_the_dataset_labels_and_names_each_dataset_once test:tests/test_paper.py::test_c_committed_output_is_current file:examples/adcs/experiments/ledger/ledger.jsonl | backed | keep |
| U22-C024 | R | \| 1000 \| 706 \| 4dc4ae0b8ebe5e7a8aa747f7a8c11fa7d6b8adb316594c86ae2bda960a6f6ee4 \| 4dc4ae0b8ebe5e7a8aa747f7a8c11fa7d6b8adb316594c86ae2bda960a6f6ee4 \| | gen:paper/generate_model.py::datasets test:tests/test_paper.py::test_c_committed_output_is_current file:examples/adcs/experiments/ledger/ledger.jsonl test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data | backed | keep |
| U22-C025 | R | \| 1000 \| 780 \| 9450713cd78cd6e0ce60ebcce0faa78388e53eba14256192a50b9ce5a9517bfa \| 9450713cd78cd6e0ce60ebcce0faa78388e53eba14256192a50b9ce5a9517bfa \| | gen:paper/generate_model.py::datasets test:tests/test_paper.py::test_c_committed_output_is_current file:examples/adcs/experiments/ledger/ledger.jsonl test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data | backed | keep |
| U22-C026 | R | \| planted-3-facet \| synthetic \| none \| none \| make_frontier_data(n_samples=900, n_features=4, n_terms=3 | gen:paper/generate_model.py::datasets test:tests/test_paper.py::test_c_committed_output_is_current test:tests/test_paper.py::test_planted_table_agrees_with_the_reference_values test:tests/test_paper.py::test_planted_example_is_reproducible_and_has_known_facets | backed | keep |
| U22-C027 | R | \| facet 1 \| 0.5 \| 0.5 \| 0 \| 0 \| | gen:paper/generate_model.py::planted_example test:tests/test_paper.py::test_c_committed_output_is_current test:tests/test_paper.py::test_planted_example_is_reproducible_and_has_known_facets | backed | keep |
| U22-C028 | R | \| facet 2 \| 0 \| 0.5 \| 0.5 \| 0 \| | gen:paper/generate_model.py::planted_example test:tests/test_paper.py::test_c_committed_output_is_current test:tests/test_paper.py::test_planted_example_is_reproducible_and_has_known_facets | backed | keep |
| U22-C029 | R | \| facet 3 \| 0 \| 0 \| 0.5 \| 0.5 \| | gen:paper/generate_model.py::planted_example test:tests/test_paper.py::test_c_committed_output_is_current test:tests/test_paper.py::test_planted_example_is_reproducible_and_has_known_facets | backed | keep |
| U22-S01 | R | \| slew_deg \| 30 \| | gen:paper/generate_model.py::evaluation test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |
| U22-S02 | R | \| t_end_s \| 600 \| | gen:paper/generate_model.py::evaluation test:tests/test_paper.py::test_c_committed_output_is_current | backed | keep |

### U23: supp Appendix D. Extended results: what the method found in the table (`paper/supporting_material.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U23-C001 | R | \| 3 \| 0.45 \| 589 \| 6 \| 0.244 to 0.245 \| slew time \| | gen:paper/generate_results.py::temperature_selection test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C002 | R | \| 5.087 \| 0.40 \| 462 to 463 \| 6 \| 0.25 \| slew time \| | gen:paper/generate_results.py::temperature_selection test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C003 | R | \| 120.9 \| 0.02266 \| 3.94 to 3.96 \| 6 \| 0.211 \| total mass \| | gen:paper/generate_results.py::temperature_selection test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C004 | R | \| inf \| 0 \| 3.2 \| 6 \| 0.2228 \| total mass \| | gen:paper/generate_results.py::temperature_selection test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C005 | R | \| 3 \| 0.45 \| 719.3 \| 7 \| 0.417 \| control effort \| | gen:paper/generate_results.py::temperature_selection test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C006 | R | \| 14.63 \| 0.2897 \| 207 to 208 \| 6 \| 0.4212 \| control effort \| | gen:paper/generate_results.py::temperature_selection test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C007 | R | \| inf \| 0 \| 4.5 \| 6 \| 0.434 \| control effort \| | gen:paper/generate_results.py::temperature_selection test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C008 | R | \| 1 \| 38.1 \| 0.0262 \| 0.20 \| 0.09632 \| [706] \| [1.0] \| | gen:paper/generate_results.py::k_diagnostics test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C009 | R | \| 2 \| 113.2 \| 0.0088 \| 0.138 \| 0.0963 to 0.0992 \| [374, 332] \| [0.629, 0.371] \| | gen:paper/generate_results.py::k_diagnostics test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C010 | R | \| 3 \| 195.2 \| 0.0051 \| 0.117 \| 0.095 to 0.098 \| [201, 188, 317] \| [0.089, 0.133, 0.778] \| | gen:paper/generate_results.py::k_diagnostics test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C011 | R | \| 1 \| 41.72 \| 0.024 \| 0.1312 \| 0.104 to 0.105 \| [780] \| [1.0] \| | gen:paper/generate_results.py::k_diagnostics test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C012 | R | \| 2 \| 78.75 \| 0.0127 \| 0.1059 \| 0.0910 to 0.0936 \| [390, 390] \| [0.694, 0.306] \| | gen:paper/generate_results.py::k_diagnostics test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C013 | R | \| 3 \| 162.8 \| 0.0061 \| 0.093 \| 0.0923 to 0.0936 \| [284, 149, 347] \| [0.077, 0.59, 0.333] \| | gen:paper/generate_results.py::k_diagnostics test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C014 | R | \| 1 \| 201 to 202 \| control effort, slew time, energy balance, pointing error, depth of discharge, settling time \| 6 \| | gen:paper/generate_results.py::exponents_and_facets test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C015 | R | \| 2 \| 187 to 188 \| energy balance, control effort, slew time, settling time, pointing error, depth of discharge \| 6 \| | gen:paper/generate_results.py::exponents_and_facets test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C016 | R | \| 3 \| 317 \| peak slew power, total mass, pointing error, slew time, depth of discharge, power margin, settling time \| 7 \| | gen:paper/generate_results.py::exponents_and_facets test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C017 | R | \| 1 \| 284 \| control effort, slew time, settling time, energy balance, pointing error, depth of discharge \| 6 \| | gen:paper/generate_results.py::exponents_and_facets test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C018 | R | \| 2 \| 149 \| peak slew power, slew time, pointing error, total mass, power margin, depth of discharge, control effort \| 7 \| | gen:paper/generate_results.py::exponents_and_facets test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C019 | R | \| 3 \| 347 \| energy balance, control effort, slew time, settling time, depth of discharge \| 5 \| | gen:paper/generate_results.py::exponents_and_facets test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C020 | R | \| tau, frac_above_, n_eff_ \| 38.1, 0.096, 16 \| 41.7, 0.104 to 0.105, 14.5 \| | gen:paper/generate_results.py::regime_comparison test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C021 | R | \| band 1/tau, near-frontier designs \| 0.0262, 51 to 52 \| 0.0240, 103 \| | gen:paper/generate_results.py::regime_comparison test:tests/test_case.py::test_regime_comparison_on_frozen_data test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C022 | R | \| settling time, total mass \| -0.54 (-0.34 to -0.33) \| -0.12 (-0.02) \| | gen:paper/generate_results.py::regime_comparison test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C023 | R | \| slew time, total mass \| -0.48 (-0.34 to -0.33) \| -0.10 (-0.03) \| | gen:paper/generate_results.py::regime_comparison test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C024 | R | \| pointing error, control effort \| -0.36 (-0.48) \| -0.70 (-0.77) \| | gen:paper/generate_results.py::regime_comparison test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C025 | R | \| settling time, pointing error \| +0.18 (+0.19 to +0.20) \| +0.69 (+0.75) \| | gen:paper/generate_results.py::regime_comparison test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C026 | R | \| slew time, control effort \| -0.87 (-0.84 to -0.83) \| -0.96 (-0.95) \| | gen:paper/generate_results.py::regime_comparison test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C027 | R | \| settling time, slew time \| +0.90 to +0.91 (+0.87 to +0.88) \| +0.99 (+0.99) \| | gen:paper/generate_results.py::regime_comparison test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C028 | R | \| contending set \| total mass, slew time, energy balance, control effort, pointing error, depth of discharge \| control effort, slew time, power margin, settling time, pointing error, eclipse reserve \| | gen:paper/generate_results.py::regime_comparison test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C029 | R | \| target fraction halved \| target 0.05 \| 65.68 \| 0.054 to 0.057 \| 5.8 \| 6 \| | gen:paper/generate_results.py::sensitivity_variants test:tests/test_paper.py::test_cr3_the_target_and_the_band_carry_their_reason_and_the_sensitivity_holds test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C030 | R | \| target fraction doubled \| target 0.2 \| 18.43 \| 0.20 \| 90 \| 6 \| | gen:paper/generate_results.py::sensitivity_variants test:tests/test_paper.py::test_cr3_the_target_and_the_band_carry_their_reason_and_the_sensitivity_holds test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C031 | R | \| robust scaler \| log-IQR scaling \| 54.77 \| 0.1048 \| 29 \| 6 \| peak slew power, total mass, pointing error, eclipse reserve, energy balance, settling time \| total mass \| 3 \| | gen:paper/generate_results.py::sensitivity_variants test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C032 | R | \| view: four metrics \| 4 attributes \| 15.37 \| 0.11 \| 20 to 21 \| 4 \| control effort, slew time, pointing error, total mass \| control effort \| 4 \| | gen:paper/generate_results.py::sensitivity_variants test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C033 | R | \| view: settling time and slew time \| 2 attributes \| 6.201 \| 0.09773 \| 23 to 24 \| 2 \| slew time, settling time \| settling time \| 1 \| | gen:paper/generate_results.py::sensitivity_variants test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C034 | R | \| robust scaler \| log-IQR scaling \| 59.98 \| 0.10 \| 9.6 \| 5 \| control effort, slew time, energy balance, pointing error, eclipse reserve \| control effort \| 4 \| | gen:paper/generate_results.py::sensitivity_variants test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C035 | R | \| view: four metrics \| 4 attributes \| 22.1 \| 0.09744 \| 15 \| 2 \| control effort, slew time \| control effort \| 2 \| | gen:paper/generate_results.py::sensitivity_variants test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C036 | R | \| small \| 191 \| 336.5 \| 0.09424 \| 5.467 \| 6 \| pointing error, total mass, peak slew power, depth of discharge, power margin, control effort \| pointing error \| | gen:paper/generate_results.py::refits_by_category test:tests/test_case.py::test_regime_comparison_on_frozen_data test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C037 | R | \| large \| 267 \| 113.2 \| 0.1086 \| 15 \| 7 \| power margin, total mass, pointing error, depth of discharge, control effort, peak slew power, slew time \| power margin \| | gen:paper/generate_results.py::refits_by_category test:tests/test_case.py::test_regime_comparison_on_frozen_data test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C038 | R | \| medium \| 279 \| 66 to 79 \| 0.093 to 0.10 \| 11 to 13 \| 6 \| control effort, slew time, power margin, pointing error, depth of discharge, total mass \| control effort \| | gen:paper/generate_results.py::refits_by_category test:tests/test_adcs_enrichment.py::test_regime_comparison_stock_gains test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C039 | R | \| fast_effort_hungry \| large \| medium \| -0.115 \| -0.11 \| 0.67 \| -4.4 \| | gen:paper/generate_results.py::candidate_designs test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C040 | R | \| precise_heavy_sensor \| large \| fine \| -0.0717 to -0.0705 \| -0.0692 to -0.0681 \| 0.772 to 0.778 \| -2.7 \| | gen:paper/generate_results.py::candidate_designs test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C041 | R | \| light_slow \| small \| coarse \| -0.144 \| -0.134 \| 0.59 \| -5.5 \| | gen:paper/generate_results.py::candidate_designs test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C042 | S | `certified`: the assignment is fixed, residuals and gaps are within tolerance, no facet is empty and the margin is positive; levels 1 to 3 hold. | func:src/hyperbolic_trade_space/solvers.py::Termination test:tests/test_estimator.py::test_termination_record_for_k_terms file:work-packages/interface-contract.md | backed | keep |
| U23-C043 | S | `stationary_without_margin`: the same with a zero margin or an empty facet; levels 1 and 2 only. | func:src/hyperbolic_trade_space/solvers.py::Termination test:tests/test_estimator.py::test_termination_record_for_k_terms test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets | backed | keep |
| U23-C044 | S | `uncertified`, `guard_stop` and `iteration_cap`: level 1 only, reported apart from certified. | func:src/hyperbolic_trade_space/solvers.py::Termination test:tests/test_solvers.py::test_iteration_cap_status test:tests/test_solvers.py::test_guard_stop_returns_the_consistent_previous_state test:tests/test_estimator.py::test_convergence_warning_keyed_to_iteration_cap | backed | keep |
| U23-C045 | S | `not_applicable`: a penalty, the tangent step or a single facet; the gaps are diagnostics. | func:src/hyperbolic_trade_space/solvers.py::Termination test:tests/test_solvers.py::test_not_applicable_statuses test:tests/test_soft_fit.py::test_r7_a_soft_fit_at_infinite_tau_is_not_applicable | backed | keep |
| U23-C046 | S | The record also holds the maximal gap, the Corollary bound, the margin, the stable radius and the shares. | func:src/hyperbolic_trade_space/solvers.py::Termination file:work-packages/interface-contract.toml test:tests/test_interface_contract.py::test_r1_termination_fields_statuses_and_report_fields | backed | keep |
| U23-C047 | R | \| 2 \| below 1e-12 \| certified \| 0.00083 to 0.0016 \| 6.8e-05 to 0.00013 \| below 1e-12 \| | gen:paper/generate_results.py::termination_records test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_k_terms_case.py::test_certificate_margin_and_radius_columns | backed | keep |
| U23-C048 | R | \| 3 \| below 1e-12 \| certified \| 0.00116 to 0.00149 \| 9.3e-05 to 0.00012 \| below 1e-12 \| | gen:paper/generate_results.py::termination_records test:tests/test_paper.py::test_facet_numbered_tables_are_current test:tests/test_k_terms_case.py::test_certificate_margin_and_radius_columns | backed | keep |
| U23-C049 | R | \| 3 \| 20 \| 0.05 \| 0.5863 \| 0.3678 \| [320, 340, 240] \| [0.397, 0.328, 0.276] \| below 1e-12 \| certified \| | gen:paper/generate_results.py::termination_records test:tests/test_paper.py::test_facet_numbered_tables_are_current | backed | keep |
| U23-C050 | M | The margin gamma is in score units, the scale of the band 1/tau; below the band, a change as small as the band can move a design to another facet. Note: L13.7 gives sufficiency only (score changes below gamma/2 keep the facets); 'a change as small as the band can move a design' is not stated (the lemma says the radius is not proved tight), and 'scale of the band 1/tau' is a reading, not a step | lemma:L13.7 lemma:L13.11 glossary:stable-radius | broader than its backing | to the driver |
| U23-C051 | M | far below it, a few designs sit on a seam and most do not. Note: gamma is the minimum gap (L13); 'far below the median gap, a few designs sit on a seam and most do not' is not in any step: a small min gap says one row is near a seam, not how many; only 'at least half have gap >= median' follows | lemma:L13 glossary:assignment-margin | broader than its backing | to the driver |
| U23-C052 | M | The stable radius is gamma divided by twice the largest norm of a row of the log-metrics with a final entry of minus one, so it is smaller than the margin and is sufficient, not tight. Note: radius = gamma/(2U) with U>=1 (hypothesis symbol U_ in L13) gives smaller than gamma and sufficient (L13.7, L13.11, doctest); 'not tight' is stronger than the lemma, which only declines to prove tightness | lemma:L13.11 lemma:L13.12 glossary:stable-radius func:src/hyperbolic_trade_space/solvers.py::assignment_margin | broader than its backing | to the driver |
| U23-C053 | R | \| 2 \| 0.00083 to 0.0016 \| 6.8e-05 to 0.00013 \| 0.0088 \| 0.50 \| | gen:paper/generate_results.py::margin_reading test:tests/test_paper.py::test_cr9_the_margin_and_the_radius_are_read_against_the_band_and_the_median_margin test:tests/test_k_terms_case.py::test_certificate_margin_and_radius_columns | backed | keep |
| U23-C054 | R | \| 3 \| 0.00022 to 0.0019 \| 1.8e-05 to 0.00016 \| 0.0051 \| 0.18 \| | gen:paper/generate_results.py::margin_reading test:tests/test_paper.py::test_cr9_the_margin_and_the_radius_are_read_against_the_band_and_the_median_margin test:tests/test_k_terms_case.py::test_certificate_margin_and_radius_columns | backed | keep |
| U23-C055 | R | \| 2 \| 0.0013 to 0.0016 \| 0.000103 to 0.000126 \| 0.0127 \| 0.23 \| | gen:paper/generate_results.py::margin_reading test:tests/test_paper.py::test_cr9_the_margin_and_the_radius_are_read_against_the_band_and_the_median_margin test:tests/test_k_terms_case.py::test_certificate_margin_and_radius_columns | backed | keep |
| U23-C056 | R | \| all attributes \| 10 \| 671 \| 706 \| 0.9504 \| | gen:paper/generate_results.py::nondominated test:tests/test_case.py::test_nondominated_counts_on_frozen_primary test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C057 | R | \| four metrics \| 4 \| 145 to 146 \| 706 \| 0.21 \| | gen:paper/generate_results.py::nondominated test:tests/test_case.py::test_nondominated_counts_on_frozen_primary test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C058 | R | \| settling time and slew time \| 2 \| 7 to 8 \| 706 \| 0.0099 to 0.011 \| | gen:paper/generate_results.py::nondominated test:tests/test_case.py::test_nondominated_counts_on_frozen_primary test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C059 | R | \| all attributes \| 10 \| 732 \| 780 \| 0.9385 \| | gen:paper/generate_results.py::nondominated test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C060 | R | \| settling time and slew time \| 2 \| 2 \| 780 \| 0.002564 \| | gen:paper/generate_results.py::nondominated test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C061 | R | \| proposal_1 \| -0.06901 \| -0.0906 to -0.0892 \| -0.0216 to -0.0202 \| 0.311 to 0.331 \| True \| 0.0880 to 0.0907 \| 1.4 \| False \| | gen:paper/generate_results.py::propose_predict_check test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results test:tests/test_case.py::test_predict_check_within_the_band | backed | keep |
| U23-C062 | R | \| proposal_2 \| -0.05764 \| -0.0807 to -0.0788 \| -0.0231 to -0.0211 \| 0.32 to 0.36 \| True \| 0.14 \| 2.2 \| False \| | gen:paper/generate_results.py::propose_predict_check test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results test:tests/test_case.py::test_predict_check_within_the_band | backed | keep |
| U23-C063 | R | \| proposal_3 \| -0.1624 \| -0.21 \| -0.0485 to -0.0454 \| 0.698 to 0.745 \| True \| 0.20 \| 3.1 \| False \| | gen:paper/generate_results.py::propose_predict_check test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results test:tests/test_case.py::test_predict_check_within_the_band | backed | keep |
| U23-C064 | S | The settling time and the slew time are read off the accepted steps of an adaptive integration | func:examples/adcs/adcs_sim.py::simulate_adcs test:tests/test_cubesat_model.py::test_dataset_reproducible_first_20 | backed | keep |
| U23-C065 | R | so a relative change of 1e-12 in a design variable can move them by up to half a second, and by much more where the error trajectory grazes the settling band Note: the gap G-17 ledger records times moving by at most 0.49 s except design 763 (33.44 s to 12.53 s), which supports 'up to half a second' and 'much more where it grazes'; the sentence is a fixed string in stability() and no test asserts the 0.5 s figure against the results file (test_cubesat_model asserts atol=0.5 on regenerated data only) | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it file:docs/superpowers/notes/abstraction-gaps.md | broader than its backing | narrow |
| U23-C066 | R | (755 quantities, of which 330 numbers move at all) | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file | backed | keep |
| U23-C067 | S | A quantity that moves is printed in this paper to the digits that held in all 6 datasets | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it | backed | keep |
| U23-C068 | R | \| the contending sets (K = 1 and each facet at K = 3) \| 20 \| identical \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it | backed | keep |
| U23-C069 | R | \| each facet's leading metrics \| 8 \| identical \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it | backed | keep |
| U23-C070 | R | \| the signs of the reported tensions \| 24 \| identical \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it | backed | keep |
| U23-C071 | R | \| the selected temperatures, to the printed 0.1 \| 6 \| identical \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it | backed | keep |
| U23-C072 | R | \| the certificate statuses \| 6 \| identical \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it | backed | keep |
| U23-C073 | R | \| the pass or miss of each check design \| 6 \| identical \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it | backed | keep |
| U23-C074 | R | \| the count of nondominated designs on all attributes \| 2 \| identical \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it | backed | keep |
| U23-C075 | R | \| nondominated, four metrics, primary \| 146 \| 145 \| 146 \| 145 to 146 \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C076 | R | \| spearman, settling time, total mass, primary \| -0.3369 \| -0.3387 \| -0.3317 \| -0.339 to -0.332 \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C077 | R | \| pearson, settling time, slew time, primary \| 0.9064 \| 0.9006 \| 0.9065 \| 0.901 to 0.907 \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C078 | R | \| margin, K = 3, primary \| 0.0002201 \| 0.0002201 \| 0.001908 \| 0.00022 to 0.0019 \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C079 | R | \| facet 3 share, K = 3, primary \| 0.7778 \| 0.7609 \| 0.7955 \| 0.761 to 0.795 \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C080 | R | \| margin, K = 3, stock \| 0.001487 \| 0.001161 \| 0.001487 \| 0.00116 to 0.00149 \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | backed | keep |
| U23-C081 | R | \| facet 2 share, K = 3, stock \| 0.5897 \| 0.5385 \| 0.5897 \| 0.54 to 0.59 \| | gen:paper/generate_results.py::stability test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it | backed | keep |
| U23-C082 | S | The diagnostic `conditioning_` of the estimator is the smallest eigenvalue of the restricted Hessian at each facet's fit Note: eigenvalue value is asserted at K=1 only; at K>1 the test checks shape and positivity, not the value; also the Hessian is restricted to the participating exponents, which the sentence omits | test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue test:tests/test_estimator.py::test_conditioning_per_facet_and_nan_cases glossary:conditioning-of-the-exponents | broader than its backing | narrow |
| U23-C083 | M | a small value flags a nearly flat direction, so weakly identified exponents. Note: L4.3 gives the curvature along a direction (tau Var_p); small smallest eigenvalue = small curvature is immediate, but 'so weakly identified exponents' is an interpretation with no lemma (L4 states uniqueness is not proved; G-2 and G-12 list it as a bridging assumption) | lemma:L4.3 glossary:conditioning-of-the-exponents | broader than its backing | to the driver |
| U23-C084 | S | It is read only and takes no part in a status. Note: read only is pinned at K=1 (exponents equal the reference solve); 'takes no part in a status' holds by code order (termination_ is set before _conditioning) but no test asserts the status is independent of it | test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue func:src/hyperbolic_trade_space/estimator.py::_conditioning | broader than its backing | narrow |
| U23-C085 | R | \| 2 \| 2 \| 0.07 \| | gen:paper/generate_results.py::conditioning_diagnostic test:tests/test_paper.py::test_appendix_d_prints_the_conditioning_diagnostic test:tests/test_paper.py::test_facet_numbered_tables_are_current | backed | keep |
| U23-C086 | R | \| 3 \| 3 \| 0.095 \| | gen:paper/generate_results.py::conditioning_diagnostic test:tests/test_paper.py::test_appendix_d_prints_the_conditioning_diagnostic test:tests/test_paper.py::test_facet_numbered_tables_are_current | backed | keep |
| U23-C087 | R | \| 3 \| 2 \| 0.15 \| | gen:paper/generate_results.py::conditioning_diagnostic test:tests/test_paper.py::test_appendix_d_prints_the_conditioning_diagnostic test:tests/test_paper.py::test_facet_numbered_tables_are_current | backed | keep |
| U23-C088 | R | says that refitting a facet on its own rows is ill-posed | gen:paper/generate_results.py::own_rows_refit test:tests/test_paper.py::test_the_claims_of_c1_have_their_true_basis | backed | keep |
| U23-C089 | R | \| infinity \| 60 \| 0 of 60 \| 0.97 \| 60 of 60 \| 0.001 \| | gen:paper/generate_results.py::own_rows_refit test:tests/test_paper.py::test_the_claims_of_c1_have_their_true_basis | backed | keep |
| U23-C090 | R | \| 50 \| 60 \| 0 of 60 \| 0.96 \| 60 of 60 \| 0.037 \| | gen:paper/generate_results.py::own_rows_refit test:tests/test_paper.py::test_the_claims_of_c1_have_their_true_basis | backed | keep |
| U23-C091 | R | \| infinity \| 20 \| 16 of 20 \| 1, 3, 8, 16 \| | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 | backed | keep |
| U23-C092 | R | \| 50 \| 20 \| 16 of 20 \| 1, 3, 8, 16 \| | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 | backed | keep |
| U23-C093 | R | \| 1 \| 5 \| no \| no \| certified \| 0.32 \| 0.54 \| | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 | backed | keep |
| U23-C094 | R | \| 3 \| 6 \| no \| no \| certified \| 0.11 \| 0.94 \| | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 | backed | keep |
| U23-C095 | R | \| 8 \| 11 \| no \| no \| certified \| 0.20 \| 0.68 \| | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 | backed | keep |
| U23-C096 | R | \| 16 \| 5 \| no \| no \| certified \| 0.34 \| 0.64 \| | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 | backed | keep |
| U23-C097 | R | At the exact maximum the fit of each of these tables stops without a margin (`stationary_without_margin`) or at the iteration cap, depending on the platform Note: the sentence is hard-coded in the generator, not computed; test_r1_planted_certificates accepts either status for a zero-margin seed but pins only seeds 1, 3, 16 (and at most 6) as zero-margin, seed 8 is not pinned; 'depending on the platform' rests on the G-10 ledger and CI run ids, not on a test | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 test:tests/test_solvers.py::test_r1_planted_certificates file:paper/environment_values.toml | broader than its backing | narrow |
| U23-C098 | M | a frontier row on two facet planes ties at the exact maximum and the platform's argmax and linear-program vertex choice resolve the tie Note: no lemma step says a row on two facet planes ties (L13 assumes positive margin, R2); the tie and the platform's argmax/LP vertex resolution are empirical, in the G-10 ledger and CI runs, only partly tested | lemma:L13.3 file:docs/superpowers/notes/abstraction-gaps.md test:tests/test_solvers.py::test_r1_planted_certificates | broader than its backing | to the driver |
| U23-C099 | R | 16 of 20 tables were recovered, and the seeds above failed, at both temperatures on macOS arm64 and on Linux amd64. | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 file:paper/environment_values.toml | backed | keep |
| U23-C100 | R | Every table recovered has at least 18 frontier rows on each planted facet. | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 | backed | keep |
| U23-C101 | R | At temperature 50 the status and the errors, printed to two digits, were the same on both platforms. | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 file:paper/environment_values.toml | backed | keep |
| U23-C102 | M | a facet needs at least 5 frontier rows, one more than there are metrics, to be determined by them Note: only the generator's rule (d+1 frontier rows per planted facet) is tested; no lemma says fewer cannot determine a facet, and d points already fix a plane in d log-metrics given the sum-to-one normalization, so 'needs at least d+1' is a design rule, not a stated necessity | test:tests/test_datasets.py::test_k_terms_every_facet_has_d_plus_one_frontier_rows | broader than its backing | to the driver |
| U23-C103 | S | The temperature is selected afresh at each K | test:tests/test_k_terms_case.py::test_tau_reselected_at_each_k_holds_the_fraction func:examples/adcs/case.py::k_fits | backed | keep |
| U23-C104 | S | `mean_slack_` is defined for every K and is comparable across K at one temperature; `objective_` is the soft maximum at one term and the mean slack at several, and is not. | test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized test:tests/test_case.py::test_mean_slack_by_k_reads_the_estimator_and_the_fixed_tau_refit_shares_one_temperature | backed | keep |
| U23-C105 | R | \| 2 \| 113.2 \| 0.138 \| 0.090 \| | gen:paper/generate_results.py::mean_slack_fixed test:tests/test_paper.py::test_cr8_the_k_comparison_says_the_temperature_differs_and_d15_fixes_it | backed | keep |
| U23-C106 | R | \| 3 \| 195.2 \| 0.117 \| 0.052 to 0.053 \| | gen:paper/generate_results.py::mean_slack_fixed test:tests/test_paper.py::test_cr8_the_k_comparison_says_the_temperature_differs_and_d15_fixes_it | backed | keep |
| U23-C107 | R | \| 2 \| 78.7 \| 0.106 \| 0.068 \| | gen:paper/generate_results.py::mean_slack_fixed test:tests/test_paper.py::test_cr8_the_k_comparison_says_the_temperature_differs_and_d15_fixes_it | backed | keep |
| U23-C108 | R | \| 3 \| 162.8 \| 0.093 \| 0.033 \| | gen:paper/generate_results.py::mean_slack_fixed test:tests/test_paper.py::test_cr8_the_k_comparison_says_the_temperature_differs_and_d15_fixes_it | backed | keep |
| U23-C109 | S | The tension report runs a principal component analysis on the chart coordinates Z of a facet's near-frontier designs. | test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions test:tests/test_case.py::test_pca_directions_are_the_tension_reports_own_principal_directions | backed | keep |
| U23-C110 | M | Its directions say along which combinations of metrics the near-frontier designs vary the most | test:tests/test_tensions.py::test_first_direction_recovers_planted_spread definition | backed | keep |
| U23-C111 | M | the fit says which metrics bind, the analysis says where the sampled designs spread along the fitted surface. | test:tests/test_tensions.py::test_contending_set_recovers_planted_support test:tests/test_tensions.py::test_first_direction_recovers_planted_spread definition | backed | keep |
| U23-C112 | S | the second is computed from the first's coordinates | test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions | backed | keep |
| U23-C113 | S | The sign of a direction is arbitrary; each is shown with its largest loading positive. | test:tests/test_case.py::test_pca_directions_are_the_tension_reports_own_principal_directions func:examples/adcs/case.py::pca_directions | backed | keep |
| U23-C114 | R | \| 1 \| 0.46 \| pointing error +0.43, total mass -0.42, peak slew power -0.41 to -0.40 \| | gen:paper/generate_results.py::pca_chain test:tests/test_paper.py::test_cr11_chaining_with_pca_is_worked_on_the_case_in_d16 | backed | keep |
| U23-C115 | R | \| 2 \| 0.21 \| depth of discharge +0.51 to +0.52, total mass -0.46, slew time -0.39 \| | gen:paper/generate_results.py::pca_chain test:tests/test_paper.py::test_cr11_chaining_with_pca_is_worked_on_the_case_in_d16 | backed | keep |
| U23-C116 | R | \| 3 \| 0.184 \| pointing error +0.71, depth of discharge -0.38 to -0.37, slew time -0.32 to -0.31 \| | gen:paper/generate_results.py::pca_chain test:tests/test_paper.py::test_cr11_chaining_with_pca_is_worked_on_the_case_in_d16 | backed | keep |
| U23-S01 | R | \| 3 \| 0.007605 \| | gen:paper/generate_results.py::termination_records test:tests/test_paper.py::test_facet_numbered_tables_are_current | backed | keep |

### U24: supp Appendix E. Assumptions and abstraction gaps (`paper/supporting_material.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U24-C001 | M | L11: a $V$-maximizer is weakly efficient; the converse is not claimed. | lemma:L11.18 test:tests/test_derivation.py::test_L11_in_chain_and_states_non_converse | backed | keep |
| U24-C002 | R | at $\tau=38.10$ it is 0.096, 0.261, 0.382 for $K=1,2,3$ (primary) Note: k3-cubesat.md fixed-tau table matches; test pins only tau 38.10 and last-row fixed-tau fraction >0.25, not 0.096/0.261/0.382 (K=1 0.096 pinned in test_case RECORD) | gen:examples/adcs/k_terms.py::run_regime test:tests/test_k_terms_case.py::test_tau_reselected_at_each_k_holds_the_fraction | broader than its backing | narrow |
| U24-C003 | R | and 0.104, 0.204, 0.338 at $\tau=41.72$ (stock) Note: table matches k3-cubesat.md; test pins only tau 41.72 and fixed-tau K=3 fraction >0.25, not 0.204/0.338 | gen:examples/adcs/k_terms.py::run_regime test:tests/test_k_terms_case.py::test_tau_reselected_at_each_k_holds_the_fraction | broader than its backing | narrow |
| U24-C004 | R | re-selecting $\tau$ per $K$ returns it to 0.092 to 0.104 | gen:examples/adcs/case.py::k_table test:tests/test_case.py::test_k_sweep_equals_the_record | backed | keep |
| U24-C005 | R | The Pareto boundary of the cubesat attainable set is not observed. | definition | backed | keep |
| U24-C006 | M | Fraction above $V=1$ is a property of $(\tau,K)$ Note: no lemma step; the dependence on (tau,K) is shown only by the numbers of C002-C004 (R), not by an M step | none | unbacked | to the driver |
| U24-C007 | M | at finite $\tau$ with $\beta=J_\tau(Uw)$ (L3, L5); $V>1$ is possible. Note: L5.15 gives LME<=max so the top row has log V>=0 (L1.7 log V=w.u-beta); strict V>1 not tagged (needs non-constant scores); only the numbers (C002) show V>1 occurs | lemma:L5.15 lemma:L1.7 | broader than its backing | to the driver |
| U24-C008 | M | (b) The $\tau=\infty$ supporting envelope: $\max_i w\cdot u_i=\beta$, the LP optimum (I1); no observed row above it. | lemma:L5.24 lemma:L5.15 | backed | keep |
| U24-C009 | M | only the log-convex part of a Pareto front is reached by some $w$ (L11) Note: L11 proves maximizer => weakly efficient only; that only the log-convex part of a front is reached (supporting-hyperplane direction) is not a tagged step | lemma:L11.17 | broader than its backing | to the driver |
| U24-C010 | M | Existence: continuous $J_\tau$ on the compact simplex. | lemma:L3.15 | backed | keep |
| U24-C011 | M | positive definite on the participating coordinates (L3, L4, R1) Note: L4.3 gives second derivative tau Var_p (PSD, convex); positive definiteness is not proved (L4 docstring: strict convexity needs a rank condition) and G-2 lists it as unprovable | lemma:L4.3 test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue | broader than its backing | to the driver |
| U24-C012 | M | Stability: the smallest eigenvalue of that matrix. | definition test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue | backed | keep |
| U24-C013 | R | Cubesat `conditioning_` (M3): $K=1$ 1.12 (primary), 0.522 (stock) Note: committed output (staleness test) pins 2 digits only: 1.1 and 0.52; the 3-digit 1.12 and 0.522 are not printed or pinned | gen:paper/generate_results.py::conditioning_diagnostic test:tests/test_paper.py::test_appendix_d_prints_the_conditioning_diagnostic | broader than its backing | narrow |
| U24-C014 | R | Halving or doubling $\tau$ at $K=1$ moves the largest exponent by 0.008 and 0.022 (primary) Note: M5 recipe is prose in abstraction-gaps.md; no generator or test prints 0.008 and 0.022 | none | unbacked | drop |
| U24-C015 | R | 0.045 and 0.056 (stock), with six participants throughout (M5) Note: M5 numbers (0.045, 0.056, six participants) have no generator or test | none | unbacked | drop |
| U24-C016 | R | One primary $K=3$ facet has 7, 5, 3 exponents above Note: M3 count of exponents above 1e-3, 1e-2, 0.03 has no generator or test (test_k3_facets pins n_lemma 6,6,7 at the 1e-9 threshold, not these) | none | unbacked | drop |
| U24-C017 | S | (conditioning below $10^{-2}$ of the base at $10^{-3}$ log-noise collinearity) | test:tests/test_estimator.py::test_conditioning_drops_for_nearly_collinear_metrics | backed | keep |
| U24-C018 | R | (exponents below about 0.03 move with a few vertex rows) Note: a caveat in adcs-tensions-probe.md (noisy below about 0.03, sensitive to a few vertex designs); a judgment, no generator or test | none | unbacked | drop |
| U24-C019 | M | a small `conditioning_` marks a flat direction in which two fits with equal objective differ in $w$ Note: L4.3 gives curvature tau Var_p along a direction; small eigenvalue means nearly flat, not that two fits with equal objective exist (equal vs nearly equal, local second order) | lemma:L4.3 test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue | broader than its backing | to the driver |
| U24-C020 | M | an identity for the population expectation. | lemma:L6.8 test:tests/test_derivation.py::test_L6_statement_is_the_restricted_population_identity | backed | keep |
| U24-C021 | R | the ratio of the fitted offset shift to $\tau\sigma^2\lVert w\rVert^2/2=0.038$ is 1.072 (N=400, sd of the shift 0.0061) Note: M1 ratio 1.072 (N=400, sd 0.0061) from prose recipe only; test pins N=40000 one seed | none | unbacked | drop |
| U24-C022 | R | 1.023 (N=4000, sd of the shift 0.0014), 0.992 (N=40000, sd of the shift 0.0012), five seeds each Note: test pins N=40000, one seed, ratio within 5e-2; N=4000 (1.023), the sds and the five-seed means are not generated or tested | test:tests/test_estimator.py::test_gaussian_noise_offset | broader than its backing | narrow |
| U24-C023 | S | five seeds each. `tests/test_estimator.py::test_gaussian_noise_offset` (N=40000, tolerance 5e-2) | test:tests/test_estimator.py::test_gaussian_noise_offset | backed | keep |
| U24-C024 | M | an elasticity $-w_k/w_j$ is a description of the fitted surface | lemma:L7.5 | backed | keep |
| U24-C025 | M | for one row it is $\min_w w\cdot u_1$, attained at the vertex on the row's smallest log-metric Note: for n=1 mean=LME=max gives J=w.u_1 (L5.14, L5.15); the vertex at the smallest log-metric is an elementary LP fact with no tagged step | lemma:L5.14 lemma:L5.15 | broader than its backing | to the driver |
| U24-C026 | R | For the row $(1,2,3)$ the convention's objective $w\cdot u_1$ is 0.597 against the infimum 0 at the vertex Note: arithmetic checked: log(6)/3=0.5973, infimum 0; test pins w=1/3 and beta=w.u (score 0) but no test or generator prints 0.597 or the infimum | test:tests/test_estimator.py::test_single_sample_gives_balanced_exponents | broader than its backing | narrow |
| U24-C027 | S | at the vertex on the smallest log-metric. `tests/test_estimator.py::test_degenerate_single_valid_row_warns_with_the_convention` ($K=1$ and $K=3$) | test:tests/test_estimator.py::test_degenerate_single_valid_row_warns_with_the_convention | backed | keep |
| U24-C028 | S | A fit on one valid row is not a result; the warning is the report. | test:tests/test_estimator.py::test_degenerate_single_valid_row_warns_with_the_convention | backed | keep |
| U24-C029 | M | $m^0=1$ for every $m\ge0$, and $0^{w}=0$ for $w>0$. | definition | backed | keep |
| U24-C030 | M | A zero metric contributes nothing at a zero exponent and sends $V$ to 0 at a positive one. | definition test:tests/test_estimator.py::test_zero_metric_with_zero_exponent_equals_the_formal_limit | backed | keep |
| U24-C031 | M | $w_j=10^{-13}$ gives a finite score and $w_j=10^{-11}$ gives $-\infty$ on the same row Note: the 1e-12 cut is in code (EPS_ZERO_EXPONENT, _zero_limit_scores) but no test sets w_j=1e-13 and 1e-11 on one row; test uses exponent exactly 0 | none | unbacked | to the driver |
| U24-C032 | R | zeroing metric 4 (exponent 0) in 10% and 30% of $N=400$ rows moves the fitted exponents by at most 0.0008 and 0.0013 Note: M4 numbers 0.0008 and 0.0013 from prose recipe (noise 0.05, alpha 0.01, N=400); no generator or test (test_zero_metric_row adds one row at 1e-9) | none | unbacked | drop |
| U24-C033 | S | `tests/test_estimator.py::test_zero_metric_with_zero_exponent_equals_the_formal_limit` (agreement to $10^{-12}$ with $m^0=1$) | test:tests/test_estimator.py::test_zero_metric_with_zero_exponent_equals_the_formal_limit | backed | keep |
| U24-C034 | S | An exponent at or below $10^{-12}$ is zero; a row with a zero metric carries no information about the other exponents. | test:tests/test_estimator.py::test_constants_are_reexported test:tests/test_estimator.py::test_zero_metric_row | backed | keep |
| U24-C035 | S | A row scored $-\infty$ has a zero metric the fitted surface depends on | test:tests/test_estimator.py::test_zero_metric_with_zero_exponent_equals_the_formal_limit | backed | keep |
| U24-C036 | M | The plain fit on a facet's own rows has its support function minimized at a vertex of the simplex Note: no lemma; ledger itself says observed, not proved; and its own example (own-rows LP returns 0.416,0,0.119,0.465) is not a vertex | none | unbacked | to the driver |
| U24-C037 | M | (edge-interior optimizers exist for other geometries) Note: existence of edge-interior optimizers is asserted without example or lemma (the seed-0 own-rows LP is a face-interior point, but is not cited for this) | none | unbacked | to the driver |
| U24-C038 | R | own-rows refit 0/60 within 0.05 of the planted exponents at $\tau=\infty$ and at $\tau=50$ | gen:paper/generate_results.py::own_rows_refit test:tests/test_paper.py::test_the_claims_of_c1_have_their_true_basis | backed | keep |
| U24-C039 | R | (median error 0.857 for facets with at most 4 frontier rows, 0.649 above 30) Note: medians 0.857 and 0.649 only in spike oracle.txt (bench_oracle.py, older data with facets of <=4 frontier rows, which the generator no longer makes); own_rows_refit prints largest errors only; no test | none | unbacked | drop |
| U24-C040 | R | step B 60/60 (median error at most 0.018 at $\tau=\infty$, at most 0.037 at $\tau=50$) Note: 60/60 pinned; medians 0.018 and 0.037 are spike figures (oracle.txt), generator prints largest error 0.001 (inf) and 0.037 (50), no medians, no test | gen:paper/generate_results.py::own_rows_refit test:tests/test_paper.py::test_the_claims_of_c1_have_their_true_basis | broader than its backing | narrow |
| U24-C041 | R | the own-rows LP on seed 0 returns $(0.416,0,0.119,0.465)$ for the planted $(0.212,0.334,0.245,0.209)$ Note: own-rows LP vector only in spike-facet-refit README/oracle.txt (bench_oracle.py); no test pins it | none | unbacked | drop |
| U24-C042 | M | A facet with fewer affinely independent frontier rows than $d$ does not determine its hyperplane Note: linear-algebra fact (d-m free parameters); no lemma step states it; spike check_identifiability.py only counts | none | unbacked | to the driver |
| U24-C043 | S | spike data from before the generator guaranteed $d+1$ rows | test:tests/test_datasets.py::test_k_terms_every_facet_has_d_plus_one_frontier_rows file:work-packages/WP9-review.md | backed | keep |
| U24-C044 | R | seed 1 has 3 rows, 1 free parameter; seed 16 has 2 rows, 2 free; seed 3 has 6 rows, 0 free Note: rows and free parameters only in spike-objective README section 2 (check_identifiability.py); no test pins them | none | unbacked | drop |
| U24-C045 | R | With true labels step B recovers all 60 facets, including those with 2 to 4 frontier rows Note: 60/60 with true labels only in spike-facet-refit README/oracle.txt; no test uses true labels | none | unbacked | drop |
| U24-C046 | R | Alternation recovery is 17/20 and 16/20 at $\tau=\infty$, 50 Note: 17/20 and 16/20 only in WP9-review/WP13-decisions and spike; no test pins the 20-seed rates | none | unbacked | drop |
| U24-C047 | R | failing seeds 1, 3, 16 and 8; fewest frontier rows 5, 6, 5, 11 Note: failing seeds and their frontier-row minima only in WP9-review/spike; tests assert only >=5 rows for 4 seeds | none | unbacked | drop |
| U24-C048 | R | Cubesat: smallest near-frontier count of a $K=3$ facet is 17 Note: test pins primary K=3 near-frontier counts [17,33,126]; stock not asserted; claim says cubesat generally | gen:examples/adcs/case.py::facet_table test:tests/test_case.py::test_k3_facets_equal_the_primary_record | broader than its backing | narrow |
| U24-C049 | M | Proposition 3 (L14) is for step B, unpenalized, with support offsets $\beta_k=J_\tau(Uw_k)$ | lemma:L14 lemma:L14.17 lemma:L14.18 | backed | keep |
| U24-C050 | M | level 1 (descent) is for B only (I7); I8 requires a convex facet objective. | lemma:L15 lemma:L12.5 lemma:L12.6 | backed | keep |
| U24-C051 | M | (I8 fails for a nonconvex objective) | lemma:L12.5 file:derivation/axioms.py | backed | keep |
| U24-C052 | R | Half-steps in which the objective rises: refit step B 0.000 at $\tau=\infty$ and 50; step D 0.501 and 0.349 Note: B zero rise pinned; D's 0.501 and 0.349 only in spike-objective README table 1a (no test; tangent test says only not monotone) | test:tests/test_solvers.py::test_terms_monotone_history_and_stops | broader than its backing | narrow |
| U24-C053 | R | Recovery, 20 seeds: support 17/20 ($\tau=\infty$), 16/20 (50); tangent 16/20, 17/20 Note: 17/20, 16/20 (support) and 16/20, 17/20 (tangent) not pinned by any test; WP9-review/spike only | none | unbacked | drop |
| U24-C054 | R | tangent seed 8 at $\tau=\infty$ has error 0.054 against the 0.05 criterion Note: seed 8 tangent error 0.054 only in WP9-review; test_tangent_recovers_planted_facets covers seeds 0,2,0,4 only | none | unbacked | drop |
| U24-C055 | S | the certificate columns are read as diagnostics and no local-optimality statement is made | test:tests/test_estimator.py::test_termination_not_applicable_cases_do_not_warn | backed | keep |
| U24-C056 | S | Under D or the penalty the fit is an option with first-order diagnostics | test:tests/test_estimator.py::test_termination_not_applicable_cases_do_not_warn func:src/hyperbolic_trade_space/solvers.py::_termination | backed | keep |
| U24-C057 | M | L5: $J_\tau$ is within $(\log n)/\tau$ of the maximum | lemma:L5.15 lemma:L5.16 | backed | keep |
| U24-C058 | M | L10: $\Phi_K$ lies in $[\max_k x_k,\max_k x_k+(\log K)/\kappa]$ | lemma:L10.15 lemma:L10.16 | backed | keep |
| U24-C059 | S | The band $\lvert\log V\rvert<1/\tau$ is the code's convention for near-frontier, not a lemma. | func:src/hyperbolic_trade_space/estimator.py::fit test:tests/test_case.py::test_regime_comparison_on_frozen_data | backed | keep |
| U24-C060 | R | $\tau$ by $K=1,2,3$: 38.10, 113.22, 195.18 (primary); 41.72, 78.75, 162.78 (stock) | gen:examples/adcs/case.py::k_table test:tests/test_case.py::test_k_sweep_equals_the_record | backed | keep |
| U24-C061 | R | band 0.0262, 0.0088, 0.0051 (primary); fraction above 0.096, 0.096, 0.098 | gen:examples/adcs/case.py::k_table test:tests/test_case.py::test_k_sweep_equals_the_record test:tests/test_case.py::test_regime_comparison_on_frozen_data | backed | keep |
| U24-C062 | R | At $K=3$ some facets hold 3 to 6 designs in their own band. Note: 3 to 6 designs in own band only in k3-cubesat.md; no test or generator cell pins it | none | unbacked | drop |
| U24-C063 | R | Mean slack at fixed $\tau$ is about a quarter of $K=1$'s, at re-selected $\tau$ 0.117 against 0.204 (primary) and 0.093 against 0.131 (stock) Note: re-selected objectives 0.117/0.204, 0.093/0.131 pinned; 'about a quarter at fixed tau' (0.0529, 0.0326) not pinned by any test | gen:examples/adcs/case.py::k_table test:tests/test_case.py::test_k_sweep_equals_the_record | broader than its backing | narrow |
| U24-C064 | R | Objective stable to $2\times10^{-6}$ over seeds 0 to 4 (primary) Note: 2e-6 over seeds 0 to 4 only in k3-cubesat.md; tests run seed 0 only; stability_extra.json is a different measure | none | unbacked | drop |
| U24-C065 | R | it was bracketed at every $K$ observed | gen:examples/adcs/k_terms.py::run_regime test:tests/test_k_terms_case.py::test_tau_reselected_at_each_k_holds_the_fraction | backed | keep |
| U24-C066 | M | the margin $\gamma=\min_i[s_{i,k(i)}-\max_{k\ne k(i)}s_{ik}]$ is zero when a row lies on two facet planes | lemma:L13 glossary:assignment-margin test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets | backed | keep |
| U24-C067 | M | at $\tau=\infty$ a frontier row on a ridge has slack 0 for both facets | lemma:L5.24 glossary:assignment-margin | backed | keep |
| U24-C068 | M | two identical facets tie on every row | test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets | backed | keep |
| U24-C069 | M | Ties are measure-zero for continuous data at finite $\tau$ | definition | backed | keep |
| U24-C070 | R | $\gamma$ at or below $10^{-9}$ on seeds 1, 3, 8, 16 and above it on the other 16 Note: tests pin 16 seeds above EPS_FEAS=1e-9 and {1,3,16} among the zero-margin; seed 8 as the fourth is not asserted | gen:tests/test_solvers.py::_planted_fit test:tests/test_solvers.py::test_r1_planted_certificates test:tests/test_solvers.py::test_margin_lemma_perturbations_inside_the_radius_keep_labels | broader than its backing | narrow |
| U24-C071 | R | at $\tau=50$ $\gamma\in(10^{-4},10^{-2})$ on all 20 | gen:tests/test_solvers.py::_planted_fit test:tests/test_solvers.py::test_r1_planted_certificates | backed | keep |
| U24-C072 | R | $\gamma\le0$ in 8 at $\tau=\infty$, 0 at $\tau=50$ Note: spike 100-restart counts (8 and 0) only in spike-certificates README tables 1 and 2; no test | none | unbacked | drop |
| U24-C073 | R | the 9 guard events at $\tau=\infty$ were round-off, 8 of them two identical facets Note: 9 guard events, 8 duplicate facets only in spike-certificates README/dup_facets.py; no test pins the counts | none | unbacked | drop |
| U24-C074 | R | $\gamma=9\times10^{-16}$ on 3 of 5 seeds (one tied row) Note: gamma 9e-16 on 3 of 5 stock seeds only in spike-certificates README table 3; no test | none | unbacked | drop |
| U24-C075 | S | Platform: facet numbering and an emptied facet differ by platform Note: platform dependence recorded in reviews; tests only compare after matching, none asserts the difference | file:work-packages/WP9-review.md file:work-packages/WP13-decisions.md | broader than its backing | narrow |
| U24-C076 | S | The Linux CI run 42540318424 resolved one tied row differently from macOS Note: WP13-decisions records Linux-only tied-row failures but not run id 42540318424; id unverifiable in repo | file:work-packages/WP13-decisions.md | broader than its backing | narrow |
| U24-C077 | S | `assignment_changes` counts a row only when its label trails the maximum score by more than `EPS_FEAS` | func:src/hyperbolic_trade_space/solvers.py::_termination test:tests/test_solvers.py::test_guard_stop_returns_the_consistent_previous_state | backed | keep |
| U24-C078 | R | run 42541322671 on Linux stopped a tied seed at the iteration cap where macOS reports stationary without margin Note: WP13-decisions records a tied tau=inf seed stopping at the cap on Linux, not run id 42541322671; id unverifiable in repo | file:work-packages/WP13-decisions.md | broader than its backing | narrow |
| U24-C079 | S | accepts both for a zero margin) | test:tests/test_solvers.py::test_r1_planted_certificates | backed | keep |
| U24-C080 | M | A fit with $\gamma=0$ is first-order stationary per facet (levels 1 and 2) with no local-optimality claim | lemma:L12 lemma:L15 lemma:L14 glossary:assignment-margin test:tests/test_solvers.py::test_r1_planted_certificates | backed | keep |
| U24-C081 | M | I2 gives replication invariance of $J_\tau$ (sample means converge to the expectation) | file:derivation/axioms.py test:tests/test_derivation.py::test_replication_invariance | backed | keep |
| U24-C082 | M | L6 gives the population cumulant identity (G-3) | lemma:L6 test:tests/test_derivation.py::test_L6_statement_is_the_restricted_population_identity | backed | keep |
| U24-C083 | R | the largest exponent error (median over seeds) is 0.013, 0.018, 0.011 at $N=200$, 2000, 20000 for $\tau=\infty$ (no decay) and 0.008, 0.007, 0.003 for $\tau=50$ Note: M2 numbers (0.013, 0.018, 0.011; 0.008, 0.007, 0.003) exist only as the ledger's recipe M2; no generator script or test pins them (test_recovery_tau_inf is noise-free) | none | unbacked | drop |
| U24-C084 | R | Objective stable over seeds in the cubesat record (primary 0.11733 for seeds 0 to 4) Note: test pins objective_ 0.1173 (abs 6e-5) for the default seed only; stability over seeds 0 to 4 and the 5th digit rest on k3-cubesat.md and the spike table, not a test (test_k_terms_case runs seeds=[0]) | gen:examples/adcs/k_terms.py::run_regime test:tests/test_case.py::test_k_sweep_equals_the_record | broader than its backing | narrow |
| U24-C085 | S | Noise-free baseline: `tests/test_estimator.py::test_recovery_tau_inf` (error below $10^{-6}$) | test:tests/test_estimator.py::test_recovery_tau_inf | backed | keep |
| U24-C086 | R | No sentence of the prose claims consistency | definition | backed | keep |
| U24-C087 | M | The contending set is the support of $w$; identified only where the restricted Hessian is positive definite Note: support definition is the glossary's; but 'identified only where the restricted Hessian is positive definite' (necessity, and uniqueness) is not proved: L4 shows convexity only and states it does NOT prove strict convexity or uniqueness | glossary:contending-set lemma:L4 | broader than its backing | to the driver |
| U24-C088 | P | Observations are designs chosen by a simulator or an analyst, not draws of the attainable set. | definition | backed | keep |
| U24-C089 | R | The $K=1$ contending set differs between the two cubesat sampling regimes | gen:examples/adcs/case.py::tension_table test:tests/test_case.py::test_k1_contending_set_equals_the_record | backed | keep |
| U24-C090 | R | (primary: total mass, slew time, energy balance, control effort, pointing error, depth of discharge; stock: control effort, slew time, power margin, settling time, pointing error, eclipse reserve) | gen:examples/adcs/case.py::tension_table test:tests/test_case.py::test_k1_contending_set_equals_the_record | backed | keep |
| U24-C091 | R | Mass has $\tau=\infty$ exponent 0.006 and working 0.094 over all designs in the probe Note: comes from the 2026-11-08 probe note on a 4-metric 960-design set (tau 21.7); the note says its script was a scratch file, nothing committed; no generator or test | none | unbacked | drop |
| U24-C092 | R | A stock $K=3$ facet has exponents of 0.0013 and 0.0188 near the threshold (M3). Note: M3 recipe only; the values 0.0013 and 0.0188 appear in no committed record, test or script output (k3-cubesat.md lists largest exponents only) | none | unbacked | drop |
| U24-C093 | P | Recovery of planted facets is measurable only where the boundary is planted. | definition | backed | keep |
| U24-C094 | M | G-1 relates the fitted objects to maximizers (L11) and to nothing else. | lemma:L11 | backed | keep |
| U24-C095 | R | 20 seeds, $N=400$, $d=4$, $K=3$: support step 17/20 ($\tau=\infty$), 16/20 (50); failures are facets with 5 to 11 frontier rows Note: 17/20 and 16/20 on 20 seeds at N=400 are recorded in work-packages/WP9-review.md (reviewer's run); no test pins them (the tests use four favourable seeds), failures at 5 to 11 frontier rows likewise only in review | none | unbacked | drop |
| U24-C096 | R | Mean slack, $K=1$ to $3$ at re-selected $\tau$: 0.204 to 0.117 (primary), 0.131 to 0.093 (stock) | gen:examples/adcs/case.py::k_table test:tests/test_case.py::test_k_sweep_equals_the_record | backed | keep |
| U24-C097 | M | (one hyperplane is not tangent where the boundary curves) Note: geometric remark with no lemma step (L10/L11 do not state it); source is docs/user-guide/limitations.md prose | none | unbacked | to the driver |
| U24-C098 | M | No theorem for the multi-facet alternation beyond I7 (the partition-and-refit pattern of Magnani and Boyd) and the three levels (L12 to L14), all local. Note: 'all local' and no global theorem are backed (L14 'does NOT prove global'; I7 is local); but 'the three levels (L12 to L14)' omits L15 (descent is proved) and L16/L17 are also theorems about the alternation | lemma:L14 lemma:L15 lemma:L16 file:derivation/axioms.py | broader than its backing | to the driver |
| U24-C099 | L | (the partition-and-refit pattern of Magnani and Boyd) | bib:magnani2009convex file:paper/reading_pass.yaml | backed | keep |
| U24-C100 | R | Stock cubesat $K=3$, $\tau=162.78$: `objective_` 0.09287 on four seeds and 0.11427 on one Note: 0.09287 on four seeds and 0.11427 on one match spike-certificates README table 3 and k3-cubesat.md; the test pins only the seed-0 value 0.0929 (abs 6e-5), not the four/one split or 0.11427 | gen:docs/superpowers/notes/spike-certificates/run_cubesat.py test:tests/test_case.py::test_k_sweep_equals_the_record | broader than its backing | narrow |
| U24-C101 | R | at $\tau=\infty$ 0.1224 (2 seeds) and 0.1447 (3 seeds) Note: 0.1224 (2 seeds) and 0.1447 (3 seeds) match spike-certificates README table 3 (stock, tau=inf) but are pinned by no test | none | unbacked | drop |
| U24-C102 | R | Planted seeds 1, 3, 8, 16 with 5, 20, 50 restarts: no failing seed recovered; seed 8 passes at 5 and fails at 20 and 50 Note: recorded in WP9-review.md third review from a scratch script outside the repo (/private/tmp/.../rec2.py); sentence lacks the scope (default step, tau=inf for seed 8); no test | none | unbacked | drop |
| U24-C103 | M | Every $K>1$ result is a local optimum of its run, reported with `random_state` Note: L14 gives a local minimizer only for step B, unpenalized, positive margin R2, exact facet optima; statuses stationary_without_margin, uncertified, guard_stop, iteration_cap, the tangent step and the penalty carry no local-optimality claim (ledger G-8, G-10), so 'every K>1 result' is broader | lemma:L14 | broader than its backing | to the driver |
| U24-C104 | M | Corollary 4 bounds $F(W)-F^*_{\text{fixed}}$, where $F^*_{\text{fixed}}$ is the optimum for the fixed assignment of the returned run (L14). | lemma:L14 lemma:L12 test:tests/test_solvers.py::test_corollary_bound_on_every_planted_fit | backed | keep |
| U24-C105 | R | assignment fixed in 89 ($\tau=\infty$) and 100 ($\tau=50$), guard in 9 and 0, 50-iteration cap in 2 and 0 Note: numbers match spike-certificates README table 2 (100 restarts per tau, run_planted.py output committed) but no test pins them; the spike predates the guard tolerance | none | unbacked | drop |
| U24-C106 | R | every chosen run of the 20 planted seeds stopped on a fixed assignment | gen:tests/test_solvers.py::_planted_fit test:tests/test_solvers.py::test_r1_planted_certificates | backed | keep |
| U24-C107 | R | Passing restarts exist among five on seeds 3 and 8 Note: spike README: passing restarts among five on seeds 3 and 8 at tau=inf; at tau=50 the default step has 0 on both (step D has 3 and 5), and WP9-review G3-1 says the counts hold only at tau=inf; sentence carries no scope; no test | file:docs/superpowers/notes/spike-objective/README.md | broader than its backing | narrow |
| U24-C108 | R | and the mean-slack selector does not choose them. Note: reviewer's third review says the mean-slack selector does not pick them (seed 8 at tau inf, default step, lost at 20 and 50 restarts); scope of tau and step not stated in the sentence and no test | file:work-packages/WP9-review.md | broader than its backing | narrow |
| U24-C109 | M | Level 3 conditions on R2 (positive margin), nonempty facets, exact facet optima ($G_k=0$) and offsets $\beta_k=J_\tau(Uw_k)$ | lemma:L14 | backed | keep |
| U24-C110 | M | with I8 (first-order convexity) and I9 (Cauchy-Schwarz) for the radius | lemma:L13.11 lemma:L13.2 lemma:L12 | backed | keep |
| U24-C111 | M | it is sufficient, attained only for changes parallel to the design vector Note: sufficiency is L13.11 (L13 says tightness is not proved); 'attained only for changes parallel to the design vector' is the Cauchy-Schwarz equality case, found only in the I9 failure_mode text, not a tagged step | lemma:L13.11 file:derivation/axioms.py | broader than its backing | to the driver |
| U24-C112 | R | Planted fits: maximum facet gap $\le10^{-12}$ after the polish (SLSQP alone left $4.7\times10^{-5}$ at $\tau=50$, none of 60 facets certified at $10^{-8}$) Note: max gap <= 1e-12 is asserted on 20 seeds; 'SLSQP alone left 4.7e-5, none of 60 facets certified at 1e-8' is spike-certificates table 4 only (the polish test checks seed 0 above 1e-8, not 4.7e-5 or all 60) | test:tests/test_solvers.py::test_r1_planted_certificates test:tests/test_solvers.py::test_polish_never_increases_the_facet_objective_and_closes_the_gap | broader than its backing | narrow |
| U24-C113 | R | $\gamma\in(10^{-4},10^{-2})$ and radius in $(10^{-6},10^{-3})$ at $\tau=50$ | gen:tests/test_solvers.py::_planted_fit test:tests/test_solvers.py::test_r1_planted_certificates | backed | keep |
| U24-C114 | R | Cubesat $K=3$ certified: gap $2.6\times10^{-14}$, $\gamma=2.2\times10^{-4}$, radius $1.8\times10^{-5}$ (primary) Note: gamma 2.2e-4 and radius 1.8e-5 pinned (abs 5e-7); the gap 2.6e-14 is pinned only as < 1e-12 and appears in no record (k3-cubesat.md gives 1.1e-14 for primary K=3 seed 0): number unverified, likely wrong | gen:examples/adcs/case.py::k_table test:tests/test_case.py::test_k_sweep_equals_the_record | broader than its backing | narrow |
| U24-C115 | R | gap $1.1\times10^{-14}$, $\gamma=1.5\times10^{-3}$, radius $1.2\times10^{-4}$ (stock) Note: gamma 1.5e-3 (0.001487) and radius 1.2e-4 (0.000119) pinned; gap 1.1e-14 pinned only as < 1e-12 and k3-cubesat.md gives 9.1e-15 for stock seed 0 (1.1e-14 is seed 2): number does not match the record | gen:examples/adcs/case.py::k_table test:tests/test_case.py::test_k_sweep_equals_the_record | broader than its backing | narrow |
| U24-C116 | S | The status states which of the three levels the fit meets: descent always, stationarity per facet when the gap is small, local optimality of the fixed assignment only when `certified`. Note: statuses and certified conditions are tested; 'descent always' holds for step B unpenalized (monotone history tested) but not for the tangent step or the penalty (status not_applicable; ledger G-8 half-steps rise), and guard_stop/iteration_cap are not mentioned | test:tests/test_solvers.py::test_r1_planted_certificates test:tests/test_solvers.py::test_terms_monotone_history_and_stops test:tests/test_estimator.py::test_termination_record_for_k_terms file:docs/user-guide/termination.md | broader than its backing | narrow |
| U24-C117 | M | The stable radius is small in parameter units, so level 3 is a local statement. | lemma:L14 lemma:L13.11 test:tests/test_solvers.py::test_r1_planted_certificates | backed | keep |
| U24-C118 | R | a relative change of $10^{-12}$ in a design variable moves the time by a small fraction of a step Note: an assumption the same row's evidence contradicts for design 763 (slew time 33.44 s to 12.53 s); no measurement of the deviation as a fraction of the step is recorded or tested | gen:examples/adcs/experiments/sensitivity.py::column_deviation test:tests/test_sensitivity.py::test_the_results_file_committed_values_equal_the_committed_case_results | broader than its backing | narrow |
| U24-C119 | R | The times moved by at most 0.49 s except one design Note: 0.49 s appears in work-packages/swap-evidence.md (five regenerations); sensitivity.json and test_sensitivity pin no time-column maximum (tests use synthetic tables) | none | unbacked | drop |
| U24-C120 | R | 763, whose slew time went from 33.44 s to 12.53 s Note: design 763, 33.44 s to 12.53 s, appears only in work-packages/swap-evidence.md; no committed result file or test pins it | none | unbacked | drop |
| U24-C121 | R | Identical in all five and to the committed data: the contending sets, each facet's leading metrics, the signs of the tensions | gen:paper/generate_results.py::stability gen:examples/adcs/experiments/sensitivity.py::summarise test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file | backed | keep |
| U24-C122 | R | the selected temperatures at the printed 0.1, the certificate statuses, the pass or miss of every check design | gen:paper/generate_results.py::stability gen:examples/adcs/experiments/sensitivity.py::summarise test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file | backed | keep |
| U24-C123 | R | all flags and feasibility verdicts, and the count 671 of 706 Note: count 671 of 706 is in sensitivity.json (identical, 671/706) and test_case.py:241 asserts 671 on committed data; but flags and feasibility verdicts (0 changed) appear only in swap-evidence.md and the report, with no test pinning them. | gen:examples/adcs/experiments/sensitivity.py::summarise test:tests/test_case.py::test_nondominated_counts_on_frozen_primary file:work-packages/swap-evidence.md | broader than its backing | narrow |
| U24-C124 | R | the nondominated counts on reduced views (146 to 145, 8 to 7, stock 157 to 158) Note: values match sensitivity.json (146 to 145, 8 to 7, stock 157 to 158); the test pins the primary ranges only, nothing pins stock 157 to 158. | gen:examples/adcs/experiments/sensitivity.py::summarise test:tests/test_paper.py::test_generated_sentences_quote_the_ranges_from_the_results_file file:examples/adcs/experiments/reports/sensitivity.json | broader than its backing | narrow |
| U24-C125 | R | the regime comparison (effective sample size 16.2 printed 16.0 or 16.1, near-frontier count 51 to 52, stock fraction above 0.104 to 0.105, five association values by 0.01) Note: values match (n_eff 16.2 vs 16.0/16.1 per swap-evidence per-seed table, near-frontier 51 to 52, stock frac 0.1038 to 0.1051, five primary association pairs move, spread at most 0.007 so 'by 0.01' is the printed step); no test pins these min/max values, only committed-inside-range. | gen:examples/adcs/experiments/sensitivity.py::summarise file:examples/adcs/experiments/reports/sensitivity.json file:work-packages/swap-evidence.md test:tests/test_paper.py::test_results_file_records_the_five_seeds_and_the_perturbation | broader than its backing | narrow |
| U24-C126 | R | the paper prints those quantities as ranges over the five regenerations Note: a test pins ranges for nondominated counts, K=3 facet shares and n_eff in the temperature sentence; not every listed quantity (near-frontier, stock fraction, associations) has a test that the paper prints its range. | gen:paper/paper_stability.py::stable test:tests/test_paper.py::test_generated_sentences_quote_the_ranges_from_the_results_file | broader than its backing | narrow |
| U24-C127 | R | The qualitative conclusions (which metrics contend, which trade against which, the certificate status, the outcomes of the checks) are stable. | gen:paper/generate_results.py::stability gen:examples/adcs/experiments/sensitivity.py::summarise test:tests/test_paper.py::test_appendix_d_has_the_stability_subsection_and_section_9_points_to_it test:tests/test_paper.py::test_stability_table_is_derived_from_the_results_file | backed | keep |

### U25: supp Appendix F. Computational reproducibility (`paper/supporting_material.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U25-C001 | S | - **The repository keeps:** the code, the tests, the lock file, the Dockerfile and the ledger. Note: The repository keeps: list of artifacts; code, tests, lock file, Dockerfile exist but the 'ledger' (axiom or experiment ledger) is not pinned by any test; intent statement of appendix content | none | unbacked | drop |
| U25-C002 | S | \| Python \| 3.12 \| .python-version; requires-python >=3.12,<3.13 \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version gen:paper/generate_repro.py::toolchain | backed | keep |
| U25-C003 | S | \| Package manager \| uv 0.9.18 \| uv.lock (format revision 3) \| Note: test pins only the prefix '\| Package manager \| uv '; 'uv 0.9.18' is the local uv --version at run time (matches Dockerfile ARG UV_VERSION); revision 3 matches uv.lock | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version gen:paper/generate_repro.py::toolchain | broader than its backing | narrow |
| U25-C004 | S | \| Locked packages \| 176 \| uv.lock \| Note: stale: uv.lock now has 178 packages (9ec8c4a added pytest-xdist); committed output says 176; test checks the generator, not the committed count | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version gen:paper/generate_repro.py::toolchain | broader than its backing | narrow |
| U25-C005 | S | \| numpy \| 2.5.4 \| uv.lock; runtime dependency \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version test:tests/test_paper.py::test_f_toolchain_committed_output_matches_the_lock | backed | keep |
| U25-C006 | S | \| scipy \| 1.18.1 \| uv.lock; runtime dependency \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version test:tests/test_paper.py::test_f_toolchain_committed_output_matches_the_lock | backed | keep |
| U25-C007 | S | \| sympy \| 1.14.0 \| uv.lock; runtime dependency \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version test:tests/test_paper.py::test_f_toolchain_committed_output_matches_the_lock | backed | keep |
| U25-C008 | S | \| scikit-learn \| 1.9.1 \| uv.lock; runtime dependency \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version test:tests/test_paper.py::test_f_toolchain_committed_output_matches_the_lock | backed | keep |
| U25-C009 | S | \| pandas \| 3.1.1 \| uv.lock; runtime dependency \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version test:tests/test_paper.py::test_f_toolchain_committed_output_matches_the_lock | backed | keep |
| U25-C010 | S | \| matplotlib \| 3.11.2 \| uv.lock; runtime dependency \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version test:tests/test_paper.py::test_f_toolchain_committed_output_matches_the_lock | backed | keep |
| U25-C011 | S | \| hyperbolic-trade-space \| 0.0.1 \| pyproject.toml; this repository \| Note: 0.0.1 matches pyproject.toml but no test asserts the project row | gen:paper/generate_repro.py::toolchain | broader than its backing | narrow |
| U25-C012 | S | \| mystmd \| 1.12.0 \| uv.lock; dependency group paper \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version test:tests/test_paper.py::test_f_toolchain_committed_output_matches_the_lock | backed | keep |
| U25-C013 | S | \| ipykernel \| 7.4.0 \| uv.lock; dependency group paper \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version | backed | keep |
| U25-C014 | S | \| nbclient \| 0.11.0 \| uv.lock; dependency group paper \| | test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version | backed | keep |
| U25-C015 | S | \| Node.js \| v23.7.0 \| not pinned by uv.lock; MyST requires 22 or newer \| Note: Node version is observed from node --version; no test; 'MyST requires 22 or newer' appears in Dockerfile comment and a test skip reason only | none | unbacked | drop |
| U25-C016 | R | \| Interpreter of this build \| 3.12.12 \| observed when the cell ran \| Note: observed value (platform.python_version); no test pins it (nor can it); 3.12.12 not asserted | gen:paper/generate_repro.py::toolchain | unbacked | drop |
| U25-C017 | R | \| Platform of this build \| macOS-26.5.2-arm64-arm-64bit \| observed when the cell ran \| Note: observed value (platform.platform); no test pins it | gen:paper/generate_repro.py::toolchain | unbacked | drop |
| U25-C018 | R | \| Commit \| f6c5df378b94de1c7d878de056447a448971eeba \| observed when the cell ran, in a checkout \| Note: test checks only form of the commit (40 hex, not found or empty); the hash is an observation, and the 'in a checkout' note is covered by the git-absence test only | gen:paper/generate_repro.py::toolchain test:tests/test_paper.py::test_toolchain_matches_the_lock_pyproject_and_python_version | broader than its backing | narrow |
| U25-C019 | S | The tests assume a git checkout of the repository: a few read its history Note: 'a few read its history' true (test_v2_data, test_experiments use git log/diff); but test_cr18 only checks the prose; no-checkout behavior is not tested | test:tests/test_paper.py::test_cr18_appendix_f_says_how_to_compare_regenerate_and_what_needs_a_checkout | broader than its backing | narrow |
| U25-C020 | S | in a copy made without it they skip with a reason. Note: narrower truth: without history test_v2_data fails explicitly (pytest.fail) or passes silently (ordering check), test_experiments fail on git diff/log; none skip with a reason | none | broader than its backing | narrow |
| U25-C021 | S | The last row of the table regenerates one row of F.4, the cells it needs included. Note: wrong row: the last row of the commands table is the myst build; regenerate_row is second to last (probably 'the penultimate row'); the script and test (two rows) are fine | test:tests/test_paper.py::test_cr18_regenerate_row_reproduces_the_committed_output_of_a_row | broader than its backing | narrow |
| U25-C022 | S | \| uv sync --locked \| install the locked environment \| exits 0 \| Note: CI runs the command; 'exits 0' is not a test assertion; test_container only checks the Dockerfile contains it | file:.github/workflows/test.yml test:tests/test_container.py::test_locked_install_and_pinned_uv | broader than its backing | narrow |
| U25-C023 | S | \| uv lock --check \| check that the lock matches pyproject.toml \| exits 0 \| Note: lock_cmd 'uv lock --check' is in the contract and CI; exit 0 not asserted by a test | file:.github/workflows/test.yml work-packages/interface-contract.toml | broader than its backing | narrow |
| U25-C024 | S | \| uv run pytest \| run the test suite, doctests included \| all tests pass \| Note: CI runs uv run pytest; the pass is the CI result, not a test; doctests enabled in pyproject (not re-verified here) | file:.github/workflows/test.yml test:tests/test_paper.py::test_f_commands_exist_in_the_repository | broader than its backing | narrow |
| U25-C025 | S | \| uv run python -m derivation.run \| run the chain L1 to L17 \| every lemma reports PASS \| Note: derivation/run.py prints PASS per lemma and 'ALL LEMMAS PASS'; the named test runs main() == 0 and checks ALL LEMMAS PASS and L1 -> L17; 'L1 to L17' is generated from lemma files (last = 17) | test:tests/test_derivation.py::test_wp13_audit_lists_new_axioms_and_headline_names_fallbacks test:tests/test_paper.py::test_f_commands_exist_in_the_repository | broader than its backing | narrow |
| U25-C026 | S | \| uv run python -m derivation.proofmap \| check the proof map against the scripts \| exits 0 \| Note: only that derivation/proofmap.py exists and the command is listed; 'exits 0' not tested by name | test:tests/test_paper.py::test_f_commands_exist_in_the_repository | broader than its backing | narrow |
| U25-C027 | S | \| uv run python paper/execute_notebooks.py \| execute both notebooks from a clean kernel and write the outputs \| exits 0; the outputs are unchanged when the data and the seeds are: `git diff --stat -- paper/paper.ipynb paper/supporting_material.ipynb` then shows only the commit and platform lines of the toolchain table, and `PAPER_EXECUTE=1 uv run pytest tests/test_paper.py -k clean_kernel` compares every other text output of a fresh run with the committed one \| Note: clean_kernel test (gated PAPER_EXECUTE) compares all text outputs but skips tab-F-toolchain entirely; 'git diff --stat shows only commit and platform lines' is untested (Node, interpreter lines also observed) | test:tests/test_paper.py::test_cr18_appendix_f_says_how_to_compare_regenerate_and_what_needs_a_checkout test:tests/test_paper.py::test_notebooks_execute_from_a_clean_kernel_and_match_the_committed_outputs | broader than its backing | narrow |
| U25-C028 | S | \| uv run python paper/regenerate_row.py ROW \| regenerate one row of the table in F.4 (ROW is its first column): runs the cells that row needs and prints the table or saves the figure, writing nothing in the repository \| prints the table, equal to that cell's committed output, or names the figure file \| Note: test pins equality with committed output for two table rows (tab-A-register, tab-F-commands) and SystemExit for an unknown row; 'writes nothing in the repository' and figure-saving untested | test:tests/test_paper.py::test_cr18_regenerate_row_reproduces_the_committed_output_of_a_row test:tests/test_paper.py::test_cr18_appendix_f_says_how_to_compare_regenerate_and_what_needs_a_checkout | broader than its backing | narrow |
| U25-C029 | S | \| cd paper && uv run myst build --html \| build the paper as a static site, written to paper/_build/html \| exits 0, with no error reported; it prints a line that a server started on a local port, because the builder renders the pages through a temporary server that stops when the build ends \| Note: gated (PAPER_BUILD) test asserts returncode 0, no error mark, index.html exists; the server-line remark rests on paper/BROWSER_NOTES.md (observation) only | test:tests/test_paper.py::test_myst_builds_the_html_site | broader than its backing | narrow |
| U25-C030 | S | shows only the commit and platform lines of the toolchain table Note: test skips tab-F-toolchain wholly, so it does not show that only the commit and platform lines differ; the git diff claim is untested | test:tests/test_paper.py::test_notebooks_execute_from_a_clean_kernel_and_match_the_committed_outputs | broader than its backing | narrow |
| U25-C031 | S | compares every other text output of a fresh run with the committed one | test:tests/test_paper.py::test_notebooks_execute_from_a_clean_kernel_and_match_the_committed_outputs | backed | keep |
| U25-C032 | S | because the builder renders the pages through a temporary server that stops when the build ends Note: explanation of builder behavior; only in paper/BROWSER_NOTES.md (observation of the build), no test or cited source | none | unbacked | drop |
| U25-C033 | S | \| tab-families \| `family_table()` \| paper/prior_art.yaml \| cell tab-families of paper.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | backed | keep |
| U25-C034 | S | \| fig-tau-sweep \| `case.tau_sweep_figure(study, fit)` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell fig-tau-sweep of paper.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | backed | keep |
| U25-C035 | S | \| fig-plane-k1 \| `case.log_plane_figure(study, fit)` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell fig-plane-k1 of paper.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | backed | keep |
| U25-C036 | S | \| fig-plane-k3 \| `case.log_plane_figure(study, fit3, band=band)` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell fig-plane-k3 of paper.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | backed | keep |
| U25-C037 | S | \| fig-chart-k3 \| `case.coordinates_figure(study, fit3, band=band)` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell fig-chart-k3 of paper.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | backed | keep |
| U25-C038 | S | \| fig-tensions-k3 \| `case.tension_figure(study, fit3, band=band)` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell fig-tensions-k3 of paper.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | backed | keep |
| U25-C039 | S | \| fig-regimes \| `case.regime_figure()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell fig-regimes of paper.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | backed | keep |
| U25-C040 | S | \| fig-predict-check \| `case.predict_check_figure(study, reg)` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell fig-predict-check of paper.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell | backed | keep |
| U25-C041 | S | \| tab-A-register \| `register_table()` \| glossary.yaml \| cell tab-A-register of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C042 | S | \| tab-B-how-to-read \| `how_to_read()` \| derivation/proof_map_record.json \| cell tab-B-how-to-read of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C043 | S | \| tab-B-proof-map \| `proof_map()` \| derivation/proof_map_record.json \| cell tab-B-proof-map of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C044 | S | \| tab-B-proofs-fit \| `proofs_fit()` \| derivation/proof_map_record.json \| cell tab-B-proofs-fit of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C045 | S | \| tab-B-proofs-solver \| `proofs_solver()` \| derivation/proof_map_record.json \| cell tab-B-proofs-solver of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C046 | S | \| tab-B-checker \| `checker()` \| derivation/proof_map_record.json \| cell tab-B-checker of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C047 | S | \| tab-C-configuration_space \| `configuration_space()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-C-configuration_space of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C048 | S | \| tab-C-evaluation \| `evaluation()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-C-evaluation of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C049 | S | \| tab-C-attribute_sources \| `attribute_sources()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-C-attribute_sources of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C050 | S | \| tab-C-feasibility \| `feasibility()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-C-feasibility of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C051 | S | \| tab-C-conditioning \| `conditioning()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-C-conditioning of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C052 | S | \| tab-C-metric_table \| `metric_table()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-C-metric_table of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C053 | S | \| tab-C-datasets \| `datasets()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-C-datasets of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C054 | S | \| tab-C-planted_example \| `planted_example()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-C-planted_example of supporting_material.ipynb \| Note: Row and call pinned; Reads column is the CASE_DATA default but the function builds synthetic data with make_frontier_data, reads no CSV | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | broader than its backing | narrow |
| U25-C055 | S | \| tab-D-temperature_selection \| `temperature_selection()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-temperature_selection of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C056 | S | \| tab-D-k_diagnostics \| `k_diagnostics()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-k_diagnostics of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C057 | S | \| tab-D-exponents_and_facets \| `exponents_and_facets()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-exponents_and_facets of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C058 | S | \| tab-D-regime_comparison \| `regime_comparison()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-regime_comparison of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C059 | S | \| tab-D-sensitivity_variants \| `sensitivity_variants()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-sensitivity_variants of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C060 | S | \| tab-D-refits_by_category \| `refits_by_category()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-refits_by_category of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C061 | S | \| tab-D-candidate_designs \| `candidate_designs()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-candidate_designs of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C062 | S | \| tab-D-termination_records \| `termination_records()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-termination_records of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C063 | S | \| tab-D-margin_reading \| `margin_reading()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-margin_reading of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C064 | S | \| tab-D-nondominated \| `nondominated()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-nondominated of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C065 | S | \| tab-D-propose_predict_check \| `propose_predict_check()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-propose_predict_check of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C066 | S | \| tab-D-stability \| `stability()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-stability of supporting_material.ipynb \| Note: Row and call pinned; Reads column is the CASE_DATA default but the function reads the committed stability records (paper_stability), not only the CSVs | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | broader than its backing | narrow |
| U25-C067 | S | \| tab-D-conditioning_diagnostic \| `conditioning_diagnostic()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-conditioning_diagnostic of supporting_material.ipynb \| Note: Row and call pinned; Reads column is the CASE_DATA default but the function Reads default CASE_DATA not verified for this function | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | broader than its backing | narrow |
| U25-C068 | S | \| tab-D-own_rows_refit \| `own_rows_refit()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-own_rows_refit of supporting_material.ipynb \| Note: Row and call pinned; Reads column is the CASE_DATA default but the function runs make_frontier_data seeds, reads no CSV | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | broader than its backing | narrow |
| U25-C069 | S | \| tab-D-planted_recovery \| `planted_recovery()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-planted_recovery of supporting_material.ipynb \| Note: Row and call pinned; Reads column is the CASE_DATA default but the function runs make_frontier_data seeds, reads no CSV | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | broader than its backing | narrow |
| U25-C070 | S | \| tab-D-mean_slack_fixed \| `mean_slack_fixed()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-mean_slack_fixed of supporting_material.ipynb \| Note: Row and call pinned; Reads column is the CASE_DATA default but the function reads the committed stability ledger, not only the CSVs | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | broader than its backing | narrow |
| U25-C071 | S | \| tab-D-pca_chain \| `pca_chain()` \| examples/adcs/data/ (the regimes' CSV files named by the case module) \| cell tab-D-pca_chain of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C072 | S | \| tab-E-gaps \| `gaps_table()` \| docs/superpowers/notes/abstraction-gaps.md \| cell tab-E-gaps of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C073 | S | \| tab-F-toolchain \| `toolchain()` \| uv.lock, pyproject.toml, .python-version \| cell tab-F-toolchain of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C074 | S | \| tab-F-commands \| `commands()` \| uv.lock, pyproject.toml, .python-version \| cell tab-F-commands of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C075 | S | \| tab-F-reproduction \| `reproduction_table()` \| uv.lock, pyproject.toml, .python-version \| cell tab-F-reproduction of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C076 | S | \| tab-G-register \| `register()` \| paper/prior_art.yaml \| cell tab-G-register of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |
| U25-C077 | S | \| tab-G-reading_pass_table \| `reading_pass_table()` \| paper/reading_pass.yaml \| cell tab-G-reading_pass_table of supporting_material.ipynb \| | gen:paper/generate_repro.py::reproduction_rows test:tests/test_paper.py::test_f_has_a_row_for_every_figure_and_table_cell test:tests/test_paper.py::test_figure_and_table_cells_are_exactly_one_call | backed | keep |

### U26: supp Appendix G. Register of prior art (`paper/supporting_material.ipynb`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U26-C001 | R | The bibliographic records of the cited works were verified | test:tests/test_references.py::test_every_entry_records_its_verification file:docs/references.bib | backed | keep |
| U26-C002 | R | what each work says was read only in part | file:paper/reading_pass.yaml test:tests/test_paper.py::test_reading_pass_yaml_matches_the_markdown_table_verbatim | backed | keep |
| U26-C003 | R | Its entries are the works and families most immediately relevant to the method Note: Tests pin only that outline families have entries; "most immediately relevant" is the author's selection judgement, not checked; reword as selection or back by reading. | test:tests/test_paper.py::test_every_family_of_the_outline_has_an_entry | broader than its backing | narrow |
| U26-C004 | R | and each says what this work does differently, extends or adds | test:tests/test_paper.py::test_prior_art_entries_have_four_nonempty_fields_and_unique_ids test:tests/test_paper.py::test_prior_art_says_nothing_is_novel_first_or_new | backed | keep |
| U26-C005 | R | A fresh reader read what is accessible of each cited work | file:paper/reading_pass.yaml file:work-packages/WP10-reading-pass.md test:tests/test_paper.py::test_reading_pass_table_is_in_appendix_g_and_current | backed | keep |
| U26-C006 | R | abstracts, open full texts, publisher descriptions; not the paywalled books and articles | file:paper/reading_pass.yaml | backed | keep |
| U26-C007 | R | A sentence was kept where the verdict is supported Note: No test asserts supported implies kept, and rows 45 and 46 are supported yet reworded (other half of the sentence); narrow to "kept where supported, except where another part was reworded". | test:tests/test_paper.py::test_reading_pass_rows_carry_what_the_paper_does_and_resolve_in_the_bibliography | broader than its backing | narrow |
| U26-C008 | R | reworded to what was read where it is partly supported or not found | test:tests/test_paper.py::test_reading_pass_rows_carry_what_the_paper_does_and_resolve_in_the_bibliography | backed | keep |
| U26-C009 | R | where the source was not accessible, reworded to what its record supports and marked *to be confirmed by the author* | test:tests/test_paper.py::test_reading_pass_rows_carry_what_the_paper_does_and_resolve_in_the_bibliography test:tests/test_paper.py::test_reading_pass_table_is_in_appendix_g_and_current | backed | keep |
| U26-C010 | R | The sentence on the author's INCOSE paper is listed for him and unchanged. | test:tests/test_paper.py::test_reading_pass_rows_carry_what_the_paper_does_and_resolve_in_the_bibliography file:paper/reading_pass.yaml | backed | keep |
| U26-C011 | R | checked each sentence of {numref}`section %s <sect-problem>` and {numref}`section %s <sect-prior-art>` Note: No test or mapping shows that every attribution sentence of the two sections (plus L11 sketch, process paragraph) has a row; only the 56 rows exist; completeness is unchecked. | file:work-packages/WP10-reading-pass.md file:paper/reading_pass.yaml | broader than its backing | narrow |
| U26-C012 | S | The repository keeps:** the long review with its dropped candidates | test:tests/test_paper_sources.py::test_the_six_snapshots_and_the_move_table_exist file:docs/superpowers/notes/paper-sources/literature.md file:docs/references.bib | backed | keep |
| U26-S01 | R | Most verdicts rest on abstracts. | file:paper/reading_pass.yaml | backed | keep |

### U27: docs index (`docs/index.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U27-C001 | S | learns the shape of a design trade space from evaluated designs | test:tests/test_estimator.py::test_recovery_tau_inf test:tests/test_estimator.py::test_recovery_tau_1e3 | backed | keep |
| U27-C002 | S | model in the posynomial invariant form. It then tells you which metrics contend | test:tests/test_tensions.py::test_contending_set_recovers_planted_support test:tests/test_estimator.py::test_fit_invariants test:tests/test_estimator.py::test_recovery_tau_inf | backed | keep |
| U27-C003 | S | It then tells you which metrics contend, at what exchange | test:tests/test_tensions.py::test_contending_set_recovers_planted_support test:tests/test_tensions.py::test_exponents_and_elasticities_consistent | backed | keep |
| U27-C004 | S | rate, where each design sits relative to the fitted reference surface | test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples test:tests/test_estimator.py::test_project_and_improvement_factors_land_on_frontier | backed | keep |
| U27-C005 | S | and where the table has gaps | test:tests/test_gaps.py::test_find_holes_2d_planted_disc test:tests/test_gaps.py::test_find_holes_1d_planted_gap test:tests/test_gaps.py::test_knn_flags_isolated_point | backed | keep |
| U27-C006 | S | It is a scikit-learn estimator (`fit`, `transform`, `inverse_transform`, `score_samples`) in the | test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator | backed | keep |
| U27-C007 | S | unsupervised and feature-engineering family, beside PCA | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score test:tests/test_estimator.py::test_pipeline_and_feature_names | backed | keep |
| U27-C008 | M | PCA finds where the data spread, this finds Note: PCA (spread) half is the definition of PCA (L-type, jolliffe2016principal); no lemma step; as an M claim there is no lemma, only tests of orient_by_pca; recast as S/L. | test:tests/test_gaps.py::test_orient_by_pca_rotation_and_sign test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions | broader than its backing | to the driver |
| U27-C009 | M | where they stop, and the two chain. Note: 'where they stop' is backed at tau=inf only (V<=1 for all rows); at finite tau a tenth of designs lie above V=1; 'chain' backed as S (tension directions = PCA of near-frontier Z), not an M lemma step; also no lemma. | test:tests/test_estimator.py::test_fit_invariants test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions test:tests/test_estimator.py::test_pipeline_and_feature_names | broader than its backing | to the driver |
| U27-C010 | R | a cubesat trade study across power, mass and attitude control Note: Description of the page's example; examples.md numbers are covered by other rows; no R-number here, but grouping power/mass/attitude control is pinned by tests/test_cubesat_model.py (WP18 R-7 partition test) - treat as scope statement; no gen/test pair for 'a trade study' as R. | none | unbacked | drop |
| U27-C011 | S | The [project page](../) links the paper, which is where the argument for the method is made Note: Link '../' resolves (test_site), but test_site asserts the paper page says 'The paper is in preparation' so 'links the paper' is true only as a link to the paper route; 'where the argument is made' is intent. | test:tests/test_site.py::test_root_and_paper_links_classified test:tests/test_site.py::test_docs_relative_links_resolve | broader than its backing | narrow |

### U28: docs getting-started (`docs/getting-started.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U28-C001 | S | The package is installed from source for now. It needs Python 3.12 and uses | file:pyproject.toml test:tests/test_interface_contract.py | backed | keep |
| U28-C002 | R | The table below is synthetic: 300 designs scored on 3 metrics, all positive and larger-is-better, Note: test pins positivity for a 500x4 table, not this 300x3 call (planted frontier yes); the run block is only executed by test_docs::test_runnable_blocks_execute; no test pins 300 designs/3 metrics here | test:tests/test_datasets.py::test_frontier_info_and_planting | broader than its backing | narrow |
| U28-C003 | R | The output is `trilemma [0 1 2]` and then `[0.3  0.37 0.33]`. Note: exact printed output [0.3 0.37 0.33] at temperature 20 on make_frontier_data(300,3,random_state=0) is not pinned by any test (blocks are only executed); doctest in tensions.py uses 400 rows at tau=inf | none | unbacked | drop |
| U28-C004 | R | metrics 0 and 1 the designs lie on or just beyond a straight frontier, and the grey band marks those Note: test pins how the line and band are drawn on a 100-row table, not that these designs lie on or just beyond the frontier; data behaviour not pinned | test:tests/test_plotting.py::test_log_plane_draws_frontier_line_in_black_and_band_in_grey | unbacked | drop |
| U28-C005 | M | The idea is easiest to see with two of the metrics, where the model is a line. | lemma:L1 test:tests/test_plotting.py::test_log_plane_draws_frontier_line_in_black_and_band_in_grey | backed | keep |
| U28-C006 | S | `fit` learned one exponent per metric, summing to one. | test:tests/test_estimator.py::test_fit_invariants | backed | keep |
| U28-C007 | S | summing to one. `report.contending_set` lists the metrics that | test:tests/test_tensions.py::test_contending_set_recovers_planted_support func:src/hyperbolic_trade_space/tensions.py::tension_report | backed | keep |
| U28-C008 | R | contend at the edge of the table: here all three, an n-lemma with n = 3, which the report names a Note: that all three contend with n=3 trilemma on this table is not pinned: doctest is 400 rows tau=inf, test_k1_is_a_single_report uses the same call only for type; naming rule is pinned by test_contending_set_recovers_planted_support | none | unbacked | drop |
| U28-C009 | S | The set is found from the data and not chosen in advance. | test:tests/test_tensions.py::test_contending_set_recovers_planted_support test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact | backed | keep |
| U28-C010 | M | fitted weights at the working temperature; their ratios are the elasticities between the contending | lemma:L7 test:tests/test_tensions.py::test_exponents_and_elasticities_consistent | backed | keep |
| U28-C011 | S | `ts.score_samples(X)` is the log of V for each design, the energy | test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples lemma:L1 glossary:energy-differential | backed | keep |
| U28-C012 | M | differential to the fitted reference surface: negative inside, positive beyond. | registered:C004 | backed | keep |
| U28-C013 | S | is the chart, `d - 1` position coordinates plus that log V, and `ts.inverse_transform` undoes it. | test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples lemma:L8 | backed | keep |
| U28-C014 | P | Real attributes are rarely positive, larger-is-better and comparably scaled. Note: general statement about real attributes, no source and not worded as the author's experience; reword as judgment (reading) or drop | none | unbacked | drop |
| U28-C015 | S | From there the guide follows the order of a study: [fit](user-guide/fitting.md), | test:tests/test_site.py::test_docs_relative_links_resolve test:tests/test_site.py::test_nav_pages_exist_and_cover_the_contract_pages | backed | keep |

### U29: docs api (`docs/api.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U29-C001 | S | The package follows the scikit-learn conventions [@pedregosa2011scikit; @buitinck2013api]: parameters | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator test:tests/test_sklearn_compat.py::test_init_stores_parameters_verbatim | backed | keep |
| U29-C002 | S | validation in `fit`, fitted attributes ending in an underscore. | test:tests/test_sklearn_compat.py::test_fitted_attributes_end_in_underscore_and_n_iter_positive test:tests/test_preconditioning.py::test_parameter_validation_in_fit | backed | keep |
| U29-C003 | S | Dimension is arbitrary: `d` metrics and `d - 1` chart coordinates. | test:tests/test_coordinates.py::test_helmert_orthonormal_kernel test:tests/test_datasets.py::test_d1 test:tests/test_estimator.py::test_d1 | backed | keep |
| U29-C004 | S | [`frontier_in_original_units`](user-guide/conditioning.md), a function: the fitted surface as a | test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples func:src/hyperbolic_trade_space/preconditioning.py::frontier_in_original_units | backed | keep |
| U29-C005 | S | [`HyperbolicTradeSpace`](user-guide/fitting.md), a transformer: fits the surface and gives the | test:tests/test_predictive.py::test_recovers_planted_coordinates test:tests/test_estimator.py::test_d1 test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator | backed | keep |
| U29-C006 | S | chart of position and log V. Fitted attributes for every number of terms include `exponents_`, | test:tests/test_estimator.py::test_attributes_exist_for_every_k_and_k1_numbers_are_unchanged test:tests/test_estimator.py::test_k_terms_attributes_conventions test:tests/test_interface_contract.py::test_r1_estimator_methods_and_fitted_attributes | backed | keep |
| U29-C007 | S | `facet_`, `coefficients_`, `facet_share_`, `objective_` (what the solver minimized) and | test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized test:tests/test_estimator.py::test_attributes_exist_for_every_k_and_k1_numbers_are_unchanged | backed | keep |
| U29-C008 | S | `mean_slack_` (the mean slack, to compare fits across numbers of terms). | test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized test:tests/test_case.py::test_mean_slack_by_k_reads_the_estimator_and_the_fixed_tau_refit_shares_one_temperature | backed | keep |
| U29-C009 | S | [`select_temperature`](user-guide/fitting.md), a function: chooses the temperature by a target | test:tests/test_tuning.py::test_selected_temperature_hits_target func:src/hyperbolic_trade_space/tuning.py::select_temperature | backed | keep |
| U29-C010 | S | [`make_frontier_data`](user-guide/fitting.md), a function: seeded synthetic data with a planted | test:tests/test_datasets.py::test_frontier_info_and_planting test:tests/test_datasets.py::test_reproducible_and_noise | backed | keep |
| U29-C011 | S | [`make_configured_frontier_data`](user-guide/prediction.md), a function: the same with | test:tests/test_datasets.py::test_configured | backed | keep |
| U29-C012 | S | [`tension_report`](user-guide/tensions.md), a function: contending set, elasticities and | test:tests/test_tensions.py::test_contending_set_recovers_planted_support test:tests/test_tensions.py::test_exponents_and_elasticities_consistent test:tests/test_tensions.py::test_first_direction_recovers_planted_spread | backed | keep |
| U29-C013 | S | [`TradeSpaceRegressor`](user-guide/prediction.md), a regressor: metrics, coordinates and novelty | test:tests/test_predictive.py::test_recovers_planted_coordinates test:tests/test_predictive.py::test_novelty_beyond_the_soft_frontier | backed | keep |
| U29-C014 | S | `hyperbolic_trade_space.tensions`: `TensionReport`, the object `tension_report` returns. | test:tests/test_interface_contract.py::test_r1_termination_fields_statuses_and_report_fields func:src/hyperbolic_trade_space/tensions.py::tension_report | backed | keep |
| U29-C015 | S | `hyperbolic_trade_space.solvers`: the multi-term solver, the `Termination` record and the | test:tests/test_interface_contract.py::test_r1_submodule_importable_with_pinned_names test:tests/test_interface_contract.py::test_r1_termination_fields_statuses_and_report_fields | backed | keep |
| U29-C016 | S | certificate functions, with `min_curvature` for a soft fit | test:tests/test_interface_contract.py::test_r1_certificate_signatures_exact test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified | backed | keep |
| U29-S01 | S | [`LogAffinePreconditioner`](user-guide/conditioning.md), a transformer: attributes to | test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift test:tests/test_preconditioning.py::test_fitted_attributes_and_larger_is_better_direction | backed | keep |
| U29-S02 | S | `hyperbolic_trade_space.gaps`: `knn_gap_scores`, `find_holes`, `frontier_targets`, `orient_by_pca` | test:tests/test_interface_contract.py::test_r1_submodule_importable_with_pinned_names test:tests/test_gaps.py::test_orient_by_pca_rotation_and_sign | backed | keep |
| U29-S03 | S | `hyperbolic_trade_space.plotting`: `plot_tensions`, `plot_log_plane`, `plot_frontier_surface_3d`, | test:tests/test_interface_contract.py::test_r1_submodule_importable_with_pinned_names test:tests/test_plotting.py::test_plot_tensions_with_real_report | backed | keep |

### U30: docs api-reference (`docs/api-reference.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U30-C001 | S | Generated from the numpydoc docstrings of the public names. Note: Page is mkdocstrings ::: directives for exactly the contract public names (test_site); but numpydoc style is asserted for only 3 names (HyperbolicTradeSpace, select_temperature, tension_report), not all public names | test:tests/test_site.py::test_api_reference_names_equal_the_contract test:tests/test_interface_contract.py::test_r1_docstring_style_pinned | broader than its backing | narrow |

### U31: docs examples (`docs/examples.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U31-C001 | S | conditions the feasible designs for `HyperbolicTradeSpace`. | test:tests/test_case.py::test_load_study_filters_and_conditions | backed | routed to P6 |
| U31-C002 | R | Ten attributes are compared under two controller-gain regimes | gen:examples/adcs/case.py::CUBESAT test:tests/test_case.py::test_load_study_filters_and_conditions test:tests/test_case.py::test_subsystem_mapping_is_data_and_covers_every_attribute | backed | routed to P6 |
| U31-C003 | R | Nothing is simulated here; the evaluated tables are committed. | test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data test:tests/test_case.py::test_regime_comparison_on_frozen_data | backed | routed to P6 |
| U31-C004 | R | The aggressive-gains table has 706 feasible designs. | gen:examples/adcs/case.py::feasible_mask test:tests/test_case.py::test_feasible_mask_counts_on_frozen_data | backed | routed to P6 |
| U31-C005 | R | The tension report finds a contending set of six metrics (total mass, slew time, | gen:examples/adcs/case.py::tension_table test:tests/test_case.py::test_k1_contending_set_equals_the_record | backed | routed to P6 |
| U31-C006 | R | a 6-lemma, found from the data with no prior choice of which | gen:examples/adcs/case.py::tension_table test:tests/test_case.py::test_k1_contending_set_equals_the_record | backed | routed to P6 |
| U31-C007 | R | The mean slack falls from 0.204 at one term to 0.117 at three, and the status is | gen:examples/adcs/case.py::mean_slack_by_k test:tests/test_case.py::test_k_sweep_equals_the_record | backed | routed to P6 |
| U31-C008 | R | 0.117 at three, and the status is | gen:examples/adcs/case.py::k_table test:tests/test_case.py::test_k_sweep_equals_the_record | backed | routed to P6 |
| U31-C009 | R | The three facets have contending sets of 6, 6 and 7 metrics. | gen:examples/adcs/case.py::facet_table test:tests/test_case.py::test_k3_facets_equal_the_primary_record | backed | routed to P6 |
| U31-C010 | R | 78 percent of the near-frontier share and is the only one containing total mass and peak slew Note: 78 percent (share 0.778) and big facet starting 'peak slew power, total mass' are pinned; 'only one containing total mass and peak slew power' not asserted (run confirms the other two lack both, but no test checks the other contending sets) | gen:examples/adcs/case.py::facet_table test:tests/test_case.py::test_k3_facets_equal_the_primary_record | broader than its backing | routed to P6 |
| U31-C011 | R | power; the other two are built on control effort, slew time and energy balance. Note: run shows facets 1,2 largest exponents are control effort/slew time/energy balance, but no test asserts the other two facets' sets or exponents | none | unbacked | routed to P6 |
| U31-C012 | R | The stock-gains table gives a different one-term contending set, so the | gen:examples/adcs/case.py::tension_table test:tests/test_case.py::test_k1_contending_set_equals_the_record | backed | routed to P6 |
| U31-C013 | R | finding depends on the regime evaluated. | gen:examples/adcs/case.py::regime_comparison test:tests/test_case.py::test_k1_contending_set_equals_the_record | backed | routed to P6 |
| U31-C014 | S | The case module in `examples/adcs/case.py` runs the study from the committed table. | test:tests/test_case.py::test_load_study_filters_and_conditions test:tests/test_case.py::test_regime_comparison_on_frozen_data | backed | routed to P6 |
| U31-C015 | R | The six outlined metrics are the contending set; grey labels mark metrics that do not participate. | gen:examples/adcs/case.py::tension_figure test:tests/test_case.py::test_panel_titles_count_the_exact_maximum_support_and_outline_exactly_those test:tests/test_plotting.py::test_plot_tensions_with_stand_in_report | backed | routed to P6 |
| U31-C016 | R | the ringed designs lie nearest the frontier. | gen:src/hyperbolic_trade_space/plotting.py::plot_frontier_coordinates test:tests/test_plotting.py::test_frontier_coordinates_one_and_two_coordinates_and_overlays | backed | routed to P6 |
| U31-C017 | M | A numbered marker is a facet's exponent vector, where that facet's V is largest for a fixed total. | registered:C001 | backed | routed to P6 |
| U31-C018 | M | V also depends on the total, so a marker is not where V = 1. | registered:C001 | backed | routed to P6 |
| U31-C019 | M | A region is where one facet dominates, named by the metrics that trade there: an analysis of the | test:tests/test_plotting.py::test_ternary_regions_partition_the_triangle | backed | routed to P6 |
| U31-C020 | M | A design mostly in metric 3 with a little metric 1 is in the blue region, where metric 3 trades Note: worked reading of the figure ('blue region', metric 3 vs metric 1) is an illustration on the planted table; no test pins the colours or which metrics trade in the region; a how-to-read example | test:tests/test_plotting.py::test_ternary_regions_partition_the_triangle | broader than its backing | routed to P6 |
| U31-C021 | M | the triangle is for reading, not for measuring distance | definition | backed | routed to P6 |
| U31-C022 | R | case do not separate in three metrics, so none is drawn for the cubesat. Note: no generator or test shows ten-metric cubesat designs do not separate in three metrics; only that plot_ternary refuses X with groups (ValueError); the 'do not separate' result is unbacked | test:tests/test_plotting.py::test_ternary_names_schemes_and_ax | broader than its backing | routed to P6 |
| U31-C023 | M | Exponents add over groups exactly: a facet's weight on a subsystem is a sum. | test:tests/test_plotting.py::test_ternary_groups_sum_the_exponents_exactly test:tests/test_plotting.py::test_ternary_cubesat_groups_are_the_docs_example_and_the_group_sums_hold | backed | routed to P6 |
| U31-C024 | R | The three-term cubesat fit by summed exponents: only facet 3 carries mass (0.18). | gen:examples/adcs/case.py::fit_study test:tests/test_plotting.py::test_ternary_cubesat_groups_are_the_docs_example_and_the_group_sums_hold | backed | routed to P6 |
| U31-C025 | R | facets 1 and 2 lie on the power and attitude control edge, and facet 3 sits inside, carrying some mass. | gen:examples/adcs/case.py::fit_study test:tests/test_plotting.py::test_ternary_cubesat_groups_are_the_docs_example_and_the_group_sums_hold | backed | routed to P6 |
| U31-C026 | S | `k_terms.py`, which reproduces the one-, two- and three-term fits: | gen:examples/adcs/k_terms.py::run_regime test:tests/test_k_terms_case.py::test_k3_fits_and_three_reports | backed | routed to P6 |
| U31-C027 | P | The same steps apply to any table of designs: condition, `select_temperature`, fit, then read the | definition | backed | routed to P6 |

### U32: docs theory (`docs/theory.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U32-C001 | M | Because the weights sum to one, $V(\lambda m)=\lambda V(m)$: doubling every metric doubles V. | lemma:L1.5 glossary:invariant-value registered:C002 | backed | keep |
| U32-C002 | M | reads as a factor of improvement, which is what "invariant" refers to. | definition glossary:invariant-value lemma:L1.5 | backed | keep |
| U32-C003 | M | extends one term to K terms and keeps the programs inside geometric programming. | lemma:L10.7 lemma:L16.49 glossary:generalized-posynomial | backed | keep |
| U32-C004 | M | so the surface V = 1 is where the posynomial equals one. | lemma:L10.7 glossary:posynomial registered:C018 | backed | keep |
| U32-C005 | M | Fitting one facet is a geometric program (GP), solved as | lemma:L4.24 glossary:geometric-program | backed | keep |
| U32-C006 | M | fitting several facets alternates weights from | lemma:L16.49 lemma:L16.48 lemma:L15.16 | backed | keep |
| U32-C007 | S | The package takes the sharp limit of the weights, one | test:tests/test_soft_fit.py::test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis file:work-packages/interface-contract.md | backed | keep |
| U32-C008 | S | which facet dominates a design is analysis of the fitted model, not part of the fit. | test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis glossary:assignment | backed | keep |
| U32-C009 | M | The fit chooses $w$ and an offset $\beta$ so that the data lie on or below the surface Note: 'on or below' holds only at tau=infinity (beta = max); at finite tau beta = LME <= max (L5.15), so rows lie beyond the surface, as the next bullet itself says | lemma:L5.15 lemma:L1.7 | broader than its backing | to the driver |
| U32-C010 | M | With one term this is a convex program. | lemma:L4.13 lemma:L4.24 | backed | keep |
| U32-C011 | M | V = 1 at the working temperature tau; it is smooth, so a few Note: L5.15 (LME <= max) gives the top design on or beyond V=1; 'a few designs' (a count) is not stated by any step | lemma:L5.15 glossary:fitted-reference-surface | broader than its backing | to the driver |
| U32-C012 | M | the same fit at tau = infinity: the exact maximum, a linear program, | lemma:L5.24 lemma:L12.31 glossary:supporting-envelope | backed | keep |
| U32-C013 | M | the nondominated set of the attainable designs, a property of the system | definition glossary:pareto-boundary | backed | keep |
| U32-C014 | M | The fit does not identify the other two with it. | lemma:L11 glossary:pareto-boundary glossary:supporting-envelope | backed | keep |
| U32-C015 | M | Inside the surface V < 1; beyond it V > 1, and V - 1 says by how much. | lemma:L1.7 glossary:energy-differential | backed | keep |
| U32-C016 | M | where $Z$ is free of overall scale and says where along the surface the design sits, and $\log V$ says | registered:C009 lemma:L8.6 glossary:chart | backed | keep |
| U32-C017 | M | The map is reversible for every row with strictly positive metrics: nothing is lost Note: L8 proves the bijection of (log-scale, Z) i.e. u, not of (Z, log V); the step to log V = w.u - beta is untagged (the test pins the round trip on data only) | registered:C010 lemma:L8.14 test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples | broader than its backing | to the driver |
| U32-C018 | M | Holes in the $Z$ plane are candidates for white space. | definition glossary:white-space | backed | keep |
| U32-C019 | M | the level surface is flat in log space, so moving along it trades | lemma:L7.5 lemma:L1.7 glossary:elasticity | backed | keep |
| U32-C020 | M | It is found from the data and not assumed: the fit at | test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact glossary:contending-set glossary:n-lemma | backed | keep |
| U32-C021 | M | tau = infinity is a linear program whose solution is generically sparse. Note: LP part backed (L12.31); 'generically sparse' is not proven, only pinned on planted sparse supports (an LP vertex is sparse, but no step or test says generic) | test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact lemma:L12.31 | broader than its backing | to the driver |
| U32-C022 | M | temperature a small weight means weak participation, set by a participation threshold. | test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact glossary:participation-threshold | backed | keep |
| U32-C023 | M | terms there is one contending set per facet, and elasticities vary between facets. | test:tests/test_tensions.py::test_k3_reports_one_per_facet_recover_planted_supports glossary:contending-set | backed | keep |
| U32-C024 | M | larger-is-better (conditioning is yours to choose); the surface is log-convex; Note: Positivity/larger-is-better are assumptions; 'log-convex surface' is not a tagged step (L10.7 posynomial; L4 convexity is in w, not in log m) | lemma:L10.7 lemma:L4.24 glossary:posynomial | broader than its backing | to the driver |
| U32-C025 | M | at one term the elasticities are constant; designs are chosen by an evaluator and not drawn from | lemma:L7.5 lemma:L10.9 definition | backed | keep |
| U32-C026 | S | The argument itself lives in the project repository, in the derivation scripts under `derivation/` Note: derivation scripts exist; the sentence goes on to name a README there and derivation/ has no README | file:derivation/lemma_01_homogeneity.py file:derivation/PROOF_MAP_FINDINGS.md | broader than its backing | narrow |

### U33: docs further-reading (`docs/further-reading.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U33-C001 | S | scikit-learn and its API design [@pedregosa2011scikit; @buitinck2013api]: the conventions the Note: S half backed (parametrize_with_checks, empty expected failures); the two cited works have no audit row in prior_art.yaml/reading_pass.yaml, so attributing the conventions to them is unbacked | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator | broader than its backing | narrow |
| U33-C002 | L | Boyd and Vandenberghe, *Convex Optimization* [@boyd2004convex]: the notation used on these pages. Note: no reading_pass/prior_art row for boyd2004convex; the notation claim is the author's alignment, mark as reading or add an audit row | none | unbacked | drop |
| U33-C003 | L | A tutorial on geometric programming [@boyd2007tutorial]: posynomials and generalized posynomials, | bib:boyd2007tutorial reading_pass:n37 | backed | keep |
| U33-C004 | M | the family the multi-term fit stays inside. | lemma:L10 lemma:L16.49 bib:boyd2007tutorial | backed | keep |
| U33-C005 | L | Fitting softmax-affine functions to data so they remain compatible with geometric programming | bib:hoburg2016data reading_pass:n39 | backed | keep |
| U33-C006 | L | [@hoburg2016data] is the source of the multi-term fit. Note: audit supports only the abstract's content; 'the source of the multi-term fit' attributes the package's fit to it, beyond what was read | bib:hoburg2016data reading_pass:n39 | broader than its backing | narrow |
| U33-C007 | L | Fitting convex piecewise-linear functions by alternating partition and refit [@magnani2009convex]: | bib:magnani2009convex reading_pass:n40 | backed | keep |
| U33-C008 | L | Reweighted $\ell_1$ minimization [@candes2008enhancing]: the sparsity option, | bib:candes2008enhancing reading_pass:n41 | backed | keep |
| U33-C009 | S | minimization [@candes2008enhancing]: the sparsity option, `penalty="reweighted_l1"`. | test:tests/test_solvers.py::test_reweighted_l1_gives_exact_zeros_on_planted_sparse_facet test:tests/test_estimator.py::test_penalty_gives_exact_zero_exponents_at_the_estimator | backed | keep |
| U33-C010 | L | the second source of the multi-term fit. | bib:magnani2009convex reading_pass:n40 | backed | keep |
| U33-C011 | L | Isometric log-ratio transformations for compositional data [@egozcue2003isometric] and principal Note: reading_pass n36 egozcue2003isometric verdict not accessible (title only); the fragment is just the title, narrow or accept as bibliographic | none | unbacked | drop |
| U33-C012 | L | component analysis of compositional data [@aitchison1983principal]: the neighbours of the chart. Note: aitchison1983principal (n34) and egozcue (n36) not accessible; 'neighbours of the chart' is the author's comparison, word as judgment (reading) or drop | none | unbacked | drop |
| U33-C013 | L | Kernel PCA [@schoelkopf1998nonlinear]: the kin of the documented kernel direction, which is not | bib:schoelkopf1998nonlinear reading_pass:n43 | backed | keep |
| U33-C014 | S | the kin of the documented kernel direction, which is not | definition | backed | keep |
| U33-C015 | L | HoroPCA [@chami2021horopca]: principal component analysis in hyperbolic space, which this package | bib:chami2021horopca reading_pass:n44 | backed | keep |
| U33-C016 | S | principal component analysis in hyperbolic space, which this package | definition | backed | keep |
| U33-C017 | L | Data envelopment analysis [@charnes1978measuring]: a frontier estimator from efficiency Note: reading_pass n16 charnes1978measuring verdict not accessible; row says only title-level scoring is kept | none | unbacked | drop |
| U33-C018 | P | analysis, the nearest neighbour outside engineering design. | reading | backed | keep |

### U34: docs user-guide/overview (`docs/user-guide/overview.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U34-C001 | M | PCA finds the directions in which the data spread; | bib:jolliffe2016principal | backed | keep |
| U34-C002 | M | this method finds the positive combination of the metrics along which the data stop, Note: L3 gives KKT/optimality of the fitted weights and L1 the invariant form; neither states the data 'stop' along the combination (a descriptive gloss of the fit; no global guarantee, see C020) | lemma:L3 lemma:L1 | broader than its backing | to the driver |
| U34-C003 | M | constraint among metrics that are all better when larger. | definition | backed | keep |
| U34-C004 | S | The answer is one weight per metric, the | test:tests/test_estimator.py::test_fit_invariants test:tests/test_tensions.py::test_exponents_and_elasticities_consistent | backed | keep |
| U34-C005 | M | weights sum to one, and the metrics with non-negligible weight are the ones that contend. Note: sum to one is the simplex axiom (L1, A2) and tested; 'non-negligible weight = contend' holds exactly only at tau=inf; at finite tau weights are smoothed and participation depends on a threshold (the test says so) | lemma:L1 lemma:L3 test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact | broader than its backing | to the driver |
| U34-C006 | S | found from the data, so you need not know in advance which dilemma or trilemma your problem holds. | test:tests/test_tensions.py::test_contending_set_recovers_planted_support | backed | keep |
| U34-C007 | M | The weights define a score V, a weighted geometric mean of the metrics. | lemma:L1 glossary:invariant-value | backed | keep |
| U34-C008 | M | V = 1 is the fitted reference surface, | lemma:L1 | backed | keep |
| U34-C009 | M | V below 1 is inside it and V above 1 is beyond | registered:C004 lemma:L1 | backed | keep |
| U34-C010 | M | Because V scales with the metrics, it reads as a factor of improvement. | lemma:L1 lemma:L7 | backed | keep |
| U34-C011 | S | A study has five stages and the package covers the last three: | definition | backed | keep |
| U34-C012 | S | attributes, with a simulator, a test or an assessment. The package never sees | definition | backed | keep |
| U34-C013 | S | the weights and the metrics that participate; | test:tests/test_tensions.py::test_exponents_and_elasticities_consistent test:tests/test_tensions.py::test_contending_set_recovers_planted_support | backed | keep |
| U34-C014 | S | its energy differential (level offset) to the fitted reference surface and its | test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples test:tests/test_coordinates.py::test_round_trip_and_invariance | backed | keep |
| U34-C015 | S | how much one metric alone would need to improve to reach the surface; | lemma:L7 test:tests/test_estimator.py::test_project_and_improvement_factors_land_on_frontier | backed | keep |
| U34-C016 | S | a novelty score and candidate white space; | test:tests/test_estimator.py::test_novelty_score test:tests/test_gaps.py::test_find_holes_2d_planted_disc | backed | keep |
| U34-C017 | S | the surface written back in your original attribute units; | lemma:L9 test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples | backed | keep |
| U34-C018 | S | a stopping record, [`termination_` and `conditioning_`](termination.md), saying how far to trust | test:tests/test_estimator.py::test_termination_record_for_k_terms test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue | backed | keep |
| U34-S01 | S | the elasticities between contending metrics; | lemma:L7 test:tests/test_tensions.py::test_exponents_and_elasticities_consistent | backed | keep |

### U35: docs user-guide/conditioning (`docs/user-guide/conditioning.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U35-C001 | S | The fit consumes a strictly positive matrix of larger-is-better metrics. | test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift | backed | keep |
| U35-C002 | P | attributes: kilograms, dollars, error rates, counts, some of them better when small. | reading | backed | keep |
| U35-C003 | S | which implements the family of maps the method allows, | test:tests/test_preconditioning.py::test_fitted_attributes_and_larger_is_better_direction func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner | backed | keep |
| U35-C004 | S | `frontier_in_original_units`, which reports the fitted surface back in the units you started with. | test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples func:src/hyperbolic_trade_space/preconditioning.py::frontier_in_original_units | backed | keep |
| U35-C005 | S | smaller-is-better attribute is inverted in log space and comes out larger-is-better. | test:tests/test_preconditioning.py::test_fitted_attributes_and_larger_is_better_direction | backed | keep |
| U35-C006 | S | a judgement about the problem, and a wrong sign is not detected: the fit finds a surface for the Note: No test or doc claim backs that a wrongly oriented fit is undetected; tests only reject orientation entries other than +1/-1 | none | unbacked | drop |
| U35-C007 | S | The cheap diagnostic is the sign of the pulled-back exponent below. | test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples | backed | keep |
| U35-C008 | S | `shift` moves the argument to `a + shift`; it must keep every | test:tests/test_preconditioning.py::test_negative_after_shift_raises func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner | backed | keep |
| U35-C009 | S | value nonnegative, and `ValueError` with "Negative values in data" is raised otherwise. | test:tests/test_preconditioning.py::test_negative_after_shift_raises | backed | keep |
| U35-C010 | M | decision about where the scale begins, and different shifts give different fits. Note: No lemma or test shows different attribute shifts give different fits; L2 is the uniform shift of log data, a different statement | none | unbacked | to the driver |
| U35-C011 | S | The reference point is the attribute value that maps to metric 1; it is the centre removed by the | test:tests/test_preconditioning.py::test_fitted_attributes_and_larger_is_better_direction func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner | backed | keep |
| U35-C012 | S | scaler and stored as `log_offset_`. It fixes what V = 1 means in practice. | test:tests/test_preconditioning.py::test_fitted_attributes_and_larger_is_better_direction | backed | keep |
| U35-C013 | S | a scaler is fitted per column. `scaler="standard"` gives each metric unit | test:tests/test_preconditioning.py::test_unit_log_standard_deviation func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner | backed | keep |
| U35-C014 | S | normalizes the interquartile range instead and suits data where a | test:tests/test_preconditioning.py::test_robust_normalizes_log_iqr_and_ignores_zeros | backed | keep |
| U35-C015 | S | few extreme designs would dominate; `None` keeps the pure power law. Note: Only invertibility with scaler=None is tested; no test asserts log_offset_=0, log_scale_=1 (pure power law), only the docstring says it | test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift | broader than its backing | narrow |
| U35-C016 | S | works if it is affine per column. The reason to scale is the temperature of the next page: it is | test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift | backed | keep |
| U35-C017 | M | quoted in inverse log-spread, so equal log-spread makes one temperature mean the same for every Note: No lemma step or test shows the temperature is in inverse log-spread units or that equal log-spread equalizes its meaning across columns | none | unbacked | to the driver |
| U35-C018 | S | An entry at exactly `-shift` maps to metric 0, and the scaler ignores it. | test:tests/test_preconditioning.py::test_zero_after_shift_maps_to_zero_and_inverts_to_minus_shift test:tests/test_preconditioning.py::test_zeros_map_to_zero_and_invert | backed | keep |
| U35-C019 | S | An entry at exactly `-shift` maps to metric 0, and the scaler ignores it. The estimator tolerates | test:tests/test_estimator.py::test_zero_metric_row | backed | keep |
| U35-C020 | S | such a row has V = 0 and no support weight, | test:tests/test_estimator.py::test_zero_metric_row | backed | keep |
| U35-C021 | S | and its chart coordinates are `nan`. | test:tests/test_estimator.py::test_zero_metric_row test:tests/test_coordinates.py::test_minus_inf_rows | backed | keep |
| U35-C022 | M | For a smaller-is-better attribute a raw zero is the best value, so mapping it to metric 0 is | test:tests/test_preconditioning.py::test_zeros_map_to_zero_and_invert | backed | keep |
| U35-C023 | S | to evaluate before conditioning, so the fitted scale describes feasible designs only. | definition | backed | keep |
| U35-C024 | P | None proves a conditioning right; they show whether the story is sensible. | reading | backed | keep |
| U35-C025 | S | After `"standard"` scaling, `np.log(M).std(axis=0)` is one in every finite column. | test:tests/test_preconditioning.py::test_unit_log_standard_deviation func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner | backed | keep |
| U35-C026 | S | `inverse_transform(transform(X))` returns `X`; the conditioning is exactly invertible. | test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift test:tests/test_preconditioning.py::test_zeros_map_to_zero_and_invert | backed | keep |
| U35-C027 | M | The pulled-back exponent on a raw attribute is `w_j * alpha_j`. | lemma:L9.5 | backed | keep |
| U35-C028 | P | contending set moves, the finding depends on the conditioning, and should be reported that way. | reading | backed | keep |
| U35-C029 | S | `exponents_orig`, `log_const` and `shift`. The surface is again a monomial, now in the raw | test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples | backed | keep |
| U35-C030 | M | attributes: a negative exponent marks a smaller-is-better attribute. | lemma:L9.5 test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples | backed | keep |
| U35-C031 | M | to get log V for raw rows. The function needs a | lemma:L9.5 test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples | backed | keep |
| U35-C032 | S | single-term fit; a multi-term fit is not a monomial in the attributes. Note: Not-a-monomial for K>1 is the posynomial sum (L10); the code raises ValueError for n_terms != 1 but no test asserts it (test_pullback_errors covers width and unfitted only) | lemma:L10.1 func:src/hyperbolic_trade_space/preconditioning.py::frontier_in_original_units | broader than its backing | narrow |

### U36: docs user-guide/fitting (`docs/user-guide/fitting.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U36-C001 | S | `HyperbolicTradeSpace` fits the frontier model to conditioned metrics. | test:tests/test_estimator.py::test_recovery_tau_inf test:tests/test_estimator.py::test_recovery_tau_1e3 | backed | routed to P6 |
| U36-C002 | S | At one term it solves a convex | lemma:L4 | backed | routed to P6 |
| U36-C003 | S | problem and returns the minimizer. It follows the scikit-learn decomposition family: `fit`, | lemma:L4 test:tests/test_solvers.py::test_slsqp_agrees_with_lp test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator | backed | keep |
| U36-C004 | S | `score_samples`, and no `predict`. Parameters are stored as given | test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score test:tests/test_sklearn_compat.py::test_init_stores_parameters_verbatim test:tests/test_estimator.py::test_invalid_params_raise_in_fit_not_init | backed | keep |
| U36-C005 | S | - `exponents_`: shape `(n_terms, d)`, each row on the simplex. | test:tests/test_estimator.py::test_fit_invariants test:tests/test_estimator.py::test_k_terms_round_trip_and_scores | backed | keep |
| U36-C006 | S | - `frac_above_`: the fraction of designs beyond V = 1. | test:tests/test_estimator.py::test_fit_invariants test:tests/test_tuning.py::test_selected_temperature_hits_target | backed | routed to P6 |
| U36-C007 | S | - `n_eff_`: how many designs carry the fit. | test:tests/test_estimator.py::test_k_terms_attributes_conventions test:tests/test_tuning.py::test_tau_sweep_is_monotone_from_half_toward_zero | backed | keep |
| U36-C008 | S | `objective_` is what the solver minimized, the soft maximum at one | test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized test:tests/test_estimator.py::test_fit_invariants test:tests/test_soft_fit.py::test_r4_the_soft_fit_serves_its_model | backed | routed to P6 |
| U36-C009 | S | term and the mean slack at several, so it is not comparable across numbers of terms. | test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized file:work-packages/interface-contract.md | backed | keep |
| U36-C010 | S | `mean_slack_` is the mean gap between facet and design, defined at every number of terms; compare Note: Gap to the dominant facet holds for the label fit; at finite term_temperature and K>1 it is the slack of the soft surface Phi_K; 'compare at a fixed temperature' is docstring only, no test. | test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized test:tests/test_estimator.py::test_attributes_exist_for_every_k_and_k1_numbers_are_unchanged | broader than its backing | routed to P6 |
| U36-C011 | S | - `termination_` and `conditioning_`: how the fit stopped and how well its exponents are identified | test:tests/test_estimator.py::test_termination_record_for_k_terms test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue test:tests/test_estimator.py::test_conditioning_drops_for_nearly_collinear_metrics | backed | keep |
| U36-C012 | S | The chart's basis, offsets and support weights are `basis_`, `log_offset_` and `support_weights_`. | test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples test:tests/test_estimator.py::test_fit_invariants | backed | keep |
| U36-C013 | S | `min_exponent` (a floor on every exponent) at 0 to | glossary:contending-set test:tests/test_estimator.py::test_fit_invariants | backed | keep |
| U36-C014 | S | `temperature` is tau, how hard the maximum is. Infinity (`np.inf`) is the exact maximum, a linear | glossary:temperature glossary:supporting-envelope lemma:L5.24 | backed | routed to P6 |
| U36-C015 | M | program giving the supporting envelope: no design lies above it. | lemma:L1 lemma:L5.15 lemma:L5.24 glossary:supporting-envelope test:tests/test_estimator.py::test_fit_invariants test:tests/test_solvers.py::test_lp_hand_built | backed | routed to P6 |
| U36-C016 | M | A finite tau gives the fitted | glossary:fitted-reference-surface test:tests/test_estimator.py::test_fit_invariants | backed | routed to P6 |
| U36-C017 | M | reference surface with a band of near-frontier designs of width 1/tau, and a few designs beyond Note: Band 1/tau is the tension_report/facet_share_ convention (pinned), not a bound (L5.16 gives log N / tau); 'a few designs beyond V=1' only pinned as 0<frac<0.5, and frac is about 1/2 at tau<3. | test:tests/test_tensions.py::test_band_default_and_report_fields test:tests/test_estimator.py::test_fit_invariants glossary:fitted-reference-surface | broader than its backing | routed to P6 |
| U36-C018 | M | V = 1. Tau is in units of inverse log-spread, so it depends on the conditioning. Note: Units claim (tau scales log-scores; scaling u by c equals tau->c*tau) is in docstrings only; no lemma step or test; one-line derivation, candidate to back. | none | unbacked | routed to P6 |
| U36-C019 | S | `select_temperature` picks tau so that a target fraction of designs lies above V = 1: | test:tests/test_tuning.py::test_selected_temperature_hits_target | backed | routed to P6 |
| U36-C020 | R | This synthetic table puts 30 percent of its rows on the planted frontier, hence the target 0.35; | gen:src/hyperbolic_trade_space/datasets.py::make_frontier_data test:tests/test_datasets.py::test_frontier_info_and_planting | backed | keep |
| U36-C021 | P | for real data the default 0.10 is a common start. Note: Default 0.10 pinned and used in the case studies; 'a common start' (field practice) is unsourced and not worded as the author's own practice. | test:tests/test_tuning.py::test_passes_estimator_params_and_default_target | broader than its backing | narrow |
| U36-C022 | M | `frac_above_` is not monotone in tau. Note: 'Not monotone' (below tau about 3) is only a comment in tests/test_tuning.py::test_tau_sweep_is_monotone_from_half_toward_zero, which asserts monotone for tau>=3 on one table; the non-monotone half is not asserted. | none | unbacked | routed to P6 |
| U36-C023 | S | A `ValueError` says when `bounds` misses the target. | test:tests/test_tuning.py::test_not_bracketed_raises | backed | keep |
| U36-C024 | M | One term is one flat facet in log space with constant elasticities. | lemma:L7.5 lemma:L10.9 glossary:facet glossary:elasticity | backed | routed to P6 |
| U36-C025 | S | Fitting alternates weights from the current model with a refit, from several seeded starts | lemma:L15 test:tests/test_solvers.py::test_terms_monotone_history_and_stops test:tests/test_estimator.py::test_k_terms_zero_rows_and_determinism | backed | keep |
| U36-C026 | S | (`n_restarts`, default 5) keeping the best. `assign_facets(X)` reads which facet Note: Default 5 and assign_facets == facet_ pinned; 'keeping the best' (min objective over restarts) is in solve_terms but no test asserts it. | test:tests/test_estimator.py::test_n_restarts_default_and_validation test:tests/test_estimator.py::test_k_terms_round_trip_and_scores | broader than its backing | routed to P6 |
| U36-C027 | S | - `term_temperature` (kappa, default infinity) sets the temperature of the soft weights: finite, | glossary:term-temperature test:tests/test_soft_fit.py::test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone file:work-packages/interface-contract.md | backed | routed to P6 |
| U36-C028 | S | every design weighs every term; infinity, one label per design. Reported facets are the dominant | glossary:term-temperature test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis test:tests/test_soft_fit.py::test_r3_the_limit_kappa_to_infinity_is_the_label_fit file:work-packages/interface-contract.md | backed | routed to P6 |
| U36-C029 | S | - `penalty="reweighted_l1"` with `alpha` pushes small exponents to exact zero, at finite temperature | test:tests/test_estimator.py::test_penalty_gives_exact_zero_exponents_at_the_estimator test:tests/test_solvers.py::test_reweighted_l1_gives_exact_zeros_on_planted_sparse_facet test:tests/test_solvers.py::test_penalty_validation_and_alpha_zero_exact | backed | routed to P6 |
| U36-C030 | S | - `facet_step` is `"support"` (default) or `"tangent"`, which is not monotone and carries no Note: Default support and tangent -> not_applicable (no local-optimality status) pinned; 'is not monotone' is stated as fact but only 'best iterate kept' is tested (comment); should read 'has no monotonicity guarantee'. | test:tests/test_estimator.py::test_facet_step_validated_and_inert_at_k1 test:tests/test_solvers.py::test_not_applicable_statuses | broader than its backing | routed to P6 |
| U36-C031 | S | `facet_` gives each training row's dominant facet; `coefficients_` and `facet_share_` the facets' | test:tests/test_estimator.py::test_k_terms_attributes_conventions test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis | backed | routed to P6 |
| U36-C032 | S | At one term `facet_` is all zeros and `facet_share_` is `[1.0]`. | test:tests/test_estimator.py::test_attributes_exist_for_every_k_and_k1_numbers_are_unchanged file:work-packages/interface-contract.md | backed | routed to P6 |
| U36-C033 | P | variation between restarts. Resample: a facet whose exponents change between bootstrap resamples Note: Rule of thumb (restart variation; a facet that changes under resampling is a splinter and K too large) has no source or test and is not worded as the author's judgement; only the K=4 run illustrates it (cold-read note is anecdotal). | none | unbacked | routed to P6 |
| U36-C034 | R | The mean slack falls from 0.855 at K = 1 to 0.692, 0.664 and 0.658: the third term is the last that Note: Values 0.855, 0.692, 0.664, 0.658 reproduced by running the page's block (K=1..4, tau=50) but no test or generator file pins them; 'third term is the last that pays' is a reading. | none | unbacked | routed to P6 |
| U36-C035 | R | Over the four resamples the smallest exponent stays within 0.07 to 0.08 at K = 3 and ranges from Note: K=3 smallest exponent 0.08 0.08 0.07 0.07 reproduced by running the page's block; not pinned by any test. | none | unbacked | drop |
| U36-C036 | R | 0.00 to 0.07 at K = 4: the fourth facet changes with the sample. Note: K=4 smallest exponent 0.00 0.03 0.00 0.07 reproduced by running the block; not pinned by any test. | none | unbacked | routed to P6 |
| U36-C037 | M | With several terms the facets are not Note: General claim about every K>1 fit rests on instances (K=2 table seed 777 floor above 0.10; cubesat frac>0.25); no lemma; estimator docstring even says each facet is a supporting hyperplane over all rows. | test:tests/test_tuning.py::test_several_terms_unreachable_target_says_what_to_try | broader than its backing | routed to P6 |
| U36-C038 | R | supporting planes, so `frac_above_` levels off above zero as tau grows (about 0.30 on the table of Note: Levels off above zero pinned for the K=2 table (not bracketed at 0.10, floor target reachable); 'about 0.30' reproduced by me (0.30 at tau=1e3, 1e4) but not pinned by any test. | test:tests/test_tuning.py::test_several_terms_unreachable_target_says_what_to_try | broader than its backing | routed to P6 |
| U36-C039 | S | `make_frontier_data(300, 4, n_terms=2, random_state=777)`) and the default target 0.10 raises "not | test:tests/test_tuning.py::test_several_terms_unreachable_target_says_what_to_try | backed | keep |
| U36-C040 | S | bracketed". The message names a target, a fixed `temperature`, and wider `bounds`. Select | test:tests/test_tuning.py::test_several_terms_unreachable_target_says_what_to_try | backed | routed to P6 |
| U36-C041 | S | `tension_report` takes its band from the temperature, 1/tau. A facet with fewer than | test:tests/test_tensions.py::test_band_default_and_report_fields | backed | routed to P6 |
| U36-C042 | S | `min_near_frontier` designs in the band raises, and the message names the `band`, and the matching | test:tests/test_tensions.py::test_first_report_at_several_terms_names_a_workable_band test:tests/test_tensions.py::test_too_few_near_frontier_raises | backed | routed to P6 |
| U36-C043 | R | `temperature`, that holds enough. On that table at tau = 50 the band 0.02 holds five designs of Note: No generator or test pins 'five designs at band 0.02'; the test only checks the named band holds >=10 rows | none | unbacked | routed to P6 |
| U36-C044 | R | facet 0 and 0.025 holds ten. Note: No generator or test pins 'ten designs at 0.025' for facet 0; unpinned number | none | unbacked | routed to P6 |
| U36-C045 | M | each facet is a straight line in log space, and the frontier is their envelope. | lemma:L10.3 | backed | routed to P6 |
| U36-C046 | S | Kernel expansions that stay inside geometric programming are documented, not built. | definition | backed | routed to P6 |
| U36-C047 | S | `make_frontier_data` plants a frontier, with `n_terms=K` for K facets; `make_configured_frontier_data` | test:tests/test_datasets.py::test_configured | backed | routed to P6 |
| U36-C048 | S | also returns configuration variables. Both are seeded and used throughout these pages. | test:tests/test_datasets.py::test_configured | backed | keep |

### U37: docs user-guide/tensions (`docs/user-guide/tensions.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U37-C001 | S | returns a frozen `TensionReport` that says which metrics contend and | test:tests/test_tensions.py::test_deterministic_frozen_and_validation test:tests/test_tensions.py::test_contending_set_recovers_planted_support | backed | keep |
| U37-C002 | M | The model looks for the binding constraint, so the report describes a tension, where Note: no lemma step or test says the fit finds the binding constraint or contrasts it with PCA; module docstring only | none | unbacked | to the driver |
| U37-C003 | S | `plot_tensions` draws the report as a heatmap: | test:tests/test_plotting.py::test_plot_tensions_with_real_report test:tests/test_plotting.py::test_plot_tensions_with_stand_in_report | backed | keep |
| U37-C004 | R | all three off-diagonal cells are negative, and all three metrics are outlined as contending. Note: no generator/test pins the signs of this figure's off-diagonals or outlines (tests only check images exist/differ; -0.38..-0.62 only in WP8a review note) | none | unbacked | drop |
| U37-C005 | S | `contending_set` holds the metrics with positive exponent in the exact-maximum fit (tau = infinity, | test:tests/test_tensions.py::test_contending_set_recovers_planted_support test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact | backed | keep |
| U37-C006 | S | `n_lemma` is its size and `lemma_name` names it: monolemma, dilemma, | test:tests/test_tensions.py::test_contending_set_recovers_planted_support test:tests/test_tensions.py::test_d1_trivial_report | backed | keep |
| U37-C007 | M | The set is found, not assumed: a facet of the achievable region on which | glossary:n-lemma test:tests/test_tensions.py::test_contending_set_recovers_planted_support | backed | keep |
| U37-C008 | S | The report solves the tau = infinity program itself, independent of the | test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact | backed | keep |
| U37-C009 | M | `min_exponent` must be 0 for this reading, because a positive floor masks the Note: no lemma step; only the warning is tested (software), and the LP being recomputed with min_exponent=0; 'masks the sparsity' (a floor forces all exponents >= floor, tests/test_estimator.py::test_fit_invariants checks w.min() >= min_exponent) is a small step not tagged | none | unbacked | to the driver |
| U37-C010 | S | the report warns when the estimator was fitted with a floor. | test:tests/test_tensions.py::test_warns_when_min_exponent_positive test:tests/test_tensions.py::test_no_warning_when_min_exponent_zero | backed | keep |
| U37-C011 | M | At the working temperature the exponents are smoothed, so a small one means weak participation, not Note: pinned only on one planted trilemma example (free-metric weights < half the members'); no lemma that smoothing gives non-membership in general | test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact | broader than its backing | to the driver |
| U37-C012 | S | `participating` marks metrics whose exponent exceeds the participation threshold | test:tests/test_tensions.py::test_exponents_and_elasticities_consistent test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact glossary:participation-threshold | backed | keep |
| U37-C013 | S | (`threshold`, default 1e-3); an exponent at or below 1e-12 is numerically zero. Note: default 1e-3 only exercised via nan rows, not asserted as the default; the 1e-12 numerically-zero cutoff is in the glossary only, no test | glossary:numerically-zero test:tests/test_tensions.py::test_exponents_and_elasticities_consistent | broader than its backing | narrow |
| U37-C014 | M | is the elasticity along the surface: the percentage change of metric j per percentage change of | lemma:L7.5 glossary:elasticity test:tests/test_tensions.py::test_exponents_and_elasticities_consistent | backed | keep |
| U37-C015 | M | metric k, constant on a facet and `nan` | lemma:L7.5 test:tests/test_tensions.py::test_exponents_and_elasticities_consistent | backed | keep |
| U37-C016 | S | where metric j does not participate. It | test:tests/test_tensions.py::test_exponents_and_elasticities_consistent | backed | keep |
| U37-C017 | M | describes a feature of the fitted model, not a causal exchange. | definition glossary:elasticity | backed | keep |
| U37-C018 | S | For designs with absolute log V below `band` (by default 1/tau, or 0.1 at infinite tau), | test:tests/test_tensions.py::test_band_default_and_report_fields test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions | backed | keep |
| U37-C019 | S | `association` is the Pearson or Spearman correlation of the log-metrics: negative is traded, positive | test:tests/test_tensions.py::test_association_signs_aligned_and_traded | backed | keep |
| U37-C020 | M | Near the surface the weighted sum of log-metrics is almost constant, so a binding | lemma:L1 | backed | keep |
| U37-C021 | M | constraint produces negative association even where no designer traded the metrics (`closure_note` Note: pinned on one planted example and the closure_note text; no lemma that a binding constraint forces negative association in general | test:tests/test_tensions.py::test_closure_induces_negative_association_without_trade | broader than its backing | to the driver |
| U37-C022 | S | Three fields describe the spread of the near-frontier designs along the surface: | test:tests/test_tensions.py::test_first_direction_recovers_planted_spread | backed | keep |
| U37-C023 | S | `tension_directions`: the principal directions of the near-frontier chart coordinates. | test:tests/test_tensions.py::test_first_direction_recovers_planted_spread | backed | keep |
| U37-C024 | S | `tension_loadings`: the same directions as loadings on the log-metrics. | test:tests/test_tensions.py::test_first_direction_recovers_planted_spread | backed | keep |
| U37-C025 | S | `explained_spread`: the share of variance along each. | test:tests/test_tensions.py::test_first_direction_recovers_planted_spread | backed | keep |
| U37-C026 | S | They equal `orient_by_pca` on the same rows. | test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions | backed | keep |
| U37-C027 | M | along the surface is the set of trade-offs the designs exercised. Note: interpretive: pinned only for a planted spread; 'the trade-offs the designs exercised' is a reading, no lemma | test:tests/test_tensions.py::test_first_direction_recovers_planted_spread | broader than its backing | to the driver |
| U37-C028 | S | At K > 1 the function returns a list of K reports, one per facet, each on the rows that facet | test:tests/test_tensions.py::test_k3_reports_one_per_facet_recover_planted_supports test:tests/test_tensions.py::test_k1_is_a_single_report_and_facet_error_names_facet | backed | keep |
| U37-C029 | S | dominates. A facet with fewer than `min_near_frontier` (default 10) near-frontier rows raises | test:tests/test_tensions.py::test_k3_reports_one_per_facet_recover_planted_supports test:tests/test_tensions.py::test_k1_is_a_single_report_and_facet_error_names_facet test:tests/test_tensions.py::test_too_few_near_frontier_raises | backed | keep |
| U37-C030 | M | Each report describes one facet and so one tension | definition glossary:n-lemma test:tests/test_tensions.py::test_k3_reports_one_per_facet_recover_planted_supports | backed | keep |
| U37-C031 | M | depends on the band, and is a statement about | test:tests/test_tensions.py::test_too_few_near_frontier_raises test:tests/test_tensions.py::test_band_default_and_report_fields | backed | keep |
| U37-C032 | M | the sampled table: tensions the sampling never exercised cannot appear. | definition | backed | keep |

### U38: docs user-guide/chart (`docs/user-guide/chart.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U38-C001 | M | One is log V, the energy differential (level offset) | registered:C004 lemma:L1.7 glossary:energy-differential glossary:level-offset | backed | keep |
| U38-C002 | M | to the fitted reference surface: negative inside, positive beyond. | registered:C004 lemma:L1.7 | backed | keep |
| U38-C003 | M | say where along the surface the design sits, | lemma:L8.6 lemma:L8.14 | backed | keep |
| U38-C004 | M | Together they are a reversible rewriting of the metrics. | registered:C010 lemma:L8.14 test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples | backed | keep |
| U38-C005 | S | `transform` returns the chart, `inverse_transform` inverts it, and `score_samples` is log V alone. | test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples | backed | keep |
| U38-C006 | S | row with a zero metric has `nan` coordinates and no inverse. | test:tests/test_estimator.py::test_zero_metric_row test:tests/test_coordinates.py::test_minus_inf_rows | backed | keep |
| U38-C007 | S | With two metrics the chart is the log plane itself: Note: the chart (Z, log V) is a linear re-coordinatization of the log plane (log V = w.u - beta), not the log plane itself; the plot_log_plane axes are the log metrics | lemma:L8.14 test:tests/test_plotting.py::test_log_plane_draws_frontier_line_in_black_and_band_in_grey | broader than its backing | narrow |
| U38-C008 | M | V is a factor of improvement: doubling every metric doubles V. | registered:C002 lemma:L1.5 | backed | keep |
| U38-C009 | S | `project(X)` returns the design moved onto V = 1 by scaling all its metrics together. | test:tests/test_estimator.py::test_project_and_improvement_factors_land_on_frontier lemma:L1.6 lemma:L7.9 | backed | keep |
| U38-C010 | S | `improvement_factors(X)` gives, per metric, the factor on that metric alone that reaches V = 1 | test:tests/test_estimator.py::test_project_and_improvement_factors_land_on_frontier lemma:L7.7 func:src/hyperbolic_trade_space/estimator.py::improvement_factors | backed | keep |
| U38-C011 | S | (`inf` where the exponent is numerically zero). | test:tests/test_estimator.py::test_improvement_factors_inf_for_numerically_zero_exponent_without_warning test:tests/test_estimator.py::test_improvement_factor_inf_at_zero_exponent | backed | keep |
| U38-C012 | M | At a finite temperature some training designs lie beyond V = 1 by construction Note: L5.15 only gives LME <= max (so the top design has V >= 1); strictly 'some beyond' is asserted only on planted data (0 < frac_above_ < 0.5), not proved in general | lemma:L5.15 lemma:L5.16 test:tests/test_estimator.py::test_fit_invariants | broader than its backing | to the driver |
| U38-C013 | M | meaningful relative to the band of width 1/tau. Note: no test pins the band width 1/tau as the right reading scale (plotting _band default is a convention; L5.16 gives log n/tau); advice sentence | none | unbacked | to the driver |
| U38-C014 | M | A score beyond the surface is not a verdict that the design is | definition | backed | keep |
| U38-C015 | S | For a multi-term fit, log V is the soft maximum over facets | test:tests/test_matches_derivation.py::test_L10_phi_k_bounds_shift_and_limit_at_numeric_instance test:tests/test_estimator.py::test_k_terms_round_trip_and_scores lemma:L10.15 lemma:L10.16 | backed | keep |
| U38-C016 | S | For a multi-term fit, log V is the soft maximum over facets, and `improvement_factors` uses each | test:tests/test_estimator.py::test_k_terms_improvement_factors_use_assigned_facet test:tests/test_estimator.py::test_k_terms_round_trip_and_scores | backed | keep |
| U38-C017 | S | `knn_gap_scores(Z, k=5)`: mean distance to the k nearest neighbours, normalized by its median. | func:src/hyperbolic_trade_space/gaps.py::knn_gap_scores test:tests/test_gaps.py::test_knn_flags_isolated_point | backed | keep |
| U38-C018 | S | `find_holes(Z, resolution=50, threshold=2.0)`: grid points inside the convex hull of Z that sit far | func:src/hyperbolic_trade_space/gaps.py::find_holes test:tests/test_gaps.py::test_find_holes_restricts_to_hull test:tests/test_gaps.py::test_find_holes_2d_planted_disc | backed | keep |
| U38-C019 | S | supports `d - 1` of 1, 2 or 3. | test:tests/test_gaps.py::test_find_holes_3d_runs_and_other_dims_raise test:tests/test_gaps.py::test_find_holes_1d_planted_gap | backed | keep |
| U38-C020 | S | `frontier_targets(Z_points, estimator, preconditioner=None)`: sets log V = 0 at given positions and | test:tests/test_gaps.py::test_frontier_targets_on_frontier_and_round_trip | backed | keep |
| U38-C021 | S | maps back to metrics and, with a preconditioner, to attributes. | test:tests/test_gaps.py::test_frontier_targets_with_real_preconditioner test:tests/test_gaps.py::test_frontier_targets_with_preconditioner_stand_in test:tests/test_gaps.py::test_frontier_targets_on_frontier_and_round_trip | backed | keep |
| U38-C022 | S | `orient_by_pca(Z, mask=None)`: rotates to the principal axes of the masked rows. | test:tests/test_gaps.py::test_orient_by_pca_rotation_and_sign test:tests/test_gaps.py::test_orient_by_pca_mask_uses_only_masked_rows | backed | keep |
| U38-C023 | R | Figure 4. One facet in the log plane: the line is V = 1, and the band below it has width 1/tau. Note: the line being V=1 (w.u=beta) and a grey band are tested; band width 1/tau (plotting _band default) is not pinned by any test | test:tests/test_plotting.py::test_log_plane_draws_frontier_line_in_black_and_band_in_grey test:tests/test_site.py::test_each_figure_is_produced_by_the_code_shown_above_it gen:scripts/build_figures.py::build_page | broader than its backing | narrow |
| U38-C024 | R | Figure 5. The chart with holes: the red points are grid positions far from every design, candidates for white space. | test:tests/test_gaps.py::test_find_holes_2d_planted_disc test:tests/test_site.py::test_each_figure_is_produced_by_the_code_shown_above_it gen:scripts/build_figures.py::build_page func:src/hyperbolic_trade_space/plotting.py::plot_frontier_coordinates | backed | keep |
| U38-C025 | M | The score cannot tell these apart | definition | backed | keep |
| U38-C026 | M | The surface is also log-convex, so structure that is not log-convex is invisible to it. Note: L10.7 gives the model as a posynomial in m; log-convexity of the surface in log metrics and the 'invisible' consequence are not a tagged step | lemma:L10.7 | broader than its backing | to the driver |
| U38-C027 | S | `plot_log_plane`: two metrics, the data, the frontier and its band. | test:tests/test_plotting.py::test_log_plane_draws_frontier_line_in_black_and_band_in_grey | backed | keep |
| U38-C028 | S | `plot_frontier_surface_3d`: three metrics, the frontier surface. | test:tests/test_plotting.py::test_surface_3d_returns_3d_axes_and_validates | backed | keep |
| U38-C029 | S | `plot_frontier_coordinates`: the chart, with optional holes and targets. | test:tests/test_plotting.py::test_frontier_coordinates_one_and_two_coordinates_and_overlays | backed | keep |
| U38-C030 | S | `plot_v_by_variable`: log V against a configuration variable. | test:tests/test_plotting.py::test_v_by_variable_numeric_and_categorical_and_existing_ax | backed | keep |
| U38-C031 | S | `plot_tensions`: the tension report as a heatmap. | test:tests/test_plotting.py::test_plot_tensions_with_stand_in_report | backed | keep |
| U38-C032 | S | Each accepts an optional `ax` and returns a matplotlib `Axes`; nothing calls `plt.show()`. Note: ax/Axes return tested for several plots; 'nothing calls plt.show()' is stated only in the module docstring (no test); plot_tensions given a list returns a list of Axes | test:tests/test_plotting.py::test_surface_3d_returns_3d_axes_and_validates test:tests/test_plotting.py::test_v_by_variable_numeric_and_categorical_and_existing_ax func:src/hyperbolic_trade_space/plotting.py::plot_log_plane | broader than its backing | narrow |
| U38-C033 | S | one colour vocabulary, declared as module constants (`FRONTIER_COLOR`, `BAND_COLOR`, `HOLE_COLOR`, | test:tests/test_plotting.py::test_log_plane_draws_frontier_line_in_black_and_band_in_grey test:tests/test_plotting.py::test_plot_tensions_with_stand_in_report | backed | keep |
| U38-C034 | S | For a multi-term fit the plots draw every facet Note: plot_log_plane draws a facet only where it has weight on both metrics (tested), so not literally every facet | test:tests/test_plotting.py::test_log_plane_k3_draws_envelope_and_facet_legend test:tests/test_plotting.py::test_surface_k3_and_coordinates_facet_colouring test:tests/test_plotting.py::test_log_plane_k3_draws_facet_only_where_it_has_weight_on_both_metrics | broader than its backing | narrow |
| U38-C035 | S | gives a per-row label to pass as `color=`. | test:tests/test_plotting.py::test_surface_k3_and_coordinates_facet_colouring func:src/hyperbolic_trade_space/plotting.py::facet_labels | backed | keep |

### U39: docs user-guide/prediction (`docs/user-guide/prediction.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U39-C001 | S | where would a configuration without measurements fall? It composes two fits. | func:src/hyperbolic_trade_space/predictive.py::TradeSpaceRegressor test:tests/test_predictive.py::test_clones_leave_parameters_untouched | backed | keep |
| U39-C002 | S | Y_metrics)` fits a clone of `trade_space` on the metrics, then fits a clone of | test:tests/test_predictive.py::test_clones_leave_parameters_untouched func:src/hyperbolic_trade_space/predictive.py::TradeSpaceRegressor.fit | backed | keep |
| U39-C003 | S | - `predict(X_config)`: metrics, through the inverse chart. | test:tests/test_predictive.py::test_recovers_planted_coordinates | backed | keep |
| U39-C004 | S | - `predict_coordinates(X_config)`: the pair `(Z, log_v)`. | test:tests/test_predictive.py::test_recovers_planted_coordinates func:src/hyperbolic_trade_space/predictive.py::TradeSpaceRegressor | backed | keep |
| U39-C005 | S | - `predict_novelty(X_config)`: V - 1, positive where the design is predicted beyond the surface. | test:tests/test_predictive.py::test_novelty_beyond_the_soft_frontier | backed | keep |
| U39-C006 | S | the regressor's `return_std` propagated by the delta method; raises | test:tests/test_predictive.py::test_predict_std_plumbing_with_gaussian_process test:tests/test_predictive.py::test_predict_std_absent_without_return_std | backed | keep |
| U39-C007 | S | - `score`: R-squared in coordinate space, not in metric units. | test:tests/test_predictive.py::test_score_is_coordinate_space_r2_and_order_independent | backed | keep |
| U39-C008 | M | Coordinates, not metrics, are the regression target, so the surrogate's error carries into the | test:tests/test_predictive.py::test_novelty_beyond_the_soft_frontier func:src/hyperbolic_trade_space/predictive.py::TradeSpaceRegressor.fit | backed | keep |
| U39-C009 | S | novelty prediction. A one-dimensional `y` is accepted for a single metric. `trade_space` may be a | test:tests/test_predictive.py::test_single_metric_accepts_1d_y test:tests/test_predictive.py::test_trade_space_can_be_a_pipeline_and_regressor_a_pipeline | backed | keep |
| U39-C010 | S | `Pipeline` ending in a `HyperbolicTradeSpace`, such as a preconditioner followed by the estimator. | test:tests/test_predictive.py::test_trade_space_can_be_a_pipeline_and_regressor_a_pipeline | backed | keep |
| U39-C011 | M | A predicted position inherits the surrogate's error and extrapolation risk, and is conditional on | test:tests/test_predictive.py::test_predict_std_plumbing_with_gaussian_process test:tests/test_predictive.py::test_recovers_planted_coordinates | backed | keep |
| U39-C012 | S | evaluation to run, to be checked, not a result. The regressor declares `positive_only` targets and | test:tests/test_sklearn_compat.py::test_regressor_tags | backed | keep |
| U39-S01 | S | raises `ValueError` on negative `y`. | test:tests/test_predictive.py::test_inputs_validated test:tests/test_sklearn_compat.py::test_regressor_tags | backed | keep |

### U40: docs user-guide/termination (`docs/user-guide/termination.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U40-C001 | S | Every fit records how it stopped. | test:tests/test_estimator.py::test_termination_record_for_k_terms test:tests/test_estimator.py::test_termination_not_applicable_cases_do_not_warn test:tests/test_solvers.py::test_margin_and_radius_are_nan_at_one_term_not_infinite | backed | keep |
| U40-C002 | M | At one term the fit is a convex program and its answer is the | lemma:L4 lemma:L12.13 test:tests/test_solvers.py::test_terms_k1_equals_slsqp_and_degenerate | backed | keep |
| U40-C003 | S | With several terms it alternates between weights from the current model and refitting each | test:tests/test_solvers.py::test_terms_monotone_history_and_stops test:tests/test_soft_fit.py::test_r1_the_soft_objective_never_rises_across_the_history | backed | keep |
| U40-C004 | S | no step made the mean slack worse (`mean_slack_`, defined at every number of terms). | test:tests/test_solvers.py::test_terms_monotone_history_and_stops test:tests/test_soft_fit.py::test_r1_the_soft_objective_never_rises_across_the_history test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized lemma:L15.16 | backed | keep |
| U40-C005 | M | Numerical stationarity: no first-order improvement is left. | lemma:L12.21 lemma:L12.23 | backed | keep |
| U40-C006 | M | The facet gap G_k measures what | lemma:L12.23 | backed | keep |
| U40-C007 | M | if no design sits exactly on a seam between facets, small changes | lemma:L13.7 lemma:L13.12 test:tests/test_solvers.py::test_margin_lemma_perturbations_inside_the_radius_keep_labels | backed | keep |
| U40-C008 | M | to the facets cannot change which facet dominates which design, so the fixed assignment is optimal. Note: L14 Prop 3 gives a local minimizer of the full objective, under exact facet optima, no penalty, step-B offsets (beta=J_tau); 'the fixed assignment is optimal' omits local and the hypotheses (lemma not covering a tolerance eps_kkt) | lemma:L14.16 lemma:L14.18 | broader than its backing | to the driver |
| U40-C009 | M | is the perturbation provably leaving every facet unchanged. | lemma:L13.7 lemma:L13.11 test:tests/test_solvers.py::test_margin_lemma_perturbations_inside_the_radius_keep_labels | backed | keep |
| U40-C010 | S | At infinite temperature this happens when a frontier row lies on two facet planes or two | test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets test:tests/test_solvers.py::test_r1_planted_certificates | backed | keep |
| U40-C011 | S | - `stationary_without_margin`: the same, with margin at most `eps_feas` or an empty facet. Levels 1 Note: margin<=eps_feas branch pinned (status stationary_without_margin, seed 1); the empty-facet branch is pinned only as 'status != certified' with n_empty==1; code in _termination | test:tests/test_estimator.py::test_termination_record_for_k_terms test:tests/test_solvers.py::test_r1_planted_certificates test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets | broader than its backing | narrow |
| U40-C012 | S | - `guard_stop`: an iteration raised the mean slack by more than `guard_tol`. Not converged. | test:tests/test_solvers.py::test_guard_stop_returns_the_consistent_previous_state test:tests/test_estimator.py::test_convergence_warning_keyed_to_guard_stop | backed | keep |
| U40-C013 | S | - `iteration_cap`: `max_iter` reached. Not converged. | test:tests/test_solvers.py::test_iteration_cap_status test:tests/test_estimator.py::test_convergence_warning_keyed_to_iteration_cap | backed | keep |
| U40-C014 | S | - `not_applicable`: one term, `facet_step="tangent"`, a `penalty`, one metric, fewer designs than | test:tests/test_solvers.py::test_not_applicable_statuses test:tests/test_soft_fit.py::test_r7_a_soft_fit_at_infinite_tau_is_not_applicable test:tests/test_soft_fit.py::test_r7_a_soft_fit_with_a_penalty_is_not_applicable test:tests/test_estimator.py::test_termination_not_applicable_cases_do_not_warn | backed | keep |
| U40-C015 | S | facets, or a soft fit at infinite temperature. Not a failure. | test:tests/test_estimator.py::test_termination_not_applicable_cases_do_not_warn | backed | keep |
| U40-C016 | S | `fit` warns (a `ConvergenceWarning` naming the status and the largest gap) for `uncertified`, Note: warning naming status and 'max facet gap' pinned for iteration_cap and guard_stop; no test produces uncertified and its warning (only _WARN_STATUSES in estimator.py) | test:tests/test_estimator.py::test_convergence_warning_keyed_to_iteration_cap test:tests/test_estimator.py::test_convergence_warning_keyed_to_guard_stop | broader than its backing | narrow |
| U40-C017 | S | A soft fit (finite `term_temperature`) has no assignment, so no margin: | test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified | backed | keep |
| U40-C018 | S | - `certified`: weighted gaps within `eps_kkt` and `min_curvature` above `eps_feas`, a strict local Note: L17.44 gives a strict local minimizer only at exact first-order conditions; L17 states a numerical tolerance on the gaps (eps_kkt) is not covered | lemma:L17.44 test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified func:src/hyperbolic_trade_space/solvers.py::soft_certificate | broader than its backing | narrow |
| U40-C019 | S | - `stationary`: the gaps hold, the curvature does not: a saddle or a flat direction. Note: pins gap<=eps_kkt with curvature < -1 (saddle) via soft_certificate, not the status string 'stationary'; 'flat direction' (curvature near 0) is not tested | lemma:L17.50 test:tests/test_soft_fit.py::test_r7_all_terms_equal_is_stationary_and_not_certified | broader than its backing | narrow |
| U40-C020 | S | - `status`, `reason`, `n_iter`; `max_gap`, `gaps` (`nan` for an empty facet) and `shares`. Note: fields exist and gaps shape/max pinned; 'nan for an empty facet' is in the fixed_assignment_bound docstring and code, no test asserts nan gaps | test:tests/test_solvers.py::test_r1_planted_certificates test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified func:src/hyperbolic_trade_space/solvers.py::fixed_assignment_bound | broader than its backing | narrow |
| U40-C021 | M | - `bound`: the share-weighted sum of facet gaps, bounding the distance from the fixed-assignment | lemma:L14.20 test:tests/test_solvers.py::test_corollary_bound_on_every_planted_fit | backed | keep |
| U40-C022 | S | - `gamma`, `radius`: the margin and stable radius, `nan` at one term. | test:tests/test_solvers.py::test_margin_and_radius_are_nan_at_one_term_not_infinite | backed | keep |
| U40-C023 | S | - `min_curvature`: soft fit only, the smallest curvature on the active face; `nan` otherwise. | test:tests/test_soft_fit.py::test_r7_a_soft_fit_at_infinite_tau_is_not_applicable test:tests/test_soft_fit.py::test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified | backed | keep |
| U40-C024 | S | A soft fit leaves `gamma`, `radius` and `bound` `nan`. | test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified | backed | keep |
| U40-C025 | S | The tolerances are module constants of `hyperbolic_trade_space.solvers`, not parameters: `EPS_KKT` = | test:tests/test_solvers.py::test_default_path_has_no_warnings_and_constants test:tests/test_estimator.py::test_constants_are_reexported | backed | keep |
| U40-C026 | S | 1e-8, `EPS_FEAS` = 1e-9, `GUARD_TOL` = 1e-12, `POLISH_STEPS` = 5. | test:tests/test_solvers.py::test_default_path_has_no_warnings_and_constants test:tests/test_solvers.py::test_polish_never_increases_the_facet_objective_and_closes_the_gap test:tests/test_estimator.py::test_constants_are_reexported | backed | keep |
| U40-C027 | S | The smallest eigenvalue of the restricted Hessian at each facet's fit, over the participating Note: value pinned for a one-term fit with all exponents participating (Helmert-restricted eigenvalue); the restriction to participating exponents above 1e-3 is pinned only as a constant and a finite sparse case | test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue test:tests/test_estimator.py::test_conditioning_per_facet_and_nan_cases test:tests/test_estimator.py::test_constants_are_reexported | broader than its backing | narrow |
| U40-C028 | S | exponents (above 1e-3), one per facet. A small value marks a nearly flat direction (weakly identified exponents). It is `nan` at infinite | test:tests/test_estimator.py::test_conditioning_per_facet_and_nan_cases | backed | keep |
| U40-C029 | S | temperature and for a facet with fewer than two participating exponents. | test:tests/test_estimator.py::test_conditioning_per_facet_and_nan_cases | backed | keep |
| U40-C030 | M | A small value marks a nearly flat direction (weakly identified exponents). | lemma:L17.5 test:tests/test_estimator.py::test_conditioning_drops_for_nearly_collinear_metrics | backed | keep |
| U40-C031 | S | The margin `gamma` is in score units (log metrics), the scale of the band 1/tau; `radius` is | test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets | backed | keep |
| U40-C032 | M | `gamma / (2R)`, with R the largest norm of a row (u, -1). Compare `gamma` with the median margin, | lemma:L13.11 test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets | backed | keep |
| U40-C033 | M | the median gap between a design's best and second-best facet score: far below it, a few designs sit Note: gamma is the minimum gap, so far below the median says at least one design is near a seam and (by the median) at least half are not; 'a few designs' is not implied; no lemma or test states it | lemma:L13.7 | broader than its backing | to the driver |
| U40-C034 | R | On this table at tau = 50, `gamma` is 0.0020 against a band of 0.02 and a median margin of 0.21: Note: I ran it: gamma 0.002017, band 0.02, median margin 0.205 (0.21); the page's block prints them but no test pins these values (test_docs only executes the block; test_r1 pins 1e-4<gamma<1e-2 on another table) | gen:docs/user-guide/termination.md::second runnable block (S, top, print) | broader than its backing | narrow |
| U40-C035 | R | level 3 holds, for perturbations well under the band. Note: L13 guarantees score changes below gamma/2 = 0.001 (5% of the 0.02 band); 'well under the band' is vague and the numbers are unpinned | lemma:L13.7 gen:docs/user-guide/termination.md::second runnable block (S, top, print) | broader than its backing | narrow |
| U40-C036 | M | `certified` says the run is a local optimum (of its fixed assignment, or of the soft objective), nothing about other restarts. Note: Prop 3 and the second-order test are for exact first-order conditions and exact facet optima; the run is certified only within eps_kkt/eps_feas, a numerical tolerance L17 says is not covered | lemma:L14.18 lemma:L17.44 | broader than its backing | to the driver |
| U40-S01 | S | All three levels hold. | test:tests/test_solvers.py::test_r1_planted_certificates test:tests/test_solvers.py::test_terms_monotone_history_and_stops test:tests/test_estimator.py::test_termination_record_for_k_terms | backed | keep |

### U41: docs user-guide/limitations (`docs/user-guide/limitations.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U41-C001 | M | The exponents describe the conditioned metrics. Moving the | definition glossary:conditioning | backed | keep |
| U41-C002 | M | reference or the scale of one metric changes which facet is tangent. Note: L2 proves only the uniform shift (exponents unchanged) and says per-metric shifts change the facet is NOT proved (spec item 6); no test or lemma shows which facet is tangent changes under reference/scale moves | lemma:L2 glossary:conditioning | broader than its backing | to the driver |
| U41-C003 | M | Dents, holes and disconnected regions are invisible to it Note: L10.4 gives exp(kappa Phi_K) a posynomial and L4 convexity of J, but no step states that dents/holes/disconnected regions are invisible; L11 only says non-log-convex front parts are not reached by any w | lemma:L10 lemma:L4 | broader than its backing | to the driver |
| U41-C004 | M | number of terms represents them. A hole is an opportunity Note: Same as C003: any K-term model is a posynomial (log-convex), but 'no number of terms represents them' is not a stated step | lemma:L10 | broader than its backing | to the driver |
| U41-C005 | M | A hole is an opportunity only if the trade space is log-convex around it. Note: Conditional about when a hole is an opportunity; no lemma, test or source states it | none | unbacked | to the driver |
| U41-C006 | M | A single term has constant elasticities and finds one tension, at | lemma:L7 lemma:L3 | backed | keep |
| U41-C007 | M | Away from that point a design can score below 1 while locally on the frontier. Note: No lemma or test shows a design can score below 1 yet be locally on the (true) frontier away from the balanced point | none | unbacked | to the driver |
| U41-C008 | M | If the balanced point sits on a vertex or Note: L7 gives elasticities only for w_j != 0 (undefined at w_j = 0); non-uniqueness of the exponents at a vertex/edge is not proved in any lemma step or test | lemma:L7 lemma:L3 | broader than its backing | to the driver |
| U41-C009 | M | exponents are not unique and some elasticities are undefined. Note: Same as C008: undefined elasticity supported by L7 (w_j in the denominator); 'exponents are not unique' not stated in a step | lemma:L7 lemma:L3 | broader than its backing | to the driver |
| U41-C010 | M | are determined by the sample you give; the Pareto boundary is a property of the system. | lemma:L11 glossary:fitted-reference-surface glossary:supporting-envelope glossary:pareto-boundary | backed | keep |
| U41-C011 | M | of V is efficient in the contending metrics, and the converse is not claimed. | lemma:L11 test:tests/test_derivation.py::test_L11_in_chain_and_states_non_converse | backed | keep |
| U41-C012 | M | At a finite temperature some designs lie beyond V = 1 by construction. | lemma:L5 glossary:temperature | backed | keep |
| U41-C013 | M | Judge a score against the band 1/tau. Note: Advice; 1/tau is the default near-frontier band (tension_report test), but L5 gives the LME offset from the max as up to (log n)/tau, not 1/tau; no lemma states 1/tau as the scale of scores beyond V = 1 | test:tests/test_tensions.py::test_band_default_and_report_fields | broader than its backing | to the driver |
| U41-C014 | M | A very high tau rests the fit on a few extreme designs | lemma:L5 lemma:L3 | backed | keep |
| U41-C015 | M | tau of about 3 the soft maximum approaches the mean. Note: L5.4 proves LME -> mean only as tau -> 0; the threshold 'about 3' appears only in fitting.md/tuning.py docstring, with no test or lemma | lemma:L5 | broader than its backing | to the driver |
| U41-C016 | M | With few designs, or designs that barely differ near the edge, exponents are Note: No test, lemma or run shows exponents are weakly determined for few or near-edge-clustered designs | none | unbacked | to the driver |
| U41-C017 | M | The set is exact at infinite temperature with `min_exponent` at | glossary:contending-set test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact test:tests/test_tensions.py::test_no_warning_when_min_exponent_zero | backed | keep |
| U41-C018 | M | 0, and graded participation at a working temperature. | test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact glossary:support-weights | backed | keep |
| U41-C019 | M | A tension is a binding constraint, not a correlation, and | definition glossary:contending-set | backed | keep |
| U41-C020 | M | negative association near the surface is partly a closure effect. | test:tests/test_tensions.py::test_closure_induces_negative_association_without_trade | backed | keep |
| U41-C021 | M | A multi-term fit is a local optimum chosen among seeded restarts. | lemma:L15 test:tests/test_estimator.py::test_n_restarts_default_and_validation | backed | keep |
| U41-C022 | R | it recovers the planted facets in 16 or 17; failures are facets with Note: Generator and test pin 16 of 20 at both temperatures (seeds 1, 3, 8, 16 fail); '16 or 17' is broader: 17 comes only from the spike/review (seed 8 differs), not the pinned run | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 | broader than its backing | narrow |
| U41-C023 | R | five or six frontier rows. More restarts do not cure this Note: Pinned thinnest-facet frontier rows of the failures are 5, 6, 11, 5 (seeds 1, 3, 8, 16): seed 8 has 11, so 'five or six' is too narrow | gen:paper/generate_results.py::planted_recovery test:tests/test_paper.py::test_cr2_the_planted_recovery_is_in_section_9_with_its_table_in_d14 | broader than its backing | narrow |
| U41-C024 | M | More restarts do not cure this; a larger sample or `facet_step="tangent"` Note: Restarts half only in G-14 text (WP9-review: 5, 20, 50 restarts, no failing seed recovered); no test/generator pins it; 'larger sample or facet_step=tangent can help' has no run: the test covers identifiable tables only, not the failing seeds | file:docs/superpowers/notes/abstraction-gaps.md test:tests/test_estimator.py::test_k_terms_both_steps_recover_under_identifiability | broader than its backing | to the driver |
| U41-C025 | M | V - 1 says how far a design lies beyond the learned surface | definition glossary:novelty | backed | keep |
| U41-C026 | M | Elasticities are shape, not preference, and not causal. Note: L7 says elasticities are shape quantities, not preferences; 'not causal' is not stated in a step or test | lemma:L7 | broader than its backing | to the driver |
| U41-C027 | M | A prediction inherits the surrogate's error and the fitted trade Note: Caution on inherited surrogate error; no lemma, test or source asserts it (test_predict_check_within_the_band checks a band, not inheritance) | none | unbacked | to the driver |
| U41-C028 | M | which tends to zero as any participating | glossary:invariant-value test:tests/test_preconditioning.py::test_pullback_zero_attribute_gives_minus_inf_in_both | backed | keep |
| U41-C029 | L | It is unrelated to PCA in hyperbolic space [@chami2021horopca]. | bib:chami2021horopca | backed | keep |
| U41-C030 | S | Machine checks confirm that formulas follow from stated conditions and that the code agrees with | test:tests/test_matches_derivation.py::test_fitted_model_matches_chain_L1_L7_L8 | backed | keep |

### U42: site index (`site/index.html`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U42-C001 | P | evaluated designs is lost, and the alternatives are bespoke or opaque. A model-based method | reading | backed | keep |
| U42-C002 | P | has to clear a bar before a decision-maker can trust it: it has to show its reasoning, say | reading | backed | keep |
| U42-C003 | P | Trade studies are usually decided from documents and tables, where the detail of the | reading | backed | keep |
| U42-C004 | M | What trades against what depends on where a design sits. | lemma:L7 lemma:L10 test:tests/test_site.py::test_why_labels_come_from_the_exponents test:tests/test_site.py::test_why_regions_partition_the_triangle_and_there_are_three_facets | backed | keep |
| U42-C005 | R | the coloured dots are at the frontier. Note: Coloured dots are those with \|log V\| < near=0.2 (near the fitted reference surface, not the Pareto frontier); no test pins which dots are coloured; test_site only checks the caption text | gen:scripts/build_site_figures.py::draw func:src/hyperbolic_trade_space/plotting.py::plot_ternary | unbacked | drop |
| U42-C006 | M | PCA explains variance; this explains tensions. | definition | backed | keep |
| U42-C007 | M | product of the metrics that names which of them compete on one part of the trade space. | lemma:L3 glossary:n-lemma test:tests/test_tensions.py::test_contending_set_recovers_planted_support | backed | keep |
| U42-C008 | P | method belongs in unsupervised learning and feature engineering beside PCA: kin rather than a | reading | backed | keep |
| U42-C009 | S | coordinates). It ships as a scikit-learn-compatible estimator (fit, | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score test:tests/test_sklearn_compat.py::test_tags_only_through_sklearn_tags | backed | keep |
| U42-C010 | S | substitute, and the two chain (the tension report already runs PCA on the near-frontier chart | test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions func:src/hyperbolic_trade_space/tensions.py::tension_report | backed | keep |
| U42-C011 | S | conformance checks pass), so it drops into the same workflows. | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator test:tests/test_estimator.py | backed | keep |
| U42-C012 | R | The black arrow is the same step in each pane: a design's energy differential to the fitted reference surface. Note: The arrow is drawn as one uniform scaling in each pane in the generator, but no test asserts the arrow or its equality across panes (test_figure1_has_three_panes checks titles and words only) | gen:paper/figures/figure1.py::figure1 | unbacked | drop |
| U42-C013 | M | The foundation box is the invariant form: a weighted geometric mean | lemma:L1 glossary:invariant-value registered:C002 | backed | keep |
| U42-C014 | M | V of the metrics, whose level V = 1 is the fitted reference surface and whose logarithm is the | lemma:L1 glossary:fitted-reference-surface glossary:energy-differential registered:C004 | backed | keep |
| U42-C015 | M | energy differential. The single-term core fits the weights and an offset to your designs as | lemma:L3 lemma:L4 lemma:L5 | backed | keep |
| U42-C016 | M | one convex problem. Four boxes use that fit: the chart (each design becomes a position along | lemma:L8 lemma:L7 lemma:L6 lemma:L9 | backed | keep |
| U42-C017 | S | its guarantees. Each box carries a badge, derived, checked numerically or open; the red box Note: Backed for the badges on the paper's lemma blocks and the open-questions list; no test checks the map image paper-map.webp itself shows badges on each box or a red box of open questions | test:tests/test_paper.py::test_badges_are_present_and_the_open_questions_are_marked | broader than its backing | narrow |
| U42-C018 | M | correction for noise, and the pull-back to your raw attributes. The lower boxes extend the | lemma:L6 lemma:L9 lemma:L10 lemma:L11 lemma:L12 lemma:L13 lemma:L14 lemma:L15 lemma:L17 | backed | keep |
| U42-C019 | S | A scikit-learn-compatible estimator for the frontier, with an invertible log-ratio chart, | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples test:tests/test_tensions.py::test_monolemma_and_names test:tests/test_plotting.py::test_ternary_regions_partition_the_triangle file:work-packages/interface-contract.toml | backed | keep |
| U42-C020 | S | to reading a tension report, the API reference, a cubesat example, the model in brief | file:work-packages/interface-contract.toml test:tests/test_site.py::test_nav_pages_exist_and_cover_the_contract_pages | backed | keep |
| U42-C021 | S | The paper tells the method, the documentation shows how to use the package task by task | definition | backed | keep |

### U43: README (`README.md`)

| Id | Kind | Fragment | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| U43-C001 | M | "space": a monomial, later posynomial, frontier V(m) = Π m_j^{w_j} whose unit level set is the | lemma:L1.4 lemma:L1.6 glossary:invariant-value | backed | keep |
| U43-C002 | M | Pareto frontier, together with an invertible coordinate chart (position along the frontier, and Note: Chart invertibility is backed (L8.14 round trip, L9.6 conditioning); 'unit level set is the Pareto frontier' is broader than L11 (a V-maximizer is efficient, converse not claimed; fitted frontier is not the true front); narrow to 'a model of the frontier' | lemma:L11.17 lemma:L8.14 lemma:L9.6 glossary:chart | broader than its backing | to the driver |
| U43-C003 | M | (configuration variables and empirically assessed attributes), the method learns a hyperbolic | definition | backed | keep |
| U43-C004 | S | log V, the energy differential to it). It is a scikit-learn-compatible unsupervised estimator, with | test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score glossary:energy-differential | backed | keep |
| U43-C005 | S | SymPy-verified derivations and an ADCS trade-study case. | test:tests/test_proof_map.py::test_checker_passes_on_the_committed_record test:tests/test_adcs_case.py::test_evaluate_design_three_fast | backed | keep |
| U43-C006 | R | Status: WP0 (setup) complete; the package code arrives in later work packages. Note: Stale: states the package code is yet to arrive, but src/hyperbolic_trade_space (estimator, solvers, plotting, etc.) exists with tests; no WP status backing; update or drop | none | unbacked | drop |

## Proposed register rows

338 rows in the fields of `claims_register.toml`, ids from C024 on, for the claims that are backed, unchanged, kept, not routed, not already registered, whose pointers are in the register's syntax, and whose fragments occur verbatim in a markdown cell or a docs page of the pinned commit. Each row passed `check_register` of `tests/test_claims_register.py` against the pinned checkout (fragment, anchor, every backing item). Rows for narrowed or routed claims are not proposed: they follow the edit. Rows are `status = "backed"`, `disposition = "keep"`; `anchor` is empty (anywhere in the file).

```toml
[[claim]]
id = "C024"
fragment = "A trade study must produce an answer and a justification an accountable executive can follow."
file = "paper/paper.ipynb"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Normative statement of the paper's own position; reading_pass n=1/2: the two products are uncited own statement (howard1988decision, keeney1993decisions only partly supported)"

[[claim]]
id = "C025"
fragment = "Principal component analysis (PCA) is trusted as reproducible and interpretable, but explains"
file = "paper/paper.ipynb"
anchor = ""
kind = "P"
backing = ["bib:jolliffe2016principal", "reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n=9: source supports dimensionality reduction/interpretability only; 'trusted' and 'reproducible' are the author's wording, marked reading"

[[claim]]
id = "C026"
fragment = "variance, not trade-offs. We explain tensions."
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["bib:jolliffe2016principal"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "PCA explains variance: prior_art id pca / reading_pass n=33 supported; 'We explain tensions' is statement of intent/scope"

[[claim]]
id = "C027"
fragment = "the data underlying the table, not the Pareto boundary, and gives the data a coordinate system;"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L8", "lemma:L11", "glossary:chart"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Chart is a coordinate system on the data (L8); surface is not the Pareto boundary (L11: maximizer of V is efficient, converse not claimed); def-objects scope statement"

[[claim]]
id = "C028"
fragment = "Modelling a single n-lemma fits a monomial, which transforms into a convex program and is solved directly; when"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L10.9", "lemma:L4.13", "lemma:L4.24", "test:tests/test_solvers.py::test_slsqp_agrees_with_lp"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L10.9 K=1 is a monomial; L4.13 convex, L4.24 geometric program (one facet). 'solved directly' only loosely pinned by SLSQP-vs-LP agreement"

[[claim]]
id = "C029"
fragment = "compatibility. Our implementation mirrors the structure of PCA as an unsupervised learning"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator", "test:tests/test_sklearn_compat.py::test_tags_only_through_sklearn_tags", "func:src/hyperbolic_trade_space/estimator.py::HyperbolicTradeSpace"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "TransformerMixin estimator with fit/transform/inverse_transform/score_samples, no predict, sklearn checks pass; 'feature engineering' role is intent; interface contract has no transform entries"

[[claim]]
id = "C030"
fragment = "the fit identifies the trade-offs among the metrics those subsystems set."
file = "paper/paper.ipynb"
anchor = ""
kind = "R"
backing = ["gen:examples/adcs/case.py::facet_table", "test:tests/test_case.py::test_k3_facets_equal_the_primary_record", "test:tests/test_case.py::test_k1_contending_set_equals_the_record", "test:tests/test_case.py::test_subsystem_mapping_is_data_and_covers_every_attribute"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Contending sets pinned (big facet: peak slew power, total mass, pointing error ...) and subsystem mapping 4+5+1; 'metrics those subsystems set' is the mapping"

[[claim]]
id = "C031"
fragment = "Decision analysis has two products: an answer, and a justification an accountable executive can follow and defend."
file = "paper/paper.ipynb"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Paper's own statement, uncited by design (reading_pass n=1 'now'); register as reading."

[[claim]]
id = "C032"
fragment = "It seeks responsible choice among conflicting objectives [@keeney1993decisions]"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:keeney1993decisions"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n=2 (reworded to 'responsible choice among conflicting objectives', matches publisher/Crossref description); row verdict was partly supported on the pre-reword sentence."

[[claim]]
id = "C033"
fragment = "and clear conversation with the decision-maker [@howard1988decision]"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:howard1988decision"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n=1 (reworded: cited for clear conversation with the decision-maker, abstract); row verdict was partly supported on the pre-reword sentence; n=50 supported."

[[claim]]
id = "C034"
fragment = "The justification is the hard product: the process turning much data into little must be recognized, reproducible, rigorous."
file = "paper/paper.ipynb"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Author's judgment of what the justification must be; no source claimed."

[[claim]]
id = "C035"
fragment = "A trade study is a document: a grid, a table, a ranking by weighted criteria"
file = "paper/paper.ipynb"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n=3 'now': that a trade study is a document is stated as the practice the author knows."

[[claim]]
id = "C036"
fragment = "a ranking by weighted criteria; surveys compare them [@baker2012survey]"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:baker2012survey"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n=3 (reworded, cited only for 'surveys compare them') and n=52 supported (Pugh, AHP, Kepner-Tregoe compared)."

[[claim]]
id = "C037"
fragment = "The weights are human judgments, susceptible to bias in trade studies [@smith2007ameliorating; @chilli2026decision]"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:smith2007ameliorating", "bib:chilli2026decision"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n=5 supported (human numerical judgment, biases); n=6 reworded, cited for bias in trade studies only; 'weights are human judgments' is the paper's own gloss."

[[claim]]
id = "C038"
fragment = "Systems engineering is moving from document-based [@henderson2021value] to model-based practice [@madni2018model]"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:henderson2021value", "bib:madni2018model"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n=8 supported (document-based to model-based, Henderson); n=7 reworded, Madni cited only for model-based practice."

[[claim]]
id = "C039"
fragment = "PCA reduces dimensionality and increases interpretability while minimizing information loss [@jolliffe2016principal]"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:jolliffe2016principal"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n=9 (reworded to what PCA does: reduces dimensionality, increases interpretability, minimizes information loss) and n=33 supported."

[[claim]]
id = "C040"
fragment = "Each facet names the metrics that contend on it with elasticities"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L7.5", "glossary:elasticity", "glossary:contending-set"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L7.5: d log m_j / d log m_k = -w_k/w_j along the facet; contending set = metrics with positive exponent (glossary)."

[[claim]]
id = "C041"
fragment = "Our implementation mirrors the structure of PCA as an unsupervised learning method for feature engineering"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator", "test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score", "test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Transformer with fit/transform/inverse_transform/score_samples under parametrize_with_checks, empty expected-failures dict, no predict; decomposition-family semantics."

[[claim]]
id = "C042"
fragment = "and the two chain: {ref}`Appendix D.16 <sub-d-16>` reads the principal directions"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["gen:paper/generate_results.py::pca_chain", "test:tests/test_paper.py::test_cr11_chaining_with_pca_is_worked_on_the_case_in_d16"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "D.16 reads principal directions of the near-frontier chart (cell tab-D-pca_chain pinned current; leading metrics identical over regenerations); prose says a reading, not a result."

[[claim]]
id = "C043"
fragment = "The fitted reference surface is the unit level set of a degree-one weighted geometric mean, not the Pareto boundary"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L1.5", "lemma:L1.6", "glossary:invariant-value", "glossary:fitted-reference-surface", "glossary:pareto-boundary"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L1.5 degree-one homogeneity, L1.6 V(m/V)=1 so V=1 is the unit level set; scope is the one-weight-vector mean (thm-invariant); 'not the Pareto boundary' is the three-objects distinction (Definition), not a proved inequality; for K>1 the surface is the posynomial's unit level set (L10)."

[[claim]]
id = "C044"
fragment = "The one-facet fit is a geometric program, convex in the logarithmic variables"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L4.23", "lemma:L4.24", "glossary:geometric-program"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L4.14-L4.24: with x=exp(w) the one-facet fit is a GP in standard form, convex in w by L4.13/L4.23."

[[claim]]
id = "C045"
fragment = "its exponents are elasticities and its chart is reversible"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L7.5", "lemma:L8.14", "glossary:elasticity", "glossary:chart"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L7.5 exponents give elasticities -w_k/w_j; L8.14 chart round trip (reversible)."

[[claim]]
id = "C046"
fragment = "Pareto methods return a nondominated set and find its members by scalarization"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:miettinen1999nonlinear", "bib:ehrgott2005multicriteria", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "rows 10 (contents list the weighting method as a posteriori scalarization; verdict partly, for the old 'supported part' wording, since removed) and 11 (not accessible); AUDIT: no supported row for the current wording, re-mark row 10 or the pointer fails the test"

[[claim]]
id = "C047"
fragment = "evolutionary algorithms generate such sets [@zitzler1999multiobjective; @deb2002fast]"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:zitzler1999multiobjective", "bib:deb2002fast", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass rows 12 and 13 both supported"

[[claim]]
id = "C048"
fragment = "Dominance is a hard comparison that stops discriminating, on this case, as metrics are added"
file = "paper/paper.ipynb"
anchor = ""
kind = "R"
backing = ["gen:paper/generate_findings.py::nondominated_sentence", "test:tests/test_paper.py::test_cr7_16_the_first_screen_says_what_scales_and_keeps_the_three_objects_apart", "test:tests/test_paper.py::test_generated_sentences_quote_the_ranges_from_the_results_file"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "706 designs: nondominated 7-8 on 2, 145-146 on 4, 671 on 10 attributes; the test pins '671 on 10' and every range against the results file; 'on this case' scopes it"

[[claim]]
id = "C049"
fragment = "while the fit returns an exponent vector per facet, a band of near-frontier designs and an effective sample size"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_fit_invariants", "test:tests/test_estimator.py::test_k_terms_attributes_conventions", "test:tests/test_estimator.py::test_n_terms_above_one_is_implemented"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "exponents_ (K,d), support_weights_ (the band, sums to 1), n_eff_ = 1/sum p^2; n_eff_ and support_weights_ are not in the interface contract's fitted_attributes list"

[[claim]]
id = "C050"
fragment = "a maximizer of V with positive exponents is Pareto-efficient"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L11.17", "lemma:L11.19", "glossary:invariant-value"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L11.17 a maximizer of V is not dominated; L11.19 efficient when every w_j > 0 (K=1)"

[[claim]]
id = "C051"
fragment = "the theorem gives efficiency of a maximizer, not the converse"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L11.17", "lemma:L11.19"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "the L11 statement says the converse is not claimed; the sentence states the scope of the theorem"

[[claim]]
id = "C052"
fragment = "It scores each unit against the data by mathematical programming, with weights obtained from the data"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:banker1984some", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "row 17 abstract: mathematical programming, ratio form obtained from the data with no a priori weights (the sentence is the reworded remainder); AUDIT: row 17 verdict is partly supported, re-mark for the current wording"

[[claim]]
id = "C053"
fragment = "a super-efficiency variant ranks efficient units against a reference technology spanned by all other units"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:andersen1993procedure", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "row 18 abstract states exactly this (reference technology spanned by all other units); AUDIT: verdict partly supported only for the dropped 'scores above one'; re-mark for the current wording"

[[claim]]
id = "C054"
fragment = "Malmquist indices run across data sets"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:fare1994productivity", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass row 19 supported: Malmquist productivity indexes over periods ('across data sets' = across periods)"

[[claim]]
id = "C055"
fragment = "practice has added weights restrictions [@allen1997weights] and protocols"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:allen1997weights", "bib:dyson2001pitfalls", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "rows 20 and 21: abstracts give weights restrictions arising from applications and protocols/pitfalls of applying DEA; AUDIT: both verdicts partly supported (dropped 'favourable weights' framing); re-mark for the current wording"

[[claim]]
id = "C056"
fragment = "We fit one exponent vector per facet, a global named structure"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_fit_invariants", "test:tests/test_estimator.py::test_n_terms_above_one_is_implemented", "file:work-packages/interface-contract.toml", "glossary:exponent-vector"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "exponents_ has shape (K,d), one simplex point per facet, fitted from the whole table (contract fitted_attributes lists exponents_)"

[[claim]]
id = "C057"
fragment = "Our facets are piecewise log-linear with constant elasticities within a facet"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L7.5", "lemma:L10.9", "lemma:L10.18", "lemma:L10.19", "glossary:facet", "glossary:elasticity"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "each facet is one monomial (log-linear, L10.19) with elasticity -w_k/w_j independent of the point (L7.5); piecewise exactly as kappa->inf (L10.18), within (log K)/kappa otherwise (L10.16)"

[[claim]]
id = "C058"
fragment = "Our metrics are larger-is-better with homogeneity from the simplex"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L1.5", "lemma:L1.8", "lemma:L11.7", "glossary:metrics", "glossary:invariant-value"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "degree-1 homogeneity passes through sum w_j = 1 (L1.5, L1.8); larger-is-better is the metrics convention (glossary) and V is nondecreasing in each metric (L11.7)"

[[claim]]
id = "C059"
fragment = "Our boundary is a soft maximum with a temperature, a band and an effective sample size"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L5.15", "lemma:L5.16", "lemma:L5.24", "glossary:temperature", "glossary:support-weights", "test:tests/test_estimator.py::test_k_terms_attributes_conventions"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "soft maximum with temperature and band (log n)/tau (L5); effective sample size is a definition, n_eff_ = 1/sum p^2, pinned by the test, not a lemma"

[[claim]]
id = "C060"
fragment = "We solve one convex program and K refits, and return coordinates with a pull-back to attribute units"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["lemma:L4", "test:tests/test_solvers.py::test_slsqp_agrees_with_lp", "test:tests/test_solvers.py::test_terms_k1_equals_slsqp_and_degenerate", "test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples", "test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "one convex program per facet (L4; K=1 fit equals the single program) and K facet refits in the alternation; the joint several-facet fit is not convex (L16), so read 'one program, K refits' as the sentence does; pull-back test pins the original-unit frontier"

[[claim]]
id = "C061"
fragment = "The weighted geometric mean with exponents summing to one has the constant-returns Cobb-Douglas form"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L1.5", "lemma:L1.8", "glossary:invariant-value"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "weighted geometric mean with sum w = 1 is homogeneous of degree one, i.e. constant returns; the identification with the Cobb-Douglas form is the paper's own (row 23 not accessible, nothing attributed)"

[[claim]]
id = "C062"
fragment = "Shephard's characterization of a technology by its distance function"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:shephard1970theory", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "row 24: publisher description gives distance function as a general characterization of technology (the table sentence supported); AUDIT: row verdict partly supported because the V reading is the author's, which this fragment does not claim; re-mark"

[[claim]]
id = "C063"
fragment = "Frontier estimation by programming, corrected least squares and one-sided error is the family of one-sided fits"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:battese1992frontier", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass row 27 supported: body states LP/QP, COLS, ML and stochastic frontiers with one-sided component; rows 28-32 (partly) for the earlier works"

[[claim]]
id = "C064"
fragment = "The model class and refit scheme come from geometric programming and max-affine fitting"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:boyd2007tutorial", "bib:hoburg2016data", "bib:magnani2009convex", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass rows 37, 39, 40 all supported (GP and generalized posynomials; softmax-affine GP-compatible fits; alternating assignment and refit)"

[[claim]]
id = "C065"
fragment = "the soft maximum is an entropic risk functional"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["bib:foellmer2026entropic", "lemma:L5", "glossary:temperature", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "row 42 supported: eq. (1) is (1/beta) log E exp(-beta X), the log-mean-exp on the empirical distribution (L5)"

[[claim]]
id = "C066"
fragment = "Kernel PCA is the feature-engineering kin of the direction"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:schoelkopf1998nonlinear", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "row 43 supported for kernel PCA; 'kin of the direction' is the author's relation (row 43 notes it)"

[[claim]]
id = "C067"
fragment = "\"hyperbolic\" here is unrelated to hyperbolic PCA"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:chami2021horopca", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass row 44 (chami2021horopca) verdict supported: HoroPCA is PCA in hyperbolic space; 'unrelated' is the paper's statement about its own term (prior_art.yaml kernel-hyperbolic-pca differs)"

[[claim]]
id = "C068"
fragment = "Tradespace exploration lets an analyst explore designs"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:ross2005tradespace", "bib:stump2009visual", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass rows 45 and 46 verdict supported (status reworded to exactly this sentence); prior_art.yaml entry tradespace"

[[claim]]
id = "C069"
fragment = "We did not find the combination in the sources reviewed"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["file:paper/prior_art.yaml", "test:tests/test_paper.py::test_prior_art_cites_resolve_in_the_bibliography"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "absence claim scoped to 'the sources reviewed', which Appendix G (generated from prior_art.yaml) lists; no row can verify absence, so it is backed only as a statement of the review's outcome"

[[claim]]
id = "C070"
fragment = "the evaluation is a black box to the method"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["file:work-packages/interface-contract.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Scope/intent: interface contract 'Black box' paragraph (line 114) states exactly this; the pipeline is by the contract"

[[claim]]
id = "C071"
fragment = "so the method stays relevant as tools move or where scoring comes from physical systems or human judgment"
file = "paper/paper.ipynb"
anchor = ""
kind = "P"
backing = ["reading", "file:work-packages/interface-contract.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Design rationale and forecast ('stays relevant'), the author's judgment; the contract backs the three sources of attributes; not marked as judgment in the prose"

[[claim]]
id = "C072"
fragment = "The formal results are properties of mathematical objects, conditioned on assumptions that we cannot certify for a given table of designs"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["file:derivation/axioms.py", "file:docs/superpowers/notes/abstraction-gaps.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Each lemma is stated under declared axioms (A1-A7, F, I, R in axioms.py); that data cannot be certified to meet them is the point of the gaps ledger; scope statement, no single lemma step"

[[claim]]
id = "C073"
fragment = "the implementation approximates those objects numerically"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["file:docs/superpowers/notes/abstraction-gaps.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Framing: floating-point/solver tolerances are recorded in the ledger (e.g. G-16 tolerances); no single test asserts 'approximates'; trivially true of numerical code"

[[claim]]
id = "C074"
fragment = "which records for each place where the map and the territory part the assumption that bridges it"
file = "paper/paper.ipynb"
anchor = ""
kind = "R"
backing = ["gen:paper/generate_gaps.py::gaps_table", "test:tests/test_paper.py::test_gaps_table_has_every_ledger_row"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "gaps_table columns are formal object, bridging assumption, what cannot be proved, evidence, interpretive consequence; test pins every ledger row appears; completeness of 'each place' is not tested"

[[claim]]
id = "C075"
fragment = "The supporting envelope is the $\\tau=\\infty$ fit, which none exceeds."
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L5", "glossary:supporting-envelope"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Definition of the tau=inf fit plus the claim: at tau=inf beta=max so log V_i=w.u_i-max<=0; L5 (F5 s_i<=M, LME->max) gives it, but no step states V<=1 for all rows of the fit; weak"

[[claim]]
id = "C076"
fragment = "At $K=1$ the frontier is the unit level set of $V$."
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L10.9", "lemma:L1.6", "glossary:fitted-reference-surface"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L10.9 Phi_1 = w.u - beta (so Phi_1=0 iff log V=0, L1.7); glossary defines the reference surface as V=1"

[[claim]]
id = "C077"
fragment = "At $\\tau=\\infty$ the fit is a linear program."
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L5.24", "lemma:L12.31", "func:src/hyperbolic_trade_space/solvers.py::solve_lp", "test:tests/test_solvers.py::test_lp_gap_equals_duality_gap_and_uniform_ties_is_a_valid_bound"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L5.24 gives J_inf = max_i w.u_i; the epigraph LP is what solve_lp implements (doctest) and LP duality is tested; no step names the LP form itself"

[[claim]]
id = "C078"
fragment = "At finite $\\tau$ one facet is a geometric program, convex after the change of variables $x=e^{w}$"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L4.24", "lemma:L4.23", "glossary:geometric-program"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L4.14-L4.24: posynomial objective, monomial equality/inequalities in x=e^w, convex by L4.13"

[[claim]]
id = "C079"
fragment = "$V_K$ is a generalized posynomial, the term maximum at the default $\\kappa=\\infty$"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L10.7", "lemma:L10.18", "lemma:L10.19", "glossary:generalized-posynomial"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "finite kappa: e^(kappa Phi_K) posynomial (L10.7); kappa=inf: max of the monomial terms (L10.18/19), a generalized posynomial per Boyd (see C007)"

[[claim]]
id = "C080"
fragment = "generalized posynomial, the term maximum at the default $\\kappa=\\infty$ [@boyd2007tutorial]"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:boyd2007tutorial", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass.yaml n=37 boyd2007tutorial verdict supported (sect. 5.3 generalized posynomials); prior_art.yaml row cites it"

[[claim]]
id = "C081"
fragment = "Several facets alternate weights with one program for all terms"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L16.49", "lemma:L16.43", "lemma:L16.30"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "fixed-weight objective over all terms is a generalized posynomial (L16.49) and majorizes the soft slack (L16.43), the thm-soft statement"

[[claim]]
id = "C082"
fragment = "$\\tau$ puts a target fraction of designs above $V=1$: 10 percent here"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_tuning.py::test_selected_temperature_hits_target", "func:src/hyperbolic_trade_space/tuning.py::select_temperature", "test:tests/test_case.py::test_sensitivity_and_refits_on_frozen_primary"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "select_temperature hits the target frac_above_ within 0.01; the case uses spec.target_frac=0.10 (case.py), baseline tau pinned"

[[claim]]
id = "C083"
fragment = "Zeros are tolerated in data and masked in the fit, negative values are rejected"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_zero_metric_row", "test:tests/test_estimator.py::test_negative_and_nonfinite_raise"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "zero row: exponents unchanged, support weight 0, score -inf; negatives raise 'Negative values in data' in fit and transform"

[[claim]]
id = "C084"
fragment = "the pull-back to attribute units is exact"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L9.5", "lemma:L9.6", "test:tests/test_preconditioning.py::test_pullback_matches_L9_chain_formula"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V = e^(w.b-beta) prod (a_j+s_j)^(w_j alpha_j) and the conditioning round trip returns u (L9.4/L9.6)"

[[claim]]
id = "C085"
fragment = "The fit is a scikit-learn transformer of the decomposition family"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator", "test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score", "file:docs/superpowers/notes/sklearn-conformance.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "parametrize_with_checks with empty expected failures; TransformerMixin class; decomposition-family surface asserted"

[[claim]]
id = "C086"
fragment = "`fit` identifies exponents and offsets, `transform` returns the chart"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_fit_invariants", "test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "fit sets exponents_ and log_offset_; transform returns the chart (shape and round trip)"

[[claim]]
id = "C087"
fragment = "`inverse_transform` reverses it, `score_samples` returns the energy differential"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples", "glossary:energy-differential"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "inverse_transform(T) == X; last chart coordinate equals score_samples (log V, the energy differential)"

[[claim]]
id = "C088"
fragment = "It has no `predict`: prediction composes a supervised regressor with the chart."
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score", "test:tests/test_predictive.py::test_trade_space_can_be_a_pipeline_and_regressor_a_pipeline"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "no predict attribute asserted; TradeSpaceRegressor composes a regressor with the chart (test_predictive)"

[[claim]]
id = "C089"
fragment = "*One facet at $K=1$:* constant elasticities; $K>1$ is built."
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["lemma:L7.5", "test:tests/test_estimator.py::test_k_terms_recovers_planted_facets", "test:tests/test_estimator.py::test_n_terms_above_one_is_implemented"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "elasticity -w_k/w_j constant along a facet (L7.5); K>1 implemented and recovers planted facets"

[[claim]]
id = "C090"
fragment = "facets are fitted at $\\kappa=\\infty$ with kinks on the ridges"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["lemma:L10.18", "test:tests/test_soft_fit.py::test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "default term_temperature is np.inf (label fit, max of affine terms, kink where terms tie)"

[[claim]]
id = "C091"
fragment = "a finite $\\kappa$ moves the score by at most $(\\log K)/\\kappa$"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L10.15", "lemma:L10.16"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "max_k x_k <= Phi_K <= max_k x_k + (log K)/kappa"

[[claim]]
id = "C092"
fragment = "on each facet the normal is an ascent direction in log space"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L1.7", "lemma:L10"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L1.7: log V = w.u - beta so gradient in log space is w, the facet normal; L10 for per-facet terms"

[[claim]]
id = "C093"
fragment = "Our case is a cubesat model coupling power, mass and attitude control."
file = "paper/paper.ipynb"
anchor = ""
kind = "R"
backing = ["gen:examples/adcs/cubesat_model.py::measure", "test:tests/test_cubesat_model.py::test_measure_returns_attributes_and_flags", "test:tests/test_paper.py::test_the_case_is_described_as_power_mass_and_attitude_control"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Model (cubesat_tradespace.sysml via cubesat_model.measure) has power, mass and attitude attributes and flags; the paper test pins the phrase"

[[claim]]
id = "C094"
fragment = "Conditioning orients each attribute, shifts and scales it to unit log-spread and keeps the map invertible."
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["test:tests/test_preconditioning.py::test_unit_log_standard_deviation", "test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift", "lemma:L9"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "default standard scaler gives unit log standard deviation, orientation and shift, round trip exact; L9 for the log-affine pull-back"

[[claim]]
id = "C095"
fragment = "A regressor from configuration to chart coordinates predicts where proposals fall"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_recovers_planted_coordinates", "test:tests/test_case.py::test_predict_check_within_the_band"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "a regressor to chart coordinates (case.fit_regressor) predicts positions; tests cover recovery and the predict-check"

[[claim]]
id = "C096"
fragment = "The exponents and elasticities are features of the conditioned empirical model"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L7.5", "glossary:elasticity"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Elasticity is the derivative along the fitted facet (L7.5); glossary not-clause: not a causal exchange or intervention effect; 'sampled designs' is the scope of the fit"

[[claim]]
id = "C097"
fragment = "they describe how the sampled designs trade, and not a causal exchange that changing a variable would reproduce"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["glossary:elasticity", "lemma:L7.5"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Statement of what the quantities do not mean (glossary not-clause), a scope statement; no stronger claim made"

[[claim]]
id = "C098"
fragment = "Novelty $V-1$ says how far beyond the fitted reference surface a design lies, not whether anyone wants it."
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L1.6", "lemma:L7.9", "glossary:novelty"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V-1 as how far beyond the reference surface (V(m/V)=1, uniform improvement 1/V); 'not whether anyone wants it' is the glossary not-clause (not a measure of attainability), scope"

[[claim]]
id = "C099"
fragment = "Machine verification shows that a formula follows from its hypotheses and that the code agrees"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["test:tests/test_proof_map.py::test_record_holds_every_step_with_tag_prose_and_code", "test:tests/test_proof_map.py::test_checker_passes_on_the_committed_record"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "The checker ties each tagged step's prose and code to the record and the ledger of hypotheses; that is what 'verification' means here"

[[claim]]
id = "C100"
fragment = "gives one line of code to read each proof step against"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_paper.py::test_appendix_b_shows_every_result_of_the_record_with_derived_counts", "test:tests/test_proof_map.py::test_record_holds_every_step_with_tag_prose_and_code"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Appendix B is generated from the record (every step is one tagged line of code, counts derived); tests pin both"

[[claim]]
id = "C101"
fragment = "How the attributes were produced is a black box to the method, so the same functions serve a simulator"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["file:work-packages/interface-contract.md", "test:tests/test_case.py::test_a_second_table_runs_without_cubesat_edits"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Contract 'Black box' paragraph: simulator, physical test or human assessment satisfy the same contract and the method depends on the table and signature only"

[[claim]]
id = "C102"
fragment = "Another table runs through the same calls."
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_case.py::test_a_second_table_runs_without_cubesat_edits"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Test runs a planted second table through load_study, fit_study, tables and k_sweep without cubesat edits; 'same calls' = the case API, not every function"

[[claim]]
id = "C103"
fragment = "The fitted surface is a log-convex envelope."
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L10.7"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L10.7: exp(kappa Phi_K) is a posynomial in m, so Phi_K is convex in u by cited I4 (log-sum-exp of affine, context only); K=1 is affine (L10.9). Convexity itself rests on cited I4, not a proved step"

[[claim]]
id = "C104"
fragment = "The exponents depend on the conditioning."
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L9.5"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Raw-attribute exponents are w_j alpha_j and the offset changes: exponents are tied to the conditioning (L9.5, L9.6 invertible)"

[[claim]]
id = "C105"
fragment = "K = 1 finds one tension; several regional tensions need K > 1."
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L10.9"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "K=1 is one monomial/facet (L10.9); 'several regional tensions need K>1' follows from K being the number of facets (Definition 3), scope"

[[claim]]
id = "C106"
fragment = "as PCA extracts components, is a research question"
file = "paper/paper.ipynb"
anchor = ""
kind = "L"
backing = ["bib:jolliffe2016principal", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Reading pass row 33 (verdict supported): PCA gives components that successively maximize variance; prior_art id pca. 'is a research question' is the author's scope"

[[claim]]
id = "C107"
fragment = "a design with $V=v$ is a frontier design scaled by $v$"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L1.5", "lemma:L1.6"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V(km)=kV(m) and V(m/V(m))=1 give m = V(m) * (m/V(m)) with m/V on the frontier"

[[claim]]
id = "C108"
fragment = "supply configurations, attributes and a conditioning rule, and use the same calls"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["file:work-packages/interface-contract.md", "test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples", "test:tests/test_docs.py::test_runnable_blocks_execute"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Contract states the source of attributes is a black box (simulator, test, human) behind the same table/signature; conditioning rule is the analyst's LogAffinePreconditioner/pipeline, tested; configurations enter the predictive fit (predictive.py, docs prediction.md). Instruction-like."

[[claim]]
id = "C109"
fragment = "the package documentation is the user's guide"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["file:docs/user-guide/overview.md", "test:tests/test_docs.py::test_runnable_blocks_exist_where_the_guide_promises_them"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Docs has a user-guide section (mkdocs nav User guide, docs/user-guide/*.md) with executed runnable blocks; the sentence names where to look (pointer/intent)."

[[claim]]
id = "C110"
fragment = "Beyond one facet, K > 1 is built"
file = "paper/paper.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_n_terms_above_one_is_implemented", "test:tests/test_estimator.py::test_k_terms_recovers_planted_facets"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "n_terms=2 fits exponents_ of shape (2,3); K=3 recovers planted facets"

[[claim]]
id = "C111"
fragment = "GGP-compatible kernels, the generalization the search motivates"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L16.31"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "scope/intent; L16.31 shows the fixed-weight objective is a generalized posynomial (I15); 'kernels' are a stated direction, 'the search motivates' is the paper's own reading"

[[claim]]
id = "C112"
fragment = "needs a convergence theorem, and Q2 to Q4 need their own conditions"
file = "paper/paper.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L15"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L15 docstring states it does NOT prove convergence; the sentence is a statement of what is open (scope)"

[[claim]]
id = "C113"
fragment = "Work was done in supervisor-gated work packages: a written scope the author approved before execution, and a review afterwards."
file = "paper/paper.ipynb"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "The author's own account of how the work was run (scope, approval, review), worded as process; work-packages/README.md records it; mark as reading in the register."

[[claim]]
id = "C114"
fragment = "AI coding assistance (Claude Code, Anthropic) drafted code, derivation scripts and text inside those packages"
file = "paper/paper.ipynb"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "The author's own account of tool use; worded as his experience; mark as reading."

[[claim]]
id = "C115"
fragment = "compiled from `glossary.yaml` and never typed"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["gen:paper/generate_register.py::register_table", "test:tests/test_paper.py::test_register_table_equals_the_glossary", "test:tests/test_paper.py::test_register_committed_output_is_current"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "register_table builds the table from glossary.yaml; tests check rows equal entries and the committed output is current; appendix cell only imports from the generator (test_appendix_cells_import_from_the_generators)"

[[claim]]
id = "C116"
fragment = "every facet is fitted against every design, each offset"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_corollary_bound_on_every_planted_fit", "test:tests/test_solvers.py::test_r1_planted_certificates"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Offsets use LME of full U@w_k for each facet; the linear part uses the facet's own rows; test pins the all-rows offset."

[[claim]]
id = "C117"
fragment = "each offset $\\beta_k=J_\\tau(Uw_k)$ being the support over all rows"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_corollary_bound_on_every_planted_fit", "test:tests/test_solvers.py::test_r1_planted_certificates", "test:tests/test_solvers.py::test_terms_k1_equals_slsqp_and_degenerate"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Test recomputes log_mean_exp(U @ W[k], tau) over all rows and matches the objective; offset_residual <= 1e-12."

[[claim]]
id = "C118"
fragment = "The alternation takes weights from the current model and then solves one program for all terms"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/solvers.py::soft_weights", "lemma:L16.11", "test:tests/test_soft_fit.py::test_r1_the_soft_objective_never_rises_across_the_history"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Soft path _solve_terms_soft takes softmax weights of the current model then refits; 'one program' is L16's formulation (code refits per term, which the fixed weights allow)"

[[claim]]
id = "C119"
fragment = "The package uses the sharp limit of the weights, one label per design"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_soft_fit.py::test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone", "test:tests/test_soft_fit.py::test_r3_the_limit_kappa_to_infinity_is_the_label_fit"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Default term_temperature=inf is the label fit (one argmax label per row)"

[[claim]]
id = "C120"
fragment = "the program then separates into one convex program per term"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["lemma:L16.44", "lemma:L4"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Fixed-weight objective regroups by terms (L16.44), each term a convex soft-max program (L4); code _refit loops per label"

[[claim]]
id = "C121"
fragment = "For each restart the package starts from random centres in the chart"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/solvers.py::solve_terms"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Docstring and code: K random rows are the centres in the Helmert chart; no test pins the initialisation, and 'centres' are random rows"

[[claim]]
id = "C122"
fragment = "if the mean slack rose, stop with the previous state"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_guard_stop_returns_the_consistent_previous_state"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Guard rejects a rise beyond GUARD_TOL and returns the previous state"

[[claim]]
id = "C123"
fragment = "the fixed-weight objective bounds the soft model's mean slack from above and equals it at the model the weights came from"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L16.43", "lemma:L16.41"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "F <= G_alpha - E with equality at x = x0; fixed-weight objective is G_alpha less the constant E (same minimizers)"

[[claim]]
id = "C124"
fragment = "it is a generalized posynomial in $e^{w}$, so its minimization is a generalized geometric program"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L16.49", "lemma:L16.31"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Generalized posynomial in exp(w) by I15 (inherited); GGP conclusion rests on I15"

[[claim]]
id = "C125"
fragment = "a generalized geometric program in the sense of Boyd et al. [@boyd2007tutorial]"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "L"
backing = ["bib:boyd2007tutorial", "file:paper/reading_pass.yaml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass.yaml row n 37, verdict supported (sect. 5.3 generalized posynomials)"

[[claim]]
id = "C126"
fragment = "L16 does not prove that the alternation converges."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L16"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Stated as a non-result in the L16 docstring ('What this does NOT prove'); not a tagged step"

[[claim]]
id = "C127"
fragment = "the gradient and the Hessian $D-\\kappa M$ of its objective"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L17.34", "lemma:L17.35"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Gradient L17.34, Hessian V'DV - kappa V'MV L17.35"

[[claim]]
id = "C128"
fragment = "the second-order test that certifies a strict local minimizer"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "M"
backing = ["lemma:L17.44"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "KKT plus positive definiteness on the face gives a strict local minimizer (I16)"

[[claim]]
id = "C129"
fragment = "The label belongs to the package and not to the model"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis", "file:work-packages/interface-contract.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "facet_ is argmax over the fitted scores, analysis not part of the model; contract: facet_ stays the analysis by the dominant term"

[[claim]]
id = "C130"
fragment = "which facet dominates a design is analysis of the fitted model"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "P"
backing = ["test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis", "file:work-packages/interface-contract.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Same backing as C053; kind P but a statement about the package"

[[claim]]
id = "C131"
fragment = "The repository keeps:** the SysML model file, the evaluation code, the experiment ledger and the data."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_paper.py::test_each_attribute_has_a_producer_that_exists_in_its_file", "test:tests/test_paper.py::test_c_committed_output_is_current"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "SysML model, evaluation code (adcs_sim.py, cubesat_model.py) read by the producer test; ledger and data read by datasets() whose output the committed-output test pins; a scope statement"

[[claim]]
id = "C132"
fragment = "`certified`: the assignment is fixed, residuals and gaps are within tolerance, no facet is empty and the margin is positive; levels 1 to 3 hold."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/solvers.py::Termination", "test:tests/test_estimator.py::test_termination_record_for_k_terms", "file:work-packages/interface-contract.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Termination docstring and contract define certified as stated; test pins certified with max_gap<=EPS_KKT and zero assignment changes; the 'levels 1 to 3' mapping is documentation (estimator termination_ docstring), not asserted"

[[claim]]
id = "C133"
fragment = "`stationary_without_margin`: the same with a zero margin or an empty facet; levels 1 and 2 only."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/solvers.py::Termination", "test:tests/test_estimator.py::test_termination_record_for_k_terms", "test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "seed-1 case pins stationary_without_margin; the empty-facet test only asserts status != certified, not the label; levels mapping is documentation"

[[claim]]
id = "C134"
fragment = "`uncertified`, `guard_stop` and `iteration_cap`: level 1 only, reported apart from certified."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/solvers.py::Termination", "test:tests/test_solvers.py::test_iteration_cap_status", "test:tests/test_solvers.py::test_guard_stop_returns_the_consistent_previous_state", "test:tests/test_estimator.py::test_convergence_warning_keyed_to_iteration_cap"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "statuses pinned and warned (reported apart from certified); 'level 1 only' is documentation, not asserted; uncertified status itself has no named test"

[[claim]]
id = "C135"
fragment = "`not_applicable`: a penalty, the tangent step or a single facet; the gaps are diagnostics."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/solvers.py::Termination", "test:tests/test_solvers.py::test_not_applicable_statuses", "test:tests/test_soft_fit.py::test_r7_a_soft_fit_at_infinite_tau_is_not_applicable"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "tangent step, penalty, single facet and soft fit at tau=inf all asserted not_applicable; 'gaps are diagnostics' is in the docstring and test_estimator K=1 case (finite max_gap)"

[[claim]]
id = "C136"
fragment = "The record also holds the maximal gap, the Corollary bound, the margin, the stable radius and the shares."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/solvers.py::Termination", "file:work-packages/interface-contract.toml", "test:tests/test_interface_contract.py::test_r1_termination_fields_statuses_and_report_fields"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "the Termination fields (max_gap, bound, gamma, radius, shares) are the contract's pinned termination_fields, checked against the class"

[[claim]]
id = "C137"
fragment = "says that refitting a facet on its own rows is ill-posed"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "R"
backing = ["gen:paper/generate_results.py::own_rows_refit", "test:tests/test_paper.py::test_the_claims_of_c1_have_their_true_basis"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "meta-sentence about what Section 'Results' says; the test asserts 'ill-posed (observed on planted data' and 'D.13' in Results, and that D.13 shows 0 of 60 against 60 of 60"

[[claim]]
id = "C138"
fragment = "The temperature is selected afresh at each K"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_k_terms_case.py::test_tau_reselected_at_each_k_holds_the_fraction", "func:examples/adcs/case.py::k_fits"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "k_fits re-selects the temperature at each K; the test asserts the temperature per K equals the re-selected one and the fraction above V=1 is held"

[[claim]]
id = "C139"
fragment = "`mean_slack_` is defined for every K and is comparable across K at one temperature; `objective_` is the soft maximum at one term and the mean slack at several, and is not."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized", "test:tests/test_case.py::test_mean_slack_by_k_reads_the_estimator_and_the_fixed_tau_refit_shares_one_temperature"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "definitions pinned (mean_slack_ at K=1 and K>1, objective_ = soft max at one term, mean slack at several); 'comparable at one temperature' is the design reading of the definition"

[[claim]]
id = "C140"
fragment = "The tension report runs a principal component analysis on the chart coordinates Z of a facet's near-frontier designs."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions", "test:tests/test_case.py::test_pca_directions_are_the_tension_reports_own_principal_directions"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "the report's directions equal orient_by_pca of the chart coordinates of the near-frontier rows"

[[claim]]
id = "C141"
fragment = "Its directions say along which combinations of metrics the near-frontier designs vary the most"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "M"
backing = ["test:tests/test_tensions.py::test_first_direction_recovers_planted_spread"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "gloss of what a principal direction is (largest variance); no lemma step, the test recovers a planted spread direction and maps loadings back to metrics through the chart basis"

[[claim]]
id = "C142"
fragment = "the fit says which metrics bind, the analysis says where the sampled designs spread along the fitted surface."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "M"
backing = ["test:tests/test_tensions.py::test_contending_set_recovers_planted_support", "test:tests/test_tensions.py::test_first_direction_recovers_planted_spread"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "gloss of the two analyses' roles; the contending set is the support of w, the PCA is of near-frontier chart coordinates; stated as intent, 'binds' is the reading (G-12)"

[[claim]]
id = "C143"
fragment = "the second is computed from the first's coordinates"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "the test builds the chart coordinates from est.transform (the fit) and reproduces the report's directions"

[[claim]]
id = "C144"
fragment = "The sign of a direction is arbitrary; each is shown with its largest loading positive."
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_case.py::test_pca_directions_are_the_tension_reports_own_principal_directions", "func:examples/adcs/case.py::pca_directions"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "pca_directions flips the sign so the largest-magnitude loading is positive; the test asserts '+' on the first listed loading"

[[claim]]
id = "C145"
fragment = "The repository keeps:** the long review with its dropped candidates"
file = "paper/supporting_material.ipynb"
anchor = ""
kind = "S"
backing = ["test:tests/test_paper_sources.py::test_the_six_snapshots_and_the_move_table_exist", "file:docs/superpowers/notes/paper-sources/literature.md", "file:docs/references.bib"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "literature.md exists (test) with Appendix A \"candidates dropped or limited\"; references.bib holds the adopted sources (test_references checks hygiene)."

[[claim]]
id = "C146"
fragment = "learns the shape of a design trade space from evaluated designs"
file = "docs/index.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_recovery_tau_inf", "test:tests/test_estimator.py::test_recovery_tau_1e3"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Planted frontier exponents and offset are recovered from evaluated designs; the phrase is a gloss of fit."

[[claim]]
id = "C147"
fragment = "model in the posynomial invariant form. It then tells you which metrics contend"
file = "docs/index.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_contending_set_recovers_planted_support", "test:tests/test_estimator.py::test_fit_invariants", "test:tests/test_estimator.py::test_recovery_tau_inf"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Fit of the frontier model (exponents, offset) pinned by recovery/invariants tests; the tension report is the 'which metrics contend' part (C003)."

[[claim]]
id = "C148"
fragment = "It then tells you which metrics contend, at what exchange"
file = "docs/index.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_contending_set_recovers_planted_support", "test:tests/test_tensions.py::test_exponents_and_elasticities_consistent"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Contending set recovers planted support; elasticities R[j,k] = -w_k/w_j pin the exchange rate."

[[claim]]
id = "C149"
fragment = "rate, where each design sits relative to the fitted reference surface"
file = "docs/index.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples", "test:tests/test_estimator.py::test_project_and_improvement_factors_land_on_frontier"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "score_samples/log V is the design's level relative to the fitted surface V=1; chart and V=1 projection pinned."

[[claim]]
id = "C150"
fragment = "and where the table has gaps"
file = "docs/index.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_gaps.py::test_find_holes_2d_planted_disc", "test:tests/test_gaps.py::test_find_holes_1d_planted_gap", "test:tests/test_gaps.py::test_knn_flags_isolated_point"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Planted holes in the chart are located; gaps are gaps in ratio profiles (gaps.py docstring), the gloss 'gaps in the table' is a fair short form."

[[claim]]
id = "C151"
fragment = "It is a scikit-learn estimator (`fit`, `transform`, `inverse_transform`, `score_samples`) in the"
file = "docs/index.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score", "test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples", "test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Methods exist and behave as a transformer; parametrize_with_checks passes; class is TransformerMixin+BaseEstimator."

[[claim]]
id = "C152"
fragment = "unsupervised and feature-engineering family, beside PCA"
file = "docs/index.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator", "test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score", "test:tests/test_estimator.py::test_pipeline_and_feature_names"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Transformer API with no predict, composes in Pipeline/ColumnTransformer; 'family beside PCA' is classification (decomposition-family semantics) backed by the conformance tests."

[[claim]]
id = "C153"
fragment = "The idea is easiest to see with two of the metrics, where the model is a line."
file = "docs/getting-started.md"
anchor = ""
kind = "M"
backing = ["lemma:L1", "test:tests/test_plotting.py::test_log_plane_draws_frontier_line_in_black_and_band_in_grey"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "log V = w.u - beta, so V=1 is a line in the log plane when d=2; test asserts the drawn line is w.u = beta"

[[claim]]
id = "C154"
fragment = "`fit` learned one exponent per metric, summing to one."
file = "docs/getting-started.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_fit_invariants"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "asserts exponents_ shape (1,d) and sum to 1 (nonnegative) at tau inf, 10, 1e3"

[[claim]]
id = "C155"
fragment = "summing to one. `report.contending_set` lists the metrics that"
file = "docs/getting-started.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_contending_set_recovers_planted_support", "func:src/hyperbolic_trade_space/tensions.py::tension_report"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "contending_set equals the planted support across sizes 2 to 5"

[[claim]]
id = "C156"
fragment = "The set is found from the data and not chosen in advance."
file = "docs/getting-started.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_contending_set_recovers_planted_support", "test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "set recovered from the data (tau=inf LP) without being supplied"

[[claim]]
id = "C157"
fragment = "fitted weights at the working temperature; their ratios are the elasticities between the contending"
file = "docs/getting-started.md"
anchor = ""
kind = "M"
backing = ["lemma:L7", "test:tests/test_tensions.py::test_exponents_and_elasticities_consistent"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L7 elasticities are ratios of exponents along a facet; test pins report.elasticities against report.exponents; ratios of working-tau weights as elasticities assumed from L7, not separately stepped at finite tau"

[[claim]]
id = "C158"
fragment = "`ts.score_samples(X)` is the log of V for each design, the energy"
file = "docs/getting-started.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples", "lemma:L1", "glossary:energy-differential"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "last chart column equals score_samples; log V = w.u - beta by L1"

[[claim]]
id = "C159"
fragment = "is the chart, `d - 1` position coordinates plus that log V, and `ts.inverse_transform` undoes it."
file = "docs/getting-started.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples", "lemma:L8"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "T has d columns (d-1 coordinates plus log V last) and inverse_transform(T)==X"

[[claim]]
id = "C160"
fragment = "From there the guide follows the order of a study: [fit](user-guide/fitting.md),"
file = "docs/getting-started.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_site.py::test_docs_relative_links_resolve", "test:tests/test_site.py::test_nav_pages_exist_and_cover_the_contract_pages"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "guide pages exist and links resolve; the sentence is a pointer to the guide order (instruction), nav order in mkdocs.yml"

[[claim]]
id = "C161"
fragment = "The package follows the scikit-learn conventions [@pedregosa2011scikit; @buitinck2013api]: parameters"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator", "test:tests/test_sklearn_compat.py::test_init_stores_parameters_verbatim"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "parametrize_with_checks plus verbatim-params test; the citations are the conventions' sources"

[[claim]]
id = "C162"
fragment = "validation in `fit`, fitted attributes ending in an underscore."
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_fitted_attributes_end_in_underscore_and_n_iter_positive", "test:tests/test_preconditioning.py::test_parameter_validation_in_fit"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "underscore test asserts all new attrs end in _; validation in fit pinned for the preconditioner and by the sklearn checks for the estimator"

[[claim]]
id = "C163"
fragment = "Dimension is arbitrary: `d` metrics and `d - 1` chart coordinates."
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_coordinates.py::test_helmert_orthonormal_kernel", "test:tests/test_datasets.py::test_d1", "test:tests/test_estimator.py::test_d1"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "helmert basis is (d-1,d) for d 2..8; d=1 handled; arbitrary d shown over a range, not literally every d"

[[claim]]
id = "C164"
fragment = "[`frontier_in_original_units`](user-guide/conditioning.md), a function: the fitted surface as a"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples", "func:src/hyperbolic_trade_space/preconditioning.py::frontier_in_original_units"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "returns exponents_orig, log_const, shift; log V in raw attributes equals pipeline score_samples"

[[claim]]
id = "C165"
fragment = "[`HyperbolicTradeSpace`](user-guide/fitting.md), a transformer: fits the surface and gives the"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_recovers_planted_coordinates", "test:tests/test_estimator.py::test_d1", "test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "transform gives (Z, log V) chart (inverse_transform of column_stack([Z, log_v]) in the predictive test)"

[[claim]]
id = "C166"
fragment = "chart of position and log V. Fitted attributes for every number of terms include `exponents_`,"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_attributes_exist_for_every_k_and_k1_numbers_are_unchanged", "test:tests/test_estimator.py::test_k_terms_attributes_conventions", "test:tests/test_interface_contract.py::test_r1_estimator_methods_and_fitted_attributes"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "exponents_, facet_, coefficients_, facet_share_ exist at K=1 and K>1"

[[claim]]
id = "C167"
fragment = "`facet_`, `coefficients_`, `facet_share_`, `objective_` (what the solver minimized) and"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized", "test:tests/test_estimator.py::test_attributes_exist_for_every_k_and_k1_numbers_are_unchanged"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "objective_ and mean_slack_ at K=1 and K=2; the test asserts the solver-minimized quantity per K"

[[claim]]
id = "C168"
fragment = "`mean_slack_` (the mean slack, to compare fits across numbers of terms)."
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized", "test:tests/test_case.py::test_mean_slack_by_k_reads_the_estimator_and_the_fixed_tau_refit_shares_one_temperature"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "mean_slack_ defined for every K; comparison across K at a shared temperature is what the case test does (the gloss 'to compare' is intent)"

[[claim]]
id = "C169"
fragment = "[`select_temperature`](user-guide/fitting.md), a function: chooses the temperature by a target"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tuning.py::test_selected_temperature_hits_target", "func:src/hyperbolic_trade_space/tuning.py::select_temperature"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "tests assert frac_above_ within 0.01 of target"

[[claim]]
id = "C170"
fragment = "[`make_frontier_data`](user-guide/fitting.md), a function: seeded synthetic data with a planted"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_datasets.py::test_frontier_info_and_planting", "test:tests/test_datasets.py::test_reproducible_and_noise"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "seeded reproducibility and planted frontier"

[[claim]]
id = "C171"
fragment = "[`make_configured_frontier_data`](user-guide/prediction.md), a function: the same with"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_datasets.py::test_configured"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "configured data with config_map to (Z, log V), reproducible by seed"

[[claim]]
id = "C172"
fragment = "[`tension_report`](user-guide/tensions.md), a function: contending set, elasticities and"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_contending_set_recovers_planted_support", "test:tests/test_tensions.py::test_exponents_and_elasticities_consistent", "test:tests/test_tensions.py::test_first_direction_recovers_planted_spread"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "report carries contending set, elasticities, tension directions"

[[claim]]
id = "C173"
fragment = "[`TradeSpaceRegressor`](user-guide/prediction.md), a regressor: metrics, coordinates and novelty"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_recovers_planted_coordinates", "test:tests/test_predictive.py::test_novelty_beyond_the_soft_frontier"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "predict (metrics), predict_coordinates and predict_novelty from configuration"

[[claim]]
id = "C174"
fragment = "`hyperbolic_trade_space.tensions`: `TensionReport`, the object `tension_report` returns."
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_interface_contract.py::test_r1_termination_fields_statuses_and_report_fields", "func:src/hyperbolic_trade_space/tensions.py::tension_report"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "TensionReport is in tensions and tension_report returns it (test_tensions asserts report fields)"

[[claim]]
id = "C175"
fragment = "`hyperbolic_trade_space.solvers`: the multi-term solver, the `Termination` record and the"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_interface_contract.py::test_r1_submodule_importable_with_pinned_names", "test:tests/test_interface_contract.py::test_r1_termination_fields_statuses_and_report_fields"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "solve_terms and Termination pinned in the solvers contract list"

[[claim]]
id = "C176"
fragment = "certificate functions, with `min_curvature` for a soft fit"
file = "docs/api.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_interface_contract.py::test_r1_certificate_signatures_exact", "test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "certificate functions pinned; min_curvature is a Termination field set for a soft fit (nan otherwise, test_soft_fit)"

[[claim]]
id = "C177"
fragment = "Because the weights sum to one, $V(\\lambda m)=\\lambda V(m)$: doubling every metric doubles V."
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L1.5", "glossary:invariant-value"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L1.5 states V(km)=kV(m) using sum w=1"

[[claim]]
id = "C178"
fragment = "extends one term to K terms and keeps the programs inside geometric programming."
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L10.7", "lemma:L16.49", "glossary:generalized-posynomial"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L10.7 the K-term model is a posynomial; L16.49 the fixed-weight multi-term objective is a generalized posynomial (GGP)"

[[claim]]
id = "C179"
fragment = "so the surface V = 1 is where the posynomial equals one."
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L10.7", "glossary:posynomial"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V_K is the 1/kappa power of the posynomial (L10.7, glossary), so V=1 iff posynomial = 1"

[[claim]]
id = "C180"
fragment = "Fitting one facet is a geometric program (GP), solved as"
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L4.24", "glossary:geometric-program"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L4.17-L4.24: posynomial objective, monomial equality/inequalities, convex in log variables (declared I13)"

[[claim]]
id = "C181"
fragment = "fitting several facets alternates weights from"
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L16.49", "lemma:L16.48", "lemma:L15.16"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Weights from the current model fixed gives one GGP over all terms (L16.48-49); sharp-label reassign-then-refit is L15; the alternation loop itself is the algorithm"

[[claim]]
id = "C182"
fragment = "The package takes the sharp limit of the weights, one"
file = "docs/theory.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_soft_fit.py::test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone", "test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis", "file:work-packages/interface-contract.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Default term_temperature is inf (sharp); facet_ is one argmax label per design"

[[claim]]
id = "C183"
fragment = "which facet dominates a design is analysis of the fitted model, not part of the fit."
file = "docs/theory.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_soft_fit.py::test_r6_analysis_stays_analysis", "glossary:assignment"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "test pins facet_ as argmax of the fitted scores, computed from the model (analysis)"

[[claim]]
id = "C184"
fragment = "With one term this is a convex program."
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L4.13", "lemma:L4.24"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L4.13 J_tau convex in w; L4.23-24 the one-term problem is a convex program"

[[claim]]
id = "C185"
fragment = "the same fit at tau = infinity: the exact maximum, a linear program,"
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L5.24", "lemma:L12.31", "glossary:supporting-envelope"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L5.24 LME -> max as tau -> inf; L12.31 the LP gap at tau=inf; glossary supporting-envelope"

[[claim]]
id = "C186"
fragment = "The fit does not identify the other two with it."
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L11", "glossary:pareto-boundary", "glossary:supporting-envelope"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L11 docstring: maximizer of V is efficient, converse not proven, nothing claimed about the fitted frontier being the true front; statement of what is not claimed"

[[claim]]
id = "C187"
fragment = "Inside the surface V < 1; beyond it V > 1, and V - 1 says by how much."
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L1.7", "glossary:energy-differential"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L1.7 log V = w.u - beta, so V<1 / V>1 are the sides of the surface; V-1 is the relative excess by definition"

[[claim]]
id = "C188"
fragment = "the level surface is flat in log space, so moving along it trades"
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L7.5", "lemma:L1.7", "glossary:elasticity"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L7.5 dlog m_j0/dlog m_k0 = -w_k0/w_j0 along the tangent at constant V"

[[claim]]
id = "C189"
fragment = "It is found from the data and not assumed: the fit at"
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact", "glossary:contending-set", "glossary:n-lemma"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Contending set computed from the tau=inf fit and pinned for planted supports of size 3; found from data is the design of tension_report"

[[claim]]
id = "C190"
fragment = "temperature a small weight means weak participation, set by a participation threshold."
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact", "glossary:participation-threshold"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Test: weights on free metrics below half the members' weights; participation depends on threshold"

[[claim]]
id = "C191"
fragment = "terms there is one contending set per facet, and elasticities vary between facets."
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["test:tests/test_tensions.py::test_k3_reports_one_per_facet_recover_planted_supports", "glossary:contending-set"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "K=3 returns one report per facet recovering planted supports; per-facet elasticities follow from L7.5 with facet-specific w"

[[claim]]
id = "C192"
fragment = "at one term the elasticities are constant; designs are chosen by an evaluator and not drawn from"
file = "docs/theory.md"
anchor = ""
kind = "M"
backing = ["lemma:L7.5", "lemma:L10.9"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Constant elasticities at K=1: L7.5 with L10.9 (Phi_1 monomial); second clause is a statement of the sampling assumption (scope)"

[[claim]]
id = "C193"
fragment = "A tutorial on geometric programming [@boyd2007tutorial]: posynomials and generalized posynomials,"
file = "docs/further-reading.md"
anchor = ""
kind = "L"
backing = ["bib:boyd2007tutorial"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n37 supported (GP definitions, generalized posynomials sect. 5.3)"

[[claim]]
id = "C194"
fragment = "the family the multi-term fit stays inside."
file = "docs/further-reading.md"
anchor = ""
kind = "M"
backing = ["lemma:L10", "lemma:L16.49", "bib:boyd2007tutorial"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L10 step 4: exp(kappa Phi_K) is a posynomial in m; L16.49: soft-fit fixed-weight objective is a generalized posynomial"

[[claim]]
id = "C195"
fragment = "Fitting softmax-affine functions to data so they remain compatible with geometric programming"
file = "docs/further-reading.md"
anchor = ""
kind = "L"
backing = ["bib:hoburg2016data"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n39 supported from the abstract (full text not obtained)"

[[claim]]
id = "C196"
fragment = "Fitting convex piecewise-linear functions by alternating partition and refit [@magnani2009convex]:"
file = "docs/further-reading.md"
anchor = ""
kind = "L"
backing = ["bib:magnani2009convex"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n40 supported: alternating assignment and refit"

[[claim]]
id = "C197"
fragment = "Reweighted $\\ell_1$ minimization [@candes2008enhancing]: the sparsity option,"
file = "docs/further-reading.md"
anchor = ""
kind = "L"
backing = ["bib:candes2008enhancing"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n41 supported: sequence of reweighted l1 problems"

[[claim]]
id = "C198"
fragment = "minimization [@candes2008enhancing]: the sparsity option, `penalty=\"reweighted_l1\"`."
file = "docs/further-reading.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_reweighted_l1_gives_exact_zeros_on_planted_sparse_facet", "test:tests/test_estimator.py::test_penalty_gives_exact_zero_exponents_at_the_estimator"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "penalty=\"reweighted_l1\" exists and sparsifies exponents at solver and estimator"

[[claim]]
id = "C199"
fragment = "the second source of the multi-term fit."
file = "docs/further-reading.md"
anchor = ""
kind = "L"
backing = ["bib:magnani2009convex"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "refit scheme as sentence in n40 and prior_art gp-maxaffine 'K > 1 refit scheme'; 'second source' is the author's attribution of the scheme, same caveat as C006 is lighter since the abstract describes the scheme"

[[claim]]
id = "C200"
fragment = "Kernel PCA [@schoelkopf1998nonlinear]: the kin of the documented kernel direction, which is not"
file = "docs/further-reading.md"
anchor = ""
kind = "L"
backing = ["bib:schoelkopf1998nonlinear"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n43 supported: kernel PCA via feature spaces"

[[claim]]
id = "C201"
fragment = "HoroPCA [@chami2021horopca]: principal component analysis in hyperbolic space, which this package"
file = "docs/further-reading.md"
anchor = ""
kind = "L"
backing = ["bib:chami2021horopca"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass n44 supported: HoroPCA, PCA generalized to hyperbolic space"

[[claim]]
id = "C202"
fragment = "analysis, the nearest neighbour outside engineering design."
file = "docs/further-reading.md"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "'nearest neighbour outside engineering design' is the author's judgment (n17 'closer cousin' is judgment); register as reading"

[[claim]]
id = "C203"
fragment = "PCA finds the directions in which the data spread;"
file = "docs/user-guide/overview.md"
anchor = ""
kind = "M"
backing = ["bib:jolliffe2016principal"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass.yaml PCA table row (maximize variance successively) supported; textbook gloss"

[[claim]]
id = "C204"
fragment = "The answer is one weight per metric, the"
file = "docs/user-guide/overview.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_fit_invariants", "test:tests/test_tensions.py::test_exponents_and_elasticities_consistent"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "fit returns one exponent per metric on the simplex, min and sum asserted"

[[claim]]
id = "C205"
fragment = "found from the data, so you need not know in advance which dilemma or trilemma your problem holds."
file = "docs/user-guide/overview.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_contending_set_recovers_planted_support"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "contending set recovered from data on planted supports (size 1,2,3); backing is planted data, not a general guarantee, claim worded modestly"

[[claim]]
id = "C206"
fragment = "The weights define a score V, a weighted geometric mean of the metrics."
file = "docs/user-guide/overview.md"
anchor = ""
kind = "M"
backing = ["lemma:L1", "glossary:invariant-value"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V = prod m_j^w_j = exp(sum w_j log m_j)"

[[claim]]
id = "C207"
fragment = "V = 1 is the fitted reference surface,"
file = "docs/user-guide/overview.md"
anchor = ""
kind = "M"
backing = ["lemma:L1"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "corollary: V(m/e^beta)=1 exactly when V(m)=e^beta; also test_uniform_rescaling_shifts_beta"

[[claim]]
id = "C208"
fragment = "Because V scales with the metrics, it reads as a factor of improvement."
file = "docs/user-guide/overview.md"
anchor = ""
kind = "M"
backing = ["lemma:L1", "lemma:L7"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V(km)=kV(m) (L1) and uniform improvement by V^-1 reaches V=1 (L7)"

[[claim]]
id = "C209"
fragment = "the weights and the metrics that participate;"
file = "docs/user-guide/overview.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_exponents_and_elasticities_consistent", "test:tests/test_tensions.py::test_contending_set_recovers_planted_support"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "tension_report exposes weights (exponents) and participating mask, asserted"

[[claim]]
id = "C210"
fragment = "its energy differential (level offset) to the fitted reference surface and its"
file = "docs/user-guide/overview.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples", "test:tests/test_coordinates.py::test_round_trip_and_invariance"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "score_samples (level) and transform (position along surface) with exact round trip; 'energy differential' is the glossary name for log V"

[[claim]]
id = "C211"
fragment = "how much one metric alone would need to improve to reach the surface;"
file = "docs/user-guide/overview.md"
anchor = ""
kind = "S"
backing = ["lemma:L7", "test:tests/test_estimator.py::test_project_and_improvement_factors_land_on_frontier"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "improvement_factors f=V^(-1/w_j) reaches V=1; test checks landing on frontier"

[[claim]]
id = "C212"
fragment = "a novelty score and candidate white space;"
file = "docs/user-guide/overview.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_novelty_score", "test:tests/test_gaps.py::test_find_holes_2d_planted_disc"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "novelty_score and find_holes (white space) tested; 'candidate' wording fits"

[[claim]]
id = "C213"
fragment = "the surface written back in your original attribute units;"
file = "docs/user-guide/overview.md"
anchor = ""
kind = "S"
backing = ["lemma:L9", "test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "frontier_in_original_units reproduces score_samples exactly under log-affine conditioning"

[[claim]]
id = "C214"
fragment = "a stopping record, [`termination_` and `conditioning_`](termination.md), saying how far to trust"
file = "docs/user-guide/overview.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_termination_record_for_k_terms", "test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "termination_ and conditioning_ attributes exist and are tested; 'how far to trust' is the intended reading"

[[claim]]
id = "C215"
fragment = "The fit consumes a strictly positive matrix of larger-is-better metrics."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Preconditioner output is strictly positive larger-is-better (M>0 asserted); zeros tolerated is stated later on the page and tested separately"

[[claim]]
id = "C216"
fragment = "attributes: kilograms, dollars, error rates, counts, some of them better when small."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Description of what attributes look like in practice; the author's own framing"

[[claim]]
id = "C217"
fragment = "which implements the family of maps the method allows,"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_fitted_attributes_and_larger_is_better_direction", "func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Test pins log m = (o log(X+shift) - offset)/scale; the log-affine family"

[[claim]]
id = "C218"
fragment = "`frontier_in_original_units`, which reports the fitted surface back in the units you started with."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples", "func:src/hyperbolic_trade_space/preconditioning.py::frontier_in_original_units"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Pulled-back log V equals the pipeline score_samples on raw rows"

[[claim]]
id = "C219"
fragment = "smaller-is-better attribute is inverted in log space and comes out larger-is-better."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_fitted_attributes_and_larger_is_better_direction"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Asserts negative correlation of metric with raw attribute for orientation -1 (inverted, larger-is-better)"

[[claim]]
id = "C220"
fragment = "The cheap diagnostic is the sign of the pulled-back exponent below."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Test asserts exponents_orig * orientation >= 0, so exponent sign follows orientation (w_j >= 0)"

[[claim]]
id = "C221"
fragment = "`shift` moves the argument to `a + shift`; it must keep every"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_negative_after_shift_raises", "func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Shift 0.5 on a value of -1 raises; shift 1.0 (zero after shift) allowed"

[[claim]]
id = "C222"
fragment = "value nonnegative, and `ValueError` with \"Negative values in data\" is raised otherwise."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_negative_after_shift_raises"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "match=\"Negative values in data\" on fit, transform, inverse_transform"

[[claim]]
id = "C223"
fragment = "The reference point is the attribute value that maps to metric 1; it is the centre removed by the"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_fitted_attributes_and_larger_is_better_direction", "func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Test pins log m = (z - log_offset_)/log_scale_, so offset is the z mapping to metric 1; the V = 1 gloss is intent"

[[claim]]
id = "C224"
fragment = "scaler and stored as `log_offset_`. It fixes what V = 1 means in practice."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_fitted_attributes_and_larger_is_better_direction"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Same test; log_offset_ is the centre removed by the scaler; second sentence is a gloss"

[[claim]]
id = "C225"
fragment = "a scaler is fitted per column. `scaler=\"standard\"` gives each metric unit"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_unit_log_standard_deviation", "func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "std of log M is 1 per column (doctest too); scaler fitted per column"

[[claim]]
id = "C226"
fragment = "normalizes the interquartile range instead and suits data where a"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_robust_normalizes_log_iqr_and_ignores_zeros"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Log IQR is 1 for robust; the 'suits data with extreme designs' is advice"

[[claim]]
id = "C227"
fragment = "works if it is affine per column. The reason to scale is the temperature of the next page: it is"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Round trip with a MinMaxScaler instance; docstring requires affine per column; the rationale sentence is covered under the temperature claim"

[[claim]]
id = "C228"
fragment = "An entry at exactly `-shift` maps to metric 0, and the scaler ignores it."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_zero_after_shift_maps_to_zero_and_inverts_to_minus_shift", "test:tests/test_preconditioning.py::test_zeros_map_to_zero_and_invert"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "X+shift==0 maps to 0 and the scale equals that of the fit without the entry"

[[claim]]
id = "C229"
fragment = "An entry at exactly `-shift` maps to metric 0, and the scaler ignores it. The estimator tolerates"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_zero_metric_row"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Fit with a zero-metric row leaves exponents unchanged"

[[claim]]
id = "C230"
fragment = "such a row has V = 0 and no support weight,"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_zero_metric_row"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Asserts invariant_value == 0 and support_weights_ == 0 for the row"

[[claim]]
id = "C231"
fragment = "and its chart coordinates are `nan`."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_zero_metric_row", "test:tests/test_coordinates.py::test_minus_inf_rows"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Transform coordinates are nan for the zero row"

[[claim]]
id = "C232"
fragment = "For a smaller-is-better attribute a raw zero is the best value, so mapping it to metric 0 is"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "M"
backing = ["test:tests/test_preconditioning.py::test_zeros_map_to_zero_and_invert"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Zero maps to metric 0 for orientation -1 (tested); 'best value' is the definition of smaller-is-better and 'bookkeeping not a verdict' is the author's judgment"

[[claim]]
id = "C233"
fragment = "None proves a conditioning right; they show whether the story is sensible."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Author's judgment about diagnostics"

[[claim]]
id = "C234"
fragment = "After `\"standard\"` scaling, `np.log(M).std(axis=0)` is one in every finite column."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_unit_log_standard_deviation", "func:src/hyperbolic_trade_space/preconditioning.py::LogAffinePreconditioner"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Asserts std(log M, axis=0)=1 and doctest; 'finite column' covers zeros ignored by the scaler"

[[claim]]
id = "C235"
fragment = "`inverse_transform(transform(X))` returns `X`; the conditioning is exactly invertible."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_round_trip_mixed_orientation_and_shift", "test:tests/test_preconditioning.py::test_zeros_map_to_zero_and_invert"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Round trip to rtol 1e-10 across scalers, orientations, shifts and zeros; 'exactly' means to floating precision"

[[claim]]
id = "C236"
fragment = "The pulled-back exponent on a raw attribute is `w_j * alpha_j`."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "M"
backing = ["lemma:L9.5"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V = e^{w.b-beta} prod (a_j+r_j)^{w_j alpha_j}; exponent on raw attribute is w_j alpha_j; test_pullback_matches_L9_chain_formula cross-checks"

[[claim]]
id = "C237"
fragment = "contending set moves, the finding depends on the conditioning, and should be reported that way."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Author's advice on reporting sensitivity to conditioning"

[[claim]]
id = "C238"
fragment = "`exponents_orig`, `log_const` and `shift`. The surface is again a monomial, now in the raw"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Asserts set(f) == {exponents_orig, log_const, shift}; 'again a monomial' is L9.5"

[[claim]]
id = "C239"
fragment = "attributes: a negative exponent marks a smaller-is-better attribute."
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "M"
backing = ["lemma:L9.5", "test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Monomial form is L9.5; test asserts exponent*orientation >= 0 so negative exponent implies orientation -1 (w_j >= 0)"

[[claim]]
id = "C240"
fragment = "to get log V for raw rows. The function needs a"
file = "docs/user-guide/conditioning.md"
anchor = ""
kind = "M"
backing = ["lemma:L9.5", "test:tests/test_preconditioning.py::test_pullback_reproduces_pipeline_score_samples"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "The stated expression log_const + exponents_orig @ log(X+shift) is the one tested equal to score_samples"

[[claim]]
id = "C241"
fragment = "problem and returns the minimizer. It follows the scikit-learn decomposition family: `fit`,"
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["lemma:L4", "test:tests/test_solvers.py::test_slsqp_agrees_with_lp", "test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Solver agrees with the exact LP and the planted fit to tolerance; decomposition-family conformance by the sklearn checks."

[[claim]]
id = "C242"
fragment = "`score_samples`, and no `predict`. Parameters are stored as given"
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score", "test:tests/test_sklearn_compat.py::test_init_stores_parameters_verbatim", "test:tests/test_estimator.py::test_invalid_params_raise_in_fit_not_init"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "No predict; score_samples present; params stored verbatim and validated in fit."

[[claim]]
id = "C243"
fragment = "- `exponents_`: shape `(n_terms, d)`, each row on the simplex."
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_fit_invariants", "test:tests/test_estimator.py::test_k_terms_round_trip_and_scores"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Shape (n_terms,d) and simplex at K=1 in the estimator test; K>1 row sums pinned only at solver level (test_solvers::test_terms_deterministic_and_sparse)."

[[claim]]
id = "C244"
fragment = "- `n_eff_`: how many designs carry the fit."
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_k_terms_attributes_conventions", "test:tests/test_tuning.py::test_tau_sweep_is_monotone_from_half_toward_zero"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "n_eff_ = 1/sum p^2 asserted; sweeps from N toward d."

[[claim]]
id = "C245"
fragment = "term and the mean slack at several, so it is not comparable across numbers of terms."
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized", "file:work-packages/interface-contract.md"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "At K=1 objective_ < mean_slack_ (different quantities); contract v3 says objective_ is what the solver minimized and mean_slack_ is the one to compare."

[[claim]]
id = "C246"
fragment = "- `termination_` and `conditioning_`: how the fit stopped and how well its exponents are identified"
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_termination_record_for_k_terms", "test:tests/test_estimator.py::test_conditioning_is_the_restricted_hessian_eigenvalue", "test:tests/test_estimator.py::test_conditioning_drops_for_nearly_collinear_metrics"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Termination status record and conditioning as smallest restricted Hessian eigenvalue, tested."

[[claim]]
id = "C247"
fragment = "The chart's basis, offsets and support weights are `basis_`, `log_offset_` and `support_weights_`."
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples", "test:tests/test_estimator.py::test_fit_invariants"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Names of attributes; basis_ drives the chart round trip, support_weights_ and log_offset_ asserted."

[[claim]]
id = "C248"
fragment = "`min_exponent` (a floor on every exponent) at 0 to"
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["glossary:contending-set", "test:tests/test_estimator.py::test_fit_invariants"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "definition/instruction: contending set is the support at the exact fit; a floor above 0 would hide it; coordinates validated."

[[claim]]
id = "C249"
fragment = "This synthetic table puts 30 percent of its rows on the planted frontier, hence the target 0.35;"
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "R"
backing = ["gen:src/hyperbolic_trade_space/datasets.py::make_frontier_data", "test:tests/test_datasets.py::test_frontier_info_and_planting"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "frontier_fraction default 0.3 pinned (mask.sum()==150 of 500); I confirmed mask mean 0.3 for n=300; 'hence 0.35' is the author's rationale, not asserted."

[[claim]]
id = "C250"
fragment = "A `ValueError` says when `bounds` misses the target."
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tuning.py::test_not_bracketed_raises"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "ValueError 'not bracketed' for bounds on either side of the target."

[[claim]]
id = "C251"
fragment = "Fitting alternates weights from the current model with a refit, from several seeded starts"
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["lemma:L15", "test:tests/test_solvers.py::test_terms_monotone_history_and_stops", "test:tests/test_estimator.py::test_k_terms_zero_rows_and_determinism"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Alternation of assignment and refit with nonincreasing history; seeded restarts deterministic."

[[claim]]
id = "C252"
fragment = "`make_frontier_data(300, 4, n_terms=2, random_state=777)`) and the default target 0.10 raises \"not"
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tuning.py::test_several_terms_unreachable_target_says_what_to_try"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Same table (300,4,n_terms=2,seed 777); default target raises 'not bracketed' (slow-marked test)."

[[claim]]
id = "C253"
fragment = "also returns configuration variables. Both are seeded and used throughout these pages."
file = "docs/user-guide/fitting.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_datasets.py::test_configured"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "random_state seeding tested (same seed same data); 'used throughout these pages' is descriptive"

[[claim]]
id = "C254"
fragment = "returns a frozen `TensionReport` that says which metrics contend and"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_deterministic_frozen_and_validation", "test:tests/test_tensions.py::test_contending_set_recovers_planted_support"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "frozen dataclass asserted (FrozenInstanceError); contending set recovered"

[[claim]]
id = "C255"
fragment = "`plot_tensions` draws the report as a heatmap:"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_plotting.py::test_plot_tensions_with_real_report", "test:tests/test_plotting.py::test_plot_tensions_with_stand_in_report"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "asserts imshow image with tension cmap, 3x3 annotated cells, outlines"

[[claim]]
id = "C256"
fragment = "`contending_set` holds the metrics with positive exponent in the exact-maximum fit (tau = infinity,"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_contending_set_recovers_planted_support", "test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "support of tau=inf LP, 1e-9 cutoff is in code; planted supports recovered"

[[claim]]
id = "C257"
fragment = "`n_lemma` is its size and `lemma_name` names it: monolemma, dilemma,"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_contending_set_recovers_planted_support", "test:tests/test_tensions.py::test_d1_trivial_report"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "n_lemma = support size, names monolemma/dilemma/trilemma/n-lemma pinned"

[[claim]]
id = "C258"
fragment = "The set is found, not assumed: a facet of the achievable region on which"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "M"
backing = ["glossary:n-lemma", "test:tests/test_tensions.py::test_contending_set_recovers_planted_support"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "definition (pointer definition); glossary n-lemma; found-not-assumed shown by planted recovery"

[[claim]]
id = "C259"
fragment = "The report solves the tau = infinity program itself, independent of the"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "contending set same at tau=5 as at inf"

[[claim]]
id = "C260"
fragment = "the report warns when the estimator was fitted with a floor."
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_warns_when_min_exponent_positive", "test:tests/test_tensions.py::test_no_warning_when_min_exponent_zero"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "warning on floor, none without"

[[claim]]
id = "C261"
fragment = "`participating` marks metrics whose exponent exceeds the participation threshold"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_exponents_and_elasticities_consistent", "test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact", "glossary:participation-threshold"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "participating = exponents > threshold; threshold=1e-9 override tested"

[[claim]]
id = "C262"
fragment = "is the elasticity along the surface: the percentage change of metric j per percentage change of"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "M"
backing = ["lemma:L7.5", "glossary:elasticity", "test:tests/test_tensions.py::test_exponents_and_elasticities_consistent"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "d log m_j/d log m_k = -w_k/w_j along F; code entry [j,k]=-w_k/w_j asserted"

[[claim]]
id = "C263"
fragment = "metric k, constant on a facet and `nan`"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "M"
backing = ["lemma:L7.5", "test:tests/test_tensions.py::test_exponents_and_elasticities_consistent"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "ratio of exponents is constant on a facet (L7.5); nan rows tested"

[[claim]]
id = "C264"
fragment = "where metric j does not participate. It"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_exponents_and_elasticities_consistent"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "nan for rows with exponent <= 1e-3 asserted"

[[claim]]
id = "C265"
fragment = "For designs with absolute log V below `band` (by default 1/tau, or 0.1 at infinite tau),"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_band_default_and_report_fields", "test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "band 0.1 at inf, 1/tau finite (0.05 at tau=20); near = |log V| < band asserted"

[[claim]]
id = "C266"
fragment = "`association` is the Pearson or Spearman correlation of the log-metrics: negative is traded, positive"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_association_signs_aligned_and_traded"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "pearson and spearman; aligned > 0.5, traded < -0.5"

[[claim]]
id = "C267"
fragment = "Near the surface the weighted sum of log-metrics is almost constant, so a binding"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "M"
backing = ["lemma:L1"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "log V = w.u - beta (L1), so |log V|<band keeps w.u within band of beta; 'almost constant' is the band reading"

[[claim]]
id = "C268"
fragment = "Three fields describe the spread of the near-frontier designs along the surface:"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_first_direction_recovers_planted_spread"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "fields exist with shapes (d-1,d-1), (d-1,d), (d-1,)"

[[claim]]
id = "C269"
fragment = "`tension_directions`: the principal directions of the near-frontier chart coordinates."
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_first_direction_recovers_planted_spread"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "principal direction recovers planted spread within 5 degrees; unit norms"

[[claim]]
id = "C270"
fragment = "`tension_loadings`: the same directions as loadings on the log-metrics."
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_first_direction_recovers_planted_spread"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "loadings = directions @ basis, proportional to planted trade vector"

[[claim]]
id = "C271"
fragment = "`explained_spread`: the share of variance along each."
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_first_direction_recovers_planted_spread"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "explained_spread sums to 1, first > 0.9"

[[claim]]
id = "C272"
fragment = "They equal `orient_by_pca` on the same rows."
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "allclose of components and evr with orient_by_pca on same rows"

[[claim]]
id = "C273"
fragment = "At K > 1 the function returns a list of K reports, one per facet, each on the rows that facet"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_k3_reports_one_per_facet_recover_planted_supports", "test:tests/test_tensions.py::test_k1_is_a_single_report_and_facet_error_names_facet"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "list of K reports, one per facet on its assigned rows (slow-marked test)"

[[claim]]
id = "C274"
fragment = "dominates. A facet with fewer than `min_near_frontier` (default 10) near-frontier rows raises"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_k3_reports_one_per_facet_recover_planted_supports", "test:tests/test_tensions.py::test_k1_is_a_single_report_and_facet_error_names_facet", "test:tests/test_tensions.py::test_too_few_near_frontier_raises"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "default 10 asserted (n_near >= 10), ValueError names facet and min_near_frontier"

[[claim]]
id = "C275"
fragment = "depends on the band, and is a statement about"
file = "docs/user-guide/tensions.md"
anchor = ""
kind = "M"
backing = ["test:tests/test_tensions.py::test_too_few_near_frontier_raises", "test:tests/test_tensions.py::test_band_default_and_report_fields"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "band changes the near-frontier set (raise at default, n_near > 10 at band=5)"

[[claim]]
id = "C276"
fragment = "say where along the surface the design sits,"
file = "docs/user-guide/chart.md"
anchor = ""
kind = "M"
backing = ["lemma:L8.6", "lemma:L8.14"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "chart Z blind to common shift (L8.6, free of overall scale); Z are the d-1 coordinates; round trip L8.14"

[[claim]]
id = "C277"
fragment = "`transform` returns the chart, `inverse_transform` inverts it, and `score_samples` is log V alone."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "asserts inverse_transform(T)==X, T[:,-1]==score_samples, transform shape"

[[claim]]
id = "C278"
fragment = "row with a zero metric has `nan` coordinates and no inverse."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_zero_metric_row", "test:tests/test_coordinates.py::test_minus_inf_rows"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "nan Z, -inf log V, nan inverse row asserted"

[[claim]]
id = "C279"
fragment = "`project(X)` returns the design moved onto V = 1 by scaling all its metrics together."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_project_and_improvement_factors_land_on_frontier", "lemma:L1.6", "lemma:L7.9"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V(project(X))==1 asserted; project is m/V (uniform scaling, L7.9)"

[[claim]]
id = "C280"
fragment = "`improvement_factors(X)` gives, per metric, the factor on that metric alone that reaches V = 1"
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_project_and_improvement_factors_land_on_frontier", "lemma:L7.7", "func:src/hyperbolic_trade_space/estimator.py::improvement_factors"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "scaling metric j alone by F[:,j] gives V=1 asserted; L7.7 states the factor"

[[claim]]
id = "C281"
fragment = "(`inf` where the exponent is numerically zero)."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_improvement_factors_inf_for_numerically_zero_exponent_without_warning", "test:tests/test_estimator.py::test_improvement_factor_inf_at_zero_exponent"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "inf at exponent below 1e-12 asserted"

[[claim]]
id = "C282"
fragment = "For a multi-term fit, log V is the soft maximum over facets"
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_matches_derivation.py::test_L10_phi_k_bounds_shift_and_limit_at_numeric_instance", "test:tests/test_estimator.py::test_k_terms_round_trip_and_scores", "lemma:L10.15", "lemma:L10.16"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "score_samples == (1/kappa) log sum exp(kappa x_k), within (log K)/kappa of the max (the entropic sum over K facets, not mean)"

[[claim]]
id = "C283"
fragment = "For a multi-term fit, log V is the soft maximum over facets, and `improvement_factors` uses each"
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_k_terms_improvement_factors_use_assigned_facet", "test:tests/test_estimator.py::test_k_terms_round_trip_and_scores"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "improvement factor of the assigned facet lands on V=1; soft max as C015"

[[claim]]
id = "C284"
fragment = "`knn_gap_scores(Z, k=5)`: mean distance to the k nearest neighbours, normalized by its median."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/gaps.py::knn_gap_scores", "test:tests/test_gaps.py::test_knn_flags_isolated_point"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "median score 1 asserted, isolated point flagged; mean-of-k is the implementation and doctest"

[[claim]]
id = "C285"
fragment = "`find_holes(Z, resolution=50, threshold=2.0)`: grid points inside the convex hull of Z that sit far"
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/gaps.py::find_holes", "test:tests/test_gaps.py::test_find_holes_restricts_to_hull", "test:tests/test_gaps.py::test_find_holes_2d_planted_disc"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "hull restriction and far-from-design score asserted"

[[claim]]
id = "C286"
fragment = "supports `d - 1` of 1, 2 or 3."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_gaps.py::test_find_holes_3d_runs_and_other_dims_raise", "test:tests/test_gaps.py::test_find_holes_1d_planted_gap"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "1, 2, 3 run; 0 and 4 raise"

[[claim]]
id = "C287"
fragment = "`frontier_targets(Z_points, estimator, preconditioner=None)`: sets log V = 0 at given positions and"
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_gaps.py::test_frontier_targets_on_frontier_and_round_trip"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V==1, log V==0 and round trip of chart coordinates asserted"

[[claim]]
id = "C288"
fragment = "maps back to metrics and, with a preconditioner, to attributes."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_gaps.py::test_frontier_targets_with_real_preconditioner", "test:tests/test_gaps.py::test_frontier_targets_with_preconditioner_stand_in", "test:tests/test_gaps.py::test_frontier_targets_on_frontier_and_round_trip"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "metrics always; attributes None without a preconditioner, mapped back with one"

[[claim]]
id = "C289"
fragment = "`orient_by_pca(Z, mask=None)`: rotates to the principal axes of the masked rows."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_gaps.py::test_orient_by_pca_rotation_and_sign", "test:tests/test_gaps.py::test_orient_by_pca_mask_uses_only_masked_rows"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "principal axes; mask uses only masked rows"

[[claim]]
id = "C290"
fragment = "Figure 5. The chart with holes: the red points are grid positions far from every design, candidates for white space."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "R"
backing = ["test:tests/test_gaps.py::test_find_holes_2d_planted_disc", "test:tests/test_site.py::test_each_figure_is_produced_by_the_code_shown_above_it", "gen:scripts/build_figures.py::build_page", "func:src/hyperbolic_trade_space/plotting.py::plot_frontier_coordinates"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "hole points are grid positions far from the data (score vs nearest design); marker colour HOLE_COLOR is orange-red (#D55E00), worded red"

[[claim]]
id = "C291"
fragment = "`plot_log_plane`: two metrics, the data, the frontier and its band."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_plotting.py::test_log_plane_draws_frontier_line_in_black_and_band_in_grey"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "data, frontier line, band asserted"

[[claim]]
id = "C292"
fragment = "`plot_frontier_surface_3d`: three metrics, the frontier surface."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_plotting.py::test_surface_3d_returns_3d_axes_and_validates"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "3d axes for three metrics"

[[claim]]
id = "C293"
fragment = "`plot_frontier_coordinates`: the chart, with optional holes and targets."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_plotting.py::test_frontier_coordinates_one_and_two_coordinates_and_overlays"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "holes and targets overlays asserted"

[[claim]]
id = "C294"
fragment = "`plot_v_by_variable`: log V against a configuration variable."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_plotting.py::test_v_by_variable_numeric_and_categorical_and_existing_ax"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "log V against a numeric or categorical variable"

[[claim]]
id = "C295"
fragment = "`plot_tensions`: the tension report as a heatmap."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_plotting.py::test_plot_tensions_with_stand_in_report"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "image with TENSION_CMAP asserted"

[[claim]]
id = "C296"
fragment = "one colour vocabulary, declared as module constants (`FRONTIER_COLOR`, `BAND_COLOR`, `HOLE_COLOR`,"
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_plotting.py::test_log_plane_draws_frontier_line_in_black_and_band_in_grey", "test:tests/test_plotting.py::test_plot_tensions_with_stand_in_report"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "FRONTIER_COLOR, BAND_COLOR, TENSION_CMAP used and asserted; HOLE_COLOR used in plot_frontier_coordinates (constants in __all__)"

[[claim]]
id = "C297"
fragment = "gives a per-row label to pass as `color=`."
file = "docs/user-guide/chart.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_plotting.py::test_surface_k3_and_coordinates_facet_colouring", "func:src/hyperbolic_trade_space/plotting.py::facet_labels"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "labels 'facet k' per row passed as color= and shown"

[[claim]]
id = "C298"
fragment = "where would a configuration without measurements fall? It composes two fits."
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "S"
backing = ["func:src/hyperbolic_trade_space/predictive.py::TradeSpaceRegressor", "test:tests/test_predictive.py::test_clones_leave_parameters_untouched"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Class docstring and doctest; fit composes chart fit then regressor fit."

[[claim]]
id = "C299"
fragment = "- `predict(X_config)`: metrics, through the inverse chart."
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_recovers_planted_coordinates"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Asserts predict equals inverse_transform of predicted coordinates."

[[claim]]
id = "C300"
fragment = "- `predict_coordinates(X_config)`: the pair `(Z, log_v)`."
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_recovers_planted_coordinates", "func:src/hyperbolic_trade_space/predictive.py::TradeSpaceRegressor"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Z, log_v recovered against planted map; doctest shapes."

[[claim]]
id = "C301"
fragment = "- `predict_novelty(X_config)`: V - 1, positive where the design is predicted beyond the surface."
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_novelty_beyond_the_soft_frontier"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Asserts novelty positive on frontier designs, negative far inside, log1p(nov) equals log V."

[[claim]]
id = "C302"
fragment = "the regressor's `return_std` propagated by the delta method; raises"
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_predict_std_plumbing_with_gaussian_process", "test:tests/test_predictive.py::test_predict_std_absent_without_return_std"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Delta method checked against Monte Carlo (rtol 5%); AttributeError without return_std."

[[claim]]
id = "C303"
fragment = "- `score`: R-squared in coordinate space, not in metric units."
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_score_is_coordinate_space_r2_and_order_independent"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Score equals mean coordinate-space R2."

[[claim]]
id = "C304"
fragment = "novelty prediction. A one-dimensional `y` is accepted for a single metric. `trade_space` may be a"
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_single_metric_accepts_1d_y", "test:tests/test_predictive.py::test_trade_space_can_be_a_pipeline_and_regressor_a_pipeline"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "1-D y and Pipeline chart tested (with a FunctionTransformer, not a literal preconditioner)."

[[claim]]
id = "C305"
fragment = "`Pipeline` ending in a `HyperbolicTradeSpace`, such as a preconditioner followed by the estimator."
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_predictive.py::test_trade_space_can_be_a_pipeline_and_regressor_a_pipeline"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Pipeline ending in HyperbolicTradeSpace works; preconditioner example itself not tested here."

[[claim]]
id = "C306"
fragment = "A predicted position inherits the surrogate's error and extrapolation risk, and is conditional on"
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "M"
backing = ["test:tests/test_predictive.py::test_predict_std_plumbing_with_gaussian_process", "test:tests/test_predictive.py::test_recovers_planted_coordinates"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Cautionary gloss; surrogate error and growing std far from data shown by tests; conditional on trade_space_ by construction."

[[claim]]
id = "C307"
fragment = "evaluation to run, to be checked, not a result. The regressor declares `positive_only` targets and"
file = "docs/user-guide/prediction.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_regressor_tags"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "positive_only tag asserted; the 'proposal to be checked' clause is advice, not a software claim."

[[claim]]
id = "C308"
fragment = "Every fit records how it stopped."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_termination_record_for_k_terms", "test:tests/test_estimator.py::test_termination_not_applicable_cases_do_not_warn", "test:tests/test_solvers.py::test_margin_and_radius_are_nan_at_one_term_not_infinite"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "K>1, K=1, tangent, penalty and degenerate fits all end with a termination_ record with a status"

[[claim]]
id = "C309"
fragment = "At one term the fit is a convex program and its answer is the"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "M"
backing = ["lemma:L4", "lemma:L12.13", "test:tests/test_solvers.py::test_terms_k1_equals_slsqp_and_degenerate"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "f_k = J_tau - linear is convex (L12.13, from L4) on the simplex; K=1 fit equals the SLSQP solve; minimizer up to solver tolerance"

[[claim]]
id = "C310"
fragment = "With several terms it alternates between weights from the current model and refitting each"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_terms_monotone_history_and_stops", "test:tests/test_soft_fit.py::test_r1_the_soft_objective_never_rises_across_the_history"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "hard fit: argmax relabel then per-facet refit until the assignment is fixed; soft fit uses softmax weights; the sentence's weights are labels in the hard case"

[[claim]]
id = "C311"
fragment = "no step made the mean slack worse (`mean_slack_`, defined at every number of terms)."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_terms_monotone_history_and_stops", "test:tests/test_soft_fit.py::test_r1_the_soft_objective_never_rises_across_the_history", "test:tests/test_estimator.py::test_mean_slack_is_defined_for_every_k_and_objective_documents_what_was_minimized", "lemma:L15.16"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "descent holds up to guard_tol 1e-12 and not under facet_step='tangent' (status not_applicable); mean_slack_ defined at every K is pinned"

[[claim]]
id = "C312"
fragment = "Numerical stationarity: no first-order improvement is left."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "M"
backing = ["lemma:L12.21", "lemma:L12.23"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "level 2 is the gap G within eps_kkt; L12: G=0 iff the simplex KKT holds, and 0<=f-f*<=G; a definition of the level with a tolerance"

[[claim]]
id = "C313"
fragment = "The facet gap G_k measures what"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "M"
backing = ["lemma:L12.23"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "G_k bounds the remaining suboptimality f_k - f_k* from above (0<=f-f*<=G); 'measures' is loose for 'bounds'"

[[claim]]
id = "C314"
fragment = "if no design sits exactly on a seam between facets, small changes"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "M"
backing = ["lemma:L13.7", "lemma:L13.12", "test:tests/test_solvers.py::test_margin_lemma_perturbations_inside_the_radius_keep_labels"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "no row on a seam = positive margin (R2); L13: score changes below gamma/2 keep every maximizing facet; 'small' is relative to gamma"

[[claim]]
id = "C315"
fragment = "is the perturbation provably leaving every facet unchanged."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "M"
backing = ["lemma:L13.7", "lemma:L13.11", "test:tests/test_solvers.py::test_margin_lemma_perturbations_inside_the_radius_keep_labels"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L13.11 radius gamma/(2U) keeps every row's maximizing facet (assignment); 'leaving every facet unchanged' is loose wording for the assignment"

[[claim]]
id = "C316"
fragment = "At infinite temperature this happens when a frontier row lies on two facet planes or two"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets", "test:tests/test_solvers.py::test_r1_planted_certificates"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "gamma=0 exactly for a tied row or identical facets (pinned); zero-margin seeds only at tau=inf, none at tau=50"

[[claim]]
id = "C317"
fragment = "- `guard_stop`: an iteration raised the mean slack by more than `guard_tol`. Not converged."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_guard_stop_returns_the_consistent_previous_state", "test:tests/test_estimator.py::test_convergence_warning_keyed_to_guard_stop"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "status and the warning pinned with a +10 rise; the threshold obj2 > obj + GUARD_TOL is read from code (_solve_terms_once), not tested at the boundary"

[[claim]]
id = "C318"
fragment = "- `iteration_cap`: `max_iter` reached. Not converged."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_iteration_cap_status", "test:tests/test_estimator.py::test_convergence_warning_keyed_to_iteration_cap"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "max_iter reached gives iteration_cap, success False, and a ConvergenceWarning"

[[claim]]
id = "C319"
fragment = "- `not_applicable`: one term, `facet_step=\"tangent\"`, a `penalty`, one metric, fewer designs than"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_not_applicable_statuses", "test:tests/test_soft_fit.py::test_r7_a_soft_fit_at_infinite_tau_is_not_applicable", "test:tests/test_soft_fit.py::test_r7_a_soft_fit_with_a_penalty_is_not_applicable", "test:tests/test_estimator.py::test_termination_not_applicable_cases_do_not_warn"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "one term, tangent, penalty, one metric, fewer designs than facets and soft at tau=inf are each asserted not_applicable"

[[claim]]
id = "C320"
fragment = "facets, or a soft fit at infinite temperature. Not a failure."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_termination_not_applicable_cases_do_not_warn"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "no ConvergenceWarning for not_applicable (tangent, penalty, K=1, one metric pinned; soft at tau=inf not asserted for no-warn but not_applicable is not in _WARN_STATUSES)"

[[claim]]
id = "C321"
fragment = "A soft fit (finite `term_temperature`) has no assignment, so no margin:"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "soft fits assert bound, gamma, radius all nan and assignment_changes == 0"

[[claim]]
id = "C322"
fragment = "- `bound`: the share-weighted sum of facet gaps, bounding the distance from the fixed-assignment"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "M"
backing = ["lemma:L14.20", "test:tests/test_solvers.py::test_corollary_bound_on_every_planted_fit"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "bound = sum_k share_k G_k >= F(W) - F*_fixed (Corollary 4), asserted on every planted fit; fixed assignment of this run, not across restarts"

[[claim]]
id = "C323"
fragment = "- `gamma`, `radius`: the margin and stable radius, `nan` at one term."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_margin_and_radius_are_nan_at_one_term_not_infinite"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "gamma and radius nan at one term pinned; margin and radius defined by assignment_margin (values test)"

[[claim]]
id = "C324"
fragment = "- `min_curvature`: soft fit only, the smallest curvature on the active face; `nan` otherwise."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_soft_fit.py::test_r7_a_soft_fit_at_infinite_tau_is_not_applicable", "test:tests/test_soft_fit.py::test_r2_the_default_is_the_explicit_infinity_and_leaves_one_term_alone", "test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "min_curvature positive for certified soft fits, nan for non-soft and soft at tau=inf; smallest eigenvalue on the active face per soft_certificate docstring"

[[claim]]
id = "C325"
fragment = "A soft fit leaves `gamma`, `radius` and `bound` `nan`."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_soft_fit.py::test_r7_the_benchmark_tables_are_certified"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "asserts np.isnan([bound, gamma, radius]).all() on soft fits"

[[claim]]
id = "C326"
fragment = "The tolerances are module constants of `hyperbolic_trade_space.solvers`, not parameters: `EPS_KKT` ="
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_default_path_has_no_warnings_and_constants", "test:tests/test_estimator.py::test_constants_are_reexported"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "constants defined in solvers.py and re-exported; they are not estimator parameters (only get_params-level check via sklearn conformance suite)"

[[claim]]
id = "C327"
fragment = "1e-8, `EPS_FEAS` = 1e-9, `GUARD_TOL` = 1e-12, `POLISH_STEPS` = 5."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_default_path_has_no_warnings_and_constants", "test:tests/test_solvers.py::test_polish_never_increases_the_facet_objective_and_closes_the_gap", "test:tests/test_estimator.py::test_constants_are_reexported"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "EPS_KKT 1e-8, EPS_FEAS 1e-9 (default-path test); GUARD_TOL 1e-12 and POLISH_STEPS 5 (polish test)"

[[claim]]
id = "C328"
fragment = "exponents (above 1e-3), one per facet. A small value marks a nearly flat direction (weakly identified exponents). It is `nan` at infinite"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_conditioning_per_facet_and_nan_cases"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "shape (n_terms,) positive per facet; nan at tau=inf pinned"

[[claim]]
id = "C329"
fragment = "temperature and for a facet with fewer than two participating exponents."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_estimator.py::test_conditioning_per_facet_and_nan_cases"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "nan at tau=inf and for a facet with one participating exponent (d=1 case) pinned; fewer-than-two in d>1 only by code"

[[claim]]
id = "C330"
fragment = "A small value marks a nearly flat direction (weakly identified exponents)."
file = "docs/user-guide/termination.md"
anchor = ""
kind = "M"
backing = ["lemma:L17.5", "test:tests/test_estimator.py::test_conditioning_drops_for_nearly_collinear_metrics"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "the Hessian of J_tau is tau times a weighted covariance (L17.5), so a small eigenvalue is a nearly flat direction; 'weakly identified' is the interpretation, illustrated by the collinear-metrics test"

[[claim]]
id = "C331"
fragment = "The margin `gamma` is in score units (log metrics), the scale of the band 1/tau; `radius` is"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "gamma is a gap between scores w.u - beta with u = log metrics; the 1/tau band is the softmax scale, a guide not a theorem"

[[claim]]
id = "C332"
fragment = "`gamma / (2R)`, with R the largest norm of a row (u, -1). Compare `gamma` with the median margin,"
file = "docs/user-guide/termination.md"
anchor = ""
kind = "M"
backing = ["lemma:L13.11", "test:tests/test_solvers.py::test_assignment_margin_values_and_duplicate_facets"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "radius = gamma/(2U), U the largest norm of (u,-1) (L13.11); values test pins 0.4/(2 sqrt 2); median-margin comparison is advice"

[[claim]]
id = "C333"
fragment = "A single term has constant elasticities and finds one tension, at"
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["lemma:L7", "lemma:L3"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L7: elasticities -w_k/w_j constant on the facet; L3 balanced KKT gives the balanced point"

[[claim]]
id = "C334"
fragment = "are determined by the sample you give; the Pareto boundary is a property of the system."
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["lemma:L11", "glossary:fitted-reference-surface", "glossary:supporting-envelope", "glossary:pareto-boundary"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Gap G-1 and glossary: the surface/envelope are fitted to the sample, the Pareto boundary is the system's; L11 non-converse"

[[claim]]
id = "C335"
fragment = "of V is efficient in the contending metrics, and the converse is not claimed."
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["lemma:L11", "test:tests/test_derivation.py::test_L11_in_chain_and_states_non_converse"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L11.3: a V-maximizer is weakly efficient in all metrics, efficient in contending ones (no dominating u'); converse explicitly not proved"

[[claim]]
id = "C336"
fragment = "At a finite temperature some designs lie beyond V = 1 by construction."
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["lemma:L5", "glossary:temperature"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L5.3: mean <= LME <= max, so beta = LME <= max and the maximizing design has log V >= 0 (strictly above for non-constant scores)"

[[claim]]
id = "C337"
fragment = "A very high tau rests the fit on a few extreme designs"
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["lemma:L5", "lemma:L3"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L5.5: LME -> max as tau -> inf; L3.5: the hard maximum depends only on the extreme support of the observations"

[[claim]]
id = "C338"
fragment = "The set is exact at infinite temperature with `min_exponent` at"
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["glossary:contending-set", "test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact", "test:tests/test_tensions.py::test_no_warning_when_min_exponent_zero"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Glossary: contending set = support of the exponents at infinite temperature; test shows set stays exact at finite tau under min_exponent 0"

[[claim]]
id = "C339"
fragment = "0, and graded participation at a working temperature."
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["test:tests/test_tensions.py::test_finite_tau_smooths_weights_and_contending_set_stays_exact", "glossary:support-weights"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Test: finite tau smooths the weights (graded participation); glossary support-weights = softmax weights"

[[claim]]
id = "C340"
fragment = "negative association near the surface is partly a closure effect."
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["test:tests/test_tensions.py::test_closure_induces_negative_association_without_trade"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Test asserts closure induces negative association without any trade; tension_report carries closure_note"

[[claim]]
id = "C341"
fragment = "A multi-term fit is a local optimum chosen among seeded restarts."
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["lemma:L15", "test:tests/test_estimator.py::test_n_restarts_default_and_validation"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "L15 descent is local only; gap G-14 no global claim; n_restarts seeds the restarts and the lowest mean slack is kept"

[[claim]]
id = "C342"
fragment = "which tends to zero as any participating"
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "M"
backing = ["glossary:invariant-value", "test:tests/test_preconditioning.py::test_pullback_zero_attribute_gives_minus_inf_in_both"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V is a weighted geometric mean so V -> 0 as a participating (w_j > 0) metric -> 0; test pins zero attribute -> log V = -inf"

[[claim]]
id = "C343"
fragment = "It is unrelated to PCA in hyperbolic space [@chami2021horopca]."
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "L"
backing = ["bib:chami2021horopca"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "reading_pass.yaml n=44 verdict supported (HoroPCA abstract; 'unrelated' is the paper's own statement); prior_art.yaml id kernel-hyperbolic-pca"

[[claim]]
id = "C344"
fragment = "Machine checks confirm that formulas follow from stated conditions and that the code agrees with"
file = "docs/user-guide/limitations.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_matches_derivation.py::test_fitted_model_matches_chain_L1_L7_L8"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Derivation lemma scripts machine-check formulas; test_matches_derivation checks the code agrees with the chain; scope statement for the rest"

[[claim]]
id = "C345"
fragment = "evaluated designs is lost, and the alternatives are bespoke or opaque. A model-based method"
file = "site/index.html"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Practice stated as fact (trade studies decided from documents and tables; alternatives bespoke or opaque); register must mark it reading, the author's experience; no audit row"

[[claim]]
id = "C346"
fragment = "has to clear a bar before a decision-maker can trust it: it has to show its reasoning, say"
file = "site/index.html"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Normative judgment on what a model-based method must do to be trusted; reading"

[[claim]]
id = "C347"
fragment = "Trade studies are usually decided from documents and tables, where the detail of the"
file = "site/index.html"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Practice claim (usually decided from documents and tables); reading, author's experience"

[[claim]]
id = "C348"
fragment = "What trades against what depends on where a design sits."
file = "site/index.html"
anchor = ""
kind = "M"
backing = ["lemma:L7", "lemma:L10", "test:tests/test_site.py::test_why_labels_come_from_the_exponents", "test:tests/test_site.py::test_why_regions_partition_the_triangle_and_there_are_three_facets"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Each facet has its own exponents (L7 elasticities along a facet, L10 sum of facets); the why-figure test pins that regions and labels follow the fitted exponents"

[[claim]]
id = "C349"
fragment = "product of the metrics that names which of them compete on one part of the trade space."
file = "site/index.html"
anchor = ""
kind = "M"
backing = ["lemma:L3", "glossary:n-lemma", "test:tests/test_tensions.py::test_contending_set_recovers_planted_support"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "n-lemma = support of the exponent vector of a facet (L3 simplex optimality, sparse at tau=inf); the test recovers planted supports; the glossary defines it"

[[claim]]
id = "C350"
fragment = "method belongs in unsupervised learning and feature engineering beside PCA: kin rather than a"
file = "site/index.html"
anchor = ""
kind = "P"
backing = ["reading"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Author's judgment on where the method belongs; the kin wording for kernel PCA is in prior_art.yaml but this is about PCA; reading"

[[claim]]
id = "C351"
fragment = "substitute, and the two chain (the tension report already runs PCA on the near-frontier chart"
file = "site/index.html"
anchor = ""
kind = "S"
backing = ["test:tests/test_tensions.py::test_orient_by_pca_equals_report_directions", "func:src/hyperbolic_trade_space/tensions.py::tension_report"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "The report's tension directions equal orient_by_pca of the near-frontier chart coordinates; the test asserts it"

[[claim]]
id = "C352"
fragment = "The foundation box is the invariant form: a weighted geometric mean"
file = "site/index.html"
anchor = ""
kind = "M"
backing = ["lemma:L1", "glossary:invariant-value"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V(km)=kV(m); weighted geometric mean per the glossary"

[[claim]]
id = "C353"
fragment = "V of the metrics, whose level V = 1 is the fitted reference surface and whose logarithm is the"
file = "site/index.html"
anchor = ""
kind = "M"
backing = ["lemma:L1", "glossary:fitted-reference-surface", "glossary:energy-differential"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "log V = w.u - beta (L1); V=1 is the fitted reference surface (Definition 1, glossary)"

[[claim]]
id = "C354"
fragment = "energy differential. The single-term core fits the weights and an offset to your designs as"
file = "site/index.html"
anchor = ""
kind = "M"
backing = ["lemma:L3", "lemma:L4", "lemma:L5"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "K=1 fit of exponents on the simplex and an offset is a convex program (L4), with KKT (L3) and log-mean-exp (L5)"

[[claim]]
id = "C355"
fragment = "one convex problem. Four boxes use that fit: the chart (each design becomes a position along"
file = "site/index.html"
anchor = ""
kind = "M"
backing = ["lemma:L8", "lemma:L7", "lemma:L6", "lemma:L9"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Chart (L8), elasticities along a facet (L7), Gaussian noise correction (L6), pull-back (L9); the fragment is the map's structural description"

[[claim]]
id = "C356"
fragment = "correction for noise, and the pull-back to your raw attributes. The lower boxes extend the"
file = "site/index.html"
anchor = ""
kind = "M"
backing = ["lemma:L6", "lemma:L9", "lemma:L10", "lemma:L11", "lemma:L12", "lemma:L13", "lemma:L14", "lemma:L15", "lemma:L17"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Noise correction L6, pull-back L9, several facets L10, Pareto relation L11, algorithm guarantees L12-L15 and L17 (the paper states none is global)"

[[claim]]
id = "C357"
fragment = "A scikit-learn-compatible estimator for the frontier, with an invertible log-ratio chart,"
file = "site/index.html"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator", "test:tests/test_estimator.py::test_chart_roundtrip_and_score_samples", "test:tests/test_tensions.py::test_monolemma_and_names", "test:tests/test_plotting.py::test_ternary_regions_partition_the_triangle", "file:work-packages/interface-contract.toml"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Estimator, invertible chart round trip, tension_report and plotting are in package.public_names and submodules of the contract and tested"

[[claim]]
id = "C358"
fragment = "to reading a tension report, the API reference, a cubesat example, the model in brief"
file = "site/index.html"
anchor = ""
kind = "S"
backing = ["file:work-packages/interface-contract.toml", "test:tests/test_site.py::test_nav_pages_exist_and_cover_the_contract_pages"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "docs.pages in the contract lists getting-started, user-guide (conditioning, tensions), api-reference, examples (cubesat), theory, glossary; the test checks the nav covers them"

[[claim]]
id = "C359"
fragment = "\"space\": a monomial, later posynomial, frontier V(m) = Π m_j^{w_j} whose unit level set is the"
file = "README.md"
anchor = ""
kind = "M"
backing = ["lemma:L1.4", "lemma:L1.6", "glossary:invariant-value"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "V = prod m_j^w_j is L1.4; V(m/V(m))=1 puts the point on the unit level set (L1.6); 'later posynomial' is the documented extension (L10)"

[[claim]]
id = "C360"
fragment = "log V, the energy differential to it). It is a scikit-learn-compatible unsupervised estimator, with"
file = "README.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_sklearn_compat.py::test_sklearn_compatible_estimator", "test:tests/test_sklearn_compat.py::test_no_predict_decision_function_or_score", "glossary:energy-differential"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "parametrize_with_checks conformance, TransformerMixin estimator with fit(X, y=None); log V as energy differential is the glossary definition"

[[claim]]
id = "C361"
fragment = "SymPy-verified derivations and an ADCS trade-study case."
file = "README.md"
anchor = ""
kind = "S"
backing = ["test:tests/test_proof_map.py::test_checker_passes_on_the_committed_record", "test:tests/test_adcs_case.py::test_evaluate_design_three_fast"]
status = "backed"
disposition = "keep"
source = "P5 claims pass, WP10 Amendment 5 R-43"
note = "Proof-map checker passes on the committed lemma record (SymPy scripts); ADCS case is exercised by tests/test_adcs_case.py"
```
