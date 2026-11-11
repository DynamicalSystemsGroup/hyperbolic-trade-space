# appendix-f

## Q1. What this appendix conveys

It tells a reader how to regenerate the paper's numbers, tables and figures: the pinned software versions, the one environment where results reproduce exactly (and how other platforms differ only in last digits), the commands with what a pass looks like, and, for each table and figure, the call that makes it, what it reads and where it writes.

## Q2. Which sentence of the story it serves

The Contribution sentence of Section 1, "Scaling up trade studies with a reproducible method", together with Section 1's demand that the justification be "recognized, reproducible, rigorous" and the line "each has hypotheses, a sketch and a script" introducing the main results. The Organization line names it ("F reproducibility"). It serves no single main-results item 1 to 7; it backs all of them by making their scripts runnable.

## Q3. Verdict: advances

The story claims a reproducible method, and this is the only unit that says concretely how to reproduce it: the versions, the environment of record and the commands. Section 11 keeps only a few sentences and points here for exactly these four things, so no other unit carries them. Its job statement ("every figure, table and reported number") is somewhat larger than what F.4 lists: only three of the main text's figures (fig-tau-sweep, fig-tensions-k3, fig-regimes) have rows, and reported numbers in the prose have none, so a reader who wants to regenerate, say, Figure 5 or the count 126 must go through the notebook execution command instead of a row.

## Q4. If "repeats"

Not applicable.

## Q7. Tables

- `tab-F-toolchain`: pointed to, yes (Section 11: "Appendix F gives the pinned toolchain"). A reader wanting the full version would look for it, yes, for the exact versions behind "reproducible". Verdict: advances; the only place the versions and the build's commit and platform are stated.
- `tab-F-commands`: pointed to, yes (Section 11: "the commands"). A reader would look for it, yes, for how to rerun the tests, the lemma scripts and the notebooks and what success looks like. Verdict: advances; it turns "each has a script" into commands with pass criteria. The notebook-execution row is long and dense in its pass column.
- `tab-F-reproduction`: pointed to, yes (Section 11: "one row per item"). A reader would look for it, yes, to find which call produces a given table or figure. Verdict: advances, with the caveat that most of its 44 rows repeat the same "Reads" entry (the regimes' CSV directory), and it lists only three main-text figures, not all nine, so it is less complete than its job statement promises.

## Q9. Read twice and could not place

- "the ledger" (in "The repository keeps: ... the Dockerfile and the ledger"): which ledger is meant (the gaps ledger of Appendix E, or a proof ledger) is not said here.
- "the history layer carries the commit" and "a git bundle that paper/container/build.sh passes in": I can tell this is container mechanics, but not why a reader of the paper needs it.
- "every figure" in the Job line against F.4: Figures 1, 2, 3, 5, 6 and 7 of the main text have no row; I could not tell whether they are made elsewhere or simply omitted.
