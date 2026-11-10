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
