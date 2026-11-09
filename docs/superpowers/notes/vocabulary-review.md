# Note: the vocabulary review (the glossary as the one source of terms; how prose is checked against it)

Written 2026-11-09 by the driver on the supervisor's direction (`work-packages/WP10-decisions.md`,
"The supervisor's reading of the abstract, second pass"): "make sure its reflected in our glossary
and that we have a documented review technique for jargon checking across our paper and
documentation to ensure we're consistent with our glossary. we should avoid unecessary jargon but
use the glossary defined terms to keep the prose clear and concise."

What set it off: one object had two names. The paper's Definition called the multi-term model a
"posynomial"; the abstract, section 5 and the docsite's theory page called it a "generalized
posynomial". Both are defensible terms in the source (Boyd, Kim, Vandenberghe and Hassibi 2007);
the fault was using two for one object and using the heavier one where the plain one is exact.

## The rule

1. **One object, one name.** A term of art in the paper, the docsite, the root page or the README
   is either an entry of `glossary.yaml`, or a term assumed of the reader (below), or it is replaced
   by plain words.
2. **Use the glossary's term, not a paraphrase of it.** Where a defined term says in two words what
   a clause says in ten, the term is used. That is what the glossary is for.
3. **No term that does no work.** A term of art that plain words serve as well is jargon and goes.
   A defined term used once, in a place its definition is not within reach, is a candidate to go.
4. **Class words keep their class.** A word that names a class of functions is not used for a class
   of problems, nor the reverse. Worked case: posynomial (a function: a sum of monomials);
   generalized posynomial (a function built from posynomials by sums, products, positive powers and
   maxima); geometric program and generalized geometric program (problems, whose objective and
   constraints are of those kinds). "Generalized" attaches to the one class statement about the
   invariant and to programs, never to the surface.

## The three lists (all in `glossary.yaml`)

| List | What it holds | Effect in the check |
|---|---|---|
| `entries` | our terms: the phrase the prose uses, a one-line meaning, the formal object, what it is not, where it is defined; optional `aliases` (accepted variants: plural, abbreviation, symbol name) and `avoid` (variants that must not appear, each with the reason) | a use of the term or an alias resolves; a use of an `avoid` variant fails |
| `assumed` | standard vocabulary assumed of the reader (calculus, linear algebra, convex optimization at the level of Boyd and Vandenberghe; scikit-learn's documented vocabulary), each with its source | resolves; not defined again in our prose |
| `stems` | the stems that mark a term of art in this subject (posynomial, monomial, program, frontier, facet, envelope, surface, chart, lemma, rate, margin, radius, temperature, gap, ...) | every phrase built on a stem must resolve to an entry, an alias or an assumed term |

A sentence that describes a source in the source's own words (Appendix G, Further reading) is
exempt for the phrase it reports, by an explicit marker beside it, never by a blanket exclusion of a
file.

## The mechanical check (a tool, run in the test suite)

    uv run python scripts/check_vocabulary.py            # report; non-zero exit on a failure
    uv run python scripts/check_vocabulary.py --density  # also the density table

It reads the prose a reader sees and nothing else: the Markdown cells of `paper/paper.ipynb` and
`paper/supporting_material.ipynb` (generated tables included, since a reader reads them), the
docsite pages, `site/index.html`, `README.md`, and the docstrings that become the API reference.
Code, math and citation keys are skipped.

- **Fails on:** an `avoid` variant; a stem phrase that resolves to nothing; a glossary term whose
  first use in the paper has no definition or cross-reference within reach; a glossary entry no
  prose uses (dead entry) unless marked `reserved`.
- **Reports, does not fail:** terms of art per hundred words by section and page (the density
  table), with the densest paragraphs listed, as the agenda of the reading below; every term used
  exactly once.
- The tool's own tests plant a violation of each kind and assert it is caught.

The check answers "is every term one of ours and used as ours". It cannot answer "is this term
needed". That is the reading.

## The reading (a reviewer with fresh context; at every acceptance review of prose, and in WP11)

The reviewer is given the rendered page or section (in the browser, as a reader meets it), the
Glossary page, and nothing else: no scope, no notes, no source. They return three lists, each item
with the sentence quoted:

1. terms they could not resolve from the page and the glossary;
2. places where a glossary term would say it shorter or more exactly than the words used;
3. terms of art that plain words would serve as well, and sentences where three or more terms of
   art arrive together.

The densest paragraphs from the density table are read first.

**Triage (the PM; calls that change a term's meaning go to the driver).** Every item gets exactly
one of: add or amend a glossary entry; replace with plain words; replace with the glossary term;
add the variant to `avoid`; no change, with the reason. A new or changed entry is a change to the
single source, so the paper's notation table, the docsite's Glossary page and the interface contract
follow in the same push. The record of each pass (the three lists, the dispositions, the tool's
output before and after) is kept beside the review of the package it belongs to.

## When it runs

- The tool: in the test suite, so on every verified commit and in CI.
- The reading: at each acceptance review of a prose deliverable (paper, docsite, root page), and as
  a standing question in the reader-grid loops (WP11): each persona reports terms they could not
  resolve.
- Before the release candidate: one full pass of both over everything a reader can reach.
