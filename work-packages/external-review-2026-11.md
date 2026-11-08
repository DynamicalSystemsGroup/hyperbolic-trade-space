# External review (third party), received 2026-11-08: record and item index

The supervisor pasted a third-party review of "Hyperbolic Trade Space" into the session on
2026-11-08, with a one-page "Paper Map" figure (`docs/superpowers/notes/external-review/paper-map.webp`).
The review refers to a computational audit that ran "all eleven derivation modules and 156 selected
tests", so it was made on the repository at or after the WP9 state (L11 present). Per the
supervisor's sequencing (verbatim in `WP10-decisions.md`, "Sequencing"): the internal loops of WP9
close first, then each item below goes through the decision loop with the supervisor (accept as
is / fix in a named package or amendment / follow-up / decline with reason), recorded here, and
the dispositions are acted on before WP12 and WP10 are scoped.

## Item index (the driver's indexing; the text is the reviewer's, quoted in section 2)

| ID | Review section | The point, in brief | Touches |
|---|---|---|---|
| E-1 | 3.1 (principal) | Distinguish numerical termination, approximate first-order stationarity and local optimality for the multi-facet algorithm; define a per-facet simplex first-order gap $G_k(w_k)=\max_{v\in\Delta}\nabla f_k(w_k)^\top(w_k-v)=\nabla f_k(w_k)^\top w_k-\min_j[\nabla f_k(w_k)]_j$ with $0\le f_k(w_k)-f_k^*\le G_k$; report feasibility residuals, max gap, objective change, assignment changes, termination reason; define the assignment margin $\gamma$ and an explicit assignment-stable radius; a conditional local-optimality proposition (unique maximizing facets, nonempty facets, exact facet optima, offsets $\beta_k=J_\tau(w_k;U)$); the approximate certificate $F(W)-F^*_{\mathrm{fixed}}\le\sum_k\frac{\lvert C_k\rvert}{N}G_k(w_k)$; three-level statement (descent / numerical stationarity / conditional local optimality); no global convergence required | WP9 solver (`solve_terms`), its docs, the derivation ledger (new lemmas/proposition), WP12's theorem, WP10 |
| E-2 | 3.2 | Finite-temperature regularity: balanced hard-support geometry does not imply an interior finite-$\tau$ optimizer (audit counterexample); state the full simplex KKT $g_j\ge\lambda,\ w_j(g_j-\lambda)=0$ and reserve equal gradients for positive-weight coordinates | L3 statement and `docs/method.md` "The fit"; R1 condition |
| E-3 | 3.3 | Distinguish the smooth fitted reference surface, the hard empirical supporting envelope and the true Pareto boundary; at finite $\tau$ some designs have $V>1$ by construction | `docs/method.md`, `docs/why-and-how.md`, the paper's definitions (notation note) |
| E-4 | 3.4 | The multi-term bounds in the text are wrong for the log-sum-exp form: correct is $\max_k x_k\le\Phi_K\le\max_k x_k+\frac{\log K}{\kappa}$; the executable derivation (L10) is right; fix the explanatory text | `docs/method.md` extension section (WP9 docs), `docs/api.md`, notation note |
| E-5 | 3.5 | Separate existence, uniqueness and stability; discuss the restricted Hessian and local sensitivity (near-correlated metrics, $\tau$ changes move $w$ while the objective barely moves); state numerical tolerances for active/inactive exponents; distinguish numerically zero from mathematically zero | `docs/method.md` identifiability, `tensions.py` threshold, sparsity option docs |
| E-6 | 3.6 | State statistical conclusions at their demonstrated level: L6 is a population cumulant identity, not finite-sample unbiasedness; consistency claims need independence, integrability, identifiability assumptions; a fitted normal is a feature of the conditioned empirical model, not a causal exchange | L6, `docs/method.md` noise section, limitations |
| E-7 | 3.7 | Implementation and terminology: the single-observation shortcut returns uniform weights where they do not minimize the objective; the exact-zero metric convention differs from the continuous limit when the exponent is zero; call $\log V$ a uniform log-scaling coordinate, not a Euclidean distance; qualify global claims about chart-origin exclusion and universal vertex solutions (edge-interior counterexamples exist) | `estimator.py` degenerate paths, `preconditioning.py` zero handling, docs wording, the spike's "sliver" argument in `docs/method.md` and the spikes' READMEs |
| E-8 | 4 | Presentation: Lemma 1 (convexity and first-order certification of facet refits), Lemma 2 (assignment-stable neighbourhood with explicit radius), Proposition 3 (assignment-stable local optimality), Corollary 4 (approximate certificate), an algorithmic stopping declaration that separates certified convergence from iteration-limit termination | derivation chain (L12–L14 candidates), `docs/method.md`, WP10 Results section |
| E-9 | 2.1–2.5 | Strengths the paper can lean on: the monomial invariant and its log form; the convex single-term fit and its hard-limit relation; the invertible chart; the posynomial extension; transparency and reproducibility | WP10 framing |
| E-10 | Paper Map (figure) | The reviewer's structure of the mathematics: assumptions A1–A6 (positive metrics, simplex weights, observations, temperature, regularity, optional noise model), foundation, single-term core C1–C3, G1–G4 (chart, elasticities, noise, pull-back), extensions P1–P3 (posynomial, Pareto efficiency, identifiability), algorithm A1–A3 (descent, stopping and certificates, assignment-stable local optimality), open questions Q1–Q4 (global convergence; statistical consistency under noise and refitting; identifiability of active metrics under finite, biased observations; conditions for frontier recovery, fitted versus true Pareto boundary); status badges Derived / Numerical / Open | WP10 outline (compare with `paper-outline-v2-search.md`); the ledger's "what is proved, inherited, observed" |

