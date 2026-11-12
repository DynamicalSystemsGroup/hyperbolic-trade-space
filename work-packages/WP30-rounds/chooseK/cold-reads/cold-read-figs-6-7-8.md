# Cold read of Figures 6, 7, 8 (K = 2) and Figure 3's caption, as rendered on the paper page

Stage read: http://localhost:8791/paper/ (assistant's stage, K = 2 figures confirmed in the served page),
own browser tab, captions hidden for the cold read and then restored. Worktree: pm-worktrees/coldfig
(origin/dev at 95f6f5d, which contains 755e151). Column width: images render at 800 px on the 913 px
desktop viewport; 351 px at 375 px (no horizontal scroll, scrollWidth 375). Screenshots are in this folder.

## Figure 6 (planes, screenshots fig6-desktop.jpg, fig6-375px.jpg)

Cold read: two scatter panels of designs in dark and light grey, each with one straight sloping line.
The bottom is a dense cloud the line runs through; the top is designs on a few columns and bands with a
line that crosses them. I took the line to be a limit the designs press against, readable in the bottom
panel and not in the top.

Surrounding text and caption: the caption explains the lattice in the top panel (three pointing-error
groups, six bands, the large wheel's lower cloud) but only after the reader has had to decode it.

Sentence test: bottom panel passes ("term 2 trades available power against unit cost, and the designs
fall on and below its line"). Top panel: "term 1's line crosses a lattice of grade-by-wheel combinations"
is a statement about the lattice, not about a trade-off.

Ink as data: bottom panel is nearly all data. Top panel is about 40 percent empty, the band between
the upper bands and the large-wheel cloud (y from -0.8 to 0.2 at x below 0.3) carries nothing, and the
line's left half runs over blank space.

Legibility: axis labels and legend readable at column width; at 375 px the axis text is small but
readable, the legend text is not (the supervisor's rule: a phone is not required).

Shows and does not show: the page's "Shows/Does not show" line is accurate for the bottom panel.

Chief engineer's question, checked. Data (term 1, K = 2, planes.py): pointing error has 2109 distinct
values but falls in three groups (two narrow columns, one wide band); peak slew power has 100 distinct
values, seven levels in the figure. Verdict: AGREE that the top panel does not read as a trade-off the
designs trace, because both axes are set by discrete grades and the slope cannot be read from columns.
PARTLY DISAGREE with "a bound floating above sparse clusters": the line is not above everything. It
touches the dark designs at about 0.3 to 0.42 for log pointing error 1.0 to 1.8, straddles the medium
columns (0.85 and 0.7 against a line at about 0.75) and sits above the coarse column (line about 1.4,
designs at 1.35 and 1.15). It is a line through a lattice, touching at the right, not a floating bound.
The bottom panel reads as intended: the cloud falls on and below the line, with the single "term 2"
label.

Smallest fixes, in the order asked:
1. A different second metric for term 1. Tried (term 1's slice redrawn with `planes.py`'s pair overridden; alt-term1-pointing-vs-unitcost.png,
   alt-term1-slew-vs-unitcost.png): pointing error against unit cost (term 1's third-heaviest, 0.12)
   makes the vertical axis continuous and the dark designs hug term 1's segment on the right, but the
   horizontal axis stays in three columns, and term 2 owns the line's left half, so the panel then carries
   two terms. Peak slew power against unit cost is worse: seven vertical stripes. Pointing error against
   available power (tried, not kept) is the same three columns. So no second metric removes the lattice,
   because both of term 1's two heaviest metrics are grade-driven; the pointing-error and unit-cost slice
   is an improvement, not a cure, and it breaks the "two heaviest metrics" rule the caption states.
2. Drop the top panel and carry it in a sentence, for example: "Term 1 trades pointing error against peak
   slew power (association -0.97, Figure 8); both are set by discrete tracker and wheel grades, so its
   plane is a lattice of design classes, not a cloud." Figure 8 already carries the number; what the top
   panel adds beyond that (the line's position over the lattice) is not something the text relies on.
   Dropping leaves a one-panel figure of term 2, so Figure 6 then needs its caption and its reading
   (one plane per term) re-worded, or the figure retired in favour of Figure 5's K = 1 plane plus the
   sentence.
No caption caveat is proposed.

## Figure 7 (chart, screenshot fig7-desktop.jpg)

Cold read: designs plotted by level against position along an axis; a flat line at zero with a thin grey
band under it; nearly all designs lie below the line, thickest at middle and right, a thin fringe at the
left. I took it that designs rarely exceed the surface and sit closest to it toward the middle.

Caption: two rendered contradictions. (a) The x-axis label inside the image says the right is "better
unit cost, total mass and peak slew power", while the caption says "to the right, better total mass and
control effort, worse pointing error". One of the two is stale; both cannot hold. (b) The page's
"Does not show" line says "the other six directions of position" for thirteen metrics (twelve other
directions). Both are found by reading the rendered page, not the PNG. I did not trace which is
current (the loadings are in Appendix D.16).
Sentence test: "the designs reach the surface in the middle and right of the main direction of spread and
fall deepest at the far left" passes; the figure shows a shape the sentence only names.
Ink as data: about 60 percent of the frame is data; the legend sits in empty lower left; one design
dot sits under the legend text near "V = 0". Legibility: fine at column width and 375 px.
Verdict: figure succeeds; fix the axis-label or caption mismatch and the "six" count before
anything else.

## Figure 8 (association, screenshots fig8-term1-desktop.jpg, fig8-term2-desktop.jpg)

Cold read: two 13 by 13 correlation grids, purple for positive, orange for negative, black outlines on
some diagonal cells; a block of strong purple among power metrics, and a few strong orange cells. I took
it as which metrics pull against each other inside each term.
Caption: the caption fixes the reading (association among near-frontier designs, outlined = contending
set, w and grey explained) and corrects the possible false cluster reading.
Sentence test: passes: "within term 1's designs pointing error and peak slew power trade almost
perfectly (-0.97); within term 2 settling time and control effort do (-0.89)". It also supports Figure 6's
top-panel pair: the strongest tension in term 1 is exactly the pair drawn there.
Ink as data: dense, all cells informative. Legibility: values are about 7 px at column width, legible; at
375 px the cell values are not (an "enlarge" link exists). Diagonal outlines are visible. Shows and does
not show: accurate.
Note: Figure 6's bottom pair (available power and unit cost) has association -0.49 in term 2, a mild
tension, which is why that cloud is diffuse; the figures agree.

## Figure 3's caption (screenshots fig3-desktop-a.jpg, fig3-desktop-b.jpg)

The picture itself is current: four subsystem groups (controls, power and energy, cost, mass), thirteen
metrics, and the experiment box reading "returns 10 of 13 metrics". The caption is stale: "the eight
metrics are what the trade study trades", "which computes the other six ... and so returns seven of the
eight", subsystems listed as three. The picture and the caption disagree on the page.
Proposed caption (sentence test: one claim, the thirteen metrics each traced to its requirement and supplier):

"The behavioural view of the cubesat model: its requirements by functional subsystem (controls, power and
energy, cost, mass), an orange line from each to the traded metric it reads (thirteen metrics are traded),
and grey lines from what supplies each metric: the slew experiment returns ten of the thirteen, three of
them (the pointing error, total mass and available power) from the configuration alone; the settling time
comes from the measured slew directly, and the unit cost and fleet cost from an analysis each. The
pointing-error and unit-cost requirements' boxes say that the baseline configuration does not satisfy
them. Every traded metric is read by a requirement, the total mass through the launch cost (yellow:
derived, not traded); top: requirements that read no traded metric. Names are read from the system
model; the placement of a requirement in a subsystem is the analyst's reading."

Unverified: I read the image down to the mass group; the "top: requirements that read no traded metric"
sentence and the page's "Shows" line were not checked against the lower part of the image, and the
claim about which requirements are unsatisfied is read from the two boxes visible (pointing error,
unit cost). The "Shows" line carries no count and needs no change.
