"""Three candidate Figure 1 schematics (design spike; synthetic data; matplotlib only).

Run from the repository root:  uv run python <this file> [--out DIR]

The world is one synthetic d = 2 trade space with a K = 3 envelope in log space,
Phi(u) = max_k (w_k . u - beta_k); the frontier is Phi = 0 (V = 1) and the level sets of V
are translates of it along the all-ones direction (shift equivariance). In metric space,
m = exp(u), the facets are hyperbolic sheets and the level sets are uniform scalings.
Colours come from hyperbolic_trade_space.plotting (one colour per meaning).
"""

import argparse
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402

from hyperbolic_trade_space.plotting import (  # noqa: E402
    CATEGORY_COLORS,
    DATA_COLOR,
    FRONTIER_COLOR,
)

HERE = pathlib.Path(__file__).resolve().parent

# ---- the synthetic world -------------------------------------------------------------------
W = np.array([[0.2, 0.8], [0.5, 0.5], [0.8, 0.2]])  # exponent vectors w_k on the simplex
BETA = np.array([0.96, 0.30, 0.60])  # reaches beta_k; corners at log metric 1 = -0.8 and 0.8
FACET_COLORS = CATEGORY_COLORS[:3]
HIGHLIGHT = FRONTIER_COLOR  # the one highlighted design (black, white edge)
PCA_COLOR = "0.35"  # PCA directions: neutral dark grey (a different method, not a facet)
LEVEL_COLOR = "0.45"  # energy levels other than V = 1: thin dotted grey


def phi(u):
    """Hard-max envelope potential Phi_K(u); rows of u are designs in log space."""
    return np.max(u @ W.T - BETA, axis=-1)


def facet_of(u):
    return np.argmax(u @ W.T - BETA, axis=-1)


def facet_line(k, u1):
    """log metric 2 on facet k's hyperplane at log metric 1 = u1 (shifted by level t)."""
    return (BETA[k] - W[k, 0] * u1) / W[k, 1]


def envelope(u1):
    """The frontier Phi = 0 as a curve u2(u1): the minimum of the facet lines."""
    return np.min([facet_line(k, u1) for k in range(3)], axis=0)


def envelope_at(u1, level):
    """Level set Phi = level, obtained by translating the frontier along the all-ones direction."""
    # Phi(u + t 1) = Phi(u) + t, so the set Phi = level is the frontier shifted by (level, level).
    return envelope(u1 - level) + level


def active_ranges():
    """The u1 intervals on which each facet is active on the frontier (K = 3, ordered)."""
    c12 = (BETA[0] / W[0, 1] - BETA[1] / W[1, 1]) / (W[0, 0] / W[0, 1] - W[1, 0] / W[1, 1])
    c23 = (BETA[1] / W[1, 1] - BETA[2] / W[2, 1]) / (W[1, 0] / W[1, 1] - W[2, 0] / W[2, 1])
    return [(-np.inf, c12), (c12, c23), (c23, np.inf)]


def sample_cloud(rng, n=260, lo=-1.9, hi=1.6, depth=1.6, elliptical=False):
    """Designs below the envelope, denser near it (synthetic, conceptual)."""
    pts = []
    while len(pts) < n:
        if elliptical:
            # a tilted ellipse whose long axis runs roughly along the envelope
            a = rng.normal(0.0, 1.25, size=4000)  # along (1, -1): across the metrics
            b = rng.normal(0.0, 0.7, size=4000)  # along (1, 1): overall quality
            u = np.column_stack([(a + b) / np.sqrt(2) - 0.2, (-a + b) / np.sqrt(2) - 0.2])
        else:
            u = rng.uniform([lo, lo], [hi, hi], size=(4000, 2))
        p = phi(u)
        keep = (p <= 0.0) & (p >= -depth) & (rng.uniform(size=len(u)) < np.exp(1.1 * p))
        pts.extend(u[keep])
    return np.array(pts[:n])


# ---- drawing helpers -----------------------------------------------------------------------
def style():
    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.titlesize": 12.5,
            "axes.labelsize": 11.5,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
        }
    )


