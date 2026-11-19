"""Support for the demo notebook: paths, constants and display helpers.

Importing this module puts ``paper/`` and ``scripts/`` of the repository on
``sys.path``.
"""

import re
import subprocess
import sys
from pathlib import Path

from IPython.display import Markdown, display

ROOT = next(
    p
    for p in [Path.cwd().resolve(), *Path.cwd().resolve().parents]
    if (p / "pyproject.toml").exists()
)
sys.path.insert(0, str(ROOT / "paper"))
sys.path.insert(0, str(ROOT / "scripts"))

MODEL = ROOT / "examples/adcs/model_v2/cubesat.sysml"
VIEWS = ROOT / "examples/adcs/model_v2/views"
FIGURES = ROOT / "paper/figures"


def _unref(text):
    """Remove work-package tags from a line of model text."""
    return re.sub(r"\s*\(WP\d+\)|;\s*[\d.]+,\s*WP\d+", "", text)


def say(sentence):
    """Show a generated sentence as Markdown, without its cross-references.

    Parameters
    ----------
    sentence : str or IPython.display.Markdown
        The sentence a findings function returned.
    """
    text = getattr(sentence, "data", sentence)
    text = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", text)
    text = re.sub(r"\s*\((?:[^()]*?)(?:Appendix [A-Z]\.\d+|Definition \d+)[^()]*\)", "", text)
    text = re.sub(
        r"(?<=\. )[^.]*(?:Theorem \d+|checked by a test of the repository)[^.]*\.\s*", "", text
    )
    text = re.sub(r"has a (\d+)-lemma", r"has \1 contending metrics", text)
    display(Markdown(text))


def excerpt(path, start, lines, skip=0):
    """Print `lines` lines of a file from the first line containing `start`.

    Parameters
    ----------
    path : path-like
        File to read.
    start : str
        Text that marks the first line.
    lines : int
        Number of lines to print.
    skip : int, default=0
        Lines to move past the marked line.
    """
    text = Path(path).read_text().splitlines()
    first = next(i for i, line in enumerate(text) if start in line) + skip
    print(_unref("\n".join(text[first : first + lines])))


def sections(path):
    """Print the numbered section headers of a SysML v2 file.

    Parameters
    ----------
    path : path-like
        The SysML v2 file.
    """
    for line in Path(path).read_text().splitlines():
        if re.match(r"\s+// \d\. ", line):
            print(_unref(line.strip()))


def draw(plantuml_text):
    """Draw PlantUML text with the PlantUML tool.

    Parameters
    ----------
    plantuml_text : str
        The PlantUML source.

    Returns
    -------
    str
        The drawing as SVG.
    """
    run = subprocess.run(
        ["plantuml", "-Djava.awt.headless=true", "-tsvg", "-pipe"],
        input=plantuml_text,
        capture_output=True,
        text=True,
        check=True,
    )
    return run.stdout
