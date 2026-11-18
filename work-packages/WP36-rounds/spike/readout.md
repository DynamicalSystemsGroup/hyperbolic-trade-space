# WP36 spike readout: a theorem prover for the paper's results, and Rust compiled to WebAssembly

Screenshots for this record: commit `2a669de`, `git show 2a669de:<path>` with `<path>` under `work-packages/WP36-rounds/`.

PM-side synthesis of `w1-theorem-prover.md`, `w2-rust-wasm.md` and `w3-sources.md`, 2026-11-12. Reading and writing only:
nothing built, no mathematics, code or claim of record changed. The SymPy lemma scripts are a pencil-and-paper
substitute; none of this makes them a formal check, and a Lean proof accepted by the kernel would be the first formal
object in the repository. Every external statement below carries a source I opened on 2026-11-12 (HTTP 200) or is
marked. "Extrapolation" means it follows from sources but nobody ran or reported it.

## 1. Ranked formalizable results, and the effort

Ranking is W1's judgement from the scripts and Mathlib's contents, not a measured difficulty. Mathlib was read at commit
`af6dcfbf` ([commit](https://github.com/leanprover-community/mathlib4/commit/af6dcfbf23867d9df7ee4835e28567fe509a2677));
"absent" means W1 grepped the names at that commit and found no declaration. Tagged steps are from
`derivation/proof_map_record.json` (505 in 20 scripts).

| Rank | Lemma(s) | Tagged steps | What the lemma needs | Mathlib status |
|---|---|---|---|---|
| 1 | L1 homogeneity, weighted geometric mean | 8 | `exp`, `log`, `rpow` identities | present |
| 2 | L2 shift of the log-mean-exp | 8 | `exp_add`, `log_mul`, finite sums | present; the log-mean-exp itself is absent and is defined in the project |
| 3 | L5 entropic soft-maximum bounds and limits | 25 | `Real.add_one_le_exp`, Jensen, `Tendsto` | present; no log-sum-exp family in Mathlib |
| 4 | L7, L8, L9, L11 elasticities, chart, pull-back, Pareto | 9, 14, 7, 20 | matrix API, affine derivatives | present |
| 5 | L10 K-term shift, K = 1, kappa to infinity | 25 | as L5, one limit | present |
| 6 | L6 Gaussian cumulant | 9 | Gaussian MGF, independent sums | present |
| 7 | L3 then L4: gradient and convexity of J_tau (Theorem 3) | 35, 24 | chain rule through a finite sum; convexity by Holder or per line | convexity on a line present; multivariable Hessian test absent; KKT with inequalities absent (I10, a hypothesis or a short proof) |
| 8 | L13 margin and Cauchy-Schwarz | 17 | `abs_real_inner_le_norm` | present |
| 9 | L18, L19 covariance cumulant, two-regime noise bound | 21, 44 | Gaussian and sub-Gaussian API, Jensen | Jensen half present; maximal inequality `E max z_i <= v sqrt(2 log n)` not found |
| 10 | L12, L14, L15 term gap and the K > 1 solver chain | 33, 20, 22 | LP strong duality, complementary slackness | absent from Mathlib; a separate Lean library proves duality ([Dvořák and Kolmogorov](https://arxiv.org/abs/2409.08119), [code](https://github.com/madvorak/duality/tree/v3.2.0)) |
| 11 | L20 Corollary 1 (ridge on the exponents) | 63 | pseudoinverse projector (I18), L18, L3, L4 | pseudoinverse absent; the script claims a first-order identity only, which is an algebraic identity plus the projector fact |
| 12 | L16, L17 soft-fit alternation and certificate | 49, 52 | second-order sufficient conditions, Hessian D - kappa M | absent |

Pilot: L1, L2, L5 (41 steps) settle the definitions every later lemma shares (simplex weights, geometric mean,
log-mean-exp). L3 and L4 then give the convexity most readers rely on. The inherited ledger entries Mathlib lacks
(I1, I12 LP duality; I10 KKT; I16 second order; I18 pseudoinverse) are why L12, L17 and L20 are last; each can stay a
stated hypothesis of the Lean theorem, as it is in the paper today.

Closest prior work: [CvxLean](https://github.com/verified-optimization/cvxlean) and
[Bentkamp, Fernández Mir and Avigad](https://arxiv.org/abs/2301.09347) verify optimization-problem reductions in Lean 4,
with a geometric-programming case study; the solver is called, not verified. I read the repository and the arXiv
record's existence, not the proofs; W3 confirmed the [ICCOPT 2025 slides](https://homepages.inf.ed.ac.uk/pbj/papers/iccopt25.pdf)
contain the figures "107 atoms" and "123 rewrite steps".

### Effort

What sources report. Dodds ([Galois, 16 September 2025](https://www.galois.com/articles/claude-can-sometimes-prove-it);
I re-read the page): Claude Code on a Lean formalization of his 2009 paper, about half of the plan done, 2,535 lines of
Lean, about 1,232 lines of proof, more than 60% definitions, each request "maybe 5-10 minutes", and his verdict "way
slower than if I'd done it by hand". Deep conceptual mistakes that the build cannot see were rare and costly; the kernel
checks the theorems, not whether the definitions say what the paper means. No total hours, no cost. Anthropic's
[Fermat's Last Theorem page](https://www.anthropic.com/research/formalizing-fermats-last-theorem) (read by W1 through a
fetch tool; I confirmed the page opens, not its figures) reports dozens of agents on an internal model over 11 days; it
is a scale reference, not a rate for one person. No source reports lemmas per week for one competent Lean user with
Claude.

Planning figures (extrapolation: one agent request of 5-10 minutes per tagged step, 3 to 5 times that for rework, 20
supervised hours a week):

| Scope | Elapsed |
|---|---|
| Pilot L1, L2, L5 | 1 to 2 weeks |
| Ranks 1 to 5 (eight easy lemmas) | 2 to 5 weeks |
| Ranks 1 to 7 (with L3, L4: Theorem 3's convexity) | 4 to 8 weeks |
| All twenty, ledger entries as hypotheses | 3 to 6 months |
| Same, with I1, I10, I12, I16, I18 proved | further months |

These are not measurements. The pilot is the measurement: run it once, record requests, hours and rework, and rescale.
Supervisor review time scales with the number of definitions, not proof lines (Dodds).

## 2. What floating point can and cannot inherit

A Lean theorem about `Real` says nothing about code run on IEEE 754 doubles; closing the gap needs a rounding-error
statement and a proof per algorithm.

| Inherits from a proof about the reals | Does not inherit |
|---|---|
| The statement's shape: which quantity is convex, which identity or bound holds in exact arithmetic | That the code computes it to a stated accuracy |
| Hypotheses made explicit (simplex, positivity, margin R2, interior R3) as conditions to check at run time | The tolerance itself |
| The algebraic rewrite the code uses: `LME(s) = max + LME(s - max)` is the stable form, so the real identity backs it | Absence of overflow, underflow or cancellation |
| Invariants a property test can compare the float code against | That a solver's output is optimal: that needs a certificate check or a verified solver |

What I opened. [Lean's reference](https://lean-lang.org/doc/reference/4.33.0/Basic-Types/Floating-Point-Numbers/) (v4.33.0)
describes a logical model of `Float`, and (per W1's reading; I confirmed the page opens) represents trigonometric
functions as opaque. Lean libraries for floating-point reasoning exist and are young: [FloatLib](https://arxiv.org/abs/2609.19352)
(arXiv, September 2026; title and authors confirmed; proofs and coverage of `exp` and `log` not read),
[FloatSpec](https://reservoir.lean-lang.org/@Beneficial-AI-Foundation/FloatSpec) and [Flean](https://github.com/minusgix/flean)
(pages open; contents per W1, not checked). The Rust standard library states that the precision of `f64::exp` and `ln`
is non-deterministic, varying by platform and Rust version, while `sqrt` is the rounded exact result
([f64 docs](https://doc.rust-lang.org/std/primitive.f64.html), re-read). The estimator's certificates already accept any
point that passes a tolerance, so they are the natural bridge: the proof backs the mathematics, the certificate checks
the float result.

## 3. Rust and WebAssembly, and what verification tools guarantee

What the estimator needs (W2, from `solvers.py`): an LP with duals at tau = infinity (HiGHS through `linprog`), a smooth
convex program on the simplex at finite tau (SLSQP plus a Newton polish), and a Python alternation over them for K > 1.
The paper's case is N = 2,134 rows, d = 13, K up to 3: small.

**Rust solvers.** [Clarabel.rs](https://github.com/oxfordcontrol/Clarabel.rs) is a pure-Rust interior-point conic solver
(LP, exponential cone, duals returned; changelog lists a wasm feature since 0.9.0) and can cover the LP; the finite-tau
program by exponential-cone rewriting is a standard reformulation not run here (extrapolation). An interior-point dual is
not a simplex dual, so the support weights could differ on tie-heavy cases (extrapolation, untested). A Rust port of
SciPy's SLSQP exists, [slsqp-rssl](https://docs.rs/slsqp-rssl), whose author reports results "not bit-identical" to SciPy
(W2, through a search summary; the docs.rs page opens, the sentence was not re-read). Nothing in Rust offers the K > 1
alternation, the certificates or a dense eigensolver: those are to be written. A second implementation is therefore a
real cost: fit, alternation, certificates, an interface, and tests against the Python outputs within certificate
tolerance, never to the last digit. The interface contract could carry a second section for a core.

**What the verification tools guarantee.** From each tool's own pages, as W2 read them:

| Tool | Guarantee | Numerics |
|---|---|---|
| Verus ([repo](https://github.com/verus-lang/verus)) | static proof that the code satisfies its specification, for a subset of Rust | W2 read "floating point: partially supported" in the guide; I could not reproduce that text (the page is script-rendered), so it is unconfirmed here |
| Creusot ([repo](https://github.com/creusot-rs/creusot)) | deductive proof of absence of panics and overflow, and of annotated correctness, through Why3 | nothing found on floating point |
| Prusti ([repo](https://github.com/viperproject/prusti-dev)) | deductive proof of absence of overflow and panics plus annotations, on a small fragment; the README calls it a prototype | nothing found on floating point |
| Kani ([book](https://model-checking.github.io/kani/)) | bounded model checking: proves, disproves with a counterexample, or runs out of resources | over-approximates `sin`, `cos`, `sqrt`; its docs say it is "unsuitable for verifying some kinds of properties (e.g. precision) about numerical algorithms" ([feature support](https://github.com/model-checking/kani/blob/main/docs/src/rust-feature-support.md), re-read) |

No page I or W2 read gives an error bound for `exp`, `ln` or a solver's iterates. What these tools can establish is the
absence of panics and overflow and any functional property one writes, about the operations as the tool models them.
Convexity and the log-mean-exp bounds are a separate proof (section 1). Which tool proves what for this estimator was
not tried. A Rust program verified this way is a stronger object than the Python package, but it still does not give a
proof of numerical accuracy.

**What WebAssembly gives.** [`wasm32-unknown-unknown`](https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html)
is a Tier 2 target; threads panic. The [core specification](https://webassembly.github.io/spec/core/exec/numerics.html)
fixes IEEE 754 round-to-nearest-even for basic arithmetic (W2's reading; page opens), so +, -, *, / and sqrt are
reproducible across engines; `exp` and `ln` come from the linked library, not the engine (extrapolation from the two
sources). Speed: the one sourced figure is general code in 2019 browsers, slower than native by an average of 45% to 55%
([Jangda et al., USENIX ATC 2019](https://www.usenix.org/conference/atc19/presentation/jangda), re-read); no figure for a
solver exists, so no speed claim is made. The case for WASM is placement, a fit in the reader's browser with no server,
not speed.

**The alternative needing no second implementation.** [Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)
lists scipy, scikit-learn, sympy, clarabel and highspy (names re-confirmed; versions per W2: scipy 1.18.0, scikit-learn
1.8.0, clarabel 0.11.1, highspy 1.13.1, for Pyodide 314.0.7). The existing package may therefore run in a browser with
the same numbers. Not tested: that it installs and fits, that `linprog(method="highs")` returns duals there, and the
package's Python pin (`>=3.12,<3.13`) against Pyodide's Python. Pyodide gives placement; it gives no formal-guarantee
story, since the numerical core is scipy's compiled code.

## 4. Source corrections

W3 resolved all 30 works (52 URLs). Two URLs in the W2 readout did not resolve as written and are corrected in
`w2-rust-wasm.md` itself, each with the dated note "2026-11-12: corrected from ... to ... per W3 sources":

- highs-js (S-9): `https://www.npmjs.com/package/highs` (403 to automated checks) to `https://registry.npmjs.org/highs`.
- slsqp-rssl (S-10): `https://rust-digger.code-maven.com/crates/slsqp-rssl` (404) to `https://docs.rs/slsqp-rssl`.

Narrowed or dropped here: W2's remark that highs-js had "no release in 12 months" is dropped (the registry record I
opened lists latest 1.15.4 and does not support it); the Verus floating-point cell is marked unconfirmed (above).
Flocq and lean-mcp-lsp are named in W1 without sources and are not relied on here. No entry has been added to
`docs/references.bib`; W3 supplied the entries for the supervisor's decision.

## 5. Draft paragraphs

**Paper, future directions** (one idea per sentence, each under fifty words):

> The lemma scripts check each step by symbolic computation, a pencil-and-paper substitute rather than a formal proof.
> A natural extension is to state selected lemmas in the Lean theorem prover, beginning with the log-mean-exp bounds and
> the convexity of the fit objective, whose analytic prerequisites Mathlib largely holds.
> Linear-programming duality, inequality-constrained optimality conditions and the pseudoinverse would remain stated hypotheses.
> A proof about real numbers backs the mathematics, not the floating-point computation, which the certificates continue to check.
> A Rust core compiled to WebAssembly is a further direction; its verification tools address panics and overflow, not numerical accuracy.

**Docs, limitations or theory page:**

> What the derivations establish. Each lemma is checked step by step by a symbolic script, a pencil-and-paper substitute;
> none is a machine-checked formal proof.
> What a formal proof would add. A Lean proof would fix the statement of a lemma over the real numbers; it would not
> bound the error of the double-precision computation.
> What the package checks at run time. Every fit returns a point tested against the certificates, whatever solver found it.
> Where the code could go. The same package may run in a browser through Pyodide; a separate Rust implementation would
> have to agree with this one within the certificate tolerances.

## 6. Options on placement (plain; the supervisor decides)

Which section, for the paper's paragraph:
- (a) the existing future-directions place, as written above;
- (b) a clause in the section on the lemma ledger where "business casual" checking is described;
- (c) not in the paper, docs only.

How much, for each surface:
- (i) the paragraph as drafted (five sentences paper, four docs);
- (ii) the first three sentences only: the Lean direction, its hypotheses, and the real-versus-float line, leaving Rust
  and WebAssembly out;
- (iii) one sentence naming both directions with no detail.

Which spike items, if any, become a scoped package:
- (A) the pilot, L1, L2 and L5 in Lean, measured, to replace the extrapolated effort with a measurement;
- (B) a Pyodide install-and-fit test of the existing package;
- (C) neither now; the readout is the record.
