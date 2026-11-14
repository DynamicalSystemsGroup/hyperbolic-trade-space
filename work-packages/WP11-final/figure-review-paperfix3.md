# Figure review of the final reader round, third paper unit: Figures 3, 4, 5, 6 and 7

The loop is `docs/superpowers/notes/figure-review.md`; the second unit's record for Figures 4 and 5 is
`figure-review-paperfix2.md`. Images are in `figure-loop/` (`figN_before.png`, `figN_after.png`), as rendered by the
committed code at this unit's head. Readers' words are quoted from the committed reports in `reports/` through the
triage files.

**What this record does not contain.** The loop's step 3, the cold read by fresh-context viewers, is not here: this unit
had no sub-agents and no fresh reader. Each figure's brief for that read is at the end of its section (image alone first,
then the caption; the sentence of test 2 is what the reader's one sentence is compared with). The PM runs the cold reads.
**Cold reads needed:** Figure 4 and Figure 5 (redrawn by the second unit, test 1 still open), Figure 7 (panel titles
changed, image regenerated), Figure 3 and Figure 6 (caption-only changes: the read asks whether the caption now says what
the image shows, and for Figure 6 whether a reader finds the designs above the line). Figure 8's caption gloss (request
132) needs no read of its own.

Dispositions follow the loop's order: keep, caption, resize, redraw, drop. Each change is reverted by reverting the
commit.

## Figure 3: the behavioural view of the cubesat model (requests 26, 88, 152)

**Recipe.** Question: which traded metric does each requirement read, and what supplies each metric. Intended takeaway:
thirteen requirements each read one of the thirteen traded metrics, grouped by subsystem; the launch budget requirement
reads the launch cost, which is derived from the total mass and is not traded. Sentence of test 2: "Each of the thirteen
requirements reads one metric (the launch budget reads the derived launch cost, computed from the total mass), and one
experiment or measurement supplies each metric." The sentence carries the count and the exception but not the grouping,
the tags that say when a requirement can be checked, or which metric each experiment supplies: kept.

