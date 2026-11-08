# WP7 — Decision records

Records typed by the agent (driver session). Decisions are the supervisor's.

## Pre-approval decision: OD1, case enrichment (2026-11-08)

- **Context:** the probe (`docs/superpowers/notes/adcs-tensions-probe.md`) showed the current ADCS
  dataset exposes settling-vs-effort, pointing-vs-effort and pointing-vs-mass (star-tracker grade)
  as tensions, settling-vs-pointing as aligned, and no agility-vs-mass tension through wheel class
  because torque limits rarely bind. The driver recommended enrichment as a separate package.
- **Supervisor (mzargham), verbatim choice:** "Enrich as a separate package WP4b"
- **Disposition:** a new package WP4b (case enrichment) is scoped and accepted before WP7 executes;
  WP4 stays accepted; WP7 runs on the enriched dataset.

## Scope approval (approval gate)

- **Document:** `work-packages/WP7-scope-of-work.md` (draft 3, two regimes, de2f758).
- **Date:** 2026-11-08
- **Supervisor (mzargham), verbatim:** "accept 4b and approve 7 and 8. given how long its been remember to send the notebook author to look at the acds-lifecycle-demo and hc-marimo repos and pages sites to get a sense of my style"
- **Disposition:** approved; defaults list approved as one item; open decisions: none. Standing
  instruction from the supervisor: the notebook author studies the adcs-lifecycle-demo and hc-marimo
  repositories and their GitHub Pages sites first to absorb his style.

## Review gaps, round 1 (review 2c28bd0, 2026-11-08)

- Items: G-1 factual error (four of five variants); G-2 axis labels "(m)" and a weak frontier figure;
  G-7 style shortfalls (no embodied hook figure, overlong cells, no call-to-action or source link);
  G-4 misnamed uncertainty columns; G-3, G-5, G-6, G-8, G-9, G-10 minor.
- **Supervisor (mzargham), verbatim choice:** "Fix G-1, G-2, G-7, G-4, G-10; accept the rest"
- **Disposition:** one editing pass (correct the sentence; relabel axes in attribute terms and
  strengthen the frontier figure; add an embodied hook figure; split long cells; add the closing
  call-to-action and source links; rename the uncertainty columns in CSV header, script and test;
  fix the loose wording), re-execute the notebook, then a fresh-reviewer rerun. G-3, G-5, G-6, G-8,
  G-9 accept as is.

## Review gaps, round 2 (review 39bbe18, second pass)

- Items: G-12 second subset hugs the envelope only partly (disclosed); G-7r style residual (hook not
  a puzzle; cells ~2× the reference length); G-11, G-13, G-14 minor.
- **Supervisor (mzargham), verbatim choice:** "I will read the notebook first"
- **Disposition:** WP7 held at the acceptance gate pending the supervisor's own reading of
  `examples/adcs/adcs_trade_study.ipynb`; no changes meanwhile.

## Supervisor's reading (2026-11-08)

- Read in a local MkDocs preview (branch `preview/site`, served locally). Verbatim: "its really hard
  to read. we're definitely going to need to do some loops, but i expect we'll need to switch to
  claude code so the browser is in the loop."
- Disposition: WP7 remains held at the gate; readability is handled by WP9 (scoped, not executed);
  WP9's OD4 decides whether WP7 is accepted as the machine-verified baseline or closed together
  with WP9.

## Acceptance (acceptance gate)

