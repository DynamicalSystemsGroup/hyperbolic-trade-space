"""Tables and verdicts of the spike, from ``results/*.csv`` by the protocol's rules.

No new numbers.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
ORDER = ["K1", "K1c", "K2", "K2s", "K3", "LQ"]
LABEL = {
    "K1": "one term (package)",
    "K1c": "one term, mean-slack criterion",
    "K2": "two terms, sharp",
    "K2s": "two terms, soft",
    "K3": "three terms, sharp",
    "LQ": "one log-quadratic term",
}
SLACK_TOL = 0.02  # a model may not sit above K1's held-out fraction above by more than this


def md(df, floatfmt="{:.4f}"):
    cols = list(df.columns)
    out = [
        "| " + " | ".join(str(c) for c in df.reset_index().columns) + " |",
        "|" + "---|" * (len(cols) + 1),
    ]
    for idx, row in df.iterrows():
        cells = [str(idx)] + [
            floatfmt.format(v) if isinstance(v, (float, np.floating)) else str(v) for v in row
        ]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def paired(df, col, model):
    """Per-fold difference ``model - K1`` of ``col``: mean, standard error, n."""
    a = df[df.model == model].set_index("fold")[col]
    b = df[df.model == "K1"].set_index("fold")[col]
    d = (a - b).dropna()
    return float(d.mean()), float(d.std(ddof=1) / np.sqrt(len(d))), len(d)


def hugs(df, model, prefix=""):
    """The protocol's 'hugs better than K1': slack below -2 se and the fraction above not higher."""
    m, se, _ = paired(df, f"{prefix}slack", model)
    ab, _, _ = paired(df, f"{prefix}above", model)
    return bool(m < -2 * se and ab <= SLACK_TOL), m, se


def verdict(df, prefix=""):
    """The four ordered rules of the protocol for one regime and one slack measure."""
    h = {m: hugs(df, m, prefix) for m in ["K2", "K2s", "K3", "LQ"]}
    if not any(v[0] for v in h.values()):
        return "none of these models hugs the bend out of sample", None
    mean = lambda m: df[df.model == m][f"{prefix}slack"].mean()  # noqa: E731
    ok = [m for m in ["K2", "K2s", "K3"] if h[m][0]]
    B = min(ok, key=mean) if ok else None
    if B is None:  # no posynomial hugs better; LQ does (rule 4)
        return "a kernel's work", None
    a = df[df.model == "LQ"].set_index("fold")[f"{prefix}slack"]
    b = df[df.model == B].set_index("fold")[f"{prefix}slack"]
    d = (a - b).dropna()
    m, se = float(d.mean()), float(d.std(ddof=1) / np.sqrt(len(d)))
    if m < -2 * se:
        return "a kernel's work", (B, m, se)
    return "more terms' work", (B, m, se)


def real():
    df = pd.read_csv(RES / "real_fits.csv")
    extra = RES / "real_fits_lqm.csv"
    has_lqm = extra.exists()
    if has_lqm:  # post-hoc, amendment 2: kept out of the protocol's verdict, shown beside it
        df = pd.concat([df, pd.read_csv(extra)], ignore_index=True)
    order = ORDER + (["LQm"] if has_lqm else [])
    out, verdicts = [], {}
    for regime in df.regime.unique():
        d = df[(df.regime == regime) & (df.fold >= 0)]
        full = df[(df.regime == regime) & (df.fold < 0)].set_index("model")
        rows = {}
        for m in order:
            s = d[d.model == m]
            row = {"tau (full table)": full.loc[m, "tau"], "train above": s.train_above.mean()}
            for c in (
                "slack",
                "above",
                "band",
                "rtail_slack",
                "rtail_above",
                "ltail_slack",
                "ltail_above",
            ):
                row[c] = s[c].mean()
            for c, label in (("slack", "d slack vs K1"), ("rtail_slack", "d rtail slack vs K1")):
                mean, se, _ = paired(d, c, m) if m != "K1" else (0.0, 0.0, 5)
                row[label] = f"{mean:+.4f} ({se:.4f})"
            row["flagged folds"] = int((s.flag.fillna("") != "").sum())
            row["not optimal"] = int((~s.ok).sum())
            rows[m] = row
        tab = pd.DataFrame(rows).T
        out.append(f"### {regime}: held-out measures, mean over five folds\n\n" + md(tab))
        v_all, det_all = verdict(d)
        v_tail, det_tail = verdict(d, "rtail_")
        verdicts[regime] = {
            "slack": v_all,
            "slack_detail": det_all,
            "rtail": v_tail,
            "rtail_detail": det_tail,
            "hugs": {m: hugs(d, m)[0] for m in ["K2", "K2s", "K3", "LQ"]},
            "hugs_rtail": {m: hugs(d, m, "rtail_")[0] for m in ["K2", "K2s", "K3", "LQ"]},
        }
        if has_lqm:
            x = {}
            for pre in ("", "rtail_"):
                h = hugs(d, "LQm", pre)
                a = d[d.model == "LQm"].set_index("fold")[f"{pre}slack"]
                row = {"hugs better than K1": h[0]}
                for ref in ("K2", "K3", "LQ"):
                    b = d[d.model == ref].set_index("fold")[f"{pre}slack"]
                    dd = (a - b).dropna()
                    row[f"minus {ref}"] = (
                        f"{dd.mean():+.4f} ({dd.std(ddof=1) / np.sqrt(len(dd)):.4f})"
                    )
                x[pre or "all rows"] = row
            verdicts[regime]["LQm"] = x
            out.append(
                "Post hoc (amendment 2), the monotone log-quadratic term LQm, "
                "paired difference in slack "
                "(mean over folds, standard error):\n\n" + md(pd.DataFrame(x).T)
            )
        out.append(f"Verdict, all held-out rows: **{v_all}**. Verdict, right tail: **{v_tail}**.\n")
        extra = full.loc["LQ", ["neg_grad_frac", "rank_S"]] if "neg_grad_frac" in full else None
        if has_lqm:
            out.append(
                f"LQm on the whole table: rank of S {int(full.loc['LQm', 'rank_S'])}, "
                "rows with a negative partial "
                f"derivative {full.loc['LQm', 'neg_grad_frac']:.3f}.\n"
            )
        if extra is not None:
            out.append(
                f"LQ on the whole table: rank of S {int(extra.rank_S)}, "
                "rows with a negative partial "
                f"derivative {extra.neg_grad_frac:.3f}.\n"
            )
    (RES / "real_summary.md").write_text("\n\n".join(out) + "\n")
    (RES / "real_verdicts.json").write_text(json.dumps(verdicts, indent=1, default=str))


