# WP42 readout: tension, and the glossary's terms across decision analysis, optimization and learning

Spike on branch `wp42` (from dev ca352f5). Nothing in `src/`, `paper/`, `docs/` or `glossary.yaml` changed (R-5; see the end).
Everything below is reproduced by the scripts in this folder: `lemma_tension.py`, `case_run.py`, `section9.py`,
`figure.py`, `dry_run.py` (each `uv run --frozen python ...`; `case_run.py`, `figure.py` and `section9.py` refit the case, about a minute each).

## 1. The definition (G1, R-1, R-2)

**Tension** between metrics i and j on term k, at a point of the surface, in the conditioned metrics: the partial
derivative of m_j with respect to m_i along the term, the other metrics held,

    T_ij = d m_j / d m_i = -(w_ki / w_kj) (m_j / m_i).

The elasticity (Definition 8, Theorem 7) is its log-log form, (m_i/m_j) T_ij = -w_ki/w_kj, constant on the term; the tension
adds the factor m_j/m_i, so it changes along the term and carries the metrics' scale.

| Case | Cell | Why |
|---|---|---|
| negative | T_ij < 0 | both w_ki and w_kj positive: the term trades i against j |
| zero | T_ij = 0 | w_ki = 0 and w_kj > 0: raising i moves nothing along the term |
| blank | undefined | w_kj = 0: m_j is not determined by m_i on the term (the derivative of the surface in m_j vanishes); drawn empty, not zero |
| reciprocal | T_ij T_ji = 1 | where both are nonzero; the zero cells and the blank cells are transposes of each other |
| piecewise | one matrix per term | at K > 1 the surface is the maximum of the terms; a design's tensions use the term it is assigned to, and near a seam the other term's value is reported beside it, never merged |

Where both are zero the blank wins (j carries none). In attribute units (Theorem 7, the conditioning
log m_k = alpha_k log(a_k + s_k) + b_k):

    d s_j / d s_i = -(w_ki alpha_i)/(w_kj alpha_j) * (a_j + s_j)/(a_i + s_i).

Two readings the build must state: (1) the sign in attribute units is minus the sign of alpha_i alpha_j, so it is negative
for two attributes of one orientation (both smaller-is-better, as pointing error and cost) and positive for mixed
orientation; "negative where both contend" is a statement in the metrics only. (2) It is a partial derivative with the
other twelve metrics held, along the fitted surface: for metrics that move together in the data (fleet cost is unit cost
times fleet size) it is not a move a design can make, and it is not the effect of changing a design variable.

