"""L20: noise on the metrics is a ridge on the exponents; the first-order shift.

Setting (symbolic d, n). Clean fit: w* minimizes J_tau(w) = (1/tau) log((1/n) Sum_i exp(tau w.u_i))
on the face of the simplex that its participating exponents span (R3); p = softmax(tau U w*),
C = Cov_p(u) the softmax-weighted covariance of the log metrics, G = U^T p the gradient. Noisy
table: u_i + eps_i, each row's noise a Gaussian vector with mean 0 and covariance Sigma (A9; for
independent equal levels Sigma = sigma^2 I, L6, and L18 turns a relative measurement error of
attribute j into the level sigma_j = delta_j / s_j). The ridge surrogate is the expected
exponential, J^R(w) = (1/tau) log E (1/n) Sum_i exp(tau w.(u_i + eps_i)), the logarithm of the
expectation of the noisy sum, not the expectation of the logarithm.

What this proves (symbolic d, n):
  1. J^R(w) = J_tau(w) + (tau/2) w'Sigma w exactly: the noise is a ridge of weight tau Sigma / 2
     on the clean objective (L18's cumulant, row by row; the rows need not be independent).
  2. The ridge has directional derivative tau v'Sigma w, and J_tau has the mixed second
     derivative tau Cov_p(v.u, delta.u) = tau v'C delta (L3, L4).
  3. At w*, with G_j = lambda (L3, the KKT conditions on the face), the first-order stationarity
     of J^R on the face (every tangent v, sum_j v_j = 0) is v'(C delta + Sigma w*) = 0, where the
     product Sigma delta (noise times shift) is set aside as second order; with P = I - 11'/d this
     is P C P delta = - P Sigma w*, and delta = - (P C P)^+ P Sigma w* (I18; delta is tangent and
     unique, R3). For Sigma = sigma^2 I it is delta = - sigma^2 (P C P)^+ P w*: tau cancels because
     the Hessian of J_tau is tau C and the ridge gradient is tau Sigma w.
  4. The shift is at most ||P Sigma w*|| / m for m the smallest eigenvalue of C on the tangent
     space (conditioning_ = tau m), when the shift is not zero; and it lowers the ridge to first
     order: delta'Sigma w* <= - m ||delta||^2 <= 0, so for Sigma = sigma^2 I the squared distance
     of the exponents from the uniform ones, ||w||^2 - 1/d, falls at first order. The lemma does
     not say each exponent moves toward 1/d: for a C that is not a multiple of the identity,
     they need not.

What this does NOT prove: that the noisy fit of a finite table lands at the minimizer of J^R
(that J^R is the logarithm of an expectation, not the expectation of a logarithm: the
difference is the slack of Jensen's inequality, which closes when the softmax weights spread over
many rows, and it is measured in tests/test_noise_ridge.py, not proved here); a bound on the
second-order remainder or a radius
within which the first-order shift is accurate (the linearisation drops terms of order
(noise)^2 and (shift)^2, and names the dropped term); anything at an exponent on the boundary of
the simplex or near it (R3 fails, and the projector of the face is then the wrong one); the
selection effect of the maximum under noise (L19 bounds the offset shift, not the exponents);
that the fitted rates are right: only how far noise of a given size moves them; any noise that
is not Gaussian, or weights fitted to the noisy table's own scaler.

Route: SymPy differentiation through the Sums for the mixed derivative (as L4); Fubini and
distributivity of finite sums for the matrix form; tagged Sum algebra for the projector P; the
Cauchy-Schwarz inequality (I9) and the Rayleigh bound (R3) for the size of the shift; the
pseudoinverse (I18) for the closed form.
"""

import sympy as sp
from sympy.stats import E

from derivation.axioms import A1, A3, A5, A9, I9, I18, R3
from derivation.lemma_03_gradient_kkt import L3_RESULT
from derivation.lemma_04_convexity import L4_RESULT
from derivation.lemma_18_noise_covariance import L18_RESULT
from derivation.licence import hypothesis_symbol, log_expand
from derivation.results import ProvedResult
from derivation.sumtools import fuse, linear, linearize, piece_in_range, push_in, replace_indexed

