# WP52 D-3: the proposal for the history page

Nothing here is on the page. The page, the record and the test ceiling change only on his word.

## The paragraph (92 words)

> There is also a governance lineage. In our own account, it runs from presuming a unique optimum to mapping a design
> space, where the choice among competing alternatives is politics, not optimization. It starts with
> [computer-aided governance](https://blog.block.science/computer-aided-governance-a-revolution-in-automated-decision-support-systems/)
> (2019), written with Jeff Emmett, which names [Alvin Roth's market design](https://doi.org/10.1111/1468-0262.00335) and
> keeps humans in charge, informed by models. With Kelsie Nabben and Ellie Rennie came
> [computer-aided ethnography](https://kelsienabben.substack.com/p/computer-aided-ethnography-cae) (2023) and
> [Building the Loop](https://doi.org/10.1111/epic.70009) (2025). This paper stays with what is possible and what trades
> against what; what is preferable is for accountable people to settle.

What each clause rests on (R-3):

| Clause | Carried by |
|---|---|
| "In our own account ... unique optimum ... design space ... politics" | his direction (WP52-decisions.md); marked as the team's account, as the page marks its other framing (claim `team-account`). No single source states it whole (`sources.md`, item 6). |
| computer-aided governance (2019), with Jeff Emmett | the post's byline, "co-authored by Michael Zargham & Jeff Emmett", 7 August 2019 |
| names Roth's market design | the post: market design "pioneered by Alvin Roth" |
| keeps humans in charge, informed by models | the post: "humans stay in charge", models simulate the results of policies |
| with Nabben and Rennie came computer-aided ethnography (2023) | the post's authors Nabben, Zargham, Rennie, 20 February 2023, building on computer-aided governance |
| Building the Loop (2025) | authors include Rennie, Nabben, Zargham; Crossref issued 2025-11 (the EPIC page says 19 January 2026) |
| "what is possible and what trades against what; what is preferable ... accountable people" | the project's own line (the scope), not a claim about a source; if he prefers it cut, the paragraph is 71 words |

Left out, for lack of reading or of support: "Why Is There Data?" (the probable "why is their data"; the title is not
confirmed and its authors are Sisson and Ben-Meir), the attention-economy paper (abstract only; no 2026 Ostrom Workshop
event found), and "computer-aided institutional design" as a phrase (no public text uses it). To add the attention
paper: append "and, with Nathan Schneider and Ronen Tamari, attention economies (2025)" to the fourth sentence (about
+12 words) and add entry 5 below.

## The `history.yaml` entries (the file's existing schema)

```yaml
  - id: 2019-computer-aided-governance
    date: "2019-08-07"
    kind: post
    title: "Computer-Aided Governance — A Revolution in Automated Decision-Support Systems"
    people: [{name: "Jeff Emmett"}, {name: "Michael Zargham"}]
    url: https://blog.block.science/computer-aided-governance-a-revolution-in-automated-decision-support-systems/
    read_on: "2026-11-14"
    shows: "The firm's blog post of 7 August 2019, 'co-authored by Michael Zargham & Jeff Emmett': computer-aided governance is not governance by computers, humans stay in charge and are better informed by simulation of policy outcomes; it names market design as pioneered by Alvin Roth."
    claim: sourced
    note: "Replaces the Medium link (HTTP 403): medium.com/block-science/computer-aided-governance-cag-a-revolution-in-automated-decision-support-systems-9faa009e57a2. The lineage sentence (unique optimum to design space) is the team's account, not the post's."

  - id: 2002-roth-economist-as-engineer
    date: "2002-07"
    kind: paper
    title: "The Economist as Engineer: Game Theory, Experimentation, and Computation as Tools for Design Economics"
    people: [{name: "Alvin Roth"}]
    url: https://doi.org/10.1111/1468-0262.00335
    read_on: "2026-11-14"
    shows: "Econometrica 70(4), 1341-1378, July 2002 (Crossref); market design as engineering; 'the adoption of a design is at least partly a political process'."
    claim: sourced
    note: "The DOI answers 403 to automated requests (blocked, not failed); Crossref confirms it."

  - id: 2023-computer-aided-ethnography
    date: "2023-02-20"
    kind: post
    title: "'Computer Aided Ethnography' (CAE)"
    people: [{name: "Kelsie Nabben"}, {name: "Michael Zargham"}, {name: "Ellie Rennie"}]
    url: https://kelsienabben.substack.com/p/computer-aided-ethnography-cae
    read_on: "2026-11-14"
    shows: "Nabben's Substack, 20 February 2023, authors as listed; builds on computer-aided governance (Zargham and Emmett)."
    claim: sourced

  - id: 2025-building-the-loop
    date: "2025-11"
    kind: paper
    title: "Building the Loop: The Role of Ethnography in Artificial Organisational Intelligence"
    people: [{name: "Ellie Rennie"}, {name: "Kelsie Nabben"}, {name: "Michael Zargham"}, {name: "Jason Potts"}, {name: "Brooke Ann Coco"}, {name: "Luke Miller"}, {name: "Matthew Green"}]
    url: https://doi.org/10.1111/epic.70009
    read_on: "2026-11-14"
    shows: "EPIC Proceedings 2025(1), 223-235 (Crossref issued 2025-11; the EPIC page lists 19 January 2026): the question is how the loop is built, not whether a human is in it."
    claim: sourced
    note: "The page says 2025, the proceedings volume's year."

  # optional, only if the attention paper is named (not in the 92-word paragraph)
  - id: 2025-attention-economies
    date: "2025-08-30"
    kind: paper
    title: "Online Governance Surfaces and Attention Economies"
    people: [{name: "Nathan Schneider"}, {name: "Kelsie Nabben"}, {name: "Ronen Tamari"}, {name: "Michael Zargham"}]
    url: https://osf.io/preprints/mediarxiv/cdrmp_v1
    read_on: "2026-11-14"
    shows: "OSF preprint on MediArXiv, published 30 August 2025 (OSF API); heuristics for whether the structure of attention in a system is appropriate, efficient and just. Abstract read; the full text not."
    claim: sourced
```

URLs are unique in the record and plain absolute https. The names Jeff Emmett, Alvin Roth, Kelsie Nabben and Ellie
Rennie are new to the page; the tests tie each name to the yaml `people` lists, which these entries supply, and each
year (2019, 2023, 2025) to an entry date. Entries default to listed, so the generated reference list gains four
lines; `listed: false` on any he would keep to the paragraph only. The `doi.org` links answer 403 to automated
requests, which the link checker reports as `blocked`, not failed; the Medium original is not used.

## Two candidate placements

**A. After the synthesis paragraph, before the client-projects paragraph.** Before: "...<Zargham> as a maintainer
across OpenSysML; in our own account, this project is part of a synthesis effort to make our learnings accessible."
After: "In our own account, Jakob Hackel and Carolina Riascos-Álvarez worked on client projects we cannot name..." Reads
as: the people and the firm, then the ideas behind the work, then the confidential clients. It keeps the page's
time order, the lineage coming after the dated history.

**B. After the opening paragraph, before "Before the firm".** Before: "...studying the spaces of feasible designs
of their systems under uncertain, strategic and adversarial users." After: "Before the firm: Zargham's convex
optimization (2014) and, with Victor Preciado, geometric programs..." Reads as: what the firm does, then the idea of
design spaces and who chooses (it picks up "spaces of feasible designs" directly), then the history. The 2019 start
of the lineage then comes before the 2014 work, which breaks the page's time order.

## Word counts (the test's own counter, `tests/test_site.py::_history_text`)

- Page today: **377** visible words. The scope's "397" is `WORDS_CEILING`, the test ceiling; a plain `split()` over
  every text node gives 398 because entities split "Zargham&rsquo;s" in two.
- Paragraph alone: 92 words by plain split. Page after, with the links and name spans, either placement: **469**.
- The ceiling test (`250 <= words <= 397`; its comment says the ceiling goes down only) fails at 469. His choices:
  raise the ceiling to 469 with the reason in the test comment; or hold 397 by deleting 72 words of what is there
  (the marginal-value test the repository asks of existing content); or shorten the paragraph. The unit proposes no
  deletions.
- Without the final sentence the paragraph is 71 words and the page 448.

Nothing was written outside `work-packages/WP52-rounds/spike/`; `history.yaml`, `site/history.html` and the tests are
unchanged (the counts came from a copy in the scratchpad directory).

## The supervisor's corrections (2026-11-14, 03:25; `WP52-decisions.md`)

- "why is their data" is "Why Is There Data?" (Sisson and Ben-Meir, SSRN 4933063): his spelling, confirmed. He is not an
  author; it is available as a fourth link in the paragraph if he wants the firm's circle named, with a `history.yaml`
  entry like the others.
- The attention-economies paper is the OSF preprint (Schneider, Nabben, Tamari and Zargham, 2025). He presented it at
  the Workshop on the Ostrom Workshop; that fact enters `history.yaml` on his authority ("on the author's word") only
  if the paragraph names the paper.