def visible_ranges(box):
    """Each facet's active u1 interval, clipped to the log-space box (u1_lo, u1_hi, u2_lo, u2_hi).

    The facet lines decrease in u1, so the box's top clips on the left and its bottom on the right.
    """
    u1_lo, u1_hi, u2_lo, u2_hi = box
    out = []
    for k, (a, b) in enumerate(active_ranges()):
        left = (BETA[k] - W[k, 1] * u2_hi) / W[k, 0]  # u1 where the line meets the box top
        right = (BETA[k] - W[k, 1] * u2_lo) / W[k, 0]  # u1 where the line meets the box bottom
        out.append((max(a, u1_lo, left), min(b, u1_hi, right)))
    return out


EXTEND = 0.7  # how far (in log units of u1) a facet's hyperplane is drawn past its active range


def draw_log_envelope(ax, box, levels=(), normals=False, extend=True, lw=2.8, arrow_len=0.55):
    """Facets in log space: coloured active segments, faint extensions, levels, normals."""
    u1_lo, u1_hi = box[0], box[1]
    g = np.linspace(u1_lo, u1_hi, 400)
    for lev in levels:
        ax.plot(g, envelope_at(g, lev), color=LEVEL_COLOR, lw=1.0, ls=":", zorder=2)
    for k, ((a0, b0), (a, b)) in enumerate(zip(active_ranges(), visible_ranges(box))):
        seg = np.linspace(a, b, 60)
        ax.plot(seg, facet_line(k, seg), color=FACET_COLORS[k], lw=lw, zorder=4,
                solid_capstyle="round")
        if extend:
            ext = np.linspace(max(a0 - EXTEND, u1_lo), min(b0 + EXTEND, u1_hi), 60)
            ax.plot(ext, facet_line(k, ext), color=FACET_COLORS[k], lw=0.9, ls="--", alpha=0.5,
                    zorder=3)
        if normals:
            um = np.array([(a + b) / 2, facet_line(k, (a + b) / 2)])
            n = W[k] / np.linalg.norm(W[k]) * arrow_len
            ax.add_patch(FancyArrowPatch(um, um + n, arrowstyle="-|>", mutation_scale=14,
                                         color=FACET_COLORS[k], lw=1.8, zorder=6))
            ax.text(*(um + n * 1.3), rf"$w_{k + 1}$", color=FACET_COLORS[k], ha="center",
                    va="center", fontsize=11.5, fontweight="bold", zorder=7)


def draw_metric_envelope(ax, box, levels=(), extend=True, lw=2.8):
    """The same facets in metric space: hyperbolic sheets, and levels as uniform scalings."""
    u1_lo, u1_hi = box[0], box[1]
    g = np.exp(np.linspace(u1_lo, u1_hi, 600))
    for lev in levels:
        ax.plot(g, np.exp(envelope_at(np.log(g), np.log(lev))), color=LEVEL_COLOR, lw=1.0,
                ls=":", zorder=2)
    for k, ((a0, b0), (a, b)) in enumerate(zip(active_ranges(), visible_ranges(box))):
        seg = np.exp(np.linspace(a, b, 120))
        ax.plot(seg, np.exp(facet_line(k, np.log(seg))), color=FACET_COLORS[k], lw=lw, zorder=4,
                solid_capstyle="round")
        if extend:
            ext = np.exp(np.linspace(max(a0 - EXTEND, u1_lo), min(b0 + EXTEND, u1_hi), 60))
            ax.plot(ext, np.exp(facet_line(k, np.log(ext))), color=FACET_COLORS[k], lw=0.9,
                    ls="--", alpha=0.5, zorder=3)


def scatter_by_facet(ax, u, xy=None, s=16, alpha=0.75):
    xy = u if xy is None else xy
    f = facet_of(u)
    for k in range(3):
        ax.scatter(*xy[f == k].T, s=s, color=FACET_COLORS[k], alpha=alpha, lw=0, zorder=3)