TITLE = "Noise on the metrics is a ridge on the exponents: the first-order shift"
STATEMENT = (
    "With rows u_i + eps_i, eps_i Gaussian with covariance Sigma (A9), the expected noisy "
    "exponential J^R(w) = (1/tau) log E (1/n) Sum_i exp(tau w.(u_i + eps_i)) equals J_tau(w) + "
    "(tau/2) w'Sigma w. At a clean minimizer w* interior to its face with C = Cov_p(u) positive "
    "definite on the tangent space (R3), the first-order condition of J^R on the face, with the "
    "product of noise and shift set aside, is P C P delta = - P Sigma w*, so delta = "
    "- (P C P)^+ P Sigma w* (P = I - 11'/d; for Sigma = sigma^2 I, delta = - sigma^2 (P C P)^+ P "
    "w*, with tau cancelled). When the shift is not zero its norm is at most ||P Sigma w*|| / m, "
    "m the smallest eigenvalue of C on the tangent space (conditioning_ = tau m), and "
    "delta'Sigma w* <= - m ||delta||^2 <= 0: the ridge falls at first order. First order only: "
    "no bound on the remainder, and no statement that the noisy fit of a finite table lands at "
    "the minimizer of J^R"
)
AXIOMS_USED = ["A1", "A3", "A5", "A9", "I9", "I18", "R3"]
L20_RESULT = ProvedResult("L20", STATEMENT)  # the corollary of Proposition 2 and Theorem 3

nd = hypothesis_symbol("nd", "positive", "When the shift is not zero")


def canon(expr, name="i"):
    """Rename the bound variable of every closed single-limit Sum to ``name`` (alpha-renaming),
    so that Sums over the same range compare structurally (as in L4)."""
    x0 = sp.Symbol(name, integer=True)

    def _ren(s):
        if len(s.limits) != 1 or len(s.limits[0]) != 3:
            return s
        x, a, b = s.limits[0]
        if x == x0 or x0 in s.function.free_symbols:
            return s
        return sp.Sum(s.function.xreplace({x: x0}), (x0, a, b))

    return expr.replace(lambda e: isinstance(e, sp.Sum), _ren)


def apply_normalization(expr, norm):
    """Substitute Sum_x p[x] -> 1 using the carried equation ``norm`` (as in L4)."""
    (lim,) = norm.lhs.limits
    base = norm.lhs.function.base

    def _is_norm(e):
        return (
            isinstance(e, sp.Sum)
            and len(e.limits) == 1
            and e.limits[0][1:] == lim[1:]
            and isinstance(e.function, sp.Indexed)
            and e.function.base == base
            and e.function.indices == (e.limits[0][0],)
        )

    return expr.replace(_is_norm, lambda e: norm.rhs)


def distribute(expr):
    """Product of finite Sums -> nested Sum (distributivity), so that Fubini can compare sides."""

    def _go(x):
        sums = [a for a in x.args if isinstance(a, sp.Sum)]
        if len(sums) < 2:
            return x
        out = sp.Mul(*[a for a in x.args if not isinstance(a, sp.Sum)])
        for s in sums:
            out = out * s.function
        for s in reversed(sums):
            out = sp.Sum(out, *s.limits)
        return out

    return expr.replace(lambda x: isinstance(x, sp.Mul), _go)


def fubini_form(expr):
    """Push constants in and fuse nested Sums into one multi-limit Sum (finite Fubini)."""
    expr = push_in(expr)
    for _ in range(6):
        expr = fuse(push_in(expr))
    return expr


def same_sum(a, b):
    """Two multi-limit Sums with the same summand and the same set of limits (Fubini)."""
    return a.function == b.function and set(a.limits) == set(b.limits)


