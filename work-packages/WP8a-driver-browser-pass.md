# WP8a — The driver's browser pass on the staged site (first pass)

2026-11-08, by the driver, in the built-in browser, on the site staged from a clean checkout of
`dev` at 6bb85e7 (`scripts/stage_site.py --serve`, 127.0.0.1:8000). Rule: `PM-BRIEF.md`, "Reviews
that pass through the browser are done in the browser".

## What was looked at, and what was not

- Looked at, rendered, top to bottom: the root page; all sixteen docsite pages (Home, Getting
  started, the eight User guide pages, API, API reference, Examples, Theory in brief, Glossary,
  Further reading); the paper's page (still the placeholder). Each at 1280 px in the light scheme
  and at 375 px in the dark scheme, with a capture per page and layout measurements (page and
  element overflow, code and table scrolling, mathematics rendered or raw, images, headings).
- Spot-checked only: 375 px in the light scheme and 1280 px in the dark scheme (two pages each).
- **Not done in this pass:** using the navigation drawer on the phone width, following every
  in-page link by clicking, the search box. They are done on the second pass, after the fixes.

## What is sound

No page scrolls sideways as a whole at 375 px. Navigation and the table of contents are present on
every page. Light and dark both render, and the docsite follows the reader's system preference on
a first visit. Mathematics renders where it is used (Theory, Limitations, Further reading) with no
errors. Citations render as footnotes with links. The glossary is alphabetical with letter
headings. The API reference shows no lemma, axiom or specification tags.

## Findings

| | Where | Finding | Kind |
|---|---|---|---|
| R1 | Root page, "How" | The map is unreadable at the size shown at every width: 694 px wide on a 1280 px screen and 333 px on a phone, from a 1536 px image, with no link to a larger view. It is the only content of "How" besides one paragraph. | major |
| R2 | Root page, Package card | The install command breaks across three lines in the middle of words. | minor |
| R3 | Paper placeholder, Documentation card | "the method is documented in full, page by page" and "The method, its mathematics and its limits" describe the docsite as it was before it was thinned. | leftover wording |
| D1 | The whole docsite | Sixteen pages and not one figure. The page "The chart, holes and plots" names six plotting functions and shows no plot; the Tensions page describes the report and shows nothing; Examples shows no result. | major |
| D2 | Getting started, Conditioning, Tensions, Chart, Prediction | At 1280 px a code block needs sideways scrolling; on Getting started the first example a user meets is cut in the middle of its import line. | major |
| D3 | API (overview table), Termination (statuses table), API reference (parameter tables), at 375 px | Tables do not fit: the API table's last column is cut off with nothing to show it scrolls; identifiers are broken into fragments; the parameter tables cut the description column. At 1280 px the API table still breaks function names mid-identifier, and the API reference is 28,000 px of tables. | medium |
| D4 | Theory in brief, at 375 px | The first display equation is clipped at the right edge; "sum of w_j = 1" cannot be read. | medium |
| D5 | Fitting, Chart, Tensions | Sentences carry long runs of attribute names in code font (fifteen in one paragraph on Fitting); one paragraph on Chart exceeds 110 words. Hard to scan. | minor |
| D6 | Docsite pages | One request fails with 404 in the browser console on a docsite page. | minor |

## The driver's calls on these (recorded in `driver-log.md`)

- **D1 reverses an approved default** ("the Examples page links only, no figures copied"; the
  docsite as text and code only). A user guide for a method whose output is read from plots needs
  the plots. The docsite gains a small set of figures, at most seven, each generated at build time
  by the package's own plotting functions from the synthetic data of the code block directly above
  it, with a caption underneath. None is copied from the paper.
- **R1:** now, the map links to its full-size file and may use the full width of a wide screen.
  Whether the map itself is redrawn with fewer, larger labels is left to the reader loops, where
  readers at the first depth will show whether it works.
- **D3:** the two hand-written tables become lists that do not need columns on a phone; the API
  reference renders parameters as lists instead of tables.
- D2, D4, D5, D6, R2, R3: fixed as found; a test keeps docsite code lines within the column.

## Second pass (2026-11-09, clean checkout at 7656157, the same server and browser)

Looked at again, rendered: Getting started, Fitting, Tensions, Chart, Examples at 1280 px light;
the docsite home, Termination, Theory in brief, API and the root page at 375 px dark; and the
behaviours left out of the first pass: the phone navigation drawer (opened, the User guide section
entered, Termination reached through it), the search box (a query for "exchange rate" returns ten
documents with Theory in brief first), and the root page's map as a link.

| Finding | State |
|---|---|
| R1 map unreadable | the map now links to its full-size file; the redraw question stays with the reader loops |
| D1 no figures | **fixed:** seven figures, each under the code that draws it, with a caption and alternative text, in a light and a dark version that follow the page |
| D2 code scrolling sideways at 1280 px | **fixed:** no code block scrolls on the five pages |
| D3 tables on a phone | **fixed:** the API overview and the termination statuses are lists; the API reference renders parameters as lists |
| D4 clipped equation | **fixed:** the invariant form breaks over two lines at 375 px |
| D6 console 404 | no failed request on the root page or Theory in brief |
| R3 stale placeholder | superseded: the staged `/paper/` is now the built paper |

Not yet re-checked: D5 (attribute inventories) page by page, R2 (the install command in the card).

New, smaller observations for the loop:

- Getting started's first figure is an unstructured cloud of points in two position coordinates. It
  is the first picture a newcomer sees and it does not show the idea. Colour the points by log V,
  or show the two-metric log plane with its frontier line there (the Chart page's first figure
  does show the idea).
- Search result previews show raw LaTeX source. A known limit of the site generator; left.
- The staged paper shows Figure 1 twice in succession, and its sections are still shells. The
  three panes match the supervisor's specification (kinked; piecewise linear; flat line with
  coloured regions). The paper is WP10's and is not judged here.
