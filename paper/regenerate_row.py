"""Regenerate one row of Appendix F.4: the cell that makes one figure or table of the paper.

    uv run python paper/regenerate_row.py ROW [--out FILE]

``ROW`` is the first column of the table in Appendix F.4 (``fig-tau-sweep``, ``tab-D-stability``,
...). The script runs the cells of the row's notebook that the row needs and prints the table (as
Markdown) or saves the figure (to ``FILE``, default ``ROW.png`` in the current directory); it
writes nothing in the repository. A row of the supporting material needs only the setup cell; a
row of the paper needs the cells before it, which build the study and the fits it shares.
Compare the printed table with the committed output of that cell, or the figure with the file in
``paper/_build`` after a site build.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

import nbformat
from paper_paths import PAPER  # importing it puts the repository on sys.path

NOTEBOOKS = ("paper.ipynb", "supporting_material.ipynb")


def _locate(row: str):
    """The notebook and the cells to run for ``row``: the cells before it, then the row's own."""
    for name in NOTEBOOKS:
        nb = nbformat.read(PAPER / name, as_version=4)
        cells = [c for c in nb.cells if c.cell_type == "code"]
        ids = [c.id for c in cells]
        if row in ids:
            upto = cells[: ids.index(row) + 1]
            if name == "supporting_material.ipynb":  # its cells are independent calls
                upto = [c for c in upto if c.id.startswith("setup") or c.id == row]
            return name, upto
    raise SystemExit(f"{row!r} is not a figure or table cell of {' or '.join(NOTEBOOKS)}")


def run(row: str):
    """Run the cells for ``row`` in one namespace and return the value of the row's own cell."""
    _, cells = _locate(row)
    space: dict = {"__name__": "__row__"}
    value = None
    for cell in cells:
        tree = ast.parse(cell.source)
        last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
        # the code is the paper's own committed cells, never input from outside
        exec(compile(tree, f"<{cell.id}>", "exec"), space)
        if last is not None:
            expr = ast.Expression(last.value)
            value = eval(compile(expr, f"<{cell.id}>", "eval"), space)
    return value


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="regenerate_row", description=__doc__.splitlines()[0])
    parser.add_argument("row", help="a row of Appendix F.4, such as fig-tau-sweep")
    parser.add_argument("--out", type=Path, default=None, help="where to save a figure")
    args = parser.parse_args(argv)
    value = run(args.row)
    if hasattr(value, "savefig"):
        out = args.out or Path(f"{args.row}.png")
        value.savefig(out, dpi=150)
        print(f"saved {out}")
    else:
        print(str(value))
    return 0


if __name__ == "__main__":
    sys.exit(main())
