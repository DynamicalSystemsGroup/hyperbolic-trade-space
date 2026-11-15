# WP52 — Decisions: the governance lineage on the history page (research spike, then a proposal)

## The direction (2026-11-14, 01:50)

**Supervisor, verbatim:** "the history page may also benefit from a reference to our computer aided governance, computer aided ethnography and
Building the Loop paper (with Ellie Rennie), now that we've factored in the governance concepts at the top level motivation,
it may be worth acknowledging that there is a (self)governance lineage here. it should cost no more than a paragraph, and
you need to read the building the loop paper as well as the older computer aided governance, why is their data and computer
aided ethnography work from blockscience and RMIT to get a handle on it. i recommend you spike first to find the material
online and on my computer, then give me a proposal for a lightweight addition to the history page to address our interest in
and attention to governance. you may also want the attention economy paper (which as it happens i presenting at the ostrom
workshop). i also have some public (and private) work related to computer aided institutional design (building on roth
economist as engineer market design work) which we can see as motivating the need to move beyond presuming a unique optimal
to teasing out a design space for which the choice amongst competing alternatives is not optimization but politics"

**Applied as:** a reading spike first, then a proposal, nothing on the page before his word (`WP52-scope-of-work.md`).
The spike finds and reads, online and on his machine: the computer-aided governance work (BlockScience), the
computer-aided ethnography work (BlockScience and RMIT), "Building the Loop" with Ellie Rennie, the attention-economy
paper he presents at the Ostrom Workshop, and his public work on computer-aided institutional design building on Roth's
"The Economist as Engineer"; private material is listed by path for him and not read into the proposal unless he says
so. The proposal is a paragraph at most for the history page, with `history.yaml` entries (the page's record), saying
the lineage he names: from presuming a unique optimum to teasing out a design space in which the choice among competing
alternatives is politics, not optimization. His direction is the approval of the spike; the proposal waits for his word.

## His corrections to the spike (2026-11-14, 03:25)

**Supervisor, verbatim:** "i just read in your response on the history, yes its why is there data. my mispelling. also the of preprint is the correct
paper and the fact that i presented it at wow may not be relevant for the history. though if it is relevant you can state it
on my authority since i literally showed up and presented it"

**Applied as:** "why is there data" is the piece ("Why Is There Data?", Sisson and Ben-Meir, SSRN 4933063; he is not an
author), so it is a work of the firm's circle he points to, available to the paragraph as a fourth link if he wants it
there; the attention-economies paper is the OSF preprint (Schneider, Nabben, Tamari, Zargham, 2025); its presentation at
the Workshop on the Ostrom Workshop is on his authority, and goes into `history.yaml` as a note on his word only if the
paragraph names the paper, which is his call with the paragraph. Recorded at the end of the spike's `proposal.md`.

## "In our own account" (2026-11-14, 21:30 EST), on the paragraph

**Supervisor, verbatim:** "we dont need to say " in our own account" this is literally our account. stuff we say is by
definition in our own account"

**Applied as:** the phrase is struck from the paragraph (now 88 words): "There is also a governance lineage. It runs
from presuming a unique optimum to mapping a design space, where the choice among competing alternatives is politics,
not optimization." The same phrase opens the page's client-projects paragraph from WP37; it goes by the same rule when
the page is edited, unless he says otherwise.

## The OpenMBEE sentence (2026-11-14, 21:40 EST), read on the history page

**Supervisor, verbatim:** "you can drop the phrase "across opensysml", i am just a maintainer at openmbee which covers work on
the organization, the ecosystem around it, opensysml and flexo. its just a role at an org, i think you are over thinking it
with that link"

**Applied as:** on the history page the sentence becomes "Zargham a maintainer at OpenMBEE" with the one link to his
research page; "maintainer across" and the OpenSysML link go. In `history.yaml` the entry `2026-maintainer` is
retitled "OpenMBEE maintainer" with the role "maintainer at OpenMBEE since 2026 (his research page)", and the
`2026-opensysml` repository entry is kept as a record but no longer listed on the page (its `listed` flag goes to
false, or the entry is removed if nothing else cites it; the tests that tie the page to the record decide which).
Queued with the governance paragraph and the "in our own account" rule as one history unit after his placement call.

**Supervisor, verbatim (21:45 EST):** "also you said in our own account again, don't say that"

**Applied as:** the phrase goes from the whole history page, both places (after the OpenMBEE sentence and at the head of
the client-projects paragraph), and from any page of ours where it stands as a hedge: what the page says is the
team's account by definition. The history unit removes both; the vocabulary checker gains the phrase as an avoided
variant so it does not come back.

## Timeline, two places (2026-11-14, 22:00 EST), on seeing the page without the paragraph yet

**Supervisor, verbatim:** "i don't see the narration of the AOI or CAG work in here yet" and "this is roughly timeline
oriented so it may not be just one paragraph the CAG work is quite old and the AOI work is quite recent"

**Applied as:** the lineage goes in two places on the page's timeline, drafted on branch `history` and previewed on the
verify server: after the cadCAD paragraph (2018 to 2019), computer-aided governance (2019) with Emmett, naming Roth's
market design, humans in charge informed by models, and the lineage sentence (unique optimum to design space, the
choice among alternatives as politics); after the synthesis paragraph, with Nabben and Rennie, computer-aided
ethnography (2023) and Building the Loop (2025) on artificial organisational intelligence, and the closing line on what
this paper does and defers. The OpenMBEE sentence and the four "in our own account" removals are on the same branch;
the record entries from the proposal are in `history.yaml`. Tests, the word ceiling and the checker follow his read.

**Supervisor, verbatim (22:10 EST), on the client-projects paragraph:** "jamming "a special case where the work was
highly public" into the timeline works against its own purpose. it makes people think more about the crypto than they
would have otherwise"

**Applied as:** the aside is gone; the sentence now names the two public items and nothing about why they are public:
"The RAI controller's design record (2021) and Zargham's talk at a workshop in Edinburgh (ICMS), October 2024 are
public."

## Two more directions on the page (2026-11-14, 22:20 EST)

**Supervisor, verbatim:** "you should include my ADCS-lifecycle-demo repo (github pages) and the OSA and JAXA talks in
the timeline"

**Supervisor, verbatim:** "the openmbee and the firm can go. it feels forced"

**Applied as:** the OpenMBEE sentence and the firm's synthesis clause are removed from the page (the NumFOCUS line
stays); the record entries `2026-openmbee`, `2026-maintainer` and `2026-opensysml` stay in `history.yaml` as record
but are no longer cited by the page. The ADCS-lifecycle-demo repository (its GitHub Pages site) and the OSA and JAXA
talks are found, read and entered in the record with resolved links and dates, and placed on the page's timeline at
their dates, each in a clause; sources checked before any sentence is written.

