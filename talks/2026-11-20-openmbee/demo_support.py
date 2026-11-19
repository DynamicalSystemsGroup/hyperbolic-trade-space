"""Support for the demo notebook: paths, constants and display helpers.

Importing this module puts ``paper/`` and ``scripts/`` of the repository on
``sys.path``.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import Markdown, display
from matplotlib.lines import Line2D

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
    text = re.sub(r"\s*The tension matrix states.*?reads [-\u2212]?\d+\.\d+\.", "", text)
    text = text.replace("energy differential", "level").replace("energy level", "level")
    text = re.sub(r" \(its [^()]*not the case's\)", "", text)
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


def ledger_table():
    """Return the latest ledger entry of each data file of the model's data.

    Returns
    -------
    pandas.DataFrame
        One row per output file: run id, evidence kind, rows, file and time.
    """
    path = ROOT / "examples/adcs/experiments/ledger/ledger.jsonl"
    ledger = pd.DataFrame([json.loads(line) for line in path.read_text().splitlines()])
    latest = ledger[ledger["output_path"].str.contains("data/v2/")]
    latest = latest.drop_duplicates("output_path", keep="last")
    latest = latest.assign(id=latest["id"].str.replace(r"@\d+", "", regex=True))
    columns = ["id", "evidence_kind", "output_rows", "output_path", "time_utc"]
    return latest[columns].reset_index(drop=True)


def predict_check_figure(study, regressor):
    """Draw the predict-and-check figure, with both chart axes labelled.

    Parameters
    ----------
    study : Study
        The case study.
    regressor : TradeSpaceRegressor
        The fitted regressor.
    """
    import case

    case.predict_check_figure(study, regressor)
    fig = plt.gcf()
    fig.axes[1].set_ylabel("Z2")
    designs, proposals, measured = fig.axes[0].collections
    edges = designs.get_edgecolor()
    ring = edges[edges[:, 3] > 0][0]
    dot = designs.get_facecolor()[0]
    handles = [
        Line2D([], [], ls="", marker="o", mfc=dot, mec="none", ms=designs.get_sizes()[0] ** 0.5),
        Line2D(
            [], [], ls="", marker="o", mfc=dot, mec=ring, mew=0.8, ms=designs.get_sizes()[0] ** 0.5
        ),
        Line2D(
            [],
            [],
            ls="",
            marker="o",
            mfc="none",
            mec=proposals.get_edgecolor()[0],
            ms=proposals.get_sizes()[0] ** 0.5,
        ),
        Line2D(
            [],
            [],
            ls="",
            marker="D",
            mfc=measured.get_facecolor()[0],
            mec=measured.get_edgecolor()[0],
            ms=measured.get_sizes()[0] ** 0.5,
        ),
        Line2D([], [], ls=""),
    ]
    labels = [
        "a design",
        "a design near the fitted reference surface",
        "a proposal, where the regressor predicted it",
        "the same proposal, where it was measured",
        "the number beside them is the proposal's number",
    ]
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.legend(handles, labels, loc="lower center", ncol=2, fontsize=11, frameon=False)


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


# The closed loop: the pipeline of paper/figures/pipeline.py, its style and stage glosses, with the
# search fed back. One input port on evaluate (the sample c and the proposal c' meet at a junction);
# one wire for w, beta out of identify (a take-off point branches it to regress).
_INK, _SUB, _EDGE, _FILL = "#111827", "#374151", "#374151", "#f3f4f6"


def _box(left, top, name, gloss, dashed=False):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    c = left + 70
    return (
        f'<rect x="{left}" y="{top}" width="140" height="60" rx="8" fill="{_FILL}" '
        f'stroke="{_EDGE}" stroke-width="1.5"{dash}/>'
        f'<text x="{c}" y="{top + 36}" text-anchor="middle" font-size="16" font-weight="600" '
        f'fill="{_INK}">{name}</text>'
        f'<text x="{c}" y="{top + 80}" text-anchor="middle" font-size="12" '
        f'fill="{_SUB}">{gloss}</text>'
    )


def _wire(*points):
    d = " ".join(("M" if i == 0 else "L") + f" {x} {y}" for i, (x, y) in enumerate(points))
    return (
        f'<path d="{d}" fill="none" stroke="{_EDGE}" stroke-width="1.5" marker-end="url(#arrow)"/>'
    )


def _label(x, y, symbol, gloss_y, gloss):
    return (
        f'<text x="{x}" y="{y}" text-anchor="middle" font-size="16" font-style="italic" '
        f'fill="{_INK}">{symbol}</text>'
        f'<text x="{x}" y="{gloss_y}" text-anchor="middle" font-size="12" '
        f'fill="{_SUB}">{gloss}</text>'
    )


def loop_figure():
    """Draw the pipeline closed into a loop by the regressor and a search.

    Returns
    -------
    str
        The drawing as SVG.
    """
    width, height, top, bot = 1040, 350, 40, 220
    y, by, jx, tx = top + 30, bot + 30, 110, 830
    parts = [
        _box(150, top, "evaluate", "a black box"),
        _box(360, top, "condition", "feature engineering"),
        _box(590, top, "identify", "fit the surface"),
        _box(860, top, "analyse", "decision analysis"),
        _box(760, bot, "regress", "c ↦ chart point"),
        _box(500, bot, "search", "maximize V̂", dashed=True),
        _wire((14, y), (jx - 8, y)),
        _label(55, y - 12, "c", top + 80, "configurations"),
        f'<circle cx="{jx}" cy="{y}" r="6" fill="#ffffff" stroke="{_EDGE}" stroke-width="1.5"/>',
        _wire((jx + 6, y), (148, y)),
        _wire((292, y), (358, y)),
        _label(325, y - 12, "a", top + 80, "attributes"),
        _wire((502, y), (588, y)),
        _label(545, y - 12, "m", top + 80, "metrics"),
        _wire((732, y), (858, y)),
        _label(770, y - 12, "w, β", top + 80, "the trade-offs"),
        f'<circle cx="{tx}" cy="{y}" r="3.5" fill="{_EDGE}"/>',
        _wire((tx, y), (tx, bot - 2)),
        _wire((758, by), (642, by)),
        _label(700, by - 12, "V̂", bot + 80, "predicted V"),
        _wire((498, by), (jx, by), (jx, y + 8)),
        _label(300, by - 12, "c\u2032", bot + 80, "a proposal"),
        f'<rect x="14" y="{height - 25}" width="26" height="14" rx="3" fill="{_FILL}" '
        f'stroke="{_EDGE}" stroke-width="1.2" stroke-dasharray="4 3"/>',
        f'<text x="48" y="{height - 14}" font-size="12" fill="{_SUB}">'
        "dashed: not yet a function of the package (case code today)</text>",
    ]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" style="max-width:{width}px;height:auto" '
        'font-family="Helvetica, Arial, sans-serif">'
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>'
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
        f'markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{_EDGE}"/>'
        "</marker></defs>" + "".join(parts) + "</svg>\n"
    )


def choosing_k_table(study, fits):
    """Tabulate what each added term buys: slack, its drop and the thinnest term.

    The mean slack is read at the temperature of the one-term fit, so the rows
    compare like with like; the thinnest term's share is read at each fit's own
    temperature.

    Parameters
    ----------
    study : Study
        The case study.
    fits : dict of int to Fit
        One fit per number of terms K, as returned by ``case.k_fits``.

    Returns
    -------
    pandas.DataFrame
        Columns ``K``, ``mean slack``, ``drop`` and ``thinnest share, own tau``.
    """
    import case
    import numpy as np

    _, k_terms, _ = case._lib()
    tau, rows, previous = fits[1].tau, [], None
    for k, fit in fits.items():
        est = k_terms.fit_k(study.M, k, tau, study.spec.seed)
        slack = float(est.mean_slack_)
        rows.append(
            {
                "K": k,
                "mean slack": slack,
                "drop": np.nan if previous is None else previous - slack,
                "thinnest share, own tau": (
                    float(np.min(fit.estimator.term_share_)) if k > 1 else 1.0
                ),
            }
        )
        previous = slack
    return pd.DataFrame(rows)
