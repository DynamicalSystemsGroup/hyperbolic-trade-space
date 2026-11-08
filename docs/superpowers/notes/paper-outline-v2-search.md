# Note: outline of the paper, v2 with the trade-off-aware search (2026-11-08)

Supersedes `paper-outline-v1-baseline.md`, which is kept as the baseline. What v2 adds, in the
supervisor's words: "the design optimization which pushes to find the highest energy level
attainable. this does not select a final design. that falls to experts, we focus on making
interpretable, reproducible process for searching the design space in a trade-off aware way";
and the generalization it motivates: "more general kernel methods which are supported by GGP
because that allows the analyst to tailor the model to fit the problem without deviating from the
method." Sections unchanged from v1 say so and are not repeated in full. Word budget about 5,000,
cap 6,000; the search adds a results subsection, a case subsection and a discussion paragraph,
so other sections compress. "WP9" marks the solver package; "WP-search" marks the search
package proposed to the supervisor (number to be assigned).

## Abstract and Figure 1

As v1, plus one sentence: the fitted facets give ascent directions in configuration space, and an
outer loop that evaluates along them and refits pushes the frontier to the highest attainable
level; the process proposes, experts choose. Figure 1 may become a pair: the facets of the trade
space, and the frontier rising over rounds of the search (decided in WP10).

## 1. Introduction: the decision problem, and the exploration problem

As v1 (trade studies as documents; the bar for a trusted model-based method; PCA explains
variance, this explains tensions; what a decision-maker needs; rerunnable analysis), plus: a
trade study also decides what to evaluate next; today that is expert intuition or exhaustive
sampling; the fitted trade-offs say where "better" is, so sampling can be trade-off aware; the
process stops short of selecting a design, which falls to experts; the contribution gains a
clause: a reproducible, interpretable process for searching the design space. Backing as v1
plus the search prior art of section 2.

## 2. Prior art, by family

As v1's table (Pareto and multiobjective optimization; DEA; production and distance functions;
deterministic and stochastic frontiers; PCA and sparse PCA; compositional PCA; geometric
programming and max-affine fitting; kernel and hyperbolic PCA; entropic risk; tradespace
exploration; decision analysis and MCDA; MBSE), plus three families for the search, to be found
and verified in WP-search's literature pass: multiobjective gradient and steepest-descent methods
(the facet exponents as the multipliers); stochastic approximation with measurement-only
oracles (Robbins-Monro, Kiefer-Wolfowitz, two-timescale schemes) and the Langevin or diffusion
picture; sequential and Bayesian design of experiments for Pareto fronts (expected hypervolume
improvement and relatives). For each: what it produces, what is shared, how this differs, cites.

## 3. Preliminaries and notation

As v1, plus: the system (a fixed configuration space with continuous and categorical variables),
the oracle (configuration to noisy attributes), the attainable set (the oracle's image in metric
space) and its Pareto front; the notation rows for the tangent space and ascent direction become
body notation rather than discussion-only. Backing: `notation.md` (rows to be added for oracle,
attainable set, round index, step size, proposal noise).

## 4. Definitions

As v1, plus: the ascent direction in configuration space (the normal chained through conditioning
and the oracle's local Jacobian); a round of the search; the stopping rule (the exact-maximum
frontier no longer moves beyond the noise band); the energy-level reading (levels of V; up is
better; the search raises the highest attainable level).

## 5. Results

As v1 (L1 to L10; L11 a V-maximizer is Pareto-efficient; the K > 1 algorithm and what it
inherits; the sparsity option), plus the search results, each stated with what is proved, what is
inherited and what is only observed:
- the gradient identity in configuration space (new lemma, calculus on L3 and L9), and its
  categorical counterpart as a finite comparison;
- stationarity of the ascent on a facet is first-order Pareto stationarity with the facet's
  exponents as multipliers (new lemma or a cited standard result, decided after the literature
  pass);
- the exact-maximum frontier is monotone outward as data accumulate; the soft-maximum frontier
  is not (new small lemma; it fixes the stopping rule);
