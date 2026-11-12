# WP37 third research pass (w5): the historical blog, the YouTube trail, Penland's spelling, Barlin

Date read for every row: 2026-11-12. Sources public only; unauthenticated fetches (curl, WebFetch); no gh CLI.
Blog dates are those of the Ghost copy at blog.block.science (`article:published_time`); the Ghost copy keeps the
original Medium date for 2019 to 2021 posts and carries a later re-publication date for some (noted per row).
Every post is by-lined "BlockScience" in the site metadata; the real byline is the line in the post, given below.

## 1. The historical blog: how it was read

The home page (https://blog.block.science/) lists only the 2025 posts and offers no archive or pagination. The whole
blog was enumerated from the sitemap (https://blog.block.science/sitemap-posts.xml, 105 posts) and the tag feed
(https://blog.block.science/tag/cadcad/rss/, 15 items, 22 Jun 2020 to 23 Dec 2024). Each post below was fetched
(HTTP 200) and its byline and date read from the page.

### 1.1 Posts that replace Medium links unreachable (HTTP 403) in earlier passes

| URL (fetched, read) | Title | Byline in the post | Date | What it says | Replaces the Medium URL |
|---|---|---|---|---|---|
| https://blog.block.science/introducing-complex-adaptive-dynamics-computer-aided-design-cadcad/ | Introducing Complex Adaptive Dynamics Computer-Aided Design (cadCAD) | "By Michael Zargham with Charles Rice" | 3 Jun 2019 (post modified 18 Jan 2024) | The firm's own origin account: cadCAD "we have created" as a modeling framework and scientific computing library for safer, better designs of cyber-physical and socioeconomic systems; opens from the 1999 Napster testimony and network effects. Carries an Update line (below). | https://medium.com/block-science/introducing-complex-adaptive-dynamics-computer-aided-design-cadcad-38b63b541eb8 |
| (same page, Update line) | the open-source announcement | unsigned update line | line undated; names August 2019 | "Update: We are now open-source! During TEGG in Berlin in August 2019, we made the announcement to make cadCAD an open-source project. Join our community at cadcad.org and community.cadcad.org." The same line is on the next row's post. This is the 2019 open-source announcement: no separate announcement post exists; the record is this update line, with the month and venue. | (same Medium URL) |
| https://blog.block.science/cadcad-filling-a-critical-gap-in-open-source-data-science/ | cadCAD: Filling a Critical Gap in Open-Source Data Science | "By Michael Zargham and Jonathan Gabler" | 12 Jun 2019 | The scientific-Python claim: automation of cyber-physical systems involving people; cadCAD as a scientific computation library for Python (the Python-ecosystem sentences are in the post body). Embeds two YouTube links: https://www.youtube.com/watch?v=X5qy_OZ7RPw (Robot Network Demo, Michael Zargham, uploaded 4 Jun 2019, 23 s) and https://www.youtube.com/watch?v=Z-gY_cFKHOQ (Curation Markets Community Call 7, Solidity Fridays, 6 Jun 2019). | https://medium.com/block-science/cadcad-filling-a-critical-gap-in-open-source-data-science-fcd0d3faa8ed |
| https://blog.block.science/how-to-perform-parameter-selection-under-uncertainty/ | How to Perform Parameter Selection Under Uncertainty | "Article by Krzysztof Paruch and Jamsheed Shorish, with edits and suggestions by Michael Zargham, Danilo Lessa Bernardineli, Jeff Emmett, and Jessica Zartler" | 8 Apr 2021 (modified 15 Sep 2024) | Confirms w4-leads-a: authors Paruch and Shorish, 8 April 2021. A workflow for scientifically iterating multi-dimensional, multi-stakeholder systems with actionable parameter recommendations. | https://medium.com/block-science/how-to-perform-parameter-selection-under-uncertainty-976931ba7e5d |
| https://blog.block.science/complex-systems-modeling-of-community-inclusion-currencies-a-blockscience-collaboration-with-grassroots-economics-the-danish-red-cross/ | Complex Systems Modeling of Community Inclusion Currencies | text names "Andrew Clark, Alexander Mihailov, and Michael Zargham" as authors of the paper | 27 Oct 2022 on the blog (Medium date 31 Oct 2020 per w4-leads-a) | The only readable page tying Clark to the firm: the post presents the paper as a BlockScience collaboration with Grassroots Economics and the Danish Red Cross (title in the URL). | https://medium.com/block-science/complex-systems-modeling-of-community-inclusion-currencies-4e2161787934 |
| https://blog.block.science/generalized-dynamical-systems-part-i-foundations-2/ | Generalized Dynamical Systems Part I: Foundations | "Dr. Michael Zargham and Dr. Jamsheed Shorish" (three-part paper and video series) | 29 Aug 2022 (modified 20 Jun 2024) | Introduces the paper and a 4-part video series; says the series are "extensively researched and leveraged at BlockScience". Part II and III were forecast and (per the supervisor) not released. The video descriptions on YouTube link a Medium copy, https://medium.com/block-science/generalized-dynamical-systems-part-i-foundations-74505bbdf0e. (The 2021 post cited by gds-core, blog.dynamicalsystemsgroup.com/..., does not resolve; this blog copy is dated 2022.) | https://medium.com/block-science/generalized-dynamical-systems-part-i-foundations-74505bbdf0e |
| https://blog.block.science/complex-systems-modeling-maids-gds-cadcad/ | Exploring Complex Systems Modeling with MAIDs, GDS & cadCAD | unsigned; "Led by Octopus, a Blockscience Research Engineer"; thanks "Octopus! for developing and leading this workshop series" | 28 Oct 2024 (modified 16 Jan 2025) | Four workshops (videos below), slides on SlideShare, code at github.com/BlockScience/MAIDs. | the Medium copy named in w4-leads-a B5 |

### 1.2 Other cadCAD, GDS and PSuU posts on the blog (for the record)

| URL | Title | Byline | Date | What it says |
|---|---|---|---|---|
| https://blog.block.science/from-nash-to-lyapunov/ | From Nash to Lyapunov | not read in the metadata (Medium copy under Zargham's name, 2 May 2019 per w4-leads-a) | 1 Oct 2018 | Early note tying equilibrium to stability; the earliest dated post of the line. |
| https://blog.block.science/cadcad-community-update/ | cadCAD Community Update | unsigned | 23 Mar 2020 | Community update (Medium copy: https://medium.com/block-science/cadcad-community-update-fd0a16982def). |
| https://blog.block.science/cadcad-gets-a-new-github-org/ | cadCAD Gets a New GitHub Org | "The cadCAD Team" | 22 Jun 2020 | cadCAD moves to its own organisation as a standalone community. |
| https://blog.block.science/announcing-cadcad-1-0-foundations-for-a-new-era-of-open-modeling/ | Announcing cadCAD 1.0: Foundations for a New Era of Open Modeling | unsigned | 1 Feb 2022 | Release of cadCAD 1.0. Embeds https://www.youtube.com/watch?v=ABSBdj9tEI8 (Algorithms as Policy, Dr. Michael Zargham, TE Academy, 9 Dec 2021). |
| https://blog.block.science/introduction-to-economic-games-as-estimators/ | Introduction to "Economic Games as Estimators" | "Zargham, Shorish, and Paruch" | 22 Aug 2023 | Introduces the paper by those three authors (University of Vienna Institute for Cryptoeconomics working paper). |
| https://blog.block.science/an-introduction-to-foundations-of-cryptoeconomic-systems-2/ | Introduction to "Foundations of Cryptoeconomic Systems" | Voshmgir and Zargham (the paper) | 20 Nov 2023 | Introduces the paper (title carries a crypto term; link only if wanted). |
| https://blog.block.science/engineering-complex-adaptive-systems-video-playlist/ | Engineering Complex Adaptive Systems, Networks & Cybernetics | unsigned | 20 Sep 2019 (modified 12 Dec 2024) | Video series by Zargham on complex adaptive systems (10 embedded videos, below). |
| https://blog.block.science/complex-systems-engineering-introduction/ | Complex Systems Engineering, Digital Infrastructure | unsigned | 20 Nov 2019 (modified 2 Oct 2024) | Embeds https://www.youtube.com/watch?v=La_DnJ65VXk (Introduction to Complex Systems, Michael Zargham, CES Summit '19; uploaded 18 Feb 2020). |

The Filecoin, Gitcoin and other client-project posts are in w4-leads-a and w4-leads-b; the blog copies there stand.
GDS posts: the GDS Part I post is the only GDS post on the blog (consistent with the supervisor's "only one paper
ended up getting released").

## 2. The YouTube trail

### 2.1 The cadCAD community call the supervisor linked

| URL | Title | Channel | Date | Speakers | What it covers |
|---|---|---|---|---|---|
| https://www.youtube.com/watch?v=ig4Z_V5RVQo | cadCAD Community Call #26: Generalized Dynamical Systems & cadCAD - Spaces, Blocks & Diagrams | cadCAD (channel id UCQ6UUADq9AczXv0RmzpgBHw) | 2 May 2023 (31 min 24 s) | Description: "Jamsheed Shorish of Block.Science presents R&D on Generalized Dynamical Systems and its use and development in cadCAD." Only Shorish is named; the description credits GDS research to Zargham and Shorish. | GDS as a template for dynamical systems whose states are influenced by decision-making, building on control theory; feasibility and admissibility of actions on solution trajectories instead of fixed assumptions about decision-makers; slides on Google Drive; links the GDS Part I article (Medium copy). |

The cadCAD channel's Community Calls playlist (https://www.youtube.com/playlist?list=PLzL4U4Szfai00_segN6mVnIi4inh5IhMb,
24 videos) runs from Call #1 (cadCAD Overview & Best Practices) to #26; #13 "cadCAD Technical Specification & Julia
Implementation", #16 "cadCAD 1.0 announcement & BlockScience Labs demo", #22 "cadcad.jl", #23 and #24 "Defining
Spaces from Generalized Dynamical Systems", #25 "cadCAD Reference SISO Alpha demo". The other playlists of that channel
(read from https://www.youtube.com/channel/UCQ6UUADq9AczXv0RmzpgBHw/playlists): cadCAD Tutorials (Robots and Marbles
1 to 5 and the 3-sided market reference model, https://www.youtube.com/playlist?list=PLzL4U4Szfai3fukeWZYSDXi8Vbbk1JPP_),
cadCAD Study Group (9 sessions, ...PLzL4U4Szfai3h9RG-6Pk0sA78b4cqBzE1), cadCAD Workshops (4), cadCAD Model Walkthroughs
(3), Talks & Presentations (1: "cadCAD: A Modeling Library for Generalized Dynamical Systems"), and client-project series
(Gitcoin Model Co-Lab, Luna Swarm project calls). Speakers are not named in the playlist pages; not attributed here.

### 2.2 Jamsheed Shorish

| URL | Title | Channel | Date | Author evidence | What it covers |
|---|---|---|---|---|---|
| https://www.youtube.com/playlist?list=PLmWm8ksQq4YJrB72Na_JB-o8Xu2JLj7h9 | Generalized Dynamical Systems (GDS) \| Zargham & Shorish \| Dynamical Systems Group (playlist, 4 videos) | Dynamical Systems Group (https://www.youtube.com/@BlockScience; the same account as the firm's older "BlockScience" channel) | videos uploaded 22 to 31 Aug 2022 | playlist title "Zargham & Shorish"; description: GDS "extensively researched and leveraged by Dr. Michael Zargham and Dr. Jamsheed Shorish"; the blog post (1.1) says "Dr. Shorish gives a brief, high-level introduction" in the first video | the video series that accompanies GDS Part I |
| https://www.youtube.com/watch?v=vid78CU-gsE | Introduction to Generalized Dynamical Systems (GDS) \| Mathematical Framework & Template | Dynamical Systems Group | 22 Aug 2022 (33 min 36 s) | as above | framework, time, actions, admissible action sets, notation |
| https://www.youtube.com/watch?v=8t-FKDzrnmA | Representation \| The Crosswalk Problem Reachability, Admissibility & GDS \| Part 1 | Dynamical Systems Group | 31 Aug 2022 | playlist | the crosswalk example as a GDS |
| https://www.youtube.com/watch?v=F3BsilIxgbY | Equilibrium & Existence \| ... \| Part 2 | Dynamical Systems Group | 31 Aug 2022 | playlist | equilibrium and existence |
| https://www.youtube.com/watch?v=ZRkYH9JY_Xo | Design & Controllability \| ... \| Part 3 | Dynamical Systems Group | 31 Aug 2022 | playlist | design and controllability |
| https://www.youtube.com/watch?v=ig4Z_V5RVQo | cadCAD Community Call #26 (above) | cadCAD | 2 May 2023 | named presenter | GDS in cadCAD |

Not found: a YouTube channel or playlists under Shorish's own name (searches returned nothing; the playlists the
supervisor remembers are, so far as the public pages show, the DSG GDS playlist above and the cadCAD channel
playlists). The supervisor should supply any other playlist.

### 2.3 Andrew Penland ("Octopus")

| URL | Title | Channel | Date | Author evidence | What it covers |
|---|---|---|---|---|---|
| https://blog.block.science/complex-systems-modeling-maids-gds-cadcad/ | Exploring Complex Systems Modeling with MAIDs, GDS & cadCAD (post) | blog | 28 Oct 2024 | "Led by Octopus, a Blockscience Research Engineer"; "A massive thank you, Octopus! for developing and leading this workshop series" | four-workshop series; slides: https://www.slideshare.net/slideshow/workshop-1-introduction-overview-complex-systems-modeling-w-maids-gds-cadcad/272835681 (and ...-2-... /272835682, -3- /272835683, -4- /272835684) |
| https://www.youtube.com/watch?v=GK5oRDTa72o | Workshop 1: Introduction & Overview \| Complex Systems Modeling w MAIDS, GDS & cadCAD | Dynamical Systems Group | 16 Dec 2024 upload (82 min 36 s) | the post | MAIDs (the Killer Tree example of Koller and Milch 2003), MAIDs as graphs and hypergraphs, links to GDS and cadCAD |
| https://www.youtube.com/watch?v=8IGZQDqAWD4 | Workshop 4: The Modeling Process & Future Directions \| ... | Dynamical Systems Group | 16 Dec 2024 upload (94 min 55 s) | the post | MAIDs informing cadCAD policy and state-update structure, agent strategy and utility, GDS admissible action space; description chapters list "Personal Background and Research Approach" and "Undergraduate Research and Team Building" |
| Workshops 2 and 3 | "Explorations & Connections" and "Agents, Strategies & Equilibria" | Dynamical Systems Group | not located: the blog gives "Watch Workshop 2/3" links whose targets are not in the page HTML I fetched; the YouTube channel's playlists tab is not served to plain fetches | | |
| https://www.youtube.com/@octopusmath | his own channel, "andrew octopus" (id UCew0u8PB9V21wRgS6KEBqbg; description "Mathematics, pedagogy, and cryptocurrency.") | himself | playlists: Calculus 1 (three), Teaching Philosophy, GitCoin Sybil Attacks Talk (2 videos: CDoE-QaCmJY "The Mathematics of Sybil Attacks on GitCoin, part 1"; fkUAgLtSdXA "Part 2: Understanding the Actual QF Matching Function") | own channel | calculus teaching; the Gitcoin talks accompany the firm's Gitcoin posts (special case, public) |

No video or playlist on GDS or cadCAD on his own channel; his GDS, cadCAD and MAID videos are the firm's channel's
workshop series above. No playlist of his on MAIDs by title other than that series was found. "Teaching Philosophy"
holds (z0OCRapnKEo) "Making Mathematical Memes with Dr. Penland", 3 Nov 2021, and (AOjjaXiO0TM) the firm's talk
"Governing Web3: Algorithms as Policy ..." (not for the page: web3 term in the title).

### 2.4 The firm's own video series by Zargham (context; not asked)

"Engineering Complex Adaptive Systems" (blog page 1.2): 10 videos on the DSG channel, 2019 to 2020 originals
re-uploaded 19 to 23 Sep 2024, e.g. https://www.youtube.com/watch?v=lU7OnIBDGE8 "The Age of Networks & the Rebirth
of Cybernetics" (Zargham, upload 18 Feb 2020). Uploaded dates are the channel's, not the talks' dates.

### 2.5 Recommendation, one per author (the page cites one each)

- Jamsheed Shorish: the GDS playlist, "Generalized Dynamical Systems (GDS) | Zargham & Shorish", DSG channel, videos
  of 22 to 31 Aug 2022, https://www.youtube.com/playlist?list=PLmWm8ksQq4YJrB72Na_JB-o8Xu2JLj7h9. Alternative if a
  single video suits: cadCAD Community Call #26, 2 May 2023, https://www.youtube.com/watch?v=ig4Z_V5RVQo (names him as
  presenter).
- Andrew Penland: Workshop 1 of the MAIDs, GDS & cadCAD series, DSG channel, uploaded 16 Dec 2024 (the series
  announced 28 Oct 2024), https://www.youtube.com/watch?v=GK5oRDTa72o, with the blog post as the series' address.

The cadCAD origin: cite the blog post of 3 Jun 2019 for the origin and its Update line for the August 2019 open-source
announcement at TEGG, Berlin (there is no separate announcement post).

## 3. Penland or Pentland

Three independent public pieces agree on "Penland"; none reads "Pentland".

| URL | What it says (quoted) | Names |
|---|---|---|
| https://te-academy.netlify.app/about | team page of the Token Engineering Academy: "Andrew Penland, Ph.D. a.k.a Octopus", role "TE Academy Wizard", "Open-Source Educator and Mathematical Researcher", "awarded with MAA Teaching Award 2021" | Penland; Octopus |
| https://www.youtube.com/watch?v=z0OCRapnKEo | his own channel (@octopusmath, "andrew octopus"), video title "Making Mathematical Memes with Dr. Penland", 3 Nov 2021 | Penland |
| https://github.com/andrewpenland (account created 2014-09-20) | his repositories include cadCAD work for the firm's projects: BalancerPools_Model ("cadCAD model to simulate Balancer AMMs", https://github.com/andrewpenland/BalancerPools_Model), gitcoin_cadcad_model (README: "a collaboration between Gitcoin and BlockScience", https://github.com/andrewpenland/gitcoin_cadcad_model), Risk-Adjusted-Bonding-Curves ("Collaboration between Interchain Foundation and BlockScience", https://github.com/andrewpenland/Risk-Adjusted-Bonding-Curves); commit author "Andrew Penland" (jackhack00/aztec-gddt, 20 Apr 2024); the profile has no name field | Penland (handle) |

The channel, the TE Academy page and the GitHub handle are joined by the nickname and the content (the same
nickname "Octopus" appears on the firm's blog as the research engineer; the GitHub account's repositories are the
firm's collaboration repositories) but no single page states all three together; the identity is the supervisor's
list plus these. Result: the spelling is Penland. The supervisor's "Pentland" is a slip for it; the assistant tells
him rather than the page assuming (his own instruction).

## 4. Matthew Barlin

| URL | Date read | What it says | Names |
|---|---|---|---|
| https://raw.githubusercontent.com/cadCAD-org/cadCAD/master/AUTHORS.txt | 2026-11-12 | "cadCAD was originally implemented by Joshua E. Jodesty and designed by Michael Zargham, Markus B. Koch, and Matthew V. Barlin in 2018." Listed under "Active and Past Contributors" as "Matthew V. Barlin @matttyb80" (not a maintainer). | Barlin; GitHub handle matttyb80 |
| https://github.com/cadCAD-org/cadCAD/graphs/contributors (API: https://api.github.com/repos/cadCAD-org/cadCAD/contributors) | 2026-11-12 | matttyb80 has 4 contributions (Jodesty 731, Koch 74, Bernardineli 37); his design role is credited in AUTHORS.txt, not shown by commit count. | |
| https://github.com/matttyb80 | 2026-11-12 | profile name "Matt Barlin"; no bio, company or organisations. | |
| https://doi.org/10.1109/MC.2020.2996572 (Crossref record) | 2026-11-12 | "Token Economics in Real Life: Cryptocurrency and Incentives Design for Insolar's Blockchain Network", IEEE Computer, Jan 2021: Laskowski, Zargham, Barlin with affiliation "BlockScience, Oakland, California United States" (title has crypto terms; link only if wanted). | Matthew Barlin, BlockScience |
| https://arxiv.org/abs/2001.03020 | 2026-11-12 | "Evidence Based Decision Making in Blockchain Economic Systems: From Theory to Practice", submitted 8 Jan 2020, revised 9 May 2020: Laskowski, Zargham, Turesson, Barlin, Kabanov, Dhaliwal; the arXiv page lists no affiliations. | Matt Barlin |

His public background (field, degree, prior employer) is stated by no source I could find: blank. What the sources
show: designer of cadCAD in 2018 (AUTHORS.txt); affiliated with BlockScience as of the 2021 paper; co-author of the
2020 evidence-based design paper. The page can credit him for that and nothing else; the contributor-background
sentence (controls, economics, physics, mathematics, computer science) cannot rest on him.

## 5. Open items for the supervisor

1. Penland, not Pentland (section 3): confirm the page keeps "Penland".
2. Octopus's workshops 2 and 3 video links and any other playlists by him; Shorish's other playlists, if there are any
   beyond the DSG GDS playlist.
3. A single dated page for the August 2019 announcement does not exist: the page can cite the Update line of the
   3 Jun 2019 post.
4. Barlin's background: blank unless he supplies it.
