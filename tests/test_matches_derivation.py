"""Cross-check of the implementation against the WP1 derivation chain (labelled, not a proof).

The WP1 chain (``derivation/``) derives the formulas for symbolic ``d`` and ``n``. Here its stored
SymPy expressions (L1, L2, L3, L5, L7, L8) are evaluated at seeded numeric instances (``d = 3``,
``n = 5``; the chain indexes from 1) and compared to what the solvers, the chart and the estimator
return, to 1e-10. Agreement shows the code implements those expressions; it does not re-prove them.
"""

import numpy as np
import pytest
import sympy as sp

from derivation.run import run_chain
from hyperbolic_trade_space import HyperbolicTradeSpace, solvers
from hyperbolic_trade_space.coordinates import (
    from_frontier_coordinates,
    helmert_basis,
    to_frontier_coordinates,
)

TOL = 1e-10
D, N, TAU = 3, 5, 4.0


@pytest.fixture(scope="module")
def ctx():
    return run_chain(verbose=False)[0]


@pytest.fixture(scope="module")
def inst():
    """Seeded instance: metrics M (N, D), exponents w on the simplex, direction v, beta."""
    rng = np.random.RandomState(7)
    M = np.exp(rng.randn(N, D))
    w = rng.dirichlet(np.ones(D))
    return {"M": M, "U": np.log(M), "w": w, "v": rng.randn(D), "beta": 0.37}


def ev(expr, S, inst, extra=None, tau=TAU, pre=None):
    """Evaluate a chain expression at the instance: sizes, tau, then indexed families (1-based)."""
    tables = {
        "w": lambda j: inst["w"][int(j) - 1],
        "v": lambda j: inst["v"][int(j) - 1],
        "u": lambda i, j: inst["U"][int(i) - 1, int(j) - 1],
        "m": lambda j: inst["M"][0, int(j) - 1],
        **(extra or {}),
    }
    e = expr.subs({S.d: D, S.n: N, S.tau: tau, **(pre or {})}).doit()
    e = e.replace(
        lambda x: isinstance(x, sp.Indexed) and str(x.base) in tables,
        lambda x: sp.Float(tables[str(x.base)](*x.indices), 30),
    )
    return float(sp.N(e.doit(), 30))


# ---------------------------------------------------------------- L1 homogeneity, invariant form
def test_L1_invariant_value_homogeneity_and_invariant_form(ctx, inst):
    S, L1 = ctx["S"], ctx["L1"]
    w, beta, M = inst["w"], inst["beta"], inst["M"]
    est = HyperbolicTradeSpace()
    est.fit(M)
    est.exponents_ = w[None, :]
    est.log_offset_ = np.array([beta])
    # V (w/o offset) = exp(w.u); estimator V = exp(w.u - beta)
    V_chain = ev(L1["V"], S, inst)
    assert V_chain * np.exp(-beta) == pytest.approx(est.invariant_value(M[:1])[0], abs=TOL)
    # V_tilde = e^{-beta0} prod m^w with beta0 -> beta
    Vt = ev(L1["V_tilde"], S, inst, pre={L1["beta0"]: beta})
    assert Vt == pytest.approx(est.invariant_value(M[:1])[0], abs=TOL)
    # homogeneity: V(k m) = k V(m)
    k = 2.5
    Vk = ev(L1["Vk"], S, inst, pre={S.k_scale: k})
    assert Vk == pytest.approx(k * V_chain, abs=TOL)
    assert est.invariant_value(k * M[:1])[0] == pytest.approx(
        k * est.invariant_value(M[:1])[0], abs=TOL
    )
    # invariant form: V(m / V(m)) = 1 (chain: V_inv_form == 1)
    assert L1["V_inv_form"] == 1
    np.testing.assert_allclose(est.invariant_value(est.project(M)), 1.0, atol=TOL)


