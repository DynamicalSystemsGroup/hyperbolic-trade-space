"""The decision section's number: a design's tension at the picked design, in attribute units.

    MPLCONFIGDIR=$(mktemp -d) uv run --frozen python work-packages/WP42-rounds/spike/section9.py

Reads the case's fits (as ``case_run.py``), takes the design ``decision()`` calls "between" (the
pick between the operator's pointing error and the sponsor's fleet cost), and writes the numbers
and the drafted sentence to ``section9.json``. Nothing in the sentence is typed: every figure comes
from the prototype.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import prototype as P  # noqa: E402
from case_run import ROOT, load  # noqa: E402  (puts examples/adcs on the path)

sys.path.insert(0, str(ROOT / "paper"))
from generate_findings import decision  # noqa: E402

ARCSEC_PER_DEG = 3600.0


def main():
    study, fits = load()
    dec = decision(study, fits)
    pick = dec.picks["between"]
    idx = int(np.flatnonzero(study.feasible["design_id"].to_numpy() == pick["design_id"])[0])
    names = study.names
    pe, fc, uc = (names.index(n) for n in ("pointing error", "fleet cost", "unit cost"))
    alpha, a = P.conditioning_of(study)
    est = fits[2].estimator
    raw = study.feasible[list(study.spec.attributes)].to_numpy(float)[idx]
    des = P.design_tensions(est, study.M[idx], raw, alpha, a)
    x = raw + a
    out = {"design_id": str(pick["design_id"]), "term": des["term"] + 1,
           "margin_to_other_term": des["margin"], "pairs": {}}  # fmt: skip
    for label, j in (("fleet cost", fc), ("unit cost", uc)):
        row = {}
        for q in range(len(est.exponents_)):
            w = est.exponents_[q]
            t_attr = P.attribute_tension(w, alpha, x, pe, j)  # USD per degree
            elas_attr = -(w[pe] * alpha[pe]) / (w[j] * alpha[j])  # percent per percent
            row[f"term {q + 1}"] = {
                "usd_per_arcsec": t_attr / ARCSEC_PER_DEG,
                "percent_per_percent_in_attributes": elas_attr,
                "T_metrics": float(P.term_tension_matrix(w, np.log(study.M[idx]))[pe, j]),
            }
        out["pairs"][label] = row
    t = out["term"]
    f = out["pairs"]["fleet cost"][f"term {t}"]
    o = out["pairs"]["fleet cost"][f"term {3 - t}"]
    pe_arcsec = raw[pe] * ARCSEC_PER_DEG
    cfg = f"{int(pick['fleet_size'])} {pick['wheel_class']}-wheel, {pick['st_grade']}-tracker"
    sentence = (
        f"At the picked fleet ({cfg} satellites) the surface's tension between the operator's "
        f"pointing error and the sponsor's fleet cost is {f['usd_per_arcsec'] / 1e6:+.1f} M USD "
        f"per arcsecond: along the surface, one percent more pointing error goes with "
        f"{abs(f['percent_per_percent_in_attributes']):.1f} percent less fleet cost. It is a rate "
        f"at that design with the other metrics held, not the price of the better tracker, and "
        f"on the other term of the fit it is {o['usd_per_arcsec'] / 1e6:+.1f} M USD per arcsecond."
    )
    out["sentence"] = sentence
    out["pointing_error_arcsec"] = pe_arcsec
    (HERE / "section9.json").write_text(json.dumps(out, indent=1))
    print(sentence)
    print(json.dumps(out["pairs"], indent=1))


if __name__ == "__main__":
    main()
