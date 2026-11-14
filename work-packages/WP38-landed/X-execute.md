# WP38 X-execute: notebook landing

Rebased N1 and N2 onto origin/dev; both notebooks executed once (paper/execute_notebooks.py,
warmed font cache, no stderr output); no figure file under paper/figures changed; no quoted
number moved (the only output differences are supporting_material.ipynb's cell text from N2's
page-template and glossary edits).

## The three test pins
- "number of designs and of metrics" (decision problem): restored in the Contribution sentence
  (the rewording to "as designs and metrics are added" is undone; the claim is the pinned one).
- "the level of a potential relative to the fitted reference surface" (Definitions): the test was
  over-pinned to a restated sentence the cut removed on purpose (Definition 2 says it); the test
  is re-pointed to "a design's level relative to the fitted reference surface", which survives.
- "not the Pareto boundary" in main result 1 (found on the first full run): the sentence is a
  claim, so a short form is restored ("It is not the Pareto boundary: ..."); the longer clause
  stays cut. The decision-problem ledger cut row is corrected to 45 words removed.

No second execution was needed: the three fixes are in markdown sources and a test, not outputs.

## Checks
Group (test_paper, claims_register, site, docs, text_encoding, residuals, gaps): 377 passed,
4 skipped. `pytest -m "not slow"` (rest): 1618 passed. ruff, format, uv lock, vocabulary: clean.
Checker after: work-packages/WP38-landed/after-checker.txt.
