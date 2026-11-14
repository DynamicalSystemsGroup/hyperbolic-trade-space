# WP11-final: the final reader round

Reports are committed byte for byte as they were written, before anyone reads them (R-3). Triage is held by the
assistant against the answer key (version 5, hash in `WP11-decisions.md`); no triage is in this directory.

- **Stage head read:** `c23cf60` (dev). The stage is `scripts/stage_site.py` output served on http://127.0.0.1:8791.
- **Slices:** captured at that head from the rendered pages; the list with byte sizes and sha256 is
  `slices-manifest.tsv`. Readers saw them through the alias directory `material/`; reports went to `returns/`.
  8 figures and 2 tables; depth-B statements file holds 28 statements, no proofs.
- **Briefs:** `briefs/` (F = first wording, G = second wording, H = root-page arrival). Placeholders are substituted.
- **Slots:** `slots.tsv` gives cell, wording, model label, held-out mark and wave. Label m1 ran on Sonnet, m2 on Haiku.
  Held-out slots (F01, F10, F15, F17, F18, F23 and their G twins) are read last, after triage and landings.
- **Waves:** seven reads each, launched only when the previous wave's reports existed; at most four browser readers
  per wave, each in its own tab.

## Wave 1 (F03 G14 G26 G08 F25 G27 F11)

Reports in `reports/`. Model per slot as in `slots.tsv`.

Harness incidents: none observed in the reports' first two lines (all seven carry the required head line). One reader's
tool log showed a call to a session hand-off tool (it cannot be attributed to one slot from the log); nothing came of it.

## Wave 2 (G02 F19 H01 F12 H02 F04 G21)

Harness incident: the reader of H02 returned its whole report as its final message instead of the three-line message
(the file itself is in `reports/` and was committed as written). The PM saw that text in the hand-back and did not
triage it.

## Wave 3 (G20 G04 F09 F02 F26 F13 G24)

Stage head read: c23cf60 (unchanged). Harness incidents: none observed.

## Waves 4 to 7 (reports committed by the assistant: b6f9b76, bc5e724 and later; triage in `triage/wave-4.md` to `wave-7.md`)

Wave 4: F06 F21 F08 F20 F05 G22 G03. Wave 5: F22 G25 G05 F16 F14 G06 F28. Wave 6: F27 F24 G12 G28 G11 F07 G16.
Wave 7: G07 G19 G09 G13. All read the stage at c23cf60 as captured (the round compares one head); the change units that
landed meanwhile (c42d860 and later) were not seen by these readers. Held-out cells (F01 F10 F15 F17 F18 F23 and their
G twins) are read later on the landed head, with slices recaptured and briefs re-rendered, in two waves of six.

Harness incidents: the H02 note above stands. A "Loading" output on first extraction for six readers; Appendix D.15
did not render once for G25; the captured first screen's collapsed contents chevron for G16.
