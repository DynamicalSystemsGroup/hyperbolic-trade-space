"""Measurement record for claims row C563 (the root page's package-only install to a first fit).

Usage: uv run python measure_install.py <git worktree to archive> <scratch dir>.
Three runs; keys in the output:
a = `uv sync`, b = `uv sync --no-default-groups`, c = the README first-fit snippet by
`uv run --no-default-groups python`, c_plain = the same by plain `uv run`. Output: measure.out."""

import io
import os
import shutil
import statistics
import subprocess
import sys
import tarfile
import time

WT = sys.argv[1]
OUT = sys.argv[2]
SNIP = """
from hyperbolic_trade_space import (
    HyperbolicTradeSpace, LogAffinePreconditioner, make_frontier_data, tension_report,
)
A, _ = make_frontier_data(300, 3, random_state=0)
A[:, 1] = 10 / A[:, 1]
M = LogAffinePreconditioner(orientation=[1, -1, 1]).fit_transform(A)
ts = HyperbolicTradeSpace(temperature=20.0).fit(M)
print(tension_report(ts, M).exponents.round(2))
"""


def fresh():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    tb = subprocess.run(
        ["git", "-C", WT, "archive", "HEAD"], capture_output=True, check=True
    ).stdout
    with tarfile.open(fileobj=io.BytesIO(tb)) as tar:
        tar.extractall(OUT, filter="data")


def run(cmd, **kw):
    t = time.perf_counter()
    r = subprocess.run(cmd, cwd=OUT, capture_output=True, text=True, **kw)
    return time.perf_counter() - t, r


res = {"a": [], "b": [], "c": [], "c_plain": []}
for i in range(3):
    fresh()
    t, r = run(["uv", "sync"])
    assert r.returncode == 0, r.stderr
    res["a"].append(t)
    fresh()
    t, r = run(["uv", "sync", "--no-default-groups"])
    assert r.returncode == 0, r.stderr
    res["b"].append(t)
    t, r = run(["uv", "run", "--no-default-groups", "python", "-c", SNIP])
    assert r.returncode == 0, r.stderr
    res["c"].append(t)
    t, r = run(["uv", "run", "python", "-c", SNIP])
    assert r.returncode == 0, r.stderr
    res["c_plain"].append(t)
    print(i, r.stdout.strip().replace("\n", " "), flush=True)
for k, v in res.items():
    print(
        k,
        [round(x, 1) for x in v],
        "min",
        round(min(v), 1),
        "median",
        round(statistics.median(v), 1),
    )
