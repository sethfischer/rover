"""Abstract base classes for CadQuery object containers."""

from __future__ import annotations

from abc import ABC, abstractmethod

import cadquery as cq

from osr_mechanical.bom.parts import PartIdentifier


class CqAssemblyContainer(ABC):
    """Abstract base class for CadQuery assembly containers."""

    @property
    @abstractmethod
    def cq_object(self) -> cq.Assembly:
        """Get CadQuery object."""
        pass

    @abstractmethod
    def _make(self) -> cq.Assembly:
        """Create CadQuery object."""
        pass

    @abstractmethod
    def cq_part(self, name: str) -> cq.Shape | cq.Workplane:
        """Get part from CadQuery assembly."""
        pass

    @abstractmethod
    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        pass
