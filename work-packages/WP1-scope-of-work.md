# WP1 — Scope of work: Derivations (SymPy lemma chain L1–L10, abstract spaces)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP1-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP1-decisions.md`, after the review report `work-packages/WP1-review.md` |

## Purpose

The mathematics of the method (spec §4) is load-bearing: the estimator (WP2), the preconditioning and
analysis code (WP3) and the narrative (WP6) must match exact formulas, and the narrative must be able
to cite numbered lemmas. WP1 turns each load-bearing result into a plain-SymPy lemma script with an
explicit axiom ledger, in the hc-marimo pattern and with symproof-style conventions
(`docs/superpowers/notes/proof-conventions.md`). Per the supervisor's direction (spec §6, amended
2026-11-07: "you don't need to enumerate values, you can use abstract spaces"), the lemmas are proved
at symbolic dimension d, symbolic sample count n and symbolic term count K, not by enumeration at
chosen sizes. Concrete values appear only as secondary cross-checks.

## Goals

- G1. Every load-bearing result of spec §4 listed in spec §6 as L1–L10 is a SymPy lemma script that derives its statement and verifies it as an identity (or recorded limit) for symbolic d, n and K.
- G2. The assumptions behind the chain are explicit: axioms A1–A6 (posited), I1–I4 (inherited, each cited), R1 (regularity), and any fallback hypothesis or inherited axiom forced by a step that resists abstract simplification. Each lemma declares which it uses and no Symbol assumption is smuggled in without a licensing axiom.
- G3. The chain is runnable and auditable in one command that prints PASS per lemma and a ledger separating DERIVED, POSITED, INHERITED and REGULARITY, with every fallback listed in the headline.
- G4. The chain is guarded by tests: the abstract chain, each lemma, concrete cross-checks by substitution into the abstract identities, hygiene checks, and the two numeric checks of inherited facts that spec §6 names (I1 primal versus dual, I2 replication).

## Non-goals

