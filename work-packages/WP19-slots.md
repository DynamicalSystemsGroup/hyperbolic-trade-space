# WP19 D-1: the figure slots of the paper, by section (stage 1)

Written 2026-11-09 by the WP19 lead under `WP19-scope-of-work.md` (approved by the driver at 7f162c6).
Base: `dev` at 363019f. Every judgement of an existing figure below was made from its rendered image
(the PNG under `paper/figures/` opened in an image view), never from code or text. The standing
reminder, the supervisor's words: "i want you to remind our team to look at images/screenshots not
just code and text because we're building this for humans."

## R-1: the figures the paper has

Script (run at 363019f; the supporting material carries no figure):

    uv run python -c "import json,re
    for n in ['paper/paper.ipynb','paper/supporting_material.ipynb']:
        nb=json.load(open(n)); md=''.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='markdown')
        print(n, re.findall(r':::+\{figure\}\s*(\S+)\s*\n:label:\s*(\S+)', md))"

Output: `paper.ipynb`: `fig-tau` (cell `fig-tau-sweep`, Figure 1), `fig-plane-1` (`fig-plane-k1`, Figure 2),
`fig-plane-3` (`fig-plane-k3`, Figure 3), `fig-chart-3` (`fig-chart-k3`, Figure 4), `fig-tensions-3`
(`fig-tensions-k3`, Figure 5), `fig-regimes-1` (`fig-regimes`, Figure 6), `fig-predict-check-1`
(`fig-predict-check`, Figure 7). `supporting_material.ipynb`: none. Each is in a slot below (S-c1, S-d1 to S-d6).

## Fixed by the supervisor (non-goals; not re-decided here)

- The three-pane figure (`paper/figures/figure1.py`) stays out of the paper's body; the index page is its
  one consumer. A hero slot for the paper is a new decision, not a restoration.
- The cubesat exponent ternary by subsystem (groups) is dropped as "vacuous"; a sentence carries it. No
  candidate below is that plot or a variant of it.
- The tension heatmap stays (liked; "you can resize it but don't rework it"); docs Figure 8 (the planted
  ternary) stays as drawn.
- No figure is redrawn for a phone; no figure that conveys its intent is redrawn.

## Reader evidence carried in (WP11 round 1 and round 1b, depth B; `WP11-round-1/triage.md`)

- Figure 2 (planes, K = 1) helped 6 of 6 and is the anchor; Figures 1, 2, 3 earn their places.
- Figure 1 (temperature sweep) read as the temperature selection by 4 of 6.
- Figure 3: the bottom panel shows a metric quantised into horizontal bands; P3 and P6 inferred a
  discrete design variable that nothing they read names. Owed: a caption clause naming the discrete
  alternative behind the bands.
- Figure 4 (chart, K = 3) helped least: "coloured dots on unexplained Z coordinates" (4 of 6, round 1);
  "I saw clusters by colour but took nothing from it I could repeat" (2 of 6, round 1b).
- Figures 5 and 6 (association heatmaps): the "w = ..." boxes are now read from the caption (CR-4's
  clause landed before round 1b); Figure 5 dense for three readers, most useful to P5.
- Figure 7 (predicted against measured): "could not tell good from bad" (4 of 6, round 1); read by all
  six in round 1b as "predictions matched measurements for three proposed designs", with no sense of what
  was proposed, why there are two panels, or what a bad position would look like.
- P6 will judge at Section 9 whether the facets give more than per-cluster correlations; Figures 5 and 6
  are the analysis, the exponents per facet are the model's reading (for the section's prose, not a figure).

## The slots

Verdict key: **slot** (a figure carries something the sentence loses; a candidate is made and read),
**keep** (an existing figure; goes through the loop in its subpackage), **no figure** (the sentence
loses nothing; nothing is drawn), **open** (sentence test first in its subpackage, recorded there).

### 19a Front and concept (abstract, Sections 1 to 7)