## Dispositions and the response to the reviewer

The supervisor's instruction, verbatim (2026-11-08): "please make sure you save the map and the
review verbatim even if we don't take all the recommendations. we'll make our own dispositions and
log our response to the reviewer in line with conventions. either accept suggestions or have a
clear explanation on why we chose not to".

Form of the record, per item E-n after the decision loop (after WP9's acceptance, one item at a
time): the supervisor's disposition quoted verbatim; the disposition class (accepted as is /
accepted with a change, naming the package or amendment that makes it / declined, with the reason);
and the response text to the reviewer, written as a reply in the conventions of a response-to-
reviewers letter: the reviewer's point restated in one sentence, what was changed and where
(commit, file, lemma or section), or why it was not changed, with evidence. The complete response
letter is assembled from these entries when all items are dispositioned, and kept here under
"Response letter".

Driver's note before triage (fact-checked 2026-11-08, not a disposition): E-4 is confirmed. The
method page defines $\Phi_K$ with a log-sum (line 533) and states the bound
$\max_k x_k-\frac{\log K}{\kappa}\le\Phi_K\le\max_k x_k$ (line 554), which is the log-mean-exp
bound; the L10 script computes $\Phi_K-M\in[0,\frac{\log K}{\kappa}]$ (correct for the sum) while its
own docstring repeats the wrong direction; two later sentences of the method page have it right
("within $(\log K)/\kappa$ above the maximum"). So the executable derivation is right and the prose
and the L10 docstring are wrong, as the reviewer says.

- **E-4 (multi-term bounds).** Driver's question: fold the correction into WP9's current loop or hold
  it for the triage. **Supervisor (mzargham), verbatim:** "Fold the E-4 correction into WP9 now".
  Disposition class: accepted as is, made in WP9 (the running Amendment 3 loop; the fourth review
  covers it). Response text (draft, to be confirmed by the commit): "Correct. $\Phi_K$ is the
  normalized-by-nothing log-sum-exp, so $\max_k x_k\le\Phi_K\le\max_k x_k+\frac{\log K}{\kappa}$; the
  derivation script L10 computed this bound and the prose stated the log-mean-exp bound. The method
  page, the L10 docstring and the API page now state the bound as the script proves it (commit to be
  named)."

- **E-1 (certificates, assignment-stable neighbourhood, conditional local optimality, three-level
  language).** Driver's options: accept in full in WP13 / accept the statements and defer the code /
  decline part. **Supervisor (mzargham), verbatim:** "accept the statements. do a spike to determine
  implementation level of effort. i prefer to accept in full but i need to make sure this is
  feasible. we can assess after the spike if anything needs to get deferred". Disposition class:
  accepted (the statements); the implementation scope is decided after a research spike on the
  level of effort (certificates and termination reporting in the solver; the lemma, proposition and
  corollary as derivation entries; docs restructured to the three levels). Response text: after the
  spike.

