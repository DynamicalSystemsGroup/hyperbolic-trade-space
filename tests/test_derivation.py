"""Tests for the abstract derivation chain (derivation/).

Chain and hygiene checks. Substitution cross-checks (test_crosscheck_L<n>) and the numeric
checks of inherited facts (I1 LP duality, I2 replication) are added alongside the lemmas.
"""

import importlib.util
import io
from contextlib import redirect_stdout

import pytest
import sympy as sp

from derivation import axioms as AX
from derivation import symbols as S
from derivation.run import CHAIN, CHAIN_NAMES, print_audit, run_chain

ALL_PRESENT = all(
    importlib.util.find_spec(f"derivation.{name}") is not None for name in CHAIN_NAMES
)


def test_full_chain_runs():
    ctx, used = run_chain(verbose=False)
    assert "S" in ctx
    for name in used:
        assert name in AX.AXIOMS


def test_each_lemma_verifies():
    ctx = {"S": S.make_symbols()}
    for lemma in CHAIN:
        lemma.derive(ctx)
        lemma.verify(ctx)  # raises AssertionError "L<n> FAIL ..." on failure
        for attr in ("TITLE", "STATEMENT", "AXIOMS_USED"):
            assert hasattr(lemma, attr), f"{lemma.__name__} missing {attr}"


def test_no_phantom_axioms():
    for lemma in CHAIN:
        for name in lemma.AXIOMS_USED:
            assert name in AX.AXIOMS, f"{lemma.__name__} cites undeclared axiom {name}"


def test_inherited_axioms_are_cited():
    inherited = AX.by_tag(AX.INHERITED)
    assert {"I1", "I2", "I3", "I4", "I5"} <= {a.name for a in inherited}
    for a in inherited:
        assert a.citation.strip(), f"inherited axiom {a.name} has no citation"


def test_regularity_and_fallbacks_state_role_and_failure_mode():
    for a in AX.by_tag(AX.REGULARITY) + AX.fallbacks():
        assert a.role.strip(), f"{a.name} has no interpretive role"
        assert a.failure_mode.strip(), f"{a.name} has no failure mode"
    assert AX.get("R1").tag == AX.REGULARITY


def test_load_bearing_symbol_assumptions_are_declared():
    """Every strong assumption in the namespace (incl. IndexedBase) is registered and licensed."""
    ns = S.make_symbols()
    registered = {(name, assumption) for (name, assumption, _) in S.SYMBOL_ASSUMPTIONS.values()}

    for tag, (name, assumption, axiom_name) in S.SYMBOL_ASSUMPTIONS.items():
        assert axiom_name in AX.AXIOMS, f"{tag}: licenses missing axiom {axiom_name}"
        obj = getattr(ns, name)
        assert getattr(obj, f"is_{assumption}", None) is True, (
            f"{tag}: {name} is not actually {assumption}"
        )

    for name, obj in vars(ns).items():
        if isinstance(obj, (sp.Symbol, sp.IndexedBase)):
            for assumption in S.STRONG_ASSUMPTIONS:
                implied_by = {"nonnegative": "positive", "nonpositive": "negative"}.get(assumption)
                if implied_by and (name, implied_by) in registered:
                    continue  # derived from a registered stronger assumption
                if getattr(obj, f"is_{assumption}", None) is True:
                    assert (name, assumption) in registered, (
                        f"{name} is {assumption} but is not registered in SYMBOL_ASSUMPTIONS "
                        f"with a licensing axiom"
                    )


def test_every_used_axiom_resolves_and_all_tags_valid():
    _, used = run_chain(verbose=False)
    for name in used:
        assert AX.get(name).tag in AX.TAGS
    for a in AX.AXIOMS.values():
        assert a.tag in AX.TAGS, f"{a.name} has invalid tag {a.tag}"
    if ALL_PRESENT:
        assert "R1" in used, "R1 is never invoked"


