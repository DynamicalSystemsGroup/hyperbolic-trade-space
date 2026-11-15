## Image alone

Title: none on the figure itself. Four framed groups labelled "(the analyst's grouping)": controls, power and energy, cost, mass.

Structure, left to right:
- Peach/orange boxes are requirements (bold name, then a tag such as SlewVerification or ConfigurationVerification; two say "not satisfied by cubesatBaseline").
- Green boxes are traded metrics, each with a stereotype («MoP» or «MoE») and a name. I count 13 green boxes.
- One yellow box, launch cost «MoE», is labelled in the legend as derived, not traded.
- A grey box, SlewMeasurement, says "measured slew: simulation here; field data when fielded".
- A purple box, SlewExperiment, is tagged «analysis def». Its text says it returns "10 of 13 metrics" and lists some of them, plus the unit and fleet cost analyses.
- Legend at the bottom: requirement, traded metric, derived, analysis, measurement; orange solid line = requirement reads metric; dotted line = computed from; grey arrow = value comes from.

Marks: orange solid lines join each requirement to one metric. Grey arrows run from the purple box and the grey measurement box into the green metrics. A dashed line joins total mass to launch cost.

One sentence: The figure links each requirement, grouped by subsystem, to the traded metric it reads, and shows that the slew experiment supplies most of those metrics.

Cannot read or understand:
- What "slew" and "cubesatBaseline" mean. Neither is defined on the figure.
- What the stereotypes «analysis def» and «MoE»/«MoP» mean beyond the one-word hint. Only the caption defines MoE and MoP, so I am reading them from the figure's context alone.
- The requirement thresholds, and whether any design passes them (not shown, by design).
- The six computed metrics that are not named in the purple box (momentum headroom, energy balance, power margin, battery peak power ratio, depth of discharge, peak slew power). Their box text does not say what they are computed from, and no grey arrow from the measurement reaches them.
- The count. The purple box says 10 of 13, but I count 11 arrows leaving it; the text does not explain how the two numbers relate.
- The legend's dotted "computed from" sample looks grey, while the dashed line in the figure looks orange. This may be a rendering or contrast artefact at this size.
- The arrows into unit cost and fleet cost are long and cross the mass frame, so I could not reliably trace them to their metrics at this resolution.

## With the caption

What the caption settles:
- It names the views: functional subsystems, MoE (read by the stakeholder) and MoP (read off the subsystems), and what the grey and orange lines mean. This answers my MoE/MoP and line-meaning questions.
- It explains the count: 11 arrows = nine computed metrics (three from configuration alone: pointing error, total mass, available power) plus two analyses (unit cost, fleet cost). The "10 of 13" adds control effort, which the experiment passes on from the measured slew. Settling time comes from the measurement directly. I can now reconcile the arrows with the text.
- It confirms the 13 traded metrics, the derived launch cost (dashed from total mass), the ConfigurationVerification versus SlewVerification tags, and the two "not satisfied by cubesatBaseline" notes. I checked each of these against the image and they match.

What the caption leaves unclear:
- It does not define "slew" or "cubesatBaseline", nor the «analysis def» stereotype.
- It does not say what the six computed metrics that are not named in the purple box are computed from. The caption says they are "computed", and the arrow count supports nine, but the slew dependency of those six is still not shown as an input. The caption says the experiment computes them; it does not say with what inputs.
- It says "the placement of a requirement in a subsystem is the analyst's reading". That matches the frame label, so it is not a gap, but it means the grouping is a reading, not a model fact.

What I still cannot read: the thresholds and pass/fail (the caption explicitly excludes them), the legend's dotted-line colour, and the long arrows at the bottom.

Does the one sentence change? It stands, with one refinement: "most" is now quantified (11 of 13 metrics leave the experiment box: nine computed plus two analyses). Its scope is still the figure's own view, not whether the designs pass.
