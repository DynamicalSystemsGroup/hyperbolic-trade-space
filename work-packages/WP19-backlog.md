# WP19 (backlog) — Figures: selection, generation, narration, by section

Backlog entry typed by the driver, 2026-11-09. Not a scope: the scope is drafted when the package
reaches the front, with the diagram spike's readout as input.

## The supervisor's direction, verbatim

"similarly we need to describe the plots a bit more in prose: for each we need to be clear about what
they do and do not show us. this is also related to how/whether they earn their place in the paper.

another kind of figure we dont have but could have is 1 or max 2 plantuml figures for the sysmlv2
model to summarize it. i did some research spikes previously on plotting tools in the toaster repo
but they are out of date, look at those spikes and scope a new spike.

i think diagram selection and narration is its own workpackage with subpackages by section. don't
worry about finetuning prose until we've confirmed the figure slots and have generated and confirmed
the figures for those slots.

this package/subpackages goes in the backlog. i think the spike on plantuml plotting can happen in
parallel since it just determines what we can do, does not change the paper yet"

Earlier the same day, on the three-pane figure: "these images are helpful high level but i am worried
they may be out of place and distracting in the paper body. it may be best to keep this in the index
as a high level story arc / gloss." (That figure leaves the paper's body; ticket already with the PM.)

## Shape of the package (the driver's reading, for the scope to confirm)

One package, one subpackage per section of the paper that carries or could carry a figure. Three
stages, the first two closed by the supervisor because he judges figures by eye:

1. **Slots.** For every section: the figures it has, the figures it could have (including one or
   two diagrams of the SysML v2 model, and a ternary plot, where the spikes show they work), and for
   each a line on what it shows, what it does not show, and whether it earns its place. Output: a
   slot list. *Gate: the supervisor confirms the slots.*
2. **Figures.** Each confirmed slot's figure generated from data or model by committed code, at the
   paper's width, in the browser. *Gate: the supervisor confirms the figures.*
3. **Narration.** Only then the prose: for each figure, what it shows and what it does not, in the
   text beside it and in its caption; then the fine-tuning of the surrounding prose.

Until stage 2 closes, no caption or figure prose is polished anywhere in the paper.

## Inputs

- `docs/superpowers/notes/spike-sysml-diagrams/` (scope written; the spike runs in parallel now).
- `docs/superpowers/notes/spike-ternary/` (what the triangle shows; the cubesat by subsystem groups).
- The second review's finding that the three heatmaps of the case analysis are hard to read.
- The claims requirement: "what it shows and does not show" is a set of claims, each backed.

## Length (the supervisor, the same day)

"the total length of the paper is less hard ceiling and more regularization. each word earns his
place, and more text has a higher burden". So figure prose, like all prose, is admitted by the job it
does and recorded in the paper's length ledger, not blocked or licensed by a number.

## The diagram spike's readout (2026-11-09, `docs/superpowers/notes/spike-sysml-diagrams/report.md`)

Checked by the driver (both images looked at; the agent wrote only inside its folder).

- Two diagrams are candidates for slots, both written as PlantUML by one projection script that
  queries the loaded model (`project.py`); no built-in view of either tool gives them.
  1. *What a configuration is* (`out/slot1_configuration_700.png`): the cubesat, its parts, the wheel
     and tracker alternatives, the design variables and their ranges, all read from the model.
     Legible at the column width. The stronger candidate.
  2. *What the model computes from a configuration* (`out/slot2_attributes_700.png`): the
     calculations, the slew analysis, the requirements and their satisfy relations. A dependency
     overview, legible at the column width and busy. It does not show the attributes the simulation
     measures outside the model (settling time, slew time, control effort).
- The built-in views (the OpenSysML command-line renderer found on this machine, version 0.9; the
  toolkit's `viz`, version 0.12) run and are unreadable at the column width, or omit the
  alternatives, and have no view of requirements or calculations.
- Model-to-picture check: adding one alternative or changing one requirement changes exactly the
  expected lines; the generated text is identical over three runs; every name in it is in the model.
- Limits: white background only; not judged by a human yet; the projection uses an interface the
  model library marks experimental; the current runtime's own view interface (nodes and edges, not
  PlantUML) was not explored; PlantUML and Java are system tools, so adoption means committed text
  and image with a test on the text where the tools exist.

## Visual loops (the supervisor, 2026-11-09)

"make sure we also do visual loops for figures". Stage 2 of this package runs the figure review of
`docs/superpowers/notes/figure-review.md` on every candidate before it is put to him: a cold read of
the image alone, the sentence test, ink as data, legibility where it is read, what it shows and does
not show. A candidate that a sentence replaces is not put forward. The cubesat triangle of the docs
(three markers in an empty triangle) is the worked failure; by the same test the first diagram of
the model spike has content and the ternary plot of the cubesat by groups does not.

## The supervisor on the model diagrams (2026-11-09)

Shown both candidates of the diagram spike. **Verbatim:** "this one i better but also still feels like
it could benefit from some refinements on the line drawing. maybe a vertical rather than horizontal
view. broadly speaking i think showing all the parts and how they assemble makes sense since our
config is larger swapping parts (categorical) or tuning params of parts (continuous). our requirements
on the other hand land on behavioral subsystems which are a distinct view from the assembly."
Earlier, on how the judgement is made: "judgements on whether the visuals are fit for purpose is mine
even if i allow for tailoring/refinement in situ later by the visualization engineer agent".

Disposition: two views of the model, both his to judge from images, refined by a visualization
engineer agent in the spike folder before any slot is taken:

1. **The assembly view** (candidate 1, refined): every part and how they assemble; the categorical
   choices (swapping a part) and the continuous ones (tuning a part's parameters) marked as the two
   kinds of configuration variable, consistently; vertical (top-down) layout; the lines routed
   cleanly; the ranges kept.
2. **The behavioural view** (new; candidate 2 is withdrawn): the requirements and what they land on,
   the behavioural subsystems (power, mass, attitude control), as a view distinct from the assembly;
   drawn from the model's requirement and satisfy elements and the analysis, not from the
   calculation dependency graph.

**Supervisor, verbatim, the same hour:** "i am also interested in a second plot that is focused on
functional subsystems, requirements and how the metrics we're actually trading relate to those
requirements". The behavioural view becomes this: the functional subsystems (power, mass, attitude
control, as the case already groups them), the requirements, and the ten metrics of the trade, with
the relation of each metric to a requirement shown, so that a reader sees which traded metrics a
requirement constrains and which are traded with no requirement on them.

