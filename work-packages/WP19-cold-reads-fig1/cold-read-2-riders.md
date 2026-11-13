# Cold read of Figure 1 after the two riders (footer removed; caption clause added)

Screenshots for this record: commit `c680853`, `git show c680853:<path>` with `<path>` under `work-packages/WP19-cold-reads-fig1/`.

Reader: one fresh Sonnet agent, image first (`fig-nlemma-riders.png`), then the caption.

Deletion and what it no longer did: the footer "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)"
(and the caption sentence about a triangle being one face of a larger simplex with the weight printed, and the unused
`weight` field of `nlemma_data`) no longer carried a figure reading: the three row sums of 1 are a property of the
exponent vectors, not a finding, and the previous cold read called the line cryptic.

Reader, image only: a triangle with three numbered dots, each term's face named; "it never says what the terms are or
what they are terms of"; w undefined; the dots look like unrelated points.

Reader, with caption: the clause "the three dots are the terms of one fitted posynomial" is consistent with the
picture (three dots, each a term with its own w, nothing contradicting one shared model; "fitted" and "one
posynomial" cannot be checked from the image alone). The caption now answers what the dots are, that position encodes
the exponent vector, and how faces map to n-lemmas. Still open for the reader: w is not named in the caption, and
n-lemma is defined by example.
