"""L8: the sum-zero chart Z = B u and the (log-scale, Z) bijection.

What this proves (abstract MatrixSymbol algebra, symbolic d, no explicit basis):
  (a) Z(u + c 1) = Z(u): the chart is blind to the common shift;
  (b) with Q = [B; 1^T/sqrt(d)] (d x d), Q Q^T = I block-wise from A7 (B B^T = I, B 1 = 0) and
      1^T 1 / d = 1;
  (c) Q^T Q = I follows from (b) by I6 (square matrix: left inverse is right inverse); the
      round trip is then DERIVED, not self-compared: B^T B u + (1/d) 1 1^T u = (Q^T Q) u, and
      substituting Q^T Q = I gives u. The check fails if A7 or I6 is dropped (negative controls
      in the tests call roundtrip_holds with the hypothesis switched off).
What this does NOT prove: that a B with B B^T = I, B 1 = 0 exists for every d (the Helmert basis
is a realization, checked concretely in the tests as a realization check only), nor anything about
which B is used (all results hold for any B satisfying A7).

Hypotheses B B^T = I and B 1 = 0 are the posited chart axiom A7. Route: MatrixSymbol/OneMatrix
algebra with block_collapse; no differentiation or limits. Mimics symproof's habit of discharging
a structural claim by rewriting with the stated hypotheses (symproof/tactics.py).
"""

import sympy as sp
from sympy.matrices.expressions import Identity, OneMatrix, ZeroMatrix

from derivation.axioms import A7, I6

TITLE = "Sum-zero (Helmert-type) chart and scale/shape bijection"
STATEMENT = "Z=Bu is shift-invariant; u = B^T Z + (1/d)(1^T u) 1; Q=[B;1^T/sqrt d] orthogonal"
AXIOMS_USED = ["A7", "I6"]


def gram_identity_blocks(B, one, d, use_orth=True, use_ker=True):
    """Q Q^T block-wise after rewriting with A7 (switches allow negative controls)."""
    Q = sp.BlockMatrix([[B], [one.T / sp.sqrt(d)]])
    g = sp.block_collapse(Q * Q.T)
    sub = {}
    if use_orth:
        # [L8.1] A7: B B^T = I (the chart's rows are orthonormal)
        sub[B * B.T] = A7.rule(0)[1]

    def kill(expr):
        """A7: B 1 = 0 (and its transpose 1^T B^T = 0), through any scalar coefficient."""
        if use_ker and isinstance(expr, sp.MatMul):
            _, prod = expr.as_coeff_mmul()
            # [L8.2] A7: B 1 = 0, and its transpose 1^T B^T = 0
            zero = A7.rule(1)[1]
            if prod == B * one:
                return zero
            if prod == one.T * B.T:
                return zero.T
        return expr

    blocks = [
        [sp.block_collapse(kill(g.blocks[a, b]).xreplace(sub)) for b in range(2)] for a in range(2)
    ]
    return Q, g, blocks


def roundtrip_holds(B, u, one, d, use_orth=True, use_ker=True, use_I6=True):
    """True iff recon = u is DERIVED: QQ^T = I (A7) => Q^T Q = I (I6) => (Q^T Q) u = u."""
    Q, _, blocks = gram_identity_blocks(B, one, d, use_orth, use_ker)
    zero_r, zero_c = ZeroMatrix(d - 1, 1), ZeroMatrix(1, d - 1)
    gram_is_I = (
        blocks[0][0] == Identity(d - 1)
        and blocks[0][1] in (zero_r, 0)
        and blocks[1][0] in (zero_c, 0)
        and sp.simplify(blocks[1][1] - Identity(1)) in (0, ZeroMatrix(1, 1))
    )
    if not gram_is_I:
        return False
    QtQ = sp.block_collapse(Q.T * Q)
    # I6 (Horn & Johnson): square Q, Q Q^T = I  =>  Q^T Q = I
    # [L8.3] I6: Q is square and Q Q^T = I, so Q^T Q = I
    QtQ_red = QtQ.xreplace({QtQ: I6.rule(0)[1]}) if use_I6 else QtQ
    recon = sp.block_collapse(QtQ_red * u).doit()
    return recon == u


