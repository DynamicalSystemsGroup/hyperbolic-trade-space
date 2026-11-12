"""Appendix G.2: what the paper took from where, from the reading pass of its attributions.

``reading_pass.yaml`` holds the fifty-six rows of the reading pass
(``work-packages/WP10-reading-pass.md``, read-only here): the sentence as it was read, the key, the
place read, the verdict and the reason, each verbatim, plus what the paper now does with the
sentence (``status`` and ``now``). The file is the record and is made from the Markdown table by
``uv run python paper/generate_reading_pass.py`` (which keeps the ``status`` and ``now`` already in
it); a test compares the two. The table of the appendix shows only what a reader needs to check a
citation: what we say, the source, the place in it. The record's verdict and reason are not shown.
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


REMOVED = (4, 14, 15)
"""Rows whose citation the paper no longer makes (their ``now`` says so): nothing is taken from the
source for a sentence, so the table has no row for them; the record keeps them."""
SAID = {10: "Scalarization, for example the weighting method, finds Pareto-optimal solutions."}
"""Rows whose ``now`` quotes the wording that was cut: the row gives the sentence as the paper now
says it (the record's ``now`` of that row, stated plainly)."""
_URL = re.compile(r"https?://[^\s,;)]*[^\s,;).]")


def _left(text: str, width: int, small: bool = False) -> str:
    """A cell of running text: left aligned, wrapping inside a minimum width (long URLs break)."""
    size = ";font-size:0.85em" if small else ""
    return (
        f'<div style="text-align:left;overflow-wrap:anywhere;min-width:{width}em{size}">'
        f"{text}</div>"
    )


def _plain(text: str) -> str:
    """Escaped text that keeps the single space at either end (so a link beside it stays apart)."""
    return (" " if text[:1].isspace() else "") + _esc(text) + (" " if text[-1:].isspace() else "")


def _place(read: str) -> str:
    """The place read, as the record gives it, with each web address a link."""
    out, last = [], 0
    for m in _URL.finditer(read):
        out += [_plain(read[last : m.start()]), f'<a href="{m.group()}">{m.group()}</a>']
        last = m.end()
    return "".join(out) + _plain(read[last:])


def citing_rows(rs=None) -> list[dict]:
    """One row per citing sentence still in the paper: what we say, the source, where in it.

    A sentence the record gives as ``(same sentence)`` is the previous row's. Where the sentence
    was reworded after the reading, the paper no longer says the sentence read, so the row gives
    what the paper now says (``now``). Where the place read is given as ``above``, it is the same
    source's earlier place.
    """
    rs = rows() if rs is None else rs
    out, sentence, places = [], "", {}
    for r in rs:
        if not r["sentence"].startswith("(same"):
            sentence = r["sentence"]
        place = r["read"]
        if "above" in place and r["key"] in places:
            place = places[r["key"]]
        places.setdefault(r["key"], place)
        if r["n"] in REMOVED:
            continue
        say = SAID.get(r["n"], sentence if r["status"] in ("kept", "supervisor") else r["now"])
        out.append({"n": r["n"], "say": say, "key": r["key"], "place": place})
    return out


def reading_pass_table() -> Md:
    """What the paper took from where: the sentence, the source, the place in it.

    Returns
    -------
    Md
        One row per citing sentence still in the paper, for the reader to check against the source.
    """
    return Md(
        md_table(
            ["What we say", "Source", "Where in it"],
            [
                [
                    _left(_esc(r["say"]), 18),
                    cite([r["key"]], "../#"),
                    _left(_place(r["place"]), 18, small=True),
                ]
                for r in citing_rows()
            ],
        )
    )


if __name__ == "__main__":
    convert()
    print(f"wrote {SOURCE} ({len(rows())} rows)", file=sys.stderr)
