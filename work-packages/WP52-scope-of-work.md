# WP52 — Scope of work: the governance lineage on the history page (research spike, then a proposal)

| | |
|---|---|
| **Status** | Spike approved by his direction of 2026-11-14, 01:50 (`WP52-decisions.md`); the page changes only on his word on the proposal. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; the spike under `work-packages/WP52-rounds/` |
| **Approval record** | His direction, quoted verbatim in `WP52-decisions.md` |
| **Acceptance record** | His word on the proposal, quoted verbatim in `WP52-decisions.md` |

## Purpose

With the governance line now in the root page's motivation, the history page may acknowledge the (self)governance
lineage of this work in at most a paragraph. The spike reads the material first so the paragraph says what the sources
say.

## Goals

- G1. **The material found and read:** computer-aided governance (BlockScience); "why is their data" (his phrase; the
  piece it names found by title or by his files); computer-aided ethnography (BlockScience with RMIT); "Building the
  Loop" with Ellie Rennie; the attention-economy paper for the Ostrom Workshop; computer-aided institutional design
  building on Roth, "The Economist as Engineer". For each: the resolved URL or DOI, authors, venue, date, date read, and
  one paragraph on what it says that bears on this project's line (assessing what is possible and what trades against
  what, and leaving what is preferable to accountable people; a design space rather than a unique optimum; the choice
  among competing alternatives as politics).
- G2. **On his machine:** the same titles under his Documents, Downloads and GitHub folders, listed by path; a file
  that is public is read; a file marked private or draft is listed for him and not read into the proposal.
- G3. **The proposal:** one paragraph at most for the history page, in the page's register ("as thin as we can"), with
  the `history.yaml` entries each link, name and year would need (the record first, the page its view, as WP37 set);
  two candidate placements on the page; the word count before and after.

## Non-goals

- Any edit to `history.yaml`, `site/history.html` or the root page; any claim about a source not read.
- Reframing the project around governance.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP52-rounds/spike/sources.md` | G1 |
| D-2 | `work-packages/WP52-rounds/spike/on-his-machine.md` (paths only for private files) | G2 |
| D-3 | `work-packages/WP52-rounds/spike/proposal.md` (the paragraph, the yaml entries, placements, counts) | G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every source cited with a resolved link and the date read; quotations short and attributed | the driver resolves each link |
| R-2 | No file outside `work-packages/WP52-rounds/` changes | `git diff --stat` |
| R-3 | The paragraph makes no claim a cited source does not carry | the driver reads the paragraph against the sources |

## Definition of good enough

- D-1 to D-3 delivered; R-1 to R-3 pass; he can accept, amend or decline the paragraph from the proposal alone.

## Agent's defaults

- One Sonnet research unit with web access and read access to his home folders; it writes only under the spike folder
  *(default)*.
- "Why is their data" is searched as a title and as a phrase in his files; if nothing is found it is reported as not
  found, not guessed *(default)*.

## Open decisions (for the supervisor)

None; the proposal is the next act.
