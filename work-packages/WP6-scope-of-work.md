# WP6 — Scope of work: Mathematics narrative

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP6-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP6-decisions.md`, after the review report `work-packages/WP6-review.md` |

## Purpose

The method's mathematics is machine-checked (WP1) and implemented (WP2). WP6 writes the discursive narrative that
explains it to a reader: what the model is, what the fit learns and why that is shape, the conditions under which the
interpretation holds and what is lost when they do not, how novelty, white space and prediction are read, where the
method sits in the literature (WP5), and how it extends. Per the supervisor's framing, the model finds the tensions that
define the trade-offs, as PCA finds variance components, and the narrative states that contrast precisely, with its
limits. WP6 also reconciles the spec's per-lemma axiom lists with the WP1 ledger so the written record agrees with the
code.

## Goals

- G1. `docs/method.md`: the mathematics, in the order of the pipeline (stage table, model, fit, what the stage learns, interpretation, novelty and white space, prediction from configuration, lineage, the GGP extension, the kernel research direction), each load-bearing claim tagged with the lemma that proves it.
- G2. The conditions of the theory (ledger entries R1, F5, F10, the conditioning assumption A4, and any other hypothesis the lemmas rest on) are stated with their interpretive role and failure mode, so the reader knows what each condition buys and what the interpretation loses without it.
- G3. The "tensions, not variance" contrast with PCA is stated as in the spec, with its limits.
- G4. A "why and how to use it" page for readers who want the idea and the workflow before the mathematics.
- G5. A limitations and extensions page.
- G6. The spec's per-lemma axiom lists (§6) agree with the WP1 ledger, checked by a test.

## Non-goals

- No change to code, `derivation/`, the bibliography (WP5) or tests of other packages; narrative claims that need a missing source are listed in the review as gaps, not patched with unverified references.
- No site configuration, MkDocs build or generated pages (WP8), no notebook (WP7), no API reference (`docs/api.md` is WP3).
- No new mathematics: every formula is one the spec §4 states, WP1 proves or the code implements; a spec formula found wrong is reported, not silently changed.
- No claim of priority or novelty for the method (WP5 marks these as the supervisor's).
- No description of tools by API name before they exist: the tension report and the other WP3 tools are described by concept and by "implemented in the analysis toolkit" until WP3 is accepted.
- No search for successive tensions by deflation: a research question, stated as such.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `docs/method.md` | G1, G2, G3 |
| D-2 | `docs/why-and-how.md` | G4 |
| D-3 | `docs/limitations.md` | G2, G3, G5 |
| D-4 | `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md`: §6 lemma and axiom lists reconciled with the ledger (only that part of the spec changes) | G6 |
| D-5 | `tests/test_narrative.py` | G1, G2, G6 |
| D-6 | `work-packages/WP6-decisions.md` (approval record) | G1–G6 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `docs/method.md` contains sections for: the pipeline stage table (spec §3), the model (V, invariant form), the fit (J_τ, gradient, convexity, temperature), what the stage learns and why it is shape (the eight statements of spec §4), interpretation (elasticities, improvement factors, projection, chart), novelty and white space, prediction from configuration, lineage, the posynomial/GGP extension, and the kernel research direction | inspect headings against spec §3 and §4 |
| R-2 | Every displayed formula in `method.md` carries a tag naming the lemma that proves it (`L1`–`L10`) or marks itself a definition; every lemma L1–L10 is cited at least once; every tag resolves to a lemma module in `derivation/` | `uv run pytest tests/test_narrative.py` |
| R-3 | Each formula in `method.md` agrees with the code: for every tagged formula there is a statement of where it is implemented (module and function) and the existing cross-check test (`tests/test_matches_derivation.py`) or lemma `verify` that ties the two; the reviewer spot-checks at least five formulas against `solvers.py`, `coordinates.py` and `estimator.py` | inspection by the reviewer against the code; `test_narrative.py` verifies that every referenced module and function exists |
| R-4 | A "Conditions of the theory" section lists exactly the ledger's REGULARITY entry (R1) and every fallback (F5, F10), plus the conditioning assumption A4, each with its interpretive role and its failure mode as recorded in `derivation/axioms.py`; the set of ids equals the ledger's set | `test_narrative.py` (id sets equal; role and failure-mode strings of the ledger appear verbatim or are quoted) |
| R-5 | Each load-bearing claim in `method.md` names the hypothesis it needs (A1–A7, I1–I6, R1, F5, F10) and, where it fails, says what the interpretation loses (a sentence per condition, not per claim); no claim is stated more strongly than the lemma proves (the lemma docstrings' "does not prove" sections are respected) | reviewer reads each lemma's docstring against the sentence citing it, for at least L3, L4, L5, L8 and L10 |
| R-6 | The PCA contrast is stated as in spec §2 ("Tensions, not variance"): PCA maximizes spread; the fit minimizes the soft maximum of w·u over the simplex, the smallest upper extent, the binding constraint among larger-is-better metrics; w is the tension and its ratios the exchange rates; metrics with w_j = 0 are free at the balanced point; along the frontier the spread of near-frontier designs in Z occurs only where metrics were traded, and its principal directions are the exercised trade-offs; metrics moving together there are aligned, not in tension | inspection against spec §2 |
| R-7 | The limits of the contrast are stated: K = 1 finds one tension; several regional tensions are the K > 1 extension; a deflation-style search for successive tensions is a research question and is not claimed; the HoroPCA/negative-curvature "hyperbolic PCA" is disambiguated | inspection |
| R-8 | `docs/why-and-how.md` explains the idea (tensions, the frontier as V = 1, the chart), the workflow in the pipeline stages, what a user needs to supply (conditioned metrics) and what they get back, in prose accessible without the mathematics, and points to the method, limitations and (by concept) the case pages | inspection |
| R-9 | `docs/limitations.md` lists the limits of the method, each with its reason: log-convexity only, one facet at K = 1, optimism off the balanced point, noise band and calibrated novelty, holes versus structural strata, novelty is not preference, dependence on conditioning, small-sample identifiability, and the extensions (K > 1, kernels) as documented-not-built | inspection against spec §4 caveats |
| R-10 | Every citation is `[@key]` with a key present in `docs/references.bib`; every prior-art statement uses only what `docs/literature.md` supports; priority and novelty claims are absent or marked as the supervisor's | `test_narrative.py` (keys resolve); inspection against `docs/literature.md` |
| R-11 | The spec's §6 axiom lists per lemma and the axiom set (A0–A7, I1–I6, R1, F5, F10) are reconciled with the ledger: for each lemma the listed axioms equal `AXIOMS_USED` in its module, and the axiom lists name every ledger id | `tests/test_narrative.py::test_spec_matches_ledger` parses spec §6 |
| R-12 | The narrative is consistent with the amended spec in other respects: β is the log-mean-exp (never the unnormalized log-sum-exp), the class and package names are `HyperbolicTradeSpace` and `hyperbolic_trade_space`, "posynomial invariant form" is the method's name | `grep` and inspection |
| R-13 | Suite, linters and lock pass; nothing outside scope changed: `git diff --stat` shows only `docs/method.md`, `docs/why-and-how.md`, `docs/limitations.md`, the spec §6 edit, `tests/test_narrative.py` and `work-packages/` | run the commands; inspect the diff |
| R-14 | No AI attribution lines; commits authored as Michael Zargham; CI green on every push | `git log` grep returns 0; `gh run list` |

## Definition of good

- A reader new to the method can follow from the idea to the mathematics to the limits without leaving the page, and sees for every result which conditions it rests on and what the interpretation loses when they fail.
- The tensions framing makes the method understandable by analogy with PCA while being exact about how it differs.
- The writing is discursive and humble: models are wrong and some are useful; the stated conditions are the method's limitations, carried honestly.
- Formulas, code and lemmas visibly agree; a reader can click from a formula to its lemma and to its implementation.

## Definition of good enough

- Deliverables D-1 to D-6 exist at the stated paths.
- R-1 to R-14 pass as checked, with evidence in the review report.
- Non-goals untouched (no code or bibliography changes, no site wiring).
- Every ledger condition is stated with role and failure mode (R-4), and the PCA contrast with its limits (R-6, R-7).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item.

- File names `docs/method.md`, `docs/why-and-how.md`, `docs/limitations.md` *(default)*; the site page titles are "Mathematics", "Why and how to use it" and "Extensions and limitations" (set in WP8) *(default)*.
- Formula tagging *(default)*: each display equation `$$ ... $$` is followed on the next line by a tag comment of the form `<!-- lemma: L5 -->` or `<!-- definition -->`, and the visible text names the lemma in a sentence ("by L5"); `test_narrative.py` parses the comments.
- Implementation pointers *(default)*: a short table at the end of each major section maps formula to module and function (for example `solvers.log_mean_exp`), and `test_narrative.py` checks the names import.
- Conditions section *(default)*: a table with columns id, statement, interpretive role, failure mode, built from `derivation/axioms.py` by quoting; the test checks the id set equals `{a.name for a in REGULARITY} ∪ {fallbacks}` plus A4 as the conditioning assumption.
- Citation style `[@key]` as in WP5 *(default)*; keys only from `docs/references.bib`; if a statement needs an unavailable source it is written without the claim and listed in the review as a gap *(default)*.
- Tool references *(default)*: the narrative refers to the WP2 estimator by its class name `HyperbolicTradeSpace` and methods; it refers to preconditioning, the tension report, gaps, prediction and plotting as "the analysis toolkit" with a note that its API is documented in `api.md`, and does not quote WP3 function signatures.
- Tone *(default)*: discursive prose, LaTeX for formulas, no emojis; "we" for the method's development, "the supervisor" is not named in the text; no claim of novelty or priority.
- Reconciliation of spec §6 *(default)*: the edit is limited to the axiom lists in the lemma paragraph and the axiom paragraph (adding A0, A7, I5, I6, F5, F10 and the fallbacks' tags, correcting lists to the ledger); `test_spec_matches_ledger` parses `L<n> ... [A.., ...]` brackets.
- Tests *(default)*: `test_narrative.py` runs offline, uses only the standard library, `re` and the project modules, and runs under the default `uv run pytest`.
- Commits prefixed "WP6: "; document, then test, then spec edit, then status table and decisions file; every push green and attribution-free (CI rejects both) *(default)*.
- Order *(default)*: ledger conditions section first (so claims can cite it), then method, limitations, why-and-how, then the reconciliation and tests.
- WP6 may start as soon as its scope is approved; it does not depend on WP3 beyond the note about tool references *(default)*.

## Open decisions (for the supervisor)

None at problem level: spec §2 (including "Tensions, not variance"), §4, §6 and §9, the WP1 ledger and the confirmed breakdown answer them. The Agent's defaults list above is the one item for the supervisor to approve or change at the scope gate.
