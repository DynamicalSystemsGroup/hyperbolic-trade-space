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

Ledger (spec §6, as built through WP10 Amendment 2): A0 to A8 (posited), I1 to I15 (inherited with citations; I14 Jensen's inequality and I15 the definition of a generalized posynomial are used by L16; I2, I3 and I4 are `CITED_CONTEXT`, reported apart and exempt from the every-axiom-is-used test, as I7 is `SOLVER_LEVEL`), R1 and R2 (regularity), F5, F10 and F12 (fallbacks); lemmas L1–L16; run at
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

## Hypotheses are interpretive conditions, not defects (supervisor's direction, 2026-11-07)

The theory grounds the method; it need not match the implementation exactly. A theorem's hypotheses
may be conditions we cannot verify for the sampled spaces (e.g. conditioning, R1). The ledger lists
each one with (a) what it buys for understanding or interpreting results and (b) what happens to
the interpretation when it fails. The docs (WP6) carry this per result as the method's limitations.
Fewer hypotheses is not the goal; explicit, explained hypotheses are.

## Solver-level inherited entries

An inherited entry is normally consumed by a lemma, which lists it in `AXIOMS_USED`, and the audit
in `tests/test_derivation.py` checks that every such entry is used. A *solver-level* inherited
entry (`SOLVER_LEVEL` in `derivation/axioms.py`; today I7, Magnani and Boyd 2009) is a result the
implementation leans on that no lemma consumes: here, that alternating partition and refit stops at
a local optimum. It carries a role and a failure mode like every ledger entry, is printed by
`derivation/run.py` in its own audit section, and is listed instead of being checked for
consumption; the every-axiom-is-used audit covers the lemma-consumed entries only.

## Ledger classes added by WP13 (I8, I9, F12, R2)

The audit prints four more entries; each carries a role and a failure mode, and each is consumed
by a lemma, so the every-axiom-is-used test covers them
(`tests/test_derivation.py::test_wp13_new_axioms_are_declared_with_role_and_failure_mode`).

- **I8, inherited** (`INHERITED`, citation required): the first-order convexity inequality
  `f(v) >= f(w) + grad f(w).(v - w)` for a differentiable convex `f` (Boyd and Vandenberghe,
  section 3.1.3). Used by L12 to turn the simplex gap into the objective bound
  `0 <= f(w) - f* <= G`. Failure mode: a nonconvex facet objective (the penalized refit, the
  tangent refit) leaves a gap that certifies stationarity only.
- **I9, inherited**: Cauchy-Schwarz, `|a.b| <= ||a||_2 ||b||_2` (Horn and Johnson). Used by L13 to
  bound a facet-score change by the parameter change times `||(u_i, -1)||_2`, which gives the
  explicit stable radius. Failure mode: none for real vectors; the radius is sufficient, not tight.
- **F12, fallback hypothesis** (`POSITED`, `fallback=True`, as F5 and F10): the minimum `m` of a
  finite family is a symbol with `x_j >= m` for all `j` and `x_{j0} = m` for some `j0`. Used by L12
  and L13 because SymPy has no symbolic-`d` minimum. Listed in FALLBACKS and in the HEADLINE.
  Failure mode: if `m` is only a lower bound, `G = g.w - m` is an upper bound on the gap.
- **R2, regularity** (`REGULARITY`, an interpretive condition, not a defect): the assignment margin
  `gamma = min_i [s_{i,k(i)} - max_{k != k(i)} s_{ik}]` is positive, so every row has a unique
  maximizing facet. Used by L13 and L14. Role: unique maximizing facets and an assignment-stable
  neighborhood, so Proposition 3 applies. Failure mode: ridge rows at `tau = infinity` and identical
  facets give `gamma = 0`; Proposition 3 does not apply and the fit reports
  `stationary_without_margin`.

R1's wording follows L3's full simplex KKT (`g_j >= lambda`, `w_j (g_j - lambda) = 0`): the
equal-gradient reading holds on the positive-weight coordinates, and balanced hard-support
geometry does not imply an interior finite-`tau` minimizer.

## Levels 1, 2, 3 and the lemmas that carry them (WP13)

The multi-facet fit states its guarantees at three levels; each has one lemma script and a
termination field. The object each is about is named in the lemma's STATEMENT (the fitted
reference surface at finite `tau`, the `tau = infinity` supporting envelope; the Pareto boundary is
related only through L11).

