"""Exception classes."""

from typing import Any


class CadQueryTypeError(Exception):
    """CadQuery type error."""

    def __init__(self, expected: Any, got: Any) -> None:
        """Initialise CadQueryTypeError."""
        self.msg = (
            f"Expected {expected.__module__}.{expected.__name__}, got {type(got)}"
        )

    def __str__(self) -> str:
        """Exception message."""
        return self.msg