| Slot | Where | Purpose (one sentence) | Shows | Does not show | Sentence; verdict |
|---|---|---|---|---|---|
| S-a1 | Title page, hero | Give an L-A reader the idea in one picture. | (three-pane: sheets, facets in log space, the chart) | | "The method fits a kinked reference surface and reads each design's position and level against it." **No figure in the body** (the supervisor's decision; the index page carries the three-pane figure). |
| S-a2 | 1 The decision problem | Show what a trade-study table looks like and what it hides. | | | "A trade study today is a grid or table in a document; it ranks but does not say what trades against what." **No figure**: the sentence loses nothing. |
| S-a3 | 2 Prior art | Place the method among its families. | | | The family table carries it. **No figure.** |
| S-a4 | 3 Notation (the pipeline) | Show configuration to attributes to metrics to identification and analysis. | | | "A configuration is evaluated into attributes, which the analyst conditions into metrics; the method identifies and analyses." **No figure**: four nouns in a row; 19b's model views show the case's first arrow concretely. |
| S-a5 | 4 Definitions, beside Definition 5 (the n-lemma) | Make the n-lemma visible as the face of the simplex that holds a facet's exponent vector. | For three metrics, the simplex as a triangle: a corner is one binding metric, an edge a dilemma, the interior a trilemma; each fitted facet's exponent vector as a point in the face that names its n-lemma, beside the planted vector it recovers; the weight the three metrics carry printed (1.00 at d = 3). | Designs, levels, the surface; more than three metrics (a three-metric face of a larger simplex shows exchange rates among those three only, with the weight printed); anything about the cubesat. | "An exponent vector lies on the simplex, and the smallest face holding it names the n-lemma: corner, edge, interior for one, two, three contending metrics." **Slot**: the sentence states the rule; the picture lets a reader place a facet by eye (hypothesis tested in 19a; if the reads show the sentence suffices, it is dropped). |
| S-a6 | 5 Methods, 6 Results | Picture the facets, the soft maximum or the chart. | | | The theorems are read in symbols at L-C; the case's Figures 2 and 3 show facets on data. **No figure.** |
| S-a7 | 7 Search (preliminary) | Picture the nested loops. | | | "Identify, propose along the facets' normals, evaluate, refit, repeat." **No figure**: future work with no results. |

### 19b The system model (Section 8, or Appendix C if the body does not take them)

| Slot | Where | Purpose | Shows | Does not show | Sentence; verdict |
|---|---|---|---|---|---|
| S-b1 | 8 Case construction (first paragraph) | Show what a configuration of the cubesat is: its parts, the alternatives swapped, the parameters tuned, with their ranges. | Every part of the cubesat and how it assembles; the two kinds of configuration variable (swap: wheel class, tracker grade; tune: panel span, battery capacity, gains) marked once each; levels and ranges read from the model. | The physics or the simulation; the attributes and metrics; which configurations were sampled or are feasible. | "The configuration swaps one of three wheels and one of three trackers and tunes the panel span, the battery capacity and two gains within ranges." **Slot**: the sentence lists variables; the picture shows where each sits in the assembly, which a P3 modeller needs to map it onto their own model. |
| S-b2 | 8 Case construction (after the regimes) | Show how the ten traded metrics relate to the requirements and the functional subsystems, and which are traded with no requirement on them. | Requirements grouped by subsystem (controls, power and energy, mass), a line from each to the metric it reads, the metrics with no requirement dashed, the requirements with no traded metric apart, and what computes each metric (the analysis, the measured slew). | Requirement thresholds or whether designs pass; the numbers; the conditioning; the fit. Requirement placement in a subsystem is the analyst's reading (said in the image's legend). | "Six of the ten traded metrics are read by a requirement; control effort, pointing error, peak slew power and total mass are traded with none." **Slot**: the chain from model to traded metric is the supervisor's ask ("a clear logical train of reasoning from the sysmlv2 model to the metrics we're trading"); the tested hypothesis decides. |

### 19c Case construction (Section 8)

