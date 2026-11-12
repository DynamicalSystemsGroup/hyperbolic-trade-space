# WP36 spike W1: the interactive-theorem-prover question

Worker W1 (reading and writing only; nothing built, no change to mathematics, code or claims). Read on 2026-11-12.
Mathlib was read at commit `af6dcfbf23867d9df7ee4835e28567fe509a2677` (head of `master`, 2026-11-12, 8,706 `.lean`
files under `Mathlib/`), by `grep` over a shallow clone, not from memory. "Not found" below means: searched for the
names and phrases given, no declaration. Pages were read through a fetch tool that summarizes; wording marked as
quoted was returned as a quotation, the rest is the tool's account.

The standing line: the SymPy lemma scripts are a pencil-and-paper substitute (the "business casual" check), not
formal verification. A Lean proof checked by the kernel would be formal; nothing in this repository is one today.

## 1. What the Galois article says (Dodds, 16 September 2025)

Source: Mike Dodds, "Claude can (sometimes) prove it", Galois, https://www.galois.com/articles/claude-can-sometimes-prove-it

| Item | What the article reports |
|---|---|
| Task | Formalize in Lean his 2009 paper *Deny-Guarantee Reasoning* (fork-join concurrency, permissions, a Hoare logic); he had last worked on it about 15 years earlier |
| Agent and model | Claude Code ("not designed for theorem proving"); the article does not name the model or the plan |
| Method | Paper and technical report converted to text (Poppler); Claude writes a formalization plan with a roadmap; the author acts as project manager; statements first with `sorry`, proofs filled in later; commit after each clean build; he wrote almost no Lean himself (a few parse errors) |
| Tool added midway | `lean-mcp-lsp`: the agent can query proof state, search code and run snippets; he says it noticeably improved proving |
| Counts at time of writing | About 50% of the plan done; 2,535 lines of Lean; about 1,232 lines of proof; more than 60% of the Lean is definitions, not theorems |
| Times | "maybe 5-10 minutes" per request. **No total duration, no hours, no total cost is reported.** Plan prices only as suggestions ($20 per month useful, about $100 per month for the state-of-the-art model) |
| What worked | Many complex proof steps; work at several levels (concept, mapping to Lean, decomposition, proving, debugging) and switching between them; a refactor to finite maps on a second, closely supervised attempt; Lean's strict errors let the agent correct itself |
| What failed | Five outcome kinds: miracles (rare), slow progress (median), thrashing (fairly common, esp. changes with large blast radius), shallow persistent mistakes (fairly rare, often parsing), deep persistent mistakes (rare, very costly: a conceptual error that the build cannot see, written into comments and then trusted) |
| Verdict | "I think formalizing using AI was way slower than if I'd done it by hand" (quoted). He has less confidence in the result than in an expert formalization: the theorems are checked, the definitions would need a careful audit. Expects cost and availability to improve; advises trying it on a problem you know |

What this gives us: the kernel checks proofs, not whether the definitions say what the paper means (the deep-mistake
category); the human supervisor's expertise is what finds those. It gives line counts and a per-request time, not a
throughput.

