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

## Rows recorded so far

Until `claims_register.toml` exists, rows are recorded here in the register's fields.

| Fragment | File | Kind | Pointer | Verdict | Disposition |
|---|---|---|---|---|---|
| "a marker is not where V = 1" (the key: a numbered marker is a facet's exponent vector, where that facet's V is largest for a fixed total; V also depends on the total) | `docs/examples.md` (WP18, R-5) | S | the `plot_ternary` doctest and Notes in `src/hyperbolic_trade_space/plotting.py` (at a fixed total facet k peaks at c = w_k); `tests/test_plotting.py::test_ternary_fixed_total_identity_and_peak` and `test_ternary_markers_sit_at_the_exponent_vectors` | backed | keep |
| "weighted geometric mean of the metrics; doubling every metric doubles it" (section 4, before Definition 2) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L1 (`V(km)=kV(m)`, `lemma_01_homogeneity.py`); glossary `invariant-value` | backed | keep |
| "It stays the same along a trade-off, hence invariant" (section 4, before Definition 2) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L1 (`log V = w.u - beta`, so V is constant where `w.u` is) and L7 (the tangent step along a facet, `lemma_07_elasticities.py`); Definition 8 (ascent direction: the tangent space trades contending metrics at constant V) | backed | keep |
| "designs of equal V stand at the same level, and log V, the energy differential, is a design's level relative to the reference surface V = 1: negative inside, positive beyond" (section 4; worded as an analogy with a potential) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L1 (`log V = w.u - beta`), Definition 1 (the reference surface is V = 1), glossary `energy-differential` and `level-offset`; the physical potential is named as an analogy, not a claim | backed | keep |
| "A difference of levels is the same along every path between two designs" (section 4) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L1 and L2: `log V(m) - log V(m') = w.(u - u')` for any two designs, free of the offset; glossary `energy-differential` formal field (a path-independent difference) | backed | keep |
| "neither a physical energy nor a Euclidean distance" (section 4) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | glossary `energy-differential` not-clause ("a Euclidean distance") and `level-offset` ("a distance"); the register's forbidden phrases; a statement of what the term does not mean, not a claim about the data | backed | keep |
| "Where several trade-offs are active at once, the model is a sum of such terms, one per facet" (section 4) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L10 (`e^(kappa Phi_K)` is a posynomial in m, the sum of K monomials); Definition 3 | backed | keep |
| "Two temperatures say how soft each maximum is, over designs and over facets; at infinity each is exact" (section 4) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L5 (the log-mean-exp, its limits and the bound `LME >= max - (log N)/tau`) and L10 (`max_k x_k <= Phi_K <= max_k x_k + (log K)/kappa`); Definition 4; glossary `temperature`, `term-temperature` | backed | keep |
| "The chart separates where a design sits along the surface from its energy differential, how far it is from the surface in levels and not in Euclidean distance" (section 4) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L8 (`Z` is free of the shift; the map between `u` and (position, log-scale) is a bijection); Definition 5; glossary `chart`, `position-along-the-frontier`, `energy-differential` | backed | keep |
| "a reversible rewriting of the metrics as a position along the surface and a level relative to it" (section 1) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L8; Definition 5; glossary `chart` | backed | keep |
| "a soft fit has a second-order certificate" (section 1, main results item 4) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L17 (`lemma_17_soft_fit_certificate.py`) | backed | keep |
| "fitting at a finite kappa is the soft fit of Section 6, which does change them" (section 5, assumption ii) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | S | interface contract version 6 (a finite `term_temperature` selects the soft fit; the default `np.inf` fit is unchanged); `tests/test_soft_fit.py`; the bound for given facets is L10 | backed | keep |
| "The one-facet fit comes first: the invariant value and its shift (L1, L2), the fit as a convex program (L3 to L5)" (section 6, opening) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | the boxes it names: L1 to L11 as stated; "not convex" for the several-facet fit is L16 part (i); the three levels are L15, L12 to L14; the certificate is L17 | backed | keep |
| "shifting every log-metric by a constant moves the offset by that constant and leaves the exponents unchanged" (section 6.1) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L2 (`lemma_02_shift.py`); L1 for "scales with the metrics" | backed | keep |
| "has simplex optimality conditions (L3), is convex (L4), and uses the log-mean-exp, which differs from the log-sum-exp by a constant (L5)" (section 6.1) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L3, L4, L5 (`LSE = LME + (log N)/tau`) | backed | keep |
| "the soft maximum of Gaussian noise has a closed form (L6), and along a facet the exponents are elasticities and give the improvement factors to V = 1 (L7)" (section 6.1) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L6 (a population identity, no consistency claim), L7; glossary `elasticity`, `improvement-factor` | backed | keep |
| "The chart is a reversible rewriting of the log-metrics (L8), and under log-affine conditioning the pull-back to attributes is exact (L9)" (section 6.1) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L8, L9 | backed | keep |
| "V_K is the 1/kappa power of a posynomial and its logarithm lies within (log K)/kappa of its largest term (L10); a maximizer of V is Pareto-efficient, and the converse is not claimed (L11)" (section 6.1) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L10, L11 (the converse is stated as not claimed in the box) | backed | keep |
| "The package fits with sharp weights at the default term temperature (infinity) and with soft weights at a finite one; a soft fit is certified by the second-order test" (section 6.2) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | S | interface contract version 6 and `work-packages/WP17-decisions.md` (R-1, R-7); `tests/test_soft_fit.py`; the test is L17 | backed | keep |
| "The sharp-weight fit meets three levels of guarantee, none global: descent (L15), numerical stationarity by the facet gap (L12) and local optimality where the margin is positive (L13, L14)" (section 6.2) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L15, L12, L13, L14 as stated in their boxes | backed | keep |
| "At a finite term temperature a second-order test certifies a strict local minimizer (L17)" (section 6.2) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L17 (a connective: the box states the conditions under which the test certifies) | backed | keep |
| "For a soft fit, certified means that the second-order test holds, and stationary that the facet gaps hold and the curvature is not positive" (section 6.2) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | S | interface contract version 6 ("certified" has two meanings; "stationary"); `work-packages/WP17-scope-of-work.md` R-7; `tests/test_soft_fit.py`; the test is L17 | backed | keep |
| "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order (KKT) conditions hold" (the L17 box, section 6.2; the statement of the derivation script, the symbol H = D - kappa M typeset) | `paper/paper.ipynb` (WP10, tickets of 2026-11-09) | M | L17 `STATEMENT` in `derivation/lemma_17_soft_fit_certificate.py`; the hypotheses (finite tau and kappa; first-order conditions holding exactly, not within a tolerance) are the script's own text; the declared inherited result I16 | backed | keep |