def derive(ctx):
    S = ctx["S"]
    n, d, i, j, k, w, v, u = S.n, S.d, S.i, S.j, S.k, S.w, S.v, S.u
    m, h = sp.Symbol("m", integer=True), sp.Symbol("h", integer=True)  # column index, mean dummy
    lim_i, lim_j, lim_m = (i, 1, n), (j, 1, d), (m, 1, d)

    # ------------------------------------------------------------ 1. the ridge identity
    # [L20.1] A3: tau > 0
    tau = A3.positive(S.tau)
    # [L20.2] L18: the moment generating function of w.eps at tau is exp(tau^2 q / 2), q = w'Sigma w
    mgf, q = L18_RESULT.take(ctx, "mgf", "q")
    # [L20.3] A1: the scores w.u_i are real, represented by the real family s_r
    sr = A1.real_base("s_r")
    # [L20.4] A9: one row's noise w.eps has the centred normal law of the Gaussian vector
    Xr = A9.obj("lin")
    row_E = sp.simplify(E(sp.exp(tau * (sr[i] + Xr))))
    EX = linear(sp.Sum(row_E, lim_i)) / n  # E applied term by term to the finite sum
    LMEs = sp.log(sp.Sum(sp.exp(tau * sr[i]), lim_i) / n) / tau
    # [L20.5] A9: q = Sum_j Sum_l w_j Sigma_jl w_l, the quadratic form of the covariance
    _q_def, qform = A9.rule(0)
    # [L20.6] A9: the covariance is symmetric, Sigma_lj = Sigma_jl
    sym_from, sym_to = A9.rule(2)
    # [L20.7] A9: the entries Sigma_jl of the covariance
    Sg = A9.obj("cov")
    l_ = sym_from.indices[0]  # the inner index of the quadratic form

    # ------------------------------------------------- 2. the derivatives of the two parts
    r = sp.Symbol("r", real=True)
    dridge = sp.diff(tau / 2 * replace_indexed(qform, w, lambda x: w[x] + r * v[x]), r).subs(r, 0)
    A_f = Sg[j, l_] * v[j] * w[l_]  # Sigma_jl v_j w_l
    B_f = Sg[j, l_] * v[l_] * w[j]  # Sigma_jl v_l w_j
    # the second term with j and l renamed (the double sum runs over one range)
    B_renamed = B_f.xreplace({j: l_, l_: j})
    # [L20.8] A9: with Sigma_lj = Sigma_jl, the renamed second term is the first
    B_sym = B_renamed.xreplace({sym_from: sym_to})

    # [L20.9] L3: the softmax weights p, the scores v.u_i, the balanced KKT G_j = lambda, and the
    # derivative Sum_j v_j of the simplex constraint
    p_def, sv, kkt, dsimplex = L3_RESULT.take(ctx, "p_def", "sv", "KKT", "dsimplex")
    # [L20.10] L4: the second derivative of J_tau(w + t v) at t = 0, tau Var_p(v.u)
    L4_d2 = L4_RESULT.take(ctx, "d2")
    dl = sp.IndexedBase("dl")  # the shift delta, a tangent direction

    def sd(x):  # delta . u_x
        return sp.Sum(u[x, j] * dl[j], lim_j)

    ta, tr, ls = (
        sp.Symbol("ta", real=True),
        sp.Symbol("tr", real=True),
        sp.Symbol("l", integer=True),
    )

    def plane_line(x):  # (w + ta delta + tr v) . u_x
        return sp.Sum((w[j] + ta * dl[j] + tr * v[j]) * u[x, j], lim_j)

    J_plane = sp.log(sp.Sum(sp.exp(tau * plane_line(ls)), (ls, 1, n)) / n) / tau
    mixed = sp.diff(J_plane, ta, tr).subs({ta: 0, tr: 0})
    mixed_vv = replace_indexed(mixed, dl, lambda x: v[x])  # the same, along delta = v
    lim_L = (ls, 1, n)
    cov_dir = sp.Sum(p_def(ls) * sv(ls) * sd(ls), lim_L) - (
        sp.Sum(p_def(ls) * sv(ls), lim_L) * sp.Sum(p_def(ls) * sd(ls), lim_L)
    )
    pair_dir = (
        sp.Sum(sp.Sum(p_def(ls) * p_def(k) * (sv(ls) - sv(k)) * (sd(ls) - sd(k)), (k, 1, n)), lim_L)
        / 2
    )
    # the abstract identity 2 Cov_p(s1, s2) = Sum_i Sum_k p_i p_k (s1_i - s1_k)(s2_i - s2_k)
    pa, s1, s2 = S.p, S.s, sp.IndexedBase("s2")
    pair_abs = (
        sp.Sum(sp.Sum(pa[ls] * pa[k] * (s1[ls] - s1[k]) * (s2[ls] - s2[k]), (k, 1, n)), lim_L) / 2
    )
    cov_abs = sp.Sum(pa[ls] * s1[ls] * s2[ls], lim_L) - (
        sp.Sum(pa[ls] * s1[ls], lim_L) * sp.Sum(pa[ls] * s2[ls], lim_L)
    )
    pair_norm = sp.expand(apply_normalization(canon(linearize(pair_abs), "l"), S.p_normalized))
    pair_unnorm = sp.expand(canon(linearize(pair_abs), "l"))

    # the matrix C_jm = Cov_p(u_j, u_m) in pair form, and v'C delta
    Cm = sp.IndexedBase("C")  # the entries C_jm

    def C_pair(a, b):
        return (
            sp.Sum(
                sp.Sum(
                    p_def(ls) * p_def(k) * (u[ls, a] - u[k, a]) * (u[ls, b] - u[k, b]), (k, 1, n)
                ),
                lim_L,
            )
            / 2
        )

    vCd_abs = sp.Sum(sp.Sum(v[j] * Cm[j, m] * dl[m], lim_m), lim_j)
    vCd = vCd_abs.replace(
        lambda e: isinstance(e, sp.Indexed) and e.base == Cm, lambda e: C_pair(*e.indices)
    )
    dsv = sp.Sum(v[j] * (u[ls, j] - u[k, j]), lim_j)  # v.u_i - v.u_k
    dsd_j = sp.Sum(dl[j] * (u[ls, j] - u[k, j]), lim_j)  # delta.u_i - delta.u_k
    dsd = dsd_j.xreplace({j: m})  # the same Sum under the dummy m (alpha-renaming)
    pair_matrix = sp.Sum(sp.Sum(p_def(ls) * p_def(k) * distribute(dsv * dsd), (k, 1, n)), lim_L) / 2

    # ------------------------------------------- 3. the first-order condition on the tangent space
    z = sp.IndexedBase("z")  # a generic vector, for the algebra of the projector

    def Pf(f, x, dummy=h):  # (P f)_x = f_x - mean(f)
        return f(x) - sp.Sum(f(dummy), (dummy, 1, d)) / d

    def zf(x):
        return z[x]

    def Sw(x):  # (Sigma w)_x
        return sp.Sum(Sg[x, l_] * w[l_], (l_, 1, d))

    def Cd(x):  # (C delta)_x
        return sp.Sum(Cm[x, m] * dl[m], lim_m)

    def force(x):  # the first-order force (C delta + Sigma w)_x
        return Cd(x) + Sw(x)

    h2 = sp.Symbol("h2", integer=True)

    def Pdl(x):  # (P delta)_x
        return Pf(lambda y: dl[y], x, h2)

    def CPd(x):  # (C P delta)_x
        return sp.Sum(Cm[x, m] * Pdl(m), lim_m)

    def Xd(x):  # (P C P delta)_x
        return Pf(CPd, x)

    def yv(x):  # (P Sigma w)_x
        return Pf(Sw, x)

    # R3, I9, I18
    # [L20.11] R3: m > 0, the smallest eigenvalue of C on the tangent space
    mc = R3.positive_symbol("m_c")
    # [L20.12] R3: the Rayleigh bound delta'C delta - m ||delta||^2 = s1 >= 0
    s_r3 = R3.nonneg_symbol("s_r3")
    # [L20.13] I9: the Cauchy-Schwarz slack ||delta|| ||y|| - |delta.y| = cs >= 0
    cs = I9.slack_symbol("cs")
    ny, A_sym, B_sym_ = (sp.Symbol(x, real=True) for x in ("ny", "A_form", "B_form"))
    VV = sp.Sum(dl[j] ** 2, lim_j)  # ||delta||^2 = nd^2
    A_expr = vCd_abs.xreplace({v: dl})  # delta'C delta
    B_expr = sp.Sum(sp.Sum(Sg[j, l_] * dl[j] * w[l_], (l_, 1, d)), lim_j)  # delta'Sigma w
    # [L20.14] R3: the Rayleigh slack delta'C delta - m ||delta||^2, nonnegative
    rayleigh = R3.slack_expr(rq_form=A_sym, m_curv=mc, vv_norm2=nd**2)
    # [L20.15] I9: the Cauchy-Schwarz gap ||delta|| ||y|| - |delta.y|, nonnegative
    cs_slack = I9.slack_expr(a_dot_b=B_sym_, norm_a=nd, norm_b=ny)
    # [L20.16] I18: if delta is in the range of X = P C P and X delta = - y, then delta = - X^+ y
    pin_range, pin_eq, pin_out = I18.obj("range"), I18.obj("equation"), I18.obj("conclusion")
    range_ok = mc.is_positive is True  # X is positive definite on the tangent space, R3

    # [L20.17] A5: sigma > 0, the common level of the equal-noise reading Sigma = sigma^2 I
    sigma = A5.positive(S.sigma)
    ctx["L20"] = dict(
        tau=tau, mgf=mgf, q=q, sr=sr, row_E=row_E, EX=EX, LMEs=LMEs, qform=qform, Sg=Sg, l_=l_,
        dridge=dridge, A_f=A_f, B_f=B_f, B_sym=B_sym, p_def=p_def, sv=sv, kkt=kkt,
        dsimplex=dsimplex, L4_d2=L4_d2, dl=dl, mixed=mixed, mixed_vv=mixed_vv, cov_dir=cov_dir,
        pair_dir=pair_dir, pair_norm=pair_norm, pair_unnorm=pair_unnorm, cov_abs=cov_abs,
        pair_abs=pair_abs, Cm=Cm, vCd_abs=vCd_abs, vCd=vCd, pair_matrix=pair_matrix,
        dsv=dsv, dsd=dsd, dsd_j=dsd_j, m=m, h=h, h2=h2, sigma=sigma, z=z, Pf=Pf, zf=zf, Sw=Sw,
        Cd=Cd, force=force, Pdl=Pdl,
        CPd=CPd, Xd=Xd, yv=yv, mc=mc, s_r3=s_r3, cs=cs, ny=ny, A_sym=A_sym, B_sym_=B_sym_,
        VV=VV, A_expr=A_expr, B_expr=B_expr, rayleigh=rayleigh, cs_slack=cs_slack,
        pin_range=pin_range, pin_eq=pin_eq, pin_out=pin_out, range_ok=range_ok, C_pair=C_pair,
    )  # fmt: skip


