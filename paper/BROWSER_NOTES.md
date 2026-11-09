# Browser notes for the reviewer (WP10 main text, after the fixes of the five findings)

Built with `cd paper && uv run myst build --html` (no warnings, no unresolved cross-references),
served with `uv run python -m http.server 8794 --directory paper/_build/html`, viewed in the
Browser pane in light and in dark mode, at 1280 px and at 375 px. Spots were viewed by eye (title
and abstract, Figure 1, the family table, a theorem block with its sketch and script box, the
candidates table, the end matter) and the whole page was measured in the DOM (visible tables,
images and code, overflow, link colours, heading order). The pane did not redraw after a deep
scroll at 375 px (it kept the previous frame), so at 375 px the lower sections, the candidates
table among them, were checked by their DOM measurements, not by eye.

## What was fixed and how it was seen

- **Citations in the family table.** The generated table is an output cell, which the site does not
  parse for citations (a `text/markdown` output is shown raw), so each key is an author-year link
  (`Charnes et al. 1978`) to its entry in the reference list. A hidden cell (`remove-cell`) cites
  every key, so that the list holds the entry; the list shows 52 entries once "Show All" is pressed
  (the site opens it at 15) and every link of the table finds its target. The links take the text
  colour and are underlined: the site's default colour for a link in an output (dark blue) was
  unreadable on the dark page. No raw `[@key]` remains on either page.
- **Candidates table at 375 px.** It sits in a container that scrolls sideways (parent 331 px, table
  552 px, `overflow-x: auto`); the family table likewise (351 and 480 px). The document is 375 px
  wide on the paper's page. Every generated table of the appendices is wrapped the same way.
- **Acknowledgments.** The site lifts a heading named exactly "Acknowledgments" out of the flow and
  prints it after the bibliography. The heading is now "Acknowledgments and process": section 13,
  before 14 "Works cited". (The test list of section headings carries the new name.)
- **Cross-references.** Every "Section n", "Table 1" and "Appendix X" of the main text is a link
  (MyST `numref` and `ref` roles); section numbers are printed by the site from the heading labels
  `(sect-...)=`, the appendix targets are `(appendix-a)=` to `(appendix-g)=`. The proof pointers
  "Appendix B, Ln" link to Appendix B. A per-proof label such as `(appendix-b-L3)=` is not possible:
  the proof headings are produced inside one output cell (raw HTML, where a label is not read), and
  a link to the `proof-l3` anchor in that output is reported as an unresolved cross-reference. The
  anchors `proof-l1` to `proof-l14` exist on the page for a reader's own link.
- **Figures and tables were shown twice** (not on the list of findings): each embedded cell had
  `remove-input` only, so the output appeared in place and again under the caption (seven figures
  and both tables). The cells are now `remove-cell`; an embedded table drops the embedded cell's
  input with the directive option `:remove-input: true`. Eight images and two tables are visible,
  each once.

## Seen and unchanged

- Dark mode: the figures keep their white backgrounds; text, tables, theorem boxes and the script
  box read well.
- Theorem-style blocks render as coloured boxes with badge, hypotheses and statement; each sketch is
  a "Proof n (Sketch)" box and each script pointer a green "Script" box with the link. Titles read
  "Name (Ln)", which nests parentheses.
- The family table's cells are centred or right-aligned by the site's table style.
- The supporting-material page measured 378 px at 375 px (cause found and fixed in the pass below).
- Clicking an author-year link of a reference that the list has not yet opened ("Show All" closed)
  does not scroll, because the entry is not on the page until the list is opened.

## Pass after the driver's change requests (2026-11-09)

