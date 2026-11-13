# Feedback on the OpenMBEE View Editor from one modelling session

Screenshots for this record: commit `2a669de`, `git show 2a669de:<path>` with `<path>` under `work-packages/WP26-view-editor-feedback/`.

Date: 2026-11-10. Editor: https://openmbee-view-editor.vercel.app/app (build as served on that date), used in a browser pane at
roughly 800 px width and, where stated, a 1600 x 1000 viewport. No account, no sign-in.

## Context

The session loaded a CubeSat attitude-control SysML v2 model of about 52,000 characters (51,612 characters; 29 calculation
definitions, 12 requirement definitions with 11 usages, 2 verification case definitions, 1 analysis case definition, 3
named configurations) together with a file of seven `view` usages, and used the editor's issues panel, diagram views,
requirements table and traceability matrix to read the model back. The text was set in the source pane through the page
(not typed), applied with "Apply source", and each result was read from the screen and from the page text. 22 steps were
logged, each with a screenshot; the screenshots cited below are copied beside this report. We came to the editor wanting
a connected view of how the design choices, the evaluated quantities and the requirements relate, and several things
about it served that well. Thank you for building it.

**How to reproduce.** Every bug below starts from the same recipe, called the loading recipe: (1) open `/app`; (2) if the
landing page offers "Restore recovery", either restore it or choose New project; (3) replace the whole text of the
source pane with the model text (select all and paste; or set it through the page's CodeMirror view: `document.querySelector(".cm-content").cmTile.view.dispatch({changes:{from:0,to:view.state.doc.length,insert:text}})`
-- an internal of the build we observed, not a published interface); (4) click "Apply source"; (5) wait about 3 s after
each click before reading. The model is not public as a single snippet; where a bug needs a construct, the construct is
shown.

## 1. What worked well

1. **Parsing and the issues panel.** The 56,550-character source (model plus views) applied with "No issues in the current
   applied model" and the status bar "Issues (0)" (`stale-banner.jpg`). The panel was a reliable reading throughout.
2. **No account, local recovery.** Work survives in the browser: an unapplied edit of 56,092 characters was still in the
   pane after the tab was navigated away and the project restored. This protected the work once.
3. **Named views as the unit.** Declaring a `view` with `expose` and `filter` and seeing it appear at once in the Views list
   and render is a good loop. Seven views were declared and edited over six revisions with one click each.
4. **Interconnection view of a part definition.** Exposing the part definition `Cubesat` drew all nine of its parts with
   their attributes, and the binding edges between the tuned values and the part attributes (`assembly-tall-column.jpg`: 24
   nodes, 4 edges). This is the structure the model's author wanted to see.
5. **Requirements diagram.** The requirements view drew 11 requirement definitions, 11 usages, the two verification
   definitions, and edges labelled `typed by`, `satisfy`, `not satisfy`, `verify` (25 nodes, 33 edges;
   `requirements-view.jpg`). The negated satisfy statement was shown as its own edge kind, which is exactly right.
6. **Requirements table and traceability matrix.** Both read the model's statements correctly: 22 requirements; satisfaction
   Declared for 10 usages and "Negated declaration" for one; verification linking each verification definition to the
   requirements it verifies (`requirements-table.jpg`, `traceability-satisfaction.jpg`, `traceability-verification.jpg`).
   The note "Links are declarations, not verification results" is honest and welcome.
7. **Edge labels and the CSV export button** make the matrix machine-checkable.
8. **Overview tree** of selected members (`expose-overview-tree.jpg`) is clear and readable at a glance.

## 2. What did not work well

Each item is paired with what was tried; bugs with steps are in section 3 and workarounds in section 4.

1. A red banner from an earlier session stays after a clean apply (Bug 1; not seen again in a cold pass on a fresh source).
2. The restored recovery held a condensed older copy of the project, not the latest saved text (Bug 2).
3. A project holds one file; no way to add a second file inside the editor (Bug 3).
4. A view whose filter admits a case definition draws nothing and prints a long list of messages (Bug 4).
5. Inherited parts are missing from a view exposing a usage (Bug 5).
6. The same `expose X` means different things in two representations (Bug 6).
7. On a part with 9 parts the interconnection view lays out as one tall column that is unreadable under fit-to-screen
   (`assembly-tall-column.jpg`). Tried zoom; it works but nothing is legible before zooming.