def panel_arrow(fig, ax_l, ax_r, text, right_pad=0.075):
    """A two-headed arrow between two panels with a label (figure coordinates)."""
    bl, br = ax_l.get_position(), ax_r.get_position()
    y = (bl.y0 + bl.y1) / 2
    x0, x1 = bl.x1 + 0.014, br.x0 - right_pad  # stop short of the right panel's y-axis label
    fig.add_artist(FancyArrowPatch((x0, y), (x1, y), transform=fig.transFigure,
                                   arrowstyle="<|-|>", mutation_scale=18, lw=1.8,
                                   color=FRONTIER_COLOR))
    fig.text((x0 + x1) / 2, y + 0.03, text, ha="center", va="bottom", fontsize=10.5)


def facet_legend(ax, loc="lower left"):
    from matplotlib.lines import Line2D

    h = [Line2D([], [], color=FACET_COLORS[k], lw=2.8, label=f"facet {k + 1}") for k in range(3)]
    h.append(Line2D([], [], color=LEVEL_COLOR, lw=1.0, ls=":", label="other energy levels of V"))
    ax.legend(handles=h, loc=loc, frameon=False)


def save(fig, name, out):
    fig.savefig(out / f"{name}.png", dpi=150)
    fig.savefig(out / f"{name}@2x.png", dpi=300)
    plt.close(fig)


# ---- S1 ------------------------------------------------------------------------------------
def s1(out, rng):
    u = sample_cloud(rng, n=260)
    m = np.exp(u)
    levels = (0.5, 0.75, 1.25)
    fig, (axm, axl) = plt.subplots(1, 2, figsize=(10.67, 6.0))
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.11, top=0.80, wspace=0.5)
    box_m = (np.log(0.12), np.log(5.2), np.log(0.02), np.log(5.2))
    box_l = (-2.3, 1.75, -2.1, 2.5)

    # metric space
    scatter_by_facet(axm, u, xy=m)
    draw_metric_envelope(axm, box_m, levels=levels)
    axm.set_xlim(0, 5.2)
    axm.set_ylim(0, 5.2)
    axm.set_xlabel("metric 1 (larger is better)")
    axm.set_ylabel("metric 2 (larger is better)")
    axm.set_title("metric space: hyperbolic sheets,\nV = 1 on the envelope")
    for lev, x in zip((0.5, 0.75, 1.25), (0.75, 1.05, 2.3)):
        y = np.exp(envelope_at(np.log(x), np.log(lev)))
        axm.text(x + 0.08, y + 0.08, f"V = {lev:g}", fontsize=9.5, color=LEVEL_COLOR)
    axm.text(1.3, 1.45, "V = 1", fontsize=11, fontweight="bold", color=FRONTIER_COLOR)
    axm.annotate("energy levels of V\n(up and right is better)", xy=(3.2, 1.35), xytext=(3.6, 3.6),
                 fontsize=9.5, ha="center", color=LEVEL_COLOR,
                 arrowprops=dict(arrowstyle="-|>", color=LEVEL_COLOR, lw=1.0))
    axm.text(0.55, 4.75, "each sheet is one\nmonomial; the dashes\nshow it continuing\nunder the "
             "others", fontsize=9.5, color="0.3", va="top")

    # log space
    scatter_by_facet(axl, u)
    draw_log_envelope(axl, box_l, levels=np.log(levels), normals=True)
    axl.set_xlim(box_l[0], box_l[1])
    axl.set_ylim(box_l[2], box_l[3])
    axl.set_aspect("equal")
    axl.set_xlabel("log metric 1")
    axl.set_ylabel("log metric 2")
    axl.set_title("log space: flat facets,\nnormals $w_k$ on the simplex")
    for lev in (0.5, 0.75, 1.25):
        x = -2.2
        y = envelope_at(x, np.log(lev))
        axl.text(x, y + 0.06, f"V = {lev:g}", fontsize=9.5, color=LEVEL_COLOR)
    axl.text(-2.2, envelope_at(-2.2, 0.0) + 0.07, "V = 1", fontsize=11, fontweight="bold",
             color=FRONTIER_COLOR)
    facet_legend(axl, loc="lower left")

    panel_arrow(fig, axm, axl, "log / exp\n(reversible)")
    fig.suptitle("A trade space is a manifold: K facets, each a trade-off", fontsize=15,
                 fontweight="bold", y=0.97)
    fig.text(0.5, 0.905, "designs (points) stop at an envelope of K = 3 monomials; each facet "
             "is one trade-off, with its own exchange rates", ha="center", fontsize=10.5,
             color="0.3")
    save(fig, "S1", out)


