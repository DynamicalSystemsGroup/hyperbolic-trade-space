# Answer key, the demo notebook cold-reader battery (2026-11-19, fixed before any read; readers never see it)

Round 1, notebook at the talk branch head after WP83 amendment 4 (the mathematics section).

## The story's parts (his arc, in order)
1. Motivation: a decision needs an answer and a justification an accountable executive can defend; trade studies are documents with elicited weights.
2. Three layers: decision analysis, machine learning (unsupervised), optimization.
3. The pipeline: configuration c -> evaluate (a black box) -> attributes a -> condition -> metrics m (positive, larger is better) -> identify -> w, beta -> analyse.
4. The mathematics in brief: V a weighted geometric mean; V = 1 the fitted reference surface; the chart (position, level); constant elasticities along a term; the n-lemma (how many metrics contend).
5. The SysML v2 model of a cubesat ADCS case; 6. its configuration diagram (swap wheel class and tracker grade; tune panel span, battery capacity, Kp, Kd; fleet size the seventh variable); 7. its subsystems and requirements diagram (13 traded metrics, MoE vs MoP).
8. Simulations described, not re-run; data of record: 3,000 designs per regime, 2,134 feasible in the primary regime; a ledger records each run.
9. The fit with tradespace (temperature, K = 1 and K = 2).
10. Exploratory analysis for choosing among alternatives: feasibility and requirements; the contending set (7 metrics at K = 1) and the tension; where each term leads; the fleet-size trade (coverage probability against fleet cost; the principals' view grounded in the same model and data); propose, predict, check (proposals fail depth of discharge); the decision (shortlist of 28; manufacturer and operator pick the 25-satellite medium/medium fleet; the sponsor picks 4 small-wheel satellites; the executives' question: how much fleet cost a gain in coverage probability is worth).
11. Closing: V is energy-like (Pareto improvements raise it; a maximizer is weakly Pareto-efficient); the regressor predicts a configuration's chart point and level; the closed loop (search proposes c', evaluate, refit) is a direction, not shipped.

## A reader must NOT come away believing (worst outcome first)
- W1 the method picks the design or makes the decision for the executives;
- W2 the weights or exponents were elicited from stakeholders;
- W3 the closed-loop search or optimizer ships in the package today;
- W4 the simulations were run live, or the data were made up for the talk;
- W5 the fitted reference surface is the Pareto frontier;
- W6 the method claims to be new, or replaces Pareto analysis, PCA or multi-criteria methods;
- W7 a star or marker on a ternary plot is a design;
- W8 the package needs a SysML v2 model or a satellite to be used;
- W9 the case is a validated, real flight program's numbers.

## The talk's constraints (his words, 2026-11-19 ~18:00 EST)
"the notebook should be mostly stand alone but i am going to be presenting it live so we do not need to jam
everything onto the page. i don't want it to feel like a text wall so don't over explain. its currently paced pretty
well. it needs to allow me to tell a story with data and code"
Triage rule from these: a request to add explanation is met by the presenter's voice, not the page, unless a reader
would hold a wrong belief (W1-W9) or lose the thread without a word on the page; pacing is protected.
