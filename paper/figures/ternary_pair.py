"""The paper's Figure 9 (WP28, the supervisor's two-panel ternary): two triples of the cubesat.

Each panel is the package's ``plot_ternary`` on three of the eight metrics of the primary regime,
fitted with two terms: a design sits at its shares of the three metrics' total, a numbered marker
is a term's exponent vector, a region is where that term is the largest, and the thin lines are
equal invariant value at a fixed total. The drawing is ``case.ternary_pair_figure`` (the docs page
draws the same figure from the same function); the designs are one neutral colour, as in the other
figures (``work-packages/WP19-decisions.md``). Case data of record.

Run ``uv run python paper/figures/ternary_pair.py`` to write ``fig-ternary-pair.png`` beside it.
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent


def _case():
    root = HERE.parent.parent
    for p in (root / "src", root / "examples" / "adcs"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import case

    return case


def ternary_pair_paper_figure():
    """The two-panel ternary of :func:`case.ternary_pair_figure`, in the light scheme."""
    case = _case()
    with plt.rc_context({"figure.dpi": 100, "savefig.dpi": 100}):
        return case.ternary_pair_figure(case.ternary_pair_fits())


def main() -> None:
    """Write ``fig-ternary-pair.png`` beside this file."""
    fig = ternary_pair_paper_figure()
    fig.savefig(
        HERE / "fig-ternary-pair.png", dpi=100, bbox_inches="tight", metadata={"Software": None}
    )
    plt.close(fig)
    print("wrote", HERE / "fig-ternary-pair.png")


if __name__ == "__main__":
    main()
