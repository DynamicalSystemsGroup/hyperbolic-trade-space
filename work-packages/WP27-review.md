# WP27 — Review: stakeholder concerns in the case model, in the view editor

The modeller's round (one modeller, the editor's tab of WP26, the step log `scratchpad/view-editor/wp27/steps.md`
with one screenshot per step; the screenshots this review cites are in `WP27-review/`). The scope is
`WP27-scope-of-work.md`; the decisions `WP27-decisions.md`. Sections: D-1 the parse check; D-2 the classed changes;
D-3 the trace as the editor shows it; the tensions read against the concerns; the checks; for the lifecycle demo.
D-4 (the P1 cold read), D-5 (the sponsor-facing prose) and D-6 (the feature requests, the UX researcher's) are not in
this round's modeller work: pending, see "Not done".

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

Cross-file reference works in both parsers: every chosen construct refers to `cubesat.sysml` from the separate
file, so the additions live in `stakeholders.sysml` and the model's bytes do not move. The two parsers disagree
twice (rows 10 and 13: the toolkit accepts, the editor rejects); the model uses only what both accept.

## D-2. The changes, classed

**Landed** (separate files; every output byte-identical; checks below at each commit):

| ID | Change | Commit |
|---|---|---|
| L-1 | `examples/adcs/model_v2/stakeholders.sysml`: the sponsor (price) and the operator (performance in operation) as parts typed by `Sponsor` and `Operator`; concern defs `PriceConcern`, `PerformanceConcern` (subject the cubesat, stakeholder); four concerns, each held by its stakeholder and holding the engineers' requirements that serve it: `lowCost` (launch budget), `longLife` (depth of discharge), `pointingAndSlewing` (pointing error, settled, control effort, momentum), `powerAndEnergy` (power, power margin, energy balance, peak slew power, battery peak power, eclipse depth of discharge). Every one of the model's eleven requirement defs serves at least one concern; the depth-of-discharge requirement serves both stakeholders | 28f7c9c, a4cde2f |
| L-2 | The roll-ups, each `doc` beginning "Illustrative roll-up" and naming its inputs: `CostToBuild` (illustrative unit costs on the parts the configuration swaps and tunes: 158,500 / 216,200 / 407,600 USD for the compact, baseline and agile configurations) and `EffectiveLife` (the depth of discharge by an illustrative cycle-life rule, 10,000 cycles at 0.3, one cycle per orbit: 2.65 / 5.11 / 8.57 years with the baseline's recorded slew); the launch cost is the model's own (71,944 / 79,749 / 93,960 USD). Read by no output (R-7, tested) | 28f7c9c |
| L-3 | The evidence cases: `EvidenceCase` (subject the cubesat; `ledgerEntry`, `recordEntry`, `testNode`, `environment`) and two usages, `configurationEvidence` (as `ConfigurationVerification`: launch budget, pointing error, power) and `slewEvidence` (as `SlewVerification`: the other eight), each verifying the concerns' requirements and pointing at `v2-primary@6`, the RECORD.md section of the data gate's regeneration, its test, and the host | 28f7c9c |
| L-4 | `views.sysml`: the view `stakeholders` (GeneralView exposing the stakeholders, the concerns with their members, the evidence cases with theirs, the roll-ups); `views.sysml` is now applied after `stakeholders.sysml` | 28f7c9c |
| L-5 | Tests: WP26's views test loads the three files; `test_stakeholders_file_loads_strictly_and_its_names_resolve` (R-1, negative control), `test_the_trace_from_who_cares_to_every_requirement_is_complete` (R-2), `test_the_rollups_are_illustrative_and_read_by_no_output` (R-7); `tests/test_verification_pointers.py` (R-6: ledger entry exists and is current, RECORD heading exists, the test node collects, the host entry names its platform; negative controls: an unknown entry, a superseded entry, an unknown heading, an unknown image) | 28f7c9c |
| L-6 | The operator's depth-of-discharge requirement named `eclipseDepthOfDischarge` (row 13 of D-1) | a4cde2f |

**Held** (judged right, not landed):

| ID | Change | Why held |
|---|---|---|
| H-1 | The requirement defs of `cubesat.sysml` each `frame` the concern they serve (D-1 row 5), so the trace is stated where the requirement is | in-file: waits for WP26's held edits and one host re-run after the gate's container regression (OD1 (b)); the separate file states the same trace now |
| H-2 | A requirement on the cost to build (the sponsor's `lowCost` has a requirement on the launch cost only) | needs a budget the supervisor chooses; none is invented |
| H-3 | Evidence cases for the baseline regime's dataset (`v2-baseline@6`) and the check experiments | one evidence entry per verification case is enough to show the chain; more on the driver's word |

**Gate** (anything an output reads; not landed):

| ID | Change | Gate |
|---|---|---|
| G-1 | The cost to build or the effective life as a traded metric | a new metric: the contract (`interface-contract.md` §14) and a regeneration |
| G-2 | The pointers name `v2-primary@6`, a host entry; when the close-out gate's container regression supersedes it, the pointer moves in the same unit (`tests/test_verification_pointers.py` fails until it does), and the record entry then names that regeneration's RECORD.md section | one line in the gate checklist (WP27-decisions.md, scope gate) |
| G-3 | Today the record pointer names the data gate's section (the container regeneration of the same experiments at `@5`): RECORD.md has no section for the host `@6` run | settled by G-2 at the gate |

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

The chain concern → requirement → verification case is readable in the editor; evidence → environment is in the
model (the pointers, tested) but not shown by the editor's tables or diagram: those gaps go to the researcher's
report (D-6) as feature requests.

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

- D-4, the P1 cold read: a fresh reader with its own tab, prompted as the scope's defaults say; not started by the
  modeller (the PM's to dispatch).
- D-5, the sponsor-facing prose: not drafted; decided after D-4.
- WP26's held in-file edits, the ledger re-run, the bug reproductions of the WP26 report: wait for the close-out
  gate's container regression (the PM's instruction).
