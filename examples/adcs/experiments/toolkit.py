"""The pinned model-checking toolkit: where it is, how to obtain it, and how to run it (WP15 D-8).

The toolkit (``sysmlv2``, a Rust CLI: ``check``, ``lint``, ``verify --solve``) is not on PyPI. The
pin in ``toolkit-pin.toml`` names a release, one archive per platform with its size and sha256, and
the standard-library directory the CLI needs (``--lib``). Nothing is downloaded unless somebody
runs the fetch command explicitly::

    uv run python -m experiments.toolkit fetch

The archive is verified against its pinned size and sha256 before a byte of it is extracted, the
binary is then checked to report the pinned version, and the standard library is taken from a
sparse git clone whose HEAD must equal the pinned commit. An unverified file is never executed.

Where the binary is looked for, first hit wins: ``SYSML_TOOLKIT_BIN`` (the legacy ``SYSMLV2_BIN``),
the cache directory (``SYSML_TOOLKIT_CACHE``, default ``~/.cache/hyperbolic-trade-space/
sysml-toolkit``), then ``sysmlv2`` on ``PATH``. The library directory: ``SYSML_TOOLKIT_LIB`` (legacy
``SYSMLV2_LIB``), then the cache. ``z3`` must be on ``PATH`` for ``verify --solve`` (the ``case``
dependency group installs it into the environment).

The alternative route, a source build, gives the same binary::

    git clone --branch v0.12.0 https://github.com/Open-MBEE/sysml-toolkit && cd sysml-toolkit
    cargo build --release --locked -p sysmlv2-cli      # toolchain from rust-toolchain.toml
    export SYSML_TOOLKIT_BIN=$PWD/target/release/sysmlv2

with ``SYSML_TOOLKIT_LIB`` pointing at the pinned standard-library directory (``fetch`` can supply
it alone: ``uv run python -m experiments.toolkit fetch --lib-only``).
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
import tomllib
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN_PATH = HERE / "toolkit-pin.toml"
FETCH_COMMAND = "uv run python -m experiments.toolkit fetch"


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


def fetch_binary(triple: str | None = None) -> Path:
    """Download the pinned archive, verify size and sha256, extract the binary, check version."""
    pin = load_pin()
    triple = triple or platform_triple()
    try:
        asset = pin["toolkit"]["assets"][triple]
    except KeyError:
        raise SystemExit(
            f"no pinned archive for {triple}; build from source instead (see the module docstring)"
        ) from None
    dest = cached_binary(pin)
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / asset["name"]
        with (
            urllib.request.urlopen(asset_url(pin, asset["name"])) as resp,
            open(archive, "wb") as f,
        ):
            shutil.copyfileobj(resp, f)
        verify_archive(archive, asset["size"], asset["sha256"])  # before any extraction
        _extract_binary(archive, pin["toolkit"]["binary"], dest)
    got = version(dest)
    if got != pin["toolkit"]["version_output"]:
        dest.unlink()
        raise ValueError(f"{dest} reports {got!r}, pinned {pin['toolkit']['version_output']!r}")
    return dest


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
        subprocess.run(clone_cmd, check=True)
        subprocess.run(["git", "-C", str(clone), "sparse-checkout", "set", s["path"]], check=True)
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m experiments.toolkit", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="download and verify the pinned toolkit (network)")
    f.add_argument("--lib-only", action="store_true", help="fetch only the standard library")
    f.add_argument("--binary-only", action="store_true", help="fetch only the binary")
    sub.add_parser("where", help="print the located binary and library")
    args = ap.parse_args(argv)
    if args.cmd == "fetch":
        if not args.lib_only:
            print(f"binary: {fetch_binary()}")
        if not args.binary_only:
            print(f"stdlib: {fetch_stdlib()}")
        return 0
    print(f"binary: {find_binary()}\nstdlib: {find_stdlib()}\ncache:  {cache_dir()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
