# WP38 landed record: paper unit N1 (slots paper-01 to paper-04)

Branch wp38nb from dev at 6007221. Sources edited, nothing executed; outputs are stale until the execution unit runs both notebooks once.


## paper-01

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 1.1 | define | paper/abstract, cell 0, abstract | routed | abstract: supervisor |
| 1.2 | split | paper/abstract, cell 0, abstract | routed | abstract: supervisor |
| 1.3 | cut | paper/abstract, cell 0, abstract | routed | abstract: supervisor |
| 1.4 | split | paper/abstract, cell 0, abstract | routed | abstract: supervisor |
| 1.5 | split | paper/abstract, cell 0, abstract | routed | abstract: supervisor |
| 1.6 | keep | paper/abstract, cell 0, abstract | routed | abstract: supervisor |
| 1.7 | split | paper/abstract, cell 0, abstract | routed | abstract: supervisor |
| 1.8 | routed | paper/the-decision-problem, cell 4, para 1 | routed | Announces the text instead of saying something, and the closing "Organization." paragraph  |
| 1.9 | cut | paper/the-decision-problem, cell 4, para 1 | applied |  |
| 1.10 | split | paper/the-decision-problem, cell 4, para 3 | applied |  |
| 1.11 | split | paper/the-decision-problem, cell 4, para 3 | applied |  |
| 1.12 | split | paper/the-decision-problem, cell 4, para 5 | applied |  |
| 1.13 | define | paper/the-decision-problem, cell 4, para 5 | not applied | a define adds a gloss; 'posynomial' is defined in Words and the reference to Definition 1 now sits in the same sentence |
| 1.14 | cut | paper/the-decision-problem, cell 4, para 5 | applied |  |
| 1.15 | split | paper/the-decision-problem, cell 4, para 5 | applied |  |
| 1.16 | keep | paper/the-decision-problem, cell 4, "Contribution." | left | keep |
| 1.17 | define | paper/the-decision-problem, cell 4, "Contribution." | applied |  |
| 1.18 | cut | paper/the-decision-problem, cell 4, count paragraph | not applied | generated sentence; tests/test_paper.py pins the range convention ('is printed as a range') |
| 1.19 | split | paper/the-decision-problem, cell 4, count paragraph | not applied | generated sentence, same pin |
| 1.20 | cut | paper/the-decision-problem, cell 4, Main results | applied |  |
| 1.21 | split | paper/the-decision-problem, cell 4, Main results 1 | applied |  |
| 1.22 | cut | paper/the-decision-problem, cell 4, Main results 1 | applied |  |
| 1.23 | define | paper/the-decision-problem, cell 4, Main results 2 | not applied | define would add words; term of art with the theorem references beside it |
| 1.24 | split | paper/the-decision-problem, cell 4, Main results 2 | applied |  |
| 1.25 | define | paper/the-decision-problem, cell 4, Main results 3 | not applied | define would add words |
| 1.26 | define | paper/the-decision-problem, cell 4, Main results 4 | not applied | define would add words |
| 1.27 | split | paper/the-decision-problem, cell 4, Main results 4 | applied |  |
| 1.28 | define | paper/the-decision-problem, cell 4, Main results 5 | not applied | define would add words |
| 1.29 | define | paper/the-decision-problem, cell 4, Main results 6 | not applied | 'Numerical' is a result-class label (claim status); left |
| 1.30 | keep | paper/the-decision-problem, cell 4, closing | left | keep |
| 1.31 | routed | paper/the-decision-problem, cell 4, Organization | routed | A sentence that lists the parts, six semicolon-separated items with a nested parenthetical |
| 1.32 | cut | paper/prior-art-by-family, cell 8, para 1 | applied |  |
| 1.33 | cut | paper/prior-art-by-family, cell 8, para 1 | applied |  |
| 1.34 | define | paper/prior-art-by-family, cell 8, Table 1 row Production | not applied | table cell is in paper/prior_art.yaml (data file, not in this unit's file set) |
| 1.35 | define | paper/prior-art-by-family, cell 8, Table 1 row Kernel PCA | not applied | same: prior_art.yaml |
| 1.36 | keep | paper/prior-art-by-family, cell 8, Table 1 row PCA | left | keep |
| 1.37 | cut | paper/prior-art-by-family, cell 8, Pareto methods | applied |  |
| 1.38 | keep | paper/prior-art-by-family, cell 8, Pareto methods | left | keep |
| 1.39 | define | paper/prior-art-by-family, cell 8, DEA | applied |  |
| 1.40 | define | paper/prior-art-by-family, cell 8, DEA | applied |  |
| 1.41 | routed | paper/prior-art-by-family, cell 8, DEA | routed | An aside that belongs with the title/definition, not in the DEA paragraph; moving it is a  |
| 1.42 | split | paper/prior-art-by-family, cell 8, HoroPCA | applied |  |
| 1.43 | define | paper/prior-art-by-family, cell 8, HoroPCA | not applied | define would add words (horospherical projections is the cited work's term) |
| 1.44 | split | paper/prior-art-by-family, cell 8, HoroPCA | applied |  |
| 1.45 | define | paper/prior-art-by-family, cell 8, HoroPCA | applied |  |
| 1.46 | split | paper/prior-art-by-family, cell 8, Lineage | applied |  |
| 1.47 | define | paper/prior-art-by-family, cell 8, Lineage | not applied | gloss or restructure would add words or touch a pinned sentence |
| 1.48 | split | paper/prior-art-by-family, cell 8, Lineage | applied |  |
| 1.49 | define | paper/prior-art-by-family, cell 8, Lineage | not applied | define would add words |
| 1.50 | routed | paper/prior-art-by-family, cell 8, Lineage | routed | "entropic risk functional" is unexplained jargon; the cite carries "n.d." (no date) and a  |
| 1.51 | define | paper/prior-art-by-family, cell 8, Lineage | applied |  |
| 1.52 | keep | paper/preliminaries-and-notation, cell 14, para 1 | left | keep |
| 1.53 | define | paper/preliminaries-and-notation, cell 14, Assumptions | not applied | define would add words (tau, kappa, Sigma named in Definition 4) |
| 1.54 | define | paper/preliminaries-and-notation, cell 14, Assumptions | not applied | define would add words; Definition 3 follows |
| 1.55 | keep | paper/preliminaries-and-notation, cell 14, Assumptions | left | keep |
| 1.56 | cut | paper/preliminaries-and-notation, cell 14, Map and territory | applied |  |
| 1.57 | keep | paper/preliminaries-and-notation, cell 14, Map and territory | left | keep |
| 1.58 | split | paper/preliminaries-and-notation, cell 14, Map and territory | applied |  |
| 1.59 | define | paper/preliminaries-and-notation, cell 14, Words | applied |  |
| 1.60 | keep | paper/preliminaries-and-notation, cell 14, Words | left | keep |
| 1.61 | keep | paper/preliminaries-and-notation, cell 14, Definition 1 | left | keep |
| 1.62 | split | paper/definitions, cell 15, opening | applied |  |
| 1.63 | keep | paper/definitions, cell 15, opening | left | keep |
| 1.64 | define | paper/definitions, Definition 2, cell 15 | not applied | forward pointer kept: defining beta here would add words |
| 1.65 | split | paper/definitions, cell 15, after Definition 2 | applied |  |
| 1.66 | cut | paper/definitions, cell 15, after Definition 2 | not applied | the first body statement of the negation; the other restatements were cut (1.73, 1.76) |
| 1.67 | split | paper/definitions, Definition 3, cell 15 | applied |  |
| 1.68 | routed | paper/definitions, Definition 3, cell 15 | routed | An implementation detail (what the package subtracts) in the middle of a definition of the |
| 1.69 | cut | paper/definitions, Definition 3, cell 15 | applied |  |
| 1.70 | define | paper/definitions, Definition 3, cell 15 | not applied | define would add words |
| 1.71 | keep | paper/definitions, cell 15, before Definition 4 | left | keep |
| 1.72 | split | paper/definitions, Definition 4, cell 15 | applied |  |
| 1.73 | cut | paper/definitions, cell 15, before Definition 5 | applied |  |
| 1.74 | define | paper/definitions, Definition 5, cell 15 | applied |  |
| 1.75 | define | paper/definitions, Definition 5, cell 15 | applied |  |
| 1.76 | cut | paper/definitions, Definition 5, cell 15 | applied |  |
| 1.77 | split | paper/definitions, Definition 6, cell 15 | applied |  |
| 1.78 | routed | paper/definitions, Definition 6, cell 15 | routed | The 10^−9 threshold is a number; whether to state it here or point to Section 5's threshol |
| 1.79 | split | paper/definitions, Definition 6, cell 15 | applied |  |
| 1.80 | define | paper/definitions, Definition 6, cell 15 | not applied | define would add words |
| 1.81 | cut | paper/definitions, cell 15, before Figure 1 | applied |  |
| 1.82 | routed | paper/definitions, Figure 1 caption, cell 15 | routed | "the case's association maps" is undefined at this point in the paper; and the Shows / Doe |
| 1.83 | split | paper/definitions, Definition 7, cell 15 | applied |  |
| 1.84 | keep | paper/definitions, Definition 7, cell 15 | left | keep |
| 1.85 | define | paper/definitions, Definition 9, cell 15 | applied |  |

## paper-02

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 2.1 | split | paper/methods, cell 18 "R1: at the exact-maximum" | applied |  |
| 2.2 | split | paper/methods, cell 18 "R3: at the clean fit" | applied |  |
| 2.3 | split | paper/methods, cell 18 "one term is a geometric program | applied |  |
| 2.4 | split | paper/methods, cell 18 "keeps one extreme design" | applied |  |
| 2.5 | split | paper/methods, cell 18 "These choices define the questi | applied |  |
| 2.6 | split | paper/methods, cell 18 "A row with a zero metric" | applied |  |
| 2.7 | split | paper/methods, cell 15/18 "participation threshold" | applied |  |
| 2.8 | define | paper/methods, cell 18/103 "docsite" | not applied | 'docsite' is the paper's own recurring word (also Section 11); left to a vocabulary decision |
| 2.9 | define | paper/methods, cell 18 "decomposition family" | not applied | scikit-learn's term, pinned by the conformance note; a gloss would add words |
| 2.10 | cut | paper/methods, cell 19 "We name each where it is made" | applied |  |
| 2.11 | split | paper/methods, cell 19 "For given terms a finite" | applied |  |
| 2.12 | split | paper/methods, cell 19 "the case needs three terms" | not applied | each clause carries a fact (three terms; why small K); no cut without losing one |
| 2.13 | split | paper/results, cell 20 "means proved from its hypothese | applied |  |
| 2.14 | split | paper/results, cell 20 "The hypothesis codes" | applied |  |
| 2.15 | cut | paper/results, cell 20 "The sentences between the boxes | applied |  |
| 2.16 | cut | paper/results, cell 27 "Three results say what the fitt | applied |  |
| 2.17 | split | paper/results, cell 29 "Gaussian noise of covariance" | applied |  |
| 2.18 | split | paper/results, cell 29 "The expected noisy objective is | applied |  |
| 2.19 | split | paper/results, cell 34 "a maximizer of $V$ is weakly Pa | applied |  |
| 2.20 | define | paper/results, cell 35 "each term is a monomial" | applied |  |
| 2.21 | cut | paper/results, cell 36 "The converse" | applied |  |
| 2.22 | split | paper/results, cell 36 "At $K>1$, $\kappa=\infty$" | applied |  |
| 2.23 | cut | paper/results, cell 36 "take the contrapositive" | applied |  |
| 2.24 | split | paper/results, cell 37 "the mean slack (how far" | applied |  |
| 2.25 | split | paper/results, cell 37 "Magnani" | applied |  |
| 2.26 | split | paper/results, cell 37 "The sharp weights give one labe | applied |  |
| 2.27 | split | paper/results, cell 37 "The labels are the alternation" | applied |  |
| 2.28 | split | paper/results, cell 38 "in an instance (" | not applied | itemised statement of the theorem; semicolons separate (i) to (iii) |
| 2.29 | define | paper/results, cell 39 "ill-posed (observed on planted  | not applied | 'planted' is used throughout and defined in Section 8; a swap adds words |
| 2.30 | split | paper/results, cell 39 "neither that plain fit nor the  | applied |  |
| 2.31 | split | paper/results, cell 41 "A8 (a partition into nonempty c | applied |  |
| 2.32 | split | paper/results, cell 41 "stationarity of the stop" | applied |  |
| 2.33 | cut | paper/results, cell 43 "tightness is not claimed" | applied |  |
| 2.34 | cut | paper/results, cell 44 "Global optimality is not claime | applied |  |
| 2.35 | define | paper/results, cell 42 "simplex KKT conditions of" | not applied | define would add words |
| 2.36 | split | paper/results, cell 47 "Soft-fit certificate: at a feas | applied |  |
| 2.37 | cut | paper/results, cell 48 "The fits of record are sharp" | applied |  |
| 2.38 | split | paper/results, cell 48 "For a sharp fit, certified mean | applied |  |
| 2.39 | cut | paper/results, cell 51 "Four questions are not establis | applied |  |
| 2.40 | split | paper/search-of-the-design-space-preliminary, cell 52 "A trade study also decides" | applied |  |
| 2.41 | cut | paper/search-of-the-design-space-preliminary, cell 52 "This section is future work" | applied |  |
| 2.42 | cut | paper/search-of-the-design-space-preliminary, cell 52 "There are nested loops" | applied |  |
| 2.43 | split | paper/search-of-the-design-space-preliminary, cell 52 "The middle loop proposes" | applied |  |
| 2.44 | define | paper/search-of-the-design-space-preliminary, cell 52 "noise band" | applied |  |
| 2.45 | routed | paper/search-of-the-design-space-preliminary, cell 52 "resembles a diffusion" | routed | A borrowed analogy with no result behind it, which reads as machine-supplied; cutting it r |
| 2.46 | cut | paper/search-of-the-design-space-preliminary, cell 12/52 "our reading" | applied |  |
| 2.47 | split | paper/search-of-the-design-space-preliminary, cell 52 "neither has a lemma here" | applied |  |

## paper-03

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 3.1 | cut | paper/case-construction, cell 53, "The design variables are" | not applied | the aside is not in the Figure 2 caption, and tests/test_paper.py pins it |
| 3.2 | split | paper/case-construction, cell 53, "The cubesat case is a worked e | applied |  |
| 3.3 | keep | paper/case-construction, Figure 2 caption, "Every name is read" | left | keep |
| 3.4 | routed | paper/case-construction, Figure 2, "Good for:" | routed | the caption template (Shows / Does not show / Good for) is a structure, not a sentence-lev |
| 3.5 | split | paper/case-construction, "Of the thirteen traded metrics" | not applied | generated; tests/test_paper.py pins 'Spearman at least 0.97' |
| 3.6 | cut | paper/case-construction, "We use two regimes" | applied |  |
| 3.7 | keep | paper/case-construction, "We use two regimes" | left | keep |
| 3.8 | split | paper/case-construction, Figure 3 caption, "an orange line" | applied |  |
| 3.9 | cut | paper/case-construction, Figure 3 caption, "Every traded metric i | applied |  |
| 3.10 | cut | paper/case-construction, Figure 3, "Does not show:" | not applied | Shows/Does not show/Good for line: template, left as routed |
| 3.11 | routed | paper/case-construction, Figure 3, "Good for:" | routed | restates the caption's first sentence; caption template is a structure |
| 3.12 | split | paper/case-construction, "Feasibility removes designs" | applied |  |
| 3.13 | split | paper/case-construction, "Feasibility removes designs" | applied |  |
| 3.14 | routed | paper/case-construction, "Feasibility removes designs" | routed | conditioning sits in the feasibility and cost paragraph where nothing leads to it; a place |
| 3.15 | cut | paper/case-construction, "Feasibility removes designs" | not applied | claims row C426 and a test pin it; sentence left |
| 3.16 | cut | paper/case-construction, "Feasibility removes designs" | applied |  |
| 3.17 | cut | paper/case-construction, "The primary regime evaluates" | not applied | generated datasets sentence; pinned in tests/test_paper.py |
| 3.18 | cut | paper/case-construction, "The primary regime evaluates" | not applied | generated, pinned in tests/test_paper.py |
| 3.19 | split | paper/case-construction, Figure 4 caption, "Top:" | applied |  |
| 3.20 | split | paper/case-construction, Figure 4 caption, "Bottom:" | applied |  |
| 3.21 | define | paper/case-construction, Figure 4, "Does not show:" | not applied | template line, left as routed |
| 3.22 | routed | paper/case-construction, Figure 4, "Good for:" | routed | caption template; "n-lemma" again undefined at second use |
| 3.23 | define | paper/case-construction, "The fit temperature is tau = 41.7" | not applied | generated; define would add words |
| 3.24 | split | paper/case-construction, "The fit temperature is tau = 41.7" | applied |  |
| 3.25 | cut | paper/case-construction, "The fit temperature is tau = 41.7" | applied |  |
| 3.26 | cut | paper/case-construction, "Figure 4 shows how" | not applied | the only in-text reference to Figure 4; cutting leaves the figure unreferenced |
| 3.27 | cut | paper/case-construction, "Figure 4 shows how" | applied |  |
| 3.28 | routed | paper/case-construction, "The worked example of Appendix C.7" | routed | planted-table detail belongs in the analysis's "A known answer" paragraph, not under the c |
| 3.29 | cut | paper/case-construction, "The worked example of Appendix C.7" | applied |  |
| 3.30 | cut | paper/case-construction, "The worked example of Appendix C.7" | applied |  |
| 3.31 | cut | paper/case-analysis, cell 69, "We read the case" | not applied | the sentence carries the only numref to Table 2 and pointers to Appendix D; left |
| 3.32 | split | paper/case-analysis, "A known answer." | not applied | generated, with two branches; reorder risks the unseen branch; left for the execution unit |
| 3.33 | define | paper/case-analysis, "One term." | not applied | define would add words |
| 3.34 | define | paper/case-analysis, "At K = 1 the exact-maximum fit" | not applied | generated; define would add words |
| 3.35 | define | paper/case-analysis, "At K = 1 the exact-maximum fit" | not applied | generated; define would add words |
| 3.36 | split | paper/case-analysis, Figure 5 caption, "Dark:" | applied |  |
| 3.37 | split | paper/case-analysis, Figure 5 caption, "Light:" | applied |  |
| 3.38 | cut | paper/case-analysis, Figure 5, "Does not show:" | not applied | template line, left as routed |
| 3.39 | routed | paper/case-analysis, Figure 5, "Good for:" | routed | caption template; restates the caption's first sentence |
| 3.40 | split | paper/case-analysis, "Two terms." | applied |  |
| 3.41 | cut | paper/case-analysis, "At K = 2 the tension separates" | applied |  |
| 3.42 | split | paper/case-analysis, "Each K selects its own fit temperature" | applied |  |
| 3.43 | split | paper/case-analysis, Figure 6 caption, "The position is measu | applied |  |
| 3.44 | cut | paper/case-analysis, Figure 6 caption, "grey:" | applied |  |
| 3.45 | routed | paper/case-analysis, Figure 6, "Good for:" | routed | restates the sentence "Figure 6 shows each design's level read apart from its position"; c |
| 3.46 | split | paper/case-analysis, Figure 7 caption, "Outlined:" | applied |  |
| 3.47 | routed | paper/case-analysis, Figure 7, "Good for:" | routed | caption template |
| 3.48 | cut | paper/case-analysis, "The K = 2 terms have contending sets" | applied |  |
| 3.49 | cut | paper/case-analysis, "The finding:" | applied |  |
| 3.50 | split | paper/case-analysis, "The finding:" | applied |  |
| 3.51 | cut | paper/case-analysis, "On term 2 the elasticity" | applied |  |
| 3.52 | split | paper/case-analysis, "Three metrics at a time." | applied |  |
| 3.53 | split | paper/case-analysis, "Three metrics at a time." | applied |  |
| 3.54 | split | paper/case-analysis, "Two regimes." | applied |  |
| 3.55 | cut | paper/case-analysis, "The regimes return a 7-lemma" | not applied | generated; pinned by tests/test_paper.py ('mass enters only in the stock regime') |
| 3.56 | cut | paper/case-analysis, "The regimes return a 7-lemma" | not applied | generated; pinned by tests/test_paper.py |
| 3.57 | keep | paper/case-analysis, "Propose, predict, check is" | left | keep |
| 3.58 | routed | paper/case-analysis, "Propose, predict, check is" | routed | spurious precision (2nd percentile, 300 holes) for a three-proposal check, and "pooled" an |
| 3.59 | routed | paper/case-analysis, "Propose, predict, check is" | routed | a caveat about a failure that does not occur in the 3 proposals; belongs in the appendix a |
| 3.60 | split | paper/case-analysis, "Of 3 proposals" | not applied | generated; values vary, reorder not safe unseen |
| 3.61 | cut | paper/case-analysis, "What the executives decide." | not applied | decision paragraph pinned by tests and claims rows |
| 3.62 | split | paper/case-analysis, "What the executives decide." | not applied | same |
| 3.63 | cut | paper/case-analysis, "What the executives decide." | not applied | same: test and claims row C-row quote it |
| 3.64 | cut | paper/case-analysis, Table 2 caption, "The baseline misses" | applied |  |
| 3.65 | cut | paper/case-analysis, Table 2 caption, "The method does not te | not applied | claims row C618 quotes it and no surviving sentence says it |

## paper-04

| Row | Flag | Surface and location | Result | Note |
|---|---|---|---|---|
| 4.1 | cut | paper/discussion, cell 100, Three claims | applied |  |
| 4.2 | split | paper/discussion, cell 100, Requirements after the fit | applied |  |
| 4.3 | split | paper/discussion, cell 100, Requirements after the fit | not applied | split not done: the sentence is shortened by 4.4; the remainder parses |
| 4.4 | cut | paper/discussion, cell 100, Requirements after the fit | applied |  |
| 4.5 | cut | paper/discussion, cell 100, What propose, predict, check s | not applied | generated; 'the easy part' pinned by a test and a claims row |
| 4.6 | split | paper/discussion, cell 100, What propose, predict, check s | applied |  |
| 4.7 | cut | paper/discussion, cell 100, What propose, predict, check s | applied |  |
| 4.8 | split | paper/discussion, cell 100, What propose, predict, check s | applied |  |
| 4.9 | keep | paper/discussion, cell 100, What propose, predict, check s | left | keep |
| 4.10 | cut | paper/discussion, cell 100, What propose, predict, check s | not applied | generated; 'remains a hypothesis' pinned by a test |
| 4.11 | define | paper/discussion, cell 100, Why a frontier | not applied | term of art is the paper's own use name; a gloss belongs in Section 1 |
| 4.12 | cut | paper/discussion, cell 100, Cross-application | applied |  |
| 4.13 | keep | paper/discussion, cell 100, Cross-application | left | keep |
| 4.14 | keep | paper/discussion, cell 100, Limits, in brief | left | keep |
| 4.15 | keep | paper/discussion, cell 100, Limits, in brief | left | keep |
| 4.16 | define | paper/discussion, cell 100, PCA | applied |  |
| 4.17 | keep | paper/discussion, cell 100, PCA | left | keep |
| 4.18 | split | paper/discussion, cell 100, Novelty and white space | applied |  |
| 4.19 | keep | paper/discussion, cell 100, The kernel direction | left | keep |
| 4.20 | keep | paper/discussion, cell 100, The kernel direction | left | keep |
| 4.21 | split | paper/reproducibility-and-your-own-case, cell 103 | applied |  |
| 4.22 | cut | paper/reproducibility-and-your-own-case, cell 103 | applied |  |
| 4.23 | split | paper/reproducibility-and-your-own-case, cell 103 | applied |  |
| 4.24 | keep | paper/reproducibility-and-your-own-case (12), cell 103 follow-on, Future work | left | keep |
| 4.25 | split | paper/reproducibility-and-your-own-case (12), cell 103 follow-on, Future work | applied |  |
| 4.26 | define | paper/reproducibility-and-your-own-case (12), cell 103 follow-on, Future work | applied |  |
| 4.27 | keep | paper/reproducibility-and-your-own-case (12), cell 103 follow-on, Future work | left | keep |
| 4.28 | cut | paper/reproducibility-and-your-own-case (12), cell 103 follow-on, Final remark | applied |  |
| 4.29 | routed | paper/reproducibility-and-your-own-case (13), cell 103 follow-on, Acknowledgments | routed | "Machine-checked" is stronger than the project's business-casual register for the lemma sc |
| 4.30 | split | paper/reproducibility-and-your-own-case (13), cell 103 follow-on, Acknowledgments | applied |  |

## Counts

{'routed': 26, 'applied': 126, 'not applied': 51, 'left': 24}

## Claims rows re-pointed (backing kept)

C004, C009, C011, C012, C016, C018, C022, C031, C038, C061, C075, C079, C082, C083, C090, C099, C108, C118, C125, C386, C403, C405, C409, C410, C461, C470, C471, C473, C493, C530, C531, C532, C565, C566, C617. C009 also moved to the anchor 'The decision problem'; C617 now points at the Figure 3 caption sentence; C016 and C461 point at the box titles that replaced the cut lead-in; C075's narrowed fragment drops the band and effective-sample-size clause.

## Ledger

Twelve [[cut]] rows added to paper/length_ledger.toml (2026-11-13). Rendered words from the sources (generated sentences as in the stale outputs): 10,354 before, 9,905 after (449 out). Generated-sentence cuts (temperature pointer, worked-example pointers, 'an association cannot give', 'Every term has an association reading') leave at execution and are counted then.

## Vocabulary baseline

Three stale first-use rows removed from scripts/vocabulary_baseline.toml (improvement factor, level offset, position along the frontier). check_vocabulary: 0 new.

## Checker

scripts/check_residuals.py --compare reads rendered or source counts; paper sources only shift after execution, so before/after for the paper pages is taken at the execution unit.

## Tests waiting for execution

tests/test_paper.py output-reading tests (generated sentences changed in paper/generate_findings.py: temperature, planted, choosing K, K temperatures, terms, elasticity, predict reading), the ledger count for generated cells, tests/test_residuals.py comparison on the rendered paper.
