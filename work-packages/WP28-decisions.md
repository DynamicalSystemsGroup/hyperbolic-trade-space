# WP28 — Decisions (improvement by subtraction, step 5a)

Approvals and acceptances are the driver's under the mandate (`release-candidate.md`, "The mandate"); the
supervisor's words are quoted verbatim where they bind; the driver's calls are listed for his review at the PR.

## Origin

The supervisor, 2026-11-09, 23:05 and 23:10 (`PM-BRIEF.md`, `driver-log.md`): "negative edits are welcome even
preferred ..." and "i will eventually have to rewrite the abstract by hand so don't stress about that specifically.
i mean more like making sure we're not jamming in plots or arguments for their ownsake that don't advance the
narrative of the paper. we got a bit bloated early n and i want a disciplined improvement by subtraction pass once
we have have complete content. or if something is stuck in a loop or cannot be made clear rather than agonize
assess removal". Step 5a of the path.

## Scope gate (2026-11-10, 18:55; scope `WP28-scope-of-work.md` drafted at 195bd81; `<start>` = 1277210)

The driver's decisions on the open items:

- **OD1 (b).** WP28 starts now; its re-test (D-5) is WP11's round 3, one read serving both; the maths-check unit
  lands before the stage. The paper's CR units of round 2 have landed (units 1 to 5); what a cut removes, a CR
  cannot still be editing, so the paper stream takes no CR unit while a cut is open on the same section.
- **OD2 (b).** An appendix is judged by its depth's job: a table goes only when nothing in the main text points to it
  and no reader at depth D would look for it; Appendix F (the reproduction) is out. The drill-down levels are the
  paper's design, not bloat.
- **OD3 (a).** A figure that serves no sentence of the story goes, cold read or not; a "good for" line is not a
  sentence of the story. Its generator stays in the case module (non-goal); the file and the cell go.
- **OD4 (b).** The figures the supervisor fixed and the two model views are inventoried with a verdict; a cut of one
  is a row in "for the supervisor", not executed.
- **OD5 (a).** The paper's ceilings drop by the cut rows and the docs' budgets are lowered to the counts after the
  pass: length is a regularizer, and nothing cut grows back without a row or a decision.
- **OD6 (a).** The driver approves the cut list before any cut is executed, recorded here under "Cut list". One
  gate; each cut then lands as one reversible commit.
- **OD7.** The Agent's defaults are approved with one change: the re-test is marked against answer key version 4
  (version 3 plus one word; its hash is in `WP11-decisions.md`), and the comparison with round 2 uses the "key
  stale" mapping the driver recorded there, so the cells still compare one for one.

**Driver, verbatim:** "WP28 approved as drafted with OD1 (b), OD2 (b), OD3 (a), OD4 (b), OD5 (a), OD6 (a) and the
defaults with the key at version 4. Start is 1277210. The inventory readers know no record; the cut list comes to
me before a cut lands."

## Cut list (2026-11-10, 20:50; `WP28-cut-list.md` at 68d240f, by a fresh triager)

The triager's reading of the 29 units not judged "advances": 3 cuts executable on approval (X-1, X-2, X-3, all on
the docs side), 1 cut held on a failing check (X-4), 10 rows for the supervisor (S-1 to S-10), 15 kept with a cited
reason; no unit stuck by the readers; one term stuck by the record ("energy differential", his decision).

The driver's decisions:

- **1 (b), approved with one change of hands.** X-1 and X-2 execute by the docs stream as written (the test member
  of X-1 changes under R-10 citing this approval; the register rows go with the figures; budgets lowered to the
  counts after, OD5 (a)). X-3 is executed by the driver, not the docs stream: `README.md` is under
  `[ownership.technical]` in the interface contract, and the contract is amended, never drifted; the driver is that
  side's writer, so no amendment is needed (decision 3 below). The fifteen kept rows stand as kept: each cites the
  pointer, reference or decision that keeps it, and the driver read them.
- **2 (a).** X-4 (`tab-D-refits_by_category`, D.6, eight words) stays: the renumbering of D.7 to D.17, the link
  constants in `paper/generate_findings.py` and two pins cost more than the eight words earn. It is noted beside
  S-10: if the supervisor cuts D.12, D.13 to D.17 renumber anyway and D.6 goes in the same unit.
