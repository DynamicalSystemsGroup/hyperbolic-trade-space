# Research spike 3 (2026-11-08): level of effort for E-1 (certificates, margin, conditional local optimality)

Throwaway. Nothing in the repository was changed. All code and outputs are in this folder
(`<folder>` = `work-packages/spikes/spike-certificates` once copied into the repository). Every
command runs from the repository root. (The subagent's harness refused to write this file; the
driver saved the report from the subagent's message verbatim.)

## Summary (for the supervisor's decision)

**Verdict: E-1 is feasible in full, one work package, 16–22 implementer hours, about 930–1220 net lines (code 200–260, tests 150–200, three lemma scripts plus ledger 350–450, docs 230–310).** Two findings from the prototype change the implementation beyond what the reviewer asked, and both are small.

1. **The mathematics matches the solver exactly.** Step B's refit is argmin of f_k(w) = J_τ(Uw) − ū_k·w on the simplex with β_k = J_τ(Uw_k) (independent restarts find nothing lower; residual 0.0), and the mean slack equals Σ_k (|C_k|/N) f_k(w_k) to 2e-16 in the code. G_k = Σ_j w_j(g_j − min g) is the scalar residual of E-2's full simplex KKT (g_j ≥ λ, w_j(g_j − λ) = 0, λ = wᵀg), with L3's equal components as the w > 0 case. At τ = ∞ the gap with the LP duals is the LP duality gap (1e-16 at HiGHS optima); with uniform-on-ties weights it is a valid but useless bound (0.02–0.3), so the implementation must keep the per-facet duals that `_refit` discards today.

2. **Planted data (20 seeds × τ ∈ {∞, 50}, the estimator's exact call): every chosen run stops on a fixed assignment**, no empty facets. τ = ∞: max G_k ≤ 1.4e-15, certified 20/20 at 1e-6 and 1e-8; but γ ≈ 1e-16 (an exact tie: a frontier row on two facet planes) on exactly the three recovery-failure seeds 1, 3, 16, so with γ > 0 required 17/20. τ = 50: γ > 0 always (2.5e-4 to 2.2e-3; radius ≈ 5e-5), but **max G_k is 3e-6 to 5e-5 at SLSQP's ftol = 1e-10: 0/20 certified at 1e-6 as built**, although the points are within 1e-12 to 3e-11 of the exact f_k* (the first-order bound is loose by six orders at SLSQP's stop). **Five reduced-Newton steps on the active set (25 lines, 1 ms per facet) bring all 60 facets to G_k ≈ 1e-15**; tightening ftol to 1e-16 gets only 48/60 under 1e-8. The polish is finite-τ only, so the literal-pinned τ = ∞ test is untouched.

3. **Cubesat K = 3 (primary τ 195.18, stock τ 162.78, five seeds, plus K = 1's τ and τ = ∞):** all stops on a fixed assignment, no empty facets, no exact ties at finite τ; max G_k 2e-5 to 3.5e-5 (same SLSQP issue), γ 2.2e-4 to 1.5e-3, radius 1.8e-5 to 1.2e-4, Corollary bound 1.2e-5 to 2.2e-5. At τ = ∞ the stock table's worse local optimum (0.1447, 3 of 5 seeds) has one tied row and γ = 9e-16; the better one (0.1224) has γ = 3e-4.

4. **A defect the certificate exposes:** the monotone guard fired in 9 of 100 τ = ∞ restarts on an "increase" of 1–3e-16 (round-off), returning labels that differ from the argmax by up to 92 rows; 8 of the 9 are two identical facets (‖w_k − w_l‖ ≤ 3e-16, ~200 tied rows). None was the chosen restart. Fix: guard with a tolerance (1e-12) and report `assignment_changes`, `n_empty` and γ = 0 as a degeneracy.

5. **Derivation pattern confirmed feasible** at symbolic d, n_k, K with plain SymPy: Lemma 1 derives with a min-representation fallback F12 (as F5/F10) plus inherited I8 (first-order convexity inequality, Boyd & Vandenberghe 3.1.3); Lemma 2's algebra derives, the explicit radius needs inherited I9 (Cauchy–Schwarz); Proposition 3's per-facet regrouping derives (Fubini swap), the K-cell regrouping is a one-line finite-sum statement (SymPy has no symbolic partitions), and local minimality and Corollary 4 are nonnegative sums (`is_nonnegative`, the L11 device). The hypotheses become ledger conditions with role and failure mode (positive margin: fails on ridge rows at τ = ∞).

**Deferrable without weakening the response:** the SymPy scripts for Lemma 2's radius and Proposition 3's regrouping (state with sketch and citations, verify numerically, lift later; saves 3–4 h); asserting the Corollary bound in tests (report it); the min_exponent > 0 gap formula (state, test at m = 0); an estimator tolerance parameter (constants suffice); a separate status for step D and the penalty. **Must not be deferred:** three-level language and the stopping declaration with explicit tolerances; G_k computed and reported (LP duality gap at τ = ∞, Newton polish at finite τ, else nothing certifies); γ and the radius; `termination_` distinguishing certified / stationary-without-margin / guard stop / iteration cap; the four statements with hypotheses as ledger entries; the guard tolerance. Docs must say level 3 is for step B, unpenalized, β_k = J_τ(Uw_k) only; under D, G_k is a diagnostic (hypothesis 3 fails by construction) and under the penalty it certifies nothing.

Risks: the polish moves finite-τ exponents by ~1e-6 (doctests round to 3 decimals, cubesat objectives agree to 6 digits: safe); the guard tolerance changes the message on 9 % of τ = ∞ restarts, so the recovery table in method.md should be re-run (22 s); the ledger gains I8, I9, F12 and a regularity entry that the every-axiom-used audit must list.

---

## FULL REPORT

| command | writes | time |
|---|---|---|
| `uv run python <folder>/check_identities.py` | stdout (section 1) | 5 s |
| `uv run python <folder>/run_planted.py` | `planted.txt`, `planted.csv`, `planted_restarts.csv` (tables 1, 2) | 22 s |
| `uv run python <folder>/run_cubesat.py` | `cubesat.txt`, `cubesat.csv` (table 3) | ~2 min |
| `uv run python <folder>/polish_and_ties.py` | `polish_and_ties.txt` (tables 4, 5) | 30 s |
| `uv run python <folder>/dup_facets.py` | stdout (table 5) | 10 s |
| `uv run python <folder>/sympy_feasibility.py` | `sympy_feasibility.txt` (section 4) | 5 s |

Prototype: `certificates.py` (`facet_gap`, `simplex_gap`, `assignment_margin`, `fixed_assignment_bound`, `termination_report`; 150 lines with docstrings); `polish_and_ties.py::newton_polish` (25 lines).

### 1. The mathematics against the solver as built (`check_identities.py`)

**Step B is exactly argmin f_k.** `_refit` calls `solve_slsqp(U - mean_k(U), tau)`; since J_τ((U − 1ū_kᵀ)w) = J_τ(Uw) − ū_k·w (Σw = 1), that is f_k(w) = J_τ(Uw) − ū_kᵀw on the simplex, and `beta_k = log_mean_exp(U @ w, tau)` is J_τ(Uw_k) (residual 0.0). Ten independent SLSQP restarts from Dirichlet starts found nothing lower than step B's value at τ = ∞ (difference 0) or τ = 50 (step B within 4e-12).

**The mean slack is the fixed-assignment expression.** (1/N)Σ_i(β_{k(i)} − w_{k(i)}·u_i) = Σ_k (|C_k|/N)(J_τ(Uw_k) − w_k·ū_k) = Σ_k (|C_k|/N) f_k(w_k), with ū_k the mean over the labels used in the refit; `_refit` computes `obj` on those labels, so the identity is exact in the code (max |F_fixed − objective| = 2e-16 over 40 fits). Hypothesis 4 of Proposition 3 is a consequence of hypothesis 1 for this objective: with β_k = J_τ(Uw_k) the full objective is (1/N)Σ_i min_k(β_k − w_k·u_i), and a positive margin keeps every row's argmin fixed on the neighbourhood.

**Mismatches found (none breaks the proposition; two need code or words).**
1. *Guard stop returns inconsistent labels.* On `"no further decrease"` the returned `labels` are the pre-step labels while the argmax under the returned (W, β) differs (up to 92 rows, table 5). In exact arithmetic the guard cannot fire (reassignment then convex refit is monotone); it fired 9 times in 100 restarts at τ = ∞, every time on an increase of 1–3e-16 (round-off), and 8 of the 9 are two identical facets (‖w_k − w_l‖_∞ ≤ 3e-16, about 200 rows tied), the 9th a genuine two-row tie. None was the chosen restart. γ = 0 exposes exactly this degeneracy, which the current message hides. Fix: guard with a tolerance (`obj2 > obj + 1e-12`) and report `assignment_changes` and γ.
2. *Restart selection and the Corollary.* `solve_terms` keeps the lowest-objective restart; the certificates are per returned run, so nothing changes, but the report should say the bound is for the fixed assignment of that run, not across restarts.
3. *Empty facets* (hypothesis 2): `_refit` skips a facet with no rows and keeps its stale (w_k, β_k). Zero empty facets occurred in 240 planted restarts and 60 cubesat fits, but the report must count them (`n_empty`): the Corollary weight is 0 and the facet is unconstrained.
4. *Step D, the penalty, `min_exponent`.* Under D, w_k is a TLS normal, not argmin f_k, so G_k > 0 is expected and hypothesis 3 fails by construction; the penalty changes the objective so G_k of the unpenalized f_k is a diagnostic, not a certificate (the reviewer's caveat). With a floor m > 0 the feasible set is {w ≥ m, 1ᵀw = 1} and the gap is G = gᵀw − m 1ᵀg − (1 − dm) min_j g_j (prototyped; check 5: 1.7e-7 at the floored optimum, same order as the m = 0 formula at the unfloored one).

**KKT consistency (L3, E-2).** G_k = gᵀw − min_j g_j = Σ_j w_j(g_j − min g) with λ = wᵀg; G_k = 0 iff g_j ≥ λ for all j and w_j(g_j − λ) = 0, which is E-2's full simplex KKT, and the interior case (w > 0) is L3's equal components. Check 3: at the SLSQP optimum g − λ = O(1e-7); 0 of 2000 random simplex points violate 0 ≤ f − f* ≤ G; a forced boundary optimum has g_j > λ at the inactive coordinate.

**τ = ∞.** f_k is piecewise linear; the subgradient is Uᵀp − ū_k for any p supported on the active rows, and G_k = f_k(w) − min_j(U_cᵀp)_j = primal minus dual objective (I1). With the LP duals p it is the LP duality gap (1e-16 at HiGHS optima, check 4); with `support_weights(·, inf)` (uniform on ties) it is a valid but useless bound (0.02–0.3 at the optimum). The estimator discards the duals (`_refit` keeps only `.w`); the implementation must keep `p` per facet or re-solve the LP in the report. The finite-τ formula does not carry over (the softmax is not the certifying subgradient); the duality gap is the right object.

### 2. Measurements

**Table 1. Planted data, `solve_terms(U, 3, tau, random_state=0)` (the estimator's call), seeds 0..19.**

| τ | termination (chosen run) | max_k G_k median / max | Cor. 4 bound median | γ min / median / max | radius median | γ ≤ 1e-6 | certified at ε_KKT = 1e-6 / 1e-8 | empty facets |
|---|---|---|---|---|---|---|---|---|
| ∞ | 20/20 assignment fixed | 3e-16 / 1.4e-15 | 2e-16 | 4e-17 / 6.7e-4 / 5.9e-3 | 2.7e-5 | 3 (seeds 1, 3, 16) | 20/20 / 20/20 (17/20 if γ > 0 required) | 0 |
| 50 | 20/20 assignment fixed | 1.2e-5 / 4.7e-5 | 7e-6 | 2.5e-4 / 1.1e-3 / 2.2e-3 | 4.6e-5 | 0 | 0/20 / 0/20 as built | 0 |

The three γ ≈ 1e-16 seeds at τ = ∞ are exactly the recovery failures (1, 3, 16): a frontier row lies on two facet planes at zero slack (the thin facet's LP plane passes through a row the big facet also touches; "rows touching two planes: 2" on each). Failing seeds with γ > 0 (3 and 8 at τ = 50, exponent error 0.11 and 0.22) are stationary local optima with positive margin, as the proposition allows. The objective change at the stop is not small (1e-4 to 0.25): the stopping rule is the fixed assignment, not the objective; the report must say so.

**Table 2. All 100 restarts per τ.**

| τ | assignment fixed | guard | max_iter (50) | γ ≤ 0 | max G 99th pct |
|---|---|---|---|---|---|
| ∞ | 89 | 9 (8 duplicate-facet, 1 two-row tie; increase ≤ 3e-16) | 2 | 8 | 1.4e-15 |
| 50 | 100 | 0 | 0 | 0 | 4.7e-5 |

**Table 3. Cubesat, K = 3, five seeds each (N = 706 primary, 780 stock; no duplicate rows; max_i ‖(u_i, −1)‖ = 6.1 / 6.3).**

| regime | τ | stops | objective range | max_k G_k | γ | radius | exact ties |
|---|---|---|---|---|---|---|---|
| primary | 195.18 (K = 3 selection) | 5/5 fixed, 7–21 it | 0.117333–0.117334 | 2.2e-5–2.7e-5 | 2.2e-4–1.0e-3 | 1.8e-5–8.2e-5 | 0 |
| primary | 38.10 (K = 1's τ) | 5/5 fixed | 0.052922–0.052923 | 1.1e-5–2.8e-5 | 5.8e-4–1.2e-3 | 4.8e-5–9.8e-5 | 0 |
| primary | ∞ | 5/5 fixed | 0.1401–0.1424 | 7e-16–3e-15 | 6.2e-5–7.9e-4 | 5e-6–6.4e-5 | 0 |
| stock | 162.78 | 5/5 fixed | 0.092872 (4 seeds), 0.114273 (1) | 2.9e-5–3.5e-5 | 8.7e-4–1.5e-3 | 7e-5–1.2e-4 | 0 |
| stock | 41.72 | 5/5 fixed | 0.032607 | 1.8e-6–3.0e-5 | 1.6e-4–6.4e-4 | 1.3e-5–5.1e-5 | 0 |
| stock | ∞ | 5/5 fixed | 0.1224 (2), 0.1447 (3) | 1e-15–2e-14 | 8.9e-16 (3 seeds), 3.1e-4 (2) | 7e-17, 2.5e-5 | 1 row on the 3 tied seeds |

**Table 4. Finite-τ certification: 60 facets of the chosen τ = 50 planted fits.**

| after | G_k median / max | ≤ 1e-6 | ≤ 1e-8 | ≤ 1e-10 | time (60 facets) |
|---|---|---|---|---|---|
| built SLSQP, ftol 1e-10 | 4.6e-6 / 4.7e-5 | 15 | 0 | 0 | — |
| SLSQP ftol 1e-14 | 2.1e-9 / 1.7e-7 | 60 | 33 | 13 | 0.06 s |
| SLSQP ftol 1e-16, 2000 it | 3.8e-10 / 5.8e-8 | 60 | 48 | 24 | 0.09 s |
| 5 reduced-Newton steps on the active set | 1.0e-15 / 3.6e-15 | 60 | 60 | 60 | 0.07 s |

The built points were within 1e-12 to 3e-11 of the exact f_k*: the fits are good, the first-order bound is loose by six orders at SLSQP's stop, and a Newton polish at the end of each refit (1 ms per facet) makes the certificate tight.

### 3. Implementation estimate

| where | what | lines |
|---|---|---|
| `solvers.py` | `simplex_gap`, `facet_gap`, `assignment_margin`, `_newton_polish` (finite τ only; LP path byte-identical so `test_default_facet_step_is_unchanged_literals` holds), keep each facet's `p` (softmax or LP duals) in `_refit`, guard tolerance, `Termination` dataclass (reason, n_iter, feasibility residuals, offset residual, max_gap, bound, objective_change, assignment_changes, n_empty, gamma, radius, status, tolerances) built in `_solve_terms_once`, `termination` field on `TermsResult`, docstrings with doctests | 170–220 |
| `estimator.py` | `termination_` attribute, module constants `EPS_KKT = 1e-8`, `EPS_FEAS = 1e-9` (no new `__init__` params needed), `ConvergenceWarning` keyed to the status, docstring | 30–40 |
| tests | gap 0 at optima (interior, boundary, floored); 0 ≤ f − f* ≤ G on random points; LP gap = duality gap; uniform-ties gap valid; margin lemma numeric (perturb within radius: labels unchanged); Corollary identity; statuses (fixed / cap via `max_iter=1` / guard); duplicate-facet detection; estimator attribute; `parametrize_with_checks` unchanged | 150–200 |
| `derivation/` | `lemma_12_facet_gap.py`, `lemma_13_margin.py`, `lemma_14_assignment_stable.py`; `axioms.py`: I8 (first-order convexity inequality, Boyd & Vandenberghe 3.1.3), I9 (Cauchy–Schwarz, Horn & Johnson), F12 (min representation, as F5/F10), R2 (positive margin; failure mode: ridge rows); `run.py` CHAIN; `test_derivation.py` per-lemma, fails-loudly, fallback-recorded | 350–450 |
| `docs/method.md` | algorithm box gains the stopping declaration; new subsection "Three levels: descent, numerical stationarity, conditional local optimality" with Lemma 1, Lemma 2, Proposition 3, Corollary 4 stated and sketched citing L12–L14; τ = ∞ gap as the LP duality gap; what D, the penalty and `min_exponent` do to each level; "What is proved…" updated; the measured certificates | 150–200 |
| `api.md`, `notation.md`, `limitations.md`, `k3-cubesat.md` (deleted; last version at 4409920), `examples/adcs/k_terms.py` | `termination_` fields; G_k, γ, radius, F*_fixed rows; limitation: γ = 0 at τ = ∞ on ridge rows; certificate column in the cubesat record | 80–110 |
| total | | 930–1220 net lines |

Hours: solver and estimator 4–5; tests 3–4; three lemma scripts and ledger 4–6; docs 4–5; case-study record and readability loop 1–2. **16–22 hours, one work package**, plus the supervisor's gates.

**Derivation plan** (`sympy_feasibility.py`, all checks pass at symbolic d, n_k, K):
- *Lemma 1 (L12).* Derive gᵀv − m = Σ_j v_j(g_j − m) ≥ 0 on the simplex, = 0 at e_{j0} (L3's KroneckerDelta device), under a min-representation fallback F12 (g_j ≥ m for all j, g_{j0} = m; SymPy has no symbolic-d min, the same reason as F5/F10); hence G = Σ_j w_j(g_j − m) ≥ 0 with G = 0 iff w_j(g_j − m) = 0 termwise (E-2's KKT; L3 when w > 0). Convexity is L4; f(v) ≥ f(w) + gᵀ(v − w) is inherited I8; the chain f(w) − f* ≤ gᵀ(w − v*) ≤ G is sign algebra.
- *Lemma 2 (L13).* Derive: after perturbing every score by at most δ the margin is ≥ γ − 2δ > 0 (L11-style positive-symbol algebra, verified). The explicit radius needs |Δθ_k·(u_i, −1)| ≤ ‖Δθ_k‖‖(u_i, −1)‖: inherited I9, then substitution. One confined numeric endpoint.
- *Proposition 3 and Corollary 4 (L14).* Derive the per-facet regrouping Σ_{i∈C_k}(β_k − w_k·u_i) = n_k(β_k − w_k·ū_k) at symbolic n_k (Fubini swap via L3's `sum_swap_equal`, verified); the regrouping of the N-sum over K cells has no symbolic-partition object in SymPy and is stated as a one-line finite-sum argument (not enumeration). Local minimality F(W') − F(W) = Σ_k (|C_k|/N)(f_k(w'_k) − f_k(w_k)) ≥ 0 and the Corollary Σ_k (|C_k|/N)(f_k − f_k*) ≤ Σ_k (|C_k|/N) G_k are nonnegative sums (`is_nonnegative`, L11 step 4). Hypotheses 1–3 are ledger conditions with role and failure mode.

**What the docs must say about step D and the penalty.** Level 1 (descent) holds for B only. Level 2 (stationarity) is reported for every step, but under D G_k measures the distance of the TLS normal from the support optimum (diagnostic) and under the penalty G_k is that of the unpenalized f_k (certifies nothing). Level 3 is for B, unpenalized, `facet_step="support"`, β_k = J_τ(Uw_k) only; `termination_.status` should read `"not_applicable"` for D and the penalty.

### 4. Risks and deferrable parts

**Risks.** (i) SLSQP's stop leaves G_k ~ 1e-5: without the Newton polish nothing at finite τ certifies at 1e-6; the polish moves exponents by ~1e-6 (doctests round to 3 decimals; cubesat objectives agree to 6 digits; the τ = ∞ literal test stays on the unpolished LP path). (ii) The LP case needs the duals kept per facet (re-solving the LP in the report is the fallback). (iii) Ties in γ at τ = ∞ are structural on ridge rows (3/20 planted chosen runs, 8/100 restarts, 3/5 stock cubesat seeds; never at finite τ on these data): hypothesis 1 fails and the docs present it as an interpretive condition. Duplicate facets are the extreme case and should be reported. (iv) The guard tolerance changes the message on 9 % of τ = ∞ restarts (not the chosen ones here); re-run the recovery table (22 s). (v) Ledger growth: I8, I9, F12, R2 must be listed for the every-axiom-used audit; the HEADLINE already reports fallbacks (F5, F10).

**Deferrable without weakening the response:** SymPy scripts for Lemma 2's radius and Proposition 3's regrouping (state with sketch and citations, verify numerically, lift later; 3–4 h); asserting the Corollary bound in tests (report it; assert only bound ≥ F − F*_fixed, which the prototype verifies); the min_exponent > 0 gap (state the formula, test m = 0); an estimator tolerance parameter; a separate status for D and the penalty.

**Must not be deferred:** three-level language and the stopping declaration with explicit tolerances in method.md and the algorithm box; G_k computed and reported (LP duality gap at τ = ∞, Newton polish at finite τ); γ and the radius; `termination_` distinguishing certified / stationary without margin / guard stop / iteration cap; the four statements with hypotheses as ledger entries; the guard tolerance.
