# WP37 W3: link-to-claim check of site/history.html at the closing unit 2 head

Date: 2026-11-13. Statuses from `uv run python scripts/check_history_links.py --page` (no credentials): every
external link of the prose ok, 0 blocked, 0 FAIL. "What the target says" is the record's `shows` for the link's entry
(read 2026-11-12 and 2026-11-13). Kinds per sentence are in `trace.md`.

Totals: 26 links on the page's prose; 22 match, 2 partial, 2 site-internal (resolve in the assembled site), 0 `no`.

| link | status | what the target says | sentence | match |
|---|---|---|---|---|
| #record | - | - | This page acknowledges the people and the human lineage of this work, which the paper’s citations cannot carry: it is the synthesis and publication of a long-running endeavour with many contributors. | site-internal |
| michael.zargham.org | ok 200 | 'In 2017 I founded Dynamical Systems Group (originally BlockScience)'. No page gives a date for the change of name. | In our own account, this work came from a contract research and engineering firm, founded in 2017 as BlockScience and now the Dynamical Systems Group. | yes |
| www.dynamicalsystemsgroup.com | ok 200 | The firm's own site, working on dynamical systems 'since 2017'. | In our own account, this work came from a contract research and engineering firm, founded in 2017 as BlockScience and now the Dynamical Systems Group. | yes |
| doi.org/10.1109/TAC.2013.2293221 | ok 202 | IEEE Transactions on Automatic Control 59(4), April 2014 (Crossref); convex network optimization: this is the convex-optimization work the page links as 'convex optimization (2014)', with the super... | Before the firm: Zargham’s convex optimization (2014) and, with Victor Preciado, geometric programs, posynomial like this paper’s frontier, for protecting networks (2014). | yes: convex network optimization, Zargham a co-author (Crossref). Status 202 is the publisher's answer |
| paper/ | - | - | Before the firm: Zargham’s convex optimization (2014) and, with Victor Preciado, geometric programs, posynomial like this paper’s frontier, for protecting networks (2014). | site-internal |
| doi.org/10.1109/TCNS.2014.2310911 | ok 202 | IEEE Transactions on Control of Network Systems 1(1), 99-108, March 2014 (Crossref authors); the abstract solves it in polynomial time using geometric programming. 354 citations on Google Scholar (... | Before the firm: Zargham’s convex optimization (2014) and, with Victor Preciado, geometric programs, posynomial like this paper’s frontier, for protecting networks (2014). | yes: the abstract names geometric programming; the clause 'posynomial like this paper's frontier' rests on the paper (link paper/) and the tutorial the paper cites, not an entry. Status 202 is the publisher's answer; Crossref gives the record |
| doi.org/10.1007/s41109-020-0254-9 | ok 200 | Applied Network Science, 19 March 2020 (Crossref authors Zhang, Zargham, Preciado); the journal version of 2018-state-space. Control engineering applied to economic networks. | With Preciado and Zixuan Zhang came the 2020 journal version of the 2018 state-space framework. | yes |
| github.com/cadCAD-org/cadCAD | ok 200 | The repository was created on 10 September 2018 (first commit 'Create README.md' by Markus Buhatem Koch); MIT license. The contributors page lists 19 contributors (counted 19 through the GitHub API... | cadCAD is the work of 19 contributors; its AUTHORS file (2018) credits, among others, Joshua Jodesty, Michael Zargham, Markus Koch, Matthew Barlin, Danilo Bernardineli and Emanuel Lima, and it was introduced in a firm post (2019). | yes |
| github.com/cadCAD-org/cadCAD/graphs/contributors | ok 200 | The repository's contributors page: 19 contributors on GitHub at the time of reading (the same count through the API on 2026-11-12 and 2026-11-13). | cadCAD is the work of 19 contributors; its AUTHORS file (2018) credits, among others, Joshua Jodesty, Michael Zargham, Markus Koch, Matthew Barlin, Danilo Bernardineli and Emanuel Lima, and it was introduced in a firm post (2019). | yes: 19 contributors (API count 2026-11-12 and 2026-11-13) |
| github.com/cadCAD-org/cadCAD/blob/master/AUTHORS.txt | ok 200 | The file's own listing, which credits more names than the page's prose names (the prose names six of them; the file also lists the other active and past contributors and a thanks list of thirteen, ... | cadCAD is the work of 19 contributors; its AUTHORS file (2018) credits, among others, Joshua Jodesty, Michael Zargham, Markus Koch, Matthew Barlin, Danilo Bernardineli and Emanuel Lima, and it was introduced in a firm post (2019). | yes: the file names the six among its credits ('among others') |
| blog.block.science/introducing-complex-adaptive-dynamics-computer-aided-design-cadcad/ | ok 200 | The firm's own origin account of cadCAD, 'By Michael Zargham with Charles Rice', 3 June 2019. An update line says cadCAD was announced as open source at TEGG in Berlin in August 2019 (no separate a... | cadCAD is the work of 19 contributors; its AUTHORS file (2018) credits, among others, Joshua Jodesty, Michael Zargham, Markus Koch, Matthew Barlin, Danilo Bernardineli and Emanuel Lima, and it was introduced in a firm post (2019). | yes |
| research.wu.ac.at/de/publications/generalized-dynamical-systems-part-i-foundations/ | ok 200 | WU Vienna working paper, 14 July 2022, DOI 10.57938/e8d456ea-d975-4111-ac41-052ce73cb0cc: a data structure mapped to itself, maps closed under composition; unifies optimal control, system dynamics,... | Jamsheed Shorish co-wrote Generalized Dynamical Systems (2022) and its video series; he and Kris Paruch wrote the parameter selection article (2021). | yes |
| www.youtube.com/playlist?list=PLmWm8ksQq4YJrB72Na_JB-o8Xu2JLj7h9 | ok 200 | Playlist of four videos on the firm's channel, uploaded 22 to 31 August 2022, accompanying the paper. No channel or playlist under Shorish's own name was found. | Jamsheed Shorish co-wrote Generalized Dynamical Systems (2022) and its video series; he and Kris Paruch wrote the parameter selection article (2021). | yes |
| blog.block.science/how-to-perform-parameter-selection-under-uncertainty/ | ok 200 | 'Article by Krzysztof Paruch and Jamsheed Shorish, with edits and suggestions by ...', 8 April 2021: a workflow for iterating multi-dimensional, multi-stakeholder systems with actionable parameter ... | Jamsheed Shorish co-wrote Generalized Dynamical Systems (2022) and its video series; he and Kris Paruch wrote the parameter selection article (2021). | yes |
| www.youtube.com/watch?v=GK5oRDTa72o | ok 200 | Firm's channel, uploaded 16 December 2024 (83 min): multi-agent influence diagrams as graphs, links to GDS and cadCAD. Workshop 4 is https://www.youtube.com/watch?v=8IGZQDqAWD4. | Andrew “Octopus” Penland led workshops on MAIDs, GDS and cadCAD under a contract with BlockScience (2024). | yes for the workshops; 'under a contract with BlockScience' is the supervisor's account, marked in trace.md |
| github.com/DynamicalSystemsGroup/gds-core | ok 200 | Created 21 February 2026: typed compositional specifications for Generalized Dynamical Systems; Apache-2.0; preferred citation is the 2022 paper. | Rohan Mehta wrote gds-core and gds-axelrod (2026), and gds-core credits Sean McOwen’s MSML (2023). | yes |
| github.com/DynamicalSystemsGroup/gds-axelrod | ok 200 | Created 4 March 2026: Axelrod's evolution-of-trust tournament built on the GDS compositional game theory ecosystem; six showcase pages from different GDS representations. | Rohan Mehta wrote gds-core and gds-axelrod (2026), and gds-core credits Sean McOwen’s MSML (2023). | yes |
| github.com/DynamicalSystemsGroup/MSML | ok 200 | Created 19 May 2023: standardizing mathematical specifications as JSON objects, in line with the firm's research on Generalized Dynamical Systems. Credited by gds-core. | Rohan Mehta wrote gds-core and gds-axelrod (2026), and gds-core credits Sean McOwen’s MSML (2023). | yes |
| github.com/DynamicalSystemsGroup/dynamical-block-diagrams | ok 200 | Created 26 July 2024: formal analysis of the execution and initialization of block diagrams of dynamical systems, with a Julia implementation. The contributors page lists two accounts, 0xekez (11 c... | Zeke Medley, whose summer internship, in our own account, focused on block diagrams as a compositional algebra and the formal methods associated with them, worked with Danilo Bernardineli on Block diagrams of dynamical systems (2024). | yes for the work and Medley (LaTeX source author) and Bernardineli (1 commit); the internship is the supervisor's account, marked 'in our own account' |
| doi.org/10.1007/s10614-023-10445-9 | ok 200 | Computational Economics 64(2), online 28 September 2023 (Crossref): a subpopulation model of a local complementary currency, from transaction data, built in cadCAD. The model's repository says 'dev... | Andrew Clark wrote with Alexander Mihailov and Zargham a community-currency model (2023), developed with the Red Cross and Grassroots Economics, which applied related methods in modeling, simulation and analysis. | yes for the work and its partners; the clause 'which applied related methods...' is the team's account, marked |
| numfocus.org/community/people | ok 200 | The NumFOCUS people page lists him under the Advisory Council; his CV dates it 2022 to present. | Zargham serves on the NumFOCUS Advisory Council. | yes |
| www.dynamicalsystemsgroup.com/partners | ok 200 | The firm's partners page: OpenMBEE is an open source collaborative engineering system; the firm contributes to its technical and ecosystem roadmaps. It does not mention OpenSysML. Dated by the day ... | The team works with OpenMBEE, Zargham as a maintainer across OpenSysML; in our own account, this project is part of a synthesis effort to make our learnings accessible. | partial: covers OpenMBEE only; OpenSysML is the next link, the role the research page |
| michael.zargham.org/research | ok 200 | His research page lists the maintainer role. | The team works with OpenMBEE, Zargham as a maintainer across OpenSysML; in our own account, this project is part of a synthesis effort to make our learnings accessible. | yes |
| github.com/Open-MBEE/OpenSysML | ok 200 | Created 1 August 2026: an open-source SysML v2 implementation in Go. The page names no member of the firm; the role is on 2026-maintainer. | The team works with OpenMBEE, Zargham as a maintainer across OpenSysML; in our own account, this project is part of a synthesis effort to make our learnings accessible. | partial: the repository names no member of the firm; the role is on the research page the clause links as 'maintainer across' |
| zenodo.org/records/10474385 | ok 200 | Zenodo record, CC BY 4.0, published 9 April 2021: the engineering design work by the firm and the system's developers before its launch on 17 February 2021; a controller, parameter selection under ... | In the same account, some projects, the RAI controller among them, were cleared for public release, special cases where the work was highly public: its design record (2021) and Zargham’s talk at a workshop in Edinburgh (ICMS), October 2024. | yes |
| michael.zargham.org/cv.pdf | ok 200 | The CV's Selected Talks: 'Crafting Reliable Rules: RAI Case Study. Mathematics for Governance Design Workshop, Edinburgh, Oct 2024.' Also: NumFOCUS Advisory Council Member 2022 to present; Corporat... | In the same account, some projects, the RAI controller among them, were cleared for public release, special cases where the work was highly public: its design record (2021) and Zargham’s talk at a workshop in Edinburgh (ICMS), October 2024. | yes |

## People audit (2026-11-13): every entry's `people` against its source

Method: authors from Crossref, Zenodo and arXiv by API; contributors from the GitHub API (unauthenticated); pages, README, AUTHORS.txt and LaTeX source fetched with curl; YouTube channel names from oEmbed; the CV by pdftotext. No `gh` CLI, no credentials. Rule: `people` carries who the source credits; where the source is a contributors page, its count is in `shows`.

Of the 43 entries with a people field after the slimming (20 entries were removed, below), 36 match their source and 7 were corrected; one entry lost its person for lack of a byline (2018-nash-lyapunov: the page has no author line, the Medium copy under Zargham's name is not readable now). Person entries: 14, each read against its own page; the shows of four were trimmed of removed entries (Bernardineli, Mehta, Shorish, Paruch) and Medley was added.

| entry | people | what the source shows | result |
|---|---|---|---|
| 2013-traffic-control | Victor Preciado; Michael Zargham; David Sun | arXiv author line: Preciado, Zargham, Sun | corrected: David Sun added |
| 2014-dual-descent | Michael Zargham; Alejandro Ribeiro; Asuman Ozdaglar; Ali Jadbabaie | Crossref authors: Zargham, Ribeiro, Ozdaglar, Jadbabaie | matches |
| 2014-network-protection | Victor Preciado; Michael Zargham; Chinwendu Enyioha; Ali Jadbabaie; George Pappas | Crossref authors: Preciado, Zargham, Enyioha, Jadbabaie, Pappas | matches |
| 2017-founded | Michael Zargham | his homepage and CV: founded 2017 | matches |
| 2018-state-space | Michael Zargham; Zixuan Zhang; Victor Preciado | arXiv author line: Zargham, Zhang, Preciado | matches |
| 2018-cadcad-repo | Joshua Jodesty; Markus Koch; Danilo Bernardineli; Tyler Mace; Benjamin Scholz; Matthew Barlin; Michael Zargham; Zixuan Zhang; Sean McOwen | contributors page, 19 contributors (API 2026-11-12 and 11-13): Jodesty 731, Koch 74, Bernardineli 37, Mace 17, Scholz 14, Lima 4, Barlin 4, Zargham 3, Zhang 2, McOwen 1 and nine more | corrected: was Koch alone ('author of the first commit'); now the contributors a source names, with the count of 19 |
| 2018-authors | Joshua Jodesty; Michael Zargham; Markus Koch; Matthew Barlin; Danilo Bernardineli; Tyler Mace; Emanuel Lima; Zixuan Zhang; Charles Rice; Benjamin Scholz; Andrew Clark | AUTHORS.txt: implemented Jodesty; designed Zargham, Koch, Barlin; upgrades Bernardineli, Mace, Lima; maintainers Lima, Zargham; active and past contributors incl. Zhang, Rice, Scholz; thanks incl. Clark | corrected: Zhang, Rice, Scholz added (named by the file); Zargham and Lima marked maintainers |
| 2019-cadcad-origin | Michael Zargham; Charles Rice | byline 'By Michael Zargham with Charles Rice' | matches |
| 2020-evidence-based | Marek Laskowski; Michael Zargham; Hjalmar Turesson; Matthew Barlin; Danil Kabanov; Eden Dhaliwal | arXiv author line: Laskowski, Zargham, Turesson, Barlin ('Matt'), Kabanov, Dhaliwal | matches |
| 2020-state-space-journal | Zixuan Zhang; Michael Zargham; Victor Preciado | Crossref authors: Zhang, Zargham, Preciado | matches |
| 2020-curved-bonding | Michael Zargham; Jamsheed Shorish; Krzysztof Paruch | Crossref authors: Zargham, Shorish, Paruch | matches |
| 2020-economic-games | Michael Zargham; Krzysztof Paruch; Jamsheed Shorish | Crossref authors: Zargham, Paruch, Shorish | matches |
| 2020-github-org | The cadCAD Team | signed 'The cadCAD Team' | matches (a signature, no individual) |
| 2020-what-and-why | Danilo Bernardineli | YouTube channel 'Danilo Lessa Bernardineli' (oEmbed author name) | matches; source was 'his channel' unverified in the page text |
| 2021-psuu | Krzysztof Paruch; Jamsheed Shorish; Michael Zargham; Danilo Bernardineli; Jeff Emmett; Jessica Zartler | 'Article by Krzysztof Paruch and Jamsheed Shorish, with edits and suggestions by Zargham, Bernardineli, Emmett, Zartler' | matches |
| 2021-machine-search | Danilo Bernardineli | contributors page: danlessa 21, sole contributor | matches |
| 2021-cadcad-jl | Emanuel Lima; Sean McOwen | contributors page: lima-emanuel 45, SeanMcOwen 2, DrCatman 1 | corrected: McOwen added; DrCatman not named (no real name) |
| 2021-rai-design | Michael Zargham; Danilo Bernardineli; Andrew Clark; Jamsheed Shorish; Jeff Emmett | Zenodo creators: Zargham, Bernardineli, Clark, Shorish, Emmett | matches |
| 2021-rai-digital-twin | Danilo Bernardineli | description: 'Danilo, a Senior Engineer at BlockScience'; channel the firm's | matches |
| 2022-gds | Michael Zargham; Jamsheed Shorish | WU record authors Zargham, Shorish | matches |
| 2022-gds-playlist | Jamsheed Shorish; Michael Zargham | playlist title 'Zargham & Shorish'; firm's post gives Shorish for the first video | matches |
| 2023-community-call-26 | Jamsheed Shorish | description: 'Jamsheed Shorish of Block.Science presents' | matches |
| 2022-community-currency-post | Andrew Clark; Alexander Mihailov; Michael Zargham | 'the academic paper by Andrew Clark, Alexander Mihailov, and Michael Zargham' | matches |
| 2022-lima-pydata | Emanuel Lima | description: 'BlockScience Research Engineer Emanuel Lima introduces cadCAD' | matches |
| 2022-formal-methods | Jamsheed Shorish; Michael Zargham | episode title: Shorish and Zargham | matches |
| 2023-fip-0056 | Danilo Bernardineli; Michael Zargham; Jamsheed Shorish; Jakob Hackel; Nick Hirannet; Kelsie Nabben; Jeff Emmett | 'written by Bernardineli, Zargham and Shorish with feedback and edits from Emmett, Hirannet, Nabben and Hackel' | matches |
| 2023-consensus-pledge | Danilo Bernardineli; Jamsheed Shorish; Jakob Hackel | 'written by Bernardineli, Shorish, and Hackel'; Zenodo creators the same | matches |
| 2023-msml | Sean McOwen; Danilo Bernardineli | contributors page: SeanMcOwen 888, danlessa 1 | corrected: Bernardineli (1 commit) added |
| 2023-mbse-post | Michael Zargham; Ilan Ben-Meir | byline 'Michael Zargham & Ilan Ben-Meir' | matches |
| 2023-community-currency | Andrew Clark; Alexander Mihailov; Michael Zargham | Crossref authors: Clark, Mihailov, Zargham | matches |
| 2023-pydata-nyc | Michael Zargham | video title: Michael Zargham | matches |
| 2023-juliacon | Emanuel Lima | pretalx speaker: Emanuel Lima | matches |
| 2024-dynamical-block-diagrams | Zeke Medley; Danilo Bernardineli | contributors page: 0xekez 11, danlessa 1; LaTeX source author line 'Zeke Medley'; README links a write-up by Carolina Riascos | corrected on the supervisor's ruling: Carolina removed; Zeke Medley and Danilo Bernardineli named |
| 2024-maids-post | Andrew Penland | 'Led by Octopus, a Blockscience Research Engineer' | matches (surname from the public record, noted) |
| 2024-workshop-1 | Andrew Penland | description 'Led by Octopus, a Blockscience Research Engineer' | matches |
| 2024-edinburgh | Michael Zargham | CV's Selected Talks entry | matches (the CV, his own) |
| 2025-bdp-lib | Sean McOwen; Danilo Bernardineli | contributors page: SeanMcOwen 161, danlessa 1 | corrected: Bernardineli (1 commit) added |
| 2022-numfocus-council | Michael Zargham | NumFOCUS people page: Advisory Council, Zargham | matches |
| 2026-scipy-talk | Michael Zargham | pretalx speaker: Michael Zargham | matches |
| 2026-maintainer | Michael Zargham | his research page | matches (his own page) |
| 2026-gds-core | Rohan Mehta; Michael Zargham; Jamsheed Shorish; Sean McOwen; Peter Hacker | README credits: author Mehta; theory Zargham and Shorish; architectural inspiration McOwen; contributors Zargham, Hacker | matches |
| 2026-gds-axelrod | Rohan Mehta; Danilo Bernardineli; Michael Zargham | contributors page: Mehta 13, Bernardineli 1, Zargham 1 | matches |
| 2026-incose | Michael Zargham | Crossref author: Zargham (Dynamical Systems Group) | matches |

Removed with their ids (each: what the list no longer did):

- 2007-gp-tutorial: Boyd et al.; the team had nothing to do with it (the supervisor); a reference of the paper, not a step of the lineage
- 2009-newton, 2013-vaccine-allocation: earlier or sibling convex-optimization papers that the 2014 entries already carry; the arc's first entry is now 2013-traffic-control
- 1997-shorish-degree, 2026-backgrounds, 2018-paruch-background: backed only the dropped sentence on the team's backgrounds
- 2019-critical-gap, 2019-tutorials, 2022-gds-post, 2022-crosswalk-part-1: second pointers to a step the list already holds (the origin post, the cadCAD record, the paper and video series)
- 2020-dynamic-games, 2021-interacting-amm, 2026-flexo-rtm, 2026-toaster, 2026-view-editor: exploratory or incidental repositories (no release, no citation, no role in the prose); flexo-rtm and toaster by the supervisor's word
- 2020-quality-metrics, 2022-filecoin-calculator, 2021-insolar: cryptocurrency-setting items beyond the cases the page names, no role in the prose
- 2024-legitimacy, 2024-zenodo-min-max: an attribute post and an unlisted presentation record that no sentence rested on

Added: 2018-cadcad-contributors (the contributors page, link), person-medley.


## The record's URLs

`uv run python scripts/check_history_links.py` over all 69 record URLs at this head (no credentials): 68 ok, 1 blocked
(https://doi.org/10.1002/iis2.70203, the Wiley bot challenge; confirmed in a browser by the assistant on 2026-11-13 as the
supervisor's INCOSE International Symposium 2026 article), 0 FAIL. The cadCAD contributor count was re-made with
unauthenticated `curl` of the GitHub API on 2026-11-13: 19 contributors (21 with anonymous commit authors counted
separately; the contributors page counts 19).
