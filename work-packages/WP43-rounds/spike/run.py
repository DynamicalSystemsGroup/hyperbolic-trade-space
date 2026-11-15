"""Run the WP43 spike (protocol.md): ``uv run --with cvxpy python run.py <stage>``.

Stages: ``real`` (the two regimes of the case), ``planted`` (kinds T, Q, D), ``times`` (serial
solve times), ``analyze`` (tables and verdicts from ``results/``), ``figures``, ``all``. Results
are written to ``results/``; nothing here reads a number from anywhere but the data of record
and the seeded generators.
"""

from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json  # noqa: E402
import pickle  # noqa: E402
import platform  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.model_selection import KFold  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import generators as gen  # noqa: E402
import models  # noqa: E402

RES = HERE / "results"
CACHE = HERE / "cache"
REGIMES = ("primary", "stock")
GROUPS = ("K1", "K1c", "K2", "K3", "LQ")  # K2s is fitted with K2 (it takes K2's tau)
PLANTED_MODELS = ("K1", "K1c", "K2", "K3", "LQ")
KINDS = {"T": gen.planted_t, "Q": gen.planted_q, "D": gen.planted_d}
SEEDS = range(20)
FOLDS = KFold(5, shuffle=True, random_state=0)


def measures(model, U, tau, tail=None):
    """Protocol measures 1 to 4 on held-out rows ``U`` (log metrics)."""
    lv = model.log_v(U)
    below = lv <= 0
    out = {
        "slack": float(-lv[below].mean()) if below.any() else np.nan,
        "above": float((lv > models.EPS).mean()),
        "band": float((np.abs(lv) < models.band_of(tau)).mean()),
        "n_hold": len(lv),
    }
    if tail is not None:
        for name, mask in tail.items():
            sub = lv[mask]
            b = sub <= 0
            out[f"{name}_slack"] = float(-sub[b].mean()) if b.any() else np.nan
            out[f"{name}_above"] = float((sub > models.EPS).mean()) if len(sub) else np.nan
            out[f"{name}_n"] = int(mask.sum())
    return out


def load(regime):
    sys.path.insert(0, str(models.ROOT / "examples" / "adcs"))
    import case

    return case.load_study(regime)


def plane_info(regime):
    """The plane of Figure 5 for a regime.

    The K1 fit's two heaviest metrics and the tail thresholds.
    """
    path = RES / f"plane_{regime}.json"
    if path.exists():
        return json.loads(path.read_text())
    import case
    import k_terms

    s = load(regime)
    fit = case.fit_study(s, 1)
    j, k = k_terms.slice_pairs(fit.estimator)[0]
    x = np.log(s.M[:, j])
    info = {
        "j": int(j),
        "k": int(k),
        "names": [s.names[j], s.names[k]],
        "q80": float(np.quantile(x, 0.8)),
        "q20": float(np.quantile(x, 0.2)),
        "tau_case_k1": fit.tau,
        "n": len(s.M),
    }
    RES.mkdir(exist_ok=True)
    path.write_text(json.dumps(info, indent=1))
    return info


