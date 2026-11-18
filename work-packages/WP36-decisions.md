# WP36 decisions: formal results with an interactive theorem prover, and Rust compiled to WASM (future directions)

Supervisor: Michael Zargham (`mzargham`). A research spike, in parallel with WP32, WP33 and WP35; its product is a
readout and, where relevant, future-directions text. The spike changes no mathematics, code or claim of record.

## The supervisor's direction (2026-11-12, afternoon, verbatim)

> there is another background parallel spike that i want you to get some worker agents to research: given we
> already have "business casual verification" for our mathematics in our paper, how hard would it be to use clause
> and an Interactive Theorem Prover like the one described here
> https://www.galois.com/articles/claude-can-sometimes-prove-it to develop formal results. its worth noting that
> this is not a hard requirement, its best understood as a future direction, and since formal verification is
> usually associated with languages that have stronger guarantees than python, i'd pair the LEAN proof future work
> with programming languages work focused on performance and guarantees, given my predelictions, rust; ideally
> compiling to wasm for which we can get both speed and formal guarantees. Please be advised this needs to be
> researched as and where relevant integrated as future directions.

## The assistant's reading

Two questions for worker agents, read and written up, nothing built: (1) how hard it would be to take the paper's
results, now checked step by step by plain-SymPy lemma scripts (the "business casual" check: a pencil-and-paper
substitute, never called formal verification), into an interactive theorem prover with Claude in the loop, as the
Galois article describes: which of L1 to L20 and the theorems are formalizable first (convexity, the log-mean-exp
bounds, LP support characterizations, the ridge of Corollary 1), what Lean 4 and Mathlib already hold for them,
what a floating-point implementation can and cannot inherit from a proof about real numbers, and an honest effort
estimate; (2) the pairing he names: a performance-and-guarantees implementation in Rust compiled to WebAssembly,
what verification tools exist for Rust today (and what they do and do not guarantee about numerics), what the
estimator needs from a solver (an LP, a convex program in GP form, an alternation) and what exists in Rust for
that, and what a WASM build would give the docs and the package's users. The readout carries plain options and a
draft of the future-directions paragraph for the paper (where the paper already points beyond itself) and for the
docs' limitations or theory page, each claim backed by a verified source or narrowed. The standing line holds: the
lemma scripts are not formal verification and the text never says they are.

## The synthesis readout and the placement (2026-11-13, 07:45; the assistant, under the supervisor's ruling that this is a future direction only)

The readout (`WP36-rounds/spike/readout.md`, 7b648a8) ranks the formalizable results, separates what a proof over the
real numbers inherits from what floating point does not, and gives plain options on placement, extent and follow-on
packages. The assistant's calls, in the readout's lettering:

**Assistant, verbatim:** "Placement (a): the existing future-work section of the paper, in its own cadence, not a new
section. Extent between (i) and (ii): the Lean direction with the two lemmas named first, the reals-versus-floating-point
line, and one clause for the Rust core compiled to WebAssembly; the hypotheses sentence and the Pyodide sentence are
dropped. The docs get two sentences on the limitations page where the lemma scripts are already described, saying what a
theorem-prover proof would fix and what it would not bound. Follow-on packages: (C), neither; the readout is the record,
and the supervisor said this is never a requirement. The lemma scripts stay 'a pencil-and-paper substitute'; no surface
says 'formally verified' or 'formal proof' of them."

## The search's outer loop: the supervisor's expectation, recorded for future work (2026-11-14, 12:20)

Context: the assistant, framing the bridge from the chart back to the design space (propose, predict, check), wrote
that the outer loop is "the refit after each check, which is Section 7's loop and the one thing about it that stays
open: whether it moves outward monotonically."

**Supervisor, verbatim:** "i don't expect it to move outward monotonically. it could move inward, but we could hoper
for a submartingale that moved outward in expectation, and a convergence result when it ceases to make progress in
expectation. save this feedback as part of our plan for future work. we don't need to get into solving the conditions
under which this would hold. we just need to document our approach and leave it as future work"

**Applied as:** the paper's open item on the search is restated as the supervisor expects it, in the main results'
open list, Section 7's Open sentence and the gaps ledger row that names it: the outer loop is not expected to move
outward at every step; the conjecture is a submartingale property, outward in expectation, with a convergence result
when the expected progress ceases; stated as future work, with no conditions derived (change request 169 of the
final round). The bridge-to-the-search package carries the same statement in its well-posedness note and its docs
page. The answer key's open-items line reads the same way from its next version.
