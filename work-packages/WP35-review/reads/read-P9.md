# Read P9: mathematical-presentation reviewer (expert), Appendix H and Section 2

## 1. Header

- Persona: P9. HEAD: 3d5a53e.
- Pages: http://127.0.0.1:8791/paper/ (Section 2, Table 1 row and the HoroPCA paragraph) and http://127.0.0.1:8791/paper/supporting-material/ (Appendix G pointer; Appendix H in full, anchors #appendix-h, #sub-h-1 to #sub-h-5).
- Viewports: 1280x800 (shots/P9-h3-results-1280.jpg), 390x844 (shots/P9-h3-table-390.jpg). Console: no errors.
- Time: two sittings (about 25 minutes). Repository links were opened with curl only to check their status; nothing from the repository was read.
- I also checked the two chance rates by simulation outside the repo (d = 4): P(|cos| >= 0.9) is 0.0374 for a uniform random direction and 0.152 for two independent uniform points of the simplex, which match the page.

## 2. Own-words summary (written before re-reading the page)

Appendix H says PCA and HoroPCA follow the spread of a table, this work follows its upper edge, and it tests this on synthetic four-metric tables with 300 rows. Three kinds of table: A varies the spread ratio with the edge vector fixed, B tilts the vector off the generator's depth direction, C removes the edge. A method "recovers" the vector when |cos| with it is at least 0.9. Prior to the run four conditions H1 to H4 were committed; all 11 cells (six tables each) agree with them, so the hypothesis survives: this work gets 6/6 wherever there is an edge, PCA and HoroPCA get 6/6 only when the vector is the largest-spread direction, and with the edge removed this work gets 0/6 while PCA still gets 6/6. Reading limits say the embedding is ours, the data are clean and small, and six tables show separation and not rates. The last section contrasts a non-convex frame objective solved by Adam from random starts with a convex soft-max program with a gap.

## 3. Findings

