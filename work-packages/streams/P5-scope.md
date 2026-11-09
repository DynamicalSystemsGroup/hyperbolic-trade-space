# P5 - Scope of work: the claims pass

| | |
|---|---|
| **Status** | DRAFT. Approved only by the driver's approval message under the mandate of `work-packages/release-candidate.md`, recorded in `work-packages/driver-log.md`. Nothing is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `posynomial-invariant-form`, branch `dev`; this document in `work-packages/streams/` |
| **Approval record** | The driver's approval message, recorded in `work-packages/driver-log.md` |
| **Acceptance record** | A fresh-context reviewer's check against these requirements, recorded in this file; then the driver's verification |

**Blast radius.** Exactly one file is written: `work-packages/WP10-claims-review.md`. Every other file is read-only, in particular `claims_register.toml` and `tests/test_claims_register.py` (stream P4, pushed). Register rows are landed by a separate follow-up unit under the PM, not by this stream: this stream proposes rows as a fenced TOML block in its file, in the register's fields. One push (rebase on `origin/dev`; `git push origin HEAD:dev`). Extractors run in fresh context with no repository access.

## Purpose

The supervisor directed (`work-packages/WP10-decisions.md`): "i prefer to drop unbacked claims. as part of our narrative, prose and copy editing work we need to sweep for claims to make sure they have backing. this does not mean we need to heavily caveat and reference a claim everytime it appears we just need to know we've not injected spurious details or unsupported claims." The requirement and mechanism are in `docs/superpowers/notes/claims-review.md`. This stream runs steps 1 to 3 once over everything a reader can reach and hands the PM a record of claims, verdicts and dispositions, with proposed register rows ready to land.

## Goals

- G1. Step 1: every claim in the reader-facing prose is listed (fragment of at least six consecutive words, kind M/R/S/L/P).
- G2. Step 2: every claim has a backing pointer or "none" and one verdict: backed / broader than its backing (how) / unbacked.
- G3. Step 3: every claim has a disposition: keep; narrow; drop; or back it (only when a small step already implied, else drop and record as a candidate).
- G4. Rows for the claims that pass are proposed in the register's fields, ready to land.

## Non-goals

- Editing any prose, or landing rows in `claims_register.toml` (the follow-up unit does).
- Editing claims in units P1 (paper text) and P6 (docs text) while they still rewrite: those are routed to their owner, not edited.
- Deciding anything that changes a mathematical statement or a conclusion: routed to the driver.
- Step 4 (the register test) and step 5 (the driver's sampled coverage check).
- Adding caveats, citations or references to the prose to make a claim pass.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP10-claims-review.md`: the pinned commit; per unit the extraction, the lookup (pointer, verdict) and the disposition; items routed to the driver or to P1/P6; candidates for later | G1, G2, G3 |
| D-2 | In D-1, one fenced TOML block of proposed rows in the register's fields | G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Units: one per section of `paper/paper.ipynb`, `paper/supporting_material.ipynb`, each page in `docs/`, `site/index.html`, `README.md`; extractors are handed only rendered text | The file lists the units; compare with `ls docs/*.md` and the notebooks' section headings |
| R-2 | Every unit has an extraction | A script finds a section in D-1 for each unit, none empty without a stated reason |
| R-3 | Every extracted claim has kind, pointer, verdict and disposition | A script over the claim tables finds no empty cell |
| R-4 | Every proposed row's fragment occurs verbatim in its named file at the pinned commit | One-line script: `git show <commit>:<file>` text, whitespace collapsed and `$`, `\` ignored as the register does, contains the fragment |
| R-5 | The commit pinned is recorded | `grep` the commit in D-1; `git cat-file -t` it |
| R-6 | Proposed rows use only the register's fields and values; no id collides with the register | Parse the block with `tomllib`; compare ids and field names with `claims_register.toml` |
| R-7 | Changes to a mathematical statement or a conclusion, and claims in P1/P6 text, are listed as routed, not dispositioned | Inspection: a routed section exists and no routed claim carries a final disposition |
| R-8 | Nothing else changed | `git diff --stat origin/dev` shows only D-1 (and this file's acceptance record) |

## Definition of good

- Extractors miss nothing a reader could rely on; lookups cite the narrowest backing (a step tag, a test id), and "broader than its backing" says exactly how.
- Dispositions keep the prose unchanged where backing exists; drops are few and each is the unbacked detail itself.

## Definition of good enough

- All units extracted and looked up once.
- Every claim has a disposition; routed items are listed for the driver or the owner.
- Proposed rows pass R-4 and R-6 and are ready to land.
- R-1 to R-8 are checked and recorded in this file.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- One extractor per paper section is taken from the second-level headings of the rendered notebook *(default)*.
- Step 1 and step 2 are run by separate agents; step 2 gets one agent per unit with repository access *(default)*.
- A claim the lookup finds backed and unchanged gets "keep" and becomes a proposed row; narrowed or backed claims become rows only after the edit lands, so they are listed, not proposed *(default)*.
- The pass is at one pinned commit; later edits to P1/P6 text are swept by the register test, not re-run here *(default)*.
- The file is in the PM's hands for step 3; the driver is consulted only on routed items *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop.
