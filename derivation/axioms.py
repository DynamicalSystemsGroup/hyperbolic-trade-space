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
_Mrow = sp.IndexedBase("Mx")  # R2: M_i, the maximum score of row i over the terms
_srow = sp.IndexedBase("sfix")  # R2: s_i,k(i), the score of row i on its maximizing term
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

_JF_MEAN, _JMEAN_F = sp.symbols(
    "jen_f_of_mean jen_mean_of_f", real=True
)  # I14: f(sum th x), sum th f(x)
_JSLACK = sp.IndexedBase("jen_slack")  # I14: the slack of the instance with index i
_GG_BUILT = sp.Symbol("built_from_posynomials")  # I15 premise and conclusion
_GG_GENPOS = sp.Symbol("generalized_posynomial")
_SOS_KKT = sp.Symbol("kkt_conditions_hold_at_a_feasible_point")  # I16 premises and conclusion
_SOS_PD = sp.Symbol("lagrangian_hessian_positive_on_the_critical_cone")
_SOS_MIN = sp.Symbol("strict_local_minimizer")

_GT, _GE, _LE = sp.StrictGreaterThan, sp.GreaterThan, sp.LessThan

_SIGM = sp.IndexedBase("Sigma")  # A9: the entries Sigma[j, l] of the noise covariance
_l = sp.Symbol("l", integer=True)
_QV = sp.Symbol("q_form", positive=True)  # A9: the variance q = w'Sigma w of w.eps (case q > 0)
_LIN = Normal("Xlin", 0, sp.sqrt(_QV))  # A9: the combination w.eps as a centred normal variable
_RT = sp.IndexedBase("rt")  # A10: the measured raw attribute
_ZETA = sp.IndexedBase("zeta")  # A10: the log-error of the measurement of attribute j
_DEL = sp.IndexedBase("delta", positive=True)  # A10: the size delta_j of the log-error
_ZJ = Normal("Zj", 0, _DEL[_j])  # A10: one log-error zeta_j ~ N(0, delta_j^2)
_VROW = sp.Symbol("v_row", positive=True)  # A11: v, the standard deviation of one row's noise
_ZROW = Normal("Zrow", 0, _VROW)  # A11: one row's noise z_i ~ N(0, v^2)
_zr = sp.IndexedBase("z")  # F19: the row noise draws z_i
_Zm = sp.Symbol("Zm", real=True)  # F19: the maximum of the draws
_i0z = sp.Symbol("i0z", integer=True)
_JX_F, _JX_EF = sp.symbols("jx_f_of_mean jx_mean_of_f", real=True)  # I17: f(E X), E f(X)
_EX_LE_P, _EX_LE_Q = sp.symbols("jx_X_le_Y_almost_surely jx_EX_le_EY")  # I17 monotonicity
_RQ, _VV = sp.symbols("rq_form vv_norm2", real=True)  # R3: v'Cv and v'v for a tangent v
_M3 = sp.Symbol("m_curv", positive=True)  # R3: the smallest eigenvalue of C on the tangent space
_PIN_SOLVES = sp.Symbol("x_equals_pinv_X_times_b")  # I18 conclusion
_PIN_EQ = sp.Symbol("X_x_equals_b")  # I18 premises
_PIN_RANGE = sp.Symbol("x_in_range_of_X")


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
        "the fit temperature is positive: tau > 0",
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
        "the term temperature is positive, kappa > 0, and each of the K terms has "
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
        "counts n_k = sum_i chi_ki are at least 1 (every cell is nonempty)",
        relation=(
            sp.Eq(sp.Sum(_chi[_k, _i], (_k, 1, _S.K)), 1),
            _GE(_chi[_k, _i], 0, evaluate=False),
            sp.Eq(_ncell[_k], sp.Sum(_chi[_k, _i], (_i, 1, _NROWS))),
            _GE(_ncell[_k], 1, evaluate=False),
        ),
        objects=(("membership", _chi), ("count", _ncell), ("rows", _NROWS)),
    ),
    "A9": Axiom(
        "A9",
        POSITED,
        "noise with a covariance: the noise vector eps is a Gaussian vector with mean 0 and a "
        "symmetric positive semi-definite covariance Sigma, so every linear combination w.eps is a "
        "centred normal variable with variance q = w'Sigma w = Sum_j Sum_l w_j Sigma_jl w_l >= 0 "
        "(the definition of a Gaussian vector); Sigma = sigma^2 I is A5",
        role="lets the noise of the conditioned metrics have unequal levels and correlations "
        "(A5 asks for one sigma in every metric), so the offset shift of L6 is read for the noise "
        "the fit actually sees",
        failure_mode="a noise that is not jointly Gaussian (heavy tails, a skewed or bounded "
        "error) has a different cumulant: the identity of L18 is a statement about the Gaussian "
        "vector only",
        relation=(
            sp.Eq(
                _QV,
                sp.Sum(sp.Sum(_S.w[_j] * _SIGM[_j, _l] * _S.w[_l], (_l, 1, _S.d)), (_j, 1, _S.d)),
            ),
            _GE(_QV, 0, evaluate=False),
            sp.Eq(_SIGM[_l, _j], _SIGM[_j, _l]),
        ),
        objects=(("lin", _LIN), ("cov", _SIGM)),
    ),
    "A10": Axiom(
        "A10",
        POSITED,
        "multiplicative measurement error: the measured raw attribute rt_j of a true value "
        "r_j > 0 has log rt_j = log r_j + zeta_j, the log-errors zeta_j are independent "
        "N(0, delta_j^2) with delta_j > 0 (to first order a relative error of size delta_j); "
        "one delta for every attribute is the equal-error case",
        role="turns a measurement error stated on the raw attribute into additive noise in the "
        "log space where the model works, so the map to the noise the fit sees is an exact "
        "linear one under log-affine conditioning",
        failure_mode="an error that is additive on the raw attribute, or not independent across "
        "attributes, is not covered: it needs its own map to the conditioned noise",
        relation=(
            sp.Eq(sp.log(_RT[_j]), sp.log(_RAW[_j]) + _ZETA[_j]),
            _GT(_RAW[_j], 0, evaluate=False),
            _GT(_DEL[_j], 0, evaluate=False),
        ),
        objects=(("zeta", _ZJ),),
    ),
    "A11": Axiom(
        "A11",
        POSITED,
        "row noise: the noise z_i = w.eps_i that the weighted metrics of row i carry are "
        "independent N(0, v^2) across the rows i = 1..n with v > 0 (v^2 = sigma^2 ||w||^2 under "
        "A5 and I5, and v^2 = w'Sigma w under A9)",
        role="lets the soft maximum of the noisy scores be compared with that of the clean scores "
        "through the single number v",
        failure_mode="noise that is shared across rows (a common offset), heteroscedastic or not "
        "Gaussian changes the moment generating function the bound uses",
        relation=(_GT(_VROW, 0, evaluate=False),),
        objects=(("noise", _ZROW),),
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
        "0 <= f(w) - f* <= G, so a reported gap certifies how far a term refit is from optimal",
        failure_mode="for a nonconvex objective (the penalized refit, a tangent refit) the "
        "inequality fails and a small gap certifies only first-order stationarity",
        relation=(_GE(_f_v, _f_w + _gdv, evaluate=False),),
    ),
    "I9": Axiom(
        "I9",
        INHERITED,
        "Cauchy-Schwarz inequality: for real vectors a and b, |a.b| <= ||a||_2 ||b||_2",
        citation="Horn & Johnson, Matrix Analysis, the Cauchy-Schwarz inequality",
        role="bounds the change of a term score by the norm of the parameter change times the "
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
        "simplex gap G of a term at tau = infinity",
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
        role="names the one-term fit as a geometric program: L4 shows that its objective is a "
        "posynomial in x = exp(w) and its simplex constraints are monomial, so the fit is a "
        "geometric program in standard form and the problem in w is its convex form",
        failure_mode="holds for a program that meets all three premises; a negative coefficient, "
        "an exponent that depends on x, or a constraint that is not a posynomial bounded by one "
        "or a monomial equal to one leaves the program outside the class. It says nothing of "
        "several terms, where each design counts against its nearest term (a minimum over "
        "terms): that fit is not a geometric program as a whole",
        relation=(sp.Equivalent(sp.And(_GP_OBJ, _GP_EQ, _GP_INEQ), _GP_STD),),
        objects=(
            ("objective", _GP_OBJ),
            ("equalities", _GP_EQ),
            ("inequalities", _GP_INEQ),
            ("conclusion", _GP_STD),
        ),
    ),
    "I14": Axiom(
        "I14",
        INHERITED,
        "Jensen's inequality: if f is convex, x_1, ..., x_K are in its domain and theta_1, ..., "
        "theta_K >= 0 with sum_k theta_k = 1, then f(sum_k theta_k x_k) <= sum_k theta_k f(x_k)",
        citation="Boyd & Vandenberghe, Convex Optimization, section 3.1.8 (Jensen's inequality "
        "and extensions; the two-point form is the definition of convexity, (3.1) of section "
        "3.1.1); read in the authors' PDF https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf",
        role="averages a convex function over finitely many points: L16 uses it for the "
        "permutation average of a program that is convex and symmetric in its terms, and for "
        "the concave logarithm (the convex function -log) in Gibbs' inequality",
        failure_mode="holds for every convex f and every convex combination; for a function "
        "that is not convex it fails, which is how L16 exhibits that the several-term objective "
        "is not convex",
        relation=(
            _LE(_JF_MEAN, _JMEAN_F, evaluate=False),
            _GE(_JSLACK[_i], 0, evaluate=False),  # the slack of each instance is nonnegative
        ),
    ),
    "I15": Axiom(
        "I15",
        INHERITED,
        "a function of positive variables formed from posynomials using addition, "
        "multiplication, positive (fractional) power and maximum is a generalized posynomial "
        "(the definition)",
        citation="Boyd, Kim, Vandenberghe & Hassibi, A tutorial on geometric programming, "
        "Optimization and Engineering 8(1), 2007, section 5.3 (generalized posynomials; "
        "section 5.4 defines the generalized geometric program with a generalized posynomial "
        "objective and inequalities and monomial equalities); read in the authors' PDF "
        "https://web.stanford.edu/~boyd/papers/pdf/gp_tutorial.pdf",
        role="names the exponential of the fixed-weight objective of L16 as a generalized "
        "posynomial: a product of positive powers of posynomials and of monomials",
        failure_mode="a power that is not positive, a posynomial with a negative coefficient or "
        "a difference of posynomials leaves the class",
        relation=(sp.Equivalent(_GG_BUILT, _GG_GENPOS),),
        objects=(("premise", _GG_BUILT), ("conclusion", _GG_GENPOS)),
    ),
    "I16": Axiom(
        "I16",
        INHERITED,
        "second-order sufficient conditions: let x be a feasible point of min f(x) subject to "
        "equality and inequality constraints c_i, with f and c_i twice continuously "
        "differentiable, and suppose there is a Lagrange multiplier vector for which the KKT "
        "conditions hold at x. If w' (Hessian of the Lagrangian) w > 0 for every nonzero w in "
        "the critical cone C(x, lambda) (the linearized feasible directions that are tangent "
        "to the equalities and to the active inequalities with a positive multiplier, and "
        "nonnegative along the active inequalities with a zero multiplier), then x is a strict "
        "local solution. No constraint qualification is needed. With affine constraints the "
        "Hessian of the Lagrangian is the Hessian of f",
        citation="Nocedal & Wright, Numerical Optimization, 2nd ed., Theorem 12.6 "
        "(Second-Order Sufficient Conditions), with the critical cone of section 12.5 "
        "(definition 12.53) and the KKT conditions (12.34); read in a course copy of the "
        "book's text (Kent State, pages as in the printed edition, p. 333), not the "
        "publisher's: to be confirmed by the author against the printed second edition",
        role="turns a first-order stationary point of the soft-weight fit, at which the Hessian "
        "D - kappa M of the soft objective is positive definite on the tangent space of the "
        "active face, into a strict local minimizer of that objective: the certificate of L17",
        failure_mode="the theorem is about an exact KKT point: a numerical stationarity "
        "tolerance is not covered by it; the critical cone is contained in the tangent space "
        "of the active face (bounds with a positive multiplier fixed), so positive definiteness "
        "on that space is sufficient, not necessary; a Hessian that is only positive "
        "semidefinite on the cone decides nothing",
        relation=(sp.Implies(sp.And(_SOS_KKT, _SOS_PD), _SOS_MIN),),
        objects=(("kkt", _SOS_KKT), ("curvature", _SOS_PD), ("conclusion", _SOS_MIN)),
    ),
    "I17": Axiom(
        "I17",
        INHERITED,
        "expectation: E is linear and monotone (X <= Y almost surely gives E X <= E Y), and for a "
        "convex f and a random variable X with E X and E f(X) existing, f(E X) <= E f(X) "
        "(Jensen's inequality for expectations)",
        citation="Boyd & Vandenberghe, Convex Optimization, section 3.1.8, inequality (3.5) "
        "f(E x) <= E f(x) (read in the authors' PDF https://web.stanford.edu/~boyd/cvxbook/"
        "bv_cvxbook.pdf); Billingsley, Probability and Measure, properties of the expected value "
        "(linearity, monotonicity)",
        role="takes the expectation of a pointwise inequality of random scores (L19) and "
        "moves a concave logarithm outside an expectation",
        failure_mode="holds whenever the expectations exist; the exponential moments the lemma "
        "uses exist for Gaussian noise",
        relation=(
            _LE(_JX_F, _JX_EF, evaluate=False),
            sp.Implies(_EX_LE_P, _EX_LE_Q),
        ),
    ),
    "I18": Axiom(
        "I18",
        INHERITED,
        "Moore-Penrose pseudoinverse: for a real symmetric matrix X, X^+ X is the orthogonal "
        "projector onto the range of X; hence if x lies in the range of X and X x = b, then "
        "x = X^+ b",
        citation="Penrose, A generalized inverse for matrices, Mathematical Proceedings of the "
        "Cambridge Philosophical Society 51 (1955) 406-413, doi:10.1017/S0305004100030401 "
        "(the four defining equations; X^+ X and X X^+ are Hermitian idempotents, so projectors); "
        "the page of the DOI was resolved, the paper itself was not read in full",
        role="turns the linearised first-order condition on the tangent space into the closed "
        "form delta = - (P C P)^+ P Sigma w (L20)",
        failure_mode="holds for every real symmetric matrix; it is a statement about the "
        "pseudoinverse, so nothing here depends on how X^+ is computed",
        relation=(sp.Implies(sp.And(_PIN_RANGE, _PIN_EQ), _PIN_SOLVES),),
        objects=(("range", _PIN_RANGE), ("equation", _PIN_EQ), ("conclusion", _PIN_SOLVES)),
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
    "R3": Axiom(
        "R3",
        REGULARITY,
        "the clean fit is interior to its face and well conditioned there: at the minimizer w* "
        "of J_tau on the simplex the participating exponents (w*_j > 0) form the face on which "
        "the fit is read, the coordinates outside it have g_j > lambda (strict complementarity, "
        "so a small perturbation of the problem leaves them at zero), and the covariance C = "
        "Cov_p(u) of the softmax weights at w* is positive definite on the tangent space "
        "{v : sum_j v_j = 0} of the face: v'Cv >= m ||v||^2 with m > 0, m the smallest "
        "eigenvalue of C there (conditioning_ = tau m)",
        role="lets the first-order condition be read on the face, makes the shift unique, and "
        "gives its size: the shift is at most ||P Sigma w*|| / m",
        failure_mode="when a coordinate sits at the boundary of the simplex (w*_j = 0) or close "
        "to it, the projector of the full simplex is the wrong one and the formula can send an "
        "exponent below zero, which the constrained fit would not do; when strict "
        "complementarity fails the face changes with the noise; when m is near zero the shift "
        "is large and the first-order reading is outside its range",
        relation=(_GE(_RQ, _M3 * _VV, evaluate=False), _GT(_M3, 0, evaluate=False)),
    ),
    "R2": Axiom(
        "R2",
        REGULARITY,
        "positive assignment margin: gamma = min_i [s_i,k(i) - max_{k != k(i)} s_ik] > 0, where "
        "s_ik = w_k.u_i - beta_k, so every row has a unique maximizing term",
        role="gives unique maximizing terms and an assignment-stable neighborhood (radius "
        "gamma / (2 max_i ||(u_i, -1)||_2)) on which the several-term objective equals its "
        "fixed-assignment expression, so Proposition 3 applies: a fit whose terms are exactly "
        "optimal is a local minimizer, and with gap-bounded terms the approximate-certificate "
        "corollary bounds the remaining improvement",
        failure_mode="ridge rows: a frontier row on two term planes has margin zero at tau = "
        "infinity, and duplicate terms give identical scores; the neighborhood is then empty, "
        "Proposition 3 does not apply, and termination reports stationary_without_margin: the "
        "fit is first-order stationary per term (levels 1 and 2) with no local-optimality claim",
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
    "F19": Axiom(
        "F19",
        POSITED,
        "max representation for L19: the maximum of the noise draws z_1, ..., z_n is a symbol Zm "
        "with z_i <= Zm for all i in 1..n and z_{i0} = Zm for some i0 in 1..n",
        role="lets the bound LME(s + z) <= LME(s) + max_i z_i and the bound on E max_i z_i be "
        "proved for symbolic n (sympy has no symbolic-n maximum)",
        failure_mode="as F5: if Zm is only an upper bound that is not attained, the first bound "
        "holds with Zm in place of the maximum but the sandwich names a larger quantity than "
        "E max z",
        fallback=True,
        relation=(_LE(_zr[_S.i], _Zm, evaluate=False), sp.Eq(_zr[_i0z], _Zm)),
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
A9 = AXIOMS["A9"]
A10 = AXIOMS["A10"]
A11 = AXIOMS["A11"]
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
I14 = AXIOMS["I14"]
I15 = AXIOMS["I15"]
I16 = AXIOMS["I16"]
I17 = AXIOMS["I17"]
I18 = AXIOMS["I18"]
R1 = AXIOMS["R1"]
R2 = AXIOMS["R2"]
R3 = AXIOMS["R3"]
F5 = AXIOMS["F5"]
F10 = AXIOMS["F10"]
F12 = AXIOMS["F12"]
F19 = AXIOMS["F19"]


def get(name):
    return AXIOMS[name]


def fingerprints():
    """name -> stable hash of each entry's statement, citation and SymPy form."""
    return {name: a.fingerprint() for name, a in AXIOMS.items()}


def by_tag(tag):
    return [a for a in AXIOMS.values() if a.tag == tag]


def fallbacks():
    return [a for a in AXIOMS.values() if a.fallback]
