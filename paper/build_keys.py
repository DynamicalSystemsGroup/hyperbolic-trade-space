"""Write the paper's key manifest, ``paper/paper-keys.json``, from the two notebooks (spec 2.6).

    uv run python paper/build_keys.py                 # write the manifest
    uv run python paper/build_keys.py --check         # exit 1 if the committed file differs
    uv run python paper/build_keys.py --check --xref paper/_build/html/myst.xref.json

A key is a label the paper defines: a MyST directive's ``:label:`` line or a ``(key)=`` target in a
markdown cell of ``paper.ipynb`` (route ``paper/``) or ``supporting_material.ipynb`` (route
``paper/supporting-material/``). The docs cite the paper through these keys and read only the
manifest, never a notebook. The manifest is canonical: ``{"schema": 1, "keys": {...}}``, keys
sorted, two-space indent, one trailing newline, so the copy published with a pin compares equal
byte for byte. ``--check`` writes nothing and prints the keys added, removed or moved; ``--xref``
also checks each key is an identifier on the page its route names in the built paper. Exit 0
holds, 1 a difference or a miss, 2 a key defined in two pages or a usage error.

>>> print(render({"thm-kkt": "paper/", "appendix-e": "paper/supporting-material/"}), end="")
{
  "schema": 1,
  "keys": {
    "appendix-e": "paper/supporting-material/",
    "thm-kkt": "paper/"
  }
}
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parent
MANIFEST = "paper-keys.json"
SCHEMA = 1
# The notebook that defines a key, and the route of the page the paper's build gives it.
PAGES = {
    "paper.ipynb": "paper/",
    "supporting_material.ipynb": "paper/supporting-material/",
}
ROUTES = frozenset(PAGES.values())
KEY = re.compile(r"^[A-Za-z0-9_-]+$")
_LABEL_LINE = re.compile(r"^\s*:label:\s*([A-Za-z0-9_-]+)\s*$", re.M)
_TARGET_LINE = re.compile(r"^\(([A-Za-z0-9_-]+)\)=\s*$", re.M)


class DuplicateKey(ValueError):
    """A key is defined in two pages of the paper."""


def notebook_keys(paper_dir: Path = PAPER_DIR) -> dict[str, str]:
    """Map every key the notebooks define to the route of its page."""
    keys: dict[str, str] = {}
    for notebook, route in PAGES.items():
        cells = json.loads((Path(paper_dir) / notebook).read_text(encoding="utf-8"))["cells"]
        for cell in cells:
            if cell["cell_type"] != "markdown":
                continue
            source = "".join(cell["source"])
            for key in _LABEL_LINE.findall(source) + _TARGET_LINE.findall(source):
                if keys.get(key, route) != route:
                    raise DuplicateKey(f"paper key {key!r} is defined in two pages")
                keys[key] = route
    return keys


def render(keys: dict[str, str]) -> str:
    """The manifest's canonical text."""
    return json.dumps({"schema": SCHEMA, "keys": dict(sorted(keys.items()))}, indent=2) + "\n"


def manifest_problems(text: str) -> list[str]:
    """The rules of specification 4 the manifest's text breaks (empty when it holds)."""
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"not JSON ({exc})"]
    if not isinstance(doc, dict) or set(doc) != {"schema", "keys"}:
        return ["the top level must hold exactly `schema` and `keys`"]
    out = []
    if doc["schema"] != SCHEMA:
        out.append(f"schema is {doc['schema']!r}, must be {SCHEMA}")
    keys = doc["keys"]
    if not isinstance(keys, dict) or not keys:
        return [*out, "`keys` must be a non-empty object"]
    out += [f"key {k!r} is not [A-Za-z0-9_-]+" for k in keys if not KEY.match(k)]
    out += [
        f"key {k!r}: route {r!r} is not a paper page" for k, r in keys.items() if r not in ROUTES
    ]
    if list(keys) != sorted(keys):
        out.append("the keys are not sorted")
    if not out and text != render(keys):
        out.append("not in the canonical form (two-space indent, one trailing newline)")
    return out


def diff(old: dict[str, str], new: dict[str, str]) -> list[str]:
    lines = [f"added: {k} -> {new[k]}" for k in sorted(new.keys() - old.keys())]
    lines += [f"removed: {k} (was {old[k]})" for k in sorted(old.keys() - new.keys())]
    lines += [
        f"moved: {k} {old[k]} -> {new[k]}"
        for k in sorted(old.keys() & new.keys())
        if old[k] != new[k]
    ]
    return lines


def xref_misses(keys: dict[str, str], xref: Path, base_url: str = "") -> list[str]:
    """Each key that is not an identifier on the page its route names in ``myst.xref.json``."""
    refs = json.loads(xref.read_text(encoding="utf-8"))["references"]
    base = base_url.rstrip("/")
    built = {}
    for r in refs:
        if "identifier" in r:
            url = r["url"]
            if base and url.startswith(base):
                url = url[len(base) :]
            built[r["identifier"]] = url.rstrip("/")
    misses = []
    for key, route in sorted(keys.items()):
        page = "/" + route.removeprefix("paper/").rstrip("/")
        want = "" if page == "/" else page
        if built.get(key) != want:
            got = "absent" if key not in built else repr(built[key] or "/")
            misses.append(f"{key}: on {route} by the manifest, {got} in the built paper")
    return misses


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare, write nothing")
    ap.add_argument("--xref", type=Path, help="the built paper's myst.xref.json")
    ap.add_argument("--paper-dir", type=Path, default=PAPER_DIR, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    path = args.paper_dir / MANIFEST
    try:
        keys = notebook_keys(args.paper_dir)
    except DuplicateKey as exc:
        print(f"build_keys: {exc}", file=sys.stderr)
        return 2
    status = 0
    if args.check:
        committed = path.read_text(encoding="utf-8") if path.is_file() else ""
        if committed != render(keys):
            status = 1
            old = json.loads(committed).get("keys", {}) if committed.strip() else {}
            print(f"build_keys: {path.name} differs from the notebooks' labels")
            for line in diff(old, keys) or ["the form differs (run without --check)"]:
                print(f"  {line}")
    else:
        path.write_text(render(keys), encoding="utf-8")
        print(f"build_keys: {path.name} written ({len(keys)} keys)")
    if args.xref is not None:
        if not args.xref.is_file():
            print(f"build_keys: {args.xref} not found", file=sys.stderr)
            return 2
        misses = xref_misses(keys, args.xref, os.environ.get("BASE_URL", ""))
        for miss in misses:
            print(f"build_keys: {miss}")
        status = status or (1 if misses else 0)
    if status == 0 and args.check:
        print(f"build_keys: ok ({len(keys)} keys)")
    return status


if __name__ == "__main__":
    sys.exit(main())
