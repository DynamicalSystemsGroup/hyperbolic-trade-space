# Triage of the P7 and P8 final reads (the assistant, 2026-11-12 08:00; staged head 8806b0e)

Read as a pair under the balance rule: the body stays minimal, Appendix C carries the detail, the repository the
model; a caveat is never the fix; nothing is added for one reader that disrupts the others. P7 (systems engineer,
flight hardware): interest yes, honesty mostly yes, three residuals. P8 (new-space executive): economics and
verdicts sane, the front of the paper not written for the executive, the decision mechanism present but priced in
bands. The reads are `P7-final.md` and `P8-final.md` in this folder.

## Dispositions

| finding | disposition | where |
|---|---|---|
| P7 N-F1 pointing error is the loop plus the tracker | one clause in C.8's leaves-out paragraph (alignment, roll axis, jitter not modelled); the body unchanged | C.8 |
| P7 N-F2 momentum one slew; what it voids | C.8's momentum clause names what the omission voids (a small-wheel feasibility reading) | C.8 |
| P7 N-F3 launch slot minimum | C.8's exclusion names its effect: fleets of one to three pay the slot, so the low end of the fleet-size axis is underpriced | C.8 |
| P7 N-F5 limits read off the data; the 600 s horizon | the body's six-requirement sentence says the limits are the model's, read from the data's pass fractions, not a mission's (one clause, at the point the reader meets them); C.8 names the 600 s horizon and the saturating PD slew law as choices | Section 8, C.8 |
| P7 N-F4, N-F8, N-F10, N-F12 (margins, load, fault tolerance, one orbit) | already toy-stated in C.8 and the case page; no change | none |
| P7 N-F6 gains as variables; slew law | C.8's gains clause stands; the slew law joins the horizon clause above | C.8 |
| P7 N-F7 rigid wings; N-F9 battery; N-F11 mass a trim on a fixed bus | one item each in C.8's leaves-out list where a sentence does the job (wings, hinge mass; the mass axis a trim on about 10.6 kg of fixed bus); the battery item stays generic | C.8 |
| P7 item 5 (two sentences of C.8 into the body) | narrowed to the one body clause above; the rest stays in C.8 (balance rule) | Section 8 |
| P8 F1 the abstract names no case number or money | the abstract rests for the supervisor's hand (his standing note); the review list carries P8's two-line proposal as a question for him, not an edit | review list |
| P8 F3 requirement prices in bands, not USD | D.17 converts the unit-cost and fleet-cost prices to USD per satellite and per fleet as it converts the mass price to launch USD; the Examples block follows; a test pins the conversion | D.17, Examples |
| P8 F4 the constrained fit's candidates result not in the text | one sentence in D.7 (two hand-named candidates sit beyond the thresholds-met surface; none meets all four); the body only if the sentence test passes there | D.7 |
| P8 F2, F6 no decision shown; adoption cost | WP33: the executive journey's first screen routes to the requirements reading (which requirement is dear, what pre-imposing them changes) and states the adoption cost in three lines (designs needed, who writes the conditioning, time to a first fit); no new paragraph in the body | WP33 |
| P8 F7 gaps said in one place only | the body's "illustrative" sentence carries the three-item gap clause (no schedule, no payload, a flat launch price) in the same clause as P7 N-F5's; the Examples page points at C.8 (it does) | Section 8 |
| P8 F8 dense first screens | WP33's wayfinding read | WP33 |
| P8 F5 soft spots (2,000,000 USD allowance; flat launch price) | toy-stated already; the launch slot clause above covers the second | none |

## Units

1. Paper unit (Sonnet): the Section 8 clause; C.8's clauses and list items; D.17's USD conversion with its test; D.7's
   sentence; notebooks and figure files in one commit; ledger rows net neutral or negative where the sentence test
   allows (the C.8 items earn their words as the hard requirement's honesty statements).
2. WP33 carries P8 F2, F6 and F8 as journey requirements (the executive's first screen), not as paper text.
3. The review list: P8's abstract proposal as a question for the supervisor; this triage's path.

What the reads do not ask for: a model change. Neither reader asks for a re-run; both accept the case as a
demonstration once its reach is stated where the claim is read.
