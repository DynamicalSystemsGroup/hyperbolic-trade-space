# WP23 close-out — Scope of work: the supervisor's thresholds, eight traded metrics, the requirements read after the fit (one regeneration on the host)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` at acceptance |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP23-decisions.md`, section "Close-out: scope gate" *(default heading)* |
| **Acceptance record** | The supervisor's verbal acceptance at the gate, quoted verbatim in `work-packages/WP23-decisions.md`, after `work-packages/WP23-closeout-review.md` |

**Header note: one package, one stream, one regeneration.** One writer, the WP23 modeller's stream, in its own
worktree, makes every change below in the order of the Agent's defaults and pushes one or two steps at a time. The
regeneration runs once, on the host (the Mac), with the suite's tolerance branches (`PM-BRIEF.md`, "The container is a
gate check, not a unit step": the supervisor, 2026-11-10, 09:05, "i don't think we should be blocking on this ... you
can relegate this to an occasional regression test rather than blocking on it"). The container of record
(`hts-paper`), its exact-equality branches, the re-pinning of the exact outputs, the `hts-alt` robustness image,
`paper/container/RECORD.md` and the Linux dispatch are the driver's regression at the gate, not steps of this package.
IDs continue the parent package (`WP23-scope-of-work.md`: G1 to G8, D-1 to D-10, R-1 to R-15, OD1 to OD9). Drafted
2026-11-10 from the inputs under Purpose and `dev` at ee7704e.

## Purpose

WP23 is accepted (`WP23-decisions.md`, "WP23 final hash: db59365"), with three of the supervisor's items open at the
time: the four thresholds, the two metric redundancies, the proposals' feasibility. Each has since been answered or
ruled on, and every ruling lands in one model change and one regeneration so the datasets and the paper regenerate
once more, not twice (`WP23-decisions.md`, "The redundancy spike's answer and the driver's calls", "Sequencing").

The rulings, verbatim where the record quotes them:

- **The four thresholds** (2026-11-10, 07:55; the supervisor, from the ladder in `WP23-review.md`, "Proposed
  thresholds, revised for the gate popup"): peak slew power "2.6 W, all small and medium"; pointing error "0.0085 deg,
  admits 95 % of primary"; control effort "0.059 N.m.s, admits 90 % of baseline"; launch budget "90,643 USD (15.11 kg,
  admits 95 %)". Disposition: 2.6 W; 0.008495 degree; 0.05922 N·m·s; 90,643 USD at the illustrative 6,000 USD/kg
  (15.107 kg); each labelled as his choice from the loop's ladder, no longer "illustrative 20 %".
- **The pointing-error threshold stands** (08:55): "Keep 0.0085 deg". The baseline configuration fails it (0.0155
  against 0.0085 degree); the case prose and the model's doc say so, with the baseline regime's pass fraction (63.7 %).
- **The redundancies** (08:00, the supervisor: "if the redundancy is a modelling issue then you clean it up. otherwise
  ... simplying the analysis to be an outcome of the analysis"; 08:20, the driver's calls on
  `WP23-rounds/spike-redundancy.md`): the eclipse reserve and the depth of discharge are one inequality, a modelling
  issue, option A1 (the reserve's calc and requirement leave the model; `dod_ok` enters the case's flags; eight traded
  metrics; a contract amendment); the power margin and the energy balance are a property of the system in its ranges,
  option B1 (the association step in the case analysis; no model change).
- **The requirements and the trade study** (08:05, 08:35, 08:45; spikes A and B under `WP23-rounds/spikes/`), and the
  supervisor on their presentation (08:50): "i'd lean toward fitting without threshold requirement, then treat the
  cuts along the requirements as an after the fact analysis. we can keep that in repo but we should restrict how much
  the paper covers this ... a sentence or two in the dicussion suffices since it will be backed up by our research
  records in the repo". Disposition: the fit of record stays the fit on the feasible set; spike B's requirements table
  and spike A's constrained-against-unconstrained table live in Appendix D and the docs' case page; the spike reports
  are the research record; the check section says plainly what spike A found about the proposals; one or two
  Discussion sentences, drafted as candidates for his review.

The outcome: the model carries his four values and eight traded metrics; the case and the paper are regenerated once
on it, every moved number explained; the full case analysis reads the requirements after the fit, in tables.

Inputs: `WP23-decisions.md` (from "The four thresholds" to the end), `WP23-rounds/spike-redundancy.md`,
`WP23-rounds/spikes/spike-A-with-and-without-infeasible.md`, `WP23-rounds/spikes/spike-B-requirements-and-the-fit.md`,
`WP23-scope-of-work.md`, `WP23-review.md` ("Proposed thresholds, revised for the gate popup"), `swap-evidence.md`
("WP23 data gate: old v2 ..."), `interface-contract.md` (rows 12 to 14), `PM-BRIEF.md` ("The container is a gate check,
not a unit step", "Derivation pushes are mechanical"), `docs/examples.md`, `examples/adcs/model_v2/cubesat.sysml`,
`examples/adcs/case-model.md`, `driver-log.md` ("Waiting for the supervisor").

## Goals

- G9. **The model at the supervisor's values, eight traded metrics.** `cubesat.sysml` carries the four requirements at
  2.6 W, 0.008495 degree, 0.05922 N·m·s and 90,643 USD (15.107 kg at the illustrative 6,000 USD/kg), each labelled as
  his choice from the ladder; the eclipse-reserve calc and requirement are gone; the depth of discharge is the metric
  and the requirement for the eclipse energy; the model's doc says plainly that the baseline configuration fails the
  pointing-error requirement (0.0155 against 0.0085 degree), with the baseline regime's pass fraction (63.7 %) beside
  it; `dod_ok` is one of the case's feasibility flags; the contract, the toolkit gates, the views and the coverage
  table follow.
- G10. **One regeneration on the host, with the data-gate comparison.** The datasets, the case's records and the
  paper's numbers regenerate once on the eight-metric model with the suite's tolerance branches; every moved number is
  listed with its cause in the comparison form of D-9.
- G11. **The requirements and the redundancies read in the full case analysis, in tables.** The association step
  (option B1), spike B's requirements table and spike A's constrained-against-unconstrained table, in Appendix C.5 and
  D and on the docs' case page, from the same regeneration; no new figure. The fit of record is unchanged in kind: the
  fit on the feasible set, no threshold imposed before it.
- G12. **The paper's prose on the record, kept tight.** The check section says plainly what spike A found about the
  proposals; the Discussion gains one or two candidate sentences for the supervisor; nothing else of the options
  enters the paper. Appendix E's table renders its mathematics.

## Non-goals

- Any change to the fit, the estimator or the derivations: nothing under `src/` or `derivation/` (none expected: the
  contract's pinned names under `src/` are not touched by a case-side metric change). Model, fit and analysis stay
  apart: the model changes, the fit runs unchanged, the analysis reads the result.
- New figures (spike A's log-plane figure and spike B's relaxation-ladder figure are not placed; the tables say what
  they would). Existing figures regenerate with the data only.
- The datasets' sampling, seeds and scenario constants: unchanged beyond the model edits of G9.
- Training the proposer on the fully feasible rows (future work, said in the paper); restating the check's criterion.
- The supervisor's pending items beyond the two candidate Discussion sentences (listed under Open decisions as
  pending, not open).
- The container run, the exact-equality re-pinning, `paper/container/RECORD.md`, the `hts-alt` run and the Linux
  dispatch: the driver's at the gate.
- The frozen generation (`examples/adcs/data/*.csv`) and the v1 model (`examples/adcs/cubesat_tradespace.sysml`).
- Historical notes under `docs/superpowers/notes/` that cite the nine-metric or slew-time data as dated evidence.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-11 | The model edit, `examples/adcs/model_v2/cubesat.sysml`: the four requirements at the supervisor's values as literal thresholds in `budgets`, each doc naming his choice and its ladder row (`WP23-decisions.md`, "The four thresholds"), the "PROPOSED ... 20 %" doc and `budgets.margin` gone, 6,000 USD/kg still labelled illustrative; `EclipseReserve` and `EclipseReserveRequirement` removed with their `satisfy`, verification entry, place in the experiment's return tuple and the header doc's metric list (eight); the header doc's sentence that the baseline configuration fails the pointing-error requirement, 0.0155 against 0.0085 degree, with 63.7 % of the baseline regime's feasible designs passing | G9 |
| D-12 | The model's followers: the toolkit gates (`tests/test_model_checking_v2.py`, `tests/test_system_model_v2.py`, `tests/test_system_model_v2_r1.py`, `tests/test_mutation_v2.py` as they pin the model), `examples/adcs/model_v2/ledger_gate.py` (run on the host, its note naming the close-out and the platform), the views at revision 9 by `docs/superpowers/notes/spike-sysml-diagrams/project.py` with the paper's byte copies (`paper/figures/fig-assembly-view.png`, `fig-behavioural-view.png`), the coverage table (`coverage.py`, `views/coverage.md`, `views/coverage.csv`, `tests/test_model_coverage.py`) | G9 |
| D-13 | The case code for eight metrics and the flag: `examples/adcs/case.py` (`_ATTRS` and its parallel tuples, `CUBESAT.flags` gains `dod_ok`), `k_terms.py`, `cubesat_model.py`, `experiments/cubesat_oracle.py`, `experiments/definitions.py`, `experiments/compare.py`, `generate_dataset.py`, `make_check_designs.py`, `model_v2/diagnostic_pair.py`, `paper/generate_model.py`, and the tests that pin nine (`test_case`, `test_cubesat_oracle`, `test_diagnostic_pair`, `test_model_coverage`, `test_interface_contract`, `test_paper`, `test_site`, `test_cubesat_model`, `test_check_designs`, `test_adcs_enrichment`, as each pins it) | G9 |
| D-14 | The contract amendment, `work-packages/interface-contract.md` and `.toml`: row 15, `contract_version` 15; `case.v2.traded_metrics` eight; the v2 headers without `eclipse_reserve_wh` *(default; see Agent's defaults)*; `dod_ok` in a pinned flag list if the manifest pins the case's flags (today it pins none for v2: the row says so) | G9 |
| D-15 | The regeneration on the host: `examples/adcs/data/v2/*` and `data/scope-sensitivity/scope_sensitivity_v2.csv` with ledger entries `v2-primary@6`, `v2-baseline@6`, `v2-check-predictions@6`, `v2-check-designs@6`, `scope-sensitivity-shared-subspace-v2@5` (`experiments/ledger/ledger.jsonl`); the K record (`k_terms`); the check designs and predictions; the coverage table; `tests/data/v2_first_designs_of_record.csv`; `examples/adcs/experiments/reports/*` (`sensitivity.json`, the change register, the v1-v2 report as their generators write them); `paper/environment_values.toml`, `paper/environment_reference.npz`, `paper/stability_extra.json`; both notebooks executed with their figures; `docs/examples.md`'s numbers | G10 |
| D-16 | The data-gate comparison, a new section of `work-packages/swap-evidence.md`, "WP23 close-out: nine metrics against eight" *(default title)*, in D-9's form: "Changed conclusions (read first)"; the files with old and new hashes; every moved number with its size and cause (the reserve's removal from the metric set; `dod_ok` entering the flags; the host regeneration against the container's); the conclusions item by item; the section-4 list of paper and docs cells by cell id with cause | G10 |
| D-17 | The case analysis additions in the same regeneration, generated by `case.py` functions *(default names: `association_all_pairs`, `requirements_table`, `design_sets_table`)* and printed by the notebooks: (a) the association of every pair of traded metrics over the feasible designs per regime, pairs at \|Spearman\| ≥ 0.99 named as one axis, the exponent reading summing a named pair per term (Appendix C.5 a row and a sentence, D.3, D.4); (b) spike B's requirements table (per requirement and regime: limit, pass fraction, band designs excluded, K = 1 exponent, price against the band, the two largest elasticities; one joint row); (c) spike A's constrained-against-unconstrained table (all designs, the feasible set, the requirement-constrained set, per regime: sizes, the one-term contending set and leaders, the three-term term types, the zero set, where the baseline configuration and the check designs sit). (b) and (c) in a new Appendix D section appended after D.16 *(default: D.17, so no existing D number moves)*; the docs' case page (`docs/examples.md`) carries (a)'s sentence and (b) and (c) | G11 |
| D-18 | The prose: `paper/paper.ipynb` cells `sec-case-analysis-5` and `num-predict-reading` (the proposals reached the four-metric frontier by spending the battery and fail the depth-of-discharge requirement; training on the fully feasible rows is future work), `sec-discussion` (one or two candidate sentences); `claims_register.toml` rows for each new or changed claim; `examples/adcs/case-model.md` (the four values as his, the baseline failing the pointing-error requirement with 63.7 %, eight metrics, the reserve's removal and why); `glossary.yaml` (the MoP entry's list loses the eclipse reserve; no entry for it exists); `paper/generate_gaps.py` (Appendix E's table renders `$...$` as mathematics in the staged page) | G9, G12 |
| D-19 | The review record `work-packages/WP23-closeout-review.md` *(default)*: the checks run with results, the candidate Discussion sentences verbatim for the supervisor, the two spike tables against the spikes' numbers, the fresh reviewer's data-gate review verbatim with dispositions | G10, G11, G12 |
| D-20 | The decision records, `work-packages/WP23-decisions.md`: the scope gate, the gate's dispositions, the supervisor's acceptance, verbatim | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-16 | The model's four requirements read the supervisor's values: 2.6 W, 0.008495 degree, 0.05922 N·m·s, 90,643 USD at 6,000 USD/kg (15.107 kg); each doc names his choice; no "20 %" and no "PROPOSED" label remains; the rate is labelled illustrative | `grep -n "2.6\|0.008495\|0.05922\|90643\|6000" examples/adcs/model_v2/cubesat.sysml`; `grep -n "20 %\|PROPOSED\|margin" examples/adcs/model_v2/cubesat.sysml` finds no threshold use; `views/coverage.md` lists the four values; a test in `tests/test_system_model_v2.py` reads them through the toolkit |
| R-17 | The eclipse reserve is absent from the model, the case code, the v2 data and the coverage table; eight traded metrics | `git grep -n "EclipseReserve\|eclipse_reserve" examples/adcs/model_v2 examples/adcs/data/v2 examples/adcs/case.py examples/adcs/k_terms.py examples/adcs/experiments/*.py` returns nothing; `coverage.md` has eight metric rows |
| R-18 | The baseline configuration's failure of the pointing-error requirement is stated plainly, without hedging, with 63.7 % beside it, in the model's doc and in `case-model.md` | `grep -n "0.0155\|63.7" examples/adcs/model_v2/cubesat.sysml examples/adcs/case-model.md`; read |
| R-19 | `dod_ok` is a flag of the case; the feasible sets stay 706 and 780 (the reserve's positivity removed exactly the `dod_ok` failures, `spike-redundancy.md`) | `uv run pytest tests/test_case.py` with a test that `CUBESAT.flags` contains `dod_ok` and the feasible counts are 706 and 780 |
| R-20 | The toolkit gates pass on the edited model; the views are at revision 9 and byte-identical over three runs; the coverage table regenerates equal to the committed one | `REQUIRE_OPENSYSML=1 uv run pytest tests/test_model_checking_v2.py tests/test_system_model_v2.py tests/test_model_coverage.py` with the pinned binary; the existing views test |
| R-21 | The contract and the data agree: row 15 names the metric-set change, the side affected and the approval; `contract_version` 15 | `uv run pytest tests/test_interface_contract.py tests/test_v2_data.py` |
| R-22 | The ledger has the five new entries, none dirty, the platform the host's; `verify` reports 0 drifts after the regeneration | `PYTHONPATH=examples/adcs uv run python -m experiments verify` |
| R-23 | The host is green: the fast suite, lint, format, lock, vocabulary | `uv run pytest -q -m "not slow"`; `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check`; `uv run python scripts/check_vocabulary.py` exits 0 |
| R-24 | The comparison lists every moved number with its size and cause, the changed conclusions first, and the paper's and docs' cells by cell id with cause (D-9's section-4 form); a changed conclusion is interrogated and resolved or brought to the driver with the record | D-16 read item by item by the fresh reviewer (R-30) and the driver |
| R-25 | The association table covers every pair of the eight traded metrics over the feasible designs in both regimes; every pair at \|Spearman\| ≥ 0.99 is named as one axis and the exponent reading sums it per term in D.3 and D.4; C.5 carries the row and the sentence; the docs' case page carries one sentence | a test in `tests/test_case.py` on the function's output (28 pairs per regime; the named set equals the pairs at ≥ 0.99); inspection of the staged appendix and `docs/examples.md` |
| R-26 | Spike B's requirements table is in Appendix D and on the docs' case page with spike B's columns and a joint row; each number equals spike B's at the paper's precision, or the comparison lists it with its cause (the eight-metric data) | the reviewer re-runs `case.requirements_table` *(default name)* and reads it against `spike-B-requirements-and-the-fit.md`, sections 1 and 2 |
| R-27 | Spike A's table is in Appendix D and on the docs' case page with its three sets per regime and the columns of D-17 (c), the conditioning and the temperature rule held fixed across sets as OD10 decides; each number equals spike A's at the paper's precision, or the comparison lists it with its cause (the eight-metric data; the conditioning rule of OD10) | the reviewer re-runs `case.design_sets_table` *(default name)* and reads it against `spike-A-with-and-without-infeasible.md` |
| R-28 | The fit of record is unchanged in kind: the fit on the feasible set (the generation's flags), no threshold imposed before it; the requirement cuts appear only in the after-the-fact tables | the paper's numbers come from `case.fit_study` on the feasible study; `git diff` shows no threshold in `load_study` or `feasible_mask` |
| R-29 | The paper's prose: the check section states spike A's finding on the proposals plainly and names training on fully feasible rows as future work; the Discussion gains at most two sentences, listed verbatim in the review as candidates; no other option of the spikes enters the paper; each new or changed claim has a register row | `git diff paper/paper.ipynb` limited to the cells of D-18 and the regenerated outputs; `uv run pytest tests/test_claims_register.py tests/test_paper.py` |
| R-30 | A fresh reviewer runs the code, reads the comparison, the model's pair of views, and the staged paper in a browser (Appendix C.5, D.3, D.4, D.17, E, the check section, the Discussion), and reports verbatim; its findings get dispositions | D-19 |
| R-31 | Appendix E's table shows typeset mathematics, no raw `$...$`, in the staged page | the browser pass of R-30; a test in `tests/test_paper.py` that the gaps table's HTML carries no unrendered `$` pair *(default)* |
| R-32 | The seam holds: nothing under `src/` or `derivation/`; no frozen data file; nothing outside the blast radius | `git diff --stat ee7704e...HEAD` at the gate |

Both platforms at the gate (the Linux dispatch, the container regression with the exact branches re-pinned and
`RECORD.md` written) are the driver's, outside this package's requirements.

## Blast radius

The files this package may change; anything else is a stop and a question to the PM.

- Model and views: `examples/adcs/model_v2/` (`cubesat.sysml`, `coverage.py`, `diagnostic_pair.py`, `ledger_gate.py`,
  `views/*`); `docs/superpowers/notes/spike-sysml-diagrams/project.py`.
- Case code: `examples/adcs/case.py`, `k_terms.py`, `cubesat_model.py`, `generate_dataset.py`, `make_check_designs.py`,
  `examples/adcs/experiments/{cubesat_oracle,definitions,compare}.py`, `examples/adcs/experiments/reports/*`,
  `examples/adcs/experiments/ledger/ledger.jsonl`.
- Data: `examples/adcs/data/v2/*`, `examples/adcs/data/scope-sensitivity/scope_sensitivity_v2.csv`,
  `tests/data/v2_first_designs_of_record.csv`.
- Paper: `paper/paper.ipynb`, `paper/supporting_material.ipynb`, `paper/figures/*.png` (regenerated, none added),
  `paper/generate_model.py`, `paper/generate_gaps.py`, `paper/environment_values.toml`,
  `paper/environment_reference.npz`, `paper/stability_extra.json`, `paper/paper_stability.py` (docstring only, if it
  names the reserve).
- Docs and prose: `docs/examples.md` (and its generated figures as the build writes them),
  `examples/adcs/case-model.md`, `claims_register.toml`, `glossary.yaml` (the MoP entry's list only).
- Contract and tests: `work-packages/interface-contract.{md,toml}`; the tests named in D-12, D-13, R-19, R-25, R-29,
  R-31; `scripts/check.py` (the path-to-test map, if a new test file is added).
- Records: this file, `work-packages/WP23-closeout-review.md`, `work-packages/WP23-decisions.md` (new sections only),
  `work-packages/swap-evidence.md` (the new section only).
- Never: `src/`, `derivation/`, `examples/adcs/data/*.csv` (frozen), `examples/adcs/cubesat_tradespace.sysml`,
  `paper/container/RECORD.md`, other `work-packages/*.md`, other files under `docs/superpowers/notes/`,
  `pyproject.toml`, `uv.lock`. `glossary.yaml` beyond the MoP entry's list only if a term leaves the corpus (dead-entry
  rule; no eclipse-reserve entry exists today).

## Definition of good

- A systems engineer reading the model sees the supervisor's four requirements as his, eight metrics each with one
  definition and no requirement stated twice, and a baseline configuration whose failure of one requirement is said
  in a sentence; the case regenerates once and every moved number is explained; the full case analysis shows how the
  fitted frontier reads a set of requirements after the fit (what each one costs at the frontier, which near-frontier
  designs it removes, and how the fit on the requirement-constrained set differs from the fit of record), with the
  spike reports as its research record; the paper stays tight: one plain check sentence and one or two Discussion
  sentences.

## Definition of good enough

- R-16 to R-23 hold on the host.
- The comparison (D-16) lists every moved number and every changed conclusion with its cause, and the section-4 cell
  list (R-24).
- The three tables are generated and placed (R-25, R-26, R-27), the fit of record unchanged in kind (R-28).
- The prose items hold (R-29, R-31) and the candidate Discussion sentences are in the review for the supervisor.
- The fresh reviewer's data-gate review is recorded with every finding disposed (R-30); R-32 holds. Stop there and
  present to the driver for the gate's container regression and Linux dispatch.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

One item for the driver's approval. Each is marked *(default)* where it appears.

- **Order of steps** (one push per step, or two steps per push where one cannot be green without the other): (1) the
  model, its toolkit gates, the views (revision 9), the coverage table; (2) the case's flag (`dod_ok`) and the
  eight-metric case code with the contract amendment; (3) the regeneration on the host (datasets and ledger, records,
  notebooks, figures, docs numbers); (4) the comparison (D-16); (5) the analysis additions (D-17), regenerated in the
  same notebook execution as (3) or re-executed once with it; (6) the prose (D-18) and the Appendix E fix; (7) the pins
  the tolerance branches read (`environment_values.toml`, `environment_reference.npz`, the first-20 recording) written
  from the host run; the exact pins are re-written by the driver's container regression. Steps (2) and (3) land in one
  push if the code and the data cannot be green apart (as 77844c5).
- **The column**: `eclipse_reserve_wh` leaves the v2 datasets with its calc (a column with no model calc would be
  untraced); the spike's sub-option of keeping it as a derived, non-traded column is not taken.
- **Thresholds in the model** as literal values in `budgets` with a doc per value citing `WP23-decisions.md`, replacing
  the `margin × baseline` expressions; the baseline measurement stays as the record of the baseline's values.
- **The association step**: Spearman and Pearson of the log metrics over the feasible designs, per regime; "one axis"
  read on \|Spearman\| ≥ 0.99 as recorded; the summed reading adds the named pair's exponents per term and prints the
  sum beside the pair.
- **Spike tables' sets on eight metrics**: spike A's "all designs" is its U8 (all 1000 designs on the eight metrics),
  since U9 needed the reserve; F and R as in the spike; the four thresholds read as `<=` with absolute tolerance 1e-9.
- **Placement**: (b) and (c) in a new section D.17 so no D number moves; on the docs' case page the same two tables at
  the docs' precision under one short heading, with the association sentence in the case's bullet list.
- **Host regeneration of the environment-of-record files**: written on the host so their keys and columns match the
  eight-metric data and the tolerance branches pass; the driver's container regression re-pins the exact values.
- **Names**: the review `WP23-closeout-review.md`; the comparison section title as in D-16; the `case.py` function
  names as in D-17; ledger ids `<id>@<n>`; the decision headings "Close-out: ..." in `WP23-decisions.md`.
- **Appendix E's fix** in `paper/generate_gaps.py` (the table's cells emitted so MyST typesets the inline
  mathematics), checked in the staged page.
- **Reviewer**: one fresh agent, `work-acceptance` style, that runs the code and reads the staged paper in a browser;
  its report quoted verbatim in the review.

## Open decisions

- **OD10. Which conditioning the constrained-against-unconstrained table uses** *(raised by the scope's trace check)*.
  The driver's call holds "the conditioning and the temperature rule fixed, as the spike did" (`WP23-decisions.md`,
  "Spike A ..."). Spike A's script conditions each design set on its own rows (`spike-A/spike_a.py`, `study_on`:
  `case._condition(rows, ...)` on the subset), and spike B found that re-conditioning the constrained subset is what
  moves peak slew power from 0 to 0.24 in the primary regime, "a conditioning artefact, not a finding"; on the
  feasible set's conditioning the primary regime's one-term exponents move by at most 0.013 and the contending set
  stands, and the baseline regime swaps power margin and energy balance (one axis) (`spike-B`, section 4;
  `spike-B/run2.log`). So the table, R-27, and the content of the Discussion candidate ("pre-imposing the four
  requirements changes the contending set while removing the infeasible designs does not") depend on the choice.
  Options: (a) the feasible set's conditioning applied to every set (spike B's caution); spike A's constrained rows are
  recomputed and the comparison lists the differences, and the Discussion candidate follows the recomputed table /
  (b) each set conditioned on its own rows, as spike A ran; spike A's numbers reproduce, and the table states the rule
  with spike B's same-conditioning reading beside it / (c) both, one column per rule.

Pending with the supervisor (not open for this gate; the work proceeds on the recorded calls): his review of the
candidate Discussion sentences (D-18, D-19); the proposals' feasibility under "Waiting for the supervisor" in
`driver-log.md`, applied here as the driver's call of 08:45 (keep them as check designs, say it plainly, training on
fully feasible rows as future work); his review of the redundancy calls (A1, B1) at his review, as the 08:20 record
says.

## Gate outcomes

- 2026-11-10, 09:50: approved for execution by the driver under the mandate; OD10 resolved as (a), the feasible
  set's conditioning applied to every set, in `WP23-decisions.md`; the Agent's defaults accepted as one item.

- 2026-11-10, during execution: the blast radius is amended to name `paper/generate_results.py`, the home of every
  Appendix D table (the driver's decision on the executor's question, relayed by the PM: "(a). paper/generate_results.py
  is the home of every Appendix D table, so the three thin wrappers ... and the one sentence each in exponents_and_terms
  and regime_comparison go there; the scope's blast radius is amended to name it"). Under the same reading the executor
  also touched, and names here for the reviewer: `paper/generate_findings.py` (the generated text of
  `num-predict-reading`, D-18's cell), `paper/length_ledger.toml` (the length ledger the scope's prose rows need),
  `examples/adcs/experiments/check_designs.py` and `experiments/sensitivity.py` (`dod_ok` joins their feasibility
  filters, the hidden dependency of the A1 call), `docs/superpowers/notes/paper-sources/method.md` and the deletion of
  `docs/superpowers/notes/k3-cubesat.md` (the brief's call on the stale K record), `tests/test_v2_data.py`,
  `tests/test_site.py` (the examples page's word budget, 650 to 720, its job stated) and
  `examples/adcs/experiments/reports/change-register.md` (CR-5), `tests/test_soft_fit.py` (the comment on the
  re-recorded reference) and `tests/data/soft_fit_default_reference.npz`.
