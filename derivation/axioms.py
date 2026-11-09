"""The axiom manifest: single source of truth for what the derivation assumes.

Tags:
  POSITED     - a modelling choice we declare (A0-A6).
  INHERITED   - an external theorem we USE and CITE but do not prove here (I1-I9).
  REGULARITY  - a condition the interpretation rests on (R1). Hypotheses are interpretive
                conditions, not defects: each states what it buys (``role``) and what the
                interpretation loses when it fails (``failure_mode``).

``fallback=True`` marks a hypothesis or inherited axiom introduced because a step resisted
abstract simplification (scope R-10). Fallbacks never replace a proof by enumeration; they are
listed in the FALLBACKS section and the HEADLINE. Lemma authors add such entries to ``AXIOMS``
with non-empty ``role`` and ``failure_mode``.

A0 is a structural axiom licensing the sizes d, n, K and the index symbols; it is not required
to be cited by a lemma (see ``STRUCTURAL``).
"""

import hashlib
from dataclasses import dataclass

import sympy as sp
from sympy.logic.inference import satisfiable
from sympy.matrices.expressions import Identity, OneMatrix, ZeroMatrix
from sympy.stats import Normal

from derivation.licence import LicenceError, _atoms_sigs, _is_positive, _sig, log_expand
from derivation.symbols import make_symbols

POSITED = "POSITED"
INHERITED = "INHERITED"
REGULARITY = "REGULARITY"
TAGS = (POSITED, INHERITED, REGULARITY)

# Axioms licensing symbol assumptions only; exempt from the every-axiom-is-used test.
STRUCTURAL = ("A0",)

# Inherited results cited as context that no proof step consumes (WP10 Amendment 2, principle 4):
# a recorded remark or an interpretation, not a premise of any lemma. Reported apart in the audit
# and exempt from the every-axiom-is-used test, as SOLVER_LEVEL is; each is listed with its reason.
CITED_CONTEXT = {
    "I2": "L5 records it as a remark on the consistency of the sample LME; no step of L5 uses it",
    "I3": "L5 records it as a remark on the support function; no step of L5 uses it",
    "I4": "L10 shows exp(kappa Phi_K) is a sum of monomials with positive coefficients, which is "
    "the definition of a posynomial; GP-compatibility is the cited reading, not a premise",
}

# Inherited results that license the K > 1 solver, not a lemma premise: reported in the ledger
# under their own heading and exempt from the every-axiom-is-used test (no lemma consumes them).
SOLVER_LEVEL = ("I7",)


# ----------------------------------------------------------------------------------------
# SymPy forms. Each entry that has a useful SymPy form declares it ONCE, here, on the shared
# symbols of ``derivation/symbols.py`` (abstract d, n, K); a lemma script takes the entry by
# name (``from derivation.axioms import A2``) and APPLIES it (``A2.rewrite(expr)``,
# ``A1.force_log(expr)``, ``I8.slack_expr(...)``, ``F12.invoke(m)``) instead of writing the
# form itself. An entry with no useful SymPy form is a named proposition (``proposition=True``):
# it still carries its statement and citation, and a step applies it by ``invoke``.
# ----------------------------------------------------------------------------------------
_S = make_symbols()
_j, _i, _k = _S.j, _S.i, _S.k
_RAW = sp.IndexedBase("r")  # raw attribute r_j of the conditioning (L9); a_j + r_j > 0
_NOISE = Normal("X", 0, _S.sigma)  # one noise variable eps_j ~ N(0, sigma^2) (A5)
_QMAT = sp.MatrixSymbol("Q", _S.d, _S.d)  # a square real matrix (I6)
_ONE = OneMatrix(_S.d, 1)  # the all-ones column 1 of the chart (A7)
_f_v, _f_w, _gdv = sp.symbols("f_v f_w g_dv", real=True)  # I8: f(v), f(w), g.(v - w)
_ab, _na, _nb = sp.symbols("a_dot_b norm_a norm_b", real=True)  # I9: a.b, ||a||, ||b||
_xk = sp.IndexedBase("xk")  # F10: the K scores x_k
_k0 = sp.Symbol("k0", integer=True)
_gj = sp.IndexedBase("g")  # F12: the family g_j whose minimum is m
_mmin = sp.Symbol("m", real=True)
_j0 = sp.Symbol("j0", integer=True)
_gamma = sp.Symbol("gamma", real=True)  # R2: the assignment margin
_Mrow = sp.IndexedBase("Mx")  # R2: M_i, the maximum score of row i over the facets
_srow = sp.IndexedBase("sfix")  # R2: s_i,k(i), the score of row i on its maximizing facet
_PV, _DV = sp.symbols("v_primal v_dual", real=True)  # I1: the optimal LP primal and dual values
_MSUM = sp.Symbol("Mgf_sum", real=True)  # I5: the MGF of the independent sum
_MG1 = sp.Function("Mgf1")  # I5: the single-variable MGF, applied at tau w_j

