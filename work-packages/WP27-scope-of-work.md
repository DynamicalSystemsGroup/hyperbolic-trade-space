# WP27 — Scope of work: stakeholder concerns in the case model, in the view editor

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` when the driver judges it merits CI |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`, "The mandate"), quoted verbatim in `work-packages/WP27-decisions.md`, section "Scope gate" *(default heading)* |
| **Acceptance record** | The supervisor's verbal acceptance, quoted verbatim in `work-packages/WP27-decisions.md`, after the PM's review of D-1 to D-7 |

**Header note.** A follow-up to WP26 for the modeller agent (`WP27-decisions.md`, "Origin": "this can be a follow up
work package for the modeller agent"), with WP26's UX researcher for D-6 and a fresh cold reader for D-4. IDs are new
to this package. Drafted 2026-11-10 from `origin/dev` at 2ce3c14. Sources: the supervisor's words, verbatim, and their
dispositions in `work-packages/WP27-decisions.md` ("Origin", 14:00 and 14:10, and the framework page read); the
direction as the driver relayed it to the PM (quoted below). The parent's rules apply as recorded in
`WP26-decisions.md`: OD1 (b) (in-file changes that leave every output byte-identical land through one host re-run of
the five ledger entries, each output's hash equal to the one before, or the change stays held) and the sequencing with
the gate (that re-run waits for the gate's container regression and runs against its entries).

## Purpose

The supervisor, verbatim (2026-11-10, `WP27-decisions.md`, "Origin"): "in order to close a loop with a sponsor for a
project i want my sysmlv2 model to be able to express stakeholder needs as concerns and to have an option to trace all
the back to "who cares" via this tool. [...] we can split it and keep it simple one stakeholder is a deeply tied to
price (getting the cubsat cost to build and cost to launch down and its effective life up), another cares about its
performance during its operational life. [...] managing the abstraction jump from the technical details from domain
engineers, to the systems engineer to the sponsors is a main benefit of executable approaches. / note we are not
jamming all this in our paper, we're just fleshing out the test case our paper uses as a means of convincing ourselves
our approach really is useful in practice." And: "it will help us determine whether our model is "useful" / "good
enough"".

The direction, as the driver relayed it (2026-11-10): "the case model expresses stakeholder needs as concerns and
traces everything back to 'who cares' in the view editor. Keep it simple: two stakeholders, one tied to price (cost to
build and cost to launch down, effective life up), one tied to performance during the operational life; their needs
as concerns framing the cubesat and the stakeholder parts; the trace from concern to requirement to metric to calc
readable in the editor (a stakeholder view and the traceability matrix); the sponsor's rolled-up measures derived from
the engineers' measures (launch cost exists; cost to build and effective life as illustrative roll-ups, stated so);
the engineers' detailed requirements and their tensions kept at their level with the trace saying which concern each
serves. The modeller first checks what parses (SysML v2's own concern def, concern, frame and stakeholder constructs
against the toolkit's strict load and the editor) and uses that. Roll-ups that become traded metrics go through the
data gate; byte-identical additions land under WP26's rule. The paper takes none of it; the case prose and the docs
page carry the sponsor-facing reading if it earns its place."

The detailed end and the guard (the supervisor, 14:10, verbatim in `WP27-decisions.md`; the disposition's words): the
model's verification cases are used explicitly, each pointing at where its evidence is logged (the ledger entry id,
the RECORD.md entry, the test that reads it) and at the environment that produced it (the image id of record, or the
host when a tolerance branch is the evidence); the model carries the pointer, the repository the evidence; the trace
runs concern → requirement → verification case → evidence → environment (the DEER layers of his framework page:
Declaration, Execution, Evidence, Realization). Where the editor cannot show that chain, the UX researcher's report
carries the gap as a feature request with the reproduction. The model built here is "the numerical demonstrator for
the HTS peice first and just an input to the next major revision of the ADCS-lifecycle-demo project"; what serves only
that revision is written down, not built.

## Goals

- G1. **What parses, first.** SysML v2's own `concern def`, `concern`, `frame` and `stakeholder` constructs (and the
  relationships the trace needs) are checked against the toolkit's strict load and the view editor, and the model uses
  only what both accept (the relay: "The modeller first checks what parses ... and uses that").
- G2. **Who cares, in the model.** Two stakeholders: one tied to price (cost to build and cost to launch down,
  effective life up), one tied to performance during the operational life; their needs as concerns framing the
  cubesat and the stakeholder parts; every one of the model's requirements traced to the concern it serves, the
  engineers' requirements and their tensions kept at their own level (the supervisor, "Origin"; the relay).
- G3. **The sponsor's measures rolled up from the engineers'.** Launch cost (in the model) and two illustrative
  roll-ups, cost to build (from the parts) and effective life (from the battery's depth of discharge), each stated as
  illustrative; none becomes a traded metric in this package (the relay; "Origin", disposition).
- G4. **The detailed end: verification cases with evidence and environment.** Each verification case points at its
  evidence (ledger entry id, RECORD.md entry, the test that reads it) and its environment (image id of record, or the
  host); the pointers resolve (the supervisor, 14:10, and its disposition).
- G5. **The trace readable in the editor, and judged there.** A stakeholder view and the traceability matrix let a
  reader go from "who cares" to the metrics and calcs; a cold reader in the sponsor's persona (P1 of
  `docs/superpowers/notes/reader-grid.md`) does so and says what they learned (the definition of good, "Origin").
- G6. **The editor's gaps as feature requests.** What the editor cannot show of the chain concern → requirement →
  verification case → evidence → environment reaches the editor's author as feature requests with reproductions
  (the supervisor, 14:10).
- G7. **The guard written down.** What serves only the ADCS-lifecycle-demo's revision is a "for the lifecycle demo"
  section of the review, not built (the supervisor, 14:10, and its disposition).

## Non-goals

- The paper: no change under `paper/` (the supervisor: "we are not jamming all this in our paper").
- No new traded metric, and no roll-up read by the oracle, the coverage table, the generator, the data or the
  contract, without the data gate: a roll-up that should become a traded metric is written up as a gate unit for the
  driver's go (a contract amendment, `interface-contract.md` §14, and a regeneration), not done here.
- No change to the data of record or to any output; in-file model changes only under WP26's OD1 (b) rule.
- The ADCS-lifecycle-demo's features: anything that serves only its revision (its repository's structure, the model as
  its own product, HTS as its dependency) is a section of the review, not built (G7).
- The editor's own code: the package reports to the editor's author (D-6), it does not change the editor.
- No account and no sign-in on the editor; nothing of the repository goes to the editor except the model files.
- WP26's gate-class findings (T3 satisfy statements only on the baseline, T5 the MoE/MoP marks invisible in the
  editor, N5, N6 requirement short ids) stay WP26's gate units; D-4 records whether any of them blocks the sponsor's
  reading, and that record goes to the driver.
- No glossary entry: a glossary entry regenerates Appendix A (`pm5-rules.md`), which is the paper's output.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | **The parse check**, recorded as the first section of `work-packages/WP27-review.md` *(default)*: a table of each construct tried (`concern def`, `concern`, `frame`, `stakeholder`, the relationship that ties a requirement to its concern, a verification case usage, and the form the pointers take), each with the toolkit's strict load result and the editor's issues count and rendering (as the WP26 harness, `docs/superpowers/notes/view-editor-harness.md`, reads them), and the construct chosen for each job | G1 |
| D-2 | **The model additions**, each committed with its checks and classed as WP26 classes them (landed byte-identical / held / gate): the two stakeholders; their concerns framing the cubesat and the stakeholder parts; each requirement traced to its concern; the stakeholder view (in `views.sysml`); the roll-ups as illustrative derived measures; the verification cases with their evidence and environment pointers. In a file of their own beside the model, `examples/adcs/model_v2/stakeholders.sysml` *(default)*, applied after `cubesat.sysml` as one model, wherever D-1 shows the construct works across files; inside `cubesat.sysml` only under WP26's OD1 (b) rule; with a toolkit test of the trace and of the pointers (R-2, R-6, R-7) | G2, G3, G4 |
| D-3 | **The sponsor's trace in the editor**: screenshots of the stakeholder view and of the traceability matrix (and the requirements table) on the applied model, with the harness's readings as data, in the review and `work-packages/WP27-review/` *(default)* | G5 |
| D-4 | **The P1 cold read in the editor**: a fresh reader in the sponsor's persona, image first, then navigating from "who cares" to the metrics in the editor; their return verbatim in the review, each point with a disposition (changed, held with reason, or to the driver) | G5 |
| D-5 | **The sponsor-facing reading in prose, only if it earns its place**: a passage in `examples/adcs/case-model.md` and `docs/examples.md`, each sentence kept only if removing it loses something the P1 read needed (the negative-edit test); "none" is an acceptable outcome, recorded with its reason | G5 |
| D-6 | **Feature requests for the chain the editor cannot show** (verification cases with no renderer, no evidence or environment field in the tables, any other gap D-1 to D-4 meet), written by the UX researcher with a reproduction each, in the researcher's report (`work-packages/WP26-view-editor-feedback.md` as a section, or `work-packages/WP27-view-editor-feedback.md` if that report is closed) *(default)* | G6 |
| D-7 | **The review**, `work-packages/WP27-review.md`: D-1, the classed changes list, D-3, D-4, the tensions-to-concerns table (each tension the method reports for the case, and the concerns its metrics trace to), the checks' results, and the section "For the lifecycle demo" | G2, G5, G7 |
| D-8 | **The decision records**, `work-packages/WP27-decisions.md` (the driver writes it): the scope gate, the driver's go for any gate-class unit, the supervisor's acceptance, verbatim | all |

## Requirements

`<start>` is the `dev` head at approval; it is named in the scope gate's record.

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The toolkit's strict load passes on the model with every added file, and every added name resolves | `REQUIRE_OPENSYSML=1 uv run pytest tests/test_system_model_v2.py` with a test that loads `cubesat.sysml`, `views.sysml` and the added file as one model strictly and finds each stakeholder, concern, verification case and view *(default: beside WP26's views test)*; a negative control (a misspelt name fails the load) |
| R-2 | The trace is complete: every concern is held by a stakeholder and reached by at least one requirement; each of the model's requirements traces to at least one concern; each traded metric's requirement reaches a concern | the test of R-1 walks the trace through the toolkit and asserts each clause |
| R-3 | The editor applies the model with all its files at 0 issues, and the stakeholder view renders (a diagram or a populated table) | the harness's §3 and §4 readings and screenshots in D-3 ("No issues in the current applied model"; `unavailable` false), read by the PM |
| R-4 | Every output stays byte-identical, and the model's gates and pins pass, after every landed unit | `PYTHONPATH=examples/adcs uv run python -m experiments verify` prints "0 drifts"; `REQUIRE_OPENSYSML=1 uv run pytest tests/test_model_checking_v2.py tests/test_system_model_v2.py tests/test_system_model_v2_r1.py tests/test_mutation_v2.py tests/test_model_coverage.py tests/test_interface_contract.py`; the coverage table and committed views as WP26 R-3 checks them |
| R-5 | An in-file change to `cubesat.sysml` lands only under WP26's OD1 (b) rule: one host re-run of the five entries after the gate's container regression has landed, each output's hash equal to its predecessor's, else held | `uv run python examples/adcs/model_v2/ledger_gate.py --host` with the WP27 note; `experiments verify` 0 drifts after it; the changes list against `git log <start>..HEAD -- examples/adcs/model_v2/cubesat.sysml` |
| R-6 | Every verification case's pointers resolve: the ledger entry id exists in `examples/adcs/experiments/ledger/ledger.jsonl` and is the current entry of its experiment; the RECORD.md entry's heading exists in `paper/container/RECORD.md`; the test exists (`uv run pytest --collect-only -q <node id>` collects it); the image id appears in RECORD.md as an image of `hts-paper`, or the environment is the host and the ledger entry's `platform` field names it | a test, `tests/test_verification_pointers.py` *(default)*, reading the pointers from the model through the toolkit; a negative control (an unknown ledger id fails) |
| R-7 | The roll-ups are stated as illustrative and read by no output: each roll-up's `doc` says illustrative and names what it rolls up; no roll-up name appears in the oracle, the coverage table, the generator, the data or the contract | read; `grep` of the roll-up names over `examples/adcs/*.py`, `examples/adcs/model_v2/coverage.py`, `docs/superpowers/notes/spike-sysml-diagrams/project.py`, `examples/adcs/data/`, `work-packages/interface-contract.toml` finds none; R-4 |
| R-8 | The P1 read's return is recorded verbatim with a disposition per point; the reader saw the stakeholder view's image before navigating and had no repository access | the review's D-4 section with the prompt quoted; read by the PM |
| R-9 | D-5 passes the negative-edit test, or is "none" with its reason; the case prose and docs tests pass | the review lists each added sentence and what removing it loses; `uv run pytest tests/test_case_model_howto.py tests/test_docs.py` |
| R-10 | Each D-6 feature request has numbered steps from the editor's landing page, the expected and observed behaviour, a screenshot, and carries no internal project detail beyond what a reproduction needs | read; WP26 R-8's `grep` over the report finds nothing a reproduction does not need |
| R-11 | One object, one name: the glossary's terms in `doc`s, the review and any D-5 prose | `uv run python scripts/check_vocabulary.py` exits 0 |
| R-12 | The seam holds: only the blast radius changes; nothing for the lifecycle demo is built; no AI attribution on any commit or file | `git diff --stat <start>..HEAD`; the review's "For the lifecycle demo" section read against the diff; `git log <start>..HEAD --format=%B \| grep -iE "co-authored\|generated by\|claude"` returns nothing |

