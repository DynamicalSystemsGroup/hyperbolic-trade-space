# fig-behavioural-view

## Q5

### (a) What the image shows (written before the caption)

A box-and-line diagram of a model (it looks like a SysML-style requirements view) for what appears to be a satellite attitude-control design. Eight green boxes are "traded metrics" (settling time, control effort, pointing error, energy balance, power margin, depth of discharge, peak slew power, total mass), sorted into three grey packages labelled "the analyst's grouping": controls, power and energy, mass. Each green metric has an orange requirement box joined to it by a solid line ("requirement reads metric"), and each requirement names how it is verified (SlewVerification or ConfigurationVerification; the pointing-error one is marked "not satisfied by cubesatBaseline"). A purple "SlewExperiment" analysis box on the right sends arrows ("value comes from") to most metrics; its text says it returns 7 of 8 metrics, two of them (pointing error, total mass) computed with no slew, and that control effort comes from the measurement and is passed on while settling time is not returned. A grey "SlewMeasurement" box (simulation now, field data later) sends arrows to settling time and control effort. In the mass package a yellow "launch cost" box is derived from total mass (dashed line) and is not traded; the launch-budget requirement reads launch cost. A dashed box at the top holds three requirements that read no traded metric (battery peak power, momentum, available power). A legend at the bottom explains colours and line styles.

### (b) After the caption

Mostly yes. The caption's claims can be checked on the image: requirements grouped into the three subsystems, an orange line from each requirement to the metric it reads, grey arrows from the measurement to settling time and control effort, grey arrows from the analysis to the other six, the pointing-error box marked as not satisfied by the baseline, total mass reaching its requirement only through the yellow launch cost, and the top box of requirements that read no traded metric.

One mismatch: the caption says the control effort is something "the analysis passes on", but no arrow shows it. The only arrow into control effort comes from SlewMeasurement, and the passing on appears only as text inside the purple box. The image also does not separate "computed from the configuration alone" (pointing error, total mass) from the other four analysis outputs. That too is only in the box's text.

What it does not show (beyond the caption's own "Does not show"): the thresholds, and which requirements act as feasibility filters and which are the four threshold requirements the text names (peak slew power, pointing error, control effort, launch cost). It also does not say what MoE and MoP mean. The legend does not cover them, and only the section text explains them. And it says nothing about either regime or about the fit.

### (c) The sentence test

Sentence: "Each of the eight traded metrics (controls: settling time, pointing error, control effort; power and energy: energy balance, power margin, depth of discharge, peak slew power; mass: total mass) is read by a requirement in the system model (total mass through the launch cost); settling time and control effort come from the simulated slew, the other six from the analysis."

The figure adds little that a reader of this paper needs beyond that sentence. Its extra content is the requirement and verification names, the MoE/MoP tags, the three requirements that read no traded metric, and the baseline's failure on pointing error. These are traceability details in a model-based systems engineering style. They help someone mapping the case onto their own system model, but they are not used later in the story.

## Q1

It traces each of the eight traded metrics to the requirement in the cubesat system model that reads it, grouped by subsystem, and to the measurement or analysis that supplies its value.

## Q2

At most, the abstract's "On a cubesat model coupling power, mass and attitude control, one term blends the subsystems' trade-offs into a single tension" and main result 7. Both lean on which metric belongs to which subsystem. But the sentence of Section 8 that lists the eight attributes by subsystem already supplies that grouping. The part only the figure carries (the requirements, their verification and the supply arrows) serves no sentence of the story.

## Q3

does not advance.

The story needs the cubesat's eight metrics and their grouping by subsystem, and the text of Section 8 already gives both in one sentence. What only this figure adds is the requirement-to-metric traceability, the MoE/MoP marking and the supply path of each value. No sentence of the abstract or Section 1 relies on any of it, and the fit ignores the requirements (Section 8 says so). It is useful context for a systems engineer, but the story does not need it.

## Q4

Not "repeats". For the record, the subsystem grouping it shows also appears in the text of Section 8 (unit sect-case-construction), in the sentence listing the eight attributes as controls, power and energy, and mass.

## Q9

- "returns 7 of 8 metrics ... settling time (not returned)" (purple box) against the caption's "the analysis passes on" the control effort. Where the settling time enters the table if the analysis does not return it, and why one measured value is passed on and the other is not, I could not place.
- "Every traded metric is read by a requirement" against "The fit ignores the four" threshold requirements and "Feasibility removes designs that do not settle, saturate the momentum budget or discharge the battery too deeply". I could not tell which boxes in the figure are feasibility filters, which are the four threshold requirements, and which are neither.
- "the launch cost and the pointing error are MoEs, the other seven traded metrics MoPs": launch cost is not traded, so "the other seven" took a second reading to reconcile with eight traded metrics.
