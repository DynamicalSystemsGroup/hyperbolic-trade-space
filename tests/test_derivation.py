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
    unused = [n for n in AX.AXIOMS if n not in used and n not in AX.STRUCTURAL]
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
    assert "R1" in _L3.AXIOMS_USED and "A3" in _L3.AXIOMS_USED
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
