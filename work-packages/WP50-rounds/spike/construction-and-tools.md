# WP50 D-2: the construction, the tools, the sources

Read 2026-11-14 (every source below was opened that day). Serves G2. Depth of reading is stated per source because it
limits what is claimed from it: **full** (read in the text), **part** (named passages read), **abstract** (the publisher's or arXiv abstract read),
**record** (the bibliographic record resolved and the title read, nothing more). A claim in this file rests on a source read
to the depth the claim needs, or on the instance (`instance.md`), or is marked as not established.

## The point of departure he named, and what it gives

His thesis (21:35): the learned coordinate system decides what is near what; the topology then reads that nearness. The three
works he named, read as follows. "Topological landmarks" is read as the landmark and witness complexes of de Silva and
Carlsson, the one landmark construction in the persistent-homology literature that the scope's G2 names; if he meant another
work, that is a one-line correction.

| Source | Read | What it establishes (for this spike) |
|---|---|---|
| Ghrist, *Barcodes: the persistent topology of data*, Bull. AMS 45(1):61-75 (2008; online 2007-10-26). DOI 10.1090/S0273-0979-07-01191-3 | the abstract, the Figure 3 caption and the passages on noise (the Edinburgh copy of the printed article, `webhomes.maths.ed.ac.uk/~v1ranick/papers/ghrist1.pdf`); not the whole article | Persistent homology of a point cloud as a barcode, a survey of Carlsson and collaborators' work. Its Figure 3 captions the question this spike turns into a protocol: "Which holes are real and which are noise?" |
| de Silva and Ghrist, *Coverage in sensor networks via persistent homology*, Algebr. Geom. Topol. 7:339-358 (2007). DOI 10.2140/agt.2007.7.339 | abstract (msp.org) and the main theorem and introduction (the author's preprint copy, `webhomes.maths.ed.ac.uk/~v1ranick/tda/desilvaghrist1.pdf`) | A homological **criterion that guarantees** coverage: for fixed nodes and a fence, if the map `H_d(R_s, F_s) -> H_d(R_w, F_w)` of a pair of Rips complexes is nonzero, the sensor cover contains the domain away from its boundary (Theorem 3.4). The condition is **sufficient, not necessary**: a nonzero map certifies there is no hole; a class that persists is not by itself a certificate of one. The pair `(R, F)` carries a fence, the relative treatment of the boundary |
| de Silva and Ghrist, *Coordinate-free coverage in sensor networks with controlled boundaries via homology*, Int. J. Robotics Res. 25(12):1205-1222 (2006). DOI 10.1177/0278364906072252 | record | The boundary-controlled version of the coverage criterion; cited for the fence only |
| de Silva and Carlsson, *Topological estimation using witness complexes*, Eurographics SPBG (2004). DOI 10.2312/SPBG/SPBG04/157-166 (resolves to `diglib.eg.org/items/fd03e9fe-d315-4c7d-8220-7b0ff2449fff`) | record, plus a secondary summary (the lazy variant and the maxmin landmark rule); not read in full | Landmarks chosen from the data, the remaining points as witnesses of which simplices on the landmarks to include; a nested family suitable for persistence. The secondary summary says witness complexes carry no guarantee of the homotopy type of the space; I do not rely on it for more than the construction |

## The construction, step by step

1. **Points.** Designs, as the chart places them (`objects-and-distances.md`): `(Z, s log V)` or `Z` alone.
2. **A complex at each scale r.** Four are used in the literature read:
   - Vietoris-Rips: a simplex when all pairwise distances are at most the scale (a clique complex on the proximity graph).
     Needs only the distances, so it is the one a coordinate-free setting can use (de Silva and Ghrist). It can contain
     simplices a ball cover would not (the "phantom" classes the sensor paper's Figure 1 shows), and its scale is a
     **diameter**, twice the radius of the cover.
   - Alpha (Delaunay, Čech-equivalent) complex: the Delaunay triangulation filtered by circumradius. It has the same
     persistent homology as the Čech complex and is much smaller (GUDHI documentation, "Delaunay complex", read 2026-11-14), so it
     is the exact choice in low dimension. Its scale is a **radius**.
   - Witness complex on landmarks: scales to many points and to higher dimension; the cost is that the landmark rule matters
     (maxmin rules favour outliers, per the secondary summary above).
   - Čech: the nerve of balls; the reference the others approximate; not built directly.
3. **Persistent homology.** Track connected components (degree 0), loops (degree 1) and voids (degree 2) as the scale grows;
   a class is born at one scale and dies at a larger one. The persistence diagram is the multiset of `(birth, death)`; the
   barcode is the same as intervals (Ghrist). Algorithms: Zomorodian and Carlsson (2005, DOI 10.1007/s00454-004-1146-y,
   record) for computing it; Edelsbrunner, Letscher and Zomorodian (2002, DOI 10.1007/s00454-002-2885-2, record) for the
   notion of persistence. Neither is read beyond its record; the instance computes what the tools compute.
4. **A long-lived class, here.** In degree 1 on `Z` (positions), a long-lived loop is a ring of designs around an unsampled
   region: the death scale is, in the alpha complex, the circumradius of the Delaunay triangle that finally fills it, the
   radius of the largest empty circle the ring encloses; the instance verifies the location: the circumcentre of the killing
   triangle lies inside the planted unsampled disk in both cases (`instance.md`). Degree 0 classes are gaps between
   components; degree 2 classes are voids in `(Z, s log V)`. None of this says the region is infeasible; it says no design
   has been measured there (Section "Hole against white space" in `readout.md`).
5. **Stability and noise.** Persistence diagrams of Vietoris-Rips complexes satisfy `d_b(dgm(Rips(X)), dgm(Rips(Y))) <= 2 d_GH(X, Y)`
   for finite metric spaces and, per Chazal, de Silva and Oudot, for all totally bounded ones (read: arXiv 1207.3885, the
   introduction; DOI of the published version 10.1007/s10711-013-9937-z). Applied to a refit: if a refit moves each design's
   chart point by at most `e`, then `d_GH <= e` and the bottleneck distance of the Rips diagrams is at most `2e`. The instance
   checks this on the case (largest row change 0.066, bound 0.133, observed bottleneck 0.040;
   `instance.md`). Separating a long-lived class from topological noise statistically is the subject of Fasy et al.
   (*Confidence sets for persistence diagrams*, Ann. Stat. 42(6):2301-2339 (2014), DOI 10.1214/14-AOS1252; abstract read:
   "separate topological signal from topological noise"); the instance uses a cruder device, a hole-free null (below), and
   does not claim the confidence-set property.
6. **Sampling guarantees.** Niyogi, Smale and Weinberger (DOI 10.1007/s00454-008-9053-2, record: *Finding the homology of
   submanifolds with high confidence from random samples*) and Chazal, Cohen-Steiner and Lieutier (DOI
   10.1007/s00454-009-9144-8, record: *A sampling theory for compact sets in Euclidean space*) give conditions under which a
   sample recovers the topology of a shape. Both are about recovering the homology of the shape the points came from; the
   hole question here is about the space the points do **not** cover. They tell what a dense enough sample would show, not
   what a sparse one's loop means, so they are used only as background and nothing is claimed from them.

## Persistent homology for sampled shapes and for design spaces, as found

Search done 2026-11-14 (web, standard mode, three queries; the closest results opened).

| Source | Read | What it is, and its distance from this spike |
|---|---|---|
| Li, Dasarathy, Ramamurthy and Berisha, *Finding the homology of decision boundaries with active learning*, NeurIPS 33 (2020), arXiv:2011.09645 (`arxiv.org/abs/2011.09645`) | abstract | Active selection of points to label so that the homology of a classifier's decision boundary is recovered with fewer samples. The nearest published relative of "sample to settle a topological question". It samples near the boundary to **recover** a known kind of topology, not to fill unsampled regions of a design space |
| Hamada and Goto, *Data-driven analysis of Pareto set topology*, GECCO 2018, DOI 10.1145/3205455.3205613, arXiv:1804.07179 | abstract | Estimates from an evolutionary algorithm's population whether the true Pareto set may be a topological simplex. The abstract does not mention persistent homology; it is topology of the **Pareto set** for judging coverage by a decomposition-based method, not holes in the interior of an attainable set |
| Kii et al., *Data-driven topology design with persistent homology for enhancing population diversity*, arXiv:2410.14496 | title (arXiv page) | Persistent homology inside an evolutionary design method for diversity of the population; a use of diagrams in selection. Not read beyond the title; no claim is taken from it |
| Zheng et al., *Active phase discovery in heterogeneous catalysis via topology-guided sampling and machine learning*, Nat. Commun. 16 (2025), DOI 10.1038/s41467-025-57824-4 | record | Its title pairs topology-guided sampling with a search of a physical space; the publisher page was not reachable, so no claim is taken from it |

Not found, in the searches above: a source that uses the classes of a persistence diagram as an objective to be improved by
choosing the next design in an engineering design space, scored beside the level of a surrogate. This is a statement about my
search, not about the literature: three queries and the results' abstracts do not establish absence. For the purposes of the
spike the direction is **not** claimed to be new; it is claimed to be well-posed (`readout.md`) and, in its geometry, buildable
from the pieces above.

Also read, for the standard comparison: Johnson, Moore and Ylvisaker (*Minimax and maximin distance designs*, J. Stat. Plan.
Inference 26:131-148 (1990), DOI 10.1016/0378-3758(90)90122-B, record), the fill-distance objectives of space-filling
design, and Jones, Schonlau and Welch (*Efficient global optimization of expensive black-box functions*, J. Global Optim.
13:455-492 (1998), DOI 10.1023/A:1008306431147, record), the acquisition-function template for trading exploration against
exploitation. They are what a topological measure of white space should be compared with in a build: a minimax design
reduces the largest empty ball anywhere, the topological measure counts only empty balls that are enclosed.

Overviews, record only: Carlsson, *Topology and data*, Bull. AMS 46(2):255-308 (2009), DOI 10.1090/S0273-0979-09-01249-X;
Otter et al., *A roadmap for the computation of persistent homology*, EPJ Data Sci. 6:17 (2017), DOI
10.1140/epjds/s13688-017-0109-5 (abstract read, arXiv:1506.08903: it surveys theory and computational methods and the software);
Chazal and Michel, *An introduction to topological data analysis*, Front. Artif. Intell. 4 (2021), DOI 10.3389/frai.2021.667963 (abstract read, arXiv:1710.04019).

## The tools

Installed in a scratch environment outside the repository (Python 3.12, `uv venv` and `uv run --with`; `pyproject.toml`
and `uv.lock` unchanged). Versions are those resolved on 2026-11-14.

| Tool | Version | Licence (source read) | What it computes | Notes from use |
|---|---|---|---|---|
| GUDHI (`gudhi`) | 3.13.0 | MIT; the Delaunay/alpha complex module is "MIT (GPL v3)", requires CGAL, and the Euclidean witness complexes likewise; the Rips complex module is MIT (`gudhi.inria.fr/licensing/` and the module list at `gudhi.inria.fr/python/latest/`, read 2026-11-14) | Simplex trees; Rips, alpha, witness, Čech complexes; persistence with the pairing of each class to its death simplex (`persistence_pairs`); bottleneck and Wasserstein distances | Gives the killing simplex, hence the circumcentre, which the instance needs. Any package that depended on the alpha module would carry a GPL v3 dependency; the package is MIT. A build would have to choose between the Rips route (MIT) and a separate Delaunay computation (scipy, BSD) |
| Ripser (`ripser`, ripser.py) | 0.6.15 | MIT (`github.com/scikit-tda/ripser.py`, LICENSE.txt, read) | Vietoris-Rips persistence to any degree, from points or a distance matrix, with greedy-permutation landmarks (`n_perm`) | Fast and simple. Gives the diagrams but no killing simplices, so no location of a hole. Rips scale is the edge length (a diameter): its numbers run near twice the alpha complex's radii (instance: 0.678 against 0.379 for the larger of the two planted loops) |
| persim (`persim`) | 0.4.1 | MIT (LICENSE.txt, read) | Bottleneck and Wasserstein distances, persistence images and landscapes for diagrams from ripser | Used for the refit check |
| giotto-tda (`giotto-tda`) | 0.6.2 | GNU AGPL v3 (the LICENSE file at `github.com/giotto-ai/giotto-tda`, read; the company L2F SA offers other terms on request) | scikit-learn-compatible transformers for diagrams (Rips, alpha, cubical, landscapes, images, amplitudes), pipelines (Tauzin et al., JMLR 22(39):1-6 (2021), `jmlr.org/papers/v22/20-325.html`, abstract read) | The only one of the four with a scikit-learn interface, and the only one under a licence the package cannot depend on (AGPL against MIT). It failed to build from source in the scratch environment (CMake missing) and installed from a binary wheel; not used for the instance |

Choice for a build: the diagrams and the killing simplices from GUDHI (the alpha module in an optional extra, if a GPL v3
dependency is accepted there) or from ripser plus scipy's Delaunay triangulation (MIT/BSD, no GPL), with persim for
distances. giotto-tda is not a candidate dependency. This is an option for the supervisor, not a recommendation (`readout.md`).

## What the literature establishes, and what it only suggests

Established (read as stated above):

- Persistence diagrams of Rips complexes are stable under changes of the point set in Gromov-Hausdorff distance, with the
  constant 2 (Chazal, de Silva, Oudot; the instance checks it numerically on a refit).
- A nonzero map of relative persistent homology of two Rips complexes is a sufficient condition for coverage (de Silva and
  Ghrist, Theorem 3.4), under their assumptions and with a fence at the boundary.
- A diagram can be filtered for noise by a statistical construction (Fasy et al., abstract).
- Persistent homology and active selection of samples have been combined to recover the homology of a decision boundary (Li et al.).

Only suggested (by the work above, not shown by it; this is where the future work lies):

- That the classes of a diagram of a **design** table are a useful measure of white space; the instance shows it on a planted
  table, where the answer is known, and finds nothing on the case's table (`instance.md`).
- That a sampling rule built on the killing simplices improves a search compared with a space-filling rule or an acquisition
  function; nothing here compares them.
- That the chart's metric is the right one for this; `objects-and-distances.md` gives the reasons and the instance shows the
  sensitivity to the level weight.

## His interests, as the repositories show them (a source of intuitions only; not cited, not favoured)

`knowledgecomplex` (last commit 2026-05-15) is a library of typed simplicial complexes with validated boundaries
(vertices, edges, faces with types and ontology-checked boundary closure); `knowledge-complex-analysis-tools` builds GUDHI
simplex trees, checks Betti numbers and boundary consistency, and does Hodge-style analysis (a `hodge_demo` notebook). Read
as intuitions: he thinks in typed complexes where the boundary is checked, in Betti numbers as invariants, and in the
Hodge picture of a class as a harmonic representative. Three things in this spike echo that and are marked as echoes, not
derived from it: a hole's boundary as a checked object (the fence, and the infeasible region as part of the boundary); type
as the dominant term of a K-term fit (a typed complex over the chart); a representative of a class as its location. The
readout does not rest on any of them.
