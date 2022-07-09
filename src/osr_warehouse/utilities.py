"""Utilities."""


class MetricBoltSpecification:
    """Metric bolt specification."""

    def __init__(self, shaft: float, pitch: float, length: float):
        """Initialise metric bolt specification."""
        self.shaft = shaft
        self.pitch = pitch
        self.length = length

    def specification(self, length=False) -> str:
        """Bolt specification."""
        specification = f"{self.shaft_m}-{self.pitch}"
        if length:
            specification = f"{specification} x {self.length}"

        return specification

    @property
    def shaft_m(self) -> str:
        """Shaft size prefixed with 'M'."""
        return f"M{self.shaft}"

    def __str__(self) -> str:
        """Bolt specification including length."""
        return self.specification(length=True)