## The block-diagrams repository, and reading the contents (2026-11-14, 22:35 EST)

**Supervisor, verbatim:** "i think this repo was mostly zeke, danilo just reviewed it https://github.com/DynamicalSystemsGroup/dynamical-block-diagrams"

**Supervisor, verbatim:** "you should probably look closer and align the prose to the contents"

**Supervisor, verbatim:** "there was also work from carolina in there but its attributed in the pdf not the git history"

**Applied as:** read from the repository itself: 0xekez (Zeke Medley) 11 of 12 commits, 26 July to 9 August 2024, the
write-up and a Julia executor with examples; danlessa (Danilo Bernardineli) one commit, 15 May 2026, "aesthetic
changes"; the README links Carolina Riascos's consensus-network write-up. The page now says Zeke wrote it (a write-up
and a Julia executor) in the internship, that it credits Carolina Riascos-Álvarez's consensus-network work in the
write-up, and that Danilo reviewed it; the record entry's people carry the three roles with their evidence. The
ADCS lifecycle demo was read the same way before its sentence was written: one geosynchronous satellite, one
requirement, evidence of several kinds, a person's judgement on the record; four presentations with dates in its
README, among them the JAXA workshop (12 June 2026) and the Open Source Architects community (15 October 2026), which
is the "OSA" he named. The earlier draft sentence calling it the cubesat's lifecycle was wrong and is gone.

## Market design lessons; the fungibility work and product invariants (2026-11-14, 23:00 EST)

**Supervisor, verbatim:** "getting close" https://blog.block.science/market-design-lessons-for-safety-first-institutional-engineering/ probably fits.
and i'd also like to flag the work on a practical theory of fungibility which set the context for ML methods and markets
but did not yet provide a coordinate system suitable for automated market makers. since automated market makers like
balancer (which we worked on with fernando martinelli who was at the time of his first proofs a blockscience team member),
this provides an interesting side bar about experience with product invariants and how the web3 lineage fed in without
itself being "the point"

