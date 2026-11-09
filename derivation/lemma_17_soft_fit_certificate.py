"""L17 - the soft-fit certificate: the gradient, the Hessian D - kappa M, and the second-order test.

Setting (as L16).  K terms with exponents W_k on the simplex, offsets beta_k = J_tau(U W_k) (the
log-mean-exp over all N designs), score x_ik = W_k.u_i - beta_k, soft model Phi_i = (1/kappa) log
sum_k exp(kappa x_ik), and the fit minimizes the mean slack F(W) = -(1/N) sum_i Phi_i, for finite
tau and kappa.  Write p_k = softmax(tau U W_k) (the support weights of term k), utilde_k =
sum_l p_lk u_l, alpha_i = softmax(kappa x_i.) (the weights of design i), n_k = sum_i alpha_ik,
c_ik = V_k.u_i for a direction V, and y_ik = V_k.(u_i - utilde_k).

What this proves (symbolic N, K, d; plain SymPy), along an arbitrary direction V:
  (i) The gradient.  d/dt F(W + tV) at t = 0 is sum_k V_k.g_k with g_k = (n_k/N)(utilde_k -
     ubar_k^alpha), ubar_k^alpha = (1/n_k) sum_i alpha_ik u_i: the weighted refit gradient of term k
     (the support value utilde_k ties the offset).  The first derivative of the score along V is
     y_ik = c_ik - sum_l p_lk c_lk, the second is -tau Var_{p_k}(c_.k).
  (ii) The Hessian.  d^2/dt^2 F(W + tV) at t = 0 is V'(D - kappa M)V with
         V'DV = sum_k (n_k/N) tau Var_{p_k}(c_.k),   D = blockdiag((n_k/N) tau Cov_{p_k}(u)),
         V'MV = (1/N) sum_i Var_{alpha_i}(y_i.),     the ambiguity of the designs between terms.
  (iii) D and M are positive semidefinite: each is a sum of a covariance (a variance of a linear
     form under weights summing to one) with nonnegative factors, so each quadratic form is a sum of
     nonnegative terms.
  (iv) The second-order test.  The constraints (the simplex of each term) are affine, so the
     Hessian of the Lagrangian is the Hessian of F.  The critical cone of the second-order
     sufficient condition lies inside the tangent space of the active face (the bounds with a
     strictly positive multiplier fixed, the others free), so positive definiteness on that space
     implies it on the cone.  The second-order sufficient condition is a declared inherited result
     (I16, Nocedal and Wright, Theorem 12.6): the certificate follows.
  (v) Numerical endpoints, an exact small instance (N = 4 designs, K = 2 terms, d = 2, tau =
     kappa = 1; the L16 designs): the gradient and the Hessian of the formulas agree with central
     finite differences of F at 60 digits; at the point with both terms equal (1/2, 1/2) the
     gradient is stationary on the simplex and the Hessian on the tangent space has a negative
     eigenvalue, so the point is stationary and is not certified, while at kappa = 1/2 the same
     point is certified; D and M are positive semidefinite there.

The statement is for a finite kappa and tau (the soft objective is smooth) and for a point at
which the first-order conditions hold exactly: a numerical tolerance on the gaps is not covered by
the theorem (see I16's failure mode).  What this does NOT prove: that the alternation reaches a
stationary point, a radius of the minimizer, anything at tau or kappa infinite, or that a
certified point is the global minimizer or the planted one.
"""

import mpmath
import sympy as sp
from sympy.logic.inference import satisfiable

from derivation.axioms import A1, A2, A3, A6, I16
from derivation.sumtools import fuse, linearize, push_in, replace_indexed, split_sums

TITLE = "the soft-fit certificate: Hessian D - kappa M and the second-order test"
STATEMENT = (
    "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order "
    "(KKT) conditions hold, if the Hessian H = D - kappa M of the soft objective is positive "
    "definite on the tangent space of the active face, the point is a strict local minimizer; D "
    "and M are both positive semidefinite, D the weighted within-term curvature and kappa M the "
    "designs' ambiguity between terms."
)
AXIOMS_USED = ["A1", "A2", "A3", "A6", "I16"]

