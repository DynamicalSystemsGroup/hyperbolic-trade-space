"""Assemble the static site: root index, MkDocs docsite under ``docs/``, paper slot.

    uv run python scripts/assemble_site.py [--out DIR] [--paper placeholder]

Default output is ``_site/``. Steps: write the generated pages (``build_generated``: the
glossary into ``docs/generated/`` for the docsite, derivations and verification into
``build/generated/`` for the paper's build), run
``mkdocs build --strict -d <out>/docs``, copy ``site/index.html`` to ``<out>/index.html`` (with
the paper's ``figure1.png`` and the story figure from ``build_site_figures``) and
build the paper slot through ``build_paper``: the real paper (``myst build --html`` in ``paper/``,
copied from ``paper/_build/html``). The command line is strict: a paper that does not build, or
writes no ``index.html``, exits non-zero naming the failure and the flag; ``--paper placeholder`` is
the only way to get the placeholder page. (The function ``assemble(paper="auto")`` keeps its
fall-back for callers.) Any other error stops the build with a non-zero exit. The
docsite's figures (``build_figures``) are built before MkDocs reads ``docs/``.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_figures  # noqa: E402
import build_generated  # noqa: E402
import build_site_figures  # noqa: E402

DEFAULT_OUT = ROOT / "_site"
GENERATED_DIR = build_generated.DEFAULT_OUT  # outside docs/: the paper's build reads it
DOCS_GENERATED_DIR = build_generated.DOCS_GENERATED  # inside mkdocs docs_dir: the glossary
ROOT_INDEX = ROOT / "site" / "index.html"
PAPER_PLACEHOLDER = ROOT / "site" / "paper" / "index.html"
PAPER_DIR = ROOT / "paper"
# The What image on the root page is the paper's Figure 1, copied (never regenerated) at build time.
FIGURE1 = PAPER_DIR / "figures" / "figure1.png"
FIGURE1_NAME = "figure1.png"
PAPER_HTML = PAPER_DIR / "_build" / "html"
PUBLIC_PAPER_BASE = "/hyperbolic-trade-space/paper"  # the published route (the Pages project path)


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


def paper_command():
    """The MyST HTML build command, run from ``paper/``."""
    return ["uv", "run", "myst", "build", "--html"]


def run_paper_build(base_url, paper_dir=PAPER_DIR):
    """Build the paper with MyST for the route ``base_url``; True when it built."""
    env = {**os.environ, "BASE_URL": base_url}
    try:
        subprocess.run(paper_command(), cwd=paper_dir, env=env, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(
            f"assemble_site: the paper did not build ({type(exc).__name__}): {exc}", file=sys.stderr
        )
        return False
    return (paper_dir / "_build" / "html" / "index.html").is_file()


def build_paper(out, paper="auto", base_url=PUBLIC_PAPER_BASE, paper_runner=None, paper_html=None):
    """Place the paper at ``<out>/paper/``; returns ``"paper"`` or ``"placeholder"``.

    ``paper="auto"`` builds the real paper (``paper_runner(base_url)``, default ``run_paper_build``)
    and copies its HTML; when the build is unavailable or fails, or ``paper="placeholder"``, the
    placeholder page is used instead. ``paper="strict"`` builds the real paper and raises when it
    does not build (the placeholder only behind ``paper="placeholder"``). ``base_url`` is the route
    the paper is served under.
    """
    out = Path(out)
    dest = out / "paper"
    if paper in ("auto", "strict"):
        built = (paper_runner or run_paper_build)(base_url)
        source = Path(paper_html) if paper_html is not None else PAPER_HTML
        if built and (source / "index.html").is_file():
            shutil.copytree(source, dest, dirs_exist_ok=True)
            return "paper"
        if paper == "strict":
            raise RuntimeError(
                "the paper did not build (its error is printed above); "
                "use --paper placeholder to stage the site without it"
            )
    elif paper != "placeholder":
        raise ValueError(f"paper must be 'auto', 'strict' or 'placeholder', got {paper!r}")
    if not PAPER_PLACEHOLDER.is_file():
        raise FileNotFoundError(f"missing paper placeholder: {PAPER_PLACEHOLDER}")
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PAPER_PLACEHOLDER, dest / "index.html")
    return "placeholder"


@contextlib.contextmanager
def _build_lock():
    """Serialize the generated-page step and the MkDocs read of ``docs/`` across processes
    (parallel pytest runs or builds in one checkout)."""
    lock_dir = ROOT / "build"
    lock_dir.mkdir(exist_ok=True)
    with open(lock_dir / ".site-build.lock", "w", encoding="utf-8") as fh:
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
    figures_builder=None,
    site_figures_builder=None,
    figure1=FIGURE1,
    paper="auto",
    paper_base=PUBLIC_PAPER_BASE,
    paper_runner=None,
    paper_html=None,
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
        (figures_builder or build_figures.build)(Path(docs_generated_dir) / "figures")
        run_mkdocs(out / "docs", runner=mkdocs_runner)
    if not ROOT_INDEX.is_file():
        raise FileNotFoundError(f"missing root index: {ROOT_INDEX}")
    shutil.copy2(ROOT_INDEX, out / "index.html")
    for asset in sorted(ROOT_INDEX.parent.glob("*.webp")):  # figures the root index uses
        shutil.copy2(asset, out / asset.name)
    if not Path(figure1).is_file():
        raise FileNotFoundError(f"missing the paper's Figure 1: {figure1}")
    shutil.copy2(figure1, out / FIGURE1_NAME)  # the What image: the paper's own file
    (site_figures_builder or build_site_figures.build_all)(
        out
    )  # the Why image and the story figure
    build_paper(out, paper, paper_base, paper_runner, paper_html)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory (default _site/)")
    parser.add_argument(
        "--generated-dir",
        default=str(GENERATED_DIR),
        help="directory for derivations.md and verification.md (default build/generated/)",
    )
    parser.add_argument(
        "--paper",
        choices=("strict", "placeholder"),
        default="strict",
        help="build the real paper and fail when it does not build (default), or use the "
        "placeholder page in its place",
    )
    args = parser.parse_args(argv)
    try:
        out = assemble(args.out, generated_dir=args.generated_dir, paper=args.paper)
    except Exception as exc:
        print(f"assemble_site: FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"assembled site in {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