**Applied as:** two additions to the page, each researched before a sentence is written: (1) the Market Design Lessons
post (Shorish with Zargham and Ben-Meir, BlockScience, 2023) enters the lineage at its date; (2) a sidebar on product
invariants: the practical theory of fungibility (the paper found and read, with its authors and date) set the context
for machine-learning methods and markets but gave no coordinate system suited to automated market makers; the work on
Balancer, whose invariant is a weighted product, with Fernando Martinelli, then a BlockScience team member at the time
of his first proofs (the affiliation sourced, or stated on the supervisor's word and marked so); the sidebar says the
web3 lineage fed the experience with product invariants without being the point. Balancer's record entries carry the
special-case flag the record uses for cryptocurrency settings. Sources resolved first; the sentences follow them.

**Supervisor, verbatim (23:05 EST):** "our configuration spaces and economic games as estimators papers are also salient
under this view"

**Applied as:** the two papers (found, read, resolved) join the product-invariant sidebar at their dates as the work
that set the context: configuration spaces, and economic games as estimators.

## RAI and Filecoin as public client work (2026-11-14, 23:20 EST)

**Supervisor, verbatim:** "the rai and filecoin work can (and should appear) as public client facing work that used these methods but with language
that avoids implying this work is "crypto"."

**Applied as:** the client-projects paragraph names the RAI and Filecoin work as public client-facing work that used
these methods, in language that says what was done (a feedback controller's design record; two network-economics
analyses adopted by the network's governance) and names no cryptocurrency setting; the record entries keep their
special-case flag, which is the record's own bookkeeping and not the page's words. The product-invariant sidebar is
written the same way: automated market makers and weighted-product invariants, the web3 lineage as the experience it
gave, not the point.

**Supervisor (23:40 EST), on the opening sentence:** "drop the word "human" in the first sentence"

**Applied as:** "This page acknowledges the people and the lineage of this work, which the paper's citations cannot carry".

**Supervisor (23:42 EST):** ""The experience with product invariants is what this method keeps." this is awkward phrasing"

**Applied as:** "What carried over is the practice of reasoning with product invariants."

**Supervisor (2026-11-15, 00:05 EST):** "should we also cite the engineering for legitimacy work that emerged to support a
client project for the arbitrum foundation"

**Applied as (pending his word):** the essay "Engineering for Legitimacy" (Ben-Meir and Zargham, BlockScience, 2024) and
the Arbitrum report it emerged beside are read and resolved first; if he says yes they enter the late lineage as public
client work in neutral words, with "emerged to support" the client project on his authority unless a source says it.

**Supervisor (00:10 EST):** "also not sure if it helps us but an older document based study is here
https://hackmd.io/@blockscience/Aztec_Sequencer_Selection from work on aztec"

**Applied as (pending):** read first; placed only if it is what the page's line needs (a trade study of candidate
designs against stated criteria, decided by the people accountable), in neutral words, or left out with the reason.

**Supervisor, verbatim (2026-11-15, 00:25 EST; popup: the Aztec trade study, the legitimacy essay with the Arbitrum report,
both, or neither):** "Both"

**Applied as:** the late lineage gains "Engineering for legitimacy" (Ben-Meir and Zargham, 2023; the page blocks
automated readers, noted) beside the Arbitrum position paper (20 March 2024) described in neutral words as a client's
governance building an accountable, cost-conscious network of expert service providers; the client paragraph gains the
Aztec study as a document-based trade study of two candidate protocols against stated technical and economic criteria
for a client's engineering team (August 2023). Record entries with the special-case flag; register rows; the word
ceiling follows the count.

## The essay's page is gone from Medium (2026-11-15, 00:45 EST)

What the sources show: the Medium URL of "Engineering for Legitimacy" answers 410, "The author deleted this Medium
story" (seen in the browser pane); the Internet Archive holds a capture of 16 June 2025 whose metadata gives the byline
"By Ilan Ben-Meir and Michael Zargham" and the publication date 19 March 2024, one day before the Arbitrum position
paper; the text does not mention Arbitrum. The page links the archived capture for now, the record says why, and his
word decides whether a deleted essay is cited at all.

**Supervisor (00:50 EST):** "two other reference points we might consider: https://blog.block.science/algorithms-as-policy/
and https://www.dynamicalsystemsgroup.com/blog/an-algorithm-is-a-camera"

**Applied as (pending):** both read and resolved; placed on the timeline at their dates if he says so, each in a clause
that says what it argued.

**Supervisor, verbatim (00:55 EST; popup over the essay, Algorithms as Policy and An Algorithm Is a Camera):** "see dsg
blog for missing content. the algorithms as policy essay from kelsie's blog is fine"

**Supervisor, verbatim (00:57 EST):** "when doubt we should use the https://www.dynamicalsystemsgroup.com/blog/engineering-for-legitimacy versions"

**Applied as:** the essay is linked to its version on the firm's own blog, not the archive; the rule for every source
of the firm's with a version there is the Dynamical Systems Group blog first; Algorithms as Policy (Zargham and
Nabben, 2021) enters the early lineage; An Algorithm Is a Camera was not answered and is left off the page until he
says otherwise.

