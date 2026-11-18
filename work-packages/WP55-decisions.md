
## The three lineages and his own style (2026-11-15, ~12:50 EST)

**Supervisor, verbatim:** "So to be clear we have 3 layers of prior art: * Decision Analysis and design optimization
level we need to look at work OpenMDAO and Alejandro Salado's work. * the machine learning layer where we are
matching style to scikit learn documentation and APIs * the optimization layer where we lean on Boyd. familiarity is
key. Lastly for my own style you can look at my TAC, CDC and transactions on networked systems papers. do not blend,
do not make stuff up, do not metanarrate. build structure, define requirements, define terms, define notation, and
build a structured coherent document which is internally compatible, and grounded in the literature."

**Applied as:** the rule set in `paper-requirements.md` names the three reference lineages by layer (OpenMDAO and
Salado for the decision and design-optimization layer; the scikit-learn documentation and API for the
machine-learning layer; Boyd for the optimization layer) and his own IEEE TAC, CDC and TCNS papers for his style; a
style spike reads his papers before WP55 is scoped; WP56's prework reads OpenMDAO and Salado.

## The two spikes delivered; the scope drafted (13:27 EST)

`WP55-rounds/spike-notation.md` (wp55spike 6291442; Boyd and Vandenberghe, the GP tutorial, Hoburg and Abbeel, Magnani and Boyd, the scikit-learn decomposition page) and `WP55-rounds/spike-his-style.md` (bbec3bc; eight of his papers resolved, three read in full). The scope `WP55-scope-of-work.md` is drafted from them and the register; it executes after WP54 lands. The driver approves it as his proxy when WP54 is landed, recorded here.

## Approval as proxy (16:18 EST)

Approved by the driver under the autonomous mode of 2026-11-15: WP55 executes on wp55 from dev at c98044d (WP54 landed), one unit, the driver soft-confirms each of the four sections on screenshots against `paper-requirements.md`, the lemma scripts and the proof map untouched (R-5).

## Landed (19:13 EST)

Landed on `dev` at 98d9753 after the driver's review on the rendered page (Sections 3, 4 and 6 soft-confirmed at
b87efdd; Section 5 returned with seven revisions and soft-confirmed at 41c04c7: results, ledger pointers and
implementation detail out of Methods, the "Simplifying assumptions" paragraph dissolved, 1,414 to 1,156 words).
Evidence: lint, format, lock, residuals, vocabulary, mkdocs and the proof map (22 files, 549 steps) green; notebooks
re-executed (only Appendix F's checkout hash moved); fast suite 2,085 passed; slow paper tests 27 passed; CI
43778944233 dispatched. His read of Sections 3 to 6 is pending; the register holds their states.
