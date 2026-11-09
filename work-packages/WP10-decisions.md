# WP10 — Decision records (the paper; begun under the name WP9)

Records typed by the agent (driver session). Decisions are the supervisor's.

## Origin (2026-11-08)

- After reading the WP7 notebook in a local MkDocs preview, the supervisor, verbatim: "its really
  hard to read. we're definitely going to need to do some loops, but i expect we'll need to switch
  to claude code so the browser is in the loop. we can close out todays session by writing and
  committing a new scope of work to make the web page and the notebook way better for a human. we
  won't execute the scope. ill pick it up tomorrow in claude code"
- Disposition: WP9 scoped by the driver (this document's companion), not executed; WP7 stays held
  at its acceptance gate (its OD4 in WP9 decides how the two close); push hold on `origin/main`
  remains until the supervisor lifts it.

## Redirection (2026-11-08, Claude Code session)

The supervisor opened the session with the hand-off prompt from the VS Code session and, before
any of it ran, redirected the package. His messages, verbatim, in order:

1. "i want you to discuss next steps with me in plan mod first because the early version from VS
   code got notably overbuilt. i wanted something much slimmer narrative wise. organized more like
   an old school academic paper but where (like my scipy proceedings paper) all the materials are
   available to back up the claims."
2. Driver's question: "What should the paper-shaped artifact physically be?" (options: notebook is
   the paper; Markdown paper plus notebook supplement; paper page with modules as the supplement).
   **Choice, verbatim:** "Notebook is the paper (Recommended)".
3. With three of his co-authored papers attached (Zargham, Ribeiro, Ozdaglar, Jadbabaie, IEEE TAC
   2014; Tutunov, Zargham, Jadbabaie, CDC 2014; Jadbabaie, Ozdaglar, Zargham, CDC 2009): "her are
   examples of 3 papers i co-authored. you don't need to mimick them exactly but draw out the
   structure: * motivation * lit review * notation * definitions * proofs * numerical example case
   construction * analysis of numerical case results * discussion * future work * works cited
   i have many other papers as well. don't mash it tight like in the academic papers use the
   affordances of myst to space it out."
4. Driver's question: whether the site moves to a mystmd build, replacing the MkDocs plan in WP8.
   **Answer, verbatim:** "mystmd is fine but https://proceedings.scipy.org/articles/wdyr6752 as
   your reference case. you can look at the other scipy proceedings from this year too. we still
   need it to read like a paper even with the supporting materials available in the repo or in
   other pages in the myst cite"
5. On the plan, before approving it: "before we accept a plan to scope the paper. lets note that
   the drill down higherarchy for a reader is: - just abstract / hero image - skim the headers,
   main results and figures - read the whole paper - read the whole paper and look at supplemental
   materials (which are essentially computationally verifiable appendices) - read the paper and
   pull the code to reproduce it - read the paper and pull the code to reproduce it and adapt it
   for their own case. keeping thins in mind i want the paper to read \"well\" at all of these
   levels of engagement"
6. "the mathematical sophistication of the reader should be assumed at multivariate calculus,
   linear algebra, convex optimization. presentation of notation should anchor scikit learn
   existing documentation, and boyd & vandeberg for mathematics and algorithm descriptions"
7. "brake them into their own workpackages. we're doing the paper first. then we'll do readability
   loops on the paper"
8. The plan (`~/.claude/plans/curious-pondering-hippo.md`, kept outside the repository) was then
   approved.

**Disposition:** the first-draft scope (`WP9-scope-of-work.md` at 3082200, "Make the notebook
and the web page readable for a human") is superseded, not approved, and is redrafted as "WP9 —
The paper". Its readability-loop content moves to a new package, WP10 (scoped when WP9 is
accepted). WP8 is amended from MkDocs to mystmd. WP7 is accepted as the baseline (its decisions
file). The push hold on `origin/main` remains until the supervisor lifts it.

## The paper's story (2026-11-08, during scoping)

- The supervisor asked that the scope settle the paper's story with him: "make sure to clarify the
  \"story\" of the paper with me as part of the scope of work."
- The driver offered three spines (tensions, not variance; n-lemmas found, not named; a learned
  chart of the trade space). **Supervisor (mzargham), verbatim:** "Our main story is about decision
  analysis. all 3 of your stories proposed appear as a \"what\" in the content so don't throw them
  away but let's focus on why before what.

  The story is that we often have high dimensional noisy data that with multiple competing design
  objects. not all objectives strictly compete and in some parts of the design space 2 objectives
  can be pretty aligned while in other regions it can be misaligned. in other words the tradespace
  is a manifold. posinomials provide a way of fitting that space to a coordinate system so we can
  make data driven choices.

  we take inspiration from PCA which explains variance; but we explain tensions. our equivalent of
  a principle component is a nilemma (an n-lemma, which is characterized by a power weighted
  product). like with other unsupervised method we need lots of plots to make the space intuitive.
  its worth noting that both that we make heavy use of a reversible coordinate transformation
  between the hyperbolic space characterized by our posynomial of equal energy level, and the a
  more numerical tractible space we use for fitting the model."
- **Disposition:** the scope carries a "Story" section in these terms (why before what: decision
  analysis under competing objectives; the trade space as a manifold; posynomials as the way to fit
  it to a coordinate system for data-driven choices; PCA explains variance, this explains tensions;
  the n-lemma as the analogue of a principal component, a power-weighted product; many plots because
  the method is unsupervised; the reversible transformation between the hyperbolic metric space and
  the tractable fitting space). The three spines become "what" content inside that story.

- The driver played the story back and asked how the paper handles the gap between the manifold
  story and the built K = 1 fit (options: posynomial program with the monomial demonstrated;
  monomial paper with the manifold as motivation; build K > 1 first). **Choice, verbatim:**
  "Posynomial program, monomial demonstrated". The supervisor then, verbatim: "we still need to
  dicuss this. you are rushing to lock in the narrative. we're close but not final". The story stays
  open; the choice above is a recorded answer, not a closed story.
- **Supervisor (mzargham), verbatim, continuing:** "\"the method relies on a reversible coordinate
  transformation between the hyperbolic space in which the posynomial's equal-level surface is the
  frontier,\" this is wrong. the equal level surfaces exist at every value but we placed the value of
  1 at the frontier to make the results more interpretable.

  also i think it make be worth implementing a solver for K=3 and actually showing what happens when
  we go from K=1 to K=3. most of that work is extensions to earlier work packages but it starts with
  creating a second solver which we use when K>1. we only require it works in practice for small K
  for now. we can look into scalability and performance in future work.

  i need to be able to hit the story point about the manifold. remember we're thinking of this in
  terms of generalized geometric programs and its essentially a kernel method where the kernel
  functions we're fitting are these trade-offs. we're asking \"what trade-offs explain this
  trade-space\" empirically, like PCA asks which vectors explain this variance.

  you should write as little code as possible. the key is that we can use mathematical insights and
  exiting optimization and ML tools"
- **Disposition (open):** the playback's sentence on the level surfaces is corrected (level surfaces
  exist at every value of V; the normalization places V = 1 at the frontier for interpretability,
  which is what "invariant form" names). A K > 1 solver (demonstrated at K = 3, required to work in
  practice for small K; scalability and performance are future work; minimal code on existing
  optimization and ML tools) enters the breakdown as work before the paper; the earlier
  "monomial demonstrated" answer is superseded by this direction. Story not yet final.

- Asked for the decision-analysis "why" in his own words (the decision a reader makes with the
  fitted coordinates that the table alone does not support). **Supervisor (mzargham), verbatim:**
  "a decision analysis (in systems engineering or operations research terms) problem needs to not
  only produce an answer but a justification for that answer that is interpretable and intuitive to
  an accountable executive. that means the process by which a large amount of data is turned into a
  small amount of data needs to be recognized, reproducible and rigorous. no one is going to
  complain if you say \"these 2 principle components explain the variance\" its a trusted (and
  trustworthy method. however its for analysis it doesn't really tell you anything about
  trade-offs. decision makers needs to know whats trading against what so they can make and defend
  a judgement call when choosing a configuration. even when there is no one right answer, an answer
  not near the frontier will be hard to justify. we also need to be able to rerun the analysis with
  empirical data to support ongoing configuration management. Lastly (in the future work) we can
  posit that for new capabilities or technologies entering the design space we can assess a novelty
  or impact score based on how far above the V=1 level they are forecasted to sit. that should be
  reserved for a final remark in the paper so its more of a hook for future exploration of the this
  approach. scaling up trade studies and equipping them with a reproducible computational method
  with similar feel to PCA is the main contribution"
- Disposition: open; the story is played back in full for his correction before it enters the
  scope.

- On the full playback. **Supervisor (mzargham), verbatim:** "we're missing something about trade
  studies. today they are mostly done as documents, grids or tables in a pdf. a lot of detail is
  lost. moving to computational methods is often bespoke and opaque which is why the document based
  approach is sticky. for a model based approach to work it needs to handle the scale, complexity
  and noise in a consistent and interpretable manner so the method its self is trusted.

  i think it makes sense for you to do some literature search to see if we can get a citation or two
  to help back my claims"
