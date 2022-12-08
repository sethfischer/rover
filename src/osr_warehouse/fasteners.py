"""Fastener utilities."""

M5_CLEARANCE_CLOSE_DIAMETER = 5.3
M5_COUNTERBORE_DIAMETER = 9.75


class MetricBoltSpecification:
    """Metric bolt specification."""

    def __init__(self, shaft: float, pitch: float, length: float) -> None:
        """Initialise MetricBoltSpecification."""
        self.shaft = shaft
        self.pitch = pitch
        self.length = length

    def specification(self, length: bool = False) -> str:
        """Bolt specification."""
        specification = f"{self.shaft_m}-{self.pitch}"
        if length:
            specification = f"{specification} x {self.length}"

        return specification

    @property
    def shaft_m(self) -> str:
        """Shaft size prefixed with 'M'."""
        return f"M{self.shaft}"

    @staticmethod
    def split_shaft_pitch(shaft_pitch: str) -> list[str]:
        """Split shaft diameter and pitch components."""
        return shaft_pitch.split("-")

    def __str__(self) -> str:
        """Bolt specification including length."""
        return self.specification(length=True)
