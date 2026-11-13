# WP27 — Review: stakeholder concerns in the case model, in the view editor

Screenshots for this record: commit `2a669de`, `git show 2a669de:<path>` with `<path>` under `work-packages/WP27-review/`.

The modeller's round (one modeller, the editor's tab of WP26, the step log `scratchpad/view-editor/wp27/steps.md`
with one screenshot per step; the screenshots this review cites are in `WP27-review/`). The scope is
`WP27-scope-of-work.md`; the decisions `WP27-decisions.md`. Sections: D-1 the parse check; D-2 the classed changes;
D-3 the trace as the editor shows it; the tensions read against the concerns; the checks; for the lifecycle demo.
D-4 the P1 cold read with its dispositions; D-5 the sponsor-facing prose (none). D-6, the feature requests, is the
UX researcher's (`WP26-view-editor-feedback.md`).

## D-1. The parse check: what both parsers accept

Each construct was tried against the toolkit's strict load (`REQUIRE_OPENSYSML=1`, the model text plus a probe
package; the probe script is in the session scratchpad, `wp27probe/probe.py`) and, where marked, in the editor
(applied after the model; the issues count read as the WP26 harness reads it, §3; rendering as §4).

| # | Construct | Toolkit strict load | Editor | Chosen for |
|---|---|---|---|---|
| 1 | `concern def` with `subject c : Cubesat; stakeholder s : Sponsor;` | passes | 0 issues; drawn with its subject and stakeholder (steps 01, 09) | the two concern defs |
| 2 | `concern x : Def;` (a concern usage) | passes | 0 issues; drawn | the four concerns |
| 3 | a concern usage binding its stakeholder before its subject (`stakeholder :>> s = sponsor;` alone) | fails: "Subject must be first parameter." | not tried | — |
| 4 | the same with `subject :>> c;` first | passes | 0 issues; the stakeholder parameter is drawn, its binding to the `sponsor` part is not (step 09) | binding each concern to its stakeholder |
| 5 | `frame concern a : Def;` and `frame x;` in a requirement def | passes | not tried | — (the requirement defs live in `cubesat.sysml`; see D-2, H-1) |
| 6 | a concern usage holding requirement usages typed by `cubesat.sysml`'s requirement defs (across files) | passes | 0 issues; drawn; the requirements table lists each as `concern::requirement` (steps 04, 08) | the trace concern → requirement |
| 7 | a requirement usage typed by a `cubesat.sysml` def that frames a concern (`{ frame x; }`) | passes | 0 issues; drawn as a `frame` node (step 02); its table row does not name the concern | — |
| 8 | `dependency from <requirement def> to <concern>` | passes | 0 issues; drawn as a dependency node (step 02) | — |
| 9 | `satisfy <concern> by cubesatBaseline` | passes | not tried | — (it would state a verdict nothing computes) |
| 10 | a verification usage typed by `ConfigurationVerification` whose objective verifies a concern's requirement | passes | rejected: "Duplicate of inherited member name 'launchBudget' from" (step 03) | — |
| 11 | a verification usage typed by `SlewVerification` carrying `String` pointer attributes and no objective | passes | 0 issues; adds no row and no link to the tables (step 04) | — |
| 12 | a verification usage of a new verification def (`EvidenceCase`) whose objective verifies a concern's requirement | passes | 0 issues; a column of the traceability matrix with "Declared" cells, and the requirement's "Declared verification" in the table (steps 04, 07, 08) | the evidence cases |
| 13 | two `verify` statements in one objective naming features of the same name (`verify a.x; verify b.x;`) | passes | rejected: "Duplicate of other owned member name" (step 05) | — (renamed, D-2) |
| 14 | `verify c::r` (a nested requirement by qualified name) | fails: "Must be an accessible feature (use dot notation for nesting)" | not tried | `verify c.r` instead |
| 15 | pointers as `String` attributes declared on the verification def and redefined on each usage (`:>> ledgerEntry = "..."`) | passes; read through the toolkit by `instantiate(<usage>).get("ledgerEntry")` (an `eval` needs the subject bound) | 0 issues; drawn as attribute nodes showing the type only (step 09) | the pointers |
| 16 | `viewpoint def` framing a concern | passes | not tried | — |
| 17 | a view exposing `<package>::*` where the package has private imports | passes | draws the imported libraries' members too (958 nodes, step 02) | the stakeholder view exposes each element by name |
| 18 | `satisfy <concern>.<requirement> by <configuration> { in <parameter> = <measurement>.<parameter>; }`: a satisfy of an existing requirement usage whose `in` parameter is bound in the body (the redefinition forms, `:>> p = ...` in the body, in a new requirement usage or in `satisfy requirement ... by`, fail the strict load: "Redefining feature must have a compatible direction") | passes; the engine evaluates the binding, not the parameter's default: a settling time of 1000 s stated in the body fails the settled requirement, and the agile control effort fails under its own measurement and holds under the baseline's | 0 issues (step 23); the statement is a cell of the Satisfaction matrix under the configuration's column (steps 24, 25) | the two contrasts' verdicts (L-8) |