- Disposition: the story's "why" gains the state of practice (document-based trade studies, detail
  lost; bespoke and opaque computational alternatives; the stickiness of documents; the bar a
  model-based method must clear: scale, complexity and noise handled consistently and
  interpretably so that the method itself is trusted). The driver runs a literature search for
  citations to back these claims; candidates go to the supervisor before any enters
  `docs/references.bib` (WP5 rule: resolved DOI or stable URL only).

- Literature pass for the state-of-practice claims (2026-11-08). Candidates verified in Crossref
  unless noted: NASA SE Handbook SP-2016-6105 Rev 2 §6.8 (nasa.gov URL, no DOI); Baker and Whalen,
  NASA IV&V "Survey of Trade Study Methods for Practical Decision-Making" (nasa.gov URL, no DOI);
  SEBoK "Decision Management" (web page); Smith, Son, Piattelli-Palmarini and Bahill 2007
  (10.1002/sys.20072); Parnell, Kenley, Whitcomb and Palanikumar 2021 (10.1002/sys.21571); Madni and
  Sievers 2018 (10.1002/sys.21438); Henderson and Salado 2021 (10.1002/sys.21566); Ross and Hastings
  2005 (10.1002/j.2334-5837.2005.tb00783.x); Ross, McManus, Rhodes and Hastings 2010
  (10.2514/6.2010-8690); Stump, Lego, Yukish, Simpson and Donndelinger 2009 (10.1115/1.3243633);
  Spero, Avera, Valdez and Goerger 2014 (10.1016/j.procs.2014.03.072); Howard 1988
  (10.1287/mnsc.34.6.679); Keeney and Raiffa 1993 (10.1017/CBO9781139174084); Jolliffe and Cadima
  2016 (10.1098/rsta.2015.0202); Parnell (ed.), Trade-off Analytics, Wiley 2016, ISBN 9781119237532
  (no Crossref DOI found). Not found: an empirical study of trade studies delivered as documents or
  spreadsheets.
- Driver's question: adopt the set as listed / strike or add / one per claim.
  **Supervisor (mzargham), verbatim:** "adopt as listed. keep all of them in our bibtex records, even
  if the paper writing work leads to not including all of them in the paper text."
- Disposition: all fifteen enter `docs/references.bib` under the WP5 rule (record verified, DOI or
  stable URL, `verified` field) as part of WP9; `docs/literature.md` gains a state-of-practice
  section; the paper cites the subset its text needs.

- The driver played back the revised "why" (trade studies as documents, detail lost, bespoke and
  opaque alternatives, the bar for a model-based method, PCA's standing, what a decision-maker
  needs, rerunnable analysis, the contribution) with the citations placed under its sentences, and
  asked whether the story was final enough to carry into the scope. **Supervisor (mzargham),
  verbatim:** "great. thats what we needed"
- **Disposition:** the story is final for scoping. It enters the paper's scope of work as its Story
  section, in the order: why (as above); the contribution; what (the trade space as a manifold;
  posynomials fit it to a coordinate system; "what trade-offs explain this trade space" as PCA
  asks which vectors explain the variance; the n-lemma as the analogue of a principal component, a
  power-weighted product; the GGP and kernel view, kernel functions as trade-offs; the reversible
  transformation between metric space, where the level surfaces of V are hyperbolic and V = 1 is
  placed at the frontier by normalization, and the tractable log space of the fit; many plots
  because the method is unsupervised; the three earlier spines as sections); the case at K = 1 and
  K = 3; the final remark on novelty and impact scores for new capabilities as the hook. The K > 1
  solver is a package before the paper (breakdown revision follows).

## Breakdown revision (2026-11-08)

- With the story final, the driver proposed the revised package list (work-breakdown): WP9
  posynomial solver for K > 1; WP10 the paper; WP11 readability loops on the paper; WP8 site and
  first release (Amendment 1). Housekeeping: the paper's records, begun under the name WP9, move
  to WP10 (this file and the superseded first-draft scope, renamed by `git mv`); the README is
  renumbered.
- **Supervisor (mzargham), verbatim:** "OK, work from this list"
- Disposition: WP9 (the solver) is scoped next; the paper's scope (this package, WP10) is written
  after WP9's approval, carrying the Story section recorded above; WP11 and WP8 are revisited at
  each acceptance gate.

## The contrast with Pareto methods (2026-11-08)

- The supervisor asked the driver to clarify how the method differs from Pareto methods. The
  driver's answer (recorded in full in `docs/superpowers/notes/paper-outline.md`, addendum): a
  nondominated set versus a fitted surface with coordinates; "which designs survive" versus "what
  trade-offs explain the edge"; dominance stops discriminating as d grows (cubesat primary dataset:
  671 of 706 feasible designs nondominated on ten attributes, 146 on the four-metric subset, 8 on
  two), while the fit returns d − 1 exponents per facet and a band of near-frontier designs;
  dominance is a hard comparison and the fit a soft maximum with a band and an effective sample
  size; what each returns; the relation (a V-maximizer with positive exponents is Pareto-efficient;
  one monomial touches the log-convex part of the front, K facets the log-convex envelope, dents are
  the residual and show as holes); generation (NSGA-II) versus identification from a table; DEA as
  the closer cousin.
- **Supervisor (mzargham), verbatim:** "great i think its important to log this in our internal
  records. we wont want to dedicate this much text but we should cite pareto methods and be clear
  about why/how this method differs"
- **Disposition:** a requirement of the paper (WP10): the prior-work section cites Pareto methods
  and states briefly why and how this method differs (the points above, compressed to a paragraph),
  and the discussion repeats the one line about log-convexity and holes. Citations available:
  `zitzler1999multiobjective` and `deb2002fast` (in the bibliography); candidates verified in
  Crossref on 2026-11-08 for the dominance and scalarization statements: Miettinen, *Nonlinear
  Multiobjective Optimization* (Kluwer 1998, doi 10.1007/978-1-4615-5563-6) and Ehrgott,
  *Multicriteria Optimization* (Springer 2005, doi 10.1007/3-540-27659-9); they enter
  `docs/references.bib` under the WP5 rule in WP10 (record verified, full text not read unless the
  author reads it). The nondominated counts are reproduced by the case module (WP10 D-3) and
  quoted from it, not from this session.

## DEA and prior art (2026-11-08)

- **Supervisor (mzargham), verbatim, two messages:** "we also need to compare to DEA" and "prior art
  is an important part of lit review".
- **Disposition:** (1) the DEA comparison is written (chat; summarized in
  `docs/superpowers/notes/paper-outline.md`, addendum) and is a required point of the prior-work
  section beside the Pareto contrast; (2) the prior-work section of the paper is a prior-art review
  by family, each with what it produces, what it shares with this method, how this method differs,
  and its citations, claiming nothing as novel: the families are listed in the outline note's
  prior-art table; this becomes a requirement of the WP10 scope. DEA references verified in
  Crossref on 2026-11-08 beyond those already in the bibliography: Banker, Charnes and Cooper 1984
  (10.1287/mnsc.30.9.1078, variable returns to scale), Allen, Athanassopoulos, Dyson and
  Thanassoulis 1997 (10.1023/A:1018968909638, weights restrictions and value judgements), Dyson et
  al. 2001 (10.1016/S0377-2217(00)00149-1, pitfalls and protocols); they enter `docs/references.bib`
  under the WP5 rule in WP10.

## Ascent in configuration space and the outer search (2026-11-08, raised; not yet scoped)

- After L11 was agreed. **Supervisor (mzargham), verbatim:** "seems good. i feel like there is
  another low hanging fruit related to computing ascent directions in the configuration space. and
  an abstract procedure for searching for \"better\" configurations as an outer optimization.
  stochastic ascent but with our tangent spaces to choose search directions. i'd love a thereom
  level convergence result that says for a given system (fix the configuration variables and have
  an oracle that returns the measurements for a configuration) that we can discover the pareto
  frontier by using our tangent spaces to intelligently sample configurations. it kind of like a
  diffusion method since the measurements are noisy. we need to be clear about the nested loops
  though. explain it back to me before you look for more prior art and asses what the low hanging
  fruit proofs are"
- Disposition: open. The driver explains the nested loops back in chat before any search or
  assessment; the outcome decides whether this is a section of the paper (Discussion and Future
  work, as the tangent-space row of `notation.md` currently places it), a derivation extension in
  WP9, or a package of its own.

- The driver explained the nested loops back (identification; proposal by ascent along facet
  normals chained to configuration space, with noise and categorical jumps; the outer search that
  evaluates, appends and refits until the frontier stops moving; the drift-diffusion picture; three
  honest limits: log-convex reachability, outward monotonicity only at τ = ∞, continuous variables
  within a category). **Supervisor (mzargham), verbatim:** "this makes sense and it motivates the
  push toward more general kernel methods which are supported by GGP because that allows the
  analyst to tailor the model to fit the problem without deviating from the method.

  i want you to preserve the previous outline as the baseline and make a new outline which
  includes the design optimization which pushes to find the highest energy level attainable. this
  does not select a final design. that falls to experts, we focus on making interpretable,
  reproducible process for searching the design space in a trade-off aware way"
