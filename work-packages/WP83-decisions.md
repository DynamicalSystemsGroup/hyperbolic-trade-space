# WP83 decisions (the demo notebook for the OpenMBEE presentation, 2026-11-20)

His words, verbatim, 2026-11-19 (EST, about), in the order given:

- (about 12:00) "i also need a separate scope of work which will go on its own branch. this scope is a jupyter notebook for a presentation // demo. the story arc of the demo is as follows:" followed by his ten items: "motivation"; "3 layers: decision analysis, ML, optimization"; "the pipeline diagram"; "the sysml v2 model (use the ADCS example)"; "show the configuration diagram"; "show the subsystems / requirements diagram"; "describe the simulations but pull the data from already run simulations don't rerun then"; "run the pipeline fit using tradespace"; "then do some exploratory data analysis"; "make sure the exploratory data analysis is clearly aligned to assessing alternative and justifying decisions"; "end on the relationship of this package to closed loop design space searching (comment on the role of a surrogate function that is energy-like for searching and optimizing over the design space."
- Asked "Is the demo notebook for tomorrow's OpenMBEE presentation?": "Yes, for tomorrow".
- "a lot of what you need already exists. i view this as curation and narration, not new build"
- Asked "After tomorrow, what happens to the demo notebook's branch?": "stays its own branch for now. i can reassess later. i don't want extra requirements for merging to dev getting in the way of getting my notebook ready for the presentation"
- "the paper's case and case analysis likely provides a lot of the scaffolding you need for this presentation"
- Asked whether the branch goes up to GitHub, given the governance pull request's branch rule: "Pushed, rule widened" (the rule's `talk/*` class rides in WP82 amendment 4, #16).
- Asked to approve the scope with its defaults to start the build: first "Show me the scope first", then, having read it: "Approve, build tonight".

**Applied as.** The scope `WP83-scope-of-work.md` approved as drafted, its Agent's defaults included; the build runs
tonight through the PM (one worker, one fresh-context reviewer); the driver verifies and pushes the branch
`talk/openmbee-2026-11-20` once.

## Amendment 1: the SysML views drawn from the model (2026-11-19)

His words, verbatim, about 17:10 EST, with screenshots of the assembly and behavioural view cells: "i thought these
figures were created from code. can we use the code rather than a display command."

**Applied as.** Amendment 1 of `WP83-scope-of-work.md`: the notebook loads the model with the views generator, draws
the assembly and behavioural views with PlantUML from the generator's text, and prints the level lines from the
generator's caption list; the battery range's `W*h` is escaped so Markdown does not italicize it. Executed in a clean
kernel (exit 0, no stderr output); the generated text equals the committed views' text.

## Amendment 2: helpers in a support module, process language out (2026-11-19)

His words, verbatim, about 17:22 EST, with a screenshot of the setup cell's `say`, `excerpt` and `draw` functions:
"these seem like they belong in a supporting utilities file. feels weird to have them in the notebook. there is also a
lot of prompt leakage / metanarration in the notebook that needs clean up"

**Applied as.** Amendment 2 of `WP83-scope-of-work.md`: the helpers, the path setup and the constants move to
`talks/2026-11-20-openmbee/demo_support.py` (the setup cell keeps imports and display settings); Markdown, comments and
emitted text lose the process language, with the filtering of generated sentences and model excerpts done in the
support module; the notebook is executed in a clean kernel and read cold in a browser by a fresh-context reviewer.

His words, verbatim, about 17:40 EST, with a screenshot of section 9.4: "also the roll up to the vantage point of the fleet is a bit undernarrated. we don't need to over do it, we can simply say if we economic objectives from stakeholders that are computable from the available model or a budgeting forecaste model then we can look at the same system from the perspective of principals who have to make a financial decision while still keeping it routed in the tradespace model and data we fit on."

**Applied as.** Section 9.4 opens with the roll-up: stakeholders' economic objectives computed from the model or a forecast model let the same system be read from the principals' vantage point, grounded in the same model and data; the fleet cost, unit cost and coverage probability are named, and the figure's corners are the sponsor, the manufacturer and the operator.

## Amendment 3: the closed-loop figure (2026-11-19)

His words, verbatim, in the order given (EST, about):

- (17:30) "also think we should make a modified version of the pipeline diagram with extra blocks to \"close the loop\" including our regressor / search optimization. give me candidates to review. the point is to motivate / explain how the design space exploration and optimization loop looks as a block diagram in the same level of depth as the first pipeline but now its a feedback loop because the output of the regressor allows us to define a new configuration, measure it and loop again"
- (17:42, on candidate C) "i think we need c' to wire into the same port as c. also w,b is the same wire so split the wire. you need to follow block diagram visual sematics"
- (17:43, on candidate A) "maybe work from this one as its a simpler representaation. more intuitive"
- (17:45, after seeing the revised A) "show it to me", then "yes add it"

**Applied as.** Amendment 3 of `WP83-scope-of-work.md`: three candidates drawn (A, energy search; B, the analyst's
target; C, both), C revised to his wiring rules, then A revised the same way and chosen. The figure is drawn by
`loop_figure` in the support module; its output equals the drawing he approved. Section 10 shows it, followed by one
paragraph on the loop.

His words, about 17:52 EST: "i am not sure we're using the term surrogate correctly and i am concerned its confusing
jargon and we should just use plan language". **Applied as.** The use was the optimization sense (a cheap model
standing in for the expensive evaluation), but the word is not in the glossary and does no work for the audience:
"surrogate" is replaced by what the regressor does (it predicts a configuration's chart point and level; V̂ is the
predicted value of V) in sections 9.6 and 10, the code comment and the figure.

