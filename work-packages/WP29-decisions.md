# WP29 — Decisions

Approvals and acceptances are the driver's under the mandate; the supervisor's words are quoted verbatim where they bind.

## Scope gate (2026-11-10, 23:20; scope `WP29-scope-of-work.md` at 35668e5; Track A, the noise result)

Origin: the supervisor on Proposition 2 (`WP28-decisions.md`, S-9, verbatim there). Stage (2) taken by the driver
(`driver-log.md`, "Track A stage (2)"): build A3 and A1.

- **OD1 (a).** The proposal file with the two statements, their sketches and one cubesat table, as one short read the
  driver puts to the supervisor in the morning.
- **OD2 (b).** Until his word, `dev` carries nothing of Track A: the lemma scripts, tests and the Appendix B
  regeneration stay on a branch `wp29`; one push lands them with the placement after his glance. Appendix B is the
  paper's, so a new lemma in it is his to see first.
- **OD3 (a), falling back to (b).** Open the entropic-risk source in full by another route (the publisher's page, a
  preprint); if it cannot be opened, no citation: the sentence is a derivation from L6 and says so.
- **OD4 (a).** The injection script moves to `examples/adcs/` with the case's experiments; its table goes to
  Appendix D at placement, with the sentence that the data of record carry no noise and the noise is injected.
- The Agent's defaults approved as one item.

**Driver, verbatim:** "WP29 approved with OD1 (a), OD2 (b), OD3 (a) falling back to (b), OD4 (a). Stages 3 and 4 run
on the branch now; nothing reaches dev before the supervisor's glance."

## The supervisor's glance (2026-11-11, 09:30; the placement proposal in his pane)

Asked whether the two lemmas go into the paper as proposed, he answered, verbatim: "explain to me why/how this
advances the papers core thesis. and if its just lemmas will be clear to the reader what the result this actually
builds to is? a theorem of a corollary of an existing theorem that accounts for noise. I really want to make sure
we're not inventing results just to have results." The driver's assessment: L18 and L19 are honest corollaries about
the offset, not the exponents the thesis reads; alone they are results for their own sake; the piece that touches the
thesis is the held candidate A2 (noise on the metrics is a ridge on the exponents; the first-order bias is governed by
the restricted Hessian's smallest eigenvalue, the conditioning diagnostic) combined with L18's conditioning map, as
one corollary of Proposition 2 and Theorem 3. Asked for the arc in simple terms, he said, verbatim: "leaning toward
adding corollary. explain in simple terms what the narrative arc of the mathematical results becomes." After the
arc (the fifth beat: how sharp the rates are), verbatim: "okay this sounds like a good addition."

**Disposition (the driver):** WP29's stage (2) is revised. Build: one corollary, after Proposition 2 and Theorem 3,
stating to first order under an interior-solution and small-noise hypothesis that Gaussian noise on the conditioned
metrics shifts the fitted exponents by delta = -sigma^2 (P C P)^+ P w (the ridge toward uniform exponents), with the
noise entering as the attribute's relative measurement error over its log spread (L18's map), so the shift is large
where `conditioning_` is small; L18 stays as its supporting lemma; L19 stays in Appendix B only (no box); the cubesat
injection table is the corollary's demonstration in Appendix D, stated as injected noise on noise-free data of record;
the gap readings G-3, G-11, G-12 revised; the main-results list gains one clause only if the paper stream shows it
earns its place. Order: the derivation (a lemma script with tagged steps for the ridge identity and the first-order
bias; the proof map), the tests on planted data and the check against the spike's numbers, then the box and the
prose; nothing on dev before the derivation passes stage (4). The driver's two statements of what it must not claim
stand: not that the rates are right, only how far noise of a given size moves them; first order, interior solution,
small noise.

## Placement (2026-11-11, 10:10; the assistant, on the branch at 33c1d07)

Stage (4) passed: L20 (51 tagged steps), the proof map at 20 files and 493 steps, the chain, `tests/test_noise_ridge.py`
28 passed (the first-order formula within 3e-4 of the ridge minimiser in nine cells). The corollary is placed between
`res-L6` and `res-L7` as `cor-noise-ridge`, stated with the four refinements the derivation found: the shift is a
statement about the exponents' displacement (its norm), an upper bound in which the temperature reappears (at most
tau times the norm of P Sigma w over `conditioning_`), the projector is the active face's (a boundary exponent breaks
the full-simplex form, tested), and the noisy fit tracks the ridge at small temperature only. It claims neither that
the rates are right, nor consistency, nor a remainder bound, nor anything at a boundary exponent. L19 stays in
Appendix B without a box; the Appendix D injection table is the demonstration, stated as injected noise on noise-free
data; G-3, G-11 and G-12 revised; the main-results list is unchanged. Before landing: the vocabulary tool on the box
text, the glossary's terms for "ridge", "active face" and "tangent space" (entries added where the glossary has
none, Appendix A regenerated), the heading of `app-B-2` as the executor set it. The paper unit lands on dev from the
branch after these, re-executed on the host.

## Stage 6, the P9 and P10 pass (reviews bcb864e, 94a3853, 6140ace; the assistant, 2026-11-11, 11:20)

The triage's dispositions under the balance rule are approved as proposed (C2 to C8 and the section lines:
substitutions and narrowings, detail to Appendix B, the one-clause list entries for A8, A9 and R3, no caveats). On C1,
the one place the claim and not the wording is in question: the script's projector is the sum-zero projector, which is
the active face's tangent space only when every exponent is positive, while the case's fits of record carry zero
exponents. The assistant's call: the corollary is stated for the exponents on the support (the active face) under
strict complementarity (the zero exponents stay zero for small noise), and L20 gains the face step: the same algebra
on the support's coordinates, P the projector onto the support's sum-zero subspace, with a test on a planted fit that
has a zero exponent; D.18's predicted shifts are recomputed with the support's P and compared again with the measured
ones. If the face step is not a page of elementary steps, the box narrows to fits with every exponent positive and
D.18 says it reads the shift within the support. Either way the box carries R3 as the triage words it and nothing is
added for the novice to stumble on. This is a call for the supervisor's review (the review list), since it decides
what the corollary claims at a boundary.

## Acceptance (2026-11-11, 13:05; at 7e7acdd, the review in WP29-review.md)

Stage 6 holds: the P9/P10 narrowings (3f8c49b), the face step (d7ac579: L20.52 to L20.63; the chain and proof map pass
at 505 steps on this Mac; 32 tests), the re-reads (7e7acdd; P10, a P5-type cold read, P9's box-against-script read).
**Assistant, verbatim:** "WP29 accepted. The corollary is stated on the support under strict complementarity, says how
far noise moves the exponents and not whether the rates are right, and its demonstration says the noise is injected."
Two riders, not conditions: the reads2 wording items (conditioned metrics as log-metrics; the fit as the clean fit;
"lowers" first order; A5 in the hypotheses line; Appendix B's quoted lines) land as one narrowing unit before the final
reader round; the Results section's net growth (+201, then narrowed) is recorded in the ledger as the supervisor's
addition and listed for his eye. The assistant's look at the rendered box comes with the next stage rebuild.
