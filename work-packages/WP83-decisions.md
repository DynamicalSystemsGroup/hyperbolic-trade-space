# WP83 decisions (the demo notebook for the OpenMBEE presentation, 2026-11-20)

His words, verbatim, 2026-11-19 (EST, about), in the order given:

- (about 12:00) "i also need a separate scope of work which will go on its own branch. this scope is a jupyter notebook for a presentation // demo. the story arc of the demo is as follows:" followed by his ten items: "motivation"; "3 layers: decision analysis, ML, optimization"; "the pipeline diagram"; "the sysml v2 model (use the ADCS example)"; "show the configuration diagram"; "show the subsystems / requirements diagram"; "describe the simulations but pull the data from already run simulations don't rerun then"; "run the pipeline fit using tradespace"; "then do some exploratory data analysis"; "make sure the exploratory data analysis is clearly aligned to assessing alternative and justifying decisions"; "end on the relationship of this package to closed loop design space searching (comment on the role of a surrogate function that is energy-like for searching and optimizing over the design space."
- Asked "Is the demo notebook for tomorrow's OpenMBEE presentation?": "Yes, for tomorrow".
- "a lot of what you need already exists. i view this as curation and narration, not new build"
- Asked "After tomorrow, what happens to the demo notebook's branch?": "stays its own branch for now. i can reassess later. i don't want extra requirements for merging to dev getting in the way of getting my notebook ready for the presentation"
- "the paper's case and case analysis likely provides a lot of the scaffolding you need for this presentation"
- Asked whether the branch goes up to GitHub, given the governance pull request's branch rule: "Pushed, rule widened" (the rule's `talk/*` class rides in WP82 amendment 4, #16).
- Asked to approve the scope with its defaults to start the build: first "Show me the scope first", then, having read it: "Approve, build tonight".

**Applied as.** The scope `WP83-scope-of-work.md` approved as drafted, its Agent's defaults included; the build runs
tonight through the PM (one worker, one fresh-context reviewer); the driver verifies and pushes the branch
`talk/openmbee-2026-11-20` once.
