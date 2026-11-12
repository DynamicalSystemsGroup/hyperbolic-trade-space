# WP37 worker W2: the people

Research record for the history and acknowledgements page. Public sources only; every attribution below was read on
the page named and is quoted briefly, never inferred. **Date read for every URL: 2026-11-12.** Where the public record
does not state something the cell is blank or says "not stated". Nothing here is page text.

## Method, limits, and one disclosure

- Sources used: public GitHub repositories and their public contributor lists (read through the GitHub API), the files
  `AUTHORS.txt` and README credit sections, the firm's public site and blog, the supervisor's personal site, Crossref,
  OpenAlex, Google Scholar, RePEc, and the Internet Archive copies of public blog posts (the blog host refuses direct
  requests).
- **Disclosure.** The GitHub tooling in this session is authenticated as the supervisor, so some searches surfaced
  repositories of the Dynamical Systems Group organisation that are private (for example a knowledge base, a
  personal-notes archive and an internal exploration repository). Those hits named two of the eleven (Jakob Hackel,
  "Octopus"). I excluded everything read there: no claim below rests on a private repository, and the two people are
  recorded as thin for that reason. Repository visibility was checked (`private: false`) for every repository cited
  below.
- Contribution counts are GitHub contributor-list commit counts at the date read; they show who committed, not
  who designed. The page should cite roles only from the sentence a source states (marked "states").
- Register: source titles are quoted as they are even where a title carries vocabulary the page will not use; the
  page's own words need not. Those titles are flagged in the last section.
- The supervisor's spelling "Bernardinelli": the sources spell it **Bernardineli** (`AUTHORS.txt`) and the GitHub
  profile name is "Danilo Lessa Bernardineli". The page's spelling is the supervisor's to settle.

## 1. The history in the sources (the spine the people attach to)

