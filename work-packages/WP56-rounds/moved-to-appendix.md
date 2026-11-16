# WP56: what left Sections 7 to 9 for Appendix C or D (for WP57c to land)

The second unit of WP56 (branch `wp56p`) rewrote Sections 7 to 9 of `paper/paper.ipynb`. Each entry below is a
paragraph, sentence or generated sentence that left those sections, verbatim as it stood at dev b8846a3, with the
subsection of the supporting material that should hold it and what that subsection already holds. WP57c lands each
(or records why not) and retires the line. Sentences that belong to "Assumptions, limitations and open questions"
went to `work-packages/WP57-rounds/assumptions-queue.md` instead (WP57d). The register rows named here were retired
with the sentence (`WP56-review.md`, the register table).

## Typed paragraphs and sentences

| Left | Verbatim | Target | Already there |
|---|---|---|---|
| Section 7, cell `sec-case-construction-1c` | "The two costs price the bus, the attitude-control parts, assembly and test, and launch, and leave out the payload, communications, operations and the rest, so each is a lower bound on a full costing." | C.8 | yes, in other words ("The model is a demonstration ... Its cost is a lower bound"); nothing to land |
| Section 7, cell `sec-case-construction-1c` | "The launch slot (a 50 kg minimum) is not costed, so for fleets of one to three the slot is up to 4.2 times the reported launch cost, and at three at most 1.4 times ({ref}`Appendix C.8 <sub-c-8>`); the decision table's fleets are four and more." | C.8 | the launch slot and "4.2 times" are in C.8; the last clause is stale (the decision table now holds fleets of 4, 10 and 25 and the baseline's fleet of 1); land only if C.8 needs it, reworded to "the shortlisted fleets are four and more" |
| Section 7, cell `sec-case-construction-1c` | "The fleet cost requirement holds that covered cost under 6,000,000 USD, inside the sponsor's full budget of 8,000,000 USD." | C.8 | yes, verbatim in substance; nothing to land |
| Section 7, cell `sec-case-construction-1c` | "The fit ignores them all; {ref}`Appendix D.17 <sub-d-17>` reads them after it." | D.17 | the requirements-after-the-fit reading is D.17's; Section 8 now states the exclusions in a generated sentence (`requirements_sentence`); nothing to land |
| Section 7, cell `sec-case-construction-1b` | "whose limits are illustrative values chosen from a ladder of candidates by the share of designs each admits, not a mission's ({ref}`Appendix D.17 <sub-d-17>` gives the values)" (from "Six are read after the fit: four thresholds (peak slew power, pointing error, control effort and the launch budget, read as a limit on total mass at 7,000 USD per kilogram), whose limits ...") | D.17 (the four thresholds' provenance) | the values are in D.17; the ladder's provenance is in `cubesat.sysml` (part `budgets`); land one sentence in D.17 if it does not say where the four limits came from (register C500 retired) |
| Section 8, cell `sec-case-analysis-3b` | "{prf:ref}`thm-convex` gives convexity, not strict convexity. For two metrics with identical columns the loss is flat along their swap, so which of a pair that nearly coincides carries the exponent is not read as a finding. The sets are compared with such a pair counted as one (its exponents are still read apart, {ref}`Appendix D.3 <sub-d-3>`)." | D.4 (the regimes side by side) or D.3 | D.3's generated output mentions strict convexity; check that the "pair counted as one" rule of the regime comparison is stated in D.4 (register C409 retired) |
| Section 8, cell `sec-case-analysis-5` | "**Propose, predict, check** is a check of the regressor on a few proposals, not an estimate of a rate." | D.10 | land as D.10's opening if it does not say so |
| Section 8, cell `sec-case-analysis-5` | "A proposal is the pooled configuration predicted nearest white space of the four-metric chart, within a radius that a stated rule sets from the data: the 2nd percentile of the pool's nearest predicted distances to the 300 most isolated points of white space." | D.10 | no ("percentile" is not in the supporting material); land |
| Section 8, cell `sec-case-analysis-5` | "Turning a predicted level into a bounded outcome is the analyst's task and can fail while the fit is certified: a prediction outside the quantity's admissible range is reported as invalid, never clipped." | D.10 | no; land (register C041 retired; its backing, the admissibility module and test, carries over) |
| Section 8, cell `tab-decision-caption` | "Balanced between the terms is the design whose two K = 2 term levels are closest. The last two rows are context: the cheapest unit needs the largest fleet." | D.19 | the balanced rule is in D.19's rule paragraph; the table no longer has the row; nothing to land |
| Section 9, cell `sec-discussion` | "**Requirements after the fit.** Fitting first and reading the requirements after is the unconstrained-then-constrained reading of a trade study. **Numerical.** {ref}`Appendix D.17 <sub-d-17>` prices each of the six requirements read after the fit at the fitted reference surface and counts the near-frontier designs it excludes." | D.17 | the first sentence moved to Section 8 (register C406 re-anchored); the second is D.17's own content; nothing to land |

## Generated sentences (the call stays in `paper/generate_findings.py`)

| Left | Call | Target | Already there |
|---|---|---|---|
| Section 7, cell `num-participation` | `participation_sentence()` ("Of the thirteen traded metrics, two, the power margin and the battery peak power ratio, enter no contending set at K = 1 to 3 in either regime ...") | D.3 | D.3's outputs carry the participation counts; land the call in D.3 (register C491, C629 keep their generator anchors) |
| Section 7, cell `num-temperature` (its last two sentences) | `temperature_variants_sentence(study)` ("The robust scaler changes it: 8 metrics, 6 of the baseline's 7 among them, the largest exponent on total mass. The exponents' stability under resampling of the rows is not assessed at K = 1: the movement of an exponent vector is read from K = 2 (Appendix D.15).") | D.5 (the scaler variant); the second sentence is a limitation (queued too) | D.5 has the robust-scaler row; land the call in D.5 (C627, C628 re-anchored to the new function) |
| Section 8, cell `num-recovery` | `recovery_sentence()` ("**A known answer.** On the 20 planted tables the fit recovers all three terms to within 0.05 in 16, ... (Appendix D.14).") | D.14 | D.14's outputs carry "16 of 20"; Section 8 keeps `planted_sentence()`; nothing to land unless D.14 lacks the failure detail (C631 keeps its anchor) |
| Section 8, cell `num-k-temperatures` | `k_temperatures_sentence(study, fits)` ("Each K selects its own fit temperature by the same rule: tau = 42 and 113 at K = 1 and 2, with bands 1/tau of 0.0240 and 0.0088. The figures and the association reading use the K = 1 band at every K (gap G-9, Appendix E).") | D.15 | G-9 is in Appendix E; land the call in D.15 |
| Section 8, cell `num-tension` | `tension_sentence(study, fits, dec)` ("At the picked fleet (5 medium-wheel, fine-tracker satellites) the surface's tension between the operator's pointing error and the sponsor's fleet cost is -1.4 M USD per arcsecond ...") | D.19 | no; its pick is the old rule's (`between`, design 1858) and its stakeholder words are the old mapping (operator: pointing error). Land it reworded without stakeholders ("the surface's tension between pointing error and fleet cost at design 1858"), or retire it; register C797, C798 keep their generator anchors until then |
| Section 9, cell `num-predict-reading` | `predict_reading(pc, reg)` ("**What propose, predict, check showed.** Two of the three proposals are one configuration. ...") | D.10 | no; land the call in D.10 (C397, C398, C399, C405 keep their generator anchors). Section 8 keeps its finding in one sentence ("The proposals fail the depth-of-discharge feasibility condition ...", C404) |

## D.19 must follow the decision's new rules

Section 8's decision now uses one stakeholder per objective (sponsor: least fleet cost; manufacturer: least unit cost;
operator: largest coverage probability; between sponsor and operator: minimax regret on fleet cost and coverage
probability, each scaled from its best to its worst on the shortlist). D.19's rule paragraph (cell `app-D-decision`)
still names the old rules ("the operator alone the smallest pointing error; between them, ... pointing error and fleet
cost ...; balanced between the terms ..."). `generate_findings.decision` keeps the old picks, so D.19's tables
(`decision_detail`, `decision_designs`) are unchanged and still correct as tables; the working table now also carries
`coverage_probability` and `nd coverage` (nondominated on fleet cost and coverage probability, 17 of the 28). WP57c
rewrites D.19's rule paragraph to the four rules above and may add the coverage column and its nondominated mark to
`decision_designs_table`.
