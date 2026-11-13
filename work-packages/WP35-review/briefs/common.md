# Common rules for the Appendix H fresh readers (P9, P10, R-13)

Each brief names this file; the PM pastes it with the brief. Fills by the PM: `{STAGE_URL}` (the staged site's base URL,
no trailing slash), `{HEAD}` (the commit the stage was built from), `{OUT_PATH}` (the file you write), `{SHOT_DIR}`
(the folder for your screenshots). The reader does not guess any of them; if one is still in braces, stop and report it.

## Rules for every reader

- You are a cold reader. Read only the rendered pages named in your brief. Do not open the repository, the notes, the
  tests, the records of earlier readers, the lemma scripts or any answer key, and do not ask for one. If you are told a
  "key" exists, you do not want it; say so and carry on.
- Read in a browser, as rendered. Open your own tab, never use or navigate another; close only your own tab when done.
  Take screenshots (at 1280 by 800, and the Appendix H results table at 390 by 844) into `{SHOT_DIR}` and name the file
  in each finding that depends on what you saw.
- Entry points, under `{STAGE_URL}`: the paper at `/paper/` (Section 2 is the prior-art section; the HoroPCA paragraph
  is in it) and the supporting material at `/paper/supporting-material/` (Appendix H, "HoroPCA beside this work: a
  tested hypothesis"; its sections in order: hypothesis with refutation conditions, design, results, interpretation,
  how the formalism and the solvers differ). Appendix G is read only as far as the pointer from G to H.
- Quote verbatim. Every finding carries the sentence (or the cell text) that prompted it, in quotation marks, and its
  place (page, anchor or heading). A finding with no quote is not a finding. Your own words go beside the quote, not
  in place of it.
- Say what you could not follow, and where you stopped following. Do not repair the text in your head and then report
  that it reads fine.
- A stderr line, a console error, a broken link, a clipped table, math that did not render, a figure that does not say
  what its caption says: each is a finding, with a screenshot.
- Do not change anything. Write one Markdown file at `{OUT_PATH}`; no other file except screenshots.

## Findings format

Write the file in this order.

1. **Header.** Persona, `{HEAD}`, pages read (URLs), viewport(s), time spent in sittings (rough).
2. **Own-words summary**, before anything else is looked at again: what Appendix H claims, in four to six sentences,
   without the page open.
3. **Findings table**, one row each: `#`, severity (blocks a reading / slows a reading / polish), place, verbatim
   quote, what happened to you, what you expected. No fix proposed unless it is one sentence and a plain word swap.
4. **Checks** (the list in your brief), each answered `holds / does not hold / could not tell`, with the quote or
   screenshot that settles it.
5. **What worked**, at most five lines, each quoted. Praise without a quote is dropped.
6. **Not read / not tested**, so the PM knows the limits of your read.

## Reader criticisms carried as checks (RA-10, from the earlier Appendix G passage)

These are the criticisms that took the earlier passage down. Check each on the finished appendix and answer it in your
checks section.

- C1. "Recovered" has a stated threshold: 0.9 on the absolute cosine (|cos|), with the chance rates beside it (0.037 for
  a random direction, 0.152 for a random point of the simplex), defined at first use and before the results table.
- C2. The causal claim is tested, not asserted: the arm that varies the spread with the planted edge held fixed is
  there, and the text says what its result would have had to be for the claim to fail.
- C3. One plain line each, at the point of first use, for: R, PC, |cos|, span alignment, distortion (if used), frame,
  horosphere. Mark any that is missing, late (used before the line), or not plain to you.
- C4. Every number you are asked to rely on has a source or a command next to it, or in the table's caption: the table
  has a caption and a source link that opens.
- C5. At 390 px wide the table's right columns are not clipped (screenshot).
- C6. Register: no sentence says HoroPCA is worse, poorer or inferior at what it was built for; none calls this work a
  PCA of any kind, or HoroPCA "PCA with a kernel". Quote any sentence that comes near.
- C7. The reading limits are stated: the embedding is ours and part of the treatment, the tables are noise-free and
  built (four dimensions, a share of rows on the boundary), six tables per cell so each "6/6" is a count and not a
  rate, default hyperparameters, and HoroPCA at R = 3 is reported and not tested.