Other cited experience (primary page read through the fetch tool; the figures are Anthropic's own):

| Source | What it reports | How it bears on us |
|---|---|---|
| Anthropic, "Formalizing Fermat's Last Theorem", https://www.anthropic.com/research/formalizing-fermats-last-theorem | An internal research model ("roughly comparable to" a model it names Fable 5.1), dozens of agents, "largely autonomously" over 11 days; 13 million lines of Lean; 29,500 intermediate theorems used (about 30,300 proved); about six billion output tokens; early attempts failed (agents lost track of project state) and were about 7% of the non-boilerplate lines; success came with Prove2Me, a graph of theorem statements with statements and proofs in separate files; the proof is checked with Lean's three standard axioms and a comparator confirms the statement matches Mathlib's FLT; a side experiment: three personal Claude Max plans formalized Vinogradov's Three Primes Theorem in three days. The article says the proof is likely longer than needed and that a formal proof does not replace a human exposition | A scale and a method (a statement graph, parallel agents), on a model that is not the one in the Dodds article and not stated to be available; no per-lemma rate; no hours of human supervision reported |
| Dvořák and Kolmogorov, https://arxiv.org/abs/2409.08119 (code: https://github.com/madvorak/duality/tree/v3.2.0) | LP duality (Farkas-like theorems, `StandardLP.strongDuality`) over linearly ordered fields in Lean 4; the abstract gives no size or time | A human-written LP duality library exists outside Mathlib; whether it was merged into Mathlib: not found (`StandardLP`, `strongDuality` do not occur in Mathlib at the commit above) |
| Bentkamp, Fernández Mir and Avigad, "Verified reductions for optimization", https://arxiv.org/abs/2301.09347; CvxLean https://github.com/verified-optimization/cvxlean | A Lean 4 framework with verified problem reductions (disciplined convex programming canonization) and a geometric programming case study; the solver (MOSEK) is called and its output is not itself verified (README: solving calls MOSEK; the page does not say "trusted", so that part is my inference); ICCOPT 2025 slides (Fernández Mir, Jackson, Bentkamp, Avigad, https://homepages.inf.ed.ac.uk/pbj/papers/iccopt25.pdf) per a search snippet only, not opened: a GP with 4 variables and 8 constraints took 123 rewrite steps; 107 atoms including log-sum-exp | The closest prior work to our setting (GP convexity by change of variables, log-sum-exp as an atom); a library to read, not a dependency to assume |

## 2. What Lean 4 and Mathlib hold today for the paper's mathematics

Mathlib commit as above. Declaration names were checked in the files named.

| Mathematics the paper uses | In Mathlib | Where | Not found / gap |
|---|---|---|---|
| Simplex as a set; convex, compact | `stdSimplex`, `convex_stdSimplex`, `isCompact_stdSimplex` | `Mathlib/Analysis/Convex/StdSimplex.lean` | |
| Convex functions; sums, compositions with linear and affine maps | `ConvexOn`, `ConvexOn.add`, `ConvexOn.comp_linearMap`, `ConvexOn.comp_affineMap` | `Mathlib/Analysis/Convex/Function.lean` | |
| Convexity of `exp`; concavity of `log` | `convexOn_exp`, `strictConvexOn_exp`, `strictConcaveOn_log_Ioi` | `Mathlib/Analysis/Convex/SpecificFunctions/Basic.lean` | |
| Jensen, finite and for expectations | `ConvexOn.map_centerMass_le`; `ConvexOn.map_integral_le` | `Mathlib/Analysis/Convex/Jensen.lean`; `Mathlib/Analysis/Convex/Integral.lean` | |
| Second-derivative convexity test (one variable) | `convexOn_of_deriv2_nonneg`, `convexOn_univ_of_deriv2_nonneg` | `Mathlib/Analysis/Convex/Deriv.lean` | The multivariable test (Hessian) and the "convex iff convex on every line" statement (I11): not found; no `Hessian` in Mathlib (a case-insensitive search of `Mathlib/*.lean` returned nothing) |
| Local minimum of a convex function is global | `IsMinOn.of_isLocalMinOn_of_convexOn` | `Mathlib/Analysis/Convex/Extrema.lean` | |
| e^x >= 1 + x | `Real.add_one_le_exp` | `Mathlib/Analysis/Complex/Exponential.lean` | |
| Weighted AM-GM | `geom_mean_le_arith_mean_weighted` (real, NNReal, ENNReal forms) | `Mathlib/Analysis/MeanInequalities.lean` | |
| Holder, Cauchy-Schwarz | `inner_le_Lp_mul_Lq`; `abs_real_inner_le_norm`, `real_inner_mul_inner_self_le` | `Mathlib/Analysis/MeanInequalities.lean`; `Mathlib/Analysis/InnerProductSpace/Basic.lean` | |
| **Log-sum-exp, log-mean-exp, softmax** | **not found** (searches: `logSumExp`, `log_sum_exp`, `logsumexp`, `softmax`) | | The function, its gradient, its convexity, the bounds `max <= LSE <= max + log n` and the entropic version must be defined and proved in the project. The convexity route by Holder is available through `inner_le_Lp_mul_Lq`; no Mathlib proof of it was found |
| Gaussian moment generating function; MGF of independent sums | `mgf_gaussianReal`; `iIndepFun.mgf_sum`, `mgf_sum_of_identDistrib`; Gaussian measures on vector spaces; `Multivariate.lean` | `Mathlib/Probability/Distributions/Gaussian/Real.lean`; `Mathlib/Probability/Moments/Basic.lean`; `Mathlib/Probability/Distributions/Gaussian/` | The linear-form-of-a-correlated-Gaussian step used by L18 (a covariance Sigma): `IsGaussian` has `map_eq_gaussianReal` for continuous linear forms, so it is plausible; I did not locate the exact statement for a given covariance matrix |
| Sub-Gaussian MGFs | `HasSubgaussianMGF` | `Mathlib/Probability/Moments/SubGaussian.lean` | A maximal inequality `E max_i z_i <= v sqrt(2 log n)` (L19): not found |
| Lagrange multipliers (equality constraints) | `IsLocalExtrOn.exists_multipliers_of_hasStrictFDerivAt` and relatives | `Mathlib/Analysis/Calculus/LagrangeMultipliers.lean` | **KKT with inequality constraints: not found; the file lists "Formalize Karush-Kuhn-Tucker theorem" under TODO** (I10, used by L3) |
| Farkas / separation by a proper cone | `ProperCone.hyperplane_separation`, `hyperplane_separation_point` | `Mathlib/Analysis/Convex/Cone/Dual.lean` | **LP strong duality and complementary slackness: not found.** `Cone/Basic.lean` lists "Define linear programs and prove LP duality as a special case of cone duality" and "Prove regular and strong duality for cone programs" under TODO. A separate library proves it: Dvořák and Kolmogorov (above), outside Mathlib |
| Implicit function theorem | `ImplicitFunctionData`, `.implicitFunction` and its API; a contracting-differentiability version | `Mathlib/Analysis/Calculus/Implicit.lean`, `ImplicitContDiff.lean`, `ImplicitFunction/` | |
| Moore-Penrose pseudoinverse | **not found** (the only hit is a docstring in `NonsingularInverse.lean` saying pseudoinverses "we do not consider here") | | I18 (X^+ X is the orthogonal projector onto the range of a symmetric X) would be proved for symmetric matrices from the spectral theorem or declared as a hypothesis |
| Geometric program; posynomial; generalized posynomial | **not found in Mathlib**; CvxLean has a GP case study | CvxLean (above) | Posynomial, GP standard form, and the change of variables x = e^y are definitions plus short proofs in the project, or taken from CvxLean |

Reading of the table. The elementary analysis (exp, log, Jensen, Cauchy-Schwarz, AM-GM, convex-set API, Gaussian MGF,
independence) is in Mathlib. What the paper's inherited ledger needs and Mathlib lacks: LP strong duality and
complementary slackness (I1, I12), KKT with inequalities (I10), multivariable second-order tests and Hessians (I11,
I16), the pseudoinverse (I18), and the log-sum-exp family itself.

## 3. The paper's lemma inventory (from `derivation/`)

Source of the list and counts: `derivation/proof_map_record.json` (the committed record of the proof-map checker, Appendix B;
`tests/test_proof_map.py` and `paper/test_proof_map.py` check it), `derivation/lemma_NN_*.py` and `derivation/axioms.py`.
Twenty lemma scripts, 505 tagged steps (333 `computed`, 160 `axiom` applications, 12 `result` imports), written in plain
SymPy over symbolic d, n, K.

| L | Content (script TITLE, shortened) | Tagged steps | Inherited / regularity entries used | Imports |
|---|---|---|---|---|
| 1 | Homogeneity; invariant form of the weighted geometric mean | 8 | none | |
| 2 | Uniform shift of the data shifts the soft-max fit | 8 | none | |
| 3 | Gradient of J_tau (softmax-weighted mean); balanced KKT | 35 | I10, R1 | |
| 4 | Convexity of J_tau: second directional derivative = tau Var_p | 24 | I11, I13 | L3 |
| 5 | LSE vs LME: offset, bounds, temperature limits | 25 | F5 | |
| 6 | Gaussian cumulant of a weighted noise sum | 9 | I5 | |
| 7 | Elasticities; single-metric improvement factor | 9 | none | L1 |
| 8 | Sum-zero (Helmert) chart bijection | 14 | I6 | |
| 9 | Pull-back through the conditioning | 7 | none | |
| 10 | K-term extension: shift equivariance, K = 1, kappa to infinity | 25 | F10 | |
| 11 | A maximizer of V is Pareto-efficient (weighted-sum, one direction) | 20 | none | |
| 12 | Simplex first-order gap bounds a term refit's suboptimality | 33 | I1, I8, I12, F12 | L4 |
| 13 | Assignment margin and assignment-stable radius | 17 | I9, R2, F12 | |
| 14 | Assignment-stable local optimality (two results) | 20 | R2 | L12, L13 |
| 15 | Descent of one step-B iteration (two results) | 22 | F12 | L12, L14 |
| 16 | Soft-weight alternation: symmetry, bound, generalized posynomial | 49 | I14, I15 | |
| 17 | Soft-fit certificate: gradient, Hessian D - kappa M, second-order test | 52 | I16 | |
| 18 | Gaussian cumulant with a noise covariance; conditioning as error map | 21 | none (A9, A10 posited) | |
| 19 | Two-regime upper bound on the noise shift (not tight) | 44 | I17, F5, F19 | |
| 20 | Noise on the metrics is a ridge on the exponents; first-order shift (Corollary 1) | 63 | I9, I18, R3 | L18, L3, L4 |

Entry codes are those of `derivation/axioms.py`: I = inherited from a cited source (I1 LP strong duality, I5 MGF of
independent sums, I6 square matrix left inverse is right inverse, I8 first-order convexity inequality, I9
Cauchy-Schwarz, I10 first-order KKT, I11 convexity along lines, I12 complementary slackness, I13 GP form, I14 Jensen,
I15 generalized posynomial, I16 second-order sufficient conditions, I17 expectation linear and Jensen, I18
pseudoinverse projector); R = regularity hypotheses (R1 balanced point in the relative interior of a facet, R2
positive margin, R3 interior and well-conditioned clean fit); F = fallbacks (F5, F10, F12, F19: representation devices
of the scripts, for example the min representation F12). A, the posited axioms (A0 to A11), are modelling
assumptions (simplex, positivity, Gaussian noise, partition of rows) and would become hypotheses of the Lean theorems.

Two honest facts for the translation. First, the scripts run at symbolic d, n, K with `Sum` over symbolic bounds and
`IndexedBase`; each step is an equality or sign check that SymPy simplifies. A Lean proof has to prove each step with
a tactic or term; the 505 steps are the outline, not a measure of Lean lines (Dodds's Lean was 2,535 lines for about
half a plan, and more than 60% of it definitions). Second, the "axiom" steps apply a ledger entry; in Lean each
entry is either a Mathlib theorem (I8 in 1-D, I9, I14, I17 for finite sums and integrals), a theorem from another
library (I1, I12 from Dvořák and Kolmogorov, if their setting fits), or a hypothesis stated in the theorem, as it is
in the paper today.

## 4. Ranking: which lemmas to formalize first

Criteria: what the lemma needs from Mathlib (above); the real-analysis content (differentiation through sums,
limits, second-order information, measure theory); dependence (a lemma blocks those that import it); and what the
reader gains (L3, L4, L5, L12 and L20 carry the paper's claims). The ranking is my judgement from the scripts and
Mathlib's contents, not a measured difficulty.

| Rank | Lemma | Why first (or not) | Needs from Mathlib | Real-analysis content | Unblocks |
|---|---|---|---|---|---|
| 1 | L1 | Pure algebra of `exp`, `log`, `rpow` on the simplex; smallest script (8 steps); a good pilot for definitions (simplex weights, geometric mean) | `Real.rpow`, `exp`, `log`, `Finset.prod` | none beyond identities | L7 |
| 2 | L2 | Shift identity of the log-mean-exp (8 steps); fixes the project's definition of log-mean-exp, which Mathlib lacks | `exp_add`, `log_mul`, `Finset.sum` | none | the LME API for L5, L10, L19, L20 |
| 3 | L5 | The entropic soft-maximum bounds and limits (25 steps); the paper's central distinction (log-mean-exp, never the unnormalized log-sum-exp) | `Real.add_one_le_exp`, `ConvexOn.map_centerMass_le`, `Finset.sup'`, `Tendsto` | bounds are elementary; the two limits in tau use `Tendsto` | L19 |
| 4 | L11, L9, L8, L7 | Short, algebraic: Pareto (20), pull-back (7), chart (14; square-matrix inverse), elasticities (9; a directional derivative of an affine function) | `Matrix` API; `HasDerivAt` of affine maps | trivial | none downstream except L7 from L1 |
| 5 | L10 | K-term Phi_K: shift equivariance, K = 1, kappa to infinity (25) | as L5 | one limit (squeeze) | none |
| 6 | L6 | Gaussian cumulant (9 steps) is short, but needs probability set-up: independent Gaussian family on a space | `mgf_gaussianReal`, `iIndepFun.mgf_sum` (found) | measure theory | L18, L19, L20 |
| 7 | L3, then L4 | The gradient of J_tau (35) and convexity (24), the core of Theorem 3. Differentiation through a finite sum of exponentials is standard (chain rule); the "second directional derivative = tau Var_p" is the same, per line. I10 (KKT) would be a hypothesis or a proof by the simplex's structure; I11 is bypassed by proving `ConvexOn` directly (Holder route or `convexOn_of_deriv2_nonneg` per line then lifting by hand: the lifting lemma was not found) | `HasDerivAt`, `convexOn_of_deriv2_nonneg`, `inner_le_Lp_mul_Lq` | first and second derivatives of a log of a sum of exps; no Hessian API | L12, L20 |
| 8 | L13 | Margin arithmetic and Cauchy-Schwarz (17) | `abs_real_inner_le_norm` | none | L14 |
| 9 | L18, L19 | Covariance version of L6 (21); the two-regime bound (44): the Jensen half (tau v^2/2) and the tangent-line half are in reach; `E max_i z_i <= v sqrt(2 log n)` not found, so it needs a sub-Gaussian maximal inequality built on `HasSubgaussianMGF` | `ConvexOn.map_integral_le`, Gaussian API | integrals, maximum of random variables | L20 |
| 10 | L12, L14, L15 | The solver chain for K > 1: term gap (33) uses LP duality (I1) and complementary slackness (I12), absent from Mathlib; L14 and L15 (20, 22) are regrouping of sums and then depend on L12, L13 | `ProperCone.hyperplane_separation` is a start toward I1; or the Dvořák-Kolmogorov library | finite-dimensional convex analysis on the simplex | L14, L15 |
| 11 | L20 (Corollary 1) | The largest script (63 steps), imports L18, L3, L4; uses the pseudoinverse (I18) which Mathlib lacks; the script proves a first-order identity and says there is "no bound on the remainder": a Lean statement of exactly that is an algebraic identity on a face plus the projector fact. A statement that w* moves differentiably with Sigma (the implicit function theorem, `ImplicitFunctionData`) is not what the script claims and would be new mathematics | symmetric-matrix spectral theory; `Matrix`; implicit function theorem if one wants more | linear algebra on the tangent space of a face; invertible-Hessian conditions (R3) | |
| 12 | L16, L17 | Largest soft-fit scripts (49, 52); L17 needs second-order sufficient conditions (I16) with a Hessian D - kappa M: no Hessian, no second-order optimality in Mathlib; L16 needs generalized-posynomial structure (I15, I14) | `ConvexOn.map_centerMass_le`; the rest to be built | second-order calculus in several variables | none |

The first three ranks form a pilot: L1, L2 and L5 (41 tagged steps), enough to settle the project's definitions
(simplex weights, geometric mean, log-mean-exp) that every later lemma shares. L3 and L4 then give Theorem 3's convexity, the claim most
readers rely on. What Mathlib does not have (LP duality, KKT with inequalities, Hessians, pseudoinverse, the
log-sum-exp family) sits in L3's I10 (hypothesis or small proof), L12 (I1, I12), L17 (I16) and L20 (I18), which
is why they are last.

## 5. What a floating-point implementation can and cannot inherit from a proof about real numbers

Facts, each with its source:

- A Lean theorem about `Real` (Mathlib's real numbers) says nothing by itself about code run on IEEE 754 doubles: the
  proof is about the mathematical function, the code computes rounded operations. Closing this gap needs a statement
  of the rounding error and a proof that the algorithm's result is within it. That is a separate body of work in Coq
  (Flocq) and, for Lean, new libraries: FloatSpec (a port of Flocq, incomplete, with `sorry` while porting;
  https://reservoir.lean-lang.org/@Beneficial-AI-Foundation/FloatSpec), Flean (formats, the five IEEE rounding modes,
  error bounds; https://github.com/minusgix/flean), and FloatLib (arXiv 2609.19352, https://arxiv.org/abs/2609.19352:
  verified arbitrary-precision floating-point arithmetic, "numerical theorems connect execution to real rounding,
  error bounds, and exactness"; the abstract does not mention `exp` or `log`). I read the abstracts or pages, not the
  proofs, and did not check their coverage.
- Lean's own `Float`: the reference (https://lean-lang.org/doc/reference/4.33.0/Basic-Types/Floating-Point-Numbers/)
  describes a logical model `Float.Model`, a 64-bit unsigned integer type with a canonical NaN, "extensively
  empirically tested" against the hardware; says other operations "such as trigonometric functions, are represented
  as opaque functions in Lean's logic" (it does not address `exp` or `log` by name in what I read); and says "Do
  not use this model as the basis of a more extensive floating-point library".
- The package's estimator uses `exp`, `log`, a softmax and linear algebra (NumPy and SciPy today). The library
  functions `exp` and `log` of a floating-point runtime are accurate to a bound that the runtime documents, not a
  property that a Mathlib proof supplies.

What each side can inherit (my reading of those facts; the first two lines are what a proof about reals gives, the rest what it does not):

| Inherits | Does not inherit |
|---|---|
| The statement's shape: which quantity is convex, which identity holds, which bound is valid in exact arithmetic | That the code computes it to any stated accuracy (needs a rounding-error theorem per algorithm) |
| The invariants the code can be tested against: a property test and the float code agree up to a tolerance you choose | The tolerance itself: a Lean theorem about reals does not give it |
| Hypotheses made explicit (positivity, simplex, a margin R2, interior R3) as the conditions to check at run time | That the solver's output (an LP, convex program, alternation) is optimal: that needs a certificate checker or a verified solver; CvxLean calls MOSEK and verifies the reduction, not the solver's answer (README; the page does not say "trusted", my inference) |
| Log-mean-exp's stable form: the real identity `LME(s) = max + LME(s - max)` is exactly what the stable implementation uses, so the proof backs the rewrite | Absence of overflow, underflow or catastrophic cancellation; those are properties of the float form, not the real one |

A proof about reals therefore backs the mathematics and the algebraic rewrites the code uses. It leaves the
numerical claims (accuracy, convergence of a float alternation) to a separate floating-point proof or to tests.

## 6. Effort estimate

What the sources give, and what they do not:

- Dodds: lines (2,535 total, 1,232 proof, over 60% definitions, about half of the plan), 5-10 minutes per request,
  and a verdict that it was slower than by hand. **No total time, no lemmas per week.**
- Anthropic's FLT: 11 days, 13 million lines, 29,500 theorems used, about six billion output tokens, dozens of agents;
  Vinogradov's Three Primes in three days with three Max plans. No human hours; the model is an internal one in the FLT case.
- No source I found reports a lemmas-per-week rate for one competent Lean user with Claude in the loop.
  So every rate below is an **extrapolation**, with its assumption in plain view.

Arithmetic you can check (all assumptions mine):

| Quantity | Value | Basis |
|---|---|---|
| Tagged steps in the 20 scripts | 505 | `proof_map_record.json` (checked) |
| Tagged steps, pilot (L1, L2, L5) | 41 | same |
| Tagged steps, ranks 1 to 5 (L1, L2, L5, L7 to L11) | 8+8+25+9+14+7+20+25 = 116 | same |
| Tagged steps, ranks 1 to 7 (above plus L6, L3, L4) | 116 + 9 + 35 + 24 = 184 | same |
| Request time, assumption "one agent request per tagged step" at 5-10 minutes | 41 steps: 3.4 to 6.8 h; 116 steps: 9.7 to 19.3 h; 184 steps: 15.3 to 30.7 h; 505 steps: 42 to 84 h | Dodds's 5-10 minutes per request (checked); the one-request-per-step assumption is **extrapolation** |
| Rework and definition factor | Unknown. Dodds reports thrashing as "fairly common" and over 60% of the code as definitions; take a range of 3 to 5 times the request time as a planning assumption | **extrapolation** |
| Supervised hours per week of a competent Lean user | Take 20 as a planning assumption | **extrapolation** |

Resulting planning figures (extrapolation, not measured):

| Scope | Elapsed estimate at 20 supervised hours per week |
|---|---|
| Pilot, L1 + L2 + L5 | roughly 1 to 2 weeks, mostly the shared definitions and their review |
| Ranks 1 to 5, eight easy lemmas | roughly 2 to 5 weeks |
| Ranks 1 to 7, with L3 and L4 (Theorem 3 convexity) | roughly 4 to 8 weeks |
| All twenty lemmas, ledger entries as stated hypotheses | roughly 3 to 6 months; the lower half if LP duality, KKT and the pseudoinverse stay as hypotheses, the upper half if L12 and L17 need their own libraries |
| The same, with I1, I10, I12, I16 and I18 proved rather than assumed | further months; LP duality alone is a published formalization in its own right (Dvořák and Kolmogorov) |

Read these as lemma counts per week: about 1 to 2 small lemmas per week in the pilot range, falling to a lemma every one
to two weeks for L12, L16, L17 and L20. The numbers are unsourced extrapolations; the way to make them a measurement
is to run the pilot (L1, L2, L5) once, record requests, hours and rework, and re-scale this table.

What the effort buys (and not): a kernel-checked proof of the lemma as stated in Lean; the definitions still need a
human audit (Dodds), so the supervisor's review time scales with the number of definitions, not with the number of
proof lines. The paper's claims stay as they are; a Lean theorem would be a stronger status for individual lemmas, to
be added lemma by lemma, never claimed for the SymPy scripts.

## 7. Findings for the future-directions text (each backed or narrowed)

1. The Galois article reports a partial formalization (about half a plan, 2,535 lines) with Claude Code and a
   verdict that it was slower than by hand; it gives no total time.
2. Mathlib holds the elementary analysis the paper uses (simplex, convex functions, Jensen, Cauchy-Schwarz, AM-GM,
   Gaussian MGF, independent sums, the implicit function theorem) and lacks the log-sum-exp family, LP duality and
   complementary slackness, KKT with inequalities, Hessians, and the pseudoinverse.
3. Lemmas L1, L2, L5 (then L7 to L11, L6, L3, L4) can be taken first; L12, L16, L17 and L20 last.
4. A Lean proof about real numbers backs the mathematics and the algebraic rewrites; it does not by itself back the
   float computation (accuracy, convergence); Lean's `Float` has a logical model for bit-level operations and treats
   transcendental functions as opaque.
5. The effort is not measured by any source; the planning figures in section 6 are extrapolations from 5-10 minutes
   per request and 505 tagged steps, with a pilot proposed to turn them into a measurement.

## Sources

- Dodds, M., "Claude can (sometimes) prove it", Galois, 16 September 2025. https://www.galois.com/articles/claude-can-sometimes-prove-it
- Anthropic, "Formalizing Fermat's Last Theorem". https://www.anthropic.com/research/formalizing-fermats-last-theorem
- Mathlib4, commit af6dcfbf23867d9df7ee4835e28567fe509a2677 (2026-11-12). https://github.com/leanprover-community/mathlib4
  Files cited: `Mathlib/Analysis/Convex/{StdSimplex,Function,Jensen,Integral,Deriv,Extrema}.lean`,
  `Mathlib/Analysis/Convex/SpecificFunctions/Basic.lean`, `Mathlib/Analysis/Convex/Cone/{Basic,Dual}.lean`,
  `Mathlib/Analysis/Calculus/{LagrangeMultipliers,Implicit,ImplicitContDiff}.lean`, `Mathlib/Analysis/MeanInequalities.lean`,
  `Mathlib/Analysis/InnerProductSpace/Basic.lean`, `Mathlib/Analysis/Complex/Exponential.lean`,
  `Mathlib/Probability/Moments/{Basic,SubGaussian}.lean`, `Mathlib/Probability/Distributions/Gaussian/{Real,Basic}.lean`,
  `Mathlib/LinearAlgebra/Matrix/NonsingularInverse.lean`.
- Dvořák, M., Kolmogorov, V., "Duality theory in linear optimization and its extensions, formally verified". https://arxiv.org/abs/2409.08119 ; code https://github.com/madvorak/duality/tree/v3.2.0
- Bentkamp, A., Fernández Mir, R., Avigad, J., "Verified reductions for optimization". https://arxiv.org/abs/2301.09347 ; CvxLean https://github.com/verified-optimization/cvxlean ; ICCOPT 2025 slides https://homepages.inf.ed.ac.uk/pbj/papers/iccopt25.pdf (snippet only)
- Lean Language Reference, floating-point numbers (v4.33.0). https://lean-lang.org/doc/reference/4.33.0/Basic-Types/Floating-Point-Numbers/
- FloatLib, arXiv 2609.19352. https://arxiv.org/abs/2609.19352 ; FloatSpec https://reservoir.lean-lang.org/@Beneficial-AI-Foundation/FloatSpec ; Flean https://github.com/minusgix/flean
- This repository: `derivation/proof_map_record.json`, `derivation/lemma_01_*.py` to `lemma_20_*.py`, `derivation/axioms.py`, `docs/superpowers/notes/proof-conventions.md`, `work-packages/WP36-decisions.md`.
