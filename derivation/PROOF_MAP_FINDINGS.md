# Proof-map findings (WP10, D-12)

What the tagging of `lemma_01` to `lemma_14` found. Nothing here was relabelled to fit: a step that
is neither computed (a line of SymPy that carries it) nor by a declared axiom (a line applying an
imported ledger entry) has no tag and is listed in section 1 for the supervisor. Addresses are file
and tag; an untagged step is addressed by the tags it falls between.

Method note. Tags are numbered in the order the steps appear in the file. The checker
(`uv run python -m derivation.proofmap`) fails on an untagged `assert` in `verify`, so every
asserted claim is a step; the other steps are the lines that apply a ledger entry.

## 1. Steps that are neither computed nor by a declared axiom (reported, not tagged)

| Address | The step (as the script's own text states it) | Why it has no line |
|---|---|---|
| `lemma_14_assignment_stable.py`, between L14.5 and L14.6 | Docstring step 2 of Proposition 3: the regrouping `sum_i = sum_k sum_{i in C_k}` and `F(W) = sum_k share_k f_k(w_k)`, with `beta_k - w_k.ubar_k = f_k(w_k)` | The script says so itself ("stated, not derived"; no ledger entry). The definitional step `beta_k = J_tau(U w_k)` is also not coded |
| `lemma_12_facet_gap.py`, after L12.24 | Docstring step 5: `p` supported on the active rows gives `sum_i p_i s_i = M`, hence `g.w = f(w)` and `G = f(w) - min_j (U_c^T p)_j` | Only `sum_i p_i (M - s_i) = M - sum_i p_i s_i` is asserted (L12.24); the termwise zero `p_i (M - s_i) = 0` is a comment (`# termwise zero`), not a line |
| `lemma_05_lse_lme.py`, after L5.6 and L5.16 | "LSE - max > 0 for n >= 2" (strictness, in `STATEMENT`) | Only `LSE - max >= 0` is asserted (L5.16); strictness is a comment in `verify` |
| `lemma_11_pareto.py`, after L11.9 and L11.13 | The deductions "a maximizer of V over S is not dominated" (contrapositive of L11.7 and L11.8) and "weakly efficient in all d metrics", "efficient when every `w_j > 0`" | Inference steps argued in the docstring and `STATEMENT`; no line |
| `lemma_02_shift.py`, after L2.4 | "Hence beta shifts by c and `w*` is unchanged" (docstring) | A corollary argued in prose, not coded |
| `lemma_04_convexity.py`, after L4.12 | "convexity of a function is equivalent to nonnegativity of its second derivative along every line" | Standard calculus, cited in the docstring, not a ledger entry and not coded |
| `lemma_03_gradient_kkt.py`, before L3.8 | The first-order necessary condition for a smooth function with one linear equality constraint ("standard calculus, not re-proved here") | Not coded; L3.8 applies R1 (no active multiplier) to the stationarity condition the script takes as given |

## 2. Premises carried as SymPy symbol assumptions (steps computed, premise not in the ledger)

These steps are computed and tagged; the premise they rest on is encoded in a local symbol's
assumption, not declared in the ledger (the hygiene test polices only the shared namespace):

- `lemma_14` L14.7, L14.8, L14.10: `share` nonnegative (facets nonempty, `n_k >= 1`), `dfk` nonnegative
  (every `w_k` minimizes `f_k`), `slackG` nonnegative (from L12).
- `lemma_11` L11.5, L11.6, L11.11, L11.12: `dl` nonnegative (`u' = u + delta`, `delta >= 0`), `gam`, `rest`.
- `lemma_13` L13.5 to L13.9: `delta`, `rest`, `a1`, `a2` nonnegative and `c` positive (`2 delta < gamma`).
- `lemma_12` L12.20 to L12.22: `a_nn`, `b_nn`, `c_nn` nonnegative stand for the I8 slack, the minimum slack
  and `f(w) - f* >= 0`.

## 3. Entries in `AXIOMS_USED` that no step of the existing script depends on

Each is applied by a tagged line (`invoke`, or an `A2.rewrite` that is a no-op) so that imports,
applied entries and `AXIOMS_USED` are the same set; the line records the premise and nothing
downstream consumes it. `AXIOMS_USED` was not changed.

| Address | Entry | Note |
|---|---|---|
| L5.3, L5.4, L5.5 | I2, I1, I3 | The script records them as remarks ("recorded, not proved here"); no step uses them |
| L2.2 | A3 | The docstring says "A3 does not enter here"; applied as the positivity licence of the forced log |
| L3.1, L4.1, L5.1, L12.8 | A3 | `tau` is a positive symbol already; the line states the premise |
| L6.1 | A2 | L6 never uses the simplex constraint; the weights `w` are declared on the simplex |
| L7.2 | A2 | "via L1": the substitution happened in L1's `Vk`; the `rewrite` here is a no-op |
| L10.3 | A2 | K = 1 reduction; no simplex substitution happens |
| L4.2, L9.1, L11.1, L7.1 | A1 | Positivity of `m` stated as the premise of `u = log m` (L7.1: V > 0 for the power) |
| L13.2, L14.2 | R2 | L13.2 states `gamma > 0`; L14.2 substitutes `M_i = s_i,k(i)` (the consequence of a unique maximizer), a real use |
| L13.3 | I9 | **Added line.** The script cited Cauchy-Schwarz only in its docstring; L13.3 introduces its slack symbol and L13.10 asserts `delta - |Delta theta.u~| >= 0` with it. The chain L13.8 and L13.9 is unchanged |

## 4. Positivity used but not through the ledger

- `lemma_10` L10.4 raises `m_j^{kappa theta_kj}` to exp of a Sum with a forced log expansion that needs
  `m > 0` (A1), but A1 is not in L10's `AXIOMS_USED`; the call has no licence argument.
- Forced `expand_log(..., force=True)` calls whose positivity is argued in comments, not by an
  entry: L2 (`verify`, the `rhs`), L5 (`offset`, `lme_floor`), L6 (`factor`), L10 (`shifted_reduced`,
  `base`, `phi1`, the `verify` difference).

## 5. Shape of the work

- Ledger: 22 entries; 14 carry a SymPy form on the shared symbols (A1, A2, A3, A4, A5 with its noise
  variable, A6, A7, I6, I8, I9, R2, F5, F10, F12); 8 are named propositions (A0, I1, I2, I3, I4, I5,
  I7, R1). Each is an importable module-level name and has a stable fingerprint.
- `sumtools.product_to_exp_sum` takes an optional licence entry (L1 and L9 pass A1 and A4).
- Inter-lemma premises (L12.9, L14.3, L14.4) are computed assertions on the earlier lemma's result,
  not re-derivations.
