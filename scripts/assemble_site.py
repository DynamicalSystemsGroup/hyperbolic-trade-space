"""Compose the static site: root index, MkDocs docsite under ``docs/``, the paper slot.

    uv run python scripts/assemble_site.py [--out DIR] [--generated-dir DIR] [--slot auto|abstract]
                                           [--artefact PATH] [--strict-slot] [--summary FILE]

Default output is ``_site/``. The composer never builds the paper (WP65 specification, 3.4): the
paper slot at ``<out>/paper/`` is either the abstract page (``scripts/paper_abstract.py``) or the
published HTML of the pin that ``paper/mode.toml`` names.

1. Resolve the slot. ``--slot abstract`` gives the abstract page. ``--slot auto`` (the default)
   reads ``paper/mode.toml``: ``abstract`` mode gives the abstract page; a pinned mode takes the
   pin's ``paper-html.tar.gz`` from ``--artefact PATH`` (with ``paper-keys.json`` beside it) or
   from the pin's GitHub release, checks its SHA-256 against the mode file's ``sha256`` and checks
   the release's ``paper-keys.json`` equals the committed ``paper/paper-keys.json`` byte for byte.
   Any failure gives the abstract page in its fallback form, with the reason; the slot is
   ``abstract``, ``pin`` or ``fallback``.
2. Write the generated pages and build the docs (``mkdocs build --strict``) with
   ``HTS_PAPER_SLOT`` set to ``pin`` or ``abstract`` (a fallback is ``abstract``), so the docs'
   citations of the paper match what ``/paper/`` holds.
3. Copy the root page, with the paper card's line for the slot; write the history page and the
   root page's figures.
4. Place the slot at ``<out>/paper/``; a pinned slot carries one banner line per page.
5. Print ``assemble_site: slot <slot> <pin or -> <reason or ->``; ``--summary FILE`` appends it as
   Markdown; a fallback also prints a GitHub warning annotation.

Exit 0 when the site is composed (any slot); 1 on a build failure, or on a fallback under
``--strict-slot`` (nothing is composed then); 2 on a usage error.
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import hashlib
import html
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_figures  # noqa: E402
import build_generated  # noqa: E402
import build_site_figures  # noqa: E402
import history_record  # noqa: E402
import paper_abstract  # noqa: E402
import paper_keys  # noqa: E402

DEFAULT_OUT = ROOT / "_site"
GENERATED_DIR = build_generated.DEFAULT_OUT  # outside docs/: the paper's own build reads it
DOCS_GENERATED_DIR = build_generated.DOCS_GENERATED  # inside mkdocs docs_dir: the glossary
ROOT_INDEX = ROOT / "site" / "index.html"
ROOT_HISTORY = ROOT / "site" / "history.html"
MODE_FILE = ROOT / "paper" / "mode.toml"
KEYS_FILE = paper_keys.MANIFEST
PAPER_MODE_SCRIPT = ROOT / "scripts" / "paper_mode.py"  # the mode file's validator (WP65, 3.1)
REPOSITORY = "DynamicalSystemsGroup/tradespace"
RELEASE_ASSET_URL = "https://github.com/" + REPOSITORY + "/releases/download/{pin}/{name}"
ARTEFACT_NAME = "paper-html.tar.gz"
KEYS_NAME = "paper-keys.json"
FETCH_TIMEOUT = 60  # seconds, per attempt
FETCH_ATTEMPTS = 2
MODES = ("abstract", "working", "submitted", "revision")
SLOTS = ("auto", "abstract")

# The root page's paper card (C14): its line per mode; the link stays paper/.
ROOT_CARD = '<a class="card" href="paper/"><strong>Read the paper</strong><span>{}</span></a>'
ROOT_CARD_LINE_PINNED = "the argument and the proofs"
ROOT_CARD_LINE_ABSTRACT = "its abstract; the paper is iterated towards release"

BANNER_STYLE = (
    "margin:0;padding:0.5rem 3.5rem;font:0.95rem/1.4 system-ui,sans-serif;text-align:center;"
    "border-bottom:1px solid rgba(127,127,127,0.4)"
)
# The theme colours its own containers, not <body>, and toggles `dark` on <html>; the banner
# names its colours for both (the padding clears the theme's fixed scheme button at phone width).
BANNER_CSS = (
    ".hts-paper-banner{color:#1c1917;background:#f5f5f4}"
    "html.dark .hts-paper-banner{color:#e7e5e4;background:#292524}"
    ".hts-paper-banner a{color:inherit}"
)
_DOI = re.compile(r"^10\.5281/zenodo\.\d+$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class SlotFailure(Exception):
    """The pinned paper cannot be served; the message is the reason given on the page."""


@dataclasses.dataclass
class Slot:
    """What ``/paper/`` holds: ``abstract``, ``pin`` (with the staged artefact) or ``fallback``."""

    slot: str
    pin: str = ""
    reason: str = ""
    mode: dict = dataclasses.field(default_factory=dict)
    staged: Path | None = None  # the unpacked artefact, banners inserted (pin only)

    @property
    def docs_slot(self) -> str:
        """The docs' citation slot: anchors for a pin, ``/paper/`` otherwise."""
        return "pin" if self.slot == "pin" else "abstract"

    def line(self) -> str:
        return f"assemble_site: slot {self.slot} {self.pin or '-'} {self.reason or '-'}"


