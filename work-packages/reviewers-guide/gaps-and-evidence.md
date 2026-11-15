# Known gaps, and where the evidence lives

## Known gaps

Each is stated once, with where its record lives.

- **The bridge page's page requests.** The fresh reader of the bridge page asked for: the temperature (tau), the
  feasibility conditions, the factor 2, the word "submartingale", a stale code comment (the "log V = 0" one), and the
  word "holes" in one sentence. They are held for the assistant to weigh. Record: `work-packages/WP41-review.md` (the D-5 read).
- **The WP43 figures' bytes.** After the lint pass the three spike figures regenerate with the same data but not the
  same bytes; the committed figures are kept and the readout's claims stand on the data files. Record:
  `work-packages/WP43-rounds/spike/rerun-record.md`.
- **The residual pass did not make every surface read clean.** 78 of 96 confirmation rows still carry flags, mostly
  long sentences (kind 9) and terms used before their definition (kind 10); the 163 lemma-script rows and the history
  page's rows are held for their owners. Record: `work-packages/WP38-review.md`, "Open items for the supervisor: the
  post-0.1 list".
- **Held-out and core reader findings routed to you.** The abstract's phrases (change request 172), the title's
  "Scaling" and "hyperbolic", the two senses of "invariant", the n-lemma name, the DEA comparison, "machine-checked",
  the case model's gain ranges, the Spearman rule (0.97 against 0.99) and the rest. Record: the section "Findings of
  the final reader round routed to the supervisor" in `work-packages/supervisor-review-list.md`; the readers' words in
  `work-packages/WP11-final/triage/`.
- **Container regression at the release head.** Recorded at the WP30 data gate only. Record: `paper/container/RECORD.md`.
- **The release workflows have never run on GitHub.** The admissibility workflows act only from the default branch
  and the issue-event ones need their files there; the labels `draft` and `small-fix` do not exist yet; the changelog
  check refuses until `[Unreleased]` becomes `[0.1.0]`. Record: `work-packages/WP47-rounds/checks.md`;
  `docs/code-owners.md`.
- **Version and changelog.** The version reads 0.0.1 and `CHANGELOG.md` reads "Unreleased"; both change last.
  Record: `work-packages/WP8b-release-checklist.md`, A1 to A3.
- **Checks that exist only after the tag and the merge.** The releases-widget 404 and the GitHub links on a private
  repository. Record: `work-packages/WP8b-release-checklist.md`, G1 and G2.
- **Repository hygiene.** Instance 4 of the cleanup deleted 97 merged local branches and three retired remote
  branches, and removed four worktrees, after a bundle of every ref was taken; branches went from 119 to 22.
  Batch 2 follows the deliveries. Record: the manifest and owner map in `work-packages/WP25-rounds/instance-4/`;
  the bundle `hts-before-cleanup-2026-11-15.bundle` in the maintainer's backups folder.
- **Windows.** The docs-paper shard runs on Linux and macOS only. Record: `work-packages/WP34-decisions.md`.
- **After 0.1.** The search (WP12), the work WP50 names (holes by persistent homology, its dependency and first
  package), WP48's checks as release gates, the package interface and the Monte Carlo demonstration of WP41's second part,
  the three example pages for WP45's records, PyPI publication beyond the first release, the PDF export, a registry
  image. Record: `work-packages/milestones.md`; `work-packages/release-punch-list.md`.
- **Appendix H citation parentheses** render without parentheses; the fault is in the site theme. Record:
  `work-packages/WP38-review.md`, open items.

## Evidence index

| Record | Path | Owner |
|---|---|---|
| Work-package board and gates | `work-packages/README.md`; `work-packages/parallel-board.md` | PM |
| Scope, decisions and review per package | `work-packages/WPn-scope-of-work.md`, `WPn-decisions.md`, `WPn-review.md` | the package's driver |
| The calls made for the supervisor | `work-packages/supervisor-review-list.md` | assistant |
| The assistant's log | `work-packages/driver-log.md` | assistant |
| The two-milestone board | `work-packages/milestones.md` | assistant |
| The supervisor's tasks | `work-packages/supervisor-tasks.md`; `work-packages/WP47-rounds/pypi-checklist.md` | assistant |
| The grid of deliverables | `work-packages/deliverables-grid.md` | PM |
| The release checklist | `work-packages/WP8b-release-checklist.md` | assistant |
| The punch list | `work-packages/release-punch-list.md` | PM |
| Changed numbers | `work-packages/swap-evidence.md`; `work-packages/WP30-rounds/data-gate/conclusions.md` | assistant |
| Residual pass | `work-packages/WP38-review.md`; `work-packages/WP38-flags/`; `work-packages/WP38-confirmations/`; `work-packages/WP38-landed/`; `scripts/residuals_baseline.json` | assistant |
| Container record | `paper/container/RECORD.md`; `paper/container/README.md` | assistant |
| Reader rounds | `work-packages/WP11-decisions.md`; `work-packages/WP11-final/`; `docs/superpowers/notes/reader-grid.md` | assistant |
| Research spikes | `work-packages/WP41-rounds/`, `WP43-rounds/`, `WP48-rounds/`, `WP50-rounds/`, `WP52-rounds/` | assistant |
| Cleanup | `work-packages/WP25-rounds/instance-4/` | assistant |
| Screenshots | commit `2a669de` (`git show 2a669de:<path>`; see `work-packages/README.md`) | PM |
| CI run links | `work-packages/driver-log.md` | assistant |
