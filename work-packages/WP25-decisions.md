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