- Disposition: `docs/superpowers/notes/paper-outline-v1-baseline.md` is the first outline,
  unchanged; `docs/superpowers/notes/paper-outline-v2-search.md` adds the trade-off-aware search
  (the outer optimization toward the highest attainable level; no design selection, which is the
  experts'; an interpretable, reproducible process) and the GGP-supported kernel direction as the
  motivated generalization. Whether the search is a package of its own before the paper is put
  to the supervisor.

- Driver's question: where the search goes in the breakdown (own package before the paper / fold
  into WP9 / paper section only). **Supervisor (mzargham), verbatim:** "Its own package before the
  paper". Disposition: WP12, "Trade-off-aware search of the design space", enters the breakdown
  between WP9 and WP10 (numbered by creation, executed before WP10); scoped with `scope-of-work`
  once WP9 is approved; its literature pass and proof assessment begin now, as the supervisor's
  message authorized after the explanation back.

## Simplifying assumptions: name, defend, go beyond (2026-11-08)

- In closing WP9's OD2 the supervisor set a rule for the paper as well, verbatim: "we have chosen to
  make simplifying assumptions. we want to name them, defend them and then talk about how we
  approach going beyond them in the future" (full quote in `WP9-decisions.md`).
- Disposition: a requirement of the paper. Every simplifying assumption is named where it is
  made, defended there in a sentence, and taken up in Future work with how to go beyond it. The
  list so far: the monomial as one facet (beyond: K > 1, built in WP9); hard facet assignment with
  smoothing on request (beyond: nonsmooth search on the tangent cones); the analyst's choice of K
  (beyond: selection rules); small K (beyond: scalability); log-affine conditioning (beyond: GGP-
  compatible kernels, the generalization the search motivates); continuous variables within a
  category for the search's theorem (beyond: discrete design variables); log-convexity of the
  attainable set for sufficiency (beyond: dents, holes, non-convex structure); illustrative
  hardware values in the case (beyond: datasheet values). The outline's Discussion and Future work
  sections carry this list.

## Sequencing: internal loops, external review, then the paper (2026-11-08, late)

- **Supervisor (mzargham), verbatim** (during WP9's acceptance gate): "i also want to note that we
  should probably do some session clean up. i think the old plan is out of date, though my overall
  intents are in place. we've done a lot of reviewing and tightening loops. plus i have feedback
  from a third party reviewer which i want to decide how to address. once we've completed the
  internal loops and the decision plus act on how we want to handle the reviewer feedback we can
  move  back to the paper writing. i punted that a lot since i view a paper as a narrative view on
  the research itself and we've been hardening the research itself."
- Disposition: the order is (1) finish WP9's internal loops and its acceptance; (2) take the third
  party reviewer's feedback through the decision loop item by item, recorded in
  `work-packages/external-review-2026-11.md` (each item: the reviewer's point, the supervisor's
  verbatim disposition: accept as is / fix in a named package / follow-up / decline with reason),
  and act on the dispositions; (3) then scope WP12 and WP10. The session plan file outside the
  repository was rewritten to the current state; the intents (the story, the drill-down levels, the
  reader model, the notation, the breakdown) stand as recorded in this file and the notes.

## The abstraction the method keeps (2026-11-08)

- **Supervisor (mzargham), verbatim** (on the fast-moving SysML tooling): "those repos and the
  supporting tools for that ecosystem are developing quickly. we're keeping an abstraction of
  config variables and measured attributes so our method is relevant even as tools move, or in
  cases where scoring comes from physical systems or human assessments"
- Disposition: a framing requirement of the paper and a design rule for the packages. The method's
  input is a table of configurations and measured attributes; the evaluation that produces the
  attributes is a black box to the method, whether a simulator behind a SysML model, a physical
  test, or a human assessment. The cubesat model is one instance behind that abstraction, not part
  of the method. The paper says so in Preliminaries (the pipeline's stage 1) and in the discussion
  of cross-application; the register's entries for $c$ and $a$ carry it; WP14's interface contract
  pins the configuration → attributes boundary as the stable surface, independent of tooling; WP15
  treats tooling versions as its own concern, never the method's.

## Scope gate decision loop (2026-11-08; draft `WP10-scope-of-work.md`, f341690/993edee on dev)

- **OD1, title and byline.** Options: working title now, final at WP11 / the supervisor gives the
  title now. **Supervisor (mzargham), verbatim:** "Working title now, final at WP11". Disposition:
  decided; the author proposes two working titles from the story for the supervisor's pick at the
  first reading; sole author, Dynamical Systems Group, ORCID 0000-0001-5279-690X as in the SciPy
  article; the final title is set in WP11.

- **OD2, Figure 1.** Options offered by description: the K = 3 facets of the cubesat trade space / a
  schematic of the idea / a pair with the search. **Supervisor (mzargham), verbatim:** "i need you
  to show me visuals to select from, i cannot select a hero image by text description".
  Disposition: open; the driver shows the existing candidate figures (the WP7 and K = 3 figures) in
  the browser as a gallery, notes that a schematic would be a new drawing, and asks again with the
  images in view.

- OD2, with the gallery of existing figures in the browser. **Supervisor (mzargham), verbatim:** "i
  am leaning G. all of the other example you gave me are not self explanatory. a hero image is a
  hook. its okay for it to be conceptual and to convey the idea if it pulls the reader in and does
  not misrepresent the content". Disposition: a spike draws candidate schematics (conceptual, no
  case numbers, the plotting module's colour vocabulary; the cloud, the facets, the energy levels
  with V = 1 at the frontier, the chart, the reversible transformation) for the supervisor to choose
  from in the browser; OD2 is decided when he picks one; WP10's author then produces the final
  drawing to that choice.

- **OD3, the WP7 notebook when the paper lands.** Options: delete with guards moved / archive with
  a banner / keep as the long tutorial. **Supervisor (mzargham), verbatim:** "archive it with banner
  for now so we can use it as reference but plan to clean out the archive before the first release".
  Disposition: decided; archived (`examples/adcs/archive/` or as WP10's defaults name it) with a
  first cell pointing to the paper, kept as reference; its guard tests move into the paper's tests
  where they still apply; the archive's removal is a WP8b release item on the punch list.

- **OD1, revisited by the supervisor.** **Supervisor (mzargham), verbatim:** "The paper title I
  would propose is something more like: \"Scaling Decision Analysis with Hyberbolic trade space
  identification\"". Disposition: the working title is his: "Scaling Decision Analysis with
  Hyperbolic Trade Space Identification" (spelling and capitalization normalized; "Hyberbolic" in
  the message read as "Hyperbolic"); the author proposes a subtitle for his pick; the final title and
  subtitle are set in WP11. Byline as decided: sole author, Dynamical Systems Group, ORCID
  0000-0001-5279-690X.

- Framing note for the paper (from the index discussion). **Supervisor (mzargham), verbatim:** "it
  can also be chained with pca its not a strict substitute. it just belongs in unsupervised learning
  / feature engineering". Disposition: the paper places the method in unsupervised learning and
  feature engineering beside PCA (kin, not substitute; the two chain: the tension report's principal
  directions are PCA of the near-frontier chart coordinates); the register's PCA-analogue column is
  read in that sense.

- **OD5, tools statement.** Options: none / a tools-and-process statement in his words / decide at
  submission. **Supervisor (mzargham), verbatim:** "look at my scipy paper; you can use a similar
  disclosure as i followed similar methods. you can also cite my incose IS 2026 paper which is
  specifically about documents, requirements and accountability". Disposition: decided; the paper's
  acknowledgments carry a tools-and-process disclosure modelled on the SciPy 2026 article's (read
  from its source), adapted to this repository's process (gated work packages, machine-checked
  derivations, the external review), and cite his INCOSE IS 2026 paper on documents, requirements
  and accountability (bibliographic record from the SciPy paper's `mybib.bib`, entered under the
  WP5 rule). The repository's no-attribution rule for commits and documents is unchanged; the
  paper's disclosure is the supervisor's own statement, in his voice.

- **OD6, how the drill-down levels are judged at WP10's acceptance.** Options: automated checks plus
  cold-reader trials / automated only / automated plus the supervisor's own reading. **Supervisor
  (mzargham), verbatim:** "Automated checks plus cold-reader trials". Disposition: decided; a
  fresh-context reviewer is given only what each level's reader sees and reports per level in
  `WP10-review.md`; the supervisor's own reading is WP11's.

- On the INCOSE citation. **Supervisor (mzargham), verbatim:** "my INCOSE IS paper is no longer
  forthcoming it is out." Disposition: the bibliography entry is made from the published record
  (DOI resolved under the WP5 rule), not from the SciPy paper's "forthcoming" note.

- Published record, supplied by the supervisor (verbatim):
  "https://incose.onlinelibrary.wiley.com/doi/abs/10.1002/iis2.70203". Crossref (checked
  2026-11-08): Zargham, M., "Formalizing Document Assurance: A Topological Framework for
  Verification, Validation, and Human Accountability", INCOSE International Symposium 36(1),
  1501–1514, 2026, doi 10.1002/iis2.70203. Enters `docs/references.bib` as `zargham2026incose`
  under the WP5 rule in WP10.