# ---- S2 ------------------------------------------------------------------------------------
def s2(out, rng):
    u = sample_cloud(rng, n=300, elliptical=True, depth=2.6)
    fig, (axp, axf) = plt.subplots(1, 2, figsize=(10.67, 5.8), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.22, top=0.84, wspace=0.25)
    lim = (-2.9, 2.0)
    box = (lim[0], lim[1], lim[0], lim[1] + 0.4)

    # PCA (on the same log-space cloud)
    mu = u.mean(axis=0)
    cov = np.cov((u - mu).T)
    val, vec = np.linalg.eigh(cov)
    order = np.argsort(val)[::-1]
    val, vec = val[order], vec[:, order]
    axp.scatter(*u.T, s=16, color=DATA_COLOR, alpha=0.6, lw=0, zorder=3)
    for i in range(2):
        d = vec[:, i] * 2.0 * np.sqrt(val[i])
        if d.sum() < 0:
            d = -d
        axp.add_patch(FancyArrowPatch(mu - d, mu + d, arrowstyle="<|-|>", mutation_scale=16,
                                      color=PCA_COLOR, lw=2.2, zorder=6))
        axp.text(*(mu + d * 1.18), f"PC {i + 1}", color=PCA_COLOR, fontsize=11.5,
                 fontweight="bold", ha="center", va="center", zorder=7)
    axp.set_xlim(*lim)
    axp.set_ylim(lim[0], lim[1] + 0.4)
    axp.set_aspect("equal")
    axp.set_xlabel("log metric 1")
    axp.set_ylabel("log metric 2")
    axp.set_title("PCA: where the data spread")
    axp.text(0.5, -0.19, "directions of spread through the middle of the cloud;\nthey summarize "
             "the variance of the designs and say\nnothing about what trades against what",
             transform=axp.transAxes, ha="center", va="top", fontsize=10.5, color="0.3")

    # this method
    scatter_by_facet(axf, u, alpha=0.6)
    draw_log_envelope(axf, box, normals=True, extend=False)
    axf.set_aspect("equal")
    axf.set_xlabel("log metric 1")
    axf.set_title("this method: where the data stop")
    axf.text(0.5, -0.19, "facets at the edge of the cloud; each normal $w_k$\nsays what trades "
             "against what, and at which\nexchange rate, in that region of the trade space",
             transform=axf.transAxes, ha="center", va="top", fontsize=10.5, color="0.3")
    from matplotlib.lines import Line2D

    axf.legend(handles=[Line2D([], [], color=FACET_COLORS[k], lw=2.8, label=f"facet {k + 1}")
                        for k in range(3)], loc="lower left", frameon=False)

    fig.suptitle("PCA explains variance; this explains tensions", fontsize=15, fontweight="bold",
                 y=0.97)
    fig.text(0.5, 0.905, "the same designs in log space, read two ways: components through the "
             "cloud versus facets bounding it", ha="center", fontsize=10.5, color="0.3")
    save(fig, "S2", out)