**Two objects, kept apart (R-2).** The term's tension matrix: from the fit, at the term's balanced point (the softmax-weighted
mean log-metric of the term's rows at the fit temperature). A design's tensions: from the data, the same formula at the
design's own metric ratios on its term. The level does not matter: a level set is the surface scaled (Theorem 1), which
leaves ratios alone.

## 2. The lemma step (G1, R-1)

`lemma_tension.py` (draft L21; the build moves it to `derivation/lemma_21_tension.py` and enters its hypotheses in the ledger).
Plain SymPy, ten tagged steps, run and passing: the implicit derivative of the term's hyperplane gives T_ij; its log-log form
equals L7's elasticity -w_i/w_j; the zero, blank, negative and reciprocal cases; the pull-back to attribute units found two
ways (the chain rule on T_ij, and the implicit derivative of L9's surface sum_k w_k alpha_k log(a_k + s_k)), which agree;
the orientation sign; the level-set invariance. It uses A1, A2, A4. It does not prove the surface is the right one, nor the
seam (reported, not smoothed). It is a pencil-and-paper substitute, not a formal verification.

## 3. The prototype on the case (G1, R-1)

`prototype.py` (not in `src/`): `term_tension_matrix(w, u_point)`, `balanced_point`, `design_tensions(estimator, m_row, raw_row,
alpha, a)`, `attribute_tension`. `case_run.py` runs the case (primary regime, 2,134 designs, thirteen metrics); full
matrices are in `matrices.npz`, the summary in `results.json`.

Finite-difference check, treating the fitted estimator as a black box (`score_samples` as the level; for a step of 1e-4 in
metric i, solve for the metric j that keeps the level; central slope), every cell with a defined value:

| Fit | Term | Cells checked | Largest relative error, nonzero cells | Zero cells |
|---|---|---|---|---|
| K = 1 (tau = 41.7) | 1 | 96 | 3.1e-7 | exactly 0 |
| K = 2 (tau = 113.2) | 1 | 96 | 2.2e-6 | exactly 0 |
| K = 2 | 2 | 96 | 2.7e-6 | exactly 0 |

Each matrix has 56 negative cells, 40 zero cells, 60 blank cells and the 13 diagonal cells (eight of thirteen metrics carry
an exponent above the participation threshold). All steps stayed in one cell of the K = 2 surface; the balanced points sit
0.21 (term 1) and 0.70 (term 2) in score from the seam. The attribute-unit formula agrees with finite differences taken
through the conditioning on the four pairs of the picked design to better than 1e-7 relative.

What the matrices show, for the reader of the build: the three measures of Section 9 at the balanced point (rows i, columns j,
pointing error, unit cost, fleet cost):

| | pointing error -> unit cost | pointing error -> fleet cost | unit cost -> pointing error |
|---|---|---|---|
| K = 1 | -0.605 | -1.03 | -1.65 |
| K = 2, term 1 | -2.63 | -3.15 | -0.38 |
| K = 2, term 2 | -0.27 | -0.77 | -3.72 |

The same pair differs by an order of magnitude across terms: that is the point of the object, and it depends on the
balanced point, which at K = 1 puts every contending metric at one common log value (0.186, as R1 says) and at K = 2 does
not (the soft fit's rows give unequal components). So the term's matrix is "at the balanced point" in a literal sense, and
the elasticity matrix is the point-free companion.

## 4. The figure (G2, R-3): `figure-review.md`

Recipe, the readers' words quoted, the five tests as the author judges them, three redraws (replace Figure 7's correlations;
the same cut to the participating metrics; both side by side) and the dark render, all as rendered images. **The cold
read is not done**: this scope allowed no sub-agents, so the figure and a one-paragraph brief are left to the PM (R-3 is
open until it runs). Findings of my own reading: the side-by-side at the paper's width is unreadable (16 in), which argues for
replacing or for a second figure; about two thirds of a full panel is empty or zero cells, which the compact version drops
at the cost of the structure the definition names.

## 5. The glossary (G3, G3b, G3c, R-4): `glossary-drafts.yaml`, `drafts.md`

Drafted: preamble (the three layers in full), entries for objective, constraint, trade-off, tension, tension matrix, design
tensions, loss (the choice stated), proposal and check (shared with WP41, which owns the wording), revised MoE and MoP (not
by themselves objectives), white space (the one word, option (a) below), and stems for objective, loss and tension. Every
entry names its layer (`layer`: decision, design or method) and the register that uses the word (`used_in`, with `elsewhere`
for the caveat). Section 3's paragraph is in `drafts.md`, brief, pointing to Appendix A.

Checker dry run (`dry_run.py`; `dry_run_violations.txt` lists them): the repository today has 60 violations with no baseline
(5 avoid, 1 first-use, 54 stem). Extended stems alone add 54 stem violations. With the drafts merged: **no new stem
violation**, and 23 new violations, each a planned edit: 17 avoid (the solver's "objective" phrases to rename to loss, 15 of
them in `paper/` and `src/`; one "holes in the chart", one "table has gaps"), 4 first-use (the paper's first use of
objective, constraint, loss, proposal lacks its gloss) and 2 dead entries (tension matrix, design tensions: used once the
build lands them). The draft texts themselves add no violation. The checker cannot take "trade-off" as a stem (a stem is one
token and it splits at the hyphen); the entry's `avoid` list catches spelling variants instead.

Sizing the build's mechanical pass over the surfaces (the checker's corpus, word counts): objective 107 (paper 65, src 38, user guide 4),
loss 12, tension 52 (paper 19, src 15, user guide 12, README, root page, docs 5), trade-off 33, gap 136, hole 22, white space 9. Many
"tension" uses mean a term's trade-off (the paper's "regional tensions", "successive tensions") and move to trade-off.