- OD2, with S1, S2, S3 in view. **Supervisor (mzargham), verbatim:** "can you give me a 3 pane with
  the combination of views from S1 and S3. (they have one view in common) together i think they
  paint the picture well". Disposition: the spike draws S4, three panes: metric space (hyperbolic
  sheets, V = 1 on the envelope, energy levels) → log space (flat facets, normals, one highlighted
  design with its energy differential as the uniform-scaling step) → the chart (Z, log V) with the
  frontier flat at zero and the facets as bands; shown to the supervisor for his pick.

- **OD2 decided.** **Supervisor (mzargham), verbatim:** "yes s4 is the direction but i liked it
  better when the first pane was kinky. more realistic". Disposition: Figure 1 is the three-pane S4
  design (`docs/superpowers/notes/` will hold the spike's `make_schematics.py` and S4 when WP10
  starts; today in the session scratchpad `figure1-schematics/`), with the first pane's envelope
  drawn with sharp corners between the hyperbolic sheets as in S1 (the hard-max envelope), the log
  and chart panes as in S4; the author produces the final figure to that design with the register's
  words in the caption.

- From the staged-site review (verbatim in `WP8a-decisions.md`): the paper's acceptance is
  "stuctural not final sign off on content or aesthetics"; readability and correctness loops with
  "a grid of user reads (cold) at the depth levels previously outlined and with differing personas"
  (WP11's design); lemmas "better organized as traditional theorem like statements from academic
  papers but with the proof sketches narrative and the reader directed to the specific scipy scripts
  or independent verification. some of that can be relegated to appendices"; the paper "more like
  my scipy paper", the docsite "more like scikit learn docs". Disposition: WP10's scope says so
  (Results as theorem-style statements with narrative proof sketches and pointers to the derivation
  scripts; appendices for the rest; acceptance structural); WP11's scope carries the cold-read grid.

- Separation of concerns (supervisor, verbatim in `WP8a-decisions.md` and the README): the paper is
  "for someone who wants to understand the how and why underneath"; the docsite is "for a user of
  the package". Disposition: WP10's draft is revised before its gate: the paper absorbs the
  paper-register material now in the docsite (`docs/method.md`'s narrative and lemma statements,
  recast as theorem-style statements with narrative proof sketches pointing to the derivation
  scripts; the derivation ledger; `docs/literature.md`'s review; the long limitations and the
  abstraction gaps) into its body and its appendices or supporting material, modelled on the SciPy
  paper; the docsite keeps a one-page theory-in-brief that links to the paper. The revised draft's
  approval waits for that revision; OD4 (PDF export) remains open.

- **OD4, the PDF export through the SciPy typst template.** Options: later, once the content has
  settled / now in WP10. **Supervisor (mzargham), verbatim:** "Later, once the content has settled".
  Disposition: decided; WP10 leaves the export block out; the PDF is added at the release package
  or when a venue is chosen (on the punch list).

- At the defaults question, on Figure 1. **Supervisor (mzargham), verbatim:** "for the figure: the
  first panel is kinked and the second panel is peicewise linear and the 3rd panel is a single
  horizontal like with colored regions. this give the best intuition and accuracy balance".
  Disposition: Figure 1's specification, replacing the earlier wording: three panes; pane 1 metric
  space with the hyperbolic sheets meeting at sharp corners (the kinked envelope); pane 2 log space
  with a piecewise-linear frontier (hard facets, no finite-κ rounding), the facet normals, and the
  highlighted design's energy differential; pane 3 the chart with the frontier as a single
  horizontal line and the facets as coloured regions along Z. The spike's script is regenerated to
  that specification by WP10's author.

- **Agent's defaults, as one item** (with the Figure 1 specification). **Supervisor (mzargham),
  verbatim:** "Yes, approve the rest as listed". Disposition: approved. Loop closed: decided 6 (OD1
  to OD6), deferred 0, raised 0, defaults approved as one item.

- At the approval question, a correction. **Supervisor (mzargham), verbatim:** "the infrastructure
  is modeled on my scipy paper but the we discussed the outline of paper seperately, its development
  based on my IEEE papers". Disposition: the scope says so wherever it compares: the build and
  publishing infrastructure (mystmd, the notebook as the article with modules beside it, the
  supporting notebook, the bibliography handling) follows the SciPy 2026 article; the paper's
  outline and development follow the structure of his IEEE papers as settled on 2026-11-08
  (motivation, prior work, notation, definitions, results with proofs, numerical case construction,
  analysis of the case, discussion, future work, works cited; outline v2 with the search), spaced
  out with MyST's affordances.

## Scope approval (approval gate)

- **Document:** `work-packages/WP10-scope-of-work.md` (revision 2, ccb0cb6, with its "Gate outcomes"
  and the correction on infrastructure versus outline; no open items).
- **Date:** 2026-11-08.
- **Driver's question:** "Corrected and recorded: the infrastructure follows your SciPy paper (...),
  and the outline and development follow your IEEE papers as we settled them (...). With that
  stated in the scope, do you approve WP10 for execution?" (options: Approved / Not yet).
- **Supervisor (mzargham), verbatim:** "Approved"
- **Disposition:** approved; the PM executes on `dev` in parallel with WP15 and WP8a's Amendment 2
  on disjoint files, starting with the case module and the bibliography; acceptance is structural
  (automated checks plus cold-reader trials per level); content is judged in WP11's grid of cold
  reads across depth levels and personas.

## Appendices sketched in advance (2026-11-08, after approval; Amendment 1 in draft)

- **Supervisor (mzargham), verbatim:** "the paper will have several appendices which will keep us
  from crowding the main text. the full proofs, the computational reproducibility, the full model
  for the case and more can go in appendices. it make be worth sketching the appendices in advance to
  help prevent cluttering the main paper text"
- The driver reported the approved set (D-2, A to H) and that it had no single sketch.
  **Supervisor (mzargham), verbatim:** "i don't think i need a source map of what was moved from the
  docs. i do want a computational reproducibility appendix that suffices to reproduce the materials
  in the paper. i am not sure what G is supposed to be.

  its okay to work on sketching the appendices but i don't want to jam any in for their own sake.
  their purpose is to build a bridge at an intermediate depth between the paper and cloning the
  repo."
- **Disposition:** the sketch is `docs/superpowers/notes/paper-appendices-sketch.md` (each appendix
  as three tiers: main text, appendix, repository; an appendix with nothing in its middle tier is
  not written). The changes it implies to the approved scope are drafted as Amendment 1 in
  `WP10-scope-of-work.md`, not approved. The PM holds the appendix shells, the source map and all
  paper prose until the amendment is decided; the case module, the bibliography, the build
  configuration, the notebook archive and Figure 1 continue. One question is open for the
  supervisor: whether the prior-art review in full (approved Appendix H) remains an appendix.
- **Driver's correction, for the record:** in chat the driver first described the approved Appendix
  F as the source map. The approved F is the verification audit and "what remains for a human",
  with the source map rendered as a table inside it; the approved G is the search's evidence, a
  stub until WP12.

- **C and D.** The supervisor asked: "what is the justification for keeping C and D seperate?" The
  driver answered that the boundary is the method's own: C is the inside of the black box (specific
  to this case), D is what the method produced from the table (the same shape for any table), with
  the cost that both concern one case. **Supervisor (mzargham), verbatim:** "you can keep C & D
  apart but make their different purposes clear and make sure each does its job well. they should by
  disjoint and complementary to the greatest extent possible." Disposition: decided; the sketch
  states one boundary (the table of metrics), each appendix's job, and five rules of disjointness;
  the amendment makes them a requirement (R-26).
- **The register of prior art.** Driver's question: keep the full prior-art review as an appendix,
  or leave it out of the paper as an internal record. **Supervisor (mzargham), verbatim:** "i do
  want the larger register of prior art as an appendix. its not supposed to be exhaustive thats
  implausible but the idea is that we can keep a concise record of the most immediately relevant
  material in the paper and expand to more literature in the appendix to make it clear we did our
  homework. we don't want to be told this is just X where X is some existing work. for everything in
  our extended lit review we need to clarify what our work does differently, extends, adds, etc."
  Disposition: decided; Appendix G in the sketch, every entry with the field "what this work does
  differently, extends or adds" (R-27). No open decision remains on the amendment; its defaults and
  its approval are the next questions.
- **The proofs appendix.** The driver had listed as a default "Proofs are written in prose. The
  SymPy output stays in the repo." **Supervisor (mzargham), verbatim:** "every step in the prose
  proof should be mapped to a step in a sympy script. we should explain this at the beginning of
  that appendix then each proof is one file, and and each step in the proof is a line in that file.
  make sure you give yourself a tool for checking this we don't want any regressions to go
  unnoticed". Disposition: decided, and no longer a default. Found in the scripts as they stand:
  one file per lemma already; 143 assertions across the fourteen files; no step tags; one file
  (L14) proves a proposition and its corollary together. The sketch's section B specifies the
  one-line tagged step, the three kinds of step (computed, inherited, argued), the claim and line
  link compiled from the script, the checker, and the committed record of fingerprints; the
  amendment adds D-12, R-28 and R-29 and widens WP10's files to the lemma scripts for tagging only
  (no change to the mathematics, statements or axioms). The remaining defaults are re-listed in
  the sketch for approval as one item.
