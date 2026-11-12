# WP36 spike W2: what the estimator needs from a solver, what Rust has, Rust verification tools, WebAssembly

Reading and writing only: nothing built, no change to mathematics, code or claims. Sources read 2026-11-12;
every external statement carries its URL in the sources list at the end (S-n). "Extrapolation" marks what
follows from sources but was not stated by them or run. The lemma scripts remain the pencil-and-paper check,
not formal verification.

## 1. What the estimator asks of a solver (read from `src/hyperbolic_trade_space/solvers.py`)

| Fit | Problem | Call in the code today | Output the package uses |
|---|---|---|---|
| tau = inf (`solve_lp`) | LP: min t s.t. U w <= t 1, sum w = 1, w >= min_exponent; d + 1 variables, N inequality rows, 1 equality | `scipy.optimize.linprog(..., method="highs")` | primal w and t; the N inequality duals (`res.ineqlin.marginals`), which become the support weights p |
| finite tau, one term (`solve_slsqp`) | min J_tau(w) = (1/tau) log((1/N) sum exp(tau w.u_i)) on the simplex with floor; smooth convex, analytic gradient U^T p | `scipy.optimize.minimize(method="SLSQP", jac=True, bounds, one equality constraint)`, warm start from the LP, `ftol` 1e-10, `maxiter` 500 | w, J_tau, iteration count, success flag; then `_newton_polish` (reduced Newton, `POLISH_STEPS = 5`) |
| sparsity option | three rounds of SLSQP on J_tau + alpha sum w_j/(w_prev_j + eps) (reweighted L1) | the same `minimize` call | w with entries below 1e-8 zeroed |
| K > 1 (`solve_terms`, `_solve_terms_once`) | alternation: assign each row to its maximizing term, refit each term by the single-term fit on its cell; `n_restarts` = 5 default, seeded random starts (`sklearn.utils.check_random_state`) | the two calls above, inside a Python loop with a monotone guard (`GUARD_TOL`) | W (K x d), labels, `Termination` record |
| soft fit (finite `term_temperature`) | minimize the mean slack of a soft K-term model; reduced-Newton polish on the soft Hessian | `_refit_soft`, `_soft_polish`; Hessian and tangent basis by `scipy.linalg.eigh`, `null_space` | W, the second-order certificate (`soft_certificate`) |
| certificates (`simplex_gap`, `term_gap`, `assignment_margin`, `fixed_assignment_bound`) | closed-form residual and gap evaluations on a returned point; no optimization | numpy, `scipy.special.logsumexp`, `softmax` | `Termination` fields, tolerances `EPS_FEAS` 1e-9, `EPS_KKT` 1e-8 |

Other scipy uses outside the fit: `scipy.spatial.Delaunay`/`cKDTree` (gaps), `scipy.stats.rankdata`
(tensions), `scipy.ndimage` (plotting). The package declares `numpy`, `scipy`, `scikit-learn`, `pandas`,
`matplotlib`, `sympy` (`pyproject.toml`).

Problem sizes in the paper's case: the primary regime has N = 2,134 feasible designs of 3,000 and d = 13
traded metrics (`examples/adcs/k_terms.py` `ATTRS`; `docs/examples.md`; `paper/paper.ipynb`); K runs over
1, 2, 3 (`k_terms.py`). So the LP has 14 variables and 2,134 inequality rows; the smooth program has 13
variables and one equality. Both are small by solver standards; the weight is the many rows, and the
repetition (restarts x alternation steps x the tau and K scans).