| # | Severity | Place | Verbatim quote | What happened to me | What I expected |
|---|---|---|---|---|---|
| 1 | slows a reading | H.1, para 1 | "The hypothesis, committed with its refutation conditions before any table existed (record)" and, two sentences earlier, "a prospectively specified follow-up to an exploratory spike that informed its design" | The spike had tables, so "before any table existed" cannot be literally true of the whole history. I could not tell which tables are meant (the ones in the results below, presumably). | "before any table of this experiment existed", or drop the clause |
| 2 | slows a reading | H.1 vs Section 2 | Section 2: "In a pre-registered test"; H.1: "prospectively specified follow-up" | Two registers for one thing; "pre-registered" suggests an external registry, the record link is a commit in the repository. | One term, the weaker (H.1's) |
| 3 | slows a reading | H.1, definition of rho | "the spread ratio ρ, the spread along the edge's vector over that along the next largest direction" | "Spread" is undefined (standard deviation or variance?). For rho < 1 (the vector is among the smallest directions) "next largest direction" is unclear: next below the vector, or the largest of the others? Table rows at 0.25 and 4 depend on this. | A one-clause definition, e.g. ratio of standard deviations, and which direction is the denominator when rho < 1 |
| 4 | slows a reading | H.1, kind B | "Kind B moves the vector, by t, off the generator's depth direction" | "t" and "depth direction" and "generator" are not defined anywhere in the appendix (is t an angle, a mixing weight, a cosine?). "t = 0.9" is the key cell of H3. | The meaning of t in one clause |
| 5 | blocks a reading (for checking H3 and C) | H.1 and H.2, kind C | "kind C removes the edge" and "In C, ρ is 2 or 0.5 and the rows are symmetric" | "Recovers the vector" is defined against "the vector", but with the edge removed there is no edge vector; I assume it is the vector that would have been the edge's, and "symmetric" (about what?) is undefined. H4 depends on both. | Say what the target is in C and what symmetric means |
| 6 | slows a reading | H1 to H4 | "this work recovers the vector in at least 0.9 of the tables"; "at most 0.1 at ρ ≤ 0.5"; "PCA at most 0.2" | With six tables per cell these bounds are counts: at least 0.9 means 6/6, at most 0.1 means 0/6, at most 0.2 means 0 or 1 of 6 (1/6 = 0.167). The fractions hide that H3 would have tolerated 1/6 and H2 would not. | Counts, since the table prints counts |
| 7 | polish | H1 | "refuted by any cell below" | "below" is ambiguous (below the bound, or below on the page). | "refuted by any cell under 0.9" |
| 8 | slows a reading | H2 | "PCA and HoroPCA, in at least 0.9 at ρ ≥ 2 and at most 0.1 at ρ ≤ 0.5" | HoroPCA at which R? H.2 gives two (0.25 and 1), the table prints both, and the count "26 checks" only works if both R values count as separate checks. Not stated in H2. | "HoroPCA at R = 0.25 and at R = 1" in H2 |
| 9 | polish | H.3 | "All 26 checks over the 11 cells hold" | I counted 9 (H1) + 12 (H2: PCA and HoroPCA at two R, over four cells) + 2 (H3) + 3 (H4) = 26. It only reaches 26 if H3's "this work at least 0.9" is counted, but H3 states "refuted by PCA above 0.2" only, and H1 already covers this work at t = 0.9. The count is reproducible but not from the stated refutation clauses. | H3's refutation clause to match what was counted |
| 10 | slows a reading | H.4, boundary-orientation claim | "the leading directions of PCA and HoroPCA track the variation in the sampled designs" | The table only prints |cos| with the planted vector. Nothing printed shows HoroPCA's direction agreeing with the direction of largest variance (for example its |cos| with PCA's first direction); this is an inference from 6/6 coinciding with large rho. | Narrow to "recover the vector only when it is the direction of largest spread, in these cells" or print the agreement |
| 11 | slows a reading | Section 2 | "the authors’ code recovered planted exponents only where they were the direction of largest spread" | Whether B, t = 0 (HoroPCA 6/6) is a "direction of largest spread" cell is not stated anywhere in H, so "only where" cannot be checked from the page. Also "planted exponents" vs H's "vector" (two words for one object). | Name the cells where the vector is the largest-spread direction (A with rho >= 2, B t = 0?) |
| 12 | slows a reading | Appendix G, HoroPCA row | "on the paper's tables its exponents are recovered by neither HoroPCA nor PCA except where the generator made them the direction of largest spread (Appendix H, and the earlier spike's record)" | Overreach (P9-b): H tests synthetic four-metric tables built for the purpose, not "the paper's tables" (the case study's table was not run). H.4 also reports PCA's least-variance component recovering the vector in 5/6 cells, which this sentence's "neither ... nor PCA" does not leave room for (it is the first component that is meant, but the sentence does not say). | "on the synthetic tables of Appendix H, the first components of PCA and HoroPCA ..." |
| 13 | slows a reading | H.5 | "returns a gap bounding the result’s distance from the best" and "nothing bounds the result’s distance from the best frame" | "Distance" is in objective value for a convex program with a duality gap; it is not distance in the parameter (frame or exponent vector) in general. The word is used for both methods and means something different from the geometry used in the experiment (|cos|). | "bounding the objective's shortfall from the best value" |
| 14 | slows a reading | H.5 | "which for one term is convex, by a linear program or sequential quadratic programming" | A log-mean-exp objective is not a linear program; which problem is solved by LP and which by SQP is not said (smoothing vs hard max?). Unreadable as a claim about the method. | Say which objective each solver takes, or drop "linear program" |
| 15 | slows a reading | H.5 | "That objective is not convex: the authors’ code runs Adam from random starts" | A claim about HoroPCA's published method (non-convexity of the explained-variance objective over frames) and a claim about its code (Adam, random starts) are in one sentence with one source line; no lemma is cited for the non-convexity (only lemma_04_convexity.py, which per its name is this work's). I could not tell which source backs which. | Sources split by claim, or the non-convexity stated as "not known to be convex" |
| 16 | slows a reading | H.5 (and H.1) | "optimizes a frame, k orthonormal directions, so that points projected along horospheres ... keep the most variance" | Busemann function is never named; what is a "direction" (ideal point) and the base point of the projection are not mentioned. As a statement of the published method it is a gloss, defensible, but it is not an estimand (what parameter space, what criterion): PCA's and this work's estimands are given in words only in H.1 ("the directions along which a table spreads most", "a vector of exponents defining a surface that bounds the rows from above") and the criterion for this work arrives only in H.5, after the results. | The three estimands, in one place before H.2 |
| 17 | slows a reading | H.2 | "HoroPCA needs a ball, so the log-metrics are centred and scaled until the farthest lies at distance R from the centre" | The "map into the ball" is called our choice in limit (a) but is not given (exponential map at the centre? radial rescale?). |cos| of a HoroPCA direction in the ball is compared with a vector in log-metric space; that this is the same direction under the map is assumed. Also: is the vector compared after centring? | Name the map |
| 18 | polish | H.4 | "though an analyst with other domain information might choose it" | Speculative addition to the least-variance sentence; not backed by the experiment. | Drop (padding) |
| 19 | slows a reading | H.4 / H.3 caption | "PCA's component of least variance recovers the vector in 5 of 6 tables at ρ = 0.25 and at t = 0.9, and in none of the other nine cells" | The count is not in the printed table (which has the first component only) and the source links in the caption (results.json, readout.md) return 404 on blob/main, so I could not check whether they hold it. "The other nine cells" includes C, where the target vector is the one discussed in finding 5. | The count in the table's source, with a working link |
| 20 | slows a reading | Caption links, H.3 | "Source: results.json, readout.md." | Both links point at github.com/.../blob/main/work-packages/WP35-rounds/spike-h/ and return 404 (curl). The hypothesis link at commit 830cf54 returns 200. | Links that open (hash-pinned like the record link) |
| 21 | polish | H.3 vs Section 2 | Section 2 Table 1 and Appendix H "Table 1:" | Two tables numbered 1 on different pages. | Distinct numbers |
| 22 | polish | H.2 | "five restarts" and H.4 "HoroPCA ran one direction at its default settings" | "default" but five restarts is said to be a design choice? Not clear whether five is the code's default. | One sentence |

