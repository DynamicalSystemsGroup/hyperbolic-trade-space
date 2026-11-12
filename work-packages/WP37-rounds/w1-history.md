# WP37 W1: the public history of cadCAD, GDS and PSuU, and the team's place in scientific computing

Worker W1 (Sonnet), read 2026-11-12. Public sources only. A source is "read" when its page (or API record) was
fetched on that date and the stated line is what that page says. Sources that could not be fetched are listed
separately and carry no claim. Source titles that carry vocabulary the page's own words must not use are linked
verbatim and marked (T).

## 0. Reading rules applied

- Fetched means fetched by this worker on 2026-11-12. Medium posts (the firm's blog) returned HTTP 403 to every
  fetch, so none is read; section 6 lists them with what they would be used for, to be fetched by someone with a
  browser. Nothing here rests on a search snippet alone except where marked "snippet".
- The BlockScience GitHub organisation's repositories show a single commit dated 2026-05-15 by `bsci-ops`
  (history flattened), so their commit dates say nothing about when the work was done. Dates below come from the
  cadCAD-org repositories, PyPI, papers and talk programmes.
- Private repositories were visible to this worker's credentials (organisation listings include them). None is
  used or cited; one record (`cadCAD-org/gds-foundations`) was seen to be private and is excluded. The
  `DynamicalSystemsGroup` and `BlockScience` organisation lists were used only to find public repositories,
  whose visibility was checked one by one.

## 1. cadCAD: the early formalisation and the code

| # | Item and URL (read 2026-11-12) | What the page says | Names on the page | Date |
|---|---|---|---|---|
| 1.1 | State-space paper, arXiv: https://arxiv.org/abs/1807.00955 | A dynamical-systems framework for describing networks and designing their economic rules with provable properties, tied to control tools such as Lyapunov-like functions. Comments field: "The Ninth International Conference on Complex Systems Oral Presentation". Title (T): "A State-Space Modeling Framework for Engineering Blockchain-Enabled Economic Systems". | Michael Zargham, Zixuan Zhang, Victor Preciado | submitted 3 July 2018 |
| 1.2 | cadCAD repository, README.md creation: https://github.com/cadCAD-org/cadCAD (first commit, via the GitHub API) | The repository's first commit is "Create README.md". | Markus Buhatem Koch (commit author) | 10 Sept 2018 |
| 1.3 | AUTHORS.txt in that repository: https://github.com/cadCAD-org/cadCAD/blob/master/AUTHORS.txt | "cadCAD was originally implemented by Joshua E. Jodesty and designed by Michael Zargham, Markus B. Koch, and Matthew V. Barlin in 2018. Since then, upgrades and improvements were further committed by Danilo L. Bernardineli, Tyler D. Mace and Emanuel Lima." Current maintainers: Emanuel Lima, Michael Zargham. Past contributors listed also include Zixuan Zhang, Charles Rice, Benjamin Scholz. A "We'd also like to thank" list includes Andrew Clark (@aclarkData) and Nick Hirannet, among others. | as quoted | file at version 0.5.3 (April 2024) |
| 1.4 | cadCAD on PyPI (JSON record): https://pypi.org/pypi/cadCAD/json | Author "cadCAD-org Developers", contact info@block.science; summary "a differential games based simulation software package for research, validation, and Computer Aided Design of economic systems". Earliest release in the record is 0.3.0 (uploaded 2019-09-07); latest 0.5.3 (2024-04-19). | cadCAD-org Developers | 2019-09-07 to 2024-04-19 |
| 1.5 | cadCAD contributors by commit count: https://github.com/cadCAD-org/cadCAD/graphs/contributors (API `contributors`) | Counts: JEJodesty 731, markusbkoch 74, danlessa 37, tylerdmace 17, BenSchZA 14, lima-emanuel 4, mzargham 3. | GitHub accounts as listed | read 2026-11-12 |
| 1.6 | cadCAD README: https://github.com/cadCAD-org/cadCAD | "a Python package that assists in the processes of designing, testing and validating complex systems through simulation, with support for Monte Carlo methods, A/B testing and parameter sweeping." MIT license. | none named | v0.5.3 |
| 1.7 | cadCAD site: https://cadcad.org | "cadCAD was created as an internal tool at BlockScience"; "We've open-sourced cadCAD for the community". No dates, no individuals, no papers. | BlockScience | undated |
| 1.8 | CHANGELOG (same repository), v0.5.0 to 0.5.3: https://github.com/cadCAD-org/cadCAD/blob/master/CHANGELOG.md | Releases 0.5.0 (2023-12-20) to 0.5.3 (April 19, 2024). | none | 2023-12 to 2024-04 |
| 1.9 | Julia implementation, repository: https://github.com/cadCAD-org/CadCAD.jl | First commit by Emanuel Lima, 2021-05-14; last commit read 2024-12-13. | Emanuel Lima | 2021-05-14 |
| 1.10 | Tools and analysis library: https://github.com/cadCAD-org/cadCAD-tools and https://github.com/cadCAD-org/cadCAD_machine_search | cadCAD-tools: "wrappers for executing simulations easily as well as tools for profiling and typing." Machine search: "cadCAD tools for preparing & analyzing experiments where large-scale machine search for selecting parameters are involved." First commits 2021-03-10 and 2021-02-02 (author "Danillo Lessa Bernardineli"). | Danilo Lessa Bernardineli (commit author) | 2021 |
| 1.11 | Tutorials repository: https://github.com/cadCAD-org/cadCAD-Tutorials | First commit 2019-01-09 by Joshua E. Jodesty; 155 commits to 2021-04-17. | Joshua E. Jodesty | 2019 to 2021 |

## 2. GDS: the mathematical specification work

| # | Item and URL | What the page says | Names | Date |
|---|---|---|---|---|
| 2.1 | WU Vienna record: https://research.wu.ac.at/de/publications/generalized-dynamical-systems-part-i-foundations/ | "Generalized Dynamical Systems Part I: Foundations", working paper, WU Institute for Cryptoeconomics series, DOI 10.57938/e8d456ea-d975-4111-ac41-052ce73cb0cc. A GDS is a data structure mapped to itself, the maps closed under composition; the paper treats decision problems with constraints, unifying optimal control, system dynamics, agent-based modelling and networks, with a contingent-derivative metric and a differential-inclusion reading. Parts II and III are said to cover applications and a software implementation in cadCAD. | Michael Zargham, Jamsheed Shorish | published 14 July 2022 |
| 2.2 | RePEc record of the same: https://ideas.repec.org/p/wiw/wus051/8671.html | Same paper, working paper no. 8671, 2022. | as above | 2022 |
| 2.3 | GDS code, `gds-core`: https://github.com/DynamicalSystemsGroup/gds-core | "Generalized Dynamical Systems — typed compositional specifications for complex systems." Credits: Author Rohan Mehta (Dynamical Systems Group); "Theoretical foundation" Michael Zargham and Jamsheed Shorish, with a 2021 blog post "Generalized Dynamical Systems, Part I: Foundations" (that blog domain did not resolve; unread); "Architectural inspiration" Sean McOwen (MSML, bdp-lib); Zargham for project direction, theory guidance, technical review; Peter Hacker for code auditing and review. Apache-2.0. Preferred citation is the 2022 paper. | Mehta, Zargham, Shorish, McOwen, Hacker | repository created 2026-02-21 (organisation listing) |
| 2.4 | MSML (Mathematical Specification Mapping Library): https://github.com/DynamicalSystemsGroup/MSML | Library for "standardizing the creation of mathematical specifications as JSON objects"; "in line with current Dynamical Systems Group research on Generalized Dynamical Systems". First commit by Sean McOwen 2023-05-19 (888 of 889 commits his; one by danlessa). | Sean McOwen | from 2023-05-19 |
| 2.5 | Block diagram library: https://github.com/DynamicalSystemsGroup/bdp-lib | "a library for instantiating and validating fundamental block diagrams"; contributors Sean McOwen (161), danlessa (1). | Sean McOwen | repository created 2025-01-29 |
| 2.6 | Block diagrams of dynamical systems: https://github.com/DynamicalSystemsGroup/dynamical-block-diagrams | "Formal analysis of the execution and initialization of block diagrams of dynamical systems", with a formal PDF and a Julia implementation, `cadCAD.jl`; credits Carolina Riascos for a consensus-network write-up. First commit 2024-07-26 by "ekez". | Carolina Riascos; commit author "ekez" | 2024 |
| 2.7 | Block diagrams, categorical cybernetics: SSRN, DOI https://doi.org/10.2139/ssrn.4569037 | Listed on Zargham's publications page as "Block Diagrams for Categorical Cybernetics", SSRN 4569037, 2023, by Zargham and Shorish. The SSRN page itself returned 403; the line rests on Zargham's page (3.1). | Zargham, Shorish | 2023 |
| 2.8 | Dynamic games seminar materials: https://github.com/cadCAD-org/DynamicGamesSeminar | "Design and Analysis of Dynamic Games": dynamic games "as dynamical systems where the inputs are controlled by strategic agents with their own beliefs, preferences" (README, partly a template); notation "similar to that of Stephen Boyd at Stanford". First commit 2020-05-23 by Michael Zargham. | Michael Zargham | 2020 |

## 3. Papers by the named people that bear on the history (all linked by DOI; read via Zargham's list unless noted)

Zargham's publications page: https://michael.zargham.org/publications (read 2026-11-12). Crossref records
(https://api.crossref.org/works/<doi>) were read for the rows marked CR. Titles marked (T).

| # | Item | What the record says | Names | Date |
|---|---|---|---|---|
| 3.1 | "From Curved Bonding to Configuration Spaces" (T), IEEE ICBC: https://doi.org/10.1109/ICBC48266.2020.9169474 (CR) | Conference paper. | Zargham, Shorish, Krzysztof Paruch | May 2020 |
| 3.2 | "Economic Games as Estimators", MARBLE 2020, Springer: https://doi.org/10.1007/978-3-030-53356-4_8 (CR) | Chapter in Springer Proceedings in Business and Economics. | Zargham, Paruch, Shorish | 2020 |
| 3.3 | "On Modeling Blockchain-Enabled Economic Networks as Stochastic Dynamical Systems" (T), Applied Network Science: https://doi.org/10.1007/s41109-020-0254-9 (CR) | Journal article; extends item 1.1. | Zixuan Zhang, Zargham, Victor Preciado | 19 Mar 2020 |
| 3.4 | "Evidence Based Decision Making in Blockchain Economic Systems: From Theory to Practice" (T), arXiv: https://arxiv.org/abs/2001.03020 | "data science and stochastic simulation can reveal system-level behaviors that designers did not expect"; finding performance issues at design time can prevent costly emergency fixes. | Marek Laskowski, Zargham, Hjalmar Turesson, Matt Barlin, Danil Kabanov, Eden Dhaliwal | v1 8 Jan 2020; v2 9 May 2020 |
| 3.5 | "Token Economics in Real Life: Cryptocurrency and Incentives Design for Insolar's Blockchain Network" (T), IEEE Computer: https://doi.org/10.1109/MC.2020.2996572 (CR) | Crossref lists Laskowski, Zargham and Barlin with affiliation "BlockScience, Oakland, California"; the other authors are York University and Insolar Technologies. | Henry M. Kim, Laskowski, Zargham, Hjalmar Turesson, Matthew Barlin, Danil Kabanov | Jan 2021 |
| 3.6 | "Complex Systems Modeling of Community Inclusion Currencies", Computational Economics 64(2): https://doi.org/10.1007/s10614-023-10445-9 (CR); WU working paper https://research.wu.ac.at/en/publications/complex-systems-modeling-of-community-inclusion-currencies/ ; Reading discussion paper https://ideas.repec.org/p/rdg/emxxdp/em-dp2021-06.html | Model of subpopulations of a local complementary currency in Kenya; 50 utility types identified from transaction records; simulated at the meso level. Crossref abstract: the authors used cadCAD. A BlockScience post (unread, 403) describes it as a collaboration with the Grassroots Economics Foundation and the Danish Red Cross (snippet). Reading record: Andrew Clark and Alexander Mihailov, Department of Economics, University of Reading; Zargham, WU Vienna. | Andrew Clark, Alexander Mihailov, Zargham | Reading dp 2021; WU wp 8 July 2022; journal 28 Sept 2023 (print 2024) |
| 3.7 | "Min-Maxing Complexity on Digital Infrastructure Mechanisms through Occam's Razor and Ashby's Law of Requisite Variety": https://zenodo.org/records/12170072 and SSRN 4865894 https://doi.org/10.2139/ssrn.4865894 | Zenodo record: type presentation, creator Danilo Lessa Bernardineli, CC BY 4.0, 19 June 2024, no description. The SSRN page returned 403; Zargham's list gives the author line Bernardineli, Ben-Meir, Zargham, Jakob Hackel. | Bernardineli; (per Zargham's list) Ilan Ben-Meir, Zargham, Jakob Hackel | 19 June 2024 |
| 3.8 | "Formalizing Document Assurance: A Topological Framework for Verification, Validation, and Human Accountability", INCOSE IS 36: https://doi.org/10.1002/iis2.70203 (CR) | Single-author paper; affiliation "Dynamical Systems Group". | Zargham | July 2026 |
| 3.9 | Optimisation and control work (background, for W2 to expand): "Accelerated Dual Descent for Network Optimization", arXiv https://arxiv.org/abs/1104.1157 (6 Apr 2011); IEEE TAC 59(4), https://doi.org/10.1109/TAC.2013.2293221 | Zargham, Ribeiro, Ozdaglar, Jadbabaie. | as listed | 2011 to 2014 |

## 4. PSuU and firm work whose code is public

| # | Item and URL | What the page says | Names | Date |
|---|---|---|---|---|
| 4.1 | PSuU information repo (HackMD): https://hackmd.io/@danlessa/HklBYikEY | PSuU "standardizing experiments and analysis so teams can iterate quickly on recommendations for multi-stakeholder scenarios built on complex models"; eight steps from goals and KPIs, success criteria, search regions, control versus environmental parameters, simulation, to a feature dataset for dimensionality reduction, sensitivity analysis and non-linear fitting; names cadCAD Machine Search, the Interacting AMM model, a Filecoin report, "Bosch Workshop #4". No author or date on the page; the URL path is under the handle `danlessa`. | none on page | undated |
| 4.2 | Interacting AMM model: https://github.com/cadCAD-org/interacting-amm-model | Public cadCAD example named by 4.1 as running the full PSuU process; first commit 2021-05-07 by Danilo Lessa Bernardineli; last 2021-07-30. | Bernardineli (commit author) | 2021 |
| 4.3 | Subspace model: https://github.com/BlockScience/subspace | README: model development "was later adapted into a workflow known as the Parameter Selection Under Uncertainty Framework, or PSuU"; glossary defines PSuU as a methodology for selecting robust parameters under uncertainty. No authors named. | none | undated (history flattened) |
| 4.4 | Aztec design model: https://github.com/BlockScience/aztec-gddt and https://github.com/BlockScience/aztec-gddt-v2 | "a cadCAD simulation model of the Aztec system ... The goal of the model is to understand the effect of design parameters and agent behaviors on the health of the Aztec network, as measured through various Key Performance Indicators (KPIs)." v2: KPIs "aligned with the Aztec Labs team". Cover image credited to Danilo L. Bernardineli, 2023. | Bernardineli (image credit) | 2023 onward |
| 4.5 | Neural Quorum Governance demo: https://github.com/BlockScience/scf-reports-public | README: a mechanism "ideated, specified and implemented in a joint effort between BlockScience and the Stellar Development Foundation (SDF)"; a cadCAD simulation generating synthetic datasets for user behaviour and outcomes. | BlockScience, SDF | undated |
| 4.6 | Reflexer model: https://github.com/BlockScience/reflexer | "create a cadCAD model to simulate the Reflexer, Rai system"; goals include stability of a controller "for a range of exogenous shocks". | none | undated |
| 4.7 | Other public client-linked models, listed only (READMEs not all read): https://github.com/BlockScience/filecoin-baseline-incentives ("Interactive Calculator ... based on cadCAD + Streamlit"), https://github.com/BlockScience/PocketSimulationModel ("simulation model for testing economic scenarios related to the Pocket Network"), https://github.com/BlockScience/gitcoin | Each is a public simulation model named for the client system. | none | undated |

None of these pages states that the work was open-sourced with the client's permission; the supervisor says it
was, and the page can say "published", not "with permission", unless he supplies a source.

## 5. Scientific computing community (SciPy, PyData, NumFOCUS)

| # | Item and URL (read 2026-11-12) | What the page says | Names | Date |
|---|---|---|---|---|
| 5.1 | NumFOCUS people page: https://numfocus.org/community/people | Text: "Michael Zargham, Ph.D., is the Chief Executive Officer and Chief Engineer of Dynamical Systems Group", under the Advisory Council heading; serves on the advisory council and "previously served on its executive director hiring committee"; also Research Director and board member of Metagov. | Zargham | undated |
| 5.2 | Zargham's CV page: https://michael.zargham.org | "2022 to present: Advisory Council Member, NumFOCUS"; "2017: Founded Dynamical Systems Group, originally named BlockScience" (paraphrase of the page's timeline). | Zargham | 2022 to present |
| 5.3 | NumFOCUS sponsors page: https://numfocus.org/sponsors | Under "Community Sponsors", a logo labelled "Dynamical Systems" linking to http://www.dynamicalsystemsgroup.com. No level, date or description. | Dynamical Systems Group | undated |
| 5.4 | SciPy 2026 talk: https://pretalx.com/scipy-2026/talk/TBDWJZ/ | "Derivations, Not Just Simulations: Teaching Applied Mathematics with Scientific Python", 17 July 2026, 10:45, Johnson Great Room; speaker bio "Chief Engineer at BlockScience". Six-stage pattern (Motivate, Symbolize, Derive, Lambdify, Simulate, Validate) with SymPy, NumPy, SciPy, matplotlib and marimo notebooks. | Zargham | 17 July 2026 |
| 5.5 | Speaker page: https://pretalx.com/scipy-2026/speaker/NNYAMC/ | Bio: "advising Humane Intelligence and NumFocus"; PhD in Electrical and Systems Engineering, University of Pennsylvania. Track: Scientific Computing in Education. | Zargham | 2026 |
| 5.6 | Talk materials: https://github.com/mzargham/hc-marimo (public) and https://youtu.be/EV5ycMqQoDI | Repository description: "Source Materials for my SciPy 2026 talk on Mathematics Education with Scientific Python." The proceedings entry is listed on Zargham's page as "forthcoming" in the Proceedings of the 25th Python in Science Conference. | Zargham | 2026 |
| 5.7 | JuliaCon 2023: https://pretalx.com/juliacon2023/talk/ERXTXE/ | "cadCAD.jl: A Modeling Library for Generalized Dynamical Systems", lightning talk, 28 July 2023; speaker bio: "Research software engineer at Block Science and lead maintainer of cadCAD" (https://pretalx.com/juliacon2023/speaker/CV3VMU/). | Emanuel Lima | 28 July 2023 |
| 5.8 | JuliaCon 2024: https://pretalx.com/juliacon2024/talk/JNFYPP/ | Same title, 12 July 2024, with a live simulation demo; bio "Senior Research Software Engineer at Block Science". | Emanuel Lima | 12 July 2024 |
| 5.9 | Metagov role (for context): https://michael.zargham.org (CV) | "2021 to present: Research Director and Board Member, Metagov". | Zargham | 2021 to present |

Not found (searched, nothing returned): a SciPy proceedings paper or earlier SciPy talk by anyone at the firm;
any PyData talk; cadCAD named as a NumFOCUS project; a NumFOCUS or cadcad.org page tying cadCAD to NumFOCUS. The
Medium post "cadCAD: Filling a Critical Gap in Open-Source Data Science" (snippet only, section 6) is said by a
search summary to describe cadCAD as part of the scientific Python ecosystem; unread.

## 6. Not fetched (HTTP 403 or not resolvable); no claim rests on these

| URL | What it would give | Status |
|---|---|---|
| https://medium.com/block-science/introducing-complex-adaptive-dynamics-computer-aided-design-cadcad-38b63b541eb8 | the firm's own account of cadCAD's origin; a search summary attributes a 2018 start and an August 2019 open-source announcement in Berlin to a Zargham and Gabler post (snippet only) | 403 |
| https://medium.com/block-science/how-to-perform-parameter-selection-under-uncertainty-976931ba7e5d | the PSuU article (author and date) | 403 |
| https://medium.com/block-science/cadcad-filling-a-critical-gap-in-open-source-data-science-fcd0d3faa8ed | the scientific-Python claim | 403 |
| https://medium.com/block-science/complex-systems-modeling-of-community-inclusion-currencies-4e2161787934 | the collaboration statement in 3.6 | not fetched |
| https://wiki.p2pfoundation.net/Complex_Adaptive_Dynamics_Computer-Aided_Design | a third-party summary mentioning the International Conference on Complex Systems paper (consistent with 1.1) | 403 |
| https://blog.dynamicalsystemsgroup.com/generalized-dynamical-systems-part-i-foundations-2/ | the 2021 GDS blog post cited by gds-core | host does not resolve |
| https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4865894 and ...4569037 | author lines for 3.7 and 2.7 | 403 |
| https://science.ecosyste.ms/projects/64753 | papers citing cadCAD | 403 |

## 7. People: what a public page says, and nothing more

"Background" is recorded only where a page states it. Dates are the date of the page's statement.

| Person | What a public page says | URL (read 2026-11-12) |
|---|---|---|
| Michael Zargham | Founded the firm in 2017, "originally named BlockScience", now Dynamical Systems Group; PhD, Electrical and Systems Engineering, University of Pennsylvania (2014), research on optimal control for resource allocation in networks; originator and lead architect of cadCAD since 2017 (his CV); co-author of GDS Part I. | https://michael.zargham.org ; https://michael.zargham.org/research ; https://pretalx.com/scipy-2026/speaker/NNYAMC/ |
| Markus Koch | "Markus Buhatem Koch": first commit of the cadCAD repository, 10 Sept 2018; named a designer of cadCAD in AUTHORS.txt; 74 commits. GitHub profile gives no bio or employer. No other public statement found. | https://github.com/cadCAD-org/cadCAD (AUTHORS.txt, commits) ; https://github.com/markusbkoch |
| Danilo Bernardineli | Past contributor in AUTHORS.txt; 37 commits to cadCAD; first commits to the machine-search and tools libraries (2021); creator of the 2024 Zenodo presentation; first commit author of the Interacting AMM model. His GitHub bio: "atmosphere physicist" and "research eng @Block_Science" (self-stated). | https://github.com/danlessa ; https://zenodo.org/records/12170072 |
| Rohan Mehta | Author of `gds-core` (466 of its commits), credited as "Rohan Mehta, Dynamical Systems Group" in its README. His GitHub profile lists a different company (Chaos Coded Systems) and "Data Scientist, Researcher". | https://github.com/DynamicalSystemsGroup/gds-core ; https://github.com/rororowyourboat |
| Joshua Jodesty | "originally implemented" cadCAD (AUTHORS.txt); 731 commits, first commit to the Tutorials repository 2019-01-09; GitHub company field: BlockScience. No bio. | https://github.com/cadCAD-org/cadCAD ; https://github.com/JEJodesty |
| Jamsheed Shorish | Co-author of GDS Part I (2022); co-author of the 2019 and 2020 papers (3.1, 3.2). RePEc: Shorish Research, Leuven (80 percent) and WU Vienna (20 percent), homepage shorishresearch.com. A search summary of a Vlerick Business School profile calls him an economist (page itself returned 404; snippet only). | https://ideas.repec.org/e/psh169.html ; https://research.wu.ac.at/de/publications/generalized-dynamical-systems-part-i-foundations/ |
| Kris Paruch | Co-author with Zargham and Shorish of "From Curved Bonding to Configuration Spaces" (2020) and "Economic Games as Estimators" (2020); Crossref gives the name as Krzysztof Paruch; listed as a public member of the cadCAD-org GitHub organisation (login `KrisParuch`). No bio or role found. | https://doi.org/10.1109/ICBC48266.2020.9169474 ; https://doi.org/10.1007/978-3-030-53356-4_8 ; https://github.com/orgs/cadCAD-org/people |
| Andrew "Octopus" Penland | Nothing found. Web and GitHub searches on the name returned no page naming him in connection with the firm, cadCAD, GDS or PSuU. A BlockScience social post that thanks "Octopus" (snippet) does not state a surname. Cannot be credited from public sources found; supervisor to supply a source or a public handle. | none |
| Jakob Hackel | Appears only as fourth author in Zargham's own list of "Min-Maxing Complexity on Digital Infrastructure Mechanisms..." (SSRN 4865894, 2024); the SSRN page was not readable and the Zenodo record lists only Bernardineli. No bio found. | https://michael.zargham.org/publications |
| Emanuel Lima | Lead maintainer of cadCAD (JuliaCon 2023 bio), listed with Zargham as current maintainer in AUTHORS.txt; author of the Julia implementation (first commit 2021-05-14); Senior Research Software Engineer at Block Science (JuliaCon 2024 bio). | https://pretalx.com/juliacon2023/speaker/CV3VMU/ ; https://pretalx.com/juliacon2024/talk/JNFYPP/ ; https://github.com/cadCAD-org/CadCAD.jl |
| Andrew Clark | Named in AUTHORS.txt's thanks list (@aclarkData); first author of the 2021 to 2024 community-currency paper (3.6); Reading discussion paper lists Department of Economics, University of Reading; the WU working paper lists the Institute for Cryptoeconomics. No statement of a role at the firm found. | https://ideas.repec.org/p/rdg/emxxdp/em-dp2021-06.html ; https://github.com/cadCAD-org/cadCAD (AUTHORS.txt) |
| Sean McOwen | 888 of 889 commits to MSML (first 2023-05-19) and 161 of 162 to bdp-lib; credited in `gds-core` for "architectural inspiration". GitHub profile has no bio. No other public statement found. | https://github.com/DynamicalSystemsGroup/MSML ; https://github.com/DynamicalSystemsGroup/bdp-lib ; https://github.com/DynamicalSystemsGroup/gds-core |

Others the sources name, offered to the supervisor as candidates, not added: Matthew (Matt) Barlin ("designed", AUTHORS.txt;
author of 3.4 and 3.5; Crossref affiliation BlockScience, 2021); Zixuan Zhang (past contributor, AUTHORS.txt; first
author of 3.3); Tyler Mace (17 commits; AUTHORS.txt); Marek Laskowski (3.4, 3.5; Crossref affiliation
BlockScience); Peter Hacker (`gds-core` review credit); Nick Hirannet (AUTHORS.txt thanks; GitHub company
"@DynamicalSystemsGroup"); Benjamin Scholz (AUTHORS.txt).

### The backgrounds sentence

The supervisor's sentence ("controls engineers, economists, physicists, mathematicians and computer scientists")
is backed in part by public pages: controls engineering (Zargham's PhD and papers, 7 and 9 above), economics
(Shorish on RePEc; Clark and Mihailov at a University department of economics), physics (Bernardineli's own GitHub
bio: "atmosphere physicist"). Mathematicians and computer scientists are not stated by any page read for a named
person. A sentence that says "controls engineering, economics, physics" with named examples is supported; the
other two need a source from the supervisor (a bio page, a CV) or are left unnamed.

## 8. Timeline

| Date | Event | Source |
|---|---|---|
| 2017 | The firm founded (Zargham's CV: "originally named BlockScience"; DSG site: working on dynamical systems "since 2017") | 5.2; https://dynamicalsystemsgroup.com |
| 3 July 2018 | State-space framework preprint, presented at the Ninth International Conference on Complex Systems | 1.1 |
| 10 Sept 2018 | First commit of the cadCAD repository (README), by Markus Buhatem Koch | 1.2 |
| 2018 | cadCAD "originally implemented by" Jodesty, "designed by" Zargham, Koch, Barlin | 1.3 |
| 9 Jan 2019 | First commit to the cadCAD tutorials repository (Jodesty) | 1.11 |
| 7 Sept 2019 | cadCAD 0.3.0 on PyPI (earliest release in the record) | 1.4 |
| 8 Jan 2020 | Evidence-based design paper v1 (Laskowski, Zargham, Turesson, Barlin, Kabanov, Dhaliwal) | 3.4 |
| March to May 2020 | Applied Network Science paper; the two papers with Paruch and Shorish | 3.3, 3.1, 3.2 |
| 23 May 2020 | Dynamic games seminar repository begun (Zargham) | 2.8 |
| Feb to May 2021 | Machine-search library, cadCAD-tools, Interacting AMM model begun (Bernardineli); Julia implementation begun (Lima, 14 May) | 1.9, 1.10, 4.2 |
| Jan 2021 | IEEE Computer paper, authors with BlockScience affiliation (client system study) | 3.5 |
| 14 July 2022 | GDS Part I working paper published (Zargham, Shorish) | 2.1 |
| 2022 to present | Zargham on the NumFOCUS Advisory Council | 5.1, 5.2 |
| 28 July 2023 | JuliaCon talk on cadCAD.jl (Lima) | 5.7 |
| 28 Sept 2023 | Community-currency paper published online (Clark, Mihailov, Zargham) | 3.6 |
| 19 June 2024 | Zenodo presentation (Bernardineli) | 3.7 |
| 19 April 2024 | cadCAD 0.5.3, latest PyPI release | 1.4, 1.8 |
| 12 July 2024 | JuliaCon talk on cadCAD.jl (Lima) | 5.8 |
| 2026-02-21 | `gds-core` repository created (Mehta; credits Zargham, Shorish, McOwen) | 2.3 |
| 2026 | Zargham: maintainer, OpenMBEE; SciPy 2026 talk, 17 July; INCOSE IS paper, July | https://michael.zargham.org ; 5.4 ; 3.8 |

## 9. Thin record: what the public record does not support, so the page says less

1. When the firm was renamed. Zargham's CV says the firm was "originally named BlockScience"; the NumFOCUS people
   page and the DSG site use Dynamical Systems Group; the SciPy 2026 speaker bio still says BlockScience. No page
   read gives a rebrand date or announcement. The page can say "founded in 2017, BlockScience, now Dynamical
   Systems Group", with the CV as its source and no date for the change.
2. The firm as an "engineering firm doing requirements, architecture, design, theorems about algorithms,
   simulation and analysis for clients". The firm's own public descriptions say "complex systems engineering,
   R&D, and analytics firm" (BlockScience GitHub organisation) and "systems engineering firm" (DSG site). The
   specific list of activities has no single public page read; it can be shown by linked works (a theorem paper,
   a simulation, a client model) rather than asserted.
3. Client permission. No README read states the work was open-sourced with the client's permission. The page can
   say "published models of client systems", not "with permission".
4. Studying "feasible design spaces under uncertain, strategic and adversarial users". PSuU (4.1, 4.3) is public
   as a method for choosing parameters under uncertainty with competing goals; the dynamic-games seminar (2.8)
   is public for strategic agents. No page read uses the word "adversarial" for the firm's own method. The five
   attributes (highly automated, adversarial, value at risk, multipolar sponsorship, legitimacy) are the
   supervisor's; no source read states them. The page can carry them as the supervisor's account, or show them by
   a linked work, but a footnote cannot back them from the record found.
5. cadCAD's origin story, the 2019 open-source announcement and the PSuU article's author and date: all in
   Medium posts that could not be fetched. The code history (1.2, 1.3) stands without them.
6. Roles. AUTHORS.txt gives "implemented" and "designed" for 2018, maintainers for the current time, and a
   contributor list; no page read states titles or employment for Jodesty, Koch, Paruch, Hackel, McOwen or Mehta
   (Mehta's README line says "Dynamical Systems Group"; his own profile names another company). Penland: nothing.
7. SciPy and PyData. The record read shows one SciPy talk (2026, Zargham) and one forthcoming proceedings entry.
   No earlier SciPy, PyData or NumFOCUS-project link was found for cadCAD or the firm. NumFOCUS shows the firm as
   a community sponsor (no level, no date) and Zargham on the advisory council (no start date on that page; his
   CV says 2022). The page can say "advisory council and community sponsor", and that the SciPy 2026 paper is the
   first proceedings entry found, not that the relationship is long-standing from record. Sponsorship or
   maintainership beyond this: nothing found. The supervisor's phrase "longstanding relationship" lacks a page for
   the early years.
8. cadCAD Foundation. Zargham's research page says cadCAD "is now governed by the cadCAD Foundation"; cadcad.org
   does not mention a foundation. One-source statement; the page can omit it.
9. Dates for GDS: the paper is 14 July 2022 (WU); the `gds-core` README says the blog post is 2021; the Reading
   paper is 2021. Use the paper's WU date and the DOI.
10. Counts of citations, downloads or stars: not recorded here (W2's task for the supervisor's work).

## 10. Eight most useful back-links

1. https://arxiv.org/abs/1807.00955 : July 2018 state-space framework, presented at the Ninth International Conference on Complex Systems; the earliest dated formal work.
2. https://github.com/cadCAD-org/cadCAD/blob/master/AUTHORS.txt : who implemented, designed and maintained cadCAD, and who is thanked.
3. https://research.wu.ac.at/de/publications/generalized-dynamical-systems-part-i-foundations/ : GDS Part I, Zargham and Shorish, 14 July 2022, DOI 10.57938/e8d456ea-d975-4111-ac41-052ce73cb0cc.
4. https://github.com/DynamicalSystemsGroup/gds-core : GDS as typed compositional specifications, with credits to Mehta, Zargham, Shorish, McOwen, Hacker.
5. https://hackmd.io/@danlessa/HklBYikEY : the PSuU workflow in eight steps, with the public example models.
6. https://github.com/BlockScience/subspace : a public client-system model whose README states how its work became PSuU.
7. https://arxiv.org/abs/2001.03020 : evidence-based design with data science and stochastic simulation on a real system, with Barlin and Laskowski.
8. https://numfocus.org/community/people : Zargham on the NumFOCUS Advisory Council, with the SciPy 2026 talk at https://pretalx.com/scipy-2026/talk/TBDWJZ/.