def verify(ctx):
    S = ctx["S"]
    r = ctx["L20"]
    d, n, i, j, k, w, v, u = S.d, S.n, S.i, S.j, S.k, S.w, S.v, S.u
    tau, mgf, q, sr = r["tau"], r["mgf"], r["q"], r["sr"]
    Sg, l_, dl, h, h2, m = r["Sg"], r["l_"], r["dl"], r["h"], r["h2"], r["m"]
    lim_i, lim_j = (i, 1, n), (j, 1, d)

    # ---------------------------------------------------------------- 1. the ridge identity
    # [L20.18] one row: E exp(tau (s_i + w.eps)) = exp(tau s_i) exp(tau^2 q / 2)
    assert sp.simplify(r["row_E"] - sp.exp(tau * sr[i]) * mgf) == 0, "L20 FAIL row expectation"
    # [L20.19] the expected noisy average is exp(tau^2 q / 2) times the clean average
    assert sp.simplify(r["EX"] - mgf * sp.Sum(sp.exp(tau * sr[i]), lim_i) / n) == 0, (
        "L20 FAIL expected noisy average"
    )
    # [L20.20] the logarithm of the expectation is J_tau + tau q / 2: the ridge identity
    assert (
        sp.simplify(log_expand(sp.log(r["EX"]), A1, A3, A9) / tau - (r["LMEs"] + tau * q / 2)) == 0
    ), "L20 FAIL ridge identity"

    # ------------------------------------------------------ 2. the derivatives of the two parts
    dsum = next(a for a in sp.Mul.make_args(r["dridge"]) if isinstance(a, sp.Sum))
    # [L20.21] the ridge derivative along v is (tau/2) Sum_jl Sigma_jl (v_j w_l + v_l w_j)
    assert sp.simplify(dsum.function - (r["A_f"] + r["B_f"])) == 0, "L20 FAIL ridge derivative"
    # [L20.22] the second term equals the first (Sigma symmetric): the derivative is tau v'Sigma w
    assert r["B_sym"] == r["A_f"], "L20 FAIL ridge gradient is tau Sigma w"
    # [L20.23] L4: the mixed derivative along (delta, v) with delta = v is L4's second derivative
    assert sp.simplify(linearize(r["mixed_vv"]) - linearize(r["L4_d2"])) == 0, (
        "L20 FAIL mixed derivative against L4"
    )
    # [L20.24] the mixed second derivative is tau Cov_p(v.u, delta.u)
    assert sp.simplify(linearize(r["mixed"]) - tau * linearize(r["cov_dir"])) == 0, (
        "L20 FAIL mixed derivative is tau Cov"
    )
    L_ = S.L
    ls = L_
    # [L20.25] the softmax weights satisfy sum_i p_i = 1
    assert sp.simplify(linearize(sp.Sum(r["p_def"](L_), (L_, 1, n))) - S.p_normalized.rhs) == 0, (
        "L20 FAIL softmax not normalized"
    )
    # [L20.26] with sum_i p_i = 1: 2 Cov_p(s1, s2) = Sum_i Sum_k p_i p_k (s1_i - s1_k)(s2_i - s2_k)
    assert sp.simplify(r["pair_norm"] - sp.expand(canon(r["cov_abs"], "l"))) == 0, (
        "L20 FAIL pair form of the covariance"
    )
    # [L20.27] negative control: without sum_i p_i = 1 the identity fails, so it is used
    assert sp.simplify(r["pair_unnorm"] - sp.expand(canon(r["cov_abs"], "l"))) != 0, (
        "L20 FAIL normalization not load-bearing"
    )
    pa, s1, s2 = S.p, S.s, sp.IndexedBase("s2")

    def inst(expr):
        expr = replace_indexed(expr, pa, r["p_def"])
        expr = replace_indexed(expr, s1, r["sv"])
        return replace_indexed(expr, s2, lambda x: sp.Sum(u[x, j] * dl[j], lim_j))

    # [L20.28] the abstract identity at the softmax weights and the scores v.u, delta.u
    assert inst(r["cov_abs"]) == r["cov_dir"] and inst(r["pair_abs"]) == r["pair_dir"], (
        "L20 FAIL instance of the covariance identity"
    )
    # [L20.29] v.u_i - v.u_k = Sum_j v_j (u_ij - u_kj), likewise for delta
    assert (
        sp.simplify(linearize(r["sv"](ls) - r["sv"](k) - r["dsv"])) == 0
        and sp.simplify(
            linearize(sp.Sum(u[ls, j] * dl[j], lim_j) - sp.Sum(u[k, j] * dl[j], lim_j) - r["dsd_j"])
        )
        == 0
    ), "L20 FAIL differences of scores"
    # [L20.30] the pair form of Cov_p(v.u, delta.u) is v'C delta with C_jm = (1/2) Sum_ik p_i p_k
    # (u_ij - u_kj)(u_im - u_km) (Fubini over the four sums)
    assert same_sum(fubini_form(r["vCd"]), fubini_form(r["pair_matrix"])), (
        "L20 FAIL pair form is v'C delta"
    )
    # [L20.31] C is symmetric: C_jm = C_mj
    assert sp.simplify(r["C_pair"](j, m) - r["C_pair"](m, j)) == 0, "L20 FAIL C not symmetric"

    # ---------------------------------------- 3. the first-order condition on the tangent space
    kkt, dsimplex = r["kkt"], r["dsimplex"]
    lam = kkt.rhs
    Gj = sp.Sum(r["p_def"](i) * u[i, j], lim_i)
    # [L20.32] the derivative of J_tau along v at w* is Sum_j v_j G_j (Fubini, as L3)
    assert same_sum(
        fubini_form(sp.Sum(r["p_def"](i) * r["sv"](i), lim_i)),
        fubini_form(sp.Sum(v[j] * Gj, lim_j)),
    ), "L20 FAIL derivative along v is v.G"
    # [L20.33] with G_j = lambda for every j (L3) and Sum_j v_j = 0 on the tangent space: v.G = 0
    assert sp.simplify(linear(sp.Sum(v[j] * lam, lim_j)).subs(dsimplex, 0)) == 0, (
        "L20 FAIL v.G on the tangent space"
    )
    # [L20.34] negative control: for v = 1, off the tangent space, Sum_j lambda = d lambda is not 0
    assert sp.simplify(sp.Sum(lam, lim_j).doit()) != 0, "L20 FAIL tangency not load-bearing"
    vSw = sp.Sum(sp.Sum(Sg[j, l_] * v[j] * w[l_], (l_, 1, d)), lim_j)
    vSd = sp.Sum(sp.Sum(Sg[j, l_] * v[j] * dl[l_], (l_, 1, d)), lim_j)
    ridge_at_shift = tau * sp.Sum(sp.Sum(Sg[j, l_] * v[j] * (w[l_] + dl[l_]), (l_, 1, d)), lim_j)
    # [L20.35] the ridge derivative at w* + delta is tau v'Sigma w* + tau v'Sigma delta; the second
    # (noise times shift) is the term set aside as second order
    assert (
        sp.simplify(linearize(ridge_at_shift) - tau * linearize(vSw) - tau * linearize(vSd)) == 0
    ), "L20 FAIL ridge at the shifted point"
    # [L20.36] first order: tau (v'C delta + v'Sigma w*) = tau Sum_j v_j (C delta + Sigma w*)_j
    assert (
        sp.simplify(
            linearize(r["vCd_abs"])
            + linearize(vSw)
            - linearize(sp.Sum(v[j] * r["force"](j), lim_j))
        )
        == 0
    ), "L20 FAIL force form of the condition"

    def total_zero(f):  # Sum_j (P f)_j, with the mean's dummy h renamed to j (alpha-renaming)
        return sp.simplify(linearize(sp.Sum(r["Pf"](f, j), lim_j)).xreplace({h: j}))

    q_ = r["force"]
    Pq = lambda x: r["Pf"](q_, x)  # noqa: E731
    # [L20.37] P maps into the tangent space: Sum_j (P q)_j = 0
    assert total_zero(q_) == 0, "L20 FAIL P q is tangent"
    # [L20.38] v = P q is tangent, and Sum_j (P q)_j q_j = Sum_j (P q)_j^2
    assert sp.simplify(linearize(sp.Sum(Pq(j) * (q_(j) - Pq(j)), lim_j)).xreplace({h: j})) == 0, (
        "L20 FAIL v'q = ||P q||^2 at v = P q"
    )
    z0 = sp.Symbol("nrm", real=True)
    # [L20.39] ||P q||^2 = 0 for a real vector forces P q = 0
    assert sp.solve(sp.Eq(z0**2, 0), z0) == [0], "L20 FAIL zero norm"
    tang2 = sp.Sum(dl[h2], (h2, 1, d))  # Sum_j delta_j = 0 (the mean's dummy in P delta)
    tang = sp.Sum(dl[j], lim_j)
    # [L20.40] delta is tangent (Sum_j delta_j = 0), so P delta = delta
    assert sp.simplify((r["Pdl"](m) - dl[m]).subs(tang2, 0)) == 0, "L20 FAIL P delta = delta"
    # [L20.41] P q = P C delta + P Sigma w* = P C P delta + y (P linear, P delta = delta)
    assert sp.simplify(linearize((r["Xd"](j) + r["yv"](j) - Pq(j)).subs(tang2, 0))) == 0, (
        "L20 FAIL P q = X delta + y"
    )
    # [L20.42] y = P Sigma w* is tangent: Sum_j y_j = 0
    assert total_zero(r["Sw"]) == 0, "L20 FAIL y tangent"
    eq_ok = True  # X delta + y = P q (previous step) and P q = 0 (the zero-norm step)
    # [L20.43] I18: delta is tangent, in the range of X (R3), and X delta = - y: delta = - X^+ y
    assert I18.entails(
        [
            sp.Equivalent(r["pin_range"], sp.true if r["range_ok"] else sp.false),
            sp.Equivalent(r["pin_eq"], sp.true if eq_ok else sp.false),
        ],
        r["pin_out"],
    ), "L20 FAIL pseudoinverse closed form"

    # ------------------------------------------------------ 4. the size of the shift, the ridge
    mc, s_r3, cs, ny, A_sym, B_ = (r[x] for x in ("mc", "s_r3", "cs", "ny", "A_sym", "B_sym_"))
    # [L20.44] the condition tested on v = delta (tangent): delta'C delta + delta'Sigma w* = 0
    assert (
        sp.simplify(
            linearize(r["A_expr"])
            + linearize(r["B_expr"])
            - linearize(sp.Sum(dl[j] * r["force"](j), lim_j))
        )
        == 0
    ), "L20 FAIL condition at v = delta"
    A_val = sp.solve(sp.Eq(r["rayleigh"], s_r3), A_sym)[0]
    # [L20.45] R3: delta'C delta = m ||delta||^2 + s, s >= 0
    assert sp.simplify(A_val - (mc * nd**2 + s_r3)) == 0, "L20 FAIL Rayleigh bound"
    # [L20.46] delta is tangent, so delta'y = delta'Sigma w* (y = P Sigma w*)
    assert (
        sp.simplify(linearize(sp.Sum(dl[j] * (r["yv"](j) - r["Sw"](j)), lim_j)).subs(tang, 0)) == 0
    ), "L20 FAIL delta.y = delta'Sigma w"
    B_val = -A_val  # the condition: delta'Sigma w* = - delta'C delta
    gap = sp.simplify(r["cs_slack"].subs(B_, B_val))
    # [L20.47] I9: ||delta|| ||y|| - |delta.y| = cs >= 0 with delta.y = - (m ||delta||^2 + s)
    assert sp.simplify(gap - (nd * ny - mc * nd**2 - s_r3)) == 0, "L20 FAIL Cauchy-Schwarz chain"
    ny_sol = sp.solve(sp.Eq(gap, cs), ny)[0]
    # [L20.48] hence ||y|| / m - ||delta|| = (s + cs) / (m ||delta||) >= 0: ||delta|| <= ||y|| / m
    assert (
        sp.simplify(ny_sol / mc - nd - (s_r3 + cs) / (mc * nd)) == 0
        and ((s_r3 + cs) / (mc * nd)).is_nonnegative is True
    ), "L20 FAIL norm bound"
    # [L20.49] and delta'Sigma w* = - m ||delta||^2 - s <= 0: the ridge falls at first order
    assert sp.simplify(B_val + mc * nd**2 + s_r3) == 0 and B_val.is_nonpositive is True, (
        "L20 FAIL ridge falls"
    )

    # ------------------------------------------------------------- 5. the equal-noise reading
    sigma = r["sigma"]
    pw = sp.Sum(sp.KroneckerDelta(S.J0, l_) * sigma**2 * w[l_], (l_, 1, d)).doit()
    # [L20.50] Sigma = sigma^2 I: (Sigma w)_x = sigma^2 w_x
    assert sp.simplify(piece_in_range(pw, S) - sigma**2 * w[S.J0]) == 0, "L20 FAIL Sigma w"
    wf = lambda x: w[x]  # noqa: E731
    sw_sigma = lambda x: sigma**2 * w[x]  # noqa: E731
    # [L20.51] hence y = sigma^2 P w*: P is linear
    assert sp.simplify(linearize(r["Pf"](sw_sigma, S.J0) - sigma**2 * r["Pf"](wf, S.J0))) == 0, (
        "L20 FAIL y = sigma^2 P w"
    )
    L20_RESULT.certify(ctx)
