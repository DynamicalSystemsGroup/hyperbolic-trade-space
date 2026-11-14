"""Shared steps of the WP45 test records: fetch with a hash check, and the fit-and-read routine.

The three cases (perovskite, amniote, wheat) differ in their data and conditioning rule and share
everything below: a fetch that fails loudly when the source changes (R-1), and one routine that
takes conditioned metrics through temperature selection, the K = 1 and K = 2 fits and the tension
report, and a sensitivity table over temperature.

Nothing here is imported by the package; the scripts import it from their own folder.
"""

from __future__ import annotations

import hashlib
import json
import tomllib
import urllib.request
import warnings
import zipfile
from pathlib import Path

import numpy as np


def load_manifest(path):
    """Read a ``manifest.toml`` (source, DOI, licence, hashes) as a dict."""
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def file_hash(path, algo):
    """Hex digest of a file."""
    h = hashlib.new(algo)
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify(path, manifest):
    """Raise ``RuntimeError`` unless the file's size and hashes are the manifest's."""
    path = Path(path)
    if path.stat().st_size != manifest["size"]:
        raise RuntimeError(
            f"{path.name}: size {path.stat().st_size} != manifest {manifest['size']}; "
            "the source changed, re-read the record before trusting the table"
        )
    for algo in ("md5", "sha256"):
        if algo in manifest and file_hash(path, algo) != manifest[algo]:
            raise RuntimeError(
                f"{path.name}: {algo} differs from the manifest; the source changed, "
                "re-read the record before trusting the table"
            )


def fetch_zip(manifest, cache):
    """Download the archive named in ``manifest`` into ``cache`` (once), verify it, unpack it.

    Returns the folder holding the unpacked files. The cache is ignored by git; nothing
    downloaded is committed.
    """
    cache = Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    zpath = cache / manifest["file"]
    if not zpath.exists():
        urllib.request.urlretrieve(manifest["url"], zpath)
    verify(zpath, manifest)
    out = cache / "unpacked"
    if not out.exists():
        with zipfile.ZipFile(zpath) as zf:
            zf.extractall(out)
    return out


def read_threads():
    """Cap the BLAS threads of the fits so the scripts do not fight for a shared machine."""
    import os

    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ.setdefault(k, "2")


def fit_read(M, names, target=0.10, taus=(3.0, 10.0, 30.0, 100.0, np.inf), k2=True, seed=0):
    """Fit conditioned metrics and read the result.

    Parameters
    ----------
    M : ndarray of shape (n, d)
        Strictly positive larger-is-better metrics.
    names : sequence of str
        Metric names, in column order.
    target : float
        Fraction of rows above V = 1 that selects the working temperature.
    taus : sequence of float
        Temperatures of the sensitivity table (the selected one is added).
    k2 : bool
        Also fit K = 2.
    seed : int
        Seed of the K = 2 initializations.

    Returns
    -------
    dict
        JSON-ready: counts, selected temperature, K = 1 exponents, contending set at tau = inf,
        the near-frontier association, the table over temperatures, and the K = 2 terms.
    """
    from hyperbolic_trade_space import HyperbolicTradeSpace, select_temperature, tension_report

    M = np.asarray(M, float)
    names = list(names)
    out = {"n": int(M.shape[0]), "metrics": names}
    tau = float(select_temperature(M, target_frac_above=target, bounds=(3.0, 1e4)))
    est = HyperbolicTradeSpace(temperature=tau, random_state=seed).fit(M)
    out["tau_selected"] = tau
    out["target_frac_above"] = target
    out["frac_above"] = float(est.frac_above_)
    out["exponents_k1"] = dict(zip(names, map(float, est.exponents_[0]), strict=True))
    out["n_eff"] = float(est.n_eff_)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rep = tension_report(est, M)
    out["contending_set"] = [names[j] for j in rep.contending_set]
    out["contending_exponents"] = [float(x) for x in rep.contending_exponents]
    out["n_lemma"] = int(rep.n_lemma)
    out["band"] = float(rep.band)
    out["n_near_frontier"] = int(rep.n_near_frontier)
    out["association"] = {
        f"{names[i]}|{names[j]}": float(rep.association[i, j])
        for i in range(len(names))
        for j in range(i + 1, len(names))
    }
    rows = []
    for t in sorted({float(x) for x in taus} | {tau}):
        e = HyperbolicTradeSpace(temperature=t, random_state=seed).fit(M)
        rows.append(
            {
                "tau": t,
                "exponents": dict(zip(names, map(float, e.exponents_[0]), strict=True)),
                "frac_above": float(e.frac_above_),
            }
        )
    out["by_temperature"] = rows
    if k2 and M.shape[0] >= 40:
        e2 = HyperbolicTradeSpace(n_terms=2, temperature=tau, random_state=seed, n_restarts=5).fit(
            M
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                r2 = tension_report(e2, M)
                lem = [[names[j] for j in r.contending_set] for r in r2]
            except ValueError as err:
                lem = str(err)[:200]
        out["k2"] = {
            "exponents": [dict(zip(names, map(float, w), strict=True)) for w in e2.exponents_],
            "term_share": [float(s) for s in e2.term_share_],
            "mean_slack": float(e2.mean_slack_),
            "mean_slack_k1": float(est.mean_slack_),
            "contending_sets": lem,
            "status": getattr(e2.termination_, "status", None),
        }
    return out


def dump(result, path):
    """Write a result dict as sorted, indented JSON."""
    Path(path).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