# ---------------------------------------------------------------- L2 shift, L5 log-mean-exp
def test_L2_objective_and_shift(ctx, inst):
    S, L2 = ctx["S"], ctx["L2"]
    U, w = inst["U"], inst["w"]
    f, _ = solvers.objective_and_grad(w, U, TAU)
    assert ev(L2["J"], S, inst) == pytest.approx(f, abs=TOL)
    c = 0.8
    shifted = ev(L2["J_shifted"].subs(S.c, c), S, inst)
    assert shifted == pytest.approx(solvers.objective_and_grad(w, U + c, TAU)[0], abs=TOL)
    # reduced form J + c, and the implementation's offset shifts the same way
    assert ev(L2["J_shifted_reduced"].subs(S.c, c), S, inst) == pytest.approx(f + c, abs=TOL)
    assert shifted == pytest.approx(f + c, abs=TOL)
    # offset of a fit equals J at the fitted exponents
    est = HyperbolicTradeSpace(temperature=TAU).fit(np.exp(U))
    inst_fit = {**inst, "w": est.exponents_[0]}
    assert est.log_offset_[0] == pytest.approx(ev(L2["J"], S, inst_fit), abs=1e-8)


def test_L5_log_mean_exp(ctx, inst):
    S, L5 = ctx["S"], ctx["L5"]
    s = inst["U"] @ inst["w"]
    extra = {"s": lambda i: s[int(i) - 1]}
    lme = solvers.log_mean_exp(s, TAU)
    assert ev(L5["LME"], S, inst, extra) == pytest.approx(lme, abs=TOL)
    lse = ev(L5["LSE"], S, inst, extra)
    assert lse - lme == pytest.approx(np.log(N) / TAU, abs=TOL)  # chain "offset"
    # the chain's 'offset' is LSE - LME = log(n)/tau, symbolically
    assert sp.simplify(L5["offset"] - sp.log(S.n) / S.tau) == 0
    assert ev(L5["mean"], S, inst, extra) == pytest.approx(s.mean(), abs=TOL)
    # bounds mean <= LME <= max and max - log(n)/tau <= LME (the chain's lme_minus_M_lower)
    low = float(L5["lme_minus_M_lower"].subs({S.n: N, S.tau: TAU}))
    assert s.mean() - TOL <= lme <= s.max() + TOL
    assert lme - s.max() >= low - TOL
    assert solvers.log_mean_exp(s, np.inf) == pytest.approx(s.max(), abs=TOL)


# ---------------------------------------------------------------- L3 gradient and softmax weights
def test_L3_gradient_and_support_weights(ctx, inst):
    S, L3 = ctx["S"], ctx["L3"]
    U, w, v = inst["U"], inst["w"], inst["v"]
    _, grad = solvers.objective_and_grad(w, U, TAU)
    p = solvers.support_weights(U @ w, TAU)
    # directional derivative dJ/dt of J(w + t v) at 0 equals v . grad
    assert ev(L3["dJ"], S, inst) == pytest.approx(v @ grad, abs=TOL)
    # softmax weights p_i
    for i in range(1, N + 1):
        assert ev(L3["p_def"](i), S, inst) == pytest.approx(p[i - 1], abs=TOL)
    # gradient components sum_i p_i u_ij (the KKT left side, for each j0)
    kkt_lhs = L3["KKT"].lhs
    for j0 in range(1, D + 1):
        val = ev(kkt_lhs.subs(sp.Symbol("j0", integer=True), j0), S, inst)
        assert val == pytest.approx(grad[j0 - 1], abs=TOL)
    # simplex derivative: sum_j v_j
    assert ev(L3["dsimplex"], S, inst) == pytest.approx(v.sum(), abs=TOL)


