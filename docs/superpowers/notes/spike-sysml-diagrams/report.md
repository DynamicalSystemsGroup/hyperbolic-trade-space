# Spike report: SysML v2 diagrams for the paper

Run 2026-11-09 on branch dev. Model: `examples/adcs/model_v2/cubesat.sysml`, copied unchanged to
`model/cubesat.sysml` (all runs use the copy). Nothing in the paper, model, docs or dependencies was
changed; nothing was installed.

## Verdict

Two diagrams are worth a slot, and both come from one small projection script, not from a built-in view:

1. **Configuration** (slot 1): `out/slot1_configuration.puml`. Legible at 700 px; marginal at 375 px.
2. **Configuration to attributes** (slot 2): `out/slot2_attributes.puml`. Legible at 700 px only as a
   structural overview (labels are small); not legible at 375 px.

No built-in pipeline gives either. The OpenSysML runtime and sysml-toolkit both run and exit 0, but
their package-level views are unusable at column width and neither draws requirements, calcs or the
analysis as a dependency picture. Slot 1 is the stronger candidate. Slot 2 is honest but busy (27
boxes); if the paper has room for one figure only, take slot 1.

## Tools as found

- `plantuml` 1.2026.8 and `dot` 16.0.0 (system). PlantUML ran with `-Djava.awt.headless=true`, `-tsvg` and `-tpng`.
- opensysml Python 0.12.1; its runtime is `~/.opensysml/bin/sysml-grpc` v0.12.1. That binary is a gRPC
  server, not a CLI with `-render`. The `-render` CLI at `~/.opensysml/bin/sysml` is **v0.9.0**
  (dated Sep 24, left from the earlier study, not what opensysml 0.12.1 provisions). The runs
  below labelled "osml 0.9 CLI" used it, so they are not a statement about 0.12.1. The 0.12.1 route
  is `Model.render_view(...)`, which returns typed nodes and edges (`RenderedView`), not PlantUML text;
  it ran but I did not write a PlantUML writer for it.
- sysml-toolkit `sysmlv2` 0.12.0 with `viz` (PlantUML only), found with the experiments helper; run with
  `SYSMLV2_LIB_DIR` set to its stdlib.

## View by pipeline

All commands ran from this folder against `model/cubesat.sysml`. Outputs are in `out/` (`.puml`/`.dot`,
`.svg`, `.png`, `_700.png`, `_375.png`; PNGs are resampled with `sips`).

| View | Pipeline and command | Exit | Shows | Omits / problem | Mutation | Stable |
|---|---|---|---|---|---|---|
| Tree, `Cubesat` | osml 0.9 CLI: `sysml model/cubesat.sysml -render "#tree:CubesatTradeSpaceV2::Cubesat" -render-form plantuml -o out/osml09-tree-Cubesat.puml` | 0 | Cubesat members as a flat list of boxes | no alternatives, no values, 3829 px wide x 271 px: unreadable at column width | adding an alternative changes the package tree; not the Cubesat root | yes |
| Tree, package | same with `#tree:CubesatTradeSpaceV2`, plantuml and dot | 0 | every definition and doc as notes | 645 to 682 lines; doc notes dominate; unreadable | rename shows; the requirement edit produced no change | yes |
| Interconnection | same with `#interconnection:...::Cubesat` (puml, dot) | 0 | member boxes in a row | no connectors in this model; 9981 px wide, unreadable; package root: "renders empty" (exit 0, note on stderr) | not tried | not tried |
| Tree, `Cubesat` | toolkit: `sysmlv2 viz model/cubesat.sysml --view tree --element CubesatTradeSpaceV2::Cubesat -o out/tk-tree-Cubesat.puml` | 0 | Cubesat with variables and values, parts with types and spans, composition arrows | no alternatives (they sit outside Cubesat), no enums, no ranges; calculated attributes listed without their calc | not run | yes |
| Tree, package | toolkit `--view tree` (and `--view mixed`) | 0 | all definitions including calc, requirement, analysis defs, with bodies | 533 and 492 lines; PNG hit PlantUML's 4096 px cap; doc notes dominate; unreadable | alternative added: node renamed and its attributes show; requirement edit appears as changed body text, not as an edge | yes (Cubesat root) |
| Interconnection | toolkit `--view interconnection --element ...::Cubesat` and `::cubesatBaseline` | 0 | 6 to 19 lines; a few boxes | the model has no connectors; nothing informative | not run | not run |
| Action | toolkit `--view action` | 0 | 2 lines, empty | the model has no actions | n/a | n/a |
| Case | toolkit `--view case` | 0 | the two verification defs and the analysis def, each with its subject and objective as bare boxes | no link to calcs or requirements; the only built-in glimpse of the analysis | not run | not run |
| Configuration (slot 1) | `uv run python project.py model/cubesat.sysml out` | 0 | see recipe | see recipe | passes | yes |
| Attributes (slot 2) | same script | 0 | see recipe | see recipe | passes | yes |
| Requirement, allocation, calc dependency views | none in any pipeline: the 0.9 CLI documents no such kind, `viz --view` lists tree, interconnection, state, action, sequence, case, mixed | | | | | |

