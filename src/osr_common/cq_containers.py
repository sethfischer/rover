"""Abstract base classes for CadQuery object containers."""

from abc import ABC, abstractmethod

import cadquery as cq

from osr_mechanical.bom.parts import PartIdentifier


class CqSketchContainer(ABC):
    """Abstract base class for CadQuery Sketch containers."""

    _cq_object: cq.Sketch

    @property
    def cq_object(self) -> cq.Sketch:
        """Get CadQuery object."""
        return self._cq_object

    @abstractmethod
    def _make(self) -> cq.Sketch:
        """Create CadQuery object."""
        ...


class CqWorkplaneContainer(ABC):
    """Abstract base class for CadQuery Workplane containers."""

    _cq_object: cq.Workplane

    @property
    def cq_object(self) -> cq.Workplane:
        """Get CadQuery object."""
        return self._cq_object

    @abstractmethod
    def _make(self) -> cq.Workplane:
        """Create CadQuery object."""
        ...


class CqAssemblyContainer(ABC):
    """Abstract base class for CadQuery Assembly containers."""

    _cq_object: cq.Assembly
    _name: str

    @property
    def cq_object(self) -> cq.Assembly:
        """Get CadQuery object."""
        return self._cq_object

    @property
    def name(self) -> str:
        """Assembly name."""
        return self._name

    def cq_part(self, name: str) -> cq.Shape | cq.Workplane:
        """Get part from CadQuery assembly."""
        result = self._cq_object.objects[name].obj

        if result is None:
            raise Exception(f"Invalid name: '{name}'.")

        return result

    def sub_assembly_name(self, name: str) -> str:
        """Sub assembly name."""
        return f"{self._name}__{name}"

    @abstractmethod
    def _make(self) -> cq.Assembly:
        """Create CadQuery object."""
        ...

    @abstractmethod
    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        ...