- **E-2 (finite-temperature regularity; full simplex KKT).** Driver's options: extend L3 and the
  method page / docs only / decline. **Supervisor (mzargham), verbatim:** "Accept: extend L3 and the
  method page". Disposition class: accepted, in WP13: L3 gains the boundary KKT statement
  ($g_j\ge\lambda$, $w_j(g_j-\lambda)=0$, $\lambda=w^\top g$), derived in SymPy where it can be and
  verified numerically where it must; the method page states the full conditions, reserves the
  equal-gradient reading for positive-weight coordinates, and records the reviewer's lesson that
  balanced hard-support geometry does not imply an interior finite-$\tau$ optimizer; condition R1's
  wording tightened accordingly. Response text: after the change, naming the commit and the lemma.

- **E-3 (fitted reference surface / empirical envelope / Pareto boundary).** Driver's options: three
  named objects used consistently / a lighter touch / decline. **Supervisor (mzargham), verbatim:**
  "enforce the sharp distinction in the sympy work but leave us some room to maneuver in the prose.
  we don't want constant caveats to break flow. its okay to know which we mean from context as long
  as the underlying math is tight". Disposition class: accepted with a change: the three objects are
  defined once (notation note, method page, the paper's definitions) and the derivation scripts and
  their statements name the object they are about precisely (the finite-$\tau$ reference surface
  $\Phi=0$ with $V>1$ possible; the $\tau=\infty$ supporting envelope; the Pareto boundary of the
  attainable set, which L11 relates to maximizers and nothing identifies with the fit); the prose
  may say "frontier" where the context makes the object clear, without repeated caveats. Response
  text: the distinction is enforced in the executable derivations and defined once in the text;
  the prose uses "frontier" where unambiguous. In WP13 (docs, derivations) and WP10 (paper).

- **E-5 (existence, uniqueness, stability; tolerances).** Driver's options: docs, tolerances and a
  sensitivity diagnostic / docs and tolerances only / decline. **Supervisor (mzargham), verbatim:**
  "Accept: docs, tolerances, and a sensitivity diagnostic". Disposition class: accepted, in WP13: a
  method-page section separating existence (compact simplex, continuity), uniqueness (strict
  convexity on the simplex tangent space) and stability (the restricted Hessian and local
  sensitivity); the participation threshold and the contending-set rule stated with their
  tolerances wherever used, numerically zero distinguished from mathematically zero; the estimator
  exposes a conditioning diagnostic (the smallest eigenvalue of the restricted Hessian at the fit,
  or an equivalent) so sensitivity is reportable. Response text: after the change.

- **E-6 (statistical claims at their demonstrated level).** Driver's options: restate L6's scope,
  add the assumptions, drop any consistency claim / keep a conditional consistency remark /
  decline. **Supervisor (mzargham), verbatim:** "Accept: restate L6's scope, add the assumptions,
  drop any consistency claim". Disposition class: accepted, in WP13: L6's statement and the noise
  section say "population identity under the log-space Gaussian model"; every sentence that reads as
  finite-sample unbiasedness or consistency is removed or conditioned on named ledger assumptions
  (independence, integrability, identifiability); the reading that a fitted normal is a feature of
  the conditioned empirical model and not a causal exchange goes into the interpretation section.
  Response text: after the change.

- **E-7 (four implementation and terminology items), first pass.** Driver's options: accept all four
  / accept (iii) and (iv) now and (i), (ii) later / decline part. **Supervisor (mzargham), verbatim:**
  "can we look at them a little closer. let's make sure we distinguish claims about the formal
  abstractions and the implementations. we know these are different things as the reviewers noted.
  i don't want to muddle up the text with lots of caveats if we can just clarify that the
  theoretical objects formal properties are conditioned on assumptions we cannot know hold in
  practice and thus we interpret results in light of them. this a common map territory gap for
  numerical methods. we should maintain a record of these gaps but also not trip over ourselves
  relitigating them. focus on the core research materials documenting the abstraction gaps and
  assumptions that we cannot strictly prove hold but we can explore how sensitive they are in
  practice. ideally we're insensitive enough to get practical results without throwing the baby out
  the baby the bath water. look at these four and also have a look at the other feedback through
  this lens so we take a consistent position. all models are wrong some are useful, useful to a
  specific purpose in a specific situation and we're focused on improving trade studies"
- Disposition: open; the driver examines the four items in the code and docs, classifies each
  (formal claim / implementation convention / wording), re-reads E-1 to E-10 through the same lens,
  and proposes one consistent position (a standing record of abstraction gaps with their bridging
  assumptions and sensitivity evidence; derivations sharp; prose stating the policy once) before
  the next question.

- **E-1, spike delivered** (`docs/superpowers/notes/spike-certificates/README.md`, scripts and tables
  beside it). Verdict: feasible in full as one package, 16 to 22 implementer hours, about 930 to
  1220 net lines (code 200–260, tests 150–200, three lemma scripts and ledger 350–450, docs
  230–310). The mathematics matches the solver as built exactly (step B is the argmin of
  $f_k$; the mean slack is the fixed-assignment sum; the gap $G_k$ is the residual of E-2's full
  simplex KKT). Two findings beyond the reviewer's ask: SLSQP's stop leaves $G_k\sim10^{-5}$ at
  finite $\tau$, so a five-step Newton polish on the active set (25 lines) is needed for a tight
  certificate; and the monotone guard fired on round-off in 9 of 100 $\tau=\infty$ restarts (8 of
  them two identical facets), which a tolerance and the reported margin expose. At $\tau=\infty$ the
  margin is exactly zero on the three recovery-failure seeds (a row on two facet planes), so the
  proposition's hypothesis fails there by structure. Deferrable without weakening the response: the
  SymPy scripts for Lemma 2's radius and Proposition 3's regrouping (state, verify numerically),
  asserting the Corollary bound in tests, the floored-gap formula, a tolerance parameter. Not
  deferrable: the three-level language and stopping declaration, $G_k$ computed and reported, the
  margin and radius, the termination status, the four statements as ledger entries, the guard
  tolerance. Implementation scope: put to the supervisor.

Pending: E-7 (second pass), E-8 to E-10, E-1's implementation scope.

## Response letter

To be assembled from the dispositions.

## The review, verbatim

Review of “Hyperbolic Trade Space”
Recommendation: Accept with Minor Revisions
1. Summary and Overall Assessment
This manuscript introduces a mathematically structured framework for identifying and representing trade-offs among competing engineering performance metrics. The central contribution is the construction of a positive, homogeneous monomial invariant whose logarithmic representation enables convex estimation, interpretable trade-off elasticities, and an invertible coordinate decomposition. The framework is subsequently extended to generalized posynomial representations, allowing more flexible descriptions of engineering trade spaces.
The work offers a compelling perspective on multi-objective engineering design. Rather than identifying directions that primarily explain empirical variance, the methodology seeks coordinates associated with constraints on attainable performance. This provides a potentially valuable connection between geometric representations, optimization, and engineering interpretation.
The manuscript is particularly strong in its mathematical organization and computational reproducibility. The principal algebraic identities, convexity results, derivative formulas, temperature limits, and coordinate reconstruction formulas are supported by exact derivations and independent computational checks. The audit reports successful execution of all eleven derivation modules and 156 selected tests, together with close agreement between independent numerical optimization methods.
The remaining concerns largely involve the precision of certain theoretical statements, the interpretation of finite-temperature frontiers, and the relationship between numerical termination, first-order stationarity, and local optimality of the multi-facet fitting algorithm.
Importantly, these concerns do not undermine the central monomial construction, the convex single-term identification problem, or the coordinate representation. They can largely be resolved by strengthening assumptions, defining numerical certificates, and stating the scope of the theoretical guarantees more precisely.
I therefore recommend acceptance with minor revisions. The revisions should focus on consolidating the mathematical presentation and ensuring that claims about convergence, local optimality, and statistical interpretation are fully supported.
2. Principal Strengths
2.1. A coherent and interpretable mathematical foundation
The proposed invariant,
[
V(m)=e^{-\beta}\prod_{j=1}^{d}m_j^{w_j},
\qquad
w\in\Delta^{d-1},
]
provides a concise representation of multiplicative relationships among engineering performance metrics.
Its logarithmic form,
[
\log V(m)=w^\top\log m-\beta,
]
transforms a multiplicative relation into an affine geometric object while retaining a direct interpretation of the exponent vector in terms of relative metric sensitivities.
The simplex normalization establishes degree-one homogeneity, giving the model a natural behavior under uniform multiplicative scaling.
These properties are mathematically useful and conceptually appropriate for engineering trade-space analysis.
2.2. A well-founded convex optimization formulation
The single-term fitting objective,
[
J_\tau(w)=
\frac1\tau
\log\left(
\frac1N\sum_{i=1}^{N}
e^{\tau u_i^\top w}
\right),
]
has a tractable gradient and Hessian. The Hessian admits a weighted-covariance interpretation, providing a direct argument for convexity.
The relationship between finite-temperature fitting and the hard minimax limit is particularly valuable. It connects the proposed method to established convex optimization and linear programming duality, while giving the temperature parameter a meaningful mathematical role.
The computational verification is convincing within its stated scope. Exact symbolic differentiation agrees with the proposed formulas, numerical derivative errors are on the order of (10^{-10}), and independent constrained solvers produce closely matching objective values.
The single-term optimization problem is therefore a strong foundation for the broader methodology.
2.3. An elegant and invertible coordinate representation
The decomposition into log-ratio coordinates and a frontier-relative coordinate is one of the manuscript's strongest contributions.
It separates metric composition from overall scaling while retaining enough information to reconstruct the original log-metric vector.
Independent numerical experiments confirm reconstruction to near machine precision across multiple dimensions, basis choices, and simplex-boundary weights.
This provides a useful alternative to dimension-reduction methods that sacrifice information and creates opportunities for interpretable trade-space visualization and sensitivity analysis.
2.4. A natural extension to generalized posynomial geometry
The multi-term construction provides a promising generalization of the monomial representation.
By combining affine terms in log-metric coordinates through a log-sum-exp structure, the framework can represent more complex level-set geometry while preserving several favorable analytical properties.
The extension is mathematically natural and gives the paper a clear direction beyond single-facet trade-space representations.
2.5. Mathematical transparency and reproducibility
The organization of the mathematical development into explicit assumptions, lemmas, executable checks, and computational experiments is commendable.
The audit includes symbolic verification, derivative checks, primal-dual optimization tests, reconstruction experiments, and adversarial counterexamples.
This level of mathematical transparency is a meaningful strength.
The fact that the audit identifies several narrow discrepancies while confirming the main identities is reassuring. The issues appear concentrated in theorem scope, boundary conventions, and algorithmic interpretation rather than in the basic mathematical construction.
3. Recommendations for Revision
3.1. Formalize stopping criteria, optimality certificates, and assignment-stable neighborhoods
This is the principal recommendation.
The multi-facet algorithm alternates between assigning observations to facets and solving constrained refitting problems. The idealized block updates admit a descent argument under the stated assumptions, and the implemented acceptance mechanism can prevent increases in the objective.
However, the manuscript should distinguish the following three statements:

1. An algorithm has terminated under a specified numerical stopping rule.
2. Its current iterate satisfies approximate first-order optimality conditions.
3. Its current iterate is a local minimizer of the full multi-facet objective.

These are not equivalent.
In particular, a small change in objective value does not by itself establish local optimality. Nor does termination at a prescribed maximum iteration count.
The computational audit identifies an example in which an iteration-limited output admits a nearby descent direction. This is not a fundamental failure of the optimization framework, but it demonstrates the need for more precise convergence language.
I recommend introducing a computational stopping certificate and a conditional local optimality result based on assignment stability.
3.1.1. Define a first-order certificate for each convex facet refit
For the unpenalized refitting objective,
[
f_k(w)=
J_\tau(w;U)-\bar u_k^\top w,
\qquad
w\in\Delta^{d-1},
]
where (\bar u_k) is the mean log-metric vector of the observations assigned to facet (k), define the simplex first-order gap
[
G_k(w_k)=
\max_{v\in\Delta^{d-1}}
\nabla f_k(w_k)^\top(w_k-v).
]
Because the feasible set is the simplex, this has the explicit expression
\min_j[\nabla f_k(w_k)]_j.
}
]
For a feasible point and differentiable convex objective, (G_k\geq0), with equality if and only if (w_k) is globally optimal for its convex refitting subproblem.
Furthermore, convexity gives the objective-error bound
[
0\leq f_k(w_k)-f_k^*\leq G_k(w_k).
]
This provides a practical and mathematically interpretable stopping certificate.
A termination rule should report, at minimum, the following quantities:

