"""Abstract base classes for CadQuery object containers."""

from __future__ import annotations

from abc import ABC, abstractmethod

import cadquery as cq

from osr_mechanical.bom.parts import PartIdentifier


class CqAssemblyContainer(ABC):
    """Abstract base class for CadQuery assembly containers."""

    _cq_object: cq.Assembly

    @property
    def cq_object(self) -> cq.Assembly:
        """Get CadQuery object."""
        return self._cq_object

    def cq_part(self, name: str) -> cq.Shape | cq.Workplane:
        """Get part from CadQuery assembly."""
        result = self._cq_object.objects[name].obj
        if result is None:
            raise Exception("Part is not a valid Shape or Workplane.")

        return result

    @abstractmethod
    def _make(self) -> cq.Assembly:
        """Create CadQuery object."""
        ...

    @abstractmethod
    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        ...
