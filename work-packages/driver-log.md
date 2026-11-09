# Driver's log (the autonomous phase)

Kept by the driver (the supervisor's assistant session). Two lists: what is waiting for the
supervisor, and what the driver decided for the PM, with its basis, so the supervisor can audit
those calls at any time. The supervisor's own decisions are quoted in the `WPn-decisions.md` files,
not here. Rules for who answers what: `PM-BRIEF.md`, "The autonomous phase".

## Waiting for the supervisor

Nothing is waiting now. Coming, each prepared as one sitting:

| Item | Package | What he will be asked | Ready when |
|---|---|---|---|
| Second staged-site review | WP8a Amendment 2 | to read the staged site on localhost; then the acceptance question | the restructured docsite passes the driver's checks |
| Acceptance | WP15 | the review's gaps, then the acceptance question | review report, change register and comparison report delivered and verified |
| Structural acceptance | WP10 with Amendment 1 | the review's gaps and the cold-reader reports, then the acceptance question | the paper builds in the container of record and the structural tests pass |
| Merge `dev` to `main` | after WP8a's acceptance | to say go (it runs CI and deploys nothing) | WP8a accepted |
| Data swap | after WP15's acceptance | whether the paper's case moves to the new data, with every changed number listed | WP15 accepted |

## Decided by the driver for the PM

| Date | Question | Decision | Basis |
|---|---|---|---|
| 2026-11-08 | WP15 needs a Z3 executable for the model checks | `z3-solver` added to the `case` group; lock at 5.3.3.0 | the supervisor's recorded role for Z3 in WP15; inside the approved scope; recorded in `WP15-decisions.md` |
| 2026-11-08 | Docsite home page linked the glossary at the wrong path (strict build failed) | routed to the PM to fix | a defect against WP8a Amendment 2's own requirement |
| 2026-11-08 | Docsite limitations page 17 words over its budget | trim the page; do not raise the budget | the budgets were approved with Amendment 2; "i think it can be thinned out" |
| 2026-11-08 | Platform of record for the container | linux/amd64, to match CI | shown to the supervisor in the approval question for WP10 Amendment 1; approved with it |

## Overruled or corrected (kept so the pattern is visible)

| Date | The driver's call | The supervisor's correction |
|---|---|---|
| 2026-11-08 | Described approved Appendix F as the source map | it was the verification audit; corrected in chat and in `WP10-decisions.md` |
| 2026-11-08 | Three kinds of proof step including one argued only in prose | "proof steps that cite an inherited result are still steps ... which still needs to happen in the code" |
| 2026-11-08 | Leave the helper functions in L3's script; move them later | "its a best bet to factor helper tools into their own file" |
| 2026-11-08 | Nine details in one defaults item | "you lumped a lot here" |
