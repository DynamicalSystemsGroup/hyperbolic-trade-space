# WP27 — Decision records (the stakeholder layer of the case model: concerns, "who cares", the abstraction jump)

## Origin (2026-11-10, 14:00)

**Supervisor (mzargham), verbatim,** with two screenshots on how SysML v2 models stakeholders and their needs
(stakeholders as parts; needs as concerns framing the subject; traceability from a stakeholder-needs concern to the
requirements): "in order to close a loop with a sponsor for a project i want my sysmlv2 model to be able to express
stakeholder needs as concerns and to have an option to trace all the back to "who cares" via this tool. see
screenshots. / that's the extreme sponsor facing side of the model. we can split it and keep it simple one
stakeholder is a deeply tied to price (getting the cubsat cost to build and cost to launch down and its effective
life up), another cares about its performance during its operational life. / this is a realistic "the final
stakeholders care about very rolled up metrics" and the engineers doing the trade study are trying to get them what
they want in a rigorous and reproducible way, including addressing genuine tensions between requirements that may
live at a level of detail that really matters to the design engineers but is not itself interesting to the sponsor.
managing the abstraction jump from the technical details from domain engineers, to the systems engineer to the
sponsors is a main benefit of executable approaches. / note we are not jamming all this in our paper, we're just
fleshing out the test case our paper uses as a means of convincing ourselves our approach really is useful in
practice. we cannot just dump a pile of analysis on a sponsor's desk, they just don't care to sift through it" and
then: "this can be a follow up work package for the modeler agent".

**Disposition.** A follow-up package to WP26 for the modeller agent, WP27, scoped by the PM for the driver's approval
after WP26's round closes. Content from his words: two stakeholders in the model (one tied to price: cost to build
and cost to launch down, effective life up; one tied to performance during the operational life); their needs as
concerns that frame the subject (the cubesat) and the stakeholder parts; the trace from each concern to the
requirements it motivates, from the requirements to the metrics and from the metrics to the calcs, readable in the
view editor (a stakeholder view and the traceability matrix) so "who cares" is one navigation; the rolled-up
measures the sponsor reads derived from the engineers' measures (launch cost exists; cost to build and effective
life are illustrative roll-ups from the parts and the battery's depth of discharge, stated as such); the tensions
between detailed requirements kept at the engineers' level with the trace saying which concern each serves. The
modeller first checks what the parsers accept (SysML v2's own `concern def`, `concern`, `frame` and `stakeholder`
constructs against the toolkit's strict load and the editor), and uses what parses. Any roll-up that becomes a
traded metric goes through the data gate; concerns, stakeholders and traces that leave the outputs byte-identical
land under WP26's rule. The paper's narrative takes none of it; the case prose and the docs' case page carry the
sponsor-facing reading if the round shows it earns its place.

**Supervisor (mzargham), verbatim, a minute later:** "it will help us determine whether our model is "useful" / "good
enough"". **Disposition:** this is WP27's definition of good: the case model is useful when a sponsor can follow the
trace from their own concern down to the trade the engineers made and back, and when the tensions the method
reports are the ones a concern cares about; "good enough" is judged by that reading in the view editor (a cold
reader in the sponsor's persona, P1, navigates from "who cares" to the metrics and says what they learned), not by
the count of model elements.

**Supervisor (mzargham), verbatim (14:10):** "also at the detailed end of this we do want to explicitly use
verification cases and track where evidence is logged and track what environments or images were used to produce
that evidence. insofar as the view editor does not yet support that we should include the gaps in our UX feedback.
you can read about how i think about this computational engineer stack on this webpage:
https://dynamicalsystemsgroup.github.io/ADCS-lifecycle-demo/#framework / eventually i expect we'll rework that other
repo based on what we learn here. but i am maintaining a seperation of concerns. our current work is building a
model that serves as the numerical case for the HTS research, when we go back to the ADCS-lifecycle demo repo we'll
be focused on the sysmlv2 model itself and hts will just be a dependency / does that make sense. we're sitting right
at the intersection of the two projects right now so we need to be a little careful about scope creep. i want the
model we build here to be the numerical demonstrator for the HTS peice first and just an input to the next major
revision of the ADCS-lifecycle-demo project"

**Disposition.** Two additions to WP27 and one guard. (1) The detailed end: the model's verification cases are used
explicitly, each pointing at where its evidence is logged (the ledger entry id, the RECORD.md entry, the test that
reads it) and at the environment that produced it (the image id of record, or the host when a tolerance branch is
the evidence); the model carries the pointer, the repository carries the evidence; the trace then runs from a
stakeholder's concern through requirement and verification case to evidence and environment. (2) Where the view
editor cannot show that chain (verification cases have no renderer today; no evidence or environment field in its
tables), the gap goes into the UX researcher's report as a feature request with the reproduction. (3) The guard: the
model built here is the numerical demonstrator for the method first; what serves only the ADCS-lifecycle-demo's
revision is written down as a note for that repository (a section of the WP27 review, "for the lifecycle demo"),
not built here. HTS becomes a dependency of that repository later; nothing here anticipates it.

**His framework page, read (the DEER layers of the engineering record):** Declaration (architecture and
requirements in SysML v2), Execution (scenarios, behavioural models and analysis pipelines in a Git repository),
Evidence (datasets from measurements, simulations and analyses in append-only stores, each tagged with its Git
SHA), Realization (cloud infrastructure and Docker images in an artifact registry); contradictory evidence is
expected. WP27's scope uses these words for the chain: a verification case (Declaration) names its analysis
(Execution), its evidence record (Evidence: the ledger entry and its hash) and the image that produced it
(Realization). The page names no trade studies or HTS; that is the separation he keeps.