def derive(ctx):
    S = ctx["S"]
    d, B, c = S.d, S.B, S.c
    one = OneMatrix(d, 1)
    u = sp.MatrixSymbol("u_vec", d, 1)

    # A7 (hypotheses)
    # [L8.4] A7: the chart's hypotheses are B B^T = I and B 1 = 0
    hyp_orth, hyp_ker = A7.rule(0)[1], A7.rule(1)[1]

    # (a) shift invariance: B (u + c 1) = B u + c (B 1) and B 1 = 0 (A7)
    Z = B * u
    shifted_raw = sp.block_collapse((B * (u + c * one)).expand()).doit()
    kept = []
    for term in shifted_raw.args:  # each term is coeff * (matrix product)
        _coeff, prod = term.as_coeff_mmul()
        # [L8.5] A7: B 1 = 0 kills the term c (B 1) of B (u + c 1)
        kills = prod == A7.rule(1)[0]
        if kills:
            continue
        kept.append(term)
    shifted = sp.MatAdd(*kept).doit()

    # (b) extended orthonormal matrix, Q Q^T = I block-wise from A7
    Q, gram, gram_blocks = gram_identity_blocks(B, one, d)

    ell = (one.T * u)[0, 0] / d  # log-scale coordinate (1/d) 1^T u
    ctx["L8"] = {
        "one": one,
        "u": u,
        "Z": Z,
        "shifted": shifted,
        "shifted_raw": shifted_raw,
        "Q": Q,
        "gram": gram,
        "gram_blocks": gram_blocks,
        "ell": ell,
        "hyp_orth": hyp_orth,
        "hyp_ker": hyp_ker,
    }


def verify(ctx):
    S = ctx["S"]
    r = ctx["L8"]
    d, B, one, u = S.d, S.B, r["one"], r["u"]
    # [L8.6] the chart is blind to the common shift: Z(u + c 1) = Z(u)
    assert r["shifted"] == r["Z"], "L8 FAIL Z(u + c 1) != Z(u)"
    g = r["gram_blocks"]
    # [L8.7] block (1,1) of Q Q^T is B B^T = I
    assert g[0][0] == Identity(d - 1), "L8 FAIL B B^T != I"
    # [L8.8] block (1,2) of Q Q^T is B 1 / sqrt(d) = 0
    assert g[0][1] == ZeroMatrix(d - 1, 1) or g[0][1] == 0, "L8 FAIL Gram (1,2) block != 0"
    # [L8.9] block (2,1) of Q Q^T is 1^T B^T / sqrt(d) = 0
    assert g[1][0] == ZeroMatrix(1, d - 1) or g[1][0] == 0, "L8 FAIL Gram (2,1) block != 0"
    # [L8.10] block (2,2) of Q Q^T is (1/d) 1^T 1 = 1
    assert sp.simplify(g[1][1] - Identity(1)) in (0, ZeroMatrix(1, 1)), "L8 FAIL (1/d) 1^T 1 != 1"
    # [L8.11] Q = [B; 1^T / sqrt(d)] is a square d x d matrix
    assert r["Q"].shape == (d, d), "L8 FAIL Q is not square"
    # Q^T Q expands to B^T B + (1/d) 1 1^T (exact)
    QtQ = sp.block_collapse(r["Q"].T * r["Q"])
    # [L8.12] Q^T Q expands to B^T B + (1/d) 1 1^T
    assert QtQ == B.T * B + OneMatrix(d, d) / d, "L8 FAIL Q^T Q expansion"
    # [L8.13] 1 1^T is the all-ones d x d matrix
    assert one * one.T == OneMatrix(d, d), "L8 FAIL 1 1^T != all-ones"
    # round trip derived: QQ^T = I (A7) => Q^T Q = I (I6) => B^T B u + (1/d) 1 1^T u = u
    # [L8.14] round trip: Q Q^T = I (A7) and Q^T Q = I (I6) give B^T B u + (1/d) 1 1^T u = u
    assert roundtrip_holds(B, u, one, d), "L8 FAIL round trip u = B^T B u + ell 1 not derived"