* Simplex feasibility residuals.
* Maximum facet first-order gap.
* Absolute or relative objective change.
* Assignment changes between iterations.
* Maximum iteration count and termination reason.

For example, a candidate convergence criterion might include
[
\max_kG_k(w_k)\leq\varepsilon_{\mathrm{KKT}},
]
together with a specified feasibility tolerance and stable assignments.
The tolerances should be reported explicitly and should not be presented as proof of exact mathematical optimality.
A maximum-iteration termination should be reported separately from certified convergence.
3.1.2. Define an assignment-stable neighborhood
Let the score of observation (i) under facet (k) be
[
s_{ik}=w_k^\top u_i-\beta_k,
]
and let (k(i)) denote the maximizing facet assigned to observation (i).
For (K\geq2), define the minimum assignment margin
\max_{k\ne k(i)}s_{ik}
\right].
}
]
If (\gamma>0), every observation has a unique maximizing facet.
By continuity, there exists a neighborhood of the fitted parameters in which the assignments remain unchanged.
This can be expressed quantitatively. If a parameter perturbation changes every individual facet score by at most (\delta), then assignment stability is guaranteed whenever
[
2\delta<\gamma.
]
For example, with parameters (\theta_k=(w_k,\beta_k)) and augmented observation vectors (\tilde u_i=(u_i,-1)), a sufficient condition is
[
\max_k|\Delta\theta_k|_2
<
\frac{\gamma}
{2\max_i|\tilde u_i|_2}.
]
This gives an explicit sufficient radius for an assignment-stable neighborhood.
It would be useful to state this result as a lemma because it connects the geometric representation directly to the algorithm's optimization properties.
3.1.3. Establish a conditional local optimality proposition
The preceding observations support a useful proposition that could be included immediately after the multi-facet algorithm.
Proposition — Assignment-Stable Local Optimality
Consider the unpenalized multi-facet mean-slack objective, with facet offsets constrained by
[
\beta_k=J_\tau(w_k;U).
]
Suppose that:

