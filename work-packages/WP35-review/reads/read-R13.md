# Read R-13 (cold reader, no persona)

Screenshots for this record: commit `2a669de`, `git show 2a669de:<path>` with `<path>` under `work-packages/WP35-review/reads/shots/`.

**Header.** Persona R-13; HEAD 3d5a53e; pages: http://127.0.0.1:8791/paper/ (Section 2) and http://127.0.0.1:8791/paper/supporting-material/ (Appendix H, plus the Appendix G pointer). Viewports: pane default (about 800 wide; not exactly 1280 by 800, the pane would not give that width) and 390 by 844 for Table 1. One sitting. Screenshots: shots/R13-appendixH-top-desktop.jpg, shots/R13-table1-390.jpg (the pane tool returns images only inline; I copied them afterwards).

## Own-words summary (from Section 2 only for Q1 to Q3; Appendix H for the rest)

1. HoroPCA, as described: an unsupervised method, table in and coordinates out, that carries PCA's components into hyperbolic space by horospherical projection, maximizing a variance.
2. This work differs in what it estimates: the one-sided edge of a table (a vector of exponents for a boundary surface), not a variance. It "is not a PCA of any kind".
3. Shared: the setting (unsupervised table to coordinates), the scikit-learn estimator interface, PCA as a downstream step. Parting: the target estimated (edge vs spread). After the appendix: the two also part in solver (non-convex Adam from random starts vs convex program with a gap).
5. Hypothesis: PCA and HoroPCA follow the spread, this work follows the edge. Refuted by any cell outside the bounds of H1 to H4 (e.g. this work below 0.9 recovered in A or B; HoroPCA below 0.9 at rho >= 2 or above 0.1 at rho <= 0.5; PCA above 0.2 at t = 0.9; this work above 0.2 with the edge removed). Result: all 26 checks over 11 cells hold.
6. Does not show: that HoroPCA could never recover boundary information (embedding is ours; R = 3 not tested), anything about noisy, realistic or tree-like data, population recovery rates (six tables per cell), anything about non-default HoroPCA settings or more than one direction.

## Findings

| # | Severity | Place | Quote | What happened | Expected |
|---|---|---|---|---|---|
| 1 | slows a reading | Section 2, HoroPCA paragraph | "In a pre-registered test, on an embedding of ours, the authors' code recovered planted exponents only where they were the direction of largest spread (Appendix H)." | "Pre-registered" sits oddly against Appendix H.1's "a prospectively specified follow-up to an exploratory spike that informed its design". A reader asks which it is. | One word for both places. |
| 2 | slows a reading | Appendix H.1 | "Tables of kind A keep the edge and vary the spread ratio ρ, the spread along the edge's vector over that along the next largest direction. Kind B moves the vector, by t, off the generator's depth direction, and kind C removes the edge." | "generator's depth direction" and "kind C removes the edge" are used with no earlier explanation of the generator or of what "removing the edge" means physically; I took it as "symmetric rows" only on reading H.2. | A half-line on what the generator is. |
| 3 | slows a reading | H.1 | "H1 (A, B): this work recovers the vector in at least 0.9 of the tables; refuted by any cell below." | Fine as a rule, but with six tables per cell "at least 0.9 of the tables" can only mean 6/6 (5/6 = 0.83). I worked that out myself; the text does not say so. | Say "6 of 6". |
| 4 | slows a reading | H.1 vs H.3 | "H2 (A): PCA and HoroPCA, in at least 0.9 at ρ ≥ 2 and at most 0.1 at ρ ≤ 0.5" ; Table row "A, ρ = 1 ... PCA 1/6" | The H2 bounds skip rho = 1 and the table says so in its caption; OK, but "in at least 0.9" has a missing noun ("recover in at least 0.9 of tables"). | Complete the sentence. |
| 5 | slows a reading | H.2 | "HoroPCA needs a ball, so the log-metrics are centred and scaled until the farthest lies at distance R from the centre: nearly flat at R = 0.25, moderately curved at R = 1." | R is never given a plain line ("R" as a radius is inferable). "Ball" is not defined for a reader without hyperbolic background. | One plain line for R and the ball. |
| 6 | slows a reading | H.5 (first use of "frame") | "HoroPCA optimizes a frame, k orthonormal directions, so that points projected along horospheres (the curved counterparts of hyperplanes in flat space) keep the most variance." | "frame" and "horosphere" are defined, but only here at the very end, although HoroPCA's output is discussed from H.1. Not late in the sense of used-before-defined, since neither word is used earlier. | None needed. |
| 7 | polish | H.3 caption | "Source: results.json, readout.md." | Both are links; I could not confirm they resolve (GitHub blob/main, see check 8). The caption does not state the command to regenerate. | A command next to the source. |
| 8 | polish | H.4 | "Appendix D.16 chains them, running PCA on the chart of the near-frontier designs." | "chart" and "near-frontier" unexplained in the appendix; I did not follow. | Pointer is present; fine. |
| 9 | polish | H.5 | "returns a gap bounding the result's distance from the best" | "gap" is not defined in the appendix. | Plain word. |
| 10 | polish | H.3 | "All 26 checks over the 11 cells hold" | I could not reproduce 26 from the table's verdict column. Counting verdict tags: H1 x9 cells, H2 x4, H3 x1, H4 x2 = 16 tags, and those are per-cell, not per-check (checks are per-method inside a cell). The number 26 has no visible derivation on the page. | A one-line count rule. |

