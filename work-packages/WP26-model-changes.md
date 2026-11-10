# WP26 — The model read through the view editor: the changes list (D-1 (b))

The modeller's findings from one round in the OpenMBEE View Editor
(https://openmbee-view-editor.vercel.app/app, project "cubesat") on `examples/adcs/model_v2/cubesat.sysml` with
`examples/adcs/model_v2/views.sysml` applied after it as one model. Each finding names the intent it serves, its
class and its evidence (step numbers are rows of the round's step log, `scratchpad/view-editor/wp26/steps.md`, with
one screenshot each). Classes, as the scope defines them: **landed** (in `views.sysml`, or an in-file change whose
outputs are byte-identical, checked), **held** (a change judged right but not landed this round, with its diff),
**gate** (anything the oracle, the coverage table, the generator or the contract reads: a diff or a sketch for the
next data gate; never lands in this package).

The intents, quoted:

- **I1** (WP22, the supervisor): "a space of configs on one side (how its constructed) and a space of metrics on the
  other (how its evaluated)".
- **I2** (WP22, the supervisor): "a bunch more metrics explicitly included but tied to our actual requirements"; every
  traded metric marked MoE or MoP ("MoE on mass, no new column", WP23).
- **I3** (WP23, the supervisor): "think of this in terms of the coupling variables between subsystems in the MDAO lit"
  (the coverage table as a connected graph).
- **I4** (WP26, the supervisor): the model "conformant, intuitive, interpretable and aligned with our intents", using
  "the sysmlv2 affordances without requiring open ended exploration of text".

Counts: **landed 8** (5 in `views.sysml`; N1 to N3 in `cubesat.sysml`, landed in the sequel), **held 1**, **gate 6**, and
4 observations with no change.

## What was applied, and the state at the end

- The model text went in verbatim: the page fetched `cubesat.sysml` at b9d8b80 from the repository's public raw URL
  (51,612 characters, equal to the file's character count; 51,749 is its byte count), and `views.sysml` was set after
  it. The final applied text (editor revision 6) is the two committed files joined by a newline: 56,550 characters,
  sha256 `a4ff88cc447f…`, equal in the page and on disk. Issues panel: "No issues in the current applied model"
  (Issues (0)) at every apply (steps 07, 17, 19, 21).
- The editor's project holds one file (`model.sysml`); it offers no way to add a second file to a project (step 04),
  so the two files are joined there. The repository keeps them apart, so the model's bytes and the ledger's model hash
  do not move for a view.
- The toolkit check: `tests/test_system_model_v2.py::test_views_file_loads_with_the_model_and_every_exposed_name_resolves`
  (`REQUIRE_OPENSYSML=1`) loads the two files as one model strictly, finds each view and every exposed name, and
  checks the model's own elements are the same with the views as without them. Negative controls: a misspelt
  exposed name fails the strict load ("unresolved reference"); `find` of an absent name returns None.

## The views, as rendered (D-1 (a), R-4)

| View | Kind | Shows (as rendered) | Step |
|---|---|---|---|
| `assembly` | InterconnectionView on `Cubesat` | the nine parts (bus, both panels, battery, antenna, IMU, wheel, tracker, controller with Kp and Kd), Cubesat's attributes, and binding edges from `panelSpan` to both panel spans and from `batteryCapacity` to the battery: the tunes drawn as bindings. 24 nodes, 4 edges | 18 |
| `alternatives` | GeneralView, part and enumeration defs | the swaps: the three wheels specialize `ReactionWheel`, the three trackers `StarTracker`, each abstract part pointing to its enumeration (`wheelClass`, `grade`); `DesignRanges` and `GainBox` alone. 12 nodes, 8 edges | 09 |
| `configurations` | GeneralView (Overview tree) | each named configuration with what it redefines: agile and compact their span, capacity, wheel, tracker and gains; the baseline its wheel and tracker. 19 nodes, 16 edges | 19 |
| `metrics` | GeneralView, calc defs | the 29 calc defs, the two verification defs and the analysis def as boxes; no edges | 20 |
| `requirements` | GeneralView, requirement defs and usages | 11 requirement defs (their docs), the 11 baseline requirements, and as related context `cubesatBaseline` and the two verification defs; edges: 11 typed-by, 10 satisfy, 1 not satisfy (pointing error), 11 verify. 25 nodes, 33 edges | 12 |
| `metricCarriers` | GeneralView (Overview tree) | total mass and launch cost, the measured slew (settling time, control effort, peak torque, peak momentum, the torque-squared integral) and the four budget limits. 13 nodes, 9 edges | 21 |

The requirements table (step 14) lists 22 requirements: declared satisfaction on the 11 baseline requirements
(`cubesatBaseline`; "Negated: cubesatBaseline" for the pointing error), declared verification on the 11 defs
(`ConfigurationVerification`: launch budget, pointing error, power; `SlewVerification`: the other eight). The
traceability matrix (steps 15, 16) shows the same as cells: satisfaction 10 "Declared" and 1 "Negated declaration"
in one column; verification 3 + 8 in two columns. Both match the model's `satisfy`, `not satisfy` and `verify`
statements one for one.

### The editor's views against ours (`views/assembly_view.png`, `views/behavioural_view.png`)

- **What the editor shows that ours do not.** The parts' own attributes and fixed values (bus dimensions, panel
  chord, antenna offset, the controller's default gains) and the bindings that carry a tune into a part
  (`panelSpan` to both panels' span, `batteryCapacity` to the battery); each named configuration with exactly what it
  redefines; every calc def of the model, not only those that end in a metric; the measured quantities that are not
  traded (peak torque, peak momentum, the torque-squared integral); the requirement usages with their satisfy, not
  satisfy and verify links drawn and tabled, including the baseline's failing pointing-error requirement as a
  negated link; a requirements table and a traceability matrix exportable as CSV.
- **What ours show that the editor's do not.** The swap and tune marks (`swap` on the categorical variables, `tune` on
  the continuous ones, fixed parts untagged: the configuration space as a reader of I1 wants it); the MoE and MoP mark
  on each traded metric (the editor shows docs on requirement defs, not on attributes or calcs); the line from each
  requirement to the metric it reads, and from the experiment and the measurement to each metric (the calc chain:
  the editor draws no edge between calcs, because an invocation inside an expression is not a relationship it
  draws); the analyst's grouping of the metrics; the three requirements that read no traded metric set apart.
- **Reading.** The editor's views complement ours: they make the structure, the configurations and the traceability
  browsable and checked by a second parser; ours remain the place where the configuration space is marked by kind of
  variable and where each metric is tied to its requirement and to how it is obtained (I1, I2, I3). Neither replaces
  the other in this round.

## Findings

### Conformance

| # | Finding | Intent | Class | Change and evidence |
|---|---|---|---|---|
| C1 | `verification` is a reserved word: a view named `verification` fails the toolkit's strict load ("is a reserved keyword, not a name the ID terminal admits") | I4 | landed (`views.sysml`) | the view renamed during drafting, then replaced (C2); the toolkit load is the test above |
| C2 | A view whose filter admits a case (`@SysML::AnalysisCaseDefinition`, `@SysML::VerificationCaseDefinition`) renders "Rendering unavailable. The case representation has no renderer in this foundation." with a list "calc def X holds no case" | I4 | landed (`views.sysml`) | `metrics` filters `@SysML::CalculationDefinition` only (cases are calcs, so they draw as boxes under it); the verification view dropped: the verify links show in `requirements`, the table and the matrix (steps 11, 13, 20) |
| C3 | The model with the views applies at 0 issues in the editor and loads strictly in the toolkit: the two parsers agree | I4 | observation | steps 07, 17-21; the parse test |

### Names and docs

| # | Finding | Intent | Class | Change and evidence |
|---|---|---|---|---|
| N1 | Section 5's package doc reads as a history ("Four requirements, one per flag ... WP22 added ... WP23 completes the set ... round 2 adds") while the section holds eleven requirements; a reader must add up the history to learn what is there | I2, I4 | landed (sequel) | restated as what is there: four flag requirements, six more on a traded metric's own quantity, the battery peak power one; same facts, no history (diff below). Checked: coverage table differs only in its hash lines; 216 of 217 model tests pass, the one failing being the ledger-hash pin (`test_mutation_v2.py::test_the_oracles_model_path_is_the_committed_file_the_ledger_hashes`, expected until the re-run); the committed views are the generator's output (byte-equal). Landed in the sequel through the container re-run of the five entries (OD1 (b) as amended; below) |
| N2 | `SlewVerification`'s doc has one 149-character line (the file's other lines are at most 100) | I4 | landed (sequel) | rewrapped (diff below); checks as N1 |
| N3 | The model's header names its two views but not the views a view editor draws | I4 | landed (sequel) | three comment lines pointing to `views.sysml` (diff below); checks as N1 |
| N4 | Docs carry project-process references that do no work for a reader of the model: "(illustrative, WP23 round 2)", "(WP23 OD1)", "(WP16)", "the supervisor's choice from the loop's ladder (WP23-decisions.md ...)", "(WP23)"; 11 mentions of a work package below the header, read in the editor's Documentation column | I4 | held | not drafted this round; the proposal: each doc states the fact and its basis (a public class, a threshold's rule), the history stays in the decision records. Two of these docs are read by the generator (the requirement docs, `project.py`), so their edits are gate class; the constants' docs are held class |
| N5 | Two requirement docs describe our generated picture: `PowerRequirement`'s and `BatteryPeakPowerRequirement`'s "so the behavioural view draws it with no line"; a model element's doc should say what the element states, not how a picture draws it | I4 | gate | the generator reads requirement docs (`project.py`, `doc_text` on each requirement): drop the clause at the next data gate and regenerate the views |
| N6 | The requirements table's Identifier column is "—" for all 22 requirements, and the Documentation column is "—" for the 11 baseline requirements (they are bare usages) | I2, I4 | gate | sketch: short ids on the defs, e.g. `requirement def <'R-PE'> PointingErrorRequirement`, and a one-line doc on each baseline requirement only if it says something the def does not (else none: a doc that repeats the def does no work). Requirement elements are read by the coverage table and the generator |

