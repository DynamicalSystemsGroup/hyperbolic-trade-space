# Note: references verified so far (seed for WP5)

Verified 2026-11-07 by web search of bibliographic records. WP5 must resolve each DOI/URL again
when building `docs/references.bib`; nothing goes into the .bib from memory.

- Hoburg, W., Kirschen, P., Abbeel, P. (2016). "Data fitting with geometric-programming-compatible
  softmax functions." *Optimization and Engineering* 17(4), 897–918. doi:10.1007/s11081-016-9332-3.
  Author manuscript on MIT DSpace (handle 1721.1/105753). Software: GPfit (gpfit.readthedocs.io).
- Magnani, A., Boyd, S. (2009). "Convex piecewise-linear fitting." *Optimization and Engineering*
  10, 1–17. PDF: https://web.stanford.edu/~boyd/papers/cvx_pwl_fit.html.
- Boyd, S., Kim, S.-J., Vandenberghe, L., Hassibi, A. (2007). "A tutorial on geometric programming."
  *Optimization and Engineering* 8, 67–127. doi:10.1007/s11081-007-9001-7.
- Aigner, D., Lovell, C. A. K., Schmidt, P. (1977). "Formulation and estimation of stochastic
  frontier production function models." *Journal of Econometrics* 6(1), 21–37.
- Andersen, P., Petersen, N. C. (1993). "A procedure for ranking efficient units in data envelopment
  analysis." *Management Science* 39(10), 1261–1264. doi:10.1287/mnsc.39.10.1261.
- Färe, R., Grosskopf, S., Norris, M., Zhang, Z. (1994). "Productivity growth, technical progress,
  and efficiency change in industrialized countries." *American Economic Review* 84(1), 66–83.
- Föllmer, H. "Entropic risk measures on Wiener space" (notes), definition (1/β) log E[exp(−βX)],
  limits mean (β→0) and essential supremum (β→∞). https://www2.mathematik.hu-berlin.de/~foellmer/papers/ERMWS.pdf
- Tall, D. O. (2008). "The Transition to Formal Thinking in Mathematics." *Mathematics Education
  Research Journal* 20(2), 5–24. ERIC EJ820231.
- Tall, D. O. (2013). *How Humans Learn to Think Mathematically: Exploring the Three Worlds of
  Mathematics.* Cambridge University Press. ISBN 9781107035706.

Candidates named in the plan but **not yet verified** (WP5 to verify or drop): Aigner & Chu 1968;
Charnes, Cooper & Rhodes 1978 (DEA); Ahmadi-Javid (entropic value at risk); Aitchison 1983
(compositional PCA) and Aitchison 1986; Egozcue et al. 2003 (ILR); Rockafellar, *Convex Analysis*
§13 (support functions); Boyd & Vandenberghe, *Convex Optimization* §5.2 (LP duality); Schölkopf et
al. (kernel PCA); Chami et al. 2021 (HoroPCA, for disambiguation); Zitzler & Thiele 1999
(hypervolume); Ross, Hastings et al. 2004 (multi-attribute tradespace exploration); Buchberger 1990;
Artigue 2002; Sfard 1991.

Added for WP9 (2026-11-08, Crossref DOI records): Candès, E. J., Wakin, M. B., Boyd, S. P. (2008).
"Enhancing sparsity by reweighted ℓ1 minimization." *J. Fourier Anal. Appl.* 14(5–6), 877–905.
doi:10.1007/s00041-008-9045-x. Miettinen, K. (1999). *Nonlinear Multiobjective Optimization.*
Springer US (Kluwer print 1999). doi:10.1007/978-1-4615-5563-6. Ehrgott, M. (2005). *Multicriteria
Optimization*, 2nd ed. Springer. doi:10.1007/3-540-27659-9 (author from Open Library; Crossref lists none).

## Added for WP10 (2026-11-08, implementer P2)

Method: each DOI was fetched from the Crossref API (authors, title, container, volume, issue, pages,
date, abstract where present) and resolved through `curl -sIL https://doi.org/<doi>`. The doi.org
redirect reached the publisher landing page for all fourteen DOIs; Wiley, INFORMS, Royal Society, ASME
and AIAA answered an automated GET with 403 after the redirect (the DOI is live, the page is not
machine-readable), Springer, Elsevier (Spero 2014, Allen 1997, Dyson 2001) and Cambridge answered
200 on the redirect target. Full texts were not read; abstracts were read from Crossref where it has
them (not for Allen 1997, Dyson 2001, Spero 2014, Ross 2010).

- Fifteen state-of-practice sources (`WP10-decisions.md`, "adopt as listed"): `hirshorn2017nasa`
  (NTRS page, no DOI), `baker2012survey` (nasa.gov PDF read, page one), `chilli2026decision`
  (SEBoK page), `smith2007ameliorating`, `parnell2021system`, `madni2018model`, `henderson2021value`,
  `ross2005tradespace`, `ross2010revisiting`, `stump2009visual`, `spero2014tradespace`,
  `howard1988decision`, `keeney1993decisions`, `jolliffe2016principal`, `parnell2016trade` (Wiley
  page, ISBN 9781119237532; no Crossref DOI exists for the book).
- DEA: `banker1984some`, `allen1997weights`, `dyson2001pitfalls`.
- `zargham2026incose` (10.1002/iis2.70203, INCOSE International Symposium 36(1), 1501-1514, 2026).
- Already present, unchanged: `miettinen1999nonlinear` (Crossref dates the Springer record 1998, the
  Kluwer print 1999), `ehrgott2005multicriteria`, `candes2008enhancing`.
- Notes: the Crossref title for Ross and Hastings 2005 begins with the session code "11.4.3"; the entry
  drops it. Baker and Whalen carries no date in the PDF; 2012 rests on the workshop listing found by
  search (the nasa.gov workshop page itself now returns 404). The NASA handbook's section 6.8 and the
  SEBoK article body were not read.

## Added for the WP10 Amendment 2 follow-up (2026-11-09, I10 re-based on LICQ)

- Nocedal, J., Wright, S. J. (2006). *Numerical Optimization*, 2nd ed. Springer.
  doi:10.1007/978-0-387-40065-5 (key `nocedal2006numerical`). Crossref record read (authors, title,
  Springer New York, 2006); the doi.org redirect reached the Springer landing page. The text of
  Chapter 12 was read in a course copy (pages.mtu.edu, `NocedalAndWright/Chpt12.pdf`, 51 pages):
  Definition 12.4 is the linear independence constraint qualification (LICQ: the gradients of the
  active constraints at the point are linearly independent; the active set is Definition 12.1) and
  Theorem 12.1 (First-Order Necessary Conditions) states that at a local solution with continuously
  differentiable f and c_i and LICQ, there is a multiplier vector satisfying the KKT conditions.
  Numbers confirmed against the chapter text; the copy is not the publisher's, so the author may
  wish to check the page numbers in the printed second edition. Ledger entry I10 cites these two
  numbers; the Boyd and Vandenberghe 5.5.3 reference stays only as a convex-case remark.
