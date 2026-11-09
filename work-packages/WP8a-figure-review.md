# WP8a: docsite figure review (P8)

Method: `docs/superpowers/notes/figure-review.md`. Scope: the nine figures `scripts/build_figures.py`
builds from the runnable blocks of `docs/*.md` and `docs/user-guide/*.md` (the root page's are separate).
Judged at the commit `76e2f31` (rendered PNGs of `scripts/build_figures.py`, light scheme at 673 to 870 px
wide). Nothing on any page, script or test is changed; these are proposals for the driver's dispositions.

Cold reads: two fresh sub-readers (A: calculus and linear algebra engineer; B: convex-optimization
paper reader) were each given only the nine images, renamed `img1..img9`, then the captions. Their
sentences are quoted in compressed form below; full text is in the P8 session transcript.

Limits of this pass, stated plainly: the dark scheme and the 375 px width were NOT inspected in the
browser. The 375 px verdicts are computed from pixel sizes (a 673 px image shown at 345 px is at 0.51 of
native, an 870 px heatmap at 0.40) and the dark verdicts are assumed from the shared drawing code; the
driver should look. Ink share is my reading of the rendered images.

Page numbering finding: figures are numbered 1 (getting-started), 2 (fitting), 3 (tensions), 4 and 5
(chart), 6 to 9 (examples), so the user-guide order is 4, 5, 2, 3 against the numbers; and the Figure 7
alt text and caption of Figure 5 say "red" for markers drawn orange.

## Figure 7 first: `plot_frontier_coordinates` (adcs-coordinates)

The supervisor: "this one feels a bit hard to read. it doesn't really seem to reveal the frontier
clearly, but maybe that's not the point. we need more clarity about what specific plots show and dont
show and what they are good for."

Recipe: `chart = fit.estimator.transform(study.M)`; Z = first two of nine position coordinates, log V =
last column; 706 designs; ring where log V >= -0.1 (the plotting default band).

The driver's reading, tested:

- "Looks straight down onto the fitted surface, the frontier is the whole plane": supported by the
  construction (log V is a column the plot omits; the plane Z0-Z1 is a slice through the nine-dimensional
  position space, every point in it has some depth). Nothing in the picture tells a reader that.
- "Depth appears only as the rings": true, and the rings are weak: 212 of 706 designs (30 percent) are
  ringed because the band used (0.1) is four times the fit's own band (0.026, 96 designs); a third of
  the cloud ringed is not a frontier signal. Rings and dots overlap; 6 of 10 reader sentences cannot say
  what a ring means without the caption.
- "Coverage and white space": yes, this is what it can honestly show; it shows no frontier.
- "Axes are the first two of nine coordinates of a fixed basis and mean nothing by themselves": supported.
  Z0 correlates with the design variables Kp (-0.67) and Kd (+0.48) but that is incidental.
- The stripes: Z1 separates the star-tracker grade: mean Z1 coarse +0.87 (n=253), medium -0.04 (n=241),
  fine -0.99 (n=212); within-group sd about 0.7, against an overall sd of 1.05. So the bands are the
  star-tracker grade (a discrete design variable), but they overlap; "stripes" is a visual impression of
  three overlapping bands, and the wheel class loads on Z1 too (large +0.50, medium +0.02, small -0.73).

Cold reads of the present figure: A: "A Z0/Z1 scatter (a 2D embedding) of blue points with some circled
in black, which form a roughly crescent/triangular shape ... I could not tell what Z is, and what the
black rings mean; there is no legend." B: "a subset ringed in black outline ... the Z axes are undefined
(PCA? the fitted transform?)". Caption helped on the rings ("yes"), not on Z.

Sentence test: "The designs spread over a roughly crescent region of the chart; those nearest the
frontier are not confined to one part of it." A reader loses little by keeping the sentence. Ink: about
60 percent of the frame carries points; about 30 percent of the points carry rings, which makes the
ringed ones look like the main mass, not a subset. Legibility: fine at column width; at 375 px markers
at 0.5 scale are just visible, the rings merge. No colour reliance beyond ring versus no ring.

Candidates (script: `docs/superpowers/notes/figure-candidates/figure7_candidates.py`; images beside it):

(a) `fig7-a-depth.png`. Recipe: `plot_frontier_coordinates` with only Z0, so log V is the vertical axis,
frontier as the line log V = 0, band shaded. Takeaway: depth is on the page, and the arch is visible
at once: designs on the left of Z0 are all deep (log V down to -0.65), the frontier is touched only for
Z0 between about -0.5 and 0.7, and at the right the cloud spreads from 0.1 above to -0.9 below. It also
shows designs above 0 (log V > 0), which the ring plot cannot. Shows: where along Z0 designs reach the
frontier, and how deep the rest are. Does not show: any other coordinate (Z1..Z8 are summed over); what
Z0 means physically. Good for: seeing that the frontier is reached only over part of the position range.
Cold reads: not run (candidates are the driver's to dispose first).

(b) `fig7-b-principal.png`. Recipe: the tension report's own principal directions of the near-frontier
designs (`case._reports(...)[0].tension_directions`, band 0.026, 96 designs), all 706 designs grey,
near ones blue; axes named by the three leading loadings (direction 1, 46 percent of spread: pointing
error +0.43, total mass -0.42, peak slew power -0.41; direction 2, 21 percent: depth of discharge +0.52,
total mass -0.46, slew time -0.39). Takeaway: near-frontier designs spread across the whole cloud's
range of both directions, so the frontier is not a small corner of the space. Honest finding: it is a
weak figure; a trade-off between pointing error and mass/slew power is named, nothing is revealed
about the frontier shape. Shows: the spread of near-frontier designs along the metric trade-offs.
Does not show: log V; anything outside the near-frontier set's two leading directions (67 percent of its
spread). Good for: naming what the near-frontier designs trade on, in the metrics' words.

(c) `fig7-c-stripes.png`. Recipe: the present plot, coloured by star-tracker grade (coarse, medium, fine,
colour-blind-safe palette), rings as before. Takeaway: Z1 orders the designs by tracker grade; the
bands are a design variable's footprint. Shows: that the position coordinates carry design structure.
Does not show: depth beyond the rings, or any frontier. Good for: a reader asking what Z1 is.

Proposed three lines for the page beside (a), if it replaces the figure: Shows: log V of every design
against the first position coordinate, the frontier as the line at zero. Does not show: the other eight
coordinates, or what the coordinate means in the metrics. Good for: seeing where along the frontier
designs reach it, and how far the others fall short.
For the present figure, if kept: Shows: where the 706 designs sit in the first two position
coordinates, the nearest-frontier ringed. Does not show: the frontier (it is the whole plane here) or
how far inside a design is, except as a ring. Good for: spotting coverage and white space, not judging
the frontier.

Disposition proposed: rework (replace by (a); (c) can follow it as a one-line aside if the supervisor wants
the stripes explained).

## The other eight

Per figure: recipe, intended takeaway (written before the reads), cold reads, tests, three lines,
verdict. Reader A and B agreed unless noted.

### Figure 1: first-fit (getting-started)

Recipe: `plot_log_plane(ts2, X2, band=0.5)` on seeded two-metric synthetic data. Takeaway: a fitted
straight frontier with the data below and a band of near ones. Sentence: "The fit is a straight line in the
log plane above all designs but a few." Cold reads: A "Scatter of log m1 vs log m0 with a black line
'frontier V = 1' and a grey band ... a trade-off frontier ... unsure: what V is"; B the same, "the wide
band makes it look loosely fit". Caption: both "yes, helps; V still undefined". Tests: the sentence
test is passed (a picture of a line and cloud is shorter than its sentence); ink about 50 percent, one
far outlier near (-9,-9) squeezes the axes so the cloud uses half the frame; at 375 px legible except
the legend. Three lines. Shows: two metrics in log space, the fitted frontier V = 1 and the near band.
Does not show: what V measures, or any design variable. Good for: seeing the straight-frontier model in
the simplest case. Verdict: keep one of 1 and 4 (they are the same plot, bands 0.5 and 0.05); rework:
clip the outlier or say it, and show the band width in the legend.

### Figure 4: log-plane (chart)

Same function, band 0.05 (`plot_log_plane(ts2, X2)`); caption "the band below it has width 1/tau". Cold
reads: A "a better-fitted frontier that the data actually touches"; B "I cannot tell whether this is
the same data refit or a narrower threshold." That is a finding: two figures that look alike and read
as different fits. Sentence test: fails against Figure 1 (duplicate). Verdict: drop (or fold into 1 with
the two bands as one figure's two panels); tau stays defined in the text.

### Figure 2: three-facets (fitting)

Recipe: `plot_log_plane` of a K = 3 fit, facet-coloured. Takeaway: a bent frontier as the envelope of
three straight lines. Cold reads: A "three coloured facets ... a bent line follows the upper-right
envelope ... facet 2 orange and green overlap heavily"; B "two segments ... facet 2 overlaps the others".
Caption resolved the one-model question. Ink: good (the bend is the point, a sentence cannot show it).
Legibility: palette is orange, green, blue distinguished by colour alone; at 375 px the facet overlap is
worse. Lines. Shows: how three straight facets make a bent frontier in log space. Does not show:
which facet a design "belongs to" beyond colour, or the facets' exponents. Good for: seeing K > 1 as an
envelope. Verdict: keep; add a facet legend and different marker shapes per facet (a redraw).

### Figure 3: tension-report (tensions)

Recipe: `plot_tensions(report, names=[m0,m1,m2])`, the 3x3 matrix. Takeaway: all three pairs are
traded. Cold reads: A "all off-diagonals negative (-0.38 to -0.62), each pair trades off"; B the same.
"Association" undefined for both; the diagonal-only outlines puzzle them (caption resolves). Sentence
test: "All three pairs of metrics are negatively associated." The sentence carries it; a three-by-three
heatmap is borderline. Ink: nine cells, all information. Legibility: 576 px wide, shown at 0.6 on a
phone: cell text about 8 px. Lines. Shows: pairwise association among the metrics near the frontier,
and which are contending. Does not show: the size of the tension in the metrics' units, or causes.
Good for: reading a trilemma off one glance. Verdict: keep (as the tiny readable case that teaches
Figure 6), define "association" on the page.

### Figure 5: chart-holes (chart)

Recipe: `plot_frontier_coordinates(chart3[:, :-1], chart3[:, -1], holes=holes)`, three metrics, planted
data. Takeaway: where the cloud has empty places. Cold reads: A "a roughly round Gaussian-like cloud ...
a ring of orange squares around the outside; the squares are a boundary or generated points"; B "the data
look like an isotropic blob". Both guessed boundary/excluded; the caption corrected to "white space
candidates" and both flagged "red" versus orange. The squares sit on the outside of the cloud, so they
read as the edge, the opposite of "inside the cloud" in the chart-page alt text. Sentence test: "The
holes are grid positions far from every design" needs the picture only to place them; but here the
picture misleads. Ink: the squares take more frame than the cloud's own holes. Verdict: rework: the
holes should be interior (a hole is an empty place inside the cloud's support), fix the colour word in
the alt and caption, add a legend. Lines. Shows: grid positions far from every design in the first two
coordinates. Does not show: whether a hole is feasible, or any depth. Good for: choosing where to
look for new designs.

### Figure 6: adcs-tensions (examples)

Recipe: `case.tension_figure(study, fit)`, 10x10 heatmap, one-term cubesat fit. Takeaway: six metrics
contend, four don't, with the strong redundant pairs visible. Cold reads: A "only 6 metrics actually
matter ... strong blocks 0.91, 0.98 show redundant metrics ... tick labels are cluttered and the grey
text is hard to read"; B "slew time and control effort -0.87 ... the method selects 6 contending
metrics". Caption resolved the greying. Sentence test: "Six of ten metrics contend: total mass, slew
time, energy balance, control effort, pointing error, depth of discharge" is in the text already; the
figure adds the redundant pairs and the sign structure, so it earns its place. Ink: all cells are data.
Legibility: 870 px wide at 375 px is 0.4 of native: cell numbers about 5 px, illegible; tick labels with
w= values are small. Lines. Shows: which metrics are traded or redundant near the frontier, and which
six contend. Does not show: how far the tension reaches in magnitude, or why. Good for: choosing which
metrics to keep in a decision. Verdict: keep; rework for a phone: fewer decimals or a larger font, and
say why the outlines are on the diagonal.

### Figure 8: ternary-planted (examples)

Recipe: `plot_ternary(ts, X, lines=True)`, K = 3 planted data. Takeaway: the facets partition the
simplex into regions of trade. Cold reads: A "a map of preference weights ... contours have no scale, the
labelled boxes cover data"; B "contour lines cluttered and cross the region labels". Caption helped; grey
dots unexplained. Sentence test: passed (regions and contours are 2-D). Ink: about 65 percent, with
region labels covering about 8 percent of the triangle's data. Legibility: 698 px at 0.5 on a phone, the
numbered markers legible, the contours dense. Lines. Shows: designs by shares of three metrics, with
the facet regions and lines of equal V. Does not show: the total (V depends on it), or distance in
metric units. Good for: seeing which pairs trade where. Verdict: keep; rework: move the region labels
off the data, define the grey dots, label contour values.

### Figure 9: ternary-cubesat (examples)

Recipe: the same plot for the cubesat grouped as power, mass, attitude control. Cold reads: A
"sparse ... I could not tell what the position coordinates mean quantitatively"; B "plot is otherwise
empty ... nothing confirms" the link to Figure 8. This is the vacuous figure the supervisor named in
WP18; it is still on the page and carries a caption that says what the picture does not (0.18 is not
readable from it). The sentence test fails. Verdict: drop (a sentence or a three-row table of the
facet exponents by group carries all of it).

Proposed page lines for the retained figures are the Shows / Does not show / Good for lines in each
section above; I did not write them for dropped figures.

## Summary

| Figure | Verdict | Reason |
|---|---|---|
| 1 first-fit | keep, rework | clip outlier, state band; one of 1 and 4 only |
| 2 three-facets | keep, rework | facet legend and marker shapes |
| 3 tension-report | keep | define association |
| 4 log-plane | drop | duplicate of 1 at another band; read as a different fit |
| 5 chart-holes | rework | holes read as boundary; caption says red, image orange |
| 6 adcs-tensions | keep, rework | illegible at 375 px |
| 7 adcs-coordinates | rework | replace by candidate (a) |
| 8 ternary-planted | keep, rework | labels cover data |
| 9 ternary-cubesat | drop | vacuous; the sentence is enough |
