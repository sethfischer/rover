"""Frame utilities."""

from osr_mechanical.bom.parts import port, starboard
from osr_mechanical.frame.side import FrameSide


class FrameSidePort(FrameSide):
    """Utility to create port frame side."""

    def __init__(self) -> None:
        """Port frame side."""
        super().__init__(port)


class FrameSideStarboard(FrameSide):
    """Utility to create starboard frame side."""

    def __init__(self) -> None:
        """Starboard frame side."""
        super().__init__(starboard)
