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
