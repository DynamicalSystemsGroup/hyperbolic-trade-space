# Fifth paper unit: the record defects of waves 8 and 9, each settled from the record before the sentence was edited

Requests 173 to 177 and 182 (H8-2, H8-3, H8-4, H8-5, H8-6, H9-1; 183 joins 173). Claims C801 to C806; length-ledger rows dated
2026-11-14 (three raises, one cut). Figure 6's reads: `paper5-figure6-reads.md`.

**173 (900 rows against 400).** `generate_results.py`: `RECOVERY_ROWS = 400`, seeds 0 to 19, `make_frontier_data(400, 4,
n_terms=3)`; `PLANTED` (C.7's worked example) is 900 rows, no noise, one table. The old sentence printed C.7's size and then
"16 of 20 such tables": the paper was wrong; the 16 of 20 are not on the 900-row table. The sentence now gives only what the
count is on, twenty planted tables of 400 rows, 4 metrics and 3 terms each (sizes from new constants `RECOVERY_METRICS`,
`RECOVERY_TERMS`), and names no 900-row example (a negative edit, 6 words). Section 6's "none of 60 planted terms" now says
60 is three on each of twenty tables of 400 rows (D.13 runs the same seeds at 400 rows).

**176 (D.3's 318 and 119 against 0.7384 and 0.2616).** Computed on the data of record: the count column is the designs within
the K = 1 band 0.0240 of the K = 2 fit (437 = 318 + 119); the share is `term_share_`, the fraction of the designs within the K =
2 fit's own band 0.0088 that a term takes (127 and 45 of 172: 0.73837, 0.26163). Both columns are right; they use two bands and
the table said neither. A generated sentence now follows each per-term table (K = 2, K = 3) naming both bands from the stable
`D k_table` entries. Section 9's 0.74 and 0.26 are the share column, unchanged.

**174 (A11).** `derivation/axioms.py` declares A0 to A11; L19 uses A11 only (row noise independent across rows, N(0, v^2), v^2 =
sigma^2 ||w||^2 under A5, w'Sigma w under A9). Appendix A's table is compiled from the glossary and lists no A codes; the only
list is Section 3's. A11 added to it (29 words). A0 (sizes, structural) is also absent and no lemma ledger cites it as a
hypothesis; left.

**177 (Proof 7's Hessian).** L20.24 gives J_tau's mixed second derivative tau v'C delta; L20.35 gives the ridge derivative at
the shifted point tau v'Sigma w* + tau v'Sigma delta, the second term set aside as second order; the Hessian of (tau/2) w'Sigma w
is tau Sigma (SymPy, run, with L18, L20 `derive` and `verify` passing). So the reader is right: J^R's Hessian is tau (C + Sigma),
tau C is J_tau's, and "its gradient on the face vanishes" is J_tau's at the clean fit. The script and the theorem are right;
the sketch said "its" of J^R. It now says which objective each fact belongs to and where tau Sigma delta is dropped. No script
change (the proof map and ledgers are untouched).

**175 (Figure 6's band).** Definition 4 is `|log V| < 1/tau`, symmetric; the K = 2 levels have 279 designs in (-0.024, 0) and
158 in [0, 0.024); the figure shaded only the lower half, so 158 of the 437 near-frontier designs were drawn outside the band,
and D.3 counts all 437. The figure was wrong. `chart_level.py` now shades both sides and the legend carries the width
(0.0240, from the code); the caption names the band and says it is on both sides. Two fresh Haiku reads (`paper5-figure6-reads.md`):
both read the band as symmetric with its width from the legend. fix4 (a114e1c) also edits this caption cell, `chart_level.py`
(the `axhline` zorder, adjacent to my `axhspan` line) and `fig-chart-level.png`: a textual conflict when the second lands;
resolve by taking both caption edits and regenerating the png from the merged `chart_level.py`.

**182 (Table 2's "all inside the near-frontier band").** The five picks' levels are +0.016, +0.010, -0.012, -0.017, -0.022, all
inside the K = 1 band 0.0240 the shortlist uses (and the sponsor-alone +0.016 is outside the K = 2 band 0.0088); the baseline
row is -0.330. The paper's sentence was true of the picks and false of the table's rows as written. The caption now says "the
levels of the five designs they pick, all inside the near-frontier band that the shortlist uses ... the baseline's level is
outside it". A test pins both from `decision()`.

Not done: request 183's "Section 6.2" half beyond the 60-term clause is covered above; nothing else touched (abstract, site,
docs/index, C693, C694, C167, C168 not edited).
