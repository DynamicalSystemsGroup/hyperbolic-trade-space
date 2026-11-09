# Note: the figure review (a visual loop; every figure earns its place or goes)

Written 2026-11-09 by the driver on the supervisor's direction (`work-packages/WP18-decisions.md`,
"The supervisor on the cubesat triangle"). He was shown a ternary plot of the cubesat fit with three
markers in an otherwise empty triangle and wrote: "this is pretty vacuous. doesn't seem to earn its
place on the page, even in the documentation. make sure we also do visual loops for figures". The
driver had passed that figure as clean. Its caption ("only facet 3 carries mass (0.18)") said
everything the picture did, which is the sign that the picture was not needed.

It sits beside the vocabulary review and the claims review, and applies to every figure a reader
can reach: the paper, the supporting material, the docsite, the root page.

## The requirement

**A figure is judged by what it is intended to convey and whether it succeeds.** The author writes
the intent first; a cold reader says what the figure conveyed; the figure succeeds when the two
agree. A figure that succeeds is left alone. A figure that fails gets the smallest change that makes
it succeed: a caption, a resize, then a redraw, in that order. A figure whose intent a sentence
carries as well does not earn its place and goes.

The supervisor, on the risk in this loop (2026-11-09): "i think there is a risk that you will
overtune here. i don't need the paper to be fully readable on a phone. i think you should reassess
the figures with a focus on what they are intended to convey and whether they succeed in doing so."
So: no redraw of a figure that conveys its intent; legibility is judged at the width the figure is
read at (the column on a laptop), and a phone is not a requirement for the paper's figures; the
docs pages must not break at phone width, but their figure text need not be readable there.

## The five tests

1. **The cold read.** A viewer with fresh context is given the image alone (no caption, no page) and
   says in one sentence what it shows and what they take from it. Then they are given the caption and
   say whether it changed their reading. The author's intended takeaway is written down *before* the
   read and compared after.
2. **The sentence test.** Write the one sentence that carries the figure's point. If nothing is lost
   by keeping the sentence and deleting the figure, the figure goes. (Three points in an empty
   triangle fail this; a cloud of designs with regions does not.)
3. **Ink is data.** The reviewer names what share of the frame carries information. Large empty
   areas, decoration, and labels that cover the data are findings.
4. **Legible where it is read.** At the column width on a laptop, in light and dark, in the
   browser: the labels that carry the intent are readable. A phone is not required; a figure is
   never redrawn for a phone.
5. **Shows, does not show, good for.** One line each, written beside the figure in the record and,
   once the figure is confirmed, on the page beside it: what the figure shows; what it does not
   show or cannot be used for; what a reader would use it for. (The supervisor: "we need more
   clarity about what specific plots show and dont show and what they are good for.")

## The loop

1. The author writes the figure's recipe first: the question it answers, the intended takeaway, the
   sentence of test 2.
2. Generate the figure by committed code; render it on its page.
3. Cold reads by fresh-context viewers (at least two; different reader personas where the reader
   grid applies), tests 1 to 4, findings verbatim.
4. Triage, smallest change first: keep as is (it conveys its intent); caption; resize; redraw (say
   what changes and why the intent needs it); drop. A redraw goes round again, twice at most; a
   figure that fails after two redraws is dropped.
5. The driver looks at every surviving figure himself in the browser and records what he saw. The
   driver's eye is one reading, not the verdict: his pass of the cubesat triangle is the case in
   point.
6. For the paper, the supervisor's two gates of WP19 (the slots, then the figures) close the loop.

## The record

`work-packages/<package>-figure-review.md`: per figure, the recipe, the cold reads verbatim, the five
tests, the disposition, and the image path and commit it was judged at.