**The readers on the figure before** (`figure-loop/fig3_before.png`, caption of c42d860 and the second unit's):

- Twelve cells (wave 5, request 26): the caption's rule "an orange line from each to the traded metric it reads" holds
  for twelve boxes and fails for the launch budget requirement, whose orange line ends at the launch cost, not at a
  traded metric.
- Three cells (wave 6, request 152): "The total mass is read through the launch cost" reads reversed against the dashed
  arrow, which runs from the total mass to the launch cost.
- G25 (wave 5): "thirteen requirement boxes against six" is the count of requirements, which the text beside the figure
  now separates (four feasibility conditions, six read after the fit).

**Disposition: caption.** The image is the model's own view (`examples/adcs/model_v2/views/`) and a redraw would be a
model change; the two readings are the caption's. The rule now says "the metric it reads", and the launch exception is
named: the launch budget requirement reads the launch cost (yellow, derived, not traded), which is computed from the total
mass (the dashed arrow). The image is unchanged (`fig3_after.png` is `fig3_before.png`).

**The tests.** (2) Sentence: above; the figure is not redundant. (3) Ink: tall (about 700 by 1,700 pixels), about half the
frame is boxes and text, the rest is the grey subsystem frames; the arrows from the two experiments cross the right half
and are the one place where lines cover each other. (4) Legible at the column width: the box text is the model's and is
readable at the page's width when the figure is opened full size; at column width the small tag lines
(`ConfigurationVerification`) are at the edge. (5) The three lines beside the figure on the page (unchanged).

**Verdict: caption; test 1 pending.** Brief for the cold read: give the image alone ("this is a figure from a paper on
trade studies of a small satellite; say in one sentence what it shows and what you take from it"), then the caption, and
ask which sentence of the caption the reader checked against the picture and whether the orange line to the yellow box
read as an exception or as an error.

## Figure 4's lower panel: the temperature sweep (requests 56, 140)

The second unit redrew the lower panel as one line per metric (`figure-review-paperfix2.md`, before and after in
`figure-loop/fig4_before.png`, `fig4_after.png`; the image is unchanged in this unit). Request 140 is the caption's: the
rings mark the sweep point nearest the fit temperature (the sweep's grid has a point at 42.06 against the fit
temperature 41.72, D.1 and D.2), and a ring is not the fit. The caption says so without printing the values (a typed value
with three decimals fails the repository's rule against typed generated numbers; the values are in D.1 and D.2).

**Disposition: caption (the figure is the second unit's redraw).** **Verdict: tests 2 to 5 as the second unit judged
them; test 1 on the redraw pending.** Brief for the cold read: image alone ("what do the five lines that rise or fall
show; where is the fit temperature"), then the caption; the question that matters is whether the reader finds the one line
that leaves the support (total mass) and the ring's place on the curve, and whether "the sweep point nearest" is read as a
distinction that matters.

## Figure 5: the K = 1 plane of available power and unit cost (requests 36, 94)

The second unit's redraw (`fig5_before.png`, `fig5_after.png`) puts every design on the line's slice; nothing changes in
this unit's image. Request 94's alt text is the caption's first sentence (below). **Verdict: tests 2 to 5 as the second
unit judged them; test 1 pending.** Brief for the cold read: image alone ("is the line an edge of the cloud, and on which
side are the designs"), then the caption; compare with the nine readers of the figure before, none of whom read an edge.

## Figure 6: the chart of the K = 2 fit (requests 41, 27, 89, 141)

**Recipe.** Question: where along the main trade do the designs reach the surface, and how deep inside do they fall.
Intended takeaway: the surface is the flat line log V = 0 whatever the position; most designs lie below it; about a tenth
lie above it, which is the fit's convention. Sentence of test 2: "In the K = 2 chart the surface is a flat line, the
designs lie mostly below it, about a tenth (203 of 2,134) above, and the depth does not depend on the position." Nothing
is lost by the sentence's numbers, but the picture shows the depth's spread and its position dependence, which the
sentence only asserts: kept.

**The readers on the figure before** (`figure-loop/fig6_before.png`):

- Two readers (wave 6, request 141): "I see no design above the line."
- Request 41's cells: the axis's "better" read as a ranking; the level not named.
- G06 (wave 5): "the fraction above zero not countable by eye".

**What the data say** (computed in this unit from the fit of record, `case.k_fits(study)`): at K = 2 the fit's temperature
is 113.2 and 203 of the 2,134 feasible designs have log V above zero, 0.0951, within 0.01 of the target 0.10 (D.2 prints
0.09513). So the convention holds and the figure's data are right. The reason readers see none is in the drawing: the 203
designs above the line lie within about 0.05 of it on an axis that runs to -0.5, the line is drawn over the points, and
the points are small; they read as the line's thickness.

**Disposition: caption first.** The caption now names the level plotted (log V of the K = 2 fit), says the surface is the
line by construction, and says a tenth of the designs lie above it, the fit's convention. The smallest next step, if a cold
read of the caption still finds none above the line: draw the line under the points and give the top of the axis room
(a resize of the axis and a z-order, not a redraw of the idea). Not done here, since the loop asks for the caption first
and a read of it.

**The tests.** (2) Sentence: above. (3) Ink: about 70 percent of the frame carries designs; the band is one thin grey
strip. (4) Legible at the column width: the axis labels are two lines and read; the x label names three metrics.
(5) The three lines beside the figure (unchanged).

**Verdict: caption; test 1 pending.** Brief for the cold read: image alone ("what is the black line, and where are the
designs relative to it"), then the caption; record whether the reader counts, or sees, designs above the line before and
after the caption.

## Figure 7: association among each term's near-frontier designs (requests 87, 153, 94, 42)

**Recipe.** Question: which metrics trade (negative association) among the near-frontier designs of each term's cell, and
which metrics are in each term's contending set, with what exponents. Intended takeaway: at K = 2, peak slew power, which
carries no exponent at K = 1, leads term 1 (0.43) against pointing error (association -0.97), so term 1 blends tensions
the one-term fit reports as one; term 2 has a different contending set led by other metrics. Sentence of test 2: "At K = 2
term 1's contending set of eight metrics is led by peak slew power, which trades against pointing error, and term 2's of
seven metrics by other metrics; the associations are those of each cell's near-frontier designs." The sentence carries the
lead and one trade; the matrices carry the others (unit cost against total mass, power margin and energy balance as one
axis): kept.

**The readers on the figure before** (`figure-loop/fig7_before.png`):

- G25 (wave 5): counted eight black labels in term 2's panel against "7-lemma" in its title: total mass at w = 0.01 is
  black (above the participation threshold 0.001) and not outlined (not in the exact-maximum support), which the caption
  states (a black label need not be outlined).
- Request 153 (wave 6): the panel titles say "exact-maximum support" where the caption says "contending set"; one name.
- Request 87 (wave 4): the outlines' weight at render size.
- Request 94 (wave 5): the image's alt text is the matplotlib repr.

**Disposition: retitle (a redraw of two strings), the alt text by the build.** The panel titles now read "term 1: 8-lemma
(8 metrics in the contending set)", the caption's and Definition 6's name. The alt text is the caption's first sentence,
set where the notebook is executed (`paper/execute_notebooks.py`, test
`test_inline_figures_have_their_caption_as_alt_text`). The 8-against-7 count is not changed: it is what the figure
shows (a black label is an exponent above the participation threshold at the fit temperature, an outline a member of the
exact-maximum support) and the caption says so. The outlines' weight is thick enough at the page's width (the second
image, `fig7_after.png`).

**The tests.** (2) Sentence: above. (3) Ink: both panels are full matrices, about 85 percent of the frame carries values;
the colour bar repeats on both panels. (4) Legible at the column width: the cell values (two decimals) are small but
readable full size; the metric labels with w are the carrying labels and read. (5) The three lines beside the figure.

**Verdict: retitled; test 1 pending.** Brief for the cold read: image alone ("which metrics trade in each panel; what do
the outlines and the grey labels mean"), then the caption; the question that matters is whether a reader takes the two
panels as the same designs split in two or as two sets of designs, and whether "contending set" and the outlines read as
one object.

## Figure 8: the two triples (request 132; no loop)

The caption now glosses "favours X" at a corner (that metric's share of the triple's total is largest) and says a region's
label names its leading pair where the third exponent is small. The root page's figure, which shares the word, is the
supervisor's surface and is not touched.
