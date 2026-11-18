"""Refuse a release whose tag and package version disagree, or whose version is not a valid release.

The release workflow calls this before it builds. A tag ``v0.1.0`` is accepted only if
``pyproject.toml`` says ``version = "0.1.0"``; a dispatch from ``dev`` has no tag and needs only a
valid version.

    uv run python scripts/check_release_version.py              # print the version
    uv run python scripts/check_release_version.py --tag v0.1.0 # exit 1 unless the tag matches
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# PEP 440 release with an optional pre-release (a, b, rc) or dev segment: 0.1.0, 0.1.0rc1.
VERSION = re.compile(r"^\d+\.\d+\.\d+((a|b|rc)\d+)?(\.dev\d+)?$")


def package_version(root: Path = ROOT) -> str:
    return tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"][
        "version"
    ]


def check(version: str, tag: str | None) -> str | None:
    """Return the reason to refuse, or None.

    >>> check("0.1.0", "v0.1.0") is None
    True
    >>> check("0.1.0", "v0.1.1")
    "tag 'v0.1.1' does not match the package version '0.1.0' (expected 'v0.1.0')"
    >>> check("0.1", None)
    "version '0.1' is not major.minor.patch with an optional a, b, rc or dev suffix"
    """
    if not VERSION.match(version):
        return (
            f"version {version!r} is not major.minor.patch with an optional a, b, rc or dev suffix"
        )
    if tag is not None and tag != f"v{version}":
        return f"tag {tag!r} does not match the package version {version!r} (expected 'v{version}')"
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tag", help="the tag being released, for example v0.1.0")
    parser.add_argument("--root", type=Path, default=ROOT, help="the tree to read (tests use this)")
    args = parser.parse_args(argv)
    version = package_version(args.root)
    problem = check(version, args.tag or None)
    if problem:
        print(f"refused: {problem}", file=sys.stderr)
        return 1
    print(version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
