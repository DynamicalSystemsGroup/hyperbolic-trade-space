# WP31 — Decisions (choosing K in the documentation)

The supervisor's words are quoted verbatim where they bind; the driver's calls are listed for his review at the PR.

## Origin

The supervisor, 2026-11-10, verbatim in `driver-log.md` ("Choosing K in the documentation").

## Stage (2), the driver (2026-11-10, 23:30; readout `WP31-readout.md` at 8386f44, 18c258c)

- **Placement A: a new user-guide page "Choosing K"**, between Fitting and Tensions, by a contract amendment adding it
  to `docs.pages`; the fitting page's "Choosing K, the temperature and the band" section shrinks to a pointer (net
  negative there). The question is one a user asks on its own, and the supervisor asked for methods and examples both.
- **The page's content, from the readout:** methods first, each with what it can and cannot do: the mean slack at one
  fixed temperature (falls with K by construction, so it never chooses alone; an elbow where there is one, as the
  stock regime at K = 3, and none where there is not, as the primary regime); the planted-recovery check as the
  method's own test (terms found at K0, extra terms spurious); the resampling splinter check with its noise stated
  (it jumps past K0 on planted tables and is noisy on the cubesat); the certificate and the term share as readings
  of a fit, not selectors; what large K does on our data (from the sweep: the per-term cells thin, the stable radius
  shrinks, the n-lemmas fragment), stated from the sweep and the lemmas, not by analogy. Then two worked examples:
  a planted table (K0 = 2 and 3) and the cubesat, both regimes. The PCA elbow heuristic named once as kin, with the
  sentence that our large-K limit differs and how. No held-out criterion is claimed, since none exists in the package.
- **The 0.31 sentence** on the fitting page does not reproduce (0.55 with fresh draws): the first unit replaces it
  with what the check shows across seeds (the spread stated, or the number dropped), a narrowing that lands before
  the page; the page then carries the re-measured statement with its seeds.
- Stage (4): three task readers ("choose K for this table and say why") on the staged page; stages (5) and (6) as
  usual; the glossary, the register and the ledger follow.

**Driver, verbatim:** "WP31 stage 2: placement A, the fitting section to a pointer, the 0.31 sentence corrected first,
the page built from the readout's methods with their limits stated and two worked examples; the elbow named once."

**Page review (e5d7c7b), the driver (2026-11-11, 02:05):** G-1, G-3 and G-4 fixes as dispatched (the K = 1 claims
narrowed to K >= 2; the sentence that the package has no held-out criterion; register rows for the method statements
and the glossary's "mean slack cannot choose K" made consistent with the page). G-2: the driver's stage-2 line said the
large-K limit shows "the stable radius shrinks, the n-lemmas fragment"; the readout's sweep shows no radius trend, so
the page rightly omits both; the driver's line was wrong on the data and is withdrawn; the page says what the sweep
shows and nothing more.

**Task readers (c8909e7), the driver (2026-11-11, 02:30):** the two planted readers chose K0 and the cubesat reader
said what the page says (no break), with every number reproduced; the page does its job. Before acceptance the four
defects the readers found are fixed as one unit: (1) a temperature recipe for the reader's own table using the
package's own `select_temperature` (the case helper is not installable), with the statement that the K comparison
holds the temperature fixed at the one selected at K = 1; (2) glosses or glossary links on the page for slack, the
band, the cell and the certificate radius, with a scale for "thin"; (3) the `sweep` helper's assertion removed (a
page example does not assert on a borderline number); (4) the repository-root note beside the `sys.path` line. The
three returns are committed verbatim (the readers are resumed to write them to files) beside the triage, as every
reader round's are; the rebuilt page is photographed by the reviewer to files, light and dark, and the driver's own
pass follows. Then acceptance and the changelog line.

**Task-reader fixes (unit wp31fix), implementer's record:** the four defects fixed on `docs/user-guide/choosing-k.md`.
(1) Recipe: `select_temperature(M, 0.10, bounds=(3, 1000))`, run on a planted table (returns 50.0; 26.5 and 38.1 on the
other two planted tables, which the page keeps at tau = 50, so no stated number changed) and equal to the case helper's
K = 1 temperature on the cubesat (38.096 primary, 45.679 stock). (2) Glosses for the mean slack, the near-frontier
band, the cell and the stable radius (glossary wording); "thin" is read against 1/K, with no threshold claimed.
(3) The sweep helper's assertions removed. (4) The repository-root note. The page's prose budget (707 words, tests/test_site.py)
held, so the additions were paid for by deletions: the `conditioning_` bullet (a check that compares metrics within a fit,
nothing about K; C431 dropped), the sentence restating the sweeps at large K (C439 dropped; the printed sweeps show it),
the closing sentence of the large-K section (repeated the methods), and the clause on the mean slack's continued fall
in the planted paragraph. C451 merged into C430.

## Acceptance (2026-11-11, 02:55; at 1d26560)

The four reader defects are fixed (378e8c6) with the page's budget held by four deletions, each recorded; the three
readers' returns are in the record verbatim (`WP31-task-readers/`); a fresh reviewer photographed the page at 1280
and 375 pixels, light and dark, to files, and found no defect; the driver's own pass in his browser tab: the page
opens with what the methods can and cannot say, the temperature recipe stands before the first block that needs it,
the helpers carry no assertion, the two worked examples follow, and the closing section names the PCA elbow once and
says where the analogy stops ("K has no ceiling and the mean slack no floor"); no horizontal scroll at the pane's
width. The supervisor's three asks are met: methods and examples both, the question answered for a user, the elbow
named without being leaned on.

**Driver, verbatim:** "WP31 accepted at 1d26560; the changelog line follows."
