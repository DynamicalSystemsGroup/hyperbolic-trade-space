# Sitting 1: the paper and its appendices

Entry point: http://127.0.0.1:8791/paper/ (the paper); http://127.0.0.1:8791/paper/supporting-material/ (the
appendices). Sources: `paper/paper.ipynb`, `paper/supporting_material.ipynb`. Stage with
`uv run python scripts/stage_site.py --serve --port 8791`. Not opened for this draft.

- [ ] Read the abstract as rendered. It is yours to rewrite before release (`work-packages/deliverables-grid.md`,
  Paper body row). It is also one of the five entry surfaces in the close read.
- [ ] Read Section 1's first screen: the reader line names who the paper is for (review-list item F-1 says the
  abstract itself names no reader).
- [ ] Read Section 9's closing subsection, "What the executives decide", and its table (WP39,
  `work-packages/WP39-review.md`; delivered, acceptance pending).
- [ ] Read the future-work paragraph and its statement of what a theorem prover would and would not change (WP36,
  `work-packages/WP36-decisions.md`).
- [ ] Open Appendix G.2, the table of what the paper took from each source (`paper/reading_pass.yaml`). This is the
  close-read item that no machine judges: for each row, open the source at the place named and say whether the paper
  reflects it. Your own words on it are in `work-packages/WP38-decisions.md` ("The supervisor, on Appendix G.2").
  Rows marked "confirm" and "supervisor" are listed in `work-packages/release-punch-list.md`.
- [ ] Open Appendix H (HoroPCA beside this work): the hypothesis, the refutation conditions, the results and the
  reading limits; the reviewer's three boundaries are in `work-packages/WP35-review.md`.
- [ ] Open Appendix E (gaps) and Appendix B (lemma chain). Look at how the mathematics typesets, at desktop width.
  The residual-pass review says generated lemma statements are the sentences readers still flag
  (`work-packages/WP38-review.md`, "Open items").
- [ ] Look at every figure: does the caption say what the plot shows (`docs/superpowers/notes/figure-review.md`)?
- [ ] Check the page for any line of error text, a missing figure, or a "Table ??"
  (`work-packages/WP38-review.md` records one such check as read at `003f1d2`).
- [ ] Residual-pass sentences still flagged on the paper and appendices are listed in `work-packages/WP38-review.md`
  ("The confirmations", "Open items for the supervisor"); decide whether any blocks release.

Evidence for this sitting: `work-packages/WP10-review.md`, `work-packages/WP35-review.md`,
`work-packages/WP39-review.md`, `work-packages/WP38-review.md`. Final reader round: pending.