Cross-file reference works in both parsers: every chosen construct refers to `cubesat.sysml` from the separate
file, so the additions live in `stakeholders.sysml` and the model's bytes do not move. The two parsers disagree
twice (rows 10 and 13: the toolkit accepts, the editor rejects); the model uses only what both accept.

## D-2. The changes, classed

**Landed** (separate files; every output byte-identical; checks below at each commit):

| ID | Change | Commit |
|---|---|---|
| L-1 | `examples/adcs/model_v2/stakeholders.sysml`: the sponsor (price) and the operator (performance in operation) as parts typed by `Sponsor` and `Operator`; concern defs `PriceConcern`, `PerformanceConcern` (subject the cubesat, stakeholder); four concerns, each held by its stakeholder and holding the engineers' requirements that serve it: `lowCost` (launch budget), `longLife` (depth of discharge), `pointingAndSlewing` (pointing error, settled, control effort, momentum), `powerAndEnergy` (power, power margin, energy balance, peak slew power, battery peak power, eclipse depth of discharge). Every one of the model's eleven requirement defs serves at least one concern; the depth-of-discharge requirement serves both stakeholders | 28f7c9c, a4cde2f |
| L-2 | The roll-ups, each `doc` beginning "Illustrative roll-up" and naming its inputs: `CostToBuild` (illustrative unit costs on the parts the configuration swaps and tunes: 158,500 / 216,200 / 407,600 USD for the compact, baseline and agile configurations) and `EffectiveLife` (the depth of discharge by an illustrative cycle-life rule, 10,000 cycles at 0.3, one cycle per orbit: 2.65 / 5.11 / 8.57 years with the baseline's recorded slew); the launch cost is the model's own (71,944 / 79,749 / 93,960 USD). Read by no output (R-7, tested) | 28f7c9c |
| L-3 | The evidence cases: `EvidenceCase` (subject the cubesat; `ledgerEntry`, `recordEntry`, `testNode`, `environment`) and two usages, `configurationEvidence` (as `ConfigurationVerification`: launch budget, pointing error, power) and `slewEvidence` (as `SlewVerification`: the other eight), each verifying the concerns' requirements and pointing at the current entry (`v2-primary@8` since the sequel), the RECORD.md section of the close-out gate's container regression, its test, and the image of record `877c42cc10e3` | 28f7c9c, 331c9e4, sequel |
| L-4 | `views.sysml`: the view `stakeholders` (GeneralView exposing the stakeholders, the concerns with their members, the evidence cases with theirs, the roll-ups); `views.sysml` is now applied after `stakeholders.sysml` | 28f7c9c |
| L-5 | Tests: WP26's views test loads the three files; `test_stakeholders_file_loads_strictly_and_its_names_resolve` (R-1, negative control), `test_the_trace_from_who_cares_to_every_requirement_is_complete` (R-2), `test_the_rollups_are_illustrative_and_read_by_no_output` (R-7); `tests/test_verification_pointers.py` (R-6: ledger entry exists and is current, RECORD heading exists, the test node collects, the host entry names its platform; negative controls: an unknown entry, a superseded entry, an unknown heading, an unknown image) | 28f7c9c |
| L-6 | The operator's depth-of-discharge requirement named `eclipseDepthOfDischarge` (row 13 of D-1) | a4cde2f |
| L-7 | The baseline configuration's verdict on each concern's requirement: twelve `satisfy` / `not satisfy` statements (the pointing error negated), checked by the engine with the model's eleven (23 hold); the Satisfaction matrix shows them (D-4, step 11) | b9c8819 |
| L-8 | The agile and compact configurations' verdicts on the same twelve requirements (WP27-decisions.md, 16:20): `agileMeasurement` and `compactMeasurement` (their slews integrated as the baseline's is recorded, re-measured by a test within the baseline test's tolerance) and twenty-four statements, the measured requirements binding their `in` parameter to the configuration's measurement (D-1 row 18). The engine checks all 47 statements of the three files and all hold: agile fails the launch budget (93,960 against 90,643 USD), the control effort (0.112 against 0.059 N.m.s) and the peak slew power (7.4 against 2.6 W); compact fails the pointing error (0.008533 against 0.008495 degree). Negative controls: a negated verdict stated as satisfied is false; the agile control effort holds once its binding is the baseline's measurement. The Satisfaction matrix shows the three configurations (D-3, steps 24, 25) | 73b4e89 |

**Held** (judged right, not landed):

| ID | Change | Why held |
|---|---|---|
| H-1 | The requirement defs of `cubesat.sysml` each `frame` the concern they serve (D-1 row 5), so the trace is stated where the requirement is | a frame in `cubesat.sysml` would refer across files to `stakeholders.sysml`'s concerns, and the oracle, the coverage table and the view generator load the model file alone; landing it means moving the concerns into `cubesat.sysml`, a gate-sized change. The separate file states the same trace now |
| H-2 | A requirement on the cost to build (the sponsor's `lowCost` has a requirement on the launch cost only) | needs a budget the supervisor chooses; none is invented |
| H-3 | Evidence cases for the baseline regime's dataset (`v2-baseline@8`) and the check experiments | one evidence entry per verification case is enough to show the chain; more on the driver's word |

**Gate** (anything an output reads; not landed):

| ID | Change | Gate |
|---|---|---|
| G-1 | The cost to build or the effective life as a traded metric | a new metric: the contract (`interface-contract.md` §14) and a regeneration |
| G-2 | When a gate's re-run supersedes the entry a pointer names, the pointer moves in the same unit (`tests/test_verification_pointers.py` fails until it does). Done twice: to `v2-primary@7` after the close-out gate's container regression (331c9e4, record entry its RECORD.md section, environment `877c42cc10e3`), and to `v2-primary@8` with WP26's container re-run | one line in the gate checklist (WP27-decisions.md, scope gate) |
| G-3 | The record pointer named the data gate's section while the current entry was the host `@6` run (RECORD.md has no section for host runs) | settled: it names the close-out gate's container regression, the record of the image the current entries were run in |

## D-3. The trace as the editor shows it

Applied text (revision 9): `cubesat.sysml`, `stakeholders.sysml`, `views.sysml` at a4cde2f's content, joined by
newlines: 69,991 characters, sha256 `fc116a037866…`, equal in the page and on disk; Issues (0) (step 06).

- **The stakeholder view** (step 09): 54 nodes, 26 edges. The sponsor and the operator; each concern with its
  subject, its stakeholder parameter and the requirements it holds; each evidence case with its four pointer
  attributes and one verify per requirement, drawn as an edge to the concern's requirement (12 edges); the two
  roll-ups. Not drawn: the binding of a concern's stakeholder to the `sponsor` or `operator` part, the pointer
  values, the docs.
- **The traceability matrix, Verification** (step 07): 34 requirements (22 of the model, 12 held by the concerns) by
  4 verification cases; each row `CubesatStakeholders::<concern>::<requirement>` has "Declared" under its evidence
  case. So "who cares" is read from the row's name, the evidence case from the column.
- **The requirements table** (step 08), searched for `CubesatStakeholders`: the 12 rows with their declared
  verification. Not shown: the concerns as rows of their own, the stakeholder, the evidence case's pointers.
- **The Satisfaction matrix with the three configurations** (steps 23 to 25, on the three files at L-8's content,
  revision 4, 75,542 characters, sha256 `afeaebf9b100…` equal in the page and on disk, Issues (0);
  `WP27-review/24-satisfaction-matrix-three-configurations.jpg` is the matrix read as data in the split layout,
  `WP27-review/25-satisfaction-matrix-full-width.jpg` the same matrix at full width): searched for `CubesatStakeholders`, "12 requirements · 3
  linked elements", the columns `cubesatAgile`, `cubesatBaseline`, `cubesatCompact`, no cell blank. Per column,
  Declared / Negated declaration: agile 9 / 3 (the launch budget, the control effort, the peak slew power), baseline
  11 / 1 (the pointing error), compact 11 / 1 (the pointing error), equal to the engine's 36 verdicts. A sponsor
  reads the three designs side by side: the agile one fails their own low-cost concern and two of the operator's
  requirements, the compact and baseline ones fail the operator's pointing requirement. The panel says "Links are
  declarations, not verification results": the check that each declaration holds is the repository's test, not the
  editor's (the researcher's feature request).

The chain concern → requirement → verification case is readable in the editor; evidence → environment is in the
model (the pointers, tested) but not shown by the editor's tables or diagram: those gaps go to the researcher's
report (D-6) as feature requests.

## D-4. The P1 cold read in the editor

A fresh reader in the sponsor's persona (P1 of `docs/superpowers/notes/reader-grid.md`), no repository access, the
stakeholder view's image first (step 09's screenshot), then its own tab on the project's recovery at revision 10
(the pushed head 05fbd3c). The prompt, verbatim, with the browser tools' names elided as "[the browser tools]" in
square brackets (the three elisions are the only changes):

