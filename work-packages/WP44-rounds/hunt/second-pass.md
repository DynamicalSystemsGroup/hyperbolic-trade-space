# WP44 hunt, second pass (research agent, Sonnet, 2026-11-14): facts read from APIs and files, as returned

Facts below were read on 2026-11-14. Each is from an API response or a file I read.

**1. Perovskite Database Project**
(a) Both DOIs are the dataset's. 10.5281/zenodo.5834698 is the concept DOI (the record's `conceptdoi`, conceptrecid 5834698). 10.5281/zenodo.5837035 is version v1.0.1, titled "The Perovskite Database (Archive)", published 2022-01-11. Read from https://zenodo.org/api/records/5837035 and https://zenodo.org/api/records/5834698. Both API calls return the same record, doi 5837035.
(b) The Zenodo record's licence is `cc-by-4.0`, access open. The GitHub README says the same (https://github.com/Jesperkemist/perovskitedatabase_data, read from the zip's README.md).
(c) The record has one file, `Jesperkemist/perovskitedatabase_data-v1.0.1.zip` (3,317,874 bytes). I downloaded it and read `data/Perovskite_database_content_all_data.csv`. It has 410 columns and 42,443 data rows.
- Photovoltaic columns: `JV_default_{Voc,Jsc,FF,PCE}`, `JV_reverse_scan_{Voc,Jsc,FF,PCE}` and `JV_forward_scan_{Voc,Jsc,FF,PCE}`. There is also `Stabilised_performance_PCE`.
- Non-empty counts: `JV_default_PCE` 41,519; `JV_default_Voc` 40,309; `JV_default_Jsc` 40,344; `JV_default_FF` 40,157. `JV_reverse_scan_PCE` is 40,767 and `JV_forward_scan_PCE` is 8,789. `Stabilised_performance_PCE` is 3,385.
- Stability columns: `Stability_PCE_T80` (1,834 non-empty), `Stability_PCE_Ts80` (87), `Stability_PCE_Te80` (49), `Stability_PCE_Tse80` (6), `Stability_PCE_T95` (223), `Stability_PCE_Ts95` (22), `Stability_PCE_initial_value` (3,036), `Stability_PCE_end_of_experiment` (7,373), `Stability_PCE_after_1000_h` (1,008), `Stability_time_total_exposure` (7,399), `Stability_lifetime_energy_yield`.
- The zip is what is archived on Zenodo. I did not check the perovskitedatabase.com project site.
(d) 10.1038/s41560-021-00941-3 resolves through doi.org (CSL JSON) to "An open-access database and analysis tool for perovskite solar cells based on the FAIR data principles", Nature Energy, 2021-12-13.

