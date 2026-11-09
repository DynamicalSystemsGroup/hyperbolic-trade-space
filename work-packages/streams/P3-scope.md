# P3 - Scope of work: the vocabulary reading

| | |
|---|---|
| **Status** | DRAFT. Approval = the driver's approval message under the mandate of `work-packages/release-candidate.md`, recorded in `work-packages/driver-log.md`. Nothing is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `posynomial-invariant-form`, branch `dev`; this file is `work-packages/streams/P3-scope.md` |
| **Approval record** | The driver's approval message, in `work-packages/driver-log.md` |
| **Acceptance record** | A fresh-context reviewer's check against these requirements, recorded in this file; then the driver's verification |

**Blast radius.** Exactly one file is written: `work-packages/WP10-vocabulary-review.md`. Every other file is read-only.
The readers run in fresh context with no repository access beyond what they are handed. No worktree is needed for writing
(reads are of a pinned commit; the PM may stage the rendered text of each unit into the scratchpad
`.../scratchpad/pm-worktrees/P3`). The one push: rebase on `origin/dev`; `git push origin HEAD:dev`.

## Purpose

The supervisor asked (`docs/superpowers/notes/vocabulary-review.md`, opening): "make sure its reflected in our glossary
and that we have a documented review technique for jargon checking across our paper and documentation to ensure we're
consistent with our glossary. we should avoid unecessary jargon but use the glossary defined terms to keep the prose
clear and concise." The mechanical check (`scripts/check_vocabulary.py`) says whether each term is ours; only a reading
says whether it is needed. This stream runs that reading once over everything a reader can reach, as one read-only
fan-out, and triages the result. It edits no prose and no glossary.

## Goals

- G1. Every reader-facing unit is read once by a fresh reader who has only that unit and the Glossary page, returning the
  three lists of the note's "The reading" section.
- G2. Every item is triaged to exactly one disposition, per the note's "Triage" section, and recorded in one file.

## Non-goals

- Editing any prose, the glossary, the notation table or the interface contract (dispositions are recorded, not applied).
- Editing sentences in units still being rewritten by P1 (paper prose) or P6 (docs prose); those items are routed, not edited.
- Deciding a change to a term's meaning (those go to the driver).
- Re-running or changing `check_vocabulary.py`; the vocabulary tickets in `work-packages/WP10-decisions.md` stay as they are.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP10-vocabulary-review.md`: the pinned commit, one section per unit with the three lists and a disposition for every item, and a routing table | G1, G2 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The pinned commit (full hash) and the `check_vocabulary.py --density` output used for ordering are recorded at the top | inspection; `git cat-file -t <hash>` |
| R-2 | Units are one per section of `paper/paper.ipynb`, one per page of `docs/*.md` and `docs/user-guide/*.md`, plus `site/index.html` and `README.md`; each has a section in the file, in density order, densest first | compare headings with the unit list built by `ls` and the notebook's heading cells |
| R-3 | Each unit section holds the three lists (unresolved terms; places a glossary term would say it shorter; plain words serve; three or more terms of art in a sentence), verbatim from its reader, "none" where empty | inspection; grep for the three list headings per unit |
| R-4 | Each reader was handed only that unit's rendered text and the Glossary page (the hand-off text is recorded once) | inspection of the recorded hand-off |
| R-5 | Every item quotes its sentence and has exactly one disposition: amend glossary entry / plain words / glossary term / add to `avoid` / no change with reason | grep: every item line has a quote and one disposition word; no item lacks one |
| R-6 | Items on sentences in P1 or P6 units still rewriting are marked "routed to P1" or "routed to P6", with the owner's current state at the pinned commit; items that change a term's meaning are marked "to the driver" | inspection against `work-packages/PM-BRIEF.md` stream state |
| R-7 | Only the one file changed | `git diff --stat origin/dev~1..HEAD` (or the stream's commits) lists only `work-packages/WP10-vocabulary-review.md` |
| R-8 | No AI attribution in the file or the commit | grep the file and the commit message for AI trailers or generation notes, none |

## Definition of good

- Each reader's lists are specific enough that the triage is a decision, not a research task; the dispositions form a short,
  consistent list of amendments the glossary owner can apply in one pass.

## Definition of good enough

- All units read once; all items triaged; R-1 to R-8 pass; the file pushed to `dev` by the one push.

## Definition of done

Good enough is met, **no open item remains unresolved**, and acceptance is recorded as above (a fresh-context reviewer's
check against these requirements, then the driver's verification).

## Agent's defaults

- Density order comes from the `--density` table (densest first); units absent from it follow in path order *(default)*.
- Readers see rendered text (notebook Markdown cells with generated tables; docs pages as built; HTML text), not source *(default)*.
- One reader per unit, run in parallel; a unit too long for one hand-off is split at its headings *(default)*.
- The routing table sits at the end of the file, one row per routed item *(default)*.

## Open decisions (for the supervisor)

None.
