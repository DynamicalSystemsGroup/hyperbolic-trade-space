# WP1 — Scope of work: Derivations (SymPy lemma chain L1–L10)

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
(`docs/superpowers/notes/proof-conventions.md`), instantiated mechanically at several sizes, so that
every later package has machine-checked formulas and lemma numbers to point at.

## Goals

- G1. Every load-bearing result of spec §4 listed in spec §6 as L1–L10 is a SymPy lemma script that derives its statement and verifies it as an identity (or recorded limit) at d ∈ {2, 3, 4} and n ∈ {2, 3}.
- G2. The assumptions behind the chain are explicit: axioms A1–A6 (posited), I1–I4 (inherited, each cited), R1 (regularity), each lemma declares which it uses, and no Symbol assumption is smuggled in without a licensing axiom.
- G3. The chain is runnable and auditable in one command that prints PASS per lemma and a ledger separating DERIVED, POSITED, INHERITED and REGULARITY.
- G4. The chain is guarded by tests, including the two inherited facts that spec §6 says are checked numerically (I1 by primal versus dual, I2 by replication).

## Non-goals

- No estimator, solver or other package code under `src/` (WP2, WP3); the lemmas are standalone scripts.
- No documentation pages, no generated ledger page, no `scripts/build_generated.py` and no MkDocs content (WP6, WP8); the statement that generic-d results are proved in prose and instantiated mechanically is recorded in the derivation code and ledger only, as text WP6 can reuse.
- No `symproof` dependency and no sealed bundles (spec §2: not on PyPI, tree mid-merge); conventions are mirrored only so the chain can be lifted later.
- No machine proof for generic d or n: instantiation at d ∈ {2, 3, 4}, n ∈ {2, 3} only.
- No new mathematics beyond L1–L10 and A/I/R as listed in spec §6; no K > 1 solver and no kernel methods (L10 verifies only the extension identities the spec lists).
- No literature or bibliography entries (WP5); inherited-axiom citations are the ones spec §6 names.
- No change to spec §4 or §6; if a derivation shows a spec formula is wrong, stop and propose an amendment.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `derivation/__init__.py` and `derivation/symbols.py`: `make_symbols(d, n)` and `SYMBOL_ASSUMPTIONS` | G1, G2 |
| D-2 | `derivation/axioms.py`: frozen dataclass `Axiom`; tags POSITED / INHERITED / REGULARITY; A1–A6, I1–I4, R1 | G2 |
| D-3 | `derivation/lemma_01_*.py` … `lemma_10_*.py`: ten lemma modules (file names in Agent's defaults) | G1, G2 |
| D-4 | `derivation/run.py`: `CHAIN`, `run_chain`, `print_audit`, command-line entry | G3 |
| D-5 | `tests/test_derivation.py`: chain, per-lemma, hygiene, and numeric checks of I1 and I2 | G4 |
| D-6 | `work-packages/WP1-decisions.md` (approval record) | G1–G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `make_symbols(d, n)` returns the symbols of spec §6 for d ≥ 2, n ≥ 2: w_1..w_{d−1} with w_d = 1 − Σ, u_{ij} (i ≤ n, j ≤ d), τ, κ, σ, c, k; no hard-coded x, y, z or a, b, c names; the dimension is a parameter | inspect `symbols.py`; `uv run pytest tests/test_derivation.py` passes for d ∈ {2,3,4} (parametrized) |
| R-2 | `SYMBOL_ASSUMPTIONS` maps every strong Symbol assumption (positive, negative, integer, …) to its licensing axiom, and the hygiene test fails if a symbol carries an unregistered strong assumption | `test_load_bearing_symbol_assumptions_are_declared` passes; temporarily adding an unregistered `positive=True` symbol makes it fail (reviewer trial) |
| R-3 | `axioms.py` defines A1–A6 as POSITED, I1–I4 as INHERITED each with a non-empty citation (I1 Boyd & Vandenberghe §5.2; I2 strong law of large numbers; I3 Rockafellar §13; I4 Hoburg, Kirschen & Abbeel 2016), and R1 as REGULARITY, with the statements of spec §6 | inspect; `test_inherited_axioms_are_cited` passes |
| R-4 | Each of the ten lemma modules defines `TITLE`, `STATEMENT`, `AXIOMS_USED`, `derive(ctx)`, `verify(ctx)` and a "what this proves / what this does NOT prove" docstring; the statements and axiom lists match spec §6 (L1 [A1,A2]; L2 [A2,A3]; L3 [A3]; L4 [A3]; L5 [A3]; L6 [A2,A5]; L7 [A1,A2]; L8 [A2]; L9 [A1,A2,A4]; L10 [A2,A6]) | inspect against spec §6; `test_each_lemma_verifies` passes |
| R-5 | Each lemma's `verify` asserts its identity symbolically (`simplify(X − Y) == 0` style, with a message beginning "L<n> FAIL"), covering the full content listed in spec §6: L1 V(k·m) = k·V(m) and V(m/V) = 1; L2 J_τ(w; U + c1ᵀ) = J_τ(w; U) + c; L3 ∇J = Σ_i p_i u_i with p = softmax(τUw) and the balanced-KKT condition; L4 second directional derivative = τ·Var_p(v·u) = (τ/2) Σ_i Σ_k p_i p_k (s_i − s_k)² ≥ 0; L5 LSE = LME + (log n)/τ, LSE − max > 0, lim_{τ→∞} LME = max, lim_{τ→0} LME = mean, mean ≤ LME ≤ max; L6 (1/τ) log E exp(τ w·ε) = τσ²‖w‖²/2 via `sympy.stats`; L7 elasticities −w_k/w_j and improvement factor V^{−1/w_j}; L8 B Bᵀ = I, B1 = 0, round trip, Z(u + c1) = Z(u) for the Helmert basis; L9 V = e^{w·b − β} Π (a_j + s_j)^{w_j α_j}; L10 Φ_2(u + c1) = Φ_2(u) + c, K = 1 reduction, lim_{κ→∞} Φ_2 = max | `test_each_lemma_verifies` and `test_full_chain_runs` pass; reviewer reads each `verify` against this list |
| R-6 | β is the log-mean-exp throughout (never the unnormalized log-sum-exp as the fit objective), consistent with spec §4; the LSE appears only in L5 and L10 where the spec uses it | `grep` for `logsumexp`/`LSE` in `derivation/` and inspection against spec §4 |
| R-7 | The chain runs at every combination d ∈ {2,3,4}, n ∈ {2,3} (six runs) with no failures | `uv run python derivation/run.py` exits 0 and prints PASS for L1–L10 for each combination; the parametrized pytest cases pass |
| R-8 | `run.py` prints, once, the ASSUMPTION AUDIT ledger with sections DERIVED, POSITED, INHERITED (with citations), REGULARITY and a HEADLINE naming where the derivation stops being valid (R1: balanced point off a facet's relative interior or normal not positive), and a closing "ALL LEMMAS PASS." | run it and read the output |
| R-9 | `test_no_phantom_axioms`, `test_inherited_axioms_are_cited`, `test_every_used_axiom_resolves_and_all_tags_valid` pass, and every axiom A1–A6, I1–I4 and R1 is used by at least one lemma | those tests pass; `test_every_axiom_is_used` (added) passes |
| R-10 | I1 is checked numerically in pytest: at seeded random data U, the LP min_{w∈Δ} max_i w·u_i (via `scipy.optimize.linprog`) equals max_{λ∈Δ_N} min_j (Uᵀλ)_j, to the tolerance in Agent's defaults | `uv run pytest tests/test_derivation.py -k lp_duality` |
| R-11 | I2 is checked by the replication test in pytest: replicating every row of U r times leaves J_τ (hence β and w*) unchanged, to the tolerance in Agent's defaults | `uv run pytest tests/test_derivation.py -k replication` |
| R-12 | The only numeric (non-symbolic) content in the chain proper is confined and seeded; the I1 and I2 checks live in the tests, not in lemma modules | inspect for `numpy`/`scipy`/`random` use in `derivation/`; any use is seeded and noted in the lemma docstring |
| R-13 | The full suite and linters pass and nothing outside the scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff` shows changes only to `derivation/`, `tests/test_derivation.py`, `pyproject.toml` (test path configuration only, if needed), `work-packages/` and the Status table | run the commands; inspect `git diff --stat` against the start commit |
| R-14 | Commits carry no AI attribution lines and are authored as Michael Zargham | `git log` with `grep -ciE 'co-authored-by|generated with'` returns 0 |

## Definition of good

- A reader of a lemma file sees at a glance what is proved, from which axioms, and what is not proved; the docstrings are precise enough that WP6 can cite them nearly verbatim.
- The lemmas fail loudly when wrong: a deliberately broken formula (reviewer's trial, not committed) makes the corresponding `verify` and test fail, with the lemma number in the message.
- The chain is fast (full six-run grid under a couple of minutes) and its output is clean enough to paste into a documentation page.
- The ledger honestly says which results are proved symbolically at instantiated sizes and which rest on inherited theorems, so no later document overclaims.
- The structure matches hc-marimo closely enough that lifting to symproof bundles later is mechanical.

## Definition of good enough

- Deliverables D-1 to D-6 exist at the stated paths.
- R-1 to R-14 pass as checked, with evidence in the review report.
- Every lemma L1–L10 passes at all six (d, n) combinations and the ledger prints as specified.
- Non-goals untouched (no `src/` code, no docs pages, no `symproof` dependency).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear below; the supervisor approves or changes the list as one item.

- Lemma file names *(default)*: `lemma_01_homogeneity.py`, `lemma_02_shift.py`, `lemma_03_gradient_kkt.py`, `lemma_04_convexity.py`, `lemma_05_lse_lme.py`, `lemma_06_gaussian_cumulant.py`, `lemma_07_elasticities.py`, `lemma_08_helmert_chart.py`, `lemma_09_pullback.py`, `lemma_10_extension.py`; lemma numbers L1–L10 exactly as in spec §6 (appears in D-3).
- `derivation/` is a top-level package with `__init__.py`; tests import it via `pythonpath = ["."]` in the pytest configuration of `pyproject.toml`, with a `sys.path` insertion in `run.py` so `uv run python derivation/run.py` works as in hc-marimo *(default)* (D-1, D-4, D-5, R-13).
- `make_symbols(d, n)` returns a `types.SimpleNamespace`-like object (attribute access) holding: `w` (list of d entries, w_d = 1 − Σ_{j<d} w_j), `u` (n×d `sympy.Matrix`), `tau`, `kappa`, `sigma`, `c`, `k` (positive-declared where an axiom licenses it: τ by A3, κ by A6, σ by A5; real otherwise), plus helpers `ones`, `p` (softmax weights as expressions), `J` (the log-mean-exp objective) *(default)*. Names: `tau`, `kappa`, `sigma`, `c`, `k`, `u`, `w`, `d`, `n`. Further lemma-local symbols (e.g. α_j, b_j, s_j, a_j for L9; θ_k, β_k for L10) are created in `make_symbols` too when shared and in the lemma otherwise *(default)*.
- `SYMBOL_ASSUMPTIONS` is keyed by tag (e.g. `"tau_positive": ("tau", "positive", "A3")`), same shape as hc-marimo, and the hygiene test iterates the symbols of a sample `make_symbols(2, 2)` *(default)*.
- `ctx` threading: `run_chain(d, n, verbose=True)` builds `ctx = {"d": d, "n": n, "S": make_symbols(d, n)}` and passes it through `derive` then `verify` of each lemma in `CHAIN` order; lemmas read earlier results through ctx keys *(default)*.
- Command line: `uv run python derivation/run.py` runs the full grid d ∈ {2,3,4} × n ∈ {2,3} and prints one ledger at the end; `--d D --n N` runs one combination *(default)*. Per-combination output lines follow hc-marimo: `[L3] PASS  TITLE / STATEMENT / axioms: ...`, preceded by a header `d=<d>, n=<n>` *(default)*.
- Ledger format: the same four sections and HEADLINE as hc-marimo `print_audit`, listing axioms in sorted name order, the HEADLINE stating that the identities hold for the instantiated sizes, that generic-d statements are proved in prose and instantiated mechanically, and that validity of the frontier reading requires R1 *(default)* (R-8).
- Axiom statements: as in spec §6 wording; machine-checkable `relation=` supplied where SymPy can state it without eager evaluation (A1 positivity, A3 τ > 0, A6 κ > 0), otherwise `None` *(default)*. A6 carries both κ > 0 and "each term on the simplex".
- Axiom usage: the `AXIOMS_USED` lists in R-4 are the spec's minimum; additions are allowed when R-9 needs them and are noted in the lemma docstring. R1 is invoked by L3 (balanced KKT at an interior optimum), I1 and I2 are invoked by the numeric tests (R-10, R-11), I3 by L5 (support-function remark) and I4 by L10 (GP compatibility) *(default)* (R-4, R-9).
- Limits (L5, L10): computed with `sympy.limit` under explicit assumptions inside `derive`, recorded in ctx, and `verify` asserts the EQUALITY `limit − value == 0`; ordering assumption s_1 > s_2 (helper symbols) is used instead of `Max`; strict inequalities such as LSE − max > 0 are proved by exhibiting a manifestly positive expression (sum of positive exponentials), never via eager `Relational` evaluation *(default)*.
- L4: the nonnegativity is verified symbolically by rewriting Var_p as the double-sum of squares form and checking the two forms are equal, then checking the double-sum is a sum of manifestly nonnegative terms (p_i p_k ≥ 0 with p_i expressed as positive helper symbols summing to 1) *(default)*.
- L6 uses `sympy.stats.Normal` and `E`; if SymPy cannot evaluate the expectation in closed form at a given size, the lemma uses the moment generating function of the Gaussian as an exact identity and records that choice in its docstring *(default)*.
- L8 uses the standard Helmert (ILR) basis for 1^⊥ built by a function in `symbols.py` (row k: (1,…,1, −k, 0,…)/√(k(k+1))); the ALR alternative is not verified *(default)*.
- L9 treats the pull-back as log m_j = α_j log(a_j + s_j) + b_j with α_j ≠ 0 (A4), and checks the closed form of V (including that negative α_j mark cost attributes) *(default)*.
- L10 uses K = 2 as the instance (Φ_2) with simplex-normalized term exponents θ_1, θ_2 and offsets β_1, β_2 *(default)*.
- I1 test: `scipy.optimize.linprog` primal and dual on `numpy.random.default_rng(0)` data with N = 8 designs and each d ∈ {2,3,4}; tolerance `abs <= 1e-7` *(default)* (R-10). I2 test: `default_rng(1)` data, replicate each row r = 3 times, compare J_τ at three random simplex points and at the minimizer from `scipy.optimize.minimize` (SLSQP), tolerance `1e-9` on J_τ, `1e-6` on w* *(default)* (R-11). The test helpers use numpy/scipy only; the package under `src/` is not imported.
- Test names: `test_full_chain_runs` (parametrized over d, n), `test_each_lemma_verifies`, `test_no_phantom_axioms`, `test_inherited_axioms_are_cited`, `test_load_bearing_symbol_assumptions_are_declared`, `test_every_used_axiom_resolves_and_all_tags_valid`, `test_every_axiom_is_used`, `test_lp_duality_numeric`, `test_replication_invariance`; additional per-result tests (e.g. reduction matches the canonical formula) as hc-marimo has *(default)*.
- How limits and other non-obvious modelling choices are recorded: in the lemma docstring under "What this proves / What this does NOT prove" and in the `STATEMENT` constant *(default)*.
- Runtime target: full six-run grid in under about 2 minutes on a laptop; if a lemma is slower at d = 4, n = 3, it may use `simplify` on a smaller equivalent form but must still run at that size *(default)*.
- Ruff applies to `derivation/` with the repository's existing configuration (line length 100); long mathematical docstrings stay within it *(default)*.
- Commit granularity: one commit per lemma or per small group, then `run.py`/tests, then the Status table and decisions file; commit messages prefixed "WP1: " *(default)*.
- Review report file `work-packages/WP1-review.md` and decisions file `work-packages/WP1-decisions.md` follow the WP0 format *(default)*.

## Open decisions (for the supervisor)

None at problem level: spec §6 and the confirmed breakdown answer them. The Agent's defaults list above is the one item for the supervisor to approve or change at the scope gate.
