# WP76 research note: what the Kitchenham-CSC case could test under a conic-expression generalisation

A short note, not public prose (the example page says nothing of this; `WP76-decisions.md`, OD1). It names what the
one real iron-triangle table the examples hold could test if the model family admits expressions beyond the
posynomial, in the vocabulary WP75's readout settles (`wp75-functional-forms.md`, on branch `wp75` at this writing);
it defines no form and proposes no package.

## What the case is, in the family's terms

Three metrics, 141 rows, one monomial frontier (the second term of K = 2 holds no near-frontier project). The
conditioning is the only place an affine expression enters today: the slack share `1 - actual / plan` is negative for
an overrun, and the shift that makes it positive (`share + 10`) is an affine map applied before the log, so the fitted
monomial is a power of an affine function of the recorded attribute. The sensitivity ladder shows what that does: the
exponents move with the shift (schedule slack 0.59 to 0.71 from shift 40 to shift 10) while the signs of the
near-frontier associations do not, and the plan-over-actual rule, which needs no shift, gives the same signs with
different exponents (0.39, 0.21, 0.40).

## Three things the case could test

1. **A level explained twice (the shared-level system).** The two slacks move together near the frontier (+0.43 at
   the rule's band, +0.13 to +0.67 across the scaled rules and bands). Under a system in which several expressions
   equal the same level V, the question the case can put is whether one expression in the two slacks (a shared
   "time-and-money" side) and one in scope explain the level better than the single monomial in all three, and
   whether the shared side's identifiability survives the band ladder and the leave-one-out table, where the slacks'
   association thins to +0.17 and turns negative without one project. A result that depends on project 16 is not
   a result.
2. **An affine side against a posynomial side.** The shift is a confession that the slack share is not a positive
   quantity with a natural zero. A form that takes the slack share itself, unshifted, on an affine side of a
   separable expression (the supervisor's `V = posynomial(x)` and `V = A x`, `notes/directions/candidates.md`) and
   scope on the posynomial side would remove the ladder's shift rungs: the test is whether the exponents stop moving
   when the shift is no longer a choice, and whether the fit stays convex in the parameters (WP75's second column).
3. **A conic in the overrun plane.** In the plane of the two overrun ratios the near-frontier projects lie in a band
   around the diagonal (both under plan by similar shares); in the three scope pairs the cloud is a wedge. Which
   conic section, if any, is a sublevel set that bounds the attainable set in log-metric space is a question the
   case can answer only by comparison against held-out rows at 141 projects, with the subset readings (type P and
   client 2, where the slacks oppose each other) as the first check that the shape is the portfolio's and not the
   form's.

## What the case cannot test

Anything about quality: the table has no quality measure, so no form with 3 + m sides is tested here, and the memo's
boundary stands. A rate of exchange between scope and slack: the exponents move with the conditioning across every
form that keeps a shift. A second term: 141 rows did not carry one.

## What a next release would build, if anything

Nothing from this case alone. If WP75 admits a shared-level or separable form, this table is a cheap first real test
(the data are committed, the model states every rule, the ladders exist), and the pass criterion is already written:
the reading must survive the band ladder, the leave-one-out table and the subsets as the monomial's negative half
does.
