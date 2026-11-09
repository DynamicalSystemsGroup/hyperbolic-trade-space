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
