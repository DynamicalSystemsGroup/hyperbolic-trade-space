# WP33 — Scope of work: journeys and signposting (one size fits none)

| | |
|---|---|
| **Status** | DRAFT, for the chief engineer's approval. Approved only by the recorded act below; nothing is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The chief engineer's approval, quoted verbatim in `work-packages/WP33-decisions.md` |
| **Acceptance record** | The chief engineer's acceptance, quoted verbatim in `WP33-decisions.md`, after `WP33-review.md` |

## Purpose

The supervisor's standing order, verbatim (`PM-BRIEF.md`, "One size fits none"): "as we near the end, we need to be very
clear about our wide range of users and their different user journeys and make sure we're not doing the thing were what
offer is "one size fits none" instead the top level index page, the paper, the documentation, the api, the examples, the
package itself, the repo organization all need to be fit for purpose and aligned to a user need. the body of content
needs to be signposted well enough that the user can quickly find what they need, not get lost in content aimed at
another user."

Binding clause, verbatim: "do not bloat the repo to meet this requirement. human (and machine) attention is scarce.
more is not always better, and where does end up being a lot of content assume the user drills down into it naturally
don;t just hit them in the face with a ton of info. they will just bounce off".

So signposting is by subtraction and layering: a first screen is a few lines that route; whom-it-is-for is one
sentence; depth is a link, a fold, an appendix or the repository; every unit is net neutral or negative in words on its
surface; the journeys map is a builders' note. Head: `dev` (WP30 cascade landed; staged site http://127.0.0.1:8791/).

## Goals

- G1. **The journeys are known:** `docs/superpowers/notes/user-journeys.md`, a row per persona (P1 to P8, U1 to U4):
  arrival surface, first need, path, content on the path aimed at another user.
- G2. **Every surface routes in the user's words.** First screen: a few lines (use the tool on your own table; read the
  paper; bring your own system model; check the mathematics; reproduce the results); top: one sentence on whom it is
  for and where the others go. The README's layout list says what each directory is for, truthfully.
- G3. **Content aimed at another user moves to that user's path or goes.**
- G4. **The paths are measured:** a wayfinding read per persona, in steps, repeated on the fixed surfaces.
- G5. **Net neutral or negative in words on every surface touched,** ledger and budgets showing it.
- G6. **The executive's journey (P8)** per the final-read triage (`WP30-rounds/persona-final/triage.md`; P8 F2, F6, F8):
  the executive's first screen routes to the requirements reading (which requirement is dear, what imposing them first
  changes) and states the adoption cost in three lines (designs needed, who writes the conditioning, time to a first
  fit); routing, not a new body paragraph.

## Non-goals

- New pages, banners, landing sections or widgets: a routing line, a link and a cut are the only instruments.
- The journeys map in the site, the paper or `docs.pages`.
- New claims: a unit moves or cuts, and a moved claim keeps its backing (the adoption-cost lines are the one exception,
  Q1).
- Changes under `src/` (bar Q2), `derivation/`, the model, data, numbers, theme, the paper's section order and appendix
  letters. The abstract is the supervisor's hand (P8 F1 stays a review-list question).