8. The configurations view shows names and types only; values of attributes are not shown on nodes (`configurations-bare.jpg`,
   `configurations-overview.jpg`). Tried the Overview tree representation: it shows what each configuration redefines,
   still without values.
9. Documentation text (`doc` comments) is not shown on attribute nodes, so the marks the model keeps there (which quantity
   is an effectiveness measure and which a performance measure) are invisible in the diagrams.
10. The pane is cramped below about 1000 px: the source pane, explorer and diagram share a narrow column and a viewport
    around 800 px shows only a thumbnail (`inherited-parts-missing.jpg`). A 1600 x 1000 viewport was used from then on.
11. The pane's screenshot lags one action behind; the page text was read as the record instead.

A cold reader (no background in the model, in the role of a sponsor) used the editor read-only for about twenty minutes and met
these (the reader's own words in quotes, from its account of where it got lost; no screenshots of them were kept):

12. The first click on a toolbar layout button hid the diagram and showed only the source: "I expected a layout toggle, not
    a swap." Nothing tried is recorded; the reader moved on.
13. The stakeholders diagram at fit-to-window was unreadable: "I expected to read at least the top row." The reader zoomed in
    three steps and read the node texts from the page.
14. Clicking a requirement row in the Requirements table seemed to do nothing for a few seconds: "I expected a detail card to open
    beside the table." The layout then split, the model tree opened to the element and the source scrolled; the reader found
    that useful but "not where a sponsor looks".
15. Selecting an element in the model tree highlighted it and moved nothing else: "I expected the source or an inspector to
    follow." The "Show Inspector" button existed; the reader did not get to it.
16. The reader asked for the `metrics` view and still had the requirements view when the time ran out. Nothing tried again is
    recorded; the reader ran out of time.
17. While the reader typed nothing, the diagram header briefly read "Applied revision · draft pending" and the toolbar
    "Working..." with Apply source lit, then returned to "Source applied": it "made me nervous that I had changed something".
    Nothing tried is recorded; the reader left it. The same transient followed restores and applies in the other passes.

## 3. Bugs

Each bug was re-run in a cold pass at the end: a second look from the landing page, in the same browser and workspace.
"New project" opened no dialog from the restored workspace, so the cold pass replaced the project's source with a small
model of 1,254 characters (the minimal model below) instead of the large one, with a second toolkit loading it strictly
with no error (`cold-base-applied.jpg`: Issues (1), a warning that a package named `Views` has the name of a standard library
package, which is right). Where a bug was first met on the large model, that is stated. Each "Reproduced" line says the result.

The minimal model: `part def Sat { part a : Wheel; part b : Wheel; part c : Wheel; }`, `part sat1 : Sat { part :>> a : SmallWheel; part :>> b : SmallWheel; }`,
`calc def Mass`, `analysis def Run`, `requirement def R1`, `verification def V { objective { verify requirement r1 : R1; } }`,
`verification def W` with an empty objective, and `concern c1 : C { requirement r1 : R1; }` and `concern c2` the same, in a
package `Demo`, with views in a package `Views`.

### Bug 1. Stale red banner after a clean apply

Steps:
1. Open `/app` (landing page).
2. Click "Restore recovery" on the project that had earlier shown the red banner.
3. Apply the loading recipe's source (steps 3 and 4) and read the Issues panel.
4. Look at the banner above the editor.

Expected: after an apply with 0 issues, the banner is cleared or reflects the current state.
Observed: the banner "Exploration source correspondence is outside the applied project." remains under "Saved recovery"
while the Issues panel reads "No issues in the current applied model." and Issues (0) (`stale-banner.jpg`). It stayed in every later screenshot. It also appeared directly after restoring (`recovery-condensed-copy.jpg`), before anything was applied.
Reproduced: seen again on every later apply and view in the first session (22 steps); in the cold pass it did NOT reproduce: no red banner after a restore or after a clean apply (`cold-base-applied.jpg`). The banner may therefore depend on the earlier project state it was restored from. The root cause was not established (the banner may belong to
an earlier "Explore model" attempt, or to the project's recovery record).

### Bug 2. Restored recovery was an older, condensed copy

Steps:
1. Open `/app`; the landing page offers "Saved recovery: <project>" with Restore and Discard.
2. Click "Restore recovery"; wait 8 s.
3. Read the source pane's length (the pane's document length; here 38,252 characters).

Expected: the text most recently applied or saved for that project (51,749 bytes / 51,612 characters of source).
Observed: the pane held a 38,252-character copy, starting at `package` with the header comment missing and doc comments
shortened (`recovery-condensed-copy.jpg`). Notes: that copy came from an earlier session in which the text was retyped; it may be
correct behaviour that recovery holds what was saved last. The landing page does not say what the recovery contains
(length, last-saved time), so a user cannot tell it is not the file they expect. Reproduced in a new form (`cold-recovery-restore.jpg`): the restore held the text of an earlier revision (69,901 characters), not the text applied last (71,008 characters), because the save after that apply had failed with Bug 10's message; the revision counter also restarts at 1 after a restore. First seen on the
first restore, and later restores (which held the user's own 56,092-character unapplied edit) behaved as expected.

### Bug 3. No way to add a second file to a project in the editor

Steps:
1. Open `/app` and a project; the Explorer lists "Files" with one file, `model.sysml`.
2. Click the "..." menu at the top of the Explorer.

Expected: an entry to add a file (the model and its views are two files in the author's repository).
Observed: the menu offers only "Narrow Explorer" and "Widen Explorer" (`no-add-file.jpg`). The Files list shows one file.
The only route to add content is to join the files into one text (done here) or "Open files or project", which imports.
Reproduced in the cold pass (`cold-explorer-menu.jpg`): the Explorer panel options show only Narrow and Widen Explorer. (The project header reads "1 files · revision N · local browser workspace").

### Bug 4. A view whose filter admits a case definition draws nothing

Steps:
1. Apply a model with a `calc def` and an `analysis def` in a package, plus this view (the exact filter that was used):
   ```
   view metrics : GeneralView {
       filter @SysML::CalculationDefinition or @SysML::AnalysisCaseDefinition;
       expose CubesatTradeSpaceV2::*;
   }
   ```
2. In the Explorer's Views list click `metrics`; wait 3 s.

Expected: the calculation definitions drawn as nodes, as the requirements view draws requirement definitions.
Observed: the canvas reads "Rendering unavailable. The case representation has no renderer in this foundation." with a
list of lines of the form "calc def <Name> holds no case; a case rendering does not show it", one per calculation
(`case-no-renderer.jpg`). The same message appears for a view filtering `VerificationCaseDefinition`
(`verification-no-renderer.jpg`, expected the two verification definitions). Changing the filter to
`@SysML::CalculationDefinition` only drew 32 nodes and 0 edges (the 29 calculation definitions plus the two verification
and one analysis definitions, which are also calculations by inheritance), so the filter works as a workaround for drawing,
but only partially (see section 4). Reproduced in the cold pass (`cold-case-filter.jpg`) with `view caseFilter : GeneralView { filter @SysML::CalculationDefinition or @SysML::AnalysisCaseDefinition; expose Demo::*; }`: "Rendering unavailable. The case representation has no renderer in this foundation." and "calc def Demo::Mass holds no case; a case rendering does not show it".

### Bug 5. Inherited parts missing when a view exposes a usage

Steps:
1. Apply a model with a part definition `Cubesat` (nine parts) and a usage `cubesatBaseline : Cubesat` that redefines two of
   them, plus
   ```
   view assembly : InterconnectionView { expose CubesatTradeSpaceV2::cubesatBaseline; }
   ```
2. Click `assembly` in the Views list; switch to the diagram layout; wait 3 s.

Expected: the usage drawn with all nine parts, as the part definition is.
Observed: three nodes, no edges: `cubesatBaseline` with its attributes, and only the two redefined parts (`wheel`,
`tracker`); the seven inherited parts are not drawn (`inherited-parts-missing.jpg`). Exposing the part definition
`CubesatTradeSpaceV2::Cubesat` drew all nine (`assembly-tall-column.jpg`), so the model is not at fault.
Reproduced in the cold pass (`cold-inherited-parts.jpg`) with `view inherited : InterconnectionView { expose Demo::sat1; }`: 3 nodes (`sat1`, `a : SmallWheel`, `b : SmallWheel`); the inherited `c : Wheel` is not drawn.

### Bug 6. `expose X` behaves differently by representation

Steps:
1. Apply the loading recipe's source with a view that exposes a part definition under a type filter, for example
   `view v : GeneralView { filter @SysML::PartUsage; expose CubesatTradeSpaceV2::Cubesat; }` (the session's view of this
   kind exposed `Cubesat` alone), and click it in the Views list.
2. Change the view to the Overview tree representation exposing the same `CubesatTradeSpaceV2::Cubesat` (New view, Show =
   the part, Representation = Overview tree), and click it.

Expected: `expose X` means the same element set in each representation.
Observed: with a filter, `Cubesat` was drawn bare; in the Overview tree the same `expose Cubesat` drew all 23 members
(`expose-overview-tree.jpg` shows the result after narrowing it to the intended members). We did not find a statement of
this difference in the editor.
Reproduced in the cold pass: `view filtered : GeneralView { filter @SysML::PartDefinition; expose Demo::Sat; }` drew 1 node, `Sat` bare (`cold-expose-filtered.jpg`); `view tree : GeneralView { expose Demo::Sat; }` drew an Overview tree of 4 nodes and 3 edges, `Sat` with `a`, `b`, `c` (`cold-expose-tree.jpg`). Earlier, seen at two revisions of the large model's views. The snippet above was a
reduction of the session's views, so if it does not show the difference the session's views are the reproduction.

## 4. Workarounds

| Failure | Tried | Worked |
|---|---|---|
| Source file not loadable by the editor (local file fetch blocked in the pane) | typing the model by script | Fetching the file's raw text from a public repository URL into a page variable, joining it with the views, and setting the pane text in one step; length and a SHA-256 of the pane text were compared with the file |
| One file per project | Looking for an add-file entry | Joining the model and the views into one text (the repository keeps them apart) |
| Recovery of unknown content | Reading the length after restore | Applying the full source and reading its length and checksum, so the pane's content is known |
| Stale red banner | Applying again; switching views | Ignoring it and trusting the Issues panel and "Source applied" |
| Case definitions do not draw (Bug 4) | Filters with `AnalysisCaseDefinition`, `VerificationCaseDefinition` | A filter of `@SysML::CalculationDefinition` alone drew the calculations (and the cases as boxes, no edges) |
| Inherited parts missing (Bug 5) | Exposing the usage | Exposing the part definition |
| Configuration usages show no owners (3 bare nodes) | Selecting only the redefined parts | Exposing each configuration plus `::*` (`configurations-overview.jpg`: 19 nodes, 16 edges) |
| Too many members under `expose X` in an Overview tree (Bug 6) | None needed beyond narrowing | Naming each member (`expose X::member`) |
| Reading a tall diagram | Fit-to-screen | Reading the node texts from the page (the `.react-flow__node` elements) instead of the image |

## 5. Suggestions

Each is paired with the failure it answers. The first group are requests for what the editor cannot yet show of a
verification chain (how a requirement is verified and by what evidence), which is what the modelling work needed most.

1. **A renderer for verification and analysis cases** (Bug 4; the verification view in `verification-no-renderer.jpg`). Draw
   the case definition with its objective, subject, `verify` links and the calculations it returns; at least list the case
   with its relations instead of "Rendering unavailable". A case is part of the verification chain; today the requirements
   view only shows the cases as related context nodes with edges.
2. **Evidence and environment fields in the requirements table and traceability matrix** (`requirements-table.jpg`,
   `traceability-verification.jpg`). Both tables record that a verification definition verifies a requirement, but have no
   column for what evidence the verification produces (its result, units, tolerance) or its environment (model, test rig,
   analysis case). The Identifier column read "-" for every requirement and the Documentation column "-" on every usage; an
   identifier taken from a `doc` or a short-name attribute, and a column that shows the requirement's constraint expression,
   would make the table readable on its own.
3. **Show attribute documentation and user metadata on nodes**, or in a hover (section 2, item 9). The model marks each
   quantity as a measure of effectiveness or of performance in a `doc`; metadata annotations are not shown either. Even a
   tooltip with the first line of `doc` would let a reader see the mark.
4. **Show attribute values on usage nodes** (item 8). A configuration is its values; showing `attr = value` on the node would
   make the configurations view carry the information that now needs the text pane.
5. **Draw calculation chains** (Bug 4's workaround, 32 nodes and 0 edges, `case-no-renderer.jpg` for the message). Edges from a `calc def` to the calculations it
   invokes and the attributes that read it would show how each evaluated quantity is obtained from the design variables;
   today only the boxes are drawn.
6. **Clear or date the red banner** (Bug 1) and **label the recovery on the landing page** with length and last-saved
   time (Bug 2), so a user knows what Restore will bring back.
7. **An add-file entry in the Explorer's menu** (Bug 3), so a model and its views stay in separate files as in a repository.
8. **Draw inherited members of a usage, or say why not** (Bug 5), and **document how `expose X` differs across
   representations** (Bug 6).
9. **A readable layout for tall interconnection views** (item 7, item 13): a two-column or grid layout, or fit-to-width with a legible
   minimum text size.
10. **A responsive layout below about 1000 px** (item 10): collapsing the explorer and source pane by default would make a
    narrow pane usable.
11. **A layout control that shows both panes by default** and labels what each button does (items 12, 13); **a detail card or
    inspector that opens on selection in the table and the tree** (items 14, 15); **a short "rendering..." note instead of "draft
    pending"** when nothing was edited (item 17).

## 6. A second session: the chain from stakeholder concern to evidence

A second session extended the model with stakeholder concerns (SysML v2 `concern` definitions and usages, each with a
subject and a stakeholder, holding requirement usages), two verification definitions that carry pointer attributes
(`String` attributes naming a log entry, a record, a test and an environment) and verification usages that verify
the concerns' requirements. The editor drew the chain from concern to requirement to verification case well: a view of
54 nodes and 26 edges, and matrix rows named `<package>::<concern>::<requirement>` with "Declared" under the verifying
case (`matrix-concern-rows.jpg`). The items below are what the editor could not show, and three places where it and a
second SysML v2 parser disagreed. Steps 1 to 3 of each item are the loading recipe of the Context section.

### Bug 7. `expose P::*` on a package with private imports also draws the imported libraries

Steps:
1. Open `/app`, restore or create the project, and apply the loading recipe's source with an added package
   `package Probe { private import CubesatTradeSpaceV2::*; ... }` of about twenty elements and a view
   `view probeView : GeneralView { expose Probe::*; }`.
2. Click `probeView` in the Views list; wait 3 s.

Expected: the package's own elements (about twenty).
Observed: 958 nodes and 1,770 edges: the members the package imports privately (the scalar-value library, the whole
model package, the standard view definitions, the SysML and KerML metamodel) are drawn as well, and the canvas is
unreadable (`expose-star-imports.jpg`). The package's own elements are among them.
Reproduced in the cold pass (`cold-expose-star.jpg`) with `package Probe { private import Demo::*; private import StandardViewDefinitions::*; part p : Sat; view star : GeneralView { expose Probe::*; } }`: 666 nodes and 1,399 edges, including scalar-value, KerML and standard view definition elements; about 20 s, with "Working..." and the previous view shown meanwhile. Workaround: expose each element by name (`expose Probe::element;`). Suggestion: `::*` should list
the members a package owns, not those it imports privately, or the view's documentation should say so.

### Bug 8. A `verify` in a typed verification usage's objective is rejected as a duplicate inherited name

Steps:
1. Apply the minimal model plus
   `package Bug8 { private import Demo::*; verification ev : V { objective { verify c1.r1; } } }`, where `V`'s objective
   already holds `verify requirement r1 : R1`. (The first session's lines were
   `verification costEvidence : ConfigurationVerification { objective { verify affordable.launchBudget; } ... }` against
   that definition's own `verify requirement launchBudget`.)
2. Click "Apply source".

Expected: the text applies (a second SysML v2 toolkit loaded the same text in strict mode with no error).
Observed: two errors "model.sysml:964 Duplicate of inherited member name 'launchBudget' from" (the message ends after
"from", with no owner named), "Source has errors; the last applied model is retained", Issues (2)
(`duplicate-inherited-member.jpg`). A `verify` takes the name of the feature it verifies, so it collides with the
definition's member of that name.
Reproduced in the cold pass (`cold-inherited-dup.jpg`): "error model.sysml:42 Duplicate of inherited member name 'r1' from", again ending after "from", then "Source has errors; the last applied model is retained". The same verification usage typed by a new definition with its own objective applied with 0 issues in the first session.
Suggestion: if the rule is intended, complete the message with the owner and say how to avoid it; if not, a verify
member in a usage's objective should not clash with the typing definition's member.

### Bug 9. Two `verify` statements naming same-named features in one objective: "Duplicate of other owned member name"

Steps:
1. Apply the minimal model plus
   `package Bug9 { private import Demo::*; verification ev2 : W { objective { verify c1.r1; verify c2.r1; } } }`,
   where `c1` and `c2` each hold a requirement usage `r1`. (The first session's lines were
   `verify longLife.depthOfDischarge; verify powerAndEnergy.depthOfDischarge;` in one objective.)
2. Click "Apply source".

Expected: the text applies (the same second toolkit accepted it).
Observed: Issues (3): "Duplicate of other owned member name" at the two `verify` lines, with no member named
(`duplicate-owned-member.jpg`); the last applied model is retained.
Reproduced in the cold pass (`cold-owned-dup.jpg`): "error model.sysml:42 Duplicate of other owned member name" twice, with no member named. Workaround: rename one requirement usage so the two verified features have different names; the text then
applied with 0 issues. Suggestion: name the member in the message and the line of the earlier declaration.

### Bug 10. Recovery clash between two tabs: the message does not say which copy wins

Steps:
1. Open `/app` in a first browser tab, click "Restore recovery" on the project's landing page and apply the loading recipe's source.
2. Open `/app` in a second tab of the same browser; click "Restore recovery" (or create a project) for the same project.
3. Return to the first tab, make an edit and click "Apply source" (the failed save shows after an apply), and look at the header.

Expected: a message that says which copy is kept and what a retry does.
Observed: "Recovery could not be saved. Your current project is unchanged. Another tab changed local recovery. Retry to
inspect its saved copy before continuing." with a "Retry recovery" button (`recovery-clash-wording.jpg`). The editor caught
the clash, which is good; the wording leaves unclear whether the saved copy or the tab's copy is kept after a retry.
Reproduced: yes. The same message appeared whenever a second tab restored or created the project; in the cold passes and in two further readers' tabs; its effect is the new form of Bug 2 (the restore then held an older text). Suggestion: name the two copies with their last-saved times and say which one "Retry recovery" keeps.

### Feature requests: what the chain needs and the editor cannot show

For each, steps 1 to 3 are the loading recipe with the second session's source (the model, a file of stakeholders and
concerns, the views).

**F-1. Show attribute values on nodes.** Steps: 4. Click the view `stakeholders` (Overview tree); 5. read an evidence
case's attribute nodes. Expected: `name : String = "..."` with the value the usage assigns. Observed: the node
shows `name : String` only (`concern-view-no-values.jpg`), so the pointers to the record, the test and the
environment, which are the evidence, are invisible in the diagram. This extends item 4 of section 5.

**F-2. A column for evidence and environment in the requirements table and traceability matrix.** Steps: 4. Open the
Requirements table; 5. type the package name into "Search requirements". Expected: beside "Declared verification", the
verifying case's pointer attributes (or any chosen attributes of the verification usage). Observed: the 12 rows show
Identifier, Kind, Documentation, Declared satisfaction and Declared verification, and nothing of the case's attributes
(`table-concern-rows.jpg`). A verification usage with pointer attributes and no objective of its own adds no row and no
link (it appeared in neither table). Suggestion: a configurable column list, or a "show attributes of the verifying
case" toggle.

**F-3. Concerns and stakeholders as rows of the requirements table.** Steps: as F-2. Expected: the concern usages as
rows (a concern is a requirement in SysML v2), with the stakeholder and the concern's documentation. Observed: only the
requirements the concerns hold, each named `<concern>::<requirement>`; the concerns themselves, their stakeholders and
their `doc` are not rows or columns (`table-concern-rows.jpg`). "Who cares" has to be read from the row's name.

**F-4. Draw the binding of a concern's stakeholder to its part.** Steps: 4. Click the view `stakeholders`; 5. find a
concern with its `stakeholder` parameter. Expected: an edge from the stakeholder parameter to the part it is bound to
(`stakeholder :>> s = sponsor`). Observed: the parameter is drawn, the binding is not (`concern-view-no-values.jpg`),
although the editor draws bindings elsewhere (`assembly-tall-column.jpg`).

**F-5. Render verification usages that carry pointers.** Steps: 4. Click the view `stakeholders` (Overview tree), whose
source exposes a verification usage `<name> : EvidenceCase` that carries four `String` pointer attributes; 5. Find the
usage's node. Expected: a rendering of the case that shows the case, its subject, its objective's `verify` links and its
attribute values, in one place. Observed: the usage is drawn as a box with attribute nodes that show the type only, and one
`verify` node per requirement (`concern-view-no-values.jpg`); a view that filters verification definitions gives "Rendering
unavailable" as in Bug 4. In the requirements table a verification usage with pointers and no objective of its own adds no row
(Bug 4's workaround of the Overview tree is what was used).

A note on what was not the editor's doing: during the session the browser tab was twice changed by something outside the
editor (once navigated to an unrelated local page, once clicked in); these are not reported as bugs.