# ---- S3 ------------------------------------------------------------------------------------
def s3(out, rng):
    u = sample_cloud(rng, n=260)
    B = np.array([[1.0, -1.0]]) / np.sqrt(2)  # Helmert row for d = 2: B 1 = 0, B B^T = I
    Z = (u @ B.T)[:, 0]
    L = phi(u)
    f = facet_of(u)
    # the highlighted design: inside facet 2's region, clearly below the frontier
    cand = np.where((f == 1) & (L < -0.55) & (L > -0.8) & (np.abs(Z) < 0.35))[0]
    i = cand[0]
    us, zs, ls = u[i], Z[i], L[i]

    fig, (axl, axc) = plt.subplots(1, 2, figsize=(10.67, 5.8))
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.12, top=0.84, wspace=0.5)
    box = (-2.1, 1.75, -2.1, 1.9)

    # log space with the energy differential
    scatter_by_facet(axl, u, alpha=0.45)
    draw_log_envelope(axl, box, levels=(ls,), normals=False, extend=False)
    top = us - ls  # the frontier point reached by uniform scaling (all-ones direction)
    ray = np.array([us - 1.0, top + 0.35])  # the all-ones ray through the design
    axl.plot(ray[:, 0], ray[:, 1], color=HIGHLIGHT, lw=0.8, ls=":", zorder=5)
    axl.add_patch(FancyArrowPatch(us, top, arrowstyle="-|>", mutation_scale=16,
                                  color=HIGHLIGHT, lw=2.2, zorder=8))
    axl.scatter(*us, s=140, marker="o", color=HIGHLIGHT, edgecolor="white", lw=1.5, zorder=9)
    axl.text(us[0] + 0.12, (us[1] + top[1]) / 2 - 0.1, "log V\n(energy differential,\nnegative "
             "below the frontier)", fontsize=9.5, va="center", color=HIGHLIGHT)
    axl.text(-2.0, envelope_at(-2.0, ls) + 0.06, "V = const. through the design", fontsize=9.5,
             color=LEVEL_COLOR)
    axl.text(-2.0, envelope_at(-2.0, 0.0) + 0.07, "V = 1", fontsize=11, fontweight="bold",
             color=FRONTIER_COLOR)
    axl.text(ray[1, 0] + 0.08, ray[1, 1] + 0.02, "uniform scaling ray:\nall metrics up by\nthe "
             "same factor", fontsize=9.5, color=HIGHLIGHT, va="bottom", ha="left")
    axl.set_xlim(box[0], box[1])
    axl.set_ylim(box[2], box[3])
    axl.set_aspect("equal")
    axl.set_xlabel("log metric 1")
    axl.set_ylabel("log metric 2")
    axl.set_title("log space: one design and its level offset")

    # the chart (Z, log V)
    corners = []
    for a, b in active_ranges():
        for c in (a, b):
            if np.isfinite(c):
                corners.append(c)
    zc = sorted({(c - facet_line(0, c)) / np.sqrt(2) for c in corners[:1]}
                | {(c - facet_line(2, c)) / np.sqrt(2) for c in corners[-1:]})
    zlim = (Z.min() - 0.25, Z.max() + 0.25)
    edges = [zlim[0], *zc, zlim[1]]
    for k in range(3):
        axc.axvspan(edges[k], edges[k + 1], color=FACET_COLORS[k], alpha=0.12, lw=0, zorder=1)
        axc.text((edges[k] + edges[k + 1]) / 2, 0.22, f"facet {k + 1}", ha="center",
                 color=FACET_COLORS[k], fontsize=10.5, fontweight="bold")
    axc.axhline(0.0, color=FRONTIER_COLOR, lw=2.2, zorder=4)
    axc.text(zlim[1] - 0.05, 0.04, "frontier  log V = 0", ha="right", va="bottom", fontsize=10.5,
             fontweight="bold", color=FRONTIER_COLOR)
    for k in range(3):
        axc.scatter(Z[f == k], L[f == k], s=16, color=FACET_COLORS[k], alpha=0.6, lw=0, zorder=3)
    axc.plot([zs, zs], [ls, 0.0], color=HIGHLIGHT, lw=2.2, zorder=8)
    axc.add_patch(FancyArrowPatch((zs, ls), (zs, 0.0), arrowstyle="-|>", mutation_scale=16,
                                  color=HIGHLIGHT, lw=2.2, zorder=8))
    axc.scatter(zs, ls, s=140, marker="o", color=HIGHLIGHT, edgecolor="white", lw=1.5, zorder=9)
    axc.text(zs + 0.07, ls / 2, "the same log V", fontsize=10, color=HIGHLIGHT, va="center")
    axc.set_xlim(*zlim)
    axc.set_ylim(-1.75, 0.4)
    axc.set_xlabel("Z  (position along the frontier)")
    axc.set_ylabel("log V  (level offset; 0 is the frontier, up is better)")
    axc.set_title("the chart (Z, log V): the frontier flattened")

    panel_arrow(fig, axl, axc, "invertible\nchange of\ncoordinates")
    fig.suptitle("Coordinates on the trade space: position along the frontier, offset from it",
                 fontsize=15, fontweight="bold", y=0.97)
    fig.text(0.5, 0.905, "every design gets a position Z along the frontier and an energy "
             "differential log V to it; the facet bands say which trade-off binds there",
             ha="center", fontsize=10.5, color="0.3")
    save(fig, "S3", out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=pathlib.Path, default=HERE)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    style()
    for fn in (s1, s2, s3):
        fn(args.out, np.random.default_rng(20261108))
    print("wrote", sorted(p.name for p in args.out.glob("S*.png")))


