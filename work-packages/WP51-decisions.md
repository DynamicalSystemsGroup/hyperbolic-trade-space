# WP51 — Decisions: the root page recast (why, what, how; the three-metric figure)

## The direction (2026-11-14, 00:20 to 01:10)

The prose rulings (the two-level Why, the three sections, headers dropped, the close read before any merge) are verbatim
in `WP33-decisions.md`, 00:20 to 00:45, because the root page was WP33's surface. The figure thought, verbatim:

**Supervisor:** "another thought i had, we could use our synthetic example to flesh this out so they match. but that would mean we'd get a 3 x
plot because we need the other 2 comparions metric 2 vs 3 and metric 1 vs 3. one thing i like about this would be that even
though we're using a constructed synthetic example we're showing that we can reveal greater than 2d trades"

**Supervisor:** "the third pane would need to sweep along the axis parameterized by 2 metrics in focus in the row, right?"

**Supervisor:** "we could pivot it, do 3 columns and 4 rows, and include both the projection and the sweep. that would make the sweep and
intermediate visualization before the projection so the projection isn't mistaken for the sweep. or if the projection is view
is actually the same for all 3, we just do 3x3 subplots + 1 seperate figure"

**Supervisor:** "i want the figure updates incorporated into the plan for building my new index."

**Applied as:** one package, WP51 (`WP51-scope-of-work.md`): the root page's body as three sections without headers
(why, what, how), already drafted on branch `rootpage` for his close read; and the how section's figure redrawn from
the same three-metric planted table as the ternary, three rows (the metric pairs) by three columns (metric space, log
space, the chart's slice along the pair's axis), the third metric as the fan parameter in every pane, with the ternary
kept as the one view of the whole position space (the projection, the same for all three pairs, so no projection pane
per row). The paper's Figure 1 is not touched. The figure goes through the figure loop with cold reads of the page.
Merge into `dev` only on his word after his close read of the rendered page.

## His wording of the why (2026-11-14, 01:20)

**Supervisor, verbatim ("here is my wording"):** "Decisions about engineered systems mix two questions: (1) what is possible and what trades against what, which can be
assessed scientifically, and (2) what is preferable, which is a judgement that belongs to the people accountable for it.
This method provides a data-driven approach to (1) in service of grounding (2) in an empirical method that is interpretable
and reproducible. The line between the options on the table and the options preferred is then auditable. Where stakeholders'
interests are in tension, the data says how they compete and where they compete. This provides guidance for deciding whether
to search for new options and for deliberating over the ones in hand. When decisions are made, the evidence base and
reasoning for that judgement can be recorded alongside the decision."

**Applied as:** his paragraph, with two light touches and nothing else: "are in tension" becomes "compete", because
tension is now the glossary's word for the local partial derivative between two metrics on the surface and the plain
word for competing interests is compete or trade off; "the data says how they compete and where they compete" becomes
"the data say how they compete and where", the paper's plural and one repetition fewer. Rendered on 8793 for his read.

## Merge of the prose; the figure and its prose to follow (2026-11-14, 01:35)

**Supervisor, verbatim:** "you can merge in the new prose but i am still expecting new plots which will also call for some
prose revisions in the later sections near the figures"

**Applied as:** the prose (his why, the what, the how, no headers, the two vocabulary edits, the rewritten tests) merges
into `dev` once the branch's checks pass (lint, format, lock, vocabulary, residuals, the fast suite, the site tests),
and that merge is the approval act for WP51's G1. WP51 continues: the three-metric figure (G2, G3) and, added to G1 by
this ruling, the prose revisions in the what and how sections and the captions that the new figure calls for, drafted
for his close read before they merge. The page is read again rendered at that point.

## The docs home (2026-11-14, 02:05; read in the pane beside the root page recast)

**Supervisor, verbatim:** "docs home needs a figure and a quickstart code block"

**Applied as:** a small unit on its own branch (`docshome`), drafted by the driver for his close read: a quickstart
code block (install, a first fit on a table, the report) and the figure that code produces, placed after the five
doors; the ruled edit "unsupervised learning, beside PCA" applied at the same time; merged only on his word after the
rendered read, as the root page was.