_LA = sp.Symbol("ja", integer=True)  # coordinate dummy inside the scores W_k . u_l
_LC = sp.Symbol("jc", integer=True)  # coordinate dummy inside the directional scores V_k . u_l
_LM = sp.Symbol("m", integer=True)  # term dummy inside the softmax normalizer
_LL = sp.Symbol("l", integer=True)  # design dummy inside the support sums


# ----------------------------------------------------------------------------- Sum algebra
def _merge(expr):
    """A product of Sums with distinct bound variables is one Sum over the union of the limits."""

    def _target(e):
        return isinstance(e, sp.Mul) and sum(isinstance(a, sp.Sum) for a in e.args) >= 2

    def _go(e):
        sums = [a for a in e.args if isinstance(a, sp.Sum)]
        bound = [lim[0] for s in sums for lim in s.limits]
        if len(set(bound)) < len(bound):
            return e
        body = sp.Mul(*[a for a in e.args if not isinstance(a, sp.Sum)])
        limits = []
        for s in sums:
            body = body * s.function
            limits += list(s.limits)
        return sp.Sum(body, *limits)

    return expr.replace(_target, _go)


def _nf(expr):
    """Normal form: split over sums of terms, merge products of Sums, push constants in, fuse into
    multi-limit Sums, with the limits in a fixed order."""
    for _ in range(6):
        expr = sp.expand(fuse(push_in(_merge(split_sums(sp.expand(expr))))))

    def _sort(s):
        return sp.Sum(s.function, *sorted(s.limits, key=lambda lim: str(lim[0])))

    return expr.replace(lambda e: isinstance(e, sp.Sum) and len(e.limits) > 1, _sort)


def _tidy(expr, x0, W, T, ZK, K, n, kappa, tau):
    """Name the two normalizers: sum_m exp(kappa x0[i, m]) as T[i] and sum_l exp(tau W_k.u_l) as
    ZK[k], whatever the bound variable, so quotients of them cancel."""

    def _is_T(q):
        return (
            isinstance(q, sp.Sum)
            and len(q.limits) == 1
            and q.limits[0][1:] == (1, K)
            and q.function.func == sp.exp
            and any(a.base == x0 for a in q.function.atoms(sp.Indexed))
        )

    def _to_T(q):
        return T[next(a for a in q.function.atoms(sp.Indexed) if a.base == x0).indices[0]]

    def _is_Z(q):
        return (
            isinstance(q, sp.Sum)
            and len(q.limits) == 1
            and q.limits[0][1:] == (1, n)
            and q.function.func == sp.exp
            and any(a.base == W for a in q.function.atoms(sp.Indexed))
        )

    def _to_Z(q):
        return ZK[next(a for a in q.function.atoms(sp.Indexed) if a.base == W).indices[0]]

    return expr.replace(_is_T, _to_T).replace(_is_Z, _to_Z)


def _tidy_sums(expr, *names):
    """Tidy, pull constants out of the sums, tidy again (a sum of the weights over its index is the
    normalizer, so a normalized weight sums to one)."""
    expr = _tidy(expr, *names)
    expr = sp.expand(linearize(expr))
    return sp.expand(sp.together(_tidy(expr, *names)))


# ----------------------------------------------------------------------------- the exact instance
def _numbers(U, W, tau, kappa):
    """The gradient g, D, M and F of the formulas at W (lists of sympy Floats, 60 digits)."""
    N, K, d = len(U), len(W), len(U[0])
    f = lambda v: sp.Float(v, 60) if not isinstance(v, sp.Float) else v  # noqa: E731
    a = [[sum(f(W[k][j]) * f(U[i][j]) for j in range(d)) for k in range(K)] for i in range(N)]
    Z = [sum(sp.exp(tau * a[i][k]) for i in range(N)) for k in range(K)]
    beta = [sp.log(Z[k] / N) / tau for k in range(K)]
    p = [[sp.exp(tau * a[i][k]) / Z[k] for k in range(K)] for i in range(N)]
    ut = [[sum(p[i][k] * f(U[i][j]) for i in range(N)) for j in range(d)] for k in range(K)]
    x = [[a[i][k] - beta[k] for k in range(K)] for i in range(N)]
    T = [sum(sp.exp(kappa * x[i][k]) for k in range(K)) for i in range(N)]
    al = [[sp.exp(kappa * x[i][k]) / T[i] for k in range(K)] for i in range(N)]
    nk = [sum(al[i][k] for i in range(N)) for k in range(K)]
    g = [
        [nk[k] / N * ut[k][j] - sum(al[i][k] * f(U[i][j]) for i in range(N)) / N for j in range(d)]
        for k in range(K)
    ]
    D = sp.zeros(K * d, K * d)
    M = sp.zeros(K * d, K * d)
    for k in range(K):
        for j in range(d):
            for jj in range(d):
                cov = (
                    sum(p[i][k] * f(U[i][j]) * f(U[i][jj]) for i in range(N)) - ut[k][j] * ut[k][jj]
                )
                D[k * d + j, k * d + jj] = nk[k] / N * tau * cov
    for k in range(K):
        for ll in range(K):
            wgt = [al[i][k] * ((1 if k == ll else 0) - al[i][ll]) for i in range(N)]
            for j in range(d):
                for jj in range(d):
                    M[k * d + j, ll * d + jj] = (
                        sum(
                            wgt[i] * (f(U[i][j]) - ut[k][j]) * (f(U[i][jj]) - ut[ll][jj])
                            for i in range(N)
                        )
                        / N
                    )
    F = -sum(sp.log(T[i]) / kappa for i in range(N)) / N
    return g, D, M, F