| Level | Statement | Script | Ledger entries | Report field |
|---|---|---|---|---|
| 1. Descent | step B does not increase the mean slack `F(W)`; the monotone guard enforces it up to `GUARD_TOL` | L14 (the fixed-assignment expression `F(W) = sum_k (n_k/N) f_k(w_k)`), I7 (solver level) | I7, A2 | `history`, `status = guard_stop` |
| 2. Numerical stationarity | each facet's gap `G_k = g.w - min_j g_j` is small: `0 <= f_k(w_k) - f_k* <= G_k`, zero iff the simplex KKT holds (L3); `tau = infinity`: the LP duality gap | L12 (Lemma 1) | A2, A3, I1, I8, F12 | `gaps`, `max_gap`, `sum_residual`, `offset_residual` against `EPS_KKT`, `EPS_FEAS` |
| 3. Conditional local optimality | positive margin: every row's maximizing facet is unique and stable within the radius (L13, Lemma 2); with nonempty facets and exact facet optima the fit is a local minimizer of `F` (Proposition 3); with gaps, `F(W) - F*_fixed <= sum_k (n_k/N) G_k` (Corollary 4) | L13, L14 | F12, I9, R2, A2 | `gamma`, `radius`, `bound`, `status = certified` |

Level 3 is for step B, unpenalized, with support offsets `beta_k = J_tau(U w_k)`; the tangent step
and the penalty report `not_applicable`. Fallbacks follow the existing rule: a step that resists
abstract simplification becomes a declared hypothesis (F12), a partition regrouping is a stated
finite-sum step (SymPy has no symbolic partitions), and nothing is replaced by enumeration. Where
the lemma proves the formal statement and the implementation can only approach it (tolerances,
the polish, ties), the gap is a row of `docs/superpowers/notes/abstraction-gaps.md` (G-2, G-10,
G-15, G-16).

## Step kinds and the licence rule (WP10 Amendment 2)

Every proof step is one tagged line of a lemma script (`# [Ln.k] prose`), and its kind is read from
the line, never declared apart from it: *computed* (SymPy code: an assertion or a call), *by a
declared axiom* (the line applies a ledger entry the file imports by name from
`derivation.axioms`), or *by a proved result* (the line uses an earlier lemma's `L<n>_RESULT`). There
is no prose-only kind. `uv run python -m derivation.proofmap` checks tags, order, kinds and the
record; `--update` rewrites the record deliberately.

The licence rule: a logarithm or a power with a symbolic exponent is taken only through
`derivation.licence` (`log_expand`, `licensed_power`), which receives the ledger entries that
declare the positivity (or reality) it needs and raises `LicenceError` without them. A symbol that
carries a sign (`positive`, `nonnegative`, ...) is made by an entry's factory
(`A2.nonneg_base`, `R1.positive_symbol`, ...), taken from a proved result, or declared as a
hypothesis of the lemma's own statement; the checker refuses any other signed symbol.

An inherited entry used as a necessary condition states its own constraint qualification and the
lemma computes it: I10 (first-order conditions on the simplex) rests on Nocedal and Wright,
Theorem 12.1 with the LICQ of Definition 12.4, and L3 computes the LICQ (the active gradients, the
all-ones vector and e_j for each w_j = 0, are independent because A2 leaves some w_k > 0), with a
negative control (all coordinates zero: dependent). A proof does not lean on a later lemma through a
textbook (convexity, L4, is not needed for necessity).
