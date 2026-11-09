"""Path setup for the paper's cells and generators.

Importing this module puts the repository root, ``src``, ``examples/adcs`` (the case module) and
``paper`` on ``sys.path``, so a notebook cell in ``paper/`` can ``import case`` and the generators
can be imported by the tests and by the cells alike.
"""

import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parent
ROOT = PAPER.parent

for _p in (ROOT, ROOT / "src", ROOT / "examples" / "adcs", PAPER):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def inline_figures() -> None:
    """Show matplotlib figures inline in a notebook cell, whatever the case modules selected.

    ``k_terms`` (imported by the case module) selects the non-interactive Agg backend, which
    leaves a returned ``Figure`` without an image output. Importing it first and then switching to
    the inline backend makes the cell's last expression display. A no-op outside IPython.
    """
    try:
        from IPython import get_ipython
    except ImportError:  # pragma: no cover
        return
    shell = get_ipython()
    if shell is None:
        return
    import k_terms  # noqa: F401  (selects Agg on import; must come before the switch)

    shell.run_line_magic("matplotlib", "inline")
