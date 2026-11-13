# WP33 — D-4: the wayfinding rounds

Twelve rows per round. The readers' returns are verbatim under `WP33-wayfinding/baseline/` (P1 to P8, head 60f92d9),
`WP33-wayfinding/repeat/` (P1 to P8, head df0cad9) and `WP32-cells/` (U1 to U4). Steps are pages opened or links
followed, as each reader counted them. The baseline and the repeat used different readers: four readers with two persona
passes each, then eight readers with one persona each (noted in the review, F-8). The repeat readers read text only.

## Round 1: baseline (head 60f92d9)

| Persona | Surface | Need | Steps | Bounce point | Skipped | Found it |
|---|---|---|---|---|---|---|
| P1 decision maker | root | what trades against what; whether to trust | 5 | root names no reader; three equal cards; the abstract is jargon | Prior art, notation, theorems, install, API | partly |
| P2 trade-study practitioner | root | run, rerun and defend | 7 | `/docs/user-guide/` guessed, a bare listing | paper, API, glossary, Choosing K, Chart | mostly yes |
| P3 modeller | docs Home | plug an evaluation in; what must hold | 6 | what must hold spread over three pages; no hand-off from a model's export | install, figure code, API, Termination | partly |
| P4 ML practitioner | docs Home | where it sits beside PCA; how to use it | 4 | "the two chain" asserted, never shown | install, report prose, derivation sentences | mostly |
| P5 optimization reader | `/paper/` | check the mathematics | 6 | "Loading..." placeholders; wide tables clipped; hypothesis codes need a side trip | Section 1 prose, Section 2, Sections 8 to 9, C, G | yes, largely |
| P6 neighbouring researcher | `/paper/` | new or a renaming | 5 | new names before Section 2 says so; stochastic-frontier entry weakest | Sections 3 to 6, 8 to 9, B, C, F | yes, with effort |
| P7 systems engineer | root | are the case's choices how a program behaves; where is it a toy | 6 | "the case page" off-site and invisible; root silent on the case | root Why/What, API, Sections 4 to 7, A, B, D | yes, in C.8 |
| P8 executive | root | would it change a decision; cost; what it does not tell | 7 | cards by route; abstract unreadable; cost to adopt unsized | code, Sections 2 to 7, appendices | partly |
| U1 package user, plain table | docs, README | fit a plain table | 8 pages (round 2, a3a61af) | `tension_report` band error at small subsets (fixed since) | Overview, Termination, Limitations, API, Examples | yes |
| U2 package user, SysML model | docs, README | model source to a table to a fit | 13 (round 3) | `tension_report` band error at the selected temperature | not listed in the return | yes |
| U3 package user, plain table | docs, README | fit a plain table | 9 (round 2, a3a61af) | none the docs owe | Overview, Prediction, Termination, Limitations, API | yes |
| U4 package user, SysML model | docs, README | model source to a table to a fit | 10 (round 3) | same band error as U2 | not listed in the return | yes |

P1 to P8 total 47 steps.

## Round 2: repeat (head df0cad9)

| Persona | Surface | Need | Steps | Bounce point | Skipped | Found it |
|---|---|---|---|---|---|---|
| P1 | root | as above | 4 | "Decide what adopting it would change" lands on D.17, mid-appendix | tool doors, Check the mathematics, Sections 2 to 7, `/docs/`, history | partly |
| P2 | root | as above | 3 | none (hesitated between the two "run" doors) | paper, decide and mathematics doors, Choosing K | yes |
| P3 | docs Home | as above | 4 | "your own data" does not say evaluation stays outside the package | install, Overview, Fitting, Limitations, API | partly |
| P4 | docs Home | as above | 4 | "Place it beside PCA" lands on an Overview whose PCA comparison is one sentence | other user-guide pages, Examples, paper | partly |
| P5 | `/paper/` | as above | 4 | link text "Appendix B, L4.14 to L4.24" does not say it leaves the article | Section 2, Sections 8 to 9, C to G | partly, leaning yes |
| P6 | `/paper/` | as above | 3 | none (Appendix G not read) | Theorems 1 to 12, Sections 5 and 6, the case | partly to yes |
| P7 | root | as above | 4 | no door named for a systems engineer; the toy statement sits in C.8 and Appendix E | A, B, D, G, `/docs/` | partly to yes |
| P8 | root | as above | 4 | same "Decide" link; adoption cost an analyst's, not sized in effort | tool doors, A, B, E to G | partly |
| U1 (round 4, df0cad9) | root, README, docs | as above | 10 listed (root, README, 8 docs pages) | README's first fit gives a temperature without saying how to choose it; `uv sync` installs every group | Overview, Termination, Limitations, API, Examples | yes; the planted answer reached |
| U2 (round 3, unchanged) | docs, README | as above | 13 | as in round 1 | as in round 1 | yes |
| U3 (round 2, unchanged) | docs, README | as above | 9 | none the docs owe | as in round 1 | yes |
| U4 (round 3, unchanged) | docs, README | as above | 10 | as in round 1 | as in round 1 | yes |

P1 to P8 total 30 steps. No persona's steps rose. The U1 count is of everything the cell listed (it opened the root
page and checked out the README as well), so it is not comparable step for step with the 8 of round 2; the cell's stops
are in `WP32-cells/round-4/triage.md`. U2 to U4 were not re-run after the fixes.

## Reading

Closed, fixed since and listed bounce points: `WP33-decisions.md`, "D-3: triage of the repeat round".

## After the round

The root page's doors changed after round 2 (the supervisor's rulings of 2026-11-14, WP33-decisions.md): five doors and the adoption line became "Read the paper" and "Use the tool" under the lead sentence, which now closes the page; the tables above describe the page as it was measured.