if __name__ == "__main__":
    main()


# ---- S4: the three panes of S1 and S3 combined, with a finite-kappa (rounded) envelope --------
KAPPA = 8.0  # finite kappa: Phi_K is the softmax-affine (log-sum-exp) of the facet potentials


def phi_soft(u):
    x = KAPPA * (np.atleast_2d(u) @ W.T - BETA)
    m = x.max(axis=-1, keepdims=True)
    return (m[:, 0] + np.log(np.exp(x - m).sum(axis=-1))) / KAPPA


def soft_frontier(u1, level=0.0):
    """u2(u1) on the level set Phi_soft = level, by bisection (Phi_soft increases in u2)."""
    u1 = np.atleast_1d(u1)
    lo, hi = np.full_like(u1, -12.0), np.full_like(u1, 12.0)
    for _ in range(60):
        mid = (lo + hi) / 2
        above = phi_soft(np.column_stack([u1, mid])) > level
        hi = np.where(above, mid, hi)
        lo = np.where(above, lo, mid)
    return (lo + hi) / 2


def draw_soft_log(ax, box, normals=True, extend=True, lw=2.8, arrow_len=0.55):
    """Rounded envelope in log space, coloured by the dominant facet; faint facet lines."""
    u1_lo, u1_hi = box[0], box[1]
    g = np.linspace(u1_lo, u1_hi, 800)
    f = soft_frontier(g)
    lab = facet_of(np.column_stack([g, f]))
    for k in range(3):
        idx = np.where(lab == k)[0]
        if len(idx) == 0:
            continue
        sl = slice(idx[0], min(idx[-1] + 2, len(g)))  # overlap one sample so segments join
        ax.plot(g[sl], f[sl], color=FACET_COLORS[k], lw=lw, zorder=4, solid_capstyle="round")
    for k, ((a0, b0), (a, b)) in enumerate(zip(active_ranges(), visible_ranges(box))):
        if extend:
            ext = np.linspace(max(a0 - EXTEND, u1_lo), min(b0 + EXTEND, u1_hi), 60)
            ax.plot(ext, facet_line(k, ext), color=FACET_COLORS[k], lw=0.9, ls="--", alpha=0.5,
                    zorder=3)
        if normals:
            xm = (a + b) / 2
            um = np.array([xm, soft_frontier(xm)[0]])
            n = W[k] / np.linalg.norm(W[k]) * arrow_len
            ax.add_patch(FancyArrowPatch(um, um + n, arrowstyle="-|>", mutation_scale=14,
                                         color=FACET_COLORS[k], lw=1.8, zorder=6))
            ax.text(*(um + n * 1.3), rf"$w_{k + 1}$", color=FACET_COLORS[k], ha="center",
                    va="center", fontsize=11.5, fontweight="bold", zorder=7)


def draw_soft_metric(ax, box, levels=(), extend=True, lw=2.8):
    u1_lo, u1_hi = box[0], box[1]
    g = np.linspace(u1_lo, u1_hi, 800)
    for lev in levels:
        ax.plot(np.exp(g), np.exp(soft_frontier(g, np.log(lev))), color=LEVEL_COLOR, lw=1.0,
                ls=":", zorder=2)
    f = soft_frontier(g)
    lab = facet_of(np.column_stack([g, f]))
    for k in range(3):
        idx = np.where(lab == k)[0]
        if len(idx) == 0:
            continue
        sl = slice(idx[0], min(idx[-1] + 2, len(g)))
        ax.plot(np.exp(g[sl]), np.exp(f[sl]), color=FACET_COLORS[k], lw=lw, zorder=4,
                solid_capstyle="round")
    if extend:
        for k, (a0, b0) in enumerate(active_ranges()):
            ext = np.linspace(max(a0 - EXTEND, u1_lo), min(b0 + EXTEND, u1_hi), 60)
            ax.plot(np.exp(ext), np.exp(facet_line(k, ext)), color=FACET_COLORS[k], lw=0.9,
                    ls="--", alpha=0.5, zorder=3)


