# WP42 — Scope of work: tension, and the glossary's terms across decision analysis, optimization and learning

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP11-decisions.md` (the abstract pass) or a `WP42-decisions.md` |
| **Acceptance record** | The supervisor's acceptance, quoted verbatim, after `WP42-review.md` |

## Purpose

The supervisor's readings of 2026-11-14 (`WP11-decisions.md`, "The abstract pass", verbatim): the terms loss, metric,
attribute and objective conflict across decision analysis, optimization and machine learning; the glossary settles
each with one meaning and the surfaces hold to it, the intuitive surfaces carrying plain words and the caveats living in
the entries and the detailed sections. Tension is defined: the partial derivative between two metrics along the
surface, in the conditioned metrics, at a point; negative where both contend, zero where one carries no exponent,
piecewise at K > 1; two objects kept apart, the term's tension matrix from the fit (at the balanced point) and a
design's tensions from the data (at its metric ratios); routes back to attribute units and the design space in the
docs. A bigger candidate edit (a new defined object with a lemma step, a method and a figure), so it runs the six
stages; this scope is the research spike and the decision gate, with the build stages scoped from the readout.

## Goals

- G1. **Tension is defined once, derived and computable:** a definition beside elasticity (Section 4), one lemma step
  (the chain rule from L7 for the metric-space derivative and from L9 for the pull-back to attribute units) scripted as
  the others are, and a prototype that returns the term's tension matrix at the balanced point and a design's tensions
  at its row, in metrics and in attribute units, checked against finite differences on the case.
- G2. **The figure is designed and judged as rendered:** the term's tension matrix drawn per term beside, or in place
  of, Figure 7's data correlations, through the figure-review loop with the readers' words from the final round
  (three cells on the association panel's label), with a cold read of the redraw.
- G3. **The glossary settles the contested terms:** entries for objective (a metric a decision-maker wants more of),
  constraint (a requirement's limit), trade-off, tension, the solver's function (loss, or objective kept: OD1), measure
  of effectiveness and measure of performance, proposal and check (shared with WP41); each entry says which register
  uses the word; the checker's stems extended to objective, loss, tension and trade-off; the surfaces brought into line,
  the abstract excepted (the supervisor's hand).
- G3b. **The three layers are stated once:** the glossary's preamble names the decision layer (objectives,
  constraints, the Pareto notions), the design layer (the model as a function of the metrics inside a designer's
  optimization; GGP and log-convex belong here) and the method layer (the fit as an optimization over the exponents;
  its word is loss), and every entry names its layer; Section 3 covers it in brief and cites Appendix A (the supervisor's
  ruling of 16:05, `WP11-decisions.md`). The readout drafts both texts.
- G3c. **The entry surfaces follow the abstract** (the supervisor's direction of 18:15; the read is
  `WP11-final/abstract/entry-surfaces-consistency.md`): the build's first list is the four small edits (the root page's
  What: "explains trade-offs" for "explains tensions", "contend" for "compete"; "unsupervised learning, beside PCA" on
  the root page and the docs home in place of "and feature engineering"; the README's Layout line "fit a frontier, read
  its trade-offs"), and the readout settles the two naming items (one word for gap, hole and white space; whether the
  package's `tension_report` gains the tension matrix and keeps its name or is renamed, the README and root page
  following). The root page's summary paragraph and its "bespoke or opaque" sentence are the supervisor's and are not
  touched.
- G4. **The decision section's number:** the readout states what one sentence of Section 9 would say with a design's
  tension at the picked design between the operator's and the sponsor's measures, in attribute units, for the
  supervisor to accept or decline at the gate; nothing lands in the paper in this scope.

## Non-goals

- Landing the definition, the figure, the method or the glossary changes: the build stage, scoped from the readout.
- Any change to the abstract.
- The seam's one-sided values beyond reporting both; any smoothing across terms.
- Renaming the solver's function throughout the theorems unless OD1 chooses it.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP42-rounds/spike/readout.md`: the definition with its cases (negative, zero, blank, reciprocal, piecewise), the lemma step's statement and script name, the prototype's matrices on the case at K = 1 and K = 2 (balanced point and the picked design), the finite-difference check, the figure recipe and its cold read, the glossary entries drafted with their registers, the Section 9 sentence drafted, plain options for the build | G1 to G4 |
| D-2 | `work-packages/WP42-rounds/spike/` scripts and images: the prototype (not in `src/`), the figure before and after, the checker's dry run with the extended stems and its new violation count | G1, G2, G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The definition's formula and the lemma step agree with Definition 8 and Theorem 7 (the derivative in log units is minus the exponent ratio; the metric-space derivative is that times m_j/m_i; the attribute-space derivative carries the conditioning slopes) | the script's `verify`; the finite-difference check on the case |
| R-2 | The two objects are named apart in the readout and the drafts (the term's tension matrix, from the fit; a design's tensions, from the data) | the readout's text; the vocabulary check on the drafts |
| R-3 | The figure's redraw passes the loop's five tests with the readers' words quoted and a cold read recorded | `WP42-rounds/spike/figure-review.md` |
| R-4 | The glossary drafts leave the vocabulary checker at zero new violations on the surfaces, the abstract excepted | `uv run python scripts/check_vocabulary.py` on the drafts' dry run |
| R-5 | No file under `src/`, `paper/`, `docs/` or `glossary.yaml` changes in this scope | `git diff --stat` |

