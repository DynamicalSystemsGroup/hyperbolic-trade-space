# WP63 — Readout: the examples with an arc

Branch `wp63` off `dev` at 059132d3. Deliverables: `notes/examples-template.md` (D-1); `docs/examples.md`,
`docs/examples/{perovskite,amniote,wheat}.md` redrafted (D-2); this readout with the captures in
`work-packages/WP63-rounds/` (D-3; `capture.py` there, headless Chrome at 1,280 by 900 against a build served on port
8891, stopped after; `<page>-NN.png` top to bottom, `<page>.txt` the article text the cold readers got).

## Per page: what it did not do before, what it does now

| page | before | now |
|---|---|---|
| Cubesat (`examples.md`) | opened on results (seven contending metrics) with no account of the model, the columns or the question | the model and its configuration, a dictionary of the thirteen metrics and the configuration, the stakeholders' question, the fit, then what the fit says and what the case cannot show |
| Perovskite | named the dataset and fitted it; the physics was one line and the reading sat inside the variants | where the devices come from, a dictionary of Voc, Jsc, FF and PCE, the detailed-balance question, the fit, then the answer in the field's terms |
| Amniote | opened on its conclusion (the orientation of maturity decides the result) | the database and what a row is, a dictionary with the orientation and the covariate, the fast-slow question, the fit with the orientation test inside it, then the answer |
| Wheat | named the experiment as a DOI and stated "the negative association is that dilemma" before the variants | Broadbalk as an experiment, a dictionary with units and source columns, the harvest-index question, the fit, the cultivars, then the answer |