1. Every observation has a unique maximizing facet, with strictly positive minimum assignment margin.
2. Every fitted facet has a nonempty assigned observation set.
3. Every facet weight vector globally minimizes its corresponding convex fixed-assignment refitting objective over the simplex.
4. The multi-facet objective agrees with the corresponding fixed-assignment mean-slack expression throughout the assignment-stable neighborhood.

Then the combined parameter vector is a local minimizer of the multi-facet objective relative to a sufficiently small assignment-stable neighborhood of the constrained parameter space.
Proof outline.
A strictly positive assignment margin ensures that sufficiently small perturbations preserve the observation-to-facet assignments.
Within that neighborhood, the multi-facet objective therefore coincides with its fixed-assignment expression.
Under the stated offset constraint, this expression decomposes into a sum of convex facet-refitting objectives,
[
F(W)=
\sum_{k=1}^{K}
\frac{|C_k|}{N}
\left[
J_\tau(w_k;U)-\bar u_k^\top w_k
\right],
]
where (C_k) is the assigned observation set.
Since every (w_k) globally minimizes its corresponding convex component, the combined parameter vector minimizes the fixed-assignment objective.
Because this expression equals the full objective within the assignment-stable neighborhood, no sufficiently small admissible perturbation can decrease the full objective.
The result follows.
This proposition would give the manuscript a precise and defensible local optimality statement without requiring a global convergence theorem for the nonconvex multi-facet problem.
It should be made clear that the result is conditional on the objective and parameterization actually used. It does not automatically extend to tangent-based refits, reweighted penalties, freely varying offsets, or other algorithmic variants.
3.1.4. Provide an approximate optimality guarantee for numerical solutions
For practical computation, exact optimality of every convex subproblem is generally unrealistic.
Fortunately, the proposed first-order gap yields an immediately useful approximate certificate.
For the fixed-assignment objective, if each facet has first-order gap (G_k), then
[
\boxed{
F(W)-F_{\mathrm{fixed}}^*
\leq
\sum_{k=1}^{K}
\frac{|C_k|}{N}G_k(w_k).
}
]
This bound quantifies the maximum objective improvement available through reoptimization while retaining the same assignment structure.
With positive assignment margins, the same bound applies to sufficiently small parameter perturbations that remain in the assignment-stable neighborhood.
This is a more informative conclusion than simply reporting that an algorithm has converged within a numerical tolerance.
I recommend incorporating this certificate into the numerical results and reporting both the maximum per-facet gap and the weighted aggregate bound.
These quantities would provide a reproducible measure of optimization quality.
3.1.5. Distinguish descent, stationarity, and local optimality in the main theorem statements
The manuscript would benefit from separating its algorithmic results into three levels.
Descent. Under compatible assignment and refitting updates, accepted iterations do not increase the chosen objective.
Numerical stationarity. At termination, feasibility and first-order gaps satisfy explicitly reported thresholds, provided termination was not caused solely by the iteration cap.
Conditional local optimality. If exact refitting optimality and a positive assignment margin hold, then the parameters are locally optimal within the assignment-stable neighborhood under the stated objective and parameterization.
This separation would make the mathematical guarantees more precise and would resolve the principal concern identified by the computational audit.
I do not consider a proof of global convergence necessary for the present manuscript.
3.2. Clarify finite-temperature regularity and simplex-boundary optimality
The manuscript invokes geometric regularity assumptions involving balanced points and supporting facets with positive normals.
These assumptions are useful for interpreting hard-frontier geometry but do not necessarily imply interiority of the optimizer for a finite-temperature fitting problem.
The audit identifies a counterexample in which a balanced hard-support geometry coexists with a finite-temperature simplex-boundary solution.
The distinction arises because the finite-temperature objective depends on the empirical distribution and multiplicity of observations, whereas the hard minimax objective depends on their extreme support.
I recommend explicitly separating these two settings.
For an interior optimum, the familiar equal-gradient condition is appropriate. At a boundary optimum, however, the correct condition is
[
g_j\geq\lambda,
\qquad
w_j(g_j-\lambda)=0,
]
where (g=\nabla J_\tau(w)) and (\lambda=w^\top g).
The paper should state the complete simplex KKT conditions and reserve the equal-gradient interpretation for positive-weight coordinates.
This is a localized revision that would strengthen the mathematical treatment of sparse or inactive metric weights.
3.3. Distinguish a fitted reference surface from a physical Pareto frontier
The finite-temperature normalization
[
\beta=J_\tau(w^*)
]
does not generally produce a supporting hyperplane containing every observed design on the same side.
At finite temperature, some observations can satisfy
[
V(m_i)>1.
]
This behavior is a consequence of log-mean-exp smoothing rather than a failure of the model.
The manuscript should consistently distinguish:

