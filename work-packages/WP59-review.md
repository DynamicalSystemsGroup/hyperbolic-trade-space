# WP59 review (D-4): conditioning and feature engineering on the three public cases

Reviewer run on branch `wp59`, head 94bd95c, in the worktree, every command `uv run --frozen`. The work tree was clean before and after (the three `data/` folders are ignored).

## Requirements

| ID | Command and result | Verdict |
|---|---|---|
| R-1 | Deleted `examples/{perovskite,amniote,wheat}/data` (none present). `python examples/amniote/run.py` fetched with manifest checks, exit 0 (40 s). `python examples/perovskite/run.py` fetched and checked, exit 0 (about 4 min). Copied `/Users/z/Downloads/01-YLD6822.zip` to `examples/wheat/data/`, `python examples/wheat/derive.py examples/wheat/data/01-YLD6822.zip`, exit 0, derived table unchanged. Then each `variants.py` (all exit 0). `git diff --stat` after all three: empty; `git status`: clean. The regenerated `variants.json` files are byte-identical to the committed ones, so no float differs at any precision. `results.json` of the three records also unchanged. | pass |
| R-2 | Primary rows against `WP45-rounds/<case>/test-record.md` section 4 (and the K = 2 lines): perovskite tau 18.8, 0.17/0.41/0.42, Voc-Jsc -0.14, shares 0.976/0.024, slack 0.560/0.594, band 0.053; amniote tau 10.7, 0.51/0.09/0.04/0.36, associations -0.97/-0.66/-0.06, shares 0.66/0.34, slack 0.345/0.412; wheat tau 8.3, 0.45/0.55, -0.87, shares 0.57/0.43. The ladder rows that coincide with record rows also match (perovskite S1, S2, S6; amniote robust, partialled out, not inverted; wheat winter, N at least 96, modern, N 96 modern, Section 1). One rounding difference: amniote band is 0.094 in `amniote.md`, 0.093 in the record (1/10.655 = 0.0938). | pass |
| R-3 | `perovskite.md` (Chains), `wheat.md` (header) and `variants.py` docstrings state: scores centred, exponentiated (perovskite also scaled to unit spread), each component signed so its largest loading is positive. The reading is reported both ways (perovskite: screen loses Jsc, two scores put all weight on the level, stability depends on the number of scores; wheat: a frontier that rewards less of one yield, "not a useful chain"). Note: the wheat rewriting is not scaled to unit spread, the perovskite and variantkit one is; the files say so, the readout does not distinguish. | pass |
| R-4 | `perovskite/run.load`, `amniote/run.load` check the manifest on every load (the reruns fetched and verified). Wheat `variants.py` verifies the archive only if it is in `data/` (the reviewer's run had it: `archive_checked` true) and always checks the derived row count (3,753) and records the derived table's sha256. `.gitignore` lists the three `data/` folders; `git status --short --ignored` shows them as ignored; the diff adds no dataset file (the wheat `derived/grain_straw.csv` and its licence file are WP45's). | pass |
| R-5 | `ruff check` on `variantkit.py` and the three `variants.py`: all checks passed. `ruff format --check`: 4 files already formatted. `uv lock --check`: resolved, ok. `scripts/check_vocabulary.py`: 0 new violations, 57 known (same with the four files copied into `docs/`; the script's coverage of those temporary files is not confirmed). `scripts/check_residuals.py` with the four files copied to `docs/zz59-*.md` (removed afterwards): exit 0; metanarration 0 in all four; hedges 0/0/0/1 (readout 1); intensifiers 0/0/2/3 (wheat 2, readout 3). Readout 1,491 words by `wc -w` (limit 1,500). `git log --format=%B dev..HEAD \| grep -i -E 'co-authored\|generated'`: no match. | pass |
| R-6 | Read as a decision analyst: see Defects 1 to 6. Each choice has what, why and a check (orientation, scaler, extremes, derived, covariate, PCA before the fit); the chain after the fit has no check that says when it matters. | fail (returned on Defects 1 to 4) |

## Sampled numbers (variants.json against the files)

Perovskite (`examples/perovskite/variants.json`): primary tau 18.8, exponents 0.17/0.41/0.42, band 0.053 (ladder.primary); no_scaler FF 0.99, Voc-Jsc +0.29, set Voc,FF; log spread 0.235/0.352/0.682 (log_spread_of_attributes); extremes_capped 0.24/0.75/0.02, Voc-Jsc -0.82, elasticity -3.11, 40,040 rows; pce_added 0.14/0.36/0.00/0.50; quantile tau 29.4, 0.43/0.29/0.28; spread direction Voc 0.76, FF -0.64, 63 percent; chains.device_metrics communality Jsc 0.65, loadings 0.57/0.59/0.57 (62 percent), ICA k3 FF 0.96, Voc 0.98, Jsc 0.95; jv_twelve screen 7 of 12, carried default_Voc,reverse_Jsc; jv_and_stability T80 0.69, end-of-test PCE 0.68, k3 PCA2 exponent 0.00. All agree.

Amniote (`examples/amniote/variants.json`): primary tau 10.7, 0.51/0.09/0.04/0.36, L-E -0.97, slack 0.345/0.412; no_scaler earliness 1.00, tau 3.4, spreads 0.58 (Y) and 1.04 (E); maturity_not_inverted +0.84, set L,Y, earliness 0.02, band 0.294; maturity_not_inverted_quantile +0.76; quantile tau 27.6, 0.41/0.14/0.14/0.30, shares 0.52/0.48; mass_partialled_out 0.48/0.12/0.06/0.33, L-E -0.93; mass_dropped 2,776 rows, largest exponent change 0.01; annual_fecundity_added exponent 0.00; spread first direction 0.68/-0.59/-0.35, and within 0.07 under the four named rows (robust 0.66/-0.65/-0.28 is the largest gap). All agree.

Wheat (`examples/wheat/variants.json`): primary tau 8.3, 0.45/0.55, straw|grain -0.80, association -0.87, shares 0.57/0.43; no_scaler 0.29/0.71, log spread 0.64/0.80; capped 0.44/0.56; modern N 96 0.72/0.28, -2.63; plus_harvest_index set straw,harvest_index, grain 0.00, tau 17.7, -1.16, -0.99; plus_biomass 0.00; year_partialled -0.62, 0.53, trend straw -0.0146 a year, grain 0.0001; pca_before_fit pulled back 0.71/-0.23 and -0.11/0.71, explained 0.84; pca after fit 0.71/-0.71. All agree.

Temperature numbers in the readout's "in common" section (perovskite FF 0.00/0.31/0.42/0.43/0.43 at tau 3, 10, 18.8, 30, inf; amniote longevity 0.48 to 0.51; wheat grain 0.43 to 0.45 between tau 3 and 100) come from the records' temperature sweeps, not `variants.json`. Each confirmed: perovskite `results.json` runs/primary/by_temperature (FF 0.00, 0.31, 0.42, 0.43, 0.43; also record section 4 text), amniote keep_mass by_temperature (0.481 at tau 3 to 0.506, 0.488 at 100 and inf; record: 0.48 to 0.51 from 3 to infinity), wheat primary (0.447 to 0.427 at 100; record: 0.43 to 0.45 from 3 to 100). The readout does not say these come from the records.

## Defects

1. `readout.md` line 17: "With no scaler the metric with the smallest log-spread takes the weight." The data contradict it: in the amniote table earliness takes 1.00 with the largest log-spread (1.04, against 0.58 to 0.95); in wheat the larger-spread straw (0.80) takes 0.71 against grain 0.64 at 0.29. Only the perovskite case (FF, 0.24) fits. State what the data show (the unscaled fit follows the units, one metric dominates) without a spread rule.
2. `readout.md` line 45: "a negative association (-0.62 to -0.99) hold under every scaler, cap, subset and year trend" for wheat. The -0.99 is the straw-index association of the harvest-index row; over the rows named the range is -0.62 to -0.90. Same file, `wheat.md` "Fixed" says "in every row" while the h row's grain-straw association is +0.56 (not shown).
3. `readout.md` line 45: perovskite "FF 0.00 to 0.61" is given for the three-metric rows, but the three-metric minimum is 0.02 (cap); 0.00 comes from the four-metric PCE row. `perovskite.md` "What moved" says "across the scaled rows", which includes that row. Say which rows.
4. `readout.md` line 47 and `readout.md` line 5: the readout says every number is in `variants.json`; the temperature sweep numbers are not (see above). Name the source (the WP45 records, `results.json`).
5. Vocabulary (`glossary.yaml`): the glossary term for the object is "exponent vector" (its entries are exponents); the four files call the same quantity "weight" and "exponent" interchangeably (readout 9 uses of "weight", perovskite.md 5, amniote.md 3, wheat.md 3), and the glossary's "support weights" means something else. "Ceiling" (wheat.md 5, readout 1) is not a glossary term. The elasticity direction is stated two ways: wheat.md "second metric per percent of the first (straw per h)"; the readout says "the elasticity of Jsc against Voc" for the perovskite figure -0.68 to -3.11, which is the entry [Voc, Jsc] (Voc per Jsc; `-w_Jsc/w_Voc`), while the wheat phrasing would call Jsc per Voc the entry [Jsc, Voc].
6. Minor. `readout.md` line 5 area: "changes no other number" (amniote fecundity): exponents, association, band, tau and K = 2 are identical, but the spread loadings move by up to 0.012. `readout.md` the weights-are-not-a-result message appears in the readout three times (common, per-page sections, chain) and again in `perovskite.md` "What moved" and `amniote.md` "What moved". The chain after the fit has no stated check. `wheat/variants.py` docstring says `uv run python` (the others `uv run --frozen`). `amniote.md` "Chaining" last sentence refers to another table's experiment rather than saying the thing.

## Not run

Rendered-page review does not apply (no figures or pages). The vocabulary script's treatment of the temporary files was not independently confirmed.

## Verdict

Returned with the list above. R-1 to R-5 pass (reruns reproduce to the byte, record rows match, checks clean); R-6 fails on Defects 1 to 4 (one claim contradicted by the data, one range misattributed, a range labelled by the wrong rows, a source not stated), plus the vocabulary points in Defect 5. Defect 6 is minor.

## The driver's revisions after this review (2026-11-15)

The four R-6 defects are fixed in `readout.md`: the no-scaler sentence now says one metric takes nearly all the
exponent and which one is an artefact of the raw units (earliness 1.00, FF 0.99, straw 0.71); the wheat association
range is -0.62 to -0.90 over the rows named; FF's range is 0.02 to 0.61 with 0.00 only when PCE is added; the
temperature sweeps are attributed to the WP45 records. Also: "exponent" throughout for the fitted quantity, "ceiling"
replaced by "a second term whose contending set is grain alone", the elasticity written one way ("with respect to"),
the after-fit chain given its check (`spread_loadings` across the ladder), the PCA scores named a change of
representation, and the wheat file's doubled comma. The readout is under 1,500 words. The driver read the readout and
the wheat file in full and sampled the perovskite and amniote files; accepted under the mandate.
