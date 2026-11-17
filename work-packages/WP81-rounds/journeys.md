# WP81 R-8: the twelve journeys traced through the pages that point at the paper

Before any edit (the scope's order of work). Each journey is the row of `notes/user-journeys.md` for its persona
(`notes/reader-grid.md`), traced by a fresh-context reader in that persona over the staged site composed at the WP81
base in abstract mode (`scripts/assemble_site.py --slot abstract`), with one screenshot per page of the path in
`captures/` (1280 px, light; `captures.json` holds each page's height and console errors). The reader was given the
screenshots and the visible text of the pages on its path and nothing else, and asked, per page: what it wanted
there; where it met a pointer to the paper and what it expected the link to give; what, knowing the paper is a
working paper with its abstract alone published, it would want in that sentence instead; and what on the page is the
paper's job rather than the docs'. Their words are quoted; the triage and the competing preferences follow in
section 2, the disposition per pointer in `notes/paper-references.md`.

## 1. The journeys, verbatim

One file per persona in `journeys/`: P1 to P8, U1 to U4, as returned on 2026-11-17 (the folder's README notes the
root page's missing figures in the stage the readers saw).

## 2. Findings per pointer, and the competing preferences

**What every persona agreed on.** A pointer that lands on the abstract page breaks trust in proportion to what it
promised: "the argument and the proofs" (root, home) and "Appendix E", "Figure 1", "the chart theorem" (theory,
temperature, limitations, bridge) were named by every reader who met them; pointers inside the docs were never
complained of. All twelve want the paper's state said plainly where the paper is named ("working paper", "abstract
only online", "builds from the repository").

**Where the personas part.** The users (U1 to U4, P3, P4, P8) want the pointers gone from the pages they work on:
"I don't need the argument to run a fit" (U2), "remove it from the home page body" (P4), "drop the pointer from the
body and keep one honest link" (P1). The theorists and the sceptic (P5, P6) want each pointer to resolve to
something: the lemma scripts, the statement in the docs' words, or the built paper, and would go to the repository
("at that point I would go to the repository, not the paper", P5). The practitioner (P2) wants a derivation to hand a
reviewer. The engineers (P7, P8) want the one engineering finding behind a pointer (the bridge's battery finding)
stated with its numbers rather than cited. His rule ("Remove until a pin"; the two jobs) decides for the users on the
pages and serves the theorists through the two naming sentences, which say how the full text builds and where the
lemma scripts are, so that a P5 reader has a route that does not dead-end. Where a pointer carried a result a user
needs, the result is stated in brief; where it carried the paper's job, it goes.

| # | Pointer (surface) | Met by | What they wanted | The choice and its reason |
|---|---|---|---|---|
| 1 | home, "The paper makes the argument for the method; the project page links it" | P1, P3, P4, U1, U2, U3, U4 | all: drop from the first line or say "working paper, abstract only"; U1: "links it is a confusing pronoun"; P4, U3: the best line on the page is the PCA contrast, buried last | removed from the opening; the naming sentence (the working paper, its abstract at `/paper/`, the full text from the repository) goes at the foot of the page after the PCA line; the first line keeps its user-facing clause |
| 2 | theory, "definitions only, no proofs; the paper has them" | P5, P6 | P5: name the lemma or where the proofs are; P6: "reassurance, not a missing piece" | "the paper has them" removed; the sentence reads "definitions only, no proofs"; Further reading says where the proofs and the lemma scripts are |
| 3, 4, 5 | theory, the links on "doubling every metric doubles V", "a convex program", "The map is reversible" | P5, P6 | P5: the one-line reason in the docs' words; P6: the reversibility's condition stated | links removed; the statements stay (each already in the docs' words and backed by its lemma in the register); the reversibility sentence already states its condition |
| 6 | theory, "n-lemma (def), drawn in Figure 1 of the paper" | P5, P6 | both: "Figure 1 of the paper" is dead text; inline a figure or drop | the figure clause removed; "n-lemma" links the glossary |
| 7, 10 | bridge, "the bridge to the search direction of Future work", "the outer loop of the search named in the paper's Future work" | P7, U4 | U4: "planned, not part of this release"; "the outer loop is: propose, evaluate, append, refit"; P7: "planned, not shipped; see What this release ships" | both rewritten in the docs' words without the paper: the search loop is planned and not shipped (the page's own list says what ships); the outer loop named by its steps |
| 8 | bridge, "(the chart theorem)" | P7, U4 | U4: link Theory in brief | the link now points at the theory page's reversibility statement |
| 9 | bridge, "(Appendix B, section 6)" on the battery finding | P7, U4 | P7: "state the finding with its numbers; I want to know how deep the discharge went"; U4: keep the finding, drop the pointer | the appendix pointer removed; the finding stays as the docs state it; its numbers are the case's and belong to package 4 or 6 if the page is to carry them (noted) |
| 11, 12 | temperature, "(definition)" and "the n-lemma's members" | P5 | P5: the definition itself, one equation, or a docs definition | both link the glossary's entries (the docs' own definitions); no equation added here (the page's budget; package 5 may add it) |
| 13, 14 | temperature, "lemma 5 in Appendix E", "lemma 22 in Appendix E" | P5 | P5: "the page already states each result in words; keep that; the lemma number is a bonus for people like me" | the appendix links removed; the results stay in words; the lemma numbers stay as "lemma 5 of the lemma scripts" with no link, which serves P5 without a dead end |
| 15 | examples, "SysML v2 system model (sect-case-construction)" | P3, P7, U2 | all three want the model shown or its path; none wanted the paper's section | the link removed; the next sentence's GitHub path to `examples/adcs/` stays; showing the model is package 4's |
| 16 | further reading, "how this work differs" on HoroPCA | P6 | P6: "the link should go, or become a sentence stating the difference"; also wants a DEA sentence | the link replaced by one clause in the docs' words (HoroPCA fits a frame in hyperbolic space; this work fits a convex soft maximum over the simplex; backed by the WP35 readout); the DEA sentence noted for package 5 or 6; this page carries the second naming sentence (the working paper, its literature review and proofs, how it builds, the lemma scripts in `derivation/`) |
| 17 | fitting, "`n_terms=K` terms (thm-extension)" | P2, P4, U1, U3 | none asked for the paper; U1: the several-term options are "research-grade" | the link removed; "terms" links the glossary |
| 18 | termination, "`certified` (thm-certificate)" | P5, U3 | P5: wants the certificate's statement; U3: "certified means trust it locally" | the link removed; "certified" links the glossary's certificate entry |
| 19 | limitations, "Appendix E of the paper states what they do and do not establish" | P5, P8 | P8: "the sentence before it is complete without it"; P5: "see derivation/ in the repository" | the clause removed; the sentence names the lemma scripts' folder `derivation/` |
| 20 | code owners, the paper's lifecycle | nobody in a journey (a maintainers' page) | P8 on the nav: "not for me" | the word "paper" stays as the governance object; "the working paper" where it names the document; the page's place in the nav is package 4's |
| 21 | root page, "The paper makes the argument and gives the proofs" and the card | P1, P7, P8, U1 | all four: "overstates", "the proofs promise is the one that bites"; P1: one honest link "Paper abstract"; U1: "point proofs to the derivation scripts" | the body sentence rewritten: the working paper makes the argument; its abstract is published here, the full text builds from the repository, the lemma scripts are in `derivation/`; the card's line per mode is the composer's (out of scope; in abstract mode it already reads "its abstract; the paper is iterated towards release") and is left |
| 22 | README | U1, U3 | both: "working paper, abstract only"; the repo map line is fine | the first paragraph names the working paper with its state; the map line unchanged |
| 23 | api-reference docstring "Theorem 1" | nobody in a journey | | out of scope (package text) |

**Recorded for later packages, from the same reads.** Package 3: Home's opening line and the PCA contrast's place
(P4, U1, U3). Package 4: the model shown or its path on the examples page (P3, P7, U2); code owners off the reader
path (P8); the cubesat as the first thing a reader meets (P7, P8, U1). Package 5: the glossary links at first use the
readers listed; a DEA sentence (P6); the figure numbering readers took for hidden paper figures (U1, P2). Package 6
or the case: the battery finding's numbers on the bridge page (P7). For the paper side: every reader of the abstract
page asked for one plain line saying it is the abstract of a working paper (sent to the v0.1 session).

## 3. After the edits

(the same journeys re-traced; before and after side by side)
