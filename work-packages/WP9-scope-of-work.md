# WP9 — Scope of work: Posynomial solver for K > 1

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP9-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP9-decisions.md`, after `work-packages/WP9-review.md` |

## Purpose

The paper (WP10) tells the story that a trade space is a manifold: objectives aligned in one
region and opposed in another, fitted by posynomials to a coordinate system. The built method is
the one-term case, a single monomial, which finds one facet with constant exchange rates; the
K-term posynomial is documented as an extension and not built (`docs/method.md`, "The posynomial
and GGP extension"; `docs/limitations.md`). The supervisor's direction (2026-11-08, verbatim in
`WP10-decisions.md`): "i think it make be worth implementing a solver for K=3 and actually showing
what happens when we go from K=1 to K=3. most of that work is extensions to earlier work packages
but it starts with creating a second solver which we use when K>1. we only require it works in
practice for small K for now. we can look into scalability and performance in future work. [...]
remember we're thinking of this in terms of generalized geometric programs and its essentially a
kernel method where the kernel functions we're fitting are these trade-offs. [...] you should
write as little code as possible. the key is that we can use mathematical insights and exiting
optimization and ML tools". This package is that second solver and the extensions around it, so
that the paper can show the cubesat case at K = 1 and K = 3.

## Goals

- G1. A second solver, used when `n_terms` > 1, fits the K-term form $\Phi_K$ of L10 to the
  log-metrics with as little new code as possible, built on the existing K = 1 solver
  (`solve_lp`, `solve_slsqp`) and SciPy, and works in practice for small K (K = 2, 3); each term's exponents can be kept sparse by a regularization option, as an alternative to the existing support-and-threshold rule.
- G2. The estimator, chart, tension report and plots work facet by facet at K > 1 without an
  interface change: `HyperbolicTradeSpace(n_terms=K)` fits; `transform`, `inverse_transform` and
  `score_samples` use $\Phi_K$; the tension report gives one n-lemma per facet.
- G3. The method is shown going from K = 1 to K = 3: on a planted multi-facet frontier that K = 1
  under-scores and K = 3 recovers, and on the cubesat case, with the outputs recorded for the paper.
- G4. The K = 1 path is unchanged: the WP7 baseline numbers and every existing test hold.
- G5. The derivation chain gains L11 (a V-maximizer is Pareto-efficient, the intuition the method started from), and the documentation moves the extension from "documented, not built" to built for small K,
  states the algorithm and what it inherits, and names scalability and performance as future work.

## Non-goals

- No scalability or performance work (large K, large N, timing); named as future work in the docs.
- No kernel methods beyond what the K-term form already is; the kernel research direction stays
  documented, not built.
- No change to the K = 1 solver's results, the datasets, the WP7 notebook or its numbers.
- No paper writing (WP10) and no site work (WP8).
- No push to `origin/main` until the supervisor lifts the hold.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `src/hyperbolic_trade_space/solvers.py`: `solve_slsqp` gains the optional sparsity penalty (see defaults); `solve_terms(U, n_terms, tau, ...)` returning per-facet `(w_k, beta_k)`, the facet assignment and the objective, implemented as alternating partition and K = 1 refit (see defaults); `SolveResult` extended or a `TermsResult` dataclass | G1 |
| D-2 | `src/hyperbolic_trade_space/estimator.py`: `n_terms > 1` accepted; a regularization-based sparsity option for the exponents of every term as keyword arguments (`penalty`, `alpha`; see defaults), the alternative to the existing rule (τ = ∞ LP support and the working-temperature threshold); attributes `exponents_` of shape `(K, d)`, `log_offset_` of shape `(K,)`, `facet_` labels of the training rows, `term_temperature` used in $\Phi_K$; `transform`, `inverse_transform`, `score_samples` facet-aware per L10 and L8 | G2 |
| D-3 | `src/hyperbolic_trade_space/tensions.py`: `tension_report` at K > 1 returns one `TensionReport` per facet (a list), each on that facet's near-frontier rows, with the facet's contending set and n-lemma | G2 |
| D-4 | `src/hyperbolic_trade_space/plotting.py`: existing plots take a facet colouring and draw the K-facet envelope where they draw the frontier; no new figure types unless one call cannot show the envelope | G2, G3 |
| D-5 | `src/hyperbolic_trade_space/datasets.py`: `make_frontier_data` (or a sibling) plants a K-facet frontier (a max of K monomials in log space) with the facet labels returned | G3 |
| D-6 | `examples/adcs/k_terms.py` (or a cell block in a scratch notebook that writes files): the cubesat primary (aggressive-gains) and stock-gains datasets each fitted at K = 1, 2 and 3 with the per-facet reports and figures saved under `examples/adcs/figures/k3_*.png` (suffixed by regime) and a Markdown record `docs/superpowers/notes/k3-cubesat.md` of what was found in each regime, numbers included; which regime the paper uses is WP10's decision (OD3) | G3 |
| D-7 | Tests: `tests/test_solvers.py`, `tests/test_estimator.py`, `tests/test_tensions.py`, `tests/test_datasets.py`, `tests/test_plotting.py`, `tests/test_sklearn_compat.py` extended for `n_terms` in {2, 3}; `tests/test_matches_derivation.py` extended with the L10 identity at a numeric instance; the K = 1 regression tests untouched | G1, G2, G4 |
| D-8a | `derivation/lemma_11_pareto.py` (L11, the hc-marimo lemma pattern: `TITLE`, `STATEMENT`, `AXIOMS_USED`, `derive`, `verify`): a V-maximizer is Pareto-efficient. Statement: for $w\in\Delta$ and $u'\ge u$ componentwise, $w\cdot u'-w\cdot u=\sum_j w_j(u'_j-u_j)\ge 0$, with strict inequality whenever some $j$ has $w_j>0$ and $u'_j>u_j$; hence a design that maximizes $V$ over a set is not dominated in the contending metrics by any member of the set (weakly efficient in all $d$ metrics; efficient when every exponent is positive); at $K>1$ the same holds for $\Phi_K$ at $\kappa=\infty$ through the active facet. The converse is not claimed (only the log-convex part of a front is reached by some $w$; cite the weighted-sum scalarization results of Miettinen and Ehrgott). Added to `derivation/run.py`'s chain, `tests/test_derivation.py`, the ledger audit and the generated ledger | G5 |
| D-8 | Docs: `docs/method.md` (a "Simplifying assumptions" passage for the K > 1 fit that names each assumption, defends it and says how to go beyond it: hard assignment at $\kappa=\infty$ with smoothing on request, where the future-work note records that the search likely tolerates the kinks because the max of smooth functions has a tangent cone at a ridge and a generalized gradient equal to the convex hull of the active normals; the partition-and-refit local optimum with restarts; the analyst's choice of K; small K only; L11 stated in "Tensions, not variance" or "Interpretation" with its one-line proof idea and the non-converse; (the extension section rewritten as built: the algorithm in Boyd & Vandenberghe's "given / repeat / until" style, what is inherited and from whom, the limit of what is proved), `docs/api.md` (K > 1 section as built), `docs/limitations.md` (small-K statement, future work: scalability, selection of K, kernels), `derivation/axioms.py` ledger entry for the inherited partition-and-refit result; `docs/references.bib` unchanged unless a new source is needed (then under the WP5 rule) | G5 |
| D-9 | `work-packages/WP9-decisions.md` (approval, decisions, acceptance) | — |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | On a planted frontier with K = 3 facets in d = 4 (seeded), `HyperbolicTradeSpace(n_terms=3)` recovers the planted exponents of each facet within 0.05 (after matching facets) and assigns at least 90 % of frontier rows to the right facet; the same data at `n_terms=1` leaves a region under-scored (its `frac_above_` or residual on one facet's rows exceeds the K = 3 fit's by a factor the test states) | `tests/test_estimator.py::test_k_terms_recovers_planted_facets` (seeded) |
| R-2 | The alternating solver does not increase its objective between iterations and stops at a fixed assignment or `max_iter`; with `n_terms=1` it returns exactly the K = 1 solver's result | `tests/test_solvers.py` (monotone objective; `n_terms=1` equality) |
| R-3 | At `n_terms=K`, `transform` returns `(Z, log V)` with `log V = Φ_K(u)` and `inverse_transform(transform(X))` reproduces `X` within 1e-8 on the facet each row is assigned to; `score_samples` equals `log V` | `tests/test_estimator.py` round trip at K = 2, 3 |
| R-4 | `tension_report` at `n_terms=K` returns K reports, each with `n_near_frontier >= min_near_frontier` on the planted data, and the facet contending sets differ where the planted facets differ | `tests/test_tensions.py` |
| R-5 | scikit-learn conformance holds at `n_terms=3` as it does at 1: `parametrize_with_checks` on `HyperbolicTradeSpace(n_terms=3)` with the same expected-failures dict | `tests/test_sklearn_compat.py` |
| R-6 | The K = 1 path is byte-for-byte the same: the WP7 notebook's committed report outputs and `tests/test_notebook.py` pass unchanged; every pre-existing assertion about K = 1 behaviour is intact; a pre-existing test changes only where an approved deliverable makes its assertion false (a feature that now exists, a lemma that now exists), and every such change is listed in the review with its reason (amended, see Amendment 2) | `uv run pytest`; `git diff` of `tests/` against the pre-package commit, each removed or edited line listed and justified in the review |
| R-7 | Both cubesat datasets (primary and stock gains) at K = 3 fit, and the record (D-6) states per regime and per facet: size, contending set, n-lemma, the largest exponents, the near-frontier count, and how the K = 1 contending set relates to the three; figures exist and are legible | run D-6; inspect the record and figures |
| R-8 | New code is small: net added lines in `src/hyperbolic_trade_space/` (excluding docstrings, blank lines and tests) within the budget in the defaults; no new dependency | `git diff --stat`; a line count the reviewer runs; `uv lock --check` |
| R-9 | Docs: the method page states the algorithm, cites L10 for the identities it uses and the ledger entry for what is inherited, and claims nothing about global optimality; "documented, not built" no longer appears for K > 1; `tests/test_docs.py` and `tests/test_narrative.py` pass | read the pages; run the tests |
| R-11 | With `penalty="reweighted_l1"` and a stated `alpha`, the fitted exponents of a planted sparse facet (two of four metrics) have exact zeros on the planted-zero metrics while the unpenalized fit at the same finite τ leaves them small but positive; `alpha=0` reproduces the unpenalized fit exactly | `tests/test_solvers.py`, `tests/test_estimator.py` |
| R-12 | L11 derives and verifies for symbolic $d$ (nonnegativity of the sum; strictness under the stated condition), is listed by `derivation/run.py` with its axioms (A1, A2), and the method page states it and cites it by tag; `tests/test_narrative.py`'s tag check passes | `uv run python derivation/run.py`; `tests/test_derivation.py`; `tests/test_narrative.py` |
| R-10 | Suite, lint, format, lock and no-attribution checks pass on every local commit | `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, `git log` grep |

