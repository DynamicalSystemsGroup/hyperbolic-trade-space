"""The public surface of ``tradespace`` as a record, for the versioning rule (GOVERNANCE.md).

    uv run python scripts/api_surface.py                                   # print the surface
    uv run python scripts/api_surface.py --write tests/data/api_surface.json
    uv run python scripts/api_surface.py --check [tests/data/api_surface.json]

The surface is read from the package by import and ``inspect``: each public module (the package and
every submodule whose name has no leading underscore), each name in the module's ``__all__`` (or,
for a module without one, each public name the module defines), for a class its own public methods
with their signatures, for a function its signature, for anything else its type and value.
``__version__`` is left out: the version is what the rule classifies, not part of the surface.
Methods a class inherits are its base's surface, not the package's, so they are left out too.

The JSON is sorted by key, so two runs on the same package produce the same bytes. ``--write``
writes it; ``--check`` compares the record with the live surface and exits 1 with each differing
entry named. ``tests/test_api_surface.py`` holds the committed record equal to the package, and
``scripts/release_checks.py version-kind`` compares the record with the previous release's.
"""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import pkgutil
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / "tests" / "data" / "api_surface.json"
PACKAGE = "tradespace"
EXCLUDED_NAMES = {"__version__"}


def _signature(obj: object) -> str | None:
    try:
        return str(inspect.signature(obj))
    except (TypeError, ValueError):
        return None


def _entry(obj: object) -> dict:
    """One name's record: a class with its own public methods, a function, or a value.

    >>> class A:
    ...     def m(self, x, y=1):
    ...         pass
    >>> _entry(A)["methods"]
    {'m': '(self, x, y=1)'}
    >>> _entry(len)["kind"], _entry(3.0)
    ('function', {'kind': 'float', 'value': '3.0'})
    """
    if inspect.isclass(obj):
        methods = {
            name: _signature(member)
            for name, member in vars(obj).items()
            if not name.startswith("_") and callable(member)
        }
        return {"kind": "class", "signature": _signature(obj), "methods": methods}
    if callable(obj):
        return {"kind": "function", "signature": _signature(obj)}
    return {"kind": type(obj).__name__, "value": repr(obj)}


def _public_names(module: ModuleType) -> list[str]:
    """``__all__``, or the public names the module itself defines."""
    if hasattr(module, "__all__"):
        names = list(module.__all__)
    else:
        names = [
            name
            for name, obj in vars(module).items()
            if not name.startswith("_")
            and not isinstance(obj, ModuleType)
            and getattr(obj, "__module__", module.__name__) == module.__name__
        ]
    return sorted(set(names) - EXCLUDED_NAMES)


def public_modules(package: str = PACKAGE) -> list[str]:
    """The package and each submodule whose name has no leading underscore, sorted."""
    root = importlib.import_module(package)
    names = [package]
    for info in pkgutil.walk_packages(root.__path__, prefix=package + "."):
        if not any(part.startswith("_") for part in info.name.split(".")):
            names.append(info.name)
    return sorted(names)


def surface(package: str = PACKAGE) -> dict[str, dict[str, dict]]:
    """``{module: {name: entry}}`` for the package's public surface."""
    out = {}
    for module_name in public_modules(package):
        module = importlib.import_module(module_name)
        out[module_name] = {name: _entry(getattr(module, name)) for name in _public_names(module)}
    return out


def flatten(record: dict) -> dict[str, str]:
    """``module.name`` and ``module.name.method`` to a one-line description.

    >>> flatten({"m": {"f": {"kind": "function", "signature": "(a)"}}})
    {'m.f': 'function (a)'}
    """
    flat = {}
    for module, names in record.items():
        for name, entry in names.items():
            key = f"{module}.{name}"
            if entry["kind"] == "class":
                flat[key] = f"class {entry.get('signature')}"
                for method, signature in entry.get("methods", {}).items():
                    flat[f"{key}.{method}"] = f"method {signature}"
            elif entry["kind"] == "function":
                flat[key] = f"function {entry.get('signature')}"
            else:
                flat[key] = f"{entry['kind']} {entry.get('value')}"
    return flat


def differences(old: dict, new: dict) -> list[str]:
    """One line per entry added, removed or changed between two records.

    >>> a = {"m": {"f": {"kind": "function", "signature": "(a)"}}}
    >>> b = {"m": {"f": {"kind": "function", "signature": "(a, b)"}, "g": a["m"]["f"]}}
    >>> differences(a, b)
    ['added: m.g', 'changed: m.f: function (a) -> function (a, b)']
    """
    before, after = flatten(old), flatten(new)
    lines = [f"added: {k}" for k in sorted(set(after) - set(before))]
    lines += [f"removed: {k}" for k in sorted(set(before) - set(after))]
    lines += [
        f"changed: {k}: {before[k]} -> {after[k]}"
        for k in sorted(set(before) & set(after))
        if before[k] != after[k]
    ]
    return lines


def dumps(record: dict) -> str:
    return json.dumps(record, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", default=PACKAGE)
    parser.add_argument("--write", type=Path, metavar="PATH", help="write the record here")
    parser.add_argument(
        "--check",
        type=Path,
        nargs="?",
        const=SNAPSHOT,
        metavar="PATH",
        help=f"compare the record (default {SNAPSHOT.relative_to(ROOT)}) with the live surface",
    )
    args = parser.parse_args(argv)
    live = surface(args.package)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(dumps(live), encoding="utf-8")
        print(f"wrote {args.write}")
        return 0
    if args.check:
        if not args.check.is_file():
            print(f"refused: {args.check} does not exist; run --write first", file=sys.stderr)
            return 1
        recorded = json.loads(args.check.read_text(encoding="utf-8"))
        problems = differences(recorded, live)
        for line in problems:
            print(f"refused: {line}", file=sys.stderr)
        return 1 if problems else 0
    print(dumps(live), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