def real_task(args):
    regime, fold, group, hints = args
    M = load(regime).M
    info = plane_info(regime)
    U = np.log(M)
    tailx = U[:, info["j"]]
    tails = {"rtail": tailx >= info["q80"], "ltail": tailx <= info["q20"]}
    idx = np.arange(len(M))
    if fold < 0:
        tr, te = idx, idx[:0]
    else:
        tr, te = list(FOLDS.split(idx))[fold]
    rows = []
    names = ("K2", "K2s") if group == "K2" else (group,)
    k2_tau = None
    for name in names:
        t_wall = time.perf_counter()
        model, tau, flag, t_sel, t_fit = models.fit_model(
            name, M[tr], tau_hint=hints.get(f"{regime}|{name}"), k2_tau=k2_tau
        )
        if name == "K2":
            k2_tau = tau
        row = {
            "regime": regime,
            "fold": fold,
            "model": name,
            "tau": tau,
            "flag": flag,
            "status": getattr(model, "status", ""),
            "ok": bool(model.ok),
            "t_select": t_sel,
            "t_fit": t_fit,
            "train_above": models.frac_above(model, U[tr]),
            "n_train": len(tr),
        }
        if len(te):
            row.update(measures(model, U[te], tau, {k: v[te] for k, v in tails.items()}))
        if name in ("LQ", "LQm"):
            row["neg_grad_frac"] = model.grad_negative_fraction(U[tr])
            row["rank_S"] = int(
                (
                    np.linalg.eigvalsh(model.S)
                    > 1e-6 * max(1e-12, np.linalg.eigvalsh(model.S).max())
                ).sum()
            )
        if fold < 0:
            CACHE.mkdir(exist_ok=True)
            with open(CACHE / f"{regime}_{name}.pkl", "wb") as fh:
                pickle.dump(model, fh)
        row["t_wall"] = time.perf_counter() - t_wall
        rows.append(row)
    return rows


def stage_real(workers):
    RES.mkdir(exist_ok=True)
    for r in REGIMES:
        plane_info(r)
    out = []
    with ProcessPoolExecutor(workers) as ex:
        full = list(ex.map(real_task, [(r, -1, g, {}) for r in REGIMES for g in GROUPS]))
        full = [row for rows in full for row in rows]
        hints = {f"{r['regime']}|{r['model']}": r["tau"] for r in full}
        out += full
        folds = list(
            ex.map(real_task, [(r, f, g, hints) for r in REGIMES for f in range(5) for g in GROUPS])
        )
        out += [row for rows in folds for row in rows]
    pd.DataFrame(out).to_csv(RES / "real_fits.csv", index=False)


def stage_lqm(workers):
    """Post-hoc (amendment 2): the log-quadratic term, every partial derivative nonnegative.

    The partials are nonnegative at the rows.
    """
    RES.mkdir(exist_ok=True)
    with ProcessPoolExecutor(workers) as ex:
        full = [
            row for rows in ex.map(real_task, [(r, -1, "LQm", {}) for r in REGIMES]) for row in rows
        ]
        folds = [
            row
            for rows in ex.map(real_task, [(r, f, "LQm", {}) for r in REGIMES for f in range(5)])
            for row in rows
        ]
    pd.DataFrame(full + folds).to_csv(RES / "real_fits_lqm.csv", index=False)


def planted_task(args):
    kind, seed = args
    X, truth = KINDS[kind](seed)
    Xt, truth_t = gen.test_sample(kind, seed, truth)
    U, Ut = np.log(X), np.log(Xt)
    idx = np.arange(len(X))
    splits = list(FOLDS.split(idx))
    rows = []
    for name in PLANTED_MODELS:
        m, _tau, _flag, _, t_fit = models.fit_model(name, X, sharp=True)
        err = m.log_v(Ut) - truth_t["log_v"]
        front = np.isclose(truth_t["log_v"], 0.0) if kind != "T" else truth_t["log_v"] > -1e-9
        row = {
            "kind": kind,
            "seed": seed,
            "model": name,
            "fold": -1,
            "n": len(X),
            "ok": bool(m.ok),
            "status": getattr(m, "status", ""),
            "t_fit": t_fit,
            "frontier_err": float(np.sqrt((err[front] ** 2).mean())),
            "overall_err": float(np.sqrt((err**2).mean())),
            "train_above": models.frac_above(m, U),
        }
        if kind == "D":
            u_c = gen.notch_point(truth)
            row["notch_level"] = float(m.log_v(u_c[None, :])[0])
            rim = gen.rim_mask(truth)
            lv = m.log_v(U[rim])
            row["rim_slack"] = float(-lv[lv <= 0].mean()) if (lv <= 0).any() else np.nan
            row["rim_above"] = float((lv > models.EPS).mean())
            row["removed"] = truth["removed"]
        rows.append(row)
        for f, (tr, te) in enumerate(splits):
            mf, tauf, _, _, _ = models.fit_model(name, X[tr], sharp=True)
            r = {
                "kind": kind,
                "seed": seed,
                "model": name,
                "fold": f,
                "n": len(tr),
                "ok": bool(mf.ok),
                "status": getattr(mf, "status", ""),
            }
            r.update(measures(mf, U[te], tauf))
            rows.append(r)
    return rows


