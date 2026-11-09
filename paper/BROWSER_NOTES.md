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
- The supporting-material page measures 378 px at 375 px; no element outside a scrolling container
  reaches that far, and the cause was not found.
- Clicking an author-year link of a reference that the list has not yet opened ("Show All" closed)
  does not scroll, because the entry is not on the page until the list is opened.
