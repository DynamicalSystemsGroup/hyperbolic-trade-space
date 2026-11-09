# WP21 - Scope of work: the response to the independent assessment

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `posynomial-invariant-form` (branch `dev`); this document lives in `work-packages/` |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP21-decisions.md` |
| **Acceptance record** | The supervisor's verbal acceptance, quoted verbatim in `work-packages/WP21-decisions.md` |
| **Evidence** | `work-packages/external-assessment-2026-11-09/{assessment.md,triage.md,verification.json}` |

## Purpose

The supervisor ran "a concurrent independent review and test session with a clean context and a different
genai stack" and asked the driver to "go through it and harvest feedback" (`triage.md`). The driver's triage
accepted findings A1 to A3 and A5 to A7, and recorded no action on A8. A4 (soft term aggregation is an
unnormalized sum) was put to the supervisor, who answered: "really the package should support both setups.
think of it as weighted vs not weighted and normalized vs not normalized. in practice these should be keyword
based. it should be pretty normal stuff to toggle in scikit-learn style unsupervised learning. you can also
defer weighted versus not weighted since i dont think we have that yet". This package applies those
dispositions: sentences in the paper and docs, one package toggle, one new reported count, and one frozen
fixture with a ledger gap. The intended outcome is that a reader keeps three claims apart (certificate,
observed geometry, usefulness outside the observations) and that no committed number moves.

## Goals

- G1. Three claims distinguished in one place each in the paper and the docs termination page (A1).
- G2. A one-term cap is explained as possibly hiding a trade-off elsewhere, with a planted example (A2).
- G3. Requested versus effective K is visible: a distinct-terms count beside the slack (A3).
- G4. The term aggregation is a keyword toggle, sum (default) or mean, with the bound stated for both and the
  duplicated-term effect documented (A4).
- G5. Equal mean slack with different boundaries is recorded as a ledger gap and shown by a frozen fixture (A5).
- G6. The responsibility for inverting a reference into a bounded outcome is stated, invalid intersections
  reported and never clipped (A6).
- G7. Conditioning is stated to belong to the question; designed samples are not independent observations (A7).

## Non-goals

- No automatic K selector or pruning; no objective that identifies unsampled boundary structure; no
  probabilistic calibration.
- No change to the objective or to any committed number: the default behaviour is today's.
- No economic case (Filecoin, RAI) in the paper; the assessment's bundles are not cited as reproductions (A8).
- Weighted versus unweighted terms (per-term weights in the aggregation): DEFERRED by the supervisor;
  candidate after 0.1.

## Deliverables

Blast radius is stated per deliverable; a file outside its list is not touched.

| ID | Deliverable | Blast radius | Serves |
|---|---|---|---|
| D-1 | Estimator keyword `term_aggregation` (`"sum"` default, `"mean"`), stored verbatim, validated in `fit`; used in `score_samples`, the soft fit's weights, objective, Hessian and certificate; docstring and doctest | `src/hyperbolic_trade_space/{estimator,solvers}.py`, `tests/test_estimator.py` | G4 |
| D-2 | Contract amendment (next version): the keyword and its values in `package.estimator`, change-log row | `interface-contract.md`, `interface-contract.toml`, `tests/test_interface_contract.py` | G3, G4 |
| D-3 | L10 extended to both forms (sum: max <= Phi_K <= max + log K / kappa; mean: max - log K / kappa <= Phi_K <= max); Appendix B regenerated in the same push | `derivation/lemma_10_extension.py`, the Appendix B generator and its output, `tests/test_derivation.py`, `tests/test_paper.py` | G4 |
| D-4 | Definition 3 and the docs fitting page name the toggle in one clause; the duplicated-term effect (log 2 / kappa) documented for the sum | paper source (through the paper stream), `docs/user-guide/fitting.md`, claims register rows | G4 |
| D-5 | Distinct-terms count in the termination record or the tension report (exponent vectors within a stated distance); K-sweep example and D.15 show it beside the slack | `src/hyperbolic_trade_space/{estimator,tensions}.py`, `interface-contract.*`, docs K-sweep example, paper Appendix D.15 | G3 |
| D-6 | Paper and docs sentences for A1, A6, A7 (certificate, boundary, prediction; invalid intersections rejected; conditioning and designed samples), each a claims-register row | paper sections 6/discussion/limitations and Appendix D (through P1), `docs/user-guide/{termination,prediction,conditioning,limitations}.md` (through P6), `tests/test_claims_register.py` | G1, G6, G7 |
| D-7 | Cap-plus-slope note on the fitting or tensions page, no economic case | `docs/user-guide/{fitting,tensions}.md` | G2 |
| D-8 | Frozen planted fixture (two envelopes, equal mean slack, different boundaries), ledger gap G-18, one sentence in the open questions | `tests/data/`, `tests/test_gaps.py`, `docs/superpowers/notes/abstraction-gaps.md`, paper Appendix E | G5 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `HyperbolicTradeSpace().term_aggregation == "sum"`; `get_params` round-trips; invalid values raise in `fit`, not `__init__` | `uv run pytest tests/test_estimator.py -k term_aggregation` |
| R-2 | With the default, every committed fitted number and every pinned test is unchanged | `uv run pytest -q` (no expected value edited; `git diff` shows none) |
| R-3 | With `"mean"`, `score_samples` and the soft weights use the mean over K terms; the score differs from `"sum"` by exactly log K / kappa; soft minimizers are equal | test over several K, kappa, d (not hard-coded d) |
| R-4 | `"mean"` with `term_temperature = inf` (or K = 1) equals `"sum"` | same test file |
| R-5 | Both bounds hold numerically on random data; the duplicated-term shift is log 2 / kappa under `"sum"` | lemma script plus `uv run pytest tests/test_derivation.py` |
| R-6 | L10 states both bounds; Appendix B is regenerated and matches | `uv run pytest -q tests/test_paper.py -k appendix_b` in a clean worktree at the pushed commit (PM-BRIEF, "Derivation pushes are mechanical") |
| R-7 | `parametrize_with_checks` passes with `xfail_strict=True` and the expected-failures dict unchanged | `uv run pytest tests/test_estimator.py -k sklearn` |
| R-8 | Contract manifest lists the new keyword and count; contract test passes | `uv run pytest tests/test_interface_contract.py` |
| R-9 | The distinct-terms count equals K on a planted K-facet set and falls below K where terms repeat; unchanged fits report the same other fields | test on planted data and on the repeated-term case |
| R-10 | The fixture's two fits have equal mean slack within a stated tolerance and boundaries that differ by more than a stated margin; G-18 lists the assessment as evidence | `uv run pytest tests/test_gaps.py` |
| R-11 | Each new paper or docs claim is a claims-register row; the docs build with no warnings | `uv run pytest tests/test_claims_register.py tests/test_docs.py` |
| R-12 | The gate: ruff check, ruff format check, `uv lock --check` pass at the commit to push | `uv run ruff check . && uv run ruff format --check . && uv lock --check` |

## Definition of good

- A reader of the paper or docs cannot take a certified fit for a validated forecast, a one-term cap for the
  absence of a trade-off, or a loss improvement across K for new geometry; the toggle is as ordinary as any
  scikit-learn hyperparameter; the planted fixture makes the equal-loss point teachable in one figure.

## Definition of good enough

- D-1 to D-8 delivered inside their blast radii; R-1 to R-12 pass with the commands shown in the report.
- No committed number changed; the default aggregation is the sum.
- Each assessment finding A1 to A7 is traced to a deliverable in the report; weighted terms appear once, as a
  deferred candidate after 0.1.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- Keyword name `term_aggregation`, values `"sum"` and `"mean"` (sklearn-style names), for the supervisor to
  strike or rename. *(default)* D-1, D-2.
- Distinct-terms count lives in the termination record, field `n_distinct_terms`, with the distance a named
  constant in `solvers`; moved to the tension report if the contract reads better. *(default)* D-5.
- Fixture size, seeds and tolerances; ledger gap numbered G-18 as the triage says. *(default)* D-8.
- Which paper and docs paragraphs carry each sentence, within the files listed. *(default)* D-4, D-6, D-7.
- Contract version number: the next free one at the time of the amendment. *(default)* D-2.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: A4 by the supervisor's answer quoted above; no
decision here changes a term's meaning or a conclusion, because the default keeps today's definition. If the
supervisor strikes the default aggregation (making the mean the default), every committed soft-fit number
would shift by log K / kappa and the scope would need an amendment.

## Gate outcomes

- 2026-11-09: approved for execution by the driver under the mandate; no open decision remained. Recorded in `driver-log.md`.