* The smooth fitted reference surface.
* The hard empirical supporting envelope.
* The true Pareto boundary of the physically feasible engineering set.

These objects may be closely related under suitable assumptions, but their equivalence is not established by the fitting construction alone.
The soft-frontier interpretation is valuable and should be retained, provided its guarantees are stated precisely.
3.4. Correct the multi-term normalization bounds
The generalized posynomial extension is well motivated, but the manuscript should reconcile the stated log-sum-exp bounds with the normalization used in the actual construction.
For
[
\Phi_K(u)=
\frac1\kappa
\log\sum_{k=1}^{K}e^{\kappa x_k(u)},
]
the correct inequalities are
[
\boxed{
\max_kx_k(u)
\leq\Phi_K(u)
\leq
\max_kx_k(u)+\frac{\log K}{\kappa}.
}
]
The executable derivation already uses the correct relationship.
The corresponding explanatory text should be corrected to avoid confusing normalized log-mean-exp and unnormalized log-sum-exp.
This change is straightforward but important for the interpretation of finite-temperature multi-facet level sets.
3.5. Clarify uniqueness, identifiability, and stability
The paper should distinguish existence of an optimizer, uniqueness of the exponent vector, and stability under perturbations of the observed data.
The compact simplex and continuity of the single-term objective establish existence.
Strict convexity restricted to the simplex tangent space is a sufficient condition for uniqueness, but uniqueness need not imply robustness when the objective is poorly conditioned.
The audit provides examples in which nearly correlated metrics, changes in temperature, or changes in the empirical observations substantially affect the fitted exponent vector even when objective values remain comparatively stable.
I recommend adding a short discussion of the restricted Hessian and its relationship to local sensitivity.
The authors should also specify numerical tolerances used to classify active or inactive exponents.
A coefficient treated as zero numerically should be distinguished from a coefficient that is mathematically zero at the exact optimizer.
These refinements would improve the credibility of engineering interpretations based on the identified active metric set.
3.6. State statistical conclusions at their demonstrated level
The Gaussian cumulant derivation is correct for the specified log-space noise model at the population-moment level.
However, a population cumulant identity does not automatically imply that the corresponding finite-sample logarithmic estimator is unbiased.
Additional uncertainty arises when the exponent vector is estimated from the same observations.
The manuscript should distinguish exact moment identities, finite-sample approximations, and statistical consistency claims.
A complete consistency theory is not required for publication of the present mathematical framework, but any claims of consistency should be accompanied by the relevant independence, integrability, and identifiability assumptions.
Likewise, a fitted normal should be interpreted as a feature of the conditioned empirical trade-space model, not automatically as a physically realizable or causal engineering exchange.
3.7. Resolve implementation and terminology inconsistencies
The audit identifies several localized issues worth correcting before publication.
The single-observation estimator shortcut returns uniform weights even in cases where these do not minimize the declared single-term objective.
The exact-zero metric convention also differs from the continuous limiting extension of a monomial when the corresponding exponent is zero.
The coordinate terminology should distinguish a uniform log-scaling coordinate from Euclidean signed distance unless an explicit metric is introduced.
Finally, global claims about chart-origin exclusion or universal vertex solutions should be qualified in light of explicit edge-interior counterexamples.
These issues appear straightforward to resolve through small implementation changes or clarification of conventions.
4. Suggested Presentation of the Revised Algorithmic Results
I recommend consolidating the optimization discussion into a short sequence of formal statements.
Lemma 1 — Convexity and first-order certification of facet refits.
Establish convexity of each fixed-assignment facet-refitting objective and define its simplex first-order gap. State the resulting objective-suboptimality bound.
Lemma 2 — Existence of an assignment-stable neighborhood.
Show that a strictly positive assignment margin guarantees a nonempty neighborhood in which all maximizing facet assignments remain unchanged. Provide an explicit sufficient radius.
Proposition 3 — Assignment-stable local optimality.
Establish that exact solutions of the nonempty convex facet-refitting subproblems yield a local minimizer of the full unpenalized mean-slack objective when the assignments remain fixed and the offset constraints are maintained.
Corollary 4 — Approximate local optimality certificate.
Use the per-facet first-order gaps to bound the objective improvement possible within the fixed-assignment region.
Algorithmic stopping declaration.
Specify the numerical feasibility, first-order, assignment, and objective-change tolerances, and require the implementation to distinguish certified convergence from iteration-limit termination.
This organization would make the relationship between the analytical derivations and the numerical algorithm considerably clearer.
It would also give future work a natural foundation for studying more general convergence behavior, statistical stability, and the interaction between assignments and fitted facet geometry.
The proposed additions are tightly connected to mathematical properties already established in the manuscript and should not require substantial restructuring of the framework.
5. Assessment of Revision Scope
The requested revisions are important, but their scope is limited and well defined.
The main mathematical framework is already supported by a coherent body of derivations and computational tests.
The principal additional theoretical work is to formulate the optimization guarantees at the correct level of generality.
In particular, I would not require the authors to establish global convergence for the multi-facet algorithm or global identifiability of the engineering frontier.
The appropriate publication standard is to provide accurate local guarantees, transparent numerical certificates, and clearly delineated assumptions.
The assignment-stable local optimality proposition offers an achievable way to meet this standard.
It strengthens the contribution by replacing potentially ambiguous convergence language with a verifiable mathematical statement.
Similarly, the other requested changes concern normalization conventions, boundary cases, finite-temperature interpretation, and the scope of statistical claims.
They can be addressed through concise corrections and qualifications without changing the central scientific contribution.
6. Final Recommendation
This manuscript presents a promising and mathematically disciplined framework for engineering trade-space identification.
Its principal strengths are the homogeneous monomial construction, the convex single-term estimation problem, the invertible log-ratio coordinate representation, and the natural extension to generalized posynomial geometry.
The systematic use of executable derivations and independent computational verification further strengthens confidence in the mathematical development.
The central revision I recommend is a precise treatment of the relationship between numerical stopping, first-order optimality, and local optimality.
By introducing a first-order gap certificate and an assignment-stable neighborhood theorem, the authors can make their convergence claims rigorous without undertaking an unnecessarily broad global convergence analysis.
The remaining revisions are largely corrections of theorem scope, normalization, boundary conventions, and interpretation.
These are meaningful but manageable refinements that would improve the manuscript's clarity and mathematical reliability.
I believe the work is suitable for publication after these revisions.
Final recommendation: Accept with Minor Revisions.

(Two display formulas in 3.1.1 and 3.1.2 arrived truncated in the paste, at the explicit expression
of $G_k$ and at the definition of the margin $\gamma$; the index above completes them from the
surrounding text: $G_k(w_k)=\nabla f_k(w_k)^\top w_k-\min_j[\nabla f_k(w_k)]_j$ and
$\gamma=\min_i\big[s_{i,k(i)}-\max_{k\ne k(i)}s_{ik}\big]$.)
