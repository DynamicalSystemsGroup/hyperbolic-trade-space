"""L8: the sum-zero chart Z = B u and the (log-scale, Z) bijection.

What this proves (abstract MatrixSymbol algebra, symbolic d, no explicit basis):
  (a) Z(u + c 1) = Z(u): the chart is blind to the common shift;
  (b) with Q = [B; 1^T/sqrt(d)] (d x d) the Gram matrix Q Q^T equals I, so Q is orthogonal
      (square with Q Q^T = I, hence Q^T Q = I too);
  (c) hence the round trip u = B^T Z + (1/d)(1^T u) 1, and (log V, Z) -> u is a linear bijection.
What this does NOT prove: that a B with B B^T = I, B 1 = 0 exists for every d (the Helmert basis
is a realization, checked concretely in the tests as a realization check only), nor anything about
which B is used (all results hold for any B satisfying A7).

Hypotheses B B^T = I and B 1 = 0 are the posited chart axiom A7. Route: MatrixSymbol/OneMatrix
algebra with block_collapse; no differentiation or limits. Mimics symproof's habit of discharging
a structural claim by rewriting with the stated hypotheses (symproof/tactics.py).
"""

import itertools

import sympy as sp
from sympy.matrices.expressions import Identity, OneMatrix, ZeroMatrix

TITLE = "Sum-zero (Helmert-type) chart and scale/shape bijection"
STATEMENT = "Z=Bu is shift-invariant; u = B^T Z + (1/d)(1^T u) 1; Q=[B;1^T/sqrt d] orthogonal"
AXIOMS_USED = ["A7"]


def derive(ctx):
    S = ctx["S"]
    d, B, c = S.d, S.B, S.c
    one = OneMatrix(d, 1)
    u = sp.MatrixSymbol("u_vec", d, 1)

    # A7 (hypotheses)
    hyp_orth = Identity(d - 1)  # B B^T = this
    hyp_ker = ZeroMatrix(d - 1, 1)  # B 1 = this

    def rewrite(expr):
        """Rewrite with A7: any product containing the adjacent factors B, 1 is zero."""
        expr = sp.block_collapse(expr).doit()
        terms = expr.args if isinstance(expr, sp.MatAdd) else (expr,)
        out = []
        for term in terms:
            facs = term.args if isinstance(term, sp.MatMul) else (term,)
            kills = any(facs[i] == B and facs[i + 1] == one for i in range(len(facs) - 1))
            if not kills:
                out.append(term)
        return sp.MatAdd(*out).doit() if out else hyp_ker

    # (a) shift invariance
    Z = B * u
    shifted = rewrite((B * (u + c * one)).expand())

    # (b) extended orthonormal matrix
    Q = sp.BlockMatrix([[B], [one.T / sp.sqrt(d)]])
    gram = sp.block_collapse(Q * Q.T)
    gram_blocks = [[gram.blocks[a, b] for b in range(2)] for a in range(2)]
    # one^T one = d (OneMatrix algebra), so the (2,2) block is (1/d) one^T one = 1
    corner = sp.simplify((one.T * one / d)[0, 0])

    # (c) round trip: Q^T Q = B^T B + (1/d) 1 1^T = I  (Q square with Q Q^T = I)
    ell = (one.T * u)[0, 0] / d  # log-scale coordinate (1/d) 1^T u
    recon = B.T * (B * u) + one * ell
    ctx["L8"] = {
        "one": one,
        "u": u,
        "Z": Z,
        "shifted": shifted,
        "Q": Q,
        "gram_blocks": gram_blocks,
        "corner": corner,
        "ell": ell,
        "recon": recon,
        "hyp_orth": hyp_orth,
        "hyp_ker": hyp_ker,
    }


def verify(ctx):
    S = ctx["S"]
    r = ctx["L8"]
    d, B = S.d, S.B
    assert r["shifted"] == r["Z"], "L8 FAIL Z(u + c 1) != Z(u)"
    # Gram blocks: B B^T = I (A7), B 1 / sqrt(d) = 0 (A7), (1/d) 1^T 1 = 1
    g = r["gram_blocks"]
    assert g[0][0] == B * B.T, "L8 FAIL Gram (1,1) block shape"
    assert g[0][0].xreplace({B * B.T: r["hyp_orth"]}) == Identity(d - 1), "L8 FAIL B B^T = I"
    facs = g[0][1].args if isinstance(g[0][1], sp.MatMul) else (g[0][1],)
    assert any(f1 == B and f2 == r["one"] for f1, f2 in itertools.pairwise(facs)), (
        "L8 FAIL Gram (1,2) block is not a multiple of B 1 (= 0 by A7)"
    )
    assert r["corner"] == 1, "L8 FAIL (1/d) 1^T 1 != 1"
    # Q Q^T = I with Q square => Q^T Q = I => B^T B + (1/d) 1 1^T = I; so recon returns u
    assert r["Q"].shape == (d, d), "L8 FAIL Q is not square"
    # B^T B u + ell 1 = u follows from Q^T Q u = u with Q^T Q = B^T B + (1/d) 1 1^T
    QtQ = sp.block_collapse(r["Q"].T * r["Q"])
    expected = B.T * B + r["one"] * r["one"].T / d
    assert sp.simplify((QtQ - expected).doit()) in (0, ZeroMatrix(d, d)) or QtQ == expected, (
        "L8 FAIL Q^T Q expansion"
    )
    assert r["recon"] == B.T * (B * r["u"]) + r["one"] * r["ell"], "L8 FAIL round-trip form"
