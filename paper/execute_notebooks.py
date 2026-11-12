"""Execute the paper's notebooks from a clean kernel and write the outputs in place.

    uv run python paper/execute_notebooks.py [paper.ipynb supporting_material.ipynb]

The kernel is the project environment (``ipykernel`` of the ``paper`` group) and runs in ``paper/``.
Volatile metadata (execution timestamps) is removed so a re-run with unchanged data and seeds
leaves the files unchanged, and an output image repeated by the inline backend is kept once.
"""

from __future__ import annotations

import os
import sys

import nbformat
from jupyter_client import KernelManager
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


def write_figure_files(nb) -> list[str]:
    """Write each ``fig-`` cell's image to ``figures/<cell id>.png``, which its caption links to.

    The page shows the output image; the link beside the caption opens the same image as a file of
    the built site. The three-pane schematic (``figures/figure1.py``) is not in the paper: the
    index page is its one consumer.
    """
    import base64

    written = []
    for cell in nb.cells:
        if cell.cell_type == "code" and cell.id.startswith("fig-"):
            for out in cell.outputs:
                png = out.get("data", {}).get("image/png")
                if png:
                    (PAPER / "figures" / f"{cell.id}.png").write_bytes(base64.b64decode(png))
                    written.append(cell.id)
                    break
    return written


def execute(name: str, timeout: int = 1800) -> None:
    """Execute one notebook of ``paper/`` and write it back."""
    path = PAPER / name
    nb = nbformat.read(path, as_version=4)
    # The kernel talks over unix sockets (``ipc``): the default TCP transport makes the kernel print
    # "[IPKernelApp] WARNING | Kernel is running over TCP without encryption" on every start, a
    # line about the connection and not about the notebook.
    # The kernel inherits the working directory, ``paper/`` (a ``resources`` path would make the
    # kernel's start fail over this transport).
    km = KernelManager(kernel_name="python3")
    km.transport = "ipc"
    here = os.getcwd()
    os.chdir(PAPER)
    try:
        NotebookClient(
            nb,
            km=km,
            timeout=timeout,
            kernel_name="python3",
            record_timing=False,
        ).execute()
    finally:
        os.chdir(here)
        if km.has_kernel:
            km.shutdown_kernel(now=False)
    _tidy(nb)
    nbformat.write(nb, path)
    if name == "paper.ipynb":
        write_figure_files(nb)


if __name__ == "__main__":
    for nb_name in sys.argv[1:] or DEFAULT:
        execute(nb_name)
        print(f"executed {nb_name}")
