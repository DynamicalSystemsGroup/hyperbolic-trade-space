# appendix-d

## Q1. What does this appendix convey?

The full numerical record of the cubesat case and the planted-term checks: how the temperature was chosen, what the one- and three-term fits returned (exponents, contending sets, shares, termination status), how stable those answers are under changed settings and rounding-level jitter, the nondominated counts, the candidate and proposed designs, the PCA reading of the near-frontier chart and the four requirements read after the fit.

## Q2. Which sentence of the story does it serve?

Main-results item 5 (PCA on the near-frontier chart, Appendix D.16), item 6 (the termination status read from the fit's record, D.8), item 7 (the cubesat terms, through the tables behind Section 9: D.3, D.4, D.15), and the Section 1 contribution sentence on the nondominated counts, 126 of 706 on 4 attributes and 659 on 8 (D.9, with their stability in D.11). The abstract's last sentence ("one term blends ... three terms separate the contending sets") is the claim its D.3 tables back in full.

## Q3. Verdict on the appendix as a whole

advances. Section 1 points into this appendix by section number three times (D.16 twice, D.11 once), and the nondominated counts it states are printed only here (D.9); main-results items 5 and 6 rest on D.16 and D.8, and no other unit in the list is described as carrying the case's full tables. Some of its tables are not needed by the story and two overlap each other (see Q7), but the appendix as a whole carries what the main text states briefly.

## Q4. If "repeats"

Not applicable to the appendix as a whole.

## Q7. Tables

- `tab-D-temperature_selection`: pointed to: no. A reader would look for it: yes, for how tau = 38.1 and 45.7 were chosen by the 10 percent target fraction. Verdict: repeats, if Figure 4 (unit fig-tau-sweep) draws the same sweep, as its name suggests; otherwise it carries the selection rule's evidence that no pointer asks for.
- `tab-D-k_diagnostics`: pointed to: no (only the general "tables: Appendix D" of Section 9; D.15 names it). A reader would look for it: yes, for the temperatures, mean slacks and term shares at K = 1, 2, 3 that Section 9 quotes. Verdict: advances (item 7; the mean slack figures quoted in Section 9 are here).
- `tab-D-exponents_and_terms`: pointed to: yes (Section 9: term shares, the near-coincident pair, the Spearman figures). A reader would look for it: yes, for the exponents and contending sets of the one- and three-term fits. Verdict: advances (item 7 and the abstract's last sentence).
- `tab-D-regime_comparison`: pointed to: no. A reader would look for it: yes, for the side-by-side of the two regimes that Section 9 summarizes ("a 5-lemma and a 5-lemma sharing 3 metrics"). Verdict: repeats tab-D-exponents_and_terms in large part (the contending sets, and its Spearman paragraph is word for word the one under D.3); the pair tensions are its own, and may be drawn in Figure 9 (unit fig-regimes).
- `tab-D-sensitivity_variants`: pointed to: yes (Section 5 and Section 8: halving or doubling the target fraction leaves the contending set unchanged). A reader would look for it: yes, for that claim. Verdict: advances (backs the robustness claim the main text makes).
- `tab-D-refits_by_category`: pointed to: no. A reader would look for it: no; nothing in the story or the pointers asks what the fit returns per wheel class. Verdict: does not advance.
- `tab-D-candidate_designs`: pointed to: yes (Section 9, candidates scored against the K = 1 fit). A reader would look for it: yes, for the candidates' log V and rank. Verdict: advances only for Section 9; no sentence of the story needs it, so against the story: does not advance (it belongs as the main text's full version, which is its job).
- `tab-D-termination_records`: pointed to: yes (Section 6, "each returned fit carries the levels it meets"; Section 8, the worked example's record). A reader would look for it: yes, for the termination statuses of item 6. Verdict: advances for item 6 and the planted 3-term record; but its cubesat rows repeat the last six columns of tab-D-k_diagnostics exactly.
- `tab-D-margin_reading`: pointed to: no (Section 6's "about 70 times smaller than the band" points to D.11, while the margin and band it compares are here). A reader would look for it: yes, for that comparison of the certified radius with the band. Verdict: advances (the only place the margin is set against the band and the median score gap).
- `tab-D-nondominated`: pointed to: no by section number (the Section 1 sentence points to D.11 for the stability, not to D.9). A reader would look for it: yes, for the 126 and 659 of 706 in Section 1. Verdict: advances (the contribution sentence's numbers; the main text should point to D.9).
- `tab-D-propose_predict_check`: pointed to: yes (Section 9, proposals predicted then measured). A reader would look for it: yes, for the predicted and measured values. Verdict: does not advance against the story (no Section 1 item names propose-predict-check), though it is the full version of a Section 9 paragraph.
- `tab-D-stability`: pointed to: yes (Section 1, Section 6, Section 8, Section 9). A reader would look for it: yes, for which conclusions and digits hold over five regenerations. Verdict: advances (Section 1's parenthesis on the counts rests on it).
- `tab-D-conditioning_diagnostic`: pointed to: no. A reader would look for it: no; the story claims no uniqueness, and nothing asks for the smallest Hessian eigenvalue per term. Verdict: does not advance (it might back item 2's "uniqueness is not claimed", but nothing says so).
- `tab-D-own_rows_refit`: pointed to: yes (Section 6, the own-rows refit is ill-posed). A reader would look for it: yes, for that observation. Verdict: advances for item 4's several-term fit as Section 6 states it; against the story's sentences it is indirect.
- `tab-D-planted_recovery`: pointed to: yes (Section 8 and Section 9, 16 of 20 recovered). A reader would look for it: yes, for the recovery count and the four failures. Verdict: advances (the only evidence that the fit recovers a known answer, behind item 7's reading of terms).
- `tab-D-mean_slack_fixed`: pointed to: yes (Section 9, mean slack refitted at the K = 1 temperature). A reader would look for it: yes, for that comparison. Verdict: advances (item 7's claim that three terms fit better than one, compared at one temperature).
- `tab-D-pca_chain`: pointed to: yes (Section 1 twice, Section 9). A reader would look for it: yes, for the shares and loadings of the principal directions. Verdict: advances (main-results item 5 is this table).
- `tab-D-requirements_at_the_frontier`: pointed to: yes (Section 8, Section 10). A reader would look for it: yes, for the price of each requirement at the fitted frontier. Verdict: does not advance against the story (no sentence of the abstract or Section 1 mentions requirements), though it is the full version of Section 10's sentence.
- `tab-D-design_sets_comparison`: pointed to: yes (D.17 as a whole, Section 8 and Section 10). A reader would look for it: only partly; the pointers describe pricing and exclusion counts, not three refits. Verdict: does not advance against the story; its second part (baseline, candidates and proposals across three fits) is the widest table here and no sentence asks for it.

## Q9. Read twice and still could not place

- The "all jointly" rows of D.17's first table ("| / 40.8 % | 19 of 56 | | / | / | / | |"): the columns do not line up and the slashes are not explained.
- D.3, term 1: "3 of ten" near-frontier designs; "ten" is not defined anywhere I read.
- D.4 cells such as "settling time, total mass | -0.50 (-0.50)": what the number outside and the number in parentheses each are.
- D.8, the planted-3-term table with a second header row inside it ("Planted terms | Largest exponent deviation after matching terms"): two tables run together.
- D.2's "objective_" against D.15's "mean_slack_": D.15 says they differ at K = 1, but D.2 is described in D.15 and Section 9 as the mean slack.
- D.11: "685 quantities, of which 243 numbers move at all", while the second table lists nine; where the other 234 are printed.
- The n_eff of 23.1 (D.4) against Section 8's "about 25 of the 706 designs" (the pointers file): which one the main text uses.
- References to "gap G-17", "gap G-10", "L12" and "level 2": named, but not resolvable from this appendix.
- D.17's design-sets table, "three terms (share)" column: three cells per row, separated by the same bars as the columns.