- Re-running WP32's cells (their returns are read for steps); style rewrites of user-guide pages.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `user-journeys.md`: twelve rows, each aimed-at-another-user entry cited to file and heading; the placements and cuts it implies | G1 |
| D-2 | One signposting unit per surface: `site/index.html`; `docs/index.md`; the paper's head and Organization paragraph; the tops of `docs/api.md`, `docs/api-reference.md`, `docs/examples.md` and the `examples/adcs/` entry; the `README.md` layout list; the package per Q2 | G2, G5, G6 |
| D-3 | Placements and cuts, each with a one-line reason in `WP33-decisions.md`; ledger and budgets in the same push | G3, G5 |
| D-4 | `WP33-wayfinding.md` and `WP33-wayfinding/`: both rounds, per reader persona, surface, need, steps, bounce points, skips, words verbatim | G4 |
| D-5 | `WP33-review.md` with screenshots of every first screen (`WP33-review/`), light and dark where both exist, one-line reading each; `WP33-decisions.md` | G2, G4, G5 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The map has twelve rows of four fields; each aimed-at-another-user entry names file, heading and that user | `grep -c '^| [PU][1-8] ' user-journeys.md` returns 12 |
| R-2 | Per touched surface the prose word count is not higher than at the start head, the sum is negative; `BUDGETS`, `TOTAL_BUDGET` and the paper ceiling only go down (paper cuts as `[[cut]]` rows, no `words_added`) | `uv run pytest tests/test_site.py::test_word_budgets_hold tests/test_paper.py`; counts per surface in `WP33-review.md` |
| R-3 | First screen at 1280 by 800 and 390 by 844: at most five need-phrases, each a link; no directory listing, section or banner; one whom-it-is-for sentence (not a heading or box) naming where the others go, also atop each hand-written docs page, the paper, the root page and the README | D-5 screenshots; a reader counts lines; grep first lines |
| R-4 | Every top-level directory is in the README list with its job and audience; no stale entry (`docs/` reads "site in WP8") | `ls` against the list |
| R-5 | The paper's Organization paragraph routes by depth (abstract and figure; headers and results; whole text; appendices; repository and container) in no more words than now | rendered paragraph, counts; L-A to L-F readers |
| R-6 | Moved claims keep their backing; links resolve; glossary and Appendix A consistent | `uv run pytest tests/test_claims_register.py tests/test_site.py tests/test_paper.py`; `uv run python scripts/check_vocabulary.py`; docs and paper build |
| R-7 | A pinned name changes only by contract amendment in the same commit, with a change-log row (Q3) | `uv run pytest tests/test_interface_contract.py`; `git diff work-packages/interface-contract.*` |
| R-8 | The executive's first screen (Q4) carries the routing and three adoption-cost lines, each backed per Q1 | screenshot; register row or test per line |
| R-9 | One fresh Sonnet reader per persona, given only the arrival surface's rendered page at a named head and the need in the reader grid's words, reports steps (page opened or link followed), where lost, what skipped, whether a wall of text made it skim; same needs, different readers at baseline and repeat | `WP33-wayfinding.md`: twelve rows per round |
| R-10 | A skim-past is fixed by a cut or placement, never added explanation; at the repeat no persona's steps rose, the total fell, each baseline bounce point is closed or listed; U1 and U3 reach the own-table path without a page presuming SysML v2 or satellites | triage in `WP33-decisions.md`; the two tables compared |
| R-11 | The reviewer looked at every first screen as rendered on the staged site (root page, README, docs Home, paper, API reference, examples, installed package per Q2) at both widths; a stderr line or broken link is a finding | screenshots; `scripts/stage_site.py` |
| R-12 | `uv run pytest -q -m "not slow"` on touched tests (full suite at the gate); whole-repo `uv run ruff check .` and `uv run ruff format --check .`; `uv lock --check`; no AI attribution | the commands; grep of `git log` |

## Definition of good

- A reader of any of the twelve kinds sees in a few lines which door is theirs and is through it in a click or two;
  nothing on the way is addressed to someone else; the repository is smaller than before.
- The surfaces read as one design; the journeys map is short enough to decide where a new sentence belongs.

## Definition of good enough

- D-1 holds twelve rows; D-2's units are in on every surface; D-3 records each cut and placement with its reason.
- R-2 and R-10 hold, both rounds recorded, every first screen screenshotted with a reading; gates pass.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent models by role

Sonnet for implementers, readers, triagers, reviewers and research agents; Haiku for mechanical units (counts, greps,
screenshot runs); nothing larger. Readers get rendered pages only. No sub-agent without the PM.

## Rounds and stopping rule

Baseline at a named head (U1 to U4 from WP32's round 1, eight others from WP33 readers); one unit per surface and
push; the repeat on the fixed surfaces. A second repeat only for a persona whose steps rose or whose bounce point the
surface owes. Stop when R-10 holds or after the second repeat, the rest listed for the chief engineer.

## Agent's defaults

- Recorded 2026-11-11 (`WP33-decisions.md`), restated for approval: a pinned name changes only by amendment; no surface
  adds net words; "the package itself" is the installed import surface; at most two rounds; WP32's U1 to U4 cells
  double as those four readers.
- Word counts by visible text; need-phrases may differ by a word per surface, destinations fixed; glossary terms.

## Open decisions (for the chief engineer)

- **Q1. What backs the three adoption-cost lines?** Options: what is asked of the user, from existing docs, no numbers /
  numbers measured by the U1 and U3 cells (time to a first fit) and a sample-size check on the planted data (designs
  needed), as new register rows / lines pointing to the limits page that state only who writes the conditioning.
- **Q2. The package as a surface.** Options: out of scope, findings go to a later package / docstring top-lines only
  (one sentence, where the docs are), with the contract's docstring pins checked / those plus the `pyproject.toml`
  description and URLs.
- **Q3. May routing remove or merge a page (an amendment)?** Options: no, lines and links only / removal or merge where
  the map shows a page serves no path / removal, merge or rename.
- **Q4. Where does the executive arrive?** Options: the root page / the docs Home / the paper's first screen.

## Blast radius

- Records: `user-journeys.md`, `WP33-*`, `parallel-board.md` rows.
- Surfaces (routing, placement, cuts only): those in D-2, `docs/user-guide/*.md` where the map names a passage,
  `mkdocs.yml` per Q3, `paper/length_ledger.toml`; down-only `tests/test_site.py` budgets; `claims_register.toml`,
  `glossary.yaml`; contract files per R-7.
- Never: `src/` and `pyproject.toml` (bar Q2), `derivation/`, `uv.lock`, data, the model, the `verify` and `stage`
  worktrees, tab-23.

## Lifecycle stages

(1) Research: map, baseline. (2) Decide placements and cuts. (3) Build, a unit per surface. (4) Quality control and the
repeat round. (5) Integrate: amendment, ledger, glossary. (6) Cascade review: first screens screenshotted.