- **Date:** 2026-11-08 (Claude Code session, the day's second session).
- **Context:** the supervisor redirected WP9 from a readability pass over this notebook to a paper
  (a mystmd article in which the notebook is the paper; see `WP10-decisions.md`, "Redirection").
  The driver asked: "With the paper replacing the WP7 notebook as the published artifact, what
  happens to WP7's held acceptance gate?" with the options "Accept WP7 as the baseline", "Close WP7
  as superseded", "Hold WP7 until the paper is accepted".
- **Supervisor (mzargham), verbatim choice:** "Accept WP7 as the baseline (Recommended)"
- **Disposition:** WP7 accepted as the machine-verified baseline. Its numbers, guards, datasets and
  figures are what the paper (WP9) reports; nothing in them changes. The WP7 notebook is retired
  as a published artifact when the paper lands (where it goes is the paper package's open decision), and its
  guards in `tests/test_notebook.py` are carried into the paper's tests. Review of record:
  `work-packages/WP7-review.md` (39bbe18, second pass); the supervisor's own reading verdict
  ("its really hard to read") stands and is answered by WP10 (the paper) and WP11 (readability loops), not by this acceptance.
- Note on the record: the driver's option labels carried a "(Recommended)" tag, against the
  decision-loop rule in `work-packages/README.md` (plain options, no steering). The label is quoted
  as shown because that is what was chosen; later questions drop the tag.

## Style study (notebook author briefing)

Written 2026-11-08 by the WP7 phase A implementer, in answer to the supervisor's standing instruction (scope approval
above). Sources read: `adcs-lifecycle-demo` (`jaxa_notebook.ipynb`, `notebook.py`, `README.md`, `site/index.html`
through the published site https://dynamicalsystemsgroup.github.io/ADCS-lifecycle-demo/) and `hc-marimo`
(`homicidal_chauffeur.py`, `TALK_NOTES.md`, `VALIDATION_CHECKLIST.md`, `README.md`, and the published site
https://mzargham.github.io/hc-marimo/). `talk.py` in both repositories was skimmed through `TALK_NOTES.md`, which
is its beat sheet. The next implementer (notebook author) should adopt the following.

1. **Open with an embodied question, not a definition.** The Pages site of hc-marimo opens with "Can a fast car with
   a bounded turning radius always catch a slower but perfectly agile pedestrian?"; the talk starts from the puzzle
   (beat 2 of `TALK_NOTES.md`) and says "Watch it get computed." The ADCS notebook opens with the question "How do
   we keep records of design judgment auditable ...". Adopt: open with the cubesat engineer's question (what must a
   small satellite give up to slew fast?), then a figure, then the method.
2. **Small visible steps, one idea per cell, numbered sections.** `jaxa_notebook.ipynb` runs ten short numbered
   sections ("## 3 . Traceable oracles ...") with a code cell that prints the quantity just named;
   `homicidal_chauffeur.py` is twelve sections (section signs) each introducing one object. Adopt: one stage per
   section, a few lines of markdown, one small code cell, one output.
3. **Prose after the output, marked as interpretation.** In `jaxa_notebook.ipynb` the sentence "The attitude error is
   still above the 0.1 line when it crosses the 120 s budget" follows the figure; the oracle records "what it computed,
   not a judgment". Adopt: every interpretation cell follows its output cell, is headed or tagged as the author's
   interpretation (human validation), and states what the output did show, not more.
4. **Verification by machine versus validation by human, stated as a distinction and shown as a section.**
   `TALK_NOTES.md` beat 9 ("Verify = did we build it right? Validate = did we build the right thing?"), the ADCS
   README ("A tool says pass. A person says satisfied.") and the hc-marimo notebook's closing V&V section (symbolic
   and numerical cross-checks, degenerate cases, symmetry) all do it. Adopt: a closing "Verification and validation"
   section with a machine-checked list (tests, lemma ids, with pointers) and a human list.
5. **A "What remains" list for the human.** `homicidal_chauffeur.py` ends its V&V with "### What Remains" (F2, F3, F4:
   checks that need visual comparison and cannot be automated), backed by `VALIDATION_CHECKLIST.md` that separates
   section A (machine-verified) from section B (requires a human). Adopt: name concretely which figures the reader
   must judge and what they should look for; leave the judgment to the reader.
6. **Limits stated plainly and early enough to matter.** The ADCS site: "Every kind of evidence has a blind spot",
   "The model is not the system", "None of them is the spacecraft". The notebook repeats "Evidence is not
   verification". Adopt: the limits section (R-12) uses the same declarative voice (hardware is stratified, values
   illustrative, times censored) and does not hedge into vagueness; the thin margins are stated as numbers.
