# WP55 — Scope of work: the mathematics builds up (Section 3's fitting problem, Sections 4 to 6)

| | |
|---|---|
| **Status** | DRAFT for the driver's approval as his proxy (autonomous mode, `driver-log.md` 2026-11-15 12:20); executes after WP54 lands, one notebook writer at a time |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `dev`; the unit on a branch `wp55` in its own worktree |
| **Approval record** | The driver's approval under his mandate, quoted in `WP55-decisions.md`, with his directions of 2026-11-15 |
| **Acceptance record** | The driver's soft-confirm of each section on screenshots against `paper-requirements.md`; his read afterwards, quoted in `WP55-decisions.md` |

## Purpose

His direction (`WP55-decisions.md`): the mathematics builds up incrementally, in the conventions of the Boyd lineage
and his own papers, so a reader at calculus, linear algebra and convex optimization follows Section 3's kit into the
definitions, the definitions into the method, the method into the results; familiarity in notation, formatting and
presentation; proofs in the appendix; open questions out of the narrative. The two spike notes
(`WP55-rounds/spike-notation.md`, `WP55-rounds/spike-his-style.md`) supply the conventions; the register
(`paper-requirements.md`) supplies each section's requirements and the rules for all.

## Goals

- G1. **Section 3's fitting problem in the lineage's template.** The displayed, numbered problem `minimize J_τ(w)
  subject to w ∈ Δ, with variable w ∈ R^d`, β named as its optimal value, then the log change of variables; the
  power-law shorthand `m^w = ∏ m_j^{w_j}` fixed where V is defined, with V's type and domain; A1 to A3 stated there
  as assumed throughout, in plain sentences. The rest of Section 3 as he left it.
- G2. **Section 4 reads from the kit.** Each definition prose first, then the formal statement, one term per
  sentence; the n-lemma definition split into the object (the contending set names it) and the reading, with the
  three thresholds and the solver's tie-breaking moved to Methods; no definition refers forward; the K-term model
  bridged to the GP tutorial's `c_k = e^{-κβ_k}, a_k = κ w_k` in one sentence.
- G3. **Section 5 states the method as his papers state a problem.** A4 to A11 and R1 to R3 each displayed and
  named in the result that uses them (A1 to A3 in Section 3); the one-term fit as the template of G1 instantiated;
  the several-term alternation as a numbered heuristic with its levels of guarantee named as its certificate; the
  temperature rule; conditioning as stage 2; the estimator's names as the WP42 build left them.
- G4. **Section 6 presents results as his papers do.** Each result "Let … Assume … Then …" with one display, its
  lemma label, "Proof: Appendix B, Lk", then one interpretation paragraph tied to a textbook result cited by theorem
  or section number; the Derived and Hypotheses labels and the Script boxes leave the main text (Appendix B keeps the
  scripts); Q1 to Q4 and every inline open point go to `work-packages/review/open-questions.md`; a limit is stated once
  where it arises.
- G5. **The argument and the mathematics preserved.** Every definition, hypothesis, theorem statement and proof
  pointer before and after in one table; no object changes meaning (β, the loss, Δ, the temperatures); no lemma
  script, proof map entry or register backing changes; each section's soft-confirm names its central claim, evidence
  and hand-off.
- G6. **Judged as rendered.** Screenshots of each section at desktop width at the three first depths (the figure,
  the figure with caption, figure with caption and prose) for Figure 3 (the n-lemma) and of each text section, in
  `WP55-rounds/`, before the driver's soft-confirm.

## Non-goals

- Sections 1, 2, 7 to 11 and the appendices (WP54, WP56, WP57). Any new result or any change to a lemma script,
  the proof map or the derivation chain. Re-lettering. The symbol table of the notation spike's recommendation 9 is
  built only if the screenshot of Section 3 shows it earns its place (an agent's default below).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `paper/paper.ipynb` with Section 3's fitting problem, Sections 4, 5 and 6 reworked; notebooks re-executed | G1 to G4 |
| D-2 | `WP55-review.md`: the before-and-after table of definitions, hypotheses, theorems and proof pointers; the central claim, evidence and hand-off of each section; the checks | G5 |
| D-3 | `work-packages/review/open-questions.md` extended with every open point removed, each with its section of origin and its record | G4 |
| D-4 | Register rows, paper tests, the vocabulary baseline and the length ledger following the text; the screenshots in `WP55-rounds/` | G5, G6 |
| D-5 | The branch landed on `dev` by the driver after its soft-confirm, with CI | all |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | No hypothesis or object changes meaning; every theorem keeps its lemma label and gains a proof pointer | the D-2 table, every row "unchanged" or the change named and justified |
| R-2 | No forward reference in Sections 3 to 6 except to equations and to Appendix B proofs | `grep` of `prf:ref` and `numref` targets against the order of labels |
| R-3 | Open points leave the narrative | `grep -i "open\b\|not established\|conjecture"` in Sections 3 to 6 returns only the pointer to the appendix section |
| R-4 | Words: Sections 3 to 6 together not above their count at WP54's head (measured and recorded first); the Derived/Script removal is expected to shrink them | `wc -w` on the cells' prose, before and after, in the review file |
| R-5 | The lemma chain and proof map unchanged | `uv run python derivation/run.py`, `uv run python -m derivation.proofmap`: same 22 lemmas and 549 steps |
| R-6 | The register's rules for every section and for Sections 3 to 6 | the driver's read against `paper-requirements.md` on the screenshots |
| R-7 | Lint, format, lock, residuals, vocabulary, the fast suite, the slow paper tests, CI both platforms | as WP53 |

## Definition of good

A reader with the stated background follows the mathematics from the kit to the results without a forward
reference, meets each result in the form his papers use, and finds the proof where it says it is.

## Definition of good enough

R-1 to R-7 met and recorded; the driver's soft-confirm of each of the four sections on screenshots, naming claim,
evidence and hand-off; his later edits plausibly light.

## Definition of done

Good enough met, no open item, landed on `dev`, his read recorded in `WP55-decisions.md`.

## Open decisions

None for him; the driver decides the defaults below as his proxy.

## Agent's defaults

- Results take his form, "Let … Assume … Then", not the textbook's "Suppose … Then" (his style governs where the
  two lineages differ).
- A1 to A3 stay in Section 3 as assumed throughout; A4 to A11 and R1 to R3 move to the results that use them, each
  displayed and named ("Assumption 4 (log-affine conditioning)").
- The symbol table (symbol, meaning, code name, at most twelve rows) is drafted and kept only if the screenshot of
  Section 3 shows it as a quick start rather than a second Appendix A.
- The several-term alternation is called a heuristic with its certificate the three levels of guarantee already
  proved (descent, the term gap, local optimality with cells fixed).
- One unit (Sonnet) executes after WP54 lands; the driver soft-confirms; a second unit only for returned items.
