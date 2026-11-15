# WP56 — Scope of work: the case and the discussion (Sections 7 to 9)

| | |
|---|---|
| **Status** | see INDEX.md (DRAFT for the driver's approval as his proxy; executes after WP55 lands, one notebook writer at a time) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; a branch `wp56` in its own worktree; the SysML v2 model and the case code under `examples/adcs/` |
| **Approval record** | His directions and choices, verbatim in `WP56-decisions.md`; the driver's approval as proxy recorded there |
| **Acceptance record** | The driver's soft-confirm of each section on screenshots against `paper-requirements.md`, the figures at the first three depths; his read afterwards |

## Purpose

His direction (`WP56-decisions.md`): the model is in the repository, so the paper narrates the case and ties it to the
thesis; Case construction makes the approach actionable, the analysis shows the way from a model to a decision with
the thread through code and data preserved; figures carry the page; the Discussion answers the value proposition of
the abstract and Section 1, revisits the three layers of Section 2 and leads into Future work; no spurious detail, a
caveat stated once; the paper is a view and the SysML v2 model is the model; "model" names its object. His choices:
the three-stakeholder ternary kept and explained (unit cost, fleet cost, coverage probability; sponsor, manufacturer,
operator; the collapse to one trade-off because fleet cost is unit cost times fleet size, said and refittable), no
equation in that figure; Figure 7 as one triangle. The lineage spike (`WP56-rounds/spike-lineage.md`) supplies the
conventions; the register the requirements.

## Goals

- G1. **Case construction narrates the case from the SysML v2 model as it is now.** Opens with the problem as a
  triple (the metrics maximised, the design variables, the feasibility conditions and requirements), carries one
  configuration through every step, names the measures of effectiveness and the requirement ordering once in one
  table, states data provenance in one sentence (the model, the data of record, the generator), and cites the
  OpenMDAO paper's CADRE cubesat as the precedent. Every sentence about the model checked against the model as the
  WP22 adoption and the WP23 realism rounds left it (the coupling table, the measures of effectiveness, launch cost
  reading mass, settling time the one time metric, the regenerated data of record); stale sentences rewritten from the
  record or cut; pricing detail and the percentile and strict-convexity remarks moved to Appendix C or D.
- G2. **Case analysis goes from the model to a decision.** What contends, with what elasticities, where designs sit,
  the requirements applied after the fit as constraints on the solution space with their excluded counts, the
  decision the executives make with one stakeholder per objective (sponsor, manufacturer, operator), and the closing
  sentence that gives the decision and the code and data that produced it (the table, the fit call, what cannot be
  rerun). K = 2 is the case's reading. The generated nondominated sentence stays if it opens the reading, else goes
  to Appendix D.
- G3. **The figures carry the sections on a skim.** Figure 7, the tension matrix, as one triangle, the triangle and
  the row order settled by the figure loop on the actual values and any range statement derived and checked first,
  the sign and reciprocal convention one across matrix, caption and prose; the decision-maker's ternary of unit cost,
  fleet cost and coverage probability, the measure named and no formula in the figure, with the prose that says the
  three objectives were not guaranteed to collapse to one trade-off, that on this model they do and why, and that a
  revised cost scaling is checked by refitting; every caption cut to what is drawn, the Shows and Does-not-show lines
  moved to the review record; each figure through the loop at the first three depths with screenshots before the
  section is soft-confirmed; the output printed beside the call that made it where a number is read from a cell.
- G4. **The performance aggregate as a modelling choice in the model.** Coverage probability defined and justified in
  the SysML v2 system model as a derived attribute of the fleet (formula, units, constants with their readings), the
  comparison across the three definitions and the decision's stability kept in the analysis record
  (`WP56-rounds/ternary/readout.md`, extended if the build changes a number); the paper presents the selected measure
  in a sentence with a reference to the model and the record.
- G5. **The Discussion answers the paper.** Interpretation as human validation; the value proposition of the abstract
  and Section 1 (interpretability at scale; reuse of the decision analysis pipeline via unsupervised learning)
  answered against what the case showed; the three layers of Section 2 revisited in a paragraph; the limits in one
  passage at the end, the repeats in captions and case text deleted; the method points that reopen earlier sections
  ("Three claims", "Why a surface", "Numerical") cut or moved to the appendix section WP57 builds; it leads into
  Future work.
- G6. **The argument preserved and the words down.** A table of every claim, number and figure in Sections 7 to 9
  before and after, each with its generator or record; Sections 7 to 9 together not above their count at WP55's head
  (1,336, 1,426 and 558 words of prose today), the removal of the caveats and method detail expected to shrink them.

## Non-goals

- Sections 1 to 6, 10 and 11 (WP53 to WP55, WP54); the appendices beyond the receiving paragraphs of Appendix C and
  D (WP57). Any new model detail beyond the coverage attribute. Any change to the data of record or the lemma scripts.
  Choosing the aggregate for the ternary's looks.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `examples/adcs/` and the SysML v2 model with the coverage attribute, its documentation in the model, the case's generator producing the ternary from the data of record, the tension matrix routine with the `triangle` option | G3, G4 |
| D-2 | `paper/paper.ipynb` Sections 7 to 9 reworked, notebooks re-executed; Appendix C and D receiving the moved detail | G1, G2, G5 |
| D-3 | `WP56-review.md`: the before-and-after table (G6), each sentence about the model with its record, the figure loop's screenshots and sentence tests in `WP56-rounds/`, the checks | G6 |
| D-4 | The register rows, paper tests, length ledger, vocabulary baseline following; `review/open-questions.md` extended | G6 |
| D-5 | Landed on `dev` by the driver after the soft-confirm of the three sections, with CI | all |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every sentence about the cubesat model matches the SysML v2 model and the data of record as they are now | the D-3 table, each row with its record (the model file, the generator, the WP23 round) |
| R-2 | Figure 7 is one triangle with one convention across matrix, caption and prose; no caption carries Shows or Does not show | the rendered page; `grep` of the captions |
| R-3 | The ternary names the measure and carries no formula; the prose says what it shows and why it collapses | the rendered page; the register entry |
| R-4 | Limits once, at the end of the Discussion | `grep -c` of the limit sentences across Sections 7 to 9 |
| R-5 | Words: Sections 7 to 9 together at or below 3,320 | `wc -w` before and after in the review |
| R-6 | The lemma chain and proof map unchanged; the data of record unchanged (`git diff --stat` on `examples/adcs/data/`) | `derivation/run.py`, `python -m derivation.proofmap`, `git diff` |
| R-7 | Lint, format, lock, residuals, vocabulary, the fast suite, the slow paper tests, CI both platforms | as WP53 |

## Definition of good

A reader who skims the figures of Sections 7 to 9 and reads their captions follows the case from the model to the
decision and sees the three stakeholders' trade-off; a reader of the prose meets each fact once, with its source.

## Definition of good enough

R-1 to R-7 met; the driver's soft-confirm of the three sections and their figures on screenshots; his later edits light.

## Definition of done

Good enough met, landed on `dev`, his read recorded in `WP56-decisions.md`.

## Open decisions

None for him; the tension matrix's triangle and row order are the driver's call on the figure loop's screenshots.

## Agent's defaults

- Two units in sequence: the first builds D-1 (the model attribute, the generator, the routine option, the figure loop
  on both figures) and lands its figures' records; the second rewrites the prose of Sections 7 to 9 on the landed
  figures. The driver soft-confirms between them.
- Row order of Figure 7: by exponent, largest first, unless the figure loop shows another order reads better; the
  triangle whose values the caption can state in one sentence.
- Coverage probability's constants take the spike's values (p0 = 0.2, e0 = the pointing requirement) and are stated
  in the model with their readings.