## Definition of good

- A reader who sees the tension matrix knows what one cell means, which cells are empty and why, and how to read the
  same number for a design in its own units; and the glossary answers "objective or metric?" in one line.

## Definition of good enough

- D-1 and D-2 delivered; R-1 to R-5 pass; the readout's options are plain and carry no recommended tag.

## Definition of done

Good enough is met, no open item remains unresolved, and the supervisor has accepted the readout; the build is then
scoped from it.

## Agent's defaults

- The balanced point is the softmax-weighted mean log-metric of the term's rows at the fit temperature, which the fit
  already computes *(default)*.
- Blank cells (j carries no exponent) are drawn as empty, not as zero; zero cells (i carries no exponent) are drawn as
  zero *(default)*.
- The figure's colour scale is signed and symmetric about zero, one colour family per sign, and the reciprocal triangle
  is drawn in log scale so the two triangles read alike *(default)*.
- The spike runs in a worktree on Sonnet; the cold reader is Haiku *(default)*.

## Open decisions (for the supervisor)

None. OD1 closed on 2026-11-14 at 15:50 (`WP11-decisions.md`, verbatim): loss for the solver's function everywhere,
the choice stated where the notation is set and in the glossary; objective reserved for the decision-analysis frame,
the subset of the metrics the decision-maker optimizes for. G3's entry for the solver's function is therefore "loss",
and the build stage carries the mechanical pass over the theorems, Appendix A, the scripts' docstrings and the tests.

## Amendment 1 (2026-11-14, 23:05): the build after the spike, as he chose it

Approved by his word on the readout's options ("Scope A, all of it", 20:30) and his four answers (`WP42-decisions.md`,
20:35 to 23:05). The build adds to the approved scope, in one unit on a branch from dev, with the spike's scripts as the
source of record:

- **Lemma:** `WP42-rounds/spike/lemma_tension.py` becomes `derivation/lemma_21_tension.py` with its hypotheses in the
  ledger and a row in Appendix B; `derivation/run.py` runs it.
- **Definition:** tension beside elasticity in Section 4 (the derivative along the term in the conditioned metrics; the
  negative, zero, blank, reciprocal and piecewise cases; the term's matrix from the fit at the balanced point and a
  design's tensions from the data, two objects), Appendix A rows; the attribute-unit route through Theorem 7 stated.
- **Package:** `tension_matrix` and `design_tensions` in `src/`, numpydoc with doctests, finite differences as the test
  (the spike's check, cells and tolerances); the renames of item 2: `trade_off_report`, `spread_directions`,
  `spread_loadings`, `plot_association`; the solver's `objective_` and `objective_*` names to loss; the interface
  contract amended (schema fields `layer`, `used_in`, `elsewhere`; the file key `preamble`; the renamed members).
- **Figure 7:** the compact tension matrix per term with the caption of item 3; the old figure's code retired from the
  paper; figure-loop test 1 re-run on the final caption, image alone then caption, reports committed verbatim.
- **Section 9:** the accepted sentence, numbers generated; claims row; ledger row.
- **Section 3:** the three layers in brief, pointing to Appendix A (the spike's draft).
- **Glossary and checker:** the drafted entries (objective, constraint, trade-off, tension, tension matrix, design
  tensions, loss, white space with hole and gap as avoided variants for that object; MoE and MoP revised; the preamble
  with the three layers in full); extended stems; the mechanical pass over paper, `src/`, user guide, README and root
  page (about 107 objective, 52 tension, 136 gap, 22 hole, 9 white space mentions by the spike's count), each use
  moved to its layer's word; the checker's baseline reduced, not extended.
- **Entry surfaces:** the four small edits of G3c; the root page's summary paragraph and "bespoke or opaque" untouched.
- **Docs:** a page on the routes back from a tension in the metrics to attribute units and to the design variables
  (what is computable, what is a conjecture past the sampled designs), linked from the user guide.

Non-goals unchanged; `hole` stays undefined in 0.1 (reserved, WP50). Good enough adds: the finite-difference tests
pass; the checker shows no new violation and a smaller baseline; the renamed API page renders; the figure's cold read
is in; the full suite, lint, format and lock check pass; `derivation/run.py` passes with L21.

