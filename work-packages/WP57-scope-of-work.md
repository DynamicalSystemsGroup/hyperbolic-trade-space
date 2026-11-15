# WP57 — Scope of work: the appendices (a planning package and its children)

| | |
|---|---|
| **Status** | DRAFT for the driver's approval as his proxy; executes after WP56 lands (the appendices follow the prose they support), children one at a time on the supporting notebook |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `dev`; `paper/supporting_material.ipynb` and the generators under `paper/` |
| **Approval record** | The driver's approval under his mandate, quoted in `WP57-decisions.md`, with his direction of 2026-11-15 |
| **Acceptance record** | The driver's soft-confirm of each appendix on screenshots against `paper-requirements.md`; his read afterwards |

## Purpose

His direction (`WP57-decisions.md`): the appendices "need to be tightened down. we accreted a lot of material ...
material that doesn't earn its place in the appendices can still live [in the repository]. i want you to spend some
cycles ensuring the appendices directly support the prose, primarily as one step deeper where needed. do not
metanarrate. the appendices job IS NOT to opine on the text of the paper." And: "the appendices package was a bit too
big so you probably need to plan for another layer of work packages for each appendix based on what you find."

The supporting material today: eight appendices, 121 cells, about 4,800 words of prose plus generated tables and
proofs (Appendix D alone 50 cells and 19 subsections; Appendix H 15 cells; Appendix B's proofs generated from the
lemma scripts).

## Goals

- G1. **A map before any edit:** for each appendix, every subsection with the paper sentence that cites it (or none),
  the words and cells it holds, and a disposition: keep as the step deeper; shorten; move to the repository (a file
  named, cited from the appendix in one line); cut. The map is the planning deliverable and the children's brief.
- G2. **Children packages, one per appendix or group, each small and serial:** proposed from the map as WP57a to
  WP57e below, each with its own scope, acceptance on screenshots, and register follow-through.
- G3. **The "Assumptions, limitations and open questions" section** built from Appendix E and the ledger
  `work-packages/review/open-questions.md`: each item with the section it left, what is assumed or not established, and
  its record; no caveat repeated in the main text.
- G4. **Re-lettering once, last:** the appendices in the order of their first mention in the paper, every reference,
  anchor, proof-map section and register row following.

## Non-goals

- Any change to a lemma script or the derivation chain (Appendix B presents them). Any change to the main text
  except the pointers that move with re-lettering. Opinions on the paper's text inside an appendix.

## The children, as the sizes suggest (the map may merge or split them)

| Child | Appendices | What it does |
|---|---|---|
| WP57a | A, F | A: the register of symbols and terms aligned with Section 3's kit and the glossary. F: the toolchain, environment and commands Section 11 points to, one step deeper, nothing the repository's README already says |
| WP57b | B | The proofs Section 6 points to, each reachable by its lemma label; the Derived, Hypotheses and Script material that leaves the main text lands here in the lineage's form; scripts cited, not opined on |
| WP57c | C, D | C: what Section 7 narrates, one step deeper (the SysML v2 model is the model; the appendix refers to it). D: the tables Section 8 reads and no more; of 19 subsections, each kept, shortened, moved to the repository or cut by the map |
| WP57d | E, G, H | E becomes the assumptions, limitations and open questions section (G3). G: the register in the three layers, already reordered. H: kept if Section 2's HoroPCA paragraph needs its three boundaries, else moved to the repository with one line in G |
| WP57e | all | Re-lettering in the order of first mention, references, anchors, proof map, register (G4); the last package before WP58 |

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP57-rounds/map.md`: the map of G1, with the children's scopes derived from it | G1, G2 |
| D-2 | `WP57a` to `WP57e` scopes, each approved as proxy and executed serially, each with its review file and screenshots | G2 to G4 |
| D-3 | `WP57-review.md`: the whole supporting material read at the five depths once the children land | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every appendix subsection kept is cited by a paper sentence or is the step deeper that sentence needs | the map's citation column, no "none" among the kept |
| R-2 | No sentence in an appendix is about the paper's text | `scripts/check_residuals.py`; a read |
| R-3 | Nothing cut is lost: moved material lands in the repository at a named path, cited from the appendix | the map's disposition column with paths; `git` shows the files |
| R-4 | The derivation chain and proof map unchanged by WP57a to WP57d; updated only by re-lettering in WP57e | `derivation/run.py`, `python -m derivation.proofmap` |
| R-5 | Register rows follow every move (ids append-only); the paper tests follow; lint, format, lock, residuals, vocabulary, suites, CI | as WP53 |

## Definition of good

Each appendix is the one step deeper a reader of its section wants, in the register of the main text, and nothing
more; the supporting material reads as one document with the paper.

## Definition of good enough

The map accepted; the children landed one by one, each soft-confirmed on screenshots; re-lettering done once; R-1 to
R-5 met.

## Definition of done

Good enough met, no open item, his read recorded in `WP57-decisions.md`.

## Open decisions

None for him; the map's dispositions are the driver's calls as proxy, listed for his read.

## Agent's defaults

- The map is written by one unit that reads the paper and the supporting material together; the children are
  dispatched by the driver one at a time after WP56 lands.
- A moved file goes under `paper/supplement/` (created) or the case's `examples/adcs/` folder as its content
  dictates, with the appendix citing it in one sentence.
