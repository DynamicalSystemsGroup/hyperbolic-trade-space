# Note: the claims review (every claim a reader can rely on has backing, or it goes)

Written 2026-11-09 by the driver on the supervisor's direction (`work-packages/WP10-decisions.md`,
"After the research sprint"): "i prefer to drop unbacked claims. as part of our narrative, prose and
copy editing work we need to sweep for claims to make sure they have backing. this does not mean we
need to heavily caveat and reference a claim everytime it appears we just need to know we've not
injected spurious details or unsupported claims. that should be addressed primarily in clarifying
our requirements and include offering a mechanism for assessing the requirement."

What set it off: the paper said the posynomial extension "reduces to the one-facet fit". That is
backed for the model (L10: with one term the model is the monomial) and not for the fit (the
one-term fit minimizes the level, the several-term refit the mean slack; their answers differ).
A detail had been carried one step past its backing.

## The requirement

**Every claim in prose a reader can reach is backed, or it is narrowed to what is backed, or it is
dropped.** It applies to the paper, the supporting material, the docsite, the root page and the
README. It is a requirement on what we know, not on what the prose shows: the prose is not given
more caveats, citations or cross-references to prove it. The evidence lives in a register beside
the prose.

**A claim** is a statement that could be false and that a reader could rely on. Five kinds:

| Kind | About | Backing that counts |
|---|---|---|
| M | the mathematics or the method | a tagged step of a lemma script (the proof map), with the statement no broader than the step |
| R | a result, a number, the behaviour of the data or the case | a generated value: the generator or cell that prints it, and the test that pins it |
| S | what the software does | a test, a doctest or the interface contract |
| L | the literature, other people's work | a row of the cited-claims audit saying what was read, verdict supported |
| P | practice, the world | a source as for L, or the sentence is worded as the author's own experience or judgment and marked as such in the register |

Not claims: definitions, statements of scope or intent, instructions, and sentences plainly worded
as the author's judgment.

## The mechanism (how the requirement is assessed)

1. **Extraction, by a reader with fresh context.** For each section or page, from the rendered
   page, list every claim: a fragment of at least six consecutive words that identifies the
   sentence, and its kind. The reader has no repository access, so nothing is skipped because it
   "is surely true".
2. **Backing, by a second agent with the repository.** For each claim, the pointer (a lemma tag, a
   generator and test, a test id, an audit row) or "none"; then one verdict: backed; broader than
   its backing (say how); unbacked.
3. **Disposition (the PM; anything that changes a mathematical statement or a conclusion goes to the
   driver, and from there to the supervisor).** Exactly one of: keep; narrow to what is backed;
   drop; back it, only when the backing is a small step already implied by the work, otherwise drop
   and record the claim as a candidate for later. Never: add a caveat or a reference in the prose
   only to make the register pass.
4. **The register and its test.** `claims_register.toml` at the repository root: one row per claim
   (fragment, file, kind, pointer, verdict, disposition). A test asserts that every fragment still
   occurs in the prose it names, that every pointer resolves (the lemma tag is in the proof-map
   record, the test exists, the audit row exists with verdict supported), and that no row is
   unbacked or broader. A sentence that is edited no longer matches its fragment, the test fails,
   and that sentence is swept again. So the register cannot go stale silently.
5. **Coverage check, by the driver.** A random sample of sentences from the rendered pages
   (seeded, at least thirty per pass) is checked against the register: a sampled sentence that is a
   claim and has no row is a miss, and a miss sends its whole section back to step 1.

## When it runs

- In full once before the release candidate, over everything a reader can reach.
- At each acceptance review of prose, on the sections that changed (the register's test shows
  which).
- Together with the vocabulary review (`vocabulary-review.md`): the same fresh-context readers can
  return both lists.