### Intents

| # | Finding | Intent | Class | Change and evidence |
|---|---|---|---|---|
| T1 | The configuration space is explicit in the editor once views expose it: the parts and the tunes' bindings (`assembly`), the swaps under their enumerations (`alternatives`), what each named configuration redefines (`configurations`) | I1 | landed (`views.sysml`) | steps 09, 18, 19 |
| T2 | The metric space reads in the editor as where the metrics live (`metricCarriers`) and the requirements with their satisfy and verify links (`requirements`, table, matrix) | I1, I2 | landed (`views.sysml`) | steps 12, 14-16, 21 |
| T3 | Only the baseline carries `satisfy` statements, so the traceability matrix has one column: the agile and compact configurations, the corners of the space, show no verdict against any requirement | I1, I2 | gate | sketch: `satisfy` / `not satisfy` each of the eleven requirements by `cubesatAgile` and `cubesatCompact`, each verdict computed by the model's own requirement (with their measured slews as recorded measurements, as for the baseline). Satisfy relations are read by the coverage table and the generator |
| T4 | The baseline states none of its tuned values: it takes `Cubesat`'s defaults, so in `configurations` it shows only its wheel and tracker, as if it tuned nothing, while agile and compact show span, capacity and gains | I1 | gate | sketch: restate `:>> panelSpan default = 0.6 [m]; :>> batteryCapacity default = 80.0 [W*h];` and the controller's gains in `cubesatBaseline` (equal values); configuration values are read by the oracle and the tests |
| T5 | The MoE and MoP marks are the first word of a `doc`; the editor shows docs on requirement defs but not on attributes or calcs, so in the editor the marks are invisible on the metrics themselves | I2, I4 | gate | sketch: SysML metadata (`metadata def MoE; metadata def MoP;` and `#MoP attribute totalMass ...`), which a view editor and a query can read as data; the coverage table and the generator read the doc mark today |
| T6 | The calc chain from configuration to metric (I3's coupling variables) is not drawn by the editor: calcs are invoked inside expressions, which it does not draw as relationships | I3 | observation | `metrics` shows 32 boxes and no edge (step 20); the coverage table and our behavioural view remain where the graph is read |

### The editor's affordances

| # | Finding | Intent | Class | Change and evidence |
|---|---|---|---|---|
| A1 | `expose X` under a `filter` draws X alone (steps 10, 20); in an Overview tree with no filter it draws X with all its members (rev 5 of `metricCarriers` drew Cubesat's 23 members); `expose X::*` draws the members without X (step 19's first version) | I4 | landed (`views.sysml`) | `configurations` and `metricCarriers` expose an element and its `::*` together, with no filter; `metricCarriers` exposes Cubesat's two metric attributes by name |
| A2 | The requirements table and the traceability matrix read `satisfy`, `not satisfy` and `verify` straight from the model, with the baseline's failing requirement shown as a negated link: the model's statement of feasibility is browsable without reading text | I2, I4 | observation | steps 14-16 |

## The in-file diff (N1, N2, N3), landed in the sequel

Byte-identical outputs are the condition for landing. The diff below landed with WP23's O-1 (the pointing limit's
primary share printed as 95.0 %: 671 of 706 feasible designs at 0.008495 degree on the data of record; the launch
budget's 94.9 %, 670 of 706, is correct and stays), under OD1 (b) as amended (2026-11-10, 15:05: a host re-run
cannot reproduce the container's bytes, so an in-file edit lands through a container re-run), on the edited model
(sha256 `65ecd7a7e731`):

- **Neutrality on the host** (a throwaway tree; its entries discarded): each output equal to its host `@6` hash:
  `d601d82833b6` (primary), `9d1f4849ba46` (baseline), `48493bf3f6e6` (check predictions), `e3f22d93c7d7` (check
  designs), `fd46402c2f61` (shared subspace).
- **The container re-run** (`hts-paper` `877c42cc10e3`, container `hts-wp26`, `--network none`, removed after;
  `ledger_gate.py --image 877c42cc10e3 --wp26`): each output equal to its `@7` hash: `a43ccc557bc6`, `10ae79a224b5`,
  `6b65b2843a99`, `5b47f53b4d7b`, `d16ae3648c40`; the entries `v2-primary@8`, `v2-baseline@8`,
  `v2-check-predictions@8`, `v2-check-designs@8`, `scope-sensitivity-shared-subspace-v2@7`, `git_dirty` False;
  no data file changed. The supplementary notebook's table of datasets prints the current entries and moved with
  them (host-recorded, re-pin at the gate).

```diff
diff --git a/examples/adcs/model_v2/cubesat.sysml b/examples/adcs/model_v2/cubesat.sysml
index ccb782b..5263e80 100644
--- a/examples/adcs/model_v2/cubesat.sysml
+++ b/examples/adcs/model_v2/cubesat.sysml
@@ -57,6 +57,10 @@
  * SysML v2 cannot integrate the ODE, so the measured quantities enter the experiment as `in`
  * parameters. Section 4 carries a closed-form approximation for model checking.
  *
+ * The views a SysML v2 view editor draws (the assembly, the alternatives, the named
+ * configurations, the calcs, where the metrics live, the requirements with their satisfy and
+ * verify links) are declared in views.sysml beside this file and applied after it as one model.
+ *
  * How a Python caller reads this model (opensysml client; `m = conn.load_from_content(text,
  * strict=True)`; P = "CubesatTradeSpaceV2"). No number below is copied into Python:
  *   ranges, gain boxes, scenario numbers, constants
@@ -547,23 +551,20 @@ package CubesatTradeSpaceV2 {
            thresholds, `satisfy` statements tying each requirement to the baseline, `verification
            def`s naming what each verifies, and claims over every in-range configuration. */
     // BEGIN 15.2
-    doc /* Feasibility is stated here and verified, not computed in Python. Four requirements, one
-           per flag the experiment reports: settled, momentum_ok, power_ok, dod_ok. A requirement
-           takes a Cubesat as its subject and, where it needs a measured quantity of the slew, an
-           `in` parameter that the runner binds by name (a Quantity, or a Real for the integral of
-           |tau|^2). The defaults of those parameters are the recorded measurement of the baseline
-           (below), so the `satisfy` statements are checkable without a runner. WP22 added one
-           requirement over each of power margin and energy balance (the calc the experiment
-           returns as the metric) and restated the depth-of-discharge requirement over its calc;
-           its requirement over the eclipse reserve, the same inequality, left at the close-out.
-           WP23 completes the set: the slew-time and slew-band requirements fold into
-           SettledRequirement (one time metric, the settling time), and the four metrics that had
-           no requirement get one, pointing error, control effort, peak slew power, and the total
-           mass through the launch cost, each with the supervisor's threshold in `budgets` below;
-           round 2 adds the battery peak power requirement, the pack's rating against the eclipse
-           peak load. Every threshold is a value this model states: zero for a margin or a balance, the
+    doc /* Feasibility is stated here and verified, not computed in Python. Eleven requirements.
+           Four are the flags the experiment reports: settled, momentum_ok, power_ok, dod_ok; the
+           settled and depth-of-discharge ones read the settling time and the depth of discharge.
+           Six more each read a traded metric's own quantity: pointing error, control effort, peak
+           slew power, power margin, energy balance, and the total mass through the launch cost;
+           so every one of the eight traded metrics has a requirement. The eleventh, the battery
+           peak power requirement, reads the pack's rating against the eclipse peak load. A
+           requirement takes a Cubesat as its subject and, where it needs a measured quantity of
+           the slew, an `in` parameter that the runner binds by name (a Quantity, or a Real for
+           the integral of |tau|^2). The defaults of those parameters are the recorded measurement
+           of the baseline (below), so the `satisfy` statements are checkable without a runner.
+           Every threshold is a value this model states: zero for a margin or a balance, the
            maximum depth of discharge of the environment, the horizon of the nominal slew, a
-           budget the supervisor chose, or the pack's own rated power. */
+           limit in `budgets`, or the pack's own rated power. */
     part def SlewMeasurement {
         doc /* A measurement of one slew: the quantities the requirements and the experiment read.
                The simulator (adcs_sim.simulate_adcs) reads these inputs of the configuration:
@@ -751,8 +752,8 @@ package CubesatTradeSpaceV2 {
                verifies the requirement on a traded metric's own quantity: settling time, control
                effort, power margin, energy balance, peak slew power, depth of discharge; the
                momentum requirement reads the measured peak momentum, and the battery peak power
-               requirement the pack's rating against the eclipse peak load, neither traded. With ConfigurationVerification, every traded metric has a
-               requirement. */
+               requirement the pack's rating against the eclipse peak load, neither traded. With
+               ConfigurationVerification, every traded metric has a requirement. */
         subject c : Cubesat;
         objective {
             verify requirement settled : SettledRequirement;
```
