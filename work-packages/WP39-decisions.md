# WP39 decisions: the case ends in a decision (a concrete, low-dimensional outcome)

Supervisor: Michael Zargham (`mzargham`). A bigger candidate edit to the paper's case, run through the six stages
(spike, decide, build, quality control, integrate, review the cascade).

## The supervisor's direction (2026-11-13, verbatim)

> one other observation. this more about the example in the paper. we need to section in the paper covering the
> case to end with a concrete low dimensional outcome, the reason i introduced the stakeholders with low dimensional
> concerns is so that we could traceably and rigorously reduce down to making a call. even if its simply narrated
> how this model helped the two executives (who we cannot assume care about all the details) decide on a
> configuration they are both willing to accept. it needs to be feasible, and sit on (near) the frontier); we're
> basically saying we're not making the decision for you but we're supporting a scientifically grounded
> debate/discussion resulting in a defensible decision by business leaders who are not themselves assumed to be
> (and don't need to be) experts in the underlying processes or systems. for sufficiently large systems there is
> no way anyone person could be an expert in all the relevant subsystems.

## The assistant's reading

The case section (Section 9, the case analysis) ends today in findings about the fit: the K = 1 lead, the K = 2
terms, the requirements reading, the candidates, the nondominated counts. It does not close the loop the model's
stakeholder layer opens: the stakeholders with low-dimensional concerns (the measures of effectiveness: pointing
error, unit cost, fleet cost; the budgets) were put there so the analysis can reduce, traceably, to a call. The
section's last part becomes that reduction, narrated: how two executives who care about few things each, and
who are not experts in the subsystems, use the fit to arrive at one configuration both accept, feasible, on or
near the fitted frontier, meeting the six requirements. The method does not choose for them; it grounds the
debate and makes the decision defensible, and the paper says exactly that. The K = 2 terms already separate the
two concerns (term 1 led by peak slew power and pointing error, term 2 by unit cost and available power), which is
the natural axis of the narration.

Stage 1 is a research spike: what the stakeholder layer of the model says (who the stakeholders are, their
concerns, their budgets); which designs are feasible, pass all six requirements and lie within the band of the
frontier; how the two executives' concerns read on those designs (a low-dimensional view each: the design's
pointing error and its cost, its level log V, its position along the surface); the rules by which such a pair
could settle on one configuration (the cheapest that meets the pointing requirement; the balanced level between
the two terms; the design each would pick alone and the one in between) and what each rule gives on the data of
record; how the narration fits the body's budget (a closing subsection of a paragraph and one small table, the
detail in Appendix D). Readout with options to the assistant; then the decision, the build through the paper
notebook's single-writer queue, QC, the integration (claims, ledger, the key's sentence, the review list as a
changed conclusion, Appendix D's table), and the review by the P7 and P8 pair, whose question this answers.

## The supervisor, on the cost and the test (verbatim)

> this may cost some space but its important that the case example section speaks to the people who actually have
> to make decisions. i don't want them seeing this as something that makes their lives harder rather than easier.

> you can determine how you want to document and test for this requirement

**The assistant's reading.** The budget bends for this: the case section may grow where the narration needs it,
each added sentence with its job in the ledger, and the section's existing text gives way first where it serves
the decision maker less. The requirement is documented as a goal of the WP39 scope in the supervisor's terms,
the case section speaks to the people who make decisions and leaves them with an easier call, not a harder one,
and it is tested the way this project tests reading: the P8 persona (the new-space executive) and the P7
persona read the finished section cold and answer two questions, whether they could follow the reduction to the
call without the subsystem detail, and whether the section made the decision easier or harder, with the sentence
that did it quoted; the answer key gains the section's sentence (what the method does and does not decide); and
the claims register backs every number the narration quotes. The reads are the acceptance, the register the
machine check.

## The supervisor, the requirement at two levels (verbatim)

> this requirement lives at two levels: at the detail level in the applied case section but also in the way we
> talk about the method which means it may have bearing on the abstract and introduction, discussion, conclusion
> and other surfaces. this is a vibe check requirement so it may not require significant changes in any other
> location. we just need to make sure a skimming exec is encouaged not scared off.

