"""Version string tests."""

from osr_mechanical import __version__


def test_version() -> None:
    """Test version string is available."""
    assert __version__ == "0.1.0"
