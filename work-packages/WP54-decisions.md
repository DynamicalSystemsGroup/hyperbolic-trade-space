# WP54 — Decisions: the paper's skeleton

## Approval and direction (2026-11-15)

**Supervisor, verbatim (direction, ~11:30 EST):** ""search of the design space preliminary" belongs in the future work
section. not its own section. the future work section can be just called future work not "future work and final
remark" Reproducibility and your own case can be pruned and what needs to be kept can be integrated into the
acknowledgements and process section. that section should be renamed AI acknowledgement and Reproducibility. it should
cover both that we did and did not use AI as well as how the results can be reproduced and adapted. do not make this
section long, do not make this section verbose or metanarration. its purely informational: what we did, how we did it
and how you can reproduce it."

**Supervisor, verbatim (approval, ~11:45 EST):** "approve 53 and 54."

**Supervisor, verbatim (Future work and the discussion, ~11:55 EST):** "The discussion is not just about the case. It
needs to address the value prop put forth in the abtract and section 1. likely revisit the 3 layers we described in
section 2. it then needs to lead into the future work section where we have to cover the 3 directions named in the
abstract. the future work section should not be long. it should clearly state what we accomplished."

## Landed (16:17 EST)

e435e4a on dev after the driver's read of the two new sections and the roadmap on the rendered paper and against the register: Future work 233 words (what the release delivered first, then the three directions in the abstract's order, each from its record, the Final remark cut), AI acknowledgement and Reproducibility 150 words (informational, scripted checks, no machine-checked), eleven numbered sections and Works cited, every reference to the old sections retargeted, the open points in `work-packages/review/open-questions.md` (OQ-1 to OQ-4). Checks on the rebased tree: lint, format and attribution clean; paper, register, site and docs tests 339 passed; the unit's fast suite 2,085 and slow paper tests 27 passed. Left for WP62: `docs/superpowers/notes/user-journeys.md` still cites the old section numbers; a duplicate `fig-tension-matrix` identifier warning in the MyST build predates this package (WP56). His read remains.