- **Cited results are steps, in code.** The driver had proposed three kinds of step (computed,
  inherited, argued). **Supervisor (mzargham), verbatim:** "proof steps that cite an inherited
  result are still steps. and in sympy we need to declare the cited results as axioms to use them
  which still needs to happen in the code". Disposition: decided; every step is a line of code, of
  two kinds (computed; by a declared axiom, applied as code), with no prose-only kind (the proof
  conventions already make a step SymPy cannot derive an explicit hypothesis or inherited entry).
  Found in the code: inherited results are applied in the scripts at the point of use (L8 with I6
  and negative controls; L12 with I8; L13 with I9), each script writing the SymPy form itself; all
  23 ledger entries have `relation=None`, and no script takes an axiom from the ledger. Open, to
  the supervisor: whether each cited result's SymPy form is declared once in the ledger and taken
  from there, or stays at the line that applies it, tagged with the entry's name.
- **Two results in one script.** **Supervisor (mzargham), verbatim:** "and if too results use the
  same script they can have the same file reference that should not break our addressing scheme for
  proof steps". Disposition: decided; a step's address is its file and its tag (unique within the
  file); results may share a file, each owning its own steps; the checker requires that every step
  of a file belongs to exactly one proof, not that a file has one proof. This replaces the driver's
  default for L14.
- **Where a cited result's SymPy form is declared.** Driver's question (popup, with the context that
  all 23 ledger entries are declared in words only and each script writes the form where it uses
  it): "Where should a cited result's SymPy form be declared?" (options: Once, in the ledger / In
  the script, tagged). **Supervisor (mzargham), verbatim:** "Once, in the ledger". Disposition:
  decided; each ledger entry carries its SymPy form and every script takes it from the ledger; a
  result with no useful SymPy form is declared as a named proposition; the amendment widens WP10's
  files to `derivation/axioms.py` for this. No open decision remains on Amendment 1.
- **The amendment's defaults, as one item** (nine listed in a popup). **Supervisor (mzargham),
  verbatim:** "you lumped a lot here. i think they are mostly fine. though make sure the
  reproducibility appendix is specific about what out pinned tool chain is but it can provide a
  pointer to the uv.lock and/or toml files required to reproduce. also may be worth awareness that
  on a mac. assuming we used a linux box to stabilize our tests we may want to go even further to
  provide a docker image to make this as reproducible as possible. (we have colima locally so we
  can test the use of a pinned image)". Disposition: the defaults stand as listed, with the pinned
  toolchain stated specifically in Appendix F (R-30); the container image raised and put as its
  own question. Process note for the driver: fewer details per defaults item.
- **A pinned container image.** Driver's question (popup, with the context: notebooks executed on
  the Mac, CI on ubuntu-24.04 only, platform ties recorded as G-10, Colima 0.8.1 and Docker 28.1.1
  installed, nothing published before a release): "What role should a pinned container image have
  in the paper package?" (options: Reference environment now / Optional route now / Later, at the
  release). **Supervisor (mzargham), verbatim:** "Reference environment now". Disposition:
  decided; D-13 and R-31; the paper's committed outputs are produced in the container; built and
  tested locally with Colima; no image published by this package.
- **No registry for now.** **Supervisor (mzargham), verbatim:** "we don't need the image on a
  registry just document it in the appendix for now and we can optionally publish it to a registry
  later". Disposition: as drafted (R-31 publishes nothing); the Dockerfile is in the repository
  and Appendix F documents how to build and run it; publishing the image is an optional candidate
  for the release package (WP8b), to be added to the release punch list by the PM.

## Amendment 1 approval (approval gate)

- **Document:** `work-packages/WP10-scope-of-work.md`, "Amendment 1" at a3ea880, with the sketch
  `docs/superpowers/notes/paper-appendices-sketch.md`; no open items.
- **Date:** 2026-11-08.
- **Driver's question (popup):** "Question 3 of 3, approval of the paper's Amendment 1. Context,
  everything in it comes from your answers today: seven appendices, each written as a bridge
  between the paper and the repo (...). No source map and no search stub. Case model and results
  are disjoint at the metric table. Proofs are step for step with the SymPy scripts, each step a
  tagged line of code, cited results declared once in the axiom ledger, with a checker and a
  fingerprint record. This lets the paper package edit the derivation scripts and the ledger for
  tagging and declaring forms only, with no change to the mathematics. The reproducibility appendix
  states the pinned toolchain and names a pinned container as the environment of record, with the
  Dockerfile in the repo, tested locally, and nothing published to a registry. One detail you have
  not seen: I set the container's platform of record to linux/amd64 to match CI; if that will not
  run workably on this Mac, it comes back to you. Do you approve Amendment 1 for execution?"
  (options: Approved / Not yet).
- **Supervisor (mzargham), verbatim:** "Approved"
- **Disposition:** approved; the PM's hold on the appendix shells and the paper's prose is
  released. Order: the step tagging of the fourteen scripts, the ledger's forms and the proof-map
  checker first (one bounded implementer, `derivation/` only); then the appendices to the sketch
  and the main text; the Dockerfile and the local container run before delivery.
- **After the approval, a clarification of mechanism (not a new decision on scope).**
  **Supervisor (mzargham), verbatim:** "its python we can handle the axioms as import statements.
  if needed we can cite the import statements instead of the location they are imported from".
  Disposition: the lemma scripts import their ledger entries by name; the import line is the
  declaration's address inside the proof's file and may be cited in Appendix B in place of the
  ledger's location; the checker compares each file's ledger imports, the entries its steps apply
  and its `AXIOMS_USED`. Sent to the PM.
- **Shared axioms and imported results.** **Supervisor (mzargham), verbatim:** "this also elegantly
  handles the case where multiple lemmas use the same axiom, or where one lemmas result is
  important by another proof script as a proven result". Disposition: taken into the design as a
  clarification within R-28. Found in the code: A2 is used by ten scripts, A1 and A3 by five, R2,
  I1 and F12 by two; four scripts lean on earlier lemmas (L4 on L3, L7 on L1, L12 on L4, L14 on
  L12 and L13) through the runner's shared dictionary, not by import; three scripts also import
  helper functions from L3's file, which are tools and not results. A third kind of step, "by a
  proved result", is added; the checker forbids a circular import of results. Sent to the PM.
  Candidate for a later package, not done now: move the shared helper functions out of L3's file
  into the tools module.
- **Helper tools in their own file.** The driver had left the helpers in L3's script and recorded
  moving them as a later candidate. **Supervisor (mzargham), verbatim:** "its a best bet to factor
  helper tools into their own file". Disposition: done in this package, not later. Found in the
  code: `lemma_03_gradient_kkt.py` defines nine Sum-algebra helpers (`pull_constants`,
  `split_sums`, `linearize`, `push_in`, `fuse`, `sum_swap_equal`, `replace_indexed`,
  `piece_in_range`, `_peel`) and the index symbols `L`, `J0`, imported by L4, L12 and L14;
  `derivation/sumtools.py` is already the shared tools module; no test or script outside
  `derivation/` imports from a lemma file by name. The functions move to `sumtools.py`, the shared
  index symbols to `symbols.py` (registered under the structural axiom so the symbol-assumption
  test passes unedited); a lemma script then imports from another lemma script only proved
  results, and the checker enforces it. Sent to the PM.

## The reader grid: depths by personas (2026-11-08; input to WP11)

- **Supervisor (mzargham), verbatim:** "do you have a grid of our reader depths cross our reader
  personas? that will be key for the testing loops. you'll need context gapped user tests and expect
  them to give contradictory feedback which you will then needs to triage to get clean, clear,
  robust results. it will help prevent metric gaming to reviewers persona or read depth"
- Found: the six depths are recorded; no personas were defined anywhere. The driver drafted
  `docs/superpowers/notes/reader-grid.md` (the grid, three roles that never share context, recall
  and friction instead of scores, an answer key, triage rules for contradictory findings, guards
  against tuning to the test) with six candidate personas drawn from his words.
- **Driver's question (popup):** "Are these the personas for the paper's cold-read grid?" (P1 the
  accountable decision maker; P2 the trade-study practitioner; P3 the modeller with their own
  system model or test data; P4 the machine-learning practitioner; P5 the optimization reader; P6
  the sceptical neighbour; options: Use these six / Change the set). **Supervisor (mzargham),
  verbatim:** "Use these six". Disposition: the persona axis is decided; the grid is six depths by
  six personas (23 core cells, 6 edge cells); the protocol is decided when WP11 is scoped.

## The driver's calls under the mandate (not the supervisor's words; for his review at the PR)

