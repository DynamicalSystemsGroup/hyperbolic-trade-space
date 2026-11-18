# Fourth paper unit (fix4): cold reads of Figures 3 and 6

One fresh Haiku reader per figure, image alone first, then the caption. No repository, no hint. Images checked byte-identical to the committed files (Figure 3: paper/figures/fig-behavioural-view.png; Figure 6: paper/figures/fig-chart-level.png). Full reports: fix4-fig3-reader.md, fix4-fig6-reader.md.

## Figure 3 (behavioural view)

Read: requirements by subsystem read the thirteen traded metrics through orange lines; grey arrows show supply; the slew experiment supplies most (11 arrows, box text says 10 of 13). Sentence given: the figure links each requirement to the traded metric it reads and shows the slew experiment supplies most of them. With the caption: the 11-arrow and 10-of-13 counts reconcile, MoE/MoP and the line meanings are settled; the sentence stands with "most" as 11 of 13.
Sentence test: met. Ink as data: met (the counts match the caption). Left unread: "slew", "cubesatBaseline", the analysis-definition tag; the slew input to six computed metrics has no arrow from the measurement.

## Figure 6 (chart level)

Read: grey dots, position along the surface against log V, black line at 0, a near-frontier band below it; sentence given from the image alone was the dots lying mostly inside the surface. Share above the line: the reader said a few percent, possibly up to about a tenth. With the caption: the surface at log V = 0 by construction, above the line V > 1, position a description and not a model variable; its sentence became "about a tenth lie beyond the surface, the rest inside, and the position axis describes spread, not a model variable".
Sentence test: met after the caption. Ink as data: met for the line and the band; the share above the line is only partly legible from the image (estimate wavered between a few percent and a tenth; the caption supplies about a tenth, 203 of 2,134). Not readable from the image: near-frontier definition and band width, the 36%, the axis origin and sign, the x units. The reader noticed a V-bar versus V notation mismatch between axis label and caption.

## Requests

- Figure 6: put the count on the figure (for example "203 of 2,134 above the line", or a count beside the line), so the share does not depend on the caption.
- Figure 6: make the y-axis label read log V exactly as the caption writes it (no bar).
- Figure 6: say what near-frontier means in the caption, or point to where it is defined.
- Figure 3: no change requested; optionally give an arrow from the measurement for the slew inputs.
