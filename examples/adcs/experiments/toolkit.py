"""The pinned model-checking toolkit: where it is, how to obtain it, and how to run it (WP15 D-8).

The toolkit (``sysmlv2``, a Rust CLI: ``check``, ``lint``, ``verify --solve``) is not on PyPI. The
pin in ``toolkit-pin.toml`` names a release, one archive per platform with its size and sha256, and
the standard-library directory the CLI needs (``--lib``). Nothing is downloaded unless somebody
runs the fetch command explicitly. The command line (``PYTHONPATH`` makes ``experiments``
importable from the repository root)::

    PYTHONPATH=examples/adcs uv run python -m experiments.toolkit fetch [--lib-only|--binary-only]
    PYTHONPATH=examples/adcs uv run python -m experiments.toolkit fetch --archive PATH
    PYTHONPATH=examples/adcs uv run python -m experiments.toolkit pin
    PYTHONPATH=examples/adcs uv run python -m experiments.toolkit where

``fetch`` is idempotent: a cached binary that reports the pinned version and a cached standard
library recorded at the pinned commit mean no network at all ("cache hit"). Otherwise the archive
is downloaded from the pinned URL with a bounded retry (3 attempts, short backoff) on transient
errors (HTTP 5xx, timeouts, connection failures); if the direct URL still fails, the same tag and
asset are fetched through the release-assets API (``GET /repos/<repo>/releases/tags/<tag>`` for the
asset id, then ``GET /repos/<repo>/releases/assets/<id>`` with ``Accept: application/octet-stream``,
sending ``Authorization: Bearer`` from ``GH_TOKEN`` or ``GITHUB_TOKEN`` when set). The git step for
the library has the same bounded retry. ``fetch --archive PATH`` installs the binary from a local
archive (for instance one obtained with ``gh release download``) with exactly the same size and
sha256 verification. Every route verifies the pinned size and sha256 before a byte is extracted;
the pin and the URL are never altered. ``pin`` prints, on one line, the repository, the tag and
the asset name for the running platform, so a workflow need not hard-code them.

The archive is verified against its pinned size and sha256 before a byte of it is extracted,
the binary is then checked to report the pinned version, and the standard library is taken from
a sparse git clone whose HEAD must equal the pinned commit. An unverified file is never executed.

Where the binary is looked for, first hit wins: ``SYSML_TOOLKIT_BIN`` (the legacy ``SYSMLV2_BIN``),
the cache directory (``SYSML_TOOLKIT_CACHE``, default ``~/.cache/hyperbolic-trade-space/
sysml-toolkit``), then ``sysmlv2`` on ``PATH``. The library directory: ``SYSML_TOOLKIT_LIB`` (legacy
``SYSMLV2_LIB``), then the cache. ``z3`` must be on ``PATH`` for ``verify --solve`` (the ``case``
dependency group installs it into the environment).

The alternative route, a source build, gives the same binary::

    git clone --branch v0.12.0 https://github.com/Open-MBEE/sysml-toolkit && cd sysml-toolkit
    cargo build --release --locked -p sysmlv2-cli      # toolchain from rust-toolchain.toml
    export SYSML_TOOLKIT_BIN=$PWD/target/release/sysmlv2

with ``SYSML_TOOLKIT_LIB`` pointing at the pinned standard-library directory (``fetch --lib-only``
supplies it alone).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN_PATH = HERE / "toolkit-pin.toml"
FETCH_COMMAND = "PYTHONPATH=examples/adcs uv run python -m experiments.toolkit fetch"


def load_pin(path: Path = PIN_PATH) -> dict:
    """The pin file as a dict."""
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def platform_triple(system: str | None = None, machine: str | None = None) -> str:
    """The release target triple of the running platform.

    >>> platform_triple("Darwin", "arm64")
    'aarch64-apple-darwin'
    >>> platform_triple("Linux", "x86_64")
    'x86_64-unknown-linux-gnu'
    """
    system = system or platform.system()
    machine = (machine or platform.machine()).lower()
    arch = {"arm64": "aarch64", "aarch64": "aarch64", "x86_64": "x86_64", "amd64": "x86_64"}.get(
        machine, machine
    )
    os_part = {
        "Darwin": "apple-darwin",
        "Linux": "unknown-linux-gnu",
        "Windows": "pc-windows-msvc",
    }.get(system, system.lower())
    return f"{arch}-{os_part}"


def cache_dir(pin: dict | None = None) -> Path:
    """The cache directory for the pinned release (outside the repository)."""
    pin = pin or load_pin()
    root = os.environ.get("SYSML_TOOLKIT_CACHE")
    base = (
        Path(root) if root else Path.home() / ".cache" / "hyperbolic-trade-space" / "sysml-toolkit"
    )
    return base / pin["toolkit"]["tag"]


def _exe(name: str) -> str:
    return name + (".exe" if sys.platform == "win32" else "")


def cached_binary(pin: dict | None = None) -> Path:
    pin = pin or load_pin()
    return cache_dir(pin) / "bin" / _exe(pin["toolkit"]["binary"])


def cached_stdlib(pin: dict | None = None) -> Path:
    pin = pin or load_pin()
    return cache_dir(pin) / "stdlib"


def find_binary() -> Path | None:
    """The toolkit binary: ``SYSML_TOOLKIT_BIN``, the cache, then ``PATH``; ``None`` if absent."""
    pin = load_pin()
    for var in ("SYSML_TOOLKIT_BIN", "SYSMLV2_BIN"):
        if os.environ.get(var):
            p = Path(os.environ[var])
            return p if p.is_file() else None
    cached = cached_binary(pin)
    if cached.is_file():
        return cached
    found = shutil.which(pin["toolkit"]["binary"])
    return Path(found) if found else None


def find_stdlib() -> Path | None:
    """The standard-library directory: ``SYSML_TOOLKIT_LIB``, then the cache; ``None`` if absent."""
    for var in ("SYSML_TOOLKIT_LIB", "SYSMLV2_LIB"):
        if os.environ.get(var):
            p = Path(os.environ[var])
            return p if p.is_dir() else None
    cached = cached_stdlib()
    return cached if cached.is_dir() else None


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify_archive(path: Path, size: int, sha256: str) -> None:
    """Raise ``ValueError`` unless the file has exactly the pinned size and sha256.

    >>> import tempfile, pathlib
    >>> d = pathlib.Path(tempfile.mkdtemp()); f = d / "a"; _ = f.write_bytes(b"abc")
    >>> good = hashlib.sha256(b"abc").hexdigest()
    >>> verify_archive(f, 3, good)
    >>> try:
    ...     verify_archive(f, 3, "0" * 64)
    ... except ValueError as e:
    ...     print("refused")
    refused
    """
    actual_size = path.stat().st_size
    if actual_size != size:
        raise ValueError(f"{path.name}: size {actual_size} differs from the pinned {size}")
    actual = sha256_of(path)
    if actual != sha256:
        raise ValueError(f"{path.name}: sha256 {actual} differs from the pinned {sha256}")


def asset_url(pin: dict, name: str) -> str:
    t = pin["toolkit"]
    return f"https://github.com/{t['repo']}/releases/download/{t['tag']}/{name}"


def _extract_binary(archive: Path, binary: str, dest: Path) -> None:
    """Write the single member whose basename is the binary to ``dest`` (no other path is made)."""
    wanted = {binary, binary + ".exe"}
    dest.parent.mkdir(parents=True, exist_ok=True)
    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive) as z:
            names = [n for n in z.namelist() if Path(n).name in wanted]
            if len(names) != 1:
                raise ValueError(f"{archive.name}: expected one {binary} member, found {names}")
            dest.write_bytes(z.read(names[0]))
    else:
        with tarfile.open(archive) as tar:
            members = [m for m in tar.getmembers() if m.isfile() and Path(m.name).name in wanted]
            if len(members) != 1:
                raise ValueError(f"{archive.name}: expected one {binary} member, found {members}")
            src = tar.extractfile(members[0])
            assert src is not None
            with open(dest, "wb") as out:
                shutil.copyfileobj(src, out)
    dest.chmod(0o755)


ATTEMPTS = 3
BACKOFF = (1.0, 3.0)  # seconds before the 2nd and 3rd attempt


def _transient(exc: BaseException) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code >= 500 or exc.code in (408, 429)
    return isinstance(exc, urllib.error.URLError | TimeoutError | ConnectionError)


def with_retry(fn, *, attempts: int = ATTEMPTS, backoff=BACKOFF, sleep=None, transient=_transient):
    """Call ``fn()``; retry up to ``attempts`` times in all when ``transient(exc)``, else raise.

    >>> calls = []
    >>> def flaky():
    ...     calls.append(1)
    ...     if len(calls) < 3:
    ...         raise TimeoutError("slow")
    ...     return "ok"
    >>> with_retry(flaky, sleep=lambda s: None)
    'ok'
    """
    sleep = sleep or time.sleep
    for i in range(attempts):
        try:
            return fn()
        except Exception as exc:
            if i == attempts - 1 or not transient(exc):
                raise
            sleep(backoff[min(i, len(backoff) - 1)])
    raise AssertionError("unreachable")


def _git_retry(cmd: list[str], **kw):
    """``subprocess.run(cmd, check=True)`` with the bounded retry on a failing git network step."""
    return with_retry(
        lambda: subprocess.run(cmd, check=True, **kw),
        transient=lambda e: isinstance(
            e, subprocess.CalledProcessError | subprocess.TimeoutExpired
        ),
    )


def _download(url: str, dest: Path, headers: dict | None = None, opener=None) -> None:
    opener = opener or urllib.request.urlopen
    req = urllib.request.Request(url, headers=headers or {})
    with opener(req, timeout=60) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)


def _api_headers(accept: str) -> dict:
    h = {"Accept": accept, "User-Agent": "hyperbolic-trade-space-toolkit-fetch"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _download_via_api(pin: dict, name: str, dest: Path, opener=None) -> None:
    """The release-assets API route for the same tag and asset name."""
    opener = opener or urllib.request.urlopen
    t = pin["toolkit"]
    base = f"https://api.github.com/repos/{t['repo']}/releases"
    req = urllib.request.Request(
        f"{base}/tags/{t['tag']}", headers=_api_headers("application/vnd.github+json")
    )
    with opener(req, timeout=60) as resp:
        release = json.load(resp)
    ids = [a["id"] for a in release.get("assets", []) if a.get("name") == name]
    if len(ids) != 1:
        raise ValueError(f"release {t['tag']} has {len(ids)} assets named {name}")
    _download(f"{base}/assets/{ids[0]}", dest, _api_headers("application/octet-stream"), opener)


def download_archive(pin: dict, name: str, dest: Path, opener=None, sleep=None) -> str:
    """Download the pinned asset to ``dest``: direct URL (bounded retry), then the API route.

    Returns the route taken (``"direct"`` or ``"api"``). Verification is the caller's, after.
    """
    try:
        with_retry(lambda: _download(asset_url(pin, name), dest, opener=opener), sleep=sleep)
        return "direct"
    except Exception as direct:
        print(f"direct download failed ({direct}); trying the release-assets API", file=sys.stderr)
        with_retry(lambda: _download_via_api(pin, name, dest, opener), sleep=sleep)
        return "api"


def _asset_for(pin: dict, triple: str) -> dict:
    try:
        return pin["toolkit"]["assets"][triple]
    except KeyError:
        raise SystemExit(
            f"no pinned archive for {triple}; build from source instead (see the module docstring)"
        ) from None


def _install_verified(pin: dict, archive: Path, asset: dict) -> Path:
    """Verify size and sha256 (before any extraction), extract the binary, check its version."""
    verify_archive(archive, asset["size"], asset["sha256"])
    dest = cached_binary(pin)
    _extract_binary(archive, pin["toolkit"]["binary"], dest)
    got = version(dest)
    if got != pin["toolkit"]["version_output"]:
        dest.unlink()
        raise ValueError(f"{dest} reports {got!r}, pinned {pin['toolkit']['version_output']!r}")
    return dest


def binary_cached(pin: dict | None = None) -> bool:
    """True when the cached binary exists and reports the pinned version (no network)."""
    pin = pin or load_pin()
    b = cached_binary(pin)
    if not b.is_file():
        return False
    try:
        return version(b) == pin["toolkit"]["version_output"]
    except (OSError, subprocess.SubprocessError):
        return False


def _stdlib_marker(pin: dict) -> Path:
    return cache_dir(pin) / "stdlib.commit"


def stdlib_cached(pin: dict | None = None) -> bool:
    """True when the cached library exists and was recorded at the pinned commit (no network)."""
    pin = pin or load_pin()
    m = _stdlib_marker(pin)
    return (
        cached_stdlib(pin).is_dir()
        and m.is_file()
        and m.read_text().strip() == pin["stdlib"]["commit"]
    )


def fetch_binary(
    triple: str | None = None, archive: Path | None = None, opener=None, sleep=None
) -> Path:
    """Obtain the pinned binary: download (or take ``archive``), verify, extract, check version."""
    pin = load_pin()
    asset = _asset_for(pin, triple or platform_triple())
    if archive is not None:
        return _install_verified(pin, Path(archive), asset)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / asset["name"]
        download_archive(pin, asset["name"], path, opener, sleep)
        return _install_verified(pin, path, asset)


def fetch_stdlib() -> Path:
    """Sparse, depth-1 clone of the pinned tag; HEAD must equal the pinned commit."""
    pin = load_pin()
    s = pin["stdlib"]
    dest = cached_stdlib(pin)
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "src"
        git = ["git", "-c", "advice.detachedHead=false"]
        clone_cmd = [*git, "clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse"]
        clone_cmd += ["--branch", s["tag"], s["repo"], str(clone)]
        _git_retry(clone_cmd)
        _git_retry(["git", "-C", str(clone), "sparse-checkout", "set", s["path"]])
        head = subprocess.run(
            ["git", "-C", str(clone), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if head != s["commit"]:
            raise ValueError(f"{s['repo']} {s['tag']} is at {head}, pinned {s['commit']}")
        if dest.exists():
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(clone / s["path"], dest)
        _stdlib_marker(pin).write_text(head + "\n")
    return dest


def version(binary: Path) -> str:
    out = subprocess.run([str(binary), "--version"], capture_output=True, text=True, check=True)
    return out.stdout.strip()


@dataclass(frozen=True)
class Toolkit:
    """A located toolkit: the binary and the standard-library directory."""

    binary: Path
    stdlib: Path

    def run(self, *args: str, timeout: float = 300.0) -> subprocess.CompletedProcess:
        """Run ``sysmlv2 <args> --lib <stdlib>``; ``z3`` must be on ``PATH`` for ``verify``."""
        cmd = [str(self.binary), *args, "--lib", str(self.stdlib)]
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

    def check(self, model: Path | str) -> subprocess.CompletedProcess:
        return self.run("check", str(model))

    def lint(self, model: Path | str) -> dict:
        """The lint report as parsed JSON (``findings`` and ``summary``)."""
        out = self.run("lint", "--format", "json", str(model))
        return json.loads(out.stdout)

    def verify_solve(self, model: Path | str) -> subprocess.CompletedProcess:
        return self.run("verify", str(model), "--solve")


def locate() -> Toolkit:
    """The toolkit, or ``FileNotFoundError`` naming the exact provisioning command."""
    binary, lib = find_binary(), find_stdlib()
    if binary is None or lib is None:
        missing = [n for n, v in (("binary", binary), ("standard library", lib)) if v is None]
        raise FileNotFoundError(
            f"the pinned sysml-toolkit {' and '.join(missing)} not found; provision with: "
            f"{FETCH_COMMAND}  (or set SYSML_TOOLKIT_BIN and SYSML_TOOLKIT_LIB)"
        )
    return Toolkit(binary, lib)


def pin_line(triple: str | None = None) -> str:
    """``<repo> <tag> <asset name>`` for the platform, from the pin file."""
    pin = load_pin()
    asset = _asset_for(pin, triple or platform_triple())
    return f"{pin['toolkit']['repo']} {pin['toolkit']['tag']} {asset['name']}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m experiments.toolkit", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser(
        "fetch",
        help="obtain and verify the pinned toolkit (cache hit: no network)",
        description="Idempotent. Retries transient errors 3 times, then falls back to the "
        "release-assets API (GH_TOKEN or GITHUB_TOKEN used when set). Always verifies size and "
        "sha256 before extraction.",
    )
    f.add_argument("--lib-only", action="store_true", help="fetch only the standard library")
    f.add_argument("--binary-only", action="store_true", help="fetch only the binary")
    f.add_argument("--archive", type=Path, metavar="PATH", help="install from a local archive")
    sub.add_parser("pin", help="print '<repo> <tag> <asset name>' for this platform")
    sub.add_parser("where", help="print the located binary and library")
    args = ap.parse_args(argv)
    if args.cmd == "pin":
        print(pin_line())
        return 0
    if args.cmd == "fetch":
        pin = load_pin()
        if not args.lib_only:
            if args.archive is None and binary_cached(pin):
                print(f"binary: {cached_binary(pin)} (cache hit)")
            else:
                print(f"binary: {fetch_binary(archive=args.archive)}")
        if not args.binary_only:
            if stdlib_cached(pin):
                print(f"stdlib: {cached_stdlib(pin)} (cache hit)")
            else:
                print(f"stdlib: {fetch_stdlib()}")
        return 0
    print(f"binary: {find_binary()}\nstdlib: {find_stdlib()}\ncache:  {cache_dir()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
