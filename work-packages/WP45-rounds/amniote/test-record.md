# WP45 test record: amniote life histories (Myhrvold et al. 2015)

Written to test the method, not to convince; reported whether it passes or not (`WP45-scope-of-work.md`, R-7).

## 1. Expected n-lemma, written from the literature before any fit (2026-11-14)

No fit of this table had been run when this section was committed.

**Metrics (default conditioning):** maximum longevity (years, larger is better), litter or clutch size (number, larger
is better), litters or clutches per year (larger is better), female age at maturity (days, smaller is better, so
inverted: the metric is earliness). Adult body mass is the covariate (decision in 3). No designer exists; taxonomy is the
categorical configuration (class, order, family), and the search story does not apply.

**The named trade-off: the fast-slow continuum.** Species fall on an axis from fast (early maturity, high fecundity,
short life) to slow (late maturity, low fecundity, long life). Bielby et al. 2007, The American Naturalist,
doi:10.1086/516847 (record resolved through Crossref 2026-11-14; title and authors only, full text not read here),
re-evaluates it for mammals.

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

## 2. Source (to be filled when fetched)