**Supervisor (01:05 EST):** ""A side road fed in without being the point." obnoxious metacommentart"

**Applied as:** the sentence is gone; the paragraph opens on the Balancer whitepaper. The record's register row for it
is removed.

**Supervisor, verbatim (01:15 EST):** "to reduce the crypto reading i want to call RAI an algorithmic debt market or similar
and filecoin as a filestorage and retrieveal network. we need to do a decrypto-fication network"

**Applied as:** "a feedback controller for the RAI algorithmic debt market"; "the governance of the Filecoin file storage
and retrieval network"; a pass over the page for words that read as cryptocurrency found no other in the prose (source
titles in the dated list keep their own words, as the list's rule allows).

**Supervisor, verbatim (01:20 EST):** "you don't actually need the brand names RAI or filecoin in the text. just their
categorical descriptions"

**Applied as:** "a feedback controller for an algorithmic debt market"; "the governance of a file storage and retrieval
network"; the names stay in the record entries and the dated list's source titles.

## Acceptance (2026-11-15, 01:25 EST)

**Supervisor, verbatim (popup: accept the history page as it now stands, or more edits):** "Accept"

**Applied as:** the history page as rendered on the verify server at this moment is accepted; branch `history` lands on
`dev` once its full checks pass (lint, format, vocabulary with the new avoided phrase, the history test module, the link
checker, the fast suite); CI then runs on the head. WP52 is accepted with it.

**Supervisor, verbatim (01:40 EST):** "algorithm is a camera can go in but only if it fits naturally, don't force it"

**Applied as:** it fits where Ben-Meir is already named, one sentence ahead of the legitimacy essay: "Ilan Ben-Meir's An
algorithm is a camera (2023) made the point this page rests on: a model is a framed view of a reality that exceeds it,
not a view from nowhere." The judgement that it fits is the driver's; his read decides.

**Supervisor, verbatim (01:45 EST):** "i also don't think citing my cv is necessary. if its a bare claim, so be it"

**Applied as:** the Edinburgh talk is stated without a link; the trace marks the sentence as the team's account; the
record entry stays as the note of where the talk is listed.

**Supervisor, verbatim (01:55 EST):** "simplify the sentence. it doesn't need to be the claim this rests on just the claim that"

**Applied as:** "Ilan Ben-Meir's An algorithm is a camera (2023) made the point that a model is a framed view of a reality
that exceeds it, not a view from nowhere."

**Supervisor, verbatim (02:10 EST):** "also my incose 2026 and in scipy 2026 papers may need to appear. the incose paper for the
AI posture and the scipy paper for the sympy proof scripting

these will also help buff up the post crypto part of the story"

**Applied as (pending the sources):** the INCOSE IS 2026 paper (document assurance; verification by machine, validation by
a named human) and the SciPy 2026 paper (derivations scripted in SymPy, the pattern this repository's lemma scripts
follow) enter the 2026 part of the timeline once each is resolved (DOI or proceedings page), each in a clause that says
what it did and how this project uses it.

**Applied (02:25 EST):** both were already in the record (entries `2026-incose`, INCOSE IS 36(1) 1501 to 1514, July 2026,
Crossref; `2026-scipy-talk`, the SciPy 2026 programme page, 17 July 2026, with video and slides; no proceedings paper
found yet). The 2026 paragraph gains two sentences: the INCOSE paper set the posture this project takes toward AI
assistance (verification by machine against a specification, validation of fitness by a named person, assurance where
both close); the SciPy talk showed derivations scripted in SymPy with identities as test assertions in continuous
integration, the pattern this repository's lemma scripts follow. Register rows C710 and C711. If the SciPy proceedings
paper appears, its link replaces the talk's on his word.

**Supervisor, verbatim (02:30 EST):** "the scipy paper is live in the proceedings https://proceedings.scipy.org/articles/wdyr6752
and has its own doi now"