def _F(U, W, tau, kappa):
    return _numbers(U, W, tau, kappa)[3]


def _flat(g):
    return [v for row in g for v in row]


def _eigs(A):
    """Eigenvalues (ascending) of a symmetric sympy matrix of Floats, at 60 digits."""
    with mpmath.workdps(60):
        vals = mpmath.eigsy(mpmath.matrix(A.tolist()), eigvals_only=True)
    return sorted(sp.Float(str(v), 60) for v in vals)


def _instance():
    """The formulas against central finite differences of F, at a generic point (60 digits)."""
    R = sp.Rational
    U = [(1, 0), (1, R(1, 2)), (0, 1), (R(1, 2), 1)]
    W = [(R(3, 4), R(1, 4)), (R(1, 5), R(4, 5))]
    tau = kappa = sp.Integer(1)
    g, D, M, _ = _numbers(U, W, tau, kappa)
    H = D - kappa * M
    h = sp.Float("1e-12", 60)
    size = len(W) * len(U[0])

    def shifted(coords):
        Wn = [list(row) for row in W]
        for idx, step in coords:
            Wn[idx // 2][idx % 2] += step
        return _F(U, Wn, tau, kappa)

    grad_err = max(
        abs((shifted([(a, h)]) - shifted([(a, -h)])) / (2 * h) - _flat(g)[a]) for a in range(size)
    )
    hess_err = 0
    for a in range(size):
        for b in range(a, size):
            fd = (
                shifted([(a, h), (b, h)])
                - shifted([(a, h), (b, -h)])
                - shifted([(a, -h), (b, h)])
                + shifted([(a, -h), (b, -h)])
            ) / (4 * h * h)
            hess_err = max(hess_err, abs(fd - H[a, b]))
    return {
        "grad_err": sp.N(grad_err, 5),
        "hess_err": sp.N(hess_err, 5),
        "asymmetry": sp.N(max(abs(H[a, b] - H[b, a]) for a in range(size) for b in range(size)), 5),
    }


def _all_equal():
    """Both terms equal to (1/2, 1/2): stationary on the simplex, curvature below zero at kappa = 1
    and above zero at kappa = 1/2."""
    R = sp.Rational
    U = [(1, 0), (1, R(1, 2)), (0, 1), (R(1, 2), 1)]
    W = [(R(1, 2), R(1, 2)), (R(1, 2), R(1, 2))]
    tau = sp.Integer(1)
    B = sp.Matrix([[1, 0], [-1, 0], [0, 1], [0, -1]])  # the tangent space: sum zero in each term
    out = {}
    for name, kappa in (("one", sp.Integer(1)), ("half", R(1, 2))):
        g, D, M, _ = _numbers(U, W, tau, kappa)
        gap = max(abs(row[0] - row[1]) for row in g)  # equal components: lambda_k = g_k0 = g_k1
        H = B.T * (D - kappa * M) * B
        out[name] = {
            "gap": sp.N(gap, 5),
            "lambda_min": _eigs(H)[0],
            "D_min": _eigs(D)[0],
            "M_min": _eigs(M)[0],
        }
    return out


# ----------------------------------------------------------------------------- derive
def derive(ctx):
    S = ctx["S"]
    n, K, d = S.n, S.K, S.d
    i, k, kappa, tau, t = S.i, S.k, S.kappa, S.tau, S.t
    out = {}

    # [L17.1] A1: the log-metrics u and the direction V (real vectors) are real families
    u, V = A1.real_base("u"), A1.real_base("V")
    # [L17.2] A2: the exponents W_kj of every term are nonnegative (on the simplex)
    W = A2.nonneg_base("W")
    # [L17.3] A1: the scores x0 of the model at W are real
    x0 = A1.real_base("x0")

    def a0(a, b):  # W_b . u_a
        return sp.Sum(W[b, _LA] * u[a, _LA], (_LA, 1, d))

    def c(a, b):  # V_b . u_a
        return sp.Sum(V[b, _LC] * u[a, _LC], (_LC, 1, d))

    def Z(b):
        return sp.Sum(sp.exp(tau * a0(_LL, b)), (_LL, 1, n))

    def p(a, b):  # the support weights of term b
        return sp.exp(tau * a0(a, b)) / Z(b)

    def pc(b):  # sum_l p_lb c_lb
        return sp.Sum(p(_LL, b) * c(_LL, b), (_LL, 1, n))

    def pc2(b):  # sum_l p_lb c_lb^2
        return sp.Sum(p(_LL, b) * c(_LL, b) ** 2, (_LL, 1, n))

    def al(a, b):  # alpha_ab = softmax_b(kappa x0_a.)
        return sp.exp(kappa * x0[a, b]) / sp.Sum(sp.exp(kappa * x0[a, _LM]), (_LM, 1, K))

    def y(a, b):  # the first derivative of the score of design a under term b along V
        return c(a, b) - pc(b)

    def z(b):  # its second derivative: minus tau times the variance of c under p_b
        return -tau * (pc2(b) - pc(b) ** 2)

    # the offset along the line W + tV: beta_k(t) = (1/tau) log of the mean of exp(tau score_l(t))
    line = sp.Sum(sp.exp(tau * (a0(_LL, k) + t * c(_LL, k))), (_LL, 1, n))
    beta_t = sp.log(line / n) / tau
    # [L17.4] the first derivative of the offset along V is sum_l p_lk c_lk (the L3 gradient)
    out["beta1_gap"] = sp.simplify(sp.diff(beta_t, t).subs(t, 0) - pc(k))
    # [L17.5] its second derivative is tau times the variance of c under the support weights
    out["beta2_gap"] = sp.simplify(sp.diff(beta_t, t, 2).subs(t, 0) - tau * (pc2(k) - pc(k) ** 2))
    score_t = a0(i, k) + t * c(i, k) - beta_t
    # [L17.6] the first derivative of the score x_ik(t) = (W_k + tV_k).u_i - beta_k(t) is y_ik
    out["y_gap"] = sp.simplify(sp.diff(score_t, t).subs(t, 0) - y(i, k))
    # [L17.7] its second derivative is -tau Var_{p_k}(c_.k)
    out["z_gap"] = sp.simplify(sp.diff(score_t, t, 2).subs(t, 0) - z(k))

    # the soft model of design i composed with the scores x(k, t): derivatives named at t = 0
    xf = sp.Function("x")
    Gi = -sp.log(sp.Sum(sp.exp(kappa * xf(k, t)), (k, 1, K))) / kappa  # -Phi_i
    T, ZK = sp.IndexedBase("T"), sp.IndexedBase("ZK")
    names = (x0, W, T, ZK, K, n, kappa, tau)

    def name_jets(e):
        e = e.replace(
            lambda q: (
                isinstance(q, sp.Derivative) and q.expr.func == xf and q.derivative_count == 2
            ),
            lambda q: z(q.expr.args[0]),
        )
        e = e.replace(
            lambda q: (
                isinstance(q, sp.Derivative) and q.expr.func == xf and q.derivative_count == 1
            ),
            lambda q: y(i, q.expr.args[0]),
        )
        return e.replace(lambda q: q.func == xf, lambda q: x0[i, q.args[0]])

    G1 = name_jets(sp.diff(Gi, t))
    G2 = name_jets(sp.diff(Gi, t, 2))
    ybar = sp.Sum(al(i, k) * y(i, k), (k, 1, K))
    # [L17.8] the first derivative of -Phi_i at t = 0 is -sum_k alpha_ik y_ik
    out["row1_gap"] = sp.simplify(_tidy(G1, *names) - _tidy(-ybar, *names))
    var_row = sp.Sum(al(i, k) * y(i, k) ** 2, (k, 1, K)) - ybar**2
    # [L17.9] the second derivative of -Phi_i at t = 0 is -kappa Var_alpha(y) - sum_k alpha_ik z_k
    out["row2_gap"] = sp.simplify(
        _tidy(G2, *names) - _tidy(-kappa * var_row - sp.Sum(al(i, k) * z(k), (k, 1, K)), *names)
    )
    # [L17.10] the weights alpha_ik = softmax_k(kappa x_ik) of a design sum to one
    out["alpha_sum"] = _tidy_sums(sp.Sum(al(i, k), (k, 1, K)) - 1, *names)
    # [L17.11] the support weights p_lk of a term sum to one
    out["p_sum"] = _tidy_sums(sp.Sum(p(_LL, k), (_LL, 1, n)) - 1, *names)

    nk = sp.Sum(al(i, k), (i, 1, n))  # n_k = sum_i alpha_ik

    def g(b, jj):  # the weighted refit gradient of term b, coordinate jj
        ut_ = sp.Sum(p(_LL, b) * u[_LL, jj], (_LL, 1, n))
        return nk.subs(k, b) / n * ut_ - sp.Sum(al(i, b) * u[i, jj], (i, 1, n)) / n

    F1 = sp.Sum(sp.Sum(-al(i, k) * y(i, k), (k, 1, K)), (i, 1, n)) / n
    grad = sp.Sum(sp.Sum(V[k, _LC] * g(k, _LC), (_LC, 1, d)), (k, 1, K))
    # [L17.12] dF along V is sum_k V_k.g_k, g_k = (n_k/N)(utilde_k - ubar_k^alpha) (refit gradient)
    out["grad_gap"] = sp.expand(_nf(F1) - _nf(grad))

    D_mom = sp.Sum(nk / n * tau * (pc2(k) - pc(k) ** 2), (k, 1, K))
    M_mom = sp.Sum(var_row, (i, 1, n)) / n
    F2 = sp.Sum(-kappa * var_row - sp.Sum(al(i, k) * z(k), (k, 1, K)), (i, 1, n)) / n
    # [L17.13] the second derivative of F along V is V'DV - kappa V'MV, the moment forms of D and M
    out["hess_gap"] = sp.expand(_nf(F2) - _nf(D_mom - kappa * M_mom))

    # the variance forms: weights summing to one, sum_l q_l (c_l - cbar)^2 = sum q c^2 - cbar^2
    cbar = sp.Sum(p(_LM, k) * c(_LM, k), (_LM, 1, n))
    D_sq = sp.Sum(
        nk / n * tau * sp.Sum(p(_LL, k) * (c(_LL, k) - cbar) ** 2, (_LL, 1, n)), (k, 1, K)
    )
    ybar_m = sp.Sum(al(i, _LM) * y(i, _LM), (_LM, 1, K))
    M_sq = sp.Sum(sp.Sum(al(i, k) * (y(i, k) - ybar_m) ** 2, (k, 1, K)), (i, 1, n)) / n

    # [L17.14] for weights q with sum Q, sum q (v - vbar)^2 = sum q v^2 - vbar^2 + vbar^2 (Q-1)
    q, v = sp.IndexedBase("q"), sp.IndexedBase("v")
    vbar = sp.Sum(q[_LM] * v[_LM], (_LM, 1, n))
    var_sq = sp.Sum(q[_LL] * (v[_LL] - vbar) ** 2, (_LL, 1, n))
    var_mom = sp.Sum(q[_LL] * v[_LL] ** 2, (_LL, 1, n)) - vbar**2
    gap_generic = linearize(var_sq) - var_mom - vbar**2 * (sp.Sum(q[_LL], (_LL, 1, n)) - 1)
    out["var_generic"] = sp.expand(
        gap_generic.replace(
            lambda e: isinstance(e, sp.Sum) and e.limits[0][0] == _LM,
            lambda e: sp.Sum(e.function.xreplace({_LM: _LL}), (_LL, *e.limits[0][1:])),
        )
    )
    # [L17.15] at the support weights of term k the sum of the weights is 1: the correction vanishes
    out["D_var_gap"] = _tidy_sums(cbar**2 * (sp.Sum(p(_LL, k), (_LL, 1, n)) - 1), *names)
    # [L17.16] at the weights of design i the sum of the weights is 1: the correction vanishes
    out["M_var_gap"] = _tidy_sums(ybar_m**2 * (sp.Sum(al(i, k), (k, 1, K)) - 1), *names)
    # [L17.17] A3, A6: tau > 0 and kappa > 0; the squares forms are sums of nonnegative terms
    tau_p, kappa_p = A3.positive(tau), A6.positive(kappa)
    out["D_nonneg"] = (D_sq.subs(tau, tau_p)).is_nonnegative
    out["M_nonneg"] = (kappa_p * M_sq).is_nonnegative
    out["D_sq"], out["M_sq"] = D_sq, M_sq

    # [L17.18] A2: the simplex constraint of a term is affine in W: second derivative along V is 0
    out["affine_gap"] = sp.diff(
        replace_indexed(A2.rule(0)[0], S.w, lambda b: W[k, b] + t * V[k, b]) - A2.rule(0)[1], t, 2
    ).doit()

    # the critical cone and the tangent space of the active face, as conditions on a direction w:
    # s: the entries of w sum to zero in every term; f: w = 0 on the bounds with a positive
    # multiplier; g: w >= 0 on the active bounds with a zero multiplier
    s_, f_, g_ = sp.symbols(
        "w_sums_to_zero w_zero_on_positive_multiplier w_nonneg_on_zero_multiplier"
    )
    cone = sp.And(s_, f_, g_)
    face = sp.And(s_, f_)
    # [L17.19] every direction of the critical cone is a direction of the tangent space of the face
    out["cone_in_face"] = not satisfiable(sp.And(cone, sp.Not(face)))
    # [L17.20] A positive definite form on the face is positive on the cone (a restriction)
    pos_face = sp.Symbol("form_positive_at_w_on_face")
    out["restriction"] = not satisfiable(
        sp.And(sp.Implies(cone, face), sp.Implies(face, pos_face), cone, sp.Not(pos_face))
    )
    # [L17.21] I16: first-order conditions and positive definiteness on the face give a strict
    # local minimizer
    out["certificate"] = I16.entails(
        [
            I16.obj("kkt"),
            sp.Implies(sp.Symbol("pd_on_face"), I16.obj("curvature")),
            sp.Symbol("pd_on_face"),
        ],
        I16.obj("conclusion"),
    )
    # [L17.22] without the first-order conditions the premises of I16 do not give the conclusion
    out["certificate_without_kkt"] = I16.entails(
        [sp.Implies(sp.Symbol("pd_on_face"), I16.obj("curvature")), sp.Symbol("pd_on_face")],
        I16.obj("conclusion"),
    )
    # [L17.23] without the curvature premise I16 does not give the conclusion
    out["certificate_without_curvature"] = I16.entails([I16.obj("kkt")], I16.obj("conclusion"))
    # [L17.24] exact instance: the formulas agree with central finite differences of F (60 digits)
    out["instance"] = _instance()
    # [L17.25] exact instance: both terms equal: the gradient and the curvature at kappa 1 and 1/2
    out["all_equal"] = _all_equal()
    ctx["L17"] = out
    return out


# ----------------------------------------------------------------------------- verify
def verify(ctx):
    r = ctx["L17"]
    # [L17.26] the offset's first derivative along V is the support-weighted mean of V_k.u
    assert r["beta1_gap"] == 0, "L17 FAIL: the offset derivative is not the weighted mean"
    # [L17.27] its second derivative is tau times the variance under the support weights
    assert r["beta2_gap"] == 0, "L17 FAIL: the offset curvature is not tau Var_p(c)"
    # [L17.28] the first derivative of the score is c_ik minus the weighted mean of c
    assert r["y_gap"] == 0, "L17 FAIL: the score derivative is not y_ik"
    # [L17.29] the second derivative of the score is minus tau Var_p(c)
    assert r["z_gap"] == 0, "L17 FAIL: the score curvature is not -tau Var_p(c)"
    # [L17.30] the soft model of a design: first derivative of -Phi_i is -sum alpha y
    assert r["row1_gap"] == 0, "L17 FAIL: the soft-max first derivative is not -sum alpha y"
    # [L17.31] the soft model of a design: second derivative is -kappa Var_alpha(y) - sum alpha z
    assert r["row2_gap"] == 0, "L17 FAIL: the soft-max second derivative is wrong"
    # [L17.32] the weights of a design sum to one
    assert r["alpha_sum"] == 0, "L17 FAIL: the design weights do not sum to one"
    # [L17.33] the support weights of a term sum to one
    assert r["p_sum"] == 0, "L17 FAIL: the support weights do not sum to one"
    # [L17.34] the gradient of F is the weighted refit gradient of each term
    assert r["grad_gap"] == 0, "L17 FAIL: the gradient is not the weighted refit gradient"
    # [L17.35] the second derivative of F is V'DV - kappa V'MV
    assert r["hess_gap"] == 0, "L17 FAIL: the Hessian is not D - kappa M"
    # [L17.36] the squares form of a weighted variance is the moment form plus vbar^2 (Q - 1)
    assert r["var_generic"] == 0, "L17 FAIL: the variance identity does not hold"
    # [L17.37] the variance of the support weights, in squares form, is its moment form
    assert r["D_var_gap"] == 0, "L17 FAIL: the squares form of D differs from its moment form"
    # [L17.38] the variance under a design's weights, in squares form, is its moment form
    assert r["M_var_gap"] == 0, "L17 FAIL: the squares form of M differs from its moment form"
    # [L17.39] D is positive semidefinite: V'DV is a sum of nonnegative terms
    assert r["D_nonneg"] is True, "L17 FAIL: D is not positive semidefinite"
    # [L17.40] M is positive semidefinite: V'MV is a sum of nonnegative terms
    assert r["M_nonneg"] is True, "L17 FAIL: M is not positive semidefinite"
    # [L17.41] the constraints are affine: the Hessian of the Lagrangian is the Hessian of F
    assert r["affine_gap"] == 0, "L17 FAIL: the simplex constraint is not affine in W"
    # [L17.42] the critical cone is inside the tangent space of the active face
    assert r["cone_in_face"] is True, "L17 FAIL: the cone is not inside the face"
    # [L17.43] positive definiteness on the face gives it on the cone
    assert r["restriction"] is True, "L17 FAIL: restriction of a positive form to the cone"
    # [L17.44] KKT and positive definiteness on the face give a strict local minimizer (I16)
    assert r["certificate"] is True, "L17 FAIL: the certificate does not follow from I16"
    # [L17.45] without the first-order conditions the certificate does not follow
    assert r["certificate_without_kkt"] is False, "L17 FAIL: the certificate needs the KKT premise"
    # [L17.46] without the curvature the certificate does not follow
    assert r["certificate_without_curvature"] is False, "L17 FAIL: the certificate needs curvature"
    ins = r["instance"]
    # [L17.47] exact instance: the gradient formula agrees with finite differences of F
    assert ins["grad_err"] < sp.Float("1e-15"), (
        "L17 FAIL: the gradient differs from finite differences"
    )
    # [L17.48] exact instance: the Hessian formula agrees with finite differences and is symmetric
    assert ins["hess_err"] < sp.Float("1e-15") and ins["asymmetry"] < sp.Float("1e-40"), (
        "L17 FAIL: the Hessian differs from finite differences"
    )
    eq = r["all_equal"]
    # [L17.49] exact instance: the point with both terms equal is stationary on the simplex
    assert eq["one"]["gap"] < sp.Float("1e-40"), "L17 FAIL: the all-equal point is not stationary"
    # [L17.50] exact instance: at kappa = 1 its Hessian on the tangent space has negative curvature
    assert eq["one"]["lambda_min"] < -sp.Float("0.01"), "L17 FAIL: no negative curvature at kappa 1"
    # [L17.51] exact instance: at kappa = 1/2 the same point has positive curvature (certified)
    assert eq["half"]["lambda_min"] > sp.Float("0.01"), (
        "L17 FAIL: no positive curvature at kappa 1/2"
    )
    # [L17.52] exact instance: D and M are positive semidefinite at the point (eigenvalues >= 0)
    assert min(eq["one"]["D_min"], eq["one"]["M_min"]) > -sp.Float("1e-40"), (
        "L17 FAIL: a negative eigenvalue of D or M"
    )
