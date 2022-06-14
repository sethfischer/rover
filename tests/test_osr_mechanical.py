"""Tests for OSR mechanical design."""

from osr_mechanical import __version__


def test_version():
    """Test version string is available."""
    assert __version__ == "0.1.0"