| When | What the source says | URL (read 2026-11-12) |
|---|---|---|
| 2013-2014 | The supervisor's optimization and control papers (section 4). | see section 4 |
| 2017 | The firm states it has taken dynamical systems "from theory to practice since 2017" (Dynamical Systems Group site, home and About). | https://www.dynamicalsystemsgroup.com ; https://www.dynamicalsystemsgroup.com/about |
| 2018 | cadCAD "originally implemented by Joshua E. Jodesty and designed by Michael Zargham, Markus B. Koch, and Matthew V. Barlin in 2018"; later "upgrades and improvements" by Danilo L. Bernardineli, Tyler D. Mace and Emanuel Lima (`AUTHORS.txt`). The repository's first-created date is 2018-09-10. | https://raw.githubusercontent.com/cadCAD-org/cadCAD/master/AUTHORS.txt ; https://github.com/cadCAD-org/cadCAD |
| 2018-07-03 | arXiv:1807.00955, "A State-Space Modeling Framework for Engineering Blockchain-Enabled Economic Systems", Zargham, Zhang, Preciado: a dynamical-systems framework "connect[ed] to control engineering tools, such as Lyapunov-like functions" (abstract, as summarised by the page). The earliest formalization the sources show. | https://arxiv.org/abs/1807.00955 |
| 2019-06-03 | Medium post "Introducing Complex Adaptive Dynamics Computer-Aided Design (cadCAD)", "By Michael Zargham with Charles Rice"; an update line says the project was announced as open source at TEGG in Berlin in August 2019. | https://web.archive.org/web/2022/https://medium.com/block-science/introducing-complex-adaptive-dynamics-computer-aided-design-cadcad-38b63b541eb8 |
| 2019-06-12 | "cadCAD: Filling a Critical Gap in Open-Source Data Science", "By Michael Zargham and Jonathan Gabler"; says cadCAD "is built as part of the scientific Python ecosystem" and brings "generalized dynamical systems and event-based differential games" to it. | https://web.archive.org/web/2022/https://medium.com/block-science/cadcad-filling-a-critical-gap-in-open-source-data-science-fcd0d3faa8ed |
| 2019-2020 | `cadCAD-org` organisation repositories: tutorials (2019-01-09), demos (2020-07-08), `DynamicGamesSeminar` (2020-05-23, "course materials on dynamic games"), `governance` (2020-07-03). | https://github.com/cadCAD-org |
| 2020 | Laskowski, Zargham, Turesson, Barlin, Kabanov, Dhaliwal, "Evidence Based Decision Making in Blockchain Economic Systems: From Theory to Practice": "combines data science and stochastic simulation"; process reveals system-level behaviours "before deployment" (abstract, summarised). arXiv:2001.03020, submitted 2020-01-08. | https://arxiv.org/abs/2001.03020 |
| 2020 | Zargham, Shorish, Paruch, "From Curved Bonding to Configuration Spaces" (IEEE ICBC, May 2020) and "Economic Games as Estimators" (Springer, 2020). Authors read from Crossref. | https://doi.org/10.1109/ICBC48266.2020.9169474 ; https://doi.org/10.1007/978-3-030-53356-4_8 |
| 2021-02 | `cadCAD_machine_search`, "Using cadCAD for performing machine search on optimal hyper-surfaces" (created 2021-02-02; one contributor, `danlessa`, 21 commits). | https://github.com/cadCAD-org/cadCAD_machine_search |
| 2021-04-08 | PSUU: the firm's post "How to Perform Parameter Selection Under Uncertainty", byline "BlockScience" (no personal author): "a workflow for scientifically iterating multi-dimensional, multi-stakeholder systems", six steps (goals, control parameters, environmental parameters, metrics, simulation, optimal parameter selection). | https://web.archive.org/web/2022/https://medium.com/block-science/how-to-perform-parameter-selection-under-uncertainty-976931ba7e5d |
| 2021 | `interacting-amm-model` (cadCAD-org, created 2021-07-28; `danlessa` 15 commits), a public model a web-search summary describes as going through the full PSUU process (not verified by me by reading its README). | https://github.com/cadCAD-org/interacting-amm-model |
| 2022-07-14 | "Generalized Dynamical Systems Part I: Foundations", Zargham and Shorish, WU Vienna Research Institute for Cryptoeconomics working paper, DOI 10.57938/e8d456ea-d975-4111-ac41-052ce73cb0cc. The abstract (summarised): a data structure maps to itself and such mappings compose; unifies optimal control, system dynamics, agent-based modelling and networks; "the two follow-up parts cover applications and a software implementation using cadCAD". A Medium listing dates a blog version 2022-08-29 (listing seen in search results, post not opened). The `gds-core` README gives the year 2021 for the same work: the sources disagree. | https://research.wu.ac.at/en/publications/generalized-dynamical-systems-part-i-foundations/ ; https://doi.org/10.57938/e8d456ea-d975-4111-ac41-052ce73cb0cc |
| 2022-2026 | `DynamicalSystemsGroup/cats`, `MSML`, `bdp-lib` and others (section 3 shows who committed). | https://github.com/DynamicalSystemsGroup |
| 2026-02-21 | `gds-core`: "Generalized Dynamical Systems: typed compositional specifications for complex systems", Apache-2.0; packages include `gds-analysis` ("reachability, and `gds_analysis.psuu` parameter search") and the deprecated `gds-psuu`. Credits section quoted in section 2. | https://github.com/DynamicalSystemsGroup/gds-core |
| 2026-10/11 | The firm's SysML v2 and OpenMBEE work (section 3 below). | |

