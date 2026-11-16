# WP57d: the unit's cold read of the rendered appendices E and H (1,280 px)

The built site (`cd paper && BASE_URL=/paper uv run --frozen myst build --html`, a clean log) served on port 8893,
captured headless by Playwright (Chrome) at 1,280 by 900. Page checks by the capture script: "Job." occurs nowhere on
the supporting page; every anchor `appendix-e`, `sub-e-1` to `sub-e-3`, `appendix-h`, `sub-h-1`, `sub-h-4`, the three
table labels and `proof-l12` resolves; no in-page link points at a missing id; "H.5" is not on the page; OQ-1 to OQ-10
and OQ-12 to OQ-14 are on the page and OQ-11 is not; page scroll width 1,280 (no horizontal overflow of the page).

| Capture | What a reader meets | Found | Done |
|---|---|---|---|
| `E-top.png` | The heading, E.1, Table 1's caption naming the ledger, the fifteen A and R rows with the section that states each and the lemmas that import it, each lemma a link to its proof in B | A0 reads "not in the main text", true: A0 is structural; the one-line statements are the ledger's words (ASCII mathematics, as B prints them) | nothing |
| `E1.png` | The same table from E.1's heading | as above | nothing |
| `E1-cited.png` | Table 2, I1 to I18 and F5 to F19, with citations | the "Used by" column wraps "none: cited as context" to three lines; I16's citation carries the ledger's "to be confirmed by the author" note, which is the record's own state | nothing; the citation is the ledger's and is not retyped |
| `E2.png` | E.2's table: section, what is not established, record; Definitions, Theorems and Appendix subsections as links | each row is one item; records resolve (Definition 5, Theorem 2, D.4, ...) | nothing |
| `E2-gaps.png` | Table 3, the gaps in four columns, each gap's title a link to its line of the ledger | first build: the fourth column ran past the text column into the table's own scroll (widths 150 + 3 x 300) | widths set to 120 + 3 x 230 (`generate_gaps.WIDTHS`); recaptured, all four columns in view |
| `E3.png` | E.3's table: thirteen open questions in the ledger's order, each id a link to the ledger, then the two research questions of Section 9 | OQ-14's section is D.19 (its record is the generator and the stability record, not a paper section) | nothing |
| `H1.png` | H.1 opens on HoroPCA and this work, then the hypothesis; no sentence about the appendix | the Job block and C591's sentence are gone; H.2 and H.3 follow unchanged | nothing |
| `H4.png` | H.4, the slab sentence, the reading limits (a) to (c), then one line linking the note on the formalism and the solvers; the references; the page ends | H.5's heading is gone; the citing line is the appendix's last sentence | nothing |
