# WP41 review: the bridge to the search, part 1 (implementer's record, before acceptance)

Branch `wp41` from `dev` d5c2576. Not yet reviewed by a fresh reader; the fresh-reader pass of D-5 is open (see the end).

## Deliverables

| ID | State | Evidence |
|---|---|---|
| D-1 | Done | `work-packages/WP41-rounds/spike/readout.md` (note, audit of twelve pieces, three rules, plain options), `selection_rules.py`, `run-record.txt`. The existing rule, recomputed, reproduces the three committed proposals. |
| D-2 | Done | `docs/bridge.md`, in the navigation after Examples, linked from the docs home and from a new Examples section. Staged with `scripts/stage_site.py --paper placeholder` and read in a browser (below). |
| D-3 | Done, with two narrowings | Section 7 gains one paragraph (57 words by `words_by_section`, 233 to 290) naming proposal, selection rule and check and the predicted-against-measured clause; ledger row added. (1) The Open sentence (request 169) is not touched: `paperfix3` already carries it, so it lands with that branch. (2) The pointer to Appendix D.10 is left out: `test_search_section_is_short_future_work_without_numbers` (R-15) requires no digit in the section and the reference role needs its text to end in `D.10`; relaxing R-15 would restore it, the supervisor's call. |
| D-4 | Done | Glossary: proposal, selection rule, check, with aliases and the stems `proposal`, `check`; claims rows C648 to C663. |
| D-5 | Partly | This record, with my own browser pass. The fresh reader (P3 or P9, Haiku) was not run: the unit may not spawn sub-agents. Open for the PM. |

## Requirements

- R-1: `uv run python scripts/check_vocabulary.py` reports 0 new violations. Before the Section 7 paragraph it reported two first-use violations (proposal and selection rule were used with no definition in paragraph); the paragraph, placed before the loops it names, resolves them.
- R-2: claims rows for every new sentence of the page and the paragraph; `tests/test_claims_register.py` passes; the 0.2 items are named as not shipped on the page.
- R-3: the audit names the regressor, the pooled proposal and its radius (both the frozen script and the data of record's `Proposer`), the check designs, the noise injection, Section 7 and Appendix D.10, each placed or marked missing.
- R-4: the prototypes run from the committed v2 data of record; the locally run v2 oracle reproduces the committed rows (settling time to 7 figures; control effort differs in the fifth figure).
- R-5: the page builds in the strict MkDocs build (staged), renders, no console error of the page's own: the only failed loads are external (Google fonts, jsDelivr MathJax request, the GitHub releases API), present on every docs page of the staged site; mathematics rendered.
- R-6: `git diff d5c2576 -- paper/paper.ipynb` is the one inserted paragraph; no other cell changes.

## Browser pass (own tab, port 8795, placeholder paper)

- `/docs/bridge/` at desktop width (dark scheme as the browser presented it): title, intro, the three-way list, the two routes, the code block (no line over the column, copy button present), the outcomes list, the closing list all read; the table of contents on the right and the navigation entry "From the chart back to a design" present; `1/\tau` rendered as mathematics.
- 375 px: no horizontal overflow (document scroll width 375 = client width 375; the code block 375 = 375); headings and lists wrap.
- Links: the three paper links resolve in the staged site to `/paper/#sect-search`, `#thm-pullback`, `#thm-chart` and the supporting material's `#sub-d-10` (the paper there is the placeholder, so the targets were not opened); the prediction link lands on the prediction page; the home page and Examples page each carry a link to `bridge/` that resolves.
- Not done: light scheme at both widths (the page persisted dark; the colour-scheme emulation did not switch the site theme), the real paper's anchors, a screenshot file (screenshots were viewed in the pane; the pane tool does not save them).

## Findings the PM or driver should see

1. The supervisor's scope says "Theorem 7" for the route back to attribute units; in the paper L7 is the elasticities and L9 is the pull-back to attributes. The page cites the pull-back theorem and the chart theorem by label.
2. Section 9 (not to be edited here) says "Beyond the analyst's K, selection rules": there, rules for choosing K. With the glossary's new entry, and Section 7 now defining the term, that sentence reads as the new term. A one-word fix (for example "K selection rules" or "rules for choosing K") belongs to a later unit that may edit Section 9.
3. On the data of record, two of the three committed proposals are the same configuration (two holes had one pooled configuration nearest), and all three fail the depth-of-discharge condition; the spike reports it, the page states it, `tests/test_bridge_page.py` pins both.
4. The three selection rules tie on reach (zero targets within the band 1/tau; three within the proposer's reach), so the scope's default ("the rule that reaches its target within the band most often") does not decide. The readout puts it to the supervisor as plain options.
5. Tests amended, each by the scope's own deliverable: `tests/test_site.py` (navigation list, word budgets, total 8,053 from 7,237), `work-packages/interface-contract.toml` and `.md` (the docs page lists and WP8a's paths), `tests/test_paper.py` (Section 7's upper bound 250 to 300 words, for the approved naming paragraph); `tests/test_bridge_page.py` added. The glossary's three entries change the compiled Appendix A register, so its committed output cell (`tab-A-register` of `paper/supporting_material.ipynb`) was regenerated, three rows added and nothing else.
6. `paper/length_ledger.toml` is appended at its end, as `paperfix3` likely also does; the rebase may need that one trivial merge.

## Open for the fresh-reader pass

A reader with no briefing opens `docs/bridge.md` (or `/docs/bridge/` staged) and states the sampled route and the conjecture route apart and names the three outcomes without being told. Not yet run.