# --- the mode file ---------------------------------------------------------------------------


def read_mode(mode_file=None) -> dict:
    """The mode file's fields, checked for serving; ``SlotFailure`` names the broken rule.

    ``scripts/paper_mode.py check --stage served`` is run when it exists (the validator of record);
    the composer also checks the fields it relies on itself.
    """
    mode_file = Path(mode_file or MODE_FILE)
    try:
        mode = tomllib.loads(mode_file.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise SlotFailure(f"{mode_file.name} unreadable: {exc}") from exc
    if PAPER_MODE_SCRIPT.is_file():
        command = [sys.executable, str(PAPER_MODE_SCRIPT), "check", "--stage", "served"]
        result = subprocess.run(
            [*command, "--file", str(mode_file)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            said = " ".join((result.stdout + result.stderr).split()) or f"exit {result.returncode}"
            raise SlotFailure(f"{mode_file.name}: {said}")
    if mode.get("schema") != 1:
        raise SlotFailure(f"{mode_file.name}: schema must be 1")
    if mode.get("mode") not in MODES:
        raise SlotFailure(f"{mode_file.name}: mode must be one of {', '.join(MODES)}")
    if mode["mode"] != "abstract":
        if not mode.get("pin"):
            raise SlotFailure(f"{mode_file.name}: a pinned mode names its pin")
        if not _DOI.match(str(mode.get("doi", ""))):
            raise SlotFailure(f"{mode_file.name}: doi must match {_DOI.pattern}")
        if not _SHA256.match(str(mode.get("sha256", ""))):
            raise SlotFailure(f"{mode_file.name}: sha256 must be 64 hex digits")
    return mode


def banner_line(mode: dict) -> str:
    """The banner's text for a pinned mode (WP65 specification, 3.2)."""
    tail = f"{mode['pin']} · {mode['date']} · DOI {mode['doi']}"
    if mode["mode"] == "working":
        return f"Working paper · {tail}"
    if mode["mode"] == "submitted":
        return f"Submitted to {mode['venue']} · {tail}"
    if mode["mode"] == "revision":
        return f"Revision {mode['round']} for {mode['venue']} · {tail}"
    raise ValueError(f"no banner in mode {mode['mode']!r}")


def banner_html(mode: dict) -> str:
    """The banner element, linked to the DOI."""
    return (
        f'<p class="hts-paper-banner" style="{BANNER_STYLE}">'
        f'<a href="https://doi.org/{html.escape(mode["doi"])}">'
        f"{html.escape(banner_line(mode))}</a></p>"
    )


def banner_installer(banner: str) -> str:
    """The banner inside a ``<template>`` with the script that installs it as ``<body>``'s first
    element once the page has loaded.

    The article theme hydrates the whole document with React, and a static element placed after
    ``<body>`` makes that hydration fail (React error 418): the theme then renders the page afresh
    on the client and the static banner is gone (WP67's browser pass). An element added after the
    load event, and put back if the theme removes it in its first seconds, stays.
    """
    return (
        f'<template id="hts-paper-banner-source"><style>{BANNER_CSS}</style>{banner}</template>\n'
        "<script>(function(){"
        'var t=document.getElementById("hts-paper-banner-source");if(!t)return;'
        "var s=t.content.firstElementChild,b=s.nextElementSibling,n=0;"
        "function put(){if(!document.head.contains(s))document.head.appendChild(s);"
        "if(!document.body.contains(b))document.body.insertBefore(b,document.body.firstChild);}"
        "function keep(){put();if(++n<50)setTimeout(keep,100);}"
        'if(document.readyState==="complete")keep();else window.addEventListener("load",keep);'
        "})();</script>\n"
    )


def insert_banner(page: str, banner: str) -> str:
    """``page`` with the banner's installer directly before its closing ``</body>`` tag;
    unchanged when it has none."""
    at = page.lower().rfind("</body>")
    if at < 0:
        return page
    return page[:at] + banner_installer(banner) + page[at:]


# --- obtaining and checking the artefact -----------------------------------------------------


def fetch(url: str) -> bytes:
    """The bytes at ``url`` (two attempts, 60 s each); ``SlotFailure`` when unreachable."""
    last = None
    for attempt in range(FETCH_ATTEMPTS):
        try:
            with urllib.request.urlopen(url, timeout=FETCH_TIMEOUT) as response:
                return response.read()
        except (urllib.error.URLError, OSError) as exc:
            last = exc
            if attempt + 1 < FETCH_ATTEMPTS:
                time.sleep(2)
    raise SlotFailure(f"{url.rsplit('/', 1)[-1]} unreachable: {last}")


def _read_local(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise SlotFailure(f"{path.name} unreachable: {exc.strerror or exc}") from exc


def unpack(data: bytes, dest: Path) -> int:
    """Unpack the artefact into ``dest``; insert nothing. Returns the number of HTML pages."""
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
            tar.extractall(dest, filter="data")
    except (tarfile.TarError, OSError, EOFError) as exc:
        raise SlotFailure(f"{ARTEFACT_NAME} does not unpack: {exc}") from exc
    if not (dest / "index.html").is_file():
        raise SlotFailure(f"{ARTEFACT_NAME} holds no index.html")
    return len(list(dest.rglob("*.html")))


def resolve_slot(
    slot="auto",
    artefact=None,
    mode_file=None,
    keys_file=None,
    fetcher=None,
) -> Slot:
    """Resolve what ``/paper/`` holds (step 1). A pinned slot is unpacked to a temporary
    directory with one banner line per page; any failure gives ``fallback`` with the reason."""
    if slot not in SLOTS:
        raise ValueError(f"slot must be one of {SLOTS}, got {slot!r}")
    if slot == "abstract":
        return Slot("abstract")
    mode_file = Path(mode_file or MODE_FILE)
    keys_file = Path(keys_file or KEYS_FILE)
    pin = ""
    try:
        with contextlib.suppress(OSError, tomllib.TOMLDecodeError):
            pin = str(tomllib.loads(Path(mode_file).read_text(encoding="utf-8")).get("pin", ""))
        mode = read_mode(mode_file)
        if mode["mode"] == "abstract":
            return Slot("abstract", mode=mode)
        pin = mode["pin"]
        if artefact is not None:
            artefact = Path(artefact)
            data = _read_local(artefact)
            keys = _read_local(artefact.parent / KEYS_NAME)
        else:
            get = fetcher or fetch
            data = get(RELEASE_ASSET_URL.format(pin=pin, name=ARTEFACT_NAME))
            keys = get(RELEASE_ASSET_URL.format(pin=pin, name=KEYS_NAME))
        digest = hashlib.sha256(data).hexdigest()
        if digest != mode["sha256"]:
            raise SlotFailure(
                f"checksum mismatch: {ARTEFACT_NAME} has SHA-256 {digest[:12]}..., "
                f"{Path(mode_file).name} names {mode['sha256'][:12]}..."
            )
        try:
            committed = Path(keys_file).read_bytes()
        except OSError as exc:
            raise SlotFailure(f"the committed {KEYS_NAME} is unreadable: {exc}") from exc
        if keys != committed:
            raise SlotFailure(
                f"keys mismatch: the pin's {KEYS_NAME} differs from the committed one"
            )
        staged = Path(tempfile.mkdtemp(prefix="hts-paper-slot-"))
        try:
            unpack(data, staged)
        except SlotFailure:
            shutil.rmtree(staged, ignore_errors=True)
            raise
        banner = banner_html(mode)
        for page in staged.rglob("*.html"):
            try:
                text = page.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                shutil.rmtree(staged, ignore_errors=True)
                name = page.relative_to(staged).as_posix()
                raise SlotFailure(f"{ARTEFACT_NAME}: {name} is not UTF-8 text") from exc
            page.write_text(insert_banner(text, banner), "utf-8")
        return Slot("pin", pin=pin, mode=mode, staged=staged)
    except SlotFailure as exc:
        return Slot("fallback", pin=pin, reason=str(exc))


def place_slot(out, slot: Slot, renderer=None) -> Path:
    """Place the slot at ``<out>/paper/`` (step 4). Returns the directory."""
    dest = Path(out) / "paper"
    if slot.slot == "pin":
        shutil.copytree(slot.staged, dest, dirs_exist_ok=True)
        shutil.rmtree(slot.staged, ignore_errors=True)
        return dest
    render = renderer or paper_abstract.render
    fallback = (slot.pin or "-", slot.reason) if slot.slot == "fallback" else None
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.html").write_text(render(fallback=fallback), encoding="utf-8")
    return dest


def root_page(slot: Slot, source=None) -> str:
    """The root page with the paper card's line for ``slot`` (step 3)."""
    text = Path(source or ROOT_INDEX).read_text(encoding="utf-8")
    pinned = ROOT_CARD.format(ROOT_CARD_LINE_PINNED)
    if text.count(pinned) != 1:
        raise ValueError(f"{ROOT_INDEX.name}: the paper card is not {pinned!r} exactly once")
    if slot.slot == "pin":
        return text
    return text.replace(pinned, ROOT_CARD.format(ROOT_CARD_LINE_ABSTRACT))


def report(slot: Slot, summary=None) -> None:
    """Print the slot line (step 5); append it to ``summary`` as Markdown; warn on a fallback."""
    print(slot.line())
    if slot.slot == "fallback":
        print(f"::warning title=Paper slot fell back::{slot.pin or '-'}: {slot.reason}")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(
                f"### Paper slot\n\n- slot: `{slot.slot}`\n- pin: `{slot.pin or '-'}`\n"
                f"- reason: {slot.reason or '-'}\n\n"
            )


# --- the docs and the rest of the site -------------------------------------------------------


def mkdocs_command(out_docs):
    """The strict MkDocs build command writing to ``out_docs``."""
    if importlib.util.find_spec("mkdocs") is not None:
        base = [sys.executable, "-m", "mkdocs"]
    else:
        base = ["uv", "run", "--group", "docs", "mkdocs"]
    return [*base, "build", "--strict", "-f", str(ROOT / "mkdocs.yml"), "-d", str(out_docs)]


@contextlib.contextmanager
def _paper_slot_variable(value):
    """Set ``HTS_PAPER_SLOT`` for the docs build, restoring the environment after."""
    old = os.environ.get(paper_keys.SLOT_VARIABLE)
    os.environ[paper_keys.SLOT_VARIABLE] = value
    try:
        yield
    finally:
        if old is None:
            os.environ.pop(paper_keys.SLOT_VARIABLE, None)
        else:
            os.environ[paper_keys.SLOT_VARIABLE] = old


def run_mkdocs(out_docs, runner=None, docs_slot="abstract"):
    """Run the MkDocs build with the docs' citation slot; ``runner(cmd)`` is injectable for tests.
    Raises on failure."""
    cmd = mkdocs_command(out_docs)
    with _paper_slot_variable(docs_slot):
        if runner is not None:
            return runner(cmd)
        subprocess.run(cmd, cwd=ROOT, check=True)


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
    slot="auto",
    artefact=None,
    resolved=None,
    mode_file=None,
    keys_file=None,
    fetcher=None,
    renderer=None,
):
    """Compose the whole site into ``out`` (replaced if present). Returns ``(out, Slot)``.

    ``resolved`` is a slot already resolved by ``resolve_slot``; otherwise ``slot``,
    ``artefact``, ``mode_file``, ``keys_file`` and ``fetcher`` resolve it here.
    """
    out = _check_out(out)
    resolved = resolved or resolve_slot(slot, artefact, mode_file, keys_file, fetcher)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    with _build_lock():
        build_generated.build(
            generated_dir, collect_runner=collect_runner, docs_out=docs_generated_dir
        )
        (figures_builder or build_figures.build)(Path(docs_generated_dir) / "figures")
        run_mkdocs(out / "docs", runner=mkdocs_runner, docs_slot=resolved.docs_slot)
    if not ROOT_INDEX.is_file():
        raise FileNotFoundError(f"missing root index: {ROOT_INDEX}")
    (out / "index.html").write_text(root_page(resolved), encoding="utf-8")
    # the stand-alone history page (WP37): its prose with the dated list of history.yaml inserted
    (out / "history.html").write_text(
        history_record.build_page_file(ROOT_HISTORY), encoding="utf-8"
    )
    for asset in sorted(ROOT_INDEX.parent.glob("*.webp")):  # figures the root index uses
        shutil.copy2(asset, out / asset.name)
    (site_figures_builder or build_site_figures.build_all)(out)  # the story and the fan figures
    place_slot(out, resolved, renderer)
    return out, resolved


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory (default _site/)")
    parser.add_argument(
        "--generated-dir",
        default=str(GENERATED_DIR),
        help="directory for derivations.md and verification.md (default build/generated/)",
    )
    parser.add_argument(
        "--slot",
        choices=SLOTS,
        default="auto",
        help="auto: what paper/mode.toml names (default); abstract: the abstract page",
    )
    parser.add_argument(
        "--artefact",
        help="a local paper-html.tar.gz of the pin (paper-keys.json beside it) instead of the "
        "pin's GitHub release",
    )
    parser.add_argument("--strict-slot", action="store_true", help="exit 1 instead of falling back")
    parser.add_argument("--summary", help="append the slot line to this Markdown file")
    args = parser.parse_args(argv)
    resolved = resolve_slot(args.slot, args.artefact)
    if resolved.slot == "fallback" and args.strict_slot:
        report(resolved, args.summary)
        print(
            "assemble_site: FAILED: the paper slot fell back under --strict-slot", file=sys.stderr
        )
        return 1
    try:
        out, resolved = assemble(args.out, generated_dir=args.generated_dir, resolved=resolved)
    except Exception as exc:
        if resolved.staged is not None:
            shutil.rmtree(resolved.staged, ignore_errors=True)
        print(f"assemble_site: FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"assembled site in {out}")
    report(resolved, args.summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