## 4. Checks

**C1 (threshold and chance rates before the table): holds.** "A method recovers the vector when the absolute cosine (|cos| ...) of its direction with it reaches the threshold below." (H.1); "The threshold is |cos| ≥ 0.9, fixed before the run. Chance reaches it with probability 0.037 for a random direction and 0.152 for a random point of the simplex" (H.3, before the table). I reproduced both rates by simulation at d = 4. Caveat: the 0.9 appears in H1 before it is stated in words, and the rates assume the planted vector is also uniform on the simplex (not stated).

**C2 (causal claim tested; failure conditions stated): holds.** Arm A "keep[s] the edge and vary[ies] the spread ratio ρ"; H2: "refuted by a cell outside either bound"; H4 "refuted by either failing". The row "At ρ = 2, removing the edge takes this work from 6 of 6 tables to 0 of 6 and leaves PCA at 6 of 6." Conditions precede results (committed before the run per the record link; I opened that link only to check status, 200). Findings 3, 5, 6 apply: the conditions are testable but ρ, C's target and fractions-as-counts are under-specified.

**C3 (plain lines at first use): partly.** R: used in H.2 with "at distance R from the centre", plain enough. |cos|: defined in H.1. Frame: "k orthonormal directions" at first use in H.5 (but "frames" already in Section 2's table and paragraph). Horosphere: "(the curved counterparts of hyperplanes in flat space)", late but at H.5's first use of the noun here. PC, span alignment, distortion: not used in H. Missing or not plain: t, depth direction, generator, spread, "tree-like", "temperature", "one term", "symmetric" (findings 3 to 5). Verdict: does not hold completely.

**C4 (sources next to numbers): does not hold.** The caption has a source line but both links return 404: "Source: results.json, readout.md." (finding 20).

**C5 (390 px, right columns not clipped): holds.** shots/P9-h3-table-390.jpg: all five columns, including "HoroPCA, R = 0.25 and 1", visible; document width 390, table 346.

**C6 (register): holds.** I find no sentence saying HoroPCA is worse or poorer at its task or calling this work a PCA. Nearest: "is not a PCA of any kind" (Section 2, about this work, fine) and "the methods answer different questions". The nearest misreading risk is "not tree-like, the data HoroPCA was built for" (H.4) which is fair. Section 2's table row labels it "HoroPCA (PCA in hyperbolic space)", which the paragraph then qualifies.

**C7 (reading limits): holds with one gap.** (a) "The embedding is part of the treatment: the centre, the scale R and the map into the ball are our choices"; (b) "noise-free, four metrics, a fixed temperature ... not tree-like ... a mechanism demonstration"; (c) "Six tables per cell establish separation, not population recovery rates; every 6/6 is a count". "A share of rows on the boundary" (30 percent) is in H.2 and not in limit (b); default hyperparameters is a bare sentence at the end; "R = 3 is in the record, not tested" says "in the record" without saying where (the repository) or what it showed. Stated once each, plainly: yes, except the last two.

**P9-a (counts, chance rates, threshold equal the table's): holds, with one gap.** Threshold 0.9 appears in H1 to H3 and in H.3; chance rates 0.037 and 0.152 equal my simulation; "6/6 ... 0/6" statements in the prose equal the table (A rho = 2 row not quoted but C rho = 2: 0/6 and 6/6 match). The count "5 of 6 ... in none of the other nine" cannot be checked from the table or the 404 sources (could not tell).

**P9-b (no sentence says more than the experiment shows): does not hold.** Findings 10 and 12 (and 11): "track the variation in the sampled designs" and "on the paper's tables". The rest of H.4 and the limits are narrow.

**Q4, recomputed verdicts (all agree with the printed cells and the stated rule):**
- A, ρ = 0.5 "survives (H1, H2)": this work 6/6 meets H1's 0.9; PCA 0/6, HoroPCA 0/6, 0/6 are at most 0.1 (H2). Agrees.
- A, ρ = 2 "survives (H1, H2)": 6/6, and PCA 6/6, HoroPCA 6/6 and 6/6 are at least 0.9. Agrees.
- B, t = 0.9 "survives (H1, H3)": this work 6/6; PCA 0/6 is at most 0.2. Agrees.
- C, ρ = 2 "survives (H4)": this work 0/6 at most 0.2, PCA 6/6 at least 0.9. Agrees. (A, ρ = 1: PCA 1/6 is untested by design, correctly labelled H1 only.)
- Tally 26: reproduced only as in finding 9.

**Q1 (what each method estimates, in my words, and silence):** This work: a vector of exponents on the simplex, the minimiser of a log-mean-exp (soft max) of weighted log-metrics, which is stated only in H.5, after the results. PCA: unit directions maximizing variance; given in words only ("the directions along which a table spreads most"). HoroPCA: a frame of orthonormal directions maximizing the variance kept by horospherical projections; "Busemann" and base point not mentioned; "variance" for a frame is not defined (Fréchet-type?). Finding 16.

**Q3 (design):** A fixes the edge, varies spread (controls the edge; does not control the embedding, or sample size effects). B moves the planted vector off the depth axis at fixed spread (controls the orientation of the edge relative to the generator's axes; whether "depth direction" is the largest-spread direction is not stated). C removes the edge at fixed spread (controls the presence of the edge; it does not control for rows lying near any other structure). The three arms separate spread from edge; none varies noise, dimension or the embedding.

**Q5 (formalism account):** see findings 13 to 16. Claims about HoroPCA's published method: frame, horospherical projections, variance. About its code: Adam, random starts, five restarts, commit c9a9996 (I did not open it). About this work: convexity for one term, LP or SQP, gap.

**Q6 (three boundaries):** each stated once in H.4's reading limits. Elsewhere "complementary" (H.4) and the G sentence in finding 12 claim more.

**Q7 (smallest-variance component):** stated defensibly ("It is outside the hypothesis: variance ranking alone does not identify which component represents the boundary"), but the count is not in the table, and its source link 404s (finding 19, could not tell). Finding 18 (padding) concerns its last clause.

### Where each precision request could go without cost to a novice (R-14)

- 3, 4, 5, 8, 17: the H.2 design paragraph or the reading limits (one clause each); novices skip it.
- 6, 9: the table caption (counts instead of fractions).
- 13, 14, 15, 16: nowhere in the body; narrow the H.5 sentences ("bound on the objective", drop "linear program").
- 10, 11, 12: nowhere, the sentences should be narrowed or backed.
- 1, 2, 7, 21, 22: word swaps, no cost.
- 19, 20: the source link and the source file.
- Padding I would remove: finding 18 ("though an analyst with other domain information might choose it").

## 5. What worked

- "At ρ = 2, removing the edge takes this work from 6 of 6 tables to 0 of 6 and leaves PCA at 6 of 6." The single sentence that carries the causal arm.
- "Chance reaches it with probability 0.037 for a random direction and 0.152 for a random point of the simplex, where this work's exponents live." Checks out by simulation.
- "Six tables per cell establish separation, not population recovery rates; every 6/6 is a count." Plain and sufficient.
- "variance ranking alone does not identify which component represents the boundary" is narrow and defensible.
- The table at 390 px is readable and unclipped.

## 6. Not read / not tested

- Not read: anything outside the two pages above (not the repository, notes, lemma scripts, records or any key). The links "record" (hash-pinned), results.json and readout.md were only status-checked with curl, not read.
- Not tested: whether the tables' numbers are right, only that the printed cells are consistent with the stated rule and the stated rates (rates by my own simulation). I did not run the authors' HoroPCA code, so the account in H.5 is judged against what I recall of the published paper, not checked against it.
- The screenshot at 1280 is the results table (shots/P9-h3-results-1280.jpg); I did not capture H.1, H.4 or H.5 as images.
