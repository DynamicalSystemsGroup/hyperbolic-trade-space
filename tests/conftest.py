"""Shared pytest configuration.

Verification in tiers (docs/superpowers/notes/verification-strategy.md):

* ``slow`` marks a test that takes over about five seconds (``pytest --durations=60`` lists them).
  ``uv run pytest -m "not slow"`` is the fast suite (tier 1); ``uv run pytest`` is the full suite.
* Tests that build the site or write shared files run in the one ``xdist_group("site")``, so under
  ``-n auto --dist loadgroup`` they never run at the same time. A test requesting one of the
  fixtures in ``SITE_FIXTURES`` is slow and in that group without a decorator.
"""

import os

import pytest

os.environ.setdefault("MPLBACKEND", "Agg")

SITE_FIXTURES = frozenset({"assembled", "generated_dir"})
SITE_MODULES = frozenset({"test_build_generated.py"})
# Fixtures whose set-up costs a minute: every test that requests one is slow.
SLOW_FIXTURES = frozenset({"_ctx_all"})


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: takes over about five seconds; excluded from the fast suite"
    )
    config.addinivalue_line(
        "markers", "xdist_group(name): run the tests of one name on one worker (--dist loadgroup)"
    )


def pytest_collection_modifyitems(config, items):
    for item in items:
        if SLOW_FIXTURES & set(getattr(item, "fixturenames", ())):
            item.add_marker(pytest.mark.slow)
        in_site = bool(SITE_FIXTURES & set(getattr(item, "fixturenames", ()))) or (
            item.path.name in SITE_MODULES
        )
        if in_site:
            item.add_marker(pytest.mark.slow)
            if item.get_closest_marker("xdist_group") is None:
                item.add_marker(pytest.mark.xdist_group("site"))
