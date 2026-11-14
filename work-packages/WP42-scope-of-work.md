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
