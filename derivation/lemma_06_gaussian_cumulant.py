"""L6: Gaussian cumulant of a weighted noise sum (a population identity).

(1/tau) log E exp(tau w.eps) = tau sigma^2 ||w||^2 / 2 under A5 (eps_j iid N(0, sigma^2),
independent across j, sigma > 0), symbolic d.  E is the population expectation over eps.

What this proves: for one Normal(0, sigma^2) variable, E exp(t eps) = exp(sigma^2 t^2 / 2)
(sympy.stats evaluates the expectation); then, by the independent-sum MGF rule (I5), the MGF of
w.eps = sum_j w_j eps_j is the Product over j = 1..d of the single-variable MGFs at t = tau w_j,
which collapses to exp(tau^2 sigma^2 / 2 * Sum_j w_j^2) with d symbolic.
What this does NOT prove: I5 itself (inherited); anything about non-Gaussian or dependent noise;
anything about a finite sample: the identity is about the population cumulant, not about a
finite-sample estimator of it, and no consistency claim (a sample statement would need its own
independence, integrability and identifiability assumptions).

Route: sympy.stats Normal + E for the one-variable MGF (no differentiation or limit); the
Product over a symbolic range is rewritten as exp(Sum) by the exponential-product identity.
Mimics symproof's pattern of deriving a closed form then checking it by equality with the
stated target (symproof/library/convex.py, closed-form identity checks).
"""

import sympy as sp
from sympy.stats import E

from derivation.axioms import A2, A5, I5

TITLE = "Gaussian cumulant of a weighted noise sum"
STATEMENT = (
    "Population identity under the log-space Gaussian model (A5: eps_j iid N(0, sigma^2), "
    "independent across j, sigma > 0): (1/tau) log E exp(tau w.eps) = tau sigma^2 ||w||^2 / 2, "
    "with E the population expectation; not a finite-sample estimator, and no consistency claim"
)
AXIOMS_USED = ["A2", "A5", "I5"]


def derive(ctx):
    S = ctx["S"]
    t = sp.Symbol("t", real=True)
    sigma, tau, j, d = S.sigma, S.tau, S.j, S.d
    # [L6.1] A2: the exponents w lie on the simplex (the weights of the noise sum w.eps)
    w = A2.invoke(S.w)

    # single-variable MGF (A5: eps ~ N(0, sigma^2))
    # [L6.2] A5: each noise term is eps ~ N(0, sigma^2) with sigma > 0, independent across j
    X = A5.obj("noise")
    mgf1 = sp.simplify(E(sp.exp(t * X)))

    # I5: MGF of sum_j w_j eps_j = Product_j mgf1(tau w_j)
    factor = mgf1.subs(t, tau * w[j])
    # [L6.3] I5: the MGF of the independent sum w.eps is the product of the MGFs at tau w_j
    prod = I5.invoke(sp.Product(factor, (j, 1, d)))
    # exp-product identity: Product exp(f_j) = exp(Sum f_j)
    f = sp.log(factor)
    f = sp.expand_log(f, force=True)
    mgf_sum = sp.exp(sp.Sum(sp.simplify(f), (j, 1, d)))
    # j-independent constants are pulled out of the Sum by simplify (w stays symbolic)
    norm2 = sp.Sum(w[j] ** 2, (j, 1, d))
    mgf_closed = sp.exp(tau**2 * sigma**2 * norm2 / 2)
    # (1/tau) log of the derived MGF: log exp(Sum f) = Sum f, then divide by tau
    cumulant = sp.simplify(mgf_sum.args[0] / tau)

    ctx["L6"] = {
        "mgf1": mgf1,
        "t": t,
        "product": prod,
        "mgf_sum": mgf_sum,
        "mgf_closed": mgf_closed,
        "norm2": norm2,
        "cumulant": cumulant,
        "target": tau * sigma**2 * norm2 / 2,
    }


def verify(ctx):
    S = ctx["S"]
    r = ctx["L6"]
    t, sigma, tau = r["t"], S.sigma, S.tau
    # [L6.4] one noise variable: E exp(t eps) = exp(sigma^2 t^2 / 2)
    assert sp.simplify(r["mgf1"] - sp.exp(sigma**2 * t**2 / 2)) == 0, "L6 FAIL one-variable MGF"
    # the Sum of per-term exponents equals the closed form's exponent, term by term
    lhs = r["mgf_sum"].args[0]
    # [L6.5] the exponent of the product of MGFs is a Sum over j
    assert isinstance(lhs, sp.Sum), "L6 FAIL exponent is not a Sum over j"
    summand_gap = sp.simplify(lhs.function - tau**2 * sigma**2 * S.w[S.j] ** 2 / 2)
    # [L6.6] each summand of the exponent is tau^2 sigma^2 w_j^2 / 2
    assert summand_gap == 0, "L6 FAIL per-term exponent mismatch"
    # [L6.7] the Sum runs over j = 1..d, the same range as ||w||^2
    assert lhs.limits == r["norm2"].limits, "L6 FAIL Sum range is not 1..d"
    # cumulant divided by tau equals tau sigma^2 ||w||^2 / 2
    # [L6.8] the cumulant (1/tau) log E exp(tau w.eps) equals tau sigma^2 ||w||^2 / 2
    assert sp.simplify(r["cumulant"] - r["target"]) == 0, "L6 FAIL cumulant formula"
    # [L6.9] the identity holds at symbolic d (the upper limit of ||w||^2 is d)
    assert r["norm2"].limits[0][2] == S.d, "L6 FAIL upper limit is not symbolic d"