- **3 (the contract stands).** No amendment: the driver edits the README under his own side's ownership.
- **4.** S-1 to S-10 go to the supervisor as one question at his next presence (the driver's log, "Waiting for the
  supervisor", with the driver's recommendation per row); nothing of them executes before his word.

**Driver, verbatim:** "The cut list is approved with X-1 and X-2 to the docs stream, X-3 executed by me under the
contract's ownership, X-4 kept, and S-1 to S-10 held for the supervisor. The fifteen kept rows are kept."

**X-3 executed by the driver (712a59f; the record at 1bd0ecc preceded the edit, whose first attempt failed before touching a file):** the README's description is the pointer sentence of the row; what the
content no longer did: it described the method a second time, in older words than the Home page, and called the unit
level set "the Pareto frontier", which Definition 1 and the abstract deny; register rows C369, C370, C371 removed
with the paragraph; `prose_words` 162 to 98.

## The rows for the supervisor, ruled (2026-11-10, 22:00 to 22:40; walked one at a time in the browser on the staged
site at af9ffea, at his request: "i want you to walk me through one at a time and show me in the browser so i can
assess myself as you walk through")

| Row | Unit | Supervisor, verbatim | Disposition |
|---|---|---|---|
| S-1 | Figure 2, the assembly view | "Keep" | kept |
| S-2 | Figure 3, the behavioural view | "this one brings to mind a modeling question. why are these requirements not related to metrics. my intuition is that these metrics should be in the trade and should into the existing groupings. my recommendation is keep but also use it as view ensure our model and our study are well matched. you can kick off a modeler research spike then a model developer to refine the model based on the modelling spike." | kept; a modelling research spike and a model-developer package (Track B) opened, origin quoted in its decision file |
| S-3 | Figure 9, the two regimes | "Cut to a pointer" | executes as a WP28 paper unit: the figure to a pointer to Appendix D.4 (114 words) |
| S-4 | docs Figure 5, the cubesat tension heatmap | "Keep" | kept |
| S-5 | docs Figure 6, the planted ternary and its subsection | "can we rebuild the figure from a trilemma using data from the ADCS model? i like this figure a lot and i lean towards keeping it but if the issue is that it feels made up we can do a real 3-lemma. don't swap in a new figure but do a loop to build an alternative" | kept as it is; a figure loop opened to build an alternative from a real 3-lemma of the case data; he chooses between the two |
| S-6 | Section 12, Future work and final remark | "Keep" | kept |
| S-7 | Section 13, Acknowledgments and process | "Keep" | kept |
| S-8 | Proposition 1 (L2) | "Keep" | kept; R-17 stands |
| S-9 | Proposition 2 (L6) | "consider whether we need another result that addresses our models relationship to measurement noise and/or noise in the process being measured. this may result in more work so first spike for relevant results and if we can add a result that builds on this proposition to character our relation to the noise. similiar to the modeling updates deploy research spike agents before deciding whether/what to build, then build, then quality control, then integrate, then review again. (also not i was bit short with my instructions before, so please apply this full lifecycle tactic to the modeling spike + model change)" | kept; a noise-result research spike opened (Track A); the six-stage lifecycle (research spike, decide, build, quality control, integrate, review again) applies to Tracks A and B and the figure loop |
| S-10 | Appendix D.12, the conditioning diagnostic | "keep and clarify why it matters. its supporting evidence for a discerning reader and our external review shows a descernign reader might ask for it. in practice conditioning does matter. we do need to provide a concise explanation for why this is relevant and how it was computed. someone who runs into issue needs a way to inspect the conditioning of their problem since trouble shooting may involve feature engineering work to get a better conditions version of the same problem." | kept; one unit adds the concise explanation (why, how computed, how a user inspects their own problem) in D.12 and on the docs page that teaches conditioning; X-4 (D.6) stays |

**S-5, the real-3-lemma candidate shown to the supervisor (2026-11-10, 23:35; the candidate at e6d0e4e: settling
time, pointing error, total mass, one term, one region). Supervisor, verbatim:** "having an example where all 3
trade everywhere is pretty realistic but not didactically interesting. my gut is we need to do some cherry picking to
get a didactically interesting example. its okay to include the one where all 3 trade everywhere but ideally either
find a real example with texture like the constructured one or also keep the constructed one to show what happens in
more complex setting. ideally we can accomplish this with a real example". **Disposition (the driver):** the figure
loop searches the data of record for a three-metric example with texture (several terms with distinct regions in
the triangle: metric triples from both regimes, K = 2 and 3 on the triple, the temperature by the case's rule, the
terms real by the splinter check and the certificate), the search recorded as a table of triples with what each
shows; if one is found it is the candidate and the one-region figure may stand beside it as the realistic case; if
none is found, the constructed figure stays to show the more complex setting and the one-region real figure joins
it. He chooses on the cold reads.

## Close units (eighth PM)

Implementer's record, one entry per unit. Worktree `wp28close` from origin/dev 089cef0.

### U1. S-3, "Cut to a pointer" (the supervisor's word, S-3 above)

- **Done.** Figure 9 (`fig-regimes`) goes: code cell, caption cell, lines cell, and `paper/figures/fig-regimes.png`.
  Section 9 (`sec-case-analysis-3b`) now points to "Appendix D.4" in place of "(Figure 9)"; the gloss "; the stock
  regime is the second panel of Figure 9" left Figure 4's caption. `case.regime_figure()` stays in the case module
  (non-goal). No register row quoted the dropped sentences (grep of `claims_register.toml`: none).
- **Ledger.** The `[[cut]]` row exists now: the header says what it is, `ledger_ceilings()` subtracts cut rows, and
  `test_each_ledger_row_names_a_job_a_reader_and_a_section_of_the_paper` checks their fields. Measured with the
  tests' own counter, the cut is 113 words, not the list's 114: Case analysis -103, Case construction -10 (Figure 4's
  caption is in Case construction); so two rows, each lowering its section's ceiling by what left (OD5 (a)); the
  counts after are Case analysis 1,722 and Case construction 1,146; the paper total 9,959 to 9,846.
- **Tests changed under R-10, citing the supervisor's word "Cut to a pointer", none weakened beyond it:**
  `test_regime_names_a_gain_box_dataset_and_the_terms_are_terms` (the `fig-regimes` label exemption leaves the
  regular expression: the label is gone, so the check is stricter by that), `test_cr1_one_definition_...` (the
  `fig-regimes-caption` leaves the "Outlined" tuple), and three counts that counted the figure
  (`..._removed_from_the_page` 4 to 3, `..._referenced_from_the_text` 10 to 9, `..._smallest_text_...` 3 to 2).
- **Re-record.** `paper/execute_notebooks.py` ran on the host (3 min). Re-recorded: only Appendix F.4
  (`tab-F-reproduction`, the row of `fig-regimes` leaves). Everything else the run changed (host platform, Node and
  interpreter lines, the commit line, four numeric outputs at the last digits, the repeated PNG bytes of the two
  host-rendered figures) was put back to the committed bytes; nothing an exact-equality branch reads was
  re-recorded, so no file is marked "host-recorded" beyond that: the driver's container regression at the gate
  re-pins as before.
- **Cold check (what was compared).** The removed figure (saved at
  `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/s3/fig-regimes-old.png`)
  carried, per regime, the 8 by 8 Pearson matrix among the near-frontier designs with the contending set outlined and
  each metric's K = 1 exponent w. D.4 (`tab-D-regime_comparison`) carries: both contending sets by name (primary:
  total mass, energy balance, pointing error, depth of discharge, settling time; stock: control effort, settling
  time, power margin, pointing error, depth of discharge; the same two five-sets as the outlines), the band and the
  near-frontier counts, and three pair associations (settling time with total mass, pointing error with control
  effort, settling time with pointing error), each in both regimes. It does not carry the full matrices or the
  exponents w; the full association table over the feasible designs is Appendix C.5's, the exponents are D.3's
  (`tab-D-exponents_and_terms`). So the sets and the pair tensions the text relies on are in D.4; the all-pairs
  picture is not (that is what "pointer" gives up).

