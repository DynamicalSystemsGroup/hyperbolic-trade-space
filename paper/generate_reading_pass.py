"""Appendix G.2: what the cited works say, from the reading pass of the paper's attributions.

``reading_pass.yaml`` holds the fifty-six rows of the reading pass
(``work-packages/WP10-reading-pass.md``, read-only here): the sentence as it was read, the key, what
was read, the verdict and the reason, each verbatim, plus what the paper now does with the sentence
(``status`` and ``now``). The table of the appendix is compiled from the file; the file is made from
the Markdown table by ``uv run python paper/generate_reading_pass.py`` (which keeps the
``status`` and ``now`` already in the file), and a test compares the two.
"""

from __future__ import annotations

import re
import sys

import yaml
from generate_prior_art import cite
from generate_proofs import _esc
from paper_common import Md, md_table
from paper_paths import PAPER, ROOT

SOURCE = PAPER / "reading_pass.yaml"
MARKDOWN = ROOT / "work-packages" / "WP10-reading-pass.md"
VERDICTS = (
    "supported",
    "partly supported",
    "not found",
    "not accessible",
    "accessible (own work)",
)
STATUS = {
    "kept": "kept as read",
    "reworded": "reworded to what was read",
    "confirm": "to be confirmed by the author",
    "supervisor": "listed for the supervisor, unchanged",
}
_ROW = re.compile(
    r"^\| (?P<n>\d+) \| (?P<sentence>.*?) \| `(?P<key>[^`]+)` \| (?P<read>.*?) \| "
    r"(?P<verdict>" + "|".join(re.escape(v) for v in VERDICTS) + r") \| (?P<why>.*) \|$"
)
FIELDS = ("n", "sentence", "key", "read", "verdict", "why")


def markdown_rows(path=MARKDOWN) -> list[dict]:
    """The rows of the Markdown table of the reading pass, fields verbatim."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _ROW.match(line)
        if m:
            rows.append({k: (int(v) if k == "n" else v) for k, v in m.groupdict().items()})
    return rows


def rows(path=SOURCE) -> list[dict]:
    """The rows of ``reading_pass.yaml``."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))["rows"]


def convert(md=MARKDOWN, out=SOURCE) -> None:
    """Write ``reading_pass.yaml`` from the Markdown table, keeping the annotations there."""
    old = {r["n"]: r for r in rows(out)} if out.exists() else {}
    merged = []
    for r in markdown_rows(md):
        prev = old.get(r["n"], {})
        merged.append({**r, "status": prev.get("status", ""), "now": prev.get("now", "")})
    head = (
        "# Rows of the reading pass (work-packages/WP10-reading-pass.md), verbatim, with what the\n"
        "# paper now does with each sentence. Made by paper/generate_reading_pass.py.\n"
    )
    out.write_text(
        head + yaml.safe_dump({"rows": merged}, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def _left(text: str, width: int, small: bool = False) -> str:
    """A cell of running text: left aligned, wrapping inside a minimum width (long URLs break)."""
    size = ";font-size:0.85em" if small else ""
    return (
        f'<div style="text-align:left;overflow-wrap:anywhere;min-width:{width}em{size}">'
        f"{text}</div>"
    )


def reading_pass_table() -> Md:
    """The reading pass as a table: sentence, key, what was read, verdict and what the paper does.

    Returns
    -------
    Md
        One row per sentence and key, with the counts of each verdict above the table.
    """
    rs = rows()
    counts = ", ".join(
        f"{v} {sum(r['verdict'] == v for r in rs)}"
        for v in VERDICTS
        if any(r["verdict"] == v for r in rs)
    )
    table = md_table(
        ["#", "Sentence", "Key", "What was read", "Verdict", "In the paper"],
        [
            [
                r["n"],
                _left(_esc(r["sentence"]), 15),
                cite([r["key"]], "../#"),
                _left(_esc(r["read"]), 18, small=True),
                r["verdict"],
                _left(f"{STATUS[r['status']]}. {_esc(r['now'])}", 16),
            ]
            for r in rs
        ],
    )
    return Md(f"{len(rs)} rows ({counts}).\n\n{table}")


if __name__ == "__main__":
    convert()
    print(f"wrote {SOURCE} ({len(rows())} rows)", file=sys.stderr)
