# Spike scope: one or two diagrams that summarize the SysML v2 model of the case

Scoped 2026-11-09 by the driver on the supervisor's direction (`work-packages/WP19-backlog.md`): "another
kind of figure we dont have but could have is 1 or max 2 plantuml figures for the sysmlv2 model to
summarize it. i did some research spikes previously on plotting tools in the toaster repo but they
are out of date, look at those spikes and scope a new spike." And: "the spike on plantuml plotting
can happen in parallel since it just determines what we can do, does not change the paper yet".

## What the earlier study found (toaster, 2026-09-29, read by the driver; pins now out of date)

`/Users/z/Documents/GitHub/toaster/decisions/diagram-study-real-fixtures.md`, its evidence folder,
`decisions/diagram-survey.md`, `diagram-tool-gaps.md`, `diagram-text-integration-survey.md`, and the
skill `.claude/skills/sysml-diagrams/` (SKILL.md, references/recipes.md).

- Three pipelines rendered real models: the OpenSysML runtime CLI to PlantUML, the same to
  DOT/Graphviz (`-render #kind:element -render-form puml|dot`), and sysml-toolkit to PlantUML. The
  OMG pilot and SysMLD failed on real content.
- Views exercised: tree (decomposition), interconnection, state, action flow. OpenSysML's
  interconnection view dropped port names and did not change when the model was mutated;
  sysml-toolkit's did.
- No tool exposed a requirement or allocation view; the in-house decomposition renderer handled
  part definitions and usages only (not requirements, constraints, calcs, analyses, satisfy).
- That project settled on DOT/Graphviz with in-house projections and a recipe per figure (question,
  selection, encoding, presentation, checks), and a mutation check: change one model element and
  see the picture change.
- Pins then: OpenSysML 0.9.0, sysml-toolkit af839f0d2. Now: opensysml 0.12.1 (this repository's
  lock), sysml-toolkit as pinned by this repository's experiment helper.

## The question

With today's pins and the tools already on this machine, which one or two diagrams, generated from
`examples/adcs/` model files and not drawn by hand, summarize the cubesat model for a reader of the
paper, and what does each show and not show?

## Candidate slots to try (the spike may propose others, two at most in the end)

1. **What a configuration is:** the cubesat's parts with their alternatives and the design
   variables (a definition or decomposition view).
2. **How a configuration becomes attributes:** the calculations, constraints, requirements and the
   analysis that turn a configuration into the ten attributes (the seam the method relies on).

## Method

- For each candidate and each pipeline that runs (OpenSysML to PlantUML, OpenSysML to DOT,
  sysml-toolkit to PlantUML; a small projection from a model query to PlantUML or DOT text if no
  built-in view covers calcs, constraints and requirements): the command, exit code, the generated
  text, the rendered SVG and a PNG at the paper's column width.
- Model-to-picture integrity: mutate one element in a copy of the model (in the spike's folder) and
  show the picture changes; check names in the generated text against the model.
- Legibility at the paper's column width and at 375 px; light and dark.
- Reproducibility: is the generated text stable run to run; what a test could pin (the text, not
  the SVG bytes); what CI would need. PlantUML, Java and Graphviz are system tools, not uv
  packages, so the likely shape is: the diagram text and the image are committed, and a test
  regenerates the text where the tools exist.
- For each surviving candidate, a recipe: question, selection, encoding, what it shows, what it does
  not show.

## Outputs (all under `docs/superpowers/notes/spike-sysml-diagrams/`)

`report.md` (the readout: a table of view by pipeline, the one or two recommended diagrams with
their recipes, limits, cost to adopt), the scripts, the generated `.puml` or `.dot` text, the SVG
and PNG files, the mutation evidence.

## Limits

Nothing is installed and nothing outside the repository and the scratchpad is changed. Tools already
present are used as they are (`plantuml`, `java`, `dot` are on this machine; the OpenSysML runtime
comes through the project's own environment; the sysml-toolkit binary through the project's
helper). No public PlantUML server or any other outside service. No Docker or Colima. The model,
the paper, the docs and the dependencies are not changed. The toaster repository is read only.
Time box: one session.