**Supervisor, verbatim (02:30), on the docs home's word budget:** "budgets were set by you, they can be revised with good
reason. in this case i asked for more content"

**Applied as:** the docs home's budget in `tests/test_site.py` goes from 206 to 250 with that reason in the comment;
the rule stands as he states it: a budget is the driver's instrument, revised with a stated reason, and his request for
content is one.

**Supervisor (2026-11-15, 09:40 EST), the docs home read in the browser (branch `docshome`, served on port 8794):**
"Land it"

The docs home lands on dev: the quickstart block (run by the driver before his read), the first-fit figure, the PCA
sentence, "white space" for "gaps" (his ruling of 2026-11-14), budget 250 raised for the figure and the block.

**Supervisor (09:45 EST), on the docs home's word budget (348 against the driver's 250):** "call it 350 going forward so
it doesn't raise an alarm but disincentivizes bloating it"

The test's bound becomes 350 with his words.

## The three-pane figure still the paper's; the fan figure dispatched (2026-11-14 21:45 EST)

**Supervisor, verbatim:** "index is still this image. i assume this is as intended and new figures have not landed or
been integrated yet"

**Applied as:** confirmed. The root page's second figure is the paper's Figure 1, unchanged; the planted ternary above
it is the whole-view figure. WP51's G2 figure (three rows of metric pairs, three columns of metric space, log space and
the chart's slice, the third metric as the fan) was never dispatched to a unit. It is dispatched now, on branch
`wp51fig`, with G3's caption, G1b's prose revisions and G4's loop, for his close read in the morning; it merges only on
his word, as the scope's good-enough says.

## The fan figure delivered for his close read (2026-11-14 22:07 EST)

Branch `wp51fig` at 2abc4d8 (six commits, no trailers): the generator (`fan_values`, `slice_pieces`, `draw_fan` in
`scripts/build_site_figures.py`, drawn from the one `fit_why()` fit, with R-1 tests); the root page shows the fan figure
in the how section in place of the paper's Figure 1 and the ternary stays as the whole view with its caption saying so;
the assembler no longer copies `figure1.png`; the figure loop recorded with two Haiku cold reads (both took the
takeaway from the image alone; the caption completed the shades), nothing changed after them; register rows added and
C358 narrowed. The unit's gates: ruff, format, lock, vocabulary and residuals clean; site and register tests 77 passed;
the fast suite 2,034 passed with one failure, the paper test that pinned the assembler copying Figure 1, updated in the
last commit and not re-run in full. The driver reruns the suite and does the browser pass at phone width and in dark;
the page is served on port 8851 for his close read; it merges only on his word.

## His read of the fan figure (2026-11-14 22:30 EST)

**Supervisor, verbatim:** "the visuals are confusing. the example or the figures may need work"

The figure loop's verdict from the one reader who matters: not kept as drawn. The fan figure stays on `wp51fig` and
off dev; the root page keeps the ternary and the paper's Figure 1 unless he says otherwise. The next step (rework the
planted example, redraw, or park the figure for after 0.1) is his call, asked in chat.

**Supervisor (2026-11-14 22:31 EST), asked whether to park the fan figure for after 0.1 or rework it tonight:** "Rework tonight"

**Applied as:** a rework unit on `wp51fig`, by the figure loop's order: three candidate renders (the fan removed, the
third metric at its median; the fan as rows for the leading pair; the planted example re-seeded so the three terms
separate), each cold-read by two fresh readers against the one-sentence test, the clearest applied with its caption and
prose, the three candidates kept in the loop record for his morning read. In every candidate the envelope at a fan value
is one connected line. Merges only on his word.

**Supervisor (2026-11-14 22:31 EST), on the fan figure as drawn (image attached in chat):** "for starters there are a lot of lines and
we've lost the story of the 3 curves and the stars are not inuitive"

**Applied as:** three constraints handed to the rework unit: one surface per pane, its three pieces in the three term
colours as one connected curve, so the story is the three curves; far fewer lines (the fan reduced to the median, or
one contrast at most, told in a single pane or the caption); no stars: the one design marked as Figure 1 marks it, a
black dot with its distance to the surface, or not at all; the chart column drawn as Figure 1's third pane draws it (the
flat surface in the three colours, the designs below), not as stacked bars.

