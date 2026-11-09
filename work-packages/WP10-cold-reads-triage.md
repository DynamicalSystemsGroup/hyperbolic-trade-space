# WP10 cold reads, round 1: the driver's triage

2026-11-09. Reports: `WP10-cold-reads.md` (verbatim, one fresh reader per depth, no personas, each
given only its depth's slice). The driver is the triager and wrote none of the paper. Honest limits
of this round: one reader per cell, so "replicated" below means across depths, not within a cell;
no answer key was fixed before the reads (it is fixed before the persona rounds); readers are
models, so their silence is weak evidence.

## Comprehension

All six readers could say what the paper is about, and what they said agrees with the story:
a table of evaluated designs, a fitted frontier, which metrics contend and at what exchange rate,
a chart of position and energy differential, beside PCA and not instead of it. None came away
believing the method picks a design, proves a global optimum, replaces Pareto analysis or PCA, or
is causal. The reader at the reproduce depth regenerated both notebooks with no differing cell and
all eight figures byte-identical. The reader at the adapt depth, given an unseen synthetic table
and only the paper's appendix and the docsite, chose two facets, recovered the planted exponents
to the second decimal and 297 of 300 assignments, and judged the third and fourth facets to be
splinters, before opening the truth.

One weak belief to correct: one reader called the unit level set "the Pareto-like frontier". The
three objects (fitted reference surface, supporting envelope, Pareto boundary) are distinguished
in section 3 and need to be distinct from the first screen.

## Findings, classified

Kinds: W wrong belief, M missing (the reader could not learn something the depth owes), F friction,
D defect, P preference. "Seen at" lists depths.

| # | Finding | Kind | Seen at | Decision |
|---|---|---|---|---|
| 1 | A facet titled "6-lemma (6 metrics contend)" shows five nonzero exponents; "contending" counts an exponent of 0.02 like one of 0.43, and the threshold is not fixed in the text | M | C, D | fix: one definition of membership, stated, and the figure agrees with the count |
| 2 | Whether the method recovers a known answer is never stated in the main text, though the planted example exists | M | C, D | fix: the planted recovery result in section 9 in one or two sentences, with its table in Appendix D |
| 3 | Why a 10 percent target above the surface, and why the band is one over the temperature | M | B, C, D | fix: the reason in a sentence each where they are introduced; the sensitivity already in Appendix D pointed to |
| 4 | "Facet share, our analogue of explained variance": not argued; a count of designs is not a conserved fraction | F | B, C, D | fix: say what it is and what role it plays; drop the bare analogy or argue it. Touches the register: listed for the supervisor |
| 5 | "Energy differential": why "energy" | F | A, B, C, D | fix: one clause at first use (the level of a potential, relative to the reference surface). The term stays: it is the register's |
| 6 | "n-lemma" reads as a proof object | F | A | fix: at first use, "by analogy with dilemma and trilemma" |
| 7 | The title promises "scaling"; nothing on the first screen says what scales | M | A | fix in the abstract or section 1: what grows (designs, metrics) and what breaks without the method. The title is the supervisor's |
| 8 | The mean-slack comparison across K is made at different temperatures; "three facets report three regimes" partly follows from asking for three | M | C, D | fix: say so where the numbers are given, and give the comparison at a fixed temperature in Appendix D |
| 9 | "Certified" with a stable radius of 1e-5 against a band of 0.03: what is it worth | M | C, F | fix: one sentence on how to read the size of the margin and radius; the same on the docsite |
| 10 | Propose-predict-check is reported as mixed in section 9 and then read as success in the Discussion; three points; the easy part passed | F | C | fix: the Discussion says what it showed and did not |
| 11 | Chaining with PCA is asserted and never shown | M | C, D | fix: either one worked line (principal directions of the near-frontier chart coordinates on the case, in Appendix D with a pointer) or state it as a use not demonstrated here |
| 12 | Hypothesis labels (A2, R1, F12, I9) cannot be resolved at skim or whole-paper depth | F | B, C | fix: each label links to its line in Appendix B or carries its words on first use |
| 13 | Generated ranges such as "(-0.072 to -0.071)" appear with no word on what varies | F | C | fix: the first range says "over five regenerations under rounding-level perturbation (Appendix D.11)" |
| 14 | Table 2 (candidates): no candidate lies beyond the surface; what the table shows is unclear | F | D | fix: caption says what it is for, or it moves to Appendix D |
| 15 | Proposition and Corollary share a script and their step numbers interleave | F | D | fix in Appendix B: the entry says so in a line, steps listed in file order under each |
| 16 | No comparison with a plain alternative (Pareto front plus regression) | M | A, B | noted for the reader loops; the nondominated counts are the paper's answer and should be visible at skim depth |
| 17 | Physical meaning of the regime differences is left to "human validation" | P | C | accept: that is the paper's stated position |
| 18 | Appendix F: two tests need git history and fail in a copy; the container paragraph is a placeholder; "outputs unchanged" does not say how to compare; no way to regenerate one row; the site build prints a server line | D | E | fix all except the container paragraph (pending) |
| 19 | Docsite, Fitting: `facet_share_` is described without saying it exists only for several terms; at one term it raises AttributeError | D | F | fix in the package: the fitted attributes exist for every K |
| 20 | `objective_` is the soft maximum at one term and the mean slack at several; nothing says so, and a reader compared them across K | D | F | fix: a quantity defined for every K to compare across K, named and documented; `objective_` documented as what was minimized |
| 21 | `select_temperature` with the default target raises "not bracketed" for several terms on a table with many frontier rows; the first `tension_report` on a two-term fit raises on the default band; no guidance on choosing K, the target or the band | D | F | fix on the docsite: a short "choosing K, the temperature and the band" passage built on what the reader did (compare at a fixed temperature, restarts, resampling), and error messages that say what to try |
| 22 | Termination page says the margin is infinite at one term; it is `nan` | D | F | fix: page and behaviour agree |

## Change requests to the authors

Sent to the PM as numbered requests giving the passage, the problem and the constraint, without
depth. Constraints that hold for all: the word cap on what renders; the register's words; nothing
claimed as novel; no number printed beyond its reproducible precision; text that does not fit moves
to an appendix with a pointer.

## For the supervisor

- Item 4 touches the register's entry for the facet share ("the explained-variance ratio" as its
  analogue). Three readers did not accept the analogy as stated.
- Item 7: the title's "scaling" is not carried by the first screen.
- Items 19 to 22 change the package's behaviour slightly (attributes at one term, a comparable
  quantity across K) and the interface contract's manifest follows by amendment.
