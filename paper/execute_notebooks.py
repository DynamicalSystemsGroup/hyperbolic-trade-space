"""Execute the paper's notebooks from a clean kernel and write the outputs in place.

    uv run python paper/execute_notebooks.py [paper.ipynb supporting_material.ipynb]

The kernel is the project environment (``ipykernel`` of the ``paper`` group) and runs in ``paper/``.
Volatile metadata (execution timestamps) is removed so a re-run with unchanged data and seeds
leaves the files unchanged, and an output image repeated by the inline backend is kept once.
"""

from __future__ import annotations

import sys

import nbformat
from nbclient import NotebookClient
from paper_paths import PAPER

DEFAULT = ("paper.ipynb", "supporting_material.ipynb")


def _tidy(nb) -> None:
    """Drop timing metadata and repeated identical image outputs."""
    for cell in nb.cells:
        cell.metadata.pop("execution", None)
        if cell.cell_type != "code":
            continue
        seen, kept = set(), []
        for out in cell.outputs:
            png = out.get("data", {}).get("image/png") if out.output_type != "stream" else None
            if png is not None:
                if png in seen:
                    continue
                seen.add(png)
            kept.append(out)
        cell.outputs = kept


def execute(name: str, timeout: int = 1800) -> None:
    """Execute one notebook of ``paper/`` and write it back."""
    path = PAPER / name
    nb = nbformat.read(path, as_version=4)
    NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(PAPER)}},
        record_timing=False,
    ).execute()
    _tidy(nb)
    nbformat.write(nb, path)


if __name__ == "__main__":
    for nb_name in sys.argv[1:] or DEFAULT:
        execute(nb_name)
        print(f"executed {nb_name}")
