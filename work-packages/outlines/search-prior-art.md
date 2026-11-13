# Note: the trade-off-aware search (WP12): prior art and the low-hanging proofs

Drafted 2026-11-08 after the supervisor confirmed the nested-loop picture
(`work-packages/WP10-decisions.md`, "Ascent in configuration space and the outer search"). Input to
the WP12 scope of work. Nothing here is claimed as novel; the aim is to say what is ours, what is
inherited, and what is only observed.

## The procedure (loops from the inside out)

0. Identification: fit the K-facet frontier to the current table (WP9); facets, normals $w_k$,
   tangent spaces, reach, assignment, chart.
1. Proposal: for near-frontier designs on facet $k$, the ascent direction in configuration space,
   $\nabla_c \log V = J_f(c)^{\top}\,\mathrm{diag}(\partial \log m/\partial a)\,w_k$, with $J_f$
   estimated from the data (finite differences on the oracle, SPSA, or the gradient of the
   supervised map $c \mapsto \log V$); a noisy step for the continuous variables; a finite
   comparison for the categorical ones; a batch of proposals.
2. Outer search: evaluate the batch against the noisy oracle, append, refit, repeat; stop when the
   exact-maximum frontier no longer moves beyond the noise band. Output: the discovered frontier,
   its facets and trade-offs, and the table that produced it. It proposes; experts choose.

Honest limits: (i) ascent along fixed normals reaches the log-convex envelope of the front; dents
are reached only by noise and recognized by the holes detector; (ii) the frontier is monotone
outward only at $\tau=\infty$; (iii) the theorem is about continuous variables within a category.

## Prior art (Crossref-verified 2026-11-08 unless marked)

| Family | Source | What it gives us | How this differs |
|---|---|---|---|
| Multiobjective gradient methods | Fliege and Svaiter 2000, *Math. Methods OR* 51, 479–494, doi 10.1007/s001860000043; Désidéri 2012, MGDA, *C. R. Math.* 350, 313–318, doi 10.1016/j.crma.2012.03.014 | Pareto stationarity as a first-order condition; a common descent direction from the convex hull of the gradients; convergence to Pareto-critical points | our multipliers are the facet's fitted exponents, found from the data's edge, not computed per step from gradients; K facets give K ascent families |
| Stochastic multi-gradient | Liu and Vicente 2021, *Ann. Oper. Res.*, doi 10.1007/s10479-021-04033-z; MoCo and "stochastic tangential Pareto dynamics" (2025 preprints; to verify) | rates for stochastic multi-gradient; the bias of the stochastic common direction, which can converge to part of the front | our direction is fixed per facet between refits, so the bias question moves to the refit; the tangential-dynamics preprint's name suggests overlap and must be read |
| Stochastic approximation | Robbins and Monro 1951, *Ann. Math. Stat.* 22, 400–407, doi 10.1214/aoms/1177729586; Kiefer and Wolfowitz 1952, *Ann. Math. Stat.* 23, 462–466, doi 10.1214/aoms/1177729392; Spall 1992 SPSA, *IEEE TAC* 37, 332–341, doi 10.1109/9.119632; Borkar 1997, two time scales, *Syst. Control Lett.* 29, 291–294, doi 10.1016/S0167-6911(97)90015-3; Kushner and Yin's book (DOI to verify) | convergence of noisy ascent with measurement-only oracles under step-size and variance conditions; the two-timescale scheme for a fast loop inside a slow one | inherited as is; our contribution is the identification of the direction, and the epoch-wise scheme that avoids two time scales by freezing the fit per epoch |
| Scalarization and proper efficiency | Geoffrion 1968, *J. Math. Anal. Appl.* 22, 618–630, doi 10.1016/0022-247x(68)90201-1; Miettinen 1998, doi 10.1007/978-1-4615-5563-6; Ehrgott 2005, doi 10.1007/3-540-27659-9 | with positive weights a scalarized maximizer is properly efficient; on convex problems every properly efficient point is one; the non-convex gap | ours is the log-space (geometric-mean) version; log-convexity of the attainable set is the hypothesis |
| Sequential and Bayesian design for Pareto fronts | Knowles 2006 ParEGO, *IEEE TEVC* 10, 50–66, doi 10.1109/TEVC.2005.851274; expected hypervolume improvement (Emmerich et al. 2006, to verify; Hupkens, Deutz and Yang 2015, doi 10.1007/978-3-319-15892-1_5); NOSTRA (IDETC 2025, arXiv 2508.16476, to verify); del Rosario et al. 2020 Pareto-shell error (arXiv 1911.03224, to verify) | where to sample next from a surrogate; metrics focused on a band around the front | the surrogate here is the frontier model itself, with a named trade-off structure; proposals follow its normals rather than an acquisition function |
| Diffusion picture | Welling and Teh 2011, stochastic gradient Langevin dynamics, ICML (proceedings URL; no DOI) | drift plus noise concentrating near maximizers | an analogy for the discussion, not a theorem we prove |

Not found: a method that fits a frontier model to a trade table and takes ascent steps along its
facets to propose new designs (two searches, 2026-11-08). To be rechecked with other phrasings
during WP12 scoping.

## Low-hanging proofs (what is ours, what is inherited)

| ID | Statement | Status | Proof idea |
|---|---|---|---|
| L11 | a V-maximizer is Pareto-efficient (weakly if some exponents are zero) | ours, in WP9 | monotonicity of the weighted geometric mean |
| L12 | the ascent direction in configuration space: $\nabla_c \log V = J_f^{\top}\mathrm{diag}(\partial\log m/\partial a)\,w_k$ on facet $k$; categorical variables by finite comparison | ours, easy | chain rule on L3 and L9 with an abstract Jacobian; symbolic $d$ |
| L13 | the exact-maximum frontier level $\beta^{*}=\min_{w\in\Delta}\max_i w\cdot u_i$ is nondecreasing when designs are added; the soft maximum (log-mean-exp) is not, with a two-point counterexample | ours, easy | a min of a pointwise-larger function; the counterexample numerically |
| L14 | a stationary point of the ascent on facet $k$ (with $w_k>0$) is first-order Pareto-stationary with multipliers $w_k$ | ours via standard | a common ascent direction would make $\sum_j w_{kj}\nabla\log m_j\cdot v>0$; cite Fliege–Svaiter and Désidéri for the definition |
| P15 | the frontier levels of the epoch-wise scheme converge | ours, easy | L13 plus boundedness of the attainable set: monotone and bounded |
| I6 | noisy ascent for a fixed facet converges to stationary points | inherited (Robbins–Monro; Kiefer–Wolfowitz or SPSA for measurement-only gradients) | ledger entry with step-size, smoothness and variance conditions and their failure modes |
| I7 | with log-convex attainable set, stationary points with positive multipliers are properly efficient, and every properly efficient point is reached by some $w$ | inherited (Geoffrion) | ledger entry; failure mode: dents |
| T1 | theorem: under L12–L14, P15, I6, I7 and finite categories, the epoch-wise search's limit points on each facet are Pareto-stationary; Pareto-optimal under log-convexity; the union over facets lies in the log-convex envelope of the front, and as $K$ grows the fitted envelope approaches the hull | assembled; proof is the chain | stated with every hypothesis by ledger tag |

Rejected as not low-hanging: a rate for the whole nested scheme; a two-timescale proof with a
refit map (Borkar's conditions on the slow ODE are not checkable for the refit); discovery of
non-log-convex parts of the front.
