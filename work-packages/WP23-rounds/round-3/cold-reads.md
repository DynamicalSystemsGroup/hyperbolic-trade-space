# WP23 round 3: the cold reads, verbatim, with their dispositions

Screenshots for this record: commit `c680853`, `git show c680853:<path>` with `<path>` under `work-packages/WP23-rounds/gate/`.

The two reports below are the records of the round-3 cold reads (D-10, R-8): a fresh P2 proxy
(practising engineer, depth L-B) and a fresh P3 proxy (systems modeller, depth L-C), each in its own
context, neither having seen rounds 1 or 2, each reading the image before the caption, on the folder
as round 3 left it (`assembly_view.png`, `behavioural_view.png`, `heatmap.png`, `heatmap_stock.png`,
`coverage.md`, `k3_record.md`, `INTENT.md`). Round 2 had no cold read of its own (it changed the
model and the coverage table only; its views were read here), and round 4 had none (it executed the
dispositions below and was checked by its author at 700 px). The reports are quoted as written and
are not edited. After each report, a table gives each finding's disposition and where it was
executed: the round-4 commit (`43e1a7f`, the round-3 dispositions on the views, the pair's regime
names) with the item of `WP23-review.md`, "Round 4"; "heatmap redraw after the gate" for the
heatmap's own drawing, which belongs to `case.tau_sweep_figure` (read-only for WP23; the list is
"Round 4", item 4); "noted, no change" with the reason; or "open" where the record holds no
disposition (listed for the PM in the review, "Rounds: the cold reads and their dispositions").
Neither reader tagged a finding [blocks].

---

# Round 3, P2 proxy (practising engineer, depth L-B), fresh context (had not seen earlier rounds), image before caption. Verbatim.

Cold sentences (written before INTENT.md, verbatim):

behavioural_view.png: "Nine requirements in three groups (controls, power and energy, mass) each point at one metric, and nearly all those metrics are produced by one SlewExperiment analysis from the configuration and a measured slew; three requirements at the top are deliberately left out of the trade." Colours/lines as read: orange = requirement (footer); green = traded metric; yellow = launch cost, derived from total mass, not traded; grey box = a measurement (data source); lavender box = the analysis that computes metrics; orange lines = requirement-to-metric trace; thin arrows = "feeds/computes"; dashed top box = requirements with no traded metric; "SlewVerification/ConfigurationVerification" = which test verifies the requirement.

assembly_view.png: "A cubesat is assembled from eight parts; the design freedom is two swappable parts (wheel class, tracker grade, three options each) and four tuned numbers (panel span, battery capacity, Kp, Kd), with bus, antenna and IMU fixed." Colours/lines: orange tag = swap (categorical), blue tag = tune (continuous); diamonds = "is made of"; open-triangle arrows = "is a kind of" (the alternatives); the boxed legend = the variable list and ranges.

heatmap.png: "As a 'temperature' tau grows, the fraction of designs above V = 1 and the effective sample size both collapse, a grey bar marks a chosen tau near 40 where the fraction crosses 0.1, and in the lower panel total mass takes a constant ~0.3 share at every tau while settling time fades out, energy balance and depth of discharge hold steady, and power margin, eclipse reserve, peak slew power and (almost) control effort get nothing." Colours/lines: blue = computed values at sampled tau; grey vertical bar = chosen tau; black horizontal = a 0.1 threshold; greyscale = some share or weight per metric per tau, white = 0, black = 0.3 (capped?); "inf" = the limit.

Findings:

1. [note] Behavioural view: cold read matches the intent on grouping, requirement-to-metric joins, the two sources and the three excluded requirements; the footer legend and the verification-case line are legible at 700 px and did their job.
2. [note] Behavioural view: what one look does not give is "reads through the element named in the metric's box" and "headless line = shared quantity, no direction"; I read the lower line of each metric box as an identifier and the orange line as a plain trace link, with no direction assumed, so nothing was misread, just not received (L-C material, fine for L-B).
3. [note] Behavioural view: pointing error is the only traded metric stereotyped «MoE»; nothing on the image or in the intent's caption text says why it differs from the «MoP» metrics, and a P2 notices the odd one out.
4. [note] Behavioural view, illegible at 700 px: the dashed box's title "requirements reading no traded metric" is light grey on white at the smallest type on the page; I had to squint, and "reading" there is an unfamiliar verb (I took it as "that use no traded metric").
5. [note] Behavioural view, ink as data: the right column between SlewMeasurement and SlewExperiment and the left two-thirds of each lane are empty; 861 px of height for nine metrics is sparse but the lines need the room, so not a redraw finding.
6. [note] Behavioural view, idiom: the lanes borrow the package/subsystem idiom, which would imply structure in the model; "(the analyst's grouping)" in each lane title defuses it, and I read them as the analyst's bins.
7. [note] Behavioural view, mislead: SlewExperiment says "computes 7 of the 9 metrics from the configuration and the measured inputs", but total mass comes from it while LaunchBudgetRequirement is ConfigurationVerification; the picture implies a mass number needs a slew, which I doubt, and it is the first thing I would ask the modeller.
8. [note] P2 verdict: the view convinces me the case has the shape of a real trade study (nine metrics with named sources, traced to requirements, binned by subsystem, honest that three requirements are gates not trades and that simulation stands in for measurement); what stops me buying it fully is that it is the "what is measured" half and not the "what trades" half: no requirement thresholds appear (the boxes say what verifies them, not what they demand) and the configuration variables of the assembly view appear nowhere on it, so I cannot see what is traded against what or whether anything binds.
9. [note] Questions for the modeller, from the behavioural view: are the three untraded requirements applied as pass/fail filters on every candidate, and how many candidates failed them; what are the thresholds behind the nine traded requirements and does any design in the data violate one; why is launch cost derived but not traded when total mass is; why total mass is a SlewExperiment output (item 7).
10. [note] Assembly view: cold read matches the intent except the count; I said eight parts, the intent says nine in eight kinds; "(panelPlus, panelMinus)" reads as two names on one box, not as two parts, so the picture does not carry "nine".
11. [note] Assembly view, ink as data: the text legend is roughly 45 per cent of the frame and is a table (levels and ranges) rather than a drawing; the sentence test says the tree carries "which parts, which swapped, which tuned, which fixed" and the ranges would carry equally in a caption, as the behavioural view's legend now does; the two views are inconsistent on where legend text lives.
12. [note] Assembly view: "baseline regime" and "primary regime" against the gains are undefined on the image; a P2 does not know what a regime is here (two gain boxes for two datasets) and the caption must say so.
13. [note] Assembly view, idiom: the generalization triangles from SmallWheel etc. to an «abstract» ReactionWheel read as "one of these alternatives is chosen"; the inheritance analogy is close enough to the swap and implies nothing false; legible at 700 px.
14. [changes the view] Heatmap: the colourbar has no name; I guessed "share or weight"; the intent's word is "contend", and the plotted quantity must be named on the colourbar or the row reading is a guess.
15. [changes the view] Heatmap: the intended sentence "control effort fades out by the selected temperature" is not readable: its cells are at or below 0.03 from the first column, indistinguishable from white at 700 px, and the selected temperature is marked on the top panels only, not on the heatmap, so "by the selected temperature" cannot be placed on the lower panel.
16. [changes the view] Heatmap: the intended ranking (total mass, then energy balance, pointing error, depth of discharge, settling time) cannot be read because rows are in some other order and three rows sit in the same mid grey; ordering rows by share at the selected temperature would make the sentence readable in one look.
17. [changes the view] Heatmap: the black total-mass row at the 0.30 cap reads as clipped (my cold read said "capped?"); the author's own note confirms 0.358 is hidden, so the row's value is unknown from the image.
18. [changes the view] Heatmap: the two top panels (fraction above V = 1, effective sample size, the 0.1 line, the grey bar) have no intent written for them; the intent sentence is the lower panel's alone, so by the sentence test they either get their own intent or go; as drawn, V, tau and the 0.1 rule are unexplained symbols to a P2.
19. [changes the view] Heatmap: the image does not say which regime it is (primary); with heatmap_stock.png existing for the baseline, a title or label naming the regime is needed, and the regime names should match the views' vocabulary (the file still says "stock").
20. [note] Heatmap, idiom: a white row in a heatmap reads as "this metric was ignored or the fit failed on it"; the intent says the three white rows are a finding (each carried by another metric or by the swaps), which the image cannot say, so the caption must carry it or a P2 takes the fit to have dropped a third of the metrics; this is the question I would put to the modeller first about the heatmap.
21. [note] Heatmap, consistency: the nine row labels match the nine green boxes of the behavioural view word for word, which let me cross-read the two without a lookup; keep that.
22. [note] Heatmap, legibility: 800 px wide rather than 700; at 700 the tick labels (3 .. inf) and axis titles still read; the duplicated axis title ("temperature tau" above, "tau" below) is a small inconsistency.