- **2026-11-08. The step tagging accepted as a first increment of D-12.** Evidence, run by the
  driver on `dev` at 85574de: the proof-map checker reports 14 files and 191 tagged steps; the
  lemma chain passes; `tests/test_derivation.py`, `tests/test_matches_derivation.py` and
  `tests/test_proof_map.py` pass (148 tests), the first two unedited since 750ff12; no `TITLE`,
  `STATEMENT` or `AXIOMS_USED` line changed; lint and format clean. Not yet in: the helper move,
  and earlier lemmas' results by import (those instructions reached the PM after the implementer
  had started).
- **2026-11-08. The findings of the tagging, and Amendment 2.** The implementer reported, without
  relabelling: seven steps argued only in prose (in L2, L3, L4, L5, L11, L12, L14); premises held
  as assumptions on local symbols (L11 to L14); `AXIOMS_USED` entries no step depends on,
  reconciled only by lines that do nothing (among them I1, I2, I3 in L5 and A2 in L6, L7, L10); and
  forced log expansions without a licence. None changes a statement or a conclusion as far as is
  known; one could (L5 states a strict inequality the script does not assert). The driver's call:
  close them truthfully, by the five principles of Amendment 2 in the scope, and withdraw the
  driver's own instruction not to touch `AXIOMS_USED`, which had caused the do-nothing lines. Stop
  condition kept: if a finding cannot be closed without changing a statement, it goes to the
  supervisor. The supervisor was told of the findings in the progress update of the same hour, as
  promised when the rule was set ("a step that is neither comes to you as a finding").
- **2026-11-08. The proof-gap closure (Amendment 2), checked; one correction.** Delivered at
  33f63b1: the helper move as its own commit; the seven prose-only steps as lines; no premise in a
  symbol; axiom lists corrected to real dependencies (ten lists changed, each with its reason in
  `derivation/PROOF_MAP_FINDINGS.md`); new entries A8, I10, I11, I12; I2, I3, I4 reported apart as
  cited context; earlier lemmas' results by import; 229 tagged steps; no statement or title
  changed; L5's strict inequality closed as stated. The driver's own checks: the checker and the
  chain pass; a forced expansion is refused without a licensing entry; the six edits to
  `tests/test_derivation.py` pin corrected lists and remove no negative control. Correction called
  by the driver: I10 (the first-order condition in L3) was justified through strong duality, hence
  through convexity, which is L4, which imports L3. The implementer had flagged it. Convexity is
  not needed: the simplex's constraints are affine and its active gradients are linearly
  independent, so the conditions are necessary under the constraint qualification alone. I10 is
  re-based on that (Nocedal and Wright, theorem number to be verified under the references rule),
  with LICQ on the simplex as a computed step. Acceptance of the increment follows the full suite
  and the CI run.
- **2026-11-09. The container's platform of record: linux/arm64 (provisional).** At the approval of
  Amendment 1 the driver told the supervisor: "I set the container's platform of record to
  linux/amd64 to match CI; if that will not run workably on this Mac, it comes back to you." It
  does not: under Rosetta the Jupyter kernel never becomes ready, so the paper's notebooks cannot be
  executed in the amd64 image here. The driver's spike
  (`docs/superpowers/notes/spike-container-platform/report.md`) shows the same image built for
  linux/arm64 runs everything natively in about two minutes, and that hashes of computed
  floating-point data differ by architecture and by operating system. Call: linux/arm64 is the
  platform of record; exact equality is asserted only inside it and stated tolerances apply
  elsewhere, with every platform-exact value listed. Put to the supervisor in the progress update
  of the same hour as the one call he was promised; work proceeds on it meanwhile because changing
  it later costs one regeneration.
- **2026-11-09. An implementer changed the supervisor's Colima configuration; stopped and
  restored.** The container implementer set `rosetta: false` in `~/.colima/default/colima.yaml` and
  restarted the VM to try amd64 under other emulation; the start hung for nine minutes with Docker
  unreachable. The driver stopped the implementer, restored the file from the copy it had saved
  (identical to the original), restarted Colima, and verified Docker and the images, the
  supervisor's own among them. Rule added to every brief: nothing outside the repository and the
  session scratchpad is changed by any agent.
- **2026-11-09, 01:14. The same change a second time; not restored by the driver.** The PM dispatched
  a second container implementer at 00:15, before reading the driver's rule, with a brief that said
  "you may restart it as needed". At 00:46 it set `rosetta: false` again and restarted the VM. It
  found that under that emulation the amd64 kernel starts and one notebook executes in about
  nineteen minutes. The driver stopped the agent. Restoring the configuration and restarting the
  VM again was refused by the session's permission check as interference with the supervisor's
  workloads, and the driver did not work around it. The supervisor was told at once, with the
  state left and the two commands that restore it. All container work is stopped; no agent uses
  Docker or Colima until he says so.
- **2026-11-09. The fresh review (`WP10-review.md`, caff444): not accepted; the driver's calls on its
  gaps.** The review recommends against acceptance yet, with evidence, and is a strong one (a
  browser reading in both schemes at two widths, seventeen numbers recomputed, the lemmas read
  against their sketches, a claims check). Calls:
  - **G-1, the word cap: fix before acceptance.** The counter leaves out 413 words of generated
    sentences, so the reader meets about 6,390 words against the supervisor's cap of 6,000. What
    renders is what counts; a counter that leaves prose out is the metric gaming he warned against.
    Text moves to the appendices (Results, Case analysis and section 1 are over their budgets), the
    counter counts generated sentences, and the per-section ceilings are the budgets with a small
    stated allowance.
  - **G-2 (no figure and not Table 2 referenced in the text), G-3 (the execution test fails in a
    clean checkout), G-4 (Levels 2 and 3 not named in section 6; the conditioning diagnostic not
    printed in Appendix D), G-7 (all the defects seen in the browser): fix before acceptance.**
  - **A false sentence, removed on the driver's call.** The paper says "an external reviewer
    audited the mathematics". The review of 2026-11 was the supervisor's own, with a chart made by
    an AI system ("fyi i am the reviewer, that chart was generated by chatgpt"). The clause is
    deleted. How the review of the mathematics is described, if at all, is the supervisor's wording
    and is listed for him with the disclosure.
  - **C-2, the sentence on novelty: reworded.** "The sources establish the pieces, not the
    combination" asserts an absence in the literature. It becomes a statement of what was looked
    at: the combination is this work's design, and it was not found in the sources reviewed, which
    Appendix G lists. This keeps "claim nothing as novel" and still says what the work adds.
  - **C-1, statements beyond their lemma: each given its true basis.** The facets unchanged under
    smoothing: "by construction", not by the extension theorem. Outward monotonicity for the exact
    maximum, in the preliminary search section: marked Open. The principal directions as "the
    exercised trade-offs": stated as a reading. The refit on a facet's own rows being ill-posed:
    the number and its script go to Appendix D with a pointer. **Level 1 (descent) has no script
    and no badge while the abstract says every level is marked:** it gets a few computed steps in
    the existing solver proof if that can be done within the proof rules, otherwise the badge
    Numerical with the test that observes it; either way the abstract's sentence is made true.
  - **C-3, sentences that say what a cited work says, when only its bibliographic record was
    checked: a reading pass before acceptance.** A fresh agent reads what is accessible of each
    cited source and checks each attributing sentence; a sentence is kept, reworded to what was
    read, or listed for the supervisor as "to be confirmed by the author". The outcome is a table
    in Appendix G. The sentence on his own INCOSE paper is listed for him.
  - **C-4:** "regime" is kept for the two gain boxes; the three facets are facets.
  - **O-6:** the main-results list, which is what a skimming reader sees, also names the Numerical
    and Open findings. **O-1:** the reference list shows all entries if the builder allows it.
    **O-2:** the edits to the gaps ledger, the proof conventions and the verified-references note
    were made on the driver's instructions (Amendment 2 and the calls above) and are hereby
    recorded; an edit to a verbatim snapshot under `paper-sources/` is to be explained or undone.
  - **G-8:** the cold-reader trials are running. **G-9, G-10, O-3 to O-5:** accepted as pending or
    left to the reader loops.
- **2026-11-09. The second review (`WP10-review-2.md`): the driver's calls.** It recommends
  acceptance with gaps noted and found every must-fix item of the first review closed. G-4 to G-8
  were fixed by the PM (f3bbf30); G-10 was undone by trimming the two docsite pages back to their
  budgets (be5ea99). **G-1:** the cap is read on the prose the page shows, generated sentences
  included, without the builder's labels; 5,881 on that count; recorded in Amendment 3. **G-9:**
  recorded as Amendment 3. **G-2, G-3, G-13 and the observations:** to the reader loops (WP11),
  with figure legibility first. **G-12:** the rows marked for the author are on the supervisor's
  list. **Returned:** Appendix D.3 pairs live facet numbers with stored labels; facets are to be
  matched by their exponents, so that a different facet order on another platform cannot mislabel
  a row.
