# Security policy

## Reporting a vulnerability

Please report a vulnerability privately, not in a public issue. Use GitHub's private vulnerability reporting:
the repository's **Security** tab, then **Report a vulnerability**. If that is unavailable to you, open an issue
that says only that you have a security report and asks for a private channel; leave out the details.

Include the version (`hyperbolic_trade_space.__version__`), what you did, what happened, and what you expected.
A code owner acknowledges a report within a week and tells you what will be done and when.

This file is for reporting a vulnerability; it does not govern releases (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Supported versions

Only the latest release receives security fixes.

## Scope

The package is a numerical library: it reads arrays and writes arrays, files only where the examples say so, and
makes no network calls. Releases are published to PyPI by trusted publishing from a tag on `main`; no publishing
token exists in the repository (see `docs/code-owners.md`).
