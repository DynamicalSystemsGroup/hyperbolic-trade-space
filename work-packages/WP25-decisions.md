# WP25 — Decision records (repository tidiness, a recurring package)

## Origin (2026-11-09, 22:20)

**Supervisor (mzargham), verbatim:** "i appreciate you clean up all the images, i think we are also starting to
accumulate a pretty big documentation cruft/drift/gap i want you to periodically deploy clean up work packages to
address repo tidiness, this is essentially context management. the git history keeps everything so tidying doesnt
eliminate history, history keeping is gits job the repo state itself does not need to duplicte that effort"

**Disposition (the driver).** A recurring package, one instance scoped small at each gate of the path and once more
before the PR; the PM scopes each instance for the driver's approval. Three parts, each with a check: (1) cruft:
files the repository no longer uses (spike folders whose result is in a decision record or a note, raw reader
reports and slices after triage, superseded reports, retired scripts, outputs no test or page reads) are deleted,
since history keeps them; the records of the gates stay (each package's scope, decisions and review); the check is
an inventory of every file not referenced by the docs navigation, a test, a script, the paper or another live
document, with its disposition; (2) drift: the docs and notes say what the code and the glossary say now (the
vocabulary tool, the claims register, doctests, and a read of each docs page against the current API and
defaults); (3) gaps: what exists in the code or the paper with no documentation, listed and either filled or
scheduled. The repository state is the present; the history is git's. Step 3h on the path (recurring).

## Approval, instance 1 (2026-11-09, 23:20)

By the driver under the mandate (`release-candidate.md`); the record is the scope's "Gate outcomes" line: no open
decision, the Agent's defaults A1 to A8 accepted as one item, the paper, the derivations, the package and WP23's and
WP24's surfaces untouched by this instance. The verbatim words are the driver's to add here.

## Instance 1 executed (2026-11-10)

At `dev` 73c5bff: inventory db150fc (346 rows: 144 keep, 169 delete, 33 hold), deletion 09117d8 (169 files), review
`WP25-review.md`. Checks run after the deletions: the assembled site builds; the fast suite 2 failed, 1816 passed, both
failures the head's before the package (`C310` in the register; `limitations.md` linking into `paper/`); the vocabulary
tool's 71 violations identical before and after; doctests 57 passed; `uv lock --check` clean. No undecided row.

## First instance accepted (2026-11-10, 00:35; the driver under the mandate)

Delivery: db150fc (the inventory, 346 rows), 09117d8 (169 files deleted in one commit), f9573fd (the review: checks
run after the deletions, 18 drift rows, 9 gap rows). The driver's check: the deletions are 154 files under
`docs/superpowers/notes` (the spike folders whose results are in decision records: sysml-diagrams 107, ternary 30,
facet-rename 4, figure-candidates 4, soft-fit 3, figure1 3, ggp-fit 2, external-review 1), the 14 raw reader
reports of WP11 round 1 (`triage.md` kept) and the superseded PM handover file (`PM-BRIEF.md` holds the current
one); every note `CLAUDE.md` names is present; no deleted basename is referenced from `CLAUDE.md`, `README.md`,
`mkdocs.yml`, the docs pages, the paper, the tests, the scripts or the package (grep 0); the watcher is green at
the head after the deletions. **Accepted.** The driver's words for D-6: "WP25 instance 1 accepted: the inventory
has no undecided row, the 169 deletions are in one commit that lists them, nothing live references a deleted file,
and the checks are green after them; the drift and gap rows pass to WP24's docs push and the next instance." One
follow-up: WP24's scope cites the facet-rename spike by its last commit (d1efdfe), since the report now lives in
history.
