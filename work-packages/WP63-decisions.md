# WP63 — Decisions: the examples with an arc

## His direction (10:42 EST, 2026-11-16, verbatim)

"i was reading through the example pages for some of the fits we created. they did their job of showing the solver
fits trades but they are hard to understand for a reader and they offer no intuition really. i think the example pages
need a short prose summary of the research or application the data was drawn from, a data dictionary for the data used.
a short explanation in scientific or engineering terms of the purpose of the analysis (avoiding prebaking the conclusion
of the analysis) then the analysis then the interpretation. this should be as concise as possible but needs to follow an
arc the reader can interpret. rigor and interpretability are part of our sorry. yes \"you can fit any data\" but why did
you do that and what do the results mean.

can you do a spike to review our examples on the documentation page and make them more interpretable to a cold reader
without eliminating the data, code and plots that serve as the demonstration of the method. as always avoid
metanarration. the point is still to show the method in action just provide a bit more context so the reader has some
intuition for the analysis."

And: "maybe a template for examples would help"

## WP63 approved as proxy (10:42 EST)

`WP63-scope-of-work.md` (a spike: the template of the arc, the three dataset pages and the cubesat example page
redrafted to it with every code block, plot and number kept, a readout with cold reads) is approved by the driver under
his mandate on the direction above. One unit on branch `wp63`; the driver soft-confirms on captures and lands the drafts
on `dev` for his read, as with the paper's sections. Dispatched after WP57's D-3 hand-back; D-3's records follow.

## WP63 accepted as proxy and landed (15:20 EST)

Delivered on `wp63`, one commit, rebased onto the records head and fast-forwarded as a9a267ed. The template
`notes/examples-template.md` (the five parts, each with its must, must-not and length; headings in the page's words;
the dictionary as a text block since the site's phone rule forbids Markdown tables and a list would cost each page's
budget; glossary links at first use). The four pages redrafted: every code block, figure, alt text, caption (Figures 6
to 10 unchanged) and register comment kept; the cubesat page in second-level headings because the docs tests pin its
choosing-K section and five phrases and the user guide links two of its anchors. Prose words within budget on every
page (cubesat 988 of 990; perovskite 687, amniote 679, wheat 690 of 700; the site 11,330 of 11,335). Cold reads, one
context-gapped reader per page (P3 or P4), answered the three questions in the page's intent on all four; two flags
acted on (the cubesat answer scoped to the thirteen-metric fit; the amniote fit paragraph naming the four-metric fit).

The driver's calls on the unit's five: the dictionary stays a text block (the budgets stay); the glossary links are
the method-term fix and a pointer to the user guide is not added (no words to spare, and the guide is one click away
in the nav); the perovskite sentence on the band gap rests on the cited detailed-balance paper, a verified source,
and stays; the wheat sentence "the shift the breeding studies report" stays beside "describes and does not test
breeding", since the first compares the medians to the cited studies and the second says what the data cannot
attribute; the synthetic three-metric case stays on the Examples page as the root page's construction (WP58 may move
it). Soft-confirmed on the captures (the arc visible on each page: source, attributes, the question, the fit, the
answer, what it cannot show). The driver's independent run on the branch, exit codes captured: lint, format, lock,
vocabulary (0 new), residuals exit 1 as on dev with no new rise, mkdocs, the diff within the scope's files, the page
tests (test_wp45_examples, test_site, test_docs) 163 passed, 1 skipped. No attribution line. CI dispatched on dev.
His read decides the arc's wording.

## His direction on the wheat figure (15:51 EST, verbatim)

"looking at the wheat example i was thinking maybe we ought to extend this figure to include lines for a bunch of V
values not just the V=1 value (and label them). as drawn it reads like fit line and feels off. but if instead we drew
level sets with labeled values of V i think it would make its point much better, it also shows the the tool is still
useful even when the trade-off in question is only 2 dimensional"

The driver's reading: Figure 10 (the log plane of grain and straw) redrawn as labeled level sets of V, the frontier
V = 1 among them, so the picture is the fitted surface's field and not one line; the band's job re-judged; the
figure loop run on the redraw (cold read, the sentence test, ink as data, legibility, shows and does not show); the
caption and alt text follow; a small unit after the register repair lands, since both touch the wheat page's
register rows.

**His follow-on (15:51 EST, verbatim):** "if this works well i suspect you should update the plotting method and also
the use of the same plot method in other places such as the paper"

The driver's reading: two steps. First the wheat figure redrawn with level sets through the figure loop, as a
`levels` option of `plot_log_plane` that leaves every existing call unchanged; if it works well on his read, a second
unit makes the level sets the method's drawing and updates every use of the method (the paper's notebooks, the docs'
pages, the examples), each use re-judged by the figure loop, the register and the paper tests following.

## The register repaired after the redraft (15:58 EST)

CI on the WP63 head failed `test_the_register_holds`: 41 rows anchored to the example pages' old sentences and
headings. Landed at 2e01b23c: 39 rows re-anchored to the sentences and headings that now carry their claims (21 by
heading only, 18 by new wording; three kept where part of the original sentence was cut and the surviving part
means the same: C845, C846, C906, the last now scoped to the thirteen grain-and-straw rows, -0.62 to -0.90, which
the variants file confirms). The unit's two calls to the driver, decided by the claims rule (narrow, never widen the
backing): the perovskite answer "All three metrics contend in every fit" overclaimed, since the no-scaler fit's set
is Voc and FF; it now reads "in each of the four conditioning fits" and C869 is re-anchored to it. The question's
physics sentence carried a directional claim ("a wider gap raises the first and lowers the second") that no verified
source in the record backs; it now reads "the band gap sets both the voltage a cell can reach and the current it can
collect", which the abstract read in the WP45 record backs, and C873 is re-anchored to it. The directional sentence
can return with a verification entry if he wants it (WP58). Register: 748 rows, no id added or reused. The driver's
run: register 21 passed; fast suite 2,096 passed on the repair; the record, budget and table tests on the two
narrowed sentences green; lint and format clean. CI dispatched.
