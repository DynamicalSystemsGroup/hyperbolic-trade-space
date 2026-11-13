# WP37 W3: link-to-claim check of site/history.html at the closing unit's head

Date: 2026-11-13. Statuses fetched by `uv run python scripts/check_history_links.py --page` (no credentials):
27 external links, 27 ok, 0 blocked, 0 FAIL. "What the target says" is the record's `shows` for the link's entry
(the target read on 2026-11-12 by the W3 and W4 workers); for the bridge clause the geometric-programming tutorial's
section 2 was read again on 2026-11-13. The sentence kinds are in `trace.md`, generated from the page and the record.

Totals: 29 links on the page's prose; 26 match, 3 partial (reasons below), 0 `no`.

| link | status | what the target says | claim on page | match |
|---|---|---|---|---|
| #record (the generated list) | resolves in the assembled page | the dated reference list that the record renders: the contributors and their dated work | a long-running endeavour with many contributors | yes: points at the list; the "synthesis" reading is the team's account (trace.md) |
| michael.zargham.org | 200 ok | 'In 2017 I founded Dynamical Systems Group (originally BlockScience)'. No page gives a date for the change of name. | founded in 2017 as BlockScience | yes |
| www.dynamicalsystemsgroup.com | 200 ok | The firm's own site, working on dynamical systems 'since 2017'. | now the Dynamical Systems Group | yes |
| doi.org/10.1109/TAC.2013.2293221 | 202 ok | IEEE Transactions on Automatic Control 59(4), April 2014 (Crossref); convex network optimization: this is the convex-optimization work the page links as 'convex optimization (2014)', with the supervis... | Zargham's convex optimization (2014) | yes: convex network optimization, Zargham a co-author |
| paper/ (the site's paper) | resolves in the assembled site (tests/test_site.py links test) | the paper's model is a posynomial frontier; a geometric program has posynomial objective and constraint functions (Boyd, Kim, Vandenberghe, Hassibi, section 2, read 2026-11-13 from web.stanford.edu/~boyd/papers/pdf/gp_tutorial.pdf) | geometric programs, posynomial like this paper's frontier | yes: the lineage step of the bridge clause; the tutorial is entry 2007-gp-tutorial |
| doi.org/10.1109/TCNS.2014.2310911 | 202 ok | IEEE Transactions on Control of Network Systems 1(1), 99-108, March 2014 (Crossref authors); the abstract solves it in polynomial time using geometric programming. 354 citations on Google Scholar (the... | with Preciado, geometric programs for protecting networks against spreading processes (2014) | yes: the abstract names geometric programming; Preciado a co-author. Status 202 is the publisher's bot answer; Crossref gives the record |
| doi.org/10.1007/s41109-020-0254-9 | 200 ok | Applied Network Science, 19 March 2020 (Crossref authors Zhang, Zargham, Preciado); the journal version of 2018-state-space. Control engineering applied to economic networks. | with Preciado and Zixuan Zhang, the 2020 journal version of the 2018 framework | yes |
| github.com/cadCAD-org/cadCAD | 200 ok | The repository was created on 10 September 2018 (first commit 'Create README.md' by Markus Buhatem Koch); MIT license; contributors by commit count Jodesty 731, Koch 74, Bernardineli 37, Mace 17, Scho... | cadCAD | yes |
| github.com/cadCAD-org/cadCAD/blob/master/AUTHORS.txt | 200 ok | The file's own listing, which credits more names than the page's prose names (the prose names the implementer, the three designers and two of the upgrade authors; the file also lists Mace and the than... | implemented by Jodesty, designed by Zargham, Koch and Barlin (2018) | yes: the file's sentence |
| blog.block.science/introducing-complex-adaptive-dynamics-computer-aided-design-cadcad/ | 200 ok | The firm's own origin account of cadCAD, 'By Michael Zargham with Charles Rice', 3 June 2019. An update line says cadCAD was announced as open source at TEGG in Berlin in August 2019 (no separate anno... | introduced in a firm post (2019) | yes: 3 June 2019 |
| research.wu.ac.at/de/publications/generalized-dynamical-systems-part-i-foundations/ | 200 ok | WU Vienna working paper, 14 July 2022, DOI 10.57938/e8d456ea-d975-4111-ac41-052ce73cb0cc: a data structure mapped to itself, maps closed under composition; unifies optimal control, system dynamics, ag... | Shorish co-wrote Generalized Dynamical Systems (2022) | yes |
| www.youtube.com/playlist?list=PLmWm8ksQq4YJrB72Na_JB-o8Xu2JLj7h9 | 200 ok | Playlist of four videos on the firm's channel, uploaded 22 to 31 August 2022, accompanying the paper. No channel or playlist under Shorish's own name was found. | presented it in a video series (2022) | yes: presenter per the firm's post |
| blog.block.science/how-to-perform-parameter-selection-under-uncertainty/ | 200 ok | 'Article by Krzysztof Paruch and Jamsheed Shorish, with edits and suggestions by ...', 8 April 2021: a workflow for iterating multi-dimensional, multi-stakeholder systems with actionable parameter rec... | he and Paruch wrote the parameter selection article (2021) | yes |
| www.youtube.com/watch?v=GK5oRDTa72o | 200 ok | Firm's channel, uploaded 16 December 2024 (83 min): multi-agent influence diagrams as graphs, links to GDS and cadCAD. Workshop 4 is https://www.youtube.com/watch?v=8IGZQDqAWD4. | Penland led workshops on MAIDs, GDS and cadCAD under a contract with BlockScience (2024) | yes for the workshops; the contract clause is the supervisor's account, marked as the team's in trace.md (no source states it) |
| github.com/DynamicalSystemsGroup/gds-core | 200 ok | Created 21 February 2026: typed compositional specifications for Generalized Dynamical Systems; Apache-2.0; preferred citation is the 2022 paper. | Mehta wrote gds-core (2026) | yes |
| github.com/DynamicalSystemsGroup/gds-axelrod | 200 ok | Created 4 March 2026: Axelrod's evolution-of-trust tournament built on the GDS compositional game theory ecosystem; six showcase pages from different GDS representations. | Mehta wrote gds-axelrod (2026) | yes |
| github.com/DynamicalSystemsGroup/MSML | 200 ok | Created 19 May 2023: standardizing mathematical specifications as JSON objects, in line with the firm's research on Generalized Dynamical Systems. Credited by gds-core. | gds-core credits McOwen's MSML (2023) | yes |
| doi.org/10.1007/s10614-023-10445-9 | 200 ok | Computational Economics 64(2), online 28 September 2023 (Crossref): a subpopulation model of a local complementary currency, from transaction data, built in cadCAD. The model's repository says 'develo... | Clark wrote a community-currency model with Mihailov and Zargham (2023), developed with the Red Cross and Grassroots Economics | yes for the work and its partners (the model repository's README); the clause "which applied related methods in modeling, simulation and analysis" is the team's account, marked in trace.md |
| github.com/CarolinaRiascos | 200 ok | Name as her own site gives it, with the handle CarolinaRiascos (her site links the profile); credited by name in dynamical-block-diagrams. No repository of the firm's organisations lists the handle. T... | Riascos-Álvarez (CarolinaRiascos) | partial: shows the handle is hers; the work on client projects is the marked team account |
| numfocus.org/community/people | 200 ok | The NumFOCUS people page lists him under the Advisory Council; his CV dates it 2022 to present. | serves on the NumFOCUS Advisory Council | yes |
| numfocus.org/sponsors | 200 ok | The firm's logo under Community Sponsors; no level and no date on the page (dated by the day read). | the firm is a community sponsor | yes |
| www.youtube.com/watch?v=vr6sIfjGmLQ | 200 ok | PyData channel, uploaded 29 November 2023 (28 min): a robust-control workflow to select the parameters of a pricing algorithm. The description names neither RAI nor any system. | PyData NYC 2023 talk is public | yes |
| pretalx.com/scipy-2026/talk/TBDWJZ/ | 200 ok | The programme page: 17 July 2026; the speaker bio gives 'Chief Engineer at BlockScience'. The proceedings paper is listed as forthcoming on his publications page. | SciPy 2026 talk is public | yes |
| www.dynamicalsystemsgroup.com/partners | 200 ok | The firm's partners page: OpenMBEE is an open source collaborative engineering system; the firm contributes to its technical and ecosystem roadmaps. It does not mention OpenSysML. Dated by the day rea... | the team works with OpenMBEE | partial: covers OpenMBEE, not OpenSysML |
| michael.zargham.org/research | 200 ok | His research page lists the maintainer role. | Zargham a maintainer across OpenSysML | yes |
| github.com/Open-MBEE/OpenSysML | 200 ok | Created 1 August 2026: an open-source SysML v2 implementation in Go. The page names no member of the firm; the role is on 2026-maintainer. | OpenSysML | partial: the link shows the project; the role is on the research page |
| blog.block.science/reviewing-the-fip-0056-and-cdm-debate-on-filecoin/ | 200 ok | 22 March 2023: an independent review at the Filecoin Foundation's request of two competing proposals; 'the debate was conducted publicly on GitHub and Slack'. | a review of two Filecoin proposals (2023), a special case where the work was highly public | yes: the review, at the Filecoin Foundation's request; "debate conducted publicly" |
| zenodo.org/records/10474385 | 200 ok | Zenodo record, CC BY 4.0, published 9 April 2021: the engineering design work by the firm and the system's developers before its launch on 17 February 2021; a controller, parameter selection under unc... | the RAI controller, a highly automated system, design record (2021) | yes |
| michael.zargham.org/cv.pdf | 200 ok | The CV's Selected Talks: 'Crafting Reliable Rules: RAI Case Study. Mathematics for Governance Design Workshop, Edinburgh, Oct 2024.' Also: NumFOCUS Advisory Council Member 2022 to present; Corporate S... | Zargham's talk at a workshop in Edinburgh (ICMS), October 2024 | yes, on the CV alone (no event page found) |

## The record's URLs, the one blocked link and the confirmation

`uv run python scripts/check_history_links.py` over every record URL is run at the final head; its totals are in
`WP37-review.md` (addendum). The one link that answers a bot challenge, https://doi.org/10.1002/iis2.70203 (Wiley), is
listed only in the generated dated list, not in the prose. It was **confirmed by the assistant in a browser**
(2026-11-13): it resolves to the INCOSE International Symposium 2026 article by the supervisor on Wiley Online Library.

## Partial rows and notes

- 2014 TCNS and 2014 TAC: the DOI answers 202 from the publisher; the content is confirmed by Crossref. Not a defect.
- OpenMBEE and OpenSysML: the partners page covers OpenMBEE only and the OpenSysML repository names no member of the
  firm; the role rests on the supervisor's research page (linked as "maintainer across"). Listed, not fixed: the page's
  words claim exactly the role that page states.
- Riascos-Álvarez: the handle is hers (her site); the relation to the firm is the marked team account.