Mutation evidence (diffs in `evidence/`):

- `model/mut1_added_alternative.sysml` adds `part def XLWheel :> ReactionWheel`. Slot 1 text gains
  `class "XLWheel"` and `ReactionWheel <|-- XLWheel` and nothing else (`evidence/mut1_slot1.diff`);
  slot 2 is byte-identical, as it should be.
- `model/mut2_requirement_calls_calc.sysml` changes `PowerRequirement` to `GeneratedPower(c) > 0.0 [W]`.
  Slot 2 gains exactly `PowerRequirement --> GeneratedPower` (`evidence/mut2_slot2.diff`). The toolkit
  tree shows only a changed text body; the 0.9 CLI tree does not change at all.
- Name check: every identifier in both generated texts occurs in the model source (script in session; 24 and 27 names, none missing).
- Stability: the projection script run three times gives identical text for both files
  (`evidence/stability_run2`); the toolkit and 0.9 CLI Cubesat trees are identical on a second run.

## Recipe 1: configuration (slot 1)

- **Question:** what is a configuration of the cubesat: what is chosen and from what.
- **Subject and selection:** package `CubesatTradeSpaceV2`, part def `Cubesat`. Included: its part
  usages with their types; abstract part defs and their concrete alternatives (by specialization); the
  enum def that selects each alternative (literals listed); attributes stated with `default`
  (the design variables: `panelSpan`, `batteryCapacity`, `Kp`, `Kd`); numeric ranges read with
  `Model.eval` from `designRanges`, `baselineGains`, `aggressiveGains`. Excluded: calculated attributes,
  environment, scenario, calcs, requirements.
- **Encoding:** filled box is the part def under consideration; composition diamond with the usage
  name; hollow triangle is specialization (an alternative); notes give the selecting enumeration and
  the ranges. The word "(variable)" marks defaulted attributes.
- **Shows:** the two categorical variables as the abstract wheel and tracker with three alternatives each;
  the four continuous variables with ranges; the fixed parts.
- **Does not show:** the attribute tables of each alternative (mass, torque, momentum, accuracy, power);
  which composed parts are fixed versus chosen other than by the absence of alternatives (the
  note and "(variable)" tags carry it); the environment; the formulas.
- **Files:** `out/slot1_configuration.puml`, `.svg`, `.png`, `_700.png`, `_375.png`.
  At 700 px all text reads. At 375 px the labels are readable but small, the stereotypes are not.
- **Known wrinkle:** `panelSpan` and `batteryCapacity` appear on `Cubesat` and again as the redefined
  `span` and `capacity` on `SolarPanel` and `Battery` (marked "(variable)" there, because they are `default` in the part def).
  The `(variable)` on those two is a consequence of the rule, not a statement that panels carry their own variable; a caption or a selection rule (variables of the root only) would settle it.

