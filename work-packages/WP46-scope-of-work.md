# WP46 — Scope of work: the fit temperature as a path

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP46-decisions.md` |
| **Acceptance record** | The supervisor's acceptance, quoted verbatim, after `WP46-review.md` |

## Purpose

The supervisor's direction (`WP46-decisions.md`, verbatim): the exponent path against the fit temperature is an
interesting and intuitive thing to document, with the tuning of tau and the changes of support at certain
temperatures. The package gives users the figure for their own table, the three readings of it, and the two ends of
the path with their names, one of which needs a lemma step before it is claimed. The paper is unchanged.

## Goals

- G1. **A user can draw the path for their own table:** a plotting helper in the package (the sweep's three panels:
  fraction above V = 1 against the target, effective sample size, the exponent path with the fit temperature marked)
  that takes a conditioned table and a sweep of temperatures, tested on the case and on a planted table.
- G2. **The page tells the path's three readings:** the kink as an active-set change (a metric enters or leaves the
  support at a temperature; the regularization-path analogy named as an analogy); which exponents are robust to the
  temperature and which are not, so the n-lemma's core and margin are read apart; the effective sample size as the
  price, and the 10 percent convention as one point on that trade, with how to move it.
- G3. **The two ends are backed:** the limit at tau to infinity (the supporting hyperplane, Section 5) as it stands;
  the limit at tau to zero stated only after a lemma script derives the second-order term of the log-mean-exp
  (mean plus tau over two times the variance of the scores) and a check on the case shows the tau = 3 fit agrees
  with a direct minimum-variance fit on the simplex to the printed digits; if either fails, the page says the small-tau
  end is a regularity the sweep shows and not a derived limit.
- G4. **The calls are on the page:** the sweep, `select_temperature`, the convention and the helper, in the order a user
  runs them.

## Non-goals

- Any change to the paper; Figure 4's caption already names the drop of total mass and the fit temperature's place.
- A rule that chooses the temperature by the path; the convention stays and the page says why.
- Any claim about phase transitions as physics; the word appears, if at all, as the supervisor's phrase in quotation
  with the active-set change as its meaning.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | A plotting helper in `src/hyperbolic_trade_space/plotting.py` (or beside it) with a numpydoc docstring and a doctest; tests on the case and a planted table | G1 |
| D-2 | `derivation/lemma_21_small_temperature.py` (or the next free number): the cumulant step, the variance limit on centred scores, scripted and verified like the others; its Appendix B entry generated | G3 |
| D-3 | The numeric check on the case: the tau = 3 fit against a direct minimum-variance fit on the simplex, recorded in `work-packages/WP46-rounds/` | G3 |
| D-4 | `docs/user-guide/temperature.md` in the user guide after Fitting, linked from Fitting, Choosing K and the API page; claims rows for every sentence | G2, G4 |
| D-5 | `work-packages/WP46-review.md`: the page read in a browser by one fresh reader with their own sweep run; screenshots held per the WP40 rule | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The helper reproduces Figure 4's lower panel on the case to the printed exponents | a test against D.1's values |
| R-2 | The small-tau sentence appears on the page only if D-2 verifies and D-3 agrees | the review; the claims row cites both |
| R-3 | Every sentence backed or narrowed; the analogy named as one | claims rows; `uv run pytest -q -m "not slow"` |
| R-4 | No file under `paper/` changes | `git diff --stat` |
| R-5 | The page builds, renders without a stderr line, and is reachable from Fitting | `uv run python scripts/stage_site.py`; the browser pass |

## Definition of good

- A user who has fitted their table draws the path, sees which metrics hold and which move, knows what the temperature
  costs in effective sample, and can defend the temperature they chose.

## Definition of good enough

- D-1 to D-5 delivered; R-1 to R-5 pass; the fresh reader names the kink and the price without being told.

## Definition of done

Good enough is met, no open item remains unresolved, and the supervisor has accepted the work by the acceptance record
above.

## Agent's defaults

- The helper's signature mirrors the case's `tau_sweep_lines_figure` and takes the fitted estimator and the table;
  the sweep's default grid is the case's thirteen temperatures *(default)*.
- The page's title is "The fit temperature" *(default)*.
- The unit runs on Sonnet in a worktree; the reader is Haiku *(default)*.

## Open decisions (for the supervisor)

- **OD1.** Place: (a) in the 0.1 candidate (a user-guide page on tuning, not an example); (b) with the 0.2 docs
  content.