## Definition of good

- An analyst sets `n_terms=3` on the cubesat table and reads three facets, each with its own
  contending set and exchange rates, and sees in the figures where the facets meet: the manifold
  of the paper's story, made visible with the tools already in the package.
- The code reads as a small loop around what exists; a reader of `solvers.py` sees the K = 1
  problem reused, not a new optimizer.
- The docs say exactly what is proved (L10's identities), what is inherited (the partition-and-refit
  scheme and its local-optimum character), and what is only observed (recovery on the planted data
  and the cubesat).

## Definition of good enough

- D-1 to D-9 exist at the stated paths; R-1 to R-12 pass as checked, with evidence in the review.
- The planted K = 3 frontier is recovered and the cubesat K = 3 record exists with figures.
- Non-goals untouched: no performance work, no kernels, no change to K = 1 results, no paper, no
  push.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- Algorithm *(default)*: partition-and-refit in log space. Given `U`, `K`, `tau`: initialize the
  facets by K-means on the near-frontier rows of the K = 1 fit (or by the K = 1 fit plus K − 1
  random restarts, whichever the implementer finds recovers the planted frontier more reliably,
  recorded); repeat: assign each row to the facet with the largest `w_k . u − beta_k`; refit each
  facet by `solve_slsqp` on its rows at `tau`; until the assignment is unchanged or `max_iter`.
  This is the max-affine fitting scheme of Magnani and Boyd (`magnani2009convex`, already in the
  bibliography) applied with the entropic K = 1 fit per facet; its objective is the hard-max
  envelope's log-mean-exp and it converges to a local optimum, which the docs state. Random restarts
  seeded by `random_state` (a new estimator parameter, scikit-learn style), best objective kept.
