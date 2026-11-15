"""WP50 D-3: persistent homology on the chart, a planted table and the cubesat chart of record.

Run from the repository root (the scratch environment adds the topology libraries; nothing is
added to pyproject.toml or uv.lock)::

    uv run --frozen --with gudhi --with ripser --with persim --with matplotlib \
        python work-packages/WP50-rounds/spike/instance/instance.py

It writes ``out/results.json`` (every number the instance.md reads), the diagrams as ``out/*.npz``
and the figures ``out/*.png``. Every random choice is seeded; a rerun gives the same diagrams.

Vocabulary: a *candidate hole* is a class of the persistence diagram that outlives a hole-free
null; it is a hypothesis until a witness is sampled. *White space* is the envelope method's word.

Licences of the libraries: ripser and persim are MIT; gudhi's alpha complex is MIT with a GPL v3
dependency (CGAL) for the Euclidean versions (https://gudhi.inria.fr/licensing/).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gudhi
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from persim import bottleneck
from ripser import ripser
from scipy.spatial import Delaunay, cKDTree
from scipy.stats import gaussian_kde

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "examples" / "adcs"))

import case  # noqa: E402

from hyperbolic_trade_space import HyperbolicTradeSpace, make_frontier_data  # noqa: E402

RESULTS: dict = {}


# ---------------------------------------------------------------------------------------------
# Persistence tools
# ---------------------------------------------------------------------------------------------


def alpha_persistence(P, max_dim):
    """Alpha-complex persistence of a point cloud, with the death simplex of each class.

    Returns ``(dgms, pairs)``; ``dgms[k]`` is an array of (birth, death) radii of degree k (the
    infinite class of degree 0 excluded), ``pairs[k]`` the death simplex (vertex tuple) of each
    finite class, in the same order.
    """
    ac = gudhi.AlphaComplex(points=P)
    st = ac.create_simplex_tree(output_squared_values=False)
    st.compute_persistence()
    dgms, pairs = [], []
    raw = st.persistence_pairs()
    for k in range(max_dim + 1):
        rows, simp = [], []
        for birth, death in raw:
            if len(birth) != k + 1 or len(death) == 0:
                continue
            b, d = st.filtration(birth), st.filtration(death)
            if d > b:
                rows.append((b, d))
                simp.append(tuple(death))
        dgms.append(np.array(rows).reshape(-1, 2))
        pairs.append(simp)
    return dgms, pairs


def circumcentre(P):
    """Circumcentre and radius of the simplex whose vertices are the rows of P."""
    A = 2 * (P[1:] - P[0])
    b = (P[1:] ** 2).sum(1) - (P[0] ** 2).sum()
    c = np.linalg.solve(A @ A.T, b - A @ P[0]) @ A + P[0]
    return c, float(np.linalg.norm(c - P[0]))


def persistence(dgm):
    return (dgm[:, 1] - dgm[:, 0]) if len(dgm) else np.zeros(0)


def null_threshold(sampler, k, n_null, seed, max_dim):
    """Largest degree-k persistence over ``n_null`` draws of a hole-free sampler."""
    rng = np.random.default_rng(seed)
    top = []
    for _ in range(n_null):
        dg, _ = alpha_persistence(sampler(rng), max_dim)
        p = persistence(dg[k])
        top.append(p.max() if len(p) else 0.0)
    return float(np.max(top)), [float(t) for t in top]


def summary(dgm, thr):
    p = persistence(dgm)
    above = p[p > thr]
    return {
        "classes": len(p),
        "above_null": len(above),
        "max_persistence": float(p.max()) if len(p) else 0.0,
        "total_persistence_above_null": float(above.sum()),
    }


# ---------------------------------------------------------------------------------------------
# Part A: the planted table (a hole is known to exist; one is feasible, one is not)
# ---------------------------------------------------------------------------------------------

D = 3
SEED = 0


def planted_chart(n_big=6000):
    """A hole-free planted table in the chart: ``(Z, log V)`` of a K = 1 fit, plus the fit."""
    X, _info = make_frontier_data(n_big, D, random_state=SEED)
    est = HyperbolicTradeSpace(random_state=SEED).fit(X)
    T = est.transform(X)
    return est, X, T[:, :-1], T[:, -1]


def in_disk(Z, c, r):
    return np.linalg.norm(Z - c, axis=1) < r


def part_a():
    _est, _X, Z, lv = planted_chart()
    # the two unsampled regions: centres on the interior of the sample, radius 0.45 of the spread
    centre = np.median(Z, axis=0)
    spread = Z.std(axis=0).mean()
    # Place the two planted regions on points of the sample away from the centre and each other.
    cA = centre + np.array([-0.9, 0.0]) * spread
    cB = centre + np.array([0.9, 0.0]) * spread
    r = 0.45 * spread
    N = 700
    keep_all = ~(in_disk(Z, cA, r) | in_disk(Z, cB, r))
    idx = np.flatnonzero(keep_all)[:N]
    Zs, lvs = Z[idx], lv[idx]
    RESULTS["planted"] = {
        "n_rows": len(idx),
        "centre_A": cA.tolist(),
        "centre_B": cB.tolist(),
        "radius": float(r),
        "spread": float(spread),
        "n_removed_from_first_6000": int((~keep_all).sum()),
    }

    # hole-free null: the first N designs of the same draw without removing the disks, plus
    # a Gaussian-KDE resampler of the sample's own position (no holes by construction)
    def null_sampler_factory(Zsample):
        kde = gaussian_kde(Zsample.T, bw_method=0.25)
        return lambda rng: kde.resample(N, seed=int(rng.integers(1 << 31))).T

    # Z-only (distance = the chart's Euclidean position metric)
    thr1, _top1 = null_threshold(
        lambda rng: Z[rng.choice(len(Z), N, replace=False)], 1, 30, SEED, 1
    )
    dg, pr = alpha_persistence(Zs, 1)
    p1 = persistence(dg[1])
    order = np.argsort(-p1)[:6]
    cand = []
    for j in order:
        tri = Zs[list(pr[1][j])]
        c, rad = circumcentre(tri)
        cand.append(
            {
                "persistence": float(p1[j]),
                "birth": float(dg[1][j, 0]),
                "death": float(dg[1][j, 1]),
                "centre": c.tolist(),
                "radius": rad,
                "in_A": bool(np.linalg.norm(c - cA) < r),
                "in_B": bool(np.linalg.norm(c - cB) < r),
                "above_null": bool(p1[j] > thr1),
            }
        )
    RESULTS["planted"]["null_max_H1_Zonly"] = thr1
    RESULTS["planted"]["candidates_before"] = cand
    RESULTS["planted"]["summary_before"] = summary(dg[1], thr1)
    np.savez(OUT / "planted_before.npz", Z=Zs, lv=lvs, h0=dg[0], h1=dg[1])

    # Rips cross-check (ripser, MIT): the same two classes by a different complex
    rg = ripser(Zs, maxdim=1)["dgms"][1]
    rp = np.sort(rg[:, 1] - rg[:, 0])[::-1][:4]
    RESULTS["planted"]["ripser_top_H1_persistence"] = [float(x) for x in rp]
    RESULTS["planted"]["ripser_convention"] = "Rips scale is edge length (diameter), twice a radius"

    # The sampling rule: for each candidate above the null, propose the circumcentre; a witness
    # is a measured design there. The oracle is the planted generator: it returns a design
    # anywhere outside B and nothing inside B (B is the region the attainable set lacks).
    rng = np.random.default_rng(SEED + 1)
    tree = cKDTree(Zs)

    def oracle(zq):
        """Measure a design at chart position zq; None if the region is infeasible."""
        if np.linalg.norm(zq - cB) < r:
            return None
        k = tree.query(zq, 8)[1]
        level = float(np.median(lvs[k]))
        meas_level = level + 0.15 * float(
            rng.standard_normal()
        )  # a measurement, not the prediction
        return meas_level, level

    log = []
    new_Z, new_lv = [], []
    for c in cand:
        if not c["above_null"]:
            continue
        zc = np.array(c["centre"])
        target = "A" if c["in_A"] else ("B" if c["in_B"] else "other")
        attempts = 0
        found = None
        budget = 12  # the stated effort: the proposal and eleven jittered within half the radius
        while attempts < budget and found is None:
            jitter = 0 if attempts == 0 else 0.5 * c["radius"] * rng.standard_normal(2) / 2
            zq = zc + jitter
            attempts += 1
            got = oracle(zq)
            if got is not None:
                found = (zq, got)
        entry = {"target": target, "attempts": attempts, "found": found is not None}
        if found:
            zq, (ml, pl) = found
            entry.update(position=zq.tolist(), predicted_level=pl, measured_level=ml)
            new_Z.append(zq)
            new_lv.append(ml)
        log.append(entry)
    RESULTS["planted"]["sampling_log"] = log

    Z2 = np.vstack([Zs, new_Z]) if new_Z else Zs
    dg2, _pr2 = alpha_persistence(Z2, 1)
    p2 = persistence(dg2[1])
    top2 = np.sort(p2)[::-1][:4]
    RESULTS["planted"]["summary_after"] = summary(dg2[1], thr1)
    RESULTS["planted"]["top_H1_after"] = [float(x) for x in top2]
    RESULTS["planted"]["top_H1_before"] = [float(x) for x in np.sort(p1)[::-1][:4]]
    np.savez(OUT / "planted_after.npz", Z=Z2, h1=dg2[1])

    # What each choice of distance does: the cloud (Z, s * log V) for several level weights s.
    # s = 0 is the position-only cloud; s = sqrt(d) makes the chart an isometric copy of log
    # metrics at K = 1 up to the shear of log V by w . B^T Z (L8), not a free choice of unit.
    rows = []
    for s in (0.0, 0.5, 1.0, np.sqrt(D), 2.0 * np.sqrt(D)):
        P = np.column_stack([Zs, s * lvs]) if s > 0 else Zs
        dgs, _ = alpha_persistence(P, 2 if s > 0 else 1)
        Pn = np.column_stack([Z, s * lv]) if s > 0 else Z
        thr, _ = null_threshold(
            lambda rg_, Pn=Pn: Pn[rg_.choice(len(Pn), N, replace=False)],
            1,
            10,
            SEED,
            2 if s > 0 else 1,
        )
        pp = persistence(dgs[1])
        rows.append(
            {
                "level_weight": float(s),
                "null_max_H1": thr,
                "top_H1": [float(x) for x in np.sort(pp)[::-1][:4]],
                "above_null": int((pp > thr).sum()),
                "H2_classes": len(dgs[2]) if s > 0 else None,
                "H2_max": float(persistence(dgs[2]).max()) if s > 0 and len(dgs[2]) else None,
            }
        )
    RESULTS["planted"]["distance_choices"] = rows

    # Figure: before and after, the candidate circumcentres and the planted regions
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.6), sharex=True, sharey=True)
    for a, (P_, ttl) in zip(
        ax, [(Zs, "before sampling"), (Z2, "after the witness sampling")], strict=False
    ):
        a.scatter(*P_.T, s=4, c="0.35")
        for cc, nm in ((cA, "A"), (cB, "B")):
            a.add_patch(plt.Circle(cc, r, fill=False, ls="--", ec="C1"))
            a.annotate(
                nm, cc + np.array([0, r + 0.12]), color="C1", ha="center", va="bottom", fontsize=14
            )
        a.set_title(ttl)
        a.set_aspect("equal")
        a.set_xlabel("position Z1")
    ax[0].set_ylabel("position Z2")
    for c in cand:
        if c["above_null"]:
            ax[0].plot(*c["centre"], "x", c="C3", ms=14, mew=2)
    if new_Z:
        ax[1].scatter(*np.array(new_Z).T, s=60, c="C2", marker="D", edgecolors="k", zorder=5)
    fig.suptitle(
        "Planted table: x = candidate hole, diamond = witness, dashed = region left unsampled"
    )
    fig.tight_layout()
    fig.savefig(OUT / "planted_chart.png", dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(1, 2, figsize=(9, 4), sharex=True, sharey=True)
    for a, (dgm, ttl) in zip(ax, [(dg[1], "before"), (dg2[1], "after")], strict=False):
        a.scatter(dgm[:, 0], dgm[:, 1], s=10)
        m = float(max(dg[1].max(), 0.1))
        a.plot([0, m], [0, m], "k:", lw=0.8)
        a.plot([0, m], [thr1, m + thr1], "C3", lw=0.8, label="null maximum")
        a.set_title(f"degree 1, {ttl}")
        a.set_xlabel("birth (radius)")
    ax[0].set_ylabel("death (radius)")
    ax[0].legend()
    fig.tight_layout()
    fig.savefig(OUT / "planted_diagram.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------------------------
# Part B: the cubesat chart of record (K = 2)
# ---------------------------------------------------------------------------------------------


def part_b():
    names = case.TERNARY_PAIR["A"][1]
    st = case.triple_study("primary", names)
    fit = case.fit_study(st, K=2)
    est = fit.estimator
    T = est.transform(st.M)
    Z, lv = T[:, :-1], T[:, -1]
    n = len(Z)
    W, B = est.exponents_, est.basis_
    # the seam: how many designs sit on each term's side, and the slope of log V in Z per term
    lab = est._assign(np.log(st.M))
    slopes = [float(np.linalg.norm(np.linalg.solve(B[0] @ B[0].T, B[0] @ W[k]))) for k in range(2)]
    RESULTS["cubesat"] = {
        "attributes": list(names),
        "n": int(n),
        "K": 2,
        "tau": float(fit.tau),
        "term_counts": [int((lab == k).sum()) for k in range(2)],
        "level_slope_in_Z_per_term": slopes,
        "chord_over_path_bound": float(1 / np.sqrt(1 + max(slopes) ** 2)),
        "Z_min": Z.min(0).tolist(),
        "Z_max": Z.max(0).tolist(),
        "logV_range": [float(lv.min()), float(lv.max())],
    }

    kde = gaussian_kde(Z.T, bw_method=0.2)

    def null_Z(rng):
        return kde.resample(n, seed=int(rng.integers(1 << 31))).T

    thr0, _ = null_threshold(null_Z, 0, 20, SEED, 1)
    thr1, _top1 = null_threshold(null_Z, 1, 20, SEED, 1)
    dg, pr = alpha_persistence(Z, 1)
    p0, p1 = persistence(dg[0]), persistence(dg[1])
    RESULTS["cubesat"]["Zonly"] = {
        "null_max_H0": thr0,
        "null_max_H1": thr1,
        "H0": summary(dg[0], thr0),
        "H1": summary(dg[1], thr1),
        "top_H0": [float(x) for x in np.sort(p0)[::-1][:5]],
        "top_H1": [float(x) for x in np.sort(p1)[::-1][:5]],
    }
    order = np.argsort(-p1)[:5]
    cands = []
    hull = Delaunay(Z)
    for j in order:
        c, rad = circumcentre(Z[list(pr[1][j])])
        cands.append(
            {
                "persistence": float(p1[j]),
                "centre": c.tolist(),
                "radius": rad,
                "inside_hull_of_sample": bool(hull.find_simplex(c) >= 0),
                "above_null": bool(p1[j] > thr1),
            }
        )
    RESULTS["cubesat"]["Zonly"]["candidates"] = cands

    # how the null's smoothing changes the reading: the same data, three bandwidths
    sens = {}
    for bw in (0.1, 0.2, 0.4):
        kb = gaussian_kde(Z.T, bw_method=bw)
        t1, _ = null_threshold(
            lambda rng, kb=kb: kb.resample(n, seed=int(rng.integers(1 << 31))).T, 1, 12, SEED, 1
        )
        sens[f"bw={bw}"] = {"null_max_H1": t1, "above_null": int((p1 > t1).sum())}
    RESULTS["cubesat"]["Zonly"]["null_bandwidth_sensitivity"] = sens

    # the near-frontier band: designs within delta of the surface (the white space on the frontier)
    delta = 0.5
    band = lv > -delta
    Zb = Z[band]
    kdeb = gaussian_kde(Zb.T, bw_method=0.2)
    thrb, _ = null_threshold(
        lambda rng: kdeb.resample(len(Zb), seed=int(rng.integers(1 << 31))).T, 1, 20, SEED, 1
    )
    dgb, _ = alpha_persistence(Zb, 1)
    pb = persistence(dgb[1])
    RESULTS["cubesat"]["band"] = {
        "delta": delta,
        "n": int(band.sum()),
        "null_max_H1": thrb,
        "H1": summary(dgb[1], thrb),
        "top_H1": [float(x) for x in np.sort(pb)[::-1][:5]],
    }

    # the three-dimensional chart (Z, s log V), s = 1 and s = sqrt(d): H1 and H2
    d3 = {}
    for s in (1.0, float(np.sqrt(3))):
        P = np.column_stack([Z, s * lv])
        k3 = gaussian_kde(P.T, bw_method=0.2)
        thr = {}
        for k in (1, 2):
            thr[k], _ = null_threshold(
                lambda rng, k3=k3: k3.resample(n, seed=int(rng.integers(1 << 31))).T, k, 8, SEED, 2
            )
        dgs, _ = alpha_persistence(P, 2)
        d3[f"s={s:.3f}"] = {
            "null_max_H1": thr[1],
            "null_max_H2": thr[2],
            "H1": summary(dgs[1], thr[1]),
            "H2": summary(dgs[2], thr[2]),
            "top_H1": [float(x) for x in np.sort(persistence(dgs[1]))[::-1][:3]],
            "top_H2": [float(x) for x in np.sort(persistence(dgs[2]))[::-1][:3]],
        }
    RESULTS["cubesat"]["chart3d"] = d3

    # Figure: the chart's position plane with the designs, near-frontier designs, candidates
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.8))
    sc = ax[0].scatter(*Z.T, s=3, c=lv, cmap="viridis")
    fig.colorbar(sc, ax=ax[0], label="log V")
    for c in cands:
        mk = "x" if c["above_null"] else "+"
        ax[0].plot(*c["centre"], mk, c="C3", ms=10, mew=2)
    ax[0].set_title(
        "cubesat chart, K = 2: Z coloured by log V\n+ = five longest loops, none above the null"
    )
    ax[0].set_aspect("equal")
    ax[1].scatter(dg[1][:, 0], dg[1][:, 1], s=8)
    m = float(dg[1].max())
    ax[1].plot([0, m], [0, m], "k:", lw=0.8)
    ax[1].plot([0, m], [thr1, m + thr1], "C3", lw=0.8, label="null maximum")
    ax[1].set_title(f"degree 1, position only, n = {n}")
    ax[1].set_xlabel("birth (radius)")
    ax[1].set_ylabel("death (radius)")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(OUT / "cubesat_chart.png", dpi=130)
    plt.close(fig)
    np.savez(OUT / "cubesat_Zonly.npz", Z=Z, lv=lv, h0=dg[0], h1=dg[1])

    # ----- refit invariance (the definition must survive refits) -----
    rng = np.random.default_rng(SEED)
    half = rng.choice(n, n // 2, replace=False)
    _, _k, _ = case._lib()
    est2 = _k.fit_k(st.M[half], 2, fit.tau, 1)
    T2 = est2.transform(st.M)
    dZ = float(np.abs(T2[:, :-1] - Z).max())
    dlv = float(np.abs(T2[:, -1] - lv).max())
    P1, P2 = np.column_stack([Z, lv]), np.column_stack([T2[:, :-1], T2[:, -1]])
    d1, _ = alpha_persistence(P1, 1)
    d2, _ = alpha_persistence(P2, 1)
    dg0b = bottleneck(d1[1], d2[1])
    # Rips diagrams (ripser, diameters) at the shared landmark subset for the stability bound
    sub = rng.choice(n, 400, replace=False)
    r1 = ripser(P1[sub], maxdim=1)["dgms"][1]
    r2 = ripser(P2[sub], maxdim=1)["dgms"][1]
    RESULTS["cubesat"]["refit"] = {
        "max_abs_change_in_Z": dZ,
        "max_abs_change_in_logV": dlv,
        "bottleneck_H1_alpha_radius": float(dg0b),
        "bottleneck_H1_rips_400_landmarks": float(bottleneck(r1, r2)),
        "bound_rips_2_times_max_row_change": float(2 * np.linalg.norm(P1 - P2, axis=1).max()),
    }

    # ----- the four-metric chart, 4 dimensions: landmarks, Rips -----
    st4 = case.view_study(case.load_study("primary"))
    f4 = case.fit_study(st4, K=2)
    T4 = f4.estimator.transform(st4.M)
    res = ripser(T4, maxdim=2, n_perm=400)
    out4 = {}
    for k in (1, 2):
        pk = persistence(res["dgms"][k])
        out4[f"H{k}"] = {"classes": len(pk), "top": [float(x) for x in np.sort(pk)[::-1][:4]]}
    # hole-free null at the same landmarks: Gaussian-KDE draws of the 4-D chart
    k4 = gaussian_kde(T4.T, bw_method=0.2)
    nl = {1: [], 2: []}
    for i in range(4):
        Pn = k4.resample(len(T4), seed=100 + i).T
        rn = ripser(Pn, maxdim=2, n_perm=400)["dgms"]
        for k in (1, 2):
            pn = persistence(rn[k])
            nl[k].append(float(pn.max()) if len(pn) else 0.0)
    out4["null_max"] = {f"H{k}": float(max(nl[k])) for k in (1, 2)}
    out4["note"] = "ripser, 400 greedy landmarks, diameters; K = 2 four-metric chart, 4 coordinates"
    RESULTS["cubesat"]["chart4d"] = out4


def part_c():
    """Checks behind objects-and-distances.md: what the chart's distances are invariant to."""
    from scipy.spatial.distance import pdist

    X, _ = make_frontier_data(300, D, random_state=3)
    est = HyperbolicTradeSpace(random_state=3).fit(X)
    T = est.transform(X)
    c = np.array([1e-3, 40.0, 7.0])  # a change of unit in each metric
    T2 = est.transform(X * c)
    raw = pdist(X), pdist(X * c)
    chart = pdist(T), pdist(T2)
    # K = 1: (Z, sqrt(d) * (log V - w . B^T Z)) is an isometric copy of the log metrics
    U = np.log(X)
    w, B = np.ravel(est.exponents_), est.basis_
    shear = T[:, -1] - T[:, :-1] @ (B @ w)
    iso = np.column_stack([T[:, :-1], np.sqrt(D) * shear])
    RESULTS["objects"] = {
        "chart_distance_change_under_unit_change": float(np.abs(chart[0] - chart[1]).max()),
        "raw_distance_ratio_range_under_unit_change": [
            float((raw[1] / raw[0]).min()),
            float((raw[1] / raw[0]).max()),
        ],
        "isometry_error_K1_sheared_chart_vs_log_metrics": float(
            np.abs(pdist(iso) - pdist(U)).max()
        ),
        "chart_vs_log_metric_distance_ratio_range_K1": [
            float((pdist(T) / pdist(U)).min()),
            float((pdist(T) / pdist(U)).max()),
        ],
    }


if __name__ == "__main__":
    part_c()
    part_a()
    part_b()
    with open(OUT / "results.json", "w") as fh:
        json.dump(RESULTS, fh, indent=1)
    print(json.dumps(RESULTS, indent=1)[:6000])
