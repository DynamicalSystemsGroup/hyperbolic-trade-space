"""Is the log-metric cloud tree-like?  Gromov four-point delta of the data's own distances.

    python gromov.py <clone> tables.npz

delta_rel = 2 * max over sampled quadruples of (largest - second largest of the three pair sums)/2, over the
diameter.  0 for a tree metric, larger for flat clouds.  Compared: the paper's tables (Euclidean distance on
the log-metrics), Gaussian clouds of the same size and dimension, and the repository's smalltree graph.
"""
import sys
import numpy as np
import networkx as nx

clone, tables = sys.argv[1:3]
rng = np.random.default_rng(0)


def delta_rel(D, n_quad=400_000):
    n = len(D)
    q = rng.integers(0, n, size=(n_quad, 4))
    q = q[(np.diff(np.sort(q, 1), axis=1) > 0).all(1)]
    x, y, z, w = q.T
    s = np.stack([D[x, y] + D[z, w], D[x, z] + D[y, w], D[x, w] + D[y, z]], 1)
    s.sort(1)
    return float(2 * ((s[:, 2] - s[:, 1]) / 2).max() / D.max())


def eucl(X):
    return np.linalg.norm(X[:, None] - X[None], axis=-1)


T = np.load(tables, allow_pickle=True)
for name in sorted({k.split("/")[0] for k in T.files if k.endswith("/logM")}):
    L = T[f"{name}/logM"]
    idx = rng.choice(len(L), size=min(300, len(L)), replace=False)
    g = rng.standard_normal((300, L.shape[1]))
    print(f"{name:16s} delta_rel(log-metrics) = {delta_rel(eucl(L[idx])):.3f}   gaussian same d = {delta_rel(eucl(g)):.3f}")
G = nx.Graph()
for line in open(f"{clone}/data/edges/smalltree.edges", encoding="utf-8"):
    a = line.split()
    if len(a) >= 2:
        G.add_edge(int(a[0]), int(a[1]))
nodes = np.arange(G.number_of_nodes())
D = nx.floyd_warshall_numpy(G, nodelist=nodes)
print(f"smalltree graph ({len(nodes)} nodes) delta_rel = {delta_rel(np.asarray(D)):.3f}")