- Fit temperature of the facets *(default)*: `tau` for every facet; the facet assignment is hard
  (the $\kappa \to \infty$ limit of L10); `term_temperature` ($\kappa$) is used only in evaluating
  $\Phi_K$ for `transform` and `score_samples`, default `np.inf` (max of the facets), so the fitted
  frontier is the max of K monomials and a finite $\kappa$ smooths it on request (OD2, decided).
  Under smoothing the hard $\beta_k$ are kept and the gap $\Phi_K - \max_k x_k \le \log K/\kappa$ is
  disclosed rather than renormalized away *(default)*.
- Chart at K > 1 *(default)*: `log V = Φ_K(u)`; `Z` is the L8 chart of the facet the row is assigned
  to; `basis_` becomes shape `(K, d−1, d)`; `facet_` labels are an attribute after `fit` and a
  `predict_facet(X)`-style helper gives them for new rows (name chosen to avoid `predict` on a
  transformer: `assign_facets(X)`).
- Tension report *(default)*: `tension_report` returns a list of K `TensionReport`s at K > 1 and a
  single report at K = 1 (unchanged); each facet's contending set is the LP support on that
  facet's rows; the closure note is per facet.
- Planted data *(default)*: `make_frontier_data(..., n_terms=K)` plants K monomials with random
  simplex exponents at least 0.3 apart in L1 and a common offset, samples rows under the max
  envelope with a fraction on it, and returns facet labels; K = 1 reproduces the current function
  exactly.
