# WP45 test record: amniote life histories (Myhrvold et al. 2015)

Written to test the method, not to convince; reported whether it passes or not (`WP45-scope-of-work.md`, R-7).

## 0. This case's row of the coverage matrix (`work-packages/examples-coverage.md`, second table)

| Counts | K, fit | Origin | Stage | Method |
|---|---|---|---|---|
| 36 recorded columns, 11 life-history attributes and body mass; 4 metrics after conditioning (longevity, litter size, litters per year, earliness of maturity), mass the covariate; objectives: none, no decision-maker and no designer | K = 1 and K = 2 tested; tau = 10.7, band 1/tau = 0.093 at 10 percent of rows above the surface; K = 2 fits clearly better (shares 0.66 and 0.34, mean slack 0.345 against 0.412), so the table is not one term | measured | not an engineering lifecycle (natural science) | actual, compiled from the literature |

Known before the fit (from the source, and written into the expected lemma below): origin, stage, method, the column
counts and the four metrics. Completed after the fit: K, tau and the band. This section was added after the fits,
when the coverage record asked for it; the known entries do not depend on the fit, and the committed order (expected
n-lemma before the first fit) is unchanged in `git log`.

**Finding, not adjusted away:** this is a soft fit with a second term worth reading. The band is 0.093, and K = 2
lowers the mean slack by 16 percent with a term holding a third of the species that weights fecundity more and
longevity less (section 4).

## 1. Expected n-lemma, written from the literature before any fit (2026-11-14)

No fit of this table had been run when this section was committed.

**Metrics (default conditioning):** maximum longevity (years, larger is better), litter or clutch size (number, larger
is better), litters or clutches per year (larger is better), female age at maturity (days, smaller is better, so
inverted: the metric is earliness). Adult body mass is the covariate (decision in 3). No designer exists; taxonomy is the
categorical configuration (class, order, family), and the search story does not apply.

**The named trade-off: the fast-slow continuum.** Species fall on an axis from fast (early maturity, high fecundity,
short life) to slow (late maturity, low fecundity, long life). Bielby et al. 2007, The American Naturalist,
doi:10.1086/516847 (record resolved through Crossref 2026-11-14; title and authors only, full text not read here),
re-evaluates it for mammals (by its title).

**Expected n-lemma at tau = infinity, K = 1:** the contending set contains longevity and at least one fecundity metric
(litter size or litters per year), with negative elasticity between longevity and fecundity. Earliness of maturity,
which the continuum puts on the fecundity side of longevity, may join the set; its membership is recorded, not
required.

**Pass:** longevity in the set and at least one of litter size or litters per year in it. **Fail:** otherwise.

**Predictions for the sensitivities (stated now so they can fail):** (a) keeping body mass as a covariate versus
partialling it out of every metric: the contending set keeps longevity and fecundity either way; the exponents move.
(b) Reading maturity as larger-is-better (not inverted): longevity and late maturity align, so the set changes; this
shows the orientation is a choice that decides what trades. (c) Fitting classes apart (mammals, birds, reptiles): the
same pair contends in each class with enough complete cases.

**Stated before the fit, as expected limits of the data:** the complete-case subset (all columns present) is far
smaller than the 21,322 species and is biased toward well-studied taxa; many values are imputed by the compilers'
conventions or estimated from congeners. The table says what is observed together, not what any lineage could have
chosen.

## 2. Source and reproduction