- No enumeration-based proofs: no lemma is established by checking instances at particular d, n or K; a concrete instance is never the proof.
- No estimator, solver or other package code under `src/` (WP2, WP3); the lemmas are standalone scripts.
- No documentation pages, no generated ledger page, no `scripts/build_generated.py` and no MkDocs content (WP6, WP8); wording WP6 can reuse is recorded in the derivation code and ledger only.
- No `symproof` dependency and no sealed bundles (spec §2); conventions are mirrored only so the chain can be lifted later.
- No new mathematics beyond L1–L10 and A/I/R as listed in spec §6; no K > 1 solver and no kernel methods (L10 verifies only the extension identities the spec lists).
- No literature or bibliography entries (WP5); inherited-axiom citations are the ones spec §6 names.
- No change to spec §4 or §6; if a derivation shows a spec formula is wrong, stop and propose an amendment.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `derivation/__init__.py` and `derivation/symbols.py`: abstract symbol namespace and `SYMBOL_ASSUMPTIONS` | G1, G2 |
| D-2 | `derivation/axioms.py`: frozen dataclass `Axiom`; tags POSITED / INHERITED / REGULARITY; A1–A6, I1–I4, R1, plus any fallback axioms | G2 |
| D-3 | `derivation/lemma_01_*.py` … `lemma_10_*.py`: ten lemma modules (file names in Agent's defaults) | G1, G2 |
| D-4 | `derivation/run.py`: `CHAIN`, `run_chain`, `print_audit`, command-line entry | G3 |
| D-5 | `tests/test_derivation.py`: abstract chain, per lemma, substitution cross-checks, hygiene, numeric checks of I1 and I2 | G4 |
| D-6 | `work-packages/WP1-decisions.md` (approval record) | G1–G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `symbols.py` provides an abstract namespace: d, n, K as positive-integer symbols; indices i, j, k; `IndexedBase` m, u (two indices), w, θ (two indices), β, c-type shifts; scalars τ, κ, σ, c, k-scale; the simplex constraint as a substitutable `Eq(Sum(w[j], (j, 1, d)), 1)`; a `MatrixSymbol` B for the chart basis. No hard-coded x, y, z or a, b, c names and no concrete dimension anywhere in the lemma modules | inspect `symbols.py` and `grep` the lemma modules for integer literals used as sizes |
| R-2 | `SYMBOL_ASSUMPTIONS` maps every strong Symbol assumption (positive, negative, integer, …) to its licensing axiom, and the hygiene test fails if a symbol carries an unregistered strong assumption | `test_load_bearing_symbol_assumptions_are_declared` passes; temporarily adding an unregistered `positive=True` symbol makes it fail (reviewer trial) |
| R-3 | `axioms.py` defines A1–A6 as POSITED, I1–I4 as INHERITED each with a non-empty citation (I1 Boyd & Vandenberghe §5.2; I2 strong law of large numbers; I3 Rockafellar §13; I4 Hoburg, Kirschen & Abbeel 2016), R1 as REGULARITY, with the statements of spec §6; A5 is stated as ε_j i.i.d. N(0, σ²), independent across j, and the independence/MGF-of-independent-sum rule is a cited item in the ledger | inspect; `test_inherited_axioms_are_cited` passes |
| R-4 | Each of the ten lemma modules defines `TITLE`, `STATEMENT`, `AXIOMS_USED`, `derive(ctx)`, `verify(ctx)` and a "what this proves / what this does NOT prove" docstring; statements and axiom lists match spec §6 as a minimum (L1 [A1,A2]; L2 [A2,A3]; L3 [A3]; L4 [A3]; L5 [A3]; L6 [A2,A5]; L7 [A1,A2]; L8 [A2]; L9 [A1,A2,A4]; L10 [A2,A6]) | inspect against spec §6; `test_each_lemma_verifies` passes |
| R-5 | Each lemma's `verify` asserts its identity symbolically for symbolic d, n, K (with `Sum`/`Product` over symbolic ranges, in log space where identities are linear in sums), with a message beginning "L<n> FAIL", covering the full content of spec §6: L1 V(k·m) = k·V(m) and V(m/V) = 1; L2 J_τ(w; U + c1ᵀ) = J_τ(w; U) + c; L3 ∇J = Σ_i p_i u_i with p = softmax(τUw) and the balanced-KKT condition; L4 second directional derivative = τ·Var_p(v·u) = (τ/2) Σ_i Σ_k p_i p_k (s_i − s_k)² ≥ 0; L5 LSE = LME + (log n)/τ, LSE − max > 0, lim_{τ→∞} LME = max, lim_{τ→0} LME = mean, mean ≤ LME ≤ max; L6 (1/τ) log E exp(τ w·ε) = τσ²‖w‖²/2; L7 elasticities −w_k/w_j and improvement factor V^{−1/w_j}; L8 round trip and Z(u + c1) = Z(u) from the hypotheses B Bᵀ = I, B1 = 0; L9 V = e^{w·b − β} Π (a_j + s_j)^{w_j α_j}; L10 Φ_K(u + c1) = Φ_K(u) + c for K terms, K = 1 reduction, lim_{κ→∞} Φ_K = max | `test_each_lemma_verifies` and `test_full_chain_runs` pass; reviewer reads each `verify` against this list |
| R-6 | β is the log-mean-exp throughout (never the unnormalized log-sum-exp as the fit objective), consistent with spec §4; the LSE appears only in L5 and L10 where the spec uses it | `grep` for `logsumexp`/`LSE` in `derivation/` and inspection against spec §4 |
| R-7 | The chain runs with no failures in abstract form: `uv run python derivation/run.py` exits 0 and prints PASS for L1–L10 with no concrete d, n or K supplied | run it |
| R-8 | `run.py` prints, once, the ASSUMPTION AUDIT ledger with sections DERIVED, POSITED, INHERITED (with citations), REGULARITY, a FALLBACKS section listing every step that was not proved abstractly (empty list printed as "none"), and a HEADLINE stating that results are proved for symbolic d, n, K, that the frontier reading requires R1, and naming each fallback; closing "ALL LEMMAS PASS." | run it and read the output |
| R-9 | `test_no_phantom_axioms`, `test_inherited_axioms_are_cited`, `test_every_used_axiom_resolves_and_all_tags_valid` pass, and every axiom A1–A6, I1–I4 and R1 is used by at least one lemma | those tests pass; `test_every_axiom_is_used` (added) passes |
| R-10 | Fallback policy: no step that resists abstract simplification is replaced by enumeration. Such a step becomes an explicitly stated hypothesis or an inherited axiom in `axioms.py` (tagged and cited as appropriate) with the reason in the lemma docstring, and appears in the FALLBACKS section and HEADLINE | inspect; `test_fallbacks_are_declared` (each fallback axiom is listed by the ledger) passes; `grep` finds no `range(`/loop over concrete sizes inside any lemma `verify` |
| R-11 | Concrete cross-checks: for each lemma where a substitution is meaningful, a test substitutes concrete values (e.g. d = 3, n = 3, K = 2) into the abstract identity and confirms it, labelled as a cross-check; the Helmert construction for L8 is verified concretely at a small d as a labelled realization check of the hypotheses B Bᵀ = I, B1 = 0 (not the theorem) | `uv run pytest tests/test_derivation.py -k crosscheck` |
| R-12 | I1 is checked numerically in pytest: at seeded random data U, the LP min_{w∈Δ} max_i w·u_i (via `scipy.optimize.linprog`) equals max_{λ∈Δ_N} min_j (Uᵀλ)_j, to the tolerance in Agent's defaults | `uv run pytest tests/test_derivation.py -k lp_duality` |
| R-13 | I2 is checked by the replication test in pytest: replicating every row of U r times leaves J_τ (hence β and w*) unchanged, to the tolerance in Agent's defaults | `uv run pytest tests/test_derivation.py -k replication` |
| R-14 | Numeric (non-symbolic) content is absent from the lemma modules (it lives in tests only); the lemma modules are symbolic | inspect for `numpy`/`scipy`/`random` imports in `derivation/` |
| R-15 | The full suite and linters pass and nothing outside the scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff` shows changes only to `derivation/`, `tests/test_derivation.py`, `pyproject.toml` (test path configuration only, if needed), `work-packages/` and the Status table | run the commands; inspect `git diff --stat` against the start commit |
| R-16 | Commits carry no AI attribution lines and are authored as Michael Zargham | `git log` with `grep -ciE 'co-authored-by|generated with'` returns 0 |

## Definition of good

- A reader of a lemma file sees at a glance what is proved (for all d, n, K), from which axioms, and what is not proved; the docstrings are precise enough that WP6 can cite them nearly verbatim.
- The lemmas fail loudly when wrong: a deliberately broken formula (reviewer's trial, not committed) makes the corresponding `verify` and test fail, with the lemma number in the message.
- Few or no fallbacks: as many steps as SymPy allows are proved abstractly, and the ledger is honest about the rest.
- The chain is fast and its output is clean enough to paste into a documentation page.
- The structure matches hc-marimo closely enough that lifting to symproof bundles later is mechanical.

## Definition of good enough

- Deliverables D-1 to D-6 exist at the stated paths.
- R-1 to R-16 pass as checked, with evidence in the review report.
- Every lemma L1–L10 passes in abstract form and every fallback, if any, is declared in the ledger (R-10).
- Non-goals untouched (no `src/` code, no docs pages, no `symproof` dependency, no enumeration-based proofs).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear below; the supervisor approves or changes the list as one item.

- Lemma file names *(default)*: `lemma_01_homogeneity.py`, `lemma_02_shift.py`, `lemma_03_gradient_kkt.py`, `lemma_04_convexity.py`, `lemma_05_lse_lme.py`, `lemma_06_gaussian_cumulant.py`, `lemma_07_elasticities.py`, `lemma_08_helmert_chart.py`, `lemma_09_pullback.py`, `lemma_10_extension.py`; numbers L1–L10 as in spec §6 (D-3). `lemma_08` keeps "helmert" in its name for spec continuity although the lemma is abstract in B; the concrete Helmert check is its cross-check.
- `derivation/` is a top-level package with `__init__.py`; tests import it via `pythonpath = ["."]` in the pytest configuration of `pyproject.toml`, with a `sys.path` insertion in `run.py` so `uv run python derivation/run.py` works as in hc-marimo *(default)* (D-1, D-4, D-5, R-15).
- Abstract namespace *(default)*: `make_symbols()` takes no size arguments and returns a `types.SimpleNamespace` with: `d`, `n`, `K` (`Symbol(..., integer=True, positive=True)`, licensed by an axiom stating they are positive integers, added to the ledger as part of A1/A2-style structural axioms or a labelled posited "sizes" axiom); indices `i`, `j`, `k` (integer); `IndexedBase` `m`, `u`, `w`, `theta`, `beta`, `s`, `a`, `alpha`, `b`; scalars `tau`, `kappa`, `sigma`, `c`, `k_scale`; `B = MatrixSymbol("B", d-1, d)`; and the simplex equation `simplex = Eq(Sum(w[j], (j, 1, d)), 1)`. τ positive (A3), κ positive (A6), σ positive (A5); m positive (A1). Further lemma-local symbols stay in the lemma.
- `SYMBOL_ASSUMPTIONS` is keyed by tag, e.g. `"tau_positive": ("tau", "positive", "A3")`, and the hygiene test iterates the symbols of the namespace, including IndexedBase assumptions *(default)*.
- Simplex handling *(default)*: w_d is not eliminated; the constraint `Sum(w[j], (j, 1, d)) = 1` is carried as an equation and substituted (via `subs`/`.subs(Sum(...), 1)` after factoring constants out of sums) where a lemma needs it.
- Log space *(default)*: lemmas work with u = log m and `Sum` over j; products Π m_j^{w_j} are rewritten as exp of Sum before verification, using the A1 positivity of m to license the log.
- `ctx` threading: `run_chain(verbose=True)` builds `ctx = {"S": make_symbols()}` and passes it through `derive` then `verify` of each lemma in `CHAIN` order; lemmas read earlier results through ctx keys *(default)*.
- Command line *(default)*: `uv run python derivation/run.py` runs the abstract chain once and prints the ledger; output lines `[L3] PASS  TITLE / STATEMENT / axioms: ...`, as hc-marimo. Cross-checks live in tests, not in `run.py`.
- Ledger *(default)*: hc-marimo's four sections in sorted name order, plus a FALLBACKS section (the axioms or hypotheses marked as fallbacks in `axioms.py`, e.g. via a `fallback=True` field on `Axiom`; printed "none" when empty) and a HEADLINE as in R-8.
- Axiom statements *(default)*: spec §6 wording; machine-checkable `relation=` supplied where SymPy can state it without eager evaluation, otherwise `None`. A5 is restated as "ε_j i.i.d. N(0, σ²), independent across j", and the rule that the MGF of a sum of independent variables is the product of MGFs is an INHERITED axiom added to the ledger (cited, e.g. Billingsley, Probability and Measure, MGF of independent sums) alongside I1–I4; this is a ledger addition beyond spec §6 and is the one additional inherited axiom named in advance.
- Axiom usage *(default)*: R1 is invoked by L3 (balanced KKT); I1 by L3 or L5 as natural; I2 by L5 (mean limit and consistency remark); I3 by L5 (support-function remark, recorded in `AXIOMS_USED`); I4 by L10. The spec's `AXIOMS_USED` lists are the minimum, additions are allowed to satisfy R-9, and the choice is noted in the docstring.
- L1, L2, L5 (identity part), L7, L9, L10 (shift identity, K = 1 reduction) *(default)*: proved abstractly by `Sum` linearity, factoring constants out of `Sum`s (`Sum.doit` with symbolic bounds), and substituting the simplex equation.
- L3 and L7 differentiation *(default)*: differentiate along a direction v through a scalar parameter t, i.e. d/dt J(w + t v) at t = 0 with `v` an `IndexedBase`, avoiding `KroneckerDelta` bookkeeping; the gradient statement ∇J = Σ_i p_i u_i is then verified as equality of directional derivatives for arbitrary v (which characterizes the gradient). For L7, elasticities are obtained as the ratio of directional derivatives along coordinate directions, using one `KroneckerDelta` direction only where needed. The implementer states in each docstring which route was used.
- L4 *(default)*: directional-derivative route, d²/dt² J(w + t v) at t = 0 equals τ·Var_p(v·u); the variance and double-sum forms are shown equal by `Sum` algebra with Σ_i p_i = 1 carried as a substitutable equation; nonnegativity of the double sum follows from p_i p_k ≥ 0 and squares (p_i positive as softmax of exponentials, A3).
- L5 limits and ordering *(default)*: lim_{τ→∞} LME = max and lim_{τ→0} LME = mean via `sympy.limit` with symbolic n where SymPy can; otherwise the max is represented by a symbol M with hypotheses s_i ≤ M for all i and s_i0 = M for some index i0, the limit is taken against that representation, and this hypothesis is stated in the docstring (and listed under FALLBACKS if it is introduced only because `sympy.limit` could not handle the Sum). The implementer states which choice was used per limit. The same applies to L10 (κ → ∞).
- L6 *(default)*: `sympy.stats` proves E exp(t ε) = exp(t²σ²/2) for one Normal; the product over j uses independence, via the added inherited MGF rule above; w·ε is treated as Σ_j w_j ε_j with symbolic d.
- L8 *(default)*: round trip and Z(u + c·1) = Z(u) are derived from the hypotheses B Bᵀ = I and B1 = 0 on a `MatrixSymbol` B with matrix algebra (the hypotheses are recorded as POSITED or fallback hypotheses on B in the ledger, licensed by a chart axiom or the L8 docstring); the round trip uses the extended orthonormal matrix [B; 1ᵀ/√d]. The Helmert basis (row k: (1,…,1, −k, 0,…)/√(k(k+1))) is built concretely in a test helper and its properties checked at a small d (default d = 4) as the labelled realization cross-check.
- L9 *(default)*: pull-back log m_j = α_j log(a_j + s_j) + b_j with α_j ≠ 0 (A4), closed form of V verified with symbolic d; negative α_j marks cost attributes as a remark in the docstring.
- L10 *(default)*: Φ_K(u) = (1/κ) log Σ_{k=1}^{K} exp(κ(θ_k·u − β_k)) with each θ_k on the simplex (A6) for symbolic K; K = 1 reduction verified by substituting K = 1 into the abstract expression.
- Cross-check tests *(default)*: parametrized over (d, n, K) ∈ {(2,2,1), (3,3,2), (4,3,3)}, substituting into the abstract identity via `doit()`; named `test_crosscheck_L<n>`; they do not replace any abstract test.
- I1 test *(default)*: `scipy.optimize.linprog` primal and dual on `numpy.random.default_rng(0)` data with N = 8 designs and each d ∈ {2,3,4}; tolerance `abs <= 1e-7`. I2 test: `default_rng(1)` data, each row replicated r = 3 times, compare J_τ at three random simplex points and at the SLSQP minimizer; tolerance 1e-9 on J_τ and 1e-6 on w*. These two stay concrete and numeric because they check inherited theorems, not chain lemmas; test helpers use numpy/scipy only and do not import `src/`.
- Test names *(default)*: `test_full_chain_runs`, `test_each_lemma_verifies`, `test_no_phantom_axioms`, `test_inherited_axioms_are_cited`, `test_load_bearing_symbol_assumptions_are_declared`, `test_every_used_axiom_resolves_and_all_tags_valid`, `test_every_axiom_is_used`, `test_fallbacks_are_declared`, `test_crosscheck_L1` … `L10`, `test_lp_duality_numeric`, `test_replication_invariance`.
- Non-obvious modelling choices are recorded in the lemma docstring ("What this proves / What this does NOT prove") and in the `STATEMENT` constant *(default)*.
- Runtime target *(default)*: the abstract chain and tests in under about 2 minutes on a laptop.
- Ruff applies to `derivation/` with the repository's configuration (line length 100) *(default)*.
- Commit granularity *(default)*: one commit per lemma or small group, then `run.py`/tests, then the Status table and decisions file; messages prefixed "WP1: ".
- Review report `work-packages/WP1-review.md` and decisions file `work-packages/WP1-decisions.md` follow the WP0 format *(default)*.

## Open decisions (for the supervisor)

None at problem level: the amended spec §6 and the confirmed breakdown answer them. The Agent's defaults list above is the one item for the supervisor to approve or change at the scope gate.