Prose words (the budget's count, `tests/test_site.py`; code, the dictionaries, alt text and comments excluded), before
→ after: cubesat 988 → 988 (budget 990); perovskite 663 → 687 (700); amniote 700 → 679 (700); wheat 660 → 690 (700);
the docsite's total 11,297 → 11,330 (budget 11,335; the total, not the page budgets, bound the last round of cuts).
Raw `wc -w`: 1,744 → 1,832; 879 → 951; 832 → 860; 788 → 857 (the rise is the dictionaries).

Kept on every page: every code block, every figure with its alt text and caption (Figures 6 to 10, numbers unchanged,
order unchanged), every quoted number with its `<!-- register -->` comment. Added: glossary links at the first use of
the contending set and the fit temperature on each page (zero words).

The cubesat arc runs in H2 headings, not under one H2 for the case: `tests/test_docs.py` pins the choosing-K sentences
to the section between `## Choosing K on the case` and the next H2, the user guide links the anchors
`#choosing-k-on-the-case` and `#three-metrics-as-shares-of-a-total`, and the test pins five phrases of the case
("has 2,134 feasible designs of 3,000", "contending set of seven metrics that trade off", "Thirteen metrics", …), all
kept. The heading "A cubesat trade study across power, mass and attitude control" went with that.

## Sentences cut, and what each no longer did

Cubesat
- "For a worked case: a synthetic satellite demonstrator, …": replaced by the account of the model (part 1).
- The three opening bullets: the one-term set moved into the fit, the two-term reading after the choosing-K checks,
  "A second table … gives a different one-term contending set" into the answer (the baseline set holds total mass).
- "the K the choosing-K checks pick": repeated the link two paragraphs up.
- "The price is in band widths and, for the costs and the mass, in USD": shortened to "in band widths and USD"; the
  block's own header says which.
- "the two cost limits are read after the fit": the requirements block above already reads them.
- "Reading it:" and its bullets: two sentences now; "V … also depends on the total" said what "not where V = 1" says.
- "The triples show how to read the figure; they are not findings.": a sentence about the figure; now "The triples are
  not findings."
- Synthetic case: "at the temperature used, that term carries the largest weight", "for a given total the term is
  largest there" (the cubesat ternary says it); "The temperature sets how closely the surface is pulled to the
  designs" (the user guide's job); the `build_slices(out, quantile=0.2)` option (the code does not use it); "The
  helpers are in `scripts/build_site_figures.py`" (the import says it).
- "Each page states the dataset and its licence, …": a sentence about pages; and "the orientation of a time cost
  decides what trades", the amniote result stated before its page. Now one line naming the three datasets.
- "Run it": folded into part 1.

Perovskite
- "it takes a few minutes": timing, not content.
- "The dataset has no time or cost attribute.": the dictionary's orientations say it.
- "The page gives each exponent as a range": metanarration.
- "so the pair the physics names is traded" and "The set was the whole set in all four, so its membership says
  little and the signs carry the reading": moved to the answer, the second shortened.
- "and the exponents" in the check: the ladder already shows the exponents move.
- "One term carries the dataset;": the term shares beside it say so.
- "List the largest values of every attribute": the check on one's own dataset already asks for the refit; now "Cap or
  remove entries that cannot be real, refit, and state the cap."
- Five headings (the conditioning rule, the named trade-off, the extremes rule, derived metrics, shares of the three
  metrics) became bold leads inside the fit or the question.

Amniote
- The opening paragraph (orientation decides the result, -0.97 to +0.84): the conclusion before the analysis; moved
  into the fit as "The orientation".
- "Here the strongest trade-off is longevity against earliness, and litters per year carries the fecundity side" and
  "litter size contends, but is nearly unrelated to longevity": findings placed before their numbers; moved to the
  answer.
- The four orientation bullets and "Body mass is the covariate": the dictionary carries them.
- "in about a minute": timing.
- "Litter size is in the page's fit": metanarration; now "in the four-metric fit".
- "such as lifespan, age at maturity and litter size" (part 1): the dictionary names the traits.
- "The set and the signs are the reading, not one exponent" (the answer): the variants paragraph gives the ranges; the
  answer keeps the one judgement the reading rests on.

Wheat
- "## Metrics and configuration": the dictionary carries it.
- "With two metrics the frontier is a line in log units, the simplex a segment, and the chart one position and one
  level.": a general account of the method; the caption names the line as the frontier.
- "The negative association is that dilemma." and "The dilemma and" in the ladder: presumed the answer; the answer is
  now in part 5.
- "so a reader fetches it", "the code below reads": about the reader and the placement.
- "Two metrics leave nothing to reduce." and "each treatment on its own strip": the PCA sentence and "on strips" carry
  them.

## Cold reads (R-5)

One context-gapped reader per page, given only `<page>.txt` and the page's screenshots of the first build. Two flags
were acted on after (noted per row) and the total-budget cuts followed; the captures in the folder are the final build.

| page | persona | what is the data | why was the analysis done | what did it find | matches intent |
|---|---|---|---|---|---|
| Cubesat | P3 | "The data are two sets of 3,000 synthetic 12U cubesat designs, one per range of controller gains, made by a SysML v2 demonstrator model with a simulated slew." | "The analysis asked whether the stakeholders' three measures (pointing error, unit cost and fleet cost) trade against one another and against the subsystem measures near the best designs, and whether one trade-off or two describes the table." | "All three stakeholder measures trade, together with available power, momentum headroom, settling time and depth of discharge, while total mass and control effort do not; two terms fit the primary range of gains best, the baseline range also brings in total mass, so the sampled gains change part of the answer, and only about a quarter of the designs meet all six requirements, which were checked only after the fit." | Yes, all three. It flagged that Figure 7 has pointing error trading against control effort while the answer says control effort does not contend; the answer now says "in the thirteen-metric fit" (Figure 7 fits three metrics). |
| Perovskite | P4 | "The data is an open, crowd-extracted table of about 42,000 perovskite solar cells reported in published papers (Perovskite Database v1.0.1), cut to 40,045 devices, each described by three larger-is-better numbers from its current-voltage scan: open-circuit voltage (Voc), short-circuit current density (Jsc) and fill factor (FF)." | "The question was whether the best reported devices trade voltage against current, as the Shockley–Queisser band-gap argument predicts, or whether the fill factor carries the trade." | "Near the frontier, Voc does trade against Jsc under every scaling choice tried, but that is not the strongest trade (Jsc against FF is stronger in the default fit), and how big it is depends a lot on five suspect rows (-0.14 rising to -0.82 when they are capped); all three metrics stay in play, and the exponents move a lot from one scaling to the next." | Yes, all three ("crowd-extracted" is the reader's word; the source says extracted from peer-reviewed papers). |
| Amniote | P3 | "The data comes from a public database of life-history traits for mammals, birds and reptiles, one row per species. It has about 21,000 species, but only 2,770 have all five traits filled in: longevity, litter size, litters per year, age at maturity and body mass." | "The analysis was meant to test the 'fast-slow continuum': among the species nearest the frontier, does a long life trade off against early maturity and high fecundity, and which reproductive measure carries the fast side?" | "It found that, near the frontier, long-lived species mature late and have few litters per year: the trade-off between longevity and earliness is very strong (about -0.9) and holds under every scaling and body-mass treatment, litters per year is the fecundity side, and litter size is nearly unrelated to longevity. The result depends on treating late maturity as a cost; flip that judgement and the conclusions change." | Yes, all three. It flagged that the caption's four-metric fit and the three-metric code were hard to tell apart; the fit paragraph now says "For the four-metric fit". |
| Wheat | P4 | "The data is 3,753 plot-years from Rothamsted's Broadbalk winter-wheat experiment, covering 1968 to 2022. Each row is one plot in one year, with grain and straw yield in t/ha plus the fertilizer treatment, cultivar, year, nitrogen and section." | "The analysis asked two things: near the top of the yield range, does more grain come with less straw, and do the 1968 cultivars and the 2022 cultivars split their biomass between grain and straw differently (harvest index)?" | "Near the fitted frontier, plot-years with more grain have less straw in every conditioning variant (association about -0.6 to -0.9), and at high nitrogen the newest cultivar puts about three quarters of its biomass into grain against about half for the oldest, at similar total biomass; a separate 'grain-only ceiling' from a second term appears only under some conditioning choices." | Yes, all three. |

What every reader could not work out: the method's terms (contending set, temperature, slack, certified, n-lemma, V)
are used undefined on the dataset pages; the P4 readers did not find where the method sits beside PCA; the P3 readers
did not find what their own table must look like (the pages call `run.condition` and `case.load_study`). The first is
partly met by the glossary links added; the rest is a call below.

## Sources for parts (1) and (2)

- Perovskite: `examples/perovskite/manifest.toml`, `run.py` (columns, the FF ≤ 1 rule, PCE set aside); the paper's
  Crossref record (api.crossref.org/works/10.1038/s41560-021-00941-3: device data extracted from peer-reviewed papers,
  over 42,400 devices); Zenodo record 5837035 (a CSV snapshot of the database, CC BY 4.0). Units V and mA/cm2 from the
  page as it stood; FF a fraction from the FF ≤ 1 rule.
- Amniote: `examples/amniote/manifest.toml`, `run.py` (columns, orientation, the -999 sentinel, the mass covariate);
  the paper's Crossref record (api.crossref.org/works/10.1890/15-0846R.1: compiled for comparative analyses of birds,
  mammals and reptiles from studies, databases and books, the median where values differ). Units from the column
  names (`_y`, `_n`, `_per_y`, `_d`, `_g`). The Wiley and figshare pages refused the fetch (403).
- Wheat: `examples/wheat/manifest.toml`, `derive.py` (`COLUMNS`: the source columns `grain`, `straw`, `harvest_year`,
  `fertilizer_code`, `cultivar`, `total_fertilizer_n_amount`, `cropping`, `section`); the e-RA landing page
  (www.era.rothamsted.ac.uk/dataset/rbk1/01-YLD6822: started autumn 1843; fertilizers and manure on strips; sections
  with rotations; "Wheat and straw yields are at 85% dry matter"). t/ha from the page as it stood and
  `results.json`'s biomass.
- Cubesat: `examples/adcs/case.py` (`_ATTRS`, `_UNITS`, `_ORIENT`, `design_vars`, `flags`, data `data/v2`),
  `examples/adcs/case-model.md` (the configuration's swaps and tunes, MoE and MoP, control effort in N.m.s, "a
  payload that points and a launch they can afford"), the paper's Section 7 (12U-class fleet, the two regimes' Kp
  ranges).

## Checks

| check | exit |
|---|---|
| `uv run ruff check .` | 0 |
| `uv run ruff format --check .` | 0 |
| `uv run mkdocs build -q` | 0 |
| `uv run pytest -q tests/test_wp45_examples.py tests/test_site.py tests/test_docs.py` | 0 (163 passed, 1 skipped) |
| `uv run python scripts/check_vocabulary.py` | 0, 0 new violations |
| `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` | 1, as on dev; `docs/examples.md` rises against the baseline no more than on dev (parens 5 = 5, long parentheticals 1 → 0, long sentences 5 = 5, terms undefined at first use 10 → 9). The dataset pages are not checker surfaces; run on a copy as `docs/*.md`, no count rose against dev. |

## The calls that are his

1. **The dictionary as a text block.** The site forbids Markdown tables (`test_no_table_needs_columns_on_a_phone`)
   and a list would cost about a hundred words of each page's budget, so each dictionary is a ```` ```text ```` block
   laid out as a table (outside the word count, as tables are). Keep, or raise the budgets for lists.
2. **The method's words on the example pages.** Every cold reader stopped at undefined terms (contending set,
   temperature, slack, certified, n-lemma, V). Glossary links at first use are in; a one-line "how to read these
   numbers" pointer to the user guide on each page would cost words the budgets do not have.
3. **The perovskite question's physics.** "A wider gap raises the first and lowers the second" rests on the cited
   detailed-balance paper, not on a lemma or a generated value.
4. **The wheat answer.** "the shift the breeding studies report" sits beside "describes and does not test breeding";
   keep, or narrow to the medians alone.
5. **The synthetic three-metric case** is the root page's construction, not an example with an arc; it stays on the
   Examples page unchanged in kind. Move it, or leave it.
