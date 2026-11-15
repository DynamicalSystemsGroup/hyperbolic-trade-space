"""The paper's pipeline figure: evaluate, condition, identify, analyse.

Four stages in a row, one fill. Between them travel the objects the package names: configurations
``c``, attributes ``a``, metrics ``m`` and the fitted weights and exponents ``w, β``. Under each
stage and each object stands a one-line gloss. The drawing is a plain SVG assembled from the
string constants below (``STAGES``, ``FLOWS``), so a stage name or a gloss is edited here and the
file is written again.

Run ``uv run python paper/figures/pipeline.py`` to write ``fig-pipeline.svg`` beside it.
"""

from __future__ import annotations

import pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "fig-pipeline.svg"

WIDTH, HEIGHT = 900, 220
INK, SUB, EDGE, FILL = "#111827", "#374151", "#374151", "#f3f4f6"
# (left edge, centre, name, gloss) of each stage box.
STAGES = (
    (70, 140, "evaluate", "a black box"),
    (280, 350, "condition", "feature engineering"),
    (510, 580, "identify", "fit the surface"),
    (720, 790, "analyse", "decision analysis"),
)
# (arrow start, arrow end, label x, symbol, gloss) of each object in transit.
FLOWS = (
    (14, 68, 40, "c", "configurations"),
    (212, 278, 245, "a", "attributes"),
    (422, 508, 465, "m", "metrics"),
    (652, 718, 685, "w, β", "the trade-offs"),
)

HEAD = f"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" font-family="Helvetica, Arial, sans-serif">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{EDGE}"/>
    </marker>
  </defs>


  <!-- four stages, one fill -->
"""
STAGE = """\
  <rect x="{left}" y="90" width="140" height="60" rx="8" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>
  <text x="{centre}" y="126" text-anchor="middle" font-size="16" font-weight="600" fill="{ink}">{name}</text>
"""
FLOW = """\
  <line x1="{x1}" y1="120" x2="{x2}" y2="120" stroke="{edge}" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="{x}" y="108" text-anchor="middle" font-size="16" font-style="italic" fill="{ink}">{symbol}</text>
"""
GLOSS = """\
  <text x="{x}" y="170" text-anchor="middle" font-size="12" fill="{sub}">{text}</text>
"""


def svg() -> str:
    """Return the figure as SVG text.

    Returns
    -------
    str
        The drawing, ending in a newline.
    """
    k = {"fill": FILL, "edge": EDGE, "ink": INK, "sub": SUB}
    out = HEAD
    out += "\n".join(
        STAGE.format(left=left, centre=centre, name=name, **k) for left, centre, name, _ in STAGES
    )
    out += "\n  <!-- data between stages -->\n"
    out += "\n".join(
        FLOW.format(x1=x1, x2=x2, x=x, symbol=symbol, **k) for x1, x2, x, symbol, _ in FLOWS
    )
    out += "\n  <!-- one line under each: what the stage is -->\n"
    glosses = sorted(
        [(x, text) for _, _, x, _, text in FLOWS] + [(c, text) for _, c, _, text in STAGES]
    )
    out += "".join(GLOSS.format(x=x, text=text, **k) for x, text in glosses)
    return out + "</svg>\n"


def main() -> None:
    """Write ``fig-pipeline.svg`` beside this file."""
    OUT.write_text(svg())
    print("wrote", OUT)


if __name__ == "__main__":
    main()