| Slot | Where | Purpose | Shows | Does not show | Sentence; verdict |
|---|---|---|---|---|---|
| S-c1 | 8, Figure 1 (`fig-tau-sweep`) | Show how the temperature is selected and what it costs. | The fraction above V = 1 and the effective sample size against τ, the target fraction and the selected τ; each metric's exponent along τ. | That the selected τ is right for any other purpose; the fit's quality; the K > 1 fits. | "The selected τ puts the target fraction of designs above V = 1, at the cost of a small effective sample, and the exponents move little across τ." (Numbers are the paper's generated sentence, not typed here.) **Keep** (read as the temperature selection by 4 of 6); the exponent panel carries the stability the sentence only asserts. Loop in 19c. |
| S-c2 | 8, the planted table | Show that the fit recovers known facets. | | | The recovery sentence and Appendix D.14 carry it. **No figure.** |

### 19d Case analysis (Section 9)

| Slot | Where | Purpose | Shows | Does not show | Sentence; verdict |
|---|---|---|---|---|---|
| S-d1 | 9, Figure 2 (`fig-plane-k1`) | Show the one-facet fit as a line of trade-off in a log-metric plane. | Designs in the plane of the facet's two largest exponents, the facet's line and the near-frontier band. | The other eight metrics (a projection: a design below the line here can be on the surface); the Pareto boundary. | "At K = 1 slew time and control effort trade along one line." **Keep** (the anchor, 6 of 6). |
| S-d2 | 9, Figure 3 (`fig-plane-k3`) | Show that three facets bend the surface and colour the designs by the facet that dominates them. | Three planes with the facets' lines and the designs by facet. | That a facet is a set of designs; a kink outside the drawn planes. | "At K = 3 the surface bends: different pairs trade on different facets." **Keep; caption clause** naming the discrete alternative behind the bands of the bottom panel (CR-4, round 1b; the alternative is read from the data in 19d, not assumed). |
| S-d3 | 9, Figure 4 (`fig-chart-k3`) | Show where designs sit along the surface (the chart's position) and that facets occupy different regions. | First three position coordinates by facet, near-frontier outlined. | Meaning of a single Z coordinate; the level. | "Designs of different facets occupy different regions of the chart's position." **Open (CR-4)**: fails the cold read as drawn; in 19d re-slot (Appendix D), redraw at most twice, or drop with this sentence. |
| S-d4 | 9, Figure 5 (`fig-tensions-k3`) | Show which metrics trade (negative association) on each facet and the contending set. | Association among near-frontier designs per facet; the exact-maximum support outlined; w per metric. | Causation; the exponents' uncertainty; designs. | "Facet 1 trades slew time against control effort, facet 2 control effort against energy balance, facet 3 pointing error against peak slew power." **Keep** (liked; "w" clause landed; no rework). |
| S-d5 | 9, Figure 6 (`fig-regimes`) | Show what the gains contribute: the contending sets of the two regimes differ. | The K = 1 association maps of the primary and stock regimes with their contending sets. | The K = 3 facets; designs. | "With stock gains mass leaves the contending set and power margin enters." **Keep** ("w" clause landed); 19d asks whether S-d6 serves the same purpose better. |
| S-d6 | 9, beside Figures 5 and 6 (new) | Show "one facet blends what three separate" at a glance, on the three metrics both regimes share. | The exponent vectors of the K = 3 facets and of both K = 1 fits on the three shared metrics (slew time, control effort, pointing error), with the weight each carries on them printed. | The other seven metrics (the printed weight says how much is left out); designs; a subsystem grouping (dropped). | "The one-facet fit sits between the three facets on the shared metrics." **Open**: spike readout 2; sentence test first in 19d. |
| S-d7 | 9, Figure 7 (`fig-predict-check`) | Show that the regressor places proposed designs where measurement puts them. | Predicted and measured chart positions of three proposals over the cloud, two coordinate planes. | Why these designs were proposed; what a bad prediction would look like; the level. | "Each proposal's measured chart position lies close to its predicted one." (The distances are the paper's generated sentence and table.) **Open (CR-4)**: fails the cold read as drawn; in 19d re-slot, redraw at most twice, or drop with this sentence (the predict-check table carries the numbers). |
| S-d8 | 10 to 12 Discussion, reproducibility, future work | | | | **No figure.** |

### 19e Appendices (supporting material)

| Slot | Where | Purpose | Shows | Does not show | Sentence; verdict |
|---|---|---|---|---|---|
| S-e1 | D.11 or D (stability of the several-term fit) | Show how firm each facet's exponents are under resampling. | Resampled exponent vectors around each facet's fitted one. | The grouped (by subsystem) triangle of the spike (`spike-ternary/D-cubesat-stability.png`) is that dropped plot's form and is not the candidate. | "Two facets are firm; the dominant facet's mass share moves." **Open**: the stability tables may carry it; sentence test first in 19e, a candidate only on ungrouped metrics. |
| S-e2 | D, the chart of K = 3 if re-slotted | Home for S-d3 if it leaves the body. | | | Decided in 19d. |
| S-e3 | C, the model views if the body does not take them | Home for S-b1, S-b2 (the scope's default sends a failing view to the model's documentation instead). | | | Decided in 19b. |

## Counts

Slots with a candidate to make or read: S-a5, S-b1, S-b2 (new); S-c1, S-d1, S-d2, S-d4, S-d5 (keep);
S-d3, S-d6, S-d7, S-e1 (open). No figure: S-a1 (supervisor), S-a2, S-a3, S-a4, S-a6, S-a7, S-c2, S-d8.

## Outcomes (stage 2 and 3; the record is `WP19-figure-review.md`)

| Slot | Outcome |
|---|---|
| S-a5 | Candidate passed (two reads); ready for placement as P-1. |
| S-b1, S-b2 | Passed (two reads each); ready as P-2, P-3 (copies of the model's views in `paper/figures/`). |
| S-c1 | Kept as is (two reads); P-4. |
| S-d1 | Kept; caption gains the slice clause (P-5). |
| S-d2 | Kept; caption gains the band clause and the slice clause, two caption steps, four reads (P-6). |
| S-d3 | Dropped by the sentence test with the WP11 evidence; sentence kept (P-7). |
| S-d4 | Kept; caption gains the association clause (two reads; P-8). |
| S-d5 | Kept; caption gains the "w" clause and the association clause (two reads; P-9). |
| S-d6 | No figure (sentence test: the form of the dropped cubesat triangle). |
| S-d7 | Dropped by the sentence test: the image conveys "matched", the finding says positions missed; the generated sentence stays (P-10). |
| S-e1 | No figure (a resampling analysis is not in the paper; the grouped form is dropped). |
