# WP44 readout: a second case study from a public dataset (2026-11-14)

Two passes: `candidates.md` (the hunt, thirteen candidates, several facts unread) and `second-pass.md` (the facts read
from the archives' APIs and the files themselves). Everything below rests on the second pass where the two differ.

## The ranking against the criteria

| Rank | Dataset | Licence (read) | Source (read) | Rows | Configuration | Attributes | Trade-off, citation | Meets |
|---|---|---|---|---|---|---|---|---|
| 1 | Perovskite Database Project, v1.0.1 | CC BY 4.0 (Zenodo record) | doi:10.5281/zenodo.5837035 (version), concept 10.5281/zenodo.5834698; paper doi:10.1038/s41560-021-00941-3 | 42,443 devices, 410 columns | absorber composition, transport layers, deposition route, architecture (design choices) | `JV_default_{Voc,Jsc,FF,PCE}` (40,157 to 41,519 non-empty); `Stabilised_performance_PCE` 3,385; `Stability_PCE_T80` 1,834 | Voc against Jsc under the detailed-balance limit (Shockley and Queisser 1961, doi:10.1063/1.1736034, resolved); efficiency against stability (a citation still to pick) | all six; PCE is the product of the other three over the input power, so it is derived, not traded, as launch cost is in the case |
| 2 | Amniote life-history database (Myhrvold et al. 2015) | CC0 (figshare record) | doi:10.6084/m9.figshare.3563457.v1; paper doi:10.1890/15-0846.1 | 21,322 species, 36 columns, sentinel -999 | class, order, family (categorical; no controllable input) | female maturity (d), litter or clutch size, litters per year, adult body mass (g), maximum longevity (y), gestation (d), birth weight (g), egg mass (g), incubation (d), adult SVL (cm), interbirth interval (y) | the fast-slow continuum: the citation the first pass gave (10.1086/512689) resolves to a paper on orchid bees and is wrong; the right one is to be resolved before use (Bielby et al. 2007 is the usual source) | 1, 2, 4, 5, 6; 3 in the categorical sense only; a complete-case subset must be counted (mass has 4,645 sentinels; other columns far more) |
| 3 | Global leaf photosynthetic traits (Maire et al. 2015, Dryad) | CC0 (Dryad API) | doi:10.5061/dryad.j42m7 | 1,509 species, 288 sites (one xlsx, not read by API) | site climate and soil, species | SLA, Nmass, Pmass, Amass, Narea, Parea, Aarea, gs | the leaf economics spectrum (Wright et al. 2004, doi:10.1038/nature02403, resolved) | 1, 2, 4, 5, 6; 3 as above; the file is readable only by download |
| 4 | ISU-ILCC battery ageing | CC BY 4.0 (figshare record) | doi:10.25380/iastate.22582234.v2 | 238 cells under 63 conditions | charge rate, discharge rate, depth of discharge (controlled stress factors) | capacity fade curves, cycle life; the per-cell attribute set (knee, end-of-life cycle, capacity at fixed cycles) is to be derived from `capacity_fade.zip` (140 KB) | fast charging against cycle life (a citation to pick) | 1, 2, 4, 6; 3 after derivation; 5 to cite; a true designed experiment, the closest in spirit to the cubesat |
| 5 | High-entropy alloys (Gorsse et al. 2018) | CC BY 4.0 (the article; the data are its supplement) | doi:10.1016/j.dib.2018.11.111; corrigendum doi:10.1016/j.dib.2020.106216 | 370 compositions | composition vector, phase, test type | hardness, yield and ultimate strength, elongation (modulus and density partly estimated) | strength against toughness (Ritchie 2011, doi:10.1038/nmat3115, resolved) | 1, 5, 6; 2 weak (a supplement); 4 at risk after complete cases |

Rejected: UCI energy efficiency (simulated), concrete slump (103 rows), auto MPG (one outcome), Rothamsted wheat (two
attributes), Starrydata2 and PanTHERIA and AVONET and GLOPNET (licence unread or absent), CatPred-DB (gated; one
measured attribute per row).

## What each of the two strongest would show that the cubesat does not

**Perovskite devices.** Configurations that are design choices made by thousands of independent groups, not a
sampler: the method on a table nobody designed to be fitted, with missing cells, repeated devices and a derived
attribute (PCE) that the example sets aside as the case sets launch cost aside. The physics gives the expected
n-lemma (Voc against Jsc at fixed band gap), so the fit has an answer to be checked against. Conditioning: all four
JV attributes positive and larger-is-better, no inversion; drop zeros and FF above 1; the stability columns are sparse
and span orders of magnitude, so a stability example is a second, smaller table. Cost to build: a fetch step from
Zenodo at build time (3.3 MB zip; CC BY allows redistribution of the derived table too), a conditioning rule, the fits
at K = 1 and 2, an Examples page; the tension matrix once WP42 lands.

**Amniote life histories.** Natural science with no designer: taxonomy as the categorical configuration and body mass
as the covariate a user must decide to partial out or keep. The fast-slow continuum is the expected n-lemma (longevity
against fecundity, with maturity age and gestation as time costs that the conditioning inverts or not, a choice the
example states because it decides what trades). It lets the docs say where the design-space story stops (no
pull-back to a design; the search does not apply). Cost: a fetch from figshare (6.5 MB zip, CC0), the -999 sentinel,
a complete-case subset whose size must be counted first, the conditioning rule with its orientation choices, the fits,
an Examples page.

## Plain options for the supervisor

1. Build the perovskite example as the second case (engineering design choices, the physics as the known answer) and
   the amniote example as the natural-science one; two Examples pages, one package.
2. Build the perovskite example alone now; the natural-science example after 0.1.
3. Build the amniote and the leaf-trait examples as a natural-science pair (both CC0, both with a named spectrum);
   the perovskite after 0.1.
4. Build the battery example (a designed experiment on three stress factors) with the perovskite; the attribute set
   derived from the capacity-fade curves first.

Each option is a build package scoped from this readout, with the docs page and the fetch-at-build step as its
deliverables and no paper change. Before any citation enters `docs/references.bib`, every DOI above is resolved again
and the two unresolved trade-off citations (fast-slow; charging against cycle life) are found and resolved.

## The two-metric example: Broadbalk wheat (the supervisor's addition, checked 2026-11-14; `wheat-check.md`)

- **The data.** "Broadbalk Wheat annual grain and straw yields 1968-2022", e-RA, doi:10.23637/rbk1-yld6822-01, CC BY
  4.0 ("This dataset is available under a Creative Commons Attribution Licence (4.0)"). Annual, per plot (strip by
  section); grain and straw at 85 percent dry matter; treatments are the fertiliser and manure strips (nil to 288 kg N
  per hectare, farmyard manure), sections continuous wheat or in rotation; cultivars modern short-strawed since 1968,
  named by period. Straw is recorded regularly for Section 1 and the first wheat in rotation since 1980 and only in
  some other section-years, so the two-metric table is the straw-recorded subset, whose row count the build counts
  first. The download is open but behind a form (name, organisation, intended use, "Agree and Download"), so the fetch
  is a manual step done once; CC BY permits committing the derived two-column table with its attribution and licence
  file, which is how the build handles it. Column names and units are in the xlsx, not on the page.
- **The story.** Breeding raised grain while shoot biomass stayed: Austin et al. 1980, Journal of Agricultural Science
  94(3), doi:10.1017/S0021859600028665 (resolved); and on Broadbalk itself, Austin, Ford, Morgan and Yeoman 1993,
  European Journal of Agronomy 2(2), doi:10.1016/S1161-0301(14)80144-5: at equal nitrogen the old and the modern
  cultivar gave similar shoot biomass and the modern one about 52 percent more grain, by its greater harvest index. So
  grain and straw trade along a biomass limit, which is the line the two-metric fit should find, with the nitrogen
  strips moving designs along it and the cultivar periods moving them across it. Shearman et al. 2005 (Crop Science)
  is a third source whose DOI did not resolve through the publisher today.
- **Verdict on the two conditions.** The story is clear and cited; the data are good for the purpose with two stated
  limits (the straw subset; the manual fetch). The example goes into WP45 as its two-metric page, conditional only on
  the subset's row count being counted when the file is in hand.
