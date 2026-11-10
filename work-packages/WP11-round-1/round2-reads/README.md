# WP11 round 2: the eleven reader reports (depths B and C), verbatim

Committed before their triage (R-3). Each file is the reader's report byte for byte, with the
two-line header the harness wrote (cell, model, date; slice commit and prompt file). Nothing was
edited; the hash of each file equals the hash of the file the reader wrote.

## The staged paper

- Commit c6d0fffd4193a26f0ce66eff4185fe92d174f7ad (c6d0fff on `dev`; the paper unchanged since
  6de8f68), built with `uv run python scripts/stage_site.py` and served locally; the page read was
  `/paper/`. The appendices (`/paper/supporting-material/`) were not opened and no reader saw them.
- As rendered: nine figures (Figure 1 to Figure 9), one table (Table 1), Sections 1 to 14 (the
  vocabulary after WP24: "term" for the earlier "facet"; the eight-metric data of record after WP23).

## The slices (captured from the rendered page in the browser, text from the visible DOM)

| File | Bytes | Given to |
|---|---|---|
| `headers.txt` | 483 | depth B |
| `main-results-and-statements.txt` | 10,377 | depth B (the main-results list of Section 1; Definitions 1 to 9, Theorems 1 to 12, Propositions 1 to 3, Lemmas 1 and 2, Corollary 1, each with its hypotheses line; proof sketches and script pointers withheld) |
| `figures-and-captions.txt` | 5,464 | depth B (the captions of Table 1 and Figures 1 to 9; the "Shows / Does not show / Good for" paragraphs are page text and were given at depth C only) |
| `figures/figure-1.png` to `figure-9.png` | 1,968 KB in all | depths B and C (the nine images exactly as served) |
| `main-text.txt` | 71,128 | depth C (title, abstract, Sections 1 to 14; figures marked in place with their captions; appendices withheld) |

The slice files and the scripts that made them (`make_slices.py`, `make_prompts.py`) stay in the
driver's scratchpad with the raw DOM extraction (`raw-page.txt`, 71,212 bytes).

## The prompt shape

One file per reader (`prompts/P{n}-{B|C}.txt`, about 25 KB at depth B and 75 KB at depth C):
the persona brief as "you are ..." (about 150 words, reworded for this round), then the slice, with
each figure introduced by "Open and look at this image now, before reading on: <path>" followed by
its caption, then the neutral task: what this is about, the main result, what you would do next,
what you would tell a colleague, what the method does not do, where you were confused or stopped
(quoting the passage), terms you had to guess, whether you would read on (at B: the whole paper;
at C: the appendices) and why. No ratings. The reader was forbidden every other file, tool and
source, and was not told that it is one cell of a grid, that an answer key exists, or that other
readers exist.

## The cells and the models

| Cell | Model | Report |
|---|---|---|
| P1-B | sonnet | `P1-B.md` |
| P2-B | the session's default model | `P2-B.md` |
| P3-B | sonnet | `P3-B.md` |
| P4-B | the session's default model | `P4-B.md` |
| P5-B | sonnet | `P5-B.md` |
| P6-B | the session's default model | `P6-B.md` |
| P1-C | the session's default model | `P1-C.md` |
| P2-C | sonnet | `P2-C.md` |
| P3-C | sonnet | `P3-C.md` |
| P5-C | the session's default model | `P5-C.md` |
| P6-C | sonnet | `P6-C.md` |

Held out: P4 at depth C (one of the six held-out core cells drawn with the key's hash,
`WP11-decisions.md`); it was not read and stays unread until the loops stop. Of the other five
held-out cells (P1-A, P2-A, P3-D, P5-D, P6-B), four are at depths not in this round; P6-B is in
the draw and was nonetheless read in round 1 and again here. The triage records this for the
driver; the confirmation read at the end needs a fresh reader on a brief wording not used in any
round.

Incidents recorded by the harness: two depth-C readers (P2-C, P3-C) said their first read of the
briefing was truncated and opened Figures 1 to 6 after the surrounding text rather than at the
marker; all nine figures were opened by every reader. No figure failed to render.