- Selection of K *(default, see OD1)*: K is the analyst's parameter; the record for the cubesat
  reports the objective and `frac_above_` at K = 1, 2, 3 as a diagnostic table, with no automatic
  selection.
- Sparsity regularization *(default)*: keyword arguments on the estimator in scikit-learn's
  style, `penalty=None` (the existing rule) or `"reweighted_l1"`, and `alpha=0.0`. On the simplex
  the plain L1 norm is constant, so the penalty is the reweighted-L1 of Candès, Wakin and Boyd
  (2008, doi 10.1007/s00041-008-9045-x, to be entered under the WP5 rule): a few SLSQP solves of
  `J_tau(w) + alpha * sum_j w_j / (w_j^{prev} + eps)` from the LP warm start, which drives small
  exponents to exact zero while leaving the large ones; `eps` 1e-4 and three reweighting rounds.
  Exact zeros are safe: a zero exponent removes the metric from the product (m_j^0 = 1); the
  log/exp hazard is zero *metrics*, which the code already masks. The contending set reported at
  τ = ∞ is unchanged by the option; at the working temperature the participating set is the
  support of the penalized fit.
- Reporting the terms *(default)*: the estimator exposes, per term, its exponent vector
  (`exponents_[k]`, the component), its lead coefficient `c_k = exp(-kappa * beta_k)` as
  `coefficients_` (the scalar attached to the term, the analogue the supervisor named), and its
  share of near-frontier rows (`facet_share_`), which is the ranking statistic the docs use when
  they say which facets explain most of the frontier; at K = 1 the invariant form fixes c = 1.
- Code budget *(default)*: at most 300 net added lines (raised from 250 for the sparsity option) in `src/hyperbolic_trade_space/` as
  counted by R-8; if the implementer cannot meet it, the PM reports why before continuing.
