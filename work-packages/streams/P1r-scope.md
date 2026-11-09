# P1r - Scope of work: reader tests of sections 4 and 6

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | posynomial-invariant-form, branch `dev`; this document lives in `work-packages/streams/` |
| **Approval record** | The driver's approval message under the mandate of `work-packages/release-candidate.md`, recorded in `work-packages/driver-log.md` |
| **Acceptance record** | A fresh-context reviewer's check against these requirements, recorded in this file, then the driver's verification |

**Blast radius.** Exactly one file is written: `work-packages/WP10-reader-tests.md`. `paper/paper.ipynb`
is read-only (single owner: P1). One push (rebase on `origin/dev`; `git push origin HEAD:dev`).
**Start condition:** P1's first pass is pushed; the PM records its commit hash and pins it.

## Purpose

Two tickets in `WP10-decisions.md` change the paper's prose and name the tests of the result. On
section 4: "i think the energy interpretation of the invariant form needs to be narrated otherwise it
comes out of thin air ... we need to pass muster for an ML or convex optimization expert but also
support a reader who is trad engineering decision analysis practicianer". On section 6: "needs to
flow for a reader who is reading the math closely AND a reader who is just skimming the math". The
prose is only as good as its readers' answers; P1 edits, this stream tests. On length the supervisor
said: "the total length of the paper is less hard ceiling and more regularization. each word earns
his place, and more text has a higher burden". Findings that ask for more words must say what the
words are for.

## Goals

- G1. Section 4 (Definitions 2 to 5) is read by three fresh personas, each of whom states the arc and
  reports where the energy interpretation comes out of thin air or a term is unresolved.
- G2. Section 6 is read by a skimmer (boxes hidden) who states the arc, and a close reader (whole
  section) who looks for any sentence looser than the box it introduces.
- G3. Every finding is quoted and routed, so P1 can act and nothing is lost.

## Non-goals

- Editing any prose, notebook, glossary or glossary page; fixing findings (P1 does, on a change request).
- Other sections, other depths or the full reader grid (WP11); judging the mathematics (P4 owns it).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP10-reader-tests.md`: pinned hash, each reader's brief and answer verbatim, findings table with routing | G1, G2, G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The pinned commit hash is recorded and every read used that commit's rendered text | `git cat-file -t <hash>`; hash appears in D-1 |
| R-2 | Section 4 readers: trade-study practitioner, ML practitioner, optimization reader, each given only the rendered section and the rendered Glossary page, no repository access; each answer present verbatim | `grep` D-1 for three persona headings, each with a non-empty verbatim block |
| R-3 | Section 6 skimmer given the section with boxes hidden; close reader given the whole section; both without repository access; answers verbatim | `grep` D-1 for two headings with verbatim blocks; inspection of the briefs |
| R-4 | Each reader's brief is recorded and contains no hint of the intended arc | Inspection of the briefs in D-1 |
| R-5 | Every finding quotes the sentence it concerns and carries a routing: a change request to P1, or no change with a stated reason | Inspection of the table: no empty quote or routing cell |
| R-6 | The stream writes one file and edits no prose | `git diff --stat <pinned>..HEAD` lists only `work-packages/WP10-reader-tests.md` |

## Definition of good

- A second round after P1's fixes, repeated until each reader states the arc correctly and the close
  reader finds no sentence looser than its box, with each round on a new pinned hash.

## Definition of good enough

- All five readers have run once on the pinned commit (R-1 to R-4), and every finding is routed (R-5),
  with the diff check passing (R-6).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- Readers are fresh subagents, one per read, with no shared context *(default)*.
- The rendered text is taken from the pinned commit's built paper page, and the Glossary page from the docsite *(default)*.
- Each reader is asked to state the arc in a few sentences, then to list unresolved terms and unsupported leaps *(default)*.
- Round 2 is appended under a new heading in the same file *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop.
