"""Tier 0 and tier 1 checks (docs/superpowers/notes/verification-strategy.md).

    uv run python scripts/check.py --changed   # lint, format and the tests mapped to changed paths
    uv run python scripts/check.py --fast      # the fast suite: pytest -m "not slow" -n auto
    uv run python scripts/check.py --list      # print the path-to-tests map

``--changed`` reads ``git diff --name-only origin/dev...HEAD`` (against the merge base, so upstream
changes are not listed as local) plus uncommitted and untracked files. A changed path that no
mapping covers (README, work-packages, uv.lock, tests/conftest.py) runs the fast suite instead.
Add ``--dry-run`` to print what would run without running it.
"""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (glob on a repo-relative posix path, pytest arguments). First match adds; all matches union.
PATH_TESTS: list[tuple[str, list[str]]] = [
    (
        "src/*",
        [
            "tests/test_package.py",
            "tests/test_estimator.py",
            "tests/test_solvers.py",
            "tests/test_sklearn_compat.py",
            "tests/test_plotting.py",
            "tests/test_coordinates.py",
            "tests/test_predictive.py",
            "tests/test_preconditioning.py",
            "tests/test_tuning.py",
            "tests/test_tensions.py",
            "tests/test_datasets.py",
            "src",
        ],
    ),
    (
        "derivation/*",
        ["tests/test_derivation.py", "tests/test_matches_derivation.py", "tests/test_proof_map.py"],
    ),
    ("derivation/*", ["tests/test_paper.py", "-k", "appendix_b"]),
    ("paper/container/*", ["tests/test_container.py"]),
    ("paper/*", ["tests/test_paper.py", "tests/test_paper_sources.py", "tests/test_case.py"]),
    (
        "docs/*",
        [
            "tests/test_site.py",
            "tests/test_docs.py",
            "tests/test_narrative.py",
            "tests/test_references.py",
        ],
    ),
    ("site/*", ["tests/test_site.py", "tests/test_narrative.py"]),
    ("mkdocs.yml", ["tests/test_site.py", "tests/test_docs.py"]),
    (
        "scripts/*",
        ["tests/test_site.py", "tests/test_build_generated.py", "tests/test_check_script.py"],
    ),
    ("glossary.yaml", ["tests/test_build_generated.py", "tests/test_paper.py"]),
    (
        "examples/adcs/experiments/*",
        [
            "tests/test_experiments.py",
            "tests/test_toolkit.py",
            "tests/test_legacy_oracle.py",
            "tests/test_cubesat_oracle.py",
        ],
    ),
    (
        "examples/adcs/model_v2/*",
        [
            "tests/test_system_model_v2.py",
            "tests/test_system_model_v2_r1.py",
            "tests/test_model_checking_v2.py",
            "tests/test_mutation_v2.py",
            "tests/test_v2_data.py",
        ],
    ),
    (
        "examples/*",
        [
            "tests/test_adcs_case.py",
            "tests/test_case.py",
            "tests/test_k_terms_case.py",
            "tests/test_cubesat_model.py",
            "tests/test_notebook.py",
        ],
    ),
    ("work-packages/interface-contract.*", ["tests/test_interface_contract.py"]),
    ("Dockerfile", ["tests/test_container.py"]),
    ("tests/test_*.py", []),  # a changed test file runs itself (added below)
    (".github/*", ["tests/test_ci_shards.py", "tests/test_site.py"]),
    ("pyproject.toml", ["tests/test_package.py"]),
]


def mapped_tests(paths: list[str]) -> list[list[str]]:
    """The pytest argument groups for the changed paths (deduplicated, in first-seen order)."""
    groups: list[list[str]] = []
    for path in paths:
        if path.startswith("tests/test_") and path.endswith(".py") and (ROOT / path).exists():
            groups.append([path])
        for pattern, args in PATH_TESTS:
            if args and fnmatch.fnmatch(path, pattern) and args not in groups:
                groups.append(args)
    return groups


def unmapped(paths: list[str]) -> list[str]:
    """The changed paths that no mapping covers (these fall back to the fast suite)."""
    return [p for p in paths if not mapped_tests([p])]


FAST = ["-m", "not slow"]


def changed_paths(base: str = "origin/dev") -> list[str]:
    def git(*a: str) -> list[str]:
        out = subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
        return [x for x in out.stdout.splitlines() if x]

    names = (
        set(git("diff", "--name-only", f"{base}...HEAD"))
        | set(git("diff", "--name-only", "HEAD"))
        | set(git("ls-files", "--others", "--exclude-standard"))
    )
    return sorted(n for n in names if (ROOT / n).exists())


def _run(cmd: list[str], dry: bool) -> int:
    print("+", " ".join(cmd), flush=True)
    return 0 if dry else subprocess.run(cmd, cwd=ROOT).returncode


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--changed", action="store_true")
    mode.add_argument("--fast", action="store_true")
    mode.add_argument("--list", action="store_true")
    ap.add_argument("--base", default="origin/dev")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if args.list:
        for pattern, tests in PATH_TESTS:
            print(f"{pattern:40s} -> {' '.join(tests) or '(the file itself)'}")
        return 0
    if args.fast:
        return _run(
            ["uv", "run", "pytest", "-m", "not slow", "-q", "-n", "auto", "--dist", "loadgroup"],
            args.dry_run,
        )

    paths = changed_paths(args.base)
    print("changed:", *paths, sep="\n  ") if paths else print("no changes")
    py = [p for p in paths if p.endswith(".py")]
    rc = 0
    if py:
        rc |= _run(["uv", "run", "ruff", "check", *py], args.dry_run)
        rc |= _run(["uv", "run", "ruff", "format", "--check", *py], args.dry_run)
    for group in mapped_tests(paths):
        rc |= _run(
            ["uv", "run", "pytest", "-q", "-n", "auto", "--dist", "loadgroup", *group], args.dry_run
        )
    if unmapped(paths):
        print("unmapped:", *unmapped(paths), sep="\n  ")
        rc |= _run(
            ["uv", "run", "pytest", *FAST, "-q", "-n", "auto", "--dist", "loadgroup"], args.dry_run
        )
    return 1 if rc else 0


if __name__ == "__main__":
    sys.exit(main())