_gr = sp.IndexedBase("gr")  # I10: the gradient components g_j of the objective at the minimizer
_lam = sp.Symbol(
    "lambda", real=True
)  # I10: the multiplier of the equality constraint sum_j w_j = 1
_mu = sp.IndexedBase("mu", nonnegative=True)  # I10: the multipliers of w_j >= 0
_P_LINE = sp.Symbol("second_derivative_nonneg_on_every_line")  # I11 premise
_Q_CONVEX = sp.Symbol("convex")  # I11 conclusion
_GP_OBJ = sp.Symbol("objective_is_posynomial")  # I13 premises and conclusion
_GP_EQ = sp.Symbol("equalities_are_monomial_equal_one")
_GP_INEQ = sp.Symbol("inequalities_are_posynomial_at_most_one")
_GP_STD = sp.Symbol("geometric_program_in_standard_form")
_chi = sp.IndexedBase("chi", nonnegative=True)  # A8: chi[k, i] = 1 when row i lies in cell k
_ncell = sp.IndexedBase("ncell")  # A8: n_k, the number of rows of cell k
_NROWS = sp.Symbol("N", integer=True, positive=True)  # A8: the number of rows

_GT, _GE, _LE = sp.StrictGreaterThan, sp.GreaterThan, sp.LessThan


def _rule_one(expr, rel):
    """Rewrite ``expr`` by the equation ``rel`` (left side to right side)."""
    lhs, rhs = rel.lhs, rel.rhs
    if isinstance(lhs, sp.Indexed):  # u[j] = log m[j] holds for every index
        return expr.replace(
            lambda e: isinstance(e, sp.Indexed) and e.base == lhs.base,
            lambda e: rhs.xreplace(dict(zip(lhs.indices, e.indices, strict=True))),
        )
    out = expr.subs(lhs, rhs)
    # the relation holds for every index: also inside a Sum whose bound variable is the relation's
    return out.replace(
        lambda e: isinstance(e, sp.Sum),
        lambda e: sp.Sum(e.function.subs(lhs, rhs), *e.limits),
    )