**The assistant's reading.** Two levels, two tests. The detail level is WP39's build in the case section, tested
by the P7 and P8 cold reads of that section. The surface level is a skim test: the P8 persona skims the paper
the way an executive does, the abstract, the first screen, the introduction's opening, the discussion's and the
conclusion's first lines, the Examples page, and reports, surface by surface, encouraged or put off and by which
sentence; the readout names the sentences that put the skimmer off, and only those are touched, as wording, by
the owning package (the abstract and the first screens are entry surfaces, so every such change is listed for the
supervisor's close read, and the abstract's own rewrite stays his). No other change is made on the strength of
the vibe check; it is a read with a small, named remedy list, not a rewrite.

## Stage 2: the spike readout accepted and the decision section decided (2026-11-13, 12:40; the assistant, under the supervisor's rulings above; readout at fb6adcc)

The stage-1 readout (`WP39-rounds/spike/readout.md`) computes the stakeholder layer, the 28 designs that pass all six
requirements and lie within both fits' bands, the decision rules on the executives' measures, the fit to Section 9's
budget, three drafts with every number traced, what gives way by marginal value, and the acceptance criteria quoted
from the P7 and P8 final reads. The assistant's calls, in the readout's numbering:

**Assistant, verbatim:** "Q1 (c): both sponsor measures are shown, unit cost and fleet cost, and the fleet size is
named as the thing the model prices and does not value. Q2 (a): the shortlist is the 28 within the band of both fits,
the paper's own convention. Q3 (a): no mapping of terms to executives in the narration; the exponents and terms stay
in the K = 2 paragraph and the appendix. Q4 (b) with a raise: the Candidates paragraph is cut (its hand-named
candidates all miss the thresholds, and the shortlist replaces them) and the K-choice sentences are shortened; the
remainder is a raise row on Section 9 with the job stated, as the supervisor allowed; Figure 9 and its paragraph are not
cut by this package and go to the final subtraction pass under the marginal-value test. The shape is Draft 2: the
executives' question named and priced in program currency, the method not choosing, with the clause that the values are
nominal and where C.8 is, and the sentence on what the method does not tell. The skim test: the bold lead-in and the
one priced sentence must read on their own. Every number is a generated value with a register row; the table is
generated by the same function. Acceptance is the supervisor's test: P7 and P8 cold-read the finished section."

## Approval of the scope (2026-11-13, 14:30; the assistant, under the supervisor's direction; scope at fe2335e)

**Assistant, verbatim:** "WP39-scope-of-work.md at fe2335e is approved as written: goals G1 to G5, the non-goals (no
choice made for the executives, no term-to-executive mapping, Figure 9 and its paragraph untouched, the abstract's
rewrite the supervisor's), deliverables D-0 to D-9, requirements R-1 to R-13 with the two cold reads and the skim test
as the supervisor set them, good enough as stated, and the agent's defaults as one item. The build queues on the paper
notebook after the G.2 return and Appendix H. Open decisions: none."

## The decision section's digits take the stability treatment (2026-11-14, 00:05; the assistant, a default of the approved scope made explicit)

**Assistant, verbatim:** "The decision section's quantities take the stability treatment like every other quoted number
of the paper: the counts (2,134; 548; 28; 11 and 1), the pointing errors, the three prices and the fine-tracker
difference go into stability_extra through paper_perturb's machinery before the notebook unit, and the generator prints
them through stable(). The counts are exact on the data of record and print exact; if the perturbation moves any of
them, the prose says 'about' and the register row says so."

## The notebook unit accepted on the clean execution (2026-11-14, 08:40; head a538fc4, unit 20bff6e)

**Assistant, verbatim:** "The WP39 notebook unit is accepted at a538fc4: Section 9 closes with 'What the executives
decide', a 141-word paragraph in the decided shape with no exponent, term, design id or log V in it, the priced
question, the two answers, the method pricing and not answering, the nominal clause pointing at C.8; the six-row
generated table with the baseline configuration and the caption's what-the-method-does-not-tell; Appendix D.19 with
the shortlist and the rules; the Candidates paragraph cut and the K-choice sentences shortened within the raised
Section 9 ceiling; every quoted number through the stability entries and a register row; the notebooks executed once
from the committed sources with no stderr line and paper.ipynb byte-identical to the unit's; the fast suite 1946 passed,
ruff, lock and vocabulary clean; the section read as rendered on the stage. The P8 and P7 cold reads and the skim test
(R-7, R-8) now run on this head; the package's acceptance is the supervisor's after them."

