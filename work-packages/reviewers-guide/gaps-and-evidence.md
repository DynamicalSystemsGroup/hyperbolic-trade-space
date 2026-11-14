# Known gaps, and where the evidence lives

## Known gaps

Each is stated once, with where it is tracked.

- **The final reader round has not run.** Plan and briefs are in the assistant's scratchpad, not in the repository;
  the settings are in `work-packages/WP11-decisions.md`. Until it runs, no paper or package cell of the grid is
  accepted for the reader columns (`work-packages/deliverables-grid.md`, "Reading the grid").
- **The residual pass did not make every surface read clean.** 78 of 96 confirmation rows still carry flags, mostly
  long sentences (kind 9) and terms used before their definition (kind 10). The 163 lemma-script rows and the history
  page's rows are held for their owners (`work-packages/WP38-review.md`).
- **Docs-site build tests.** `tests/test_site.py` and `tests/test_docs.py` fixtures failed in the WP38 review
  worktree (2 failed, 11 errors; a MkDocs 2 warning banner on stderr). They were green on earlier heads; a re-run on
  a clean checkout is open (`work-packages/PM-BRIEF.md`, handover of the fourteenth PM, open item 1;
  `work-packages/WP38-review.md`, "Gates").
- **Version and changelog.** The version reads 0.0.1 and `CHANGELOG.md` still reads "Unreleased"; both change last
  (`work-packages/WP8b-release-checklist.md`, A1 to A3).
- **Container regression at the release head.** Recorded at the WP30 data gate only (`paper/container/RECORD.md`).
- **Checks that exist only after the tag and the merge.** The releases-widget 404 and the GitHub links on a private
  repository (`work-packages/WP8b-release-checklist.md`, G1 and G2).
- **Reader grid, worst cells.** Not reported until the final round.
- **Windows.** The docs-paper shard runs on Linux and macOS only (`work-packages/WP34-decisions.md`).
- **After 0.1.** Search (WP12), PyPI, the PDF export, a registry image (`work-packages/release-punch-list.md`).
- **Appendix H citation parentheses** render without parentheses; the fault is in the site theme
  (`work-packages/WP38-review.md`, open items).

## Evidence index

| Record | Path | Owner |
|---|---|---|
| Work-package board and gates | `work-packages/README.md`; `work-packages/parallel-board.md` | PM |
| Scope, decisions and review per package | `work-packages/WPn-scope-of-work.md`, `WPn-decisions.md`, `WPn-review.md` | the package's driver |
| The calls made for the supervisor | `work-packages/supervisor-review-list.md` | assistant |
| The assistant's log | `work-packages/driver-log.md` | assistant |
| The grid of deliverables | `work-packages/deliverables-grid.md` | PM |
| The release checklist | `work-packages/WP8b-release-checklist.md` | assistant |
| The punch list | `work-packages/release-punch-list.md` | PM |
| Changed numbers | `work-packages/swap-evidence.md`; `work-packages/WP30-rounds/data-gate/conclusions.md` | assistant |
| Residual pass | `work-packages/WP38-review.md`; `work-packages/WP38-flags/`; `work-packages/WP38-confirmations/`; `work-packages/WP38-landed/`; `scripts/residuals_baseline.json` | assistant |
| Container record | `paper/container/RECORD.md`; `paper/container/README.md` | assistant |
| Reader rounds | `work-packages/WP11-decisions.md`; `work-packages/WP11-round-1/`; `docs/superpowers/notes/reader-grid.md` | assistant |
| Screenshots | commit `2a669de` (`git show 2a669de:<path>`; see `work-packages/README.md`) | PM |
| CI run links | `work-packages/driver-log.md` | assistant |
