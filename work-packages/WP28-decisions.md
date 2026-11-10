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