### Dispositions of the round-3 P2 findings

| # | Tag | Disposition | Where |
|---|---|---|---|
| 1 | note | Noted, no change: the cold read matches the intent on the grouping, the joins, the sources and the three excluded requirements; the legend and the verification-case line did their job at 700 px | — |
| 2 | note | Noted, no change: "reads through the element named in the box" and "headless line = shared quantity" are the caption's (L-C material); nothing was misread | — |
| 3 | note | Closed: the MoE/MoP rule is one caption item (the model's rule, with the pointing error and the launch cost as its two instances); nothing on the image | `43e1a7f`; review "Round 4", item 1, last sentence; `round-4/INTENT.md` |
| 4 | note | Closed: the dashed group is titled "requirements that read no traded metric", in black (its type was body size already, 9.3 px bold, but grey) | `43e1a7f`; review "Round 4", item 1 |
| 5 | note | Noted, no change: the reader's own verdict ("the lines need the room, so not a redraw finding") | — |
| 6 | note | Noted, no change: "(the analyst's grouping)" in each lane title defused the package idiom, as round 3 intended | review "Round 3", "The views of round 3" |
| 7 | note | Open: the total mass is drawn from `SlewExperiment` (it is return entry 2 of its tuple, `cubesat.totalMass`) while `LaunchBudgetRequirement` is verified in `ConfigurationVerification`; the view does not say that this entry needs no slew. The same point as round-1 P3 finding 13 | open item B |
| 8 | note | Open on the view: no threshold is drawn and the configuration variables of the assembly view appear nowhere on the behavioural view. Where the record answers it: the thresholds and the share of feasible designs each admits are the review's "Proposed thresholds, revised for the gate popup" (`3483ee9`); the link from the configuration variables to the metrics is the coverage table's first table (decision element x traded metric), the pair's third element. The same point as round-1 P2 finding 15 | open item E |
| 9 | note | Answered in the record, except the last: the three untraded requirements are the flags `power_ok` and `momentum_ok` of the dataset (`power_ok` holds for 1.000 of the designs in both regimes, review "Round 3" (a); the feasible counts are 706 of 1000 primary, 780 of 1000 baseline, `k3_record.md`) and, from round 2, the battery peak power, which holds over the whole declared space (review "Round 2", "Where it binds"); the thresholds and the designs that violate them, review "Proposed thresholds, revised"; the launch cost is derived and not traded by OD1 and OD2 ("MoE on mass, no new column"); why the total mass is a `SlewExperiment` output: finding 7, open | the sections named; open item B |
| 10 | note | Closed: round 4's intent says eight boxes and names the pair in the solar panel's box, with the reason the drawing stays at eight | `43e1a7f`; review "Round 4", item 2 |
| 11 | note | Closed: the legend keeps the two tag keys and the untagged rule; the levels and ranges are the caption's (`assembly_caption.md`, written by the generator from the model); the frame is 245 px tall against 357 | `43e1a7f`; review "Round 4", item 2 |
| 12 | note | Closed in the caption: the levels and ranges left the image, and the caption names the two regimes with their datasets and gain boxes (`round-4/INTENT.md`: the primary regime is `adcs_designs_cubesat_gains.csv`, the aggressive gain box; the baseline regime `adcs_designs_cubesat.csv`, the baseline gain box) | `43e1a7f`; review "Round 4", items 2 and 3 |
| 13 | note | Noted, no change: the specialization idiom reads as the swap and implies nothing false | — |
| 14 | changes the view | Deferred: the colourbar is unnamed | heatmap redraw after the gate: review "Round 4", item 4, first bullet |
| 15 | changes the view | Deferred for the marker: the selected tau is not marked on the grid. Open for the scale: cells at or below 0.03 read as white at 700 px, so the fade cannot be seen even with the marker; not in the redraw list (the same point as round-1 P2 finding 7) | heatmap redraw after the gate: "Round 4", item 4, second bullet; open item A |
| 16 | changes the view | Deferred: the row order (the CaseSpec's attribute order, which the figure does not say) | heatmap redraw after the gate: review "Round 4", item 4, fourth bullet |
| 17 | changes the view | Deferred: the total-mass row is clipped at the cap of 0.30 | heatmap redraw after the gate: `e20db3f`; "Round 4", item 4, third bullet |
| 18 | changes the view | Deferred: the top panels' intent | heatmap redraw after the gate: review "Round 4", item 4, fifth bullet |
| 19 | changes the view | Closed: each heatmap panel is titled with its regime ("K = 1 exponent of each metric across tau, primary regime"), the baseline heatmap is `heatmap_baseline.png`, and the record's headings say "baseline regime" (the CaseSpec key `stock` is mapped to the word at the point of writing) | `43e1a7f`; review "Round 4", item 3 |
| 20 | note | Closed in the caption: the three white rows are stated as the round's finding, not a defect of the fit, each carried by another metric or by the swaps; the case prose (D-7) carries the same reading | `round-3/INTENT.md` and `round-4/INTENT.md`, heatmap section (`abdb88f`, `43e1a7f`); `a27191e` |
| 21 | note | Noted, keep: the nine row labels are the coverage table's metric names, as the behavioural view's boxes are | — |
| 22 | note | Deferred for the two axis titles (redraw list). Noted, no change for the width: the figure is `case.tau_sweep_figure`'s at its own size, and the reader found the tick labels and axis titles legible at 700 | review "Round 4", item 4, sixth bullet |

---

# Round 3, P3 proxy (systems modeller, depth L-C), fresh context (had not seen earlier rounds), image before caption. Verbatim.

Cold sentences (written before any text was read):

behavioural_view.png: "Each of nine traded metrics is a green box in one of three analyst groupings, fed by either the measured slew or the SlewExperiment analysis (grey arrows) and read by one orange requirement (headless orange line), with three requirements at the top reading no traded metric and one yellow derived metric, launch cost, hanging off total mass." Boxes: orange = requirement with its verification case named beneath; green = traded metric with its MoE/MoP stereotype and model identifier; yellow = derived, not traded; grey = the measurement source; lilac = the analysis def. Lines: orange headless = requirement reads metric; grey with open head = source produces metric. Dashed frame = requirements with no metric to point at. I read LaunchBudgetRequirement as reading total mass directly, with launch cost a second thing it reads.

assembly_view.png: "A Cubesat is composed of eight parts, two of which (reaction wheel, star tracker) are swapped among three alternatives each and four of which carry tuned parameters (panel span, battery capacity, Kp, Kd), the other three fixed; the legend gives the levels and ranges and says the gain ranges differ between two regimes." Filled diamonds = composition; open triangles = specialization (the alternatives); orange swap tag = categorical variable; blue tune tag = continuous variable; untagged = fixed.

heatmap.png: "As temperature tau rises the fraction above V = 1 and the effective sample size fall, with a tau near 40 picked where the fraction crosses 0.1; across the nine metrics total mass dominates at every tau, energy balance, pointing error and depth of discharge hold steady, settling time fades and energy balance strengthens with tau, control effort vanishes after tau about 10, and power margin, eclipse reserve and peak slew power are zero throughout." Dots/line = the sweep; black horizontal = the 0.1 target; grey vertical bar = the selected tau; heatmap grey = an unnamed 0 to 0.30 quantity per metric per tau column, 13 columns ending in "inf".

Findings:

1. [changes the view] behavioural_view.png, mass lane: the chain requirement -> launch cost -> total mass that the intent names is carried by a ~5 px vertical stub between the two stacked boxes; read cold at 700 px I missed it and took the requirement to read total mass directly. The one place the view departs from one-requirement-one-metric is its least visible line.
2. [changes the view] heatmap.png: nothing on the image names the regime or dataset, and a near-identical heatmap_stock.png exists; the intent sentence begins "in the primary regime", which only the file name carries.
3. [changes the view] heatmap.png, colourbar: unlabelled; k3_record.md calls the quantity "exponent w" and nothing on the figure does.
4. [changes the view] heatmap.png, bottom panel: the selected tau (38.1) is marked on the two top panels only; 38.1 falls between columns 25 and 42 and the heatmap has no marker, so "the control effort fades out by the selected temperature" cannot be read off the panel that shows the control effort.
5. [note] heatmap.png, x axis: the "inf" column has no counterpart in the top panels (which end at 1000) and none of INTENT.md, coverage.md or k3_record.md says what it is (diagnostic_pair.py appends np.inf to the sweep).
6. [note] heatmap.png, total mass row: clipped at the 0.30 cap (0.358 per k3_record.md; INTENT.md acknowledges); the strongest row is the one whose value the figure cannot show.
7. [note] heatmap.png vs INTENT.md (sentence test): the five-contend / three-never / control-effort-fades sentence is carried by k3_record.md's K = 1 exponent table and its "zero at every tau" line except the fade; the tau axis also shows settling time weakening and energy balance strengthening with tau, which the intent does not claim; either the intent claims the tau dependence or the columns do little.
8. [note] behavioural_view.png, legend: covers three of the five box colours; grey (SlewMeasurement), lilac (SlewExperiment) and the two line kinds are left to the caption, as INTENT.md says; read cold I read them correctly.
9. [note] behavioural_view.png vs coverage.md DSM, "requirements read off": the DSM lists MomentumRequirement under controls and PowerRequirement and BatteryPeakPowerRequirement under power and energy; the view places the same three outside every lane in the dashed group. One object, two placements.
10. [note] behavioural_view.png vs coverage.md DSM, coupling: the off-diagonal cells (usableWheelTorque, peakTorque, torqueSquaredIntegral between controls and power and energy; InertiaX/Y/Z and structureMass from mass to controls) are drawn in neither view; the SlewExperiment box says "the measured inputs" but no arrow joins SlewMeasurement to SlewExperiment, so the measured peakTorque and torqueSquaredIntegral that five power-and-energy metrics need have no drawn path.
11. [note] naming: "the analyst's grouping" (lane titles), "subsystems" (coverage.md DSM, CaseSpec), "lanes" (INTENT.md) for one object.
12. [note] naming of the datasets: k3_record.md says "stock regime" where INTENT.md and the assembly legend say "baseline regime" (INTENT.md flags it as a PM item); the CSV names mark the primary member ("_gains") while the heatmap files mark the baseline member ("_stock"), so the unmarked default is a different dataset under the two conventions.
13. [note] assembly_view.png, legend "read from the model": "baseline regime" and "primary regime" are not model names; the model's gain boxes are baselineGains and aggressiveGains, and "primary" appears there only in a doc comment. A P3 going to the model for "primary regime" will not find it.
14. [note] assembly_view.png, swap tags: "TrackerGrade" names the enum type while the part's attribute is `grade`; on the wheel the attribute `wheelClass` and the type `WheelClass` coincide; the tune tags name attributes (panelSpan, batteryCapacity, Kp, Kd). Consistent with coverage.md's decision-element column, but the tags mix identifier levels.
15. [note] assembly_view.png, composition lines: the lines to StarTracker and Controller cross the header of the ReactionWheel and StarTracker boxes (polyline over box).
16. [note] assembly_view.png: nine parts in eight boxes; "(panelPlus, panelMinus)" is the only sign of two usages and cold I counted eight parts, as INTENT.md anticipates.
17. [note] consistency confirmed: the nine metrics, their MoE/MoP marks, requirement names and verification cases agree across behavioural_view.png, coverage.md's second table and cubesat_r2.sysml (ConfigurationVerification: Power, PointingError, LaunchBudget; SlewVerification: the other nine); the heatmap and k3_record.md list the same nine metrics in the coverage order; the six swap/tune tags match coverage.md's decision elements; the heatmap's selected tau, fraction above (0.092), n_eff (23) and the three white rows agree with k3_record.md's primary K = 1 lines; SlewExperiment's "7 of the 9" matches the model's eight return entries with controlEffort passed through; round-3/coverage.md is byte-identical to examples/adcs/model_v2/views/coverage.md.

Nothing tagged [blocks].


### Dispositions of the round-3 P3 findings

| # | Tag | Disposition | Where |
|---|---|---|---|
| 1 | changes the view | Closed: the line from the launch cost to the total mass carries the element the two share, `totalMass`, and the gap between boxes at one rank is 16 (8 in round 3), so the line is about 30 px long with its label beside it; the requirement's line to the launch-cost box stays unlabelled because it lands on the box that names `LaunchCost` (three drawings measured by the type they leave: 8.6, 7.0 and 9.2 px) | `43e1a7f`; review "Round 4", item 1 |
| 2 | changes the view | Closed: each heatmap panel is titled with its regime; the baseline heatmap is `heatmap_baseline.png` | `43e1a7f`; review "Round 4", item 3 |
| 3 | changes the view | Deferred: the colourbar is unnamed | heatmap redraw after the gate: review "Round 4", item 4, first bullet |
| 4 | changes the view | Deferred: the selected tau is not marked on the grid | heatmap redraw after the gate: review "Round 4", item 4, second bullet |
| 5 | note | Closed in the caption: `INTENT.md` says in one clause that the last column is the tau = infinity limit (`diagnostic_pair.py` appends it to the sweep). The image's own label stays "inf" | `43e1a7f`; review "Round 4", item 3 |
| 6 | note | Deferred: the clipped total-mass row | heatmap redraw after the gate: `e20db3f`; "Round 4", item 4, third bullet |
| 7 | note | Open: the intent sentence claims one tau dependence (the control effort fades out by the selected temperature) and the panel shows two more (the settling time weakening, the energy balance strengthening with tau) that it does not claim; the record neither widens the sentence nor drops the columns. The figure is redrawn after the gate on the regenerated data, where the intent is written again | open item A |
| 8 | note | Noted, no change: the caption carries grey, lilac and the two line kinds (`INTENT.md`), and the reader read them correctly cold | — |
| 9 | note | Open: the coupling table lists `MomentumRequirement` under the controls and `PowerRequirement` and `BatteryPeakPowerRequirement` under power and energy ("requirements read off"); the view places the three outside every lane in the dashed group. One object, two placements; no disposition recorded | open item B |
| 10 | note | Open: the coupling variables of the table's off-diagonal cells (`usableWheelTorque`, `peakTorque`, `torqueSquaredIntegral`; the inertias and `structureMass`) are drawn in neither view, and no arrow joins `SlewMeasurement` to `SlewExperiment` although the analysis reads the measured `peakTorque` and `torqueSquaredIntegral`; no disposition recorded | open item B |
| 11 | note | Open: "the analyst's grouping" (the lane titles), "subsystems" (`coverage.md`, the CaseSpec) and "lanes" (`INTENT.md`) name one object; round 4's caption says "the analyst's grouping of the metrics (the CaseSpec's subsystems)" and does not pick one | open item C |
| 12 | note | Closed for the record's words: `k3_record.md` and the heatmap files say "baseline regime" from round 4. Noted, no change for the file names: the CSV names (`_gains` marks the primary regime) are the contract's and the CaseSpec key `stock` is `case.py`'s, both outside the round's blast radius (review "Round 3", last paragraph; "Round 4", item 3) | `43e1a7f` |
| 13 | note | Open: "baseline regime" and "primary regime" are the scope's names, not the model's; the caption maps each regime to its dataset and gain box in words (`round-4/INTENT.md`: the primary regime is the aggressive gain box) but names neither `baselineGains` nor `aggressiveGains`, so a P3 going from the caption to the model still has no identifier to search for | open item C |
| 14 | note | Open: the swap tags name the enum type (`TrackerGrade`, `WheelClass`) and the tune tags name attributes (`panelSpan`, `batteryCapacity`, `Kp`, `Kd`), consistent with the coverage table's decision-element column; no disposition recorded | open item C |
| 15 | note | Open: the composition lines to `StarTracker` and `Controller` cross box headers; round 4 changed the assembly view's legend and not its layout, and the round-4 record does not say whether the crossings remain | open item F |
| 16 | note | Closed: round 4's intent says eight boxes and names the pair (panelPlus, panelMinus) in the solar panel's box, with the reason the drawing stays at eight | `43e1a7f`; review "Round 4", item 2 |
| 17 | note | Noted, no change: the consistency confirmed is the record's | — |