- Cubesat record *(default)*: K = 1, 2, 3 on the primary dataset (`adcs_designs_cubesat_gains.csv`) and on the stock-gains dataset (`adcs_designs_cubesat.csv`),
  feasible rows, the same conditioning and `tau` as WP7's four-metric and ten-metric fits; figures
  `k3_log_planes.png`, `k3_frontier_coordinates.png`, `k3_tensions.png` via the plotting module;
  the record is a note, not a notebook, so WP10 writes the paper's cells from it.
- Derivation *(default)*: no new SymPy lemma; L10 is cited for the identities; `derivation/axioms.py`
  gains an INHERITED entry I5 (Magnani and Boyd 2009: alternating partition and least-squares fit
  converges to a local optimum of the max-affine problem; role: the solver's convergence; failure
  mode: a poor local optimum, mitigated by restarts) with its interpretive role and failure mode
  per the ledger convention; `tests/test_derivation.py` and the generated ledger follow.
- Execution *(default)*: the PM/implementer pattern of `PM-BRIEF.md`; TDD; commits prefixed
  "WP9: ", local only; acceptance review in a fresh context.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (`work-packages/WP9-decisions.md`,
2026-11-08): decided 4, deferred 0, raised 1. OD1 selection of K: "Analyst's parameter, diagnostic
table". OD2 what the solver fits: hard fit with finite-κ smoothing on request, documented as a
simplifying assumption (named, defended, with the nonsmooth search on the ridges' tangent cones as
future work). OD3 where K = 3 is demonstrated: "do experiments on both and we can decide what to
use after we see the results". OD4 regularization (raised by OD2): a regularization-based sparsity
option as keyword arguments, alongside the existing rule. The Agent's defaults were approved as one
item: "Approve the defaults as listed".

## Amendment 1 (2026-11-08, at the acceptance gate; supervisor's G-1 disposition)

What changed and why, per scope-of-work section 6. The approved default "refit each facet by
`solve_slsqp` on its rows" is ill-posed in principle (the support function of a sliver is
minimized at a simplex vertex; 0 of 60 planted facets recovered even from the true labels), as the
two research spikes measured (`docs/superpowers/notes/spike-facet-refit/`,
`docs/superpowers/notes/spike-objective/`). The supervisor's decision, verbatim in
`WP9-decisions.md`: "keep both B and D in the code base, and evidence base but paper should focus
on the mean slack approach because of the monotone guarantee". Items below replace or extend
their originals; everything not named is as approved.

- Algorithm default (replaces the "Algorithm" default): the per-facet step is **B**, the supporting
  hyperplane of all rows tightest on the facet's rows: $w_k=\arg\min_w\,[J_\tau(Uw)-\bar u_k\cdot w]$
  (`solve_slsqp` on $U$ centred at the facet mean), $\beta_k=J_\tau(Uw_k)$ over all rows; the
  alternation minimizes the mean slack $\frac1N\sum_i(\beta_{k(i)}-w_{k(i)}\cdot u_i)$, which does
  not increase under either half-step (R-2). Mean slack is the K > 1 analogue of the K = 1 reach: the
  one-sided volume between the cloud and the envelope.
- D-1 and D-2 gain a keyword `facet_step` with values `"support"` (B, default) and `"tangent"`
  (**D**: the facet's direction is the smallest-variance direction of its near-frontier rows,
  projected to the simplex, when the facet has at least $d+1$ such rows, and B otherwise;
  $\beta_k$ the support value over all rows; the objective is not monotone under D and the docs say
  so) *(default: name and values)*. Restart selection stays by mean slack *(default)*.
- D-5 and R-1: the planted generator at `n_terms=K` guarantees at least $d+1$ frontier rows per
  facet (identifiability: a facet with fewer frontier rows than dimensions is not determined by
  them; spike round 2, section 2), and R-1 states that condition; the recovery claim in the docs is
  the measured rate on 20 seeds under the generator's conditions, for both steps, with the cause of
  any failure *(default)*.
- D-7: `tests/test_estimator.py` and `tests/test_solvers.py` cover both steps on the planted data;
  `tests/test_k_terms_case.py` runs the cubesat record with the default step only *(default)*.