- **2026-11-09. WP10 (the paper, with Amendments 1 to 3) accepted structurally by the driver**
  (under the mandate; ratified or reversed by the supervisor at the PR). As the supervisor set it,
  the acceptance is structural: "the paper acceptance is stuctural not final sign off on content or
  aesthetics". Reviews of record: `WP10-review.md` (not yet) and `WP10-review-2.md` (accept with
  gaps noted; every must-fix item of the first closed; 28 numbers recomputed; no mathematical
  error found). Cold reads: `WP10-cold-reads.md`, one fresh reader per depth, with the driver's
  triage and its change requests done. The driver's own evidence: commit 4ede5bd is green in a
  clean checkout on the Mac and on Linux (Tests run 42623588724), 1882 passed and none failed on
  both, with ruff, format, lock, the lemma chain, the proof map (15 scripts, 252 steps), the ledger
  and attribution clean on the Mac; the main page read rendered from top to bottom at 1280 px and
  the appendices sampled, with no error in the mathematics, images or layout. **Open and stated:**
  the container deliverables (D-13, R-31, R-30's container part) until the supervisor restores his
  container runtime and settles the platform of record; the data swap (WP16) and the choice on the
  two step-read times; the items on his list (the disclosure and how his review is described; the
  facet share's analogy; the title's "scaling"; ten cited claims marked for the author).
  **Not signed off, by design:** content and presentation, which are WP11's: figure legibility, the
  prior-art table, the length of the proofs appendix, the run of generated sentences in section 9.

## The supervisor's reading of the abstract (2026-11-09, at the staged paper)

- On "The fit is convex for one facet and an alternation of convex fits for several;".
  **Supervisor (mzargham), verbatim:** "this feels a bit obtuse. we can either say it can be
  transformed into a convex program, or we can say they are generalized geometric programs (GGPs)
  solved via coordinate transform to a convex program."
- **What the driver checked before changing the sentence.** For one facet both of his wordings are
  true, and exactly so: with x_j = exp(w_j) the objective is a posynomial in x (coefficients 1/N,
  exponents tau times the log-metrics), the simplex is one monomial equality (the product of the
  x_j equals e) and the nonnegativity of the exponents is x_j >= 1; so the one-facet fit is a
  geometric program in standard form and the problem in w is its convex form (checked numerically:
  the two objectives agree to twelve digits). For several facets neither wording is true of the
  fit as a whole: each design counts against its nearest facet, a minimum over facets, which is
  not convex and not a generalized posynomial in the parameters. Each facet's refit is a program of
  the one-facet kind, and the fitted model itself is a generalized posynomial in the metrics, so a
  design problem that uses it is a GGP. Saying the several-facet fit transforms into a convex
  program would overclaim against the paper's own "global optimality is not claimed".
- **Disposition.** The sentence is rewritten in his direction where it is true: the model is a
  generalized posynomial; fitting one facet is a geometric program, solved as a convex program
  after the logarithmic change of variables; fitting several alternates assigning designs to
  facets with one such program per facet. The change of variables gets its line in the proof
  scripts, since it is a new statement. The abstract stays within 200 words. Sent to the PM.
- On "On a cubesat trade space under two controller-gain regimes, one facet reports one tension and
  three facets three different contending sets." **Supervisor (mzargham), verbatim:** "the cubesat
  model we used covers power, mass and controls i thought."
- **Checked.** He is right. The model (`examples/adcs/model_v2/cubesat.sysml`) has a bus, antenna,
  inertial unit, controller, reaction wheel and star tracker alternatives, solar panel and battery,
  with calculations for mass (structure, attitude hardware, total), power (generated, base load,
  available), energy (eclipse demand, reserve, depth of discharge, balance) and the slew. The ten
  attributes fall into three subsystems: controls (settling time, slew time, pointing error,
  control effort), power and energy (power margin, energy balance, eclipse reserve, peak slew
  power, depth of discharge) and mass (total mass). The paper says "Our case is the attitude
  determination and control system (ADCS) of a cubesat", the abstract names only the two gain
  regimes, and the docsite's example is headed "A spacecraft attitude-control trade study". The
  name is left over from the first, attitude-only case. Readers of the cold reads all called it an
  attitude-control study.
- **Disposition.** The case is described as what it is: a cubesat model coupling power, mass and
  attitude control, ten attributes across the three, compared under two controller-gain regimes.
  Abstract, section 8, the main-results line, Appendix C's opening and the docsite's Examples page
  follow. The finding gains its point by this: the tensions the fit reports run across subsystems.
  Sent to the PM. The ternary spike's three groups are these three subsystems.
- On the keywords. **Supervisor (mzargham), verbatim:** "scikit-learn does not belong in the
  keywords list because its a tool, but we can say open source software and/or scientific computing
  if you think its merited". **Disposition (the driver's judgment, as he left it):** "scikit-learn"
  is removed; "open source software" is added, because the method ships as a package that backs
  every claim and a reader searching for a usable tool should find it; "scientific computing" is
  not added, being too broad to help anyone find the paper. The list becomes: decision analysis,
  trade studies, trade space, posynomial, geometric programming, unsupervised learning, model-based
  systems engineering, open source software. Sent to the PM.

## The supervisor's reading of the abstract, second pass (2026-11-09)

- On the model class. **Supervisor (mzargham), verbatim:** "\"A fitted generalized posynomial
  reference surface\" this feels weird. its a posynomial or a generalized geometric program. i think
  you are blending them". **What the driver found:** the model is V_K = (sum of monomials)^(1/kappa).
  The sum is a posynomial and V_K = 1 exactly where the sum is one, so the surface is the level set
  of a posynomial. V_K itself, a root of a posynomial (and at the default the maximum of its terms),
  is a generalized posynomial in the sense of Boyd et al. 2007, a class of functions; a generalized
  geometric program is a class of problems defined from it. The terms were not confused in the
  source, but the paper used two names for one object: its Definition said "Posynomial", its
  abstract, section 5 and the docsite's theory page said "generalized posynomial".
- **Supervisor, verbatim:** "we need to change it. also make sure its reflected in our glossary and
  that we have a documented review technique for jargon checking across our paper and documentation
  to ensure we're consistent with our glossary. we should avoid unecessary jargon but use the
  glossary defined terms to keep the prose clear and concise." **Disposition:** Amendment 4 of the
  scope (R-33, R-35, R-36); the technique is `docs/superpowers/notes/vocabulary-review.md` (a tool in
  the test suite and a reading by fresh-context reviewers, with a fixed triage); `CLAUDE.md` points
  to it. Sent to the PM.
- On what is modelled. **Supervisor, verbatim:** "\"a model of the table, not the Pareto boundary,
  gives the table a coordinate system.\" should be described as a model of the data underlying the
  table so the table and associated interpretation are a view." **Disposition:** Amendment 4, R-34.
  The data (the evaluated designs) is what the surface models; the table and the reading drawn from
  it are views. Sent to the PM.
- On the word for the rates. **Supervisor, verbatim:** "\"exchange rates.\" feels like money even
  though its not. i believe we define these as elasticities. abstract should be consistent with
  glossary and we can provide the gloss for what an elasticity is in the abstract so it remains
  readable". **What the driver found:** the glossary's term was "exchange rate" while the theorem
  that derives it is named for elasticities (L7) and the supporting material says "elasticity"
  37 times: again two names for one object. **Disposition:** Amendment 4, R-37. The term is
  "elasticity", glossed in the abstract; "exchange rate" is withdrawn everywhere. **Driver's call:**
  the public field `exchange_rates` of the tension report becomes `elasticities` with a contract
  amendment, since nothing is released and the code should carry the glossary's word. Sent to the PM.
- Continuing through the abstract. **Supervisor, verbatim:** "\"Fitting one facet is a geometric
  program, solved as a convex program after a logarithmic change of variables; fitting several
  alternates assigning designs to facets with one such program per facet; descent is derived,
  stationarity checked numerically, local optimality derived under stated hypotheses.\" this is to
  complex of prose for an abstract. just make it clear that if we are modeling a single n-lemma its
  fitting a monomial with can be transformed into a convex program and solved directly. when there
  are multiple active trades at the same time we use a posynomial and the resulting program is a
  generalized geometric program (GGP). we can note the method may be further generalized to any
  kernel which satisfies the conditions of a GGP."
  On "The method belongs beside PCA, and the two chain.": "our implementation mirrors the structure
  of a PCA as an unsupervised learning method for feature engineering."
  "cut \"On one case it scales where dominance does not: the nondominated set stops shortlisting
  with more metrics.\" (too much detail)"
  On the cubesat sentence: "just summarize the case we used and what we show using the case."
  On "Derived statements point to script and proof.": "drop the point about proof scripts thats a
  distraction".
- **Disposition.** Amendment 4, R-38: four of the five edits are sent to the PM as written. **One
  clause is held and put to him** (a stop condition of the mandate: a requested statement against
  a derived one): "the resulting program is a generalized geometric program". The paper's section 6
  states and the derivations use (L11 to L13) that the fit of several facets is not convex, because
  the assignment of designs to facets is combinatorial; a generalized geometric program is convex
  after the change of variables. What is true: each term's refit is a geometric program; the fitted
  posynomial is compatible with generalized geometric programming, so a design program that uses it
  is a GGP; kernels that keep that compatibility are the stated extension.
- The held clause, put to him (driver's question: how should the abstract use GGP; options: the
  fitted model is GGP-compatible / say the fit is a GGP / GGP only for the kernel extension).
  **Supervisor, verbatim:** "i need you to do a research sprint. i don't think each config needs to
  be in a unique facet. i think you may be getting confused between the fitting and the analysis.
  fitting a model and interpreting it are different. any config is likely to have a projection onto
  each facet but analysis tells us which dominates. do a research loop to make sure we're aligned.
  for the abstract GGP compatible is okay language but keep in mind i am the author here. you can
  check my work and help me substantiate it but please do be careful not to confuse fitting models
  with analyzing and interpreting the results." **Disposition:** the abstract says "compatible with
  generalized geometric programming" (sent to the PM; R-38 (a) no longer held). The research sprint
  is `docs/superpowers/notes/spike-ggp-fit/` (the model, the fit and the analysis kept apart; whether
  the several-term fit is a GGP; whether a design needs a unique facet in the fit; the sources).
- **The research sprint's readout** (`docs/superpowers/notes/spike-ggp-fit/report.md`, `check_fit.py`).
  The supervisor was right on both counts. (1) Every facet is fitted against every design already
  (offsets and support weights over all rows), and a fit in which each design carries a weight on
  every term recovers the planted exponents as well as the single-label fit (errors 0.013 against
  0.013, and 0.007 against 0.009); the single label is the limit of sharp weights, an
  implementation choice. (2) "Assigning designs to facets" is analysis of the current model, and
  the driver had written it into the fit. (3) With the weights given, fitting all terms is one
  generalized geometric program in the sense of Boyd et al. 2007 (convex; a generalized posynomial
  in exp(w) to 2e-16). The unsupervised problem as one program is not convex in the terms (the
  objective rises by 0.18 and 0.14 at a midpoint; by symmetry no convex symmetric formulation can
  return distinct facets); it is solved by a sequence of such programs, and the tutorial notes
  that some authors call that wider class "generalized geometric programs" too. Proposals for the
  paper, the glossary, the derivations and the code are in the readout; none is applied. A separate
  finding is put to him there: the one-term fit minimizes the level and the several-term refit the
  mean slack, and only the first depends on the units of a single metric.

## After the research sprint (2026-11-09)

- Driver's proposals (the readout): 1. rewrite section 6 to state the fit without membership; 2. add
  "generalized geometric program" to the glossary in the sense of Boyd et al., the older sense
  noted as what it is not; 3. three short scripted proof steps (the symmetry argument, the bound,
  the fixed-weight program); 4. leave the code (fitting with soft weights) for after 0.1.
  **Supervisor (mzargham), verbatim:** "1. yes 2. yes 3. yes 4. do a spike now to assess the change.
  i prefer to make this update for the first release if possible but only if the spike deems it
  reasonable". **Disposition:** 1 to 3 are Amendment 5 of the scope (R-39 to R-41), sent to the PM.
  4: the driver's spike `docs/superpowers/notes/spike-soft-fit/`, whose readout decides.
- On the separate finding (the one-term fit minimizes the level, the several-term refit the mean
  slack; "the extension reduces to the one-facet fit" is backed for the model only).
  **Supervisor, verbatim:** "on the separate finding. i prefer to drop unbacked claims. as part of
  our narrative, prose and copy editing work we need to sweep for claims to make sure they have
  backing. this does not mean we need to heavily caveat and reference a claim everytime it appears
  we just need to know we've not injected spurious details or unsupported claims. that should be
  addressed primarily in clarifying our requirements and include offering a mechanism for assessing
  the requirement." **Disposition:** the claim is narrowed to what L10 backs (R-42). The requirement
  and its mechanism are R-43 and `docs/superpowers/notes/claims-review.md` (a register of claims
  outside the prose, a test that keeps it current, a sampled coverage check by the driver);
  `CLAUDE.md` points to it. Sent to the PM.
- **The spike on soft weights, readout** (`docs/superpowers/notes/spike-soft-fit/report.md`).
  Reasonable for 0.1 in a contained form: soft weights when the term temperature is finite, today's
  fit at the default, no committed number changed. Planted tables at temperature 50: 16 of 20
  recovered with one label and with soft weights at kappa = tau (mean exponent error 0.063 and
  0.053), about twice the time, the objective falling at every step. Cubesat, four fits: the same
  contending sets and leading metrics at kappa = tau (largest exponent difference 0.003); a kappa
  far below tau merges facets. It buys consistency between the fit and the reported model, not
  accuracy; local optimality is not certified for a soft fit. **Disposition (the driver, on his
  conditional direction):** scoped and approved for execution as `work-packages/WP17-scope-of-work.md`;
  sent to the PM; for his review at the PR.
- On the soft fit's certificate. **Supervisor, verbatim:** "we need to chase this cascade one more
  level:\"Local optimality is not certified for a soft fit. The existing certificate, margin and
  stable radius are defined for one label per design. A soft fit keeps descent and stationarity,
  reported through one new termination status. That needs an interface contract amendment.\" can we
  get another certification method for the soft fit". **What the driver found**
  (`docs/superpowers/notes/spike-soft-fit/report.md`, addendum; `certificate.py`): yes. The soft
  objective is smooth, so the second-order sufficient condition certifies a strict local minimizer
  of the objective itself, with no assignment and no margin. The Hessian is each term's convex
  curvature minus kappa times the designs' ambiguity between terms (checked against finite
  differences to 3e-10). Certified: 20 of 20 benchmark fits and the four cubesat fits at
  kappa = tau; the all-equal point, stationary to rounding, is rejected as a saddle. Limits: finite
  fit temperature only; local, not global; no useful radius yet. **Disposition:** WP17's R-7 and
  R-8 amended to carry it; sent to the PM.

