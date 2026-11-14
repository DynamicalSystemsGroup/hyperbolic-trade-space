# WP50 — Scope of work: topological holes in the chart by persistent homology (research spike; future direction)

| | |
|---|---|
| **Status** | DRAFT, a research spike. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; the readout under `work-packages/WP50-rounds/` |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP50-decisions.md` |
| **Acceptance record** | The supervisor's acceptance of the readout, quoted verbatim |

## Purpose

The supervisor's direction (`WP50-decisions.md`): the word hole is reserved for future work in which the piecewise-affine
chart and the sampled designs give distances, the distances give simplicial complexes, and persistent homology finds
topological holes, which emerge naturally under strategic sampling and need a definition that goes beyond the envelope
method. The spike is research only: it establishes a clear direction, using this method's coordinate system and data
points together with topological data analysis. It writes no code into the package and no claim into the paper.

## Goals

- G1. **The objects, named:** what a point is (a design in the chart: position Z and level log V, Section 4), what
  distance between two points is a candidate for (the chart's Euclidean metric per term, a metric across the seam of two
  terms, a distance in the metrics' log units), and what each choice does to a hole; why the piecewise-affine chart is
  the natural place, stated against doing it in the raw metrics.
- G2. **The construction, read,** from the point of departure he named (21:35): Ghrist's barcodes paper, the
  topological-landmarks work (landmark and witness complexes) and the sensor-network coverage work by persistent
  homology, with the thesis that the learned coordinate system decides what is near what; then Vietoris–Rips, witness
  and alpha complexes on those distances, persistent homology in degrees 0, 1 and 2, the persistence diagram and
  barcode and what a long-lived class means here; the tools (at least GUDHI, Ripser,
  giotto-tda) with licences and what each computes; the literature on persistent homology for sampled surfaces and for
  design spaces, each source resolved.
- G3. **Hole against white space:** the envelope method's white space (the fit speaks, the data do not) and a topological
  hole (a class that persists) are two objects; where they coincide, where they do not, with a small worked instance on
  the cubesat chart of record or a planted table (a figure of the diagram is allowed as a readout image, not a paper
  figure).
- G4. **Strategic sampling, sketched, with two objectives kept apart** (his direction of 22:15): advancing the frontier
  (the envelope's level, which the fit measures) and filling white space, measurable once holes are classes of a
  persistence diagram (their number and persistence, and how a new sample changes them); what the measure of a hole
  is, how a proposed sample is scored against it, how that score sits beside the level in the propose-predict-check
  loop of Section 7 so a sampling rule can trade the two, how such a rule makes holes emerge, and what a definition of
  hole that survives refits must satisfy.
- G5. **The boundary:** what 0.1 may say (a future-work sentence at most, drafted for him), what it may not, and what a
  later release would build, with its first package named.

## Non-goals

- Any change to `src/`, `paper/`, `docs/`, `glossary.yaml` or the interface contract; defining hole in 0.1.
- A theorem; the spike reports what the literature establishes and what it only suggests, cited.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP50-rounds/spike/objects-and-distances.md` | G1 |
| D-2 | `work-packages/WP50-rounds/spike/construction-and-tools.md` (sources with dates read; the tools' licences) | G2 |
| D-3 | `work-packages/WP50-rounds/spike/instance/` (a script and its persistence diagram on the chart of record or a planted table, reproducible with `uv run`, dependencies added to a scratch environment and not to `pyproject.toml`) and `instance.md` | G3 |
| D-4 | `work-packages/WP50-rounds/spike/readout.md`: hole against white space, the sampling sketch, the boundary, the drafted future-work sentence, plain options for the first package of the later release | G3, G4, G5 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every source cited with a resolved DOI or stable URL and the date read; quotations short and attributed | the notes; the assistant resolves three at random |
| R-2 | No file outside `work-packages/WP50-rounds/` changes; `pyproject.toml` and `uv.lock` unchanged | `git diff --stat`, `uv lock --check` |
| R-3 | The instance's script reruns to the same diagram (the assistant reruns it) | the rerun |
| R-4 | The readout keeps the two objects apart by name throughout: white space (0.1's word) and hole (reserved) | the file; `scripts/check_vocabulary.py` on the readout |
| R-5 | Options plain, no steering order, no recommended tag | the file |

## Definition of good

The supervisor can state the future direction in one paragraph with the objects named, pick the later release's first
package, and accept or decline a future-work sentence for 0.1.

## Definition of good enough

- D-1 to D-4 delivered; R-1 to R-5 pass; the readout ends with the three-part boundary.

## Definition of done

Good enough met, no open item remaining, and the supervisor's acceptance of the readout recorded verbatim in
`WP50-decisions.md`.

## Agent's defaults

- The unit reads his `knowledgecomplex` repository and any earlier notes of his on topological data analysis it can
  reach as a source of his interests and intuitions only; the readout does not favour or cite his work over the
  literature *(default)*.
- One research agent on Sonnet with web access, in a worktree, with a scratch environment for the TDA library (GUDHI or
  Ripser, whichever installs clean under uv in the scratch environment) *(default)*.
- The instance uses the K = 2 chart of record of the cubesat case (position and level per design) and one planted table
  with a region left unsampled on purpose, so a hole is known to exist in one and not assumed in the other *(default)*.
- The readout lands after WP42's build and before the v0.1 pull request, so the future-work sentence can be decided with
  the paper in view; the work itself is beyond 0.2 unless he places it *(default)*.

## Open decisions (for the supervisor)

None. The direction of 20:35 settles the aim (research only, a clear future direction) and the reservation of the word.