@dataclass(frozen=True)
class Axiom:
    name: str
    tag: str
    statement: str  # human-readable claim
    relation: object = None  # the SymPy form: one relation or a tuple of relations, shared symbols
    objects: tuple = ()  # (key, SymPy object) pairs the entry declares (e.g. the noise variable)
    proposition: bool = False  # True: no useful SymPy form, declared as a named proposition
    citation: str = ""  # required for INHERITED
    role: str = ""  # interpretive role: what the condition buys for interpretation
    failure_mode: str = ""  # what the interpretation loses when it does not hold
    fallback: bool = False  # introduced because a step resisted abstract simplification

    def __str__(self):
        cite = f"  [{self.citation}]" if self.citation else ""
        return f"{self.name} ({self.tag}): {self.statement}{cite}"

    # ---- the form -------------------------------------------------------------------------
    def relations(self):
        """The entry's SymPy relations as a tuple (empty for a named proposition)."""
        if self.relation is None:
            return ()
        return (
            tuple(self.relation) if isinstance(self.relation, (tuple, list)) else (self.relation,)
        )

    def has_form(self):
        """True when the entry declares a SymPy form or is declared as a named proposition."""
        return bool(self.relations() or self.objects or self.proposition)

    def obj(self, key):
        """A SymPy object the entry declares (A5's noise variable)."""
        return dict(self.objects)[key]

    def fingerprint(self):
        """Stable text hash of the entry's statement, citation and SymPy form."""
        parts = [self.name, self.tag, self.statement, self.citation, str(self.proposition)]
        parts += [sp.srepr(r) for r in self.relations()]
        parts += [f"{key}={sp.srepr(val)}" for key, val in self.objects]
        return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()

    # ---- applying the entry in a proof step -------------------------------------------------
    def rewrite(self, expr, rename=None, only=None):
        """Apply the entry's equations to ``expr`` as rewrite rules (left side to right side).

        ``rename`` maps a symbol or family of the form to the one the proof uses (for example
        the simplex family w to a nonnegative stand-in family wn); ``only`` selects equations by
        position.
        """
        for position, rel in enumerate(self.relations()):
            if isinstance(rel, sp.Eq) and (only is None or position in only):
                expr = _rule_one(expr, rel.xreplace(rename) if rename else rel)
        return expr

    def entails(self, facts, goal):
        """True iff the entry's relations and the ``facts`` (Boolean) logically force ``goal``:
        a propositional step that SymPy checks by showing the negated goal unsatisfiable."""
        premises = [r for r in self.relations() if isinstance(r, (sp.Implies, sp.Equivalent))]
        return not satisfiable(sp.And(*premises, *facts, sp.Not(goal)))

    def rule(self, index):
        """(left side, right side) of the entry's ``index``-th equation."""
        rel = self.relations()[index]
        return rel.lhs, rel.rhs

    def positive_sigs(self):
        """Signatures of the atoms this entry declares positive (relations ``x > 0``)."""
        return {_sig(r.lhs) for r in self.relations() if isinstance(r, _GT) and r.rhs == 0} - {None}

    def real_sigs(self):
        """Signatures of the atoms this entry declares real: those in an ordering relation or in
        an equation with a logarithm (log of a declared-positive quantity)."""
        out = set()
        for r in self.relations():
            if isinstance(r, (_GT, _GE, _LE)) or (isinstance(r, sp.Eq) and r.has(sp.log)):
                out |= _atoms_sigs(r.lhs) | _atoms_sigs(r.rhs)
        return out - {None}

    def force_log(self, expr, *also):
        """``expand_log(expr, force=True)``, licensed by this entry (and ``also``)."""
        return log_expand(expr, self, *also)

    def positive(self, x):
        """``x`` itself, taken as positive on this entry's licence (``LicenceError`` if the entry
        does not declare it)."""
        if not _is_positive(x, [self]):
            raise LicenceError(f"{self.name} does not declare {x} positive")
        return x

    def real_base(self, name):
        """A real-valued family of the kind this entry declares real (A1: the log-metrics)."""
        if not self.real_sigs():
            raise LicenceError(f"{self.name} declares nothing real")
        return sp.IndexedBase(name, real=True)

    def positive_symbol(self, name):
        """A positive symbol standing for a quantity this entry declares positive."""
        if not any(isinstance(r, _GT) for r in self.relations()):
            raise LicenceError(f"{self.name} declares nothing positive")
        return sp.Symbol(name, positive=True)

    def nonneg_symbol(self, name):
        """A nonnegative symbol for a slack or quantity this entry declares nonnegative."""
        if not any(isinstance(r, (_GT, _GE, _LE)) for r in self.relations()):
            raise LicenceError(f"{self.name} declares no inequality")
        return sp.Symbol(name, nonnegative=True)

    def specialize(self, **funcs):
        """The right side of the entry's equation with its undefined functions replaced
        (``I5.specialize(Mgf1=lambda arg: ...)``): the entry applied to a concrete instance."""
        rel = next(r for r in self.relations() if isinstance(r, sp.Eq))
        return rel.rhs.replace(
            lambda e: isinstance(e, sp.core.function.AppliedUndef) and e.func.__name__ in funcs,
            lambda e: funcs[e.func.__name__](*e.args),
        )

    def slack_expr(self, **values):
        """lhs - rhs of the entry's inequality (>= 0 by the entry), at values given by name."""
        rel = next(r for r in self.relations() if isinstance(r, (_GE, _GT, _LE)))
        gap = rel.lhs - rel.rhs if isinstance(rel, (_GE, _GT)) else rel.rhs - rel.lhs
        return gap.subs({s: values[s.name] for s in gap.free_symbols if s.name in values})

    def slack_symbol(self, name):
        """A symbol for the entry's inequality slack: nonnegative (positive for a strict one)."""
        strict = any(isinstance(r, _GT) for r in self.relations())
        return sp.Symbol(name, positive=True) if strict else sp.Symbol(name, nonnegative=True)

    def nonneg_base(self, name):
        """A family x_j >= 0 declared by the entry (A2: w_j >= 0; F12: g_j - m >= 0)."""
        if not any(isinstance(r, _GE) and isinstance(r.lhs, sp.Indexed) for r in self.relations()):
            raise LicenceError(f"{self.name} declares no nonnegative family")
        return sp.IndexedBase(name, nonnegative=True)


