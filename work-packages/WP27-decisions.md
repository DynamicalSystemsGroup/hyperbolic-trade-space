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
