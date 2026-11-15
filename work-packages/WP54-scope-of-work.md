# WP54 — Scope of work: the paper's skeleton

| | |
|---|---|
| **Status** | Approved verbally, "approve 53 and 54" (2026-11-15, `WP54-decisions.md`); executes after WP53 lands |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `dev` |
| **Approval record** | His words, quoted verbatim in `WP54-decisions.md` |
| **Acceptance record** | His read of the rendered sections on the staged site; his word quoted verbatim in `WP54-decisions.md` |

## Purpose

Fix the section list before anyone edits inside the sections (WP55 to WP57): the preliminary search section folded
into Future work, Future work written fresh from the spike records and kept short, and one short informational
closing section on AI use and reproducibility in place of two.

## Goals

- G1. Section 7, "Search of the design space (preliminary)", is no longer a section. What it says that is still true
  goes into Future work under the search direction, in a few sentences; its conjecture and its open point go to the
  open-questions ledger that WP57 builds into the appendices.
- G2. The section is titled "Future work". It is written from the spike records, not patched: WP41 (the way back from
  the chart and the search), WP43 (the kernel direction), WP48 (the checks), WP50 (holes by topological data
  analysis and its dependency choice), WP36 and the formal direction (the Lean theorem prover, the Rust core); each
  direction states what the spike found and what the next release builds, within the boundary the readouts set
  ("fruitful enough to name as a direction, not as a result"). The abstract's three thrusts are its spine. It
  states plainly what this release accomplished before it names what comes next. It is short.
- G3. "Reproducibility and your own case" and "Acknowledgments and process" become one section, "AI acknowledgement
  and Reproducibility": what AI assistance did and did not do, how the work was gated and checked, how every figure,
  table and number is reproduced and how a reader adapts the pipeline to a table of their own. Informational, short,
  no sentence about the text itself. It does not call the derivations machine-checked or formally verified; they are
  scripted checks (`docs/superpowers/notes/proof-conventions.md`).
- G4. Everything that pointed at the old sections follows: the roadmap paragraph of Section 1, the numbering, the
  labels (`sect-search`, `sect-reproducibility`, `sect-process`) in the paper, the docsite (`docs/bridge.md` points at
  the search of Section 7) and the tests; the register rows of the removed and rewritten text.

## Non-goals

- The Discussion's content (WP56 owns it, including how it leads into Future work); the appendices beyond the
  labels they share (WP57); Sections 4 to 6 (WP55).
- Any new result or claim. Future work names directions, each backed by its record.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The paper notebook with Section 7 removed, its surviving sentences in Future work, the conjecture listed in `work-packages/review/open-questions.md` (the ledger WP57 consumes) | G1 |
| D-2 | "Future work", under 250 words, each direction with its record named in `work-packages/WP54-review.md` | G2 |
| D-3 | "AI acknowledgement and Reproducibility", under 200 words, replacing the two sections | G3 |
| D-4 | The roadmap paragraph, labels, docs page, tests and register rows updated; notebooks re-executed; the lot landed on `dev` with CI | G4 |
| D-5 | `work-packages/WP54-review.md`: the verification record and a table of every sentence of the old Section 7 and the old Future work with its fate (kept where, cut, to the ledger) and the record behind each new sentence | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | No section in the paper is a preliminary or a remark: eleven numbered sections (the decision problem through AI acknowledgement and Reproducibility) and Works cited, as the roadmap and `paper-requirements.md` name them | the roadmap paragraph and the rendered table of contents agree |
| R-2 | No label is dangling | the MyST build log has no warning about a missing label; `grep -rn "sect-search\|sect-process\|sect-reproducibility" paper docs tests` returns only live targets |
| R-3 | Future work names the three thrusts of the abstract in its order and no direction without a record | the review file's table |
| R-4 | Words: Future work under 250, the closing section under 200 | `wc -w` on the cells' prose in the review file |
| R-5 | No metanarration | `scripts/check_residuals.py` exit 0; a read of both sections against CLAUDE.md's rule |
| R-6 | Lint, format, lock, residuals, vocabulary, the fast suite, the slow paper tests, CI both platforms | as WP53 R-3 to R-8 |

## Definition of good

A reader of the paper meets the search once, as a direction in Future work; the last two sections say in plain
sentences what was built, what was used to build it, how to rerun it and what comes next.

## Definition of good enough

R-1 to R-6 met and recorded; his read of the two new sections on the staged site with no change asked, or his edits
applied in place and the package re-verified.

## Definition of done

Good enough met, no open item, his acceptance quoted in `WP54-decisions.md`.

## Open decisions

None.

## Agent's defaults

- The "Final remark" paragraph (a forecast V for a new technology) is cut: an aside, not a result or a direction.
  He can restore it in one line.
- `docs/bridge.md`'s sentence pointing at Section 7 points at Future work's search direction.
- The ledger file `work-packages/review/open-questions.md` lists each open question with the section it left and its
  record; WP57 decides what enters the appendix section.
- Future work's order follows the abstract: the search; holes by topological data analysis; formal verification and
  performance. What was accomplished comes first, in one short paragraph.