## Blast radius

The files this package may change; anything else is a stop and a question to the PM.

- The modeller: `examples/adcs/model_v2/stakeholders.sysml` (new) *(default)*; `examples/adcs/model_v2/views.sysml`
  (the stakeholder view); `examples/adcs/model_v2/cubesat.sysml` only under WP26's OD1 (b) rule;
  `examples/adcs/model_v2/views/*` only through the generator, and
  `docs/superpowers/notes/spike-sysml-diagrams/project.py` only if a name it reads changed; the model tests' pins
  (`tests/test_model_checking_v2.py`, `tests/test_system_model_v2.py`, `tests/test_system_model_v2_r1.py`,
  `tests/test_mutation_v2.py`, `tests/test_model_coverage.py`), never weakened; `tests/test_verification_pointers.py`
  (new) *(default)*; under the OD1 (b) rule only, `examples/adcs/experiments/ledger/ledger.jsonl` (the five re-run
  entries), `examples/adcs/model_v2/ledger_gate.py` (the WP27 note) and `examples/adcs/model_v2/views/coverage.md`
  (the model-hash line); for D-5 only, `examples/adcs/case-model.md` and `docs/examples.md`;
  `work-packages/WP27-review.md` and `work-packages/WP27-review/`; the scratch folder `scratchpad/view-editor/wp27/`.
