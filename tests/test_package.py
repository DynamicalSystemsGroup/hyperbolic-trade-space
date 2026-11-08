"""WP0 placeholder: the package imports and carries a version."""

import posynomial_invariant_form as pif


def test_version_is_a_string() -> None:
    assert isinstance(pif.__version__, str)
    assert pif.__version__