AXIOMS = {
    # ---------------------------------------------------------------- POSITED
    "A0": Axiom(
        "A0",
        POSITED,
        "sizes: the dimension d, the sample count n and the term count K are positive "
        "integers, and the index symbols i, j, k are integers (structural; the lemmas are "
        "proved for symbolic d, n, K, not at chosen sizes)",
        proposition=True,
    ),
    "A1": Axiom(
        "A1",
        POSITED,
        "metrics are strictly positive, larger-is-better: m_i[j] > 0, so u = log m is defined",
        relation=(_GT(_S.m[_j], 0, evaluate=False), sp.Eq(_S.u[_j], sp.log(_S.m[_j]))),
    ),
    "A2": Axiom(
        "A2",
        POSITED,
        "the exponents w lie on the simplex: w_j >= 0 and sum_j w_j = 1",
        relation=(_S.simplex, _GE(_S.w[_j], 0, evaluate=False)),
    ),
    "A3": Axiom(
        "A3",
        POSITED,
        "the soft-maximum temperature is positive: tau > 0",
        relation=(_GT(_S.tau, 0, evaluate=False),),
    ),
    "A4": Axiom(
        "A4",
        POSITED,
        "conditioning is log-affine and invertible: log m_j = alpha_j log(a_j + s_j) + b_j "
        "with alpha_j != 0 (negative alpha_j marks a cost attribute)",
        relation=(
            sp.Eq(_S.u[_j], _S.alpha[_j] * sp.log(_S.a[_j] + _RAW[_j]) + _S.b[_j]),
            sp.Ne(_S.alpha[_j], 0),
            _GT(_S.a[_j] + _RAW[_j], 0, evaluate=False),
        ),
    ),
    "A5": Axiom(
        "A5",
        POSITED,
        "noise: eps_j are i.i.d. N(0, sigma^2), independent across j, with sigma > 0",
        relation=(_GT(_S.sigma, 0, evaluate=False),),
        objects=(("noise", _NOISE),),
    ),
    "A6": Axiom(
        "A6",
        POSITED,
        "the extension temperature is positive, kappa > 0, and each of the K terms has "
        "exponents theta_k on the simplex",
        relation=(
            _S.simplex_theta,
            _GE(_S.theta[_k, _j], 0, evaluate=False),
            _GT(_S.kappa, 0, evaluate=False),
        ),
    ),
    "A7": Axiom(
        "A7",
        POSITED,
        "the sum-zero chart: Z = B u with B a (d-1) x d matrix satisfying B B^T = I and "
        "B 1 = 0 (orthonormal rows spanning the sum-zero subspace; the Helmert basis is one "
        "realization)",
        role="makes Z the scale-free coordinates of the metric vector: Z is blind to a common "
        "multiplicative scale (a shift of u along 1), and with the log-scale it gives an "
        "isometric linear bijection, so Gaussian noise and distances can be read in Z",
        failure_mode="if B 1 != 0 the chart sees the overall scale and Z is not invariant; if "
        "B B^T != I the chart is not isometric, so noise in u is not isotropic in Z and "
        "distances in Z distort those in u",
        relation=(
            sp.Eq(_S.B * _S.B.T, Identity(_S.d - 1)),
            sp.Eq(_S.B * _ONE, ZeroMatrix(_S.d - 1, 1)),
        ),
    ),
    "A8": Axiom(
        "A8",
        POSITED,
        "the cells C_1..C_K partition the N rows: every row lies in exactly one cell "
        "(chi_ki = 1 when row i is in cell k, sum_k chi_ki = 1, chi_ki >= 0), and the cell "
        "counts n_k = sum_i chi_ki are at least 1 (every facet is nonempty)",
        relation=(
            sp.Eq(sp.Sum(_chi[_k, _i], (_k, 1, _S.K)), 1),
            _GE(_chi[_k, _i], 0, evaluate=False),
            sp.Eq(_ncell[_k], sp.Sum(_chi[_k, _i], (_i, 1, _NROWS))),
            _GE(_ncell[_k], 1, evaluate=False),
        ),
        objects=(("membership", _chi), ("count", _ncell), ("rows", _NROWS)),
    ),
    # -------------------------------------------------------------- INHERITED
    "I1": Axiom(
        "I1",
        INHERITED,
        "LP strong duality: min_{w in simplex} max_i w.u_i equals the dual max over "
        "lambda in the simplex of min_j (U^T lambda)_j (checked numerically in pytest)",
        citation="Boyd & Vandenberghe, Convex Optimization, section 5.2",
        relation=(sp.Eq(_PV, _DV),),  # the optimal primal and dual values coincide
        objects=(("primal", _PV), ("dual", _DV)),
    ),
    "I2": Axiom(
        "I2",
        INHERITED,
        "strong law of large numbers: sample means converge almost surely to the "
        "expectation (replication leaves J_tau unchanged; checked in pytest)",
        citation="Kolmogorov strong law of large numbers; Billingsley, Probability and Measure",
        proposition=True,
    ),
    "I3": Axiom(
        "I3",
        INHERITED,
        "a closed convex set is determined by its support function",
        citation="Rockafellar, Convex Analysis, section 13",
        proposition=True,
    ),
    "I4": Axiom(
        "I4",
        INHERITED,
        "softmax-affine (log-sum-exp of affine) functions are GP-compatible",
        citation="Hoburg, Kirschen & Abbeel, 2016, Data fitting with geometric-programming-"
        "compatible softmax functions",
        proposition=True,
    ),
    "I5": Axiom(
        "I5",
        INHERITED,
        "the moment generating function of a sum of independent random variables is the "
        "product of their moment generating functions (ledger addition to spec section 6)",
        citation="Billingsley, Probability and Measure, MGF of independent sums",
        relation=(
            sp.Eq(_MSUM, sp.Product(_MG1(_S.tau * _S.w[_j]), (_j, 1, _S.d))),
        ),  # M_{sum_j w_j eps_j}(tau) = prod_j M_{eps_j}(tau w_j)
    ),
    "I6": Axiom(
        "I6",
        INHERITED,
        "for a square real matrix Q, Q Q^T = I implies Q^T Q = I (a left inverse of a square "
        "matrix is also its right inverse)",
        citation="Horn & Johnson, Matrix Analysis, invertible matrices (the inverse is two-sided)",
        relation=(sp.Eq(_QMAT.T * _QMAT, Identity(_S.d)),),  # given Q Q^T = I, Q square
    ),
    "I7": Axiom(
        "I7",
        INHERITED,
        "alternating partition and refit converges to a local optimum of the max-affine "
        "(convex piecewise-linear) fitting problem: assign each point to its maximizing term, "
        "refit each term on its cell, repeat; the least-squares error is nonincreasing and "
        "the iteration terminates at a local optimum",
        citation="Magnani & Boyd, 2009, Convex piecewise-linear fitting, Optimization and "
        "Engineering 10(1), 1-17 (bib key magnani2009convex)",
        role="the convergence of the K > 1 solver: the hard-assignment (kappa = infinity) "
        "partition-and-refit loop stops at a local optimum rather than cycling",
        failure_mode="a poor local optimum: the limit depends on the initial partition, "
        "mitigated by restarts; a global optimum is not claimed",
        proposition=True,
    ),
    "I8": Axiom(
        "I8",
        INHERITED,
        "first-order convexity inequality: a differentiable convex f satisfies "
        "f(v) >= f(w) + grad f(w).(v - w) for all feasible v, w",
        citation="Boyd & Vandenberghe, Convex Optimization, section 3.1.3",
        role="turns the simplex first-order gap into an objective-error bound: "
        "0 <= f(w) - f* <= G, so a reported gap certifies how far a facet refit is from optimal",
        failure_mode="for a nonconvex objective (the penalized refit, a tangent refit) the "
        "inequality fails and a small gap certifies only first-order stationarity",
        relation=(_GE(_f_v, _f_w + _gdv, evaluate=False),),
    ),
    "I9": Axiom(
        "I9",
        INHERITED,
        "Cauchy-Schwarz inequality: for real vectors a and b, |a.b| <= ||a||_2 ||b||_2",
        citation="Horn & Johnson, Matrix Analysis, the Cauchy-Schwarz inequality",
        role="bounds the change of a facet score by the norm of the parameter change times the "
        "norm of the augmented design vector, which gives the explicit assignment-stable radius "
        "gamma / (2 max_i ||(u_i, -1)||_2)",
        failure_mode="none for real vectors in a Euclidean space; the radius is sufficient, not "
        "tight, because the inequality is attained only when the change is parallel to the "
        "design vector",
        relation=(_LE(sp.Abs(_ab), _na * _nb, evaluate=False),),
    ),
    "I10": Axiom(
        "I10",
        INHERITED,
        "first-order (KKT) necessary conditions at a local minimizer w of a continuously "
        "differentiable f on the simplex {w >= 0, sum_j w_j = 1}: there are lambda and mu_j >= 0 "
        "with "
        "g_j - lambda - mu_j = 0 (g = grad f(w)) and w_j mu_j = 0. The constraints are affine and "
        "their active gradients (the all-ones vector, and e_j for each w_j = 0) are linearly "
        "independent at every point of the simplex, so the linear independence constraint "
        "qualification holds and no convexity of f is used",
        citation="Nocedal & Wright, Numerical Optimization, 2nd ed., Theorem 12.1 (first-order "
        "necessary conditions) with Definition 12.4 (LICQ); for a convex f the same conditions "
        "are also Boyd & Vandenberghe, Convex Optimization, section 5.5.3, a remark and not the "
        "basis",
        role="turns stationarity of the soft-maximum objective on the simplex into the "
        "multiplier equations of L3: equal gradient components where no bound is active, and "
        "g_j >= lambda with complementary slackness in general",
        failure_mode="the conditions are necessary at a local minimizer of a continuously "
        "differentiable f for any such f, convex or not (the penalized refit, a tangent refit); "
        "at a non-minimizing stationary point they hold without being sufficient, and sufficiency "
        "needs convexity (L12)",
        relation=(
            sp.Eq(_gr[_j] - _lam - _mu[_j], 0),
            _GE(_mu[_j], 0, evaluate=False),
            sp.Eq(_S.w[_j] * _mu[_j], 0),
        ),
        objects=(("gradient", _gr), ("lambda", _lam), ("mu", _mu)),
    ),
    "I11": Axiom(
        "I11",
        INHERITED,
        "a function is convex if and only if its restriction to every line is convex, and a "
        "twice differentiable function of one variable is convex if and only if its second "
        "derivative is nonnegative: convexity is nonnegativity of the second derivative along "
        "every line",
        citation="Boyd & Vandenberghe, Convex Optimization, sections 3.1.1 (restriction to a "
        "line) and 3.1.4 (second-order conditions)",
        role="lets L4 conclude that J_tau is convex from the sign of its second directional "
        "derivative at an arbitrary point in an arbitrary direction",
        failure_mode="none for a twice differentiable function on an open convex domain, as "
        "J_tau is on R^d",
        relation=(sp.Equivalent(_P_LINE, _Q_CONVEX),),
        objects=(("premise", _P_LINE), ("conclusion", _Q_CONVEX)),
    ),
    "I12": Axiom(
        "I12",
        INHERITED,
        "complementary slackness of the LP pair at tau = infinity: the dual weights p are "
        "supported on the rows whose score attains the maximum M, p_i (M - s_i) = 0 for every "
        "row i, with s_i = w.u_i",
        citation="Boyd & Vandenberghe, Convex Optimization, section 5.5.2 (complementary "
        "slackness)",
        role="gives the termwise zero p_i (M - s_i) = 0 that turns the LP duality gap into the "
        "simplex gap G of a facet at tau = infinity",
        failure_mode="holds for an optimal primal-dual pair (and by construction for any p "
        "supported on the active rows); for a p with weight on a non-active row the gap is not G",
        relation=(
            sp.Eq(
                _S.p[_i] * (_S.M - sp.Sum(_S.w[_j] * _S.u[_i, _j], (_j, 1, _S.d))),
                0,
            ),
        ),
    ),
    "I13": Axiom(
        "I13",
        INHERITED,
        "a geometric program in standard form minimizes a posynomial f0(x) (a sum of monomials "
        "c x_1^a_1 ... x_n^a_n with coefficients c > 0 and real exponents) over positive x subject "
        "to f_i(x) <= 1 with f_i posynomial and g_i(x) = 1 with g_i a monomial; a constraint "
        "g1 = g2 of two monomials is the monomial g1 / g2 = 1. With y = log x, the problem "
        "minimizing log f0(e^y) subject to log f_i(e^y) <= 0 and log g_i(e^y) = 0 is its convex "
        "form",
        citation="Boyd, Kim, Vandenberghe & Hassibi, A tutorial on geometric programming, "
        "Optimization and Engineering 8(1), 2007, section 2.1 (monomial, posynomial), section 2.2 "
        "(standard form, problem (3)), section 2.3 (g1 = g2 as g1/g2 = 1) and section 2.5 "
        "(logarithmic change of variables, problem (6)); read in the authors' PDF "
        "https://web.stanford.edu/~boyd/papers/pdf/gp_tutorial.pdf",
        role="names the one-facet fit as a geometric program: L4 shows that its objective is a "
        "posynomial in x = exp(w) and its simplex constraints are monomial, so the fit is a "
        "geometric program in standard form and the problem in w is its convex form",
        failure_mode="holds for a program that meets all three premises; a negative coefficient, "
        "an exponent that depends on x, or a constraint that is not a posynomial bounded by one "
        "or a monomial equal to one leaves the program outside the class. It says nothing of "
        "several facets, where each design counts against its nearest facet (a minimum over "
        "facets): that fit is not a geometric program as a whole",
        relation=(sp.Equivalent(sp.And(_GP_OBJ, _GP_EQ, _GP_INEQ), _GP_STD),),
        objects=(
            ("objective", _GP_OBJ),
            ("equalities", _GP_EQ),
            ("inequalities", _GP_INEQ),
            ("conclusion", _GP_STD),
        ),
    ),
    # ------------------------------------------------------------- REGULARITY
    "R1": Axiom(
        "R1",
        REGULARITY,
        "the balanced point lies in the relative interior of a facet of the frontier with "
        "positive normal; this is a statement about the hard-support (tau = infinity) geometry "
        "and does not imply that the finite-tau minimizer of J_tau is interior",
        role="makes the KKT balanced point a genuine interior frontier point, so the "
        "gradient condition identifies w* as the facet normal and the improvement factors "
        "and elasticities can be read as trade-offs along the frontier; where the fitted "
        "minimizer has w_j > 0 the equal-gradient condition holds on those coordinates",
        failure_mode="at a vertex, an edge or a facet with a zero normal component the "
        "gradient condition holds only as a subgradient inclusion: w* is not unique, some "
        "elasticities are undefined, and the frontier reading degrades to the weaker "
        "invariant-form reading; at finite tau the multiplicity of the observations can put "
        "the minimizer on the simplex boundary even when the hard-support geometry is balanced, "
        "and then only the full simplex KKT (g_j >= lambda, w_j (g_j - lambda) = 0) holds, with "
        "equal gradients on the positive-weight coordinates only",
        relation=(_GT(_S.w[_j], 0, evaluate=False),),  # the balanced point has w_j > 0
    ),
    "R2": Axiom(
        "R2",
        REGULARITY,
        "positive assignment margin: gamma = min_i [s_i,k(i) - max_{k != k(i)} s_ik] > 0, where "
        "s_ik = w_k.u_i - beta_k, so every row has a unique maximizing facet",
        role="gives unique maximizing facets and an assignment-stable neighborhood (radius "
        "gamma / (2 max_i ||(u_i, -1)||_2)) on which the multi-facet objective equals its "
        "fixed-assignment expression, so Proposition 3 applies: a fit whose facets are exactly "
        "optimal is a local minimizer, and with gap-bounded facets Corollary 4 bounds the "
        "remaining improvement",
        failure_mode="ridge rows: a frontier row on two facet planes has margin zero at tau = "
        "infinity, and duplicate facets give identical scores; the neighborhood is then empty, "
        "Proposition 3 does not apply, and termination reports stationary_without_margin: the "
        "fit is first-order stationary per facet (levels 1 and 2) with no local-optimality claim",
        relation=(_GT(_gamma, 0, evaluate=False), sp.Eq(_Mrow[_i], _srow[_i])),
    ),
    # -------------------------------------------------- FALLBACK HYPOTHESES (L5, L10)
    "F5": Axiom(
        "F5",
        POSITED,
        "max representation for L5: the maximum of the scores is a symbol M with "
        "s_i <= M for all i in 1..n and s_{i0} = M for some i0 in 1..n",
        role="lets the tau -> infinity limit and the bound LME <= max be proved for symbolic n "
        "(sympy has no symbolic-n max and cannot take limits through the symbolic Sum): "
        "M - (log n)/tau <= LME <= M is squeezed with sympy.limit",
        failure_mode="the statement is about the actual maximum only when M really is "
        "max_i s_i; if M is any upper bound that is not attained the lower squeeze bound is "
        "lost and the limit is only an upper bound on the true limit",
        fallback=True,
        relation=(_LE(_S.s[_i], _S.M, evaluate=False), sp.Eq(_S.s[_S.i0], _S.M)),
    ),
    "F10": Axiom(
        "F10",
        POSITED,
        "max representation for L10: the maximum over the K terms of x_k = theta_k.u - beta_k "
        "is a symbol M with x_k <= M for all k in 1..K and x_{k0} = M for some k0 in 1..K",
        role="lets lim_{kappa->inf} Phi_K = max_k x_k and the bounds max <= Phi_K <= "
        "max + (log K)/kappa be proved for symbolic K (same squeeze as F5), so the extension "
        "reads as a soft maximum of K affine log-scores",
        failure_mode="as F5: if M is not attained by some term the lower bound Phi_K >= M "
        "is lost and only the upper bound M + (log K)/kappa on the limit is available",
        fallback=True,
        relation=(_LE(_xk[_k], _S.M, evaluate=False), sp.Eq(_xk[_k0], _S.M)),
    ),
    "F12": Axiom(
        "F12",
        POSITED,
        "min representation for L12 and L13: the minimum m of a finite family x_j (the gradient "
        "components g_j in L12, the row gaps in L13) is a symbol with x_j >= m for all j and "
        "x_{j0} = m for some j0",
        role="lets the simplex gap G = g.w - min_j g_j and the bound min_{v in simplex} g.v = m be "
        "proved for symbolic d (sympy has no symbolic-d min): g.v - m = sum_j v_j (g_j - m) >= 0, "
        "attained at the vertex e_{j0}",
        failure_mode="as F5: if m is only a lower bound that is not attained, g.v >= m holds but "
        "the minimum over the simplex may exceed m, and G = g.w - m is then an upper bound on "
        "the first-order gap rather than its value",
        fallback=True,
        relation=(_GE(_gj[_j], _mmin, evaluate=False), sp.Eq(_gj[_j0], _mmin)),
    ),
}


