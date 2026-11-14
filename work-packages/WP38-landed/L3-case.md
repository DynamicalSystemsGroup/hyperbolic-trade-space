# WP38 landed: unit L3-case

Surfaces: `examples/adcs/case-model.md` (slots example-01, example-02) and the `short` fields of
`glossary.yaml` (the Glossary-page part of glossary-01). Appendix A rows and slot glossary-appendix-a
belong to the notebook unit; none touched. The abstract, `src/`, `derivation/` and the data are untouched.

## Counts by disposition (rows of the flag tables)

| slot | rows | applied | left (keep) | routed | not applied |
|---|---|---|---|---|---|
| example-01 | 63 | 52 | 3 | 6 | 2 |
| example-02 | 61 | 46 | 5 | 8 | 2 |
| glossary-01, Glossary-page rows | 24 | 10 | 6 | 1 | 7 |

## Routed (no change made), with owner

- example-01: table row 5 "15.2, WP22" (generated section table; owner the model file and the howto generator test); `PointingErrorRequirement` bound 0.008495 degree vs 0.0085 (a number; WP23 / the model file); launch slot "3.1 to 4.2 times at one satellite" (a number; WP23; `tests/test_paper.py` quotes the model part of this sentence); the "third part" of the coverage table (structure; WP23 / case page; the XDSM gloss and bibliography key left with it); "Appendix C.8 of the paper" against "of the supporting material" (a placement; the sentence naming the paper was cut as a duplicate of the later lower-bound bullet, the later name stands).
- example-02: generated cadCAD block lines (cadCAD terms, "where the mapping does not fit"; owner the docstring of `experiments/experiment.py`); the generated toolkit table rows (`verify_constraint`, engine `smt`, engine `tool:fmi`; owner the toolkit-table generator); the tolerance path `tests/test_v2_data.py` (a placement); "The draws are 20 of the variables the two variants share" (a claim about the run; owner to confirm); the four constants in the shared-subspace parenthesis (a number set; owner WP23/experiments).
- glossary-01: MoP's list of seven case metrics (placement; owner the case page / glossary owner). Nothing in `glossary.yaml` was changed that regenerates a notebook: only `short`, which compiles to the Glossary page alone.

## Not applied, with the reason

- example-01: "the ledger" at first use in the intro (a gloss adds words; the term is defined under Running an experiment); "texture", "K = 1", "exponent heatmap", "fit temperature" in the hypothesis (a gloss would add content; the record pointer and the non-goal pointer were cut).
- example-02: "the runtime"/"the toolkit"/"the pinned binary" naming (the page gives no name to use without new content); "bang-bang" and "necessary-condition result" (no plain word that keeps the claim).
- glossary-01: certificate (reordering "That ..." adds words), conditioning (the class name is the API link), contending set ("n-lemma"), geometric program and generalized geometric program (posynomial and monomial glossed only by pointing; adds words), participation threshold, conditioning of the exponents (a gloss adds words).

- example-02: the two test ids after the battery-range example were kept: `tests/test_case_model_howto.py::test_the_tests_the_howto_points_to_exist` requires the Z3 section to cite at least one test, and these back the two claims they follow. (Those two rows count as not applied; the other test ids on the page were cut.)

## Applied (summary)

Cuts: the announcing opening paragraph, the frozen file list, "swap gate", the line-pointer and generator sentences, "What to take from each section:", record, test and commit pointers in parentheses, the lines on removed metrics (eclipse reserve, slew time), "(below)" pointers, "the fit of record" and "data of record", the closing parentheticals of the recap, the repeated cadCAD sentence, the ledger-field list under Z3, and "An example from the tests:". Splits: the three-oracle definition, the Requirements bullet, the MoE/MoP rule, the assessment sentence, the battery peak power ratio, the unit and fleet cost lines, the thresholds paragraph, the coverage and coupling paragraphs, the supersede bullet, the toolkit paragraph, the exclusion paragraphs, the legacy oracle and shared-subspace sentences, the Run paragraph, and ten glossary `short` entries. Plain-word swaps: "model checking" to "the solver", "traded metrics" to "metrics" in the requirements bullet, "IMU masses" list to "part masses", "calcs" to "calculations", "LEO" to "low Earth orbit", "event detection" to "last exit from the band". Glosses (shortest): cadCAD, Z3, SysML, the controller gain Kp, the gain Kd.

## Claims register and ledgers

No claims-register row quotes the cut sentences (`claims_register.toml` has no case-model fragment); none re-pointed. No paper length-ledger row touched (no paper text changed). Test ids cut from the page remain in `tests/` and back their claims there.

## Checker, before and after (surfaces of this unit)

`scripts/check_residuals.py --compare scripts/residuals_baseline.json`: before, the case-model and glossary surfaces were at or below baseline in the flag-time report (`work-packages/WP38-flags/before-checker.txt`); after, no count of these surfaces rose above baseline. Words per surface, before to after:
case-model.md sections: 342 to 251, 497 to 428, 2235 to 1973, 463 to 444, 187 to 171, 728 to 695, 580 to 468, 213 to 202, 427 to 365; glossary/long-forms 2615 to 2595. Long sentences, parentheses, path parentheses and compound sentences fell in every case-model section (assembly: parens 63 to 44, path parens 23 to 13, compound 14 to 5). Acronyms undefined at first use in case-model.md: 16 to 11.

## Tests

`scripts/check_vocabulary.py` (0 new), `ruff check`, `tests/test_docs.py`, `tests/test_claims_register.py`, `tests/test_text_encoding.py`, `tests/test_case_model_howto.py`, `tests/test_build_generated.py`, `tests/test_vocabulary.py`.
