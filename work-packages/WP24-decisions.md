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