**Applied as:** the page links the paper by its DOI (10.25080/wdyr6752; SciPy Proceedings 2026, published 29 October
2026, first page 303, per the proceedings page's metadata) and says "SciPy paper"; the record gains the entry
`2026-scipy-paper` beside the talk's.

**Supervisor, verbatim (02:35 EST):** "https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00335 for roth  doi:
https://doi.org/10.1111/1468-0262.00335 and https://incose.onlinelibrary.wiley.com/doi/abs/10.1002/iis2.70203 for my paper.
doi: https://doi.org/10.1002/iis2.70203"

**Applied as:** the page keeps the DOIs as its links (the record's convention); the two Wiley landing pages are noted on
the record entries as where each DOI resolves. Both hosts answer 403 to automated requests, as the DOIs do, so the
link checker's "blocked" reading stands for both.

**Supervisor (02:50 EST):** "does protocols and institutions belong in this history and acknowledgements page"

**The driver's view, pending his word:** yes, as one clause in the late lineage at its date. The record: Zargham and
Ben-Meir, "Protocols and Institutions", Zenodo preprint of a book chapter, 6 March 2025, doi:10.5281/zenodo.15122312
(resolves): institutions defined mathematically by correspondence to stability in Lyapunov's sense, protocols and
institutions read through control systems engineering, with institutional economics, cybernetics and market design
cross-referenced. It is the step between legitimacy as trade-off curves (2024) and the ethnography-and-loop work (2025)
and the theoretical ground of the protocol-based stance his contributing guideline takes; it also brings the control
and stability vocabulary of his earliest work back into the lineage. Against: the page is at 904 words and each
clause must earn its place. If he says yes: "Protocols and institutions (2025), with Ben-Meir, defined institutions by
their stability in Lyapunov's sense and set protocols as the engineered part of them", one record entry, one row.

**Supervisor (03:05 EST):** "another document that may merit a link is https://www.researchgate.net/publication/381615723_Min-Maxing_Complexity_on_Digital_Infrastructure_Mechanisms_through_Occam's_Razor_and_Ashby's_Law_of_Requisite_Variety"

**Applied as (pending):** found and read where a stable record exists (a DOI or publisher page rather than ResearchGate,
which blocks automated readers); placed if it fits the lineage's line, with the reason either way.

**What the sources show (03:10 EST):** ResearchGate answers 403 to automated readers; the stable record is a Zenodo
presentation of 19 June 2024 by Danilo Lessa Bernardineli alone (doi:10.5281/zenodo.12170072), with no abstract on the
record; the title is all a clause could rest on without reading the file. The driver's view: it is Danilo's work, so if it
enters the page it enters the people's paragraph beside his review of the block-diagrams repository, as his presentation
on keeping a mechanism as simple as Occam's razor allows and as varied as Ashby's law requires; it is not on the
governance lineage's line. Pending his word, and his word on whether a paper version with other authors exists.

**Supervisor, verbatim (03:15 EST; popup):** "Add Protocols and Institutions,Add min-maxing complexity"

**Supervisor, verbatim (03:16 EST):** "the length can be relaxed. 1000 words is okay with me, we're filling in the real
story of this work which is actually quite rich"

**Applied as:** Protocols and institutions (2025) as one sentence between the legitimacy work and the loop; Bernardineli's
presentation (2024) as a clause in the people's paragraph after his review; record entries and rows; the page's word
ceiling in `tests/test_site.py` set to 1000 with his words as the reason.

**Supervisor (03:20 EST):** "i downloaded the minimax complexity paper for you to read"

**What it is (read from the PDF in his Downloads, `ssrn-4865894.pdf`, 20 pages):** "Min-Maxing Complexity on Digital
Infrastructure Mechanisms through Occam's Razor and Ashby's Law of Requisite Variety", Danilo Lessa Bernardineli, Ilan
Ben-Meir, Michael Zargham and Jakob Hackel, BlockScience; mechanisms for multi-stakeholder digital infrastructure are
to be as complex as needed to encode the variety of behaviour and as simple as possible to stay legible to the
stakeholders they affect; with the precautionary principle, three decision principles for mechanism selection,
variety, legibility and safety; two case studies, the Aztec sequencer selection and Neural Quorum Governance on the
Stellar Community Fund. **Applied as:** the clause moves from the people's paragraph into the late lineage as the
firm's paper with four authors, linked by its SSRN record, and ties to the Aztec trade study the page already names;
the presentation entry stays in the record as the talk of it.

**Supervisor (03:30 EST):** "one more post crypto citation https://docs.dynamicalsystemsgroup.com/governed-compute/ assess
this for inclusion" and "Tindall is the correct spelling / the lead on this work was Sayer Tinsall" (the second line his
correction of the first: Sayer Tindall).

**Applied as (pending the read):** the page is read; if it enters, it enters the 2026 paragraph as the firm's work on
governed compute led by Sayer Tindall, the Realization layer the lifecycle demo's README points to, in neutral words;
the record entry names Tindall as lead on his authority unless the page states it.

**Applied (03:40 EST):** governed compute read (the firm's documentation, September 2026, no byline: authorization opens a
run; nothing advances until it conforms to its specification and is fit for its purpose; evidence a byproduct of the
work) and placed in the 2026 paragraph as led by Sayer Tindall on his authority. The addition took the page to 1,021
words against his ceiling of 1,000, so the sentence was tightened and the page's closing line "This project keeps the
same split between machine verification and human validation" was cut as redundant now that the INCOSE paper and the
governed-compute sentence say it; the page stands under the ceiling.

**Supervisor, verbatim (03:55 EST):** "the 1000 word is a guidance not a hard requirement. the governed compute needs to be
tied back to the idea of algorithms as policy. and making the decision surfaces explicit so governance is informed and
accountable. there are at least a few words you can carve back, eg "a firm post" is just a "post""

**Applied as:** the governed-compute sentence now reads "took algorithms as policy into the firm's own infrastructure,
with every decision surface explicit so that its governance is informed and accountable: a run opens on authorization,
advances only when it conforms and is fit for its purpose, and its evidence is a byproduct of the work"; "a firm post"
is "a post"; the test's word bound sits above his guidance of 1,000 (1,100) with his words in the comment.

**Supervisor, verbatim (04:05 EST):** "i might also suggest spending a sentence or two to acknowledge that the BDP and MSML
work was subsumed by adopting the OMG standard sysmlv2 and the openmbee implementations"

**Applied as (for his read):** one sentence after the block-diagrams and MSML work: that work was subsumed when the firm
adopted the OMG standard SysML v2 and the OpenMBEE implementations of it, in which this paper's cubesat model is
written; the claim of subsumption is the team's account; the links are the OMG specification and OpenSysML (the
record's existing entry).

**Supervisor, verbatim (04:15 EST):** "protocols and institutions formalizes an argument first made in a 2019 blog: from nash
to lyupunov"

**Applied as:** the sentence gains "formalising an argument first made in From Nash to Lyapunov (2018)", linked to the
record's existing entry; the record dates the firm's blog copy 1 October 2018 and the Medium copy 2 May 2019, so the
page says 2018; the tie is his account, noted on the row.

**Supervisor (04:20 EST):** "given the political economy undertones, it might worth citing: https://mzargham.github.io/politics-of-progress/
and https://www.dynamicalsystemsgroup.com/blog/knowledge-networks-and-the-politics-of-protocols"

**What the pages show:** Knowledge Networks and the Politics of Protocols, Zargham, Ben-Meir and Nabben, the firm's blog,
9 January 2024 (marked updated): tools that let users provision, operate and govern their own instances create a new
commons; the tools are never politically neutral, since developers' decisions structure the action space ("design is
governance", after Amber Case). The Politics of Progress, Zargham 2025, a GitHub Pages site: a comparative and
meta-analysis of two books on techno-political thought (Andreessen's manifesto; Klein and Thompson's Abundance) to
surface the assumptions behind the Overton window on progress. **The driver's view:** the first belongs, one clause in
2024 between Algorithms as Policy and the legitimacy work, since it states the premise the page's lineage sentence
rests on (a protocol structures an action space, so its design is politics); the second is a reading of other people's
books and would read as editorial on a page about this work's lineage; his call.

**Supervisor, verbatim (04:25 EST; popup):** "also add my role as research director and board member of metagov.org,Add
Knowledge Networks,Add The Politics of Progress"

**Applied as (pending the role's source):** Knowledge Networks (2024) as a clause before the legitimacy work; The Politics
of Progress (2025) as a clause after Protocols and Institutions, with the citation its page gives; his role as research
director and board member of the Metagovernance Project beside the NumFOCUS sentence, sourced from metagov.org if a
page states it, else on his authority and marked so.

**Supervisor, verbatim (04:30 EST):** "the politics of progress should be cited as an example of the role of constraints and
tradeoffs" and "the point i was making in the editorial is that neither acknowledged tradeoffs"

**Applied as:** "The politics of progress (2025) read two popular visions of technology and society and found that neither
acknowledged trade-offs: abundance needs institutions that make them visible and negotiate shared constraints"; the
record quotes the page's own sentence on deliberative institutions and marks "neither acknowledged trade-offs" as his
summary of his editorial. Knowledge Networks (2024) placed before the camera and legitimacy sentences. His Metagov role
sourced from metagov.org/people (Board; Research Director) and placed beside the NumFOCUS sentence.

**Supervisor (04:45 EST):** ""at the JAXA MBSE/MCE Workshop in June" June 2026 so it its not inaccurate once the year changes"

**Applied as:** "in June 2026 and to the Open Source Architects community in October 2026".

**Supervisor (05:10 EST):** "" long-running endeavour with many contributors." doesn't need a link i think"

**Applied as:** the opening sentence's link to the dated-references anchor is removed; the list keeps its own heading and
anchor; the test that pinned the link is turned round.

**Supervisor (05:15 EST):** "the full paper is in downloads" (the CredSperiment, SSRN 4570035, Ellie Rennie, 49 pages, posted 14
September 2023, revised 30 November 2023, per the screenshot he sent); "use this source for algorithms as policy
https://kelsienabben.substack.com/p/algorithms-as-policy (2020)"; "which also cites our sourcecred work
https://medium.com/sourcecred/exploring-subjectivity-in-algorithms-5d8bf1c91714 and there is additionally ellie's post on
the credsperiment"

**Applied as (pending the reads):** Algorithms as Policy re-sourced to Kelsie Nabben's Substack with its 2020 date; the
SourceCred work (Exploring Subjectivity in Algorithms) and Rennie's ethnography of the CredSperiment read and placed at
their dates as the strand from algorithms as policy to computer-aided ethnography, in neutral words.

**Supervisor (05:30 EST):** "one more reference from Eric Alston that may help build up the background
https://law.mit.edu/pub/governanceasconflict/release/1" and "we also had this in the same journal which may also fit the
story arc https://law.mit.edu/pub/dao-precedents-cybernetics/release/1", then: "i am going to need you to give me an
assessment of how these works fit the story. basically this history spans mathematics, engineering, economics, and
political science"

**What the sources show so far:** law.mit.edu answers 403 to automated readers (Cloudflare). From secondary records:
Alston, "Governance as Conflict: Constitution of Shared Values Defining Future Margins of Disagreement", MIT
Computational Law Report: conflict as an input to institutional decision-making, accommodated ex ante (mitigated) and
ex post (resolved) among heterogeneous governance preferences, applied to DAO design. Zargham and Nabben, "Aligning
'Decentralized Autonomous Organization' to Precedents in Cybernetics", SSRN 4077358 (4 April 2022) with a version in the
same journal: Beer's viable system model, DAOs read by viability and purpose, the 1Hive case, the subjectivity of the
governance designer. The assessment he asked for is given in chat and recorded here once he has answered it.

**Supervisor (05:55 EST):** "i opened both in your browser so you can see them. Alston is a longstanding team member whose work
has direct bearing on ours so i would like to get him a credit in this history. but i want you to look at the article before
i make a judgement"

**Read (the driver, in the browser pane, both pages whole):** Eric Alston, "Governance as Conflict: Constitution of Shared
Values Defining Future Margins of Disagreement", MIT Computational Law Report, published 5 December 2022; author note: Scholar
in Residence, Leeds School of Business, University of Colorado Boulder; thanks the Metagov DAO for research support. No DOI
on the page; the law.mit.edu host answers 403 to automated readers. Zargham and Nabben, "Aligning 'Decentralized Autonomous
Organization' to Precedents in Cybernetics", same journal, published 20 November 2023; SSRN preprint 4 April 2022
(DOI 10.2139/ssrn.4077358, resolved through Crossref). The assessment is in chat; his judgement to follow. Alston's standing
as a team member rests on the supervisor's word.

**Supervisor (06:05 EST):** "part of the goal of this history and acknowledgements page is to retell this story of design
optimization, legitemacy, economics and governance of highly automated (and often adversarial) systems in plain language
without the web3 stylings"

Recorded as the page's intent, beside the earlier rulings (categorical descriptions, no brand names, the lineage fed in
without being the point). Applied to the pending sentence: the paper with Nabben is described by what it argues, not by
the acronym in its title; Alston's organisations are described as organisations whose rules are partly code.

**Supervisor (06:10 EST):** "Eric is cited primarily for the need to support conflict and disagreement as essential rather
than to model them away"

The point of the Alston sentence is fixed by this; the draft in chat carries it, with the paper with Nabben described in
plain words. Placement, the word bound and the two remaining "automated market maker" phrasings await his word.

**Supervisor (06:30 EST):** "\"the design record of a feedback controller for an algorithmic debt market, written with its
developers before launch (2021)\" this is the same example as the pydata talk but the pydata talk (and then later the ICMS
talk) cover that system after it had been in production for years and models were used for configuration management of
the fielded system"

