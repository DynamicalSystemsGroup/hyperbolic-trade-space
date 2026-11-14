# WP44 — Decisions: a second case study from a public dataset (a research spike)

## The direction (2026-11-14, 14:05)

**Supervisor, verbatim:** "another spike i want that is not aimed at the paper but instead at the package and the
examples, i want you to hunt through the internet for datasets that would make a great case study that is independent
of the synthetic satellite. something from natural sciences could be good. we just need configurations and measured
attributes where the underlying phenomena of interest includes trade-offs. again this not targeting the paper but
instead helping us build support for our claims and also provide examples to help people using the tool."

**Applied as:** WP44 is a research spike: a hunt for public datasets with configurations (controllable or categorical
inputs) and several measured attributes whose phenomenon includes trade-offs, natural sciences preferred; each
candidate with its licence, a stable source (DOI or archival URL, the repository's rule for references), size, the
configuration and attribute columns, the trade-off the literature names, and how it maps to the pipeline
(configuration, attributes, conditioning into metrics). The readout ranks the candidates against the criteria and
gives plain options for the one or two to build as documentation examples in a later package; nothing enters the paper.
`WP44-scope-of-work.md` holds the scope; the hunt itself is read-only and starts at once; the build of an example waits
on the supervisor's choice from the readout.

## The readout, and a low-dimensional example added (2026-11-14, 14:50)

The readout (`WP44-rounds/hunt/readout.md`, b332787) ranks the perovskite devices and the amniote life histories
first, with the leaf traits and the battery ageing set behind, and offers four build options.

**Supervisor, verbatim:** "i am okay with doing a low dimensional example ALSO. it doesn't satisfy the request of this
spike but we can do "Rothamsted's wheat yields" as a low dimensional example to help build inuition if the data is
otherwise good and the story is clear"

**Applied as:** Rothamsted's Broadbalk wheat yields (e-RA, doi:10.23637/rbk1-yld6822-01, CC BY 4.0; treatments and
cultivar as configuration; grain and straw yield as the two attributes) is added to the readout as a two-metric
example for intuition, conditional on two checks the assistant runs before it is built: the data's columns, rows and
licence read from the archive, and a clear story with a citation (the harvest index: grain rose and straw fell across
cultivars, so the two trade along the biomass frontier). The spike's own choice among the four options stays open.

## The choice (2026-11-14, 14:55)

**Supervisor, verbatim:** "you can also do both cases proposed: The Perovskite Database Project and The Amniote
life-history database"

**Applied as:** option 1 of the readout. The build is scoped as WP45 (two Examples pages with fetch-at-build steps,
conditioning rules stated, the fits at K = 1 and 2, the tension matrix once WP42 lands; the Broadbalk wheat example as
the two-metric page if its two checks hold); its place in 0.1 or after is the one open decision of that scope.

## The purpose, in the supervisor's words (2026-11-14, 15:00)

**Supervisor, verbatim:** "the point here is to truly show the method works, for that we need a variety of unrelated
cases." And: "this will do double duty by populating an examples section of the documentation and help us harden our
understanding of our own method"

**Applied as:** WP45's purpose is the demonstration: unrelated cases (in domain, in who made the data, in dimension, in
whether a designer exists), each a known-answer test against the field's named trade-off, reported whether the fit
names it or not; the Examples section of the docs is the second duty. The leaf-trait and battery tables stay on the
candidates list as the next two domains.

**The wheat checks (15:10):** both conditions hold with two stated limits (the straw-recorded subset; a manual fetch
behind a form, the derived table committed under CC BY with attribution); the story is Austin et al. 1980
(doi:10.1017/S0021859600028665) and Austin et al. 1993 on Broadbalk itself (doi:10.1016/S1161-0301(14)80144-5).
Recorded in the readout; the page is WP45's G4.

**Supervisor, verbatim (15:15):** "these are two different requirements so don't confuse readers to convince us. think
in terms of work you do to test our method and then draw a didactic story from that work for the user"

**Applied as:** WP45 separates the two: for each case, first a test record in `work-packages/WP45-rounds/<case>/`
(the expected n-lemma written from the literature before the fit, the fit, pass or fail, the sensitivity to
conditioning and temperature, the row counts and the limits), which is the work that hardens the method and is reported
whether it passes or not; then the docs page, drawn from that record as a didactic story for a user with their own
table (what the data are, how to condition, how to fit, how to read), with none of the test record's apparatus on the
page and no sentence written to convince. The page cites the record for a reader who wants it.

**Supervisor, verbatim (15:25), on WP45's place:** "i want the research and testing our method part of the work to land
before 0.1 to help us make sure we didn't miss something or get something wrong but extending examples in documentation
site 0.2 content"

**Applied as:** WP45 splits by that line: the test records for the three cases (D-0: the fetches, the conditioning
rules, the fits, the known-answer verdicts, the sensitivities, the limits) land in the 0.1 candidate as research under
`work-packages/WP45-rounds/`, with their scripts under `examples/` so the fits are reproducible; the docs pages (D-2)
and their fresh-reader review (D-4) are 0.2's first package, drawn from the records. OD1 is closed.

## Approval (2026-11-14, 15:40)

**Supervisor, verbatim:** "i approve the Work Packages above. we can return to the open wording discussions"

**Applied as:** the scope as drafted is approved (WP41, WP43 and WP45 were the three listed; WP42 waits on its open
decision, the solver's word). Execution begins under `work-execution`: a unit per package in its own worktree on
Sonnet, in the background, with the scope file as the brief; the assistant verifies each delivery before the
supervisor's acceptance.

## The breadth of the examples (2026-11-14, 20:00; an intent, not a build item)

**Supervisor, verbatim:** "there is a different track of feedback that i got distracted from giving. when we are building out the examples we want
to make sure we're showing the breadth of the model, that means some examples that are high dimensional (number attributes,
number of metrics, number of objectives can all vary), some are low dimensional, some end up with larger K number of
posynomial terms and some are fewer posynomial terms. some will be tight fits and some will be softer. some are real world
measured cases and some are simulation based on models. we also expect real world engineering problems to have data from
different engineering lifecycle stages from research to design to quality control to configuration management to end of
life. this will mean there is a rich mix of data produced by different measurement methods synthetic and actual"

**Supervisor, verbatim:** "i am not exactly sure how this will fit into the build out but it fit with my broader effort to help capture my intents as
we establish this first release as an initial condition"

**Applied as:** an intent record, `work-packages/examples-coverage.md`: the axes he names (dimension in attributes,
metrics and objectives; the number of terms K; tight or soft fit; measured or simulated; the engineering lifecycle stage
from research to end of life; the measurement method, synthetic or actual), the current and candidate cases placed on
them from what is known today, and the gaps. It changes no scope. Each WP45 test record states its case's row (the
counts, the K and temperature found, the data's origin, the stage, the method) so the matrix fills from the records,
and v0.2's example pages are chosen with the gaps in view. The cubesat remains the paper's one demonstrator.