- The UX researcher: its report (D-6) and that report's screenshot folder.
- The PM and the driver: `work-packages/WP27-decisions.md`, this file (amendments only).
- Never: the data, the paper, `src/`, `derivation/`, `glossary.yaml`, `claims_register.toml`; never
  `work-packages/interface-contract.*`, unless a roll-up becomes a traded metric, which is a gate unit on the driver's go.

## Definition of good

The supervisor's, as recorded (`WP27-decisions.md`, "Origin", disposition): the case model is useful when a sponsor can
follow the trace from their own concern down to the trade the engineers made and back, and when the tensions the
method reports are the ones a concern cares about. The detailed end reaches the evidence: from a concern through its
requirement and verification case to the ledger entry, the test and the environment that produced it, with the model
carrying the pointer and the repository the evidence.

## Definition of good enough

Judged by the reading in the view editor, not by counting model elements (the supervisor, "Origin", disposition):

- D-1 is recorded, and D-2's landed units pass R-1, R-2, R-4, R-6 and R-7 at their commits; every in-file change is
  landed under R-5 or listed as held or gate.
- The applied model shows 0 issues in the editor, and the stakeholder view and the traceability matrix are in D-3
  (R-3).
- The P1 cold reader, in the editor, goes from "who cares" to the metrics and says what they learned; the return is
  recorded with dispositions (R-8), and no disposition leaves a point the reader could not follow unanswered (each is
  changed, held with its reason, or with the driver).