The client sentence is to carry the arc: the design record before launch (2021), then the PyData talk and the ICMS talk
(October 2024) on the same system after years in production, where models served the configuration management of the
fielded system.

**Supervisor (06:40 EST):** "the main difference is we have less focus on me, and the common thread is the ideas and lots of
other people given explicit acknowledgements for their ideas and contributions"

Recorded as the page's second statement of intent: the ideas are the thread; the people are acknowledged by name for
their ideas and contributions; the page is not about Zargham. The driver's read of where the page still centres him, and
the proposed edits, are in chat.

**Supervisor (06:50 EST):** "after that i want you to do a sanity check against my personal website for timeline and story
arc consistency. this is a different view but its the same history so compatibility not consistency is the requirement:
michael.zargham.org" and, on Alston: "tied in via the MIT cybernetics paper (common case study 1hive, but also was used by
giveth, commons stack and token engineering commons)."

The site's three pages read by the driver (front, research, publications; "Updated October 2026"). The joint works with
Alston found there: "What Constitutes a Constitution?" (Zargham, Alston, Nabben, Ben-Meir; Zenodo 10.5281/zenodo.10609125,
6 April 2023) and "Path Dependence: An Uncomfortable Institutional Design Axiom" (Alston, Case, Zargham; Ostrom Workshop
abstract 2024, hdl:10535/11015). The communities he names are described on the page in categorical terms, per his rule.

