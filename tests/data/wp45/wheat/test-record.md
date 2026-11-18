# WP45 test record: Broadbalk wheat, grain and straw (Rothamsted e-RA)

Written to test the method, not to convince; reported whether it passes or not (`WP45-scope-of-work.md`, R-7).

## 0. This case's row of the coverage matrix (`work-packages/examples-coverage.md`, second table)

| Counts | K, fit | Origin | Stage | Method |
|---|---|---|---|---|
| 45 recorded columns; 2 metrics (grain, straw); objectives: none, no decision-maker; treatment, cultivar, section and year are the configuration | K = 1 and K = 2 tested; tau = 8.3, band 1/tau = 0.12 at 10 percent of rows above the surface; K = 2 fits better (shares 0.57 and 0.43, mean slack 0.748 against 0.859) and its second term is grain alone | measured | a long-run field experiment (research), 1968 to 2022 | actual |

Known before the fit (from the landing page, and written into the expected lemma below): origin, stage, method, the two
metrics. Completed after the fit: the column count (read from the file), K, tau and the band. The expected n-lemma was
committed (a07c7e6) before the supervisor fetched the file and before any fit; this section was added after.

**Finding, not adjusted away:** a soft fit (band 0.12) whose second term at K = 2 is a grain ceiling with straw free
(section 4).

## 1. Expected n-lemma, written from the literature before any fit (2026-11-14)

No fit of this table had been run when this section was committed.

**Metrics:** grain yield and straw yield (t per hectare at 85 percent dry matter), per plot and year, both larger is
better. Treatments (fertiliser and manure strips) and cultivar period are the configuration. With two metrics the
simplex is a segment, the surface a line in log units, and the n-lemma can only be 1 (one metric binds alone) or 2.

**The named trade-off: the harvest index.** Austin et al. 1980, J. Agric. Sci. 94(3), doi:10.1017/S0021859600028665,
and on Broadbalk itself Austin, Ford, Morgan and Yeoman 1993, Eur. J. Agron. 2(2), doi:10.1016/S1161-0301(14)80144-5
(both records resolved through Crossref 2026-11-14; abstracts read in the WP44 check, full texts not read here): at equal
nitrogen an old and a modern cultivar gave similar shoot biomass, and the modern one gave about 52 percent more grain by
its greater harvest index. Grain and straw therefore share a biomass limit and trade along it.

**Expected n-lemma at tau = infinity, K = 1:** a dilemma, n = 2, with both exponents positive; the fitted frontier is a
line of negative slope in log units. The nitrogen strips move designs along the frontier; the cultivar periods move
them across it (modern cultivars at higher grain share for similar total biomass).

**Pass:** n = 2 at tau = infinity and, near the frontier, a negative association between log grain and log straw.
**Fail:** n = 1, or no negative association. The cultivar-period reading (grain share of total biomass rises across
periods at similar total) is checked separately and reported either way.

**Stated before the fit, as expected limits of the data:** straw is recorded regularly only for Section 1 and the first
wheat in rotation since 1980 (and in some other section-years), so the two-metric table is the straw-recorded subset,
a small slice of the plots; straw is combine-cut straw and includes weed material; the data download is behind a form
and is a manual step.

## 2. Source and reproduction

