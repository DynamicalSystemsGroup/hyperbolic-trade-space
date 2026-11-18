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

**Supervisor (2026-11-14 22:34 EST):** "my gut is that you are trying to do too much. keeping just term 1, term 2 and term 3, dropping
the percentile lines is a good place to start and the stars may also need to go since i don't think they add much given
we already have data point dots for designs"

**Applied as:** the rework narrows to one candidate first: the three-by-three with the fan dropped (the third metric at
its median), the three terms only, no stars and no marked design; the caption and the prose follow; the other
candidates only if that one fails its cold reads.

**Supervisor (2026-11-14 22:36 EST):** "the square root of 2 also comes a bit out of no where"

**Applied as:** the chart column's axis label loses the formula: it reads as Figure 1's third pane reads, the position
along the pair's axis (Z); if the construction needs stating, the caption says the axis is the difference of the two
log-metrics, scaled to unit length, and the square root of two appears nowhere on the figure.

**Supervisor (2026-11-14 22:38 EST):** "my impression is that since this is visual story telling the refinement loops will need to use
screenshots and user feedback loops, both for the figure and the index page as a whole to get us to a solid top level
index page"

**Applied as:** the figure loop for the root page runs with him in it, iteration by iteration: each candidate is
screenshotted as rendered (desktop and phone width, light and dark) and sent to him in chat, his words come back and are
recorded, and the next iteration follows; the same loop then runs over the index page as a whole (prose, both figures,
the doors). The fresh-reader cold reads stay as the screen before his, not instead of it. WP51's good-enough is his word
on the whole page, not a unit's gates.

**Supervisor (2026-11-14 22:42 EST):** "remember you can tune on temperature to get a nice visual and just report the temperature you
used"

**Applied as:** the planted example's fit temperature is a free parameter of the figure: the unit may choose the
temperature that makes the three pieces read, and the caption states the temperature used (as the paper's figures state
theirs); the fit stays the one `fit_why()` fit at that temperature (R-1).

**Supervisor (2026-11-14 22:48 EST):** "i will add that once you do the work get the example plots in the top level index you should
also build an example in the documentation that explicates the synthetic case so anyone who sees the index and wants to
see how it was made can reproduce it with out us bloating the index"

