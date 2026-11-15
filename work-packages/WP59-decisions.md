# WP59 — Decisions: conditioning and feature engineering on the three public cases

## Direction (2026-11-15, ~13:10 EST)

The driver walked him through WP45's three test records (perovskite, amniote, Broadbalk wheat: all passed their
pre-stated n-lemma; soft fits; the exponents unstable on the wide table; the orientation of a time cost decides the
lemma; a grain ceiling at K = 2) and proposed building their documentation pages in 0.1.

**Supervisor, verbatim:** "before we build pages for them. i'd like you to use these cases to further examine the
conditioning step, and explore the impact of feature engineering work, or chaining with other unsupervised ML methods.
the wide table for example could get something like a PCA before our method. i don't know if it will help but we're
trying to show that this is comparable to other data science work. on the one hand its a highly reproducible
procedure, on the other hand, how the data represents the problem matters. conditioning sensitivity is not a surprise
to a seasoned ML engineer, but most decision analysts are not seasoned ML engineers so building out these examples with
guidance about what was done why is valuable"

**Earlier the same sitting, verbatim (on WP57):** "i want to note that the appendices package was a bit too big so you
probably need to plan for another layer of work packages for each appendix based on what you find."

**Recorded as:** a research spike on the three cases before any page (conditioning and feature-engineering variants,
chaining with other unsupervised methods, the fit's reading under each, written up as guidance for a decision analyst:
what was done and why); the pages follow from its readout. WP57 becomes a planning package that spawns one package
per appendix or group from what it reads.

**Supervisor, verbatim (approval of the spike as described in chat, 2026-11-15 ~13:20 EST):** "ok"

## Amendment from the metamanager's feedback (2026-11-15 afternoon)

PCA scores made positive and oriented are a change of representation, reported with an explicit interpretation of
each component; a positive leading loading does not make a larger score preferable to a stakeholder. The readout
says so where it reports the chain, and keeps every conditioning result that weakens the preferred reading.

## Acceptance (13:02 EST)

Accepted by the driver under the mandate after its own read: the reviewer's reruns from a clean cache matched byte for byte, the primary rows reproduce the WP45 records, the four readout defects the review found were fixed by the driver, and the readout reads as guidance an analyst can act on. Landed on dev at a9cfb60. His read remains; the pages (WP60) are scoped from the readout.

**Supervisor, verbatim (on the readout, 13:18 EST):** "seems like a fine plan. my main takeaway is that "bigger is better" is a normative judgement which is why the feature engineering and conditioning have to be part of using the method, rather than predefined by the method itself"

**Recorded as the thesis of the WP60 pages and of the conditioning guidance:** the orientation of each metric is a normative judgement the analyst makes and states; the method takes it as given and tests whether it mattered. The readout's orientation section and the amniote page open on it.
