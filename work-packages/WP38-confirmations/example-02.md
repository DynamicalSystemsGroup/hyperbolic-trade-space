# WP38 confirmation forms, slot example-02

Rendered view note: the docs site at http://127.0.0.1:8791/docs/ does not serve the case model page
(`/docs/examples/adcs/case-model/` returns 404; the examples page only links to the GitHub tree), so each
surface was read as file text of `examples/adcs/case-model.md` at head 4bcbf9a, the view the inventory allows
("or the file on GitHub"). The ten kinds were applied to each section after one reading-pace pass. The lost-fact
check found no gap, undefined first use or dangling reference that came from a cut, except where listed under
kind 10.

| Surface | Reader | Rendered view and head | Reads clean | Remaining flags (kind, sentence) | Cuts that lost something |
|---|---|---|---|---|---|
| `examples/adcs/case-model.md/running-an-experiment-and-reading-the-ledger` | example-02 | file text of the case model page (docs page not served), head 4bcbf9a | no | 1 flag. Kind 4 (repository path in parentheses in reader-facing prose): "An experiment is a declared object (`experiments/experiment.py`); the declarations of the v2 generation are in `experiments/definitions.py`." | none |
| `examples/adcs/case-model.md/the-cadcad-like-mapping` | example-02 | file text of the case model page (docs page not served), head 4bcbf9a | yes | none | none |
| `examples/adcs/case-model.md/the-toolkit-account` | example-02 | file text of the case model page (docs page not served), head 4bcbf9a | no | 4 flags.<br>Kind 10 (a): "The model uses the runtime's checking and simulation machinery where it supports them, and Python holds only what the model language cannot do." ("the runtime" and "the toolkit" are never named or defined in the document; first use of "runtime" is in the ledger-entry table, `versions` row.)<br>Kind 9 (and unclear reference): "The client's own documents are `docs/clients/python/verification.md`, which is not a path in this repository, and its README, "The service"." ("its README" has no clear antecedent; the sentence interrupts itself.)<br>Kind 10 (b): "joint satisfiability of the model's asserted constraints with a gating exit code; the runtime's `solve` engine gives the three-way answer for claims, so the CLI is the CI gate and not the claim checker" (CLI and CI never expanded in the document.)<br>Kind 10 (b): "not ready here (the runner variable is unset) and outside the scope" and "it answers over schedules and answers no constraint claim here" (FMI and SMT, the engine names `tool:fmi` and `smt`, are never expanded or glossed.) | none |
| `examples/adcs/case-model.md/z3-excludes-infeasible-configurations-before-sim` | example-02 | file text of the case model page (docs page not served), head 4bcbf9a | no | 6 flags.<br>Kind 4: "The recipe, run by `tests/test_case_model_howto.py` (`ADCS` is `examples/adcs`):"<br>Kind 4: "Every one has `dod_ok` false (`tests/test_cubesat_oracle.py::test_flags_observe_the_excluded_battery_region`)."<br>Kind 4: "and every sampled design has `dod_ok` true (`tests/test_cubesat_oracle.py::test_flags_observe_the_all_feasible_battery_region`)."<br>Kind 7: "When the whole variant is proved infeasible, `build` raises before anything is simulated, and the runner first appends an `exclusion` entry." (the earlier paragraph already says `build` raises `ExcludedVariant` and nothing is simulated; likewise "When the exclusion block in `inputs["exclusion"]` has a region classified `excluded`" repeats "stores the block in the experiment's `inputs["exclusion"]`" two sentences before.)<br>Kind 9: "The closed-form bang-bang peak momentum is an approximation that the integrated slew overshoots, so an excluded wheel region is a necessary-condition result that the simulation confirms, and "all feasible" there means feasible by the closed form."<br>Kind 10 (a): "bang-bang" in the same sentence is used without definition at first use in the document. | none |
| `examples/adcs/case-model.md/the-legacy-geostationary-oracle-and-the-scope-se` | example-02 | file text of the case model page (docs page not served), head 4bcbf9a | no | 1 flag. Kind 2 (a parenthetical that carries a second thought, 10 words): "`legacy_oracle.py` puts `design_space.evaluate_design` behind the same `Oracle` protocol (`LegacyGeostationaryOracle`, evidence `simulation`, the frozen keys and column order), with no edit to the frozen modules and no need for `opensysml`." (quoted from "`experiments/legacy_oracle.py` puts ...", same sentence.) | none |
| `examples/adcs/case-model.md/provide-the-oracle-three-small-cases-through-the` | example-02 | file text of the case model page (docs page not served), head 4bcbf9a | yes | none | none |

## Heads

- running-an-experiment-and-reading-the-ledger: no, 1 flag
- the-cadcad-like-mapping: yes, 0 flags
- the-toolkit-account: no, 4 flags
- z3-excludes-infeasible-configurations-before-sim: no, 6 flags
- the-legacy-geostationary-oracle-and-the-scope-se: no, 1 flag
- provide-the-oracle-three-small-cases-through-the: yes, 0 flags