The database is compiled from peer-reviewed studies of individual species and other sources (abstract of doi:10.1890/15-0846R.1, read 2026-11-14). Amniote life-history database, full archive, doi:10.6084/m9.figshare.3563457.v1, CC0 1.0 as read from the figshare
record; paper doi:10.1890/15-0846R.1 (Ecology 96:3109). Archive `ECOL_96_269.zip`, 6,539,535 bytes, md5
`5d78e9ca3494f33ed55ee532c8c01e1c` (equal to figshare's), sha256 in `examples/amniote/manifest.toml`; fetched 2026-11-14,
checked on every run. Table `Data_Files/Amniote_Database_Aug_2015.csv`, sentinel -999. Nothing is committed from the
archive; cache `examples/amniote/data/` (ignored by git), licence note `examples/amniote/LICENCE-DATA.txt`.

`uv run python examples/amniote/run.py` (about 25 seconds) writes `examples/amniote/results.json`; every number below is
from it.

## 3. Counts and the conditioning rule

21,322 species, 36 columns. Present (not -999): maximum longevity 5,500; litter or clutch size 13,078; litters or
clutches per year 4,948; female maturity 3,473; adult body mass 16,677. **Complete cases of the five: 2,770** (Mammalia
1,548, Aves 1,028, Reptilia 194; 59 orders), 13 percent of the table; with gestation as well (mammals only): 1,537.

Rule: -999 read as missing; complete cases, strictly positive; metrics longevity (+1), litter size (+1), litters per year
(+1), earliness of maturity (maturity in days, -1); shift 0; standard scaler of the log. Body mass is the covariate: the
primary table keeps its effect in the metrics ("keep_mass", chosen before the fit as the default conditioning); the
variant partials out the linear effect of log mass from each oriented log metric. Taxonomy is not in the fit; the
per-class variants use it as the categorical configuration.

## 4. The fit and the verdict

Primary table, K = 1; the temperature is chosen so that 10 percent of rows lie above the frontier (bounds 3 to 10^4).

| variant | rows | tau | n | contending set at tau = inf | exponents at tau (longevity, litter size, litters/yr, earliness) |
|---|---|---|---|---|---|
| primary, keep mass | 2,770 | 10.7 | 3 | longevity, litter size, earliness | 0.51, 0.09, 0.04, 0.36 |
| mass partialled out | 2,770 | 8.3 | 4 | all four | 0.48, 0.12, 0.06, 0.33 |
| maturity not inverted | 2,770 | 3.4 | 2 | longevity, litters per year | 0.51, 0.08, 0.39, 0.02 |
| robust scaler | 2,770 | 12.1 | 3 | longevity, litter size, earliness | 0.53, 0.15, 0.00, 0.31 |
| Mammalia | 1,548 | 12.1 | 3 | longevity, litter size, earliness | 0.57, 0.06, 0.04, 0.33 |
| Aves | 1,028 | 5.7 | 4 | all four | 0.43, 0.19, 0.11, 0.27 |
| Reptilia | 194 | 22.1 | 4 | all four | 0.50, 0.07, 0.14, 0.30 |
| Mammalia, mass partialled out | 1,548 | 9.4 | 4 | all four | 0.53, 0.07, 0.07, 0.32 |
| Mammalia, gestation added (5 metrics) | 1,537 | 15.6 | 5 | all five | 0.54, 0.01, 0.07, 0.30 (gestation speed 0.08) |

Near-frontier association of log metrics (Pearson), primary / mass partialled out: longevity-earliness -0.97 / -0.93;
longevity-litters per year -0.66 / -0.60; longevity-litter size -0.06 / -0.17; litters per year-earliness +0.60 /
+0.49. By class (longevity-litter size): Mammalia -0.73, Aves -0.36, Reptilia +0.68.

**Verdict against section 1: pass.** Longevity and litter size are in the contending set in the primary table and in
every variant except the one that reads maturity the other way round, where longevity and litters per year are. The
three pre-stated predictions: (a) mass kept or partialled out, longevity and fecundity stay in the set: held (the set
grows to four); (b) maturity read as larger-is-better changes the set: held (n = 2, longevity with litters per year, and the
longevity-maturity association flips from -0.97 to +0.84), so the orientation is a choice that decides what trades;
(c) the pair contends in each class: held for membership (Reptilia's longevity-litter size association is positive, +0.68,
with 194 rows).

**What the pass does and does not say.**

- Longevity carries about half the weight in every variant (0.43 to 0.57), earliness a third. The strongest
  near-frontier association is longevity against earliness (-0.80 to -0.98), not against fecundity; the fecundity side
  is carried by litters per year (-0.60 to -0.80) and, for mammals, litter size (-0.73), while pooled litter size is
  nearly unrelated to longevity (-0.06). So the membership test passes on litter size, but the evidence for fecundity
  against longevity in the pooled table is litters per year. Both are as the fast-slow continuum has it.
- The set reads as a full-support one in most variants (n = 3 to 5 of 4 to 5 metrics), so as in the perovskite
  record the informative content is the association and the orientation sensitivity, not the count.
- Mass does not explain the longevity-earliness trade: partialling out mass moves that association from -0.97 to -0.93.
- K = 2 (primary): shares 0.66 and 0.34; terms (longevity, litter size, litters per year, earliness) 0.59, 0.04,
  0.00, 0.37 and 0.36, 0.19, 0.11, 0.34; mean slack 0.345 against 0.412 at K = 1; certified. With mass partialled
  out: shares 0.72 and 0.28, mean slack 0.415 against 0.471. The second term puts more weight on fecundity and less on
  longevity; no regime is named from this.
- Temperature: the exponents move little between tau 3 and infinity in the primary table (longevity 0.48 to 0.51,
  earliness 0.34 to 0.40, litter size 0.09 to 0.12, litters per year 0.07 to 0.00).

## 5. Limits

The complete-case subset is 13 percent of the species and is the well-studied end; maximum longevity is a record maximum
that grows with how many individuals were observed, and the compilers' values are in part estimated or taken from related
species (not tested here). No designer exists: there is no configuration to choose, and a point on the frontier is a
species that evolved, not a design anyone could pick, so the pull-back and the search do not apply. Bibliographic
status of the citation relied on: Bielby et al. 2007, doi:10.1086/516847, record resolved (title and authors), text not
read; that it states the fast-slow continuum in these terms is not checked. Not asserted: that the continuum is one axis
(it is written here as a trade-off between longevity and the early, fecund side).

## 6. What this changes for the method

The orientation of a time cost decides the lemma and flips the sign of an association: a page for a user must state
it with its reason. The n-lemma by count is again close to full support; the association and the orientation test carry
the reading.
