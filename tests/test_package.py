"""WP0 placeholder: the package imports and carries a version."""

import hyperbolic_trade_space as hts


def test_version_is_a_string() -> None:
    assert isinstance(hts.__version__, str)
    assert hts.__version__