## The cold reads and the skim test ruled on (2026-11-14, 09:05; the assistant; reads at c3d66a3 on stage a538fc4)

Both readers followed the reduction to the two-way choice and both said easier (P7 quoting the pricing-not-answering
sentence, P8 the priced question), so R-7's test is met on the reading; both stopped at "lie within the band of both
fits", and P8 found the opening sentence's cross-reference rendered "Table ??". The skim test (R-8) found the
executive encouraged by Section 1 and the contribution line, neutral on the discussion and the docs root, put off by
the root page's adoption and What lines, two future-work fragments, and the Examples page's "mean slack" sentence.

**Assistant, verbatim:** "One fix unit on the paper queue, then one re-run of the P8 read, as R-7 allows. The unit:
(1) the opening sentence's reference resolves, as a numbered table or as words pointing at the subsection; (2) 'lie
within the band of both fits' is glossed in plain words at the point of use (near the fitted frontier at both fits),
'regrets least' becomes 'gives up the least of either measure', and 'the 5' is said as the five designs of the
shortlist that no other beats on both measures; (3) 'of a 6 M USD fleet budget' becomes the 6 M USD fleet-cost limit,
since C.8 puts the sponsor's full budget at 8 M USD, a correctness fix; (4) the executive table's configuration column
reduces to wheel class, tracker grade and fleet size, the full configuration staying in D.19; the level column stays
with its caption saying in plain words that it is the distance above or below the fitted reference surface; the two
rows the paragraph does not name get one clause; (5) the caption names the requirement the baseline misses, the unit
cost limit; (6) D.19's table shows the two term levels the balanced rule reads, or the rule's text gives the gap;
(7) 'operator' and 'sponsor' are introduced as the case's two stakeholders at first mention. Words within the raised
Section 9 ceiling, cuts first, the ledger measured. Skim test: the root page's two put-off sentences change as wording
(exponents to trade-off strengths in the adoption line; the n-lemma gloss to a combination of the measures) and are
listed under Entry surfaces for the supervisor's close read; the Examples page's 'mean slack' sentence goes to plain
words without the code name; the abstract is reported to the supervisor, not touched; the future-work sentences and
the docs root's definition of a term stay, since they serve the method reader and the first-use rule; the root page's
unexplained 'conditioning' is listed for the supervisor with the entry surfaces."

## The second fix unit accepted (2026-11-14, 10:35; head f89c663)

**Assistant, verbatim:** "WP39's second fix unit is accepted as rendered: the subsection opens with the case's two
stakeholders, the pick 'gives up the least of either measure among the 5 of the 28 that no other beats on both', the
executive table's configuration column reads wheel class, tracker grade and fleet size, the level is glossed in the
caption as the distance above or below the fitted reference surface and not a ranking, the baseline's missed limits
named, D.19 shows the two term levels; Section 9 at 1,734 of 1,736 with no raise; the full group 358 passed in the
unit's run and the fast suite here. The one P8 re-read runs on this head; the package's acceptance is the
supervisor's after it and the review."

## WP39 delivered and verified by the assistant (2026-11-14, 11:55; head 94cb6a1)

**Assistant, verbatim:** "WP39 is delivered and verified under the mandate: R-1 to R-13 met with evidence in
WP39-review.md; both cold readers followed the closing subsection and said easier, and the P8 re-read after the two
fix units says easier for the closing paragraph taken alone and harder for Section 9's middle (the K = 1 fit, the
terms and the temperatures), which is the analyst's part of the section and not the executive's path, so it stands as
a reader note beside the row and not as a return; the skim test's put-off sentences were remedied where ruled and the
abstract's two are reported; the suite 1946 passed on 94cb6a1 with the hash-abbreviation flake fixed; CI fully green
at 8699324. WP39 goes on the review list for the supervisor's acceptance with the three reads and the re-read beside
it."