**Supervisor (06:55 EST):** "honestly open question:" with three sources, the conviction-voting paper
(github.com/BlockScience/conviction, social-sensorfusion.pdf), Giveth's post "Conviction voting: a novel continuous
decision-making alternative to governance" and the firm's "A brief history of conviction voting": "this work was part of the
substance of the computer aided governance push and as you can see its built on systems that existed in production"

**Supervisor (07:00 EST):** "the story covers: model based systems engineering, simulations and measurements, decision
analysis, economics and governance."

The five strands replace the driver's four-field reading as the page's frame. The conviction-voting question is assessed
in chat after the three sources are read (the two posts answer 403 to curl; read in the browser pane).

**Read (the driver, 07:15 EST):** the conviction-voting proposal "Sensor Networks and Social Choice" (Zargham, dated
30 July 2018, "at the request of Frank Wang of X-Order Research firm"; conviction voting "derived from the Discounted
Integral Priority algorithm" of his 2014 GLOBECOM paper; governance as sensor fusion; Stella and Python prototypes;
acknowledges Jadbabaie, Preciado and Olfati-Saber); Jeff Emmett's Commons Stack explainer on Giveth's blog (3 July 2019:
"derived from the paper on 'Social Sensor Fusion' by Dr. Michael Zargham"; the cadCAD model); and "A Brief History of
Conviction Voting" (Zargham, 26 December 2020: Balancer proofs with Koch and Martinelli, the Zug prototype as dynamic
average consensus, Griff Green, Emmett and the Commons Stack, SourceCred, deployment by the 1Hive DAO). Both Medium
hosts answer 403 to automated readers. The assessment, the focus read and the compatibility check against his site are in
chat; his calls to follow.

