"""Assemble the static site: root index, MkDocs docsite under ``docs/``, paper slot.

    uv run python scripts/assemble_site.py [--out DIR]

Default output is ``_site/``. Steps: write the generated pages (``build_generated``: the
glossary into ``docs/generated/`` for the docsite, derivations and verification into
``build/generated/`` for the paper's build), run
``mkdocs build --strict -d <out>/docs``, copy ``site/index.html`` to ``<out>/index.html`` and
build the paper slot through ``build_paper`` (WP10 replaces that one function). Any error
stops the build with a non-zero exit.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_generated  # noqa: E402

DEFAULT_OUT = ROOT / "_site"
GENERATED_DIR = build_generated.DEFAULT_OUT  # outside docs/: the paper's build reads it
DOCS_GENERATED_DIR = build_generated.DOCS_GENERATED  # inside mkdocs docs_dir: the glossary
ROOT_INDEX = ROOT / "site" / "index.html"
PAPER_PLACEHOLDER = ROOT / "site" / "paper" / "index.html"


def mkdocs_command(out_docs):
    """The strict MkDocs build command writing to ``out_docs``."""
    if importlib.util.find_spec("mkdocs") is not None:
        base = [sys.executable, "-m", "mkdocs"]
    else:
        base = ["uv", "run", "--group", "docs", "mkdocs"]
    return [*base, "build", "--strict", "-f", str(ROOT / "mkdocs.yml"), "-d", str(out_docs)]


def run_mkdocs(out_docs, runner=None):
    """Run the MkDocs build; ``runner(cmd)`` is injectable for tests. Raises on failure."""
    cmd = mkdocs_command(out_docs)
    if runner is not None:
        return runner(cmd)
    subprocess.run(cmd, cwd=ROOT, check=True)


def build_paper(out):
    """Place the paper at ``<out>/paper/``. WP10 replaces this function with the MyST build."""
    out = Path(out)
    if not PAPER_PLACEHOLDER.is_file():
        raise FileNotFoundError(f"missing paper placeholder: {PAPER_PLACEHOLDER}")
    dest = out / "paper"
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PAPER_PLACEHOLDER, dest / "index.html")


@contextlib.contextmanager
def _build_lock():
    """Serialize the generated-page step and the MkDocs read of ``docs/`` across processes
    (parallel pytest runs or builds in one checkout)."""
    lock_dir = ROOT / "build"
    lock_dir.mkdir(exist_ok=True)
    with open(lock_dir / ".site-build.lock", "w") as fh:
        try:
            import fcntl
        except ImportError:  # not POSIX: no lock available
            yield
            return
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _check_out(out):
    out = Path(out).resolve()
    if out == ROOT or out in ROOT.parents or out == Path(out.anchor):
        raise ValueError(f"refusing to use {out} as an output directory")
    return out


def assemble(
    out=DEFAULT_OUT,
    mkdocs_runner=None,
    generated_dir=GENERATED_DIR,
    collect_runner=None,
    docs_generated_dir=DOCS_GENERATED_DIR,
):
    """Build the whole site into ``out`` (replaced if present). Returns the output path."""
    out = _check_out(out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    with _build_lock():
        build_generated.build(
            generated_dir, collect_runner=collect_runner, docs_out=docs_generated_dir
        )
        run_mkdocs(out / "docs", runner=mkdocs_runner)
    if not ROOT_INDEX.is_file():
        raise FileNotFoundError(f"missing root index: {ROOT_INDEX}")
    shutil.copy2(ROOT_INDEX, out / "index.html")
    for asset in sorted(ROOT_INDEX.parent.glob("*.webp")):  # figures the root index uses
        shutil.copy2(asset, out / asset.name)
    build_paper(out)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory (default _site/)")
    parser.add_argument(
        "--generated-dir",
        default=str(GENERATED_DIR),
        help="directory for derivations.md and verification.md (default build/generated/)",
    )
    args = parser.parse_args(argv)
    try:
        out = assemble(args.out, generated_dir=args.generated_dir)
    except Exception as exc:
        print(f"assemble_site: FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"assembled site in {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