## Recipe 2: configuration to attributes (slot 2)

- **Question:** which calculations take a configuration to the attributes, and which requirements the same configuration is held to.
- **Selection:** calc defs, requirement defs, analysis defs and verification defs directly under the
  package, with `Cubesat`; edges from invocations found in the model JSON (`to_api_json`), taking the
  nearest top-level container as the caller. Pruned to what is reachable from `Cubesat`, the analysis
  and the requirement defs (this drops the closed-form slew-time calcs and the two verification
  defs, which nothing reaches). Constraint defs are omitted (parameter): they restate the accounting for the solver.
- **Encoding:** blue box the configuration type, green box the analysis `SlewExperiment`, orange boxes
  requirement defs, white boxes calc defs; solid arrow is "invokes"; dashed arrow `<<satisfy>>` goes to
  the named configuration the model asserts it for.
- **Shows:** the seam: the analysis's eight returned calculations, the shared sub-calcs (generation,
  eclipse demand, inertia), the accounting calcs the configuration evaluates itself, and which requirement reads which calc.
- **Does not show:** that two of the ten attributes (settling time and slew time, with control effort)
  are measured from the simulation and enter as inputs; which edge is which of the ten attributes (the
  analysis edges carry no label; the ten are not nodes); the constants and formulas; input and output
  types; the Python simulator outside the model; that four of the five requirements take measured
  inputs. The requirements appear nearly disconnected from the calcs because they read measured inputs.
- **Files:** `out/slot2_attributes.puml`, `.svg`, `.png`, `_700.png`, `_375.png`. At 700 px the box
  labels read but the stereotypes are tiny; at 375 px nothing reads. It wants a full-width or landscape slot.
- **Honest caveat:** this is a dependency overview, not a data flow of the ten attributes. Calling
  it the "analysis" figure would overstate it.

## Limits

- The projection depends on `to_api_json` (marked experimental by opensysml, an `ExperimentalFeatureWarning`) and on element-id spelling (`::` in queries, `__` in JSON); a runtime upgrade can break it, which a pinned test would reveal.
- Light and dark were not rendered: PlantUML output has a white background by default; a dark-theme variant was not tried.
- Reading the PNGs was done by me at the stated widths; a human judgment of legibility is still due.
- I did not write a PlantUML writer for the 0.12.1 `render_view` typed output, and I did not run the toolkit with `--show-inherited` or `--color`, which might make the toolkit's Cubesat tree show more.
- `sysml-toolkit` 0.12.0 `viz` accepts `--view` of seven kinds; the model has no state, action, sequence or connector content, so those views were not meaningful tests.
- 375 px PNGs are resampled from the full render, not drawn at that size.

## Cost to adopt

- One script (`project.py`, about 200 lines; presentation settings are constants at its top), run with `uv run python`. It uses only opensysml, which is already locked.
- Committed: the generated `.puml` text and an SVG (or PNG) for the paper; the model is the source, the text is a build product.
- A test could pin the generated PlantUML text byte-for-byte (stable across three runs here) and could assert
  that every node name occurs in the model and that specific edges exist (e.g. `PowerRequirement --> ...`).
  Such a test needs the opensysml runtime (downloaded to `~/.opensysml` on first connect) but not PlantUML or Java.
- Rendering to SVG needs `plantuml` and Java (system tools, not uv packages). CI would either skip
  the render and compare text only, or install them in the workflow; the committed image is the one the paper uses.
- A model change in `model_v2/cubesat.sysml` means regenerating and recommitting the pair; the text diff shows what changed.

## Files

`SCOPE.md`; `project.py`; `render.sh`; `model/` (copy plus two mutations); `out/` (all pipeline outputs and logs); `evidence/` (mutation diffs, mutated renders, stability run).
