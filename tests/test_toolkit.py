"""The toolkit provisioning (WP15 D-8): idempotent fetch, bounded retry, API fallback, archive.

No test opens a network connection: openers are fakes, and the cache-hit tests make urllib, socket
and subprocess raise.
"""

from __future__ import annotations

import hashlib
import io
import json
import socket
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request

import pytest
from experiments import toolkit

TRIPLE = "x86_64-unknown-linux-gnu"

# The fixture's archive holds a shell script as the binary, which Windows cannot execute
# ([WinError 216]); the unpacked binary is run for its version, so these tests need a POSIX
# executable. The provisioning code itself ran against the real sysmlv2.exe on Windows (WP34 spike).
posix_binary = pytest.mark.skipif(
    sys.platform == "win32",
    reason="the fixture archive's binary is a shell script; Windows runs only the real sysmlv2.exe",
)


def make_archive(path, payload=b"#!/bin/sh\necho 'sysmlv2 0.12.0'\n"):
    with tarfile.open(path, "w:gz") as tar:
        info = tarfile.TarInfo("sysmlv2-0.12.0/sysmlv2")
        info.size = len(payload)
        tar.addfile(info, io.BytesIO(payload))
    return path


@pytest.fixture
def pinned(tmp_path, monkeypatch):
    """A pin whose linux asset is a small real archive; cache redirected to tmp_path."""
    archive = make_archive(tmp_path / "good.tar.gz")
    pin = toolkit.load_pin()
    pin["toolkit"]["assets"][TRIPLE] = {
        "name": "sysmlv2-test.tar.gz",
        "size": archive.stat().st_size,
        "sha256": toolkit.sha256_of(archive),
    }
    monkeypatch.setattr(toolkit, "load_pin", lambda path=toolkit.PIN_PATH: pin)
    monkeypatch.setenv("SYSML_TOOLKIT_CACHE", str(tmp_path / "cache"))
    monkeypatch.setattr(toolkit, "platform_triple", lambda *a, **k: TRIPLE)
    return pin, archive


class Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


def http_error(code):
    return urllib.error.HTTPError("u", code, "err", {}, None)


class FakeOpener:
    """Maps URL to bytes or an exception (or a list of them, consumed in order)."""

    def __init__(self, routes):
        self.routes = {k: (list(v) if isinstance(v, list) else [v]) for k, v in routes.items()}
        self.log = []

    def __call__(self, req, timeout=None):
        self.log.append((req.full_url, dict(req.header_items())))
        queue = self.routes[req.full_url]
        item = queue.pop(0) if len(queue) > 1 else queue[0]
        if isinstance(item, Exception):
            raise item
        return Resp(item)


def no_sleep(_):
    return None


# --- cache hit: no connection at all -------------------------------------------------------------


