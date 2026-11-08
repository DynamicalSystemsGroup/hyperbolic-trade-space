"""Axiom-explicit SymPy derivation chain for the posynomial invariant form (WP1).

One script per lemma (`lemma_01_*` ... `lemma_10_*`), chained by `run.py`. Lemmas are proved at
symbolic dimension d, symbolic sample count n and symbolic term count K (abstract spaces);
concrete sizes appear only in tests as cross-checks. Every lemma declares the axioms it
invokes; the runner ends with an assumption audit separating DERIVED, POSITED, INHERITED,
REGULARITY and FALLBACKS, where each regularity condition and fallback states its interpretive
role and failure mode.

Plain SymPy, hc-marimo pattern, symproof-compatible ledger conventions. No sign/seal/hash.
"""
