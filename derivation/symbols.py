"""Abstract symbol namespace for the derivation chain (no concrete dimension anywhere).

``make_symbols()`` takes no size arguments: d, n, K are symbolic positive integers. Lemma-local
symbols stay in the lemma modules.

Load-bearing accounting (symproof discipline): any SymPy assumption baked into a Symbol or
IndexedBase (positive, integer, ...) is a modelling commitment and must correspond to a declared
axiom. ``SYMBOL_ASSUMPTIONS`` records that mapping, keyed by tag with value
``(symbol name, assumption, licensing axiom)``; the hygiene test checks that every strong
assumption in the namespace is registered.
"""

from types import SimpleNamespace

import sympy as sp

# Strong assumptions that the hygiene test polices.
STRONG_ASSUMPTIONS = ("positive", "negative", "nonnegative", "nonpositive", "integer")

# tag -> (symbol name in the namespace, assumption, licensing axiom)
SYMBOL_ASSUMPTIONS = {
    "d_positive": ("d", "positive", "A0"),
    "d_integer": ("d", "integer", "A0"),
    "n_positive": ("n", "positive", "A0"),
    "n_integer": ("n", "integer", "A0"),
    "K_positive": ("K", "positive", "A0"),
    "K_integer": ("K", "integer", "A0"),
    "i_integer": ("i", "integer", "A0"),
    "j_integer": ("j", "integer", "A0"),
    "k_integer": ("k", "integer", "A0"),
    "i0_integer": ("i0", "integer", "A0"),
    "L_integer": ("L", "integer", "A0"),
    "J0_integer": ("J0", "integer", "A0"),
    "m_positive": ("m", "positive", "A1"),
    "k_scale_positive": ("k_scale", "positive", "A1"),
    "tau_positive": ("tau", "positive", "A3"),
    "sigma_positive": ("sigma", "positive", "A5"),
    "kappa_positive": ("kappa", "positive", "A6"),
}

# shared index symbols (integer, A0): L is the dummy of the softmax normalizer (L3, L4), J0 the
# coordinate-direction index (L3, L12)
L = sp.Symbol("l", integer=True)
J0 = sp.Symbol("j0", integer=True)


def make_symbols():
    """Return the abstract namespace shared by all lemmas (symbolic d, n, K).

    >>> S = make_symbols()
    >>> S.simplex
    Eq(Sum(w[j], (j, 1, d)), 1)
    >>> S.B.shape
    (d - 1, d)
    """
    # sizes: positive integers (licensed by posited "sizes" axiom A0)
    d = sp.Symbol("d", integer=True, positive=True)
    n = sp.Symbol("n", integer=True, positive=True)
    K = sp.Symbol("K", integer=True, positive=True)

    # indices (integer, A0)
    i, j, k, i0 = (sp.Symbol(s, integer=True) for s in ("i", "j", "k", "i0"))

    # indexed families. m_i[j]: metrics, positive (A1). u[i, j] = log m_i[j].
    m = sp.IndexedBase("m", positive=True)
    u = sp.IndexedBase("u")
    w = sp.IndexedBase("w")  # exponents (simplex, A2)
    theta = sp.IndexedBase("theta")  # theta[k, j]: exponent of term k (L10)
    beta = sp.IndexedBase("beta", real=True)  # beta[k]: real offset of term k (L10)
    s = sp.IndexedBase("s")  # scores s[i] = w . u_i
    a = sp.IndexedBase("a")  # conditioning offsets (L9)
    alpha = sp.IndexedBase("alpha")  # conditioning exponents, alpha_j != 0 (A4, L9)
    b = sp.IndexedBase("b")  # conditioning log-shifts (L9)

    # helpers for L3/L4/L5/L6/L10
    v = sp.IndexedBase("v")  # direction (L3, L4, L7)
    p = sp.IndexedBase("p")  # softmax weights p[i]
    eps = sp.IndexedBase("eps")  # noise eps[j] (L6)
    t = sp.Symbol("t", real=True)  # scalar line parameter for d/dt J(w + t v)

    # scalars
    tau = sp.Symbol("tau", positive=True)
    kappa = sp.Symbol("kappa", positive=True)
    sigma = sp.Symbol("sigma", positive=True)
    c = sp.Symbol("c", real=True)  # additive shift
    k_scale = sp.Symbol("k_scale", positive=True)  # multiplicative scale (L1)
    M = sp.Symbol("M", real=True)  # maximum of the scores (L5, L10 representation)

    # chart basis (L8): rows span the sum-zero subspace
    B = sp.MatrixSymbol("B", d - 1, d)

    # simplex constraint, carried as a substitutable equation (w_d not eliminated)
    simplex = sp.Eq(sp.Sum(w[j], (j, 1, d)), 1)
    # same constraint for the K-term family, term k
    simplex_theta = sp.Eq(sp.Sum(theta[k, j], (j, 1, d)), 1)
    # softmax normalization carried as an equation
    p_normalized = sp.Eq(sp.Sum(p[i], (i, 1, n)), 1)

    return SimpleNamespace(
        d=d, n=n, K=K, i=i, j=j, k=k, i0=i0, L=L, J0=J0,
        m=m, u=u, w=w, theta=theta, beta=beta, s=s, a=a, alpha=alpha, b=b,
        v=v, p=p, eps=eps, t=t,
        tau=tau, kappa=kappa, sigma=sigma, c=c, k_scale=k_scale, M=M,
        B=B, simplex=simplex, simplex_theta=simplex_theta, p_normalized=p_normalized,
    )  # fmt: skip