def stage_planted(workers):
    RES.mkdir(exist_ok=True)
    tasks = [(k, s) for k in KINDS for s in SEEDS]
    with ProcessPoolExecutor(workers) as ex:
        out = [row for rows in ex.map(planted_task, tasks) for row in rows]
    pd.DataFrame(out).to_csv(RES / "planted_fits.csv", index=False)


def stage_times():
    """Serial solve times on the full regime tables.

    Three fits each at the recorded tau; one selection.
    """
    RES.mkdir(exist_ok=True)
    full = pd.read_csv(RES / "real_fits.csv")
    full = full[full.fold == -1].set_index(["regime", "model"])
    out = []
    for r in REGIMES:
        M = load(r).M
        for name in ("K1", "K1c", "K2", "K3", "K2s", "LQ"):
            tau = float(full.loc[(r, name), "tau"])
            fits = []
            for _ in range(3):
                t0 = time.perf_counter()
                if name in ("K1c", "LQ"):
                    models.QuadModel(name == "LQ").fit(np.log(M), tau)
                else:
                    models.PackageModel(
                        {"K1": 1, "K2": 2, "K3": 3, "K2s": 2}[name], name == "K2s"
                    ).fit(M, tau)
                fits.append(time.perf_counter() - t0)
            t0 = time.perf_counter()
            if name != "K2s":
                models.fit_model(name, M, tau_hint=tau)
            sel = time.perf_counter() - t0
            out.append(
                {
                    "regime": r,
                    "model": name,
                    "tau": tau,
                    "fit_s_median": float(np.median(fits)),
                    "fit_s_min": min(fits),
                    "fit_s_max": max(fits),
                    "select_and_fit_s": sel if name != "K2s" else np.nan,
                }
            )
    pd.DataFrame(out).to_csv(RES / "times.csv", index=False)


def environment():
    import cvxpy
    import scipy
    import sklearn

    import hyperbolic_trade_space as hts

    RES.mkdir(exist_ok=True)
    lines = [
        f"python {platform.python_version()}",
        f"platform {platform.platform()}",
        f"machine {platform.machine()} {platform.processor()}",
        f"numpy {np.__version__}",
        f"scipy {scipy.__version__}",
        f"scikit-learn {sklearn.__version__}",
        f"cvxpy {cvxpy.__version__}",
        f"solvers {cvxpy.installed_solvers()}",
        f"hyperbolic_trade_space {getattr(hts, '__version__', '?')}",
    ]
    try:
        import clarabel

        lines.append(f"clarabel {clarabel.__version__}")
    except Exception:
        pass
    (RES / "environment.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    workers = int(os.environ.get("SPIKE_WORKERS", "6"))
    t0 = time.perf_counter()
    if stage in ("real", "all"):
        environment()
        stage_real(workers)
    if stage in ("lqm", "all"):
        stage_lqm(workers)
    if stage in ("planted", "all"):
        stage_planted(workers)
    if stage in ("times", "all"):
        stage_times()
    if stage in ("analyze", "all"):
        import analyze

        analyze.main()
    if stage in ("figures", "all"):
        import figures

        figures.main()
        import diagnostics  # noqa: F401  (writes results/lq_monotone.md on import)
    print(f"stage {stage}: {time.perf_counter() - t0:.0f} s")
