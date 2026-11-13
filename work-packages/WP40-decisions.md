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

## Stage 2: the inventory accepted and the thinning decided (2026-11-13, 21:45; the assistant, under the supervisor's direction; readout at 64aa577)

The readout (`WP40-rounds/inventory/readout.md`) sizes the checkout (65 MB real bytes, 52 MB of it `work-packages/`,
324 screenshots at 44.7 MB read by no test or script, a 100 MiB pack), names what is protected, and gives options per
class. The assistant's calls, in the readout's numbering:

**Assistant, verbatim:** "1. Screenshots: they leave the working tree at the build; git keeps them, and each review or
round file that embedded or listed them gains one line naming the commit at which they can be seen, so 'screenshots in
the record' stays true with the record being the history; images a markdown page or a test reads stay (the inventory
says none). 2. Review and round directories: the text stays; it is the record and is small without the images. 3.
Reader runs: stay, the record of the user tests. 4. Notes: the eight convention notes and the six live ones stay under
`docs/superpowers/notes/`; the five build notes, the three outline and search notes and the two spike folders move
under `work-packages/`, the build's record, with every path that names them updated and the paper's source map and
the three dangling comment paths with them. 5. Superseded inventories: go. 6. The pack stays; no history rewrite, the
records quote hashes. 7. The README's Layout list per the draft, with one correction: `history.yaml` is the record
behind the history and acknowledgements page, not the release history; and a short header in `work-packages/README.md`
saying what the folder holds and that it is not needed to use the method. 8. Drift closed in the build. Sequencing:
the build runs after WP39 lands and before the final reader round, so no reader meets a moving path, and the residual
pass runs on the surfaces after it. Protected as the readout lists, and the held-out WP11 material untouched. The
scope for my approval next."

## Approval of the scope (2026-11-13, 22:30; the assistant, under the supervisor's direction; scope at dfc7c95)

**Assistant, verbatim:** "WP40-scope-of-work.md at dfc7c95 is approved as written: goals G1 to G4, the non-goals (no
history rewrite, no change to the paper's content or the data of record, the records' text untouched and keyed by the
move table, the held-out WP11 material untouched), deliverables D-0 to D-10, requirements R-1 to R-11, good enough as
stated, the sequencing after WP39 and before the final reader round, and the agent's defaults as one item, including
the three the PM raised: spike-container-platform moves as the third spike folder and the build reports any other
count rather than guessing; one ruff-exclusion line in pyproject.toml because the spike folders move, the lock
untouched; the two comment-only edits under derivation/ made only if neither file is pinned by a hash or the ledger,
otherwise reported. Open decisions: none."

## The build verified for D-1 to D-7 and D-9 (2026-11-14, 12:50; head ea6169d; D-8 in flight)

**Assistant, verbatim:** "WP40's build is verified at ea6169d for everything but D-8: no tracked image under
work-packages (333 removed, held at c680853, a sample retrieved by `git show`); the pointer lines in the records and
the retrieval note in work-packages/README.md; the four superseded inventories removed and named; the build notes,
outlines and three spike folders moved under work-packages with every path updated and the ruff exclusion naming the
folders that remain; the README's Layout list naming every top-level entry with history.yaml as the record behind the
history page and work-packages as the build's record; the drift comments reworded; the move table and the measure
(work-packages 56.3 to 7.9 MB; the archive 70.9 to 22.2 MB, 53.1 to 7.9 MB gzipped). Protected items byte-identical
to the start head except the assistant's own records. The lemma chain passes after the two derivation comment edits;
the fast suite 1946 passed; ruff, lock, vocabulary and attribution clean. D-8, the notebook cells naming moved
paths, lands through the paper queue and completes the package."
