# WP11 — Scope of work: readability and correctness loops over the reader grid

| | |
|---|---|
| **Status** | Defined and approved by the driver under the mandate of 2026-11-08 (`release-candidate.md`); for the supervisor's review at the PR. Starts when WP10 is structurally accepted. |
| **Supervisor (accountable)** | mzargham |
| **Records** | `WP11-decisions.md`; the grid and protocol in `docs/superpowers/notes/reader-grid.md`; the driver's calls in `driver-log.md` |

## Purpose

The supervisor: "we'll need to run a grid of user reads (cold) at the depth levels previously
outlined and with differing personas"; "you'll need context gapped user tests and expect them to
give contradictory feedback which you will then needs to triage to get clean, clear, robust
results. it will help prevent metric gaming to reviewers persona or read depth"; "i am a human not
a computer ... if you present the information badly i wont be able to sign off on it".

## Goals

- G1. The paper, the root page and the docsite read correctly and without avoidable friction for
  the six personas at the depths each one reads (the grid's 24 core cells), as far as model readers
  can show it.
- G2. No reader leaves with a belief the answer key lists as wrong.
- G3. The result is robust: a change made for one cell is tested on its neighbours, and a held-out
  set of cells never used while revising confirms it.
- G4. The supervisor receives the whole grid with its worst cells, the changes made and why, and
  what model readers could not tell him.

## Non-goals

- New results, new mathematics, new case material. A finding that needs one goes to the driver.
- The search (WP12). The supervisor's own reading: it follows, at the PR.
- Aesthetic redesign beyond what a finding requires.

## The three roles (they never share context)

Authors (the PM's implementers) see only change requests. Readers are fresh agents given a persona
brief, their depth's slice of the rendered site and a neutral task. The triager is the driver.

## Deliverables

| ID | Deliverable |
|---|---|
| D-1 | **The answer key**, fixed before the first persona read and kept out of the repository until the loops end. Its sha256 is committed before round 1 (`WP11-decisions.md`), so that it can be shown afterwards to have been fixed in advance; the key itself is committed when the loops stop. |
| D-2 | Persona briefs (background, what the reader wants, what they do not know; nothing about the paper), reworded each round; committed after use. |
| D-3 | The depth slices, captured from the rendered site at a named commit in a browser (screenshots and the rendered pages restricted to the slice). |
| D-4 | Round records: every reader report verbatim (`WP11-reads-round-N.md`), the triage (`WP11-triage-round-N.md`), the change requests, the commits that answer them. |
| D-5 | The grid report (`WP11-grid.md`): per cell, the last round's outcome against the key (correct, missing, wrong) and the open friction; the worst cells first; what the held-out cells showed. |
| D-6 | The same loop, smaller, for the docsite with a package user doing tasks (install and first fit; read a tension report; choose K; read a termination record): three task readers per round. |

## Rounds

- **Held out from the start:** six core cells, one per persona, chosen by a seeded draw recorded
  with the key's hash; never read until the end.
- **Round 1:** the other eighteen core cells, one reader each; three edge cells.
- **Triage** by the grid note's rules: classify; a wrong belief or a defect counts at once, friction
  or a missing item counts when seen in two cells; preferences are logged. Contradictions resolve by
  the depth contract, then the recorded intents, then the reader model; what remains goes to the
  supervisor with both readers' words.
- **After a revision:** new readers on the cells that found something, the same depth for the other
  personas, the same persona one depth either side, and a rotating third of the rest.
- **Stop** when two consecutive rounds show no wrong belief in a core cell and no replicated
  friction; then the held-out cells are read once. At most four rounds before the driver reports to
  the supervisor that the loop has not converged, with the grid as it stands.
- Readers are spread over at least two models. Reports carry no ratings.

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The key's hash and the held-out draw are committed before the first read of round 1. | commit order |
| R-2 | No author's brief contains a reader's report, a persona, a depth or the key. | the driver reads the briefs' text |
| R-3 | Every reader report is committed verbatim before its triage. | commit order |
| R-4 | Every change traces to a numbered request in a triage; every request names a passage, a problem and a constraint. | the triage files |
| R-5 | After each revision the paper stays under the word cap as rendered, the proof-map and the suite stay green on this Mac and on CI, and the driver has read the changed pages in a browser. | the driver's verification |
| R-6 | The grid report states the worst cells and what model readers cannot establish. | the report |

## Definition of good enough

The stopping rule is met and the held-out cells show no wrong belief and no new replicated
friction; or four rounds have run and the grid is reported as it stands. R-1 to R-6 hold.

## Agent's defaults

Eighteen plus three reads in round 1; briefs of about 150 words; slices as images for depths A and
B and as the rendered page for C and D; depths E and F in a clean worktree at the commit; the
docsite loop runs alongside round 1.