- convergence of noisy ascent for a fixed facet to stationary points (inherited: stochastic
  approximation, conditions in the ledger); convergence of the nested scheme, fast ascent for a
  fixed fit and slow refit (inherited: two-timescale stochastic approximation); sufficiency, that
  stationary points are Pareto-optimal, under log-convexity of the attainable set (inherited:
  weighted-sum scalarization; a ledger hypothesis with its failure mode);
- the reach of the search: the log-convex envelope of the front; dents are found only by noise
  and recognized by the holes detector; the whole front when the attainable set is log-convex.
Backing: `derivation/` (new lemmas), the ledger with new INHERITED entries, `docs/method.md`;
WP-search for the code the statements describe.

## 6. Case construction

As v1 (the cubesat design space, two regimes, the planted multi-facet frontier), plus the search
setup: the oracle is the cubesat simulator called live with measurement noise (the only place the
paper simulates; everything else reads cached tables); the starting table is the WP4b sample; the
step, noise and batch sizes; the number of rounds; the categorical moves (wheel class, tracker
grade); the reference against which discovery is judged (a dense reference sample of the
attainable set, or an evolutionary front, decided in WP-search). Backing: `examples/adcs/adcs_sim.py`,
`cubesat_model.py`, `design_space.py`; WP-search's driver module.

## 7. Case analysis

As v1 (K = 1 and K = 3 on the cubesat; persistence; regime comparison; where candidates sit),
plus the search: the frontier's reach per facet by round; designs beyond the old frontier per
round; the stopping round; the discovered front against the reference; which design variables the
ascent moved, by facet, in the engineer's terms; what the search found that the original sample
did not; its cost in oracle calls against exhaustive sampling. Figures: levels rising by round;
the chart with the search path; the per-facet configuration moves.

## 8. Discussion

As v1 (interpretation as human validation; what the decision-maker holds; limits; verify versus
validate; rerunning for configuration management), with the tangent-space paragraph promoted:
what the search does and does not do (it proposes and raises the attainable level; it does not
select a design; experts choose among frontier designs with the trade-offs made explicit); the
diffusion picture in words; the three limits of the theorem; what reproducibility means for a
search (seeds, the oracle's record, the table after every round committed). The GGP-supported
kernel direction is stated here as what the search motivates: a family of fitted forms the
analyst can tailor to the problem while the programs remain geometric programs, so the method's
guarantees and its reading rules carry over; not built.

## 9. Reproducibility and your own case

As v1, plus the search's commands and the recipe for plugging in one's own oracle (the interface
the driver module expects: a function from a configuration row to an attribute row, and the
conditioning).

## 10. Future work and the final remark

Organized by the simplifying assumptions named in the body (the supervisor's rule, 2026-11-08: name them, defend them, say how to go beyond them): one facet → K > 1 (built); hard assignment with smoothing on request → nonsmooth search on the tangent cones of the ridges (the search likely tolerates kinks); the analyst's K → selection rules; small K → scalability; log-affine conditioning → GGP-compatible kernels; continuous variables within a category → discrete design variables; log-convexity for sufficiency → dents and holes; illustrative values → datasheets. Then: Scalability and performance of the solver and the search; selection of K; GGP-compatible kernel
expansions (the motivated generalization, documented, not built); estimating the configuration
Jacobian better than finite differences; discrete design variables beyond a finite comparison;
richer cases. Final remark, the hook: a novelty or impact score for new capabilities entering the
design space from how far above V = 1 they are forecast to sit.

## References, supporting material, reading paths

As v1, plus Appendix F: the search's round-by-round tables and the convergence diagnostics, and
the verified references of the three new families. Reading paths unchanged; L-F (adapt to your
own case) gains "plug in your oracle".

## Breakdown implication (for the supervisor)

The search needs code (a proposal step, Jacobian estimation from data or finite differences, a
round driver, the reference front), derivations (the new lemmas and ledger entries), a
literature pass, and a cubesat experiment with the simulator live. That is a package of its own
between the solver (WP9) and the paper (WP10), scoped with `scope-of-work` after WP9 is approved
or in parallel with it; proposed name WP12 (numbered by creation, executed before WP10).
