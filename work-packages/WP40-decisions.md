# WP40 decisions: release thinning and repository organization

Supervisor: Michael Zargham (`mzargham`). The assistant records his words verbatim and its own calls under them.

## The direction (2026-11-13, 18:55)

**Supervisor, verbatim:** "stuff link this '(docs/superpowers/notes/abstraction-gaps.md).' reads as LLM but i am also
thinking that may just be that we've got a repo a bit bloated with materials from the build and that some thinning
and organizational cleanup is merited as we approach our release"

**The assistant's reading and first calls:** two things. (1) A repository path in parentheses inside reader-facing
prose is a residual of the kind WP38 names (a detail that belongs elsewhere); the supporting material has three
(`notation.md`, `abstraction-gaps.md`, `literature.md` in Appendices A, E and G), the paper and the docs none; the
WP38 checker gains the pattern and the three go in the Appendix H or WP39 notebook unit's wake, as a path becomes a
link with words or leaves. (2) The repository carries the build's materials: 31 notes under
`docs/superpowers/notes/`, 183 entries and 51 MB under `work-packages/` with 306 screenshots, a 100 MB pack. WP40 is the
tidiness package of the release (the recurring kind): a stage-1 inventory of what a release reader finds, each item
with what it does for that reader or for the record, then the decision on what moves, what goes (git keeps history)
and what the repository's top level and README say about where things are, then the build under a scope the assistant
approves. Nothing of the paper's content, the data of record or the decision records is thinned by it.
