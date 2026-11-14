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

