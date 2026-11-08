# Note: SymPy derivation conventions (WP1)

Sources read 2026-11-07: `/Users/z/Documents/GitHub/sympy-proof` (package `symproof`, the
supervisor's proof framework) and `/Users/z/Documents/GitHub/hc-marimo/derivation/` (plain-SymPy
chain used for the SciPy 2026 paper). Decision: use the hc-marimo plain-SymPy pattern, mirroring
symproof's ledger conventions, so the chain can later be lifted into sealed symproof bundles.

## hc-marimo pattern (copy this)

- `derivation/symbols.py`: shared symbols and canonical target expressions; `SYMBOL_ASSUMPTIONS`
  maps each strong Symbol assumption (positive, negative, integer, ...) to the axiom that licenses it.
- `derivation/axioms.py`: frozen dataclass `Axiom(name, tag, statement, relation=None, citation="")`;
  tags `POSITED`, `INHERITED` (citation required), `REGULARITY`; names `A*`, `I*`, `R*`.
- `derivation/lemma_NN_<slug>.py`: module constants `TITLE`, `STATEMENT`, `AXIOMS_USED` (list of
  axiom names; empty list with a comment for pure algebra); `derive(ctx)` writes results into a
  shared dict; `verify(ctx)` uses bare `assert sp.simplify(X - Y) == 0, "L4 FAIL: ..."`.
  Dependencies are implicit through `ctx` keys in `CHAIN` order.
- `derivation/run.py`: `CHAIN = [lemma_01, ...]`; `run_chain(verbose)` runs derive then verify per
  lemma and prints `[L{i}] PASS  TITLE / STATEMENT / axioms: ...`; `print_audit(used)` prints the
  ASSUMPTION AUDIT ledger: DERIVED, POSITED, INHERITED (with citations), REGULARITY, then a HEADLINE
  stating where the derivation breaks; exit code 0 after "ALL LEMMAS PASS."
- `test_derivation.py` (pytest): full chain; per lemma; `test_no_phantom_axioms`;
  `test_inherited_axioms_are_cited`; `test_load_bearing_symbol_assumptions_are_declared` (scans the
  symbols module for strong assumptions not registered); tag validity.
- One numeric endpoint at most in the chain, confined and seeded (hc-marimo L8 compares a
  lambdified result at 50 seeded points to 1e-10).

## symproof conventions to mirror (for later lifting)

- Three kinds of assumption: posited axioms; inherited axioms (must carry a `Citation`); external
  theorems (`expr = S.true` with description). Hypothesis = the theorem; sealed bundle = proved.
- Lemma kinds: EQUALITY (`simplify(expr - expected) == 0`), BOOLEAN (`simplify(expr) is true`, then
  `refine`, then contradiction for `Implies`), QUERY (`sympy.ask` with assumptions), PROPERTY,
  INFERENCE (justified by a named rule, not checked), COORDINATE_TRANSFORM (round trip).
- Load-bearing accounting: if `Symbol("x", positive=True)` affects verification, `x > 0` must be a
  named axiom. Every external theorem's preconditions are declared as inherited axioms.
- Docstring sections "What this proves / What this does NOT prove".

## SymPy pitfalls (from symproof's skill notes and experience)

- Build inequalities so they are not eagerly evaluated to `True`.
- The Q-system cannot derive `1 - f > 0` from `0 < f < 1`; introduce a helper symbol declared positive.
- `simplify` cancels across singularities; watch division.
- `Piecewise`, `Max`, `Min` do not simplify under assumptions; use ordering assumptions
  (e.g. s_1 > s_2) instead of `Max`.
- Limits: compute with `sympy.limit` under explicit assumptions outside the lemma, then record an
  EQUALITY `expr - value == 0`.
- Probability: `sympy.stats` (`Normal`, `E`) for the Gaussian cumulant lemma.

## This project's chain (spec §6)

Axioms A1–A6 (posited), I1–I4 (inherited with citations), R1 (regularity); lemmas L1–L10; run at
d ∈ {2, 3, 4} and n ∈ {2, 3} via `make_symbols(d, n)`. Docs state that generic-d results are proved
in prose and instantiated mechanically at these sizes.

## Abstract spaces and techniques to mimic (supervisor's direction, 2026-11-07)

- Work at symbolic d, n, K with `IndexedBase`, `Sum`/`Product` over symbolic bounds, the simplex
  constraint as a substitutable `Sum(w[j], (j, 1, d)) = 1`, and the chart basis as a `MatrixSymbol`
  with hypotheses B·Bᵀ = I, B·1 = 0. Enumerating concrete sizes is not a proof; concrete substitution
  is only a cross-check. Steps that resist abstract simplification become explicit hypotheses or
  inherited axioms in the ledger, never enumeration.
- Do not import `symproof`, but mimic its library in plain SymPy (cite file and function in a
  comment): `symproof/library/convex.py` (`convex_scalar`, `convex_hessian`, `strongly_convex`,
  `unique_minimizer`, `gp_to_convex` — log-sum-exp convexity after x = e^y), `symproof/library/
  topology.py` (`continuous_at_point` — compute `sympy.limit` outside the lemma, record the result as
  an equality), `symproof/tactics.py` (`signed_sum_lemmas` for sums of signed terms).