Observation (extrapolation, from the code's structure): the solver is reachable only through `solve_lp` and
`solve_slsqp`, and every fit ends in the certificate functions, which test a returned point and do not care
how it was found. A different solver is therefore checkable by the package's own certificates.

## 2. What exists in Rust for each need

| Need | Candidate | What it gives (source) | What is missing or unknown |
|---|---|---|---|
| LP at tau = inf with duals | Clarabel.rs 0.11.1 (pure Rust; interior point; Apache-2.0) | LPs, QPs, SOCPs, SDPs and exponential, power and generalized-power cone problems (S-1, S-2); form min 1/2 x'Px + q'x s.t. Ax + s = b, s in K (S-2); solution struct carries `x`, `z` (dual vector), `s`, `status`, residuals, iterations (S-3); cones include `ZeroConeT`, `NonnegativeConeT`, `ExponentialConeT`, `PowerConeT` (S-4); good_lp says it implements the dual-value trait (S-5) | An interior-point dual is not a simplex vertex dual: the package's `p` are read from HiGHS (simplex or interior point with crossover; which one `linprog` uses was not read); whether the two agree on degenerate LPs (ties among rows) was not tested. Extrapolation: tie-heavy cases may differ in `p` while agreeing in `beta` |
| LP, pure Rust, WASM | microlp (fork of the archived minilp; no C dependencies; "can compile to WASM targets") | simplex-style LP, branch and bound for integers (S-6); good_lp lists it WASM-yes, fast-no (S-5); minilp itself archived 2022-09-22 with the warning "it will probably cycle, lose precision or panic on some harder problems" (S-7) | duals not documented in what was read; "fast: no" per good_lp; precision/cycling warning is the upstream minilp's, not shown to apply to the fork |
| LP, binding to HiGHS | `highs` crate (rust-or) | safe Rust bindings to the HiGHS solver (S-8); good_lp lists `highs` WASM-no, needs a C compiler (S-5) | no WASM build path stated; duals not shown in the README read |
| LP in the browser without Rust | highs-js (`highs` on npm): HiGHS C++ compiled to WebAssembly with Emscripten (S-9) | the same solver family as scipy's `method="highs"` | JavaScript, not Rust; maintenance status unclear (a registry page reports no release in 12 months, S-9) |
| Modelling layer | good_lp | one API over `clarabel`, `highs`, `microlp`, `coin_cbc`, `lpsolve`, `scip`, `cplex-rs`; exposes `SolutionWithDual` for Clarabel (S-5) | "none of the supported solvers provides a determinism guarantee" (S-5); LP/MILP only, nothing nonlinear |
| Convex program in GP form at finite tau | Clarabel exponential cone | the cone exists (S-1, S-4); the standard rewriting of "log-mean-exp <= t" into N exponential cones and one linear row is a mathematical fact | extrapolation, not run: with s_i >= exp(tau (w.u_i - t)) and sum s_i <= N, the program has N exponential cones (3N conic rows) plus N + d + 1 variables, here about 2,134 cones; time on this size was not measured. The package solves the same optimum by SLSQP today, so the interior-point route would be a different algorithm reaching the same minimizer, with accuracy set by Clarabel's tolerances, not `ftol` 1e-10 |
| SLSQP-class refit | `slsqp` crate (translation of NLopt's SLSQP, began as a c2rust transpilation, then hand-edited; 1.0.x) (S-10); `slsqp-rssl`, a port of SciPy's Fortran SLSQP whose author reports agreement with SciPy on Hock-Schittkowski problems "though results are not bit-identical" (S-10) | the algorithm the package uses now | WASM status of either not read; "not bit-identical to SciPy" is the portable-port outcome: the Rust fit would not reproduce the Python one to the last digit |
| General Rust optimization | argmin (pure Rust): line searches, trust region, L-BFGS, Newton, Gauss-Newton and others (S-11) | Newton and L-BFGS building blocks for the polish | the page read does not say whether it handles bounds or equality constraints; WASM not stated |
| Linear algebra for the polish and Hessian (eigh, null space) | not searched | | open: a Rust symmetric eigensolver and null space would be needed; not researched in this spike |
| K > 1 alternation, restarts, certificates | none to import | | to write (section 6) |

No Rust crate found in this spike offers the whole path (LP with duals, constrained smooth convex, alternation).
Clarabel alone could cover the LP and, by the exponential-cone rewriting, the single-term finite-tau program;
the alternation and the certificates are small loops over those calls plus closed-form evaluations.

## 3. Verification tools for Rust: what each guarantees

| Tool | Guarantee as the tool's own pages state it | Unbounded or bounded | Floating point, as far as the pages read say | Docs |
|---|---|---|---|---|
| Verus | "statically checks that the executable Rust code will always satisfy the specifications"; relies on solvers; supports "a subset of Rust (which we are working to expand)" (S-12); project goals: SMT-based (Z3), a subset easy to verify (S-13) | unbounded (static proof) | the guide's feature table lists "Floating point: Partially supported" (S-14); no statement on rounding, NaN or transcendental functions was found | https://verus-lang.github.io/verus/guide/ |
| Creusot | "verifies your code is safe from panics, overflows, and assertion failures"; with annotations, that it "does the correct thing"; translates to Coma, an intermediate language of Why3 (S-15) | unbounded (deductive) | the README read does not mention floating point; the guide page fetched returned only a fragment; nothing found | https://guide.creusot.rs |
| Kani | model checking: "will either prove the property, disprove the property (with a counterexample), or may run out of resources"; checks undefined behaviour, panics, arithmetic overflow, custom properties (S-16); the tool-comparison page classes it as bounded: "exhaustive (though often only up to some bound on input or problem size)" (S-17) | bounded | "supports floating point numbers, but some supported operations on floats are over-approximated" (trigonometric functions and `sqrt` named); "This makes Kani unsuitable for verifying some kinds of properties (e.g. precision) about numerical algorithms" (S-18). `exp` and `ln` are not named there | https://model-checking.github.io/kani/ |
| Prusti | "an automated program verifier for Rust, based on the Viper infrastructure"; by default proves absence of integer overflows and panics, plus user pre/postconditions and loop invariants (S-19, S-20); targets "a small fragment of Rust" (S-19) | unbounded (deductive) | nothing stated on floating point in the two pages read; the README calls it a "prototype verifier" (S-20); no maintenance statement read | https://prusti.github.io/prusti/user-guide/ |

What none of the four pages says: that a proof about the program's `f64` arithmetic gives an error bound on
`exp`, `ln` or a solver's iterates. The one explicit statement on numerics (Kani) says the tool is unsuited to
precision properties. Rust's own documentation says the precision of `f64::exp` and `f64::ln` "is
non-deterministic ... varies by platform, Rust version, and can even differ within the same execution" (S-21),
while `sqrt` is "guaranteed to be the rounded infinite-precision result" (S-21). Two consequences, stated as
the sources support them: (a) a Rust program that calls `exp` has no platform-independent bit result to
verify against; (b) what such tools can establish is the absence of panics and overflow, and any
functional property one writes down, about the operations as the tool models them. What they establish
about real-number mathematics (convexity, the bounds of the log-mean-exp) is a separate proof (the W1
question), not inherited from the program proof. Which tool proves what for this estimator was not tried.

## 4. What compiling to WebAssembly gives, and the Pyodide path

| Question | Finding | Source |
|---|---|---|
| Can Rust target the browser | `wasm32-unknown-unknown` is a Tier 2 target; `core` and `alloc` fully supported; threads panic (`std::thread::spawn`); `println!` does nothing | S-22 |
| Does Clarabel build for wasm | Clarabel.rs changelog: 0.9.0 "Add wasm feature"; 0.10.0 "wasm as platform dependency"; good_lp's table marks the Clarabel backend WASM-yes | S-23, S-5 |
| Speed vs native | measured on SPEC CPU benchmarks, 2019: WebAssembly "run slower by an average of 45% (Firefox) to 55% (Chrome)", peak slowdowns 2.08x (Firefox) and 2.5x (Chrome) relative to native. This is a general-code figure from 2019 browsers; no figure for LP or conic solvers in WASM was found, so none is given for this estimator | S-24 |
| Speed vs the current Python path | not measurable from sources; the Python fit calls compiled HiGHS and SLSQP already, so the comparison is native compiled code against WASM compiled code. Extrapolation: no speedup claim is supportable; the case for WASM is placement (in the page), not speed | none |
| Floating-point semantics | the WebAssembly core spec: IEEE 754, round-to-nearest ties-to-even, no directed rounding, exceptions not observable; NaN payloads nondeterministic; `fma` is single-rounded and specified. Extrapolation: basic operations (+, -, *, /, sqrt) are therefore reproducible across engines; `exp` and `ln` are library code compiled in, so results follow the Rust or libm version linked, not the engine | S-25, S-21 |
| What it gives the docs | a fit in the reader's browser with no server: a Rust function behind JavaScript (via wasm-bindgen or similar); size and load time not measured | extrapolation |
| The alternative: Pyodide | Pyodide 314.0.7 lists scipy 1.18.0, numpy 2.4.6, scikit-learn 1.8.0, pandas 3.0.2, matplotlib 3.10.8, clarabel 0.11.1, highspy 1.13.1, cvxpy-base 1.8.2, micropip 0.11.1; not listed: cvxopt, osqp, ecos, scs. Constraints: no threading or multiprocessing, sockets non-functional, network through the browser | S-26, S-27 |

What runs today, bounded by what was read: every dependency the package declares except `sympy` is named in the
Pyodide list (sympy was not looked up here); the package's own code is Python. Not tested here: that the
package installs and fits in Pyodide, that `linprog(method="highs")` returns duals there, and the Python
version pin (`requires-python >=3.12,<3.13`) against the Python of Pyodide 314 (the release number suggests a
different Python; not verified). So the Pyodide path needs no second implementation and no new algorithm;
what it needs is a test run and possibly a relaxed pin. It carries scipy and its test of record, so it gives
the same numbers as the Python package, not Rust's. It does not give a formal-guarantee story, because the
numerical core is scipy's compiled code.

## 5. The two paths side by side

| | Pyodide (the existing package in the browser) | Rust to WASM (a new estimator core) |
|---|---|---|
| Second implementation to maintain | none | yes: fit, alternation, certificates |
| Same numbers as the Python package | yes, same scipy | no: different solvers (Clarabel interior point, or a ported SLSQP "not bit-identical"), different `exp`/`ln` library |
| In-browser fit for the docs | open, untested here | open, same |
| Verification tools can reach it | no (scipy's Fortran/C++) | yes, for panics, overflow and written properties (section 3), not for numerics |
| Speed | no figure | no figure for this problem (general WASM overhead in S-24) |
| What runs today | the list in S-26 | Clarabel builds for wasm per S-23; the estimator's loop does not exist in Rust |

## 6. What a second implementation costs (what must be written; no hours)

| Piece | Written how | Tested against what |
|---|---|---|
| `solve_lp` equivalent: build the (d+1)-variable, N-row problem for Clarabel (or microlp), return w, t, duals | new Rust | `solve_lp` outputs on the doctest and on the primary and stock regimes (beta equal to tolerance; p compared where the LP is non-degenerate) |
| Finite-tau single-term fit: exponential-cone form, or a ported SLSQP plus Newton polish | new Rust (the cone form is a rewriting of the objective; one of the two to choose) | `solve_slsqp` outputs; the package's `simplex_gap` at `EPS_KKT` |
| Alternation: assignment, per-term refit, monotone guard, restarts with a seeded generator | new Rust | `solve_terms` on the case; note the seed streams differ from numpy's `check_random_state`, so restarts do not reproduce, only the certified outcome can be compared |
| Soft fit: Hessian, tangent basis (eigh, null space), reduced-Newton polish | new Rust, needs a dense eigensolver | `soft_certificate` values |
| Certificate functions (`simplex_gap`, `term_gap`, `assignment_margin`, `fixed_assignment_bound`) | new Rust, closed form | exact formulas in the docstrings; the same fixtures |
| Estimator layer (`fit`, `transform`, `score_samples`), preconditioner, sklearn conformance | not required for the browser core; scikit-learn's contract is Python | the conformance suite stays on the Python side |
| JavaScript/WASM interface and a page that calls it | new | a browser test |
| Verification (optional, per section 3) | annotations and proofs in a chosen tool | the tool |

The shared specification already exists in part. The interface contract (`work-packages/interface-contract.md`,
manifest `interface-contract.toml`, asserted by `tests/test_interface_contract.py`) pins the public names, the
`Termination` field names and status strings, the tolerances `EPS_FEAS`, `EPS_KKT`, `GUARD_TOL`,
`POLISH_STEPS`, and the fitted attributes; it pins the configuration-to-attributes boundary and says it names
no tool. It does not pin numerical outputs, and it is a Python-package contract (importable names and
parameter names), so a Rust core would need its own pinned surface. Extrapolation for the decision: the
contract could carry a second section for a core (the solve inputs, the outputs, the status strings, the
tolerances), with the committed fixtures and the certificates as the cross-implementation tests; the
certificates (accepting any point that passes) are the natural acceptance test because they do not depend on
which solver found the point. The contract's role under this reading is the shared specification; the
equality of the two implementations is then checked per fixture, within the certificate tolerances, not
to the last digit.

## 7. Findings

1. The estimator needs three solver capabilities: an LP with duals at tau = inf (HiGHS via `linprog`), a smooth
   convex program on the simplex at finite tau (SLSQP plus Newton polish) and a Python alternation over them
   for K > 1; the paper's case is N = 2,134, d = 13, K <= 3, small.
2. Rust has Clarabel (pure Rust, LP and exponential cone, duals returned, a wasm feature since 0.9.0) which
   can cover the LP and, by a standard rewriting (not run here), the finite-tau program; the alternation, the
   certificates and a dense eigensolver have nothing to import and are to be written.
3. The Rust verification tools (Verus, Creusot, Kani, Prusti) give proofs about panics, overflow and written
   properties; none of the pages read gives an error bound for `exp`/`ln`, Kani says it is unsuitable for
   precision properties, and Rust documents `f64::exp` and `ln` precision as non-deterministic across
   platforms and versions.
4. WebAssembly gives a server-free fit in the docs and IEEE-754 basic arithmetic; the only speed figure with a
   source is the 2019 general-code slowdown of 45 to 55 percent against native; no figure for a solver exists
   in what was read, so no speed claim for this estimator is made.
5. Pyodide already lists scipy 1.18.0, scikit-learn 1.8.0, clarabel 0.11.1 and highspy 1.13.1, so the existing
   package may reach the browser with no second implementation (untested here; the Python pin and an install
   test are the open items); a Rust core costs a second implementation to keep equal to the Python one,
   with the interface contract and the certificates as the shared specification.

## Sources

- S-1 Clarabel.rs repository README: https://github.com/oxfordcontrol/Clarabel.rs
- S-2 Clarabel documentation: https://clarabel.org/stable/
- S-3 DefaultSolution: https://docs.rs/clarabel/latest/clarabel/solver/implementations/default/struct.DefaultSolution.html
- S-4 SupportedConeT: https://docs.rs/clarabel/latest/clarabel/solver/enum.SupportedConeT.html
- S-5 good_lp README (solver table, determinism, Clarabel duals): https://raw.githubusercontent.com/rust-or/good_lp/main/README.md and https://docs.rs/good_lp/latest/good_lp/
- S-6 microlp: https://github.com/Specy/microlp/ and https://docs.rs/crate/microlp/0.4.0
- S-7 minilp (archived 2022-09-22): https://github.com/ztlpn/minilp
- S-8 highs crate: https://github.com/rust-or/highs
- S-9 highs-js / npm `highs`: https://github.com/lovasoa/highs-js and https://www.npmjs.com/package/highs
- S-10 slsqp crate and slsqp-rssl: https://docs.rs/crate/slsqp/latest and https://docs.rs/slsqp (slsqp-rssl: https://rust-digger.code-maven.com/crates/slsqp-rssl); read through a search summary, not the pages themselves
- S-11 argmin: https://argmin-rs.github.io/argmin/argmin/
- S-12 Verus repository: https://github.com/verus-lang/verus
- S-13 Verus project goals: https://raw.githubusercontent.com/verus-lang/verus/main/source/docs/project-goals.md
- S-14 Verus guide, feature table (Floating point: Partially supported): https://verus-lang.github.io/verus/guide/
- S-15 Creusot repository: https://github.com/creusot-rs/creusot
- S-16 Kani book: https://model-checking.github.io/kani/
- S-17 Kani tool comparison: https://github.com/model-checking/kani/blob/main/docs/src/tool-comparison.md
- S-18 Kani Rust feature support, floating point: https://github.com/model-checking/kani/blob/main/docs/src/rust-feature-support.md
- S-19 Prusti project page: https://www.pm.inf.ethz.ch/research/prusti.html
- S-20 Prusti README: https://github.com/viperproject/prusti-dev
- S-21 Rust `f64::exp` / `ln` / `sqrt`: https://doc.rust-lang.org/std/primitive.f64.html
- S-22 wasm32-unknown-unknown target: https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html
- S-23 Clarabel.rs changelog: https://raw.githubusercontent.com/oxfordcontrol/Clarabel.rs/main/CHANGELOG.md
- S-24 Jangda et al., Not So Fast, USENIX ATC 2019: https://www.usenix.org/conference/atc19/presentation/jangda
- S-25 WebAssembly core spec, numerics: https://webassembly.github.io/spec/core/exec/numerics.html
- S-26 Pyodide packages: https://pyodide.org/en/stable/usage/packages-in-pyodide.html
- S-27 Pyodide constraints: https://pyodide.org/en/stable/usage/wasm-constraints.html

None of these has a DOI; each is a stable project or documentation URL (S-24 is a conference paper page). The
sources are for the spike's readout; nothing here is entered in `docs/references.bib`.
