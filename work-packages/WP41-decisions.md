# WP41 — Decisions: the bridge to the search (from the chart back to the design space)

Verbal approvals and rulings, quoted verbatim, with the assistant's reading of each ("Applied as").

## The gap, the research and its timing (2026-11-14, 12:05 to 12:30)

**Supervisor, verbatim (12:05):** "i think we have one more practical gap. when going from the hyperbolic space back to
the configuration space (the design space), we lose inevitability (as intended). this is only sort of true, if we hav a
point with a datum in the hyperbolic space we can get back to the design that produced it, but if i pick a point in
the resulting space that doesn't have a data point and try to get back to the design space, firstly my proposed design
is merely a conjecture (second i need a rule with which to pick since it wont be unique) and thirdly if actually
construct that design and then run measurements on it (say run a monte carlo experiment) i may learn that i was wrong
(which isn't necessarily bad). the stuff i am describing is the bridge to the search so i don't want you to do anything
crazy with the paper but i do want this to be carefully researched in repo and implemented and we can consider
expanding the paper in a future release. the reason we need to do some of this research now is because its key to the
story of the tool and we need to make sure that even if the exact how is open ended, the overall approach is well posed"

**Applied as:** "inevitability" read as invertibility. The assistant framed the procedure (the forward map loses
invertibility at evaluation only; a proposal is a configuration, a predicted chart point and a tolerance, a conjecture
until checked; a selection rule is named because the preimage is not unique; the check has three informative outcomes,
confirmed, refuted and infeasible; the outer loop is the refit) and proposed a six-stage package with the paper held to
Section 7's names.

**Supervisor, verbatim (12:20), on the outer loop:** recorded in `WP36-decisions.md` (the submartingale conjecture,
future work, no conditions derived; change request 169).

**Assistant's question (12:25):** where the package lands: (1) inside 0.1, all four stages; (2) framing and docs page in
0.1, interface and demonstration in 0.2; (3) all in 0.2, the spike run now.

**Supervisor, verbatim (12:30):** "to answer your question: Framing and docs page in 0.1; interface and demonstration in
0.2."

**Applied as:** WP41 is the 0.1 part: the research spike, the well-posedness note (the framing, the selection rules
named with a default, the outcome set, what stays open), the docs page that tells the story, and Section 7's one
paragraph naming the procedure with no new claim. The package interface and the case demonstration with a Monte Carlo
check are the first package of 0.2, scoped from the note. `WP41-scope-of-work.md` holds the scope; its approval is the
supervisor's verbal word, quoted here when given.

## Approval (2026-11-14, 15:40)

**Supervisor, verbatim:** "i approve the Work Packages above. we can return to the open wording discussions"

**Applied as:** the scope as drafted is approved (WP41, WP43 and WP45 were the three listed; WP42 waits on its open
decision, the solver's word). Execution begins under `work-execution`: a unit per package in its own worktree on
Sonnet, in the background, with the scope file as the brief; the assistant verifies each delivery before the
supervisor's acceptance.

## The method's intent, in the supervisor's words (2026-11-14, 16:35)

**Supervisor, verbatim:** "so the intuition for my method is to make a patchwork of weighted product terms that
parameterize the (near) frontier in high dimensional space so we can look in the data to see if there are areas that
are devoid of data we might want to fill in (space filling). here holes would be places the fit had something to say
but the data does not, so if possible we should get some data. i also want to know at any give point (or region) of
our (approximate) frontier which competing objectives are binding, and through chain rule, partials and pull backs what
metrics and what configuration dimensions are most relevant. I also want the ability to ask questions about what moving
up the energy levels (past the frontier) looks like, and to be able to reason about that in terms gradients on the my
fit surface so i can pull back into config space and search for new configurations that might move us upward"

**Applied as:** the statement of intent the docs' "User guide: start here" page and the glossary's preamble carry (in
WP42's build); each clause maps to an object and a package: the patchwork of terms and the chart (built); holes in the
chart as places the fit speaks and the data do not (built, D.10's holes; the proposal rule in WP41); the binding
objectives at a point or region (the contending set, built; the tension matrix and a design's tensions, WP42); the
pull-back to attribute units (Theorem 7, built) and to configuration dimensions through the surrogate's Jacobian (the
chain rule from a tension or the ascent direction through the regressor: WP41 part 2, 0.2, a conjecture until checked);
moving past the frontier as the ascent direction w on the fit surface, pulled back through the surrogate into
configuration space as the search's step (Section 7; WP41 part 2), with the submartingale conjecture as its open item.
