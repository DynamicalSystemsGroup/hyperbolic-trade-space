# WP41 — Scope of work: the bridge to the search, part 1 (framing and docs page)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP41-decisions.md` |
| **Acceptance record** | The supervisor's acceptance, quoted verbatim in `WP41-decisions.md`, after `WP41-review.md` |

## Purpose

The supervisor's direction of 2026-11-14 (`WP41-decisions.md`, verbatim there): going from the chart back to the design
space loses invertibility, as intended; a point with a datum maps back to its design; a point without one gives a
proposed design that is a conjecture, needs a selection rule because the preimage is not unique, and may be refuted when
built and measured; this is the bridge to the search, to be researched and implemented in the repository without
changing the paper beyond its names, because the overall approach must be well posed even where the exact how is open.
His timing ruling: framing and docs page in 0.1; interface and demonstration in 0.2. This package is the 0.1 part.

## Goals

- G1. **The approach is stated once and is well posed:** a note names the forward map and where it loses invertibility
  (evaluation: many-to-one, not onto, noisy), the preimage set of a chart point, a proposal (a configuration, its
  predicted chart point, a tolerance; a conjecture until checked), the selection rules with a declared default, the
  check and its three outcomes (confirmed; refuted, a row the table lacked, so the fit is rerun; infeasible), the
  outer loop as the refit, and what stays open (the submartingale conjecture of `WP36-decisions.md`, future work).
- G2. **The existing pieces are audited against the note:** the regressor (`src/hyperbolic_trade_space/predictive.py`),
  the pooled-configuration proposal and its radius rule, the check designs (`examples/adcs/make_check_designs.py`, D.10),
  the noise injection (`examples/adcs/noise_injection.py`) and Section 7's prose; each is placed in the note's terms or
  named as missing.
- G3. **A reader of the docs can follow the story:** a docs page tells the sampled route (a chart point with a datum is
  its row, so its configuration is known) and the conjecture route (propose, predict, check) apart, with the routes
  back to attribute units (Theorem 7) and to the design space, and says what 0.1 ships and what the next release adds.
- G4. **The paper's Section 7 names the procedure and claims nothing new:** one paragraph with the objects' names and the
  open item as the supervisor states it; no result, no figure, no new number.

## Non-goals

- The package interface (`propose`, `check`) and its tests: 0.2.
- The case demonstration running the loop through the simulator with a Monte Carlo evaluation: 0.2.
- Any derivation or condition for the submartingale conjecture: future work by the supervisor's ruling.
- Any change to the abstract (the supervisor's hand), to Sections 8 and 9, or to the decision section.
- Deciding the selection rule's mathematics beyond naming two or three candidates and a default for 0.2 to build.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP41-rounds/spike/readout.md`: the well-posedness note, the audit table of the existing pieces, two or three selection rules prototyped on the case (one run each, recorded), plain options for the default rule and the interface's shape for 0.2 | G1, G2 |
| D-2 | `docs/bridge.md` (title and place per the defaults), built into the docsite, linked from the docs home's navigation line and from the Examples page's search mention | G3 |
| D-3 | Section 7 of `paper/paper.ipynb`: one paragraph naming the procedure; the open item in the supervisor's words (change request 169 lands it if first) | G4 |
| D-4 | Glossary entries for proposal, selection rule, check (and their aliases), with the checker's stems extended; claims rows for every new sentence | G1, G3, G4 |
| D-5 | `work-packages/WP41-review.md`: the review, with the docs page read in a browser by one fresh reader (P3 or P9) and the screenshot held per the WP40 rule | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The note's objects each have one name, in the glossary, and the docs page and Section 7 use those names and no other | `uv run python scripts/check_vocabulary.py`; grep of the page and the paragraph for the names |
| R-2 | Every sentence of the docs page and the paragraph is backed (a lemma, a generated value, a test, a verified source) or narrowed; the conjecture is called a conjecture; the 0.2 items are named as not shipped | claims rows in `claims_register.toml`; `uv run pytest -q -m "not slow"` |
| R-3 | The audit names every existing piece and says where it sits in the note's terms or that it is missing | the readout's table, checked against `git grep` of the module and script names |
| R-4 | The prototypes run from the committed data of record and are recorded with their rule, their proposal and its predicted point | the readout's run records; the commands reproducible in the container |
| R-5 | The page builds, renders without a stderr line, and is reachable from the docs home | `uv run python scripts/stage_site.py`; the browser pass with screenshot |
| R-6 | Nothing in the abstract, Sections 8 and 9 or the decision section changes | `git diff` of the notebook cells |

## Definition of good

- A reader who asks "if I pick a point on the surface with no design under it, what do I do?" finds the answer on one
  page: it is a conjecture, here is how a design is proposed, here is how it is checked, here is what each outcome
  means, and here is what is still open.

## Definition of good enough

- D-1 to D-5 delivered; R-1 to R-6 pass; the fresh reader of the docs page states the sampled route and the conjecture
  route apart and names the three outcomes without being told; the paper's word count moves by the paragraph only,
  with its ledger row.

## Definition of done

Good enough is met, no open item remains unresolved, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- The docs page is `docs/bridge.md`, titled "From the chart back to a design", in the user guide after Examples
  *(default)*.
- The selection rules the spike prototypes are: nearest configuration in the pool (the existing rule), smallest change
  from a named reference design, and a constrained search over the surrogate; the default proposed for 0.2 is whichever
  the readout shows reaches its target within the band most often on the case *(default)*.
- The tolerance of a check is the fit's band 1/tau *(default)*.
- Section 7's paragraph replaces no existing sentence but the Open one (request 169) and adds at most 60 words
  *(default)*.
- The spike runs in a worktree on Sonnet; the docs page's fresh reader is Haiku *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (the timing ruling of 12:30; the outer loop ruling of 12:20).
