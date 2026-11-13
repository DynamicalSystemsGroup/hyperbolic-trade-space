# WP39 — Scope of work: the case ends in a decision

| | |
|---|---|
| **Status** | DRAFT, for the assistant's approval. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The assistant's approval, quoted verbatim in `work-packages/WP39-decisions.md` |
| **Acceptance record** | The supervisor's acceptance, quoted verbatim in `WP39-decisions.md`, after `WP39-review.md` |

## Purpose

The supervisor's direction, verbatim (`WP39-decisions.md`, 2026-11-13):

> we need section in the paper covering the case to end with a concrete low dimensional outcome, the reason i
> introduced the stakeholders with low dimensional concerns is so that we could traceably and rigorously reduce down to
> making a call. even if its simply narrated how this model helped the two executives (who we cannot assume care about
> all the details) decide on a configuration they are both willing to accept. it needs to be feasible, and sit on
> (near) the frontier); we're basically saying we're not making the decision for you but we're supporting a
> scientifically grounded debate/discussion resulting in a defensible decision by business leaders who are not
> themselves assumed to be (and don't need to be) experts in the underlying processes or systems.

On the cost and the test: "this may cost some space but its important that the case example section speaks to the
people who actually have to make decisions. i don't want them seeing this as something that makes their lives harder
rather than easier." and "you can determine how you want to document and test for this requirement". On the level:
"this requirement lives at two levels: at the detail level in the applied case section but also in the way we talk
about the method ... this is a vibe check requirement so it may not require significant changes in any other
location. we just need to make sure a skimming exec is encouaged not scared off."

Stage 1 (the research spike, `WP39-rounds/spike/readout.md`, fb6adcc) computed the stakeholder layer, the 28 designs that
pass all six requirements and lie within the band of both fits, the decision rules on the executives' measures and three
drafts with every number traced. Stage 2 is decided (`WP39-decisions.md`, 1af5c8a): Q1 (c), Q2 (a), Q3 (a), Q4 (b) with a
raise row for the remainder; the shape is Draft 2. This package is the build, quality control, integration and review of
that closing subsection, and the skim test of the surfaces around it. Head at scoping: `dev` at `9b284fa` or later.

## Goals

- G1. **The case section speaks to the people who make decisions and leaves them with an easier call, not a harder one.**
  Section 9 closes with a subsection that reduces, traceably, from the feasible designs to the call two executives with
  few concerns each would make: the 2,134 feasible designs, the 548 that pass all six requirements, the 28 within the
  band of both fits; the one question that is theirs (whether a fine star tracker, pointing error from about 0.003 to
  0.0008 degree, is worth about 0.56 M USD of a 6 M USD fleet budget), priced in program currency; the designs that answer
  it either way, feasible and on or near the frontier. The method does not choose; the subsection says so and says what it
  does not tell (schedule and risk, what to buy beyond the modelled parts, the value of fleet size).
- G2. **The body budget bends for this section, and the existing text gives way first.** Each added sentence carries its
  job in the ledger; the Candidates paragraph is cut and the K-choice sentences shortened, because they serve the decision
  maker less; the remainder is a raise row on Section 9 with the job stated (the supervisor allowed the space).
- G3. **Nothing is asked to be trusted as a ranking.** The values are nominal, a clause says so and points at Appendix C.8
  beside the table, and the model prices options and does not choose (P7, section 4 of the final read).
- G4. **Every number is generated and backed.** The narration's numbers and the table come from one function, each with a
  claims-register row.
- G5. **The second level, the skim test:** after the build, a skimming executive is encouraged, not scared off, by the
  surfaces around the case, and only the sentences that put the skimmer off are touched.

## Non-goals

- Choosing a design for the executives, ranking the 28, or any sentence that says the method decides.
- Mapping the K = 2 terms to the executives in the narration (Q3 (a)); the exponents and terms stay in the K = 2 paragraph
  and the appendix. No stakeholder-to-term table.
- Cutting Figure 9 or its paragraph: they go to the final subtraction pass under the marginal-value test.
- Cutting the "Two regimes" or "Propose, predict, check" paragraphs, or the shows/does-not-show lines of the figures.
- Any change to the model, the data, the fit, the requirements or their thresholds; anything under `src/`, `derivation/`,
  `pyproject.toml`, `uv.lock`.
- A rewrite of any surface on the strength of the skim test, beyond the put-off sentences it names, as wording. The
  abstract's own rewrite stays the supervisor's.
- The answer key's sentence is the assistant's: it is written by the assistant, held outside the repository, and no agent
  of this package reads or drafts it; the scope names it only so the criterion is not forgotten.
- The residual pass (WP38) and the final reader round, which read the finished text later.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-0 | This scope of work, committed and pushed alone | all |
| D-1 | The closing subsection of Section 9 in `paper/paper.ipynb`: one paragraph (about 130 to 150 words, shape of Draft 2 with the bold lead-in and one priced sentence that read on their own) and one small table (six rows: baseline configuration, sponsor alone, operator alone, between them, balanced between the terms, cheapest unit cost; columns the rule, the configuration, pointing error, unit cost, fleet cost, level), with the nominal-values clause pointing at Appendix C.8 and the sentence on what the method does not tell | G1, G3 |
| D-2 | The detail in Appendix D of `paper/supporting_material.ipynb`: the 28-design table and the decision rules (the readout's section (c)), generated by the same function as D-1 | G1, G4 |
| D-3 | The generator function (in `paper/generate_findings.py` or `examples/adcs/case.py`, chosen at the build) returning every number of D-1 and D-2, the narrated sentences and both tables from one place, with its tests in `tests/test_paper.py` | G4 |
| D-4 | Claims-register rows, one per number the narration quotes (2,134; 548; 28; 0.0008 and 0.003; 0.56 M; 6 M; 5; 1.69 M; 337,000; 1.13 M; 11 nondominated and 1 inside both bands; the table's cells), each backed by a generated value | G4 |
| D-5 | The displaced sentences and the ledger rows: a [[cut]] row for the Candidates paragraph (48 words), the shortened K-choice sentences, the new paragraph's rows each with its job, and a [[raise]] row on Section 9 for the remainder, stating the job; the cascade of the Candidates cut (D.7, `candidates_sentence`, its claims rows, cross-references) resolved | G2 |
| D-6 | The review-list row as a changed conclusion, if the decision section changes one (the P8 F2 and F3 findings of the final read); the stakeholder-term mapping choice recorded as decided (none, Q3 (a)) | G1 |
| D-7 | The reads (below) and their records under `WP39-rounds/`: the P8 and P7 cold reads of the finished section, the skim test, each with dispositions | G1, G5 |
| D-8 | The skim test's put-off sentences, changed as wording by the owning package, with the ledger rows; every change to an entry surface (the abstract, `site/index.html`, `README.md`, `docs/index.md`, `site/history.html`) listed in `supervisor-review-list.md` "Entry surfaces" for the supervisor's close read | G5 |
| D-9 | `WP39-review.md` and `WP39-decisions.md` (the approval and the acceptance quoted) | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Each number in the narration and in the table is a generated value and has a claims-register row; the table and the sentences come from one function (the machine check) | `uv run pytest -q tests/test_claims_register.py tests/test_paper.py`; a perturbation of the function's input moves the sentence and the register fails |
| R-2 | The subsection states, in program currency and not in bands or log V, what the executives would relax or buy: the fine tracker for about 0.56 M USD of fleet cost, and the fleet-size range (acceptance criterion 1, P8 F2 and F3) | read the paragraph; the sentence is quoted in the P8 read |
| R-3 | The narration is readable without the subsystem detail: the executives' measures are named in their words (pointing error, unit cost, fleet cost), the subsystem choices appear as configuration (wheel, tracker, fleet), and no exponent, term, design id or log V appears in the paragraph (criterion 2) | read; `grep` of the paragraph for those; the table carries ids and level |
| R-4 | The subsection says the values are nominal and where C.8 is, next to the table, and that the model prices options and does not choose (criterion 3) | read; the P7 read quotes the clause |
| R-5 | The subsection says what the method does not tell: schedule and risk, what to buy beyond the modelled parts, and the value of fleet size, which the model prices and does not value (criterion 4; Q1 (c): both sponsor measures shown) | read; the P8 read |
| R-6 | The shortlist is the 28 within the band of both fits, the paper's own convention (Q2 (a)); every design named lies in it and passes the six requirements | the generator's assertion and test; the register row for 28 |
| R-7 | The P8 and P7 cold reads of the finished section on the rendered page each answer two questions: could they follow the reduction to the call without the subsystem detail, and did the section make the decision easier or harder, quoting the sentence that did it (criterion 5). The section passes if both readers follow it and both say easier. A reader who says harder, or cannot follow, names the sentence; it is fixed and that reader re-reads once | the read files under `WP39-rounds/`, on the rendered page, with screenshots |
| R-8 | The skim test: after the build, the P8 persona skims the paper as an executive does (the abstract, the first screen, the introduction's opening, the discussion's and the conclusion's first lines, and the Examples page) and reports surface by surface whether it is encouraged or put off, and by which sentence, quoted. Only put-off sentences are touched, as wording, by the owning package, with the ledger | the skim record; `git diff` of those surfaces shows only the named sentences |
| R-9 | Entry-surface changes (the abstract and the first screens are entry surfaces) are each listed in `supervisor-review-list.md` "Entry surfaces" with reason and commit; the abstract's rewrite is left to the supervisor and listed if the skimmer was put off by it | the list against `git log` of those files |
| R-10 | Section 9's ceiling and the paper's total hold after the cuts and the raise; every added sentence has a ledger row stating its job; the Candidates cut and the K-choice shortening each state what the text no longer did | `uv run pytest -q tests/test_paper.py`; the ledger diff |
| R-11 | The cascade is resolved: the Candidates cut leaves no dangling pointer (D.7, Section 1's pointers, `paper_perturb.py`, tests); Figure 9 and its paragraph are unchanged | `uv run pytest -q tests/test_paper.py tests/test_site.py tests/test_docs.py`; grep for the removed labels |
| R-12 | Vocabulary: glossary terms only; the glossary's term for the decision problem is checked at the build; "defensible" is the supervisor's word and used only where it is a claim the section backs | `uv run python scripts/check_vocabulary.py` |
| R-13 | Gates: whole-repo `uv run ruff check .` and `uv run ruff format --check .`; `uv lock --check`; `tests/test_text_encoding.py`; no AI attribution; notebooks and `paper/figures/` in one commit | the commands; grep of `git log` |

## Definition of good

- The two executives and the reader who is neither can follow, in one paragraph and one table, how the model took
  2,134 designs to a choice that is theirs; the fine-tracker question is the only thing left, and it has a price. They
  finish the section knowing what they would decide and what the method did not tell them, and the skimmer who read only
  the bold lead-in and the priced sentence got the same call.
- The section grew only where it carried a sentence the decision maker needed; what it displaced served them less.

## Definition of good enough

- D-1 to D-6 landed and R-1 to R-6, R-10 to R-13 pass.
- Both cold reads follow the reduction and say easier (R-7), and the skim test has been run with its put-off sentences
  fixed and its entry-surface changes listed (R-8, R-9).
- The cascade review finds the repository in a clean merged state: ledger, register, Section 9, Appendix D, docs pages and
  tests consistent; the rendered page seen.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Lifecycle stages

(1) Research spike: done (`WP39-rounds/spike/`). (2) Decide: done (`WP39-decisions.md`, 1af5c8a). (3) Build: the generator,
the subsection, Appendix D's table, the register and ledger rows, through the paper notebook's single-writer queue, after
the units already in it: the return of G.2 and WP35's Appendix H. The notebook is re-executed once the queue reaches this
unit; while a gate's container regression runs, nothing that regenerates paper outputs is pushed. (4) Quality control: the
register and paper tests, the vocabulary check, the rendered page. (5) Integrate: the displaced sentences and ledger, the
review-list row, the skim-test changes. (6) Review the cascade to a clean merged state: the P8 and P7 cold reads, the skim
test, `WP39-review.md`.

## Agents and models

Sonnet for the implementers and for the readers (the P8 and P7 personas, fresh, reading the rendered page only; screenshots
in the record); Haiku for mechanical units (counts, grep of removed labels, screenshot runs); nothing larger. No
sub-agent without the PM. Readers do not see the answer key, and none is asked for its sentence.

## Agent's defaults

One item for the assistant: the generator's location and name (`paper/generate_findings.py` unless `case.py` fits better);
the table's six rows and columns as in D-1; the subsection's title ("What the executives decide", the lead-in of Draft 2) and
its place as the last part of Section 9; Appendix D's table ordered by fleet cost with the nondominated marks; the raise
row's size, fixed at the build from the written paragraph less the cuts; the baseline regime given in one sentence of
Appendix D only; dollars to the nearest 1,000 or 0.01 M in the narration and exact in the table; the reads' files named
`WP39-rounds/read-P8.md`, `read-P7.md`, `skim-P8.md`; the cold reads run once after the build and once more only on the
rule in R-7; the personas' briefs taken from `WP30-rounds/persona-final/`.

## Open decisions (for the assistant)

None. Every item was resolved through the decision loop (`WP39-decisions.md`: the direction, the two levels, the cost and
the test, and stage 2's Q1 to Q4).

## Blast radius

- New: the generator and its tests, the register and ledger rows, `WP39-rounds/` reads, `WP39-review.md`,
  `WP39-decisions.md` entries.
- Edited: `paper/paper.ipynb` (Section 9 and any put-off sentence of the skim test), `paper/supporting_material.ipynb`
  (Appendix D), `paper/length_ledger.toml`, `claims_register.toml`, `paper/paper_perturb.py` where the Candidates cut
  touches it, `supervisor-review-list.md`, and the entry surfaces only for put-off sentences and each listed.
- Never: `src/`, `derivation/`, `pyproject.toml`, `uv.lock`, the data, the model, Figure 9 and its paragraph, the answer
  key, the `verify` and `stage` worktrees, tab-23.