- D-8: the method page states the per-facet problem as B solves it, with the spikes' evidence
  (the ill-posedness of the own-rows refit, the oracle recovery, the identifiability limit, the
  monotonicity table), presents D as the evidence-driven alternative, and says that the paper
  presents the mean-slack approach because of the monotone guarantee; `docs/api.md` documents
  `facet_step`; the "Simplifying assumptions" passage gains this choice (named, defended, beyond:
  a non-monotone evidence step or a frontier-weighted objective, both measured and parked).
- R-9: "the method page states the algorithm" now means both steps, with B as the default and the
  reason.
- Non-goals unchanged; code budget unchanged (300 net lines; D is about 26 lines by the spike's
  count).

Re-approval: the supervisor's disposition above is the approval of this amendment (it was decided
at the gate in the decision loop); the delivery is re-reviewed in full by a fresh reviewer before
acceptance.

## Amendment 2 (2026-11-08, at the acceptance gate; supervisor's G2-3 direction)

What changed and why, per scope-of-work section 6. R-6 as approved said "every pre-existing test
passes without edits to its assertions" and "additions only", which contradicts the package's own
deliverables: a test asserting that `n_terms > 1` is not implemented must change when it is
implemented, and tests that hard-code the lemma count must change when L11 is added. The
supervisor, verbatim (`WP9-decisions.md`): "i think the lemma count is arbitrary and i don't want
you to mess up the logical structure or clarity to game a metric" and "start by relaxing
artificial constraints then tell me what gap remains and propose how to address remaining gaps".
R-6 is restated above to its intent: the K = 1 results and the notebook are unchanged, the
pre-existing K = 1 assertions are intact, and edits forced by approved deliverables are listed in
the review with their reasons. No test or ledger restructuring is done to satisfy a count.
Nothing else changes.

## Amendment 3 (2026-11-08, at the acceptance gate; supervisor's G2-7 disposition)

What changed and why, per scope-of-work section 6. The record (D-6) used the temperature selected
at K = 1 for the K = 2 and K = 3 fits, so the fraction of designs above the K-facet envelope rose
to about a third (reviewed as G-7 and G2-7); and two of three stock-regime log-plane panels showed
no envelope (G-6). The supervisor's disposition, verbatim in `WP9-decisions.md`: "Fix before
acceptance". Items below replace or extend their originals; everything not named is as approved.

- D-6 and the "Cubesat record" default: for each regime and each K in {1, 2, 3}, τ is selected by
  `select_temperature` with the same target (a tenth of designs above V = 1) applied to the
  K-term fit, so the band means the same thing at every K; the record reports the re-selected
  fits (τ, band, facets, contending sets, n-lemmas, reach, share, near-frontier counts) as the
  record, and keeps the fixed-τ table (τ from K = 1 reused at K = 2, 3) as the diagnostic that shows
  the effect of not re-selecting; `select_temperature` accepts the estimator parameters it needs
  for this (`n_terms`, `facet_step`, `n_restarts`, `random_state`) *(default)*. The K = 1 rows are
  unchanged.
- D-4 and R-7 (figures): a log-plane slice draws a facet's envelope only where that facet has
  weight on both plotted metrics (exponents above the report's participation threshold), and the
  record's slices are chosen so that every facet is visible in at least one panel; the caption of
  each figure names the facets it shows *(default)*. If a legible two-metric slice does not exist
  for a facet, the record says so and the coordinates and tension figures carry it.
- R-7: "both cubesat datasets at K = 3 fit" is checked at the re-selected τ; the fixed-τ diagnostic
  is present.
- `docs/superpowers/notes/k3-cubesat.md`, `docs/limitations.md` (the open question "a K-specific
  temperature" becomes "τ is re-selected at each K by the K = 1 criterion; whether the target
  fraction should differ by K is open") and `docs/method.md` follow.

Re-approval: the supervisor's disposition is the approval of this amendment; the delivery is
re-reviewed (fourth review, delta) before acceptance.
