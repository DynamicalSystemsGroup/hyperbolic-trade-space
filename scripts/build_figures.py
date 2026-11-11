"""Build the docsite's figures by running the code blocks that sit above them.

    uv run python scripts/build_figures.py [--out DIR]

A docsite page embeds a figure as the pair ``![alt](.../NAME-light.png#only-light)`` and
``![alt](.../NAME-dark.png#only-dark)``. The figure is what the last matplotlib figure holds after
the ``{.runnable}`` code block directly above that pair has run, with the page's earlier blocks
run first in one namespace (the same rule the tests use). Nothing is copied from the paper and no
data are hand-drawn: each image is the package's own plotting function on the block's seeded
synthetic data, or the case module on the committed data. Every page's blocks run once per colour
scheme (the light pass and the dark pass differ only in the matplotlib style and the frontier
colour), so the two images of a figure show the same picture. Default output is
``docs/generated/figures/`` (git-ignored, inside the docsite's ``docs_dir``).

The paper's static figures (those drawn by a module of ``paper/figures/`` rather than by a cell of a
notebook) are regenerated in place by the same run: see :data:`PAPER_FIGURES`. ``--docs-only``
skips them.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DEFAULT_OUT = DOCS / "generated" / "figures"

MAX_FIGURES = 8
BLOCK = re.compile(r"^```python \{\.runnable\}\n(.*?)^```", re.M | re.S)
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s#]*?)([\w-]+)-light\.png#only-light\)")
ALT = re.compile(r"!\[([^\]]*)\]\([^)\s#]*?([\w-]+)-light\.png#only-light\)")
_SIZE = (7.0, 4.2)  # inches; width fits a 46 rem column at 100 dpi
_DPI = 110
# Figures drawn wider than the column are redrawn at this width in inches (labels keep their size).
RESIZE = {"adcs-tensions": 6.3}
# The paper's static figures: the modules of ``paper/figures/`` whose ``main()`` writes the image
# beside the module (WP19's candidates: the n-lemma, Figure 3 and Figure 4 redrawn without term
# colouring; the last two read the case's committed data and are regenerated with WP23's). The
# index page's three-pane figure has its own command (``uv run python paper/figures/figure1.py``)
# and is not rebuilt here: its SVG's ids vary from run to run.
PAPER_FIGURES = ("nlemma", "planes", "chart_level", "ternary_pair")
# The model's two views, drawn by the model's own projection (PlantUML, a system tool) and committed
# beside the model; the paper takes byte-identical copies (published path in paper/figures: source).
MODEL_VIEWS = {
    "fig-assembly-view.png": "examples/adcs/model_v2/views/assembly_view.png",
    "fig-behavioural-view.png": "examples/adcs/model_v2/views/behavioural_view.png",
}

# What differs between the schemes: the style that is applied, and the colour of "black". The
# dark scheme leaves ``text.color`` alone: the heatmap's cell values are drawn in it, on cells that
# are light and dark, and keep the legibility they have in the light scheme.
SCHEMES = {
    "light": {"rc": {}, "frontier": "black", "text": "#1c1c1c"},
    "dark": {
        "rc": {
            "axes.labelcolor": "#e8e6e1",
            "axes.edgecolor": "#a5a19a",
            "xtick.color": "#e8e6e1",
            "ytick.color": "#e8e6e1",
            "axes.titlecolor": "#e8e6e1",
            "legend.labelcolor": "#e8e6e1",
        },
        "frontier": "white",
        "text": "#e8e6e1",
    },
}


def page_blocks(path):
    """The ``{.runnable}`` blocks of a page, in order."""
    return BLOCK.findall(Path(path).read_text())


def page_figures(path):
    """``[(block_index, name)]``: each figure and the index of the block directly above it."""
    text = Path(path).read_text()
    events = [(m.start(), "block", None) for m in BLOCK.finditer(text)]
    events += [(m.start(), "figure", m.group(2)) for m in IMAGE.finditer(text)]
    figures, seen = [], -1
    for _, kind, name in sorted(events):
        if kind == "block":
            seen += 1
        else:
            if seen < 0:
                raise ValueError(f"{path}: figure {name} has no code block above it")
            figures.append((seen, name))
    return figures


def figure_alts(path):
    """``{name: alt text}`` of the page's figures; the alt text is also written into each image."""
    return {m.group(2): m.group(1) for m in ALT.finditer(Path(path).read_text())}


