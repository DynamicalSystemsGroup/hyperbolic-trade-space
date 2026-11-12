# WP38 — Scope of work: the residual pass (patterns that read as machine-written)

| | |
|---|---|
| **Status** | DRAFT, for the chief engineer's approval. Approved only by the recorded act below; nothing is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The chief engineer's approval, quoted verbatim in `work-packages/WP38-decisions.md` |
| **Acceptance record** | The chief engineer's acceptance, quoted verbatim in `WP38-decisions.md`, after `WP38-review.md` |

## Purpose

The supervisor's direction, verbatim (`WP38-decisions.md`): "as we get close to the end there is another kind of a
review i want. this review eliminates LLM residuals or patterns that feel like LLM. often this is unecessary
metanarration, parentheticals or out of place caveats or spurious details that either dont belong in that location or
dont belong at all. llms love details so much so they inject them where they dont belong". He added: "you can work in
parallel to build the review machinery for this review"; that the use of the machinery "becomes part of the final
deliverable" and, being late, "shouldn't really cover anything but style improvements and minor copy editing level
decisions"; that LLMs "construct overly complex gramatical structures that are hard for human readers to parse"; and
that "within any particular document we should use plain language where it suffice and terms of art where needed to
streamline or reference properly. define clearly on first use. this holds for acronyms as especially."

The package builds the machinery now (the reader's brief, the flag and confirmation forms, the surface inventory, the
mechanical checker with its baseline), and runs the pass once the prose surfaces are stable: after WP33, WP35, WP36,
WP37 and the WP39 build land, before the final reader round, so that round reads the cleaner text. Fresh readers go
over every prose surface with one lens, where does this read as machine-written; each flag gets a disposition; the cuts
land as negative edits; a second fresh reader confirms each surface. The machinery and its records ship with 0.1 and
are named in the reviewer's guide, so a later reader can re-run the pass. Head at scoping: `dev` at `35619df`.

## Goals

- G1. **The lens is written down:** a reader's brief with ten kinds of residual, each defined in one line and shown by
  an example from this repository's own earlier drafts where one exists, and the pass's reach stated (copy-editing only).
- G2. **Every prose surface is listed and assigned:** an inventory with word counts, so none is missed.
- G3. **The mechanical patterns are reported, never edited:** a checker with a committed baseline, so the counts can
  be seen to fall (or at least not rise) across the pass.
- G4. **Every surface is read with the lens and confirmed clean** by a second fresh reader; flags are tabled with a
  disposition and a reason; the cuts land as negative edits with their backing kept.
- G5. **The machinery and its use ship with 0.1,** named in the reviewer's guide.

## Non-goals

- Any change to a claim, a number, a figure, a structure or a placement. A flag that is more than copy-editing goes to
  the owning package or the supervisor's list and is not touched.