## Checks

- C1 (threshold and chance rates before table): **holds.** H.3 opens with "The threshold is |cos| ≥ 0.9, fixed before the run. Chance reaches it with probability 0.037 for a random direction and 0.152 for a random point of the simplex, where this work's exponents live." It precedes Table 1. |cos| is also defined in H.1 ("agreement of directions ignoring sign").
- C2 (causal arm, failure condition stated): **holds.** Kind A varies rho with the edge fixed; H1 to H4 state refutation ("refuted by any cell below"; "refuted by a cell outside either bound"); H.3: "At ρ = 2, removing the edge takes this work from 6 of 6 tables to 0 of 6 and leaves PCA at 6 of 6."
- C3 (plain line at first use): R: **could not tell / partly** (finding 5; "distance R from the centre" only). PC: not used (it says "PCA's component of least variance"). |cos|: holds. span alignment: not used. distortion: not used. frame: only in H.5, defined there. horosphere: defined in H.5 parenthesis. PCA: defined in H.1.
- C4 (sources next to numbers; caption and link that opens): **could not tell.** Caption exists: "Table 1: ... Source: results.json, readout.md." Links point to github.com/.../blob/main/work-packages/WP35-rounds/spike-h/results.json and readout.md; `record` points to blob/830cf54/.../hypothesis.md. My in-page fetch to GitHub was blocked by CORS (not a 404), so I could not confirm they open. The Chami URL returned 200. H.5 sources are named but unlinked inline ("solvers.py; lemma_04_convexity.py", "the authors' repository at commit c9a9996").
- C5 (390 px, no clipping): **holds.** Table width 346 of 366 container, document scrollWidth 390 = viewport; all columns including "HoroPCA, R = 0.25 and 1" visible. Screenshot: shots/R13-table1-390.jpg.
- C6 (register): **holds.** Section 2: "is not a PCA of any kind"; "the closest existing analog in setting ... and the farthest in what is estimated". Appendix H.4: "the methods answer different questions. The methods are complementary". Nearest sentence to a worse-claim: "variance ranking alone does not identify which component represents the boundary" (about PCA's least-variance component, not a deficiency at its own task); and "nothing bounds the result's distance from the best frame" (H.5, a property of the solver, reads mildly adverse but is about guarantees, not quality). I took neither as saying HoroPCA is worse at what it was built for. Nothing calls this work a hyperbolic-geometry method except the title, and Section 2 says "it uses no negative-curvature geometry" (Appendix G). No "PCA with a kernel".
- C7 (reading limits): **holds.** H.4: "(a) The embedding is part of the treatment ... a second embedding was not run, and R = 3 is in the record, not tested. (b) The tables favour clean identification (noise-free, four metrics, a fixed temperature) and are not tree-like ... (c) Six tables per cell establish separation, not population recovery rates; every 6/6 is a count. HoroPCA ran one direction at its default settings." One item not stated as a limit: "30 percent of the rows on the edge" (a share of rows on the boundary) appears in H.2 but not in the limits.
- Q4 whether any sentence implies a kernel method: **holds** (none), Section 2 says "This work builds no kernel" in the table.
- Q8 navigation: Section 2 paragraph carries "(Appendix H)" linking to supporting-material#appendix-h: **holds**, one step. Table to source: caption names results.json, readout.md as links: **could not tell** whether they open. Page errors: none from the page itself; console shows only thebe debug lines; the four error lines were CORS blocks from my own fetch tests on GitHub and doi.org.

## What worked

- "Chance reaches it with probability 0.037 for a random direction and 0.152 for a random point of the simplex" gave me a baseline before the table.
- "At ρ = 2, removing the edge takes this work from 6 of 6 tables to 0 of 6 and leaves PCA at 6 of 6." is the clearest single sentence of the causal arm.
- "every 6/6 is a count" kept me from over-reading the table.
- "A HoroPCA of the chart would be the same kind of chain and was not run." plainly drew a boundary.
- "is not a PCA of any kind" settled what the method is not.

## Not read / not tested

Rest of the paper and Appendix G beyond the pointers; did not follow GitHub links (could not confirm them); did not read the figure, math rendering elsewhere, or the references beyond the two shown; 1280 by 800 desktop screenshot not exactly achieved (pane about 800 wide); no key sought.
