# WP26 — Decision records (the model in the view editor: a modeller and a UX researcher)

## Origin (2026-11-10, 11:20)

**Supervisor (mzargham), verbatim:** "i want you to have the PM scope and deploy 2 agents to collaborate; one is
tasked with using the view editor to further improve the quality of the model for our papers case. i see the view
editor as enabling constraints plus a useful integrated modeling environment that helps us ensure our sysmlv2
model is conformant, intuitive, interpretable and aligned with our intents. it will help us make the most of the
sysmlv2 affordances without requiring open ended exploration of text. the other agents job is to sit over the
shoulder of the modeler and doing UX research. the second agents output is a report for the person who built the
view editor aimed at providing productive and constructive feedback covering what worked well, what didn't work
well and logging bugs if and when they are encountered, as well as documenting workarounds. the reason i need 2
agents is i want each to have clearly scoped deliverables which are distinct. the modeler is going to improve our
model, the UX reseacher captures feedback for the provider of the view editor."

Context: the editor at https://openmbee-view-editor.vercel.app/app holds the project "cubesat" with the full
`examples/adcs/model_v2/cubesat.sysml` applied verbatim (the loading recipe in the session scratchpad,
`view-editor/`); the first exploration found it parses with no issues and renders no diagram because the model has
no `view` package. **Disposition:** one package, WP26, scoped by the PM for the driver's approval, two agents with
distinct deliverables: the modeller's are model changes in the repository (a change that alters any calc or
output goes through the data gate after the close-out; a change that leaves every output byte-identical lands
freely, verified by the toolkit gates and the ledger at 0 drifts); the researcher's is
`work-packages/WP26-view-editor-feedback.md`, written for the editor's author. One browser, one driver: the
researcher observes through milestones, screenshots and short interviews.

## Scope approved; OD1 (2026-11-10, 12:40; the driver)

`WP26-scope-of-work.md` (74b2402). **OD1, in-file changes to `cubesat.sysml` that leave every output byte-identical:**
(b). They land this round through one host re-run of the five ledger entries at the round's end (`@7`, with a WP26
note); each output's hash must equal its `@6` hash, or the change reverts to held; the ledger, the gate's note and
the coverage table's hash line join the blast radius. A doc edit that improves the model's readability is the
point of the package and must not wait on a data gate it cannot affect; the hash equality is the proof it did not.
The `view` package lives in its own file. **Approved for execution by the driver under the mandate**; the two agents
deploy; the Agent's defaults as one item.

## Computer-use access and a minimal harness (2026-11-10, 13:10)

**Supervisor (mzargham), verbatim:** "i just saw and gave a claude subprocess access to my computer in a manner that
should support the modeling and UX work. if we need to we can build minimum viable harness for managing the view
editor work loops since that needs to pass through reading from and writing to the view editor not by editing
text and code files."

**Disposition.** WP26 gains one deliverable: a minimal harness for the editor loops in the repository
(`docs/superpowers/notes/view-editor-harness.md`, with its snippets, or `scripts/view_editor/` if more than a page):
load a source file verbatim into a named project file (the chunked insert with length and checksum), apply and read
the issues panel, list the views with their render status, read the requirements table and the traceability matrix
as data, capture a named view's canvas to an image, export or import the project through the native file dialog.
Written by the modeller from its step log at the round's end; cited by the researcher's report as the reproduction
path. Computer-use access is used only for the editor's native file dialogs; the browser pane's tools do the rest.

**Ledger sequencing with the close-out gate (2026-11-10, 13:15; the driver, answering the modeller directly).**
The container regression at the close-out gate writes the ledger's next entries if it re-pins; the modeller's host
re-run for byte-identical in-file edits (OD1 b) waits until that regression has landed, then runs against the
container's re-pinned outputs as the baseline and writes the entries after it, hash-equal or the edits stay held.
Unit 1 (views.sysml and its parse test) is on dev at d793a95. The harness deliverable is the modeller's, written
from its step log at the round's end.

**OD1 (b) amended (2026-11-10, 15:05; the driver).** Now that the entries of record are the container's (@7, image
877c42cc10e3), a host re-run cannot reproduce their bytes (the platform step difference registered as CR-2), so a
host re-run can no longer land an in-file model edit. The rule becomes: a byte-identical in-file edit lands through
a container re-run of the five ledger entries only (`ledger_gate.py --image`, about ten minutes in `hts-paper`, a
container named hts-<stream>, removed after) on the edited model, each output hash equal to the @7 hash, the entries
landing as the next numbers with the WP26 note; otherwise the edit reverts to held. A host run with no entries
written remains the cheap evidence of neutrality before the container run. The modeller's unit runs it; the
driver's gate regression is unaffected.