Schema change the build must make (amend `interface-contract.md/.toml`; `tests/test_interface_contract.py` R-6 pins the
fields): entry fields `layer`, `used_in`, `elsewhere`; file key `preamble`, shown at the top of the docs Glossary page.

**Entry surfaces (G3c).** Build's first list, as ruled: the four small edits (root page What: "explains trade-offs",
"contend"; "unsupervised learning, beside PCA" on the root page and the docs home; README Layout "fit a frontier, read its
trade-offs"). Not touched: the root page's summary paragraph and "bespoke or opaque".

## 6. The decision section's number (G4)

From `section9.py` (design 1858, the pick "between", term 1 of K = 2, 0.16 in score from the seam; the numbers are
computed, not typed):

> At the picked fleet (5 medium-wheel, fine-tracker satellites) the surface's tension between the operator's pointing error
> and the sponsor's fleet cost is -1.4 M USD per arcsecond: along the surface, one percent more pointing error goes with 2.4
> percent less fleet cost. It is a rate at that design with the other metrics held, not the price of the better tracker, and on
> the other term of the fit it is -0.4 M USD per arcsecond.

Unit cost: -43 thousand USD per arcsecond (0.37 percent per percent). The sentence is the supervisor's to accept or decline;
it lands nowhere in this scope. The figure that it is (-1.4 M USD per arcsecond of a fleet cost of 1.7 M USD at 2.9
arcseconds of error) is a local slope, large against the whole, so the sentence says it is not a price.

## 7. Naming items for the supervisor (plain options, no recommendation)

1. **One word for an unoccupied region of the chart** (now gap in 136 places counting its other senses, hole 22, white space 9):
   (a) white space, the abstract's word; hole and gap for this object become avoided variants, gap staying with the term gap and
   the gaps ledger; (b) hole, the glossary's present word for the object; (c) both, white space for the region and hole for its
   mathematical form in the chart's distribution.
2. **`tension_report`:** (a) keeps its name and gains the tension matrix; (b) is renamed (for example to `trade_off_report`) and
   the README and root page follow. Related, either way: the report's `tension_directions` and `tension_loadings` are principal
   directions of the data's spread and `plot_tensions` draws the association among designs, so under the new definition both
   carry a word for another object; (a) leave, (b) rename them (spread directions; association map).
3. **Figure 7:** (a) replace the correlations by the tension matrix, full; (b) replace by the compact matrix; (c) keep the
   correlations and add the tension matrix as a second figure; (d) neither.
4. **The solver's attribute `objective_`** and `objective_*` function names in `src/`: (a) rename to loss now (no release yet);
   (b) keep the names and the prose, which the 15:50 ruling's "everywhere" does not allow, so (a) unless he says otherwise.

## 8. Plain options for the build

- **Scope A, all of it:** lemma L21 into `derivation/`, the definition beside elasticity (Section 4) and Appendix A and B rows,
  `tension_matrix` and `design_tensions` into `src/` with doctests and tests (finite differences as the test), Figure 7's
  decision, the glossary and checker changes with the schema, the mechanical loss pass, the entry-surface edits, the Section 3
  paragraph, the docs page on the routes back to attributes and the design space.
- **Scope B, definition and glossary first:** lemma, definition, glossary, schema, checker, mechanical pass and entry edits; the
  package function, the figure and Section 9's sentence in a second package.
- **Scope C, as B without the mechanical pass**, which becomes its own package.

## 9. What the paper may say now, may not, and what the next release builds

May say now: tension is the derivative along the surface, in the metrics, with its cases; the term's matrix (from the fit) and a
design's tensions (from the data) are two objects; both are computable and agree with finite differences on the case; the
attribute-unit route through Theorem 7. May not: that a tension is the effect of changing a design variable, that it is
constant along a term (the elasticity is), a value at a seam, or a tension for collinear metrics as a separate trade. Next
release builds: the package function, the routes back to the design space for the other methods (kernels), and the seam's
one-sided values as reported pairs.

## Not done, and checks

- The cold read of the figure (R-3): left to the PM, brief in `figure-review.md`.
- `git diff --stat dev..wp42` touches only `work-packages/WP42-rounds/` (R-5).
- Ruff passes on the spike folder; the repository's test suite was not run (nothing outside the folder changed).