def s4(out, rng):
    # the cloud under the rounded envelope, plus three designs just beyond V = 1
    pts = []
    while len(pts) < 250:
        u = rng.uniform([-1.9, -1.9], [1.6, 1.6], size=(4000, 2))
        p = phi_soft(u)
        keep = (p <= 0.0) & (p >= -1.6) & (rng.uniform(size=len(u)) < np.exp(1.1 * p))
        pts.extend(u[keep])
    u = np.array(pts[:250])
    beyond_u1 = np.array([-1.35, 0.15, 1.0])
    beyond = np.column_stack([beyond_u1, soft_frontier(beyond_u1)]) + np.array([0.06, 0.08, 0.07])[:, None]
    u = np.vstack([u, beyond])
    L = phi_soft(u)
    f = facet_of(u)
    Z = (u[:, 0] - u[:, 1]) / np.sqrt(2)
    cand = np.where((f == 1) & (L < -0.55) & (L > -0.8) & (np.abs(Z) < 0.35))[0]
    i = cand[0]
    us, zs, ls = u[i], Z[i], L[i]
    top = us - ls
    levels = (0.5, 0.75, 1.25)

    fig, (axm, axl, axc) = plt.subplots(1, 3, figsize=(16, 6.4))
    fig.subplots_adjust(left=0.045, right=0.99, bottom=0.11, top=0.80, wspace=0.6)
    box_m = (np.log(0.12), np.log(5.2), np.log(0.02), np.log(5.2))
    box_l = (-2.3, 1.75, -2.1, 2.5)

    # pane 1: metric space
    scatter_by_facet(axm, u, xy=np.exp(u))
    draw_soft_metric(axm, box_m, levels=levels)
    axm.scatter(*np.exp(us), s=140, color=HIGHLIGHT, edgecolor="white", lw=1.5, zorder=9)
    axm.set_xlim(0, 5.2)
    axm.set_ylim(0, 5.2)
    axm.set_xlabel("metric 1 (larger is better)")
    axm.set_ylabel("metric 2 (larger is better)")
    axm.set_title("metric space: hyperbolic sheets,\nV = 1 on the envelope")
    for lev, x in zip(levels, (0.75, 1.05, 2.3)):
        y = np.exp(soft_frontier(np.log(x), np.log(lev))[0])
        axm.text(x + 0.08, y + 0.08, f"V = {lev:g}", fontsize=9.5, color=LEVEL_COLOR)
    axm.text(1.3, 1.45, "V = 1", fontsize=11, fontweight="bold", color=FRONTIER_COLOR)
    axm.annotate("energy levels of V\n(up and right is better)", xy=(3.2, 1.35), xytext=(3.6, 3.6),
                 fontsize=9.5, ha="center", color=LEVEL_COLOR,
                 arrowprops=dict(arrowstyle="-|>", color=LEVEL_COLOR, lw=1.0))
    axm.text(0.55, 4.75, "each sheet is one\nmonomial; the dashes\nshow it continuing\nunder the "
             "others", fontsize=9.5, color="0.3", va="top")

    # pane 2: log space, the shared view
    scatter_by_facet(axl, u, alpha=0.5)
    draw_soft_log(axl, box_l, normals=True)
    g = np.linspace(box_l[0], box_l[1], 400)
    axl.plot(g, soft_frontier(g, ls), color=LEVEL_COLOR, lw=1.0, ls=":", zorder=2)
    ray = np.array([us - 0.9, top + 0.3])
    axl.plot(ray[:, 0], ray[:, 1], color=HIGHLIGHT, lw=0.8, ls=":", zorder=5)
    axl.add_patch(FancyArrowPatch(us, top, arrowstyle="-|>", mutation_scale=16, color=HIGHLIGHT,
                                  lw=2.2, zorder=8))
    axl.scatter(*us, s=140, color=HIGHLIGHT, edgecolor="white", lw=1.5, zorder=9)
    axl.text(us[0] + 0.12, (us[1] + top[1]) / 2 - 0.1, "log V\n(energy differential,\nnegative "
             "below the frontier)", fontsize=9.5, va="center", color=HIGHLIGHT)
    axl.text(ray[1, 0] + 0.06, ray[1, 1] + 0.02, "uniform\nscaling ray:\nall metrics up\nby one "
             "factor", fontsize=9.5, color=HIGHLIGHT, va="bottom", ha="left")
    axl.text(-2.2, soft_frontier(-2.2, ls)[0] + 0.06, "V = const. through the design",
             fontsize=9.5, color=LEVEL_COLOR)
    axl.text(-2.2, soft_frontier(-2.2)[0] + 0.07, "V = 1", fontsize=11, fontweight="bold",
             color=FRONTIER_COLOR)
    axl.set_xlim(box_l[0], box_l[1])
    axl.set_ylim(box_l[2], box_l[3])
    axl.set_aspect("equal")
    axl.set_xlabel("log metric 1")
    axl.set_ylabel("log metric 2")
    axl.set_title("log space: flat facets, normals $w_k$;\none design and its level offset")
    facet_legend(axl, loc="lower left")

    # pane 3: the chart
    corners = [r[1] for r in active_ranges()[:2]]
    zc = sorted([(corners[0] - facet_line(0, corners[0])) / np.sqrt(2),
                 (corners[1] - facet_line(2, corners[1])) / np.sqrt(2)])
    zlim = (Z.min() - 0.25, Z.max() + 0.25)
    edges = [zlim[0], *zc, zlim[1]]
    for k in range(3):
        axc.axvspan(edges[k], edges[k + 1], color=FACET_COLORS[k], alpha=0.12, lw=0, zorder=1)
        axc.text((edges[k] + edges[k + 1]) / 2, 0.27, f"facet {k + 1}", ha="center",
                 color=FACET_COLORS[k], fontsize=10.5, fontweight="bold")
    axc.axhline(0.0, color=FRONTIER_COLOR, lw=2.2, zorder=4)
    axc.text(zlim[1] - 0.05, 0.1, "frontier  log V = 0", ha="right", va="bottom", fontsize=10.5,
             fontweight="bold", color=FRONTIER_COLOR)
    for k in range(3):
        axc.scatter(Z[f == k], L[f == k], s=16, color=FACET_COLORS[k], alpha=0.6, lw=0, zorder=3)
    axc.add_patch(FancyArrowPatch((zs, ls), (zs, 0.0), arrowstyle="-|>", mutation_scale=16,
                                  color=HIGHLIGHT, lw=2.2, zorder=8))
    axc.scatter(zs, ls, s=140, color=HIGHLIGHT, edgecolor="white", lw=1.5, zorder=9)
    axc.text(zs + 0.07, ls / 2, "the same log V", fontsize=10, color=HIGHLIGHT, va="center")
    axc.set_xlim(*zlim)
    axc.set_ylim(-1.75, 0.45)
    axc.set_xlabel("Z  (position along the frontier)")
    axc.set_ylabel("log V  (level offset; 0 is the frontier, up is better)")
    axc.set_title("the chart (Z, log V):\nthe frontier flattened")

    panel_arrow(fig, axm, axl, "log / exp\n(reversible)", right_pad=0.045)
    panel_arrow(fig, axl, axc, "chart (Z, log V)\n(reversible)", right_pad=0.045)
    fig.suptitle("A trade space is a manifold: K facets, each a trade-off; one design read in "
                 "the chart", fontsize=15.5, fontweight="bold", y=0.975)
    fig.text(0.5, 0.905, "designs stop at a slightly rounded envelope of K = 3 monomials, a few "
             "just beyond V = 1; each gets a position Z along the frontier and an energy "
             "differential log V to it", ha="center", fontsize=10.5, color="0.3")
    save(fig, "S4", out)


if __name__ == "__main__":
    style()
    s4(HERE, np.random.default_rng(20261108))
    print("wrote S4.png, S4@2x.png")
