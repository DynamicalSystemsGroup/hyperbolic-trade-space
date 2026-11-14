# Cold-read briefs, third paper unit (test 1 of the figure-review loop)

Each brief is for a fresh-context reader (at least two per figure, different personas where the reader grid applies):
give the image alone, ask for one sentence on what it shows and what they take from it, then give the caption (the
paper's, in `paper/paper.ipynb`, cell `fig-*-caption`) and ask whether it changed the reading. Compare the first sentence
with the sentence of test 2 in `../figure-review-paperfix3.md` (Figures 3, 6, 7) and `../figure-review-paperfix2.md`
(Figures 4, 5). Images: `figN_before.png` is the figure at dev 40a93f2, `figN_after.png` at this unit's head.

Cold read needed: Figure 7 (retitled and regenerated), Figure 3 and Figure 6 (caption changes only; the image is unchanged).
Figures 4 and 5 had their test 1 at 40a93f2 (`../figure-review-paperfix2.md`); the briefs below for them are kept for a
second read if the PM wants one after the caption and label changes of this unit.

**Figure 3** (`fig3_after.png`; the model's behavioural view). "This is a figure from a paper on trade studies of a small
satellite. Say in one sentence what it shows." Then the caption. Record whether the orange line from the launch budget
requirement to the yellow box reads as an exception the caption names or as an error, and which way the reader takes the
dashed arrow (the launch cost is computed from the total mass).

**Figure 4** (`fig4_after.png`; the temperature sweep). Image alone: "what do the lines in the lower panel show; where is the
fit temperature on the upper panel's curves". Then the caption. Record whether the reader finds the one line that leaves the
support, and whether the ring is read as the fit or as the nearest sweep point (the caption now says the second).

**Figure 5** (`fig5_after.png`; the K = 1 plane). Image alone: "is the line an edge of the cloud, and on which side are the
designs". Then the caption. The nine readers of the figure before (`fig5_before.png`) read no edge; the redraw is judged on
whether these readers do.

**Figure 6** (`fig6_after.png`; the K = 2 chart). Image alone: "what is the black line, and where are the designs relative to
it; roughly what share lie above it". Then the caption, which says about a tenth lie above (203 of 2,134). Record the share the
reader estimates before and after. If the reader still sees none above the line after the caption, the next step is to draw
the line under the points and give the top of the axis room (a z-order and an axis limit, not a new idea).

**Figure 7** (`fig7_after.png`; association among each term's near-frontier designs). Image alone: "which metrics trade in
each panel; what do the outlines and the grey labels mean". Then the caption. Record whether the two panels read as one set of
designs split in two (the cells of the two terms) or as two sets, whether the outlines and the panel titles ("contending set")
read as one object, and whether the eight black labels in the second panel against its 7-lemma title is found and
explained by the caption.