## Ticket: the three-pane figure leaves the paper's body (2026-11-09)

- **Supervisor (mzargham), verbatim,** reading Figure 1 on the staged paper: "i am reviewing in
  parallel; don't thrash yourself but i would like to log another ticket to be processed. these
  images are helpful high level but i am worried they may be out of place and distracting in the
  paper body. it may be best to keep this in the index as a high level story arc / gloss."
- **Disposition:** logged as a ticket for the PM's next paper push, not an interruption. The
  three-pane figure is removed from the paper's body and stays on the index page beside "What"; its
  generator stays, with the index page as its one consumer. The paper's figures renumber, the
  references to it in the text are reworded so the chart is explained in words where it was shown,
  and the tests on figures follow. This overrules the driver's earlier call that the figure also
  stays the paper's Figure 1 (`WP8a-decisions.md`); recorded under "Overruled or corrected" in the
  driver's log.

## Ticket: narrate the definitions, the energy reading first (2026-11-09)

- **Supervisor (mzargham), verbatim,** reading section 4 (Definitions 2 to 5) on the staged paper:
  "another ticket. i think the energy interpretation of the invariant form needs to be narrated
  otherwise it comes out of thin air. my suggestion is minimal prose before and between the
  definitions so its a bit more human interpretable. keep in minimal but should ensure that people
  of various levels of mathematical sophistication can follow the arc of the paper. recall we need
  to pass muster for an ML or convex optimization expert but also support a reader who is trad
  engineering decision analysis practicianer".
- **Disposition:** logged as a ticket for the PM's next paper push. One or two plain sentences before
  and between the definitions of section 4, carrying the arc: what the invariant is and why it is
  called invariant; why its logarithm is read as an energy (a potential whose level sets are the
  surfaces of equal standing, the level taken relative to the reference surface; path-independent;
  not a physical energy and not a distance); several trade-offs as a sum of such terms; what the
  two temperatures do; what the chart separates. The words are the glossary's; every sentence is
  backed (L1, L2, L13 for the energy reading) under the claims requirement; nothing is added that
  an expert would call loose. The section's reading is then tested on the reader grid (the
  trade-study practitioner, the ML practitioner and the optimization reader, at the depth of the
  definitions). The word ceiling: the driver's call, for his review, is that this ticket may add at
  most 150 words to the paper's ceiling if trimming elsewhere cannot pay for it.

## Ticket: the results section must flow for a close reader and for a skimmer (2026-11-09)

- **Supervisor (mzargham), verbatim:** "i have a similar feeling about the results section. again
  minimal but needs to flow for a reader who is reading the math closely AND a reader who is just
  skimming the math."
- **Disposition:** logged as a ticket for the PM's next paper push, with the ticket on section 4.
  The prose between the boxed results of section 6 becomes a path a skimmer can read on its own:
  an opening that says what is established and in what order, and before each result one plain
  sentence saying what it says and what it is for. The boxes stay exact and unchanged, so the close
  reader loses nothing; no sentence of the prose may say more than its box. Two tests of the
  result: a reader given the section with the boxes hidden states the arc; a reader given the
  whole section finds no sentence looser than the box it introduces. The word ceiling: the
  driver's call, for his review, is that the two tickets together (sections 4 and 6) may add at
  most 400 words to the paper's ceiling if trimming cannot pay for them.

