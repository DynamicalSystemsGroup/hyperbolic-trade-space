# Sitting 1: the paper and its appendices

Entry point: http://127.0.0.1:8791/paper/ (the paper); http://127.0.0.1:8791/paper/supporting-material/ (the
appendices). Sources: `paper/paper.ipynb`, `paper/supporting_material.ipynb`. Stage with
`uv run python scripts/stage_site.py --serve --port 8791`.

- [ ] The abstract as rendered (entry surface 3 of 5, and yours to rewrite): your text of 497 words with the closing
  sentence now a list of three thrusts (the search; identifying and filling holes by topological data analysis; formal
  verification and performance), about 506 words against a test bound of 525. Review it against your words in
  `work-packages/WP50-decisions.md` ("After the readout") and `work-packages/WP11-decisions.md` ("The abstract pass").
  Its Pareto sentence stays as written, on your word of the held-out round.
- [ ] The abstract's phrases the readers stopped at (change request 172: "We explain tensions" before the term is
  defined, "soft support", "reversible chart", "GGP" and "kernel", "solved directly", and others). They are your hand;
  the table is the section "Findings of the final reader round routed to the supervisor" in
  `work-packages/supervisor-review-list.md`, with each
  reader's words in `work-packages/WP11-final/triage/`.
- [ ] Section 1's first screen: the sentence that names who the paper is for. The abstract itself names no reader
  (`work-packages/supervisor-review-list.md`, F-1).
- [ ] The tension definition beside elasticity, the sentence on the pick's tension at the end of Section 9, Lemma 21 in
  Appendix B, and Figure 7 as the compact tension matrix. Review against your four answers in
  `work-packages/WP42-decisions.md` and the build record `work-packages/WP42-rounds/build-record/`.
- [ ] Section 9's closing subsection, "What the executives decide", and its table, with Appendix D.19. Accepted by you;
  review against `work-packages/WP39-review.md`.
- [ ] Section 7's paragraph on the way back from the chart to the design space (WP41; landed with the bridge page at af54b3b).
  Review it against your intent as written in `work-packages/WP41-decisions.md` ("The gap", "The method's intent"):
  no new claim, the names of Section 7 held.
- [ ] The future-work paragraph beside the abstract's three thrusts, and what a theorem prover would and would not
  change (`work-packages/WP36-decisions.md`; the WP50 readout's boundary, "fruitful enough to name as a direction, not
  as a result", `work-packages/WP50-rounds/spike/readout.md`).
- [ ] Appendix G.2, the reading pass (entry-surface-grade close read): for each row open the source at the place named
  and say whether the paper reflects it (`paper/reading_pass.yaml`; your words in `work-packages/WP38-decisions.md`,
  "The supervisor, on Appendix G.2"). Rows marked "confirm" and "supervisor" are in `work-packages/release-punch-list.md`.
- [ ] Appendix H (HoroPCA beside this work) against the three boundaries in `work-packages/WP35-review.md`; Appendix E
  and Appendix B typeset at desktop width.
- [ ] Every figure against its caption, and the page for a line of error text, a missing figure or a "Table ??"
  (`docs/superpowers/notes/figure-review.md`; the cold reads of Figures 3, 6 and 7 are in
  `work-packages/WP11-final/figure-review-paperfix3.md`). The record defects the held-out reads found at depth D
  (Section 8's row count, D.3's shares, Proof 7's Hessian, Figure 6's band, Table 2's caption) are fixed in the fifth
  paper unit: check them against `work-packages/WP11-final/paperfix3-record-defects.md`.

Evidence for this sitting: `work-packages/WP10-review.md`, `work-packages/WP35-review.md`,
`work-packages/WP39-review.md`, `work-packages/WP38-review.md`, `work-packages/WP11-final/triage/`.
