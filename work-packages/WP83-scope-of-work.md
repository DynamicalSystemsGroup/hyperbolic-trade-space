# WP83 — Scope of work: the demo notebook for the OpenMBEE presentation (2026-11-20)

| | |
|---|---|
| **Status** | Approved: "Approve, build tonight" (the supervisor, 2026-11-19, about 12:20 EST), quoted in `WP83-decisions.md` |
| **Supervisor (accountable)** | mzargham |
| **Branch** | `talk/openmbee-2026-11-20` off `dev`, pushed; it does not merge into `dev` (his word: "stays its own branch for now. i can reassess later") |
| **Acceptance record** | his word after he has run and read the notebook, quoted in `WP83-decisions.md` |

## Purpose

A Jupyter notebook he presents tomorrow (2026-11-20) at OpenMBEE: a narrated walk from motivation to the fitted
trade space of the cubesat ADCS case and the decisions it supports, ending on closed-loop design-space search. His
words: "i view this as curation and narration, not new build"; "the paper's case and case analysis likely provides a
lot of the scaffolding you need for this presentation"; "i don't want extra requirements for merging to dev getting
in the way of getting my notebook ready for the presentation".

## Goals (his arc, in order)

- G1. **Motivation**: the decision problem (an answer and a justification; trade studies decided from documents),
  from the paper's "The decision problem" (`paper/paper.ipynb`, cell `sect-problem`) and the root page's lead.
- G2. **Three layers**: decision analysis, machine learning, optimization, shown with the paper's figure
  `paper/figures/fig-prior-art-layers.svg` and the paper's Discussion paragraph "The three layers".
- G3. **The pipeline diagram**: `paper/figures/fig-pipeline.svg` (evaluate -> condition -> identify -> analyse; c, a,
  m, w and beta on the arrows).
- G4. **The SysML v2 model** of the ADCS example: what `examples/adcs/model_v2/cubesat.sysml` holds (sections), shown
  as text excerpts.
- G5. **The configuration diagram**: the assembly view `examples/adcs/model_v2/views/assembly_view.png` with its
  caption (`assembly_caption.md`).
- G6. **The subsystems and requirements diagram**: the behavioural view `examples/adcs/model_v2/views/behavioural_view.png`
  with its caption.
- G7. **The simulations, described, not re-run**: what the oracle evaluates (one 30-degree slew under a saturating PD
  law, the SysML calculations, the four feasibility flags; `examples/adcs/case-model.md`), and the data of record
  loaded from `examples/adcs/data/v2/` through `case.load_study` (3,000 designs per regime; 2,134 feasible in the
  primary regime); the ledger named as the record of the runs.
- G8. **The fit with tradespace**: conditioning and the fit through the case module (`case.fit_study`, `case.k_fits`,
  `select_temperature`), with the temperature sweep and the trade-off report.
- G9. **Exploratory analysis aligned to assessing alternatives and justifying decisions**: the paper's case sequence,
  each step ending on what it means for choosing among alternatives: feasibility and the requirements; the
  contending set and the tension matrix; the ternary views of where each term leads; the fleet-size trade; the
  requirements read after the fit; propose, predict, check; the decision (the shortlist of 28, the stakeholders'
  picks, what remains for the executives; `paper/generate_findings.py` `decision`).
- G10. **Closing: closed-loop design-space search**: the fitted invariant V as an energy-like function (Pareto
  improvements raise it; a maximizer of V is weakly Pareto-efficient, theorem L11), the regressor from configuration
  to metrics as the surrogate that makes it a function of the design, and the outer loop (propose, evaluate, refit)
  from `docs/bridge.md` and the paper's Future work, said as direction, not as shipped capability.

## Non-goals

No new simulation, dataset, analysis function or figure generator; no change under `src/`, `examples/adcs/`,
`docs/`, `paper/`, `site/` or the tests; no merge into `dev` and no requirement that exists only for one (the docs
site, the claims register, the residual and vocabulary gates); no re-rendering of SysML views (the committed images
are used; superseded by Amendment 1); no statement of a capability the package does not ship.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The notebook, executed, outputs committed, at the default path below | G1-G10 |
| D-2 | `WP83-scope-of-work.md`, `WP83-decisions.md` (his words verbatim) and a short review record with screenshots, on the branch | the gates |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Runs top to bottom in a clean kernel with the locked environment, no simulation | `uv run jupyter nbconvert --to notebook --execute --inplace <path>` exits 0, with `MPLCONFIGDIR` set to a scratch folder; no network |
| R-2 | No error, warning or stderr in any committed output | read the outputs (a script greps the notebook JSON for `"name": "stderr"` and error outputs) |
| R-3 | The arc's ten sections appear in his order, each with its heading | read the rendered notebook |
| R-4 | Every number shown is the case's own (e.g. 3,000 designs, 2,134 feasible, the shortlist of 28) | compare with the paper's committed outputs |
| R-5 | Each analysis step states what it means for choosing among the alternatives | read |
| R-6 | No change outside the notebook and its records | `git diff --stat origin/dev...HEAD` lists only them |

## Definition of good

He presents from it without editing it: every section reads aloud in one or two sentences, each figure says what its
caption says, and the analysis builds to a decision an audience can follow and question.

## Definition of good enough

R-1 to R-6 met, a fresh-context reviewer has run it and looked at it rendered (screenshots in the record), and he has
read it once and his edits are small.

## Definition of done

Good enough met; his word recorded.

## Open decisions

None. The branch is pushed (his answer "Pushed, rule widened": the governance pull request's Branches rule admits `talk/*` branches, in its amendment 4).

## Agent's defaults

- Path `talks/2026-11-20-openmbee/demo.ipynb`; branch `talk/openmbee-2026-11-20`.
- The triad is the paper's (decision analysis, machine learning, optimization), not the glossary's decision / design /
  method nesting.
- Setup as in the paper: one setup cell importing `paper_paths` and `case`; then short cells, mostly one call each;
  narration in Markdown cells in the glossary's words; figures from the case module's figure functions or the
  committed images. The two SysML views are drawn from the model in the notebook (Amendment 1).
- The primary regime only; the stock regime mentioned in one sentence.
- Build: the PM starts one worker for the notebook and one fresh-context reviewer who runs it and looks at it
  rendered; the driver verifies and hands it to him tonight.

## Amendment 1 (2026-11-19, about 17:20 EST): the SysML views drawn from the model

His word, quoted in `WP83-decisions.md`: the two views are drawn in the notebook by the code that made the committed
images, not displayed from those images. What changes:

- The non-goal "no re-rendering of SysML views" is superseded. The notebook imports the views generator
  (`scripts/sysml_project.py`), loads the model, projects it to PlantUML text, and draws that text with PlantUML. The
  generator, the model and the committed views are unchanged; the generator's text equals the committed `.puml`
  files (`tests/test_system_model_v2_r1.py`, the committed-views test).
- R-1 gains a precondition: PlantUML on the `PATH` (`plantuml`, as `scripts/sysml_render.sh` uses it) and Java.
- The assembly view's level lines come from the generator's caption list, not from `assembly_caption.md`.