- Rewriting for style beyond the ten kinds; new content; a new house style.
- An automatic rewriter or any script that edits prose: the checker reports, readers decide.
- Duplicating `scripts/check_vocabulary.py` (the project's own terms stay its job).
- Appendix G.2's new table (what we say, the source, where in it) and the human validation of the reading pass: owned
  by the paper-notebook unit and the supervisor's close read (`WP38-decisions.md`). The pass reads G.2 as it then renders.
- Anything under `src/`, `derivation/`, `pyproject.toml`, `uv.lock`, the data or the model.
- Running the pass before the surfaces are stable.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-0 | This scope of work, committed and pushed alone | all |
| D-1 | `docs/superpowers/notes/residual-review.md`, the reader's brief: the lens; the ten kinds (metanarration; second-thought parenthetical; caveat with no claim; misplaced detail; hedge against a definite record; signposting the structure gives; restatement; stock intensifier; grammatical complexity; jargon), each with a one-line definition, an example from the repository's drafts where one exists (under 25 words, with commit), and a disposition; the pass's reach | G1 |
| D-2 | The flag table format (surface, location, sentence, kind, proposed disposition cut/move/keep/split/define, reason) and the second reader's confirmation form, both in the brief | G4 |
| D-3 | `scripts/prose_surfaces.py`: every prose surface (paper body and appendices by section, docs pages, README, root page, history page, the glossary's long forms) with word counts | G2 |
| D-4 | `scripts/check_residuals.py`, a report only, with `scripts/residuals_baseline.json` and `tests/test_residuals.py` | G3 |
| D-5 | The pass plan, in the brief: readers per surface (Sonnet, fresh, rendered pages for the site and the paper, the README as GitHub renders it); the implementer landing cuts as negative edits under the ledger and the claims register; entry-surface changes listed for the supervisor; the second reader's confirmation per surface | G4 |
| D-6 | The pass's records (`WP38-flags/` tables, `WP38-confirmations/`), `WP38-review.md` with the checker's before and after, `WP38-decisions.md` | G4 |
| D-7 | The reviewer's guide skeleton (`work-packages/WP8b-reviewers-guide-skeleton.md`) names the brief, the inventory, the checker with its baseline, and the pass's flag tables and confirmations | G5 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The brief names exactly ten kinds, each with a one-line definition and a disposition rule; the examples are from this repository's history, verifiable, and under 25 words | `grep -c '^### Kind ' residual-review.md` returns 10; each example's commit resolves with `git show` |
| R-2 | The brief states the reach: copy-editing only; never a claim, number, figure, structure or placement; beyond that, routed to the owning package or the supervisor's list | read the section; a pass flag of that sort appears in the table as "routed", not edited |
| R-3 | Kind 9 prescribes split or reorder, never added words; kind 10 prescribes the plain word or a definition at first use, never a gloss repeated at later uses | read the two kinds |
| R-4 | The flag table has the six columns; the confirmation form records per surface the reader, the rendered view used, the verdict and any remaining flags | the forms in the brief; one filled example row each |
| R-5 | The inventory lists every prose surface once, with a word count and an assigned reader slot; its listing includes the paper's body and each appendix by heading, every `docs/*.md` and `docs/user-guide/*.md`, `README.md`, `site/index.html`, `site/history.html` and the glossary's long forms | `uv run python scripts/prose_surfaces.py`; its totals against `find` and the paper's headings |
| R-6 | The checker reports per surface: counts of metanarrative openers, hedges, stock intensifiers, parentheticals per paragraph, restatement-by-overlap sentences, sentence length and clause depth (signals), and per document the acronyms and glossary terms with line of first use and whether a definition or glossary link precedes it; it writes no prose file and does not repeat `check_vocabulary.py` | `uv run python scripts/check_residuals.py`; test that no tracked file changes after a run; grep of imports |
| R-7 | The baseline `scripts/residuals_baseline.json` is generated at the head the tooling branches from, and the report is stable in form (same keys, same order, rerun gives identical output) | `uv run pytest -q tests/test_residuals.py`; two runs diffed |
| R-8 | During the pass, the checker's counts per surface do not rise against the baseline | the checker's comparison mode; `WP38-review.md` before and after |
| R-9 | Every surface is read by a fresh Sonnet reader and confirmed by a second fresh reader, each on the rendered page, not the source | the flag tables and confirmations, one per inventory row |
| R-10 | Every cut is a negative edit: the ledger and the claims register show it, a moved claim keeps its backing, and each cut states what the sentence no longer did | `uv run pytest tests/test_claims_register.py tests/test_paper.py tests/test_site.py tests/test_docs.py`; the decisions record |
| R-11 | No claim, number, figure, structure or placement changed by the pass | `git diff` of numbers and labels over the pass; the generated outputs unchanged (`uv run pytest tests/test_paper.py`); the second reader's confirmation |
| R-12 | Entry-surface changes (`site/index.html`, `README.md`, the paper's abstract, `site/history.html`, `docs/index.md`) are listed in `supervisor-review-list.md` "Entry surfaces" with reason and commit | the list against `git log` of those files |
| R-13 | The reviewer's guide names the machinery and its records (D-7) | grep of the skeleton |
| R-14 | Whole-repo `uv run ruff check .` and `uv run ruff format --check .`; `uv lock --check`; `tests/test_text_encoding.py`; `tests/test_residuals.py`; vocabulary check unchanged; no AI attribution | the commands; grep of `git log` |

## Definition of good

- A reader of any surface meets sentences that say rather than announce; each sentence parses at one pass; every term
  of art and acronym is met after its definition in that document; nothing was added to make that so.
- The brief is short enough that a new reader applies it without the author present, and the checker's report is a
  page a person can scan.

## Definition of good enough

- D-1 to D-4 exist and pass R-1 to R-7; the pass plan is in the brief.
- On the pass: every inventory row read and confirmed (R-9), the checker's counts not rising (R-8), no claim lost
  (R-10, R-11), entry-surface changes listed (R-12), the guide naming the machinery (R-13), gates pass (R-14).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent models by role

Sonnet for implementers, first and second readers, triagers and reviewers; Haiku for mechanical units (counts, the
inventory run, screenshot runs); nothing larger. Readers get rendered pages only. No sub-agent without the PM.

## Rounds and stopping rule

The tooling is built once, reading and tooling only. The pass is one read per surface, one landing unit per surface and
push, one confirmation per surface. A surface whose confirmation lists remaining flags gets one more round; after that
the remaining flags are listed for the chief engineer. Stop when every surface is confirmed or listed.

## Agent's defaults

- The brief's path, the script names, the baseline format (JSON) and the test name are as in D-1 to D-4 *(default)*.
- Signal thresholds in the checker (a long sentence, clause depth, a dense paragraph, overlap for restatement) are
  chosen to flag for a reader's attention, not to fail a build; the test checks form, not thresholds *(default)*.
- Word counts by visible text; the glossary's long forms counted by their `short` and `formal` fields *(default)*.
- Acronym detection: capitalised tokens of two to six letters, with a small list of common non-acronyms ignored *(default)*.
- Examples in the brief come from `git log -S` over the paper, docs, README and root page; a kind without a surviving
  example says so *(default)*.
- Readers per surface are one first and one second, never the same agent; the README is read as GitHub renders it
  *(default)*.
- The pass records are `WP38-flags/<surface>.md` and `WP38-confirmations/<surface>.md` *(default)*.

## Open decisions (for the chief engineer)

None. Every item was resolved through the decision loop (`WP38-decisions.md`: the direction, the reach, the two added
kinds, and the machinery shipping with 0.1).

## Blast radius

- New: the brief, `scripts/prose_surfaces.py`, `scripts/check_residuals.py`, `scripts/residuals_baseline.json`,
  `tests/test_residuals.py`, `WP38-*` records; `work-packages/WP8b-reviewers-guide-skeleton.md` (D-7).
- During the pass, prose only: the surfaces the inventory lists, `paper/length_ledger.toml` (down only),
  `claims_register.toml` where a cut touches a row, the entry-surface list in `supervisor-review-list.md`.
- Never: `src/`, `derivation/`, `pyproject.toml`, `uv.lock`, data, the model, figures, numbers, the `verify` and
  `stage` worktrees, tab-23.

## Lifecycle stages

(1) Research: the kinds, with examples from history. (2) Decide: the reach and the forms (recorded). (3) Build: the
brief, the inventory, the checker and its baseline. (4) Quality control: the checker on the head, the test, the first
reads. (5) Integrate: cuts landed under the ledger and register; the guide updated. (6) Cascade review: second
readers, the checker's before and after, the entry-surface list.
