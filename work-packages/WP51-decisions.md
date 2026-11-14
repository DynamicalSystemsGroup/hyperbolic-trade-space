# WP51 — Decisions: the root page recast (why, what, how; the three-metric figure)

## The direction (2026-11-15, 00:20 to 01:10)

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

## His wording of the why (2026-11-15, 01:20)

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

## Merge of the prose; the figure and its prose to follow (2026-11-15, 01:35)

**Supervisor, verbatim:** "you can merge in the new prose but i am still expecting new plots which will also call for some
prose revisions in the later sections near the figures"

**Applied as:** the prose (his why, the what, the how, no headers, the two vocabulary edits, the rewritten tests) merges
into `dev` once the branch's checks pass (lint, format, lock, vocabulary, residuals, the fast suite, the site tests),
and that merge is the approval act for WP51's G1. WP51 continues: the three-metric figure (G2, G3) and, added to G1 by
this ruling, the prose revisions in the what and how sections and the captions that the new figure calls for, drafted
for his close read before they merge. The page is read again rendered at that point.

## The docs home (2026-11-15, 02:05; read in the pane beside the root page recast)

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