def planted():
    df = pd.read_csv(RES / "planted_fits.csv")
    full, folds = df[df.fold < 0], df[df.fold >= 0]
    out = []
    rec_rows = []
    for kind in ("T", "Q", "D"):
        rows = {}
        for m in ["K1", "K1c", "K2", "K3", "LQ"]:
            f = full[(full.kind == kind) & (full.model == m)]
            g = folds[(folds.kind == kind) & (folds.model == m)]
            q = lambda c, f=f: f[c].quantile([0.25, 0.5, 0.75])  # noqa: E731
            fe, oe = q("frontier_err"), q("overall_err")
            recovered = bool(fe[0.5] <= 0.05 and oe[0.5] <= 0.10)
            r = {
                "frontier err (q25/median/q75)": f"{fe[0.25]:.3f} / {fe[0.5]:.3f} / {fe[0.75]:.3f}",
                "overall err (q25/median/q75)": f"{oe[0.25]:.3f} / {oe[0.5]:.3f} / {oe[0.75]:.3f}",
                "recovered": recovered,
                "held-out slack": g.slack.mean(),
                "held-out above": g.above.mean(),
                "not optimal": int((~f.ok).sum() + (~g.ok).sum()),
            }
            if kind == "D":
                r["notch level (median)"] = f.notch_level.median()
                r["notch level (min)"] = f.notch_level.min()
                r["rim slack"] = f.rim_slack.mean()
                r["rim above"] = f.rim_above.mean()
            rows[m] = r
            rec_rows.append(
                {
                    "kind": kind,
                    "model": m,
                    "recovered": recovered,
                    "frontier_median": fe[0.5],
                    "overall_median": oe[0.5],
                }
            )
        out.append(
            f"### kind {kind}: {len(full[(full.kind == kind) & (full.model == 'K1')])} tables\n\n"
            + md(pd.DataFrame(rows).T)
        )
    # kind Q split by rank
    q = full[(full.kind == "Q")]
    rk = {}
    for m in ["K1", "K2", "K3", "LQ"]:
        for lo, hi, lab in ((0, 9, "rank 1"), (10, 19, "rank 2")):
            f = q[(q.model == m) & (q.seed >= lo) & (q.seed <= hi)]
            rk[f"{m} {lab}"] = {
                "frontier err median": f.frontier_err.median(),
                "overall err median": f.overall_err.median(),
            }
    out.append("### kind Q by rank of the planted Q\n\n" + md(pd.DataFrame(rk).T))
    (RES / "planted_summary.md").write_text("\n\n".join(out) + "\n")
    pd.DataFrame(rec_rows).to_csv(RES / "planted_recovery.csv", index=False)


def times():
    p = RES / "times.csv"
    if p.exists():
        t = pd.read_csv(p)
        t["key"] = t.regime + " / " + t.model
        (RES / "times_summary.md").write_text(
            md(t.drop(columns=["regime", "model"]).set_index("key"), "{:.2f}") + "\n"
        )


def main():
    if (RES / "real_fits.csv").exists():
        real()
    if (RES / "planted_fits.csv").exists():
        planted()
    times()


if __name__ == "__main__":
    main()
