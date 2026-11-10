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