- The tensions-to-concerns table is in the review.
- D-5 is decided by R-9; D-6 meets R-10; the review has its "For the lifecycle demo" section; R-11 and R-12 hold.
  Stop there and present to the PM.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

One item for the driver's approval. Each is marked *(default)* where it appears, or is stated here.

- **The two stakeholders' names:** `sponsor` (price: cost to build, cost to launch, effective life) and `operator`
  (performance during the operational life), as parts typed by stakeholder part defs, renamed if D-1 or the glossary's
  terms say otherwise.
- **The roll-up formulas, marked illustrative:** cost to build, the sum of illustrative unit costs on the parts;
  effective life, the battery's cycle life at its eclipse depth of discharge from an illustrative cycle-life rule
  (the environment's 0.3 maximum depth of discharge is its anchor); launch cost as it stands. Each `doc` begins
  "Illustrative", names its inputs, and claims no cited price or life.
- **The stakeholder view's definition:** a `GeneralView` in `views.sysml` exposing the stakeholders, their concerns
  and the requirements that serve them, filtered to those kinds as D-1 finds the editor draws them; the
  traceability matrix and requirements table read as the editor offers them.
- **The pointer syntax inside the model:** a `doc` or attributes on each verification case (ledger id, RECORD
  heading, test node id, image id or "host"), as the parse check decides; the test of R-6 reads whichever is chosen.
  A pointer names the current ledger entry; when a gate's re-run supersedes it, the pointer is updated in the same
  unit (the test fails until it is), so the driver's gate gains that one line.
- **Where the additions live:** their own file (`stakeholders.sysml`) beside the model so the model's bytes and the
  ledger's model hash do not move, wherever D-1 shows cross-file reference works in both parsers; otherwise in
  `cubesat.sysml` under OD1 (b).
- **The P1 reader's prompt shape:** a fresh agent with no repository access, the persona row of P1 from
  `reader-grid.md` ("The accountable decision maker": domain judgement, little time, no convex analysis; wants "to
  know what trades against what, and whether to trust the method"), the stakeholder view's image first and a request
  to say what it shows, then its own browser tab on the editor's project (harness §1) to navigate from "who cares" to
  the metrics, and three questions: what each stakeholder cares about, which engineering trade bears on it, and
  whether they would trust the reading; return verbatim.
- **Sequencing:** WP27 starts after WP26's round closes (the WP26 modeller's tab passes to WP27); the separate-file
  units may land outside a gate's container-regression window; in-file units wait until WP26's held edits have landed
  after the regression, then go through one host re-run of their own.
- **The agents:** the modeller (drives its tab, owns D-1 to D-3 and D-7), the UX researcher (observes, owns D-6), the
  P1 cold reader (D-4, its own tab); one round; the step log `scratchpad/view-editor/wp27/steps.md` with one
  screenshot per step, as WP26's.
- **Names and placement:** the review `WP27-review.md` with D-1, D-3 and D-4 as its sections and the screenshots in
  `WP27-review/`; D-6 as a section of the WP26 researcher's report if still open, else its own file; the decisions
  heading "Scope gate".
- **The tensions read:** the tensions the method reports for the case as its committed outputs state them
  (`tension_report` on the fits of record), each mapped through the trace to the concerns its metrics serve; the
  source of each tension cited in the review.

## Open decisions

None. The trace check found no problem-level item: every goal, non-goal, deliverable and check traces to the
supervisor's words or their dispositions in `WP27-decisions.md`, to WP26's recorded rules, or to the Agent's defaults
above, which go to the driver as one item.