### U2. S-10, the supervisor's word (S-10 above): Appendix D.12 explains why, how and how to inspect

- **Done.** D.12 (`app-D-cond`) gains one paragraph of three labelled parts (153 words net): why the conditioning of
  the exponents matters (the curvature of the convex objective along its flattest direction; the case's K = 1 values
  7.1 primary and 0.017 stock), how it is computed (`HyperbolicTradeSpace._conditioning` in
  `src/hyperbolic_trade_space/estimator.py`; printed by `conditioning_diagnostic()` of `paper/generate_results.py`),
  and how a user inspects their own problem (`HyperbolicTradeSpace(temperature=50.0).fit(M).conditioning_` for a
  strictly positive `M`; a small value is a prompt to rescale, merge or drop metrics, refit and compare).
- **Path named in the brief.** `paper/paper_perturb.py` does not compute the number: it only lists
  `conditioning_diagnostic` among the tables whose term numbering moves under a restart shift. The code path cited is
  the estimator's `_conditioning`, with the generator that prints the table.
- **Backing.** Test `test_d12_says_why_conditioning_matters_how_it_is_computed_and_how_to_inspect_it` (the two values
  recomputed from the fits, the named paths exist, the printed call is evaluated on a strictly positive planted
  table and returns one positive value); claims rows C423 to C425; the ledger `[[raise]]` row (section "Appendix D",
  admitted with a zero baseline like "Appendix B") quotes his words as the job.
- **Checked and left out.** A near-duplicate metric does not lower `conditioning_` (the fit gives the duplicate a
  zero exponent, and only participating exponents count: 39.4 with four metrics, 39.2 with a fifth near-copy), so the
  paragraph does not say that duplicates are what the number finds. The docs conditioning page is the docs stream's.