# Each ledger entry as an importable module-level name: a lemma script writes
# ``from derivation.axioms import A2, I8`` and applies the entry in the tagged step.
A0 = AXIOMS["A0"]
A1 = AXIOMS["A1"]
A2 = AXIOMS["A2"]
A3 = AXIOMS["A3"]
A4 = AXIOMS["A4"]
A5 = AXIOMS["A5"]
A6 = AXIOMS["A6"]
A7 = AXIOMS["A7"]
A8 = AXIOMS["A8"]
I1 = AXIOMS["I1"]
I2 = AXIOMS["I2"]
I3 = AXIOMS["I3"]
I4 = AXIOMS["I4"]
I5 = AXIOMS["I5"]
I6 = AXIOMS["I6"]
I7 = AXIOMS["I7"]
I8 = AXIOMS["I8"]
I9 = AXIOMS["I9"]
I10 = AXIOMS["I10"]
I11 = AXIOMS["I11"]
I12 = AXIOMS["I12"]
I13 = AXIOMS["I13"]
R1 = AXIOMS["R1"]
R2 = AXIOMS["R2"]
F5 = AXIOMS["F5"]
F10 = AXIOMS["F10"]
F12 = AXIOMS["F12"]


def get(name):
    return AXIOMS[name]


def fingerprints():
    """name -> stable hash of each entry's statement, citation and SymPy form."""
    return {name: a.fingerprint() for name, a in AXIOMS.items()}


def by_tag(tag):
    return [a for a in AXIOMS.values() if a.tag == tag]


def fallbacks():
    return [a for a in AXIOMS.values() if a.fallback]