7. **One documented visual vocabulary.** `jaxa_notebook.ipynb` defines a palette in its first code cell ("blue,
   green, purple for X, Y, Z; red reserved for limits") and uses it throughout; the hc-marimo and talk figures keep
   one colour per player. Adopt: use the plotting module's constants (`FRONTIER_COLOR`, `CATEGORY_COLORS`, ...), say
   so in the first figure cell, and never reuse a colour for a second meaning.
8. **Notation introduced at first use, plus a compact legend.** `TALK_NOTES.md` beat 4c: "capital = policy, lowercase
   = action" introduced before the symbols appear; "define the controls before they appear in the dynamics".
   Adopt: define V, Z, tau, orientation and the contending set where they first occur, in one sentence each, with the
   quickstart table near the top (SciPy paper prescription, `presentation-framing.md`).
9. **Name what was assumed, derived, inherited, leaned on.** Beat 8-9 of the talk: a script "that derives it, checks
   it, and names what it assumed" (`AXIOMS_USED`), and a ledger of Derived, Posited, Inherited, Leaned-on. Adopt in
   the final section: the conditions of the theory the case touches (R1, A4, conditioning, regime), by ledger tag.
10. **Credit sources and claim only the implementation.** The ADCS notebook's ontology section: "The contribution is
    the assembly, not new terms - imported like open-source packages"; hc-marimo credits Isaacs (1951) and cites the
    literature in its extensions section; the site credits author, group and projects used. Adopt: cite the packages
    and the prior work the notebook uses; no novelty, priority or "first" claims; "novelty" is used only as the
    technical term V - 1.
11. **Show the failure or the unwelcome result, then discuss it.** `jaxa_notebook.ipynb` section 3 shows REQ-001 failing
    ("the behavior model itself tells us the settling requirement is not met") before the retune in section 7, and
    the attestation text says the evidence shows the requirement is "not yet satisfied". Adopt: report the
    propose-predict-check comparison whether or not it is inside the band, and say plainly when a prediction misses.
12. **Landing-page tone and cards for anything the notebook points to.** Both sites: a single scrolling page, short
    declarative sentences, bold labels, one card per artifact with a bold title, a stack line of tools, an audience
    note, a one-sentence description and a call to action ("Open the notebook ->"), "start wherever suits you",
    source link at the foot. Adopt: the notebook's opening cell reads like a card (title, byline, stack line, one
    paragraph, links); WP8 should reuse the card form.
