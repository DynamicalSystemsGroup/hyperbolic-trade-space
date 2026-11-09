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

## Scope approval (approval gate)

- pending (the paper's scope is drafted after WP9's acceptance, the external review's triage, and
  WP12)
