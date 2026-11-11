# WP31 — Review report (choosing K in the documentation)

| | |
|---|---|
| **Scope of work** | None as a package document: the supervisor's request (`driver-log.md`, "Choosing K in the documentation") and the driver's stage 2 (`WP31-decisions.md`); requirements below are derived from the stage 2 text, which the supervisor's request bound. |
| **Work reviewed** | commits 9acd878, 19fb2b5, 39582fe, e155772 on `dev`; worktree `wp31review` at origin/dev head `cd2aad2a0d0f7ed920334d57d8455e95faf25f24` |
| **Reviewer** | a fresh agent that did not build the work; reviews and does not accept |
| **Acceptance record** | the supervisor's (stage 3 and the three task readers, stage 4, follow) |

Scratch evidence (screenshots, page output, sweep rerun): `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp31review/`.

## Requirements (derived from `WP31-decisions.md`, stage 2)

| ID | Requirement | Verdict | Evidence |
|---|---|---|---|
| R-1 | Placement A: new page `user-guide/choosing-k.md` between Fitting and Tensions; in nav | met | `mkdocs.yml` nav; built site lists "Choosing K" between Fitting and Tensions (screenshots). |
| R-2 | Contract amendment 17 adds the page to `docs.pages`; manifest and document agree | met | `interface-contract.md` block and `.toml` both carry the page in `docs.pages` and `presentation_pages`, version 17, change-log row 17; `uv run pytest tests/test_interface_contract.py`: 92 passed. |
| R-3 | Fitting page's K section shrinks to a pointer (net negative there) | met | Diff 9acd878..e155772 on `fitting.md`: about 40 lines out; the pointer is the inline link "(Choosing K)" on the several-terms sentence; the section now headed "The temperature and the band at several terms". Budget 800 to 668. |
| R-4 | The 0.31 sentence corrected first, before the page | met | 19fb2b5 (before 39582fe) narrows it; 39582fe then removes the whole section, so no 0.31 or "K = 4 is too large" remains anywhere in `docs/` (grep). Commit message's eight-seed spread (0.03 to 0.06 at K = 1 ... 0.17 to 0.61 at K = 4) I did not re-run (it backs no page sentence now); the readout's own non-reproduction (0.55 at K = 3) I did not contradict. |
| R-5 | Methods first, each with what it cannot say: mean slack at one temperature (no break possible by construction; elbow where there is one, none where not), planted check, resampling check with noise stated, certificate and term share as readings not selectors | met | Page "Methods" has six bullets each ending in what it cannot say. Term share is a "thinnest term" bullet, certificate a bullet, plus `conditioning_` (an addition beyond the stage 2 text, in the readout's table). |
| R-6 | What large K does on our data, stated from sweep and lemmas, not by analogy | partly | The final section states: slack still falling at the largest K tried, unmatched terms appear beyond K0, thinnest share 0.00 on the K0 = 2 table at K = 5; all from the page's own blocks. The stage 2 text also listed "the stable radius shrinks, the n-lemmas fragment"; the page says neither (the readout found no radius trend, so omitting radius is right; the stage 2 line is wrong there) and cites no lemma. See G-2. |
| R-7 | Two worked examples: a planted table (K0 = 2 and 3) and the cubesat, both regimes | met | Sections "A planted table" (K0 = 2; K0 = 3 tables 0 and 1) and "The cubesat" (primary and stock), each with runnable blocks. |
| R-8 | PCA elbow named once, with the sentence that our large-K limit differs and how | met | Last section: one paragraph, "variance explained ends at d components, while here K has no ceiling and the mean slack no floor", backed by the sweeps. The analogy is not leaned on. The page does state that a table can have no break. |
| R-9 | No held-out criterion claimed | met | The page never mentions or implies one (grep "held-out", "cross-valid": none). It also does not say none exists; see G-3. |
| R-10 | Every claim backed or narrowed; numbers reproduce | met with gaps | Ran all five runnable blocks (`page_output.txt`); every number in the prose reproduces (K0 = 2 drops 0.108, 0.005...; K0 = 3 table 0 0.163, 0.029 and three found at K = 3; table 1 0.181, 0.006, two found; movement 0.04 0.02 / 0.23 0.24; stock 0.065, 0.068, 0.011, 0.004 with thinnest 0.17; primary 0.112, 0.044, 0.017, 0.010 with 0.07; movement ranges 0.09 to 0.45, 0.25 to 0.69, 0.17 to 0.54; radius 3e-06 to 1e-04). Rows C427 to C439 exist, all `backed`, and `test_claims_register` reports no failure on them. Re-ran `WP31-readout/k_sweep.py cubesat stock`: output byte-identical to the committed `cubesat-stock.csv`, and agrees with the page's stock figures. Gaps G-1, G-4. |
| R-11 | Runnable blocks execute | met | `uv run pytest -q -k runnable tests/test_docs.py`: 10 passed in 89 s. |
| R-12 | Build, vocabulary, glossary | met | `build_generated.py` ok; `mkdocs build --strict` as run by `assemble_site.py` passes for the docs (the bare `mkdocs build --strict` fails on missing generated figures, which `build_figures` makes first; same on every page, not WP31). `check_vocabulary.py`: 0 new violations. No new term, so no glossary entry (agree: "thinnest term", "movement" are descriptive). |
| R-13 | Word budgets | met | `tests/test_site.py` budgets: choosing-k 677, fitting 668, termination 743, total 7450 (test passes in the part that runs). |
| R-14 | Side units: conditioning pointer (9acd878), termination `min_exponent=0.1` sentence (e155772) | met | Both present in the built pages; termination sentence "at the default of zero ... prints 12.4" (the claim was not re-run by me; outside the page under review). |
| R-15 | Rendered look | met | Screenshots below: desktop light and dark, phone 375: no horizontal overflow (scrollWidth 375 on every page), code blocks wrap in their own scroll, table of contents and nav entry correct. Static blocks show no output; the prose numbers are only backed by running the blocks, as on the other pages. |

## Outside the scope

- Out-of-scope changes: none in the four commits beyond the termination.md sentence and the conditioning.md pointer, both listed as units.
- Non-goals touched: none; the paper is untouched.

## Screenshots (own, headless Chrome through the DevTools protocol; the pane's own tab-56 was also viewed)

All under the scratchpad directory above: `choosing-k-desktop-light.png`, `choosing-k-desktop-dark.png`, `choosing-k-phone375-light.png`, `choosing-k-phone375-dark.png`, `fitting-desktop-light.png`, `fitting-desktop-dark.png`, `fitting-phone375-light.png`, `termination-desktop-light.png`, `termination-desktop-dark.png`, `termination-phone375-light.png`, `conditioning-desktop-light.png`, `conditioning-desktop-dark.png`, `conditioning-phone375-light.png`; crops `crop-dark.png`, `crop-phone-dark.png`. Dark is forced by setting `data-md-color-scheme="slate"` after load (the emulated media query did not switch Material). The fitting, termination and conditioning pages were looked at only in the changed passages and for layout; none shows a defect.

Site served: `python3 -m http.server 8793 --bind 127.0.0.1` from `/Users/z/Documents/GitHub/wp31review/_stage`, pid 24833 (the docs, root index and figure1 are built; the paper slot is absent because `assemble_site.py` stopped at the Why image on a missing DejaVu Sans font in this sandbox, after the docs were built).

## Observations and gaps

- **G-1.** The page says the certificate holds "at every K tried"; at K = 1 the status is `not_applicable` (the helper asserts "certified or not_applicable"). Likewise the K0 = 3 table 1 "finds two of the three at every K" is false at K = 1 (found 0). Narrow to "K = 2 and above". Not a number error, a wording one.
- **G-2.** The stage 2 text promised the stable radius shrinking and the n-lemmas fragmenting at large K; the page has neither and no lemma citation. The readout says the radius has no trend, so the stage 2 line should be amended, and the page might cite the lemma on fragmentation if one backs it.
- **G-3.** The page claims no held-out criterion but does not say the package has none; a reader asking "do I cross-validate K" gets no answer. One sentence would do.
- **G-4.** Claim coverage: register rows exist for the numbers, but not for the method statements ("mean_slack_ comparable across K only at one temperature, objective_ not at all", "movement at most 2", "the planted check tests the method, not your table's K"). The glossary says mean slack "cannot choose K" while the page says a break "marks a K worth keeping"; reconcile the two.
- **G-5 (not WP31).** At dev head `uv run pytest tests/test_claims_register.py::test_the_register_holds` fails on C192 and C195 (`docs/theory.md`) and C375 (`termination.md`): fragments no longer found after WP8b D-6 (cfbad4f, `paper:key` citations). None is a WP31 row. In this sandbox the `tests/test_site.py` tests that assemble the site also error on the missing DejaVu font (environment).
- Observation: the page is 677 words plus a 55-line helper block shown before the first example; a reader meets code before any example output. The marginal-value question for the `thinnest term` and `conditioning_` bullets (short, useful) I judge passed; none is a deletion candidate.

## Gap dispositions

Not asked of the supervisor here (the review stops before the decision loop; the driver takes it).

## Recommendation

Recommend acceptance with the listed gaps noted: every stage 2 element is present, every number on the page reproduces, the blocks run, the site builds and renders in both schemes and at 375 px, and the elbow and held-out limits are honestly drawn. G-1 and G-3 are one-sentence fixes worth making before the three task readers; G-2 is a stage 2 text correction. This report does not accept the work.