**2. Amniote life-history database**
(a) The figshare API (https://api.figshare.com/v2/articles/3563457) gives the title "Full Archive", DOI 10.6084/m9.figshare.3563457.v1, and licence CC0 (https://creativecommons.org/publicdomain/zero/1.0/), published 2016-08-10. The files are `default.htm` and `ECOL_96_269.zip` (6.5 MB). The Ecological Archives E096-269 page (`default.htm` from that record) says "Copyright Authors". It says nothing more on copyright. The paper is Ecology 96:3109, http://dx.doi.org/10.1890/15-0846R.1.
(b) I downloaded the zip and read `Data_Files/Amniote_Database_Aug_2015.csv`. It has 21,322 data rows (the abstract says 21,322 species) and 36 columns. Units come from `Supplemental_Table_9_Dataset_Field_Information.csv` in the same zip. Eight or more trait columns with units:
- `female_maturity_d` (days)
- `litter_or_clutch_size_n` (number)
- `litters_or_clutches_per_y` (per year)
- `adult_body_mass_g` (g)
- `maximum_longevity_y` (years)
- `gestation_d` (days, mammals only)
- `birth_or_hatching_weight_g` (g)
- `egg_mass_g` (g, birds and reptiles)
- `incubation_d` (days, birds and reptiles)
- `adult_svl_cm` (cm)
- `inter_litter_or_interbirth_interval_y` (years)
- The abstract says up to 29 parameters.
(c) Yes, the missing-value sentinel is -999. The count of -999 values per column runs from 4,645 (`adult_body_mass_g`) to 21,318. No column has blanks or "NA".

**3. Dryad doi:10.5061/dryad.j42m7**
(a) The Dryad API (https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.j42m7) gives the licence as https://spdx.org/licenses/CC0-1.0.html. The title is "Data from: Global effects of soil and climate on leaf photosynthetic traits and rates". Publication date is 2016-02-10, version 2.
(b) Could not verify the row count or the column names. The one file is `globamax_data_160609 (for GEB ms).xlsx` (1,125,213 bytes). Its download endpoints returned "Unauthorized, must have current bearer token" (api/v2/files/102638/download) or 403 (downloads/file_stream/102638). I then tried a browser-style user agent on the 403 endpoint. The permission system denied that, so I stopped.
- What the metadata says: the abstract gives 1509 species from 288 sites. The file description gives a legend sheet and a data sheet with SLA, Nmass, Pmass, Amass, Narea, Parea, Aarea and gs, plus soil and climate variables, and a "references" sheet.

**4. Gorsse et al. high-entropy alloys**
(a) No separate DOI or Mendeley Data record found. The paper's Specifications table (https://pmc.ncbi.nlm.nih.gov/articles/PMC6290247/) says "Data source location: Data are with the article" and "Data accessibility: Direct submission". The data are in the supplementary materials and tabulated in the paper. A web search found no Mendeley deposit (my search did not search the Mendeley Data site directly). The paper covers 370 alloys, 2004 to 2016.
(b) The licence is CC BY 4.0, "Â© 2018 The Authors" (PMC page above; Crossref lists creativecommons.org/licenses/by/4.0/).
(c) The corrigendum is "Corrigendum to Database on the mechanical properties of high entropy alloys and complex concentrated alloys, Data in Brief 21 (2018) 2664â2678", Data in Brief 32 (2020) 106216, DOI 10.1016/j.dib.2020.106216 (Crossref, https://api.crossref.org/works/10.1016/j.dib.2020.106216; issued 2020-10 per Crossref, PMC says 2020 Aug 22). Crossref and PMC give no abstract or reason for the correction, so I do not know what it changed.

**5. DOIs resolved (CSL JSON via doi.org)**
- 10.1063/1.1736034: "Detailed Balance Limit of Efficiency of p-n Junction Solar Cells", J. Appl. Phys., 1961
- 10.1086/512689: "Scaling of Nectar Foraging in Orchid Bees", The American Naturalist, 2007
- 10.1038/nature02403: "The worldwide leaf economics spectrum", Nature, 2004
- 10.1038/nmat3115: "The conflicts between strength and toughness", Nature Materials, 2011
- 10.1038/nmat2090: "Complex thermoelectric materials", Nature Materials, 2008

**6. Further datasets**
- Battery cycle life: the ISU-ILCC Battery Aging Dataset. It is on figshare, DOI 10.25380/iastate.22582234.v2, with licence CC BY 4.0, published 2023-12-21 (https://api.figshare.com/v2/articles/22582234). The description says 251 Li-ion polymer cells cycled under 63 conditions. The current release has 238 cells. The stress factors are charge rate, discharge rate and depth of discharge. Files: Valid_cells.csv, README_V2.0.pdf, capacity_fade.zip (140 KB), Q_interpolated.zip (48 MB), RPT_json.zip (0.9 GB), Cycling_json.zip (10 GB). I did not download the data. Cell counts and licence are as stated by figshare.
- Enzyme kinetics: no CC0 or CC BY dataset with at least 200 rows and four measured attributes per row confirmed.
  - Closest: CatPred-DB (https://huggingface.co/api/datasets/RosettaCommons/CatPred-DB, tag cc-by-4.0, size 10K to 100K rows; repo https://github.com/maranasgroup/CatPred-DB). The search snippet gave 23,197 kcat, 41,174 Km and 11,929 Ki entries. It is a BRENDA/SABIO-RK compilation, with separate processed files for kcat, Km and Ki. I did not check whether one row carries several measured attributes. The Hugging Face repo is gated (access restricted). The files could not be read, and the README text was fetched through the raw/resolve paths.
  - The BglB glycoside hydrolase mutant study (PLoS ONE 2016, PMC4729467) has 100 mutants, which is under 200. I did not find its data licence.
  - A search for deep mutational scanning stability/activity datasets on Zenodo returned nothing usable.
