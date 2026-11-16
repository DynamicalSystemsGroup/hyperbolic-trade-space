"""The supplement: tables of the record that the appendices cite, written from their generators.

    uv run python paper/generate_supplement.py           # write every file under paper/supplement/
    uv run python paper/generate_supplement.py --check   # exit 1 if a file is stale

Each file under ``paper/supplement/`` is a heading, one sentence naming the record it is made from
and the command that writes it, and the table a generator function returns; nothing in it is typed
per row. A test compares each file with its generator (``tests/test_paper.py``), so a file cannot
go stale silently.
"""

from __future__ import annotations

import sys
from collections.abc import Callable

import generate_reading_pass
from paper_paths import PAPER


def _metric_associations() -> str:
    import case
    import generate_model

    rest = list(case.CUBESAT.regimes)[1:]
    return (
        str(generate_model.metric_table(regimes=rest))
        + "\n\n"
        + str(generate_model.metric_associations(at_least=0.0))
    )


def _results(name: str) -> Callable[[], str]:
    def table() -> str:
        import generate_results

        return str(getattr(generate_results, name)())

    return table


SUPPLEMENT = PAPER / "supplement"
COMMAND = "uv run python paper/generate_supplement.py"

FILES: dict[str, tuple[str, str, Callable[[], str]]] = {
    "reading-pass.md": (
        "The reading pass: what the paper took from where",
        "One row per sentence of the paper that rests on a cited work: the sentence, the source "
        "and the place in it that was read, with the source's own link. The record is "
        "`paper/reading_pass.yaml`; the table is `generate_reading_pass.reading_pass_table`'s, "
        f"written by `{COMMAND}`.",
        lambda: str(generate_reading_pass.reading_pass_table(plain=True)),
    ),
    "metric-associations.md": (
        "The table of metrics: the baseline regime's first rows and every pair's association",
        "Appendix C.5 prints the primary regime's first rows and the pairs at |Spearman| 0.5 or "
        "above; this file holds the baseline regime's first rows and all the pairs of traded "
        "metrics over the feasible designs of both regimes. The tables are "
        "`generate_model.metric_table` and `generate_model.metric_associations`, read from the "
        f"data of record (`examples/adcs/data/v2/`) and written by `{COMMAND}`.",
        _metric_associations,
    ),
    "temperature-sweep.md": (
        "The K = 1 fit at each temperature of the sweep, both regimes",
        "The sweep behind the fit temperature of each regime; the paper's figure of the sweep "
        "draws the primary regime. The table is `generate_results.temperature_selection`, read "
        f"from the data of record and written by `{COMMAND}`.",
        _results("temperature_selection"),
    ),
    "refits-by-category.md": (
        "The K = 1 fit within each wheel class, both regimes",
        "The one-term fit refitted on the designs of each wheel class. The table is "
        "`generate_results.refits_by_category`, read from the data of record and written by "
        f"`{COMMAND}`.",
        _results("refits_by_category"),
    ),
}
"""File name -> (title, the sentence under it, the generator of its table)."""


def render(name: str) -> str:
    """The text of a supplement file: title, sentence, table, with a trailing newline."""
    title, sentence, table = FILES[name]
    return f"# {title}\n\n{sentence}\n\n{table()}\n"


def write_all(root=SUPPLEMENT) -> list[str]:
    """Write every file; return the names written."""
    root.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        (root / name).write_text(render(name), encoding="utf-8")
    return list(FILES)


def stale(root=SUPPLEMENT) -> list[str]:
    """The files that differ from their generator (missing files included)."""
    out = []
    for name in FILES:
        path = root / name
        if not path.is_file() or path.read_text(encoding="utf-8") != render(name):
            out.append(name)
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv == ["--check"]:
        bad = stale()
        for name in bad:
            print(f"stale: paper/supplement/{name} (run {COMMAND})", file=sys.stderr)
        return 1 if bad else 0
    for name in write_all():
        print(f"wrote paper/supplement/{name}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