## Amendment 4: the mathematics in brief (2026-11-19)

His words, verbatim, about 17:55 EST, with a screenshot of section 3 (the pipeline): "after the pipeline before the sysmlv2 model i think we should do the mathematics in brief. similar to whats going in the documentation not whats in the full paper"

And about 17:52 EST, on the word surrogate: "i am not sure we're using the term surrogate correctly and i am concerned its confusing jargon and we should just use plan language"

**Applied as.** Amendment 4 of `WP83-scope-of-work.md`: the new section 4 is written from `docs/theory.md` in plain words (its
paper links and theorem numbers dropped); the later sections are renumbered. Executed in a clean kernel (exit 0, no
stderr output); read cold in a browser by a fresh-context reviewer, screenshots in `WP83-rounds/amendment-4/`.

## Amendment 5: the cold-reader register's edits (2026-11-19)

His words, verbatim, about 18:22 EST: "All edits, decide D". The register and answer key are copied to
`WP83-rounds/round-3-readers/`.

**Applied as.** E1 to E13 as listed in Amendment 5 of the scope (E3 with D2). Each is a phrase, a sentence or a deletion;
the generated-sentence edits (E5, E6) are filters in `demo_support.py`, nothing in `src/`, `examples/`, `paper/`.

His answers to the five open decisions, quoted:

- D1, the word "energy" (eight readers found "energy level" and "energy differential" unmotivated; one noted the clash with
  the energy-balance metric): "Level on page, energy in §11". **Applied as:** "level" (log V) in sections 4 to 10, in
  prose, the decision table header and generated sentences (filtered in `say`); section 11 keeps "energy-like".
- D2, the "between sponsor and operator" row: "Keep it, label it". **Applied as:** one clause in the note after the
  decision table says the row is one more rule, the analyst's, not the fit's answer.
- D3, showing the estimator: "Add one short cell". **Applied as:** a two-line cell after the fit prints the estimator and
  calls `score_samples` on four rows of the conditioned metrics.
- D4, the generated-sentence cells: "Import once in setup". **Applied as:** one `from generate_findings import (...)` in the
  setup cell; each later cell is its `say(...)` call.
- D5, the question up front: "Add one line". **Applied as:** one line in the title cell names the decision: which cubesat
  fleet to build and how to defend the choice to the executives.

His words, verbatim, about 18:35 EST, with a screenshot of the section 10.6 predict/check figure: "this figure needs a legend"

**Applied as.** The support module's `predict_check_figure` adds one legend below the figure, built from proxy handles
read from the figure's own marks (a design; a design near the fitted reference surface; a proposal where the regressor
predicted it; the same proposal where it was measured; the number beside them), and the sentence before the figure that
described the marks is cut.

His words, verbatim, about 18:40 to 18:45 EST, in order:

- "also we show sweeping temperature but we don't show anything about sweeping K"
- "we should also have a least a brief block about preprocessing or conditioning our data to conform to the assumptions of the tool"
- "change the notebook title to"Tradeoff analysis with tradespace and sysml v2""

**Applied as.** K-1: after the temperature sweep a table of the mean slack at the one-term temperature for K = 1, 2, 3, its
drop per added term and the thinnest term's share at each fit's own temperature (`choosing_k_table` in the support
module; it leaves out the case's movement-under-resampling column, which takes over three minutes), with a sentence that K is the analyst's
choice. C-1: the opening of section 9 states what the tool takes and what conditioning does to meet it. T-1: the title is
"Tradeoff analysis with `tradespace` and SysML v2" (capitalisation and code font smoothed); the question stays under it.

His words, about 19:00 EST, on the setup cell's import list (D4 applied as one parenthesised import of thirteen names):
"jut import * from generate findings its too verbose". **Applied as.** The setup cell imports the findings module's
names with one star import (`from generate_findings import *`); its names overlap the notebook's only in `case` and
`pd`, the same modules.

His words, about 19:02 EST: "drop "described and not re-run" its metanarration. it doesn't really matter, i could rerun
them but i just want the talk to wait for that". **Applied as.** The section 8 heading is "8. The simulations" (his arc's
item "describe the simulations but pull the data from already run simulations" is kept in the content, not the
heading); the opening's "No simulation is run;" goes for the same reason, leaving "The fits and figures are computed
from the data."

His words, about 20:10 EST: "i need my notebook presentation to have a step where i click out of the notebook into the
view editor briefly"; and, told that the editor times out on the model (twice, "Engine operation timed out after 60
seconds", on the three model files as written, 104,785 characters), about 20:18 EST: "can you open a subset of the
model?". **Applied as.** The subset is the whole model with its prose trimmed: each documentation comment cut to its
first sentence and the other comments removed (58,023 characters, 12,805 elements, the same count as the full text in the
repository's toolkit). The editor applies it in under 20 s with no issues; its requirements table holds all 13
requirements and its traceability matrix shows the satisfy and not-satisfy declarations by configuration. A Markdown cell
at the end of section 7 links the model to the OpenMBEE View Editor (https://openmbee-view-editor.vercel.app/app, Rohan
Mehta's editor, its address since 2026-11-10 per the team's Slack); the next cell calls `editor_model()` in the support
module, which writes that text as `cubesat-view-editor.sysml` beside the notebook (committed; the run rewrites it
unchanged), for the editor's "Open files or project". The editor keeps a project in the presenting browser's local
recovery, so the file is opened there before the talk.