> You are a cold reader. You have no access to any repository, record or file except the one image named below, and you use only the built-in browser pane ([the browser tools]) in a tab you create yourself. Do not open, read or search any other file or website.
>
> Who you are: an accountable decision maker, the sponsor of a small satellite project. You have domain judgement and very little time; you do not do mathematics beyond what a budget review needs; you fund the project and sign off the design. What you want to know: what trades against what in this design, and whether you would trust the reading the engineers give you.
>
> Step 1, the image first. Open with the Read tool exactly this one file and say in your own words what it shows, before anything else: /private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/view-editor/wp27/09-stakeholders-view.jpg
>
> Step 2, the tool. Create a NEW browser tab ([the browser tools' new-tab call], then navigate in that tab; never act in any other tab, there is one that belongs to someone else) and open https://openmbee-view-editor.vercel.app/app . If the landing page offers "Restore recovery" for a project called "cubesat", click Restore and wait about 8 seconds; if it offers only "New project", stop and report that. Emulate a 1600 x 1000 viewport ([the browser tools' viewport call]) so the diagram is readable. You are READ ONLY: never click "Apply source", "Discard", "New project", never type in the source pane, never import or export. Use the Explorer's Views list (click the view named "stakeholders"; use the diagram layout and zoom to read node texts; you may read node texts from the page with read_page or get_page_text when the image is small), the "Requirements table" and the "Traceability matrix" (search for "CubesatStakeholders" in them; choose Relationship = Verification in the matrix), and the model tree. Your task: starting from "who cares" (the stakeholders and their concerns), follow the model down to the quantities the engineers trade and how each is checked, as far as the tool lets you. Spend the time a busy sponsor would, about 20 minutes of clicking. Take a screenshot at each thing you looked at and say in one line what it was. Close your tab at the end (tabs_close on your own tab id only).
>
> Step 3, your return, in your own words, no ratings: (a) what the image showed you, before you clicked anything; (b) what each stakeholder cares about, as the model states it; (c) for each concern, which engineering trade or requirement bears on it, and where you found that; (d) whether you would trust this reading, and why or why not; (e) where you got lost or stopped, naming the screen and what you expected; (f) what you could not find (for example where a measurement's evidence comes from, or what the numbers are); (g) what you would ask the engineers next. Return this as your final message, verbatim as you wrote it, with the list of screens you looked at.

The return, verbatim:

> Cold read of the cubesat stakeholders view, as the project sponsor. Image first, then about twenty minutes in the tool, read-only, in my own tab (tab-25, created, fronted, and closed at the end; viewport reset before closing). I did not click Apply source, Discard, New project, import or export, and typed only into the requirements search box.
>
> SCREENS I LOOKED AT
> 1. The landing page: "Saved recovery: cubesat" with Restore recovery; I clicked Restore and waited.
> 2. The restored workspace: source file on the left, the stakeholders diagram on the right, "No issues in the current applied model".
> 3. The source file full-width (my layout click hid the diagram): a long English cover note at the top of the file.
> 4. The stakeholders diagram full-width, the overview tree, text too small to read; I read the node texts from the page.
> 5. The diagram zoomed three steps: Sponsor over launchBudget and depthOfDischarge, Operator over pointingError and power, verify edges down to an EvidenceCase with four String slots.
> 6. The diagram zoomed hard on the powerAndEnergy concern: concern → stakeholder Operator; "verify power / powerMargin / energyBalance" subsetting the requirements.
> 7. The Requirements table: 34 requirements, with the line "Read-only · Applied model. Links are declarations, not verification results."
> 8. The table filtered to CubesatStakeholders: 12 requirements; only "Declared verification" is filled (configurationEvidence or slewEvidence); Identifier, Documentation and Declared satisfaction all blank.
> 9. Clicking the lowCost::launchBudget row: nothing visible at first, then (a beat late) the layout split, the model tree opened to lowCost → launchBudget, and the source scrolled to the concern definitions.
> 10. The Traceability matrix, Relationship = Satisfaction: "12 requirements · 0 linked elements".
> 11. The matrix, Relationship = Verification: "12 requirements · 2 linked elements"; launchBudget, pointingError and power "Declared" against configurationEvidence, the other nine against slewEvidence. Every cell says Declared; none says passed.
> 12. Model tree, configurationEvidence selected: highlighted, source did not move.
> 13. Model tree, EffectiveLife calc def selected: same.
> 14. Source scrolled to section 3, "ROLL-UPS": UnitCosts, CostToBuild, BatteryLife, EffectiveLife, each doc saying "illustrative".
> 15. Source scrolled to section 4, "EVIDENCE": the two verification cases with ledgerEntry "v2-primary@8", a recordEntry naming a container regression on 2026-11-10, a test name, and environment "877c42cc10e3".
> 16. The engineers' "requirements" view: a flat row of eleven requirement definitions with their English statements, eleven "baseline..." usages, and edges labelled satisfy, one labelled "not satisfy".
> 17. My click on the "metrics" view: the pane still showed the requirements view when I closed the tab, so I did not see it. During screens 16–17 the diagram header briefly read "Applied revision · draft pending" and the toolbar "Working..." with Apply source live, then went back to "Source applied"; I typed nothing in the source pane and touched neither button.
>
> (a) WHAT THE IMAGE SHOWED ME, BEFORE CLICKING
> A modelling tool showing a project called "cubesat - modified", with a banner saying a recovery was saved locally and, in red, that something about "exploration source correspondence" is outside the applied project. A list of seven views on the left (assembly, alternatives, configurations, metrics, requirements, metricCarriers, stakeholders), a model tree of three packages, and a tree-shaped diagram: a top row of two or three stakeholders (I could make out Operator and Sponsor), a second row that looked like concerns, rows of requirement boxes about pointing, power, mass and energy, and at the bottom a row of boxes typed String (targetEntry, traceability, methods, environment, as I misread them at that size; they turned out to be ledgerEntry, recordEntry, testNode, environment). An Issues pane saying no issues. The shape told me "people at the top, measurements at the bottom, with a chain between"; the text told me nothing, it was unreadable.
>
> (b) WHAT EACH STAKEHOLDER CARES ABOUT, AS THE MODEL STATES IT
> Two stakeholders, two concern types.
> - Sponsor (me): "Pays for the mission and answers for it. Cares about price: what the cubesat costs to build and to launch (down), and how long it serves (up). Reads rolled-up measures, not the engineers' detail." Two concerns of type PriceConcern:
>   - lowCost: the cubesat costs little to build and to launch.
>   - longLife: the cubesat serves long; the battery's cycle life falls as its eclipse depth of discharge grows.
> - Operator: "Flies the cubesat. Cares about how it performs during its operational life: that it slews, settles and points as asked, and that its power and energy hold up." Two concerns of type PerformanceConcern:
>   - pointingAndSlewing: points the payload accurately, slews and settles in time, within what its wheels can store and give.
>   - powerAndEnergy: power and energy hold up through an orbit and through a slew in eclipse.
>
> (c) FOR EACH CONCERN, WHICH TRADE OR REQUIREMENT BEARS ON IT, AND WHERE I FOUND IT
> - lowCost → one requirement, launchBudget (LaunchBudgetRequirement): "the launch cost (the MoE on the traded metric total mass) is within budgets.launchBudget. It reads the configuration only." Found in the diagram (screen 5), the filtered table (8), the concern's own doc in the source (9), and the English statement in the requirements view (16). The concern's doc also says the cost to build is "an illustrative roll-up with no requirement on it": CostToBuild sums unit prices for bus, panels, battery, antenna, IMU, wheels and tracker (screen 14). So on my "build cost" concern there is a formula but no requirement and no check.
> - longLife → one requirement, depthOfDischarge (DepthOfDischargeRequirement): depth of discharge in eclipse, with the slew loss energy, over battery capacity, stays within the environment's allowed depth. Found at screens 5, 8, 9, 16. The "effective life" is again an illustrative roll-up (EffectiveLife: 10,000 reference cycles at 0.3 depth, inversely proportional, one cycle per orbit, converted to years), with "no requirement reads it" (screen 14).
> - pointingAndSlewing → four requirements: pointingError (configuration-only; the requirements view says outright "The baseline configuration fails it (0.0155 against 0.0085 degree)"), settled (settling time below the horizon of the nominal slew, measured), controlEffort (within budgets.controlEffortLimit, measured), momentum (peak wheel momentum within wheel class capacity). Screens 5, 8, 16.
> - powerAndEnergy → six requirements: power (panels cover housekeeping and tracker loads, configuration-only), powerMargin (not negative at the peak of the slew), energyBalance (over an orbit, not negative), peakSlewPower (within budgets.peakSlewPowerLimit), batteryPeakPower (eclipse peak load within the pack's discharge rating times capacity), eclipseDepthOfDischarge (the same DepthOfDischargeRequirement again; the doc says it serves both the operator's concern and my long-life concern, "the trace says so, not the requirement"). Screens 6, 8, 16.
> How each is checked (screens 11, 15): three requirements that need only the configuration (launchBudget, pointingError, power) are verified by configurationEvidence; the nine that need a measured slew are verified by slewEvidence. Both evidence cases point at the same ledger entry "v2-primary@8", the same container record ("Container regression at the WP23 close-out gate, 2026-11-10, image 877c42cc10e3, head 61cef31"), a named test each, and environment "877c42cc10e3". The quantities actually traded, as the requirement texts name them: total mass (through launch cost), pointing error, settling time, control effort, peak wheel momentum, power margin, energy balance, peak slew power, depth of discharge.
>
> (d) WOULD I TRUST THIS READING
> Partly, and the model itself tells me where to stop trusting it.
> What I trust: the structure is honest and narrow. Each of my concerns names exactly which engineering requirement serves it; the tool's own tables agree with the diagram and with the source text; the two things I would most want (build cost, service life) are explicitly labelled illustrative roll-ups with no requirement on them, rather than dressed up as checked. The tool is careful to say "Links are declarations, not verification results", and the cover note at the top of the file says plainly that this is "documentation of a demonstration, not an engineering model", that every number is illustrative and "never calibrated to hardware". The evidence cases point at a specific ledger entry, a dated container run, a test name and an image id: that is the shape of an audit trail, not a hand-wave.
> What I do not trust yet, as a sponsor: nothing in front of me shows a verdict. The matrix shows "Declared" twelve times and never "passed" or "failed". The one verdict I did see was in the engineers' requirement text: the baseline fails pointing error (0.0155 against 0.0085 degree), and the requirements view has one "not satisfy" edge, which matches. So the design I would be signing off on, as drawn, fails one of the operator's requirements, and I only learned that by reading a sentence inside a definition, not from the stakeholders view. The Satisfaction matrix had 0 linked elements for my twelve requirements, so the model does not say what in the design satisfies them; it says only what checks them. And the numbers I care about most (what is the launch budget in dollars, what is the cost to build, how many years is the effective life for the baseline) are nowhere on screen; the unit costs are invented by the engineers' own admission.
>
> (e) WHERE I GOT LOST OR STOPPED
> - Screen 3: my first toolbar click hid the diagram and gave me a page of source code; I expected a layout toggle, not a swap.
> - Screen 4: the stakeholders diagram at fit-to-window is unreadable; I expected to read at least the top row.
> - Screen 9: clicking a requirement in the table seemed to do nothing for a few seconds; I expected a detail card to open beside the table. It did eventually jump the source and tree, which was useful but is not where a sponsor looks.
> - Screens 12–13: selecting an element in the model tree highlighted it but moved nothing else; I expected the source or an inspector to follow. (The "Show Inspector" button existed; I did not get to it.)
> - Screen 17: I asked for the metrics view and still had the requirements view when I ran out of time; and the header's momentary "draft pending / Working..." with Apply source lit up made me nervous that I had changed something, though I had not typed into the source and it reverted to "Source applied".
>
> (f) WHAT I COULD NOT FIND
> - Any pass/fail result for the twelve requirements, per configuration or for the baseline, in the stakeholders view, the table or the matrix.
> - The numeric thresholds: budgets.launchBudget, pointingErrorLimit (I got 0.0085 degree only from a sentence), controlEffortLimit, peakSlewPowerLimit, the allowed depth of discharge (0.3 appears only in the battery-life note).
> - The evidence itself: the ledger entry "v2-primary@8", the container RECORD, and the two named tests are pointers to a repository I cannot open from here. The model says so: "The model carries the pointer; the repository carries the evidence."
> - What satisfies the requirements (Satisfaction matrix: 0 linked elements for these twelve).
> - A computed cost to build or effective life for any configuration; only the formulas.
> - The metrics view and the alternatives view, which I suspect are where the actual trade-offs between these quantities are drawn.
>
> (g) WHAT I WOULD ASK THE ENGINEERS NEXT
> 1. For the baseline and for whatever design you are asking me to fund: a one-page table of the twelve requirements with the measured value, the limit, and pass/fail, in the units a sponsor reads. The model says the baseline fails pointing error; what fixes it, and what does the fix cost in mass, power and dollars?
> 2. What is the launch budget in currency, what is the baseline's launch cost against it, and how much margin is left?
> 3. Cost to build and effective life are "illustrative, never calibrated". What would it take to replace the unit costs and the battery cycle-life rule with quoted or measured figures, and would you then put a requirement on each?
> 4. Depth of discharge serves both my long-life concern and the operator's power concern. If the operator wants deeper slews in eclipse, how many years of life do I give up? Show me that trade.
> 5. The evidence points at ledger entry v2-primary@8 and container image 877c42cc10e3 dated 2026-11-10. Who can open that record for me, and what did the two named tests actually report when they ran?
> 6. The tool shows what verifies each requirement but nothing that satisfies it. Is that a gap in the model or a choice, and if a choice, where do I look for "which part of the design meets this"?
> 7. Why did the diagram header flash "draft pending" while I was only clicking around? I want to be sure the model I was reading is the one you are reporting against.

### Dispositions (R-8)

| Point (the reader's words, short) | Disposition |
|---|---|
| (d), (f), (g)6: "nothing in front of me shows a verdict"; "Satisfaction matrix: 0 linked elements for these twelve"; the baseline's failure on pointing error learned "by reading a sentence inside a definition, not from the stakeholders view" | **Changed** (b9c8819): each concern's requirement carries the baseline configuration's verdict as a `satisfy` or `not satisfy` statement in `stakeholders.sysml`; the toolkit's engine checks all 23 statements of the three files and all hold; the Satisfaction matrix now shows the twelve rows against `cubesatBaseline`, 11 Declared and the pointing error's Negated declaration (step 11, `WP27-review/11-satisfaction-matrix-verdicts.jpg`). |
| (g)1 and (g)4, a verdict "for whatever design you are asking me to fund", and the trade between the operator's eclipse slews and the sponsor's life | **Changed** for the verdicts (73b4e89, L-8; the driver's decision of 16:20): the agile and compact configurations' verdicts on each concern's requirement are in `stakeholders.sysml`, engine-checked, and the Satisfaction matrix shows the three designs side by side (D-3, step 25). **To the driver** for the trade: the life-against-slew trade needs `EffectiveLife` traded (G-1, gate). |
| (f), (g)2: the thresholds' numbers and the roll-ups' computed values are not on screen | **Held, reason**: the editor shows no attribute values on nodes or in its tables (the researcher's F-1); an attribute usage per configuration for the roll-ups would draw as a node with its type and no number, so it would not answer the reader. The numbers are in the model (the launch budget 90,643 USD in `budgets`' doc; cost to build 216,200 USD and effective life 5.11 years for the baseline, D-2 L-2) and readable once the editor shows values. |
| (c), (g)3: the cost to build has a formula but no requirement and no check; the unit costs and the cycle-life rule are illustrative | **With the supervisor** (H-2, through the driver): a cost-to-build budget is his number; calibration is written down for the lifecycle demo, not built. |
| (f), (g)5: the evidence is pointers to a repository the reader cannot open | **By design**: the model carries the pointer, the repository the evidence (WP27-decisions.md, 14:10); the pointers resolve (`tests/test_verification_pointers.py`). That the editor shows neither the pointers' values nor a link is the researcher's feature request. |
| (a), (e) screens 3, 4, 9, 12-13, 17 and the "draft pending / Working..." flash while read-only; (g)7 | **To the researcher** (the editor's): sent by message with the screen numbers for its report. |
| (f): the metrics and alternatives views not reached | **No change**: the reader ran out of time on screen 17; the views render (WP26 steps 09, 20). |
| (b): what each stakeholder cares about | **No change**: read as the model states it. |

### WP26's gate-class findings against the sponsor's reading (the non-goal; to the driver)

Whether each of WP26's gate-class findings blocks the sponsor's reading, read against the P1 return. **T3** (verdicts
only on the baseline): it blocked the comparison of designs the reader asked for ((g)1) and is met for the twelve
concern requirements by 73b4e89 (L-8): the Satisfaction matrix shows the three configurations; the model's own eleven
`baseline...` requirements still carry the baseline's statements only, which the sponsor's path does not read. **T5**
(the MoE and MoP marks invisible in the editor): does not block; the reader named the traded quantities from the
requirement texts and never needed to tell a measure of effectiveness from a measure of performance. **N5** (two
requirement docs describe the generated picture): does not block; the reader quoted the requirement docs and read
their statements, though the clause "the behavioural view draws it with no line" is a sentence a sponsor cannot place.
**N6** (no short ids; the baseline requirements undocumented): does not block the path the reader took, since the
twelve concern rows name `concern::requirement` and the defs' docs are on the requirements view; it is the one of the
four that would have helped: the reader's screen 8 saw the Identifier and Documentation columns blank for the twelve
rows, and short ids on the defs would fill the Identifier column. The record of the four is the driver's.

## D-5. The sponsor-facing prose: none, by the negative-edit test

The reader's needs that prose could serve are (g)1 and (g)2: each requirement's value, limit and pass or fail, and
the launch budget in currency. The docs' case page already carries the requirements table read after the fit
(`docs/examples.md`, "Requirements read after the fit": pass shares per regime, the near-frontier designs each
excludes, the price in bands), and the baseline's verdicts are now in the model and the editor's matrix (D-4, first
row), where this reader looked. A pointer sentence in `examples/adcs/case-model.md` or `docs/examples.md` would not
have reached a reader who read the editor, and removing it would lose nothing this reader needed. D-5 is "none"
(R-9); the case and docs tests are untouched.

## The tensions, read against the concerns

The tensions the method reports for the case are the K = 1 contending sets of the fits of record
(`examples/adcs/case-model.md`, "What the fit returned on the data of record").

| Regime | Contending metric | Its requirement | Concern(s) | Stakeholder(s) |
|---|---|---|---|---|
| primary | total mass (0.358) | launch budget (through the launch cost) | lowCost | sponsor |
| primary | energy balance | energy balance | powerAndEnergy | operator |
| primary | pointing error | pointing error | pointingAndSlewing | operator |
| primary | depth of discharge | depth of discharge | longLife, powerAndEnergy | sponsor, operator |
| primary | settling time | settled | pointingAndSlewing | operator |
| baseline | control effort (0.432) | control effort | pointingAndSlewing | operator |
| baseline | settling time | settled | pointingAndSlewing | operator |
| baseline | power margin | power margin | powerAndEnergy | operator |
| baseline | pointing error | pointing error | pointingAndSlewing | operator |
| baseline | depth of discharge | depth of discharge | longLife, powerAndEnergy | sponsor, operator |

In the primary regime the contending set crosses the two stakeholders: the sponsor's low cost (the total mass)
trades against the operator's pointing, settling and energy; the depth of discharge sits on both sides (the
sponsor's long life and the operator's energy in eclipse). In the baseline regime every contending metric is the
operator's except the depth of discharge.

## Checks

At 28f7c9c and a4cde2f: `experiments verify` 0 drifts (39 entries, 11 current); the model tests with the pointer
test, `REQUIRE_OPENSYSML=1 uv run pytest tests/test_model_checking_v2.py tests/test_system_model_v2.py
tests/test_system_model_v2_r1.py tests/test_mutation_v2.py tests/test_model_coverage.py
tests/test_interface_contract.py tests/test_verification_pointers.py`: 224 passed; the coverage table regenerated
equals the committed one (no diff); the committed views are the generator's output (test); `check_vocabulary.py`:
0 new violations (69 exist on the base); `ruff check` clean. No change to `cubesat.sysml`, the
ledger, the data, the paper or the contract.

At 73b4e89 (L-8): `experiments verify` 0 drifts (49 entries, 11 current); `REQUIRE_OPENSYSML=1 uv run pytest -q -m "not
slow"` on every fast test file that reads the model (`test_case_model_howto`, `test_check_script`, `test_case`,
`test_cubesat_oracle`, `test_diagnostic_pair`, `test_model_coverage`, `test_mutation_v2`, `test_model_checking_v2`,
`test_paper`, `test_system_model_v2`, `test_system_model_v2_r1`, `test_v2_data`, `test_verification_pointers`) with
`test_interface_contract` and `test_docs`: 498 passed, 4 skipped; `check_vocabulary.py`: 0 new violations (69 on the
base); `ruff check` and `ruff format --check` clean. No change to `cubesat.sysml`, the ledger, the data, the paper or
the contract.

## For the lifecycle demo (written down, not built)

What the round met that serves the ADCS-lifecycle-demo's revision rather than this case, for that repository:

- The DEER layers as model elements: the evidence case's four pointers are the Evidence and Realization layers as
  strings; a lifecycle model would type them (a ledger entry, an image digest, a test) and resolve them from the
  model, not from a test in the repository.
- Verification cases per lifecycle stage (design, integration, operation), each with its own evidence; here one
  stage, the design trade, is shown.
- Stakeholders beyond two (launch provider, ground segment, payload owner) and their concerns.
- The roll-ups calibrated (cited unit costs, a cited cycle-life curve) rather than illustrative.

## Not done in this round

- The bug reproductions (one cold pass per bug, WP26's six and WP27's three): after the P1 reader (the PM's word).
  WP26's held in-file edits and the ledger re-run landed in the sequel (`WP26-model-changes.md`).
