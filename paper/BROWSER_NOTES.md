# Browser notes for the reviewer (WP10 main text)

Built with `cd paper && uv run myst build --html` (no warnings, no unresolved cross-references),
served with `python -m http.server 8793 --directory paper/_build/html`, viewed at 1280 px and 375 px.
The theme is dark by default (the toggle exists); light mode was not viewed.

- Title, byline, abstract and keywords render; the table of contents lists sections 1 to 12 and
  "Works cited"; the Acknowledgments render as a part after "Works cited" and the numbering reads
  "14 Works cited".
- Theorem-style blocks render as coloured boxes with the badge, hypotheses and statement; each
  sketch is a "Proof n (Sketch)" box and each script pointer a green "Script" box. Numbering is per
  kind: Definition 1 to 9, Theorem 1 to 9, Proposition 1 to 3, Lemma 1 and 2; Corollary 4 is
  unnumbered with its number typed in the title. Titles read "Name (Ln)", which nests parentheses.
- The family table renders, but its Cites column shows raw `[@key; @key]` text, not citations (the
  generated table is raw HTML output; `paper/generate_prior_art.py` is not changed here).
- At 375 px the page has no horizontal scroll (document width 375), all figures scale to 351 px, and
  the two tables scroll or clip inside their containers: the family table scrolls, the candidates
  table (embed) is wider than its container and its overflow is visible.
- All 8 figures and 2 tables carry numbered captions; the generated sentences of sections 2, 8 and 9
  render in place as plain text.
- Screenshots after a deep scroll did not update in the pane (it kept showing the same frame), so
  the lower sections were checked through the page text and element sizes, not by eye.
