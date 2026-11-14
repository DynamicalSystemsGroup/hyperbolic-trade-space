# WP45 test record: perovskite solar cells (Perovskite Database Project)

Written to test the method, not to convince; reported whether it passes or not (`WP45-scope-of-work.md`, R-7).

## 1. Expected n-lemma, written from the literature before any fit (2026-11-14)

No fit of this table had been run when this section was committed.

**Metrics (the default-scan JV attributes, all larger is better, no inversion):** open-circuit voltage Voc, short-circuit
current density Jsc, fill factor FF. Power conversion efficiency (PCE) is the product of the three over the input
power, so it is derived and set aside, as launch cost is in the cubesat case.

**The named trade-off.** Under the detailed-balance limit (Shockley and Queisser 1961, doi:10.1063/1.1736034, record
resolved through Crossref 2026-11-14; full text not read here) a wider band gap raises the voltage a cell can
deliver and lowers the current it can collect. Voc against Jsc is the dilemma. In that limit FF is a function of Voc
alone (it rises weakly with Voc), so FF rides with Voc and is not an independent third constraint.

**Expected n-lemma at tau = infinity, K = 1:** the contending set contains Voc and Jsc, with a negative elasticity
between them (a gain in one is paid in the other along the frontier). FF is expected outside the set or with a
small exponent; its inclusion would make a trilemma and is not excluded by the literature, only not expected.

**Pass:** Voc and Jsc both in the contending set. **Fail:** either missing from it. FF's membership and the exponents'
values are recorded either way. K = 2 is read the same way, per term (expected: the terms split by band-gap regime or
architecture, not asserted).

**Stated before the fit, as expected limits of the data:** devices are not a sampler (thousands of groups, a
publication bias toward high efficiency), so the frontier is the field's best practice and not a physical bound;
FF has a practical ceiling near 0.85 where many devices cluster.

## 2. Source and reproduction

