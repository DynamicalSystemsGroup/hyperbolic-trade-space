# fig-assembly-view

## Q5 (a) What the image shows (written before the caption)

A UML/SysML-style block diagram. A top box "Cubesat «part def»" is joined by filled-diamond (composition) lines to eight part boxes: ReactionWheel (wheel, abstract), Bus, SolarPanel (panelPlus, panelMinus), Battery, StarTracker (tracker, abstract), Antenna, Imu, Controller. ReactionWheel has a blue-less orange "swap wheelClass" tag and three hollow-triangle (specialisation) children: SmallWheel, MediumWheel, LargeWheel. StarTracker has an orange "swap grade" tag and children CoarseTracker, MediumTracker, FineTracker. SolarPanel has a blue "tune panelSpan", Battery a blue "tune batteryCapacity", Controller two blue tags "tune Kp" and "tune Kd". Bus, Antenna and Imu carry no tag. A legend box reads: swap = categorical, a part is swapped for one of its alternatives; tune = continuous, a parameter tuned within a range; untagged = fixed (Bus, Antenna, Imu).

## Q5 (b) After the caption

Yes, the image shows what the caption says: parts under the cubesat by filled diamond, alternatives of the two abstract parts by open triangle (the caption says "open arrow"), swap on wheel class and tracker grade, tune on panel span, battery capacity, Kp and Kd. The caption's own admission that the ranges are not drawn is true of the image. The image also shows what the caption does not mention: three parts are fixed (Bus, Antenna, Imu), and the names of the alternative levels (Small/Medium/Large, Coarse/Medium/Fine). It does not show: the ranges or the number of levels per variable, the physics, the attributes or metrics, which configurations were sampled or feasible, or how the parts couple (power, mass, attitude control). The "mass" and "power" coupling named in the abstract is not visible in it.

## Q5 (c) The sentence test

Sentence: "A configuration of the cubesat swaps the reaction wheel among small, medium and large and the star tracker among coarse, medium and fine, and tunes the panel span, battery capacity and controller gains Kp and Kd; the bus, antenna and IMU are fixed."

The figure conveys little more than this sentence. What it adds is the part-of structure (which parameter belongs to which part), the names of the fixed parts, and a mapping a reader could lay over their own system model; none of that is used by the rest of the story. Section 8's text already lists the six design variables.

## Q1

It conveys which parts of the cubesat model are swapped among alternatives, which are tuned continuously, and which are fixed, i.e. where the six configuration variables live in the part hierarchy.

## Q2

None directly. It sits under the setup for main-results item 7 ("On a cubesat model coupling power, mass and attitude control...") and the abstract's last sentence about the cubesat model, but those sentences are about terms separating contending sets, not about how the design variables are organized. The figure shows no coupling.

## Q3

Verdict: does not advance.

No sentence of the story needs it: the story's cubesat sentences concern what the terms separate, and the six design variables are already named in Section 8's first paragraph. The figure is a clear, correct map for someone mapping the case onto their own system model (its own "Good for" line), but that is not a sentence of the story.

## Q4

Not applicable (verdict is not "repeats"). Closest overlap: the opening paragraph of Section 8 (sect-case-construction), which lists the same variables in words.

## Q9

- "panelPlus, panelMinus" in the SolarPanel box: not explained anywhere I read.
- "(wheel)", "(tracker)", "(bus)", "(imu)" in lowercase under part names: presumably the usage names in the model, not explained.
- "«part def»" and "«abstract»": modelling-language notation not explained in the caption or text.
- The caption says "open arrow" while the image draws hollow triangles: a small mismatch, not a barrier.