**Applied as:** a follow-on to WP51, after the root page's figures settle: a docs example page for the planted
three-metric case (the table's construction, the fit at its stated temperature, the ternary and the slices drawn by
the same code as the root page's figures, each step runnable), linked from the root page's captions in one short clause
so the index itself stays lean. Scoped as its own unit once the figure passes his loop; its budget set then; it joins the
Examples page's journey ("See the worked case").

**Supervisor (2026-11-14 23:00 EST), on round 2 (the three terms at the median, temperature 10; image in chat):** "drawings look much
easier to interpret now. i would take this one as a baseline and still try to improve it. for me the most obvious
improvement would be if the fit frontier was pushed closer the the visible extent of the data. i am not expecting 100%
inside the envelope but right now it seems like the envelope is pretty conservative"

**Applied as:** round 2 is the baseline (kept in the loop record as such). Round 3 works on the gap between the surface
and the visible data in the slices, which has two sources: the planted table leaves parts of the surface unpopulated in
a median slice (the flat pieces sit above empty space), and the dots shown in a pane are designs within a band of the
held value, so they scatter below a slice that is exact. The unit tries the example first (designs planted along the
whole surface, mostly inside the band, so each slice's data reach its surface), then the display band (narrower, the
dots' shade by closeness to the slice), each cold-read; the fit's convention (the share of designs beyond the surface)
is not changed for the figure without his word, since it is the paper's.

**Supervisor (2026-11-14 23:01 EST):** "its fine if not every color appears on every row as long as all 3 colors appear in at least
1 row"

**Applied as:** a constraint relaxed for round 3: a row may show two of the three terms; the figure as a whole shows all
three; the unit need not plant the example so that every slice carries every term.

**Supervisor (2026-11-14 23:02 EST):** "its even okay if a row has only one term, as long as all 3 terms appear in at least one row"

**Applied as:** the constraint relaxed further: a row may show one term; the figure as a whole shows all three.

**Supervisor (2026-11-14 23:04 EST), with the ternary attached:** "optionally you can plot the diamond, the star and the square which
as i recall are specific designs. this become landmarks to help the reader navigate the coordinate transforms. this is
an optional add on if its confusing rather than helpful, drop it"

**Applied as:** an optional add-on for round 3, after the main change: the three designs the ternary marks (star,
diamond, square) drawn with the same markers in the slices' panes as landmarks across the three views, judged by the
cold reads and dropped if they confuse; what the three markers are is read from the ternary's code and kept the same.

**Supervisor (2026-11-14 23:06 EST):** "you have the code to map between coordinate systems. whether they are concrete designs or
attribute vectors or points in the metrics or values of the exponents. to me knowledge we have unique mappings"

**Applied as:** the landmarks are mapped, not matched: a point of the share simplex (a design's shares or a term's
exponent vector) fixes a ray in metric space, and V's homogeneity of degree one puts exactly one point of the surface on
that ray (t = 1/V(s)); from there the log-metric point and the chart point follow by the package's transform. So the
ternary's three markers can be drawn in every pane as points of the surface, with the slice's held value noted where
the point is off the slice. The unit draws them so and the cold reads judge.

**Supervisor (2026-11-14 23:07 EST), on round 3 as served (the re-planted table, the data reaching the surface in every slice; image in
chat):** "this is good. looking forward to seeing what it looks like with the landmarks"

**Applied as:** round 3 passes his read; the landmarks (the ternary's three markers mapped to their surface points) are
the next and last add-on of the night, judged by his read in the morning if he is asleep by then.

## The landmarks tried and dropped by the unit (2026-11-14 23:12 EST)

The ternary's three markers are the terms' exponent vectors read as shares (the point where each term's V peaks at a
fixed total); mapped to their surface points as ruled and drawn hollow in the slices and on the chart's line (render
`rework-round3-markers-light.png`). Two fresh readers: the one-sentence reading did not get worse, but both asked what
the markers are, one took them for landmark designs, and in the slices they sit off the drawn curve (their third metric
is not the held median) and read as stray points. The unit dropped them; the page carries round 3 without markers
(`wp51fig` 3bc5510, temperature 50 after the re-planting). The render was sent to him; his call stands over the
readers'.

**Supervisor (2026-11-14 23:23 EST):** "is there an alternative to using median that would make this work better. its okay if there is
not but i think its worth exploring a bit." and, with the chart column attached: "the third col where they fall on the
log V = 0 line looks quite good so i suppose another option would be to only plot them on that col; though for
consistency sake it would be great if we could address the question of how to make it look good on all 3 cols. we
still retain baseline option to not include the landmarks"

**The driver's reading:** the chart column works because the chart flattens the whole surface onto log V = 0 (a
projection), while the metric and log columns show a plane section at one value of the third metric, and three surface
points at three different values of that metric cannot lie on one section curve. The alternatives that keep few lines:
(a) the landmarks on the chart column only; (b) the surface drawn in the metric and log columns as a projection too, a
shaded band between its sections at the third metric's 20th and 80th percentiles with the median section on top, the
landmarks inside the band as surface points; (c) each row's section taken through one landmark's value instead of the
median (one marker exactly on each curve, the others off it). Round 4 tries (a) and (b), cold-read, and keeps the
baseline without landmarks as the fallback; (c) is held unless (b) fails.

**Supervisor (2026-11-14 23:23 EST):** "one more thing to remember, don't bloat the index with lots of detail about how the plots were
made. document and ensure reproducibility of the synthetic example in the documentation cite. provide a more minimal
narrative oriented caption and text in the index and link out to the example in the documentation"

**Applied as:** the index's captions and the how-section prose are cut to the narrative (what the picture shows and what
it means), with no construction detail (temperature, percentiles, band widths, the planted table's recipe); those go to
the docs example page that reproduces the synthetic case, and the index links to it in one short clause. The follow-on
unit for that page becomes part of the same work, not a later package; until it exists, the caption's detail is held
in the loop record, not on the page.

**Supervisor (2026-11-14 23:27 EST), on the root page's footer (image in chat):** "this should also have a placeholder link for pypi.
and probably a link to the documentation. the github repo can just say source code"

**Applied as:** the footer reads "Source code · Documentation · PyPI · Release notes · History and acknowledgements":
the repository link's text is "Source code"; a Documentation link to the docs home; a PyPI link to the project's page
(a placeholder until the first publish; the site tests allow it as the punch list names it). Applied by the figure unit
in its page edit, since it holds the file tonight.

**Supervisor (2026-11-14 23:29 EST):** "the call to action will need a minor update. we still want the two doors: one for reading paper
and one for using the code, but we may need to update it to fit in cleanly with the updated prose and visual content and
footer."

**Applied as:** the two doors stay (read the paper; use the code); their lead sentence and labels are redrafted to sit
after the slices figure and before the new footer, in the page's register, as one short paragraph; drafted by the
figure unit with the page and shown to him in the morning read of the page as a whole. The earlier ruling that the
summary paragraph and the two doors were "unchanged" is superseded for the doors' wording, not their presence.

**Supervisor (2026-11-14 23:32 EST), on candidate A (the landmarks on the chart column; image in chat):** "\"own\" in the \"term <k>'s
own point\" is confusing. what is the its point? it was derived from something what actually charactizes it, is it a
maximal point or something else"

**The driver's reading, to be confirmed against the code:** the ternary's marker for term k is the point of the share
simplex whose shares equal the term's exponents, which by the inequality of the means is where that term's monomial is
largest among points with a fixed total; mapped to the surface it is the term's peak on the surface. The legend and
caption name it by what characterises it ("term k's peak: where the term's share of each metric equals its exponent")
and "own point" goes. The glossary's "balanced point" is a different object (the dual-weighted mean) and is not used.

**Supervisor (2026-11-14 23:33 EST):** "we used the term own in the caption of the figure as well. should we call it the characteristic
point"

**Applied as:** the name is "characteristic point" (of a term): the point of the surface whose shares of the metrics
are the term's exponents, where the term's monomial is largest for a given total. It replaces "own point" in the
legend and both captions (the ternary's too) and "peak" in the driver's draft; it enters the glossary as one entry so
the docs example page and the captions use one word; the register rows follow.

**Supervisor (2026-11-14 23:34 EST):** "and its characteristic point is a peak?"

**The driver's answer (given in chat):** yes, in a precise sense, by the weighted inequality of the means: among points
with the same total of the metrics, a term's monomial is largest where the shares equal its exponents; equivalently, on
the term's piece of the surface the characteristic point is the point with the smallest total. The caption may say the
first; the glossary entry carries both.

**Supervisor (2026-11-14 23:34 EST):** "this will be more important for documenting the example and the plotting methods than the
narrative for the index page which just needs to be intuitive"

**Applied as:** the precise sense (largest for a given total; smallest total on the term's piece) goes to the glossary
entry and the docs example page; the index's caption says only what a reader needs to follow the markers ("each term's
characteristic point, where that term is strongest"), in plain words.

**Supervisor (2026-11-14 23:37 EST):** "and in the ternary plot the way we colored the region, what was that? is based on which of the
surfaces dominates? what does dominating mean? is there a better word? we had to calculate it so there must be a
specific rule used to determine which color goes here"

**The rule, from the code (`plotting._ternary_region_of`):** at a point of the triangle with shares c, each term's
value is its offset plus its exponents times the log shares, a_k + s Σ_j w_kj log c_j; the region is coloured by the
term with the largest value there, the code's word being "the binding term". At the exact-maximum fit V equals that
term there; at finite temperature it is the term that contributes most to V. For designs the glossary calls this
assignment the term's cell (the rows whose largest term it is); the coloured region is the same rule applied to every
point of the triangle. Candidate words for the page: "the largest term", "the term that binds"; "dominates" and "leads"
are the current words. His choice pending.

**Supervisor (2026-11-14 23:38 EST):** "i like the phrase which term \"binds\" if its technically accurate"

**The driver on accuracy:** at the exact-maximum fit the surface in log space is the upper envelope of the terms'
linear pieces, log V = max_k (a_k + w_k · log m), and the piece the surface follows at a point is the active one, which
is what "binds" means of a constraint that holds with equality; so the word is exact there. At a finite temperature V
is the log-mean-exp, a soft maximum, and no term binds strictly: the region's term is the one with the largest value and
the largest weight, and the soft surface lies within 1/τ of the binding piece. The page's figures are drawn at a
finite temperature, so the glossary entry says "binds" is the exact-maximum word and names the finite-temperature
reading; the captions use "binds".

**Applied as:** "each region is where one term binds" on the ternary's caption; the docs page and the glossary carry the
rule and the qualification; "dominates" leaves the plotting module's docstring in the same unit.

**Supervisor (2026-11-14 23:41 EST), after "so at finite temperature its which team dominates and at infinite temperature its binds?"
and the driver's note that "dominates" is Pareto's word in the paper:** "okay binds it is then"

**Applied as:** one word at every temperature: the term that binds. The glossary entry carries the exact-maximum sense
and the finite-temperature reading; "dominates" is not used of terms anywhere.

**Supervisor (2026-11-14 23:42 EST):** "we say binds based on the infinite temperature interpretation but clarify in the glossary (and
elsewhere if necessary) that the term “carries the largest weight” at a finite temperature"

**Applied as:** the glossary entry for the binding term: the term whose piece the surface follows at the exact maximum
(τ = ∞), the sense the word is used in; at a finite temperature it is the term that carries the largest weight. The
same clarification goes wherever the docs explain the regions or the cells (the docs example page, the tensions and
chart pages if they say "binds"); the index says "binds" alone.

**Supervisor (2026-11-14 23:44 EST), on the legend (image in chat):** "reorder the legend so its 3 line 1,2,3 in row one, then 3 points
1,2,3 in row 2. the cols need to align by color (term)"

**Applied as:** a two-row legend: row one the three term lines in order 1, 2, 3; row two the three characteristic
points in the same order under their term's colour; three columns, one per term.

**Supervisor (2026-11-14 23:57 EST), on the redrafted call to action's lead sentence:** "please avoid obnoxious LLM metanarration
\"You have now seen the same table three ways.\" qualifies. i need a standing rule against this kind of thing, you do it
all the time and i really don't want to spend all my review effort playing whack a mole"

**Applied as:** a standing rule in `CLAUDE.md` (Derivations and docs): no sentence whose subject is the text, the page,
the figure's placement or the reader's experience; the residual checker's metanarration patterns extended to the
reader-experience openers; the unit redrafts the lead and re-reads its captions under the rule; the driver re-reads
the root page, the docs home and the history essay for the same fault before the morning.

**Supervisor (2026-11-15 00:03 EST), with the ternary and the slices side by side:** "i need you to make sure these plots have terms
which are numbered and colored the same"

**Applied as:** one mapping from the fit's term index to number, colour and marker, shared by the ternary and the
slices by construction (one function both call), and a test that renders both from `fit_why()` and asserts the mapping
is the same; the ternary's own colour assignment is checked against the palette's order, since the two figures were
drawn by different code paths tonight.

**Supervisor (2026-11-15 00:09 EST):** "i don't know. in the versions i am looking at yellow is 1 in both but blue term is 2 in the
ternary and 3 in the 3x3, green term is 3 in the ternary but 2 in the 3x3" then "my bad maybe i am misreading green is 3
in both"

**Checked from the fit:** term 1 (0.53, 0.21, 0.26) amber, "all three trade"; term 2 (0.19, 0.05, 0.76) blue, "metric 3
trades against metric 1"; term 3 (0, 0.17, 0.83) green, "metric 3 trades against metric 2"; one colour function serves
both figures, so the mapping is the same in both; the test making it a guarantee is still being added.


## His review of the root page before the merge (2026-11-15, ~12:30 EST)

**Supervisor, verbatim (on the slices caption, screenshot in chat):** "this caption is overloaded. simplify it and
put some of the explanation in prose. drop "select the figure to open at full size"). direct the reader to the
example in the documentation in the prose. that serves as a transition sentence into the 2 door call to action. use
"cards" for the paper and the code rather than. bullet list."

**Applied as:** the slices caption is one sentence (the rows, the held metric, the three columns); the colouring of
the pieces and the characteristic points moved into the preceding paragraph; "Select the figure to open it at full
size" dropped from both captions; a lead paragraph before the doors says the table is constructed with three planted
terms and both figures are rebuilt step by step in the documentation's example, then the paper-and-documentation
sentence; the two doors are cards (`.doors` grid, `.card` links with a title and a line), the bullet list gone; the
root-page test follows.

**Supervisor, verbatim (the root page):** "table -> dataset"

**Applied as:** on the root page, the five uses of "table" for the data (both captions, the lead paragraph, the
paper-and-documentation sentence, the code card) read "dataset"; "the options on the table" and "documents and
tables" in his own paragraphs keep their words. The paper and docs keep "table" (the glossary's word) unless he rules
on them.

**Supervisor, verbatim (the held metric):** "okay, then is the median the right value to take. i wonder if the
quantile should slide with temperature choice." then "okay. we'll accept the top page as it is but make sure the
plotting methods have an option to use a different quantile value, rather than hardcoded as median"

**Applied as:** the root page accepted as it stands (the median, stated); `scripts/build_site_figures.py` takes a
`quantile` on `held_at`, `draw_slices` and `build_slices` (0.5 by default), the row title following it
(`held_label`), with a test; the docs example names the option. The band-conditioned section (the held value as
the median of the near-frontier designs, which moves with tau) is carried to WP56 as a question for the case figures.

**Supervisor, verbatim (an idea, by his word not a suggestion):** "i wonder if imputing at the value of the relevant characteristic point would have landed the characteristic points on the curves in an intuitive way" ... "that could be too big a stretch though. it was an idea not a suggestion"

**Recorded as:** an option for WP56's case figures (hold the third metric at one term's characteristic value, which puts that term's point on the section; one point per pane, or three sections); not applied.
