# Abstract, working copy (his review, 2026-11-15)

One sentence per line. Edit here; the integration pass writes it back into `paper/paper.ipynb`.

A trade study must produce an answer and a justification an accountable decision-maker can follow.
Machine learning techniques can make principled scientific workflows scalable, reproducible and interpretable.
For example, principal component analysis (PCA) identifies basis vectors which explain the variance in a dataset.
Our method, hyperbolic trade space (HTS), explains trade-offs in a dataset of designs and measurements of their performance on real-valued attributes.
Trade-offs trace piecewise hyperbolic frontiers: in order to get more of one objective, we must tolerate less of another.
When supplied with a dataset we first condition the attributes into metrics that are strictly positive and "all else being equal, more is better." We do not assume the design space is well behaved, as it is often a mix of categorical and numerical values, on different scales and with different units.
While we apply conditioning to ensure the solvers behave in practice, we do not make strong assumptions about the sampling distribution, only that the frontier is log-convex.
To discover trade-offs among many designs and many metrics, we define the family of hyperbolic trade spaces by the level sets of a posynomial function of the metrics.
The monomial case is a convex optimization problem, and the posynomial case is compatible with generalized geometric programming.
Like PCA, HTS is an unsupervised learning method: PCA fits a subspace and projects the data onto it; HTS fits a surface one dimension below the data and places each design by its position on it and its level above or below that surface.
By assuming this hyperbolic shape and solving for the "energy" level sets, the resulting fit describes the trade-off space.
Expanding on the concept of a dilemma or trilemma, a monomial term in n metrics characterizes an n-lemma ("nye-LEM-uh").
Pareto improvements increase energy, and a design that maximizes energy is Pareto-efficient.
White space within an occupied level set may be an under-explored region of the design space.
The paper provides a literature review, formal results and a worked example to demonstrate HTS's applicability to decision analysis.
Our proofs are scripted with SymPy, and HTS is implemented with a scikit-learn-compatible API, so it integrates with existing pipelines and tools.
The worked example is a cubesat design optimization problem.
The underlying design problem is characterized by a SysML v2 model, and a simulation study scores each design on thirteen metrics.
High-dimensional n-lemmas are detected and used to inform a design decision by stakeholders who care primarily about cost and performance, without losing the thread back to the source designs.
A point of the trade space pulls back to the design that produced it; a point without data is a conjecture about a design, proposed by a rule and settled by building and measuring it.
Future work has three thrusts: (1) searching the design space for designs that push the frontier outward, (2) finding and filling the holes within it by topological data analysis, and (3) formal verification and performance, moving beyond Python into Rust and using theorem provers.