def pages_with_figures(docs=DOCS):
    """The hand-written pages that embed a figure, as sorted paths."""
    return sorted(
        p
        for p in Path(docs).rglob("*.md")
        if p.relative_to(docs).parts[0] not in ("generated", "superpowers") and page_figures(p)
    )


def _apply(scheme):
    import matplotlib.pyplot as plt

    from hyperbolic_trade_space import plotting

    spec = SCHEMES[scheme]
    plotting.FRONTIER_COLOR = spec["frontier"]
    return plt.rc_context(
        {"figure.figsize": _SIZE, "figure.dpi": _DPI, "savefig.dpi": _DPI, **spec["rc"]}
    )


def build_page(path, out, schemes=("light", "dark")):
    """Run a page's blocks once per scheme and save each figure; returns the written paths."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from hyperbolic_trade_space import plotting

    path, out = Path(path), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    blocks, wanted, alts = page_blocks(path), {}, figure_alts(path)
    for index, name in page_figures(path):
        wanted.setdefault(index, []).append(name)
    written = []
    cwd, sys_path = os.getcwd(), list(sys.path)
    original = plotting.FRONTIER_COLOR
    os.chdir(ROOT)  # the case page imports examples/adcs by a path relative to the repository
    try:
        for scheme in schemes:
            namespace = {"__name__": "__docs_block__"}
            with _apply(scheme):
                for i, block in enumerate(blocks):
                    with contextlib.redirect_stdout(io.StringIO()):  # the blocks print results
                        exec(compile(block, f"{path.name}[block {i + 1}]", "exec"), namespace)
                    for name in wanted.get(i, []):
                        fig = plt.gcf()
                        if name in RESIZE:
                            w, h = fig.get_size_inches()
                            fig.set_size_inches(RESIZE[name], h * RESIZE[name] / w)
                            fig.tight_layout()
                        target = out / f"{name}-{scheme}.png"
                        fig.savefig(
                            target,
                            bbox_inches="tight",
                            transparent=True,
                            metadata={"Software": None, "Description": alts.get(name)},
                        )
                        written.append(target)
                        plt.close("all")
            plt.close("all")
    finally:
        plotting.FRONTIER_COLOR = original
        os.chdir(cwd)
        sys.path[:] = sys_path
    return written


def build(out=DEFAULT_OUT, docs=DOCS):
    """Build every figure of the docsite into ``out``; returns the written paths."""
    written = []
    for page in pages_with_figures(docs):
        written += build_page(page, out)
    names = {p.name.rsplit("-", 1)[0] for p in written}
    if len(names) > MAX_FIGURES:
        raise ValueError(f"{len(names)} figures; the docsite carries at most {MAX_FIGURES}")
    return written


def build_paper(modules=PAPER_FIGURES):
    """Regenerate the paper's static figures beside their modules in ``paper/figures/``."""
    import importlib

    import matplotlib

    matplotlib.use("Agg")
    sys_path = list(sys.path)
    sys.path[:0] = [str(ROOT / "paper"), str(ROOT / "src")]
    try:
        for name in modules:
            with contextlib.redirect_stdout(io.StringIO()):
                importlib.import_module(f"figures.{name}").main()
    finally:
        sys.path[:] = sys_path
    for name, source in MODEL_VIEWS.items():
        (ROOT / "paper" / "figures" / name).write_bytes((ROOT / source).read_bytes())
    return [*modules, *MODEL_VIEWS]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    parser.add_argument("--docs-only", action="store_true", help="skip the paper's static figures")
    args = parser.parse_args(argv)
    try:
        written = build(args.out)
        paper = [] if args.docs_only else build_paper()
    except Exception as exc:
        print(f"build_figures: FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"built {len(written)} images in {args.out}")
    if paper:
        print(f"regenerated the paper's static figures: {', '.join(paper)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
