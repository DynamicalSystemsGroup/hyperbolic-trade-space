"""L18: Gaussian cumulant with a noise covariance; the conditioning as the map from a
measurement error to the noise the fit sees.

What this proves (symbolic d): for a Gaussian noise vector eps with mean 0 and covariance Sigma
(A9), (1/tau) log E exp(tau w.eps) = tau w'Sigma w / 2. For a diagonal Sigma = diag(sigma_j^2) the
shift is tau Sum_j w_j^2 sigma_j^2 / 2, and with every sigma_j equal it is the L6 value tau
sigma^2 ||w||^2 / 2 (L6 is Sigma = sigma^2 I). Under log-affine conditioning u_j = alpha_j log(a_j
+ r_j) + b_j with a_j = 0 (A4: the log, orient, standardise conditioning of the case) and a
multiplicative measurement error log rt_j = log r_j + zeta_j, zeta_j ~ N(0, delta_j^2) (A10), the
noise in the conditioned metric is eps_j = alpha_j zeta_j ~ N(0, alpha_j^2 delta_j^2): so sigma_j
= delta_j / s_j, with s_j := 1/|alpha_j|, the log spread of attribute j by the convention that the
standardising conditioning divides by. To first order a log-error of size delta_j is a relative
error of size delta_j.

What this does NOT prove: that s_j := 1/|alpha_j| is the spread of the data (that is the
convention of the standardising conditioning, here a definition); anything for a noise that is not
jointly Gaussian, or for weights w or a scaler alpha fitted to the noisy table; a map for
conditioning with a_j != 0 (the factor alpha_j r_j / (a_j + r_j) enters and the lemma does not
carry it) or for other scalers; anything about the data of record, which carry no noise of their
own (the noise is a property of an experiment); a finite-sample statement or consistency of the
fit.

Route: sympy.stats for the one-variable moment generating function of the centred normal w.eps;
KroneckerDelta for the diagonal quadratic form; A4 and A10 applied as rewrite rules for the map.
"""

import sympy as sp
from sympy.stats import E, variance

from derivation.axioms import A3, A4, A5, A9, A10
from derivation.sumtools import linear

TITLE = "Gaussian cumulant with a noise covariance; the conditioning maps error to noise"
STATEMENT = (
    "Under a Gaussian noise vector with mean 0 and covariance Sigma (A9): (1/tau) log E "
    "exp(tau w.eps) = tau w'Sigma w / 2; for diagonal Sigma, tau Sum_j w_j^2 sigma_j^2 / 2; "
    "for equal sigma_j it is the L6 value tau sigma^2 ||w||^2 / 2. Under log-affine "
    "conditioning with a_j = 0 and a multiplicative measurement error log rt_j = log r_j + "
    "zeta_j, zeta_j ~ N(0, delta_j^2) (A10), the conditioned noise is eps_j = alpha_j "
    "zeta_j, sigma_j = |alpha_j| delta_j = delta_j / s_j with s_j := 1/|alpha_j| the log "
    "spread; to first order delta_j is a relative error"
)
AXIOMS_USED = ["A3", "A4", "A5", "A9", "A10"]


