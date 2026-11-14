# WP45 test record: Broadbalk wheat, grain and straw (Rothamsted e-RA)

Written to test the method, not to convince; reported whether it passes or not (`WP45-scope-of-work.md`, R-7).

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

## 2. Source, and what was not done

Broadbalk Wheat annual grain and straw yields 1968-2022, Glendining and Poulton (2023), e-RA, doi:10.23637/rbk1-yld6822-01,
CC BY 4.0 ("This dataset is available under a Creative Commons Attribution Licence (4.0)", read from the landing page
2026-11-14 in the WP44 check). The download is open but behind a form (name, organisation, organisation type, country,
intended use, "Agree and Download"). **The file was not fetched**: entering personal data into a form and agreeing to
terms is not something the implementer does, so this record has no fit, no counts and no verdict.

**Status: NOT RUN. Section 1 stands as the only content; nothing in it has been tested.** The scope's wheat checks
(G4) are therefore open, not passed and not failed.

What is ready for the supervisor's one manual step:

1. Fetch the Frictionless zip (CSVs) or the xlsx from the landing page in `examples/wheat/manifest.toml` and put the
   yield CSV under `examples/wheat/data/` (ignored by git). The environment has no `openpyxl`, so the CSV from the
   Frictionless zip is the input.
2. `uv run python examples/wheat/derive.py examples/wheat/data/<file>.csv --list` shows the columns.
3. `uv run python examples/wheat/derive.py examples/wheat/data/<file>.csv --record` writes the size and hashes into the
   manifest (R-1).
4. `uv run python examples/wheat/derive.py examples/wheat/data/<file>.csv --grain <col> --straw <col> --year <col>
   [--plot <col>] [--treatment <col>] [--cultivar <col>]` writes `examples/wheat/derived/grain_straw.csv` with
   `LICENCE-DATA.txt` beside it (both to be committed: CC BY 4.0 allows the derived two-column table with
   attribution), counts the straw-recorded subset and fits `examples/wheat/results.json`.

The script's column handling was written without sight of the file and is covered only by a test on a synthetic frame
(`tests/test_wp45_examples.py`); it fails loudly on a missing column. The cultivar-period reading (grain share against
period) needs the cultivar or a period variable the page does not list; it is to be added when the columns are known.