**Supervisor (07:25 EST):** "it might be good to get a \"bottom line up front paragraph\" before then recounting the whole
story. then closing with a conclusion that resumarizes the thesis and connects it directly to the motivation for this work.

we have this page because a lot of the substantive learning came not from academia but from designing and governing
production systems in highly automation, highly adversarial, highly politicized digital ecosystems."

The page's shape: a bottom-line paragraph first, the story, a closing paragraph restating the thesis and tying it to this
work's motivation. His sentence is the thesis; the drafts are in chat in his words.

**Supervisor (07:35 EST):** "we can treat this as an essay in its own right that stands in contrast to the academic work
cited which cannot capture lived experience and grey literature"

The page is an essay, not a one-screen acknowledgements list: the WP37 "one screen" word test no longer states the page's
intent, and the bound is to be reset with his words once the shape lands. The opening sentence is to say what the essay
carries that the citations cannot: lived experience and the grey literature.

**Supervisor (07:40 EST):** "2000 is generous and once you have a full draft we can go back and carve it down to ensure
everyone word and reference earns its place"

Taken as the go for the full draft in one edit pass on the history branch, bound 2,000, with a carving pass to follow his
read.

**Supervisor (07:55 EST):** "i also think we probably want to make my distributed convex optimization work slightly more
explicit so that Jadbabaie, Ribeiro and Ozdaglar are named in the text. this is for my TAC paper which came before the
paper with Preciado."

Applied in the pass: the "Before the firm" paragraph opens with the TAC paper (2014) and its four authors, then the paper
with Preciado.

**Supervisor (07:58 EST):** "still before founding the firm."

Both 2014 papers stay in the "Before the firm" paragraph, the TAC paper first.

**Supervisor (08:35 EST):** "i don't want the history records forced into the page you can keep them in the background
for fact checking."

The generated "Dated references" list leaves the page. The record (`history.yaml`), the trace and the tests that tie
every link, name and year of the prose to the record stay as the fact-checking apparatus.

