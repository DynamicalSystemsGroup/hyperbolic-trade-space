"""Regenerate the paper's generated text under a perturbation that mimics a platform difference.

    uv run python paper/paper_perturb.py OUT.json [--restarts SHIFT]

The thread counts of the maths libraries are taken from the environment (the caller sets
``OMP_NUM_THREADS`` and its relatives); ``--restarts SHIFT`` adds SHIFT to every estimator's
``random_state``, which permutes the order of the restarts and so the tie-sensitive choices among
equally good optima. The output maps the name of each generated table or sentence to its text, so
two runs can be compared: a name whose text moves prints a quantity that depends on the platform
(``tests/test_paper.py::test_generated_tables_do_not_move_under_platform_perturbation``).
"""

from __future__ import annotations

import json
import sys

import paper_paths  # noqa: F401  (puts the repository on sys.path)


def _shift_restarts(shift: int) -> None:
    from hyperbolic_trade_space import HyperbolicTradeSpace

    fit = HyperbolicTradeSpace.fit

    def shifted(self, *args, **kwargs):
        kept = self.random_state
        self.random_state = (0 if kept is None else kept) + shift
        try:
            return fit(self, *args, **kwargs)
        finally:
            self.random_state = kept

    HyperbolicTradeSpace.fit = shifted


def generated() -> dict[str, str]:
    """The text of every generated table and sentence that is computed from a fit."""
    import case
    import generate_findings as gf
    import generate_model
    import generate_results as gr

    out = {}
    for name in ("planted_recovery", "margin_reading", "pca_chain",
                 "stability", "temperature_selection", "k_diagnostics", "exponents_and_terms",
                 "regime_comparison", "sensitivity_variants", "refits_by_category",
                 "candidate_designs", "termination_records", "nondominated",
                 "propose_predict_check", "conditioning_diagnostic", "own_rows_refit"):  # fmt: skip
        out[f"D {name}"] = str(getattr(gr, name)())
    for name in ("configuration_space", "evaluation", "attribute_sources", "feasibility",
                 "conditioning", "metric_table", "datasets", "planted_example"):  # fmt: skip
        out[f"C {name}"] = str(getattr(generate_model, name)())
    study = case.load_study("primary")
    fits = case.k_fits(study)
    reg = case.fit_regressor(study)
    pc = case.predict_check(study, reg)
    out["sentence num-nondominated"] = str(gf.nondominated_sentence(study))
    out["sentence num-certificates"] = str(gf.certificate_sentence(fits))
    out["sentence num-margin"] = str(gf.margin_sentence(study, fits))
    out["sentence num-recovery"] = str(gf.recovery_sentence())
    out["sentence num-temperature"] = str(gf.temperature_sentence(study, fits[1]))
    out["sentence num-terms"] = str(gf.terms_sentence(study, fits))
    out["sentence num-regimes"] = str(gf.regime_sentence())
    out["sentence num-predict"] = str(gf.predict_check_sentence(pc, reg))
    out["sentence num-predict-reading"] = str(gf.predict_reading(pc, reg))
    out["sentence num-planted"] = str(gf.planted_sentence())
    decided = gf.decision(study, case.k_fits(study, (1, case.CASE_K)))
    out["sentence decision"] = str(gf.decision_sentence(decided))
    out["sentence decision-detail"] = str(gf.decision_detail_sentence(decided))
    out["sentence decision-baseline"] = str(gf.decision_baseline_sentence())
    out["D decision_table"] = str(gf.decision_table(decided))
    out["D decision_designs"] = str(gf.decision_designs_table(decided))
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    shift = int(args[args.index("--restarts") + 1]) if "--restarts" in args else 0
    if shift:
        _shift_restarts(shift)
    with open(args[0], "w", encoding="utf-8") as f:
        json.dump(generated(), f, indent=1)