Broadbalk Wheat annual grain and straw yields 1968-2022, Glendining and Poulton (2023), e-RA, doi:10.23637/rbk1-yld6822-01,
CC BY 4.0 (the landing page, and the package's `datapackage.json`: Creative Commons Attribution 4.0 International). The
download is behind a form; **the supervisor fetched it himself** (2026-11-14) and no agent entered the form. The zip,
`01-YLD6822.zip`, is 2,026,055 bytes, sha256 `6b5957d4fcc19776a52bd21e9d886d3e598d7af6d0e7b88a785e537145b43e43`: the
download of record. The table the script reads is `01-BKyld6822/yield_data.csv` inside it (1,863,995 bytes). Both sets
of hashes are in `examples/wheat/manifest.toml`, and `derive.py` verifies whichever of the two it is given (decision:
the zip stays the download of record and the extracted CSV has its own hashes, so either input is checked). The
cache `examples/wheat/data/` is ignored by git (the rule is in `.gitignore`); the data are not committed. The derived
table `examples/wheat/derived/grain_straw.csv` (3,753 rows, selected columns) is committed with `LICENCE-DATA.txt`
beside it, as CC BY 4.0 allows.

`uv run python examples/wheat/derive.py examples/wheat/data/01-YLD6822.zip` (about a minute) derives the table and
writes `examples/wheat/results.json`; every number below is from it. Grain and straw are at 85 percent dry matter; the
file's field description gives no unit and the fit does not need one (the metrics are standardized logs).

## 3. Counts and the conditioning rule

8,573 plot-years, 45 columns. Grain present (the file marks a missing value `*`): 7,814; straw present: 3,755; both
present and positive: **3,753**, the straw-recorded subset (44 percent of the plot-years), of which 3,640 winter wheat and
113 spring wheat. The file's straw field says straw has been recorded regularly since 1980 for Section 1 and the first
wheat in rotation only, with some other sections in other years; the subset in fact spans all ten sections (Section 1
1,043 rows, no section below 228) and the years 1968 to 2022.

Rule: grain and straw both larger is better (orientation +1), shift 0, standard scaler of the log; rows with either
missing or not positive are dropped.

## 4. The fit and the verdict

Primary table, K = 1; the temperature is chosen so that 10 percent of rows lie above the frontier (bounds 3 to 10^4).

| variant | rows | tau | n | exponents at tau (grain, straw) | grain-straw association, near frontier |
|---|---|---|---|---|---|
| primary (straw-recorded subset) | 3,753 | 8.3 | 2 | 0.45, 0.55 | -0.87 |
| winter wheat only | 3,640 | 8.3 | 2 | 0.45, 0.55 | -0.87 |
| total N at least 96 kg/ha | 2,811 | 6.4 | 2 | 0.51, 0.49 | -0.87 |
| without Cappelle Desprez (modern cultivars) | 2,331 | 10.7 | 2 | 0.60, 0.40 | -0.81 |
| N at least 96, modern | 1,768 | 8.3 | 2 | 0.72, 0.28 | -0.82 |
| Section 1 only | 1,043 | 9.4 | 2 | 0.72, 0.28 | -0.68 |

**Verdict against section 1: pass.** n = 2 with both exponents positive in every variant, and the near-frontier
association between log grain and log straw is negative in every one (-0.68 to -0.87).

**The cultivar-period reading (section 1, checked separately).** At total N of at least 96 kg/ha, median grain over
grain plus straw (the harvest index) and median total (grain plus straw) biomass by cultivar, in order of first year:

| cultivar | years | rows | harvest index | biomass (grain + straw) |
|---|---|---|---|---|
| Cappelle Desprez | 1968-1978 | 1,043 | 0.52 | 8.97 |
| Flanders | 1979-1984 | 236 | 0.61 | 10.44 |
| Brimstone | 1985-1990 | 167 | 0.68 | 10.07 |
| Apollo | 1991-1995 | 139 | 0.67 | 9.79 |
| Hereward | 1996-2012 | 755 | 0.66 | 9.06 |
| Crusoe | 2013-2018 | 221 | 0.67 | 8.89 |
| Mulika | 2015 | 30 | 0.67 | 9.96 |
| Zyatt | 2019-2022 | 161 | 0.76 | 8.75 |
| Tybalt | 2020 | 59 | 0.77 | 7.20 |

The harvest index rises from 0.52 to 0.61 or more with total biomass within about 20 percent of the old cultivar's for
every cultivar except Tybalt (one year, 59 rows, 7.2): held, as the expectation had it (a higher grain share for similar
total biomass). The numbers are medians at a stated N, not a paired comparison at equal N: cultivar is confounded with
decade, weather and the years' husbandry.

**What the pass does and does not say.**

- With d = 2 the n-lemma can only be 1 or 2, and a negative association among two metrics near a frontier is also what
  the closure effect forces, so the pass is weakly informative; the cultivar table is the more specific reading.
- The exponents are stable in temperature in the primary table (grain 0.43 to 0.45 from tau 3 to 100) but not across
  subsets: grain runs 0.45 to 0.72 (a heavy-fertilizer, modern-cultivar subset puts the weight on grain).
- K = 2 (primary): shares 0.57 and 0.43; terms (grain, straw) 0.19, 0.81 and 1.00, 0.00; mean slack 0.748 against
  0.859 at K = 1 (13 percent lower); certified. The second term has the contending set {grain} alone: a ceiling on
  grain with straw free, which K = 1 cannot show. No agronomic reading of it is made here.
- The surface is a line in log units and the simplex a segment, as expected for two metrics.

## 5. Limits

The subset is the straw-recorded plot-years, not the experiment; straw is combine-cut straw without stubble (the field
description) and includes weed material (the landing page). Cultivar, decade and weather are confounded, so the cultivar
table is a description, not a test of breeding. The 1993 paper's "about 52 percent more grain at equal nitrogen" (read
from its repository record in WP44, not from the text) is not reproduced by these medians (grain 4.76 against 6.88 for
Brimstone, 45 percent, at N of at least 96 and not paired). Bibliographic status: Austin et al. 1980,
doi:10.1017/S0021859600028665, abstract read (variety improvement raised the yield potential of winter wheat in the
U.K.); Austin et al. 1993, doi:10.1016/S1161-0301(14)80144-5, record resolved, no abstract and text not read. Not
asserted: that the harvest index is the cause of the frontier's shape.

## 6. What this changes for the method

Two metrics are enough for a clean read but cannot test the lemma count; the informative things are the association,
the K = 2 term and the by-group table. A fit whose second term is a one-metric ceiling is a result the K = 1 page would
not show; a page for a user should say what a monolemma term is.