Built with `cd paper && uv run myst build --html` (no warnings), served with
`uv run python -m http.server 8796 --directory paper/_build/html`, viewed in a tab of my own in the
Browser pane. Light and dark (the page's theme class, set and read back) at 1280 px and at 375 px.
Viewed by eye: the main-results list and organization paragraph; the Level paragraph and the Level 1
block (Theorem 10); the stopping declaration and the Numerical line; the Open questions and the
search section; the case analysis from its opening to the candidates table, with the figure and
table references; on the supporting page G.2 (the reading pass), D.8 (the status paragraph), D.13
and Appendix A. The pages were not scrolled end to end by eye: the pane is 800 by 569 points, the
main page is 27,000 px and the supporting page 73,000 px at 1280 px, so the rest was measured in
the DOM (below).

- **Cross-references to floats.** The page has ten links to a figure or table in the running text
  (Figure 1 to 8, Table 1 and 2), each to its own target; Table 2 and every figure are now
  referenced (test `test_every_figure_and_table_is_referenced_from_the_text`).
- **Defects of the review, fixed.** "Definition Definition 9" is gone (the role prints its own
  kind); "[Math Processing Error]" is gone (`conditioning_` is in code font in Appendix A);
  no interval stands in parentheses in a generated sentence; the regressor's band is called its own.
  DOM check on both pages: no "Math Processing Error", no "Definition Definition", no raw `$...$`
  text once the page has loaded, no "external reviewer".
- **375 px overflow of the supporting page (3 px), cause and fix.** The anchor mark of a heading is
  a zero-width inline box moved 10 px to the right (`translate-x-[10px]`); after a heading whose
  text fills the line, here "B.1 The fit and its geometry (L1 to L11)", the glyph leaves the page by
  3 px and the whole page scrolls sideways. Found by hiding elements until `scrollWidth` fell.
  `paper/style.css` (the template option `site.options.style`) clips the article's horizontal
  overflow below 640 px (`overflow-x: clip`, which makes no scroll container). After the fix
  `scrollWidth` is 375 on both pages; tables still scroll inside their own containers.
- **Raw dollar signs before the mathematics appears.** Not fixed: no template option controls it.
  The text sits in output cells (raw HTML) that the page typesets with MathJax after it loads, so
  the dollar signs show for a moment. Left as the review recorded it.
- **Reference list shows 15 entries until "Show All".** Not fixable by a setting: the article theme
  takes the limit as a component default (`hideLongBibliography`, 15) and `template.yml` has no
  option for it; the hidden entries are not in the page until the button is pressed.
- **G.2, the reading pass (56 rows).** The table is wider than a column and scrolls inside its
  container at 1280 and 375 px (the site's table style fixes the column widths); long addresses wrap
  inside their cell. Readable in light and dark.
- **Seen and unchanged.** A generated sentence prints in a smaller type than the prose around it;
  the Level 1 block is Theorem 10 (the site numbers a kind in order of appearance, and the block
  stands before Lemma 1 as the algorithm's order asks); proof boxes are numbered by their position
  ("Proof 12" for Theorem 10).

## Pass after the cold-read change requests (2026-11-09, round 2)

Built with `cd paper && uv run myst build --html` (no warnings; it prints a line that a server
started on port 3000, the builder's own temporary server, which stops with the build; Appendix F
now says so), served with `uv run python -m http.server 8797 --directory paper/_build/html`, viewed
in a tab of my own in the Browser pane, light and dark (the page's theme class, set and read back),
at 1280 px and at 375 px, scrolling to each changed place. Viewed by eye: the abstract; section 1
(what scales, the nondominated sentence, the main-results list); the definitions (the n-lemma, the
band, the chart, the share); Methods (the target sentence, the participation sentence); a proof box
with a worded label (L3); the margin sentence and Open questions; the start of section 9 (the
recovery sentence, the K = 1 sentence), the K = 3 association figure and its caption, the K sweep
sentence; on the supporting page D.14 (dark, 375 px). Measured in the DOM: `scrollWidth` is 375 on
both pages at 375 px; every new heading and table is present once the page has loaded.

- **Panel titles.** Each association panel is titled with its count and what it counts ("facet 1:
  6-lemma (6 metrics in the exact-maximum support)"); the outlined squares on the diagonal are the
  members (six in facet 1, counted in the image), and a member can carry w = 0.00 in its label (the
  settling time of facet 1); the caption says both. The figure is 21 inches wide and is shown at 40
  percent, so a title is small on the page; the caption carries the claim in text.
- **First frame after a theme change or a jump is blank or stale** (white or black): the pane does
  not redraw until it is scrolled or waited on; a second look showed the page. Not a page defect.
- **Text of the generated sentences** prints in a smaller type than the prose around it (unchanged
  from before). The nondominated sentence now stands in section 1 and shows the same.
- **Candidates table** is no longer in the main text (Appendix D.7); the page has eight images and
  one table in the text.
- **D.14 at 375 px:** the table of failures scrolls inside its container (the status column is
  cut at the edge until scrolled); dark text is `rgba(255,255,255,0.87)` on `rgb(28,25,23)`.
- Not viewed by eye at 375 px: sections 1 to 8 of the main text (measured only), and the dark
  frames of the changed places other than D.14 (checked by the theme class and the colours).

## WP10, second-review gaps G-4 to G-8 (1280 px, light and dark)

- Rendered and read: the abstract ("On one case it scales where dominance does not ...", "Every
  derived statement points to its script and its step-by-step proof"); section 1 (document-based and
  model-based citations split between Henderson and Madni; the contribution sentence "On this case");
  section 2 (Pareto paragraph ending in an Open reading; "on this case"; DEA without the N linear
  programs clause); Methods R2 sentence ends with a full stop; section 7 limits sentence.
- Light and dark both read; no layout change. The pane lagged one frame after the theme change.

## WP10, facet matching, legible figures, Table 1, subsection links (1280 px light; 375 px dark)

Built with `cd paper && uv run myst build --html` (no warnings), served on port 8801 from
`paper/_build/html`, viewed in a tab of my own in the Browser pane; the server is stopped.

- **Figures.** The figure column is 842 px at 1280 px. All figures are now 8 in wide at 100 dpi
  (792 to 793 px) and shown at scale 1.00, with 9 pt type (12.5 px) as the smallest text; Figure 1
  (1640 px, shown at 0.51) has 9 pt as its smallest type, 12.8 px. Panels stand one per row. Figure
  6 (three association maps) is 22 in tall; each panel reads without zooming (viewed). The
  `enlarge` link under each caption opens the file the site serves from `/build/` (eight links, all
  resolve).
- **Table 1.** Four columns (family with its sources in small type, then three short phrases);
  793 px tall where it was 1663 px, one screen at 1280 px; the cells are left-aligned (the notebook
  output style right-aligned them; `style.css` overrides it). At 375 px the table scrolls sideways
  inside its container (the last column is cut at the edge until scrolled); the page itself does
  not (`scrollWidth` 375, dark).
- **Subsection links.** `supporting-material#sub-d-7` and `supporting-material/#sub-d-13` land with
  the heading at the top of the viewport (D.7, D.13); the link in a generated sentence
  (`supporting-material/#sub-d-14`) is underlined and takes the text colour.
- **Remaining.** At 375 px an image is scaled to the column (about 0.43), so figure text is about
  5 px there; the `enlarge` link is the remedy on a phone. As before, the pane shows a stale frame
  after a jump or a theme change for a second. A figure link shows a download mark (the site's
  rendering of a link to a file).
