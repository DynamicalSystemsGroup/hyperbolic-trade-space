"""The axiom manifest: single source of truth for what the derivation assumes.

Tags:
  POSITED     - a modelling choice we declare (A0-A6).
  INHERITED   - an external theorem we USE and CITE but do not prove here (I1-I6).
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

from dataclasses import dataclass

POSITED = "POSITED"
INHERITED = "INHERITED"
REGULARITY = "REGULARITY"
TAGS = (POSITED, INHERITED, REGULARITY)

# Axioms licensing symbol assumptions only; exempt from the every-axiom-is-used test.
STRUCTURAL = ("A0",)

# Inherited results that license the K > 1 solver, not a lemma premise: reported in the ledger
# under their own heading and exempt from the every-axiom-is-used test (no lemma consumes them).
SOLVER_LEVEL = ("I7",)


@dataclass(frozen=True)
class Axiom:
    name: str
    tag: str
    statement: str  # human-readable claim
    relation: object = None  # optional SymPy relation making it machine-checkable
    citation: str = ""  # required for INHERITED
    role: str = ""  # interpretive role: what the condition buys for interpretation
    failure_mode: str = ""  # what the interpretation loses when it does not hold
    fallback: bool = False  # introduced because a step resisted abstract simplification

    def __str__(self):
        cite = f"  [{self.citation}]" if self.citation else ""
        return f"{self.name} ({self.tag}): {self.statement}{cite}"


AXIOMS = {
    # ---------------------------------------------------------------- POSITED
    "A0": Axiom(
        "A0",
        POSITED,
        "sizes: the dimension d, the sample count n and the term count K are positive "
        "integers, and the index symbols i, j, k are integers (structural; the lemmas are "
        "proved for symbolic d, n, K, not at chosen sizes)",
    ),
    "A1": Axiom(
        "A1",
        POSITED,
        "metrics are strictly positive, larger-is-better: m_i[j] > 0, so u = log m is defined",
    ),
    "A2": Axiom(
        "A2",
        POSITED,
        "the exponents w lie on the simplex: w_j >= 0 and sum_j w_j = 1",
    ),
    "A3": Axiom(
        "A3",
        POSITED,
        "the soft-maximum temperature is positive: tau > 0",
    ),
    "A4": Axiom(
        "A4",
        POSITED,
        "conditioning is log-affine and invertible: log m_j = alpha_j log(a_j + s_j) + b_j "
        "with alpha_j != 0 (negative alpha_j marks a cost attribute)",
    ),
    "A5": Axiom(
        "A5",
        POSITED,
        "noise: eps_j are i.i.d. N(0, sigma^2), independent across j, with sigma > 0",
    ),
    "A6": Axiom(
        "A6",
        POSITED,
        "the extension temperature is positive, kappa > 0, and each of the K terms has "
        "exponents theta_k on the simplex",
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
    ),
    # -------------------------------------------------------------- INHERITED
    "I1": Axiom(
        "I1",
        INHERITED,
        "LP strong duality: min_{w in simplex} max_i w.u_i equals the dual max over "
        "lambda in the simplex of min_j (U^T lambda)_j (checked numerically in pytest)",
        citation="Boyd & Vandenberghe, Convex Optimization, section 5.2",
    ),
    "I2": Axiom(
        "I2",
        INHERITED,
        "strong law of large numbers: sample means converge almost surely to the "
        "expectation (replication leaves J_tau unchanged; checked in pytest)",
        citation="Kolmogorov strong law of large numbers; Billingsley, Probability and Measure",
    ),
    "I3": Axiom(
        "I3",
        INHERITED,
        "a closed convex set is determined by its support function",
        citation="Rockafellar, Convex Analysis, section 13",
    ),
    "I4": Axiom(
        "I4",
        INHERITED,
        "softmax-affine (log-sum-exp of affine) functions are GP-compatible",
        citation="Hoburg, Kirschen & Abbeel, 2016, Data fitting with geometric-programming-"
        "compatible softmax functions",
    ),
    "I5": Axiom(
        "I5",
        INHERITED,
        "the moment generating function of a sum of independent random variables is the "
        "product of their moment generating functions (ledger addition to spec section 6)",
        citation="Billingsley, Probability and Measure, MGF of independent sums",
    ),
    "I6": Axiom(
        "I6",
        INHERITED,
        "for a square real matrix Q, Q Q^T = I implies Q^T Q = I (a left inverse of a square "
        "matrix is also its right inverse)",
        citation="Horn & Johnson, Matrix Analysis, invertible matrices (the inverse is two-sided)",
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
    ),
    # ------------------------------------------------------------- REGULARITY
    "R1": Axiom(
        "R1",
        REGULARITY,
        "the balanced point lies in the relative interior of a facet of the frontier with "
        "positive normal",
        role="makes the KKT balanced point a genuine interior frontier point, so the "
        "gradient condition identifies w* as the facet normal and the improvement factors "
        "and elasticities can be read as trade-offs along the frontier",
        failure_mode="at a vertex, an edge or a facet with a zero normal component the "
        "gradient condition holds only as a subgradient inclusion: w* is not unique, some "
        "elasticities are undefined, and the frontier reading degrades to the weaker "
        "invariant-form reading",
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
    ),
}


def get(name):
    return AXIOMS[name]


def by_tag(tag):
    return [a for a in AXIOMS.values() if a.tag == tag]


def fallbacks():
    return [a for a in AXIOMS.values() if a.fallback]