# ---------------------------------------------------------------- L7 elasticities, improvement
def test_L7_improvement_factor_and_elasticity(ctx, inst):
    S, L7 = ctx["S"], ctx["L7"]
    X, w, beta = inst["M"], inst["w"], inst["beta"]
    est = HyperbolicTradeSpace().fit(X)
    est.exponents_ = w[None, :]
    est.log_offset_ = np.array([beta])
    F = est.improvement_factors(X)
    Ut = np.log(X) - beta  # m~ = m e^{-beta}: the chain's u_pt carries the offset
    for i in range(N):
        for j0 in range(1, D + 1):
            tables = {"u_pt": lambda j, i=i: Ut[i, int(j) - 1]}
            subs = {L7["j0"]: j0}
            lf = ev(L7["logf_star"].subs(subs), S, inst, tables)
            assert np.exp(lf) == pytest.approx(F[i, j0 - 1], rel=TOL)
            assert ev(L7["f_star"].subs(subs), S, inst, tables) == pytest.approx(
                F[i, j0 - 1], rel=TOL
            )
            # logV + logf w_j0 = 0 at the chain's factor
            lv = ev(L7["logV_new"].subs({**subs, L7["logf"]: lf}), S, inst, tables)
            assert lv == pytest.approx(0.0, abs=TOL)
    # elasticity: dG = w_k0 + x w_j0 vanishes at x = -w_k0/w_j0
    for k0, j0 in [(1, 2), (3, 1)]:
        x = ev(L7["x_sol"].subs({L7["k0"]: k0, L7["j0"]: j0}), S, inst)
        assert x == pytest.approx(-w[k0 - 1] / w[j0 - 1], abs=TOL)
        g = ev(L7["dG"].subs({L7["k0"]: k0, L7["j0"]: j0, sp.Symbol("x", real=True): x}), S, inst)
        assert g == pytest.approx(0.0, abs=TOL)


# ---------------------------------------------------------------- L8 chart
def test_L8_chart_relations(ctx, inst):
    S, L8 = ctx["S"], ctx["L8"]
    U, w, beta = inst["U"], inst["w"], inst["beta"]
    B = helmert_basis(D)
    # hypotheses A7: B B^T = I, B 1 = 0
    np.testing.assert_allclose(B @ B.T, np.eye(D - 1), atol=TOL)
    np.testing.assert_allclose(B @ np.ones(D), 0.0, atol=TOL)
    Z, log_v = to_frontier_coordinates(U, w, beta, B)
    for r in range(N):
        sub = {S.B: sp.Matrix(B), L8["u"]: sp.Matrix(U[r])}
        Zc = np.array(L8["Z"].xreplace(sub).doit().tolist(), dtype=float).ravel()
        np.testing.assert_allclose(Z[r], Zc, atol=TOL)
        # shift invariance: chain's shifted == B u, implementation Z blind to + c 1
        Zs = np.array(L8["shifted"].xreplace(sub).doit().tolist(), dtype=float).ravel()
        np.testing.assert_allclose(Zs, Z[r], atol=TOL)
        Zshift, _ = to_frontier_coordinates(U[r : r + 1] + 1.7, w, beta, B)
        np.testing.assert_allclose(Zshift[0], Z[r], atol=TOL)
        # log-scale coordinate ell = (1/d) 1^T u and the reconstruction u = B^T Z + ell 1
        ell_expr = (
            L8["ell"]
            .subs(S.d, D)
            .doit()
            .replace(
                lambda x: isinstance(x, sp.matrices.expressions.matexpr.MatrixElement),
                lambda x, r=r: sp.Float(U[r, int(x.args[1])], 30),
            )
        )
        ell = float(ell_expr)
        assert ell == pytest.approx(U[r].mean(), abs=TOL)
        back = from_frontier_coordinates(Z[r : r + 1], log_v[r : r + 1], w, beta, B)[0]
        np.testing.assert_allclose(back, U[r], atol=TOL)
        np.testing.assert_allclose(B.T @ Z[r] + ell, U[r], atol=TOL)
    # block Gram identity of the chain: Q Q^T = I with Q = [B; 1/sqrt(d) 1]
    Q = np.vstack([B, np.ones((1, D)) / np.sqrt(D)])
    np.testing.assert_allclose(Q @ Q.T, np.eye(D), atol=TOL)
    np.testing.assert_allclose(Q.T @ Q, np.eye(D), atol=TOL)
