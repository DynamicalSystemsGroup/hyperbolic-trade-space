# WP56 spike: how the decision-analysis and design-optimization lineage writes up a case

## Sources resolved

1. Gray, Hwang, Martins, Moore, Naylor (2019), "OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization", *Struct. Multidisc. Optim.* 59, 1075-1104, doi:10.1007/s00158-019-02211-z. Read in full (MDO Lab preprint).
2. OpenMDAO documentation, "Sellar" and "First optimization" pages, openmdao.org/newdocs. Read in full. Also the paper's Sec. 7 (applications, including the CADRE cubesat).
3. Martins and Lambe (2013), "Multidisciplinary design optimization: a survey of architectures", *AIAA J.* 51(9), 2049-2075, doi:10.2514/1.J051895. Read in full (preprint, websites.umich.edu/~mdolaboratory/pdf/Martins2013.pdf).
4. Salado, "A systems-theoretic articulation of stakeholder needs and system requirements", *Systems Engineering* 24(2), 2021, doi:10.1002/sys.21568; Salado and Kannan, "Elemental patterns of verification strategies", *Syst. Eng.* 22(5), 2019, doi:10.1002/sys.21481; Salado, Nilchiani, Verma, "Solution spaces and requirements", *J. Syst. Sci. Syst. Eng.* 2016, doi:10.1007/s11518-016-5315-3; Salado and Shadab, *Syst. Eng.* 2023, doi:10.1002/sys.21738; "Efficient population of the verification tradespace using Bayesian inference", *IEEE Syst. J.* 2020, doi:10.1109/JSYST.2019.2932916. Abstracts only (Semantic Scholar, Crossref); every full text is paywalled or 403.

## Conventions observed

**Model to decision.** OpenMDAO runs one toy model through the whole paper (Sec. 3.2, equations 1-3, a design structure matrix, then the run script) so every later idea has a concrete referent; the decision is the optimizer's output, with objective, constraints and design variables printed beside it. Applications get a table of XDSM, design variables, objective and constraints, and "we present an overview of these applications". Salado's abstracts describe a definitional chain (needs, requirements, solution space) illustrated by worked examples that show elicitation, derivation and decomposition step by step.

**Problem definition.** Always a fixed triple: minimize objective, with respect to design variables, subject to constraints, in one notation reused for every case (the survey's whole contribution). Salado: requirements bound the solution space; needs live in the problem space. 

**Configuration and provenance.** The framework paper ends with "Replication of Results": what is open (GitHub, openmdao.org), which figures' scripts are supplemental, and which result cannot be reproduced (non-open code), said once. 

**Figures and captions.** The XDSM carries structure: data on thick grey lines, process on thin black ones, numbers for execution order, components on the diagonal; the survey explains the notation once on two small examples, then every figure reuses it with a one-line caption ("XDSM for the AAO problem"). Application papers use one XDSM per case.

**Limits.** Stated once, at the end: the survey's benchmarking section lists three limitations of the literature; the framework paper's conclusion gives one sentence of scope (best when models are built inside the framework).

**Close.** A short conclusions section restating what was shown, then open work.

Salado's abstracts promise "better formulation of requirements" and test it by experiment.

## What the paper's case sections do differently

- "Our case is a cubesat model" begins with the model's variables in one long paragraph, with no objective-and-constraints statement; OpenMDAO and the survey state the triple first.
- Figure captions (fig-behavioural, fig-tau, fig-chart-case) run long with Shows, Does not show and Good for lines beneath; the lineage uses one-line captions and puts the notation explanation in the text once.
- "The model states thirteen requirements" and "The fit ignores them all" split the requirements across two paragraphs and carry pricing detail ("The launch slot (a 50 kg minimum)...", "up to 4.2 times") that a reader cannot use.
- Caveats recur: "The hardware values of the case are illustrative", the table caption's "The method does not tell the schedule", "Limits, in brief", Discussion's "Interpretation is human validation". The lineage states limits once.
- "Propose, predict, check" and "Two regimes" carry method detail (the percentile rule, "convexity, not strict convexity") that belongs in an appendix.
- The analysis ends in a table whose caption carries a paragraph; there is no sentence giving the decision it supports. The Discussion then reopens method points ("Three claims", "Why a surface").
- Data provenance is in Appendix C pointers only; no sentence says where the table, the fit and the figures come from or how to rerun them.

## Recommendations

1. Open Case construction with the problem as a triple: maximize the metrics, over the six design variables, subject to the four feasibility conditions and six requirements (Martins and Lambe, Table 1).
2. Carry one configuration through every step, as OpenMDAO's Sec. 3 does with its toy model.
3. Name the measures of effectiveness and the requirement ordering once, in one table, and drop the per-paragraph requirement counts (Salado 2021).
4. Show each requirement as a constraint on the solution space, applied after the fit, with its excluded count (Salado et al. 2016).
5. Cut captions to what is drawn; move Shows, Does not show and Good for into the review record (Martins and Lambe, one-line XDSM captions).
6. Move the launch-slot bound, the percentile rule and the strict-convexity remark to appendices (OpenMDAO Sec. 7).
7. State limits in one passage at the end of the Discussion and delete the repeats in captions and case text (survey Sec. V).
8. End Case analysis with the decision and the code and data that produced it, as the survey ends with its classification.
9. Add a short replication paragraph naming the table, the fit call and what cannot be rerun (Gray et al., "Replication of Results").
10. Print the output beside the call that made it (OpenMDAO docs, paraboloid example).
