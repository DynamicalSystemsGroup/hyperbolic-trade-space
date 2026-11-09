# WP13 — Scope of work: Response to the external review

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` at acceptance |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP13-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP13-decisions.md`, after `work-packages/WP13-review.md` |

## Purpose

A third-party reviewer recommended acceptance with minor revisions (`work-packages/external-review-2026-11.md`,
verbatim, with the paper map). The supervisor took every item through the decision loop on
2026-11-08; nothing was declined, and one standing position was adopted for all of them (his
words, in the review file): formal statements made exact in the derivations and the ledger; one
record of the map-territory gaps with their bridging assumptions, what cannot be proved, the
sensitivity evidence and the interpretive consequence; the words for the mathematics settled once
in the register; the policy stated once in the prose ("all models are wrong some are useful,
useful to a specific purpose in a specific situation and we're focused on improving trade
studies"). This package makes those changes to the research materials (derivations, code, docs)
and writes the response to the reviewer. The paper (WP10) then draws on them.

## Goals

- G1. The multi-facet solver's guarantees are stated at three levels and certified in code
  (E-1, accepted in full): descent; numerical stationarity with a per-facet first-order gap and a
  termination record with explicit tolerances; conditional local optimality under a positive
  assignment margin, as four statements with their hypotheses in the ledger.
- G2. The single-term theory is stated exactly where the review found it loose: the full simplex
  KKT conditions in L3 and the method page (E-2); L6 as a population identity with the assumptions
  any finite-sample or consistency statement needs, and no consistency claim (E-6); existence,
  uniqueness and stability separated, with tolerances and a sensitivity diagnostic (E-5).
- G3. One abstraction-gaps ledger records every map-territory gap the review and WP9 surfaced,
  each with its formal object, implementation, bridging assumption, what cannot be proved, the
  sensitivity evidence, and the interpretive consequence; the prose states the policy once and
  points to it (E-3, E-5, E-6, E-7, E-10's Q1 to Q4, WP9's gaps).
- G4. The implementation conventions the review named are declared or aligned (E-7): the
  degenerate-input shortcut kept as a declared convention with a warning; zero-metric scoring
  aligned with the formal limit; the sliver claim moved to "observed".
- G5. The register (`docs/superpowers/notes/notation.md`) settles the words for the mathematics
  (E-3's three objects, "energy differential" for $\log V$, facet, term, reach, share) and is
  published as the paper's supporting table.
- G6. A response letter answers every item, accepted or changed, citing commits, lemmas and
  evidence, in the conventions of a response to reviewers.

## Non-goals

- No global convergence result and no global identifiability claim (the reviewer does not ask for
  them; Q1 is marked not pursued).
- No change to the K = 1 fitted results, the datasets, the WP7 baseline numbers or the cubesat
  K = 1 record; the K > 1 record changes only where the Newton polish or the guard tolerance moves a
  number, and every such change is listed.
- No paper writing (WP10), no site (WP8a), no search (WP12), no release.
- No new caveats in the prose beyond the single policy statement and the register's definitions.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `src/hyperbolic_trade_space/solvers.py`: `simplex_gap`, `facet_gap`, `assignment_margin`, a finite-$\tau$ reduced-Newton polish at the end of each facet refit, per-facet dual or softmax weights kept, the monotone guard with a tolerance, a `Termination` record (status: certified / stationary without margin / guard stop / iteration cap / not applicable; iterations; feasibility and offset residuals; max gap; Corollary bound; objective change; assignment changes; empty facets; margin and radius; tolerances) on `TermsResult`; the $\tau=\infty$ gap as the LP duality gap | G1 |
| D-2 | `src/hyperbolic_trade_space/estimator.py`: `termination_` attribute; module constants for the tolerances; a `ConvergenceWarning` keyed to the status; `conditioning_` (the smallest eigenvalue of the restricted Hessian at the fit, or an equivalent) for E-5; the degenerate-input convention declared in the docstring with a warning at fit; zero-metric scoring aligned with the formal limit (a zero metric with a numerically zero exponent contributes nothing; rows with a zero metric on a participating exponent keep $V=0$; masking in the fit unchanged) | G1, G2, G4 |
| D-3 | `derivation/`: `lemma_03_gradient_kkt.py` extended with the boundary KKT statement (E-2); `lemma_06_gaussian_cumulant.py` statement restricted to the population identity with the assumptions named (E-6); `lemma_12_facet_gap.py`, `lemma_13_margin.py`, `lemma_14_assignment_stable.py` (E-1: Lemma 1, Lemma 2 with the explicit radius, Proposition 3 and Corollary 4) in the lemma-script pattern with symbolic $d$, $n_k$, $K$; `axioms.py` gains I8 (first-order convexity inequality), I9 (Cauchy–Schwarz), F12 (min representation, as F5/F10) and a positive-margin regularity condition, each with role and failure mode; `run.py` and the audit follow | G1, G2 |
| D-4 | `docs/superpowers/notes/abstraction-gaps.md` (the gaps ledger) with the columns above, populated from the review (E-3 three objects, E-5 stability and identifiability, E-6 finite sample, E-7 conventions, E-10 Q2 to Q4; Q1 not pursued) and from WP9 (thin facets, the tangent step and the penalty outside Proposition 3, $\tau$ re-selected per K, ties on ridge rows, platform ties); each entry's sensitivity evidence cites the spikes, the planted tests or the cubesat seeds; generated into the docsite by WP8a | G3 |
| D-5 | `docs/method.md`: the algorithm section restructured to the three levels with the stopping declaration (E-8's order: Lemma 1, Lemma 2, Proposition 3, Corollary 4, declaration); the full simplex KKT and the finite-temperature lesson; existence / uniqueness / stability with the restricted Hessian; L6's scope; the sliver statement moved to "observed"; the three objects defined once; one "Map and territory" paragraph stating the policy and pointing to the gaps ledger; `docs/api.md`, `docs/limitations.md`, `docs/why-and-how.md` and `docs/superpowers/notes/proof-conventions.md` follow | G1 to G5 |
| D-6 | `docs/superpowers/notes/notation.md` (the register) completed: the three objects, "energy differential", facet/term/reach/share, each with the formal object, the one phrase, what it is not, where defined; cross-checked against the derivation statements | G5 |
| D-7 | Tests: gap zero at interior, boundary and floored optima; $0\le f-f^*\le G$ on random simplex points; LP gap equals the duality gap; margin lemma numerically (perturbations within the radius keep the labels); Corollary identity; statuses; duplicate-facet detection; the zero-metric limit; the degenerate-input warning; `conditioning_`; the derivation tests for L3, L6, L12 to L14 and the ledger; `parametrize_with_checks` unchanged; the register's phrases present in the docs | G1 to G5 |
| D-8 | `docs/superpowers/notes/k3-cubesat.md` and `examples/adcs/k_terms.py`: certificate, margin and radius columns; re-run after the polish and the guard tolerance with every changed number listed | G1 |
| D-9 | `work-packages/external-review-2026-11.md`, "Response letter": one reply per item, the reviewer's point restated, what changed and where (commit, file, lemma), or why not, with evidence | G6 |
| D-10 | `work-packages/WP13-decisions.md` | — |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | On the planted data (20 seeds, $\tau\in\{\infty,50\}$) the default solver's returned fits have max facet gap below $10^{-8}$ after the polish, and `termination_.status` is "certified" wherever the margin is positive; where the margin is zero the status says so | `tests/test_solvers.py`, `tests/test_estimator.py`; the spike's numbers reproduced |
| R-2 | The LP gap at $\tau=\infty$ equals the LP duality gap to $10^{-12}$; the uniform-ties gap is reported as a valid bound only | tests |
| R-3 | Within the computed radius, random parameter perturbations leave the assignment unchanged (100 draws per fit on the planted data) | tests |
| R-4 | $F(W)-F^*_{\text{fixed}}\le\sum_k\frac{\lvert C_k\rvert}{N}G_k$ holds on every planted fit, with $F^*_{\text{fixed}}$ from independent per-facet solves | tests |
| R-5 | L3 states and verifies the boundary KKT; L12 to L14 derive at symbolic $d$, $n_k$, $K$ with their fallbacks recorded; the ledger lists I8, I9, F12 and the margin condition with role and failure mode; `derivation/run.py` ends in ALL LEMMAS PASS | `uv run python derivation/run.py`; `tests/test_derivation.py` |
| R-6 | The K = 1 path is byte-identical (the polish and the guard act on K > 1 only); the WP7 notebook and its tests untouched; `tests/test_notebook.py` passes | suite; `git diff` |
| R-7 | The gaps ledger has every entry named in D-4 with all six columns filled, and the method page points to it from exactly one policy paragraph; no new caveat sentences elsewhere (a reviewer's count of hedging phrases added in the diff) | inspection; a grep of the diff for "caveat", "note that", "however" additions |
| R-8 | The register defines the three objects and "energy differential"; the docs and the paper notes use the register's phrases ("distance" only as the register allows) | `tests/test_docs.py` extension: the register's phrases present, forbidden phrases absent |
| R-9 | Zero-metric scoring equals the formal limit on a planted case with a planted-zero exponent; the degenerate-input shortcut warns and its docstring says it is a convention | tests |
| R-10 | The response letter answers E-1 to E-10, each with its disposition class and evidence | inspection against the review |
| R-11 | Suite, lint, format, lock and the attribution grep pass on every commit; a manual Tests run on `dev` is green before the acceptance merge | commands; `gh run list` |

## Definition of good

- A reader of the method page sees three levels of guarantee for the multi-facet fit, each
  stated with its hypotheses, and can read the certificate a fit prints; a reader of the gaps
  ledger sees in one table where the map and the territory part and what evidence says about it;
  a reader of the prose meets the policy once and the register's words throughout.
- The response letter lets the reviewer verify every change by commit and lemma.

## Definition of good enough

- D-1 to D-10 exist; R-1 to R-11 pass as checked, with evidence in the review.
- Every item E-1 to E-10 has a response entry; nothing in the K = 1 results moved.
- Non-goals untouched.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- Tolerances *(default)*: `EPS_KKT = 1e-8`, `EPS_FEAS = 1e-9`, guard tolerance `1e-12`, polish: five
  reduced-Newton steps on the active set at finite $\tau$ only; module constants, not parameters.
- Gaps ledger *(default)*: a Markdown table in `docs/superpowers/notes/abstraction-gaps.md`, one row
  per gap, ids G-1, G-2, …; the method page's policy paragraph and the paper's discussion cite it;
  WP8a renders it as a docsite page.
- Register *(default)*: `notation.md` keeps its table and gains the columns "what it is not" and
  "where defined"; published as Appendix A by WP10.
- Zero-metric scoring *(default)*: $\log V=\sum_{j:w_j>10^{-12}} w_j\log m_j-\beta$ with
  $0\cdot\log 0:=0$; a row with a zero metric on a participating exponent keeps $V=0$; the fit's
  masking is unchanged.
- Degenerate input *(default)*: unchanged behaviour (uniform exponents), a `UserWarning` naming the
  convention, docstring says the fitted object does not exist for the input.
- The letter *(default)*: addressed to "the reviewer", one numbered reply per item in the review's
  order, each with disposition class, change and evidence; kept in the review file.
- Execution *(default)*: PM/implementer pattern; TDD; commits "WP13: " on `dev`; a fresh reviewer;
  the acceptance merge to `main` by the driver.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: the review's items in
`work-packages/external-review-2026-11.md` (decided there, nothing declined) and the Agent's defaults
approved as one item (`WP13-decisions.md`, 2026-11-08: "Approve the defaults as listed"). Decided 0
here, deferred 0, raised 0.