13. **Narrative arc over taxonomy.** The ADCS notebook is organized as acts ("Act 1: The Assignment" ... "Act 8:
    Design Iteration") and the HC talk as ten beats ending on the human step. Adopt: keep the R-3 stage headings, but
    let each section end by saying what the next one needs from it; end on validation, the human step, not on a
    summary of results.
14. **Honest mode flags for anything not live.** The ADCS README labels each piece of its demo as precomputed or live
    with a "labelled fallback"; `jaxa_notebook.ipynb` prints "FLEXO_TOKEN not set - offline rehearsal mode". Adopt:
    where the notebook reads cached results (datasets, check designs), say so in the cell output ("read from
    `check_designs_cubesat.csv`, simulated once by `make_check_designs.py`"); no silent regeneration.
15. **No emojis, no hype.** Neither repository uses emojis in notebooks; the sites avoid superlatives and say what the
    page does. Adopt: plain headings, no exclamation, no "powerful", "novel" or "breakthrough".

(Observed difference to respect: the two repositories are written as marimo notebooks or Jupyter notebooks with
interleaved HTML helper output; WP7's deliverable is a plain executed Jupyter notebook, so interactive sliders are not
used; the static figures carry the story.)

## Author notes (WP7 phase B, notebook author)

Written 2026-11-08 by the notebook author. The notebook is `examples/adcs/adcs_trade_study.ipynb`, built with `nbformat`
from a script kept outside the repository and executed with `jupyter nbconvert --execute --to notebook --inplace`
(about 11 s; needs `uv sync --group notebooks`, no change to `pyproject.toml` or `uv.lock`). Style points of the study above
that were applied, and where:

- Point 1 (embodied question first): section 1 opens with the designer's questions and a figure of the raw attributes; no
  method before it. No tension or n-lemma is named before the report cell (checked by `tests/test_notebook.py`).
- Point 2 (small visible steps): sixteen numbered sections, one object each, a short markdown cell and one code cell.
- Point 3 (prose after output, marked): every "What the output shows" cell follows its output; section 9 is headed as the
  author's interpretation for human validation and comes after the report and the sensitivity table.
- Points 4 and 5 (verify versus validate, what remains): section 16, with the machine-verified list (tests, L1 to L9
  with tags, ledger R1, A4, F5, F10 with failure modes) and a seven-item "What remains for a human".
- Point 6 (limits plainly): section 15 in declarative voice with the notebook's own numbers; the thin margins are numbers.
- Point 7 (one visual vocabulary): the plotting module's constants, printed in the first cell; wheel class is the only
  categorical colouring; measured check designs add one colour (`CATEGORY_COLORS[3]`), declared there.
- Point 8 (notation at first use): a notation table after the hook and definitions repeated where each symbol first works.
- Point 9 (assumed, derived, inherited): section 16 lists the conditions by ledger tag.
- Point 10 (credit, no priority claims): plain-text citation lines with existing bib keys; "novelty" only as V - 1.
- Point 11 (show the unwelcome result): the propose-predict-check comparison is reported as measured: log V inside the band
  for all three, position along the frontier outside it for all three, two of three proposals fail `dod_ok`.
- Point 12 (card): the opening cell has title, stack line, one paragraph and pointers.
- Point 13 (arc): each section ends with a "Next" line; the notebook ends on the human step.
- Point 14 (mode flags): the load and check cells print "read from ... (cached ...)"; nothing is regenerated or simulated.
- Point 15 (no emojis, no hype): none used.

Deviations and findings the reviewer should know:

- The "reference shifted +0.5 log-spread on all metrics" check of the default list multiplies every score by one factor and
  leaves the fit unchanged by L2 (the notebook shows that it does); an alternating +0.5 / -0.5 shift was added as the real
  probe of the reference point.
- The sensitivity and interpretation sections come after the tension report (they need its output), which is a section
  order the scope allows (R-3 lists stages, not their placement relative to the interpretation).
- Defect in the recorded predictions file, not changed: the columns `pred_std_z1`, `pred_std_z2`, `pred_std_z3`,
  `pred_std_log_v` of `check_predictions_cubesat.csv` are the delta-method standard deviations of the four predicted
  metrics (slew time, pointing error, control effort, total mass; `TradeSpaceRegressor.predict_std` has shape
  (n, n_metrics)), written by `make_check_designs.py` under coordinate names. The notebook shows them under their true meaning.
- The damping figures (a third underdamped, 4.7 % below 0.5) are quoted from the WP4b record; the dataset has no damping column
  and the notebook does not recompute them.
- Contending sets are not stable in detail under the conditioning checks (effort leaves the set under the robust scaler and
  the eight-metric refit); total mass and pointing error stay in all five variants. The notebook reports this.

### Editing pass (after the supervisor's disposition "Fix G-1, G-2, G-7, G-4, G-10; accept the rest")

Notebook author, 2026-11-08. G-3, G-5, G-6, G-8 and G-9 are untouched, as dispositioned.

- **G-1.** Section 8 reading corrected: control effort loads against an agility metric in the first principal direction in four of
  the five variants (and one of the four, the all-metric shift, is the baseline again by L2); the exception is the eight-metric
  refit, where the first direction is led by total mass (-0.58) and control effort (-0.46) and settling time loads +0.04. The sensitivity
  cell now prints the effort and agility loadings of direction 1 per variant, so the sentence is checkable from the output.
- **G-2.** Axis labels of every figure are in attribute terms with units and say "conditioned ... (larger is better)" where a conditioned
  metric is shown; no "(m)" labels remain. Figure 03 is now a 2 x 2 figure: the 3-D surface (left) and an edge-on log-space view of the
  same surface (right: each design against the height of V = 1 above it, black line V = 1, grey band, near-frontier designs ringed).
  It shows the hugging in the first subset and shows plainly that in the second subset the surface runs above the data at its upper end
  (reported in the reading). Hole colour is called vermillion everywhere in the notebook (a test forbids "red").
- **G-7.** Figure 01 is now a hook of two designs picked by one column each (the fastest slew, the lightest bus), their ten attributes as
  factors of the table median, and the table cloud of slew time and mass by wheel class (`01_two_designs.png` replaces `01_attributes.png`);
  it names no tension (test unchanged). Section 9 and the report, regime and verification cells are split into short cells of one idea each
  (mechanism, design variable, what would change it). The notebook ends with "Where to go from here": next steps by interest (derivations,
  toolkit and API, limitations, the SysML model, your own data with a five-line recipe) and links to the repository, the specification and
  `docs/method.md`; the card at the top carries the repository link.
- **G-4.** The four standard-deviation columns of `check_predictions_cubesat.csv` are now `pred_std_slew_time_s`,
  `pred_std_pointing_error_deg`, `pred_std_control_effort`, `pred_std_total_mass_kg` (header only; data rows are byte-identical, checked
  with a diff of the rows). `make_check_designs.py` writes them under those names and its docstring says what they are;
  `tests/test_check_designs.py` and the notebook follow.
- **G-10.** Section 8 no longer says the uniform shift "multiplies every score": it adds the constant to every score and to the fitted
  offset, and the exponents are unchanged (L2). (The first author note above, which used the old wording, is the record of the earlier draft.)
- Tests: `tests/test_notebook.py` keeps all guards and adds: no "(m)" in figure code, "vermillion" and no "red", a closing call-to-action
  with the repository link, the hook figure before section 2, and the renamed prediction columns.
