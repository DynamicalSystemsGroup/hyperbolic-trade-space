"""Stage the site locally: assemble into ``_stage/`` and serve it on 127.0.0.1.

    uv run python scripts/stage_site.py [--serve] [--port 8000] [--no-build]

No network access and no kernel are needed. Review the pages printed, then stop with Ctrl-C.
"""

from __future__ import annotations

import argparse
import functools
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import assemble_site

STAGE_DIR = assemble_site.ROOT / "_stage"
HOST = "127.0.0.1"
REVIEW_PAGES = (
    "/",
    "/docs/",
    "/docs/getting-started/",
    "/docs/user-guide/overview/",
    "/docs/theory/",
    "/docs/generated/glossary/",
    "/docs/api-reference/",
    "/docs/further-reading/",
    "/paper/",
)


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def make_server(directory, port=8000):
    """A threading HTTP server for ``directory`` bound to 127.0.0.1 only (port 0 = ephemeral)."""
    handler = functools.partial(_QuietHandler, directory=str(directory))
    return ThreadingHTTPServer((HOST, port), handler)


def serve_in_thread(directory, port=0):
    """Start ``make_server`` in a daemon thread; return the server (call ``shutdown``)."""
    server = make_server(directory, port)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def stage(out=STAGE_DIR, build=True, mkdocs_runner=None):
    """Assemble into ``out`` (unless ``build`` is false and it exists). Returns the path."""
    out = Path(out)
    if build or not out.exists():
        return assemble_site.assemble(out, mkdocs_runner=mkdocs_runner)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--serve", action="store_true", help="serve the staged site")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-build", action="store_true", help="reuse an existing _stage/")
    args = parser.parse_args(argv)
    try:
        out = stage(STAGE_DIR, build=not args.no_build)
    except Exception as exc:
        print(f"stage_site: FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"staged site in {out}")
    if not args.serve:
        return 0
    server = make_server(out, args.port)
    base = f"http://{HOST}:{server.server_address[1]}"
    print(f"serving {base} (Ctrl-C to stop). Pages to review:")
    for page in REVIEW_PAGES:
        print(f"  {base}{page}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
