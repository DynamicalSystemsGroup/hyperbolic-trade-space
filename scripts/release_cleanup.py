"""Remove what a failed release left behind: the draft GitHub release and the tag.

    uv run --no-project python scripts/release_cleanup.py --tag TAG [--repo OWNER/NAME]
        [--run-id ID] [--dry-run] [--json] [--report FILE]

``TAG`` is ``v<version>`` (the software) or a paper tag (``paper-working-YYYYMMDD[-n]``,
``paper-submitted-<venue>``, ``paper-revision-<venue>-r<n>``). The script reads the tag's ref and
release with ``gh`` and, for a ``v`` tag, PyPI's record of the version (read only; a paper tag never
asks PyPI). Then:

- no tag and no release: nothing to remove (exit 0);
- a published release (not a draft): nothing removed, it is public and archived (exit 3);
- a ``v`` tag whose version PyPI holds: tag and draft kept, PyPI's files name this version (exit 3);
- otherwise: the draft release is deleted, then the tag (exit 0; ``--dry-run`` removes nothing);
- PyPI or ``gh`` unreadable, or a deletion fails: stops there and says what was removed (exit 1);
- bad arguments or a tag of no known shape: nothing (exit 2).

Standard library plus ``gh`` on ``PATH``; run by release.yml's and paper.yml's ``on-failure`` jobs
and by hand. ``--json`` prints the report as JSON; ``--report`` also writes it as Markdown.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).resolve().parent
PYPI_JSON = "https://pypi.org/pypi/tradespace/{version}/json"


def _version_pattern() -> re.Pattern:
    spec = importlib.util.spec_from_file_location(
        "_check_release_version", HERE / "check_release_version.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.VERSION


VERSION = _version_pattern()
# The paper's tag shapes (specification 2.3); none starts with v.
PAPER_TAGS = (
    re.compile(r"^paper-working-(?P<date>\d{8})(?:-(?P<n>[2-9]|[1-9]\d+))?$"),
    re.compile(r"^paper-submitted-(?P<venue>[a-z0-9]+(?:-[a-z0-9]+)*)$"),
    re.compile(r"^paper-revision-(?P<venue>[a-z0-9]+(?:-[a-z0-9]+)*)-r(?P<round>[1-9]\d*)$"),
)

# gh(args) -> (exit code, stdout, stderr)
Gh = Callable[[list[str]], tuple[int, str, str]]
# pypi(version) -> True (present) or False (absent); raises when PyPI cannot be read
PyPI = Callable[[str], bool]


class Unreadable(Exception):
    """A source the decision needs could not be read."""


def tag_kind(tag: str) -> str | None:
    """``software``, ``paper`` or None for a tag of no known shape.

    >>> tag_kind("v0.1.0"), tag_kind("paper-working-20261120-2")
    ('software', 'paper')
    >>> tag_kind("paper-submitted-ieee-tse"), tag_kind("paper-revision-ieee-tse-r2")
    ('paper', 'paper')
    >>> tag_kind("v0.1"), tag_kind("paper-working-2026"), tag_kind("0.1.0")
    (None, None, None)
    """
    if tag.startswith("v") and VERSION.match(tag[1:]):
        return "software"
    if any(p.match(tag) for p in PAPER_TAGS):
        return "paper"
    return None


def run_gh(args: list[str]) -> tuple[int, str, str]:
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def pypi_has(version: str) -> bool:
    try:
        with urllib.request.urlopen(PYPI_JSON.format(version=version), timeout=60):
            return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise Unreadable(f"PyPI answered {e.code} for {version}") from e
    except OSError as e:
        raise Unreadable(f"PyPI could not be read ({e})") from e


def _absent(stderr: str) -> bool:
    s = stderr.lower()
    return "404" in s or "not found" in s


def read_tag(gh: Gh, repo: str, tag: str) -> str | None:
    code, out, err = gh(["api", f"repos/{repo}/git/ref/tags/{tag}"])
    if code != 0:
        if _absent(err):
            return None
        raise Unreadable(f"gh could not read the tag ({err.strip() or code})")
    return json.loads(out)["object"]["sha"]


def read_release(gh: Gh, repo: str, tag: str) -> dict | None:
    code, out, err = gh(["release", "view", tag, "--repo", repo, "--json", "isDraft,assets"])
    if code != 0:
        if _absent(err):
            return None
        raise Unreadable(f"gh could not read the release ({err.strip() or code})")
    doc = json.loads(out)
    return {"draft": bool(doc["isDraft"]), "assets": len(doc.get("assets") or [])}


def resolve_repo(gh: Gh, env: dict) -> str:
    if env.get("GITHUB_REPOSITORY"):
        return env["GITHUB_REPOSITORY"]
    code, out, err = gh(["repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"])
    if code != 0 or not out.strip():
        raise Unreadable(f"gh could not name the repository ({err.strip() or code})")
    return out.strip()


def _found_line(report: dict) -> str:
    tag, found = report["tag"], report["found"]
    parts = [f"tag {tag} -> {found['tag'][:7]}" if found["tag"] else f"no tag {tag}"]
    rel = found["release"]
    if rel is None:
        parts.append("no release")
    else:
        kind = "draft release" if rel["draft"] else "published release"
        parts.append(f"{kind} {tag} ({rel['assets']} assets)")
    if found["pypi"] is not None:
        parts.append(f"PyPI {tag[1:]} {'present' if found['pypi'] else 'absent'}")
    return "found: " + "; ".join(parts)


def text_report(report: dict) -> str:
    lines = [f"release_cleanup: {report['tag']} in {report['repo']}"]
    found = report["found"]
    if found is not None:
        lines.append(_found_line(report))
        if found["tag"] is None and found["release"] is None:
            lines.append("nothing to remove")
    lines += [f"removed: {x}" for x in report["removed"]]
    lines += [f"would remove: {x}" for x in report["would_remove"]]
    lines += [f"kept: {x}" for x in report["kept"]]
    lines += [f"error: {x}" for x in report["errors"]]
    lines += [f"retry: {x}" for x in report["retry"]]
    return "\n".join(lines) + "\n"


def cleanup(
    tag: str,
    repo: str,
    gh: Gh,
    pypi: PyPI,
    run_id: str | None = None,
    dry_run: bool = False,
) -> dict:
    """Read the state of ``tag`` and remove the draft and the tag where that is safe."""
    kind = tag_kind(tag)
    run = run_id or "<run-id>"
    report = {
        "tag": tag,
        "repo": repo,
        "dry_run": dry_run,
        "found": None,
        "removed": [],
        "would_remove": [],
        "kept": [],
        "errors": [],
        "retry": [],
        "exit": 0,
    }
    try:
        found = {
            "tag": read_tag(gh, repo, tag),
            "release": read_release(gh, repo, tag),
            "pypi": None,
        }
        report["found"] = found
        if found["tag"] is None and found["release"] is None:
            return report
        if found["release"] is not None and not found["release"]["draft"]:
            report["kept"].append(
                f"release {tag} and its tag: the release is published (public, archived by Zenodo)"
            )
            report["exit"] = 3
            return report
        if kind == "software":
            found["pypi"] = pypi(tag[1:])
            if found["pypi"]:
                report["kept"].append(f"tag {tag} and the draft: PyPI holds {tag[1:]}")
                report["retry"] += [
                    f"gh run rerun {run} --failed   (same commit, within 30 days of the run; "
                    "the PyPI files are reused through skip-existing and the hash check)",
                    f"when the cause needs a code change, the next release is a new version: "
                    f"PyPI holds {tag[1:]}",
                ]
                report["exit"] = 3
                return report
    except Unreadable as e:
        report["errors"].append(str(e))
        report["exit"] = 1
        return report

    steps = []
    if found["release"] is not None:
        steps.append((f"draft release {tag}", ["release", "delete", tag, "--repo", repo, "--yes"]))
    if found["tag"] is not None:
        steps.append((f"tag {tag}", ["api", "-X", "DELETE", f"repos/{repo}/git/refs/tags/{tag}"]))
    for what, args in steps:
        if dry_run:
            report["would_remove"].append(what)
            continue
        code, _, err = gh(args)
        if code != 0:
            report["errors"].append(f"could not remove {what} ({err.strip() or code})")
            report["exit"] = 1
            return report
        report["removed"].append(what)
    if kind == "software":
        report["retry"] += [
            f"gh run rerun {run}   (the whole run, same commit, within 30 days of the run; "
            "the tag and the draft are made again)",
            f"after a fix on dev, merge a new pull request into main; {tag} is free",
        ]
    else:
        report["retry"].append("fix on `paper`, push, and push the tag again; the name is free")
    return report


def main(
    argv: list[str] | None = None,
    gh: Gh = run_gh,
    pypi: PyPI = pypi_has,
    env: dict | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tag", required=True, help="v<version> or a paper tag")
    parser.add_argument("--repo", help="OWNER/NAME (default $GITHUB_REPOSITORY, else gh repo view)")
    parser.add_argument("--run-id", help="the failed run, named in the retry lines")
    parser.add_argument("--dry-run", action="store_true", help="read everything, remove nothing")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--report", type=Path, help="also write the report here as Markdown")
    args = parser.parse_args(argv)
    if tag_kind(args.tag) is None:
        print(
            f"release_cleanup: {args.tag!r} is neither v<version> nor a paper tag", file=sys.stderr
        )
        return 2
    env = os.environ if env is None else env
    try:
        repo = args.repo or resolve_repo(gh, env)
    except Unreadable as e:
        print(f"release_cleanup: {e}", file=sys.stderr)
        return 1
    report = cleanup(args.tag, repo, gh, pypi, run_id=args.run_id, dry_run=args.dry_run)
    text = text_report(report)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(text, end="")
    if args.report:
        body = "\n".join(f"- {line}" for line in text.splitlines()[1:])
        args.report.write_text(f"### {text.splitlines()[0]}\n\n{body}\n", encoding="utf-8")
    return report["exit"]


if __name__ == "__main__":
    sys.exit(main())
