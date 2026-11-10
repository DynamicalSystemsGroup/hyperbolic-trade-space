# WP24 — Decision records (the vocabulary rename)

Origin: `WP10-decisions.md`, "The word facet" (the supervisor's proposal, the spike, "Everything before 0.1").
Approval: the driver under the mandate, 2026-11-09, 22:50 (gate line in the scope).

## Two details the scope left open (2026-11-10, 00:35; the driver)

- `examples/adcs/model_v2/diagnostic_pair.py` (on the never-list, but it calls `case.facet_table` and reads `facet_`
  attributes): WP23's stream changes it in its own unit right after WP24's push 1, identifier renames only. The
  never-list stays honest and the file keeps its one writer.
- `CHANGELOG.md` is a reader surface and gets the vocabulary; `paper/BROWSER_NOTES.md` and the design spec are
  records and keep their wording.
- The spike report is cited by its last commit, d1efdfe (deleted from the tree by WP25; history keeps it).

## Push 1's question: old identifiers in a record a test reads (2026-11-10, 06:35; the driver)

`tests/test_narrative.py` checks that function names cited in `docs/superpowers/notes/paper-sources/method.md`
exist; the note is a record (A5) and cites four old names. Decision: (b), the identifier-only edit to the record,
recorded as an amendment of A5: a record keeps its wording, but a code identifier is not wording, and a map that
keeps old names alive in a test is the drift the package exists to remove. The same rule for any other record a
test reads. No map.

**Push 2's question, the same seam on quoted statements (06:45).** `tests/test_narrative.py` requires
`docs/superpowers/notes/paper-sources/method.md` to quote the ledger's R2 word for word, and the ledger now says
"term". Decision: (2). The paper-sources notes are the paper's source text, not decision records, so A5 is amended:
`docs/superpowers/notes/paper-sources/*.md` take the vocabulary by identifier and word edits, and both test maps
are dropped. Decision records (`WPn-decisions.md`, the supervisor's quotations, `PROOF_MAP_FINDINGS.md` section 10)
keep their wording. R1's polyhedral "facet" in Appendix B carries the exempt marker (push 4).

**Push 2 landed (a5c67f2, 27dab4d, 9b1152e, a9e23b2; 2026-11-10, 07:20).** Linux dispatched on the head after it
(c37197c and the board) with the two paper register tests known red until the paper unit. On 7fad5ff (a text-only
citation row in `derivation/PROOF_MAP_FINDINGS.md` pushed by WP25-2 without an Appendix B regeneration): no revert;
the file is a findings record not compiled into Appendix B as the record shows, and the paper unit's container run
runs the Appendix B test, which settles it; a failure there is fixed forward. The `coverage.csv` column names
staying as enum types with the caption as the bridge: accepted as the PM's call.

**Pushes 3 and 4 landed together (9df7483, 1b1249d, a2e6bd5, ee7704e; 2026-11-10, 09:30).** The vocabulary tool
reads no "facet" outside the three marked polyhedral sentences; the paper's output cells are byte-equal after the
rename (no number moved); the docs home glosses "a monomial term (a product of powers of the metrics) is one
trade-off". Linux dispatched on ee7704e. Two items from push 4, the driver's calls: (1) `site/paper-map.webp` on
the root page is a raster from the external review with no source in the repository and stale words in the
image; it goes (negative edit; a map with a source may return as a candidate for the supervisor's review), the
root page's caption and alt text with it. (2) Appendix E's HTML table shows raw `$...$` math on the staged page:
fixed in the close-out's paper regeneration (a rendering defect on staging, not published).
