# WP70 — Decisions: the iron triangle as an HTS study (the probe)

## His direction (15:41 EST, 2026-11-16, verbatim)

"the new work package i want you to scope is related to an example case. i was talking to my team and they think we
should use HTS to do a study of the iron trangle from project management (and its various manifestations). our method
is emperical so ideally we'd find a big open access data set and build our study around that but we can also make a
synthetic case. iron triangle is not actually a trilemma its a n=3+m lemma, where m the cardinality of a set of
relevant quality metrics. time is schedule slack (more is better, and can be as a percentage of the total schedule if
we want), budget slack (also can be as a percentage of the total though keep in mind we need to ensure going over
budget stays positive), scope is tricky to pin down but if we use an agile project management base we can say its
story points (which is a floating unit but works fine for us since our method is emperical); then whatever the m
quality metrics are for the project in question.

obviously if our model is synthetics we can structure the experiements to generate data that fits my story above. if
we find data sets then we need to work with what they have. i think we could do more than one example. in fact an
entire research program around the iron triangle is merited in my opinion but for now lets start with a probe. explore
and come back to me with a pitch for a bounded scope model and analysis using HTS for an iron triangle.

the initial goal is to get project management folks (like my COO who is a PE & PMP interested)"

## His answer on the probe's depth (15:44 EST, verbatim)

Asked whether the probe includes a throwaway fit or stays survey and pitch: "you can do more than that. i need to walk
away from my computer for a while. i you can do a bounded case study based on what you learn. think of the pitch as
for a larger program with the initial fit (real or synthetic or one of each) as the proof of concept to back up the
pitch for a broader program. you can also argue that the materials are two sparse to do a broader program and instead
recommend smaller cases integrated into examples with no bigger picture plan"

## WP70 approved (15:44 EST)

His words above are the approval of the probe at that depth; the driver approves the scope's details as his proxy
under the mandate (D-4 as the bounded case study, real or synthetic or one of each; the pitch for a programme or
against one). One unit on branch `wp70`; the pitch and the case study go to his read.

## WP70 delivered and landed (16:04 EST)

`work-packages/WP70-rounds/` landed as 4bf40d31: `pitch.md` (part one for a PE and PMP, part two in the method's terms,
three options, the assessment, a P1 cold read), `datasets.md` (12 open sources ranked; every link resolved),
`synthetic.md`, and `case/` (the manifest, scripts, results and three figures; the data git-ignored; a 15-row result
table of near-frontier project ids and ratios committed under CC BY 4.0, accepted as a result and not a dataset).
The case: Kitchenham-CSC (doi:10.5281/zenodo.268457), the one open table with all three sides at one grain fetched
today; 141 projects; time and money as share of plan with shift 10, scope as function points; tau 22.8; exponents
0.71, 0.18, 0.11; all three contend; among the 15 nearest the frontier budget slack against scope -0.92, schedule
slack against scope -0.71, the two slacks together +0.43; one term; the direction held across six scaled scorings of
the whole portfolio, the exponents moved. A synthetic run with m = 2 recovered its planted two terms within 0.07.

The unit's assessment, which the driver accepts for his read: the open materials are too sparse for a programme now;
smaller cases in the examples, starting with option A (an example page on Kitchenham-CSC, one package); option B
(TAWOS sprints, where quality sits when time and cost are fixed by the sprint, two packages) is the one that could
grow into a programme. His choice decides. Three package findings routed to the plotting and analysis work: the
ternary's region label names the two largest exponents as trading even when their near-frontier association is
positive (+0.43 here); `trade_off_report` raises when fewer than ten rows fall within 1/tau; the tau = inf contending
set includes the planted non-participant in every synthetic run.

## His direction on the plot (16:04 EST, verbatim)

On the grain, straw and biomass case: "ternary might be the wrong plot for it. maybe this is an opportunity to create
another reusable plot"

The driver's reading: a size-against-shape plot, the level V on one axis and the chart's trade coordinate on the
other, with the frontier band, reusable for any d through the chart's first near-frontier direction; a new public
name, so a contract amendment; built with the second plotting step after the level-set figure lands, through the
figure loop.
