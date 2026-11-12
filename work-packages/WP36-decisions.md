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