The proof-of-theorem thread the supervisor named (theorems about algorithms) is not covered by the sources above
beyond the GDS paper's differential-inclusion results and the lemma-script style of `sympy-proof`
(https://github.com/DynamicalSystemsGroup/sympy-proof, created 2026-04-09, "Pythonic proof authoring assistant"); no
public source I read states an early theorem-proving engagement for a client. The page should say less there.

## 2. The eleven: works, attributions, backgrounds

Columns: person | public works bearing on the history (URL; what it says; the quoted words are the source's) | public
background (URL; the source's words) | thin-record notes.

| Person | Public works bearing on the history | Public background | Thin-record notes |
|---|---|---|---|
| **Markus Koch** (sources: Markus B. Koch / Markus Buhatem Koch, GitHub `markusbkoch`) | `AUTHORS.txt` **states** "designed by Michael Zargham, Markus B. Koch, and Matthew V. Barlin in 2018" and lists him among active and past contributors (https://raw.githubusercontent.com/cadCAD-org/cadCAD/master/AUTHORS.txt). Contributor list of cadCAD: 74 commits, second after `JEJodesty` 731 (https://github.com/cadCAD-org/cadCAD). Also 72 commits in `cadCAD-Tutorials` (https://github.com/cadCAD-org/cadCAD-Tutorials, created 2019-01-09) and 27 in `demos` (https://github.com/cadCAD-org/demos). GitHub profile shows name "Markus Buhatem Koch", no bio (https://github.com/markusbkoch). | Not stated by a public primary source. (A third-party org-chart page, https://theorg.com/org/blockscience/org-chart/markus-buhatem-koch, marked "Unverified", calls him a Research Advisor with a data-science career; not relied on.) | Role in 2018 design is stated; no paper, talk or post of his found. Background blank. |
| **Danilo Bernardinelli** (sources: Danilo L. Bernardineli / Danilo Lessa Bernardineli, `danlessa`) | `AUTHORS.txt` **states** later "upgrades and improvements were further committed by Danilo L. Bernardineli, Tyler D. Mace and Emanuel Lima" and lists him as active and past contributor. Commits (public repos): `cadCAD` 37, `cadCAD-legacy-devel` 57, `demos` 34, `snippets` 39, `cadCAD-tools` 28, `cadCAD_machine_search` 21 (sole contributor), `cadCAD_diagram` 18, `interacting-amm-model` 15 (sole contributor), `cadcad-ri` 10 (https://github.com/cadCAD-org/cadCAD_machine_search ; https://github.com/cadCAD-org/interacting-amm-model). The PSUU hackmd page by `danlessa` links "First internal implementation of the PSuU methodology" (https://hackmd.io/@danlessa/HklBYikEY; the page names no author or date). Later: `bicycling-energy-model` 223 commits (https://github.com/DynamicalSystemsGroup/bicycling-energy-model). A listing in search results gave him the title "Senior Engineer, Computational Science, Complex Systems Modeling" (secondary; not relied on). | GitHub profile bio: "atmosphere physicist" and "research eng" at the firm (https://github.com/danlessa). | Strongest public trail of the PSUU tooling (machine search, the AMM model). The PSUU method's authorship is not stated by any source I read; the Medium post is bylined to the firm. |
| **Rohan Mehta** (GitHub `rororowyourboat`, profile name "Rohan Mehta") | `gds-core` README **states** "Author: Rohan Mehta, Dynamical Systems Group" (credits section) (https://github.com/DynamicalSystemsGroup/gds-core); 466 commits there. `Open-MBEE/sysml_view_editor`: 78 commits, sole contributor, "browser-based SysML v2 editor with source-defined views..., powered by OpenSysML and SysML Toolkit" (https://github.com/Open-MBEE/sysml_view_editor). Also `gds-axelrod` 13 ("Interactive Evolution of Trust showcase", https://github.com/DynamicalSystemsGroup/gds-axelrod), `mbse_skills`, `awesome-sysmlv2-mbse`, `sysml-concept-reference`, `openmbee-grokking-talk` (https://github.com/DynamicalSystemsGroup/openmbee-grokking-talk). | GitHub profile: "Data Scientist, Researcher", company "Chaos Coded Systems" (https://github.com/rororowyourboat); the consultancy's site says "Rohan architects the systems" (https://chaoscoded.com). A discipline (degree, field) is not stated. | Strong for the 2026 GDS software and the OpenMBEE editor; nothing public before 2026 found. Background blank as to discipline. |
| **Joshua Jodesty** (Joshua E. Jodesty, `JEJodesty`) | `AUTHORS.txt` **states** cadCAD was "originally implemented by Joshua E. Jodesty". Most commits of any contributor: `cadCAD` 731 commits, the most of any contributor (https://github.com/cadCAD-org/cadCAD), `documentation` 11 (https://github.com/cadCAD-org/documentation), `cadCAD-Tutorials` 23. Later `DynamicalSystemsGroup/cats` 485 ("cats", created 2022-01-04, https://github.com/DynamicalSystemsGroup/cats) and the `koi-net` family. GitHub profile: company "BlockScience", Brooklyn, NY (https://github.com/JEJodesty). | Not stated (profile bio "Focusing"; no field). | Implementation credit is stated and the commit record matches it. Background blank. |
| **Jamsheed Shorish** (`jshorish`) | Co-author, with Zargham, of "Generalized Dynamical Systems Part I: Foundations" (WU Vienna working paper, 2022-07-14) (https://research.wu.ac.at/en/publications/generalized-dynamical-systems-part-i-foundations/); `gds-core` README: "Theoretical foundation: Dr. Michael Zargham and Dr. Jamsheed Shorish" (https://github.com/DynamicalSystemsGroup/gds-core). Co-author of "From Curved Bonding to Configuration Spaces" (IEEE ICBC 2020, https://doi.org/10.1109/ICBC48266.2020.9169474) and "Economic Games as Estimators" (Springer 2020, https://doi.org/10.1007/978-3-030-53356-4_8), and with Matt Stephenson of "A Practical Theory of Fungibility" (WU working paper, https://ideas.repec.org/e/psh169.html). Co-author contributor to `cadCAD-org/DynamicGamesSeminar` (2 commits, https://github.com/cadCAD-org/DynamicGamesSeminar). | Economics: terminal degree 1997, Department of Economics, Tepper School of Business, Carnegie Mellon (RePEc Genealogy, https://genealogy.repec.org/pages/psh169.html; RePEc profile https://ideas.repec.org/e/psh169.html lists Shorish Research, Leuven, and WU Vienna affiliations). | Well sourced. |
| **Kris Paruch** (Krzysztof Paruch) | Co-author, with Zargham and Shorish, of "From Curved Bonding to Configuration Spaces" (IEEE ICBC, May 2020) and "Economic Games as Estimators" (Springer, 2020); authors read from Crossref (https://doi.org/10.1109/ICBC48266.2020.9169474 ; https://doi.org/10.1007/978-3-030-53356-4_8). Talk "Social Choice, Parameter Selection and Optimization", EthCC[7], 2024-07-10: "novel theoretical results in multistakeholder decision making and system optimization" (https://ethcc.io/archive/Social-Choice-Parameter-Selection-and-Optimization); his current affiliation on the conference site is Token Engineering Labs GmbH (https://ethcc.io/speakers/krzysztof-paruch). | His own 2018 post: "Having a mathematical background with focus on economic modeling" (https://web.archive.org/web/2022/https://medium.com/crypto3conomics/token-engineering-from-an-economic-perspective-b6c464f20241, dated 2018-11-06, published in the WU Vienna lab's blog). | No public page I read states his employment at the firm or the dates; the link to the firm is the two co-authored papers and the talk. A page claim should be "co-author", not "member". |
| **Andrew "Octopus" Penland** | **No public source found that connects "Octopus" to a name, or states a role.** Public commits authored "Andrew Penland" (2024-04-20 to 2024-05-08, many commits, e.g. "Temporary adjustment to psuu run sweep default parameters", 2024-05-02) in the repository `jackhack00/aztec-gddt`, a cadCAD model repository for a public project ("Aztec Granular Design Digital Twin" is the firm's repository name) (https://github.com/jackhack00/aztec-gddt, example commit https://github.com/jackhack00/aztec-gddt/commit/1ce3520844554a1f5220e1bbe351eed54cbe2ad3). A firm social-media post reads "Thanks Octopus for surfacing" (search listing https://oauth.lightnews.app/bsky/blockscience.bsky.social), no name. | Not stated in any public source read. | **Thin.** The commits show a person named Andrew Penland worked on the PSUU sweep of that model in a fork; they do not say he is the "Octopus", and the fork's owner account (`jackhack00`) has no profile name. The page can name him only as the supervisor's list does, with no work attributed beyond what the supervisor adds, unless the supervisor supplies a public source. |
| **Jakob Hackel** | **Nothing public found** (web search; code search of public repositories; the contributor lists of the 70-odd public repositories of the firm's organisation). | Not stated. | **Thin: no public source.** Do not attribute anything. |
| **Emanuel Lima** (`lima-emanuel`, GitHub profile name "Emanuel Lima", Fortaleza) | `AUTHORS.txt` **states** "upgrades and improvements" by him and lists him as **current project maintainer** with Zargham (https://raw.githubusercontent.com/cadCAD-org/cadCAD/master/AUTHORS.txt). Commits: `cadcad-ri` ("The Reference Implementation", created 2021-12-30) 58 (https://github.com/cadCAD-org/cadcad-ri), `CadCAD.jl` ("cadCAD implementation in Julia", 2021-05-14) 45 (https://github.com/cadCAD-org/CadCAD.jl), `snippets` 9, `cadCAD` 4 (2024-04-11 to 2024-04-19 among them). | Not stated (GitHub bio blank). | Maintainer role stated; background blank. (Search engines returned other people of the same name; none was tied to the firm.) |
| **Andrew Clark** (`aclarkData`) | `AUTHORS.txt` lists him under "We'd also like to thank" (https://raw.githubusercontent.com/cadCAD-org/cadCAD/master/AUTHORS.txt). First author of "Complex Systems Modeling of Community Inclusion Currencies" with Alexander Mihailov and Zargham, *Computational Economics* 64(2), published online 2023-09-28 (https://doi.org/10.1007/s10614-023-10445-9; authors read from Crossref); the model repository: `Community_Inclusion_Currencies` (10 commits, https://github.com/DynamicalSystemsGroup/Community_Inclusion_Currencies). Also `cadCAD-org/demos` 7 and `DynamicGamesSeminar` 2 commits. | Not stated by a source I could open (the publisher page refused automated reading; the GitHub profile gives only "Richmond, VA"). | Thanked and a co-author; background blank. |
| **Sean McOwen** (`SeanMcOwen`) | `gds-core` README credits "Architectural inspiration: Sean McOwen, MSML and bdp-lib" (https://github.com/DynamicalSystemsGroup/gds-core). `MSML` (created 2023-05-19) 888 commits, `bdp-lib` 161, `MSML-Template` 95 (https://github.com/DynamicalSystemsGroup/MSML ; https://github.com/DynamicalSystemsGroup/bdp-lib). `cadCAD-org/uniswap_digital_twin` 34 commits, 2021-07 to 2021-09 (https://github.com/cadCAD-org/uniswap_digital_twin). Appears once in the cadCAD contributor list (https://github.com/cadCAD-org/cadCAD). | Not stated (profile blank). | Strong commit record for the specification-language work (MSML) the GDS software credits as inspiration. Background blank. |

### The supervisor's point on backgrounds (control engineers, economists, physicists, mathematicians, computer scientists)

What the public sources state, field by field:

| Field | Who the source states it for | Source |
|---|---|---|
| Control and optimization (electrical and systems engineering) | Michael Zargham: Ph.D. Electrical and Systems Engineering, University of Pennsylvania, "robust control and optimal resource allocation policies in distributed systems" | https://www.dynamicalsystemsgroup.com/leadership |
| Economics | Jamsheed Shorish (economics terminal degree, Carnegie Mellon, 1997) | https://genealogy.repec.org/pages/psh169.html |
| Physics | Danilo Bernardineli ("atmosphere physicist", his GitHub bio) | https://github.com/danlessa |
| Mathematics (with economic modelling) | Kris Paruch (his own words, 2018) | link in his row |
| Computer science | **No source states it as a discipline for anyone on the list.** Roles are stated ("Data Scientist, Researcher" for Mehta; the commit record for Jodesty, McOwen, Lima, Koch) but a degree or field is not. | none |

So the sources back four of the five fields for four people; "computer scientists" is true only as the roles the commit
record shows. The page can state the mix as the supervisor said it only if he vouches for the rest; otherwise it
names the four. The firm's COO is a mechanical engineer by training (https://www.dynamicalsystemsgroup.com/leadership),
which is outside the supervisor's list of five but is on the public leadership page.

## 3. The firm's current work on and with OpenMBEE and OpenSysML (public)

| What | Source (read 2026-11-12) | Says |
|---|---|---|
| Role in OpenMBEE | https://www.dynamicalsystemsgroup.com/partners | "DSG contributes to the technical and ecosystem development roadmaps, bringing research and systems-integration expertise." |
| Supervisor's role | https://www.dynamicalsystemsgroup.com/leadership | Zargham "helps set the technical roadmap and ecosystem direction for OpenMBEE, the open-source MBSE platform, including Flexo MMS"; "serves on the NumFOCUS advisory council". |
| Personal site | https://michael.zargham.org/research.html | Lists a maintainer role "working across the OpenSysML and Flexo MMS tool ecosystem" and "originator and lead architect since 2017" for cadCAD (the page's words, read via a summary; confirm by reading before quoting). |
| OpenMBEE is a NumFOCUS project | https://www.openmbee.org (navigation: "NumFOCUS Project") and https://www.openmbee.org/about | OpenMBEE "is an open source collaborative engineering system"; the About page carries the NumFOCUS notice. |
| `Open-MBEE/toaster` | https://github.com/Open-MBEE/toaster (created 2026-09-25) | "An executable tutorial on recursive system decomposition using SysML v2 and OpenSysML." Contributor list: `mzargham` 795 commits (sole). |
| `Open-MBEE/sysml_view_editor` | https://github.com/Open-MBEE/sysml_view_editor | Browser-based SysML v2 editor with source-defined views, "Powered by OpenSysML and SysML Toolkit"; sole contributor `rororowyourboat` (Rohan Mehta's account), 78 commits. |
| `Open-MBEE/OpenSysML` | https://github.com/Open-MBEE/OpenSysML | "Open Source SysML v2 Implementation in Go". Contributors listed are others; DSG's commit share there is not shown (not claimed). |
| Org membership | https://github.com/orgs/Open-MBEE/people | `mzargham` and `rororowyourboat` are public members. |
| DSG repositories | https://github.com/DynamicalSystemsGroup/flexo-rtm ("Verifiable self-certification oracle for bidirectional requirements traceability of SysML v2 models", v0.1.0-rc1); `flexo-rtm-research`; `flexo-mms-deployment` ("Example docker compose and k8s files for deployment of Flexo MMS services"); `mbse_skills`; `awesome-sysmlv2-mbse`; `sysml-concept-reference`; `ADCS-lifecycle-demo` ("Requirements Traceability including evidence records (structural, symbolic and numeric)") | Public, created 2025-12 to 2026-10. |
| Talk | https://dynamicalsystemsgroup.github.io/openmbee-grokking-talk/ (repo https://github.com/DynamicalSystemsGroup/openmbee-grokking-talk, created 2026-10-23) | "Continuous analysis with the Flexo Change Adapter" (slides). |
| Demonstrations | https://dynamicalsystemsgroup.github.io | Four hosted demos, the first "Bidirectional requirements traceability for a satellite attitude-determination and control system" (the ADCS demo). |

The scientific-computing relationships the supervisor named: the NumFOCUS advisory council role and OpenMBEE as a
NumFOCUS project are stated above; the SciPy 2026 proceedings talk "Derivations, Not Just Simulations: Teaching
Applied Mathematics with Scientific Python" (video https://youtu.be/EV5ycMqQoDI, slides
https://mzargham.github.io/hc-marimo/slides/) is listed on https://michael.zargham.org/publications.html, marked
forthcoming. The firm's OpenTeams partnership (https://www.dynamicalsystemsgroup.com/partners) is stated as
well. A PyData engagement was not found.

## 4. The supervisor's own public account

**His website:** https://michael.zargham.org (found from the GitHub profile `mzargham`, field "Website/blog"; the same
profile links ORCID https://orcid.org/0000-0001-5279-690X, Google Scholar
https://scholar.google.com/citations?user=bbdc3vkAAAAJ, LinkedIn `in/mczargham`). Title: "Michael C. Zargham, Ph.D. |
CEO and Chief Engineer, Dynamical Systems Group". Sub-pages: https://michael.zargham.org/research.html,
https://michael.zargham.org/publications.html, a CV PDF (`cv.pdf`).

**Arc and register** (read from the home and research pages; summary mine):
- The home page opens with a one-line promise, "Where mathematical models become operational commitments", then
  walks three stages in order: networked optimization at Penn (the 2014 dissertation era), economic and institutional
  systems at his firm, and current work on systems engineering and assurance (SysML v2, formal and executable
  specifications), with the Dynamical Systems Group as the vehicle. It then lists current roles, teaching and
  research affiliations, education and contact.
- The research page traces one question across the three: how "simple, local behavior adds up to dependable
  behavior", then how structure shapes emergent behaviour and how to keep it within bounds when objectives are unknown,
  then "what assurances should be required" and showing with traceable evidence and a named accountable person that a
  system meets its requirements.
- Register: first person, measured, plain declarative sentences, little hype; academic rigour (citations, theory)
  beside practitioner detail (production systems, prototypes, talks); self-aware about scope (it separates simulation
  from deployment and notes proprietary work). The three sub-sections are anchored `#networks`, `#institutions`,
  `#assurance`.
- Words about the work in the page's own terms: cadCAD "originator and lead architect since 2017"; the GDS paper is
  listed by its spelled-out title only; geometric programming and PSUU do not appear on the site.

**Publications in optimization and control and the cited work that uses geometric programs.** Counts are as each
index states them; **dates read 2026-11-12**. The two papers below say "geometric program (GP)" and use posynomials
(read in the arXiv full texts: "solved in polynomial time using Geometric Programming (GP)"; the posynomial form,
convex in log scale); neither full text uses the words "generalized geometric program". The supervisor's term GGP
is the log-convex form these programs have; the page should say "geometric program" unless he wants the other term.

| Paper | Venue, year | Google Scholar (his profile) | OpenAlex | Crossref | Links |
|---|---|---|---|---|---|
| "Optimal Resource Allocation for Network Protection Against Spreading Processes" (Preciado, Zargham, Enyioha, Jadbabaie, Pappas) | IEEE Transactions on Control of Network Systems 1(1), 99-108, March 2014 | **354** | 274 | 227 | DOI https://doi.org/10.1109/TCNS.2014.2310911 ; arXiv https://arxiv.org/abs/1309.6270 (abstract: "both ... can be solved in polynomial time using Geometric Programming (GP)") |
| "Traffic Control for Network Protection Against Spreading Processes" (Preciado, Zargham, Sun) | arXiv:1310.4894, submitted 2013-10-18; no journal reference listed | **7** | 4 | not indexed | https://arxiv.org/abs/1310.4894 (abstract names GP) |

Other highly cited optimization and control papers on his Scholar profile (all dates read 2026-11-12; Scholar page
https://scholar.google.com/citations?user=bbdc3vkAAAAJ shows 1,664 total citations, h-index 19, i10-index 24):

| Paper | Venue, year | Scholar count | Notes |
|---|---|---|---|
| "Optimal vaccine allocation to control epidemic outbreaks in arbitrary networks" | IEEE CDC 2013 (https://doi.org/10.1109/CDC.2013.6761078; arXiv https://arxiv.org/abs/1303.3984) | 230 (Crossref 120) | Abstract: "a convex framework"; **does not name a geometric program**, so not counted above. |
| "Accelerated dual descent for network flow optimization" | IEEE Transactions on Automatic Control 59(4), 905-920, 2014 (https://doi.org/10.1109/TAC.2013.2293221) | 184 | Convex network optimization. |
| "A distributed Newton method for network optimization" | IEEE CDC 2009 (https://doi.org/10.1109/CDC.2009.5400289) | 120 | Convex network optimization. |
| "Traffic optimization to control epidemic outbreaks in metapopulation models" | IEEE GlobalSIP 2013 | 35 | Not read for GP. |
| "Accelerated backpressure algorithm" | IEEE GLOBECOM 2013 | 34 | Not read for GP. |
| "A convex framework to control spreading processes in directed networks" | CISS 2014 | 17 | Not read for GP. |

Post-2017 control-flavoured work cited by the same profile: "A state-space modeling framework for engineering
blockchain-enabled economic systems" (arXiv:1807.00955, 2018, 23); "On modeling blockchain-enabled economic networks
as stochastic dynamical systems" (Applied Network Science, 2020, 40); the titles carry vocabulary the page will not
use.

The Scholar page lists the publications "highly cited" in the supervisor's phrase: the two GP papers sum to 361 on
Scholar; the accelerated dual descent paper (184) and the vaccine paper (230) are the other cited optimization and
control work. His own publications page (https://michael.zargham.org/publications.html) lists the TCNS paper and the
TAC paper among 8 peer-reviewed journal articles; the traffic-control arXiv preprint is not on it.

## 5. Possibly also (for the supervisor; not for the page)

Names the sources show as part of the history. None goes on the page unless the supervisor adds it.

| Name | What the source shows | URL |
|---|---|---|
| Matthew V. Barlin | `AUTHORS.txt`: one of the three designers of cadCAD in 2018; co-author of the Insolar-network paper (2021, authors' affiliations "BlockScience") and of arXiv:2001.03020 | https://raw.githubusercontent.com/cadCAD-org/cadCAD/master/AUTHORS.txt ; https://doi.org/10.1109/MC.2020.2996572 |
| Tyler D. Mace | `AUTHORS.txt`: "upgrades and improvements"; 17 commits to cadCAD | same |
| Zixuan Zhang | `AUTHORS.txt` contributor; first author, with Zargham and Preciado, of the 2018 state-space paper (arXiv:1807.00955) and the 2020 stochastic-dynamical-systems paper (https://doi.org/10.1007/s41109-020-0254-9) | same |
| Charles Rice | `AUTHORS.txt` contributor; co-author of the 2019-06-03 introduction post | same |
| Benjamin Scholz | `AUTHORS.txt` contributor; 14 commits to cadCAD; a profile elsewhere says he developed the radCAD framework (secondary) | same |
| Jonathan Gabler | `AUTHORS.txt` thanks; co-author of the 2019-06-12 post | same |
| Nick Hirannet | `AUTHORS.txt` thanks; COO of the firm, joined 2018 (leadership page) | https://www.dynamicalsystemsgroup.com/leadership |
| Peter Hacker | `gds-core` README: "Code auditing and review" (a different name from Jakob Hackel; do not confuse) | https://github.com/DynamicalSystemsGroup/gds-core |
| Marek Laskowski, Hjalmar Turesson, Danil Kabanov, Eden Dhaliwal | co-authors of arXiv:2001.03020 (2020) | https://arxiv.org/abs/2001.03020 |
| Victor M. Preciado | co-author of the 2013-14 geometric-program papers and the 2018 paper | section 4 |
| Alexander Mihailov | co-author with Clark and Zargham, 2023 | https://doi.org/10.1007/s10614-023-10445-9 |
| Matt Stephenson | co-author with Shorish and Zargham of "A Practical Theory of Fungibility" | https://ideas.repec.org/e/psh169.html |
| Chris Catoya | A conference speaker page calls him Executive Director of the cadCAD Foundation, formerly at BlockScience (secondary; not read in full) | https://www.deep-tech-week.com/speakers/chris-catoya |
| Jeff Emmett, Ilan Ben-Meir, Jessica Zartler | Appear in the firm's historical team listing (search-result snippet only) and as contributors to public repositories (`ibenmeir` in the organisation members list) | https://github.com/orgs/DynamicalSystemsGroup/people |
| Griff Green, Isaac (`eenti`), Jonny Dubowsky, Sem Brestels, Andrea Maria Piana, `fjribi`, Harry Goodnight, Charlie Hoppes, Nikhil Jamdade, Chris Frazier | `AUTHORS.txt` "We'd also like to thank" list | same |

## 6. Where the sources and the supervisor's list disagree or run thin

1. **Penland ("Octopus") and Hackel**: no public attribution; hits on them were only in private repositories, which I did not use. Ask the supervisor for a public source for each or leave the two as names acknowledged without a described work.
2. **Spelling**: "Bernardinelli" (supervisor) vs "Bernardineli" (`AUTHORS.txt`).
3. **Year of the GDS paper**: 2022 (WU record, DOI) vs 2021 (`gds-core` README).
4. **PSUU**: no source names its author; the 2021-04-08 post is bylined to the firm. The public code trail is `cadCAD_machine_search`, `interacting-amm-model` (both `danlessa`) and, in 2026, `gds_analysis.psuu`.
5. **Early theorem-proving and client requirements/architecture work**: the supervisor's description of the firm as an engineering firm doing requirements, architecture, proofs and simulation for clients is backed only partly: public client-adjacent work is in the repositories (digital-twin and model repositories) and the 2020 methodology paper; the sources give no public account of requirements and architecture work for clients before 2025.
6. **"Computer scientists"** is not backed by a stated discipline (section 2).
7. **Register flags** (titles to link without echoing): "A State-Space Modeling Framework for Engineering Blockchain-Enabled Economic Systems"; "Evidence Based Decision Making in Blockchain Economic Systems"; "Economic Games as Estimators" (clean); "Token Economics in Real Life ..." (Computer 2021); "Foundations of Cryptoeconomic Systems"; the Research Institute for Cryptoeconomics (publisher of the GDS paper); Token Engineering Labs (Paruch's affiliation); repository names carrying the names of the systems studied.