Perovskite Database Project v1.0.1, doi:10.5281/zenodo.5837035 (concept doi:10.5281/zenodo.5834698), CC BY 4.0 as read
from the Zenodo record; paper doi:10.1038/s41560-021-00941-3. Archive `perovskitedatabase_data-v1.0.1.zip`, 3,317,874
bytes, md5 `1119f05607ebe4bbf46ad7cc3258c6b0` (equal to Zenodo's), sha256 in `examples/perovskite/manifest.toml`; fetched
2026-11-14, checked against the manifest on every run (a changed size or hash stops the script with the file named).
Nothing from the archive is committed; the cache is `examples/perovskite/data/` (ignored by git), the licence text is
`examples/perovskite/LICENCE-DATA.txt`.

`uv run python examples/perovskite/run.py` (about 3 minutes on a loaded machine) writes `examples/perovskite/results.json`;
every number below is from it.

## 3. Counts

42,443 devices, 410 columns. Default scan Voc, Jsc and FF all present: 40,084. All three positive: 40,066. FF at most 1
(the primary table): **40,045**. Dropped by the rule: 2,398 = 2,359 (an attribute missing) + 18 (zero or negative) + 21 (FF above 1). Of the 40,045,
5 rows have Voc above 2 V or Jsc above 40 mA/cm2 (S1 drops them), 295 are module rows (S3) and 2,094 repeat another
row's Voc, Jsc, FF triple (S4).

## 4. The fit and the verdict

Primary table, K = 1, standard log scaler, orientation +1 on all three; the temperature is chosen so that 10 percent of
rows lie above the frontier (`select_temperature`, bounds 3 to 10^4): tau = 18.8, effective supporting rows 36.9.

| variant | rows | tau | n | contending set at tau = inf | exponents at tau (Voc, Jsc, FF) | Voc-Jsc association, near frontier |
|---|---|---|---|---|---|---|
| primary | 40,045 | 18.8 | 3 | Voc, Jsc, FF | 0.17, 0.41, 0.42 | -0.14 |
| S1 caps (Voc at most 2 V, Jsc at most 40) | 40,040 | 25.9 | 3 | Voc, Jsc, FF | 0.24, 0.75, 0.02 | -0.82 |
| S2 robust scaler | 40,045 | 13.7 | 3 | Voc, Jsc, FF | 0.12, 0.27, 0.61 | -0.13 |
| S3 cells only (no modules) | 39,750 | 20.1 | 3 | Voc, Jsc, FF | 0.34, 0.31, 0.35 | -0.65 |
| S4 deduplicated | 37,951 | 18.8 | 3 | Voc, Jsc, FF | 0.17, 0.41, 0.42 | -0.15 |
| S5 band gap 1.5 to 1.7 eV (exploratory) | 27,401 | 20.1 | 3 | Voc, Jsc, FF | 0.39, 0.32, 0.29 | -0.19 |
| S6 PCE added as a fourth metric | 39,980 | 22.8 | 4 | Voc, Jsc, FF, PCE | 0.14, 0.36, 0.00 (FF), 0.50 (PCE) | -0.69 |

**Verdict against section 1: pass.** Voc and Jsc are in the contending set in every variant and the near-frontier
association between log Voc and log Jsc is negative in every one (-0.13 to -0.82), the sign the detailed-balance limit
gives. The reading is a trilemma, n = 3: FF is in the set too, which section 1 had marked as not expected and not
excluded.

**What the pass does and does not say.**

- With d = 3 and 40,000 rows the contending set was the full set in all six three-metric variants, so the pass test
  (Voc and Jsc in the set) could hardly have failed on this table; the informative parts are the sign of the Voc-Jsc
  association and the n = 3 reading, not the membership test. The set is a property of the exact-maximum fit, so it does not
  change with temperature (the tension report solves that LP itself); the sensitivity to temperature is in the
  exponents.
- The exponent values are not stable: Voc runs 0.12 to 0.39, FF 0.02 to 0.61 across S1 to S5, and across temperature at
  fixed rows (primary: at tau 3, 10, 18.8, 30, inf the FF exponent is 0.00, 0.31, 0.42, 0.43, 0.43; the Voc exponent
  0.51, 0.23, 0.17, 0.17, 0.17). Only the set and the association signs are results; the weights are not.
- Which pair is traded is not settled by this fit: the near-frontier association is strongest for Jsc with FF
  (-0.63) in the primary table, with Voc-Jsc at -0.14, while the physics names Voc-Jsc. S1 (cap the extremes) puts it at
  -0.82. The closure effect (the tension report's own note) forces negative association among participating
  metrics, so a negative association alone is read with the exponents and not as proof.
- S5, a narrow band-gap window where the detailed-balance trade-off should weaken (one gap, one point), leaves the
  association at -0.19, not near zero. This was run after the fit, to see; it is exploratory.
- S6: with PCE in the table PCE takes exponent 0.50 and FF falls to 0, and n = 4. PCE is a function of the other three,
  so it absorbs them; this supports setting it aside (the choice made in section 1).
- K = 2 (primary): two terms with shares 0.976 and 0.024; the small term has Jsc exponent 0 and sits on Voc and FF; mean
  slack 0.560 against 0.594 at K = 1; termination status certified. A K = 2 contending set per term is Voc, Jsc, FF for
  both. There is no regime split by band gap or architecture to report.

## 5. Limits

The frontier is the field's published best, not a physical bound: publication favours high efficiency, and a few
thousand papers contribute 40,000 rows. The raw columns have extreme values (Voc up to 4.05 V, Jsc up to 144 mA/cm2, FF up to 5), probably module or
unit entries; the exact maximum is sensitive to them (dropping five rows, S1, moves the exponents by 0.07 to 0.4: Jsc 0.41 to 0.75, FF 0.42 to 0.02). The
default scan is whichever scan the authors called default. Bibliographic status of the one citation relied on: Shockley
and Queisser 1961, doi:10.1063/1.1736034, record resolved, text not read; Jacobsson et al. 2021, doi:10.1038/s41560-021-00941-3,
record resolved. Not asserted: that the dilemma is Voc against Jsc and not Jsc against FF.

## 6. What this changes for the method

(For the supervisor's reading, not for a page.) The exponents of the contending set are not a stable summary on a
table this large and this unstructured; a page built from it should show the set and the association sign and leave
the weights out, or show their range across the conditioning choices. The n-lemma on a three-metric table with
many rows will usually be the full set; the informative test is the association and elasticity, which is what the
tension matrix (WP42) is for.
