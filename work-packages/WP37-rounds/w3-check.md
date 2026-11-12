# WP37 W3: independent check of site/history.html (draft at b0386e3)

Checker: Sonnet, edits only this record. Date read: 2026-11-12. Public sources only; GitHub API read without a token.

## 1. Links (26 distinct URLs; HEAD/GET with redirects followed)

Status: all 26 resolve (200; the IEEE DOI ends at 202 on ieeexplore, a bot-challenge response, content exists per Crossref). Match counts: 22 yes, 4 partial, 0 no.

| link | status | what the target says | claim on page | match |
|---|---|---|---|---|
| michael.zargham.org | 200 | "In 2017 I founded Dynamical Systems Group (originally BlockScience)" | founded in 2017 | yes |
| dynamicalsystemsgroup.com | 200 | DSG site, "since 2017" | now the Dynamical Systems Group | yes |
| arxiv 1807.00955 | 200 | "A State-Space Modeling Framework for Engineering Blockchain-Enabled Economic Systems" (Zargham, Zhang, Preciado); abstract on ledger/Byzantine, control framing | 2018 state-space framework tied to control tools | partial: abstract read to its first 700 characters only; "control tools" not seen there; Preciado is a control author |
| github cadCAD | 200 | cadCAD repo | cadCAD simulation | yes |
| wu.ac.at Part I | 200 | "Generalized Dynamical Systems Part I: Foundations", Zargham and Shorish, WU working paper, 14 July 2022 | GDS Part I; Shorish co-wrote | yes |
| gds-core | 200 | "typed compositional specifications for complex systems"; Author Rohan Mehta; Architectural inspiration Sean McOwen (MSML, bdp-lib) | software for GDS; Mehta wrote; credits MSML, bdp-lib | yes |
| arxiv 2001.03020 | 200 | "Evidence Based Decision Making in Blockchain Economic Systems: From Theory to Practice"; "Data Science and Stochastic Simulation and Modelling" | data science with stochastic simulation for design | yes (title carries a banned term; page label does not) |
| hackmd PSuU | 200 | "Parameter Selection Under Uncertainty (PSuU) Information Repo"; no author named; no mention of Subspace | parameter selection under uncertainty | yes for the label; the "grown from" claim rests on the Subspace link |
| BlockScience/subspace | 200 | "A cadCAD Design Digital Twin for Subspace Network Economic Dynamics"; later "adapted to a general workflow ... PSUU" | grown from a published model | yes |
| flexo-rtm | 200 | "Verifiable self-certification oracle for bidirectional requirements traceability of SysMLv2 models" | requirements traceability for SysML v2 models | yes |
| cadCAD AUTHORS.txt | 200 | "originally implemented by Joshua E. Jodesty and designed by Michael Zargham, Markus B. Koch, and Matthew V. Barlin in 2018 ... upgrades ... by Danilo L. Bernardineli, Tyler D. Mace and Emanuel Lima"; maintainers incl. Emanuel Lima; thanks Andrew Clark @aclarkData | Jodesty implemented, Koch designed; Bernardinelli and Lima extended; Lima a listed maintainer; Clark thanked | yes (Koch is one of three designers; page does not say "the" designer; spelling "Bernardineli" in source vs "Bernardinelli" on page) |
| github danlessa | 200 | bio "atmosphere physicist @usponline + research eng @Block_Science", name Danilo Lessa Bernardineli | a physicist, by his profile | yes |
| repec genealogy psh169 | 200 | Shorish, terminal degree 1997, Carnegie Mellon, Tepper economics dept, advisor Stephen Spear | trained in economics | yes (field inferred from department listing) |
| web.archive medium (Paruch) | 200 | author Krzysztof Paruch (username krisparuch); "Having a mathematical background with focus on economic modeling" | Kris Paruch, a mathematician, in his words | partial: he says "a mathematical background with focus on economic modeling", not "a mathematician" |
| doi 978-3-030-53356-4_8 | 200 (Springer) | Crossref: "Economic Games as Estimators", Zargham, Krzysztof Paruch, Shorish | Paruch co-wrote | yes |
| doi TCNS.2014.2310911 | 202 (ieeexplore) | Crossref/arXiv 1309.6270: "Optimal Resource Allocation for Network Protection Against Spreading Processes"; abstract "polynomial time solution ... using Geometric Programming (GP)"; Scholar 354 | a paper using geometric programs, TCNS 2014, 354 citations | yes |
| arxiv 1310.4894 | 200 | "Traffic Control for Network Protection Against Spreading Processes" (2013); abstract "using Geometric Programming (GP)" | paper using geometric programs, arXiv 2013 | yes |
| doi s11081-007-9001-7 | 200 | Crossref: "A tutorial on geometric programming", Boyd, Kim, Vandenberghe, Hassibi, Optimization and Engineering | form of Boyd et al. | yes (that the frontier takes this form is the team's own account) |
| numfocus people | 200 | "He serves on the NumFOCUS advisory council" (under Advisory Council) | serves on the Advisory Council | yes (the fetch summary did not show the name beside the line; the personal site CV also states "2022 - present Advisory Council Member, NumFOCUS") |
| numfocus sponsors | 200 | DSG logo under "Community Sponsors" | the firm is a community sponsor | yes |
| pretalx TBDWJZ | 200 | "Derivations, Not Just Simulations: Teaching Applied Mathematics with Scientific Python", speaker Zargham, "Chief Engineer at BlockScience"; no paper mentioned | SciPy 2026 talk | yes |
| zargham publications | 200 | lists the SciPy 2026 paper (same title) as forthcoming in Proceedings of the 25th Python in Science Conference | paper forthcoming | yes (citation counts are not on this page; Scholar is) |
| dsg partners | 200 | OpenMBEE "an open source collaborative engineering system"; DSG helps shape its technical and ecosystem roadmaps; no mention of OpenSysML | works on and with OpenMBEE | partial: covers OpenMBEE only |
| Open-MBEE/OpenSysML | 200 | open-source SysML v2 implementation in Go; no DSG, BlockScience or Zargham named | works on and with OpenSysML | partial: link shows the project, not the team's role; the role is on michael.zargham.org/research ("OpenMBEE: maintainer since 2026, working across the OpenSysML and Flexo MMS tool ecosystem") |
| github DynamicalSystemsGroup/MSML, bdp-lib | 200 | exist; credited by gds-core README | MSML and bdp-lib of Sean McOwen | yes (the repos sit in the DSG org; the README credit is what ties them to McOwen) |

Re-read of the 354: Google Scholar profile user=bbdc3vkAAAAJ was readable by curl on 2026-11-12; the row "Optimal resource allocation for network protection against spreading processes ... IEEE TCNS 1(1), 99-108, 2014" shows 354 (the "*" marks merged versions). Crossref shows 227 for the same DOI on the same date; the page names Google Scholar, so the figure is backed.

## 2. Sentence kinds

Sentences (S) in order; i = sourced, ii = shown by a link, iii = team's own account.

1. "This method did not come from an academic group." iii, but not marked (the marker "In our own account" opens the next sentence and governs it grammatically).
2. "In our own account, it came from an engineering firm, founded in 2017 as BlockScience and now the Dynamical Systems Group, that did requirements, architecture, design, simulation and analysis for clients, all software-defined, studying the spaces of feasible designs ... adversarial users." iii (marked); the founding year and the rename are i (zargham site). The rebrand is undated, per the decision.
3. "Those systems were highly automated, with much value at risk and multipolar, contentious sponsorship ... legitimacy bearing on outcomes." iii, but NOT marked: it follows a marked sentence yet is a separate sentence, and the decisions record says the page states that the list is the supervisor's account. FLAG (minor).
4. "Public work shows the rest: ..." ii for each linked item. Three links show less than the clause says: "tied to control tools" (1807.00955, not seen in abstract), "grown from a published model" rests on the Subspace README (yes), "studying the spaces of feasible designs" is not shown by any link. FLAG (minor): "tied to control tools" unverified beyond the abstract's first lines.
5. Credit paragraph: Jodesty/Koch; Bernardinelli physicist, Lima maintainer; Shorish economics, co-wrote Part I; Paruch "a mathematician, in his words"; co-wrote Economic Games; Mehta/gds-core/McOwen; Clark thanked. i throughout. FLAG: "a mathematician, in his words" is not his word; he writes "a mathematical background with focus on economic modeling". FLAG (minor): the page says Koch "designed it" while AUTHORS.txt lists three designers (Zargham, Koch, Barlin); true but partial, and Barlin goes uncredited.
6. "With thanks also to Jakob Hackel and Andrew 'Octopus' Penland." Neither kind: no public source ties either name to the work (w1 and w2 both record nothing public for them). FLAG: a thanks with no source is the supervisor's own addition; it is neither i, ii nor a marked iii. Needs the supervisor's mark or a source. Note the supervisor named them, so it may stand if the page marks it as the team's thanks.
7. "Control, economics, physics, mathematics: what a convex program, elasticities, a frontier and an estimator rest on." Part i (backgrounds: control engineer is stated nowhere for a named person on the credit line; physics = Bernardinelli, economics = Shorish, mathematics = Paruch's background); the "what ... rest on" mapping is the team's own account and unmarked. FLAG: "control" and the mapping are unsourced on the page; computer science (in the supervisor's list) is omitted.
8. "Zargham's record is in optimization and control: two papers using geometric programs, ..." i/ii, backed (both abstracts say GP; the 2014 count backed by Scholar read today).
9. "the form of Boyd et al. is the one this method's frontier takes." iii, unmarked, about the method (the model's GGP compatibility is in the repo docs, not on this page). Not a source claim; minor flag.
10. "He serves on the NumFOCUS Advisory Council, the firm is a community sponsor, and his SciPy 2026 talk has a paper forthcoming." i, all backed. "SciPy 2026 talk": pretalx has the talk page; whether it was delivered is not claimed.
11. "This package is a scikit-learn-conformant estimator by design." ii (the repo), unmarked as team account; fine.
12. "Today the team works on and with OpenMBEE and OpenSysML; this project is part of a synthesis effort ..." OpenMBEE: i (partners page). OpenSysML: i via the supervisor's research page, not via the linked page (partial). Synthesis effort: iii, the supervisor's statement, unmarked.
13. "With computers, fast but with confidence." the supervisor's phrase, iii.

Verified claims asked about: Jodesty implemented / Koch designed: true, AUTHORS.txt (with two co-designers). Bernardinelli physicist: "atmosphere physicist" in his GitHub bio. Shorish economics: RePEc Genealogy lists the Tepper economics department, 1997. Paruch: author Krzysztof Paruch (page uses "Kris", the username is krisparuch), mathematical background in his words (partial). Founded 2017: zargham site first-person CV; DSG site says "since 2017". 354 citations: re-read today on Scholar. NumFOCUS Advisory Council and community sponsor: backed. SciPy talk and paper forthcoming: backed (publication title identical). Mehta/McOwen: gds-core README credits, backed.

## 3. Vocabulary

Visible words and link labels checked for cryptocurrency, crypto, token, tokenomics, blockchain, smart contract, web3, DAO, DeFi, NFT, mining, ledger: no hits (the only substring hit is "software-defined", which contains "defi"). Banned terms occur only in link targets: the archive URL (crypto3conomics, token-engineering), the titles of arXiv 1807.00955 and 2001.03020 at their targets, and the Subspace repo README, none on the page.

## 4. Private material

GitHub API without a token: cadCAD-org/cadCAD, DynamicalSystemsGroup/gds-core, MSML, bdp-lib, flexo-rtm, BlockScience/subspace, Open-MBEE/OpenSysML all return 200; users/danlessa 200. No link targets a non-public repository.

## 5. Slow tests

`uv run pytest tests/test_site.py -k "history or assembled" -q`: 8 passed, 47 deselected, 620.57 s (10:20).

## Flags summary

1. "a mathematician, in his words": his words are "a mathematical background with focus on economic modeling". Narrow the label or the wording.
2. Hackel and Penland thanked with no public source; mark as the team's own thanks or drop.
3. Sentence 3 (attributes) unmarked as the team's account.
4. "tied to control tools" not shown at the link; "studying spaces of feasible designs" shown by no link.
5. OpenSysML: the linked page does not show the team's role; the research page does (add it or leave to the team's account).
6. "Control" and the background-to-method mapping are unsourced; computer science omitted.
7. Koch is one of three designers (Zargham, Koch, Barlin); Barlin not credited; Bernardinelli spelled Bernardineli in AUTHORS.txt and "Lessa Bernardineli" on GitHub (check the preferred spelling).