@posix_binary
def test_cache_hit_opens_no_connection(pinned, monkeypatch, capsys):
    pin, archive = pinned
    toolkit.fetch_binary(archive=archive)  # populate the binary
    monkeypatch.setattr(toolkit, "version", lambda b: pin["toolkit"]["version_output"])
    toolkit.cache_dir(pin).joinpath("stdlib").mkdir(parents=True, exist_ok=True)
    toolkit.cache_dir(pin).joinpath("stdlib.commit").write_text(
        pin["stdlib"]["commit"] + "\n", encoding="utf-8"
    )

    def boom(*a, **k):
        raise AssertionError("network or subprocess used on a cache hit")

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    monkeypatch.setattr(socket, "create_connection", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(subprocess, "run", boom)
    assert toolkit.main(["fetch"]) == 0
    out = capsys.readouterr().out
    assert out.count("cache hit") == 2


def test_stdlib_at_another_commit_is_not_a_hit(pinned):
    pin, _ = pinned
    d = toolkit.cache_dir(pin)
    (d / "stdlib").mkdir(parents=True)
    (d / "stdlib.commit").write_text("0" * 40 + "\n", encoding="utf-8")
    assert not toolkit.stdlib_cached(pin)


# --- retry ---------------------------------------------------------------------------------------


@posix_binary
def test_retry_on_transient_then_success(pinned):
    pin, archive = pinned
    name = pin["toolkit"]["assets"][TRIPLE]["name"]
    url = toolkit.asset_url(pin, name)
    op = FakeOpener({url: [http_error(504), TimeoutError("t"), archive.read_bytes()]})
    toolkit.fetch_binary(opener=op, sleep=no_sleep)
    assert [u for u, _ in op.log] == [url] * 3


def test_a_client_error_is_not_retried(tmp_path):
    calls = []

    def fn():
        calls.append(1)
        raise http_error(404)

    with pytest.raises(urllib.error.HTTPError):
        toolkit.with_retry(fn, sleep=no_sleep)
    assert len(calls) == 1


def test_retry_is_bounded(tmp_path):
    calls = []

    def fn():
        calls.append(1)
        raise http_error(503)

    with pytest.raises(urllib.error.HTTPError):
        toolkit.with_retry(fn, sleep=no_sleep)
    assert len(calls) == toolkit.ATTEMPTS == 3


def test_git_step_is_retried(monkeypatch):
    calls = []

    def run(cmd, **k):
        calls.append(cmd)
        if len(calls) < 3:
            raise subprocess.CalledProcessError(128, cmd)
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", run)
    monkeypatch.setattr(toolkit.time, "sleep", lambda s: None)
    toolkit._git_retry(["git", "clone"])
    assert len(calls) == 3


# --- API fallback --------------------------------------------------------------------------------


def api_routes(pin, name, payload):
    t = pin["toolkit"]
    base = f"https://api.github.com/repos/{t['repo']}/releases"
    release = json.dumps({"assets": [{"id": 4242, "name": name}, {"id": 1, "name": "other"}]})
    return base, {
        toolkit.asset_url(pin, name): http_error(504),
        f"{base}/tags/{t['tag']}": release.encode(),
        f"{base}/assets/4242": payload,
    }


@posix_binary
def test_fallback_to_the_release_assets_api(pinned, monkeypatch):
    pin, archive = pinned
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    name = pin["toolkit"]["assets"][TRIPLE]["name"]
    base, routes = api_routes(pin, name, archive.read_bytes())
    op = FakeOpener(routes)
    dest = toolkit.fetch_binary(opener=op, sleep=no_sleep)
    assert dest.is_file()
    urls = [u for u, _ in op.log]
    assert urls[-2:] == [f"{base}/tags/{pin['toolkit']['tag']}", f"{base}/assets/4242"]
    last = {k.lower(): v for k, v in op.log[-1][1].items()}
    assert last["accept"] == "application/octet-stream"
    assert "authorization" not in last


@posix_binary
def test_api_fallback_sends_the_token(pinned, monkeypatch):
    pin, archive = pinned
    monkeypatch.setenv("GH_TOKEN", "tok123")
    name = pin["toolkit"]["assets"][TRIPLE]["name"]
    _, routes = api_routes(pin, name, archive.read_bytes())
    op = FakeOpener(routes)
    toolkit.fetch_binary(opener=op, sleep=no_sleep)
    for _, headers in op.log[-2:]:
        assert {k.lower(): v for k, v in headers.items()}["authorization"] == "Bearer tok123"


def test_api_route_is_as_strict_as_direct(pinned, monkeypatch):
    pin, archive = pinned
    name = pin["toolkit"]["assets"][TRIPLE]["name"]
    _, routes = api_routes(pin, name, archive.read_bytes() + b"tampered")
    with pytest.raises(ValueError, match="size"):
        toolkit.fetch_binary(opener=FakeOpener(routes), sleep=no_sleep)
    assert not toolkit.cached_binary(pin).exists()


def test_direct_route_verifies_too(pinned):
    pin, archive = pinned
    name = pin["toolkit"]["assets"][TRIPLE]["name"]
    data = bytearray(archive.read_bytes())
    data[-1] ^= 1  # same size, different digest
    op = FakeOpener({toolkit.asset_url(pin, name): bytes(data)})
    with pytest.raises(ValueError, match="sha256"):
        toolkit.fetch_binary(opener=op, sleep=no_sleep)
    assert not toolkit.cached_binary(pin).exists()


# --- local archive -------------------------------------------------------------------------------


@posix_binary
def test_local_archive_installs_when_it_matches(pinned):
    pin, archive = pinned
    assert toolkit.fetch_binary(archive=archive) == toolkit.cached_binary(pin)
    assert toolkit.cached_binary(pin).is_file()


def test_tampered_local_archive_is_never_extracted(pinned, tmp_path, monkeypatch):
    pin, _ = pinned
    bad = make_archive(tmp_path / "bad.tar.gz", payload=b"#!/bin/sh\necho evil\n")
    monkeypatch.setattr(
        toolkit, "_extract_binary", lambda *a: pytest.fail("extracted an unverified archive")
    )
    with pytest.raises(ValueError):
        toolkit.fetch_binary(archive=bad)
    assert not toolkit.cached_binary(pin).exists()


@posix_binary
def test_cli_fetch_archive(pinned, capsys):
    pin, archive = pinned
    assert toolkit.main(["fetch", "--binary-only", "--archive", str(archive)]) == 0
    assert str(toolkit.cached_binary(pin)) in capsys.readouterr().out


# --- pin subcommand ------------------------------------------------------------------------------


@pytest.mark.parametrize("triple", sorted(toolkit.load_pin()["toolkit"]["assets"]))
def test_pin_line_per_platform(triple):
    pin = toolkit.load_pin()
    assert toolkit.pin_line(triple) == (
        f"Open-MBEE/sysml-toolkit v0.12.0 {pin['toolkit']['assets'][triple]['name']}"
    )


def test_pin_subcommand_uses_the_running_platform(monkeypatch, capsys):
    monkeypatch.setattr(toolkit, "platform_triple", lambda *a, **k: TRIPLE)
    assert toolkit.main(["pin"]) == 0
    assert capsys.readouterr().out.strip() == (
        "Open-MBEE/sysml-toolkit v0.12.0 sysmlv2-0.12.0-x86_64-unknown-linux-gnu.tar.gz"
    )


def test_the_pinned_values_are_unchanged():
    t = toolkit.load_pin()["toolkit"]["assets"][TRIPLE]
    assert t["sha256"] == "0f17df5c0eefbfc1715e98a30c533476a7323c2d20145065589fbf7d2227d497"
    assert t["size"] == 6300846
    assert toolkit.asset_url(toolkit.load_pin(), t["name"]) == (
        "https://github.com/Open-MBEE/sysml-toolkit/releases/download/v0.12.0/" + t["name"]
    )


def test_sha256_helper_matches_hashlib(tmp_path):
    f = tmp_path / "x"
    f.write_bytes(b"abc")
    assert toolkit.sha256_of(f) == hashlib.sha256(b"abc").hexdigest()
