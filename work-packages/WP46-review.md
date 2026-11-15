# WP46 review record: the fit temperature as a path (implementer's pass; the fresh reader is still to run)

This is the implementer's record of what was run and looked at. D-5 asks for one fresh reader to read the page in a
browser with their own sweep; that reader was not dispatched by the implementer (a unit may not start sub-agents), so
the fresh-reader item is open for the PM.

## What was run

- `uv run pytest -q tests/test_temperature_path.py src/hyperbolic_trade_space/plotting.py`: 24 passed, including the
  doctests of `temperature_path` and `plot_temperature_path` and the slow R-1 test against the case's
  `tau_sweep_lines_figure` on a 300-design sample of the data of record (lines equal to 5e-4, names equal).
- `uv run python -m derivation.proofmap` (PROOF MAP OK, 21 files, 531 steps) and `uv run python derivation/run.py`
  (ALL LEMMAS PASS, L22 among them).
- `uv run python work-packages/WP46-rounds/small_tau_check.py` on the data of record (D-3, `WP46-rounds/`).
- `uv run python scripts/stage_site.py` (paper strict build, exit 0) and again with `--paper placeholder` after the
  figure's layout fix; the docs build reports no warning for the page beyond the paper-link INFO lines every page has.
- `uv run python scripts/check_vocabulary.py`: 0 new violations. The claims register check: passes with C823 to C841 (C706 deleted).

## What was looked at (screenshots held outside the tree per the WP40 rule, in the unit's scratchpad)

- The page `/docs/user-guide/temperature/` in a browser (staged site served on 127.0.0.1:8846, one tab), dark scheme,
  narrow pane; the figure renders, the three panels and the ring at the fit temperature are legible; the page links
  from Fitting, Choosing K and the API page resolve. One 404 on the console is `/favicon.ico`, which the whole staged
  site has.
- The figure as an image in both schemes. Defects found by looking and fixed: the top-right panel's y label ran into
  the left panel (the helper now lays out its own figure), and the fit temperature's tick label (49) overprinted its
  neighbour (42), so the neighbour's label is now left blank.

## Items for the PM

1. **D-3's criterion is not met** (`WP46-rounds/small-tau-check.md`): the tau = 3 fit is within 0.0021 of the
   minimum-variance fit but three of thirteen exponents differ at three places. By R-2 the page says the small-tau end
   is a regularity the sweep shows, not a derived limit; the lemma (L22) verifies and the page cites it only for what
   it proves.
2. **Adding L22 to the chain breaks three paper tests that R-4 forbids the unit to fix**:
   `test_appendix_b_committed_output_is_current`, `test_appendix_b_shows_every_result_of_the_record_with_derived_counts`
   and `test_cr18_regenerate_row_reproduces_the_committed_output_of_a_row` (the committed outputs of
   `paper/supporting_material.ipynb` and the heading "(L12 to L20)" of its B.2 cell). They pass once the Appendix B
   outputs are regenerated and the heading reads L22; that is a change under `paper/` and the PM's call.
3. The claims rows were renumbered to C823 to C841 at the rebase onto dev a1879e6 (dev holds C676 to C692; C693 and C694 are reserved for the root page); C706 is deleted.
4. Housekeeping the new page forced, all additive: interface-contract amendment 24 (`docs.pages`,
   `docs.presentation_pages`; version 23 to 24); `tests/test_site.py` gains the page in `NAV_PAGES` and a word budget
   (564) with the total ceiling raised by the same amount (7237 to 7801); the docsite's figure captions after Fitting
   are renumbered (Figure 3 is the new one, Tensions 4, Chart 5, Examples 6 and 7); `tests/test_build_generated.py`
   expects a chain of 21.
5. The page links Appendix B for lemma 22 (`paper:appendix-b`); until the paper's Appendix B is regenerated (item 2)
   the appendix does not show L22.

## Appendix B regeneration (R-4 amended by the driver)

`uv run python paper/execute_notebooks.py` was run; only `paper/supporting_material.ipynb` changed (`paper.ipynb` came back
byte-identical). Changes: the lemma-21 row and its proof section; the derived totals in "how to read" (computed 333 to 356
steps, by declared axiom 160 to 163, results and steps counts follow from L22's 26 steps); the Appendix B.2 heading and the
contents line, "L12 to L20" to "L12 to L22" (a hand-held heading, edited once). No value outside the lemma-21 row and the
totals it enters moved; no platform-dependent value moved. `tests/test_paper.py` and the register tests: 225 passed.
Claims ids were renumbered (C823 to C841) before this instruction arrived; PM16 renumbers again from the register's last id at landing.

**Renumbered at landing (2026-11-14, the driver):** the small-temperature lemma is L22 on dev, not L21, because the WP42 build landed first with the tension lemma as L21; every step id, the script name, the register rows, the temperature page and the regenerated Appendix B say L22.