def test_fallbacks_are_declared():
    """Every fallback axiom is listed in the ledger; an empty list prints 'none'."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        print_audit([])
    out = buf.getvalue()
    assert "FALLBACKS" in out and "HEADLINE" in out
    fb = AX.fallbacks()
    if fb:
        for a in fb:
            assert a.name in out, f"fallback {a.name} missing from ledger"
            assert a.role.strip() and a.failure_mode.strip()
    else:
        assert "none" in out
    for a in AX.by_tag(AX.REGULARITY):
        assert "interpretive role" in out and "failure mode" in out and a.name in out


@pytest.mark.skipif(not ALL_PRESENT, reason="needs all ten lemma modules")
def test_every_axiom_is_used():
    _, used = run_chain(verbose=False)
    unused = [
        n
        for n in AX.AXIOMS
        if n not in used
        and n not in AX.STRUCTURAL
        and n not in AX.SOLVER_LEVEL
        and n not in AX.CITED_CONTEXT
    ]
    assert not unused, f"axioms never used by any lemma: {unused}"


# --- lemmas L6,L8 ---
def _run_lemma(mod_name):
    import importlib

    mod = importlib.import_module(f"derivation.{mod_name}")
    ctx = {"S": S.make_symbols()}
    mod.derive(ctx)
    mod.verify(ctx)
    return mod, ctx


def test_L6_gaussian_cumulant_abstract():
    mod, ctx = _run_lemma("lemma_06_gaussian_cumulant")
    assert {"A2", "A5", "I5"} <= set(mod.AXIOMS_USED)
    r = ctx["L6"]
    assert sp.simplify(r["mgf1"] - sp.exp(ctx["S"].sigma ** 2 * r["t"] ** 2 / 2)) == 0
    assert r["norm2"].limits[0][2] == ctx["S"].d  # symbolic d, not a number


def test_L8_chart_abstract():
    mod, ctx = _run_lemma("lemma_08_helmert_chart")
    assert {"A7", "I6"} <= set(mod.AXIOMS_USED)
    assert AX.get("I6").tag == AX.INHERITED and AX.get("I6").citation.strip()
    assert AX.get("A7").tag == AX.POSITED
    assert AX.get("A7").role.strip() and AX.get("A7").failure_mode.strip()
    r = ctx["L8"]
    assert r["shifted"] == r["Z"]
    assert r["Q"].shape == (ctx["S"].d, ctx["S"].d)


def test_L8_A7_fails_without_kernel_hypothesis():
    """Negative control: without B 1 = 0 the shifted chart keeps the c*B*1 term."""
    from sympy.matrices.expressions import OneMatrix

    S_ = S.make_symbols()
    one = OneMatrix(S_.d, 1)
    u = sp.MatrixSymbol("u_vec", S_.d, 1)
    assert (S_.B * (u + S_.c * one)).expand() != S_.B * u


def _l8_inputs():
    from sympy.matrices.expressions import OneMatrix

    S_ = S.make_symbols()
    return S_.B, sp.MatrixSymbol("u_vec", S_.d, 1), OneMatrix(S_.d, 1), S_.d


def test_L8_roundtrip_derived_positive():
    from derivation.lemma_08_helmert_chart import roundtrip_holds

    assert roundtrip_holds(*_l8_inputs())


def test_L8_roundtrip_fails_without_orthonormality():
    """Negative control: dropping B B^T = I (A7) leaves Q Q^T != I, so the round trip fails."""
    from derivation.lemma_08_helmert_chart import roundtrip_holds

    assert not roundtrip_holds(*_l8_inputs(), use_orth=False)


def test_L8_roundtrip_fails_without_kernel():
    """Negative control: dropping B 1 = 0 (A7) leaves off-diagonal Gram blocks nonzero."""
    from derivation.lemma_08_helmert_chart import roundtrip_holds

    assert not roundtrip_holds(*_l8_inputs(), use_ker=False)


def test_L8_roundtrip_fails_without_I6():
    """Negative control: without I6, Q^T Q stays B^T B + (1/d) 1 1^T and (Q^T Q) u != u."""
    from derivation.lemma_08_helmert_chart import roundtrip_holds

    B, u, one, d = _l8_inputs()
    assert not roundtrip_holds(B, u, one, d, use_I6=False)
    QtQ = sp.block_collapse(
        sp.BlockMatrix([[B], [one.T / sp.sqrt(d)]]).T * sp.BlockMatrix([[B], [one.T / sp.sqrt(d)]])
    )
    assert QtQ != sp.Identity(d)


def test_crosscheck_L8_helmert_realization_d4():
    """Concrete realization check only (NOT the theorem): Helmert basis at d = 4 satisfies A7."""
    d = 4
    rows = []
    for k in range(1, d):
        row = [1] * k + [-k] + [0] * (d - k - 1)
        rows.append([sp.Integer(x) / sp.sqrt(k * (k + 1)) for x in row])
    Bc = sp.Matrix(rows)
    assert Bc.shape == (d - 1, d)
    assert sp.simplify(Bc * Bc.T) == sp.eye(d - 1)
    assert sp.simplify(Bc * sp.ones(d, 1)) == sp.zeros(d - 1, 1)


# --- lemmas L3,L4 ---
from derivation import lemma_03_gradient_kkt as _L3  # noqa: E402
from derivation import lemma_04_convexity as _L4  # noqa: E402


def _ctx_l3_l4():
    ctx = {"S": S.make_symbols()}
    _L3.derive(ctx)
    _L3.verify(ctx)
    _L4.derive(ctx)
    _L4.verify(ctx)
    return ctx


def test_L3_L4_verify_abstractly_with_declared_axioms():
    ctx = _ctx_l3_l4()
    for mod in (_L3, _L4):
        assert all(a in AX.AXIOMS for a in mod.AXIOMS_USED)
    assert "R1" in _L3.AXIOMS_USED
    assert "A3" in _L4.AXIOMS_USED
    assert ctx["L3"]["KKT"].rhs == _L3.LAM  # (U^T p)_{j0} = lambda
    assert ctx["L4"]["convex"] is True


def test_L3_directional_derivative_is_softmax_weighted_and_wrong_claim_fails():
    ctx = _ctx_l3_l4()
    Sy, c = ctx["S"], ctx["L3"]
    wrong = sp.Sum(c["sv"](Sy.i), (Sy.i, 1, Sy.n)) / Sy.n  # uniform weights, not softmax
    wrong_L = sp.Sum(c["sv"](_L3.L), (_L3.L, 1, Sy.n)) / Sy.n
    assert wrong != wrong_L
    assert sp.simplify(_L3.linearize(c["dJ"]) - _L3.linearize(wrong_L)) != 0


def test_L4_second_derivative_is_tau_variance_and_needs_normalization():
    ctx = _ctx_l3_l4()
    Sy, c = ctx["S"], ctx["L4"]
    # a wrong factor (tau**2 instead of tau) is rejected by the same check
    p_def, sv = ctx["L3"]["p_def"], ctx["L3"]["sv"]
    n = Sy.n
    var = (
        sp.Sum(p_def(_L3.L) * sv(_L3.L) ** 2, (_L3.L, 1, n))
        - sp.Sum(p_def(_L3.L) * sv(_L3.L), (_L3.L, 1, n)) ** 2
    )
    assert sp.simplify(_L3.linearize(c["d2"]) - Sy.tau**2 * _L3.linearize(var)) != 0


def test_L4_sign_argument_is_per_term_then_net():
    ctx = _ctx_l3_l4()
    Sy, c = ctx["S"], ctx["L4"]
    a_r, s_r = c["a_r"], c["s_r"]
    term = sp.exp(Sy.tau * a_r[Sy.i])
    assert term.is_positive is True
    # without realness the per-term sign is not available
    plain = sp.exp(Sy.tau * Sy.u[Sy.i, Sy.j])
    assert plain.is_positive is not True
    assert (s_r[Sy.i] - s_r[Sy.k]) ** 2 >= 0


# --- lemmas L1,L2,L5,L7,L9,L10 ---
import importlib as _il  # noqa: E402

_MY_LEMMAS = {
    1: "lemma_01_homogeneity",
    2: "lemma_02_shift",
    5: "lemma_05_lse_lme",
    7: "lemma_07_elasticities",
    9: "lemma_09_pullback",
    10: "lemma_10_extension",
}


def _run_lemmas(*numbers):
    """derive+verify the listed lemmas (L7 reads L1 through ctx) on a fresh abstract ctx."""
    ctx = {"S": S.make_symbols()}
    mods = {}
    for n in numbers:
        mods[n] = _il.import_module(f"derivation.{_MY_LEMMAS[n]}")
        mods[n].derive(ctx)
        mods[n].verify(ctx)
    return ctx, mods


@pytest.mark.parametrize("num", sorted(_MY_LEMMAS))
def test_lemma_L1_L2_L5_L7_L9_L10_verify_abstractly(num):
    needs = (1, num) if num == 7 else (num,)
    ctx, mods = _run_lemmas(*needs)
    mod = mods[num]
    assert mod.TITLE and mod.STATEMENT and mod.AXIOMS_USED
    for name in mod.AXIOMS_USED:
        assert name in AX.AXIOMS
    # abstract: sizes stay symbolic, no concrete dimension in the lemma state
    assert ctx["S"].d.is_integer and not ctx["S"].d.is_number


@pytest.mark.parametrize("num", sorted(_MY_LEMMAS))
def test_lemma_L1_L2_L5_L7_L9_L10_no_enumeration(num):
    import inspect

    src = inspect.getsource(_il.import_module(f"derivation.{_MY_LEMMAS[num]}"))
    assert "range(" not in src, f"L{num}: loop over concrete sizes"
    assert "numpy" not in src and "scipy" not in src and "random" not in src


def test_L1_fails_loudly_when_formula_broken():
    ctx, mods = _run_lemmas(1)
    ctx["L1"]["Vk"] = ctx["L1"]["Vk"] * 2  # V(k m) = 2 k V(m): wrong
    with pytest.raises(AssertionError, match="L1 FAIL"):
        mods[1].verify(ctx)


def test_L2_fails_loudly_when_shift_broken():
    ctx, mods = _run_lemmas(2)
    ctx["L2"]["J_shifted_reduced"] = ctx["L2"]["J_shifted_reduced"] + 1
    with pytest.raises(AssertionError, match="L2 FAIL"):
        mods[2].verify(ctx)


def test_L5_limits_and_fallback_recorded():
    ctx, _ = _run_lemmas(5)
    r = ctx["L5"]
    assert sp.simplify(r["lim_zero"] - r["mean"]) == 0
    assert sp.simplify(r["lim_lower"] - ctx["S"].M) == 0
    assert "F5" in _il.import_module("derivation.lemma_05_lse_lme").AXIOMS_USED
    assert AX.get("F5").fallback and AX.get("F5").role and AX.get("F5").failure_mode
    assert "SLLN" in r["consistency_remark"] and "support function" in r["support_function_remark"]


def test_L5_fails_loudly_when_limit_wrong():
    ctx, mods = _run_lemmas(5)
    ctx["L5"]["lim_zero"] = ctx["L5"]["lim_zero"] + 1
    with pytest.raises(AssertionError, match="L5 FAIL"):
        mods[5].verify(ctx)


def test_L7_fails_loudly_when_elasticity_wrong():
    ctx, mods = _run_lemmas(1, 7)
    ctx["L7"]["x_sol"] = -ctx["L7"]["x_sol"]  # +w_k/w_j: wrong sign
    with pytest.raises(AssertionError, match="L7 FAIL"):
        mods[7].verify(ctx)


def test_L9_fails_loudly_when_exponent_wrong():
    ctx, mods = _run_lemmas(9)
    ctx["L9"]["target"] = ctx["L9"]["target"] * 2
    with pytest.raises(AssertionError, match="L9 FAIL"):
        mods[9].verify(ctx)


def test_L10_fails_loudly_when_limit_wrong_and_fallback_recorded():
    ctx, mods = _run_lemmas(10)
    assert AX.get("F10").fallback and "F10" in mods[10].AXIOMS_USED
    ctx["L10"]["lim_lower"] = ctx["L10"]["lim_lower"] + 1
    with pytest.raises(AssertionError, match="L10 FAIL"):
        mods[10].verify(ctx)


# --- numeric I1/I2 and cross-checks ---
import numpy as np  # noqa: E402
from scipy.optimize import linprog, minimize  # noqa: E402


@pytest.mark.parametrize("d", [2, 3, 4])
def test_lp_duality_numeric(d):
    """I1 (LP / minimax duality), numeric: min_{w in simplex_d} max_i w.u_i
    = max_{lam in simplex_N} min_j (U^T lam)_j.  Numeric check of an inherited fact only."""
    N = 8
    rng = np.random.default_rng(0)
    U = rng.normal(size=(N, d))
    # primal: variables (w_1..w_d, z); min z s.t. U w - z <= 0, sum w = 1, w >= 0
    c = np.r_[np.zeros(d), 1.0]
    A_ub = np.c_[U, -np.ones(N)]
    primal = linprog(
        c,
        A_ub=A_ub,
        b_ub=np.zeros(N),
        A_eq=[np.r_[np.ones(d), 0.0]],
        b_eq=[1.0],
        bounds=[(0, None)] * d + [(None, None)],
        method="highs",
    )
    # dual: variables (lam_1..lam_N, y); max y s.t. y - (U^T lam)_j <= 0, sum lam = 1, lam >= 0
    cd = np.r_[np.zeros(N), -1.0]
    A_ub_d = np.c_[-U.T, np.ones(d)]
    dual = linprog(
        cd,
        A_ub=A_ub_d,
        b_ub=np.zeros(d),
        A_eq=[np.r_[np.ones(N), 0.0]],
        b_eq=[1.0],
        bounds=[(0, None)] * N + [(None, None)],
        method="highs",
    )
    assert primal.status == 0 and dual.status == 0
    assert abs(primal.fun - (-dual.fun)) < 1e-7


def _lme(U, w, tau):
    z = tau * (U @ w)
    mx = z.max()
    return (mx + np.log(np.mean(np.exp(z - mx)))) / tau


def test_replication_invariance():
    """I2: replicating each row r times leaves the log-mean-exp J_tau (and its minimizer)
    unchanged. numpy/scipy only; no import of src/."""
    rng = np.random.default_rng(1)
    N, d, r, tau = 6, 3, 3, 1.7
    U = rng.normal(size=(N, d))
    Ur = np.repeat(U, r, axis=0)
    for _ in range(3):
        w = rng.dirichlet(np.ones(d))
        assert abs(_lme(U, w, tau) - _lme(Ur, w, tau)) < 1e-9

    def argmin(M):
        res = minimize(
            lambda w: _lme(M, w, tau),
            np.ones(d) / d,
            method="SLSQP",
            bounds=[(0, 1)] * d,
            constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
            options={"ftol": 1e-14, "maxiter": 500},
        )
        assert res.success
        return res.x

    assert np.max(np.abs(argmin(U) - argmin(Ur))) < 1e-6


# ---- substitution cross-checks of the ABSTRACT lemma results (ctx), per (d, n, K) ----
_DNK = [(2, 2, 1), (3, 3, 2), (4, 3, 3)]
_TOL = sp.Float("1e-18")


@pytest.fixture(scope="module")
def _ctx_all():
    ctx, _ = run_chain(verbose=False)
    return ctx


def _val(name, idx, dnk):
    """Deterministic concrete entries for every IndexedBase (rationals, exact)."""
    d, _n, _K = dnk
    R = sp.Rational
    if name == "w":
        return R(idx[0], d * (d + 1) // 2)  # on the simplex
    if name == "theta":
        k, j = idx
        return R(j + k, sum(jj + k for jj in range(1, d + 1)))  # each row on the simplex
    if name == "u":
        return R((3 * idx[0] + 5 * idx[-1]) % 7 - 3, 4)
    if name == "v":
        return R((-1) ** idx[0] * idx[0], 5)
    if name == "m":
        return R(idx[0] + 1, 2)
    if name == "s":
        return R(idx[0] ** 2, 3) - 1
    if name == "beta":
        return R(idx[0], 3)
    if name == "a":
        return R(idx[0], 2)
    if name == "alpha":
        return R(idx[0], 4)
    if name == "b":
        return R(idx[0], 5)
    if name == "r":
        return R(idx[0] + 2, 3)
    if name == "u_pt":
        return R(idx[0], 3)
    if name == "eps":
        return R(idx[0], 2)
    raise KeyError(name)


def _conc(expr, dnk, S_, extra=None, override=None):
    """Substitute sizes + named scalars, expand Sums explicitly, then concrete entries, evalf."""
    d, n, K = dnk
    sub = {S_.d: d, S_.n: n, S_.K: K}
    sub.update(extra or {})
    e = expr.subs(sub).doit()
    rep = {}
    for at in e.atoms(sp.Indexed):
        nm = str(at.base)
        idx = tuple(int(x) for x in at.indices)
        if override and nm in override:
            rep[at] = override[nm](idx)
        else:
            rep[at] = _val(nm, idx, dnk)
    return sp.N(e.xreplace(rep), 30)


def _eq(a, b):
    assert abs(sp.N(a - b, 30)) < _TOL, f"{a} != {b}"


def _le(a, b):
    assert sp.N(a - b, 30) <= _TOL, f"{a} > {b}"


_TAU = sp.Rational(3, 2)
_PARAMS = pytest.mark.parametrize("dnk", _DNK, ids=lambda t: f"d{t[0]}_n{t[1]}_K{t[2]}")


@_PARAMS
def test_crosscheck_L1(_ctx_all, dnk):
    S_, r = _ctx_all["S"], _ctx_all["L1"]
    ex = {S_.k_scale: sp.Rational(5, 2), r["beta0"]: sp.Rational(1, 3)}
    V = _conc(r["V"], dnk, S_)
    _eq(_conc(r["Vk"], dnk, S_, ex), sp.Rational(5, 2) * V)
    _eq(_conc(r["V_tilde"], dnk, S_, ex), sp.exp(-sp.Rational(1, 3)) * V)
    _eq(_conc(r["V_prod_as_exp"], dnk, S_), V)
    _eq(_conc(r["V_inv_form"], dnk, S_), 1)


@_PARAMS
def test_crosscheck_L2(_ctx_all, dnk):
    S_, r = _ctx_all["S"], _ctx_all["L2"]
    ex = {S_.tau: _TAU, S_.c: sp.Rational(7, 3)}
    J = _conc(r["J"], dnk, S_, ex)
    _eq(_conc(r["J_shifted"], dnk, S_, ex), J + sp.Rational(7, 3))
    _eq(_conc(r["J_shifted_reduced"], dnk, S_, ex), J + sp.Rational(7, 3))


@_PARAMS
def test_crosscheck_L3(_ctx_all, dnk):
    """dJ (abstract directional derivative) vs exact softmax-weighted form and vs the
    difference quotient of the abstract J."""
    S_, r, r2 = _ctx_all["S"], _ctx_all["L3"], _ctx_all["L2"]
    d, n, _ = dnk
    ex = {S_.tau: _TAU}
    dJ = _conc(r["dJ"], dnk, S_, ex)
    # softmax weights p_i from the concrete w
    sc = [
        sum(_val("u", (i, j), dnk) * _val("w", (j,), dnk) for j in range(1, d + 1))
        for i in range(1, n + 1)
    ]
    Z = sum(sp.exp(_TAU * x) for x in sc)
    pv = {i: sp.exp(_TAU * sc[i - 1]) / Z for i in range(1, n + 1)}
    ov = {"p": lambda idx: pv[idx[0]]}
    _eq(_conc(r["lhs_abs"], dnk, S_, ex, ov), dJ)
    _eq(_conc(r["rhs_abs"], dnk, S_, ex, ov), dJ)
    _eq(_conc(r["dsimplex"], dnk, S_), sum(_val("v", (j,), dnk) for j in range(1, d + 1)))
    # central difference of the abstract J along w + t v (u-independent of t)
    h = sp.Rational(1, 10**8)
    Jw = r2["J"]
    wv = lambda sgn: lambda idx: _val("w", idx, dnk) + sgn * h * _val("v", idx, dnk)  # noqa: E731
    fd = (_conc(Jw, dnk, S_, ex, {"w": wv(1)}) - _conc(Jw, dnk, S_, ex, {"w": wv(-1)})) / (2 * h)
    # J (L2) is the log-MEAN-exp; its w-derivative equals that of the log-sum-exp, i.e. dJ.
    assert abs(sp.N(fd - dJ, 30)) < 1e-12


@_PARAMS
def test_crosscheck_L4(_ctx_all, dnk):
    S_, r = _ctx_all["S"], _ctx_all["L4"]
    d, n, _ = dnk
    ex = {S_.tau: _TAU}
    sc = [
        sum(_val("u", (i, j), dnk) * _val("w", (j,), dnk) for j in range(1, d + 1))
        for i in range(1, n + 1)
    ]
    Z = sum(sp.exp(_TAU * x) for x in sc)
    pv = {i: sp.exp(_TAU * sc[i - 1]) / Z for i in range(1, n + 1)}
    sv = {
        i: sum(_val("u", (i, j), dnk) * _val("v", (j,), dnk) for j in range(1, d + 1))
        for i in range(1, n + 1)
    }
    ov = {"p": lambda idx: pv[idx[0]], "s": lambda idx: sv[idx[0]]}
    var = _conc(r["var_abs"], dnk, S_, ex, ov)
    _eq(_conc(r["dbl_abs"], dnk, S_, ex, ov), 2 * var)
    _eq(_conc(r["d2"], dnk, S_, ex), _TAU * var)
    assert var >= 0


@_PARAMS
def test_crosscheck_L5(_ctx_all, dnk):
    S_, r = _ctx_all["S"], _ctx_all["L5"]
    n = dnk[1]
    ex = {S_.tau: _TAU}
    lse, lme = _conc(r["LSE"], dnk, S_, ex), _conc(r["LME"], dnk, S_, ex)
    _eq(lme, lse - sp.log(n) / _TAU)
    M = max(_val("s", (i,), dnk) for i in range(1, n + 1))
    mean = _conc(r["mean"], dnk, S_)
    _le(mean, lme)
    _le(lme, M)
    _le(M, lse)
    _le(M - sp.log(n) / _TAU, lme)
    _eq(_conc(r["lme_floor"], dnk, S_), mean)
    _eq(_conc(r["offset"], dnk, S_, ex), lse - lme)  # LSE - LME = log(n)/tau


@_PARAMS
def test_crosscheck_L6(_ctx_all, dnk):
    S_, r = _ctx_all["S"], _ctx_all["L6"]
    d = dnk[0]
    ex = {S_.tau: _TAU, S_.sigma: sp.Rational(5, 4)}
    sig, t = sp.Rational(5, 4), r["t"]
    # product of one-dimensional mgfs at t = tau w_j equals the closed form
    prod = sp.Integer(1)
    for j in range(1, d + 1):
        prod *= r["mgf1"].subs({S_.sigma: sig, t: _TAU * _val("w", (j,), dnk)})
    _eq(prod, _conc(r["mgf_closed"], dnk, S_, ex))
    _eq(sp.log(prod) / _TAU, _conc(r["cumulant"], dnk, S_, ex))
    _eq(_conc(r["cumulant"], dnk, S_, ex), _conc(r["target"], dnk, S_, ex))


@_PARAMS
def test_crosscheck_L7(_ctx_all, dnk):
    S_, r = _ctx_all["S"], _ctx_all["L7"]
    for jj in range(1, dnk[0] + 1):
        ex = {r["j0"]: jj, r["k0"]: 1}
        wj = _val("w", (jj,), dnk)
        xs = _conc(r["x_sol"], dnk, S_, ex)
        _eq(xs, -_val("w", (1,), dnk) / wj)
        dG = r["dG"].subs({r["j0"]: jj, r["k0"]: 1})
        wsub = {
            at: _val("w", tuple(int(i) for i in at.indices), dnk) for at in dG.atoms(sp.Indexed)
        }
        dGc = dG.xreplace(wsub)
        (xsym,) = dGc.free_symbols
        _eq(dGc.subs(xsym, xs), 0)
        lf = _conc(r["logf_star"], dnk, S_, ex)
        _eq(_conc(r["logV_new"], dnk, S_, {**ex, r["logf"]: lf}), 0)
        _eq(_conc(r["f_star"], dnk, S_, ex), sp.exp(lf))


@_PARAMS
def test_crosscheck_L8(_ctx_all, dnk):
    """Helmert realization of the abstract chart identities (A7 hypotheses and recon)."""
    ctxL8 = _ctx_all["L8"]
    assert ctxL8["hyp_orth"] is not None
    d = dnk[0]
    rows = []
    for k in range(1, d):
        rows.append(
            [sp.Integer(x) / sp.sqrt(k * (k + 1)) for x in [1] * k + [-k] + [0] * (d - k - 1)]
        )
    Bc = sp.Matrix(rows)
    uc = sp.Matrix([_val("u", (j + 1,), dnk) for j in range(d)])
    assert sp.simplify(Bc * Bc.T) == sp.eye(d - 1)  # hyp_orth
    assert sp.simplify(Bc * sp.ones(d, 1)) == sp.zeros(d - 1, 1)  # hyp_ker
    ell = sum(uc) / d
    recon = ell * sp.ones(d, 1) + Bc.T * Bc * uc  # abstract: ell*1 + B^T B u
    assert sp.simplify(recon - uc) == sp.zeros(d, 1)
    # shift equivariance: B (u + c 1) = B u
    assert sp.simplify(Bc * (uc + sp.Rational(3, 7) * sp.ones(d, 1)) - Bc * uc) == sp.zeros(
        d - 1, 1
    )


@_PARAMS
def test_crosscheck_L9(_ctx_all, dnk):
    S_, r = _ctx_all["S"], _ctx_all["L9"]
    d = dnk[0]
    beta0 = sp.Rational(1, 3)
    ex = {r["beta0"]: beta0}
    Vd = _conc(r["V_derived"], dnk, S_, ex)
    _eq(Vd, _conc(r["target"], dnk, S_, ex))
    direct = sp.exp(-beta0)
    for j in range(1, d + 1):
        direct *= (
            sp.exp(_val("b", (j,), dnk))
            * (_val("a", (j,), dnk) + _val("r", (j,), dnk)) ** _val("alpha", (j,), dnk)
        ) ** _val("w", (j,), dnk)
    _eq(Vd, direct)


@_PARAMS
def test_crosscheck_L10(_ctx_all, dnk):
    S_, r = _ctx_all["S"], _ctx_all["L10"]
    d, _n, K = dnk
    ex = {S_.kappa: _TAU, S_.c: 0, S_.K: K}
    phi = [
        -_val("beta", (k,), dnk)
        + sum(_val("theta", (k, j), dnk) * _val("u", (j,), dnk) for j in range(1, d + 1))
        for k in range(1, K + 1)
    ]
    M = max(phi)
    lse = _conc(r["base"], dnk, S_, ex) / _TAU
    _le(M, lse)
    _le(lse, M + sp.log(K) / _TAU)
    _eq(_conc(r["phi1"], dnk, S_), phi[0])
    _eq(_conc(r["ceil"], dnk, S_, ex), sp.log(K) / _TAU)
    # shift: u -> u + c adds c because each theta row sums to 1
    cc = sp.Rational(7, 3)
    _eq(_conc(r["shifted_reduced"], dnk, S_, {**ex, S_.c: cc}), cc + lse)
    # monomial form with m = exp(u)
    ov = {"m": lambda idx: sp.exp(_val("u", idx, dnk))}
    for k in range(1, K + 1):
        term = sp.exp(-_TAU * _val("beta", (k,), dnk)) * sp.exp(
            _TAU * sum(_val("theta", (k, j), dnk) * _val("u", (j,), dnk) for j in range(1, d + 1))
        )
        _eq(_conc(r["term_in_m"].subs(S_.k, k), dnk, S_, ex, {"m": ov["m"]}), term)


# --- L11: a V-maximizer is Pareto-efficient (WP9) ---
def _run_l11():
    import derivation.lemma_11_pareto as L11

    ctx = {"S": S.make_symbols()}
    L11.derive(ctx)
    L11.verify(ctx)
    return ctx, L11


def test_L11_verifies_abstractly_with_declared_axioms():
    ctx, L11 = _run_l11()
    assert L11.TITLE and L11.STATEMENT
    assert list(L11.AXIOMS_USED) == ["A2"]
    for name in L11.AXIOMS_USED:
        assert name in AX.AXIOMS
    assert ctx["S"].d.is_integer and not ctx["S"].d.is_number


def test_L11_in_chain_and_states_non_converse():
    from derivation.run import CHAIN_NAMES as names

    assert "lemma_11_pareto" in names
    _, L11 = _run_l11()
    assert "converse is not claimed" in L11.STATEMENT
    assert any(m.__name__.endswith("lemma_11_pareto") for m in CHAIN)


def test_L11_no_enumeration():
    import inspect

    src = inspect.getsource(_il.import_module("derivation.lemma_11_pareto"))
    assert "range(" not in src and "numpy" not in src and "scipy" not in src


def test_L11_fails_loudly_when_sign_claim_broken():
    ctx, L11 = _run_l11()
    ctx["L11"]["gain_nonneg"] = False
    with pytest.raises(AssertionError, match="L11 FAIL"):
        L11.verify(ctx)
    ctx, L11 = _run_l11()
    ctx["L11"]["ratio_gt1"] = sp.Interval(0, sp.oo)  # strictness claim made non-strict
    with pytest.raises(AssertionError, match="L11 FAIL"):
        L11.verify(ctx)


def test_I7_solver_level_inherited_entry():
    a = AX.get("I7")
    assert a.tag == AX.INHERITED and a.citation.strip() and "magnani2009convex" in a.citation
    assert a.role.strip() and a.failure_mode.strip()
    assert "I7" in AX.SOLVER_LEVEL
    buf = io.StringIO()
    with redirect_stdout(buf):
        print_audit(["A1", "A2"])
    assert "I7" in buf.getvalue() and "restarts" in buf.getvalue()


# --- WP13 (E-2, E-6): L3 full simplex KKT, L6 restricted to the population identity ---
def test_L3_states_full_simplex_kkt():
    assert "g_j >= lambda" in _L3.STATEMENT and "w_j (g_j - lambda) = 0" in _L3.STATEMENT
    assert "complementary slackness" in _L3.STATEMENT
    assert "does not imply an interior finite-tau minimizer" in _L3.STATEMENT


def test_L3_boundary_kkt_derives_symbolically_in_d():
    ctx = _ctx_l3_l4()
    c = ctx["L3"]
    Sy = ctx["S"]
    assert ctx["S"].d.is_integer and not ctx["S"].d.is_number
    # equal-gradient case is kept, the boundary KKT is added
    kb = c["KKT_boundary"]
    assert c["KKT"].rhs == _L3.LAM
    assert kb["lambda_solved"] == [sp.Sum(Sy.w[Sy.j] * kb["gr"][Sy.j], (Sy.j, 1, Sy.d))]
    assert kb["mu"][Sy.j].is_nonnegative is True  # g_j - lambda = mu_j >= 0
    assert kb["positive_case_solution"] == [0]  # w_j > 0 forces mu_j = 0: G_j = lambda


def test_L3_boundary_example_has_inactive_gradient_above_lambda():
    ctx = _ctx_l3_l4()
    ex = ctx["L3"]["boundary_example"]
    # balanced hard-support geometry at tau = inf, boundary optimizer at finite tau
    assert ex["hard_primal"] == ex["hard_dual"] == 1
    assert ex["w_star"] == (1, 0)
    assert ex["g_inactive_minus_lambda"].evalf() > 0


def test_L3_fails_loudly_when_boundary_claim_broken():
    ctx = _ctx_l3_l4()
    ctx["L3"]["KKT_boundary"]["lambda_solved"] = [
        sp.Sum(ctx["S"].p[ctx["S"].j], (ctx["S"].j, 1, ctx["S"].d))
    ]
    with pytest.raises(AssertionError, match="L3 FAIL"):
        _L3.verify(ctx)
    ctx = _ctx_l3_l4()
    ctx["L3"]["boundary_example"]["g_inactive_minus_lambda"] = -ctx["L3"]["boundary_example"][
        "g_inactive_minus_lambda"
    ]
    with pytest.raises(AssertionError, match="L3 FAIL"):
        _L3.verify(ctx)


def test_L6_statement_is_the_restricted_population_identity():
    L6 = _il.import_module("derivation.lemma_06_gaussian_cumulant")
    s = L6.STATEMENT
    assert "population" in s and "A5" in s and "independent across j" in s and "sigma > 0" in s
    assert "not a finite-sample estimator" in s and "no consistency claim" in s
    assert "A5" in L6.AXIOMS_USED


# --- WP13 (E-1): L12 facet gap, L13 margin, L14 assignment-stable local optimality ---
_WP13 = {
    12: "lemma_12_facet_gap",
    13: "lemma_13_margin",
    14: "lemma_14_assignment_stable",
}


def _run_wp13(*numbers):
    """derive+verify L3, L4 (L12 reads L4's convexity), then the listed WP13 lemmas."""
    ctx = {"S": S.make_symbols()}
    _L3.derive(ctx)
    _L3.verify(ctx)
    _L4.derive(ctx)
    _L4.verify(ctx)
    mods = {}
    for n in numbers:
        mods[n] = _il.import_module(f"derivation.{_WP13[n]}")
        mods[n].derive(ctx)
        mods[n].verify(ctx)
    return ctx, mods


@pytest.mark.parametrize("num", sorted(_WP13))
def test_wp13_lemmas_in_chain_in_order_and_no_enumeration(num):
    import inspect

    assert _WP13[num] in CHAIN_NAMES
    assert CHAIN_NAMES[-4:-1] == list(_WP13.values())  # L15 follows (Level 1)
    src = inspect.getsource(_il.import_module(f"derivation.{_WP13[num]}"))
    assert "range(" not in src and "numpy" not in src and "scipy" not in src


def test_L12_verifies_at_symbolic_d_with_declared_axioms():
    ctx, mods = _run_wp13(12)
    L12 = mods[12]
    assert L12.TITLE and L12.STATEMENT
    assert set(L12.AXIOMS_USED) >= {"A2", "I1", "I8", "F12"}
    for name in L12.AXIOMS_USED:
        assert name in AX.AXIOMS
    assert ctx["S"].d.is_integer and not ctx["S"].d.is_number
    assert ctx["L12"]["convex"] is True


def test_L12_statement_names_the_gap_the_chain_and_the_objects():
    _, mods = _run_wp13(12)
    s = mods[12].STATEMENT
    assert "G = g.w - min_j g_j = sum_j w_j (g_j - min g)" in s
    assert "0 <= f(w) - f* <= G" in s
    assert "w_j (g_j - min g) = 0" in s  # E-2's KKT, equality iff
    assert "fitted reference surface" in s and "tau = inf supporting envelope" in s
    assert "LP duality gap" in s


def test_L12_min_representation_fallback_and_inherited_first_order_inequality():
    _, mods = _run_wp13(12)
    assert AX.get("F12").fallback and AX.get("F12").role and AX.get("F12").failure_mode
    assert "F12" in mods[12].AXIOMS_USED
    a = AX.get("I8")
    assert a.tag == AX.INHERITED and "3.1.3" in a.citation and "Boyd" in a.citation
    assert a.role.strip() and a.failure_mode.strip()


def test_L12_lp_duality_gap_instance_is_exact():
    ctx, _ = _run_wp13(12)
    lp = ctx["L12"]["lp"]
    assert lp["gap_at_optimum"] == 0 and lp["primal_at_optimum"] == lp["dual_at_optimum"]
    assert lp["gap_off_optimum"] >= lp["f_off_optimum"] - lp["f_star"] >= 0


def test_L12_fails_loudly_when_gap_claim_broken():
    ctx, mods = _run_wp13(12)
    ctx["L12"]["gap_nonneg"] = False
    with pytest.raises(AssertionError, match="L12 FAIL"):
        mods[12].verify(ctx)
    ctx, mods = _run_wp13(12)
    ctx["L12"]["chain_slack"] = ctx["L12"]["chain_slack"] - 1  # G - (f - f*) != a + b
    with pytest.raises(AssertionError, match="L12 FAIL"):
        mods[12].verify(ctx)
    ctx, mods = _run_wp13(12)
    ctx["L12"]["lp"]["gap_at_optimum"] = 1
    with pytest.raises(AssertionError, match="L12 FAIL"):
        mods[12].verify(ctx)
    ctx, mods = _run_wp13(12)
    ctx["L4"]["convex"] = False  # L12 is conditional on L4's convexity
    with pytest.raises(AssertionError, match="L12 FAIL"):
        mods[12].verify(ctx)


def test_L13_verifies_with_declared_axioms_and_states_the_radius():
    ctx, mods = _run_wp13(13)
    L13 = mods[13]
    assert set(L13.AXIOMS_USED) >= {"F12", "I9", "R2"}
    for name in L13.AXIOMS_USED:
        assert name in AX.AXIOMS
    s = L13.STATEMENT
    assert "gamma - 2 delta" in s and "2 delta < gamma" in s
    assert "max_k ||Delta theta_k||_2 < gamma / (2 max_i ||(u_i, -1)||_2)" in s
    assert "energy differential" in s
    assert ctx["S"].d.is_integer and not ctx["S"].d.is_number


def test_wp13_new_axioms_are_declared_with_role_and_failure_mode():
    i9 = AX.get("I9")
    assert i9.tag == AX.INHERITED and "Horn" in i9.citation and "Matrix Analysis" in i9.citation
    assert i9.role.strip() and i9.failure_mode.strip()
    r2 = AX.get("R2")
    assert r2.tag == AX.REGULARITY and "positive assignment margin" in r2.statement
    assert r2.role.strip() and "unique maximizing" in r2.role and "Proposition 3" in r2.role
    assert "ridge" in r2.failure_mode and "stationary_without_margin" in r2.failure_mode
    assert "duplicate" in r2.failure_mode
    r1 = AX.get("R1")
    assert "does not imply" in r1.statement and "interior" in r1.statement


def test_L13_numeric_endpoint_labels_survive_the_radius():
    ctx, _ = _run_wp13(13)
    num = ctx["L13"]["numeric"]
    assert num["margin"] == 1 and num["perturbed_margin"] >= num["margin"] - 2 * num["delta"] > 0
    assert num["labels"] == num["labels_perturbed"]
    assert num["r"] < num["radius"]


def test_L13_fails_loudly_when_margin_claim_broken():
    for key, bad in (
        ("margin_slack", 1),  # new gap != (gamma - 2 delta) + slacks
        ("margin_nonneg", False),
        ("margin_positive", False),
        ("score_change_slack", 1),  # change in the score is not Delta theta . (u, -1)
    ):
        ctx, mods = _run_wp13(13)
        ctx["L13"][key] = bad
        with pytest.raises(AssertionError, match="L13 FAIL"):
            mods[13].verify(ctx)
    ctx, mods = _run_wp13(13)
    ctx["L13"]["radius_set"] = sp.Interval(0, sp.oo)  # radius not bounded by gamma / (2 U)
    with pytest.raises(AssertionError, match="L13 FAIL"):
        mods[13].verify(ctx)
    ctx, mods = _run_wp13(13)
    ctx["L13"]["numeric"]["perturbed_margin"] = -1
    with pytest.raises(AssertionError, match="L13 FAIL"):
        mods[13].verify(ctx)


def test_L14_verifies_at_symbolic_d_nk_K_with_declared_axioms():
    ctx, mods = _run_wp13(12, 13, 14)
    L14 = mods[14]
    assert set(L14.AXIOMS_USED) >= {"R2"}
    for name in L14.AXIOMS_USED:
        assert name in AX.AXIOMS
    assert ctx["S"].d.is_integer and not ctx["S"].d.is_number
    assert ctx["S"].K.is_integer and not ctx["S"].K.is_number
    assert ctx["L14"]["nk"].is_integer and not ctx["L14"]["nk"].is_number


def test_L14_statement_scopes_level_three_to_step_b_unpenalized_support_offsets():
    _, mods = _run_wp13(12, 13, 14)
    s = mods[14].STATEMENT
    assert "Level 3" in s and "step B" in s and "unpenalized" in s
    assert "beta_k = J_tau(U w_k)" in s and "support offsets" in s
    assert "n_k (beta_k - w_k.ubar_k)" in s
    assert "F(W') - F(W) = sum_k (n_k/N) (f_k(w'_k) - f_k(w_k)) >= 0" in s
    assert "F(W) - F*_fixed" in s and "sum_k (n_k/N) G_k" in s
    assert "fitted reference surface" in s


def test_L14_partition_regrouping_is_declared_by_A8_not_enumerated_and_not_a_fallback():
    import inspect

    mod = _il.import_module("derivation.lemma_14_assignment_stable")
    src = inspect.getsource(mod)
    assert "A8" in mod.AXIOMS_USED and "declared relation A8" in src
    assert not any("L14" in (a.statement + a.role) for a in AX.fallbacks())


def test_L14_fails_loudly_when_premise_or_step_broken():
    for key, bad in (
        ("regroup_swap_equal", False),
        ("local_min_slack", 1),
        ("local_min_nonneg", False),
        ("cor_slack", 1),
        ("cor_nonneg", False),
        ("objective_agrees", 1),
    ):
        ctx, mods = _run_wp13(12, 13, 14)
        ctx["L14"][key] = bad
        with pytest.raises(AssertionError, match="L14 FAIL"):
            mods[14].verify(ctx)
    # broken premises inherited from earlier lemmas
    ctx, mods = _run_wp13(12, 13, 14)
    ctx["L13"]["margin_positive"] = False  # R2 fails: no assignment-stable neighborhood
    with pytest.raises(AssertionError, match="L14 FAIL"):
        mods[14].verify(ctx)
    ctx, mods = _run_wp13(12, 13, 14)
    ctx["L12"]["chain_nonneg"] = False  # Lemma 1 not established
    with pytest.raises(AssertionError, match="L14 FAIL"):
        mods[14].verify(ctx)


def test_wp13_audit_lists_new_axioms_and_headline_names_fallbacks():
    _, used = run_chain(verbose=False)
    for name in ("I8", "I9", "F12", "R2"):
        assert name in used, f"{name} is consumed by no lemma"
    buf = io.StringIO()
    with redirect_stdout(buf):
        print_audit(used)
    out = buf.getvalue()
    head = out[out.index("HEADLINE") :]
    for name in ("I8", "I9"):
        assert name in out
    for name in ("R1", "R2", "F5", "F10", "F12"):
        assert f"{name}: buys:" in head and f"{name}: when it fails:" in head
    assert "L14" in out and "L12" in out and "L13" in out
    buf = io.StringIO()
    from derivation.run import main

    with redirect_stdout(buf):
        assert main() == 0
    assert "L1 -> L15" in buf.getvalue() and buf.getvalue().rstrip().endswith("ALL LEMMAS PASS.")


# --- WP10 C-1: L15, Level 1 (descent) ---
def test_L15_is_the_last_lemma_and_states_level_one_exactly():
    mod = _il.import_module("derivation.lemma_15_descent")
    assert CHAIN_NAMES[-1] == "lemma_15_descent"
    assert mod.STATEMENT == (
        "Level 1 (descent), step B unpenalized: reassigning every row to its maximizing facet "
        "does not increase the mean slack F, and refitting each facet to a minimizer of its "
        "convex facet objective does not increase F; so F is non-increasing along accepted "
        "iterations."
    )
    assert set(mod.AXIOMS_USED) == {"A8", "F12"}


def _run_L15():
    ctx, _ = _run_wp13(12, 13, 14)
    mod = _il.import_module("derivation.lemma_15_descent")
    mod.derive(ctx)
    mod.verify(ctx)
    return ctx, mod


def test_L15_verifies_and_fails_loudly_when_a_step_is_broken():
    ctx, mod = _run_L15()
    assert ctx["L15"]["nonincreasing"] is True
    for key, bad in (
        ("row_split", 1),
        ("on_maximizing", 1),
        ("reassign_diff", 1),
        ("reassign_nonneg", False),
        ("partition_identity", False),
        ("refit_diff", 1),
        ("refit_nonneg", None),
        ("total", 1),
    ):
        ctx, mod = _run_L15()
        ctx["L15"][key] = bad
        with pytest.raises(AssertionError, match="L15 FAIL"):
            mod.verify(ctx)
