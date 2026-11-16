# WP71 — Decisions: Broadbalk, the level V against biomass

## His direction (16:09 EST, 2026-11-16, verbatim)

"we have two different scopes now. one is to simply update the broadbalk wheat example so it calls out the
observation that the V levels correlate strongly with biomass which is cool and intuitive but bounded. the other is a
research spike on a variant of our method that can find this pattern which we can test out on the wheat example but
also on public uniswap data (which i am pretty sure i have access to from a github model i made many years ago)"

Earlier the same day (`WP63-decisions.md`): his question on the grain, straw and biomass ternary; "seems like a nice
intuitive example"; "ternary might be the wrong plot for it. maybe this is an opportunity to create another reusable
plot".

## WP71 approved as proxy (16:09 EST)

`WP71-scope-of-work.md` is approved by the driver under his mandate on the direction above: the wheat page calls out,
with a generated number, that the fitted level V tracks biomass across the plot-years and that at a fixed level grain
trades against straw; bounded to that page and its generator. It runs after the level-set figure (`wp63-figure`)
lands, since both edit the page.

## WP71 delivered and landed (17:05 EST)

Landed as b8254d71. The generator (`examples/wheat/derive.py`, `level_biomass_correlation`) writes
`runs.primary.corr_log_v_log_biomass` = 0.99 to `results.json` (K = 1 at the selected temperature 8.27, the
standardized-log conditioning, log V from `score_samples` against log(grain + straw) over 3,753 plot-years); the
unchanged generator reproduced the committed results byte for byte first, and the only diff after is the new key.
The page: in the fit's derived-metric paragraph, "The fitted level V, a weighted geometric mean of the two yields, is
an index of biomass: across the plot-years log V correlates with log biomass at 0.99."; the interpretation opens "At a
fixed level grain trades against straw at the rate the exponents give." The driver moved the number out of the
interpretation into the fit's paragraph, since the examples template keeps new numbers out of part 5 (the unit had
followed the brief and flagged it). Paid for by 44 words cut (the caption's trade clause, now said with the exponents;
a PCA sentence the level sets carry; a repeated orientation; "behind a form"; a re-labelling of the harvest index;
"in Harpenden"); the page at 699 of 700. Register: C1103 added for the number; C907 kept with an elision across the
inserted sentence. The record test reads the correlation from the page (the driver's one-line addition; the WP45
record itself is dated and unchanged). The driver's checks: record and register tests 35 passed; budgets; lint and
format; the fast suite 1,929 passed on the branch; mkdocs. CI dispatched; 8797 restaged. His read decides the
wording; WP72's finding (biomass a size set by year and treatment, not conserved) is his fifth question there and not
on the page.
