# WP51 figure review: the fan figure of the root page

Process note: the recipe below was fixed before the figure's cold reads and before its captions. Two
development renders (geometry, axis limits, legend) were drawn first to see whether the slices came out as the
recipe says; no reader saw either. Images: `figure-loop/before-figure1.png` (the paper's Figure 1, which the root
page's how section showed) and `figure-loop/after-site-fan-light.png`, `after-site-fan-dark.png`.

## The recipe

**The question.** When the trade space has three metrics, what does the trade between any two of them depend on?

**The intended takeaway.** The surface that two metrics trade along moves as the third metric moves: terms appear
on it, change places and leave, and the same fitted model shows this in three views (the metric space, the log space,
the chart), for each of the three pairs, so a trade among more than two metrics is shown, not told.

**The sentence of the sentence test.** "Fix the third metric at three values and the surface between the other two
changes, term by term, in the metric space, the log space and the chart."

**What it shows.** The fitted surface (V = 1) of the planted three-term table, sliced in the plane of each pair of
metrics with the third held at its 20th, 50th and 80th percentile over the table, coloured by the term that leads
along it; the designs within a band of each held value; the same slice in the chart along the pair's axis.

**What it does not show.** The whole position space at once (the ternary beside it does that); a design's value of
the third metric (a design is drawn in the slice it lies near); anything about a table other than the planted one.

**What a reader uses it for.** To see that a pairwise trade is conditional on the other metrics, and where the
terms of the surface take over from one another.

## Cold reads (fresh Haiku readers; image first, then the caption; reports verbatim)

Page served from the built images and `site/index.html` on port 8851 (a static copy: `site-fan-*.png`,
`ternary-planted-*.png`, `index.html`); the readers were given the image file path.

**Reader A, image alone (light render):** "The figure is a 3x3 panel of a fan of posynomial reference curves: the left column plots metric 1 against metric 2, metric 2 against metric 3 and metric 1 against metric 3 in metric space, the middle column shows the same pairs in log space as an envelope of three colored terms, and the right column shows a slice of log V with bars for each fan value, with a legend for the 20th, 50th and 80th percentile third metric and a star marking one design. What I take from it is that the surface is a set of terms whose envelope moves across the fan as the third metric changes, and that the sampled points cluster around log V = 0 with spread below it."
**Reader A, with the caption:** "the figure now reads as the triangle's three metric pairs sliced at the third metric's 20th, 50th and 80th percentiles, with the fitted terms appearing and leaving as that slice moves. The caption changed my reading only in confirming that the faint-to-strong lines are percentile levels."

**Reader B, image alone (dark render, seen on white):** "The figure is a 3x3 grid of small-multiples for a three-metric posynomial fit, with the metric-space curves on the left, the log-space envelopes in the middle, and the slice charts on the right; each row fixes a different metric as the fan variable (20th, 50th and 80th percentile curves) and marks one design with a star, so the reader takes away that the fitted term-by-term frontier and its spread across the third metric can be read directly from the panels, though the faint light-grey rendering on white and the unlabelled fan colours make the percentile bands hard to tell apart."
**Reader B, with the caption:** "the figure shows the fitted reference surface as three rows of pairwise slices, each with the third metric fixed at its 20th, 50th or 80th percentile (faint to strong), and the caption does change my reading, since it settles the shading I had called unlabelled and says the terms appear and leave as the slice moves, which I did not read from the image."

## The five tests

1. Cold read: both readers named the three views, the three pairs, the fan of three values and the star; both took
   that the surface depends on the third metric (A: "envelope moves across the fan"). Neither took "terms appear
   and leave" from the image alone; the caption supplies it and B said so. Intent and reading agree on the
   takeaway; the appear-and-leave part rests on the caption.
2. Sentence test: the sentence says the claim; the figure carries what it cannot (where each term leads along each
   slice, the shift of the surface by pair and by value, the designs near each slice); it stays.
3. Ink is data: curves, designs and bars are data; about one third of each pane is empty axis (metric space's upper
   right, the chart's lower half left of the designs); no decoration; no label covers data (the one note in the
   top-left pane of the chart column sits above the bars).
4. Legible where read: at the wide column on a laptop the axis labels, the row names and the key are readable;
   the fan is told apart by ink strength, which the key states. B's "faint on white" is the dark render viewed on
   white, not how it is read (transparent ground on the dark page).
5. Shows: the fitted reference surface of the planted table sliced for each metric pair with the third held at
   three values, in the metric space, the log space and the chart; where each term leads. Does not show: the whole
   position space at once (the triangle does), a design's value of the third metric. Good for: seeing that a trade
   between two metrics depends on a third, and where terms take over.

## Disposition

Keep as is. The reads convey the intent (the caption completes it, as the loop allows); no redraw. The one finding
of B, the unlabelled shades, is answered by the key already in the image and by the caption's "(faint to strong)".

## Rework (2026-11-14, night): the fan removed

The supervisor read the figure above and said: "the visuals are confusing. the example or the figures may need work";
then, "there are a lot of lines and we've lost the story of the 3 curves and the stars are not inuitive"; then "my
gut is that you are trying to do too much. keeping just term 1, term 2 and term 3, dropping the percentile lines is a
good place to start and the stars may also need to go since i don't think they add much given we already have data
point dots for designs"; then "the square root of 2 also comes a bit out of no where". The figure above is the before
(`figure-loop/after-site-fan-light.png`, `after-site-fan-dark.png`; the paper's Figure 1 is
`figure-loop/before-figure1.png`).

**Candidate A only**, as he narrowed it; B (one pair, three rows) and C (the table re-seeded) were not built, because
the rule was to try them only if both readers missed the three-pieces story, and neither did. A development render of B
was drawn and looked at (the terms do enter down the rows: one at the 20th and 50th percentile, three at the 80th),
and a re-seeding of the planted exponents was explored numerically; neither is kept.

### Recipe (written before the draw)

**Question.** What does the fitted surface of a three-metric table look like, between each pair of metrics?
**Takeaway / sentence.** "The fitted surface of a three-metric table is three pieces, one per term; between any two
metrics its shape depends on the third, and a term enters or leaves as the third metric moves."
**Drawn.** Rows the three metric pairs; columns the metric space, the log space and the chart as the paper's Figure 1
draws it (the surface laid flat as a line in the term colours, the designs below it); the third metric held at its
median only; one connected curve per pane, pieces in the term colours, nothing else coloured; designs within a band
(0.12 in log) of the held value as grey dots; no percentile lines, no star, no marked design, no arrow; the
chart's horizontal axis is "position along the metric i against metric j axis" and the square root of two is nowhere.
The dependence on the third metric is told by the caption, not drawn.
**Shows.** The fitted reference surface of the planted table cut in each pair's plane, term by term, with the designs
near the cut. **Does not show.** The surface at any value of the third metric but its median (the caption says the
pieces change), a design's own value of the third metric. **Good for.** Seeing the surface as pieces, one per term,
and that a pair's trade is read with the third metric held.

### Cold reads (fresh Haiku readers, image first, then the caption; verbatim)

Round 1 (axis label still the formula; the light render, then the dark render on its dark ground):

**Reader 1, image alone:** "The image is a 3x3 grid of slices of a fitted three-term surface, with metric space, log space and a flattened chart in columns and each pair of metrics in rows, showing grey designs scattered below coloured piecewise curves (blue, orange, green) that read as a frontier the data sits beneath."
**Reader 1, with the caption:** "The caption says the figure shows the same table as the triangle sliced by a held-median third metric, with each pane's curve made of one piece per term and each dot a design within a band of the held value, and that the chart column lays the surface flat with designs placed below it by log V; this confirms my reading that the colored pieces are the fitted terms and that the data sits beneath the surface, though the caption's \"a term enters or leaves\" under other held values is not visible in these three panes."
**Reader 2, image alone:** "The figure is a 3x3 grid on a dark background, with each row a pair of metrics (1 vs 2, 2 vs 3, 1 vs 3) showing three coloured fitted terms as a curve in metric space, as an envelope in log space, and laid flat, over grey data points, and I take from it that the fitted surface is three terms whose envelope bends where one term takes over."
**Reader 2, with the caption:** "The caption says the figure is the triangle's table in slices, one row per metric pair with the third held at its median, and each column is metric space, log space, or the flat chart, so the surface reads as one curve of three coloured pieces with dots within a band of the held value; this makes clear that the held value changes which terms appear, which the figure alone did not state."

Round 2 (the final render: the axis label "position along the metric i against metric j axis", the caption as on the page; the light render, then the dark):

**Reader 3, image alone:** "The figure is a three-by-three grid showing the fitted reference surface for three metric pairs, each in metric space, log space and a flattened chart, with the three colour-coded terms drawn over grey data points, and I take from it that the fit bends into a piecewise envelope whose term changes shift where the curve breaks."
**Reader 3, with the caption:** "The caption says the figure is the triangle's table in slices, with the third metric held at its median, and that each column is metric space, log space or the flattened chart, which makes the grid readable as stated and reinforces that the term changes at other held values, so the caption did change my reading by explaining the column meanings and the held-value slicing."
**Reader 4, image alone:** "The figure is a 3x3 grid on a dark background: each row fixes the third metric at its median and plots one pair of metrics (1 vs 2, 2 vs 3, 1 vs 3) in metric space, log space and a flattened chart, with the fitted reference surface drawn as coloured pieces (term 1 blue, term 2 orange, term 3 green) over grey design dots, so the reader can see which term leads where along each slice."
**Reader 4, with the caption:** "The caption explains the three columns, the median-held slices, the colour-coded term pieces and the note that a term enters or leaves when the held value changes, which makes the figure's column headings and the term switches readable rather than puzzling, though it does not change my overall reading."

### Against the sentence

All four readers took the first part (a fitted surface of coloured pieces, one per term, that bends where a term takes
over) from the image alone. None took the second part (the shape depends on the third metric, a term enters or
leaves) from the image alone: reader 1 says so, reader 2 says the figure alone did not state it, readers 3 and 4 get it
from the caption. That part rests on the caption, which the loop allows, and a figure cannot show it with the third
metric held at one value. No candidate was drawn that shows it in the image; B does (the rows), at the cost of one pair.

### Tests, disposition

1. Cold read: the three-pieces story passes from the image; the dependence on the third metric passes from the caption.
2. Sentence test: the sentence's first half is carried by the image, the second by the caption; the figure stays.
3. Ink is data: lines are the surface, dots the designs; about a third of each position pane is empty axis.
4. Legible: the column heads, the row names (the held metric and its value) and the key read at the column width.
5. Shows, does not show, good for: as in the recipe.

Disposition: A on the page (`site-slices-light.png`, `site-slices-dark.png`; images `figure-loop/rework-A-light.png`,
`rework-A-dark.png`). Deleted, each for what it no longer did: the fan (three overlaid surfaces per pane, which hid the
one connected surface), the stars (a second mark for a design the dots already show), the stacked bars (which no
caption explained), the root of two (a formula on an axis).

### Temperature (the supervisor: "remember you can tune on temperature to get a nice visual and just report the temperature you used")

The one fit of `fit_why()` was at temperature 50, where the median slices showed one, two and three pieces by pane
(row one a single term). Tried 3 to 200 (`TEMPERATURE` in the generator): at 10 the median slices show two, three and
three pieces; at 5 and 8 the same count but with the surface further inside the designs (more designs above log V = 0,
up to 0.32 at 10 against 0.07 at 50). **Used: 10.** The ternary is drawn from the same fit, so it changed with it
(regenerated; the terms are renumbered, the regions and labels follow the fitted exponents as before); the caption and
the register state the temperature.

Round 3 (the final render at temperature 10, the line joins rounded; light, then dark; verbatim):

**Reader 5, image alone:** "The figure is a 3x3 grid of slices of a fitted posynomial reference surface for three metrics, one row per metric pair with the third held at its median, and each row shows the curve in metric space, the same curve as a piecewise-linear envelope in log space coloured by which of three terms leads, and the surface laid flat with each grey design dot sitting below it by its log V."
**Reader 5, with the caption:** "The caption confirms the layout (columns are metric space, log space, and the flat chart; dots are designs within a band of the held value) and adds that the coloured pieces are the terms leading along the surface, and that holding the third metric at another value makes terms enter or leave, which the three rows make visible, so the caption did not change the reading; it sharpened it, and it also notes the table was fitted at temperature 10, which the image does not state."
**Reader 6, image alone:** "The figure is a 3x3 grid on a dark background, one row per pair of metrics (metric 1 against metric 2, metric 2 against metric 3, metric 1 against metric 3, third metric at its median), showing the fitted reference surface as an orange, blue and green curve in metric space, as a log-space envelope, and laid flat as a chart with the scattered designs below it, and I take from it that the fitted surface runs along the data with different terms leading in different regions."
**Reader 6, with the caption:** "The caption says the same table as the triangle at temperature 10, in slices, with each curve piece coloured by the term leading along it, each dot a design within a band of the held value, and the log V offset, and it adds that holding the third metric at other values makes terms enter or leave, which matches what I read from the panes and does not change my reading."

Both final readers took the three-pieces story (terms leading in different regions, a piecewise envelope in three
colours) from the image; the third-metric dependence still comes from the caption (reader 5 credits the three rows,
which each hold a different pair and not a different value of the third metric: a misreading). Round 2 images (the baseline the supervisor
took): `figure-loop/rework-round2-light.png`, `rework-round2-dark.png`.

## Round 3: the surface brought to the data

The supervisor on round 2 (the baseline, kept as `figure-loop/rework-round2-light.png`, `rework-round2-dark.png`): "drawings
look much easier to interpret now. i would take this one as a baseline and still try to improve it. for me the most obvious
improvement would be if the fit frontier was pushed closer the the visible extent of the data. i am not expecting 100%
inside the envelope but right now it seems like the envelope is pretty conservative"; and: "its fine if not every color
appears on every row as long as all 3 colors appear in at least 1 row", "its even okay if a row has only one term".

**The planted construction (the example).** `PLANT` in the generator: `frontier_fraction = 0.7` (70% of the designs lie on
the surface), `interior_scale = 0.25` (the rest lie 0.25 below it on average), `noise = 0.07` (the surface rows scatter by
0.07 in log V, so about a tenth lie beyond it: 11% measured), the package's seeded exponents unchanged, three terms,
900 rows. **Temperature 50** (swept 10 to 100 on this construction: at 10 more than half the designs lie beyond the
surface, at 100 almost none; 50 gives 11% and the data reaching the surface along 78%, 100% and 100% of the three median
slices at 0.35 log). The ternary is drawn from the same fit and regenerated; its terms are renumbered, the regions and labels
follow the fitted exponents. **The display.** The band on the held metric is 0.15 (log) and each dot's opacity runs from
0.95 at the held value to 0.15 at the band's edge, the farthest drawn first. Round 2 had temperature 10 on the package's
default table.

**Cold reads, final render (image alone, then the caption; verbatim):**

**Reader 7 (light), image alone:** "The figure shows three rows of a fitted reference surface for three metrics, each row drawn in metric space, log space and as a flattened chart, with the three colored terms forming a piecewise envelope over grey data points, so I take from it that the fit tracks the cloud from above and the flattened residuals sit mostly just below zero."
**Reader 7, with the caption:** "The caption says the figure is the triangle table fitted at temperature 50 sliced into three pairs with the third metric at its median, and it explains that each design sits below the surface by its log V, so it confirms the reading that the points lie below the envelope and that terms enter or leave as the held value changes."
**Reader 8 (dark), image alone:** "The figure is a three-by-three grid on a dark background showing one fitted surface for three metrics, drawn in metric space, log space and a flat chart, with the orange, blue and green term segments bending over grey scatter points."
**Reader 8, with the caption:** "The caption says this is the triangle's table sliced by metric pairs with the third held at its median, that dots darken as they sit nearer the held value, and that the flat chart's vertical axis is log V, which confirms my reading and explains why the terms change when the held value moves."

Against the sentence: both took the three coloured pieces of one fitted surface, and that it tracks the data from above
(reader 7: "the fit tracks the cloud"), from the image alone; the dependence on the third metric again comes from the caption.
The gap the supervisor saw is closed: the data reach the surface along the slices. Row one (metric 1 against metric 2)
shows two terms, rows two and three show three; all three terms lead somewhere, as he allowed.

### The optional landmarks (the triangle's star, diamond and square): tried, dropped

The ternary's three markers are not designs: each is a term's exponent vector read as shares of the three metrics (the
point where that term's V peaks at a fixed total; `ternary_marker_values`). They were mapped as the supervisor said:
shares c = w_k fix the ray m = t c (each metric in units of its typical size), V is homogeneous of degree one so the ray
meets the surface once at t = 1/V(c), and the log of that point is the log-metric point, with the chart point at (position
along the pair's axis, log V = 0). Checked: log V is 0 at all three points and the shares read back as the exponents.
Drawn as hollow markers of the triangle's shapes in the metric and log panes (they lie on the surface, but their third
metric is not the held median, so they float off the slice's curve) and filled in the term colour on the chart's flat
line, with a legend entry (render: `figure-loop/rework-round3-markers-light.png`).

Cold reads of that render (image alone, then caption with one added sentence on the markers; verbatim, the relevant parts):
**Reader 9 (light):** "...with the three terms coloured and a star, diamond and square marking landmarks; I take it that the surface is an envelope where the terms take over in turn, but I could not tell the units, what the grey scatter represents, what the log V scale means numerically, or what the three markers stand for."
**Reader 10 (dark):** "...with three coloured term pieces tracing the frontier and star, diamond and square markers for landmark designs; I take from it that term 1 governs the high-metric end while terms 2 and 3 govern the low end, but I could not tell what the grey dots are, what units or normalisation log V uses, or whether the landmarks correspond to the named designs, and the right-hand axis labels are clipped at the edge."

The one-sentence reading did not get worse, but both readers asked what the markers are, and reader 10 took them for
named designs, which they are not (the supervisor's own test for dropping them). In the position panes the hollow
markers sit off the drawn curve, which reads as stray points. **Dropped**: the markers and the code that drew them are
not on the page or in the generator (git history keeps it). A reader who wants to follow a term across the views has the
colours.

## Round 4: the terms' own points (the triangle's star, diamond and square), two candidates

The supervisor, on the dropped markers: "is there an alternative to using median that would make this work better. its okay
if there is not but i think its worth exploring a bit." and "the third col where they fall on the log V = 0 line looks quite
good so i suppose another option would be to only plot them on that col; though for consistency sake it would be great if we
could address the question of how to make it look good on all 3 cols. we still retain baseline option to not include the
landmarks". Round 3 without markers stays the baseline (`figure-loop/rework-round3-*.png`).

Why the median cannot carry them: the chart projects the whole surface onto log V = 0, while the metric and log columns are
a section at one value of the third metric; the three points (each a term's exponent vector taken to the surface) have three
different third metrics, so they cannot lie on one section. Mapping and construction: `synthetic-case.md`.

- **A** (`figure-loop/rework-round3-chart-markers-*.png`): round 3 plus the three markers on the chart column only, exactly on
  the line, a legend entry "term k's own point".
- **B** (`figure-loop/rework-round3-band-markers-*.png`): the metric and log columns drawn as a projection too, the surface
  shaded between its sections at the 20th and 80th percentile of the third metric, the median section on top, the markers
  hollow in those columns, filled on the chart.

Cold reads, image alone (two readers each; verbatim). The sentence tested: the round 3 one, plus "where the terms' own
points sit".

**A, reader 11 (light):** "The figure shows the fitted posynomial reference surface for the three metrics in three slices (each metric held at its median), drawn in metric space, in log space as a piecewise-linear envelope of the three terms, and flattened onto a position axis; I take from it that term 1 dominates the high-metric end of each slice while terms 2 and 3 take over toward the low end, with the scattered data sitting around the surface." / "The terms' own special points appear only in the right-hand column, the flattened chart, as a star for term 1, a diamond for term 2 and a square for term 3, each placed on its term's segment, and the legend names them \"own point\" without saying what they are, so the figure does not explain them. (Term 3's square shows only in the middle row, and the metric-space and log-space panels mark none of them.)"
**A, reader 12 (dark):** "The figure shows three pairwise slices of a fitted reference surface (metric 1 against 2, 2 against 3, and 1 against 3, each with the third metric at its median) in three columns: metric space, log space where the surface reads as a piecewise-linear envelope of three terms over the scattered data, and a flattened chart of log V against position along each axis, and from it I take that the data sits in a band beneath a surface made of three monomial pieces, with a different term dominating each region." / "The three terms' own points appear only in the right-hand flattened chart column, as a star for term 1, a diamond for term 2 and a square for term 3, and the figure never says what they are beyond the legend's \"term k's own point\"; they are not marked on the kinks of the surface in the other two columns, and in the top row the term 2 diamond sits on the orange term 1 band, so it is not clearly on its own term's band."
**B, reader 13 (light):** "This shows the fitted three-term posynomial surface across three metric pairs (each with the third metric held at its median), in metric space, log space and flattened chart form, with the data as grey points; the surface reads as a lower envelope of three terms, with term 1 dominant at high metric 1 and metric 2 and term 3 at the flat top-left." / "The markers labelled \"term N's own point\" (star, diamond, square) appear in all nine panels, and in the flattened chart column each sits on its term's segment, but in the metric-space and log-space panels some sit off the curves near the axes, and the figure never says what the points are beyond the legend label."
**B, reader 14 (dark):** "The figure is a 3 by 3 grid of the fitted posynomial surface for three metrics, each row holding the third metric at its median, shown in metric space, in log space as an envelope of three linear terms (orange, blue, green), and laid flat as a chart of log V against position, with grey dots as data; I take from it that the fitted surface is the upper envelope of the three terms and that the flat chart shows which term is active across the design." / "Yes, the figure marks each term's own point with a distinct marker (a star for term 1, a diamond for term 2, a square for term 3, listed in the legend as \"term N's own point\"), and in the flat chart column these sit at log V = 0 on their own term's segment, which is where that term attains the envelope."

**Reading.** All four took the three-pieces story from the image, as in round 3 (neither candidate reads worse). In A the
readers find the markers on the chart line and on their term's segment, and say the legend does not say what they are (the
caption does). In B the readers name nothing of the shaded band; they find markers in nine panels, some off the curves near
the axes, which is the confusion the first attempt had: two of the three terms' points have a third metric far outside the
middle three-fifths, so they fall outside the band and read as strays. B adds ink and a legend entry and no reading. **Chosen:
A**, on the page with the markers on the chart column only. B is kept as the render above and its code deleted.

### The page text (the supervisor: "don't bloat the index with lots of detail about how the plots were made...")

Both captions cut to the narrative (the table, the three terms, one surface, the same table three ways, the markers), with
no temperature, percentile, band or construction, and the slices caption ends with one clause linking to
`docs/examples.md#the-synthetic-three-metric-case` (to be filled by a later unit). The construction detail is in
`synthetic-case.md`. The how-section sentence ("the surface between any two changes with the third, and terms enter and
leave it") was already the narrative and is unchanged. Final render: `figure-loop/rework-round4-*.png`.
