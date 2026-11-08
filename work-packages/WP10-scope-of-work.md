# WP10 — Scope of work (SUPERSEDED FIRST DRAFT, written as WP9: Make the notebook and the web page readable for a human)

> Superseded on 2026-11-08 by the supervisor's redirection (see `WP10-decisions.md`, "Redirection" and "The paper's story"). Kept until the paper's scope replaces this file; nothing below is approved.

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. Written at the close of the 2026-11-08 session for pick-up in Claude Code with a browser in the loop. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP9-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP9-decisions.md`, after `work-packages/WP9-review.md` and the supervisor's own reading in a browser |

## Purpose

The WP7 notebook is machine-verified (two reviews, byte-identical re-execution, the fit's report
driving the prose) but the supervisor, reading it rendered in a local MkDocs preview, found it
"really hard to read". His words: "we're definitely going to need to do some loops, but i expect
we'll need to switch to claude code so the browser is in the loop. we can close out todays session
by writing and committing a new scope of work to make the web page and the notebook way better for
a human." This package is that readability work: iterative, with the rendered page on screen in
each loop, changing how the material is presented without changing what it found.

## Goals

- G1. The notebook reads well for its human reader in one sitting: the question first, a picture
  that poses it, short steps, prose that interprets outputs rather than narrating code, and figures
  that carry the argument.
- G2. The rendered web page of the notebook (and the pages it links to) reads well in a browser:
  typography, figure size and legibility, navigation, no walls of output or code.
- G3. The work is done in review loops with the supervisor looking at the rendered page in a browser
  (Claude Code with the browser in the loop), each loop recorded with what changed and why.
- G4. Machine verification is preserved: the fit's numbers, the step-0 gate, the "nothing named
  before the report" guard and the notebook tests remain intact; any re-execution is recorded.

## Non-goals

- No change to the datasets, the estimator, the toolkit, the derivations or the method's claims.
- No new analysis or new results; presentation only (re-ordering, rewriting, re-plotting, hiding
  code, splitting cells, captions, navigation).
- No site deployment, workflow or release (WP8); WP8 adopts whatever page configuration WP9 settles.
- No style for its own sake: every change must make the material easier for a human to follow.
- No pushes to `origin/main` until the supervisor lifts the hold he set on 2026-11-08.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | Revised `examples/adcs/adcs_trade_study.ipynb`, executed, with figures in `examples/adcs/figures/` | G1, G4 |
| D-2 | Rendered-page configuration for the notebook (MkDocs + mkdocs-jupyter settings: code visibility, figure sizing, table rendering, navigation), carried on from the local `preview/site` branch into a form WP8 adopts | G2 |
| D-3 | A reading guide at the top of the notebook (what the reader will learn, how long it takes, where to jump) | G1 |
| D-4 | `work-packages/WP9-loops.md`: one entry per review loop (date, what the supervisor saw, what changed, screenshots or their paths) | G3 |
| D-5 | `tests/test_notebook.py` updated to the revised structure, with the WP7 guards retained | G4 |
| D-6 | `work-packages/WP9-decisions.md` | — |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | A cold reader (a fresh reviewer subagent, and the supervisor) can state the method's claim and the case's finding after the first screen and the hook figure, before any code | reviewer trial, quoted; supervisor's reading in a browser |
| R-2 | Markdown cells are short: median length within the supervisor's reference notebooks (about 300 characters; longest cells under 1200) unless a cell is an explicit reading guide | `tests/test_notebook.py` measures and asserts the budget |
| R-3 | In the rendered page, code is secondary: hidden or collapsed by default with a visible way to show it; outputs that are tables are formatted, with no raw DataFrame dumps longer than 12 rows | inspect the rendered page in the browser; test on the notebook JSON for output lengths |
| R-4 | Every figure has a one-sentence caption that says what to see, placed with the figure; axis labels in attribute terms with units; figures legible at 1280 px width without horizontal scroll | browser check per figure, recorded in the loop log |
| R-5 | The page has navigation that matches the reading order (sections, a table of contents) and the reading guide's jump links work | browser check; link test on the rendered HTML |
| R-6 | The fit's reported numbers are unchanged from the WP7 state, or the notebook was re-executed with the documented command and any change is explained in the loop log | diff of the report cell outputs against the WP7 commit; loop log |
| R-7 | The WP7 guards hold: step-0 gate first, nothing named before the report, the wheel-class statement in the supervisor's words, disclosures and limits present | `tests/test_notebook.py` |
| R-8 | Each review loop ends with the supervisor's verbatim verdict recorded; the package stops when he says it reads well, or at the loop budget in the defaults | `WP9-loops.md` |
| R-9 | Suite, lint, lock and no-attribution checks pass on every local commit | `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, `git log` grep |

## Definition of good

- It reads like the supervisor's own notebooks (ADCS-lifecycle-demo, hc-marimo): an embodied hook,
  small visible steps, interpretation written after the outputs and marked as the author's, one
  visual vocabulary, verification by machine and validation by human made explicit, limits stated
  plainly, and a closing "start wherever suits you".
- A systems engineer new to the method finishes it knowing what the trade space's shape is, which
  tensions the fit found and why, and what the model cannot say.

## Definition of good enough

- D-1 to D-6 exist; R-1 to R-9 pass as checked.
- The supervisor, reading the rendered page in a browser, says it reads well (his verbatim words
  recorded), within the loop budget.
- Non-goals untouched: numbers, data, code paths and claims unchanged except as recorded.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- Loops run in Claude Code with a browser available; the page is served locally with the preview
  configuration (`mkdocs serve` on the `preview/site` branch or an equivalent in the working copy);
  each loop takes screenshots of the sections discussed and files them under
  `work-packages/wp9-screens/` (gitignored if large) *(default)*.
- Loop budget: five loops before the package stops to re-plan *(default)*.
- Code visibility: `mkdocs-jupyter` with code cells collapsed by default and a "show code" toggle;
  if the renderer cannot collapse, code cells are moved after the prose that interprets them and
  tagged for hiding *(default)*.
- Cell budget as in R-2; long interpretation cells split into one-idea cells with a bold lead
  *(default)*.
- Figures: captions as Markdown under each figure; 150 dpi; width sized for the Material content
  column; the visual vocabulary from WP3's plotting module *(default)*.
- Tables: pandas styled or Markdown tables with units in headers; no index columns *(default)*.
- The notebook keeps reading only the cached CSVs; any re-execution uses the WP7 command
  *(default)*.
- Commits prefixed "WP9: ", local only until the hold is lifted *(default)*.

## Open decisions (for the supervisor, to resolve at the first loop)

- **OD1.** Who is the target reader: a systems engineer new to the method, a data scientist new to
  trade studies, or both with two reading paths?
- **OD2.** One artifact or two: the executed notebook rendered as the page, or a separate narrative
  page with the figures and a link to the notebook for those who want the code?
- **OD3.** Default code visibility on the page: hidden, collapsed, or shown?
- **OD4.** WP7's gate: accept WP7 now as the machine-verified baseline (with WP9 as the readability
  pass on top), or hold WP7 until WP9 completes and accept both together?
- **OD5.** Reading length target: a 10-minute read, a 30-minute read, or layered (10-minute path
  plus depth)?
