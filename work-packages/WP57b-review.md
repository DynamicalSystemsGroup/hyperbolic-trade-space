# WP57b review: Appendix B

Branch `wp57ab`, one commit after WP57a's d4f6fc5. Every count below is read from a named generated output:
`work-packages/WP57-rounds/a/counts-after.txt` (the state after WP57a, the "before" here) and
`work-packages/WP57-rounds/b/counts-after.txt` (`uv run python work-packages/WP57-rounds/map_counts.py --paper
paper/paper.ipynb --supp paper/supporting_material.ipynb`), `work-packages/WP57-rounds/b/pointers.txt`,
`tests/test_paper.py`, `scripts/check_vocabulary.py`, `scripts/check_residuals.py`, `python -m derivation.proofmap`,
the MyST build log. Screenshots: `work-packages/WP57-rounds/b/*.png`.

## What changed

| Place | Before | After | No longer does |
|---|---|---|---|
| Cell `app-B-job` | the Job block (112 words) and "What the scripts establish" (125) | "What the scripts establish" alone (125; C387 to C389 keep their rows) | says what the main text keeps and what the repository keeps |
| `generate_proofs.how_to_read` (cell `tab-B-how-to-read`) | the rule, the counts, the three kinds, the two-parts list, the closing paragraph | the rule, the counts, the three kinds, the shared-file sentence (generated words of the `appendix-b` row: 888 to 793) | lists the appendix's parts; repeats Section 9's sentence that the checker cannot say a sentence means what its line computes |
| Cell `app-B-2`, the paragraph under B.2's heading | "The algorithm", 398 words | "Restarts, stopping and the polish", 121 words | restates Section 5's alternation, labels and program (`eq-slack`); comments on L16, L17, L18, L19 and L21 before their tables; says which result the paper does not use |
| `proof_map`, B.1 `proofs_fit`, `proofs_solver`, B.3 `checker` | | unchanged (`counts-after.txt`: B.1 10,748 generated words and 184 rows, B.2's table 21,238 and 365, B.3 596 and 30) | |

Typed prose of Appendix B: 635 to 246 (`B` row 237 to 125, `B.2` row 398 to 121). The supporting material in all:
3,980 to 3,591 typed words, 55,659 to 55,564 generated, 1,237 to 1,237 rows.

"L16 does not prove that the alternation converges" (C142) is the second line of
`work-packages/WP57-rounds/assumptions-queue.md`, for WP57d.

## Register rows

Retired with their sentences: C132, C133, C134, C135, C136 (the offsets, the alternation, the sharp limit, the
separation into one program per term), C139, C140, C141 (L16's bound and its generalized-posynomial form, the Boyd et
al. citation), C142 (queued), C143, C144 (L17's Hessian and second-order test), C145, C146 (the label belongs to the
package), C667 (L19 unused by the paper). The main text carries these statements in its own sentences with their own
rows (WP55's C922 to C966). Kept, their fragments verbatim in the new paragraph: C137 ("For each restart the package
starts from random centres in the chart"), C138 ("if the mean slack rose, stop with the previous state"), C666 ("five
reduced Newton steps (the polish)"). No row added.

## Every L-pointer and its landing (G4, R-1)

`work-packages/WP57-rounds/b/pointers.txt`: the 25 distinct "Appendix B, Ln" pointers of Sections 3 to 6 (every
one a `{ref}` to `<appendix-b>`, the appendix's heading; the main text is a non-goal here, so the targets are as WP55
left them), each with the id of its result's heading in the rendered appendix (`generate_proofs._anchor`: `proof-l1`
to `proof-l21`) and, for the four step pointers (L3.9, L5.25, L17.13, L17.19), the step's row in its table. All 25
land; the proof map's rows link the same ids. The script:

```python
import paper_paths, json, re
import generate_proofs as gp

nb = json.load(open("paper.ipynb"))
sect = ""
pointers = {}
for c in nb["cells"]:
    if c["cell_type"] != "markdown":
        continue
    src = "".join(c["source"])
    for a in re.findall(r"^\((sect-[a-z0-9-]+)\)=", src, re.M):
        sect = a
    for m in re.finditer(r"Appendix B, (L[0-9.]+(?: to L[0-9.]+)?) <appendix-b>", src):
        pointers.setdefault(m.group(1), set()).add(sect)
fit, solver = str(gp.proofs_fit()), str(gp.proofs_solver())
for ptr in pointers:
    n = int(re.match(r"L(\d+)", ptr).group(1))
    table = fit if n <= 11 else solver
    assert f'id="{gp._anchor(n)}"' in table
    for t in re.findall(r"L[\d.]+", ptr):
        if "." in t:
            assert re.search(r"^\| \*\*%s\*\* \|" % re.escape(t), table, re.M)
```

## Tests

- `JOB_BLOCKS` loses B (A, B, F, G carry no Job block or tier phrase).
- `test_appendix_b_shows_every_result_of_the_record_with_derived_counts`: the counts in `how_to_read` and the heading
  of B.2 as before; the `(L12 to L22)` assertion on `how_to_read` goes with the parts list; asserts "two parts" and
  "human validation" are absent.
- `test_the_polish_and_the_unused_lemma_are_named_in_appendix_b2` becomes `test_appendix_b2_is_the_restart_stop_and_polish_rules`.
- `test_the_claims_of_c1_have_their_true_basis` (named in D-4): unchanged; it reads Methods and D.13, not B.2.

## Requirements

| ID | Check | Result |
|---|---|---|
| R-1 | kept subsections cited; every lemma label resolves | `pytest tests/test_paper.py -k references_resolve`: 1 passed, 235 deselected in 0.90s; `pointers.txt`, 25 of 25 land |
| R-2 | nothing about the paper's text; `how_to_read` states no Section 9 sentence | `check_residuals.py --json` on dev's tree (b5b3a86) and on this branch after both children: metanarration 16 to 8, parens 823 to 810, long sentences 263 to 256, compound 188 to 182, restatements 8 to 8 (a first draft of B.2 had one, the sentence on the returned restart repeating the one before it; reworded before the commit); `--compare --strict` against the WP38 baseline: 129 counts above it on dev, 129 here (B.2's 121-word paragraph is under the inventory's `MIN_WORDS` of 150, so `prose_surfaces` folds it into L12's piece, `appendix/b-2`; the folded piece's counts are at or below the sum of dev's `b-2` and `l12`: parens 16 against 21, long sentences 3 against 5, compound 2 against 4). The per-document first-use report moves two glossary terms, `generalized posynomial` and `generalized geometric program`, to an undefined first use in the supporting material (273 to 275 in all): their first uses were B.2's cut sentences with a definition cue, and are now L16's generated statement and G.1's register text; the paper's own first uses (Sections 3 and 4) are unchanged and `check_vocabulary` reports 0 new; the page states no sentence about the paper's text |
| R-3 | the L16 clause in the queue; the cut text at `git show c89843a:paper/supporting_material.ipynb` (cells `app-B-job`, `app-B-2` unchanged between c89843a and WP57a's d4f6fc5) | the queue's second line |
| R-4 | proof map and derivation unchanged | `PROOF MAP OK: 22 lemma files, 549 tagged steps`; `git diff dev -- derivation/` empty |
| R-5 | suites, lint, format, lock, vocabulary, build | `uv run pytest -q -m "not slow"`: 2,086 passed, 17 skipped, 2 xfailed, one failure that was the B.2 test reading the sentence reworded while the suite ran; `tests/test_paper.py -m "not slow"` rerun on the final state: 206 passed, 3 skipped; `uv run pytest -q -m slow tests/test_paper.py`, once after both children: 27 passed in 22 min 55 s; `ruff check`, `ruff format --check`, `uv lock --check` clean; `check_vocabulary.py` 0 new, 67 known; the MyST build log without a warning or error |

## Screenshots

`work-packages/WP57-rounds/b/`: `B-top.png` (the appendix opens on "What the scripts establish", then the rule and the kinds, then the proof map), `B2.png` (the heading, the one paragraph, then L12's statement and step table), `L16-table.png` (the step table reached from Section 6's "Proof: Appendix B, L16" pointer, `#proof-l16`). Page checks by the screenshot script at 1,280 px: "Job." occurs four times (C, D, E, H); "two parts", "human validation" and the L19 sentence absent; "random centres in the chart" present; every id `proof-l1` to `proof-l22` on the page; a cell reading `L17.13` present; no horizontal overflow.