def derive(ctx):
    S = ctx["S"]
    j = S.j
    sg = sp.IndexedBase("sg")  # sg[j]: the noise level sigma_j of metric j (squared only)
    e = sp.Symbol("e", real=True)  # a relative measurement error
    r_raw, rt = sp.IndexedBase("r"), sp.IndexedBase("rt")  # true and measured raw attribute

    # [L18.1] A3: tau > 0
    tau = A3.positive(S.tau)
    # [L18.2] A9: w.eps is a centred normal variable with variance q = w'Sigma w (case q > 0)
    X = A9.obj("lin")
    # one-variable moment generating function at tau (sympy.stats)
    mgf = sp.simplify(E(sp.exp(tau * X)))
    # [L18.3] A9: the variance q of w.eps is the quadratic form Sum_j Sum_l w_j Sigma_jl w_l
    q, qform = A9.rule(0)
    cumulant = sp.simplify(sp.log(mgf) / tau)
    # degenerate case q = 0: w.eps = 0 almost surely, E exp(tau * 0) = 1
    cumulant_zero = sp.simplify(sp.log(sp.exp(tau * 0)) / tau)

    # [L18.4] A9: the entries Sigma_jl, here diagonal: Sigma_jl = KroneckerDelta(j, l) sigma_j^2
    cov = A9.obj("cov")
    diag = qform.replace(
        lambda x: isinstance(x, sp.Indexed) and x.base == cov,
        lambda x: sp.KroneckerDelta(x.indices[0], x.indices[1]) * sg[x.indices[0]] ** 2,
    )
    # the Kronecker delta collapses the inner Sum; the guard j <= d it leaves holds on j = 1..d
    diag_sum = diag.doit().replace(lambda x: isinstance(x, sp.Piecewise), lambda x: x.args[0].expr)
    # [L18.5] A5: sigma > 0, the equal level sigma_j = sigma of A5
    sigma = A5.positive(S.sigma)
    equal = linear(
        diag_sum.replace(lambda x: isinstance(x, sp.Indexed) and x.base == sg, lambda x: sigma)
    )

    # the conditioning map. A4 with a_j = 0: u_j = alpha_j log r_j + b_j, alpha_j real
    # [L18.6] A4: alpha_j is real (A4 declares the log-equation over real quantities)
    alpha_r = A4.real_base("alpha")
    # [L18.7] A4: the clean conditioned metric u_j = alpha_j log(a_j + r_j) + b_j
    u_clean = A4.rewrite(S.u[j], rename={S.alpha: alpha_r})
    pure = u_clean.subs(S.a[j], 0)
    # the same conditioning applied to the measured attribute rt_j in place of r_j
    noisy = pure.subs(r_raw[j], rt[j])
    # [L18.8] A10: the measured attribute has log rt_j = log r_j + zeta_j
    noisy_log = A10.rewrite(noisy)
    eps_j = sp.simplify(noisy_log - pure)
    # [L18.9] A10: zeta_j ~ N(0, delta_j^2), so Var(alpha_j zeta_j) = alpha_j^2 delta_j^2
    var_eps = sp.simplify(variance(alpha_r[j] * A10.obj("zeta")))
    # the log spread s_j = 1/|alpha_j| of the standardising conditioning
    spread = 1 / sp.Abs(alpha_r[j])
    # [L18.10] A10: delta_j > 0, the size of the log-error of attribute j
    delta_j = A10.rule(2)[0]
    # first order: log(1 + e) = e + O(e^2), a relative error e is a log-error e
    first_order = sp.series(sp.log(1 + e), e, 0, 2).removeO()

    ctx["L18"] = {
        "tau": tau,
        "q": q,
        "mgf": mgf,
        "cumulant": cumulant,
        "cumulant_zero": cumulant_zero,
        "qform": qform,
        "diag_sum": diag_sum,
        "sg": sg,
        "equal": equal,
        "sigma": sigma,
        "eps_j": eps_j,
        "alpha": alpha_r,
        "var_eps": var_eps,
        "spread": spread,
        "delta_j": delta_j,
        "e": e,
        "first_order": first_order,
        "l": next(lim[0] for lim in qform.limits if lim[0] != j),
    }


def verify(ctx):
    S = ctx["S"]
    r = ctx["L18"]
    tau, q, j, d, w, sg = r["tau"], r["q"], S.j, S.d, S.w, r["sg"]
    norm2 = sp.Sum(w[j] ** 2, (j, 1, d))
    zeta_j = sp.IndexedBase("zeta")[j]
    # [L18.11] the MGF of the centred normal w.eps at tau is exp(tau^2 q / 2)
    assert sp.simplify(r["mgf"] - sp.exp(tau**2 * q / 2)) == 0, "L18 FAIL one-variable MGF"
    # [L18.12] the cumulant (1/tau) log E exp(tau w.eps) equals tau q / 2 with q = w'Sigma w
    assert sp.simplify(r["cumulant"] - tau * q / 2) == 0, "L18 FAIL cumulant formula"
    # [L18.13] the degenerate case q = 0 gives the same formula: the cumulant is 0 = tau * 0 / 2
    assert r["cumulant_zero"] == 0, "L18 FAIL degenerate cumulant"
    # [L18.14] the quadratic form q runs over j, l = 1..d, the same range as ||w||^2
    assert r["qform"].limits == ((r["l"], 1, d), (j, 1, d)), "L18 FAIL quadratic form range"
    # [L18.15] diagonal Sigma: the quadratic form is Sum_j w_j^2 sigma_j^2
    assert sp.simplify(r["diag_sum"].function - w[j] ** 2 * sg[j] ** 2) == 0, (
        "L18 FAIL diagonal quadratic form"
    )
    # [L18.16] the diagonal sum runs over j = 1..d
    assert r["diag_sum"].limits == ((j, 1, d),), "L18 FAIL diagonal range"
    # [L18.17] equal levels: the quadratic form is sigma^2 ||w||^2, so the shift is the L6 value
    assert sp.simplify(r["equal"] - r["sigma"] ** 2 * norm2) == 0, "L18 FAIL equal-levels form"
    # [L18.18] conditioning: the measurement error enters the conditioned metric as alpha_j zeta_j
    assert sp.simplify(r["eps_j"] - r["alpha"][j] * zeta_j) == 0, "L18 FAIL conditioned noise"
    # [L18.19] its variance is alpha_j^2 delta_j^2
    assert sp.simplify(r["var_eps"] - r["alpha"][j] ** 2 * r["delta_j"] ** 2) == 0, (
        "L18 FAIL conditioned variance"
    )
    # [L18.20] sigma_j = sqrt(alpha_j^2 delta_j^2) = delta_j / s_j with s_j := 1/|alpha_j|
    assert sp.simplify(sp.sqrt(r["var_eps"]) - r["delta_j"] / r["spread"]) == 0, (
        "L18 FAIL sigma_j = delta_j / s_j"
    )
    # [L18.21] first order: log(1 + e) = e + O(e^2), a relative error e is a log-error e
    assert sp.simplify(r["first_order"] - r["e"]) == 0, "L18 FAIL first-order relative error"
