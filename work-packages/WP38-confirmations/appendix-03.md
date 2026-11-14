# WP38 confirmation: appendix-03

Rendered view for all rows: the paper's appendices, built site, http://127.0.0.1:8791/paper/supporting-material/ (Appendix B), own tab, read at reading pace, lemma step tables skipped as generated. Head: page as served on the day of the reading; no commit read. Math renders (checked by screenshot at L5 and L7).

| Surface | Reader | Rendered view and head | Reads clean | Remaining flags (kind, sentence) | Cuts that lost something |
|---|---|---|---|---|---|
| `appendix/l5` | appendix-03 | supporting material, Appendix B, L5 block (statement, hypotheses, ledger line) | no | Kind 10: "LSE = LME + (log n)/tau; LSE - max >= 0 (strict for n >= 2); lim_{tau->inf} LME = max; lim_{tau->0} LME = mean; mean <= LME <= max; ..." (and the L5 heading): LSE and LME are never expanded anywhere in the document (the glossary rows say "log-mean-exp", LSE appears nowhere in words) | none found |
| `appendix/l6` | appendix-03 | supporting material, Appendix B, L6 block | no | (1) Kind 7/3: Hypotheses line "A2, A3, A5, I5 (moment generating functions multiply); a population identity, with no consistency claim." repeats the Statement's "not a finite-sample estimator, and no consistency claim". (2) Kind 10: "Population identity under the log-space Gaussian model (A5: eps_j iid N(0, sigma^2), independent across j, sigma > 0): ..." : "iid" is never expanded in the Statement (the step table spells "i.i.d.", and "independent across j" is stated again right after) | none found |
| `appendix/l7` | appendix-03 | supporting material, Appendix B, L7 block | yes | none | none found |
| `appendix/l8` | appendix-03 | supporting material, Appendix B, L8 block | yes | none | none found |
| `appendix/l9` | appendix-03 | supporting material, Appendix B, L9 block | yes | none | none found |

Remaining-flag counts: l5 1, l6 2, l7 0, l8 0, l9 0.
Lost-fact check: no dangling reference or undefined term found beyond the kind 10 rows above; "Helmert-type" (L8) and "F" (L7) are used without a gloss in the block but are glossed in the axiom text and glossary and were left unflagged.
