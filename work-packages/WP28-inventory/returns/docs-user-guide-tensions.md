# docs-user-guide-tensions

## Q1
The page shows how to call `tension_report` and read each field of what it returns (contending set and n-lemma, participation and elasticities, near-frontier association, tension directions, the K > 1 case), with a worked example where a one-term fit hides a cap and a slope, and a closing statement of what a report cannot say.

## Q2
Home page: "It then tells you which metrics contend, with what elasticity, where each design sits relative to the fitted reference surface, and where the table has gaps" and the "User guide: one page per task, from conditioning your attributes to reading what the fit reports." Root page: "a guide per task from conditioning your attributes to reading a tension report."

## Q3
Verdict: advances. The Home page promises that the package tells you which metrics contend and with what elasticity, and the root page names "reading a tension report" as the end of the guide. This page is the only one in the list of units that explains how to read the report's fields (contending set, elasticities, association, directions). The paper's Figure 8 (fig-tensions-k3) and the Examples page show reports, but they do not teach the reading field by field.

## Q4
Not applicable.

## Q8
- Against the Home page: it delivers "which metrics contend, with what elasticity". It does not deliver "where the table has gaps", but another page may carry that. The PCA chaining sentence ("PCA finds where the data spread, this finds where they stop, and the two chain") is served by the "Tension directions" section.
- Against the root page: it serves "reading a tension report" in the Documentation card and "PCA explains variance; this explains tensions". The n-lemma is used as a term without being defined on the page; the root page and the paper define it.
- Against its own opening sentence ("returns a frozen TensionReport that says which metrics contend and how they trade ... describes a tension, where PCA would describe spread"): the page does this. The contending set and elasticities say which metrics contend and how they trade. The directions section ties back to PCA. The "A cap can hide a slope" section is a worked caution that goes a little beyond "how to read", but it is about reading a monolemma correctly.

Sections that serve none of the three: none clearly. "A cap can hide a slope" comes closest. Its first words are "A term reported as a monolemma is a cap". It is about the K > 1 fit, which the Fitting page presumably carries, so here it serves the reading of a monolemma and not the opening sentence directly.

## Q9
- "min_exponent must be 0 for this reading" and "the report warns when the estimator was fitted with a floor": I could not place what min_exponent is, because it is not introduced on this page.
- "absolute log V below band" and "closure_note": V is never defined on this page.
- "The report solves the tau = infinity program itself, independent of the fit temperature": I could place the claim, but not why a first-time user needs it.
- The figure label "Figure 3" on a page that shows only one figure.
